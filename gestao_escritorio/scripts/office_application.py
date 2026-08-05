"""Regras de aplicação do painel, independentes do transporte HTTP e do disco."""

from __future__ import annotations


def completion_blockers(item: dict) -> list[str]:
    """Explica por que uma demanda ainda não pode ser marcada como cumprida."""
    blockers: list[str] = []
    attachments = item.get("anexos") or {}
    if attachments.get("externosPendentes"):
        blockers.append("há anexos ou mídias externas ainda pendentes")
    expected = attachments.get("diretosEsperados")
    downloaded = attachments.get("diretosBaixados")
    if isinstance(expected, int) and isinstance(downloaded, int) and downloaded < expected:
        blockers.append(f"foram materializados apenas {downloaded} de {expected} anexos diretos")
    stage = str(item.get("etapaOperacional") or "").strip().lower()
    if stage in {"insumos_parciais", "entregue_para_revisao", "bloqueada"}:
        blockers.append(f"a etapa operacional ainda é {stage}")
    return blockers
