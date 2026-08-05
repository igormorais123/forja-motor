"""Hash-preserving invalidation graph for FORJA N4 artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from forja_n3_common import read_json, resolve_case_dir
from forja_n4_common import append_trace, write_artifact
from forja_state_machine import derive_state, record_event


DEPENDENCIES = {
    "source_document": ["F3_EVENT_IDENTITY.json", "F3_DOCUMENT_COMPARISON.json", "F3_REASONING_GRAPH.json", "F3_CONDUCT_LEDGER.json", "F4_COVERAGE_MATRIX.json", "F4_THESIS_MATURITY.json", "F4_CASE_ACCEPTANCE_TESTS.json", "F4_DECISION_FACTOR_MAP.json", "F4_INTERTEMPORAL_MAP.json", "F4_QUANTIFICATION_SCENARIOS.json", "F5C_RESEARCH_PROTOCOL.json", "F5C_STUDY_LEDGER.json", "F5C_EVIDENCE_SYNTHESIS.json", "F5C_CLAIM_EVIDENCE_MAP.json", "F7_CASE_TEST_RESULTS.json", "F7_GLOBAL_CONSISTENCY.json", "F7_METACOGNITIVE_AUDIT.json", "F7_SCIENCE_AUDIT.json", "F9_DELIVERY_SELECTION.json", "F10_DELIVERY_INTEGRITY.json"],
    "fact_or_proposition_ledger": ["F3_REASONING_GRAPH.json", "F4_COVERAGE_MATRIX.json", "F4_THESIS_MATURITY.json", "F4_CASE_ACCEPTANCE_TESTS.json", "F7_CASE_TEST_RESULTS.json", "F7_GLOBAL_CONSISTENCY.json", "F9_DELIVERY_SELECTION.json", "F10_DELIVERY_INTEGRITY.json"],
    "case_test": ["F7_CASE_TEST_RESULTS.json", "F7_GLOBAL_CONSISTENCY.json", "F9_DELIVERY_SELECTION.json", "F10_DELIVERY_INTEGRITY.json"],
    "science_source": ["F5C_STUDY_LEDGER.json", "F5C_EVIDENCE_SYNTHESIS.json", "F5C_CLAIM_EVIDENCE_MAP.json", "F7_SCIENCE_AUDIT.json", "F7_GLOBAL_CONSISTENCY.json", "F9_DELIVERY_SELECTION.json", "F10_DELIVERY_INTEGRITY.json"],
    "markdown": ["F7_CASE_TEST_RESULTS.json", "F7_GLOBAL_CONSISTENCY.json", "F9_DELIVERY_SELECTION.json", "F10_DELIVERY_INTEGRITY.json"],
    "docx_or_pdf": ["F7_GLOBAL_CONSISTENCY.json", "F9_DELIVERY_SELECTION.json", "F10_DELIVERY_INTEGRITY.json"],
    "formula_or_input": ["F4_QUANTIFICATION_SCENARIOS.json", "F7_GLOBAL_CONSISTENCY.json", "F9_DELIVERY_SELECTION.json", "F10_DELIVERY_INTEGRITY.json"],
    # Âncora reprovada derruba a rota que ela sustentava: o brief volta a ser
    # proposta, e tudo o que dele derivou envelhece junto.
    "precedent_anchor": ["F4_SIGNATURE_BRIEF.json", "F4_THESIS_MATURITY.json", "F4_COVERAGE_MATRIX.json", "F7_GLOBAL_CONSISTENCY.json", "F9_DELIVERY_SELECTION.json", "F10_DELIVERY_INTEGRITY.json"],
    # Composição, prevenção ou competência que mudam alteram para quem se
    # escreve — e o brief foi desenhado para um destinatário.
    "recipient_map": ["F4_SIGNATURE_BRIEF.json", "F4_THESIS_MATURITY.json", "F7_GLOBAL_CONSISTENCY.json", "F9_DELIVERY_SELECTION.json", "F10_DELIVERY_INTEGRITY.json"],
    "council_decision": ["F4_THESIS_MATURITY.json", "F4_COVERAGE_MATRIX.json", "F7_GLOBAL_CONSISTENCY.json", "F9_DELIVERY_SELECTION.json", "F10_DELIVERY_INTEGRITY.json"],
}


def invalidate(case_dir: Path, trigger: str, *, reason: str, actor: str = "forja-n4-invalidation") -> dict:
    if trigger not in DEPENDENCIES:
        raise ValueError(f"gatilho desconhecido: {trigger}")
    stale = []
    for filename in DEPENDENCIES[trigger]:
        path = case_dir / "n4_artifacts" / filename
        payload = read_json(path, None)
        if not isinstance(payload, dict) or payload.get("status") == "stale":
            continue
        payload["status"] = "stale"
        payload["issues"] = list(payload.get("issues") or []) + [{"code": "N4-STALE", "severity": "p0", "detail": reason, "trigger": trigger}]
        write_artifact(case_dir, filename, payload)
        stale.append(filename)
    append_trace(case_dir, "artifacts_invalidated", run_id=actor, status="ok", detail={"trigger": trigger, "reason": reason, "staleArtifacts": stale})
    state = derive_state(case_dir)
    if state.get("revision"):
        record_event(
            case_dir,
            "n4_gate_reopened",
            expected_revision=state["revision"],
            idempotency_key=f"n4-invalidate:{trigger}:{reason}:{','.join(stale)}",
            actor=actor,
            payload={"trigger": trigger, "reason": reason, "staleArtifacts": stale},
        )
    return {"caseId": case_dir.name, "trigger": trigger, "staleArtifacts": stale}


def main() -> None:
    parser = argparse.ArgumentParser(description="Invalida dependências N4 sem apagar histórico")
    parser.add_argument("case")
    parser.add_argument("trigger", choices=sorted(DEPENDENCIES))
    parser.add_argument("reason")
    args = parser.parse_args()
    print(json.dumps(invalidate(resolve_case_dir(args.case), args.trigger, reason=args.reason), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
