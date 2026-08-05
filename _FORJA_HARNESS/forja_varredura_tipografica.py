# -*- coding: utf-8 -*-
"""forja_varredura_tipografica.py — quem está fora do padrão Word do escritório?

O padrão existe desde 08/07/2026: Times New Roman 12, justificado, recuo de 1ª
linha de 2,0 a 2,5 cm. Até 04/08 a esteira não sabia dizer quem saía dele,
porque o gate capaz de medir só era chamado dentro de uma fase F8 — e a F8 é a
fase que menos roda. Um padrão sem instrumento que o meça é uma intenção.

Este módulo existe porque a medição de 04/08 nasceu como script descartável, e a
lição 1 do plano visual diz que recurso dependente de esforço manual por caso não
sobrevive ao volume. Foi assim que a edição visual parou em 10/07 sem ninguém
notar.

Duas armadilhas que a primeira medição caiu, e que o código evita:

  1. **O universo.** 361 DOCX no acervo, 316 com achado — número inútil, porque
     o acervo é dominado por minuta de origem, prompt, anexo de terceiro e
     artefato de teste. Tentei filtrar pelo timbre, que seria a prova estrutural
     correta: 312 dos 361 têm timbre, porque o template é usado para tudo. O
     recorte que funciona é prosaico — nome de entregável, exclusão explícita de
     material de terceiro e de teste, e piso de parágrafos.

  2. **A leitura.** Contar `<w:jc>` cru no `document.xml` produz números
     alarmantes e falsos: parágrafo que herda a justificação do estilo não tem
     `w:jc` nenhum, e o XML do corpo inclui tabelas e caixas. Quem lê certo é
     `audit_docx_layout`, que percorre a cadeia de estilos. Pela leitura crua o
     relatório do Cafelana aparecia com 0% de justificação; pela correta, 100%.

Uso:
    python forja_varredura_tipografica.py
    python forja_varredura_tipografica.py --json saida.json --limite 20
"""
from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path

VERSAO = "FORJA-VARREDURA-TIPOGRAFICA-v1"
RAIZ = Path(__file__).resolve().parent
FABRICA = RAIZ.parent

# Nome de entregável. Não é elegante e é o que funciona: veja no cabeçalho por
# que o timbre — a alternativa estrutural — não separa nada neste acervo.
ENTREGAVEL = re.compile(
    r"(?i)(FINAL|ASSINATURA|PROTOCOL|ENTREGA|_V\d|MEMORIAIS|IMPUGNACAO|PARECER|PETICAO|"
    r"CONTRARRAZOES|AGRAVO|EMBARGOS)")
# Material que não é nosso, ou não é peça. Cada entrada tem motivo:
#   ORIGINAL RECEBIDO / VERSÃO HUMANA — documento de terceiro, não se cobra dele
#     o padrão da casa;
#   SOURCE_ / pre_layout / audited_source / _tmp_ / __ / TEST — estágio interno
#     anterior à diagramação;
#   Prompt — arquivo de instrução, não peça.
EXCLUIR = ("~$", "_compare_base", "TEMPLATE_", "SOURCE_", "__", "pre_layout",
           "audited_source", "_tmp_", "TEST", "ORIGINAL RECEBIDO", "VERSÃO HUMANA",
           "propostas_justificacao", "node_modules")
_PROMPT = re.compile(r"(?i)^\d+\.\s*Prompt\b|\bPrompt\s+\d+\b")

PISO_PARAGRAFOS = 20


def _e_entregavel(caminho: Path) -> bool:
    if any(t in str(caminho) for t in EXCLUIR):
        return False
    if _PROMPT.search(caminho.name):
        return False
    return bool(ENTREGAVEL.search(caminho.name))


def _caso_de(caminho: Path) -> str:
    """A pasta de caso: o primeiro nível abaixo da raiz da fábrica."""
    try:
        relativo = caminho.resolve().relative_to(FABRICA.resolve())
    except ValueError:
        return str(caminho.parent)
    return relativo.parts[0] if relativo.parts else "."


_MARCADORES_VERSAO = frozenset({
    "ajustada", "ajustado", "alteracao", "alteracoes", "antes", "assinatura",
    "before", "controle", "corrigida", "corrigido", "de", "diagram", "final",
    "font", "fonts", "interna", "interno", "justificada", "justificado", "limpa",
    "limpo", "para", "proposta", "proposto", "qa", "revisao", "revisado",
    "revisada", "teste", "test", "versao", "visual",
})
_MARCADORES_CORRECAO = ("corrigid", "justificad", "revisad", "ajustad", "qa_visual")


