# -*- coding: utf-8 -*-
"""test_forja_gate_liveness.py — catraca da liveness dos gates.

Este teste não verifica se a medição está "certa": verifica que ela não piora.

A medição de 04/08/2026 estabeleceu a linha de base do harness:

    computados por código : 15 de 73 (20%)
    atestados pelo agente : 42 de 73 (57%)
    inexequíveis          : 16 (14 deles no F8_QA_VISUAL)

Os limiares abaixo são catraca, não meta. Um gate novo que o agente atesta a si
mesmo empurra `AUTODECLARADOS_MAX`; um gate que ninguém sabe emitir empurra
`INEXEQUIVEIS_MAX`. Nos dois casos o teste falha e a decisão vira consciente:
ou a mudança é justificada e o número é atualizado com motivo escrito, ou o gate
ganha produtor em código.

Mover um limiar para pior sem trocar o comentário que o explica é o que este
arquivo existe para tornar constrangedor.

Uso: python test_forja_gate_liveness.py   (exit 0 = ok; exit 1 = regressão)
"""
from __future__ import annotations

import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from forja_gate_liveness import medir  # noqa: E402

# Linha de base medida em 04/08/2026. Só melhora.
#
# Primeira medição do dia: 15 computados, 42 autodeclarados, 16 inexequíveis.
# Depois de dar produtor aos 14 gates do F8 e aos três gates da F10 canônica,
# a linha de base sobe. Os autodeclarados não caem por decreto: só diminuem
# quando uma rota real deixa de confiar no PHASE_RESULT do agente.
COMPUTADOS_MIN = 73
AUTODECLARADOS_MAX = 0
INEXEQUIVEIS_MAX = 0


def main() -> int:
    laudo = medir()
    falhas = 0

    computados = len(laudo["computados"])
    autodeclarados = len(laudo["autodeclarados"])
    inexequiveis = len(laudo["inexequiveis"])

    if computados < COMPUTADOS_MIN:
        print(f"  FALHOU: gates computados por código caíram de {COMPUTADOS_MIN} para {computados} — "
              "a esteira passou a confiar mais na palavra do agente")
        falhas += 1
    if autodeclarados > AUTODECLARADOS_MAX:
        novos = sorted(set(laudo["autodeclarados"]))
        print(f"  FALHOU: gates atestados pelo agente subiram de {AUTODECLARADOS_MAX} para "
              f"{autodeclarados} — a superfície de autovalidação cresceu: {novos[-3:]}")
        falhas += 1
    if inexequiveis > INEXEQUIVEIS_MAX:
        print(f"  FALHOU: gates inexequíveis subiram de {INEXEQUIVEIS_MAX} para {inexequiveis} — "
              "há exigência de contrato que ninguém sabe cumprir")
        falhas += 1

    # A medição precisa continuar enxergando o acervo. Zero resultados examinados
    # faria todos os números parecerem ótimos — é o modo de falha que esta
    # própria ferramenta foi criada para detectar, aplicado a ela mesma.
    if laudo["resultadosExaminados"] < 50:
        print(f"  FALHOU: só {laudo['resultadosExaminados']} resultados examinados — "
              "a medição perdeu o acervo e seus números não valem nada")
        falhas += 1

    if falhas:
        print(f"REGRESSÃO: {falhas} verificação(ões) de liveness falharam")
        return 1
    print(f"ok: {computados} gates computados, {autodeclarados} autodeclarados, "
          f"{inexequiveis} inexequíveis, {laudo['resultadosExaminados']} resultados examinados")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
