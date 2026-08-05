"""Verificação criptográfica de revisão humana de proposição jurídica.

Um campo JSON ``type=human`` é dado controlado pelo produtor e não comprova
supervisão humana. Este módulo exige um recibo assinado por uma chave Ed25519
previamente confiada fora do workspace da FORJA. A FORJA apenas verifica; ela
não gera chave privada nem assina recibos.

O trust store fica no caminho fixo ``~/.hermes/trust`` e seu SHA-256 deve estar
pinado em arquivo protegido pela régua. A variável de ambiente do processo não
pode trocar essa raiz. Ausência de configuração, hash divergente, chave
desconhecida ou assinatura inválida bloqueia em modo estrito.
"""

from __future__ import annotations

import base64
import hashlib
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from forja_n3_common import read_json, sha256_file


CLAIM_ATTESTATION_VERSION = "FORJA-HUMAN-CLAIM-REVIEW-v2"
VISUAL_ATTESTATION_VERSION = "FORJA-HUMAN-VISUAL-REVIEW-v1"
DEFAULT_TRUST_STORE = Path.home() / ".hermes" / "trust" / "FORJA_HUMAN_REVIEW_TRUST.json"
TRUST_STORE_PIN_PATH = Path(__file__).resolve().with_name("FORJA_HUMAN_REVIEW_TRUST_PIN.json")


def public_key_id(public_key_raw: bytes) -> str:
    return hashlib.sha256(public_key_raw).hexdigest()


