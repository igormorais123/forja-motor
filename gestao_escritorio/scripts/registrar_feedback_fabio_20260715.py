from pathlib import Path

from office_io import atomic_write_json, now_iso, read_json


ROOT = Path(__file__).resolve().parents[1]
MANUAL_PATH = ROOT / "data" / "intervencoes_manuais.json"
AT = "2026-07-15T00:12:00-03:00"
EMAIL_ID = "19f63cbcf127ba3b"


UPDATES = {
    "email-auto-19f3ed5bdbdcf159": {
        "status": "cumprida",
        "proximaAcao": (
            "Fábio revisar a V2 interna corrigida. Antes de uso externo, reunir e conferir os documentos "
            "contratuais e processuais ainda indicados no ledger e remover a classificação interna."
        ),
        "texto": (
            "Feedback de 14/07 incorporado na Azimut V2: limites do Tema 1368, segmentação temporal, "
            "Lei 14.905/2024, contratos, sub-rogação, admissibilidade, cumprimento provisório e "
            "prequestionamento revistos. DOCX/PDF internos com QA aprovados enviados ao Fábio por e-mail "
            f"Gmail {EMAIL_ID}."
        ),
    },
    "email-auto-19f3f25cb64df962": {
        "status": "cumprida",
        "proximaAcao": (
            "Fábio revisar a V7. Antes do protocolo, fechar mandato/curatela, definir a tutela cirúrgica, "
            "obter relatório médico específico e numerar o pacote documental conforme o manifesto."
        ),
        "texto": (
            "Feedback de 14/07 incorporado na V7 SulAmérica: omissão formal separada de autoria, controle "
            "e intenção; atuação material da secretária/intermediário; histórico Bradesco; natureza da "
            "contratação; documentos odontológicos reclassificados; exibição do dossiê de implantação e "
            "posição processual do intermediário revistos. DOCX/PDF com QA aprovados enviados ao Fábio por "
            f"e-mail Gmail {EMAIL_ID}."
        ),
    },
    "email-cafelana-agint-aresp-2698443-19f2f0876e358eab": {
        "status": "aberta",
        "proximaAcao": (
            "Obter o ato oficial de suspensão, fechar a cronologia do prazo, conferir os precedentes e os "
            "atos de liquidação/título e então produzir a versão protocolável em DOCX/PDF com QA."
        ),
        "texto": (
            "Feedback de 14/07 consolidado em protocolo corretivo: preliminar principal de ausência de "
            "impugnação específica a fundamento autônomo, retirada da intempestividade do AgInt atual, "
            "controle rigoroso da eventual intempestividade do AREsp e distinção dos precedentes. Blueprint "
            f"enviado ao Fábio por e-mail Gmail {EMAIL_ID}; versão protocolável permanece bloqueada por fontes oficiais."
        ),
    },
    "email-natura-cabreuva-19f3991ebc75fe03": {
        "status": "aberta",
        "proximaAcao": (
            "Executar OCR/inspeção dirigida dos documentos de baixa extração, conferir anexos do e-mail de "
            "20/08/2021 e consultar o PA E-14561/2025 para movimento posterior a maio de 2026; depois fechar parecer e quesitos."
        ),
        "texto": (
            "Busca integral dos seis itens solicitados executada sobre 205 arquivos e 3.034 páginas. Foram "
            "localizados os principais indícios e separadas as lacunas que ainda exigem OCR, inspeção visual "
            f"ou consulta oficial. Relatório operacional enviado ao Fábio por e-mail Gmail {EMAIL_ID}; demanda principal segue aberta."
        ),
    },
    "email-auto-19f621344387bbc8": {
        "status": "cumprida",
        "proximaAcao": (
            "Fábio avaliar o dossiê atualizado e definir se deseja a pesquisa processual nominal exaustiva e "
            "a estratégia de aproximação; nenhuma afirmação criminal atual deve ser usada sem processo exato."
        ),
        "texto": (
            "Atualização oficial do dossiê Chico Rodrigues concluída, com mandato, proposições recentes, "
            "agenda provável e cautela sobre notícia criminal histórica. Relatório enviado ao Fábio por "
            f"e-mail Gmail {EMAIL_ID}."
        ),
    },
}


def main():
    manual = read_json(MANUAL_PATH, {"schema": 1, "items": {}})
    manual.setdefault("schema", 1)
    items = manual.setdefault("items", {})

    for demand_id, update in UPDATES.items():
        entry = items.setdefault(demand_id, {"comentarios": [], "overrides": {}})
        comments = entry.setdefault("comentarios", [])
        comment_id = f"feedback-fabio-20260715-{demand_id}"
        if not any(comment.get("id") == comment_id for comment in comments):
            comments.append(
                {
                    "id": comment_id,
                    "at": AT,
                    "tipo": "feedback-juridico",
                    "texto": update["texto"],
                    "autor": "Codex/Hermes",
                }
            )

        overrides = entry.setdefault("overrides", {})
        overrides.update(
            {
                "status": update["status"],
                "respondidoComConteudo": True,
                "evidenciaResposta": f"Entrega consolidada ao Fábio por e-mail Gmail {EMAIL_ID} em 15/07/2026.",
                "evidenciaTipo": "email",
                "proximaAcao": update["proximaAcao"],
            }
        )
        entry["updatedAt"] = AT

    manual["updatedAt"] = now_iso()
    atomic_write_json(MANUAL_PATH, manual)
    print({"ok": True, "updated": len(UPDATES), "emailId": EMAIL_ID})


if __name__ == "__main__":
    main()
