"""End-to-end anti-self-certification checks against a real N4 baseline copy."""

from __future__ import annotations

import argparse
import json
import shutil
import tempfile
from pathlib import Path

import forja_acervo
from unittest.mock import patch

from forja_case_tests import suite_hash
from forja_n4_common import expected_content_hash
from forja_n4_validate import validate_case


ROOT = Path(__file__).resolve().parent
DEFAULT_CASE = ROOT / "state" / forja_acervo.caso("CASO-19")


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _save(path: Path, payload: dict) -> None:
    if "contentHash" in payload:
        payload["contentHash"] = expected_content_hash(payload)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _copy_case(source: Path, parent: Path) -> Path:
    target = parent / source.name
    shutil.copytree(source, target)
    return target


def _codes(report: dict) -> set[str]:
    return {str(item.get("code")) for item in report.get("findings") or []}


def run(source: Path = DEFAULT_CASE) -> dict:
    scenarios: list[dict] = []
    with tempfile.TemporaryDirectory(prefix="forja-n4-e2e-") as raw:
        workspace = Path(raw)

        control = _copy_case(source, workspace / "control")
        report = validate_case(control, write=False, mode_override="pilot_blocking")
        scenarios.append({"id": "valid_control", "blocked": not report["approved"], "passed": report["approved"], "codes": sorted(_codes(report))})

        benign = _copy_case(source, workspace / "benign-format")
        path = benign / "n4_artifacts" / "F7_CASE_TEST_RESULTS.json"
        payload = _load(path)
        path.write_text(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
        report = validate_case(benign, write=False, mode_override="pilot_blocking")
        scenarios.append({"id": "benign_json_reformat", "blocked": not report["approved"], "passed": report["approved"], "codes": sorted(_codes(report))})

        tampered = _copy_case(source, workspace / "score")
        path = tampered / "n4_artifacts" / "F7_CASE_TEST_RESULTS.json"
        payload = _load(path)
        payload["antiFraud"].update({"mutationScore": 999, "killed": 999, "total": 1})
        _save(path, payload)
        report = validate_case(tampered, write=False, mode_override="pilot_blocking")
        codes = _codes(report)
        scenarios.append({"id": "fabricated_mutation_score", "blocked": not report["approved"], "passed": "N4-TEST-MUTATION-INCONSISTENT" in codes and "N4-TEST-REEXECUTION-DRIFT" in codes, "codes": sorted(codes)})

        tampered = _copy_case(source, workspace / "semantic-score")
        path = tampered / "n4_artifacts" / "F7_CASE_TEST_RESULTS.json"
        payload = _load(path)
        payload["antiFraud"]["semanticMutationScore"] = 1.0
        _save(path, payload)
        report = validate_case(tampered, write=False, mode_override="pilot_blocking")
        codes = _codes(report)
        scenarios.append({"id": "fabricated_semantic_score", "blocked": not report["promotionEligible"], "passed": "N4-TEST-REEXECUTION-DRIFT" in codes and not report["promotionEligible"], "codes": sorted(codes)})

        tampered = _copy_case(source, workspace / "draft-hash")
        path = tampered / "n4_artifacts" / "F7_CASE_TEST_RESULTS.json"
        payload = _load(path)
        payload["draftHash"] = "f" * 64
        _save(path, payload)
        report = validate_case(tampered, write=False, mode_override="pilot_blocking")
        codes = _codes(report)
        scenarios.append({"id": "fabricated_draft_hash", "blocked": not report["approved"], "passed": "N4-TEST-DRAFT-UNRESOLVED" in codes, "codes": sorted(codes)})

        tampered = _copy_case(source, workspace / "empty-registry")
        manifest_path = tampered / "FORJA_CASE_MANIFEST.json"
        manifest = _load(manifest_path)
        manifest["n4SourceRegistry"] = {}
        _save(manifest_path, manifest)
        report = validate_case(tampered, write=False, mode_override="pilot_blocking")
        codes = _codes(report)
        scenarios.append({"id": "empty_source_registry", "blocked": not report["approved"], "passed": "N4-SOURCE-HASH" in codes and "N4-TEST-DRAFT-UNRESOLVED" in codes, "codes": sorted(codes)})

        tampered = _copy_case(source, workspace / "draft-status")
        path = tampered / "n4_artifacts" / "F2_QUESTION_TREE.json"
        payload = _load(path)
        payload["status"] = "draft"
        _save(path, payload)
        report = validate_case(tampered, write=False, mode_override="pilot_blocking")
        codes = _codes(report)
        scenarios.append({"id": "required_artifact_draft", "blocked": not report["approved"], "passed": "N4-ARTIFACT-STATUS" in codes, "codes": sorted(codes)})

        tampered = _copy_case(source, workspace / "global-evidence")
        path = tampered / "n4_artifacts" / "F7_GLOBAL_CONSISTENCY.json"
        payload = _load(path)
        sources = payload["layerEvidence"]["C1"]["checks"][0]["evidenceData"]["sources"]
        next(iter(sources.values()))["sha256"] = "0" * 64
        _save(path, payload)
        report = validate_case(tampered, write=False, mode_override="pilot_blocking")
        codes = _codes(report)
        scenarios.append({"id": "fabricated_global_evidence", "blocked": not report["approved"], "passed": "N4-GLOBAL-REPLAY-C1" in codes, "codes": sorted(codes)})

        tampered = _copy_case(source, workspace / "temporal")
        suite_path = tampered / "n4_artifacts" / "F4_CASE_ACCEPTANCE_TESTS.json"
        suite = _load(suite_path)
        previous_hash = suite_hash(suite)
        suite.update({"executionMode": "prospective", "draftedBeforeFinalText": True, "frozenAt": "2026-07-11T10:00:00-03:00", "finalProducedAt": "2026-07-11T11:00:00-03:00"})
        suite.pop("retrospectiveReason", None)
        suite["suiteHash"] = suite_hash(suite)
        _save(suite_path, suite)
        result_path = tampered / "n4_artifacts" / "F7_CASE_TEST_RESULTS.json"
        result = _load(result_path)
        result["suiteHash"] = suite["suiteHash"]
        _save(result_path, result)
        report = validate_case(tampered, write=False, mode_override="pilot_blocking")
        scenarios.append({"id": "retro_relabelled_prospective", "blocked": not report["approved"] or not report["promotionEligible"], "passed": previous_hash != suite["suiteHash"] and not report["promotionEligible"], "codes": sorted(_codes(report))})

        empty = workspace / "empty" / "case-empty"
        empty.mkdir(parents=True)
        with patch("forja_n4_validate.load_config", return_value={"features": {}, "n4": {"mode": "shadow"}}):
            report = validate_case(empty, target_phase="F0_RECONCILIACAO_FILA", write=False)
        scenarios.append({"id": "zero_artifacts", "blocked": not report["approved"], "passed": report.get("evaluationStatus") == "not_evaluated" and not report["approved"], "codes": sorted(_codes(report))})

    passed = sum(item["passed"] for item in scenarios)
    return {"schemaVersion": 1, "suite": "N4-E2E-ANTI-SELF-CERTIFICATION-v3", "sourceCase": source.name, "passed": passed, "total": len(scenarios), "approved": passed == len(scenarios), "scenarios": scenarios}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", type=Path, default=DEFAULT_CASE)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run(args.case)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report_output = ROOT / "reports" / "N4_E2E_ANTI_SELF_CERTIFICATION_2026-07-11.json"
    report_output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["approved"] else 1)


if __name__ == "__main__":
    main()
