# Inventário da divergência entre `AGENTS.md` e `CLAUDE.md` — 04/08/2026

Os dois arquivos governam o mesmo trabalho para famílias de modelo diferentes: o
Codex lê o `AGENTS.md`, o Claude Code lê o `CLAUDE.md`. **Nenhum é cópia do
outro**, e a reconciliação está pendente desde 03/08 como trabalho consciente.

Este documento não altera nem um nem outro. Ele existe para que a decisão do dono
custe uma leitura em vez de duas.

## O achado que mais importa

**Não há contradição.** Nenhuma regra de um arquivo manda o contrário do outro. A
divergência é inteira de omissão recíproca — cada família opera com um subconjunto
diferente do protocolo, e nenhuma das duas tem tudo.

Isso é melhor do que parecia e pior do que soa. Melhor porque ninguém está sendo
instruído a errar. Pior porque o dano é invisível: um agente cumpre à risca o
arquivo que lê e ignora, sem saber, uma ordem inviolável que só existe no outro.

## Só no `AGENTS.md` — o Claude não vê

| Tema | Onde | O que é |
|---|---|---|
| Mapa de tribunais das pastas | L15-25 | Tabela por caso com o alcance de cada consolidação regimental (STJ até a ER 51, TRF1 até a ER 5/2022) |
| Anti-alucinação | L79-81 | Verificabilidade, marca `[VERIFICAR]`, trabalho sempre em cópia |
| Gates computados | L142-163 | A frente de 04/08: 42 dos 73 gates eram autodeclarados e passaram a Python com veredito |
| Archify e Graphify | L174-183 | Protocolo dos mapas de arquitetura, relações CURATED e INFERRED, regeneração |

## Só no `CLAUDE.md` — o Codex não vê

| Tema | Onde | O que é |
|---|---|---|
| Estratégia visual | L66-68 | As nove técnicas nomeadas: primazia, Von Restorff, fluência, dupla codificação, Gestalt, ancoragem, padrão F |
| Prescrição administrativa por matriz | L100-107 | Ordem de 15/07: separar fundo de direito, metodologia, parcelas, negativa e ciência |
| Atualidade dos regimentos | L126-130 | Conferir metadados e emendas posteriores; vale o regimento vigente na data do protocolo |
| Adiamento do gate F8-S | L102-112 | O estado de observação e o motivo do adiamento, e não só a regra de não decorar o estado |
| Desvio do Libra Sul | L30 | O caso concreto de peça fora do padrão Word, guardado como lição |

## Como eu leria isso

Três das cinco lacunas do lado do Codex são **protocolo jurídico**, não engenharia:
prescrição por matriz, atualidade de regimento e o desvio do Libra Sul valem para
quem redige, seja qual for o modelo. Essas são as que eu levaria primeiro, porque
são as que produzem peça errada.

As duas do lado do Claude que mais pesam são o **mapa de tribunais** — que é
justamente o insumo do protocolo de regimento que só o Claude tem — e a
**anti-alucinação**. Vale notar a ironia: um arquivo tem a regra e o outro tem a
tabela que a regra precisa.

A seção de gates computados e o protocolo Archify são específicos de quem mexe no
harness. Podem ficar onde estão sem prejuízo, desde que isso seja escolha.

## O que este inventário não resolve

A divergência continua crescendo enquanto ninguém decide: a própria seção de gates
computados nasceu hoje, só no `AGENTS.md`, documentando trabalho que também foi
feito por este lado. Dois arquivos vivos, sem regra de propagação, divergem por
construção — o inventário envelhece a cada leva.

A decisão que falta não é qual conteúdo copiar. É se existe uma **fonte única com
um recorte por família**, ou se os dois seguem paralelos com uma conferência
periódica declarada. Enquanto isso não for escolhido, todo inventário é foto.
