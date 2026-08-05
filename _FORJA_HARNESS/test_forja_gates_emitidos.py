# -*- coding: utf-8 -*-
"""test_forja_gates_emitidos.py — o produtor EMITE o nome que o contrato exige?

O medidor de liveness responde essa pergunta por grep, e grep é aproximação: um
nome dentro de uma lista de constantes conta como implementado sem que nada o
compute. Aqui a prova é outra — os produtores são CHAMADOS, e o teste confere
que cada gate do contrato aparece no dicionário que eles devolvem.

Foi essa a diferença entre os 17 gates classificados como inertes em 04/08/2026
e os 16 do F8 que a tarefa 16 encontrou de fato inexequíveis: os primeiros têm
produtor e a rota é que nunca rodou; os segundos ninguém sabia emitir. O
instrumento de medida precisa distinguir as duas coisas, senão o relatório
acusa dívida onde há só rota rara — e some com a dívida real no meio.

Uso: python test_forja_gates_emitidos.py   (exit 0 = ok; exit 1 = regressão)
"""
from __future__ import annotations

import io
import json
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

FORJA = Path(__file__).resolve().parent


def _contrato(fase: str) -> list[str]:
    dados = json.loads((FORJA / "phase_contracts" / f"{fase}.json").read_text(encoding="utf-8"))
    return list(dados["requiredGates"])


def _emitidos_f8() -> set:
    from forja_f8_contract import _gates_do_contrato
    emitidos = set()
    # Duas passagens: política frouxa e estrita. Gate exclusivo do modo estrito
    # devolve `not_applicable` fora dele, e continua sendo emitido — o que não
    # pode acontecer é sumir do dicionário, porque aí o contrato cobra um nome
    # que ninguém escreve.
    for politica in ("internal_review", "strict_protocol"):
        saida = _gates_do_contrato({}, None, None, [], release_policy=politica)
        emitidos |= set(saida)
    return emitidos


def _emitidos_f10() -> set:
    from forja_f10_contract import compute_f10_gates
    import inspect

    parametros = inspect.signature(compute_f10_gates).parameters
    argumentos = {}
    for nome, param in parametros.items():
        if param.default is not inspect.Parameter.empty:
            continue
        anotacao = str(param.annotation)
        if "int" in anotacao:
            argumentos[nome] = 0
        elif "str" in anotacao:
            argumentos[nome] = ""
        else:
            argumentos[nome] = {}
    return set(compute_f10_gates(**argumentos))


def main() -> int:
    falhas = 0
    linhas = []

    for fase, emissor in (("F8", _emitidos_f8), ("F10", _emitidos_f10)):
        exigidos = _contrato(fase)
        try:
            emitidos = emissor()
        except Exception as erro:  # noqa: BLE001
            print(f"  FALHOU: o produtor do {fase} não pôde ser chamado: {erro!r}")
            falhas += 1
            continue
        faltando = [g for g in exigidos if g not in emitidos]
        if faltando:
            print(f"  FALHOU: o produtor do {fase} não emite {len(faltando)} gate(s) que o "
                  f"contrato exige: {', '.join(faltando)}")
            falhas += 1
        linhas.append(f"{fase}: {len(exigidos) - len(faltando)}/{len(exigidos)} emitidos")

    # O medidor precisa separar as duas dívidas; se voltar a fundi-las, o
    # relatório passa a acusar dívida grave onde só há rota rara.
    from forja_gate_liveness import medir
    laudo = medir()
    if "naoExercitados" not in laudo:
        print("  FALHOU: o medidor voltou a tratar 'sem produtor' e 'rota nunca rodou' "
              "como a mesma coisa")
        falhas += 1
    else:
        sobreposicao = ({i["gate"] for i in laudo["naoExercitados"]}
                        & {i["gate"] for i in laudo["inexequiveis"]})
        if sobreposicao:
            print(f"  FALHOU: {len(sobreposicao)} gate(s) classificados nas duas faixas ao "
                  f"mesmo tempo: {', '.join(sorted(sobreposicao))}")
            falhas += 1
        linhas.append(f"liveness: {len(laudo['naoExercitados'])} não exercitados, "
                      f"{len(laudo['inexequiveis'])} inexequíveis")

    if falhas:
        print(f"REGRESSÃO: {falhas} verificação(ões) de emissão de gate falharam")
        return 1
    print("ok: " + "; ".join(linhas))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
