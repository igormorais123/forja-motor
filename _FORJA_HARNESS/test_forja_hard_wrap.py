# -*- coding: utf-8 -*-
"""Canário do detector de hard-wrap no markdown da edição visual.

O defeito real: em 05/08/2026 dois adendos foram entregues ao cliente com as
frases partidas no meio, cada pedaço recebendo um número de parágrafo, porque o
markdown estava quebrado em 80 colunas e o compositor trata cada linha como um
parágrafo. Nenhum gate reprovou — a fidelidade textual dava 100%, o lastro dava
zero, o F8-S dava conforme. Só o olho na página renderizada pegou.

Aqui o texto defeituoso real é a fixture, e a sua correção é a contraprova.
"""
import unittest

from forja_visual import detectar_hard_wrap

# O texto como foi entregue, quebrado em 80 colunas.
DEFEITUOSO = """# Adendo II

## 3. O achado que reenquadra a demanda

Em todo o contencioso declarado pela companhia, provisionado e possível, somando
mais de dois bilhões de reais, **não há uma única ação de improbidade
administrativa, nem ação popular**. A única ação civil pública mencionada é
trabalhista.
"""

# O mesmo conteúdo, cada parágrafo em uma linha.
CORRIGIDO = """# Adendo II

## 3. O achado que reenquadra a demanda

Em todo o contencioso declarado pela companhia, provisionado e possível, somando mais de dois bilhões de reais, **não há uma única ação de improbidade administrativa, nem ação popular**. A única ação civil pública mencionada é trabalhista.
"""


class CanarioDoHardWrap(unittest.TestCase):
    def test_o_defeito_real_e_acusado(self):
        """O caso que motivou o gate precisa reprovar."""
        quebras = detectar_hard_wrap(DEFEITUOSO)
        self.assertTrue(quebras, "o markdown que foi entregue quebrado passou limpo")
        self.assertGreaterEqual(len(quebras), 3)

    def test_a_correcao_passa_limpa(self):
        self.assertEqual(detectar_hard_wrap(CORRIGIDO), [])

    def test_tabela_nao_e_hard_wrap(self):
        """Linha de tabela não termina em pontuação e é legítima."""
        tabela = "| natureza | valor |\n|---|---|\n| trabalhistas | 259.045 |\n"
        self.assertEqual(detectar_hard_wrap(tabela), [])

    def test_titulo_seguido_de_prosa_nao_e_hard_wrap(self):
        self.assertEqual(detectar_hard_wrap("## Um título sem ponto\nA prosa começa aqui.\n"), [])

    def test_item_de_lista_nao_e_hard_wrap(self):
        lista = "1. Primeiro item sem ponto final\n2. Segundo item\n3. Terceiro\n"
        self.assertEqual(detectar_hard_wrap(lista), [])

    def test_bloco_de_codigo_e_poupado(self):
        codigo = "```\nx = 1\ny = 2\n```\n"
        self.assertEqual(detectar_hard_wrap(codigo), [])

    def test_paragrafos_separados_por_linha_em_branco_passam(self):
        texto = "Primeira frase termina aqui.\n\nSegunda começa e termina.\n"
        self.assertEqual(detectar_hard_wrap(texto), [])

    def test_frase_terminando_em_aspas_ou_parentese_passa(self):
        texto = 'Ele disse "assim mesmo"\nOutra linha começa.\n'
        self.assertEqual(detectar_hard_wrap(texto), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
