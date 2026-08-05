# -*- coding: utf-8 -*-
"""Helpers SVG para os diagramas das edições visual law Medina Osório.

Convenção validada (08/07/2026): viewBox em unidades-ponto da largura final
(viewBox_w = largura_cm * 28.3465) => font-size N == N pt impressos.
Mínimos do gate: 8pt texto, 8,5-9pt rótulos, 10,5pt títulos internos.
ARMADILHA: <text> não quebra linha e o Inkscape CORTA o que sair do viewBox —
quebrar linhas manualmente e manter padding lateral nas pontas.
"""
import math, os, textwrap
from estilo_medina import CORES, FONTE_DIAGRAMA, checar_fontes_svg

PET = CORES["petroleo"]; PETE = CORES["petroleo_escuro"]
TER = CORES["terracota"]; TERE = CORES["terracota_escura"]
GRA = CORES["grafite"]; PV = CORES["painel_verde"]; PT_ = CORES["painel_terra"]
ALE = CORES["alerta"]; RUL = CORES["linha_cinza"]
F = FONTE_DIAGRAMA
CMPT = 28.3465


def wrap(txt, chars):
    return textwrap.wrap(txt, chars)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def tblock(x, y, lines, size, fill, weight="normal", anchor="middle",
           style="normal", lh=None):
    """Bloco de texto multilinha. Retorna (svg, y_final)."""
    lh = lh or size * 1.22
    out = []
    for i, ln in enumerate(lines):
        out.append(
            f'<text x="{x:.1f}" y="{y + i * lh:.1f}" font-family="{F}" '
            f'font-size="{size}" font-weight="{weight}" font-style="{style}" '
            f'fill="{fill}" text-anchor="{anchor}">{esc(ln)}</text>')
    return "\n".join(out), y + len(lines) * lh


def seta(x1, y1, x2, y2, cor, lw=1.1, curva=None):
    """Linha (ou curva quadrática via ponto de controle) com ponta triangular."""
    ang = math.atan2(y2 - y1, x2 - x1)
    L = 6.0
    if curva:
        cx, cy = curva
        d = f'M {x1:.1f} {y1:.1f} Q {cx:.1f} {cy:.1f} {x2:.1f} {y2:.1f}'
        ang = math.atan2(y2 - cy, x2 - cx)
        path = f'<path d="{d}" fill="none" stroke="{cor}" stroke-width="{lw}"/>'
    else:
        path = (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                f'stroke="{cor}" stroke-width="{lw}"/>')
    p1 = (x2 - L * math.cos(ang - 0.42), y2 - L * math.sin(ang - 0.42))
    p2 = (x2 - L * math.cos(ang + 0.42), y2 - L * math.sin(ang + 0.42))
    tri = (f'<polygon points="{x2:.1f},{y2:.1f} {p1[0]:.1f},{p1[1]:.1f} '
           f'{p2[0]:.1f},{p2[1]:.1f}" fill="{cor}"/>')
    return path + tri


def caixa(x, y, w, h, fill, stroke=None, sw=1.0, rx=3):
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ' stroke="none"'
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}"{s}/>'


import re as _re


def _gate_v2_enabled():
    if os.environ.get("FORJA_VISUAL_GATE_V2") == "1":
        return True
    config = os.path.join(os.path.dirname(__file__), "..", "_FORJA_HARNESS", "FORJA_N3_CONFIG.json")
    try:
        import json
        with open(config, "r", encoding="utf-8-sig") as handle:
            return bool((json.load(handle).get("features") or {}).get("visualGateV2"))
    except (OSError, ValueError, TypeError):
        return False

def _overflow_texto(corpo, w, h, folga=2.0):
    """Estima a caixa de cada <text> e devolve os que saem do viewBox.
    O Inkscape CORTA no viewBox — texto de ponta cortado foi erro recorrente
    (CASO-04 fig1 08/07; Jalusa fig2 09/07). Heurística: Segoe UI ~0,52em/char
    (0,58 bold)."""
    probs = []
    for m in _re.finditer(
            r'<text x="([\d.-]+)" y="([\d.-]+)" [^>]*font-size="([\d.]+)" '
            r'font-weight="(\w+)"[^>]*text-anchor="(\w+)">([^<]*)</text>', corpo):
        x, y, size, peso, anchor, txt = (float(m.group(1)), float(m.group(2)),
                                         float(m.group(3)), m.group(4),
                                         m.group(5), m.group(6))
        fator = 0.58 if peso == "bold" else 0.52
        larg = len(txt) * size * fator
        if anchor == "middle":
            x0, x1 = x - larg / 2, x + larg / 2
        elif anchor == "end":
            x0, x1 = x - larg, x
        else:
            x0, x1 = x, x + larg
        if x0 < -folga or x1 > w + folga or y - size > h or y < 0:
            probs.append((round(x0, 1), round(x1, 1), txt[:40]))
    return probs