def _familia_de(caminho: Path) -> tuple[str, ...]:
    """Extrai a identidade estável da peça, removendo rótulos de versão/status."""
    nome = unicodedata.normalize("NFKD", Path(caminho).stem)
    nome = nome.encode("ascii", "ignore").decode("ascii").lower()
    tokens = re.findall(r"[a-z0-9]+", nome)
    return tuple(
        token for token in tokens
        if token not in _MARCADORES_VERSAO and not re.fullmatch(r"v\d+[a-z]*", token)
    )


def _tem_marca_correcao(nome: str) -> bool:
    normalizado = unicodedata.normalize("NFKD", nome).encode("ascii", "ignore").decode("ascii").lower()
    return any(marca in normalizado for marca in _MARCADORES_CORRECAO)


_TOKENS_GENERICO_CASO = frozenset({
    "agravo", "assinatura", "cafelana", "contrarrazoes", "de", "edcl", "embargos",
    "escritorio", "entregas", "fabio", "gestao", "impugnacao", "memorial", "memoriais",
    "parecer", "peticao", "plano", "relatorio", "revisao",
})


def _tokens_do_caminho(caminho: Path) -> set[str]:
    try:
        relativo = caminho.resolve().relative_to(FABRICA.resolve())
        partes = relativo.parts[:-1]
    except ValueError:
        partes = caminho.parts[:-1]
    tokens = set()
    for parte in partes:
        normalizado = unicodedata.normalize("NFKD", parte).encode("ascii", "ignore").decode("ascii").lower()
        tokens.update(re.findall(r"[a-z0-9]+", normalizado))
    return tokens


def _mesmo_caso(a: Path, b: Path, familia: tuple[str, ...]) -> bool:
    caso_a, caso_b = _caso_de(a), _caso_de(b)
    if caso_a == caso_b and caso_a not in {"gestao_escritorio", "entregas_fabio_osorio"}:
        return True
    estaveis = set(familia) - _TOKENS_GENERICO_CASO
    comuns = estaveis & _tokens_do_caminho(a) & _tokens_do_caminho(b)
    return len(comuns) >= 2


def _marcar_superadas(medidas: list) -> None:
    """Uma peça corrigida depois não é defeito vivo — é história.

    Achado que motivou isto: o `01_PARECER_NATURA_CABREUVA_FINAL_LIMPO_PARA_
    ASSINATURA` foi medido em 8,2% de justificação e apontado como o caso mais
    grave do acervo. Ele é de 20/07 às 19h24. Ao lado dele, de 21/07 às 20h39,
    está o `..._CORRIGIDO_JUSTIFICADO` com os mesmos 245 parágrafos e 100% nas
    três dimensões: o escritório detectou e consertou no dia seguinte, sozinho.
    Acusar a versão antiga é o mesmo erro que o censo cometeu ao parear tentativa
    descartada com estratégia promovida — medir o que foi substituído.

    O critério é conservador de propósito: mesmo CASO, mesma família nominal,
    o candidato precisa carregar marca explícita de correção, contagem de
    parágrafos próxima (o corrigido pode ganhar ou perder um) e conformidade
    estritamente melhor nas TRÊS dimensões. Sem os quatro, a peça continua
    contando. Isso evita parear documentos diferentes do mesmo caso só porque
    têm tamanho parecido.

    O agrupamento é por caso e não por pasta porque a correção costuma nascer em
    outra pasta que a original — no Natura, o pacote pós-auditoria de 20/07 e a
    correção de 21/07 são diretórios diferentes do mesmo caso. Agrupar por pasta
    deixava a versão superada contando como defeito vivo.
    """
    for item in medidas:
        item["superadaPor"] = None
    por_familia: dict = {}
    for item in medidas:
        familia = _familia_de(Path(item["caminho"]))
        por_familia.setdefault(familia, []).append(item)

    for irmas in por_familia.values():
        for item in irmas:
            for outra in irmas:
                if outra is item:
                    continue
                if not _tem_marca_correcao(outra["peca"]):
                    continue
                familia_item = _familia_de(Path(item["caminho"]))
                if familia_item != _familia_de(Path(outra["caminho"])):
                    continue
                if len(familia_item) < 3 or not _mesmo_caso(
                        Path(item["caminho"]), Path(outra["caminho"]), familia_item):
                    continue
                if abs(outra["paragrafos"] - item["paragrafos"]) > 2:
                    continue
                if (outra["justificacao"] > item["justificacao"]
                        and outra["tamanho"] > item["tamanho"]
                        and outra["fonte"] > item["fonte"]):
                    item["superadaPor"] = outra["peca"]
                    break


