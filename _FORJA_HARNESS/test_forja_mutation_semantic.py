# -*- coding: utf-8 -*-
"""Regressão da mutação semântica (M3.1 do plano 19).

DEVE_PEGAR: operadores geram mutantes; suíte/verificador matam; gate de sanidade
impede o score 1.0 falso (visto no primeiro run real de 12/07). NÃO_PODE_TRAVAR:
controles benignos vivem; texto sem padrões não explode; determinismo.
Roda com: python test_forja_mutation_semantic.py
"""
import json
import tempfile
import unittest
from pathlib import Path

from forja_mutation_semantic import rodar, _aplicar, OPERADORES

TEXTO = (
    "EXCELENTÍSSIMO SENHOR DESEMBARGADOR RELATOR.\n"
    "1. O agravante sustenta que é cabível a condenação, pois restou comprovado "
    "o dano em 22 de fevereiro de 2013, no valor de R$ 165.000,00.\n"
    "2. Nesse contexto, o STJ firmou entendimento no REsp 1.795.982/SP, e a "
    "Súmula 362 do STJ define o termo da correção monetária.\n"
    "3. Ademais, requer o provimento da apelação, com a procedência do pedido.\n"
)

SUITE = {"tests": [
    {"testId": "CT-1", "severity": "blocking", "method": "deterministic",
     "evaluator": {"kind": "contains", "value": "R$ 165.000,00"}},
    {"testId": "CT-2", "severity": "blocking", "method": "deterministic",
     "evaluator": {"kind": "contains", "value": "22 de fevereiro de 2013"}},
    {"testId": "CT-3", "severity": "blocking", "method": "deterministic",
     "evaluator": {"kind": "contains", "value": "é cabível a condenação"}},
]}

TEXTO_S5 = (
    "A tese foi confirmada pelo REsp 1.234.567/DF.\n"
)


def _rodar(texto=TEXTO, suite=SUITE):
    with tempfile.TemporaryDirectory() as tmp:
        draft = Path(tmp) / "minuta.md"
        draft.write_text(texto, encoding="utf-8")
        return rodar(suite, draft)


class DevePegar(unittest.TestCase):

    def setUp(self):
        self.r = _rodar()

    def test_todas_familias_geram_mutantes_no_texto_sintetico(self):
        aplicaveis = {f for f, s in self.r["porFamilia"].items() if s["aplicaveis"]}
        self.assertEqual(aplicaveis, set(OPERADORES))

    def test_inversao_de_tese_e_morta_pela_suite(self):
        s1 = [m for m in self.r["mutantes"] if m["familia"] == "S1_inversao_tese"]
        self.assertTrue(any(m["killed"] and str(m["killer"]).startswith("case_test")
                            for m in s1), s1)

    def test_troca_sumula_tribunal_e_morta_pelo_verificador(self):
        s6 = [m for m in self.r["mutantes"] if m["familia"] == "S6_deturpacao_precedente"]
        self.assertTrue(any(m["killed"] and "G4-sumula" in str(m["killer"]) for m in s6), s6)

    def test_sobreabstracao_p1_e_contabilizada(self):
        r = _rodar(texto=TEXTO_S5, suite={"tests": []})
        s5 = [m for m in r["mutantes"] if m["familia"] == "S5_sobreabstracao"]
        self.assertTrue(
            any(m["killed"] and "S5-sobreabstracao:P1" in str(m["killer"]) for m in s5),
            s5,
        )

    def test_mutacao_de_valor_e_morta(self):
        s3 = [m for m in self.r["mutantes"] if m["familia"] == "S3_valor_ou_data"]
        self.assertTrue(any(m["killed"] for m in s3), s3)

    def test_gate_de_sanidade_suite_quebrada_nunca_da_score_falso(self):
        """Lição do primeiro run real (12/07): suíte que reprova o ORIGINAL
        mataria qualquer mutante — 24/24 falso. Tem que reprovar por regra."""
        suite_quebrada = {"tests": [
            {"testId": "CT-X", "severity": "blocking", "method": "deterministic",
             "evaluator": {"kind": "contains", "value": "texto que não existe na minuta"}}]}
        r = _rodar(suite=suite_quebrada)
        self.assertFalse(r["suiteValida"])
        self.assertFalse(r["aprovado"])
        self.assertEqual(r["suiteReprovaOriginal"], "CT-X")
        # nenhum mutante pode ter sido morto pelo canal case_test inválido
        self.assertTrue(all(not str(m["killer"]).startswith("case_test")
                            for m in r["mutantes"] if m["killed"]))

    def test_familias_fracas_sao_nominadas(self):
        fracas = self.r["familiasAbaixoDoAlvo"]
        for f in fracas:
            self.assertTrue(self.r["porFamilia"][f]["aplicaveis"] > 0)
        # com score < 1.0 total, ao menos o campo existe e é lista
        self.assertIsInstance(fracas, list)


class NaoPodeTravar(unittest.TestCase):

    def test_controles_benignos_nao_sao_mortos(self):
        r = _rodar()
        self.assertEqual(r["controlesMortos"], [],
                         f'paráfrase neutra morta: {r["controlesBenignos"]}')

    def test_texto_sem_padroes_nao_explode(self):
        r = _rodar(texto="Documento administrativo sem conteúdo processual.\n",
                   suite={"tests": []})
        self.assertEqual(r["aplicaveis"], 0)
        self.assertEqual(r["semanticMutationScore"], 0.0)

    def test_determinismo(self):
        a, b = _rodar(), _rodar()
        for chave in ("semanticMutationScore", "aplicaveis", "mortos", "porFamilia"):
            self.assertEqual(a[chave], b[chave])
        self.assertEqual([m["mutationId"] for m in a["mutantes"]],
                         [m["mutationId"] for m in b["mutantes"]])

    def test_aplicar_ocorrencia_inexistente_retorna_none(self):
        self.assertIsNone(_aplicar("sem padrão aqui", r"\bagravante\b", "agravado", 0))


if __name__ == "__main__":
    unittest.main(verbosity=2)
