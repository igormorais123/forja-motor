from __future__ import annotations

import sys
from pathlib import Path

from docx import Document
from docx.oxml import OxmlElement


def clear_story(story) -> None:
    element = story._element
    for child in list(element):
        element.remove(child)
    element.append(OxmlElement("w:p"))


def main() -> int:
    path = Path(sys.argv[1]).resolve()
    doc = Document(path)
    seen = set()
    for section in doc.sections:
        for story in (
            section.header,
            section.first_page_header,
            section.even_page_header,
            section.footer,
            section.first_page_footer,
            section.even_page_footer,
        ):
            key = str(story.part.partname)
            if key not in seen:
                clear_story(story)
                seen.add(key)

    compact = "ENDERECO_EXEQUIBILIDADE" in path.name.upper()
    in_requests = False
    for paragraph in doc.paragraphs:
        text = paragraph.text.strip()
        if text.startswith("ANEXO — MINUTA DE ACORDO"):
            paragraph.paragraph_format.page_break_before = True
        if compact and text.startswith("V — DOS PEDIDOS"):
            in_requests = True
        elif in_requests and text:
            paragraph.paragraph_format.line_spacing = 1.15

    doc.core_properties.author = "Wagner César Vieira"
    doc.core_properties.last_modified_by = "Wagner César Vieira"
    doc.save(path)
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
