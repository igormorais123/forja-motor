# -*- coding: utf-8 -*-
"""forja_conferir_entregas.py — paga a dívida de auditoria das entregas declaradas.

O censo separa `entregue` (artefato em disco) de `entrega_declarada` (localizador
registrado e nunca conferido). A segunda não é dívida de trabalho: alguém
entregou e anotou onde. É dívida de **auditoria** — ninguém foi olhar.

Enquanto ninguém olha, as duas situações se parecem no relatório e a diferença
some. Este programa vai olhar: pega o identificador da mensagem, pergunta à
caixa se ela existe, e guarda o que a caixa respondeu.

**O que a conferência prova, e o que não prova.** Ela prova que existe uma
mensagem com aquele identificador, enviada em tal data, com tal assunto e tais
destinatários. Não prova que o conteúdo era a peça certa, nem que o
destinatário a leu, nem que o trabalho estava bom. Por isso o registro guarda
data, assunto e destinatário: quem lê decide se aquilo é a entrega esperada. Um
programa que respondesse "sim, entregue" e escondesse esses três campos estaria
trocando uma dívida por uma afirmação.

Dialetos que não dá para conferir daqui ficam **declarados como não conferidos**,
com o motivo. `arquivo_em_disco` já nasce conferido, porque o censo só o aceita
depois de achar o arquivo. `whatsapp` não tem rota automática nesta máquina, e
inventar que tem seria pior do que a dívida.

Uso
    python forja_conferir_entregas.py --listar
    python forja_conferir_entregas.py --conferir
    python forja_conferir_entregas.py --conferir --limite 5
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import forja_censo

FORJA = Path(__file__).resolve().parent
LEDGER = FORJA / "state" / "CENSO_CONFERENCIAS.json"
CRED = Path.home() / ".gmail-mcp"
API = "https://gmail.googleapis.com/gmail/v1/users/me"

VERSAO = "FORJA-CONFERENCIA-ENTREGA-v1"

# Por que cada dialeto pode ou não ser conferido daqui. Vocabulário fechado
# pela mesma razão da causa de insumo bloqueado: "não deu" não é diagnóstico.
CONFERIVEL = {
    "gmail": None,
    "arquivo_em_disco": "o censo só aceita o caminho depois de encontrar o arquivo",
    "whatsapp": None,
}
SEM_ROTA = {
    "whatsapp": ("não há rota autenticada para o histórico do WhatsApp nesta "
                 "máquina; conferir exige abrir a conversa"),
}


def _agora() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def _token() -> str:
    chaves = json.loads((CRED / "gcp-oauth.keys.json").read_text(encoding="utf-8"))
    k = chaves.get("installed") or chaves.get("web")
    cr = json.loads((CRED / "credentials.json").read_text(encoding="utf-8"))
    corpo = urllib.parse.urlencode({
        "client_id": k["client_id"], "client_secret": k["client_secret"],
        "refresh_token": cr["refresh_token"], "grant_type": "refresh_token"}).encode()
    req = urllib.request.Request("https://oauth2.googleapis.com/token", data=corpo)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())["access_token"]


def _mensagem(ident: str, tk: str) -> dict:
    """O que a caixa diz sobre esse identificador.

    O identificador pode ser de mensagem ou de fio — o painel registrou os dois
    ao longo do tempo. Tentar só um deles produziria "não existe" para entregas
    que existem, que é o pior resultado possível aqui.
    """
    for recurso in ("messages", "threads"):
        url = f"{API}/{recurso}/{ident}?format=metadata"
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {tk}"})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                d = json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code in (403, 429):
                raise
            continue
        msgs = d.get("messages") or [d]
        primeira = msgs[0]
        cabecalhos = {h["name"]: h["value"]
                      for h in (primeira.get("payload", {}).get("headers") or [])}
        enviada = any("SENT" in (m.get("labelIds") or []) for m in msgs)
        return {
            "existe": True,
            "recurso": recurso,
            "mensagens": len(msgs),
            "enviadaPorNos": enviada,
            "assunto": cabecalhos.get("Subject"),
            "para": cabecalhos.get("To"),
            "de": cabecalhos.get("From"),
            "data": cabecalhos.get("Date"),
        }
    return {"existe": False}


def pendentes() -> list[dict]:
    """Entregas com localizador registrado e ainda não conferidas."""
    ja = carregar()
    dados = forja_censo.censo()
    fila = []
    for c in dados["casos"]:
        if c["situacao"] != "entrega_declarada" or not c.get("localizadorDaEntrega"):
            continue
        if c["caseId"] in ja:
            continue
        fila.append(c)
    return fila


def carregar() -> dict:
    try:
        return json.loads(LEDGER.read_text(encoding="utf-8")).get("casos", {})
    except (OSError, json.JSONDecodeError):
        return {}


def gravar(casos: dict) -> None:
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    LEDGER.write_text(json.dumps(
        {"versao": VERSAO, "atualizadoEm": _agora(), "casos": casos},
        ensure_ascii=False, indent=2), encoding="utf-8")


def conferir(limite: int | None = None) -> dict:
    fila = pendentes()
    if limite:
        fila = fila[:limite]
    casos = carregar()
    tk = None
    resumo = {"conferidos": 0, "ausentes": 0, "sem_rota": 0, "erro": 0}

    for c in fila:
        dialeto = c.get("dialetoDoLocalizador")
        ident = c["localizadorDaEntrega"]
        base = {"conferidoEm": _agora(), "localizador": ident, "dialeto": dialeto}

        if dialeto in SEM_ROTA:
            casos[c["caseId"]] = {**base, "resultado": "sem_rota_automatica",
                                  "motivo": SEM_ROTA[dialeto]}
            resumo["sem_rota"] += 1
            continue
        if dialeto == "arquivo_em_disco":
            casos[c["caseId"]] = {**base, "resultado": "confere",
                                  "motivo": CONFERIVEL["arquivo_em_disco"]}
            resumo["conferidos"] += 1
            continue

        try:
            tk = tk or _token()
            achado = _mensagem(ident, tk)
        except Exception as e:  # rede, cota, credencial vencida
            casos[c["caseId"]] = {**base, "resultado": "nao_foi_possivel_conferir",
                                  "motivo": f"{type(e).__name__}: {str(e)[:140]}"}
            resumo["erro"] += 1
            continue

        if achado.get("existe"):
            casos[c["caseId"]] = {**base, "resultado": "confere", **achado}
            resumo["conferidos"] += 1
        else:
            # Não é o mesmo que "não entregue": o identificador pode estar errado
            # no registro. O que se sabe é que a caixa não o reconhece.
            casos[c["caseId"]] = {**base, "resultado": "nao_encontrado",
                                  "motivo": "a caixa não reconhece este identificador, "
                                            "nem como mensagem nem como fio"}
            resumo["ausentes"] += 1

    gravar(casos)
    return resumo


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--listar", action="store_true")
    p.add_argument("--conferir", action="store_true")
    p.add_argument("--limite", type=int)
    a = p.parse_args(argv)

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    if a.conferir:
        r = conferir(a.limite)
        print(f"conferidas {r['conferidos']} · não encontradas {r['ausentes']} · "
              f"sem rota {r['sem_rota']} · falha de acesso {r['erro']}")
        print(f"registro: {LEDGER.name}")
        return 1 if r["ausentes"] or r["erro"] else 0

    fila = pendentes()
    if not fila:
        print("Nenhuma entrega declarada pendente de conferência.")
        return 0
    for c in fila:
        print(f"  [{c.get('dialetoDoLocalizador')}] {c['caseId']}"
              f"\n      {c['localizadorDaEntrega']}")
    print(f"\n{len(fila)} entrega(s) com localizador e sem conferência.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
