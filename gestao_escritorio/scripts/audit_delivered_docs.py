import base64
import email.utils
import json
import re
import subprocess
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

from office_io import atomic_write_json


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
DATA_PATH = ROOT / "data" / "demandas.json"
OUT_JSON = ROOT / "data" / "entregas_fabio_osorio.json"
OUT_MD = WORKSPACE / "ENTREGAS_FABIO_OSORIO.md"
ARCHIVE = ROOT / "entregas_fabio_osorio"
GWS_CMD = Path.home() / "AppData" / "Roaming" / "npm" / "gws.cmd"

SENT_QUERY = "in:sent after:2026/06/01 -in:trash -in:spam"
MAX_PAGES = 8
PAGE_SIZE = 100
DOC_EXTS = (".docx", ".doc", ".pdf", ".odt", ".rtf", ".txt", ".xlsx", ".xls", ".pptx")


def run_gws(args, timeout=60):
    cmd = [str(GWS_CMD), *args] if GWS_CMD.exists() else ["gws", *args]
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)


def gws_json(args, timeout=60):
    proc = run_gws(args, timeout=timeout)
    if proc.returncode != 0:
        return None, {
            "ok": False,
            "error": scrub_error((proc.stderr or proc.stdout or "").strip()),
            "authRequired": "invalid_grant" in (proc.stderr or proc.stdout or ""),
        }
    try:
        return json.loads(proc.stdout), {"ok": True}
    except Exception as exc:
        return None, {"ok": False, "error": f"Resposta gws não era JSON: {exc}", "authRequired": False}


def scrub_error(text):
    text = re.sub(r"code=4/[^&\s]+", "code=***", text or "")
    text = re.sub(r"ya29\.[A-Za-z0-9._-]+", "***", text)
    return text[:700]


def norm(text):
    text = unicodedata.normalize("NFKD", text or "")
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return text.lower()


def safe_name(text, fallback):
    text = re.sub(r'[<>:"/\\|?*\x00-\x1f]', " ", text or fallback)
    text = re.sub(r"\s+", " ", text).strip(" .")
    return (text[:140] or fallback).strip()


def unique_path(folder, filename):
    path = folder / filename
    if not path.exists():
        return path
    stem, suffix = path.stem, path.suffix
    for idx in range(2, 300):
        candidate = folder / f"{stem} ({idx}){suffix}"
        if not candidate.exists():
            return candidate
    return folder / f"{stem} ({datetime.now().strftime('%H%M%S')}){suffix}"


def read_json(path, fallback):
    if not path.exists():
        return fallback
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path, data):
    atomic_write_json(path, data)


def list_sent_ids():
    ids = []
    page_token = None
    for _ in range(MAX_PAGES):
        params = {"userId": "me", "q": SENT_QUERY, "maxResults": PAGE_SIZE}
        if page_token:
            params["pageToken"] = page_token
        data, status = gws_json(
            ["gmail", "users", "messages", "list", "--params", json.dumps(params, ensure_ascii=False)],
            timeout=60,
        )
        if not status["ok"]:
            return ids, status
        ids.extend([m["id"] for m in data.get("messages", []) if m.get("id")])
        page_token = data.get("nextPageToken")
        if not page_token:
            break
    return ids, {"ok": True}


def get_message(message_id):
    return gws_json(
        [
            "gmail",
            "users",
            "messages",
            "get",
            "--params",
            json.dumps({"userId": "me", "id": message_id, "format": "full"}, ensure_ascii=False),
        ],
        timeout=60,
    )


def get_attachment(message_id, attachment_id):
    return gws_json(
        [
            "gmail",
            "users",
            "messages",
            "attachments",
            "get",
            "--params",
            json.dumps({"userId": "me", "messageId": message_id, "id": attachment_id}, ensure_ascii=False),
        ],
        timeout=60,
    )


def header(message, name):
    for item in message.get("payload", {}).get("headers", []) or []:
        if item.get("name", "").lower() == name.lower():
            return item.get("value", "")
    return ""


def parse_date(message):
    raw = header(message, "Date")
    try:
        return email.utils.parsedate_to_datetime(raw).astimezone().isoformat()
    except Exception:
        internal = message.get("internalDate")
        if internal:
            return datetime.fromtimestamp(int(internal) / 1000, timezone.utc).astimezone().isoformat()
    return ""


def walk_parts(payload):
    if not payload:
        return
    yield payload
    for part in payload.get("parts") or []:
        yield from walk_parts(part)


