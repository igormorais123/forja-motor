# -*- coding: utf-8 -*-
"""test_forja_exploracao_diversidade.py — formulário é acusado, exploração passa.

Contexto medido em 05/08/2026. As 14 árvores `F2_QUESTION_TREE.json` do acervo com
protocolo `FORJA-F2A-100-v1` carregam, entre 100 perguntas: de 0 a 8 valores
distintos de `unansweredConsequence`, 1 ou 10 de `caseAnchor`, de 1 a 5 de
`downstreamTargets`. As 14 condições estruturais que o validador confere são todas
satisfeitas por um formulário bem preenchido, e por isso as 14 passavam.

Duas checagens novas, ambas P1:

  - `N4-Q-100-DIVERSITY` — os campos que carregam o pensamento não podem ser os
    mesmos em todas as perguntas. Piso de 10 valores distintos em 100, que é o teto
    observado no acervo inteiro (o padrão "um por ótica").
  - `N4-Q-100-NO-GAP` — nenhuma pergunta bloqueada em 100 é implausível, e desliga
    a única checagem que cobraria a consequência da lacuna. `unansweredConsequence`
    só é exigido quando `status == "blocked"`; como quem produz a árvore escolhe o
    status, declarar tudo `answered` isenta o produtor do campo que o obrigaria a
    pensar sobre o que não sabe. A precondição da checagem estava nas mãos de quem
    ela deveria conferir.

**O caso que dá valor a esta suíte é o controle.** Um gate que acusa 14 de 14 pode
estar certo ou pode simplesmente acusar tudo. Só a árvore diversa, que passa limpa,
distingue uma coisa da outra.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ))

from forja_exploracao_100 import validate_exploration_100  # noqa: E402

LENTES_POR_PERGUNTA = 10


def _codigos(payload: dict) -> set[str]:
    saida = validate_exploration_100(payload)
    achados = saida if isinstance(saida, list) else (
        saida.get("findings") or saida.get("achados") or [])
    return {a.get("code") for a in achados}


def _severidade(payload: dict, codigo: str) -> str | None:
    saida = validate_exploration_100(payload)
    achados = saida if isinstance(saida, list) else (
        saida.get("findings") or saida.get("achados") or [])
    for a in achados:
        if a.get("code") == codigo:
            return a.get("severity")
    return None


def _validar_cli(payload: dict) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory(prefix="forja-f2a-cli-") as pasta:
        caminho = Path(pasta) / "tree.json"
        caminho.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        return subprocess.run(
            [sys.executable, str(RAIZ / "forja_exploracao_100.py"), "validate", str(caminho)],
            cwd=RAIZ,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )


def _arvore(*, diversa: bool, com_lacuna: bool, n: int = 100) -> dict:
    """Monta uma árvore mínima. Só interessam os campos das duas checagens novas."""
    from forja_exploracao_100 import LENSES
    lentes = list(LENSES)
    questions = []
    for i in range(1, n + 1):
        lente = lentes[(i - 1) // (n // len(lentes))] if lentes else "x"
        if diversa:
            ancora = f"nos autos, evento {i}: o laudo de fl. {100 + i} registra o item {i}"
            consequencia = (f"sem a resposta {i}, a tese de mérito perde o elo {i} e "
                            "a peça teria de recuar para pedido subsidiário")
            rota = ["F3"] if i % 3 == 0 else (["F4"] if i % 3 == 1 else ["F5"])
            porque = f"decide a questão {i}, que muda o pedido e não apenas a redação"
        else:
            ancora = "no caso concreto"
            consequencia = "Impede considerar concluída a exploração F2-A."
            rota = ["F3"]
            porque = f"importa para a ótica {lente}"
        bloqueada = com_lacuna and i % 20 == 0
        questions.append({
            "questionId": f"Q{i:03d}",
            "lens": lente,
            "text": f"Pergunta {i} sobre o ponto {i} do caso, formulada de modo distinto",
            "caseAnchor": ancora,
            "whyItMatters": porque,
            "unansweredConsequence": consequencia,
            "downstreamTargets": rota,
            "status": "blocked" if bloqueada else "answered",
            "epistemicStatus": "not_verified" if bloqueada else "confirmed_document",
            "materiality": "material",
            "answer": ("A resposta depende da conferência documental da fonte indicada."
                       if bloqueada else f"resposta {i} com lastro no documento {i}"),
            "supportIds": [f"F{i:03d}"],
            "category": "processual",
        })
    bloqueadas = sum(q["status"] == "blocked" for q in questions)
    return {
        "protocolVersion": "FORJA-F2A-100-v1",
        "problemDefinition": (
            "A decisão depende de distinguir o fato documentado da hipótese ainda "
            "não verificada no caso concreto."
        ),
        "diagnosticSynthesis": (
            "A leitura das fontes disponíveis separa fatos, lacunas e inferências, "
            "permitindo escolher uma rota jurídica reversível e rastreável."
        ),
        "questions": questions,
        "coverage": {
            "total": len(questions),
            "material": len(questions),
            "answeredMaterial": len(questions) - bloqueadas,
            "blockedMaterial": bloqueadas,
            "perLens": {lente: 10 for lente in lentes},
        },
        "solutionHypotheses": [
            {
                "hypothesisId": "H01",
                "description": "Seguir a tese principal somente com os fatos confirmados.",
                "conditions": ["a fonte principal confirma o fato"],
                "risks": ["a lacuna documental pode exigir recuo"],
                "questionIds": ["Q001"],
            },
            {
                "hypothesisId": "H02",
                "description": "Preservar pedido subsidiário até a diligência documental.",
                "conditions": ["a fonte principal permanece incompleta"],
                "risks": ["a solução pode ter alcance menor"],
                "questionIds": ["Q002"],
            },
        ],
        "downstreamHandoff": {fase: ["Q001"] for fase in ("F3", "F4", "F5", "F6", "F7")},
        "openDecisiveQuestions": [],
        "draftRelease": "blocked" if bloqueadas else "ready_for_drafting",
    }


def rodar() -> int:
    falhas = []

    def caso(nome, ok, detalhe=""):
        if ok:
            return
        print(f"  FALHOU: {nome} {detalhe}")
        falhas.append(nome)

    # --- CONTROLE: exploração genuína não pode ser acusada -------------------
    boa = _arvore(diversa=True, com_lacuna=True)
    codigos = _codigos(boa)
    caso("controle: árvore diversa não é acusada de repetição",
         "N4-Q-100-DIVERSITY" not in codigos, str(sorted(codigos))[:220])
    caso("controle: árvore com lacuna declarada não é acusada de ausência de lacuna",
         "N4-Q-100-NO-GAP" not in codigos, str(sorted(codigos))[:220])

    # --- SABOTAGEM 1: formulário ---------------------------------------------
    formulario = _arvore(diversa=False, com_lacuna=True)
    codigos = _codigos(formulario)
    caso("sabotagem: formulário com campos repetidos é acusado",
         "N4-Q-100-DIVERSITY" in codigos, str(sorted(codigos))[:220])
    caso("a acusação de repetição é P1, não P0",
         _severidade(formulario, "N4-Q-100-DIVERSITY") == "p1",
         str(_severidade(formulario, "N4-Q-100-DIVERSITY")))

    # --- SABOTAGEM 2: tudo respondido, nada bloqueado ------------------------
    sem_lacuna = _arvore(diversa=True, com_lacuna=False)
    codigos = _codigos(sem_lacuna)
    caso("sabotagem: 100 respondidas e nenhuma bloqueada é acusado",
         "N4-Q-100-NO-GAP" in codigos, str(sorted(codigos))[:220])
    caso("a acusação de ausência de lacuna é P1, não P0",
         _severidade(sem_lacuna, "N4-Q-100-NO-GAP") == "p1",
         str(_severidade(sem_lacuna, "N4-Q-100-NO-GAP")))

    # --- SABOTAGEM 3: diversidade parcial ------------------------------------
    # Um campo diverso não compra os outros. Este caso existe porque a primeira
    # ideia era exigir diversidade "em algum campo", e isso seria trivial de
    # satisfazer variando só o mais barato de variar.
    meio = _arvore(diversa=False, com_lacuna=True)
    for i, q in enumerate(meio["questions"], 1):
        q["caseAnchor"] = f"âncora distinta {i} no evento {i} dos autos"
    codigos = _codigos(meio)
    caso("sabotagem: variar só um campo não compra os demais",
         "N4-Q-100-DIVERSITY" in codigos, str(sorted(codigos))[:220])

    # --- as checagens novas não podem ter criado bloqueio --------------------
    for nome, arv in (("formulário", formulario), ("sem lacuna", sem_lacuna)):
        saida = validate_exploration_100(arv)
        achados = saida if isinstance(saida, list) else (
            saida.get("findings") or saida.get("achados") or [])
        p0_novos = [a for a in achados
                    if a.get("severity") == "p0"
                    and a.get("code") in {"N4-Q-100-DIVERSITY", "N4-Q-100-NO-GAP"}]
        caso(f"nenhuma checagem nova bloqueia ({nome})", not p0_novos, str(p0_novos))

    # --- CONTRAPROVA DE CLI: P1 informa; P0 bloqueia -------------------------
    for nome, arv in (("formulário", formulario), ("sem lacuna", sem_lacuna)):
        resultado = _validar_cli(arv)
        saida = json.loads(resultado.stdout)
        caso(f"CLI preserva a aprovação com P1 ({nome})",
             resultado.returncode == 0 and saida["approved"] is True,
             f"returncode={resultado.returncode}, approved={saida.get('approved')}")

    p0 = _arvore(diversa=True, com_lacuna=True)
    p0["questions"] = p0["questions"][:-1]
    resultado_p0 = _validar_cli(p0)
    saida_p0 = json.loads(resultado_p0.stdout)
    caso("CLI continua bloqueando uma falha P0",
         resultado_p0.returncode != 0 and saida_p0["approved"] is False,
         f"returncode={resultado_p0.returncode}, approved={saida_p0.get('approved')}")

    if falhas:
        print(f"\nFALHOU: {len(falhas)} verificação(ões) — {', '.join(falhas)}")
        return 1
    print("ok: formulário é acusado, exploração genuína passa limpa, e nenhuma das "
          "duas checagens novas bloqueia a fábrica")
    return 0


if __name__ == "__main__":  # pragma: no cover
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    raise SystemExit(rodar())
