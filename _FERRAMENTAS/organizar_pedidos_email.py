import base64
import csv
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from html import unescape
from pathlib import Path


ROOT = Path(r"C:\Users\IgorPC\.claude\projects\Escritório fabio osório\fabricas de melhoria de petições")
GMAIL_CREDENTIALS = Path(r"C:\Users\IgorPC\.gmail-mcp\credentials.json")
GMAIL_OAUTH_KEYS = Path(r"C:\Users\IgorPC\.gmail-mcp\gcp-oauth.keys.json")

CASES = [
    {
        "name": "Assunto Laudo Pericial Contábil – Atualização de Valores – Proc. 0003453-28.1997.4.01.3400",
        "messages": ["19f1f9467513bbae"],
        "note": "Pedido de laudo pericial contábil; documentos enviados por WeTransfer e já presentes na pasta.",
    },
    {
        "name": "Cafelana",
        "messages": ["19f1f9d3cc69c8c8"],
        "note": "Pedido de contrarrazões de EDCL em ação rescisória.",
    },
    {
        "name": r"Cafelana\contrarrazões ao AgInt no AREsp nº 2.698.443D",
        "messages": ["19f2f0876e358eab"],
        "note": "Pedido de contrarrazões/impugnação ao AgInt no AREsp 2.698.443/DF.",
    },
    {
        "name": "Memoriais Cautelar Fiscal",
        "messages": ["19f24b1ec0eb7b34", "19f28a9fa7d73ab3", "19f398df0abc8eed"],
        "note": "Pedido de memoriais no processo 5002486-81.2012.4.04.7216 e retorno com versão revisada.",
    },
    {
        "name": "Minuta de Embargos de Declaração — José Eduardo Siqueira Campos",
        "messages": ["19f1f92c333b1e4e", "19f39840e51b6feb"],
        "note": "Pedido de melhoria de embargos de declaração e retorno com versão revisada para protocolo.",
    },
    {
        "name": "CORSAN AGERST - Proposta de Serviços Jurídicos",
        "messages": ["19f3dc9ff92081cd"],
        "note": "Novo pedido de parecer, análise de risco, proposta e plano estratégico AGERST/CORSAN/AEGEA.",
    },
    {
        "name": "Memoriais Apelação Patrícia e Fábio - Proc. 0014560-09.2014.8.19.0209",
        "messages": ["19f3c68ee6d8fef2"],
        "note": "Novo pedido de memoriais para julgamento da apelação no TJRJ.",
    },
    {
        "name": "Memoriais AgInt AREsp 2578181 SC - LIBRA SUL",
        "messages": ["19f3c9350d875062"],
        "note": "Novo pedido de memoriais para AgInt no AREsp 2.578.181/SC.",
    },
    {
        "name": "Embargos AgInt AREsp 1883361 RS - Jorge Haroldo",
        "messages": ["19f3c8200768b56e"],
        "note": "Novo pedido de embargos de declaração no AgInt no AREsp 1.883.361/RS.",
    },
    {
        "name": "Jalusa Prestes Abaide - Proc. 5000447-02.2011.4.04.7102",
        "messages": [
            "19f38b672e687d72",
            "19f38b85d3c84448",
            "19f38b8ee9d90b53",
            "19f38b9950abe771",
            "19f38d26eb0dcbd6",
            "19f38d33a559cb7a",
            "19f38d8383a0060e",
            "19f38ea3e8306b13",
        ],
        "note": "Novo pedido urgente de análise e eventual melhoria de petição, com etapas documentais da cliente Jalusa.",
    },
]

URL_RE = re.compile(r"https?://[^\s<>\]\)\"']+")


def b64url_decode(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(value + padding)


def sanitize_filename(name: str, max_len: int = 140) -> str:
    name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', " ", name)
    name = re.sub(r"\s+", " ", name).strip().rstrip(".")
    return (name[:max_len].rstrip() or "sem_nome")


def strip_html(html: str) -> str:
    html = re.sub(r"(?is)<(script|style).*?>.*?</\1>", " ", html)
    html = re.sub(r"(?i)<br\s*/?>", "\n", html)
    html = re.sub(r"(?i)</p\s*>", "\n\n", html)
    html = re.sub(r"(?is)<.*?>", " ", html)
    html = unescape(html)
    return re.sub(r"[ \t\r\f\v]+", " ", html).strip()


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def save_json(path: Path, data: dict) -> None:
    with path.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)


