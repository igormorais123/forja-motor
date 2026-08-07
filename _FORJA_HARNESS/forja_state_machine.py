"""FORJA N3 event store and derived state machine.

The N3 state is additive and writes FORJA_N3_STATE.json. Legacy FORJA_STATE.json
is read for import metadata but is never mutated by this module.
"""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path

from forja_n3_common import (
    PHASES,
    InterProcessLock,
    RevisionConflict,
    TransitionError,
    atomic_write_json,
    atomic_write_text,
    canonical_hash,
    load_config,
    new_id,
    now_iso,
    read_json,
    resolve_case_dir,
)


EVENT_TYPES = {
    "case_initialized",
    "phase_started",
    "phase_completed",
    "phase_blocked",
    "gate_recorded",
    "gate_reopened",
    "artifact_promoted",
    "package_created",
    "draft_created",
    "delivery_confirmed",
    "case_fulfilled",
    "case_superseded",
    "sync_succeeded",
    "sync_failed",
    "n4_module_classified",
    "question_added",
    "question_answered",
    "question_blocked",
    "coverage_item_resolved",
    "event_identity_confirmed",
    "document_comparison_completed",
    "thesis_maturity_decided",
    "case_test_frozen",
    "case_test_executed",
    "science_protocol_approved",
    "science_source_verified",
    "science_synthesis_completed",
    "global_consistency_failed",
    "metacognitive_issue_found",
    "human_diff_classified",
    "delivery_selection_verified",
    "delivery_integrity_recorded",
    "regression_test_proposed",
    "n4_gate_promoted",
    "n4_gate_reopened",
    "post_protocol_candidate_detected",
    "post_protocol_identity_ambiguous",
    "post_protocol_blocked",
    "post_protocol_captured",
    "post_protocol_claimed",
    "post_protocol_verified",
    "post_protocol_ai_baseline_unresolved",
    "post_protocol_baseline_backfilled",
    "post_protocol_diff_ready",
    "post_protocol_review_pending",
    "post_protocol_learning_proposed",
    "post_protocol_learning_promoted",
    "post_protocol_complete",
}
EVENT_RE = re.compile(r"^(\d{8})-(evt-[0-9a-f]+)\.json$")


def _phase_index(phase: str) -> int:
    try:
        return PHASES.index(phase)
    except ValueError as exc:
        raise TransitionError(f"fase desconhecida: {phase}") from exc


def _highest_completed_index(state: dict) -> int:
    indexes = [_phase_index(item) for item in state.get("completedPhases") or []]
    legacy_phase = ((state.get("legacy") or {}).get("highestCompletedPhase"))
    if legacy_phase in PHASES:
        indexes.append(_phase_index(legacy_phase))
    return max(indexes, default=-1)


def event_paths(case_dir: Path) -> list[Path]:
    directory = case_dir / "events"
    if not directory.exists():
        return []
    paths = [path for path in directory.iterdir() if path.is_file() and EVENT_RE.match(path.name)]
    return sorted(paths, key=lambda path: int(EVENT_RE.match(path.name).group(1)))


def load_events(case_dir: Path) -> list[dict]:
    events = []
    for expected, path in enumerate(event_paths(case_dir), 1):
        match = EVENT_RE.match(path.name)
        payload = read_json(path, None)
        if not isinstance(payload, dict):
            raise TransitionError(f"evento inválido: {path}")
        if int(match.group(1)) != expected or payload.get("eventSeq") != expected:
            raise TransitionError(f"sequência de eventos descontínua em {path.name}")
        if payload.get("eventId") != match.group(2):
            raise TransitionError(f"eventId divergente do nome em {path.name}")
        events.append(payload)
    return events


