import argparse
import hashlib
import json
import os
import re
import socket
import subprocess
import sys
from datetime import date, datetime, timezone
from pathlib import Path

from dashboard_enrichment import enrich_snapshot
from office_io import atomic_write_json


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "demandas.json"
MANUAL = ROOT / "data" / "intervencoes_manuais.json"
STATUS_OUT = ROOT / "data" / "hermes_bridge_status.json"
SNAPSHOT_OUT = ROOT / "data" / "hermes_snapshot.json"
APPLY_MANUAL = ROOT / "scripts" / "apply_manual_updates.py"
REMOTE_SCRIPT = ROOT / "scripts" / "hermes_office_panel_remote.py"
REMOTE_STATE = "/root/.hermes/state/office-demand-panel"
REMOTE_BIN = "/root/.hermes/bin/office-demand-panel"
RENDER_SCRIPT = ROOT / "scripts" / "render_dashboard.py"
REMOTE_HTML = ROOT / "PAINEL_ESCRITORIO_MEDINA_OSORIO.html"
REMOTE_WEB_DIR = "/var/www/escritorio-painel/p-yjp3RHTnCnaMntEV"
FORJA_STATUS = ROOT / "data" / "forja_status.json"
REMOTE_SCRIPT_VERSION = "2.1.0"


def now_iso():
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def read_json(path, fallback):
    if not path.exists():
        return fallback
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path, data):
    atomic_write_json(path, data)


def ssh_command(ssh_alias, *remote_args):
    return ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=12", ssh_alias, *remote_args]


def scp_command(source, target):
    return ["scp", "-o", "BatchMode=yes", "-o", "ConnectTimeout=12", str(source), target]


def truncate(value, limit=500):
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    return text if len(text) <= limit else text[: limit - 3].rstrip() + "..."


def parse_date(value):
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def urgency_label(item):
    if item.get("status") == "cumprida":
        return "cumprida"
    due = parse_date(item.get("prazo"))
    if due:
        delta = (due - date.today()).days
        if delta < 0:
            return "vencida"
        if delta <= 2:
            return "48h"
        if delta <= 7:
            return f"{delta}d"
    return item.get("urgenciaManual") or "normal"


def urgency_rank(item):
    label = urgency_label(item)
    if label == "vencida":
        return 0
    if label == "48h":
        return 1
    if item.get("urgenciaManual") == "alta":
        return 2
    due = parse_date(item.get("prazo"))
    if due:
        return 3 + max((due - date.today()).days, 0)
    return 50


def compact_item(item, forja=None):
    derived = item.get("derived") or {}
    forja = forja or {}
    return {
        "id": item.get("id"),
        "titulo": truncate(item.get("titulo"), 180),
        "clienteOuCaso": truncate(item.get("clienteOuCaso"), 160),
        "origem": item.get("origem"),
        "fonte": derived.get("fonteLabel") or item.get("origem"),
        "emailLinks": derived.get("emailLinks") or [],
        "datasMencionadas": [
            {"date": d.get("date"), "context": truncate(d.get("context"), 120), "source": d.get("source")}
            for d in (derived.get("dateMentions") or [])[:5]
        ],
        "status": item.get("status"),
        "prazo": item.get("prazo"),
        "prazoTexto": truncate(item.get("prazoTexto"), 180),
        "urgencia": urgency_label(item),
        "urgenciaManual": item.get("urgenciaManual"),
        "resumo": truncate(item.get("resumo"), 420),
        "proximaAcao": truncate(item.get("proximaAcao"), 420),
        "pasta": item.get("pasta"),
        "respondidoComConteudo": bool(item.get("respondidoComConteudo")),
        "comentarios": int((item.get("manual") or {}).get("commentCount") or 0),
        "ultimoComentario": truncate((item.get("manual") or {}).get("lastComment"), 260),
        "tags": item.get("tags") or [],
        "notificationState": "suppressed_fulfilled" if item.get("status") == "cumprida" else "actionable",
        "forja": {
            "lifecycleStatus": forja.get("lifecycleStatus"),
            "phaseCursor": forja.get("phaseCursor"),
            "blockers": len(forja.get("blockers") or []),
            "nextAction": truncate(forja.get("nextAction"), 260),
            "managementStatusWins": True,
        } if forja else None,
    }


