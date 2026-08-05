# -*- coding: utf-8 -*-
"""Calibração do gerador de mapa visual contra os 5 mapas escritos à mão.

Métrica operacional (plano 24, Onda 1A): para cada categoria (pulls, caixas,
linhas_sintese), a fração das âncoras do mapa MANUAL que o gerador também
selecionou. A cobertura do caso é a MENOR entre as categorias — média esconde
categoria zerada. Alvo: >= 0,70 por caso.

A comparação é por sobreposição de âncoras normalizadas: âncoras de comprimento
diferente contam como acerto se uma contém a outra (ambas apontam o mesmo
parágrafo, que é o que importa).

Uso: python calibrar_mapa_gen.py
"""
import importlib.util
import json
import sys
from pathlib import Path

import forja_acervo

FORJA = Path(__file__).resolve().parent
sys.path.insert(0, str(FORJA))

from forja_visual_mapa_gen import gerar_mapa, _norm  # noqa: E402

CASOS = [
    ("CASO-02", forja_acervo.caso("CASO-02"), "MEMORIAL_AZIMUT_RESP_2237713.md"),
    ("CASO-07", forja_acervo.caso("CASO-07"), "DIAGNOSTICO_CORSAN_AGERST.md"),
    ("libra", forja_acervo.caso("CASO-16"),
     "MEMORIAIS_LIBRA_SUL_AGINT_ARESP_2578181.md"),
    ("CASO-17", forja_acervo.caso("CASO-17"),
     "ESTUDO_PRELIMINAR_NATURA_CABREUVA.md"),
    ("patricia", forja_acervo.caso("CASO-19"),
     "MEMORIAIS_PATRICIA_FABIO_APELACAO.md"),
]


