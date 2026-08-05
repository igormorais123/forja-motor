from pathlib import Path

from office_io import atomic_write_json, now_iso, read_json


ROOT = Path(__file__).resolve().parents[1]
DEMANDS_PATH = ROOT / "data" / "demandas.json"
MANUAL_PATH = ROOT / "data" / "intervencoes_manuais.json"
DEMAND_ID = "email-auto-19f3ea400b7dec3d"
DELIVERY_ID = "19f871e89ca4a984"
DELIVERY_THREAD_ID = "19f3ea400b7dec3d"
CASE_FOLDER = "Material para elaboração de parecer - interessado Deltan Dallagnol"
N4_FOLDER = f"{CASE_FOLDER}/_forja_n4_atualizacao_2026-07-21"


SUMMARY = (
    "N4 produzida após o complemento urgente de 21/07/2026. O parecer incorpora o RDE e dois "
    "pareceres supervenientes, define Senado/PR, usa a tabela como matriz crítica e registra "
    "inconsistências que impedem sua adoção literal. DOCX/PDF foram entregues ao Fábio para "
    "revisão interna."
)

NEXT_ACTION = (
    "Obter o áudio ou transcrição conferível do advogado Leandro e o número/recibo do RDE. "
    "Depois, conferir certidões, inteiros teores e anexos probatórios antes de gerar versão "
    "assinável ou liberar qualquer uso externo."
)

EVIDENCE = (
    "Entrega interna N4 confirmada no Gmail 19f871e89ca4a984, em 21/07/2026, com DOCX e PDF. "
    "A evidência comprova a remessa para revisão do escritório, não a conclusão integral da "
    "nova instrução nem liberação externa: o áudio do Leandro e o identificador oficial do RDE "
    "continuam pendentes."
)


def append_comment(entry: dict, payload: dict) -> None:
    comments = entry.setdefault("comentarios", [])
    if not any(item.get("id") == payload["id"] for item in comments):
        comments.append(payload)


