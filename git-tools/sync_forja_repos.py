# -*- coding: utf-8 -*-
"""Mantém os dois repositórios da FORJA atuais a partir da pasta de trabalho.

Por que existe. O repositório único anterior misturava o motor com 17 GB de acervo
processual e por isso deixou de conseguir subir: o primeiro commit não publicado
sozinho tinha 3,47 GB, e commit é atômico — não há fatiamento possível. O push
falhava todo dia desde 31/07/2026, num log que ninguém abria, e o GitHub parecia
ser cópia de segurança sem ser.

A separação em dois repositórios resolve o volume e resolve junto uma questão de
governança: o motor não carrega nome de cliente e pode ser lido por qualquer
engenheiro; o acervo de auditoria carrega, e tem outro regime de acesso.

    forja-harness             motor: código, contratos, schemas, testes, doutrina
    forja-acervo-auditoria    state/, modelos aprovados, painel de gestão

O acervo processual — autos, laudos, anexos — não vai a nenhum dos dois. Fica no
disco de trabalho, e a origem dele é o e-mail.

Uso:
    python sync_forja_repos.py            # sincroniza e envia
    python sync_forja_repos.py --seco     # mostra o que faria, sem tocar em nada
"""
from __future__ import annotations

import argparse
import filecmp
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

TRABALHO = Path(__file__).resolve().parent.parent
REPOS = Path(os.environ.get("USERPROFILE", "C:/Users/IgorPC")) / "repos"
MOTOR = REPOS / "forja-harness"
ACERVO = REPOS / "forja-acervo-auditoria"

# GitHub recusa arquivo acima de 100 MB. A margem existe porque o limite vale
# para o objeto após compressão de transporte.
LIMITE_BYTES = 95 * 2**20

# `cache/` NÃO entra aqui: `cache/fontes_oficiais/` guarda súmulas e dispositivos
# em texto verbatim conferido, que é dado do MOTOR e do qual a suíte de fontes
# oficiais depende. Excluí-lo por parecer descartável deixou 1 suíte reprovada no
# teste de reconstituição — o nome "cache" enganou.
IGNORAR_DIR = {".git", "__pycache__", "node_modules", ".venv", ".pytest_cache",
               ".mypy_cache", "telemetria"}

# (origem relativa à pasta de trabalho, destino relativo ao repo, subpastas excluídas)
MAPA_MOTOR = [
    ("_FORJA_HARNESS", "_FORJA_HARNESS", ("state",)),
    ("_FERRAMENTAS", "_FERRAMENTAS", ()),
    ("git-tools", "git-tools", ()),
    ("_LEIS_GERAIS", "_LEIS_GERAIS", ()),
    ("00_IA_NAVIGACAO", "00_IA_NAVIGACAO", ()),
    # O painel de gestão tem CÓDIGO que o motor importa — `test_forja_n3_*` e
    # `test_forja_post_protocol` morriam com `ModuleNotFoundError:
    # dashboard_enrichment` quando a pasta inteira foi para o repositório de
    # acervo. Aqui vem só o executável; os dados (demandas, entregas, logs e os
    # HTML gerados com nome de cliente) vão para o outro repositório.
    ("gestao_escritorio", "gestao_escritorio",
     ("data", "entregas_fabio_osorio", "logs")),
    (".claude", ".claude", ()),
    (".agents", ".agents", ()),
    (".codex", ".codex", ()),
]
ARQUIVOS_MOTOR = [
    "CLAUDE.md", "AGENTS.md", "APRENDIZADOS_FEEDBACK_HUMANO.md",
    "PROTOCOLO_TRATAMENTO_E_CITACAO_ACERVO_PROCESSUAL.md",
    "PROTOCOLO_FECHAMENTO_MULTICANAL_WHATSAPP_EMAIL.md",
    "PROMPT-FABRICA-MELHORIA-PETICAO.md", "FAILURE_TAXONOMY.md",
    "QUALITY_BOARD.md", "ARCHIFY_ARQUITETURA.md", "GRAPHIFY_GRAFO.md",
    "ATUALIZAR_MAPA_IA.ps1", "INICIAR_MAPA_IA_VIVO.ps1", "GITHUB_BACKUP_README.md",
]
MAPA_ACERVO = [
    ("_FORJA_HARNESS/state", "state", ()),
    ("_MODELOS", "_MODELOS", ()),
    # Só o que é dado: demandas, entregas ao titular, logs. O código do painel
    # fica no motor, porque a esteira o importa.
    ("gestao_escritorio/data", "gestao_escritorio/data", ()),
    ("gestao_escritorio/entregas_fabio_osorio", "gestao_escritorio/entregas_fabio_osorio", ()),
    ("gestao_escritorio/logs", "gestao_escritorio/logs", ()),
]
ARQUIVOS_ACERVO = [
    "ENTREGAS_FABIO_OSORIO.md", "CONTROLE_AUTOS_COMPLETOS_2026-07-19.md",
    "RELATORIO_SISTEMA_GESTAO_ESCRITORIO.md",
]
ARQUIVOS_ACERVO_EXTRA = [
    ("gestao_escritorio/PAINEL_ESCRITORIO_MEDINA_OSORIO.html",
     "gestao_escritorio/PAINEL_ESCRITORIO_MEDINA_OSORIO.html"),
    ("gestao_escritorio/painel_gestao_escritorio.html",
     "gestao_escritorio/painel_gestao_escritorio.html"),
    ("gestao_escritorio/TRIAGEM_AUDIOS_FABIO_2026-07-10.md",
     "gestao_escritorio/TRIAGEM_AUDIOS_FABIO_2026-07-10.md"),
    ("gestao_escritorio/NOTA_DECISAO_PENDENCIAS_ENTREGA_2026-07-23.md",
     "gestao_escritorio/NOTA_DECISAO_PENDENCIAS_ENTREGA_2026-07-23.md"),
]