def build_snapshot(data):
    forja_data = read_json(FORJA_STATUS, {"items": {}})
    forja_items = forja_data.get("items") or {}
    enriched = enrich_snapshot({"demandas": data, "forja": forja_data}, ROOT.parent)
    items = enriched.get("demandas", {}).get("demandas", [])
    open_items = [item for item in items if item.get("status") != "cumprida"]
    done_items = [item for item in items if item.get("status") == "cumprida"]
    priorities = sorted(open_items, key=lambda item: (urgency_rank(item), str(item.get("prazo") or "9999"), str(item.get("titulo") or "")))
    urgent = [item for item in open_items if urgency_label(item) in {"vencida", "48h"} or item.get("urgenciaManual") == "alta"]
    compact_priorities = [compact_item(item, forja_items.get(item.get("id"))) for item in priorities[:20]]
    fingerprint_payload = [
        {
            "id": item.get("id"),
            "status": item.get("status"),
            "prazo": item.get("prazo"),
            "proximaAcao": item.get("proximaAcao"),
        }
        for item in compact_priorities
    ]
    notification_fingerprint = hashlib.sha256(
        json.dumps(fingerprint_payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
    ).hexdigest()
    return {
        "schema": 2,
        "privacy": "operational-summary-no-raw-chat",
        "updatedAt": now_iso(),
        "sourceHost": socket.gethostname(),
        "panelUrlLocalOnly": "http://127.0.0.1:8765/",
        "freshness": {"maxAgeMinutes": 180, "onStale": "suppress_demands_and_request_sync"},
        "authority": {
            "source": "demandas.json+intervencoes_manuais+delivery_evidence",
            "openOnlyIsActionable": True,
            "managementStatusWinsOverForja": True,
            "factoryResponsibilityEndsOnDeliveryToOffice": True,
            "protocolOrReceiptRequiredFromIgor": False,
        },
        "notificationFingerprint": notification_fingerprint,
        "statusIndex": [
            {
                "id": item.get("id"),
                "titulo": truncate(item.get("titulo"), 180),
                "status": item.get("status"),
                "gmailIds": list(dict.fromkeys(
                    [str(value) for value in (item.get("emailsRecebidos") or []) if value]
                    + [str(value) for value in (item.get("emailsResposta") or []) if value]
                    + [str(value) for value in (item.get("threadIds") or []) if value]
                )),
                "hasDeliveryEvidence": bool(str(item.get("evidenciaResposta") or "").strip()),
            }
            for item in items
        ],
        "totals": {
            "total": len(items),
            "open": len(open_items),
            "done": len(done_items),
            "urgent": len(urgent),
            "email": len([item for item in items if item.get("origem") == "email"]),
            "whatsapp": len([item for item in items if str(item.get("origem", "")).startswith("whatsapp")]),
        },
        "actionableItems": compact_priorities,
        "priorities": compact_priorities,
        "openItems": [compact_item(item, forja_items.get(item.get("id"))) for item in open_items],
        "doneRecent": [compact_item(item, forja_items.get(item.get("id"))) for item in done_items[-10:]],
    }


def run(cmd, timeout=60, check=True):
    proc = subprocess.run(cmd, text=True, capture_output=True, timeout=timeout)
    if check and proc.returncode != 0:
        raise RuntimeError(f"command failed: {' '.join(cmd)}\n{proc.stderr[-1000:]}")
    return proc


def install_remote(ssh_alias):
    run(ssh_command(ssh_alias, f"mkdir -p {REMOTE_STATE}/inbox {REMOTE_STATE}/outbox {REMOTE_STATE}/archive /root/.hermes/bin"), timeout=30)
    run(scp_command(REMOTE_SCRIPT, f"{ssh_alias}:{REMOTE_BIN}"), timeout=60)
    run(ssh_command(ssh_alias, f"chmod 700 {REMOTE_BIN}"), timeout=30)


def export_snapshot(ssh_alias):
    data = read_json(DATA, {"demandas": []})
    snapshot = build_snapshot(data)
    write_json(SNAPSHOT_OUT, snapshot)
    run(scp_command(SNAPSHOT_OUT, f"{ssh_alias}:{REMOTE_STATE}/panel_snapshot.json"), timeout=60)
    publish_remote_panel(ssh_alias)
    return snapshot


def publish_remote_panel(ssh_alias):
    """Publica o painel em modo leitura na VPS (https com senha) para acesso pelo celular."""
    run([sys.executable, str(RENDER_SCRIPT)], timeout=60)
    if not REMOTE_HTML.exists():
        return
    run(scp_command(REMOTE_HTML, f"{ssh_alias}:{REMOTE_WEB_DIR}/index.html"), timeout=60)


def manual_entry(manual, item_id):
    entry = manual.setdefault("items", {}).setdefault(item_id, {"comentarios": [], "overrides": {}})
    entry.setdefault("comentarios", [])
    entry.setdefault("overrides", {})
    return entry


def add_comment(manual, item_id, text, tipo="hermes"):
    entry = manual_entry(manual, item_id)
    entry["comentarios"].append(
        {
            "id": f"{tipo}-{int(datetime.now().timestamp() * 1000)}",
            "at": now_iso(),
            "tipo": tipo,
            "texto": text,
            "autor": "Hermes VPS",
        }
    )
    entry["updatedAt"] = now_iso()


def safe_folder_name(value, fallback):
    text = re.sub(r'[<>:"/\\|?*\x00-\x1f]', " ", value or fallback)
    text = re.sub(r"\s+", " ", text).strip(" .")
    return (text[:110] or fallback).strip()


def create_task(data, item):
    queue_id = item.get("queueId")
    for existing in data.get("demandas", []):
        if (existing.get("manualSource") or {}).get("hermesQueueId") == queue_id:
            return existing.get("id"), False
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    title = item.get("titulo") or "Tarefa Hermes"
    item_id = f"hermes-{re.sub(r'[^A-Za-z0-9]+', '-', queue_id or timestamp).strip('-')[:48]}"
    folder_name = safe_folder_name(f"Hermes WhatsApp - {title} - {timestamp}", f"Hermes WhatsApp {timestamp}")
    folder = ROOT.parent / folder_name
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "COMANDO_HERMES.md").write_text(
        "# Tarefa recebida do Hermes\n\n"
        f"- ID: `{item_id}`\n"
        f"- Queue ID Hermes: `{queue_id}`\n"
        f"- Criada em: {now_iso()}\n"
        f"- Prazo: {item.get('prazo') or 'sem prazo'}\n\n"
        "## Resumo\n\n"
        f"{item.get('resumo') or title}\n\n"
        "## Observação do Hermes\n\n"
        f"{item.get('sourceNote') or item.get('note') or ''}\n",
        encoding="utf-8",
    )
    data.setdefault("demandas", []).append(
        {
            "id": item_id,
            "titulo": title,
            "clienteOuCaso": item.get("clienteOuCaso") or title,
            "origem": item.get("origem") or "hermes_whatsapp",
            "emailsRecebidos": [],
            "emailsResposta": [],
            "pasta": folder_name,
            "recebidoEm": item.get("createdAt") or now_iso(),
            "prazo": item.get("prazo"),
            "prazoTexto": "prazo recebido do Hermes" if item.get("prazo") else "sem prazo definido no Hermes",
            "resumo": item.get("resumo") or title,
            "proximaAcao": item.get("proximaAcao") or "Executar ou detalhar a tarefa recebida pelo Hermes/WhatsApp.",
            "status": "aberta",
            "respondidoComConteudo": False,
            "evidenciaResposta": "",
            "urgenciaManual": item.get("urgenciaManual") or "media",
            "anexos": {
                "diretosBaixados": None,
                "diretosEsperados": None,
                "externosPendentes": True,
                "observacao": "Tarefa recebida pela ponte Hermes; conferir se há anexos no WhatsApp/e-mail.",
            },
            "tags": item.get("tags") or ["hermes", "whatsapp"],
            "manualSource": {"hermesQueueId": queue_id, "source": item.get("source")},
        }
    )
    return item_id, True


