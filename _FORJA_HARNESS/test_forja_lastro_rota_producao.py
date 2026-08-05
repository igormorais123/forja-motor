# -*- coding: utf-8 -*-
"""test_forja_lastro_rota_producao.py — o laudo de lastro nasce no disco?

A definição de pronto do Plano 41 exige que L1/L2/L7 estejam "comprovadamente
computados na rota de produção". Até 04/08/2026 essa prova existia apenas no
nível da função: a regressão chamava `_compute_lastro_gates` diretamente. Nada
provava que `_validate_result` — a rota real, que grava o laudo e sobrescreve o
gate declarado pelo agente — chegasse a executá-la.

A distinção não é acadêmica. Naquela manhã descobriu-se que o recomputo estava
inerte desde que nasceu: 7 fases F7 no acervo, zero `COMPUTED_LASTRO_GATES.json`.
O teste de função passava e a produção não auditava nada. Um teste que exercita a
função e não a rota tem exatamente esse ponto cego.

Os três casos abaixo montam uma tentativa que satisfaz o contrato F7 e verificam,
no disco:

1. o laudo é materializado quando a fase é validada;
2. o gate `fact_grounding_verbatim` declarado `pass` pelo agente NÃO sobrevive a
   um ledger sem transcrição — o recomputo derruba a promoção;
3. um fato devidamente transcrito passa, para que o gate não seja uma trava.

Uso: python test_forja_lastro_rota_producao.py   (exit 0 = ok; exit 1 = regressão)
"""
from __future__ import annotations

import io
import json
import sys
import tempfile
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from forja_phase_contracts import load_contract  # noqa: E402
from forja_run import _validate_result  # noqa: E402

FASE = "F7_AUDITORIA_JURIDICA_FACTUAL"


def _montar_tentativa(raiz: Path, ledger: dict, texto: str) -> Path:
    """Tentativa mínima que satisfaz o contrato F7, com ledger de fatos declarado."""
    contrato = load_contract(FASE)
    attempt = raiz / "case-x" / "runs" / "r1" / FASE / "attempt-1"
    attempt.mkdir(parents=True)

    artifacts = []
    for nome in contrato["requiredOutputs"]:
        arquivo = attempt / f"{nome}.json"
        arquivo.write_text("{}", encoding="utf-8")
        artifacts.append({"id": nome, "path": arquivo.name, "role": nome,
                          "audience": "internal_review", "releasePolicy": "requires_f8"})

    # O texto final é markdown de verdade; o recomputo o lê.
    final = attempt / "final_markdown.md"
    final.write_text(texto, encoding="utf-8")
    for item in artifacts:
        if item["id"] == "final_markdown":
            item["path"] = final.name

    # Desde 04/08/2026 a mesma rota recomputa o exame adversarial da F7. Uma
    # tentativa mínima precisa trazer red team enumerado e recheck com
    # aplicabilidade declarada — antes disso o `{}` de todos os artefatos
    # passava, e era esse o buraco.
    red = attempt / "red_team_report.md"
    red.write_text("\n".join(
        f"{i}. Objeção {i}: o adversário sustentaria X. Resposta: Y."
        for i in range(1, 10)), encoding="utf-8")
    recheck = {"applicable": False,
               "notApplicableReason": "manifestação sem peça adversária anterior nos autos"}
    (attempt / "adversarial_recheck.json").write_text(
        json.dumps(recheck, ensure_ascii=False), encoding="utf-8")

    # E a mesma rota recomputa a validação de contexto: identidade processual
    # declarada, recheque declarado e nenhuma questão material pendente sobre
    # liberação externa aprovada.
    (attempt / "context_validation.json").write_text(json.dumps({
        "schemaVersion": 1, "factsRechecked": True, "tribunal": "TRF4",
        "proceduralIdentity": "manifestação em processo de teste",
        "approvedForExternalRelease": False, "pendingMaterialQuestions": [],
    }, ensure_ascii=False), encoding="utf-8")

    # E o resultado da F7 precisa declarar a contagem de P0, que desde a leva 12
    # é conferida contra a própria lista de achados em vez de aceita como dada.
    (attempt / "f7_gate_result.json").write_text(
        json.dumps({"schemaVersion": 1, "p0": 0, "p1": 0, "findings": []},
                   ensure_ascii=False), encoding="utf-8")

    # E o ledger de fontes verificadas, que desde a leva 14 responde por
    # cobertura, reabertura ao vivo e casamento de excerto.
    (attempt / "verified_source_ledger.json").write_text(json.dumps({
        "schemaVersion": 1,
        "entries": [{"id": "SRC-CPC", "claim": "CPC, art. 203, § 4º",
                     "authorityIdentity": {"court": None, "kind": "ARTICLE", "number": "203"},
                     "finalUseAllowed": True, "status": "confirmed"}],
    }, ensure_ascii=False), encoding="utf-8")
    for item in artifacts:
        if item["id"] == "red_team_report":
            item["path"] = red.name

    # O ledger de fatos não está no contrato: é descoberto pela rota, como em
    # produção, onde a F3 o promove para n3_artifacts.
    promovido = raiz / "case-x" / "n3_artifacts" / "F3_FONTES_REGIMENTO_LEIS"
    promovido.mkdir(parents=True)
    (promovido / "fact_ledger.json").write_text(
        json.dumps(ledger, ensure_ascii=False), encoding="utf-8")

    resultado = {
        "schemaVersion": 1, "phase": FASE, "status": "pass",
        "producer": "produtor-teste", "reviewer": "revisor-teste",
        "producerRole": contrato["producerRole"], "reviewerRole": contrato["reviewerRole"],
        # O agente declara TODOS os gates como aprovados. É exatamente a
        # situação que o recomputo existe para não aceitar de graça.
        "gates": {nome: "pass" for nome in contrato["requiredGates"]},
        "artifacts": artifacts,
    }
    (attempt / "PHASE_RESULT.json").write_text(
        json.dumps(resultado, ensure_ascii=False), encoding="utf-8")
    (attempt / "RUN_CONTEXT.json").write_text(
        json.dumps({"phase": FASE, "inputs": {}}, ensure_ascii=False), encoding="utf-8")
    return attempt