def _base_state(case_dir: Path) -> dict:
    return {
        "schemaVersion": 1,
        "specVersion": "N3.0-r2",
        "caseId": case_dir.name,
        "demandId": None,
        "inputs": {},
        "revision": 0,
        "updatedAt": None,
        "phaseCursor": None,
        "lifecycleStatus": "queued",
        "completedPhases": [],
        "invalidatedPhases": [],
        "gateStatus": {},
        "blockers": [],
        "artifacts": {},
        "package": None,
        "draft": None,
        "deliveryEvidence": None,
        "sync": {"status": "never", "lastSyncedEventSeq": 0},
        "n4": {"lastEvent": None, "events": 0, "staleArtifacts": []},
        "postProtocol": {
            "status": "not_detected",
            "protocolStatus": None,
            "contentKey": None,
            "humanArtifactId": None,
            "aiBaselineArtifactId": None,
            "protocolEvidenceId": None,
            "diffArtifactId": None,
            "learningCandidateIds": [],
            "promotedLearningIds": [],
            "openReasonCodes": [],
            "reasonCodeSources": {},
            "lastEventSeq": None,
        },
        "legacy": None,
    }


def derive_state(case_dir: Path, events: list[dict] | None = None) -> dict:
    state = _base_state(case_dir)
    for event in events if events is not None else load_events(case_dir):
        state["revision"] = event["eventSeq"]
        state["updatedAt"] = event["at"]
        event_type = event["type"]
        phase = event.get("phase")
        payload = event.get("payload") or {}

        if event_type == "case_initialized":
            state["demandId"] = event.get("demandId") or payload.get("demandId")
            state["inputs"] = payload.get("inputs") or {}
            state["legacy"] = payload.get("legacy")
            if payload.get("legacyPhase"):
                state["phaseCursor"] = payload["legacyPhase"]
            if payload.get("legacyStatus"):
                state["lifecycleStatus"] = payload["legacyStatus"]
        elif event_type == "phase_started":
            state["phaseCursor"] = phase
            state["lifecycleStatus"] = "running"
            state["blockers"] = []
        elif event_type == "phase_completed":
            state["phaseCursor"] = phase
            if phase not in state["completedPhases"]:
                state["completedPhases"].append(phase)
            state["invalidatedPhases"] = [item for item in state["invalidatedPhases"] if item != phase]
            state["gateStatus"][phase] = {"status": "pass", "eventSeq": event["eventSeq"]}
            state["lifecycleStatus"] = payload.get("lifecycleStatus") or "running"
        elif event_type == "phase_blocked":
            state["phaseCursor"] = phase
            state["lifecycleStatus"] = "blocked"
            state["gateStatus"][phase] = {"status": "blocked", "eventSeq": event["eventSeq"]}
            state["blockers"] = payload.get("blockers") or [payload.get("reason") or "bloqueio não detalhado"]
        elif event_type == "gate_recorded":
            name = str(payload.get("gate") or phase or "").strip()
            if name:
                state["gateStatus"][name] = {
                    "status": payload.get("status") or "unknown",
                    "artifactHash": payload.get("artifactHash"),
                    "eventSeq": event["eventSeq"],
                }
        elif event_type == "gate_reopened":
            target = phase or payload.get("targetPhase")
            state["phaseCursor"] = target
            state["lifecycleStatus"] = "blocked"
            state["blockers"] = [payload.get("reason") or "gate reaberto"]
            start = _phase_index(target)
            affected = list(PHASES[start:])
            state["invalidatedPhases"] = sorted(set(state["invalidatedPhases"] + affected), key=_phase_index)
            for item in affected:
                if item in state["gateStatus"]:
                    state["gateStatus"][item]["status"] = "stale"
        elif event_type == "artifact_promoted":
            artifact_id = str(payload.get("artifactId") or "").strip()
            if artifact_id:
                state["artifacts"][artifact_id] = payload.get("artifact") or {}
        elif event_type == "package_created":
            state["package"] = payload
            state["lifecycleStatus"] = "ready_for_review"
        elif event_type == "draft_created":
            state["draft"] = payload
            state["lifecycleStatus"] = "draft_awaiting_review"
        elif event_type == "delivery_confirmed":
            state["deliveryEvidence"] = payload
            state["lifecycleStatus"] = "sent_confirmed"
        elif event_type == "case_fulfilled":
            state["lifecycleStatus"] = "fulfilled_by_forja_f10"
            gates = payload.get("gates")
            if isinstance(gates, dict):
                evidence = dict(state.get("deliveryEvidence") or {})
                evidence["gates"] = gates
                state["deliveryEvidence"] = evidence
        elif event_type == "case_superseded":
            state["lifecycleStatus"] = "superseded"
        elif event_type == "sync_succeeded":
            state["sync"] = {
                "status": "ok",
                "lastSyncedEventSeq": payload.get("syncedEventSeq") or event["eventSeq"],
                "syncedAt": event["at"],
            }
        elif event_type == "sync_failed":
            state["sync"] = {
                "status": "pending",
                "lastSyncedEventSeq": state["sync"].get("lastSyncedEventSeq", 0),
                "lastAttemptAt": event["at"],
                "error": payload.get("error") or "falha de sincronização",
            }
        elif event_type.startswith("post_protocol_"):
            post = state["postProtocol"]
            post["lastEventSeq"] = event["eventSeq"]
            post["status"] = event_type.removeprefix("post_protocol_")
            for key in (
                "contentKey",
                "humanArtifactId",
                "aiBaselineArtifactId",
                "protocolEvidenceId",
                "diffArtifactId",
            ):
                if payload.get(key) is not None:
                    post[key] = payload[key]
            if event_type == "post_protocol_identity_ambiguous":
                post["protocolStatus"] = "identity_ambiguous"
            elif event_type == "post_protocol_claimed":
                post["protocolStatus"] = "protocol_claimed"
            elif event_type == "post_protocol_verified":
                post["protocolStatus"] = "protocol_verified"
            elif payload.get("protocolStatus"):
                post["protocolStatus"] = payload["protocolStatus"]
            source = str(payload.get("reasonSource") or event_type)
            reason_sources = post.setdefault("reasonCodeSources", {})
            for code in payload.get("resolvedReasonCodes") or []:
                owners = set(reason_sources.get(code) or [])
                owners.discard(source)
                if owners:
                    reason_sources[code] = sorted(owners)
                else:
                    reason_sources.pop(code, None)
            for code in payload.get("openReasonCodes") or []:
                reason_sources[code] = sorted(set((reason_sources.get(code) or []) + [source]))
            post["openReasonCodes"] = sorted(reason_sources)
            if payload.get("learningCandidateIds"):
                post["learningCandidateIds"] = sorted(
                    set(post["learningCandidateIds"] + list(payload["learningCandidateIds"]))
                )
            if payload.get("promotedLearningIds"):
                post["promotedLearningIds"] = sorted(
                    set(post["promotedLearningIds"] + list(payload["promotedLearningIds"]))
                )
        elif event_type in EVENT_TYPES and event_type not in {
            "case_initialized", "phase_started", "phase_completed", "phase_blocked", "gate_recorded",
            "gate_reopened", "artifact_promoted", "package_created", "draft_created", "delivery_confirmed",
            "case_fulfilled", "case_superseded", "sync_succeeded", "sync_failed",
        }:
            state["n4"]["lastEvent"] = {"type": event_type, "eventSeq": event["eventSeq"], "at": event["at"]}
            state["n4"]["events"] += 1
            stale = payload.get("staleArtifacts") or []
            state["n4"]["staleArtifacts"] = sorted(set(state["n4"]["staleArtifacts"] + stale))
    state["stateHash"] = canonical_hash({key: value for key, value in state.items() if key != "stateHash"})
    return state