def apply_remote_items(items):
    data = read_json(DATA, {"schema": 1, "demandas": []})
    manual = read_json(MANUAL, {"schema": 1, "updatedAt": now_iso(), "items": {}})
    applied = []
    for item in items:
        queue_id = item.get("queueId")
        typ = item.get("type")
        if not queue_id or typ == "error":
            continue
        if typ == "comment" and item.get("itemId") and item.get("text"):
            add_comment(manual, item["itemId"], item["text"], tipo="hermes-comment")
            applied.append(queue_id)
        elif typ == "status" and item.get("itemId") and item.get("status") in ("aberta", "cumprida"):
            if item.get("status") == "cumprida" and not str(item.get("note") or "").strip():
                continue
            entry = manual_entry(manual, item["itemId"])
            entry["overrides"]["status"] = item["status"]
            entry["overrides"]["respondidoComConteudo"] = item["status"] == "cumprida"
            if item.get("note"):
                entry["overrides"]["evidenciaResposta"] = item["note"]
                entry["overrides"]["evidenciaTipo"] = item.get("evidenceType") or "manual"
            add_comment(manual, item["itemId"], item.get("note") or f"Hermes marcou como {item['status']}.", tipo="hermes-status")
            applied.append(queue_id)
        elif typ == "task":
            item_id, created = create_task(data, item)
            add_comment(manual, item_id, item.get("sourceNote") or "Tarefa importada da fila Hermes.", tipo="hermes-task")
            applied.append(queue_id)
    if applied:
        data["updatedAt"] = now_iso()
        manual["updatedAt"] = now_iso()
        write_json(DATA, data)
        write_json(MANUAL, manual)
        run([sys.executable, str(APPLY_MANUAL)], timeout=30)
    return applied