def decode_body_data(data):
    if not data:
        return b""
    return base64.urlsafe_b64decode(data + "=" * (-len(data) % 4))


def body_text(message):
    chunks = []
    for part in walk_parts(message.get("payload", {})):
        if part.get("mimeType", "").startswith("text/plain"):
            raw = (part.get("body") or {}).get("data")
            if raw:
                try:
                    chunks.append(decode_body_data(raw).decode("utf-8", errors="replace"))
                except Exception:
                    pass
    return "\n".join(chunks)


def attachment_parts(message):
    for part in walk_parts(message.get("payload", {})):
        filename = part.get("filename") or ""
        if not filename:
            continue
        body = part.get("body") or {}
        if filename.lower().endswith(DOC_EXTS):
            yield {
                "filename": safe_name(filename, "documento"),
                "attachmentId": body.get("attachmentId"),
                "inlineData": body.get("data"),
                "mimeType": part.get("mimeType", ""),
                "size": body.get("size"),
            }


def is_relevant_delivery(message, attachments):
    recipients = " ".join([header(message, "To"), header(message, "Cc"), header(message, "Bcc")])
    subject = header(message, "Subject")
    text = body_text(message)
    nrec = norm(recipients)
    nhay = norm(" ".join([recipients, subject, text]))
    recipient_match = (
        "medinaosorio.adv.br" in nrec
        or "fabio" in nrec
        or "fabio" in nhay
        or "medina osorio" in nhay
        or "medinaosorio" in nhay
    )
    delivery_terms = [
        "segue",
        "anexo",
        "encaminho",
        "minuta",
        "memoriais",
        "parecer",
        "peticao",
        "peca",
        "contrarrazoes",
        "embargos",
        "docx",
        "pdf",
    ]
    delivery_match = any(term in nhay for term in delivery_terms)
    return recipient_match and (bool(attachments) or delivery_match)


def download_attachments(message, delivery_folder, attachments):
    saved = []
    errors = 0
    delivery_folder.mkdir(parents=True, exist_ok=True)
    for attachment in attachments:
        canonical = delivery_folder / attachment["filename"]
        if canonical.exists():
            saved.append(str(canonical))
            continue
        target = unique_path(delivery_folder, attachment["filename"])
        try:
            if attachment.get("inlineData"):
                raw = decode_body_data(attachment["inlineData"])
            else:
                payload, status = get_attachment(message["id"], attachment["attachmentId"])
                if not status["ok"] or not payload or not payload.get("data"):
                    errors += 1
                    continue
                raw = decode_body_data(payload["data"])
            if not target.exists():
                target.write_bytes(raw)
            saved.append(str(target))
        except Exception:
            errors += 1
    return saved, errors


GENERIC_MATCH_TERMS = {
    "assunto",
    "documento",
    "documentos",
    "elaboracao",
    "material",
    "parecer",
    "peca",
    "peticao",
    "processo",
    "minuta",
    "memoriais",
    "contrarrazoes",
    "embargos",
    "solicitacao",
    "entrada",
    "contrato",
    "social",
    "interessado",
    "recurso",
    "anexo",
    "anexos",
    "audio",
    "cliente",
    "whatsapp",
}


def specific_terms(text):
    return [
        term
        for term in re.findall(r"[a-z0-9]{4,}", norm(text))
        if term not in GENERIC_MATCH_TERMS and not term.isdigit()
    ]


def match_demands(message, demands):
    """Retorna somente vínculos fortes; sem resolução conclusiva por palavras do assunto."""
    message_id = message.get("id")
    thread_id = message.get("threadId")
    subject = header(message, "Subject")
    direct = []
    for item in demands:
        if message_id in (item.get("emailsResposta") or []):
            direct.append(item.get("id"))
    if direct:
        return sorted(set(m for m in direct if m))

    matches = []
    subject_norm = norm(subject)
    for item in demands:
        item_threads = sorted(set((item.get("threadIds") or []) + (item.get("postProtocolThreadIds") or [])))
        if item.get("origem") == "email" and item_threads:
            if thread_id and thread_id in item_threads:
                matches.append(item.get("id"))
            continue
        item_text = " ".join([item.get("titulo", ""), item.get("clienteOuCaso", ""), item.get("pasta", "")])
        process_numbers = set(re.findall(r"\b\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}\b", item_text))
        if process_numbers and any(number in subject for number in process_numbers):
            matches.append(item.get("id"))
            continue
        # Termos soltos são úteis para triagem, mas não resolvem identidade.
        # O falso vínculo Jalusa/WhatsApp mostrou que dois nomes no assunto não
        # bastam para ligar uma peça a um caso.
    return sorted(set(m for m in matches if m))


