# PRD — Ponderação e inteligência dos grafos da fábrica

**Versão:** v2, 05/08/2026. Substitui a v1 do mesmo dia.
**Origem:** plano 42 (`_FORJA_HARNESS\planejamento\42_PLANO_GRAFOS_PONDERADOS.md`).
**Redação:** v1 por Claude Fable 5 sob briefing; revisão adversarial por Claude Fable 5 em sessão separada, com briefing montado pela skill `forja-briefing-revisor`; correção de transporte, conferência na fonte e consolidação da v2 por Claude Opus 5.
**`familyAssurance`: `cross_session_same_family`.** Fable 5 e Opus 5 são da mesma família. A revisão foi cega quanto ao contexto do construtor e leu fonte primária, mas não substitui a perna cruzada com a outra família (Codex/GPT), que segue em aberto — motivo da degradação registrado aqui, conforme o protocolo.

**Objetivo:** fazer o grafo de raciocínio jurídico deixar de ser documentação e virar estrutura consultável, capaz de apontar antes do protocolo onde a argumentação está exposta.

**Métrica de sucesso:** três achados que hoje ninguém produz (tese sem lastro, exposição concentrada, parágrafo órfão por fonte desatualizada) saindo automaticamente no relatório de melhorias, com o número decomposto até a aresta que o gerou.

---

## 1. Problema, corrigido pela revisão

### A. O grafo tem aresta e não tem peso

O `F3_REASONING_GRAPH.json` estrutura nós (documento, tese, pedido, decisão) e arestas (`supports`, `qualifies`, `justifies`, entre treze relações previstas) com profundidade jurídica real: `scope`, `reason`, `reviewStatus`. Não há número em lugar nenhum. O grafo não sabe força da fonte, não sabe se a tese cai quando a aresta cai, não sabe idade da conferência.

### B. E ninguém nunca percorreu uma aresta — fato apurado na revisão

A v1 afirmava que a única travessia do harness era `_dependency_cycles`, em `forja_reasoning.py:112`. Certo quanto ao código, errado quanto ao efeito. Aquela função só monta o grafo com arestas de relação `depends_on`. A varredura dos cinco `F3_REASONING_GRAPH.json` reais do harness — 49 arestas ao todo — devolve `supports` 19, `justifies` 12, `qualifies` 8, `records` 4, `limits` 4, `distinguishes` 2 e **zero `depends_on`**.

O detector de ciclo monta grafo vazio e devolve lista vazia em toda execução, desde sempre. **Nenhuma aresta de raciocínio jurídico jamais foi percorrida nesta fábrica.** Todo o resto do consumo é pertinência de id: os leitores montam o conjunto de ids de nós e checam se um `supportId` de outro artefato existe ali.

Consequência para o escopo: M1 e M2 não estendem uma capacidade existente. Eles criam a primeira.

### C. E os dois artefatos que precisariam conversar não têm chave comum

O `paragraph_provenance.json` real tem a forma `{main, note}`, cada um com `paragraphs[]`, e cada parágrafo é `{id, textPrefix, provenance, status}`. O campo `provenance` é **texto livre nomeando ledgers** — por exemplo `"fact_ledger/source_ledger/strategic_analysis"`. Não há nenhum campo que referencie `SRC_*` ou `THESIS-*`.

Ou seja: hoje é impossível responder "esta fonte caiu; que parágrafos ficaram sem lastro?", porque não existe a chave. M2-R3 depende de criá-la (§4.3).

### D. Os quatro defeitos transversais

1. O peso está onde não decide (a fila pontua e não tem aresta) e falta onde decide.
2. Grafo que ninguém percorre é desenho — e aqui o não percorrer é literal.
3. Uma dimensão por grafo: o reasoning graph só sabe "confirmado / não confirmado".
4. Nada envelhece: regimento baixado em 06/07 pesa igual a um conferido hoje.

---

## 2. Solução