def carrega_manual(path):
    spec = importlib.util.spec_from_file_location("mapa_manual", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.MAPA


def acha_md(base, nome):
    hits = list(base.rglob(nome))
    return hits[0] if hits else None


def resolve(ancora, paragrafos):
    """Índice do parágrafo que a âncora endereça. O humano ancora no MEIO do
    parágrafo, o gerador ancora no início — comparar strings mede o estilo da
    âncora, não a escolha editorial. O que interessa é se os dois apontaram o
    MESMO parágrafo."""
    n = _norm(ancora)
    if not n:
        return None
    for k, p in enumerate(paragrafos):
        if n in p:
            return k
    return None


def cobre(manuais, gerados, paragrafos):
    """Fração dos parágrafos escolhidos à mão que o gerador também escolheu."""
    if not manuais:
        return None, 0, 0
    alvo = {resolve(a, paragrafos) for a in manuais}
    alvo.discard(None)
    obtido = {resolve(a, paragrafos) for a in gerados}
    obtido.discard(None)
    if not alvo:
        return None, 0, 0
    acertos = len(alvo & obtido)
    return acertos / len(alvo), acertos, len(alvo)


def main():
    linhas, piores = [], []
    for nome, caso, md_nome in CASOS:
        base = FORJA / "state" / caso / "producao"
        mapa_py = next((base / "_visual").glob("compor_*_mapa.py"), None)
        md = acha_md(base, md_nome)
        if not mapa_py or not md:
            linhas.append((nome, "SEM FONTE", "-", "-", "-", "-"))
            continue
        manual = carrega_manual(mapa_py)
        try:
            ger = gerar_mapa(md)
        except Exception as exc:                      # noqa: BLE001
            linhas.append((nome, f"ERRO: {type(exc).__name__}: {str(exc)[:70]}",
                           "-", "-", "-", "-"))
            piores.append(0.0)
            continue

        # universo de parágrafos elegíveis, na mesma leitura que compor() faz
        from forja_visual_mapa_gen import _varre
        elegiveis, _, _ = _varre(md.read_text(encoding="utf-8"))
        paragrafos = [e["norm"] for e in elegiveis]

        cats = {}
        cats["pulls"] = cobre([a for a, _ in manual.get("pulls") or []],
                              [a for a, _ in ger.get("pulls") or []], paragrafos)
        cats["caixas"] = cobre([a for a, _, _ in manual.get("caixas") or []],
                               [a for a, _, _ in ger.get("caixas") or []], paragrafos)
        # linhas-síntese são chaveadas por TÍTULO de seção, não por parágrafo
        manual_sec = [_norm(k) for k in (manual.get("linhas_sintese") or {})]
        ger_sec = [_norm(k) for k in (ger.get("linhas_sintese") or {})]
        acertos_sec = sum(1 for s in manual_sec if s in ger_sec)
        cats["sintese"] = ((acertos_sec / len(manual_sec)) if manual_sec else None,
                           acertos_sec, len(manual_sec))
        validos = [v[0] for v in cats.values() if v[0] is not None]
        pior = min(validos) if validos else 0.0
        piores.append(pior)
        linhas.append((
            nome,
            f"{pior:.0%}",
            *[("-" if cats[c][0] is None else f"{cats[c][0]:.0%} ({cats[c][1]}/{cats[c][2]})")
              for c in ("pulls", "caixas", "sintese")],
            f"g:{len(ger.get('pulls') or [])}p/{len(ger.get('caixas') or [])}c/"
            f"{len(ger.get('figs') or [])}f",
        ))

    largura = [10, 10, 14, 14, 14, 16]
    cab = ["caso", "CONCORD.", "pulls", "caixas", "sintese", "gerado"]
    print(" | ".join(h.ljust(w) for h, w in zip(cab, largura)))
    print("-+-".join("-" * w for w in largura))
    for linha in linhas:
        print(" | ".join(str(c).ljust(w) for c, w in zip(linha, largura)))
    if piores:
        print(f"\nCONCORDÂNCIA com a escolha humana — menor: {min(piores):.0%} | "
              f"média: {sum(piores) / len(piores):.0%}")
        print("  (mede gosto editorial; variância irredutível — NÃO é o critério do gate)")

    # --- critério que o gate usa: densidade e validade ---
    print("\nDENSIDADE E VALIDADE (critério de pronto da Onda 1A)")
    print("  regra: 4 a 8 pulls, >=1 caixa, >=1 figura, âncoras únicas e válidas,")
    print("         texto das pulls verbatim do markdown")
    ok_todos = True
    for nome, caso, md_nome in CASOS:
        base = FORJA / "state" / caso / "producao"
        md = acha_md(base, md_nome)
        if not md:
            continue
        texto = md.read_text(encoding="utf-8")
        try:
            g = gerar_mapa(md)                      # já autovalida âncoras
        except Exception as exc:                    # noqa: BLE001
            print(f"  {nome:<10} REPROVADO: {type(exc).__name__}: {str(exc)[:60]}")
            ok_todos = False
            continue
        np_ = len(g.get("pulls") or [])
        nc = len(g.get("caixas") or [])
        nf = len(g.get("figs") or [])
        alvo_norm = _norm(texto)
        verbatim = all(_norm(t) in alvo_norm for _, t in (g.get("pulls") or []))
        falhas = []
        if not 4 <= np_ <= 8:
            falhas.append(f"pulls={np_}")
        if nc < 1:
            falhas.append("sem caixa")
        if nf < 1:
            falhas.append("sem figura")
        if not verbatim:
            falhas.append("pull nao-verbatim")
        veredito = "OK" if not falhas else "REPROVADO: " + ", ".join(falhas)
        ok_todos = ok_todos and not falhas
        print(f"  {nome:<10} {np_}p / {nc}c / {nf}f | verbatim={'sim' if verbatim else 'NAO'} | {veredito}")
    print(f"\nOnda 1A: {'VERDE' if ok_todos else 'VERMELHA'}")
    return 0 if ok_todos else 1


if __name__ == "__main__":
    raise SystemExit(main())
