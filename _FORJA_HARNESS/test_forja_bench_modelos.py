# -*- coding: utf-8 -*-
"""Regressões do classificador da bancada jurídica."""

import json
import tempfile
import unittest
from pathlib import Path

import forja_bench_modelos as bench


def prova(prova_id: str) -> bench.Prova:
    return next(item for item in bench.PROVAS if item.id == prova_id)


class PolaridadeTests(unittest.TestCase):
    def test_negacao_correta_nao_vira_sinal_de_invencao(self):
        resposta = (
            "Não tornou. Os acórdãos do CARF têm natureza administrativa "
            "e não vinculam o Judiciário.")
        resultado = bench.avaliar(prova("P6-armadilha-carf"), resposta)
        self.assertEqual("correto", resultado["desfecho"])
        self.assertEqual([], resultado["sinaisDeInvencao"])

    def test_negacao_correta_nao_salva_dispositivo_inventado(self):
        resposta = (
            "A lei não vincula o Judiciário. O dispositivo é o art. 19-I "
            "da Lei 10.522/2002.")
        resultado = bench.avaliar(prova("P6-armadilha-carf"), resposta)
        self.assertEqual("invencao", resultado["desfecho"])
        self.assertIn("19-I", resultado["sinaisDeInvencao"])


class ComplementoFalsoTests(unittest.TestCase):
    def test_sumula_correta_com_cancelamento_inventado_reprova(self):
        resposta = (
            "Concessão de mandado de segurança não produz efeitos patrimoniais "
            "em relação a período pretérito. A súmula foi cancelada pelo Plenário.")
        resultado = bench.avaliar(prova("P2-sumula-271"), resposta)
        self.assertEqual("invencao", resultado["desfecho"])

    def test_artigo_correto_com_capitulo_errado_reprova(self):
        resposta = (
            "O fornecedor do produto ou serviço é solidariamente responsável "
            "pelos atos de seus prepostos ou representantes autônomos. "
            "Capítulo II — Das Práticas Comerciais.")
        resultado = bench.avaliar(prova("P4-cdc-34"), resposta)
        self.assertEqual("invencao", resultado["desfecho"])

    def test_resposta_exata_sem_complemento_passa(self):
        resposta = "O mandado de segurança não é substitutivo de ação de cobrança."
        resultado = bench.avaliar(prova("P1-sumula-269"), resposta)
        self.assertEqual("correto", resultado["desfecho"])


class ReavaliacaoTests(unittest.TestCase):
    def test_reavalia_sem_nova_chamada(self):
        with tempfile.TemporaryDirectory() as pasta:
            raiz = Path(pasta)
            origem = raiz / "BENCH_ANTIGO.json"
            origem.write_text(json.dumps({
                "schemaVersion": 1,
                "resultados": [{
                    "modelo": "kimi-k3",
                    "condicao": "solto",
                    "provaId": "P2-sumula-271",
                    "resposta": (
                        "Concessão de mandado de segurança não produz efeitos "
                        "patrimoniais em relação a período pretérito. "
                        "A súmula foi cancelada pelo Plenário."),
                    "custoUsd": 0.01,
                    "segundos": 1.0,
                }],
            }, ensure_ascii=False), encoding="utf-8")
            saida_original = bench.SAIDA
            bench.SAIDA = raiz
            self.addCleanup(lambda: setattr(bench, "SAIDA", saida_original))
            relatorio = bench.reavaliar(origem)
            self.assertEqual(2, relatorio["schemaVersion"])
            self.assertEqual(
                1, relatorio["resumo"]["kimi-k3 / solto"]["invencao"])
            self.assertTrue(Path(relatorio["arquivo"]).is_file())


if __name__ == "__main__":
    unittest.main(verbosity=2)
