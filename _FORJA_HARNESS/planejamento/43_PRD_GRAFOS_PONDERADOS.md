# PRD — Ponderação e inteligência dos grafos da fábrica

**Origem:** plano 42 (\_FORJA_HARNESS\planejamento\42_PLANO_GRAFOS_PONDERADOS.md\), 05/08/2026.
**Objetivo de negócio:** Extrair inteligência estruturada do grafo de raciocínio jurídico (\F3_REASONING_GRAPH.json\) — o artefato mais valioso da fábrica — transformando-o de desenho de relações em estrutura navegável que responda perguntas operacionais: onde está a fragilidade concentrada, qual a verdadeira cadeia de sustentação de cada pedido, e qual o custo real de cada fonte caísse.
**Métrica de sucesso:** Gates F7 automatizados com achados auditáveis (tese órfã, fragilidade concentrada, lastro insuficiente) e consultas que hoje exigem leitura manual — caminho crítico fonte→tese→pedido, corte mínimo, propagação de invalidação — gerando tabelas explicáveis no relatório de melhorias.

---

## 1. Problema

### A. O raciocínio jurídico é grafo mas não tem pesos
O \F3_REASONING_GRAPH.json\ estrutura nós (documentos, teses, pedidos) e arestas (supports, qualifies, justifies) com profundidade jurídica (scope, reason, reviewStatus). Mas nenhum número em lugar algum: não sabe força da fonte, não sabe se a tese cai se a aresta cair, não sabe risco de perder aquele precedente específico, não sabe idade da conferência.

Resultado: o grafo é auditável por humano e criado com cuidado, mas ninguém o percorre. A única travessia que existe em todo o harness é \_dependency_cycles\ em \orja_reasoning.py:155\ — detector de ciclo. Fora isso, as arestas são validadas quanto a endpoint e relação, e nunca consultadas.

### B. Diagnóstico na fábrica real: grafo do CASO-04
O caso real do CASO-04 (21 nós, 13 arestas, status \pproved\) revela dois achados não-óbvios que o grafo contém e ninguém extraiu:

1. **SRC_A8 (Nova Decisão de 28/04/2026) sustenta sozinho 4 das 5 teses** — arestas EDGE-A8-PARTIAL, EDGE-A8-1022, EDGE-A8-211, EDGE-A8-S7. É fragilidade concentrada: se aquela decisão cair ou for descoberta stale, a impugnação perde quatro pilares de uma vez.
2. **THESIS-FINE tem grau de entrada zero** — tese sem nenhuma aresta de entrada (source), só sai dela a aresta para REQUEST-FINE. Ou falta a aresta, ou falta a fonte. Em ambos os casos é achado de auditoria que passou pelo revisor independente sem ser percebido.

### C. Quatro defeitos transversais
1. Peso está onde não decide (fila tem score, não tem aresta) e falta onde decide (raciocínio tem aresta, não tem score).
2. Grafo que ninguém percorre é desenho.
3. Uma dimensão por grafo — o reasoning graph só sabe "confirmado / não confirmado".
4. Nada envelhece — regimento de 06/07 pesa igual a um conferido hoje.

---

## 2. Solução em uma frase

Um motor determinístico (\orja_grafo_pesos.py\ para M1; \orja_grafo_consulta.py\ para M2) que pondera arestas do \F3_REASONING_GRAPH\ com tabela normativa declarada (força da fonte, necessidade para a tese, data de conferência), calcula três métricas derivadas automaticamente (lastro da tese, fragilidade concentrada, tese órfã), e expõe três consultas auditáveis (caminho crítico, corte mínimo, propagação de invalidação) — alimentando gates F7 automáticos e red team estruturado.

---

## 3. Requisitos funcionais — M1 (Ponderar o grafo)