Dois módulos determinísticos, ambos PROPOSTOS: `forja_grafo_pesos.py` (M1) pondera as arestas por tabela normativa fechada e deriva três medidas; `forja_grafo_consulta.py` (M2) percorre o grafo ponderado e responde três perguntas. Nenhum dos dois usa modelo de linguagem, rede ou heurística opaca.

---

## 3. M1 — ponderar o grafo

### 3.1 Campos novos, todos opcionais

| Campo | Onde | Tipo | Default quando ausente |
|---|---|---|---|
| `strength` | aresta | 0–1, valor da tabela | `0,3` (o piso — inferência declarada) |
| `necessity` | aresta | 0–1, valor da tabela | `1,0` (pior caso: presume-se que a tese cai) |
| `verifiedAt` | aresta | data ISO | ausente; a aresta entra como não conferida e a consulta de decaimento a lista à parte |
| `criticality` | nó `thesis` | 0–1, valor da tabela | `1,0` (pior caso: presume-se pedido decisivo) |

Os defaults são **conservadores por desenho**: na dúvida, a fonte vale pouco e a tese importa muito, de modo que a ausência de dado empurra o caso para o gate e não para longe dele. Todo default aplicado é **impresso nominalmente no relatório**, com a contagem de arestas afetadas. Default silencioso é bloqueador (§10).

### 3.2 Tabela normativa, fechada

| Campo | Valor | Quando |
|---|---|---|
| `strength` | 1,0 | documento oficial juntado aos autos |
| | 0,9 | ato oficial externo conferido na fonte oficial |
| | 0,8 | precedente com inteiro teor lido e conferido |
| | 0,5 | doutrina |
| | 0,3 | inferência declarada |
| `necessity` | 1,0 | a tese cai se esta aresta cair |
| | 0,5 | a tese enfraquece |
| | 0,2 | redundante — há outra aresta equivalente |
| `criticality` | 1,0 | pedido decisivo |
| | 0,5 | pedido subsidiário |
| | 0,2 | pedido acessório |

**Por que cinco degraus e não escala contínua** (achado 7 da revisão): escala contínua convida o atribuidor a produzir 0,72 e a chamar isso de medida. Os cinco degraus de `strength` correspondem a categorias probatórias que o escritório já distingue na prática e que um auditor humano consegue conferir olhando a fonte. Valor intermediário é rejeição, não arredondamento.

### 3.3 Agregação — decisão técnica revista

A v1 propunha `lastro = Σ(strength × necessity)`. A revisão derrubou isso por dois motivos corretos: a soma cresce sem limite e colide com limiares em escala 0–1 (achado 10), e não distingue uma fonte forte de cinco fracas (achado 3). **A v2 troca soma por OU ruidoso (*noisy-OR*):**

```
contribuição da aresta e = strength(e) × necessity(e)
lastro(tese) = 1 − Π (1 − contribuição(e)), sobre as arestas sustentadoras de entrada
```

O que isso resolve, de uma vez:

- Fica em [0, 1] por construção. Nunca colide com o limiar.
- Redundância soma, mas com retorno decrescente, que é como prova funciona: duas fontes de 0,5 dão 0,75, mais que cada uma sozinha e menos que uma fonte de 1,0.
- Cinco fontes de 0,2 dão 0,67 — abaixo de uma única fonte de 1,0. A estrutura passa a estar no número, que é exatamente o que a revisão apontou faltar.

**Duas restrições que a fórmula exige e ficam declaradas:**

1. *OU ruidoso* pressupõe independência entre as fontes. Fontes não são independentes quando derivam do mesmo ato. Por isso, **uma fonte contribui uma vez**: havendo mais de uma aresta do mesmo nó de origem para a mesma tese, vale a de maior contribuição e as demais entram no relatório como redundantes internas.
2. Contam para o lastro apenas as relações **sustentadoras** — `supports` e `justifies`. `qualifies`, `limits` e `distinguishes` entram no relatório como modulação, e não como lastro. Somar uma qualificadora ao lastro seria contar a favor uma aresta que restringe.

### 3.4 As três medidas derivadas

