"""Synchronize FORJA N3 derived state into the office-management sidecar."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from office_io import InterProcessLock, atomic_write_json, now_iso, read_json


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
FORJA = WORKSPACE / "_FORJA_HARNESS"
STATE_ROOT = FORJA / "state"
DATA_DIR = ROOT / "data"
DEMANDS = DATA_DIR / "demandas.json"
SIDECAR = DATA_DIR / "forja_status.json"
LINKS = DATA_DIR / "forja_case_links.json"
MANUAL = DATA_DIR / "intervencoes_manuais.json"
LOCK = DATA_DIR / ".forja-status.lock"
SHADOW_REPLAY = FORJA / "reports" / "N3_SHADOW_REPLAY_2026-07-09.json"

sys.path.insert(0, str(FORJA))
from forja_n3_common import ForjaN3Error, feature_enabled, sha256_file  # noqa: E402
from forja_state_machine import derive_state, load_events, record_event  # noqa: E402


NEXT_ACTIONS = {
    "not_run": "A FORJA ainda não foi executada nesta demanda.",
    "queued": "Iniciar a reconciliação F0.",
    "running": "Concluir a fase em andamento e seus gates.",
    "blocked": "Resolver os bloqueadores registrados pela FORJA.",
    "ready_for_review": "Revisar o pacote produzido pela FORJA.",
    "draft_awaiting_review": "Revisar o rascunho e decidir o envio.",
    "sent_confirmed": "Registrar sincronização final e encerramento F10.",
    "fulfilled_by_forja_f10": "Ciclo encerrado com evidência.",
    "fulfilled_by_reconciliation": "Cumprimento anterior reconhecido por evidência.",
    "superseded": "Consultar o caso canônico substituto.",
}

REPLAY_BLOCKER_LABELS = {
    "silent_phase_regression": "Regressão de fase detectada no histórico; a N3 exige reabertura formal.",
    "pending_source_in_review_cycle": "Há fonte não autorizada no ciclo de revisão; resolver antes da promoção.",
    "invalid_json": "Há arquivo JSON inválido no caso.",
    "declared_artifact_missing": "Há artefato declarado que não foi localizado.",
    "visual_gate_failed": "O replay visual encontrou diagrama que não passa no gate N3.",
    "legacy_state_import_divergence": "O estado antigo divergiu da visão N3 reconstruída.",
    "original_state_changed": "O estado histórico mudou durante o replay.",
}

POST_PROTOCOL_NEXT_ACTIONS = {
    "not_detected": "Aguardar retorno da versão humana.",
    "candidate_detected": "Resolver o vínculo do retorno com o caso.",
    "identity_ambiguous": "Resolver manualmente a identidade do caso.",
    "captured": "Classificar a evidência de protocolo e localizar a base entregue.",
    "claimed": "Obter elo verificável entre o protocolo e o arquivo.",
    "verified": "Comparar com a versão exata entregue pela FORJA.",
    "ai_baseline_unresolved": "Reconstruir a seleção F9/F10 pelo hash entregue.",
    "diff_ready": "Revisar as mudanças materiais detectadas.",
    "review_pending": "Revisar e decidir as lições candidatas.",
    "learning_proposed": "Revisar e decidir as lições candidatas.",
    "learning_promoted": "Monitorar a lição no próximo ciclo.",
    "complete": "Loop pós-protocolo concluído.",
}


def _post_protocol_summary(state: dict) -> dict:
    """Projeção fechada: IDs, estados e reason codes; nunca prosa jurídica."""
    source = state.get("postProtocol") or {}
    status = str(source.get("status") or "not_detected")
    reason_codes = [
        str(code)
        for code in source.get("openReasonCodes") or []
        if re.fullmatch(r"PP-[A-Z0-9-]+", str(code))
    ]
    return {
        "status": status,
        "protocolStatus": source.get("protocolStatus"),
        "contentKey": source.get("contentKey"),
        "humanArtifactId": source.get("humanArtifactId"),
        "aiBaselineArtifactId": source.get("aiBaselineArtifactId"),
        "protocolEvidenceId": source.get("protocolEvidenceId"),
        "diffArtifactId": source.get("diffArtifactId"),
        "learningCandidateCount": len(source.get("learningCandidateIds") or []),
        "promotedLearningCount": len(source.get("promotedLearningIds") or []),
        "reasonCodes": sorted(set(reason_codes)),
        "nextAction": POST_PROTOCOL_NEXT_ACTIONS.get(status, "Conferir o estado pós-protocolo."),
        "lastEventSeq": source.get("lastEventSeq"),
    }


def _demand_ids(path: Path = DEMANDS) -> set[str]:
    payload = read_json(path, {"demandas": []}) or {}
    return {str(item.get("id")) for item in payload.get("demandas") or [] if item.get("id")}


def _demand_records(path: Path = DEMANDS) -> dict[str, dict]:
    payload = read_json(path, {"demandas": []}) or {}
    return {
        str(item.get("id")): item
        for item in payload.get("demandas") or []
        if isinstance(item, dict) and item.get("id")
    }


def _management_base_status(demand_id: str, item: dict) -> dict:
    safe_id = "".join(char if char.isalnum() or char in "._-" else "-" for char in demand_id)
    return {
        "version": "N3.0-management",
        "mode": "management_reconciliation",
        "caseId": f"case-management-{safe_id}",
        "demandId": demand_id,
        "eventRevision": 0,
        "lifecycleStatus": "not_run",
        "phaseCursor": None,
        "completedPhases": [],
        "invalidatedPhases": [],
        "gates": {},
        "blockers": [],
        "nextAction": NEXT_ACTIONS["not_run"],
        "visualQa": {"reviewed": 0, "total": 0, "status": "not_applicable"},
        "artifacts": [],
        "package": None,
        "draft": None,
        "deliveryEvidence": None,
        "lastEventAt": ((item.get("manual") or {}).get("updatedAt") or item.get("recebidoEm")),
        "stale": False,
        "integrity": {"status": "current", "source": "management_record", "checkedAt": None},
    }


def reconcile_management_evidence(status: dict, demand_id: str, item: dict) -> dict:
    """Make management evidence authoritative without pretending that FORJA ran."""
    result = dict(status)
    evidence = str(item.get("evidenciaResposta") or "").strip()
    fulfilled = item.get("status") == "cumprida" and bool(evidence)
    if fulfilled:
        if status.get("lifecycleStatus") != "fulfilled_by_reconciliation":
            result["legacySnapshot"] = {
                "version": status.get("version"),
                "caseId": status.get("caseId"),
                "lifecycleStatus": status.get("lifecycleStatus"),
                "deliveryEvidence": status.get("deliveryEvidence"),
            }
        result.update({
            "version": "N3.0-management",
            "mode": "management_reconciliation",
            "demandId": demand_id,
            "lifecycleStatus": "fulfilled_by_reconciliation",
            "phaseCursor": "F10_RECONCILIACAO_GESTAO",
            "completedPhases": ["F10_RECONCILIACAO_GESTAO"],
            "invalidatedPhases": [],
            "gates": {"EVIDENCIA_GESTAO": {"status": "pass"}},
            "blockers": [],
            "nextAction": "Entrega ou encerramento reconhecido pela evidência registrada na gestão.",
            "visualQa": {"reviewed": 0, "total": 0, "status": "not_applicable"},
            "deliveryEvidence": {
                "status": "management_verified",
                "type": item.get("evidenciaTipo") or "registro_gestao",
                "detail": evidence,
            },
            "lastEventAt": ((item.get("manual") or {}).get("updatedAt") or item.get("recebidoEm")),
            "stale": False,
            "integrity": {
                "status": "current",
                "source": "management_evidence",
                "checkedAt": ((item.get("manual") or {}).get("updatedAt") or item.get("recebidoEm")),
            },
        })
        return result

    terminal = {"fulfilled", "complete", "sent_confirmed", "fulfilled_by_forja_f10", "fulfilled_by_reconciliation"}
    if item.get("status") != "cumprida" and str(status.get("lifecycleStatus") or "") in terminal:
        result["legacySnapshot"] = {
            "version": status.get("version"),
            "caseId": status.get("caseId"),
            "lifecycleStatus": status.get("lifecycleStatus"),
            "deliveryEvidence": status.get("deliveryEvidence"),
        }
        result.update({
            "version": "N3.0-management",
            "mode": "management_reopened",
            "demandId": demand_id,
            "lifecycleStatus": "queued",
            "phaseCursor": "F0_REABERTURA_GESTAO",
            "completedPhases": [],
            "invalidatedPhases": [],
            "gates": {},
            "blockers": [],
            "nextAction": item.get("proximaAcao") or NEXT_ACTIONS["queued"],
            "deliveryEvidence": None,
            "lastEventAt": ((item.get("manual") or {}).get("updatedAt") or item.get("recebidoEm")),
            "stale": False,
            "integrity": {
                "status": "current",
                "source": "management_reopen",
                "checkedAt": ((item.get("manual") or {}).get("updatedAt") or item.get("recebidoEm")),
            },
        })
        return result

    if item.get("status") != "cumprida":
        result["managementStatus"] = "aberta"
        result["nextAction"] = item.get("proximaAcao") or result.get("nextAction") or NEXT_ACTIONS["queued"]
        integrity = dict(result.get("integrity") or {})
        integrity["managementSource"] = "open_demand_record"
        result["integrity"] = integrity

    delivery = result.get("deliveryEvidence")
    delivery_status = str((delivery or {}).get("status") or "") if isinstance(delivery, dict) else ""
    if not item.get("respondidoComConteudo") and not evidence and delivery_status in {"none", "manual_override"}:
        result["deliveryEvidence"] = None
        result.pop("legacyDeliveryEvidence", None)
    return result


def _linked_demand(case_id: str, state: dict, links_path: Path = LINKS) -> str:
    demand_id = str(state.get("demandId") or "").strip()
    if demand_id:
        return demand_id
    links = read_json(links_path, {"links": {}}) or {}
    demand_id = str((links.get("links") or {}).get(case_id) or "").strip()
    if not demand_id:
        raise ForjaN3Error(f"caso sem demandId ou vínculo explícito: {case_id}")
    return demand_id


def _visual_summary(state: dict) -> dict:
    artifacts = state.get("artifacts") or {}
    artifact = artifacts.get("f8_qa_ledger") or artifacts.get("visual_qa_ledger") or {}
    path = Path(str(artifact.get("path") or ""))
    ledger = read_json(path, {}) if path.is_file() else {}
    pages = ledger.get("pages") or [] if isinstance(ledger, dict) else []
    reviewed = sum((item.get("independentReview") or {}).get("status") == "pass" for item in pages)
    return {
        "reviewed": reviewed,
        "total": int(ledger.get("pageCount") or len(pages)) if isinstance(ledger, dict) else 0,
        "status": "pass" if ledger.get("approved") is True else "blocked" if ledger else "not_run",
    }


def _legacy_gates(value: object) -> dict:
    if isinstance(value, dict):
        return value
    result = {}
    entries = value if isinstance(value, list) else []
    for index, entry in enumerate(entries, 1):
        if not isinstance(entry, dict):
            continue
        name = str(entry.get("code") or f"GATE_{index}")
        severity = str(entry.get("severity") or "unknown").lower()
        status = "pass" if severity in {"resolved", "info", "pass"} else severity
        result[name] = {"status": status, "detail": entry.get("detail"), "at": entry.get("at")}
    return result


def _load_replay_cases(path: Path = SHADOW_REPLAY) -> tuple[dict[str, dict], str | None]:
    report = read_json(path, {}) if path.is_file() else {}
    if not isinstance(report, dict):
        return {}, None
    cases = {
        str(item.get("caseId")): item
        for item in report.get("cases") or []
        if isinstance(item, dict) and item.get("caseId")
    }
    return cases, report.get("generatedAt")


def _manual_forja_entries(path: Path = MANUAL) -> dict[str, dict]:
    payload = read_json(path, {}) if path.is_file() else {}
    if not isinstance(payload, dict):
        return {}
    return {
        str(demand_id): entry
        for demand_id, entry in (payload.get("items") or {}).items()
        if isinstance(entry, dict) and isinstance(entry.get("forja"), dict)
    }


def _overlay_artifacts(entries: object) -> list[dict]:
    artifacts = []
    for index, raw in enumerate(entries if isinstance(entries, list) else [], 1):
        entry = raw if isinstance(raw, dict) else {"path": raw}
        path = Path(str(entry.get("path") or ""))
        if not path.is_absolute():
            path = WORKSPACE / path
        exists = path.is_file()
        artifacts.append({
            "artifactId": str(entry.get("artifactId") or f"manual-{index}"),
            "label": str(entry.get("label") or path.name or f"Artefato {index}"),
            "role": str(entry.get("role") or "final_audited"),
            "audience": str(entry.get("audience") or "internal_review"),
            "path": str(path),
            "sha256": sha256_file(path) if exists else entry.get("sha256"),
            "exists": exists,
        })
    return artifacts


def apply_manual_forja_overlay(status: dict, demand_id: str, entry: dict | None) -> dict:
    """Promote an audited legacy product without mutating its historical state."""
    overlay = (entry or {}).get("forja")
    if not isinstance(overlay, dict):
        return status
    result = dict(status)
    result["legacySnapshot"] = {
        "version": status.get("version"),
        "caseId": status.get("caseId"),
        "lifecycleStatus": status.get("lifecycleStatus"),
        "integrity": status.get("integrity"),
    }
    result.update({
        "version": str(overlay.get("version") or "N3.0-manual-audit"),
        "mode": "finalized_product_overlay",
        "demandId": demand_id,
        "lifecycleStatus": str(overlay.get("lifecycleStatus") or result.get("lifecycleStatus") or "queued"),
        "phaseCursor": overlay.get("phaseCursor"),
        "completedPhases": list(overlay.get("completedPhases") or []),
        "invalidatedPhases": list(overlay.get("invalidatedPhases") or []),
        "gates": dict(overlay.get("gates") or {}),
        "blockers": list(overlay.get("blockers") or []),
        "nextAction": str(overlay.get("nextAction") or result.get("nextAction") or "Conferir o fechamento auditado."),
        "visualQa": dict(overlay.get("visualQa") or {"reviewed": 0, "total": 0, "status": "not_applicable"}),
        "artifacts": _overlay_artifacts(overlay.get("artifacts")),
        "package": overlay.get("package"),
        "draft": overlay.get("draft"),
        "deliveryEvidence": overlay.get("deliveryEvidence"),
        "lastEventAt": (entry or {}).get("updatedAt") or result.get("lastEventAt"),
        "stale": False,
        "integrity": {
            "status": str((overlay.get("integrity") or {}).get("status") or "current"),
            "source": "manual_final_audit",
            "checkedAt": (entry or {}).get("updatedAt"),
        },
    })
    return result


def state_to_status(case_dir: Path, state: dict, *, event_revision: int | None = None, last_event_at: str | None = None) -> dict:
    lifecycle = state.get("lifecycleStatus") or "queued"
    artifacts = []
    for artifact_id, entry in sorted((state.get("artifacts") or {}).items()):
        path = Path(str(entry.get("path") or ""))
        artifacts.append({
            "artifactId": artifact_id,
            "label": path.name or artifact_id,
            "role": entry.get("role"),
            "audience": entry.get("audience"),
            "sha256": entry.get("sha256"),
            "exists": path.is_file(),
        })
    package = state.get("package") or {}
    status = {
        "version": "N3.0-r2",
        "caseId": case_dir.name,
        "demandId": state.get("demandId"),
        "eventRevision": event_revision if event_revision is not None else state.get("revision"),
        "lifecycleStatus": lifecycle,
        "phaseCursor": state.get("phaseCursor"),
        "completedPhases": state.get("completedPhases") or [],
        "invalidatedPhases": state.get("invalidatedPhases") or [],
        "gates": state.get("gateStatus") or {},
        "blockers": state.get("blockers") or [],
        "nextAction": NEXT_ACTIONS.get(lifecycle, "Conferir o estado atual da FORJA."),
        "visualQa": _visual_summary(state),
        "artifacts": artifacts,
        "package": {
            "packageId": package.get("packageId"),
            "packageHash": package.get("packageHash"),
            "path": package.get("path"),
        } if package else None,
        "draft": state.get("draft"),
        "deliveryEvidence": state.get("deliveryEvidence"),
        "postProtocol": _post_protocol_summary(state),
        "lastEventAt": last_event_at or state.get("updatedAt"),
        "stale": False,
        "integrity": {
            "status": "blocked" if state.get("blockers") or state.get("invalidatedPhases") else "current",
            "source": "n3_events",
            "checkedAt": last_event_at or state.get("updatedAt"),
        },
    }
    try:
        from forja_n4_validate import management_summary

        status["n4"] = management_summary(case_dir)
        if status["n4"].get("blocksCurrentFlow"):
            status["integrity"] = {
                "status": "blocked",
                "source": "n4_validation",
                "checkedAt": last_event_at or state.get("updatedAt"),
            }
    except Exception as exc:
        status["n4"] = {
            "enabled": True,
            "mode": "shadow",
            "status": "sync_error",
            "evaluationStatus": "sync_error",
            "approved": False,
            "promotionEligible": False,
            "legalReleaseStatus": "human_review_required",
            "materialBlocks": 0,
            "blocksCurrentFlow": False,
            "nextAction": f"Atualizar visão N4: {str(exc)[:240]}",
            "artifactIds": [],
        }
        status["integrity"] = {
            "status": "stale",
            "source": "n4_validation_error",
            "checkedAt": last_event_at or state.get("updatedAt"),
            "detail": str(exc)[:240],
        }
    return status


def legacy_state_to_status(
    case_dir: Path,
    legacy: dict,
    *,
    replay_case: dict | None = None,
    replay_at: str | None = None,
) -> dict:
    raw_status = str(legacy.get("status") or "pending")
    phase = legacy.get("currentPhase")
    if raw_status == "superseded":
        lifecycle = "superseded"
    elif raw_status in {"fulfilled", "cumprida"}:
        lifecycle = "fulfilled_by_reconciliation"
    elif raw_status == "draft_awaiting_review":
        lifecycle = "draft_awaiting_review"
    elif raw_status == "blocked":
        lifecycle = "blocked"
    elif phase and not str(phase).startswith("F0"):
        lifecycle = "running"
    else:
        lifecycle = "queued"
    artifacts = []
    for index, value in enumerate(legacy.get("artifacts") or [], 1):
        path = Path(str(value))
        if not path.is_absolute():
            path = WORKSPACE / path
        artifacts.append({
            "artifactId": f"legacy-{index}",
            "label": path.name or f"Artefato {index}",
            "role": "legacy",
            "audience": "legacy",
            "sha256": None,
            "exists": False,
        })
    demand_id = str(((legacy.get("inputs") or {}).get("demandId") or "")).strip()
    replay_blockers = list((replay_case or {}).get("blockers") or [])
    integrity_blockers = [REPLAY_BLOCKER_LABELS.get(code, str(code)) for code in replay_blockers]
    legacy_blockers = [str(value) for value in legacy.get("blockers") or []]
    all_blockers = list(dict.fromkeys(legacy_blockers + integrity_blockers))
    completed_phases = list(dict.fromkeys(
        item.get("phase") for item in legacy.get("phaseHistory") or []
        if isinstance(item, dict) and item.get("status") == "ok" and item.get("phase")
    ))
    integrity_status = "blocked" if replay_blockers else "compatible" if replay_case else "not_replayed"
    return {
        "version": "N2.0-compat",
        "mode": "legacy_readonly",
        "caseId": case_dir.name,
        "demandId": demand_id,
        "eventRevision": 0,
        "lifecycleStatus": lifecycle,
        "phaseCursor": phase,
        "completedPhases": completed_phases,
        "invalidatedPhases": [],
        "gates": _legacy_gates(legacy.get("gates")),
        "blockers": all_blockers,
        "nextAction": (
            "Resolver as pendências de integridade indicadas antes de promover a entrega."
            if integrity_status == "blocked"
            else NEXT_ACTIONS.get(lifecycle, "Conferir o estado legado da FORJA.")
        ),
        "visualQa": {"reviewed": 0, "total": 0, "status": "legacy_unverified"},
        "artifacts": artifacts,
        "package": None,
        "draft": legacy.get("deliveryEvidence") if lifecycle == "draft_awaiting_review" else None,
        "deliveryEvidence": legacy.get("deliveryEvidence"),
        "lastEventAt": legacy.get("updatedAt"),
        "stale": False,
        "integrity": {
            "status": integrity_status,
            "source": "n3_shadow_replay" if replay_case else "legacy_only",
            "checkedAt": replay_at,
            "visualFiles": len(((replay_case or {}).get("visual") or {}).get("files") or []),
            "visualFailed": int(((replay_case or {}).get("visual") or {}).get("failed") or 0),
            "codes": replay_blockers,
        },
    }


def sync_case(
    case_dir: Path,
    *,
    sidecar_path: Path = SIDECAR,
    demands_path: Path = DEMANDS,
    links_path: Path = LINKS,
    manual_path: Path = MANUAL,
    apply: bool = True,
    record_sync_event: bool = True,
) -> dict:
    state = derive_state(case_dir)
    business_events = [event for event in load_events(case_dir) if event.get("type") not in {"sync_succeeded", "sync_failed"}]
    business_revision = business_events[-1]["eventSeq"] if business_events else 0
    business_at = business_events[-1]["at"] if business_events else state.get("updatedAt")
    demand_id = _linked_demand(case_dir.name, state, links_path)
    if demand_id not in _demand_ids(demands_path):
        raise ForjaN3Error(f"demandId não existe na gestão: {demand_id}")
    status = state_to_status(case_dir, state, event_revision=business_revision, last_event_at=business_at)
    status["demandId"] = demand_id
    demand_record = _demand_records(demands_path).get(demand_id)
    if demand_record:
        # A FORJA descreve o ciclo produtivo, mas a gestão é a autoridade sobre
        # entrega. Evidência de envio ao escritório encerra a cobrança mesmo que
        # um estado técnico antigo ainda esteja bloqueado ou aguardando revisão.
        status = reconcile_management_evidence(status, demand_id, demand_record)
    # A specifically promoted audited product may become the presentation
    # layer over a canonical N3 stream. The explicit flag avoids changing old
    # manual audits from unrelated cases during a batch reconciliation.
    manual_entry = _manual_forja_entries(manual_path).get(demand_id)
    manual_overlay = (manual_entry or {}).get("forja")
    if isinstance(manual_overlay, dict) and manual_overlay.get("overrideCanonicalN3") is True:
        status = apply_manual_forja_overlay(status, demand_id, manual_entry)
    if not apply:
        return {"changed": True, "dryRun": True, "demandId": demand_id, "status": status}
    lock_path = sidecar_path.parent / f".{sidecar_path.name}.lock"
    with InterProcessLock(lock_path):
        sidecar = read_json(sidecar_path, None)
        if not isinstance(sidecar, dict):
            sidecar = {"schemaVersion": 1, "revision": 0, "updatedAt": None, "items": {}}
        sidecar.setdefault("items", {})
        current = sidecar["items"].get(demand_id)
        if current and current.get("caseId") != case_dir.name and current.get("version") == "N3.0-r2" and current.get("lifecycleStatus") != "superseded":
            raise ForjaN3Error(f"demanda já vinculada a outro caso: {demand_id} -> {current.get('caseId')}")
        current_revision = int((current or {}).get("eventRevision") or 0)
        incoming_revision = int(status.get("eventRevision") or 0)
        if incoming_revision < current_revision:
            raise ForjaN3Error(f"sidecar está à frente do caso: {current_revision} > {incoming_revision}")
        comparable_current = {key: value for key, value in (current or {}).items() if key != "syncedAt"}
        changed = comparable_current != status
        if changed:
            status["syncedAt"] = now_iso()
            sidecar["items"][demand_id] = status
            sidecar["revision"] = int(sidecar.get("revision") or 0) + 1
            sidecar["updatedAt"] = now_iso()
            atomic_write_json(sidecar_path, sidecar)
        elif current:
            status["syncedAt"] = current.get("syncedAt")
    if record_sync_event:
        try:
            record_event(
                case_dir,
                "sync_succeeded",
                expected_revision=state["revision"],
                idempotency_key=f"{case_dir.name}:sync:{business_revision}",
                payload={"syncedEventSeq": business_revision, "sidecarRevision": sidecar.get("revision")},
            )
        except Exception:
            # The sidecar is already correct; replay can reconstruct the acknowledgement.
            pass
    return {"changed": changed, "dryRun": False, "demandId": demand_id, "sidecarRevision": sidecar.get("revision"), "status": status}


def reconcile(*, apply: bool, sidecar_path: Path = SIDECAR) -> dict:
    results = []
    errors = []
    candidates: dict[str, tuple[Path, dict]] = {}
    skipped = []
    valid_demands = _demand_ids(DEMANDS)
    for state_path in sorted(STATE_ROOT.glob("case-*/FORJA_N3_STATE.json")):
        try:
            state = derive_state(state_path.parent)
            demand_id = _linked_demand(state_path.parent.name, state, LINKS)
            # O diretório global da FORJA também contém casos pessoais. A
            # reconciliação em lote da gestão só deve importar casos já
            # cadastrados no quadro do escritório; a sincronização direta
            # continua estrita e reprova qualquer demandId inexistente.
            if demand_id not in valid_demands:
                skipped.append({"caseId": state_path.parent.name, "reason": "fora do escopo da gestão do escritório"})
                continue
            current = candidates.get(demand_id)
            rank = (state.get("lifecycleStatus") != "superseded", str(state.get("updatedAt") or ""), state_path.parent.name)
            if current:
                previous_path, previous_state = current
                previous_rank = (previous_state.get("lifecycleStatus") != "superseded", str(previous_state.get("updatedAt") or ""), previous_path.parent.name)
                if rank <= previous_rank:
                    skipped.append({"caseId": state_path.parent.name, "reason": f"estado duplicado; canônico: {previous_path.parent.name}"})
                    continue
                skipped.append({"caseId": previous_path.parent.name, "reason": f"estado duplicado; canônico: {state_path.parent.name}"})
            candidates[demand_id] = (state_path, state)
        except Exception as exc:
            errors.append({"caseId": state_path.parent.name, "error": str(exc)[:500]})
    for state_path, _ in sorted(candidates.values(), key=lambda item: str(item[0])):
        try:
            results.append(sync_case(state_path.parent, sidecar_path=sidecar_path, apply=apply, record_sync_event=apply))
        except Exception as exc:
            errors.append({"caseId": state_path.parent.name, "error": str(exc)[:500]})
    return {"ok": not errors, "apply": apply, "synced": len(results), "skipped": skipped, "errors": errors, "results": results}


def reconcile_legacy(
    *,
    apply: bool,
    sidecar_path: Path = SIDECAR,
    demands_path: Path = DEMANDS,
    state_root: Path = STATE_ROOT,
    manual_path: Path = MANUAL,
) -> dict:
    demand_records = _demand_records(demands_path)
    valid_demands = set(demand_records)
    replay_cases, replay_at = _load_replay_cases()
    manual_entries = _manual_forja_entries(manual_path)
    candidates: dict[str, tuple[Path, dict, dict]] = {}
    skipped = []
    for path in sorted(state_root.glob("case-*/FORJA_STATE.json")):
        legacy = read_json(path, None)
        if not isinstance(legacy, dict):
            skipped.append({"caseId": path.parent.name, "reason": "estado inválido"})
            continue
        status = legacy_state_to_status(
            path.parent,
            legacy,
            replay_case=replay_cases.get(path.parent.name),
            replay_at=replay_at,
        )
        demand_id = status["demandId"]
        if not demand_id or demand_id not in valid_demands:
            skipped.append({"caseId": path.parent.name, "reason": "demanda ausente na gestão"})
            continue
        if status["lifecycleStatus"] == "superseded":
            skipped.append({"caseId": path.parent.name, "reason": "estado substituído"})
            continue
        status = reconcile_management_evidence(status, demand_id, demand_records[demand_id])
        status = apply_manual_forja_overlay(status, demand_id, manual_entries.get(demand_id))
        existing = candidates.get(demand_id)
        if existing is None or str(status.get("lastEventAt") or "") > str(existing[2].get("lastEventAt") or ""):
            candidates[demand_id] = (path.parent, legacy, status)

    # A management-only demand can still have verified delivery evidence or an
    # explicit audited overlay even when no FORJA state directory was created.
    for demand_id, item in demand_records.items():
        if demand_id in candidates:
            continue
        manual_entry = manual_entries.get(demand_id)
        evidence = str(item.get("evidenciaResposta") or "").strip()
        if not manual_entry and not (item.get("status") == "cumprida" and evidence):
            continue
        status = _management_base_status(demand_id, item)
        status = reconcile_management_evidence(status, demand_id, item)
        status = apply_manual_forja_overlay(status, demand_id, manual_entry)
        candidates[demand_id] = (state_root / status["caseId"], {}, status)
    if not apply:
        return {"ok": True, "apply": False, "candidates": len(candidates), "skipped": skipped, "items": {key: value[2] for key, value in candidates.items()}}
    with InterProcessLock(sidecar_path.parent / f".{sidecar_path.name}.lock"):
        sidecar = read_json(sidecar_path, None)
        if not isinstance(sidecar, dict):
            sidecar = {"schemaVersion": 1, "revision": 0, "updatedAt": None, "items": {}}
        sidecar.setdefault("items", {})
        changed = 0
        for demand_id, (_, _, status) in candidates.items():
            current = sidecar["items"].get(demand_id)
            current_case = str((current or {}).get("caseId") or "")
            canonical_n3 = bool(
                current_case
                and (state_root / current_case / "FORJA_N3_STATE.json").is_file()
            )
            # N3 only wins when backed by a canonical state, never by a replay copy.
            if current and current.get("version") in {"N3.0-r2", "N3.0-management"} and canonical_n3:
                continue
            comparable = {key: value for key, value in (current or {}).items() if key != "syncedAt"}
            if comparable != status:
                status["syncedAt"] = now_iso()
                sidecar["items"][demand_id] = status
                changed += 1
        if changed:
            sidecar["revision"] = int(sidecar.get("revision") or 0) + 1
            sidecar["updatedAt"] = now_iso()
            atomic_write_json(sidecar_path, sidecar)
    return {"ok": True, "apply": True, "candidates": len(candidates), "changed": changed, "skipped": skipped}


def main() -> None:
    parser = argparse.ArgumentParser(description="Sincroniza FORJA N3 com sidecar da gestão")
    parser.add_argument("--case")
    parser.add_argument("--reconcile", action="store_true")
    parser.add_argument("--legacy", action="store_true")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--sidecar", type=Path, default=SIDECAR)
    args = parser.parse_args()
    if args.apply and not feature_enabled("managementSidecarV1"):
        raise SystemExit("managementSidecarV1 está desligado; use sem --apply para shadow mode")
    if args.legacy:
        result = reconcile_legacy(apply=args.apply, sidecar_path=args.sidecar)
    elif args.reconcile:
        result = reconcile(apply=args.apply, sidecar_path=args.sidecar)
    elif args.case:
        matches = list(STATE_ROOT.glob(f"case-*{args.case}*"))
        if len(matches) != 1:
            raise SystemExit(f"caso ambíguo/ausente: {args.case}")
        result = sync_case(matches[0], sidecar_path=args.sidecar, apply=args.apply, record_sync_event=args.apply)
    else:
        parser.error("use --case ou --reconcile")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result.get("ok", True) else 1)


if __name__ == "__main__":
    main()
