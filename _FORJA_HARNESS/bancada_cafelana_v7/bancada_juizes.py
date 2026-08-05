# -*- coding: utf-8 -*-
"""
bancada_juizes.py — Julgamento cego comparativo, com controle de posição e âncora verificada.

A camada determinística mede o que é regra. Esta mede o que é ofício: força da
tese, aderência do precedente à proposição, ordem dispositiva, economia da
prosa. Isso não se afere por regex — e também não se afere por um juiz só.

Cinco blindagens, todas herdadas do ciclo AR da casa:

1. **Cegamento real.** As peças viram P1..Pn em ordem sorteada, e o mapa vai
   para fora do workspace (`%USERPROFILE%\\.forja_ar_secrets\\`). Quem lê a pasta
   da bancada não consegue ligar peça a autor.
2. **Varredura de vazamento antes de cegar.** Peça que se identifica — nome de
   modelo, "como IA", assinatura de família — é sinalizada. Cegamento sobre
   texto que se denuncia é teatro.
3. **Controle de posição.** Cada juiz julga duas vezes, com a ordem de
   apresentação invertida. Ranking que muda ao inverter a ordem mede viés de
   posição, não qualidade — e isso passa a ser um número no relatório.
4. **Âncora literal conferida por código.** O juiz precisa transcrever um trecho
   da peça que elegeu. Se o trecho não existe naquela peça, o voto é anulado.
   É o teste de que o juiz leu o que julgou.
5. **Auto-preferência medida, não presumida.** Todo juiz aqui também é
   participante. Isso não se resolve com boa vontade: mede-se quanto cada
   família favorece a si mesma e publica-se o número.

Uso:
    python bancada_juizes.py --cegar
    python bancada_juizes.py --julgar [--juiz opus-5]
    python bancada_juizes.py --consolidar
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import random
import re
import sys
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path

BANCADA = Path(__file__).resolve().parent
FORJA = BANCADA.parent
sys.path.insert(0, str(FORJA))

from bancada_executar import (  # noqa: E402
    PARTICIPANTES, _custo, _via_assinatura, _via_openrouter,
)

VERSAO = "BANCADA-CAFELANA-V7-JUIZES-v1"
SEGREDOS = Path(os.environ.get("FORJA_AR_SECRETS_DIR")
                or Path(os.environ.get("USERPROFILE", Path.home())) / ".forja_ar_secrets")
MAPA = SEGREDOS / "bancada_cafelana_v7_mapa.json"

# Três famílias. Nenhuma escapa de ser participante também — por isso a
# auto-preferência é medida em vez de negada.
JUIZES = ["opus-5", "sol-5.6", "grok-4.5"]

_VAZAMENTO = re.compile(
    r"\b(?:claude|opus|fable|anthropic|chatgpt|gpt-?\d|openai|grok|xai|"
    r"kimi|moonshot|luna|sol-?5|gemini|llama|mistral|deepseek)\b|"
    r"como (?:uma? )?(?:intelig[êe]ncia artificial|modelo de linguagem|IA)\b|"
    r"\bas an AI\b|\bcomo assistente\b",
    re.I)

CRITERIOS = [
    ("tese", "Força da tese principal e enfrentamento do risco de conhecimento parcial"),
    ("comando", "Fidelidade às determinações do titular e à identidade processual do caso"),
    ("autoridade", "Uso de autoridade: pertinência e aderência entre o precedente e a "
                   "proposição que ele sustenta"),
    ("arquitetura", "Arquitetura da peça, ordem dispositiva e escada de pedidos"),
    ("escrita", "Escrita forense: precisão, economia, ausência de adjetivação inútil"),
    ("utilidade", "Utilidade para o julgador: síntese de abertura, navegabilidade, "
                  "capacidade de decidir a partir da peça"),
]


def _rotulos(n: int) -> list[str]:
    return [f"P{i + 1}" for i in range(n)]


def cegar() -> dict:
    fontes = sorted(p for p in (BANCADA / "execucao").iterdir()
                    if (p / "SAIDA.md").is_file())
    if len(fontes) < 2:
        raise SystemExit("são necessárias ao menos duas peças para julgar")

    vazamentos = {}
    textos = {}
    for pasta in fontes:
        texto = (pasta / "SAIDA.md").read_text(encoding="utf-8")
        achados = sorted({m.group(0).casefold() for m in _VAZAMENTO.finditer(texto)})
        if achados:
            vazamentos[pasta.name] = achados
        textos[pasta.name] = texto

    ordem = [p.name for p in fontes]
    random.shuffle(ordem)
    mapa = {rot: nome for rot, nome in zip(_rotulos(len(ordem)), ordem)}

    cego = BANCADA / "cego"
    cego.mkdir(exist_ok=True)
    for antigo in cego.glob("P*.md"):
        antigo.unlink()
    for rotulo, nome in mapa.items():
        (cego / f"{rotulo}.md").write_text(textos[nome], encoding="utf-8")

    SEGREDOS.mkdir(parents=True, exist_ok=True)
    MAPA.write_text(json.dumps({
        "versao": VERSAO,
        "em": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "mapa": mapa,
        "vazamentosDetectados": vazamentos,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    (cego / "CEGAMENTO.json").write_text(json.dumps({
        "versao": VERSAO,
        "rotulos": sorted(mapa),
        "mapaGuardadoEm": "fora do workspace (~/.forja_ar_secrets)",
        "vazamentosDetectados": {k: len(v) for k, v in vazamentos.items()},
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"cegadas {len(mapa)} peças em {cego}")
    if vazamentos:
        print("  ATENÇÃO — peças que se identificam:")
        for nome, achados in vazamentos.items():
            print(f"    {nome}: {', '.join(achados[:6])}")
    else:
        print("  varredura de vazamento: nenhuma peça se identifica")
    return mapa


def _prompt_juiz(rotulos: list[str], textos: dict[str, str]) -> str:
    criterios = "\n".join(f"{i + 1}. **{c}** — {d}" for i, (c, d) in enumerate(CRITERIOS))
    corpo = "\n\n".join(
        f"{'=' * 78}\n### PEÇA {r}\n{'=' * 78}\n\n{textos[r]}" for r in rotulos)
    chaves = ", ".join(f'"{c}"' for c, _ in CRITERIOS)
    return f"""Você é desembargador aposentado, hoje parecerista, e recebeu {len(rotulos)} versões
