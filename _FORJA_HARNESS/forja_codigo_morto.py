# -*- coding: utf-8 -*-
"""forja_codigo_morto.py — o que ninguém chama, e a prova de que ninguém chama.

Código morto não é só peso: ele mente. Quem lê a pasta supõe que 153 módulos
são 153 coisas que o sistema faz, e decide a partir daí. Um gate que ninguém
invoca parece proteção; um helper que ninguém chama parece contrato.

O risco de podar é maior que o de deixar, então o critério aqui é
deliberadamente tímido e a prova é textual, não estrutural:

  1. A busca é por TEXTO em toda a árvore, e não pelo grafo de imports. Import
     dinâmico, chamada por `subprocess`, nome citado em protocolo, alvo de
     agendamento e menção em documentação são referências reais, e nenhuma
     delas aparece num grafo de `import`. Quem varre só o grafo apaga o que a
     esteira invoca por nome.
  2. Entrada de linha de comando NÃO é órfã por não ser importada. Metade dos
     módulos da casa existe para ser chamada por uma pessoa.
  3. Suíte de regressão não é morta por ninguém a importar: quem a chama é o
     baseline, que a descobre pelo nome do arquivo.
  4. O que sobra vira CANDIDATO, nunca remoção automática. A decisão é humana
     e o laudo existe para caber numa leitura.

Uso:
    python forja_codigo_morto.py               # laudo legível
    python forja_codigo_morto.py --json        # laudo estruturado
    python forja_codigo_morto.py --simbolos    # inclui funções sem chamador
"""
from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

FORJA = Path(__file__).resolve().parent
RAIZ = FORJA.parent

# Onde procurar referência. Documentação e configuração contam: um módulo
# citado só no protocolo continua sendo parte do sistema, e apagá-lo deixa a
# instrução apontando para o vazio.
EXTENSOES_TEXTO = {".py", ".md", ".json", ".txt", ".yaml", ".yml", ".toml",
                   ".ps1", ".bat", ".cmd", ".sh", ".cfg", ".ini"}

# Árvores que não são fonte: saída de execução, dependência de terceiro,
# material de caso. Varrê-las infla o índice e cria referência fantasma —
# um relatório antigo que cita o módulo não prova que alguém o chama hoje.
PASTAS_IGNORADAS = {
    "state", "telemetria", "reports", "cache", "node_modules", ".git",
    "__pycache__", ".venv", "venv", "_deps", "learning_registry",
    "00_MAPA_ARQUITETURA_IA", ".planning", ".autoresearch", "private",
}

# Nomes que existem para serem descobertos por convenção, e não chamados.
NOMES_DE_CONVENCAO = re.compile(r"^(main|test_|setUp|tearDown|__)")


def _fontes() -> list[Path]:
    """Módulos que respondem pelo sistema: raiz do harness e as ferramentas."""
    fontes = sorted(FORJA.glob("*.py"))
    ferramentas = RAIZ / "_FERRAMENTAS"
    if ferramentas.is_dir():
        fontes += sorted(ferramentas.glob("*.py"))
    return fontes


def _corpus() -> dict[Path, str]:
    """Todo texto onde uma referência pode estar escrita."""
    corpus = {}
    for caminho in RAIZ.rglob("*"):
        if not caminho.is_file() or caminho.suffix.lower() not in EXTENSOES_TEXTO:
            continue
        if PASTAS_IGNORADAS & set(caminho.relative_to(RAIZ).parts):
            continue
        try:
            corpus[caminho] = caminho.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
    return corpus


def _arvore(caminho: Path):
    try:
        return ast.parse(caminho.read_text(encoding="utf-8", errors="replace"))
    except (OSError, SyntaxError):
        return None


def _tem_cli(arvore) -> bool:
    """Módulo com bloco `if __name__ == "__main__"` é chamável por gente."""
    for no in ast.walk(arvore):
        if not isinstance(no, ast.If):
            continue
        alvo = ast.dump(no.test)
        if "__name__" in alvo and "__main__" in alvo:
            return True
    return False