# Arquivos que ficam de fora do MOTOR mesmo estando numa pasta de código: são
# saída gerada a partir de dado de cliente. O painel HTML tem 1 MB de nome de
# cliente e número de processo dentro.
FORA_DO_MOTOR = (
    "gestao_escritorio/PAINEL_ESCRITORIO_MEDINA_OSORIO.html",
    "gestao_escritorio/painel_gestao_escritorio.html",
    "gestao_escritorio/TRIAGEM_AUDIOS_FABIO_2026-07-10.md",
    "gestao_escritorio/NOTA_DECISAO_PENDENCIAS_ENTREGA_2026-07-23.md",
)


def _iguais(a: Path, b: Path) -> bool:
    """Compara por tamanho e conteúdo, nunca por data de modificação.

    Data engana: o observador de mapas reescreve arquivo com conteúdo idêntico e
    a data muda. Sincronizar por data produziria commit vazio de substância todo
    dia, e commit assim treina o leitor a ignorar o histórico.
    """
    try:
        if a.stat().st_size != b.stat().st_size:
            return False
    except OSError:
        return False
    return filecmp.cmp(a, b, shallow=False)


def espelhar(origem: Path, destino: Path, excluir: tuple[str, ...],
             grandes: list, seco: bool, fora: tuple[str, ...] = ()) -> tuple[int, int]:
    """Copia o que mudou e apaga o que sumiu. Devolve (copiados, removidos)."""
    copiados = removidos = 0
    if not origem.is_dir():
        return 0, 0
    presentes: set[Path] = set()
    vetados = {f for f in fora}

    for raiz, dirs, arqs in os.walk(origem):
        dirs[:] = [d for d in dirs if d not in IGNORAR_DIR]
        rel = Path(raiz).relative_to(origem)
        if any(str(rel) == e or str(rel).startswith(e + os.sep) for e in excluir):
            dirs[:] = []
            continue
        for nome in arqs:
            fonte = Path(raiz) / nome
            if str(fonte.relative_to(TRABALHO)).replace(os.sep, "/") in vetados:
                continue
            try:
                tamanho = fonte.stat().st_size
            except OSError:
                continue
            if tamanho > LIMITE_BYTES:
                # Não é silêncio: entra no manifesto do repositório.
                grandes.append((str(fonte.relative_to(TRABALHO)).replace(os.sep, "/"),
                                tamanho))
                continue
            alvo = destino / rel / nome
            presentes.add(alvo)
            if alvo.is_file() and _iguais(fonte, alvo):
                continue
            if not seco:
                alvo.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(fonte, alvo)
            copiados += 1

    # Apagar do repositório o que não existe mais na pasta de trabalho — senão o
    # repositório vira acúmulo e deixa de retratar o estado real.
    if destino.is_dir():
        for raiz, dirs, arqs in os.walk(destino):
            dirs[:] = [d for d in dirs if d != ".git"]
            for nome in arqs:
                alvo = Path(raiz) / nome
                if alvo not in presentes:
                    if not seco:
                        alvo.unlink(missing_ok=True)
                    removidos += 1
    return copiados, removidos


