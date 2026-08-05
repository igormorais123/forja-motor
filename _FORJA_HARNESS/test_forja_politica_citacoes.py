# -*- coding: utf-8 -*-
"""test_forja_politica_citacoes.py — o gate de política de citação sabe dizer não.

`citations_policy_satisfied` era o gate de maior volume da esteira e o mais caro
se falso: onze execuções, onze `pass`, nenhuma reprovação, todas escritas pelo
próprio agente da fase. "Jurisprudência com atribuição errada" é o erro
recorrente nº 1 das entregas reais desta fábrica.

A política computada é de COBERTURA e LIBERAÇÃO: toda autoridade citada no texto
final precisa existir no ledger de fontes verificadas, e nenhuma pode ser usada
com `finalUseAllowed` diferente de true. Fidelidade à tese do precedente — ratio
ou dictum, superado ou vigente — segue sendo trabalho humano do F7.

Três listas, e a terceira é a que mais importa:

  DEVE_REPROVAR      — citação não conferida, uso bloqueado, ledger ausente.
  NAO_PODE_TRAVAR    — peça sem citação; citação devidamente liberada.
  NAO_PODE_MENTIR    — ledger de esquema que não permite conferir devolve `warn`,
                       nunca `pass`. Silêncio não pode significar auditado, e
                       este gate nasceu justamente para não repetir a MC-15.

Uso: python test_forja_politica_citacoes.py   (exit 0 = ok; exit 1 = regressão)
"""
from __future__ import annotations

import io
import json
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from forja_citations import validar_politica_citacoes  # noqa: E402

TEXTO = "Conforme o AgInt no AREsp 2.698.443/DF e a Súmula 7 do STJ, o recurso não prospera."

LIBERADAS = {"entries": [
    {"authorityIdentity": {"court": "STJ", "kind": "ARESP", "number": "2698443"},
     "finalUseAllowed": True},
    {"authorityIdentity": {"court": "STJ", "kind": "SUMULA", "number": "7"},
     "finalUseAllowed": True},
]}


def _veredito(texto, ledger):
    return validar_politica_citacoes(texto, ledger)["gates"]["citations_policy_satisfied"]


def main() -> int:
    falhas = 0
    casos = 0

    # NÃO PODE TRAVAR
    casos += 1
    if _veredito(TEXTO, LIBERADAS) != "pass":
        print("  FALHOU: citações devidamente liberadas foram travadas")
        falhas += 1

    casos += 1
    if _veredito("Manifestação processual sem qualquer autoridade citada.", {}) != "pass":
        print("  FALHOU: peça sem citação foi cobrada de ledger")
        falhas += 1

    # DEVE REPROVAR
    casos += 1
    parcial = {"entries": [LIBERADAS["entries"][1]]}
    if _veredito(TEXTO, parcial) != "fail":
        print("  FALHOU: autoridade citada e ausente do ledger não reprovou")
        falhas += 1

    casos += 1
    bloqueada = {"entries": [dict(LIBERADAS["entries"][0], finalUseAllowed=False),
                             LIBERADAS["entries"][1]]}
    if _veredito(TEXTO, bloqueada) != "fail":
        print("  FALHOU: autoridade com finalUseAllowed=false foi usada sem reprovar")
        falhas += 1

    # Ausência do campo é ausência de liberação, não liberação tácita.
    casos += 1
    sem_campo = {"entries": [{"authorityIdentity": {"court": "STJ", "kind": "ARESP",
                                                    "number": "2698443"}},
                             LIBERADAS["entries"][1]]}
    if _veredito(TEXTO, sem_campo) != "fail":
        print("  FALHOU: entrada sem finalUseAllowed foi tratada como liberada")
        falhas += 1

    # NÃO PODE MENTIR — esquema que não permite conferir devolve warn.
    casos += 1
    outro_esquema = {"processSources": ["evento 228", "evento 239"]}
    if _veredito(TEXTO, outro_esquema) != "warn":
        print("  FALHOU: ledger não conferível deveria devolver warn, não pass nem fail")
        falhas += 1

    # O segundo esquema real do acervo É conferível: identidade sai do
    # `identifier` pelo mesmo extrator usado no texto.
    casos += 1
    oficial = {"officialSources": [
        {"identifier": "AREsp 2.698.443/DF", "archivedSha256": "abc", "status": "official_copy_archived"},
        {"identifier": "Súmula 7 do STJ", "archivedSha256": "def", "status": "official_copy_archived"},
    ]}
    if _veredito(TEXTO, oficial) != "pass":
        print("  FALHOU: ledger em officialSources com cópia arquivada não foi reconhecido")
        falhas += 1

    casos += 1
    sem_copia = {"officialSources": [
        {"identifier": "AREsp 2.698.443/DF", "status": "pendente"},
        {"identifier": "Súmula 7 do STJ", "archivedSha256": "def"},
    ]}
    if _veredito(TEXTO, sem_copia) != "fail":
        print("  FALHOU: officialSources sem cópia arquivada foi tratado como conferido")
        falhas += 1

    # CONTRA O ACERVO REAL — o gate precisa produzir vereditos distintos e por
    # motivos distintos nas peças de verdade, senão é decorativo.
    vistos = {}
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
        veredito = _veredito(final.read_text(encoding="utf-8", errors="replace"), ledger)
        vistos[veredito] = vistos.get(veredito, 0) + 1

    casos += 1
    if len(vistos) < 2:
        print(f"  FALHOU: no acervo real o gate devolveu sempre o mesmo veredito ({vistos}) — "
              "gate que nunca varia não está medindo nada")
        falhas += 1

    if falhas:
        print(f"REGRESSÃO: {falhas} de {casos} verificações da política de citação falharam")
        return 1
    print(f"ok: {casos} verificações — reprova citação não conferida e uso bloqueado, "
          f"não trava citação liberada nem peça sem citação, e devolve warn onde não pode "
          f"conferir; no acervo real produz {vistos}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
