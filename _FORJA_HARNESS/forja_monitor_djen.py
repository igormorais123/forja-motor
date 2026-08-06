# -*- coding: utf-8 -*-
"""Vigia comunicações processuais pelo Diário de Justiça Eletrônico Nacional.

Existe porque em 06/08/2026 a varredura de um mapeamento revelou, por acaso, que
dois agravos do escritório estavam pautados para julgamento em duas semanas — com
o prazo de sustentação oral correndo. As intimações haviam sido divulgadas três
semanas antes e ninguém as tinha visto. Achado que depende de acaso não se repete.

Diferença em relação ao vigia do STF (`forja_monitor_stf.py`): aquele raspa a aba
de andamentos de um processo do Supremo; este consulta a base nacional de
comunicações, que cobre todos os tribunais e devolve o TEOR de cada ato.

A lista do que vigiar NÃO mora aqui. Número de processo e nome de parte são dado
de cliente, e este arquivo pertence ao motor, que é público. Os vigiados ficam em
`state/ACERVO_VALORES.json`, sob a chave `monitor_djen_vigiados`, e sem o acervo
este módulo roda sem alvo e diz que rodou assim.

Formato esperado da entrada no acervo:

    "monitor_djen_vigiados": {
      "<chave-livre>": {"tribunal": "TRF3", "numero": "0000000-00.0000.0.00.0000",
                        "porque": "por que este processo é vigiado"}
    }

Uso
    python forja_monitor_djen.py --listar
    python forja_monitor_djen.py
    python forja_monitor_djen.py --processo <chave>
    python forja_monitor_djen.py --json

Saída
    Código 0 sem novidade, 10 com novidade, 1 em erro, 2 sem alvo configurado.
    O retrato fica em `telemetria/monitor_djen/<chave>.json` e cada novidade
    também vai para `<chave>_novidades.log`.

O que ele NÃO faz
    Não peticiona, não requer sustentação oral e não avisa ninguém sozinho.
    Avisar continua sendo decisão de quem lê o resultado.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import forja_acervo

RAIZ = Path(__file__).resolve().parent
DESTINO = RAIZ / "telemetria" / "monitor_djen"
BASE = "https://comunicaapi.pje.jus.br/api/v1/comunicacao"

CABECALHO = {
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"),
    "Accept": "application/json",
}

# Palavras que, no teor de um ato novo, pedem leitura humana imediata.
URGENTE = re.compile(
    r"pauta|sustenta[çc][ãa]o|julgamento|ac[óo]rd[ãa]o|senten[çc]a|prazo|destaque", re.I)


def gravar_json(caminho: Path, dados: dict, tentativas: int = 4) -> None:
    """Grava o retrato sem deixar arquivo pela metade e sem morrer por disputa.

    Escrever direto falhou em produção com `OSError: [Errno 22]` em dois dos
    cinco processos, na execução pelo agendador — no Windows, antivírus,
    indexador e o observador de mapas tocam o mesmo arquivo. Um vigia que perde
    o retrato passa a acusar tudo como novidade na leitura seguinte.
    """
    texto = json.dumps(dados, ensure_ascii=False, indent=2)
    ultimo = None
    for tentativa in range(tentativas):
        tmp = None
        try:
            fd, tmp = tempfile.mkstemp(dir=str(caminho.parent), suffix=".tmp")
            with os.fdopen(fd, "w", encoding="utf-8") as fh:
                fh.write(texto)
            os.replace(tmp, caminho)
            return
        except OSError as e:
            ultimo = e
            if tmp:  # senão cada retentativa deixa um órfão na pasta de telemetria
                try:
                    os.unlink(tmp)
                except OSError:
                    pass
            time.sleep(0.25 * (tentativa + 1))
    raise ultimo


def vigiados() -> dict:
    """Os processos acompanhados, lidos do acervo. Vazio quando ele não está aqui."""
    return forja_acervo.valor("monitor_djen_vigiados", {}) or {}


def _limpar(texto: str) -> str:
    texto = html.unescape(texto or "")
    texto = re.sub(r"(?is)<(script|style).*?</\1>", " ", texto)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", texto)).strip()


def consultar(tribunal: str, numero: str, timeout: float = 90) -> list[dict]:
    """Comunicações do processo, da mais recente para a mais antiga."""
    consulta = {"numeroProcesso": numero, "siglaTribunal": tribunal,
                "itensPorPagina": "100"}
    req = urllib.request.Request(f"{BASE}?{urllib.parse.urlencode(consulta)}",
                                 headers=CABECALHO)
    with urllib.request.urlopen(req, timeout=timeout) as resposta:
        dados = json.loads(resposta.read().decode("utf-8", "replace"))
    itens = dados.get("items")
    if itens is None:
        raise RuntimeError("resposta sem a lista de comunicações — a API pode ter mudado")
    saida = []
    for item in itens:
        teor = _limpar(item.get("texto"))
        saida.append({
            "id": str(item.get("id") or item.get("hash") or ""),
            "data": item.get("data_disponibilizacao"),
            "tipo": item.get("tipoComunicacao"),
            "orgao": item.get("nomeOrgao"),
            "resumo": teor[:400],
            "urgente": bool(URGENTE.search(teor)),
        })
    return sorted(saida, key=lambda c: c["data"] or "", reverse=True)


def verificar(chave: str, cfg: dict) -> dict:
    DESTINO.mkdir(parents=True, exist_ok=True)
    retrato = DESTINO / f"{chave}.json"
    agora = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")

    comunicacoes = consultar(cfg["tribunal"], cfg["numero"])
    anterior = json.loads(retrato.read_text(encoding="utf-8")) if retrato.is_file() else {}
    conhecidos = {c.get("id") for c in (anterior.get("comunicacoes") or [])}
    novas = [c for c in comunicacoes if c["id"] not in conhecidos] if conhecidos else []

    resultado = {
        "chave": chave, "tribunal": cfg["tribunal"],
        "porque": cfg.get("porque", ""), "verificadoEm": agora,
        "sha256": hashlib.sha256(
            "\n".join(c["id"] for c in comunicacoes).encode("utf-8")).hexdigest(),
        "primeiraLeitura": not conhecidos,
        "houveNovidade": bool(novas),
        "novidades": novas,
        "novidadesUrgentes": [c for c in novas if c["urgente"]],
        "total": len(comunicacoes),
        "ultima": comunicacoes[0] if comunicacoes else None,
    }
    gravar_json(retrato, {**resultado, "comunicacoes": comunicacoes})

    if novas:
        with (DESTINO / f"{chave}_novidades.log").open("a", encoding="utf-8") as fh:
            for c in novas:
                marca = "URGENTE" if c["urgente"] else "       "
                fh.write(f"{agora}\t{marca}\t{c['data']}\t{c['tipo']}\t{c['resumo'][:200]}\n")
    return resultado


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Vigia comunicações processuais pelo DJEN")
    p.add_argument("--processo", help="verificar apenas um processo vigiado")
    p.add_argument("--listar", action="store_true", help="listar os processos vigiados")
    p.add_argument("--json", action="store_true", help="saída em JSON")
    a = p.parse_args(argv)

    alvos = vigiados()
    if not alvos:
        print("nenhum processo vigiado: a lista vive no acervo, sob "
              "`monitor_djen_vigiados`, e ele não está nesta máquina", file=sys.stderr)
        return 2

    if a.listar:
        for k, v in alvos.items():
            print(f"{k}\n   {v.get('tribunal')}\n   {v.get('porque', '')}")
        return 0

    if a.processo and a.processo not in alvos:
        print(f"processo não vigiado: {a.processo}", file=sys.stderr)
        return 1
    casos = {a.processo: alvos[a.processo]} if a.processo else alvos

    resultados, houve, erro = [], False, False
    for chave, cfg in casos.items():
        try:
            r = verificar(chave, cfg)
        except (urllib.error.URLError, RuntimeError, OSError, json.JSONDecodeError,
                KeyError) as e:
            erro = True
            r = {"chave": chave, "erro": f"{type(e).__name__}: {e}"}
        resultados.append(r)
        houve = houve or bool(r.get("houveNovidade"))

    if a.json:
        print(json.dumps(resultados, ensure_ascii=False, indent=2))
    else:
        for r in resultados:
            if r.get("erro"):
                print(f"[ERRO ] {r['chave']}: {r['erro']}")
            elif r["primeiraLeitura"]:
                print(f"[BASE ] {r['chave']}: retrato inicial com {r['total']} comunicações")
            elif r["houveNovidade"]:
                urgentes = len(r["novidadesUrgentes"])
                selo = f" — {urgentes} pede(m) leitura imediata" if urgentes else ""
                print(f"[NOVO ] {r['chave']}: {len(r['novidades'])} nova(s){selo}")
                for c in r["novidades"]:
                    marca = "URGENTE " if c["urgente"] else "        "
                    print(f"   {marca}{c['data']} · {c['tipo']}\n            {c['resumo'][:220]}")
            else:
                print(f"[igual] {r['chave']}: sem comunicação nova")

    return 1 if erro else (10 if houve else 0)


if __name__ == "__main__":
    raise SystemExit(main())