independentes da mesma peça: uma impugnação a agravo interno no AREsp nº 2.698.443/DF,
perante a Primeira Turma do Superior Tribunal de Justiça, em que as agravadas são as
clientes e a agravante é a União.

As versões foram escritas por autores diferentes a partir do mesmo material. Você não
sabe quem escreveu qual, e não deve especular. Julgue o texto.

## Critérios, de 0 a 10 cada

{criterios}

## O que você precisa observar com rigor

- **Precedente que não sustenta o que a peça afirma** é falha grave, ainda que o texto
  soe convincente. Se a peça marcou algo como pendente de conferência, isso é honestidade,
  não defeito.
- **Determinação do cliente descumprida** é falha grave, mesmo que a alternativa pareça
  tecnicamente melhor.
- Peça longa não é peça forte. Peça curta não é peça enxuta. Meça densidade por parágrafo.
- Desconfie de fluência: prosa bonita que não decide nada vale menos que prosa seca que
  fecha a questão.

## Formato da resposta

Devolva **apenas** um objeto JSON, sem texto antes ou depois, exatamente assim:

{{
  "notas": {{ "<rótulo>": {{ {chaves} }} }},
  "ranking": ["<rótulo do melhor>", "...", "<rótulo do pior>"],
  "protocolaria": "<rótulo da única peça que você assinaria e protocolaria hoje>",
  "ancora": "<transcrição literal de 15 a 30 palavras, copiada exatamente da peça que você
              indicou em 'protocolaria', que justifique a escolha>",
  "porque": "<3 a 5 frases: o que decidiu a comparação>",
  "erroMaisGrave": {{ "<rótulo>": "<o erro mais grave daquela peça, em uma frase>" }}
}}

A âncora será conferida contra o texto da peça. Transcreva, não parafraseie.