| Medida | Definição | Leitura |
|---|---|---|
| **Lastro** | fórmula de §3.3 | quanto de sustentação a tese tem, em [0,1] |
| **Exposição concentrada** | `1 − lastro_sem_a_fonte_de_maior_contribuição / lastro` | fração do lastro que evapora se a fonte principal cair |
| **Tese órfã** | nenhuma aresta sustentadora de entrada | binário |

Nenhuma delas é escrita à mão: são sempre recalculadas a partir do grafo, e o relatório decompõe cada uma listando as arestas que a compõem.

### 3.5 Exposição concentrada não é defeito por si — correção do achado 8

A revisão tem razão no ponto mais importante: em contrarrazões construídas em torno de um ato novo do tribunal, concentrar quatro teses na decisão recorrida é **arquitetura correta**, não fragilidade. Um gate que reprovasse isso produziria falso positivo justamente nas peças bem feitas.

A v2 separa exposição de defeito. A exposição é sempre medida e sempre relatada; a severidade depende da natureza da fonte que concentra:

| Situação | Severidade | Racional |
|---|---|---|
| exposição > limiar, fonte concentradora com `strength` 1,0 (documento nos autos) | **P2, informativo** | é a arquitetura esperada; o relatório apenas nomeia onde a peça está apoiada |
| exposição > limiar, fonte concentradora com `strength` < 1,0 | **P1** | a peça depende de um único apoio que não é documento dos autos |
| tese órfã sustentando pedido decisivo | **P1** | falta aresta ou falta fonte; nos dois casos há o que responder antes de protocolar |
| tese com lastro abaixo do mínimo sustentando pedido decisivo | **P1** | — |

O gate nunca usa a palavra "fragilidade" na saída. Usa "exposição", e diz a quê.

### 3.6 Requisitos M1

| ID | Requisito | Aceite |
|---|---|---|
| M1-R1 | Estender o schema com os quatro campos opcionais de §3.1; grafo antigo valida sem erro. | Validação existente continua verde em grafo sem os campos; teste confirma default aplicado e impresso. |
| M1-R2 | Só os valores da tabela de §3.2 são aceitos; valor intermediário é rejeitado nomeando a regra violada. | Teste por valor válido e teste de rejeição. |
| M1-R3 | Implementar a agregação de §3.3, com as duas restrições (fonte conta uma vez; só relação sustentadora entra no lastro). | Testes unitários das duas restrições, além das âncoras de §9. |
| M1-R4 | Derivar as três medidas de §3.4 sem nunca gravá-las no artefato canônico. | O `F3_REASONING_GRAPH.json` de entrada sai da execução byte a byte idêntico. |
| M1-R5 | Gate em F7 com a matriz de severidade de §3.5; todo achado imprime o parâmetro e o valor vigente que o disparou. | Ver §9. |
| M1-R6 | Módulo `forja_grafo_pesos.py`: função pura, entrada é o payload, saída é cópia com `derivedMetrics`. | Grafo de entrada não mutado. |
| M1-R7 | Regressão-âncora com o CASO-04 (§9.3). | Suíte verde e incorporada à baseline. |
| M1-R8 | **Calibração pré-produção** antes de ligar o gate (§6.1). | Artefato de calibração existe e o valor de config aponta para ele. |

---

## 4. M2 — percorrer o grafo

### 4.1 Caminho crítico fonte → tese → pedido

Ordena as fontes por quanto do pedido cai se cada uma cair. Para cada fonte, remove-se a fonte do grafo, recalcula-se o lastro de todas as teses e mede-se a queda ponderada pela `criticality` de cada tese e pela ligação tese → pedido. Saída em JSON: fonte, teses atingidas, pedidos atingidos, queda.

É recálculo, não heurística: a mesma fórmula de §3.3 rodada sobre o grafo sem aquele nó.

### 4.2 Corte mínimo — com a ressalva que a revisão exigiu

Menor conjunto de fontes cuja queda leva todo pedido abaixo do lastro mínimo. Busca exaustiva sobre subconjuntos, viável porque os grafos têm dezenas de nós.

