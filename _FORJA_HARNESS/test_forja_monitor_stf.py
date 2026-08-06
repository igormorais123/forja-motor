# -*- coding: utf-8 -*-
"""Canário do monitor do STF: ele sabe acusar movimento novo?

Um vigia que nunca foi visto acusando é indistinguível de um vigia cego. Aqui o
retrato salvo é adulterado de propósito — retira-se o movimento mais recente — e
exige-se que a leitura seguinte o reporte como novidade. Sem rede: a consulta é
substituída por um dublê.
"""
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import forja_monitor_stf as mon

MOVIMENTOS = [
    "27/07/2026 · Intimado eletronicamente · PROCURADOR-GERAL DA REPÚBLICA",
    "20/07/2026 · Petição · PROCURADOR-GERAL DA REPÚBLICA - Petição: 92561",
    "16/07/2026 · Provido · Decisão monocrática · MIN. GILMAR MENDES",
]

CFG = {"incidente": "0", "rotulo": "processo de teste", "porque": "canário"}


class CanarioDoMonitor(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.patch = mock.patch.object(mon, "DESTINO", Path(self.tmp.name))
        self.patch.start()
        self.addCleanup(self.patch.stop)
        self.addCleanup(self.tmp.cleanup)

    def _consulta(self, movs):
        return mock.patch.object(mon, "consultar", return_value=(movs, "sha-" + str(len(movs))))

    def test_primeira_leitura_vira_baseline_sem_alarme_falso(self):
        with self._consulta(MOVIMENTOS):
            r = mon.verificar("teste", CFG)
        self.assertTrue(r["primeiraLeitura"])
        self.assertFalse(r["houveNovidade"])
        self.assertEqual(r["totalMovimentos"], 3)

    def test_sem_mudanca_nao_inventa_novidade(self):
        with self._consulta(MOVIMENTOS):
            mon.verificar("teste", CFG)
            r = mon.verificar("teste", CFG)
        self.assertFalse(r["houveNovidade"])
        self.assertEqual(r["novidades"], [])

    def test_movimento_novo_e_acusado(self):
        """O caso que importa: o Relator decide e o vigia precisa gritar."""
        with self._consulta(MOVIMENTOS[1:]):      # retrato antigo, sem o de 27/07
            mon.verificar("teste", CFG)
        with self._consulta(MOVIMENTOS):          # portal agora traz o movimento novo
            r = mon.verificar("teste", CFG)
        self.assertTrue(r["houveNovidade"])
        self.assertEqual(r["novidades"], [MOVIMENTOS[0]])

    def test_novidade_fica_registrada_no_log(self):
        with self._consulta(MOVIMENTOS[1:]):
            mon.verificar("teste", CFG)
        with self._consulta(MOVIMENTOS):
            mon.verificar("teste", CFG)
        log = Path(self.tmp.name) / "teste_novidades.log"
        self.assertTrue(log.is_file())
        self.assertIn("92561", log.read_text(encoding="utf-8") + MOVIMENTOS[1])
        self.assertIn(MOVIMENTOS[0], log.read_text(encoding="utf-8"))

    def test_retrato_guarda_os_movimentos_para_a_proxima_comparacao(self):
        with self._consulta(MOVIMENTOS):
            mon.verificar("teste", CFG)
        dados = json.loads((Path(self.tmp.name) / "teste.json").read_text(encoding="utf-8"))
        self.assertEqual(dados["movimentos"], MOVIMENTOS)

    def test_portal_mudou_de_formato_vira_erro_e_nao_silencio(self):
        """Zero movimento é falha de leitura, não processo sem andamento."""
        with mock.patch.object(mon.urllib.request, "urlopen") as u:
            u.return_value.__enter__.return_value.read.return_value = b"<html>nada</html>"
            with self.assertRaises(RuntimeError):
                mon.consultar("0")


if __name__ == "__main__":
    unittest.main(verbosity=2)
