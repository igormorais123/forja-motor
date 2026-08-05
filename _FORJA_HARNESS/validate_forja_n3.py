"""Canonical FORJA validation runner for legacy script-tests and N3 unittests."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

from forja_n3_common import FORJA, WORKSPACE, atomic_write_json, now_iso
from forja_phase_contracts import validate_all


UNIT_MODULES = [
    "test_forja_reconcile",
    "test_forja_n3_context",
    "test_forja_n3_fidelity",
    "test_forja_n3_headless",
    "test_forja_n3_management",
    "test_forja_n3_metrics",
    "test_forja_n3_package",
    "test_forja_n3_runner",
    "test_forja_n3_server_routes",
    "test_forja_n3_state",
    "test_forja_n3_visual",
    "test_word_visual_pipeline_retry",
]

SCRIPT_TESTS = [
    "test_forja_verificador.py",
    "test_forja_citacoes.py",
    "test_forja_injection.py",
    "test_f7_campos.py",
    "test_licao41.py",
    "test_forja_regua.py",
    "_scripts_oneoff/validate_f7_integration.py",
]

COMPILE_TARGETS = [
    *FORJA.glob("forja_*.py"),
    WORKSPACE / "_FERRAMENTAS" / "medina_visual_lint.py",
    WORKSPACE / "_FERRAMENTAS" / "word_visual_pipeline.py",
    WORKSPACE / "_FERRAMENTAS" / "word_pdf_worker.py",
    WORKSPACE / "gestao_escritorio" / "scripts" / "sync_forja_gestao.py",
    WORKSPACE / "gestao_escritorio" / "scripts" / "dashboard_enrichment.py",
    WORKSPACE / "gestao_escritorio" / "scripts" / "render_dashboard.py",
    WORKSPACE / "gestao_escritorio" / "scripts" / "server.py",
]


def run_command(name: str, command: list[str], *, timeout: int) -> dict:
    started = time.monotonic()
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    try:
        proc = subprocess.run(
            command,
            cwd=FORJA,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            env=env,
            shell=False,
        )
        output = (proc.stdout + "\n" + proc.stderr).strip()
        return {
            "name": name,
            "status": "pass" if proc.returncode == 0 else "fail",
            "exitCode": proc.returncode,
            "seconds": round(time.monotonic() - started, 3),
            "tail": output[-3000:],
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "name": name,
            "status": "timeout",
            "exitCode": None,
            "seconds": round(time.monotonic() - started, 3),
            "tail": str(exc)[-3000:],
        }


def validate_json_files() -> dict:
    invalid = []
    count = 0
    for root in (FORJA, WORKSPACE / "gestao_escritorio" / "data"):
        for path in root.rglob("*.json"):
            count += 1
            try:
                json.loads(path.read_text(encoding="utf-8-sig"))
            except Exception as exc:
                invalid.append({"path": str(path), "error": str(exc)})
    return {"status": "pass" if not invalid else "fail", "checked": count, "invalid": invalid}


def main() -> None:
    parser = argparse.ArgumentParser(description="Executa a validação canônica da FORJA N3")
    parser.add_argument("--real-word", action="store_true", help="inclui render real Word/PDF")
    parser.add_argument("--run-replay", action="store_true", help="refaz o replay dos 21 estados")
    parser.add_argument("--output", type=Path, default=FORJA / "reports" / "N3_VALIDATION_2026-07-10.json")
    args = parser.parse_args()

    results = []
    compile_paths = [str(path) for path in COMPILE_TARGETS if path.is_file()]
    results.append(run_command("compile", [sys.executable, "-m", "py_compile", *compile_paths], timeout=120))
    results.append(run_command(
        "n3_unittests",
        [sys.executable, "-m", "unittest", "-v", *UNIT_MODULES],
        timeout=300,
    ))
    for script in SCRIPT_TESTS:
        results.append(run_command(script, [sys.executable, script], timeout=300))
    if args.real_word:
        results.append(run_command(
            "test_real_telemetria_licao41.py",
            [sys.executable, "test_real_telemetria_licao41.py"],
            timeout=600,
        ))
    if args.run_replay:
        results.append(run_command(
            "shadow_replay",
            [sys.executable, "forja_n3_shadow_replay.py"],
            timeout=300,
        ))
    contracts = validate_all()
    json_result = validate_json_files()
    report = {
        "schemaVersion": 1,
        "specVersion": "N3.0-r2",
        "generatedAt": now_iso(),
        "status": "pass" if all(item["status"] == "pass" for item in results) and json_result["status"] == "pass" else "fail",
        "commands": results,
        "contracts": {"status": "pass", "count": len(contracts)},
        "json": json_result,
        "realWordIncluded": args.real_word,
        "replayIncluded": args.run_replay,
    }
    atomic_write_json(args.output, report)
    print(json.dumps({
        "status": report["status"],
        "commands": len(results),
        "passed": sum(item["status"] == "pass" for item in results),
        "contracts": len(contracts),
        "jsonChecked": json_result["checked"],
        "output": str(args.output),
    }, ensure_ascii=False, indent=2))
    raise SystemExit(0 if report["status"] == "pass" else 1)


if __name__ == "__main__":
    main()
