#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera mapas vivos de navegação IA para a fábrica de petições.

O script escreve um MAPA_IA.md em cada pasta analisada, além de inventário
JSON e índice central. Ele sobrescreve somente arquivos gerados por este
próprio sistema, identificados pelo marcador GENERATED_MARKER.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys
import time
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


GENERATED_MARKER = "<!-- IA_NAVIGACAO:GERADO_AUTO:v1 -->"
MAP_NAME = "MAPA_IA.md"
SYSTEM_DIR_NAME = "00_IA_NAVIGACAO"
ROOT = Path(__file__).resolve().parents[2]
SYSTEM_DIR = ROOT / SYSTEM_DIR_NAME
DATA_DIR = SYSTEM_DIR / "dados"
ROOT_MAP = ROOT / MAP_NAME
INDEX_MD = SYSTEM_DIR / "INDICE_GERAL_IA.md"
STATUS_MD = SYSTEM_DIR / "STATUS_MAPA_IA.md"
INVENTORY_JSON = DATA_DIR / "inventario_ia.json"
TREE_JSON = DATA_DIR / "arvore_ia.json"

EXCLUDED_DIR_NAMES = {".git", ".hg", ".svn", SYSTEM_DIR_NAME}
EXCLUDED_FILE_NAMES = {MAP_NAME}

TEXT_EXTS = {".md", ".txt", ".csv", ".json", ".jsonl", ".yml", ".yaml", ".tex", ".dot", ".mmd", ".js", ".py", ".ps1", ".html", ".url"}
DOC_EXTS = {".pdf", ".docx", ".doc", ".rtf", ".odt"}
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".svg", ".emf", ".gif", ".webp"}
DATA_EXTS = {".json", ".jsonl", ".csv", ".xlsx", ".xls", ".xml"}
SCRIPT_EXTS = {".py", ".ps1", ".js", ".bat", ".cmd"}

ROLE_ORDER = {
    "regras": 0,
    "comando": 1,
    "mapa_indice": 2,
    "regimento_lei": 3,
    "plano_contexto": 4,
    "peca_trabalho": 5,
    "relatorio_auditoria": 6,
    "fonte_documento": 7,
    "imagem_visual": 8,
    "dados_script": 9,
    "artefato_tecnico": 10,
    "outro": 99,
}


@dataclass
class FileInfo:
    path: Path
    rel: str
    name: str
    ext: str
    size: int
    modified: str
    role: str
    note: str
    headings: list[str] = field(default_factory=list)


@dataclass
class DirInfo:
    path: Path
    rel: str
    name: str
    depth: int
    parent_rel: str | None
    kind: str
    note: str
    total_files_recursive: int
    total_dirs_recursive: int
    size_recursive: int
    direct_files: list[FileInfo] = field(default_factory=list)
    child_dirs: list[str] = field(default_factory=list)
    ext_counts: dict[str, int] = field(default_factory=dict)
    roles: dict[str, int] = field(default_factory=dict)
    modified_latest: str = ""


def now_local() -> str:
    return dt.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %z")


def relpath(path: Path, base: Path = ROOT) -> str:
    try:
        text = os.path.relpath(path.resolve(), base.resolve()).replace("\\", "/")
    except ValueError:
        text = path.resolve().as_posix()
    return "." if text == "." else text


def md_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("|", "\\|").replace("[", "\\[").replace("]", "\\]")


def mermaid_escape(text: str) -> str:
    text = text.replace("\\n", "<br/>").replace("\\", "/").replace('"', "'")
    text = re.sub(r"\s+", " ", text).strip()
    return text[:140]


def short_label(text: str, limit: int = 58) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= limit:
        return text
    return text[: max(0, limit - 1)].rstrip() + "…"


def md_link(label: str, target: str) -> str:
    target = target.replace("\\", "/")
    if target in {"", "."}:
        target = "."
    return f"[{md_escape(label)}](<{target}>)"


def human_size(num: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    value = float(num)
    for unit in units:
        if value < 1024 or unit == units[-1]:
            if unit == "B":
                return f"{int(value)} {unit}"
            return f"{value:.1f} {unit}"
        value /= 1024
    return f"{num} B"


def safe_stat(path: Path) -> os.stat_result | None:
    try:
        return path.stat()
    except OSError:
        return None


def is_excluded_dir(path: Path) -> bool:
    return path.name in EXCLUDED_DIR_NAMES


def should_exclude_file(path: Path) -> bool:
    if path.name in EXCLUDED_FILE_NAMES:
        return True
    if any(part in EXCLUDED_DIR_NAMES for part in path.parts):
        return True
    return False


def iter_dirs() -> list[Path]:
    dirs = [ROOT]
    for current, dirnames, _filenames in os.walk(ROOT):
        current_path = Path(current)
        dirnames[:] = sorted([d for d in dirnames if d not in EXCLUDED_DIR_NAMES], key=str.casefold)
        if current_path == ROOT:
            continue
        dirs.append(current_path)
    return sorted(dirs, key=lambda p: (len(p.relative_to(ROOT).parts), relpath(p).casefold()))


def iter_files_under(path: Path) -> Iterable[Path]:
    for current, dirnames, filenames in os.walk(path):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDED_DIR_NAMES]
        for filename in filenames:
            item = Path(current) / filename
            if not should_exclude_file(item):
                yield item


