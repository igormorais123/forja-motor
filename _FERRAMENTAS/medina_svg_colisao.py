# -*- coding: utf-8 -*-
"""Gate de corretude de desenho do SVG — colisão, oclusão e cor inválida.

POR QUE EXISTE. Em 03/08/2026 o Igor apontou diagrama errado na peça que ele
próprio aprovara em 09/07 e que o gate F8-S usa como teste-âncora. O defeito
estava no XML, à vista: em `fig2_obices_convergentes.svg` o retângulo do
fecho ("NÃO CONHECIMENTO") é desenhado DEPOIS das caixas inferiores e cobre o
texto de duas delas; e o texto do fecho traz `fill="ffffff"` sem `#`, que não é
cor SVG válida — o renderizador cai no preto e o rótulo perde contraste sobre o
fundo petróleo.

Nenhum gate da casa via isso. O de legibilidade mede tamanho de fonte; o de
overflow mede saída do viewBox; o F8-S conta PRESENÇA de elementos no DOCX.
Todos aprovam um diagrama internamente quebrado — a memória da fábrica já dizia
que "só o zoom pega". Este módulo é o que pega sem o zoom.

ONDE MORA O RISCO. Os geradores programáticos (`cronologia`, `encadeamento`,
`matriz`) empilham verticalmente com altura calculada pelo conteúdo e não têm
como produzir esta falha. Ela vive no SVG escrito à mão com coordenadas
absolutas, que era o modelo dos mapas manuais de julho. Por isso o gate roda na
conversão para EMF (`word_visual_pipeline.svg_para_emf`), por onde TODO SVG
passa antes de entrar no Word, e não só em `medina_svg_kit.salvar`.

LIMITE DECLARADO. A largura do texto é estimada por fator médio de caractere,
não medida na fonte real. Serve para achar sobreposição grosseira — que é a
classe de defeito observada —, não para validar espaçamento fino. Um achado
deste gate é sempre verdadeiro no XML; a estimativa afeta a MARGEM, não a
existência da sobreposição, quando a fração coberta é alta.
"""
import re
import xml.etree.ElementTree as ET

SVG_NS = "http://www.w3.org/2000/svg"

# Mesmos fatores do gate de overflow (medina_svg_kit._overflow_texto), um degrau
# mais conservadores: aqui uma superestimativa de largura vira acusação falsa de
# colisão, enquanto lá ela só apertava a margem do viewBox.
_FATOR = {"bold": 0.56, "normal": 0.50}
_ASC, _DESC = 0.72, 0.20

# Fração da área do texto que precisa estar coberta para virar achado. Abaixo
# disso a estimativa de largura não sustenta a acusação.
_LIMIAR_OCLUSAO = 0.12
_LIMIAR_TEXTO_TEXTO = 0.20

