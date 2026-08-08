# -*- coding: utf-8 -*-
"""Nenhum vigia agendado pode gravar o aviso na raiz do harness.

Os três vigias — STF, DJEN e fios de e-mail sem resposta — nasceram do mesmo
molde, e o molde tinha um defeito: deixava o aviso na raiz do harness "porque
log que ninguém abre não avisa ninguém". A intenção estava certa e o lugar,
errado. O aviso nomeia processo, cliente ou assunto de fio, e a raiz do harness
é MOTOR — o repositório destinado a ser compartilhado com outros escritórios.

O efeito não é cosmético: com um aviso desses na raiz, a sincronização reprova
e **nada** é publicado, nem o motor nem o acervo. Aconteceu três vezes em dois
dias, uma por vigia, e das três eu consertei o arquivo em vez do molde.

Este teste existe para que o quarto vigia não repita. Ele não confere se o
aviso é bonito nem se o texto está certo: confere só onde ele nasce.

Uso: python test_vigias_avisam_no_acervo.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HARNESS = Path(__file__).resolve().parent

# `reports/` é acervo pela régua da fronteira e é destino de escrita de outros
# módulos, então o aviso continua à vista de quem opera.
DESTINOS_ACEITOS = ("reports",)

ATRIBUI_FLAG = re.compile(
    r"^\s*\$flag\s*=\s*Join-Path\s+\$harness\s+'([^']+)'", re.MULTILINE)

falhas: list[str] = []
conferidos = 0


def relativo(p: Path) -> str:
    return p.relative_to(HARNESS).as_posix()


for script in sorted(HARNESS.glob("*_diario.ps1")):
    texto = script.read_text(encoding="utf-8-sig")
    achados = ATRIBUI_FLAG.findall(texto)
    if not achados:
        # vigia que não deixa aviso é legítimo; só não tem o que conferir
        continue
    for destino in achados:
        conferidos += 1
        partes = destino.replace("/", "\\").split("\\")
        if len(partes) == 1:
            falhas.append(
                f"{relativo(script)}: grava o aviso em '{destino}', na raiz do "
                f"harness, que é MOTOR. Aviso nomeia caso e derruba a "
                f"sincronização inteira. Use "
                f"'reports\\{destino}'.")
        elif partes[0] not in DESTINOS_ACEITOS:
            falhas.append(
                f"{relativo(script)}: grava o aviso em '{destino}'. A pasta "
                f"'{partes[0]}' não está entre as de acervo aceitas "
                f"{DESTINOS_ACEITOS}.")

# O aviso pode já existir em disco de execução anterior ao conserto; se estiver
# na raiz, a próxima sincronização reprova mesmo com o script certo.
for nome in ("NOVIDADE_STF.md", "NOVIDADE_PROCESSUAL.md", "FIO_SEM_RESPOSTA.md"):
    if (HARNESS / nome).exists():
        falhas.append(
            f"{nome} está na raiz do harness. O script já grava no lugar "
            f"certo, mas este arquivo é de execução anterior e ainda reprova "
            f"a fronteira. Mova para reports\\.")

if conferidos == 0:
    print("REGRESSÃO: nenhum vigia foi conferido — o padrão de busca não casa "
          "mais com os scripts, e um teste que não mede nada passa sempre")
    sys.exit(1)

if falhas:
    for f in falhas:
        print("  FALHOU:", f)
    print(f"REGRESSÃO: {len(falhas)} de {conferidos} destino(s) de aviso "
          f"fora do acervo")
    sys.exit(1)

print(f"ok: {conferidos} destino(s) de aviso conferido(s) — nenhum vigia grava "
      f"na raiz do motor")
