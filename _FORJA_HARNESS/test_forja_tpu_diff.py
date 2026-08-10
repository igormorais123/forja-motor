# -*- coding: utf-8 -*-
"""Regressão do comparador entre versões das TPU do CNJ.

O comparador só serve se detectar **cada** categoria que o procedimento de
manutenção exige, e se não inventar nenhuma. Um diff que devolve zero é
indistinguível de um diff quebrado — o controle "versão contra ela mesma dá
zero" prova pouco sozinho, e por isso aqui cada categoria tem a sua mutação.

A armadilha específica que o último teste tranca: **sumir a data de inativação
não prova reativação.** Pode ser reativação, pode ser correção da data. O CNJ
tem coluna própria para reativar, e quando as duas discordam o item precisa ir
para conferência humana, nunca virar veredito automático.
"""

import sqlite3
import tempfile
import unittest
from pathlib import Path

from forja_tpu import ESQUEMA
from forja_tpu_diff import carregar, comparar, relatorio

COLUNAS = ("tabela", "segmento", "codigo", "cod_pai", "descricao", "glossario",
           "dt_publicacao", "dt_alteracao", "dt_inativacao", "dt_reativacao",
           "extras", "arquivo")


def _item(codigo, descricao, pai=None, glossario=None,
          inativacao=None, reativacao=None):
    return ("assuntos", "STJ", codigo, pai, descricao, glossario,
            "2021-01-11", None, inativacao, reativacao, None, "f.xls")


BASE = [
    _item("1", "Direito Administrativo"),
    _item("11559", "Improbidade Administrativa", pai="1"),
    _item("200", "Dano ao Erário", pai="11559", glossario="texto antigo"),
    _item("300", "Enriquecimento Ilícito", pai="11559"),
    _item("400", "Verba de Representação", pai="1", inativacao="2024-02-02"),
]


def _banco(itens, destino: Path) -> Path:
    con = sqlite3.connect(destino)
    con.executescript(ESQUEMA)
    con.executemany(
        f"INSERT INTO itens ({','.join(COLUNAS)}) "
        f"VALUES ({','.join('?' * len(COLUNAS))})", itens)
    con.commit()
    con.close()
    return destino


class TestComparador(unittest.TestCase):
    def _diff(self, depois):
        with tempfile.TemporaryDirectory() as tmp:
            a = _banco(BASE, Path(tmp) / "a.sqlite")
            b = _banco(depois, Path(tmp) / "b.sqlite")
            return comparar(carregar(a), carregar(b))

    def test_versao_igual_nao_acusa_nada(self):
        d = self._diff(BASE)
        self.assertFalse(d["houveMudanca"])
        self.assertEqual(sum(d["resumo"].values()), 0)

    def test_codigo_novo(self):
        d = self._diff(BASE + [_item("500", "Concessão Indevida", pai="11559")])
        self.assertEqual([i["codigo"] for i in d["acrescentados"]], ["500"])

    def test_codigo_que_saiu_do_export_nao_e_inativacao(self):
        """Inativado ainda existe e aparece em processo antigo; removido, não."""
        d = self._diff([i for i in BASE if i[2] != "300"])
        self.assertEqual([i["codigo"] for i in d["removidos"]], ["300"])
        self.assertEqual(d["inativados"], [])

    def test_inativacao(self):
        mutado = [_item("300", "Enriquecimento Ilícito", pai="11559",
                        inativacao="2026-07-01") if i[2] == "300" else i
                  for i in BASE]
        d = self._diff(mutado)
        self.assertEqual([(i["codigo"], i["em"]) for i in d["inativados"]],
                         [("300", "2026-07-01")])

    def test_reativacao_com_data_propria(self):
        mutado = [_item("400", "Verba de Representação", pai="1",
                        reativacao="2026-07-01") if i[2] == "400" else i
                  for i in BASE]
        d = self._diff(mutado)
        self.assertEqual([i["codigo"] for i in d["reativados"]], ["400"])
        self.assertEqual(d["divergencias"], [])

    def test_data_de_inativacao_que_some_sem_reativacao_vai_para_conferencia(self):
        """O caso que não se pode adivinhar: reativou ou corrigiu a data?"""
        mutado = [_item("400", "Verba de Representação", pai="1")
                  if i[2] == "400" else i for i in BASE]
        d = self._diff(mutado)
        self.assertEqual(d["reativados"], [], "reativação inferida sem lastro")
        self.assertEqual([i["codigo"] for i in d["divergencias"]], ["400"])

    def test_mudanca_de_hierarquia(self):
        mutado = [_item("200", "Dano ao Erário", pai="1",
                        glossario="texto antigo") if i[2] == "200" else i
                  for i in BASE]
        d = self._diff(mutado)
        self.assertEqual([(i["codigo"], i["paiAntes"], i["paiDepois"])
                          for i in d["hierarquia"]], [("200", "11559", "1")])

    def test_descricao_e_glossario_sao_categorias_distintas(self):
        mutado = [_item("200", "Dano ao Erário Público", pai="11559",
                        glossario="texto novo") if i[2] == "200" else i
                  for i in BASE]
        d = self._diff(mutado)
        self.assertEqual([i["codigo"] for i in d["descricao"]], ["200"])
        self.assertEqual([i["codigo"] for i in d["glossario"]], ["200"])

    def test_codigo_repetido_com_conteudo_diferente_vai_para_conferencia(self):
        """O CNJ redeclara nó de topo; se as cópias discordarem, alguém decide."""
        d = self._diff(BASE + [_item("1", "Direito Administrativo e Militar")])
        self.assertIn("1", [i["codigo"] for i in d["divergencias"]])


class TestRelatorio(unittest.TestCase):
    def test_sem_mudanca_diz_isso_em_vez_de_tabela_vazia(self):
        with tempfile.TemporaryDirectory() as tmp:
            a = _banco(BASE, Path(tmp) / "a.sqlite")
            texto = relatorio(comparar(carregar(a), carregar(
                _banco(BASE, Path(tmp) / "b.sqlite"))), "v1", "v2")
        self.assertIn("Nenhuma diferença", texto)

    def test_corte_por_categoria_e_declarado_e_nao_silencioso(self):
        """Truncar sem dizer quanto ficou de fora lê-se como 'foi tudo'."""
        extras = [_item(str(1000 + n), f"Novo {n}", pai="1") for n in range(45)]
        with tempfile.TemporaryDirectory() as tmp:
            a = _banco(BASE, Path(tmp) / "a.sqlite")
            b = _banco(BASE + extras, Path(tmp) / "b.sqlite")
            texto = relatorio(comparar(carregar(a), carregar(b)), "v1", "v2",
                              limite=40)
        self.assertIn("e mais **5**", texto)


if __name__ == "__main__":
    unittest.main()
