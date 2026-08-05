from __future__ import annotations

import re
import zipfile
from pathlib import Path

from lxml import etree


NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "v": "urn:schemas-microsoft-com:vml",
    "wps": "http://schemas.microsoft.com/office/word/2010/wordprocessingShape",
}


def _reescrever_pacote(docx: Path, mutator) -> None:
    with zipfile.ZipFile(docx) as archive:
        data = {name: archive.read(name) for name in archive.namelist()}
    mutator(data)
    with zipfile.ZipFile(docx, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, blob in data.items():
            archive.writestr(name, blob)


def ajustar_folio_lateral(docx: str | Path, largura_pt: float = 28.0) -> None:
    """Mantém o fólio áureo na extrema direita, fora da faixa das notas."""
    caminho = Path(docx)
    largura_emu = round(largura_pt * 12700)

    def mutator(data):
        target = "word/header2.xml"
        if target not in data:
            return
        xml = data[target].decode("utf-8")
        xml = re.sub(
            r'(<wp:extent\s+cx=")\d+("\s+cy="\d+"\s*/>)',
            rf"\g<1>{largura_emu}\g<2>",
            xml,
            count=1,
        )
        xml = re.sub(
            r'(<a:ext\s+cx=")\d+("\s+cy="\d+"\s*/>)',
            rf"\g<1>{largura_emu}\g<2>",
            xml,
            count=1,
        )
        xml = re.sub(
            r"<wp14:sizeRelH\b.*?</wp14:sizeRelH>",
            "",
            xml,
            count=1,
            flags=re.DOTALL,
        )
        xml = re.sub(r"width:\d+(?:\.\d+)?pt", f"width:{largura_pt:g}pt", xml)
        xml = re.sub(r"margin-left:\d+(?:\.\d+)?pt", "margin-left:0pt", xml)
        data[target] = xml.encode("utf-8")

    _reescrever_pacote(caminho, mutator)


def remover_barras_cinzas_template(docx: str | Path) -> None:
    """Remove apenas as duas cápsulas cinzas vazias do cabeçalho da capa."""
    caminho = Path(docx)

    def mutator(data):
        target = "word/header3.xml"
        if target not in data:
            return
        root = etree.fromstring(data[target])
        removidos = 0
        for node in list(root.xpath(".//wps:wsp", namespaces=NS)):
            cores = node.xpath(
                ".//a:fillRef/a:srgbClr/@val | .//a:solidFill/a:srgbClr/@val",
                namespaces=NS,
            )
            if any(str(cor).upper() == "E6E7E7" for cor in cores):
                node.getparent().remove(node)
                removidos += 1
        for node in list(root.xpath(".//v:shape", namespaces=NS)):
            if str(node.get("fillcolor", "")).lower() == "#e6e7e7":
                node.getparent().remove(node)
                removidos += 1
        if removidos:
            data[target] = etree.tostring(
                root,
                xml_declaration=True,
                encoding="UTF-8",
                standalone=True,
            )

    _reescrever_pacote(caminho, mutator)


def sanear_release_docx(docx: str | Path) -> None:
    # O template dos estudos internos nasce com o fólio centralizado na margem.
    # A liberação final exige a mesma assinatura áurea das peças judiciais.
    from medina_visual_kit import _aplicar_folio_aureo

    _aplicar_folio_aureo(docx)
    ajustar_folio_lateral(docx)
    remover_barras_cinzas_template(docx)
