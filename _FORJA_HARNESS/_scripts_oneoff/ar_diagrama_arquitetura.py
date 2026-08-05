"""Diagrama de arquitetura do subsistema FORJA AUTO-RESEARCH (ciclo AR) — como construído.

SVG com tokens da marca INTEIA (visual-thinking/scripts/inteia_brand.py quando disponível).
Saída: autoresearch/ciclos/ciclo-0/AR_ARQUITETURA_DIAGRAMA.svg
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "autoresearch" / "ciclos" / "ciclo-0" / "AR_ARQUITETURA_DIAGRAMA.svg"

BRAND_DIR = Path.home() / ".claude" / "skills" / "visual-thinking" / "scripts"
sys.path.insert(0, str(BRAND_DIR))
try:
    from inteia_brand import BRAND  # type: ignore

    NAVY = BRAND.colors.navy
    GOLD = BRAND.colors.gold
    TEXT = BRAND.colors.text_primary
    TEXT2 = BRAND.colors.text_secondary
    SUCCESS = BRAND.colors.success
    WARNING = BRAND.colors.warning
    DANGER = BRAND.colors.danger
    INFO = BRAND.colors.info
except Exception:
    NAVY, GOLD = "#1B2A4A", "#C9A227"
    TEXT, TEXT2 = "#2C3E50", "#5A5A5A"
    SUCCESS, WARNING, DANGER, INFO = "#2E7D32", "#F57C00", "#C62828", "#1565C0"

W, H = 1780, 1290
FONT = "Inter, 'Segoe UI', Arial, sans-serif"
MONO = "'JetBrains Mono', Consolas, monospace"

parts: list[str] = []


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def rect(x, y, w, h, fill="#FFFFFF", stroke=NAVY, sw=1.5, rx=10, dash="", opacity=1.0):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    parts.append(
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" '
        f'stroke="{stroke}" stroke-width="{sw}" opacity="{opacity}"{d}/>'
    )


def text(x, y, s, size=13, fill=TEXT, weight="normal", anchor="start", font=FONT, spacing=""):
    sp = f' letter-spacing="{spacing}"' if spacing else ""
    parts.append(
        f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" fill="{fill}" '
        f'font-weight="{weight}" text-anchor="{anchor}"{sp}>{esc(s)}</text>'
    )


def lines(x, y, itens, size=12.5, lh=19, fill=TEXT):
    for i, s in enumerate(itens):
        if s.startswith("**"):
            text(x, y + i * lh, s.strip("*"), size, fill, "600")
        elif s.startswith("~"):
            text(x, y + i * lh, s[1:], size - 1, TEXT2)
        elif s.startswith("`"):
            text(x, y + i * lh, s.strip("`"), size - 1, INFO, font=MONO)
        else:
            text(x, y + i * lh, s, size, fill)


def arrow(x1, y1, x2, y2, color=NAVY, sw=2.2, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    parts.append(
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
        f'stroke-width="{sw}" marker-end="url(#seta)"{d}/>'
    )


def zona(x, y, w, h, titulo, cor=NAVY):
    rect(x, y, w, h, fill="#FAFBFC", stroke=cor, sw=2, rx=14)
    rect(x, y, w, 34, fill=cor, stroke=cor, rx=14)
    parts.append(f'<rect x="{x}" y="{y + 20}" width="{w}" height="14" fill="{cor}"/>')
    text(x + 14, y + 23, titulo, 15, "#FFFFFF", "700", spacing="0.4px")


def caixa(x, y, w, h, titulo, itens, cor=NAVY, tsize=13):
    rect(x, y, w, h, fill="#FFFFFF", stroke=cor, sw=1.4, rx=8)
    text(x + 12, y + 21, titulo, tsize, cor, "700")
    lines(x + 12, y + 41, itens)


# ---------------------------------------------------------------- fundo e defs
parts.append(
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img">'
    f'<title>Arquitetura FORJA AUTO-RESEARCH (ciclo AR)</title>'
    f'<desc>Diagrama como-construído: material real, medição, anti-trapaça, ciclo A0–A6, segredos externos, Régua e governança.</desc>'
    f'<defs><marker id="seta" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto">'
    f'<path d="M0,0 L10,4 L0,8 z" fill="{NAVY}"/></marker></defs>'
    f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>'
)

# ---------------------------------------------------------------- cabeçalho
text(40, 46, "INTE", 26, NAVY, "800")
text(102, 46, "IA", 26, GOLD, "800")
text(150, 46, "|  FORJA AUTO-RESEARCH — ciclo AR de auto-melhoria anti-trapaça (como construído, 23/07/2026)", 19, TEXT, "700")
text(150, 68, "PRD/TDD v1.1 (planejamento/22–23) após review adversarial Codex GPT-5.5: v1.0 REPROVADA com 13 P1 — todos incorporados", 13, TEXT2)
rect(1490, 26, 250, 46, fill="#FFF6E5", stroke=WARNING, sw=2, rx=10)
text(1615, 45, "STATUS: estudo_descritivo", 13.5, WARNING, "700", anchor="middle")
text(1615, 62, "nenhuma promoção até sealed prospectivo", 10.5, TEXT2, anchor="middle")

# ================================================================ ZONA 1 — MATERIAL REAL
zona(40, 96, 400, 560, "1 · MATERIAL REAL (corpus)", NAVY)
caixa(60, 148, 360, 96, "state/ — 49 casos reais da esteira", [
    "43 elegíveis no scan (critério amplo validado",
    "contra o disco; glob literal cobria só 3)",
    "~7 artefatos pontuáveis (final/draft/produto md);",
    "~36 metadata_only — inventariados, nunca pontuam",
])
caixa(60, 258, 360, 118, "forja_ar_corpus.py — split determinístico", [
    "**HMAC(chave externa, LINHAGEM) — nunca caseId**",
    "grupo do mesmo litígio jamais se separa",
    "estratificado por produto×tribunal, com mínimos",
    "train 28 · holdout 7 · sealed 8",
    "~sealed NÃO listado no workspace (só contagem)",
])
caixa(60, 390, 360, 86, "AR_CORPUS.json + --check", [
    "hash SHA-256 de cada artefato",
    "linhagem em splits distintos = erro",
    "re-scan → splits idênticos (função pura)",
])
caixa(60, 490, 360, 86, "Extensão descritiva (calibração)", [
    ".autoresearch/fabrica-peticoes-v1",
    "17 peças reais (pilotos + rodadas cegas gen-0..2)",
    "~usadas SÓ no painel descritivo do ciclo-0",
], cor=INFO)
text(60, 610, "Painel ciclo-0: 22 peças reais avaliadas", 12.5, TEXT, "600")
text(60, 630, "σ reais: I2 0.29 · I4 0.42 · I5 0.42 · I6 0.47", 12.5, TEXT2)

# ================================================================ ZONA 2 — MEDIÇÃO
zona(470, 96, 420, 560, "2 · MEDIÇÃO (painel de indicadores)", NAVY)
caixa(490, 148, 380, 108, "Sensores vivos REUTILIZADOS (nunca editados)", [
    "`forja_verificador.py  (G1–G9 determinísticos)`",
    "`forja_metricas_f7.py  (extração de citações)`",
    "`forja_estilo_humano.py  (v2, P0/P1)`",
    "`forja_human_review.py  (recibos Ed25519)`",
])
caixa(490, 270, 380, 250, "forja_ar_indicadores.py — I1–I10", [
    "**alvo**  I1 citações: cobertura×correção (ledger)",
    "**alvo**  I3 premissas com lastro (ledger)",
    "**alvo**  I7 blindagem recursal (issue ledger)",
    "**alvo**  I9 juiz cego pairwise (entre variantes)",
    "**veto**  I2 integridade jurídica (súmula/instituto)",
    "**veto**  I4 placeholders  ·  I6 origem operacional",
    "**veto**  I8 QA visual (zero crítico + recibo)",
    "sentinela I5 estilo humano · operacional I10",
    "~ledger congelado PRÉ-geração: taxa não melhora",
    "~por exclusão de conteúdo (R4 do review)",
    "~pesos SÓ do AR_MANIFEST.json (nada hardcoded)",
])
caixa(490, 534, 380, 104, "Regras fail-honest", [
    "sensor ausente → null MOTIVADO (nunca 0)",
    "comparação: máscara pareada pelo baseline",
    "**novo null na variante = BLOQUEIO (não renormaliza)**",
    "cache content-addressed (artefato+sensor+contexto)",
], cor=DANGER)

# ================================================================ ZONA 3 — ANTI-TRAPAÇA
zona(920, 96, 420, 560, "3 · ANTI-TRAPAÇA (prova pareada e cega)", NAVY)
caixa(940, 148, 380, 170, "forja_ar_canarios.py — falha única real", [
    "base REAL (peça Azimut, train) + UMA falha injetada",
    "públicos: placeholder · origem operacional · estilo IA",
    "· súmula×tribunal trocada · citação obrigatória removida",
    "+2 secretos externos (paráfrase Drive, placeholder sutil)",
    "**kill 7/7 pelo sensor-alvo · zero contaminação**",
    "**controles benignos vivos (paráfrase não morre)**",
    "~hashes congelados; alteração exige motivo",
])
caixa(940, 332, 380, 100, "forja_ar_runpair.py — execução pareada", [
    "input + ledgers CONGELADOS antes da geração",
    "manifest por lado: modelo, família, params, tokens, hash",
    "**paridade violada → par não chega ao juiz**",
], cor=INFO)
caixa(940, 446, 380, 200, "forja_ar_blind.py — julgamento cego", [
    "bundles canonicalizados (sem nome/versão/front-matter)",
    "A/B e B/A (swap obrigatório) em diretório isolado",
    "mapping com HMAC — chave FORA do workspace;",
    "hash registrado no log ANTES do julgamento",
    "**consolidação por artifactSha256, não por rótulo**",
    "mesma POSIÇÃO vencendo 2× = viés → par anulado",
    "≥2 famílias de juiz (Claude × Codex);",
    "**família geradora NÃO julga a própria variante**",
    "devolutiva exige trecho-âncora literal do bundle",
], cor=DANGER)

# ================================================================ ZONA 4 — CICLO
zona(1370, 96, 370, 560, "4 · CICLO A0–A6 e PROMOÇÃO", NAVY)
fases = [
    ("A0", "snapshot: pré-registro congelado + hash no log"),
    ("A1", "painel baseline (máscara pareada)"),
    ("A2", "canários: all-pass público + secreto"),
    ("A3", "execução pareada vigente × variante"),
    ("A4", "julgamento cego (kappa ≥ 0.6)"),
    ("A5", "promotion gate técnico"),
    ("A6", "revisão independente + humano"),
]
fy = 150
for fase_id, desc in fases:
    rect(1390, fy, 330, 34, fill="#FFFFFF", stroke=NAVY, sw=1.3, rx=8)
    parts.append(f'<circle cx="1410" cy="{fy + 17}" r="12" fill="{NAVY}"/>')
    text(1410, fy + 21, fase_id, 10.5, "#FFFFFF", "700", anchor="middle")
    text(1430, fy + 21, desc, 11.8, TEXT)
    if fase_id != "A6":
        arrow(1555, fy + 34, 1555, fy + 44, sw=1.6)
    fy += 44

caixa(1390, 468, 330, 170, "Gate de 3 estados (anti-autoaprovação)", [
    "① technical_candidate_passed",
    "~   não-inferioridade POR dimensão + vetos +",
    "~   orçamentos (5 candidatos · 10 holdout · sealed 3 VITALÍCIO)",
    "② independent_review_passed (família ≠ geradora)",
    "**③ human_promotion_approved (recibo Ed25519)**",
    "log AR_LOG.jsonl ENCADEADO por hash",
    "~edição de manifest pós-resultado invalida o ciclo",
], cor=SUCCESS)

# ---------------------------------------------------------------- setas entre zonas
arrow(440, 320, 470, 320)   # corpus -> medição
arrow(890, 330, 920, 330)   # medição -> anti-trapaça (indicadores alimentam canários)
arrow(1340, 380, 1370, 380) # anti-trapaça -> ciclo
parts.append(f'<path d="M 440 540 C 700 700, 1100 700, 1385 640" stroke="{INFO}" stroke-width="2" fill="none" stroke-dasharray="6 4" marker-end="url(#seta)"/>')
text(860, 688, "holdout/sealed: consultados só no gate, com orçamento debitado", 11.5, INFO, anchor="middle")

# ================================================================ FAIXA INFERIOR
zona(40, 740, 545, 250, "SEGREDOS FORA DO WORKSPACE", DANGER)
caixa(60, 792, 505, 176, "%USERPROFILE%\\.forja_ar_secrets\\  (nunca em repositório)", [
    "`ar_hmac.key` — chave do split e do mapping cego (64 bytes)",
    "`sealed_registry.json` — inventário sealed + orçamento",
    "   VITALÍCIO de consultas (3; intocado)",
    "`canarios_secretos/` — camada rotativa de auditoria",
    "testes redirecionam via `FORJA_AR_SECRETS_DIR` (tmp_path)",
    "~criado sob demanda; jamais impresso ou commitado",
])

zona(615, 740, 545, 250, "PROTEÇÃO E REGRESSÃO (Régua)", SUCCESS)
caixa(635, 792, 505, 176, "Régua FORJA — APROVADA em 23/07/2026", [
    "68 arquivos hash-protegidos (13 novos do AR, rebaseline motivado)",
    "13 suítes verdes, incluindo `test_forja_autoresearch.py`",
    "**23 testes · 12 sabotagens nominais:** split-shopping,",
    "mapping vazado, injeção contra juiz, supressão de ledger,",
    "inflação de páginas, remoção de citações, stuffing de I7,",
    "manifest pós-resultado, replay do sealed, linhagem separada,",
    "pesos hardcoded, controle benigno morto",
])

zona(1190, 740, 550, 250, "GOVERNANÇA E CALIBRAÇÃO (ciclo-0)", GOLD)
caixa(1210, 792, 510, 176, "Trilha auditável do que foi feito", [
    "PRD §14: triagem das 15 recomendações Codex (13 P1 acatadas)",
    "AR_MANIFEST v1.0-piloto: pesos/margens/orçamentos pré-registrados,",
    "histórico com σ por indicador e decisão de calibração",
    "spot-check I6: 7/7 flags = verdadeiros positivos (caminho local",
    "vazado em peças históricas — diretriz inviolável 11/07 confirmada)",
    "missingness DECLARADA: I1/I3/I7/I8 sem dado histórico (ledgers",
    "e recibos só nascem prospectivamente) — sem alegação de eficácia",
])

# ---------------------------------------------------------------- conexões faixa inferior
arrow(230, 740, 230, 660, color=DANGER, sw=1.8, dash="5 4")
text(240, 700, "HMAC do split", 11, DANGER)
arrow(1080, 740, 1080, 660, color=SUCCESS, sw=1.8, dash="5 4")
text(1090, 700, "suíte AR na régua", 11, SUCCESS)
arrow(1460, 740, 1460, 660, color=GOLD, sw=1.8, dash="5 4")
text(1470, 700, "pré-registro do ciclo", 11, "#9A7B1D")

# ---------------------------------------------------------------- rodapé
parts.append('<line x1="40" y1="1030" x2="1740" y2="1030" stroke="#E1E5EA" stroke-width="1.5"/>')
text(40, 1060, "Fluxo de uma melhoria: variante candidata → A0 pré-registro → painel/canários → execução pareada → juiz cego (swap, 2 famílias) → gate técnico → revisor independente → aprovação humana → propagação manual com backup + rebaseline da Régua.", 13, TEXT)
text(40, 1084, "O que o desenho anti-trapaça impede: otimizar por exclusão de conteúdo (ledgers congelados) · juiz viciado por posição/verbosidade/autopreferência (swap, hash, famílias) · overfitting ao holdout (orçamentos, sealed vitalício) ·", 12.5, TEXT2)
text(40, 1104, "autoaprovação (3 estados + Ed25519 + log encadeado) · métrica de fachada (canário de falha única com atribuição por sensor; indicador sem variância vira sentinela ou sai).", 12.5, TEXT2)
text(40, 1140, "Pendências reais declaradas: ledgers I1/I3/I7 só nascem nos próximos casos (A0/runpair) · sealed prospectivo ainda não consumível · rotação da camada secreta após cada uso em decisão.", 12.5, WARNING)
text(40, 1180, "Módulos:", 12.5, TEXT, "700")
text(105, 1180, "forja_ar_corpus.py · forja_ar_indicadores.py · forja_ar_canarios.py · forja_ar_runpair.py · forja_ar_blind.py · forja_ar_ciclo.py · test_forja_autoresearch.py", 12.5, INFO, font=MONO)
text(40, 1204, "Artefatos: autoresearch/{AR_MANIFEST, AR_CORPUS, AR_PANEL, AR_LOG.jsonl, prompts/, canarios/, ciclos/ciclo-0/AR_CICLO_0_RELATORIO.md}", 12.5, TEXT2, font=MONO)
text(40, 1240, "Figura 1 — Arquitetura como-construída do subsistema FORJA AUTO-RESEARCH (ciclo AR). Fonte: elaboração própria, 23/07/2026.", 11.5, TEXT2)
text(1740, 1240, "INTEIA · Inteligência Estratégica", 11.5, TEXT2, anchor="end")

parts.append("</svg>")
OUT.write_text("\n".join(parts), encoding="utf-8")
print(f"ok: {OUT}")
