# PRD — Grafo de raciocínio: completude antes de peso

> **SUBSTITUÍDO EM 05/08/2026** por `planejamento/45_PRD_INSTRUMENTACAO_FORJA.md`,
> que unifica este documento com o PRD 44 da mesma data. Permanece legível como
> anexo histórico: a medição da § 1, os critérios de E0 e o critério aritmético de
> reabertura da ponderação seguem valendo por incorporação, e não foram
> redigitados no 45.

**Versão:** v3 final, 05/08/2026. Substitui a v2 do mesmo dia, que propunha ponderação como primeiro movimento.
**Decisão e redação:** Efesto Tekhton (Claude Opus 5), a partir de três pareceres adversariais independentes produzidos em `gpt-5.6-luna` esforço máximo — Helena (estratégia), Efesto-Codex (engenharia), Diabob (autoengano) — e de medição direta sobre os seis grafos reais do harness.
**Modo:** arquitetura. A decisão material é de ordem de execução, e está registrada em §2.

---

## 1. Resultado da revisão: a v2 estava errada na ordem

A v2 propunha ponderar as arestas do `F3_REASONING_GRAPH` como primeiro movimento. Rodei a fórmula proposta contra todos os grafos reais antes de aprovar. O resultado reprova a proposta:

**Seis grafos, 49 arestas, 20 teses. Aplicando a fórmula da v2 com os defaults da v2: 12 teses saturam em lastro exatamente 1,000 e 8 dão exatamente 0,000. Nenhuma cai no meio.**

A métrica é binária na prática. Não tem poder de discriminação nenhum, e os oito zeros ainda provocam divisão por zero no cálculo de exposição. Um número que só assume dois valores, um dos quais quebra a fórmula seguinte, não é medida — é ruído com casas decimais.

A causa não é a fórmula. É o dado:

| Caso | Nós | Arestas | Teses | Teses sem aresta sustentadora |
|---|---:|---:|---:|---:|
| CASO-04 (reconstrução) | 39 | 17 | 5 | 3 |
| CASO-18 | 36 | 8 | 3 | 2 |
| CASO-04 (AgInt) — a fixture | 23 | 13 | 5 | 1 |
| CASO-19 | 7 | 3 | 1 | 0 |
| CASO-17 | 35 | 5 | 5 | 2 |
| CASO-16 | 7 | 3 | 1 | 0 |

**8 das 20 teses da fábrica inteira — 40% — não recebem uma única aresta `supports` ou `justifies`.** Conferi uma a uma: duas recebem apenas `qualifies`, que restringe e não sustenta; uma não tem aresta alguma, em nenhuma direção; as demais só têm aresta de saída. Nenhuma se sustenta por caminho alternativo.

E o CASO-17 tem 35 nós com 5 arestas: trinta fontes catalogadas e desconectadas. O grafo ali é uma lista de fontes com meia dúzia de ligações.

Há ainda um segundo achado que nenhum dos pareceres viu, porque exige comparar os grafos entre si: **não existe ontologia comum**. Um grafo usa `document`; outro usa `source` e `official_source`; outro usa `event`, `fact`, `rule`, `inference`, `gap`, `strategy`, `coverage`. O schema declara `additionalProperties: true` e nunca restringe `type`. Consulta que cruze casos é impossível hoje, e nenhum dos dois documentos anteriores notou.

**Conclusão de engenharia: os grafos não estão subponderados. Estão despovoados e sem vocabulário comum.** Pesar aresta que não existe é instalar velocímetro em quadro de bicicleta sem roda. A v2 teria produzido, com esforço real, um número igual a 1,000 em doze teses e indefinido em oito — e o relatório de melhorias exibiria isso como inteligência.

### 1.1 Correção de fato da v1 e da v2

Os dois documentos anteriores diziam "cinco grafos reais". São **seis** em `n4_artifacts`. Helena apontou a divergência de contagem no parecer dela; ela contou sete somando cópia de execução em `runs/`. O número canônico é seis, e as 49 arestas se distribuem 17 + 8 + 13 + 3 + 5 + 3.

