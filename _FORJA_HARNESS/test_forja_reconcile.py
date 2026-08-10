from __future__ import annotations

import tempfile
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

import forja_reconcile
from forja_n3_common import atomic_write_json, read_json
from validate_forja_n3 import SCRIPT_TESTS


class ForjaReconcileGateHistoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.state_root = Path(self.temp.name) / "state"
        self.demanda = {"id": "d1"}
        self.integracoes = {"gmail": "offline"}
        self.evidence = {"status": "none", "detail": "sem evidência"}

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _gravar(self, findings):
        with patch.object(forja_reconcile, "STATE_DIR", self.state_root):
            case_id = forja_reconcile.gravar_state(
                self.demanda,
                findings,
                "pending",
                self.evidence,
                self.integracoes,
            )
        return read_json(self.state_root / case_id / "FORJA_STATE.json")

    def test_gate_que_deixa_de_ser_atual_e_resolvido_sem_sumir(self) -> None:
        case_dir = self.state_root / "case-d1"
        case_dir.mkdir(parents=True)
        atomic_write_json(case_dir / "FORJA_STATE.json", {
            "caseId": "case-d1",
            "createdAt": "2026-07-15T10:00:00-03:00",
            "phaseHistory": [],
            "gates": [
                {
                    "code": "COMANDO_AUSENTE",
                    "severity": "P0",
                    "detail": "Nenhum COMANDO_*.md na pasta do caso.",
                    "at": "2026-07-15T10:01:00-03:00",
                },
                {
                    "code": "SEM_PRAZO_TRIAGEM",
                    "severity": "P2",
                    "detail": "Aberta sem prazo estruturado; triagem pendente.",
                    "at": "2026-07-15T10:02:00-03:00",
                },
            ],
        })

        state = self._gravar([
            forja_reconcile.finding(
                "SEM_PRAZO_TRIAGEM",
                "P2",
                "Aberta sem prazo estruturado; triagem pendente.",
            )
        ])

        self.assertEqual(["SEM_PRAZO_TRIAGEM"], [gate["code"] for gate in state["gates"]])
        self.assertEqual("active", state["gates"][0]["status"])
        self.assertEqual("2026-07-15T10:02:00-03:00", state["gates"][0]["at"])
        self.assertEqual(1, len(state["gateHistory"]))
        resolvido = state["gateHistory"][0]
        self.assertEqual("COMANDO_AUSENTE", resolvido["code"])
        self.assertEqual("resolved", resolvido["status"])
        self.assertEqual("forja_reconcile:F0", resolvido["resolvedBy"])
        self.assertTrue(resolvido["resolvedAt"])
        self.assertEqual(
            "finding_not_observed_in_current_reconciliation",
            resolvido["resolution"],
        )

        repetido = self._gravar([
            forja_reconcile.finding(
                "SEM_PRAZO_TRIAGEM",
                "P2",
                "Aberta sem prazo estruturado; triagem pendente.",
            )
        ])
        self.assertEqual(1, len(repetido["gateHistory"]))

    def test_runner_referencia_o_script_f7_no_destino_atual(self) -> None:
        caminho = "_scripts_oneoff/validate_f7_integration.py"
        self.assertIn(caminho, SCRIPT_TESTS)
        raiz = Path(__file__).resolve().parent
        self.assertTrue((raiz / caminho).is_file())
        processo = subprocess.run(
            [sys.executable, caminho],
            cwd=raiz,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=30,
            check=False,
        )
        self.assertEqual(0, processo.returncode, processo.stdout + processo.stderr)


