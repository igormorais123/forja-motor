"""Read-only N2 -> N3 shadow replay with a deeper six-case regression corpus."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

from forja_n3_common import FORJA, WORKSPACE, atomic_write_json, atomic_write_text, now_iso, read_json, sha256_file
from forja_state_machine import derive_state, initialize_case

sys.path.insert(0, str(WORKSPACE / "_FERRAMENTAS"))
from medina_visual_lint import lint_svg  # noqa: E402


REPRESENTATIVE_CASES = {
    "Azimut": "case-email-azimut-19f3ed5bdbdcf159",
    "CORSAN": "case-email-corsan-agerst-19f3dc9ff92081cd",
    "Libra Sul": "case-email-libra-sul-agint-stj-19f3c9350d875062",
    "Natura": "case-email-natura-cabreuva-19f3991ebc75fe03",
    "Patrícia/Fábio": "case-email-patricia-fabio-memoriais-19f3c68ee6d8fef2",
    "Plano de Saúde": "case-email-auto-19f3f25cb64df962",
}


def _phase_number(value: object) -> int | None:
    match = re.match(r"^F(10|[0-9])(?:_|$)", str(value or ""))
    return int(match.group(1)) if match else None


def _phase_regressions(history: list[dict]) -> list[dict]:
    regressions = []
    highest = -1
    previous = None
    for index, entry in enumerate(history):
        phase = str((entry or {}).get("phase") or "")
        current = _phase_number(phase)
        if current is None:
            continue
        if current < highest:
            regressions.append({
                "index": index,
                "from": previous,
                "to": phase,
                "highestPhaseNumber": highest,
                "at": (entry or {}).get("at"),
            })
        highest = max(highest, current)
        previous = phase
    return regressions


def _artifact_candidates(case_dir: Path, raw: str, state_root: Path) -> list[Path]:
    path = Path(raw)
    if path.is_absolute():
        return [path]
    return [case_dir / path, state_root / path, WORKSPACE / path]


def _artifact_audit(case_dir: Path, legacy: dict, state_root: Path) -> dict:
    found, missing = [], []
    for raw in legacy.get("artifacts") or []:
        if not isinstance(raw, str) or not raw.strip():
            missing.append({"declared": raw, "reason": "invalid_path"})
            continue
        candidates = _artifact_candidates(case_dir, raw, state_root)
        actual = next((path for path in candidates if path.is_file()), None)
        if actual:
            found.append({"declared": raw, "path": str(actual), "sha256": sha256_file(actual)})
        else:
            missing.append({"declared": raw, "candidates": [str(path) for path in candidates]})
    return {"declared": len(legacy.get("artifacts") or []), "found": found, "missing": missing}


def _json_audit(case_dir: Path) -> list[dict]:
    invalid = []
    for path in sorted(case_dir.rglob("*.json")):
        try:
            json.loads(path.read_text(encoding="utf-8-sig"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            invalid.append({"path": str(path), "error": str(exc)})
    return invalid


def _visual_roots(case_dir: Path, legacy: dict) -> list[Path]:
    roots = [case_dir]
    case_folder = Path(str((legacy.get("inputs") or {}).get("caseFolder") or ""))
    if case_folder.is_dir() and case_folder.resolve() != case_dir.resolve():
        roots.append(case_folder)
    return roots


def _visual_audit(case_dir: Path, legacy: dict, *, deep: bool) -> dict:
    if not deep:
        return {"status": "not_in_corpus", "files": [], "failed": 0, "findings": 0}
    paths: dict[str, Path] = {}
    for root in _visual_roots(case_dir, legacy):
        for path in root.rglob("*.svg"):
            paths[str(path.resolve()).lower()] = path
    results = [lint_svg(path) for path in sorted(paths.values(), key=lambda item: str(item).lower())]
    return {
        "status": "pass" if results and all(item["approved"] for item in results) else "blocked" if results else "not_found",
        "files": results,
        "failed": sum(not item["approved"] for item in results),
        "findings": sum(len(item.get("findings") or []) for item in results),
    }


def replay_case(case_dir: Path, *, label: str | None, state_root: Path) -> dict:
    state_path = case_dir / "FORJA_STATE.json"
    before_hash = sha256_file(state_path)
    legacy = read_json(state_path, None)
    if not isinstance(legacy, dict):
        return {"caseId": case_dir.name, "label": label, "status": "invalid_legacy_state"}
    with tempfile.TemporaryDirectory(prefix="forja-n3-replay-") as temp:
        shadow_case = Path(temp) / case_dir.name
        shadow_case.mkdir()
        shutil.copy2(state_path, shadow_case / "FORJA_STATE.json")
        initialize_case(shadow_case, from_legacy=True)
        derived = derive_state(shadow_case)
        replay_ok = (
            (derived.get("legacy") or {}).get("sourceHash")
            and derived.get("phaseCursor") == legacy.get("currentPhase")
            and derived.get("lifecycleStatus") == legacy.get("status")
        )

    regressions = _phase_regressions(legacy.get("phaseHistory") or [])
    artifacts = _artifact_audit(case_dir, legacy, state_root)
    invalid_json = _json_audit(case_dir)
    pending_sources = [
        entry for entry in legacy.get("sourceLedger") or []
        if isinstance(entry, dict) and entry.get("finalUseAllowed") is False
    ]
    has_review_product = str(legacy.get("status") or "") in {
        "draft_awaiting_review", "ready_for_review", "sent_confirmed", "fulfilled"
    }
    visual = _visual_audit(case_dir, legacy, deep=label is not None)
    blockers = []
    if regressions:
        blockers.append("silent_phase_regression")
    if pending_sources and has_review_product:
        blockers.append("pending_source_in_review_cycle")
    if invalid_json:
        blockers.append("invalid_json")
    if artifacts["missing"]:
        blockers.append("declared_artifact_missing")
    if visual["status"] == "blocked":
        blockers.append("visual_gate_failed")
    if not replay_ok:
        blockers.append("legacy_state_import_divergence")
    after_hash = sha256_file(state_path)
    if before_hash != after_hash:
        blockers.append("original_state_changed")
    return {
        "caseId": case_dir.name,
        "label": label,
        "status": "blocked" if blockers else "compatible",
        "legacy": {
            "phase": legacy.get("currentPhase"),
            "lifecycle": legacy.get("status"),
            "historyEntries": len(legacy.get("phaseHistory") or []),
            "sourceLedgerEntries": len(legacy.get("sourceLedger") or []),
        },
        "shadowImport": {
            "ok": bool(replay_ok),
            "derivedPhase": derived.get("phaseCursor"),
            "derivedLifecycle": derived.get("lifecycleStatus"),
            "revision": derived.get("revision"),
        },
        "immutability": {"beforeSha256": before_hash, "afterSha256": after_hash, "preserved": before_hash == after_hash},
        "phaseRegressions": regressions,
        "pendingSources": pending_sources,
        "artifacts": artifacts,
        "invalidJson": invalid_json,
        "visual": visual,
        "blockers": blockers,
    }


def _render_markdown(report: dict) -> str:
    summary = report["summary"]
    rows = []
    for case in report["cases"]:
        rows.append(
            f"| {case.get('label') or case['caseId']} | {case['status']} | "
            f"{len(case.get('phaseRegressions') or [])} | {len(case.get('pendingSources') or [])} | "
            f"{len((case.get('artifacts') or {}).get('missing') or [])} | "
            f"{(case.get('visual') or {}).get('failed', 0)} | "
            f"{', '.join(case.get('blockers') or []) or '-'} |"
        )
    return "\n".join([
        "# FORJA N3 — RELATÓRIO DE REPLAY EM SOMBRA",
        "",
        f"Gerado em: `{report['generatedAt']}`  ",
        f"Modo: `{report['mode']}` — os estados e as peças originais não foram alterados.",
        "",
        "## Resultado consolidado",
        "",
        f"- Estados N2 reproduzidos: **{summary['replayed']}/{summary['total']}**.",
        f"- Estados originais preservados por hash: **{summary['immutable']}/{summary['total']}**.",
        f"- Casos compatíveis sem bloqueio: **{summary['compatible']}**.",
        f"- Casos em que a N3 abriu bloqueio explícito: **{summary['blocked']}**.",
        f"- Diagramas examinados no corpus: **{summary['visualFiles']}**, reprovados: **{summary['visualFailed']}**.",
        "",
        "Bloqueio no replay não altera a peça histórica. Ele demonstra que o fluxo novo interromperia a promoção até correção ou decisão humana registrada.",
        "",
        "## Casos",
        "",
        "| Caso | Resultado N3 | Regressões | Fontes pendentes | Artefatos ausentes | SVGs reprovados | Motivos |",
        "|---|---:|---:|---:|---:|---:|---|",
        *rows,
        "",
        "## Limites desta execução",
        "",
        "- O replay comprova importação, imutabilidade, consistência estrutural, referências de arquivos e lint dos SVGs disponíveis.",
        "- Ele não transforma retrospectivamente estados N2 em prova de cobertura por página; casos sem cadernos de contexto N3 permanecem sem essa comprovação.",
        "- A promoção como padrão continua dependente de três ciclos novos completos, conforme o critério de aceitação do plano.",
        "",
    ])


def run_replay(state_root: Path, output_json: Path, output_md: Path) -> dict:
    cases = []
    reverse = {case_id: label for label, case_id in REPRESENTATIVE_CASES.items()}
    for case_dir in sorted(path for path in state_root.iterdir() if path.is_dir() and (path / "FORJA_STATE.json").is_file()):
        cases.append(replay_case(case_dir, label=reverse.get(case_dir.name), state_root=state_root))
    summary = {
        "total": len(cases),
        "replayed": sum((case.get("shadowImport") or {}).get("ok") is True for case in cases),
        "immutable": sum((case.get("immutability") or {}).get("preserved") is True for case in cases),
        "compatible": sum(case.get("status") == "compatible" for case in cases),
        "blocked": sum(case.get("status") == "blocked" for case in cases),
        "visualFiles": sum(len((case.get("visual") or {}).get("files") or []) for case in cases),
        "visualFailed": sum((case.get("visual") or {}).get("failed") or 0 for case in cases),
        "representativeFound": sum(case.get("label") is not None for case in cases),
    }
    report = {
        "schemaVersion": 1,
        "specVersion": "N3.0-r2",
        "generatedAt": now_iso(),
        "mode": "shadow_readonly_copy",
        "stateRoot": str(state_root),
        "summary": summary,
        "cases": cases,
    }
    atomic_write_json(output_json, report)
    atomic_write_text(output_md, _render_markdown(report))
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Replay imutável N2 -> N3 e corpus visual")
    parser.add_argument("--state-root", type=Path, default=FORJA / "state")
    parser.add_argument("--output-json", type=Path, default=FORJA / "reports" / "N3_SHADOW_REPLAY_2026-07-09.json")
    parser.add_argument("--output-md", type=Path, default=FORJA / "reports" / "N3_SHADOW_REPLAY_2026-07-09.md")
    args = parser.parse_args()
    report = run_replay(args.state_root.resolve(), args.output_json, args.output_md)
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