def http_json(url: str, method: str = "GET", token: str | None = None, data: dict | None = None) -> dict:
    body = None
    headers = {}
    if data is not None:
        body = urllib.parse.urlencode(data).encode("utf-8")
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, data=body, method=method, headers=headers)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def get_access_token() -> str:
    creds = load_json(GMAIL_CREDENTIALS)
    now_ms = int(time.time() * 1000)
    if creds.get("access_token") and int(creds.get("expiry_date", 0)) > now_ms + 120_000:
        return creds["access_token"]

    keys = load_json(GMAIL_OAUTH_KEYS)["installed"]
    token_resp = http_json(
        keys["token_uri"],
        method="POST",
        data={
            "client_id": keys["client_id"],
            "client_secret": keys["client_secret"],
            "refresh_token": creds["refresh_token"],
            "grant_type": "refresh_token",
        },
    )
    creds["access_token"] = token_resp["access_token"]
    creds["token_type"] = token_resp.get("token_type", "Bearer")
    creds["expiry_date"] = now_ms + int(token_resp.get("expires_in", 3600)) * 1000
    save_json(GMAIL_CREDENTIALS, creds)
    return creds["access_token"]


def gmail_get_message(token: str, message_id: str) -> dict:
    url = f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{message_id}?format=full"
    return http_json(url, token=token)


def gmail_get_attachment(token: str, message_id: str, attachment_id: str) -> bytes:
    url = (
        "https://gmail.googleapis.com/gmail/v1/users/me/messages/"
        f"{message_id}/attachments/{urllib.parse.quote(attachment_id)}"
    )
    payload = http_json(url, token=token)
    return b64url_decode(payload["data"])


def header_map(part: dict) -> dict:
    return {h.get("name", "").lower(): h.get("value", "") for h in part.get("headers", [])}


def walk_parts(part: dict):
    yield part
    for child in part.get("parts", []) or []:
        yield from walk_parts(child)


def extract_text(payload: dict) -> str:
    plain_chunks = []
    html_chunks = []
    for part in walk_parts(payload):
        body = part.get("body", {})
        data = body.get("data")
        if not data:
            continue
        mime = part.get("mimeType", "")
        try:
            text = b64url_decode(data).decode("utf-8", errors="replace")
        except Exception:
            continue
        if mime == "text/plain":
            plain_chunks.append(text)
        elif mime == "text/html":
            html_chunks.append(strip_html(text))
    text = "\n\n".join(chunk.strip() for chunk in plain_chunks if chunk.strip())
    if not text and html_chunks:
        text = "\n\n".join(chunk for chunk in html_chunks if chunk)
    return text.strip()


def extract_urls(text: str) -> list[str]:
    out = []
    seen = set()
    for raw in URL_RE.findall(text):
        url = raw.rstrip(".,;)")
        if url not in seen:
            seen.add(url)
            out.append(url)
    return out


def subject_from_message(msg: dict) -> str:
    headers = header_map(msg.get("payload", {}))
    return headers.get("subject", "(sem assunto)")


def metadata_block(msg: dict) -> str:
    headers = header_map(msg.get("payload", {}))
    ts = int(msg.get("internalDate", "0")) / 1000
    date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))
    return (
        f"ID Gmail: {msg.get('id')}\n"
        f"Thread: {msg.get('threadId')}\n"
        f"Data local aproximada: {date}\n"
        f"De: {headers.get('from', '')}\n"
        f"Para: {headers.get('to', '')}\n"
        f"Cc: {headers.get('cc', '')}\n"
        f"Assunto: {headers.get('subject', '')}\n"
    )


def should_skip_inline(part: dict) -> bool:
    headers = header_map(part)
    disposition = headers.get("content-disposition", "").lower()
    filename = (part.get("filename") or "").lower()
    if "attachment" in disposition:
        return False
    if "inline" in disposition and filename in {"image.png", "outlook-nvuzidmf.png"}:
        return True
    return False


