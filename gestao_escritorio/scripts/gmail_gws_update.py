import argparse
import base64
from email.utils import parsedate_to_datetime
import json
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from office_io import atomic_write_json


GWS_CMD = Path.home() / "AppData" / "Roaming" / "npm" / "gws.cmd"
GWS_PS1 = Path.home() / "AppData" / "Roaming" / "npm" / "gws.ps1"


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def run_gws(args, timeout=45):
    if GWS_CMD.exists():
        cmd = [str(GWS_CMD), *args]
    elif GWS_PS1.exists():
        cmd = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(GWS_PS1), *args]
    else:
        cmd = ["gws", *args]
    proc = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
    )
    return proc


def gws_json(args, timeout=45):
    try:
        proc = run_gws(args, timeout=timeout)
    except subprocess.TimeoutExpired:
        return None, {"ok": False, "error": f"Gmail excedeu {timeout}s nesta etapa.", "authRequired": False}
    except OSError as exc:
        return None, {"ok": False, "error": scrub_error(exc), "authRequired": False}
    if proc.returncode != 0:
        msg = (proc.stderr or proc.stdout or "").strip()
        return None, {
            "ok": False,
            "error": scrub_error(msg),
            "authRequired": "invalid_grant" in msg or "Authentication failed" in msg,
        }
    try:
        return json.loads(proc.stdout), {"ok": True}
    except Exception as exc:
        return None, {"ok": False, "error": f"Resposta gws não era JSON: {exc}", "authRequired": False}


def scrub_error(text):
    # Keep operational diagnosis, never echo long payloads or possible tokens.
    text = re.sub(r"ya29\.[A-Za-z0-9._-]+", "***", text or "")
    text = re.sub(r"refresh_token[^\s,}]+", "refresh_token=***", text)
    return text[:500]


def norm(s):
    import unicodedata

    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def safe_folder_name(s, fallback):
    s = s or fallback
    s = re.sub(r'[<>:"/\\|?*\x00-\x1f]', " ", s)
    s = re.sub(r"\s+", " ", s).strip(" .")
    return (s[:110] or fallback).strip()


def get_header(message, name):
    for h in message.get("payload", {}).get("headers", []) or []:
        if h.get("name", "").lower() == name.lower():
            return h.get("value", "")
    return ""


def decode_part(part):
    data = (part.get("body") or {}).get("data")
    if not data:
        return ""
    try:
        return base64.urlsafe_b64decode(data + "=" * (-len(data) % 4)).decode("utf-8", errors="replace")
    except Exception:
        return ""


def body_from_payload(payload):
    if not payload:
        return ""
    mime = payload.get("mimeType", "")
    if mime.startswith("text/plain"):
        return decode_part(payload)
    parts = payload.get("parts") or []
    for part in parts:
        if part.get("mimeType", "").startswith("text/plain"):
            return decode_part(part)
    for part in parts:
        text = body_from_payload(part)
        if text:
            return text
    return ""


def list_ids(query, max_results=500):
    ids = []
    page_token = None
    estimate = None
    while len(ids) < max_results:
        params = {"userId": "me", "q": query, "maxResults": min(100, max_results - len(ids))}
        if page_token:
            params["pageToken"] = page_token
        data, status = gws_json(
            [
                "gmail",
                "users",
                "messages",
                "list",
                "--params",
                json.dumps(params, ensure_ascii=False),
            ]
        )
        if not status["ok"]:
            return [], status
        estimate = data.get("resultSizeEstimate", estimate)
        ids.extend(m["id"] for m in data.get("messages", []) if m.get("id"))
        page_token = data.get("nextPageToken")
        if not page_token:
            break
    return ids, {"ok": True, "resultSizeEstimate": estimate, "pagesComplete": not bool(page_token)}


def get_message(message_id, fmt="full"):
    data, status = gws_json(
        [
            "gmail",
            "users",
            "messages",
            "get",
            "--params",
            json.dumps({"userId": "me", "id": message_id, "format": fmt}, ensure_ascii=False),
        ],
        timeout=60,
    )
    return data, status


