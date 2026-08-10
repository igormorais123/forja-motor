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
import hashlib
import json
import mimetypes
import sys
from email.message import EmailMessage
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ))

PROTOCOLO = "2025-06-18"
VERSAO = "1.1.0"

# O Gmail aceita 25 MB de anexo. O corpo vai em base64, que infla um terço, e a
# mensagem carrega cabeçalhos: o teto útil fica abaixo do anunciado. Cortar aqui,
# com o número na mensagem de erro, é melhor que descobrir pela recusa da API
# depois de montar tudo.
TETO_ANEXOS_BYTES = 18 * 1024 * 1024


def _servico():
    from forja_email import _servico as servico_gmail
    return servico_gmail()


def _registrar(evento: dict) -> None:
    from forja_email import _registrar as registrar
    registrar(evento)


# ---------------------------------------------------------------------------
# Ferramentas
# ---------------------------------------------------------------------------

def _anotar_veredito(veredito: dict, contexto: dict) -> None:
    """Grava na trilha o que o gate viu — o que barrou, o que não conseguiu ver.

    Compartilhado pelas duas saídas. Enquanto só o rascunho anexava, esta lógica
    vivia dentro dele; ao abrir a segunda porta, duplicá-la garantiria que uma
    delas passasse a registrar menos que a outra em algumas semanas.
    """
    import forja_gate_anexo_saida as gate

    if not veredito["aprovado"]:
        _registrar({**contexto, "evento": "envio_barrado_por_anexo",
                    "arquivos": [m["arquivo"] for m in veredito["bloqueados"]]})
        raise ValueError(gate.explicar(veredito))
    if veredito.get("naoInspecionados"):
        # Ponto cego declarado: o anexo saiu sem passar pela conferência. Não
        # barra — ausência de medida nunca foi prova de desvio —, mas fica na
        # trilha, porque barreira com ponto cego invisível é pior que barreira
        # nenhuma: ninguém sabe o que ela não viu.
        _registrar({**contexto, "evento": "anexo_nao_inspecionado",
                    "itens": veredito["naoInspecionados"]})
    if veredito["liberadosPorDeclaracao"]:
        # Passar por declaração é decisão de quem envia, e fica na trilha: sem
        # o registro, a exceção vira o caminho normal em duas semanas.
        _registrar({**contexto, "evento": "anexo_liberado_por_declaracao",
                    "arquivos": [m["arquivo"] for m in veredito["liberadosPorDeclaracao"]]})


def _preparar_anexos(anexos, material_de_terceiro, contexto):
    """Resolve os caminhos, submete ao gate da casa e devolve o que anexar.

    Devolve uma lista de `(Path, bytes, sha256)`. O hash existe para o ledger:
    ele registra QUAL arquivo saiu sem guardar o arquivo, que é a mesma regra
    do loop pós-protocolo.
    """
    import forja_gate_anexo_saida as gate

    caminhos, ausentes = [], []
    for bruto in anexos:
        p = Path(str(bruto)).expanduser()
        (caminhos if p.is_file() else ausentes).append(p)
    if ausentes:
        # Anexo que não existe é erro de quem chamou, e precisa ser dito pelo
        # nome. Enviar o e-mail sem ele seria pior: o destinatário recebe uma
        # mensagem que promete um documento que não vai junto.
        raise ValueError("anexo não encontrado no disco: "
                         + "; ".join(str(p) for p in ausentes))

    total = sum(p.stat().st_size for p in caminhos)
    if total > TETO_ANEXOS_BYTES:
        raise ValueError(
            f"anexos somam {total/1048576:.1f} MB e o teto é "
            f"{TETO_ANEXOS_BYTES/1048576:.0f} MB — divida o envio ou mande o PDF sem o DOCX")

    _anotar_veredito(gate.avaliar(caminhos, material_de_terceiro=material_de_terceiro),
                     contexto)

    preparados = []
    for p in caminhos:
        dados = p.read_bytes()
        preparados.append((p, dados, hashlib.sha256(dados).hexdigest()))
    return preparados


