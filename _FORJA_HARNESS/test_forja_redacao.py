# -*- coding: utf-8 -*-
"""test_forja_redacao.py — regressão dos gates computados da F6.

A contraprova mais importante está no fim: os treze rascunhos reais do acervo,
rodados pelos detectores que até 04/08/2026 só existiam na F7-B. Nenhum produz
achado. Esse zero é o argumento de que instalar os gates mais cedo não trava
ninguém — e se um dia deixar de ser zero, é porque a rota mudou, não porque o
gate ficou rígido.

Uso: python test_forja_redacao.py   (exit 0 = ok; exit 1 = regressão)
"""
from __future__ import annotations

import io
import json
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from forja_redacao import (  # noqa: E402
    GATE_ENTIDADES, GATE_TEMPLATE, GATE_VOZ, validar_redacao)

LIMPO = ("# Manifestação\n\n1. A parte requer a reforma da decisão do evento 228, "
         "juntada aos autos.\n\n2. Pede deferimento.\n")
PROV_OK = {"template": "TEMPLATE_MEDINA_OSORIO_PETICAO.docx",
           "foreignEntityCheck": {"status": "pass", "unexpectedEntities": []}}


def main() -> int:
    falhas = 0
    casos = 0

    def checar(nome, obtido, esperado):
        nonlocal falhas, casos
        casos += 1
        if obtido != esperado:
            print(f"  FALHOU: {nome} — esperado {esperado}, obtido {obtido}")
            falhas += 1

    def g(prov, texto, gate):
        return validar_redacao(prov, texto)["gates"][gate]

    checar("rascunho ausente", g(PROV_OK, None, GATE_VOZ), "fail")
    checar("rascunho limpo", g(PROV_OK, LIMPO, GATE_VOZ), "pass")

    # A regra inviolável de 11/07: origem operacional no corpo da peça é P0.
    for vazamento in (
            "conforme arquivo compartilhado pelo escritório",
            "documento recebido por e-mail em 12/07",
            "planilha enviada por WhatsApp pelo cliente"):
        casos += 1
        texto = LIMPO.replace("juntada aos autos", vazamento)
        if validar_redacao(PROV_OK, texto)["gates"][GATE_VOZ] != "fail":
            print(f"  FALHOU (não pegou origem operacional): {vazamento}")
            falhas += 1

    checar("entidade estranha listada pela própria conferência",
           g({**PROV_OK, "foreignEntityCheck": {"status": "pass",
                                                "unexpectedEntities": ["Banco Alfa S.A."]}},
             LIMPO, GATE_ENTIDADES), "fail")
    checar("conferência de entidades encerrada com status diferente de pass",
           g({**PROV_OK, "foreignEntityCheck": {"status": "blocked"}}, LIMPO, GATE_ENTIDADES),
           "fail")
    checar("entidades não conferidas",
           g({"template": "x"}, LIMPO, GATE_ENTIDADES), "warn")
    checar("dialeto de qualityControls",
           g({"template": "x", "qualityControls": {"unexplainedForeignEntities": False}},
             LIMPO, GATE_ENTIDADES), "pass")

    checar("template não declarado", g({}, LIMPO, GATE_TEMPLATE), "warn")
    checar("template declarado", g(PROV_OK, LIMPO, GATE_TEMPLATE), "pass")

    # CONTRAPROVA — os rascunhos reais. Nenhum pode produzir achado de voz.
    rascunhos, reprovados = 0, []
    for arquivo in Path("state").rglob("F6_REDACAO_TEMPLATE/**/draft_markdown.md"):
        texto = arquivo.read_text(encoding="utf-8", errors="replace")
        prov = {}
        vizinho = arquivo.parent / "paragraph_provenance.json"
        if vizinho.is_file():
            try:
                prov = json.loads(vizinho.read_text(encoding="utf-8"))
            except (ValueError, OSError):
                prov = {}
        rascunhos += 1
        casos += 1
        laudo = validar_redacao(prov, texto)
        if laudo["gates"][GATE_VOZ] != "pass":
            reprovados.append(arquivo)
            print(f"  TRAVOU O APROVADO: {arquivo}")
            for item in laudo["findings"]:
                if item["sev"] == "P0":
                    print(f"      {item['gate']}: {item['problema'][:140]}")
            falhas += 1
        if laudo["gates"][GATE_ENTIDADES] == "fail":
            print(f"  TRAVOU O APROVADO (entidades): {arquivo}")
            falhas += 1

    if rascunhos < 6:
        print(f"  FALHOU: só {rascunhos} rascunhos reais examinados — a contraprova "
              "perdeu o acervo")
        falhas += 1

    if falhas:
        print(f"REGRESSÃO: {falhas} de {casos} verificações de redação falharam")
        return 1
    print(f"ok: {casos} verificações — os {rascunhos} rascunhos reais passam nos detectores "
          "que até agora só rodavam na F7-B")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
