# -*- coding: utf-8 -*-
"""Confere se a skill da FORJA ainda descreve a FORJA que existe no disco.

**Por que este script existe.** Uma skill é documentação que o agente segue sem
conferir a fonte — é esse o ponto dela. Isso a torna o lugar mais perigoso da
casa para uma afirmação envelhecida: quando o `AGENTS.md` do harness manda rodar
um script que foi renomeado, quem lê tenta, falha e improvisa. A regra da casa
para gates vale para documentação: **o que ninguém verifica, ninguém percebe que
quebrou.**

O que ele afere, e só isso:

- todo script `forja_*.py` citado na skill existe no disco;
- todo contrato de fase citado existe em `phase_contracts/`;
- todo template citado existe em `templates/`;
- toda referência interna `reference/<arquivo>` existe na própria skill;
- todo arquivo de referência da skill é apontado por `SKILL.md` (referência
  órfã é referência que ninguém abre — a Lição 89 na forma de documento).

O que ele **não** afere, e é bom dizer: se o texto está certo. Nenhum script
sabe se a descrição de uma fase corresponde ao que a fase faz. Isso continua
sendo leitura humana, e este verificador não é desculpa para pular a leitura —
é só a catraca que pega o erro mecânico, que é o que se repete.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

VERSAO = "FORJA-SKILL-DOCTOR-v1"

HARNESS = Path(__file__).resolve().parent
RAIZ = HARNESS.parent
SKILL_PADRAO = RAIZ / ".claude" / "skills" / "forja"

# `_FORJA_HARNESS\forja_algo.py` ou `_FORJA_HARNESS/forja_algo.py` ou `forja_algo.py`
_SCRIPT = re.compile(r"\b((?:_FORJA_HARNESS[\\/])?(?:forja|montar|compor)_[a-z0-9_]+\.py)\b")
_CONTRATO = re.compile(r"\bphase_contracts[\\/](F[0-9A-Za-z_.]+\.json)\b")
_TEMPLATE = re.compile(r"\btemplates[\\/]([A-Za-z0-9_.\-]+\.md)\b")
_REFERENCIA = re.compile(r"\breference[\\/]([A-Za-z0-9_.\-]+\.md)\b")
# Scripts que vivem em _FERRAMENTAS, não no harness.
_FERRAMENTAS = {"montar_visual.py", "word_visual_pipeline.py", "forja_visual.py",
                "medina_svg_kit.py", "medina_visual_kit.py", "estilo_medina.py"}


def _texto_da_skill(base: Path) -> dict[str, str]:
    """{caminho relativo: conteúdo} de SKILL.md e de tudo em reference/."""
    arquivos = {}
    skill = base / "SKILL.md"
    if skill.exists():
        arquivos["SKILL.md"] = skill.read_text(encoding="utf-8")
    ref = base / "reference"
    if ref.is_dir():
        for f in sorted(ref.glob("*.md")):
            arquivos[f"reference/{f.name}"] = f.read_text(encoding="utf-8")
    return arquivos


def _sem_bloco_de_codigo_negativo(texto: str) -> str:
    """Remove os trechos marcados como exemplo do que NÃO fazer.

    A skill cita, de propósito, nomes de coisas que não existem mais — é assim
    que ela impede o agente de procurá-las. Esses trechos ficam entre
    `<!-- doctor:ignora -->` e `<!-- /doctor:ignora -->`.
    """
    return re.sub(r"<!--\s*doctor:ignora\s*-->.*?<!--\s*/doctor:ignora\s*-->",
                  "", texto, flags=re.S)


def auditar(base: Path) -> dict:
    arquivos = _texto_da_skill(base)
    achados = []

    if not arquivos:
        return {"schemaVersion": 1, "versao": VERSAO, "skill": str(base),
                "aprovado": False,
                "findings": [{"gate": "DOC0-skill-inexistente", "sev": "P0",
                              "problema": f"não há SKILL.md em {base}"}],
                "conferidos": {}}

    scripts_citados, contratos, templates, referencias = set(), set(), set(), set()
    for nome, bruto in arquivos.items():
        texto = _sem_bloco_de_codigo_negativo(bruto)
        for m in _SCRIPT.finditer(texto):
            scripts_citados.add((Path(m.group(1)).name, nome))
        for m in _CONTRATO.finditer(texto):
            contratos.add((m.group(1), nome))
        for m in _TEMPLATE.finditer(texto):
            templates.add((m.group(1), nome))
        for m in _REFERENCIA.finditer(texto):
            referencias.add((m.group(1), nome))

    for script, onde in sorted(scripts_citados):
        if script in _FERRAMENTAS:
            existe = (RAIZ / "_FERRAMENTAS" / script).exists()
            local = "_FERRAMENTAS"
        else:
            existe = (HARNESS / script).exists()
            local = "_FORJA_HARNESS"
        if not existe:
            achados.append({
                "gate": "DOC1-script-inexistente", "sev": "P0", "arquivo": onde,
                "problema": f"a skill manda usar {script}, que não existe em {local}",
                "acao": "conferir se foi renomeado ou removido, e corrigir a skill"})

    for contrato, onde in sorted(contratos):
        if not (HARNESS / "phase_contracts" / contrato).exists():
            achados.append({
                "gate": "DOC2-contrato-inexistente", "sev": "P0", "arquivo": onde,
                "problema": f"contrato de fase citado e ausente: {contrato}"})

    for template, onde in sorted(templates):
        if not (HARNESS / "templates" / template).exists():
            achados.append({
                "gate": "DOC3-template-inexistente", "sev": "P1", "arquivo": onde,
                "problema": f"template citado e ausente: {template}"})

    for referencia, onde in sorted(referencias):
        if f"reference/{referencia}" not in arquivos:
            achados.append({
                "gate": "DOC4-referencia-quebrada", "sev": "P0", "arquivo": onde,
                "problema": f"aponta para reference/{referencia}, que não existe"})

    # Referência que existe e ninguém abre.
    apontadas = {r for r, _ in referencias}
    for nome in arquivos:
        if not nome.startswith("reference/"):
            continue
        alvo = nome.split("/", 1)[1]
        if alvo not in apontadas:
            achados.append({
                "gate": "DOC5-referencia-orfa", "sev": "P1", "arquivo": nome,
                "problema": "existe em reference/ e nenhum documento da skill aponta para ela",
                "acao": "apontar a partir do SKILL.md ou remover"})

    # Frontmatter mínimo: sem name e description a skill não é descoberta.
    cabecalho = arquivos.get("SKILL.md", "")[:1200]
    for campo in ("name:", "description:"):
        if campo not in cabecalho:
            achados.append({
                "gate": "DOC6-frontmatter-incompleto", "sev": "P0", "arquivo": "SKILL.md",
                "problema": f"falta `{campo}` no frontmatter"})

    p0 = sum(1 for a in achados if a["sev"] == "P0")
    return {
        "schemaVersion": 1, "versao": VERSAO, "skill": str(base),
        "aprovado": p0 == 0,
        "conferidos": {
            "arquivos": len(arquivos),
            "scriptsCitados": len({s for s, _ in scripts_citados}),
            "contratosCitados": len({c for c, _ in contratos}),
            "templatesCitados": len({t for t, _ in templates}),
            "referenciasCitadas": len(apontadas),
        },
        "p0": p0, "p1": sum(1 for a in achados if a["sev"] == "P1"),
        "findings": achados,
    }


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Confere se a skill da FORJA ainda bate com o disco.")
    ap.add_argument("--skill", default=str(SKILL_PADRAO),
                    help="pasta da skill (padrão: .claude/skills/forja)")
    ap.add_argument("--json", action="store_true", help="saída em JSON")
    args = ap.parse_args()

    r = auditar(Path(args.skill))
    if args.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0 if r["aprovado"] else 1

    c = r["conferidos"]
    print(f"{VERSAO} — {r['skill']}")
    if c:
        print(f"  {c['arquivos']} arquivo(s) · {c['scriptsCitados']} script(s) citado(s) · "
              f"{c['contratosCitados']} contrato(s) · {c['referenciasCitadas']} referência(s)")
    for a in r["findings"]:
        print(f"  [{a['sev']}] {a['gate']} ({a.get('arquivo','-')}): {a['problema']}")
    print("  APROVADO" if r["aprovado"] else f"  REPROVADO — {r['p0']} P0")
    return 0 if r["aprovado"] else 1


if __name__ == "__main__":
    sys.exit(main())
