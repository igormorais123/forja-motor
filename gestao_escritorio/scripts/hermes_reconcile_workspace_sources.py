#!/usr/bin/env python3
"""Reconciles the VPS workspace index with the authoritative office snapshot."""

import json
import re
import sqlite3
import unicodedata
from pathlib import Path


SNAPSHOT = Path("/root/.hermes/state/office-demand-panel/panel_snapshot.json")
WORKSPACE_DB = Path("/root/.hermes/state/fabio_osorio_workspace.sqlite3")


def normalize(value):
    text = unicodedata.normalize("NFKD", str(value or ""))
    text = "".join(char for char in text if not unicodedata.combining(char)).lower()
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


def main():
    if not SNAPSHOT.is_file() or not WORKSPACE_DB.is_file():
        print(json.dumps({"ok": False, "reason": "snapshot_or_workspace_db_missing"}))
        return 1
    snapshot = json.loads(SNAPSHOT.read_text(encoding="utf-8-sig"))
    index = snapshot.get("statusIndex") or []
    by_gmail = {}
    normalized = []
    for item in index:
        for gmail_id in item.get("gmailIds") or []:
            by_gmail[str(gmail_id)] = item
        title = normalize(item.get("titulo"))
        if title:
            normalized.append((title, item))

    changed = 0
    matched = 0
    con = sqlite3.connect(WORKSPACE_DB, timeout=30)
    try:
        rows = con.execute("select key, kind, title, status from sources where kind in ('gmail','manual')").fetchall()
        for key, kind, title, current in rows:
            if normalize(title).startswith("notificacao prazo medina"):
                if current != "ignorado":
                    con.execute("update sources set status='ignorado', updated_at=current_timestamp where key=?", (key,))
                    changed += 1
                continue
            gmail_id = str(key).split(":", 1)[1] if ":" in str(key) else ""
            item = by_gmail.get(gmail_id)
            source_title = normalize(title)
            if item is None and kind == "manual" and "cafelana" in source_title:
                if "embargos de declaracao" in source_title:
                    item = next((entry for entry in index if "cafelana-edcl" in str(entry.get("id") or "")), None)
                elif "impugnacao" in source_title or "contrarrazoes ao recurso" in source_title:
                    item = next((entry for entry in index if "cafelana-agint" in str(entry.get("id") or "")), None)
            if item is None:
                candidates = [entry for norm, entry in normalized if len(norm) >= 18 and (norm in source_title or source_title in norm)]
                if len(candidates) == 1:
                    item = candidates[0]
            if item is None:
                continue
            matched += 1
            target = "cumprida" if item.get("status") == "cumprida" else "aberta"
            if current != target:
                con.execute("update sources set status=?, updated_at=current_timestamp where key=?", (target, key))
                changed += 1
        con.commit()
    finally:
        con.close()
    print(json.dumps({"ok": True, "matched": matched, "changed": changed, "snapshotUpdatedAt": snapshot.get("updatedAt")}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
