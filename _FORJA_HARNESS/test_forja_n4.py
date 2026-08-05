from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import jsonschema

from forja_case_tests import run_suite, suite_hash, validate_results, validate_suite
from forja_consistency import (
    validate_comparison,
    validate_delivery,
    validate_event_identity,
    validate_global,
    validate_intertemporal,
    validate_quantification,
)
from forja_learning import validate_feedback_assimilation, validate_learning
from forja_metacognition import validate_metacognition
from forja_n4_common import ARTIFACT_SPECS, build_envelope, validate_envelope, write_artifact
from forja_n4_validate import validate_case
from forja_n4_invalidation import invalidate
from forja_reasoning import validate_conducts, validate_coverage, validate_graph, validate_question_tree, validate_theses
from forja_science import validate_claims, validate_studies, validate_synthesis
from forja_render_docx import _tipo_produto
from forja_delivery_integrity import confirm, select


def codes(findings: list[dict]) -> set[str]:
    return {item["code"] for item in findings}


class ForjaN4Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.case = Path(self.temp.name) / "case-n4-test"
        self.case.mkdir()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_schema_catalog_covers_every_artifact_and_resolves(self):
        root = Path(__file__).parent / "n4_schemas"
        catalog = json.loads((root / "ARTIFACT_CATALOG.json").read_text(encoding="utf-8"))
        self.assertEqual(set(ARTIFACT_SPECS), set(catalog["artifacts"]))
        for item in catalog["artifacts"].values():
            schema = json.loads((root / item["schema"]).read_text(encoding="utf-8"))
            jsonschema.Draft202012Validator.check_schema(schema)

    def test_render_classifies_internal_diagnostic_without_weakening_petitions(self):
        self.assertEqual("estudo", _tipo_produto("# DIAGNÓSTICO INTERNO", "Diagnóstico"))
        self.assertEqual("peca", _tipo_produto("EXCELENTÍSSIMO SENHOR DESEMBARGADOR", "Petição inicial"))

    def test_envelope_hash_and_independent_review(self):
        payload = build_envelope(self.case, "F2_QUESTION_TREE.json", {"questions": [], "coverage": {"total": 0, "material": 0, "answeredMaterial": 0, "blockedMaterial": 0}}, source_hashes=[], producer_run_id="run-a", reviewer_run_id="run-b", status="approved")
        self.assertEqual([], validate_envelope(self.case, "F2_QUESTION_TREE.json", payload))
        payload["reviewerRunId"] = "run-a"
        self.assertIn("N4-ENV-SELF-REVIEW", codes(validate_envelope(self.case, "F2_QUESTION_TREE.json", payload)))

    def test_required_cannot_be_not_applicable(self):
        payload = build_envelope(self.case, "F2_QUESTION_TREE.json", {"justification": "x"}, source_hashes=[], producer_run_id="a", applicability="required", status="not_applicable")
        self.assertIn("N4-ENV-REQUIRED-NA", codes(validate_envelope(self.case, "F2_QUESTION_TREE.json", payload)))

    def test_material_question_requires_answer_or_block(self):
        payload = {"questions": [{"questionId": "Q1", "category": "fact", "materiality": "decisive", "status": "pending"}], "coverage": {"total": 1, "material": 1, "answeredMaterial": 0, "blockedMaterial": 0}}
        self.assertIn("N4-Q-UNRESOLVED", codes(validate_question_tree(payload)))

    def test_answered_fact_requires_support(self):
        payload = {"questions": [{"questionId": "Q1", "category": "fact", "materiality": "decisive", "status": "answered", "answer": "sim", "supportIds": []}], "coverage": {"total": 1, "material": 1, "answeredMaterial": 1, "blockedMaterial": 0}}
        self.assertIn("N4-Q-NO-SUPPORT", codes(validate_question_tree(payload)))

    def test_estado_fora_do_contrato_e_recusado(self):
        """Os estados `retired` e `accepted_by_human` saíram em 25/07/2026.

        O schema F2-A nunca os admitiu e nenhuma árvore real os usava; enquanto
        eram tolerados aqui, um produtor podia emiti-los e escapar do exame. A
        regra vale para qualquer materialidade.
        """
        for estado in ("retired", "accepted_by_human", "quase_pronta"):
            payload = {"questions": [{"questionId": "Q1", "category": "risk", "materiality": "minor", "status": estado}], "coverage": {"total": 1, "material": 0, "answeredMaterial": 0, "blockedMaterial": 0}}
            self.assertIn("N4-Q-STATUS", codes(validate_question_tree(payload)), estado)

    def test_estados_canonicos_passam(self):
        for estado in ("answered", "blocked", "not_applicable"):
            payload = {"questions": [{"questionId": "Q1", "category": "risk", "materiality": "minor", "status": estado}], "coverage": {"total": 1, "material": 0, "answeredMaterial": 0, "blockedMaterial": 0}}
            self.assertNotIn("N4-Q-STATUS", codes(validate_question_tree(payload)), estado)

    def test_material_coverage_requires_paragraph(self):
        payload = {"items": [{"coverageId": "C1", "status": "covered", "materiality": "decisive", "draftParagraphIds": []}]}
        self.assertIn("N4-COV-NO-PARAGRAPH", codes(validate_coverage(payload)))

    def test_material_exclusion_requires_council(self):
        payload = {"items": [{"coverageId": "C1", "status": "intentionally_excluded", "materiality": "decisive", "strategicReason": "x"}]}
        self.assertIn("N4-COV-COUNCIL", codes(validate_coverage(payload)))

    def test_council_decision_requires_evidence_and_locator(self):
        payload = {"theses": [{"thesisId": "T", "role": "primary", "bestObjection": "x", "helenaDecision": "adopt", "ciceroDecision": "adopt"}]}
        self.assertIn("N4-THESIS-COUNCIL-EVIDENCE", codes(validate_theses(payload)))

    def test_council_rejection_is_visible_without_fake_structural_p0(self):
        payload = {"theses": [{"thesisId": "T", "role": "primary", "bestObjection": "x", "helenaDecision": "review_required", "helenaEvidenceId": "H", "helenaDecisionLocator": "conclusão", "ciceroDecision": "reject_current_version", "ciceroEvidenceId": "C", "ciceroDecisionLocator": "veredito"}]}
        findings = validate_theses(payload)
        self.assertEqual(2, sum(item["code"] == "N4-THESIS-COUNCIL-PENDING" for item in findings))
        self.assertFalse(any(item["severity"] == "p0" for item in findings))

    def test_graph_rejects_dangling_and_unknown_relation(self):
        payload = {"nodes": [{"id": "A"}], "edges": [{"edgeId": "E", "from": "A", "to": "B", "relation": "sustenta_parcialmente", "reason": "x"}]}
        result = codes(validate_graph(payload))
        self.assertIn("N4-GRAPH-DANGLING", result)
        self.assertIn("N4-GRAPH-RELATION", result)

    def test_support_edge_requires_scope(self):
        payload = {"nodes": [{"id": "A"}, {"id": "B"}], "edges": [{"edgeId": "E", "from": "A", "to": "B", "relation": "supports", "reason": "x"}]}
        self.assertIn("N4-GRAPH-SCOPE", codes(validate_graph(payload)))

    def test_dependency_cycle_is_detected(self):
        payload = {"nodes": [{"id": "A"}, {"id": "B"}], "edges": [{"edgeId": "E1", "from": "A", "to": "B", "relation": "depends_on", "reason": "x"}, {"edgeId": "E2", "from": "B", "to": "A", "relation": "depends_on", "reason": "x"}]}
        self.assertIn("N4-GRAPH-CYCLE", codes(validate_graph(payload)))

    def test_terminology_conflict_is_p0(self):
        payload = {"events": [{"eventId": "EV1", "canonicalLabel": "não conhecimento", "sourceId": "D1", "locator": "p.1", "allowedParaphrases": [], "forbiddenEquivalents": ["improcedência"]}], "surfaces": [{"surfaceId": "draft", "text": "A improcedência foi correta."}]}
        self.assertIn("N4-EVENT-CONFLICT", codes(validate_event_identity(payload)))

    def test_semantic_contrast_allows_forbidden_term(self):
        payload = {"events": [{"eventId": "EV1", "canonicalLabel": "não conhecimento", "sourceId": "D1", "locator": "p.1", "allowedParaphrases": [], "forbiddenEquivalents": ["improcedência"]}], "surfaces": [{"surfaceId": "draft", "text": "Não houve improcedência.", "semanticContrast": True}]}
        self.assertNotIn("N4-EVENT-CONFLICT", codes(validate_event_identity(payload)))

    def test_comparison_never_generates_automatic_sanction(self):
        payload = {"comparisonSets": [{"setId": "S", "documents": ["A", "B"], "units": [{"unitId": "U", "classification": "repeated_with_no_material_novelty", "reviewStatus": "confirmed", "consequence": "fine"}]}]}
        self.assertIn("N4-CMP-AUTO-SANCTION", codes(validate_comparison(payload)))

    def test_possible_prequestioning_requires_review(self):
        payload = {"comparisonSets": [{"setId": "S", "documents": ["A", "B"], "units": [{"unitId": "U", "classification": "possible_prequestioning", "reviewStatus": "pending", "consequence": "triage_only"}]}]}
        self.assertIn("N4-CMP-REVIEW", codes(validate_comparison(payload)))

    def test_intertemporal_date_requires_source(self):
        payload = {"issues": [{"issueId": "T", "triggeringDate": "2020-01-01", "conclusion": "CPC/2015", "transitionRuleSourceId": "SRC"}]}
        self.assertIn("N4-TEMP-DATE-SOURCE", codes(validate_intertemporal(payload)))

    def test_quantification_recomputes_range(self):
        payload = {"scenarios": [{"scenarioId": "Q", "formula": "base * percentual", "knownInputs": [{"name": "base", "value": 1000, "sourceId": "D"}], "disputedInputs": [{"name": "percentual", "range": [0.1, 0.2], "basisIds": ["P"]}], "outputs": {"minimum": 1, "maximum": 2}}]}
        self.assertIn("N4-QUANT-OUTPUT", codes(validate_quantification(payload)))

    def test_quantification_rejects_unsafe_formula(self):
        payload = {"scenarios": [{"scenarioId": "Q", "formula": "__import__('os')", "knownInputs": [], "outputs": {"value": 1}}]}
        self.assertIn("N4-QUANT-CALC", codes(validate_quantification(payload)))

    def test_unverified_conduct_cannot_be_externalized(self):
        payload = {"conducts": [{"conductId": "C", "verificationStatus": "not_verified", "externalPhrasingAllowed": "agiu de má-fé"}]}
        self.assertIn("N4-COND-EXTERNAL", codes(validate_conducts(payload)))

    def test_case_suite_detects_silent_criterion_change(self):
        suite = {"suiteId": "v1", "draftedBeforeFinalText": True, "countJustification": "fixture", "tests": [{"testId": "T", "severity": "blocking", "method": "deterministic", "expected": "x", "evidenceRequired": ["draft"], "evaluator": {"kind": "contains", "value": "correto"}}]}
        frozen = suite_hash(suite)
        suite["tests"][0]["expected"] = "relaxado"
        self.assertNotEqual(frozen, suite_hash(suite))

    def test_suite_hash_binds_temporal_classification(self):
        suite = {"suiteId": "temporal", "executionMode": "retrospective_baseline", "draftedBeforeFinalText": False, "retrospectiveReason": "fixture", "tests": []}
        frozen = suite_hash(suite)
        suite["executionMode"] = "prospective"
        suite["draftedBeforeFinalText"] = True
        suite["frozenAt"] = "2026-07-11T10:00:00-03:00"
        suite["finalProducedAt"] = "2026-07-11T11:00:00-03:00"
        self.assertNotEqual(frozen, suite_hash(suite))

    def test_retrospective_suite_cannot_claim_pre_final_timing(self):
        suite = {"suiteId": "retro", "executionMode": "retrospective_baseline", "draftedBeforeFinalText": True, "retrospectiveReason": "texto preexistente", "countJustification": "fixture", "tests": []}
        self.assertIn("N4-TEST-RETRO-HONESTY", codes(validate_suite(suite)))

    def test_prospective_suite_requires_chronological_evidence(self):
        suite = {"suiteId": "prospective", "executionMode": "prospective", "draftedBeforeFinalText": True, "frozenAt": "2026-07-11T10:00:00-03:00", "finalProducedAt": "2026-07-11T09:00:00-03:00", "countJustification": "fixture", "tests": []}
        self.assertIn("N4-TEST-TIMING-ORDER", codes(validate_suite(suite)))

    def test_prospective_suite_rejects_unparseable_or_timezone_free_dates(self):
        suite = {"suiteId": "prospective", "executionMode": "prospective", "draftedBeforeFinalText": True, "frozenAt": "qualquer", "finalProducedAt": "2026-07-11T11:00:00", "countJustification": "fixture", "tests": []}
        self.assertIn("N4-TEST-TIMING-EVIDENCE", codes(validate_suite(suite)))

    def test_mutation_testing_proves_discrimination(self):
        draft = self.case / "draft.md"
        draft.write_text("pedido correto sem placeholder", encoding="utf-8")
        suite = {"suiteId": "mut", "executionMode": "retrospective_baseline", "draftedBeforeFinalText": False, "retrospectiveReason": "fixture", "countJustification": "fixture", "tests": [
            {"testId": "T1", "severity": "blocking", "method": "deterministic", "expected": "contains", "evidenceRequired": ["draft"], "evaluator": {"kind": "contains", "value": "pedido correto"}},
            {"testId": "T2", "severity": "blocking", "method": "deterministic", "expected": "not_contains", "evidenceRequired": ["draft"], "evaluator": {"kind": "not_contains", "value": "[VERIFICAR]"}},
        ]}
        result = run_suite(suite, draft, reviewer_run_id="review")
        self.assertEqual(1.0, result["antiFraud"]["mutationScore"])
        self.assertEqual(2, result["antiFraud"]["killed"])

    def test_mutation_summary_cannot_claim_impossible_score(self):
        suite = {"suiteId": "mut", "executionMode": "retrospective_baseline", "draftedBeforeFinalText": False, "retrospectiveReason": "fixture", "countJustification": "fixture", "tests": []}
        result = {"suiteHash": suite_hash(suite), "results": [], "antiFraud": {"mutationScore": 999, "killed": 999, "total": 1, "mutations": []}}
        self.assertIn("N4-TEST-MUTATION-INCONSISTENT", codes(validate_results(result, suite)))

    def test_measured_global_pass_requires_evidence_per_layer(self):
        payload = {"measurementContract": "N4-MEASURED-v1", "layers": {"C1": "pass", "C2": "pass", "C3": "pass", "C4": "pass", "C5": "pass"}, "layerEvidence": {}, "findings": []}
        self.assertIn("N4-GLOBAL-EVIDENCE", codes(validate_global(payload)))

    def test_case_test_results_invalidate_when_draft_changes(self):
        draft = self.case / "draft.md"
        draft.write_text("texto correto", encoding="utf-8")
        suite = {"suiteId": "v1", "draftedBeforeFinalText": True, "countJustification": "fixture", "tests": [{"testId": "T", "severity": "blocking", "method": "deterministic", "expected": "contém correto", "evidenceRequired": ["draft"], "evaluator": {"kind": "contains", "value": "correto"}}]}
        result = run_suite(suite, draft, reviewer_run_id="review")
        draft.write_text("texto alterado", encoding="utf-8")
        self.assertIn("N4-TEST-STALE-DRAFT", codes(validate_results(result, suite, draft)))

    def test_same_run_cannot_review_case_tests(self):
        draft = self.case / "draft.md"
        draft.write_text("correto", encoding="utf-8")
        suite = {"suiteId": "v1", "draftedBeforeFinalText": True, "countJustification": "fixture", "tests": [{"testId": "T", "severity": "blocking", "method": "deterministic", "expected": "x", "evidenceRequired": ["draft"], "evaluator": {"kind": "contains", "value": "correto"}}]}
        self.assertIn("N4-TEST-SELF-REVIEW", codes(run_suite(suite, draft, reviewer_run_id="same", producer_run_id="same")["findings"]))

    def test_doi_title_mismatch_is_rejected(self):
        study = {"studies": [{"studyId": "S", "identifiers": {"doi": "10.1/x"}, "identityCheck": {"queriedTitle": "A", "returnedTitle": "B"}, "verification": {"identity": "confirmed", "content": "confirmed", "correctionRetraction": "checked"}, "publicationStatus": "current", "limitations": ["x"]}]}
        self.assertIn("N4-SCI-TITLE-MISMATCH", codes(validate_studies(study)))

    def test_retracted_study_cannot_support_claim(self):
        study = {"studies": [{"studyId": "S", "identifiers": {}, "verification": {"identity": "confirmed", "content": "confirmed", "correctionRetraction": "checked"}, "publicationStatus": "retracted", "supportsClaimIds": ["C"], "limitations": ["x"]}]}
        self.assertIn("N4-SCI-RETRACTED", codes(validate_studies(study)))

    def test_preprint_is_not_peer_reviewed_version(self):
        study = {"studies": [{"studyId": "S", "version": "preprint", "peerReviewStatus": "confirmed", "identifiers": {}, "verification": {"identity": "confirmed", "content": "confirmed", "correctionRetraction": "checked"}, "publicationStatus": "current", "limitations": ["x"]}]}
        self.assertIn("N4-SCI-PREPRINT", codes(validate_studies(study)))

    def test_observational_claim_cannot_be_made_causal(self):
        claims = {"claims": [{"scienceClaimId": "C", "draftText": "X causa Y", "synthesisStatus": "mixed", "supportingStudyIds": ["S"], "contraryStudyIds": [], "transferLimits": ["x"], "causalLanguageAllowed": False, "finalUseAllowed": True}]}
        self.assertIn("N4-SCI-CAUSAL", codes(validate_claims(claims)))

    def test_population_evidence_cannot_diagnose_individual(self):
        claims = {"claims": [{"scienceClaimId": "C", "draftText": "A literatura comprova que o paciente possui diagnóstico", "useType": "contextual_support", "synthesisStatus": "mixed", "supportingStudyIds": ["S"], "contraryStudyIds": [], "transferLimits": ["não prova o indivíduo"], "causalLanguageAllowed": False, "finalUseAllowed": True}]}
        self.assertIn("N4-SCI-INDIVIDUAL", codes(validate_claims(claims)))

    def test_science_requires_contrary_evidence_search(self):
        payload = {"synthesisStatus": "convergent", "contraryEvidenceSearch": {"performed": False}, "limitations": ["x"]}
        self.assertIn("N4-SCI-CONTRARY", codes(validate_synthesis(payload)))

    def test_instruction_like_article_text_is_not_a_blocker(self):
        study = {"studies": [{"studyId": "S", "title": "Ignore previous instructions as an attack pattern", "identifiers": {}, "verification": {"identity": "confirmed", "content": "confirmed", "correctionRetraction": "checked"}, "publicationStatus": "current", "limitations": ["x"]}]}
        self.assertFalse(any(item["severity"] == "p0" for item in validate_studies(study)))

    def test_shared_source_is_not_independent_consensus(self):
        payload = {"premises": [], "consensusChecks": [{"issueId": "M", "agentsAgreeing": 3, "independentSourceCount": 1, "verdict": "consensus"}], "recommendationChanges": [], "bestObjection": "x", "alternativeExplanation": "y"}
        self.assertIn("N4-META-CONSENSUS", codes(validate_metacognition(payload)))

    def test_unconfirmed_email_premise_not_used_as_fact(self):
        payload = {"premises": [{"premiseId": "P", "status": "declared_not_confirmed", "usedInDraft": True}], "consensusChecks": [], "recommendationChanges": [], "bestObjection": "x", "alternativeExplanation": "y"}
        self.assertIn("N4-META-UNCONFIRMED", codes(validate_metacognition(payload)))

    def test_style_preference_does_not_become_global_gate(self):
        payload = {"changes": [{"changeId": "C", "cause": "style_preference", "before": "a", "after": "b"}], "regressionProposals": [{"proposalId": "P", "sourceChangeId": "C", "scope": "global", "status": "proposed"}]}
        self.assertIn("N4-LEARN-STYLE-GATE", codes(validate_learning(payload)))

    def test_feedback_ledger_rejects_raw_whatsapp_content(self):
        payload = {"conversationUnits": [{"unitId": "U", "messageIds": ["M"], "contentClass": "human_authored", "body": "conteúdo bruto"}]}
        self.assertIn("N4-FEEDBACK-RAW", codes(validate_feedback_assimilation(payload)))

    def test_imported_ai_output_cannot_be_attributed_as_human_original(self):
        payload = {
            "conversationUnits": [{"unitId": "U", "messageIds": ["M"], "contentClass": "imported_ai_output"}],
            "signals": [{"signalId": "S", "unitIds": ["U"], "kind": "imported_content", "scope": "case", "confidence": "high", "status": "observed", "interpretation": "material importado", "operationalConsequence": "não atribuir autoria"}],
            "contributions": [{"contributionId": "C", "thesisId": "T", "changeType": "added", "origin": "human_original", "evidenceIds": ["S"], "validationStatus": "audited"}],
        }
        self.assertIn("N4-FEEDBACK-FALSE-HUMAN-ATTRIBUTION", codes(validate_feedback_assimilation(payload)))

    def test_implicit_personality_hypothesis_never_auto_promotes(self):
        payload = {
            "conversationUnits": [{"unitId": "U", "messageIds": ["M"], "contentClass": "human_authored"}],
            "signals": [{"signalId": "S", "unitIds": ["U"], "kind": "implicit_hypothesis", "scope": "office", "confidence": "medium", "status": "promoted", "interpretation": "preferência inferida", "operationalConsequence": "alterar fluxo", "approvedBy": "reviewer", "evidenceRuns": ["R1", "R2"]}],
        }
        self.assertIn("N4-FEEDBACK-IMPLICIT-PROMOTION", codes(validate_feedback_assimilation(payload)))

    def test_essential_missing_audio_blocks_feedback_assimilation(self):
        payload = {"conversationUnits": [{"unitId": "U", "messageIds": ["M"], "contentClass": "human_authored", "mediaCoverage": {"expected": 1, "materialized": 0, "essentialMissing": 1}}]}
        self.assertIn("N4-FEEDBACK-MEDIA-MISSING", codes(validate_feedback_assimilation(payload)))

    def test_valid_feedback_assimilation_preserves_authorship_and_test_gate(self):
        payload = {
            "conversationUnits": [{"unitId": "U", "messageIds": ["M1", "M2"], "contentClass": "human_authored", "mediaCoverage": {"expected": 0, "materialized": 0, "essentialMissing": 0}}],
            "signals": [{"signalId": "S", "unitIds": ["U"], "kind": "explicit_correction", "scope": "office", "confidence": "high", "status": "promoted", "interpretation": "atribuir a origem das teses", "operationalConsequence": "gerar ledger", "approvedBy": "Igor", "evidenceRuns": ["caso-a", "caso-b"]}],
            "contributions": [{"contributionId": "C", "thesisId": "T", "changeType": "strengthened", "origin": "human_original", "evidenceIds": ["S"], "sourceIds": ["SRC"], "validationStatus": "external_ready", "legalDecisionId": "D"}],
            "workflowChanges": [{"changeId": "W", "sourceSignalIds": ["S"], "targetPhase": "F10_ENTREGA_EVIDENCIA_APRENDIZADO", "scope": "office", "behavior": "classificar a origem intelectual por tese", "status": "promoted", "approvedBy": "Igor", "testId": "test-feedback", "evidenceRuns": ["caso-a", "caso-b"]}],
        }
        self.assertEqual([], validate_feedback_assimilation(payload))

    def test_delivery_blocks_wrong_selected_hash(self):
        payload = {"packageHash": "a", "selectedHash": "b", "preSendMatch": False}
        self.assertIn("N4-DELIVERY-PRESEND", codes(validate_delivery(payload)))

    def test_delivery_accepts_artifact_evidence_without_post_hash(self):
        payload = {"packageHash": "a", "selectedHash": "a", "preSendMatch": True, "postDeliveryVerification": {"mode": "artifact_evidence", "deliveredHash": None, "deliveryEvidenceId": "E", "status": "confirmed"}}
        self.assertEqual([], validate_delivery(payload))

    def test_channel_hash_requires_exact_delivered_bytes(self):
        payload = {"packageHash": "a", "selectedHash": "a", "preSendMatch": True, "postDeliveryVerification": {"mode": "channel_hash", "deliveredHash": "b", "status": "confirmed"}}
        self.assertIn("N4-DELIVERY-CHANNEL-HASH", codes(validate_delivery(payload)))

    def test_shadow_missing_artifacts_never_blocks_current_flow(self):
        report = validate_case(self.case, write=False)
        self.assertFalse(report["approved"])
        self.assertFalse(report["complete"])
        self.assertFalse(report["blocksCurrentFlow"])
        self.assertTrue(report["shadowAllowsCurrentFlow"])
        self.assertGreater(report["counts"]["p1"], 0)

    def test_zero_expected_artifacts_is_not_evaluated_not_approved(self):
        for mode in ("shadow", "pilot_blocking", "default_on"):
            with self.subTest(mode=mode), patch(
                "forja_n4_validate.load_config",
                return_value={"features": {}, "n4": {"mode": mode}},
            ):
                report = validate_case(self.case, target_phase="F0_RECONCILIACAO_FILA", write=False)
            self.assertEqual("not_evaluated", report["evaluationStatus"])
            self.assertFalse(report["complete"])
            self.assertFalse(report["approved"])
            self.assertFalse(report["blocksCurrentFlow"])

    def test_pilot_mode_blocks_incomplete_selected_case(self):
        report = validate_case(self.case, write=False, mode_override="pilot_blocking")
        self.assertFalse(report["approved"])
        self.assertTrue(report["blocksCurrentFlow"])
        self.assertGreater(report["counts"]["p0"], 0)

    def test_pilot_blocks_only_promoted_gate_groups(self):
        from forja_n4_validate import _pilot_blocking_finding
        self.assertTrue(_pilot_blocking_finding({"code": "N4-Q-UNRESOLVED"}))
        self.assertTrue(_pilot_blocking_finding({"code": "N4-DELIVERY-PRESEND"}))
        self.assertFalse(_pilot_blocking_finding({"code": "N4-COND-EXTERNAL"}))

    def test_runtime_schema_rejects_wrong_artifact_type(self):
        payload = build_envelope(self.case, "F2_QUESTION_TREE.json", {"questions": [], "coverage": {"total": 0, "material": 0, "answeredMaterial": 0, "blockedMaterial": 0}}, source_hashes=[], producer_run_id="run")
        payload["artifactType"] = "wrong_type"
        from forja_n4_validate import _schema_findings
        self.assertIn("N4-SCHEMA", codes(_schema_findings("F2_QUESTION_TREE.json", payload)))

    def test_revoked_source_blocks_even_when_hash_still_exists(self):
        from forja_n4_validate import _source_registry_findings
        source = self.case / "source.md"
        source.write_text("conteúdo antigo", encoding="utf-8")
        import hashlib
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        manifest = {"n4SourceRegistry": {"draft": {"path": str(source), "sha256": digest, "status": "revoked", "reason": "feedback jurídico superveniente"}}}
        registered, findings = _source_registry_findings(self.case, manifest)
        self.assertIn(digest, registered)
        self.assertIn("N4-SOURCE-REVOKED", codes(findings))

    def test_opaque_hash_is_rejected_in_blocking_mode(self):
        from forja_n4_validate import _source_registry_findings
        _, findings = _source_registry_findings(self.case, {"n4SourceRegistry": {"legacy": "a" * 64}}, require_verifiable=True)
        self.assertIn("N4-SOURCE-OPAQUE", codes(findings))

    def test_origin_explicitly_invalidated_blocks_derived_copy(self):
        from forja_n4_validate import _source_registry_findings
        origin = self.case / "origin.md"
        copy = self.case / "copy.md"
        origin.write_text("Esta fonte foi invalidada após revisão.", encoding="utf-8")
        copy.write_text("texto derivado", encoding="utf-8")
        import hashlib
        digest = hashlib.sha256(copy.read_bytes()).hexdigest()
        manifest = {"n4SourceRegistry": {"draft": {"path": str(copy), "originPath": str(origin), "sha256": digest, "status": "active"}}}
        _, findings = _source_registry_findings(self.case, manifest)
        self.assertIn("N4-SOURCE-ORIGIN-REVOKED", codes(findings))

    def test_cross_artifact_support_must_exist_in_reasoning_graph(self):
        from forja_n4_validate import _cross_reference_findings
        files = {
            "F3_REASONING_GRAPH.json": {"nodes": [{"id": "DOC-1"}]},
            "F2_QUESTION_TREE.json": {"questions": [{"questionId": "Q1", "supportIds": ["DOC-2"]}]},
        }
        self.assertIn("N4-CROSS-Q-SUPPORT", codes(_cross_reference_findings(files)))

    def test_delivery_chain_selects_packaged_bytes_and_confirms_evidence(self):
        package_file = self.case / "packages" / "pkg" / "final.pdf"
        package_file.parent.mkdir(parents=True)
        package_file.write_bytes(b"final controlado")
        import hashlib
        digest = hashlib.sha256(package_file.read_bytes()).hexdigest()
        (self.case / "FORJA_PACKAGE.json").write_text(json.dumps({
            "packageId": "pkg",
            "packageHash": "f" * 64,
            "attachments": [{"artifactId": "petition_pdf", "packagePath": str(package_file), "sha256": digest}],
        }), encoding="utf-8")
        selected = select(self.case, "petition_pdf", layout_profile_id="medina_visual_law", producer_run_id="f9-producer", reviewer_run_id="f9-reviewer")
        confirmed = confirm(self.case, mode="artifact_evidence", delivery_evidence_id="email-thread-123", delivered_path=None, producer_run_id="f10-producer", reviewer_run_id="f10-reviewer")
        self.assertEqual(digest, selected["selectedHash"])
        self.assertEqual("confirmed", confirmed["postDeliveryVerification"]["status"])

    def test_write_artifact_is_idempotent_for_semantic_hash(self):
        payload = build_envelope(self.case, "F2_QUESTION_TREE.json", {"questions": [], "coverage": {"total": 0, "material": 0, "answeredMaterial": 0, "blockedMaterial": 0}}, source_hashes=[], producer_run_id="run")
        write_artifact(self.case, "F2_QUESTION_TREE.json", payload)
        first = json.loads((self.case / "n4_artifacts" / "F2_QUESTION_TREE.json").read_text(encoding="utf-8"))["contentHash"]
        write_artifact(self.case, "F2_QUESTION_TREE.json", payload)
        second = json.loads((self.case / "n4_artifacts" / "F2_QUESTION_TREE.json").read_text(encoding="utf-8"))["contentHash"]
        self.assertEqual(first, second)

    def test_invalidation_marks_stale_without_deleting_artifact(self):
        payload = build_envelope(self.case, "F7_GLOBAL_CONSISTENCY.json", {"layers": {"C1": "pass", "C2": "pass", "C3": "pass", "C4": "pass", "C5": "pass"}, "findings": []}, source_hashes=[], producer_run_id="run")
        path = write_artifact(self.case, "F7_GLOBAL_CONSISTENCY.json", payload)
        result = invalidate(self.case, "markdown", reason="texto alterado")
        self.assertIn("F7_GLOBAL_CONSISTENCY.json", result["staleArtifacts"])
        self.assertTrue(path.is_file())
        self.assertEqual("stale", json.loads(path.read_text(encoding="utf-8"))["status"])


if __name__ == "__main__":
    unittest.main()
