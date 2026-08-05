# -*- coding: utf-8 -*-
"""Alerta proativo de P0 (M1.1 do plano 19).

Quando um gate derruba um caso com P0, o estado registrava e o processo parava
sem avisar ninguém. Este módulo publica o alerta onde o Igor já olha — o painel
de gestão (comentário na demanda via intervencoes_manuais.json) — e mantém um
log global de auditoria. Tudo fail-open: falha de canal nunca quebra o
pipeline; o alerta cai em ALERTAS_PENDENTES.jsonl do caso e o próximo sync drena.

Anti-ruído: deduplicação por (caseId, gate) em janela de 6h; resolução de
bloqueador emite uma única notificação.

Uso programático:
    from forja_alertas import notificar_p0, notificar_resolucao
    notificar_p0(case_dir, gate="G7-datas", motivo="prazo contado com sábado", origem="forja_delivery")

Uso CLI (drenar pendentes de um caso): python forja_alertas.py --drenar <case_dir>
"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
GESTAO_SCRIPTS = RAIZ.parent / "gestao_escritorio" / "scripts"
MANUAL_JSON = RAIZ.parent / "gestao_escritorio" / "data" / "intervencoes_manuais.json"
LOG_GLOBAL = RAIZ / "reports" / "ALERTAS_P0.jsonl"
JANELA_DEDUP = timedelta(hours=6)


def _now():
    return datetime.now().astimezone()


def _now_iso():
    return _now().isoformat(timespec="seconds")


def _registro_enviados(case_dir: Path) -> Path:
    return Path(case_dir) / "ALERTAS_ENVIADOS.json"


def _pendentes(case_dir: Path) -> Path:
    return Path(case_dir) / "ALERTAS_PENDENTES.jsonl"


def _ler_json(path: Path, fallback):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return fallback


def _dedup_ok(case_dir: Path, chave: str) -> bool:
    """True se pode notificar (fora da janela de 6h)."""
    reg = _ler_json(_registro_enviados(case_dir), {})
    ultimo = reg.get(chave)
    if not ultimo:
        return True
    try:
        return _now() - datetime.fromisoformat(ultimo) >= JANELA_DEDUP
    except ValueError:
        return True


def _marcar_enviado(case_dir: Path, chave: str):
    path = _registro_enviados(case_dir)
    reg = _ler_json(path, {})
    reg[chave] = _now_iso()
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8")
    os.replace(tmp, path)


def _log_global(evento: dict):
    LOG_GLOBAL.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_GLOBAL, "a", encoding="utf-8") as f:
        f.write(json.dumps(evento, ensure_ascii=False) + "\n")


def _demand_id_do_caso(case_dir: Path) -> str | None:
    for nome in ("FORJA_STATE.json", "FORJA_N3_STATE.json"):
        dados = _ler_json(Path(case_dir) / nome, {})
        did = dados.get("demandId") or (dados.get("inputs") or {}).get("demandId")
        if did:
            return did
    return None


def _comentar_no_painel(demand_id: str, texto: str) -> bool:
    """Comentário na demanda do painel de gestão (canal visível ao Igor).

    Usa o lock interprocesso do office_io quando disponível; sem ele, escrita
    atômica simples. Retorna False em qualquer falha (chamador faz fallback)."""
    try:
        if not MANUAL_JSON.parent.is_dir():
            return False
        lock_ctx = None
        try:
            sys.path.insert(0, str(GESTAO_SCRIPTS))
            from office_io import InterProcessLock  # type: ignore
            lock_ctx = InterProcessLock(MANUAL_JSON.with_suffix(".lock"))
        except Exception:
            lock_ctx = None

        def _aplicar():
            manual = _ler_json(MANUAL_JSON, {"schema": 1, "updatedAt": _now_iso(), "items": {}})
            entry = manual.setdefault("items", {}).setdefault(
                demand_id, {"comentarios": [], "overrides": {}})
            entry.setdefault("comentarios", []).append({
                "id": f"forja-p0-{int(_now().timestamp() * 1000)}",
                "at": _now_iso(),
                "tipo": "forja-p0",
                "texto": texto,
                "autor": "FORJA",
            })
            entry["updatedAt"] = _now_iso()
            manual["updatedAt"] = _now_iso()
            tmp = MANUAL_JSON.with_suffix(".tmp")
            tmp.write_text(json.dumps(manual, ensure_ascii=False, indent=2), encoding="utf-8")
            os.replace(tmp, MANUAL_JSON)

        if lock_ctx is not None:
            with lock_ctx:
                _aplicar()
        else:
            _aplicar()
        return True
    except Exception:
        return False


def _emitir(case_dir: Path, evento: dict, chave_dedup: str) -> dict:
    case_dir = Path(case_dir)
    if not _dedup_ok(case_dir, chave_dedup):
        return {"status": "deduplicado", "chave": chave_dedup}

    demand_id = evento.get("demandId") or _demand_id_do_caso(case_dir)
    evento["demandId"] = demand_id

    try:
        _log_global(evento)
    except Exception:
        pass

    entregue = False
    if demand_id:
        entregue = _comentar_no_painel(demand_id, evento["texto"])

    if entregue:
        _marcar_enviado(case_dir, chave_dedup)
        return {"status": "notificado", "canal": "painel", "demandId": demand_id}

    # fallback durável: o próximo sync/drenagem entrega
    try:
        with open(_pendentes(case_dir), "a", encoding="utf-8") as f:
            f.write(json.dumps(evento, ensure_ascii=False) + "\n")
        _marcar_enviado(case_dir, chave_dedup)
        return {"status": "pendente", "arquivo": str(_pendentes(case_dir))}
    except Exception as exc:
        return {"status": "falha", "erro": f"{type(exc).__name__}: {exc}"}


def notificar_p0(case_dir, gate: str, motivo: str, origem: str = "",
                 demand_id: str | None = None) -> dict:
    """Notifica um bloqueador P0. P1/P2 são ignorados por contrato (anti-ruído)."""
    caso = os.path.basename(str(case_dir))
    evento = {
        "at": _now_iso(),
        "tipo": "p0",
        "caseId": caso,
        "demandId": demand_id,
        "gate": gate,
        "motivo": (motivo or "")[:500],
        "origem": origem,
        "texto": f"[FORJA P0] Gate {gate} derrubou o caso {caso}"
                 f"{' (' + origem + ')' if origem else ''}: {(motivo or '')[:300]}",
    }
    return _emitir(case_dir, evento, chave_dedup=f"p0:{gate}")


def notificar_resolucao(case_dir, gate: str, demand_id: str | None = None) -> dict:
    """Notificação única de bloqueador resolvido (reaquecimento do metal)."""
    caso = os.path.basename(str(case_dir))
    evento = {
        "at": _now_iso(),
        "tipo": "p0_resolvido",
        "caseId": caso,
        "demandId": demand_id,
        "gate": gate,
        "texto": f"[FORJA] Bloqueador {gate} do caso {caso} foi resolvido.",
    }
    return _emitir(case_dir, evento, chave_dedup=f"resolvido:{gate}")


def drenar_pendentes(case_dir) -> dict:
    """Reentrega alertas que ficaram no fallback (painel indisponível na hora)."""
    path = _pendentes(case_dir)
    if not path.is_file():
        return {"status": "vazio", "reentregues": 0}
    restantes, reentregues = [], 0
    for linha in path.read_text(encoding="utf-8").splitlines():
        try:
            ev = json.loads(linha)
        except json.JSONDecodeError:
            continue
        if ev.get("demandId") and _comentar_no_painel(ev["demandId"], ev.get("texto", "")):
            reentregues += 1
        else:
            restantes.append(linha)
    if restantes:
        path.write_text("\n".join(restantes) + "\n", encoding="utf-8")
    else:
        path.unlink(missing_ok=True)
    return {"status": "ok", "reentregues": reentregues, "restantes": len(restantes)}


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "--drenar":
        print(json.dumps(drenar_pendentes(sys.argv[2]), ensure_ascii=False))
    else:
        print(__doc__)
