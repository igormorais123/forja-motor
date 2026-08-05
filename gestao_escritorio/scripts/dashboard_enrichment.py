import copy
import re
from datetime import date, datetime, timedelta
from pathlib import Path


DATE_MIN = date.today() - timedelta(days=366)
DATE_MAX = date.today() + timedelta(days=1095)


def gmail_url(identifier):
    if not identifier:
        return ""
    return f"https://mail.google.com/mail/u/0/#all/{identifier}"


def source_label(origin):
    origin = str(origin or "").strip().lower()
    if origin == "email":
        return "E-mail"
    if origin == "whatsapp_audio":
        return "Áudio WhatsApp"
    if origin == "whatsapp":
        return "WhatsApp"
    if origin == "hermes_whatsapp":
        return "Hermes/WhatsApp"
    if origin == "manual":
        return "Manual"
    return origin or "Não informada"


def _valid_date(y, m, d):
    try:
        dt = date(int(y), int(m), int(d))
    except ValueError:
        return None
    if DATE_MIN <= dt <= DATE_MAX:
        return dt
    return None


def _context(text, start, end, radius=54):
    left = max(0, start - radius)
    right = min(len(text), end + radius)
    snippet = re.sub(r"\s+", " ", text[left:right]).strip()
    return snippet[:150]


def extract_date_mentions(text, source):
    mentions = []
    seen = set()
    text = text or ""
    for match in re.finditer(r"\b(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})\b", text):
        day, month, year = match.groups()
        year = int(year)
        if year < 100:
            year += 2000
        dt = _valid_date(year, month, day)
        if not dt:
            continue
        key = (dt.isoformat(), source, _context(text, match.start(), match.end()))
        if key in seen:
            continue
        seen.add(key)
        mentions.append(
            {
                "date": dt.isoformat(),
                "source": source,
                "context": key[2],
            }
        )
    for match in re.finditer(r"\b(20\d{2})-(\d{2})-(\d{2})\b", text):
        year, month, day = match.groups()
        dt = _valid_date(year, month, day)
        if not dt:
            continue
        key = (dt.isoformat(), source, _context(text, match.start(), match.end()))
        if key in seen:
            continue
        seen.add(key)
        mentions.append(
            {
                "date": dt.isoformat(),
                "source": source,
                "context": key[2],
            }
        )
    return mentions


def command_body_for_item(workspace, item):
    folder_name = item.get("pasta")
    if not folder_name:
        return ""
    folder = Path(workspace) / folder_name
    candidates = [
        "COMANDO_DO_EMAIL.md",
        "COMANDO_DO_WHATSAPP.md",
        "COMANDO_HERMES.md",
        "COMANDO_MANUAL.md",
    ]
    chunks = []
    for name in candidates:
        path = folder / name
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for marker in ("## Corpo", "## Resumo", "Resumo operacional:"):
            if marker in text:
                text = text.split(marker, 1)[1]
                break
        chunks.append(text)
    return "\n\n".join(chunks)


