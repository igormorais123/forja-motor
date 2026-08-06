# 42 — Plano de ponderação e inteligência dos grafos da fábrica

Data: 05/08/2026
Origem: vídeo "Larguei tudo pra aprender Graph Engineering" (Lucas Montano, 31/07/2026, 15min) + auditoria dos grafos existentes no repositório nesta data.
Status: plano. Nada implementado ainda.

---

## 1. O que o vídeo entrega, destilado

O vídeo é majoritariamente didático (o que é nó, o que é aresta). Três ideias dele são aproveitáveis aqui, e só três:

1. **A aresta carrega peso, e o peso é a informação.** O exemplo é doméstico — acordar → levantar = 2 minutos — mas a tese é a certa: sem número na aresta você tem um desenho de relações, não uma estrutura sobre a qual se busca ou se otimiza.
2. **"Uma métrica nunca é suficiente."** É o ponto central. Um agente em loop otimizando custo de aquisição baixa o CAC e aumenta o churn sem perceber, porque só enxerga uma aresta. Grafo existe para representar como uma métrica afeta a outra.
3. **O exemplo do gerente de projetos.** Epic → story → task → subtask *não é árvore*, porque há dependências cruzadas. E é exatamente a dependência que responde a pergunta operacional real: quantos recursos podem trabalhar em paralelo agora, e o que destrava o quê.

O que o vídeo **não** entrega: nenhuma receita de engenharia, nenhum esquema, nenhum algoritmo. O autor inclusive conclui que não valia parar tudo para estudar "graph engineering". Portanto este plano usa o vídeo como provocação, não como especificação.

---

## 2. Inventário dos grafos existentes e diagnóstico de cada um

### A. `graphify-out/graph.json` — grafo de código do Motor
3.156 nós, 9.136 arestas, 111 comunidades (relatório de 05/08/2026, commit `3866e1c1`).

É o único grafo da casa que **tem um número na aresta**: `confidence_score` (1.0 para `EXTRACTED`, ~0.92 para os 103 `INFERRED`). Mas é peso de *procedência da aresta*, não de importância do que ela liga. Três defeitos concretos:

- **God node.** `FORJA Harness` tem 2.019 das 9.136 arestas. Qualquer centralidade calculada sobre este grafo mede a distância até esse nó e mais nada.
- **Comunidade que não é comunidade.** A 90001 ("Interfaces inferiores v3") tem 1.647 nós e coesão **0,00**. Não é um agrupamento, é o resto.
- Ninguém consome. É gerado, lido por humano, e fim.

### B. `F3_REASONING_GRAPH.json` — grafo de raciocínio jurídico, um por caso
**É o grafo mais valioso da fábrica e o menos ponderado.** Nós: `document`, `thesis`, `request`, `decision`. Arestas: `relation` (supports / qualifies / justifies), `scope` (full / partial), `reason`, `reviewStatus`. **Nenhum número em lugar algum.**

A auditoria do grafo real do CASO-04 (`forja_acervo.caso("CASO-04")`, 21 nós, 13 arestas, status `approved`, com reviewer independente) produziu dois achados que o grafo já contém e que ninguém extraiu:

- **`SRC_A8` (Nova Decisão de 28/04/2026) sustenta sozinho 4 das 5 teses** — PARTIAL, 1022, 211 e S7. É fragilidade concentrada: derrubada aquela peça, a impugnação perde quatro pilares de uma vez. O grafo sabe disso desde 15/07 e nunca contou a ninguém.
- **`THESIS-FINE` não tem nenhuma aresta de entrada.** É uma tese sem lastro documental declarado no grafo — só sai dela a aresta para `REQUEST-FINE`. Ou falta a aresta, ou falta a fonte. Em ambos os casos é achado de auditoria, e passou pelo revisor independente.

Quanto ao consumo: verifiquei todos os leitores (`forja_n4_validate`, `forja_reasoning`, `forja_pso_pet`, `forja_run_metrics`, `forja_n4_invalidation`). Eles leem o **conjunto de ids dos nós** para checar se um `supportId` de outro artefato existe. Fora isso, as arestas são validadas quanto a endpoint e relação, e nunca percorridas.

