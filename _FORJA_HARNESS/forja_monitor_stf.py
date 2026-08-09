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
import os
import re
import sys
import tempfile
import time
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


def gravar_json(caminho: Path, dados: dict, tentativas: int = 4) -> None:
    """Grava o retrato sem deixar arquivo pela metade e sem morrer por disputa.

    Escrever direto falhou em produção com `OSError: [Errno 22]` no vigia irmão,
    na execução pelo agendador — no Windows, antivírus, indexador e o observador
    de mapas tocam o mesmo arquivo. Um vigia que perde o retrato passa a acusar
    tudo como novidade na leitura seguinte.
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


_DATA = re.compile(r"\d{2}/\d{2}/\d{4}")


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


def verificar(caso: str, cfg: dict, avisar: bool = True) -> dict:
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
    gravar_json(retrato, {**resultado, "movimentos": movs})

    if novos:
        log = DESTINO / f"{caso}_novidades.log"
        with log.open("a", encoding="utf-8") as fh:
            for m in novos:
                fh.write(f"{agora}\t{m}\n")
        # O log é a trilha; a caixa é o destinatário. Sem esta linha o vigia
        # detecta e a informação para aqui — foi o que aconteceu com os embargos
        # de 07/08/2026, vistos pelo vigia às 09h00 de 08/08 e desconhecidos do
        # titular até 09/08. Detecção sem destinatário nomeado é telemetria.
        # `avisar=False` (--sem-aviso) existe para conferir a fiação sem deixar
        # aviso permanente: a caixa só sai por ciência nominada, e três avisos
        # de processo inventado abriram todas as sessões de 09/08/2026.
        try:
            from forja_avisos import depositar
            for m in novos if avisar else ():
                depositar(origem="monitor_stf", chave=f"{caso}:{m}",
                          titulo=f"{cfg['rotulo']} — movimento novo no STF",
                          detalhe=m, caso=caso,
                          urgencia="alta" if _movimento_grave(m) else "media")
        except Exception as exc:  # vigia nunca cai por causa do aviso
            print(f"[aviso] não consegui depositar na caixa: "
                  f"{type(exc).__name__}: {exc}", file=sys.stderr)
    return resultado


# Movimento que muda o que se pode afirmar sobre o processo lá fora. A lista é
# curta de propósito: marcar tudo como urgente é o mesmo que não marcar nada.
# Comparação sem acento porque o portal alterna "trânsito" e "Transitado" na
# mesma coluna, e a primeira versão desta lista perdeu justamente o trânsito em
# julgado por causa do circunflexo.
_GRAVES = ("embargo", "agravo", "decisao", "acordao", "julgamento", "julgad",
           "provido", "liminar", "tutela", "transit", "baixa", "pauta",
           "sentenca", "vista")


def _movimento_grave(movimento: str) -> bool:
    import unicodedata
    nfkd = unicodedata.normalize("NFKD", (movimento or "").lower())
    texto = "".join(c for c in nfkd if not unicodedata.combining(c))
    return any(k in texto for k in _GRAVES)


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Vigia andamentos de processos no STF")
    p.add_argument("--caso", help="verificar apenas um caso vigiado")
    p.add_argument("--listar", action="store_true", help="listar os casos vigiados")
    p.add_argument("--json", action="store_true", help="saída em JSON")
    p.add_argument("--sem-aviso", action="store_true",
                   help="não deposita na caixa de avisos; para conferir a fiação "
                        "do vigia sem deixar aviso permanente")
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
            r = verificar(caso, cfg, avisar=not a.sem_aviso)
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
