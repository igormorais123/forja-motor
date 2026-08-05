"""Primitives for the additive FORJA N4 candidate layer.

N4 artifacts are ordinary JSON files under ``state/<case>/n4_artifacts``.
The helpers in this module never change N2/N3 artifacts or legal content.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from forja_n3_common import (
    ForjaN3Error,
    InterProcessLock,
    atomic_write_json,
    canonical_hash,
    now_iso,
    read_json,
)


SPEC_VERSION = "N4.0-candidate"
ARTIFACT_DIR = "n4_artifacts"
VALID_APPLICABILITY = {"required", "conditional", "not_applicable"}
VALID_STATUS = {"draft", "pending_review", "approved", "blocked", "stale", "not_applicable"}


ARTIFACT_SPECS: dict[str, dict[str, Any]] = {
    "F2_N4_CLASSIFICATION.json": {"type": "n4_classification", "phase": "F2_CLASSIFICACAO_PRODUTO_RISCO", "keys": ["science"]},
    "F2_QUESTION_TREE.json": {"type": "question_tree", "phase": "F2_CLASSIFICACAO_PRODUTO_RISCO", "keys": ["questions", "coverage"]},
    "F3_EVENT_IDENTITY.json": {"type": "event_identity", "phase": "F3_FONTES_REGIMENTO_LEIS", "keys": ["events"]},
    "F3_DOCUMENT_COMPARISON.json": {"type": "document_comparison", "phase": "F3_FONTES_REGIMENTO_LEIS", "keys": ["comparisonSets"]},
    "F3_REASONING_GRAPH.json": {"type": "reasoning_graph", "phase": "F3_FONTES_REGIMENTO_LEIS", "keys": ["nodes", "edges"]},
    # FORJA-ASSINATURA Lite (25/07/2026): tipos próprios, não conchas reaproveitadas.
    # "mapa do destinatário" e "decision factor map" não são o mesmo objeto, e um
    # nome que guarda outra coisa é um nome que mente.
    "F3_MAPA_DESTINATARIO.json": {"type": "recipient_map", "phase": "F3_FONTES_REGIMENTO_LEIS", "keys": ["recipient", "competence", "prevention", "composition", "positions"]},
    "F3_CONDUCT_LEDGER.json": {"type": "conduct_ledger", "phase": "F3_FONTES_REGIMENTO_LEIS", "keys": ["conducts"]},
    "F4_COVERAGE_MATRIX.json": {"type": "coverage_matrix", "phase": "F4_BLUEPRINT_ESTRATEGICO", "keys": ["items"]},
    "F4_THESIS_MATURITY.json": {"type": "thesis_maturity", "phase": "F4_BLUEPRINT_ESTRATEGICO", "keys": ["theses"]},
    "F4_CASE_ACCEPTANCE_TESTS.json": {"type": "case_acceptance_tests", "phase": "F4_BLUEPRINT_ESTRATEGICO", "keys": ["suiteId", "tests"]},
    "F4_DECISION_FACTOR_MAP.json": {"type": "decision_factor_map", "phase": "F4_BLUEPRINT_ESTRATEGICO", "keys": ["decisions"]},
    "F4_SETTLEMENT_MAP.json": {"type": "settlement_map", "phase": "F4_BLUEPRINT_ESTRATEGICO", "keys": ["interests", "prohibitions"]},
    "F4_SIGNATURE_BRIEF.json": {"type": "signature_brief", "phase": "F4_BLUEPRINT_ESTRATEGICO", "keys": ["decisiveQuestion", "routes", "selectedRouteId", "mandatoryContent"]},
    "F4_INTERTEMPORAL_MAP.json": {"type": "intertemporal_map", "phase": "F4_BLUEPRINT_ESTRATEGICO", "keys": ["temporalIssues"]},
    "F4_QUANTIFICATION_SCENARIOS.json": {"type": "quantification_scenarios", "phase": "F4_BLUEPRINT_ESTRATEGICO", "keys": ["scenarios"]},
    "F5C_RESEARCH_PROTOCOL.json": {"type": "science_research_protocol", "phase": "F5_PESQUISA_OFICIAL", "keys": ["researchQuestion", "databases", "queries"]},
    "F5C_STUDY_LEDGER.json": {"type": "science_study_ledger", "phase": "F5_PESQUISA_OFICIAL", "keys": ["studies"]},
    "F5C_EVIDENCE_SYNTHESIS.json": {"type": "science_evidence_synthesis", "phase": "F5_PESQUISA_OFICIAL", "keys": ["synthesisStatus", "contraryEvidenceSearch"]},
    "F5C_CLAIM_EVIDENCE_MAP.json": {"type": "science_claim_evidence_map", "phase": "F5_PESQUISA_OFICIAL", "keys": ["claims"]},
    "F7_CASE_TEST_RESULTS.json": {"type": "case_test_results", "phase": "F7_AUDITORIA_JURIDICA_FACTUAL", "keys": ["suiteHash", "draftHash", "results"]},
    "F7_GLOBAL_CONSISTENCY.json": {"type": "global_consistency", "phase": "F7_AUDITORIA_JURIDICA_FACTUAL", "keys": ["layers", "findings"]},
    "F7_METACOGNITIVE_AUDIT.json": {"type": "metacognitive_audit", "phase": "F7_AUDITORIA_JURIDICA_FACTUAL", "keys": ["premises", "consensusChecks", "recommendationChanges"]},
    "F7_SCIENCE_AUDIT.json": {"type": "science_audit", "phase": "F7_AUDITORIA_JURIDICA_FACTUAL", "keys": ["applicability", "findings"]},
    "F9_DELIVERY_SELECTION.json": {"type": "delivery_selection", "phase": "F9_PACOTE_REVISAO_DRAFT_OPCIONAL", "keys": ["packageArtifactId", "selectedArtifactId", "packageHash", "selectedHash", "preSendMatch", "layoutProfileId"]},
    "F10_DELIVERY_INTEGRITY.json": {"type": "delivery_integrity", "phase": "F10_ENTREGA_EVIDENCIA_APRENDIZADO", "keys": ["packageArtifactId", "selectedArtifactId", "packageHash", "selectedHash", "preSendMatch", "postDeliveryVerification"]},
    "F10_HUMAN_DIFF_CLASSIFICATION.json": {"type": "human_diff_classification", "phase": "F10_ENTREGA_EVIDENCIA_APRENDIZADO", "keys": ["changes", "regressionProposals"]},
    "F10_POST_PROTOCOL_RETURN.json": {
        "type": "post_protocol_return",
        "phase": "F10_ENTREGA_EVIDENCIA_APRENDIZADO",
        "schema": "post_protocol_return.schema.json",
        "keys": ["contentKey", "evidenceKeys", "caseResolution", "humanArtifact"],
    },
    "F10_PROTOCOL_EVIDENCE.json": {
        "type": "protocol_evidence",
        "phase": "F10_ENTREGA_EVIDENCIA_APRENDIZADO",
        "schema": "protocol_evidence.schema.json",
        "keys": ["protocolStatus", "humanArtifactHash", "evidenceLinks"],
    },
    "F10_POST_PROTOCOL_BASELINE_BACKFILL.json": {
        "type": "post_protocol_baseline_backfill",
        "phase": "F10_ENTREGA_EVIDENCIA_APRENDIZADO",
        "schema": "post_protocol_baseline_backfill.schema.json",
        "keys": [
            "selectedArtifactId",
            "selectedHash",
            "selectedPath",
            "deliveredAt",
            "deliveryEvidenceId",
            "provenance",
            "preSendMatch",
        ],
    },
    "F10_POST_PROTOCOL_DOCUMENT_COMPARISON.json": {
        "type": "post_protocol_document_comparison",
        "phase": "F10_ENTREGA_EVIDENCIA_APRENDIZADO",
        "schema": "document_comparison.schema.json",
        "keys": ["contentKey", "baseline", "humanArtifact", "summary", "changes", "privateComparisonHash"],
    },
    "F10_LEARNING_CANDIDATE.json": {
        "type": "learning_candidate",
        "phase": "F10_ENTREGA_EVIDENCIA_APRENDIZADO",
        "schema": "learning_candidate.schema.json",
        "keys": ["contentKey", "candidates"],
    },
}


def issue(code: str, detail: str, *, severity: str = "p0", artifact: str | None = None) -> dict:
    value = {"code": code, "severity": severity, "detail": detail}
    if artifact:
        value["artifact"] = artifact
    return value


def semantic_payload(payload: dict) -> dict:
    return {key: value for key, value in payload.items() if key not in {"contentHash", "updatedAt"}}


def expected_content_hash(payload: dict) -> str:
    return canonical_hash(semantic_payload(payload))


def artifact_path(case_dir: Path, filename: str) -> Path:
    if filename not in ARTIFACT_SPECS and filename != "N4_VALIDATION.json":
        raise ForjaN3Error(f"artefato N4 desconhecido: {filename}")
    return case_dir / ARTIFACT_DIR / filename


def build_envelope(
    case_dir: Path,
    filename: str,
    content: dict,
    *,
    source_hashes: list[str],
    producer_run_id: str,
    reviewer_run_id: str | None = None,
    applicability: str = "required",
    status: str = "draft",
) -> dict:
    spec = ARTIFACT_SPECS[filename]
    stamp = now_iso()
    payload = {
        "schemaVersion": 1,
        "specVersion": SPEC_VERSION,
        "caseId": case_dir.name,
        "artifactType": spec["type"],
        "phase": spec["phase"],
        "applicability": applicability,
        "status": status,
        "sourceHashes": sorted(set(source_hashes)),
        "producerRunId": producer_run_id,
        "reviewerRunId": reviewer_run_id,
        "createdAt": stamp,
        "updatedAt": stamp,
        "issues": [],
    }
    for key, value in content.items():
        if key in payload:
            if payload[key] != value:
                raise ForjaN3Error(f"conteúdo de {filename} tenta sobrescrever campo do envelope: {key}")
            continue
        payload[key] = value
    payload["contentHash"] = expected_content_hash(payload)
    return payload


def write_artifact(case_dir: Path, filename: str, payload: dict) -> Path:
    payload = dict(payload)
    payload["updatedAt"] = now_iso()
    payload["contentHash"] = expected_content_hash(payload)
    path = artifact_path(case_dir, filename)
    atomic_write_json(path, payload)
    append_trace(
        case_dir,
        "artifact_written",
        run_id=str(payload.get("producerRunId") or "unknown"),
        detail={"filename": filename, "artifactType": payload.get("artifactType"), "contentHash": payload["contentHash"], "sourceHashes": payload.get("sourceHashes") or []},
    )
    return path


def append_trace(case_dir: Path, action: str, *, run_id: str, detail: dict, status: str = "ok") -> None:
    directory = case_dir / ARTIFACT_DIR
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "N4_EXECUTION_TRACE.jsonl"
    record = {"schemaVersion": 1, "specVersion": SPEC_VERSION, "caseId": case_dir.name, "at": now_iso(), "runId": run_id, "action": action, "status": status, "detail": detail}
    with InterProcessLock(directory / ".n4-trace.lock", timeout=10, stale_after=300):
        with path.open("a", encoding="utf-8", newline="\n") as handle:
            import json

            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
            handle.flush()


def validate_envelope(case_dir: Path, filename: str, payload: Any) -> list[dict]:
    spec = ARTIFACT_SPECS.get(filename)
    if not isinstance(payload, dict) or not spec:
        return [issue("N4-ENV-INVALID", "JSON ausente, inválido ou sem contrato", artifact=filename)]
    findings: list[dict] = []
    expected = {
        "schemaVersion": 1,
        "specVersion": SPEC_VERSION,
        "caseId": case_dir.name,
        "artifactType": spec["type"],
        "phase": spec["phase"],
    }
    for key, value in expected.items():
        if payload.get(key) != value:
            findings.append(issue("N4-ENV-MISMATCH", f"{key} deveria ser {value!r}", artifact=filename))
    applicability = payload.get("applicability")
    status = payload.get("status")
    if applicability not in VALID_APPLICABILITY:
        findings.append(issue("N4-ENV-APPLICABILITY", "applicability inválida", artifact=filename))
    if status not in VALID_STATUS:
        findings.append(issue("N4-ENV-STATUS", "status inválido", artifact=filename))
    if applicability == "required" and status == "not_applicable":
        findings.append(issue("N4-ENV-REQUIRED-NA", "artefato obrigatório não pode terminar como não aplicável", artifact=filename))
    if applicability == "not_applicable":
        if not str(payload.get("justification") or "").strip():
            findings.append(issue("N4-ENV-NA-REASON", "não aplicabilidade exige justificativa", artifact=filename))
    else:
        for key in spec["keys"]:
            if key not in payload:
                findings.append(issue("N4-ENV-CONTENT", f"campo funcional ausente: {key}", artifact=filename))
    if status == "approved":
        if not payload.get("reviewerRunId"):
            findings.append(issue("N4-ENV-NO-REVIEW", "aprovação sem revisor", artifact=filename))
        if payload.get("producerRunId") == payload.get("reviewerRunId"):
            findings.append(issue("N4-ENV-SELF-REVIEW", "produtor e revisor não podem ser a mesma execução", artifact=filename))
    if payload.get("contentHash") != expected_content_hash(payload):
        findings.append(issue("N4-ENV-HASH", "contentHash não corresponde ao conteúdo atual", artifact=filename))
    return findings


def load_artifact(case_dir: Path, filename: str) -> dict | None:
    return read_json(artifact_path(case_dir, filename), None)


def validate_file(
    case_dir: Path,
    filename: str,
    validator: Callable[[dict], list[dict]] | None = None,
) -> tuple[dict | None, list[dict]]:
    payload = load_artifact(case_dir, filename)
    findings = validate_envelope(case_dir, filename, payload)
    if isinstance(payload, dict) and payload.get("applicability") != "not_applicable" and validator:
        findings.extend(validator(payload))
    return payload, findings


def ids_unique(items: list[dict], key: str, code: str) -> list[dict]:
    seen: set[str] = set()
    findings = []
    for item in items:
        value = str(item.get(key) or "").strip()
        if not value:
            findings.append(issue(code, f"{key} ausente"))
        elif value in seen:
            findings.append(issue(code, f"{key} duplicado: {value}"))
        seen.add(value)
    return findings
