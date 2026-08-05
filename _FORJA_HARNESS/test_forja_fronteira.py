# -*- coding: utf-8 -*-
"""test_forja_fronteira.py — a fronteira aprova o legítimo e reprova o vazamento.

Um gate de fronteira tem duas maneiras de ser inútil, e as duas já aconteceram
neste harness em outros gates:

  1. Reprovar o que é correto. Aí alguém o desliga, e ele deixa de existir na
     prática. Foi o que quase aconteceu quando a busca por substring encontrou
     "natura" dentro de "natureza" e acusou quatro capturas oficiais limpas.
  2. Aprovar por não olhar. Um gate que só confere lista de arquivos não vê o
     nome do cliente dentro do arquivo — e foi assim que o repositório do motor
     chegou a 1.843 arquivos com sinal de cliente parecendo separado.

Cada caso aqui existe por causa de um defeito medido em 05/08/2026, e o teste
guarda os dois lados: o que deve passar e o que deve reprovar.

Uso: python test_forja_fronteira.py
Saída: 0 quando todos os casos conferem.
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import forja_fronteira as fr  # noqa: E402

falhas = 0
casos = 0


def checar(nome: str, condicao: bool, detalhe: str = "") -> None:
    global falhas, casos
    casos += 1
    if not condicao:
        falhas += 1
        print(f"  FALHOU: {nome}" + (f" — {detalhe}" if detalhe else ""))


# ---------------------------------------------------------------- classificação
CLASSIFICACAO = [
    ("_FORJA_HARNESS/forja_run.py", fr.MOTOR, "código da esteira"),
    ("_FORJA_HARNESS/phase_contracts/F7.json", fr.MOTOR, "contrato de fase"),
    ("_FERRAMENTAS/medina_visual_kit.py", fr.MOTOR, "kit visual"),
    ("CLAUDE.md", fr.MOTOR, "doutrina da raiz"),
    ("_FORJA_HARNESS/state/case-x/FORJA_STATE.json", fr.ACERVO, "cadeia de auditoria"),
    ("_FORJA_HARNESS/reports/AUDITORIA_X.md", fr.ACERVO, "relatório de execução"),
    ("_MODELOS/peca.docx", fr.ACERVO, "modelo aprovado"),
    ("gestao_escritorio/data/demandas.json", fr.ACERVO, "dado do painel"),
    ("gestao_escritorio/scripts/render_dashboard.py", fr.MOTOR, "código do painel"),
    ("gestao_escritorio/scripts/registrar_entrega_x_20260715.py", fr.ACERVO,
     "script de uma vez só amarrado a um caso"),
    ("Pasta Do Cliente/autos.pdf", fr.LOCAL, "pasta de caso"),
    ("_FORJA_HARNESS/private/post_protocol/x.json", fr.LOCAL, "cofre pós-protocolo"),
    ("qualquer/PEÇA PROTOCOLADA — x.docx", fr.LOCAL, "cofre pós-protocolo"),
    ("_FORJA_HARNESS/__pycache__/x.pyc", fr.LOCAL, "cache"),
    # O nome "cache" enganou uma vez e custou uma suíte reprovada no teste de
    # reconstituição: `cache/fontes_oficiais/` é dado do motor, não descartável.
    ("_FORJA_HARNESS/cache/fontes_oficiais/STF_SUMULA_282.txt", fr.MOTOR,
     "fonte oficial verbatim"),
    ("_FORJA_HARNESS/cache/raw/pagina.html", fr.LOCAL, "captura bruta refazível"),
    # Prompt e manifesto do ciclo AR estão presos por hash na régua e precisam
    # vir ANTES da regra que manda a pasta inteira para o acervo.
    ("_FORJA_HARNESS/autoresearch/prompts/JUIZ_CEGO_PROMPT.md", fr.MOTOR,
     "prompt protegido pela régua"),
    ("_FORJA_HARNESS/autoresearch/ciclos/ciclo-2/x.json", fr.ACERVO,
     "execução do ciclo sobre peça real"),
    ("_FORJA_HARNESS/RELATORIO_X_2026-08-05.md", fr.ACERVO, "registro datado"),
    ("_FORJA_HARNESS/INDICE_FORJA.md", fr.MOTOR, "doutrina, não datada"),
    # Arquivo oculto: `lstrip("./")` removia qualquer ponto inicial e mandava
    # `.gitignore` e as pastas de instrução de agente para LOCAL. O efeito era
    # silencioso — elas simplesmente não eram publicadas, sem nada reprovar.
    (".claude/settings.json", fr.MOTOR, "arquivo oculto: instrução de agente"),
    (".codex/AGENTS.md", fr.MOTOR, "arquivo oculto: instrução de agente"),
    # `.gitignore` pertence ao repositório em que está, e não ao motor: o da
    # pasta de trabalho lista caminhos de pasta de caso, e cada repositório
    # publicado tem o seu, escrito para o que ele guarda.
    (".gitignore", fr.LOCAL, "ignore é do repositório, não do sistema"),
    ("./_FORJA_HARNESS/forja_run.py", fr.MOTOR, "caminho com prefixo ./"),
]
for caminho, esperado, porque in CLASSIFICACAO:
    obtido, motivo = fr.classificar(caminho)
    checar(f"classificação de {caminho} ({porque})", obtido == esperado,
           f"esperado {esperado}, obtido {obtido} — {motivo}")

# Windows escreve com contrabarra; a classificação não pode depender disso.
checar("caminho com contrabarra classifica igual",
       fr.classificar(r"_FORJA_HARNESS\state\case-x\a.json")[0] == fr.ACERVO)


# ------------------------------------------------------------------- detecção
# Nomes inventados. O teste prova o MECANISMO de detecção, e escrever aqui os
# clientes de verdade colocaria no motor exatamente o que este gate existe para
# tirar — o primeiro rascunho fazia isso, e a própria fronteira o reprovou.
# "Cruz" cobre o caso do nome que também é pedaço de palavra comum — aparece
# dentro de "cruzamento" —, que foi o defeito real: um nome de cliente que é
# vocabulário reprovava capturas oficiais limpas.
NOMES = ["Acmelana", "Cruz", "Bela Serra"]
# A curadoria precisa estar carregada ANTES de compilar os padrões: é ela que
# decide se o nome casa por grafia exata. Compilar antes deixava o padrão em
# minúsculas e a busca sensível a caixa, que não casa com nada.
fr._NOMES_AMBIGUOS = {"cruz"}
PADROES = {n: fr._padrao_de_nome(n) for n in NOMES}

# Montados em pedaços de propósito. Escritos por extenso, um CNJ e uma inscrição
# de aparência realista são indistinguíveis de dado real para o próprio gate,
# que então reprova o arquivo que existe para prová-lo. Montar em tempo de
# execução mantém o teste honesto sem deixar no motor algo com cara de processo.
CNJ_FICTICIO = "084" + "7362-19." + "2019" + ".8.26.0100"
OAB_FICTICIA = "OAB/DF " + "47" + ".913"

DEVE_ACUSAR = [
    ("a cliente Acmelana pediu", "NOME:Acmelana", "nome em prosa"),
    ("ACMELANA COMERCIO LTDA", "NOME:Acmelana", "nome em caixa alta"),
    ("o caso Bela  Serra", "NOME:Bela Serra", "espaço duplo entre as palavras"),
    (f"processo {CNJ_FICTICIO}", "CNJ:" + CNJ_FICTICIO, "número CNJ"),
    (f"subscrito por {OAB_FICTICIA}", "OAB:", "inscrição na OAB"),
]
for texto, marca, porque in DEVE_ACUSAR:
    sinais = fr.sinais_no_texto(texto, NOMES, PADROES)
    checar(f"acusa {porque}", any(s.startswith(marca) for s in sinais), str(sinais))

DEVE_PASSAR = [
    # O defeito real: "natura" dentro de "natureza" reprovou quatro capturas
    # oficiais que não têm nada de cliente.
    ("o cruzamento das provas", "nome dentro de outra palavra, em minúscula"),
    ("dados cruzados no laudo", "nome como radical de outra palavra"),
    ("processo 0000000-00.0000.0.00.0000", "CNJ obviamente sintético"),
    ("processo 1234567-89.2020.8.26.0100", "CNJ sequencial de fixture"),
    ("OAB/DF 12345", "inscrição sintética de canário"),
    # A máscara da casa. Sem reconhecê-la, cada rodada de anonimização produz
    # uma safra nova de violações e o gate acusa o próprio remédio.
    ("processo 9000001-00.1997.4.01.0000", "CNJ mascarado pela casa"),
    ("OAB/RS 90.008", "inscrição mascarada pela casa"),
]
for texto, porque in DEVE_PASSAR:
    sinais = fr.sinais_no_texto(texto, NOMES, PADROES)
    checar(f"não acusa {porque}", not sinais, str(sinais))


# ----------------------------------------------------- degradação sem o acervo
with tempfile.TemporaryDirectory() as tmp:
    vazio = Path(tmp)
    nomes, modo = fr.carregar_nomes(vazio)
    checar("sem acervo, o modo é declarado como estrutural", modo == "estrutural", modo)
    checar("sem acervo, nenhum nome é carregado", nomes == [], str(nomes))

    # Um arquivo do motor com CNJ real ainda é reprovado sem o acervo: é o que
    # garante que o gate serve a quem clonou só o motor.
    (vazio / "_FORJA_HARNESS").mkdir(parents=True)
    (vazio / "_FORJA_HARNESS" / "forja_x.py").write_text(
        f"# processo {CNJ_FICTICIO}\n", encoding="utf-8")
    laudo = fr.varrer(vazio)
    checar("sem acervo, o CNJ real ainda reprova", not laudo["aprovado"], str(laudo["violacoes"]))
    checar("sem acervo, o laudo diz em que modo rodou", laudo["modo"] == "estrutural")


# ------------------------------------------------------- binário não declarado
with tempfile.TemporaryDirectory() as tmp:
    raiz = Path(tmp)
    (raiz / "_FORJA_HARNESS").mkdir(parents=True)
    (raiz / "_FORJA_HARNESS" / "planilha.xlsx").write_bytes(b"PK\x03\x04qualquercoisa")
    laudo = fr.varrer(raiz)
    checar("binário não declarado no motor reprova",
           any(v["classe"] == "binario_nao_declarado" for v in laudo["violacoes"]),
           str(laudo["violacoes"]))

    # E o declarado passa: o gate não lê binário, então a lista é a promessa de
    # que alguém olhou. Sem esse lado, a regra reprovaria o timbre da casa.
    (raiz / "_FERRAMENTAS").mkdir()
    (raiz / "_FERRAMENTAS" / "TEMPLATE_MEDINA_OSORIO_PETICAO.docx").write_bytes(b"PK\x03\x04")
    laudo2 = fr.varrer(raiz)
    checar("binário declarado no motor passa",
           not any(v["caminho"].endswith("TEMPLATE_MEDINA_OSORIO_PETICAO.docx")
                   for v in laudo2["violacoes"]))


# --------------------------------------------------- a fábrica real está limpa
laudo_real = fr.varrer(fr.RAIZ_PADRAO)
checar("a pasta de trabalho real passa na fronteira", laudo_real["aprovado"],
       "; ".join(v["caminho"] for v in laudo_real["violacoes"][:5]))
checar("o modo da execução real é nominal", laudo_real["modo"] == "nominal",
       laudo_real["modo"])
checar("o motor tem arquivo suficiente para ser o sistema",
       laudo_real["contagem"][fr.MOTOR] > 300, str(laudo_real["contagem"]))

if falhas:
    print(f"REGRESSÃO: {falhas} de {casos} casos falharam")
    raise SystemExit(1)
print(f"ok: {casos} casos — a fronteira separa motor de acervo, acusa vazamento "
      f"real e não acusa vocabulário nem valor sintético")
