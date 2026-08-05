# -*- coding: utf-8 -*-
"""forja_canario_mutacao.py — o gate sabe dizer não?

O censo de 04/08/2026 mediu que 41 nomes de gate produzem veredito sobre material real
(39 gates de contrato e dois diagnósticos auxiliares),
e que QUATORZE deles só souberam dizer `pass` no acervo inteiro. Isso não é
defeito por si: pode significar que a esteira anda limpa naquele ponto. Mas
também é exatamente o que um gate tautológico produziria, e as duas hipóteses
são indistinguíveis pela observação passiva.

A regressão unitária não resolve a dúvida. Ela prova que a função reprova o
caso que o autor do gate imaginou — e o autor do gate é quem tinha interesse em
que ela passasse. O que falta é prova ATIVA: pegar o artefato real que o gate
aprovou, destruí-lo de um jeito que qualquer leitor humano chamaria de defeito,
e exigir que o veredito mude.

Três mutações, da mais brutal à mais sutil:

  M1 `zerar`   — o artefato vira `{}`. Um gate que continua aprovando aqui não
                 está lendo nada: é a MC-15 vista do lado de dentro.
  M2 `esvaziar`— toda lista vira `[]` e todo dicionário de itens vira `{}`. O
                 artefato mantém a forma e perde o conteúdo. Pega o gate que
                 confere a presença do campo e nunca o que há dentro dele.
  M3 `desprover` — apaga os campos que carregam prova (hash, fonte, id de
                 documento, citação, lastro). O artefato continua íntegro e
                 deixa de ser verificável. É a mutação que mais se parece com o
                 defeito real da esteira.

Sobrevivência à mutação = o gate disse `pass` sobre o artefato destruído. Cada
sobrevivente é um gate que ninguém deveria contar como proteção.

Uma ressalva honesta, e ela vale para todo o instrumento: `not_applicable` NÃO
é sobrevivência. Zerar um artefato é uma forma legítima de fazê-lo desaparecer,
e um gate que responde "não há o que examinar" está certo, não complacente. Só
`pass` sobre ruína conta como falha.

Uso:
    python forja_canario_mutacao.py                 # relatório completo
    python forja_canario_mutacao.py --json saida.json
"""
from __future__ import annotations

import json
import shutil
import tempfile
from collections import defaultdict
from pathlib import Path

VERSAO = "FORJA-CANARIO-MUTACAO-v1"
RAIZ = Path(__file__).resolve().parent

# Campos que carregam PROVA. Apagá-los não muda a forma do artefato e destrói a
# sua verificabilidade — é a mutação que imita o defeito real da esteira.
_CAMPOS_DE_PROVA = {
    "sha256", "hash", "digest", "checksum", "markdownSha256", "auditSha256",
    "sourceId", "sourceIds", "sources", "source", "fonte", "fontes",
    "evidence", "evidencia", "evidencias", "lastro", "supports", "supportIds",
    "provenance", "proveniencia", "citation", "citations", "citacoes",
    "factIds", "factId", "propositionIds", "anchor", "anchors", "ancora",
    "excerpt", "excerpts", "textPrefix", "verbatim", "quote", "quotes",
    "path", "file", "archivedAt", "capturedAt", "url",
}

#  M4 `emudecer` — todo valor de texto vira "". A estrutura fica intacta e as
#                 declarações somem. Existe porque `esvaziar` só zera LISTAS, e
#                 um gate que lê campo escalar — `tribunal.name`,
#                 `tribunal.basis` — atravessava as três primeiras mutações sem
#                 ser tocado e era contado como sobrevivente. Terceiro defeito
#                 deste instrumento no mesmo dia, e os três da mesma natureza:
#                 medir o que o gate não lê é medir a si mesmo.
MUTACOES = ("zerar", "esvaziar", "desprover", "emudecer")

