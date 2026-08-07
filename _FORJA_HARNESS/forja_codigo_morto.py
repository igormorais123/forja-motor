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
    # Inventários auto-gerados. Eles catalogam TODO arquivo do disco, então
    # citam o módulo abandonado com o mesmo peso com que citam o mais central
    # do sistema. Deixá-los no índice foi o que fez a primeira varredura
    # devolver zero candidatos com ar de boa notícia: a prova de vida era o
    # próprio catálogo dizendo que o arquivo existe.
    "graphify-out", "00_IA_NAVIGACAO",
}

ARQUIVOS_IGNORADOS = {"inventario_ia.json", "arvore_ia.json", "MAPA_IA.md",
                      "INTERFACES_INFERIORES.json", "ARCHIFY_ARQUITETURA.md"}

# Nomes que existem para serem descobertos por convenção, e não chamados.
NOMES_DE_CONVENCAO = re.compile(r"^(main|test_|setUp|tearDown|__)")


def entradas_externas() -> dict[str, str]:
    """Módulos invocados por configuração FORA do repositório. nome -> quem chama.

    Existe por um quase-acidente de 07/08/2026: a varredura apontou
    `forja_mcp_email.py` como candidato a poda, porque nenhum arquivo do
    repositório o importa nem o cita. Ele é o servidor MCP de e-mail, declarado
    em `~/.claude.json`, e apagá-lo teria removido a ferramenta usada naquela
    mesma sessão para enviar uma peça ao titular.

    A lição é geral: **servidor, plugin e hook são invocados por quem está
    fora**, e nenhuma varredura restrita à árvore do projeto pode vê-los. Quem
    varre precisa ir ler as configurações que apontam para dentro.
    """
    achados: dict[str, str] = {}
    for config in (Path.home() / ".claude.json", Path.home() / ".claude" / "settings.json"):
        try:
            dados = json.loads(config.read_text(encoding="utf-8", errors="replace"))
        except (OSError, ValueError):
            continue
        for bloco in _mcp_blocos(dados):
            for nome_servidor, definicao in (bloco or {}).items():
                for argumento in (definicao or {}).get("args", []) or []:
                    if str(argumento).endswith(".py"):
                        achados[Path(str(argumento)).stem] = f"{config.name}: mcpServers.{nome_servidor}"
    return achados


def _mcp_blocos(dados):
    """Todo dicionário `mcpServers` do arquivo, em qualquer profundidade."""
    if isinstance(dados, dict):
        if isinstance(dados.get("mcpServers"), dict):
            yield dados["mcpServers"]
        for valor in dados.values():
            yield from _mcp_blocos(valor)
    elif isinstance(dados, list):
        for item in dados:
            yield from _mcp_blocos(item)


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
        if caminho.name in ARQUIVOS_IGNORADOS:
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


def imports_sem_uso(caminho: Path) -> list[dict]:
    """Nomes importados no topo do módulo que o corpo nunca menciona.

    Três cuidados que separam poda de estrago:

    * `from __future__ import ...` fica sempre. Não é um nome a usar; muda o
      comportamento do compilador, e removê-lo altera a semântica do arquivo.
    * `# noqa: F401` fica sempre. É a forma como quem escreveu declarou que o
      import existe pelo efeito colateral — deixar o módulo carregado para um
      hook, registrar um plugin, disparar a inscrição de um handler.
    * `import *` desliga a análise da linha: não há como saber que nomes
      entraram.

    A busca é textual sobre o corpo sem as linhas de import, e não pela árvore:
    com `from __future__ import annotations` as anotações viram texto, e um
    nome usado só em anotação some da árvore mas continua no arquivo.
    """
    try:
        texto = caminho.read_text(encoding="utf-8", errors="replace")
        arvore = ast.parse(texto)
    except (OSError, SyntaxError):
        return []

    linhas = texto.splitlines()
    importados: dict[str, int] = {}
    # O intervalo COMPLETO de cada import, e não só a linha de abertura: num
    # `from x import (\n  A,\n  B,\n)` os nomes moram nas linhas seguintes, e
    # excluir só a primeira deixava `B` no corpo. O nome aparecia como uso de
    # si mesmo e import multilinha morto nunca era detectado.
    linhas_de_import: set[int] = set()
    for no in arvore.body:
        if not isinstance(no, (ast.Import, ast.ImportFrom)):
            continue
        if isinstance(no, ast.ImportFrom):
            if no.module == "__future__":
                continue
            if any(alias.name == "*" for alias in no.names):
                # Sem saber que nomes entraram, a linha é opaca: ela sai do
                # corpo para não gerar uso fantasma, e nenhum nome é acusado.
                linhas_de_import.update(range(no.lineno, (no.end_lineno or no.lineno) + 1))
                continue
        linhas_de_import.update(range(no.lineno, (no.end_lineno or no.lineno) + 1))
        for alias in no.names:
            if isinstance(no, ast.Import):
                importados[alias.asname or alias.name.split(".")[0]] = no.lineno
            else:
                importados[alias.asname or alias.name] = no.lineno

    if not importados:
        return []

    corpo = "\n".join(l for i, l in enumerate(linhas, 1) if i not in linhas_de_import)
    presentes = set(_IDENTIFICADOR.findall(corpo))

    achados = []
    for nome, lineno in sorted(importados.items(), key=lambda x: x[1]):
        if nome in presentes:
            continue
        if "noqa" in linhas[lineno - 1].lower():
            continue
        achados.append({"nome": nome, "linha": lineno,
                        "texto": linhas[lineno - 1].strip()})
    return achados


