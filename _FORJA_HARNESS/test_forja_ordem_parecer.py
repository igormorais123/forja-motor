# -*- coding: utf-8 -*-
"""Regressão da ordem parecer -> redação (M2.1 do plano 19, ordem do Igor 09/07).

DEVE_PEGAR: parecer criado depois do início do F6 em caso novo reprova.
NÃO_PODE_TRAVAR: caso legado (F6 antes de 12/07/2026), caso sem F6 e parecer
anterior ao F6 aprovam. Roda com: python test_forja_ordem_parecer.py
"""
import os
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path

from forja_delivery import parecer_antes_da_redacao, CORTE_ORDEM_PARECER


def _state(f6_at=None):
    hist = []
    if f6_at:
        hist.append({"phase": "F6_REDACAO_TEMPLATE", "at": f6_at, "status": "ok"})
    return {"phaseHistory": hist}


def _tocar(path: Path, quando: datetime):
    path.write_text("parecer de teste com conteúdo", encoding="utf-8")
    ts = quando.timestamp()
    os.utime(path, (ts, ts))


class DevePegar(unittest.TestCase):

    def test_parecer_depois_do_f6_reprova_caso_novo(self):
        # F6 iniciado logo após o corte (passado real); o parecer é criado AGORA,
        # portanto depois do F6 — deve reprovar. (Não dá para retroagir st_ctime,
        # então o cenário usa F6 no passado em vez de parecer no futuro.)
        f6 = CORTE_ORDEM_PARECER + timedelta(hours=1)
        with tempfile.TemporaryDirectory() as tmp:
            parecer = Path(tmp) / "F4_PARECER_HELENA.md"
            parecer.write_text("parecer de teste com conteúdo", encoding="utf-8")
            ok, motivo = parecer_antes_da_redacao(parecer, _state(f6.isoformat()))
        self.assertFalse(ok)
        self.assertIn("PARECER_POS_REDACAO", motivo)

    def test_parecer_inexistente_com_f6_iniciado_reprova(self):
        f6 = (CORTE_ORDEM_PARECER + timedelta(days=1)).isoformat()
        ok, motivo = parecer_antes_da_redacao(None, _state(f6))
        self.assertFalse(ok)
        self.assertIn("inexistente", motivo)


class NaoPodeTravar(unittest.TestCase):

    def test_caso_legado_nao_retroage(self):
        f6 = (CORTE_ORDEM_PARECER - timedelta(days=3)).isoformat()
        with tempfile.TemporaryDirectory() as tmp:
            parecer = Path(tmp) / "F4_PARECER_CICERO.md"
            _tocar(parecer, datetime.now().astimezone())
            ok, motivo = parecer_antes_da_redacao(parecer, _state(f6))
        self.assertTrue(ok)
        self.assertIn("legado", motivo)

    def test_sem_f6_no_historico_aprova(self):
        ok, motivo = parecer_antes_da_redacao(None, _state())
        self.assertTrue(ok)

    def test_parecer_antes_do_f6_aprova(self):
        agora = datetime.now().astimezone()
        f6 = agora + timedelta(days=2)  # redação começa depois do parecer
        with tempfile.TemporaryDirectory() as tmp:
            parecer = Path(tmp) / "F4_PARECER_HELENA.md"
            _tocar(parecer, agora - timedelta(hours=1))
            ok, motivo = parecer_antes_da_redacao(parecer, _state(f6.isoformat()))
        self.assertTrue(ok, motivo)

    def test_timestamp_invalido_no_historico_nao_explode(self):
        ok, _ = parecer_antes_da_redacao(None, {"phaseHistory": [
            {"phase": "F6_REDACAO_TEMPLATE", "at": "data-invalida"}]})
        self.assertTrue(ok)


if __name__ == "__main__":
    unittest.main(verbosity=2)
