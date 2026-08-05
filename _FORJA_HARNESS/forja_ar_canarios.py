"""Canários públicos e secretos de falha única do FORJA AUTO-RESEARCH."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

from forja_ar_corpus import secrets_dir
from forja_ar_indicadores import computar_indicadores

SCHEMA = "FORJA-AR-v1"
ROOT = Path(__file__).resolve().parent
PUBLIC_MANIFEST = ROOT / "autoresearch" / "canarios" / "CANARIOS_MANIFEST.json"
FIXED_TIME = "1970-01-01T00:00:00Z"


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8", errors="replace"))


def _adverse(indicator: str, base: dict, changed: dict) -> bool:
    before = base["indicadores"][indicator]
    after = changed["indicadores"][indicator]
    if before.get("valor") is None or after.get("valor") is None:
        return False
    return float(after["valor"]) < float(before["valor"])


def verificar_manifest(manifest_path: Path) -> dict:
    """Exige kill pelo sensor-alvo, atribuição e controle benigno vivo."""
    manifest = _load(manifest_path)
    root = manifest_path.parent
    results = []
    entries = list(manifest.get("classes") or []) + list(manifest.get("examples") or [])
    for entry in entries:
        folder = root / str(entry["path"])
        base_path = folder / str(entry.get("base", "base.md"))
        mutation_path = folder / str(entry.get("mutation", "mutacao.md"))
        control_path = folder / str(entry.get("control", "controle_benigno.md"))
        errors = []
        expected_hashes = entry.get("hashes") or {}
        for label, path in (("base", base_path), ("mutation", mutation_path), ("control", control_path)):
            if not path.is_file():
                errors.append(f"{label}_ausente")
            elif expected_hashes.get(label) and _sha(path) != expected_hashes[label]:
                errors.append(f"{label}_hash_divergente")
        if errors:
            results.append({"id": entry.get("id"), "passed": False, "errors": errors})
            continue
        context = entry.get("context") if isinstance(entry.get("context"), dict) else {}
        base = computar_indicadores(base_path.read_text(encoding="utf-8", errors="replace"), context)
        mutation = computar_indicadores(mutation_path.read_text(encoding="utf-8", errors="replace"), context)
        control = computar_indicadores(control_path.read_text(encoding="utf-8", errors="replace"), context)
        target = str(entry["targetSensor"])
        kill = _adverse(target, base, mutation)
        benign_alive = not _adverse(target, base, control)
        other_changes = []
        for indicator in sorted(base["indicadores"]):
            if indicator == target:
                continue
            left = base["indicadores"][indicator].get("valor")
            right = mutation["indicadores"][indicator].get("valor")
            if left is not None and right is not None and left != right:
                other_changes.append(indicator)
        results.append(
            {
                "id": entry.get("id"),
                "targetSensor": target,
                "mutationKilled": kill,
                "benignAlive": benign_alive,
                "otherSensorsChanged": other_changes,
                "passed": kill and benign_alive and not other_changes,
                "errors": [],
            }
        )
    all_pass = bool(entries) and all(item["passed"] for item in results)
    return {
        "schemaVersion": SCHEMA,
        "generatedAt": FIXED_TIME,
        "producerRunId": "forja-ar-canarios",
        "allPass": all_pass,
        "mutationKill": sum(item.get("mutationKilled") is True for item in results),
        "total": len(results),
        "results": results,
    }


def verificar(*, public_manifest: Path = PUBLIC_MANIFEST, secreto: bool = False) -> dict:
    """Executa camada pública e, quando exigido, a camada externa."""
    public = verificar_manifest(public_manifest)
    payload = {
        "schemaVersion": SCHEMA,
        "generatedAt": FIXED_TIME,
        "producerRunId": "forja-ar-canarios-aggregate",
        "public": public,
        "secret": None,
        "allPass": public["allPass"],
    }
    if secreto:
        secret_manifest = secrets_dir(create=True) / "canarios_secretos" / "CANARIOS_MANIFEST.json"
        if not secret_manifest.is_file():
            payload["secret"] = {"allPass": False, "reason": f"manifest secreto ausente em {secret_manifest}"}
            payload["allPass"] = False
        else:
            secret = verificar_manifest(secret_manifest)
            payload["secret"] = {
                "allPass": secret["allPass"],
                "mutationKill": secret["mutationKill"],
                "total": secret["total"],
            }
            payload["allPass"] = payload["allPass"] and secret["allPass"]
    return payload


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Canários do FORJA AUTO-RESEARCH")
    parser.add_argument("--verificar", action="store_true", required=True)
    parser.add_argument("--secreto", action="store_true")
    parser.add_argument("--manifest", type=Path, default=PUBLIC_MANIFEST)
    args = parser.parse_args(argv)
    try:
        result = verificar(public_manifest=args.manifest, secreto=args.secreto)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["allPass"] else 2
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"erro: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
