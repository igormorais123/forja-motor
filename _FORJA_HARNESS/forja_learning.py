"""Human-diff classification and guarded regression proposals for FORJA N4."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from forja_n3_common import resolve_case_dir
from forja_n4_common import ids_unique, issue, validate_file
from forja_post_protocol_contracts import IMPACTS, LAYERS, LAYER_CAUSES


CAUSES = {
    "fact", "legal_rule", "source_retrieval", "citation_scope", "reasoning", "calculation",
    "terminology", "visual", "delivery", "style_preference", "missing_input", "other",
}
FEEDBACK_KINDS = {
    "explicit_request", "explicit_correction", "approval", "repeated_preference",
    "implicit_hypothesis", "imported_content",
}
FEEDBACK_SCOPES = {"case", "product_type", "tribunal", "office", "global"}
FEEDBACK_STATUSES = {"observed", "proposed", "promoted", "rejected"}
CONFIDENCE = {"low", "medium", "high"}
CONTENT_CLASSES = {"human_authored", "imported_ai_output", "mixed", "unknown"}
CONTRIBUTION_ORIGINS = {
    "human_original", "human_selected", "forja_generated", "external_model_import",
    "source_derived", "mixed", "unknown",
}
THESIS_CHANGES = {"added", "strengthened", "weakened", "removed", "reframed", "unchanged"}
CONTRIBUTION_STATUS = {"unverified", "audited", "human_approved", "external_ready"}
WORKFLOW_STATUSES = {"proposed", "promoted", "rejected"}
FORBIDDEN_RAW_KEYS = {"body", "raw", "rawchat", "raw_chat", "transcript", "transcription", "quote", "verbatim"}


def _duplicates(values: list[str]) -> set[str]:
    seen: set[str] = set()
    return {value for value in values if value in seen or seen.add(value)}


def _raw_keys(value: object, prefix: str = "feedbackAssimilation") -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            normalized = str(key).lower().replace("-", "_")
            if normalized in FORBIDDEN_RAW_KEYS:
                found.append(f"{prefix}.{key}")
            found.extend(_raw_keys(child, f"{prefix}.{key}"))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.extend(_raw_keys(child, f"{prefix}[{index}]"))
    return found


def validate_feedback_assimilation(payload: dict) -> list[dict]:
    """Validate privacy-safe conversation learning and intellectual attribution."""
    findings: list[dict] = []
    units = payload.get("conversationUnits") or []
    signals = payload.get("signals") or []
    contributions = payload.get("contributions") or []
    workflow_changes = payload.get("workflowChanges") or []

    findings += ids_unique(units, "unitId", "N4-FEEDBACK-UNIT")
    findings += ids_unique(signals, "signalId", "N4-FEEDBACK-SIGNAL")
    findings += ids_unique(contributions, "contributionId", "N4-FEEDBACK-CONTRIBUTION")
    findings += ids_unique(workflow_changes, "changeId", "N4-FEEDBACK-WORKFLOW")
    for path in _raw_keys(payload):
        findings.append(issue("N4-FEEDBACK-RAW", f"conteúdo bruto proibido no ledger: {path}"))

    units_by_id = {str(item.get("unitId")): item for item in units if item.get("unitId")}
    message_owners: list[str] = []
    for unit in units:
        uid = str(unit.get("unitId") or "?")
        message_ids = [str(value) for value in unit.get("messageIds") or [] if value]
        if not message_ids:
            findings.append(issue("N4-FEEDBACK-UNIT-EVIDENCE", f"{uid}: unidade sem messageIds"))
        if unit.get("contentClass") not in CONTENT_CLASSES:
            findings.append(issue("N4-FEEDBACK-CONTENT-CLASS", f"{uid}: classe de autoria inválida"))
        message_owners.extend(message_ids)
        media = unit.get("mediaCoverage") or {}
        if int(media.get("essentialMissing") or 0) > 0:
            findings.append(issue("N4-FEEDBACK-MEDIA-MISSING", f"{uid}: mídia essencial não materializada"))
        if int(media.get("materialized") or 0) > int(media.get("expected") or 0):
            findings.append(issue("N4-FEEDBACK-MEDIA-COUNT", f"{uid}: materialização excede eventos esperados"))
    for message_id in sorted(_duplicates(message_owners)):
        findings.append(issue("N4-FEEDBACK-MESSAGE-OVERLAP", f"mensagem {message_id} pertence a mais de uma unidade"))

    signals_by_id = {str(item.get("signalId")): item for item in signals if item.get("signalId")}
    for signal in signals:
        sid = str(signal.get("signalId") or "?")
        unit_ids = [str(value) for value in signal.get("unitIds") or [] if value]
        if not unit_ids or any(value not in units_by_id for value in unit_ids):
            findings.append(issue("N4-FEEDBACK-SIGNAL-SOURCE", f"{sid}: unidade-fonte ausente ou desconhecida"))
        if signal.get("kind") not in FEEDBACK_KINDS:
            findings.append(issue("N4-FEEDBACK-KIND", f"{sid}: tipo de sinal inválido"))
        if signal.get("scope") not in FEEDBACK_SCOPES:
            findings.append(issue("N4-FEEDBACK-SCOPE", f"{sid}: escopo inválido"))
        if signal.get("confidence") not in CONFIDENCE:
            findings.append(issue("N4-FEEDBACK-CONFIDENCE", f"{sid}: confiança inválida"))
        if signal.get("status") not in FEEDBACK_STATUSES:
            findings.append(issue("N4-FEEDBACK-STATUS", f"{sid}: estado inválido"))
        if not signal.get("interpretation") or not signal.get("operationalConsequence"):
            findings.append(issue("N4-FEEDBACK-INTERPRETATION", f"{sid}: falta interpretação ou consequência"))
        if signal.get("kind") == "implicit_hypothesis" and signal.get("status") == "promoted":
            findings.append(issue("N4-FEEDBACK-IMPLICIT-PROMOTION", f"{sid}: inferência implícita não pode virar regra automaticamente"))
        if signal.get("status") == "promoted" and signal.get("scope") in {"office", "global"}:
            if not signal.get("approvedBy") or len(signal.get("evidenceRuns") or []) < 2:
                findings.append(issue("N4-FEEDBACK-GLOBAL-PROMOTION", f"{sid}: promoção ampla sem aprovação e duas evidências independentes"))

    for contribution in contributions:
        cid = str(contribution.get("contributionId") or "?")
        evidence_ids = [str(value) for value in contribution.get("evidenceIds") or [] if value]
        if not contribution.get("thesisId"):
            findings.append(issue("N4-FEEDBACK-THESIS", f"{cid}: contribuição sem thesisId"))
        if contribution.get("changeType") not in THESIS_CHANGES:
            findings.append(issue("N4-FEEDBACK-THESIS-CHANGE", f"{cid}: alteração de tese inválida"))
        if contribution.get("origin") not in CONTRIBUTION_ORIGINS:
            findings.append(issue("N4-FEEDBACK-ORIGIN", f"{cid}: origem intelectual inválida"))
        if not evidence_ids or any(value not in signals_by_id for value in evidence_ids):
            findings.append(issue("N4-FEEDBACK-CONTRIBUTION-EVIDENCE", f"{cid}: sinal-fonte ausente ou desconhecido"))
        if contribution.get("validationStatus") not in CONTRIBUTION_STATUS:
            findings.append(issue("N4-FEEDBACK-CONTRIBUTION-STATUS", f"{cid}: validação inválida"))
        source_units = {
            unit_id
            for signal_id in evidence_ids
            for unit_id in (signals_by_id.get(signal_id, {}).get("unitIds") or [])
        }
        if contribution.get("origin") == "human_original" and source_units and all(
            units_by_id.get(unit_id, {}).get("contentClass") == "imported_ai_output"
            for unit_id in source_units
        ):
            findings.append(issue("N4-FEEDBACK-FALSE-HUMAN-ATTRIBUTION", f"{cid}: conteúdo importado atribuído como criação humana"))
        if contribution.get("origin") == "unknown" and contribution.get("changeType") in {"added", "strengthened"}:
            findings.append(issue("N4-FEEDBACK-UNKNOWN-ORIGIN", f"{cid}: tese nova/fortalecida sem origem resolvida"))
        if contribution.get("validationStatus") == "external_ready" and contribution.get("changeType") in {"added", "strengthened", "reframed"}:
            if not contribution.get("sourceIds") or not contribution.get("legalDecisionId"):
                findings.append(issue("N4-FEEDBACK-EXTERNAL-READY", f"{cid}: tese material externa sem fonte e decisão jurídica"))

    for change in workflow_changes:
        wid = str(change.get("changeId") or "?")
        source_ids = [str(value) for value in change.get("sourceSignalIds") or [] if value]
        if not source_ids or any(value not in signals_by_id for value in source_ids):
            findings.append(issue("N4-FEEDBACK-WORKFLOW-SOURCE", f"{wid}: sinal-fonte ausente ou desconhecido"))
        if change.get("scope") not in FEEDBACK_SCOPES:
            findings.append(issue("N4-FEEDBACK-WORKFLOW-SCOPE", f"{wid}: escopo inválido"))
        if change.get("status") not in WORKFLOW_STATUSES:
            findings.append(issue("N4-FEEDBACK-WORKFLOW-STATUS", f"{wid}: estado inválido"))
        if not change.get("targetPhase") or not change.get("behavior"):
            findings.append(issue("N4-FEEDBACK-WORKFLOW-BEHAVIOR", f"{wid}: falta fase-alvo ou comportamento observável"))
        if change.get("status") == "promoted" and not all(
            (change.get("approvedBy"), change.get("testId"), change.get("evidenceRuns"))
        ):
            findings.append(issue("N4-FEEDBACK-WORKFLOW-PROMOTION", f"{wid}: promoção sem aprovação, teste e evidência"))
    return findings


def validate_learning(payload: dict) -> list[dict]:
    changes = payload.get("changes") or []
    proposals = payload.get("regressionProposals") or []
    post_protocol_v1 = bool(payload.get("comparisonId") or payload.get("protocolStatus"))
    findings = ids_unique(changes, "changeId", "N4-LEARN-CHANGE") + ids_unique(proposals, "proposalId", "N4-LEARN-PROPOSAL")
    if post_protocol_v1 and not re.fullmatch(r"[0-9a-f]{64}", str(payload.get("contentKey") or "")):
        findings.append(issue("N4-LEARN-CONTENT-KEY", "human diff pós-protocolo sem contentKey válido"))
    changes_by_id = {item.get("changeId"): item for item in changes}
    for change in changes:
        cid = str(change.get("changeId") or "?")
        if change.get("cause") not in CAUSES:
            findings.append(issue("N4-LEARN-CAUSE", f"{cid}: causa inválida"))
        layer = change.get("layer")
        if post_protocol_v1 and layer not in LAYERS:
            findings.append(issue("N4-LEARN-LAYER", f"{cid}: layer inválida"))
        elif layer in LAYERS and change.get("cause") not in LAYER_CAUSES[layer]:
            findings.append(issue("N4-LEARN-LAYER-CAUSE", f"{cid}: combinação layer/cause inválida"))
        if post_protocol_v1 and change.get("impact") not in IMPACTS:
            findings.append(issue("N4-LEARN-IMPACT", f"{cid}: impacto inválido"))
        has_full_diff = bool(change.get("before") or change.get("after"))
        has_hashed_diff = bool(change.get("beforeHash") and change.get("afterHash"))
        if not has_full_diff and not has_hashed_diff:
            findings.append(issue("N4-LEARN-DIFF", f"{cid}: alteração sem antes/depois ou hashes"))
        if layer == "unknown" and change.get("reviewDecision") not in {"pending", "rejected"}:
            findings.append(issue("N4-LEARN-UNKNOWN-GATE", f"{cid}: mudança desconhecida não pode ser aceita"))
        if change.get("origin") in {"unknown", "mixed"} and change.get("scopeCeiling") not in {None, "case"}:
            findings.append(issue("N4-LEARN-ORIGIN-SCOPE", f"{cid}: origem não resolvida só pode ficar no caso"))
    for proposal in proposals:
        pid = str(proposal.get("proposalId") or "?")
        source = changes_by_id.get(proposal.get("sourceChangeId"))
        if not source:
            findings.append(issue("N4-LEARN-SOURCE", f"{pid}: mudança-fonte inexistente"))
            continue
        if source.get("cause") == "style_preference" and proposal.get("scope") == "global":
            findings.append(issue("N4-LEARN-STYLE-GATE", f"{pid}: preferência isolada não pode virar gate global"))
        if proposal.get("status") == "promoted" and proposal.get("decision") != "approved":
            findings.append(issue("N4-LEARN-PROMOTION-DECISION", f"{pid}: promoção exige decision approved"))
        if proposal.get("status") == "promoted" and not all(proposal.get(key) for key in ("approvedBy", "fixtureId", "testId", "evidenceRuns")):
            findings.append(issue("N4-LEARN-PROMOTION", f"{pid}: promoção sem aprovação, fixture, teste e evidência"))
    if "feedbackAssimilation" in payload:
        findings.extend(validate_feedback_assimilation(payload.get("feedbackAssimilation") or {}))
    return findings


def validate_case(case_dir: Path) -> dict:
    _, findings = validate_file(case_dir, "F10_HUMAN_DIFF_CLASSIFICATION.json", validate_learning)
    return {"approved": not any(x["severity"] == "p0" for x in findings), "findings": findings}


def main() -> None:
    parser = argparse.ArgumentParser(description="Valida aprendizado humano FORJA N4")
    parser.add_argument("case")
    args = parser.parse_args()
    print(json.dumps(validate_case(resolve_case_dir(args.case)), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
