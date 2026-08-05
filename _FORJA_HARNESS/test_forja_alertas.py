# -*- coding: utf-8 -*-
"""Regressão dos alertas P0 (M1.1 do plano 19).

Padrão DEVE_PEGAR / NÃO_PODE_TRAVAR. Roda com: python test_forja_alertas.py
Os testes redirecionam MANUAL_JSON e LOG_GLOBAL para pastas temporárias —
nunca tocam o painel real.
"""
import json
import os
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path

import forja_alertas as fa


class Base(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        tmp = Path(self._tmp.name)
        self.case_dir = tmp / "case-teste"
        self.case_dir.mkdir()
        (self.case_dir / "FORJA_STATE.json").write_text(
            json.dumps({"demandId": "email-teste-1"}), encoding="utf-8")
        self._manual_orig = fa.MANUAL_JSON
        self._log_orig = fa.LOG_GLOBAL
        fa.MANUAL_JSON = tmp / "painel" / "intervencoes_manuais.json"
        fa.MANUAL_JSON.parent.mkdir()
        fa.LOG_GLOBAL = tmp / "reports" / "ALERTAS_P0.jsonl"

    def tearDown(self):
        fa.MANUAL_JSON = self._manual_orig
        fa.LOG_GLOBAL = self._log_orig
        self._tmp.cleanup()

    def _comentarios(self):
        dados = json.loads(fa.MANUAL_JSON.read_text(encoding="utf-8"))
        return dados["items"]["email-teste-1"]["comentarios"]


class DevePegar(Base):

    def test_p0_novo_notifica_painel(self):
        r = fa.notificar_p0(self.case_dir, "G7-datas", "prazo com sábado", origem="teste")
        self.assertEqual(r["status"], "notificado")
        coments = self._comentarios()
        self.assertEqual(len(coments), 1)
        self.assertIn("G7-datas", coments[0]["texto"])
        self.assertEqual(coments[0]["tipo"], "forja-p0")
        self.assertEqual(coments[0]["autor"], "FORJA")
        self.assertTrue(fa.LOG_GLOBAL.is_file())

    def test_p0_repetido_em_6h_deduplica(self):
        fa.notificar_p0(self.case_dir, "G7-datas", "motivo")
        r2 = fa.notificar_p0(self.case_dir, "G7-datas", "motivo de novo")
        self.assertEqual(r2["status"], "deduplicado")
        self.assertEqual(len(self._comentarios()), 1)

    def test_p0_apos_janela_notifica_de_novo(self):
        fa.notificar_p0(self.case_dir, "G7-datas", "motivo")
        reg = fa._registro_enviados(self.case_dir)
        dados = json.loads(reg.read_text(encoding="utf-8"))
        antigo = (datetime.now().astimezone() - timedelta(hours=7)).isoformat()
        dados["p0:G7-datas"] = antigo
        reg.write_text(json.dumps(dados), encoding="utf-8")
        r = fa.notificar_p0(self.case_dir, "G7-datas", "voltou")
        self.assertEqual(r["status"], "notificado")
        self.assertEqual(len(self._comentarios()), 2)

    def test_gates_distintos_nao_deduplicam_entre_si(self):
        fa.notificar_p0(self.case_dir, "G7-datas", "a")
        r = fa.notificar_p0(self.case_dir, "G4-sumula", "b")
        self.assertEqual(r["status"], "notificado")
        self.assertEqual(len(self._comentarios()), 2)

    def test_resolucao_notifica_uma_vez(self):
        r1 = fa.notificar_resolucao(self.case_dir, "G7-datas")
        r2 = fa.notificar_resolucao(self.case_dir, "G7-datas")
        self.assertEqual(r1["status"], "notificado")
        self.assertEqual(r2["status"], "deduplicado")


class NaoPodeTravar(Base):

    def test_painel_indisponivel_cai_no_fallback_sem_excecao(self):
        fa.MANUAL_JSON = Path(self._tmp.name) / "nao-existe" / "x.json"
        r = fa.notificar_p0(self.case_dir, "G1-personas", "persona no produto")
        self.assertEqual(r["status"], "pendente")
        pend = fa._pendentes(self.case_dir)
        self.assertTrue(pend.is_file())
        ev = json.loads(pend.read_text(encoding="utf-8").splitlines()[0])
        self.assertEqual(ev["gate"], "G1-personas")

    def test_drenagem_reentrega_quando_painel_volta(self):
        painel_bom = fa.MANUAL_JSON
        fa.MANUAL_JSON = Path(self._tmp.name) / "nao-existe" / "x.json"
        fa.notificar_p0(self.case_dir, "G1-personas", "motivo")
        fa.MANUAL_JSON = painel_bom
        r = fa.drenar_pendentes(self.case_dir)
        self.assertEqual(r["reentregues"], 1)
        self.assertEqual(r["restantes"], 0)
        self.assertFalse(fa._pendentes(self.case_dir).is_file())
        self.assertEqual(len(self._comentarios()), 1)

    def test_caso_sem_state_nao_explode(self):
        vazio = Path(self._tmp.name) / "case-vazio"
        vazio.mkdir()
        r = fa.notificar_p0(vazio, "G7", "motivo")
        # sem demandId o alerta fica pendente, mas nunca levanta exceção
        self.assertIn(r["status"], ("pendente", "notificado"))

    def test_registro_de_dedup_corrompido_nao_trava(self):
        fa._registro_enviados(self.case_dir).write_text("{corrompido", encoding="utf-8")
        r = fa.notificar_p0(self.case_dir, "G7", "motivo")
        self.assertEqual(r["status"], "notificado")


if __name__ == "__main__":
    unittest.main(verbosity=2)
