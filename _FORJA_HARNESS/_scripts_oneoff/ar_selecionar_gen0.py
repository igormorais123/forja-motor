"""Seleção do vencedor da geração 0 com hashes canônicos reais + eventos no log."""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from forja_ar_blind import canonicalize  # noqa: E402
from forja_ar_evolucao import selecionar_winner, verificar_convergencia  # noqa: E402
from forja_ar_ciclo import append_log  # noqa: E402

CICLO = ROOT / "autoresearch" / "ciclos" / "ciclo-1"
EXEC = CICLO / "exec"
LOG = ROOT / "autoresearch" / "AR_LOG.jsonl"


def canon_sha(side: str) -> str:
    text = canonicalize((EXEC / f"OUT_{side}.md").read_text(encoding="utf-8", errors="replace"))
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


resultados = [
    {"id": "varA", "judgmentPath": str(CICLO / "AR_JUDGMENT_ciclo1-varA.json"),
     "comparisonPath": str(CICLO / "AR_COMPARISON_varA.json"), "variantOutputSha256": canon_sha("varA")},
    {"id": "varB", "judgmentPath": str(CICLO / "AR_JUDGMENT_ciclo1-varB.json"),
     "comparisonPath": str(CICLO / "AR_COMPARISON_varB.json"), "variantOutputSha256": canon_sha("varB")},
]
selecao = selecionar_winner("prompt-mestre-v2", 0, resultados)
print(json.dumps(selecao, ensure_ascii=False, indent=2))

for acao, payload in (
    ("julgamento_consolidado", {"varA": "invalido_ancora", "varB": "valido_kappa_1.0_winner_variante"}),
    ("promotion", {"status": "technical_candidate_passed", "sealed": "nao_consultado",
                    "nota": "sem consulta sealed — sem promoção de produção (PRD §13)"}),
    ("selecao_geracao_0", selecao),
):
    append_log(LOG, "ciclo-1", acao, payload, payload)

print(json.dumps(verificar_convergencia("prompt-mestre-v2"), ensure_ascii=False, indent=2))
