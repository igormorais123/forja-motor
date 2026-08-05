# -*- coding: utf-8 -*-
"""Regressão do passe editorial final e da barreira anti-autocertificação."""

import json
import tempfile
import unittest
from pathlib import Path

from forja_editorial_fidelity import PROTOCOL_VERSION, validate_editorial_bundle
import forja_editorial_model as editorial_model
from forja_editorial import FINAL_MARKER, PROMPT, REPORT_MARKER, run_editorial_pass
from forja_n3_common import ForjaN3Error, atomic_write_json, resolve_name, sha256_file
from forja_phase_contracts import load_contract


SOURCE = """# CONTRARRAZÕES

1. O documento do evento 42 foi apresentado em 12/03/2026. O art. 10 da Lei 12.016/2009 disciplina a matéria.

2. O acórdão registrou \"prova suficiente\" e manteve a decisão.

## PEDIDOS

Requer-se o não provimento do AgInt no AREsp nº 2.698.443.

Nestes termos, pede deferimento.
"""

FINAL = """# CONTRARRAZÕES

1. Em 12/03/2026, foi apresentado o documento do evento 42. A matéria é disciplinada pelo art. 10 da Lei 12.016/2009.

2. Ao registrar \"prova suficiente\", o acórdão manteve a decisão.

## PEDIDOS

Requer-se o não provimento do AgInt no AREsp nº 2.698.443.

Nestes termos, pede deferimento.
"""


def gosto_receipt() -> dict:
    return {
        "protocolo": "FORJA-GOSTO-EDGE-v1",
        "versaoObviaRejeitada": "mera recapitulação cronológica",
        "direcoesConsideradas": [
            {"direcao": "prova antes da regra", "decisao": "selecionada", "razao": "antecipa o fato decisivo"},
            {"direcao": "regra antes da prova", "decisao": "rejeitada", "razao": "abre de forma genérica"},
            {"direcao": "pedido antes da prova", "decisao": "rejeitada", "razao": "reduz a compreensão"},
        ],
        "direcaoSelecionada": "prova antes da regra",
        "ancorasDoTexto": [
            "documento do evento 42",
            "prova suficiente",
        ],
        "consequenciaSemDramatizacao": "o acórdão manteve a decisão",
    }


def fable_payload(source_hash: str, *, taste: bool = True) -> dict:
    payload = {"sourceHash": source_hash, "mudancas": [], "duvidas": []}
    if taste:
        payload["gostoJuridico"] = gosto_receipt()
    return payload


def write_bundle(root: Path, final_text: str = FINAL) -> tuple[Path, Path, Path]:
    source = root / "audited_markdown.md"
    final = root / "final_markdown.md"
    report = root / "editorial_report.json"
    source.write_text(SOURCE, encoding="utf-8")
    final.write_text(final_text, encoding="utf-8")
    atomic_write_json(report, {
        "protocolVersion": PROTOCOL_VERSION,
        "model": "claude-opus-5",
        "producerModel": {"canonicalId": "claude-opus-5", "family": "claude", "sessionId": "s-editor"},
        "reviewerModel": {"canonicalId": "gpt-5.6-sol", "family": "openai", "sessionId": "s-revisor"},
        "familyAssurance": editorial_model.CROSS_FAMILY,
        "billing": "assinatura OAuth Claude Max (sem API key)",
        "sourceSha256": sha256_file(source),
        "finalSha256": sha256_file(final),
        "fableReport": {"sourceHash": sha256_file(source), "duvidas": []},
    })
    return source, final, report