---

## 2. Decisão

Inverto a ordem da v2 e reduzo o escopo.

**Autorizado agora: E0, e só E0.** Um lint estrutural de rastreabilidade, determinístico, sem peso, sem limiar e sem calibração. Ele mede se o grafo foi preenchido. Hoje ele acende em 40% das teses.

**Condicionado: E1**, a ontologia. Fixar o vocabulário de `type` no schema. Sem isso nenhuma consulta atravessa casos.

**Suspenso: E2**, a ponderação. Só volta à mesa quando E0 mostrar população suficiente para peso discriminar, e a decisão de reabrir exige a medição de §9.2, não uma reunião.

**Promovido: M3**, o grafo de atos processuais. Helena tem razão em §1 do parecer dela: o protocolo exige cronologia auditada e grafo dos atos em processo volumoso desde 11/07/2026, e isso está descumprido hoje. Cumprir obrigação vigente vem antes de criar capacidade nova. M3 sai deste PRD e vira plano próprio, com prioridade acima de E1 e E2.

### 2.1 Por que não simplesmente consertar a fórmula

Considerei e rejeitei. Trocar OU ruidoso por outra agregação — média, mínimo, soma normalizada — não resolve: com 40% das teses em grau de entrada zero e trinta fontes soltas num caso, qualquer agregação devolve o mesmo par de valores degenerados. O problema está a montante da matemática. Corrigir a fórmula agora seria tratar o sintoma que a medição mostrou e ignorar a causa que ela revelou.

### 2.2 Nome honesto do que se entrega

E0 **não é** detecção de vulnerabilidade jurídica. É lint de rastreabilidade: verifica se o raciocínio foi documentado de forma navegável, não se o raciocínio está certo. Diabob (§9) e Helena (§3) chegaram a isso por caminhos independentes, e estão certos. O relatório usa essa palavra e não outra. Se em algum momento alguém chamar a saída de E0 de "análise de risco da tese", é uso indevido e o documento diz isso.

---

## 3. E0 — Lint estrutural do grafo

### 3.1 O que mede

Tudo determinístico, sem parâmetro ajustável, sem juízo.

| Código | Verificação | Estado hoje |
|---|---|---|
| `GRAFO-01` | tese sem nenhuma aresta de entrada `supports` ou `justifies` | acende em 8 de 20 teses |
| `GRAFO-02` | nó de fonte com grau zero — catalogado e nunca ligado a nada | acende forte no CASO-17 (30 fontes, 5 arestas) |
| `GRAFO-03` | pedido sem nenhuma tese que o justifique | a medir |
| `GRAFO-04` | tese cuja única aresta de entrada é restritiva (`qualifies`, `limits`, `distinguishes`) — restringe algo que nada sustenta | acende em 2 teses |
| `GRAFO-05` | valor de `type` fora do vocabulário canônico de E1 | inativo até E1 existir |
| `GRAFO-06` | densidade: arestas por nó não isolado, com o número no relatório | informativo |

`GRAFO-01` a `GRAFO-04` são achados. `GRAFO-05` e `GRAFO-06` são informativos.

### 3.2 Severidade — sem limiar, sem calibração

Não há número a calibrar porque não há escala: as verificações são binárias. A severidade é fixa e derivada da consequência, não de tolerância estatística:

- **`GRAFO-01` e `GRAFO-03` em tese ou pedido que a peça efetivamente usa: P1.** A peça afirma algo cuja sustentação não está registrada em lugar nenhum. Isso é falha de rastreabilidade, e o auditor humano precisa saber antes do protocolo.
- **`GRAFO-01` em tese que a peça abandonou: P2.** Resíduo de blueprint, não defeito.
- **`GRAFO-02` e `GRAFO-04`: P2.** Sinalizam grafo incompleto, não afirmação sem lastro.

Distinguir "tese que a peça usa" de "tese abandonada" exige saber o que a peça usa. Enquanto o elo com o texto não existir (§5), **todo `GRAFO-01` sai como P2 e o relatório declara que a distinção não foi feita**. Declarar a limitação é obrigatório; presumir P2 em silêncio é bloqueador.

