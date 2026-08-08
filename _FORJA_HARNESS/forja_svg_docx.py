# -*- coding: utf-8 -*-
"""Embute SVG diretamente no DOCX, sem conversão, renderização ou Word COM.

A FORJA precisa preservar a natureza vetorial dos diagramas, mas a antiga
ponte SVG -> EMF -> Word dependia de conversores e da materialização em PDF/PNG
para validar a saída. Esta rota usa o suporte nativo do Office a SVG: o arquivo
SVG é um ``image/svg+xml`` dentro do pacote OOXML e o parágrafo marcador recebe
um ``wp:inline`` com a relação de imagem. O XML é determinístico e pode ser
auditado sem abrir o documento em um renderizador.

O módulo não inventa uma figura nem altera o texto. Antes de embutir, executa os
lintes geométrico e estrutural já calibrados; um SVG inválido ou com colisão
bloqueante nunca é colocado no DOCX.
"""

from __future__ import annotations

import hashlib
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from lxml import etree

from docx import Document
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.opc.part import Part
from docx.oxml import OxmlElement
from docx.oxml.ns import qn


SVG_CONTENT_TYPE = "image/svg+xml"
PNG_CONTENT_TYPE = "image/png"
PIC_URI = "http://schemas.openxmlformats.org/drawingml/2006/picture"
# Identificador fixo da extensão de SVG do Office. Não é escolha nossa: é o
# valor que o Word procura para saber que aquele `blip` tem versão vetorial.
SVG_EXT_URI = "{96DAC541-7B7A-43D3-8B79-37D633B846F1}"
SVG_EXT_NS = "http://schemas.microsoft.com/office/drawing/2016/SVG/main"
EMU_PER_CM = 360000
FORJA = Path(__file__).resolve().parent
sys.path.insert(0, str(FORJA.parent / "_FERRAMENTAS"))


def _number(value: object, default: float = 0.0) -> float:
    match = re.search(r"-?\d+(?:\.\d+)?", str(value or ""))
    return float(match.group()) if match else default


def _svg_ratio(path: Path) -> float:
    """Retorna largura/altura do SVG sem depender de um visualizador."""
    root = ET.parse(path).getroot()
    view_box = [float(value) for value in re.split(r"[\s,]+", root.get("viewBox", "").strip()) if value]
    if len(view_box) == 4 and view_box[2] > 0 and view_box[3] > 0:
        return view_box[2] / view_box[3]
    width = _number(root.get("width"), 0.0)
    height = _number(root.get("height"), 0.0)
    if width <= 0 or height <= 0:
        raise ValueError(f"SVG sem viewBox ou dimensões positivas: {path}")
    return width / height


def _paragraphs(container):
    """Percorre corpo e células, inclusive tabelas aninhadas."""
    for paragraph in getattr(container, "paragraphs", ()):  # Document/Cell
        yield paragraph
    for table in getattr(container, "tables", ()):
        for row in table.rows:
            for cell in row.cells:
                yield from _paragraphs(cell)


def _next_docpr_id(document) -> int:
    ids = []
    for node in document.part.element.xpath(".//*[local-name()='docPr']"):
        try:
            ids.append(int(node.get("id")))
        except (TypeError, ValueError):
            pass
    return max(ids, default=0) + 1


def _new_svg_part(document, path: Path):
    package = document.part.package
    partname = package.next_partname("/word/media/image%d.svg")
    part = Part(partname, SVG_CONTENT_TYPE, path.read_bytes(), package)
    return document.part.relate_to(part, RT.IMAGE)


def _new_png_part(document, path: Path):
    package = document.part.package
    partname = package.next_partname("/word/media/image%d.png")
    part = Part(partname, PNG_CONTENT_TYPE, path.read_bytes(), package)
    return document.part.relate_to(part, RT.IMAGE)


def _raster_de_reserva(svg: Path) -> Path:
    """Rasteriza o SVG ao lado dele. Sem isto, o Word recusa o arquivo inteiro.

    Descoberto em 07/08/2026: apontar `a:blip r:embed` direto para o SVG produz
    OOXML que o Microsoft Word não abre — a mensagem é de arquivo corrompido, e
    o documento inteiro fica inacessível ao destinatário. O suporte a SVG do
    Office é uma EXTENSÃO: o `blip` aponta para um raster e o vetor entra em
    `a:extLst`. Leitor moderno mostra o vetor; leitor antigo mostra o raster.

    O defeito atravessou o QA porque ele lê o pacote com Python e nunca abriu o
    resultado no programa que vai abri-lo. Auditar o XML prova que o XML é o
    que se quis escrever, e não que o consumidor o aceita.
    """
    from word_visual_pipeline import svg_para_png

    png = svg.with_suffix(".png")
    svg_para_png(str(svg), str(png), dpi=300)
    if not png.is_file() or png.stat().st_size == 0:
        raise RuntimeError(f"raster de reserva não foi gerado para {svg.name}")
    return png