def download_gmail_attachments(token: str, msg: dict, target_dir: Path) -> list[dict]:
    saved = []
    for part in walk_parts(msg.get("payload", {})):
        filename = part.get("filename") or ""
        attachment_id = part.get("body", {}).get("attachmentId")
        if not filename or not attachment_id or should_skip_inline(part):
            continue
        safe_name = sanitize_filename(filename)
        output = target_dir / safe_name
        if output.exists():
            stem, suffix = output.stem, output.suffix
            counter = 2
            while output.exists():
                output = target_dir / f"{stem} ({counter}){suffix}"
                counter += 1
        data = gmail_get_attachment(token, msg["id"], attachment_id)
        output.write_bytes(data)
        saved.append(
            {
                "message_id": msg["id"],
                "filename": filename,
                "saved_as": str(output),
                "bytes": len(data),
                "mime": part.get("mimeType", ""),
            }
        )
    return saved


def drive_file_id(url: str) -> str | None:
    patterns = [
        r"drive\.google\.com/file/d/([^/]+)",
        r"docs\.google\.com/(?:document|spreadsheets|presentation)/d/([^/]+)",
        r"[?&]id=([^&]+)",
    ]
    for pat in patterns:
        m = re.search(pat, url)
        if m:
            return m.group(1)
    return None


def download_public_drive_file(url: str, target_dir: Path, preferred_name: str) -> tuple[bool, str]:
    file_id = drive_file_id(url)
    if not file_id:
        return False, "sem_file_id"
    session = urllib.request.build_opener(urllib.request.HTTPCookieProcessor())
    download_url = f"https://drive.google.com/uc?export=download&id={urllib.parse.quote(file_id)}"
    try:
        resp = session.open(download_url, timeout=60)
        data = resp.read()
        ctype = resp.headers.get("Content-Type", "")
        if b"download_warning" in data[:5000] or "text/html" in ctype.lower():
            text = data.decode("utf-8", errors="ignore")
            token_match = re.search(r"confirm=([0-9A-Za-z_]+)", text)
            uuid_match = re.search(r"uuid=([0-9A-Za-z_-]+)", text)
            if token_match:
                params = {"export": "download", "id": file_id, "confirm": token_match.group(1)}
                if uuid_match:
                    params["uuid"] = uuid_match.group(1)
                resp = session.open(f"https://drive.google.com/uc?{urllib.parse.urlencode(params)}", timeout=60)
                data = resp.read()
                ctype = resp.headers.get("Content-Type", "")
        if "text/html" in ctype.lower() and data[:200].lower().find(b"<html") >= 0:
            return False, "permissao_ou_login_necessario"
        suffix = ".pdf"
        if "zip" in ctype:
            suffix = ".zip"
        elif "word" in ctype or "officedocument" in ctype:
            suffix = ".docx"
        safe_name = sanitize_filename(preferred_name)
        if "." not in Path(safe_name).name:
            safe_name += suffix
        output = target_dir / safe_name
        if output.exists():
            return True, str(output)
        output.write_bytes(data)
        return True, str(output)
    except urllib.error.HTTPError as exc:
        return False, f"HTTP {exc.code}"
    except Exception as exc:
        return False, f"{type(exc).__name__}: {exc}"


def markdown_link_label(text: str, url: str) -> str:
    escaped = re.escape(url)
    m = re.search(r"\[([^\]]{1,180})\]\(" + escaped + r"\)", text)
    if m:
        return m.group(1)
    return Path(urllib.parse.urlparse(url).path).name or "documento_drive"


