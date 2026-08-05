# -*- coding: utf-8 -*-
"""forja_forma_artefatos.py — o gate alcança o artefato na forma em que ele existe?

Em 04/08/2026, três gates diferentes falharam pelo mesmo motivo em uma única
tarde, e nenhum deles por causa do nome de um campo:

  - `status_consistent` só lia `reconciliation_report.json`, e o acervo inteiro
    tem `reconciliation_report.md`. Resultado: `warn` em três de três tentativas,
    para sempre. O gate nunca soube dizer `pass`.
  - `quotes_compared` só lia `citation_checklist.json`, e sete dos nove
    checklists reais são markdown. O gate não produzia veredito sobre 78% do
    material que devia examinar.
  - `jurisdictional_question_defined` já tinha sido corrigido antes pelo mesmo
    motivo (12 blueprints em markdown contra 3 em JSON).

A dívida de esquema que essa frente vinha tratando era a do VOCABULÁRIO: campos
com nomes diferentes para a mesma coisa, resolvida pelo leitor canônico em
`forja_artefatos.py`. Esta é outra, e mais perigosa, porque é silenciosa: o gate
não lê o campo errado, ele não abre o arquivo. Não há erro, não há exceção, não
há achado — há um `warn` educado, ou um veredito que simplesmente não aparece.
O operador lê "sem achados" e entende "conferido".

O instrumento é simples: varrer o acervo, agrupar os artefatos por radical, e
apontar todo radical que existe em mais de uma forma. Cada um deles é um lugar
onde um leitor pode estar enxergando metade do material.

Uso:
    python forja_forma_artefatos.py
"""
from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

VERSAO = "FORJA-FORMA-ARTEFATOS-v1"
RAIZ = Path(__file__).resolve().parent

# Radicais que não são artefato de fase — ruído de build, cache e relatório.
_IGNORAR = re.compile(
    r"(?i)^(readme|leia-?me|index|mapa_ia|sha256sums|package-lock|requirements|"
    r"__init__|conftest|build_f\d+|.*_relatorio|.*_report_\d+)$")
_FORMAS = {".json", ".md", ".yaml", ".yml", ".txt", ".csv"}
# Sufixo de versionamento que o harness carimba: `blueprint-019df3d6bc35.md`.
_SUFIXO_VERSAO = re.compile(r"-[0-9a-f]{8,16}$")


def _radical(caminho: Path) -> str:
    return _SUFIXO_VERSAO.sub("", caminho.stem)


def _lidos_pelo_censo() -> set:
    """Os nomes de arquivo que o censo abre, extraídos do próprio código.

    Ler o código em vez de manter uma lista à parte é deliberado: uma lista à
    parte envelhece em silêncio, que é exatamente o defeito que este módulo
    existe para pegar.
    """
    fonte = (RAIZ / "forja_recomputo_censo.py").read_text(encoding="utf-8")
    return set(re.findall(r'"([a-z0-9_]+\.(?:json|md))"', fonte))


def censo_de_formas(raiz=None) -> dict:
    base = Path(raiz) if raiz else (RAIZ / "state")
    formas: dict = defaultdict(set)
    contagem: dict = defaultdict(lambda: defaultdict(int))
    orfaos: dict = defaultdict(list)

    for arquivo in base.rglob("*"):
        if not arquivo.is_file() or arquivo.suffix.lower() not in _FORMAS:
            continue
        radical = _radical(arquivo)
        if _IGNORAR.match(radical):
            continue
        formas[radical].add(arquivo.suffix.lower())
        contagem[radical][arquivo.suffix.lower()] += 1
        orfaos[radical].append(arquivo)

    lidos = _lidos_pelo_censo()
    ambiguos = {}
    cegueiras = []
    for radical, sufixos in sorted(formas.items()):
        if len(sufixos) < 2:
            continue
        ambiguos[radical] = {s: contagem[radical][s] for s in sorted(sufixos)}
        nao_lidas = [s for s in sorted(sufixos) if f"{radical}{s}" not in lidos]
        lidas = [s for s in sorted(sufixos) if f"{radical}{s}" in lidos]
        # Só é cegueira onde o censo JÁ lê uma das formas: aí ele examina o
        # artefato e ignora parte do material. Radical que nenhum leitor abre
        # não é cegueira deste instrumento — é assunto do censo de gates.
        if not (lidas and nao_lidas):
            continue
        # Cegueira só existe onde a forma ignorada está SOZINHA na pasta. Um
        # `.md` ao lado do `.json` que o leitor abre não esconde nada: o gate vê
        # o material pela outra porta. Contar esse caso como cegueira acusava o
        # `adversarial_audit` do CASO-23, onde as duas formas convivem —
        # ruído que treinaria o operador a ignorar a catraca.
        invisiveis = [a for a in orfaos.get(radical, [])
                      if a.suffix.lower() in nao_lidas
                      and not any((a.parent / f"{radical}{s}").is_file() for s in lidas)]
        if invisiveis:
            cegueiras.append({
                "artefato": radical,
                "lidas": lidas,
                "ignoradas": sorted({a.suffix.lower() for a in invisiveis}),
                "arquivosIgnorados": len(invisiveis),
                "pastas": sorted(str(a.parent) for a in invisiveis)[:4],
            })

    return {
        "versao": VERSAO,
        "radicaisExaminados": len(formas),
        "radicaisEmMaisDeUmaForma": ambiguos,
        "cegueirasDeForma": sorted(cegueiras, key=lambda c: -c["arquivosIgnorados"]),
    }


def _relatar(laudo: dict) -> None:
    print("=" * 74)
    print("CENSO DE FORMAS — o leitor alcança o artefato na forma em que ele existe?")
    print("=" * 74)
    print(f"  radicais examinados          : {laudo['radicaisExaminados']}")
    print(f"  existem em mais de uma forma : {len(laudo['radicaisEmMaisDeUmaForma'])}")
    print(f"  cegueiras de forma           : {len(laudo['cegueirasDeForma'])}")

    if laudo["cegueirasDeForma"]:
        print("\n  CEGUEIRAS — o leitor abre uma forma e ignora a outra")
        for item in laudo["cegueirasDeForma"]:
            print(f"    {item['artefato']:38} lê {','.join(item['lidas'])} "
                  f"e ignora {','.join(item['ignoradas'])} "
                  f"({item['arquivosIgnorados']} arquivo(s))")

    print("\n  ARTEFATOS EM MAIS DE UMA FORMA (informativo)")
    for radical, contagem in list(laudo["radicaisEmMaisDeUmaForma"].items())[:20]:
        detalhe = " ".join(f"{s}={n}" for s, n in contagem.items())
        print(f"    {radical:38} {detalhe}")


if __name__ == "__main__":  # pragma: no cover
    import argparse

    ap = argparse.ArgumentParser(description="Mede artefatos que existem em mais de uma forma.")
    ap.add_argument("--json", metavar="ARQUIVO")
    args = ap.parse_args()

    laudo = censo_de_formas()
    _relatar(laudo)
    if args.json:
        Path(args.json).write_text(json.dumps(laudo, ensure_ascii=False, indent=2),
                                   encoding="utf-8")
        print(f"\ncenso de formas: {args.json}")