_CORES_CSS = {
    "none", "transparent", "currentcolor", "black", "white", "gray", "grey",
    "red", "green", "blue", "yellow", "orange", "purple", "brown", "pink",
    "silver", "navy", "teal", "olive", "maroon", "lime", "aqua", "fuchsia",
}
_HEX = re.compile(r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$")
_FUNC = re.compile(r"^(?:rgb|rgba|hsl|hsla|url|var)\(", re.I)


def _cor_valida(valor):
    # `!important` é CSS legítimo dentro de style= e não faz parte da cor. Sem
    # esta normalização o gate acusava 373 falsos positivos nos diagramas do
    # atlas, todos com `style="fill:#e8f1ef !important"`.
    v = re.sub(r"\s*!\s*important\s*$", "", (valor or "").strip(), flags=re.I)
    if not v:
        return True
    if v.lower() in _CORES_CSS or _HEX.match(v) or _FUNC.match(v):
        return True
    return False


def _luminancia(hexcor):
    """Luminância relativa WCAG. Devolve None se a cor não for hex sólido."""
    v = (hexcor or "").strip()
    if not _HEX.match(v):
        return None
    v = v.lstrip("#")
    if len(v) in (3, 4):
        v = "".join(c * 2 for c in v[:3])
    v = v[:6]
    canais = []
    for i in (0, 2, 4):
        c = int(v[i:i + 2], 16) / 255.0
        canais.append(c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * canais[0] + 0.7152 * canais[1] + 0.0722 * canais[2]


def _contraste(cor_a, cor_b):
    la, lb = _luminancia(cor_a), _luminancia(cor_b)
    if la is None or lb is None:
        return None
    claro, escuro = max(la, lb), min(la, lb)
    return (claro + 0.05) / (escuro + 0.05)


def _transform(valor):
    """Composição de translate/scale/matrix num par (offset, escala).

    Rotação e skew não são suportados: o desenho da casa não os usa, e fingir
    que uma caixa girada é um retângulo alinhado produziria achado falso. Quando
    aparecem, o elemento é marcado como não analisável (ver `_percorrer`)."""
    dx = dy = 0.0
    sx = sy = 1.0
    suportado = True
    for nome, args in re.findall(r"(\w+)\s*\(([^)]*)\)", valor or ""):
        n = [float(x) for x in re.split(r"[\s,]+", args.strip()) if x]
        if nome == "translate":
            dx += n[0] * sx
            dy += (n[1] if len(n) > 1 else 0.0) * sy
        elif nome == "scale":
            sx *= n[0]
            sy *= n[1] if len(n) > 1 else n[0]
        elif nome == "matrix" and len(n) == 6:
            if abs(n[1]) > 1e-9 or abs(n[2]) > 1e-9:
                suportado = False
            else:
                sx *= n[0]
                sy *= n[3]
                dx += n[4]
                dy += n[5]
        else:
            suportado = False
    return dx, dy, sx, sy, suportado


def _num(el, attr, padrao=0.0):
    try:
        return float(re.sub(r"[a-z%]+$", "", (el.get(attr) or "").strip()))
    except ValueError:
        return padrao


def _tag(el):
    return el.tag.split("}")[-1] if "}" in el.tag else el.tag


def _herda(el, attr, herdado):
    return el.get(attr) or herdado.get(attr)


def _opaco(el, herdado):
    """A forma tapa o que está debaixo?"""
    fill = (_herda(el, "fill", herdado) or "").strip().lower()
    if fill in ("", "none", "transparent"):
        return False
    for chave in ("opacity", "fill-opacity"):
        try:
            if float(_herda(el, chave, herdado) or 1.0) < 0.85:
                return False
        except ValueError:
            pass
    return True


def _percorrer(no, herdado, dx, dy, sx, sy, saida, ok):
    for el in no:
        tag = _tag(el)
        t_dx, t_dy, t_sx, t_sy, sup = _transform(el.get("transform"))
        if not sup:
            ok.append(_tag(el))
        cdx, cdy = dx + t_dx * sx, dy + t_dy * sy
        csx, csy = sx * t_sx, sy * t_sy
        prop = dict(herdado)
        for k in ("fill", "stroke", "font-size", "font-weight", "text-anchor",
                  "opacity", "fill-opacity", "font-family"):
            if el.get(k):
                prop[k] = el.get(k)
        # `style="fill:#fff;font-size:9px"` é tão comum quanto o atributo solto.
        for k, v in re.findall(r"([a-z-]+)\s*:\s*([^;]+)", el.get("style") or ""):
            prop[k.strip()] = v.strip()

        if tag in ("g", "svg", "a"):
            _percorrer(el, prop, cdx, cdy, csx, csy, saida, ok)
            continue

        item = {"tag": tag, "el": el, "prop": prop}
        if tag == "text":
            filhos = [c for c in el if _tag(c) == "tspan"]
            partes = []
            if filhos:
                for c in filhos:
                    p = dict(prop)
                    for k, v in c.attrib.items():
                        if k in ("fill", "font-size", "font-weight", "text-anchor"):
                            p[k] = v
                    partes.append((c, p, "".join(c.itertext())))
            else:
                partes.append((el, prop, "".join(el.itertext())))
            # Cursor de fluxo: um <tspan> SEM x próprio começa onde o anterior
            # terminou, não no x do <text> pai. Tratá-los todos como iniciando
            # no mesmo x fazia o gate acusar 96% de sobreposição entre o rótulo
            # em negrito e a frase que vem depois dele — que na página estão
            # lado a lado. Foi o único falso positivo da medição no acervo.
            cursor = None
            for elem, p, txt in partes:
                txt = (txt or "").strip()
                if not txt:
                    continue
                try:
                    size = float(re.sub(r"[a-z%]+$", "",
                                        str(p.get("font-size", "0")).strip()))
                except ValueError:
                    size = 0.0
                if size <= 0:
                    continue
                y = _num(elem, "y", _num(el, "y")) * csy + cdy
                size_e = size * csy
                largura = len(txt) * size_e * _FATOR.get(
                    str(p.get("font-weight", "normal")).lower(), _FATOR["normal"])
                anchor = str(p.get("text-anchor", "start")).lower()
                proprio = elem.get("x") is not None
                if not proprio and cursor is not None:
                    x0 = cursor
                else:
                    x = _num(elem, "x", _num(el, "x")) * csx + cdx
                    if anchor == "middle":
                        x0 = x - largura / 2
                    elif anchor == "end":
                        x0 = x - largura
                    else:
                        x0 = x
                cursor = x0 + largura
                saida.append({**item, "tipo": "texto", "texto": txt,
                              "fill": p.get("fill"),
                              "caixa": (x0, y - _ASC * size_e,
                                        x0 + largura, y + _DESC * size_e)})
        elif tag == "rect":
            x = _num(el, "x") * csx + cdx
            y = _num(el, "y") * csy + cdy
            saida.append({**item, "tipo": "forma",
                          "caixa": (x, y, x + _num(el, "width") * csx,
                                    y + _num(el, "height") * csy)})
        elif tag in ("circle", "ellipse"):
            cx = _num(el, "cx") * csx + cdx
            cy = _num(el, "cy") * csy + cdy
            rx = (_num(el, "r") or _num(el, "rx")) * csx
            ry = (_num(el, "r") or _num(el, "ry")) * csy
            saida.append({**item, "tipo": "forma",
                          "caixa": (cx - rx, cy - ry, cx + rx, cy + ry)})
        elif tag == "polygon":
            pts = [float(v) for v in re.split(r"[\s,]+", (el.get("points") or "").strip()) if v]
            if len(pts) >= 4:
                xs = [p * csx + cdx for p in pts[0::2]]
                ys = [p * csy + cdy for p in pts[1::2]]
                saida.append({**item, "tipo": "forma",
                              "caixa": (min(xs), min(ys), max(xs), max(ys))})
        elif tag in ("line", "path", "polyline"):
            saida.append({**item, "tipo": "traco",
                          "caixa": _envelope_traco(el, cdx, cdy, csx, csy),
                          "segmentos": _segmentos(el, cdx, cdy, csx, csy)})
        _percorrer(el, prop, cdx, cdy, csx, csy, saida, ok)


def _envelope_traco(el, dx, dy, sx, sy):
    if _tag(el) == "line":
        xs = [_num(el, "x1") * sx + dx, _num(el, "x2") * sx + dx]
        ys = [_num(el, "y1") * sy + dy, _num(el, "y2") * sy + dy]
    else:
        nums = [float(v) for v in re.findall(r"-?\d+\.?\d*",
                                             el.get("points") or el.get("d") or "")]
        if len(nums) < 4:
            return None
        xs = [n * sx + dx for n in nums[0::2]]
        ys = [n * sy + dy for n in nums[1::2]]
    return (min(xs), min(ys), max(xs), max(ys))


def _segmentos(el, dx, dy, sx, sy):
    """Segmentos de reta do traço, já transformados.

    Necessário porque o envelope de uma diagonal é um retângulo enorme que toca
    caixas que a linha real não encosta: na primeira medição do gate uma seta
    diagonal acusava 13 textos, dos quais nenhum era tocado. O envelope serve de
    filtro barato; a decisão sai daqui."""
    if _tag(el) == "line":
        return [((_num(el, "x1") * sx + dx, _num(el, "y1") * sy + dy),
                 (_num(el, "x2") * sx + dx, _num(el, "y2") * sy + dy))]
    nums = [float(v) for v in re.findall(r"-?\d+\.?\d*",
                                         el.get("points") or el.get("d") or "")]
    pts = [(nums[i] * sx + dx, nums[i + 1] * sy + dy)
           for i in range(0, len(nums) - 1, 2)]
    return [(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]


def _corta_caixa(p0, p1, caixa):
    """Liang-Barsky: o segmento toca o retângulo?"""
    x0, y0 = p0
    x1, y1 = p1
    dx, dy = x1 - x0, y1 - y0
    t0, t1 = 0.0, 1.0
    for p, q in ((-dx, x0 - caixa[0]), (dx, caixa[2] - x0),
                 (-dy, y0 - caixa[1]), (dy, caixa[3] - y0)):
        if abs(p) < 1e-12:
            if q < 0:
                return False
            continue
        r = q / p
        if p < 0:
            if r > t1:
                return False
            t0 = max(t0, r)
        else:
            if r < t0:
                return False
            t1 = min(t1, r)
    return t0 <= t1


def _intersec(a, b):
    if not a or not b:
        return 0.0
    x = max(0.0, min(a[2], b[2]) - max(a[0], b[0]))
    y = max(0.0, min(a[3], b[3]) - max(a[1], b[1]))
    return x * y


def _area(c):
    return max(0.0, c[2] - c[0]) * max(0.0, c[3] - c[1])


def analisar(svg_path=None, texto=None):
    """Devolve o laudo de desenho. Não levanta: quem decide bloquear é o gate."""
    if texto is None:
        with open(svg_path, encoding="utf-8") as f:
            texto = f.read()
    raiz = ET.fromstring(texto)
    itens, nao_analisados = [], []
    _percorrer(raiz, {}, 0.0, 0.0, 1.0, 1.0, itens, nao_analisados)

    achados = []

    def add(codigo, gravidade, msg, alvo):
        achados.append({"codigo": codigo, "gravidade": gravidade,
                        "mensagem": msg, "elemento": alvo[:60]})

    for i, it in enumerate(itens):
        # SVGC-04 — cor sintaticamente inválida. `fill="ffffff"` (sem #) foi o
        # caso real: o renderizador ignora e pinta preto, e o rótulo branco
        # planejado some no fundo escuro.
        for attr in ("fill", "stroke"):
            # Valor efetivo: atributo do próprio elemento, senão o que veio de
            # style=/herança. Ler só o atributo deixaria passar cor inválida
            # escrita no style.
            v = it["el"].get(attr) or it["prop"].get(attr)
            if v and not _cor_valida(v):
                add("SVGC-04", "bloqueia",
                    f'{attr}="{v}" não é cor SVG válida (falta "#"?)',
                    it.get("texto") or it["tag"])

        if it["tipo"] != "texto" or not it["caixa"]:
            continue
        area_txt = _area(it["caixa"])
        if area_txt <= 0:
            continue

        for j in range(i + 1, len(itens)):
            outro = itens[j]
            if not outro["caixa"]:
                continue
            inter = _intersec(it["caixa"], outro["caixa"])
            if inter <= 0:
                continue
            frac = inter / area_txt

            # SVGC-01 — texto tapado por forma pintada depois dele.
            if outro["tipo"] == "forma" and _opaco(outro["el"], outro["prop"]):
                if frac >= _LIMIAR_OCLUSAO:
                    add("SVGC-01", "bloqueia",
                        f'texto coberto por <{outro["tag"]}> desenhado depois '
                        f'({frac:.0%} da caixa do texto)', it["texto"])
                continue

            # SVGC-02 — dois textos por cima um do outro.
            if outro["tipo"] == "texto":
                menor = min(area_txt, _area(outro["caixa"])) or area_txt
                if inter / menor >= _LIMIAR_TEXTO_TEXTO:
                    add("SVGC-02", "bloqueia",
                        f'sobreposto a "{outro["texto"][:30]}" '
                        f'({inter / menor:.0%})', it["texto"])
                continue

            # SVGC-03 — traço (seta, conector) passando por cima do texto.
            # Aviso, não bloqueio: uma linha fina cruzando a borda de um rótulo
            # incomoda, mas não apaga a informação como um retângulo opaco.
            if outro["tipo"] == "traco" and any(
                    _corta_caixa(a, b, it["caixa"])
                    for a, b in (outro.get("segmentos") or [])):
                add("SVGC-03", "aviso",
                    f'traço <{outro["tag"]}> posterior cruza o texto',
                    it["texto"])

        # SVGC-05 — contraste do texto contra a última forma opaca pintada
        # ANTES dele que o contenha (o fundo efetivo).
        fundo = None
        for ant in itens[:i]:
            if ant["tipo"] == "forma" and ant["caixa"] and _opaco(ant["el"], ant["prop"]):
                if _intersec(it["caixa"], ant["caixa"]) / area_txt > 0.8:
                    fundo = ant["prop"].get("fill") or ant["el"].get("fill")
        if fundo:
            # Limiar 2.0:1, não os 3.0:1 da WCAG. O rótulo terracota sobre
            # painel terra da identidade da casa dá 2.3:1 e está aprovado desde
            # 09/07 — um gate calibrado na WCAG reprovaria a paleta do
            # escritório, que é o erro que já cometi na detecção de timbre por
            # cor. Abaixo de 2.0 o texto some de fato (foi o caso do preto
            # acidental sobre o fundo petróleo).
            r = _contraste(it.get("fill"), fundo)
            if r is not None and r < 2.0:
                add("SVGC-05", "aviso",
                    f'contraste {r:.1f}:1 do texto sobre {fundo} — ilegível',
                    it["texto"])

    bloqueios = [a for a in achados if a["gravidade"] == "bloqueia"]
    return {
        # `str` e não o objeto recebido: quem chama passa `Path`, e o laudo é
        # gravado em JSON pela rota canônica de produção. Devolver `Path` fazia
        # `forja_visual_build` estourar `TypeError` ao escrever o
        # F8_QA_ESTRUTURAL.json — ou seja, toda peça COM figura quebrava, e só a
        # peça sem figura passava. Descoberto em 04/08/2026 compondo o Cafelana.
        "svg": str(svg_path),
        "elementos": len(itens),
        "textos": sum(1 for i in itens if i["tipo"] == "texto"),
        "naoAnalisados": sorted(set(nao_analisados)),
        "achados": achados,
        "aprovado": not bloqueios,
    }


def checar(svg_path, bloquear=True):
    """Roda o gate. Levanta ValueError nos achados bloqueantes."""
    laudo = analisar(svg_path)
    if bloquear and not laudo["aprovado"]:
        linhas = [f'  [{a["codigo"]}] {a["elemento"]}: {a["mensagem"]}'
                  for a in laudo["achados"] if a["gravidade"] == "bloqueia"]
        raise ValueError(f"{svg_path} REPROVADO no gate de desenho:\n" + "\n".join(linhas))
    return laudo


if __name__ == "__main__":
    import json
    import sys
    for caminho in sys.argv[1:]:
        try:
            print(json.dumps(analisar(caminho), ensure_ascii=False, indent=2))
        except ET.ParseError as e:
            print(json.dumps({"svg": caminho, "erro": f"XML ilegível: {e}"},
                             ensure_ascii=False))
