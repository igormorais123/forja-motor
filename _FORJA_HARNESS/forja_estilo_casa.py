# -*- coding: utf-8 -*-
"""Perfil de escrita da instalação, sem misturar identidade privada ao motor.

O motor conhece somente este contrato genérico. A configuração concreta vive no
acervo e é resolvida por ``forja_acervo``. O avaliador mede aderência a um método
de comunicação da casa; ele não atribui autoria, não estima "parecença" com uma
pessoa e não autoriza personificação.
"""

from __future__ import annotations

import hashlib
import json
import re
import statistics
import unicodedata
from pathlib import Path
from typing import Any


VERSION = "ARCANO-HOUSE-WRITING-v1"
PROFILE_SCHEMA = "ARCANO-HOUSE-WRITING-PROFILE-v1"
PROFILE_KEY = "perfil-estilo-casa"


class PerfilEstiloInvalido(RuntimeError):
    """O acervo ofereceu um perfil, mas o contrato não pode ser confiado."""


def _caminho_perfil() -> Path | None:
    from forja_acervo import caminho

    return caminho(PROFILE_KEY)


def carregar_perfil(*, exigir: bool = False) -> dict[str, Any] | None:
    """Lê e valida a configuração privada de escrita da instalação."""
    caminho = _caminho_perfil()
    if caminho is None:
        if exigir:
            raise PerfilEstiloInvalido(
                f"perfil {PROFILE_KEY!r} não configurado no acervo"
            )
        return None
    try:
        perfil = json.loads(caminho.read_text(encoding="utf-8"))
    except (OSError, ValueError) as erro:
        raise PerfilEstiloInvalido(f"perfil de escrita ilegível: {erro}") from erro
    if not isinstance(perfil, dict) or perfil.get("schema") != PROFILE_SCHEMA:
        raise PerfilEstiloInvalido(
            f"schema do perfil de escrita deve ser {PROFILE_SCHEMA}"
        )
    if not perfil.get("profileVersion") or not isinstance(perfil.get("channels"), dict):
        raise PerfilEstiloInvalido("perfil de escrita sem versão ou canais")
    return perfil


def _sem_acentos(texto: str) -> str:
    normal = unicodedata.normalize("NFKD", texto.casefold())
    return "".join(c for c in normal if not unicodedata.combining(c))


def _palavras(texto: str) -> list[str]:
    return re.findall(r"\b[\wÀ-ÿ]+\b", texto, re.UNICODE)


def _sentencas(texto: str) -> list[str]:
    partes = re.split(r"(?<=[.!?])\s+(?=[A-ZÁÉÍÓÚÂÊÔÃÕÇ0-9])", texto)
    return [p.strip() for p in partes if len(_palavras(p)) >= 3]


def _contem(texto_normal: str, marcadores: list[str]) -> bool:
    return any(_sem_acentos(str(m)) in texto_normal for m in marcadores if str(m).strip())


def _achado(regra: str, severidade: str, problema: str, acao: str, **extra) -> dict:
    item = {
        "gate": f"G11-padrao-casa/{regra}",
        "sev": severidade,
        "trecho": "",
        "problema": problema,
        "acao": acao,
        "versao": VERSION,
    }
    item.update(extra)
    return item


def prompt(tipo: str, *, perfil: dict[str, Any] | None = None) -> str:
    """Compõe o contrato de geração do canal sem expor corpus ou exemplares."""
    perfil = perfil if perfil is not None else carregar_perfil()
    if not perfil:
        return ""
    canal = (perfil.get("channels") or {}).get(tipo)
    if not isinstance(canal, dict):
        return ""
    nucleo = [str(x).strip() for x in perfil.get("coreMethod") or [] if str(x).strip()]
    regras = [str(x).strip() for x in canal.get("generationRules") or [] if str(x).strip()]
    limites = [str(x).strip() for x in perfil.get("representationLimits") or [] if str(x).strip()]
    linhas = [
        "",
        f"PADRÃO CONFIGURADO DE ESCRITA DA CASA — {perfil['profileVersion']}",
        "Aplique o método abaixo sem copiar frases do corpus e sem representar pessoa real:",
    ]
    linhas.extend(f"- {item}" for item in nucleo)
    linhas.append(f"Regras específicas do canal {tipo}:")
    linhas.extend(f"- {item}" for item in regras)
    linhas.append("Limites de representação:")
    linhas.extend(f"- {item}" for item in limites)
    linhas.append(
        "A conformidade mede método profissional e adequação ao canal; não prova autoria."
    )
    return "\n".join(linhas) + "\n"


