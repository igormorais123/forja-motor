# -*- coding: utf-8 -*-
"""forja_adocao_rota.py — a rota boa está sendo percorrida?

Existe uma família de defeito que nenhum gate da fábrica detecta, porque todos
eles perguntam sobre a peça e nenhum pergunta sobre o CAMINHO: a esteira constrói
a rota certa, instala gates nela, e a produção segue por fora. O gate fica verde
para sempre, porque nunca é chamado.

Já aconteceu três vezes:

  1. A edição visual parou em 10/07/2026 e ninguém notou por vinte dias.
  2. O elo 4-B de lastro era sério e rodou em 3 casos na história inteira
     (`CLAUDE.md`, 03/08: *gate instalado na rota que ninguém percorre é gate
     nenhum*).
  3. Em 05/08/2026, medindo o raio de explosão de tornar o F8-S bloqueante,
     descobri que `forja_visual_build.build()` — declarada nos canônicos como
     **entrada única de produção** — tinha rodado UMA vez na história, e que
     nenhum código de produção a chama: só testes e a régua. A prática real é o
     compositor manual por caso, que é justamente o "esforço manual por caso" que
     a lição 1 da saga visual diz não sobreviver ao volume.

As três vezes o defeito foi descoberto por acaso, roteirizando à mão. Este módulo
existe para que a quarta seja impossível de não ver.

O que ele mede, e só isso: das entregas recentes do acervo, quantas carregam a
marca de ter passado pela rota. Não julga qualidade — para isso há os outros 73
gates. Julga se eles tiveram a chance de rodar.

Marcas de passagem (basta uma):
    VISUAL_BUILD.json        a entrada única foi invocada
    FIDELIDADE_VISUAL.json   `forja_visual.compor()` gravou o lastro textual
    F8S_ASSINATURA_VISUAL.json  o gate de assinatura chegou a emitir laudo

Uso:
    python forja_adocao_rota.py               # últimas 20 entregas
    python forja_adocao_rota.py --ultimas 40
    python forja_adocao_rota.py --json saida.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

VERSAO = "FORJA-ADOCAO-ROTA-v1"
RAIZ = Path(__file__).resolve().parent
FABRICA = RAIZ.parent

MARCAS = ("VISUAL_BUILD.json", "FIDELIDADE_VISUAL.json", "F8S_ASSINATURA_VISUAL.json")

# Pastas que não são entrega: material de trabalho, testes e arquivos temporários.
IGNORAR = ("_FORJA_HARNESS", "_scripts_oneoff", "node_modules", ".git",
           "__pycache__", "_MODELOS", "_FERRAMENTAS")


def _sha_arquivo(caminho):
    h = hashlib.sha256()
    try:
        with caminho.open("rb") as fh:
            for bloco in iter(lambda: fh.read(1 << 20), b""):
                h.update(bloco)
    except OSError:
        return None
    return h.hexdigest()


def _entregas(limite):
    """As `limite` entregas mais recentes, contando OBRA e não arquivo.

    O defeito que isto corrige foi apontado pelo Diabob em 05/08/2026 e era
    material: a mesma peça existe em várias pastas — pasta do caso, pasta de
    entrega, pacote de revisão — e cada cópia entrava na amostra como se fosse
    uma entrega distinta. Numa amostra de 20, um único relatório ocupava quatro
    posições. O denominador virava contagem de arquivos e o leitor lia como
    contagem de trabalho feito.

    A desduplicação é por SHA-256 do conteúdo, e não por nome: nome igual pode
    ser versão diferente, e nome diferente pode ser a mesma obra copiada com
    outro rótulo. Byte a byte não admite discussão.

    A cópia mais recente representa a obra, mas **a marca de rota é procurada em
    todas as cópias** — uma peça que passou pela rota e depois foi copiada para
    a pasta de entrega sem os laudos ao lado continua tendo passado pela rota.
    Ignorar isso puniria a obra pela cópia, e mediria arrumação de pasta em vez
    de caminho percorrido.
    """
    achados = []
    for caminho in FABRICA.rglob("*.docx"):
        nome = caminho.name
        if nome.startswith("~$") or nome.startswith("_tmp"):
            continue
        if any(parte in caminho.parts for parte in IGNORAR):
            continue
        try:
            achados.append((caminho.stat().st_mtime, caminho))
        except OSError:
            continue
    achados.sort(reverse=True)

    obras, por_sha = [], {}
    for mtime, caminho in achados:
        sha = _sha_arquivo(caminho)
        if sha is None:
            continue
        if sha in por_sha:
            por_sha[sha]["copias"].append(caminho)
            continue
        obra = {"mtime": mtime, "docx": caminho, "sha256": sha, "copias": [caminho]}
        por_sha[sha] = obra
        obras.append(obra)

    janela = obras[:limite]
    # Cópias colapsadas DENTRO da janela examinada. Contar o acervo inteiro aqui
    # daria um número grande e irrelevante para o que se está medindo.
    colapsadas = sum(len(obra["copias"]) - 1 for obra in janela)
    return janela, colapsadas


def _caminho_alvo(valor, marcador):
    """Resolve os formatos absoluto e relativo usados pelos três laudos."""
    if not isinstance(valor, str) or not valor.strip():
        return []
    bruto = Path(valor)
    if bruto.is_absolute():
        candidatos = [bruto]
    else:
        # Os laudos mais novos são relativos à fábrica; os antigos podem ser
        # relativos à pasta do próprio laudo. Tentar ambos não cria vínculo por
        # pasta: a confirmação final ainda exige o mesmo arquivo.
        candidatos = [FABRICA / bruto, marcador.parent / bruto, RAIZ / bruto]
    resolvidos = []
    for candidato in candidatos:
        try:
            resolvido = candidato.resolve()
        except OSError:
            continue
        if resolvido not in resolvidos:
            resolvidos.append(resolvido)
    return resolvidos


def _alvo_do_marcador(dados):
    """Extrai caminho e hash sem assumir um único schema histórico."""
    docx = dados.get("docx") if isinstance(dados, dict) else None
    sha = dados.get("docxSha256") if isinstance(dados, dict) else None
    if isinstance(docx, dict):
        sha = docx.get("sha256") or sha
        docx = docx.get("path") or docx.get("arquivo")
    return docx, sha


def _marca_aplica(marcador, docx):
    """Só aceita a marca quando ela prova este DOCX, não um irmão da pasta."""
    try:
        dados = json.loads(marcador.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return False
    alvo, sha_esperado = _alvo_do_marcador(dados)
    if not alvo:
        return False
    docx_real = docx.resolve()
    candidatos = _caminho_alvo(alvo, marcador)
    if not any(candidato == docx_real for candidato in candidatos):
        return False
    if isinstance(sha_esperado, str) and sha_esperado.strip():
        try:
            sha_real = hashlib.sha256(docx.read_bytes()).hexdigest()
        except OSError:
            return False
        return sha_real.casefold() == sha_esperado.strip().casefold()
    return True


def _marcas_do_docx(caminho):
    """Retorna apenas marcas cujo registro aponta para `caminho` exatamente."""
    return [
        nome for nome in MARCAS
        if _marca_aplica(caminho.parent / nome, caminho)
    ]


def medir(limite=20):
    obras, colapsadas = _entregas(limite)
    linhas = []
    for obra in obras:
        # A marca vale se QUALQUER cópia da obra a carrega — ver o docstring de
        # `_entregas`. O vínculo por hash em `_marca_aplica` continua valendo em
        # cada cópia, então isto não afrouxa a prova: afrouxa só a exigência de
        # que o laudo esteja na mesma pasta da cópia que ficou mais recente.
        marcas, onde = [], None
        for copia in obra["copias"]:
            achadas = _marcas_do_docx(copia)
            if achadas:
                marcas, onde = achadas, copia
                break
        principal = obra["docx"]
        linhas.append({
            "docx": principal.name,
            "pasta": str(principal.parent.relative_to(FABRICA)),
            "modificadoEm": time.strftime("%Y-%m-%d", time.localtime(obra["mtime"])),
            "sha256": obra["sha256"][:16],
            "copias": len(obra["copias"]),
            "marcas": marcas,
            "marcaEncontradaEm": str(onde.parent.relative_to(FABRICA)) if onde else None,
            "passouPelaRota": bool(marcas),
        })
    passaram = sum(1 for l in linhas if l["passouPelaRota"])
    total = len(linhas)
    return {
        "versao": VERSAO,
        "entregasExaminadas": total,
        "copiasColapsadas": colapsadas,
        "passaramPelaRota": passaram,
        "adocao": round(passaram / total, 4) if total else None,
        "linhas": linhas,
    }


def main():  # pragma: no cover
    ap = argparse.ArgumentParser(description="Mede se a rota canônica é percorrida.")
    ap.add_argument("--ultimas", type=int, default=20)
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    laudo = medir(args.ultimas)
    if args.json:
        Path(args.json).write_text(json.dumps(laudo, ensure_ascii=False, indent=2),
                                   encoding="utf-8")

    print("=" * 78)
    print("ADOÇÃO DA ROTA CANÔNICA DE PRODUÇÃO VISUAL")
    print("=" * 78)
    for linha in laudo["linhas"]:
        marca = "ROTA " if linha["passouPelaRota"] else "  -  "
        copias = f" ({linha['copias']}x)" if linha["copias"] > 1 else ""
        print(f"  {marca} {linha['modificadoEm']}  {linha['docx'][:52]}{copias}")
    total, passaram = laudo["entregasExaminadas"], laudo["passaramPelaRota"]
    print("-" * 78)
    if laudo["copiasColapsadas"]:
        print(f"  {laudo['copiasColapsadas']} cópia(s) do mesmo conteúdo colapsadas "
              "— a unidade medida é a obra, não o arquivo")
    if not total:
        print("  nenhuma entrega encontrada")
        return 0
    print(f"  {passaram} de {total} entregas recentes passaram pela rota "
          f"({laudo['adocao']:.0%})")
    if laudo["adocao"] < 0.5:
        print("\n  A maioria da produção não percorre a rota que tem os gates.")
        print("  Apertar os gates não alcança essas peças. A pergunta útil é por que")
        print("  o caminho bom não é o caminho fácil — não qual limiar subir.")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
