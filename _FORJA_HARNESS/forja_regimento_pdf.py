"""Converte o PDF oficial de um regimento interno no arquivo-padrão da fábrica.

O protocolo exige `REGIMENTO_INTERNO_<TRIBUNAL>.md` com **texto integral** (nunca
resumo), cabeçalho de metadados e seção final de emendas posteriores. Até
09/08/2026 esses arquivos eram montados caso a caso, e o resultado foi previsível:
20 regimentos na fábrica e nenhum do STF — o tribunal mais alto, justamente.

Este conversor é determinístico de propósito. Pedir a um agente que transcreva
centenas de páginas é a mesma armadilha já medida na composição visual: cinco de
cinco resumiram. Aqui o texto vem do extrator, e o agente só preenche o que é
juízo — versão, data de conferência e as emendas posteriores.

A seção de emendas nasce **declaradamente vazia**, com a pergunta em aberto. Um
regimento convertido não é um regimento vigente: entre a consolidação impressa e
a data do protocolo pode haver anos de emenda, e é o pesquisador que fecha essa
distância.

    python forja_regimento_pdf.py --pdf cache/regimentos/RISTF.pdf \
        --tribunal STF --nome "Supremo Tribunal Federal" \
        --url-oficial https://... --versao "Atualizado até a ER n. 58/2022" \
        --saida "<pasta do caso>/REGIMENTO_INTERNO_STF.md"
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from datetime import date
from pathlib import Path

# Marca de página do tipo "—  30 —" ou "- 30 -", isolada na linha.
PAGINA_RE = re.compile(r"^\s*[—–-]{1,2}\s*\d{1,4}\s*[—–-]{1,2}\s*$")
# Hifenização de fim de linha: "compe-\ntência" volta a ser uma palavra só.
HIFEN_QUEBRA_RE = re.compile(r"(\w)-\n(\w)")
ESPACOS_RE = re.compile(r"[ \t]{2,}")

AVISO = ("> **Aviso**: documento de apoio para elaboração de petições. A versão "
         "que vale é a oficial vigente no portal do tribunal, na data do "
         "protocolo.")


BLOCO_RE = re.compile(r"(?i)</(p|div|h[1-6]|li|tr|br|section)\s*>|<br\s*/?>")
TAG_RE = re.compile(r"<[^>]+>")


def _extrair_pdf(pdf: Path) -> list[str]:
    try:
        import pypdf
    except ImportError:  # pragma: no cover - ambiente sem a dependência
        raise SystemExit("pypdf não instalado: pip install pypdf")
    return [(p.extract_text() or "") for p in pypdf.PdfReader(str(pdf)).pages]


def _extrair_epub(epub: Path) -> list[str]:
    """Texto do epub na ordem do spine.

    O STF publica o mesmo regimento em PDF e em epub, e nem sempre na mesma
    versão: em 09/08/2026 o PDF era a edição 2023 (até a ER 58/2022) e o epub, a
    de 2024 (até a ER 59/2023). Ler os dois e ficar com o mais novo é mais
    barato que descobrir a diferença dentro de uma peça.
    """
    import html as _html
    import zipfile
    from xml.etree import ElementTree

    with zipfile.ZipFile(epub) as z:
        nomes = z.namelist()
        opf = next((n for n in nomes if n.lower().endswith(".opf")), None)
        ordem: list[str] = []
        if opf:
            raiz = ElementTree.fromstring(z.read(opf))
            ns = {"o": "http://www.idpf.org/2007/opf"}
            itens = {i.get("id"): i.get("href")
                     for i in raiz.iterfind(".//o:manifest/o:item", ns)}
            base = opf.rsplit("/", 1)[0] + "/" if "/" in opf else ""
            for ref in raiz.iterfind(".//o:spine/o:itemref", ns):
                href = itens.get(ref.get("idref"))
                if href:
                    ordem.append(base + href)
        if not ordem:
            ordem = [n for n in nomes if n.lower().endswith((".xhtml", ".html", ".htm"))]
        partes = []
        for nome in ordem:
            if nome not in nomes:
                continue
            bruto = z.read(nome).decode("utf-8", "replace")
            bruto = BLOCO_RE.sub("\n", bruto)
            partes.append(_html.unescape(TAG_RE.sub("", bruto)))
    return partes


def extrair(origem: Path) -> tuple[list[str], dict]:
    if origem.suffix.lower() == ".epub":
        blocos, rotulo = _extrair_epub(origem), "documentos do epub"
    else:
        blocos, rotulo = _extrair_pdf(origem), "páginas do PDF"
    diag = {
        "paginas": len(blocos),
        "rotulo": rotulo,
        "caracteres": sum(len(t) for t in blocos),
        "paginasQuaseVazias": sum(1 for t in blocos if len(t.strip()) < 20),
        "sha256Pdf": hashlib.sha256(origem.read_bytes()).hexdigest(),
    }
    return blocos, diag


def limpar(paginas: list[str]) -> str:
    linhas: list[str] = []
    for texto in paginas:
        for linha in texto.splitlines():
            if PAGINA_RE.match(linha):
                continue
            linhas.append(ESPACOS_RE.sub(" ", linha.rstrip()))
        linhas.append("")
    corpo = "\n".join(linhas)
    corpo = HIFEN_QUEBRA_RE.sub(r"\1\2", corpo)
    return re.sub(r"\n{3,}", "\n\n", corpo).strip()


def montar(corpo: str, *, tribunal: str, nome: str, url: str, versao: str,
           origem_pdf: str, diag: dict, hoje: str) -> str:
    cab = [
        f"# REGIMENTO INTERNO DO {nome.upper()}",
        "",
        "## Informações do Documento",
        "",
        f"- **Tribunal**: {nome} ({tribunal})",
        f"- **URL Oficial**: {url}",
        f"- **Versão**: {versao}",
        f"- **Data de Download**: {hoje}",
        f"- **Fonte**: {origem_pdf}",
        f"- **SHA-256 do arquivo baixado**: `{diag['sha256Pdf']}`",
        f"- **Extração**: {diag['paginas']} {diag['rotulo']}, {diag['caracteres']:,} caracteres, "
        f"{diag['paginasQuaseVazias']} sem texto extraível"
        .replace(",", "."),
        f"- **Conversão**: `forja_regimento_pdf.py` (determinística; sem resumo, sem reescrita)",
        "",
        AVISO,
        "",
        "---",
        "",
        "## CONTEÚDO INTEGRAL",
        "",
    ]
    rodape = [
        "",
        "---",
        "",
        "## Emendas posteriores",
        "",
        f"**Estado em {hoje}: NÃO PESQUISADO.**",
        "",
        f"A consolidação acima para em: _{versao}_. Entre essa data e o dia do "
        "protocolo pode haver emenda regimental que mude competência do órgão "
        "julgador, processamento de recurso, prazo, pauta ou sustentação oral.",
        "",
        "Antes de usar este arquivo em qualquer peça, pesquisar na fonte oficial "
        "o que saiu depois e registrar aqui, uma linha por emenda, com número, "
        "data, objeto e link. Enquanto esta seção disser NÃO PESQUISADO, o "
        "arquivo serve para consulta interna e **não** sustenta afirmação sobre "
        "o regimento vigente.",
        "",
    ]
    return "\n".join(cab) + corpo + "\n" + "\n".join(rodape)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--pdf", required=True, type=Path,
                    help="PDF ou EPUB oficial")
    ap.add_argument("--tribunal", required=True, help="sigla, ex.: STF")
    ap.add_argument("--nome", required=True, help="nome por extenso")
    ap.add_argument("--url-oficial", required=True)
    ap.add_argument("--versao", required=True,
                    help="até onde a consolidação impressa vai, verbatim do PDF")
    ap.add_argument("--origem", default=None, help="URL de onde o PDF foi baixado")
    ap.add_argument("--saida", required=True, type=Path)
    args = ap.parse_args(argv)

    if not args.pdf.is_file():
        print(f"arquivo não encontrado: {args.pdf}", file=sys.stderr)
        return 2
    paginas, diag = extrair(args.pdf)
    if diag["caracteres"] < 50_000:
        print(f"extração pobre ({diag['caracteres']} chars): o PDF provavelmente é "
              "imagem e precisa de OCR — não gravei nada", file=sys.stderr)
        return 3
    corpo = limpar(paginas)
    texto = montar(corpo, tribunal=args.tribunal, nome=args.nome,
                   url=args.url_oficial, versao=args.versao,
                   origem_pdf=args.origem or args.url_oficial, diag=diag,
                   hoje=date.today().isoformat())
    args.saida.parent.mkdir(parents=True, exist_ok=True)
    args.saida.write_text(texto, encoding="utf-8")
    print(f"gravado: {args.saida} ({len(texto):,} chars)".replace(",", "."))
    print(f"páginas {diag['paginas']} | sem texto {diag['paginasQuaseVazias']} | "
          f"sha256 {diag['sha256Pdf'][:16]}")
    print("PENDENTE: seção 'Emendas posteriores' está NÃO PESQUISADO.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
