"""Discriminating anti-fraud evaluator for real N4 artifacts and adversarial mutations."""

from __future__ import annotations

import copy
import json
import statistics
from pathlib import Path

import forja_acervo

from forja_n3_common import FORJA, atomic_write_json, now_iso, read_json, sha256_file
from forja_n4_e2e_adversarial import run as run_e2e


WEIGHTS = {"provenance": 0.30, "temporal_honesty": 0.20, "mutation_discrimination": 0.25, "measured_consistency": 0.15, "management_truth": 0.10}
CASES = [
    forja_acervo.caso("CASO-19"),
    forja_acervo.caso("CASO-16"),
    "case-email-auto-19f3f25cb64df962",
    forja_acervo.caso("CASO-04"),
]


def _snapshot(case_dir: Path, sidecar: dict) -> dict:
    manifest = read_json(case_dir / "FORJA_CASE_MANIFEST.json", {}) or {}
    artifacts = case_dir / "n4_artifacts"
    validation = read_json(artifacts / "N4_VALIDATION.json", {}) or {}
    demand_id = str(manifest.get("demandId") or case_dir.name.removeprefix("case-"))
    return {
        "label": case_dir.name,
        "registry": manifest.get("n4SourceRegistry") or {},
        "suite": read_json(artifacts / "F4_CASE_ACCEPTANCE_TESTS.json", {}) or {},
        "results": read_json(artifacts / "F7_CASE_TEST_RESULTS.json", {}) or {},
        "global": read_json(artifacts / "F7_GLOBAL_CONSISTENCY.json", {}) or {},
        "validation": validation,
        "management": (sidecar.get("items") or {}).get(demand_id) or {},
        "adversarial": False,
    }


def evaluate(snapshot: dict) -> dict:
    registry = snapshot.get("registry") or {}
    verifiable = 0
    active = 0
    provenance_findings = []
    for source_id, raw in registry.items():
        if not isinstance(raw, dict):
            provenance_findings.append(f"{source_id}:opaque")
            continue
        if raw.get("status", "active") != "active":
            provenance_findings.append(f"{source_id}:{raw.get('status')}")
            continue
        active += 1
        path = Path(str(raw.get("path") or ""))
        digest = str(raw.get("sha256") or raw.get("hash") or "")
        if path.is_file() and digest and sha256_file(path) == digest:
            verifiable += 1
        else:
            provenance_findings.append(f"{source_id}:unverifiable")
    provenance = 100.0 * verifiable / active if active else 0.0

    suite = snapshot.get("suite") or {}
    mode = suite.get("executionMode") or "legacy"
    if mode == "retrospective_baseline":
        temporal = 100.0 if suite.get("draftedBeforeFinalText") is False and suite.get("retrospectiveReason") else 0.0
    elif mode == "prospective":
        temporal = 100.0 if suite.get("draftedBeforeFinalText") is True and suite.get("frozenAt") and suite.get("finalProducedAt") and str(suite["frozenAt"]) < str(suite["finalProducedAt"]) else 0.0
    else:
        temporal = 25.0 if suite.get("draftedBeforeFinalText") is True else 0.0

    anti_fraud = (snapshot.get("results") or {}).get("antiFraud") or {}
    mutation = 100.0 * float(anti_fraud.get("mutationScore") or 0.0) if int(anti_fraud.get("total") or 0) > 0 else 0.0

    global_payload = snapshot.get("global") or {}
    measured_layers = 0
    if global_payload.get("measurementContract") == "N4-MEASURED-v1":
        for layer in ("C1", "C2", "C3", "C4", "C5"):
            evidence = ((global_payload.get("layerEvidence") or {}).get(layer) or {})
            checks = evidence.get("checks") or []
            if evidence.get("measuredAt") and checks and all(item.get("passed") is True and item.get("evidence") for item in checks):
                measured_layers += 1
    consistency = measured_layers * 20.0

    validation = snapshot.get("validation") or {}
    management_n4 = ((snapshot.get("management") or {}).get("n4") or {})
    approval_match = management_n4.get("approved") == validation.get("approved")
    promotion_match = management_n4.get("promotionEligible") == validation.get("promotionEligible")
    management = 50.0 * approval_match + 50.0 * promotion_match

    dimensions = {"provenance": provenance, "temporal_honesty": temporal, "mutation_discrimination": mutation, "measured_consistency": consistency, "management_truth": management}
    score = sum(dimensions[key] * WEIGHTS[key] for key in WEIGHTS)
    p1 = []
    if provenance < 100:
        p1.append("source_provenance_not_fully_verifiable")
    if temporal < 100:
        p1.append("test_timing_not_proven")
    if mutation < 80:
        p1.append("mutation_score_below_80")
    if consistency < 100:
        p1.append("global_layers_not_measured")
    if management < 100:
        p1.append("management_validation_mismatch")
    verdict = "BLOCKED" if p1 else "APPROVED" if score >= 80 else "ACCEPTABLE" if score >= 65 else "REJECTED"
    return {"label": snapshot.get("label"), "adversarial": snapshot.get("adversarial", False), "dimensions": dimensions, "score": round(score, 2), "p1": p1, "verdict": verdict, "provenanceFindings": provenance_findings}


