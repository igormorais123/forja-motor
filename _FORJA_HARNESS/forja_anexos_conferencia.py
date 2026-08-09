"""Confere se um caso tem anexo externo pendente — de fato, não por default.

Em 09/08/2026 a fila inteira de bloqueios da FORJA — 22 casos, dois com prazo
vencido — repousava sobre um campo que nunca afirmou o que dizia. O
`anexos.externosPendentes` do painel nasce `True` em toda demanda criada
automaticamente, com a observação "anexos ainda precisam ser conferidos", e nada
na esteira o desliga: 75 das 84 demandas o carregavam, **53 delas já entregues**.
O rótulo derivado dele — "anexos externos (Drive/TransferNow/WhatsApp)
pendentes" — afirmava um fato que ninguém tinha verificado em caso nenhum.

Conferir à mão 22 casos resolveria hoje e não sobreviveria ao volume, que é a
lição que a casa já pagou duas vezes. Então a conferência é mecânica e mede duas
coisas verificáveis:

1. **O comando cita link externo?** Drive, TransferNow, WeTransfer, Dropbox,
   OneDrive, wa.me. Se não cita nenhum, não há anexo externo a esperar — e o
   caso não deveria estar fora da fila por causa disso.
2. **A pasta do caso tem documento de origem?** Não é prova de que veio tudo,
   e o script não finge que é: pasta cheia com link não resolvido continua
   `a_conferir`, para olho humano.

O veredito automático só é emitido no caso limpo — sem link nenhum. Onde há
link, o script mostra o link e a linha em que ele aparece, e para. **Ele não
grava em `demandas.json`**, que é quadro de comando humano; grava o próprio
artefato, que a fila lê como sobreposição.

    python forja_anexos_conferencia.py            # relatório, não grava
    python forja_anexos_conferencia.py --aplicar  # grava os vereditos limpos
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import date, datetime, timezone
from pathlib import Path

FORJA = Path(__file__).resolve().parent
RAIZ = FORJA.parent
DATA = RAIZ / "gestao_escritorio" / "data"
ARTEFATO = FORJA / "state" / "ANEXOS_CONFERENCIA.json"
VERSAO = "FORJA-ANEXOS-CONFERENCIA-v1"

COMANDOS = ("COMANDO_DO_EMAIL.md", "COMANDO_DO_WHATSAPP.md",
            "COMANDO_HERMES.md", "COMANDO_MANUAL.md", "COMANDO_DO_CASO.md")

# Hospedeiros de arquivo que aparecem nos e-mails do escritório. A lista é
# fechada de propósito: procurar "http" acusaria toda citação de jurisprudência.
LINK_EXTERNO_RE = re.compile(
    r"https?://[^\s)>\]]*(?:drive\.google|docs\.google|transfernow|wetransfer|"
    r"we\.tl|dropbox|1drv\.ms|onedrive|sharepoint|mega\.nz|filemail|"
    r"swisstransfer|sendgb)[^\s)>\]]*", re.I)
WHATSAPP_RE = re.compile(r"https?://(?:wa\.me|chat\.whatsapp\.com)/[^\s)>\]]*", re.I)

# Arquivos que a própria fábrica gera: não contam como documento de origem.
NOSSOS = re.compile(
    r"^(COMANDO_|MAPA_IA|RELATORIO_|F\d|REGIMENTO_INTERNO_|compor_|gerar_|"
    r"ATUALIZACAO_|RESPOSTA_)", re.I)


def _agora() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def links_no_comando(pasta: Path) -> list[dict]:
    achados = []
    for nome in COMANDOS:
        arq = pasta / nome
        if not arq.is_file():
            continue
        for n, linha in enumerate(arq.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            for regex, tipo in ((LINK_EXTERNO_RE, "hospedeiro_de_arquivo"),
                                (WHATSAPP_RE, "whatsapp")):
                for m in regex.finditer(linha):
                    achados.append({"arquivo": nome, "linha": n, "tipo": tipo,
                                    "url": m.group(0)[:180],
                                    "contexto": " ".join(linha.split())[:200]})
    return achados


def documentos_de_origem(pasta: Path) -> int:
    """Arquivos que vieram de fora, não os que a fábrica escreveu."""
    if not pasta.is_dir():
        return 0
    n = 0
    for p in pasta.rglob("*"):
        if not p.is_file() or NOSSOS.match(p.name):
            continue
        if p.suffix.lower() in (".pdf", ".docx", ".doc", ".xlsx", ".xls", ".msg",
                                ".eml", ".jpg", ".jpeg", ".png", ".zip", ".ogg", ".mp3"):
            n += 1
    return n


def conferir(demanda: dict) -> dict:
    pasta_rel = demanda.get("pasta") or ""
    pasta = RAIZ / pasta_rel if pasta_rel else None
    existe = bool(pasta and pasta.is_dir())
    links = links_no_comando(pasta) if existe else []
    docs = documentos_de_origem(pasta) if existe else 0

    if not existe:
        veredito, porque = "a_conferir", "pasta do caso não localizada no disco"
    elif not links:
        veredito, porque = ("sem_pendencia",
                            f"nenhum link de hospedeiro externo no comando; "
                            f"{docs} documento(s) de origem na pasta")
    else:
        veredito, porque = ("a_conferir",
                            f"{len(links)} link(s) externo(s) no comando — abrir e "
                            f"confrontar com os {docs} documento(s) na pasta")
    return {
        "demandaId": demanda.get("id"),
        "caseId": "case-" + (demanda.get("id") or "sem-id"),
        "titulo": demanda.get("titulo"),
        "pasta": pasta_rel,
        "veredito": veredito,
        "porque": porque,
        "linksExternos": links,
        "documentosDeOrigem": docs,
        "conferidoEm": date.today().isoformat(),
    }


def carregar_demandas() -> list[dict]:
    d = json.loads((DATA / "demandas.json").read_text(encoding="utf-8"))
    return d["demandas"] if isinstance(d, dict) else d


def carregar_artefato() -> dict:
    if ARTEFATO.is_file():
        return json.loads(ARTEFATO.read_text(encoding="utf-8"))
    return {"contrato": VERSAO, "conferencias": {}}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--aplicar", action="store_true",
                    help="grava os vereditos automáticos (só os limpos)")
    ap.add_argument("--todas", action="store_true",
                    help="inclui demandas já cumpridas")
    args = ap.parse_args(argv)

    resultados = [conferir(d) for d in carregar_demandas()
                  if args.todas or d.get("status") == "aberta"]
    limpos = [r for r in resultados if r["veredito"] == "sem_pendencia"]
    conferir_mao = [r for r in resultados if r["veredito"] == "a_conferir"]

    print(f"{len(resultados)} demanda(s) examinada(s)")
    print(f"  {len(limpos)} sem link externo no comando — nada a esperar")
    print(f"  {len(conferir_mao)} com link ou pasta ausente — exigem olho humano\n")
    for r in conferir_mao:
        print(f"[A CONFERIR] {r['titulo'][:72]}")
        print(f"             {r['porque']}")
        for l in r["linksExternos"][:4]:
            print(f"             · {l['arquivo']}:{l['linha']} [{l['tipo']}] {l['url'][:110]}")
    if not args.aplicar:
        print("\n(nada gravado; use --aplicar para registrar os vereditos limpos)")
        return 0

    art = carregar_artefato()
    art["contrato"] = VERSAO
    art["atualizadoEm"] = _agora()
    for r in limpos:
        art["conferencias"][r["caseId"]] = {
            "conferencia": "sem_pendencia", "porque": r["porque"],
            "conferidoEm": r["conferidoEm"], "por": "forja_anexos_conferencia",
            "documentosDeOrigem": r["documentosDeOrigem"],
        }
    ARTEFATO.parent.mkdir(parents=True, exist_ok=True)
    ARTEFATO.write_text(json.dumps(art, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8")
    print(f"\ngravado: {ARTEFATO.name} — {len(limpos)} veredito(s) sem_pendencia")
    print("Os 'a conferir' NÃO foram gravados: link aberto é decisão de quem abre.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
