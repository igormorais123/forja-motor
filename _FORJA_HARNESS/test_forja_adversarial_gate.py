# -*- coding: utf-8 -*-
"""test_forja_adversarial_gate.py — regressão da família adversarial e de replay.

Duas armadilhas de método ficaram registradas aqui:

  1. A contraprova precisa **parear auditoria e estratégia do MESMO caso**. O
     primeiro diagnóstico juntou a auditoria de um caso com a estratégia achada
     por varredura, e produziu três `fail` de `auditSha256` que não existiam.
     Pareado por caso, o acervo inteiro sai limpo.
  2. `excerptMatches: []` é ambíguo — "nada a conferir" ou "nada encontrado" —
     e o artefato não distingue. `warn`, nunca `fail`: a leitura pessimista
     reprovaria toda fonte citada sem transcrição, que é a maioria.

Uso: python test_forja_adversarial_gate.py   (exit 0 = ok; exit 1 = regressão)
"""
from __future__ import annotations

import hashlib
import io
import json
import sys
import tempfile
from datetime import date
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from forja_adversarial_gate import (  # noqa: E402
    GATE_AUDITORIA, GATE_DECISOES, GATE_ESCOPO, GATE_LIBERACAO, GATE_MA_FE,
    validar_auditoria_adversarial, validar_politica_liberacao)
from forja_replay import (  # noqa: E402
    GATE_COBERTURA, GATE_EXCERTO, GATE_REPLAY, validar_replay)

AUDITORIA_OK = {"applicable": True,
                "scope": {"fullReadingConfirmed": True, "pagesOrSectionsCovered": ["I", "II"]},
                "factualClaims": [{"id": "A1"}], "contradictions": [{"id": "C1"}],
                "citationInventory": [{"id": "CIT1"}], "decisivePoints": ["p"],
                "researchLog": ["l"], "badFaithIndicators": []}
ESTRATEGIA_OK = {"applicable": True, "badFaithDecision": {"impute": False},
                 "decisions": [{"findingId": "C1", "decision": "subsidiary",
                                "rationale": "altera a matriz prescricional"}]}
HOJE = date(2026, 8, 4)


