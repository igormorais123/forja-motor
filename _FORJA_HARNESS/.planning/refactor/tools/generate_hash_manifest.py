from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "deliverables" / "PLANNING_PACKAGE_HASHES.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    candidates = [
        *ROOT.glob("*.md"),
        ROOT / "REFACTOR_PLAN_MANIFEST.json",
        *ROOT.glob("plans/*.md"),
        *ROOT.glob("tools/*.py"),
    ]
    files = []
    for path in sorted({item.resolve() for item in candidates if item.is_file()}):
        files.append(
            {
                "path": path.relative_to(ROOT).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )
    payload = {
        "schemaVersion": "FORJA-PLANNING-SNAPSHOT-1.0",
        "generatedAt": "2026-07-15",
        "algorithm": "sha256",
        "files": files,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"ok": True, "files": len(files), "output": str(OUTPUT)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
