# -*- coding: utf-8 -*-
"""Métricas agregadas de gates e fases (M1.3 do plano 19).

Varre state/*/FORJA_STATE.json + FORJA_N3_STATE.json e agrega o que hoje só
existe por caso: qual gate mais derruba, tempo médio por fase, P0/P1 abertos,
casos por status. Saída: reports/METRICAS_GATES.json (consumido pelo painel)
+ tabela legível.

Uso: python forja_metricas_gates.py [--quiet]
"""
import io
import json
import os
import sys
from collections import Counter, defaultdict
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
RAIZ = os.path.dirname(os.path.abspath(__file__))
STATE_DIR = os.path.join(RAIZ, "state")
SAIDA = os.path.join(RAIZ, "reports", "METRICAS_GATES.json")

FASES = ["F0", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10"]


def _fase(nome):
    import re
    m = re.match(r"^(F\d{1,2})", str(nome or ""))
    return m.group(1) if m and m.group(1) in FASES else None


def _ts(texto):
    try:
        return datetime.fromisoformat(texto)
    except (ValueError, TypeError):
        return None


def _ler(caminho):
    try:
        with open(caminho, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return None


def coletar():
    por_gate = Counter()
    casos_por_gate = defaultdict(set)
    severidade_por_gate = defaultdict(Counter)
    duracao_fase = defaultdict(list)   # fase -> [horas até a transição seguinte]
    status_casos = Counter()
    abertos = {"P0": [], "P1": []}
    ilegiveis = []

    if not os.path.isdir(STATE_DIR):
        return None

    for nome in sorted(os.listdir(STATE_DIR)):
        pasta = os.path.join(STATE_DIR, nome)
        if not os.path.isdir(pasta) or not nome.startswith("case-"):
            continue
        n2 = _ler(os.path.join(pasta, "FORJA_STATE.json"))
        n3 = _ler(os.path.join(pasta, "FORJA_N3_STATE.json"))
        if n2 is None and n3 is None:
            ilegiveis.append(nome)
            continue

        status = (n2 or {}).get("status") or (n3 or {}).get("lifecycleStatus") or "desconhecido"
        status_casos[status] += 1

        # frequência de queda por gate (N2 gates[] + N3 blockers[])
        vistos = set()
        for g in (n2 or {}).get("gates") or []:
            chave = (g.get("code"), g.get("detail"))
            if chave in vistos:
                continue
            vistos.add(chave)
            gate = g.get("code") or "?"
            sev = g.get("severity") or "P1"
            por_gate[gate] += 1
            casos_por_gate[gate].add(nome)
            severidade_por_gate[gate][sev] += 1
            if status != "fulfilled" and sev in ("P0", "P1"):
                abertos[sev if sev == "P0" else "P1"].append(
                    {"caso": nome, "gate": gate, "detalhe": str(g.get("detail"))[:120]})
        for b in (n3 or {}).get("blockers") or []:
            chave = (b.get("gate"), b.get("reason"))
            if chave in vistos:
                continue
            vistos.add(chave)
            gate = b.get("gate") or "?"
            sev = b.get("severity") or "P1"
            por_gate[gate] += 1
            casos_por_gate[gate].add(nome)
            severidade_por_gate[gate][sev] += 1
            if status != "fulfilled":
                abertos[sev if sev == "P0" else "P1"].append(
                    {"caso": nome, "gate": gate, "detalhe": str(b.get("reason"))[:120]})

        # tempo por fase: delta entre entradas consecutivas do phaseHistory
        hist = [(_fase(h.get("phase")), _ts(h.get("at")))
                for h in (n2 or {}).get("phaseHistory") or []]
        hist = [(f, t) for f, t in hist if f and t]
        for (f_a, t_a), (_f_b, t_b) in zip(hist, hist[1:]):
            horas = (t_b - t_a).total_seconds() / 3600
            if 0 <= horas <= 24 * 14:  # descarta deltas absurdos (reconcile tardio)
                duracao_fase[f_a].append(horas)

    ranking = [{"gate": g, "quedas": n, "casos": len(casos_por_gate[g]),
                "severidades": dict(severidade_por_gate[g])}
               for g, n in por_gate.most_common()]
    tempos = {f: {"mediaHoras": round(sum(v) / len(v), 2), "amostras": len(v)}
              for f, v in sorted(duracao_fase.items()) if v}

    return {
        "generatedAt": datetime.now().astimezone().isoformat(timespec="seconds"),
        "topFallingGate": ranking[0]["gate"] if ranking else None,
        "rankingGates": ranking,
        "tempoMedioPorFase": tempos,
        "casosPorStatus": dict(status_casos),
        "abertos": abertos,
        "casosIlegiveis": ilegiveis,
    }


def main(argv=None):
    argv = argv or sys.argv[1:]
    m = coletar()
    if m is None:
        print("state/ não encontrado")
        return 1
    os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
    tmp = SAIDA + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(m, f, ensure_ascii=False, indent=1)
    os.replace(tmp, SAIDA)

    if "--quiet" not in argv:
        print(f"Métricas de gates ({m['generatedAt']}) -> {SAIDA}")
        print(f"Casos por status: {m['casosPorStatus']}")
        print("| gate | quedas | casos | severidades |")
        print("|---|---|---|---|")
        for r in m["rankingGates"][:10]:
            print(f"| {r['gate']} | {r['quedas']} | {r['casos']} | {r['severidades']} |")
        print("| fase | média (h) | amostras |")
        print("|---|---|---|")
        for f, v in m["tempoMedioPorFase"].items():
            print(f"| {f} | {v['mediaHoras']} | {v['amostras']} |")
        if m["abertos"]["P0"]:
            print(f"P0 ABERTOS: {json.dumps(m['abertos']['P0'], ensure_ascii=False)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
