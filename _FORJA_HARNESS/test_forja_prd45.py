import hashlib
import json
import tempfile
import unittest
from pathlib import Path

import jsonschema

from forja_disciplinas import (
    build_d1_briefing,
    build_d3_hypotheses,
    build_d4_uncertain_decisions,
    build_d5_handoff,
    consume_d1_briefing,
    consume_d5_handoff,
    reconcile_f9,
    reopen_hypothesis,
    validate_d1_briefing,
    validate_d3_hypotheses,
    validate_d4_uncertain_decisions,
    validate_d5_handoff,
    validate_decisions_directory,
    write_d6_decision,
)
from forja_exploracao_100 import build_scaffold, gates_da_exploracao, validate_exploration_100
from forja_grafo_lint import lint_graph
from forja_instrumentacao import (
    InstrumentationError,
    append_observation,
    effective_mode,
    metrics_for_case,
    observation_metrics,
    validate_ledger,
    validate_observation,
)
from forja_proposition_evidence import reconcile_f7, validate_map, verify_f3_immutable
from forja_severidade import blocking_findings
from forja_stop_reason import build_stop_receipt, extract_stop_reason


class SeverityAndF2Tests(unittest.TestCase):
    def test_p1_stays_visible_and_does_not_fail_computed_gates(self):
        payload = build_scaffold("case-p1", "Âncora de teste suficientemente específica")
        for item in payload["questions"]:
            item.update({
                "caseAnchor": f"Âncora do caso {item['questionId']} com materialidade",
                "status": "answered",
                "answer": "Resposta desenvolvida para o caso de teste e seu impacto.",
                "epistemicStatus": "legal_inference",
                "downstreamTargets": ["F3", "F4"],
            })
            if item["category"] in {"fact", "evidence", "procedural_event", "precedent", "calculation"}:
                item["supportIds"] = ["SRC-001"]
            item.pop("unansweredConsequence", None)
        payload["problemDefinition"] = "Definição material do problema para validação do F2A."
        payload["diagnosticSynthesis"] = "Síntese diagnóstica detalhada das dez óticas, das evidências, das lacunas e das consequências decisórias."
        payload["coverage"].update({"answeredMaterial": 100, "blockedMaterial": 0})
        payload["solutionHypotheses"] = [
            {"hypothesisId": "H1", "description": "Hipótese principal suficientemente descrita.", "conditions": ["condição"], "risks": ["risco"], "questionIds": ["Q001"], "downstreamTargets": ["F4"]},
            {"hypothesisId": "H2", "description": "Hipótese subsidiária suficientemente descrita.", "conditions": ["condição"], "risks": ["risco"], "questionIds": ["Q002"], "downstreamTargets": ["F4"]},
        ]
        payload["downstreamHandoff"] = {phase: ["Q001"] for phase in ("F3", "F4", "F5", "F6", "F7")}
        payload["draftRelease"] = "ready_for_drafting"
        findings = validate_exploration_100(payload)
        self.assertFalse(blocking_findings(findings))
        self.assertTrue({item["code"] for item in findings} >= {"N4-Q-100-DIVERSITY", "N4-Q-100-NO-GAP"})
        report = gates_da_exploracao(payload)
        self.assertTrue(all(value == "pass" for value in report["gates"].values()))
        self.assertEqual([], report["blockingFindings"])

    def test_missing_severity_fails_closed(self):
        self.assertEqual("p0", blocking_findings([{"code": "novo"}])[0]["severity"])