def _quem_importa(modulos: dict[Path, ast.Module]) -> dict[str, set[Path]]:
    """nome do módulo -> arquivos que o importam de fato, lido da árvore.

    Separado da busca textual de propósito: `import forja_x` é rota certa,
    ao passo que a palavra `forja_x` numa retrospectiva é só memória.
    """
    mapa: dict[str, set[Path]] = defaultdict(set)
    for caminho, arvore in modulos.items():
        for no in ast.walk(arvore):
            if isinstance(no, ast.Import):
                for alias in no.names:
                    mapa[alias.name.split(".")[0]].add(caminho)
            elif isinstance(no, ast.ImportFrom) and no.module:
                mapa[no.module.split(".")[0]].add(caminho)
            elif isinstance(no, ast.Call):
                # import dinâmico: importlib.import_module("forja_x")
                alvo = getattr(no.func, "attr", None) or getattr(no.func, "id", None)
                if alvo in {"import_module", "__import__"} and no.args:
                    literal = getattr(no.args[0], "value", None)
                    if isinstance(literal, str):
                        mapa[literal.split(".")[0]].add(caminho)
    return mapa


def _simbolos_de_topo(arvore) -> list[tuple[str, int]]:
    """Funções e classes definidas no nível do módulo, com a linha."""
    saida = []
    for no in arvore.body:
        if isinstance(no, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            saida.append((no.name, no.lineno))
    return saida


_IDENTIFICADOR = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")


def _sem_prosa(texto: str) -> str:
    """Remove comentários e docstrings de um .py, preservando o resto.

    O nome de um módulo escrito num comentário ou numa docstring é
    documentação, e documentação não invoca ninguém. Sem esta separação, um
    módulo abandonado que a própria vizinhança menciona em prosa aparece vivo,
    e a varredura devolve zero candidatos com ar de boa notícia.

    As demais cadeias de texto FICAM: `subprocess.run(["python", "forja_x.py"])`
    é rota de verdade, e apagá-la do índice criaria falso positivo — que aqui é
    o erro caro, porque termina em remoção.
    """
    import io
    import tokenize

    try:
        arvore = ast.parse(texto)
    except SyntaxError:
        return texto

    docstrings = set()
    for no in ast.walk(arvore):
        if not isinstance(no, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef,
                               ast.ClassDef)):
            continue
        corpo = getattr(no, "body", None)
        if corpo and isinstance(corpo[0], ast.Expr) and isinstance(corpo[0].value, ast.Constant) \
                and isinstance(corpo[0].value.value, str):
            docstrings.add((corpo[0].lineno, corpo[0].col_offset))

    pedacos = []
    try:
        for tok in tokenize.generate_tokens(io.StringIO(texto).readline):
            if tok.type == tokenize.COMMENT:
                continue
            if tok.type == tokenize.STRING and tok.start in docstrings:
                continue
            pedacos.append(tok.string)
    except (tokenize.TokenError, IndentationError):
        return texto
    return "\n".join(pedacos)


def _indice_executavel(corpus: dict[Path, str]) -> dict[str, set[Path]]:
    """Índice só do que pode invocar: código, configuração e script de shell.

    Markdown fica de fora inteiro. `.py` entra sem comentários nem docstrings.
    """
    indice: dict[str, set[Path]] = defaultdict(set)
    for caminho, texto in corpus.items():
        if caminho.suffix.lower() == ".md":
            continue
        util = _sem_prosa(texto) if caminho.suffix.lower() == ".py" else texto
        for token in set(_IDENTIFICADOR.findall(util)):
            indice[token].add(caminho)
    return indice


