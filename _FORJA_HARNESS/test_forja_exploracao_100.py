from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import forja_reconcile
from forja_exploracao_100 import (
    FACTUAL_CATEGORIES,
    LENSES,
    PROTOCOL_VERSION,
    build_scaffold,
    validate_exploration_100,
)
from forja_phase_contracts import load_contract
from forja_n3_common import ForjaN3Error
from forja_n4_common import build_envelope, expected_content_hash, validate_envelope
from forja_n4_validate import _schema_findings
from forja_run import _validate_result


def codes(findings: list[dict]) -> set[str]:
    return {item["code"] for item in findings}


def valid_payload() -> dict:
    payload = build_scaffold("case-email-teste", "Processo 0000000-00.2026.8.00.0000")
    payload["problemDefinition"] = (
        "A situação documental ainda precisa ser convertida em uma intervenção processual "
        "útil, cabível e compatível com o resultado prático solicitado."
    )
    payload["diagnosticSynthesis"] = (
        "As dez óticas foram examinadas separando comando, fatos, prova, processo, direito, "
        "objeções, riscos, alternativas, execução e comunicação; as respostas abaixo formam "
        "o mapa de entrada obrigatório das fases de fontes, estratégia, pesquisa, redação e auditoria."
    )
    for question in payload["questions"]:
        question["caseAnchor"] = f"Âncora específica do caso para {question['questionId']} e seu ponto decisório"
        question["status"] = "answered"
        question["answer"] = "Resposta específica e suficientemente desenvolvida para o caso sintético de validação."
        question["epistemicStatus"] = (
            "confirmed_document" if question["category"] in FACTUAL_CATEGORIES else "legal_inference"
        )
        question["supportIds"] = ["SRC-001"] if question["category"] in FACTUAL_CATEGORIES else []
        question.pop("unansweredConsequence", None)
        question["downstreamTargets"] = ["F3", "F4"]
    payload["coverage"].update({"answeredMaterial": 100, "blockedMaterial": 0})
    payload["solutionHypotheses"] = [
        {"hypothesisId": "H01", "description": "Usar o veículo principal após fechar as fontes.", "conditions": ["cabimento confirmado"], "risks": ["cognição limitada"], "questionIds": ["Q031", "Q041"], "downstreamTargets": ["F4"]},
        {"hypothesisId": "H02", "description": "Preservar solução subsidiária de menor alcance.", "conditions": ["tese principal rejeitada"], "risks": ["resultado parcial"], "questionIds": ["Q074", "Q075"], "downstreamTargets": ["F4"]},
    ]
    payload["downstreamHandoff"] = {
        "F3": ["Q011", "Q021", "Q031"],
        "F4": ["Q051", "Q061", "Q071"],
        "F5": ["Q041", "Q042", "Q050"],
        "F6": ["Q076", "Q091", "Q092"],
        "F7": ["Q066", "Q097", "Q100"],
    }
    payload["draftRelease"] = "ready_for_drafting"
    return payload


