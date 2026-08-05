"""Consolidated, evidence-based run metrics for a FORJA N3 case."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from forja_n3_common import PHASES, atomic_write_json, now_iso, read_json, resolve_case_dir
from forja_state_machine import derive_state, load_events


def _safe_ledger(path_value: str | None) -> dict:
    path = Path(path_value or "")
    if not path.is_file():
        return {}
    value = read_json(path, {})
    return value if isinstance(value, dict) else {}


def build_metrics(case_dir: Path) -> dict:
    events = load_events(case_dir)
    state = derive_state(case_dir, events)
    event_types = Counter(str(event.get("type") or "unknown") for event in events)
    attempts = Counter(
        str(event.get("phase")) for event in events
        if event.get("type") == "phase_started" and event.get("phase") in PHASES
    )
    blocked = Counter(
        str(event.get("phase")) for event in events
        if event.get("type") == "phase_blocked" and event.get("phase") in PHASES
    )
    artifacts = state.get("artifacts") or {}
    context_entry = artifacts.get("context_validation") or {}
    visual_entry = artifacts.get("f8_qa_ledger") or {}
    context = _safe_ledger(context_entry.get("path"))
    visual = _safe_ledger(visual_entry.get("path"))
    page_records = visual.get("pages") or []
    retries = {phase: max(0, attempts[phase] - 1) for phase in PHASES if attempts[phase]}
    n4_dir = case_dir / "n4_artifacts"
    n4_validation = _safe_ledger(str(n4_dir / "N4_VALIDATION.json"))
    question_tree = _safe_ledger(str(n4_dir / "F2_QUESTION_TREE.json"))
    coverage = _safe_ledger(str(n4_dir / "F4_COVERAGE_MATRIX.json"))
    graph = _safe_ledger(str(n4_dir / "F3_REASONING_GRAPH.json"))
    case_tests = _safe_ledger(str(n4_dir / "F7_CASE_TEST_RESULTS.json"))
    classification = _safe_ledger(str(n4_dir / "F2_N4_CLASSIFICATION.json"))
    studies = _safe_ledger(str(n4_dir / "F5C_STUDY_LEDGER.json"))
    question_counts = question_tree.get("coverage") or {}
    coverage_counts = Counter(str(item.get("status") or "unknown") for item in coverage.get("items") or [])
    test_counts = Counter(str(item.get("status") or "unknown") for item in case_tests.get("results") or [])
    study_rows = studies.get("studies") or []
    metrics = {
        "schemaVersion": 1,
        "specVersion": "N3.0-r2",
        "caseId": case_dir.name,
        "demandId": state.get("demandId"),
        "generatedAt": now_iso(),
        "eventRevision": state.get("revision"),
        "stateHash": state.get("stateHash"),
        "phaseCursor": state.get("phaseCursor"),
        "lifecycleStatus": state.get("lifecycleStatus"),
        "completedPhases": state.get("completedPhases") or [],
        "invalidatedPhases": state.get("invalidatedPhases") or [],
        "blockers": state.get("blockers") or [],
        "eventCounts": dict(sorted(event_types.items())),
        "attemptsByPhase": {phase: attempts[phase] for phase in PHASES if attempts[phase]},
        "retriesByPhase": retries,
        "blockedByPhase": {phase: blocked[phase] for phase in PHASES if blocked[phase]},
        "artifactCount": len(artifacts),
        "artifactIds": sorted(artifacts),
        "context": {
            "status": context.get("status") or ("not_run" if not context else "unknown"),
            "documents": context.get("documentsChecked"),
            "pages": context.get("pagesChecked"),
            "findings": len(context.get("findings") or []),
        },
        "visualQa": {
            "status": "pass" if visual.get("approved") is True else "blocked" if visual else "not_run",
            "pagesChecked": len(page_records),
            "findings": len(visual.get("findings") or []),
            "generatorRunId": visual.get("generatorRunId"),
            "reviewerRunId": visual.get("reviewerRunId"),
        },
        "closeCycle": {
            "packageCreated": bool(state.get("package")),
            "draftCreated": bool(state.get("draft")),
            "deliveryConfirmed": bool(state.get("deliveryEvidence")),
            "managementSync": (state.get("sync") or {}).get("status") or "never",
            "fulfilled": state.get("lifecycleStatus") == "fulfilled_by_forja_f10",
        },
        "n4": {
            "specVersion": n4_validation.get("specVersion") or "N4.0-candidate",
            "mode": n4_validation.get("mode") or "not_run",
            "validationHash": n4_validation.get("validationHash"),
            "approved": n4_validation.get("approved"),
            "blocksCurrentFlow": n4_validation.get("blocksCurrentFlow", False),
            "questions": {
                "total": question_counts.get("total", 0),
                "material": question_counts.get("material", 0),
                "answeredMaterial": question_counts.get("answeredMaterial", 0),
                "blockedMaterial": question_counts.get("blockedMaterial", 0),
            },
            "coverageByStatus": dict(sorted(coverage_counts.items())),
            "graph": {"nodes": len(graph.get("nodes") or []), "edges": len(graph.get("edges") or [])},
            "caseTestsByStatus": dict(sorted(test_counts.items())),
            "science": {
                "mode": ((classification.get("science") or {}).get("mode") or "not_run"),
                "studies": len(study_rows),
                "identityConfirmed": sum(((item.get("verification") or {}).get("identity") == "confirmed") for item in study_rows),
                "contentConfirmed": sum(((item.get("verification") or {}).get("content") == "confirmed") for item in study_rows),
                "editorialChecked": sum(((item.get("verification") or {}).get("correctionRetraction") == "checked") for item in study_rows),
            },
            "findingCounts": (n4_validation.get("counts") or {}),
            "artifactIds": sorted(path.name for path in n4_dir.glob("*.json")) if n4_dir.is_dir() else [],
        },
    }
    return metrics


def write_metrics(case_dir: Path, output: Path | None = None) -> dict:
    metrics = build_metrics(case_dir)
    path = output or (case_dir / "FORJA_RUN_METRICS.json")
    atomic_write_json(path, metrics)
    return metrics


def main() -> None:
    parser = argparse.ArgumentParser(description="Consolida métricas verificáveis de um ciclo FORJA N3")
    parser.add_argument("case")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    case_dir = resolve_case_dir(args.case)
    print(json.dumps(write_metrics(case_dir, args.output), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
