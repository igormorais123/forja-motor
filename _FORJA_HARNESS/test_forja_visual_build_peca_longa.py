# -*- coding: utf-8 -*-
"""test_forja_visual_build_peca_longa.py — a peça grande e com figura.

Em 04/08/2026, ao compor pela entrada canônica o markdown real do Cafelana —
18 seções e 2 figuras —, `forja_visual_build.build` estourou duas vezes seguidas
por motivos independentes, e nenhum dos dois tinha teste:

  1. `IndexError` em `medina_visual_kit.abre()`. Os numerais romanos das seções
     vinham de uma lista literal que parava em ``XV``, indexada direto. A 16ª
     seção derrubava a composição inteira. Teto silencioso em constante é dívida
     esperando o documento comprido — e quem chega lá é justamente a peça grande,
     que é a mais cara de refazer.
  2. `TypeError: WindowsPath is not JSON serializable` ao gravar o
     `F8_QA_ESTRUTURAL.json`. `medina_svg_colisao.analisar` devolvia no laudo o
     `Path` que recebeu. Consequência exata: peça SEM figura passava e peça COM
     figura quebrava — o pior formato de falha, porque o caminho feliz do teste
     de fumaça é o que não tem figura.

Os dois só apareceram porque a rota canônica foi exercitada com material real em
vez de sintético. O teste sintético anterior compunha um parágrafo e não tinha
como encontrar nenhum dos dois.

O terceiro caso guarda o veredito de layout no resumo: a régua tipográfica sempre
rodou dentro do build, mas o veredito morria no JSON e não chegava a quem lê o
resultado. Aqui se cobra a PRESENÇA do veredito, nunca o seu valor — reprovar a
peça é decisão de política, presa ao F8-S.

Uso: python test_forja_visual_build_peca_longa.py   (exit 0 = ok)
"""
from __future__ import annotations

import io
import json
import sys
import tempfile
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

RAIZ = Path(__file__).resolve().parent
FERRAMENTAS = RAIZ.parent / "_FERRAMENTAS"
if str(FERRAMENTAS) not in sys.path:
    sys.path.insert(0, str(FERRAMENTAS))

# Markdown real, auditado, com seções acima do antigo teto e com figuras. É a
# âncora do teste: se ele sumir do acervo, o teste diz isso em vez de passar
# calado sobre um caminho que não existe mais.
PECA_ANCORA = RAIZ / (
    "state/case-cafelana-geral-reconstrucao-20260803/runs/run-cafelana-f7-repair-20260804"
    "/F7_AUDITORIA_JURIDICA_FACTUAL/attempt-bd2edd42d0644bbba8379da16dc37b2d"
    "/final_markdown.md"
)
SECOES_MINIMAS = 16


def _casos() -> list[tuple[str, bool, str]]:
    resultados: list[tuple[str, bool, str]] = []

    def caso(nome: str, condicao: bool, detalhe: str = "") -> None:
        resultados.append((nome, bool(condicao), detalhe))

    from medina_visual_kit import romano

    esperado = {1: "I", 4: "IV", 9: "IX", 15: "XV", 16: "XVI", 19: "XIX",
                24: "XXIV", 40: "XL", 90: "XC"}
    obtido = {n: romano(n) for n in esperado}
    caso("numeral romano de seção não tem teto", obtido == esperado, f"{obtido}")

    from medina_svg_colisao import analisar

    svgs = sorted(FERRAMENTAS.glob("**/*.svg"))[:1] or sorted(RAIZ.parent.rglob("*.svg"))[:1]
    if svgs:
        laudo = analisar(svgs[0])
        caso("laudo de colisão é serializável em JSON",
             isinstance(laudo.get("svg"), str) and json.dumps(laudo, ensure_ascii=False))
    else:
        caso("laudo de colisão é serializável em JSON", False, "nenhum SVG no acervo")

    if not PECA_ANCORA.is_file():
        caso("peça-âncora existe no acervo", False, str(PECA_ANCORA))
        return resultados
    caso("peça-âncora existe no acervo", True)

    texto = PECA_ANCORA.read_text(encoding="utf-8")
    secoes = sum(1 for linha in texto.splitlines() if linha.startswith("## "))
    caso(f"peça-âncora ainda tem {SECOES_MINIMAS}+ seções (senão não exercita o teto)",
         secoes >= SECOES_MINIMAS, f"{secoes} seções")

    from forja_visual_build import build

    tmp = Path(tempfile.mkdtemp(prefix="forja_peca_longa_"))
    md = tmp / "peca.md"
    md.write_text(texto, encoding="utf-8")
    try:
        resumo = build(md, tmp / "out", "Peça longa", montar_word=False)
    except Exception as erro:  # noqa: BLE001
        caso("build da peça longa com figura conclui", False, repr(erro))
        return resultados

    caso("build da peça longa com figura conclui", True)
    caso("build produziu figuras (senão o bug do Path não é exercitado)",
         bool(resumo.get("figuras")), str(resumo.get("figuras")))
    caso("F8_QA_ESTRUTURAL.json foi gravado",
         (tmp / "out" / "F8_QA_ESTRUTURAL.json").is_file())

    veredito = resumo.get("veredictoLayout") or {}
    caso("veredito de layout chega ao resumo do build",
         "aprovado" in veredito and isinstance(veredito.get("achadosP0"), list))
    cobertura = veredito.get("cobertura") or {}
    caso("veredito de layout traz as três coberturas",
         {"justificationCoverage", "fontCoverage", "sizeCoverage"} <= set(cobertura))

    # A rota canônica tem de passar no PRÓPRIO gate. Isso valeu 100% nas três
    # dimensões pela primeira vez em 04/08/2026, e só depois que três falsos
    # positivos do gate contra o desenho da casa foram corrigidos: o título em
    # caixa mista lido como corpo, a linha de status lida como corpo e o pull
    # quote em moldura lido como citação recuada.
    #
    # É a checagem mais valiosa deste arquivo, porque é a única que pega o
    # produtor e o auditor discordando — e quando isso acontece, um dos dois
    # está errado e ninguém percebe enquanto os dois rodam separados.
    abaixo = {k: v for k, v in cobertura.items() if isinstance(v, (int, float)) and v < 1.0}
    caso("a rota canônica passa no próprio gate de layout, 100% nas três dimensões",
         not abaixo, f"{abaixo}")
    return resultados


def main() -> int:
    resultados = _casos()
    falhas = [x for x in resultados if not x[1]]
    for nome, ok, detalhe in resultados:
        if not ok:
            print(f"  FALHOU: {nome}" + (f" — {detalhe}" if detalhe else ""))
    if falhas:
        print(f"REGRESSÃO: {len(falhas)} de {len(resultados)} verificações falharam")
        return 1
    print(f"ok: {len(resultados)} verificações — a peça longa com figura compõe pela rota "
          "canônica e o veredito de layout chega ao resumo")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
