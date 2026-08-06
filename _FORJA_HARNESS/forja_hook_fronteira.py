# -*- coding: utf-8 -*-
"""Avisa, no instante da escrita, quando um arquivo do motor ganha dado de cliente.

Por que no instante da escrita, e não só na publicação. O gate de fronteira roda
antes de sincronizar, e roda bem — em 05/08/2026 ele barrou três publicações
seguidas. O problema é o intervalo: quem escreveu o arquivo às 15h só descobre
às 20h, quando a rotina noturna reprova, e a essa altura quem escreveu não está
mais ali para explicar por que aquele número estava no código. O dado fica, a
publicação para, e o conserto vira arqueologia.

Este hook fecha esse intervalo. Ele não substitui o gate: roda por arquivo, no
momento em que o agente escreve, e devolve o aviso a quem ainda tem o contexto
na cabeça. O gate continua sendo a barreira que impede a publicação.

O que ele acusa é o que a fronteira acusa, pela mesma função — número CNJ, CPF,
CNPJ, inscrição na OAB e nome de cliente, este último só onde o acervo está
montado. Fora do acervo o hook degrada para os sinais estruturais e **diz que
degradou**, em vez de calar.

Entrada: JSON do hook, em stdin. Saída: código 2 com a mensagem em stderr
quando há sinal, para que o agente veja e corrija; 0 no resto, inclusive em
qualquer erro interno — um hook que quebra a sessão por causa de si mesmo é pior
do que um hook ausente.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent


def _caminho_do_evento(evento: dict) -> Path | None:
    entrada = evento.get("tool_input") or {}
    bruto = entrada.get("file_path") or entrada.get("notebook_path")
    if not bruto:
        return None
    try:
        return Path(bruto).resolve()
    except (OSError, ValueError):
        return None


def main() -> int:
    try:
        evento = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0

    caminho = _caminho_do_evento(evento)
    if caminho is None or not caminho.is_file():
        return 0
    try:
        rel = caminho.relative_to(RAIZ).as_posix()
    except ValueError:
        return 0                                   # fora da pasta de trabalho

    sys.path.insert(0, str(RAIZ / "_FORJA_HARNESS"))
    try:
        import forja_fronteira as fronteira
    except ImportError:
        return 0

    destino, _ = fronteira.classificar(rel)
    if destino != fronteira.MOTOR:
        return 0                                   # acervo e local podem carregar cliente
    if caminho.suffix.lower() not in fronteira.TEXTO:
        return 0                                   # binário é barrado por regra de caminho

    try:
        texto = caminho.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return 0

    nomes, modo = fronteira.carregar_nomes(RAIZ)
    padroes = {n: fronteira._padrao_de_nome(n) for n in nomes}
    sinais = fronteira.sinais_no_texto(texto, nomes, padroes)
    if not sinais:
        return 0

    aviso = [
        f"FRONTEIRA: `{rel}` vai para o repositório do MOTOR e carrega dado de cliente.",
        f"Sinais: {', '.join(sinais[:6])}"
        + (f" (e mais {len(sinais) - 6})" if len(sinais) > 6 else ""),
        "",
        "O motor é o repositório destinado a ser compartilhado com outros",
        "escritórios. Enquanto isto estiver aqui, a sincronização das 20:00",
        "reprova e NADA é publicado — nem o acervo.",
        "",
        "Saídas, na ordem: em `.md`/`.txt`, trocar o nome pelo pseudônimo do caso",
        "(`CASO-NN`); em código ou JSON, registrar o dado no acervo e lê-lo por",
        "`forja_acervo.valor()` / `.caminho()` / `.caso()`; se o arquivo inteiro é",
        "registro de um caso e não doutrina do sistema, ele pertence ao acervo.",
    ]
    if modo != "nominal":
        aviso += ["",
                  "Atenção: o acervo não está montado, então este aviso viu apenas",
                  "CNJ, CPF, CNPJ e OAB — nome de cliente NÃO foi verificado."]
    print("\n".join(aviso), file=sys.stderr)
    return 2


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:                              # noqa: BLE001
        sys.exit(0)
