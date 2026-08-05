# -*- coding: utf-8 -*-
"""test_forja_baseline_aprovado.py — o padrão aprovado continua sendo lido igual.

Guarda três coisas, e a terceira é a que importa:

  1. O manifesto existe e cobre todas as âncoras declaradas.
  2. Nenhum artefato aprovado foi editado desde a gravação.
  3. Nenhum gate mudou de veredito sobre eles.

O item 3 é a rede que faltava em 04/08/2026, quando quatro ajustes de gate no
mesmo dia reprovaram o padrão da casa e a peça foi tratada como defeituosa. Depois
desta suíte, um ajuste desse tipo não passa em silêncio: ele acende aqui, e a
pergunta "o gate melhorou ou eu o moldei até aprovar o que eu produzo?" vira
obrigatória antes de seguir.

Divergência aqui NÃO significa que o gate está errado. Significa que alguém
precisa decidir, por escrito, qual dos dois lados mudou — e regravar o baseline
com motivo, se a mudança for legítima.

Uso: python test_forja_baseline_aprovado.py   (exit 0 = ok; exit 1 = divergência)
"""
from __future__ import annotations

import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from forja_baseline_aprovado import ANCORAS, MANIFESTO, conferir  # noqa: E402


def main() -> int:
    if not MANIFESTO.is_file():
        print(f"  FALHOU: o manifesto do baseline não existe ({MANIFESTO.name}) — "
              "sem ele, 'padrão aprovado' volta a ser declaração em vez de fato conferível")
        return 1

    laudo = conferir()

    falhas = 0
    if laudo.get("ausentes"):
        print(f"  FALHOU: âncora(s) ausente(s) do acervo: {', '.join(laudo['ausentes'])} — "
              "peça aprovada que some leva junto a prova de que o gate a aprovava")
        falhas += 1

    if laudo["ancorasConferidas"] < len(ANCORAS):
        print(f"  FALHOU: só {laudo['ancorasConferidas']} de {len(ANCORAS)} âncoras foram "
              "conferidas — o baseline mede menos do que declara guardar")
        falhas += 1

    for divergencia in laudo["divergencias"]:
        if divergencia["tipo"] == "artefato_alterado":
            print(f"  FALHOU: a peça aprovada '{divergencia['ancora']}' foi EDITADA desde a "
                  "gravação do baseline — documento entregue não se altera em silêncio")
        else:
            print(f"  FALHOU: o veredito sobre '{divergencia['ancora']}' mudou em "
                  f"{divergencia['campo']}: {divergencia['antes']} -> {divergencia['agora']}. "
                  f"Esta âncora guarda: {divergencia['guarda']}")
        falhas += 1

    if falhas:
        print("REGRESSÃO: o padrão aprovado deixou de ser lido como era. Decida por escrito "
              "qual lado mudou — e só então regrave com "
              "`python forja_baseline_aprovado.py --gravar \"motivo\"`")
        return 1

    print(f"ok: {laudo['ancorasConferidas']} âncoras do padrão aprovado intactas e com o mesmo "
          "veredito — nenhum gate derivou contra o que a casa aprovou")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
