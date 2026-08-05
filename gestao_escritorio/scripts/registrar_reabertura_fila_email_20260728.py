from __future__ import annotations

from office_io import atomic_write_json, now_iso, read_json


ROOT = __import__("pathlib").Path(__file__).resolve().parents[1]
DEMANDS_PATH = ROOT / "data" / "demandas.json"
MANUAL_PATH = ROOT / "data" / "intervencoes_manuais.json"


UPDATES = {
    "email-auto-19fa9e2969483efd": {
        "message": "19fabc554a30f5ff",
        "stage": "respondida_em_producao",
        "deadline": "2026-07-30",
        "urgency": "critica",
        "next": (
            "Produzir e entregar ao escritório, até 30/07, os memoriais dos EDs no AI "
            "5006962-48.2026.4.02.0000/RJ em DOCX/PDF, após leitura integral dos autos, "
            "Regimento do TRF2, auditoria de fontes e QA visual."
        ),
        "comment": (
            "Recebimento e cronograma confirmados por e-mail ao Alessandro, com cópia ao Fábio "
            "e à Controladoria (Gmail 19fabc554a30f5ff). A resposta é de andamento; não prova "
            "entrega da minuta."
        ),
    },
    "email-auto-19f975ddb90c1675": {
        "message": "19fabc55aeeee819",
        "stage": "respondida_em_producao",
        "deadline": "2026-07-31",
        "urgency": "alta",
        "next": (
            "Entregar até 31/07 a matriz consolidada das quatro frentes e a próxima etapa do "
            "corpus oficial da Natura, sem contato ou proposta à companhia."
        ),
        "comment": (
            "Diretriz do Fábio reconhecida por e-mail (Gmail 19fabc55aeeee819). A entrega "
            "anterior cobriu apenas compliance; a demanda foi reaberta até a matriz das quatro "
            "frentes e o avanço do corpus oficial."
        ),
    },
    "email-auto-19f4f728b4215846": {
        "message": "19fabc560705687f",
        "stage": "respondida_em_revisao",
        "deadline": None,
        "urgency": "alta",
        "next": (
            "Reauditar cada precedente da versão final da Cafelana, preservar a formulação mais "
            "favorável tecnicamente sustentável e entregar peça ajustada, quadro de aderência e "
            "íntegras oficiais efetivamente utilizadas."
        ),
        "comment": (
            "Nova diretriz metodológica do Fábio respondida no Gmail 19fabc560705687f. A versão "
            "atual voltou a revisão interna e não deve ser tratada como liberada."
        ),
    },
    "email-auto-19f888ab04efad45": {
        "message": "19fabc5ad35486e3",
        "stage": "respondida_em_producao",
        "deadline": "2026-08-04",
        "urgency": "alta",
        "next": (
            "Montar pacote de decisões oficiais STF/STJ com índice de identidade e uso; manter a "
            "petição PGR 92.561/2026 como conteúdo não verificado enquanto não estiver pública."
        ),
        "comment": (
            "Fábio recebeu resposta sobre a origem autônoma do andamento da petição PGR "
            "92.561/2026 e sobre o pacote de decisões oficiais (Gmail 19fabc5ad35486e3). "
            "O conteúdo da petição continua não verificado."
        ),
    },
    "email-corsan-agerst-19f3dc9ff92081cd": {
        "message": "19fabc5b1b838720",
        "stage": "respondida_em_producao",
        "deadline": "2026-08-04",
        "urgency": "alta",
        "next": (
            "Entregar checklist exaustivo do acervo CORSAN/AGERST, distinguindo recebido, aberto, "
            "lido integralmente, apenas identificado, pendente de OCR/indexação e não localizado."
        ),
        "comment": (
            "Esclarecimento enviado ao Fábio, com cópia ao Nilson (Gmail 19fabc5b1b838720): "
            "o limite das 283 páginas era cobertura/indexação, não falha de abertura. A demanda "
            "permanece aberta até o checklist exaustivo."
        ),
    },
    "email-auto-19f8ca940af75d2d": {
        "message": "19fabc5b6a6d7b40",
        "stage": "respondida_em_producao",
        "deadline": "2026-08-20",
        "urgency": "media",
        "next": (
            "Revisar contrato, proposta, Amplify e mensagens da Serena sob direito inglês; "
            "entregar matriz contratual e minuta de cláusulas para renovação, sem aceite ou "
            "contato externo."
        ),
        "comment": (
            "Resposta preliminar enviada ao Fábio (Gmail 19fabc5b6a6d7b40), preservando a "
            "necessidade de testar incorporação, ordem de prevalência, acordo integral e alteração "
            "contratual antes de concluir que a proposta comercial vincula as partes."
        ),
    },
}


