# -*- coding: utf-8 -*-
"""Fios de e-mail em que a última palavra não é minha.

Existe porque em 06/08/2026 a varredura de fim de trabalho deu tudo verde —
baseline, fronteira, painel de demandas, nenhuma flag na raiz — enquanto dois
retornos do escritório de 05/08 esperavam resposta, um deles com uma promessa
minha por escrito. Nenhum dos quatro instrumentos enxergava isso, porque a
demanda que os originou já constava cumprida: a peça foi entregue. O retorno
sobre a entrega abre trabalho novo que o painel registra como o mesmo item
fechado.

A regra que este módulo materializa: **entrega feita não fecha o fio**. Enquanto
houver mensagem do escritório posterior à última resposta minha em qualquer
thread, há trabalho aberto, seja qual for a cor da demanda no painel.

Os remetentes vigiados NÃO moram aqui. Endereço de escritório é dado de cliente
e este arquivo pertence ao motor. Eles ficam em `state/ACERVO_VALORES.json`, sob
a chave `fios_remetentes_casa`, e sem o acervo este módulo roda sem alvo e diz
que rodou assim.

    "fios_remetentes_casa": ["exemplo.adv.br", "fulano@gmail.com"]

Credenciais: reaproveita o OAuth já autorizado em `~/.gmail-mcp`, o mesmo que o
`hermes_email.py` usa. Nada é enviado — este módulo só lê.

Uso
    python forja_fios_abertos.py
    python forja_fios_abertos.py --dias 30
    python forja_fios_abertos.py --json

Saída
    Código 0 sem fio aberto, 10 com fio aberto, 1 em erro, 2 sem alvo.
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

import forja_acervo

CRED = Path.home() / ".gmail-mcp"
API = "https://gmail.googleapis.com/gmail/v1/users/me"


def remetentes() -> list:
    """Os endereços cuja mensagem sem resposta conta como trabalho aberto."""
    return forja_acervo.valor("fios_remetentes_casa", []) or []


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


def _pegar(url: str, tk: str) -> dict:
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {tk}"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.loads(r.read().decode("utf-8"))


def abertos(alvos: list, dias: int = 20) -> list:
    """Fios com mensagem da casa posterior à minha última resposta."""
    tk = _token()
    filtro = " OR ".join(f"from:{a}" for a in alvos)
    q = urllib.parse.quote(f"newer_than:{dias}d ({filtro})")
    fios = _pegar(f"{API}/threads?q={q}&maxResults=100", tk).get("threads", [])

    saida = []
    for f in fios:
        d = _pegar(f"{API}/threads/{f['id']}?format=metadata", tk)
        ult_casa = ult_minha = None
        assunto = ""
        for m in d.get("messages", []):
            hs = {h["name"]: h["value"] for h in m["payload"]["headers"]}
            assunto = assunto or hs.get("Subject", "")
            ts = int(m["internalDate"])
            if "SENT" in (m.get("labelIds") or []):
                ult_minha = max(ult_minha or 0, ts)
            elif any(a in (hs.get("From") or "").lower() for a in alvos):
                ult_casa = max(ult_casa or 0, ts)
        if ult_casa and (ult_minha is None or ult_casa > ult_minha):
            saida.append({
                "thread": f["id"], "assunto": assunto,
                "ultimaDaCasa": datetime.fromtimestamp(
                    ult_casa / 1000, timezone.utc).astimezone().isoformat(timespec="minutes"),
                "minhaUltima": None if ult_minha is None else datetime.fromtimestamp(
                    ult_minha / 1000, timezone.utc).astimezone().isoformat(timespec="minutes"),
                "nuncaRespondi": ult_minha is None,
            })
    return sorted(saida, key=lambda x: x["ultimaDaCasa"], reverse=True)


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Fios de e-mail ainda sem resposta minha")
    p.add_argument("--dias", type=int, default=20, help="janela de busca (padrão 20)")
    p.add_argument("--json", action="store_true", help="saída em JSON")
    a = p.parse_args(argv)

    alvos = remetentes()
    if not alvos:
        print("nenhum remetente vigiado: a lista vive no acervo, sob "
              "`fios_remetentes_casa`, e ele não está nesta máquina", file=sys.stderr)
        return 2

    try:
        fios = abertos(alvos, a.dias)
    except (urllib.error.URLError, OSError, KeyError, json.JSONDecodeError) as e:
        print(f"falhou: {type(e).__name__}: {e}", file=sys.stderr)
        return 1

    if a.json:
        print(json.dumps(fios, ensure_ascii=False, indent=2))
    elif not fios:
        print(f"nenhum fio aberto nos últimos {a.dias} dias — a última palavra é minha "
              "em todos")
    else:
        print(f"{len(fios)} fio(s) em que a última palavra NÃO é minha:\n")
        for f in fios:
            marca = "NUNCA RESPONDI" if f["nuncaRespondi"] else f"minha: {f['minhaUltima'][:16]}"
            print(f"  {f['ultimaDaCasa'][:16]}  {f['assunto'][:76]}")
            print(f"      thread {f['thread']} · {marca}\n")

    return 10 if fios else 0


if __name__ == "__main__":
    raise SystemExit(main())
