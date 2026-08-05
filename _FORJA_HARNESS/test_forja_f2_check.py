# -*- coding: utf-8 -*-
"""Regressão da coerência F2 (M4.3 do plano 19).

Casos de tribunal calcados no mapa real da fábrica (CLAUDE.md): J4 = Justiça
Federal (TR indica o TRF); 8.27 = TJTO; AREsp/REsp = STJ; RE/ARE = STF.
Roda com: python test_forja_f2_check.py
"""
import unittest

from forja_f2_check import tribunal_do_cnj, tribunais_do_texto, validar_classificacao


class DevePegar(unittest.TestCase):

    def test_cnj_federal_trf1(self):
        # caso real da fábrica: Laudo Pericial Contábil
        self.assertEqual(tribunal_do_cnj("9000001-00.1997.4.01.0000"), "TRF1")

    def test_cnj_federal_trf4(self):
        # caso real: Jalusa (TRF4)
        self.assertEqual(tribunal_do_cnj("9000004-00.2011.4.04.0000"), "TRF4")

    def test_cnj_estadual_tjto(self):
        # caso real: CASO-15 (AI TJTO)
        self.assertEqual(tribunal_do_cnj("9000012-00.2023.8.27.0000"), "TJTO")

    def test_cnj_estadual_tjrj(self):
        # caso real: CASO-19
        self.assertEqual(tribunal_do_cnj("9000003-00.2014.8.19.0000"), "TJRJ")

    def test_classe_aresp_infere_stj(self):
        self.assertIn("STJ", tribunais_do_texto("AgInt no AREsp nº 2.698.443/DF"))

    def test_tribunal_declarado_divergente_vira_p1(self):
        achados = validar_classificacao(
            {"product": "memoriais", "tribunal": "TJTO"},
            "Processo 9000003-00.2014.8.19.0000 — apelação")
        self.assertTrue(any(a["campo"] == "tribunal" for a in achados))

    def test_perfil_pso_invalido_vira_p1(self):
        achados = validar_classificacao(
            {"product": "parecer", "psoProfile": "gigante"}, "")
        self.assertTrue(any(a["campo"] == "psoProfile" for a in achados))

    def test_produto_vazio_vira_p1(self):
        achados = validar_classificacao({"product": "  "}, "")
        self.assertTrue(any(a["campo"] == "product" for a in achados))


class NaoPodeTravar(unittest.TestCase):

    def test_classificacao_coerente_e_silencio(self):
        achados = validar_classificacao(
            {"product": "memoriais", "complexity": "high", "tribunal": "TJRJ",
             "psoProfile": "completo"},
            "Processo 9000003-00.2014.8.19.0000")
        self.assertEqual(achados, [])

    def test_sem_cnj_no_texto_nao_acusa_tribunal(self):
        achados = validar_classificacao(
            {"product": "parecer", "tribunal": "STJ"}, "texto sem número de processo")
        self.assertFalse(any(a["campo"] == "tribunal" for a in achados))

    def test_texto_vazio_e_dict_vazio_nao_explodem(self):
        self.assertIsNone(tribunal_do_cnj(""))
        self.assertEqual(tribunais_do_texto(""), set())
        achados = validar_classificacao({}, "")
        self.assertTrue(all(a["sev"] == "P1" for a in achados))


if __name__ == "__main__":
    unittest.main(verbosity=2)
