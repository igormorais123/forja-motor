# -*- coding: utf-8 -*-
"""test_forja_identidade_citacoes.py — CNJ manda, rótulo é hipótese.

Âncora real: o P0 mais grave do caso Vale Trading foi afirmar que um agravo
"envolve as mesmas partes e a mesma liquidação" quando os números CNJ apontavam
para liquidações distintas. O protocolo da casa manda identificar o tribunal
pelo número CNJ antes de qualquer coisa, e até 04/08/2026 o gate que atesta isso
era escrito pelo próprio agente da fase.

Duas listas, e a segunda é a que impede o gate de virar ruído:

  DEVE_REPROVAR   — CNJ cujo segmento contradiz o tribunal nomeado ao lado.
  NAO_PODE_TRAVAR — CNJ coerente; recurso que subiu ao STJ (o tribunal superior
                    aparece legitimamente perto de um CNJ de origem); artigo de
                    lei, que não tem tribunal; e as peças REAIS do acervo.

Uso: python test_forja_identidade_citacoes.py   (exit 0 = ok; exit 1 = regressão)
"""
from __future__ import annotations

import io
import json
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from forja_citations import validar_identidade_citacoes  # noqa: E402

GATE = "citation_identity_and_cnj_tribunal_resolved"

DEVE_REPROVAR = [
    ("CNJ do TRF4 atribuído ao TJSP",
     "Nos autos 5020376-80.2018.4.04.7100, em trâmite no TJSP, a decisão foi mantida."),
    ("CNJ do TRF1 atribuído ao TRF4",
     "O feito 0003453-28.1997.4.01.3400 tramita no TRF4 desde a distribuição."),
    ("CNJ do TJTO atribuído ao TJSP",
     "A apelação 1234567-89.2020.8.27.0100 foi julgada pelo TJSP em composição plena."),
]

NAO_PODE_TRAVAR = [
    ("CNJ coerente com o tribunal nomeado",
     "Nos autos 5020376-80.2018.4.04.7100, do TRF4, a decisão foi mantida."),
    # O tribunal superior aparece legitimamente ao lado de um CNJ de origem:
    # o recurso sobe. Tratar isso como contradição reprovaria toda peça de
    # recurso especial da casa.
    ("recurso que subiu ao STJ",
     "O REsp interposto nos autos 5020376-80.2018.4.04.7100 subiu ao STJ."),
    ("STF perto do CNJ de origem",
     "O ARE oriundo do processo 1234567-89.2020.8.26.0100 aguarda juízo no STF."),
    # Norma não tem tribunal. A primeira versão do gate cobrou corte de três
    # artigos do CPC numa peça correta; ruído ensina a ignorar o gate.
    ("artigo de lei não tem tribunal",
     "Nos termos do art. 203 do CPC e do art. 678 do CPC, o ato é ordinatório."),
    ("dois CNJ distintos sem afirmar identidade",
     "A liquidação 5020376-80.2018.4.04.7100 e a liquidação 5072582-42.2016.4.04.7100 "
     "correm ambas no TRF4 e não se confundem."),
    ("peça sem citação alguma",
     "Manifestação processual sem autoridade citada."),
]


def _veredito(texto, ledger=None):
    return validar_identidade_citacoes(texto, ledger)["gates"][GATE]


def main() -> int:
    falhas = 0
    casos = 0

    for nome, texto in DEVE_REPROVAR:
        casos += 1
        if _veredito(texto) != "fail":
            print(f"  FALHOU (não pegou): {nome}")
            falhas += 1

    for nome, texto in NAO_PODE_TRAVAR:
        casos += 1
        if _veredito(texto) != "pass":
            print(f"  TRAVOU INDEVIDAMENTE: {nome}")
            falhas += 1

    # Corte ambígua é P1: ambiguidade de redação não é afirmação falsa.
    casos += 1
    laudo = validar_identidade_citacoes("Aplica-se o Tema 1368 ao caso.")
    if laudo["gates"][GATE] != "pass" or not any(
            item["gate"] == "LI2-corte-ambigua" for item in laudo["findings"]):
        print("  FALHOU: Tema sem tribunal deveria gerar P1 sem bloquear")
        falhas += 1

    # E o ledger que resolve a corte silencia o P1 — senão o gate cobraria no
    # texto o que já está resolvido no lugar próprio.
    casos += 1
    resolvido = {"entries": [{"authorityIdentity": {"court": "STJ", "kind": "TEMA",
                                                    "number": "1368"},
                              "finalUseAllowed": True}]}
    if validar_identidade_citacoes("Aplica-se o Tema 1368 ao caso.", resolvido)["findings"]:
        print("  FALHOU: corte resolvida no ledger continuou sendo cobrada no texto")
        falhas += 1

    # CONTRA O ACERVO REAL — nenhuma peça aprovada pode reprovar em P0.
    reais = 0
    for pr in sorted(Path("state").rglob("PHASE_RESULT.json")):
        try:
            dados = json.loads(pr.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            continue
        if dados.get("phase") != "F7_AUDITORIA_JURIDICA_FACTUAL":
            continue
        por_id = {a["id"]: pr.parent / a["path"] for a in dados.get("artifacts") or []
                  if isinstance(a, dict) and a.get("path")}
        final, ledger_path = por_id.get("final_markdown"), por_id.get("verified_source_ledger")
        if not final or not final.is_file():
            continue
        ledger = {}
        if ledger_path and ledger_path.is_file():
            try:
                ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
            except Exception:  # noqa: BLE001
                ledger = {}
        reais += 1
        casos += 1
        if _veredito(final.read_text(encoding="utf-8", errors="replace"), ledger) != "pass":
            print(f"  TRAVOU O APROVADO: {pr.parent.parent.parent.name}")
            falhas += 1

    if reais < 4:
        print(f"  FALHOU: só {reais} peças reais examinadas — a contraprova perdeu o acervo")
        falhas += 1

    if falhas:
        print(f"REGRESSÃO: {falhas} de {casos} verificações de identidade falharam")
        return 1
    print(f"ok: {casos} verificações — reprova os 3 desencontros CNJ×tribunal, não trava "
          f"recurso que sobe, norma sem tribunal nem as {reais} peças reais do acervo")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
