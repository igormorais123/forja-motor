# -*- coding: utf-8 -*-
"""
Tokens de estilo e verificador de legibilidade para diagramas de petições.
Fonte única de verdade para cores, fontes e tamanhos — usar em TODO diagrama
(SVG manual, Graphviz, Mermaid, matplotlib, TikZ) para garantir consistência.

Causa raiz das "fontes pequenas": um SVG com viewBox de 600 px inserido com
15 cm de largura imprime cada px a ~0,71 pt — texto de 10 px vira ~7 pt.
Regra: TODO diagrama passa por checar_fontes_svg() antes de ser convertido
para EMF/PNG. Violação = corrigir o SVG, nunca entregar.
"""
import re

# ---------- PERFIL MEDINA OSÓRIO ----------
CORES = {
    "petroleo": "#395C60",
    "petroleo_escuro": "#2A4548",
    "terracota": "#D9926A",
    "terracota_escura": "#9C5B38",   # setas/traços finos: melhor contraste de impressão
    "grafite": "#49494D",
    "painel_verde": "#EFF4F3",
    "painel_terra": "#FBF2EC",
    "alerta": "#7A2E2E",             # só para descumprimento/risco
    "linha_cinza": "#C9C9C9",
}
FONTE_TEXTO = "Times New Roman"      # corpo da peça
FONTE_DIAGRAMA = "Segoe UI"          # rótulos de diagramas (humanista, legível pequena)
FONTE_DADOS = "Consolas"             # números/tabelas técnicas quando necessário

# Tamanhos mínimos NO TAMANHO FINAL IMPRESSO (pontos tipográficos)
MIN_PT_ROTULO = 8.0        # qualquer texto de diagrama (absoluto — nunca abaixo)
MIN_PT_PRINCIPAL = 9.0     # rótulos principais/nós
MIN_PT_TITULO = 10.5       # títulos internos do diagrama
PT_LEGENDA_FIGURA = 9.0    # legenda "Figura N — ..." abaixo do diagrama

PT_POR_CM = 28.3465


def escala_pt_por_px(viewbox_largura_px: float, largura_final_cm: float) -> float:
    """Quantos pontos tipográficos mede 1 px do SVG quando impresso na largura final."""
    return (largura_final_cm * PT_POR_CM) / viewbox_largura_px


def fonte_px_minima(viewbox_largura_px: float, largura_final_cm: float,
                    min_pt: float = MIN_PT_ROTULO) -> float:
    """Menor font-size (px) permitido num SVG para respeitar o mínimo impresso.
    Ex.: viewBox 600, largura 15cm -> ~11.3 px para 8 pt."""
    return min_pt / escala_pt_por_px(viewbox_largura_px, largura_final_cm)


def _fs_para_px(valor: float, unidade: str) -> float:
    """Converte um font-size declarado para px (referência CSS: 1pt=4/3px, 1em=16px)."""
    u = (unidade or "px").lower()
    if u == "pt":
        return valor * 4.0 / 3.0
    if u in ("em", "rem"):
        return valor * 16.0
    return valor  # px ou sem unidade


def checar_fontes_svg(svg_path: str, largura_final_cm: float,
                      min_pt: float = MIN_PT_ROTULO) -> list:
    """Gate de legibilidade: lista violações [(font_px, pt_efetivo), ...].
    Lista vazia = aprovado.

    Cobre (validado na bateria .autoresearch/pipeline-visual-medina, 08/07/2026):
    - font-size em atributo, style inline e bloco CSS; unidades px/pt/em/rem;
    - shorthand CSS `font: 400 9px 'Segoe UI'` (formato do matplotlib com
      svg.fonttype='none' e de alguns exports);
    - viewBox com decimais/vírgulas/offset (Graphviz emite '0.00 0.00 W H');
    - <text> sem nenhum font-size declarado -> avalia o default do renderizador
      (16px) contra a escala, para não passar texto herdado invisível.
    Limite conhecido: texto convertido em caminhos (svg.fonttype='path') não é
    auditável — usar aplicar_estilo_matplotlib(), que força fonttype='none'."""
    with open(svg_path, encoding="utf-8") as f:
        svg = f.read()
    m = re.search(r'viewBox\s*=\s*"([^"]+)"', svg)
    if not m:
        raise ValueError(f"{svg_path}: sem viewBox — adicionar antes de checar")
    partes = [p for p in re.split(r"[\s,]+", m.group(1).strip()) if p]
    if len(partes) != 4:
        raise ValueError(f"{svg_path}: viewBox ilegível: {m.group(1)!r}")
    escala = escala_pt_por_px(float(partes[2]), largura_final_cm)
    declarados = re.findall(r'font-size[:=]"?\s*([\d.]+)\s*(px|pt|em|rem)?', svg)
    # shorthand CSS: font: [peso/estilo] TAMANHOpx família
    declarados += re.findall(r'font\s*:\s*[^;"}>]*?([\d.]+)\s*(px|pt)\b', svg)
    tamanhos_px = [_fs_para_px(float(v), u) for v, u in declarados]
    if not tamanhos_px and re.search(r"<(?:text|tspan)\b", svg):
        tamanhos_px = [16.0]  # nenhum font-size declarado: vale o default do renderizador
    violacoes = []
    for px in tamanhos_px:
        pt = px * escala
        if pt < min_pt - 0.05:
            violacoes.append((round(px, 1), round(pt, 1)))
    return sorted(set(violacoes))


