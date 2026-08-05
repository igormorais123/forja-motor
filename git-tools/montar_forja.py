# -*- coding: utf-8 -*-
"""montar_forja.py — reconstitui a árvore de trabalho a partir dos dois repositórios.

A FORJA vive em dois repositórios privados que se completam:

    forja-motor       o sistema
    forja-auditoria   a cadeia de auditoria, os modelos e o painel

Os dois usam a MESMA estrutura de caminhos, então montar é copiar um sobre o
outro. Este script existe para que isso seja um comando, e não uma sequência que
cada pessoa refaz de memória — e porque a montagem precisa TERMINAR EM PROVA, e
não em "os arquivos estão lá".

Foi essa diferença que pegou os três defeitos da primeira separação, em
05/08/2026: `cache/fontes_oficiais/` fora por parecer descartável, o código do
painel de gestão num repositório e seu importador no outro, e a conversão
automática de fim de linha do git alterando os bytes de 1.594 arquivos presos
por sha256. Conferir a lista de arquivos aprovaria os três.

O que a árvore montada NÃO tem: os autos. Laudos, anexos e PDFs dos processos não
vão a repositório nenhum, e a origem deles é o e-mail. As verificações que
dependem deles dizem que não verificaram, em vez de passar caladas.

Uso:
    python montar_forja.py DESTINO
    python montar_forja.py DESTINO --sem-testes
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

MOTOR = "https://github.com/igormorais123/forja-motor.git"
ACERVO = "https://github.com/igormorais123/forja-auditoria.git"


def _rodar(*args, cwd=None) -> subprocess.CompletedProcess:
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True,
                          encoding="utf-8", errors="replace")


def clonar(url: str, destino: Path) -> bool:
    print(f"  clonando {url.rsplit('/', 1)[-1]} ...", flush=True)
    r = _rodar("git", "clone", "--quiet", url, str(destino))
    if r.returncode != 0:
        print(f"  ERRO: {(r.stderr or r.stdout).strip()[:300]}")
        return False
    return True


def sobrepor(origem: Path, destino: Path) -> int:
    """Copia o acervo sobre a árvore do motor, sem o `.git` dele."""
    copiados = 0
    for p in origem.rglob("*"):
        if not p.is_file() or ".git" in p.parts:
            continue
        alvo = destino / p.relative_to(origem)
        alvo.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, alvo)
        copiados += 1
    return copiados


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("destino", type=Path)
    ap.add_argument("--sem-testes", action="store_true",
                    help="monta sem rodar o baseline — a montagem fica SEM PROVA")
    args = ap.parse_args(argv)

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    destino = args.destino.resolve()
    if destino.exists() and any(destino.iterdir()):
        print(f"REPROVADO — {destino} existe e não está vazia.")
        return 1
    destino.parent.mkdir(parents=True, exist_ok=True)

    if not clonar(MOTOR, destino):
        return 1
    temporario = destino.parent / (destino.name + "__acervo")
    if temporario.exists():
        shutil.rmtree(temporario, ignore_errors=True)
    if not clonar(ACERVO, temporario):
        return 1

    copiados = sobrepor(temporario, destino)
    shutil.rmtree(temporario, ignore_errors=True)
    print(f"  {copiados} arquivo(s) do acervo sobrepostos")

    # A prova de que a árvore está inteira não é a contagem de arquivos: é a
    # esteira rodando dentro dela. Sem isto a montagem é uma promessa.
    if args.sem_testes:
        print("\nMontado SEM PROVA (--sem-testes). Rode o baseline antes de confiar:")
        print(f"  cd {destino} && python -X utf8 _FORJA_HARNESS/forja_baseline.py")
        return 0

    print("\n  rodando o baseline na árvore montada ...", flush=True)
    r = _rodar(sys.executable, "-X", "utf8", "forja_baseline.py", "--quiet",
               cwd=str(destino / "_FORJA_HARNESS"))
    print((r.stdout or "").strip()[-2000:])
    if r.returncode != 0:
        print("\nA árvore montou, mas o baseline REPROVOU. Algumas suítes exigem os "
              "autos, que não estão em repositório nenhum — leia o relatório acima e "
              "separe 'não verificado' de 'regressão' antes de concluir.")
        return 1
    print(f"\nÁrvore montada e provada em {destino}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
