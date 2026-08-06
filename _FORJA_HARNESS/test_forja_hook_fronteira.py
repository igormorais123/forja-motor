# -*- coding: utf-8 -*-
"""Regressão do aviso precoce da fronteira em Write/Edit.

O gate de publicação é a barreira real e já possui sua própria regressão. Estes
testes prendem o comportamento complementar do hook: avisar somente quando um
arquivo textual destinado ao motor recebe dado com aparência real, sem bloquear
acervo, arquivo externo ou texto limpo.
"""
from __future__ import annotations

import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import forja_fronteira  # noqa: F401  # deixa o módulo disponível ao hook
import forja_hook_fronteira as hook


class HookFronteiraTest(unittest.TestCase):
    def executar(self, raiz: Path, caminho: Path) -> tuple[int, str]:
        evento = {"tool_input": {"file_path": str(caminho)}}
        erro = io.StringIO()
        with (
            mock.patch.object(hook, "RAIZ", raiz),
            mock.patch.object(sys, "stdin", io.StringIO(json.dumps(evento))),
            mock.patch.object(sys, "stderr", erro),
        ):
            retorno = hook.main()
        return retorno, erro.getvalue()

    def test_motor_com_cnj_realista_avisa_e_declara_degradacao(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            raiz = Path(tmp)
            caminho = raiz / "_FORJA_HARNESS" / "canario.py"
            caminho.parent.mkdir(parents=True)
            cnj = "084" + "7362-19." + "2019" + ".8.26.0100"
            caminho.write_text(f"# processo {cnj}\n", encoding="utf-8")

            retorno, aviso = self.executar(raiz, caminho)

            self.assertEqual(2, retorno)
            self.assertIn("vai para o repositório do MOTOR", aviso)
            self.assertIn("CNJ:", aviso)
            self.assertIn("nome de cliente NÃO foi verificado", aviso)

    def test_texto_limpo_do_motor_passa(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            raiz = Path(tmp)
            caminho = raiz / "_FORJA_HARNESS" / "canario.py"
            caminho.parent.mkdir(parents=True)
            caminho.write_text("# biblioteca sem dado de caso\n", encoding="utf-8")

            retorno, aviso = self.executar(raiz, caminho)

            self.assertEqual(0, retorno)
            self.assertEqual("", aviso)

    def test_acervo_pode_carregar_identificador(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            raiz = Path(tmp)
            caminho = raiz / "_FORJA_HARNESS" / "state" / "case-x" / "evento.json"
            caminho.parent.mkdir(parents=True)
            cnpj = "12." + "345.678/" + "0001-95"
            caminho.write_text(json.dumps({"cnpj": cnpj}), encoding="utf-8")

            retorno, aviso = self.executar(raiz, caminho)

            self.assertEqual(0, retorno)
            self.assertEqual("", aviso)

    def test_arquivo_fora_da_pasta_de_trabalho_passa(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_raiz, tempfile.TemporaryDirectory() as tmp_fora:
            raiz = Path(tmp_raiz)
            caminho = Path(tmp_fora) / "externo.py"
            caminho.write_text("# OAB/DF " + "47" + ".913\n", encoding="utf-8")

            retorno, aviso = self.executar(raiz, caminho)

            self.assertEqual(0, retorno)
            self.assertEqual("", aviso)

    def test_evento_sem_caminho_passa(self) -> None:
        erro = io.StringIO()
        with (
            mock.patch.object(sys, "stdin", io.StringIO('{"tool_input": {}}')),
            mock.patch.object(sys, "stderr", erro),
        ):
            retorno = hook.main()
        self.assertEqual(0, retorno)
        self.assertEqual("", erro.getvalue())


if __name__ == "__main__":
    unittest.main()