# Marcas de prova em texto corrido. O parecer da Helena, o do Cícero, o relatório
# de red team e o registro de decisões do conselho são MARKDOWN — a primeira
# versão deste canário só mutava JSON e por isso deu cinco falsos sobreviventes,
# gates cujo insumo a mutação nunca tocou. Instrumento que não alcança a entrada
# do gate mede a si mesmo.
_MARCAS_DE_PROVA_EM_TEXTO = (
    "fl.", "fls.", "e-stj", "evento", "doc.", "sha256", "http", "art.",
    "súmula", "sumula", "resp", "acatad", "rejeitad", "recomenda",
)


def _muta_texto(texto: str, modo: str) -> str:
    if modo == "zerar":
        return ""
    linhas = texto.splitlines()
    if modo in ("esvaziar", "emudecer"):
        # Mantém só a estrutura: títulos sem uma linha de conteúdo sob eles.
        return "\n".join(l for l in linhas if l.lstrip().startswith("#"))
    return "\n".join(l for l in linhas
                     if not any(m in l.lower() for m in _MARCAS_DE_PROVA_EM_TEXTO))


def _muta(dados, modo: str):
    """Aplica a mutação recursivamente, preservando a forma quando o modo exige."""
    if modo == "zerar":
        return {} if isinstance(dados, dict) else ([] if isinstance(dados, list) else dados)

    if isinstance(dados, dict):
        saida = {}
        for chave, valor in dados.items():
            if modo == "desprover" and chave in _CAMPOS_DE_PROVA:
                continue
            if modo == "esvaziar" and isinstance(valor, list):
                saida[chave] = []
                continue
            if modo == "emudecer" and isinstance(valor, str):
                saida[chave] = ""
                continue
            saida[chave] = _muta(valor, modo)
        return saida

    if isinstance(dados, list):
        if modo == "esvaziar":
            return []
        return [_muta(item, modo) for item in dados]

    return dados


def _vereditos(pasta: Path, resultado: dict) -> dict:
    """Roda todos os produtores sobre uma pasta e devolve gate -> veredito."""
    from forja_recomputo_censo import _produtores

    saida = {}
    for laudo in _produtores(pasta, resultado):
        saida.update(laudo.get("gates") or {})
    return saida


def _tentativas(base: Path) -> list:
    vistas = []
    for resultado in base.rglob("PHASE_RESULT.json"):
        vistas.append(resultado.parent)
    return vistas