def largura_recomendada_cm(svg_path: str, alvo_pt: float = 10.0,
                           maximo_cm: float = 15.0) -> float:
    """Largura de inserção que faz o MENOR font-size do SVG imprimir ~alvo_pt.

    Resolve o efeito 'diagrama gigante': um fluxo Graphviz de 3 nós tem viewBox
    pequeno — inserido a 15cm a fonte sai enorme. Usar esta largura no
    inserir_emf_word_com em vez de 15cm fixo. Nunca excede maximo_cm."""
    with open(svg_path, encoding="utf-8") as f:
        svg = f.read()
    m = re.search(r'viewBox\s*=\s*"([^"]+)"', svg)
    if not m:
        raise ValueError(f"{svg_path}: sem viewBox")
    w_px = float([p for p in re.split(r"[\s,]+", m.group(1).strip()) if p][2])
    declarados = re.findall(r'font-size[:=]"?\s*([\d.]+)\s*(px|pt|em|rem)?', svg)
    declarados += re.findall(r'font\s*:\s*[^;"}>]*?([\d.]+)\s*(px|pt)\b', svg)
    menor_px = min((_fs_para_px(float(v), u) for v, u in declarados), default=16.0)
    cm = (alvo_pt / menor_px) * w_px / PT_POR_CM
    return round(min(cm, maximo_cm), 1)


def aplicar_estilo_matplotlib():
    """rcParams para gráficos quantitativos consistentes com a identidade Medina."""
    import matplotlib
    matplotlib.rcParams.update({
        "font.family": FONTE_DIAGRAMA,
        "font.size": 11,
        "axes.titlesize": 12, "axes.labelsize": 11,
        "xtick.labelsize": 10, "ytick.labelsize": 10,
        "legend.fontsize": 10,
        "axes.edgecolor": CORES["grafite"], "axes.labelcolor": CORES["grafite"],
        "xtick.color": CORES["grafite"], "ytick.color": CORES["grafite"],
        "axes.prop_cycle": matplotlib.cycler(color=[
            CORES["petroleo"], CORES["terracota_escura"], CORES["grafite"],
            CORES["terracota"], CORES["petroleo_escuro"]]),
        "figure.dpi": 150, "savefig.dpi": 300, "savefig.bbox": "tight",
        # mantém <text> real no SVG (auditável pelo gate e editável); 'path' esconderia as fontes
        "svg.fonttype": "none",
        "axes.grid": True, "grid.color": CORES["linha_cinza"], "grid.linewidth": 0.4,
        "axes.spines.top": False, "axes.spines.right": False,
    })


ESTILO_GRAPHVIZ = (
    'graph [fontname="Segoe UI", fontsize=12, bgcolor="transparent"]; '
    'node [fontname="Segoe UI", fontsize=12, shape=box, style="rounded,filled", '
    'fillcolor="#EFF4F3", color="#395C60", fontcolor="#2A4548", penwidth=1.2]; '
    'edge [fontname="Segoe UI", fontsize=11, color="#9C5B38", fontcolor="#49494D", penwidth=1.1];'
)

TEMA_MERMAID = {
    "theme": "base",
    "themeVariables": {
        "fontFamily": "Segoe UI", "fontSize": "16px",
        "primaryColor": "#EFF4F3", "primaryBorderColor": "#395C60",
        "primaryTextColor": "#2A4548", "lineColor": "#9C5B38",
        "secondaryColor": "#FBF2EC", "tertiaryColor": "#FFFFFF",
    },
}

if __name__ == "__main__":
    # exemplo de auditoria rápida
    print("1 px em viewBox 600 @ 15cm =", round(escala_pt_por_px(600, 15), 2), "pt")
    print("font-size px mínimo p/ 8pt:", round(fonte_px_minima(600, 15), 1))
    print("font-size px mínimo p/ 9pt:", round(fonte_px_minima(600, 15, 9), 1))
