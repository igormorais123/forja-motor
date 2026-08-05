# -*- coding: utf-8 -*-
"""QA determinístico de páginas renderizadas (M4.2 do plano 19).

Complementa o QA visual do F8 com três detecções baratas sobre os PNGs de
página (a colisão interna de diagrama "que só o zoom pega" aparece como
anomalia de densidade):

1. densidade anômala — fração de pixels não-brancos muito acima da faixa das
   demais páginas do documento (diagrama estourado, mancha, sobreposição);
2. página em branco no meio do documento (quebra de seção errada);
3. conteúdo colado na borda inferior (corte de rodapé/diagrama no render).

O que continua manual permanece manual (estratégia visual, hierarquia) — sem
teatro de automação. Achado = P1 nominado; a decisão de regenerar é do agente.

Uso: python forja_qa_paginas.py <pasta-com-p01.png...> [--json saida.json]
Exit: 0 sem achados; 1 com achados; 2 erro de uso.
"""
from __future__ import annotations

import io
import json
import statistics
import sys
from pathlib import Path

from PIL import Image

LIMIAR_BRANCO = 245          # pixel com todos os canais >= 245 conta como fundo
DENSIDADE_BRANCO = 0.002     # abaixo disso, página é considerada em branco
FATOR_ANOMALIA = 2.2         # densidade > mediana * fator (e > 3 desvios) = anômala
BORDA_INFERIOR_FRAC = 0.02   # faixa dos 2% finais da altura
DENSIDADE_BORDA_MAX = 0.02   # conteúdo na faixa acima disso = possível corte


def _densidade(img: Image.Image, y0: int = 0, y1: int | None = None) -> float:
    """Fração de pixels não-brancos na faixa vertical [y0, y1)."""
    gray = img.convert("L")
    w, h = gray.size
    y1 = y1 if y1 is not None else h
    faixa = gray.crop((0, y0, w, y1))
    hist = faixa.histogram()
    total = faixa.size[0] * faixa.size[1]
    nao_branco = sum(hist[:LIMIAR_BRANCO])
    return nao_branco / total if total else 0.0


def analisar_pasta(pasta: Path) -> dict:
    paginas = sorted(p for p in Path(pasta).glob("*.png"))
    medidas, achados = [], []
    for p in paginas:
        try:
            with Image.open(p) as img:
                dens = _densidade(img)
                h = img.size[1]
                borda = _densidade(img, y0=int(h * (1 - BORDA_INFERIOR_FRAC)))
        except OSError as exc:
            achados.append({"sev": "P1", "pagina": p.name,
                            "problema": f"PNG ilegível: {exc}"})
            continue
        medidas.append({"pagina": p.name, "densidade": round(dens, 5),
                        "densidadeBordaInferior": round(borda, 5)})

    densidades = [m["densidade"] for m in medidas]
    if len(densidades) >= 3:
        mediana = statistics.median(densidades)
        # MAD em vez de desvio-padrão: o próprio outlier infla o pstdev e se
        # esconde (visto no teste sintético — página 0.85 escapava com σ=0.25)
        mad = statistics.median(abs(d - mediana) for d in densidades)
        for m in medidas:
            d = m["densidade"]
            if mediana > 0 and d > mediana * FATOR_ANOMALIA and \
               (mad == 0 or d > mediana + 6 * mad):
                achados.append({
                    "sev": "P1", "pagina": m["pagina"],
                    "problema": f"densidade anômala ({d:.3f} vs mediana {mediana:.3f}) — "
                                "diagrama estourado/sobreposição? Inspecionar com zoom"})

    for i, m in enumerate(medidas):
        interna = 0 < i < len(medidas) - 1
        if interna and m["densidade"] < DENSIDADE_BRANCO:
            achados.append({"sev": "P1", "pagina": m["pagina"],
                            "problema": "página em branco no meio do documento"})
        # 1ª página isenta da checagem de borda: o template Medina Osório tem
        # rodapé institucional encostado na borda POR PROJETO (validado nos
        # renders reais de CASO-19 em 12/07 — densidade ~0.93 é o rodapé).
        if i > 0 and m["densidadeBordaInferior"] > DENSIDADE_BORDA_MAX:
            achados.append({
                "sev": "P1", "pagina": m["pagina"],
                "problema": f"conteúdo na borda inferior "
                            f"({m['densidadeBordaInferior']:.3f}) — possível corte "
                            "de rodapé/diagrama"})

    return {
        "pasta": str(pasta),
        "paginas": len(medidas),
        "medidas": medidas,
        "achados": achados,     # P1 nominados; decisão de regenerar é do agente
        "aprovado": not achados,
    }


def main(argv=None) -> int:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    argv = argv if argv is not None else sys.argv[1:]
    if not argv:
        print(__doc__)
        return 2
    pasta = Path(argv[0])
    if not pasta.is_dir():
        print(f"pasta não encontrada: {pasta}")
        return 2
    r = analisar_pasta(pasta)
    if "--json" in argv:
        Path(argv[argv.index("--json") + 1]).write_text(
            json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{r['paginas']} páginas analisadas em {pasta}")
    for a in r["achados"]:
        print(f"  {a['sev']} {a['pagina']}: {a['problema']}")
    if not r["achados"]:
        print("  nenhum achado — densidades dentro da faixa")
    return 0 if r["aprovado"] else 1


if __name__ == "__main__":
    sys.exit(main())
