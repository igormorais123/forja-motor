import json
from pathlib import Path

from office_io import atomic_write_json, now_iso, read_json


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "demandas.json"
MANUAL_PATH = ROOT / "data" / "intervencoes_manuais.json"


DELIVERIES = {
    "email-auto-19f4f728b4215846": {
        "message_id": "19f5685f97c18b95",
        "summary": "Comentários do Fábio sobre as contrarrazões Cafelana respondidos com relatório técnico consolidado em DOCX e PDF.",
        "next": "Solicitação deste e-mail respondida. A demanda principal permanece aberta até a obtenção das e-STJ fls. 938/949 e o fechamento da minuta sobre a base humana.",
        "evidence": "Resposta técnica entregue por e-mail Gmail 19f5685f97c18b95, na thread 19f4f728b4215846, com DOCX e PDF do relatório final de revisão Cafelana.",
    },
    "email-auto-19f4e4ba37368447": {
        "message_id": "19f56477ba346816",
        "summary": "Pedido de complementações Cafelana respondido com relatório técnico consolidado em DOCX e PDF.",
        "next": "Solicitação deste e-mail respondida. A demanda principal permanece aberta até a obtenção das e-STJ fls. 938/949.",
        "evidence": "Resposta técnica entregue por e-mail Gmail 19f56477ba346816, na thread 19f4e4ba37368447, com DOCX e PDF do relatório final de revisão Cafelana.",
    },
    "whatsapp-audio-cafelana-prevencao-20260708": {
        "message_id": "19f5685f97c18b95",
        "summary": "Diretrizes dos áudios sobre prevenção, preclusão e uso da peça humana incorporadas à revisão técnica e comunicadas ao Fábio.",
        "next": "Diretrizes incorporadas. A demanda principal Cafelana permanece aberta até a obtenção do agravo interno integral e o fechamento da minuta.",
        "evidence": "Diretrizes incorporadas e resultado técnico entregue ao Fábio por e-mail Gmail 19f5685f97c18b95, com relatório final em DOCX e PDF.",
    },
    "email-auto-19f3ed5bdbdcf159": {
        "message_id": "19f567c99b0cb4c7",
        "summary": "Memorial Azimut N3 condicionado enviado ao advogado do caso para revisão humana, em DOCX e PDF.",
        "next": "Etapa de minuta de Igor concluída. O advogado responsável deve lapidar a peça e conferir os sete grupos documentais indicados antes de eventual protocolo.",
        "evidence": "Minuta para revisão humana entregue por e-mail Gmail 19f567c99b0cb4c7, na thread 19f3ed5bdbdcf159, com DOCX e PDF do Memorial Azimut N3 condicionado.",
    },
    "email-corsan-agerst-19f3dc9ff92081cd": {
        "message_id": "19f567d3ac707232",
        "summary": "Diagnóstico interno CORSAN/AGERST N3 enviado ao advogado do caso para revisão humana, em DOCX e PDF.",
        "next": "Etapa de minuta de Igor concluída. A equipe jurídica decide o produto seguinte e obtém as fontes originárias listadas antes de qualquer manifestação externa.",
        "evidence": "Diagnóstico para revisão humana entregue por e-mail Gmail 19f567d3ac707232, na thread 19f3dc9ff92081cd, com DOCX e PDF da reconstrução CORSAN/AGERST N3.",
    },
    "email-natura-cabreuva-19f3991ebc75fe03": {
        "message_id": "19f567dc07e28c44",
        "summary": "Roteiro jurídico interno Natura/Cabreúva N3 enviado ao advogado do caso para revisão humana, em DOCX e PDF.",
        "next": "Etapa de minuta de Igor concluída. O advogado responsável deve lapidar o roteiro e obter o caderno documental antes do parecer conclusivo à cliente.",
        "evidence": "Roteiro para revisão humana entregue por e-mail Gmail 19f567dc07e28c44, na thread 19f3991ebc75fe03, com DOCX e PDF da reconstrução Natura/Cabreúva N3.",
    },
    "email-laudo-pericial-contabil-19f1f9467513bbae": {
        "message_id": "19f567e7d9e1808d",
        "summary": "Parecer técnico-contábil corrigido e enviado a Pedro, com cópia a Fábio, para revisão humana, em DOCX, PDF e pacote de apêndices.",
        "next": "Etapa de minuta de Igor concluída. O advogado e o contador responsável devem lapidar, preencher qualificação profissional e conferir os autos posteriores a 2004 antes de uso processual.",
        "evidence": "Minuta para revisão humana entregue por e-mail Gmail 19f567e7d9e1808d, na thread 19f1f9467513bbae, com DOCX, PDF e pacote de apêndices técnicos.",
    },
}


def main():
    timestamp = now_iso()
    data = read_json(DATA_PATH, {"schema": 1, "demandas": []})
    manual = read_json(MANUAL_PATH, {"schema": 1, "items": {}})
    manual.setdefault("schema", 1)
    manual.setdefault("items", {})

    by_id = {item.get("id"): item for item in data.get("demandas", [])}
    for item_id, delivery in DELIVERIES.items():
        item = by_id.get(item_id)
        if not item:
            raise RuntimeError(f"Demanda não encontrada: {item_id}")
        responses = item.setdefault("emailsResposta", [])
        if delivery["message_id"] not in responses:
            responses.append(delivery["message_id"])

        entry = manual["items"].setdefault(item_id, {"comentarios": [], "overrides": {}})
        entry.setdefault("comentarios", [])
        comment_id = f"entrega-revisao-humana-{delivery['message_id']}"
        if not any(comment.get("id") == comment_id for comment in entry["comentarios"]):
            entry["comentarios"].append(
                {
                    "id": comment_id,
                    "at": timestamp,
                    "tipo": "entrega-email",
                    "texto": delivery["evidence"],
                    "autor": "Igor/Codex",
                }
            )
        entry["overrides"].update(
            {
                "status": "cumprida",
                "respondidoComConteudo": True,
                "evidenciaResposta": delivery["evidence"],
                "evidenciaTipo": "email",
                "resumo": delivery["summary"],
                "proximaAcao": delivery["next"],
            }
        )
        entry["updatedAt"] = timestamp

    data["updatedAt"] = timestamp
    manual["updatedAt"] = timestamp
    atomic_write_json(DATA_PATH, data)
    atomic_write_json(MANUAL_PATH, manual)
    print(json.dumps({"ok": True, "updated": list(DELIVERIES), "at": timestamp}, ensure_ascii=False))


if __name__ == "__main__":
    main()