def classify_file(path: Path) -> tuple[str, str]:
    name = path.name
    upper = name.upper()
    lower_path = relpath(path).casefold()
    ext = path.suffix.casefold()

    if upper in {"AGENTS.MD", "CLAUDE.MD"}:
        return "regras", "regras obrigatórias para agentes"
    if upper.startswith("COMANDO_"):
        return "comando", "origem da demanda e instrução operacional"
    if upper.startswith("REGIMENTO_INTERNO_"):
        return "regimento_lei", "regimento do tribunal; ler antes de redigir"
    if "LEIA-ME" in upper or upper == "README.MD":
        return "regras", "instruções locais da pasta"
    if upper.startswith(("MAPA", "INDICE", "ÍNDICE")) or "INDICE" in upper or "ÍNDICE" in upper:
        return "mapa_indice", "índice/mapa existente"
    if upper.startswith(("PLANO", "DOSSIE", "DOSSIÊ", "BRIEF", "CONTEXTO", "BLUEPRINT", "ROADMAP")):
        return "plano_contexto", "contexto, planejamento ou dossiê"
    if upper.startswith(("RELATORIO", "RELATÓRIO", "AUDITORIA", "CHECKLIST", "REGISTRO")) or "APRENDIZADOS" in upper:
        return "relatorio_auditoria", "relatório, auditoria, checklist ou aprendizado"
    if upper.startswith(("PETICAO", "PETIÇÃO", "MEMORIAIS", "MEMORIAL", "PARECER", "EMBARGOS", "CONTRARRAZ", "MINUTA", "AGRAVO")):
        return "peca_trabalho", "peça, minuta, parecer ou memorial"
    if ext in SCRIPT_EXTS or ext in DATA_EXTS:
        return "dados_script", "dado estruturado ou rotina técnica"
    if ext in IMAGE_EXTS:
        if any(token in lower_path for token in ["qa", "render", "pages", "img", "_build", "visual"]):
            return "artefato_tecnico", "imagem/render de QA ou build"
        return "imagem_visual", "imagem ou elemento visual"
    if ext in DOC_EXTS or ext == ".zip":
        if any(token in lower_path for token in ["anexos", "autos", "fonte", "documentos", "baixados"]):
            return "fonte_documento", "fonte/anexo para verificação"
        return "peca_trabalho", "documento de trabalho ou entrega"
    if any(token in lower_path for token in ["_build", "_extract", "docx_extract", "__pycache__", "render", "qa"]):
        return "artefato_tecnico", "artefato técnico gerado"
    return "outro", "arquivo não classificado automaticamente"


def classify_dir(path: Path, direct_files: list[FileInfo], child_names: list[str]) -> tuple[str, str]:
    if path == ROOT:
        return "raiz da fábrica", "entrada principal; ler regras, mapa vivo e escolher a pasta do caso/demanda"

    rel = relpath(path)
    name = path.name
    lower = rel.casefold()
    file_names = {f.name.upper() for f in direct_files}
    roles = {f.role for f in direct_files}

    if rel.startswith("_LEIS_GERAIS"):
        return "leis gerais obrigatórias", "Estatuto da OAB e LOMAN; considerar em toda peça"
    if rel.startswith("_ferramentas"):
        return "ferramentas de produção visual", "scripts e padrões de diagramação/QA visual"
    if rel.startswith("gestao_escritorio"):
        return "gestão de demandas", "painel, dados e rotinas de acompanhamento do escritório"
    if "skills_repertorio" in lower:
        return (
            "repertório de skills por fase",
            "cardápio, não contrato; ler só o documento da fase corrente (F0..F10)",
        )
    if "whatsapp" in lower:
        return "demanda WhatsApp", "triagem sanitizada; evitar expor conversa bruta"
    if "audio" in lower:
        return "demanda por áudio", "comando manual e materiais derivados de áudio"
    if "anexos" in lower or "autos drive" in lower or "documentos" in lower:
        return "fontes e anexos", "local de prova/documento; verificar antes de afirmar"
    if "links pendentes" in lower:
        return "links pendentes", "atalhos externos ainda dependentes de baixa ou validação"
    if "comandos e emails" in lower:
        return "emails e comandos", "origem textual da demanda e instruções recebidas"
    if any(token in lower for token in ["_build", "_extract", "docx_extract", "__pycache__", "render", "qa", "pages", "img", "media", "theme", "_rels", "customxml"]):
        return "artefatos técnicos", "build, extração ou QA; ler só quando precisar validar entrega"
    if any(token in lower for token in ["_trabalho", "trabalho", "planejamento", "visual_law", "documentacao_final", "documentação_final"]):
        return "área de trabalho", "planejamento, execução, documentação ou material visual"
    if "REGIMENTO_INTERNO" in " ".join(file_names) or "regimento_lei" in roles:
        return "caso jurídico com regimento", "identificar tribunal e ler regimento antes de redigir"
    if any(name.startswith("COMANDO_") for name in file_names):
        return "demanda operacional", "começar pelo comando e anexos antes de produzir"
    if any(role in roles for role in ["peca_trabalho", "relatorio_auditoria", "plano_contexto"]):
        return "pasta de caso/produção", "contém peça, parecer, memorial, relatório ou plano"
    if child_names:
        return "pasta organizadora", "agrega subpastas; abrir mapa filho conforme objetivo"
    return "pasta auxiliar", "conteúdo auxiliar ou residual"