def run() -> dict:
    sidecar = read_json(FORJA.parent / "gestao_escritorio" / "data" / "forja_status.json", {}) or {}
    snapshots = [_snapshot(FORJA / "state" / case_id, sidecar) for case_id in CASES]
    base = copy.deepcopy(snapshots[2])
    adversarials = []

    opaque = copy.deepcopy(base)
    opaque.update(label="ADV-opaque-source", adversarial=True)
    opaque["registry"] = {"fake": "f" * 64}
    adversarials.append(opaque)

    timing = copy.deepcopy(base)
    timing.update(label="ADV-retrospective-lie", adversarial=True)
    timing["suite"]["draftedBeforeFinalText"] = True
    adversarials.append(timing)

    mutation = copy.deepcopy(base)
    mutation.update(label="ADV-no-mutation", adversarial=True)
    mutation["results"]["antiFraud"] = {"mutationScore": 0, "killed": 0, "total": 10}
    adversarials.append(mutation)

    hardcoded = copy.deepcopy(base)
    hardcoded.update(label="ADV-hardcoded-layers", adversarial=True)
    hardcoded["global"].pop("layerEvidence", None)
    adversarials.append(hardcoded)

    stale = copy.deepcopy(base)
    stale.update(label="ADV-stale-management", adversarial=True)
    stale["management"]["n4"]["approved"] = not bool(stale["validation"].get("approved"))
    stale["management"]["n4"]["promotionEligible"] = not bool(stale["validation"].get("promotionEligible"))
    adversarials.append(stale)

    evaluations = [evaluate(item) for item in snapshots + adversarials]
    scenario_dispersion = {dimension: round(statistics.pstdev([item["dimensions"][dimension] for item in evaluations]), 2) for dimension in WEIGHTS}
    discriminating_weight = sum(weight for dimension, weight in WEIGHTS.items() if scenario_dispersion[dimension] >= 10)
    real_new = evaluations[:3]
    adversarial_evals = evaluations[len(snapshots):]
    expected = ["APPROVED", "APPROVED", "APPROVED", "BLOCKED"] + ["BLOCKED"] * len(adversarial_evals)
    observed = ["APPROVED" if item["verdict"] == "APPROVED" else "BLOCKED" for item in evaluations]
    confusion = {
        "validAccepted": sum(e == "APPROVED" and o == "APPROVED" for e, o in zip(expected, observed)),
        "validBlocked": sum(e == "APPROVED" and o == "BLOCKED" for e, o in zip(expected, observed)),
        "invalidBlocked": sum(e == "BLOCKED" and o == "BLOCKED" for e, o in zip(expected, observed)),
        "invalidAccepted": sum(e == "BLOCKED" and o == "APPROVED" for e, o in zip(expected, observed)),
    }
    e2e = run_e2e()
    approved = (
        all(item["verdict"] == "APPROVED" for item in real_new)
        and all(item["verdict"] != "APPROVED" for item in adversarial_evals)
        and confusion["invalidAccepted"] == 0
        and confusion["validBlocked"] == 0
        and discriminating_weight >= 0.70
        and e2e.get("approved") is True
    )
    report = {
        "schemaVersion": 1,
        "generatedAt": now_iso(),
        "evaluatorVersion": "N4-ANTI-FRAUD-v2",
        "weights": WEIGHTS,
        "corpus": {"real": len(snapshots), "adversarial": len(adversarials), "total": len(evaluations)},
        "scenarioDispersion": scenario_dispersion,
        "operationalVarianceMeasured": False,
        "metricNames": {
            "provenance": "source_registry_physical_integrity",
            "mutation_discrimination": "literal_mutation_coverage",
            "measured_consistency": "declared_layers_with_replay_support",
        },
        "methodLimitations": [
            "scenarioDispersion mede separação entre cenários escolhidos, não variância operacional",
            "mutation_discrimination cobre mutações literais; mutação semântica continua requisito separado de promoção",
            "integridade física de fonte não equivale a sustentação jurídica da proposição",
        ],
        "scope": "mechanical_integrity_and_self_certification_resistance",
        "doesNotAssess": ["legal_release", "merits_accuracy", "council_approval", "protocol_readiness"],
        "discriminatingWeight": discriminating_weight,
        "confusionMatrix": confusion,
        "e2eAntiSelfCertification": {"suite": e2e.get("suite"), "passed": e2e.get("passed"), "total": e2e.get("total"), "approved": e2e.get("approved")},
        "evaluations": evaluations,
        "approved": approved,
    }
    output = FORJA / "telemetria" / "N4_ANTI_FRAUD_AUDIT_2026-07-11.json"
    atomic_write_json(output, report)
    report_output = FORJA / "reports" / "N4_ANTI_FRAUD_AUDIT_RESULT.json"
    atomic_write_json(report_output, report)
    report["output"] = str(output)
    report["reportOutput"] = str(report_output)
    return report


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
