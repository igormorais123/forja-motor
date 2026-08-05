from pathlib import Path

from office_io import atomic_write_json, now_iso, read_json


ROOT = Path(__file__).resolve().parents[1]
MANUAL_PATH = ROOT / "data" / "intervencoes_manuais.json"
AT = "2026-07-15T13:43:10-03:00"
PRIMARY_ID = "email-auto-19f3f25cb64df962"
COMPLEMENT_ID = "email-auto-19f65f816c27ba65"
EMAIL_ID = "19f66a5e5fefe4db"


def upsert(items: dict, demand_id: str, *, comment_id: str, text: str, overrides: dict) -> None:
    entry = items.setdefault(demand_id, {"comentarios": [], "overrides": {}})
    comments = entry.setdefault("comentarios", [])
    if not any(comment.get("id") == comment_id for comment in comments):
        comments.append(
            {
                "id": comment_id,
                "at": AT,
                "tipo": "forja-entrega-auditada",
                "texto": text,
                "autor": "FORJA N4/Codex",
            }
        )
    entry.setdefault("overrides", {}).update(overrides)
    entry["updatedAt"] = AT


def main() -> None:
    manual = read_json(MANUAL_PATH, {"schema": 1, "items": {}})
    items = manual.setdefault("items", {})
    evidence = f"V8 entregue ao Fábio no Gmail {EMAIL_ID}, no tópico 19f65f816c27ba65, com DOCX/PDF conferidos."

    upsert(
        items,
        PRIMARY_ID,
        comment_id="entrega-v8-sulamerica-20260715-primary",
        text=(
            "Material autenticado de 15/07 incorporado na V8. A peça reconhece a assinatura da proposta "
            "comercial em 18/07/2025, distingue esse ato da DPS de 11/07/2025, não atribui autoria por "
            "campo sem log nativo e pede preservação/exibição da trilha técnica. F1–F10 e N4 aprovadas, "
            f"18 páginas inspecionadas e entrega confirmada no Gmail {EMAIL_ID}."
        ),
        overrides={
            "status": "cumprida",
            "respondidoComConteudo": True,
            "resumo": (
                "Petição inicial V8 substitutiva concluída em DOCX/PDF, com 18 páginas e gates jurídico, "
                "factual, visual e de entrega aprovados. A assinatura comercial foi reconhecida sem "
                "inferência indevida sobre autoria das respostas da DPS."
            ),
            "proximaAcao": (
                "Fábio revisar a V8. Antes do protocolo, confirmar mandato/curatela, relatório médico "
                "específico, tutela cirúrgica, numeração dos documentos e, se disponível, a trilha nativa "
                "de preenchimento da DPS."
            ),
            "evidenciaResposta": evidence,
            "evidenciaTipo": "email",
        },
    )

    upsert(
        items,
        COMPLEMENT_ID,
        comment_id="merge-v8-sulamerica-20260715-complement",
        text=(
            "Demanda complementar incorporada à demanda principal do caso SulAmérica "
            f"({PRIMARY_ID}); não constitui frente autônoma. O material foi analisado, a V8 foi gerada e "
            f"entregue no Gmail {EMAIL_ID}."
        ),
        overrides={
            "status": "cumprida",
            "respondidoComConteudo": True,
            "resumo": "Complemento autenticado absorvido pela V8 da demanda principal SulAmérica/Mateus.",
            "proximaAcao": f"Acompanhar a revisão humana na demanda principal {PRIMARY_ID}.",
            "evidenciaResposta": evidence,
            "evidenciaTipo": "email",
        },
    )

    manual["updatedAt"] = now_iso()
    atomic_write_json(MANUAL_PATH, manual)
    print({"ok": True, "updated": [PRIMARY_ID, COMPLEMENT_ID], "emailId": EMAIL_ID})


if __name__ == "__main__":
    main()
