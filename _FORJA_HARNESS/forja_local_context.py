# -*- coding: utf-8 -*-
"""LocalContext da FORJA (M1.2 do plano 19) — hook SessionStart.

Injeta no início da sessão um resumo vivo da fila: casos não concluídos com
fase e idade, bloqueadores P0/P1 abertos e entregas da semana, lendo
state/*/FORJA_STATE.json diretamente. Fail-open: qualquer erro imprime aviso
curto e sai 0, nunca bloqueia a sessão.

Registrado em _FORJA_HARNESS/.claude/settings.json (SessionStart, timeout 5s).
"""
import io
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
AQUI = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(AQUI, "state")
FASES = ["F0", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10"]


def _fase(nome):
    m = re.match(r"^(F\d{1,2})", str(nome or ""))
    return m.group(1) if m and m.group(1) in FASES else None


def _ts(texto):
    try:
        return datetime.fromisoformat(texto)
    except (ValueError, TypeError):
        return None


def _caso(pasta):
    try:
        with open(os.path.join(pasta, "FORJA_STATE.json"), encoding="utf-8-sig") as f:
            n2 = json.load(f)
    except (OSError, json.JSONDecodeError):
        return None
    status = n2.get("status") or "pending"
    hist = [_fase(h.get("phase")) for h in n2.get("phaseHistory") or []]
    hist = [f for f in hist if f]
    # caso concluído mostra a MAIOR fase alcançada (o reconcile reabre F0 — lição 75)
    fase = (max(hist, key=FASES.index) if status == "fulfilled" and hist
            else (hist[-1] if hist else _fase(n2.get("currentPhase")) or "F0"))
    gates = n2.get("gates") or []
    atualizado = _ts(n2.get("updatedAt"))
    idade = None
    if atualizado:
        ref = atualizado if atualizado.tzinfo else atualizado.replace(tzinfo=timezone.utc)
        idade = (datetime.now(timezone.utc) - ref).total_seconds() / 3600
    return {
        "caseId": os.path.basename(pasta),
        "demandId": (n2.get("inputs") or {}).get("demandId") or "",
        "fase": fase, "status": status,
        "p0": [g for g in gates if g.get("severity") == "P0"],
        "p1": [g for g in gates if g.get("severity") != "P0"],
        "idadeHoras": idade,
        "atualizado": atualizado,
    }


def main():
    casos = []
    for nome in sorted(os.listdir(STATE)):
        pasta = os.path.join(STATE, nome)
        if os.path.isdir(pasta) and nome.startswith("case-"):
            c = _caso(pasta)
            if c:
                casos.append(c)
    ativos = [c for c in casos if c["status"] not in ("fulfilled",)]
    limite = datetime.now(timezone.utc) - timedelta(days=7)
    entregues_7d = sum(1 for c in casos if c["status"] == "fulfilled" and c["atualizado"]
                       and (c["atualizado"] if c["atualizado"].tzinfo
                            else c["atualizado"].replace(tzinfo=timezone.utc)) >= limite)

    print("## FORJA — estado da fila (forja_local_context)")
    print(f"- casos: {len(casos)} | ativos: {len(ativos)} | entregues 7d: {entregues_7d}")
    for c in sorted(ativos, key=lambda c: (not c["p0"], c["fase"])):
        marca = " **P0**" if c["p0"] else ""
        idade = (f", {c['idadeHoras']:.0f}h parado"
                 if c["idadeHoras"] and c["idadeHoras"] > 24 else "")
        print(f"- [{c['fase']}] {c['demandId'][:70]} "
              f"({c['status']}{marca}, {len(c['p1'])} P1{idade})")
        for b in c["p0"]:
            print(f"  - P0 {b.get('code')}: {str(b.get('detail'))[:100]}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # fail-open: hook nunca bloqueia a sessão
        print(f"## FORJA — LocalContext indisponível ({type(exc).__name__}: {exc})")
    sys.exit(0)
