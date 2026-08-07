# -*- coding: utf-8 -*-
"""test_forja_codigo_morto.py — a poda tem que ser tímida, e a timidez tem que ser testada.

Esta suíte não protege o resultado da varredura, que muda a cada semana. Ela
protege os quatro critérios que impedem a ferramenta de apagar código vivo, e
cada um nasceu de um erro cometido em 07/08/2026:

  1. `# noqa` e `__future__` sobrevivem. O primeiro é como se declara import
     por efeito colateral; o segundo muda o comportamento do compilador.
  2. Entrada declarada fora do repositório nunca é candidata. `forja_mcp_email`
     apareceu na lista de poda e é o servidor MCP de e-mail registrado em
     `~/.claude.json` — apagá-lo teria removido a ferramenta usada naquela
     mesma sessão para enviar uma peça ao titular.
  3. A poda reescreve o arquivo de trás para a frente. Ir do começo ao fim
     desloca os números de linha depois do primeiro corte, e o corte seguinte
     cai em cima de código.
  4. A gravação preserva a quebra de linha do arquivo. A primeira versão
     converteu arquivos em LF inteiros para CRLF e produziu diff de 200 linhas
     para remover um import.

Uso: python test_forja_codigo_morto.py
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import forja_codigo_morto as cm  # noqa: E402

falhas = 0
casos = 0


def checar(nome: str, condicao: bool, detalhe: str = "") -> None:
    global falhas, casos
    casos += 1
    if not condicao:
        falhas += 1
        print(f"  FALHOU: {nome}" + (f" — {detalhe}" if detalhe else ""))


def escrever(pasta: Path, nome: str, texto: str, *, crlf: bool = False) -> Path:
    caminho = pasta / nome
    dados = texto.replace("\n", "\r\n") if crlf else texto
    with caminho.open("w", encoding="utf-8", newline="") as fh:
        fh.write(dados)
    return caminho


# ------------------------------------------------- o que a poda NÃO pode tocar
with tempfile.TemporaryDirectory() as tmp:
    base = Path(tmp)

    alvo = escrever(base, "protegidos.py", (
        "from __future__ import annotations\n"
        "import forja_fronteira  # noqa: F401  # deixa o módulo disponível ao hook\n"
        "import json\n"
        "\n"
        "def f():\n"
        "    return 1\n"
    ))
    achados = {a["nome"] for a in cm.imports_sem_uso(alvo)}
    checar("`from __future__` nunca entra na lista", "annotations" not in achados)
    checar("import com `# noqa` nunca entra na lista", "forja_fronteira" not in achados)
    checar("import de verdade sem uso entra", "json" in achados, f"achados={achados}")

    alvo = escrever(base, "estrela.py", "from os.path import *\nprint(join('a','b'))\n")
    checar("`import *` desliga a análise da linha", cm.imports_sem_uso(alvo) == [])

    alvo = escrever(base, "anotacao.py", (
        "from __future__ import annotations\n"
        "from pathlib import Path\n"
        "\n"
        "def f(p: Path) -> Path:\n"
        "    return p\n"
    ))
    checar("nome usado só em anotação conta como uso",
           not cm.imports_sem_uso(alvo),
           "com `from __future__ import annotations` a anotação vira texto e some da árvore")


# ------------------------------------------------- a poda em si
with tempfile.TemporaryDirectory() as tmp:
    base = Path(tmp)

    # Dois imports mortos em linhas diferentes, com código entre eles: é aqui
    # que a reescrita de frente para trás apagaria a linha errada.
    alvo = escrever(base, "duplo.py", (
        "import json\n"
        "CONST = 1\n"
        "import os\n"
        "CONST2 = 2\n"
        "\n"
        "def f():\n"
        "    return CONST + CONST2\n"
    ))
    removidos = cm.podar_imports(alvo)
    texto = alvo.read_text(encoding="utf-8")
    checar("remove os dois imports mortos", sorted(removidos) == ["json", "os"])
    checar("e não leva o código junto",
           "CONST = 1" in texto and "CONST2 = 2" in texto and "return CONST + CONST2" in texto,
           texto)

    # Import de várias linhas entre parênteses: recortar só a primeira deixaria
    # os nomes soltos e o arquivo inválido.
    alvo = escrever(base, "multilinha.py", (
        "from collections import (\n"
        "    Counter,\n"
        "    defaultdict,\n"
        ")\n"
        "\n"
        "def f():\n"
        "    return Counter()\n"
    ))
    removidos = cm.podar_imports(alvo)
    texto = alvo.read_text(encoding="utf-8")
    checar("import multilinha: tira só o nome morto", removidos == ["defaultdict"])
    checar("e o que sobrou continua sendo Python válido",
           "Counter" in texto and "defaultdict" not in texto)
    import ast
    try:
        ast.parse(texto)
        valido = True
    except SyntaxError:
        valido = False
    checar("o arquivo podado parseia", valido, texto)

    # Nenhum nome sobrevive: a linha inteira sai.
    alvo = escrever(base, "linha_toda.py", "import json\n\ndef f():\n    return 1\n")
    cm.podar_imports(alvo)
    checar("quando nenhum nome sobrevive, a linha some",
           "import json" not in alvo.read_text(encoding="utf-8"))


# ------------------------------------------------- quebra de linha preservada
with tempfile.TemporaryDirectory() as tmp:
    base = Path(tmp)
    conteudo = "import json\n\ndef f():\n    return 1\n"

    alvo = escrever(base, "arquivo_lf.py", conteudo)
    cm.podar_imports(alvo)
    dados = alvo.read_bytes()
    checar("arquivo em LF continua em LF", b"\r\n" not in dados,
           "converter para CRLF reescreve o arquivo inteiro e esconde a mudança real")

    alvo = escrever(base, "arquivo_crlf.py", conteudo, crlf=True)
    cm.podar_imports(alvo)
    dados = alvo.read_bytes()
    checar("arquivo em CRLF continua em CRLF",
           b"\r\n" in dados and dados.count(b"\n") == dados.count(b"\r\n"))


# ------------------------------------------------- entradas fora do repositório
externas = cm.entradas_externas()
checar("a ferramenta lê as configurações que apontam para dentro do repositório",
       isinstance(externas, dict))
laudo = cm.medir()
candidatos = {x["modulo"] for x in laudo["orfaos"]} | {x["modulo"] for x in laudo["cliNaoCitado"]} \
    | {x["modulo"] for x in laudo["soDocumental"]}
for nome in externas:
    checar(f"entrada externa `{nome}` nunca é candidata a poda",
           not any(c.endswith(f"/{nome}.py") for c in candidatos),
           f"quem a invoca: {externas[nome]}")
if not externas:
    print("  NÃO VERIFICADO: nenhuma entrada externa declarada nesta máquina — "
          "a proteção existe e não pôde ser exercitada contra um caso real")

print(f"ok: {casos} casos — a poda não encosta em import protegido, código ou quebra de linha"
      if not falhas else f"REGRESSÃO: {falhas} de {casos} casos falharam")
sys.exit(1 if falhas else 0)
