# -*- coding: utf-8 -*-
"""test_forja_ingestao.py — regressão de `critical_documents_indexed` e
`coverage_declared`, mais os gates da exploração F2.

Três contraprovas vieram de medição e cada uma derrubou uma regra que parecia
óbvia: índice sem `documents[]` (o acervo está em `keyDocuments`), caminho que
não resolve daqui (4 dos 6 índices reais), e completude qualificada ao lado de
lacuna declarada (os 5 ledgers reais, e isso é honestidade, não contradição).

Uso: python test_forja_ingestao.py   (exit 0 = ok; exit 1 = regressão)
"""
from __future__ import annotations

import hashlib
import io
import json
import sys
import tempfile
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from forja_ingestao import (  # noqa: E402
    GATE_COBERTURA, GATE_INDICE, validar_cobertura, validar_indice_documentos)


def main() -> int:
    falhas = 0
    casos = 0
    temp = Path(tempfile.mkdtemp(prefix="forja_ingestao_"))
    doc = temp / "peticao.pdf"
    doc.write_bytes(b"conteudo do documento")
    digest = hashlib.sha256(doc.read_bytes()).hexdigest()

    def checar(nome, obtido, esperado):
        nonlocal falhas, casos
        casos += 1
        if obtido != esperado:
            print(f"  FALHOU: {nome} — esperado {esperado}, obtido {obtido}")
            falhas += 1

    def indice(dados, base=None):
        return validar_indice_documentos(dados, base)["gates"][GATE_INDICE]

    def cobertura(dados):
        return validar_cobertura(dados)["gates"][GATE_COBERTURA]

    checar("índice ausente", indice(None), "fail")
    checar("índice vazio", indice({}), "fail")
    checar("índice sem acervo, sem crítico e sem totais",
           indice({"schemaVersion": 1, "caseId": "x"}), "fail")
    checar("hash que não confere com o arquivo",
           indice({"documents": [{"id": "D1", "path": "peticao.pdf", "sha256": "0" * 64,
                                  "critical": True}]}, temp), "fail")
    checar("hash que confere",
           indice({"documents": [{"id": "D1", "path": "peticao.pdf", "sha256": digest,
                                  "critical": True}]}, temp), "pass")
    # O acervo prova que existe índice legítimo sem `documents[]`.
    checar("acervo declarado só no topo, como a Natura",
           indice({"keyDocuments": ["laudo", "decisão"],
                   "aggregateValidation": {"files": 200, "pdfPages": 3035}}), "pass")
    # Nenhum ato crítico apontado: avisa, não trava.
    checar("índice sem nenhum ato crítico apontado",
           indice({"documents": [{"id": "D1", "name": "a.pdf"}]}), "warn")

    checar("ledger ausente", cobertura(None), "fail")
    checar("ledger que não declara cobertura alguma",
           cobertura({"schemaVersion": 1, "generatedAt": "2026-08-04"}), "fail")
    checar("validados acima de recebidos",
           cobertura({"declaredCoverage": "integral", "sourcePdfsReceived": 10,
                      "sourcePdfsValidated": 12}), "fail")
    checar("validação parcial sem qualificação",
           cobertura({"declaredCoverage": "integral", "sourcePdfsReceived": 12,
                      "sourcePdfsValidated": 9}), "warn")
    checar("completude nua sobre lacuna registrada",
           cobertura({"coverageStatus": "complete", "openGaps": ["falta o laudo"]}), "warn")
    # A forma que o acervo inteiro usa: completude qualificada + lacuna ao lado.
    checar("completude qualificada com lacuna declarada",
           cobertura({"coverageStatus": "complete_for_f2a_internal_working",
                      "knownGap": "cálculos recebidos em PDF"}), "pass")

    # CONTRAPROVA — artefatos reais. Nenhum pode ser REPROVADO.
    indices, ledgers = {}, {}
    for arquivo in Path("state").rglob("document_index.json"):
        try:
            dados = json.loads(arquivo.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            continue
        if not isinstance(dados, dict):
            continue
        chave = tuple(sorted(dados))
        if chave in indices:
            continue
        indices[chave] = arquivo
        casos += 1
        if indice(dados, arquivo.parent) == "fail":
            print(f"  TRAVOU O APROVADO: {arquivo}")
            falhas += 1

    for arquivo in Path("state").rglob("coverage_ledger.json"):
        try:
            dados = json.loads(arquivo.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            continue
        if not isinstance(dados, dict):
            continue
        chave = tuple(sorted(dados))
        if chave in ledgers:
            continue
        ledgers[chave] = arquivo
        casos += 1
        if cobertura(dados) == "fail":
            print(f"  TRAVOU O APROVADO: {arquivo}")
            falhas += 1

    if len(indices) < 4 or len(ledgers) < 4:
        print(f"  FALHOU: contraprova magra — {len(indices)} índices e {len(ledgers)} "
              "ledgers reais examinados")
        falhas += 1

    # --- gates da exploração F2, nomeados a partir do validador que já existia ---
    from forja_exploracao_100 import gates_da_exploracao

    vazio = gates_da_exploracao({}, require_protocol=True)["gates"]
    for gate in ("exploration_100_complete", "answers_provenance_classified",
                 "downstream_handoff_ready"):
        casos += 1
        if vazio.get(gate) != "fail":
            print(f"  FALHOU: exploração vazia devolveu {vazio.get(gate)} em {gate}")
            falhas += 1

    # Achado de código novo, ainda não mapeado, não pode passar despercebido.
    import forja_exploracao_100 as exp

    original = exp.validate_exploration_100
    try:
        exp.validate_exploration_100 = lambda payload, **kw: [
            {"code": "N4-Q-CODIGO-QUE-AINDA-NAO-EXISTE", "detail": "achado novo"}]
        casos += 1
        if exp.gates_da_exploracao({})["gates"]["exploration_100_complete"] != "fail":
            print("  FALHOU: achado de código não mapeado foi aprovado por omissão")
            falhas += 1
    finally:
        exp.validate_exploration_100 = original

    # CONTRAPROVA da exploração — as árvores reais não podem reprovar.
    arvores = 0
    for arquivo in Path("state").rglob("question_tree.json"):
        try:
            dados = json.loads(arquivo.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            continue
        if not isinstance(dados, dict) or dados.get("protocolVersion") is None:
            continue
        arvores += 1
        casos += 1
        if original(dados, require_protocol=True):
            continue  # a árvore já era reprovada pelo validador; não é regressão minha
        if exp.gates_da_exploracao(dados)["gates"]["exploration_100_complete"] != "pass":
            print(f"  TRAVOU O APROVADO: {arquivo} passa no validador e reprova no gate")
            falhas += 1

    if falhas:
        print(f"REGRESSÃO: {falhas} de {casos} verificações de ingestão/exploração falharam")
        return 1
    print(f"ok: {casos} verificações — {len(indices)} índices, {len(ledgers)} ledgers e "
          f"{arvores} árvores de exploração reais, nenhum reprovado")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
