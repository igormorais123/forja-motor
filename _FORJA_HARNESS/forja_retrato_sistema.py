# -*- coding: utf-8 -*-
"""forja_retrato_sistema.py — quanto da esteira desenhada é esteira usada.

Existe porque as perguntas "o que já funciona, o que está parcial e o que é
plano" não se respondem lendo documentação: a documentação descreve o desenho,
e o desenho é o que se pretendeu, não o que aconteceu. A diferença entre os
dois é a informação inteira.

O retrato responde três coisas que nenhum artefato isolado responde:

  1. Quantos casos entraram e quantos percorreram a esteira formal. Caso que
     tem pasta e não tem execução é trabalho conduzido à mão — legítimo, e
     invisível para todo controle instalado na rota automática.
  2. Onde a esteira afunila. A contagem por fase mostra em que etapa os casos
     param, e a etapa que mais roda diz qual é o uso real do sistema.
  3. Quanto do aprendizado tem procedência declarada. Regra sem origem
     continua valendo e não se sabe defender.

A vitalidade dos gates NÃO é recalculada aqui: quem responde por ela é
`forja_gate_liveness.py`, e duplicar o cálculo criaria duas verdades. Este
script chama aquele e repassa o veredito.

Uso: python forja_retrato_sistema.py [--json]
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

_NOME_DE_FASE = re.compile(r"^F\d+")

FORJA = Path(__file__).resolve().parent
ESTADO = FORJA / "state"
REGISTRO_APRENDIZADO = FORJA / "learning_registry" / "REGRAS_APRENDIDAS.json"

# Marcas de que o executor formal rodou naquele caso, e não só de que alguém
# criou a pasta. `FORJA_EVENTS.jsonl` é o mais honesto dos três: ele só existe
# quando uma fase efetivamente iniciou.
MARCAS_DE_EXECUCAO = ("FORJA_EVENTS.jsonl", "FORJA_N3_STATE.json", "PHASE_RESULT.json")


def _fase_do_resultado(caminho: Path, dados: dict) -> str:
    """A fase declarada pelo artefato; na falta dela, a pasta que o abriga.

    Tentativas de F7 moram em subpastas `ATTEMPT-<uuid>`, e cair na pasta-pai
    direta transformaria cada nova tentativa numa "fase" própria: o retrato
    ganharia dez fases inexistentes e perderia as sete execuções de F7 que elas
    de fato são. Sobe-se até a primeira pasta que se chame como fase.
    """
    fase = dados.get("phase") or dados.get("fase")
    if not fase:
        pasta = caminho.parent
        while pasta != ESTADO and not _NOME_DE_FASE.match(pasta.name):
            pasta = pasta.parent
        fase = pasta.name
    achado = _NOME_DE_FASE.match(str(fase))
    return achado.group(0) if achado else str(fase).split("_", 1)[0].upper()


def medir() -> dict:
    casos = sorted(d for d in ESTADO.iterdir() if d.is_dir()) if ESTADO.is_dir() else []
    com_execucao = []
    com_resultado_de_fase = []
    fases = Counter()
    resultados = 0

    for caso in casos:
        executou = False
        for marca in MARCAS_DE_EXECUCAO:
            if any(caso.rglob(marca)):
                executou = True
                break
        if executou:
            com_execucao.append(caso.name)
        if any(caso.rglob("PHASE_RESULT.json")):
            com_resultado_de_fase.append(caso.name)
        for resultado in caso.rglob("PHASE_RESULT.json"):
            resultados += 1
            try:
                dados = json.loads(resultado.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            if isinstance(dados, dict):
                fases[_fase_do_resultado(resultado, dados)] += 1

    regras, com_origem = [], 0
    try:
        registro = json.loads(REGISTRO_APRENDIZADO.read_text(encoding="utf-8"))
        regras = registro.get("regras") or []
        com_origem = sum(1 for r in regras if r.get("origem"))
    except (OSError, ValueError):
        pass

    # Os dois critérios medem coisas diferentes e a distância entre eles é o
    # achado: abrir o caso na esteira é barato, levá-lo por fases com resultado
    # registrado é o que custa. Colapsar os dois num número só esconde qual das
    # duas coisas aconteceu.
    return {
        "casos": len(casos),
        "casosComExecucao": len(com_execucao),
        "casosComResultadoDeFase": len(com_resultado_de_fase),
        "resultadosDeFase": resultados,
        "execucoesPorFase": dict(sorted(fases.items())),
        "regras": len(regras),
        "regrasComOrigemDeclarada": com_origem,
    }


def _liveness() -> dict:
    """Delega ao dono do assunto. Duas contagens do mesmo gate seriam duas verdades.

    Só os totais entram no retrato; a lista nominal de cada balde continua no
    laudo de origem, que é onde ela é acionável.
    """
    sys.path.insert(0, str(FORJA))
    import forja_gate_liveness as live

    laudo = live.medir()
    return {
        "resultadosExaminados": laudo["resultadosExaminados"],
        "declarados": laudo["gatesDeclarados"],
        "observados": laudo["gatesObservados"],
        "computadosPorCodigo": len(laudo["computados"]),
        "atestadosPeloAgente": len(laudo["autodeclarados"]),
        "inexequiveis": len(laudo["inexequiveis"]),
        "naoExercitados": len(laudo["naoExercitados"]),
        "complacentes": len(laudo["complacentes"]),
        "orfaos": len(laudo["orfaos"]),
        "ativos": len(laudo["ativos"]),
    }


def main(argv: list[str]) -> int:
    retrato = medir()
    try:
        retrato["gates"] = _liveness()
    except Exception as erro:  # noqa: BLE001 — a ausência do laudo é declarada, não silenciada
        retrato["gates"] = {"indisponivel": str(erro)}

    if "--json" in argv:
        print(json.dumps(retrato, ensure_ascii=False, indent=2))
        return 0

    print("=" * 66)
    print("RETRATO DO SISTEMA — desenho contra uso")
    print("=" * 66)
    print(f"  casos com pasta de estado      : {retrato['casos']}")
    print(f"  casos que abriram na esteira   : {retrato['casosComExecucao']}")
    print(f"  casos com resultado de fase    : {retrato['casosComResultadoDeFase']}")
    print(f"  resultados de fase registrados : {retrato['resultadosDeFase']}")
    print()
    print("  EXECUÇÕES POR FASE (arquivos PHASE_RESULT.json)")
    if not retrato["execucoesPorFase"]:
        print("    nenhuma")
    for fase, n in retrato["execucoesPorFase"].items():
        print(f"    {fase:6} {n:4}")
    print()
    print(f"  regras aprendidas em vigor  : {retrato['regras']}")
    print(f"  com procedência declarada   : {retrato['regrasComOrigemDeclarada']}")
    print()
    print("  A vitalidade dos gates é responsabilidade de forja_gate_liveness.py.")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main(sys.argv[1:]))
