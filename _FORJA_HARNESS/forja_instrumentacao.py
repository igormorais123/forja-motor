"""Instrumentação prospectiva da FORJA (PRD 45, R0).

O ledger é deliberadamente separado do estado N3/N4: registra oportunidades,
não promove fases nem libera conteúdo jurídico. A escrita é append-only e o
mesmo ``opportunityId`` é idempotente quando o evento reaparece sem alteração.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any

from forja_n3_common import InterProcessLock, atomic_write_json, now_iso, sha256_file
from forja_severidade import blocking_findings


LEDGER_FILENAME = "OBSERVATION_LEDGER.jsonl"
SCHEMA_VERSION = 1
INSTRUMENTATION_VERSION = "FORJA-INSTRUMENTACAO-v2"
VALID_MODES = {"off", "observe", "candidate_shadow"}
REQUIRED_FIELDS = (
    "schemaVersion", "opportunityId", "caseId", "disciplineId",
    "triggerEventId", "triggerSequence", "registeredAt", "eligible",
    "eligibilityReason", "dispatchEventId", "nonDispatchReason",
    "artifactPath", "artifactSha256", "consumerEventId", "consumedSha256",
    "humanReviewer", "humanAudit", "materialOutcome", "costMinutes",
    "arExperimentId",
)


class InstrumentationError(ValueError):
    pass


def effective_mode(config: Mapping | None = None, *, override: str | None = None) -> str:
    """Resolve o namespace de rollout sem ativação por omissão ambígua."""
    declared = override if override is not None else ((config or {}).get("instrumentation") or {}).get("mode", "off")
    mode = str(declared or "off").strip().casefold()
    if mode not in VALID_MODES:
        raise InstrumentationError(f"modo de instrumentação inválido: {mode!r}")
    return mode


def observation_path(case_dir: Path) -> Path:
    return Path(case_dir) / "instrumentation" / LEDGER_FILENAME


def _digest(value: Any) -> str:
    data = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def _text(value: Any) -> str:
    return str(value or "").strip()


def _record_without_hash(record: Mapping) -> dict:
    return {key: value for key, value in record.items() if key != "recordSha256"}


def record_sha256(record: Mapping) -> str:
    return _digest(_record_without_hash(record))


def _replay_fingerprint(record: Mapping) -> str:
    """Identidade do evento, sem o carimbo local criado pelo registrador."""
    return _digest({key: value for key, value in _record_without_hash(record).items() if key != "registeredAt"})


def _record_issue(code: str, detail: str, *, severity: str = "p0") -> dict:
    return {"code": code, "severity": severity, "detail": detail}


def validate_observation(record: Mapping | None, *, trigger_sequence: int | None = None) -> list[dict]:
    """Valida uma oportunidade sem depender do caso no disco."""
    if not isinstance(record, Mapping):
        return [_record_issue("OBS-01", "registro não é objeto JSON")]
    findings: list[dict] = []
    for field in REQUIRED_FIELDS:
        if field not in record:
            findings.append(_record_issue("OBS-02", f"campo obrigatório ausente: {field}"))
    if record.get("schemaVersion") != SCHEMA_VERSION:
        findings.append(_record_issue("OBS-03", "schemaVersion divergente"))
    for field in ("opportunityId", "caseId", "disciplineId", "triggerEventId", "registeredAt"):
        if not _text(record.get(field)):
            findings.append(_record_issue("OBS-04", f"identificador/data ausente: {field}"))
    sequence = record.get("triggerSequence")
    if not isinstance(sequence, int) or isinstance(sequence, bool) or sequence < 0:
        findings.append(_record_issue("OBS-05", "triggerSequence deve ser inteiro não negativo"))
    elif trigger_sequence is not None and sequence != trigger_sequence:
        findings.append(_record_issue("OBS-06", "triggerSequence não corresponde ao evento registrado"))
    eligible = record.get("eligible")
    if not isinstance(eligible, bool):
        findings.append(_record_issue("OBS-07", "eligible deve ser booleano"))
    if eligible is False and not _text(record.get("eligibilityReason")):
        findings.append(_record_issue("OBS-08", "oportunidade inelegível sem motivo"))
    dispatched = bool(_text(record.get("dispatchEventId")))
    if eligible is True and not dispatched and not _text(record.get("nonDispatchReason")):
        findings.append(_record_issue("OBS-09", "elegível sem despacho exige nonDispatchReason"))
    if dispatched and not _text(record.get("dispatchEventId")):
        findings.append(_record_issue("OBS-10", "dispatchEventId inválido"))
    consumed = bool(_text(record.get("consumerEventId")) or _text(record.get("consumedSha256")))
    if consumed and not (_text(record.get("consumerEventId")) and _text(record.get("consumedSha256"))):
        findings.append(_record_issue("OBS-11", "consumo exige evento e hash consumido"))
    consumer_sequence = record.get("consumerSequence")
    if consumed and consumer_sequence is not None:
        if not isinstance(consumer_sequence, int) or isinstance(consumer_sequence, bool):
            findings.append(_record_issue("OBS-20", "consumerSequence deve ser inteiro"))
        elif isinstance(sequence, int) and consumer_sequence <= sequence:
            findings.append(_record_issue("OBS-20", "consumo deve ocorrer em sequência posterior ao gatilho"))
    produced = _text(record.get("artifactSha256"))
    consumed_hash = _text(record.get("consumedSha256"))
    if consumed_hash and produced and consumed_hash != produced:
        findings.append(_record_issue("OBS-12", "hash consumido diverge do artefato produzido"))
    cost = record.get("costMinutes")
    if cost is not None and (not isinstance(cost, (int, float)) or isinstance(cost, bool) or cost < 0):
        findings.append(_record_issue("OBS-13", "costMinutes deve ser número não negativo"))
    reviewer = record.get("humanReviewer")
    audit = record.get("humanAudit")
    if audit not in (None, "", True, False) and not isinstance(audit, Mapping):
        findings.append(_record_issue("OBS-14", "humanAudit deve ser objeto ou booleano"))
    if reviewer and not _text(reviewer):
        findings.append(_record_issue("OBS-15", "humanReviewer inválido"))
    return findings


def load_observations(case_dir: Path) -> list[dict]:
    path = observation_path(case_dir)
    if not path.exists():
        return []
    records: list[dict] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise InstrumentationError(f"linha {number} inválida no ledger de observação: {exc}") from exc
        if not isinstance(value, dict):
            raise InstrumentationError(f"linha {number} do ledger não é objeto")
        records.append(value)
    return records


def append_observation(case_dir: Path, record: Mapping, *, artifact_path: Path | None = None) -> dict:
    """Registra uma oportunidade ou retorna o replay idempotente já existente."""
    payload = dict(record)
    payload.setdefault("schemaVersion", SCHEMA_VERSION)
    payload.setdefault("registeredAt", now_iso())
    if artifact_path is not None:
        payload["artifactPath"] = str(artifact_path)
        if artifact_path.is_file():
            payload["artifactSha256"] = sha256_file(artifact_path)
    findings = validate_observation(payload)
    if blocking_findings(findings):
        raise InstrumentationError("; ".join(item["detail"] for item in findings))
    payload["recordSha256"] = record_sha256(payload)
    path = observation_path(case_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    lock_path = path.with_suffix(path.suffix + ".lock")
    with InterProcessLock(lock_path, timeout=10, stale_after=300):
        records = load_observations(case_dir)
        for prior in records:
            if str(prior.get("opportunityId")) != str(payload.get("opportunityId")):
                continue
            if record_sha256(prior) == record_sha256(payload) or _replay_fingerprint(prior) == _replay_fingerprint(payload):
                return prior
            raise InstrumentationError(
                f"opportunityId já registrado com conteúdo diferente: {payload.get('opportunityId')}"
            )
        with path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")
            handle.flush()
    return payload


def validate_ledger(case_dir: Path) -> dict:
    records = load_observations(case_dir)
    findings: list[dict] = []
    seen: dict[str, dict] = {}
    previous_sequence = -1
    for index, record in enumerate(records, start=1):
        findings.extend({**finding, "line": index} for finding in validate_observation(record))
        opportunity = str(record.get("opportunityId") or "")
        if opportunity in seen:
            if record_sha256(seen[opportunity]) != record_sha256(record):
                findings.append(_record_issue("OBS-16", f"replay divergente para {opportunity}"))
        else:
            seen[opportunity] = record
        sequence = record.get("triggerSequence")
        if isinstance(sequence, int) and sequence < previous_sequence:
            findings.append(_record_issue("OBS-17", "sequência de gatilho regressiva", severity="p1"))
        if isinstance(sequence, int):
            previous_sequence = max(previous_sequence, sequence)
        if record.get("consumerEventId") and record.get("dispatchEventId") and record.get("consumerEventId") == record.get("dispatchEventId"):
            findings.append(_record_issue("OBS-18", "consumidor não pode ser o mesmo evento de despacho"))
        if record.get("recordSha256") and record.get("recordSha256") != record_sha256(record):
            findings.append(_record_issue("OBS-19", "hash do registro diverge do conteúdo"))
    return {
        "schemaVersion": SCHEMA_VERSION,
        "caseId": Path(case_dir).name,
        "records": len(records),
        "uniqueOpportunities": len(seen),
        "findings": findings,
        "approved": not blocking_findings(findings),
    }


def observation_metrics(records: Iterable[Mapping]) -> dict:
    rows = [dict(record) for record in records]
    eligible = [row for row in rows if row.get("eligible") is True]
    consumed = [
        row for row in eligible
        if _text(row.get("consumerEventId"))
        and _text(row.get("consumedSha256"))
        and _text(row.get("artifactSha256")) == _text(row.get("consumedSha256"))
        and isinstance(row.get("consumerSequence"), int)
        and isinstance(row.get("triggerSequence"), int)
        and row.get("consumerSequence") > row.get("triggerSequence")
    ]
    non_dispatch = [row for row in eligible if not _text(row.get("dispatchEventId"))]
    audited = [row for row in eligible if row.get("humanAudit") not in (None, "", False)]
    costs = [float(row["costMinutes"]) for row in eligible if isinstance(row.get("costMinutes"), (int, float)) and not isinstance(row.get("costMinutes"), bool)]
    denominator = len(eligible)
    def ratio(value: int) -> float | None:
        return round(value / denominator, 6) if denominator else None
    return {
        "eligible": denominator,
        "consumed": len(consumed),
        "nonDispatch": len(non_dispatch),
        "humanAudited": len(audited),
        "adoption": ratio(len(consumed)),
        "nonDispatchRate": ratio(len(non_dispatch)),
        "humanAuditRate": ratio(len(audited)),
        "costMedianMinutes": _median(costs),
        "costMaxMinutes": max(costs) if costs else None,
        "status": "not_applicable" if denominator == 0 else "observed",
    }


def _median(values: list[float]) -> float | None:
    if not values:
        return None
    values = sorted(values)
    middle = len(values) // 2
    if len(values) % 2:
        return values[middle]
    return round((values[middle - 1] + values[middle]) / 2, 6)


def metrics_for_case(case_dir: Path) -> dict:
    records = load_observations(case_dir)
    return {"caseId": Path(case_dir).name, **observation_metrics(records)}


def _main() -> int:
    parser = argparse.ArgumentParser(description="Ledger prospectivo de instrumentação da FORJA")
    sub = parser.add_subparsers(dest="command", required=True)
    validate = sub.add_parser("validate")
    validate.add_argument("case", type=Path)
    metrics = sub.add_parser("metrics")
    metrics.add_argument("case", type=Path)
    register = sub.add_parser("register")
    register.add_argument("case", type=Path)
    register.add_argument("record", type=Path)
    args = parser.parse_args()
    if args.command == "validate":
        result = validate_ledger(args.case)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["approved"] else 1
    if args.command == "metrics":
        print(json.dumps(metrics_for_case(args.case), ensure_ascii=False, indent=2))
        return 0
    record = json.loads(args.record.read_text(encoding="utf-8-sig"))
    result = append_observation(args.case, record)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
