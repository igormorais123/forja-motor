# -*- coding: utf-8 -*-
"""forja_arvore_estavel.py — a bateria mede uma árvore que outros estão escrevendo.

Em 10/08/2026 duas suítes distintas reprovaram dentro do baseline e passaram
sozinhas minutos depois, sem que nada tivesse sido consertado: a que varre a
tipografia dos entregáveis e a que confere a fronteira motor/acervo. A
explicação óbvia — "a bateria renderiza peça na própria árvore que a varredura
mede" — foi escrita, virou entrada de taxonomia, e **estava errada**.

A medição desmentiu: fotografando os 30.866 arquivos antes e depois de uma
execução completa, **nenhum `.docx` ou `.pdf` foi tocado**. O que mudou foram
17 telemetrias da própria bateria e, decisivamente, arquivos de **outra sessão
do agente trabalhando na mesma pasta ao mesmo tempo** — um módulo do motor
alterado, um teste novo aparecendo, documentos de caso sendo escritos. A
bateria leva quase nove minutos; ninguém para de trabalhar nesse intervalo.

Disso segue o desenho. Não há conserto do lado das suítes: elas não são o
problema, e nenhuma mudança nelas impede que a pasta mude debaixo delas. O
conserto é a bateria **saber que o chão se moveu** e dizer isso, em vez de
emitir veredito sobre uma árvore que já não existe.

Três estados, e não dois — a mesma regra que a casa aplica a insumo, a anexo e
a gate: **verde ≠ instável ≠ vermelho**. `instavel` não é aprovação: é a recusa
de afirmar. A suíte reprovou, a árvore mudou durante a leitura, e a segunda
leitura passou. Nada disso autoriza dizer que está tudo bem, e nada disso
autoriza dizer que quebrou.

A salvaguarda contra virar tapete: **só é instável quem repete verde E teve a
árvore mexida.** Suíte que reprova duas vezes é vermelha, mexa-se a árvore o
quanto for. E a lista do que mudou vai no relatório, para que a instabilidade
seja um fato conferível e não uma desculpa reutilizável.
"""
from __future__ import annotations

import os
from pathlib import Path

FORJA = Path(__file__).resolve().parent
RAIZ = FORJA.parent

# Ruído de execução: mudam sempre, por construção, e não são a árvore que as
# suítes medem. Incluí-los faria toda execução parecer instável, que é o mesmo
# que não medir instabilidade nenhuma.
IGNORAR_PASTAS = {".git", "__pycache__", ".pytest_cache", "node_modules",
                  "telemetria", ".ruff_cache", ".mypy_cache"}
IGNORAR_SUFIXOS = (".pyc", ".tmp", ".log", ".lock")


def impressao(raiz: Path | None = None) -> dict[str, tuple[int, int]]:
    """Retrato da árvore: caminho → (mtime, tamanho).

    Guarda tamanho junto do relógio porque gravação em curso muda os dois, e
    porque relógio de sistema de arquivos no Windows tem resolução grosseira o
    bastante para duas escritas caberem no mesmo carimbo.
    """
    base = raiz or RAIZ
    retrato: dict[str, tuple[int, int]] = {}
    for pasta, subs, arquivos in os.walk(base):
        subs[:] = [s for s in subs if s not in IGNORAR_PASTAS]
        for nome in arquivos:
            if nome.endswith(IGNORAR_SUFIXOS):
                continue
            caminho = Path(pasta) / nome
            try:
                st = caminho.stat()
            except OSError:
                # Arquivo que some entre listar e medir é, ele próprio, sinal de
                # árvore em movimento — registrado como ausente, não ignorado.
                continue
            retrato[str(caminho.relative_to(base))] = (st.st_mtime_ns, st.st_size)
    return retrato


def mexeu(antes: dict, depois: dict, limite: int = 12) -> dict:
    """O que mudou entre dois retratos, com a lista contida e o total honesto."""
    novos = sorted(set(depois) - set(antes))
    sumidos = sorted(set(antes) - set(depois))
    mudados = sorted(k for k in set(antes) & set(depois) if antes[k] != depois[k])
    total = len(novos) + len(sumidos) + len(mudados)
    return {
        "mexeu": bool(total),
        "total": total,
        "novos": len(novos), "sumidos": len(sumidos), "mudados": len(mudados),
        # A amostra é para quem lê decidir se aquilo explica a falha; o total,
        # ao lado, impede que a amostra passe por lista completa.
        "amostra": (novos + mudados + sumidos)[:limite],
    }
