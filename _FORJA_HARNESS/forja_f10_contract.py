# -*- coding: utf-8 -*-
"""Recomputo independente dos gates finais da F10.

O contrato F10 declarava três gates que, até aqui, eram satisfeitos apenas por
um ``PHASE_RESULT`` escrito pelo produtor. Este módulo é a autoridade pequena
da rota de fechamento: recebe manifesto, evidência e estado já materializados
e devolve somente os três veredictos que podem ser reproduzidos.

Ele não confirma o conteúdo jurídico da entrega nem inventa prova de envio.
Confere apenas identidade externa, vínculo criptográfico do pacote e a
sincronização de gestão exigida antes de marcar o caso como cumprido.
"""

from __future__ import annotations

from pathlib import Path

from forja_n3_common import sha256_file


REQUIRED_F10_GATES = (
    "external_identifier_valid",
    "package_hash_matches",
    "management_synced",
)


def _pass(ok: bool) -> str:
    return "pass" if ok else "fail"


def _external_identifier_valid(evidence: dict) -> bool:
    """Aceita ID externo ou evidência local íntegra; nunca mera presença."""
    if str(evidence.get("externalId") or evidence.get("external_id") or "").strip():
        return True
    path = Path(str(evidence.get("path") or ""))
    declared = str(evidence.get("sha256") or "").strip().lower()
    if not path.is_file() or not declared:
        return False
    try:
        return sha256_file(path).lower() == declared
    except OSError:
        return False


def _management_synced(state: dict, *, minimum_event_seq: int) -> bool:
    sync = state.get("sync") or {}
    try:
        synced = int(sync.get("lastSyncedEventSeq") or 0)
    except (TypeError, ValueError):
        synced = 0
    return sync.get("status") == "ok" and synced >= minimum_event_seq


def compute_f10_gates(
    package_manifest: dict,
    evidence: dict,
    state: dict,
    *,
    minimum_synced_event_seq: int | None = None,
) -> dict[str, str]:
    """Recomputa os gates F10 contra os insumos finais.

    ``minimum_synced_event_seq`` é explícito na rota de fechamento porque o
    evento de sincronização antecede o evento de cumprimento em uma revisão.
    Quando omitido, usa a mesma fronteira segura da rota canônica.
    """
    if minimum_synced_event_seq is None:
        try:
            minimum_synced_event_seq = max(0, int(state.get("revision") or 0) - 1)
        except (TypeError, ValueError):
            minimum_synced_event_seq = 0
    try:
        minimum_synced_event_seq = int(minimum_synced_event_seq)
    except (TypeError, ValueError):
        minimum_synced_event_seq = 0

    expected_hash = str(package_manifest.get("packageHash") or "").strip()
    received_hash = str(evidence.get("packageHash") or "").strip()
    return {
        "external_identifier_valid": _pass(_external_identifier_valid(evidence)),
        "package_hash_matches": _pass(bool(expected_hash and expected_hash == received_hash)),
        "management_synced": _pass(
            _management_synced(state, minimum_event_seq=minimum_synced_event_seq)
        ),
    }


def validate_f10_gates(gates: dict | None) -> dict:
    """Valida presença e veredicto dos gates, sem aceitar omissão silenciosa."""
    findings = []
    values = gates if isinstance(gates, dict) else {}
    for name in REQUIRED_F10_GATES:
        if values.get(name) != "pass":
            findings.append(f"{name} não passou na recomputação F10")
    return {"approved": not findings, "findings": findings}


__all__ = ["REQUIRED_F10_GATES", "compute_f10_gates", "validate_f10_gates"]
