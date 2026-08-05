"""Camada evolutiva Karpathy do FORJA AUTO-RESEARCH (gerações, winners, convergência).

Modelo da skill `autoresearch` (AutoResearch de Andrej Karpathy): gerações sucessivas de
variantes mutadas a partir dos vencedores, seleção determinística e propagação manual.
Esta camada NÃO avalia nada sozinha: cada variante só vira vencedora com o resultado de um
ciclo AR completo (canários + não-inferioridade + juiz cego), preservando o anti-trapaça.

Estratégias de mutação canônicas (skill autoresearch): rephrase, expand, compress,
pivot, hybrid. Cada variante declara a sua e o eixo conceitual do diff.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

SCHEMA = "FORJA-AR-v1"
ROOT = Path(__file__).resolve().parent
EVOLUCAO = ROOT / "autoresearch" / "evolucao"
FIXED_TIME = "1970-01-01T00:00:00Z"
ESTRATEGIAS = {"rephrase", "expand", "compress", "pivot", "hybrid"}


def _sha_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8", errors="replace"))


def _save(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _manifest_path(experimento: str) -> Path:
    return EVOLUCAO / experimento / "manifest.json"


def init_experimento(experimento: str, alvo: Path, *, convergencia_ganho_min: float = 0.02,
                     convergencia_geracoes: int = 3, top_k: int = 1) -> dict:
    """Cria o experimento com baseline congelado (geração -1 = artefato vigente)."""
    alvo = Path(alvo)
    if not alvo.is_file():
        raise ValueError(f"alvo inexistente: {alvo}")
    manifest = {
        "schemaVersion": SCHEMA,
        "generatedAt": FIXED_TIME,
        "producerRunId": f"evolucao-init-{experimento}",
        "experimento": experimento,
        "alvo": str(alvo),
        "alvoSha256": _sha_file(alvo),
        "topK": int(top_k),
        "convergencia": {"ganhoMin": float(convergencia_ganho_min), "geracoesSemGanho": int(convergencia_geracoes)},
        "geracaoAtual": -1,
        "geracoes": [],
    }
    base_dir = EVOLUCAO / experimento
    baseline = base_dir / "baseline.md"
    baseline.parent.mkdir(parents=True, exist_ok=True)
    baseline.write_text(alvo.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
    _save(_manifest_path(experimento), manifest)
    return manifest


def registrar_geracao(experimento: str, variantes: list[dict]) -> dict:
    """Registra geração N com variantes já escritas em disco (estratégia declarada)."""
    manifest = _load(_manifest_path(experimento))
    numero = int(manifest["geracaoAtual"]) + 1
    registros = []
    for item in variantes:
        estrategia = str(item.get("estrategia") or "")
        path = Path(str(item.get("path") or ""))
        if estrategia not in ESTRATEGIAS:
            raise ValueError(f"estratégia desconhecida: {estrategia} (canônicas: {sorted(ESTRATEGIAS)})")
        if not path.is_file():
            raise ValueError(f"variante inexistente: {path}")
        if not str(item.get("eixo") or "").strip():
            raise ValueError("cada variante declara o eixo conceitual do diff (mutação inteligente, não aleatória)")
        registros.append({
            "id": str(item.get("id") or path.stem),
            "path": str(path),
            "sha256": _sha_file(path),
            "estrategia": estrategia,
            "eixo": str(item["eixo"]),
            "parent": str(item.get("parent") or ("baseline" if numero == 0 else f"winner-gen-{numero - 1}")),
        })
    manifest["geracoes"].append({
        "numero": numero,
        "variantes": registros,
        "resultado": None,
        "winner": None,
    })
    manifest["geracaoAtual"] = numero
    _save(_manifest_path(experimento), manifest)
    return {"schemaVersion": SCHEMA, "geracao": numero, "variantes": len(registros)}


def selecionar_winner(experimento: str, geracao: int, resultados: list[dict]) -> dict:
    """Seleciona vencedor SÓ com evidência de ciclo AR: juiz cego + não-inferioridade.

    resultado por variante: {"id", "judgmentPath", "comparisonPath"} — a variante só
    concorre se o julgamento for válido, o vencedor por hash for o dela e a comparação
    de indicadores estiver aprovada (sem regressão além da margem, sem novo null).
    """
    manifest = _load(_manifest_path(experimento))
    entry = next((g for g in manifest["geracoes"] if g["numero"] == int(geracao)), None)
    if entry is None:
        raise ValueError(f"geração inexistente: {geracao}")
    aprovados = []
    detalhes = []
    for item in resultados:
        variant = next((v for v in entry["variantes"] if v["id"] == item.get("id")), None)
        if variant is None:
            raise ValueError(f"variante fora da geração: {item.get('id')}")
        judgment = _load(Path(str(item["judgmentPath"])))
        comparison = _load(Path(str(item["comparisonPath"])))
        output_sha = str(item.get("variantOutputSha256") or "")
        venceu_cego = bool(judgment.get("valid")) and judgment.get("winnerArtifactSha256") == output_sha and output_sha
        nao_inferior = bool(comparison.get("aprovado"))
        detalhes.append({
            "id": variant["id"],
            "estrategia": variant["estrategia"],
            "venceuJuizCego": venceu_cego,
            "naoInferioridade": nao_inferior,
            "kappa": judgment.get("kappa"),
        })
        if venceu_cego and nao_inferior:
            aprovados.append(variant)
    winner = aprovados[0] if len(aprovados) >= 1 else None
    if len(aprovados) > 1:
        # desempate determinístico pré-registrado: menor sha256 do artefato
        winner = sorted(aprovados, key=lambda v: v["sha256"])[0]
    entry["resultado"] = detalhes
    entry["winner"] = winner["id"] if winner else None
    if winner:
        winners_dir = EVOLUCAO / experimento / "winners"
        winners_dir.mkdir(parents=True, exist_ok=True)
        (winners_dir / f"gen-{geracao}.md").write_text(
            Path(winner["path"]).read_text(encoding="utf-8", errors="replace"), encoding="utf-8"
        )
    _save(_manifest_path(experimento), manifest)
    return {"schemaVersion": SCHEMA, "geracao": int(geracao), "winner": entry["winner"], "detalhes": detalhes}


def verificar_convergencia(experimento: str) -> dict:
    """Convergiu quando K gerações consecutivas terminam sem vencedor (sem ganho)."""
    manifest = _load(_manifest_path(experimento))
    limite = int(manifest["convergencia"]["geracoesSemGanho"])
    fechadas = [g for g in manifest["geracoes"] if g.get("resultado") is not None]
    seguidas_sem_winner = 0
    for entry in reversed(fechadas):
        if entry.get("winner"):
            break
        seguidas_sem_winner += 1
    return {
        "schemaVersion": SCHEMA,
        "experimento": experimento,
        "geracoesFechadas": len(fechadas),
        "seguidasSemGanho": seguidas_sem_winner,
        "convergiu": seguidas_sem_winner >= limite,
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Evolução Karpathy do FORJA AUTO-RESEARCH")
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init")
    init.add_argument("--experimento", required=True)
    init.add_argument("--alvo", type=Path, required=True)
    gen = sub.add_parser("nova-geracao")
    gen.add_argument("--experimento", required=True)
    gen.add_argument("--variantes", type=Path, required=True, help="JSON: [{id, path, estrategia, eixo, parent?}]")
    sel = sub.add_parser("selecionar")
    sel.add_argument("--experimento", required=True)
    sel.add_argument("--geracao", type=int, required=True)
    sel.add_argument("--resultados", type=Path, required=True,
                     help="JSON: [{id, judgmentPath, comparisonPath, variantOutputSha256}]")
    conv = sub.add_parser("convergencia")
    conv.add_argument("--experimento", required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "init":
            result = init_experimento(args.experimento, args.alvo)
        elif args.command == "nova-geracao":
            result = registrar_geracao(args.experimento, json.loads(args.variantes.read_text(encoding="utf-8")))
        elif args.command == "selecionar":
            result = selecionar_winner(args.experimento, args.geracao,
                                       json.loads(args.resultados.read_text(encoding="utf-8")))
        else:
            result = verificar_convergencia(args.experimento)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"erro: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
