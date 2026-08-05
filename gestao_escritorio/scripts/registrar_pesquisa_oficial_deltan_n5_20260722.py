from pathlib import Path

from office_io import atomic_write_json, now_iso, read_json


ROOT = Path(__file__).resolve().parents[1]
DEMANDS_PATH = ROOT / "data" / "demandas.json"
MANUAL_PATH = ROOT / "data" / "intervencoes_manuais.json"
DEMAND_ID = "email-auto-19f3ea400b7dec3d"
CASE_FOLDER = "Material para elaboração de parecer - interessado Deltan Dallagnol"
N5_FOLDER = f"{CASE_FOLDER}/_forja_n5_acervo_disponivel_2026-07-22"


SUMMARY = (
    "N4 entregue para revisão interna e complementada por fechamento N5 de fontes oficiais. "
    "O inteiro teor do ED-RO-El 0601407-70/PR foi preservado e a cronologia corrigida, sem "
    "alteração da conclusão jurídica nem geração de nova versão externa."
)

NEXT_ACTION = (
    "Obter o áudio ou transcrição conferível do advogado Leandro e o número/recibo oficial do "
    "RDE. Em seguida, reunir os anexos do RDE, a certidão de trânsito do RO-El e as decisões ou "
    "certidões oficiais dos expedientes CNMP/MPF antes de liberar versão assinável ou externa."
)

COMMENT = (
    "Pesquisa oficial concluída com o acervo disponível: localizado e arquivado o acórdão do "
    "ED-RO-El 0601407-70/PR, julgado em 14/09/2023 e publicado em 21/09/2023. O TSE rejeitou "
    "os embargos por unanimidade e declarou prejudicado o pedido de efeito suspensivo. A fonte "
    "corrige a cronologia e o identificador da Sindicância 1.00145.2020-16, mas não substitui a "
    "certidão de trânsito nem as decisões individuais do CNMP/MPF. Nenhuma saída externa foi realizada."
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

    demand.update(
        {
            "resumo": SUMMARY,
            "proximaAcao": NEXT_ACTION,
            "status": "aberta",
            "respondidoComConteudo": True,
            "urgenciaManual": "alta",
        }
    )
    demand["tags"] = list(
        dict.fromkeys(
            [
                *(demand.get("tags") or []),
                "N5 fontes oficiais",
                "ED-RO-El localizado",
                "certidão de trânsito pendente",
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
            "id": "deltan-pesquisa-oficial-n5-20260722",
            "at": now,
            "tipo": "pesquisa-oficial",
            "texto": COMMENT,
            "autor": "Igor/Codex",
        },
    )

    entry.setdefault("overrides", {}).update(
        {
            "status": "aberta",
            "respondidoComConteudo": True,
            "urgenciaManual": "alta",
            "resumo": SUMMARY,
            "proximaAcao": NEXT_ACTION,
            "tags": demand["tags"],
        }
    )

    forja = entry.setdefault("forja", {})
    forja.update(
        {
            "overrideCanonicalN3": True,
            "lifecycleStatus": "blocked",
            "phaseCursor": "F10_RECONCILIACAO_GESTAO",
            "blockers": [
                "Áudio ou transcrição conferível do advogado Leandro não disponível.",
                "Número, recibo, distribuição e relatoria oficiais do RDE não comprovados.",
                "Anexos do RDE não disponíveis.",
                "Certidão de trânsito em julgado do RO-El não incorporada.",
                "Decisões e certidões oficiais dos expedientes CNMP/MPF incompletas.",
            ],
            "nextAction": NEXT_ACTION,
        }
    )
    artifacts = forja.setdefault("artifacts", [])
    new_artifacts = [
        {
            "path": f"{N5_FOLDER}/ADENDO_PESQUISA_OFICIAL_N5.md",
            "label": "Adendo N5 - fechamento de fontes oficiais",
            "role": "source_audit",
            "audience": "internal_working",
        },
        {
            "path": f"{N5_FOLDER}/CRONOLOGIA_E_GRAFO_ATOS_N5.md",
            "label": "Cronologia auditada N5",
            "role": "procedural_timeline",
            "audience": "internal_working",
        },
        {
            "path": (
                f"{N5_FOLDER}/fontes_oficiais/"
                "TSE_ED_RO_EL_0601407_70_ACORDAO_2023-09-14.pdf"
            ),
            "label": "TSE - acórdão oficial do ED-RO-El 0601407-70/PR",
            "role": "official_source",
            "audience": "internal_working",
        },
    ]
    existing_paths = {item.get("path") for item in artifacts}
    artifacts.extend(
        item for item in new_artifacts if item["path"] not in existing_paths
    )
    entry["updatedAt"] = now
    manual["updatedAt"] = now
    atomic_write_json(MANUAL_PATH, manual)

    print(
        {
            "ok": True,
            "demandId": DEMAND_ID,
            "status": "aberta",
            "newComment": "deltan-pesquisa-oficial-n5-20260722",
            "outbound": False,
        }
    )


if __name__ == "__main__":
    main()