def write_report(payload):
    lines = [
        "# Entregas ao Fábio / Medina Osório",
        "",
        f"Atualizado em: {payload['updatedAt']}",
        f"Consulta base: `{payload['query']}`",
        "",
        "## Resumo",
        "",
        f"- Mensagens enviadas varridas: {payload['sentScanned']}",
        f"- Entregas prováveis encontradas: {payload['deliveriesFound']}",
        f"- Anexos de documentos encontrados: {payload['attachmentsExpected']}",
        f"- Anexos baixados: {payload['attachmentsDownloaded']}",
        f"- Erros de download: {payload['attachmentErrors']}",
        "",
        "## Entregas",
        "",
    ]
    for item in payload["deliveries"]:
        lines.extend(
            [
                f"### {item['subject'] or '(sem assunto)'}",
                "",
                f"- Data: {item['date'] or 'não identificada'}",
                f"- Gmail ID: `{item['messageId']}`",
                f"- Para/Cc: {item['recipients'] or 'não identificado'}",
                f"- Demandas relacionadas: {', '.join(item['relatedDemandIds']) if item['relatedDemandIds'] else 'não vinculada automaticamente'}",
                f"- Pasta local da entrega: `{item['folder']}`",
                f"- Anexos: {len(item['attachments'])}",
            ]
        )
        for attachment in item["attachments"]:
            lines.append(f"  - `{attachment['filename']}`")
        lines.append("")
    OUT_MD.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main():
    data = read_json(DATA_PATH, {"demandas": []})
    sent_ids, status = list_sent_ids()
    if not status["ok"]:
        payload = {
            "ok": False,
            "updatedAt": datetime.now(timezone.utc).astimezone().isoformat(),
            "query": SENT_QUERY,
            "error": status.get("error"),
            "authRequired": status.get("authRequired", False),
            "sentScanned": 0,
            "deliveriesFound": 0,
            "attachmentsExpected": 0,
            "attachmentsDownloaded": 0,
            "attachmentErrors": 0,
            "deliveries": [],
        }
        write_json(OUT_JSON, payload)
        print(json.dumps(payload, ensure_ascii=False))
        return 0

    deliveries = []
    attachment_errors = 0
    attachments_downloaded = 0
    attachments_expected = 0
    for mid in sent_ids:
        message, msg_status = get_message(mid)
        if not msg_status["ok"] or not message:
            continue
        attachments = list(attachment_parts(message))
        if not is_relevant_delivery(message, attachments):
            continue
        subject = header(message, "Subject")
        date = parse_date(message)
        folder_key = safe_name(f"{date[:10]} {subject} {mid[:8]}", f"entrega {mid[:8]}")
        folder = ARCHIVE / folder_key
        saved, errors = download_attachments(message, folder, attachments)
        attachment_errors += errors
        attachments_downloaded += len(saved)
        attachments_expected += len(attachments)
        deliveries.append(
            {
                "messageId": mid,
                "threadId": message.get("threadId"),
                "date": date,
                "subject": subject,
                "recipients": "; ".join(
                    [v for v in [header(message, "To"), header(message, "Cc"), header(message, "Bcc")] if v]
                ),
                "folder": str(folder),
                "attachments": [
                    {
                        "filename": att["filename"],
                        "mimeType": att.get("mimeType", ""),
                        "size": att.get("size"),
                    }
                    for att in attachments
                ],
                "savedFiles": saved,
                "relatedDemandIds": match_demands(message, data.get("demandas", [])),
            }
        )

    deliveries.sort(key=lambda item: item.get("date") or "", reverse=True)
    payload = {
        "ok": True,
        "updatedAt": datetime.now(timezone.utc).astimezone().isoformat(),
        "query": SENT_QUERY,
        "sentScanned": len(sent_ids),
        "deliveriesFound": len(deliveries),
        "attachmentsExpected": attachments_expected,
        "attachmentsDownloaded": attachments_downloaded,
        "attachmentErrors": attachment_errors,
        "archiveFolder": str(ARCHIVE),
        "report": str(OUT_MD),
        "deliveries": deliveries,
    }
    write_json(OUT_JSON, payload)
    write_report(payload)
    print(json.dumps(payload, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
