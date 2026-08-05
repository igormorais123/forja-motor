# -*- coding: utf-8 -*-
"""Geração 0 — bateria exaustiva do gate de legibilidade e dos geradores de SVG.
Objetivo: encontrar FUROS no gate (casos em que texto pequeno passa despercebido)
e falsos positivos (casos em que o gate reprova texto legítimo)."""
import os, sys, json, subprocess, traceback

BASE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
sys.path.insert(0, BASE)
import estilo_medina as em
import word_visual_pipeline as wvp

OUT = os.path.dirname(os.path.abspath(__file__))
resultados = []

def caso(nome, esperado, obtido, detalhe=""):
    ok = (esperado == obtido)
    resultados.append({"caso": nome, "esperado": esperado, "obtido": obtido,
                       "ok": ok, "detalhe": detalhe})
    print(("PASS " if ok else "FURO ") + nome + ("  -> " + detalhe if detalhe else ""))

def svg_teste(nome, corpo, viewbox='0 0 600 200'):
    path = os.path.join(OUT, nome)
    with open(path, "w", encoding="utf-8") as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}">{corpo}</svg>')
    return path

def checa(path):
    try:
        v = em.checar_fontes_svg(path, 15)
        return "reprova" if v else "aprova", str(v)
    except ValueError as e:
        return "erro", str(e)[:120]

# --- grupo A: detecção básica (deve reprovar) ---
r, d = checa(svg_teste("a1_attr_px.svg", '<text font-size="10px" x="10" y="50">réu</text>'))
caso("A1 atributo font-size=10px", "reprova", r, d)

r, d = checa(svg_teste("a2_attr_sem_unidade.svg", '<text font-size="10" x="10" y="50">réu</text>'))
caso("A2 atributo font-size=10 sem unidade", "reprova", r, d)

r, d = checa(svg_teste("a3_style_inline.svg", '<text style="font-size:10px" x="10" y="50">réu</text>'))
caso("A3 style inline font-size:10px", "reprova", r, d)

r, d = checa(svg_teste("a4_css_bloco.svg", '<style>text{font-size:10px}</style><text x="10" y="50">réu</text>'))
caso("A4 bloco CSS font-size", "reprova", r, d)

r, d = checa(svg_teste("a5_decimal.svg", '<text font-size="10.5" x="10" y="50">réu</text>'))
caso("A5 decimal 10.5px", "reprova", r, d)

# --- grupo B: casos que devem APROVAR (falso positivo = furo de usabilidade) ---
r, d = checa(svg_teste("b1_ok_12px.svg", '<text font-size="12" x="10" y="50">réu</text>'))
caso("B1 12px em viewBox 600 @15cm (8,5pt)", "aprova", r, d)

r, d = checa(svg_teste("b2_ok_grande.svg", '<text font-size="16" x="10" y="50">réu</text>'))
caso("B2 16px", "aprova", r, d)

# --- grupo C: FUROS suspeitos (texto pequeno que o gate talvez não veja) ---
r, d = checa(svg_teste("c1_font_shorthand.svg",
    '<text style="font: 400 9px \'Segoe UI\'" x="10" y="50">réu</text>'))
caso("C1 shorthand CSS font: 9px (matplotlib usa)", "reprova", r, d)

r, d = checa(svg_teste("c2_unidade_pt.svg", '<text font-size="6pt" x="10" y="50">réu</text>'))
caso("C2 font-size=6pt (unidade pt)", "reprova", r, d)

r, d = checa(svg_teste("c3_sem_fontsize.svg", '<text x="10" y="50">réu sem font-size</text>'))
caso("C3a sem font-size em viewBox 600 (default 16px = 11,3pt)", "aprova", r, d)

r, d = checa(svg_teste("c3b_sem_fontsize_largo.svg", '<text x="10" y="50">réu sem font-size</text>', viewbox="0 0 1400 300"))
caso("C3b sem font-size em viewBox 1400 (default 16px = 4,9pt)", "reprova", r, d)

r, d = checa(svg_teste("c4_viewbox_virgulas.svg", '<text font-size="9" x="10" y="50">réu</text>', viewbox="0, 0, 600, 200"))
caso("C4 viewBox com vírgulas avalia normalmente", "reprova", r, d)

r, d = checa(svg_teste("c5_viewbox_offset.svg", '<text font-size="9" x="10" y="50">réu</text>', viewbox="10 10 600 200"))
caso("C5 viewBox com offset avalia pela largura", "reprova", r, d)

r, d = checa(svg_teste("c8_pt_grande.svg", '<text font-size="14pt" x="10" y="50">réu</text>'))
caso("C8 font-size=14pt (18,7px = 13,2pt) sem falso positivo", "aprova", r, d)

r, d = checa(svg_teste("c6_em_unidade.svg", '<text font-size="0.5em" x="10" y="50">réu</text>'))
caso("C6 font-size=0.5em (8px = 5,7pt)", "reprova", r, d)

