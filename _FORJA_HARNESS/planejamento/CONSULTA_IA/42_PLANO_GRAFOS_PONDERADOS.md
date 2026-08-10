# Consulta IA — 42 — Plano de ponderação e inteligência dos grafos da fábrica

> Cópia de consulta derivada. O documento canônico permanece no caminho de origem indicado abaixo.

## Metadados e rastreabilidade

- **Documento de origem:** `42_PLANO_GRAFOS_PONDERADOS.md`
- **Tipo:** Plano
- **SHA-256 da origem:** `129f3786837ed8a701e7a09d7d49f3bd482786d5574b15ac75e352403e6de991`
- **Linhas da origem:** 127
- **Blocos integralmente indexados:** 18
- **Geração:** 2026-08-10T13:53:35-03:00
- **Cobertura:** 100% das linhas e do texto da origem, sem omissão.
- **Links relativos normalizados:** 0 destino(s), apenas para preservar a navegação na cópia.

## Roteiro de consulta para IA

**Síntese de localização:** Data: 05/08/2026 Origem: vídeo "Larguei tudo pra aprender Graph Engineering" (Lucas Montano, 31/07/2026, 15min) + auditoria dos grafos existentes no repositório nesta data.

**Termos de recuperação:** não, grafo, json, aresta, têm, arestas, tese, plano, vídeo, peso, grafos, fonte.

Use o índice abaixo para localizar o bloco pertinente. Cada entrada informa as linhas exatas no documento de origem. Para afirmações materiais, leia o bloco integral e confira o arquivo canônico pelo SHA-256.

## Índice detalhado e cobertura integral

