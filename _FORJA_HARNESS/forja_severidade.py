"""Semântica única de severidade para achados da FORJA.

O executor e o CLI precisam decidir bloqueio exatamente do mesmo modo.  Este
módulo mantém a regra pequena e explícita: somente ``p0`` bloqueia; ausência ou
valor desconhecido de severidade é falha fechada e, portanto, ``p0``.
"""

from __future__ import annotations

from typing import Iterable, Mapping


def normalized_severity(finding: Mapping | None) -> str:
    """Retorna ``p0`` ou ``p1``; qualquer valor ausente/desconhecido vira P0."""
    value = str((finding or {}).get("severity") or "").strip().casefold()
    return value if value in {"p0", "p1"} else "p0"


def blocking_findings(findings: Iterable[Mapping] | None) -> list[dict]:
    """Seleciona os achados que impedem a promoção, preservando o laudo."""
    result: list[dict] = []
    for finding in findings or []:
        item = dict(finding) if isinstance(finding, Mapping) else {
            "code": "FORJA-SEVERITY-INVALID",
            "detail": repr(finding),
        }
        item["severity"] = normalized_severity(item)
        if item["severity"] == "p0":
            result.append(item)
    return result
