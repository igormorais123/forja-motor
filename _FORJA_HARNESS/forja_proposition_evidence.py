"""Ponte experimental F4 → F5 → F7 (PRD 45, R1/R2).

O mapa é derivado e vive em ``state/<case>/instrumentation``. Nenhuma função
deste módulo escreve nos ledgers de F4/F5 ou no grafo F3.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable, Mapping

from forja_n3_common import sha256_file
from forja_severidade import blocking_findings


MAP_FILENAME = "F5_PROPOSITION_EVIDENCE_MAP.json"
ALLOWED_RELATIONS = {"supports", "qualifies", "contradicts", "does_not_reach"}
EVIDENCE_VERSION = "FORJA-INSTRUMENTACAO-v2"


def _issue(code: str, detail: str, *, severity: str) -> dict:
    return {"code": code, "severity": severity, "detail": detail}


def _items(payload: Mapping | None, *keys: str) -> list[dict]:
    if not isinstance(payload, Mapping):
        return []
    for key in keys:
        value = payload.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
        if isinstance(value, Mapping):
            return [item for item in value.values() if isinstance(item, dict)]
    return []


def proposition_items(payload: Mapping | None) -> list[dict]:
    return _items(payload, "propositions", "claims", "items")


def source_items(payload: Mapping | None) -> list[dict]:
    return _items(payload, "sources", "entries", "officialSources")


def proposition_id(item: Mapping) -> str:
    return str(item.get("propositionId") or item.get("id") or item.get("claimId") or "")


def source_id(item: Mapping) -> str:
    return str(item.get("sourceId") or item.get("id") or "")


def _is_decisive(item: Mapping) -> bool:
    if item.get("decisive") is not None:
        return bool(item.get("decisive"))
    if item.get("materiality") is not None:
        return str(item.get("materiality")).casefold() in {"decisive", "material"}
    if item.get("decisionClass") is not None:
        return str(item.get("decisionClass")).casefold() in {"decisive", "material"}
    # O ledger F4 existente não tem uma coluna decisiva. Na ausência da
    # marcação, toda proposição emitida é cobrada; declarar ``decisive:false``
    # é a única forma explícita de excluí-la do denominador.
    return True


def _declared_hash(entry: Mapping | None) -> str:
    if not isinstance(entry, Mapping):
        return ""
    return str(entry.get("sha256") or entry.get("archivedSha256") or entry.get("contentSha256") or "")


def _source_hash(source: Mapping, *, base_dir: Path | None = None) -> tuple[str, bool]:
    declared = _declared_hash(source)
    candidates = [source.get("archivedPath"), source.get("archived"), source.get("path"), source.get("localCopy")]
    for value in candidates:
        if not value:
            continue
        path = Path(str(value))
        if base_dir and not path.is_absolute():
            path = base_dir / path
        if path.is_file():
            return sha256_file(path), True
    return declared, False


def _refs_match(payload: Mapping, proposition_ledger: Mapping | None, source_ledger: Mapping | None) -> list[dict]:
    findings: list[dict] = []
    for field, ledger in (("propositionLedger", proposition_ledger), ("sourceLedger", source_ledger)):
        ref = payload.get(field) or {}
        expected = _declared_hash(ref)
        if expected and isinstance(ledger, Mapping):
            actual = str(ledger.get("contentHash") or "")
            if actual and actual != expected:
                findings.append(_issue("EVID-05", f"{field}: hash do ledger consumido diverge do produzido", severity="p0"))
    return findings


def validate_map(
    payload: Mapping | None,
    proposition_ledger: Mapping | None = None,
    source_ledger: Mapping | None = None,
    *,
    f7_source_ledger: Mapping | None = None,
    source_base_dir: Path | None = None,
    f3_before_sha256: str | None = None,
    f3_after_sha256: str | None = None,
) -> list[dict]:
    """Emite EVID-01..07, preservando severidade do instrumento."""
    if not isinstance(payload, Mapping):
        return [_issue("EVID-00", "mapa ausente ou inválido", severity="p0")]
    findings: list[dict] = []
    if payload.get("schemaVersion") != 1:
        findings.append(_issue("EVID-00", "schemaVersion do mapa divergente", severity="p0"))
    if payload.get("producerPhase") != "F5_PESQUISA_OFICIAL":
        findings.append(_issue("EVID-00", "producerPhase deve ser F5_PESQUISA_OFICIAL", severity="p0"))
    props = {proposition_id(item): item for item in proposition_items(proposition_ledger)}
    sources = {source_id(item): item for item in source_items(source_ledger)}
    f7_sources = {source_id(item) for item in source_items(f7_source_ledger)}
    findings.extend(_refs_match(payload, proposition_ledger, source_ledger))
    links = [item for item in payload.get("links") or [] if isinstance(item, Mapping)]
    link_by_prop: dict[str, list[Mapping]] = {}
    for link in links:
        pid = str(link.get("propositionId") or "")
        sid = str(link.get("sourceId") or "")
        link_by_prop.setdefault(pid, []).append(link)
        if pid not in props:
            findings.append(_issue("EVID-02", f"propositionId inexistente: {pid}", severity="p0"))
        if sid not in sources:
            findings.append(_issue("EVID-03", f"sourceId inexistente: {sid}", severity="p0"))
            continue
        relation = str(link.get("relation") or "")
        if relation not in ALLOWED_RELATIONS:
            findings.append(_issue("EVID-06", f"relação inválida em {link.get('linkId') or pid}: {relation}", severity="p0"))
        source = sources[sid]
        expected_hash, recomputed = _source_hash(source, base_dir=source_base_dir)
        mapped_hash = str(link.get("archivedSourceSha256") or "")
        if recomputed and not mapped_hash:
            findings.append(_issue("EVID-04", f"fonte arquivada sem hash no vínculo: {sid}", severity="p0"))
        if mapped_hash and expected_hash and mapped_hash != expected_hash:
            findings.append(_issue("EVID-04", f"hash da fonte arquivada diverge: {sid}", severity="p0"))
        if mapped_hash and not expected_hash:
            findings.append(_issue("EVID-04", f"fonte arquivada sem hash recomputável: {sid}", severity="p0"))
        produced = str(link.get("producedSourceSha256") or link.get("archivedSourceSha256") or "")
        consumed = str(link.get("consumedSourceSha256") or link.get("consumedSha256") or "")
        if consumed and produced and consumed != produced:
            findings.append(_issue("EVID-05", f"hash consumido diverge do produzido em {sid}", severity="p0"))
        if f7_source_ledger is not None and sid not in f7_sources:
            findings.append(_issue("EVID-07", f"fonte {sid} não reconciliada no ledger verificado de F7", severity="p1"))

    blocked = {}
    for item in payload.get("blockedPropositions") or []:
        if isinstance(item, str):
            blocked[item] = "bloqueio declarado sem detalhe adicional"
        elif isinstance(item, Mapping):
            blocked[str(item.get("propositionId") or "")] = str(item.get("reason") or "")
    for pid, item in props.items():
        if not _is_decisive(item):
            continue
        if not link_by_prop.get(pid) and not str(blocked.get(pid) or "").strip():
            findings.append(_issue("EVID-01", f"proposição decisiva sem link nem bloqueio: {pid}", severity="p1"))
    if f3_before_sha256 and f3_after_sha256 and f3_before_sha256 != f3_after_sha256:
        findings.append(_issue("EVID-05", "F3_REASONING_GRAPH foi alterado durante a F5", severity="p0"))
    return findings


def verify_f3_immutable(before: Path | str, after: Path | str) -> dict:
    before_hash = sha256_file(Path(before))
    after_hash = sha256_file(Path(after))
    return {"beforeSha256": before_hash, "afterSha256": after_hash, "unchanged": before_hash == after_hash}


def reconcile_f7(payload: Mapping, f7_source_ledger: Mapping, *, proposition_ledger: Mapping | None = None,
                  source_ledger: Mapping | None = None, f3_before_sha256: str | None = None,
                  f3_after_sha256: str | None = None) -> dict:
    # A reconciliação pode ser executada no consumidor F7 sem reler o arquivo
    # original de F4. Nesse caso, os IDs já presentes no mapa formam apenas o
    # catálogo de identidade; eles não criam novas proposições nem alteram o
    # ledger histórico.
    if proposition_ledger is None:
        ids = {str(item.get("propositionId") or "") for item in payload.get("links") or [] if isinstance(item, Mapping)}
        ids.update(str(item.get("propositionId") or item) for item in payload.get("blockedPropositions") or [] if isinstance(item, Mapping) or isinstance(item, str))
        proposition_ledger = {"propositions": [{"id": value} for value in sorted(ids) if value]}
    source_ledger = source_ledger or f7_source_ledger
    findings = validate_map(payload, proposition_ledger=proposition_ledger, source_ledger=source_ledger,
                            f7_source_ledger=f7_source_ledger,
                            f3_before_sha256=f3_before_sha256, f3_after_sha256=f3_after_sha256)
    return {"findings": findings, "approvedForObservation": not blocking_findings(findings),
            "metricsEligible": not bool(blocking_findings(findings))}


def build_map(
    *, case_id: str, producer_run_id: str, proposition_ledger: Mapping, source_ledger: Mapping,
    links: Iterable[Mapping] = (), blocked_propositions: Iterable[Mapping | str] = (),
    proposition_hash: str = "", source_hash: str = "",
) -> dict:
    return {
        "schemaVersion": 1,
        "specVersion": EVIDENCE_VERSION,
        "caseId": case_id,
        "producerPhase": "F5_PESQUISA_OFICIAL",
        "producerRunId": producer_run_id,
        "propositionLedger": {"artifactId": "proposition_ledger", "sha256": proposition_hash},
        "sourceLedger": {"artifactId": "source_ledger", "sha256": source_hash},
        "links": [dict(link) for link in links],
        "blockedPropositions": list(blocked_propositions),
    }


def _main() -> int:
    parser = argparse.ArgumentParser(description="Lint da ponte experimental F4-F5-F7")
    parser.add_argument("map", type=Path)
    parser.add_argument("--propositions", type=Path)
    parser.add_argument("--sources", type=Path)
    parser.add_argument("--f7-sources", type=Path)
    args = parser.parse_args()
    read = lambda path: json.loads(path.read_text(encoding="utf-8-sig")) if path else None
    result = validate_map(read(args.map), read(args.propositions), read(args.sources), f7_source_ledger=read(args.f7_sources))
    print(json.dumps({"approved": not blocking_findings(result), "findings": result}, ensure_ascii=False, indent=2))
    return 0 if not blocking_findings(result) else 1


if __name__ == "__main__":
    raise SystemExit(_main())
