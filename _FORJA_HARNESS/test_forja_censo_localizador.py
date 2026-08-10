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
            "Pacote ENTREGA_FINAL.zip entregue pelo WhatsApp 3EB0F1F1F1F1F1F1F1F1F1")
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


class TestDivergenciaSeApuraPorSentido(unittest.TestCase):
    """`fulfilled` e `fulfilled_by_forja_f10` são o mesmo estado em dois
    vocabulários, e a decisão de situação sempre os tratou assim. Comparar as
    cadeias cruas acusava 5 divergências que não existiam."""

    def _caso_com_dois_esquemas(self, raiz, legado, n3, modo="shadow"):
        d = raiz / "case-x"
        d.mkdir(parents=True)
        (d / "FORJA_STATE.json").write_text(json.dumps(
            {"caseId": "case-x", "status": legado,
             "deliveryEvidence": {"status": "ok", "detail": "e-mail 19fc8853eadd3438"}}),
            encoding="utf-8")
        (d / "FORJA_N3_STATE.json").write_text(json.dumps(
            {"caseId": "case-x", "lifecycleStatus": n3}), encoding="utf-8")
        (d / "FORJA_CASE_MANIFEST.json").write_text(json.dumps({"mode": modo}),
                                                    encoding="utf-8")
        return d

    def _um(self, legado, n3, modo="shadow", conferido=False):
        with tempfile.TemporaryDirectory() as tmp:
            raiz = Path(tmp)
            self._caso_com_dois_esquemas(raiz, legado, n3, modo)
            conf = {"case-x": {"resultado": "confere"}} if conferido else {}
            return forja_censo.censo(raiz, resolucoes={},
                                     conferencias=conf)["casos"][0]

    def test_sinonimos_terminais_nao_sao_divergencia(self):
        for n3 in ("fulfilled_by_forja_f10", "complete", "superseded"):
            with self.subTest(n3=n3):
                self.assertFalse(self._um("fulfilled", n3)["esquemasDivergem"])

    def test_sombra_diferente_do_legado_e_esperado_e_nao_pendencia(self):
        c = self._um("fulfilled", "pending", modo="shadow")
        self.assertTrue(c["esquemasDivergem"])
        self.assertEqual(c["arbitro"]["veredito"], "n3_e_sombra")

    def test_n3_nao_sombra_parado_com_entrega_provada_e_achado(self):
        """Contraprova do anterior: fora do modo sombra, o mesmo par acusa."""
        c = self._um("fulfilled", "pending", modo="pilot_blocking", conferido=True)
        self.assertEqual(c["arbitro"]["veredito"], "n3_parou_no_meio")

    def test_sem_conferencia_o_arbitro_nao_escolhe_vencedor(self):
        """Localizador registrado e não conferido não prova entrega — e o árbitro
        que chutasse aqui estaria decidindo por impaciência, não por evidência."""
        c = self._um("fulfilled", "pending", modo="pilot_blocking", conferido=False)
        self.assertEqual(c["arbitro"]["veredito"], "conflito_real")

    def test_carimbo_sem_prova_nao_vira_achado_proprio(self):
        """Ele só ocorre junto de `concluido_sem_prova`: seria contar duas vezes."""
        with tempfile.TemporaryDirectory() as tmp:
            raiz = Path(tmp)
            d = self._caso_com_dois_esquemas(raiz, "fulfilled", "pending")
            (d / "FORJA_STATE.json").write_text(json.dumps(
                {"caseId": "case-x", "status": "fulfilled",
                 "deliveryEvidence": {"status": "ok", "detail": "entregue, sem id"}}),
                encoding="utf-8")
            dados = forja_censo.censo(raiz, resolucoes={}, conferencias={})
            achados = forja_censo.gate_censo(dados)
        self.assertEqual(dados["casos"][0]["arbitro"]["veredito"],
                         "legado_carimbou_sem_prova")
        self.assertEqual([a["id"] for a in achados if a["id"] == "CEN6"], [])