LIBRA_HANDOFFS = {
    "email-auto-19fa5c4c6536b438",
    "email-auto-19fab5f079a2c305",
}


def add_comment(entry: dict, demand_id: str, text: str, at: str) -> None:
    comment_id = f"reabertura-email-20260728-{demand_id}"
    comments = entry.setdefault("comentarios", [])
    if any(item.get("id") == comment_id for item in comments):
        return
    comments.append(
        {
            "id": comment_id,
            "at": at,
            "tipo": "reconciliacao-gmail",
            "texto": text,
            "autor": "Igor/Codex",
        }
    )


def main() -> None:
    data = read_json(DEMANDS_PATH, {"schema": 1, "demandas": []}) or {
        "schema": 1,
        "demandas": [],
    }
    manual = read_json(MANUAL_PATH, {"schema": 1, "items": {}}) or {
        "schema": 1,
        "items": {},
    }
    by_id = {item.get("id"): item for item in data.get("demandas", [])}
    missing = sorted((set(UPDATES) | LIBRA_HANDOFFS) - set(by_id))
    if missing:
        raise SystemExit(f"demandas não encontradas: {missing}")

    at = now_iso()
    for demand_id, payload in UPDATES.items():
        demand = by_id[demand_id]
        replies = demand.setdefault("emailsResposta", [])
        if payload["message"] not in replies:
            replies.append(payload["message"])
        demand.update(
            {
                "status": "aberta",
                "etapaOperacional": payload["stage"],
                "respondidoComConteudo": False,
                "proximaAcao": payload["next"],
                "urgenciaManual": payload["urgency"],
            }
        )
        if payload["deadline"]:
            demand["prazo"] = payload["deadline"]

        entry = manual.setdefault("items", {}).setdefault(
            demand_id, {"comentarios": [], "overrides": {}}
        )
        add_comment(entry, demand_id, payload["comment"], at)
        overrides = entry.setdefault("overrides", {})
        overrides.update(
            {
                "status": "aberta",
                "respondidoComConteudo": False,
                "proximaAcao": payload["next"],
                "urgenciaManual": payload["urgency"],
            }
        )
        if payload["deadline"]:
            overrides["prazo"] = payload["deadline"]
        entry["updatedAt"] = at

    for demand_id in LIBRA_HANDOFFS:
        demand = by_id[demand_id]
        next_action = (
            "Acompanhar a entrega pela outra instância já responsável pela LIBRA SUL; não "
            "executar nem responder em duplicidade nesta frente."
        )
        demand.update(
            {
                "status": "aberta",
                "etapaOperacional": "em_execucao_outra_instancia",
                "proximaAcao": next_action,
                "urgenciaManual": "critica",
            }
        )
        entry = manual.setdefault("items", {}).setdefault(
            demand_id, {"comentarios": [], "overrides": {}}
        )
        add_comment(
            entry,
            demand_id,
            (
                "Igor informou em 28/07 que o caso LIBRA SUL está sendo executado por outra "
                "instância. Esta execução excluiu a frente para evitar colisão e duplicidade."
            ),
            at,
        )
        entry.setdefault("overrides", {}).update(
            {
                "status": "aberta",
                "proximaAcao": next_action,
                "urgenciaManual": "critica",
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
            "reopened": len(UPDATES),
            "libraHandoffs": len(LIBRA_HANDOFFS),
            "messageIds": [item["message"] for item in UPDATES.values()],
        }
    )


if __name__ == "__main__":
    main()
