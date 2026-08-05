from __future__ import annotations

from pathlib import Path

from office_io import atomic_write_json, now_iso, read_json


ROOT = Path(__file__).resolve().parents[1]
DEMANDS_PATH = ROOT / "data" / "demandas.json"
MANUAL_PATH = ROOT / "data" / "intervencoes_manuais.json"
DEMAND_ID = "email-auto-19fa9e2969483efd"
MESSAGE_ID = "19fabd8c8457195d"
EVIDENCE = (
    "Entrega interna comprovada no mesmo thread do Gmail pela mensagem "
    f"{MESSAGE_ID}, com NYLTON_MEMORIAIS_EDCL_TRF2_V1.docx e "
    "NYLTON_MEMORIAIS_EDCL_TRF2_V1.pdf anexados para revisão do escritório."
)
NEXT_ACTION = (
    "Aguardar a revisão do escritório e eventual pedido de ajuste; protocolo e decisão "
    "sobre oposição ao julgamento virtual permanecem com o advogado responsável."
)


def main() -> None:
    data = read_json(DEMANDS_PATH, {"schema": 1, "demandas": []})
    manual = read_json(MANUAL_PATH, {"schema": 1, "items": {}})
    demand = next(
        (item for item in data.get("demandas", []) if item.get("id") == DEMAND_ID),
        None,
    )
    if not demand:
        raise SystemExit(f"demanda não encontrada: {DEMAND_ID}")

    replies = demand.setdefault("emailsResposta", [])
    if MESSAGE_ID not in replies:
        replies.append(MESSAGE_ID)
    demand.update(
        {
            "status": "cumprida",
            "etapaOperacional": "entregue_para_revisao",
            "respondidoComConteudo": True,
            "evidenciaTipo": "email",
            "evidenciaResposta": EVIDENCE,
            "proximaAcao": NEXT_ACTION,
        }
    )

    at = now_iso()
    entry = manual.setdefault("items", {}).setdefault(
        DEMAND_ID, {"comentarios": [], "overrides": {}}
    )
    comment_id = "entrega-nylton-20260729"
    comments = entry.setdefault("comentarios", [])
    if not any(comment.get("id") == comment_id for comment in comments):
        comments.append(
            {
                "id": comment_id,
                "at": at,
                "tipo": "entrega-interna",
                "texto": EVIDENCE,
                "autor": "Igor/Codex",
            }
        )
    entry.setdefault("overrides", {}).update(
        {
            "status": "cumprida",
            "respondidoComConteudo": True,
            "evidenciaTipo": "email",
            "evidenciaResposta": EVIDENCE,
            "proximaAcao": NEXT_ACTION,
        }
    )
    entry["updatedAt"] = at
    data["updatedAt"] = at
    manual["updatedAt"] = at
    atomic_write_json(DEMANDS_PATH, data)
    atomic_write_json(MANUAL_PATH, manual)
    print(
        {
            "ok": True,
            "demandId": DEMAND_ID,
            "status": "cumprida",
            "stage": "entregue_para_revisao",
            "messageId": MESSAGE_ID,
        }
    )


if __name__ == "__main__":
    main()