def _muta_arquivo(arquivo: Path, modo: str) -> None:
    """Destrói um arquivo no lugar, pela forma que ele tiver."""
    if arquivo.suffix.lower() == ".json":
        try:
            original = json.loads(arquivo.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            return
        arquivo.write_text(json.dumps(_muta(original, modo), ensure_ascii=False, indent=2),
                           encoding="utf-8")
        return
    try:
        texto = arquivo.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return
    arquivo.write_text(_muta_texto(texto, modo), encoding="utf-8")


def _internaliza_externos(pasta: Path, espelho: Path, resultado: dict, modo: str) -> dict:
    """Traz para dentro do espelho os artefatos que moram fora da tentativa.

    O canário copiava só a pasta da tentativa e destruía o que estava lá dentro.
    Mas boa parte dos artefatos é declarada no PHASE_RESULT por caminho ABSOLUTO,
    apontando para o material promovido do caso — e esses o canário lia intactos.

    Consequência medida em 04/08/2026: `email_claims_true` e
    `email_human_style_passed` apareceram como sobreviventes da destruição. Eram
    falsos positivos do instrumento, não complacência dos gates: o manifesto e o
    e-mail da única F9 real do acervo estão em `n3_artifacts`, fora da tentativa,
    e a mutação nunca os tocou. Um canário que não alcança o que o gate lê mede a
    própria cobertura e chama isso de veredito — exatamente o defeito que ele foi
    construído para achar nos outros.
    """
    itens = resultado.get("artifacts") or []
    if not isinstance(itens, list):
        return resultado

    externos = espelho / "_externos"
    copia = json.loads(json.dumps(resultado, ensure_ascii=False))
    for indice, item in enumerate(copia.get("artifacts") or []):
        if not isinstance(item, dict):
            continue
        valor = item.get("path") or item.get("source")
        if not valor:
            continue
        origem = Path(str(valor))
        if not origem.is_absolute():
            origem = pasta / origem
        try:
            dentro = origem.resolve().is_relative_to(pasta.resolve())
        except (OSError, ValueError):
            continue
        if dentro or not origem.is_file():
            continue
        externos.mkdir(parents=True, exist_ok=True)
        # Prefixo pelo índice: dois artefatos de fases diferentes podem ter o
        # mesmo nome de arquivo, e sobrescrever um com o outro trocaria o material
        # examinado sem aviso.
        destino = externos / f"{indice:02d}_{origem.name}"
        try:
            shutil.copy2(origem, destino)
        except OSError:
            continue
        _muta_arquivo(destino, modo)
        chave = "path" if item.get("path") else "source"
        item[chave] = str(destino)
    return copia


def canario(raiz=None, mutacoes=MUTACOES, limite_por_gate: int = 3) -> dict:
    """Para cada gate aprovado em caso real, exige que a mutação mude o veredito."""
    base = Path(raiz) if raiz else (RAIZ / "state")

    from forja_recomputo_censo import _ler

    sobreviventes: dict = defaultdict(lambda: defaultdict(list))
    mortos: dict = defaultdict(set)
    examinados: dict = defaultdict(int)
    estritos_na_base: dict = defaultdict(set)
    erros = []

    for pasta in _tentativas(base):
        resultado = _ler(pasta / "PHASE_RESULT.json")
        try:
            base_vereditos = _vereditos(pasta, resultado)
        except Exception as erro:  # noqa: BLE001
            erros.append(f"{pasta.name}: base: {type(erro).__name__}: {erro}")
            continue

        aprovados = {g for g, v in base_vereditos.items() if v == "pass"}
        # Gate que reprova o artefato REAL, sem mutação nenhuma, não pode ser
        # mutado — não há `pass` para derrubar. Ele sai de `examinados`, e a
        # catraca de piso lia essa saída como "um gate ficou cego".
        #
        # As duas causas são opostas e precisavam ser separadas. Em 05/08/2026 o
        # `exploration_100_complete` saiu do censo justamente porque passou a
        # ENXERGAR: as checagens de diversidade acusaram que as 14 árvores reais
        # são formulário, e o veredito-base virou `warn`. A catraca acusou
        # cegueira onde havia rigor novo. Sem esta distinção, todo gate que
        # passasse a reprovar dado real derrubaria o canário, e a saída fácil
        # seria baixar o piso — que é exatamente como uma campanha de melhoria
        # se autoaprova destruindo a proteção que deveria reforçar.
        for gate, veredito in base_vereditos.items():
            if veredito in ("fail", "warn"):
                estritos_na_base[gate].add(pasta.name)
        # Só interessa mutar onde ainda falta prova de reprovação, e só umas
        # poucas vezes por gate: o instrumento é caro e a evidência satura.
        alvos = {g for g in aprovados
                 if examinados[g] < limite_por_gate and g not in mortos}
        if not alvos:
            continue
        for gate in alvos:
            examinados[gate] += 1

        for modo in mutacoes:
            with tempfile.TemporaryDirectory(prefix="forja-canario-") as tmp:
                espelho = Path(tmp) / pasta.name
                try:
                    shutil.copytree(pasta, espelho)
                except OSError as erro:
                    erros.append(f"{pasta.name}: copia: {erro}")
                    break

                for arquivo in espelho.glob("*.json"):
                    if arquivo.name in ("PHASE_RESULT.json", "RUN_CONTEXT.json"):
                        continue
                    try:
                        original = json.loads(arquivo.read_text(encoding="utf-8"))
                    except (ValueError, OSError):
                        continue
                    arquivo.write_text(
                        json.dumps(_muta(original, modo), ensure_ascii=False, indent=2),
                        encoding="utf-8")

                for arquivo in espelho.glob("*.md"):
                    try:
                        texto = arquivo.read_text(encoding="utf-8", errors="replace")
                    except OSError:
                        continue
                    arquivo.write_text(_muta_texto(texto, modo), encoding="utf-8")

                resultado_espelhado = _internaliza_externos(pasta, espelho, resultado, modo)

                try:
                    mutados = _vereditos(espelho, resultado_espelhado)
                except Exception as erro:  # noqa: BLE001
                    erros.append(f"{pasta.name}[{modo}]: {type(erro).__name__}: {erro}")
                    continue

                for gate in alvos:
                    # Ausente ou `not_applicable` = o gate percebeu que não há o
                    # que examinar. Isso é acerto, não complacência.
                    depois = mutados.get(gate)
                    if depois == "pass":
                        sobreviventes[gate][modo].append(pasta.name)
                    elif depois in ("fail", "warn"):
                        mortos[gate].add(modo)

    todos = sorted(set(examinados))
    # Sobreviver é ter dito `pass` sobre a ruína, e nunca ter reprovado. Gate que
    # apenas sumiu do laudo — ou respondeu `not_applicable` — percebeu que não
    # havia o que examinar, e a primeira versão deste canário o acusava junto com
    # os complacentes. Ausência de veredito não é veredito complacente.
    sobreviveram = sorted(g for g in todos if g not in mortos and sobreviventes.get(g))
    sem_veredito = sorted(g for g in todos if g not in mortos and not sobreviventes.get(g))
    return {
        "versao": VERSAO,
        "gatesExaminados": len(todos),
        # Gates que reprovam o artefato real sem mutação. Contam como
        # cobertura viva: não são cegueira, são rigor que já mordeu.
        "gatesEstritosNaBase": sorted(estritos_na_base),
        "coberturaViva": len(set(todos) | set(estritos_na_base)),
        "gatesQueReprovaramAlgumaMutacao": sorted(mortos),
        "gatesQueSobreviveramATodas": sobreviveram,
        "gatesSemVereditoAposMutacao": sem_veredito,
        "sobreviventes": {g: {m: sorted(set(p))[:4] for m, p in v.items()}
                          for g, v in sorted(sobreviventes.items())},
        "erros": erros,
    }


def _relatar(laudo: dict) -> None:
    print("=" * 74)
    print("CANÁRIO DE MUTAÇÃO — o gate percebe que o artefato foi destruído?")
    print("=" * 74)
    print(f"  gates examinados                : {laudo['gatesExaminados']}")
    print(f"  reprovaram alguma mutação       : {len(laudo['gatesQueReprovaramAlgumaMutacao'])}")
    print(f"  aprovaram a ruína em toda mutação: {len(laudo['gatesQueSobreviveramATodas'])}")
    print(f"  sumiram do laudo após a mutação : {len(laudo['gatesSemVereditoAposMutacao'])}"
          "  (percebem a ausência; não são complacentes)")

    if laudo["erros"]:
        print(f"\n  ERROS ({len(laudo['erros'])})")
        for erro in laudo["erros"][:6]:
            print(f"    {erro[:150]}")

    if laudo["gatesQueSobreviveramATodas"]:
        print("\n  SOBREVIVERAM A TODAS AS MUTAÇÕES")
        print("  Cada um destes disse `pass` sobre artefato zerado, esvaziado E sem prova.")
        for gate in laudo["gatesQueSobreviveramATodas"]:
            modos = laudo["sobreviventes"].get(gate, {})
            print(f"    {gate:48} {', '.join(sorted(modos)) or '(sem detalhe)'}")

    print("\n  REPROVARAM A MUTAÇÃO (sabem dizer não)")
    for gate in laudo["gatesQueReprovaramAlgumaMutacao"]:
        print(f"    {gate}")


if __name__ == "__main__":  # pragma: no cover
    import argparse

    ap = argparse.ArgumentParser(description="Mede se os gates percebem artefato destruído.")
    ap.add_argument("--json", metavar="ARQUIVO")
    ap.add_argument("--limite", type=int, default=3, help="tentativas mutadas por gate")
    args = ap.parse_args()

    laudo = canario(limite_por_gate=args.limite)
    _relatar(laudo)
    if args.json:
        Path(args.json).write_text(json.dumps(laudo, ensure_ascii=False, indent=2),
                                   encoding="utf-8")
        print(f"\ncanário: {args.json}")
