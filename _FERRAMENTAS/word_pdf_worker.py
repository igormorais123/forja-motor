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
        doc = word.Documents.Open(
            FileName=source,
            ConfirmConversions=False,
            ReadOnly=True,
            AddToRecentFiles=False,
            Revert=False,
            OpenAndRepair=True,
            NoEncodingDialog=True,
        )
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
