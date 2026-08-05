import json
import re
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
DATA_PATH = ROOT / "data" / "demandas.json"
MANUAL_PATH = ROOT / "data" / "intervencoes_manuais.json"


def now_iso():
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def read_json(path, fallback):
    if not path.exists():
        return fallback
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def safe_folder_name(value):
    text = re.sub(r'[<>:"/\\|?*\x00-\x1f]', " ", value)
    text = re.sub(r"\s+", " ", text).strip(" .")
    return text[:110]


def manual_entry(manual, item_id):
    entry = manual.setdefault("items", {}).setdefault(item_id, {"comentarios": [], "overrides": {}})
    entry.setdefault("comentarios", [])
    entry.setdefault("overrides", {})
    return entry


def add_comment(manual, item_id, text, tipo="audio"):
    entry = manual_entry(manual, item_id)
    if any(c.get("texto") == text for c in entry["comentarios"]):
        return False
    entry["comentarios"].append(
        {
            "id": f"{tipo}-{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
            "at": now_iso(),
            "tipo": tipo,
            "texto": text,
            "autor": "Codex/Hermes",
        }
    )
    entry["updatedAt"] = now_iso()
    return True


def set_override(manual, item_id, **kwargs):
    entry = manual_entry(manual, item_id)
    changed = False
    for key, value in kwargs.items():
        if entry["overrides"].get(key) != value:
            entry["overrides"][key] = value
            changed = True
    if changed:
        entry["updatedAt"] = now_iso()
    return changed


def demand_exists(data, item_id):
    return any(item.get("id") == item_id for item in data.get("demandas", []))


def create_task(data, item):
    if demand_exists(data, item["id"]):
        return False
    folder = WORKSPACE / item["pasta"]
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "COMANDO_MANUAL.md").write_text(
        "# Tarefa originada de áudio/WhatsApp\n\n"
        f"- ID: `{item['id']}`\n"
        f"- Origem: {item['origem']}\n"
        f"- Criada em: {now_iso()}\n"
        f"- Prazo: {item.get('prazo') or 'sem prazo definido'}\n\n"
        "## Resumo operacional\n\n"
        f"{item['resumo']}\n\n"
        "## Próxima ação\n\n"
        f"{item['proximaAcao']}\n\n"
        "## Fonte sanitizada\n\n"
        "Áudios recentes de Fábio Medina Osório no WhatsApp/Hermes. "
        "Este arquivo registra apenas o encaminhamento operacional; a conversa bruta não é exposta no painel.\n",
        encoding="utf-8",
    )
    data.setdefault("demandas", []).append(item)
    return True


