# -*- coding: utf-8 -*-
"""FORJA — entrada ÚNICA de produção da peça com assinatura visual (Onda 2).

Decisão de arquitetura (30/07/2026, Igor + Efesto). Havia duas rotas com poder
equivalente de gerar entregável:

  rota visual   forja_visual.compor() -> PecaVisual + SVG nativo no OOXML:
                a linguagem visual aprovada em julho (CASO-04, CASO-14, José
                CASO-15, CASO-16).

Não há uma segunda rota de materialização. Os SVGs são embutidos diretamente no
DOCX como ``image/svg+xml`` e o QA lê OOXML, fidelidade, tipografia, metadados e
geometria. A FORJA não chama ``forja_render_docx.py``, Word COM, PDF ou PNG.

Uso:
    python forja_visual_build.py <peca.md> <saida_dir> ["Título"]
"""
import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

FORJA = Path(__file__).resolve().parent
RAIZ = FORJA.parent
sys.path.insert(0, str(FORJA))
sys.path.insert(0, str(RAIZ / "_FERRAMENTAS"))

from forja_visual_mapa_gen import gerar_mapa                     # noqa: E402
from forja_visual_figuras import (BRIEF_NOME, carregar_brief,    # noqa: E402
                                  gerar_figuras, validar_brief)


def _tipo_produto(texto, titulo):
    import re
    abertura = (titulo + "\n" + texto[:1800]).upper()
    if re.search(r"\b(ESTUDO|DIAGN[ÓO]STICO|RELAT[ÓO]RIO|PARECER|MATRIZ|CHECKLIST)\b",
                 abertura):
        return "estudo"
    return "peca"


def _case_dir_efetivo(md_path, declarado=None):
    """Resolve a pasta do caso sem permitir que a omissão do CLI desligue gates.

    O feedback de 10/08/2026 depende de confrontar a peça com os anexos do
    comando. Antes, bastava não passar ``--case-dir`` para esse contexto sumir.
    Procuramos o comando nos ancestrais próximos e, na ausência, usamos a pasta
    do markdown — sempre há um contexto concreto, nunca ``None`` silencioso.
    """
    if declarado:
        return Path(declarado)
    atual = Path(md_path).resolve().parent
    for candidato in (atual, *list(atual.parents)[:4]):
        if (candidato / "COMANDO_DO_EMAIL.md").is_file():
            return candidato
        try:
            if any(p.is_dir() and "anexos do email" in p.name.casefold()
                   for p in candidato.iterdir()):
                return candidato
        except OSError:
            pass
        if candidato == RAIZ:
            break
    return atual


def _rebind_integrity_ledgers(docx_path):
    """Vincula os recibos ao DOCX que efetivamente sai da porta única.

    ``compor()`` grava os dois recibos antes de ``inserir_svgs()`` alterar o
    pacote OOXML. O hash antigo, embora verdadeiro naquele instante, passava a
    identificar um arquivo que já não existia. Recompomos somente o campo de
    integridade depois da última mutação do DOCX e deixamos essa mudança
    declarada no próprio recibo.
    """
    docx_path = Path(docx_path)
    digest = hashlib.sha256(docx_path.read_bytes()).hexdigest()
    recibos = (
        docx_path.with_name("FIDELIDADE_VISUAL.json"),
        docx_path.with_name(docx_path.stem + "_PORTA_UNICA.json"),
    )
    atualizados = []
    instante = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
    for recibo in recibos:
        if not recibo.is_file():
            continue
        dados = json.loads(recibo.read_text(encoding="utf-8"))
        dados["docxSha256"] = digest
        dados["integridadeVinculadaAposSvgOoxml"] = True
        dados["integridadeVinculadaEm"] = instante
        recibo.write_text(json.dumps(dados, ensure_ascii=False, indent=2),
                          encoding="utf-8")
        atualizados.append(str(recibo))
    return {"docxSha256": digest, "recibosAtualizados": atualizados}


