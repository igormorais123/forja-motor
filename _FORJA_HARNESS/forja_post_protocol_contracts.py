"""Contratos funcionais do ramo pós-protocolo da FORJA.

Os validadores são fail-closed e não dependem de Gmail, disco ou painel.
"""

from __future__ import annotations

import re
from pathlib import Path

from forja_n4_common import ids_unique, issue


LAYERS = {
    "format_layout",
    "copy_style_voice",
    "fact",
    "procedural_identity",
    "legal_rule",
    "authority_citation",
    "reasoning",
    "request_relief",
    "evidence_annex",
    "calculation",
    "signature_protocol",
    "unknown",
}
LAYER_CAUSES = {
    "format_layout": {"visual"},
    "copy_style_voice": {"style_preference", "terminology"},
    "fact": {"fact"},
    "procedural_identity": {"fact", "reasoning"},
    "legal_rule": {"legal_rule"},
    "authority_citation": {"citation_scope", "source_retrieval"},
    "reasoning": {"reasoning"},
    "request_relief": {"reasoning"},
    "evidence_annex": {"missing_input", "source_retrieval"},
    "calculation": {"calculation"},
    "signature_protocol": {"delivery"},
    "unknown": {"other"},
}
IMPACTS = {"material", "não_material", "incerto"}
PROTOCOL_STATUSES = {
    "human_final_received",
    "protocol_claimed",
    "protocol_verified",
    "identity_ambiguous",
    "not_a_petition",
}
RESOLUTION_METHODS = {"existing_thread", "cnj", "delivery_evidence", "manual", "unresolved"}
EVIDENCE_KINDS = {"filing_receipt", "stamped_document", "lawyer_declaration", "none", "conflict"}
EVIDENCE_STRENGTHS = {
    "verified_file_link",
    "corroborating",
    "declaration_only",
    "none",
    "conflicting",
}
PROMOTION_STAGES = {
    "case_only",
    "evidence_repeated",
    "fixture_added",
    "test_passed",
    "independently_reviewed",
    "human_approved",
    "monitored",
    "retained",
    "rolled_back",
}
SCOPES = {"case", "product_type", "tribunal", "office", "global"}
STATUSES = {"observed", "proposed", "promoted", "rejected"}
DECISIONS = {"pending", "pending_revalidation", "approved", "rejected"}
ORIGINS = {
    "human_original",
    "human_selected",
    "forja_generated",
    "external_model_import",
    "source_derived",
    "mixed",
    "unknown",
}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
FORBIDDEN_RAW_KEYS = {"before", "after", "text", "quote", "verbatim", "raw", "body"}


def _hash_findings(value: object, field: str, code: str) -> list[dict]:
    return [] if SHA256_RE.fullmatch(str(value or "")) else [issue(code, f"{field}: SHA-256 inválido")]


def _raw_key_findings(value: object, prefix: str = "$") -> list[dict]:
    findings: list[dict] = []
    if isinstance(value, dict):
        for key, child in value.items():
            normalized = str(key).casefold().replace("-", "_")
            if normalized in FORBIDDEN_RAW_KEYS:
                findings.append(issue("PP-CONTRACT-RAW-TEXT", f"conteúdo jurídico bruto proibido em {prefix}.{key}"))
            findings.extend(_raw_key_findings(child, f"{prefix}.{key}"))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            findings.extend(_raw_key_findings(child, f"{prefix}[{index}]"))
    return findings


def validate_post_protocol_return(payload: dict) -> list[dict]:
    findings = _raw_key_findings(payload)
    findings.extend(_hash_findings(payload.get("contentKey"), "contentKey", "PP-CONTRACT-CONTENT-KEY"))
    evidence_keys = payload.get("evidenceKeys") or []
    if not evidence_keys or any(not SHA256_RE.fullmatch(str(key or "")) for key in evidence_keys):
        findings.append(issue("PP-CONTRACT-EVIDENCE-KEY", "evidenceKeys ausentes ou inválidas"))
    resolution = payload.get("caseResolution") or {}
    if resolution.get("status") not in {"resolved", "identity_ambiguous"}:
        findings.append(issue("PP-CONTRACT-RESOLUTION", "status de resolução inválido"))
    if resolution.get("method") not in RESOLUTION_METHODS:
        findings.append(issue("PP-CONTRACT-RESOLUTION", "método de resolução inválido"))
    if resolution.get("status") == "resolved" and not resolution.get("caseId"):
        findings.append(issue("PP-CONTRACT-RESOLUTION", "resolução conclusiva sem caseId"))
    artifact = payload.get("humanArtifact") or {}
    findings.extend(_hash_findings(artifact.get("sha256"), "humanArtifact.sha256", "PP-CONTRACT-HUMAN-HASH"))
    for key in ("artifactId", "originalName", "originalPath", "canonicalPath", "receivedAt"):
        if not str(artifact.get(key) or "").strip():
            findings.append(issue("PP-CONTRACT-HUMAN", f"humanArtifact.{key} ausente"))
    return findings