class ObservationTests(unittest.TestCase):
    def record(self, **overrides):
        value = {
            "schemaVersion": 1, "opportunityId": "OP-1", "caseId": "case-x", "disciplineId": "D2",
            "triggerEventId": "evt-1", "triggerSequence": 10, "registeredAt": "2026-08-06T00:00:00Z",
            "eligible": True, "eligibilityReason": "proposição decisiva", "dispatchEventId": "evt-2",
            "nonDispatchReason": "", "artifactPath": "map.json", "artifactSha256": "a" * 64,
            "consumerEventId": "evt-3", "consumerSequence": 11, "consumedSha256": "a" * 64, "humanReviewer": "igor",
            "humanAudit": {"status": "audited"}, "materialOutcome": {"correction": False}, "costMinutes": 5,
            "arExperimentId": "AR-45",
        }
        value.update(overrides)
        return value

    def test_append_replay_and_denominator(self):
        with tempfile.TemporaryDirectory() as temp:
            case = Path(temp) / "case-x"
            first = append_observation(case, self.record())
            replay = append_observation(case, self.record())
            self.assertEqual(first["recordSha256"], replay["recordSha256"])
            self.assertEqual(1, validate_ledger(case)["uniqueOpportunities"])
            self.assertEqual(1, metrics_for_case(case)["eligible"])
            self.assertEqual(1.0, metrics_for_case(case)["adoption"])

    def test_eligibility_and_non_dispatch_are_fail_closed(self):
        with self.assertRaises(InstrumentationError):
            append_observation(Path(tempfile.mkdtemp()), self.record(dispatchEventId="", nonDispatchReason=""))
        with tempfile.TemporaryDirectory() as temp:
            case = Path(temp) / "case-x"
            append_observation(case, self.record(opportunityId="OP-2", eligible=False, eligibilityReason="sem linha material", dispatchEventId="", consumerEventId="", consumedSha256=""))
            self.assertEqual("not_applicable", observation_metrics([])["status"])
            self.assertEqual(0, metrics_for_case(case)["eligible"])

    def test_hash_consumption_mismatch_is_rejected(self):
        findings = validate_observation(self.record(consumedSha256="b" * 64))
        self.assertIn("OBS-12", {item["code"] for item in findings})
        findings = validate_observation(self.record(consumerSequence=10))
        self.assertIn("OBS-20", {item["code"] for item in findings})

    def test_schema_is_valid(self):
        for name in ("observation_ledger.schema.json", "proposition_evidence_map.schema.json", "instrumentation_config.schema.json"):
            schema = json.loads((Path("contracts") / name).read_text(encoding="utf-8"))
            jsonschema.Draft202012Validator.check_schema(schema)

    def test_rollout_mode_is_explicit(self):
        self.assertEqual("off", effective_mode({}))
        self.assertEqual("observe", effective_mode({"instrumentation": {"mode": "observe"}}))
        with self.assertRaises(InstrumentationError):
            effective_mode({"instrumentation": {"mode": "unknown"}})


