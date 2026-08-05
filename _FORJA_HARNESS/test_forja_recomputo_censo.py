# -*- coding: utf-8 -*-
"""test_forja_recomputo_censo.py — catraca de disparo dos recomputos.

Regressão verde prova que a função funciona; não prova que ela é chamada sobre
material real. Esta catraca guarda o número de gates que efetivamente produzem
veredito contra as tentativas do acervo. Se um recomputo parar de disparar —
porque o artefato mudou de nome, porque a rota mudou, porque um import quebrou
em silêncio —, o número cai e a suíte avisa.

É a lição 3 do plano visual aplicada ao próprio trabalho desta frente: gate
instalado na rota que ninguém percorre é gate nenhum, e treze recomputos novos
em um dia não estão imunes por serem novos.

Uso: python test_forja_recomputo_censo.py   (exit 0 = ok; exit 1 = regressão)
"""
from __future__ import annotations

import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from forja_recomputo_censo import censo  # noqa: E402

# Medido em 04/08/2026. Só pode subir.
# 41 -> 46 na leva 23: os cinco gates da F9 saíram do limbo. Quatro passaram a
# produzir veredito quando o censo deixou de procurar o arquivo literal
# `package_manifest.json` e passou a resolver o id `package_manifest` declarado
# no PHASE_RESULT — a única F9 real do acervo o registra como
# `PACKAGE_DEFINITION_NYLTON_V1.json`. O quinto, `email_human_style_passed`,
# ganhou produtor em `forja_entrega`.
GATES_COM_VEREDITO_MIN = 46
TENTATIVAS_MIN = 55


def main() -> int:
    falhas = 0
    casos = 0
    laudo = censo()

    casos += 1
    if laudo["erros"]:
        print(f"  FALHOU: {len(laudo['erros'])} produtor(es) estouraram sobre material real:")
        for erro in laudo["erros"][:5]:
            print(f"      {erro[:160]}")
        falhas += 1

    casos += 1
    if laudo["tentativasExaminadas"] < TENTATIVAS_MIN:
        print(f"  FALHOU: o censo examinou {laudo['tentativasExaminadas']} tentativas, abaixo do "
              f"piso de {TENTATIVAS_MIN} — a catraca ficaria verde por falta de material")
        falhas += 1

    casos += 1
    if laudo["gatesQueProduziramVeredito"] < GATES_COM_VEREDITO_MIN:
        print(f"  FALHOU: só {laudo['gatesQueProduziramVeredito']} gates produziram veredito "
              f"sobre material real, contra {GATES_COM_VEREDITO_MIN} medidos em 04/08/2026. "
              "Algum recomputo deixou de disparar.")
        falhas += 1

    # Um gate que só sabe dizer `pass` no acervo inteiro não provou saber dizer
    # não. Não é defeito por si, mas o número não pode explodir sem ninguém ver.
    complacentes = [g for g, c in laudo["vereditosPorGate"].items() if set(c) == {"pass"}]
    casos += 1
    if len(complacentes) > len(laudo["vereditosPorGate"]) * 0.75:
        print(f"  FALHOU: {len(complacentes)} de {len(laudo['vereditosPorGate'])} gates só "
              "disseram `pass` — a esteira inteira virou complacente")
        falhas += 1

    # Os gates com achado real precisam continuar achando: se todos ficarem
    # verdes de uma vez, o mais provável é que algo parou de rodar.
    com_reprovacao = [g for g, c in laudo["vereditosPorGate"].items() if c.get("fail")]
    casos += 1
    if not com_reprovacao:
        print("  FALHOU: nenhum gate reprovou nada no acervo inteiro — em 04/08/2026 eram nove, "
              "entre eles a pergunta jurisdicional ausente e o regimento não declarado")
        falhas += 1

    # A rota de produção resolve o fact_ledger promovido pela F3 quando o F7
    # não o repete na pasta da tentativa. O censo tem de exercer essa mesma
    # ligação pelo menos uma vez; sem isso o gate de lastro desaparece do
    # acervo por um falso "sem arquivo local".
    lastro = laudo["vereditosPorGate"].get("fact_grounding_verbatim", {})
    casos += 1
    if not lastro or sum(lastro.values()) < 1:
        print("  FALHOU: fact_grounding_verbatim não foi recomputado por artefato promovido")
        falhas += 1

    if falhas:
        print(f"REGRESSÃO: {falhas} de {casos} verificações de disparo falharam")
        return 1
    print(f"ok: {laudo['gatesQueProduziramVeredito']} gates produziram veredito sobre "
          f"{laudo['tentativasExaminadas']} tentativas reais; {len(com_reprovacao)} reprovaram "
          f"alguma coisa e {len(complacentes)} só disseram `pass`")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