def main() -> int:
    falhas = 0
    casos = 0

    def checar(nome, obtido, esperado):
        nonlocal falhas, casos
        casos += 1
        if obtido != esperado:
            print(f"  FALHOU: {nome} — esperado {esperado}, obtido {obtido}")
            falhas += 1

    def g(a, e, gate, caminho=None):
        return validar_auditoria_adversarial(a, e, caminho)["gates"][gate]

    checar("auditoria ausente", g(None, ESTRATEGIA_OK, GATE_ESCOPO), "fail")
    checar("aplicabilidade não declarada",
           g({"factualClaims": [{"id": "A1"}]}, ESTRATEGIA_OK, GATE_ESCOPO), "fail")
    checar("inaplicável sem motivo", g({"applicable": False}, {}, GATE_ESCOPO), "warn")
    checar("inaplicável com motivo",
           g({"applicable": False, "notApplicableReason": "não há peça adversária"},
             {"applicable": False, "reason": "idem"}, GATE_ESCOPO), "pass")
    checar("inaplicável não vira aprovação na auditoria",
           g({"applicable": False, "notApplicableReason": "não há peça adversária"},
             {"applicable": False, "reason": "idem"}, GATE_AUDITORIA), "not_applicable")
    checar("aplicável sem registro do que foi lido",
           g({**AUDITORIA_OK, "scope": {}}, ESTRATEGIA_OK, GATE_ESCOPO), "warn")
    checar("aplicável sem substância alguma",
           g({"applicable": True, "scope": {"fullReadingConfirmed": True}}, ESTRATEGIA_OK,
             GATE_AUDITORIA), "fail")
    checar("auditoria completa", g(AUDITORIA_OK, ESTRATEGIA_OK, GATE_AUDITORIA), "pass")

    checar("estratégia ausente", g(AUDITORIA_OK, None, GATE_DECISOES), "fail")
    checar("aplicável sem nenhuma decisão",
           g(AUDITORIA_OK, {"applicable": True, "decisions": []}, GATE_DECISOES), "fail")
    checar("decisão sem razão",
           g(AUDITORIA_OK, {"applicable": True, "badFaithDecision": {"impute": False},
                            "decisions": [{"findingId": "C1", "decision": "usar"}]},
             GATE_DECISOES), "warn")
    checar("decisões registradas", g(AUDITORIA_OK, ESTRATEGIA_OK, GATE_DECISOES), "pass")

    # A estratégia decide sobre ESTA auditoria?
    temp = Path(tempfile.mkdtemp(prefix="forja_adv_"))
    arquivo = temp / "adversarial_audit.json"
    arquivo.write_text(json.dumps(AUDITORIA_OK, ensure_ascii=False), encoding="utf-8")
    digest = hashlib.sha256(arquivo.read_bytes()).hexdigest()
    checar("estratégia aponta para outra auditoria",
           g(AUDITORIA_OK, {**ESTRATEGIA_OK, "auditSha256": "0" * 64}, GATE_DECISOES, arquivo),
           "fail")
    checar("estratégia aponta para esta auditoria",
           g(AUDITORIA_OK, {**ESTRATEGIA_OK, "auditSha256": digest}, GATE_DECISOES, arquivo),
           "pass")

    checar("indicador de má-fé sem decisão que o autorize",
           g({**AUDITORIA_OK, "badFaithIndicators": ["omissão deliberada de documento"]},
             {"applicable": True, "decisions": ESTRATEGIA_OK["decisions"]}, GATE_MA_FE), "fail")
    checar("indicador de má-fé com decisão registrada",
           g({**AUDITORIA_OK, "badFaithIndicators": ["omissão deliberada"]}, ESTRATEGIA_OK,
             GATE_MA_FE), "pass")

    # release_policy_satisfied
    def lib(m, gr=None):
        return validar_politica_liberacao(m, gr)["gates"][GATE_LIBERACAO]

    checar("pacote sem entregável", lib({"deliverables": []}), "fail")
    checar("pacote protocolável sobre F7 que negou liberação",
           lib({"deliverables": [{"id": "p", "releasePolicy": "strict_protocol"}]},
               {"approvedForExternalRelease": False}), "fail")
    checar("pacote interno sobre F7 que negou liberação",
           lib({"deliverables": [{"id": "p", "releasePolicy": "internal_review_only"}]},
               {"approvedForExternalRelease": False}), "pass")
    checar("entregável sem política declarada",
           lib({"deliverables": [{"id": "p"}]}, {"approvedForExternalRelease": True}), "warn")

    # --- replay --------------------------------------------------------------
    def r(dados, gate):
        return validar_replay(dados, hoje=HOJE)["gates"][gate]

    LEDGER = {"entries": [{"id": "S1", "claim": "REsp 1", "finalUseAllowed": True}],
              "liveReplay": {"S1": {"ok": True, "status": 200,
                                    "capturedAt": "2026-08-03T22:00:00",
                                    "excerptMatches": [{"factId": "F1", "matched": True}]}}}
    checar("ledger ausente", r(None, GATE_REPLAY), "fail")
    checar("ledger sem fontes", r({"entries": []}, GATE_COBERTURA), "fail")
    checar("fonte sem identidade",
           r({"entries": [{"finalUseAllowed": True}]}, GATE_COBERTURA), "fail")
    checar("replay que falhou",
           r({**LEDGER, "liveReplay": {"S1": {"ok": False, "status": 503}}}, GATE_REPLAY), "fail")
    checar("replay envelhecido",
           r({**LEDGER, "liveReplay": {"S1": {"ok": True, "status": 200,
                                              "capturedAt": "2026-01-01T00:00:00"}}},
             GATE_REPLAY), "warn")
    checar("replay recente", r(LEDGER, GATE_REPLAY), "pass")
    checar("excerto reencontrado", r(LEDGER, GATE_EXCERTO), "pass")
    checar("excerto explicitamente não encontrado",
           r({**LEDGER, "liveReplay": {"S1": {"ok": True, "status": 200,
                                              "capturedAt": "2026-08-03T22:00:00",
                                              "excerptMatches": [{"factId": "F1",
                                                                  "matched": False}]}}},
             GATE_EXCERTO), "fail")
    # A ambiguidade: lista vazia não pode reprovar.
    checar("nenhum casamento registrado",
           r({**LEDGER, "liveReplay": {"S1": {"ok": True, "status": 200,
                                              "capturedAt": "2026-08-03T22:00:00",
                                              "excerptMatches": []}}}, GATE_EXCERTO), "warn")

    # CONTRAPROVA — auditoria e estratégia PAREADAS POR CASO.
    pares, vereditos = 0, []
    for caso in sorted(Path("state").glob("case-*")):
        a_p = caso / "n3_artifacts" / "F3_FONTES_REGIMENTO_LEIS" / "adversarial_audit.json"
        e_p = caso / "n3_artifacts" / "F4_BLUEPRINT_ESTRATEGICO" / "adversarial_strategy.json"
        if not a_p.is_file():
            continue
        try:
            auditoria = json.loads(a_p.read_text(encoding="utf-8"))
            estrategia = json.loads(e_p.read_text(encoding="utf-8")) if e_p.is_file() else {}
        except (ValueError, OSError):
            continue
        pares += 1
        casos += 1
        laudo = validar_auditoria_adversarial(auditoria, estrategia, a_p)
        vereditos.extend(laudo["gates"].values())
        reprovados = [n for n, v in laudo["gates"].items() if v == "fail"]
        if reprovados:
            print(f"  TRAVOU O APROVADO: {caso.name} em {', '.join(reprovados)}")
            for item in laudo["findings"]:
                if item["sev"] == "P0":
                    print(f"      {item['gate']}: {item['problema'][:130]}")
            falhas += 1

    if pares < 4:
        print(f"  FALHOU: só {pares} pares auditoria/estratégia reais examinados")
        falhas += 1

    reais = 0
    for arquivo in Path("state").rglob("verified_source_ledger.json"):
        try:
            dados = json.loads(arquivo.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            continue
        if not isinstance(dados, dict):
            continue
        reais += 1
        casos += 1
        laudo = validar_replay(dados, hoje=HOJE)
        if "fail" in laudo["gates"].values():
            print(f"  TRAVOU O APROVADO (replay): {arquivo}")
            falhas += 1

    if falhas:
        print(f"REGRESSÃO: {falhas} de {casos} verificações adversariais/replay falharam")
        return 1
    print(f"ok: {casos} verificações — {pares} pares reais pareados por caso e {reais} ledgers "
          f"verificados, nenhum reprovado; vereditos do acervo: "
          f"{', '.join(sorted(set(vereditos)))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
