"""Registro sanitizado de lições pós-protocolo promovidas.

O registro contém somente identificadores, escopo e comportamento de teste.
Nenhum trecho da peça ou do e-mail entra nele.
"""

from __future__ import annotations

from pathlib import Path

from forja_n3_common import (
    FORJA,
    InterProcessLock,
    atomic_write_json,
    canonical_hash,
    now_iso,
    read_json,
    sha256_file,
)
from forja_n4_common import issue


REGISTRY_PATH = FORJA / "learning_registry" / "ACTIVE_RULES.json"


def _load() -> dict:
    return read_json(REGISTRY_PATH, {"schemaVersion": 1, "rules": []}) or {
        "schemaVersion": 1,
        "rules": [],
    }


def register_promoted_rule(
    *,
    source_case_id: str,
    candidate: dict,
    scope_key: str | None,
) -> dict:
    fixture_path = Path(candidate["fixtureId"]).resolve()
    execution_path = Path(candidate["testExecutionPath"]).resolve()
    try:
        fixture_id = str(fixture_path.relative_to(FORJA))
    except ValueError:
        fixture_id = fixture_path.name
    raw_test_id = str(candidate["testId"])
    test_path, separator, selector = raw_test_id.partition("::")
    try:
        relative_test = str(Path(test_path).resolve().relative_to(FORJA))
    except ValueError:
        relative_test = Path(test_path).name
    rule = {
        "ruleId": f"rule-{candidate['candidateId']}",
        "candidateId": candidate["candidateId"],
        "sourceCaseId": source_case_id,
        "scope": candidate["scope"],
        "scopeKey": scope_key or source_case_id,
        "layer": candidate["layer"],
        "cause": candidate["cause"],
        "impact": candidate["impact"],
        "behaviorCode": f"require_regression_test:{candidate['layer']}",
        "fixtureId": fixture_id,
        "testId": relative_test + (separator + selector if separator else ""),
        "testExecutionHash": sha256_file(execution_path),
        "approvedBy": candidate["approvedBy"],
        "active": True,
        "promotedAt": candidate["promotedAt"],
    }
    rule["ruleHash"] = canonical_hash(rule)
    with InterProcessLock(REGISTRY_PATH.with_suffix(".lock"), timeout=15, stale_after=900):
        payload = _load()
        by_id = {item["ruleId"]: item for item in payload.get("rules") or []}
        by_id[rule["ruleId"]] = rule
        payload["rules"] = sorted(by_id.values(), key=lambda item: item["ruleId"])
        payload["updatedAt"] = now_iso()
        payload["contentHash"] = canonical_hash({
            key: value for key, value in payload.items() if key not in {"contentHash", "updatedAt"}
        })
        atomic_write_json(REGISTRY_PATH, payload)
    return rule


def active_rules(*, case_id: str, product_type: str | None = None, tribunal: str | None = None) -> list[dict]:
    result = []
    for rule in _load().get("rules") or []:
        if not rule.get("active"):
            continue
        scope = rule.get("scope")
        key = rule.get("scopeKey")
        applies = (
            (scope == "case" and key == case_id)
            or (scope == "product_type" and product_type and key == product_type)
            or (scope == "tribunal" and tribunal and key == tribunal)
            or scope in {"office", "global"}
        )
        if applies:
            result.append(rule)
    return result


def suite_learning_findings(case_dir: Path, suite: dict) -> list[dict]:
    classification = read_json(case_dir / "n4_artifacts" / "F2_N4_CLASSIFICATION.json", {}) or {}
    product_type = str(classification.get("product") or "") or None
    manifest = read_json(case_dir / "FORJA_CASE_MANIFEST.json", {}) or {}
    tribunal = str(manifest.get("tribunal") or "") or None
    rules = active_rules(case_id=case_dir.name, product_type=product_type, tribunal=tribunal)
    covered = {
        str(test.get("learningCandidateId"))
        for test in suite.get("tests") or []
        if test.get("learningCandidateId")
    }
    return [
        issue(
            "PP-LEARNING-NOT-APPLIED",
            f"suíte prospectiva não cobre a lição promovida {rule['candidateId']}",
        )
        for rule in rules
        if rule["candidateId"] not in covered
    ]
