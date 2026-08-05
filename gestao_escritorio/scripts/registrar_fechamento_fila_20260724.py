from __future__ import annotations

from office_io import atomic_write_json, now_iso, read_json


ROOT = __import__("pathlib").Path(__file__).resolve().parents[1]
DEMANDS_PATH = ROOT / "data" / "demandas.json"
MANUAL_PATH = ROOT / "data" / "intervencoes_manuais.json"

DELIVERIES = {
    "email-corsan-agerst-19f3dc9ff92081cd": {
        "message": "19f94dd4449f2751",
        "thread": "19f3dc9ff92081cd",
        "summary": (
            "Aditamento interno sobre execução fiscal e boletim de ocorrência entregue em "
            "DOCX/PDF, com separação das frentes, ressalvas probatórias e QA visual de 6/6 páginas."
        ),
        "next": (
            "Fábio e Nilson revisarem o aditamento. A liberação externa continua condicionada "
            "à cadeia administrativa integral, à conferência da citação/exigibilidade e à "
            "indexação do processo volumoso."
        ),
        "evidence": (
            "Entrega interna CORSAN/AGERST enviada ao Fábio, com cópia ao Nilson, no Gmail "
            "19f94dd4449f2751, thread 19f3dc9ff92081cd, com DOCX e PDF. As pendências documentais "
            "foram preservadas como bloqueadores de uso externo, não como trabalho pendente de Igor."
        ),
    },
    "email-auto-19f3ea400b7dec3d": {
        "message": "19f94e291f295b8e",
        "thread": "19f3ea400b7dec3d",
        "summary": (
            "Memorando N5 consolidado entregue com matriz saneada dos procedimentos, cronologia "
            "e conclusão prudencial; áudios excluídos por orientação expressa."
        ),
        "next": (
            "Fábio revisar o memorando. Documentos do Dr. Leandro e fontes ainda nominadas "
            "permanecem condicionantes de qualquer versão externa."
        ),
        "evidence": (
            "Entrega interna Deltan N5 enviada ao Fábio no Gmail 19f94e291f295b8e, thread "
            "19f3ea400b7dec3d, com DOCX/PDF e anexos de fontes oficiais. Dependências documentais "
            "foram preservadas sem impedir o encerramento da entrega ao escritório."
        ),
    },
    "email-auto-19f888ab04efad45": {
        "message": "19f94dfa4b689bdf",
        "thread": "19f888ab04efad45",
        "summary": (
            "Nota técnica Cafelana atualizada com conferência viva do STF, comparação processual "
            "e mapa de rastreabilidade entregue ao escritório."
        ),
        "next": (
            "Fábio revisar. Antes de uso processual, obter a inicial integral da ACP e a petição "
            "92.561/2026 da PGR quando houver acesso ao conteúdo."
        ),
        "evidence": (
            "Dossiê Cafelana entregue ao Fábio no Gmail 19f94dfa4b689bdf, thread "
            "19f888ab04efad45, com DOCX/PDF e mapa documental. Lacunas da ACP e da petição da PGR "
            "foram mantidas como ressalvas pré-uso externo."
        ),
    },
    "email-auto-19f888002985a9d4": {
        "message": "19f94e08b79195be",
        "thread": "19f888002985a9d4",
        "summary": (
            "Pacote Natura/Cabreúva corrigido e paginado entregue com release gate, preservando "
            "a distinção entre revisão interna e liberação externa."
        ),
        "next": (
            "Fábio revisar. Uso externo permanece bloqueado até a obtenção dos recibos oficiais "
            "das 21 autoridades e a conferência final das premissas probatórias."
        ),
        "evidence": (
            "Pacote Natura/Cabreúva entregue ao Fábio no Gmail 19f94e08b79195be, thread "
            "19f888002985a9d4, com DOCX, PDF e release gate. A classificação internal_review_only "
            "e as 21 autoridades pendentes de recibo oficial foram expressamente preservadas."
        ),
    },
    "email-auto-19f8ca940af75d2d": {
        "message": "19f94d847022ea5a",
        "thread": "19f8ca940af75d2d",
        "summary": (
            "Avaliação Legal 500/Amplify concluída com recomendação negocial, condições de "
            "governança, dados, escopo, saída e custo-benefício."
        ),
        "next": (
            "Fábio decidir se abre negociação condicionada. Não assinar nem contratar Amplify "
            "sem proposta itemizada, minuta, DPA, SLA, integração e saída documentados."
        ),
        "evidence": (
            "Avaliação Legal 500/Amplify respondida ao Fábio no Gmail 19f94d847022ea5a, thread "
            "19f8ca940af75d2d, com recomendação de não assinatura imediata e condições objetivas "
            "para eventual piloto."
        ),
    },
    "email-auto-19f8cec883a0ac31": {
        "message": "19f94ec54b3e12d6",
        "thread": "19f8cec883a0ac31",
        "summary": (
            "Complementação substancial Vale Trading entregue em 14 páginas, com inventário, "
            "matriz dos embargos, matriz de premissas e quadro de cenários."
        ),
        "next": (
            "Fábio e Pedro revisarem. O quantum continua bloqueado até a tabela CIEX oficial, "
            "planilhas nativas, conciliação por operação e correção da escala de janeiro de 1989."
        ),
        "evidence": (
            "Adendo Vale Trading entregue ao Fábio, com cópia ao Pedro, no Gmail "
            "19f94ec54b3e12d6, thread 19f8cec883a0ac31, com DOCX/PDF e QA visual de 14/14 páginas. "
            "O documento substitui a orientação conclusiva anterior e permanece internal_review_only."
        ),
    },
}


def add_comment(entry: dict, demand_id: str, payload: dict, at: str) -> None:
    comment_id = f"fechamento-fila-20260724-{demand_id}"
    comments = entry.setdefault("comentarios", [])
    if any(item.get("id") == comment_id for item in comments):
        return
    comments.append(
        {
            "id": comment_id,
            "at": at,
            "tipo": "entrega-interna-reconciliada",
            "texto": (
                payload["evidence"]
                + " O status cumprida encerra a entrega operacional de Igor ao escritório; "
                "não declara protocolo, aprovação do cliente ou liberação externa."
            ),
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
    missing = sorted(set(DELIVERIES) - set(by_id))
    if missing:
        raise SystemExit(f"demandas não encontradas: {missing}")

    at = now_iso()
    for demand_id, payload in DELIVERIES.items():
        demand = by_id[demand_id]
        replies = demand.setdefault("emailsResposta", [])
        if payload["message"] not in replies:
            replies.append(payload["message"])
        demand.update(
            {
                "status": "cumprida",
                "respondidoComConteudo": True,
                "resumo": payload["summary"],
                "proximaAcao": payload["next"],
                "evidenciaResposta": payload["evidence"],
                "evidenciaTipo": "email",
            }
        )

        entry = manual.setdefault("items", {}).setdefault(
            demand_id, {"comentarios": [], "overrides": {}}
        )
        add_comment(entry, demand_id, payload, at)
        entry.setdefault("overrides", {}).update(
            {
                "status": "cumprida",
                "respondidoComConteudo": True,
                "resumo": payload["summary"],
                "proximaAcao": payload["next"],
                "evidenciaResposta": payload["evidence"],
                "evidenciaTipo": "email",
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
            "updated": len(DELIVERIES),
            "messageIds": [payload["message"] for payload in DELIVERIES.values()],
        }
    )


if __name__ == "__main__":
    main()