def varrer(raiz=None, piso=PISO_PARAGRAFOS) -> dict:
    from forja_docx_layout import audit_docx_layout

    base = Path(raiz) if raiz else FABRICA
    medidas, erros = [], []
    vistos = set()

    for arquivo in sorted(base.rglob("*.docx")):
        if not _e_entregavel(arquivo):
            continue
        try:
            if arquivo.stat().st_size < 5000:
                continue
            laudo = audit_docx_layout(arquivo)
        except Exception as erro:  # noqa: BLE001
            erros.append(f"{arquivo.name[:60]}: {type(erro).__name__}")
            continue
        m = laudo.get("metrics") or {}
        paragrafos = m.get("bodyParagraphs") or 0
        if paragrafos < piso:
            continue
        # O mesmo entregável aparece copiado em pasta de entrega, de caso e de
        # backup. Contar três vezes distorce qualquer proporção.
        chave = (
            arquivo.name,
            paragrafos,
            round(m.get("justificationCoverage", 0), 4),
            round(m.get("sizeCoverage", 0), 4),
            round(m.get("fontCoverage", 0), 4),
        )
        if chave in vistos:
            continue
        vistos.add(chave)
        medidas.append({
            "peca": arquivo.name,
            "caminho": str(arquivo),
            "paragrafos": paragrafos,
            "justificacao": round(m.get("justificationCoverage", 0), 4),
            "tamanho": round(m.get("sizeCoverage", 0), 4),
            "fonte": round(m.get("fontCoverage", 0), 4),
        })

    _marcar_superadas(medidas)
    vivas = [x for x in medidas if not x["superadaPor"]]

    def abaixo(campo, limite):
        return [x for x in vivas if x[campo] < limite]

    return {
        "versao": VERSAO,
        "entregaveisMedidos": len(vivas),
        "superadasPorVersaoCorrigida": sorted(
            {x["peca"]: x["superadaPor"] for x in medidas if x["superadaPor"]}.items()),
        "erros": erros,
        "foraDoPadrao": {
            "justificacaoAbaixoDe50": len(abaixo("justificacao", 0.5)),
            "justificacaoAbaixoDe90": len(abaixo("justificacao", 0.9)),
            "tamanhoAbaixoDe90": len(abaixo("tamanho", 0.9)),
            "fonteAbaixoDe90": len(abaixo("fonte", 0.9)),
        },
        # Peça que sai do padrão nas TRÊS dimensões ao mesmo tempo não é descuido
        # de formatação: é peça que não passou pela diagramação da casa.
        "foraNasTresDimensoes": sorted(
            (x for x in vivas
             if x["justificacao"] < 0.5 and x["tamanho"] < 0.5 and x["fonte"] < 0.5),
            key=lambda x: x["justificacao"]),
        "piores": sorted(vivas, key=lambda x: (x["justificacao"], x["tamanho"]))[:20],
    }


def _relatar(laudo: dict, limite: int) -> None:
    print("=" * 78)
    print("VARREDURA TIPOGRÁFICA — quem sai do padrão Word do escritório")
    print("=" * 78)
    print(f"  entregáveis distintos medidos : {laudo['entregaveisMedidos']}")
    f = laudo["foraDoPadrao"]
    print(f"  justificação abaixo de 50%    : {f['justificacaoAbaixoDe50']}")
    print(f"  justificação abaixo de 90%    : {f['justificacaoAbaixoDe90']}")
    print(f"  tamanho 12 pt abaixo de 90%   : {f['tamanhoAbaixoDe90']}")
    print(f"  Times New Roman abaixo de 90% : {f['fonteAbaixoDe90']}")
    if laudo["erros"]:
        print(f"\n  não abriram ({len(laudo['erros'])}): {', '.join(laudo['erros'][:4])}")

    if laudo["foraNasTresDimensoes"]:
        print("\n  FORA NAS TRÊS DIMENSÕES — não passaram pela diagramação da casa")
        for x in laudo["foraNasTresDimensoes"]:
            print(f"    just {x['justificacao']*100:5.1f}%  tam {x['tamanho']*100:5.1f}%  "
                  f"fonte {x['fonte']*100:5.1f}%  {x['peca'][:56]}")

    print("\n  PIORES POR JUSTIFICAÇÃO")
    print("    just%   tam% fonte%   pgf  peça")
    for x in laudo["piores"][:limite]:
        print(f"    {x['justificacao']*100:5.1f} {x['tamanho']*100:6.1f} "
              f"{x['fonte']*100:6.1f} {x['paragrafos']:5}  {x['peca'][:56]}")


if __name__ == "__main__":  # pragma: no cover
    import argparse

    ap = argparse.ArgumentParser(description="Mede a conformidade tipográfica dos entregáveis.")
    ap.add_argument("--json", metavar="ARQUIVO")
    ap.add_argument("--limite", type=int, default=12)
    args = ap.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    laudo = varrer()
    _relatar(laudo, args.limite)
    if args.json:
        Path(args.json).write_text(json.dumps(laudo, ensure_ascii=False, indent=2),
                                   encoding="utf-8")
        print(f"\nvarredura: {args.json}")
