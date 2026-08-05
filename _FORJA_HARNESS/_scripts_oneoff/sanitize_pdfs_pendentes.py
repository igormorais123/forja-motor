# -*- coding: utf-8 -*-
"""Sanitiza os 2 PDFs N3 que estavam abertos no PDFelement em 10/07/2026.

Uso: fechar o PDFelement e rodar `python sanitize_pdfs_pendentes.py`.
Contexto: auditoria ultracode 10/07 — todos os demais DOCX/PDF N3 já foram
sanitizados (autor 'thais mulati' / título 'Proposta de Serviços e Honorários'
herdados do template). Este script é idempotente e se auto-remove no sucesso.
"""
import os
import sys

from pypdf import PdfReader, PdfWriter

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALVOS = [
    os.path.join(BASE, "Análise de caso pessoal Fábio Medina Osório - Plano de Saúde",
                 "_forja_n3_reconstrucao_2026-07-10",
                 "PETICAO_INICIAL_TJDFT_MATEUS_NIVEL_SOL_V6_N3_10-07-2026.pdf"),
    os.path.join(BASE, "Memoriais AgInt AREsp 2578181 SC - LIBRA SUL",
                 "_forja_n3_reconstrucao_2026-07-10",
                 "MEMORIAIS_LIBRA_SUL_N3_SUPERIOR.pdf"),
]

pendentes = 0
for f in ALVOS:
    r = PdfReader(f)
    md = dict(r.metadata or {})
    if md.get("/Author") != "thais mulati" and md.get("/Title") != "Proposta de Serviços e Honorários":
        print("já limpo:", os.path.basename(f))
        continue
    try:
        w = PdfWriter()
        w.append(r)
        md["/Author"] = "Medina Osório Advogados"
        md["/Title"] = os.path.splitext(os.path.basename(f))[0].replace("_", " ")
        md.pop("/Subject", None)
        w.add_metadata(md)
        tmp = f + ".tmp"
        with open(tmp, "wb") as fh:
            w.write(fh)
        os.replace(tmp, f)
        print("sanitizado:", os.path.basename(f))
    except OSError as e:
        print("AINDA BLOQUEADO (feche o visualizador):", os.path.basename(f), "|", e)
        pendentes += 1

if pendentes:
    sys.exit(1)
os.remove(os.path.abspath(__file__))
print("tudo limpo — script auto-removido")
