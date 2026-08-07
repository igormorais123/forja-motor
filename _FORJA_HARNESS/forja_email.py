"""forja_email.py — envio real de e-mail pela FORJA.

Existe porque a esteira sabia redigir e deixar o rascunho pronto, mas não sabia
entregar: o conector do Gmail disponível ao agente expõe `create_draft`,
`update_draft` e leitura, e **não expõe `send`**. Um sistema que produz a peça e
para na véspera do envio transfere ao humano justamente a etapa mecânica.

Autenticação: reaproveita o token OAuth já existente em
``%USERPROFILE%\\.secrets\\gmail_organizer_token.pickle``, cujo escopo é
``gmail.modify`` — que abrange ``users.messages.send`` e ``users.drafts.send``.
Nenhuma credencial nova é criada, nada é impresso e o token renovado é gravado
de volta no mesmo arquivo.

Preferimos **enviar o rascunho existente** (`drafts.send`) a montar a mensagem do
zero. O rascunho é o que o humano revisou; enviar outra coisa, ainda que com o
mesmo texto, quebraria a correspondência entre o que foi aprovado e o que saiu.

Uso:
    python forja_email.py --listar
    python forja_email.py --enviar-rascunho <draftId>
    python forja_email.py --enviar-rascunho <draftId> --confirmar

Sem ``--confirmar`` o comando roda em ensaio: mostra destinatário, assunto e
tamanho, e não envia nada. Envio é irreversível e não deve acontecer por
digitação distraída.
"""

from __future__ import annotations

import argparse
import base64
import json
import pickle
import sys
from datetime import datetime
from pathlib import Path

TOKEN = Path.home() / ".secrets" / "gmail_organizer_token.pickle"
LEDGER_ENVIOS = Path(__file__).resolve().parent / "telemetria" / "ENVIOS_EMAIL.jsonl"


def _servico():
    """Carrega o token, renova se preciso e devolve o cliente do Gmail."""
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build

    if not TOKEN.is_file():
        raise SystemExit(f"token ausente: {TOKEN}")
    with TOKEN.open("rb") as fh:
        cred = pickle.load(fh)

    if not cred.valid:
        if not (cred.expired and cred.refresh_token):
            raise SystemExit("token inválido e sem refresh_token — reautorize o app do Gmail")
        cred.refresh(Request())
        # Grava o token renovado para que a próxima execução não precise da rede
        # só para descobrir que expirou de novo.
        with TOKEN.open("wb") as fh:
            pickle.dump(cred, fh)

    return build("gmail", "v1", credentials=cred, cache_discovery=False)


def _cabecalho(msg: dict, nome: str) -> str:
    for h in (msg.get("payload") or {}).get("headers") or []:
        if h.get("name", "").lower() == nome.lower():
            return h.get("value", "")
    return ""


def listar(svc, limite: int = 10) -> int:
    resp = svc.users().drafts().list(userId="me", maxResults=limite).execute()
    rascunhos = resp.get("drafts") or []
    if not rascunhos:
        print("nenhum rascunho")
        return 0
    for d in rascunhos:
        det = svc.users().drafts().get(userId="me", id=d["id"], format="metadata").execute()
        msg = det.get("message") or {}
        print(f"{d['id']}")
        print(f"   para:    {_cabecalho(msg, 'To')}")
        print(f"   assunto: {_cabecalho(msg, 'Subject')[:88]}")
        print(f"   thread:  {msg.get('threadId')}")
    return 0


def criar_rascunho(svc, *, para, assunto, corpo, anexos=(), responder_a=None) -> str:
    """Compõe um rascunho com anexos e devolve o draftId.

    Existia um vão entre produzir e entregar: a esteira sabia disparar o
    rascunho pronto, e não sabia montar rascunho que levasse o arquivo que ela
    mesma acabara de compor. Quem quisesse anexar precisava fazê-lo à mão no
    Gmail, o que tira o envio da rota onde a barreira de anexo está instalada.

    O rascunho é criado, não enviado. Quem envia é `enviar_rascunho`, que roda
    a conferência do padrão da casa antes de qualquer coisa sair.
    """
    import mimetypes
    from email.message import EmailMessage

    msg = EmailMessage()
    msg["To"] = ", ".join(para)
    msg["Subject"] = assunto
    msg.set_content(corpo)

    for caminho in anexos:
        caminho = Path(caminho)
        if not caminho.is_file():
            raise SystemExit(f"anexo inexistente: {caminho}")
        tipo, _ = mimetypes.guess_type(caminho.name)
        principal, _, secundario = (tipo or "application/octet-stream").partition("/")
        msg.add_attachment(caminho.read_bytes(), maintype=principal,
                           subtype=secundario or "octet-stream",
                           filename=caminho.name)

    corpo_api = {"message": {"raw": base64.urlsafe_b64encode(msg.as_bytes()).decode()}}
    if responder_a:
        # Sem o threadId a resposta vira mensagem solta e o destinatário
        # reconstrói o contexto na mão.
        original = svc.users().messages().get(userId="me", id=responder_a,
                                              format="metadata").execute()
        corpo_api["message"]["threadId"] = original.get("threadId")
        assunto_original = _cabecalho(original, "Subject")
        if assunto_original and not assunto.lower().startswith("re:"):
            msg.replace_header("Subject", f"Re: {assunto_original}")
            corpo_api["message"]["raw"] = base64.urlsafe_b64encode(msg.as_bytes()).decode()

    criado = svc.users().drafts().create(userId="me", body=corpo_api).execute()
    return criado["id"]


