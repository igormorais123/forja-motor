# Por que o F2A degradou — primeira medição

**05/08/2026.** Este documento existe porque o Diabob, no parecer que decidiu
congelar o diagnóstico v2, recusou o congelamento sem investigação: *"congelar
não é o mesmo que investigar causa; sem cronograma, é procrastinação
estruturada"*. É o critério 1 de descongelamento inscrito na § 21 do plano 40.

É **primeira medição, não laudo fechado**. O que está abaixo foi conferido no
código e no acervo hoje; o que não foi medido está nomeado como não medido.

## O que se sabia antes

Que o F2A "virou formulário preenchido em vez de exploração real", e a hipótese
corrente era estrutural: *sem gate no contrato de fase, método bom não acontece*.

## Correção antes de tudo: a hipótese corrente NÃO estava errada

A primeira versão deste documento afirmava ter falsificado o diagnóstico
anterior. Estava errada, e a correção importa porque o erro era meu, não do
registro. Eu confundi dois diagnósticos distintos de 30/07/2026: *"sem gate no
contrato de fase, método bom não acontece"* explica o **PSO-Pet**, que nasceu
`shadow-only` e nunca rodou. Sobre o F2A o registro dizia o oposto — que ele
rodou **porque** tinha validador, gate e ordem — e apontava a causa correta:
*"o gate `exploration_100_complete` premia completude numérica, e a cota é
atingida pelo caminho mais barato: preencher."*

A medição de hoje **confirma** aquilo. E o registro de 30/07 traz evidência
quantitativa que eu havia declarado inexistente, mais dura que a minha:

| Medida nos 7 casos com `FORJA-F2A-100-v1` | Resultado |
|---|---|
| valores distintos de `unansweredConsequence` entre as 100 perguntas | **1** |
| valores distintos de `whyItMatters` | 10 — um por ótica, copiado |
| valores distintos de `caseAnchor` e `downstreamTargets` | **1** |
| casos com 100/100 `answered` e nenhuma bloqueada | 6 de 7 |
| comprimento das respostas | 23 a 59 palavras |

Cem perguntas com uma única consequência declarada não é exploração: é um campo
preenchido cem vezes. Isso é o formulário, medido.

## O que a medição de hoje acrescenta

O gate **existe e é computado**:

- `phase_contracts/F2.json` exige `exploration_100_complete`,
  `answers_provenance_classified` e `downstream_handoff_ready` em `requiredGates`,
  e exige `question_tree` em `requiredOutputs`. Artefato ausente não passa
  despercebido — reprova por output faltante.
- `forja_run._recompute_exploracao` chama `gates_da_exploracao` e grava
  `COMPUTED_EXPLORACAO_GATES.json`. A linha 906 derruba a fase quando a
  exploração reprova. Não é autoatestação: o agente escreve, o orquestrador
  recomputa por cima.
- O gate inclusive **reprova o que não conhece**: código de achado novo, ainda
  não mapeado, derruba `exploration_100_complete` em vez de passar. É o oposto
  de aprovar por omissão.

Havia, sim, autoatestação no passado — `build_f2.py` de um caso real escreve
`"exploration_100_complete": "pass"` na mão. Mas isso é hoje sobrescrito pelo
recomputo.

**Então não é falta de gate.** A hipótese que estava na memória do projeto foi
falsificada por esta medição, e deve ser corrigida lá.

## A causa provável, e por que ela é mais difícil de consertar

O gate confere **catorze condições estruturais**: protocolo declarado, contagem
de 100, dez por ótica, IDs, ausência de duplicata, profundidade, ausência de
placeholder, cobertura, problema, diagnóstico, soluções, profundidade das
soluções e vínculo entre elas. Mais oito de proveniência epistemológica e duas
de handoff.

Todas são satisfeitas por um formulário bem preenchido.

Não há como um verificador determinístico distinguir "cem perguntas que
exploraram o problema" de "cem perguntas que preencheram dez baldes de dez".
Ambas têm 100 itens, dez por ótica, sem duplicata literal, com resposta acima do
comprimento mínimo e com classificação epistemológica declarada. **O gate mede
presença e forma; a degradação é de substância.**

É a mesma família de tudo o que esta fábrica descobriu nos últimos dias: gate de
presença não detecta pobreza. Foi assim no visual, e é assim aqui.

## O que isso significa para o v2

Torna o v2 **menos promissor, não mais**. A proposta do v2 é trocar a cota fixa
de cem por quantidade adaptativa com gates de lastro, causalidade, rival e
parada. Se a cota fixa degrada por ser satisfazível por forma, a quantidade
adaptativa degrada igual — com a agravante de que "adaptativa" remove o único
número que hoje é conferível.

Isso não mata o v2; muda o que ele precisa provar antes de existir.

## O que NÃO foi medido, e portanto não afirmo

- **Não remedi as 16 árvores hoje.** A medição de 30/07 cobriu 7 e é
  suficiente para a conclusão; as 9 posteriores não foram conferidas, e não sei
  se o padrão se manteve, melhorou ou piorou depois daquela data.
- **Não medi se `N4-Q-100-DEPTH` é comprimento de texto ou algo mais forte.**
  Se for comprimento, é o elo mais fraco da cadeia e o mais fácil de satisfazer
  vazio.
- **Não sei quantos dos 53 casos passaram por F2A.** Existem 16 árvores; os
  demais casos podem nunca ter chegado à fase, o que é diferente de terem
  passado sem exploração.

## Próximo passo concreto — e ele já tem forma de gate

A medição de 30/07 não só diagnostica: **entrega o sinal estrutural que faltava.**
"Cem perguntas com um único valor distinto de `unansweredConsequence`" é
conferível por código, determinístico, e não depende de julgar o mérito de
nenhuma resposta. O mesmo vale para `caseAnchor` e `downstreamTargets`.

Um gate de **diversidade de campo** — exigir que a variedade de consequências,
âncoras e destinos cresça com o número de perguntas — reprova o formulário sem
reprovar a exploração legítima, porque exploração real produz consequências
diferentes por pergunta e formulário não. É a contraparte afirmativa que faltava:
o gate atual mede que os campos estão preenchidos; este mediria que dizem coisas
distintas.

Isso muda a ordem das coisas. **Antes de construir o v2, vale construir esse
gate e medir se o v1 se recupera** — que é exatamente o critério 1 de
descongelamento na sua forma mais barata. Falta remedir as 9 árvores posteriores
a 30/07 para calibrar o limiar, e a calibração é obrigatória antes de bloquear,
como em todo gate desta casa.
