"""M0 baseline: initialize additive N3 state and audit N4 readiness.

Legacy files and production artifacts are hashed before and after. The command
does not rewrite them and never represents a historical cycle as a new run.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from forja_n3_common import FORJA, atomic_write_json, now_iso, read_json, sha256_file
from forja_n4_validate import validate_case
from forja_state_machine import initialize_case


def _protected(case_dir: Path) -> dict[str, str]:
    result = {}
    for path in case_dir.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(case_dir)
        if relative.parts[0] in {"events", "n4_artifacts", "n3_artifacts", "runs", "packages"}:
            continue
        if path.name in {"FORJA_N3_STATE.json", "FORJA_EVENTS.jsonl", "FORJA_CASE_MANIFEST.json", "FORJA_MANAGEMENT_SYNC.json", "FORJA_RUN_METRICS.json"}:
            continue
        result[str(relative)] = sha256_file(path)
    return result


def run(*, initialize_n3: bool) -> dict:
    cases = []
    for case_dir in sorted(path for path in (FORJA / "state").iterdir() if path.is_dir() and path.name.startswith("case-")):
        before = _protected(case_dir)
        initialized = False
        if initialize_n3 and not (case_dir / "FORJA_N3_STATE.json").is_file():
            initialize_case(case_dir, from_legacy=(case_dir / "FORJA_STATE.json").is_file())
            initialized = True
        validation = validate_case(case_dir)
        after = _protected(case_dir)
        changed = sorted(key for key in set(before) | set(after) if before.get(key) != after.get(key))
        cases.append({
            "caseId": case_dir.name,
            "n3Initialized": initialized,
            "legacyProtectedFiles": len(before),
            "protectedChanges": changed,
            "n4": {
                "approved": validation.get("approved"),
                "mode": validation.get("mode"),
                "expected": (validation.get("counts") or {}).get("expected"),
                "present": (validation.get("counts") or {}).get("present"),
                "p0": (validation.get("counts") or {}).get("p0"),
                "p1": (validation.get("counts") or {}).get("p1"),
            },
        })
    report = {
        "schemaVersion": 1,
        "specVersion": "N4.0-candidate",
        "generatedAt": now_iso(),
        "initializeN3": initialize_n3,
        "caseCount": len(cases),
        "n3Initialized": sum(item["n3Initialized"] for item in cases),
        "protectedChanges": sum(bool(item["protectedChanges"]) for item in cases),
        "cases": cases,
    }
    stamp = now_iso().replace(":", "").replace("-", "")[:15]
    output = FORJA / "reports" / f"N4_M0_BASELINE_{stamp}.json"
    atomic_write_json(output, report)
    report["reportPath"] = str(output)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Comprova baseline N3/N4 sem alterar artefatos históricos")
    parser.add_argument("--initialize-n3", action="store_true")
    args = parser.parse_args()
    print(json.dumps(run(initialize_n3=args.initialize_n3), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
