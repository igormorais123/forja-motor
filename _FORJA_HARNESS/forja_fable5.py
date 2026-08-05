"""Shim de compatibilidade: `forja_fable5` foi renomeado para `forja_editorial`.

Motivo do rename (M9). O nome do módulo carregava o nome de um modelo
específico. Desde a determinação de 25/07/2026 o modelo editorial é parâmetro
lido da allowlist de `forja_editorial_model`, e o padrão passou a ser
`claude-opus-5`, com o Fable 5 apenas autorizado como legado. Módulo com nome
de fornecedor num harness multimodelo é convite a acoplamento: quem lê
`forja_fable5` supõe que a fase pertence àquele modelo, e a fase pertence ao
papel editorial.

Este shim existe porque há prompts de auto-research, roteiros e documentação
histórica que importam o nome antigo. Ele não deve receber lógica nova: tudo
vive em `forja_editorial`. A remoção fica condicionada a não haver mais
referência viva ao nome antigo — a busca é `grep -rn "forja_fable5"` fora de
`reports/`, `telemetria/` e `autoresearch/`, que são registro histórico e não
se reescrevem.

Compatibilidade de artefato, que é separada desta: `EDITORIAL_RESULT.json` é o
nome canônico e os leitores ainda aceitam `FABLE5_RESULT.json`, assim como
`editor_usage` ainda aceita `fable5_usage`. Ver `forja_n3_common.ALIASES`.
"""
from __future__ import annotations

import warnings

from forja_editorial import *  # noqa: F401,F403
from forja_editorial import (  # noqa: F401  (reexport explícito do contrato usado por terceiros)
    FINAL_MARKER,
    MAX_REWRITE_ATTEMPTS,
    PHASE,
    PROMPT,
    REPORT_MARKER,
    TASTE_PROTOCOL,
    TIMEOUT_S,
    main,
    run_editorial_pass,
)

warnings.warn(
    "forja_fable5 foi renomeado para forja_editorial; o shim será removido "
    "quando não houver mais referência viva ao nome antigo",
    DeprecationWarning,
    stacklevel=2,
)

if __name__ == "__main__":
    raise SystemExit(main())
