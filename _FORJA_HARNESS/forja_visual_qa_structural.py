# -*- coding: utf-8 -*-
"""QA visual determinística sem renderização.

A rota oficial inspeciona o que é verificável no DOCX e nos SVGs: pacote OOXML,
marcadores, fidelidade textual, tipografia, metadados, relações SVG e
geometria. Não chama Word, LibreOffice, PyMuPDF, conversor PDF ou rasterizador.
O resultado é um laudo de observação; a aprovação jurídica continua humana.
"""

from __future__ import annotations

import json
import re
import zipfile
from pathlib import Path

from forja_fidelity import compare_docx_fidelity
from forja_n3_common import now_iso, sha256_file


def _svg_check(path: Path) -> dict:
    from medina_svg_colisao import analisar
    from medina_visual_lint import lint_svg

    colisao = analisar(path)
    lint = lint_svg(path)
    findings = [
        {**item, "source": "medina_svg_colisao"}
        for item in colisao.get("achados", [])
        if item.get("gravidade") == "bloqueia"
    ]
    findings.extend(
        {**item, "source": "medina_visual_lint"}
        for item in lint.get("findings", [])
        if item.get("severity") == "P0"
    )
    return {
        "file": str(path),
        "sha256": sha256_file(path),
        "colisao": colisao,
        "lint": lint,
        "findings": findings,
        "approved": not findings,
    }


def _package_audit(docx: Path) -> dict:
    findings = []
    try:
        with zipfile.ZipFile(docx) as archive:
            names = set(archive.namelist())
            required = {"[Content_Types].xml", "word/document.xml", "word/_rels/document.xml.rels"}
            for name in sorted(required - names):
                findings.append({"severity": "P0", "code": "docx_part_missing", "part": name})
            document_xml = archive.read("word/document.xml").decode("utf-8", "replace")
            rels_xml = archive.read("word/_rels/document.xml.rels").decode("utf-8", "replace")
            types_xml = archive.read("[Content_Types].xml").decode("utf-8", "replace")
            markers = re.findall(r"\{\{[^}]+\}\}", document_xml)
            if markers:
                findings.append({"severity": "P0", "code": "unresolved_visual_marker", "markers": sorted(set(markers))})
            svg_media = sorted(name for name in names if name.lower().endswith(".svg"))
            for name in svg_media:
                if name not in rels_xml and name.lstrip("/") not in rels_xml:
                    # Relações guardam o alvo relativo (media/imageN.svg).
                    if Path(name).name not in rels_xml:
                        findings.append({"severity": "P0", "code": "svg_without_document_relationship", "part": name})
                if 'ContentType="image/svg+xml"' not in types_xml:
                    findings.append({"severity": "P0", "code": "svg_content_type_missing", "part": name})
            return {
                "validZip": True,
                "parts": len(names),
                "svgMedia": svg_media,
                "markers": markers,
                "findings": findings,
                "approved": not findings,
            }
    except (OSError, zipfile.BadZipFile, KeyError) as exc:
        findings.append({"severity": "P0", "code": "docx_package_unreadable", "detail": str(exc)})
        return {"validZip": False, "parts": 0, "svgMedia": [], "markers": [], "findings": findings, "approved": False}


def _docx_lint(docx: Path) -> dict:
    from forja_visual_qa import lint_docx
    from forja_docx_layout import audit_docx_layout

    lint = lint_docx(docx)
    try:
        layout = audit_docx_layout(docx)
    except Exception as exc:  # laudo não pode esconder falha estrutural
        layout = {"approved": False, "findings": [{"severity": "P0", "code": "layout_audit_error", "detail": str(exc)}]}
    return {"lint": lint, "layout": layout}


def auditar_documento(docx: str | Path, *, markdown: str | Path | None = None,
                      svgs: list[str | Path] | None = None) -> dict:
    """Executa a régua estática e devolve um laudo serializável."""
    docx = Path(docx)
    package = _package_audit(docx)
    textual = _docx_lint(docx)
    fidelity = compare_docx_fidelity(Path(markdown), docx) if markdown else None
    svg_results = [_svg_check(Path(path)) for path in (svgs or [])]
    findings = list(package.get("findings") or [])
    findings += list(textual["lint"].get("findings") or [])
    findings += list(textual["layout"].get("findings") or [])
    if fidelity and not fidelity.get("approved"):
        findings += list(fidelity.get("findings") or [])
    for result in svg_results:
        findings += list(result.get("findings") or [])
    return {
        "schemaVersion": 1,
        "generatedAt": now_iso(),
        "mode": "static_ooxml_svg",
        "renderingUsed": False,
        "pdfCreated": False,
        "pngCreated": False,
        "docx": {"path": str(docx), "sha256": sha256_file(docx)},
        "package": package,
        "docxLint": textual["lint"],
        "layoutAudit": textual["layout"],
        "fidelity": fidelity,
        "svg": svg_results,
        "findings": findings,
        "approved": not findings,
    }


def write_audit(docx: str | Path, output: str | Path, *, markdown=None, svgs=None) -> dict:
    result = auditar_documento(docx, markdown=markdown, svgs=svgs)
    Path(output).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result


__all__ = ["auditar_documento", "write_audit"]
