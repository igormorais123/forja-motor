"""Fecha, de forma idempotente, os dois cartões duplicados dos EDcl Libra Sul."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from office_io import atomic_write_json, now_iso, read_json


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
DATA_PATH = ROOT / "data" / "demandas.json"
MANUAL_PATH = ROOT / "data" / "intervencoes_manuais.json"

DEMAND_IDS = (
    "email-auto-19fa5c4c6536b438",
    "email-auto-19fab5f079a2c305",
)
MESSAGE_ID = "19fabe7f08b9c742"
THREAD_ID = "19fab5f079a2c305"
CASE_FOLDER = (
    "URGENTE - Medida Cautelar Fiscal n.º 5002486-81.2012.4.04.7216 SC "
    "- analise a aperfeiçoamento de Embargos de D"
)
DELIVERY_FOLDER = WORKSPACE / CASE_FOLDER / "ENTREGA_FORJA_2026-07-29"
DELIVERABLES = (
    "EDCL_LIBRA_SUL_EVENTO_176_REVISAO_INTERNA.docx",
    "EDCL_LIBRA_SUL_EVENTO_176_REVISAO_INTERNA.pdf",
)
REGISTER = DELIVERY_FOLDER / "REGISTRO_FECHAMENTO_LIBRA_SUL_2026-07-29.md"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def main() -> None:
    missing = [str(DELIVERY_FOLDER / name) for name in DELIVERABLES if not (DELIVERY_FOLDER / name).is_file()]
    if not REGISTER.is_file():
        missing.append(str(REGISTER))
    if missing:
        raise SystemExit("Artefatos de fechamento ausentes: " + "; ".join(missing))

    hashes = {name: sha256(DELIVERY_FOLDER / name) for name in DELIVERABLES}
    evidence = (
        f"Entrega interna por e-mail Gmail {MESSAGE_ID}, conversa {THREAD_ID}, "
        f"com DOCX SHA-256 {hashes[DELIVERABLES[0]]} e PDF SHA-256 {hashes[DELIVERABLES[1]]}. "
        "Destinatário: Fábio Medina Osório; cópias: Alessandro Rodrigues e Controladoria. "
        "Versão internal_review_only; conferência no eproc e protocolo são providências do escritório."
    )
    comment = (
        "LIBRA SUL encerrada em 29/07/2026. Os dois cartões abertos correspondiam à mesma obrigação "
        f"material, cumprida pelo e-mail {MESSAGE_ID} com DOCX e PDF. Releitura do Gmail, do acervo e "
        "do WhatsApp sanitizado não identificou outra demanda Libra Sul pendente. O protocolo judicial "
        "permanece fora do limite operacional de Igor."
    )
    stamp = now_iso()

    data = read_json(DATA_PATH, {"schema": 1, "demandas": []})
    manual = read_json(MANUAL_PATH, {"schema": 1, "updatedAt": stamp, "items": {}})
    manual.setdefault("schema", 1)
    manual.setdefault("items", {})
    found = set()

    for item in data.get("demandas", []):
        item_id = item.get("id")
        if item_id not in DEMAND_IDS:
            continue
        found.add(item_id)
        item["status"] = "cumprida"
        item["respondidoComConteudo"] = True
        item["evidenciaResposta"] = evidence
        item["evidenciaTipo"] = "email"
        item["etapaOperacional"] = "cumprida"
        item["proximaAcao"] = "Nenhuma ação interna pendente; revisão final e protocolo cabem ao escritório."
        item["urgenciaManual"] = "normal"
        item.setdefault("emailsResposta", [])
        if MESSAGE_ID not in item["emailsResposta"]:
            item["emailsResposta"].append(MESSAGE_ID)
        item.setdefault("threadIds", [])
        if THREAD_ID not in item["threadIds"]:
            item["threadIds"].append(THREAD_ID)
        attachments = item.setdefault("anexos", {})
        attachments["externosPendentes"] = False
        if item_id == "email-auto-19fab5f079a2c305":
            attachments["diretosEsperados"] = 0
            attachments["diretosBaixados"] = 0
            attachments["observacao"] = (
                "Cartão duplicado de confirmação urgente, sem anexo próprio; insumos materializados "
                "na demanda original e produto entregue por e-mail."
            )

        entry = manual["items"].setdefault(item_id, {"comentarios": [], "overrides": {}})
        comments = entry.setdefault("comentarios", [])
        comment_id = f"fechamento-libra-sul-20260729-{item_id}"
        if not any(row.get("id") == comment_id for row in comments):
            comments.append(
                {
                    "id": comment_id,
                    "at": stamp,
                    "tipo": "fechamento-multicanal",
                    "texto": comment,
                    "autor": "Igor/Codex",
                }
            )
        overrides = entry.setdefault("overrides", {})
        overrides.update(
            {
                "status": "cumprida",
                "respondidoComConteudo": True,
                "evidenciaResposta": evidence,
                "evidenciaTipo": "email",
                "proximaAcao": "Nenhuma ação interna pendente; revisão final e protocolo cabem ao escritório.",
                "urgenciaManual": "normal",
            }
        )
        entry["updatedAt"] = stamp

    absent = sorted(set(DEMAND_IDS) - found)
    if absent:
        raise SystemExit("Demandas não localizadas: " + ", ".join(absent))

    data["updatedAt"] = stamp
    manual["updatedAt"] = stamp
    atomic_write_json(DATA_PATH, data)
    atomic_write_json(MANUAL_PATH, manual)
    print(
        json.dumps(
            {
                "ok": True,
                "closed": sorted(found),
                "messageId": MESSAGE_ID,
                "hashes": hashes,
                "register": str(REGISTER),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