### 3.3 O que E0 explicitamente não faz

- Não atribui peso, força ou confiança a nada.
- Não diz que uma tese é fraca. Diz que a sustentação dela não está registrada.
- Não bloqueia entrega. Emite achado no formato que o F7 já usa.

---

## 4. E1 — Ontologia (condicionado)

Fixar no schema o conjunto fechado de `type` de nó. Hoje o campo é livre e os seis grafos usam três vocabulários diferentes.

Proposta de vocabulário, a partir do que os grafos reais já usam: `document`, `official_source`, `fact`, `event`, `rule`, `thesis`, `request`, `decision`, `inference`, `gap`. Os valores `source`, `official_fact`, `strategy`, `coverage` e `calculation`, hoje em uso, precisam ser mapeados ou justificados — não elimino nenhum por decreto sem olhar o caso que o usa.

Migração: os grafos existentes são artefatos aprovados e não se reescrevem. O schema aceita o vocabulário antigo com aviso, e `GRAFO-05` reporta a divergência sem reprovar.

---

## 5. O elo com o texto — reclassificado

A v2 propunha `supportIds` no `paragraph_provenance.json` para ligar parágrafo a nó do grafo. Helena (§4) e Diabob (§6) atacaram por lados diferentes e ambos acertaram: a fixture tem 187 parágrafos, nenhum com o campo, e cobertura parcial declarada não é ponte, é lacuna com etiqueta.

**Decisão: o elo continua necessário e sai do escopo de código.** Ele é decisão de rotina de F6 — quem preenche, quando, com que cobertura mínima. Construir a propagação de invalidação antes de existir um único caso com o campo populado é escrever código sobre lacuna conhecida, que é o modo de falha que a casa já registrou como gate em rota não percorrida.

Pré-requisito para reabrir: **um caso real com `supportIds` populado por inteiro**. Com um caso, mede-se o custo de preencher e decide-se com dado. Sem ele, não.

---

## 6. Riscos

| Risco | Mitigação |
|---|---|
| E0 acende em 40% das teses e vira ruído que todos ignoram | O primeiro relatório é lido com o Igor antes de E0 entrar em rotina. Se 40% for o estado real e aceito, o achado é a informação — e a decisão passa a ser sobre preencher os grafos, não sobre o gate. |
| Tratarem lint de rastreabilidade como aval jurídico | O nome está em §2.2 e a saída repete a ressalva. É bloqueador em §8. |
| E0 pressionar por grafo mais denso em vez de raciocínio melhor — o "aprender a produzir grafos densos" de Diabob §9 | E0 não pontua densidade como qualidade; `GRAFO-06` é informativo e não entra em severidade. Nenhuma métrica de E0 melhora ao se acrescentar aresta sem conteúdo. |
| A ordem invertida ser lida como abandono do plano 42 | Não é. O plano 42 continua correto no diagnóstico — grafo que ninguém percorre é desenho. Errou no primeiro passo, e a medição de §1 é o fato novo que corrige. |

---

## 7. Aceitação

1. `GRAFO-01` a `GRAFO-04` implementados, determinísticos, sem parâmetro ajustável.
2. **Cada verificação tem um teste que falha antes e passa depois**, com caso real como fixture — a exigência de Diabob §10, acatada. Ressalva escrita não conta como correção.
3. Regressão nomeada, com os números desta medição como valor esperado: 8 teses em `GRAFO-01`, 2 em `GRAFO-04`, distribuídas pelos seis casos.
4. Contraprova: um grafo sintético completo e bem formado passa sem nenhum achado. Gate que só sabe acender não foi testado.
5. Achado no formato que o F7 já emite, sem mudança na estrutura de saída.
6. Relatório declara a limitação de §3.2 enquanto o elo com o texto não existir.
7. Nenhum número de E0 no DOCX protocolável.

---

## 8. Bloqueadores