def read_headings(path: Path, max_headings: int = 4) -> list[str]:
    if path.suffix.casefold() != ".md":
        return []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")[:30000]
    except OSError:
        return []
    headings: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if re.match(r"^#{1,3}\s+\S", stripped):
            title = re.sub(r"^#{1,3}\s+", "", stripped).strip()
            if title and not title.startswith("Mapa IA -"):
                headings.append(title[:120])
        if len(headings) >= max_headings:
            break
    return headings


def make_file_info(path: Path) -> FileInfo | None:
    stat = safe_stat(path)
    if stat is None:
        return None
    role, note = classify_file(path)
    return FileInfo(
        path=path,
        rel=relpath(path),
        name=path.name,
        ext=path.suffix.casefold() or "(sem extensão)",
        size=stat.st_size,
        modified=dt.datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M"),
        role=role,
        note=note,
        headings=read_headings(path),
    )


def collect() -> dict[str, DirInfo]:
    dirs = iter_dirs()
    infos: dict[str, DirInfo] = {}

    direct_files_by_dir: dict[Path, list[FileInfo]] = {}
    child_dirs_by_dir: dict[Path, list[str]] = {}
    for directory in dirs:
        direct_files: list[FileInfo] = []
        child_dirs: list[str] = []
        try:
            entries = sorted(directory.iterdir(), key=lambda p: (not p.is_dir(), p.name.casefold()))
        except OSError:
            entries = []
        for entry in entries:
            if entry.is_dir():
                if not is_excluded_dir(entry):
                    child_dirs.append(relpath(entry))
            elif entry.is_file() and not should_exclude_file(entry):
                info = make_file_info(entry)
                if info:
                    direct_files.append(info)
        direct_files.sort(key=lambda f: (ROLE_ORDER.get(f.role, 99), f.name.casefold()))
        direct_files_by_dir[directory] = direct_files
        child_dirs_by_dir[directory] = child_dirs

    # Agrega de baixo para cima. A versão anterior fazia um os.walk completo
    # para CADA pasta e degradava quadraticamente em fábricas com muitos
    # artefatos. Os dados diretos já foram coletados acima; cada pai pode somar
    # as estatísticas prontas dos filhos sem reler toda a subárvore.
    latest_by_dir: dict[Path, float] = {}
    for directory in reversed(dirs):
        direct_files = direct_files_by_dir[directory]
        ext_counter: Counter[str] = Counter(f.ext for f in direct_files)
        role_counter: Counter[str] = Counter(f.role for f in direct_files)
        size_total = sum(f.size for f in direct_files)
        total_files = len(direct_files)
        recursive_dirs = 0
        latest = 0.0
        for file_info in direct_files:
            stat = safe_stat(file_info.path)
            if stat:
                latest = max(latest, stat.st_mtime)
        for child_rel in child_dirs_by_dir[directory]:
            child_path = ROOT / child_rel
            child = infos.get(child_rel)
            # Junctions/symlinks podem aparecer em iterdir sem serem
            # percorridos por os.walk. Mantém a semântica anterior: não somar
            # uma árvore que o inventário deliberadamente não visitou.
            if child is None:
                continue
            total_files += child.total_files_recursive
            recursive_dirs += 1 + child.total_dirs_recursive
            size_total += child.size_recursive
            ext_counter.update(child.ext_counts)
            role_counter.update(child.roles)
            latest = max(latest, latest_by_dir.get(child_path, 0.0))

        rel = relpath(directory)
        parent_rel = None if directory == ROOT else relpath(directory.parent)
        kind, note = classify_dir(directory, direct_files_by_dir[directory], child_dirs_by_dir[directory])
        infos[rel] = DirInfo(
            path=directory,
            rel=rel,
            name=directory.name if directory != ROOT else ROOT.name,
            depth=0 if directory == ROOT else len(directory.relative_to(ROOT).parts),
            parent_rel=parent_rel,
            kind=kind,
            note=note,
            total_files_recursive=total_files,
            total_dirs_recursive=recursive_dirs,
            size_recursive=size_total,
            direct_files=direct_files_by_dir[directory],
            child_dirs=child_dirs_by_dir[directory],
            ext_counts=dict(ext_counter.most_common()),
            roles=dict(role_counter.most_common()),
            modified_latest=dt.datetime.fromtimestamp(latest).strftime("%Y-%m-%d %H:%M") if latest else "",
        )
        latest_by_dir[directory] = latest
    return infos


def map_target_for_dir(rel: str, from_dir: Path) -> str:
    target_dir = ROOT if rel == "." else ROOT / rel
    return relpath(target_dir / MAP_NAME, from_dir)


def rel_target(path: Path, from_dir: Path) -> str:
    return relpath(path, from_dir)


def mermaid_id(value: str) -> str:
    digest = hashlib.sha1(value.encode("utf-8", errors="ignore")).hexdigest()[:10]
    return f"N{digest}"


