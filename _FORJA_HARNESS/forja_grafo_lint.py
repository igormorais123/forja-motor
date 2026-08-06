"""Lint estrutural independente do grafo de raciocínio F3 (PRD 45, R3/R4)."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Mapping

from forja_reasoning import validate_graph


PROPOSED_ONTOLOGY = {
    "document", "official_source", "fact", "event", "rule", "thesis",
    "request", "decision", "inference", "gap",
}
LEGACY_ONTOLOGY = {"source", "official_fact", "strategy", "coverage", "calculation"}
ALL_ONTOLOGY = PROPOSED_ONTOLOGY | LEGACY_ONTOLOGY
SOURCE_TYPES = {"document", "source", "official_source", "official_fact"}
SUPPORT_RELATIONS = {"supports", "justifies"}
RESTRICTIVE_RELATIONS = {"limits", "qualifies", "contradicts", "ignored_by"}


def _finding(code: str, detail: str, *, severity: str = "p2") -> dict:
    return {"code": code, "severity": severity, "detail": detail}


def lint_graph(payload: Mapping | None) -> dict:
    if not isinstance(payload, Mapping):
        return {"findings": [_finding("GRAFO-00", "grafo ausente ou inválido", severity="p0")], "metrics": {}}
    nodes = [node for node in payload.get("nodes") or [] if isinstance(node, Mapping)]
    edges = [edge for edge in payload.get("edges") or [] if isinstance(edge, Mapping)]
    node_by_id = {str(node.get("id")): node for node in nodes}
    incoming: dict[str, list[Mapping]] = defaultdict(list)
    outgoing: dict[str, list[Mapping]] = defaultdict(list)
    for edge in edges:
        incoming[str(edge.get("to") or "")].append(edge)
        outgoing[str(edge.get("from") or "")].append(edge)
    findings: list[dict] = []
    findings.extend(_finding("GRAFO-00", f"{item.get('code')}: {item.get('detail')}", severity="p0") for item in validate_graph(dict(payload)))
    thesis = [node for node in nodes if node.get("type") == "thesis"]
    for node in thesis:
        node_id = str(node.get("id") or "?")
        supporting = [edge for edge in incoming[node_id] if edge.get("relation") in SUPPORT_RELATIONS]
        if not supporting:
            findings.append(_finding("GRAFO-01", f"tese sem entrada supports/justifies: {node_id}"))
    for node in nodes:
        node_id = str(node.get("id") or "?")
        if node.get("type") in SOURCE_TYPES and not incoming[node_id] and not outgoing[node_id]:
            findings.append(_finding("GRAFO-02", f"nó de fonte isolado: {node_id}"))
    for node in nodes:
        if node.get("type") != "request":
            continue
        node_id = str(node.get("id") or "?")
        if not any(edge.get("relation") == "justifies" and node_by_id.get(str(edge.get("from")), {}).get("type") == "thesis" for edge in incoming[node_id]):
            findings.append(_finding("GRAFO-03", f"pedido sem tese justificadora: {node_id}"))
    for node in thesis:
        node_id = str(node.get("id") or "?")
        incoming_edges = incoming[node_id]
        if incoming_edges and all(edge.get("relation") in RESTRICTIVE_RELATIONS for edge in incoming_edges):
            findings.append(_finding("GRAFO-04", f"tese só recebe entradas restritivas: {node_id}"))
    type_counts = Counter(str(node.get("type") or "") for node in nodes)
    for node_type, count in sorted(type_counts.items()):
        if node_type not in ALL_ONTOLOGY:
            findings.append(_finding("GRAFO-05", f"tipo fora da ontologia: {node_type} ({count} nó(s))"))
        elif node_type in LEGACY_ONTOLOGY:
            findings.append(_finding("GRAFO-05", f"tipo legado requer proveniência: {node_type} ({count} nó(s))"))
    possible = max(len(nodes) * max(len(nodes) - 1, 1), 1)
    density = round(len(edges) / possible, 6)
    findings.append(_finding("GRAFO-06", f"densidade informativa: {density}", severity="p2"))
    metrics = {
        "nodes": len(nodes),
        "edges": len(edges),
        "theses": len(thesis),
        "thesesWithoutSupport": sum(
            not any(edge.get("relation") in SUPPORT_RELATIONS for edge in incoming[str(node.get("id") or "")])
            for node in thesis
        ),
        "sourceNodes": sum(node.get("type") in SOURCE_TYPES for node in nodes),
        "density": density,
        "ontology": {"proposed": sorted(PROPOSED_ONTOLOGY), "legacy": sorted(LEGACY_ONTOLOGY)},
    }
    return {"findings": findings, "metrics": metrics, "blocking": []}


def lint_file(path: Path) -> dict:
    return lint_graph(json.loads(path.read_text(encoding="utf-8-sig")))


def _main() -> int:
    parser = argparse.ArgumentParser(description="Lint estrutural GRAFO-01..06")
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    result = lint_file(args.path)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
