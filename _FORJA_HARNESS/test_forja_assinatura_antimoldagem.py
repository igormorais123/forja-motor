# -*- coding: utf-8 -*-
"""test_forja_assinatura_antimoldagem.py — o gate F8-S ainda sabe reprovar?

A acusação do Diabob, e ela é séria: o gate de assinatura visual foi escrito
pelo mesmo agente que produz as peças, os limiares foram escolhidos por esse
agente, a cobertura foi medida com esse mesmo gate, e a peça declarada CONFORME
passou num gate que o autor calibrou. Pelo resultado, isso é indistinguível de
um instrumento moldado até aprovar o que o pipeline emite.

O que separa as duas coisas não é a intenção de quem escreveu: é a existência de
prova de que o gate reprova destruição real de qualidade. O censo prova o lado
fácil — 74 de 356 documentos do acervo passam, então o gate não aprova tudo.
Este teste prova o lado difícil, que é o que a acusação pede.

Método: pegar a peça APROVADA PELO DONO (Cafelana V8, entregue em 30/07/2026,
que hoje passa limpa) e destruí-la no OOXML, um elemento de cada vez, exigindo
que o gate acuse a família certa. Se ele aprovar a peça destruída, o limiar é
decorativo — e a suíte falha, mesmo com todo o resto verde.

Destruições, uma por vez:
  - `desfigurar`  : remove os EMF/WMF do pacote      -> VIS-03
  - `despaletar`  : troca os tokens da paleta        -> VIS-05
  - `destimbrar`  : apaga a arte do cabeçalho        -> VIS-05
  - `desdestacar` : afina a barra e mata as molduras -> VIS-04
  - `desnegritar` : remove todo o negrito do corpo   -> VIS-04
  - `desmesar`    : remove todas as tabelas          -> VIS-11 / VIS-02

O que este teste NÃO prova está escrito no fim do arquivo, e importa tanto
quanto o que ele prova.

Uso: python test_forja_assinatura_antimoldagem.py   (exit 0 = ok; 1 = regressão)
"""
from __future__ import annotations

import io
import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from forja_assinatura_visual import avaliar  # noqa: E402

RAIZ = Path(__file__).resolve().parent
FABRICA = RAIZ.parent

BASE = (FABRICA / "Cafelana" / "contrarrazões ao AgInt no AREsp nº 2.698.443D"
        / "_v8_visual_2026-07-30" / "IMPUGNACAO_AGINT_CAFELANA_V8_AJUSTADA_VISUAL.docx")

# Não se exige o código exato para não amarrar o teste à implementação: exige-se
# que o gate acuse algo da família certa.
DESTRUICOES = {
    "desfigurar": {"VIS-03"},
    "despaletar": {"VIS-05"},
    "destimbrar": {"VIS-05"},
    "desdestacar": {"VIS-04"},
    "desnegritar": {"VIS-04"},
    "desmesar": {"VIS-11", "VIS-02"},
}


def _e_corpo(nome: str) -> bool:
    return nome == "word/document.xml"


def _e_cabecalho(nome: str) -> bool:
    return bool(re.match(r"word/header\d*\.xml$", nome))


def _destruir(origem: Path, destino: Path, modo: str) -> int:
    """Reescreve o pacote com um elemento destruído. Devolve quantos alvos tocou."""
    tocados = 0
    with zipfile.ZipFile(origem) as entrada, \
            zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as saida:
        for item in entrada.infolist():
            dados = entrada.read(item.filename)

            if modo == "desfigurar" and item.filename.lower().endswith((".emf", ".wmf")):
                tocados += 1
                continue  # a figura simplesmente não vai para o pacote novo

            if modo in ("despaletar", "destimbrar", "desdestacar", "desnegritar", "desmesar"):
                alvo = _e_corpo(item.filename) or _e_cabecalho(item.filename)
                if alvo:
                    texto = dados.decode("utf-8", "replace")
                    antes = texto

                    if modo == "despaletar":
                        texto = texto.replace("395C60", "333333").replace("D9926A", "777777")
                    elif modo == "destimbrar" and _e_cabecalho(item.filename):
                        # descaracteriza os marcadores de desenho sem quebrar o XML
                        texto = re.sub(r"a:blip|r:embed|<v:shape|<v:group|<w:drawing|a:prstGeom",
                                       "zz:nada", texto)
                    elif modo == "desdestacar" and _e_corpo(item.filename):
                        texto = texto.replace('w:sz="24"', 'w:sz="4"')
                        texto = texto.replace("<w:framePr", "<w:zzframePr")
                    elif modo == "desnegritar" and _e_corpo(item.filename):
                        texto = re.sub(r"<w:b\s*/>|<w:b\s[^>]*/>", "", texto)
                    elif modo == "desmesar" and _e_corpo(item.filename):
                        texto = texto.replace("<w:tbl>", "<w:zztbl>").replace(
                            "</w:tbl>", "</w:zztbl>")

                    if texto != antes:
                        tocados += 1
                    dados = texto.encode("utf-8")

            saida.writestr(item, dados)
    return tocados


def main() -> int:
    falhas = 0

    if not BASE.is_file():
        print(f"  FALHOU: a peça aprovada sumiu do acervo — {BASE.name}")
        print("REGRESSÃO: sem peça aprovada não há como provar que o gate reprova destruição")
        return 1

    limpo = avaliar(BASE)
    if not limpo["conforme"]:
        codigos = sorted({a["codigo"] for a in limpo["achados"]})
        print(f"  FALHOU: a peça aprovada já reprova no gate ({codigos}) — a destruição não "
              "provaria nada, porque o gate já estava reclamando antes dela")
        falhas += 1

    with tempfile.TemporaryDirectory(prefix="forja-f8s-antimoldagem-") as tmp:
        for modo, esperados in DESTRUICOES.items():
            destino = Path(tmp) / f"destruido_{modo}.docx"
            tocados = _destruir(BASE, destino, modo)
            if not tocados:
                print(f"  FALHOU: a destruição '{modo}' não alcançou nenhum alvo no pacote — "
                      "o teste ficaria verde por não ter destruído nada")
                falhas += 1
                continue
            laudo = avaliar(destino)
            codigos = {a["codigo"] for a in laudo["achados"]}
            if not (codigos & esperados):
                print(f"  FALHOU: o gate APROVOU a peça destruída em '{modo}' "
                      f"({tocados} alvo(s) atingido(s)). Esperava algo de {sorted(esperados)}, "
                      f"obteve {sorted(codigos) or 'nada'} — o limiar é decorativo")
                falhas += 1

    if falhas:
        print(f"REGRESSÃO: {falhas} verificação(ões) anti-moldagem do F8-S falharam")
        return 1

    print(f"ok: a peça aprovada passa limpa e as {len(DESTRUICOES)} destruições deliberadas são "
          "acusadas — o F8-S não foi moldado até aprovar o que o pipeline emite")
    print("     (o que este teste NÃO prova: que o gate resista a um adversário que ADICIONE "
          "elementos vazios. Ver F8S_ANTICIRCULARIDADE_2026-08-04.md)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