def make_mermaid(info: DirInfo, infos: dict[str, DirInfo]) -> str:
    lines = ["flowchart TD"]
    this_id = mermaid_id(info.rel + ":this")
    label = f"{short_label(info.name)}\\n{info.kind}\\n{info.total_files_recursive} arquivos / {info.total_dirs_recursive} subpastas"
    lines.append(f'  {this_id}["{mermaid_escape(label)}"]')

    if info.parent_rel:
        parent = infos.get(info.parent_rel)
        parent_id = mermaid_id(info.rel + ":parent")
        parent_label = f"subir: {short_label(parent.name if parent else info.parent_rel)}"
        lines.append(f'  {parent_id}["{mermaid_escape(parent_label)}"]')
        lines.append(f"  {this_id} --> {parent_id}")
        parent_target = map_target_for_dir(info.parent_rel, info.path)
        lines.append(f'  click {parent_id} "{parent_target}" "Abrir mapa superior"')

    for child_rel in info.child_dirs[:30]:
        child = infos.get(child_rel)
        if not child:
            continue
        child_id = mermaid_id(child_rel)
        child_label = f"{short_label(child.name)}\\n{child.kind}\\n{child.total_files_recursive} arquivos"
        lines.append(f'  {child_id}["{mermaid_escape(child_label)}"]')
        lines.append(f"  {this_id} --> {child_id}")
        lines.append(f'  click {child_id} "{map_target_for_dir(child_rel, info.path)}" "Abrir mapa da pasta"')

    key_files = [f for f in info.direct_files if f.role in {"regras", "comando", "mapa_indice", "regimento_lei", "plano_contexto", "peca_trabalho", "relatorio_auditoria"}][:12]
    for file_info in key_files:
        file_id = mermaid_id(info.rel + ":" + file_info.name)
        file_label = f"{short_label(file_info.name)}\\n{file_info.note}"
        lines.append(f'  {file_id}["{mermaid_escape(file_label)}"]')
        lines.append(f"  {this_id} --> {file_id}")
        lines.append(f'  click {file_id} "{rel_target(file_info.path, info.path)}" "Abrir arquivo"')

    if len(info.child_dirs) > 30:
        extra_id = mermaid_id(info.rel + ":extra")
        lines.append(f'  {extra_id}["mais {len(info.child_dirs) - 30} subpastas listadas abaixo"]')
        lines.append(f"  {this_id} --> {extra_id}")
    return "\n".join(lines)


def route_steps(info: DirInfo) -> list[str]:
    steps = [
        "Ler este `MAPA_IA.md` antes de abrir arquivos pesados.",
        "Subir para a raiz se precisar das regras globais `AGENTS.md`, `CLAUDE.md` e `_LEIS_GERAIS`.",
    ]
    roles = set(info.roles)
    names = {f.name.upper() for f in info.direct_files}
    if any(name.startswith("COMANDO_") for name in names):
        steps.insert(0, "Começar pelo `COMANDO_*` desta pasta para entender origem, pedido e pendências.")
    if "regimento_lei" in roles or any("REGIMENTO_INTERNO" in name for name in names):
        steps.append("Antes de redigir peça, identificar tribunal e ler o `REGIMENTO_INTERNO_*` local.")
        steps.append("Aplicar também `_LEIS_GERAIS/LEIA-ME.md`, Estatuto da OAB e LOMAN quando houver impacto.")
    if "fonte_documento" in roles:
        steps.append("Para fatos, datas, citações e IDs: verificar nos anexos/fontes antes de afirmar.")
    if "artefato_tecnico" in roles or "artefatos técnicos" in info.kind:
        steps.append("Usar builds, renders e QA apenas para validar entrega ou rastrear geração; não começar por eles.")
    if "gestão" in info.kind:
        steps.append("Tratar dados de WhatsApp/Gmail como triagem sanitizada; não expor conversa bruta.")
    return steps


def role_label(role: str) -> str:
    return {
        "regras": "regras",
        "comando": "comando",
        "mapa_indice": "mapa/índice",
        "regimento_lei": "regimento/lei",
        "plano_contexto": "plano/contexto",
        "peca_trabalho": "peça/trabalho",
        "relatorio_auditoria": "relatório/auditoria",
        "fonte_documento": "fonte/documento",
        "imagem_visual": "imagem/visual",
        "dados_script": "dados/script",
        "artefato_tecnico": "artefato técnico",
        "outro": "outro",
    }.get(role, role)


def escrever_com_retry(path: Path, content: str, tentativas: int = 6) -> str | None:
    """Grava tolerando bloqueio transitório do sistema de arquivos.

    Em 03/08/2026 a atualização passou a abortar com `OSError: [Errno 22]
    Invalid argument` em arquivos DIFERENTES a cada execução, sempre em pastas
    profundas. A escrita do mesmo caminho, com os mesmos parâmetros, funcionava
    quando repetida isoladamente — sinal de bloqueio momentâneo por outro
    processo (indexador, antivírus, sincronizador), e não de caminho inválido.

    Sem isto, uma varredura de 22 mil arquivos era perdida inteira por causa de
    um único arquivo travado por instantes. O erro persistente continua subindo
    depois das tentativas: o objetivo é tolerar o transitório, não esconder
    falha real."""
    for tentativa in range(tentativas):
        try:
            path.write_text(content, encoding="utf-8", newline="\n")
            return None
        except OSError as exc:
            if tentativa == tentativas - 1:
                return f"{type(exc).__name__} {exc.errno}: {path}"
            # Backoff exponencial (0,25s → 4s). Medido em 03/08/2026: com espera
            # linear curta, 33 arquivos de 2.048 falhavam; e as falhas mudavam de
            # arquivo a cada execução, caindo para 19 na rodada seguinte — perfil
            # de bloqueio por varredura de antivírus sobre escrita em massa, não
            # de caminho inválido (a escrita isolada nos mesmos arquivos sempre
            # funcionou).
            time.sleep(0.25 * (2 ** tentativa))
    return None