- Peso, escala ou confiança em qualquer saída de E0.
- Saída de E0 apresentada como avaliação da qualidade jurídica da tese.
- `GRAFO-01` emitido como P2 sem a limitação declarada.
- Verificação sem o par de testes de §7.2.
- Implementar E2 antes da medição de §9.2.
- Implementar a propagação antes de um caso com `supportIds` completo.

---

## 9. Reabertura de E2 — critério objetivo

### 9.1 Por que travado

Com a distribuição atual, peso não discrimina. Isso é medição, não opinião, e está em §1.

### 9.2 O que destrava

Rodar de novo a medição de §1 e obter, sobre os grafos vigentes:

- teses com grau de entrada sustentador zero abaixo de 10% (hoje 40%);
- e mediana de arestas sustentadoras por tese igual ou maior que 3 (hoje a moda é 1).

Abaixo disso qualquer agregação continua degenerada, e o motivo é aritmético.

Quando destravar, três coisas ficam decididas desde já contra a v2:

1. **Ausência de dado nunca produz sustentação.** O default `strength` 0,3 combinado com `necessity` 1,0 fazia três arestas vazias renderem lastro 0,657 — Diabob §4, conferido e correto. Campo ausente exclui a aresta do cálculo e a conta em separado como não ponderada.
2. **Não há salvo-conduto para documento dos autos.** A v2 rebaixava a P2 a concentração ancorada em peça dos autos, tratando existência processual como suficiência. Os autos contêm alegação da parte contrária, decisão superada e fato controvertido. Diabob §5, acatado integralmente.
3. **`strength` se prende a artefato verificável, não a declaração.** "Precedente com inteiro teor lido" não é aferível; "precedente presente em `cache/fontes_oficiais/` com data de conferência" é. Diabob §3, acatado — e é a mesma lógica que a casa já usa para citação.

---

## 10. Esforço

[Inferência] E0: 3 a 5 horas, incluindo os testes de §7 e a integração no F7. E1: 2 a 3 horas, mais o levantamento dos `type` divergentes. E2: não estimo o que está suspenso.

A v2 estimava 8 a 13 horas para M1, calibração e M2. O escopo autorizado agora custa menos da metade e entrega a única coisa que a medição mostrou ser real.

---

## 11. Decisões sobre os três pareceres

Conferi cada achado na fonte antes de decidir. Onde a conferência mudou o achado, está dito.

### Helena — estratégia

| # | Achado | Decisão |
|---|---|---|
| 1 | M3 é obrigação vigente e foi postergado | **Acatado.** M3 promovido acima de E1 e E2, e sai para plano próprio (§2). |
| 2 | Score converte ordinal em aparência probabilística; fixture não tem os campos novos; contagem de grafos divergente | **Acatado.** A medição de §1 confirmou de forma mais dura do que ela previu. Contagem corrigida em §1.1: são seis, não cinco. |
| 3 | Pode estar medindo qualidade da documentação, não do raciocínio | **Acatado.** Vira o nome do produto em §2.2. |
| 4 | `supportIds` sem rotina assegurada | **Acatado.** §5: sai do escopo de código, pré-requisito de um caso populado. |
| 5 | Custo de oportunidade; autorizar só piloto com critério de saída | **Acatado em parte.** O escopo caiu para menos da metade, o que atende a preocupação. Não instituí critério formal de piloto porque E0 não tem limiar a validar: ou ele acende nas 8 teses que já sei que estão órfãs, ou está quebrado. |

### Efesto-Codex — engenharia

**O parecer não vale como revisão de engenharia.** O executor negou acesso ao repositório (`CreateProcessAsUserW: acesso negado`) e ele reportou bloqueio em vez de inventar achados — o que é a conduta correta e está registrado a favor dele. Um único achado sobreviveu, porque foi derivado da fórmula transcrita no briefing e não do código:

| # | Achado | Decisão |
|---|---|---|
| 2 | Contribuição 1,0 satura o lastro; exposição indefinida quando lastro = 0 | **Acatado e confirmado por medição.** Foi o que me levou a rodar §1, e a medição mostrou que não é caso de borda: é o comportamento em 20 de 20 teses. Achado decisivo desta rodada, vindo do parecer mais fraco. |