def validate_protocol_evidence(payload: dict) -> list[dict]:
    findings = _raw_key_findings(payload)
    findings.extend(_hash_findings(
        payload.get("humanArtifactHash"),
        "humanArtifactHash",
        "PP-CONTRACT-HUMAN-HASH",
    ))
    status = payload.get("protocolStatus")
    if status not in PROTOCOL_STATUSES:
        findings.append(issue("PP-CONTRACT-PROTOCOL-STATUS", "protocolStatus inválido"))
    links = payload.get("evidenceLinks") or []
    verified_links = 0
    for index, link in enumerate(links, 1):
        if link.get("kind") not in EVIDENCE_KINDS:
            findings.append(issue("PP-CONTRACT-EVIDENCE", f"evidência {index}: kind inválido"))
        if link.get("strength") not in EVIDENCE_STRENGTHS:
            findings.append(issue("PP-CONTRACT-EVIDENCE", f"evidência {index}: strength inválido"))
        if link.get("strength") == "verified_file_link":
            path = Path(str(link.get("evidencePath") or ""))
            digest = str(link.get("sha256") or "")
            external_id = str(link.get("externalProtocolId") or "").strip()
            if not external_id or not path.is_file() or not SHA256_RE.fullmatch(digest):
                findings.append(issue(
                    "PP-PROTOCOL-INCOMPLETE-LINK",
                    f"evidência {index}: protocolo externo, arquivo existente e SHA-256 são obrigatórios",
                ))
            else:
                from forja_n3_common import sha256_file

                if sha256_file(path) != digest:
                    findings.append(issue("PP-PROTOCOL-HASH-MISMATCH", f"evidência {index}: hash não confere"))
                else:
                    verified_links += 1
    if status == "protocol_verified" and verified_links == 0:
        findings.append(issue("PP-PROTOCOL-NO-FILE-LINK", "protocol_verified sem elo verificável do arquivo"))
    if status == "protocol_claimed" and verified_links:
        findings.append(issue("PP-PROTOCOL-UNDERCLASSIFIED", "há elo verificável, mas o status ficou apenas declarado"))
    return findings


def validate_document_comparison(payload: dict) -> list[dict]:
    findings: list[dict] = _raw_key_findings(payload)
    findings.extend(_hash_findings(payload.get("contentKey"), "contentKey", "PP-CONTRACT-CONTENT-KEY"))
    for side in ("baseline", "humanArtifact"):
        record = payload.get(side) or {}
        findings.extend(_hash_findings(record.get("sha256"), f"{side}.sha256", "PP-CONTRACT-COMPARE-HASH"))
        if not record.get("artifactId") or not record.get("path"):
            findings.append(issue("PP-CONTRACT-COMPARE-SIDE", f"{side}: artifactId/path ausente"))
    findings.extend(
        _hash_findings(
            payload.get("privateComparisonHash"),
            "privateComparisonHash",
            "PP-CONTRACT-COMPARE-PRIVATE-HASH",
        )
    )
    if not isinstance(payload.get("changes"), list):
        findings.append(issue("PP-CONTRACT-COMPARE-CHANGES", "changes deve ser lista"))
    return findings