def extract_deadline(text):
    today = datetime.now().date()
    candidates = []
    pattern = re.compile(r"\b(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})\b")
    source = text or ""
    for match in pattern.finditer(source):
        d, m, y = match.groups()
        if len(y) == 2:
            y = "20" + y
        try:
            dt = datetime(int(y), int(m), int(d)).date()
        except ValueError:
            continue
        before = norm(source[max(0, match.start() - 110) : match.start()])
        immediate = norm(source[max(0, match.start() - 42) : match.start()])
        context = before + " " + norm(source[match.end() : min(len(source), match.end() + 24)])
        score = 0
        if re.search(r"prazo\s+(fatal|interno|final)", before):
            score += 7
        if re.search(r"(minuta|entregar|encaminhar|enviar|protocolar|protocolo).{0,45}\b(ate|para|em)\b", before):
            score += 5
        if re.search(r"\b(prazo|vencimento|limite)\b", before):
            score += 4
        if re.search(r"\b(ate|impreterivelmente|no maximo)\b", immediate):
            score += 2
        if re.search(r"\b(data do email|recebido em)\b", immediate):
            score -= 20
        if re.search(r"\b(julgamento|sessao|publicacao|intimacao)\b", immediate):
            score -= 12
        if score >= 4 and dt >= today - timedelta(days=30):
            candidates.append((score, dt))
    if not candidates:
        return None
    candidates.sort(key=lambda value: (-value[0], value[1]))
    return candidates[0][1].isoformat()


def received_at(header_value):
    try:
        parsed = parsedate_to_datetime(header_value)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone().isoformat(timespec="seconds")
    except (TypeError, ValueError, OverflowError):
        return ""


def already_known_ids(data):
    ids = set()
    for item in data.get("demandas", []):
        ids.update(item.get("emailsRecebidos") or [])
        ids.update(item.get("emailsResposta") or [])
    return ids


def thread_map(data):
    mapping = {}
    for item in data.get("demandas", []):
        if item.get("origem") != "email":
            continue
        for thread_id in item.get("threadIds") or []:
            mapping.setdefault(thread_id, item)
    return mapping


def has_delivery_attachment(message):
    for part in walk_parts(message.get("payload", {})):
        filename = part.get("filename") or ""
        if filename.lower().endswith((".docx", ".pdf", ".doc", ".odt")):
            return filename
    return ""


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
    "relatorio",
    "resposta",
    "retorno",
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


def message_matches_item(msg, item, allow_existing=True):
    msg_id = msg.get("id")
    if allow_existing and msg_id in (item.get("emailsResposta") or []):
        return True
    msg_thread = msg.get("threadId")
    item_threads = sorted(set((item.get("threadIds") or []) + (item.get("postProtocolThreadIds") or [])))
    if item.get("origem") == "email" and item_threads:
        return bool(msg_thread and msg_thread in item_threads)
    subject_norm = norm(get_header(msg, "Subject"))
    item_text = " ".join([item.get("titulo", ""), item.get("clienteOuCaso", ""), item.get("pasta", "")])
    process_numbers = set(re.findall(r"\b\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}\b", item_text))
    if process_numbers and any(number in get_header(msg, "Subject") for number in process_numbers):
        return True
    # Sem CNJ ou vínculo de thread, o assunto apenas gera triagem. Nunca
    # conclui a identidade, evitando associação transversal entre casos.
    return False


def walk_parts(payload):
    if not payload:
        return
    yield payload
    for part in payload.get("parts") or []:
        yield from walk_parts(part)


def attachment_parts(message):
    for part in walk_parts(message.get("payload", {})):
        filename = part.get("filename") or ""
        body = part.get("body") or {}
        attachment_id = body.get("attachmentId")
        if filename and attachment_id:
            yield {
                "filename": safe_file_name(filename, "anexo"),
                "attachmentId": attachment_id,
                "mimeType": part.get("mimeType", ""),
            }


def safe_file_name(name, fallback):
    name = name or fallback
    name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', " ", name)
    name = re.sub(r"\s+", " ", name).strip(" .")
    return (name[:180] or fallback).strip()