**Ressalva obrigatória, que vai impressa na saída e no relatório** (achado 5): o corte mínimo é modelo matemático de vulnerabilidade estrutural. Não é o que a parte adversária fará. O adversário real ataca admissibilidade, deturpa a *ratio*, explora premissa não declarada e omissão — coisas que não estão no grafo. **O corte mínimo alimenta o red team de nove perguntas; não o substitui, e não dispensa nenhuma delas.** Qualquer leitura de que "o red team já foi feito pelo grafo" é uso indevido.

### 4.3 Propagação de invalidação — o contrato que faltava

O achado 1 da revisão está confirmado e é mais grave do que ele descreveu: não é que o contrato esteja mal especificado, é que **não existe chave**. O campo `provenance` do parágrafo é texto livre nomeando ledgers.

Contrato definido nesta v2:

1. Cada parágrafo do `paragraph_provenance.json` ganha o campo **opcional** `supportIds: []`, com ids de nós do `F3_REASONING_GRAPH` do mesmo caso — normalmente `THESIS-*`, podendo ser `SRC_*` quando o parágrafo cita a fonte diretamente. O campo `provenance` em texto livre permanece, sem alteração, para não quebrar leitor existente.
2. Integridade referencial vira validação: `supportId` que não exista no grafo do caso é achado, no mesmo formato dos `N4-CROSS-*` que `forja_n4_validate._cross_reference_findings` já emite para as outras travessias de id.
3. Enquanto o campo não estiver populado, a propagação **declara cobertura parcial e diz quantos parágrafos ficaram fora**. Não estima por semelhança de texto, não infere por proximidade. Cobertura parcial declarada é resultado; cobertura silenciosa é bloqueador.
4. A cascata: fonte marcada desatualizada → teses que perdem lastro → parágrafos cujo `supportIds` só apontava para aquelas teses. Saída nomeia os três níveis.

**Quem popula `supportIds`.** É trabalho do produtor de F6, não de inferência automática. Enquanto a população não estiver na rotina, M2-R3 roda em cobertura parcial e o número aparece no relatório — que é a forma de tornar a lacuna visível em vez de fingir que não existe.

### 4.4 Requisitos M2

| ID | Requisito | Aceite |
|---|---|---|
| M2-R1 | Caminho crítico por recálculo (§4.1). | No CASO-04, `SRC_A8` encabeça o ranking. |
| M2-R2 | Corte mínimo com a ressalva de §4.2 impressa na saída e no relatório. | A ressalva aparece no JSON e no template; teste verifica a presença. |
| M2-R3 | Propagação com o contrato de §4.3, incluindo declaração de cobertura parcial. | Teste com `supportIds` presente e teste com ausente, este último verificando que a cobertura parcial é declarada. |
| M2-R4 | Campo `supportIds` opcional no schema de proveniência + validação de integridade referencial. | Grafo e proveniência antigos continuam válidos. |
| M2-R5 | Módulo `forja_grafo_consulta.py` com as três consultas e CLI. | Saída JSON estruturada. |
| M2-R6 | Seção "Inteligência do grafo de raciocínio" no relatório de melhorias, com as três tabelas e a ressalva do corte mínimo. | Renderiza sem placeholder remanescente. |
| M2-R7 | Corte mínimo entra como **insumo** do red team em F4, com a ressalva anexa. | O texto do red team continua exigindo as nove respostas. |

---

## 5. Requisitos não funcionais

- **Determinismo total.** Sem rede, sem modelo de linguagem, sem heurística opaca no cálculo.
- **Retrocompatibilidade.** Todo campo novo é opcional, nos dois artefatos.
- **Imutabilidade do canônico.** Nem o grafo aprovado nem a proveniência são reescritos pelos módulos de leitura.
- **Auditabilidade.** Todo número decompõe até a aresta.
- **Nada disso entra na peça.** Estes números são instrumento de auditoria interna. Nenhum deles aparece no DOCX protocolável — é bloqueador (§10).
- **Custo.** [Inferência] Dezenas de nós por caso; o corte mínimo exaustivo é o mais caro e ainda assim roda em milissegundos. Não muda o tempo de ciclo de F7.

