# -*- coding: utf-8 -*-
"""test_forja_regimento_gate.py — regressão dos gates da F3.

A distinção que este teste protege: hash divergente de **cópia arquivada** é P0
(o arquivo deveria estar congelado), hash divergente de **regimento** é `warn`
(o protocolo manda atualizá-lo com as emendas posteriores antes de cada peça).
Confundir as duas coisas reprovaria quem cumpriu a regra inviolável da casa —
foi exatamente o que o caso Natura fez, atualizando o .md em 26/07 depois da F3
de 15/07.

Uso: python test_forja_regimento_gate.py   (exit 0 = ok; exit 1 = regressão)
"""
from __future__ import annotations

import hashlib
import io
import json
import sys
import tempfile
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from forja_regimento_gate import (  # noqa: E402
    GATE_FATOS, GATE_REGIMENTO, GATE_TRIBUNAL, validar_regimento)

LEDGER_OK = {"facts": [{"id": "F1", "claim": "algo", "status": "confirmed_document",
                        "support": ["E228"]},
                       {"id": "F2", "claim": "outra coisa", "status": "blocked"}]}


def main() -> int:
    falhas = 0
    casos = 0
    temp = Path(tempfile.mkdtemp(prefix="forja_regimento_"))
    reg = temp / "REGIMENTO_INTERNO_TJSP.md"
    reg.write_text("# Regimento\n\nArt. 1º ...\n\n## Emendas posteriores\n\nConferido em 2026-08-04.\n",
                   encoding="utf-8")
    digest = hashlib.sha256(reg.read_bytes()).hexdigest()
    BASE = {"tribunal": {"name": "TJSP", "basis": "endereçamento e CNJ 8.26"},
            "regimento": {"path": str(reg), "sha256": digest}}

    def checar(nome, obtido, esperado):
        nonlocal falhas, casos
        casos += 1
        if obtido != esperado:
            print(f"  FALHOU: {nome} — esperado {esperado}, obtido {obtido}")
            falhas += 1

    def g(mapa, gate, ledger=LEDGER_OK):
        return validar_regimento(mapa, ledger)["gates"][gate]

    checar("mapa ausente", g(None, GATE_REGIMENTO), "fail")
    checar("tribunal não identificado",
           g({"regimento": {"path": str(reg)}}, GATE_TRIBUNAL), "fail")
    checar("tribunal sem base da identificação",
           g({**BASE, "tribunal": {"name": "TJSP"}}, GATE_TRIBUNAL), "warn")
    checar("tribunal com base", g(BASE, GATE_TRIBUNAL), "pass")

    checar("regimento não declarado",
           g({"tribunal": {"name": "TJSP", "basis": "x"}}, GATE_REGIMENTO), "fail")
    checar("regimento declarado que não existe",
           g({**BASE, "regimento": {"path": str(temp / "nao_existe.md")}}, GATE_REGIMENTO), "fail")
    checar("regimento íntegro", g(BASE, GATE_REGIMENTO), "pass")
    # A distinção que importa: aqui divergir é o protocolo funcionando.
    checar("hash do regimento mudou desde a F3",
           g({**BASE, "regimento": {"path": str(reg), "sha256": "0" * 64}}, GATE_REGIMENTO),
           "warn")

    sem_emendas = temp / "REGIMENTO_INTERNO_TRF9.md"
    sem_emendas.write_text("# Regimento\n\nArt. 1º ...\n", encoding="utf-8")
    checar("regimento sem seção de emendas posteriores",
           g({**BASE, "regimento": {"path": str(sem_emendas)}}, GATE_REGIMENTO), "warn")

    checar("ledger sem fatos", g(BASE, GATE_FATOS, {"facts": []}), "fail")
    checar("fato afirmado sem lastro",
           g(BASE, GATE_FATOS,
             {"facts": [{"id": "F1", "claim": "algo", "status": "confirmed_document"}]}), "fail")
    checar("fato bloqueado não precisa de lastro",
           g(BASE, GATE_FATOS, {"facts": [{"id": "F1", "status": "blocked"}]}), "pass")
    checar("fatos lastreados", g(BASE, GATE_FATOS), "pass")
    checar("sourceIds são lastro documental",
           g(BASE, GATE_FATOS,
             {"facts": [{"factId": "F1", "epistemicClass": "documented",
                         "sourceIds": ["DOC-001"]}]}), "pass")

    # A forma MARKDOWN dos dois artefatos da F3. O mapa do Vale Trading e o
    # ledger do Nylton só existem assim, e enquanto o gate só abria JSON ele
    # reportava "ledger sem fatos" sobre um ledger de nove fatos com localizador
    # processual em cada linha — achado que chegou a entrar num laudo de triagem
    # como defeito do caso.
    MAPA_MD = ("# Mapa de fontes\n\n## Fontes processuais\n- Evento 228: parte 8, p. 1117.\n\n"
               "## Fontes normativas\n"
               "- Regimento Interno do TRF4, consolidação oficial até o Assento Regimental "
               "nº 37/2026, baixada em 23/07/2026.\n")
    LEDGER_MD = ("# Ledger de fatos\n\n"
                 "| ID | Proposição | Estatuto | Fonte/localizador | Limite |\n"
                 "|---|---|---|---|---|\n"
                 "| SRC-E718 | A magistrada indeferiu a impenhorabilidade | `[FONTE: autos]` | "
                 "Evento 718, DESPADEC1, pp. 1-2 | não examina os efeitos da sentença |\n"
                 "| SRC-E735 | A intimação está aberta de 20 a 24/07/2026 | `[FONTE: autos]` | "
                 "Evento 735; PDF parte 10, pp. 83-84 | o prazo interno é mais conservador |\n")
    md = validar_regimento(MAPA_MD, LEDGER_MD)["gates"]
    checar("mapa em markdown identifica o tribunal", md[GATE_TRIBUNAL], "warn")
    checar("regimento em prosa não é regimento ausente", md[GATE_REGIMENTO], "warn")
    checar("tabela de fatos em markdown tem lastro", md[GATE_FATOS], "pass")
    # O afrouxamento é de FORMA, não de substância: markdown sem regimento algum
    # continua reprovado, senão bastaria escrever em markdown para escapar da
    # regra inviolável de 06/07.
    checar("markdown sem regimento continua reprovado",
           validar_regimento("# Mapa\n\n- Evento 228: parte 8.\n")[ "gates"][GATE_REGIMENTO],
           "fail")

    # CONTRAPROVA — os artefatos reais da F3. Nada pode reprovar por defeito meu.
    dialetos, vereditos = {}, []
    for arquivo in Path("state").rglob("sources_map.json"):
        try:
            mapa = json.loads(arquivo.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            continue
        if not isinstance(mapa, dict):
            continue
        chave = tuple(sorted(mapa))
        if chave in dialetos:
            continue
        dialetos[chave] = arquivo
        ledger = {}
        vizinho = arquivo.parent / "fact_ledger.json"
        if vizinho.is_file():
            try:
                ledger = json.loads(vizinho.read_text(encoding="utf-8"))
            except (ValueError, OSError):
                ledger = {}
        casos += 1
        laudo = validar_regimento(mapa, ledger)
        vereditos.append(laudo["gates"][GATE_REGIMENTO])
        if laudo["gates"][GATE_REGIMENTO] == "fail" and (
                mapa.get("regimento") or mapa.get("regiment")):
            print(f"  TRAVOU O APROVADO: {arquivo}")
            for item in laudo["findings"]:
                if item["sev"] == "P0":
                    print(f"      {item['gate']}: {item['problema'][:140]}")
            falhas += 1

    if len(dialetos) < 3:
        print(f"  FALHOU: só {len(dialetos)} mapas de fontes reais examinados")
        falhas += 1

    if falhas:
        print(f"REGRESSÃO: {falhas} de {casos} verificações de regimento falharam")
        return 1
    print(f"ok: {casos} verificações — {len(dialetos)} mapas reais; vereditos de regimento: "
          f"{', '.join(sorted(set(vereditos)))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
