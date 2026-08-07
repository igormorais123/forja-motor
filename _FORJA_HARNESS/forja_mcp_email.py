#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""forja_mcp_email.py — servidor MCP que dá ao agente a ferramenta de ENVIAR.

Por que existe. O conector do Gmail do claude.ai expõe `create_draft`,
`update_draft` e leitura, e **não expõe envio**. A superfície desse conector é
definida do lado do provedor e não é editável daqui. O resultado prático era que
a esteira redigia, deixava o rascunho pronto e parava na véspera — devolvendo ao
humano justamente a etapa mecânica, que é o oposto do que a FORJA existe para
fazer. Ordem do Igor em 05/08/2026, textual: *"a FORJA tem que poder mandar
e-mail, que é para isso que ela serve"*.

`forja_email.py` já resolvia isso por linha de comando. Este módulo dá o passo
que faltava: transforma a capacidade em **ferramenta**, para que enviar deixe de
depender de o agente lembrar que existe um script e passe a estar no mesmo lugar
onde ele procura tudo o mais.

Autenticação e ledger são os do `forja_email.py`, deliberadamente: um único
caminho de credencial, um único registro de envio. Nenhum token novo, nenhum
segredo impresso.

Protocolo MCP implementado em JSON-RPC cru sobre stdin/stdout, sem dependência
de biblioteca. São três métodos e cabem numa tela; puxar um pacote para isso
acrescentaria superfície de manutenção sem acrescentar capacidade.

Registro em `.claude.json`:

    "forja-email": {
      "type": "stdio",
      "command": "python",
      "args": ["<caminho>/forja_mcp_email.py"]
    }
