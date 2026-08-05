"""Constrói e registra os manifests de execução pareada do ciclo AR-1 a partir dos logs reais."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CICLO = ROOT / "autoresearch" / "ciclos" / "ciclo-1"
EXEC = CICLO / "exec"

versao = subprocess.run(["codex.cmd", "--version"], capture_output=True, text=True).stdout.strip() or "codex-cli"
input_hash = json.loads((CICLO / "runpair-varA" / "INPUT_0.json").read_text(encoding="utf-8"))["inputHash"]


def usage(side: str) -> int:
    total = 0
    for line in (EXEC / f"raw_{side}.jsonl").read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if obj.get("type") == "turn.completed":
            u = obj.get("usage", {})
            total = int(u.get("input_tokens", 0)) + int(u.get("output_tokens", 0))
    return total


def manifest(side: str) -> Path:
    out = EXEC / f"OUT_{side}.md"
    prompt = EXEC / f"EXECPROMPT_{side}.md"
    payload = {
        "modelo": "gpt-5.5",
        "familia": "codex",
        "versao": versao,
        "parametros": {"reasoning_effort": "high", "sandbox": "danger-full-access", "invocacao": "codex exec --json (stdin)"},
        "promptHash": hashlib.sha256(prompt.read_bytes()).hexdigest(),
        "inputHash": input_hash,
        "outputPath": str(out),
        "outputSha256": hashlib.sha256(out.read_bytes()).hexdigest(),
        "tokens": usage(side),
        "duracao": max(0, int(out.stat().st_mtime - prompt.stat().st_mtime)),
        "repeticao": 0,
    }
    dest = EXEC / f"MANIFEST_{side}.json"
    dest.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return dest


for side in ("vigente", "varA", "varB"):
    print(side, manifest(side), "tokens:", usage(side))

runs = [
    ("runpair-varA", "vigente", "MANIFEST_vigente.json"),
    ("runpair-varA", "variante", "MANIFEST_varA.json"),
    ("runpair-varB", "vigente", "MANIFEST_vigente.json"),
    ("runpair-varB", "variante", "MANIFEST_varB.json"),
]
sys.path.insert(0, str(ROOT))
from forja_ar_runpair import register_manifest, validate_pair  # noqa: E402

for pair_dir, side, mf in runs:
    register_manifest(CICLO / pair_dir, side, EXEC / mf)
for pair_dir in ("runpair-varA", "runpair-varB"):
    result = validate_pair(CICLO / pair_dir)
    print(pair_dir, "valid:", result["valid"], result["errors"])
