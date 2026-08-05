# -*- coding: utf-8 -*-
"""Regressão do gate de escrita humana e de suas barreiras anti-autocertificação."""

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from forja_estilo_humano import analisar, mandatory_prompt_for_phase, relatorio
from forja_n3_common import ForjaN3Error
from forja_package import validate_f7
from forja_render_docx import render
from forja_run import _validate_human_style


class DeveBloquear(unittest.TestCase):
    def assertRegra(self, texto, regra, tipo="peca"):
        p0 = [item for item in analisar(texto, tipo) if item["sev"] == "P0"]
        self.assertTrue(any(regra in item["gate"] for item in p0), p0)

    def test_formulas_contrastivas(self):
        self.assertRegra(
            "Não apenas a decisão ignorou o laudo, mas também deixou de examinar o contrato.",
            "contraste-formular",
        )
        self.assertRegra(
            "A questão não é a existência do crédito, mas a sua exigibilidade.",
            "contraste-formular",
        )
        self.assertRegra(
            "Não se trata de rever a prova, mas de aplicar a consequência jurídica correta.",
            "contraste-formular",
        )

    def test_metadiscurso_cliche_e_dogmatismo(self):
        self.assertRegra("Vale destacar que a ciência é o alicerce do progresso.", "metadiscurso-vazio")
        self.assertRegra("Claramente, a parte nunca comprovou o pagamento.", "dogmatismo-retorico")

    def test_lugar_comum_juridico_sem_fonte(self):
        self.assertRegra(
            "É cediço que a Administração deve observar os princípios constitucionais.",
            "metadiscurso-vazio",
        )
        self.assertRegra(
            "Como se sabe, a tutela jurisdicional deve ser efetiva.",
            "metadiscurso-vazio",
        )

    def test_ritmo_robotico(self):
        texto = (
            "O autor apresenta o referencial teórico. Ele descreve a metodologia adotada. "
            "Ele analisa os dados coletados. Ele discute os resultados obtidos."
        )
        self.assertRegra(texto, "ritmo-robotico")

    def test_conclusao_tautologica(self):
        texto = """
O contrato foi assinado em maio e prevê pagamento em trinta dias.

A nota fiscal venceu em junho, mas permaneceu sem quitação.

A cobrança abrange o principal e a correção prevista no contrato.

Assim, o contrato assinado e a nota vencida demonstram a falta de pagamento.
"""
        self.assertRegra(texto, "conclusao-tautologica")

    def test_pacote_recomputa_p0_forjado(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            md = root / "peca.md"
            texto = "Vale destacar que a questão não é o fato, mas a consequência."
            md.write_text(texto, encoding="utf-8")
            sha = hashlib.sha256(md.read_bytes()).hexdigest()
            f7 = root / "f7.json"
            f7.write_text(json.dumps({"p0": 0, "mdSha256": sha}), encoding="utf-8")
            resultado = validate_f7(
                {"path": str(f7)}, document_key=None, release_policy="strict_protocol",
                markdown={"path": str(md), "sha256": sha},
            )
            self.assertFalse(resultado["approved"])
            self.assertGreater(resultado["recomputedP0"], 0)

    def test_executor_f6_recomputa_gate(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "draft.md"
            path.write_text("Obviamente, a questão não é o prazo, mas a prova.", encoding="utf-8")
            with self.assertRaises(ForjaN3Error) as ctx:
                _validate_human_style(
                    "F6_REDACAO_TEMPLATE",
                    [{"artifactId": "draft_markdown", "source": path}],
                )
            self.assertIn("escrita humana", str(ctx.exception))

    def test_render_persiste_relatorio_e_nao_gera_word_com_p0(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            md = root / "minuta.md"
            md.write_text("Vale destacar que, obviamente, a tese procede.", encoding="utf-8")
            out = root / "saida"
            with self.assertRaises(RuntimeError):
                render(md, out, "Minuta")
            self.assertTrue((out / "F7_VERIFICADOR_FORJA.json").is_file())
            self.assertFalse((out / "minuta.docx").exists())

    def test_email_com_formulas_automaticas(self):
        texto = (
            "Prezado Dr. Fábio,\n\n"
            "Espero que este e-mail o encontre bem. Gostaria de informar que realizei uma análise detalhada.\n\n"
            "Permaneço à disposição para quaisquer esclarecimentos adicionais."
        )
        p0 = [item for item in analisar(texto, "email") if item["sev"] == "P0"]
        self.assertGreaterEqual(len(p0), 3, p0)
        self.assertTrue(all("email-" in item["gate"] for item in p0), p0)

    def test_email_com_cara_de_relatorio(self):
        self.assertRegra(
            "Prezado Fábio,\n\n## Resumo executivo\n\nSegue a peça revisada.",
            "email-cara-de-relatorio",
            tipo="email",
        )

    def test_email_ignora_formula_no_historico_citado(self):
        texto = (
            "Fábio,\n\nAjustei o pedido da página 7. Seguem Word e PDF.\n\n"
            "> Espero que este e-mail o encontre bem.\n"
            "> Gostaria de informar que a versão anterior foi recebida."
        )
        p0_email = [
            item for item in analisar(texto, "email")
            if item["sev"] == "P0" and "email-" in item["gate"]
        ]
        self.assertEqual([], p0_email)

    def test_email_ignora_historico_encaminhado_no_gate_comum(self):
        texto = (
            "Fábio,\n\nSegue a versão com o ajuste da página 7.\n\n"
            "---------- Forwarded message ---------\n"
            "Obviamente, a questão não é o prazo, mas a prova."
        )
        p0 = [item for item in analisar(texto, "email") if item["sev"] == "P0"]
        self.assertEqual([], p0)


class NaoPodeTravar(unittest.TestCase):
    def assertSemP0(self, texto):
        p0 = [item for item in analisar(texto, "peca") if item["sev"] == "P0"]
        self.assertEqual([], p0)

    def test_conector_isolado_e_contraste_natural(self):
        self.assertSemP0(
            "Contudo, o evento 185 contém o comprovante bancário de 5 de maio. "
            "O documento identifica favorecido, valor e autenticação."
        )
        self.assertSemP0("O recurso não trata da perícia contábil juntada no evento 12.")

    def test_absoluto_com_fonte_e_citacao_transcrita(self):
        achados = analisar("O art. 10 da Lei 12.016/2009 incide sempre que a inicial for inepta.", "peca")
        self.assertFalse(any(item["sev"] == "P0" for item in achados), achados)
        self.assertSemP0(
            '> "Não apenas se exige a prova, mas também sua contemporaneidade", registrou o acórdão.\n\n'
            "O trecho acima é transcrição literal do evento 42."
        )

    def test_prompt_so_em_f6_f7(self):
        self.assertIn("ESCRITA HUMANA", mandatory_prompt_for_phase("F6_REDACAO_TEMPLATE"))
        self.assertIn("ESCRITA HUMANA", mandatory_prompt_for_phase("F7_AUDITORIA_JURIDICA_FACTUAL"))
        self.assertIn("FORJA-GOSTO-EDGE-v1", mandatory_prompt_for_phase("F6_REDACAO_TEMPLATE"))
        self.assertIn("EXACTING", mandatory_prompt_for_phase("F7_AUDITORIA_JURIDICA_FACTUAL"))
        self.assertIn("E-MAIL HUMANO", mandatory_prompt_for_phase("F9_PACOTE_REVISAO_DRAFT_OPCIONAL"))
        self.assertEqual("", mandatory_prompt_for_phase("F5_PESQUISA_OFICIAL"))

    def test_email_direto_e_pessoal(self):
        texto = (
            "Fábio,\n\n"
            "Revisei a impugnação e anexei as versões em Word e PDF. O argumento sobre a fl. 938 "
            "agora está ligado ao pedido de não conhecimento.\n\n"
            "Pontos que exigem o seu olho:\n"
            "- confirmar a data da intimação, indicada na página 3;\n"
            "- decidir se mantemos o pedido subsidiário da página 9.\n\n"
            "Fico à disposição."
        )
        p0 = [item for item in analisar(texto, "email") if item["sev"] == "P0"]
        self.assertEqual([], p0)

    def test_relatorio_nao_finge_probabilidade_de_autoria(self):
        resultado = relatorio("O documento do evento 42 contém o recibo.", "peca")
        self.assertIn("não estima autoria", resultado["metodo"])
        self.assertNotIn("probabilidade", {k.lower() for k in resultado})


if __name__ == "__main__":
    unittest.main(verbosity=2)
