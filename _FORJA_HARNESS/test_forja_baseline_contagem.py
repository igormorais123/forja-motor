# -*- coding: utf-8 -*-
"""O relatório do baseline conta o que realmente aconteceu.

Achado em 09/08/2026, e ele durou o tempo em que ninguém precisou do número: a
expressão que lia a última linha do pytest era
`(?:(\\d+) failed[,\\s])?(\\d+) passed`. Em `1 failed, 21 passed` o `[,\\s]`
consumia a vírgula, o caractere seguinte era um espaço e não um dígito, o
casamento retrocedia e o grupo opcional saía de cena. **Todo relatório gravava
`failed: 0`, inclusive nas execuções reprovadas.** E `1 error in 0.20s` — a
forma como aparece um módulo que sequer importa — não casava com nada, o que
zerava as três contagens de uma vez.

O veredito nunca dependeu disso: ele vem do código de saída, e continuou certo.
O que estava errado era **o número que alguém leria depois para saber o tamanho
do estrago** — e relatório que subnotifica é pior que relatório ausente, porque
parece resposta.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import forja_baseline as bl

falhas = 0
casos = 0

# (última linha do pytest, passed, failed, errors, subtests)
AMOSTRAS = [
    ("22 passed in 0.27s", 22, 0, 0, 0),
    # O caso real que passava despercebido.
    ("1 failed, 21 passed in 0.59s", 21, 1, 0, 0),
    ("5 failed, 2 passed in 1.02s", 2, 5, 0, 0),
    ("63 passed, 3 subtests passed in 0.75s", 63, 0, 0, 3),
    # Módulo que nem importou: nenhuma das contagens antigas o via.
    ("1 error in 0.20s", 0, 0, 1, 0),
    ("2 errors in 0.31s", 0, 0, 2, 0),
    ("2 passed, 2 warnings in 0.31s", 2, 0, 0, 0),
    # Suíte só de subtests não pode ter o subtest lido como total.
    ("3 subtests passed in 0.10s", 0, 0, 0, 3),
    ("1 failed, 4 passed, 2 subtests passed in 1.10s", 4, 1, 0, 2),
]

for texto, p, f, e, s in AMOSTRAS:
    casos += 1
    c = bl._contagens_pytest(texto)
    obtido = (c["passed"], c["failed"], c["errors"], c["subtests"])
    if obtido != (p, f, e, s):
        falhas += 1
        print(f"  FALHOU: {texto!r} -> {obtido}, esperado {(p, f, e, s)}")

# A propriedade que resume tudo: linha que menciona falha nunca produz zero.
casos += 1
if bl._contagens_pytest("1 failed, 21 passed in 0.59s")["failed"] == 0:
    falhas += 1
    print("  FALHOU: linha com falha declarada devolveu failed=0")

if falhas:
    print(f"REGRESSÃO: {falhas} de {casos} casos falharam")
    raise SystemExit(1)
print(f"ok: {casos} casos — o relatório do baseline conta falha, erro de importação "
      f"e subtest pelo que eles são, e nunca devolve zero sobre execução reprovada")
