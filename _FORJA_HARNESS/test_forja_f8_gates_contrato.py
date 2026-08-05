# -*- coding: utf-8 -*-
"""test_forja_f8_gates_contrato.py — o contrato F8 e o produtor não podem divergir.

Em 04/08/2026, `forja_gate_liveness.py` mediu que 14 dos 16 gates exigidos por
`phase_contracts/F8.json` não tinham produtor em lugar nenhum do harness: o nome
existia só no JSON do contrato. `_validate_result` os cobrava e nenhuma execução
sabia emiti-los, de modo que **uma F8 nova não fechava**. As duas F8 do acervo
haviam rodado antes de o contrato ser apertado, relatando 6 gates.

A causa não foi descuido pontual: o contrato evoluiu sozinho, e nada falhava
quando ele se afastava de quem o cumpre. Este teste é esse "nada" deixando de
existir. Ele compara os dois conjuntos e reprova nas duas direções — gate
exigido sem produtor, e gate produzido que o contrato não conhece.

Uso: python test_forja_f8_gates_contrato.py   (exit 0 = ok; exit 1 = regressão)
"""
from __future__ import annotations

import io
import json
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from forja_f8_contract import _gates_do_contrato  # noqa: E402

# Estes dois eram a exceção nomeada desta suíte: gates do contrato F8 sem
# produtor no validador estático. Em 04/08/2026 passaram a ser emitidos — o
# `svg_lint_pass` reexecutando `medina_svg_colisao` sobre o arquivo, o
# `markdown_lint_pass` exigindo que a afirmação de lint venha com alvo e
# resultado. Ambos devolvem `not_applicable` quando não há o que conferir, e
# por isso continuam fora da conta de "todo gate íntegro sai `pass`": o ledger
# do teste não aponta caminho de SVG nem declara lint de markdown.
FORA_DO_VALIDADOR_ESTATICO = {
    "markdown_lint_pass",   # emitido; `not_applicable` sem declaração de lint
    "svg_lint_pass",        # emitido; `not_applicable` sem caminho conferível
}


def _ledger_completo() -> dict:
    return {
        "mode": "static_ooxml_svg",
        "renderingUsed": False, "pdfCreated": False, "pngCreated": False,
        "approved": True,
        "svg": [{"approved": True}],
        "visualReviewReceipt": {
            "reviewType": "human", "reviewer": "revisor-teste",
            "reviewMethod": "manual", "approved": True,
            "signedAt": "2026-08-04T10:00:00-03:00",
            "pages": [1, 2], "pagesReviewed": 2, "pageCount": 2,
        },
        "externalTrustStoreVerified": True,
    }


LAYOUT_OK = {"findings": [], "approved": True,
             "metrics": {"justificationCoverage": 1.0, "fontCoverage": 1.0,
                         "sizeCoverage": 1.0}}
FIDELITY_OK = {"approved": True}


def main() -> int:
    falhas = 0
    contrato = set(json.loads(
        Path("phase_contracts/F8.json").read_text(encoding="utf-8"))["requiredGates"])
    esperados = contrato - FORA_DO_VALIDADOR_ESTATICO

    produzidos = set(_gates_do_contrato(_ledger_completo(), LAYOUT_OK, FIDELITY_OK, [],
                                        release_policy="strict_protocol"))

    faltando = sorted(esperados - produzidos)
    if faltando:
        print(f"  FALHOU: o contrato F8 exige gates que nenhum produtor emite: {faltando}")
        falhas += 1

    sobrando = sorted(produzidos - contrato)
    if sobrando:
        print(f"  FALHOU: o validador emite gates que o contrato F8 não conhece: {sobrando}")
        falhas += 1

    # Com tudo íntegro, o veredito é aprovação em toda a linha. Sem esta
    # contraprova, um mapeamento que devolvesse "fail" sempre passaria nos dois
    # testes de conjunto acima e tornaria o F8 impossível de fechar.
    integros = _gates_do_contrato(_ledger_completo(), LAYOUT_OK, FIDELITY_OK, [],
                                  release_policy="strict_protocol")
    reprovados = sorted(nome for nome, valor in integros.items() if valor == "fail")
    if reprovados:
        print(f"  FALHOU: documento íntegro reprovou em {reprovados} — o gate virou trava")
        falhas += 1

    # E um documento defeituoso precisa reprovar pelo motivo certo, senão o
    # mapeamento é decorativo.
    quebrado = dict(_ledger_completo())
    quebrado["renderingUsed"] = True
    quebrado["svg"] = [{"approved": False}]
    layout_ruim = {"findings": [{"code": "folio_width_unsafe"},
                                {"code": "table_typography_inconsistent"}],
                   "metrics": {"justificationCoverage": 0.7, "fontCoverage": 1.0,
                               "sizeCoverage": 1.0}}
    ruim = _gates_do_contrato(quebrado, layout_ruim, {"approved": False}, ["algo"],
                              release_policy="internal_review")
    for nome in ("no_pdf_or_raster_rendering", "svg_embeds_integrity_pass",
                 "docx_folio_collision_safe", "docx_table_typography_consistent_min_8pt",
                 "docx_body_justified_times_12_pass", "semantic_fidelity_recomputed"):
        if ruim.get(nome) != "fail":
            print(f"  FALHOU: {nome} não reprovou com o defeito correspondente presente")
            falhas += 1

    # Fora da liberação estrita, os dois gates estritos não podem virar "pass"
    # por conveniência: não ocorreram.
    fora = _gates_do_contrato(_ledger_completo(), LAYOUT_OK, FIDELITY_OK, [],
                              release_policy="internal_review")
    for nome in ("human_visual_review_signed_receipt_for_strict_release",
                 "external_human_trust_store_verified_for_strict_release"):
        if fora.get(nome) != "not_applicable":
            print(f"  FALHOU: {nome} deveria ser not_applicable fora da liberação estrita, "
                  f"veio {fora.get(nome)}")
            falhas += 1

    if falhas:
        print(f"REGRESSÃO: {falhas} verificação(ões) do contrato F8 falharam")
        return 1
    print(f"ok: {len(esperados)} gates do contrato F8 têm produtor, reprovam pelo motivo certo "
          f"e não travam documento íntegro ({len(FORA_DO_VALIDADOR_ESTATICO)} fora do validador estático, nomeados)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