def unique_path(folder, filename):
    path = folder / filename
    if not path.exists():
        return path
    stem = path.stem
    suffix = path.suffix
    for idx in range(2, 200):
        candidate = folder / f"{stem} ({idx}){suffix}"
        if not candidate.exists():
            return candidate
    return folder / f"{stem} ({datetime.now().strftime('%H%M%S')}){suffix}"


def get_attachment(message_id, attachment_id):
    data, status = gws_json(
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
    return data, status


def download_message_attachments(workspace, item, message):
    if not item.get("pasta"):
        return {"expected": 0, "downloaded": 0, "errors": 0}
    parts = list(attachment_parts(message))
    if not parts:
        ensure_attachment_state(item, 0, 0)
        return {"expected": 0, "downloaded": 0, "errors": 0}
    folder = workspace / item["pasta"]
    attach_dir = folder / "Anexos do email"
    attach_dir.mkdir(parents=True, exist_ok=True)
    downloaded = 0
    errors = 0
    for part in parts:
        existing = list(attach_dir.glob(part["filename"]))
        if existing:
            downloaded += 1
            continue
        payload, status = get_attachment(message.get("id"), part["attachmentId"])
        if not status["ok"] or not payload or not payload.get("data"):
            errors += 1
            continue
        try:
            raw = base64.urlsafe_b64decode(payload["data"] + "=" * (-len(payload["data"]) % 4))
            unique_path(attach_dir, part["filename"]).write_bytes(raw)
            downloaded += 1
        except Exception:
            errors += 1
    ensure_attachment_state(item, len(parts), downloaded)
    return {"expected": len(parts), "downloaded": downloaded, "errors": errors}


def ensure_attachment_state(item, expected, downloaded):
    anexos = item.setdefault("anexos", {})
    anexos["diretosEsperados"] = expected
    anexos["diretosBaixados"] = downloaded
    if expected and downloaded >= expected:
        anexos["observacao"] = f"{downloaded}/{expected} anexos diretos do Gmail baixados."
    elif expected:
        anexos["observacao"] = f"{downloaded}/{expected} anexos diretos do Gmail baixados; revisar falhas ou links externos."
    else:
        anexos.setdefault("observacao", "Sem anexos diretos detectados no Gmail.")


def mark_sent_responses(data, sent_messages):
    changed = 0
    for msg in sent_messages:
        subject = get_header(msg, "Subject")
        body = body_from_payload(msg.get("payload", {}))
        attachment = has_delivery_attachment(msg)
        delivery_signal = re.search(
            r"\b(seguem?|encaminho|envio|anex[oa]s?|segue\s+em\s+anexo)\b.{0,140}\b(peti[cç][aã]o|pe[cç]a|memoriais|minuta|parecer|documento|vers[aã]o)\b",
            body,
            re.I | re.S,
        )
        if not attachment and not delivery_signal:
            continue
        for item in data.get("demandas", []):
            if item.get("origem") != "email":
                continue
            if item.get("respondidoComConteudo"):
                continue
            if message_matches_item(msg, item):
                item.setdefault("emailsResposta", [])
                if msg.get("id") not in item["emailsResposta"]:
                    item["emailsResposta"].append(msg.get("id"))
                item["respondidoComConteudo"] = True
                item["status"] = "cumprida"
                item["evidenciaResposta"] = f"E-mail enviado {msg.get('id')} com conteúdo de entrega" + (f" e anexo {attachment}." if attachment else ".")
                item["evidenciaTipo"] = "email"
                changed += 1
    return changed


def repair_false_response_matches(data, sent_messages):
    sent_by_id = {msg.get("id"): msg for msg in sent_messages}
    repaired = 0
    for item in data.get("demandas", []):
        original = list(item.get("emailsResposta") or [])
        if not original:
            continue
        kept = []
        removed = []
        for mid in original:
            msg = sent_by_id.get(mid)
            if msg is None or message_matches_item(msg, item, allow_existing=False):
                kept.append(mid)
            else:
                removed.append(mid)
        if removed:
            item["emailsResposta"] = kept
            repaired += len(removed)
            if not kept:
                item["respondidoComConteudo"] = False
                item["status"] = "aberta"
                item["evidenciaResposta"] = ""
                item.pop("evidenciaTipo", None)
    return repaired


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument(
        "--since-days",
        type=int,
        default=0,
        help="Restringe a atualização cotidiana aos últimos N dias; zero mantém a auditoria histórica.",
    )
    ap.add_argument(
        "--sent-cache",
        help="Arquivo temporário opcional para reutilizar nesta execução as mensagens enviadas já lidas.",
    )
    args = ap.parse_args()

    root = Path(args.root)
    workspace = root.parent
    data_path = root / "data" / "demandas.json"
    config_path = root / "config.json"
    data = read_json(data_path)
    config = read_json(config_path)
    inbound_query = config["gmail"]["inboundQuery"]
    sent_query = config["gmail"]["sentQuery"]
    if args.since_days > 0:
        cutoff = (datetime.now().astimezone() - timedelta(days=args.since_days)).strftime("%Y/%m/%d")
        inbound_query = re.sub(r"\bafter:\d{4}/\d{2}/\d{2}\b", f"after:{cutoff}", inbound_query)
        sent_query = re.sub(r"\bafter:\d{4}/\d{2}/\d{2}\b", f"after:{cutoff}", sent_query)

    status = {
        "ok": False,
        "updatedAt": datetime.now(timezone.utc).astimezone().isoformat(),
        "authRequired": False,
        "newInbound": 0,
        "sentScanned": 0,
        "responsesMarked": 0,
        "message": "",
    }

    inbound_ids, inbound_status = list_ids(inbound_query)
    if not inbound_status["ok"]:
        status.update(inbound_status)
        status["message"] = "Gmail local indisponível; rode gws auth login para habilitar o botão completo."
        print(json.dumps(status, ensure_ascii=False))
        return 0

    sent_ids, sent_status = list_ids(sent_query)
    if not sent_status["ok"]:
        status.update(sent_status)
        status["message"] = "Gmail local conseguiu recebidos, mas falhou em enviados."
        print(json.dumps(status, ensure_ascii=False))
        return 0

    known = already_known_ids(data)
    new_ids = [mid for mid in inbound_ids if mid not in known]
    by_thread = thread_map(data)
    inbound_messages = {}
    created = 0
    attachment_downloaded = 0
    attachment_expected = 0
    attachment_errors = 0
    for mid in inbound_ids:
        msg, msg_status = get_message(mid, "full")
        if not msg_status["ok"] or not msg:
            continue
        inbound_messages[mid] = msg
        if mid not in new_ids:
            continue
        subject = get_header(msg, "Subject") or f"Demanda Gmail {mid}"
        date = get_header(msg, "Date")
        sender = get_header(msg, "From")
        body = body_from_payload(msg.get("payload", {}))
        existing_thread_item = by_thread.get(msg.get("threadId"))
        if existing_thread_item:
            existing_thread_item.setdefault("emailsRecebidos", [])
            if mid not in existing_thread_item["emailsRecebidos"]:
                existing_thread_item["emailsRecebidos"].append(mid)
            existing_thread_item.setdefault("threadIds", [])
            if msg.get("threadId") and msg.get("threadId") not in existing_thread_item["threadIds"]:
                existing_thread_item["threadIds"].append(msg.get("threadId"))
            folder = workspace / existing_thread_item.get("pasta", "")
            if folder.exists():
                complement = folder / f"EMAIL_COMPLEMENTO_{mid}.md"
                if not complement.exists():
                    complement.write_text(
                        f"# Complemento de e-mail na mesma conversa\n\n"
                        f"- Gmail ID: `{mid}`\n"
                        f"- De: {sender}\n"
                        f"- Data: {date}\n"
                        f"- Assunto: {subject}\n\n"
                        f"## Corpo\n\n{body.strip()}\n",
                        encoding="utf-8",
                    )
            continue
        deadline = extract_deadline(subject + "\n" + body)
        folder_name = safe_folder_name(subject, f"Demanda Gmail {mid}")
        folder = workspace / folder_name
        folder.mkdir(exist_ok=True)
        (folder / "COMANDO_DO_EMAIL.md").write_text(
            f"# Comando do e-mail\n\n"
            f"- Gmail ID: `{mid}`\n"
            f"- De: {sender}\n"
            f"- Data: {date}\n"
            f"- Assunto: {subject}\n\n"
            f"## Corpo do pedido\n\n{body.strip()}\n",
            encoding="utf-8",
        )
        (folder / "ANEXOS_EMAIL_RECEBIDOS_OU_PENDENTES.txt").write_text(
            "Criado automaticamente pelo painel. Conferir anexos no Gmail/Drive e baixar para `Anexos do email`.\n",
            encoding="utf-8",
        )
        new_item = {
                "id": f"email-auto-{mid}",
                "titulo": subject,
                "clienteOuCaso": subject,
                "origem": "email",
                "emailsRecebidos": [mid],
                "emailsResposta": [],
                "threadIds": [msg.get("threadId")] if msg.get("threadId") else [],
                "pasta": folder_name,
                "recebidoEm": received_at(date),
                "prazo": deadline,
                "prazoTexto": f"prazo sugerido automaticamente: {deadline}; confirmar no e-mail" if deadline else "prazo não detectado automaticamente",
                "prazoConfianca": "sugerido" if deadline else "nao_detectado",
                "resumo": (body.strip()[:500] + ("..." if len(body.strip()) > 500 else "")) or "E-mail novo detectado; ler COMANDO_DO_EMAIL.md.",
                "proximaAcao": "Conferir anexos, confirmar prazo e transformar o pedido em peça/documento.",
                "status": "aberta",
                "respondidoComConteudo": False,
                "evidenciaResposta": "",
                "urgenciaManual": "alta" if deadline else "media",
                "anexos": {
                    "diretosBaixados": 0,
                    "diretosEsperados": None,
                    "externosPendentes": True,
                    "observacao": "Criado automaticamente; anexos ainda precisam ser conferidos.",
                },
                "tags": ["gmail-auto", "a conferir"],
        }
        data["demandas"].append(new_item)
        if msg.get("threadId"):
            by_thread[msg.get("threadId")] = new_item
        created += 1

    for item in data.get("demandas", []):
        for mid in item.get("emailsRecebidos") or []:
            msg = inbound_messages.get(mid)
            if not msg:
                continue
            if msg.get("threadId"):
                item.setdefault("threadIds", [])
                if msg.get("threadId") not in item["threadIds"]:
                    item["threadIds"].append(msg.get("threadId"))
            if str(item.get("id", "")).startswith("email-auto-"):
                subject = get_header(msg, "Subject") or item.get("titulo", "")
                body = body_from_payload(msg.get("payload", {}))
                item["titulo"] = subject
                item["clienteOuCaso"] = subject
                item["recebidoEm"] = item.get("recebidoEm") or received_at(get_header(msg, "Date"))
                item["resumo"] = (body.strip()[:500] + ("..." if len(body.strip()) > 500 else "")) or item.get("resumo", "")
            att = download_message_attachments(workspace, item, msg)
            attachment_downloaded += att["downloaded"]
            attachment_expected += att["expected"]
            attachment_errors += att["errors"]

    sent_messages = []
    for mid in sent_ids:
        msg, msg_status = get_message(mid, "full")
        if msg_status["ok"] and msg:
            sent_messages.append(msg)
    if args.sent_cache:
        atomic_write_json(
            Path(args.sent_cache),
            {
                "query": sent_query,
                "createdAt": datetime.now(timezone.utc).astimezone().isoformat(),
                "messages": sent_messages,
            },
        )
    repaired = repair_false_response_matches(data, sent_messages)
    responses = mark_sent_responses(data, sent_messages)
    data["updatedAt"] = datetime.now(timezone.utc).astimezone().isoformat()
    atomic_write_json(data_path, data)
    status.update(
        {
            "ok": True,
            "authRequired": False,
            "inboundScanned": len(inbound_ids),
            "sentScanned": len(sent_ids),
            "newInbound": created,
            "responsesMarked": responses,
            "responsesRepaired": repaired,
            "attachmentsExpected": attachment_expected,
            "attachmentsDownloaded": attachment_downloaded,
            "attachmentErrors": attachment_errors,
            "message": "Gmail local atualizado com sucesso.",
            "scanMode": "incremental" if args.since_days > 0 else "historico",
            "sinceDays": args.since_days,
        }
    )
    print(json.dumps(status, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
