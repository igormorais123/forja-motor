# -*- coding: utf-8 -*-
"""Regressão do perfil privado de escrita e das portas que o aplicam."""

from __future__ import annotations

import pytest

import forja_estilo_casa as casa
import forja_mcp_email as mcp
from forja_email import _validar_corpo_email
from forja_entrega import GATE_EMAIL_ESTILO, validar_pacote
from forja_estilo_humano import (
    analisar,
    mandatory_prompt_for_channel,
    mandatory_prompt_for_phase,
    relatorio,
)


EMAIL_CONFORME = (
    "Dra. Ana,\n\n"
    "Revisei a minuta e ajustei o pedido da página 9 porque a decisão exige "
    "a delimitação expressa do prazo. A versão em Word e o PDF seguem anexos.\n\n"
    "Peço que confirme a data da intimação; com isso, fecho o pacote hoje."
)

MENSAGEM_CONFORME = (
    "O ponto está resolvido. Revisei a decisão e o prazo termina amanhã. "
    "Por isso, peço que confirme hoje; depois disso, fecho a versão."
)

EMAIL_SEM_METODO = (
    "Apresento algumas considerações gerais acerca do trabalho realizado e do "
    "contexto existente. O tema possui diferentes aspectos que podem ser vistos "
    "sob variadas perspectivas e merece atenção cuidadosa por todos os envolvidos. "
    "Há muitos elementos relevantes no cenário e eles podem ser analisados de "
    "formas diversas conforme a situação. O assunto continua aberto e comporta "
    "reflexões adicionais em momento oportuno."
)


@pytest.fixture
def perfil_teste(monkeypatch):
    """Perfil sintético: a regressão do motor não depende do acervo privado."""
    perfil = {
        "schema": casa.PROFILE_SCHEMA,
        "profileVersion": "test.house.1",
        "coreMethod": [
            "Apresente cedo a questão dominante, o resultado ou a decisão necessária.",
            "Separe confirmado, condicional e ainda não verificado.",
            "Ligue a análise à consequência concreta e feche com a providência.",
        ],
        "representationLimits": [
            "Não represente pessoa real nem invente opinião, fato ou mandato.",
            "Não copie conteúdo privado de corpus.",
        ],
        "forbiddenPersonificationPatterns": [r"\bescrevo\s+como\s+a\s+pessoa\s+real\b"],
        "caricature": {"terms": ["brilhante", "fantástico", "espetáculo"], "maxTotal": 1},
        "channels": {
            "email": {
                "minimumScore": 72, "blockingScore": 48,
                "minimumWordsForStructure": 35, "openingWindowWords": 55,
                "sentenceMedianGuidance": [16, 22],
                "generationRules": ["Abra com entrega ou decisão e feche com próximo passo."],
                "markers": {
                    "directOpening": ["segue", "revisei", "peço", "a questão"],
                    "grounding": ["documento", "anexo", "página", "decisão", "prazo", "se "],
                    "consequence": ["porque", "por isso", "prazo", "com isso"],
                    "nextAction": ["peço", "confirme", "segue", "fecho"],
                },
            },
            "mensagem": {
                "minimumScore": 68, "blockingScore": 45,
                "minimumWordsForStructure": 22, "openingWindowWords": 35,
                "sentenceMedianGuidance": [6, 10],
                "generationRules": ["Dê a conclusão na primeira rajada."],
                "markers": {
                    "directOpening": ["o ponto", "revisei", "peço", "vamos"],
                    "grounding": ["documento", "decisão", "prazo", "se "],
                    "consequence": ["porque", "por isso", "prazo", "com isso"],
                    "nextAction": ["peço", "confirme", "vamos", "fecho"],
                },
            },
        },
    }
    monkeypatch.setattr(casa, "carregar_perfil", lambda **_kwargs: perfil)
    return perfil