def _validate_transition(events: list[dict], event_type: str, phase: str | None, payload: dict) -> None:
    if event_type not in EVENT_TYPES:
        raise TransitionError(f"tipo de evento desconhecido: {event_type}")
    state = derive_state(Path(payload.get("_caseDir") or "."), events)
    if phase is not None:
        _phase_index(phase)
    historical_import = event_type == "artifact_promoted" and payload.get("historicalImport") is True
    if state["lifecycleStatus"] in {"fulfilled", "fulfilled_by_reconciliation", "fulfilled_by_forja_f10", "superseded"} and event_type not in {
        "sync_succeeded", "sync_failed", "human_diff_classified", "regression_test_proposed", "n4_gate_reopened",
    } and not event_type.startswith("post_protocol_") and not historical_import:
        raise TransitionError(f"caso encerrado não aceita {event_type}")
    if event_type == "case_initialized" and events:
        raise TransitionError("caso já inicializado")
    if event_type != "case_initialized" and not events:
        raise TransitionError("primeiro evento deve ser case_initialized")
    if event_type == "phase_started":
        if phase is None:
            raise TransitionError("phase_started exige fase")
        highest = _highest_completed_index(state)
        target = _phase_index(phase)
        reopened = phase in state["invalidatedPhases"]
        same_retry = state["phaseCursor"] == phase and state["lifecycleStatus"] in {"blocked", "running"}
        if target > highest + 1 and not payload.get("allowSkip"):
            raise TransitionError(f"salto de fase não permitido: {phase}")
        if target <= highest and not (reopened or same_retry):
            raise TransitionError(f"regressão silenciosa não permitida: {phase}; use gate_reopened")
    if event_type in {"phase_completed", "phase_blocked"}:
        if phase is None or state["phaseCursor"] != phase:
            raise TransitionError(f"{event_type} exige fase em execução: {phase}")
    if event_type == "gate_reopened":
        if phase is None:
            raise TransitionError("gate_reopened exige fase alvo")
        highest = _highest_completed_index(state)
        if _phase_index(phase) > highest:
            raise TransitionError("não é possível reabrir fase ainda não concluída")
    if event_type == "post_protocol_diff_ready":
        post = state.get("postProtocol") or {}
        if not post.get("humanArtifactId") or not payload.get("aiBaselineArtifactId"):
            raise TransitionError("post_protocol_diff_ready exige captura humana e base IA exata")
    if event_type == "post_protocol_verified" and not payload.get("protocolEvidenceId"):
        raise TransitionError("post_protocol_verified exige protocolEvidenceId")
    if event_type == "post_protocol_learning_promoted":
        if not payload.get("promotedLearningIds"):
            raise TransitionError("post_protocol_learning_promoted exige promotedLearningIds")


