# -*- coding: utf-8 -*-
"""forja_canario_catraca.py — a catraca sabe reprovar?

O harness mede a si mesmo com quatro instrumentos, e cada um é guardado por uma
"catraca": uma constante no topo do teste que fixa o número medido e só admite
melhora. É o mecanismo que impede uma regressão de passar despercebida.

Nenhuma delas jamais foi vista falhando.

Uma catraca pode ser decorativa de dois jeitos, e os dois são invisíveis quando
tudo está verde:

  1. **A constante existe e ninguém a compara.** Alguém a declara, esquece de
     usá-la no corpo do teste, e ela vira comentário com sintaxe de código. O
     teste passa para sempre, inclusive quando o número piora.
  2. **A constante é afrouxada em vez de defendida.** Quando a realidade piora,
     mexer no número é mais barato que investigar — e o instrumento que deveria
     acusar o retrocesso passa a documentá-lo. Isto aqui não impede a mudança;
     ela às vezes é legítima. O que ele faz é tirá-la do silêncio, exibindo cada
     catraca com o valor vigente para que afrouxar seja uma decisão visível.

O método é o do canário de mutação, aplicado ao instrumento em vez do artefato:
aperto a catraca para um valor que a realidade não pode satisfazer e exijo que o
teste REPROVE. Catraca que continua verde diante do impossível não guarda nada.

Uso:
    python forja_canario_catraca.py
    python forja_canario_catraca.py --json saida.json
    python forja_canario_catraca.py --suite test_forja_forma_artefatos.py
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

VERSAO = "FORJA-CANARIO-CATRACA-v1"
RAIZ = Path(__file__).resolve().parent

# Constante de catraca: MAIÚSCULA no nível do módulo, valor inteiro, sufixo que
# declara a direção. `_MIN` é piso (o universo medido não pode encolher); `_MAX`
# é teto (o número de defeitos não pode crescer).
_CONSTANTE = re.compile(r"^([A-Z][A-Z0-9_]*_(?:MIN|MAX|MINIMAS|MINIMO|MAXIMO))\s*=\s*(\d+)\s*$",
                        re.M)

# O canário roda cada suíte uma vez por catraca. Suíte cara multiplicada por
# muitas catracas passa de dez minutos, e um instrumento que ninguém tem paciência
# de rodar é um instrumento morto. Estas ficam de fora por custo, e a exclusão é
# nominal para não virar recorte silencioso.
CARAS = {
    "test_forja_recomputo_censo.py": "o censo percorre 60+ tentativas reais por execução",
}


def catracas(suites: list[str] | None = None) -> list[dict]:
    achadas = []
    for arquivo in sorted(RAIZ.glob("test_*.py")):
        if suites and arquivo.name not in suites:
            continue
        texto = arquivo.read_text(encoding="utf-8")
        for nome, valor in _CONSTANTE.findall(texto):
            # A constante precisa ser CONSULTADA, não só declarada. Se aparece uma
            # única vez no arquivo, ela é a própria atribuição e mais nada.
            usos = len(re.findall(rf"\b{re.escape(nome)}\b", texto))
            achadas.append({
                "suite": arquivo.name,
                "constante": nome,
                "valor": int(valor),
                "direcao": "piso" if nome.endswith(("_MIN", "_MINIMO", "_MINIMAS")) else "teto",
                "usos": usos,
                "declaradaSemUso": usos <= 1,
            })
    return achadas


_RUNNER = """
import runpy, sys, types
mod = types.ModuleType("alvo")
mod.__file__ = {arquivo!r}
codigo = compile(open({arquivo!r}, encoding="utf-8").read(), {arquivo!r}, "exec")
sys.argv = [{arquivo!r}]
glob = {{"__name__": "alvo", "__file__": {arquivo!r}}}
exec(codigo, glob)
glob[{constante!r}] = {impossivel!r}
sys.exit(int(glob["main"]()))
"""


def _aperta(entrada: dict) -> dict:
    """Aperta a catraca para o impossível e cobra a reprovação."""
    arquivo = str(RAIZ / entrada["suite"])
    # Piso impossível: um universo que nenhum acervo real alcança. Teto
    # impossível: menos defeitos que zero. Os dois são inatingíveis por
    # construção, então qualquer verde é prova de que ninguém consultou a
    # constante.
    impossivel = entrada["valor"] + 10 ** 7 if entrada["direcao"] == "piso" else -1
    script = _RUNNER.format(arquivo=arquivo, constante=entrada["constante"],
                            impossivel=impossivel)
    try:
        proc = subprocess.run([sys.executable, "-c", script], cwd=str(RAIZ),
                              capture_output=True, text=True, encoding="utf-8",
                              errors="replace", timeout=900)
        codigo = proc.returncode
        erro = "" if codigo in (0, 1) else (proc.stderr or "")[-400:]
    except subprocess.TimeoutExpired:
        codigo, erro = None, "estourou 900s"
    return {**entrada, "apertadaPara": impossivel, "exit": codigo,
            "reprovou": codigo == 1, "erro": erro}


def canario(suites: list[str] | None = None) -> dict:
    todas = catracas(suites)
    examinadas, puladas = [], []
    for entrada in todas:
        motivo = CARAS.get(entrada["suite"])
        if motivo and not suites:
            puladas.append({**entrada, "motivo": motivo})
            continue
        examinadas.append(_aperta(entrada))

    decorativas = [x for x in examinadas if not x["reprovou"]]
    return {
        "versao": VERSAO,
        "catracasEncontradas": len(todas),
        "examinadas": len(examinadas),
        "reprovaramOImpossivel": len(examinadas) - len(decorativas),
        "decorativas": decorativas,
        "puladasPorCusto": puladas,
        "declaradasSemUso": [x for x in todas if x["declaradaSemUso"]],
        "detalhe": examinadas,
    }


def _relatar(laudo: dict) -> None:
    print("=" * 78)
    print("CANÁRIO DE CATRACA — a catraca sabe reprovar?")
    print("=" * 78)
    print(f"  catracas encontradas   : {laudo['catracasEncontradas']}")
    print(f"  examinadas             : {laudo['examinadas']}")
    print(f"  reprovaram o impossível: {laudo['reprovaramOImpossivel']}")
    for x in laudo["puladasPorCusto"]:
        print(f"  pulada por custo       : {x['suite']}::{x['constante']} — {x['motivo']}")
    if laudo["declaradasSemUso"]:
        print("\n  DECLARADAS E NUNCA CONSULTADAS")
        for x in laudo["declaradasSemUso"]:
            print(f"    {x['suite']}::{x['constante']}")
    if laudo["decorativas"]:
        print("\n  DECORATIVAS — continuaram verdes com a catraca no impossível")
        for x in laudo["decorativas"]:
            print(f"    {x['suite']}::{x['constante']} = {x['valor']} "
                  f"(apertada para {x['apertadaPara']}, exit {x['exit']}) {x['erro']}")
    else:
        print("\n  nenhuma catraca decorativa entre as examinadas")

    print("\n  VALORES VIGENTES (afrouxar é decisão, não acidente)")
    for x in sorted(laudo["detalhe"], key=lambda y: (y["suite"], y["constante"])):
        print(f"    {x['direcao']:5} {x['valor']:>8}  {x['suite']}::{x['constante']}")


if __name__ == "__main__":  # pragma: no cover
    import argparse

    ap = argparse.ArgumentParser(description="Prova que as catracas do harness reprovam.")
    ap.add_argument("--json", metavar="ARQUIVO")
    ap.add_argument("--suite", action="append", metavar="test_x.py")
    args = ap.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    laudo = canario(args.suite)
    _relatar(laudo)
    if args.json:
        Path(args.json).write_text(json.dumps(laudo, ensure_ascii=False, indent=2),
                                   encoding="utf-8")
        print(f"\ncanário: {args.json}")
    raise SystemExit(1 if laudo["decorativas"] or laudo["declaradasSemUso"] else 0)