def test_perfil_privado_esta_ativo_e_rastreado():
    perfil = casa.carregar_perfil()
    if perfil is None:
        pytest.skip("acervo privado não montado neste checkout do motor")

    assert perfil["profileVersion"] == "2026-08-15.fmo-derived.1"
    assert perfil["methodologicalBoundary"].find("AUC 0,457") >= 0
    assert len(perfil["provenance"]["sources"]) >= 5


def test_prompt_f9_e_canal_recebem_o_metodo_sem_copiar_corpus(perfil_teste):
    f9 = mandatory_prompt_for_phase("F9_PACOTE_REVISAO_DRAFT_OPCIONAL")
    mensagem = mandatory_prompt_for_channel("mensagem")

    assert "test.house.1" in f9
    assert "questão dominante" in f9
    assert "Regras específicas do canal mensagem" in mensagem
    assert "não prova autoria" in f9.lower()


def test_email_e_mensagem_conformes_passam_com_dimensoes_explicitas(perfil_teste):
    email = casa.analisar(EMAIL_CONFORME, "email")
    mensagem = casa.analisar(MENSAGEM_CONFORME, "mensagem")

    assert email["approved"] and email["score"] >= 72
    assert mensagem["approved"] and mensagem["score"] >= 68
    assert set(email["dimensions"]) == {
        "directOpening", "groundingOrCalibration", "consequence",
        "nextAction", "channelCadence",
    }


def test_texto_generico_longo_reprova_por_estrutura_e_nao_por_autoria(perfil_teste):
    resultado = casa.analisar(EMAIL_SEM_METODO, "email")

    assert not resultado["approved"]
    assert any(x["gate"].endswith("aderencia-estrutural") and x["sev"] == "P0"
               for x in resultado["findings"])
    assert "autoria" in resultado["method"]


@pytest.mark.parametrize("texto,regra", [
    ("Escrevo como a pessoa real para dizer que segue o documento.", "personificacao"),
    ("Ficou brilhante, fantástico e um espetáculo. Segue.", "caricatura"),
])
def test_personificacao_e_caricatura_sao_bloqueadores(texto, regra, perfil_teste):
    p0 = [x for x in analisar(texto, "mensagem") if x["sev"] == "P0"]

    assert any(regra in x["gate"] for x in p0), p0


def test_relatorio_expoe_versao_hash_e_limite_metodologico(perfil_teste):
    resultado = relatorio(EMAIL_CONFORME, "email")

    assert resultado["aprovado"]
    assert resultado["houseStyle"]["profileVersion"] == "test.house.1"
    assert len(resultado["houseStyle"]["profileSha256"]) == 64
    assert "não estima autoria" in resultado["metodo"]


def test_perfil_ausente_nao_inventa_autoria(monkeypatch):
    monkeypatch.setattr(casa, "_caminho_perfil", lambda: None)

    resultado = casa.analisar(EMAIL_CONFORME, "email")
    assert resultado["status"] == "not_configured"
    assert resultado["approved"]
    assert "autoria" in resultado["method"]


def test_criacao_de_email_barra_corpo_antes_da_api(perfil_teste):
    with pytest.raises(ValueError, match="padrão da casa"):
        _validar_corpo_email(EMAIL_SEM_METODO)


def test_mcp_barra_corpo_antes_de_abrir_o_gmail(monkeypatch, perfil_teste):
    abriu = []
    monkeypatch.setattr(mcp, "_servico", lambda: abriu.append(True))

    with pytest.raises(ValueError, match="padrão da casa"):
        mcp.enviar_email(["destinatario@example.test"], "Assunto", EMAIL_SEM_METODO)
    assert abriu == []


def test_pacote_extrai_corpo_do_json_e_recomputa_o_gate(perfil_teste):
    pacote = {"deliverables": [{"id": "minuta", "releasePolicy": "internal_review_only"}]}
    resposta = validar_pacote(pacote, {"subject": "Assunto", "body": EMAIL_SEM_METODO})

    assert resposta["gates"][GATE_EMAIL_ESTILO] == "fail"
    assert any(x["gate"].startswith("G11-padrao-casa/") for x in resposta["findings"])
