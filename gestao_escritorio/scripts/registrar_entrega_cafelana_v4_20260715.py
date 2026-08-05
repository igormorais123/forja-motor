from pathlib import Path

from office_io import atomic_write_json, now_iso, read_json


ROOT = Path(__file__).resolve().parents[1]
MANUAL_PATH = ROOT / "data" / "intervencoes_manuais.json"
DEMAND_ID = "email-cafelana-agint-aresp-2698443-19f2f0876e358eab"
AT = "2026-07-15T14:15:58-03:00"
EMAIL_ID = "19f66c733b7409da"
THREAD_ID = "19f4f728b4215846"


def main() -> None:
    manual = read_json(MANUAL_PATH, {"schema": 1, "items": {}}) or {"schema": 1, "items": {}}
    entry = manual.setdefault("items", {}).setdefault(DEMAND_ID, {"comentarios": [], "overrides": {}})
    comments = entry.setdefault("comentarios", [])
    comment_id = "entrega-cafelana-v4-auditada-20260715"
    if not any(comment.get("id") == comment_id for comment in comments):
        comments.append(
            {
                "id": comment_id,
                "at": AT,
                "tipo": "forja-entrega-auditada",
                "texto": (
                    "V4 protocolável concluída após leitura integral de A9 e confronto com A8. A formulação "
                    "foi corrigida para conhecimento parcial, preclusão do capítulo do art. 512/Súmula 284 "
                    "e desprovimento dos capítulos devolvidos; a intempestividade histórica foi retirada após "
                    "a Portaria TRF1 138/2024; prazo final fixado em 21/08/2026; multa apenas condicionada. "
                    "FORJA N4 F1–F10 aprovada com 24/24 artefatos, zero P0/P1 e nove páginas inspecionadas. "
                    f"DOCX/PDF enviados ao Fábio no Gmail {EMAIL_ID}, fio {THREAD_ID}, com readback confirmado."
                ),
                "autor": "FORJA N4/Codex",
            }
        )
    evidence = (
        f"V4 entregue ao Fábio no Gmail {EMAIL_ID}, no tópico {THREAD_ID}, "
        "com DOCX/PDF exatos e leitura de retorno confirmada."
    )
    entry.setdefault("overrides", {}).update(
        {
            "status": "cumprida",
            "respondidoComConteudo": True,
            "urgenciaManual": "media",
            "prazo": "2026-08-21",
            "prazoTexto": "termo final auditado da resposta: 21/08/2026; versão V4 entregue ao escritório em 15/07/2026",
            "resumo": (
                "Impugnação V4 concluída e entregue em DOCX/PDF. A íntegra do Agravo Interno foi confrontada "
                "com a decisão de 28/04/2026; a peça pede conhecimento parcial, preclusão do capítulo omitido "
                "e desprovimento da extensão conhecida."
            ),
            "proximaAcao": (
                "Fábio e Pedro revisarem a V4 e, antes do protocolo, confirmarem apenas a data efetiva de "
                "protocolo/assinatura e eventual movimentação processual superveniente."
            ),
            "evidenciaResposta": evidence,
            "evidenciaTipo": "email",
            "tags": ["STJ", "Cafelana", "AgInt", "V4 entregue", "FORJA N4 aprovada"],
        }
    )
    entry["updatedAt"] = AT
    manual["updatedAt"] = now_iso()
    atomic_write_json(MANUAL_PATH, manual)
    print({"ok": True, "demandId": DEMAND_ID, "emailId": EMAIL_ID})


if __name__ == "__main__":
    main()
