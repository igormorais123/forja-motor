"""Regressão da porta de envio: anexar é capacidade, e passa pelo mesmo gate.

Até 10/08/2026 `enviar_email` montava só o corpo. Quem quisesse mandar um
documento tinha de montar um rascunho antes — e, na prática, a esteira chegou ao
ponto de ter seis arquivos prontos para o titular e não conseguir despachá-los.
Capacidade que só existe por um caminho estreito falta justamente na hora em que
se precisa dela.

Abrir a segunda porta é onde mora o risco: em 06/08/2026 dois documentos fora do
padrão da casa seguiram para o cliente pela porta do rascunho, e foi por isso que
o gate de anexo nasceu. Uma porta nova sem a mesma barreira teria reaberto o
buraco em vez de fechar a lacuna. Estes testes prendem as duas coisas ao mesmo
tempo: o anexo sai, e o anexo fora do padrão não sai.
"""

from __future__ import annotations

import base64
import hashlib
import sys
from email import message_from_bytes
from pathlib import Path

import pytest
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt

sys.path.insert(0, str(Path(__file__).resolve().parent))

import forja_mcp_email as mcp  # noqa: E402


class _Execucao:
    def __init__(self, resultado):
        self._resultado = resultado

    def execute(self):
        return self._resultado


class _Mensagens:
    def __init__(self, caixa):
        self.caixa = caixa

    def send(self, userId=None, body=None):  # noqa: N803
        self.caixa.append(body)
        return _Execucao({"id": "msg-1", "threadId": "thr-1"})


class _Usuarios:
    def __init__(self, caixa):
        self._mensagens = _Mensagens(caixa)

    def messages(self):
        return self._mensagens


class _ServicoFalso:
    def __init__(self):
        self.caixa = []

    def users(self):
        return _Usuarios(self.caixa)


@pytest.fixture
def correio(monkeypatch):
    """Serviço e ledger de mentira; nada sai da máquina, nada é gravado."""
    svc = _ServicoFalso()
    trilha = []
    monkeypatch.setattr(mcp, "_servico", lambda: svc)
    monkeypatch.setattr(mcp, "_registrar", trilha.append)
    return svc, trilha


def _docx(caminho: Path, *, conforme: bool) -> Path:
    """Documento com parágrafos suficientes para o gate medir.

    Fora do padrão nas três dimensões é Calibri 10 sem justificação — que é
    exatamente o que o Word entrega quando ninguém define nada.
    """
    doc = Document()
    for i in range(25):
        p = doc.add_paragraph(
            f"Parágrafo {i} com texto longo o bastante para a medida ser estável "
            "e não oscilar por conta de uma linha curta isolada no documento.")
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY if conforme else WD_ALIGN_PARAGRAPH.LEFT
        for run in p.runs:
            run.font.name = "Times New Roman" if conforme else "Calibri"
            run.font.size = Pt(12) if conforme else Pt(10)
    doc.save(str(caminho))
    return caminho


def _anexos_da_caixa(corpo) -> dict:
    bruto = base64.urlsafe_b64decode(corpo["raw"].encode("ascii"))
    msg = message_from_bytes(bruto)
    saida = {}
    for parte in msg.walk():
        nome = parte.get_filename()
        if nome:
            saida[nome] = parte.get_payload(decode=True)
    return saida


class AnexarEUmaCapacidade:
    pass


