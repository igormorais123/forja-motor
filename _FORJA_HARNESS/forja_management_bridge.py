"""Best-effort N3 event -> office sidecar bridge.

Case events remain authoritative when the office panel is unavailable. Failures
are materialized inside the case and reconciled by the next dashboard update.
"""

from __future__ import annotations

import sys
from pathlib import Path

from forja_n3_common import FORJA, WORKSPACE, atomic_write_json, feature_enabled, now_iso


MANAGEMENT_SCRIPTS = WORKSPACE / "gestao_escritorio" / "scripts"
CANONICAL_STATE_ROOT = (FORJA / "state").resolve()
sys.path.insert(0, str(MANAGEMENT_SCRIPTS))


def sync_after_event(case_dir: Path, event: dict) -> dict:
    status_path = case_dir / "FORJA_MANAGEMENT_SYNC.json"
    resolved_case = case_dir.resolve()
    if resolved_case.parent != CANONICAL_STATE_ROOT:
        result = {
            "status": "ignored_noncanonical",
            "eventSeq": event.get("eventSeq"),
            "at": now_iso(),
        }
        atomic_write_json(status_path, result)
        return result
    if not feature_enabled("forjaManagementBridge") or not feature_enabled("managementSidecarV1"):
        result = {"status": "disabled", "eventSeq": event.get("eventSeq"), "at": now_iso()}
        atomic_write_json(status_path, result)
        return result
    try:
        from sync_forja_gestao import sync_case

        synced = sync_case(case_dir, apply=True, record_sync_event=True)
        result = {
            "status": "ok",
            "eventSeq": event.get("eventSeq"),
            "sidecarRevision": synced.get("sidecarRevision"),
            "changed": synced.get("changed"),
            "at": now_iso(),
        }
    except Exception as exc:
        result = {
            "status": "pending",
            "eventSeq": event.get("eventSeq"),
            "error": str(exc)[:1000],
            "at": now_iso(),
        }
    atomic_write_json(status_path, result)
    return result
