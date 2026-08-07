"""Regressão da rota Cursor (Grok 4.5) e dos dois postos que ela ocupa.

Nenhum teste aqui chama rede ou o CLI de verdade: o que se protege é o
contrato — registro do modelo, despacho, leitura da saída, mensagem de erro
útil e queda declarada para a reserva. Teste que precisa de login não roda no
baseline, e teste que não roda não protege nada.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

import forja_diabob as fd
import forja_modelos as fm
import forja_triagem_rapida as ft


# --------------------------------------------------------------------------
# Registro e despacho
# --------------------------------------------------------------------------

def test_modelo_no_registro():
    m = fm.MODELOS["grok-4.5-cursor"]
    assert m.provedor == "cursor"
    assert m.familia == "xai"
    assert m.remoto == "cursor-grok-4.5-high"
    assert "F1" in m.fases and "F4" in m.fases and "F7" in m.fases


def test_custo_zero_declarado():
    """Zero porque é mensalidade, não porque é grátis. Centavo estimado mente no ledger."""
    m = fm.MODELOS["grok-4.5-cursor"]
    assert fm.custo_usd(m, 1_000_000, 1_000_000) == 0.0


def test_despacho_conhece_a_rota():
    assert "cursor" in fm.DESPACHO


def test_mesma_familia_da_reserva():
    """Cair para o OpenRouter não pode trocar a família: o contraditório é xAI."""
    assert fm.MODELOS["grok-4.5-cursor"].familia == fm.MODELOS["grok-4.5"].familia


# --------------------------------------------------------------------------
# GPT-5.5 é proibido na FORJA (ordem do titular, 06/08/2026)
# --------------------------------------------------------------------------

@pytest.mark.parametrize("remoto", [
    "gpt-5.5", "GPT-5.5", "openai/gpt-5.5", "openai/gpt-5.5-mini",
    "openai/gpt-5.5-codex", "cx/gpt-5.5", "gpt-5.5-turbo-qualquer-coisa",
])
def test_gpt_55_proibido(remoto):
    assert fm.modelo_remoto_proibido(remoto) is True


@pytest.mark.parametrize("remoto", [
    "openai/gpt-5.6-sol", "openai/gpt-5.6-luna", "gpt-5.6-luna",
    "x-ai/grok-4.5", "grok-4.5", "anthropic/claude-opus-5",
])
def test_o_que_deve_passar_passa(remoto):
    """`grok-4.5` é o falso positivo óbvio de uma regra ingênua sobre '5'."""
    assert fm.modelo_remoto_proibido(remoto) is False


def test_nenhum_5_5_no_registro():
    proibidos = [k for k, v in fm.MODELOS.items()
                 if fm.modelo_remoto_proibido(v.remoto) or fm.modelo_remoto_proibido(v.id)]
    assert proibidos == []


def test_constantes_do_codex_na_forja():
    """A ordem inclui o esforço: `max` não é otimização a negociar."""
    assert fm.CODEX_MODELO_FORJA == "gpt-5.6-luna"
    assert fm.CODEX_ESFORCO_FORJA == "max"
    assert not fm.modelo_remoto_proibido(fm.CODEX_MODELO_FORJA)


def test_chamar_recusa_modelo_proibido(monkeypatch):
    """A trava precisa pegar em `chamar`, não só na função de teste."""
    monkeypatch.setitem(
        fm.MODELOS, "contrabando",
        fm.Modelo(id="contrabando", familia="openai", provedor="openrouter",
                  remoto="openai/gpt-5.5", forte_em=(), fases=("F7",)))
    with pytest.raises(fm.ForjaModeloError, match="vedado por decisão do titular"):
        fm.chamar("contrabando", "oi", registrar=False)


def test_as_duas_proibicoes_ficam_separadas():
    """K2 e GPT-5.5 são decisões distintas, de datas distintas, por motivos distintos.

    Fundi-las num conjunto só quebrou a regressão que documentava o K2 — e teria
    apagado a razão de cada uma. A separação é o registro; a função é a trava.
    """
    assert all("kimi-k2" in x for x in fm.MODELOS_PROIBIDOS)
    assert all("gpt-5.5" in x for x in fm.MODELOS_PROIBIDOS_GPT55)
    assert not (fm.MODELOS_PROIBIDOS & fm.MODELOS_PROIBIDOS_GPT55)


# --------------------------------------------------------------------------
# Localização do binário
# --------------------------------------------------------------------------

def test_binario_respeita_override(tmp_path, monkeypatch):
    falso = tmp_path / "cursor-agent.cmd"
    falso.write_text("@echo off", encoding="utf-8")
    monkeypatch.setenv("FORJA_CURSOR_AGENT", str(falso))
    assert fm._cursor_binario() == falso


def test_binario_reclama_de_override_invalido(tmp_path, monkeypatch):
    monkeypatch.setenv("FORJA_CURSOR_AGENT", str(tmp_path / "nao_existe.cmd"))
    with pytest.raises(fm.ForjaModeloError, match="inexistente"):
        fm._cursor_binario()


# --------------------------------------------------------------------------
# O prompt vai por stdin — o bug que produzia parecer plausível sobre fragmento
# --------------------------------------------------------------------------

def _falso_subprocess(monkeypatch, capturado: dict, saida: str = '{"result":"ok"}'):
    class Proc:
        returncode = 0
        stdout = saida
        stderr = ""

    def falso_run(comando, **kwargs):
        capturado["comando"] = comando
        capturado["kwargs"] = kwargs
        return Proc()

    monkeypatch.setattr(fm.subprocess, "run", falso_run)


def test_prompt_vai_por_stdin_e_nao_por_argumento(monkeypatch):
    """Medido em 07/08/2026: o wrapper `.cmd` passa pelo cmd.exe, que CORTA o
    argumento na primeira quebra de linha.

    O modelo respondia sobre a primeira linha e devolvia texto plausível — o
    Diabob chegou a dizer "você só me nomeou, não há alvo" com o alvo dentro do
    prompt. Erro que não levanta exceção e produz parecer verossímil é o pior
    tipo que existe nesta casa.
    """
    cap: dict = {}
    _falso_subprocess(monkeypatch, cap)
    m = fm.MODELOS["grok-4.5-cursor"]
    fm._cursor(m, "linha 1\nlinha 2\nlinha 3", "persona\ncom quebra", 512, 60)

    enviado = cap["kwargs"]["input"]
    assert "linha 3" in enviado and "persona" in enviado
    # nenhuma parte do prompt pode viajar como argumento de linha de comando
    for pedaco in cap["comando"]:
        assert "linha 2" not in pedaco and "linha 3" not in pedaco


def test_roda_em_pasta_vazia_e_nao_na_pasta_do_caso(monkeypatch):
    """`--trust` é seguro numa pasta vazia dedicada; na pasta do caso não seria."""
    cap: dict = {}
    _falso_subprocess(monkeypatch, cap)
    fm._cursor(fm.MODELOS["grok-4.5-cursor"], "p", None, 512, 60)
    assert Path(cap["kwargs"]["cwd"]) == fm.CURSOR_SANDBOX
    assert "--trust" in cap["comando"]


def test_modo_somente_leitura_e_obrigatorio(monkeypatch):
    """Sem `--mode ask` o agente do Cursor tem escrita e shell."""
    cap: dict = {}
    _falso_subprocess(monkeypatch, cap)
    fm._cursor(fm.MODELOS["grok-4.5-cursor"], "p", None, 512, 60)
    comando = cap["comando"]
    assert "--mode" in comando and comando[comando.index("--mode") + 1] == "ask"


def test_id_remoto_e_o_que_o_cursor_expoe():
    """Conferido em `cursor-agent --list-models`: não existe `grok-4.5` puro lá."""
    assert fm.MODELOS["grok-4.5-cursor"].remoto == "cursor-grok-4.5-high"


# --------------------------------------------------------------------------
# Leitura da saída — o formato do CLI muda entre versões
# --------------------------------------------------------------------------

@pytest.mark.parametrize("bruto,esperado", [
    (json.dumps({"result": "parecer aqui"}), "parecer aqui"),
    (json.dumps({"text": "parecer aqui"}), "parecer aqui"),
    (json.dumps("parecer aqui"), "parecer aqui"),
    ('{"type":"a","text":"linha 1"}\n{"type":"b","text":"linha 2"}', "linha 1\nlinha 2"),
    ("texto puro sem json", "texto puro sem json"),
])
def test_extrai_texto_dos_formatos(bruto, esperado):
    assert fm._cursor_texto(bruto) == esperado


def test_saida_vazia_vira_vazio():
    """`chamar` levanta em conteúdo vazio; devolver o log como parecer seria pior."""
    assert fm._cursor_texto("   ") == ""


# --------------------------------------------------------------------------
# Diabob — rota padrão, reserva e queda declarada
# --------------------------------------------------------------------------

def test_diabob_usa_cursor_por_padrao():
    assert fd.MODELO_PADRAO == "grok-4.5-cursor"
    assert fd.MODELO_RESERVA == "grok-4.5"


def test_diabob_recusa_alvo_vazio():
    with pytest.raises(fm.ForjaModeloError, match="red team de texto vazio"):
        fd.red_team("   ")


def test_diabob_nao_cai_para_rota_paga_sozinho(monkeypatch):
    """Ordem do titular: o Grok roda SEMPRE pela assinatura OAuth do Cursor.

    Cair no OpenRouter em silêncio trocaria a assinatura que ele paga por gasto
    novo que ele não pediu. O padrão é falhar alto com a instrução de conserto.
    """
    chamados = []

    def falso_chamar(modelo_id, prompt, **kwargs):
        chamados.append(modelo_id)
        raise fm.ForjaModeloError("Cursor sem autenticação")

    monkeypatch.setattr(fm, "chamar", falso_chamar)
    with pytest.raises(fm.ForjaModeloError, match="cursor-agent login"):
        fd.red_team("uma análise qualquer")
    assert chamados == [fd.MODELO_PADRAO]  # não tentou a paga


def test_diabob_declara_a_queda_quando_autorizada(monkeypatch):
    """Com autorização explícita a reserva entra — e a queda fica no recibo."""
    chamados = []

    def falso_chamar(modelo_id, prompt, **kwargs):
        chamados.append(modelo_id)
        if modelo_id == fd.MODELO_PADRAO:
            raise fm.ForjaModeloError("Cursor sem autenticação")
        return {"modelo": modelo_id, "familia": "xai", "provedor": "openrouter",
                "conteudo": "objeção", "custoUsd": 0.01, "segundos": 1.0}

    monkeypatch.setattr(fm, "chamar", falso_chamar)
    recibo = fd.red_team("uma análise qualquer", permitir_reserva=True)
    assert chamados == [fd.MODELO_PADRAO, fd.MODELO_RESERVA]
    assert recibo["rotaDegradada"] and "Cursor sem autenticação" in recibo["rotaDegradada"]


def test_triagem_tambem_nao_gasta_sozinha(monkeypatch, tmp_path):
    """A mesma ordem vale para a triagem de F1."""
    monkeypatch.setattr(fm, "chamar", lambda *a, **k: (_ for _ in ()).throw(
        fm.ForjaModeloError("sem login")))
    doc = tmp_path / "d.txt"
    doc.write_text("texto", encoding="utf-8")
    with pytest.raises(fm.ForjaModeloError, match="cursor-agent login"):
        ft.triar_documento(doc)


# --------------------------------------------------------------------------
# Triagem rápida de F1
# --------------------------------------------------------------------------

def test_triagem_nao_chama_modelo_para_arquivo_vazio(tmp_path, monkeypatch):
    """Arquivo sem texto é falha de extração ou de OCR, não trabalho de modelo."""
    monkeypatch.setattr(fm, "chamar", lambda *a, **k: pytest.fail("não devia chamar modelo"))
    vazio = tmp_path / "vazio.txt"
    vazio.write_text("   \n", encoding="utf-8")
    r = ft.triar_documento(vazio)
    assert r["estado"] == "vazio"
    assert "OCR" in r["nota"]


def test_triagem_reconhece_sem_achados(tmp_path, monkeypatch):
    monkeypatch.setattr(fm, "chamar", lambda *a, **k: {
        "modelo": "grok-4.5-cursor", "familia": "xai", "segundos": 1.0,
        "conteudo": "SEM ACHADOS"})
    doc = tmp_path / "d.txt"
    doc.write_text("texto normal de uma peça", encoding="utf-8")
    r = ft.triar_documento(doc)
    assert r["estado"] == "sem_achados" and r["achados"] == []


def test_triagem_declara_truncamento(tmp_path, monkeypatch):
    """O que não foi lido precisa aparecer: silêncio sobre corte vira cobertura falsa."""
    monkeypatch.setattr(fm, "chamar", lambda *a, **k: {
        "modelo": "grok-4.5-cursor", "familia": "xai", "segundos": 1.0,
        "conteudo": "[X] | trecho | motivo | conferir"})
    doc = tmp_path / "grande.txt"
    doc.write_text("a" * (ft.LIMITE_CARACTERES + 500), encoding="utf-8")
    r = ft.triar_documento(doc)
    assert r["textoTruncado"] is True
    assert r["caracteresLidos"] == ft.LIMITE_CARACTERES
    assert r["caracteresTotais"] == ft.LIMITE_CARACTERES + 500


def test_laudo_declara_que_nao_e_gate(tmp_path, monkeypatch):
    """A natureza precisa viajar junto com o artefato, senão vira gate por hábito."""
    monkeypatch.setattr(fm, "chamar", lambda *a, **k: {
        "modelo": "grok-4.5-cursor", "familia": "xai", "segundos": 1.0,
        "conteudo": "SEM ACHADOS"})
    doc = tmp_path / "d.txt"
    doc.write_text("texto", encoding="utf-8")
    laudo = ft.triar([doc])
    assert laudo["contrato"] == "FORJA-F1-TRIAGEM-RAPIDA-v1"
    assert "nao e gate" in laudo["natureza"].casefold()
    assert "nao substitui forja_injection_scan.py" in laudo["natureza"].casefold()


def test_triagem_isola_falha_de_um_documento(tmp_path, monkeypatch):
    """Um documento que falha não pode derrubar a triagem dos outros."""
    def falso(modelo_id, prompt, **kwargs):
        if "quebra" in prompt:
            raise fm.ForjaModeloError("modelo fora do ar")
        return {"modelo": "grok-4.5-cursor", "familia": "xai", "segundos": 1.0,
                "conteudo": "SEM ACHADOS"}

    monkeypatch.setattr(fm, "chamar", falso)
    bom = tmp_path / "bom.txt"; bom.write_text("texto normal", encoding="utf-8")
    ruim = tmp_path / "ruim.txt"; ruim.write_text("isto quebra", encoding="utf-8")
    laudo = ft.triar([bom, ruim])
    assert laudo["documentos"] == 2 and laudo["falharam"] == 1


# --------------------------------------------------------------------------
# Gate do conselho — o Diabob obrigatório vira verificação, não promessa
# --------------------------------------------------------------------------

def _recibo(**troca) -> dict:
    base = {"contrato": "FORJA-F4-PARECER-DIABOB-v1", "persona": "diabob",
            "modelo": "grok-4.5-cursor", "familia": "xai", "provedor": "cursor",
            "rotaDegradada": None, "parecer": "objeção fundamentada. " * 60}
    base.update(troca)
    return base


def _gate(tmp_path, dados=None, nome="F4_PARECER_DIABOB.json", texto=None):
    from forja_conselho import validar_conselho
    caminho = None
    if texto is not None:
        caminho = tmp_path / nome
        caminho.write_text(texto, encoding="utf-8")
    elif dados is not None:
        caminho = tmp_path / nome
        caminho.write_text(json.dumps(dados, ensure_ascii=False), encoding="utf-8")
    laudo = validar_conselho(helena=None, cicero=None, decisoes=None, diabob=caminho)
    return laudo["gates"]["diabob_present"], laudo["findings"]


def test_gate_aprova_recibo_real(tmp_path):
    veredito, _ = _gate(tmp_path, _recibo())
    assert veredito == "pass"


def test_gate_nao_declarado_fica_unknown_e_nao_pass(tmp_path):
    """`unknown` é a recusa de atestar o que não se viu — e não reprova caso antigo."""
    veredito, achados = _gate(tmp_path)
    assert veredito == "unknown"
    assert any(a["gate"] == "LC4-Diabob" and a["sev"] == "P1" for a in achados)


def test_gate_reprova_prosa_dizendo_que_passou(tmp_path):
    """"Passou pelo Diabob" escrito à mão é exatamente o que não prova nada."""
    veredito, _ = _gate(tmp_path, texto="Passou pelo Diabob. Tudo certo.",
                        nome="F4_PARECER_DIABOB.md")
    assert veredito == "fail"


def test_gate_reprova_eco_da_mesma_familia(tmp_path):
    """Lição 99: red team pelo mesmo modelo repete os pontos cegos com voz mais dura."""
    veredito, achados = _gate(tmp_path, _recibo(familia="anthropic"))
    assert veredito == "fail"
    assert any("MESMA família" in a["problema"] for a in achados)


def test_gate_reprova_casca_sem_parecer(tmp_path):
    veredito, _ = _gate(tmp_path, _recibo(parecer="ok"))
    assert veredito == "fail"


def test_gate_avisa_rota_degradada_sem_reprovar(tmp_path):
    """Rodar pela rota paga não invalida o contraditório — mas não passa calado."""
    veredito, achados = _gate(tmp_path, _recibo(rotaDegradada="cursor caiu"))
    assert veredito == "pass"
    assert any(a["sev"] == "P1" and "degradada" in a["problema"] for a in achados)


def test_assinatura_antiga_do_validador_continua_funcionando(tmp_path):
    """Chamador que não conhece o Diabob não pode quebrar — só fica sem veredito."""
    from forja_conselho import validar_conselho
    laudo = validar_conselho(helena=None, cicero=None, decisoes=None)
    assert laudo["gates"]["diabob_present"] == "unknown"
    assert {"helena_present", "cicero_present",
            "council_decisions_recorded"} <= set(laudo["gates"])


# --------------------------------------------------------------------------
# Complementaridade — a razão de a triagem existir
# --------------------------------------------------------------------------

def test_scanner_lexical_nao_le_texto_extraido():
    """Os dois não veem o mesmo substrato, e é por isso que os dois rodam.

    `forja_injection_scan.py` examina o PDF atrás de texto escondido — fonte
    minúscula, branco sobre branco. Ele nem aceita .txt como entrada. A triagem
    semântica examina o texto JÁ extraído, atrás de sentido. Se um dia este
    teste falhar porque o scanner passou a aceitar texto, a complementaridade
    precisa ser reavaliada, não presumida.
    """
    origem = Path(__file__).with_name("forja_injection_scan.py").read_text(
        encoding="utf-8", errors="replace")
    assert "não é PDF ou pasta" in origem or "nao e PDF ou pasta" in origem