class Exploracao100Tests(unittest.TestCase):
    def test_scaffold_has_exactly_ten_lenses_and_one_hundred_questions(self):
        payload = build_scaffold("case-x", "Âncora real do caso com tamanho suficiente")
        self.assertEqual(PROTOCOL_VERSION, payload["protocolVersion"])
        self.assertEqual("question_tree", payload["artifactType"])
        self.assertEqual("draft", payload["status"])
        self.assertTrue(payload["contentHash"])
        self.assertEqual(100, len(payload["questions"]))
        self.assertEqual({lens: 10 for lens in LENSES}, payload["coverage"]["perLens"])
        self.assertIn("N4-Q-100-PLACEHOLDER", codes(validate_exploration_100(payload)))

    def test_complete_exploration_passes(self):
        findings = validate_exploration_100(valid_payload())
        self.assertFalse(
            [item for item in findings if item.get("severity") == "p0"],
            findings,
        )
        self.assertEqual(
            {"N4-Q-100-DIVERSITY", "N4-Q-100-NO-GAP"},
            codes(findings),
        )
        self.assertTrue(all(item.get("severity") == "p1" for item in findings))

    def test_ninety_nine_questions_fail(self):
        payload = valid_payload()
        payload["questions"].pop()
        payload["coverage"]["total"] = 99
        payload["coverage"]["material"] = 99
        payload["coverage"]["answeredMaterial"] = 99
        payload["coverage"]["perLens"]["comunicacao_visual_validacao"] = 9
        self.assertIn("N4-Q-100-COUNT", codes(validate_exploration_100(payload)))

    def test_repeated_question_fails(self):
        payload = valid_payload()
        payload["questions"][1]["text"] = payload["questions"][0]["text"]
        self.assertIn("N4-Q-100-DUPLICATE", codes(validate_exploration_100(payload)))

    def test_answered_fact_without_support_fails(self):
        payload = valid_payload()
        fact = next(item for item in payload["questions"] if item["category"] in FACTUAL_CATEGORIES)
        fact["supportIds"] = []
        self.assertIn("N4-Q-NO-SUPPORT", codes(validate_exploration_100(payload)))

    def test_blocked_material_question_blocks_drafting(self):
        payload = valid_payload()
        question = payload["questions"][0]
        question.update({
            "status": "blocked",
            "answer": "Não respondida porque o documento primário ainda não foi disponibilizado.",
            "epistemicStatus": "not_verified",
            "unansweredConsequence": "Bloqueia o uso externo da premissa.",
        })
        payload["coverage"].update({"answeredMaterial": 99, "blockedMaterial": 1})
        payload["draftRelease"] = "ready_for_drafting"
        self.assertIn("N4-Q-100-RELEASE", codes(validate_exploration_100(payload)))

    def test_missing_downstream_handoff_fails(self):
        payload = valid_payload()
        payload["downstreamHandoff"]["F7"] = []
        self.assertIn("N4-Q-100-HANDOFF", codes(validate_exploration_100(payload)))

    def test_contract_makes_exploration_output_and_downstream_input_mandatory(self):
        f2 = load_contract("F2_CLASSIFICACAO_PRODUTO_RISCO")
        f3 = load_contract("F3_FONTES_REGIMENTO_LEIS")
        f4 = load_contract("F4_BLUEPRINT_ESTRATEGICO")
        self.assertIn("question_tree", f2["requiredOutputs"])
        self.assertIn("exploration_100_complete", f2["requiredGates"])
        self.assertIn("question_tree", f3["requiredInputs"])
        self.assertIn("question_tree", f4["requiredInputs"])

    def test_phase_promotion_rejects_invalid_question_tree(self):
        contract = load_contract("F2_CLASSIFICACAO_PRODUTO_RISCO")
        with tempfile.TemporaryDirectory() as temp:
            attempt = Path(temp)
            artifacts = []
            for output_id in contract["requiredOutputs"]:
                path = attempt / f"{output_id}.json"
                payload = valid_payload() if output_id == "question_tree" else {"ok": True}
                if output_id == "question_tree":
                    payload["questions"].pop()
                path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
                artifacts.append({"id": output_id, "path": path.name})
            (attempt / "PHASE_RESULT.json").write_text(json.dumps({
                "status": "pass",
                "producer": "producer-1",
                "reviewer": "reviewer-2",
                "producerRole": contract["producerRole"],
                "reviewerRole": contract["reviewerRole"],
                "gates": {gate: "pass" for gate in contract["requiredGates"]},
                "artifacts": artifacts,
            }), encoding="utf-8")
            with self.assertRaisesRegex(ForjaN3Error, "exploração F2-A reprovada"):
                _validate_result(attempt, contract)

    def test_schema_keeps_legacy_question_trees_readable(self):
        with tempfile.TemporaryDirectory() as temp:
            case = Path(temp) / "case-legacy"
            case.mkdir()
            legacy = build_envelope(
                case,
                "F2_QUESTION_TREE.json",
                {"questions": [], "coverage": {"total": 0, "material": 0, "answeredMaterial": 0, "blockedMaterial": 0}},
                source_hashes=[],
                producer_run_id="legacy-run",
            )
            self.assertFalse(any(item["code"] == "N4-SCHEMA" for item in _schema_findings("F2_QUESTION_TREE.json", legacy)))

    def test_complete_tree_can_form_valid_n4_artifact(self):
        payload = valid_payload()
        payload.update({"status": "approved", "producerRunId": "producer-1", "reviewerRunId": "reviewer-2", "sourceHashes": ["a" * 64]})
        payload["contentHash"] = expected_content_hash(payload)
        with tempfile.TemporaryDirectory() as temp:
            case = Path(temp) / payload["caseId"]
            case.mkdir()
            self.assertEqual([], validate_envelope(case, "F2_QUESTION_TREE.json", payload))
            self.assertFalse(any(item["code"] == "N4-SCHEMA" for item in _schema_findings("F2_QUESTION_TREE.json", payload)))

    def test_reconciliation_registers_pending_then_materialized_exploration(self):
        with tempfile.TemporaryDirectory() as temp, patch.object(forja_reconcile, "STATE_DIR", Path(temp)):
            demand = {"id": "email-novo-caso", "pasta": "Caso"}
            forja_reconcile.gravar_state(demand, [], "pending", {"status": "none"}, {})
            state_path = Path(temp) / "case-email-novo-caso" / "FORJA_STATE.json"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            self.assertEqual("pending", state["initialExploration"]["status"])
            artifact = state_path.parent / "n4_artifacts" / "F2_QUESTION_TREE.json"
            artifact.parent.mkdir()
            artifact.write_text("{}", encoding="utf-8")
            forja_reconcile.gravar_state(demand, [], "pending", {"status": "none"}, {})
            state = json.loads(state_path.read_text(encoding="utf-8"))
            self.assertEqual("materialized", state["initialExploration"]["status"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
