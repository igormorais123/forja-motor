# -*- coding: utf-8 -*-
"""forja_artefatos.py — vocabulário canônico dos artefatos da esteira.

O mesmo artefato existe no acervo em vários formatos, porque cada fase inventou
o seu vocabulário. Medido em 04/08/2026:

    injection_scan          7 esquemas
    source_ledger           6 esquemas
    document_index          6 esquemas
    context_validation      6 esquemas
    paragraph_provenance    5 esquemas
    coverage_ledger         5 esquemas
    f7_gate_result          9 esquemas

A consequência prática apareceu ao construir os gates computados: cada um
precisou do seu próprio mapa de sinônimos, e hoje há QUATORZE desses mapas
espalhados por cinco módulos. Quando um caso novo inventa mais um nome, todo
gate passa a ler errado — em silêncio, devolvendo `pass` sobre o que não
entendeu. É a `MC-15` vista do lado do produtor.

Este módulo é a fonte única desse vocabulário. Ele NÃO migra artefato antigo:
normaliza na leitura, que é o único caminho que não reescreve história nem
quebra caso já entregue.

A parte que faltava em tudo isso é o `censo`: ele varre o acervo e aponta os
campos que NENHUM mapa conhece. Um vocabulário mantido de memória envelhece
sem avisar; mantido contra o acervo, ele reclama sozinho.
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

VERSAO = "FORJA-ARTEFATOS-v1"
RAIZ = Path(__file__).resolve().parent

# Conceito -> nomes já vistos no acervo. Consolidado dos mapas que estavam
# espalhados em forja_paragrafos, forja_fontes_oficiais, forja_ingestao,
# forja_contexto e forja_injection_scan.
DIALETOS: dict[str, dict[str, tuple]] = {
    "paragraph_provenance": {
        "unidades": ("paragraphs", "blocks", "paragrafos", "unidades"),
        "lastro": ("provenance", "sources", "propositions", "supports", "supportIds",
                   "factIds", "propositionIds", "sourceIds", "evidence", "basis",
                   "lastro", "fontes"),
        "isencao_editorial": ("editorialOnly", "editorial", "claimClass", "kind", "tipo", "classe"),
        "amostra_do_texto": ("textPrefix", "sample", "trecho", "excerpt"),
        "hash_do_texto": ("markdownSha256", "draftSha256", "documentSha256"),
        "template": ("template", "templateUsed", "modelo", "baseTemplate"),
        "entidades_estrangeiras": ("foreignEntityCheck", "unexplainedForeignEntities",
                                   "entidadesEstrangeiras"),
    },
    "source_ledger": {
        "fontes": ("sources", "entries", "fontes", "officialSources"),
        "caminho_arquivado": ("archivedPath", "archived", "archive", "caminhoArquivado",
                              "localCopy"),
        "hash_arquivado": ("archivedSha256", "sha256", "hash", "contentSha256"),
        "url_oficial": ("officialUrl", "officialSource", "url", "fonteOficial", "link"),
        "autoridade": ("authority", "autoridade", "orgao", "órgão", "court"),
    },
    "citation_checklist": {
        "itens": ("items", "citations", "entries", "itens"),
        "usou_transcricao": ("quoteUsed", "citacaoTextual", "verbatim", "hasQuote",
                             "quote", "citacao", "excerpt", "trecho"),
        "registro_de_cotejo": ("comparedTo", "quoteComparedTo", "cotejo", "sourceExcerptSha256",
                               "excerptHash", "locator", "pincite", "quoteCompared",
                               "compared", "cotejado"),
    },
    "document_index": {
        "documentos": ("documents", "documentos"),
        "criticos_no_topo": ("criticalActs", "keyDocuments", "criticalDocumentsIndexed",
                             "atosCriticos", "documentosCriticos"),
        "totais": ("totals", "aggregateValidation"),
        "hash": ("sha256", "hash"),
        "caminho": ("path", "file", "name"),
    },
    "coverage_ledger": {
        "declaracao": ("declaredCoverage", "coverageStatus", "coverage", "coverageDeclared",
                       "cobertura", "items"),
        "lacunas": ("blockedMaterial", "openGaps", "knownGap", "pendingVerification",
                    "unansweredOrBlocked", "lacunas", "gaps"),
    },
    "injection_scan": {
        "escopo_varrido": ("total_pdfs", "pdfCount", "documentsScanned", "pdfs",
                           "arquivos_analisados", "files", "scanScope"),
        "triagem": ("triagem", "triage", "humanTriage", "review", "injectionTriaged",
                    "existingSpecificEvidence", "approved", "status"),
        "achado_p0": ("resumo_p0", "summaryP0", "p0Findings", "p0", "severidade",
                      "promptInjectionDetected"),
    },
    "context_validation": {
        "pendencias": ("pendingMaterialQuestions", "blockedQuestions", "openMaterialQuestions",
                       "questoesPendentes"),
        "hash_do_texto": ("auditedMarkdownSha256", "auditedSha256", "finalMarkdownSha256",
                          "markdown", "sourceHashes"),
        "identidade": ("processIdentity", "proceduralIdentity", "actIdentity", "tribunal",
                       "identidadeProcessual"),
        "liberacao_externa": ("approvedForExternalRelease", "approvedForClientOrFiling"),
        "recheque_de_fatos": ("factsRechecked", "facts_rechecked"),
    },
    "adversarial_recheck": {
        "itens_rechecados": ("recheckedIssues", "findingsRechecked", "citationsRechecked",
                             "externalAllegations", "alegacoesRechecadas"),
        "aplicabilidade": ("applicable",),
        "motivo": ("notApplicableReason", "reason"),
    },
}

# Campos que aparecem em todo artefato e não carregam conceito de negócio. Ficam
# declarados para que o censo não os aponte como deriva a cada execução.
_ESTRUTURAIS = {
    "schemaVersion", "kind", "caseId", "phase", "generatedAt", "revisedAt", "revisionReason",
    "documentId", "document", "documentVersion", "version", "producer", "reviewer", "status",
    "approved", "releasePolicy", "audience", "notes", "supersedes", "evaluatedAt",
    "evaluatedArtifact", "markdownPath", "root", "sourceManifest", "sourceMessageId",
    "receivedAt", "accessedAt", "scope", "method", "generatedBy", "protocolVersion",
}


def ler(caminho) -> dict:
    """Lê um artefato JSON e desembrulha o invólucro `main`, quando houver."""
    alvo = Path(caminho)
    if not alvo.is_file():
        return {}
    try:
        dados = json.loads(alvo.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return {}
    if isinstance(dados, dict) and isinstance(dados.get("main"), dict):
        return dados["main"]
    return dados if isinstance(dados, dict) else {}


def nomes(especie: str, conceito: str) -> tuple:
    """Nomes conhecidos para um conceito. Erra alto se o conceito não existe."""
    mapa = DIALETOS.get(especie)
    if mapa is None:
        raise KeyError(f"espécie de artefato desconhecida: {especie}")
    if conceito not in mapa:
        raise KeyError(f"conceito desconhecido em {especie}: {conceito}")
    return mapa[conceito]


def campo(dados: dict, especie: str, conceito: str, padrao=None):
    """Primeiro valor não vazio entre os nomes conhecidos do conceito."""
    if not isinstance(dados, dict):
        return padrao
    for nome in nomes(especie, conceito):
        valor = dados.get(nome)
        if isinstance(valor, str) and valor.strip():
            return valor
        if isinstance(valor, (list, dict)) and len(valor) > 0:
            return valor
        if isinstance(valor, bool) or isinstance(valor, (int, float)):
            return valor
    return padrao


def lista(dados: dict, especie: str, conceito: str) -> list:
    """Lista de dicionários sob o conceito, em qualquer dialeto."""
    valor = campo(dados, especie, conceito)
    if isinstance(valor, list):
        return [item for item in valor if isinstance(item, dict)]
    if isinstance(valor, dict):
        return [item for item in valor.values() if isinstance(item, dict)]
    return []


def censo(raiz=None) -> dict:
    """Varre o acervo e aponta os campos que nenhum dialeto conhece.

    É a peça que faltava. Um mapa de sinônimos mantido de memória envelhece em
    silêncio: o caso novo inventa `fontesConferidas`, o gate não encontra nada,
    devolve `pass` e ninguém sabe. Aqui a divergência é relatada.
    """
    base = Path(raiz) if raiz else (RAIZ / "state")
    conhecidos = {especie: set().union(*mapa.values()) | _ESTRUTURAIS
                  for especie, mapa in DIALETOS.items()}
    esquemas: dict = defaultdict(set)
    desconhecidos: dict = defaultdict(lambda: defaultdict(int))
    examinados = 0

    for especie in DIALETOS:
        for arquivo in base.rglob(f"{especie}.json"):
            dados = ler(arquivo)
            if not dados:
                continue
            examinados += 1
            esquemas[especie].add(tuple(sorted(dados)))
            for chave in dados:
                if chave not in conhecidos[especie]:
                    desconhecidos[especie][chave] += 1

    return {
        "versao": VERSAO,
        "artefatosExaminados": examinados,
        "esquemasPorEspecie": {e: len(v) for e, v in sorted(esquemas.items())},
        "camposDesconhecidos": {e: dict(sorted(v.items(), key=lambda x: -x[1]))
                                for e, v in sorted(desconhecidos.items()) if v},
    }


def _relatar(laudo: dict) -> None:
    print("=" * 74)
    print("CENSO DE VOCABULÁRIO DOS ARTEFATOS DA FORJA")
    print("=" * 74)
    print(f"  artefatos examinados : {laudo['artefatosExaminados']}")
    print("\n  ESQUEMAS DISTINTOS POR ESPÉCIE")
    for especie, quantos in laudo["esquemasPorEspecie"].items():
        print(f"    {especie:26} {quantos}")
    desconhecidos = laudo["camposDesconhecidos"]
    print(f"\n  CAMPOS QUE NENHUM DIALETO CONHECE ({sum(len(v) for v in desconhecidos.values())})")
    if not desconhecidos:
        print("    nenhum — o vocabulário canônico cobre o acervo")
    for especie, campos in desconhecidos.items():
        print(f"    {especie}:")
        for nome, quantos in list(campos.items())[:12]:
            print(f"        {nome:40} em {quantos} artefato(s)")


if __name__ == "__main__":  # pragma: no cover
    import argparse

    ap = argparse.ArgumentParser(description="Vocabulário canônico e censo de dialetos.")
    ap.add_argument("--json", metavar="ARQUIVO", help="grava o censo em JSON")
    args = ap.parse_args()

    laudo = censo()
    _relatar(laudo)
    if args.json:
        Path(args.json).write_text(json.dumps(laudo, ensure_ascii=False, indent=2),
                                   encoding="utf-8")
        print(f"\ncenso: {args.json}")
