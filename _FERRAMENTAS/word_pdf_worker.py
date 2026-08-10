"""Isolated Word COM worker used by word_visual_pipeline.py."""

from __future__ import annotations

import os
import sys
import traceback
import ctypes
from ctypes import wintypes
from pathlib import Path


class PROCESSENTRY32W(ctypes.Structure):
    _fields_ = [
        ("dwSize", wintypes.DWORD),
        ("cntUsage", wintypes.DWORD),
        ("th32ProcessID", wintypes.DWORD),
        ("th32DefaultHeapID", ctypes.c_size_t),
        ("th32ModuleID", wintypes.DWORD),
        ("cntThreads", wintypes.DWORD),
        ("th32ParentProcessID", wintypes.DWORD),
        ("pcPriClassBase", wintypes.LONG),
        ("dwFlags", wintypes.DWORD),
        ("szExeFile", wintypes.WCHAR * 260),
    ]


def _winword_pids() -> set[int]:
    snapshot = ctypes.windll.kernel32.CreateToolhelp32Snapshot(0x00000002, 0)
    if snapshot == wintypes.HANDLE(-1).value:
        return set()
    entry = PROCESSENTRY32W()
    entry.dwSize = ctypes.sizeof(entry)
    pids = set()
    try:
        ok = ctypes.windll.kernel32.Process32FirstW(snapshot, ctypes.byref(entry))
        while ok:
            if entry.szExeFile.lower() == "winword.exe":
                pids.add(int(entry.th32ProcessID))
            ok = ctypes.windll.kernel32.Process32NextW(snapshot, ctypes.byref(entry))
    finally:
        ctypes.windll.kernel32.CloseHandle(snapshot)
    return pids


def main() -> int:
    if len(sys.argv) != 5:
        print("uso: word_pdf_worker.py <docx> <pdf-temporario> <pid-file> <status-file>", file=sys.stderr)
        return 2
    source, destination, pid_path, status_path = map(os.path.abspath, sys.argv[1:])
    import pythoncom
    import win32com.client
    pythoncom.CoInitialize()
    word = None
    doc = None
    try:
        Path(status_path).write_text("dispatch_started", encoding="ascii")
        before = _winword_pids()
        word = win32com.client.DispatchEx("Word.Application")
        Path(status_path).write_text("word_created", encoding="ascii")
        created = _winword_pids() - before
        if len(created) == 1:
            Path(pid_path).write_text(str(next(iter(created))), encoding="ascii")
        word.Visible = False
        word.DisplayAlerts = 0
        try:
            word.Options.SaveNormalPrompt = False
            word.Options.ConfirmConversions = False
        except Exception:
            pass
        try:
            word.AutomationSecurity = 3
        except Exception:
            pass
        Path(status_path).write_text("document_open_started", encoding="ascii")
        # `OpenAndRepair=True` dispara a passagem de reparo do Word em TODO
        # documento, e ela não tem teto de tempo. Em 10/08/2026 três entregáveis
        # de um mesmo caso estouraram os 75 segundos do processo pai sempre no
        # mesmo ponto, `document_open_started`, e a mesma máquina os abria em
        # 0,3 segundo sem esse parâmetro — inclusive o arquivo original,
        # intocado, o que descartou defeito de conteúdo. O resultado foi um "não
        # dá para converter" falso sobre documento saudável, e a falsa causa é
        # cara: ela manda diagnosticar o arquivo em vez da ferramenta.
        # O reparo continua disponível, mas como segunda tentativa: quem precisa
        # dele é o arquivo corrompido, e esse falha na abertura normal primeiro.
        abertura = dict(FileName=source, ConfirmConversions=False, ReadOnly=True,
                        AddToRecentFiles=False, Revert=False, NoEncodingDialog=True)
        try:
            doc = word.Documents.Open(**abertura)
        except Exception:
            Path(status_path).write_text("document_open_repair", encoding="ascii")
            doc = word.Documents.Open(**abertura, OpenAndRepair=True)
        Path(status_path).write_text("document_opened", encoding="ascii")
        Path(status_path).write_text("export_started", encoding="ascii")
        doc.ExportAsFixedFormat(destination, 17, False, 0, 0, 0, 0, False)
        Path(status_path).write_text("exported", encoding="ascii")
        return 0
    except Exception:
        traceback.print_exc(file=sys.stderr)
        return 1
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