def salvar(nome, w, h, corpo, largura_cm):
    """Grava o SVG e roda os gates: legibilidade + overflow do viewBox."""
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
           f'width="{w}pt" height="{h}pt">\n{corpo}\n</svg>')
    with open(nome, "w", encoding="utf-8") as f:
        f.write(svg)
    viol = checar_fontes_svg(nome, largura_cm)
    if viol:
        raise ValueError(f"{nome} REPROVADO no gate de legibilidade @ {largura_cm}cm: {viol}")
    over = _overflow_texto(corpo, w, h)
    if over:
        raise ValueError(f"{nome} REPROVADO: texto fora do viewBox (o EMF corta!): {over}")
    from medina_svg_colisao import checar as _checar_desenho
    _checar_desenho(nome)
    if _gate_v2_enabled():
        from medina_visual_lint import lint_svg
        report = lint_svg(nome)
        if not report["approved"]:
            resumo = [item["code"] for item in report["findings"][:8]]
            raise ValueError(f"{nome} REPROVADO no visual gate V2: {resumo}")
    print(f"{nome}: APROVADO @ {largura_cm}cm")
    return nome


def _chars(largura_pt, size, bold=False):
    """Quantos caracteres cabem numa largura, pelo mesmo fator do gate de
    overflow (0,52em normal / 0,58em bold). Manter os dois em sincronia: se o
    wrap usar fator menor que o gate, o texto passa no wrap e reprova no gate."""
    return max(6, int(largura_pt / (size * (0.58 if bold else 0.52))))


def cronologia(nome, eventos, largura_cm=13.1, titulo=None):
    """Linha do tempo vertical dos atos. eventos: [(data, descrição), ...].

    Vertical por decisão de legibilidade: horizontal força texto minúsculo ou
    corta descrição quando há mais de 4 marcos — os dois modos de falha que o
    gate de overflow pega. A altura é calculada pelo conteúdo, nunca fixa.
    """
    W = largura_cm * CMPT
    PAD = 6.0
    X_DATA, W_DATA = PAD, 74.0
    X_LINHA = X_DATA + W_DATA + 12
    X_TXT = X_LINHA + 13
    W_TXT = W - X_TXT - PAD
    ch_data = _chars(W_DATA, 8.5, bold=True)
    ch_txt = _chars(W_TXT, 8.5)

    corpo, y = [], 16.0
    if titulo:
        t, y = tblock(PAD, y, wrap(titulo, _chars(W - 2 * PAD, 10.5, True)),
                      10.5, PETE, "bold", "start")
        corpo.append(t)
        y += 10
    pontos = []
    for data, desc in eventos:
        linhas_data = wrap(str(data), ch_data)
        linhas_desc = wrap(str(desc), ch_txt)
        pontos.append(y - 3.0)
        t, _ = tblock(X_DATA, y, linhas_data, 8.5, TERE, "bold", "start", lh=10)
        corpo.append(t)
        t, _ = tblock(X_TXT, y, linhas_desc, 8.5, GRA, "normal", "start", lh=10.5)
        corpo.append(t)
        y += max(len(linhas_data), len(linhas_desc)) * 10.5 + 9
    if pontos:
        corpo.insert(0, f'<line x1="{X_LINHA:.1f}" y1="{pontos[0]:.1f}" '
                        f'x2="{X_LINHA:.1f}" y2="{pontos[-1]:.1f}" '
                        f'stroke="{RUL}" stroke-width="1.6"/>')
        for py in pontos:
            corpo.append(f'<circle cx="{X_LINHA:.1f}" cy="{py:.1f}" r="3.4" '
                         f'fill="{PET}"/>')
    return salvar(nome, round(W, 1), round(y + PAD, 1), "\n".join(corpo), largura_cm)


def encadeamento(nome, etapas, largura_cm=13.1, rotulo_final="CONCLUSÃO"):
    """Fluxo vertical premissa -> premissa -> conclusão. etapas: [texto, ...];
    o último item é destacado como conclusão (fundo petróleo, texto branco)."""
    W = largura_cm * CMPT
    PAD = 6.0
    BW = W - 2 * PAD
    ch = _chars(BW - 22, 8.5)
    corpo, y = [], 8.0
    for k, texto in enumerate(etapas):
        final = (k == len(etapas) - 1)
        linhas = wrap(str(texto), ch)
        alt = len(linhas) * 11.0 + (24 if final else 14)
        corpo.append(caixa(PAD, y, BW, alt, PET if final else PV,
                           None if final else PET, 1.0))
        ty = y + 12
        t, _ = tblock(W / 2, ty, linhas, 8.5, "#FFFFFF" if final else GRA,
                      "bold" if final else "normal", "middle", lh=11)
        corpo.append(t)
        if final:
            t, _ = tblock(W / 2, y + alt - 8, [rotulo_final], 8.0, "#FFFFFF", "bold",
                          "middle")
            corpo.append(t)
        y += alt
        if not final:
            corpo.append(seta(W / 2, y + 2, W / 2, y + 13, TERE, 1.2))
            y += 16
    return salvar(nome, round(W, 1), round(y + PAD, 1), "\n".join(corpo), largura_cm)


