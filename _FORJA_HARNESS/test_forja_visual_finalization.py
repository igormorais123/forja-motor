# -*- coding: utf-8 -*-
"""Regressões da finalização visual descobertas na peça Vale, 10/08/2026."""
import hashlib
import json
import sys
import zipfile
from pathlib import Path

FORJA = Path(__file__).resolve().parent
FERRAMENTAS = FORJA.parent / "_FERRAMENTAS"
sys.path.insert(0, str(FORJA))
sys.path.insert(0, str(FERRAMENTAS))

from forja_assinatura_visual import avaliar  # noqa: E402
from forja_visual_build import _rebind_integrity_ledgers  # noqa: E402
from word_visual_pipeline import render_paginas  # noqa: E402


def _docx_minimo(path):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as pacote:
        pacote.writestr("word/document.xml", "<w:document><w:body/></w:document>")
    return path


def test_recibos_apontam_para_docx_pos_svg(tmp_path):
    docx = tmp_path / "peca_VISUAL_LAW.docx"
    docx.write_bytes(b"pacote-ooxml-depois-dos-svgs")
    recibos = (
        tmp_path / "FIDELIDADE_VISUAL.json",
        tmp_path / "peca_VISUAL_LAW_PORTA_UNICA.json",
    )
    for recibo in recibos:
        recibo.write_text(json.dumps({"docxSha256": "hash-anterior"}), encoding="utf-8")

    resultado = _rebind_integrity_ledgers(docx)
    esperado = hashlib.sha256(docx.read_bytes()).hexdigest()

    assert resultado["docxSha256"] == esperado
    for recibo in recibos:
        dados = json.loads(recibo.read_text(encoding="utf-8"))
        assert dados["docxSha256"] == esperado
        assert dados["integridadeVinculadaAposSvgOoxml"] is True


def test_build_nao_usa_pdf_irmao_antigo(tmp_path):
    import fitz

    docx = _docx_minimo(tmp_path / "peca.docx")
    pdf = fitz.open()
    pdf.new_page()
    pdf.save(tmp_path / "peca.pdf")
    pdf.close()

    assert avaliar(docx, buscar_pdf_irmao=True)["paginas"] == 1
    laudo = avaliar(docx, buscar_pdf_irmao=False)
    assert laudo["paginas"] is None
    assert laudo["densidadeCalibrada"] is False


def test_render_remove_so_paginas_antigas_da_propria_saida(tmp_path):
    import fitz

    pdf_path = tmp_path / "uma_pagina.pdf"
    pdf = fitz.open()
    pdf.new_page()
    pdf.save(pdf_path)
    pdf.close()

    saida = tmp_path / "qa"
    saida.mkdir()
    (saida / "p13.png").write_bytes(b"pagina-obsoleta")
    (saida / "preservar.png").write_bytes(b"arquivo-do-usuario")

    paginas = render_paginas(str(pdf_path), str(saida), dpi=72)

    assert [Path(p).name for p in paginas] == ["p01.png"]
    assert not (saida / "p13.png").exists()
    assert (saida / "preservar.png").read_bytes() == b"arquivo-do-usuario"