def _simbolos_de_topo(arvore) -> list[tuple[str, int]]:
    """Funções e classes definidas no nível do módulo, com a linha."""
    saida = []
    for no in arvore.body:
        if isinstance(no, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            saida.append((no.name, no.lineno))
    return saida


def _ocorrencias(termo: str, corpus: dict[Path, str], excluir: Path | None) -> list[Path]:
    """Arquivos que mencionam o termo como palavra inteira, fora do próprio."""
    padrao = re.compile(rf"\b{re.escape(termo)}\b")
    return [caminho for caminho, texto in corpus.items()
            if caminho != excluir and padrao.search(texto)]


def medir(com_simbolos: bool = False) -> dict:
    corpus = _corpus()
    fontes = _fontes()

    modulos, sem_arvore = {}, []
    for caminho in fontes:
        arvore = _arvore(caminho)
        if arvore is None:
            sem_arvore.append(str(caminho.relative_to(RAIZ)))
            continue
        modulos[caminho] = arvore

    orfaos, cli_nao_citado, simbolos_sem_chamador = [], [], []

    for caminho, arvore in modulos.items():
        nome = caminho.stem
        rel = str(caminho.relative_to(RAIZ)).replace("\\", "/")
        citacoes = _ocorrencias(nome, corpus, excluir=caminho)
        cli = _tem_cli(arvore)

        if not citacoes:
            registro = {"modulo": rel, "linhas": len(caminho.read_text(
                encoding="utf-8", errors="replace").splitlines()), "temCli": cli}
            if nome.startswith("test_"):
                # Descoberta pelo nome do arquivo: o baseline varre `test_*.py`.
                registro["ressalva"] = "suíte descoberta por convenção; não é órfã por falta de citação"
                continue
            (cli_nao_citado if cli else orfaos).append(registro)

        if not com_simbolos:
            continue
        for simbolo, linha in _simbolos_de_topo(arvore):
            if NOMES_DE_CONVENCAO.match(simbolo):
                continue
            if not _ocorrencias(simbolo, corpus, excluir=caminho):
                # Uso dentro do próprio módulo não conta como chamador externo,
                # mas conta como uso: só entra na lista quem ninguém chama nem
                # de fora nem de dentro.
                texto = caminho.read_text(encoding="utf-8", errors="replace")
                usos_internos = len(re.findall(rf"\b{re.escape(simbolo)}\b", texto))
                if usos_internos <= 1:
                    simbolos_sem_chamador.append(
                        {"modulo": rel, "simbolo": simbolo, "linha": linha})

    return {
        "versao": "FORJA-CODIGO-MORTO-v1",
        "modulosExaminados": len(modulos),
        "arquivosNoCorpus": len(corpus),
        "naoParsearam": sem_arvore,
        "orfaos": sorted(orfaos, key=lambda x: -x["linhas"]),
        "cliNaoCitado": sorted(cli_nao_citado, key=lambda x: -x["linhas"]),
        "simbolosSemChamador": simbolos_sem_chamador,
    }


def relatar(laudo: dict) -> None:
    print("=" * 74)
    print("CÓDIGO SEM CHAMADOR — candidatos, não sentenças")
    print("=" * 74)
    print(f"  módulos examinados : {laudo['modulosExaminados']}")
    print(f"  arquivos no corpus : {laudo['arquivosNoCorpus']}")
    if laudo["naoParsearam"]:
        print(f"  NÃO PARSEARAM     : {len(laudo['naoParsearam'])} — {laudo['naoParsearam'][:3]}")
    print()

    print(f"ÓRFÃOS — ninguém importa, ninguém cita, e não têm linha de comando ({len(laudo['orfaos'])})")
    print("  Nenhuma rota chega até eles. São os candidatos mais fortes.")
    for item in laudo["orfaos"]:
        print(f"    {item['linhas']:5} linhas  {item['modulo']}")
    if not laudo["orfaos"]:
        print("    nenhum")
    print()

    print(f"ENTRADAS NÃO CITADAS — têm linha de comando, ninguém as menciona ({len(laudo['cliNaoCitado'])})")
    print("  Diagnóstico diferente: podem ser ferramenta de mão que alguém usa e")
    print("  nunca documentou. Pedem decisão humana, não remoção.")
    for item in laudo["cliNaoCitado"]:
        print(f"    {item['linhas']:5} linhas  {item['modulo']}")
    if not laudo["cliNaoCitado"]:
        print("    nenhuma")

    if laudo["simbolosSemChamador"]:
        print()
        print(f"FUNÇÕES SEM CHAMADOR ({len(laudo['simbolosSemChamador'])})")
        for item in laudo["simbolosSemChamador"]:
            print(f"    {item['modulo']}:{item['linha']}  {item['simbolo']}")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Varredura de código sem chamador na FORJA.")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--simbolos", action="store_true",
                    help="inclui funções e classes de topo que ninguém chama")
    args = ap.parse_args(argv)

    laudo = medir(com_simbolos=args.simbolos)
    if args.json:
        print(json.dumps(laudo, ensure_ascii=False, indent=2))
    else:
        relatar(laudo)
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main(sys.argv[1:]))