def _materialize_locked(case_dir: Path, events: list[dict]) -> dict:
    state = derive_state(case_dir, events)
    atomic_write_json(case_dir / "FORJA_N3_STATE.json", state)
    lines = "".join(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n" for event in events)
    atomic_write_text(case_dir / "FORJA_EVENTS.jsonl", lines)
    return state


def record_event(
    case_dir: Path,
    event_type: str,
    *,
    expected_revision: int,
    idempotency_key: str,
    phase: str | None = None,
    actor: str = "forja-n3",
    run_id: str | None = None,
    attempt_id: str | None = None,
    demand_id: str | None = None,
    artifact_hashes: dict | None = None,
    payload: dict | None = None,
) -> tuple[dict, dict, bool]:
    case_dir = case_dir.resolve()
    config = load_config()
    lock_cfg = config.get("locks") or {}
    lock = InterProcessLock(
        case_dir / ".forja-n3.lock",
        timeout=float(lock_cfg.get("timeoutSeconds") or 15),
        stale_after=float(lock_cfg.get("staleAfterSeconds") or 900),
    )
    with lock:
        events = load_events(case_dir)
        for existing in events:
            if existing.get("idempotencyKey") == idempotency_key:
                return existing, derive_state(case_dir, events), False
        current = len(events)
        if expected_revision != current:
            raise RevisionConflict(f"revisão esperada {expected_revision}; revisão atual {current}")
        clean_payload = dict(payload or {})
        _validate_transition(events, event_type, phase, {**clean_payload, "_caseDir": str(case_dir)})
        event_id = new_id("evt")
        seq = current + 1
        event = {
            "schemaVersion": 1,
            "eventId": event_id,
            "eventSeq": seq,
            "idempotencyKey": idempotency_key,
            "caseId": case_dir.name,
            "demandId": demand_id,
            "runId": run_id,
            "attemptId": attempt_id,
            "expectedRevision": expected_revision,
            "type": event_type,
            "phase": phase,
            "result": clean_payload.pop("result", None),
            "artifactHashes": artifact_hashes or {},
            "payload": clean_payload,
            "at": now_iso(),
            "actor": actor,
        }
        directory = case_dir / "events"
        directory.mkdir(parents=True, exist_ok=True)
        final = directory / f"{seq:08d}-{event_id}.json"
        fd, temp_name = tempfile_event(directory, event_id)
        try:
            with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
                json.dump(event, handle, ensure_ascii=False, indent=2)
                handle.write("\n")
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temp_name, final)
        finally:
            Path(temp_name).unlink(missing_ok=True)
        events.append(event)
        state = _materialize_locked(case_dir, events)
    if event_type not in {"sync_succeeded", "sync_failed"}:
        try:
            from forja_management_bridge import sync_after_event

            sync_after_event(case_dir, event)
            state = derive_state(case_dir)
        except Exception:
            # Event durability does not depend on the management surface.
            pass
    return event, state, True


