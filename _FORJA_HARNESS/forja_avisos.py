# -*- coding: utf-8 -*-
"""Caixa de avisos com destinatário e estado — o metro que faltava depois da detecção.

Em 07/08/2026, às 18h17, foram opostos embargos de declaração contra a decisão
que o titular usaria como paradigma numa negociação. O vigia do STF capturou a
movimentação às 09h00 do dia seguinte, comparou hash, confirmou a novidade e
gravou a linha em `telemetria/monitor_stf/<caso>_novidades.log`. Ali ela ficou. O
titular só soube em 09/08, porque alguém foi conferir o andamento à mão por outro
motivo.

O vigia não falhou: leu, comparou, detectou, datou. **Falhou o metro seguinte.**
Aviso que ninguém abre é indistinguível de aviso que não existe, e o desenho
antigo piorava isso de duas maneiras. Primeira, o destino era um arquivo de log
que ninguém tinha razão para abrir. Segunda, e pior, o log só registrava a
novidade: a execução seguinte já dizia `[igual] sem movimento novo`, de modo que
quem não olhasse na janela certa perdia a informação para sempre.

Este módulo troca log por **caixa**, e a diferença é o estado. Um aviso nasce
`naoVisto` e continua `naoVisto` em toda leitura, todo dia, até que alguém o
marque como visto. Não some por decurso de tempo, não some porque já foi
impresso uma vez, e não some porque a próxima execução do vigia não achou nada
de novo — a ausência de novidade nova não é ciência da novidade antiga.

    from forja_avisos import depositar
    depositar(origem="monitor_stf", chave=f"{caso}:{movimento}",
              titulo="RE 1.395.147 — embargos de declaração",
              detalhe="Petição 99.875, 07/08/2026 18h17", caso=caso)

O depósito é idempotente por `(origem, chave)`: o vigia pode rodar de hora em
hora sem multiplicar o mesmo aviso, e sem reabrir o que já foi visto.

    python forja_avisos.py                  # o que está esperando leitura
    python forja_avisos.py --todos          # inclui os já vistos
    python forja_avisos.py --visto <id>     # dar ciência, com nome de quem deu
    python forja_avisos.py --json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

FORJA = Path(__file__).resolve().parent
CAIXA = FORJA / "state" / "AVISOS.json"
VERSAO = "FORJA-AVISOS-v1"

URGENCIAS = ("alta", "media", "baixa")


def _agora() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def _id(origem: str, chave: str) -> str:
    return hashlib.sha256(f"{origem}\x00{chave}".encode("utf-8")).hexdigest()[:12]


def carregar() -> dict:
    if CAIXA.is_file():
        try:
            d = json.loads(CAIXA.read_text(encoding="utf-8"))
            d.setdefault("avisos", [])
            return d
        except (OSError, ValueError):
            pass
    return {"contrato": VERSAO, "avisos": []}


def _gravar(d: dict) -> None:
    d["contrato"] = VERSAO
    CAIXA.parent.mkdir(parents=True, exist_ok=True)
    CAIXA.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def depositar(*, origem: str, chave: str, titulo: str, detalhe: str = "",
              caso: str | None = None, urgencia: str = "media") -> dict:
    """Deposita um aviso. Idempotente por (origem, chave).

    Reaparecer não reabre: se o aviso já existe e já foi visto, ele continua
    visto. O vigia repete a leitura o tempo todo, e reabrir a cada execução
    transformaria a caixa em ruído — que é a forma mais rápida de ensinar
    alguém a não olhar para ela.
    """
    if urgencia not in URGENCIAS:
        raise ValueError(f"urgência {urgencia!r} fora de {URGENCIAS}")
    d = carregar()
    aid = _id(origem, chave)
    for a in d["avisos"]:
        if a["id"] == aid:
            a["ultimaLeitura"] = _agora()
            _gravar(d)
            return a
    aviso = {
        "id": aid, "origem": origem, "chave": chave, "titulo": titulo,
        "detalhe": detalhe, "caso": caso, "urgencia": urgencia,
        "depositadoEm": _agora(), "ultimaLeitura": _agora(),
        "estado": "naoVisto", "vistoEm": None, "vistoPor": None, "nota": None,
    }
    d["avisos"].append(aviso)
    _gravar(d)
    return aviso


def pendentes() -> list[dict]:
    ordem = {u: i for i, u in enumerate(URGENCIAS)}
    return sorted((a for a in carregar()["avisos"] if a["estado"] == "naoVisto"),
                  key=lambda a: (ordem.get(a["urgencia"], 9), a["depositadoEm"]))


def dar_ciencia(aid: str, *, por: str, nota: str | None = None) -> dict | None:
    d = carregar()
    for a in d["avisos"]:
        if a["id"] == aid or a["id"].startswith(aid):
            a["estado"] = "visto"
            a["vistoEm"] = _agora()
            a["vistoPor"] = por
            a["nota"] = nota
            _gravar(d)
            return a
    return None


def linhas_para_contexto(limite: int = 8) -> list[str]:
    """O que o LocalContext imprime no começo da sessão. Vazio se não há nada."""
    p = pendentes()
    if not p:
        return []
    out = [f"## FORJA — {len(p)} aviso(s) esperando leitura (forja_avisos)"]
    for a in p[:limite]:
        marca = " **URGENTE**" if a["urgencia"] == "alta" else ""
        out.append(f"- [{a['id']}]{marca} {a['titulo']}")
        if a["detalhe"]:
            out.append(f"  - {a['detalhe'][:160]}")
    if len(p) > limite:
        out.append(f"- (+{len(p) - limite} outro(s); `python forja_avisos.py`)")
    out.append("- dar ciência: `python forja_avisos.py --visto <id> --por <nome>`")
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--todos", action="store_true", help="inclui os já vistos")
    ap.add_argument("--visto", metavar="ID", help="dar ciência de um aviso")
    ap.add_argument("--por", default=None, help="quem deu ciência")
    ap.add_argument("--nota", default=None, help="o que foi feito a respeito")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    if args.visto:
        if not args.por:
            print("--visto exige --por: ciência sem nome não é ciência", file=sys.stderr)
            return 2
        a = dar_ciencia(args.visto, por=args.por, nota=args.nota)
        if not a:
            print(f"aviso {args.visto} não encontrado", file=sys.stderr)
            return 1
        print(f"visto: [{a['id']}] {a['titulo']} — por {a['vistoPor']}")
        return 0

    itens = carregar()["avisos"] if args.todos else pendentes()
    if args.json:
        print(json.dumps(itens, ensure_ascii=False, indent=2))
        return 0
    if not itens:
        print("nenhum aviso esperando leitura")
        return 0
    for a in itens:
        estado = "" if a["estado"] == "naoVisto" else f" (visto por {a['vistoPor']})"
        print(f"[{a['id']}] {a['urgencia']:<5} {a['titulo']}{estado}")
        if a["detalhe"]:
            print(f"           {a['detalhe'][:150]}")
        print(f"           origem {a['origem']} · depositado {a['depositadoEm'][:16]}")
    print(f"\n{len(itens)} aviso(s). Ciência: --visto <id> --por <nome>")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
