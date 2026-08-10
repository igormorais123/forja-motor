# -*- coding: utf-8 -*-
"""forja_estado_orfao.py — devolve estado legível a pasta de caso que perdeu o seu.

Uma pasta em `state/` sem arquivo de estado deixa o censo incompleto, e censo
incompleto invalida **todo** número derivado dele: não se pode dizer "55
entregues" sobre uma população que não se conseguiu ler inteira. Em 10/08/2026
eram duas pastas em 91, ambas com artefato real dentro — trabalho feito cujo
registro nunca foi escrito.

A reconstrução obedece a uma regra única: **só afirma o que está no disco.**
Ela lê os artefatos da pasta, deduz a fase mais avançada que eles comprovam e
grava isso. Não inventa entrega, não carimba `fulfilled`, não inventa prazo. Se
os artefatos não comprovarem nada, o estado nasce `aberto`, que é a verdade.

Todo estado reconstruído carrega `reconstruido`, com a data, o que foi lido e a
advertência de que ele descreve o disco e não a história do caso — os eventos
que não foram gravados na época não voltam, e fingir que voltaram seria pior do
que a lacuna.

Uso
    python forja_estado_orfao.py --listar
    python forja_estado_orfao.py --caso case-<id-da-pasta>
    python forja_estado_orfao.py --todos
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

FORJA = Path(__file__).resolve().parent
STATE = FORJA / "state"

VERSAO = "FORJA-ESTADO-ORFAO-v1"

# O que cada artefato prova sobre onde o caso parou. A ordem é a da esteira: a
# fase gravada é a mais avançada entre as comprovadas, nunca a mais otimista
# entre as possíveis.
PROVAS = (
    ("F1_INSUMO_BLOQUEADO.json", "F1_INGESTAO_AUTOS", "blocked",
     "há insumo bloqueado declarado, com causa e diligências"),
    ("F2_QUESTION_TREE.json", "F2A_EXPLORACAO_PROBLEMA_100_PERGUNTAS", "in_progress",
     "a exploração inicial foi materializada"),
    ("F4.json", "F4_BLUEPRINT_CONSELHO", "in_progress",
     "há blueprint com parecer do conselho"),
    ("f7_gate_result.json", "F7_AUDITORIA_JURIDICA_FACTUAL", "draft_awaiting_review",
     "a auditoria factual rodou e deixou veredito"),
)


def _agora() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def orfaos(raiz: Path = STATE) -> list[Path]:
    """Pastas de caso sem nenhum dos dois arquivos de estado.

    O recorte `case-*` é o mesmo do censo, de propósito: `state/` também guarda
    pasta que não é caso (`prd44-revisao`, por exemplo), e reconstruir estado
    para elas inventaria caso onde não há.
    """
    achados = []
    for d in sorted(p for p in raiz.glob("case-*") if p.is_dir()):
        if (d / "FORJA_STATE.json").is_file() or (d / "FORJA_N3_STATE.json").is_file():
            continue
        achados.append(d)
    return achados


def _ler(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError):
        return None


def evidencia(case_dir: Path) -> tuple[str, str, list[dict]]:
    """(fase, status, artefatos lidos) — tudo derivado do que existe na pasta."""
    fase, status, lidos = "F0_INGESTAO_TRIAGEM", "aberto", []
    for nome, f, s, porque in PROVAS:
        for achado in case_dir.rglob(nome):
            dados = _ler(achado)
            item = {"arquivo": str(achado.relative_to(case_dir)).replace("\\", "/"),
                    "prova": porque, "legivel": dados is not None}
            if dados and nome == "f7_gate_result.json":
                # O veredito do próprio gate manda; ele é mais específico do que
                # a mera presença do arquivo.
                item["status"] = dados.get("status")
                s = dados.get("status") or s
            lidos.append(item)
            fase, status = f, s
    return fase, status, lidos


def reconstruir(case_dir: Path, seco: bool = False) -> dict:
    fase, status, lidos = evidencia(case_dir)
    estado = {
        "caseId": case_dir.name,
        "specVersion": VERSAO,
        "createdAt": _agora(),
        "updatedAt": _agora(),
        "currentPhase": fase,
        "status": status,
        "inputs": {},
        "phaseHistory": [{"phase": fase, "at": _agora(), "status": status}],
        "artifacts": [i["arquivo"] for i in lidos],
        "gates": {},
        "deliveryEvidence": None,
        "reconstruido": {
            "em": _agora(),
            "por": VERSAO,
            "lido": lidos,
            "advertencia": (
                "Estado reconstruído a partir dos artefatos em disco, e não da "
                "história do caso. Os eventos que não foram gravados na época "
                "não voltam: datas de fase, gates anteriores e trilha de decisão "
                "estão ausentes de propósito. Nenhuma entrega é afirmada aqui — "
                "se houve, precisa ser declarada por quem a fez."),
        },
    }
    if not seco:
        (case_dir / "FORJA_STATE.json").write_text(
            json.dumps(estado, ensure_ascii=False, indent=2), encoding="utf-8")
    return estado


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--listar", action="store_true", help="só mostrar os órfãos")
    p.add_argument("--caso", help="reconstruir um caso pelo nome da pasta")
    p.add_argument("--todos", action="store_true", help="reconstruir todos os órfãos")
    p.add_argument("--seco", action="store_true", help="mostrar sem gravar")
    a = p.parse_args(argv)

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    achados = orfaos()
    if a.listar or not (a.caso or a.todos):
        if not achados:
            print("Nenhuma pasta de caso sem estado. O censo consegue ler a população inteira.")
            return 0
        for d in achados:
            fase, status, lidos = evidencia(d)
            print(f"  {d.name}\n      seria {status} em {fase}, por {len(lidos)} artefato(s)")
        print(f"\n{len(achados)} pasta(s) sem estado. Enquanto existirem, o censo é "
              f"incompleto e nenhum número dele é retrato da população.")
        return 1

    alvos = achados if a.todos else [STATE / a.caso]
    for d in alvos:
        if not d.is_dir():
            print(f"pasta inexistente: {d.name}")
            return 2
        estado = reconstruir(d, seco=a.seco)
        marca = "(seco) " if a.seco else ""
        print(f"{marca}{d.name}: {estado['status']} em {estado['currentPhase']}, "
              f"por {len(estado['reconstruido']['lido'])} artefato(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