def analisar(
    texto: str,
    tipo: str,
    *,
    perfil: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Avalia o contrato positivo da casa para ``email`` ou ``mensagem``.

    O escore serve para localizar desvios. Somente personificação, caricatura ou
    aderência estrutural muito baixa viram P0; distância estilométrica jamais é
    tratada como autoria.
    """
    perfil = perfil if perfil is not None else carregar_perfil()
    if not perfil:
        return {
            "protocolVersion": VERSION,
            "status": "not_configured",
            "applicable": False,
            "approved": True,
            "score": None,
            "findings": [],
            "method": "perfil privado ausente; nenhuma autoria foi inferida",
        }
    canal = (perfil.get("channels") or {}).get(tipo)
    if not isinstance(canal, dict):
        return {
            "protocolVersion": VERSION,
            "profileVersion": perfil.get("profileVersion"),
            "status": "not_applicable",
            "applicable": False,
            "approved": True,
            "score": None,
            "findings": [],
            "method": "canal não configurado; nenhuma autoria foi inferida",
        }

    texto = str(texto or "").strip()
    normal = _sem_acentos(texto)
    palavras = _palavras(texto)
    sentencas = _sentencas(texto)
    tamanhos = [len(_palavras(s)) for s in sentencas]
    mediana = float(statistics.median(tamanhos)) if tamanhos else 0.0
    achados: list[dict] = []

    for padrao in perfil.get("forbiddenPersonificationPatterns") or []:
        if re.search(str(padrao), texto, re.I):
            achados.append(_achado(
                "personificacao",
                "P0",
                "a saída se apresenta como a pessoa real ou lhe atribui voz atual",
                "escreva como sistema do escritório e preserve a autoria/revisão humanas",
            ))
            break

    caricatura = perfil.get("caricature") or {}
    max_total = int(caricatura.get("maxTotal", 1))
    encontrados = {
        termo: len(re.findall(rf"\b{re.escape(_sem_acentos(str(termo)))}\b", normal))
        for termo in caricatura.get("terms") or []
    }
    total_caricatura = sum(encontrados.values())
    if total_caricatura > max_total:
        achados.append(_achado(
            "caricatura-lexical",
            "P0",
            f"marcadores pessoais repetidos ({total_caricatura}; limite={max_total})",
            "retire bordões e preserve apenas a arquitetura profissional do raciocínio",
            contagem=encontrados,
        ))

    marcadores = canal.get("markers") or {}
    janela = int(canal.get("openingWindowWords", 55))
    abertura = _sem_acentos(" ".join(palavras[:janela]))
    direto = _contem(abertura, list(marcadores.get("directOpening") or []))
    lastro = _contem(normal, list(marcadores.get("grounding") or []))
    consequencia = _contem(normal, list(marcadores.get("consequence") or []))
    acao = _contem(normal, list(marcadores.get("nextAction") or []))

    alvos = canal.get("sentenceMedianGuidance") or [0, 10_000]
    minimo, maximo = float(alvos[0]), float(alvos[1])
    if not tamanhos or minimo <= mediana <= maximo:
        pontos_cadencia = 15
    elif minimo * 0.7 <= mediana <= maximo * 1.3:
        pontos_cadencia = 10
    else:
        pontos_cadencia = 5
        achados.append(_achado(
            "cadencia-do-canal",
            "P1",
            f"mediana de {mediana:.1f} palavras por frase fora da faixa-guia {minimo:g}–{maximo:g}",
            "ajuste o ritmo ao canal sem perseguir uma métrica frase a frase",
            medianaPalavrasPorFrase=round(mediana, 2),
        ))

    pontos_abertura = 20 if direto else 8
    pontos_lastro = 20 if lastro else 14
    pontos_consequencia = 20 if consequencia else (10 if len(palavras) < 60 else 2)
    pontos_acao = 25 if acao else (10 if len(palavras) < 35 else 2)
    score = pontos_abertura + pontos_lastro + pontos_consequencia + pontos_acao + pontos_cadencia

    if len(palavras) >= int(canal.get("minimumWordsForStructure", 35)) and not direto:
        achados.append(_achado(
            "questao-central-tardia",
            "P1",
            "a abertura não contém resultado, decisão, questão dominante ou pedido reconhecível",
            "antecipe no primeiro parágrafo o que foi feito ou o que precisa ser decidido",
        ))
    if len(palavras) >= 60 and not consequencia:
        achados.append(_achado(
            "sem-consequencia",
            "P1",
            "o texto desenvolve o assunto sem dizer por que isso muda a decisão ou o risco",
            "ligue o ponto material à consequência prática, processual ou de prazo",
        ))
    if len(palavras) >= int(canal.get("minimumWordsForStructure", 35)) and not acao:
        achados.append(_achado(
            "sem-proximo-movimento",
            "P1",
            "não há providência, responsável, decisão pedida ou fechamento operacional",
            "termine com o próximo movimento proporcional à conversa",
        ))

    minimo_score = int(canal.get("minimumScore", 75))
    bloqueio = int(canal.get("blockingScore", 52))
    if score < minimo_score:
        achados.append(_achado(
            "aderencia-estrutural",
            "P0" if score < bloqueio else "P1",
            f"aderência estrutural {score}/100 abaixo do mínimo {minimo_score}",
            "reorganize a resposta em questão central, lastro/condição, consequência e providência",
            score=score,
            minimo=minimo_score,
        ))

    material = json.dumps(perfil, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return {
        "protocolVersion": VERSION,
        "profileVersion": perfil.get("profileVersion"),
        "profileSha256": hashlib.sha256(material).hexdigest(),
        "status": "active",
        "applicable": True,
        "approved": not any(x.get("sev") == "P0" for x in achados),
        "score": score,
        "dimensions": {
            "directOpening": pontos_abertura,
            "groundingOrCalibration": pontos_lastro,
            "consequence": pontos_consequencia,
            "nextAction": pontos_acao,
            "channelCadence": pontos_cadencia,
        },
        "metrics": {
            "words": len(palavras),
            "sentences": len(sentencas),
            "medianWordsPerSentence": round(mediana, 2),
        },
        "findings": achados,
        "method": (
            "contrato positivo de escrita da casa; distância de gênero não é autoria "
            "e bordão não é identidade"
        ),
    }
