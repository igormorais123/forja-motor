from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "demandas.json"
MANUAL = ROOT / "data" / "intervencoes_manuais.json"
NOW = "2026-07-29T16:55:00-03:00"

UPDATES = {
    "email-corsan-agerst-19f3dc9ff92081cd": {
        "message": "19faf69d5394fab2",
        "status": "aberta",
        "stage": "entregue_para_revisao",
        "summary": "Checklist exaustivo CORSAN/AGERST entregue ao Fábio, com cópia ao Nilson, separando recebimento, abertura, extração e conferência. Os três volumes digitalizados abrem e somam 283 páginas, mas não possuem camada textual.",
        "next": "Concluir a leitura visual e a indexação página a página dos três volumes de 100, 100 e 83 páginas antes de afirmar auditoria integral do processo do PROCON.",
        "evidence": "Word e PDF enviados no Gmail 19faf69d5394fab2, thread 19f3dc9ff92081cd; QA visual de 6/6 páginas concluído.",
    },
    "email-auto-19f888ab04efad45": {
        "message": "19faf6ad6c8e4349",
        "status": "aberta",
        "stage": "entregue_para_revisao",
        "summary": "Pacote oficial Cafelana/RE 1.395.147 entregue com decisão do STF, dois inteiros teores do STJ e mapa de rastreabilidade.",
        "next": "Monitorar a publicidade da petição PGR 92.561/2026 e obter a inicial integral da ACP; não tratar o rastreamento como documentalmente exaurido.",
        "evidence": "Quatro anexos enviados ao Fábio no Gmail 19faf6ad6c8e4349, thread 19f888ab04efad45.",
    },
    "email-auto-19f8ca940af75d2d": {
        "message": "19faf6d2bf90d500",
        "status": "cumprida",
        "stage": "entregue_ao_escritorio",
        "summary": "Matriz Legal 500 Premium + Amplify entregue com hierarquia documental, exigibilidade por função, arquitetura de dados, economia, plano 30/60/90 dias e recomendação de não contratar no estado documental atual.",
        "next": "Aguardar eventual nova quote e termos do fornecedor; uma nova emissão constitui novo insumo, não pendência documental do escritório.",
        "evidence": "Word e PDF enviados ao Fábio no Gmail 19faf6d2bf90d500, thread 19f8ca940af75d2d; QA visual de 11/11 páginas concluído.",
    },
    "email-auto-19f975ddb90c1675": {
        "message": "19faf5ce3a3dca0c",
        "status": "cumprida",
        "stage": "entregue_ao_escritorio",
        "summary": "Matriz consolidada das quatro frentes Natura/Cabreúva e corpus oficial entregues para revisão interna, sem contato externo.",
        "next": "Aguardar revisão do Fábio; eventual nova orientação gera nova rodada.",
        "evidence": "Word e PDF enviados ao Fábio no Gmail 19faf5ce3a3dca0c, thread 19f975ddb90c1675; QA visual de 3/3 páginas concluído.",
    },
    "email-auto-19faeca0e5607d67": {
        "message": "19faf57fec8f63f0",
        "status": "cumprida",
        "stage": "substituida_por_versao_final_do_titular",
        "summary": "A demanda original de memoriais JESC foi superada pela versão final encaminhada pelo Fábio, preservada como base oficial do escritório.",
        "next": "Nenhuma ação de redação; acompanhar apenas nova orientação expressa do titular.",
        "evidence": "Confirmação enviada no Gmail 19faf57fec8f63f0, reconhecendo a versão final do Fábio e a revisão humana do Alessandro.",
    },
    "email-auto-19faf1270ad26799": {
        "message": "19faf57fec8f63f0",
        "status": "cumprida",
        "stage": "entregue_ao_escritorio",
        "summary": "Ajustes finais JESC recebidos e reconciliados; a versão do Fábio foi mantida como versão final interna.",
        "next": "Nenhuma ação sem nova orientação.",
        "evidence": "Confirmação enviada no Gmail 19faf57fec8f63f0, no mesmo fluxo do caso.",
    },
    "email-auto-19faeffe655eeb4e": {
        "message": "19faf66efa3673af",
        "status": "aberta",
        "stage": "entregue_para_revisao",
        "summary": "Memoriais ERM/Transpetro entregues ao Alessandro, com cópia ao Fábio e à Controladoria, corrigindo processo e tribunal para AI 5004633-36.2026.4.03.0000/TRF3.",
        "next": "Fechar a leitura visual das seis peças escaneadas e a revisão cruzada entre famílias antes de liberar versão protocolável.",
        "evidence": "Word e PDF enviados no Gmail 19faf66efa3673af; QA visual de 6/6 páginas e gates lexicais concluídos.",
    },
    "email-auto-19faf0794679a6ba": {
        "message": "19faf6427977a315",
        "status": "aberta",
        "stage": "entregue_para_revisao",
        "summary": "Memoriais Estre/Transpetro entregues ao Alessandro, com cópia ao Fábio e à Controladoria, corrigindo a identificação para TRF3.",
        "next": "Fechar a leitura visual das fontes escaneadas e a revisão cruzada entre famílias antes de liberar versão protocolável.",
        "evidence": "Word e PDF enviados no Gmail 19faf6427977a315; QA visual de 7/7 páginas e gates lexicais concluídos.",
    },
}