def _indice(corpus: dict[Path, str]) -> dict[str, set[Path]]:
    """token -> arquivos que o contêm. Uma passada pelo corpus, não uma por termo.

    A versão ingênua procurava cada nome em cada arquivo: com 153 módulos e
    milhares de arquivos, são centenas de milhares de varreduras de texto e o
    laudo não terminava. O índice inverte isso — o corpus é lido uma vez, e a
    consulta de cada nome vira uma busca em dicionário.
    """
    indice: dict[str, set[Path]] = defaultdict(set)
    for caminho, texto in corpus.items():
        for token in set(_IDENTIFICADOR.findall(texto)):
            indice[token].add(caminho)
    return indice


def _ocorrencias(termo: str, indice: dict[str, set[Path]], excluir: Path | None) -> list[Path]:
    """Arquivos que mencionam o termo como palavra inteira, fora do próprio."""
    return sorted(indice.get(termo, set()) - {excluir})


def medir(com_simbolos: bool = False) -> dict:
    corpus = _corpus()
    indice = _indice(corpus)
    executavel = _indice_executavel(corpus)
    fontes = _fontes()

    modulos, sem_arvore = {}, []
    for caminho in fontes:
        arvore = _arvore(caminho)
        if arvore is None:
            sem_arvore.append(str(caminho.relative_to(RAIZ)))
            continue
        modulos[caminho] = arvore

    importadores = _quem_importa(modulos)
    externas = entradas_externas()

    orfaos, cli_nao_citado, so_documental, simbolos_sem_chamador = [], [], [], []

    for caminho, arvore in modulos.items():
        nome = caminho.stem
        rel = str(caminho.relative_to(RAIZ)).replace("\\", "/")
        citacoes = _ocorrencias(nome, indice, excluir=caminho)
        cli = _tem_cli(arvore)
        linhas = len(caminho.read_text(encoding="utf-8", errors="replace").splitlines())

        if nome.startswith("test_"):
            # Descoberta pelo nome do arquivo: o baseline varre `test_*.py`.
            continue
        if nome in externas:
            # Alcançado de fora do repositório. Nunca é candidato.
            continue

        importado_por = sorted(str(p.relative_to(RAIZ)).replace("\\", "/")
                               for p in importadores.get(nome, ()))
        # Citação em código ou configuração é rota possível; citação apenas em
        # documentação é lápide. As duas contam como "menção" e significam
        # coisas opostas: a segunda descreve o sistema que se pretendeu.
        executaveis = _ocorrencias(nome, executavel, excluir=caminho)
        registro = {"modulo": rel, "linhas": linhas, "temCli": cli,
                    "importadoPor": importado_por,
                    "citadoEmCodigoOuConfig": len(executaveis),
                    "citadoEmDocumentacao": len(citacoes) - len(executaveis)}

        if not citacoes:
            (cli_nao_citado if cli else orfaos).append(registro)
        elif not importado_por and not executaveis:
            so_documental.append(registro)

        if not com_simbolos:
            continue
        for simbolo, linha in _simbolos_de_topo(arvore):
            if NOMES_DE_CONVENCAO.match(simbolo):
                continue
            if not _ocorrencias(simbolo, indice, excluir=caminho):
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
        "soDocumental": sorted(so_documental, key=lambda x: -x["linhas"]),
        "simbolosSemChamador": simbolos_sem_chamador,
        "importsSemUso": [
            {"modulo": str(c.relative_to(RAIZ)).replace("\\", "/"), **achado}
            for c in modulos for achado in imports_sem_uso(c)
        ],
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
    print()

    print(f"SÓ DOCUMENTAL — ninguém importa nem invoca; existe em texto ({len(laudo['soDocumental'])})")
    print("  A menção é lápide, não rota: descreve o sistema que se pretendeu.")
    for item in laudo["soDocumental"]:
        print(f"    {item['linhas']:5} linhas  {item['modulo']:58} "
              f"(citado em {item['citadoEmDocumentacao']} doc)")
    if not laudo["soDocumental"]:
        print("    nenhum")

    print()
    print(f"IMPORTS SEM USO ({len(laudo['importsSemUso'])})")
    print("  Poda mecânica: o nome não aparece em lugar nenhum do corpo.")
    for item in laudo["importsSemUso"]:
        print(f"    {item['modulo']}:{item['linha']}  {item['nome']}")
    if not laudo["importsSemUso"]:
        print("    nenhum")

    if laudo["simbolosSemChamador"]:
        print()
        print(f"FUNÇÕES SEM CHAMADOR ({len(laudo['simbolosSemChamador'])})")
        for item in laudo["simbolosSemChamador"]:
            print(f"    {item['modulo']}:{item['linha']}  {item['simbolo']}")


