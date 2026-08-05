#!/usr/bin/env python3
import argparse
import json
import os
import re
import shutil
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path("/root/.hermes/state/office-demand-panel")
VERSION = "2.1.0"
SNAPSHOT = ROOT / "panel_snapshot.json"
INBOX = ROOT / "inbox"
ARCHIVE = ROOT / "archive"
DEFAULT_MAX_AGE_MINUTES = 180


def now_iso():
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def read_json(path, fallback):
    if not path.exists():
        return fallback
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    temp_path = Path(temp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(data, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_path, path)
    finally:
        temp_path.unlink(missing_ok=True)


def queue_id(prefix):
    return f"{prefix}-{int(time.time() * 1000)}"


def write_queue(payload):
    ROOT.mkdir(parents=True, exist_ok=True)
    INBOX.mkdir(parents=True, exist_ok=True)
    payload.setdefault("queueId", queue_id(payload.get("type", "update")))
    payload.setdefault("createdAt", now_iso())
    payload.setdefault("source", "hermes-vps")
    target = INBOX / f"{payload['queueId']}.json"
    write_json(target, payload)
    return payload


def snapshot_health(snap):
    updated_at = snap.get("updatedAt")
    max_age = int((snap.get("freshness") or {}).get("maxAgeMinutes") or DEFAULT_MAX_AGE_MINUTES)
    if not updated_at:
        return {"stale": True, "ageMinutes": None, "maxAgeMinutes": max_age, "reason": "snapshot_missing"}
    try:
        parsed = datetime.fromisoformat(str(updated_at).replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        age = max(0, int((datetime.now(timezone.utc) - parsed.astimezone(timezone.utc)).total_seconds() / 60))
    except (TypeError, ValueError):
        return {"stale": True, "ageMinutes": None, "maxAgeMinutes": max_age, "reason": "invalid_updated_at"}
    return {"stale": age > max_age, "ageMinutes": age, "maxAgeMinutes": max_age, "reason": "age_limit" if age > max_age else None}


def snapshot_status(args):
    snap = read_json(SNAPSHOT, {})
    health = snapshot_health(snap)
    if args.json:
        payload = dict(snap)
        payload["snapshotHealth"] = health
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    totals = snap.get("totals") or {}
    print(f"Painel do escritório: {totals.get('total', 0)} demandas")
    print(f"Abertas: {totals.get('open', 0)} | Cumpridas: {totals.get('done', 0)} | Urgentes: {totals.get('urgent', 0)}")
    print(f"Atualizado: {snap.get('updatedAt', 'sem snapshot')}")
    print(f"Frescor: {'DESATUALIZADO - não cobrar' if health['stale'] else 'atual'} | idade: {health.get('ageMinutes')} min")


def priorities(args):
    snap = read_json(SNAPSHOT, {})
    health = snapshot_health(snap)
    items = snap.get("actionableItems") or snap.get("priorities") or []
    if health["stale"]:
        payload = {
            "ok": False,
            "stale": True,
            "updatedAt": snap.get("updatedAt"),
            "snapshotHealth": health,
            "notificationFingerprint": snap.get("notificationFingerprint"),
            "priorities": [],
            "instruction": "Snapshot desatualizado: não cobrar demandas antigas; solicitar sincronização local.",
        }
        if args.json:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            print(payload["instruction"])
        return
    if args.json:
        print(json.dumps({
            "ok": True,
            "stale": False,
            "updatedAt": snap.get("updatedAt"),
            "snapshotHealth": health,
            "authority": snap.get("authority") or {},
            "notificationFingerprint": snap.get("notificationFingerprint"),
            "priorities": items,
        }, ensure_ascii=False, indent=2))
        return
    if not items:
        print("Sem prioridades abertas no snapshot.")
        return
    for idx, item in enumerate(items[: args.limit], start=1):
        due = item.get("prazo") or "sem prazo"
        source = item.get("fonte") or item.get("origem") or "fonte nao informada"
        print(f"{idx}. [{item.get('id')}] {item.get('titulo')} | fonte: {source} | prazo: {due} | urgencia: {item.get('urgencia')}")
        print(f"   Proxima acao: {item.get('proximaAcao', '')}")
        if item.get("datasMencionadas"):
            dates = ", ".join(d.get("date", "") for d in item.get("datasMencionadas", []) if d.get("date"))
            if dates:
                print(f"   Datas no email/comando a conferir: {dates}")


def add_task(args):
    payload = write_queue(
        {
            "type": "task",
            "titulo": args.title,
            "resumo": args.summary or args.title,
            "prazo": args.deadline,
            "urgenciaManual": args.priority,
            "origem": args.origin,
            "sourceNote": args.note or "",
            "tags": ["hermes", "whatsapp", "vps"],
        }
    )
    print(json.dumps({"ok": True, "queued": payload}, ensure_ascii=False, indent=2))


def add_comment(args):
    payload = write_queue(
        {
            "type": "comment",
            "itemId": args.id,
            "text": args.text,
            "note": args.note or "",
        }
    )
    print(json.dumps({"ok": True, "queued": payload}, ensure_ascii=False, indent=2))


def set_status(args):
    if args.status == "cumprida" and not (args.note or "").strip():
        raise SystemExit("status cumprida exige --note com evidencia concreta")
    payload = write_queue(
        {
            "type": "status",
            "itemId": args.id,
            "status": args.status,
            "note": args.note or "",
            "evidenceType": args.evidence_type or "manual",
        }
    )
    print(json.dumps({"ok": True, "queued": payload}, ensure_ascii=False, indent=2))


def pending(args):
    INBOX.mkdir(parents=True, exist_ok=True)
    items = []
    for path in sorted(INBOX.glob("*.json")):
        try:
            payload = read_json(path, {})
            payload["_file"] = str(path)
            items.append(payload)
        except Exception as exc:
            items.append({"queueId": path.stem, "type": "error", "error": str(exc), "_file": str(path)})
    print(json.dumps({"ok": True, "count": len(items), "items": items}, ensure_ascii=False, indent=2))


def archive(args):
    INBOX.mkdir(parents=True, exist_ok=True)
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    safe = re.sub(r"[^A-Za-z0-9_.-]+", "_", args.queue_id)
    source = INBOX / f"{safe}.json"
    if not source.exists():
        print(json.dumps({"ok": False, "error": "queue item not found", "queueId": args.queue_id}, ensure_ascii=False))
        return
    dest = ARCHIVE / f"{safe}.json"
    shutil.move(str(source), str(dest))
    print(json.dumps({"ok": True, "archived": str(dest)}, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description="Hermes bridge for Igor office demand panel.")
    parser.add_argument("--version", action="version", version=VERSION)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("status")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=snapshot_status)

    p = sub.add_parser("priorities")
    p.add_argument("--json", action="store_true")
    p.add_argument("--limit", type=int, default=10)
    p.set_defaults(func=priorities)

    p = sub.add_parser("add-task")
    p.add_argument("--title", required=True)
    p.add_argument("--summary", default="")
    p.add_argument("--deadline", default=None)
    p.add_argument("--priority", choices=["alta", "media", "baixa"], default="media")
    p.add_argument("--origin", default="hermes_whatsapp")
    p.add_argument("--note", default="")
    p.set_defaults(func=add_task)

    p = sub.add_parser("comment")
    p.add_argument("--id", required=True)
    p.add_argument("--text", required=True)
    p.add_argument("--note", default="")
    p.set_defaults(func=add_comment)

    p = sub.add_parser("status-set")
    p.add_argument("--id", required=True)
    p.add_argument("--status", choices=["aberta", "cumprida"], required=True)
    p.add_argument("--note", default="")
    p.add_argument("--evidence-type", choices=["email", "whatsapp", "protocolo", "arquivo", "manual"], default="manual")
    p.set_defaults(func=set_status)

    p = sub.add_parser("pending")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=pending)

    p = sub.add_parser("archive")
    p.add_argument("--queue-id", required=True)
    p.set_defaults(func=archive)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
