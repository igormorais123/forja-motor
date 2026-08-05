# -*- coding: utf-8 -*-
"""test_forja_canario_mutacao.py — catraca do canário de mutação.

Mede o que o censo não consegue: o censo observa que um gate só disse `pass`, e
isso tanto pode significar esteira limpa quanto gate cego. O canário decide,
destruindo o artefato real que o gate aprovou e exigindo que o veredito mude.

O que esta catraca guarda:

  - nenhum gate pode aprovar artefato zerado, esvaziado ou sem prova;
  - o número de gates que sabem reprovar a mutação só pode subir.

O limite honesto do instrumento, para quem for lê-lo daqui a seis meses: ele
prova que o gate LÊ o artefato, não que ele julgue bem. Um gate pode reprovar
o arquivo vazio e continuar cego para o defeito sutil — a mutação é grosseira
de propósito, porque grosseira ela é barata e determinística. A pergunta fina
continua sendo respondida por regressão com contraprova, e por leitura humana.

Uso: python test_forja_canario_mutacao.py   (exit 0 = ok; exit 1 = regressão)
"""
from __future__ import annotations

import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from forja_canario_mutacao import canario  # noqa: E402

# Medido em 04/08/2026 com as quatro mutações: 36 gates examinados, 33
# reprovaram alguma, 3 sumiram do laudo (percebendo a ausência), 0 aprovaram a
# ruína. Só sobe.
#
# Leva 23: 33/36 -> 35/40. O canário passou a internalizar no espelho os
# artefatos declarados por caminho absoluto fora da pasta da tentativa. Antes ele
# os lia intactos, e a família da F9 aparecia como sobrevivente da destruição —
# falso positivo do instrumento, não complacência do gate.
#
# Leva 24 (05/08/2026): a catraca passou a contar PROVA DE QUE O GATE SABE DIZER
# NÃO, e não só a prova obtida por mutação.
#
# O que aconteceu. As checagens de diversidade do F2A entraram e o
# `exploration_100_complete` passou a reprovar as 14 árvores reais do acervo, que
# são formulário. Como o canário só muta gate cujo veredito-base é `pass`, ele
# deixou de ter o que mutar ali: o gate saiu de `gatesExaminados` (40 -> 39) e de
# `gatesQueReprovaramAlgumaMutacao` (35 -> 34). A catraca acusou "algum gate ficou
# cego" — quando a causa era o oposto exato, o gate tinha acabado de ENXERGAR.
#
# A saída fácil seria baixar o piso de 40/35 para 39/34, e é precisamente assim
# que uma campanha de melhoria destrói a proteção que deveria reforçar: um número
# por vez, sempre com bom motivo. Em vez disso corrigiu-se a MEDIDA.
#
# `coberturaViva` = gates examinados por mutação ∪ gates que já reprovam o
# artefato real sem mutação nenhuma. `provaDeQueSabeDizerNao` = os que reprovaram
# alguma mutação ∪ os estritos na base.
#
# Isto NÃO afrouxa a catraca, e a razão é simples: um gate cego não reprova
# mutação nem reprova o artefato real, então não entra em nenhum dos dois
# conjuntos. Só muda o que conta como prova — passar a aceitar a evidência mais
# forte (reprovar o dado verdadeiro) além da evidência simulada (reprovar o dado
# destruído). Os pisos numéricos ficam onde estavam.
REPROVAM_MUTACAO_MIN = 35
EXAMINADOS_MIN = 40


def _contraprova_da_medida() -> list[str]:
    """A medida nova precisa continuar reprovando gate cego.

    Trocar "reprovou mutação" por "reprovou mutação OU reprova o artefato real"
    amplia o que conta como prova, e ampliar critério é exatamente o movimento
    com que uma campanha se autoaprova. Então a ampliação é exercida aqui contra
    um laudo forjado: um gate que não reprova nada não pode entrar em conjunto
    nenhum, e a catraca tem de acusar.
    """
    falhas = []
    cego = {
        "gatesExaminados": 1, "coberturaViva": 1,
        "gatesQueReprovaramAlgumaMutacao": [], "gatesEstritosNaBase": [],
    }
    sabem = set(cego["gatesQueReprovaramAlgumaMutacao"]) | set(cego["gatesEstritosNaBase"])
    if sabem:
        falhas.append("gate que não reprova nada entrou no conjunto de prova")
    if cego["coberturaViva"] >= EXAMINADOS_MIN:
        falhas.append("laudo sem material passaria o piso de cobertura")

    # E o inverso: gate estrito na base conta, porque reprovar o dado VERDADEIRO
    # é evidência mais forte que reprovar o dado destruído.
    estrito = {"gatesQueReprovaramAlgumaMutacao": [], "gatesEstritosNaBase": ["g"]}
    if not (set(estrito["gatesQueReprovaramAlgumaMutacao"])
            | set(estrito["gatesEstritosNaBase"])):
        falhas.append("gate que reprova o artefato real não foi contado como prova")
    return falhas


def main() -> int:
    falhas = 0
    for problema in _contraprova_da_medida():
        print(f"  FALHOU (contraprova da medida): {problema}")
        falhas += 1
    laudo = canario(limite_por_gate=2)

    if laudo["erros"]:
        print(f"  FALHOU: {len(laudo['erros'])} erro(s) durante a mutação:")
        for erro in laudo["erros"][:5]:
            print(f"      {erro[:160]}")
        falhas += 1

    if laudo["gatesQueSobreviveramATodas"]:
        print("  FALHOU: gate(s) disseram `pass` sobre artefato destruído — não protegem nada:")
        for gate in laudo["gatesQueSobreviveramATodas"]:
            print(f"      {gate}")
        falhas += 1

    estritos = set(laudo.get("gatesEstritosNaBase") or ())
    cobertura = laudo.get("coberturaViva", laudo["gatesExaminados"])
    if cobertura < EXAMINADOS_MIN:
        print(f"  FALHOU: cobertura viva de {cobertura} gates ({laudo['gatesExaminados']} "
              f"examinados por mutação + {len(estritos)} estritos na base), abaixo do piso "
              f"de {EXAMINADOS_MIN} — a catraca ficaria verde por falta de material")
        falhas += 1

    sabem_dizer_nao = set(laudo["gatesQueReprovaramAlgumaMutacao"]) | estritos
    reprovaram = len(laudo["gatesQueReprovaramAlgumaMutacao"])
    if len(sabem_dizer_nao) < REPROVAM_MUTACAO_MIN:
        print(f"  FALHOU: {len(sabem_dizer_nao)} gates provaram saber dizer não "
              f"({reprovaram} reprovando mutação + {len(estritos)} reprovando o artefato "
              f"real), contra o piso de {REPROVAM_MUTACAO_MIN} — algum gate ficou cego")
        falhas += 1

    if falhas:
        print(f"REGRESSÃO: {falhas} verificação(ões) do canário falharam")
        return 1
    print(f"ok: {reprovaram} de {laudo['gatesExaminados']} gates reprovam artefato destruído; "
          f"{len(laudo['gatesSemVereditoAposMutacao'])} percebem a ausência; nenhum aprova a ruína")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
