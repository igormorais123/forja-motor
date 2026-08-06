"""Baseline canônico por caso para o PRD 45.

Só considera ``state/<case>/n4_artifacts``. Cópias em ``runs`` e ``history``
continuam acessíveis, mas não inflacionam o denominador prospectivo.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from forja_n3_common import FORJA, atomic_write_json, now_iso, sha256_file


def canonical_inventory(case_dir: Path, *, filenames: tuple[str, ...] = ("F2_QUESTION_TREE.json",)) -> dict:
    artifacts_dir = Path(case_dir) / "n4_artifacts"
    artifacts = []
    for filename in filenames:
        path = artifacts_dir / filename
        if not path.is_file():
            artifacts.append({"filename": filename, "status": "missing"})
            continue
        artifacts.append({"filename": filename, "status": "present", "path": str(path), "sha256": sha256_file(path), "size": path.stat().st_size})
    return {"schemaVersion": 1, "caseId": Path(case_dir).name, "generatedAt": now_iso(), "scope": "n4_artifacts_only", "artifacts": artifacts}


def freeze_case(case_dir: Path, *, filenames: tuple[str, ...] = ("F2_QUESTION_TREE.json",)) -> Path:
    case_dir = Path(case_dir)
    output = case_dir / "instrumentation" / "CANONICAL_BASELINE.json"
    atomic_write_json(output, canonical_inventory(case_dir, filenames=filenames))
    return output


def verify_case(case_dir: Path) -> dict:
    path = Path(case_dir) / "instrumentation" / "CANONICAL_BASELINE.json"
    if not path.is_file():
        return {"caseId": Path(case_dir).name, "status": "not_verified", "reason": "baseline ausente"}
    baseline = json.loads(path.read_text(encoding="utf-8"))
    current = canonical_inventory(case_dir, filenames=tuple(item.get("filename") for item in baseline.get("artifacts") or [] if item.get("filename")))
    divergences = []
    before = {item["filename"]: item for item in baseline.get("artifacts") or []}
    after = {item["filename"]: item for item in current.get("artifacts") or []}
    for filename in sorted(set(before) | set(after)):
        if before.get(filename, {}).get("sha256") != after.get(filename, {}).get("sha256") or before.get(filename, {}).get("status") != after.get(filename, {}).get("status"):
            divergences.append(filename)
    return {"caseId": Path(case_dir).name, "status": "pass" if not divergences else "diverged", "divergences": divergences, "baseline": str(path)}


def freeze_all(state_dir: Path | None = None) -> dict:
    root = Path(state_dir or (FORJA / "state"))
    cases = []
    for case in sorted(path for path in root.glob("case-*") if path.is_dir()):
        # O baseline F2A é do acervo canônico materializado. Diretórios de
        # fila, snapshots antigos e casos sem árvore não entram no denominador.
        if not (case / "n4_artifacts" / "F2_QUESTION_TREE.json").is_file():
            continue
        cases.append({"caseId": case.name, "baselinePath": str(freeze_case(case))})
    return {"schemaVersion": 1, "generatedAt": now_iso(), "scope": "canonical_n4_per_case", "caseCount": len(cases), "cases": cases}


def _main() -> int:
    parser = argparse.ArgumentParser(description="Congela ou verifica baseline canônico F2A por caso")
    parser.add_argument("command", choices=("freeze", "verify"))
    parser.add_argument("case", nargs="?", type=Path)
    args = parser.parse_args()
    if args.command == "freeze":
        if args.case:
            result = {"path": str(freeze_case(args.case))}
        else:
            result = freeze_all()
    else:
        if not args.case:
            parser.error("verify exige caso")
        result = verify_case(args.case)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("status", "pass") in {"pass", "not_verified"} else 1


if __name__ == "__main__":
    raise SystemExit(_main())