def _validar(attempt: Path) -> tuple[dict | None, str | None]:
    try:
        resultado, _ = _validate_result(attempt, load_contract(FASE))
        return resultado, None
    except Exception as exc:  # noqa: BLE001 - o tipo do erro é o dado do teste
        return None, f"{type(exc).__name__}: {exc}"


SEM_TRANSCRICAO = {"facts": [{"id": "F-SEM", "status": "confirmed_document",
                              "support": ["fonte.md"]}]}
COM_TRANSCRICAO = {"facts": [{"id": "F-COM", "status": "confirmed_document",
                              "support": ["fonte.md"],
                              "quote": "Deverá apresentar dois cálculos de liquidação "
                                       "atualizados para o período indicado."}]}
TEXTO = "# Manifestação\n\nTexto sem material econômico, apenas processual.\n"


def main() -> int:
    falhas = 0

    # 1 e 2 — ledger sem transcrição: o laudo nasce e a promoção cai.
    with tempfile.TemporaryDirectory() as d:
        attempt = _montar_tentativa(Path(d), SEM_TRANSCRICAO, TEXTO)
        _, erro = _validar(attempt)
        laudo = attempt / "COMPUTED_LASTRO_GATES.json"
        if not laudo.is_file():
            print("  FALHOU: a rota de produção não materializou COMPUTED_LASTRO_GATES.json")
            falhas += 1
        else:
            dados = json.loads(laudo.read_text(encoding="utf-8"))
            if not dados.get("applicable") or not dados.get("findings"):
                print(f"  FALHOU: laudo gravado sem recomputo efetivo: {dados.get('computed')}")
                falhas += 1
        if not erro:
            print("  FALHOU: gate declarado 'pass' pelo agente sobreviveu a ledger sem transcrição")
            falhas += 1

    # 3 — contraprova: fato transcrito não pode ser travado pelo mesmo caminho.
    with tempfile.TemporaryDirectory() as d:
        attempt = _montar_tentativa(Path(d), COM_TRANSCRICAO, TEXTO)
        resultado, erro = _validar(attempt)
        if erro and "lastro" in erro.lower():
            print(f"  FALHOU: fato com transcrição foi travado pelo recomputo: {erro}")
            falhas += 1
        laudo = attempt / "COMPUTED_LASTRO_GATES.json"
        if laudo.is_file():
            dados = json.loads(laudo.read_text(encoding="utf-8"))
            if dados.get("computed", {}).get("fact_grounding_verbatim") != "pass":
                print("  FALHOU: transcrição válida não produziu fact_grounding_verbatim=pass")
                falhas += 1

    if falhas:
        print(f"REGRESSÃO: {falhas} verificação(ões) da rota de produção falharam")
        return 1
    print("ok: o laudo de lastro nasce no disco pela rota de produção, derruba gate "
          "autoatestado sem transcrição e não trava fato transcrito (3 verificações)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