| ID | Requisito | Critério de aceite |
|---|---|---|
| M1-R1 | Adicionar campos opcionais ao schema \F3_REASONING_GRAPH\ sem quebra retrocompatível: \strength\ (0–1) e \
ecessity\ (0–1) e \erifiedAt\ (data ISO) na aresta; \criticality\ (0–1) no nó (tese). Ausência de campo = default declarado explicitamente no relatório, nunca default silencioso (no \orja_grafo_pesos.py\ ou no F7) | Schema estendido; validação OK com nós/arestas ausentes de campos; teste de leitura de grafo antigo sem campos retorna defaults nomeados |
| M1-R2 | Tabela normativa de atribuição **declarada e imutável** para \strength\ (documento oficial 1.0, ato oficial externo conferido 0.9, precedente inteiro teor 0.8, doutrina 0.5, inferência 0.3) e \
ecessity\ (tese cai 1.0, enfraquece 0.5, redundante 0.2) e \criticality\ (pedido decisivo 1.0, subsidiário 0.5, acessório 0.2). Nenhum valor fora desta tabela aceito. | Função \orja_grafo_pesos.py:atribuicao_strength()\ etc. com teste de cada valor; rejeição de valor fora da tabela com mensagem clara |
| M1-R3 | Computar três métricas derivadas **nunca editadas à mão** (sempre recalculadas): **lastro da tese** = Σ(\strength\ × \
ecessity\) das arestas de entrada da tese; **fragilidade concentrada** = fracção máxima do lastro que vem de uma única fonte; **tese órfã** = grau de entrada zero (binário). Armazenar em relatório de melhorias, nunca no artefato canônico (o grafo fica immutável). | Função \orja_grafo_pesos.py:calcular_metricas()\ com entrada: grafo + pesos das arestas/nós; saída: relatório JSON com as três métricas por tese; teste com o CASO-04 confirma SRC_A8 com fragilidade >= 50% e THESIS-FINE com grau zero |
| M1-R4 | Gate em F7: **tese órfã** (grau entrada = 0) → achado bloqueante ou P1 conforme calibração (PARÂMETRO_LIMIAR_ORFAO); **tese sustentando pedido decisivo com lastro abaixo do limiar** (valor proposto: 0,4 = mínimo da tabela) → P1; **fragilidade concentrada acima do limiar** (valor proposto: 0,7 = 70% do lastro de uma tese vindo de uma fonte) → P1, com listagem das teses frágeis. Limiares são PARÂMETROS_CALIBRÁVEIS, não números mágicos — arquivo \orja_n3_config.json\ com chave \	hreshold_thesis_support_minimum\ etc. | Arquivo \orja_n3_config.json\ carregado no F7 (\orja_verificador.py\ ou módulo de gates F7 novo); gates emitidos com descrição do parâmetro e o valor vigente; teste: CASO-04 com limiar padrão emite P1 por THESIS-FINE órfã e P1 por SRC_A8 concentrado |
| M1-R5 | Entregável \orja_grafo_pesos.py\ (função principal \ponderar_grafo(payload_graph: dict, defaults_path: str | None) -> dict\) — lê grafo; aplica tabela normativa com defaults declarados; retorna novo payload com campos opcionais preenchidos e relatório de métricas em chave nova \derivedMetrics\ (não toca no grafo original). Nunca emite opinião — cada valor tem regra nomeada. | Função pura, testável; grafo original preservado (cópia modificada); relatório decompõe cada métrica com o valor de cada aresta que a compõe |
| M1-R6 | Testes de regressão com o grafo real do CASO-04: fixture \F3_REASONING_GRAPH.json\; asserções: (a) \lastro(THESIS-PARTIAL)\ > 0, porque SRC_A8 + SRC_A9 sustentam; (b) \lastro(THESIS-FINE)\ = 0 porque grau entrada = 0 (nó órfão); (c) \ragilidade(THESIS-1022)\ >= 50% porque SRC_A8 é única fonte com força 1.0; (d) \ragilidade(THESIS-PARTIAL)\ < 50% porque há cobertura plural (SRC_A8, SRC_A9, SRC_ERESP). | Arquivo \	est_forja_grafo_pesos.py\ com fixture carregada, os 4 testes acima, ambos passando; regressão incluída em suite geral (\pytest test_forja_*.py\) |

---

## 4. Requisitos funcionais — M2 (Consultas no grafo)