def podar_imports(caminho: Path) -> list[str]:
    """Remove os nomes importados e não usados. Devolve o que saiu.

    Só reescreve o arquivo se o resultado ainda for Python válido: um erro de
    sintaxe aqui destrói um módulo, e a poda não vale esse risco. Reconstrói a
    linha em vez de apagá-la quando o import traz outros nomes que continuam em
    uso, e apaga a linha inteira quando nenhum sobrevive.
    """
    achados = imports_sem_uso(caminho)
    if not achados:
        return []

    # `newline=""` nas duas pontas: sem isso o Python traduz a quebra de linha
    # na gravação e um arquivo em LF volta inteiro em CRLF. O conteúdo fica
    # correto e o diff mostra 200 linhas alteradas para remover um import —
    # o que esconde a mudança real no meio do ruído e atrapalha quem revisa.
    with caminho.open("r", encoding="utf-8", newline="") as fh:
        texto = fh.read()
    linhas = texto.splitlines(keepends=True)
    arvore = ast.parse(texto)
    # A linha que eu componho tem de terminar como as do arquivo. Compor com
    # "\n" dentro de um arquivo CRLF deixa o arquivo misto e o diff mostra o
    # bloco inteiro trocado — o mesmo ruído que o `newline=""` acabou de fechar,
    # entrando pela outra porta.
    quebra = "\r\n" if texto.count("\r\n") > texto.count("\n") - texto.count("\r\n") else "\n"
    mortos_por_linha: dict[int, set[str]] = defaultdict(set)
    for achado in achados:
        mortos_por_linha[achado["linha"]].add(achado["nome"])

    removidos: list[str] = []
    # De trás para a frente: reescrever um import de três linhas como uma só
    # desloca todo número de linha posterior, e o corte seguinte cairia no
    # lugar errado — apagando código em vez de import. Indo do fim ao começo,
    # os índices ainda não visitados permanecem válidos.
    for no in sorted(arvore.body, key=lambda n: getattr(n, "lineno", 0), reverse=True):
        if not isinstance(no, (ast.Import, ast.ImportFrom)):
            continue
        mortos = mortos_por_linha.get(no.lineno)
        if not mortos:
            continue
        # `end_lineno` cobre o import que se espalha por várias linhas entre
        # parênteses; recortar só a primeira deixaria os nomes soltos no
        # arquivo e produziria erro de sintaxe.
        inicio, fim = no.lineno - 1, (no.end_lineno or no.lineno)
        vivos = [alias for alias in no.names
                 if (alias.asname or alias.name.split(".")[0]) not in mortos]
        indentacao = linhas[inicio][:len(linhas[inicio]) - len(linhas[inicio].lstrip())]

        def _escrito(alias):
            return alias.name + (f" as {alias.asname}" if alias.asname else "")

        multilinha = fim - inicio > 1
        if not vivos:
            novas = []
        elif isinstance(no, ast.Import):
            novas = [f"{indentacao}import {', '.join(_escrito(a) for a in vivos)}{quebra}"]
        elif multilinha:
            # O arquivo escolheu a forma entre parênteses, provavelmente porque
            # a linha única não caberia. Reescrever tudo numa linha só é
            # reformatar código a pretexto de podar: o diff cresce, a linha
            # estoura a largura da casa e quem revisa perde a mudança real.
            cabeca = f"{indentacao}from {'.' * no.level}{no.module or ''} import ({quebra}"
            corpo_import = [f"{indentacao}    {_escrito(a)},{quebra}" for a in vivos]
            novas = [cabeca, *corpo_import, f"{indentacao}){quebra}"]
        else:
            nomes = ", ".join(_escrito(a) for a in vivos)
            novas = [f"{indentacao}from {'.' * no.level}{no.module or ''} import {nomes}{quebra}"]

        linhas[inicio:fim] = novas
        removidos.extend(sorted(mortos))

    novo = "".join(linhas)
    try:
        ast.parse(novo)
    except SyntaxError as erro:
        raise RuntimeError(f"poda deixaria {caminho.name} inválido: {erro}") from erro

    with caminho.open("w", encoding="utf-8", newline="") as fh:
        fh.write(novo)
    return removidos


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Varredura de código sem chamador na FORJA.")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--simbolos", action="store_true",
                    help="inclui funções e classes de topo que ninguém chama")
    ap.add_argument("--podar-imports", action="store_true",
                    help="remove os imports sem uso; reprova se deixar o arquivo inválido")
    args = ap.parse_args(argv)

    if args.podar_imports:
        total = 0
        for caminho in _fontes():
            removidos = podar_imports(caminho)
            if removidos:
                total += len(removidos)
                print(f"  {caminho.name}: {', '.join(removidos)}")
        print(f"{total} import(s) sem uso removido(s)")
        return 0

    laudo = medir(com_simbolos=args.simbolos)
    if args.json:
        print(json.dumps(laudo, ensure_ascii=False, indent=2))
    else:
        relatar(laudo)
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main(sys.argv[1:]))
