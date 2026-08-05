from __future__ import annotations

import sys
from pathlib import Path

import forja_render_docx


# O sanitizador ZIP corrente da FORJA invalida o DOCX para o Word nativo.
# A higienização de marca e metadados desta demanda ocorre depois, via Word COM.
forja_render_docx.sanitize_final_artifacts = lambda docx, pdf: None


def _docx_only(docx, pdf):
    # O Word COM pode permanecer bloqueado em estações com instâncias órfãs.
    # Neste modo a FORJA materializa apenas o DOCX; PDF e QA são executados
    # separadamente, depois da neutralização de marca.
    Path(pdf).touch()


def _skip_page_render(pdf, paginas_dir, dpi=110):
    Path(paginas_dir).mkdir(parents=True, exist_ok=True)


if "--docx-only" in sys.argv:
    sys.argv.remove("--docx-only")
    forja_render_docx.docx_para_pdf = _docx_only
    forja_render_docx.render_paginas = _skip_page_render


if __name__ == "__main__":
    forja_render_docx.render(
        sys.argv[1],
        sys.argv[2],
        sys.argv[3] if len(sys.argv) > 3 else "Peça FORJA",
    )