def enrich_item(item, workspace, forja_status=None):
    item["forja"] = copy.deepcopy(forja_status) if isinstance(forja_status, dict) else {
        "version": "N3.0-r2",
        "lifecycleStatus": "not_run",
        "phaseCursor": None,
        "blockers": [],
        "nextAction": "A FORJA ainda não foi executada nesta demanda.",
        "artifacts": [],
        "visualQa": {"reviewed": 0, "total": 0, "status": "not_run"},
        "stale": False,
    }
    derived = dict(item.get("derived") or {})
    threads = [x for x in item.get("threadIds") or [] if x]
    received = [x for x in item.get("emailsRecebidos") or [] if x]
    response = [x for x in item.get("emailsResposta") or [] if x]
    email_links = []
    if threads:
        for idx, thread_id in enumerate(threads[:3], 1):
            email_links.append(
                {
                    "label": "Abrir conversa no Gmail" if idx == 1 else f"Conversa Gmail {idx}",
                    "url": gmail_url(thread_id),
                    "kind": "thread",
                    "id": thread_id,
                }
            )
    elif received:
        for idx, message_id in enumerate(received[:3], 1):
            email_links.append(
                {
                    "label": "Abrir e-mail original" if idx == 1 else f"E-mail recebido {idx}",
                    "url": gmail_url(message_id),
                    "kind": "message",
                    "id": message_id,
                }
            )
    derived["fonteLabel"] = source_label(item.get("origem"))
    derived["emailLinks"] = email_links
    derived["emailIdsResumo"] = {
        "recebidos": received[:5],
        "respostas": response[:5],
        "threads": threads[:5],
    }

    mentions = []
    prazo_texto = item.get("prazoTexto") or ""
    mentions.extend(extract_date_mentions(prazo_texto, "prazoTexto"))
    body = command_body_for_item(workspace, item)
    mentions.extend(extract_date_mentions(body, "comandoEmail"))

    primary = item.get("prazo")
    by_date = {}
    for mention in mentions:
        if mention["date"] == primary:
            continue
        by_date.setdefault(mention["date"], mention)
    derived["dateMentions"] = sorted(by_date.values(), key=lambda x: x["date"])[:10]
    derived["hasDatesWithoutPrimary"] = bool(not primary and derived["dateMentions"])

    issues = []
    local = item.get("local") or {}
    attachments = item.get("anexos") or {}
    if not item.get("pasta") or local.get("folderExists") is False:
        issues.append({"code": "missing_folder", "label": "Pasta local ausente", "severity": "high"})
    if item.get("pasta") and local.get("comandoMd") is False:
        issues.append({"code": "missing_command", "label": "Comando da demanda ausente", "severity": "high"})
    if item.get("status") != "cumprida" and not item.get("prazo"):
        issues.append({"code": "missing_deadline", "label": "Prazo não confirmado", "severity": "medium"})
    if attachments.get("externosPendentes"):
        issues.append({"code": "external_attachments", "label": "Anexos externos pendentes", "severity": "medium"})
    expected = attachments.get("diretosEsperados")
    downloaded = attachments.get("diretosBaixados")
    if isinstance(expected, int) and isinstance(downloaded, int) and downloaded < expected:
        issues.append({"code": "attachment_gap", "label": f"Anexos {downloaded}/{expected}", "severity": "high"})
    if item.get("status") == "cumprida" and not item.get("evidenciaResposta"):
        issues.append({"code": "missing_evidence", "label": "Conclusão sem evidência", "severity": "high"})

    forja = item.get("forja") or {}
    lifecycle = str(forja.get("lifecycleStatus") or "not_run")
    nonterminal = {"not_run", "queued", "running", "blocked", "ready_for_review", "draft_awaiting_review"}
    review_states = {"ready_for_review", "draft_awaiting_review"}
    management_fulfilled = item.get("status") == "cumprida" and bool(str(item.get("evidenciaResposta") or "").strip())
    if item.get("status") == "cumprida" and lifecycle in nonterminal and not management_fulfilled:
        issues.append({"code": "forja_status_conflict", "label": "Gestão cumprida, FORJA ainda aberta", "severity": "high"})
    if item.get("status") == "pronta_para_revisao" and lifecycle not in review_states:
        issues.append({"code": "forja_status_conflict", "label": "Revisão da gestão diverge da FORJA", "severity": "high"})
    delivery = forja.get("deliveryEvidence")
    delivery_status = str((delivery or {}).get("status") or "") if isinstance(delivery, dict) else ""
    if lifecycle in nonterminal and delivery_status not in {"", "none"} and not management_fulfilled:
        issues.append({"code": "forja_delivery_conflict", "label": "Entrega vinculada a ciclo não concluído", "severity": "high"})
    if str(forja.get("mode") or "") in {"finalized_product_overlay", "n3_events"} or str(forja.get("version") or "").startswith("N3.0-r2"):
        missing_artifacts = [artifact for artifact in forja.get("artifacts") or [] if artifact.get("exists") is False]
        if missing_artifacts:
            issues.append({"code": "forja_artifact_missing", "label": f"Artefatos FORJA ausentes: {len(missing_artifacts)}", "severity": "high"})

    received = None
    try:
        received = datetime.fromisoformat(str(item.get("recebidoEm") or "").replace("Z", "+00:00"))
        if received.tzinfo:
            received = received.astimezone().replace(tzinfo=None)
    except (TypeError, ValueError):
        received = None
    derived["ageDays"] = max(0, (datetime.now() - received).days) if received else None
    derived["quality"] = {
        "issues": issues,
        "high": len([issue for issue in issues if issue["severity"] == "high"]),
        "medium": len([issue for issue in issues if issue["severity"] == "medium"]),
        "ok": not issues,
    }
    item["derived"] = derived
    return item


def enrich_snapshot(snapshot, workspace):
    result = copy.deepcopy(snapshot)
    demandas = result.get("demandas") or {}
    items = demandas.get("demandas") or []
    forja_items = ((result.get("forja") or {}).get("items") or {})
    demandas["demandas"] = [enrich_item(item, workspace, forja_items.get(str(item.get("id")))) for item in items]
    enriched_items = demandas["demandas"]
    linked_forja = [item for item in enriched_items if (item.get("forja") or {}).get("lifecycleStatus") != "not_run"]
    integration_issues = [
        issue
        for item in enriched_items
        for issue in ((item.get("derived") or {}).get("quality", {}).get("issues") or [])
        if str(issue.get("code") or "").startswith("forja_")
    ]
    result["insights"] = {
        "qualityIssues": sum(len((item.get("derived") or {}).get("quality", {}).get("issues") or []) for item in enriched_items),
        "missingDeadlines": len([item for item in enriched_items if item.get("status") != "cumprida" and not item.get("prazo")]),
        "missingFolders": len([item for item in enriched_items if any(issue.get("code") == "missing_folder" for issue in (item.get("derived") or {}).get("quality", {}).get("issues") or [])]),
        "missingEvidence": len([item for item in enriched_items if any(issue.get("code") == "missing_evidence" for issue in (item.get("derived") or {}).get("quality", {}).get("issues") or [])]),
        "forjaRunning": len([item for item in enriched_items if (item.get("forja") or {}).get("lifecycleStatus") == "running"]),
        "forjaBlocked": len([item for item in enriched_items if (item.get("forja") or {}).get("lifecycleStatus") == "blocked"]),
        "forjaReady": len([item for item in enriched_items if (item.get("forja") or {}).get("lifecycleStatus") in {"ready_for_review", "draft_awaiting_review"}]),
        "forjaNotRun": len([item for item in enriched_items if (item.get("forja") or {}).get("lifecycleStatus") == "not_run"]),
        "forjaIntegrityBlocked": len([item for item in enriched_items if ((item.get("forja") or {}).get("integrity") or {}).get("status") == "blocked"]),
        "forjaLinked": len(linked_forja),
        "forjaTotal": len(enriched_items),
        "forjaCoveragePercent": round((100 * len(linked_forja) / len(enriched_items)), 1) if enriched_items else 100.0,
        "forjaIntegrationIssues": len(integration_issues),
        "forjaStatusConflicts": len([issue for issue in integration_issues if issue.get("code") == "forja_status_conflict"]),
        "forjaDeliveryConflicts": len([issue for issue in integration_issues if issue.get("code") == "forja_delivery_conflict"]),
        "forjaArtifactFailures": len([issue for issue in integration_issues if issue.get("code") == "forja_artifact_missing"]),
    }
    return result