class ReconciliacaoNaoPuxaOCasoParaTras(unittest.TestCase):
    """Os dois defeitos medidos em 09/08/2026, presos como regressão.

    A varredura de F0 reescrevia `currentPhase` para a primeira fase e empilhava
    um carimbo em toda passagem. Um caso que entregou 94 arquivos se descrevia
    como "em reconciliação", com vinte e três entradas idênticas no histórico e
    o relógio sempre em zero. Nenhum leitor do estado tinha como distinguir isso
    de uma fábrica parada.
    """

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.state_root = Path(self.temp.name) / "state"
        self.demanda = {"id": "d1"}

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _gravar(self, status="pending"):
        with patch.object(forja_reconcile, "STATE_DIR", self.state_root):
            case_id = forja_reconcile.gravar_state(
                self.demanda, [], status,
                {"status": "none", "detail": "sem evidência"}, {"gmail": "offline"})
        return read_json(self.state_root / case_id / "FORJA_STATE.json")

    def _semear(self, **campos):
        case_dir = self.state_root / "case-d1"
        case_dir.mkdir(parents=True, exist_ok=True)
        atomic_write_json(case_dir / "FORJA_STATE.json",
                          {"caseId": "case-d1", "phaseHistory": [], **campos})

    def test_fase_adiantada_sobrevive_a_varredura(self) -> None:
        self._semear(currentPhase="F7_AUDITORIA_JURIDICA_FACTUAL")

        self.assertEqual("F7_AUDITORIA_JURIDICA_FACTUAL", self._gravar()["currentPhase"])

    def test_caso_novo_nasce_na_fase_da_reconciliacao(self) -> None:
        self.assertEqual("F0_RECONCILIACAO_FILA", self._gravar()["currentPhase"])

    def test_fase_desconhecida_nao_derruba_a_gravacao(self) -> None:
        self._semear(currentPhase="F42_INVENTADA")

        self.assertEqual("F0_RECONCILIACAO_FILA", self._gravar()["currentPhase"])

    def test_passagem_sem_mudanca_nao_carimba_de_novo(self) -> None:
        primeiro = self._gravar()
        segundo = self._gravar()
        terceiro = self._gravar()

        self.assertEqual(1, len(terceiro["phaseHistory"]))
        self.assertEqual(primeiro["updatedAt"], segundo["updatedAt"])
        self.assertEqual(primeiro["updatedAt"], terceiro["updatedAt"])

    def test_mudanca_de_situacao_carimba(self) -> None:
        self._gravar("pending")

        depois = self._gravar("blocked")

        self.assertEqual(["pending", "blocked"],
                         [e["status"] for e in depois["phaseHistory"]])


class OResumoNaoPodeComerAProva(unittest.TestCase):
    """O que se confere contra a fonte não pode caber no que sobrou do corte.

    Em 10/08/2026 um caso da casa aparecia no censo como "cumprido sem prova".
    O painel registrava dois identificadores de mensagem — e os dois estavam
    depois do caractere 140, onde a evidência era cortada antes de ser gravada
    no estado. O censo lia o corte, não o registro, e acusava de falta de prova
    um trabalho que tinha prova. Resumo é comodidade de leitura; localizador é
    a única parte que se confere.
    """

    LONGO = ("Triagem sanitizada concluida em 13/07/2026. O audio recente foi "
             "classificado e respondido com orientacao segura por e-mail Gmail "
             "19a0b1c2d3e4f506; a pendencia foi escalada ao titular por e-mail "
             "Gmail 19a0b1c2d3e4f507, sem assumir custo ou compromisso.")

    def test_identificador_alem_do_corte_sobrevive(self) -> None:
        resumo = forja_reconcile._resumo_com_localizadores(self.LONGO)

        self.assertIn("19a0b1c2d3e4f507", resumo)

    def test_o_que_ja_estava_no_corte_nao_se_repete(self) -> None:
        resumo = forja_reconcile._resumo_com_localizadores(self.LONGO)

        self.assertEqual(1, resumo.count("19a0b1c2d3e4f506"))

    def test_texto_curto_sai_intacto_e_sem_apendice(self) -> None:
        self.assertEqual("respondido por telefone",
                         forja_reconcile._resumo_com_localizadores("respondido por telefone"))

    def test_localizador_do_whatsapp_tambem_sobrevive(self) -> None:
        texto = "x" * 150 + " entregue pelo WhatsApp 3EB0F1F1F1F1F1F1F1F1F1 por link"

        self.assertIn("3EB0F1F1F1F1F1F1F1F1F1",
                      forja_reconcile._resumo_com_localizadores(texto))

    def test_a_evidencia_gravada_carrega_o_localizador(self) -> None:
        """O caminho real: da demanda ao campo que o censo lê."""
        _status, descricao = forja_reconcile.evidencia_de_entrega(
            {"evidenciaResposta": self.LONGO}, {}, None)

        self.assertIn("19a0b1c2d3e4f507", descricao)


if __name__ == "__main__":
    unittest.main(verbosity=2)