class EvidenceAndGraphTests(unittest.TestCase):
    def test_evidence_map_good_bad_and_blocked(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source_path = root / "official.txt"
            source_path.write_text("fonte oficial integral", encoding="utf-8")
            digest = hashlib.sha256(source_path.read_bytes()).hexdigest()
            propositions = {"propositions": [{"id": "P1", "decisive": True, "claim": "tese"}, {"id": "P2", "decisive": True}]}
            sources = {"sources": [{"id": "S1", "path": str(source_path), "sha256": digest}]}
            good = {"schemaVersion": 1, "caseId": "case-x", "producerPhase": "F5_PESQUISA_OFICIAL", "producerRunId": "run-1", "propositionLedger": {"artifactId": "proposition_ledger", "sha256": "a" * 64}, "sourceLedger": {"artifactId": "source_ledger", "sha256": "b" * 64}, "links": [{"linkId": "L1", "propositionId": "P1", "sourceId": "S1", "relation": "supports", "sourceLocator": "p. 1", "archivedSourceSha256": digest, "reviewStatus": "pending_human_review"}], "blockedPropositions": [{"propositionId": "P2", "reason": "fonte oficial ainda não localizada"}]}
            self.assertNotIn("EVID-01", {item["code"] for item in validate_map(good, propositions, sources, source_base_dir=root)})
            reconciled = reconcile_f7(good, sources)
            self.assertTrue(reconciled["approvedForObservation"])
            unknown = dict(good, links=[dict(good["links"][0], sourceId="S9")])
            self.assertIn("EVID-03", {item["code"] for item in validate_map(unknown, propositions, sources)})
            swapped = dict(good, links=[dict(good["links"][0], archivedSourceSha256="c" * 64)])
            self.assertIn("EVID-04", {item["code"] for item in validate_map(swapped, propositions, sources, source_base_dir=root)})
            self.assertEqual([], [item for item in validate_map(good, propositions, sources) if item["severity"] == "p0"])

    def test_graph_lint_is_diagnostic_and_ontology_warns(self):
        graph = {"nodes": [{"id": "S1", "type": "official_source"}, {"id": "T1", "type": "thesis"}, {"id": "Q1", "type": "request"}, {"id": "L1", "type": "legacy_type"}], "edges": [{"edgeId": "E1", "from": "S1", "to": "T1", "relation": "supports", "scope": "full", "reason": "fonte"}, {"edgeId": "E2", "from": "T1", "to": "Q1", "relation": "justifies", "scope": "full", "reason": "tese"}]}
        report = lint_graph(graph)
        codes = {item["code"] for item in report["findings"]}
        self.assertIn("GRAFO-05", codes)
        self.assertIn("GRAFO-06", codes)
        self.assertEqual([], report["blocking"])


class DisciplineAndStopTests(unittest.TestCase):
    def test_d1_d3_d4_d5_d6_contracts(self):
        d1 = build_d1_briefing(case_id="case-x", trigger_event_id="evt-1", trigger_sequence=1, questions=[{"questionId": "Q1", "order": 1}], sources=[{"sourceId": "S1", "sha256": "a" * 64}])
        self.assertEqual([], validate_d1_briefing(d1))
        self.assertEqual("evt-2", consume_d1_briefing(d1, consumer_event_id="evt-2", consumer_sequence=2)["consumerEventId"])
        d3 = build_d3_hypotheses(case_id="case-x", trigger_event_id="evt-1", trigger_sequence=1, hypotheses=[{"statement": "hipótese"}])
        self.assertEqual([], validate_d3_hypotheses(d3))
        reopened = reopen_hypothesis(d3, "H-001", reason="fonte posterior contradiz", actor="igor", event_id="evt-4")
        self.assertEqual("reopened", reopened["hypotheses"][0]["status"])
        d4 = build_d4_uncertain_decisions(case_id="case-x", trigger_event_id="evt-5", trigger_sequence=5, items=[{"uncertainty": "identidade", "sourceLocator": "p. 2", "action": "diligence"}])
        self.assertEqual([], validate_d4_uncertain_decisions(d4))
        mapped = reconcile_f9(d4, consumer_event_id="evt-6", consumer_sequence=6)
        self.assertNotIn("decisionId", mapped["externalSafeMap"][0])
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            artifact = root / "source.md"
            artifact.write_text("conteúdo", encoding="utf-8")
            d5 = build_d5_handoff(case_id="case-x", trigger_event_id="evt-7", trigger_sequence=7, artifact_path=artifact, receiver="revisor", traps=["não usar fonte sem hash"])
            self.assertEqual([], validate_d5_handoff(d5, artifact_path=artifact))
            self.assertEqual("evt-8", consume_d5_handoff(d5, consumer_event_id="evt-8", consumer_sequence=8, received_sha256=d5["artifactSha256"])["consumerEventId"])
            decisions = root / "decisoes"
            write_d6_decision({"schemaVersion": 1, "decisionId": "D-1", "topic": "teste", "status": "decided", "decision": "decisão", "source": "fonte", "reopenWhen": "fato novo"}, decisions)
            self.assertTrue(validate_decisions_directory(decisions)["approved"])

    def test_stop_reason_outcomes(self):
        self.assertEqual("end_turn", extract_stop_reason({"stop_reason": "end_turn"}))
        self.assertEqual("missing_stop_reason", build_stop_receipt({})["stopReason"])
        self.assertEqual("invalid_output", build_stop_receipt({}, parse_error="marcador ausente")["stopReason"])
        self.assertEqual("model_divergence", build_stop_receipt({}, expected_model="gpt", actual_model="claude")["stopReason"])

    def test_f3_hash_helper(self):
        with tempfile.TemporaryDirectory() as temp:
            before = Path(temp) / "before.json"
            after = Path(temp) / "after.json"
            before.write_text("{}", encoding="utf-8")
            after.write_text("{}", encoding="utf-8")
            self.assertTrue(verify_f3_immutable(before, after)["unchanged"])
            after.write_text("{\"changed\":true}", encoding="utf-8")
            self.assertFalse(verify_f3_immutable(before, after)["unchanged"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
