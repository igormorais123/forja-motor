---
type: "query"
date: "2026-07-24T21:31:06.093469+00:00"
question: "Onde integrar gosto jurídico autônomo, diferenciação, grounding e seleção editorial na FORJA?"
contributor: "graphify"
outcome: "useful"
source_nodes: ["forja_estilo_humano.py", "forja_fable5.py", "forja_editorial_fidelity.py", "forja_run._validate_fable5_editorial(phase: str, artifacts: list[dict]) -> None", "test_forja_estilo_humano.py", "test_forja_fable5.py"]
---

# Q: Onde integrar gosto jurídico autônomo, diferenciação, grounding e seleção editorial na FORJA?

## Answer

Expanded from original query via vocab: [forja, estilo, humano, editorial, audit, validate, run, package, fable, texto, redacao, test]. O grafo localizou forja_estilo_humano.py como gate observável, forja_fable5.py como passe editorial F7-B, forja_editorial_fidelity.py como verificador independente, forja_run.py como recomposição na promoção, e test_forja_estilo_humano.py/test_forja_fable5.py como regressões. A menor integração coerente é prompt EDGE em F6/F7 e F7-B, recibo validado no executor, e comparação cega no AUTO-RESEARCH, sem alterar runner ou contratos nesta onda.

## Outcome

- Signal: useful

## Source Nodes

- forja_estilo_humano.py
- forja_fable5.py
- forja_editorial_fidelity.py
- forja_run._validate_fable5_editorial(phase: str, artifacts: list[dict]) -> None
- test_forja_estilo_humano.py
- test_forja_fable5.py