---

## 6. Parâmetros calibráveis

| Parâmetro | Valor inicial | Regra |
|---|---|---|
| `threshold_thesis_support_minimum` | a definir na calibração (§6.1) | piso absoluto 0,3 — abaixo disso a inferência declarada sozinha passaria |
| `threshold_exposure_concentration` | a definir na calibração (§6.1) | severidade sempre pela matriz de §3.5 |
| `threshold_thesis_orphan_gate` | P1 | sobe para bloqueante se a órfã por lapso de aresta deixar de ser a maioria dos casos |
| `days_until_stale` | 180 precedente, 90 ato regulamentar | gatilho de reconferência, nunca presunção de invalidade; regimento e lei compilada envelhecem por emenda, não por calendário |

### 6.1 Calibração pré-produção — bloqueia o gate, não o módulo

O achado 6 da revisão está certo: 0,4 e 0,7 eram chute apresentado como ponto de partida. A v2 não fixa esses dois valores. O procedimento:

1. Rodar M1 nos cinco `F3_REASONING_GRAPH.json` reais que existem no harness, incluindo os aprovados com revisor independente.
2. Levantar a distribuição real de lastro e de exposição por tese, com a fonte concentradora identificada em cada caso.
3. Escolher o limiar de modo que os casos hoje considerados bons **não** acendam P1 — o teste-âncora da casa: gate que reprova o que o dono aprovou está errado, não a peça.
4. Gravar a distribuição, o limiar escolhido e o motivo em artefato de calibração versionado, referenciado pela config.

Enquanto esse artefato não existir, o gate roda em **observação**: mede, relata no artefato interno, e não emite P1. O módulo pode ser implementado e usado antes; o que a calibração bloqueia é a severidade.

---

## 7. Fora de escopo — não reabrir sem fato novo

1. Substituir o pipeline F0–F10 por orquestração de grafo — rejeitado no plano 42; a sequência dos gates é decisão jurídica.
2. RAG e GraphRAG — rejeitados no plano 07.
3. LLM-as-judge como gate — rejeitado no plano 07. Vale também aqui: nenhum peso é atribuído por juízo de modelo.
4. Banco de grafo dedicado — rejeitado no plano 42.
5. RCT interno e visualização 3D — rejeitados nos planos 07 e 19.

---

## 8. Riscos

| Risco | Cenário | Mitigação |
|---|---|---|
| **Número sem regra é opinião com cara de medida** | 0,75 atribuído porque "parece forte"; o número ganha ar de rigor. | Tabela fechada com rejeição, não aviso. E nenhum destes números sai no protocolável. |
| **Falso positivo em peça bem construída** | A peça concentra em torno da decisão recorrida, como deve, e o gate grita. | Matriz de severidade de §3.5 e calibração de §6.1 contra os casos aprovados. |
| **O grafo vira o red team** | Alguém lê o corte mínimo e pula as nove perguntas. | Ressalva impressa na saída, no template e no insumo de F4; as nove perguntas continuam exigidas. |
| **Consultas viram código morto** | Módulos escritos, testes verdes, ninguém usa — o modo de falha que o plano 42 já registrou para gate em rota não percorrida. | M2 não é dado por concluído sem a seção no relatório e sem o insumo em F4. |
| **`supportIds` nunca é populado** | A propagação fica em cobertura parcial para sempre. | A cobertura parcial é declarada em número no relatório de cada caso. Lacuna visível pressiona; lacuna silenciosa acomoda. |
| **Independência presumida onde não há** | Duas fontes derivadas do mesmo ato inflam o lastro. | Fonte conta uma vez (§3.3); o relatório lista as redundâncias internas colapsadas. |

---

## 9. Aceitação