class TestConferenciaNaoViraEntregue(unittest.TestCase):
    """Conferir prova que a mensagem existe, não que o conteúdo era o esperado.

    Se `entrega_conferida` virasse `entregue`, o relatório perderia a distinção
    que a conferência acabou de criar — dois graus de prova com um nome só.
    """

    def test_conferido_e_situacao_propria_e_traz_destinatario(self):
        with tempfile.TemporaryDirectory() as tmp:
            raiz = Path(tmp)
            _caso(raiz, "case-x", "enviado em 19fc8853eadd3438")
            dados = forja_censo.censo(raiz, resolucoes={}, conferencias={
                "case-x": {"resultado": "confere", "para": "fulano@exemplo.com",
                           "data": "Wed, 8 Jul 2026 20:13:11 -0300"}})
        c = dados["casos"][0]
        self.assertEqual(c["situacao"], "entrega_conferida")
        self.assertIn("fulano@exemplo.com", c["porque"])
        self.assertIn("não que o conteúdo", c["porque"])

    def test_conferencia_que_nao_confere_nao_promove(self):
        with tempfile.TemporaryDirectory() as tmp:
            raiz = Path(tmp)
            _caso(raiz, "case-x", "enviado em 19fc8853eadd3438")
            dados = forja_censo.censo(raiz, resolucoes={}, conferencias={
                "case-x": {"resultado": "nao_encontrado"}})
        self.assertEqual(dados["casos"][0]["situacao"], "entrega_declarada")


class TestDeclaracaoHumana(unittest.TestCase):
    """A pessoa declara o que a máquina não afere — e só o que o vocabulário admite.

    `entrega_atestada` veio de um caso medido em 10/08/2026: produto de mídia,
    289 arquivos e 386 MB entregues na pasta da demanda, nenhum deles `.docx` ou
    `.pdf`, que é a única prova que esta régua lê. Afrouxar a régua para todos
    seria aceitar qualquer arquivo como prova de petição entregue; a saída é
    deixar alguém dizer o que viu, respondendo pelo que disse.
    """

    def _com_declaracao(self, resolucao):
        with tempfile.TemporaryDirectory() as tmp:
            raiz = Path(tmp)
            _caso(raiz, "case-x", "entregue, sem identificador")
            dados = forja_censo.censo(raiz, resolucoes={"case-x": resolucao},
                                      conferencias={})
        return dados["casos"][0]

    def test_entrega_atestada_sai_de_sem_prova_e_nao_vira_entregue(self):
        c = self._com_declaracao({"situacao": "entrega_atestada",
                                  "por": "Fulano", "motivo": "kit de mídia"})
        self.assertEqual(c["situacao"], "entrega_atestada")
        self.assertIn("Fulano", c["porque"])

    def test_declaracao_antiga_sem_campo_continua_valendo(self):
        """O arquivo de resoluções já tem registros sem `situacao`; quebrar a
        leitura deles trocaria um defeito por outro."""
        c = self._com_declaracao({"por": "Fulano", "motivo": "não era tarefa"})
        self.assertEqual(c["situacao"], "triado_sem_demanda")

    def test_declarar_grava_a_situacao_pedida_e_quem_respondeu(self):
        """Sem este, a categoria podia sumir do vocabulário de escrita e nenhum
        teste notaria: os demais montam o registro à mão e nunca passam por
        `declarar`. Foi a contraprova que apontou o buraco, não a suíte."""
        with tempfile.TemporaryDirectory() as tmp:
            alvo = Path(tmp) / "r.json"
            forja_censo.declarar("case-x", "kit de mídia entregue por link",
                                 "Fulano", situacao="entrega_atestada", path=alvo)
            reg = json.loads(alvo.read_text(encoding="utf-8"))["casos"]["case-x"]
        self.assertEqual(reg["situacao"], "entrega_atestada")
        self.assertEqual(reg["por"], "Fulano")
        self.assertIn("em", reg, "declaração sem data não responde por quando")

    def test_situacao_fora_do_vocabulario_e_recusada_na_escrita(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(forja_censo.CensoError):
                forja_censo.declarar("case-x", "m", "p", situacao="entregue",
                                     path=Path(tmp) / "r.json")

    def test_atestada_nao_deve_nada_e_sem_prova_deve(self):
        """Se `entrega_atestada` entrasse em DEVENDO, declarar não fecharia nada."""
        self.assertNotIn("entrega_atestada", forja_censo.DEVENDO)
        self.assertIn("concluido_sem_prova", forja_censo.DEVENDO)


if __name__ == "__main__":
    unittest.main()