**Correção da v1, trazida pela revisão adversarial de 05/08/2026 (achado 2).** A v1 deste plano afirmava que a única travessia de aresta do harness era `_dependency_cycles`, em `forja_reasoning.py:112`. A afirmação está certa quanto ao código e errada quanto ao efeito: aquela função só monta o grafo com arestas de relação `depends_on`. Varredura dos cinco `F3_REASONING_GRAPH.json` reais do harness — 49 arestas ao todo — devolve `supports` 19, `justifies` 12, `qualifies` 8, `records` 4, `limits` 4, `distinguishes` 2, e **zero `depends_on`**. Ou seja: a única travessia existente monta um grafo vazio e devolve lista vazia em toda execução, desde sempre. **Nenhuma aresta de raciocínio jurídico jamais foi percorrida nesta fábrica.** O defeito é maior do que a v1 descreveu, e o detector de ciclo é hoje um gate que não gateia nada.

### C. `paragraph_provenance.json` / `paragraph_evidence_map_n4.json`
Grafo bipartido parágrafo → prova, já existente e populado (54 KB no CASO-17, 42 KB no CASO-18). Sem peso: um parágrafo que carrega a tese decisiva e um parágrafo de cortesia processual valem igual.

### D. `00_IA_NAVIGACAO/dados/arvore_ia.json` (700 KB) + `inventario_ia.json` (13 MB) + `MAPA_IA.md` por pasta
É **árvore**, não grafo — só hierarquia de diretório, zero aresta transversal. Não sabe que o caso X e o caso Y compartilham fonte, tribunal ou tese.

### E. Archify — `*.architecture.json`, `*.workflow.json`, `*.dataflow.json`, `*.sequence.json`
São especificações de **diagrama**, para renderizar. Não são estruturas consultáveis e não pretendem ser.

### F. `forja_fila.py` — a fila priorizada
O espelho invertido do reasoning graph: **tem pesos e não tem arestas.** A tabela normativa do PRD §5 é boa e é declarada (urgência 40/20/0, prazo 40/30/20/10/0, alto valor 10, idade com teto de 10). Mas é uma lista plana: não modela que a demanda A bloqueia a B, que duas peças dependem da mesma fonte, nem quantos casos podem correr em paralelo. É exatamente o exemplo do gerente de projetos do vídeo, sem as arestas.

### G. O grafo que o protocolo exige e não existe
O `CLAUDE.md` determina, desde 11/07/2026, que processo volumoso tenha "cronologia auditada **e grafo dos atos**", com identidade própria por recurso, decisão, retratação e intimação. Hoje isso existe como markdown de cronologia. Como grafo, não existe.

---

## 3. Os quatro defeitos transversais

1. **O peso está onde não decide e falta onde decide.** A fila pontua e não tem aresta; o raciocínio jurídico tem aresta e não pontua.
2. **Grafo que ninguém percorre é desenho.** Um único algoritmo de travessia em toda a casa, é detector de ciclo, e ele nunca rodou — procura uma relação que nenhum grafo real usa.
3. **Uma dimensão por grafo** — o alerta central do vídeo. O reasoning graph só sabe "confirmado / não confirmado". Não sabe força, não sabe custo de perder aquela fonte, não sabe risco, não sabe idade.
4. **Nada envelhece.** Regimento baixado em 06/07 pesa igual a um conferido hoje; precedente possivelmente superado pesa igual a um vigente. O protocolo já exige verificar atualidade — o grafo não representa isso.

---

## 4. Plano — cinco movimentos, em ordem de retorno

### M1 · Ponderar o F3_REASONING_GRAPH  *(maior retorno, menor custo)*

Três números por aresta e um por nó, todos com **tabela normativa declarada** — no formato da tabela do §5 da fila, nunca atribuídos por julgamento livre de modelo:

| Campo | Onde | Escala | Regra de atribuição |
|---|---|---|---|
| `strength` | aresta | 0–1 | documento oficial nos autos 1,0 · ato oficial externo conferido na fonte 0,9 · precedente com inteiro teor lido 0,8 · doutrina 0,5 · inferência declarada 0,3 |
| `necessity` | aresta | 0–1 | a tese cai se esta aresta cair? 1,0 = cai · 0,5 = enfraquece · 0,2 = redundante |
| `verifiedAt` | aresta | data | data da conferência na fonte; alimenta decaimento |
| `criticality` | nó (tese) | 0–1 | a tese sustenta pedido decisivo, subsidiário ou acessório |

