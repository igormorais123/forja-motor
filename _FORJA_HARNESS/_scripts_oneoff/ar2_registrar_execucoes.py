"""Constrói e registra os manifests de execução pareada do ciclo AR-2 a partir dos logs reais."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CICLO = ROOT / "autoresearch" / "ciclos" / "ciclo-2"
EXEC = CICLO / "exec"

versao = subprocess.run(["codex.cmd", "--version"], capture_output=True, text=True).stdout.strip() or "codex-cli"


def usage(name: str) -> int:
    total = 0
    for line in (EXEC / f"raw_{name}.jsonl").read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if obj.get("type") == "turn.completed":
            u = obj.get("usage", {})
            total = int(u.get("input_tokens", 0)) + int(u.get("output_tokens", 0))
    return total


def manifest(tid: str, side: str, input_hash: str) -> Path:
    name = f"{tid}_{side}"
    out = EXEC / f"OUT_{name}.md"
    prompt = EXEC / f"EXECPROMPT_{name}.md"
    payload = {
        "modelo": "gpt-5.5",
        "familia": "codex",
        "versao": versao,
        "parametros": {"reasoning_effort": "high", "sandbox": "danger-full-access", "invocacao": "codex exec --json (stdin)"},
        "promptHash": hashlib.sha256(prompt.read_bytes()).hexdigest(),
        "inputHash": input_hash,
        "outputPath": str(out),
        "outputSha256": hashlib.sha256(out.read_bytes()).hexdigest(),
        "tokens": usage(name),
        "duracao": max(0, int(out.stat().st_mtime - prompt.stat().st_mtime)),
        "repeticao": 0,
    }
    dest = EXEC / f"MANIFEST_{name}.json"
    dest.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return dest


sys.path.insert(0, str(ROOT))
from forja_ar_runpair import register_manifest, validate_pair  # noqa: E402

for tid in ("t1", "t2"):
    input_hash = json.loads((CICLO / f"runpair-{tid}" / "INPUT_0.json").read_text(encoding="utf-8"))["inputHash"]
    for side_label, lado in (("vigente", "vigente"), ("varH", "variante")):
        mf = manifest(tid, side_label, input_hash)
        register_manifest(CICLO / f"runpair-{tid}", lado, mf)
        print(tid, side_label, "tokens:", usage(f"{tid}_{side_label}"))
    result = validate_pair(CICLO / f"runpair-{tid}")
    print(f"runpair-{tid}", "valid:", result["valid"], result["errors"])
