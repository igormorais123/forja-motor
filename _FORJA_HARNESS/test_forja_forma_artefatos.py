# -*- coding: utf-8 -*-
"""test_forja_forma_artefatos.py — catraca contra a cegueira de forma.

Em 04/08/2026, cinco gates falharam pelo mesmo motivo em uma tarde, e nenhum
deles por causa do nome de um campo: `status_consistent`, `quotes_compared`,
`jurisdictional_question_defined`, `regimento_available` e
`critical_facts_sourced` liam apenas a forma JSON de artefatos que o acervo
mantém em markdown.

Essa falha não produz erro, exceção nem achado. Produz um `warn` educado, ou um
veredito que simplesmente não aparece — e o operador lê "sem achados" e entende
"conferido". É a MC-15 pela porta dos fundos: em vez de um conjunto vazio, um
arquivo que ninguém abriu.

A catraca é direta: nenhuma cegueira de forma pode existir. Se um leitor abre
`x.json` e o acervo também tem `x.md`, ou ele passa a ler os dois, ou alguém
decide por escrito que a outra forma não é artefato — e aí ela entra na lista de
ignorados do módulo, com o motivo.

Uso: python test_forja_forma_artefatos.py   (exit 0 = ok; exit 1 = regressão)
"""
from __future__ import annotations

import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from forja_forma_artefatos import censo_de_formas  # noqa: E402

# Medido em 04/08/2026, depois de fechar as cinco cegueiras. Só pode cair.
CEGUEIRAS_MAX = 0
RADICAIS_MIN = 3000


def main() -> int:
    falhas = 0
    laudo = censo_de_formas()

    if laudo["radicaisExaminados"] < RADICAIS_MIN:
        print(f"  FALHOU: só {laudo['radicaisExaminados']} radicais examinados, abaixo do piso "
              f"de {RADICAIS_MIN} — a catraca ficaria verde por falta de material")
        falhas += 1

    cegueiras = laudo["cegueirasDeForma"]
    if len(cegueiras) > CEGUEIRAS_MAX:
        print(f"  FALHOU: {len(cegueiras)} artefato(s) existem numa forma que o leitor não abre:")
        for item in cegueiras:
            print(f"      {item['artefato']}: lê {','.join(item['lidas'])}, "
                  f"ignora {','.join(item['ignoradas'])} "
                  f"({item['arquivosIgnorados']} arquivo(s) invisíveis)")
        falhas += 1

    if falhas:
        print(f"REGRESSÃO: {falhas} verificação(ões) de forma falharam")
        return 1
    print(f"ok: {laudo['radicaisExaminados']} radicais; "
          f"{len(laudo['radicaisEmMaisDeUmaForma'])} existem em mais de uma forma e o leitor "
          "alcança todas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
