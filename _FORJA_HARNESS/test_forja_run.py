# -*- coding: utf-8 -*-
"""Regressão do executor de fases N3 (M4.1 do plano 19).

O forja_run.py rodava em sombra sem suíte dedicada. DEVE_PEGAR: fase inválida,
entradas faltantes, resultado reprovado, autorrevisão, gates ausentes, excesso
de tentativas. NÃO_PODE_TRAVAR: fluxo feliz F0, replay idempotente, bloqueio
formal. Roda com: python test_forja_run.py
"""
import json
import tempfile
import unittest
from pathlib import Path

from forja_n3_common import ForjaN3Error
from forja_run import (
    prepare_attempt,
    promote_attempt,
    block_phase,
    load_contract,
    _compute_lastro_gates,
    _recompute_regimento,
    _validate_result,
)
from forja_state_machine import initialize_case, derive_state

F0 = "F0_RECONCILIACAO_FILA"


def _novo_caso(tmp: Path):
    """Caso sintético completo: pasta do caso + comando + estado legado N2."""
    pasta_caso = tmp / "PASTA_DO_CASO"
    pasta_caso.mkdir()
    (pasta_caso / "COMANDO_MANUAL.md").write_text("# comando de teste\n", encoding="utf-8")
    case_dir = tmp / "case-teste-run"
    case_dir.mkdir()
    legado = {
        "caseId": case_dir.name, "specVersion": "N2.0",
        "currentPhase": F0, "status": "pending",
        "inputs": {"demandId": "email-teste-run", "caseFolder": str(pasta_caso),
                   "commandFile": "COMANDO_MANUAL.md"},
        "phaseHistory": [],
    }
    (case_dir / "FORJA_STATE.json").write_text(json.dumps(legado), encoding="utf-8")
    state = initialize_case(case_dir, from_legacy=True)
    return case_dir, state


def _conteudo_do_artefato(out_id: str, attempt_dir: Path) -> dict:
    """Conteúdo mínimo que satisfaz os gates computados de cada artefato.

    Desde as levas de 04/08/2026 o `{"conteudo": "real"}` genérico não basta:
    o `case_manifest` é conferido contra o disco, porque é dele que o recomputo
    de lastro tira a pasta do cliente. Um manifesto que não mapeia para lugar
    nenhum é exatamente o defeito que o gate existe para pegar — inclusive num
    caso de teste.
    """
    if out_id == "case_manifest":
        raiz = attempt_dir.parents[3]  # <case_dir>/runs/<run>/<fase>/<attempt>
        pasta = raiz.parent / "PASTA_DO_CASO"
        return {"artefato": out_id, "caseId": raiz.name, "demandId": "email-teste-run",
                "caseFolder": str(pasta), "commandFile": str(pasta / "COMANDO_MANUAL.md")}
    return {"artefato": out_id, "conteudo": "real"}


def _resultado_valido(attempt_dir: Path, contrato: dict) -> None:
    artifacts = []
    for out_id in contrato["requiredOutputs"]:
        arq = attempt_dir / f"{out_id}.json"
        arq.write_text(json.dumps(_conteudo_do_artefato(out_id, attempt_dir)),
                       encoding="utf-8")
        artifacts.append({"id": out_id, "path": arq.name})
    resultado = {
        "status": "pass",
        "producer": "run-produtor-1", "reviewer": "run-revisor-2",
        "producerRole": contrato["producerRole"],
        "reviewerRole": contrato["reviewerRole"],
        "gates": {g: "pass" for g in contrato["requiredGates"]},
        "artifacts": artifacts,
    }
    (attempt_dir / "PHASE_RESULT.json").write_text(
        json.dumps(resultado), encoding="utf-8")