def pull_updates(ssh_alias):
    proc = run(ssh_command(ssh_alias, REMOTE_BIN, "pending", "--json"), timeout=60)
    payload = json.loads(proc.stdout)
    items = payload.get("items") or []
    applied = apply_remote_items(items)
    for queue_id in applied:
        run(ssh_command(ssh_alias, REMOTE_BIN, "archive", "--queue-id", queue_id), timeout=30, check=False)
    return {"pending": len(items), "applied": len(applied), "appliedIds": applied}


def sync(args):
    status = {"ok": False, "updatedAt": now_iso(), "sshAlias": args.ssh_alias}
    try:
        remote_check = run(ssh_command(args.ssh_alias, f"test -x {REMOTE_BIN} && {REMOTE_BIN} --version"), timeout=20, check=False)
        remote_version = (remote_check.stdout or "").strip()
        if args.install or remote_check.returncode != 0 or remote_version != REMOTE_SCRIPT_VERSION:
            install_remote(args.ssh_alias)
            status["installed"] = True
        else:
            status["installed"] = False
        pulled = pull_updates(args.ssh_alias)
        snapshot = export_snapshot(args.ssh_alias)
        status.update({"ok": True, "pulled": pulled, "snapshotTotals": snapshot.get("totals")})
    except Exception as exc:
        status["error"] = str(exc)
    write_json(STATUS_OUT, status)
    if not args.quiet:
        print(json.dumps(status, ensure_ascii=False, indent=2))
    return 0 if status["ok"] else 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ssh-alias", default="hermes")
    parser.add_argument("--install", action="store_true")
    parser.add_argument("--quiet", action="store_true")
    sub = parser.add_subparsers(dest="cmd")
    sub.add_parser("sync")
    sub.add_parser("export")
    sub.add_parser("install")
    args = parser.parse_args()
    if args.cmd == "install":
        install_remote(args.ssh_alias)
        print(json.dumps({"ok": True, "installed": True}, ensure_ascii=False))
        return 0
    if args.cmd == "export":
        snapshot = export_snapshot(args.ssh_alias)
        print(json.dumps({"ok": True, "totals": snapshot.get("totals")}, ensure_ascii=False))
        return 0
    return sync(args)


if __name__ == "__main__":
    raise SystemExit(main())