def enviar_email(to, subject, body, cc=None, bcc=None, reply_to_message_id=None,
                 anexos=None, material_de_terceiro=None):
    """Compõe e envia, com ou sem anexo. Devolve messageId e threadId da API."""
    if not to:
        raise ValueError("destinatário ausente")
    svc = _servico()

    preparados = []
    if anexos:
        preparados = _preparar_anexos(anexos, material_de_terceiro,
                                      {"para": to, "assunto": subject})

    msg = EmailMessage()
    msg["To"] = ", ".join(to)
    if cc:
        msg["Cc"] = ", ".join(cc)
    if bcc:
        msg["Bcc"] = ", ".join(bcc)
    msg["Subject"] = subject or ""
    msg.set_content(body or "")

    for caminho, dados, _hash in preparados:
        tipo, _ = mimetypes.guess_type(caminho.name)
        principal, _, secundario = (tipo or "application/octet-stream").partition("/")
        msg.add_attachment(dados, maintype=principal,
                           subtype=secundario or "octet-stream",
                           filename=caminho.name)

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
        # Nome, tamanho e hash. Nunca o conteúdo: o documento vive na pasta do
        # caso e na caixa de saída, e o ledger existe para dizer QUAL saiu.
        "anexos": [{"arquivo": c.name, "bytes": len(d), "sha256": h}
                   for c, d, h in preparados],
    })
    return {"messageId": enviado.get("id"), "threadId": enviado.get("threadId"),
            "para": to, "assunto": subject,
            "anexos": [c.name for c, _d, _h in preparados]}


def enviar_rascunho(draft_id, material_de_terceiro=None):
    """Envia um rascunho já revisado, preservando o texto exato aprovado.

    Até 10/08/2026 esta era a **única** saída da FORJA por onde um documento
    efetivamente saía, porque o `enviar_email` montava só corpo. O efeito prático
    apareceu quando havia seis arquivos prontos para o titular e a esteira não
    tinha como despachá-los: capacidade que só existe por um caminho estreito é
    capacidade que falta na hora em que se precisa dela. Hoje as duas portas
    anexam, e **as duas passam pelo mesmo gate** — foi por aqui que, em
    06/08/2026, dois documentos fora do padrão da casa seguiram para o cliente,
    e abrir a segunda porta sem a mesma barreira teria reaberto exatamente esse
    buraco.
    """
    import forja_gate_anexo_saida as gate

    svc = _servico()
    veredito = gate.avaliar_rascunho(svc, draft_id,
                                     material_de_terceiro=material_de_terceiro)
    _anotar_veredito(veredito, {"draftId": draft_id})
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
            "Envia um e-mail de verdade pela conta do Igor, COM OU SEM ANEXO. "
            "IRREVERSÍVEL — não há desfazer. Use quando o envio já estiver "
            "autorizado. Para anexar, passe os caminhos em `anexos`: a ferramenta "
            "lê os arquivos do disco e os embarca na mensagem, então NÃO existe "
            "razão para prometer um documento no corpo e mandar só o texto. "
            "Anexo .docx fora do padrão Word do escritório nas três dimensões "
            "barra o envio inteiro; material redigido fora da casa passa quando "
            "declarado nominalmente em `material_de_terceiro`. Para responder "
            "dentro de uma conversa existente, informe reply_to_message_id: e-mail "
            "solto sobre assunto em curso obriga o destinatário a reconstruir "
            "contexto. Todo envio fica registrado em telemetria/ENVIOS_EMAIL.jsonl, "
            "com nome, tamanho e hash de cada anexo — nunca o conteúdo."
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
                "anexos": {
                    "type": "array", "items": {"type": "string"},
                    "description": "caminhos de arquivo no disco. Absolutos de "
                                   "preferência. Teto de 18 MB somados."},
                "material_de_terceiro": {
                    "type": "array", "items": {"type": "string"},
                    "description": "nomes de arquivo redigidos fora do escritório, "
                                   "que devem ser encaminhados como vieram e por "
                                   "isso não respondem ao padrão da casa",
                },
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
        reply_to_message_id=a.get("reply_to_message_id"),
        anexos=a.get("anexos"),
        material_de_terceiro=a.get("material_de_terceiro")),
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