def matriz(nome, cabecalho, linhas, largura_cm=13.1):
    """Quadro comparativo vetorial. Usar quando a comparação precisa virar
    FIGURA; comparação que já é tabela no markdown continua indo para o
    quadro zebrado do Word, que é editável e melhor para leitura longa."""
    W = largura_cm * CMPT
    PAD = 6.0
    n = max(1, len(cabecalho))
    CW = (W - 2 * PAD) / n
    ch = _chars(CW - 12, 8.0)
    ch_cab = _chars(CW - 12, 8.5, bold=True)

    cab_linhas = [wrap(str(c), ch_cab) for c in cabecalho]
    alt_cab = max(len(b) for b in cab_linhas) * 10.5 + 10
    corpo, y = [], PAD
    for j, blocos in enumerate(cab_linhas):
        corpo.append(caixa(PAD + j * CW, y, CW, alt_cab, PET, None, rx=0))
        t, _ = tblock(PAD + j * CW + CW / 2, y + 12, blocos, 8.5, "#FFFFFF",
                      "bold", "middle", lh=10.5)
        corpo.append(t)
    y += alt_cab
    for i, linha in enumerate(linhas):
        celulas = [wrap(str(c), ch) for c in list(linha)[:n]]
        celulas += [[""]] * (n - len(celulas))
        alt = max(len(b) for b in celulas) * 10.0 + 10
        for j, blocos in enumerate(celulas):
            corpo.append(caixa(PAD + j * CW, y, CW, alt,
                               PV if i % 2 == 0 else "#FFFFFF", RUL, 0.6, rx=0))
            t, _ = tblock(PAD + j * CW + 6, y + 12, blocos, 8.0, GRA,
                          "normal", "start", lh=10)
            corpo.append(t)
        y += alt
    return salvar(nome, round(W, 1), round(y + PAD, 1), "\n".join(corpo), largura_cm)


def cards_ancora(nome, dados, largura_cm=13.1):
    """Faixa de âncoras da capa. dados: [(numero, cor_hex, fundo_hex, descricao), ...]
    Altura calculada pelo card mais alto — nunca corta texto (lição EDcl 09/07)."""
    W = largura_cm * CMPT
    n = len(dados)
    GAP = 7.8
    CW = (W - GAP * (n - 1)) / n
    # A descrição do card é composta em CAIXA ALTA, e maiúscula é mais larga que
    # a média de 0,52em usada pelo gate de overflow — que só mede a borda do
    # viewBox e não a borda do card. Resultado: "CONTEXTO PROCESSUAL" passava no
    # gate e saía cortado na borda do card (CASO-04 V7, 30/07/2026). 0,60em
    # com a largura útil real (CW menos os 7pt de recuo de cada lado).
    chars = max(12, int((CW - 14) / (8 * 0.60)))
    blocos = [wrap(desc, chars) for _, _, _, desc in dados]
    altura = 36 + max(len(b) for b in blocos) * 10 + 4
    corpo = []
    for i, ((num, cor, fundo, _), subs) in enumerate(zip(dados, blocos)):
        x = i * (CW + GAP)
        corpo.append(caixa(x, 2, CW, altura - 2, fundo, rx=0))
        corpo.append(f'<line x1="{x}" y1="2.1" x2="{x + CW}" y2="2.1" '
                     f'stroke="{cor}" stroke-width="2.4"/>')
        # auto-ajuste: título bold em caixa alta ocupa ~0,66×fonte por
        # caractere; título longo em 15pt fixo estoura a borda do card
        # (flagrado no QA da CASO-04 AgInt em 10/07/2026: "4 FUNDAMENTOS"
        # com o S cortado). Piso de 9pt respeita o gate de legibilidade.
        fonte_num = min(15.0, max(9.0, (CW - 14) / (0.66 * max(1, len(num)))))
        t, _ = tblock(x + 7, 22, [num], round(fonte_num, 1), cor, "bold", "start")
        corpo.append(t)
        t, _ = tblock(x + 7, 36, subs, 8, GRA, "normal", "start", lh=10)
        corpo.append(t)
    return salvar(nome, round(W, 1), altura, "\n".join(corpo), largura_cm)