- [SRC-S001 · L1–L9 · 42 — Plano de ponderação e inteligência dos grafos da fábrica](#src-s001)
  - Assuntos: grafos, plano, prd, não, ponderação, inteligência, fábrica, data
  - Trecho-guia: Data: 05/08/2026 Origem: vídeo "Larguei tudo pra aprender Graph Engineering" (Lucas Montano, 31/07/2026, 15min) + auditoria dos grafos existentes no repositório nesta data.
  - SHA-256 do bloco: `014d2a43dabe3a024b269fdc36d9b62a8a5cb16366e58795fcc3e362b3b19c0e`
  - [SRC-S002 · L10–L21 · 1. O que o vídeo entrega, destilado](#src-s002)
    - Caminho: 42 — Plano de ponderação e inteligência dos grafos da fábrica > 1. O que o vídeo entrega, destilado
    - Assuntos: vídeo, não, aresta, entrega, destilado, três, peso, exemplo
    - Trecho-guia: O vídeo é majoritariamente didático (o que é nó, o que é aresta). Três ideias dele são aproveitáveis aqui, e só três:
    - SHA-256 do bloco: `dc972c2acc33ac14110314d546b04dbbfe217ac725f43a4a675c1535a00ac0be`
  - [SRC-S003 · L22–L23 · 2. Inventário dos grafos existentes e diagnóstico de cada um](#src-s003)
    - Caminho: 42 — Plano de ponderação e inteligência dos grafos da fábrica > 2. Inventário dos grafos existentes e diagnóstico de cada um
    - Assuntos: inventário, grafos, existentes, diagnóstico, cada
    - Trecho-guia: Documento de consulta sobre 2. Inventário dos grafos existentes e diagnóstico de cada um.
    - SHA-256 do bloco: `16e01d4764de342c20a5d33137de5b86d383669c076cf74225cbb2c991d14252`
    - [SRC-S004 · L24–L32 · A. graphify-out/graph.json — grafo de código do Motor](#src-s004)
      - Caminho: 42 — Plano de ponderação e inteligência dos grafos da fábrica > 2. Inventário dos grafos existentes e diagnóstico de cada um > A. graphify-out/graph.json — grafo de código do Motor
      - Assuntos: grafo, tem, não, graphify-out, graph, json, código, motor
      - Trecho-guia: 3.156 nós, 9.136 arestas, 111 comunidades (relatório de 05/08/2026, commit 3866e1c1).
      - SHA-256 do bloco: `ca6f4a93130fcfdbfd8d73c94b8f633888eb7c3d92ebe51b7da95fd700ec3f24`
    - [SRC-S005 · L33–L44 · B. F3REASONINGGRAPH.json — grafo de raciocínio jurídico, um por caso](#src-s005)
      - Caminho: 42 — Plano de ponderação e inteligência dos grafos da fábrica > 2. Inventário dos grafos existentes e diagnóstico de cada um > B. F3REASONINGGRAPH.json — grafo de raciocínio jurídico, um por caso
      - Assuntos: grafo, arestas, aresta, quanto, json, raciocínio, jurídico, caso
      - Trecho-guia: É o grafo mais valioso da fábrica e o menos ponderado. Nós: document, thesis, request, decision. Arestas: relation (supports / qualifies / justifies), scope (full / partial), reason, reviewStatus. Nenhum número em lugar algum.
      - SHA-256 do bloco: `ea6196372ce789d20b15a8b828e2632b5eeb6d7a73a8c50a2b7e05ca9b9300eb`
    - [SRC-S006 · L45–L47 · C. paragraphprovenance.json / paragraphevidencemapn4.json](#src-s006)
      - Caminho: 42 — Plano de ponderação e inteligência dos grafos da fábrica > 2. Inventário dos grafos existentes e diagnóstico de cada um > C. paragraphprovenance.json / paragraphevidencemapn4.json
      - Assuntos: json, parágrafo, paragraphprovenance, paragraphevidencemapn4, paragraph_provenance, paragraph_evidence_map_n4, grafo, bipartido
      - Trecho-guia: Grafo bipartido parágrafo → prova, já existente e populado (54 KB no CASO-17, 42 KB no CASO-18). Sem peso: um parágrafo que carrega a tese decisiva e um parágrafo de cortesia processual valem igual.
      - SHA-256 do bloco: `e84c2ffef2f6186f1c0f2b0add87e8403bd91c70b53c3bd36b7ccaac33e05ed3`
    - [SRC-S007 · L48–L50 · D. 00IANAVIGACAO/dados/arvoreia.json (700 KB) + inventarioia.json (13 MB) + MAPAIA.md por pasta](#src-s007)
      - Caminho: 42 — Plano de ponderação e inteligência dos grafos da fábrica > 2. Inventário dos grafos existentes e diagnóstico de cada um > D. 00IANAVIGACAO/dados/arvoreia.json (700 KB) + inventarioia.json (13 MB) + MAPAIA.md por pasta
      - Assuntos: json, dados, pasta, não, caso, ianavigacao, arvoreia, inventarioia
      - Trecho-guia: É árvore, não grafo — só hierarquia de diretório, zero aresta transversal. Não sabe que o caso X e o caso Y compartilham fonte, tribunal ou tese.
      - SHA-256 do bloco: `c9d4d0b101abe778601ecb0f0dd28960f3e8218a93dbcd80fcb7cc5eaad39017`
    - [SRC-S008 · L51–L53 · E. Archify — .architecture.json, .workflow.json, .dataflow.json, .sequence.json](#src-s008)
      - Caminho: 42 — Plano de ponderação e inteligência dos grafos da fábrica > 2. Inventário dos grafos existentes e diagnóstico de cada um > E. Archify — .architecture.json, .workflow.json, .dataflow.json, .sequence.json
      - Assuntos: json, archify, architecture, workflow, dataflow, sequence, são, não
      - Trecho-guia: São especificações de diagrama, para renderizar. Não são estruturas consultáveis e não pretendem ser.
      - SHA-256 do bloco: `59eb728b621ded422808a13105a44f7097858f4b4550cdbafb91f523fcc7620a`
    - [SRC-S009 · L54–L56 · F. forjafila.py — a fila priorizada](#src-s009)
      - Caminho: 42 — Plano de ponderação e inteligência dos grafos da fábrica > 2. Inventário dos grafos existentes e diagnóstico de cada um > F. forjafila.py — a fila priorizada
      - Assuntos: fila, priorizada, tem, não, arestas, forjafila, forja_fila, espelho
      - Trecho-guia: O espelho invertido do reasoning graph: tem pesos e não tem arestas. A tabela normativa do PRD §5 é boa e é declarada (urgência 40/20/0, prazo 40/30/20/10/0, alto valor 10, idade com teto de 10). Mas é uma lista plana: não modela que a demanda A bloqueia a B, que duas peças depen
      - SHA-256 do bloco: `4cdb0f253108d442ff006b5ca6ed39b7216c82bc3f94914482ee725da07b4598`
    - [SRC-S010 · L57–L61 · G. O grafo que o protocolo exige e não existe](#src-s010)
      - Caminho: 42 — Plano de ponderação e inteligência dos grafos da fábrica > 2. Inventário dos grafos existentes e diagnóstico de cada um > G. O grafo que o protocolo exige e não existe
      - Assuntos: grafo, existe, não, protocolo, exige, cronologia, claude, determina
      - Trecho-guia: O CLAUDE.md determina, desde 11/07/2026, que processo volumoso tenha "cronologia auditada e grafo dos atos", com identidade própria por recurso, decisão, retratação e intimação. Hoje isso existe como markdown de cronologia. Como grafo, não existe.
      - SHA-256 do bloco: `040bf29de9926df3b234a420ceefb600eb4f222f5f09e241b620180e745c18f1`
  - [SRC-S011 · L62–L70 · 3. Os quatro defeitos transversais](#src-s011)
    - Caminho: 42 — Plano de ponderação e inteligência dos grafos da fábrica > 3. Os quatro defeitos transversais
    - Assuntos: não, sabe, grafo, quatro, defeitos, transversais, onde, decide
    - Trecho-guia: 1. O peso está onde não decide e falta onde decide. A fila pontua e não tem aresta; o raciocínio jurídico tem aresta e não pontua. 2. Grafo que ninguém percorre é desenho. Um único algoritmo de travessia em toda a casa, é detector de ciclo, e ele nunca rodou — procura uma relação
    - SHA-256 do bloco: `85fa64102801769eaa3b8f930c85929439db0aa276804ca707fd6b9ca2e18123`
  - [SRC-S012 · L71–L72 · 4. Plano — cinco movimentos, em ordem de retorno](#src-s012)
    - Caminho: 42 — Plano de ponderação e inteligência dos grafos da fábrica > 4. Plano — cinco movimentos, em ordem de retorno
    - Assuntos: plano, cinco, movimentos, ordem, retorno
    - Trecho-guia: Documento de consulta sobre 4. Plano — cinco movimentos, em ordem de retorno.
    - SHA-256 do bloco: `4bc075a343d9900219803c785655c8b324cf41e6bd45e42aedc941dcd20b373f`
    - [SRC-S013 · L73–L93 · M1 · Ponderar o F3REASONINGGRAPH (maior retorno, menor custo)](#src-s013)
      - Caminho: 42 — Plano de ponderação e inteligência dos grafos da fábrica > 4. Plano — cinco movimentos, em ordem de retorno > M1 · Ponderar o F3REASONINGGRAPH (maior retorno, menor custo)
      - Assuntos: tese, aresta, maior, nunca, fonte, lastro, ponderar, retorno
      - Trecho-guia: Três números por aresta e um por nó, todos com tabela normativa declarada — no formato da tabela do §5 da fila, nunca atribuídos por julgamento livre de modelo:
      - SHA-256 do bloco: `ab04e7bd49c1cf33eeafaad8ade0ff09f6fae708b61683863e3cf4f1a50444fa`
    - [SRC-S014 · L94–L103 · M2 · Fazer alguém percorrer](#src-s014)
      - Caminho: 42 — Plano de ponderação e inteligência dos grafos da fábrica > 4. Plano — cinco movimentos, em ordem de retorno > M2 · Fazer alguém percorrer
      - Assuntos: pedido, fazer, alguém, percorrer, hoje, fonte, fontes, cair
      - Trecho-guia: Três consultas que o grafo já pode responder e que hoje ninguém pergunta:
      - SHA-256 do bloco: `e7222f34a7545719cb9703e450380b7f34968773fd594622e4e120f059fa0bed`
    - [SRC-S015 · L104–L109 · M3 · Grafo de atos processuais (cumpre ordem já vigente)](#src-s015)
      - Caminho: 42 — Plano de ponderação e inteligência dos grafos da fábrica > 4. Plano — cinco movimentos, em ordem de retorno > M3 · Grafo de atos processuais (cumpre ordem já vigente)
      - Assuntos: grafo, atos, processuais, cumpre, ordem, vigente, recurso, decisão
      - Trecho-guia: Nós = ato (recurso, decisão, retratação, intimação, destaque), com id próprio, data, sujeito, classe/número. Arestas = impugna, responde, retrata, intima, com peso = prazo em dias — o exemplo "acordar → levantar = 2 minutos" do vídeo, aplicado ao que a casa realmente faz.
      - SHA-256 do bloco: `a02accbd7a9a51df11299f75b3759bc307cd6f79e4e87ca510a27104204a2a2e`
    - [SRC-S016 · L110–L113 · M4 · A fila vira grafo](#src-s016)
      - Caminho: 42 — Plano de ponderação e inteligência dos grafos da fábrica > 4. Plano — cinco movimentos, em ordem de retorno > M4 · A fila vira grafo
      - Assuntos: fila, vira, grafo, passa, adicionar, arestas, demandas, bloqueia
      - Trecho-guia: Adicionar arestas entre demandas: bloqueia, mesmafonte, mesmocliente, aguardadecisãohumana. O score deixa de ser soma local e passa a considerar o subgrafo — a demanda que destrava outras três sobe. E a pergunta operacional que hoje não tem resposta passa a ter: quantos casos pod
      - SHA-256 do bloco: `74e9148c96caa76ef1d0029ab6ad9cf965f466d2c571a5dfb72f56444f570075`
    - [SRC-S017 · L114–L121 · M5 · Higienizar o graphify antes de tirar conclusão dele](#src-s017)
      - Caminho: 42 — Plano de ponderação e inteligência dos grafos da fábrica > 4. Plano — cinco movimentos, em ordem de retorno > M5 · Higienizar o graphify antes de tirar conclusão dele
      - Assuntos: higienizar, graphify, antes, tirar, conclusão, dele, comunidade, não
      - Trecho-guia: Podar o god node de 2.019 arestas; separar a comunidade 90001 (1.647 nós, coesão 0,00 — é resto, não comunidade); usar confidencescore como peso em centralidade ponderada em vez de contar aresta. Só depois disso "nó central" significa alguma coisa. Menor prioridade: é grafo de có
      - SHA-256 do bloco: `7d336ff7af348dfc441465a250ef0e2385cad3df91d6782d32b9897e0eb03d8d`
  - [SRC-S018 · L122–L127 · 5. O que não fazer](#src-s018)
    - Caminho: 42 — Plano de ponderação e inteligência dos grafos da fábrica > 5. O que não fazer
    - Assuntos: não, fazer, grafo, tem, plano, sobre, grafos, peso
    - Trecho-guia: Não trocar o pipeline F0–F10 por "orquestrador de grafo". O vídeo fala de agentes paralelos queimando token; a fábrica tem gates sequenciais por razão jurídica, não por limitação técnica. F7 antes de F7-B é decisão registrada (ADR-J04), não acidente. Não reabrir RAG / GraphRAG. R
    - SHA-256 do bloco: `6f99279b850c7da3cb684ac389e6da0bdec94e6488cc3eace42886a85cf19567`

## Conteúdo integral indexado

Os marcadores HTML abaixo são apenas âncoras de navegação. O texto reproduz integralmente a origem normalizada em UTF-8; somente destinos de links relativos podem ter sido recalculados para apontar ao mesmo arquivo a partir desta pasta.

<a id="src-s001"></a>

# 42 — Plano de ponderação e inteligência dos grafos da fábrica

Data: 05/08/2026
Origem: vídeo "Larguei tudo pra aprender Graph Engineering" (Lucas Montano, 31/07/2026, 15min) + auditoria dos grafos existentes no repositório nesta data.

> **Status: diagnóstico válido, ordem de execução SUPERADA.** O PRD `43_PRD_GRAFOS_PONDERADOS.md` v3, de 05/08/2026, inverteu o primeiro movimento deste plano depois de medir a fórmula proposta contra os seis grafos reais: 12 das 20 teses saturam em lastro 1,000 e 8 dão 0,000, e 40% das teses não têm nenhuma aresta sustentadora. Os grafos não estão subponderados, estão despovoados e sem ontologia comum. **Não implemente o M1 deste plano** — vale o E0 do PRD v3, que mede completude sem peso. O diagnóstico das seções 2 e 3 abaixo permanece correto e é a base do PRD.

---


<a id="src-s002"></a>

## 1. O que o vídeo entrega, destilado

O vídeo é majoritariamente didático (o que é nó, o que é aresta). Três ideias dele são aproveitáveis aqui, e só três:

1. **A aresta carrega peso, e o peso é a informação.** O exemplo é doméstico — acordar → levantar = 2 minutos — mas a tese é a certa: sem número na aresta você tem um desenho de relações, não uma estrutura sobre a qual se busca ou se otimiza.
2. **"Uma métrica nunca é suficiente."** É o ponto central. Um agente em loop otimizando custo de aquisição baixa o CAC e aumenta o churn sem perceber, porque só enxerga uma aresta. Grafo existe para representar como uma métrica afeta a outra.
3. **O exemplo do gerente de projetos.** Epic → story → task → subtask *não é árvore*, porque há dependências cruzadas. E é exatamente a dependência que responde a pergunta operacional real: quantos recursos podem trabalhar em paralelo agora, e o que destrava o quê.

O que o vídeo **não** entrega: nenhuma receita de engenharia, nenhum esquema, nenhum algoritmo. O autor inclusive conclui que não valia parar tudo para estudar "graph engineering". Portanto este plano usa o vídeo como provocação, não como especificação.

---


<a id="src-s003"></a>

## 2. Inventário dos grafos existentes e diagnóstico de cada um


<a id="src-s004"></a>

### A. `graphify-out/graph.json` — grafo de código do Motor
3.156 nós, 9.136 arestas, 111 comunidades (relatório de 05/08/2026, commit `3866e1c1`).

É o único grafo da casa que **tem um número na aresta**: `confidence_score` (1.0 para `EXTRACTED`, ~0.92 para os 103 `INFERRED`). Mas é peso de *procedência da aresta*, não de importância do que ela liga. Três defeitos concretos:

- **God node.** `FORJA Harness` tem 2.019 das 9.136 arestas. Qualquer centralidade calculada sobre este grafo mede a distância até esse nó e mais nada.
- **Comunidade que não é comunidade.** A 90001 ("Interfaces inferiores v3") tem 1.647 nós e coesão **0,00**. Não é um agrupamento, é o resto.
- Ninguém consome. É gerado, lido por humano, e fim.


<a id="src-s005"></a>

### B. `F3_REASONING_GRAPH.json` — grafo de raciocínio jurídico, um por caso
**É o grafo mais valioso da fábrica e o menos ponderado.** Nós: `document`, `thesis`, `request`, `decision`. Arestas: `relation` (supports / qualifies / justifies), `scope` (full / partial), `reason`, `reviewStatus`. **Nenhum número em lugar algum.**

A auditoria do grafo real do CASO-04 (`forja_acervo.caso("CASO-04")`, 21 nós, 13 arestas, status `approved`, com reviewer independente) produziu dois achados que o grafo já contém e que ninguém extraiu:

- **`SRC_A8` (Nova Decisão de 28/04/2026) sustenta sozinho 4 das 5 teses** — PARTIAL, 1022, 211 e S7. É fragilidade concentrada: derrubada aquela peça, a impugnação perde quatro pilares de uma vez. O grafo sabe disso desde 15/07 e nunca contou a ninguém.
- **`THESIS-FINE` não tem nenhuma aresta de entrada.** É uma tese sem lastro documental declarado no grafo — só sai dela a aresta para `REQUEST-FINE`. Ou falta a aresta, ou falta a fonte. Em ambos os casos é achado de auditoria, e passou pelo revisor independente.

Quanto ao consumo: verifiquei todos os leitores (`forja_n4_validate`, `forja_reasoning`, `forja_pso_pet`, `forja_run_metrics`, `forja_n4_invalidation`). Eles leem o **conjunto de ids dos nós** para checar se um `supportId` de outro artefato existe. Fora isso, as arestas são validadas quanto a endpoint e relação, e nunca percorridas.

**Correção da v1, trazida pela revisão adversarial de 05/08/2026 (achado 2).** A v1 deste plano afirmava que a única travessia de aresta do harness era `_dependency_cycles`, em `forja_reasoning.py:112`. A afirmação está certa quanto ao código e errada quanto ao efeito: aquela função só monta o grafo com arestas de relação `depends_on`. Varredura dos cinco `F3_REASONING_GRAPH.json` reais do harness — 49 arestas ao todo — devolve `supports` 19, `justifies` 12, `qualifies` 8, `records` 4, `limits` 4, `distinguishes` 2, e **zero `depends_on`**. Ou seja: a única travessia existente monta um grafo vazio e devolve lista vazia em toda execução, desde sempre. **Nenhuma aresta de raciocínio jurídico jamais foi percorrida nesta fábrica.** O defeito é maior do que a v1 descreveu, e o detector de ciclo é hoje um gate que não gateia nada.


<a id="src-s006"></a>

### C. `paragraph_provenance.json` / `paragraph_evidence_map_n4.json`
Grafo bipartido parágrafo → prova, já existente e populado (54 KB no CASO-17, 42 KB no CASO-18). Sem peso: um parágrafo que carrega a tese decisiva e um parágrafo de cortesia processual valem igual.


<a id="src-s007"></a>

### D. `00_IA_NAVIGACAO/dados/arvore_ia.json` (700 KB) + `inventario_ia.json` (13 MB) + `MAPA_IA.md` por pasta
É **árvore**, não grafo — só hierarquia de diretório, zero aresta transversal. Não sabe que o caso X e o caso Y compartilham fonte, tribunal ou tese.


<a id="src-s008"></a>

### E. Archify — `*.architecture.json`, `*.workflow.json`, `*.dataflow.json`, `*.sequence.json`
São especificações de **diagrama**, para renderizar. Não são estruturas consultáveis e não pretendem ser.


<a id="src-s009"></a>

### F. `forja_fila.py` — a fila priorizada
O espelho invertido do reasoning graph: **tem pesos e não tem arestas.** A tabela normativa do PRD §5 é boa e é declarada (urgência 40/20/0, prazo 40/30/20/10/0, alto valor 10, idade com teto de 10). Mas é uma lista plana: não modela que a demanda A bloqueia a B, que duas peças dependem da mesma fonte, nem quantos casos podem correr em paralelo. É exatamente o exemplo do gerente de projetos do vídeo, sem as arestas.


<a id="src-s010"></a>

### G. O grafo que o protocolo exige e não existe
O `CLAUDE.md` determina, desde 11/07/2026, que processo volumoso tenha "cronologia auditada **e grafo dos atos**", com identidade própria por recurso, decisão, retratação e intimação. Hoje isso existe como markdown de cronologia. Como grafo, não existe.

---


<a id="src-s011"></a>

## 3. Os quatro defeitos transversais

1. **O peso está onde não decide e falta onde decide.** A fila pontua e não tem aresta; o raciocínio jurídico tem aresta e não pontua.
2. **Grafo que ninguém percorre é desenho.** Um único algoritmo de travessia em toda a casa, é detector de ciclo, e ele nunca rodou — procura uma relação que nenhum grafo real usa.
3. **Uma dimensão por grafo** — o alerta central do vídeo. O reasoning graph só sabe "confirmado / não confirmado". Não sabe força, não sabe custo de perder aquela fonte, não sabe risco, não sabe idade.
4. **Nada envelhece.** Regimento baixado em 06/07 pesa igual a um conferido hoje; precedente possivelmente superado pesa igual a um vigente. O protocolo já exige verificar atualidade — o grafo não representa isso.

---


<a id="src-s012"></a>

## 4. Plano — cinco movimentos, em ordem de retorno


<a id="src-s013"></a>

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


<a id="src-s014"></a>

### M2 · Fazer alguém percorrer

Três consultas que o grafo já pode responder e que hoje ninguém pergunta:

- **Caminho crítico fonte → tese → pedido.** Ordena as fontes por quanto do pedido cai se cada uma cair.
- **Corte mínimo.** O menor conjunto de fontes que a parte adversária precisa derrubar para o pedido cair. Isto é red team calculado, e alimenta diretamente as 9 perguntas do red team estruturado.
- **Propagação de invalidação.** Fonte marcada `stale` → quais parágrafos do DOCX ficam sem lastro. Liga o reasoning graph ao `paragraph_provenance` que já existe; hoje os dois são ilhas.

Entregável: `forja_grafo_consulta.py`, saída JSON + tabela no relatório de melhorias da peça.


<a id="src-s015"></a>

### M3 · Grafo de atos processuais  *(cumpre ordem já vigente)*

Nós = ato (recurso, decisão, retratação, intimação, destaque), com id próprio, data, sujeito, classe/número. Arestas = `impugna`, `responde`, `retrata`, `intima`, **com peso = prazo em dias** — o exemplo "acordar → levantar = 2 minutos" do vídeo, aplicado ao que a casa realmente faz.

Ganhos diretos: acaba o "o recurso" / "a decisão anterior" que o protocolo proíbe; a dupla contagem de prazo vira travessia verificável em vez de duas leituras humanas; preclusão vira pergunta de alcançabilidade.


<a id="src-s016"></a>

### M4 · A fila vira grafo

Adicionar arestas entre demandas: `bloqueia`, `mesma_fonte`, `mesmo_cliente`, `aguarda_decisão_humana`. O score deixa de ser soma local e passa a considerar o subgrafo — a demanda que destrava outras três sobe. E a pergunta operacional que hoje não tem resposta passa a ter: **quantos casos podem correr em paralelo agora** (largura da anticadeia), que é literalmente o exemplo do gerente de projetos do vídeo.


<a id="src-s017"></a>

### M5 · Higienizar o graphify antes de tirar conclusão dele

Podar o god node de 2.019 arestas; separar a comunidade 90001 (1.647 nós, coesão 0,00 — é resto, não comunidade); usar `confidence_score` como peso em centralidade ponderada em vez de contar aresta. Só depois disso "nó central" significa alguma coisa. Menor prioridade: é grafo de código, não de caso.

**Ordem:** M1 → M2 → M3 → M4 → M5. M1 e M2 cabem numa sessão e é onde está quase todo o ganho jurídico.

---


<a id="src-s018"></a>

## 5. O que não fazer

- **Não trocar o pipeline F0–F10 por "orquestrador de grafo".** O vídeo fala de agentes paralelos queimando token; a fábrica tem gates sequenciais por razão jurídica, não por limitação técnica. F7 antes de F7-B é decisão registrada (ADR-J04), não acidente.
- **Não reabrir RAG / GraphRAG.** Rejeitado no plano 07 e nada aqui muda a premissa. Este plano é sobre ponderar grafos pequenos e auditáveis, não sobre recuperação semântica.
- **Não adotar banco de grafo.** Os grafos de caso têm dezenas de nós. JSON + travessia em memória basta e mantém tudo diffável e hashável, como o resto do harness.
- **Peso inventado por modelo é pior que peso ausente.** Número sem regra declarada de atribuição é opinião com cara de medida — e, em peça protocolável, medida falsa vira alegação falsa. Toda ponderação entra com tabela normativa e conferência, ou não entra.
