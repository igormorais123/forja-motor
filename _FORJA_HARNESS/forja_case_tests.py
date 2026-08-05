"""Versioned, hash-bound case-specific acceptance tests for FORJA N4."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path

from forja_n3_common import atomic_write_json, canonical_hash, resolve_case_dir, sha256_file
from forja_n4_common import ids_unique, issue, validate_file


SEVERITIES = {"blocking", "review_required", "informational"}
METHODS = {"deterministic", "semantic_independent", "deterministic_plus_semantic"}


def suite_hash(payload: dict) -> str:
    tests = []
    for raw in payload.get("tests") or []:
        tests.append({key: value for key, value in raw.items() if key not in {"status", "result", "executedAt"}})
    timing = {
        key: payload.get(key)
        for key in (
            "executionMode",
            "draftedBeforeFinalText",
            "frozenAt",
            "finalProducedAt",
            "retrospectiveReason",
        )
        if key in payload
    }
    return canonical_hash({"suiteId": payload.get("suiteId"), "timing": timing, "tests": tests})


def _parse_aware_iso(value: object) -> datetime | None:
    raw = str(value or "").strip()
    if not raw:
        return None
    try:
        parsed = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None and parsed.utcoffset() is not None else None


def validate_suite(payload: dict) -> list[dict]:
    tests = payload.get("tests") or []
    findings = ids_unique(tests, "testId", "N4-TEST-ID")
    execution_mode = payload.get("executionMode") or "legacy"
    if execution_mode not in {"legacy", "prospective", "retrospective_baseline"}:
        findings.append(issue("N4-TEST-MODE", "modo temporal da suíte inválido"))
    elif execution_mode == "legacy":
        if payload.get("draftedBeforeFinalText") is not True:
            findings.append(issue("N4-TEST-TIMING", "testes não foram congelados antes do texto final"))
    elif execution_mode == "prospective":
        if payload.get("draftedBeforeFinalText") is not True:
            findings.append(issue("N4-TEST-TIMING", "testes prospectivos não foram congelados antes do texto final"))
        frozen_at = _parse_aware_iso(payload.get("frozenAt"))
        final_at = _parse_aware_iso(payload.get("finalProducedAt"))
        if not frozen_at or not final_at:
            findings.append(issue("N4-TEST-TIMING-EVIDENCE", "suíte prospectiva sem datas de congelamento e produção final"))
        elif frozen_at >= final_at:
            findings.append(issue("N4-TEST-TIMING-ORDER", "congelamento dos testes não antecede a produção final"))
    else:
        if payload.get("draftedBeforeFinalText") is not False:
            findings.append(issue("N4-TEST-RETRO-HONESTY", "baseline retrospectiva não pode declarar testes anteriores ao texto"))
        if not str(payload.get("retrospectiveReason") or "").strip():
            findings.append(issue("N4-TEST-RETRO-REASON", "baseline retrospectiva sem justificativa"))
    if not 10 <= len(tests) <= 25 and not str(payload.get("countJustification") or "").strip():
        findings.append(issue("N4-TEST-COUNT", f"suite possui {len(tests)} testes; desvio exige justificativa", severity="p1"))
    for test in tests:
        tid = str(test.get("testId") or "?")
        if test.get("severity") not in SEVERITIES:
            findings.append(issue("N4-TEST-SEVERITY", f"{tid}: severidade inválida"))
        if test.get("method") not in METHODS:
            findings.append(issue("N4-TEST-METHOD", f"{tid}: método inválido"))
        if not test.get("evidenceRequired"):
            findings.append(issue("N4-TEST-EVIDENCE", f"{tid}: teste sem evidência exigida"))
        if test.get("supersedesTestId") and not all(test.get(key) for key in ("changeReason", "changeAuthor", "previousHash")):
            findings.append(issue("N4-TEST-VERSION", f"{tid}: alteração sem razão, autor e hash anterior"))
    declared = payload.get("suiteHash")
    if declared and declared != suite_hash(payload):
        findings.append(issue("N4-TEST-HASH", "suiteHash diverge dos critérios atuais"))
    return findings


def _deterministic(test: dict, text: str) -> tuple[str, str]:
    evaluator = test.get("evaluator") or {}
    kind = evaluator.get("kind")
    value = str(evaluator.get("value") or "")
    flags = re.I if evaluator.get("ignoreCase", True) else 0
    if not kind:
        return "requires_semantic_review", "teste sem avaliador determinístico"
    if kind == "contains":
        ok = value.casefold() in text.casefold() if flags else value in text
    elif kind == "not_contains":
        ok = value.casefold() not in text.casefold() if flags else value not in text
    elif kind == "regex_present":
        ok = re.search(value, text, flags) is not None
    elif kind == "regex_absent":
        ok = re.search(value, text, flags) is None
    else:
        return "invalid", f"avaliador desconhecido: {kind}"
    return ("pass", "critério satisfeito") if ok else ("fail", "critério não satisfeito")


def run_suite(suite: dict, draft_path: Path, *, reviewer_run_id: str, producer_run_id: str | None = None) -> dict:
    findings = validate_suite(suite)
    if producer_run_id and producer_run_id == reviewer_run_id:
        findings.append(issue("N4-TEST-SELF-REVIEW", "resultado avaliado pela mesma execução produtora"))
    text = draft_path.read_text(encoding="utf-8-sig", errors="replace")
    results = []
    for test in suite.get("tests") or []:
        method = test.get("method")
        status, detail = _deterministic(test, text) if method in {"deterministic", "deterministic_plus_semantic"} else ("requires_semantic_review", "avaliação semântica independente necessária")
        results.append({"testId": test.get("testId"), "severity": test.get("severity"), "status": status, "detail": detail})
        if test.get("severity") == "blocking" and status != "pass":
            findings.append(issue("N4-TEST-BLOCKING", f"{test.get('testId')}: {detail}"))
    mutations = []
    for test in suite.get("tests") or []:
        if test.get("severity") != "blocking" or test.get("method") not in {"deterministic", "deterministic_plus_semantic"}:
            continue
        evaluator = test.get("evaluator") or {}
        kind = evaluator.get("kind")
        value = str(evaluator.get("value") or "")
        if not value or kind not in {"contains", "not_contains"}:
            continue
        if kind == "contains":
            mutated = re.sub(re.escape(value), "__FORJA_MUTATION__", text, flags=re.I if evaluator.get("ignoreCase", True) else 0)
            applicable = mutated != text
        else:
            mutated = text + "\n" + value
            applicable = True
        killed = False
        if applicable:
            for candidate in suite.get("tests") or []:
                if candidate.get("severity") != "blocking" or candidate.get("method") not in {"deterministic", "deterministic_plus_semantic"}:
                    continue
                candidate_status, _ = _deterministic(candidate, mutated)
                if candidate_status != "pass":
                    killed = True
                    break
        mutations.append({"mutationId": f"MUT-{test.get('testId')}", "targetTestId": test.get("testId"), "kind": kind, "applicable": applicable, "killed": killed})
    applicable_mutations = [item for item in mutations if item["applicable"]]
    killed_count = sum(item["killed"] for item in applicable_mutations)
    mutation_score = killed_count / len(applicable_mutations) if applicable_mutations else 0.0
    if applicable_mutations and mutation_score < 0.8:
        findings.append(issue("N4-TEST-MUTATION-SCORE", f"suíte matou {killed_count}/{len(applicable_mutations)} mutações ({mutation_score:.1%})"))
    return {
        "suiteHash": suite_hash(suite),
        "draftHash": sha256_file(draft_path),
        "reviewerRunId": reviewer_run_id,
        "results": results,
        "approved": not any(item["severity"] == "p0" for item in findings),
        "findings": findings,
        "antiFraud": {"mutationScore": mutation_score, "killed": killed_count, "total": len(applicable_mutations), "survivors": [item for item in applicable_mutations if not item["killed"]], "mutations": mutations},
    }


def validate_results(payload: dict, suite: dict | None = None, draft_path: Path | None = None) -> list[dict]:
    findings = []
    if suite and payload.get("suiteHash") != suite_hash(suite):
        findings.append(issue("N4-TEST-STALE-SUITE", "resultados usam versão anterior da suite"))
    if draft_path and (not draft_path.is_file() or payload.get("draftHash") != sha256_file(draft_path)):
        findings.append(issue("N4-TEST-STALE-DRAFT", "resultados usam texto diferente do atual"))
    for result in payload.get("results") or []:
        if result.get("severity") == "blocking" and result.get("status") != "pass":
            findings.append(issue("N4-TEST-RESULT", f"teste bloqueante não aprovado: {result.get('testId')}"))
    anti_fraud = payload.get("antiFraud") or {}
    requires_mutation = isinstance(suite, dict) and suite.get("executionMode") in {"prospective", "retrospective_baseline"}
    killed = int(anti_fraud.get("killed") or 0)
    total = int(anti_fraud.get("total") or 0)
    score = float(anti_fraud.get("mutationScore") or 0)
    expected_score = killed / total if total else 0.0
    if killed < 0 or total < 0 or killed > total or not 0 <= score <= 1 or abs(score - expected_score) > 1e-9:
        findings.append(issue("N4-TEST-MUTATION-INCONSISTENT", "contagens e mutationScore são matematicamente inconsistentes"))
    mutations = anti_fraud.get("mutations") or []
    applicable = [item for item in mutations if item.get("applicable") is True]
    if mutations and (len(applicable) != total or sum(item.get("killed") is True for item in applicable) != killed):
        findings.append(issue("N4-TEST-MUTATION-DETAIL", "resumo de mutações diverge dos resultados individuais"))
    if requires_mutation and (total < 1 or score < 0.8):
        findings.append(issue("N4-TEST-MUTATION-MISSING", "resultado sem mutation testing discriminante aprovado"))
    suite_ids = [str(item.get("testId") or "") for item in (suite or {}).get("tests") or []]
    result_ids = [str(item.get("testId") or "") for item in payload.get("results") or []]
    if suite and result_ids != suite_ids:
        findings.append(issue("N4-TEST-RESULT-SET", "resultados não correspondem, na mesma ordem, aos testes congelados"))
    return findings


def main() -> None:
    parser = argparse.ArgumentParser(description="Executa TDD jurídico do caso FORJA N4")
    parser.add_argument("case")
    parser.add_argument("draft", type=Path)
    parser.add_argument("--reviewer-run-id", required=True)
    parser.add_argument("--producer-run-id")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    case_dir = resolve_case_dir(args.case)
    suite, findings = validate_file(case_dir, "F4_CASE_ACCEPTANCE_TESTS.json", validate_suite)
    if not isinstance(suite, dict):
        result = {"approved": False, "findings": findings}
    else:
        result = run_suite(suite, args.draft, reviewer_run_id=args.reviewer_run_id, producer_run_id=args.producer_run_id)
        result["findings"] = findings + result["findings"]
        result["approved"] = not any(item["severity"] == "p0" for item in result["findings"])
    if args.output:
        atomic_write_json(args.output, result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
