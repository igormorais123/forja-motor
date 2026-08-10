# -*- coding: utf-8 -*-
"""Revisão cruzada da FORJA pelo Codex, na família OpenAI.

Por ordem do titular de 10/08/2026, o revisor padrão de toda a esteira é o
`gpt-5.6-sol` no esforço `high`. A produção continua no modelo de produção
(`CODEX_MODELO_FORJA`); revisor e produtor não podem ser o mesmo, que é a razão
de o gate `cross_model_review_verified` existir.

Este executor existe pelo mesmo motivo que o do Diabob: chamada feita à mão
repete os mesmos erros toda vez. Os quatro que já custaram tempo estão fechados
aqui, no código, e não pedidos ao agente:

1. **Prompt por argumento, nunca por stdin.** `codex exec` com stdin trava no
   Windows e o pipe derruba a sessão. O prompt vai como argumento posicional,
   lido de arquivo. **Cuidado: no Cursor é o contrário** — lá o wrapper é um
   `.cmd`, o cmd.exe corta o argumento na primeira quebra de linha e o prompt
   TEM de ir por stdin (regressão em `test_forja_cursor_grok.py`). São binários
   diferentes com armadilhas opostas; não uniformize os dois.
2. **`--cd` explícito.** Sem ele o executor não enxerga o diretório de trabalho
   e responde "o sandbox bloqueou a leitura" — parecer sem fonte, com cara de
   parecer. Medido em 10/08/2026: a mesma pergunta, com e sem `--cd`, deu
   "não verificável" e a resposta certa.
3. **MCPs desligados.** Os servidores da sessão interativa entram na chamada,
   estouram o orçamento de contexto das skills e disparam ferramentas que nada
   têm a ver com a revisão.
4. **Sandbox somente leitura.** Revisor não altera artefato. Se alterasse, a
   revisão deixaria de ser independente do objeto revisado.

Uso:

    python forja_revisao_cruzada.py --prompt PROMPT.md --cd <pasta do caso> \
        --saida REVISAO.md [--producao]

`--producao` troca para o modelo de produção, e só deve ser usado quando a
tarefa não for revisão. O executor recusa o modelo proibido pela allowlist.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

import forja_modelos

CONTRATO = "FORJA-REVISAO-CRUZADA-v1"


def _erro(msg: str) -> "NoReturn":  # noqa: F821
    print(f"forja_revisao_cruzada: {msg}", file=sys.stderr)
    raise SystemExit(2)


def executar(prompt_path: str | Path, cd: str | Path, *,
             producao: bool = False, timeout: int = 3600) -> dict:
    """Roda o Codex sobre o prompt e devolve o parecer com a proveniência."""
    prompt_path = Path(prompt_path)
    if not prompt_path.is_file():
        _erro(f"prompt não encontrado: {prompt_path}")
    cd = Path(cd)
    if not cd.is_dir():
        _erro(f"diretório de trabalho não encontrado: {cd}")

    if producao:
        modelo = forja_modelos.CODEX_MODELO_FORJA
        esforco = forja_modelos.CODEX_ESFORCO_FORJA
        papel = "producao"
    else:
        modelo = forja_modelos.CODEX_MODELO_REVISAO_FORJA
        esforco = forja_modelos.CODEX_ESFORCO_REVISAO_FORJA
        papel = "revisao"

    if forja_modelos.modelo_remoto_proibido(modelo):
        _erro(f"modelo proibido pela allowlist: {modelo}")

    prompt = prompt_path.read_text(encoding="utf-8")
    if not prompt.strip():
        _erro("prompt vazio")

    cmd = [
        "codex", "exec",
        "--model", modelo,
        "-c", f"model_reasoning_effort={esforco}",
        "-c", "mcp_servers={}",
        "--cd", str(cd),
        "--sandbox", "read-only",
        "--skip-git-repo-check",
        prompt,
    ]

    inicio = time.time()
    try:
        r = subprocess.run(cmd, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=timeout)
    except FileNotFoundError:
        _erro("CLI `codex` não encontrado no PATH")
    except subprocess.TimeoutExpired:
        _erro(f"tempo esgotado ({timeout}s) — aumente --timeout ou reduza o escopo")
    segundos = round(time.time() - inicio, 2)

    saida = r.stdout or ""
    # O parecer é o que vem depois do último marcador de uso de tokens; antes
    # disso está o traço de execução, que não é o parecer e não deve ser lido
    # como se fosse.
    corte = saida.rfind("tokens used")
    parecer = saida[corte:].split("\n", 1)[-1].strip() if corte >= 0 else saida.strip()

    return {
        "contrato": CONTRATO,
        "papel": papel,
        "modelo": modelo,
        "esforco": esforco,
        "familia": "openai",
        "provedor": "codex-oauth",
        "cd": str(cd),
        "prompt": str(prompt_path),
        "segundos": segundos,
        "returncode": r.returncode,
        "parecer": parecer,
        "natureza": (
            "Revisao cruzada por familia distinta da que produziu o artefato. "
            "O revisor aponta defeito com evidencia; ele nao reescreve a peca, "
            "nao cria fato e nao substitui a auditoria F7."
        ),
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--cd", required=True)
    ap.add_argument("--saida")
    ap.add_argument("--producao", action="store_true",
                    help="usa o modelo de producao em vez do de revisao")
    ap.add_argument("--timeout", type=int, default=3600)
    a = ap.parse_args(argv)

    r = executar(a.prompt, a.cd, producao=a.producao, timeout=a.timeout)
    if a.saida:
        destino = Path(a.saida)
        if destino.suffix.casefold() == ".json":
            destino.write_text(json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8")
        else:
            destino.write_text(r["parecer"], encoding="utf-8")
        print(f"{r['modelo']} ({r['esforco']}) em {r['segundos']}s -> {destino}")
    else:
        print(r["parecer"])
    return 0 if r["returncode"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