1. Schema estendido nos dois artefatos, com campos opcionais; validação existente continua verde.
2. Nenhum valor fora da tabela de §3.2 é aceito.
3. **Regressão-âncora com a fixture do CASO-04:**
   - `THESIS-FINE` detectada como órfã — nenhuma aresta sustentadora de entrada.
   - `SRC_A8` identificada como origem das quatro arestas `EDGE-A8-PARTIAL`, `EDGE-A8-1022`, `EDGE-A8-211`, `EDGE-A8-S7`.
   - Exposição de `THESIS-1022` = 1,0 — `EDGE-A8-1022` é a única de entrada. Idem `THESIS-211` e `THESIS-S7`.
   - Exposição de `THESIS-PARTIAL` < 1,0 — recebe `EDGE-A8-PARTIAL` e `EDGE-A9-PARTIAL`; a qualificadora `EDGE-ERESP-PARTIAL` **não** entra no lastro, e o teste verifica isso.
   - Severidade da exposição de `THESIS-1022` é P2 e não P1, porque `SRC_A8` é documento dos autos com `strength` 1,0 — o teste que impede o falso positivo do achado 8.
4. Teste de regressão da agregação: uma fonte de 1,0 produz lastro maior que cinco fontes de 0,2.
5. Teste de que o grafo de entrada não é mutado.
6. Teste de cobertura parcial declarada quando `supportIds` está ausente.
7. Artefato de calibração de §6.1 existente antes de o gate emitir P1.
8. Suíte nova verde e na baseline.

---

## 10. Bloqueadores

- Default aplicado sem ser impresso no relatório.
- Valor fora da tabela chegando à produção.
- Medida derivada gravada no artefato canônico ou editada à mão.
- Corte mínimo publicado sem a ressalva de §4.2.
- Propagação declarando cobertura total quando `supportIds` está ausente.
- Gate emitindo P1 antes da calibração de §6.1.
- Qualquer um destes números aparecendo no DOCX protocolável.

---

## 11. Faseamento — esforço reestimado

A v1 estimava só o código dos módulos. A revisão apontou que testes, template e integração ficavam fora e seriam os primeiros a cair sob pressão (achado 9). Os números abaixo são de entrega **pronta para produção**, incluindo teste, integração e lição registrada. Todos são [Inferência].

| Movimento | Esforço | Bloqueador | Inclui |
|---|---|---|---|
| M1 — ponderar | 4–6h | nenhum | módulo, schema, gate em observação, regressão CASO-04, lição em `RETROSPECTIVAS.md` |
| M1-cal — calibração | 1–2h | M1 | rodar nos cinco grafos reais, artefato de calibração, definir os dois limiares, ligar a severidade |
| M2 — consultar | 3–5h | M1 | módulo, contrato `supportIds`, template do relatório, insumo em F4, testes |
| M3 — grafo de atos | 4–6h | definir schema de ato e produtor em F3 | — |
| M4 — fila vira grafo | 3–4h | M1 | — |
| M5 — higienizar graphify | 2–3h | nenhum | — |

Ordem: M1 → M1-cal → M2. Depois, decisão sobre M3, M4 e M5 — que aqui seguem declarados como escopo, não especificados.

---

## 12. Validação continuada

- **Falso positivo** — o gate aponta e o auditor discorda: registrar em `APRENDIZADOS_FEEDBACK_HUMANO.md`; recalibrar se passar de um terço em vinte casos.
- **Falso negativo** — o auditor encontra exposição que o gate não pegou: vira regressão nova, com o caso como fixture.
- **Adoção** — se três peças seguidas saírem sem que ninguém leia a seção nova, o problema é de rota e não de cálculo; reabrir M2-R6 antes de seguir para M3.
- **Cobertura de `supportIds`** — acompanhar o percentual por caso; se não subir em cinco casos, a população não entrou na rotina de F6 e M2-R3 permanece decorativo.

---

## 13. Decisões sobre o parecer do revisor

Conforme o protocolo da casa, cada recomendação recebe decisão registrada. Conferi cada uma na fonte antes de decidir.