class TestOAnexoSai:
    def test_arquivo_do_disco_chega_embarcado_na_mensagem(self, correio, tmp_path):
        svc, _trilha = correio
        alvo = tmp_path / "parecer.pdf"
        alvo.write_bytes(b"%PDF-1.7 conteudo do parecer")

        saida = mcp.enviar_email(["a@b.c"], "Assunto", "Corpo", anexos=[str(alvo)])

        assert saida["anexos"] == ["parecer.pdf"]
        embarcados = _anexos_da_caixa(svc.caixa[0])
        assert embarcados["parecer.pdf"] == b"%PDF-1.7 conteudo do parecer"

    def test_varios_anexos_saem_juntos_com_o_tipo_certo(self, correio, tmp_path):
        svc, _trilha = correio
        a = tmp_path / "peca.pdf"
        a.write_bytes(b"%PDF-1.7 x")
        b = _docx(tmp_path / "peca.docx", conforme=True)

        mcp.enviar_email(["a@b.c"], "S", "C", anexos=[str(a), str(b)])

        bruto = base64.urlsafe_b64decode(svc.caixa[0]["raw"].encode("ascii"))
        tipos = {p.get_filename(): p.get_content_type()
                 for p in message_from_bytes(bruto).walk() if p.get_filename()}
        assert tipos["peca.pdf"] == "application/pdf"
        assert tipos["peca.docx"] == (
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document")

    def test_envio_sem_anexo_continua_igual(self, correio):
        svc, _trilha = correio

        saida = mcp.enviar_email(["a@b.c"], "S", "C")

        assert saida["anexos"] == []
        assert _anexos_da_caixa(svc.caixa[0]) == {}


class TestOAnexoForaDoPadraoNaoSai:
    def test_docx_fora_nas_tres_dimensoes_barra_o_envio_inteiro(self, correio, tmp_path):
        svc, trilha = correio
        ruim = _docx(tmp_path / "fora.docx", conforme=False)

        with pytest.raises(ValueError):
            mcp.enviar_email(["a@b.c"], "S", "C", anexos=[str(ruim)])

        assert svc.caixa == []  # nada saiu
        assert any(e["evento"] == "envio_barrado_por_anexo" for e in trilha)

    def test_declaracao_nominal_libera_e_fica_na_trilha(self, correio, tmp_path):
        svc, trilha = correio
        ruim = _docx(tmp_path / "de_terceiro.docx", conforme=False)

        mcp.enviar_email(["a@b.c"], "S", "C", anexos=[str(ruim)],
                         material_de_terceiro=["de_terceiro.docx"])

        assert len(svc.caixa) == 1
        assert any(e["evento"] == "anexo_liberado_por_declaracao" for e in trilha)

    def test_docx_conforme_passa_sem_declaracao(self, correio, tmp_path):
        svc, _trilha = correio
        bom = _docx(tmp_path / "conforme.docx", conforme=True)

        mcp.enviar_email(["a@b.c"], "S", "C", anexos=[str(bom)])

        assert len(svc.caixa) == 1


class TestErroDeChamadaNaoViraEmailMutilado:
    def test_anexo_inexistente_falha_pelo_nome_e_nada_sai(self, correio, tmp_path):
        svc, _trilha = correio
        sumido = tmp_path / "nao_existe.pdf"

        with pytest.raises(ValueError, match="não encontrado"):
            mcp.enviar_email(["a@b.c"], "S", "Segue o parecer em anexo.",
                             anexos=[str(sumido)])

        assert svc.caixa == []

    def test_acima_do_teto_barra_antes_de_montar(self, correio, tmp_path, monkeypatch):
        svc, _trilha = correio
        monkeypatch.setattr(mcp, "TETO_ANEXOS_BYTES", 1024)
        grande = tmp_path / "grande.pdf"
        grande.write_bytes(b"x" * 4096)

        with pytest.raises(ValueError, match="teto"):
            mcp.enviar_email(["a@b.c"], "S", "C", anexos=[str(grande)])

        assert svc.caixa == []

    def test_destinatario_ausente_continua_barrando(self, correio):
        svc, _trilha = correio

        with pytest.raises(ValueError):
            mcp.enviar_email([], "S", "C")

        assert svc.caixa == []


class TestOLedgerDizQualSaiuSemGuardarOQueSaiu:
    def test_registra_nome_tamanho_e_hash(self, correio, tmp_path):
        _svc, trilha = correio
        conteudo = b"%PDF-1.7 documento sigiloso do cliente"
        alvo = tmp_path / "sigiloso.pdf"
        alvo.write_bytes(conteudo)

        mcp.enviar_email(["a@b.c"], "S", "C", anexos=[str(alvo)])

        enviado = [e for e in trilha if e["evento"] == "enviado_por_mcp"][0]
        assert enviado["anexos"] == [{"arquivo": "sigiloso.pdf",
                                      "bytes": len(conteudo),
                                      "sha256": hashlib.sha256(conteudo).hexdigest()}]

    def test_conteudo_do_anexo_nunca_entra_na_trilha(self, correio, tmp_path):
        _svc, trilha = correio
        alvo = tmp_path / "sigiloso.pdf"
        alvo.write_bytes(b"%PDF-1.7 SEGREDO_DO_CLIENTE")

        mcp.enviar_email(["a@b.c"], "S", "C", anexos=[str(alvo)])

        import json
        assert "SEGREDO_DO_CLIENTE" not in json.dumps(trilha, ensure_ascii=False)


class TestOSistemaSabeQuePode:
    """Capacidade que existe e não é anunciada é capacidade que não será usada.

    O agente não lê o código do servidor: ele lê a descrição da ferramenta e a
    skill. Se a implementação anexar e o anúncio não disser, o próximo agente
    volta a responder que não dá para anexar — que foi exatamente o que
    aconteceu na véspera desta mudança.
    """

    def _ferramenta(self, nome):
        return [f for f in mcp.FERRAMENTAS if f["name"] == nome][0]

    def test_o_esquema_anuncia_anexo_e_a_declaracao_nominal(self):
        propriedades = self._ferramenta("enviar_email")["inputSchema"]["properties"]

        assert "anexos" in propriedades
        assert "material_de_terceiro" in propriedades

    def test_a_descricao_diz_que_anexa_e_que_o_gate_barra(self):
        descricao = self._ferramenta("enviar_email")["description"].lower()

        assert "anexo" in descricao
        assert "barra" in descricao

    def test_tudo_que_o_esquema_promete_o_executor_aceita(self):
        """O modo de falha silencioso: o esquema ganha um campo e o lambda o ignora."""
        import inspect

        for ferramenta in mcp.FERRAMENTAS:
            declarados = set(ferramenta["inputSchema"].get("properties") or {})
            executor = mcp.EXECUTORES[ferramenta["name"]]
            fonte = inspect.getsource(executor)
            faltando = [c for c in declarados if f'"{c}"' not in fonte]
            assert not faltando, f"{ferramenta['name']} anuncia e não lê: {faltando}"

    def test_a_skill_da_forja_descreve_a_capacidade(self):
        comandos = (Path(__file__).resolve().parents[1] / ".claude" / "skills" /
                    "forja" / "reference" / "COMANDOS.md")
        texto = comandos.read_text(encoding="utf-8")

        assert "forja-email" in texto
        assert "anexos" in texto
        assert "material_de_terceiro" in texto


class TestAsDuasPortasUsamOMesmoRegistro:
    """Duplicar a lógica garantiria que uma delas registrasse menos que a outra."""

    def test_o_veredito_e_anotado_pela_mesma_funcao(self, correio):
        _svc, trilha = correio
        veredito = {"aprovado": True, "bloqueados": [],
                    "liberadosPorDeclaracao": [{"arquivo": "x.docx"}],
                    "naoInspecionados": ["y.docx: ilegível"]}

        mcp._anotar_veredito(veredito, {"draftId": "d1"})

        eventos = {e["evento"] for e in trilha}
        assert eventos == {"anexo_nao_inspecionado", "anexo_liberado_por_declaracao"}
        assert all(e["draftId"] == "d1" for e in trilha)

    def test_veredito_reprovado_levanta_e_nomeia_os_arquivos(self, correio):
        _svc, trilha = correio
        bloqueado = {"arquivo": "fora.docx", "justificacao": 0.1, "tamanho": 0.0,
                     "fonte": 0.0, "paragrafos": 25}
        veredito = {"aprovado": False, "bloqueados": [bloqueado],
                    "liberadosPorDeclaracao": [], "medidos": [bloqueado],
                    "naoInspecionados": []}

        with pytest.raises(ValueError):
            mcp._anotar_veredito(veredito, {"para": ["a@b.c"]})

        assert trilha[0]["arquivos"] == ["fora.docx"]