class DevePegar(unittest.TestCase):

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_fase_inexistente_falha_claro(self):
        with self.assertRaises(Exception):
            load_contract("F99_FASE_INVENTADA")

    def test_entrada_obrigatoria_faltante(self):
        case_dir, state = _novo_caso(self.tmp)
        # remove o comando do disco: F0 exige commandFile
        (Path(json.loads((case_dir / "FORJA_STATE.json").read_text())["inputs"]["caseFolder"])
         / "COMANDO_MANUAL.md").unlink()
        with self.assertRaises(ForjaN3Error) as ctx:
            prepare_attempt(case_dir, F0, expected_revision=state["revision"])
        self.assertIn("entradas obrigatórias", str(ctx.exception))

    def test_resultado_reprovado_nao_promove(self):
        case_dir, state = _novo_caso(self.tmp)
        prep = prepare_attempt(case_dir, F0, expected_revision=state["revision"])
        attempt = Path(prep["attemptDir"])
        (attempt / "PHASE_RESULT.json").write_text(
            json.dumps({"status": "fail"}), encoding="utf-8")
        with self.assertRaises(ForjaN3Error) as ctx:
            promote_attempt(case_dir, attempt,
                            expected_revision=prep["state"]["revision"])
        self.assertIn("não aprovada", str(ctx.exception))

    def test_autorrevisao_reprovada(self):
        case_dir, state = _novo_caso(self.tmp)
        prep = prepare_attempt(case_dir, F0, expected_revision=state["revision"])
        attempt = Path(prep["attemptDir"])
        contrato = load_contract(F0)
        _resultado_valido(attempt, contrato)
        res = json.loads((attempt / "PHASE_RESULT.json").read_text())
        res["reviewer"] = res["producer"]
        (attempt / "PHASE_RESULT.json").write_text(json.dumps(res), encoding="utf-8")
        with self.assertRaises(ForjaN3Error) as ctx:
            promote_attempt(case_dir, attempt,
                            expected_revision=prep["state"]["revision"])
        self.assertIn("mesma execução", str(ctx.exception))

    def test_gate_faltando_reprova(self):
        case_dir, state = _novo_caso(self.tmp)
        prep = prepare_attempt(case_dir, F0, expected_revision=state["revision"])
        attempt = Path(prep["attemptDir"])
        contrato = load_contract(F0)
        _resultado_valido(attempt, contrato)
        res = json.loads((attempt / "PHASE_RESULT.json").read_text())
        res["gates"].popitem()
        (attempt / "PHASE_RESULT.json").write_text(json.dumps(res), encoding="utf-8")
        with self.assertRaises(ForjaN3Error) as ctx:
            promote_attempt(case_dir, attempt,
                            expected_revision=prep["state"]["revision"])
        self.assertIn("gates", str(ctx.exception))

    def test_excesso_de_tentativas(self):
        case_dir, state = _novo_caso(self.tmp)
        max_attempts = int(load_contract(F0)["retryPolicy"]["maxAttempts"])
        rev = state["revision"]
        for _ in range(max_attempts):
            prep = prepare_attempt(case_dir, F0, expected_revision=rev)
            rev = prep["state"]["revision"]
        with self.assertRaises(ForjaN3Error) as ctx:
            prepare_attempt(case_dir, F0, expected_revision=rev)
        self.assertIn("tentativas", str(ctx.exception))