# tspan herdando de <g>
r, d = checa(svg_teste("c7_g_heranca.svg", '<g font-size="9"><text x="10" y="50">réu</text></g>'))
caso("C7 font-size=9 herdado de <g>", "reprova", r, d)

# --- grupo D: geradores reais produzem SVG que o gate consegue ler? ---
# D1 Graphviz com ESTILO_GRAPHVIZ
dot = os.path.join(OUT, "d1_fluxo.dot")
with open(dot, "w", encoding="utf-8") as f:
    f.write('digraph G { rankdir=LR; ' + em.ESTILO_GRAPHVIZ +
            ' a[label="Sentença"]; b[label="Apelação"]; c[label="Acórdão"]; a->b->c; }')
d1 = os.path.join(OUT, "d1_fluxo.svg")
try:
    wvp.dot_para_svg(dot, d1)
    r, det = checa(d1)
    caso("D1 Graphviz gera SVG auditável pelo gate", True, r in ("aprova", "reprova"),
         f"gate={r} {det}")
except Exception as e:
    caso("D1 Graphviz gera SVG legível pelo gate", True, False, str(e)[:150])

# D2 Mermaid com TEMA_MERMAID
mmd = os.path.join(OUT, "d2_timeline.mmd")
cfg = os.path.join(OUT, "d2_cfg.json")
with open(mmd, "w", encoding="utf-8") as f:
    f.write("flowchart LR\n  A[Sentença] --> B[Apelação] --> C[Acórdão]\n")
with open(cfg, "w", encoding="utf-8") as f:
    json.dump(em.TEMA_MERMAID, f)
d2 = os.path.join(OUT, "d2_timeline.svg")
try:
    subprocess.run([wvp.MMDC, "-i", mmd, "-o", d2, "-w", "1400", "-b", "transparent",
                    "-c", cfg], check=True, capture_output=True, text=True)
    r, det = checa(d2)
    caso("D2 Mermaid+tema gera SVG auditável", True, r in ("aprova", "reprova"),
         f"gate={r} {det[:100]}")
except Exception as e:
    caso("D2 Mermaid+tema gera SVG auditável", True, False, str(e)[:200])

# D3 matplotlib com aplicar_estilo_matplotlib -> SVG: o gate enxerga as fontes?
try:
    import matplotlib
    matplotlib.use("Agg")
    em.aplicar_estilo_matplotlib()
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.bar(["2019", "2021", "2024"], [120, 340, 90])
    ax.set_title("Evolução do débito (R$ mil)")
    d3 = os.path.join(OUT, "d3_matplotlib.svg")
    fig.savefig(d3)
    plt.close(fig)
    with open(d3, encoding="utf-8") as f:
        conteudo = f.read()
    tem_fontsize = "font-size" in conteudo
    tem_shorthand = re.search(r'font:\s', conteudo) is not None if (re := __import__("re")) else False
    r, det = checa(d3)
    caso("D3 matplotlib SVG auditável pelo gate", True,
         r in ("aprova", "reprova") and tem_fontsize,
         f"gate={r} font-size_presente={tem_fontsize} shorthand_font={tem_shorthand} {det[:80]}")
except Exception as e:
    caso("D3 matplotlib SVG auditável pelo gate", True, False, traceback.format_exc()[-200:])

# --- grupo E: gate embutido no svg_para_emf ---
ruim = svg_teste("e1_ruim.svg", '<text font-size="9" x="10" y="50">texto pequeno</text>')
try:
    wvp.svg_para_emf(ruim, os.path.join(OUT, "e1.emf"), largura_final_cm=15)
    caso("E1 svg_para_emf bloqueia SVG reprovado", "bloqueia", "passou", "EMF gerado indevidamente")
except ValueError as e:
    caso("E1 svg_para_emf bloqueia SVG reprovado", "bloqueia", "bloqueia", str(e)[:100])

bom = svg_teste("e2_bom.svg", '<text font-size="13" font-family="Segoe UI" x="10" y="60">Texto legível de diagrama</text>')
try:
    emf = wvp.svg_para_emf(bom, os.path.join(OUT, "e2.emf"), largura_final_cm=15)
    tam = os.path.getsize(emf)
    caso("E2 svg_para_emf converte SVG aprovado", True, tam > 100, f"EMF {tam} bytes")
except Exception as e:
    caso("E2 svg_para_emf converte SVG aprovado", True, False, str(e)[:150])

# --- resumo ---
furos = [r for r in resultados if not r["ok"]]
print(f"\n=== {len(resultados)} casos, {len(furos)} furos ===")
with open(os.path.join(OUT, "scores.json"), "w", encoding="utf-8") as f:
    json.dump(resultados, f, ensure_ascii=False, indent=1)
sys.exit(0)