def build(md_path, out_dir, titulo="Peça FORJA", tipo=None, montar_word=True,
          *, case_dir=None, ledger_path=None, base_dir=None):
    """Compõe a peça em edição visual law. Devolve o resumo com lastro e tempos."""
    inicio = time.monotonic()
    md_path, out_dir = Path(md_path), Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    texto = md_path.read_text(encoding="utf-8")
    tipo = tipo or _tipo_produto(texto, titulo)
    case_dir = _case_dir_efetivo(md_path, case_dir)

    # ---- F7 fail-closed: nenhum artefato nasce com P0 ----
    from forja_verificador import verificar as gates_forja
    from forja_lastro import material_economico
    from forja_metricas_f7 import metricas_f7
    viol = gates_forja(
        texto, tipo, case_dir=case_dir, ledger=(
            json.loads(Path(ledger_path).read_text(encoding="utf-8"))
            if ledger_path else None
        ), base_dir=base_dir,
        exigir_economico=material_economico(texto),
    )
    gate = {"total": len(viol),
            "p0": sum(1 for x in viol if x["sev"] == "P0"),
            "p1": sum(1 for x in viol if x["sev"] == "P1"),
            "violacoes": viol}
    f7 = {"arquivo": str(md_path), "tipo": tipo,
          "mdSha256": hashlib.sha256(texto.encode("utf-8")).hexdigest(),
          **gate, **metricas_f7(texto),
          "geradoEm": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")}
    (out_dir / "F7_VERIFICADOR_FORJA.json").write_text(
        json.dumps(f7, ensure_ascii=False, indent=2), encoding="utf-8")
    if gate["p0"]:
        amostra = "; ".join(f"{i['gate']}: {i['problema']}"
                            for i in viol if i["sev"] == "P0")[:900]
        raise RuntimeError(f"F7 REPROVADO — {gate['p0']} P0: {amostra}")

    # ---- F7.5: brief visual declarado (figuras semânticas) ----
    brief = carregar_brief(md_path)
    problemas_brief = validar_brief(brief, texto) if brief else []
    if problemas_brief:
        raise RuntimeError("BRIEF VISUAL REPROVADO (" + BRIEF_NOME + "): "
                           + "; ".join(problemas_brief[:8]))
    t_gates = time.monotonic()

    # ---- mapa (Onda 1A) + figuras (Onda 1B) ----
    mapa = gerar_mapa(md_path, tipo=tipo)
    figs = gerar_figuras(texto, out_dir / "_figuras", mapa, brief=brief, tipo=tipo)
    t_mapa = time.monotonic()

    # ---- composição visual ----
    from forja_visual import compor
    destino = out_dir / (md_path.stem + "_VISUAL_LAW.docx")
    compor(md_path, destino, mapa, case_dir=case_dir,
           ledger_path=ledger_path, base_dir=base_dir)
    t_compor = time.monotonic()

    # ---- SVG nativo no OOXML + QA estrutural (sem renderização) ----
    svg_embeds = {}
    if montar_word and figs:
        from forja_svg_docx import inserir_svgs
        svg_embeds = inserir_svgs(destino, figs)
    integridade = _rebind_integrity_ledgers(destino)
    from forja_visual_qa_structural import auditar_documento
    qa_estrutural = auditar_documento(
        destino,
        markdown=md_path,
        svgs=[value[0] for value in figs.values()],
    )
    (out_dir / "F8_QA_ESTRUTURAL.json").write_text(
        json.dumps(qa_estrutural, ensure_ascii=False, indent=2), encoding="utf-8")
    t_fim = time.monotonic()

    # A régua tipográfica já era executada aqui — o que não saía do JSON era o
    # VEREDITO dela. `build()` interrompe por P0 do F7 e segue calado diante de
    # um laudo de layout reprovado, o que faz a medição existir sem consequência:
    # o operador lê "build ok" e o defeito fica no arquivo que ninguém abre.
    # O resumo abaixo põe o veredito ao lado do gate do F7. Continua NÃO
    # bloqueante: travar a rota é decisão de política presa ao F8-S.
    layout = qa_estrutural.get("layoutAudit") or {}
    veredito_layout = {
        "aprovado": bool(layout.get("approved")),
        "achadosP0": sorted({
            f.get("code") for f in layout.get("findings") or []
            if f.get("severity") == "P0" and f.get("code")
        }),
        "cobertura": {
            k: v for k, v in (layout.get("metrics") or {}).items()
            if k.endswith("Coverage")
        },
    }

    (out_dir / "mapa.json").write_text(
        json.dumps(mapa, ensure_ascii=False, indent=2), encoding="utf-8")

    # ---- gate F8-S em modo OBSERVAÇÃO ----
    # Registra o que reprovaria; não bloqueia. A ativação bloqueante depende da
    # conferência humana das peças de calibração (ordem do Igor, 30/07/2026).
    from forja_assinatura_visual import avaliar as avaliar_assinatura
    # A rota canônica insere SVG nativo no OOXML e não passa por Word COM, então
    # normalmente não há PDF e não há contagem física de páginas. Um PDF irmão
    # pode ser sobra de uma montagem anterior e não prova a extensão deste DOCX;
    # por isso a porta única não o infere. A etapa que materializa o PDF deve
    # chamar o avaliador com a contagem real e persistir o laudo final.
    laudo = avaliar_assinatura(destino, None, tipo, buscar_pdf_irmao=False)
    (out_dir / "F8S_ASSINATURA_VISUAL.json").write_text(
        json.dumps(laudo, ensure_ascii=False, indent=2), encoding="utf-8")

    resumo = {
        "docx": str(destino),
        "pdf": None,
        "paginas": None,
        "tipoProduto": tipo,
        "rota": "visual_law_canonica_svg_ooxml",
        "briefVisual": bool(brief),
        "figuras": sorted(k.strip("{}") for k in figs),
        "svgEmbeds": svg_embeds,
        "mapa": {"pulls": len(mapa.get("pulls") or []),
                 "caixas": len(mapa.get("caixas") or []),
                 "figs": len(mapa.get("figs") or []),
                 "linhasSintese": len(mapa.get("linhas_sintese") or {})},
        "lastroFidelidadeTextual": str(destino.with_name("FIDELIDADE_VISUAL.json")),
        "integridadeFinal": integridade,
        "qaEstrutural": str(out_dir / "F8_QA_ESTRUTURAL.json"),
        "veredictoLayout": veredito_layout,
        # COM QUE PARÂMETROS esta peça foi construída. Sem isto, um laudo verde
        # não distingue "os gates econômicos rodaram e aprovaram" de "os gates
        # econômicos nem foram chamados, porque ninguém passou o ledger" — e a
        # segunda hipótese é invisível no resultado. Só caminhos e sinalizadores;
        # nenhum conteúdo de caso, nenhum segredo.
        "executadoCom": {
            "ledgerPath": str(ledger_path) if ledger_path else None,
            "caseDir": str(case_dir) if case_dir else None,
            "baseDir": str(base_dir) if base_dir else None,
            "montarWord": bool(montar_word),
            "materialEconomico": bool(material_economico(texto)),
            "briefVisualDeclarado": bool(brief),
        },
        "renderingUsed": False,
        "gatesForjaVerificador": gate,
        "assinaturaVisual": {"conforme": laudo["conforme"],
                             "modo": laudo["modo"],
                             "achados": [a["codigo"] for a in laudo["achados"]],
                             "laudo": str(out_dir / "F8S_ASSINATURA_VISUAL.json")},
        "tempoSegundos": {
            "gates": round(t_gates - inicio, 1),
            "mapaEFiguras": round(t_mapa - t_gates, 1),
            "composicao": round(t_compor - t_mapa, 1),
            "svgOoxmlQa": round(t_fim - t_compor, 1),
            "total": round(t_fim - inicio, 1),
        },
    }
    (out_dir / "VISUAL_BUILD.json").write_text(
        json.dumps(resumo, ensure_ascii=False, indent=2), encoding="utf-8")
    return resumo


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("md_path")
    parser.add_argument("out_dir")
    parser.add_argument("titulo", nargs="?", default="Peça FORJA")
    parser.add_argument("--case-dir")
    parser.add_argument("--ledger")
    parser.add_argument("--base-dir")
    # `_tipo_produto` decide por palavra-chave no título e nos 1.800 primeiros
    # caracteres. É bom palpite e erra: um relatório ao cliente que não diga
    # "relatório" nas primeiras linhas é classificado como peça, e então cobra
    # endereçamento e assinatura com OAB que ele não deve ter. Quem escreve sabe
    # o que escreveu; a declaração explícita prevalece e a heurística fica de
    # reserva. O gate NÃO é afrouxado: peça declarada continua sendo cobrada
    # como peça.
    parser.add_argument("--tipo", choices=("peca", "estudo"),
                        help="declara o tipo do produto em vez de deduzi-lo")
    args = parser.parse_args()
    r = build(args.md_path, args.out_dir, args.titulo, tipo=args.tipo,
              case_dir=args.case_dir, ledger_path=args.ledger,
              base_dir=args.base_dir)
    print(json.dumps(r, ensure_ascii=False, indent=2))
