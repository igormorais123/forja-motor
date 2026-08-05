#!/usr/bin/env python3
"""Inventaria áudios recebidos do Fábio sem expor conteúdo de mensagens."""

from __future__ import annotations

import collections
import datetime as dt
import json
import sqlite3
from pathlib import Path


CHAT_ID = "60855441973370@lid"
DB = Path("/root/.hermes/state/whatsapp-personal/messages.sqlite")
OLD_MANIFEST = Path("/root/.hermes/state/office-demand-audio-intake/fabio_recent_audio_manifest.json")
TZ = dt.timezone(dt.timedelta(hours=-3))


def media_paths(raw: str | None) -> list[str]:
    if not raw:
        return []
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return [raw]
    if isinstance(parsed, list):
        return [str(item) for item in parsed]
    if isinstance(parsed, dict):
        return [str(value) for value in parsed.values() if isinstance(value, str)]
    return [str(parsed)]


def main() -> None:
    connection = sqlite3.connect(DB)
    connection.row_factory = sqlite3.Row
    rows = connection.execute(
        """
        SELECT message_id, timestamp, direction, message_type, media_type, media_paths
          FROM messages
         WHERE chat_id = ? AND has_media = 1
         ORDER BY timestamp DESC
         LIMIT 200
        """,
        (CHAT_ID,),
    ).fetchall()

    audio_rows = []
    for row in rows:
        kind = f"{row['message_type'] or ''} {row['media_type'] or ''}".lower()
        if "audio" in kind or "ptt" in kind:
            audio_rows.append(row)

    previous = json.loads(OLD_MANIFEST.read_text(encoding="utf-8")) if OLD_MANIFEST.exists() else {"items": []}
    seen = {str(item.get("message_id")) for item in previous.get("items", [])}
    by_date = collections.Counter(
        dt.datetime.fromtimestamp(int(row["timestamp"]), TZ).date().isoformat()
        for row in audio_rows
    )
    incoming_labels = {"in", "incoming", "from_contact", "received"}
    incoming_audio = [row for row in audio_rows if str(row["direction"] or "").lower() in incoming_labels]
    pending = [row for row in reversed(incoming_audio) if str(row["message_id"]) not in seen]

    result = {
        "chatId": CHAT_ID,
        "windowAudioCount": len(audio_rows),
        "incomingAudioCount": len(incoming_audio),
        "directions": dict(collections.Counter(str(row["direction"] or "") for row in audio_rows)),
        "alreadyInPreviousBatch": sum(str(row["message_id"]) in seen for row in incoming_audio),
        "pendingCount": len(pending),
        "byDate": dict(sorted(by_date.items())),
        "pending": [
            {
                "messageId": str(row["message_id"]),
                "timestamp": dt.datetime.fromtimestamp(int(row["timestamp"]), TZ).isoformat(),
                "paths": media_paths(row["media_paths"]),
            }
            for row in pending
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