def sincronizar(repo: Path, mapa: list, arquivos: list, seco: bool,
                fora: tuple[str, ...] = ()) -> dict:
    grandes: list = []
    copiados = removidos = 0
    for orig_rel, dest_rel, excluir in mapa:
        c, r = espelhar(TRABALHO / orig_rel, repo / dest_rel, excluir, grandes, seco, fora)
        copiados += c
        removidos += r
    pares = [(n, n) for n in arquivos]
    if repo == ACERVO:
        pares += ARQUIVOS_ACERVO_EXTRA
    for nome, destino_rel in pares:
        fonte = TRABALHO / nome
        if not fonte.is_file():
            continue
        alvo = repo / destino_rel
        alvo.parent.mkdir(parents=True, exist_ok=True) if not seco else None
        if alvo.is_file() and _iguais(fonte, alvo):
            continue
        if not seco:
            shutil.copy2(fonte, alvo)
        copiados += 1

    if grandes and not seco:
        (repo / "ARTEFATOS_FORA_DO_REPOSITORIO.json").write_text(json.dumps({
            "schemaVersion": 1,
            "porQue": ("Acima do limite de 100 MB por arquivo do GitHub. Permanecem no disco "
                       "de trabalho. Quando estão presos por hash num ledger de eventos, não "
                       "podem ser regenerados nem encolhidos sem quebrar a cadeia de auditoria."),
            "atualizadoEm": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "arquivos": [{"caminho": c, "bytes": b} for c, b in sorted(grandes)],
        }, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"copiados": copiados, "removidos": removidos, "grandes": len(grandes)}


def publicar(repo: Path, seco: bool) -> str:
    def git(*args, **kw):
        return subprocess.run(["git", "-C", str(repo), *args],
                              capture_output=True, text=True,
                              encoding="utf-8", errors="replace", **kw)
    git("add", "-A")
    if git("diff", "--cached", "--quiet").returncode == 0:
        return "sem mudanças"
    if seco:
        n = len([l for l in git("diff", "--cached", "--name-only").stdout.splitlines() if l])
        return f"[seco] {n} arquivo(s) entrariam no commit"
    msg = "sync: {:%Y-%m-%d %H:%M:%S}".format(datetime.now())
    c = git("-c", "user.name=FORJA sync", "-c", "user.email=forja-sync@localhost",
            "commit", "-m", msg)
    if c.returncode != 0:
        return f"ERRO no commit: {c.stderr.strip()[:200]}"
    p = git("push", "origin", "main")
    if p.returncode != 0:
        return f"ERRO no push: {(p.stderr or p.stdout).strip()[:300]}"
    return f"enviado: {msg}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--seco", action="store_true",
                    help="mostra o que faria, sem copiar, commitar ou enviar")
    args = ap.parse_args()

    falhou = False
    for nome, repo, mapa, arqs in (("motor", MOTOR, MAPA_MOTOR, ARQUIVOS_MOTOR),
                                   ("acervo", ACERVO, MAPA_ACERVO, ARQUIVOS_ACERVO)):
        if not (repo / ".git").is_dir():
            print(f"{nome}: repositório ausente em {repo}")
            falhou = True
            continue
        r = sincronizar(repo, mapa, arqs, args.seco,
                        fora=FORA_DO_MOTOR if nome == "motor" else ())
        estado = publicar(repo, args.seco)
        print(f"{nome:7} copiados={r['copiados']:5} removidos={r['removidos']:5} "
              f"fora-por-tamanho={r['grandes']:2} | {estado}")
        falhou |= estado.startswith("ERRO")
    return 1 if falhou else 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    raise SystemExit(main())
