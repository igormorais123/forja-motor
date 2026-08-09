# -*- coding: utf-8 -*-
"""Regressão do leitor das Tabelas Processuais Unificadas do CNJ.

O defeito que este arquivo tranca não deu erro nenhum. A primeira versão do
leitor devolveu 60.891 itens em vez de 62.298, sem exceção, sem arquivo ilegível
e sem aviso: o CNJ fecha mal algumas linhas e emite **dois itens dentro do mesmo
`<tr>`**, e o recorte pelo fim da linha descartava o segundo. O resultado tinha
aparência de completo e trazia 1.154 itens apontando para pais inexistentes —
inclusive o código 1198, "PROCEDIMENTOS ADMINISTRATIVOS", pai de 82 classes.

A fixture é a linha emendada real do arquivo de Classes dos Juizados Especiais
Estaduais, com os textos encurtados e o número da lei trocado. O que se preserva
é a anatomia: 5 células de recuo, 14 colunas, e o segundo registro colado no fim
sem as células vazias da cauda.
"""

import unittest

from forja_tpu import _registros, _segmento, _texto

# 14 colunas, como nas tabelas de Classes.
N = 14

# Item comum: descrição, quatro células de recuo, depois as colunas.
SIMPLES = ["Transferência Entre Estabelecimentos", "", "", "", "",
           "12728", "385", "LEP", "86", "TEEP", "", "texto", "2020-06-05", "",
           "", "", "", "Criminal", "Originário"]

# A linha emendada: o item acima seguido, na MESMA linha, de um nó de topo que
# só traz descrição e código — o CNJ omite a cauda de células vazias.
EMENDADA = SIMPLES + ["PROCEDIMENTOS ADMINISTRATIVOS", "1198"]

# Item aninhado: o recuo vem antes da descrição, e é ele que desenha a árvore.
ANINHADO = ["", "", "Acordo (Outros)", "", "", "143", "11", "", "", "", "",
            "", "2021-01-11", "", "", "", "", "", ""]


class TestLinhaEmendada(unittest.TestCase):
    def test_linha_comum_da_um_item(self):
        itens = list(_registros(SIMPLES, N))
        self.assertEqual(len(itens), 1)
        descricao, dados = itens[0]
        self.assertEqual(descricao, "Transferência Entre Estabelecimentos")
        self.assertEqual(dados[:2], ["12728", "385"])

    def test_linha_emendada_da_os_dois_itens(self):
        """O item perdido era o nó-pai; sem ele a árvore quebra em 82 filhos."""
        itens = list(_registros(EMENDADA, N))
        self.assertEqual(len(itens), 2, "o segundo registro da linha se perdeu")
        self.assertEqual(itens[1][0], "PROCEDIMENTOS ADMINISTRATIVOS")
        self.assertEqual(itens[1][1][0], "1198")

    def test_cauda_omitida_e_completada_sem_deslocar_coluna(self):
        """O segundo item tem 2 células e precisa das 14 colunas, na ordem."""
        _, dados = list(_registros(EMENDADA, N))[1]
        self.assertEqual(len(dados), N)
        self.assertEqual(dados[1], "", "cód. pai inventado a partir da cauda")

    def test_recuo_antes_da_descricao_nao_vira_item(self):
        itens = list(_registros(ANINHADO, N))
        self.assertEqual([i[0] for i in itens], ["Acordo (Outros)"])
        self.assertEqual(itens[0][1][:2], ["143", "11"])

    def test_legenda_nao_vira_item(self):
        """Linha sem código numérico depois da descrição não é item da tabela."""
        legenda = ["", "Itens adicionados nesta versão."]
        self.assertEqual(list(_registros(legenda, N)), [])


class TestLeituraFielAFonte(unittest.TestCase):
    def test_entidade_html_do_glossario_e_resolvida(self):
        """O arquivo é HTML de verdade: sem isto o glossário sai com `&agrave;`."""
        self.assertEqual(
            _texto("<td>aditamento &agrave; inicial</td>"),
            "aditamento à inicial")

    def test_segmento_sai_do_nome_do_arquivo(self):
        self.assertEqual(_segmento("79_Tabela_Movimentos_CJF.xls"), "CJF")
        self.assertEqual(
            _segmento("79_Tabela_Classes_Justica_Estadual_1_Grau.xls"),
            "Justica_Estadual_1_Grau")

    def test_documentos_nao_tem_segmento(self):
        """Arquivo único; forçar um segmento aqui inventaria um ramo."""
        self.assertIsNone(_segmento("79_Tabela_Documentos_Processuais.xls"))


if __name__ == "__main__":
    unittest.main()
