"""Recibo de encerramento do envelope editorial (PRD 45, R6)."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Mapping

from forja_n3_common import atomic_write_json


def extract_stop_reason(envelope: Mapping | None) -> str | None:
    if not isinstance(envelope, Mapping):
        return None
    for key in ("stop_reason", "stopReason", "finish_reason", "finishReason"):
        value = envelope.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    result = envelope.get("result")
    if isinstance(result, Mapping):
        return extract_stop_reason(result)
    return None


def build_stop_receipt(
    envelope: Mapping | None,
    *,
    expected_model: str | None = None,
    actual_model: str | None = None,
    parse_error: str | None = None,
    attempt: int | None = None,
) -> dict:
    if parse_error:
        reason = "invalid_output"
    elif expected_model and actual_model and expected_model != actual_model:
        reason = "model_divergence"
    elif not isinstance(envelope, Mapping):
        reason = "invalid_envelope"
    else:
        reason = extract_stop_reason(envelope) or "missing_stop_reason"
    return {
        "schemaVersion": 1,
        "recordedAt": datetime.now(timezone.utc).isoformat(),
        "stopReason": reason,
        "modelStopReason": extract_stop_reason(envelope),
        "expectedModel": expected_model,
        "actualModel": actual_model,
        "attempt": attempt,
        "parseError": parse_error,
    }


def record_stop_reason(
    output_dir: Path,
    envelope: Mapping | None,
    *,
    expected_model: str | None = None,
    actual_model: str | None = None,
    parse_error: str | None = None,
    attempt: int | None = None,
) -> dict:
    receipt = build_stop_receipt(
        envelope,
        expected_model=expected_model,
        actual_model=actual_model,
        parse_error=parse_error,
        attempt=attempt,
    )
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    atomic_write_json(output_dir / "STOP_REASON.json", receipt)
    if attempt is not None:
        atomic_write_json(output_dir / f"STOP_REASON-{attempt}.json", receipt)
    return receipt