| ID | Requisito | Critério de aceite |
|---|---|---|
| M2-R1 | **Consulta 1 — Caminho crítico fonte→tese→pedido.** Dado o grafo ponderado, ordenar as fontes (nós de tipo \document\) por quanto do pedido cai se cada fonte cair. Saída: lista \[{source, thesis[], request[], impact_score}]\ ordenada por \impact_score\ desc. \impact_score\ = Σ(\criticality\ da tese × \lastro\ da tese que vem daquela fonte / lastro total da tese). Traduz em linguagem operacional: "SRC_A8 sustenta 60% da sua força em REQUEST-DENY porque as teses que a usar têm criticidade alta". | Função \orja_grafo_consulta.py:caminho_critico()\ com entrada (grafo ponderado, request_id); saída: JSON com ranking de fontes + impacto; teste CASO-04: SRC_A8 aparece no topo para REQUEST-DENY com impact_score > 0.5 |
| M2-R2 | **Consulta 2 — Corte mínimo (minimum cut).** Dado o grafo, encontrar o menor conjunto de fontes que a parte adversária precisa derrubar para que nenhum pedido alcance força suficiente. Saída: \{min_cut: [source_ids], size: N, coverage: {request_id: True/False}}\. Alimenta diretamente o red team estruturado de 9 perguntas (hoje manual, será integrado em F4). | Função \orja_grafo_consulta.py:corte_minimo()\ (entrada: grafo ponderado, threshold de força mínima = 0.4 default); saída: JSON com o corte mínimo explicitado e cobertura de cada pedido; teste: CASO-04 com limiar 0.4 retorna corte mínimo e a ordem explica onde seca cada pedido se o corte é aplicado |
| M2-R3 | **Consulta 3 — Propagação de invalidação.** Marcar uma fonte como \stale\ (verifiedAt passou de N dias, padrão 180); propagação automática: tese que dependia só dessa fonte fica sem lastro (lastro cai para 0); parágrafo que justifica só com essa tese fica órfão. Ligar \F3_REASONING_GRAPH\ ao \paragraph_provenance.json\ que já existe (hoje os dois são ilhas). Saída: \{source_id: "SRC_A8", marked_stale: True, affected_theses: [id: "THESIS-211", new_support: 0.0], affected_paragraphs: [id: "PARA_015", new_provenance_status: "orphaned"]}\. | Função \orja_grafo_consulta.py:propagar_invalidacao()\ (entrada: grafo ponderado + paragraph_provenance.json + dias_limite); saída: JSON com cascata de invalidação; teste: CASO-04 com SRC_A8 marcado stale emite THESIS-1022 órfã, que orphana os parágrafos 3-5 que a usam como única justificativa |
| M2-R4 | Entregável \orja_grafo_consulta.py\ com as três funções (caminho_crítico, corte_mínimo, propagação_invalidação) e função \xecutar_consultas(graph_id: str, query_list: list[str]) -> dict\ que roda zero, uma ou as três consultas conforme pedido. | Módulo \orja_grafo_consulta.py\ com as três funções; função orquestradora que aceita \--caminho_critico\, \--corte_minimo\, \--propagar\ como flags; saída: JSON estruturado com as chaves acima |
| M2-R5 | Relatório de melhorias (\F7_RELATORIO_MELHORIAS.md\) inclui seção nova "Inteligência do Grafo de Raciocínio" com: (a) tabela "Caminho crítico" (fonte + teses sustentadas + impacto); (b) tabela "Corte mínimo" (fontes que a adversária deve derrubar); (c) lista de parágrafos órfãos se houver invalidação. Formatação de tabela legível, anti-placeholders. | Template novo em \_FORJA_HARNESS\templates\F7_RELATORIO_GRAFO_CONSULTAS.md\; \orja_render_docx.py\ integrado para montar a seção na versão final; teste: CASO-04 com consultas da M2 renderiza tabelas sem \[PLACEHOLDER]\ |

---

## 5. Requisitos não-funcionais

