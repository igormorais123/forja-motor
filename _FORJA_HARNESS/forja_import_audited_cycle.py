"""Register already-audited cycle files in N3 without rewriting or re-running them."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from forja_n3_common import resolve_case_dir, sha256_file
from forja_state_machine import derive_state, record_event


ROLE_RULES = (
    (re.compile(r"F7.*\.json$", re.I), "f7_gate_result"),
    (re.compile(r"F8.*\.json$", re.I), "f8_qa_ledger"),
    (re.compile(r"(?:FIDELITY|FIDELIDADE).*\.json$", re.I), "format_fidelity"),
    (re.compile(r"HELENA.*\.(?:md|json)$", re.I), "helena_opinion"),
    (re.compile(r"CICERO.*\.(?:md|json)$", re.I), "cicero_opinion"),
    (re.compile(r"EMAIL.*\.(?:txt|md)$", re.I), "email_draft"),
    (re.compile(r"\.docx$", re.I), "final_docx"),
    (re.compile(r"\.pdf$", re.I), "final_pdf"),
    (re.compile(r"\.md$", re.I), "draft_markdown"),
)


def role_for(path: Path) -> str:
    for pattern, role in ROLE_RULES:
        if pattern.search(path.name):
            return role
    return "historical_cycle_artifact"


def import_cycle(case_dir: Path, source_dir: Path) -> dict:
    files = [path for path in sorted(source_dir.iterdir()) if path.is_file() and path.suffix.lower() in {".md", ".json", ".txt", ".docx", ".pdf"}]
    imported = []
    state = derive_state(case_dir)
    for path in files:
        digest = sha256_file(path)
        role = role_for(path)
        artifact_id = role
        if artifact_id in (state.get("artifacts") or {}) and (state["artifacts"][artifact_id] or {}).get("sha256") != digest:
            artifact_id = f"{role}-{digest[:10]}"
        artifact = {
            "path": str(path.resolve()),
            "sha256": digest,
            "size": path.stat().st_size,
            "role": role,
            "audience": "internal_review",
            "releasePolicy": "historical_audited_import",
            "historicalImport": True,
        }
        _, state, created = record_event(
            case_dir,
            "artifact_promoted",
            expected_revision=state["revision"],
            idempotency_key=f"historical-import:{artifact_id}:{digest}",
            actor="forja-n3-import",
            artifact_hashes={artifact_id: digest},
            payload={"artifactId": artifact_id, "artifact": artifact, "historicalImport": True},
        )
        imported.append({"artifactId": artifact_id, "path": str(path), "sha256": digest, "created": created})
    return {"caseId": case_dir.name, "sourceDir": str(source_dir), "files": len(files), "imported": imported, "revision": state["revision"]}


def main() -> None:
    parser = argparse.ArgumentParser(description="Registra ciclo auditado existente no estado aditivo N3")
    parser.add_argument("case")
    parser.add_argument("source_dir", type=Path)
    args = parser.parse_args()
    if not args.source_dir.is_dir():
        raise SystemExit(f"pasta ausente: {args.source_dir}")
    print(json.dumps(import_cycle(resolve_case_dir(args.case), args.source_dir), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
