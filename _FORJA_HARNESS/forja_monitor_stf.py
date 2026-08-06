# -*- coding: utf-8 -*-
"""Vigia o andamento de processos no STF e avisa quando a movimentação muda.

Existe porque "monitorar o processo" vinha sendo uma promessa que dependia de
alguém lembrar de olhar. Em 05/08/2026, uma demanda de rastreamento ficou
parada em "aguardando decisão" sem que nada verificasse se a decisão havia
saído. Isto verifica. Quais processos são vigiados é dado de cliente e vive
no acervo, sob a chave `monitor-stf-vigiados`; use `--listar` para vê-los.

Como funciona
    Lê a aba de andamentos do portal do STF, que responde a requisição simples
    desde que se envie um User-Agent de navegador — a página principal do
    processo carrega os andamentos por chamada separada, e é essa chamada que
    interessa. Extrai a lista de movimentos, compara com o último retrato salvo
    e devolve as novidades.

Uso
    python forja_monitor_stf.py --listar
    python forja_monitor_stf.py                 # verifica todos os vigiados
    python forja_monitor_stf.py --caso <chave listada por --listar>
    python forja_monitor_stf.py --json          # saída para automação

Saída
    Código 0 sem novidade, 10 com novidade, 1 em erro de rede ou de leitura.
    O retrato fica em `telemetria/monitor_stf/<caso>.json`, e cada novidade é
    registrada em `telemetria/monitor_stf/<caso>_novidades.log`.

O que ele NÃO faz
    Não lê o teor das peças, que exige peticionamento com procuração, e não
    envia e-mail sozinho. Avisar é decisão de quem lê o resultado.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import forja_acervo  # noqa: E402

RAIZ = Path(__file__).resolve().parent
DESTINO = RAIZ / "telemetria" / "monitor_stf"
URL = "https://portal.stf.jus.br/processos/abaAndamentos.asp?incidente={incidente}&imprimir=true"

CABECALHO = {
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"),
    "Accept": "text/html,application/xhtml+xml,*/*",
    "Accept-Language": "pt-BR,pt;q=0.9",
}


def _vigiados() -> dict[str, dict]:
    """Processos vigiados, lidos do acervo. O motor não guarda nenhum.

    A lista é dado de cliente inteiro: número único do processo, o que se espera
    da decisão e desde quando. Escrita aqui, ela entra no repositório do motor
    por uma porta que ninguém vigia — parece configuração e é ficha de processo.
    Fica em `state/ACERVO_VALORES.json`, sob a chave abaixo, e o `incidente` é o
    identificador interno do portal do STF, visível na URL de detalhe.

    Sem o acervo montado a lista é vazia, e quem chama precisa dizer que **não
    verificou** — nunca tratar "nenhum processo vigiado" como "nada mudou".
    """
    return forja_acervo.valor("monitor-stf-vigiados", {}) or {}


_DATA = re.compile(r"\d{2}/\d{2}/\d{4}")


def _texto_limpo(html: str) -> str:
    html = re.sub(r"(?is)<(script|style).*?</\1>", " ", html)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "\n", html)).strip()


def _movimentos(html: str, limite: int = 40) -> list[str]:
    """Devolve as linhas de andamento, da mais recente para a mais antiga."""
    linhas = [ln.strip() for ln in re.sub(r"<[^>]+>", "\n", html).splitlines()]
    linhas = [ln for ln in linhas if ln]
    saida, atual = [], None
    for ln in linhas:
        if _DATA.fullmatch(ln):
            if atual:
                saida.append(atual)
            atual = ln
        elif atual and len(saida) < limite:
            atual = f"{atual} · {ln}" if len(atual) < 400 else atual
    if atual:
        saida.append(atual)
    return saida[:limite]


def consultar(incidente: str, timeout: float = 45) -> tuple[list[str], str]:
    req = urllib.request.Request(URL.format(incidente=incidente), headers=CABECALHO)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        html = r.read().decode("utf-8", "replace")
    movs = _movimentos(html)
    if not movs:
        raise RuntimeError("nenhum andamento reconhecido — o portal pode ter mudado de formato")
    return movs, hashlib.sha256("\n".join(movs).encode("utf-8")).hexdigest()


def verificar(caso: str, cfg: dict) -> dict:
    DESTINO.mkdir(parents=True, exist_ok=True)
    retrato = DESTINO / f"{caso}.json"
    agora = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")

    movs, sha = consultar(cfg["incidente"])
    anterior = json.loads(retrato.read_text(encoding="utf-8")) if retrato.is_file() else {}
    conhecidos = set(anterior.get("movimentos") or [])
    novos = [m for m in movs if m not in conhecidos] if conhecidos else []
    primeira = not conhecidos

    resultado = {
        "caso": caso, "rotulo": cfg["rotulo"], "porque": cfg["porque"],
        "verificadoEm": agora, "sha256": sha,
        "primeiraLeitura": primeira,
        "houveNovidade": bool(novos),
        "novidades": novos,
        "ultimoMovimento": movs[0] if movs else None,
        "totalMovimentos": len(movs),
    }
    retrato.write_text(json.dumps(
        {**resultado, "movimentos": movs}, ensure_ascii=False, indent=2), encoding="utf-8")

    if novos:
        log = DESTINO / f"{caso}_novidades.log"
        with log.open("a", encoding="utf-8") as fh:
            for m in novos:
                fh.write(f"{agora}\t{m}\n")
    return resultado


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Vigia andamentos de processos no STF")
    p.add_argument("--caso", help="verificar apenas um caso vigiado")
    p.add_argument("--listar", action="store_true", help="listar os casos vigiados")
    p.add_argument("--json", action="store_true", help="saída em JSON")
    a = p.parse_args(argv)

    vigiados = _vigiados()
    if not vigiados:
        print("NÃO VERIFICADO: a lista de processos vigiados vive no acervo, que "
              "não está montado nesta máquina.", file=sys.stderr)
        return 1

    if a.listar:
        for k, v in vigiados.items():
            print(f"{k}\n   {v['rotulo']}\n   incidente {v['incidente']} — {v['porque']}")
        return 0

    if a.caso and a.caso not in vigiados:
        print(f"caso não vigiado: {a.caso}", file=sys.stderr)
        return 1
    casos = {a.caso: vigiados[a.caso]} if a.caso else vigiados

    resultados, houve, erro = [], False, False
    for caso, cfg in casos.items():
        try:
            r = verificar(caso, cfg)
        except (urllib.error.URLError, RuntimeError, OSError) as e:
            erro = True
            r = {"caso": caso, "erro": f"{type(e).__name__}: {e}"}
        resultados.append(r)
        houve = houve or bool(r.get("houveNovidade"))

    if a.json:
        print(json.dumps(resultados, ensure_ascii=False, indent=2))
    else:
        for r in resultados:
            if r.get("erro"):
                print(f"[ERRO ] {r['caso']}: {r['erro']}")
            elif r["primeiraLeitura"]:
                print(f"[BASE ] {r['caso']}: retrato inicial com {r['totalMovimentos']} movimentos")
                print(f"         último: {r['ultimoMovimento']}")
            elif r["houveNovidade"]:
                print(f"[NOVO ] {r['caso']} — {len(r['novidades'])} movimento(s) novo(s):")
                for m in r["novidades"]:
                    print(f"         {m}")
            else:
                print(f"[igual] {r['caso']}: sem movimento novo desde a última leitura")
                print(f"         último: {r['ultimoMovimento']}")

    return 1 if erro else (10 if houve else 0)


if __name__ == "__main__":
    raise SystemExit(main())
