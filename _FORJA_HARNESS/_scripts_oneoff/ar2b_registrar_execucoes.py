"""Registra manifests da rodada 2 do ciclo AR-2 (nomes opacos) e valida paridade em runpair-t1b/t2b."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CICLO = ROOT / "autoresearch" / "ciclos" / "ciclo-2"
EXEC2 = CICLO / "exec2"

versao = subprocess.run(["codex.cmd", "--version"], capture_output=True, text=True).stdout.strip() or "codex-cli"
MAP = json.loads((EXEC2 / "EXECMAP.json").read_text(encoding="utf-8"))


def usage(eid: str) -> int:
    total = 0
    for line in (EXEC2 / f"raw_{eid}.jsonl").read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if obj.get("type") == "turn.completed":
            u = obj.get("usage", {})
            total = int(u.get("input_tokens", 0)) + int(u.get("output_tokens", 0))
    return total


sys.path.insert(0, str(ROOT))
from forja_ar_runpair import freeze_input, register_manifest, validate_pair  # noqa: E402

INPUTS = {
    "t1": (
        "case-email-auto-19f3f25cb64df962",
        ROOT / "state" / "case-email-auto-19f3f25cb64df962" / "n3_artifacts" / "F6_REDACAO_TEMPLATE" / "draft_markdown.md",
    ),
    "t2": (
        "case-email-azimut-19f3ed5bdbdcf159",
        ROOT / "state" / "case-email-azimut-19f3ed5bdbdcf159" / "runs" / "azimut-v4-20260719-f7_auditoria"
        / "F7_AUDITORIA_JURIDICA_FACTUAL" / "attempt-azimut-v4-20260719" / "final_markdown_v4.md",
    ),
}

for tid, (case_id, alvo) in INPUTS.items():
    pair_dir = CICLO / f"runpair-{tid}b"
    freeze_input(pair_dir, case_id, alvo)
    input_hash = json.loads((pair_dir / "INPUT_0.json").read_text(encoding="utf-8"))["inputHash"]
    for eid, (m_tid, side) in MAP.items():
        if m_tid != tid:
            continue
        out = EXEC2 / f"OUT_{eid}.md"
        prompt = EXEC2 / f"EXECPROMPT_{eid}.md"
        payload = {
            "modelo": "gpt-5.5",
            "familia": "codex",
            "versao": versao,
            "parametros": {"reasoning_effort": "high", "sandbox": "danger-full-access", "invocacao": "codex exec --json (stdin)"},
            "promptHash": hashlib.sha256(prompt.read_bytes()).hexdigest(),
            "inputHash": input_hash,
            "outputPath": str(out),
            "outputSha256": hashlib.sha256(out.read_bytes()).hexdigest(),
            "tokens": usage(eid),
            "duracao": max(0, int(out.stat().st_mtime - prompt.stat().st_mtime)),
            "repeticao": 0,
        }
        mf = EXEC2 / f"MANIFEST_{eid}.json"
        mf.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        lado = "vigente" if side == "vigente" else "variante"
        register_manifest(pair_dir, lado, mf)
        print(tid, eid, side, "tokens:", payload["tokens"])
    result = validate_pair(pair_dir)
    print(f"runpair-{tid}b", "valid:", result["valid"], result["errors"])