Três métricas **derivadas** (nunca escritas à mão):

- **Lastro da tese** = Σ (`strength` × `necessity`) das arestas de entrada.
- **Fragilidade concentrada** = maior fração do lastro vinda de uma única fonte. No CASO-04 isso acenderia hoje em quatro teses por causa de `SRC_A8`.
- **Tese órfã** = grau de entrada zero. Pega o `THESIS-FINE` hoje.

Gate em F7: tese órfã, ou tese sustentando pedido decisivo com lastro abaixo do limiar, ou fragilidade concentrada acima do limiar → achado bloqueante ou P1 conforme calibração.

Entregáveis: `forja_grafo_pesos.py`; campos **opcionais** no schema (retrocompatível — ausência de peso vira default explicitamente declarado no relatório, nunca default silencioso); `test_forja_grafo_pesos.py` com o grafo real do CASO-04 como fixture e os dois achados acima como asserção.

### M2 · Fazer alguém percorrer

Três consultas que o grafo já pode responder e que hoje ninguém pergunta:

- **Caminho crítico fonte → tese → pedido.** Ordena as fontes por quanto do pedido cai se cada uma cair.
- **Corte mínimo.** O menor conjunto de fontes que a parte adversária precisa derrubar para o pedido cair. Isto é red team calculado, e alimenta diretamente as 9 perguntas do red team estruturado.
- **Propagação de invalidação.** Fonte marcada `stale` → quais parágrafos do DOCX ficam sem lastro. Liga o reasoning graph ao `paragraph_provenance` que já existe; hoje os dois são ilhas.

Entregável: `forja_grafo_consulta.py`, saída JSON + tabela no relatório de melhorias da peça.

### M3 · Grafo de atos processuais  *(cumpre ordem já vigente)*

Nós = ato (recurso, decisão, retratação, intimação, destaque), com id próprio, data, sujeito, classe/número. Arestas = `impugna`, `responde`, `retrata`, `intima`, **com peso = prazo em dias** — o exemplo "acordar → levantar = 2 minutos" do vídeo, aplicado ao que a casa realmente faz.

Ganhos diretos: acaba o "o recurso" / "a decisão anterior" que o protocolo proíbe; a dupla contagem de prazo vira travessia verificável em vez de duas leituras humanas; preclusão vira pergunta de alcançabilidade.

### M4 · A fila vira grafo

Adicionar arestas entre demandas: `bloqueia`, `mesma_fonte`, `mesmo_cliente`, `aguarda_decisão_humana`. O score deixa de ser soma local e passa a considerar o subgrafo — a demanda que destrava outras três sobe. E a pergunta operacional que hoje não tem resposta passa a ter: **quantos casos podem correr em paralelo agora** (largura da anticadeia), que é literalmente o exemplo do gerente de projetos do vídeo.

### M5 · Higienizar o graphify antes de tirar conclusão dele

Podar o god node de 2.019 arestas; separar a comunidade 90001 (1.647 nós, coesão 0,00 — é resto, não comunidade); usar `confidence_score` como peso em centralidade ponderada em vez de contar aresta. Só depois disso "nó central" significa alguma coisa. Menor prioridade: é grafo de código, não de caso.

**Ordem:** M1 → M2 → M3 → M4 → M5. M1 e M2 cabem numa sessão e é onde está quase todo o ganho jurídico.

---

## 5. O que não fazer

- **Não trocar o pipeline F0–F10 por "orquestrador de grafo".** O vídeo fala de agentes paralelos queimando token; a fábrica tem gates sequenciais por razão jurídica, não por limitação técnica. F7 antes de F7-B é decisão registrada (ADR-J04), não acidente.
- **Não reabrir RAG / GraphRAG.** Rejeitado no plano 07 e nada aqui muda a premissa. Este plano é sobre ponderar grafos pequenos e auditáveis, não sobre recuperação semântica.
- **Não adotar banco de grafo.** Os grafos de caso têm dezenas de nós. JSON + travessia em memória basta e mantém tudo diffável e hashável, como o resto do harness.
- **Peso inventado por modelo é pior que peso ausente.** Número sem regra declarada de atribuição é opinião com cara de medida — e, em peça protocolável, medida falsa vira alegação falsa. Toda ponderação entra com tabela normativa e conferência, ou não entra.