class NaoPodeTravar(unittest.TestCase):

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_fluxo_feliz_f0_promove_e_avanca(self):
        case_dir, state = _novo_caso(self.tmp)
        prep = prepare_attempt(case_dir, F0, expected_revision=state["revision"])
        attempt = Path(prep["attemptDir"])
        _resultado_valido(attempt, load_contract(F0))
        retorno = promote_attempt(case_dir, attempt,
                                  expected_revision=prep["state"]["revision"])
        novo = retorno["state"]
        self.assertIn(F0, novo.get("completedPhases") or [])
        for out_id in load_contract(F0)["requiredOutputs"]:
            self.assertIn(out_id, novo.get("artifacts") or {})

    def test_replay_idempotente(self):
        case_dir, state = _novo_caso(self.tmp)
        prep = prepare_attempt(case_dir, F0, expected_revision=state["revision"])
        attempt = Path(prep["attemptDir"])
        _resultado_valido(attempt, load_contract(F0))
        promote_attempt(case_dir, attempt, expected_revision=prep["state"]["revision"])
        a, b = derive_state(case_dir), derive_state(case_dir)
        self.assertEqual(a["stateHash"], b["stateHash"])
        self.assertEqual(a["revision"], b["revision"])

    def test_bloqueio_formal(self):
        case_dir, state = _novo_caso(self.tmp)
        novo = block_phase(case_dir, F0, expected_revision=state["revision"],
                           reason="anexo externo pendente",
                           blockers=["ANEXOS_EXTERNOS_PENDENTES"])
        self.assertEqual(novo.get("lifecycleStatus"), "blocked")
        self.assertTrue(novo.get("blockers"))

    def test_recomputo_prefere_ledger_canonico_ao_snapshot_hash(self):
        pasta = self.tmp / "F3_FONTES_REGIMENTO_LEIS"
        pasta.mkdir()
        declarado = pasta / "fact_ledger-f00067d94084.json"
        canonico = pasta / "fact_ledger.json"
        declarado.write_text(json.dumps({"facts": []}), encoding="utf-8")
        canonico.write_text(json.dumps({"facts": [], "releasePolicy": "internal_review_only"}), encoding="utf-8")
        produto = self.tmp / "final_markdown.md"
        produto.write_text("Texto sem material econômico.", encoding="utf-8")
        laudo = _compute_lastro_gates(
            "F7_AUDITORIA_JURIDICA_FACTUAL",
            [{"artifactId": "fact_ledger", "source": declarado},
             {"artifactId": "final_markdown", "source": produto}],
            {},
        )
        self.assertTrue(laudo["applicable"])
        self.assertEqual(Path(laudo["ledger"]), canonico)
        self.assertEqual(Path(laudo["ledgerDeclared"]), declarado)

    def test_recomputo_ledger_invalido_nao_finge_na(self):
        pasta = self.tmp / "F3_FONTES_REGIMENTO_LEIS"
        pasta.mkdir()
        ledger = pasta / "fact_ledger.json"
        ledger.write_text("{ JSON quebrado", encoding="utf-8")
        produto = self.tmp / "final_markdown.md"
        produto.write_text("Texto econômico: R$ 100.000,00.", encoding="utf-8")
        laudo = _compute_lastro_gates(
            "F7_AUDITORIA_JURIDICA_FACTUAL",
            [{"artifactId": "fact_ledger", "source": ledger},
             {"artifactId": "final_markdown", "source": produto}],
            {},
        )
        self.assertTrue(laudo["applicable"])
        self.assertEqual(laudo["computed"]["status"], "fail")
        self.assertTrue(any(item["gate"] == "L0-recomputo-sem-insumo"
                            and item["sev"] == "P0"
                            for item in laudo["findings"]))

    def test_recomputo_regimento_alcanca_fontes_markdown(self):
        tentativa = self.tmp / "attempt-f3-markdown"
        tentativa.mkdir()
        mapa = tentativa / "sources_map.md"
        mapa.write_text(
            "# Mapa de fontes\n\n"
            "Regimento Interno do TRF4, consolidação oficial até o Assento "
            "Regimental nº 37/2026.\n",
            encoding="utf-8",
        )
        ledger = tentativa / "fact_ledger.md"
        ledger.write_text(
            "# Ledger de fatos\n\n"
            "| ID | Proposição | Estatuto | Fonte/localizador | Limite |\n"
            "|---|---|---|---|---|\n"
            "| FACT-1 | fato confirmado | confirmado | decisão, p. 1 | limite declarado |\n",
            encoding="utf-8",
        )
        auditoria = tentativa / "adversarial_audit.json"
        auditoria.write_text(
            json.dumps({"applicable": False, "reason": "sem peça adversária"}),
            encoding="utf-8",
        )
        resultado = {}
        _recompute_regimento(
            load_contract("F3_FONTES_REGIMENTO_LEIS"),
            [
                {"artifactId": "sources_map", "source": mapa},
                {"artifactId": "fact_ledger", "source": ledger},
                {"artifactId": "adversarial_audit", "source": auditoria},
            ],
            tentativa,
            resultado,
        )
        gates = resultado["computedRegimentoGates"]
        self.assertEqual("warn", gates["tribunal_identified"])
        self.assertEqual("warn", gates["regimento_available"])
        self.assertEqual("pass", gates["critical_facts_sourced"])

    def test_gate_obrigatorio_warn_nao_promove_apos_recomputacao(self):
        tentativa = self.tmp / "attempt-f3-warning"
        tentativa.mkdir()
        contrato = load_contract("F3_FONTES_REGIMENTO_LEIS")
        arquivos = {
            "fact_ledger": ("fact_ledger.md",
                             "# Ledger de fatos\n\n"
                             "| ID | Proposição | Estatuto | Fonte/localizador | Limite |\n"
                             "|---|---|---|---|---|\n"
                             "| FACT-1 | fato confirmado | confirmado | decisão, p. 1 | limite declarado |\n"),
            "chronology": ("chronology.md", "# Cronologia\n"),
            "contradictions": ("contradictions.json", "{}"),
            "sources_map": ("sources_map.md",
                             "# Mapa de fontes\n\n"
                             "Regimento Interno do TRF4, consolidação oficial até o Assento "
                             "Regimental nº 37/2026.\n"),
            "adversarial_audit": ("adversarial_audit.json",
                                   json.dumps({"applicable": False,
                                               "reason": "sem peça adversária"})),
        }
        artifacts = []
        for artifact_id in contrato["requiredOutputs"]:
            nome, conteudo = arquivos[artifact_id]
            (tentativa / nome).write_text(conteudo, encoding="utf-8")
            artifacts.append({"id": artifact_id, "path": nome})
        (tentativa / "PHASE_RESULT.json").write_text(
            json.dumps({
                "status": "pass",
                "producer": "run-produtor-1", "reviewer": "run-revisor-2",
                "producerRole": contrato["producerRole"],
                "reviewerRole": contrato["reviewerRole"],
                "gates": {gate: "pass" for gate in contrato["requiredGates"]},
                "artifacts": artifacts,
            }), encoding="utf-8")
        (tentativa / "RUN_CONTEXT.json").write_text(
            json.dumps({"phase": contrato["phase"], "inputs": {}}), encoding="utf-8")
        with self.assertRaisesRegex(ForjaN3Error, "após recomputação"):
            _validate_result(tentativa, contrato)


if __name__ == "__main__":
    unittest.main(verbosity=2)