- **Determinismo total**: sem rede, sem LLM, sem heurística opaca. Tabela normativa é lei.
- **Retrocompatibilidade**: campos novos são opcionais; grafo antigo sem pesos lê sem erro, com defaults declarados.
- **Imutabilidade do canônico**: \F3_REASONING_GRAPH.json\ fica inalterado; métricas derivadas e pesos vivem no relatório F7, não no artefato.
- **Auditabilidade**: cada número vem de regra nomeada; relatório decompõe a origem de cada valor.

---

## 6. Parâmetros calibráveis (nunca números mágicos)

| Parâmetro | Escala | Valor proposto | Ajuste futuro | Onde |
|---|---|---|---|---|
| \	hreshold_thesis_support_minimum\ | 0–1 | 0,4 | Calibração após 2 semanas com material real; rejeitar valor < 0,3 (mínimo absoluto pela tabela) | \orja_n3_config.json\ |
| \	hreshold_fragility_concentration\ | 0–1 | 0,7 | Calibração; 0,7 = "esta fonte é 70% da força"; após 2 semanas avaliar se sobe para 0,75 | \orja_n3_config.json\ |
| \	hreshold_thesis_orphan_gate\ | "P1" ou "bloqueante" | "P1" | Sem mudança prevista antes do ciclo AR; se > 5 teses órfãs por caso, reavaliar para bloqueante | \orja_n3_config.json\ |
| \days_until_stale\ (M2-R3) | dias | 180 | Calibração com jurisprudência real; regimento de STJ não muda com idade mas precedente muda; sugestão: 180 para precedente, 90 para regulação | \orja_n3_config.json\ |

---

## 7. Fora de escopo (anti-requisitos — não reabrir sem fato novo)

1. **Não trocar o pipeline F0–F10 por "orquestrador de grafo"** (rejeitado no plano 42; gates sequenciais têm razão jurídica, não técnica).
2. **Não reabrir RAG / GraphRAG** (rejeitado no plano 07; M1/M2 é sobre ponderar grafos pequenos e auditáveis, não recuperação semântica).
3. **Não adotar banco de grafo** (rejeitado no plano 42; JSON + travessia em memória mantém tudo diffável e hashável como o resto do harness).
4. **Peso inventado por modelo não entra em produção** (Diretriz 08/07/2026 inviolável: "Peso sem tabela normativa é opinião com cara de medida — e em peça protocolável, medida falsa vira alegação falsa"). M1 só trabalha com tabela declarada; LLM em futuro é problema de AR.

---

## 8. Riscos e mitigações

| Risco | Cenário | Mitigação |
|---|---|---|
| **Número sem regra = fraude** | Agente calcula \strength\ por livre juízo, gera 0,75 porque "parece forte", entra na peça como "prova". Julgador vê número e pressupõe métrica rigorosa. Sentença reverte porque o número era opinião. | **Tabela normativa é bloqueador de entrada**: qualquer valor fora da tabela (1.0, 0.9, 0.8, 0.5, 0.3 para strength; 1.0, 0.5, 0.2 para necessity; 1.0, 0.5, 0.2 para criticality) é rejeição P0 no gate. Teste: \	est_forja_grafo_pesos.py:test_rejeita_valor_fora_tabela()\ |
| **Métrica derivada calculada errado** | \lastro()\ soma sem considerar \
ecessity\, tese fica com força 1.0 quando deveria ser 0.4. Gate cai e achado falso não sai. | Fórmula é função pura em testes; fixture CASO-04 é canária — mesmos valores desde 15/07. Regressão obrigatória em toda mudança de \orja_grafo_pesos.py\. Código revisado manualmente antes de M1 fechar. |
| **Calibração de limiar deixa tese importante despercebida** | Limiar de fragilidade em 0,7; uma tese com 65% concentrado não sai. Auditor perdeu. | Parâmetro é \	hreshold_fragility_concentration\, não número mágico. Arquivo de config tem histórico (git versionado). Após 2 semanas de uso real com ≥ 5 casos, reunião de calibração registrada. Se critério mudar, PR explica. |
| **Consultas M2 ficam listas como código morto** | Funções escritas, tests passam, ninguém usa. Grafo continua desenho. | **Integração em F7 + red team estruturado**: corte mínimo alimenta diretamente as 9 perguntas (hoje em prompt; amanhã será lista gerada); relatório de melhorias sempre inclui seção "Inteligência do Grafo" (R2-R5). Métrica de sucesso: ≥ 3 peças por mês usam as três consultas. |
| **Schema estendido quebra consumer antigo** | Novo campo \strength\ é adicionado; código antigo que espera schema v1 fecha com erro. | Campos são opcionais (allOf no schema); valor ausente = default declarado, nunca silencioso (mensagem explícita no relatório). Teste: \	est_forja_grafo_pesos.py:test_compatibilidade_retroativa()\ com grafo antigo sem campos. |