def tempfile_event(directory: Path, event_id: str) -> tuple[int, str]:
    import tempfile

    return tempfile.mkstemp(prefix=f".{event_id}.", suffix=".tmp", dir=directory)


def initialize_case(case_dir: Path, *, demand_id: str | None = None, from_legacy: bool = False) -> dict:
    legacy = read_json(case_dir / "FORJA_STATE.json", {}) if from_legacy else {}
    legacy_inputs = legacy.get("inputs") or {}
    demand_id = demand_id or legacy_inputs.get("demandId")
    legacy_completed = [
        str(item.get("phase")) for item in legacy.get("phaseHistory") or []
        if isinstance(item, dict) and item.get("status") == "ok" and str(item.get("phase")) in PHASES
    ]
    legacy_highest = max(legacy_completed, key=_phase_index) if legacy_completed else None
    payload = {
        "demandId": demand_id,
        "inputs": legacy_inputs,
        "legacy": {
            "specVersion": legacy.get("specVersion"),
            "currentPhase": legacy.get("currentPhase"),
            "status": legacy.get("status"),
            "highestCompletedPhase": legacy_highest,
            "sourceHash": canonical_hash(legacy) if legacy else None,
        } if legacy else None,
        "legacyPhase": legacy.get("currentPhase") if legacy else None,
        "legacyStatus": legacy.get("status") if legacy else None,
    }
    _, state, _ = record_event(
        case_dir,
        "case_initialized",
        expected_revision=0,
        idempotency_key=f"{case_dir.name}:initialize:v1",
        actor="forja-n3-import" if legacy else "forja-n3",
        demand_id=demand_id,
        payload=payload,
    )
    manifest_path = case_dir / "FORJA_CASE_MANIFEST.json"
    if not manifest_path.exists():
        atomic_write_json(
            manifest_path,
            {
                "schemaVersion": 1,
                "specVersion": "N3.0-r2",
                "caseId": case_dir.name,
                "demandId": demand_id,
                "inputs": legacy_inputs,
                "createdAt": state["updatedAt"],
                "eventRevision": state["revision"],
                "mode": "shadow",
            },
        )
    return state


def main() -> None:
    parser = argparse.ArgumentParser(description="Máquina de estados aditiva da FORJA N3")
    parser.add_argument("case")
    parser.add_argument("--state-root", type=Path)
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init")
    init.add_argument("--demand-id")
    init.add_argument("--from-legacy", action="store_true")
    status = sub.add_parser("status")
    event = sub.add_parser("event")
    event.add_argument("type", choices=sorted(EVENT_TYPES))
    event.add_argument("--phase", choices=PHASES)
    event.add_argument("--expected-revision", type=int, required=True)
    event.add_argument("--idempotency-key", required=True)
    event.add_argument("--actor", default="forja-n3-cli")
    event.add_argument("--payload", default="{}")
    args = parser.parse_args()
    case_dir = resolve_case_dir(args.case, state_root=args.state_root)
    if args.command == "init":
        result = initialize_case(case_dir, demand_id=args.demand_id, from_legacy=args.from_legacy)
    elif args.command == "status":
        result = derive_state(case_dir)
    else:
        _, result, _ = record_event(
            case_dir,
            args.type,
            expected_revision=args.expected_revision,
            idempotency_key=args.idempotency_key,
            phase=args.phase,
            actor=args.actor,
            payload=json.loads(args.payload),
        )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
