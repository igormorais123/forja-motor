# -*- coding: utf-8 -*-
"""Espalha a skill da FORJA para os carregadores de skill deste PC.

**Por que é script e não cópia à mão.** A skill canônica vive no projeto da
fábrica, e é lá que ela é editada e conferida. Os agentes, porém, procuram skill
em quatro lugares diferentes — Claude, Codex, Cursor e Hermes —, e uma cópia
feita à mão envelhece em silêncio: ninguém sabe dizer qual das cinco está certa.
Aqui a canônica é uma só, e as cópias são derivadas conferíveis por hash. É a
Lição 87 aplicada à documentação: recurso que depende de esforço manual por vez
não sobrevive ao volume.

**O que a cópia ganha e o repositório não pode ter.** A skill canônica não diz
onde a fábrica está no disco, e não pode dizer: caminho de instalação é
informação específica desta máquina e a fronteira motor/acervo o proíbe no
motor. Mas uma skill global é lida por um agente que pode estar em qualquer
diretório, e sem o caminho ela manda rodar comandos que não existem ali. Por
isso o carimbo de localização é gerado **aqui**, na cópia, e nunca no original.

Uso:
    python forja_skill_deploy.py            # espalha e confere
    python forja_skill_deploy.py --seco     # mostra o que faria
    python forja_skill_deploy.py --verificar  # as cópias ainda batem com a canônica?
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path

VERSAO = "FORJA-SKILL-DEPLOY-v1"

HARNESS = Path(__file__).resolve().parent
RAIZ = HARNESS.parent
CANONICA = RAIZ / ".claude" / "skills" / "forja"

# Onde cada agente procura skill neste PC. O nome é o do carregador, não o do
# modelo: o Codex lê `.agents/skills`, e é por isso que ele aparece com esse
# caminho e não com um `.codex`.
DESTINOS = {
    "Claude": Path.home() / ".claude" / "skills" / "forja",
    "Codex": Path.home() / ".agents" / "skills" / "forja",
    "Cursor": Path.home() / ".cursor" / "skills" / "forja",
    "Hermes": Path.home() / ".hermes" / "skills" / "forja",
}

_MARCA_INICIO = "<!-- forja:instalacao -->"
_MARCA_FIM = "<!-- /forja:instalacao -->"


def _carimbo(destino_nome: str) -> str:
    """O bloco que diz ao agente global onde a fábrica está.

    Fica logo depois do frontmatter, porque é a primeira coisa que decide se os
    comandos abaixo são executáveis. `doctor:ignora` envolve o trecho para que o
    verificador não tente resolver o caminho absoluto como script do harness.
    """
    return (
        f"{_MARCA_INICIO}\n"
        f"> **Instalação local** — bloco gerado por `forja_skill_deploy.py` para a cópia\n"
        f"> do {destino_nome}; ele não existe na skill canônica, porque caminho de\n"
        f"> instalação não entra no repositório do motor.\n"
        f">\n"
        f"> A fábrica está em `{RAIZ}`.\n"
        f"> Todo comando desta skill roda de dentro de `_FORJA_HARNESS`, ali dentro.\n"
        f"> A skill canônica — a que se edita e se confere — é\n"
        f"> `{CANONICA}`. **Não edite esta cópia:** rode\n"
        f"> `python forja_skill_deploy.py` depois de alterar a canônica.\n"
        f"{_MARCA_FIM}\n"
    )


def _sem_carimbo(texto: str) -> str:
    """Remove um carimbo anterior, para que reaplicar não empilhe blocos."""
    return re.sub(re.escape(_MARCA_INICIO) + r".*?" + re.escape(_MARCA_FIM) + r"\n?",
                  "", texto, flags=re.S)


def _com_carimbo(texto: str, destino_nome: str) -> str:
    texto = _sem_carimbo(texto)
    # Depois do frontmatter fechado: a segunda ocorrência de uma linha `---`.
    m = re.match(r"^---\n.*?\n---\n", texto, flags=re.S)
    if not m:
        return _carimbo(destino_nome) + "\n" + texto
    corte = m.end()
    return texto[:corte] + "\n" + _carimbo(destino_nome) + texto[corte:]


def _sha(texto: str) -> str:
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()[:12]


def _arquivos_da_canonica() -> dict[str, str]:
    """{caminho relativo: conteúdo} — SKILL.md e reference/*.md."""
    saida = {}
    skill = CANONICA / "SKILL.md"
    if skill.exists():
        saida["SKILL.md"] = skill.read_text(encoding="utf-8")
    ref = CANONICA / "reference"
    if ref.is_dir():
        for f in sorted(ref.glob("*.md")):
            # Artefato derivado do observador. Cada carregador recebe contexto
            # próprio, portanto o mapa não integra a skill nem o hash canônico.
            if f.name == "MAPA_IA.md":
                continue
            saida[f"reference/{f.name}"] = f.read_text(encoding="utf-8")
    return saida


def espalhar(seco: bool = False, apenas_verificar: bool = False) -> dict:
    origem = _arquivos_da_canonica()
    if not origem:
        return {"schemaVersion": 1, "versao": VERSAO, "ok": False,
                "erro": f"não encontrei a skill canônica em {CANONICA}", "destinos": []}

    relatorio = []
    for nome, base in DESTINOS.items():
        esperado = {rel: (_com_carimbo(txt, nome) if rel == "SKILL.md" else txt)
                    for rel, txt in origem.items()}
        escritos, iguais, divergentes, sobrando = [], [], [], []

        for rel, conteudo in esperado.items():
            alvo = base / rel
            atual = alvo.read_text(encoding="utf-8") if alvo.exists() else None
            if atual == conteudo:
                iguais.append(rel)
                continue
            divergentes.append(rel)
            if seco or apenas_verificar:
                continue
            alvo.parent.mkdir(parents=True, exist_ok=True)
            alvo.write_text(conteudo, encoding="utf-8")
            escritos.append(rel)

        # Arquivo que sobrou de uma versão anterior da skill: some da canônica e
        # fica na cópia dizendo coisa que ninguém mais mantém.
        if base.exists():
            for f in sorted(base.rglob("*.md")):
                if f.name == "MAPA_IA.md":
                    continue
                rel = f.relative_to(base).as_posix()
                if rel not in esperado:
                    sobrando.append(rel)
                    if not (seco or apenas_verificar):
                        f.unlink()

        relatorio.append({
            "destino": nome, "caminho": str(base),
            "iguais": len(iguais), "atualizados": len(divergentes),
            "escritos": len(escritos), "removidos": sobrando,
            "emDia": not divergentes and not sobrando,
        })

    tudo_em_dia = all(d["emDia"] for d in relatorio)
    return {
        "schemaVersion": 1, "versao": VERSAO,
        "canonica": str(CANONICA),
        "arquivos": len(origem),
        "hashCanonica": _sha("".join(origem[k] for k in sorted(origem))),
        "ok": tudo_em_dia if apenas_verificar else True,
        "destinos": relatorio,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--seco", action="store_true",
                    help="mostra o que faria, sem escrever")
    ap.add_argument("--verificar", action="store_true",
                    help="só confere se as cópias batem com a canônica")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    r = espalhar(seco=args.seco, apenas_verificar=args.verificar)
    if args.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0 if r["ok"] else 1

    if not r.get("destinos"):
        print(f"{VERSAO} — ERRO: {r.get('erro')}")
        return 1
    print(f"{VERSAO} — canônica: {r['arquivos']} arquivo(s), hash {r['hashCanonica']}")
    for d in r["destinos"]:
        estado = "em dia" if d["emDia"] else (
            f"{d['atualizados']} a atualizar" if (args.seco or args.verificar)
            else f"{d['escritos']} escrito(s)")
        print(f"  {d['destino']:8} {estado}"
              + (f" · removidos: {', '.join(d['removidos'])}" if d["removidos"] else ""))
    if args.verificar and not r["ok"]:
        print("  DESATUALIZADO — rode `python forja_skill_deploy.py`")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
