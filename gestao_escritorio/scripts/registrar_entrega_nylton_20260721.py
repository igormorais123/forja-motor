from pathlib import Path

from office_io import atomic_write_json, now_iso, read_json


ROOT = Path(__file__).resolve().parents[1]
MANUAL_PATH = ROOT / "data" / "intervencoes_manuais.json"
DEMANDS_PATH = ROOT / "data" / "demandas.json"
DEMAND_ID = "email-auto-19f81838ad4d83ce"
EMAIL_ID = "19f82a496dbd2196"
THREAD_ID = "19f81838ad4d83ce"
SENT_AT = "2026-07-21T00:07:32-03:00"
PACKAGE_HASH = "75174d5996c12c10be738c4db572080c5eff3300af61cdf12738fcd048b641c0"


def main() -> None:
    evidence = (
        f"Minuta entregue ao escritório no Gmail {EMAIL_ID}, fio {THREAD_ID}, em 21/07/2026, "
        "com DOCX e PDF anexados e leitura de retorno confirmada. "
        f"Pacote FORJA hash {PACKAGE_HASH}."
    )

    manual = read_json(MANUAL_PATH, {"schema": 1, "items": {}}) or {"schema": 1, "items": {}}
    entry = manual.setdefault("items", {}).setdefault(DEMAND_ID, {"comentarios": [], "overrides": {}})
    comments = entry.setdefault("comentarios", [])
    comment_id = f"entrega-nylton-{EMAIL_ID}"
    if not any(comment.get("id") == comment_id for comment in comments):
        comments.append(
            {
                "id": comment_id,
                "at": SENT_AT,
                "tipo": "forja-entrega-auditada",
                "texto": (
                    "Acesso e ingestão dos 11 PDFs concluídos: 7.969 páginas. A cronologia mostrou que "
                    "embargos de declaração contra o evento 718 enfrentariam intempestividade e que o "
                    "evento 734 é ato ordinatório. A entrega foi convertida em manifestação urgente com "
                    "pedido de suspensão cautelar, certificação do processo dependente e decisão expressa. "
                    "FORJA F0-F9, Fable 5, fidelidade integral e QA visual das cinco páginas aprovados. "
                    f"DOCX/PDF enviados no Gmail {EMAIL_ID}; destinatários e dois anexos confirmados por readback."
                ),
                "autor": "Igor/Codex",
            }
        )
    entry.setdefault("overrides", {}).update(
        {
            "status": "cumprida",
            "respondidoComConteudo": True,
            "urgenciaManual": "alta",
            "prazo": "2026-07-21",
            "prazoTexto": (
                "prazo interno 21/07/2026 cumprido; minuta entregue ao escritório em 21/07; "
                "protocolo indicado pelo Fábio para 23/07; intimação do evento 735 registrada no eproc até 24/07"
            ),
            "resumo": (
                "Manifestacão urgente sobre o ato ordinatório do evento 734 entregue em DOCX/PDF. "
                "A peça pede suspensão cautelar dos atos expropriatórios e certificação do estado "
                "dos Embargos de Terceiro, evitando embargos de declaração intempestivos."
            ),
            "proximaAcao": (
                "Fábio e João revisarem a minuta e providenciarem o protocolo no prazo do escritório. "
                "A entrega de Igor está concluída e comprovada."
            ),
            "evidenciaResposta": evidence,
            "evidenciaTipo": "email",
            "tags": [
                "Nylton Simões",
                "manifestação urgente entregue",
                "suspensão de leilão",
                "FORJA aprovada",
                "prazo interno cumprido",
            ],
        }
    )
    entry["updatedAt"] = SENT_AT
    manual["updatedAt"] = now_iso()
    atomic_write_json(MANUAL_PATH, manual)

    data = read_json(DEMANDS_PATH, {"schema": 1, "demandas": []}) or {"schema": 1, "demandas": []}
    match = next((item for item in data.get("demandas", []) if item.get("id") == DEMAND_ID), None)
    if match is None:
        raise RuntimeError(f"Demanda ausente: {DEMAND_ID}")
    responses = match.setdefault("emailsResposta", [])
    if EMAIL_ID not in responses:
        responses.append(EMAIL_ID)
    data["updatedAt"] = now_iso()
    atomic_write_json(DEMANDS_PATH, data)

    print({"ok": True, "demandId": DEMAND_ID, "emailId": EMAIL_ID, "threadId": THREAD_ID})


if __name__ == "__main__":
    main()
