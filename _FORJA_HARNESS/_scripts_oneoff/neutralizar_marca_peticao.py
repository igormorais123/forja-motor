from __future__ import annotations

import sys
from pathlib import Path

import pythoncom
import win32com.client


def clear_story(story) -> None:
    try:
        story.LinkToPrevious = False
    except Exception:
        pass
    try:
        story.Range.Text = ""
    except Exception:
        pass
    try:
        while story.Shapes.Count:
            story.Shapes(1).Delete()
    except Exception:
        pass


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("uso: python neutralizar_marca_peticao.py arquivo.docx")
    path = Path(sys.argv[1]).resolve()
    pythoncom.CoInitialize()
    word = None
    doc = None
    try:
        word = win32com.client.DispatchEx("Word.Application")
        word.Visible = False
        word.DisplayAlerts = 0
        doc = word.Documents.Open(str(path), ReadOnly=False, AddToRecentFiles=False)
        print("aberto", flush=True)
        for section in doc.Sections:
            for index in (1, 2, 3):
                clear_story(section.Headers(index))
                clear_story(section.Footers(index))
        print("marca removida", flush=True)
        compact_address = "ENDERECO_EXEQUIBILIDADE" in path.name.upper()
        annex = doc.Content.Duplicate
        if annex.Find.Execute("ANEXO — MINUTA DE ACORDO GLOBAL CONDICIONADO"):
            annex.Paragraphs(1).Format.PageBreakBefore = True
        print("anexo ajustado", flush=True)
        if compact_address:
            requests = doc.Content.Duplicate
            if requests.Find.Execute("V — DOS PEDIDOS"):
                requests.SetRange(requests.Paragraphs(1).Range.End, doc.Content.End)
                requests.ParagraphFormat.LineSpacingRule = 5
                requests.ParagraphFormat.LineSpacing = 13.8
        print("layout ajustado", flush=True)
        try:
            doc.BuiltInDocumentProperties("Author").Value = "Wagner César Vieira"
            doc.BuiltInDocumentProperties("Last Author").Value = "Wagner César Vieira"
            doc.BuiltInDocumentProperties("Company").Value = ""
        except Exception:
            pass
        print("metadados ajustados", flush=True)
        doc.Save()
        print("salvo", flush=True)
        doc.Close(False)
        doc = None
        print(path)
        return 0
    finally:
        if doc is not None:
            try:
                doc.Close(False)
            except Exception:
                pass
        if word is not None:
            try:
                word.Quit()
            except Exception:
                pass
        pythoncom.CoUninitialize()


if __name__ == "__main__":
    raise SystemExit(main())
