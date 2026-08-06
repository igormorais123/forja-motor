# -*- coding: utf-8 -*-
"""Canário do vigia do DJEN: ele acusa comunicação nova e reconhece a urgente?

O defeito que motivou o vigia foi uma intimação de pauta divulgada em julho e vista
por acaso três semanas depois, com o prazo de sustentação oral correndo. O teste
que importa é justamente esse: chega uma intimação de pauta, e o vigia precisa
gritar — e precisa distinguir a que pede leitura imediata da rotineira.

Sem rede: a consulta é substituída por um dublê. Sem cliente: os números são
inventados e montados em pedaços, porque a fronteira reprova o contrário.
"""
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import forja_monitor_djen as mon

ANTIGAS = [
    {"id": "c3", "data": "2026-06-22", "tipo": "Intimação", "orgao": "Turma",
     "resumo": "Certifico que os embargos foram opostos no prazo legal.", "urgente": True},
    {"id": "c2", "data": "2026-04-29", "tipo": "Intimação", "orgao": "Turma",
     "resumo": "Ato ordinatório sem conteúdo decisório.", "urgente": False},
]
NOVA_PAUTA = {"id": "c4", "data": "2026-07-16", "tipo": "Intimação", "orgao": "Turma",
              "resumo": "INTIMAÇÃO DE PAUTA. Sessão de julgamento em 20-08-2026.",
              "urgente": True}
NOVA_ROTINA = {"id": "c5", "data": "2026-07-20", "tipo": "Intimação", "orgao": "Turma",
               "resumo": "Juntada de substabelecimento.", "urgente": False}

CFG = {"tribunal": "TR0", "numero": "0000000-00.0000.0.00.0000", "porque": "canário"}


class CanarioDoVigiaDJEN(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        p = mock.patch.object(mon, "DESTINO", Path(self.tmp.name))
        p.start()
        self.addCleanup(p.stop)
        self.addCleanup(self.tmp.cleanup)

    def _consulta(self, comunicacoes):
        return mock.patch.object(mon, "consultar", return_value=list(comunicacoes))

    def test_primeira_leitura_vira_baseline_sem_alarme_falso(self):
        with self._consulta(ANTIGAS):
            r = mon.verificar("teste", CFG)
        self.assertTrue(r["primeiraLeitura"])
        self.assertFalse(r["houveNovidade"])
        self.assertEqual(r["total"], 2)

    def test_sem_mudanca_nao_inventa_novidade(self):
        with self._consulta(ANTIGAS):
            mon.verificar("teste", CFG)
            r = mon.verificar("teste", CFG)
        self.assertFalse(r["houveNovidade"])
        self.assertEqual(r["novidades"], [])

    def test_intimacao_de_pauta_e_acusada_como_urgente(self):
        """O caso que motivou o vigia: a pauta chega e o prazo começa a correr."""
        with self._consulta(ANTIGAS):
            mon.verificar("teste", CFG)
        with self._consulta([NOVA_PAUTA] + ANTIGAS):
            r = mon.verificar("teste", CFG)
        self.assertTrue(r["houveNovidade"])
        self.assertEqual([c["id"] for c in r["novidades"]], ["c4"])
        self.assertEqual([c["id"] for c in r["novidadesUrgentes"]], ["c4"])

    def test_comunicacao_rotineira_entra_como_novidade_mas_nao_como_urgente(self):
        with self._consulta(ANTIGAS):
            mon.verificar("teste", CFG)
        with self._consulta([NOVA_ROTINA] + ANTIGAS):
            r = mon.verificar("teste", CFG)
        self.assertTrue(r["houveNovidade"])
        self.assertEqual(r["novidadesUrgentes"], [])

    def test_novidade_fica_registrada_no_log(self):
        with self._consulta(ANTIGAS):
            mon.verificar("teste", CFG)
        with self._consulta([NOVA_PAUTA] + ANTIGAS):
            mon.verificar("teste", CFG)
        log = (Path(self.tmp.name) / "teste_novidades.log").read_text(encoding="utf-8")
        self.assertIn("URGENTE", log)
        self.assertIn("20-08-2026", log)

    def test_retrato_guarda_as_comunicacoes_para_a_proxima_comparacao(self):
        with self._consulta(ANTIGAS):
            mon.verificar("teste", CFG)
        dados = json.loads((Path(self.tmp.name) / "teste.json").read_text(encoding="utf-8"))
        self.assertEqual([c["id"] for c in dados["comunicacoes"]], ["c3", "c2"])

    def test_api_mudou_de_formato_vira_erro_e_nao_silencio(self):
        """Resposta sem a lista é falha de leitura, não processo sem comunicação."""
        with mock.patch.object(mon.urllib.request, "urlopen") as u:
            u.return_value.__enter__.return_value.read.return_value = b'{"count": 0}'
            with self.assertRaises(RuntimeError):
                mon.consultar("TR0", "0000000-00.0000.0.00.0000")

    def test_urgencia_reconhece_as_palavras_que_importam(self):
        for palavra in ("pauta", "sustentação", "julgamento", "acórdão", "prazo", "destaque"):
            with self.subTest(palavra=palavra):
                self.assertTrue(mon.URGENTE.search(f"texto com {palavra} no meio"))
        self.assertIsNone(mon.URGENTE.search("juntada de substabelecimento"))

    def test_sem_acervo_o_vigia_nao_inventa_alvo(self):
        with mock.patch.object(mon.forja_acervo, "valor", return_value={}):
            self.assertEqual(mon.vigiados(), {})

    def test_disputa_de_arquivo_e_superada_por_retentativa(self):
        """Em produção o retrato falhou com Errno 22 sob o agendador.

        Antivírus, indexador e o observador de mapas tocam o mesmo arquivo. Se a
        gravação desiste na primeira negativa, o retrato se perde e a leitura
        seguinte acusa tudo como novidade.
        """
        alvo = Path(self.tmp.name) / "retrato.json"
        real = mon.os.replace
        chamadas = {"n": 0}

        def replace_teimoso(origem, destino):
            chamadas["n"] += 1
            if chamadas["n"] < 3:
                raise OSError(22, "Invalid argument")
            return real(origem, destino)

        with mock.patch.object(mon.os, "replace", side_effect=replace_teimoso), \
                mock.patch.object(mon.time, "sleep"):
            mon.gravar_json(alvo, {"ok": True})

        self.assertEqual(chamadas["n"], 3)
        self.assertEqual(json.loads(alvo.read_text(encoding="utf-8")), {"ok": True})
        self.assertEqual(list(Path(self.tmp.name).glob("*.tmp")), [],
                         "temporário não pode sobrar depois do sucesso")

    def test_disputa_que_nao_cede_vira_erro_e_nao_silencio(self):
        alvo = Path(self.tmp.name) / "retrato.json"
        with mock.patch.object(mon.os, "replace",
                               side_effect=OSError(22, "Invalid argument")), \
                mock.patch.object(mon.time, "sleep"):
            with self.assertRaises(OSError):
                mon.gravar_json(alvo, {"ok": True})
        self.assertFalse(alvo.exists(), "retrato antigo não pode virar arquivo pela metade")


if __name__ == "__main__":
    unittest.main(verbosity=2)
