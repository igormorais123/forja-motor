# -*- coding: utf-8 -*-
"""forja_acervo.py — a única porta pela qual o motor pede algo ao acervo.

O motor e o acervo são dois repositórios separados: o primeiro é o sistema e vai
ser compartilhado; o segundo carrega nome de cliente, número de processo e o
texto das peças. Só que o motor precisa alcançar o acervo para trabalhar — a
esteira lê os autos, os testes conferem contra peça aprovada, o gate de fronteira
consulta o registro de nomes.

Sem um ponto único, esse alcance vira caminho escrito à mão espalhado pelo
código, e foi o que aconteceu: em 05/08/2026 o caminho completo de uma peça
protocolada aparecia em três arquivos distintos do motor, com o nome da pasta do
cliente dentro. Aqui o motor pede por CHAVE; o acervo diz onde está.

As três respostas possíveis, e a diferença importa:

    disponivel()      o acervo está montado nesta máquina?
    caminho(chave)    onde está este insumo? `None` quando não há.
    exigir(chave)     o mesmo, mas levanta erro em vez de devolver `None`.

Quem consome precisa distinguir "confere e passou" de "não pude conferir". Um
teste que trata acervo ausente como aprovação é pior do que teste nenhum, porque
fica verde para sempre — é a lição do gate instalado na rota que ninguém percorre.

O registro de chaves vive no acervo, em `state/ACERVO_FIXTURES.json`, porque cada
entrada é um caminho para material de cliente.
"""
from __future__ import annotations

import json
from pathlib import Path

FORJA = Path(__file__).resolve().parent
FABRICA = FORJA.parent
REGISTRO = FORJA / "state" / "ACERVO_FIXTURES.json"


class AcervoIndisponivel(RuntimeError):
    """O insumo pedido depende do acervo, que não está montado aqui."""


def disponivel() -> bool:
    """O acervo está montado? Basta o registro de chaves existir."""
    return REGISTRO.is_file()


def _registro() -> dict[str, str]:
    if not REGISTRO.is_file():
        return {}
    try:
        dados = json.loads(REGISTRO.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return {str(k): str(v) for k, v in (dados.get("chaves") or {}).items()}


def caminho(chave: str) -> Path | None:
    """Caminho real do insumo, ou `None` se o acervo não o oferece.

    O caminho gravado é relativo à pasta de trabalho. Se o arquivo não estiver
    onde o registro diz, a busca cai para o nome do arquivo, porque pasta de caso
    é renomeada de vez em quando e o nome do documento é estável.
    """
    relativo = _registro().get(chave)
    if not relativo:
        return None
    direto = FABRICA / relativo
    if direto.is_file() or direto.is_dir():
        return direto
    return next(FABRICA.rglob(Path(relativo).name), None)


def exigir(chave: str) -> Path:
    alvo = caminho(chave)
    if alvo is None:
        raise AcervoIndisponivel(
            f"o insumo {chave!r} vive no acervo, que não está montado aqui. "
            f"Registro esperado em {REGISTRO.relative_to(FABRICA).as_posix()}.")
    return alvo


CASOS = FORJA / "state" / "ACERVO_CASOS.json"


def caso(rotulo: str) -> str | None:
    """Identificador canônico do caso, a partir do rótulo estável.

    O `caseId` é a chave da cadeia de auditoria e **não pode ser renomeado**:
    ele aparece em milhares de artefatos presos por hash. Só que ele carrega o
    nome do cliente por construção — `case-email-<cliente>-<assunto>-<id>` — e
    por isso não pode ser escrito no motor. O motor pede por rótulo; o acervo
    responde com o identificador verdadeiro.
    """
    if not CASOS.is_file():
        return None
    try:
        dados = json.loads(CASOS.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return (dados.get("casos") or {}).get(rotulo)


def pasta_de_caso(rotulo: str) -> Path | None:
    """Pasta de estado do caso, em `state/<caseId>`."""
    cid = caso(rotulo)
    if not cid:
        return None
    alvo = FORJA / "state" / cid
    return alvo if alvo.exists() else None


VALORES = FORJA / "state" / "ACERVO_VALORES.json"


def valor(chave: str, padrao=None):
    """Valor esperado que deriva de conteúdo de cliente.

    Um teste que confere o resultado de um gate contra uma peça real precisa
    escrever o resultado esperado em algum lugar, e esse resultado carrega o que
    a peça carrega — número de processo, nome de parte. Escrevê-lo no teste põe
    dado de cliente no motor por uma porta que ninguém vigia, porque parece
    constante de teste e não documento.
    """
    if not VALORES.is_file():
        return padrao
    try:
        dados = json.loads(VALORES.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return padrao
    return (dados.get("valores") or {}).get(chave, padrao)


def motivo_da_ausencia(chave: str) -> str:
    """Frase pronta para quem precisa relatar que não pôde verificar."""
    if not disponivel():
        return ("o acervo de auditoria não está montado nesta máquina; "
                "esta verificação não foi feita, e não passou")
    return (f"o acervo está montado mas não oferece {chave!r}; "
            "esta verificação não foi feita, e não passou")