# Escritas que falharam mesmo depois do backoff. São repescadas ao final da
# varredura, quando a rajada que provocou o bloqueio já passou. Medido em
# 03/08/2026: as falhas mudam de arquivo a cada execução (1 numa rodada, 5 na
# seguinte), então repetir a varredura inteira não converge — repescar sim.
ADIADOS: list[tuple[Path, str]] = []


def write_if_generated(path: Path, content: str, dry_run: bool = False) -> tuple[bool, str]:
    if path.exists():
        try:
            old = path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            return False, f"erro ao ler {path}: {exc}"
        if GENERATED_MARKER not in old:
            alt = path.with_name(path.stem + "_GERADO.md")
            content = content.replace(f"# Mapa IA -", "# Mapa IA gerado -", 1)
            path = alt
            if path.exists():
                try:
                    old_alt = path.read_text(encoding="utf-8", errors="replace")
                except OSError as exc:
                    return False, f"erro ao ler {path}: {exc}"
                if GENERATED_MARKER not in old_alt:
                    return False, f"preservado mapa manual sem marcador: {path}"
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
    if dry_run:
        return True, f"dry-run: {path}"
    path.parent.mkdir(parents=True, exist_ok=True)
    falha = escrever_com_retry(path, content)
    if falha:
        # Uma varredura de 22 mil arquivos não pode ser perdida por causa de um
        # arquivo que o sistema recusou. Fica para a repescagem final; só vira
        # falha de verdade se ainda recusar depois que a rajada terminar.
        ADIADOS.append((path, content))
        return False, f"adiado para repescagem: {falha}"
    return True, str(path)


def repescar(dry_run: bool = False) -> tuple[list[str], list[str]]:
    """Reescreve, ao final, o que o sistema de arquivos recusou durante a rajada.

    Roda com paciência maior que a da varredura (até ~16 s por arquivo) porque
    aqui o custo de esperar é irrelevante: são poucos arquivos e a alternativa é
    entregar o mapa incompleto."""
    if dry_run or not ADIADOS:
        return [], []
    pendentes = list(ADIADOS)
    ADIADOS.clear()
    recuperados: list[str] = []
    falhas: list[str] = []
    for path, content in pendentes:
        falha = escrever_com_retry(path, content, tentativas=8)
        if falha:
            falhas.append(f"falha ao escrever: {falha}")
        else:
            recuperados.append(str(path))
    return recuperados, falhas


def file_table(files: list[FileInfo], from_dir: Path) -> str:
    if not files:
        return "_Sem arquivos diretos nesta pasta._\n"
    lines = ["| Arquivo | Papel | Tamanho | Modificado | Observação |", "|---|---:|---:|---:|---|"]
    for item in files:
        label = item.name
        target = rel_target(item.path, from_dir)
        note = item.note
        if item.headings:
            note += " | tópicos: " + "; ".join(item.headings[:3])
        lines.append(
            f"| {md_link(label, target)} | {role_label(item.role)} | {human_size(item.size)} | {item.modified} | {md_escape(note)} |"
        )
    return "\n".join(lines) + "\n"


def child_table(info: DirInfo, infos: dict[str, DirInfo]) -> str:
    if not info.child_dirs:
        return "_Sem subpastas diretas._\n"
    lines = ["| Subpasta | Tipo | Conteúdo | Atualização | Próximo passo |", "|---|---|---:|---:|---|"]
    for child_rel in info.child_dirs:
        child = infos[child_rel]
        target = map_target_for_dir(child_rel, info.path)
        lines.append(
            f"| {md_link(child.name, target)} | {md_escape(child.kind)} | {child.total_files_recursive} arquivos / {child.total_dirs_recursive} subpastas | {child.modified_latest or '-'} | {md_escape(child.note)} |"
        )
    return "\n".join(lines) + "\n"


def ext_summary(info: DirInfo) -> str:
    if not info.ext_counts:
        return "sem arquivos"
    parts = []
    for ext, count in list(info.ext_counts.items())[:10]:
        parts.append(f"{ext}: {count}")
    if len(info.ext_counts) > 10:
        parts.append(f"+{len(info.ext_counts) - 10} tipos")
    return ", ".join(parts)