| # | Achado | Decisão | Motivo |
|---|---|---|---|
| 1 | Contrato com `paragraph_provenance` indefinido | **Acatado, e agravado** | Conferido na fonte: não é contrato mal definido, é ausência de chave — `provenance` é texto livre de ledgers. Resolvido em §4.3 com campo `supportIds` opcional e cobertura parcial declarada. |
| 2 | `_dependency_cycles` nunca roda no grafo real | **Acatado** | Confirmado por varredura: 49 arestas em cinco grafos, zero `depends_on`. O plano 42 foi corrigido e o PRD reescrito em §1.B. Achado mais valioso da revisão. |
| 3 | Soma não distingue robustez de fragilidade | **Acatado** | Substituída por OU ruidoso em §3.3, que resolve isto e o achado 10 juntos. A contraproposta do revisor (métrica extra de redundância) foi preterida: prefiro uma fórmula que já carregue a estrutura a duas métricas que o leitor precise combinar de cabeça. |
| 4 | Default de campo ausente não declarado | **Acatado em parte** | O default faltava mesmo, para os quatro campos — corrigido em §3.1, com defaults conservadores. A parte de que faltava `criticality` na tabela normativa está incorreta: ela já estava lá com três valores. |
| 5 | Corte mínimo não é o red team jurídico | **Acatado** | Ressalva obrigatória impressa na saída, no template e no insumo de F4 (§4.2). |
| 6 | Limiares eram chute | **Acatado** | Os dois valores foram retirados. §6.1 institui calibração pré-produção contra os casos aprovados, e o gate roda em observação até ela existir. |
| 7 | Discretização em cinco degraus não justificada | **Acatado** | Justificativa em §3.2. |
| 8 | Concentração pode ser boa arquitetura jurídica | **Acatado, e promovido a P1** | O revisor classificou como P2; é o achado de maior risco prático depois do 2, porque produziria falso positivo justamente nas peças bem feitas. Resolvido pela matriz de severidade de §3.5 e por um teste-âncora dedicado (§9.3, última asserção). |
| 9 | Esforço subestimado | **Acatado** | §11 reestimado para entrega pronta para produção. |
| 10 | Lastro cresce sem limite acima de 1,0 | **Acatado** | Resolvido pelo OU ruidoso, que é limitado por construção — melhor que o *clamp* proposto, que descartaria informação silenciosamente. |

Veredicto do revisor: prosseguir com as correções 1 a 6. Todas as dez foram tratadas.

---

## 14. Artefatos

**Código novo (PROPOSTO):** `forja_grafo_pesos.py`, `forja_grafo_consulta.py`, `test_forja_grafo_pesos.py`, `test_forja_grafo_consulta.py`.

**Alteração em artefato existente:** `n4_schemas\f3_reasoning_graph.schema.json` (quatro campos opcionais); schema da proveniência de parágrafo (`supportIds` opcional); validação de integridade referencial junto aos `N4-CROSS-*`; ponto de integração do gate em F7; seção nova no relatório de melhorias; insumo do red team em F4.

**Documentação:** este PRD; artefato de calibração de §6.1; lição em `RETROSPECTIVAS.md` ao fim da implementação; fichas de decisão em `_FORJA_HARNESS\decisoes\` — pasta que ainda não existe e cuja criação é pré-requisito de §15.

---

## 15. Pendências antes de implementar

1. **Perna cruzada de família.** A revisão foi Fable→Opus, mesma família. A revisão por Codex/GPT sobre a fórmula de agregação de §3.3 e sobre a matriz de severidade de §3.5 continua em aberto.
2. **Fichas de decisão.** A pasta `_FORJA_HARNESS\decisoes\` não existe; a skill `forja-adr` prevê a migração das rejeições que hoje vivem em prosa. Três decisões deste PRD são candidatas a ficha: OU ruidoso em vez de soma; exposição concentrada não é defeito por si; gate em observação até calibrar.
3. **Quem popula `supportIds`** em F6 — decisão de rotina, não de código.
