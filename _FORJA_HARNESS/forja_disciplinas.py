"""Contratos pequenos das disciplinas D1–D6 do PRD 45.

As funções aqui produzem artefatos experimentais, validam hashes e ordenação e
não promovem fase. Cada disciplina tem produtor, consumidor e canário explícito
para permitir observação prospectiva sem segunda fonte normativa.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable, Mapping

from forja_n3_common import atomic_write_json, atomic_write_text, now_iso, sha256_file


DISCIPLINES = {
    "D1": {"trigger": "antes do despacho de conselho F4", "output": "F4_COUNSEL_BRIEFING.json", "consumer": "revisor do conselho", "canary": "remover uma fonte ou pergunta obrigatória"},
    "D2": {"trigger": "cada propositionId decisiva em F5", "output": "F5_PROPOSITION_EVIDENCE_MAP.json", "consumer": "F7", "canary": "trocar a fonte entre dois precedentes"},
    "D3": {"trigger": "depois de F1, com duas linhas materiais abertas", "output": "F2_INTAKE_HYPOTHESES.json", "consumer": "F2A/F4", "canary": "fonte posterior contradiz hipótese"},
    "D4": {"trigger": "antes do fechamento F7", "output": "F7_UNCERTAIN_DECISIONS.json", "consumer": "F9", "canary": "dúvida retrospectiva fabricada"},
    "D5": {"trigger": "antes do despacho de revisão cruzada", "output": "HANDOFF.md", "consumer": "revisor cruzado", "canary": "remover armadilha material do caso"},
    "D6": {"trigger": "quando decisão de arquitetura/processo é tomada", "output": "decisoes/", "consumer": "manutenção e novas propostas", "canary": "remover critério de reabertura"},
}
VALID_D3_STATUS = {"open", "confirmed", "rejected", "reopened", "superseded"}
VALID_D4_ACTIONS = {"decision", "diligence", "human_correction"}
VALID_D4_STATUS = {"open", "resolved", "reopened", "not_applicable"}
VALID_D6_STATUS = {"decided", "rejected", "active", "reopened", "superseded"}


def _digest(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def artifact_hash(payload: Mapping) -> str:
    return _digest({key: value for key, value in payload.items() if key not in {"contentHash", "briefingSha256", "handoffSha256"}})


def _finding(code: str, detail: str, *, severity: str = "p0") -> dict:
    return {"code": code, "severity": severity, "detail": detail}


def _ids(items: Iterable[Mapping], keys: tuple[str, ...]) -> list[str]:
    result = []
    for item in items:
        value = next((item.get(key) for key in keys if item.get(key)), None)
        result.append(str(value or ""))
    return result


def build_d1_briefing(*, case_id: str, trigger_event_id: str, trigger_sequence: int, questions: Iterable[Mapping], sources: Iterable[Mapping], rejected_decisions: Iterable[Mapping] = ()) -> dict:
    payload = {
        "schemaVersion": 1,
        "disciplineId": "D1",
        "caseId": case_id,
        "triggerEventId": trigger_event_id,
        "triggerSequence": trigger_sequence,
        "createdAt": now_iso(),
        "questions": sorted([dict(item) for item in questions], key=lambda item: (int(item.get("order", 0)), str(item.get("questionId") or ""))),
        "sources": sorted([dict(item) for item in sources], key=lambda item: str(item.get("sourceId") or item.get("id") or "")),
        "rejectedDecisions": [dict(item) for item in rejected_decisions],
        "status": "ready",
    }
    payload["briefingSha256"] = artifact_hash(payload)
    return payload


def validate_d1_briefing(payload: Mapping | None) -> list[dict]:
    if not isinstance(payload, Mapping):
        return [_finding("D1-00", "briefing ausente")]
    findings: list[dict] = []
    if payload.get("disciplineId") != "D1":
        findings.append(_finding("D1-01", "disciplineId divergente"))
    if not isinstance(payload.get("triggerSequence"), int) or payload.get("triggerSequence") < 0:
        findings.append(_finding("D1-02", "triggerSequence inválida"))
    questions = payload.get("questions") or []
    sources = payload.get("sources") or []
    if not questions:
        findings.append(_finding("D1-03", "briefing sem pergunta obrigatória"))
    if not sources:
        findings.append(_finding("D1-04", "briefing sem fonte declarada"))
    for field, items, key in (("question", questions, "questionId"), ("source", sources, "sourceId")):
        seen = set()
        for item in items:
            if not isinstance(item, Mapping) or not str(item.get(key) or item.get("id") or "").strip():
                findings.append(_finding("D1-05", f"{field} sem identificador"))
                continue
            identifier = str(item.get(key) or item.get("id"))
            if identifier in seen:
                findings.append(_finding("D1-06", f"{field} repetido: {identifier}"))
            seen.add(identifier)
            if field == "source" and not (str(item.get("sha256") or item.get("archivedSha256") or "").strip() or str(item.get("path") or "").strip()):
                findings.append(_finding("D1-07", f"fonte sem hash ou caminho: {identifier}"))
    if payload.get("briefingSha256") != artifact_hash(payload):
        findings.append(_finding("D1-08", "hash do briefing divergente"))
    return findings


def consume_d1_briefing(payload: Mapping, *, consumer_event_id: str, consumer_sequence: int, expected_sha256: str | None = None) -> dict:
    findings = validate_d1_briefing(payload)
    if findings:
        raise ValueError("briefing D1 inválido: " + "; ".join(item["detail"] for item in findings))
    digest = str(payload["briefingSha256"])
    if expected_sha256 and expected_sha256 != digest:
        raise ValueError("hash recebido do briefing D1 diverge")
    if consumer_sequence <= int(payload["triggerSequence"]):
        raise ValueError("consumo D1 deve ocorrer depois do evento de gatilho")
    return {"disciplineId": "D1", "briefingSha256": digest, "consumerEventId": consumer_event_id, "consumerSequence": consumer_sequence, "consumedAt": now_iso()}


def build_d3_hypotheses(*, case_id: str, trigger_event_id: str, trigger_sequence: int, hypotheses: Iterable[Mapping]) -> dict:
    items = []
    for index, raw in enumerate(hypotheses, start=1):
        item = dict(raw)
        item.setdefault("hypothesisId", f"H-{index:03d}")
        item.setdefault("status", "open")
        item["provisional"] = True
        item.setdefault("sourceIds", [])
        item.setdefault("reopenHistory", [])
        items.append(item)
    return {"schemaVersion": 1, "disciplineId": "D3", "caseId": case_id, "triggerEventId": trigger_event_id,
            "triggerSequence": trigger_sequence, "createdAt": now_iso(), "provisional": True, "hypotheses": items}


def validate_d3_hypotheses(payload: Mapping | None) -> list[dict]:
    if not isinstance(payload, Mapping):
        return [_finding("D3-00", "hipóteses de intake ausentes")]
    findings = []
    if payload.get("disciplineId") != "D3" or payload.get("provisional") is not True:
        findings.append(_finding("D3-01", "D3 deve permanecer provisória"))
    seen = set()
    for item in payload.get("hypotheses") or []:
        hid = str(item.get("hypothesisId") or "") if isinstance(item, Mapping) else ""
        if not hid or hid in seen:
            findings.append(_finding("D3-02", f"hypothesisId ausente ou duplicado: {hid}"))
        seen.add(hid)
        if item.get("status") not in VALID_D3_STATUS:
            findings.append(_finding("D3-03", f"status D3 inválido: {hid}"))
        if item.get("status") in {"rejected", "reopened", "superseded"} and not str(item.get("reopenReason") or item.get("reason") or "").strip():
            findings.append(_finding("D3-04", f"mudança de hipótese sem motivo: {hid}"))
    return findings


def reopen_hypothesis(payload: Mapping, hypothesis_id: str, *, reason: str, actor: str, event_id: str) -> dict:
    if not reason.strip():
        raise ValueError("reabertura de hipótese exige motivo")
    updated = deepcopy(dict(payload))
    for item in updated.get("hypotheses") or []:
        if str(item.get("hypothesisId")) == str(hypothesis_id):
            history = list(item.get("reopenHistory") or [])
            history.append({"eventId": event_id, "actor": actor, "reason": reason, "at": now_iso()})
            item["reopenHistory"] = history
            item["status"] = "reopened"
            item["reopenReason"] = reason
            return updated
    raise ValueError(f"hipótese não encontrada: {hypothesis_id}")


def build_d4_uncertain_decisions(*, case_id: str, trigger_event_id: str, trigger_sequence: int, items: Iterable[Mapping]) -> dict:
    decisions = []
    for index, raw in enumerate(items, start=1):
        item = dict(raw)
        item.setdefault("decisionId", f"U-{index:03d}")
        item.setdefault("status", "open")
        item.setdefault("action", "human_correction")
        item.setdefault("externalLabel", f"Ponto de conferência {index}")
        decisions.append(item)
    return {"schemaVersion": 1, "disciplineId": "D4", "caseId": case_id, "triggerEventId": trigger_event_id,
            "triggerSequence": trigger_sequence, "createdAt": now_iso(), "decisions": decisions}


def validate_d4_uncertain_decisions(payload: Mapping | None) -> list[dict]:
    if not isinstance(payload, Mapping):
        return [_finding("D4-00", "incertezas F7 ausentes")]
    findings = []
    seen = set()
    for item in payload.get("decisions") or []:
        did = str(item.get("decisionId") or "")
        if not did or did in seen:
            findings.append(_finding("D4-01", f"decisionId ausente ou duplicado: {did}"))
        seen.add(did)
        if item.get("status") not in VALID_D4_STATUS:
            findings.append(_finding("D4-02", f"status D4 inválido: {did}"))
        if item.get("action") not in VALID_D4_ACTIONS:
            findings.append(_finding("D4-03", f"ação D4 inválida: {did}"))
        if item.get("status") != "not_applicable" and not str(item.get("sourceLocator") or item.get("reason") or "").strip():
            findings.append(_finding("D4-04", f"incerteza sem trecho localizado ou razão: {did}"))
    return findings


def reconcile_f9(payload: Mapping, *, consumer_event_id: str, consumer_sequence: int) -> dict:
    findings = validate_d4_uncertain_decisions(payload)
    if findings:
        raise ValueError("incertezas D4 inválidas: " + "; ".join(item["detail"] for item in findings))
    if consumer_sequence <= int(payload.get("triggerSequence") or -1):
        raise ValueError("reconciliação F9 deve ocorrer depois do fechamento F7")
    internal = []
    external = []
    for item in payload.get("decisions") or []:
        internal.append({"decisionId": item["decisionId"], "action": item["action"], "status": item["status"], "sourceLocator": item.get("sourceLocator")})
        external.append({"label": item.get("externalLabel"), "action": item["action"], "status": item["status"]})
    return {"schemaVersion": 1, "disciplineId": "D4", "consumer": "F9", "consumerEventId": consumer_event_id,
            "consumerSequence": consumer_sequence, "internalMap": internal, "externalSafeMap": external}


def build_d5_handoff(*, case_id: str, trigger_event_id: str, trigger_sequence: int, artifact_path: Path, receiver: str, traps: Iterable[str] = ()) -> dict:
    digest = sha256_file(artifact_path)
    payload = {"schemaVersion": 1, "disciplineId": "D5", "caseId": case_id, "handoffId": f"HND-{trigger_event_id}",
               "triggerEventId": trigger_event_id, "triggerSequence": trigger_sequence, "artifactPath": str(artifact_path),
               "artifactSha256": digest, "receiver": receiver, "materialTraps": list(traps), "createdAt": now_iso()}
    payload["handoffSha256"] = artifact_hash(payload)
    return payload


def validate_d5_handoff(payload: Mapping | None, *, artifact_path: Path | None = None) -> list[dict]:
    if not isinstance(payload, Mapping):
        return [_finding("D5-00", "handoff ausente")]
    findings = []
    for field in ("handoffId", "caseId", "triggerEventId", "receiver", "artifactSha256", "handoffSha256"):
        if not str(payload.get(field) or "").strip():
            findings.append(_finding("D5-01", f"campo D5 ausente: {field}"))
    if artifact_path and artifact_path.is_file() and sha256_file(artifact_path) != payload.get("artifactSha256"):
        findings.append(_finding("D5-02", "hash do artefato entregue diverge"))
    if payload.get("handoffSha256") != artifact_hash(payload):
        findings.append(_finding("D5-03", "hash do handoff diverge"))
    if not payload.get("materialTraps"):
        findings.append(_finding("D5-04", "handoff sem armadilha material declarada", severity="p1"))
    return findings


def consume_d5_handoff(payload: Mapping, *, consumer_event_id: str, consumer_sequence: int, received_sha256: str) -> dict:
    findings = validate_d5_handoff(payload)
    if findings:
        raise ValueError("handoff D5 inválido: " + "; ".join(item["detail"] for item in findings))
    if consumer_sequence <= int(payload.get("triggerSequence") or -1):
        raise ValueError("consumo D5 fora de ordem")
    if received_sha256 != payload.get("artifactSha256"):
        raise ValueError("hash recebido do handoff D5 diverge")
    return {"disciplineId": "D5", "handoffId": payload["handoffId"], "consumerEventId": consumer_event_id,
            "consumerSequence": consumer_sequence, "receivedSha256": received_sha256, "consumedAt": now_iso()}


def render_handoff(payload: Mapping) -> str:
    return "# HANDOFF — revisão cruzada\n\n" + "\n".join([
        f"- Caso: {payload.get('caseId')}",
        f"- Evento de gatilho: {payload.get('triggerEventId')} (sequência {payload.get('triggerSequence')})",
        f"- Destinatário: {payload.get('receiver')}",
        f"- Artefato: {payload.get('artifactPath')}",
        f"- SHA-256: {payload.get('artifactSha256')}",
        "\n## Armadilhas materiais\n",
        *[f"- {trap}" for trap in payload.get("materialTraps") or []],
    ]) + "\n"


def write_handoff(payload: Mapping, output_dir: Path) -> tuple[Path, Path]:
    findings = validate_d5_handoff(payload)
    if findings:
        raise ValueError("handoff D5 inválido: " + "; ".join(item["detail"] for item in findings))
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    md_path = output_dir / "HANDOFF.md"
    receipt_path = output_dir / "HANDOFF_RECEIPT.json"
    atomic_write_text(md_path, render_handoff(payload))
    atomic_write_json(receipt_path, {"schemaVersion": 1, **dict(payload), "renderedSha256": sha256_file(md_path)})
    return md_path, receipt_path


def validate_d6_decision(payload: Mapping | None) -> list[dict]:
    if not isinstance(payload, Mapping):
        return [_finding("D6-00", "ficha de decisão ausente")]
    findings = []
    for field in ("decisionId", "topic", "status", "decision", "source", "reopenWhen"):
        if not str(payload.get(field) or "").strip():
            findings.append(_finding("D6-01", f"campo de decisão ausente: {field}"))
    if payload.get("status") not in VALID_D6_STATUS:
        findings.append(_finding("D6-02", "status de decisão inválido"))
    return findings


def write_d6_decision(payload: Mapping, decisions_dir: Path) -> Path:
    findings = validate_d6_decision(payload)
    if findings:
        raise ValueError("decisão D6 inválida: " + "; ".join(item["detail"] for item in findings))
    path = Path(decisions_dir) / f"{payload['decisionId']}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        existing = json.loads(path.read_text(encoding="utf-8"))
        if _digest(existing) != _digest(dict(payload)):
            raise ValueError(f"decisão D6 existente divergente: {path.name}")
        return path
    atomic_write_json(path, dict(payload))
    return path


def validate_decisions_directory(decisions_dir: Path) -> dict:
    findings = []
    files = list(Path(decisions_dir).glob("*.json")) if Path(decisions_dir).is_dir() else []
    for path in files:
        try:
            payload = json.loads(path.read_text(encoding="utf-8-sig"))
        except json.JSONDecodeError:
            findings.append(_finding("D6-03", f"JSON inválido: {path.name}"))
            continue
        findings.extend({**item, "artifact": path.name} for item in validate_d6_decision(payload))
    return {"records": len(files), "findings": findings, "approved": not any(item.get("severity") == "p0" for item in findings)}


def _main() -> int:
    parser = argparse.ArgumentParser(description="Contratos experimentais das disciplinas FORJA")
    parser.add_argument("decisions_dir", type=Path)
    args = parser.parse_args()
    result = validate_decisions_directory(args.decisions_dir)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["approved"] else 1


if __name__ == "__main__":
    raise SystemExit(_main())