{corpo}
"""


def julgar(juiz_id: str, *, invertido: bool, timeout: int) -> dict:
    cego = BANCADA / "cego"
    rotulos = sorted((p.stem for p in cego.glob("P*.md")),
                     key=lambda r: int(r[1:]), reverse=invertido)
    textos = {r: (cego / f"{r}.md").read_text(encoding="utf-8") for r in rotulos}
    prompt = _prompt_juiz(rotulos, textos)
    p = PARTICIPANTES[juiz_id]

    bruto = (_via_assinatura if p.rota == "assinatura" else _via_openrouter)(
        p, prompt, timeout)
    texto = bruto["texto"].strip()
    limpo = re.sub(r"^```(?:json)?\s*|\s*```$", "", texto, flags=re.I | re.M).strip()
    inicio, fim = limpo.find("{"), limpo.rfind("}")
    try:
        voto = json.loads(limpo[inicio:fim + 1])
    except (json.JSONDecodeError, ValueError) as erro:
        raise SystemExit(f"{juiz_id}: voto não é JSON válido ({erro})")

    # Âncora: o juiz leu a peça que elegeu?
    eleita = str(voto.get("protocolaria") or "")
    ancora = " ".join(str(voto.get("ancora") or "").split())
    def _norm(v):
        return " ".join(re.sub(r"[^\w\s]", " ", v.casefold()).split())
    valida = bool(ancora) and eleita in textos and _norm(ancora) in _norm(textos[eleita])

    resultado = {
        "versao": VERSAO,
        "juiz": juiz_id,
        "familiaJuiz": p.familia,
        "ordem": "invertida" if invertido else "direta",
        "rotulosApresentados": rotulos,
        "voto": voto,
        "ancoraValida": valida,
        "votoAnulado": not valida,
        "custoUsd": round(_custo(p, bruto["tokensEntrada"], bruto["tokensSaida"]), 4),
        "tokensEntrada": bruto["tokensEntrada"],
        "tokensSaida": bruto["tokensSaida"],
        "em": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "sha256Prompt": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
    }
    destino = BANCADA / "avaliacao" / "juizes"
    destino.mkdir(parents=True, exist_ok=True)
    nome = f"{juiz_id}_{'inv' if invertido else 'dir'}.json"
    (destino / nome).write_text(
        json.dumps(resultado, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    marca = "ANULADO (âncora não confere)" if not valida else f"elegeu {eleita}"
    print(f"  [{juiz_id}/{resultado['ordem']}] {marca} · US$ {resultado['custoUsd']:.3f}")
    return resultado


def consolidar() -> dict:
    mapa = json.loads(MAPA.read_text(encoding="utf-8"))["mapa"]
    votos = [json.loads(p.read_text(encoding="utf-8"))
             for p in sorted((BANCADA / "avaliacao" / "juizes").glob("*.json"))]
    validos = [v for v in votos if not v["votoAnulado"]]
    rotulos = sorted(mapa, key=lambda r: int(r[1:]))

    # Pontos de Borda: em ranking de n, o primeiro leva n-1, o último 0.
    borda = {r: 0.0 for r in rotulos}
    criterios = {r: {c: [] for c, _ in CRITERIOS} for r in rotulos}
    eleicoes = {r: 0 for r in rotulos}
    for v in validos:
        ranking = [r for r in v["voto"].get("ranking", []) if r in borda]
        n = len(ranking)
        for i, r in enumerate(ranking):
            borda[r] += (n - 1 - i)
        for r, notas in (v["voto"].get("notas") or {}).items():
            if r in criterios and isinstance(notas, dict):
                for c, _ in CRITERIOS:
                    if isinstance(notas.get(c), (int, float)):
                        criterios[r][c].append(float(notas[c]))
        eleita = v["voto"].get("protocolaria")
        if eleita in eleicoes:
            eleicoes[eleita] += 1

    # Estabilidade de posição: o ranking muda quando a ordem de apresentação inverte?
    estabilidade = {}
    for juiz in {v["juiz"] for v in validos}:
        pares = {v["ordem"]: v["voto"].get("ranking", []) for v in validos if v["juiz"] == juiz}
        if len(pares) == 2:
            a, b = pares.get("direta", []), pares.get("invertida", [])
            comuns = [r for r in a if r in b]
            concordancia = sum(1 for r in comuns if a.index(r) == b.index(r))
            estabilidade[juiz] = {
                "posicoesIdenticas": concordancia, "de": len(comuns),
                "mesmoTopo": bool(a and b and a[0] == b[0]),
            }

    # Borda entre famílias: o voto de um juiz sobre peça da PRÓPRIA família não
    # conta. Sem isso, quem julga e concorre soma pontos por reconhecer o
    # próprio estilo — e o campeão da bancada seria, em parte, eleito por si.
    familia_de = {nome: PARTICIPANTES[nome].familia for nome in mapa.values()}
    borda_cruzado = {r: 0.0 for r in rotulos}
    votos_cruzados = {r: 0 for r in rotulos}
    for v in validos:
        ranking = [r for r in v["voto"].get("ranking", []) if r in borda_cruzado]
        n = len(ranking)
        for i, r in enumerate(ranking):
            if familia_de.get(mapa[r]) == v["familiaJuiz"]:
                continue
            borda_cruzado[r] += (n - 1 - i)
            votos_cruzados[r] += 1
    # Normaliza pelo número de votos que cada peça de fato recebeu de fora da
    # própria família: peças anthropic são julgadas por 4 votos, as demais por 6.
    borda_cruzado_norm = {
        r: (round(borda_cruzado[r] / votos_cruzados[r], 2) if votos_cruzados[r] else None)
        for r in rotulos}

    # Auto-preferência: cada juiz é também participante.
    auto = {}
    for juiz in {v["juiz"] for v in validos}:
        propria = [r for r, nome in mapa.items() if nome == juiz]
        if not propria:
            continue
        rot = propria[0]
        posicoes = [v["voto"]["ranking"].index(rot) + 1
                    for v in validos if v["juiz"] == juiz and rot in v["voto"].get("ranking", [])]
        outras = [v["voto"]["ranking"].index(rot) + 1
                  for v in validos if v["juiz"] != juiz and rot in v["voto"].get("ranking", [])]
        if posicoes and outras:
            auto[juiz] = {
                "posicaoQueDeuASiMesmo": round(sum(posicoes) / len(posicoes), 2),
                "posicaoQueOsOutrosDeram": round(sum(outras) / len(outras), 2),
                "vantagem": round(sum(outras) / len(outras) - sum(posicoes) / len(posicoes), 2),
            }

    consolidado = {
        "versao": VERSAO,
        "votosTotais": len(votos),
        "votosValidos": len(validos),
        "votosAnulados": [f"{v['juiz']}/{v['ordem']}" for v in votos if v["votoAnulado"]],
        "porParticipante": {
            mapa[r]: {
                "rotuloCego": r,
                "borda": borda[r],
                "bordaEntreFamilias": borda_cruzado[r],
                "bordaEntreFamiliasMedia": borda_cruzado_norm[r],
                "votosDeOutrasFamilias": votos_cruzados[r],
                "eleitoParaProtocolo": eleicoes[r],
                "medias": {c: (round(sum(vs) / len(vs), 2) if vs else None)
                           for c, vs in criterios[r].items()},
                "mediaGeral": (round(sum(x for vs in criterios[r].values() for x in vs)
                                     / max(1, sum(len(vs) for vs in criterios[r].values())), 2)
                               if any(criterios[r].values()) else None),
            } for r in rotulos},
        "estabilidadeDePosicao": estabilidade,
        "autoPreferencia": auto,
        "custoUsd": round(sum(v["custoUsd"] for v in votos), 4),
    }
    (BANCADA / "avaliacao" / "JUIZES_CONSOLIDADO.json").write_text(
        json.dumps(consolidado, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"\n  {len(validos)}/{len(votos)} votos válidos · US$ {consolidado['custoUsd']:.2f}")
    print(f"  {'participante':<11}{'borda':>7}{'cruzada':>9}{'votos':>7}"
          f"{'média':>8}{'eleições':>10}")
    for nome, d in sorted(consolidado["porParticipante"].items(),
                          key=lambda kv: -(kv[1]["bordaEntreFamiliasMedia"] or 0)):
        media = d["mediaGeral"] if d["mediaGeral"] is not None else 0
        cruz = d["bordaEntreFamiliasMedia"]
        print(f"  {nome:<11}{d['borda']:>7.0f}"
              f"{(f'{cruz:.2f}' if cruz is not None else '—'):>9}"
              f"{d['votosDeOutrasFamilias']:>7}{media:>8.2f}"
              f"{d['eleitoParaProtocolo']:>10}")
    for juiz, d in auto.items():
        print(f"  auto-preferência {juiz}: deu a si {d['posicaoQueDeuASiMesmo']}º, "
              f"os outros deram {d['posicaoQueOsOutrosDeram']}º "
              f"(vantagem {d['vantagem']:+.2f} posições)")
    return consolidado


def main() -> int:
    ap = argparse.ArgumentParser(description="julgamento cego da bancada V7")
    ap.add_argument("--cegar", action="store_true")
    ap.add_argument("--julgar", action="store_true")
    ap.add_argument("--consolidar", action="store_true")
    ap.add_argument("--juiz", action="append", default=[])
    ap.add_argument("--timeout", type=int, default=1200)
    args = ap.parse_args()

    if args.cegar:
        cegar()
    if args.julgar:
        for juiz in (args.juiz or JUIZES):
            for invertido in (False, True):
                try:
                    julgar(juiz, invertido=invertido, timeout=args.timeout)
                except Exception as erro:              # noqa: BLE001
                    print(f"  [FALHA] {juiz}/{'inv' if invertido else 'dir'}: {erro}")
    if args.consolidar:
        consolidar()
    if not (args.cegar or args.julgar or args.consolidar):
        ap.error("informe --cegar, --julgar ou --consolidar")
    return 0


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    raise SystemExit(main())