def _registrar(evento: dict) -> None:
    """Trilha de envio. Sem isto, 'a FORJA enviou' seria narrativa, não evidência."""
    LEDGER_ENVIOS.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER_ENVIOS.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(evento, ensure_ascii=False) + "\n")


def enviar_rascunho(svc, draft_id: str, confirmar: bool, terceiro=None) -> int:
    det = svc.users().drafts().get(userId="me", id=draft_id, format="full").execute()
    msg = det.get("message") or {}
    para = _cabecalho(msg, "To")
    assunto = _cabecalho(msg, "Subject")
    corpo = msg.get("snippet", "")

    print(f"rascunho: {draft_id}")
    print(f"para:     {para}")
    print(f"assunto:  {assunto}")
    print(f"thread:   {msg.get('threadId')}")
    print(f"trecho:   {corpo[:160]}")

    # A conferência roda TAMBÉM no ensaio: descobrir que o anexo está fora do
    # padrão só na hora de confirmar é descobrir tarde, e o ensaio existe
    # justamente para mostrar o que aconteceria.
    import forja_gate_anexo_saida as gate

    veredito = gate.avaliar_rascunho(svc, draft_id, material_de_terceiro=terceiro)
    for m in veredito["medidos"]:
        print(f"anexo:    {m['arquivo'][:52]:54} just {m['justificacao']:.0%}  "
              f"tam {m['tamanho']:.0%}  fonte {m['fonte']:.0%}")
    for c in veredito.get("naoInspecionados") or []:
        # Não barra, mas quem envia precisa ver: este saiu sem conferência.
        print(f"cego:     {c['arquivo'][:52]:54} {c['motivo']}")
    if not veredito["aprovado"]:
        print()
        print(gate.explicar(veredito))
        _registrar({"em": datetime.now().astimezone().isoformat(timespec="seconds"),
                    "evento": "envio_barrado_por_anexo", "draftId": draft_id,
                    "arquivos": [m["arquivo"] for m in veredito["bloqueados"]]})
        return 1

    if not confirmar:
        print("\nENSAIO — nada foi enviado. Repita com --confirmar para enviar de verdade.")
        return 0

    enviado = svc.users().drafts().send(userId="me", body={"id": draft_id}).execute()
    evento = {
        "em": datetime.now().astimezone().isoformat(timespec="seconds"),
        "draftId": draft_id,
        "messageId": enviado.get("id"),
        "threadId": enviado.get("threadId"),
        "para": para,
        "assunto": assunto,
    }
    _registrar(evento)
    print(f"\nENVIADO. messageId={enviado.get('id')} threadId={enviado.get('threadId')}")
    print(f"registro: {LEDGER_ENVIOS.name}")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Envio de e-mail da FORJA (Gmail OAuth existente).")
    ap.add_argument("--listar", action="store_true", help="lista rascunhos com destinatário e assunto")
    ap.add_argument("--enviar-rascunho", metavar="DRAFT_ID", help="envia um rascunho já composto")
    ap.add_argument("--confirmar", action="store_true", help="sai do ensaio e envia de fato")
    ap.add_argument("--material-de-terceiro", action="append", default=[], metavar="ARQUIVO",
                    help="nome de anexo redigido fora do escritório, a encaminhar como veio; "
                         "repetível. Sem isto, anexo fora do padrão da casa barra o envio")
    ap.add_argument("--criar-rascunho", action="store_true",
                    help="compõe um rascunho com anexos e imprime o draftId; não envia")
    ap.add_argument("--para", action="append", default=[], metavar="ENDERECO")
    ap.add_argument("--assunto")
    ap.add_argument("--corpo-arquivo", metavar="ARQUIVO",
                    help="arquivo de texto com o corpo da mensagem")
    ap.add_argument("--anexo", action="append", default=[], metavar="ARQUIVO")
    ap.add_argument("--responder-a", metavar="MESSAGE_ID")
    args = ap.parse_args(argv)

    if not args.listar and not args.enviar_rascunho and not args.criar_rascunho:
        ap.print_help()
        return 2

    svc = _servico()
    if args.criar_rascunho:
        if not (args.para and args.assunto and args.corpo_arquivo):
            raise SystemExit("--criar-rascunho exige --para, --assunto e --corpo-arquivo")
        draft_id = criar_rascunho(
            svc, para=args.para, assunto=args.assunto,
            corpo=Path(args.corpo_arquivo).read_text(encoding="utf-8"),
            anexos=args.anexo, responder_a=args.responder_a)
        print(draft_id)
        return 0
    if args.listar:
        return listar(svc)
    return enviar_rascunho(svc, args.enviar_rascunho, args.confirmar,
                           terceiro=args.material_de_terceiro)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main(sys.argv[1:]))
