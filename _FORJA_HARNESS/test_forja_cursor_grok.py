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
    assert m.remoto == "grok-4.5"
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


def test_diabob_declara_a_queda(monkeypatch):
    """Degradar é permitido; degradar em silêncio troca assinatura por gasto sem ninguém ver."""
    chamados = []

    def falso_chamar(modelo_id, prompt, **kwargs):
        chamados.append(modelo_id)
        if modelo_id == fd.MODELO_PADRAO:
            raise fm.ForjaModeloError("Cursor sem autenticação")
        return {"modelo": modelo_id, "familia": "xai", "provedor": "openrouter",
                "conteudo": "objeção", "custoUsd": 0.01, "segundos": 1.0}

    monkeypatch.setattr(fm, "chamar", falso_chamar)
    recibo = fd.red_team("uma análise qualquer")
    assert chamados == [fd.MODELO_PADRAO, fd.MODELO_RESERVA]
    assert recibo["rotaDegradada"] and "Cursor sem autenticação" in recibo["rotaDegradada"]


def test_diabob_sem_reserva_propaga(monkeypatch):
    monkeypatch.setattr(fm, "chamar", lambda *a, **k: (_ for _ in ()).throw(
        fm.ForjaModeloError("sem login")))
    with pytest.raises(fm.ForjaModeloError, match="sem login"):
        fd.red_team("análise", permitir_reserva=False)


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
