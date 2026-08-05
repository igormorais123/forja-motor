# -*- coding: utf-8 -*-
"""test_forja_canario_catraca.py — catraca sobre as catracas.

O harness guarda os próprios números com constantes de catraca. Este teste guarda
as catracas, e faz isso em dois níveis de custo bem diferentes:

  - **Estático, grátis.** Nenhuma constante de catraca pode existir sem ser
    consultada no corpo do teste, e o número TOTAL de catracas não pode encolher.
    Uma constante declarada e nunca comparada é comentário com sintaxe de código:
    o teste passa para sempre, inclusive quando o número piora. E apagar a
    catraca é o jeito mais rápido de nunca mais ver a regressão que ela guarda.

  - **Dinâmico, caro.** Apertar a catraca para o impossível e cobrar a reprovação.
    Aqui só entram as suítes baratas; a varredura do acervo e o canário de mutação
    levam minutos por execução e multiplicá-los por catraca inviabilizaria a régua.
    A prova completa é `forja_canario_catraca.py`, rodado à mão junto dos outros
    instrumentos.

O que este teste NÃO faz: exigir que os números melhorem, nem impedir que alguém
afrouxe uma catraca. Afrouxar é às vezes legítimo — o acervo cresce e um relatório
interno novo entra na conta. O que ele impede é o afrouxamento invisível, que é o
modo como um instrumento de medição vira decoração.

Uso: python test_forja_canario_catraca.py   (exit 0 = ok; exit 1 = regressão)
"""
from __future__ import annotations

import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from forja_canario_catraca import _aperta, catracas  # noqa: E402

# Medido em 04/08/2026: 17 catracas em 6 suítes. O piso existe para que remover a
# catraca não seja mais barato que defender o número que ela guarda.
CATRACAS_MIN = 17

# Suítes cujo custo cabe na régua. As caras ficam para o instrumento manual, e a
# exclusão é nominal para não virar recorte silencioso: a lista abaixo é o que
# este teste realmente exercita, e o resto está declarado como não exercitado.
RAPIDAS = (
    "test_forja_forma_artefatos.py",
    "test_forja_gate_liveness.py",
    "test_forja_artefatos.py",
)


def main() -> int:
    falhas = 0
    todas = catracas()

    if len(todas) < CATRACAS_MIN:
        print(f"  FALHOU: {len(todas)} catracas no harness, abaixo do piso de {CATRACAS_MIN} — "
              "alguém apagou uma catraca, que é o jeito mais barato de nunca mais ver a "
              "regressão que ela guardava")
        falhas += 1

    sem_uso = [x for x in todas if x["declaradaSemUso"]]
    if sem_uso:
        print(f"  FALHOU: {len(sem_uso)} catraca(s) declarada(s) e nunca consultada(s) — "
              "constante que ninguém compara é comentário com sintaxe de código:")
        for x in sem_uso:
            print(f"      {x['suite']}::{x['constante']}")
        falhas += 1

    exercitadas = [x for x in todas if x["suite"] in RAPIDAS]
    if not exercitadas:
        print("  FALHOU: nenhuma catraca das suítes rápidas foi encontrada — os nomes em "
              "RAPIDAS provavelmente saíram de sincronia com os arquivos reais")
        falhas += 1

    decorativas = []
    for entrada in exercitadas:
        resultado = _aperta(entrada)
        if not resultado["reprovou"]:
            decorativas.append(resultado)

    if decorativas:
        print(f"  FALHOU: {len(decorativas)} catraca(s) continuaram verdes com o limiar no "
              "impossível — não guardam nada:")
        for x in decorativas:
            print(f"      {x['suite']}::{x['constante']} apertada para {x['apertadaPara']}, "
                  f"exit {x['exit']} {x['erro']}")
        falhas += 1

    nao_exercitadas = sorted({x["suite"] for x in todas} - set(RAPIDAS))
    if falhas:
        print(f"REGRESSÃO: {falhas} verificação(ões) sobre as catracas falharam")
        return 1
    print(f"ok: {len(todas)} catracas, todas consultadas; {len(exercitadas)} apertadas ao "
          f"impossível reprovaram. Não exercitadas aqui por custo: {', '.join(nao_exercitadas)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
