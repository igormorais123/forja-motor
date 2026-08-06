# -*- coding: utf-8 -*-
"""Executor de mutação semântica em lote.

Roda forja_mutation_semantic.py em múltiplos casos e consolida em painel.

Uso:
  python forja_mutation_lote.py [glob-pattern] [--output painel.json] [--verbose]

Exemplos:
  python forja_mutation_lote.py state/case-email-*
  python forja_mutation_lote.py state/case-email-<caso-a> state/case-email-<caso-b>
  python forja_mutation_lote.py --output mutation_panel.json
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

from forja_mutation_semantic import rodar, _achar_draft, ALVO_SCORE

RAIZ = Path(__file__).resolve().parent


def _encontrar_casos(padroes: list[str] = None) -> list[Path]:
    """Encontra casos por padrão glob. Se vazio, retorna todos."""
    if not padroes:
        padroes = [str(RAIZ / "state" / "case-*")]

    cases = []
    for padrao in padroes:
        p = Path(padrao)
        if p.is_dir():
            cases.append(p)
        else:
            matches = list((RAIZ / "state").glob(Path(padrao).name))
            cases.extend(matches)

    return sorted(set(cases))


def rodar_lote(case_dirs: list[Path], verbose: bool = False) -> list[dict]:
    """Roda harness em cada caso."""
    resultados = []

    for case_dir in case_dirs:
        case_id = case_dir.name

        if verbose:
            print(f"Rodando {case_id}...", file=sys.stderr)

        # Achar draft
        draft = _achar_draft(case_dir)
        if draft is None:
            if verbose:
                print(f"  ✗ Draft não localizado", file=sys.stderr)
            continue

        # Achar suite
        suite = {}
        suite_path = case_dir / "n4_artifacts" / "F4_CASE_ACCEPTANCE_TESTS.json"
        if suite_path.is_file():
            try:
                suite = json.loads(suite_path.read_text(encoding="utf-8"))
            except:
                pass

        # Rodar harness
        try:
            resultado = rodar(suite, draft, case_dir=case_dir)
            resultado["caseId"] = case_id
            resultado["suite"] = str(suite_path) if suite_path.is_file() else None
            resultados.append(resultado)

            if verbose:
                score = resultado["semanticMutationScore"]
                mortos = resultado["mortos"]
                aplicaveis = resultado["aplicaveis"]
                print(f"  ✓ Score: {score:.4f} ({mortos}/{aplicaveis})", file=sys.stderr)
                if resultado["controlesMortos"]:
                    print(f"    Controles mortos: {resultado['controlesMortos']}", file=sys.stderr)
        except Exception as e:
            if verbose:
                print(f"  ✗ Erro: {e}", file=sys.stderr)

    return resultados


def consolidar_painel(resultados: list[dict]) -> dict:
    """Consolida resultados em painel."""
    familia_stats = defaultdict(lambda: {"aplicaveis": 0, "mortos": 0, "casos": []})
    casos_resumo = []

    for resultado in resultados:
        case_id = resultado["caseId"]
        score = resultado["semanticMutationScore"]
        casos_resumo.append({
            "case": case_id,
            "score": score,
            "mortos": resultado["mortos"],
            "aplicaveis": resultado["aplicaveis"],
            "suite_valida": resultado["suiteValida"],
            "controles_mortos": resultado["controlesMortos"],
        })

        for familia, stats in resultado["porFamilia"].items():
            aplicaveis = stats["aplicaveis"]
            mortos = stats["mortos"]
            if aplicaveis > 0:
                familia_stats[familia]["aplicaveis"] += aplicaveis
                familia_stats[familia]["mortos"] += mortos
                familia_stats[familia]["casos"].append({
                    "case": case_id,
                    "score": stats["score"],
                    "mortos": mortos,
                    "aplicaveis": aplicaveis,
                })

    # Calcular agregados
    familia_resumo = {}
    for familia in sorted(familia_stats.keys()):
        stats = familia_stats[familia]
        score = stats["mortos"] / stats["aplicaveis"] if stats["aplicaveis"] > 0 else 0
        familia_resumo[familia] = {
            "score": round(score, 4),
            "mortos": stats["mortos"],
            "aplicaveis": stats["aplicaveis"],
            "casos": len(stats["casos"]),
            "pronto": score >= ALVO_SCORE,
        }

    total_aplicaveis = sum(f["aplicaveis"] for f in familia_resumo.values())
    total_mortos = sum(f["mortos"] for f in familia_resumo.values())
    escore_geral = total_mortos / total_aplicaveis if total_aplicaveis > 0 else 0

    return {
        "schemaVersion": 1,
        "artifactType": "MUTATION_LOTE_PAINEL",
        "totalCasos": len(resultados),
        "casosResumo": casos_resumo,
        "familiaResumo": familia_resumo,
        "agregado": {
            "score": round(escore_geral, 4),
            "mortos": total_mortos,
            "aplicaveis": total_aplicaveis,
            "casosProntosParaProducao": len([c for c in casos_resumo if c["score"] >= ALVO_SCORE]),
        },
    }


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]

    # Parser simples
    padroes = []
    output_path = None
    verbose = False

    i = 0
    while i < len(argv):
        if argv[i] == "--output":
            output_path = Path(argv[i + 1])
            i += 2
        elif argv[i] == "--verbose":
            verbose = True
            i += 1
        elif argv[i].startswith("-"):
            print(f"Opção desconhecida: {argv[i]}", file=sys.stderr)
            return 2
        else:
            padroes.append(argv[i])
            i += 1

    # Encontrar casos
    case_dirs = _encontrar_casos(padroes)
    if not case_dirs:
        print("Nenhum caso encontrado", file=sys.stderr)
        return 2

    if verbose:
        print(f"Encontrados {len(case_dirs)} casos", file=sys.stderr)

    # Rodar lote
    resultados = rodar_lote(case_dirs, verbose=verbose)

    if not resultados:
        print("Nenhum resultado coletado", file=sys.stderr)
        return 1

    if verbose:
        print(f"Processados: {len(resultados)}/{len(case_dirs)}", file=sys.stderr)

    # Consolidar painel
    painel = consolidar_painel(resultados)

    # Salvar
    if output_path:
        output_path.write_text(json.dumps(painel, ensure_ascii=False, indent=1), encoding="utf-8")
        if verbose:
            print(f"Painel salvo em {output_path}", file=sys.stderr)

    # Imprimir resumo
    print()
    print("=" * 80)
    print("PAINEL DE MUTACAO SEMANTICA")
    print("=" * 80)
    print()

    print(f"Escore geral: {painel['agregado']['score']:.4f} ({painel['agregado']['mortos']}/{painel['agregado']['aplicaveis']})")
    print(f"Casos prontos: {painel['agregado']['casosProntosParaProducao']}/{painel['totalCasos']}")
    print()

    print("Por família:")
    for familia, resumo in painel["familiaResumo"].items():
        status = "✓" if resumo["pronto"] else "✗"
        print(f"  {status} {familia}: {resumo['score']:.4f} ({resumo['mortos']}/{resumo['aplicaveis']})")

    print()
    print("=" * 80)

    return 0


if __name__ == "__main__":
    sys.exit(main())
