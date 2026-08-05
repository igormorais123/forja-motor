from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "deliverables" / "diagramas"
MMDC = shutil.which("mmdc") or str(Path.home() / "AppData" / "Roaming" / "npm" / "mmdc.cmd")


def slug(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9_-]+", "_", value).strip("_")
    return value[:80] or "diagram"


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    rendered: list[dict[str, str]] = []
    failures: list[dict[str, str]] = []

    for document in sorted(ROOT.glob("*.md")):
        raw = document.read_text(encoding="utf-8")
        for index, match in enumerate(re.finditer(r"```mermaid\n(.*?)\n```", raw, flags=re.DOTALL), 1):
            prefix = raw[: match.start()]
            headings = re.findall(r"^##+\s+(.+)$", prefix, flags=re.MULTILINE)
            title = headings[-1] if headings else f"diagram-{index:02d}"
            stem = slug(f"{document.stem}-{index:02d}-{title}")
            source = OUTPUT / f"{stem}.mmd"
            target = OUTPUT / f"{stem}.svg"
            source.write_text(match.group(1).strip() + "\n", encoding="utf-8")
            command = [MMDC, "-i", str(source), "-o", str(target), "-w", "1600", "-b", "transparent"]
            result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace")
            if result.returncode == 0 and target.is_file() and target.stat().st_size:
                rendered.append({"source": str(document.relative_to(ROOT)), "title": title, "svg": str(target.relative_to(ROOT))})
            else:
                failures.append(
                    {
                        "source": str(document.relative_to(ROOT)),
                        "title": title,
                        "stderr": (result.stderr or result.stdout)[-1500:],
                    }
                )

    report = {"ok": not failures, "count": len(rendered), "failures": failures, "rendered": rendered}
    (OUTPUT / "render_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"ok": report["ok"], "count": report["count"], "failures": len(failures)}, ensure_ascii=False))
    if failures:
        for failure in failures:
            print(json.dumps(failure, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
