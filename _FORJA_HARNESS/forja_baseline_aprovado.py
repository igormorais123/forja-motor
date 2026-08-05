# -*- coding: utf-8 -*-
"""forja_baseline_aprovado.py — a memória do que está CERTO.

O harness aprendeu muito bem o que não fazer: são 73 gates que reprovam. O que
ele não tinha é memória do que **fazer** — o padrão aprovado pelo dono vivia como
regra escrita em protocolo, e regra escrita não se confere contra um artefato.

O preço disso foi medido em 04/08/2026: **quatro vezes num único dia** um gate
reprovou o padrão aprovado e a peça foi tratada como defeituosa. Síntese executiva
a 10,5 pt, fólio de 57,3 pt, mistura de Segoe UI com Times nas tabelas, título em
caixa mista e pull quote em moldura. Numa delas cheguei a gerar uma "correção" que
desfazia a identidade visual da casa. Todas as quatro vezes o erro foi o mesmo:
comparar contra o que estava escrito em vez de contra o que foi aprovado.

O que este módulo congela NÃO é "zero achados". Congelar perfeição seria mentira:
o template tem uma linha de exemplo não justificada, e a V4 tem um parágrafo fora
do tamanho. O que se congela é o **veredito medido na data da aprovação**. Assim o
baseline pega os dois lados:

  - o artefato mudou (hash diferente) — alguém editou uma peça aprovada;
  - o veredito mudou (métrica ou achados diferentes) — o gate derivou, e a
    pergunta "o gate melhorou ou eu o moldei?" passa a ser obrigatória.

Não substitui `test_forja_layout_papeis.py`, que ancora o texto verbatim dos
papéis, nem `test_forja_layout_antimoldagem.py`, que prova que o gate ainda
reprova estrago. Os três respondem coisas diferentes: o que a casa aprova, como
cada papel se parece, e se o gate ainda sabe dizer não.

Uso:
    python forja_baseline_aprovado.py            # confere
    python forja_baseline_aprovado.py --gravar "motivo da regravação"
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

VERSAO = "FORJA-BASELINE-APROVADO-v1"
RAIZ = Path(__file__).resolve().parent
FABRICA = RAIZ.parent
MANIFESTO = RAIZ / "BASELINE_APROVADO.json"

# Cada âncora diz O QUE ela guarda. Sem isso o baseline vira uma lista de arquivos
# e ninguém sabe, seis meses depois, por que aquela peça está ali.
ANCORAS = [
    {
        "id": "cafelana-v8",
        "caminho": ("Cafelana/contrarrazões ao AgInt no AREsp nº 2.698.443D/"
                    "_v8_visual_2026-07-30/IMPUGNACAO_AGINT_CAFELANA_V8_AJUSTADA_VISUAL.docx"),
        "aprovadaEm": "2026-07-30",
        "guarda": ("a identidade tipográfica da casa dentro de tabela — rótulo em Segoe UI, "
                   "conteúdo em Times New Roman — e o fólio de 57,3 pt numa margem de 3,5 cm"),
    },
    {
        "id": "cafelana-v4",
        "caminho": ("Cafelana/contrarrazões ao AgInt no AREsp nº 2.698.443D/"
                    "_v4_2026-07-15/IMPUGNACAO_AGINT_CAFELANA_V4_15-07-2026.docx"),
        "aprovadaEm": "2026-07-15",
        "guarda": ("a mesma mistura tipográfica numa entrega ANTERIOR, o que impede tratá-la "
                   "como acidente de uma versão só"),
    },
    {
        "id": "template-casa",
        "caminho": "_FERRAMENTAS/TEMPLATE_MEDINA_OSORIO_PETICAO.docx",
        "aprovadaEm": "2026-07-08",
        "guarda": ("o fólio da casa medido, e não inferido: 57,3 pt. Toda peça nasce daqui, "
                   "então um gate que reprova este arquivo reprova a fábrica inteira"),
    },
]


def _resolver(relativo: str) -> Path | None:
    direto = FABRICA / relativo
    if direto.is_file():
        return direto
    # A pasta do caso é renomeada de vez em quando; o nome do arquivo é estável.
    return next(FABRICA.rglob(Path(relativo).name), None)


def _medir(caminho: Path) -> dict:
    from forja_docx_layout import audit_docx_layout

    laudo = audit_docx_layout(caminho)
    metricas = laudo.get("metrics") or {}
    return {
        "sha256": hashlib.sha256(caminho.read_bytes()).hexdigest(),
        "achados": sorted({f.get("code") for f in (laudo.get("findings") or []) if f.get("code")}),
        "paragrafosDeCorpo": metricas.get("bodyParagraphs"),
        "justificacao": round(metricas.get("justificationCoverage", 0), 6),
        "tamanho": round(metricas.get("sizeCoverage", 0), 6),
        "fonte": round(metricas.get("fontCoverage", 0), 6),
    }


def conferir() -> dict:
    if not MANIFESTO.is_file():
        return {"versao": VERSAO, "erro": "manifesto inexistente", "divergencias": [],
                "ancorasConferidas": 0, "ausentes": [a["id"] for a in ANCORAS]}

    manifesto = json.loads(MANIFESTO.read_text(encoding="utf-8"))
    gravado = {item["id"]: item for item in manifesto.get("ancoras") or []}
    divergencias, ausentes, conferidas = [], [], 0

    for ancora in ANCORAS:
        caminho = _resolver(ancora["caminho"])
        anterior = gravado.get(ancora["id"])
        if caminho is None or anterior is None:
            ausentes.append(ancora["id"])
            continue
        conferidas += 1
        atual = _medir(caminho)
        if atual["sha256"] != anterior.get("sha256"):
            divergencias.append({
                "ancora": ancora["id"], "tipo": "artefato_alterado",
                "detalhe": "o arquivo aprovado mudou desde a gravação do baseline",
            })
            continue
        for campo in ("achados", "paragrafosDeCorpo", "justificacao", "tamanho", "fonte"):
            if atual[campo] != anterior.get(campo):
                divergencias.append({
                    "ancora": ancora["id"], "tipo": "veredito_mudou", "campo": campo,
                    "antes": anterior.get(campo), "agora": atual[campo],
                    "guarda": ancora["guarda"],
                })

    return {
        "versao": VERSAO,
        "gravadoEm": manifesto.get("gravadoEm"),
        "motivo": manifesto.get("motivo"),
        "ancorasConferidas": conferidas,
        "ausentes": ausentes,
        "divergencias": divergencias,
    }


def gravar(motivo: str) -> dict:
    from forja_n3_common import now_iso

    ancoras, ausentes = [], []
    for ancora in ANCORAS:
        caminho = _resolver(ancora["caminho"])
        if caminho is None:
            ausentes.append(ancora["id"])
            continue
        ancoras.append({**ancora, "caminhoResolvido": str(caminho), **_medir(caminho)})

    manifesto = {"versao": VERSAO, "gravadoEm": now_iso(), "motivo": motivo,
                 "ausentes": ausentes, "ancoras": ancoras}
    MANIFESTO.write_text(json.dumps(manifesto, ensure_ascii=False, indent=2), encoding="utf-8")
    return manifesto


if __name__ == "__main__":  # pragma: no cover
    import argparse

    ap = argparse.ArgumentParser(description="Congela e confere o padrão aprovado da casa.")
    ap.add_argument("--gravar", metavar="MOTIVO")
    args = ap.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    if args.gravar:
        if not args.gravar.strip():
            print("Regravar o baseline exige motivo escrito.")
            raise SystemExit(2)
        m = gravar(args.gravar)
        print(f"baseline gravado: {len(m['ancoras'])} âncora(s); ausentes: {m['ausentes'] or 'nenhuma'}")
        raise SystemExit(0)

    laudo = conferir()
    print("=" * 78)
    print("BASELINE DO PADRÃO APROVADO")
    print("=" * 78)
    print(f"  gravado em     : {laudo.get('gravadoEm')}")
    print(f"  motivo         : {laudo.get('motivo')}")
    print(f"  âncoras        : {laudo['ancorasConferidas']} conferida(s)")
    if laudo["ausentes"]:
        print(f"  AUSENTES       : {', '.join(laudo['ausentes'])}")
    if laudo["divergencias"]:
        print("\n  DIVERGÊNCIAS — o padrão aprovado deixou de ser lido como antes")
        for d in laudo["divergencias"]:
            print(f"    {d['ancora']}: {d['tipo']}"
                  + (f" em {d['campo']}: {d['antes']} -> {d['agora']}" if d.get("campo") else ""))
        raise SystemExit(1)
    print("\n  nenhuma divergência: o que a casa aprovou continua sendo lido do mesmo jeito")
