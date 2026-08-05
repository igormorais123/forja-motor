# -*- coding: utf-8 -*-
"""Vocabulário do modelo editorial da subfase F7-B (emenda E14, passos M1 a M5).

O que tinha valor no arranjo anterior não era o nome do modelo: era a recusa em
aceitar a autodeclaração dele. O orquestrador confere no envelope quem executou,
em vez de acreditar no relatório. Isso permanece intacto — o que muda é que o
modelo autorizado passa a vir de uma allowlist e do contrato do run, não de uma
constante literal cravada em duas comparações.

Determinação de 25/07/2026 do titular do projeto, que supera a de 15/07/2026:
o Opus 5 substitui o Fable 5 na escrita final, e a revisão entre famílias
distintas de modelo passa a ser exigência de produção, não critério de pesquisa.
"""

from __future__ import annotations

from dataclasses import dataclass

from forja_n3_common import ForjaN3Error


@dataclass(frozen=True)
class EditorialModel:
    """Modelo habilitado a participar da subfase editorial."""

    canonical_id: str
    family: str
    alias: str | None = None  # rótulo curto de conveniência; NUNCA vai para o CLI

    @property
    def can_execute(self) -> bool:
        return self.alias is not None

    @property
    def cli_model(self) -> str:
        """O que se passa em `--model`: sempre o id canônico, nunca o apelido.

        A bancada de 27/07/2026 mediu isto: `--model opus` resolve para
        `claude-opus-4-8` nesta instalação, e `--model opusplan` para
        `claude-sonnet-4-6`. Apelido é conveniência de sessão interativa —
        o Claude Code é livre para remapeá-lo a cada release, e remapeou.
        Em execução auditável, pedir por apelido é pedir "o melhor que houver",
        que é exatamente o que um contrato de fase não pode dizer.
        """
        return self.canonical_id


# Allowlist. `alias` preenchido significa que a FORJA sabe invocá-lo por conta
# própria; sem alias, o modelo só é reconhecido como revisor declarado, operado
# fora daqui. Reconhecer não é o mesmo que saber executar, e o código não finge
# capacidade que não tem.
EDITORIAL_MODELS: dict[str, EditorialModel] = {
    "claude-opus-5": EditorialModel("claude-opus-5", "claude", "opus"),
    "claude-fable-5": EditorialModel("claude-fable-5", "claude", "fable"),
    "gpt-5.6-sol": EditorialModel("gpt-5.6-sol", "openai"),
}

DEFAULT_EDITORIAL_MODEL = "claude-opus-5"

# Enum já aprovado no ciclo AUTO-RESEARCH (decisão R2 da revisão adversarial de
# 24/07/2026), aqui promovido de critério de avaliação a gate de produção.
CROSS_FAMILY = "cross_family"
SAME_FAMILY = "cross_session_same_family"
UNVERIFIED = "unverified"
FAMILY_ASSURANCE_LEVELS = (CROSS_FAMILY, SAME_FAMILY, UNVERIFIED)


def resolve(canonical_id: str | None = None) -> EditorialModel:
    """Resolve o modelo editorial pelo id canônico, exigindo allowlist."""
    wanted = str(canonical_id or DEFAULT_EDITORIAL_MODEL).strip().casefold()
    model = EDITORIAL_MODELS.get(wanted)
    if model is None:
        autorizados = ", ".join(sorted(EDITORIAL_MODELS))
        raise ForjaN3Error(
            f"modelo editorial não autorizado: {canonical_id!r}; a allowlist contém {autorizados}"
        )
    return model


def resolve_executable(canonical_id: str | None = None) -> EditorialModel:
    """Idem, recusando modelo que esta instalação não sabe invocar."""
    model = resolve(canonical_id)
    if not model.can_execute:
        raise ForjaN3Error(
            f"a FORJA reconhece {model.canonical_id} como revisor, mas não possui executor "
            "próprio para ele; conduza a revisão fora do harness e declare-a no contrato do run"
        )
    return model


def is_authorized(canonical_id: str | None) -> bool:
    return str(canonical_id or "").strip().casefold() in EDITORIAL_MODELS


def family_of(canonical_id: str | None) -> str | None:
    model = EDITORIAL_MODELS.get(str(canonical_id or "").strip().casefold())
    return model.family if model else None


def family_assurance(
    producer_id: str | None,
    reviewer_id: str | None,
    *,
    producer_session: str | None = None,
    reviewer_session: str | None = None,
) -> str:
    """Classifica a independência entre quem escreveu e quem revisou.

    Sem revisor identificado, ou com revisor fora da allowlist, o resultado é
    `unverified` — que não libera entrega em modo algum. A degradação para
    `cross_session_same_family` é legítima quando a segunda família está
    indisponível, desde que fique registrada; jamais é silenciosa.
    """
    producer_family = family_of(producer_id)
    reviewer_family = family_of(reviewer_id)
    if not producer_family or not reviewer_family:
        return UNVERIFIED
    if producer_family != reviewer_family:
        return CROSS_FAMILY
    sessions = (str(producer_session or "").strip(), str(reviewer_session or "").strip())
    if all(sessions) and sessions[0] != sessions[1]:
        return SAME_FAMILY
    return UNVERIFIED


def describe(canonical_id: str | None, session_id: str | None = None) -> dict:
    """Ficha do modelo para o contrato do run (passo M4)."""
    model = resolve(canonical_id)
    return {
        "canonicalId": model.canonical_id,
        "family": model.family,
        "sessionId": str(session_id).strip() if str(session_id or "").strip() else None,
    }