def render_dir_map(info: DirInfo, infos: dict[str, DirInfo]) -> str:
    root_rel = rel_target(ROOT_MAP, info.path)
    protocol_rel = rel_target(SYSTEM_DIR / "PROTOCOLO_NAVEGACAO_IA.md", info.path)
    index_rel = rel_target(INDEX_MD, info.path)
    inventory_rel = rel_target(INVENTORY_JSON, info.path)
    parent_line = ""
    if info.parent_rel:
        parent = infos.get(info.parent_rel)
        parent_line = f"- Mapa superior: {md_link(parent.name if parent else info.parent_rel, map_target_for_dir(info.parent_rel, info.path))}\n"

    lines = [
        GENERATED_MARKER,
        f"# Mapa IA - {info.name}",
        "",
        f"Atualizado automaticamente em: **{now_local()}**",
        "",
        f"- Caminho: `{info.path}`",
        f"- Tipo: **{info.kind}**",
        f"- Função para navegação: {info.note}",
        f"- Conteúdo recursivo: **{info.total_files_recursive} arquivos**, **{info.total_dirs_recursive} subpastas**, **{human_size(info.size_recursive)}**",
        f"- Tipos de arquivo: {md_escape(ext_summary(info))}",
        f"- Mapa raiz: {md_link('MAPA_IA.md', root_rel)}",
        f"- Índice geral: {md_link('INDICE_GERAL_IA.md', index_rel)}",
        f"- Protocolo de navegação: {md_link('PROTOCOLO_NAVEGACAO_IA.md', protocol_rel)}",
        f"- Inventário JSON para agentes: {md_link('inventario_ia.json', inventory_rel)}",
    ]
    if parent_line:
        lines.append(parent_line.rstrip())

    lines.extend([
        "",
        "## GPS Mermaid",
        "",
        "```mermaid",
        make_mermaid(info, infos),
        "```",
        "",
        "## Ordem de leitura recomendada",
        "",
    ])
    for idx, step in enumerate(route_steps(info), start=1):
        lines.append(f"{idx}. {step}")

    lines.extend([
        "",
        "## Subpastas diretas",
        "",
        child_table(info, infos).rstrip(),
        "",
        "## Arquivos diretos",
        "",
        file_table(info.direct_files, info.path).rstrip(),
        "",
        "## Leitura por papel",
        "",
    ])
    grouped: dict[str, list[FileInfo]] = defaultdict(list)
    for item in info.direct_files:
        grouped[item.role].append(item)
    if grouped:
        for role in sorted(grouped, key=lambda r: ROLE_ORDER.get(r, 99)):
            links = ", ".join(md_link(item.name, rel_target(item.path, info.path)) for item in grouped[role])
            lines.append(f"- **{role_label(role)}**: {links}")
    else:
        lines.append("- Sem arquivos diretos.")

    lines.extend([
        "",
        "## Observações anti-alucinação",
        "",
        "- Este mapa classifica por nomes, extensões e posição na árvore; não substitui leitura de fonte primária.",
        "- Fato, citação, ID processual, prazo e jurisprudência só entram em peça depois de conferência no arquivo-fonte ou fonte oficial.",
        "- Se a pasta tiver regimento, a peça deve refletir o regimento vigente na data do protocolo.",
        "",
    ])
    return "\n".join(lines)


def render_root_index(infos: dict[str, DirInfo]) -> str:
    root_info = infos["."]
    top_dirs = [infos[rel] for rel in root_info.child_dirs]
    lines = [
        GENERATED_MARKER,
        "# MAPA_IA.md - GPS vivo da Fábrica de Melhoria de Petições",
        "",
        f"Atualizado automaticamente em: **{now_local()}**",
        "",
        "Este é o ponto de entrada para qualquer IA navegar a pasta sem perder contexto, ordem de leitura ou regras críticas.",
        "",
        "## Protocolo mínimo para qualquer agente",
        "",
        "1. Ler `AGENTS.md` e `CLAUDE.md` da raiz antes de trabalhar.",
        "2. Abrir o `MAPA_IA.md` da pasta alvo e seguir a ordem de leitura indicada.",
        "3. Em peça judicial, identificar tribunal, ler `REGIMENTO_INTERNO_<TRIBUNAL>.md` da pasta do caso e aplicar `_LEIS_GERAIS`.",
        "4. Começar por `COMANDO_*`, `MAPA_*`, `INDICE_*`, `PLANO_*`, `DOSSIE_*`, `BRIEF_*` e só depois abrir anexos pesados.",
        "5. Usar build/render/QA apenas para validar entrega, não como fonte primária de fatos.",
        "6. Marcar como `[VERIFICAR]` qualquer fato, citação, ID, prazo ou jurisprudência sem fonte conferida.",
        "",
        "## Visão macro Mermaid",
        "",
        "```mermaid",
        "flowchart TD",
        '  ROOT["Fábrica de Melhoria de Petições\\nentrada principal"]',
    ]
    for child in top_dirs:
        node = mermaid_id(child.rel)
        label = f"{short_label(child.name)}\\n{child.kind}\\n{child.total_files_recursive} arquivos"
        lines.append(f'  {node}["{mermaid_escape(label)}"]')
        lines.append(f"  ROOT --> {node}")
        lines.append(f'  click {node} "{map_target_for_dir(child.rel, ROOT)}" "Abrir mapa"')
    lines.extend([
        "```",
        "",
        "## Rotas rápidas",
        "",
        f"- Regras do agente: {md_link('AGENTS.md', 'AGENTS.md')} e {md_link('CLAUDE.md', 'CLAUDE.md')}",
        f"- Leis gerais obrigatórias: {md_link('_LEIS_GERAIS/MAPA_IA.md', '_LEIS_GERAIS/MAPA_IA.md')}",
        f"- Ferramentas visuais: {md_link('_ferramentas/MAPA_IA.md', '_ferramentas/MAPA_IA.md')}",
        f"- Gestão do escritório: {md_link('gestao_escritorio/MAPA_IA.md', 'gestao_escritorio/MAPA_IA.md')}",
        f"- Protocolo detalhado de navegação IA: {md_link('00_IA_NAVIGACAO/PROTOCOLO_NAVEGACAO_IA.md', '00_IA_NAVIGACAO/PROTOCOLO_NAVEGACAO_IA.md')}",
        f"- Inventário JSON completo: {md_link('00_IA_NAVIGACAO/dados/inventario_ia.json', '00_IA_NAVIGACAO/dados/inventario_ia.json')}",
        "",
        "## Índice de pastas",
        "",
        "| Pasta | Tipo | Conteúdo | Atualização | Função |",
        "|---|---|---:|---:|---|",
    ])
    for rel, info in sorted(infos.items(), key=lambda kv: (kv[1].depth, kv[0].casefold())):
        if rel == ".":
            continue
        indent = "&nbsp;" * 4 * max(0, info.depth - 1)
        label = indent + md_escape(info.name)
        lines.append(
            f"| {md_link(label, map_target_for_dir(rel, ROOT))} | {md_escape(info.kind)} | {info.total_files_recursive} arquivos / {info.total_dirs_recursive} subpastas | {info.modified_latest or '-'} | {md_escape(info.note)} |"
        )
    lines.extend([
        "",
        "## Comandos de manutenção",
        "",
        "- Atualizar agora: `powershell -ExecutionPolicy Bypass -File .\\ATUALIZAR_MAPA_IA.ps1`",
        "- Manter vivo em janela aberta: `powershell -ExecutionPolicy Bypass -File .\\INICIAR_MAPA_IA_VIVO.ps1`",
        "- Instalar atualização automática no Windows: `powershell -ExecutionPolicy Bypass -File .\\00_IA_NAVIGACAO\\scripts\\instalar_atualizacao_automatica.ps1`",
        "",
        "## Garantia de escopo",
        "",
        "- O sistema ignora a própria pasta `00_IA_NAVIGACAO` para não criar recursão artificial.",
        "- `MAPA_IA.md` é gerado; se um arquivo manual com esse nome existir, o gerador preserva e grava alternativa `MAPA_IA_GERADO.md`.",
        "- O mapa mostra nomes, metadados e ordem de leitura. Ele não transforma anexo em fato processual sem conferência.",
        "",
    ])
    return "\n".join(lines)


