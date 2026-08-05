#!/usr/bin/env python3
"""Transcreve no Hermes um lote diário de áudios recebidos, sem imprimir conteúdo."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import sqlite3
from pathlib import Path

import whisper


CHAT_ID = "60855441973370@lid"
DB = Path("/root/.hermes/state/whatsapp-personal/messages.sqlite")
STATE = Path("/root/.hermes/state/office-demand-audio-intake")
TZ = dt.timezone(dt.timedelta(hours=-3))
INCOMING = {"in", "incoming", "from_contact", "received"}


def parse_paths(raw: str | None) -> list[Path]:
    if not raw:
        return []
    try:
        value = json.loads(raw)
    except json.JSONDecodeError:
        value = raw
    if isinstance(value, str):
        return [Path(value)]
    if isinstance(value, list):
        return [Path(str(item)) for item in value]
    if isinstance(value, dict):
        return [Path(str(item)) for item in value.values() if isinstance(item, str)]
    return []


def select_audio(day: dt.date) -> list[dict]:
    start = int(dt.datetime.combine(day, dt.time.min, TZ).timestamp())
    end = int(dt.datetime.combine(day + dt.timedelta(days=1), dt.time.min, TZ).timestamp())
    connection = sqlite3.connect(DB)
    connection.row_factory = sqlite3.Row
    rows = connection.execute(
        """
        SELECT message_id, timestamp, direction, message_type, media_type, media_paths
          FROM messages
         WHERE chat_id = ? AND has_media = 1 AND timestamp >= ? AND timestamp < ?
         ORDER BY timestamp
        """,
        (CHAT_ID, start, end),
    ).fetchall()
    selected = []
    for row in rows:
        kind = f"{row['message_type'] or ''} {row['media_type'] or ''}".lower()
        if str(row["direction"] or "").lower() not in INCOMING:
            continue
        if "audio" not in kind and "ptt" not in kind:
            continue
        paths = [path for path in parse_paths(row["media_paths"]) if path.exists()]
        if not paths:
            continue
        selected.append(
            {
                "messageId": str(row["message_id"]),
                "timestamp": int(row["timestamp"]),
                "at": dt.datetime.fromtimestamp(int(row["timestamp"]), TZ).isoformat(),
                "path": paths[0],
            }
        )
    return selected


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True, help="Data local em YYYY-MM-DD")
    parser.add_argument("--model", default="small")
    args = parser.parse_args()
    day = dt.date.fromisoformat(args.date)
    items = select_audio(day)
    output_dir = STATE / f"whisper-{day.strftime('%Y%m%d')}-fabio"
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = STATE / f"fabio_audio_manifest_{day.strftime('%Y%m%d')}.json"

    pending = []
    manifest_items = []
    for item in items:
        digest = hashlib.sha256(item["messageId"].encode("utf-8")).hexdigest()[:12]
        target = output_dir / f"audio_{item['timestamp']}_{digest}.json"
        record = {**item, "path": str(item["path"]), "transcript": str(target)}
        manifest_items.append(record)
        if not target.exists():
            pending.append((record, target))

    print(json.dumps({"selected": len(items), "pending": len(pending), "outputDir": str(output_dir)}), flush=True)
    model = whisper.load_model(args.model) if pending else None
    completed = 0
    failures = []
    for record, target in pending:
        try:
            result = model.transcribe(
                record["path"],
                language="pt",
                task="transcribe",
                fp16=False,
                temperature=0,
                verbose=False,
            )
            target.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
            completed += 1
            print(json.dumps({"progress": completed, "total": len(pending), "at": record["at"]}), flush=True)
        except Exception as exc:  # mantém o lote avançando e registra a falha sem conteúdo
            failures.append({"messageId": record["messageId"], "error": type(exc).__name__})

    manifest = {
        "schemaVersion": 1,
        "createdAt": dt.datetime.now(TZ).isoformat(),
        "date": day.isoformat(),
        "chatId": CHAT_ID,
        "model": args.model,
        "count": len(manifest_items),
        "completedNow": completed,
        "failures": failures,
        "items": manifest_items,
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"ok": not failures, "count": len(items), "completedNow": completed, "failures": len(failures), "manifest": str(manifest_path)}), flush=True)


if __name__ == "__main__":
    main()
