# -*- coding: utf-8 -*-
"""Regressão do que o censo aceita como prova de entrega, e do órfão sem estado.

Dois defeitos reais de 10/08/2026, medidos antes de consertados:

**O censo conhecia um dialeto só.** `deliveryEvidence` traz o localizador da
entrega, e o reconhecedor aceitava exclusivamente o ID de mensagem do Gmail.
Sobre as 88 pastas com estado: 77 citavam o ID do Gmail, 1 o ID da mensagem do
WhatsApp, 1 o arquivo entregue e 5 eram prosa de verdade. Os dois do meio caíam
em `concluido_sem_prova` — o P0 de "diz-se cumprido, sem nada" — tendo prova
conferível registrada. A acusação mais grave por incapacidade de ler.

**Duas pastas de caso não tinham estado.** Enquanto existiam, o censo lia 89 de
91 e nenhum número dele era retrato da população: não se afirma "55 entregues"
sobre o que não se conseguiu ler inteiro.

O que estes testes trancam é a assimetria: caminho citado **que existe** é
prova; caminho citado que não existe é prosa com aparência de prova, que é pior.
"""

import json
import tempfile
import unittest
from pathlib import Path

import forja_censo
import forja_estado_orfao


def _caso(raiz: Path, nome: str, detalhe: str | None, status="fulfilled") -> Path:
    d = raiz / nome
    d.mkdir(parents=True)
    estado = {"caseId": nome, "status": status, "currentPhase": "F10_ENTREGA",
              "deliveryEvidence": ({"status": "manual_override", "detail": detalhe}
                                   if detalhe is not None else None)}
    (d / "FORJA_STATE.json").write_text(json.dumps(estado, ensure_ascii=False),
                                        encoding="utf-8")
    return d


class TestDialetosDeLocalizador(unittest.TestCase):
    def _situacao(self, detalhe: str) -> tuple[str, str]:
        with tempfile.TemporaryDirectory() as tmp:
            raiz = Path(tmp)
            _caso(raiz, "case-x", detalhe)
            dados = forja_censo.censo(raiz, resolucoes={})
            c = dados["casos"][0]
            return c["situacao"], c["porque"]

    def test_id_do_gmail_continua_valendo(self):
        s, _ = self._situacao("entregue no e-mail 19fc8853eadd3438")
        self.assertEqual(s, "entrega_declarada")

    def test_id_do_whatsapp_e_localizador(self):
        """O caso real: pacote entregue ao titular pelo WhatsApp, com o ID da mensagem."""
        s, porque = self._situacao(
            "Pacote ENTREGA_FINAL.zip entregue pelo WhatsApp 3EB0C0D4F1DCEF58A21FA1")
        self.assertEqual(s, "entrega_declarada")
        self.assertIn("conversa", porque)

    def test_prosa_sem_identificador_continua_sem_prova(self):
        """Contraprova: sem esta, o reconhecedor ampliado aprovaria qualquer frase."""
        s, _ = self._situacao(
            "Triagem concluída em 13/07/2026 e respondida por e-mail ao titular")
        self.assertEqual(s, "concluido_sem_prova")

    def test_arquivo_citado_e_ausente_nao_e_prova(self):
        s, _ = self._situacao("Arquivo local: Pasta Que Nao Existe/peça final.docx")
        self.assertEqual(s, "concluido_sem_prova")


class TestCaminhoCitadoDecideNoDisco(unittest.TestCase):
    """O recorte vem de prosa e arrasta palavras; quem decide é o disco."""

    def test_caminho_com_espacos_atras_de_palavras_da_frase(self):
        with tempfile.TemporaryDirectory() as tmp:
            raiz = Path(tmp)
            pasta = raiz / "WhatsApp Audio - Protocolo de aprendizados IA - 2026-07-08"
            pasta.mkdir(parents=True)
            (pasta / "PROTOCOLO_POS_ENTREGA.md").write_text("x", encoding="utf-8")
            anterior = forja_censo.WORKSPACE
            forja_censo.WORKSPACE = raiz
            try:
                valor, dialeto = forja_censo._localizador(
                    "Evidência: Arquivo local: WhatsApp Audio - Protocolo de "
                    "aprendizados IA - 2026-07-08/PROTOCOLO_POS_ENTREGA.md")
            finally:
                forja_censo.WORKSPACE = anterior
        self.assertEqual(dialeto, "arquivo_em_disco")
        self.assertTrue(valor.endswith("PROTOCOLO_POS_ENTREGA.md"))
        self.assertFalse(valor.startswith("Evidência"), "não descascou a frase")


class TestOrfaoSemEstado(unittest.TestCase):
    def test_pasta_de_caso_sem_estado_deixa_o_censo_incompleto(self):
        with tempfile.TemporaryDirectory() as tmp:
            raiz = Path(tmp)
            _caso(raiz, "case-a", "e-mail 19fc8853eadd3438")
            (raiz / "case-orfao").mkdir()
            dados = forja_censo.censo(raiz, resolucoes={})
            self.assertFalse(dados["populacao"]["completo"])
            self.assertEqual(dados["populacao"]["pastasDeCaso"], 2)

    def test_reconstrucao_deriva_a_fase_do_artefato_e_nao_afirma_entrega(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp) / "case-orfao" / "n4_artifacts"
            d.mkdir(parents=True)
            (d / "F1_INSUMO_BLOQUEADO.json").write_text("{}", encoding="utf-8")
            estado = forja_estado_orfao.reconstruir(d.parent)
        self.assertEqual(estado["status"], "blocked")
        self.assertEqual(estado["currentPhase"], "F1_INGESTAO_AUTOS")
        self.assertIsNone(estado["deliveryEvidence"], "reconstrução afirmou entrega")
        self.assertIn("reconstruido", estado)

    def test_pasta_sem_artefato_nenhum_nasce_aberta_e_nao_entregue(self):
        """A reconstrução não pode ser a porta de fundo para carimbar cumprido."""
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp) / "case-vazio"
            d.mkdir()
            estado = forja_estado_orfao.reconstruir(d)
        self.assertEqual(estado["status"], "aberto")
        self.assertEqual(estado["artifacts"], [])

    def test_pasta_que_nao_e_caso_nao_recebe_estado(self):
        """`state/` guarda pasta que não é caso; inventar estado ali inventa caso."""
        with tempfile.TemporaryDirectory() as tmp:
            raiz = Path(tmp)
            (raiz / "prd44-revisao").mkdir()
            (raiz / "case-orfao").mkdir()
            self.assertEqual([p.name for p in forja_estado_orfao.orfaos(raiz)],
                             ["case-orfao"])


if __name__ == "__main__":
    unittest.main()
