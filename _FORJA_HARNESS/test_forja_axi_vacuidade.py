# -*- coding: utf-8 -*-
"""Teste de verificação: all() sem guarda em forja_axi.py — CONCLUSÃO: todas seguras.

Medição das 3 ocorrências relatadas:
- Linha 648: all(isinstance(item, dict) for item in items)
- Linha 654: all(_is_primitive(item[key]) for key in fields)
- Linha 697: all(_is_primitive(item) for item in value)

RESULTADO: Todas têm guardinhas. Nenhuma mudança necessária.
Raridade: forja_axi.py é importado APENAS por test_forja_axi.py — fachada
sem consumidor de produção.
"""

from __future__ import annotations

import unittest

from forja_axi import _is_primitive, _uniform_primitive_rows, _encode_toon_value


class TestVacuidadeAll(unittest.TestCase):
    """Verificação de que os 3 all() estão guardados contra vacuidade."""

    # ====== LINHA 648 ======
    # all(isinstance(item, dict) for item in items)
    # Guarda: short-circuit evaluation com 'not items or'

    def test_linha_648_items_vazio_nao_chama_all(self):
        """items=[] não chama all() — retorna False por 'not items'."""
        result, fields = _uniform_primitive_rows([])
        self.assertFalse(result)
        self.assertEqual(fields, [])

    def test_linha_648_items_com_nao_dicts_chama_all(self):
        """items com não-dicts chama all() e retorna False."""
        result, fields = _uniform_primitive_rows(["not a dict"])
        self.assertFalse(result)
        self.assertEqual(fields, [])

    def test_linha_648_items_com_dicts_passa_all(self):
        """items com dicts passa all() e continua análise."""
        result, fields = _uniform_primitive_rows(
            [{"a": 1}, {"a": 2}]
        )
        # Prossegue para análise de campos
        self.assertTrue(result)
        self.assertEqual(fields, ["a"])

    # ====== LINHA 654 ======
    # all(_is_primitive(item[key]) for key in fields)
    # Guarda: fields é verificado ser não-vazio nas linhas 651-652

    def test_linha_654_fields_vazio_retorna_antes_do_all(self):
        """fields=[] faz return na linha 652, antes de chegar ao all()."""
        # Teste indireto: se os dicts têm chaves vazias, retorna False
        result, fields = _uniform_primitive_rows([{}])
        self.assertFalse(result)
        self.assertEqual(fields, [])

    def test_linha_654_fields_nao_vazio_chama_all(self):
        """fields não-vazio faz all() ser chamado com campos."""
        result, fields = _uniform_primitive_rows(
            [{"x": 1, "y": "hello"}, {"x": 2, "y": "world"}]
        )
        # all() é chamado para verificar se x e y são primitivos
        self.assertTrue(result)
        self.assertIn("x", fields)
        self.assertIn("y", fields)

    def test_linha_654_fields_com_nao_primitivo_falha_all(self):
        """Valor não-primitivo no campo faz all() retornar False."""
        result, fields = _uniform_primitive_rows(
            [{"x": 1, "y": [1, 2, 3]}, {"x": 2, "y": [4, 5, 6]}]
        )
        # all(_is_primitive(...)) retorna False porque y é lista
        self.assertFalse(result)

    # ====== LINHA 697 ======
    # all(_is_primitive(item) for item in value)
    # Guarda: value é verificado ser não-vazio nas linhas 683-685

    def test_linha_697_value_vazio_retorna_antes_do_all(self):
        """value=[] faz return na linha 685, antes de chegar ao all()."""
        lines = []
        _encode_toon_value("test", [], depth=0, lines=lines)
        # Deve ter adicionado "[]" e retornado
        self.assertEqual(len(lines), 1)
        self.assertIn("[]", lines[0])

    def test_linha_697_value_nao_vazio_primitivos_chama_all(self):
        """value com primitivos chama all() e codifica em uma linha."""
        lines = []
        _encode_toon_value("test", [1, 2, 3], depth=0, lines=lines)
        # all(_is_primitive(...)) retorna True
        self.assertEqual(len(lines), 1)
        self.assertIn("[3]:", lines[0])
        self.assertIn("1,2,3", lines[0])

    def test_linha_697_value_nao_vazio_nao_primitivos_chama_all_retorna_false(self):
        """value com não-primitivos chama all() e retorna False."""
        lines = []
        _encode_toon_value("test", [1, [2, 3]], depth=0, lines=lines)
        # all(_is_primitive(...)) retorna False
        # Código cai na branch de linhas múltiplas
        self.assertGreaterEqual(len(lines), 2)
        # Primeiro deve ser "test[2]:"
        self.assertIn("[2]:", lines[0])

    # ====== TESTE DE INVARIANTE ======
    # Nunca deve haver avaliação de all() em sequência vazia

    def test_invariante_all_nunca_vazio_linha_648(self):
        """
        Propriedade: quando _uniform_primitive_rows( items ) alcança o
        all(isinstance(item, dict) for item in items) na linha 648,
        items é garantido ser não-vazio.
        """
        # Simular entrada vazia
        items_vazio = []
        # A função retorna antes do all():
        result, _ = _uniform_primitive_rows(items_vazio)
        # Se chegasse ao all([...]), teríamos resultado True (vacuidade)
        # Mas chegamos aqui com False (proteção por short-circuit)
        self.assertFalse(result)

    def test_invariante_all_nunca_vazio_linha_654(self):
        """
        Propriedade: quando o loop em linha 653 alcança o all() na linha 654,
        fields é garantido ser não-vazio (verificado nas linhas 651-652).
        """
        # Simular dicts com campos vazios
        items_campos_vazios = [{}]
        result, _ = _uniform_primitive_rows(items_campos_vazios)
        # A função retorna na linha 652 antes de alcançar linha 654
        self.assertFalse(result)

    def test_invariante_all_nunca_vazio_linha_697(self):
        """
        Propriedade: quando _encode_toon_value alcança o all() na linha 697,
        value é garantido ser não-vazio (verificado nas linhas 683-685).
        """
        lines = []
        # Lista vazia não chama all():
        _encode_toon_value("empty", [], depth=0, lines=lines)
        # Deve ter retornado cedo
        self.assertEqual(len(lines), 1)
        self.assertIn("[]", lines[0])


if __name__ == "__main__":
    unittest.main()
