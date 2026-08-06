"""Loop pós-protocolo: captura, prova, diff, aprendizado e eventos F10.

O núcleo recebe um retorno já associado a um caso. A varredura Gmail usa o
matcher canônico da gestão e chama esta aplicação somente quando há um vínculo
inequívoco.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import re
import shutil
import subprocess
import sys
from email.utils import getaddresses, parsedate_to_datetime
from datetime import datetime
from pathlib import Path
from typing import Any

from forja_document_compare import compare_documents, extract_document, render_markdown
from forja_n3_common import (
    FORJA,
    WORKSPACE,
    ForjaN3Error,
    InterProcessLock,
    RevisionConflict,
    atomic_write_json,
    atomic_write_text,
    canonical_hash,
    feature_enabled,
    load_config,
    new_id,
    now_iso,
    read_json,
    resolve_case_dir,
    sha256_bytes,
    sha256_file,
)
from forja_n4_common import build_envelope, write_artifact
from forja_post_protocol_contracts import (
    validate_document_comparison,
    validate_learning_candidate,
    validate_post_protocol_baseline_backfill,
    validate_post_protocol_return,
    validate_protocol_evidence,
)
from forja_learning import validate_learning
from forja_learning_registry import register_promoted_rule
from forja_state_machine import derive_state, initialize_case, load_events, record_event


OFFICE_SCRIPTS = WORKSPACE / "gestao_escritorio" / "scripts"
OFFICE_DATA = WORKSPACE / "gestao_escritorio" / "data"
SUPPORTED_RETURN_EXTENSIONS = {".docx", ".pdf", ".odt"}
PROTOCOL_CLAIM_RE = re.compile(
    r"\b(protocolad[ao]s?|protocolei|protocolo\s+(?:realizado|efetuado)|pe[cç]a\s+protocolada)\b",
    re.I,
)
PROTOCOL_MARK_RE = re.compile(
    r"\b(?:protocolad[ao]|n[uú]mero\s+do\s+protocolo|recibo\s+de\s+protocolo)\b",
    re.I,
)
E_SIGNATURE_RE = re.compile(r"\b(?:documento|peti[cç][aã]o)\s+assinado\s+eletronicamente\b", re.I)
EXTERNAL_PROTOCOL_ID_RE = re.compile(
    r"\b(?:protocolo|recibo)\s*(?:n[ºo.]|n[uú]mero|id)?\s*[:#-]?\s*"
    r"([A-Z0-9][A-Z0-9./_-]{5,})\b",
    re.I,
)
CNJ_RE = re.compile(r"\b\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}\b")
REASON_CODES = {
    "PP-01",
    "PP-02",
    "PP-03",
    "PP-04",
    "PP-05",
    "PP-06",
    "PP-07",
    "PP-08",
    "PP-09",
    "PP-10",
    "PP-11",
    "PP-12",
    "PP-13",
    "PP-14",
    "PP-15",
    "PP-BASELINE-MISSING",
    "PP-BASELINE-AMBIGUOUS",
    "PP-BASELINE-HASH",
    "PP-OCR-LOW-CONFIDENCE",
    "PP-SENDER-NOT-ALLOWED",
    "PP-CAPTURE-FAILED",
    "PP-NOT-A-REVISION",
    "PP-NO-RETURN-ATTACHMENT",
}

# Piso de comparabilidade: abaixo dele o documento humano não é revisão da nossa
# peça, e sim outro documento. Medido nos cinco retornos reais de 2026: os que
# eram revisão deram 0,50 e 0,67 de texto em comum; os que eram documento
# distinto deram 0,007, 0,031 e 0,134. Não há caso real entre 0,134 e 0,499.
#
# A medida é PROPORÇÃO de texto em comum, e não contagem de blocos preservados.
# A contagem foi testada junto e descartada: ela cresce com o tamanho do
# documento, de modo que uma peça curta legitimamente revisada não alcança
# piso nenhum e seria barrada por ser curta. Nos cinco retornos reais os dois
# sinais concordavam, então exigir os dois não comprava separação — só
# comprava um falso negativo em peça pequena.
PISO_TEXTO_COMUM = 0.30


def _e_revisao(comparison: dict) -> tuple[bool, dict]:
    """A peça humana é revisão da nossa base, ou é outro documento?

    Vem antes de qualquer aprendizado. Quando os dois documentos não têm
    origem comum, o alinhamento de tokens casa trechos sem relação entre si, e
    cada par casado vira uma "mudança" com camada, causa e confiança altas. O
    efeito não é uma linha errada: é volume. Nos retornos de 2026, três pares
    incomparáveis produziram 496 mudanças e 228 classificadas como materiais —
    mais do que o dobro do que veio dos dois retornos que eram revisão de
    verdade. Agregado por classe, esse ruído tem a forma exata de um padrão do
    escritório, e foi assim que quase virou regra.
    """
    resumo = comparison.get("summary") or {}
    medidas = {
        "sharedTokenRatio": resumo.get("sharedTokenRatio"),
        "retainedBlockRuns": resumo.get("retainedBlockRuns"),
        "pisoTextoComum": PISO_TEXTO_COMUM,
    }
    razao = resumo.get("sharedTokenRatio")
    if razao is None:
        # Comparação de versão anterior do comparador, sem a medida. Não se
        # inventa aprovação por ausência de dado.
        return False, medidas
    return razao >= PISO_TEXTO_COMUM, medidas
VERSIONED_POST_PROTOCOL_ARTIFACTS = (
    "F10_POST_PROTOCOL_RETURN.json",
    "F10_PROTOCOL_EVIDENCE.json",
    "F10_POST_PROTOCOL_DOCUMENT_COMPARISON.json",
    "F10_LEARNING_CANDIDATE.json",
    "F10_HUMAN_DIFF_CLASSIFICATION.json",
)


def safe_component(value: str, fallback: str, *, limit: int = 120) -> str:
    value = re.sub(r'[<>:"/\\|?*\x00-\x1f]', " ", value or fallback)
    value = re.sub(r"\s+", " ", value).strip(" .")
    return (value[:limit] or fallback).strip()


def content_key(case_id: str, attachment_hash: str) -> str:
    return sha256_bytes(f"{case_id}{attachment_hash}".encode("utf-8"))


def evidence_key(account_id: str, thread_id: str, message_id: str, attachment_id: str) -> str:
    return sha256_bytes(f"{account_id}{thread_id}{message_id}{attachment_id}".encode("utf-8"))


def _record(
    case_dir: Path,
    event_type: str,
    key: str,
    payload: dict,
    *,
    artifact_hashes: dict | None = None,
) -> tuple[dict, bool]:
    for _ in range(3):
        revision = derive_state(case_dir)["revision"]
        try:
            event, _state, created = record_event(
                case_dir,
                event_type,
                expected_revision=revision,
                idempotency_key=key,
                actor="forja-post-protocol",
                artifact_hashes=artifact_hashes,
                payload=payload,
            )
            return event, created
        except RevisionConflict:
            continue
    raise RevisionConflict(f"não foi possível registrar {event_type} após três conflitos")


def _parse_timestamp(value: str | None) -> datetime | None:
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=datetime.now().astimezone().tzinfo)
        return parsed.astimezone()
    except (TypeError, ValueError):
        return None


def _baseline_records(case_dir: Path) -> list[dict]:
    records: list[dict] = []
    current = read_json(case_dir / "n4_artifacts" / "F10_DELIVERY_INTEGRITY.json", None)
    if isinstance(current, dict):
        records.append(current)
    backfill = read_json(case_dir / "n4_artifacts" / "F10_POST_PROTOCOL_BASELINE_BACKFILL.json", None)
    if isinstance(backfill, dict):
        records.append(backfill)
    history = case_dir / "n4_artifacts" / "delivery_history"
    if history.is_dir():
        for path in sorted(history.glob("*.json")):
            payload = read_json(path, None)
            if isinstance(payload, dict) and (
                payload.get("artifactType") == "delivery_integrity"
                or (payload.get("postDeliveryVerification") or {}).get("status") == "confirmed"
            ):
                records.append(payload)
    unique: dict[str, dict] = {}
    for record in records:
        key = str(record.get("contentHash") or canonical_hash(record))
        unique[key] = record
    return list(unique.values())


def resolve_ai_baseline(case_dir: Path, *, received_at: str) -> tuple[dict | None, list[str]]:
    return_time = _parse_timestamp(received_at)
    candidates: list[tuple[datetime, dict]] = []
    reason_codes: list[str] = []
    for record in _baseline_records(case_dir):
        delivered_at = _parse_timestamp(record.get("deliveredAt"))
        if delivered_at is None or (return_time is not None and delivered_at > return_time):
            continue
        selected_path = Path(str(record.get("selectedPath") or ""))
        if not selected_path.is_absolute():
            selected_path = case_dir / selected_path
        selected_hash = str(record.get("selectedHash") or "")
        if not selected_path.is_file() or not selected_hash:
            reason_codes.append("PP-BASELINE-MISSING")
            continue
        if sha256_file(selected_path) != selected_hash:
            reason_codes.append("PP-BASELINE-HASH")
            continue
        is_backfill = record.get("artifactType") == "post_protocol_baseline_backfill"
        post = record.get("postDeliveryVerification") or {}
        if not is_backfill and post.get("status") != "confirmed":
            continue
        candidates.append((
            delivered_at,
            {
                **record,
                "selectedPath": str(selected_path.resolve()),
                "baselineAssurance": (
                    record.get("assurance")
                    if is_backfill
                    else "delivery_integrity_confirmed"
                ),
            },
        ))
    if not candidates:
        return None, sorted(set(reason_codes or ["PP-BASELINE-MISSING"]))
    candidates.sort(key=lambda item: item[0], reverse=True)
    latest_time = candidates[0][0]
    latest = [record for stamp, record in candidates if stamp == latest_time]
    hashes = {record.get("selectedHash") for record in latest}
    if len(hashes) != 1:
        return None, ["PP-BASELINE-AMBIGUOUS"]
    return latest[0], []


def _delivery_timestamp(message: dict) -> str:
    raw = _message_header(message, "Date")
    try:
        return parsedate_to_datetime(raw).astimezone().isoformat(timespec="seconds")
    except (TypeError, ValueError, OverflowError):
        internal = message.get("internalDate")
        if internal:
            return datetime.fromtimestamp(int(internal) / 1000).astimezone().isoformat(timespec="seconds")
    return now_iso()


def _sent_baseline_candidates(
    demand: dict,
    *,
    human_suffix: str,
    received_at: str,
    get_message,
) -> list[dict]:
    received = _parse_timestamp(received_at)
    candidates: list[dict] = []
    for sent_id in demand.get("emailsResposta") or []:
        message, status = get_message(sent_id)
        if not status.get("ok") or not isinstance(message, dict):
            continue
        sent_at = _delivery_timestamp(message)
        sent_time = _parse_timestamp(sent_at)
        if sent_time is None or (received is not None and sent_time >= received):
            continue
        parts = []
        for part in _walk_gmail_parts(message.get("payload") or {}):
            filename = str(part.get("filename") or "")
            body = part.get("body") or {}
            attachment_id = body.get("attachmentId")
            suffix = Path(filename).suffix.lower()
            if attachment_id and suffix in {".docx", ".pdf", ".odt"}:
                parts.append({
                    "filename": filename,
                    "attachmentId": attachment_id,
                    "mimeType": part.get("mimeType"),
                    "suffix": suffix,
                })
        same_format = [part for part in parts if part["suffix"] == human_suffix]
        pool = same_format or parts
        if len(pool) == 1:
            candidates.append({
                "messageId": sent_id,
                "threadId": message.get("threadId"),
                "deliveredAt": sent_at,
                **pool[0],
            })
    candidates.sort(key=lambda item: _parse_timestamp(item["deliveredAt"]) or datetime.min.astimezone(), reverse=True)
    return candidates


def _walk_gmail_parts(payload: dict):
    if not payload:
        return
    yield payload
    for part in payload.get("parts") or []:
        yield from _walk_gmail_parts(part)


def backfill_baseline_from_gmail(
    case_dir: Path,
    demand: dict,
    *,
    human_suffix: str,
    received_at: str,
    get_message,
    get_attachment,
    shadow: bool,
) -> dict | None:
    if not load_events(case_dir):
        initialize_case(case_dir, demand_id=str(demand.get("id") or "") or None)
    candidates = _sent_baseline_candidates(
        demand,
        human_suffix=human_suffix,
        received_at=received_at,
        get_message=get_message,
    )
    if not candidates:
        return None
    latest_at = candidates[0]["deliveredAt"]
    latest = [item for item in candidates if item["deliveredAt"] == latest_at]
    if len(latest) != 1:
        return {"status": "ambiguous", "reasonCode": "PP-BASELINE-AMBIGUOUS"}
    selected = latest[0]
    if shadow:
        return {
            "status": "available",
            "messageId": selected["messageId"],
            "attachmentId": selected["attachmentId"],
            "deliveredAt": selected["deliveredAt"],
        }
    response, status = get_attachment(selected["messageId"], selected["attachmentId"])
    if not status.get("ok") or not response or not response.get("data"):
        return {"status": "download_failed", "reasonCode": "PP-BASELINE-MISSING"}
    raw = base64.urlsafe_b64decode(response["data"] + "=" * (-len(response["data"]) % 4))
    digest = sha256_bytes(raw)
    vault = case_dir / "private" / "post_protocol" / "delivery_baselines"
    vault.mkdir(parents=True, exist_ok=True)
    selected_path = vault / f"{digest}{selected['suffix']}"
    if not selected_path.exists():
        selected_path.write_bytes(raw)
    if sha256_file(selected_path) != digest:
        raise ForjaN3Error("baseline Gmail divergiu após download")
    artifact_id = f"gmail-sent-{selected['messageId']}-{digest[:12]}"
    existing_backfill = read_json(
        case_dir / "n4_artifacts" / "F10_POST_PROTOCOL_BASELINE_BACKFILL.json",
        {},
    ) or {}
    if (
        existing_backfill.get("selectedHash") == digest
        and existing_backfill.get("deliveredAt") == selected["deliveredAt"]
        and existing_backfill.get("deliveryEvidenceId") == selected["messageId"]
    ):
        return {
            "status": "existing",
            "messageId": selected["messageId"],
            "attachmentId": selected["attachmentId"],
            "selectedArtifactId": existing_backfill["selectedArtifactId"],
            "selectedHash": digest,
            "selectedPath": existing_backfill["selectedPath"],
            "deliveredAt": selected["deliveredAt"],
        }
    run_id = new_id("post-protocol-backfill")
    backfill_content = {
        "selectedArtifactId": artifact_id,
        "selectedHash": digest,
        "selectedPath": str(selected_path.resolve()),
        "deliveredAt": selected["deliveredAt"],
        "deliveryEvidenceId": selected["messageId"],
        "provenance": "gmail_sent_attachment",
        "preSendMatch": False,
        "assurance": "gmail_exact_attachment_pending_review",
    }
    backfill = build_envelope(
        case_dir,
        "F10_POST_PROTOCOL_BASELINE_BACKFILL.json",
        backfill_content,
        source_hashes=[digest],
        producer_run_id=run_id,
        status="pending_review",
    )
    findings = validate_post_protocol_baseline_backfill(backfill)
    if findings:
        raise ForjaN3Error("backfill Gmail inválido: " + "; ".join(item["detail"] for item in findings))
    history = case_dir / "n4_artifacts" / "post_protocol_baseline_history"
    history.mkdir(parents=True, exist_ok=True)
    atomic_write_json(history / f"{backfill['contentHash']}.json", backfill)
    write_artifact(case_dir, "F10_POST_PROTOCOL_BASELINE_BACKFILL.json", backfill)
    _record(
        case_dir,
        "post_protocol_baseline_backfilled",
        f"gmail-baseline:{selected['messageId']}:{selected['attachmentId']}",
        {
            "aiBaselineArtifactId": artifact_id,
            "openReasonCodes": [],
            "reasonSource": "baseline",
            "resolvedReasonCodes": ["PP-BASELINE-MISSING", "PP-BASELINE-AMBIGUOUS", "PP-BASELINE-HASH"],
        },
        artifact_hashes={"selected": digest, "baselineBackfill": backfill["contentHash"]},
    )
    return {
        "status": "created",
        "messageId": selected["messageId"],
        "attachmentId": selected["attachmentId"],
        "selectedArtifactId": artifact_id,
        "selectedHash": digest,
        "selectedPath": str(selected_path),
        "deliveredAt": selected["deliveredAt"],
    }


def _select_return_parts(parts: list[dict]) -> tuple[list[dict], list[dict], str | None]:
    scored: list[tuple[int, dict]] = []
    evidence: list[dict] = []
    for part in parts:
        name = str(part.get("filename") or "").casefold()
        if re.search(r"\b(comprovante|recibo|protocolo)\b", name):
            evidence.append(part)
            continue
        score = 1
        if re.search(r"\b(final|assinad[ao]|protocolad[ao])\b", name):
            score += 4
        if re.search(r"\b(peti[cç][aã]o|memoriais|agravo|recurso|contrarraz|embargos|contesta[cç][aã]o)\b", name):
            score += 3
        scored.append((score, part))
    if not scored:
        return [], evidence, "PP-01"
    maximum = max(score for score, _part in scored)
    selected = [part for score, part in scored if score == maximum]
    remaining = evidence + [part for score, part in scored if score != maximum]
    if len(selected) != 1:
        return [], remaining + selected, "PP-01"
    return selected, remaining, None


def _text_similarity(first: Path, second: Path) -> float:
    left = extract_document(first).visible_text
    right = extract_document(second).visible_text
    normalize = lambda value: re.findall(r"[a-zà-ÿ0-9]+", value.casefold())
    a, b = normalize(left), normalize(right)
    if not a or not b:
        return 0.0
    def shingles(tokens: list[str], size: int = 5) -> set[str]:
        bounded = tokens[:100_000]
        if len(bounded) < size:
            return {" ".join(bounded)}
        return {" ".join(bounded[index:index + size]) for index in range(len(bounded) - size + 1)}

    left_shingles, right_shingles = shingles(a), shingles(b)
    return len(left_shingles & right_shingles) / max(1, len(left_shingles | right_shingles))


def _verified_protocol_link(link: dict) -> bool:
    if link.get("strength") != "verified_file_link" or not link.get("externalProtocolId"):
        return False
    path = Path(str(link.get("evidencePath") or ""))
    digest = str(link.get("sha256") or "")
    return path.is_file() and re.fullmatch(r"[0-9a-f]{64}", digest) is not None and sha256_file(path) == digest


def classify_protocol(
    human_path: Path,
    *,
    declaration_text: str = "",
    evidence_paths: list[Path] | None = None,
    explicit_links: list[dict] | None = None,
) -> tuple[str, list[dict], list[str]]:
    links = [dict(item) for item in (explicit_links or [])]
    reason_codes: list[str] = []
    for link in links:
        if _verified_protocol_link(link):
            return "protocol_verified", links, reason_codes
    claim = bool(PROTOCOL_CLAIM_RE.search(declaration_text or ""))
    if claim:
        links.append({
            "evidenceId": f"declaration-{hashlib.sha256(declaration_text.encode('utf-8')).hexdigest()[:16]}",
            "kind": "lawyer_declaration",
            "strength": "declaration_only",
        })
    for evidence in evidence_paths or []:
        evidence = evidence.resolve()
        if not evidence.is_file():
            continue
        try:
            extracted = extract_document(evidence)
        except ForjaN3Error:
            continue
        marker = bool(PROTOCOL_MARK_RE.search(extracted.visible_text))
        external_match = EXTERNAL_PROTOCOL_ID_RE.search(extracted.visible_text)
        external_protocol_id = external_match.group(1) if external_match else None
        electronic_signature_only = bool(E_SIGNATURE_RE.search(extracted.visible_text)) and not marker
        similarity = 0.0
        if marker and evidence != human_path.resolve():
            try:
                similarity = _text_similarity(human_path, evidence)
            except Exception:
                similarity = 0.0
        evidence_id = f"evidence-{sha256_file(evidence)[:16]}"
        if marker and external_protocol_id and similarity >= 0.94:
            links.append({
                "evidenceId": evidence_id,
                "kind": "stamped_document",
                "strength": "verified_file_link",
                "sha256": sha256_file(evidence),
                "evidencePath": str(evidence),
                "externalProtocolId": external_protocol_id,
                "similarity": round(similarity, 4),
            })
            return "protocol_verified", links, reason_codes
        links.append({
            "evidenceId": evidence_id,
            "kind": "filing_receipt" if "comprov" in evidence.name.casefold() else "stamped_document",
            "strength": "corroborating" if marker or electronic_signature_only else "none",
            "sha256": sha256_file(evidence),
            "evidencePath": str(evidence),
            **({"externalProtocolId": external_protocol_id} if external_protocol_id else {}),
        })
    if claim:
        reason_codes.append("PP-03")
        return "protocol_claimed", links, reason_codes
    return "human_final_received", links or [{
        "evidenceId": "none",
        "kind": "none",
        "strength": "none",
    }], reason_codes


def _folder_labels(protocol_status: str, piece_name: str, process_id: str, date_label: str) -> tuple[str, str]:
    middle = " — ".join(
        value for value in (
            safe_component(piece_name, "PEÇA"),
            safe_component(process_id, "SEM IDENTIFICADOR", limit=42),
            safe_component(date_label, "SEM DATA", limit=20),
        )
        if value
    )
    prefix = "PEÇA PROTOCOLADA" if protocol_status == "protocol_verified" else "VERSÃO HUMANA FINAL"
    return f"{prefix} — {middle}", f"{prefix} — {middle}"


def _index_path(case_dir: Path) -> Path:
    return case_dir / "private" / "post_protocol" / "INDEX.json"


def _load_index(case_dir: Path) -> dict:
    return read_json(_index_path(case_dir), {"schemaVersion": 1, "contents": {}}) or {
        "schemaVersion": 1,
        "contents": {},
    }


def _set_index_state(case_dir: Path, ckey: str, state: str, **updates: Any) -> None:
    private_root = case_dir / "private" / "post_protocol"
    with InterProcessLock(private_root / ".capture.lock", timeout=15, stale_after=900):
        index = _load_index(case_dir)
        entry = (index.get("contents") or {}).get(ckey)
        if not isinstance(entry, dict):
            raise ForjaN3Error(f"índice pós-protocolo perdeu contentKey {ckey}")
        entry.update(updates)
        entry["state"] = state
        entry["updatedAt"] = now_iso()
        atomic_write_json(_index_path(case_dir), index)


def _require_post_protocol_enabled() -> None:
    if not feature_enabled("n4PostProtocolV1"):
        raise ForjaN3Error("loop pós-protocolo desabilitado por features.n4PostProtocolV1=false")


def _block_capture(
    case_dir: Path,
    ckey: str,
    manifest_path: Path,
    manifest: dict,
    *,
    reason_codes: list[str],
    detail: str,
    human_artifact_id: str,
    protocol_status: str,
) -> dict:
    codes = sorted(set(reason_codes))
    manifest["reasonCodes"] = sorted(set((manifest.get("reasonCodes") or []) + codes))
    manifest["captureState"] = "blocked"
    manifest["lastBlockDetail"] = detail
    manifest["updatedAt"] = now_iso()
    atomic_write_json(manifest_path, manifest)
    _set_index_state(case_dir, ckey, "blocked", reasonCodes=codes)
    _record(
        case_dir,
        "post_protocol_blocked",
        f"{ckey}:blocked:{canonical_hash({'codes': codes, 'detail': detail})}",
        {
            "contentKey": ckey,
            "humanArtifactId": human_artifact_id,
            "protocolStatus": protocol_status,
            "openReasonCodes": codes,
            "reasonSource": "capture",
            "blockDetailCode": detail,
        },
    )
    return {
        "status": "blocked",
        "contentKey": ckey,
        "protocolStatus": protocol_status,
        "reasonCodes": codes,
        "created": False,
    }


def _write_artifact_checked(
    case_dir: Path,
    filename: str,
    content: dict,
    source_hashes: list[str],
    validator,
    *,
    producer_run_id: str,
) -> dict:
    payload = build_envelope(
        case_dir,
        filename,
        content,
        source_hashes=source_hashes,
        producer_run_id=producer_run_id,
        status="pending_review",
    )
    findings = validator(payload)
    if findings:
        raise ForjaN3Error(
            f"{filename} inválido: " + "; ".join(str(item.get("detail")) for item in findings)
        )
    write_artifact(case_dir, filename, payload)
    return payload


def _archive_prior_post_protocol_artifacts(case_dir: Path, incoming_content_key: str) -> None:
    root = case_dir / "n4_artifacts"
    for filename in VERSIONED_POST_PROTOCOL_ARTIFACTS:
        current = read_json(root / filename, None)
        if not isinstance(current, dict):
            continue
        old_content_key = str(current.get("contentKey") or "")
        if not old_content_key or old_content_key == incoming_content_key:
            continue
        target = root / "post_protocol_history" / old_content_key / filename
        if target.is_file():
            saved = read_json(target, {}) or {}
            if saved.get("contentHash") == current.get("contentHash"):
                continue
            target = target.with_name(
                f"{target.stem}-{str(current.get('contentHash') or canonical_hash(current))[:16]}.json"
            )
        atomic_write_json(target, current)


def _sanitize_changes(changes: list[dict]) -> list[dict]:
    result = []
    for item in changes:
        result.append({
            "changeId": item["changeId"],
            "changeFingerprint": item["changeFingerprint"],
            "regionId": item.get("regionId"),
            "operation": item["operation"],
            "beforeHash": sha256_bytes(item.get("before", "").encode("utf-8")),
            "afterHash": sha256_bytes(item.get("after", "").encode("utf-8")),
            "baselineLocator": item.get("baselineLocator") or [],
            "humanLocator": item.get("humanLocator") or [],
            "layer": item["layer"],
            "cause": item["cause"],
            "impact": item["impact"],
            "confidence": item["confidence"],
            "origin": item.get("origin") or "unknown",
            "scopeCeiling": "case",
            "reasonCodes": item.get("reasonCodes") or [],
            "reviewDecision": item.get("reviewDecision") or "pending",
        })
    return result


def _preserve_change_reviews(changes: list[dict], prior_changes: list[dict]) -> list[dict]:
    prior = {
        str(item.get("changeFingerprint")): item
        for item in prior_changes
        if item.get("changeFingerprint")
    }
    for change in changes:
        old = prior.get(str(change.get("changeFingerprint")))
        if old:
            for key in ("reviewDecision", "origin", "scopeCeiling", "reviewedBy", "reviewedAt"):
                if old.get(key) is not None:
                    change[key] = old[key]
    return changes


def _learning_candidates(changes: list[dict], existing: list[dict] | None = None) -> list[dict]:
    prior_by_fingerprint = {
        str(item.get("changeFingerprint")): item
        for item in (existing or [])
        if item.get("changeFingerprint")
    }
    candidates = []
    for item in changes:
        fingerprint = str(item["changeFingerprint"])
        prior = prior_by_fingerprint.get(fingerprint, {})
        candidate = {
            "candidateId": str(prior.get("candidateId") or f"learn-{fingerprint[:16]}"),
            "sourceChangeId": item["changeId"],
            "changeFingerprint": fingerprint,
            "status": prior.get("status") or "observed",
            "scope": prior.get("scope") or "case",
            "promotionStage": prior.get("promotionStage") or "case_only",
            "origin": prior.get("origin") or "unknown",
            "impact": item["impact"],
            "layer": item["layer"],
            "cause": item["cause"],
            "confidence": item["confidence"],
            "destination": "regression_fixture" if item["impact"] == "material" else "review_queue",
            "decision": prior.get("decision") or "pending",
        }
        for key in (
            "approvedBy",
            "fixtureId",
            "testId",
            "testExecutionPath",
            "evidenceRuns",
            "evidenceCaseIds",
            "stageHistory",
            "promotedAt",
            "rejectedAt",
            "originEvidenceId",
            "originDecidedBy",
            "originDecidedAt",
        ):
            if prior.get(key) is not None:
                candidate[key] = prior[key]
        if candidate.get("status") == "promoted":
            receipt = read_json(Path(str(candidate.get("testExecutionPath") or "")), {}) or {}
            fixture_ok = Path(str(candidate.get("fixtureId") or "")).is_file()
            if receipt.get("passed") is True and receipt.get("exitCode") == 0 and fixture_ok:
                candidate["decision"] = "approved"
                candidate["promotionCarryoverValidatedAt"] = now_iso()
            else:
                candidate.update({
                    "status": "observed",
                    "scope": "case",
                    "promotionStage": "case_only",
                    "decision": "pending_revalidation",
                })
                for proof_key in (
                    "approvedBy",
                    "fixtureId",
                    "testId",
                    "testExecutionPath",
                    "evidenceRuns",
                    "evidenceCaseIds",
                    "stageHistory",
                    "promotedAt",
                ):
                    candidate.pop(proof_key, None)
        candidates.append(candidate)
    return candidates


def _regression_proposals(candidates: list[dict]) -> list[dict]:
    result = []
    for candidate in candidates:
        proposal = {
            "proposalId": candidate["candidateId"],
            "sourceChangeId": candidate["sourceChangeId"],
            "status": candidate["status"],
            "scope": candidate["scope"],
            "promotionStage": candidate["promotionStage"],
            "origin": candidate["origin"],
            "decision": candidate["decision"],
        }
        for key in (
            "approvedBy",
            "fixtureId",
            "testId",
            "testExecutionPath",
            "evidenceRuns",
            "evidenceCaseIds",
            "stageHistory",
        ):
            if candidate.get(key) is not None:
                proposal[key] = candidate[key]
        result.append(proposal)
    return result


def ingest_return(
    case_dir: Path,
    attachment_path: Path,
    *,
    account_id: str,
    thread_id: str,
    message_id: str,
    attachment_id: str,
    received_at: str,
    original_name: str | None = None,
    piece_name: str = "PETIÇÃO",
    process_id: str = "",
    declaration_text: str = "",
    evidence_paths: list[Path] | None = None,
    explicit_evidence_links: list[dict] | None = None,
    producer_run_id: str | None = None,
) -> dict:
    _require_post_protocol_enabled()
    case_dir = case_dir.resolve()
    attachment_path = attachment_path.resolve()
    if not attachment_path.is_file():
        raise ForjaN3Error(f"anexo não localizado: {attachment_path}")
    if attachment_path.suffix.lower() not in SUPPORTED_RETURN_EXTENSIONS:
        raise ForjaN3Error(f"anexo não é peça comparável: {attachment_path.suffix}")
    if not load_events(case_dir):
        initialize_case(case_dir)
    run_id = producer_run_id or new_id("post-protocol")
    attachment_hash = sha256_file(attachment_path)
    ckey = content_key(case_dir.name, attachment_hash)
    ekey = evidence_key(account_id, thread_id, message_id, attachment_id)
    _record(
        case_dir,
        "post_protocol_candidate_detected",
        f"{ekey}:candidate:v1",
        {
            "contentKey": ckey,
            "openReasonCodes": [],
            "sourceChannel": "gmail_read_only",
        },
        artifact_hashes={"attachment": attachment_hash},
    )
    protocol_status, evidence_links, protocol_reasons = classify_protocol(
        attachment_path,
        declaration_text=declaration_text,
        evidence_paths=evidence_paths,
        explicit_links=explicit_evidence_links,
    )
    _archive_prior_post_protocol_artifacts(case_dir, ckey)
    date_label = (received_at or now_iso())[:10]
    folder_label, file_stem = _folder_labels(protocol_status, piece_name, process_id, date_label)
    private_root = case_dir / "private" / "post_protocol"
    lock = InterProcessLock(private_root / ".capture.lock", timeout=15, stale_after=900)
    created_capture = True
    with lock:
        index = _load_index(case_dir)
        existing = (index.get("contents") or {}).get(ckey)
        if existing:
            manifest_path = Path(existing["manifestPath"])
            manifest = read_json(manifest_path, {}) or {}
            manifest["evidenceKeys"] = sorted(set((manifest.get("evidenceKeys") or []) + [ekey]))
            manifest["updatedAt"] = now_iso()
            index["contents"][ckey]["evidenceKeys"] = manifest["evidenceKeys"]
            index["contents"][ckey]["updatedAt"] = now_iso()
            terminal = existing.get("state") in {"diff_ready", "review_pending", "complete"}
            if terminal and manifest_path.is_file() and (manifest.get("comparison") or {}).get("comparisonHash"):
                atomic_write_json(manifest_path, manifest)
                atomic_write_json(_index_path(case_dir), index)
                return {
                    "status": "duplicate_content",
                    "contentKey": ckey,
                    "evidenceKey": ekey,
                    "folder": existing["folder"],
                    "manifest": str(manifest_path),
                    "created": False,
                }
            created_capture = False
            folder = Path(existing["folder"])
            original_target = Path(str(manifest.get("originalPath") or folder / f"ORIGINAL RECEBIDO — {safe_component(original_name or attachment_path.name, attachment_path.name)}"))
            canonical_target = Path(str(manifest.get("canonicalPath") or folder / f"{file_stem}{attachment_path.suffix.lower()}"))
            human_artifact_id = str(manifest.get("humanArtifactId") or f"human-{ckey[:16]}")
            if not folder.exists():
                folder.mkdir(parents=True)
            if not original_target.is_file():
                shutil.copyfile(attachment_path, original_target)
            if not canonical_target.is_file():
                shutil.copyfile(attachment_path, canonical_target)
            if sha256_file(original_target) != attachment_hash or sha256_file(canonical_target) != attachment_hash:
                raise ForjaN3Error("retomada encontrou cópia divergente do anexo")
            if not manifest:
                manifest = {
                    "schemaVersion": 1,
                    "contentKey": ckey,
                    "evidenceKeys": [ekey],
                    "caseId": case_dir.name,
                    "humanArtifactId": human_artifact_id,
                    "protocolStatus": protocol_status,
                    "previousNames": [],
                    "originalName": original_name or attachment_path.name,
                    "originalPath": str(original_target.resolve()),
                    "canonicalPath": str(canonical_target.resolve()),
                    "sha256": attachment_hash,
                    "receivedAt": received_at,
                    "source": {
                        "channel": "gmail_read_only",
                        "accountId": account_id,
                        "threadId": thread_id,
                        "messageId": message_id,
                        "attachmentId": attachment_id,
                    },
                    "evidenceLinks": evidence_links,
                    "reasonCodes": protocol_reasons,
                    "createdAt": now_iso(),
                }
            manifest["captureState"] = "captured"
            atomic_write_json(manifest_path, manifest)
            index["contents"][ckey]["state"] = "captured"
            atomic_write_json(_index_path(case_dir), index)
        else:
            folder = case_dir / folder_label
            if folder.exists():
                suffix = 2
                while (case_dir / f"{folder_label} — v{suffix:02d}").exists():
                    suffix += 1
                folder = case_dir / f"{folder_label} — v{suffix:02d}"
            folder.mkdir(parents=True)
            original_filename = safe_component(original_name or attachment_path.name, "original" + attachment_path.suffix)
            if not Path(original_filename).suffix:
                original_filename += attachment_path.suffix
            original_target = folder / f"ORIGINAL RECEBIDO — {original_filename}"
            canonical_target = folder / f"{file_stem}{attachment_path.suffix.lower()}"
            human_artifact_id = f"human-{ckey[:16]}"
            manifest_path = folder / "PROTOCOLO_E_PROVENIENCIA.json"
            index.setdefault("contents", {})[ckey] = {
                "folder": str(folder.resolve()),
                "manifestPath": str(manifest_path.resolve()),
                "evidenceKeys": [ekey],
                "sha256": attachment_hash,
                "state": "capturing",
                "updatedAt": now_iso(),
            }
            atomic_write_json(_index_path(case_dir), index)
            shutil.copyfile(attachment_path, original_target)
            shutil.copyfile(attachment_path, canonical_target)
            if sha256_file(original_target) != attachment_hash or sha256_file(canonical_target) != attachment_hash:
                raise ForjaN3Error("cópia capturada divergiu do anexo")
            manifest = {
            "schemaVersion": 1,
            "contentKey": ckey,
            "evidenceKeys": [ekey],
            "caseId": case_dir.name,
            "humanArtifactId": human_artifact_id,
            "protocolStatus": protocol_status,
            "previousNames": [],
            "originalName": original_name or attachment_path.name,
            "originalPath": str(original_target.resolve()),
            "canonicalPath": str(canonical_target.resolve()),
            "sha256": attachment_hash,
            "receivedAt": received_at,
            "source": {
                "channel": "gmail_read_only",
                "accountId": account_id,
                "threadId": thread_id,
                "messageId": message_id,
                "attachmentId": attachment_id,
            },
            "evidenceLinks": evidence_links,
            "reasonCodes": protocol_reasons,
            "createdAt": now_iso(),
            "updatedAt": now_iso(),
            "captureState": "captured",
            }
            atomic_write_json(manifest_path, manifest)
            atomic_write_json(folder / "HASHES.json", {
                "schemaVersion": 1,
                "original": sha256_file(original_target),
                "canonical": sha256_file(canonical_target),
                "sourceAttachment": attachment_hash,
            })
            index["contents"][ckey]["state"] = "captured"
            index["contents"][ckey]["updatedAt"] = now_iso()
            atomic_write_json(_index_path(case_dir), index)
    return_content = {
        "contentKey": ckey,
        "evidenceKeys": [ekey],
        "caseResolution": {
            "status": "resolved",
            "caseId": case_dir.name,
            "demandId": derive_state(case_dir).get("demandId"),
            "method": "existing_thread",
            "confidence": "high",
            "reasonCodes": [],
        },
        "humanArtifact": {
            "artifactId": human_artifact_id,
            "sha256": attachment_hash,
            "originalName": original_name or attachment_path.name,
            "originalPath": str(original_target.resolve()),
            "canonicalPath": str(canonical_target.resolve()),
            "receivedAt": received_at,
        },
    }
    returned = _write_artifact_checked(
        case_dir,
        "F10_POST_PROTOCOL_RETURN.json",
        return_content,
        [attachment_hash, ekey],
        validate_post_protocol_return,
        producer_run_id=run_id,
    )
    _record(
        case_dir,
        "post_protocol_captured",
        f"{ckey}:captured:v1",
        {
            "contentKey": ckey,
            "humanArtifactId": human_artifact_id,
            "protocolStatus": protocol_status,
            "openReasonCodes": protocol_reasons,
        },
        artifact_hashes={"postProtocolReturn": returned["contentHash"]},
    )
    protocol_content = {
        "contentKey": ckey,
        "protocolStatus": protocol_status,
        "humanArtifactHash": attachment_hash,
        "evidenceLinks": evidence_links,
    }
    protocol_artifact = _write_artifact_checked(
        case_dir,
        "F10_PROTOCOL_EVIDENCE.json",
        protocol_content,
        [attachment_hash] + [str(link.get("sha256")) for link in evidence_links if link.get("sha256")],
        validate_protocol_evidence,
        producer_run_id=run_id,
    )
    protocol_evidence_id = f"protocol-{protocol_artifact['contentHash'][:16]}"
    protocol_event = {
        "protocol_verified": "post_protocol_verified",
        "protocol_claimed": "post_protocol_claimed",
    }.get(protocol_status)
    if protocol_event:
        _record(
            case_dir,
            protocol_event,
            f"{ckey}:{protocol_status}:v1",
            {
                "contentKey": ckey,
                "humanArtifactId": human_artifact_id,
                "protocolEvidenceId": protocol_evidence_id,
                "protocolStatus": protocol_status,
                "openReasonCodes": protocol_reasons,
            },
            artifact_hashes={"protocolEvidence": protocol_artifact["contentHash"]},
        )
    baseline, baseline_reasons = resolve_ai_baseline(case_dir, received_at=received_at)
    if baseline is None:
        _record(
            case_dir,
            "post_protocol_ai_baseline_unresolved",
            f"{ckey}:baseline-unresolved:v1",
            {
                "contentKey": ckey,
                "humanArtifactId": human_artifact_id,
                "protocolEvidenceId": protocol_evidence_id,
                "protocolStatus": protocol_status,
                "openReasonCodes": baseline_reasons,
            },
        )
        manifest["reasonCodes"] = sorted(set(protocol_reasons + baseline_reasons))
        manifest["captureState"] = "baseline_unresolved"
        manifest["updatedAt"] = now_iso()
        atomic_write_json(manifest_path, manifest)
        _set_index_state(
            case_dir,
            ckey,
            "baseline_unresolved",
            reasonCodes=baseline_reasons,
        )
        return {
            "status": "captured_baseline_unresolved",
            "contentKey": ckey,
            "evidenceKey": ekey,
            "folder": str(folder),
            "protocolStatus": protocol_status,
            "reasonCodes": baseline_reasons,
            "created": created_capture,
        }
    baseline_path = Path(baseline["selectedPath"])
    manifest["baseline"] = {
        "artifactId": baseline.get("selectedArtifactId"),
        "sha256": baseline["selectedHash"],
        "path": str(baseline_path),
        "deliveredAt": baseline.get("deliveredAt"),
        "assurance": baseline.get("baselineAssurance"),
        "deliveryEvidenceId": (
            baseline.get("deliveryEvidenceId")
            or (baseline.get("postDeliveryVerification") or {}).get("deliveryEvidenceId")
        ),
    }
    manifest["captureState"] = "baseline_resolved"
    manifest["updatedAt"] = now_iso()
    atomic_write_json(manifest_path, manifest)
    _set_index_state(case_dir, ckey, "baseline_resolved")
    try:
        comparison = compare_documents(baseline_path, canonical_target, allow_ocr=True)
    except Exception as exc:
        return _block_capture(
            case_dir,
            ckey,
            manifest_path,
            manifest,
            reason_codes=["PP-CAPTURE-FAILED"],
            detail=f"compare:{type(exc).__name__}",
            human_artifact_id=human_artifact_id,
            protocol_status=protocol_status,
        )
    if min(
        comparison["baseline"]["extractionConfidence"],
        comparison["humanArtifact"]["extractionConfidence"],
    ) < 0.75:
        return _block_capture(
            case_dir,
            ckey,
            manifest_path,
            manifest,
            reason_codes=["PP-OCR-LOW-CONFIDENCE"],
            detail="ocr_low_confidence",
            human_artifact_id=human_artifact_id,
            protocol_status=protocol_status,
        )
    revisao, medidas = _e_revisao(comparison)
    if not revisao:
        return _block_capture(
            case_dir,
            ckey,
            manifest_path,
            manifest,
            reason_codes=["PP-NOT-A-REVISION"],
            detail=(
                "nao_e_revisao_da_base:"
                f"texto_comum={medidas['sharedTokenRatio']}:"
                f"blocos_preservados={medidas['retainedBlockRuns']}"
            ),
            human_artifact_id=human_artifact_id,
            protocol_status=protocol_status,
        )
    private_comparison_path = folder / "COMPARAÇÃO_PRIVADA_IA_VS_HUMANO.json"
    atomic_write_json(private_comparison_path, comparison)
    markdown_path = folder / "MUDANÇAS_IA_VS_PEÇA_PROTOCOLADA.md"
    atomic_write_text(
        markdown_path,
        render_markdown(
            comparison,
            protocol_status=protocol_status,
            baseline_artifact_id=str(baseline.get("selectedArtifactId")),
            human_artifact_id=human_artifact_id,
        ),
    )
    existing_learning = read_json(
        case_dir / "n4_artifacts" / "F10_LEARNING_CANDIDATE.json",
        {},
    ) or {}
    existing_human_diff = read_json(
        case_dir / "n4_artifacts" / "F10_HUMAN_DIFF_CLASSIFICATION.json",
        {},
    ) or {}
    sanitized_changes = _preserve_change_reviews(
        _sanitize_changes(comparison["changes"]),
        existing_human_diff.get("changes") or [],
    )
    comparison_content = {
        "contentKey": ckey,
        "baseline": {
            "artifactId": baseline.get("selectedArtifactId"),
            "sha256": baseline["selectedHash"],
            "path": str(baseline_path),
            "deliveryEvidenceId": (baseline.get("postDeliveryVerification") or {}).get("deliveryEvidenceId"),
            "deliveredAt": baseline.get("deliveredAt"),
            "assurance": baseline.get("baselineAssurance"),
        },
        "humanArtifact": {
            "artifactId": human_artifact_id,
            "sha256": attachment_hash,
            "path": str(canonical_target),
        },
        "summary": comparison["summary"],
        "changes": sanitized_changes,
        "privateComparisonHash": sha256_file(private_comparison_path),
        "comparisonHash": comparison["comparisonHash"],
        "protocolEvidenceId": protocol_evidence_id,
    }
    comparison_artifact = _write_artifact_checked(
        case_dir,
        "F10_POST_PROTOCOL_DOCUMENT_COMPARISON.json",
        comparison_content,
        [baseline["selectedHash"], attachment_hash, protocol_artifact["contentHash"]],
        validate_document_comparison,
        producer_run_id=run_id,
    )
    comparison_id = f"comparison-{comparison_artifact['contentHash'][:16]}"
    candidates = _learning_candidates(
        comparison["changes"],
        existing_learning.get("candidates") or [],
    )
    learning_artifact = _write_artifact_checked(
        case_dir,
        "F10_LEARNING_CANDIDATE.json",
        {"contentKey": ckey, "comparisonId": comparison_id, "candidates": candidates},
        [comparison_artifact["contentHash"]],
        validate_learning_candidate,
        producer_run_id=run_id,
    )
    human_diff_content = {
        "contentKey": ckey,
        "comparisonId": comparison_id,
        "protocolStatus": protocol_status,
        "baselineHash": baseline["selectedHash"],
        "humanArtifactHash": attachment_hash,
        "changes": sanitized_changes,
        "regressionProposals": _regression_proposals(candidates),
    }
    human_diff_artifact = _write_artifact_checked(
        case_dir,
        "F10_HUMAN_DIFF_CLASSIFICATION.json",
        human_diff_content,
        [comparison_artifact["contentHash"], learning_artifact["contentHash"]],
        validate_learning,
        producer_run_id=run_id,
    )
    _record(
        case_dir,
        "post_protocol_diff_ready",
        f"{ckey}:diff:{comparison['comparisonHash']}:v1",
        {
            "contentKey": ckey,
            "humanArtifactId": human_artifact_id,
            "aiBaselineArtifactId": baseline.get("selectedArtifactId"),
            "protocolEvidenceId": protocol_evidence_id,
            "diffArtifactId": comparison_id,
            "protocolStatus": protocol_status,
            "openReasonCodes": [],
            "reasonSource": "comparison",
            "resolvedReasonCodes": ["PP-OCR-LOW-CONFIDENCE", "PP-CAPTURE-FAILED"],
        },
        artifact_hashes={
            "documentComparison": comparison_artifact["contentHash"],
            "humanDiff": human_diff_artifact["contentHash"],
        },
    )
    candidate_ids = [item["candidateId"] for item in candidates]
    _record(
        case_dir,
        "post_protocol_learning_proposed",
        f"{ckey}:learning:{learning_artifact['contentHash']}:v1",
        {
            "contentKey": ckey,
            "humanArtifactId": human_artifact_id,
            "aiBaselineArtifactId": baseline.get("selectedArtifactId"),
            "protocolEvidenceId": protocol_evidence_id,
            "diffArtifactId": comparison_id,
            "learningCandidateIds": candidate_ids,
            "protocolStatus": protocol_status,
            "openReasonCodes": [],
            "reasonSource": "learning",
        },
        artifact_hashes={"learningCandidate": learning_artifact["contentHash"]},
    )
    _record(
        case_dir,
        "post_protocol_review_pending",
        f"{ckey}:review-pending:v1",
        {
            "contentKey": ckey,
            "humanArtifactId": human_artifact_id,
            "aiBaselineArtifactId": baseline.get("selectedArtifactId"),
            "protocolEvidenceId": protocol_evidence_id,
            "diffArtifactId": comparison_id,
            "learningCandidateIds": candidate_ids,
            "protocolStatus": protocol_status,
            "openReasonCodes": [],
            "reasonSource": "review",
        },
    )
    manifest["comparison"] = {
        "comparisonId": comparison_id,
        "comparisonHash": comparison["comparisonHash"],
        "privateComparisonPath": str(private_comparison_path),
        "markdownPath": str(markdown_path),
    }
    manifest["updatedAt"] = now_iso()
    atomic_write_json(manifest_path, manifest)
    _set_index_state(case_dir, ckey, "review_pending")
    return {
        "status": "review_pending",
        "contentKey": ckey,
        "evidenceKey": ekey,
        "folder": str(folder),
        "protocolStatus": protocol_status,
        "baselineArtifactId": baseline.get("selectedArtifactId"),
        "baselineHash": baseline["selectedHash"],
        "comparisonId": comparison_id,
        "comparisonHash": comparison["comparisonHash"],
        "changeCount": comparison["summary"]["changeCount"],
        "learningCandidateIds": candidate_ids,
        "created": created_capture,
    }


def promote_learning(
    case_dir: Path,
    candidate_id: str,
    *,
    content_key_value: str = "",
    approved_by: str,
    fixture_id: str,
    test_id: str,
    evidence_runs: list[str],
    evidence_case_ids: list[str] | None = None,
    scope: str = "case",
    scope_key: str | None = None,
) -> dict:
    _require_post_protocol_enabled()
    if not re.fullmatch(r"[0-9a-f]{64}", content_key_value):
        raise ForjaN3Error("promoção exige contentKey SHA-256 explícito")
    path, payload = _learning_payload_for_content(
        case_dir,
        candidate_id,
        content_key_value,
    )
    candidates = payload.get("candidates") or []
    matches = [item for item in candidates if item.get("candidateId") == candidate_id]
    if len(matches) != 1:
        raise ForjaN3Error(f"candidato não encontrado de modo único: {candidate_id}")
    candidate = matches[0]
    if candidate.get("status") == "rejected":
        raise ForjaN3Error("candidato rejeitado não pode ser promovido sem nova proposta")
    if candidate.get("status") == "promoted":
        learning_changed = candidate.get("decision") != "approved"
        candidate["decision"] = "approved"
        findings = validate_learning_candidate(payload)
        if findings:
            raise ForjaN3Error("promoção existente inválida: " + "; ".join(
                item["detail"] for item in findings
            ))
        if learning_changed:
            _write_learning_payload(case_dir, path, payload)
        human_diff_path = path.with_name("F10_HUMAN_DIFF_CLASSIFICATION.json")
        human_diff = read_json(human_diff_path, {}) or {}
        proposal_changed = False
        for proposal in human_diff.get("regressionProposals") or []:
            if proposal.get("proposalId") == candidate_id and proposal.get("decision") != "approved":
                proposal.update(_regression_proposals([candidate])[0])
                proposal_changed = True
        human_findings = validate_learning(human_diff)
        if human_findings:
            raise ForjaN3Error("promoção existente reprovou human diff: " + "; ".join(
                item["detail"] for item in human_findings
            ))
        if proposal_changed:
            _write_human_diff_payload(case_dir, human_diff_path, human_diff)
        return candidate
    if candidate.get("origin") in {"unknown", "mixed"} and scope != "case":
        raise ForjaN3Error("origem não resolvida não pode ser promovida acima do caso")
    if scope != "case" and not str(scope_key or "").strip():
        raise ForjaN3Error("promoção acima do caso exige scope_key explícito")
    fixture_path = Path(fixture_id)
    if not fixture_path.is_absolute():
        fixture_path = FORJA / fixture_path
    if not fixture_path.is_file():
        raise ForjaN3Error(f"fixture não existe: {fixture_path}")
    test_target, _, test_selector = test_id.partition("::")
    test_path = Path(test_target)
    if not test_path.is_absolute():
        test_path = FORJA / test_path
    if not test_path.is_file():
        raise ForjaN3Error(f"teste não existe: {test_path}")
    canonical_test_id = str(test_path) + (f"::{test_selector}" if test_selector else "")
    completed = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", canonical_test_id],
        cwd=str(FORJA),
        capture_output=True,
        text=True,
        timeout=180,
        check=False,
    )
    receipt = {
        "schemaVersion": 1,
        "candidateId": candidate_id,
        "testId": canonical_test_id,
        "exitCode": completed.returncode,
        "passed": completed.returncode == 0,
        "executedAt": now_iso(),
        "outputHash": sha256_bytes((completed.stdout + completed.stderr).encode("utf-8")),
    }
    receipt_path = (
        case_dir
        / "private"
        / "post_protocol"
        / "promotion_tests"
        / f"{safe_component(candidate_id, 'candidate')}-{receipt['outputHash'][:12]}.json"
    )
    atomic_write_json(receipt_path, receipt)
    if completed.returncode != 0:
        raise ForjaN3Error(f"teste de promoção falhou: {canonical_test_id}")
    case_ids = sorted(set(evidence_case_ids or [case_dir.name]))
    if len(case_ids) < (2 if scope in {"office", "global"} else 1):
        raise ForjaN3Error("promoção exige evidências associadas a casos distintos")
    if len(set(evidence_runs)) < len(case_ids):
        raise ForjaN3Error("cada caso de evidência exige uma execução identificável")
    candidate.update({
        "status": "promoted",
        "decision": "approved",
        "scope": scope,
        "promotionStage": "human_approved",
        "approvedBy": approved_by,
        "fixtureId": str(fixture_path.resolve()),
        "testId": canonical_test_id,
        "testExecutionPath": str(receipt_path.resolve()),
        "evidenceRuns": sorted(set(evidence_runs)),
        "evidenceCaseIds": case_ids,
        "stageHistory": [
            "case_only",
            "fixture_added",
            "test_passed",
            "human_approved",
        ],
        "promotedAt": now_iso(),
    })
    findings = validate_learning_candidate(payload)
    if findings:
        raise ForjaN3Error("promoção reprovada: " + "; ".join(item["detail"] for item in findings))
    payload["updatedAt"] = now_iso()
    from forja_n4_common import expected_content_hash

    payload["contentHash"] = expected_content_hash(payload)
    _write_learning_payload(case_dir, path, payload)
    human_diff_path = path.with_name("F10_HUMAN_DIFF_CLASSIFICATION.json")
    human_diff = read_json(human_diff_path, {}) or {}
    for proposal in human_diff.get("regressionProposals") or []:
        if proposal.get("proposalId") == candidate_id:
            proposal.update(_regression_proposals([candidate])[0])
    human_findings = validate_learning(human_diff)
    if human_findings:
        raise ForjaN3Error("promoção reprovou human diff: " + "; ".join(
            item["detail"] for item in human_findings
        ))
    _write_human_diff_payload(case_dir, human_diff_path, human_diff)
    rule = register_promoted_rule(
        source_case_id=case_dir.name,
        candidate=candidate,
        scope_key=scope_key,
    )
    state = derive_state(case_dir)
    post = state.get("postProtocol") or {}
    _record(
        case_dir,
        "post_protocol_learning_promoted",
        f"{candidate_id}:promoted:{payload['contentHash']}",
        {
            "contentKey": post.get("contentKey"),
            "humanArtifactId": post.get("humanArtifactId"),
            "aiBaselineArtifactId": post.get("aiBaselineArtifactId"),
            "protocolEvidenceId": post.get("protocolEvidenceId"),
            "diffArtifactId": post.get("diffArtifactId"),
            "promotedLearningIds": [candidate_id],
            "protocolStatus": post.get("protocolStatus"),
            "openReasonCodes": [],
        },
        artifact_hashes={"learningCandidate": payload["contentHash"]},
    )
    return {**candidate, "activeRuleId": rule["ruleId"]}


def _learning_payload_for_content(
    case_dir: Path,
    candidate_id: str,
    content_key_value: str = "",
) -> tuple[Path, dict]:
    current = case_dir / "n4_artifacts" / "F10_LEARNING_CANDIDATE.json"
    paths = [current, *sorted(
        (case_dir / "n4_artifacts" / "post_protocol_history").glob(
            "*/F10_LEARNING_CANDIDATE.json"
        )
    )]
    matches: list[tuple[Path, dict]] = []
    for path in paths:
        payload = read_json(path, None)
        if not isinstance(payload, dict) or payload.get("contentKey") != content_key_value:
            continue
        if any(item.get("candidateId") == candidate_id for item in payload.get("candidates") or []):
            matches.append((path, payload))
    if len(matches) != 1:
        raise ForjaN3Error(
            f"candidato/contentKey não encontrado de modo único: {candidate_id}/{content_key_value}"
        )
    return matches[0]


def _write_learning_payload(case_dir: Path, path: Path, payload: dict) -> None:
    if path.resolve() == (
        case_dir / "n4_artifacts" / "F10_LEARNING_CANDIDATE.json"
    ).resolve():
        write_artifact(case_dir, "F10_LEARNING_CANDIDATE.json", payload)
        return
    from forja_n4_common import expected_content_hash

    payload["updatedAt"] = now_iso()
    payload["contentHash"] = expected_content_hash(payload)
    atomic_write_json(path, payload)


def _write_human_diff_payload(case_dir: Path, path: Path, payload: dict) -> None:
    if path.resolve() == (
        case_dir / "n4_artifacts" / "F10_HUMAN_DIFF_CLASSIFICATION.json"
    ).resolve():
        write_artifact(case_dir, "F10_HUMAN_DIFF_CLASSIFICATION.json", payload)
        return
    from forja_n4_common import expected_content_hash

    payload["updatedAt"] = now_iso()
    payload["contentHash"] = expected_content_hash(payload)
    atomic_write_json(path, payload)


def resolve_learning_origin(
    case_dir: Path,
    candidate_id: str,
    *,
    content_key_value: str,
    origin: str,
    evidence_id: str,
    decided_by: str,
) -> dict:
    _require_post_protocol_enabled()
    if not re.fullmatch(r"[0-9a-f]{64}", content_key_value):
        raise ForjaN3Error("resolve-origin exige contentKey SHA-256 explícito")
    if origin in {"unknown", "mixed"}:
        raise ForjaN3Error("resolve-origin exige uma origem determinada")
    path, payload = _learning_payload_for_content(
        case_dir,
        candidate_id,
        content_key_value,
    )
    matches = [item for item in payload.get("candidates") or [] if item.get("candidateId") == candidate_id]
    if len(matches) != 1:
        raise ForjaN3Error(f"candidato não encontrado de modo único: {candidate_id}")
    candidate = matches[0]
    if candidate.get("status") == "promoted":
        raise ForjaN3Error("origem de candidato promovido é imutável")
    candidate.update({
        "origin": origin,
        "originEvidenceId": evidence_id,
        "originDecidedBy": decided_by,
        "originDecidedAt": now_iso(),
    })
    findings = validate_learning_candidate(payload)
    if findings:
        raise ForjaN3Error("resolução de origem reprovada: " + "; ".join(item["detail"] for item in findings))
    _write_learning_payload(case_dir, path, payload)
    human_diff_path = path.with_name("F10_HUMAN_DIFF_CLASSIFICATION.json")
    human_diff = read_json(human_diff_path, {}) or {}
    for change in human_diff.get("changes") or []:
        if change.get("changeFingerprint") == candidate.get("changeFingerprint"):
            change.update({
                "origin": origin,
                "reviewDecision": "accepted_for_fixture",
                "reviewedBy": decided_by,
                "reviewedAt": now_iso(),
            })
    human_findings = validate_learning(human_diff)
    if human_findings:
        raise ForjaN3Error("resolução de origem reprovou human diff: " + "; ".join(
            item["detail"] for item in human_findings
        ))
    _write_human_diff_payload(case_dir, human_diff_path, human_diff)
    return candidate


def rebuild_comparison(case_dir: Path, ckey: str, *, producer_run_id: str | None = None) -> dict:
    """Regenera JSON/Markdown derivados após evolução versionada do comparador."""
    _require_post_protocol_enabled()
    case_dir = case_dir.resolve()
    index = _load_index(case_dir)
    entry = (index.get("contents") or {}).get(ckey)
    if not entry:
        raise ForjaN3Error(f"contentKey não localizado: {ckey}")
    manifest_path = Path(entry["manifestPath"])
    manifest = read_json(manifest_path, None)
    if not isinstance(manifest, dict):
        raise ForjaN3Error("manifesto de protocolo/proveniência ausente")
    existing_learning = read_json(
        case_dir / "n4_artifacts" / "F10_LEARNING_CANDIDATE.json",
        {},
    ) or {}
    baseline = manifest.get("baseline") or {}
    baseline_path = Path(str(baseline.get("path") or ""))
    human_path = Path(str(manifest.get("canonicalPath") or ""))
    if not baseline_path.is_file() or sha256_file(baseline_path) != baseline.get("sha256"):
        raise ForjaN3Error("base registrada no manifesto está ausente ou mudou")
    if not human_path.is_file() or sha256_file(human_path) != manifest.get("sha256"):
        raise ForjaN3Error("peça humana registrada está ausente ou mudou")
    run_id = producer_run_id or new_id("post-protocol-rebuild")
    comparison = compare_documents(baseline_path, human_path, allow_ocr=True)
    if min(
        comparison["baseline"]["extractionConfidence"],
        comparison["humanArtifact"]["extractionConfidence"],
    ) < 0.75:
        return _block_capture(
            case_dir,
            ckey,
            manifest_path,
            manifest,
            reason_codes=["PP-OCR-LOW-CONFIDENCE"],
            detail="rebuild_ocr_low_confidence",
            human_artifact_id=manifest["humanArtifactId"],
            protocol_status=manifest["protocolStatus"],
        )
    revisao, medidas = _e_revisao(comparison)
    if not revisao:
        return _block_capture(
            case_dir,
            ckey,
            manifest_path,
            manifest,
            reason_codes=["PP-NOT-A-REVISION"],
            detail=(
                "rebuild_nao_e_revisao_da_base:"
                f"texto_comum={medidas['sharedTokenRatio']}:"
                f"blocos_preservados={medidas['retainedBlockRuns']}"
            ),
            human_artifact_id=manifest["humanArtifactId"],
            protocol_status=manifest["protocolStatus"],
        )
    folder = manifest_path.parent
    private_path = folder / "COMPARAÇÃO_PRIVADA_IA_VS_HUMANO.json"
    markdown_path = folder / "MUDANÇAS_IA_VS_PEÇA_PROTOCOLADA.md"
    atomic_write_json(private_path, comparison)
    atomic_write_text(
        markdown_path,
        render_markdown(
            comparison,
            protocol_status=manifest["protocolStatus"],
            baseline_artifact_id=baseline["artifactId"],
            human_artifact_id=manifest["humanArtifactId"],
        ),
    )
    existing_human_diff = read_json(
        case_dir / "n4_artifacts" / "F10_HUMAN_DIFF_CLASSIFICATION.json",
        {},
    ) or {}
    sanitized = _preserve_change_reviews(
        _sanitize_changes(comparison["changes"]),
        existing_human_diff.get("changes") or [],
    )
    protocol_artifact = read_json(
        case_dir / "n4_artifacts" / "F10_PROTOCOL_EVIDENCE.json",
        {},
    ) or {}
    comparison_content = {
        "contentKey": ckey,
        "baseline": {
            "artifactId": baseline["artifactId"],
            "sha256": baseline["sha256"],
            "path": str(baseline_path),
            "deliveryEvidenceId": baseline.get("deliveryEvidenceId"),
            "deliveredAt": baseline.get("deliveredAt"),
        },
        "humanArtifact": {
            "artifactId": manifest["humanArtifactId"],
            "sha256": manifest["sha256"],
            "path": str(human_path),
        },
        "summary": comparison["summary"],
        "changes": sanitized,
        "privateComparisonHash": sha256_file(private_path),
        "comparisonHash": comparison["comparisonHash"],
        "protocolEvidenceId": (derive_state(case_dir).get("postProtocol") or {}).get("protocolEvidenceId"),
    }
    comparison_artifact = _write_artifact_checked(
        case_dir,
        "F10_POST_PROTOCOL_DOCUMENT_COMPARISON.json",
        comparison_content,
        [baseline["sha256"], manifest["sha256"], str(protocol_artifact.get("contentHash") or "")],
        validate_document_comparison,
        producer_run_id=run_id,
    )
    comparison_id = f"comparison-{comparison_artifact['contentHash'][:16]}"
    candidates = _learning_candidates(
        comparison["changes"],
        existing_learning.get("candidates") or [],
    )
    learning_artifact = _write_artifact_checked(
        case_dir,
        "F10_LEARNING_CANDIDATE.json",
        {"contentKey": ckey, "comparisonId": comparison_id, "candidates": candidates},
        [comparison_artifact["contentHash"]],
        validate_learning_candidate,
        producer_run_id=run_id,
    )
    human_diff = _write_artifact_checked(
        case_dir,
        "F10_HUMAN_DIFF_CLASSIFICATION.json",
        {
            "contentKey": ckey,
            "comparisonId": comparison_id,
            "protocolStatus": manifest["protocolStatus"],
            "baselineHash": baseline["sha256"],
            "humanArtifactHash": manifest["sha256"],
            "changes": sanitized,
            "regressionProposals": _regression_proposals(candidates),
        },
        [comparison_artifact["contentHash"], learning_artifact["contentHash"]],
        validate_learning,
        producer_run_id=run_id,
    )
    post = derive_state(case_dir).get("postProtocol") or {}
    _record(
        case_dir,
        "post_protocol_diff_ready",
        f"{ckey}:diff:{comparison['comparisonHash']}:v1",
        {
            "contentKey": ckey,
            "humanArtifactId": manifest["humanArtifactId"],
            "aiBaselineArtifactId": baseline["artifactId"],
            "protocolEvidenceId": post.get("protocolEvidenceId"),
            "diffArtifactId": comparison_id,
            "protocolStatus": manifest["protocolStatus"],
            "openReasonCodes": [],
        },
        artifact_hashes={
            "documentComparison": comparison_artifact["contentHash"],
            "humanDiff": human_diff["contentHash"],
        },
    )
    _record(
        case_dir,
        "post_protocol_learning_proposed",
        f"{ckey}:learning:{learning_artifact['contentHash']}:v1",
        {
            "contentKey": ckey,
            "humanArtifactId": manifest["humanArtifactId"],
            "aiBaselineArtifactId": baseline["artifactId"],
            "protocolEvidenceId": post.get("protocolEvidenceId"),
            "diffArtifactId": comparison_id,
            "learningCandidateIds": [item["candidateId"] for item in candidates],
            "protocolStatus": manifest["protocolStatus"],
            "openReasonCodes": [],
        },
        artifact_hashes={"learningCandidate": learning_artifact["contentHash"]},
    )
    manifest["comparison"] = {
        "comparisonId": comparison_id,
        "comparisonHash": comparison["comparisonHash"],
        "privateComparisonPath": str(private_path),
        "markdownPath": str(markdown_path),
        "rebuiltAt": now_iso(),
    }
    manifest["updatedAt"] = now_iso()
    atomic_write_json(manifest_path, manifest)
    _set_index_state(case_dir, ckey, "review_pending")
    return {
        "status": "review_pending",
        "contentKey": ckey,
        "comparisonId": comparison_id,
        "comparisonHash": comparison["comparisonHash"],
        "summary": comparison["summary"],
        "markdownPath": str(markdown_path),
    }


def _message_header(message: dict, name: str) -> str:
    for header in (message.get("payload") or {}).get("headers") or []:
        if str(header.get("name") or "").casefold() == name.casefold():
            return str(header.get("value") or "")
    return ""


def _case_for_demand(demand_id: str, demands: list[dict]) -> str | None:
    links = read_json(OFFICE_DATA / "forja_case_links.json", {"links": {}}) or {}
    matches: set[str] = {
        str(case_id)
        for case_id, demand in (links.get("links") or {}).items()
        if str(demand or "") == demand_id
    }
    item = next((entry for entry in demands if entry.get("id") == demand_id), {})
    case_id = ((item.get("forja") or {}).get("caseId") if isinstance(item.get("forja"), dict) else None)
    if case_id and (FORJA / "state" / case_id).is_dir():
        matches.add(str(case_id))
    for case_dir in (FORJA / "state").iterdir():
        if not case_dir.is_dir():
            continue
        manifest = read_json(case_dir / "FORJA_CASE_MANIFEST.json", {}) or {}
        state = read_json(case_dir / "FORJA_N3_STATE.json", {}) or {}
        linked = str(manifest.get("demandId") or state.get("demandId") or "")
        if linked == demand_id:
            matches.add(case_dir.name)
    if len(matches) == 1:
        return next(iter(matches))
    return None


def _sender_allowed(message: dict) -> bool:
    config = load_config()
    gmail = ((config.get("postProtocol") or {}).get("gmail") or {})
    allowed_domains = {str(item).casefold().lstrip("@") for item in gmail.get("allowedDomains") or []}
    allowed_addresses = {str(item).casefold() for item in gmail.get("allowedAddresses") or []}
    addresses = {
        address.casefold()
        for _name, address in getaddresses([_message_header(message, "From")])
        if address
    }
    return bool(addresses) and all(
        address in allowed_addresses or address.rsplit("@", 1)[-1] in allowed_domains
        for address in addresses
    )


def _registrar_retorno_sem_anexo(case_id: str | None, message: dict) -> None:
    """Deixa a correção que veio no corpo do e-mail registrada no caso.

    O relatório da varredura é sobrescrito a cada execução: registrar só nele
    seria perder a correção na próxima rodada. Aqui ela fica ancorada no caso,
    acumula por mensagem e é idempotente.

    Guarda-se o localizador e o assunto, não o corpo. O assunto entra porque é
    o que permite reencontrar a mensagem sem abrir uma a uma; o corpo é o
    conteúdo da correção e vive no Gmail, não em artefato nosso. Quem tria abre
    a mensagem — o mesmo desenho do resto do loop, que guarda hash e localizador
    e nunca o trecho.
    """
    # Demanda reconhecida sem caso FORJA aberto ainda: a correção existe do
    # mesmo jeito e não pode ficar só no relatório da varredura, que é
    # sobrescrito. Vai para uma lista própria, declarada como sem caso.
    caminho = (
        FORJA / "state" / case_id / "n4_artifacts" / "F10_RETORNO_SEM_ANEXO.json"
        if case_id else
        FORJA / "private" / "post_protocol" / "RETORNOS_SEM_ANEXO_SEM_CASO.json"
    )
    case_id = case_id or "(sem caso FORJA aberto)"
    atual = read_json(caminho, None) or {
        "schema": "FORJA-RETORNO-SEM-ANEXO-v1",
        "porque": ("Mensagens do escritório vinculadas a este caso que trazem correção "
                   "no corpo do e-mail, sem peça anexada para comparar. Ficam aqui para "
                   "triagem humana: não há diff possível, e classificar prosa por "
                   "heurística seria inventar. O texto permanece no e-mail."),
        "caseId": case_id,
        "mensagens": [],
    }
    message_id = str(message.get("id") or "")
    if any(item.get("messageId") == message_id for item in atual["mensagens"]):
        return
    atual["mensagens"].append({
        "messageId": message_id,
        "threadId": str(message.get("threadId") or ""),
        "assunto": _message_header(message, "Subject"),
        "recebidoEm": _message_header(message, "Date"),
        "triagem": "pendente",
    })
    atual["atualizadoEm"] = now_iso()
    caminho.parent.mkdir(parents=True, exist_ok=True)
    atomic_write_json(caminho, atual)


def consulta_padrao(*, desde: str = "2026/06/01") -> str:
    """A consulta do varredor, derivada da lista de remetentes autorizados.

    Antes ela filtrava por `has:attachment`, e a esteira ficava cega para a
    correção que vem escrita no corpo do e-mail. Tirar só o filtro não bastava:
    sem ele a consulta traz a caixa inteira, e a cota de mensagens se esgota em
    correspondência que nem é do escritório — medido em 06/08/2026, 60 de 60
    mensagens vieram de remetente não autorizado e nenhuma correção foi lida.

    Filtrar por QUEM manda, e não por se veio anexo, resolve os dois: a
    mensagem do escritório chega tendo anexo ou não, e a cota não se gasta com
    o resto. A lista é a mesma que autoriza a ingestão — não há duas verdades
    sobre quem é remetente legítimo.
    """
    gmail = ((load_config().get("postProtocol") or {}).get("gmail") or {})
    remetentes = [f"@{str(item).lstrip('@')}" for item in gmail.get("allowedDomains") or []]
    remetentes += [str(item) for item in gmail.get("allowedAddresses") or []]
    base = f"in:anywhere after:{desde} -in:sent -in:trash -in:spam"
    if not remetentes:
        # Sem allowlist configurada nada seria ingerido de qualquer modo; a
        # consulta ampla ao menos deixa o diagnóstico visível.
        return base
    alvo = " OR ".join(f"from:{item}" for item in remetentes)
    return f"{base} ({alvo})"


def scan_gmail(*, query: str, max_results: int = 100, shadow: bool = False) -> dict:
    """Consulta Gmail em leitura, usa o matcher da gestão e ingere vínculos únicos."""
    if not feature_enabled("n4PostProtocolV1"):
        return {
            "ok": True,
            "status": "disabled",
            "query": query,
            "shadow": shadow,
            "messagesScanned": 0,
            "processed": 0,
            "quarantined": 0,
            "results": [],
            "quarantine": [],
            "updatedAt": now_iso(),
        }
    sys.path.insert(0, str(OFFICE_SCRIPTS))
    from audit_delivered_docs import match_demands
    from gmail_gws_update import (
        attachment_parts,
        body_from_payload,
        get_attachment,
        get_message,
        list_ids,
    )

    demand_payload = read_json(OFFICE_DATA / "demandas.json", {"demandas": []}) or {}
    demands = demand_payload.get("demandas") or []
    message_ids, status = list_ids(query, max_results=max_results)
    if not status.get("ok"):
        return {"ok": False, "status": "gmail_degraded", "error": status.get("error"), "query": query}
    results = []
    quarantine = []
    for message_id in message_ids:
        message, message_status = get_message(message_id)
        if not message_status.get("ok") or not isinstance(message, dict):
            continue
        if not _sender_allowed(message):
            quarantine.append({
                "messageId": message_id,
                "threadId": message.get("threadId"),
                "reasonCode": "PP-SENDER-NOT-ALLOWED",
                "matchCount": 0,
                "attachmentCount": 0,
            })
            continue
        matches = match_demands(message, demands)
        all_parts = [
            part for part in attachment_parts(message)
            if Path(part.get("filename") or "").suffix.lower() in SUPPORTED_RETURN_EXTENSIONS
        ]
        if not all_parts:
            # Correção do titular que chega como texto do e-mail, sem peça
            # anexada — "tire aquele argumento", "o prazo é outro", "não use
            # esse precedente". Não há o que comparar, e por isso a esteira
            # inteira é cega para ela; era literalmente descartada em silêncio,
            # e a própria consulta padrão pedia `has:attachment`, de modo que a
            # mensagem nem chegava a ser lida. Aqui ela passa a existir: fica
            # registrada com o vínculo ao caso, para triagem humana. Nenhum
            # trecho do corpo é copiado — quem tria abre a mensagem.
            if len(matches) == 1:
                quarantine.append({
                    "messageId": message_id,
                    "threadId": message.get("threadId"),
                    "reasonCode": "PP-NO-RETURN-ATTACHMENT",
                    "matchCount": 1,
                    "attachmentCount": 0,
                })
                if not shadow:
                    _registrar_retorno_sem_anexo(
                        _case_for_demand(matches[0], demands), message)
            continue
        parts, evidence_parts, selection_reason = _select_return_parts(all_parts)
        if selection_reason:
            quarantine.append({
                "messageId": message_id,
                "threadId": message.get("threadId"),
                "reasonCode": selection_reason,
                "matchCount": 0,
                "attachmentCount": len(all_parts),
            })
            continue
        if len(matches) != 1:
            quarantine.append({
                "messageId": message_id,
                "threadId": message.get("threadId"),
                "reasonCode": "PP-01",
                "matchCount": len(matches),
                "attachmentCount": len(all_parts),
            })
            continue
        raw_received_at = _message_header(message, "Date")
        try:
            parsed_received = parsedate_to_datetime(raw_received_at)
            received_at = parsed_received.astimezone().isoformat(timespec="seconds")
        except (TypeError, ValueError, OverflowError):
            received_at = now_iso()
        case_id = _case_for_demand(matches[0], demands)
        if not case_id:
            quarantine.append({
                "messageId": message_id,
                "threadId": message.get("threadId"),
                "reasonCode": "PP-01",
                "matchCount": 1,
                "attachmentCount": len(all_parts),
            })
            continue
        demand = next((item for item in demands if item.get("id") == matches[0]), {})
        baseline, baseline_reasons = resolve_ai_baseline(
            FORJA / "state" / case_id,
            received_at=received_at,
        )
        if baseline is None:
            try:
                backfill = backfill_baseline_from_gmail(
                    FORJA / "state" / case_id,
                    demand,
                    human_suffix=Path(parts[0]["filename"]).suffix.lower(),
                    received_at=received_at,
                    get_message=get_message,
                    get_attachment=get_attachment,
                    shadow=shadow,
                )
            except Exception as exc:
                quarantine.append({
                    "messageId": message_id,
                    "threadId": message.get("threadId"),
                    "reasonCode": "PP-BASELINE-MISSING",
                    "errorType": type(exc).__name__,
                    "matchCount": 1,
                    "attachmentCount": len(all_parts),
                })
                continue
            if shadow and backfill and backfill.get("status") == "available":
                results.append({
                    "status": "shadow_match",
                    "caseId": case_id,
                    "demandId": matches[0],
                    "messageId": message_id,
                    "attachmentId": parts[0]["attachmentId"],
                    "attachmentSuffix": Path(parts[0]["filename"]).suffix.lower(),
                    "baselineResolution": "gmail_exact_attachment_backfill_available",
                    "baselineMessageId": backfill["messageId"],
                })
                continue
            if not shadow and backfill and backfill.get("status") == "created":
                baseline, baseline_reasons = resolve_ai_baseline(
                    FORJA / "state" / case_id,
                    received_at=received_at,
                )
            if baseline is None:
                reason_code = (
                    backfill.get("reasonCode")
                    if isinstance(backfill, dict) and backfill.get("reasonCode")
                    else baseline_reasons[0]
                )
                quarantine.append({
                    "messageId": message_id,
                    "threadId": message.get("threadId"),
                    "reasonCode": reason_code,
                    "matchCount": 1,
                    "attachmentCount": len(all_parts),
                })
                continue
        subject = _message_header(message, "Subject")
        body = body_from_payload(message.get("payload") or {})
        process_match = CNJ_RE.search(subject)
        downloaded_evidence_paths: list[Path] = []
        if not shadow:
            for evidence_part in evidence_parts:
                evidence_payload, evidence_status = get_attachment(message_id, evidence_part["attachmentId"])
                if not evidence_status.get("ok") or not evidence_payload or not evidence_payload.get("data"):
                    continue
                evidence_raw = base64.urlsafe_b64decode(
                    evidence_payload["data"] + "=" * (-len(evidence_payload["data"]) % 4)
                )
                evidence_stage = FORJA / "state" / case_id / "private" / "post_protocol" / "inbox_staging"
                evidence_stage.mkdir(parents=True, exist_ok=True)
                evidence_path = evidence_stage / (
                    f"{sha256_bytes(evidence_raw)}{Path(evidence_part['filename']).suffix.lower()}"
                )
                if not evidence_path.exists():
                    evidence_path.write_bytes(evidence_raw)
                downloaded_evidence_paths.append(evidence_path)
        for part in parts:
            if shadow:
                results.append({
                    "status": "shadow_match",
                    "caseId": case_id,
                    "demandId": matches[0],
                    "messageId": message_id,
                    "attachmentId": part["attachmentId"],
                    "attachmentSuffix": Path(part["filename"]).suffix.lower(),
                })
                continue
            attachment_payload, attachment_status = get_attachment(message_id, part["attachmentId"])
            if not attachment_status.get("ok") or not attachment_payload or not attachment_payload.get("data"):
                quarantine.append({
                    "messageId": message_id,
                    "threadId": message.get("threadId"),
                    "reasonCode": "PP-06",
                    "matchCount": 1,
                    "attachmentCount": 1,
                })
                continue
            raw = base64.urlsafe_b64decode(
                attachment_payload["data"] + "=" * (-len(attachment_payload["data"]) % 4)
            )
            staging = FORJA / "state" / case_id / "private" / "post_protocol" / "inbox_staging"
            staging.mkdir(parents=True, exist_ok=True)
            stage_path = staging / f"{sha256_bytes(raw)}{Path(part['filename']).suffix.lower()}"
            if not stage_path.exists():
                stage_path.write_bytes(raw)
            try:
                result = ingest_return(
                    FORJA / "state" / case_id,
                    stage_path,
                    account_id="gmail-me",
                    thread_id=str(message.get("threadId") or ""),
                    message_id=message_id,
                    attachment_id=part["attachmentId"],
                    received_at=received_at,
                    original_name=part["filename"],
                    piece_name=subject.removeprefix("Re:").strip() or Path(part["filename"]).stem,
                    process_id=process_match.group(0) if process_match else "",
                    declaration_text=body,
                    evidence_paths=downloaded_evidence_paths,
                )
                results.append({"caseId": case_id, "demandId": matches[0], **result})
            except Exception as exc:
                quarantine.append({
                    "messageId": message_id,
                    "threadId": message.get("threadId"),
                    "reasonCode": "PP-CAPTURE-FAILED",
                    "errorType": type(exc).__name__,
                    "matchCount": 1,
                    "attachmentCount": 1,
                })
    report = {
        "ok": True,
        "query": query,
        "shadow": shadow,
        "messagesScanned": len(message_ids),
        "processed": len(results),
        "quarantined": len(quarantine),
        "results": results,
        "quarantine": quarantine,
        "updatedAt": now_iso(),
    }
    atomic_write_json(FORJA / "private" / "post_protocol" / "POST_PROTOCOL_LAST_RUN.json", report)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Loop pós-protocolo da FORJA")
    sub = parser.add_subparsers(dest="command", required=True)
    ingest = sub.add_parser("ingest")
    ingest.add_argument("case")
    ingest.add_argument("attachment", type=Path)
    ingest.add_argument("--account-id", required=True)
    ingest.add_argument("--thread-id", required=True)
    ingest.add_argument("--message-id", required=True)
    ingest.add_argument("--attachment-id", required=True)
    ingest.add_argument("--received-at", required=True)
    ingest.add_argument("--original-name")
    ingest.add_argument("--piece-name", default="PETIÇÃO")
    ingest.add_argument("--process-id", default="")
    ingest.add_argument("--declaration-text", default="")
    ingest.add_argument("--evidence", action="append", type=Path, default=[])
    scan = sub.add_parser("scan-gmail")
    # A consulta sai da lista de remetentes autorizados, e não de `has:attachment`
    # — ver `consulta_padrao`.
    scan.add_argument("--query", default=None)
    scan.add_argument("--max-results", type=int, default=100)
    scan.add_argument("--shadow", action="store_true")
    promote = sub.add_parser("promote")
    promote.add_argument("case")
    promote.add_argument("candidate_id")
    promote.add_argument("--content-key", required=True)
    promote.add_argument("--approved-by", required=True)
    promote.add_argument("--fixture-id", required=True)
    promote.add_argument("--test-id", required=True)
    promote.add_argument("--evidence-run", action="append", required=True)
    promote.add_argument("--evidence-case", action="append", required=True)
    promote.add_argument("--scope", choices=["case", "product_type", "tribunal", "office", "global"], default="case")
    promote.add_argument("--scope-key")
    rebuild = sub.add_parser("rebuild")
    rebuild.add_argument("case")
    rebuild.add_argument("content_key")
    resolve_origin = sub.add_parser("resolve-origin")
    resolve_origin.add_argument("case")
    resolve_origin.add_argument("candidate_id")
    resolve_origin.add_argument("--content-key", required=True)
    resolve_origin.add_argument("--origin", required=True)
    resolve_origin.add_argument("--evidence-id", required=True)
    resolve_origin.add_argument("--decided-by", required=True)
    args = parser.parse_args()
    if args.command == "scan-gmail":
        result = scan_gmail(query=args.query or consulta_padrao(),
                            max_results=args.max_results, shadow=args.shadow)
    elif args.command == "promote":
        result = promote_learning(
            resolve_case_dir(args.case),
            args.candidate_id,
            content_key_value=args.content_key,
            approved_by=args.approved_by,
            fixture_id=args.fixture_id,
            test_id=args.test_id,
            evidence_runs=args.evidence_run,
            evidence_case_ids=args.evidence_case,
            scope=args.scope,
            scope_key=args.scope_key,
        )
    elif args.command == "resolve-origin":
        result = resolve_learning_origin(
            resolve_case_dir(args.case),
            args.candidate_id,
            content_key_value=args.content_key,
            origin=args.origin,
            evidence_id=args.evidence_id,
            decided_by=args.decided_by,
        )
    elif args.command == "rebuild":
        result = rebuild_comparison(resolve_case_dir(args.case), args.content_key)
    else:
        result = ingest_return(
            resolve_case_dir(args.case),
            args.attachment,
            account_id=args.account_id,
            thread_id=args.thread_id,
            message_id=args.message_id,
            attachment_id=args.attachment_id,
            received_at=args.received_at,
            original_name=args.original_name,
            piece_name=args.piece_name,
            process_id=args.process_id,
            declaration_text=args.declaration_text,
            evidence_paths=args.evidence,
        )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
