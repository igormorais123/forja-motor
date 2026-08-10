# -*- coding: utf-8 -*-
"""Catraca da rastreabilidade das lições: o ponteiro tem de resolver.

Medido em 10/08/2026, quando a queixa "o sistema esquece" virou pergunta
respondível: `RETROSPECTIVAS.md` tem 382 lições e 319 números, porque a
numeração foi reiniciada várias vezes ao longo do arquivo. **48 números
designam de duas a cinco lições diferentes.**

O efeito não é estético. Das 27 lições cujo número aparece em código, teste ou
contrato, **9 apontam para um número duplicado** — um terço da rastreabilidade
que a casa julga ter. Uma citação assim não erra o alvo: ela fica sem alvo. E em
pelo menos um caso o texto que cita descreve conteúdo que não bate com nenhum
dos candidatos, o que sugere que a citação já nasceu apontando para outro
arquivo mental.

Por que catraca e não gate absoluto: exigir zero hoje reprovaria o acervo
inteiro por uma dívida acumulada em meses, e gate que nasce vermelho é
desligado na primeira semana — a casa já registrou isso. O que não se pode
aceitar é a dívida **crescer**. Os tetos abaixo são o estado medido no dia; cada
um só pode descer.

Desambiguar as 9 existentes é trabalho de autoria, não de varredura: exige
decidir qual das lições homônimas cada trecho quis citar, e chutar isso seria
gravar no código uma resposta errada com aparência de referência.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import forja_licoes as lic

# Estado medido em 10/08/2026. Tetos, nunca metas: podem descer, nunca subir.
CITACOES_AMBIGUAS_MAX = 9
NUMEROS_AMBIGUOS_MAX = 48

falhas = 0
casos = 0


def checar(nome: str, condicao: bool, detalhe: str = "") -> None:
    global falhas, casos
    casos += 1
    if not condicao:
        falhas += 1
        print(f"  FALHOU: {nome}" + (f" — {detalhe}" if detalhe else ""))


r = lic.retrato()

checar("o arquivo de lições é legível e tem conteúdo", r["licoes"] > 100,
       f"{r['licoes']} lições encontradas")

n_ambiguas = len(r["citacoesAmbiguas"])
checar("nenhuma citação nova aponta para número duplicado",
       n_ambiguas <= CITACOES_AMBIGUAS_MAX,
       f"{n_ambiguas} citações ambíguas, contra o teto de {CITACOES_AMBIGUAS_MAX} "
       f"medido em 10/08/2026 — uma citação nova reusou número já duplicado")

checar("a duplicidade de numeração não cresceu",
       r["numerosAmbiguos"] <= NUMEROS_AMBIGUOS_MAX,
       f"{r['numerosAmbiguos']} números duplicados, contra {NUMEROS_AMBIGUOS_MAX}; "
       f"a lição nova reusou um número em vez de seguir a sequência")

checar("nenhuma citação aponta para lição que não existe no arquivo",
       not r["citacoesSemLicao"],
       "; ".join(f"Lição {n} em {', '.join(a)}"
                 for n, a in list(r["citacoesSemLicao"].items())[:3]))

# O identificador estável é a saída de longo prazo: ele não depende do número
# nem da posição, então uma lição que desce no arquivo continua sendo ela mesma.
ids = [x["id"] for x in r["itens"]]
checar("todo identificador de lição é estável e bem formado",
       all(i.startswith("licao-") and len(i) == 18 for i in ids))

# Duas lições com o mesmo título são a mesma lição repetida, e aí o id coincidir
# é correto; o que não pode é o id mudar quando o arquivo é editado em volta.
antes = lic._ident("Gate instalado em rota que ninguém percorre é gate nenhum")
depois = lic._ident("Gate  instalado   em rota que ninguem percorre e gate nenhum")
checar("o identificador ignora acento e espaçamento, não o conteúdo",
       antes == depois, f"{antes} != {depois}")
checar("títulos diferentes recebem identificadores diferentes",
       lic._ident("uma coisa") != lic._ident("outra coisa"))

if falhas:
    print(f"REGRESSÃO: {falhas} de {casos} casos falharam")
    raise SystemExit(1)
print(f"ok: {casos} casos — {r['licoes']} lições indexadas, "
      f"{n_ambiguas} citação(ões) ambígua(s) sob o teto, "
      f"{r['citadasEmCodigo']} com âncora em código")