def validate_learning_candidate(payload: dict) -> list[dict]:
    candidates = payload.get("candidates") or []
    findings = _raw_key_findings(payload)
    findings.extend(_hash_findings(payload.get("contentKey"), "contentKey", "PP-CONTRACT-CONTENT-KEY"))
    findings.extend(ids_unique(candidates, "candidateId", "PP-LEARN-CANDIDATE-ID"))
    for item in candidates:
        candidate_id = str(item.get("candidateId") or "?")
        if item.get("status") not in STATUSES:
            findings.append(issue("PP-LEARN-STATUS", f"{candidate_id}: status inválido"))
        if item.get("decision") not in DECISIONS:
            findings.append(issue("PP-LEARN-DECISION", f"{candidate_id}: decision inválida"))
        if item.get("scope") not in SCOPES:
            findings.append(issue("PP-LEARN-SCOPE", f"{candidate_id}: scope inválido"))
        if item.get("promotionStage") not in PROMOTION_STAGES:
            findings.append(issue("PP-LEARN-STAGE", f"{candidate_id}: promotionStage inválido"))
        if item.get("origin") not in ORIGINS:
            findings.append(issue("PP-LEARN-ORIGIN", f"{candidate_id}: origin inválida"))
        if item.get("origin") in {"unknown", "mixed"} and item.get("scope") != "case":
            findings.append(issue("PP-LEARN-ORIGIN-SCOPE", f"{candidate_id}: origem não resolvida só pode ficar no caso"))
        if item.get("status") == "promoted":
            if item.get("decision") != "approved":
                findings.append(issue("PP-LEARN-PROMOTION-DECISION", f"{candidate_id}: promoção exige decision approved"))
            required = (
                "approvedBy",
                "fixtureId",
                "testId",
                "testExecutionPath",
                "evidenceRuns",
                "evidenceCaseIds",
                "stageHistory",
            )
            if not all(item.get(key) for key in required):
                findings.append(issue("PP-LEARN-PROMOTION", f"{candidate_id}: promoção incompleta"))
            case_ids = list(item.get("evidenceCaseIds") or [])
            if len(case_ids) != len(set(case_ids)):
                findings.append(issue("PP-LEARN-EVIDENCE-CASES", f"{candidate_id}: casos de evidência duplicados"))
            if item.get("scope") in {"office", "global"} and len(set(case_ids)) < 2:
                findings.append(issue("PP-LEARN-WIDE-EVIDENCE", f"{candidate_id}: promoção ampla exige dois casos"))
            fixture = Path(str(item.get("fixtureId") or ""))
            receipt_path = Path(str(item.get("testExecutionPath") or ""))
            if not fixture.is_file():
                findings.append(issue("PP-LEARN-FIXTURE", f"{candidate_id}: fixture não existe"))
            receipt = {}
            if receipt_path.is_file():
                import json

                try:
                    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
                except (OSError, json.JSONDecodeError):
                    receipt = {}
            if receipt.get("passed") is not True or receipt.get("exitCode") != 0:
                findings.append(issue("PP-LEARN-TEST", f"{candidate_id}: execução verde não comprovada"))
            expected_order = ["case_only", "fixture_added", "test_passed", "human_approved"]
            history = item.get("stageHistory") or []
            if history[: len(expected_order)] != expected_order:
                findings.append(issue("PP-LEARN-STAGE-ORDER", f"{candidate_id}: progressão de estágio inválida"))
        if item.get("status") == "rejected" and item.get("decision") != "rejected":
            findings.append(issue("PP-LEARN-REJECTION-DECISION", f"{candidate_id}: rejeição exige decision rejected"))
    return findings


def validate_post_protocol_baseline_backfill(payload: dict) -> list[dict]:
    findings = _raw_key_findings(payload)
    if payload.get("status") != "pending_review":
        findings.append(issue("PP-BASELINE-BACKFILL-STATUS", "backfill histórico deve permanecer pending_review"))
    if payload.get("provenance") != "gmail_sent_attachment":
        findings.append(issue("PP-BASELINE-BACKFILL-PROVENANCE", "proveniência do backfill inválida"))
    if payload.get("preSendMatch") is not False:
        findings.append(issue("PP-BASELINE-BACKFILL-MATCH", "backfill não pode declarar preSendMatch"))
    findings.extend(_hash_findings(payload.get("selectedHash"), "selectedHash", "PP-BASELINE-BACKFILL-HASH"))
    path = Path(str(payload.get("selectedPath") or ""))
    if not payload.get("selectedArtifactId") or not payload.get("deliveredAt") or not path.is_file():
        findings.append(issue("PP-BASELINE-BACKFILL-EVIDENCE", "backfill sem artefato, data ou arquivo existente"))
    elif SHA256_RE.fullmatch(str(payload.get("selectedHash") or "")):
        from forja_n3_common import sha256_file

        if sha256_file(path) != payload["selectedHash"]:
            findings.append(issue("PP-BASELINE-BACKFILL-HASH", "arquivo do backfill não confere"))
    return findings