def render_protocol() -> str:
    return "\n".join([
        GENERATED_MARKER,
        "# Protocolo de Navegação IA",
        "",
        f"Atualizado automaticamente em: **{now_local()}**",
        "",
        "## Objetivo",
        "",
        "Dar a qualquer IA um GPS operacional desta pasta: onde começar, que arquivos ler, quando subir ou descer na árvore e como evitar alucinação em trabalho jurídico.",
        "",
        "## Ordem padrão",
        "",
        "1. Na raiz, ler `AGENTS.md`, `CLAUDE.md`, este protocolo e `MAPA_IA.md`.",
        "2. Escolher a pasta do caso/demanda pelo índice geral.",
        "3. Dentro da pasta alvo, ler o `MAPA_IA.md` local.",
        "4. Ler `COMANDO_DO_EMAIL.md`, `COMANDO_DO_WHATSAPP.md` ou `COMANDO_MANUAL.md`, quando houver.",
        "5. Ler mapas, índices, planos, dossiês, briefs e contexto antes de anexos pesados.",
        "6. Em peça judicial, ler regimento local e `_LEIS_GERAIS` antes de redigir.",
        "7. Verificar fontes primárias para fatos, citações, datas, IDs e jurisprudência.",
        "8. Só depois abrir peças, versões finais, relatórios, QA visual, renders e builds.",
        "",
        "## Leitura por tipo de pasta",
        "",
        "- `Anexos do email`, `Autos Drive`, `Documentos`: fonte primária ou material recebido; não resumir sem leitura.",
        "- `Links pendentes`: demanda de coleta/baixa; confirmar link antes de tratar como arquivo disponível.",
        "- `_build`, `_extract`, `render`, `QA`, `pages`, `img`: artefato técnico; útil para validar entrega, não para fundamentar fato.",
        "- `_trabalho`, `PLANEJAMENTO`, `visual_law`: produção intermediária; checar se há versão final mais recente.",
        "- `gestao_escritorio`: painel e dados operacionais; manter WhatsApp/Gmail em nível sanitizado.",
        "",
        "## Regra jurídica crítica",
        "",
        "Toda peça deve identificar tribunal, cabimento, órgão competente, prazo, sustentação oral e impactos regimentais. Se faltar regimento local, a IA deve baixar a consolidação oficial mais recente, converter integralmente para Markdown e registrar fonte/data antes de redigir.",
        "",
        "## Marcação de incerteza",
        "",
        "- `[FONTE: arquivo]`: quando a informação foi lida no arquivo indicado.",
        "- `[DECLARAÇÃO]`: quando vem de instrução do usuário ou comando, sem prova documental conferida.",
        "- `[INFERÊNCIA]`: quando é conclusão lógica a partir de fontes.",
        "- `[NÃO VERIFICADO]` ou `[VERIFICAR]`: quando ainda não há lastro suficiente para peça.",
        "",
    ])


