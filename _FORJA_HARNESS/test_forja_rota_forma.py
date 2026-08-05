# -*- coding: utf-8 -*-
"""test_forja_rota_forma.py — a ROTA DE PRODUÇÃO lê o artefato na forma real?

O censo (`forja_recomputo_censo.py`) é instrumento de medida. Quem roda quando
uma fase é promovida de verdade é `forja_run._validate_result`, e são coisas
diferentes: em 04/08/2026 eu corrigi cinco gates para lerem markdown no CENSO e
por um momento acreditei ter consertado a esteira. Tinha consertado o termômetro.

Na rota de produção sobravam duas cegueiras, e a segunda era pior que cega:

  - `reconciliation_report` em markdown era descartado de propósito, e como
    `forja_reconcile.py` SEMPRE emitiu markdown, `status_consistent` nunca disse
    `pass` em nenhuma execução da história do harness;
  - `citation_checklist` em markdown ia para o parser JSON, virava `{}`, e o
    gate lia isso como "checklist ausente" — BLOQUEANDO uma F5 correta por causa
    da extensão do arquivo. Reprovar trabalho bom é o defeito mais caro que um
    gate tem.

Este teste não simula a fase inteira: ele confere que cada leitura de artefato
da rota de produção passa pelo leitor tolerante a forma, e que os produtores
aceitam o que ele devolve. É teste de fiação, não de comportamento — e é a
fiação que estava errada.

Uso: python test_forja_rota_forma.py   (exit 0 = ok; exit 1 = regressão)
"""
from __future__ import annotations

import io
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

RAIZ = Path(__file__).resolve().parent

# Artefatos que existem em markdown no acervo e alimentam gate computado.
# A fonte desta lista é o censo de formas; se um artefato novo passar a existir
# em duas formas, `test_forja_forma_artefatos.py` avisa antes deste aqui.
ARTEFATOS_BIFORMES = ("reconciliation_report", "citation_checklist", "sources_map",
                      "fact_ledger", "blueprint")


def main() -> int:
    falhas = 0
    casos = 0
    fonte = (RAIZ / "forja_run.py").read_text(encoding="utf-8")

    # 1. Nenhum artefato biforme pode ir direto ao parser JSON na rota.
    for artefato in ARTEFATOS_BIFORMES:
        casos += 1
        direto = re.search(
            rf'read_json\(\s*{artefato}_path|read_json\(\s*por_id\.get\("{artefato}"\)', fonte)
        if direto:
            print(f"  FALHOU: a rota de produção manda `{artefato}` direto ao parser JSON — "
                  "a forma markdown vira `{}` e o gate lê ausência onde há artefato")
            falhas += 1

    # 2. O leitor tolerante existe e trata markdown como texto, não como vazio.
    casos += 1
    from forja_run import _read_gate_artifact
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        md = Path(tmp) / "x.md"
        md.write_text("# Título\n\nconteúdo real\n", encoding="utf-8")
        lido = _read_gate_artifact(md)
        if not isinstance(lido, str) or "conteúdo real" not in lido:
            print("  FALHOU: _read_gate_artifact não devolve o texto do markdown")
            falhas += 1

    # 3. Os produtores aceitam a string que o leitor entrega — sem isso, ler o
    #    markdown só troca "vazio" por "tipo errado".
    from forja_entrega import GATE_STATUS, validar_reconciliacao
    from forja_fontes_oficiais import GATE_COTEJO, validar_cotejo_citacoes
    from forja_produto import GATE_PERGUNTA, validar_pergunta_jurisdicional
    from forja_regimento_gate import GATE_FATOS, GATE_REGIMENTO, validar_regimento

    MANIFESTO = {"caseFolder": str(RAIZ), "commandFile": str(RAIZ / "forja_run.py"),
                 "caseId": "c", "demandId": "d"}
    provas = [
        ("reconciliation_report",
         lambda: validar_reconciliacao(
             MANIFESTO,
             "# R\n\n## Status\n- Nenhuma inconsistência detectada.\n")["gates"][GATE_STATUS],
         "pass"),
        ("citation_checklist",
         lambda: validar_cotejo_citacoes(
             "# C\n\n- [x] O parecer usará paráfrases fiéis, sem transcrição literal.\n"
         )["gates"][GATE_COTEJO], "not_applicable"),
        ("blueprint",
         lambda: validar_pergunta_jurisdicional(
             "# B\n\n## Pergunta central\n\nO crédito permanece exigível em 2026, dada a "
             "negativa de 2019?\n")["gates"][GATE_PERGUNTA], "pass"),
        ("sources_map",
         lambda: validar_regimento(
             "# Mapa\n\n- Regimento Interno do TRF4, consolidação oficial até o Assento "
             "Regimental nº 37/2026.\n")["gates"][GATE_REGIMENTO], "warn"),
        ("fact_ledger",
         lambda: validar_regimento(
             "# Mapa\n\n- Regimento Interno do TRF4.\n",
             "| ID | Proposição | Estatuto | Fonte | Limite |\n|---|---|---|---|---|\n"
             "| SRC-E718 | A magistrada indeferiu | `[FONTE: autos]` | Evento 718, pp. 1-2 | - |\n"
         )["gates"][GATE_FATOS], "pass"),
    ]
    for nome, chamada, esperado in provas:
        casos += 1
        try:
            obtido = chamada()
        except Exception as erro:  # noqa: BLE001
            print(f"  FALHOU: o produtor de `{nome}` estourou com markdown: "
                  f"{type(erro).__name__}: {erro}")
            falhas += 1
            continue
        if obtido != esperado:
            print(f"  FALHOU: `{nome}` em markdown deu {obtido}, esperado {esperado}")
            falhas += 1

    if falhas:
        print(f"REGRESSÃO: {falhas} de {casos} verificações de fiação falharam")
        return 1
    print(f"ok: {casos} verificações — a rota de produção lê os {len(ARTEFATOS_BIFORMES)} "
          "artefatos biformes na forma em que eles existem")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