---

## 9. Critérios de aceitação

1. Schema \F3_REASONING_GRAPH\ estendido com campos opcionais e validação backward-compatible; \	est_forja_n4_common.py\ passa.
2. \orja_grafo_pesos.py\ implementado e testado: função \ponderar_grafo()\ com entrada e saída JSON; nenhum valor fora da tabela normativa aceito.
3. Testes de regressão com fixture CASO-04:
   - THESIS-FINE tem grau de entrada = 0 (nó órfão detectado).
   - SRC_A8 aparece como elo crítico em 4 teses (THESIS-PARTIAL, THESIS-1022, THESIS-211, THESIS-S7).
   - Fragilidade de THESIS-1022 >= 50% porque SRC_A8 é única fonte.
   - Fragilidade de THESIS-PARTIAL < 50% porque SRC_A8 + SRC_A9 dividem o peso.
4. Gate F7 implementado: tese órfã → P1; tese decisiva com lastro < 0,4 → P1; fragilidade > 0,7 → P1 com lista de teses frágeis.
5. \orja_grafo_consulta.py\ implementado com três funções (caminho_crítico, corte_mínimo, propagação_invalidação) e teste ponta a ponta com CASO-04.
6. Relatório de melhorias (F7) incluir seção "Inteligência do Grafo de Raciocínio" com tabelas explicáveis (sem \[PLACEHOLDER]\).
7. Arquivo \orja_n3_config.json\ com os quatro parâmetros calibráveis e valores propostos; mudança de valor propaga para gate F7.
8. Suite \	est_forja_grafo_*.py\ verde; regressão de CASO-04 incluída em ciclo CI/CD.

---

## 10. Critérios de NÃO-aceitação (bloqueadores)

- Qualquer valor de \strength\ / \
ecessity\ / \criticality\ fora da tabela normativa entra em produção.
- Métrica derivada (\lastro\, \ragilidade\, \orfao\) não recalculada automaticamente em toda alteração do grafo; ou editada à mão no artefato canônico.
- Gate F7 não emite achado P1 quando THESIS-FINE é órfã ou SRC_A8 concentra > 70% do lastro em THESIS-1022 (teste de regressão falha).
- Consultas M2 são funções sem integração em F7 / relatório de melhorias; ficam código morto.
- Parâmetro de limiar é número mágico no código, não em config externalizável.

---

## 11. Faseamento e dependências

### Ordem de execução

**M1 → M2 → (M3, M4, M5 em paralelo)**. M1 e M2 cabem numa sessão e é onde está quase todo o ganho jurídico.

| Movimento | Duração est. | Bloqueador | Saída |
|---|---|---|---|
| **M1** | 3–4h | Nenhum; schema já existe, entrada é grafo aprovado. | \orja_grafo_pesos.py\, schema estendido, testes regressão CASO-04, gate F7 pronto. |
| **M2** | 2–3h | M1 concluído (M2 usa o grafo ponderado de M1). | \orja_grafo_consulta.py\, três consultas funcionais, integração em F7 + relatório. |
| **M3** (Grafo de atos) | 4–6h | Protocolo de cronologia auditada (vigente desde 11/07); bloqueador: decisão sobre schema de ato/evento. | Schema novo \F3_ACT_GRAPH.schema.json\, produtor em F3, teste com CASO-04. |
| **M4** (Fila vira grafo) | 3–4h | M1 + M3 (modelo de aresta); bloqueador: desenho das arestas (bloqueia, mesma_fonte, aguarda). | \orja_fila_grafo.py\, arestas entre demandas, pergunta operacional "quantos casos em paralelo agora". |
| **M5** (Higienizar graphify) | 2–3h | Nenhum; grafo de código é grafo existente a melhorar. | Podar god node, separar comunidade 90001, usar confidence_score em centralidade. |