def canonical_receipt_bytes(payload: dict) -> bytes:
    signed = {key: value for key, value in payload.items() if key != "signatureBase64"}
    return json.dumps(
        signed,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def build_unsigned_claim_receipt(
    *,
    reviewer_id: str,
    reviewed_at: str,
    public_key_id_value: str,
    generator_run_id: str,
    claim: str,
    claim_sha256: str,
    source_excerpt: str,
    source_excerpt_sha256: str,
    source_sha256: str,
    source_url: str,
    source_identity: dict,
    source_identity_sha256: str,
    document_sha256: str,
    document_proposition: str,
    document_proposition_sha256: str,
    document_paragraph_index: int,
    document_paragraph_sha256: str,
    authority_identity: dict,
    authority_identity_sha256: str,
) -> dict:
    """Monta os campos a serem exibidos e assinados pelo revisor externo."""
    return {
        "schemaVersion": 2,
        "attestationVersion": CLAIM_ATTESTATION_VERSION,
        "decision": "pass",
        "reviewPurpose": "jurisprudence_claim_entailment",
        "reviewerId": reviewer_id,
        "reviewedAt": reviewed_at,
        "publicKeyId": public_key_id_value,
        "generatorRunId": generator_run_id,
        "claim": claim,
        "claimSha256": claim_sha256,
        "sourceExcerpt": source_excerpt,
        "sourceExcerptSha256": source_excerpt_sha256,
        "sourceSha256": source_sha256,
        "sourceUrl": source_url,
        "sourceIdentity": source_identity,
        "sourceIdentitySha256": source_identity_sha256,
        "documentSha256": document_sha256,
        "documentProposition": document_proposition,
        "documentPropositionSha256": document_proposition_sha256,
        "documentParagraphIndex": int(document_paragraph_index),
        "documentParagraphSha256": document_paragraph_sha256,
        "authorityIdentity": authority_identity,
        "authorityIdentitySha256": authority_identity_sha256,
    }


def build_unsigned_visual_receipt(
    *,
    reviewer_id: str,
    reviewed_at: str,
    public_key_id_value: str,
    generator_run_id: str,
    reviewer_run_id: str,
    pdf_sha256: str,
    docx_sha256: str,
    page_count: int,
    page_image_sha256: list[str],
    required_checks: list[str],
    visual_attestation_sha256: str,
) -> dict:
    """Monta o recibo que o humano assina após olhar todas as páginas."""
    return {
        "schemaVersion": 1,
        "attestationVersion": VISUAL_ATTESTATION_VERSION,
        "decision": "pass",
        "reviewPurpose": "all_pages_visual_layout_review",
        "reviewerId": reviewer_id,
        "reviewedAt": reviewed_at,
        "publicKeyId": public_key_id_value,
        "generatorRunId": generator_run_id,
        "reviewerRunId": reviewer_run_id,
        "pdfSha256": pdf_sha256,
        "docxSha256": docx_sha256,
        "pageCount": int(page_count),
        "pageImageSha256": list(page_image_sha256),
        "requiredChecks": list(required_checks),
        "visualAttestationSha256": visual_attestation_sha256,
    }


def _trusted_key(trust_store: dict, reviewer_id: str, key_id: str) -> tuple[dict | None, list[str]]:
    reviewers = trust_store.get("reviewers") if isinstance(trust_store, dict) else None
    if trust_store.get("schemaVersion") != 1 or not isinstance(reviewers, list):
        return None, ["trust store humano inválido"]
    matches = [
        item for item in reviewers
        if isinstance(item, dict)
        and item.get("enabled") is True
        and item.get("reviewerId") == reviewer_id
        and item.get("publicKeyId") == key_id
        and item.get("algorithm") == "Ed25519"
    ]
    if len(matches) != 1:
        return None, ["revisor ou chave humana não consta do trust store"]
    return matches[0], []


def _load_pinned_trust_store(
    trust_store_path: Path | None,
    trust_store_pin_path: Path | None,
) -> tuple[dict, list[str]]:
    configured = Path(trust_store_path) if trust_store_path else DEFAULT_TRUST_STORE
    pin_path = Path(trust_store_pin_path) if trust_store_pin_path else TRUST_STORE_PIN_PATH
    findings: list[str] = []
    pin = read_json(pin_path, None)
    if not isinstance(pin, dict) or pin.get("schemaVersion") != 1:
        return {}, ["pin do trust store humano ausente ou inválido"]
    pinned_path = Path(str(pin.get("trustStorePath") or "")).expanduser()
    try:
        if configured.resolve() != pinned_path.resolve():
            findings.append("caminho do trust store humano diverge do pin protegido")
    except OSError:
        findings.append("caminho do trust store humano não pode ser resolvido")
    pinned_hash = str(pin.get("trustStoreSha256") or "").strip()
    if len(pinned_hash) != 64:
        findings.append("trust store humano ainda não foi pinado por revisão operacional")
    if not configured.is_file():
        findings.append("trust store humano externo não configurado")
        return {}, findings
    actual_hash = sha256_file(configured)
    if pinned_hash and actual_hash != pinned_hash:
        findings.append("hash do trust store humano diverge do pin protegido")
    return (read_json(configured, None) or {}), findings


def _validate_signed_receipt(
    receipt_path: Path,
    *,
    expected: dict,
    attestation_version: str,
    review_purpose: str,
    trust_store_path: Path | None = None,
    trust_store_pin_path: Path | None = None,
) -> dict:
    findings: list[str] = []
    receipt_path = Path(receipt_path)
    receipt = read_json(receipt_path, None)
    if not isinstance(receipt, dict):
        return {"approved": False, "findings": ["recibo humano ausente ou inválido"]}
    expected_schema = 2 if attestation_version == CLAIM_ATTESTATION_VERSION else 1
    if receipt.get("schemaVersion") != expected_schema or receipt.get("attestationVersion") != attestation_version:
        findings.append("recibo humano usa contrato desconhecido")
    if receipt.get("decision") != "pass" or receipt.get("reviewPurpose") != review_purpose:
        findings.append("recibo humano não aprova o objeto da revisão")

    for field, value in expected.items():
        if receipt.get(field) != value:
            findings.append(f"recibo humano diverge em {field}")

    reviewed_at = str(receipt.get("reviewedAt") or "")
    try:
        timestamp = datetime.fromisoformat(reviewed_at.replace("Z", "+00:00"))
        if timestamp.tzinfo is None:
            raise ValueError("timezone ausente")
        if timestamp.astimezone(timezone.utc) > datetime.now(timezone.utc) + timedelta(minutes=5):
            findings.append("recibo humano possui data futura")
    except ValueError:
        findings.append("recibo humano sem data ISO-8601 válida")

    trust_store, trust_load_findings = _load_pinned_trust_store(
        trust_store_path,
        trust_store_pin_path,
    )
    findings += trust_load_findings

    reviewer_id = str(receipt.get("reviewerId") or "")
    key_id = str(receipt.get("publicKeyId") or "")
    trusted, trust_findings = _trusted_key(trust_store, reviewer_id, key_id)
    findings += trust_findings
    if trusted:
        try:
            raw = base64.b64decode(str(trusted.get("publicKeyBase64") or ""), validate=True)
            if len(raw) != 32 or public_key_id(raw) != key_id:
                findings.append("chave pública humana inválida ou com id divergente")
            else:
                signature = base64.b64decode(str(receipt.get("signatureBase64") or ""), validate=True)
                from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

                Ed25519PublicKey.from_public_bytes(raw).verify(signature, canonical_receipt_bytes(receipt))
        except (ValueError, TypeError, ImportError) as exc:
            findings.append(f"assinatura humana inválida: {exc}")
        except Exception:
            # cryptography.exceptions.InvalidSignature não precisa vazar detalhe.
            findings.append("assinatura humana inválida")

    return {
        "approved": not findings,
        "findings": findings,
        "receiptPath": str(receipt_path),
        "receiptSha256": sha256_file(receipt_path),
        "reviewerId": reviewer_id,
        "publicKeyId": key_id,
        "reviewedAt": reviewed_at,
    }


def validate_claim_review_receipt(
    receipt_path: Path,
    *,
    expected: dict,
    trust_store_path: Path | None = None,
    trust_store_pin_path: Path | None = None,
) -> dict:
    """Valida assinatura e vínculo exato do recibo ao claim e à fonte."""
    return _validate_signed_receipt(
        receipt_path,
        expected=expected,
        attestation_version=CLAIM_ATTESTATION_VERSION,
        review_purpose="jurisprudence_claim_entailment",
        trust_store_path=trust_store_path,
        trust_store_pin_path=trust_store_pin_path,
    )


def validate_visual_review_receipt(
    receipt_path: Path,
    *,
    expected: dict,
    trust_store_path: Path | None = None,
    trust_store_pin_path: Path | None = None,
) -> dict:
    """Valida confirmação humana assinada da inspeção integral das páginas."""
    return _validate_signed_receipt(
        receipt_path,
        expected=expected,
        attestation_version=VISUAL_ATTESTATION_VERSION,
        review_purpose="all_pages_visual_layout_review",
        trust_store_path=trust_store_path,
        trust_store_pin_path=trust_store_pin_path,
    )