def main():
    data = read_json(DATA_PATH, {"schema": 1, "demandas": []})
    manual = read_json(MANUAL_PATH, {"schema": 1, "updatedAt": now_iso(), "items": {}})
    manual.setdefault("schema", 1)
    manual.setdefault("items", {})
    changed = False

    changed |= add_comment(
        manual,
        "email-auto-19f3ea400b7dec3d",
        "Áudios do Fábio em 07/07/2026 indicam que o parecer Deltan deve ser tratado como estudo pro bono, com independência intelectual, avaliação conjunta e diretrizes posteriores do Fábio. Manter como tarefa aberta até receber/organizar essas diretrizes.",
    )

    changed |= add_comment(
        manual,
        "email-auto-19f38f30238ff4d3",
        "Áudio do Fábio em 07/07/2026 informa que o anexo mencionado como 'Dom Prifai/Dom Profai' também integra o contrato. Conferir documento/anexo no WhatsApp antes de fechar a tarefa de contrato social.",
    )

    jalusa_evidence = "Cumprida por WhatsApp em 07/07/2026: documento enviado ao Fábio às 21:21, seguido de explicação de que a peça incorporou elementos úteis da minuta humana e da revisão do processo."
    changed |= set_override(
        manual,
        "email-jalusa-prestes-5000447",
        status="cumprida",
        respondidoComConteudo=True,
        evidenciaResposta=jalusa_evidence,
        prazoTexto="cumprida por entrega via WhatsApp em 07/07/2026",
        proximaAcao="Arquivada como cumprida; manter apenas acompanhamento de eventual retorno do Fábio.",
        urgenciaManual="baixa",
    )
    changed |= add_comment(manual, "email-jalusa-prestes-5000447", jalusa_evidence, tipo="status")

    changed |= add_comment(
        manual,
        "email-cafelana-agint-aresp-2698443-19f2f0876e358eab",
        "Feedback por áudio do Fábio em 07/07/2026: pesquisar o momento de arguição da prevenção e eventual preclusão, considerando subida anterior à Min. Regina Helena; ponderar também a vantagem pragmática da turma atual antes de insistir em prevenção.",
    )

    tasks = [
        {
            "id": "whatsapp-audio-cafelana-prevencao-20260708",
            "titulo": "Cafelana - peça humana e diretrizes de prevenção/preclusão",
            "clienteOuCaso": "Cafelana / STJ",
            "origem": "whatsapp_audio",
            "emailsRecebidos": [],
            "emailsResposta": [],
            "pasta": safe_folder_name("WhatsApp Audio - Cafelana peça humana e prevenção - 2026-07-08"),
            "recebidoEm": "2026-07-07T22:19:34-03:00",
            "prazo": None,
            "prazoTexto": "sem prazo expresso; demanda vinda por áudio do Fábio",
            "resumo": "Fábio indicou que passará uma peça humana da Cafelana para melhoria. Diretriz: pesquisar prevenção/preclusão, especialmente se o momento de arguir prevenção já passou, e avaliar a estratégia diante da turma atual.",
            "proximaAcao": "Aguardar ou localizar a peça humana prometida, conferir autos/STJ, pesquisar prevenção/preclusão e incorporar a diretriz sem reabrir o que já foi entregue se for apenas aprendizado.",
            "status": "aberta",
            "respondidoComConteudo": False,
            "evidenciaResposta": "",
            "urgenciaManual": "alta",
            "anexos": {
                "diretosBaixados": None,
                "diretosEsperados": None,
                "externosPendentes": True,
                "observacao": "Fonte por áudio/WhatsApp; verificar se a peça humana foi enviada depois.",
            },
            "tags": ["WhatsApp", "áudio", "Cafelana", "STJ", "prevenção"],
            "manualSource": {
                "audioMessageIds": [
                    "3A24F98D2F1C5198942B",
                    "3A5A2F26E1DC3CE81D6E",
                    "3A52F917BB8C60B4D685",
                    "3ACA4828B944F115F46B",
                ],
                "transcriptBatch": "/root/.hermes/state/office-demand-audio-intake/whisper-20260708-fabio-recent",
            },
        },
        {
            "id": "whatsapp-audio-roraima-senador-20260708",
            "titulo": "Roraima / Senador Chico Rodrigues - estruturar possível cliente",
            "clienteOuCaso": "Roraima / Senador Chico Rodrigues",
            "origem": "whatsapp_audio",
            "emailsRecebidos": [],
            "emailsResposta": [],
            "pasta": safe_folder_name("WhatsApp Audio - Roraima Senador cliente - 2026-07-08"),
            "recebidoEm": "2026-07-07T21:24:58-03:00",
            "prazo": None,
            "prazoTexto": "sem prazo expresso; tarefa de desenvolvimento de cliente",
            "resumo": "Fábio tratou o contato de Roraima/Senador como possível cliente a estruturar no modelo do escritório, com responsabilidade do Igor e apoio do escritório em precificação e formatação do produto.",
            "proximaAcao": "Definir quem é o decisor, qual problema jurídico-político será vendido, produto, entregáveis, faixa de honorários e próximos passos de abordagem.",
            "status": "aberta",
            "respondidoComConteudo": False,
            "evidenciaResposta": "",
            "urgenciaManual": "media",
            "anexos": {
                "diretosBaixados": None,
                "diretosEsperados": None,
                "externosPendentes": True,
                "observacao": "Tarefa não processual; veio por áudio/WhatsApp.",
            },
            "tags": ["WhatsApp", "áudio", "cliente", "Roraima", "prospecção"],
            "manualSource": {
                "audioMessageIds": [
                    "3AB6B37BAA79A166F35E",
                    "3AF298083A7BB162516A",
                    "3A0BD45AA1A0286BBC2E",
                ],
                "transcriptBatch": "/root/.hermes/state/office-demand-audio-intake/whisper-20260708-fabio-recent",
            },
        },
        {
            "id": "whatsapp-audio-protocolo-aprendizados-20260708",
            "titulo": "Sistema de petições - transformar erros e feedbacks em protocolos",
            "clienteOuCaso": "Gestão interna / IA do escritório",
            "origem": "whatsapp_audio",
            "emailsRecebidos": [],
            "emailsResposta": [],
            "pasta": safe_folder_name("WhatsApp Audio - Protocolo de aprendizados IA - 2026-07-08"),
            "recebidoEm": "2026-07-07T22:35:32-03:00",
            "prazo": None,
            "prazoTexto": "sem prazo expresso; melhoria contínua do sistema",
            "resumo": "Fábio reforçou que cada trabalho, erro, problema detectado e feedback prático deve virar protocolo/diretriz para a IA do escritório, preservando supervisão humana e contexto estratégico.",
            "proximaAcao": "Criar rotina de pós-entrega por caso: registrar feedback, atualizar protocolo, marcar o que a IA não viu e vincular aprendizado ao painel da demanda.",
            "status": "aberta",
            "respondidoComConteudo": False,
            "evidenciaResposta": "",
            "urgenciaManual": "media",
            "anexos": {
                "diretosBaixados": None,
                "diretosEsperados": None,
                "externosPendentes": False,
                "observacao": "Tarefa interna de melhoria do sistema.",
            },
            "tags": ["WhatsApp", "áudio", "aprendizado", "protocolo", "IA"],
            "manualSource": {
                "audioMessageIds": [
                    "3A0EB7ED43FB703C8D67",
                    "3AD9837CCDEB1006DC5C",
                    "3A8C389E29D3036A4E69",
                    "3ABF37BA0BAE447B7B88",
                ],
                "transcriptBatch": "/root/.hermes/state/office-demand-audio-intake/whisper-20260708-fabio-recent",
            },
        },
    ]

    for task in tasks:
        if create_task(data, task):
            changed = True
            add_comment(manual, task["id"], "Criada a partir de transcrição sanitizada dos áudios do Fábio de 07/07/2026.", tipo="criacao")

    data["updatedAt"] = now_iso()
    manual["updatedAt"] = now_iso()
    write_json(DATA_PATH, data)
    write_json(MANUAL_PATH, manual)
    print(json.dumps({"ok": True, "changed": changed, "demands": len(data.get("demandas", [])), "manualItems": len(manual.get("items", {}))}, ensure_ascii=False))


if __name__ == "__main__":
    main()
