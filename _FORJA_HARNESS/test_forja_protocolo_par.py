# -*- coding: utf-8 -*-
"""A ordem da casa vale para as duas famílias de modelo, ou não é ordem.

`CLAUDE.md` e `AGENTS.md` governam esta fábrica e são lidos por agentes
diferentes: nenhum dos dois carrega o do vizinho. Medido em 11/08/2026, seis
assuntos existiam em um só — entre eles "Gates computados: fim da autovalidação
da esteira" e a seção de anti-alucinação. Uma ordem assim vale para uma família
e não para a outra, e ninguém percebe: cada agente lê o seu e encontra um
documento coerente. O silêncio do outro lado parece concordância.

Este teste não exige que os arquivos sejam iguais — eles têm conteúdo
legitimamente próprio, rota do Codex de um lado e do Claude do outro. Exige
**paridade de assunto**: o que é ordem da casa aparece nos dois, com a redação
de cada um.

Diferente das outras catracas do baseline, esta nasce em zero e por isso é
absoluta, não teto: a divergência foi paga por inteiro no dia em que o gate
entrou, então aceitar uma nova seria retroceder de um estado limpo.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import forja_protocolo_par as par

falhas = 0
casos = 0


def checar(nome: str, condicao: bool, detalhe: str = "") -> None:
    global falhas, casos
    casos += 1
    if not condicao:
        falhas += 1
        print(f"  FALHOU: {nome}" + (f" — {detalhe}" if detalhe else ""))


checar("os dois documentos de protocolo existem",
       par.CLAUDE.is_file() and par.AGENTS.is_file())

r = par.retrato()

checar("nenhum assunto da casa vale só para uma família de modelo",
       r["divergencias"] == 0,
       "; ".join(f"{x['assunto']} (só no CLAUDE)" for x in r["soNoClaude"]) +
       "; ".join(f"{x['assunto']} (só no AGENTS)" for x in r["soNoAgents"]) +
       " — porte o assunto para o outro arquivo, com a redação dele")

# Sonda que não acha nada nos dois lados não prova paridade: prova que a sonda
# apodreceu junto com o assunto que ela deveria vigiar.
checar("nenhuma sonda ficou órfã dos dois documentos",
       not r["emNenhum"],
       "; ".join(x["assunto"] for x in r["emNenhum"]) +
       " — ou o assunto saiu do protocolo, ou o termo da sonda mudou")

checar("a lista de sondas cobre o núcleo do protocolo", r["sondas"] >= 20,
       f"{r['sondas']} sondas")

# A normalização de espaço não é detalhe: a primeira medição deste par deu um
# falso "ausente" porque a expressão estava partida entre duas linhas. Sem esta
# contraprova, o gate mediria formatação e chamaria de divergência.
texto = par._plano(par.CLAUDE)
checar("a leitura junta linhas antes de procurar",
       "  " not in texto and "\n" not in texto,
       "quebra de linha sobreviveu à normalização e produziria falso ausente")

if falhas:
    print(f"REGRESSÃO: {falhas} de {casos} casos falharam")
    raise SystemExit(1)
print(f"ok: {casos} casos — {r['sondas']} assuntos, "
      f"{len(r['nosDois'])} presentes nos dois documentos, 0 divergências")