"""
from __future__ import annotations

import base64
import json
import sys
from email.message import EmailMessage
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ))

PROTOCOLO = "2025-06-18"
VERSAO = "1.0.0"


def _servico():
    from forja_email import _servico as servico_gmail
    return servico_gmail()


def _registrar(evento: dict) -> None:
    from forja_email import _registrar as registrar
    registrar(evento)


# ---------------------------------------------------------------------------
# Ferramentas
# ---------------------------------------------------------------------------

def enviar_email(to, subject, body, cc=None, bcc=None, reply_to_message_id=None):
    """Compõe e envia. Devolve messageId e threadId reais da API."""
    if not to:
        raise ValueError("destinatário ausente")
    svc = _servico()

    msg = EmailMessage()
    msg["To"] = ", ".join(to)
    if cc:
        msg["Cc"] = ", ".join(cc)
    if bcc:
        msg["Bcc"] = ", ".join(bcc)
    msg["Subject"] = subject or ""
    msg.set_content(body or "")

    corpo = {"raw": base64.urlsafe_b64encode(msg.as_bytes()).decode("ascii")}

    # Responder no fio existente é o padrão: e-mail solto sobre assunto em curso
    # obriga o destinatário a reconstruir o contexto que já estava montado.
    if reply_to_message_id:
        try:
            original = svc.users().messages().get(
                userId="me", id=reply_to_message_id, format="metadata",
                metadataHeaders=["Message-ID", "References", "Subject"]).execute()
            corpo["threadId"] = original.get("threadId")
            cabecalhos = {h["name"].lower(): h["value"]
                          for h in original.get("payload", {}).get("headers", [])}
            ident = cabecalhos.get("message-id")
            if ident:
                msg["In-Reply-To"] = ident
                msg["References"] = (cabecalhos.get("references", "") + " " + ident).strip()
                corpo["raw"] = base64.urlsafe_b64encode(msg.as_bytes()).decode("ascii")
        except Exception as erro:  # noqa: BLE001
            # Falhar em achar o fio não pode impedir o envio, mas também não pode
            # passar em silêncio: quem lê o ledger precisa saber que saiu solto.
            _registrar({"evento": "fio_nao_resolvido", "messageId": reply_to_message_id,
                        "erro": f"{type(erro).__name__}: {erro}"})

    enviado = svc.users().messages().send(userId="me", body=corpo).execute()
    _registrar({
        "evento": "enviado_por_mcp", "para": to, "cc": cc or [],
        "assunto": subject, "messageId": enviado.get("id"),
        "threadId": enviado.get("threadId"), "caracteres": len(body or ""),
    })
    return {"messageId": enviado.get("id"), "threadId": enviado.get("threadId"),
            "para": to, "assunto": subject}


def enviar_rascunho(draft_id, material_de_terceiro=None):
    """Envia um rascunho já revisado, preservando o texto exato aprovado.

    Esta é a única saída da FORJA por onde um documento efetivamente sai: o
    `enviar_email` monta só corpo. Até 06/08/2026 ela despachava o que estivesse
    anexado sem olhar uma vez, e foi por aqui que dois documentos fora do padrão
    da casa seguiram para o cliente.
    """
    import forja_gate_anexo_saida as gate

    svc = _servico()
    veredito = gate.avaliar_rascunho(svc, draft_id,
                                     material_de_terceiro=material_de_terceiro)
    if not veredito["aprovado"]:
        _registrar({"evento": "envio_barrado_por_anexo", "draftId": draft_id,
                    "arquivos": [m["arquivo"] for m in veredito["bloqueados"]]})
        raise ValueError(gate.explicar(veredito))
    if veredito.get("naoInspecionados"):
        # Ponto cego declarado: o anexo saiu sem passar pela conferência. Não
        # barra — ausência de medida nunca foi prova de desvio —, mas fica na
        # trilha, porque barreira com ponto cego invisível é pior que barreira
        # nenhuma: ninguém sabe o que ela não viu.
        _registrar({"evento": "anexo_nao_inspecionado", "draftId": draft_id,
                    "itens": veredito["naoInspecionados"]})
    if veredito["liberadosPorDeclaracao"]:
        # Passar por declaração é decisão de quem envia, e fica na trilha: sem
        # o registro, a exceção vira o caminho normal em duas semanas.
        _registrar({"evento": "anexo_liberado_por_declaracao", "draftId": draft_id,
                    "arquivos": [m["arquivo"] for m in veredito["liberadosPorDeclaracao"]]})
    enviado = svc.users().drafts().send(userId="me", body={"id": draft_id}).execute()
    _registrar({"evento": "rascunho_enviado_por_mcp", "draftId": draft_id,
                "messageId": enviado.get("id"), "threadId": enviado.get("threadId")})
    return {"messageId": enviado.get("id"), "threadId": enviado.get("threadId"),
            "draftId": draft_id}


def listar_rascunhos(limite=10):
    svc = _servico()
    from forja_email import _cabecalho
    itens = svc.users().drafts().list(userId="me", maxResults=int(limite)).execute()
    saida = []
    for item in itens.get("drafts", []):
        detalhe = svc.users().drafts().get(
            userId="me", id=item["id"], format="metadata").execute()
        msg = detalhe.get("message", {})
        saida.append({"draftId": item["id"],
                      "para": _cabecalho(msg, "To"),
                      "assunto": _cabecalho(msg, "Subject")})
    return {"rascunhos": saida}


FERRAMENTAS = [
    {
        "name": "enviar_email",
        "description": (
            "Envia um e-mail de verdade pela conta do Igor. IRREVERSÍVEL — não há "
            "desfazer. Use quando o envio já estiver autorizado. Para responder "
            "dentro de uma conversa existente, informe reply_to_message_id: e-mail "
            "solto sobre assunto em curso obriga o destinatário a reconstruir "
            "contexto. Todo envio fica registrado em telemetria/ENVIOS_EMAIL.jsonl."
        ),
        "inputSchema": {
            "type": "object",
            "required": ["to", "subject", "body"],
            "properties": {
                "to": {"type": "array", "items": {"type": "string"},
                       "description": "endereços simples, sem 'Nome <...>'"},
                "cc": {"type": "array", "items": {"type": "string"}},
                "bcc": {"type": "array", "items": {"type": "string"}},
                "subject": {"type": "string"},
                "body": {"type": "string", "description": "texto simples"},
                "reply_to_message_id": {
                    "type": "string",
                    "description": "id da mensagem a responder, para manter o fio"},
            },
        },
    },
    {
        "name": "enviar_rascunho",
        "description": (
            "Envia um rascunho existente, preservando exatamente o texto revisado. "
            "Prefira este caminho quando o rascunho já passou por revisão humana: "
            "remontar a mensagem quebraria a correspondência entre o que foi "
            "aprovado e o que saiu. IRREVERSÍVEL. Anexo .docx fora do padrão Word "
            "do escritório nas três dimensões barra o envio; material redigido "
            "fora da casa passa quando declarado nominalmente."
        ),
        "inputSchema": {
            "type": "object", "required": ["draft_id"],
            "properties": {
                "draft_id": {"type": "string"},
                "material_de_terceiro": {
                    "type": "array", "items": {"type": "string"},
                    "description": "nomes de arquivo redigidos fora do escritório, "
                                   "que devem ser encaminhados como vieram",
                },
            },
        },
    },
    {
        "name": "listar_rascunhos",
        "description": "Lista rascunhos com destinatário e assunto. Não envia nada.",
        "inputSchema": {
            "type": "object",
            "properties": {"limite": {"type": "integer", "default": 10}},
        },
    },
]

EXECUTORES = {
    "enviar_email": lambda a: enviar_email(
        a.get("to"), a.get("subject"), a.get("body"),
        cc=a.get("cc"), bcc=a.get("bcc"),
        reply_to_message_id=a.get("reply_to_message_id")),
    "enviar_rascunho": lambda a: enviar_rascunho(
        a.get("draft_id"), material_de_terceiro=a.get("material_de_terceiro")),
    "listar_rascunhos": lambda a: listar_rascunhos(a.get("limite", 10)),
}


# ---------------------------------------------------------------------------
# JSON-RPC sobre stdin/stdout
# ---------------------------------------------------------------------------

def _responder(ident, resultado=None, erro=None) -> None:
    if ident is None:  # notificação não recebe resposta
        return
    msg = {"jsonrpc": "2.0", "id": ident}
    msg["error" if erro else "result"] = erro or resultado
    sys.stdout.write(json.dumps(msg, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def _tratar(pedido: dict) -> None:
    metodo = pedido.get("method")
    ident = pedido.get("id")
    params = pedido.get("params") or {}

    if metodo == "initialize":
        _responder(ident, {
            "protocolVersion": PROTOCOLO,
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "forja-email", "version": VERSAO},
        })
    elif metodo == "tools/list":
        _responder(ident, {"tools": FERRAMENTAS})
    elif metodo == "tools/call":
        nome = params.get("name")
        executor = EXECUTORES.get(nome)
        if not executor:
            _responder(ident, erro={"code": -32601, "message": f"ferramenta desconhecida: {nome}"})
            return
        try:
            saida = executor(params.get("arguments") or {})
            texto = json.dumps(saida, ensure_ascii=False, indent=1)
            _responder(ident, {"content": [{"type": "text", "text": texto}]})
        except Exception as erro:  # noqa: BLE001
            # Erro de envio volta como conteúdo com isError, e não como falha de
            # protocolo: o agente precisa LER o motivo para decidir o que fazer.
            _responder(ident, {
                "content": [{"type": "text",
                             "text": f"falhou: {type(erro).__name__}: {erro}"}],
                "isError": True,
            })
    elif metodo in ("notifications/initialized", "notifications/cancelled"):
        return
    elif metodo == "ping":
        _responder(ident, {})
    else:
        _responder(ident, erro={"code": -32601, "message": f"método não suportado: {metodo}"})


def main() -> int:
    for linha in sys.stdin:
        linha = linha.strip()
        if not linha:
            continue
        try:
            pedido = json.loads(linha)
        except json.JSONDecodeError:
            continue
        try:
            _tratar(pedido)
        except Exception as erro:  # noqa: BLE001
            _responder(pedido.get("id"), erro={"code": -32603, "message": str(erro)})
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    raise SystemExit(main())