Pendência: a perna de engenharia sobre código real continua **não executada**. O acesso do Codex ao workspace precisa ser resolvido antes de E0 ir para produção, porque a revisão cruzada de família sobre a implementação ainda não aconteceu.

### Diabob — autoengano

Também sem acesso a arquivo; trabalhou sobre os fatos do briefing. Como a missão dele era atacar o desenho, e o desenho estava descrito por inteiro, os achados sobre desenho valem. Descartei o que dependia de leitura de código.

| # | Achado | Decisão |
|---|---|---|
| 2 | Fixture escolhida e avaliada pelo mesmo circuito; n=1 vendido como padrão | **Acatado, e ele subestimou.** A medição mostrou que o padrão real é pior e diferente do que a fixture sugeria: não é uma tese órfã anômala, são 40% delas. |
| 3 | `strength` 0,8 sem testemunho de leitura | **Acatado.** §9.2, item 3. |
| 4 | Defaults transformam ausência em sustentação | **Acatado.** Conferido: três arestas vazias davam 0,657. §9.2, item 1. |
| 5 | Salvo-conduto para documento dos autos confunde existência com suficiência | **Acatado integralmente.** §9.2, item 2. Corrige inclusive uma decisão que eu havia tomado na v2 em resposta a outro revisor. |
| 6 | `supportIds` parcial deixa texto fora da inspeção | **Acatado.** §5. |
| 7 | "Ausência de ciclos" é ausência de dado | **Acatado.** Já corrigido no plano 42. |
| 8 | Gate em observação sem prazo é telemetria | **Acatado por eliminação:** E0 não tem modo observação. Não há limiar a calibrar, então não há desculpa para não ligar. |
| 9 | Mede o que é fácil contar, não o que decide recurso | **Acatado.** §2.2. |
| 10 | Ressalva escrita não é correção testada | **Acatado.** Virou critério de aceitação §7.2, incluindo a contraprova de §7.4. |
| 11 | Origem em vídeo é estética, não evidência | **Acatado em parte.** Retirei a ambição; mantive o diagnóstico, que se sustenta em medição e não na origem. A pergunta de onde veio a ideia não decide se ela é verdadeira — o dado decide, e aqui o dado reprovou a versão entusiasmada. |
| 12 | Matar a v2 | **Acatado quanto à v2.** A v2 está morta: sua premissa foi reprovada por medição. Não acatado quanto a parar tudo: E0 não depende de nenhuma das hipóteses que ele derrubou, não produz número, não tem limiar e responde uma pergunta factual — o grafo foi preenchido? A resposta hoje é não em 40% dos casos, e isso é informação que a casa não tem. |

### Nota de circularidade

Eu sou Efesto e julguei o parecer do Efesto-Codex. Registro para que se olhe com atenção: o único achado que aproveitei dele é também o que mais reforçou a minha conclusão. Mitigação real: não o aceitei por concordância, rodei a medição de §1 e ela é reproduzível pelo script em §12.

---

## 12. Reprodução da medição

A medição de §1 foi feita sobre `state/*/n4_artifacts/F3_REASONING_GRAPH.json`, aplicando a fórmula da v2 com os defaults da v2, contando por tese as arestas de entrada `supports` e `justifies`. Ela deve virar o primeiro teste de E0, com os números desta data como baseline — se a distribuição mudar, é porque os grafos começaram a ser preenchidos, e aí §9.2 é consultada.

---

## 13. Pendências

1. **Revisão de engenharia sobre código real não aconteceu.** O Codex não conseguiu ler o workspace nesta rodada. Resolver o acesso antes de E0 entrar em produção.
2. **M3 precisa de plano próprio**, com prioridade acima de E1 e E2.
3. **Fichas de decisão.** `_FORJA_HARNESS\decisoes\` ainda não existe. Três decisões desta v3 são candidatas: completude antes de peso; E2 suspenso com critério aritmético de reabertura; ausência de dado nunca produz sustentação.
4. **Um caso com `supportIds` populado**, para decidir a propagação com dado de custo real.
