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

from docx import Document
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.opc.part import Part
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm


SVG_CONTENT_TYPE = "image/svg+xml"
PIC_URI = "http://schemas.openxmlformats.org/drawingml/2006/picture"
EMU_PER_CM = 360000
FORJA = Path(__file__).resolve().parent
sys.path.insert(0, str(FORJA.parent / "_FERRAMENTAS"))


def _local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


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


def _inline_svg(document, path: Path, width_cm: float, docpr_id: int):
    ratio = _svg_ratio(path)
    width = max(1, round(float(width_cm) * EMU_PER_CM))
    height = max(1, round(width / ratio))
    rid = _new_svg_part(document, path)

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
    blip.set(qn("r:embed"), rid)
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
        paragraph._p.append(inline)
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