def render_status(infos: dict[str, DirInfo]) -> str:
    total_files = infos["."].total_files_recursive
    total_dirs = len(infos)
    ext_counts = Counter(infos["."].ext_counts)
    roles = Counter(infos["."].roles)
    lines = [
        GENERATED_MARKER,
        "# Status do Mapa IA Vivo",
        "",
        f"Última atualização: **{now_local()}**",
        "",
        f"- Pastas mapeadas: **{total_dirs}**",
        f"- Arquivos mapeados: **{total_files}**",
        f"- Tamanho mapeado: **{human_size(infos['.'].size_recursive)}**",
        "",
        "## Principais tipos de arquivo",
        "",
    ]
    for ext, count in list(ext_counts.items())[:20]:
        lines.append(f"- `{ext}`: {count}")
    lines.extend(["", "## Papéis detectados", ""])
    for role, count in roles.most_common():
        lines.append(f"- {role_label(role)}: {count}")
    lines.extend(["", "## Manutenção", "", "- Atualizar manualmente: `./ATUALIZAR_MAPA_IA.ps1`", "- Observar mudanças em tempo real: `./INICIAR_MAPA_IA_VIVO.ps1`", ""])
    return "\n".join(lines)


def render_index(infos: dict[str, DirInfo]) -> str:
    return render_root_index(infos).replace("# MAPA_IA.md - GPS vivo da Fábrica de Melhoria de Petições", "# Índice Geral IA - Fábrica de Melhoria de Petições", 1)


def write_inventory(infos: dict[str, DirInfo], dry_run: bool = False) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated_at": now_local(),
        "root": str(ROOT),
        "map_name": MAP_NAME,
        "policy": {
            "anti_alucinacao": "nomes/metadados nao bastam para fato processual; verificar fonte primaria",
            "regimento": "ler regimento local e _LEIS_GERAIS antes de redigir peca judicial",
        },
        "directories": [],
    }
    for rel, info in sorted(infos.items(), key=lambda kv: kv[0].casefold()):
        payload["directories"].append(
            {
                "rel": rel,
                "path": str(info.path),
                "map": str(info.path / MAP_NAME),
                "kind": info.kind,
                "note": info.note,
                "depth": info.depth,
                "parent": info.parent_rel,
                "child_dirs": info.child_dirs,
                "files_recursive": info.total_files_recursive,
                "dirs_recursive": info.total_dirs_recursive,
                "size_recursive": info.size_recursive,
                "ext_counts": info.ext_counts,
                "roles": info.roles,
                "direct_files": [
                    {
                        "name": f.name,
                        "rel": f.rel,
                        "role": f.role,
                        "note": f.note,
                        "ext": f.ext,
                        "size": f.size,
                        "modified": f.modified,
                        "headings": f.headings,
                    }
                    for f in info.direct_files
                ],
            }
        )
    if not dry_run:
        escrever_com_retry(INVENTORY_JSON, json.dumps(payload, ensure_ascii=False, indent=2))
        tree = {
            "generated_at": payload["generated_at"],
            "root": str(ROOT),
            "children": build_tree(".", infos),
        }
        escrever_com_retry(TREE_JSON, json.dumps(tree, ensure_ascii=False, indent=2))


def build_tree(rel: str, infos: dict[str, DirInfo]) -> dict:
    info = infos[rel]
    return {
        "rel": rel,
        "name": info.name,
        "kind": info.kind,
        "files_recursive": info.total_files_recursive,
        "children": [build_tree(child, infos) for child in info.child_dirs if child in infos],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Atualiza mapas vivos de navegação IA.")
    parser.add_argument("--dry-run", action="store_true", help="calcula sem escrever arquivos")
    parser.add_argument("--quiet", action="store_true", help="reduz saída")
    args = parser.parse_args(argv)

    infos = collect()
    written: list[str] = []
    failed: list[str] = []

    for rel, info in infos.items():
        content = render_dir_map(info, infos)
        target = info.path / MAP_NAME
        ok, message = write_if_generated(target, content, args.dry_run)
        (written if ok else failed).append(message)

    for target, content in [
        (ROOT_MAP, render_root_index(infos)),
        (INDEX_MD, render_index(infos)),
        (SYSTEM_DIR / "PROTOCOLO_NAVEGACAO_IA.md", render_protocol()),
        (STATUS_MD, render_status(infos)),
    ]:
        ok, message = write_if_generated(target, content, args.dry_run)
        (written if ok else failed).append(message)

    write_inventory(infos, args.dry_run)

    # Repescagem: o que o antivírus recusou durante a rajada costuma aceitar
    # agora. As mensagens de adiamento saem da lista de falhas quando recuperadas.
    recuperados, falhas_finais = repescar(args.dry_run)
    if recuperados or falhas_finais:
        failed = [m for m in failed if not m.startswith("adiado para repescagem:")]
        written.extend(recuperados)
        failed.extend(falhas_finais)

    if not args.quiet:
        print(f"Pastas mapeadas: {len(infos)}")
        print(f"Arquivos mapeados: {infos['.'].total_files_recursive}")
        print(f"Mapas escritos: {len(written)}")
        if recuperados:
            print(f"Recuperados na repescagem: {len(recuperados)}")
        if failed:
            print("Falhas/preservações:")
            for item in failed:
                print(f"- {item}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