class EditorialFidelityTests(unittest.TestCase):
    def test_rewrite_preserving_invariants_passes(self):
        with tempfile.TemporaryDirectory() as temp:
            source, final, report = write_bundle(Path(temp))
            result = validate_editorial_bundle(source, final, report)
            self.assertTrue(result["approved"], result["findings"])
            self.assertTrue(all(value == "pass" for value in result["gates"].values()))

    def test_changed_number_is_blocked_even_if_model_claims_success(self):
        with tempfile.TemporaryDirectory() as temp:
            changed = FINAL.replace("12/03/2026", "13/03/2026")
            source, final, report = write_bundle(Path(temp), changed)
            result = validate_editorial_bundle(source, final, report)
            self.assertFalse(result["approved"])
            self.assertTrue(any(item["gate"] == "numbers_preserved" for item in result["findings"]))

    def test_changed_orders_are_blocked(self):
        with tempfile.TemporaryDirectory() as temp:
            changed = FINAL.replace("não provimento", "provimento parcial")
            source, final, report = write_bundle(Path(temp), changed)
            result = validate_editorial_bundle(source, final, report)
            self.assertFalse(result["approved"])
            self.assertTrue(any(item["gate"] == "pedidos_preserved" for item in result["findings"]))

    def test_wrong_model_or_billing_is_blocked(self):
        with tempfile.TemporaryDirectory() as temp:
            source, final, report = write_bundle(Path(temp))
            payload = json.loads(report.read_text(encoding="utf-8"))
            payload["model"] = "claude-opus"  # fora da allowlist
            atomic_write_json(report, payload)
            result = validate_editorial_bundle(source, final, report)
            self.assertFalse(result["approved"])
            self.assertEqual("blocked", result["gates"]["editor_model_confirmed"])

    def test_removed_argumentative_chapter_is_blocked(self):
        with tempfile.TemporaryDirectory() as temp:
            changed = FINAL.replace(
                "# CONTRARRAZÕES\n\n1.",
                "# CONTRARRAZÕES\n\n## RAZÕES DECISIVAS\n\nA coerência do sistema exige a manutenção do julgado.\n\n1.",
            )
            source, final, report = write_bundle(Path(temp), changed)
            # Inverte os papéis para simular supressão do capítulo no texto final.
            source.write_text(changed, encoding="utf-8")
            final.write_text(FINAL, encoding="utf-8")
            payload = json.loads(report.read_text(encoding="utf-8"))
            payload["sourceSha256"] = sha256_file(source)
            payload["finalSha256"] = sha256_file(final)
            payload["fableReport"]["sourceHash"] = sha256_file(source)
            atomic_write_json(report, payload)
            result = validate_editorial_bundle(source, final, report)
            self.assertFalse(result["approved"])
            self.assertTrue(any(item["gate"] == "headings_preserved" for item in result["findings"]))


