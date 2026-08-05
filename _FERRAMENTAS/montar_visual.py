# -*- coding: utf-8 -*-
"""Montagem final das edições visual law: SVG→EMF (gate) → inserção via Word COM
nos marcadores → PDF → render das páginas para o QA obrigatório.

Uso (no diretório da peça):
    import sys; sys.path.insert(0, r'..\\..\\_FERRAMENTAS')  # ajustar nível
    from montar_visual import montar
    montar("PECA.docx", {"{{CARDS}}": ("cards.svg", 13.1), "{{FIG1}}": ("fig1.svg", 12.0)})
"""
import os
import shutil
from word_visual_pipeline import svg_para_emf, render_paginas
from medina_svg_kit import _gate_v2_enabled


def montar(docx, figs, qa_dir="qa", dpi=100, *, generator_run_id=None,
           reviewer_run_id=None, ledger_path=None, markdown_path=None,
           fidelity_path=None, word_stage_dir=None):
    """figs: {'{{TAG}}': (svg_path, largura_cm), ...}. Retorna (pdf, paginas)."""
    import win32com.client
    emfs = {}
    for tag, (svg, larg) in figs.items():
        emf = os.path.splitext(svg)[0] + ".emf"
        svg_para_emf(svg, emf, largura_final_cm=larg)
        emfs[tag] = (emf, larg)

    target_docx = os.path.abspath(docx)
    target_pdf = os.path.splitext(target_docx)[0] + ".pdf"
    word_docx = target_docx
    word_pdf = target_pdf
    if word_stage_dir:
        stage = os.path.abspath(word_stage_dir)
        os.makedirs(stage, exist_ok=True)
        word_docx = os.path.join(stage, "document.docx")
        word_pdf = os.path.join(stage, "document.pdf")
        for stale in (word_docx, word_pdf):
            if os.path.exists(stale):
                os.unlink(stale)
        shutil.copy2(target_docx, word_docx)
    # DispatchEx: instância própria do Word — não conflita com documentos que o
    # usuário estiver com abertos na tela (lição 09/07: Dispatch reaproveitava a
    # instância aberta e o objeto retornado perdia os métodos de Document)
    word = win32com.client.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0          # wdAlertsNone — nenhum diálogo modal invisível
    try:
        word.AutomationSecurity = 3  # msoAutomationSecurityForceDisable (sem macros)
    except Exception:
        pass
    doc = None
    try:
        doc = word.Documents.Open(word_docx)
        for marcador, (emf, larg) in emfs.items():
            find = word.Selection.Find
            word.Selection.HomeKey(6)  # wdStory
            find.ClearFormatting()
            if find.Execute(marcador):
                word.Selection.Text = ""
                shape = word.Selection.InlineShapes.AddPicture(
                    os.path.abspath(emf), False, True)
                escala = (larg * 28.3465) / shape.Width
                shape.Width = int(shape.Width * escala)
                shape.Height = int(shape.Height * escala)
                word.Selection.ParagraphFormat.Alignment = 1
                print("inserido:", marcador)
            else:
                raise RuntimeError(f"MARCADOR NÃO ENCONTRADO: {marcador}")
        doc.Save()
        # ExportAsFixedFormat mantém o DOCX aberto no formato nativo e evita o
        # modal invisível que SaveAs(FileFormat=17) pode disparar após várias
        # instâncias COM sucessivas. A saída continua sendo o PDF nativo do Word.
        doc.ExportAsFixedFormat(word_pdf, 17)
    finally:
        # fechar o doc SEMPRE, mesmo em erro no meio da inserção (review 09/07/2026)
        if doc is not None:
            doc.Close(False)
        word.Quit()

    # Word rewrites lastModifiedBy during Save/SaveAs. Normalize the physical
    # finals before hashes, page renders and F8 are calculated.
    import sys
    from pathlib import Path
    harness = Path(__file__).resolve().parents[1] / "_FORJA_HARNESS"
    sys.path.insert(0, str(harness))
    from forja_metadata import sanitize_final_artifacts
    sanitize_final_artifacts(word_docx, word_pdf)
    if word_stage_dir:
        shutil.copy2(word_docx, target_docx)
        shutil.copy2(word_pdf, target_pdf)

    docx = target_docx
    pdf = target_pdf

    paginas = render_paginas(pdf, qa_dir, dpi=dpi)
    print(f"{pdf}: {len(paginas)} páginas em {qa_dir}/")
    if _gate_v2_enabled():
        if not generator_run_id or not reviewer_run_id or not markdown_path:
            raise RuntimeError("visualGateV2 exige markdown_path e runs independentes de geração/revisão")
        harness = Path(__file__).resolve().parents[1] / "_FORJA_HARNESS"
        sys.path.insert(0, str(harness))
        from forja_visual_qa import run_visual_qa
        ledger_path = Path(ledger_path) if ledger_path else Path(qa_dir) / "F8_QA_LEDGER.json"
        ledger = run_visual_qa(
            Path(pdf), ledger_path, qa_dir=Path(qa_dir) / "v2",
            generator_run_id=generator_run_id, reviewer_run_id=reviewer_run_id,
            docx=Path(docx), markdown=Path(markdown_path),
            fidelity_output=Path(fidelity_path) if fidelity_path else None,
            svgs=[Path(value[0]) for value in figs.values()],
        )
        if not ledger["approved"]:
            raise RuntimeError(f"QA visual V2 reprovado: {ledger_path}")
    return pdf, paginas


def anti_placeholder(pdf):
    """Varredura do texto do PDF final. Retorna lista de achados (vazia = ok)."""
    import fitz, re
    d = fitz.open(pdf)
    txt = "".join(p.get_text() for p in d)
    return re.findall(r"\{\{[^}]*\}\}|\[(?:NOME|VERIFICAR|dia|m.s|ano|CRC[^\]]*)\]", txt)
