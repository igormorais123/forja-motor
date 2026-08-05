"""Metacognitive audit rules for FORJA N4."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from forja_n3_common import resolve_case_dir
from forja_n4_common import ids_unique, issue, validate_file


def validate_metacognition(payload: dict) -> list[dict]:
    premises = payload.get("premises") or []
    findings = ids_unique(premises, "premiseId", "N4-META-PREMISE")
    for premise in premises:
        pid = str(premise.get("premiseId") or "?")
        status = premise.get("status")
        if status not in {"confirmed", "declared_not_confirmed", "contradicted", "preference", "objective"}:
            findings.append(issue("N4-META-STATUS", f"{pid}: estado inválido"))
        if status == "confirmed" and not premise.get("confirmedBySourceIds"):
            findings.append(issue("N4-META-NO-SOURCE", f"{pid}: premissa confirmada sem fonte"))
        if status == "declared_not_confirmed" and premise.get("usedInDraft") is True:
            findings.append(issue("N4-META-UNCONFIRMED", f"{pid}: declaração não confirmada usada como fato"))
    for check in payload.get("consensusChecks") or []:
        if int(check.get("agentsAgreeing") or 0) > 1 and int(check.get("independentSourceCount") or 0) <= 1:
            if check.get("verdict") != "shared_source_not_independent_consensus":
                findings.append(issue("N4-META-CONSENSUS", f"{check.get('issueId')}: concordância de agentes sem fontes independentes"))
    for change in payload.get("recommendationChanges") or []:
        if change.get("from") != change.get("to") and not change.get("reasonType"):
            findings.append(issue("N4-META-CHANGE", f"{change.get('recommendationId')}: mudança sem causa"))
    metrics = payload.get("metricChecks") or []
    for check in metrics:
        if check.get("improvedByRemovingHardQuestions") is True and check.get("verdict") != "gaming_detected":
            findings.append(issue("N4-META-GAMING", "métrica melhorou removendo questões difíceis"))
    if not str(payload.get("bestObjection") or "").strip():
        findings.append(issue("N4-META-OBJECTION", "auditoria sem melhor objeção", severity="p1"))
    if not str(payload.get("alternativeExplanation") or "").strip():
        findings.append(issue("N4-META-ALTERNATIVE", "auditoria sem explicação alternativa", severity="p1"))
    return findings


def validate_case(case_dir: Path) -> dict:
    _, findings = validate_file(case_dir, "F7_METACOGNITIVE_AUDIT.json", validate_metacognition)
    return {"approved": not any(x["severity"] == "p0" for x in findings), "findings": findings}


def main() -> None:
    parser = argparse.ArgumentParser(description="Valida auditoria metacognitiva FORJA N4")
    parser.add_argument("case")
    args = parser.parse_args()
    print(json.dumps(validate_case(resolve_case_dir(args.case)), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
