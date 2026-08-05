# -*- coding: utf-8 -*-
"""
bancada_relatorio.py — Junta as duas camadas e produz o quadro final.

A nota final não é média das duas camadas. É composição com papéis distintos:
a camada determinística tem **poder de veto** e a camada de juízes tem poder de
ordenar. Peça que inventa autoridade não sobe por ser bem escrita; peça limpa
mas medíocre não vence por ser limpa.

Uso: python bancada_relatorio.py
"""
from __future__ import annotations

import io
import json
import sys
from pathlib import Path

BANCADA = Path(__file__).resolve().parent

PESO_DETERMINISTICO = 0.55
PESO_JUIZES = 0.45


def _carregar() -> tuple[dict, dict | None]:
    det = json.loads((BANCADA / "avaliacao" / "DETERMINISTICA.json")
                     .read_text(encoding="utf-8"))["resultados"]
    caminho = BANCADA / "avaliacao" / "JUIZES_CONSOLIDADO.json"
    juizes = json.loads(caminho.read_text(encoding="utf-8")) if caminho.is_file() else None
    return det, juizes


def compor(det: dict, juizes: dict | None) -> list[dict]:
    linhas = []
    n = len(det)
    for nome, a in det.items():
        nota_det = a["pontuacao"]["nota"]
        jd = (juizes or {}).get("porParticipante", {}).get(nome, {})
        media = jd.get("mediaGeral")
        # Borda ENTRE FAMÍLIAS, normalizado de 0 a 100. Uso a versão cruzada
        # porque o Borda bruto premia quem julga e concorre: o campeão seria,
        # em parte, eleito pelo próprio voto.
        media_cruzada = jd.get("bordaEntreFamiliasMedia")
        borda_norm = (100.0 * media_cruzada / (n - 1)) if media_cruzada is not None else None
        # O juiz fala por dois canais: a nota por critério e a ordem. Uso os
        # dois, porque nota infla e ordem discrimina.
        nota_jui = (None if media is None and borda_norm is None else
                    round(((media * 10 if media is not None else 0) +
                           (borda_norm if borda_norm is not None else 0)) /
                          (int(media is not None) + int(borda_norm is not None)), 1))
        final = (round(nota_det * PESO_DETERMINISTICO + nota_jui * PESO_JUIZES, 1)
                 if nota_jui is not None else nota_det)
        # O teto da camada determinística vale para a nota final: é veto, não desconto.
        teto = a["pontuacao"]["teto"]
        linhas.append({
            "participante": nome,
            "notaFinal": min(final, teto),
            "notaDeterministica": nota_det,
            "notaJuizes": nota_jui,
            "teto": teto,
            "tetosAplicados": a["pontuacao"]["tetosAplicados"],
            "palavras": a["palavras"],
            "inventadas": len(a["autoridades"]["novasAfirmadas"]),
            "declaradas": len(a["autoridades"]["novasDeclaradas"]),
            "canarios": [c["id"] for c in a["canarios"] if c["acionado"]],
            "similaridade": a.get("similaridadeV6"),
            "custoUsd": a["meta"].get("custoUsd"),
            "segundos": a["meta"].get("segundos"),
            "truncada": a["meta"].get("truncada"),
        })
    return sorted(linhas, key=lambda x: -x["notaFinal"])


def main() -> int:
    det, juizes = _carregar()
    linhas = compor(det, juizes)
    (BANCADA / "avaliacao" / "QUADRO_FINAL.json").write_text(
        json.dumps({"pesos": {"deterministico": PESO_DETERMINISTICO,
                              "juizes": PESO_JUIZES},
                    "quadro": linhas}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")

    print("=" * 100)
    print("QUADRO FINAL — BANCADA CAFELANA V7")
    print("=" * 100)
    print(f"{'#':<3}{'participante':<12}{'final':>7}{'determ':>8}{'juízes':>8}"
          f"{'palavras':>10}{'invent':>8}{'contenção':>11}{'US$':>8}{'seg':>7}")
    print("-" * 100)
    for i, r in enumerate(linhas, 1):
        sim = (r["similaridade"] or {}).get("contencao")
        nj = f"{r['notaJuizes']:.1f}" if r["notaJuizes"] is not None else "—"
        print(f"{i:<3}{r['participante']:<12}{r['notaFinal']:>7.1f}"
              f"{r['notaDeterministica']:>8.1f}{nj:>8}"
              f"{r['palavras']:>10}{r['inventadas']:>8}"
              f"{(f'{sim:.3f}' if sim is not None else '—'):>11}"
              f"{(r['custoUsd'] or 0):>8.3f}{(r['segundos'] or 0):>7.0f}")
    print("-" * 100)
    total = sum(r["custoUsd"] or 0 for r in linhas)
    if juizes:
        total += juizes.get("custoUsd", 0)
    print(f"  custo total da bancada: US$ {total:.2f}")
    for r in linhas:
        if r["tetosAplicados"] or r["canarios"]:
            print(f"  {r['participante']}: " + "; ".join(
                r["tetosAplicados"] + [f"canário {c}" for c in r["canarios"]]))
    return 0


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    raise SystemExit(main())