def write_case_files(token: str, case: dict) -> dict:
    case_dir = ROOT / case["name"]
    commands_dir = case_dir / "Comandos e emails"
    attachments_dir = case_dir / "Anexos do email"
    drive_dir = case_dir / "Documentos de links do Drive"
    case_dir.mkdir(parents=True, exist_ok=True)
    commands_dir.mkdir(exist_ok=True)
    attachments_dir.mkdir(exist_ok=True)
    drive_dir.mkdir(exist_ok=True)

    consolidated = [
        f"CASO/PASTA: {case['name']}",
        f"OBSERVAÇÃO: {case.get('note', '')}",
        "",
        "Este arquivo foi gerado para preservar os comandos recebidos por e-mail e iniciar o trabalho da peça.",
        "",
    ]
    all_urls = []
    attachment_rows = []
    drive_rows = []

    for message_id in case["messages"]:
        msg = gmail_get_message(token, message_id)
        subject = subject_from_message(msg)
        text = extract_text(msg.get("payload", {}))
        meta = metadata_block(msg)
        ts = int(msg.get("internalDate", "0")) / 1000
        date_slug = time.strftime("%Y-%m-%d_%H%M", time.localtime(ts))
        subject_slug = sanitize_filename(subject, 80)
        msg_dir = attachments_dir / f"{date_slug} - {subject_slug} - {message_id}"
        msg_dir.mkdir(parents=True, exist_ok=True)

        msg_file = commands_dir / f"{date_slug} - {subject_slug} - {message_id}.txt"
        msg_file.write_text(meta + "\n\n" + text + "\n", encoding="utf-8")

        consolidated.extend(
            [
                "=" * 90,
                meta.rstrip(),
                "-" * 90,
                text,
                "",
            ]
        )

        urls = extract_urls(text)
        new_urls = [(message_id, subject, url, markdown_link_label(text, url)) for url in urls]
        all_urls.extend(new_urls)

        saved = download_gmail_attachments(token, msg, msg_dir)
        attachment_rows.extend(saved)

        for _, _, url, label in new_urls:
            if "drive.google.com" in url or "docs.google.com" in url:
                ok, result = download_public_drive_file(url, drive_dir, label)
                drive_rows.append(
                    {
                        "message_id": message_id,
                        "subject": subject,
                        "label": label,
                        "url": url,
                        "baixado": "sim" if ok else "não",
                        "resultado": result,
                    }
                )

    (case_dir / "COMANDO_DO_EMAIL.txt").write_text("\n".join(consolidated).strip() + "\n", encoding="utf-8")

    with (case_dir / "LINKS_DO_EMAIL.txt").open("w", encoding="utf-8") as fh:
        for message_id, subject, url, label in all_urls:
            fh.write(f"[{message_id}] {subject}\n{label}: {url}\n\n")

    if attachment_rows:
        with (case_dir / "ANEXOS_GMAIL_BAIXADOS.csv").open("w", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=["message_id", "filename", "saved_as", "bytes", "mime"])
            writer.writeheader()
            writer.writerows(attachment_rows)

    if drive_rows:
        with (case_dir / "LINKS_DRIVE_TENTATIVA_DOWNLOAD.csv").open("w", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(
                fh,
                fieldnames=["message_id", "subject", "label", "url", "baixado", "resultado"],
            )
            writer.writeheader()
            writer.writerows(drive_rows)

    return {
        "pasta": str(case_dir),
        "mensagens": len(case["messages"]),
        "anexos_gmail_baixados": len(attachment_rows),
        "links": len(all_urls),
        "links_drive_baixados": sum(1 for row in drive_rows if row["baixado"] == "sim"),
        "links_drive_pendentes": sum(1 for row in drive_rows if row["baixado"] != "sim"),
    }


def main() -> None:
    token = get_access_token()
    results = []
    for case in CASES:
        print(f"Organizando: {case['name']}")
        results.append(write_case_files(token, case))

    report = ROOT / "RELATORIO_ORGANIZACAO_EMAILS_MEDINA_OSORIO.md"
    lines = [
        "# Relatório de organização dos pedidos por e-mail",
        "",
        f"Gerado em: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "| Pasta | Mensagens | Anexos Gmail baixados | Links | Drive baixados | Drive pendentes |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in results:
        lines.append(
            "| {pasta} | {mensagens} | {anexos_gmail_baixados} | {links} | {links_drive_baixados} | {links_drive_pendentes} |".format(
                **row
            )
        )
    lines.extend(
        [
            "",
            "Observações:",
            "- Anexos diretos do Gmail foram baixados para subpastas `Anexos do email`.",
            "- Corpos completos dos e-mails foram salvos em `COMANDO_DO_EMAIL.txt` e também separados em `Comandos e emails`.",
            "- Links de Drive foram tentados por download público. Quando o link exige login/permissão, o arquivo fica registrado em `LINKS_DRIVE_TENTATIVA_DOWNLOAD.csv`.",
            "- Links externos como WeTransfer, TransferNow, Acrobat e YouTube foram preservados em `LINKS_DO_EMAIL.txt`.",
        ]
    )
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Relatório: {report}")


if __name__ == "__main__":
    main()