def _inline_svg(document, path: Path, width_cm: float, docpr_id: int):
    ratio = _svg_ratio(path)
    width = max(1, round(float(width_cm) * EMU_PER_CM))
    height = max(1, round(width / ratio))
    rid = _new_svg_part(document, path)
    rid_png = _new_png_part(document, _raster_de_reserva(path))

    inline = OxmlElement("wp:inline")
    inline.set("distT", "0")
    inline.set("distB", "0")
    inline.set("distL", "0")
    inline.set("distR", "0")

    extent = OxmlElement("wp:extent")
    extent.set("cx", str(width))
    extent.set("cy", str(height))
    inline.append(extent)

    effect = OxmlElement("wp:effectExtent")
    for attr in ("l", "t", "r", "b"):
        effect.set(attr, "0")
    inline.append(effect)

    docpr = OxmlElement("wp:docPr")
    docpr.set("id", str(docpr_id))
    docpr.set("name", path.name)
    docpr.set("descr", "Diagrama vetorial FORJA — SVG embutido")
    inline.append(docpr)

    frame = OxmlElement("wp:cNvGraphicFramePr")
    locks = OxmlElement("a:graphicFrameLocks")
    locks.set("noChangeAspect", "1")
    frame.append(locks)
    inline.append(frame)

    graphic = OxmlElement("a:graphic")
    data = OxmlElement("a:graphicData")
    data.set("uri", PIC_URI)
    picture = OxmlElement("pic:pic")

    nv = OxmlElement("pic:nvPicPr")
    c_nv = OxmlElement("pic:cNvPr")
    c_nv.set("id", "0")
    c_nv.set("name", path.name)
    c_nv.set("descr", "Diagrama vetorial FORJA")
    nv.append(c_nv)
    nv.append(OxmlElement("pic:cNvPicPr"))
    picture.append(nv)

    blip_fill = OxmlElement("pic:blipFill")
    blip = OxmlElement("a:blip")
    # O `blip` aponta para o raster; o vetor vem logo abaixo, na extensão que o
    # Office reserva para SVG. A ordem importa: `a:extLst` é o último filho de
    # `a:blip`, e o Word recusa o arquivo se ele vier antes.
    blip.set(qn("r:embed"), rid_png)
    ext_list = OxmlElement("a:extLst")
    ext = OxmlElement("a:ext")
    ext.set("uri", SVG_EXT_URI)
    # O prefixo `asvg` não está no mapa de namespaces do python-docx, então o
    # elemento é criado direto pelo lxml, declarando o namespace nele mesmo.
    svg_blip = etree.SubElement(ext, f"{{{SVG_EXT_NS}}}svgBlip",
                                nsmap={"asvg": SVG_EXT_NS})
    svg_blip.set(qn("r:embed"), rid)
    ext_list.append(ext)
    blip.append(ext_list)
    blip_fill.append(blip)
    source_rect = OxmlElement("a:srcRect")
    source_rect.set("l", "0")
    source_rect.set("t", "0")
    source_rect.set("r", "0")
    source_rect.set("b", "0")
    blip_fill.append(source_rect)
    stretch = OxmlElement("a:stretch")
    stretch.append(OxmlElement("a:fillRect"))
    blip_fill.append(stretch)
    picture.append(blip_fill)

    shape = OxmlElement("pic:spPr")
    transform = OxmlElement("a:xfrm")
    off = OxmlElement("a:off")
    off.set("x", "0")
    off.set("y", "0")
    ext = OxmlElement("a:ext")
    ext.set("cx", str(width))
    ext.set("cy", str(height))
    transform.append(off)
    transform.append(ext)
    shape.append(transform)
    geometry = OxmlElement("a:prstGeom")
    geometry.set("prst", "rect")
    geometry.append(OxmlElement("a:avLst"))
    shape.append(geometry)
    picture.append(shape)

    data.append(picture)
    graphic.append(data)
    inline.append(graphic)
    return inline, rid, width, height


