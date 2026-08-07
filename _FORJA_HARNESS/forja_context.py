"""Structured evidence and semantic continuity validators for FORJA N3."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Iterable

from forja_n3_common import atomic_write_json, canonical_hash, read_json, sha256_file


FACT_CLASSES = {"PROVADO", "DECLARADO", "INFERENCIA", "CONFLITANTE", "NAO_VERIFICADO"}
FINAL_ALLOWED = {"PROVADO", "DECLARADO"}


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def markdown_blocks(text: str) -> list[dict]:
    """Parse semantic Markdown blocks without rewriting their text."""

    lines = text.splitlines()
    blocks: list[dict] = []
    index = 0
    in_fence = False
    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        if stripped.startswith("```"):
            start = index
            chunk = [line]
            in_fence = not in_fence
            index += 1
            while index < len(lines):
                chunk.append(lines[index])
                if lines[index].strip().startswith("```"):
                    index += 1
                    in_fence = False
                    break
                index += 1
            kind, raw = "code", "\n".join(chunk)
        elif not stripped:
            index += 1
            continue
        elif re.match(r"^#{1,6}\s+", stripped):
            start, kind, raw = index, "heading", line
            index += 1
        elif stripped.startswith("|"):
            start = index
            chunk = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                chunk.append(lines[index])
                index += 1
            kind, raw = "table", "\n".join(chunk)
        elif re.match(r"^\s*>\s?", line):
            start = index
            chunk = []
            while index < len(lines) and re.match(r"^\s*>\s?", lines[index]):
                chunk.append(lines[index])
                index += 1
            kind, raw = "blockquote", "\n".join(chunk)
        elif re.match(r"^\s*(?:[-+*•]|\d+[.)])\s+", line):
            start = index
            chunk = []
            while index < len(lines) and re.match(r"^\s*(?:[-+*•]|\d+[.)])\s+", lines[index]):
                chunk.append(lines[index])
                index += 1
            kind, raw = "list", "\n".join(chunk)
        else:
            start = index
            chunk = [line]
            index += 1
            while index < len(lines):
                nxt = lines[index]
                s = nxt.strip()
                if not s or s.startswith("|") or s.startswith("```"): break
                if re.match(r"^#{1,6}\s+|^\s*>\s?|^\s*(?:[-+*•]|\d+[.)])\s+", nxt): break
                chunk.append(nxt)
                index += 1
            kind, raw = "paragraph", "\n".join(chunk)
        normalized = _norm(raw)
        block_id = f"b{len(blocks) + 1:04d}-{canonical_hash([kind, normalized])[:12]}"
        blocks.append({
            "blockId": block_id,
            "kind": kind,
            "startLine": start + 1,
            "endLine": start + raw.count("\n") + 1,
            "text": raw,
            "normalizedHash": canonical_hash(normalized),
        })
    return blocks


def validate_document_index(index_payload: dict) -> list[dict]:
    findings = []
    documents = index_payload.get("documents") or []
    seen = set()
    for position, document in enumerate(documents, 1):
        source_id = str(document.get("sourceId") or "").strip()
        if not source_id:
            findings.append({"severity": "P0", "code": "missing_source_id", "position": position})
            continue
        if source_id in seen:
            findings.append({"severity": "P0", "code": "duplicate_source_id", "sourceId": source_id})
        seen.add(source_id)
        if not document.get("sha256"):
            findings.append({"severity": "P0", "code": "missing_source_hash", "sourceId": source_id})
        page_count = document.get("pageCount")
        if not isinstance(page_count, int) or page_count < 1:
            findings.append({"severity": "P1", "code": "invalid_page_count", "sourceId": source_id})
    if not documents:
        findings.append({"severity": "P0", "code": "empty_document_index"})
    return findings


def _covered_pages(entry: dict, page_count: int) -> set[int]:
    covered: set[int] = set()
    for interval in entry.get("ranges") or []:
        if interval.get("status") not in {"read", "verified"}:
            continue
        try:
            start, end = int(interval["start"]), int(interval["end"])
        except (KeyError, TypeError, ValueError):
            continue
        covered.update(range(max(1, start), min(page_count, end) + 1))
    for excluded in entry.get("excludedPages") or []:
        if excluded.get("reason"):
            try:
                covered.add(int(excluded["page"]))
            except (KeyError, TypeError, ValueError):
                pass
    return covered


def validate_coverage(index_payload: dict, coverage_payload: dict) -> list[dict]:
    findings = []
    coverage_by_id = {str(item.get("sourceId")): item for item in coverage_payload.get("documents") or []}
    for document in index_payload.get("documents") or []:
        source_id = str(document.get("sourceId") or "")
        page_count = document.get("pageCount")
        if not isinstance(page_count, int) or page_count < 1:
            continue
        entry = coverage_by_id.get(source_id)
        if entry is None:
            findings.append({
                "severity": "P0" if document.get("critical", True) else "P1",
                "code": "coverage_missing",
                "sourceId": source_id,
            })
            continue
        missing = sorted(set(range(1, page_count + 1)) - _covered_pages(entry, page_count))
        if missing:
            findings.append({
                "severity": "P0" if document.get("critical", True) else "P1",
                "code": "pages_not_covered",
                "sourceId": source_id,
                "pages": missing,
            })
        if entry.get("extractionStatus") in {"failed", "partial", "ocr_uncertain"} and not entry.get("reviewedVisually"):
            findings.append({"severity": "P0", "code": "extraction_not_resolved", "sourceId": source_id})
    return findings


def validate_fact_ledger(fact_payload: dict, source_ids: Iterable[str]) -> list[dict]:
    findings = []
    valid_sources = set(source_ids)
    seen = set()
    for fact in fact_payload.get("facts") or []:
        fact_id = str(fact.get("factId") or "").strip()
        if not fact_id or fact_id in seen:
            findings.append({"severity": "P0", "code": "invalid_fact_id", "factId": fact_id})
            continue
        seen.add(fact_id)
        classification = str(fact.get("classification") or "").upper()
        if classification not in FACT_CLASSES:
            findings.append({"severity": "P0", "code": "invalid_fact_class", "factId": fact_id})
            continue
        sources = fact.get("sources") or []
        if classification in {"PROVADO", "DECLARADO", "CONFLITANTE"} and not sources:
            findings.append({"severity": "P0", "code": "sourced_fact_without_source", "factId": fact_id})
        for source in sources:
            if source.get("sourceId") not in valid_sources:
                findings.append({"severity": "P0", "code": "unknown_fact_source", "factId": fact_id, "sourceId": source.get("sourceId")})
            if not source.get("pageOrEvent"):
                findings.append({"severity": "P1", "code": "fact_source_without_locator", "factId": fact_id})
        if classification not in FINAL_ALLOWED and fact.get("finalUseAllowed") is True:
            findings.append({"severity": "P0", "code": "unsafe_final_use", "factId": fact_id})
    return findings


def validate_paragraph_provenance(
    markdown_text: str,
    provenance_payload: dict,
    fact_payload: dict,
    proposition_payload: dict,
) -> tuple[list[dict], list[dict]]:
    blocks = markdown_blocks(markdown_text)
    entries = {str(item.get("blockId")): item for item in provenance_payload.get("blocks") or []}
    fact_ids = {str(item.get("factId")) for item in fact_payload.get("facts") or []}
    proposition_ids = {str(item.get("propositionId")) for item in proposition_payload.get("propositions") or []}
    findings = []
    for block in blocks:
        significant = block["kind"] in {"paragraph", "blockquote", "list", "table"} and len(_norm(block["text"])) >= 45
        if not significant:
            continue
        entry = entries.get(block["blockId"])
        if entry is None:
            findings.append({"severity": "P1", "code": "block_without_provenance", "blockId": block["blockId"], "line": block["startLine"]})
            continue
        unknown_facts = sorted(set(entry.get("factIds") or []) - fact_ids)
        unknown_props = sorted(set(entry.get("propositionIds") or []) - proposition_ids)
        if unknown_facts or unknown_props:
            # Extrai excerpt do texto para âncora — primeiros ~100 caracteres ou até a primeira quebra
            text_excerpt = _norm(block["text"])[:100]
            if len(block["text"]) > 100:
                text_excerpt += "…"

            findings.append({
                "severity": "P0",
                "code": "unknown_provenance_reference",
                "gateCode": "LCX9-unknown-provenance",
                "blockId": block["blockId"],
                "factIds": unknown_facts,
                "propositionIds": unknown_props,
                "anchor": {
                    "blockId": block["blockId"],
                    "startLine": block["startLine"],
                    "endLine": block["endLine"],
                    "text": text_excerpt,
                },
            })
        if not entry.get("factIds") and not entry.get("propositionIds") and not entry.get("editorialOnly"):
            findings.append({"severity": "P1", "code": "empty_provenance", "blockId": block["blockId"]})
    return blocks, findings


def validate_context(case_dir: Path) -> dict:
    paths = {
        "index": case_dir / "F1_DOCUMENT_INDEX.json",
        "coverage": case_dir / "F1_COVERAGE.json",
        "facts": case_dir / "F3_FACT_LEDGER.json",
        "propositions": case_dir / "F4_PROPOSITION_LEDGER.json",
        "provenance": case_dir / "F6_PARAGRAPH_PROVENANCE.json",
    }
    missing = [name for name, path in paths.items() if not path.exists()]
    if missing:
        result = {
            "schemaVersion": 1,
            "approved": False,
            "p0": len(missing),
            "p1": 0,
            "blocks": 0,
            "findings": [
                {"severity": "P0", "code": "missing_ledger", "ledger": name}
                for name in missing
            ],
            "inputs": {
                name: {"path": str(path), "sha256": sha256_file(path)}
                for name, path in paths.items()
                if path.is_file()
            },
            "markdown": None,
        }
        atomic_write_json(case_dir / "CONTEXT_VALIDATION.json", result)
        return result
    index_payload = read_json(paths["index"], {})
    coverage_payload = read_json(paths["coverage"], {})
    fact_payload = read_json(paths["facts"], {})
    proposition_payload = read_json(paths["propositions"], {})
    provenance_payload = read_json(paths["provenance"], {})
    markdown_path = Path(str(provenance_payload.get("markdownPath") or ""))
    if not markdown_path.is_absolute():
        markdown_path = case_dir / markdown_path
    findings = validate_document_index(index_payload)
    findings += validate_coverage(index_payload, coverage_payload)
    source_ids = [item.get("sourceId") for item in index_payload.get("documents") or []]
    findings += validate_fact_ledger(fact_payload, source_ids)
    blocks = []
    if markdown_path.exists():
        blocks, provenance_findings = validate_paragraph_provenance(
            markdown_path.read_text(encoding="utf-8"), provenance_payload, fact_payload, proposition_payload
        )
        findings += provenance_findings
    else:
        findings.append({"severity": "P0", "code": "markdown_for_provenance_missing", "path": str(markdown_path)})
    result = {
        "schemaVersion": 1,
        "approved": not any(item["severity"] == "P0" for item in findings),
        "p0": sum(item["severity"] == "P0" for item in findings),
        "p1": sum(item["severity"] == "P1" for item in findings),
        "blocks": len(blocks),
        "findings": findings,
        "inputs": {
            name: {"path": str(path), "sha256": sha256_file(path)}
            for name, path in paths.items()
        },
        "markdown": {"path": str(markdown_path), "sha256": sha256_file(markdown_path)} if markdown_path.is_file() else None,
    }
    atomic_write_json(case_dir / "CONTEXT_VALIDATION.json", result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Valida continuidade de contexto FORJA N3")
    parser.add_argument("case_dir", type=Path)
    args = parser.parse_args()
    result = validate_context(args.case_dir.resolve())
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["approved"] else 1)


if __name__ == "__main__":
    main()
