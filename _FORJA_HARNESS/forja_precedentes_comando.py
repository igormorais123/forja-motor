# -*- coding: utf-8 -*-
"""Gates F7 para precedentes escolhidos no comando e paradigmas de temas.

O produtor resolve duas falhas observadas num caso real em 10/08/2026:

* todo precedente anexado ao comando precisa terminar citado, distinguido de
  forma expressa ou justificado por escrito como não utilizado;
* a primeira menção a tema repetitivo ou de repercussão geral precisa trazer o
  respectivo paradigma.

O veredito é computado. O ledger declara escolhas jurídicas que a máquina não
pode inventar; o código confere cobertura, consistência com os anexos e presença
efetiva da autoridade no texto. Ausência do ledger não vira aprovação tácita.

Regras do retorno humano que este produtor computa, e é por citá-las aqui que a
ligação se confere nos dois sentidos (`forja_aprendizado.py conferir`):

* `regra-ee28e25dbcf6` — todo precedente anexado ao comando deve ser citado,
  distinguido expressamente ou ter o não uso justificado no relatório, sempre
  com localizador verificável;
* `regra-1f38820826f7` — na primeira menção de tema de repercussão geral ou
  recurso repetitivo, identificar também o processo paradigma ou leading case.

Apagar este gate sem revogar as regras faz o identificador sumir junto, e a
conferência acusa — que é exatamente o modo de falha que ela existe para pegar.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from forja_authorities import extract_authorities


ARTEFATO = "F7_PRECEDENTES_DO_COMANDO.json"
DESTINOS = {"cited", "distinguished", "not_used"}
EXTENSOES = {".pdf", ".docx", ".md", ".txt"}

# Mapeamentos confirmados no retorno humano do caso-âncora. Outros temas não
# são adivinhados: precisam ser declarados no ledger do caso.
PARADIGMAS_CONFIRMADOS = {
    ("STF", "897"): [{"court": "STF", "kind": "RE", "number": "852475"}],
    ("STF", "1199"): [{"court": "STF", "kind": "ARE", "number": "843989"}],
    ("STF", "309"): [{"court": "STF", "kind": "RE", "number": "656558"}],
}

TEMA_RE = re.compile(
    r"\bTema\s+(?:Repetitivo\s+)?(?:n[oº.]?\s*)?"
    r"(?P<num>\d{1,3}(?:\.\d{3})+|\d{1,5})"
    r"(?:\s*(?:/|do\s+|[-–—]\s*)\s*(?P<corte>STF|STJ))?",
    re.I,
)


def _norm_num(valor: object) -> str:
    return re.sub(r"\D", "", str(valor or ""))


def _identidade(citacao: dict) -> dict:
    ident = dict(citacao.get("authorityIdentity") or {})
    return {
        "court": str(ident.get("court") or "").upper(),
        "kind": str(ident.get("kind") or "").upper(),
        "number": _norm_num(ident.get("number")),
    }


def _chave(ident: dict, *, ignorar_corte: bool = False) -> tuple[str, str, str]:
    return (
        "" if ignorar_corte else str(ident.get("court") or "").upper(),
        str(ident.get("kind") or "").upper(),
        _norm_num(ident.get("number")),
    )


def _achado(gate: str, problema: str, trecho: str = "") -> dict:
    return {"gate": gate, "sev": "P0", "trecho": trecho[:240], "problema": problema}


def _pastas_anexos(caso: Path) -> list[Path]:
    pastas = []
    for pasta in caso.rglob("*"):
        if pasta.is_dir() and "anexos do email" in pasta.name.casefold():
            pastas.append(pasta)
    return sorted(set(pastas))


def inventariar_precedentes(caso: str | Path) -> list[dict]:
    """Extrai identidades de precedentes dos nomes dos anexos do comando."""
    caso = Path(caso)
    inventario = []
    for pasta in _pastas_anexos(caso):
        for arquivo in sorted(pasta.iterdir()):
            if not arquivo.is_file() or arquivo.suffix.lower() not in EXTENSOES:
                continue
            citacoes = extract_authorities(arquivo.stem)
            identidades = [_identidade(c) for c in citacoes]
            identidades = [i for i in identidades if i["kind"] and i["number"]]
            # Se o nome traz processo e Tema, o arquivo é o acórdão do processo;
            # o Tema será conferido pelo gate próprio, sem contar como sétimo anexo.
            nao_temas = [i for i in identidades if i["kind"] != "TEMA"]
            identidades = nao_temas or identidades
            if identidades:
                inventario.append({
                    "attachment": arquivo.name,
                    "relativePath": str(arquivo.relative_to(caso)),
                    "identities": identidades,
                })
    return inventario


def _carregar_ledger(caso: Path) -> tuple[dict | None, str | None]:
    candidatos = [caso / ARTEFATO]
    candidatos.extend(caso.glob(f"**/{ARTEFATO}"))
    vistos = set()
    for caminho in candidatos:
        chave = str(caminho.resolve()) if caminho.exists() else str(caminho)
        if chave in vistos:
            continue
        vistos.add(chave)
        if caminho.is_file():
            try:
                dados = json.loads(caminho.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                return None, f"{caminho}: {exc}"
            return dados if isinstance(dados, dict) else None, None
    return None, None


def _autoridade_presente(texto: str, identidades: list[dict]) -> bool:
    citadas = [_identidade(c) for c in extract_authorities(texto)]
    for esperada in identidades:
        for citada in citadas:
            if _chave(esperada) == _chave(citada):
                return True
            # Tema pode vir sem corte na sintaxe da peça; número e espécie ainda
            # são verificáveis, enquanto a corte será cobrada pelo paradigma.
            if esperada.get("kind") == "TEMA" and _chave(
                    esperada, ignorar_corte=True) == _chave(citada, ignorar_corte=True):
                return True
    return False


def _destinos_por_anexo(ledger: dict) -> dict[str, dict]:
    saida = {}
    for item in ledger.get("commandPrecedents") or []:
        if not isinstance(item, dict):
            continue
        nome = Path(str(item.get("attachment") or "")).name.casefold()
        if nome:
            saida[nome] = item
    return saida


def gate_precedentes_comando(texto: str, caso: str | Path) -> list[dict]:
    inventario = inventariar_precedentes(caso)
    if not inventario:
        return []
    caso = Path(caso)
    ledger, erro = _carregar_ledger(caso)
    if erro:
        return [_achado("G12-precedentes-comando", "ledger de precedentes inválido", erro)]
    if ledger is None:
        return [_achado(
            "G12-precedentes-comando",
            f"{len(inventario)} precedente(s) anexado(s) ao comando sem {ARTEFATO}",
            ", ".join(i["attachment"] for i in inventario),
        )]

    destinos = _destinos_por_anexo(ledger)
    achados = []
    for anexo in inventario:
        nome = anexo["attachment"]
        item = destinos.get(nome.casefold())
        if not item:
            achados.append(_achado(
                "G12-precedentes-comando",
                "precedente anexado sem destino registrado",
                nome,
            ))
            continue
        destino = str(item.get("destination") or "").strip().casefold()
        if destino not in DESTINOS:
            achados.append(_achado(
                "G12-precedentes-comando",
                "destino inválido; use cited, distinguished ou not_used",
                nome,
            ))
            continue
        if destino == "not_used":
            justificativa = str(item.get("justification") or "").strip()
            localizador = str(item.get("reportLocator") or "").strip()
            if len(justificativa) < 25 or not localizador:
                achados.append(_achado(
                    "G12-precedentes-comando",
                    "não utilização exige justificativa substantiva e localizador no relatório",
                    nome,
                ))
            continue

        if not _autoridade_presente(texto, anexo["identities"]):
            achados.append(_achado(
                "G12-precedentes-comando",
                f"precedente marcado como {destino}, mas sua autoridade não aparece na peça",
                nome,
            ))
        if not str(item.get("pieceLocator") or "").strip():
            achados.append(_achado(
                "G12-precedentes-comando",
                "citação ou distinção exige localizador verificável na peça",
                nome,
            ))
        if destino == "distinguished" and len(str(item.get("justification") or "").strip()) < 25:
            achados.append(_achado(
                "G12-precedentes-comando",
                "distinção exige fundamento substantivo no ledger",
                nome,
            ))
    return achados


def _paradigmas_do_ledger(ledger: dict | None) -> dict[tuple[str, str], list[dict]]:
    saida = {k: [dict(x) for x in v] for k, v in PARADIGMAS_CONFIRMADOS.items()}
    for item in (ledger or {}).get("themeParadigms") or []:
        if not isinstance(item, dict):
            continue
        corte = str(item.get("court") or "").upper()
        tema = _norm_num(item.get("theme"))
        casos = item.get("leadingCases") or []
        identidades = []
        for caso in casos:
            if isinstance(caso, dict):
                ident = {
                    "court": str(caso.get("court") or corte).upper(),
                    "kind": str(caso.get("kind") or "").upper(),
                    "number": _norm_num(caso.get("number")),
                }
                if ident["kind"] and ident["number"]:
                    identidades.append(ident)
        if corte and tema and identidades:
            saida[(corte, tema)] = identidades
    return saida


def gate_tema_paradigma(texto: str, caso: str | Path) -> list[dict]:
    ledger, erro = _carregar_ledger(Path(caso))
    if erro:
        return [_achado("G13-tema-paradigma", "ledger de paradigmas inválido", erro)]
    mapas = _paradigmas_do_ledger(ledger)
    vistos = set()
    achados = []
    for m in TEMA_RE.finditer(texto):
        tema = _norm_num(m.group("num"))
        corte = str(m.group("corte") or "").upper()
        # Quando a menção omite a corte, só há inferência segura se o mapa traz
        # uma única corte para aquele número.
        if not corte:
            cortes = {c for c, n in mapas if n == tema}
            if len(cortes) == 1:
                corte = next(iter(cortes))
        chave = (corte, tema)
        if chave in vistos:
            continue
        vistos.add(chave)
        paradigmas = mapas.get(chave)
        if not paradigmas:
            achados.append(_achado(
                "G13-tema-paradigma",
                "tema citado sem paradigma declarado no ledger do caso",
                m.group(0),
            ))
            continue
        # A primeira referência completa pode estar no corpo ou em nota
        # explicitamente vinculada. Não ampliamos por número bruto de caracteres:
        # isso fez o segundo parágrafo mascarar a omissão no primeiro canário.
        fim_paragrafo = texto.find("\n\n", m.start())
        if fim_paragrafo < 0:
            fim_paragrafo = len(texto)
        recorte = texto[m.start():fim_paragrafo]
        for nota in re.findall(r"\[\^([^\]]+)\]", recorte):
            definicao = re.search(
                rf"(?m)^\[\^{re.escape(nota)}\]:\s*(.+)$", texto)
            if definicao:
                recorte += "\n" + definicao.group(1)
        if not _autoridade_presente(recorte, paradigmas):
            nomes = ", ".join(f"{p['kind']} {p['number']}" for p in paradigmas)
            achados.append(_achado(
                "G13-tema-paradigma",
                f"primeira menção ao Tema {tema}/{corte or '?'} sem o paradigma ({nomes})",
                recorte[:180],
            ))
    return achados


def analisar(texto: str, caso: str | Path) -> list[dict]:
    return gate_precedentes_comando(texto, caso) + gate_tema_paradigma(texto, caso)