def main() -> None:
    data = read_json(DEMANDS_PATH, {"schema": 1, "demandas": []}) or {
        "schema": 1,
        "demandas": [],
    }
    demand = next(
        (item for item in data.get("demandas", []) if item.get("id") == DEMAND_ID),
        None,
    )
    if demand is None:
        raise SystemExit(f"demanda não encontrada: {DEMAND_ID}")

    replies = demand.setdefault("emailsResposta", [])
    if DELIVERY_ID not in replies:
        replies.append(DELIVERY_ID)
    demand.update(
        {
            "pasta": CASE_FOLDER,
            "prazo": None,
            "prazoTexto": (
                "complemento urgente recebido em 21/07/2026; sem novo prazo objetivo informado"
            ),
            "resumo": SUMMARY,
            "proximaAcao": NEXT_ACTION,
            "status": "aberta",
            "respondidoComConteudo": True,
            "evidenciaResposta": EVIDENCE,
            "evidenciaTipo": "email",
            "urgenciaManual": "alta",
        }
    )
    demand["tags"] = list(
        dict.fromkeys(
            [
                *(demand.get("tags") or []),
                "reaberta por complemento",
                "N4 entregue internamente",
                "áudio pendente",
                "RDE 2026",
            ]
        )
    )
    data["updatedAt"] = now_iso()
    atomic_write_json(DEMANDS_PATH, data)

    manual = read_json(MANUAL_PATH, {"schema": 1, "items": {}}) or {
        "schema": 1,
        "items": {},
    }
    entry = manual.setdefault("items", {}).setdefault(
        DEMAND_ID, {"comentarios": [], "overrides": {}}
    )
    now = now_iso()
    append_comment(
        entry,
        {
            "id": "deltan-complemento-sanitizado-20260721",
            "at": now,
            "tipo": "whatsapp-sanitizado",
            "texto": (
                "Fábio pediu exame urgente do novo conjunto do caso Deltan, consideração da "
                "orientação oral do advogado Leandro e avaliação da utilidade de uma tabela por "
                "procedimento. O cargo foi esclarecido como Senado/PR. Nenhuma conversa bruta foi "
                "transcrita no painel."
            ),
            "autor": "Igor/Codex",
        },
    )
    append_comment(
        entry,
        {
            "id": "deltan-forja-n4-20260721",
            "at": now,
            "tipo": "forja-n4-producao",
            "texto": (
                "Parecer N4 concluído para revisão interna: 24 páginas, quatro elementos visuais, "
                "fidelidade integral, zero achados P0 e inspeção visual de todas as páginas. A "
                "tabela foi aproveitada criticamente; inconsistências de número, datas e estado "
                "processual foram registradas. O texto externo não contém marcadores de auditoria "
                "nem proveniência operacional."
            ),
            "autor": "FORJA N4/Codex",
        },
    )
    append_comment(
        entry,
        {
            "id": f"deltan-entrega-{DELIVERY_ID}",
            "at": now,
            "tipo": "entrega-interna",
            "texto": EVIDENCE,
            "autor": "Igor/Codex",
        },
    )

    entry.setdefault("overrides", {}).update(
        {
            "status": "aberta",
            "respondidoComConteudo": True,
            "urgenciaManual": "alta",
            "prazo": None,
            "prazoTexto": (
                "complemento urgente recebido em 21/07/2026; sem novo prazo objetivo informado"
            ),
            "resumo": SUMMARY,
            "proximaAcao": NEXT_ACTION,
            "evidenciaResposta": EVIDENCE,
            "evidenciaTipo": "email",
            "tags": demand["tags"],
        }
    )
    entry["forja"] = {
        "overrideCanonicalN3": True,
        "lifecycleStatus": "blocked",
        "phaseCursor": "F10_RECONCILIACAO_GESTAO",
        "completedPhases": [
            "F7_AUDITORIA",
            "F8_QA_VISUAL",
            "F9_PACOTE_REVISAO",
        ],
        "gates": {
            "F7_AUDITORIA": {"status": "pass", "p0": 0},
            "F8_QA_VISUAL": {"status": "pass", "findings": 0},
            "F9_PACOTE_REVISAO": {"status": "pass_internal_only"},
        },
        "blockers": [
            "Áudio ou transcrição conferível do advogado Leandro não disponível.",
            "Número e recibo oficial do RDE não fornecidos.",
            "Certidões, inteiros teores e anexos probatórios ainda exigem conferência.",
        ],
        "visualQa": {"reviewed": 24, "total": 24, "status": "pass"},
        "artifacts": [
            {
                "path": f"{N4_FOLDER}/PARECER_DELTAN_N4_REVISAO_INTERNA.docx",
                "label": "Parecer Deltan N4 - Word",
                "role": "opinion",
                "audience": "internal_review",
            },
            {
                "path": f"{N4_FOLDER}/PARECER_DELTAN_N4_REVISAO_INTERNA.pdf",
                "label": "Parecer Deltan N4 - PDF",
                "role": "opinion",
                "audience": "internal_review",
            },
            {
                "path": f"{N4_FOLDER}/MATRIZ_INTEGRACAO_RDE_PARECERES_N4.md",
                "label": "Matriz crítica do RDE e pareceres",
                "role": "evidence_matrix",
                "audience": "internal_working",
            },
        ],
        # A remessa interna parcial fica na evidência da demanda. No ciclo
        # FORJA, deliveryEvidence permanece nulo para não sugerir conclusão
        # enquanto persistirem bloqueadores jurídicos materiais.
        "deliveryEvidence": None,
        "nextAction": NEXT_ACTION,
    }
    entry["updatedAt"] = now
    manual["updatedAt"] = now
    atomic_write_json(MANUAL_PATH, manual)

    print(
        {
            "ok": True,
            "demandId": DEMAND_ID,
            "status": "aberta",
            "respondidoComConteudo": True,
            "deliveryId": DELIVERY_ID,
        }
    )


if __name__ == "__main__":
    main()
