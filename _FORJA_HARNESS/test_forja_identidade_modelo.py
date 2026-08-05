# -*- coding: utf-8 -*-
"""
test_forja_identidade_modelo.py — Regressão das duas falhas de captura de modelo.

Âncora: bancada Cafelana V7, 27/07/2026. Nenhuma das duas era falha de modelo, e
as duas produziam artefato com proveniência falsa ou texto mutilado.

**Apelido não é modelo.** `--model opus` resolveu para `claude-opus-4-8` e
`--model opusplan` para `claude-sonnet-4-6`. O `forja_headless.py` pedia por
apelido e não conferia o envelope: toda fase headless vinha rodando em Opus 4.8
sem que nada acusasse. Apelido é conveniência de sessão interativa — o Claude
Code pode remapeá-lo a cada release, e remapeou.

**`--output-format json` devolve só o último turno.** Peça longa atravessa mais
de um turno; 36 mil tokens de saída voltaram como 10 KB começando no meio de uma
palavra. O contrato de F7-B então reprovava por "texto fora do contrato",
culpando o modelo por um defeito de captura.

Uso: pytest test_forja_identidade_modelo.py
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

import forja_editorial
import forja_editorial_model
import forja_headless

FORJA = Path(__file__).resolve().parent

# Id canônico tem família e versão no nome. Apelido, não.
_CANONICO = re.compile(r"^(?:claude-[a-z]+-\d+(?:-\d+)?|gpt-[\d.]+-[a-z]+|"
                       r"x-ai/[\w.-]+|openai/[\w.-]+|moonshotai/[\w.-]+)$")
APELIDOS_PROIBIDOS = {"opus", "sonnet", "haiku", "fable", "opusplan", "default"}


def test_cli_model_devolve_id_canonico():
    """O que vai para `--model` é sempre o id canônico."""
    for canonical_id, modelo in forja_editorial_model.EDITORIAL_MODELS.items():
        assert modelo.cli_model == canonical_id
        assert modelo.cli_model not in APELIDOS_PROIBIDOS
        assert _CANONICO.match(modelo.cli_model), f"{canonical_id} não parece id canônico"


def test_apelido_continua_existindo_mas_nao_vai_ao_cli():
    """O apelido segue como rótulo de leitura — o teste garante que ele não vaze."""
    opus = forja_editorial_model.EDITORIAL_MODELS["claude-opus-5"]
    assert opus.alias == "opus"          # rótulo de conveniência preservado
    assert opus.cli_model != opus.alias  # e que não é o que se pede ao executor


def test_headless_pede_modelo_por_id_canonico():
    assert forja_headless.MODELO not in APELIDOS_PROIBIDOS
    assert _CANONICO.match(forja_headless.MODELO)


def test_nenhum_modulo_de_producao_passa_apelido_ao_cli():
    """Varredura de código: `--model` seguido de apelido é bloqueio.

    A varredura existe porque o defeito não estava numa função, e sim numa
    constante distraída. Revisão de diff não pega isso; teste pega.
    """
    padrao = re.compile(r'--model["\']?\s*,\s*["\']([a-z][\w.-]*)["\']')
    ofensores = []
    for caminho in FORJA.glob("forja_*.py"):
        for achado in padrao.finditer(caminho.read_text(encoding="utf-8", errors="replace")):
            if achado.group(1) in APELIDOS_PROIBIDOS:
                ofensores.append(f"{caminho.name}: {achado.group(1)}")
    assert not ofensores, f"apelido passado ao CLI: {ofensores}"


def test_headless_falha_alto_quando_o_envelope_diverge():
    envelope = {"modelUsage": {"claude-opus-4-8": {"inputTokens": 10}}}
    with pytest.raises(SystemExit) as erro:
        forja_headless._confirmar_modelo(envelope, "F7_AUDITORIA_JURIDICA_FACTUAL")
    assert "divergente" in str(erro.value)
    assert forja_headless.MODELO in str(erro.value)


def test_headless_aceita_o_modelo_pedido():
    forja_headless._confirmar_modelo({"modelUsage": {forja_headless.MODELO: {}}}, "F1")


def test_headless_nao_afirma_nada_sem_telemetria():
    """Envelope sem `modelUsage` não prova divergência — e também não prova acerto."""
    forja_headless._confirmar_modelo({}, "F1")


def test_stream_recompoe_todos_os_turnos_na_ordem():
    linhas = [
        {"type": "assistant", "message": {"content": [{"type": "text", "text": "primeiro "}]}},
        {"type": "assistant", "message": {"content": [{"type": "thinking", "thinking": "ignorar"},
                                                      {"type": "text", "text": "segundo "}]}},
        {"type": "assistant", "message": {"content": [{"type": "text", "text": "terceiro"}]}},
        {"type": "result", "is_error": False, "session_id": "s-1",
         "modelUsage": {"claude-opus-5": {"outputTokens": 9}}},
    ]
    envelope = forja_editorial._recompor_stream(
        "\n".join(json.dumps(linha, ensure_ascii=False) for linha in linhas))
    assert envelope["result"] == "primeiro segundo terceiro"
    assert envelope["turnosAssistente"] == 3
    assert envelope["session_id"] == "s-1"
    assert "claude-opus-5" in envelope["modelUsage"]


def test_stream_de_turno_unico_continua_funcionando():
    """O caso comum não pode ter regredido para consertar o caso raro."""
    linhas = [
        {"type": "assistant", "message": {"content": [{"type": "text", "text": "texto único"}]}},
        {"type": "result", "is_error": False, "session_id": "s-2", "modelUsage": {}},
    ]
    envelope = forja_editorial._recompor_stream(
        "\n".join(json.dumps(linha) for linha in linhas))
    assert envelope["result"] == "texto único"
    assert envelope["turnosAssistente"] == 1


def test_stream_preserva_o_erro_do_executor():
    linhas = [{"type": "result", "is_error": True, "result": "limite atingido"}]
    envelope = forja_editorial._recompor_stream(json.dumps(linhas[0]))
    assert envelope["is_error"] is True
    assert envelope["result"] == "limite atingido"


def test_stream_recusa_saida_que_nao_e_ndjson():
    with pytest.raises(forja_editorial.ForjaN3Error):
        forja_editorial._recompor_stream("isto não é json\nnem isto")


def test_stream_ignora_ruido_de_hook_entre_os_eventos():
    """O executor intercala eventos de hook; eles não podem virar texto da peça."""
    linhas = [
        {"type": "system", "subtype": "hook", "output": "ruído"},
        {"type": "assistant", "message": {"content": [{"type": "text", "text": "peça"}]}},
        {"type": "rate_limit_event", "rate_limit_info": {}},
        {"type": "result", "is_error": False},
    ]
    envelope = forja_editorial._recompor_stream(
        "\n".join(json.dumps(linha) for linha in linhas))
    assert envelope["result"] == "peça"
