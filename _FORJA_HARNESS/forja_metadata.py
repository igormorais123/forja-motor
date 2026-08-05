"""Normalize final DOCX/PDF metadata after Word has finished writing files."""

from __future__ import annotations

import os
import re
import tempfile
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape


OFFICE = "Medina Osório Advogados"
CP = "http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
DC = "http://purl.org/dc/elements/1.1/"

# Errnos transitórios no Windows quando Word COM/AV/sessão paralela segura o arquivo
# por instantes (EINVAL e EACCES observados na bateria real de 23/07/2026).
_TRANSIENT_ERRNOS = {13, 22}


def retry_transient_io(operation, *, tries: int = 6, base_delay: float = 0.5):
    """Reexecuta operação de I/O quando o erro é lock transitório; relança os demais."""
    import time

    last: OSError | None = None
    delay = base_delay
    for attempt in range(tries):
        try:
            return operation()
        except OSError as exc:
            if exc.errno not in _TRANSIENT_ERRNOS:
                raise
            last = exc
            if attempt < tries - 1:
                time.sleep(delay)
                delay = min(delay * 2, 8.0)
    raise last  # type: ignore[misc]


def _replace_core_text(xml: bytes, tag: str, value: str) -> bytes:
    """Replace a Dublin Core/core-properties value without reserializing XML.

    ElementTree rewrites namespace prefixes (and can leave QName-valued
    attributes such as ``xsi:type=\"dcterms:W3CDTF\"`` pointing at an
    undeclared prefix). Word then reports the DOCX as corrupt. Keeping the
    original XML bytes preserves the template's namespace declarations and
    prefix choices.
    """
    text = xml.decode("utf-8")
    safe = escape(value)
    pattern = rf"(<{re.escape(tag)}(?:\s[^>]*)?>).*?(</{re.escape(tag)}>)"
    replaced, count = re.subn(pattern, rf"\1{safe}\2", text, count=1, flags=re.S)
    if count:
        return replaced.encode("utf-8")
    marker = "</cp:coreProperties>"
    if marker in replaced:
        replaced = replaced.replace(marker, f"<{tag}>{safe}</{tag}>{marker}", 1)
    return replaced.encode("utf-8")


def sanitize_docx(path: Path) -> None:
    def _once() -> None:
        resolved = path.resolve()
        fd, temp_name = tempfile.mkstemp(prefix=f".{resolved.stem}.", suffix=".docx.tmp", dir=resolved.parent)
        os.close(fd)
        temp = Path(temp_name)
        try:
            with zipfile.ZipFile(resolved, "r") as source, zipfile.ZipFile(temp, "w") as target:
                for entry in source.infolist():
                    data = source.read(entry.filename)
                    if entry.filename == "docProps/core.xml":
                        # Preserve namespace prefixes and QName-valued attributes;
                        # see _replace_core_text for why a full XML round-trip is
                        # unsafe for Word core-properties.
                        data = _replace_core_text(data, "dc:creator", OFFICE)
                        data = _replace_core_text(data, "cp:lastModifiedBy", OFFICE)
                    target.writestr(entry, data)
            os.replace(temp, resolved)
        finally:
            temp.unlink(missing_ok=True)

    retry_transient_io(_once)


def sanitize_pdf(path: Path) -> None:
    import fitz

    def _once() -> None:
        resolved = path.resolve()
        fd, temp_name = tempfile.mkstemp(prefix=f".{resolved.stem}.", suffix=".pdf.tmp", dir=resolved.parent)
        os.close(fd)
        temp = Path(temp_name)
        temp.unlink(missing_ok=True)
        try:
            with fitz.open(resolved) as source:
                metadata = dict(source.metadata or {})
                metadata["author"] = OFFICE
                source.set_metadata(metadata)
                source.save(temp, garbage=4, deflate=True)
            os.replace(temp, resolved)
        finally:
            temp.unlink(missing_ok=True)

    retry_transient_io(_once)


def sanitize_final_artifacts(docx: str | Path, pdf: str | Path) -> None:
    sanitize_docx(Path(docx))
    sanitize_pdf(Path(pdf))
