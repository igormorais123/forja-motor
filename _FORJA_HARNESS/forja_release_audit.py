"""Auditoria somente leitura dos pacotes FORJA contra a política vigente."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from forja_n3_common import atomic_write_json, now_iso, read_json
from forja_package import RELEASE_POLICY_VERSION, release_policy_hash, revalidate_package_manifest


def audit_packages(state_root: Path) -> dict:
    results = []
    for pointer in sorted(Path(state_root).glob("case-*/FORJA_PACKAGE.json")):
        case_dir = pointer.parent
        manifest = read_json(pointer, None)
        if not isinstance(manifest, dict):
            validation = {"approved": False, "stale": True, "findings": ["manifesto ilegível"]}
            manifest = {}
        else:
            validation = revalidate_package_manifest(case_dir, manifest)
        results.append({
            "caseId": case_dir.name,
            "packageId": manifest.get("packageId"),
            "createdAt": manifest.get("createdAt"),
            "declaredStatus": manifest.get("status"),
            "approvedNow": validation["approved"],
            "stale": validation.get("stale", not validation["approved"]),
            "findings": validation.get("findings") or [],
        })
    blocked = sum(not item["approvedNow"] for item in results)
    return {
        "schemaVersion": 1,
        "auditType": "read_only_current_release_policy",
        "generatedAt": now_iso(),
        "policyVersion": RELEASE_POLICY_VERSION,
        "policyHash": release_policy_hash(),
        "packagesScanned": len(results),
        "approvedNow": len(results) - blocked,
        "blockedOrStale": blocked,
        "packages": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Audita pacotes FORJA sem alterar estado")
    parser.add_argument("--state-root", type=Path, default=Path(__file__).resolve().parent / "state")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--fail-on-blocked", action="store_true")
    args = parser.parse_args()
    result = audit_packages(args.state_root)
    if args.output:
        atomic_write_json(args.output, result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 2 if args.fail_on_blocked and result["blockedOrStale"] else 0


if __name__ == "__main__":
    raise SystemExit(main())