def main() -> None:
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    manual_payload = json.loads(MANUAL.read_text(encoding="utf-8"))
    manual_items = manual_payload.setdefault("items", {})
    by_id = {item["id"]: item for item in payload["demandas"]}
    applied = []
    missing = []
    for demand_id, update in UPDATES.items():
        item = by_id.get(demand_id)
        if not item:
            missing.append(demand_id)
            continue
        message = update["message"]
        item.setdefault("emailsResposta", [])
        if message not in item["emailsResposta"]:
            item["emailsResposta"].append(message)
        item["status"] = update["status"]
        item["etapaOperacional"] = update["stage"]
        item["respondidoComConteudo"] = True
        item["resumo"] = update["summary"]
        item["proximaAcao"] = update["next"]
        item["evidenciaResposta"] = update["evidence"]
        item["evidenciaTipo"] = "email"
        manual = item.setdefault("manual", {})
        comments = manual.setdefault("comentarios", [])
        comment_id = f"entrega-20260729-{message}"
        if not any(c.get("id") == comment_id for c in comments):
            comments.append(
                {
                    "id": comment_id,
                    "at": NOW,
                    "tipo": "entrega-interna-reconciliada",
                    "texto": update["evidence"],
                    "autor": "Igor/Codex",
                }
            )
        manual["updatedAt"] = NOW
        manual["commentCount"] = len(comments)
        manual["lastComment"] = update["evidence"]
        overrides = manual.setdefault("overrides", {})
        overrides.update(
            {
                "status": update["status"],
                "respondidoComConteudo": True,
                "resumo": update["summary"],
                "proximaAcao": update["next"],
                "evidenciaResposta": update["evidence"],
                "evidenciaTipo": "email",
                "etapaOperacional": update["stage"],
            }
        )
        persistent = manual_items.setdefault(
            demand_id,
            {"updatedAt": NOW, "comentarios": [], "overrides": {}},
        )
        persistent_comments = persistent.setdefault("comentarios", [])
        if not any(c.get("id") == comment_id for c in persistent_comments):
            persistent_comments.append(
                {
                    "id": comment_id,
                    "at": NOW,
                    "tipo": "entrega-interna-reconciliada",
                    "texto": update["evidence"],
                    "autor": "Igor/Codex",
                }
            )
        persistent["updatedAt"] = NOW
        persistent.setdefault("overrides", {}).update(overrides)
        applied.append(demand_id)
    payload["atualizadoEm"] = datetime.now().astimezone().isoformat()
    manual_payload["updatedAt"] = NOW
    DATA.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    MANUAL.write_text(
        json.dumps(manual_payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"applied": applied, "missing": missing}, ensure_ascii=False))


if __name__ == "__main__":
    main()
