from pathlib import Path

from office_io import atomic_write_json, now_iso, read_json


ROOT = Path(__file__).resolve().parents[1]
MANUAL_PATH = ROOT / "data" / "intervencoes_manuais.json"
DEMAND_ID = "email-natura-cabreuva-19f3991ebc75fe03"
AT = "2026-07-15T18:26:25-03:00"
EMAIL_ID = "19f6707b30feedc0"
THREAD_ID = "19f3991ebc75fe03"


def main() -> None:
    manual = read_json(MANUAL_PATH, {"schema": 1, "items": {}}) or {"schema": 1, "items": {}}
    entry = manual.setdefault("items", {}).setdefault(DEMAND_ID, {"comentarios": [], "overrides": {}})
    comments = entry.setdefault("comentarios", [])
    comment_id = "entrega-natura-v1-auditada-20260715"
    if not any(comment.get("id") == comment_id for comment in comments):
        comments.append(
            {
                "id": comment_id,
                "at": AT,
                "tipo": "forja-entrega-auditada",
                "texto": (
                    "Parecer Natura/Cabreúva V1 e nota urgente para a réplica concluídos após inspeção de "
                    "200/200 arquivos e 3.035 páginas, OCR dirigido e pesquisa em fontes oficiais. A análise "
                    "foi corrigida para segmentar prescrição, aplicar a modulação da ADI pelo dispositivo, "
                    "tratar R$ 35.097.209,80 como estimativa, separar envio de e-mail de recebimento/processamento "
                    "e limitar o alcance de PA, protesto e leis supervenientes. FORJA F1–F10 e N4 aprovadas, "
                    "24/24 artefatos, zero P0/P1. DOCX/PDF do parecer e da nota enviados ao Fábio no Gmail "
                    f"{EMAIL_ID}, fio {THREAD_ID}, com readback dos quatro anexos confirmado."
                ),
                "autor": "FORJA N4/Codex",
            }
        )
    evidence = (
        f"Parecer V1 e nota urgente entregues ao Fábio no Gmail {EMAIL_ID}, no tópico {THREAD_ID}, "
        "com quatro anexos exatos e leitura de retorno confirmada."
    )
    entry.setdefault("overrides", {}).update(
        {
            "status": "cumprida",
            "respondidoComConteudo": True,
            "urgenciaManual": "media",
            "prazo": "2026-07-20",
            "prazoTexto": (
                "minuta solicitada até 20/07/2026; parecer V1 e nota urgente entregues ao escritório "
                "em 15/07/2026; prazo aparente da réplica 23/07/2026 sujeito ao contador do portal"
            ),
            "resumo": (
                "Parecer Natura/Cabreúva V1 entregue em Word/PDF, com conclusão favorável condicionada "
                "à prova de ingresso do requerimento de 2021 e à segmentação temporal e contábil do crédito. "
                "Nota urgente da réplica também entregue."
            ),
            "proximaAcao": (
                "Fábio revisar o parecer. Antes de liberar à cliente ou protocolar, obter o anexo original "
                "do requerimento de agosto/2021, .eml/headers ou logs de recebimento, instrumento específico "
                "da sucessão Avon-Natura, confirmação do prazo no portal e matriz contábil parcela a parcela."
            ),
            "evidenciaResposta": evidence,
            "evidenciaTipo": "email",
            "tags": [
                "Natura",
                "Cabreúva",
                "parecer V1 entregue",
                "nota de réplica entregue",
                "FORJA N4 aprovada",
            ],
        }
    )
    entry["updatedAt"] = AT
    manual["updatedAt"] = now_iso()
    atomic_write_json(MANUAL_PATH, manual)
    print({"ok": True, "demandId": DEMAND_ID, "emailId": EMAIL_ID, "threadId": THREAD_ID})


if __name__ == "__main__":
    main()
