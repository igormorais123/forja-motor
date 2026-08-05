from pathlib import Path

from office_io import atomic_write_json, now_iso, read_json


ROOT = Path(__file__).resolve().parents[1]
DEMANDS_PATH = ROOT / "data" / "demandas.json"
MANUAL_PATH = ROOT / "data" / "intervencoes_manuais.json"
DEMAND_ID = "whatsapp-fabio-cafelana-re1395147-20260719"
RECEIVED_AT = "2026-07-19T20:37:36-03:00"
CASE_FOLDER = r"Cafelana\_demanda_whatsapp_re_1395147_2026-07-19"
MESSAGE_IDS = [
    "3A5E540FEABF35BFA1BF",
    "3A133E4EE741421C4D4E",
    "3A1C64BFCB7D15711421",
]
AUDIO_IDS = [
    "3A5597184B7369087849",
    "3AC1E36671A9992C5432",
]


def demand_payload() -> dict:
    return {
        "id": DEMAND_ID,
        "titulo": "Cafelana — revisão rastreável da comparação com o RE 1.395.147/PR",
        "clienteOuCaso": "Cafelana / STF RE 1.395.147/PR",
        "origem": "whatsapp",
        "emailsRecebidos": [],
        "emailsResposta": [],
        "pasta": CASE_FOLDER,
        "recebidoEm": RECEIVED_AT,
        "prazo": None,
        "prazoTexto": "sem prazo expresso; follow-up do Fábio localizado em 21/07/2026 e tratado como prioridade alta",
        "resumo": (
            "O Fábio pediu revisão integral e rastreável da nota comparativa entre Cafelana e o "
            "RE 1.395.147/PR, com 19 verificações sobre a origem e os pedidos da ACP, eventual "
            "frente investigativa/criminal, teoria fática e acervo integral de Cafelana."
        ),
        "proximaAcao": (
            "Conferir e enviar ao Fábio o rascunho executivo já preparado. Antes de uso processual, "
            "obter a inicial integral da ACP e ler a petição 92.561/2026 da PGR quando pública."
        ),
        "status": "aberta",
        "respondidoComConteudo": False,
        "evidenciaResposta": "",
        "urgenciaManual": "alta",
        "anexos": {
            "diretosBaixados": 5,
            "diretosEsperados": 5,
            "externosPendentes": True,
            "observacao": (
                "Dois áudios, dois PDFs técnicos e a nota HTML foram recuperados. Nove documentos-chave "
                "de Cafelana foram baixados do Drive; as três íntegras foram localizadas e ingeridas por texto."
            ),
        },
        "tags": [
            "WhatsApp",
            "Fábio",
            "Cafelana",
            "RE 1.395.147/PR",
            "rastreabilidade",
            "demanda nova",
        ],
        "manualSource": {
            "messageIds": MESSAGE_IDS,
            "audioMessageIds": AUDIO_IDS,
            "source": "whatsapp-live-audit-2026-07-21",
        },
    }


def main() -> None:
    data = read_json(DEMANDS_PATH, {"schema": 1, "demandas": []}) or {
        "schema": 1,
        "demandas": [],
    }
    demands = data.setdefault("demandas", [])
    existing = next((item for item in demands if item.get("id") == DEMAND_ID), None)
    if existing is None:
        demands.append(demand_payload())
        created = True
    else:
        preserved = {
            "emailsRecebidos": existing.get("emailsRecebidos", []),
            "emailsResposta": existing.get("emailsResposta", []),
        }
        existing.update(demand_payload())
        existing.update(preserved)
        created = False
    data["updatedAt"] = now_iso()
    atomic_write_json(DEMANDS_PATH, data)

    manual = read_json(MANUAL_PATH, {"schema": 1, "items": {}}) or {
        "schema": 1,
        "items": {},
    }
    entry = manual.setdefault("items", {}).setdefault(
        DEMAND_ID, {"comentarios": [], "overrides": {}}
    )
    comment_id = "auditoria-cafelana-re1395147-20260721"
    comments = entry.setdefault("comentarios", [])
    if not any(comment.get("id") == comment_id for comment in comments):
        comments.append(
            {
                "id": comment_id,
                "at": now_iso(),
                "tipo": "auditoria-documental",
                "texto": (
                    "Demanda específica separada da triagem genérica do WhatsApp. Acesso ao Drive confirmado; "
                    "nove documentos-chave materializados; inicial e liminar OCRizadas página a página; três "
                    "íntegras ingeridas por texto; fontes oficiais STF/STJ preservadas. Nota interna responde "
                    "as 19 questões e corrige a comparação anterior. Nenhuma resposta externa foi enviada."
                ),
                "autor": "Igor/Codex",
            }
        )
    draft_comment_id = "rascunho-executivo-cafelana-re1395147-20260721"
    if not any(comment.get("id") == draft_comment_id for comment in comments):
        comments.append(
            {
                "id": draft_comment_id,
                "at": now_iso(),
                "tipo": "rascunho-resposta",
                "texto": (
                    "Resposta executiva ao Fábio preparada com as correções jurídicas e as lacunas "
                    "materiais preservadas. Rascunho interno; nenhum envio externo foi realizado."
                ),
                "autor": "Igor/Codex",
            }
        )
    entry.setdefault("overrides", {}).update(
        {
            "status": "aberta",
            "respondidoComConteudo": False,
            "urgenciaManual": "alta",
            "prazoTexto": (
                "sem prazo expresso; follow-up do Fábio localizado em 21/07/2026 e tratado como prioridade alta"
            ),
            "resumo": demand_payload()["resumo"],
            "proximaAcao": demand_payload()["proximaAcao"],
            "tags": demand_payload()["tags"],
        }
    )
    entry["updatedAt"] = now_iso()
    manual["updatedAt"] = now_iso()
    atomic_write_json(MANUAL_PATH, manual)

    print(
        {
            "ok": True,
            "created": created,
            "demandId": DEMAND_ID,
            "demands": len(demands),
        }
    )


if __name__ == "__main__":
    main()
