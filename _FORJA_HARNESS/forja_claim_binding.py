"""Prepara o ledger jurídico v2 para revisão humana externa.

O comando calcula vínculos; não decide mérito, não cria chave e não assina.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from forja_authorities import authority_key, extract_authorities
from forja_n3_common import ForjaN3Error, atomic_write_json, canonical_hash, read_json, sha256_file
from forja_official_sources import source_excerpt_sha256


def _entries(payload: dict) -> list[dict]:
    for key in ("entries", "citations", "citationLedger", "sources"):
        value = payload.get(key)
        if isinstance(value, list):
            return [dict(item) for item in value if isinstance(item, dict)]
    raise ForjaN3Error("ledger não contém lista de entries")


def bind_claims(markdown_path: Path, ledger_path: Path, output_path: Path) -> dict:
    markdown_path = Path(markdown_path)
    payload = read_json(Path(ledger_path), None)
    if not markdown_path.is_file() or not isinstance(payload, dict):
        raise ForjaN3Error("Markdown ou ledger de entrada ausente/inválido")
    text = markdown_path.read_text(encoding="utf-8", errors="replace")
    paragraphs = [item.strip() for item in re.split(r"\n\s*\n", text) if item.strip()]
    inventory = {authority_key(item) for item in extract_authorities(text)}
    inventory.discard(("", "", ""))
    document_hash = sha256_file(markdown_path)
    bound = []
    for item in _entries(payload):
        label = str(item.get("claim") or item.get("id") or "entrada sem id")
        proposition = str(item.get("documentProposition") or "").strip()
        try:
            paragraph_index = int(item.get("documentParagraphIndex"))
        except (TypeError, ValueError):
            paragraph_index = 0
        if not proposition or not 1 <= paragraph_index <= len(paragraphs):
            raise ForjaN3Error(f"{label}: proposição ou índice de parágrafo inválido")
        paragraph = paragraphs[paragraph_index - 1]
        if proposition not in paragraph:
            raise ForjaN3Error(f"{label}: proposição não consta literalmente do parágrafo")
        identity = item.get("authorityIdentity")
        key = authority_key(identity if isinstance(identity, dict) else {})
        if key not in inventory:
            raise ForjaN3Error(f"{label}: autoridade não consta do inventário do documento")
        previous_binding = {
            field: item.get(field)
            for field in (
                "documentSha256", "documentPropositionSha256",
                "documentParagraphSha256", "authorityIdentitySha256",
            )
        }
        item.update({
            "documentSha256": document_hash,
            "documentPropositionSha256": canonical_hash({"proposition": proposition}),
            "documentParagraphIndex": paragraph_index,
            "documentParagraphSha256": canonical_hash({"paragraph": paragraph}),
            "authorityIdentitySha256": canonical_hash(identity),
        })
        excerpt = str(item.get("sourceExcerpt") or "").strip()
        if excerpt:
            item["sourceExcerptSha256"] = source_excerpt_sha256(excerpt)
        source = Path(str(item.get("sourcePathOrUrl") or ""))
        if source.is_file():
            item["sourceSha256"] = sha256_file(source)
        current_binding = {field: item.get(field) for field in previous_binding}
        if previous_binding != current_binding:
            item["claimReview"] = {"status": "pending_new_signature"}
        bound.append(item)
    missing = sorted(inventory - {authority_key(item.get("authorityIdentity") or {}) for item in bound})
    if missing:
        rendered = ", ".join(" ".join(part for part in key if part) for key in missing[:12])
        raise ForjaN3Error("ledger não cobre todas as autoridades do documento: " + rendered)
    result = {
        "schemaVersion": 2,
        "bindingVersion": "FORJA-LEGAL-CLAIM-BINDING-v2",
        "document": {"path": str(markdown_path), "sha256": document_hash},
        "entries": bound,
    }
    atomic_write_json(Path(output_path), result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Vincula ledger jurídico ao Markdown final")
    parser.add_argument("markdown", type=Path)
    parser.add_argument("ledger", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    result = bind_claims(args.markdown, args.ledger, args.output)
    print(json.dumps({
        "output": str(args.output),
        "documentSha256": result["document"]["sha256"],
        "entries": len(result["entries"]),
        "status": "pending_human_signature",
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

