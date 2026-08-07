"""Execute the immutable N4 regression corpus and write telemetry."""

from __future__ import annotations

import json

from forja_consistency import validate_comparison, validate_delivery, validate_event_identity, validate_global, validate_intertemporal, validate_quantification
from forja_n3_common import FORJA, atomic_write_json, now_iso, read_json
from forja_reasoning import validate_question_tree
from forja_science import validate_claims, validate_studies


VALIDATORS = {
    "comparison": validate_comparison,
    "delivery": validate_delivery,
    "event_identity": validate_event_identity,
    "global": validate_global,
    "intertemporal": validate_intertemporal,
    "quantification": validate_quantification,
    "question_tree": validate_question_tree,
    "science_claims": validate_claims,
    "science_studies": validate_studies,
}


def run() -> dict:
    source = FORJA / "n4_fixtures" / "N4_REGRESSION_CORPUS.json"
    corpus = read_json(source, {}) or {}
    results = []
    for fixture in corpus.get("fixtures") or []:
        validator = VALIDATORS[fixture["validator"]]
        findings = validator(fixture.get("payload") or {})
        codes = {item.get("code") for item in findings}
        missing = sorted(set(fixture.get("expectedCodes") or []) - codes)
        unexpected = sorted(set(fixture.get("expectedAbsent") or []) & codes)
        results.append({"id": fixture["id"], "class": fixture["class"], "passed": not missing and not unexpected, "codes": sorted(codes), "missingExpected": missing, "unexpected": unexpected})
    report = {
        "schemaVersion": 1,
        "specVersion": "N4.0-candidate",
        "generatedAt": now_iso(),
        "source": str(source),
        "fixtures": len(results),
        "passed": sum(item["passed"] for item in results),
        "failed": sum(not item["passed"] for item in results),
        "results": results,
    }
    stamp = now_iso().replace(":", "").replace("-", "")[:15]
    output = FORJA / "telemetria" / f"N4_CORPUS_{stamp}.json"
    atomic_write_json(output, report)
    report["output"] = str(output)
    return report


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