### Dependências de dados

- M1/M2 dependem de \F3_REASONING_GRAPH\ aprovado (já existe, CASO-04 confirmado).
- M2-R3 (propagação de invalidação) depende de \paragraph_provenance.json\ (já existe, 54 KB CASO-17, 42 KB Nylton).
- M3 bloqueado por: definição de schema de ato, responsável para produtor em F3.
- M4 bloqueado por M3 (modelo de aresta) + decisão sobre arestas de demanda.

### Faseamento no ciclo FORJA

- **M1** integra em **F7** (gates automáticos: tese órfã, fragilidade concentrada, lastro insuficiente).
- **M2** integra em **F7** (relatório de melhorias) + **F4** (red team estruturado — corte mínimo alimenta as 9 perguntas).
- **M3/M4/M5** são **fora do critério de sucesso imediato** (ganho jurídico está em M1/M2); comunicação de sequência antes de começar M3.

---

## 12. Métricas e validação

### Durante a implementação

- \	est_forja_grafo_pesos.py\: 4 asserções CASO-04 (nó órfão, fontes concentradas, plural coverage, impacto).
- \	est_forja_grafo_consulta.py\: 3 consultas executam sem erro; outputs com estrutura esperada.
- Gate F7 com 5+ casos reais: tese órfã ou fragilidade > limiar sai em relatório.

### Pós-implementação (M1/M2 encerrados)

- Tempo de ciclo F7: sem mudança perceptível (consultas em O(n²) em nós/arestas, N ≈ 20–50 por caso — milissegundos).
- Achados falsos positivos (gate emite P1 que auditor humano discorda): registrar em \APRENDIZADOS_FEEDBACK_HUMANO.md\, recalibrar limiar se > 30% false positive em 20 casos.
- Achados falsos negativos (auditor encontra fragilidade que gate perdeu): regressão nova em \	est_forja_grafo_*.py\.

---

## 13. Fora do escopo (futuro, não bloqueia M1/M2)

- **Ciclo AR** de calibração automática de limiares (será feito depois, em ciclo Auto-Research v2).
- **LLM em loop** para sugerir pesos (rejeitado inviolavelmente; peso sem regra não entra).
- **Grafo de processo** (M3) integrado com contratos / SLAs (futuro; M3 é escopo declarado, não prioritário).
- **Otimização de fila** por subgrafo (M4) com regressão de paralelo máximo (futuro; M4 é ganho de velocidade, não de risco jurídico).

---

## 14. Artefatos esperados

### Código novo

- \_FORJA_HARNESS/forja_grafo_pesos.py\ — função \ponderar_grafo()\, tabela normativa, derivação de métricas.
- \_FORJA_HARNESS/forja_grafo_consulta.py\ — três consultas (caminho crítico, corte mínimo, propagação).
- \_FORJA_HARNESS/test_forja_grafo_pesos.py\ — regressão CASO-04.
- \_FORJA_HARNESS/test_forja_grafo_consulta.py\ — testes das três consultas.

### Documentação

- Este PRD, seções 6 e 14 (parâmetros e artefatos).
- Template novo: \_FORJA_HARNESS\templates\F7_RELATORIO_GRAFO_CONSULTAS.md\.
- Atualização de \RETROSPECTIVAS.md\ com lições mineradas da implementação.

### Mudança em artefatos existentes

- \_FORJA_HARNESS\n4_schemas\f3_reasoning_graph.schema.json\ — adicionar \strength\, \
ecessity\, \erifiedAt\ (aresta); \criticality\ (nó).
- \orja_n3_config.json\ — quatro chaves novas com valores padrão.
- \orja_verificador.py\ ou novo módulo de gates F7 — integração dos gates automáticos.
- \orja_render_docx.py\ — integração do template de consultas no relatório F7.