def _validate_svg(path: Path) -> dict:
    from medina_svg_colisao import analisar
    from medina_visual_lint import lint_svg

    colisao = analisar(path)
    lint = lint_svg(path)
    bloqueios = [
        *[item for item in colisao.get("achados", []) if item.get("gravidade") == "bloqueia"],
        *[item for item in lint.get("findings", []) if item.get("severity") == "P0"],
    ]
    if bloqueios:
        resumo = "; ".join(
            str(item.get("mensagem") or item.get("code") or item)[:180]
            for item in bloqueios[:6]
        )
        raise RuntimeError(f"SVG REPROVADO antes do embutimento ({path.name}): {resumo}")
    return {"colisao": colisao, "lint": lint}


def inserir_svgs(docx_path: str | Path, figuras: dict) -> dict:
    """Substitui marcadores por SVGs nativos no pacote DOCX.

    ``figuras`` tem o formato produzido por ``gerar_figuras``:
    ``{"{{FIG1}}": ("fig1.svg", 13.1)}``. Cada marcador precisa existir uma
    única vez e ocupar um parágrafo próprio; qualquer ambiguidade bloqueia para
    não apagar texto jurídico.
    """
    docx_path = Path(docx_path)
    document = Document(str(docx_path))
    paragraphs = list(_paragraphs(document))
    # Texto antes da inserção. Esta função é o único ponto do fluxo que reabre e
    # regrava o DOCX depois de `PecaVisual.salvar()`, isto é, depois da última
    # validação documental. Reexecutar L9-L13 aqui seria reprocessar um texto
    # que não muda; o que faltava era provar que não muda. O invariante abaixo
    # é a prova, e custa uma extração de texto.
    texto_antes = "\n".join(p.text for p in paragraphs)
    docpr_id = _next_docpr_id(document)
    inserted = {}
    for tag, value in (figuras or {}).items():
        svg_value, width_cm = value if isinstance(value, (tuple, list)) else (value, 13.1)
        svg = Path(svg_value)
        if not svg.is_file():
            raise FileNotFoundError(f"SVG da figura não existe: {svg}")
        checks = _validate_svg(svg)
        matches = [paragraph for paragraph in paragraphs if tag in paragraph.text]
        if len(matches) != 1:
            raise RuntimeError(
                f"marcador {tag} deve aparecer uma vez em parágrafo próprio; encontrado {len(matches)}"
            )
        paragraph = matches[0]
        if paragraph.text.strip() != tag:
            raise RuntimeError(f"marcador {tag} misturado a texto; embutimento recusado")
        inline, rid, width, height = _inline_svg(document, svg, float(width_cm), docpr_id)
        docpr_id += 1
        paragraph._p.clear_content()
        # `wp:inline` NÃO é filho legítimo de `w:p`. Ele mora dentro de
        # `w:r/w:drawing`, e sem esse invólucro o Word recusa o documento
        # inteiro com mensagem de arquivo corrompido — o destinatário não abre
        # nada, nem o texto. O defeito viveu de 03/08 a 07/08/2026 porque o QA
        # da rota lê o pacote com Python, e biblioteca de leitura aceita XML
        # que o Word rejeita: auditar a estrutura não é o mesmo que provar que
        # o programa do leitor a aceita.
        run = OxmlElement("w:r")
        drawing = OxmlElement("w:drawing")
        drawing.append(inline)
        run.append(drawing)
        paragraph._p.append(run)
        inserted[tag] = {
            "svg": str(svg),
            "svgSha256": hashlib.sha256(svg.read_bytes()).hexdigest(),
            "relationshipId": rid,
            "contentType": SVG_CONTENT_TYPE,
            "widthCm": float(width_cm),
            "heightEmu": height,
            "widthEmu": width,
            "qa": checks,
        }
    # A única diferença legítima entre antes e depois é o desaparecimento dos
    # marcadores consumidos. Qualquer outra alteração significa que o produto
    # mudou depois do último gate documental, e aí o gate deixou de valer.
    esperado = texto_antes
    for tag in inserted:
        esperado = esperado.replace(tag, "", 1)
    depois = "\n".join(p.text for p in _paragraphs(document))
    if depois != esperado:
        raise RuntimeError(
            "inserção de SVG alterou o texto do DOCX além dos marcadores consumidos — "
            "o produto mudou depois da última validação documental"
        )
    document.save(str(docx_path))
    return inserted


__all__ = ["inserir_svgs"]