class FableRunnerTests(unittest.TestCase):
    def test_prompt_exige_selecao_edge_e_recibo_de_gosto(self):
        self.assertIn("FORJA-GOSTO-EDGE-v1", PROMPT)
        self.assertIn("três direções editoriais", PROMPT)
        self.assertIn('"gostoJuridico"', PROMPT)
        self.assertIn('"ancorasDoTexto"', PROMPT)

    def test_mocked_claude_code_writes_hash_bound_artifacts(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "audited_markdown.md"
            gate = root / "f7_gate_result.json"
            source.write_text(SOURCE, encoding="utf-8")
            atomic_write_json(gate, {"p0": 0})
            source_hash = sha256_file(source)
            response = (
                FINAL_MARKER + "\n" + FINAL + "\n" + REPORT_MARKER + "\n" +
                json.dumps(fable_payload(source_hash), ensure_ascii=False)
            )

            def invoke(_prompt):
                return {
                    "result": response,
                    "session_id": "session-fable-test",
                    "usage": {"input_tokens": 100, "output_tokens": 50},
                    "modelUsage": {"claude-opus-5": {"inputTokens": 100}},
                    "_forjaAuth": {
                        "authMethod": "claude.ai", "apiProvider": "firstParty",
                        "subscriptionType": "max",
                    },
                }

            result = run_editorial_pass(
                source, root, gate_path=gate, case_id="case-test", invoke=invoke,
                reviewer_model="gpt-5.6-sol", reviewer_session="s-revisor",
            )
            self.assertEqual("pass", result["status"])
            self.assertTrue((root / "final_markdown.md").is_file())
            self.assertTrue((root / "editorial_diff.patch").is_file())
            self.assertTrue((root / "EDITORIAL_RESULT.json").is_file())
            report = json.loads((root / "editorial_report.json").read_text(encoding="utf-8"))
            self.assertEqual("claude-opus-5", report["model"])
            self.assertEqual(source_hash, report["sourceSha256"])
            usage = json.loads((root / "editor_usage.json").read_text(encoding="utf-8"))
            self.assertEqual("max", usage["subscriptionType"])

    def test_fable_does_not_run_while_f7_has_p0(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "audited_markdown.md"
            gate = root / "f7_gate_result.json"
            source.write_text(SOURCE, encoding="utf-8")
            atomic_write_json(gate, {"p0": 1})
            with self.assertRaises(ForjaN3Error):
                run_editorial_pass(
                    source, root, gate_path=gate, case_id="case-test",
                    invoke=lambda _prompt: self.fail("Claude não deveria ser chamado"),
                )

    def test_fidelity_failure_retries_from_original_inside_same_attempt(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "audited_markdown.md"
            gate = root / "f7_gate_result.json"
            source.write_text(SOURCE, encoding="utf-8")
            atomic_write_json(gate, {"p0": 0})
            source_hash = sha256_file(source)
            calls = []

            def invoke(prompt):
                calls.append(prompt)
                text = FINAL.replace("documento", '"documento"', 1) if len(calls) == 1 else FINAL
                response = (
                    FINAL_MARKER + "\n" + text + "\n" + REPORT_MARKER + "\n" +
                    json.dumps(fable_payload(source_hash))
                )
                return {
                    "result": response,
                    "session_id": f"session-{len(calls)}",
                    "usage": {},
                    "modelUsage": {"claude-opus-5": {}},
                    "_forjaAuth": {
                        "authMethod": "claude.ai", "apiProvider": "firstParty",
                        "subscriptionType": "max",
                    },
                }

            result = run_editorial_pass(
                source, root, gate_path=gate, case_id="case-test", invoke=invoke,
                reviewer_model="gpt-5.6-sol", reviewer_session="s-revisor",
            )
            self.assertEqual("pass", result["status"])
            self.assertEqual(2, len(calls))
            self.assertIn("tentativa anterior foi descartada", calls[1].casefold())
            report = json.loads((root / "editorial_report.json").read_text(encoding="utf-8"))
            self.assertEqual(2, report["rewriteAttempt"])

    def test_recibo_de_gosto_incompleto_e_descartado(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "audited_markdown.md"
            gate = root / "f7_gate_result.json"
            source.write_text(SOURCE, encoding="utf-8")
            atomic_write_json(gate, {"p0": 0})
            source_hash = sha256_file(source)
            calls = []

            def invoke(prompt):
                calls.append(prompt)
                report = fable_payload(source_hash, taste=len(calls) > 1)
                response = (
                    FINAL_MARKER + "\n" + FINAL + "\n" + REPORT_MARKER + "\n"
                    + json.dumps(report, ensure_ascii=False)
                )
                return {
                    "result": response,
                    "session_id": f"session-taste-{len(calls)}",
                    "usage": {},
                    "modelUsage": {"claude-opus-5": {}},
                    "_forjaAuth": {
                        "authMethod": "claude.ai",
                        "apiProvider": "firstParty",
                        "subscriptionType": "max",
                    },
                }

            result = run_editorial_pass(
                source, root, gate_path=gate, case_id="case-test", invoke=invoke,
                reviewer_model="gpt-5.6-sol", reviewer_session="s-revisor",
            )
            self.assertEqual("pass", result["status"])
            self.assertEqual(2, len(calls))
            self.assertIn("taste_receipt_valid", calls[1])

    def test_modelo_fora_da_allowlist_nao_executa(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "audited_markdown.md"
            gate = root / "f7_gate_result.json"
            source.write_text(SOURCE, encoding="utf-8")
            atomic_write_json(gate, {"p0": 0})
            with self.assertRaises(ForjaN3Error) as erro:
                run_editorial_pass(
                    source, root, gate_path=gate, case_id="case-test",
                    editor_model="modelo-inventado",
                    invoke=lambda _prompt: self.fail("nenhum modelo deveria ser chamado"),
                )
            self.assertIn("allowlist", str(erro.exception))

    def test_modelo_reconhecido_sem_executor_local_e_recusado(self):
        """A FORJA reconhece o GPT como revisor, mas não sabe invocá-lo daqui."""
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "audited_markdown.md"
            gate = root / "f7_gate_result.json"
            source.write_text(SOURCE, encoding="utf-8")
            atomic_write_json(gate, {"p0": 0})
            with self.assertRaises(ForjaN3Error) as erro:
                run_editorial_pass(
                    source, root, gate_path=gate, case_id="case-test",
                    editor_model="gpt-5.6-sol",
                    invoke=lambda _prompt: self.fail("não há executor próprio"),
                )
            self.assertIn("executor", str(erro.exception))

    def test_envelope_de_outro_modelo_derruba_a_tentativa(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "audited_markdown.md"
            gate = root / "f7_gate_result.json"
            source.write_text(SOURCE, encoding="utf-8")
            atomic_write_json(gate, {"p0": 0})
            source_hash = sha256_file(source)
            response = (
                FINAL_MARKER + "\n" + FINAL + "\n" + REPORT_MARKER + "\n" +
                json.dumps(fable_payload(source_hash), ensure_ascii=False)
            )

            def invoke(_prompt):
                # O contrato pede Opus 5; quem consumiu tokens foi outro modelo.
                return {
                    "result": response, "session_id": "s1", "usage": {},
                    "modelUsage": {"claude-fable-5": {}},
                    "_forjaAuth": {"authMethod": "claude.ai", "apiProvider": "firstParty",
                                   "subscriptionType": "max"},
                }

            with self.assertRaises(ForjaN3Error) as erro:
                run_editorial_pass(
                    source, root, gate_path=gate, case_id="case-test", invoke=invoke,
                    editor_model="claude-opus-5",
                )
            self.assertIn("claude-opus-5", str(erro.exception))


class RevisaoCruzadaTests(unittest.TestCase):
    def test_revisor_de_outra_familia_e_cross_family(self):
        self.assertEqual(
            editorial_model.CROSS_FAMILY,
            editorial_model.family_assurance("claude-opus-5", "gpt-5.6-sol"),
        )

    def test_mesma_familia_em_sessoes_distintas_degrada_sem_silencio(self):
        self.assertEqual(
            editorial_model.SAME_FAMILY,
            editorial_model.family_assurance(
                "claude-opus-5", "claude-fable-5",
                producer_session="s1", reviewer_session="s2",
            ),
        )

    def test_mesma_sessao_ou_revisor_ausente_fica_unverified(self):
        self.assertEqual(
            editorial_model.UNVERIFIED,
            editorial_model.family_assurance("claude-opus-5", None),
        )
        self.assertEqual(
            editorial_model.UNVERIFIED,
            editorial_model.family_assurance(
                "claude-opus-5", "claude-fable-5",
                producer_session="s1", reviewer_session="s1",
            ),
        )

    def test_bundle_sem_revisor_identificado_e_bloqueado(self):
        with tempfile.TemporaryDirectory() as temp:
            source, final, report = write_bundle(Path(temp))
            payload = json.loads(report.read_text(encoding="utf-8"))
            payload.pop("reviewerModel")
            payload["familyAssurance"] = editorial_model.UNVERIFIED
            atomic_write_json(report, payload)
            result = validate_editorial_bundle(source, final, report)
            self.assertFalse(result["approved"])
            self.assertEqual("blocked", result["gates"]["cross_model_review_verified"])

    def test_garantia_declarada_a_maior_e_recomposta_e_bloqueada(self):
        """Declarar cross_family sem segunda família não compra a liberação."""
        with tempfile.TemporaryDirectory() as temp:
            source, final, report = write_bundle(Path(temp))
            payload = json.loads(report.read_text(encoding="utf-8"))
            payload["reviewerModel"] = {
                "canonicalId": "claude-fable-5", "family": "claude", "sessionId": "s-revisor",
            }
            atomic_write_json(report, payload)  # continua declarando cross_family
            result = validate_editorial_bundle(source, final, report)
            self.assertFalse(result["approved"])
            self.assertTrue(any(
                item["gate"] == "cross_model_review_verified" for item in result["findings"]
            ))

    def test_modo_estrito_recusa_degradacao_para_mesma_familia(self):
        with tempfile.TemporaryDirectory() as temp:
            source, final, report = write_bundle(Path(temp))
            payload = json.loads(report.read_text(encoding="utf-8"))
            payload["reviewerModel"] = {
                "canonicalId": "claude-fable-5", "family": "claude", "sessionId": "s-revisor",
            }
            payload["familyAssurance"] = editorial_model.SAME_FAMILY
            atomic_write_json(report, payload)
            self.assertTrue(validate_editorial_bundle(source, final, report)["approved"])
            estrito = validate_editorial_bundle(source, final, report, strict_family=True)
            self.assertFalse(estrito["approved"])

    def test_contrato_f7_exige_os_gates_do_modelo_editorial(self):
        f7 = load_contract("F7_AUDITORIA_JURIDICA_FACTUAL")
        self.assertIn("editor_model_confirmed", f7["requiredGates"])
        self.assertIn("cross_model_review_verified", f7["requiredGates"])
        self.assertIn("editor_usage", f7["requiredOutputs"])
        self.assertNotIn("fable5_oauth_confirmed", f7["requiredGates"])

    def test_nome_legado_de_artefato_continua_legivel(self):
        self.assertEqual("fable5_usage", resolve_name("editor_usage", {"fable5_usage": {}}))
        self.assertEqual("editor_usage", resolve_name("editor_usage", {"editor_usage": {}}))
        self.assertIsNone(resolve_name("editor_usage", {}))


class ContractTests(unittest.TestCase):
    def test_contract_embeds_f7b_without_new_canonical_phase(self):
        f7 = load_contract("F7_AUDITORIA_JURIDICA_FACTUAL")
        f8 = load_contract("F8_QA_VISUAL")
        self.assertIn("final_markdown", f7["requiredOutputs"])
        self.assertIn("editorial_fidelity_pass", f7["requiredGates"])
        self.assertEqual("F8_QA_VISUAL", f7["nextPhase"])
        self.assertEqual("final_markdown", f8["requiredInputs"][0])


if __name__ == "__main__":
    unittest.main(verbosity=2)
