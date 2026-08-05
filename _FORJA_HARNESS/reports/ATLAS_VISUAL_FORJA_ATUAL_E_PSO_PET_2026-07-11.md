# FORJA explicada por dentro

**Como a demanda se transforma em uma petição pronta para revisão humana**<br>
**Data de referência:** 12/07/2026<br>
**Como ler as cores:** petróleo = funcionamento atual; terracota = melhoria em teste; grafite = evolução planejada; verde = informação confirmada; vermelho = impedimento.

> Este atlas mostra, em linguagem direta, o que a FORJA já faz, quais melhorias estão sendo testadas e o que ainda depende de comprovação. A edição de 12/07/2026 reúne o fluxo completo, a integração com a gestão do escritório, as verificações jurídicas e os aprendizados obtidos com petições reais.

<div class="executive-cards">
  <div class="executive-card active"><strong>11 etapas</strong><span>da entrada da demanda à comprovação da entrega</span></div>
  <div class="executive-card evidence"><strong>Afirmação → fonte</strong><span>cada ponto importante pode ser conferido</span></div>
  <div class="executive-card human"><strong>Helena + Cícero</strong><span>conselho obrigatório e registrado</span></div>
  <div class="executive-card shadow"><strong>Análise aprofundada</strong><span>melhorias testadas antes de se tornarem obrigatórias</span></div>
</div>

## 1. Visão executiva

### 1.1 A FORJA dentro do escritório

**A base da FORJA já funciona. As análises mais profundas ainda passam por testes controlados.**

```mermaid
flowchart LR
    Intake["E-mail, WhatsApp/Hermes<br/>ou comando manual"] --> Management["Gestão do escritório<br/>fila, prazo, responsável e evidência"]
    Management --> Forja["FORJA<br/>onze etapas, da entrada à entrega,<br/>com registros e verificações"]
    Case["Pasta do caso<br/>autos, anexos, regimento e leis"] --> Forja
    Forja --> Council["Conselho obrigatório<br/>Helena + Cícero"]
    Council --> Draft["Primeira versão da peça<br/>tese, fatos, fundamentos e pedidos"]
    Draft --> Audit["Revisão dos fatos, do direito,<br/>do sentido e da apresentação"]
    Audit --> Human["Revisão humana<br/>Igor + Fábio"]
    Human --> Delivery["Envio ou protocolo<br/>com evidência real"]
    Delivery --> Management
    Delivery --> Learning["Comparação com a versão final<br/>e aprendizado para casos futuros"]
    Learning --> Forja
    Pso["Diagnóstico aprofundado<br/>problema, causas, alternativas<br/>e forma de conferir o resultado"] -. "melhoria em teste" .-> Forja

    classDef active fill:#e8f1ef,stroke:#395c60,color:#21383b,stroke-width:2px;
    classDef shadow fill:#fbf2ec,stroke:#9c5b38,color:#5b3522,stroke-width:2px;
    classDef human fill:#fff4d8,stroke:#9a6b18,color:#4b370d,stroke-width:2px;
    classDef evidence fill:#e9f4ec,stroke:#2f6f54,color:#1f4c39,stroke-width:2px;
    class Intake,Management,Forja,Case,Draft,Audit,Delivery,Learning active;
    class Council,Human human;
    class Pso shadow;
```

### 1.2 O que é fonte de verdade

```mermaid
flowchart TB
    subgraph Operational["Verdade operacional"]
        Queue["Painel do escritório<br/>fila, prioridade e responsável"]
        State["Andamento do caso<br/>etapa atual e impedimentos"]
        Evidence["e-mail, protocolo ou intervenção<br/>evidência de entrega"]
    end
    subgraph Legal["Verdade jurídica"]
        Autos["Autos e anexos primários"]
        Regimento["Regimento vigente do tribunal"]
        Official["Lei e fonte oficial"]
        Precedent["Precedente integral e conferido"]
    end
    subgraph Derived["Informações organizadas e conferíveis"]
        Ledger["Registro de fatos, fontes e afirmações"]
        Graph["Ligação entre pergunta, fato,<br/>fundamento, tese e pedido"]
        Blueprint["Plano da peça e força das teses"]
        PsoCase["Diagnóstico do caso<br/>problema, causas e soluções possíveis"]
    end
    Queue --> State
    Evidence --> State
    Autos --> Ledger
    Regimento --> Ledger
    Official --> Ledger
    Precedent --> Ledger
    Ledger --> Graph
    Graph --> Blueprint
    PsoCase -. "em teste" .-> Blueprint
    Blueprint --> Petition["Petição limpa e pronta para protocolo"]
    State --> Petition
    Petition --> Evidence

    classDef active fill:#e8f1ef,stroke:#395c60,color:#21383b;
    classDef evidence fill:#e9f4ec,stroke:#2f6f54,color:#1f4c39;
    classDef shadow fill:#fbf2ec,stroke:#9c5b38,color:#5b3522;
    classDef output fill:#f0f1f3,stroke:#49494d,color:#2d2d31;
    class Queue,State,Evidence active;
    class Autos,Regimento,Official,Precedent,Ledger evidence;
    class Graph,Blueprint active;
    class PsoCase shadow;
    class Petition output;
```

## 2. O caminho completo de uma petição

### 2.1 As onze etapas, da demanda à entrega

```mermaid
flowchart TB
    F0["Etapa 1 · Conferir a demanda<br/>fila, canais de entrada e situação real"] --> F1["Etapa 2 · Organizar e conferir os documentos<br/>orientação, anexos, arquivos e instruções ocultas"]
    F1 --> F2["Etapa 3 · Definir o tipo de peça e o risco<br/>produto, tribunal, risco e perfil"]
    F2 --> F3["Etapa 4 · Confirmar tribunal, regras e fontes<br/>regimento, leis, fatos e sequência dos atos"]
    F3 --> F4["Etapa 5 · Planejar a estratégia<br/>perguntas, teses, pedidos e pareceres"]
    F4 --> F5["Etapa 6 · Pesquisar e validar fundamentos<br/>jurisprudência oficial e pesquisa científica, quando necessária"]
    F5 --> F6["Etapa 7 · Redigir a peça<br/>modelo oficial do escritório e fontes conferíveis"]
    F6 --> F7["Etapa 8 · Revisar fatos, direito e coerência<br/>inclui a melhor crítica que a parte contrária poderia fazer"]
    F7 --> F8["Etapa 9 · Conferir apresentação e legibilidade<br/>Microsoft Word, PDF e todas as páginas"]
    F8 --> F9["Etapa 10 · Preparar o material para revisão<br/>arquivo conferido e rascunho de e-mail, quando autorizado"]
    F9 --> F10["Etapa 11 · Comprovar a entrega e registrar o aprendizado<br/>evidência, gestão, comparação e retrospectiva"]

    F7 -->|"impedimento grave ou mudança de sentido"| F3
    F7 -->|"tese mal desenhada"| F4
    F5 -->|"fonte altera o problema"| F2
    F8 -->|"arquivo precisa ser refeito"| F7

    classDef active fill:#e8f1ef,stroke:#395c60,color:#21383b,stroke-width:2px;
    classDef research fill:#edf2f8,stroke:#315f8c,color:#243f5c,stroke-width:2px;
    classDef human fill:#fff4d8,stroke:#9a6b18,color:#4b370d,stroke-width:2px;
    class F0,F1,F2,F3,F6,F8,F9,F10 active;
    class F4,F5,F7 research;
```

### 2.2 Como a situação do trabalho muda

```mermaid
stateDiagram-v2
    state "Nova demanda" as nova
    state "Conferindo a entrada" as em_reconciliacao
    state "Confirmando regras e fontes" as em_fontes
    state "Planejando a estratégia" as em_planejamento
    state "Pesquisando fundamentos" as em_pesquisa
    state "Redigindo a peça" as em_redacao
    state "Revisando fatos e direito" as em_auditoria
    state "Conferindo a apresentação" as em_qa_visual
    state "Pronta para revisão humana" as pronta_para_revisao
    state "Aguardando prova da entrega" as aguardando_evidencia_entrega
    state "Trabalho concluído" as cumprida
    state "Trabalho cancelado" as cancelada
    state "Parada por impedimento" as blocked
    state "Pesquisa temporariamente limitada" as degraded
    [*] --> nova
    nova --> em_reconciliacao
    em_reconciliacao --> blocked: comando/pasta conflitante
    em_reconciliacao --> em_fontes: entrada íntegra
    em_fontes --> blocked: falta fonte essencial ou regimento
    em_fontes --> em_planejamento
    em_planejamento --> em_pesquisa
    em_planejamento --> blocked: divergência grave não decidida
    em_pesquisa --> em_redacao
    em_pesquisa --> degraded: fonte externa indisponível
    degraded --> em_pesquisa: acesso restabelecido
    em_redacao --> em_auditoria
    em_auditoria --> em_planejamento: tese precisa redesenho
    em_auditoria --> em_qa_visual: sem impedimento grave
    em_qa_visual --> em_auditoria: arquivo regenerado
    em_qa_visual --> pronta_para_revisao
    pronta_para_revisao --> aguardando_evidencia_entrega
    aguardando_evidencia_entrega --> cumprida: prova real
    blocked --> em_reconciliacao: lacuna sanada
    pronta_para_revisao --> cancelada: decisão humana
    cumprida --> [*]
    cancelada --> [*]
```

### 2.3 Responsabilidades e decisões

```mermaid
sequenceDiagram
    participant O as Origem e gestão
    participant F as FORJA
    participant H as Helena
    participant C as Cícero
    participant I as Igor
    participant B as Fábio
    participant D as Entrega

    O->>F: comando, prazo, pasta e anexos
    F->>F: confere a entrada, define o tipo de peça e verifica as fontes
    F->>H: diagnóstico, alternativas e melhor objeção
    H-->>F: recomendações estratégicas e razões
    F->>C: veículo, tese, pedidos e riscos jurídicos
    C-->>F: orientação jurídica e limites da formulação
    F->>F: redige, testa, gera os documentos e revisa
    F->>I: peça, pontos pendentes e arquivo conferido
    I->>B: revisão jurídica final
    B-->>I: aprova, corrige ou muda estratégia
    I->>F: decisão humana e versão aprovada
    F->>D: versão aprovada e identificação segura do arquivo
    D-->>F: evidência de envio ou protocolo
    F->>O: atualiza gestão e aprendizado
```

## 3. Como o caso entra e se torna confiável

### 3.1 Da demanda recebida ao conjunto de documentos conferido

```mermaid
flowchart LR
    Signal["Sinal recebido"] --> Reconcile{"Já existe demanda<br/>ou pasta compatível?"}
    Reconcile -->|"sim"| Merge["Reunir com o que já existe, sem sobrescrever"]
    Reconcile -->|"não"| Create["Criar demanda e pasta"]
    Merge --> Inventory["Inventário de anexos"]
    Create --> Inventory
    Inventory --> Scan["Verificar integridade<br/>e procurar instruções ocultas"]
    Scan --> Command["Comando arquivado"]
    Command --> Tribunal["Identificar tribunal e órgão"]
    Tribunal --> Rules["Regimento integral + emendas<br/>+ leis gerais"]
    Rules --> Chronology["Sequência dos atos<br/>e relação entre recursos e decisões"]
    Chronology --> Identity{"Ato atual impugnado<br/>está inequívoco?"}
    Identity -->|"não"| Block["Impedimento grave<br/>não produzir versão pronta para protocolo"]
    Identity -->|"sim"| Ledger["Registro inicial das fontes"]

    classDef active fill:#e8f1ef,stroke:#395c60,color:#21383b;
    classDef evidence fill:#e9f4ec,stroke:#2f6f54,color:#1f4c39;
    classDef blocker fill:#fdecea,stroke:#a33b2b,color:#64251b,stroke-width:2px;
    class Signal,Reconcile,Merge,Create,Inventory,Scan,Command,Tribunal active;
    class Rules,Chronology,Identity,Ledger evidence;
    class Block blocker;
```

### 3.2 Origem da informação interna versus referência processual

```mermaid
flowchart TB
    Source["Origem da informação<br/>documento recebido, autos ou fonte oficial"] --> Internal["Registro interno<br/>origem, identificação do arquivo, página, trecho e situação"]
    Internal --> Claim["Afirmação juridicamente relevante"]
    Claim --> Gate{"A afirmação pode aparecer<br/>na petição?"}
    Gate -->|"não"| Pending["Pendência interna<br/>remover, confirmar ou bloquear"]
    Gate -->|"sim"| Procedural["Referência processual verdadeira<br/>número do documento, evento, folha ou anexo"]
    Procedural --> Clean["Petição limpa<br/>sem mencionar e-mails, pastas ou bastidores"]

    classDef evidence fill:#e9f4ec,stroke:#2f6f54,color:#1f4c39;
    classDef internal fill:#edf2f8,stroke:#315f8c,color:#243f5c;
    classDef blocker fill:#fdecea,stroke:#a33b2b,color:#64251b;
    class Source,Internal,Claim internal;
    class Gate,Procedural,Clean evidence;
    class Pending blocker;
```

## 4. Como a FORJA organiza as informações

### 4.1 O que fica em primeiro plano e o que é consultado depois

**A FORJA mantém em primeiro plano apenas o que é necessário para decidir cada questão. Os documentos completos permanecem disponíveis para conferência.**

```mermaid
flowchart TB
    L0["Informação essencial neste momento<br/>problema, objetivo, decisões e impedimentos"]
    L1["Uma ficha para cada questão<br/>pergunta, provas, dependências e próximo passo"]
    L2["Quadros de apoio<br/>sequência dos atos, fatos, teses e pontos respondidos"]
    L3["Documentos consultados quando necessários<br/>autos, anexos, regimento, precedentes e estudos"]
    L4["Histórico preservado<br/>versões anteriores e material secundário"]

    L0 --> L1
    L1 -->|"indicação da origem"| L2
    L2 -->|"falta de prova"| L3
    L3 -->|"nova evidência"| L1
    L2 -->|"não ativo agora"| L4
    L4 -->|"condição de retorno"| L1
    L1 --> Output["Tarefa de análise específica<br/>sem carregar o processo inteiro de uma vez"]

    classDef active fill:#e8f1ef,stroke:#395c60,color:#21383b,stroke-width:2px;
    classDef shadow fill:#fbf2ec,stroke:#9c5b38,color:#5b3522,stroke-width:2px;
    classDef archive fill:#f0f1f3,stroke:#707078,color:#3e3e44;
    class L2,L3 active;
    class L0,L1,Output shadow;
    class L4 archive;
```

### 4.2 Ciclo de uma questão

```mermaid
flowchart LR
    Question["Questão relevante"] --> Packet["Abrir a ficha da questão"]
    Packet --> Need{"Evidência suficiente?"}
    Need -->|"não"| Fetch["Consultar somente os documentos necessários"]
    Fetch --> Test["Comparar o que favorece, o que limita<br/>e o que aponta em sentido contrário"]
    Need -->|"sim"| Test
    Test --> Answer{"Resposta sustentada?"}
    Answer -->|"sim"| Record["Registrar resposta, fonte e consequência"]
    Answer -->|"parcial"| Partial["Registrar o que ainda falta e o risco restante"]
    Answer -->|"não"| Block["Bloquear ou retirar a tese"]
    Record --> Close["Fechar a ficha e indicar quando ela deve ser reaberta"]
    Partial --> Close
    Close --> Trigger{"Surgiu nova decisão,<br/>documento ou contradição?"}
    Trigger -->|"sim"| Packet
    Trigger -->|"não"| Done["Preservar no mapa do raciocínio e no plano da peça"]

    classDef shadow fill:#fbf2ec,stroke:#9c5b38,color:#5b3522;
    classDef evidence fill:#e9f4ec,stroke:#2f6f54,color:#1f4c39;
    classDef blocker fill:#fdecea,stroke:#a33b2b,color:#64251b;
    class Question,Packet,Need,Trigger shadow;
    class Fetch,Test,Answer,Record,Partial,Close,Done evidence;
    class Block blocker;
```

## 5. Como a FORJA constrói a estratégia jurídica

### 5.1 Das perguntas do caso aos fundamentos e pedidos

```mermaid
flowchart LR
    Root["Pergunta que o julgador precisa responder"] --> QF["Questões de fato"]
    Root --> QP["Questões processuais"]
    Root --> QM["Questões de mérito"]
    Root --> QR["Pedidos e riscos"]

    QF --> Fact["Fato relevante"]
    Fact --> Doc["Documento, página e trecho"]
    QP --> Event["Ato processual relevante"]
    Event --> Rule["Regra, regimento e vigência no tempo"]
    QM --> Thesis["Tese"]
    Doc --> Thesis
    Rule --> Thesis
    Counter["Fonte contrária ou melhor objeção"] --> Thesis
    Thesis --> Request["Pedido e consequência"]
    Request --> Test["Pergunta de conferência"]
    Test --> Paragraph["Parágrafo, quadro ou diagrama correspondente"]

    classDef active fill:#e8f1ef,stroke:#395c60,color:#21383b;
    classDef evidence fill:#e9f4ec,stroke:#2f6f54,color:#1f4c39;
    classDef challenge fill:#fbf2ec,stroke:#9c5b38,color:#5b3522;
    class Root,QF,QP,QM,QR,Thesis,Request,Test,Paragraph active;
    class Fact,Doc,Event,Rule evidence;
    class Counter challenge;
```

### 5.2 Como uma tese ganha força ou é descartada

```mermaid
flowchart TB
    Candidate["Teses candidatas"] --> Evidence["Força documental"]
    Candidate --> Law["Força jurídica"]
    Candidate --> Fit["Relação com o problema principal"]
    Candidate --> Objection["Melhor objeção"]
    Candidate --> Contamination["Risco de enfraquecer uma tese melhor"]
    Evidence --> Council["Helena + Cícero"]
    Law --> Council
    Fit --> Council
    Objection --> Council
    Contamination --> Council
    Council --> Role{"Como a tese será usada?"}
    Role --> Primary["Principal"]
    Role --> Subsidiary["Subsidiária"]
    Role --> Reserve["Reserva para uma situação específica"]
    Role --> Exclude["Não usar"]
    Primary --> Architecture["Estrutura final da peça"]
    Subsidiary --> Architecture
    Reserve --> Trigger["Fato que autoriza o uso"]
    Trigger --> Architecture
    Exclude --> Record["Motivo preservado"]

    classDef active fill:#e8f1ef,stroke:#395c60,color:#21383b;
    classDef human fill:#fff4d8,stroke:#9a6b18,color:#4b370d;
    classDef blocker fill:#fdecea,stroke:#a33b2b,color:#64251b;
    class Candidate,Evidence,Law,Fit,Objection,Contamination,Role,Primary,Subsidiary,Reserve,Trigger,Architecture active;
    class Council human;
    class Exclude,Record blocker;
```

## 6. Como a FORJA aprofunda o diagnóstico do caso

### 6.1 A petição como resposta planejada para um problema concreto

```mermaid
flowchart TD
    Command["Comando recebido"] --> Mess["Situação processual complexa"]
    Mess --> Problem["Problema principal<br/>situação atual, resultado pretendido e limites"]
    Problem --> Diagnosis["Diagnóstico<br/>causas prováveis e explicações alternativas"]
    Diagnosis --> Requirements["O que a solução precisa respeitar<br/>direito, provas, prazo, leitor e limites"]
    Requirements --> Options["Soluções jurídicas possíveis"]
    Options --> Select["Comparação e escolha"]
    Select --> Mechanism["Por que a solução escolhida pode funcionar"]
    Mechanism --> Direct["Resultado concreto esperado"]
    Direct --> Validate{"Atende aos requisitos<br/>e resiste à objeção?"}
    Validate -->|"não"| Reopen["Reabrir diagnóstico,<br/>alternativa ou restrição negociável"]
    Reopen --> Diagnosis
    Reopen --> Options
    Validate -->|"sim"| Draft["Detalhar tese, prova,<br/>pedido e forma visual"]
    Draft --> Observe["Plano de protocolo, acompanhamento e caminho alternativo"]
    Observe --> Learn["Registro do que foi feito,<br/>do resultado e dos limites encontrados"]

    classDef shadow fill:#fbf2ec,stroke:#9c5b38,color:#5b3522,stroke-width:2px;
    classDef planned fill:#f0f1f3,stroke:#707078,color:#3e3e44,stroke-dasharray:5 4;
    class Command,Mess,Problem,Diagnosis,Requirements,Options,Select,Mechanism,Direct,Validate,Reopen,Draft shadow;
    class Observe,Learn planned;
```

### 6.2 Requisitos e alternativas

```mermaid
flowchart LR
    subgraph Req["Quatro grupos de requisitos"]
        Functional["Resultado pretendido<br/>o que a peça precisa alcançar"]
        Reader["Leitor<br/>clareza e ordem para decidir"]
        Boundary["Condições não negociáveis<br/>lei, prazo, competência e prova"]
        Restriction["Restrições negociáveis<br/>extensão, ordem e profundidade"]
    end
    subgraph Alternatives["Espaço de solução"]
        Vehicle["Medida processual adequada"]
        Thesis["Tese principal e caminhos alternativos"]
        Evidence["Forma de apresentar e provar os fatos"]
        Composition["Ordem da narrativa e recursos visuais"]
        Execution["Protocolo e acompanhamento"]
    end
    Functional --> Compare["Comparação pelos mesmos critérios"]
    Reader --> Compare
    Boundary --> Compare
    Restriction --> Compare
    Vehicle --> Compare
    Thesis --> Compare
    Evidence --> Compare
    Composition --> Compare
    Execution --> Compare
    Compare --> Choice["Solução escolhida<br/>motivo e condição para mudar de caminho"]

    classDef shadow fill:#fbf2ec,stroke:#9c5b38,color:#5b3522;
    classDef evidence fill:#e9f4ec,stroke:#2f6f54,color:#1f4c39;
    class Functional,Reader,Boundary,Restriction shadow;
    class Vehicle,Thesis,Evidence,Composition,Execution,Compare,Choice evidence;
```

### 6.3 A profundidade da análise varia conforme o caso

```mermaid
flowchart LR
    Classify{"Complexidade do caso"}
    Classify -->|"questão única<br/>baixo volume"| Light["ANÁLISE ESSENCIAL<br/>núcleo, requisitos essenciais,<br/>alternativa considerada e validação curta"]
    Classify -->|"recurso, resposta<br/>ou múltiplas teses"| Full["ANÁLISE COMPLETA<br/>duas soluções comparadas,<br/>objeção mais forte e fontes conferíveis"]
    Classify -->|"alto impacto, muitos documentos,<br/>ciência ou cálculo"| Intensive["ANÁLISE APROFUNDADA<br/>mapa completo das questões, cenários<br/>e participação reforçada do conselho"]
    Light --> Gate["A mesma revisão jurídica final vale para todos"]
    Full --> Gate
    Intensive --> Gate

    classDef shadow fill:#fbf2ec,stroke:#9c5b38,color:#5b3522,stroke-width:2px;
    classDef active fill:#e8f1ef,stroke:#395c60,color:#21383b;
    class Classify,Light,Full,Intensive shadow;
    class Gate active;
```

## 7. Como a FORJA examina a peça da parte contrária

### 7.1 Busca de erros, contradições e pontos decisivos

```mermaid
flowchart TB
    Opponent["Peça adversária integral"] --> Claims["Separar alegações, pedidos e citações"]
    Claims --> Compare["Comparar com autos, decisões<br/>e manifestações anteriores"]
    Compare --> Citation["Citação existe, pertence ao julgado<br/>e sustenta a afirmação?"]
    Compare --> Contradiction["Contradição interna ou com documento?"]
    Compare --> Omission["Ponto decisivo omitido?"]
    Compare --> Conduct["Indício de conduta processual relevante?"]
    Citation --> Refute["Tentar demonstrar que o possível erro não existe"]
    Contradiction --> Refute
    Omission --> Refute
    Conduct --> Refute
    Refute --> Verdict{"Achado sobrevive?"}
    Verdict -->|"não"| Discard["Descartar e registrar o alarme incorreto"]
    Verdict -->|"sim, sem acusação"| Strategy["Usar na resposta e nos pedidos"]
    Verdict -->|"sim, exige acusação grave"| Cicero["Cícero ou responsável humano aprova a linguagem"]
    Cicero --> Strategy

    classDef active fill:#e8f1ef,stroke:#395c60,color:#21383b;
    classDef challenge fill:#fbf2ec,stroke:#9c5b38,color:#5b3522;
    classDef human fill:#fff4d8,stroke:#9a6b18,color:#4b370d;
    classDef blocker fill:#fdecea,stroke:#a33b2b,color:#64251b;
    class Opponent,Claims,Compare,Citation,Contradiction,Omission,Conduct,Refute,Verdict active;
    class Strategy challenge;
    class Cicero human;
    class Discard blocker;
```

## 8. Como as pesquisas fortalecem a petição

### 8.1 Jurisprudência oficial

```mermaid
flowchart LR
    Question["Afirmação jurídica que precisa de apoio"] --> Discover["Busca por palavras e por sentido"]
    Discover --> Candidate["Precedente candidato"]
    Candidate --> Official{"Fonte oficial ou<br/>arquivo oficial?"}
    Official -->|"não"| Lead["Somente pista de pesquisa"]
    Official -->|"sim"| Identity["Tribunal, órgão, processo,<br/>data e situação"]
    Identity --> Ratio["Trecho, fundamento central e alcance"]
    Ratio --> Limits["Diferenças do caso, analogia e limites"]
    Limits --> Claim["Ligar o precedente à afirmação exata"]
    Claim --> F7["Conferir novamente autoria, sentido e vigência"]
    F7 --> Use["Usar com precisão e sem exagero"]

    classDef research fill:#edf2f8,stroke:#315f8c,color:#243f5c;
    classDef evidence fill:#e9f4ec,stroke:#2f6f54,color:#1f4c39;
    classDef blocker fill:#fdecea,stroke:#a33b2b,color:#64251b;
    class Question,Discover,Candidate,Official,Identity,Ratio,Limits,Claim,F7 research;
    class Use evidence;
    class Lead blocker;
```

### 8.2 Apoio científico de outras áreas do conhecimento

```mermaid
flowchart TB
    Trigger["Questão importante de outra área<br/>saúde, psicologia, economia ou contabilidade"] --> Applicability{"A pesquisa científica pode ajudar?"}
    Applicability -->|"não"| NA["Registrar por que ela não é necessária"]
    Applicability -->|"sim"| RQ["Pergunta de pesquisa precisa"]
    RQ --> Protocol["Plano de pesquisa<br/>fontes, buscas e critérios de escolha"]
    Protocol --> Search["bases acadêmicas reconhecidas<br/>e repositórios científicos"]
    Search --> Identity["Confirmar autores, título, versão<br/>e eventual correção ou retirada"]
    Identity --> Appraisal["Examinar método, pessoas estudadas,<br/>riscos de distorção, resultado e limites"]
    Appraisal --> Contrary["Busca de evidência contrária"]
    Contrary --> Synthesis["Conclusão: apoio forte, misto, fraco,<br/>ausente ou inaplicável ao caso"]
    Synthesis --> Map["Afirmação científica → estudo → limite"]
    Map --> Audit["Revisão independente da pesquisa"]
    Audit --> Calibrated["Uso proporcional e com limites claros"]
    Audit --> Block["Impedir diagnóstico individual,<br/>relação de causa não demonstrada ou exagero"]

    classDef shadow fill:#fbf2ec,stroke:#9c5b38,color:#5b3522;
    classDef research fill:#edf2f8,stroke:#315f8c,color:#243f5c;
    classDef evidence fill:#e9f4ec,stroke:#2f6f54,color:#1f4c39;
    classDef blocker fill:#fdecea,stroke:#a33b2b,color:#64251b;
    class Trigger,Applicability,RQ,Protocol shadow;
    class Search,Identity,Appraisal,Contrary,Synthesis,Map,Audit research;
    class Calibrated,NA evidence;
    class Block blocker;
```

## 9. Da redação ao documento final

### 9.1 Como o conteúdo chega ao Word e ao PDF sem perder sentido

```mermaid
flowchart TB
    Blueprint["Plano da peça aprovado<br/>teses, ordem, fontes e pedidos"] --> Freeze["Fixar a versão do texto que será conferida"]
    Freeze --> Template["Modelo oficial do escritório Medina Osório<br/>ou peça anterior do caso"]
    Template --> Draft["Redação com a fonte de cada ponto importante indicada"]
    Draft --> VisualMap["Plano de apresentação<br/>caixas, quadros, tabelas e diagramas"]
    VisualMap --> Fidelity["Conferir se o conteúdo permanece igual<br/>no texto, no Word e no PDF"]
    Fidelity --> Vector["Preparar diagramas nítidos<br/>e compatíveis com o Word"]
    Vector --> PDF["Gerar o PDF final pelo Microsoft Word"]
    PDF --> Render["Gerar imagens de todas as páginas"]
    Render --> Inspect["Conferir cortes, sobreposições, letras,<br/>timbre, número de página, rodapé e dados do arquivo"]
    Inspect --> Pass{"Todas as páginas estão corretas e legíveis?"}
    Pass -->|"não"| Fix["Corrigir e marcar as versões anteriores como vencidas"]
    Fix --> Fidelity
    Pass -->|"sim"| Package["Arquivo liberado para revisão humana"]

    classDef active fill:#e8f1ef,stroke:#395c60,color:#21383b;
    classDef visual fill:#fbf2ec,stroke:#9c5b38,color:#5b3522;
    classDef evidence fill:#e9f4ec,stroke:#2f6f54,color:#1f4c39;
    classDef blocker fill:#fdecea,stroke:#a33b2b,color:#64251b;
    class Blueprint,Freeze,Template,Draft active;
    class VisualMap,Vector,PDF,Render,Inspect visual;
    class Fidelity,Pass,Package evidence;
    class Fix blocker;
```

## 10. Como a FORJA evita erros e conclusões apressadas

### 10.1 As revisões feitas antes da liberação

```mermaid
flowchart LR
    Candidate["Primeira versão da peça"] --> Formal["Dados formais<br/>nomes, números, datas,<br/>campos incompletos e formato"]
    Candidate --> Factual["Fatos<br/>afirmação, fonte, página e trecho"]
    Candidate --> Legal["Direito<br/>cabimento, regra, vigência e alcance"]
    Candidate --> Semantic["Coerência de sentido<br/>ato processual, tese e pedido"]
    Candidate --> Adversarial["Crítica contrária<br/>melhor objeção e ponto decisivo"]
    Candidate --> Meta["Revisão do raciocínio<br/>premissas, concordâncias e mudanças"]
    Formal --> Result["Lista de impedimentos, alertas e melhorias"]
    Factual --> Result
    Legal --> Result
    Semantic --> Result
    Adversarial --> Result
    Meta --> Result
    Result --> Council["Helena e Cícero<br/>decisões ligadas ao trecho correspondente"]
    Council --> Gate{"Há impedimento grave<br/>ou discordância importante?"}
    Gate -->|"sim"| Reopen["Voltar à etapa que originou o problema"]
    Gate -->|"não"| F8["Liberar para revisão da apresentação"]

    classDef audit fill:#edf2f8,stroke:#315f8c,color:#243f5c;
    classDef human fill:#fff4d8,stroke:#9a6b18,color:#4b370d;
    classDef blocker fill:#fdecea,stroke:#a33b2b,color:#64251b;
    class Candidate,Formal,Factual,Legal,Semantic,Adversarial,Meta,Result,Gate audit;
    class Council human;
    class Reopen blocker;
    style F8 fill:#e9f4ec,stroke:#2f6f54,color:#1f4c39;
```

### 10.2 O sistema não pode aprovar o próprio trabalho

```mermaid
flowchart TB
    Saved["Resultado registrado"] --> Resolve["Localizar novamente o texto e as fontes usados"]
    Resolve --> Hash{"O arquivo, sua origem e sua identificação conferem?"}
    Hash -->|"não"| Block["Impedimento grave<br/>fonte revogada, alterada ou sem origem clara"]
    Hash -->|"sim"| Rerun["Executar novamente as verificações"]
    Rerun --> Compare{"O novo resultado confirma<br/>o que havia sido registrado?"}
    Compare -->|"não"| Fraud["Impedir que o sistema aprove o próprio resultado"]
    Compare -->|"sim"| Layers["Repetir cinco verificações independentes<br/>e conferir cada página"]
    Layers --> Council{"Helena e Cícero aprovaram<br/>e indicaram os trechos examinados?"}
    Council -->|"não"| Structural["Resultado apenas estrutural<br/>revisão humana obrigatória"]
    Council -->|"sim"| Prospective{"Houve caso novo e testes capazes<br/>de revelar mudança de sentido?"}
    Prospective -->|"não"| Structural
    Prospective -->|"sim"| Eligible["A melhoria pode ser submetida<br/>à decisão humana de adoção"]

    classDef evidence fill:#e9f4ec,stroke:#2f6f54,color:#1f4c39;
    classDef blocker fill:#fdecea,stroke:#a33b2b,color:#64251b,stroke-width:2px;
    classDef shadow fill:#fbf2ec,stroke:#9c5b38,color:#5b3522;
    class Saved,Resolve,Hash,Rerun,Compare,Layers,Council,Prospective evidence;
    class Block,Fraud blocker;
    class Structural shadow;
    style Eligible fill:#fff4d8,stroke:#9a6b18,color:#4b370d;
```

## 11. Como medir se a FORJA realmente melhorou a peça

### 11.1 Oito aspectos avaliados separadamente

```mermaid
flowchart LR
    Plan["Plano do caso elaborado antes da redação"] --> PDI["Definição do problema<br/>o problema está claro e delimitado?"]
    Plan --> DCI["Coerência do diagnóstico<br/>as causas explicam o problema?"]
    Plan --> AQI["Qualidade das alternativas<br/>foram comparadas soluções realmente diferentes?"]
    Plan --> RTI["Respeito aos requisitos<br/>a solução cumpre direito, prova, prazo e objetivo?"]
    Plan --> MSI["Clareza do caminho escolhido<br/>está explicado por que a solução pode funcionar?"]
    Plan --> VSI["Força da conferência<br/>a solução resiste à melhor objeção?"]
    Plan --> CDI["Controle das informações<br/>cada questão usa somente o material necessário?"]
    Plan --> LVI["Qualidade do aprendizado<br/>a correção humana gerou uma lição útil?"]
    PDI --> Gate{"Os aspectos essenciais atingem<br/>o mínimo necessário?"}
    DCI --> Gate
    RTI --> Gate
    VSI --> Gate
    AQI --> Review["Quadro completo para revisão humana"]
    MSI --> Review
    CDI --> Review
    LVI --> Review
    Gate -->|"não"| Bottleneck["Mostrar o ponto fraco<br/>sem escondê-lo em uma média geral"]
    Gate -->|"sim"| Review
    Review --> LegalGate["A revisão jurídica final continua independente"]

    classDef shadow fill:#fbf2ec,stroke:#9c5b38,color:#5b3522;
    classDef evidence fill:#e9f4ec,stroke:#2f6f54,color:#1f4c39;
    classDef blocker fill:#fdecea,stroke:#a33b2b,color:#64251b;
    class Plan,PDI,DCI,AQI,RTI,MSI,VSI,CDI,LVI,Gate,Review shadow;
    class LegalGate evidence;
    class Bottleneck blocker;
```

### 11.2 O que os primeiros casos revelaram

```mermaid
xychart-beta
    title "Problemas encontrados nos quatro primeiros casos examinados"
    x-axis ["Teste simples", "Raciocínio circular", "Caso já concluído", "Conselho pendente", "Fonte bloqueada"]
    y-axis "Casos" 0 --> 4
    bar [4, 3, 3, 3, 1]
```

Leitura: esses números mostram problemas encontrados durante a revisão; não são notas sobre a qualidade jurídica das peças. Os oito aspectos do novo método ainda não foram medidos porque os casos analisados já estavam prontos quando o método foi criado.

## 12. Entrega e gestão integrada

### 12.1 Escolha dos arquivos, entrega e atualização da gestão

```mermaid
sequenceDiagram
    participant F8 as Revisão da apresentação
    participant F9 as Preparação do material
    participant H as Revisão humana
    participant C as Canal de entrega
    participant F10 as Comprovação da entrega
    participant G as Gestão do escritório

    F8->>F9: Word e PDF aprovados e identificados
    F9->>F9: selecionar e conferir os arquivos exatos
    F9->>H: peça, relatório, fontes e pendências
    H-->>F9: versão aprovada ou correção
    F9->>C: arquivo exato autorizado
    C-->>F10: comprovante ou identificação segura do arquivo
    F10->>F10: conferir pacote, arquivo e evidência
    alt entrega confirmada
        F10->>G: concluída + prova da entrega + arquivos
    else sem evidência
        F10->>G: aguardando evidência e ainda não cumprida
    end
    G-->>F10: feedback humano e estado operacional
    F10->>F10: comparar com a versão humana e registrar aprendizado
```

## 13. O que já funciona e o que ainda está sendo acrescentado

### 13.1 A base atual, as melhorias em teste e os próximos passos

```mermaid
flowchart TB
    subgraph Current["FUNCIONAMENTO ATUAL · permanece intacto"]
        Queue["Gestão e fila"]
        Phases["Onze etapas e situação de cada trabalho"]
        Sources["Regimento, fontes e registros de conferência"]
        Draft["Modelo do escritório, Word, PDF e recursos visuais"]
        Delivery["Material para revisão, prova da entrega e gestão"]
    end
    subgraph Pilot["MELHORIAS EM TESTE · já disponíveis em casos escolhidos"]
        N4["Análise aprofundada<br/>perguntas, fontes, ciência, testes e coerência"]
        PsoValidator["Diagnóstico antes da redação<br/>problema, causas, alternativas e forma de conferir"]
        Context["Uma ficha para cada questão importante"]
    end
    subgraph Planned["PRÓXIMOS PASSOS · dependem de casos novos"]
        Prospective["Plano do caso registrado antes da redação"]
        Semantic["Testes mais fortes contra perda de sentido"]
        Value["Tempo, retrabalho, omissões<br/>e revisão humana comparados"]
        Promotion["Adoção apenas das verificações que provarem valor"]
    end
    Queue --> Phases --> Sources --> Draft --> Delivery
    Sources --> N4
    N4 --> PsoValidator
    PsoValidator --> Context
    Context -.-> Prospective
    Prospective --> Semantic --> Value --> Promotion
    Promotion -. "somente após evidência" .-> Phases

    classDef active fill:#e8f1ef,stroke:#395c60,color:#21383b,stroke-width:2px;
    classDef shadow fill:#fbf2ec,stroke:#9c5b38,color:#5b3522,stroke-width:2px;
    classDef planned fill:#f0f1f3,stroke:#707078,color:#3e3e44,stroke-dasharray:5 4;
    class Queue,Phases,Sources,Draft,Delivery active;
    class N4,PsoValidator,Context shadow;
    class Prospective,Semantic,Value,Promotion planned;
```

### 13.2 Como uma melhoria passa do teste para o uso regular

```mermaid
flowchart LR
    Shadow["Agora<br/>observar sem interferir"] --> Light["Caso novo<br/>análise essencial"]
    Light --> Full["Caso novo<br/>análise completa"]
    Full --> Intensive["Caso novo<br/>análise aprofundada"]
    Intensive --> Compare["Comparar erros, retrabalho<br/>e tempo com os casos anteriores"]
    Compare --> Council["Helena + Cícero + revisão humana"]
    Council --> Decision{"Ganho real sem<br/>sobrecarga ou falso bloqueio?"}
    Decision -->|"não"| Revise["Rever a melhoria ou mantê-la apenas em observação"]
    Decision -->|"sim"| Promote["Adotar somente<br/>as verificações comprovadamente úteis"]
    Revise --> Shadow
    Promote --> Monitor["Acompanhar novos erros<br/>e permitir retorno à versão anterior"]

    classDef shadow fill:#fbf2ec,stroke:#9c5b38,color:#5b3522;
    classDef planned fill:#f0f1f3,stroke:#707078,color:#3e3e44,stroke-dasharray:5 4;
    classDef human fill:#fff4d8,stroke:#9a6b18,color:#4b370d;
    class Shadow,Light,Full,Intensive,Compare,Revise planned;
    class Council,Decision human;
    class Promote,Monitor shadow;
```

## 14. Quem faz o quê

### 14.1 Responsabilidades ao longo do trabalho

Esta visão separa com clareza quem prepara, quem verifica e quem toma a decisão final.

```mermaid
flowchart LR
    subgraph Origin["Origem e gestão"]
        Demand["Demanda, prazo e responsável"]
        Command["Comando e anexos"]
        Queue["Fila operacional"]
    end
    subgraph Deterministic["Controles automáticos e conferíveis"]
        Reconcile["Conferir a demanda e a situação real"]
        Ingest["Organizar os documentos e apontar o que falta"]
        Sources["Confirmar tribunal, regimento, leis e fontes"]
        Gates["Revisar fatos, direito, coerência e apresentação"]
        Package["Preparar a revisão humana e comprovar a entrega"]
    end
    subgraph Intelligence["Inteligência jurídica"]
        Classify["Definir o tipo de peça, a urgência e o risco"]
        Diagnose["Delimitar o problema e comparar caminhos possíveis"]
        Research["Pesquisar fundamentos jurídicos e científicos"]
        Draft["Redigir teses, respostas e pedidos"]
    end
    subgraph Council["Conselho independente"]
        Helena["Helena · estratégia, explicações alternativas e consequências"]
        Cicero["Cícero · direito, medida processual e limites"]
    end
    subgraph Human["Decisão humana"]
        Igor["Igor · direção e exceções"]
        Fabio["Fábio · revisão jurídica final"]
    end

    Demand --> Reconcile
    Command --> Ingest
    Queue --> Reconcile
    Reconcile --> Ingest --> Classify --> Sources --> Diagnose
    Diagnose --> Helena
    Diagnose --> Cicero
    Helena --> Research
    Cicero --> Research
    Research --> Draft --> Gates
    Gates -->|"impedimento grave"| Diagnose
    Gates -->|"aprovado"| Igor --> Fabio --> Package
    Package --> Queue

    classDef active fill:#e8f1ef,stroke:#395c60,color:#21383b;
    classDef research fill:#edf2f8,stroke:#315f8c,color:#243f5c;
    classDef human fill:#fff4d8,stroke:#9a6b18,color:#4b370d;
    class Demand,Command,Queue,Reconcile,Ingest,Sources,Gates,Package active;
    class Classify,Diagnose,Research,Draft research;
    class Helena,Cicero,Igor,Fabio human;
```

### 14.2 Como demandas de diferentes canais entram no mesmo fluxo

```mermaid
sequenceDiagram
    participant O as "Origem da demanda"
    participant G as "Gestão do escritório"
    participant F0 as "Etapa 1 · Conferir a demanda"
    participant C as "Pasta do caso"
    participant F1 as "Organização dos documentos"
    participant S as "Registro do andamento"

    O->>G: e-mail, WhatsApp/Hermes ou inclusão manual
    G->>F0: demanda, prazo, responsável e situação
    F0->>C: localizar comando e anexos
    C-->>F0: encontrados, ausentes ou conflitantes
    F0->>S: registrar vínculo e estado real
    F0->>F1: entrada reconciliada
    F1->>C: listar os documentos, identificá-los e verificar o que falta
    F1->>F1: procurar instruções ocultas e arquivos inválidos
    alt anexo crítico ou origem conflitante
        F1->>S: registrar impedimento e pendência específica
        S-->>G: próxima ação concreta
    else conjunto de documentos íntegro
        F1->>S: registrar conjunto de documentos aprovado
        S-->>G: próxima etapa e horário da atualização
    end
```

### 14.3 Tribunal, regimento, prazo e fontes mínimas

```mermaid
flowchart TD
    Case["Número CNJ, endereçamento e decisões"] --> Court["Identificar tribunal e órgão"]
    Court --> Rules{"Regimento integral e atualizado existe?"}
    Rules -->|"não"| Obtain["Obter consolidação oficial e emendas"]
    Obtain --> Rules
    Rules -->|"sim"| General["Consultar Estatuto OAB e LOMAN"]
    General --> Deadline["Contagem de prazo por duas verificações"]
    Deadline --> Holiday["Calendário, dias úteis, feriados e marco inicial"]
    Holiday --> Corpus["Ler a decisão questionada, as peças anteriores e os autos relevantes"]
    Corpus --> Critical{"Fonte crítica ou ato impugnado ausente?"}
    Critical -->|"sim"| Block["Impedimento grave<br/>não redigir versão pronta para protocolo"]
    Critical -->|"não"| Question["Resumir em uma frase o que o julgador precisa decidir"]
    Question --> Blueprint["Liberar o planejamento com a sequência dos atos conferida"]

    classDef evidence fill:#e9f4ec,stroke:#2f6f54,color:#1f4c39;
    classDef blocker fill:#fdecea,stroke:#a33b2b,color:#64251b;
    class Case,Court,Rules,Obtain,General,Deadline,Holiday,Corpus,Critical,Question,Blueprint evidence;
    class Block blocker;
```

## 15. Como versões e arquivos são preservados

### 15.1 Uma tentativa com erro não apaga a última versão válida

```mermaid
sequenceDiagram
    participant R as "Responsável pelo fluxo"
    participant K as "Regras da etapa"
    participant A as "Tentativa isolada"
    participant V as "Revisor independente"
    participant M as "Registro dos arquivos aprovados"
    participant E as "Histórico do caso"

    R->>K: ler documentos necessários, resultado esperado e verificações
    K-->>R: regras da etapa confirmadas
    R->>A: abrir uma nova tentativa identificada
    A->>A: trabalhar sem alterar a última versão válida
    A->>V: resultado, fontes e identificação dos arquivos
    alt resultado inválido ou verificação reprovada
        V-->>R: problemas encontrados e etapa responsável
        R->>E: registrar falha sem substituir versão válida
    else saída válida
        V->>M: registrar os arquivos aprovados
        M->>E: registrar a mudança no histórico
        E-->>R: autorizar a próxima etapa
    end
```

### 15.2 O que fica guardado na pasta de cada caso

```mermaid
flowchart TB
    Case["Pasta do caso"] --> State["Andamento<br/>etapa, impedimentos e provas da entrega"]
    Case --> Runs["Tentativas anteriores preservadas"]
    Case --> Context["Documentos, fatos, afirmações e questões"]
    Case --> Opinions["Pareceres de Helena e Cícero"]
    Case --> Research["Fontes jurídicas e pesquisas científicas"]
    Case --> Production["Texto, Word, PDF e imagens das páginas"]
    Case --> Audit["Revisões, testes e melhor crítica contrária"]
    Case --> Package["Relação dos arquivos preparados para revisão"]
    Case --> Delivery["Comprovante, comparação e aprendizado"]
    Production --> Visual["Plano de apresentação e diagramas nítidos"]
    Visual --> Pages["Todas as páginas conferidas"]
    Package --> Selected["arquivo selecionado = arquivo auditado"]
    Selected --> Delivery

    classDef active fill:#e8f1ef,stroke:#395c60,color:#21383b;
    classDef evidence fill:#e9f4ec,stroke:#2f6f54,color:#1f4c39;
    class Case,State,Runs,Context,Opinions,Research,Production,Visual,Pages active;
    class Audit,Package,Selected,Delivery evidence;
```

### 15.3 Cada afirmação importante deve levar à sua fonte

```mermaid
flowchart LR
    Source["Documento ou fonte oficial"] --> Locator["Número, página, trecho, data e identificação do arquivo"]
    Locator --> Fact["Fato, evento ou afirmação"]
    Fact --> Confidence["O que está confirmado, condicionado ou incerto"]
    Contrary["Fonte ou explicação contrária"] --> Confidence
    Confidence --> Thesis["Tese principal, subsidiária ou reserva"]
    Thesis --> Paragraph["Parágrafo com função definida"]
    Paragraph --> Request["Pedido ou consequência processual"]
    Request --> Test["Pergunta objetiva para conferir o pedido"]
    Test --> Audit{"Sobrevive à melhor objeção?"}
    Audit -->|"não"| Rework["Reabrir fato, fonte ou desenho da tese"]
    Audit -->|"sim"| Eligible["Elegível para revisão humana"]

    classDef evidence fill:#e9f4ec,stroke:#2f6f54,color:#1f4c39;
    classDef challenge fill:#fbf2ec,stroke:#9c5b38,color:#5b3522;
    class Source,Locator,Fact,Confidence,Thesis,Paragraph,Request,Test evidence;
    class Contrary,Audit,Rework challenge;
    style Eligible fill:#fff4d8,stroke:#9a6b18,color:#4b370d;
```

## 16. Gestão do escritório, prazos e canais

### 16.1 Como a FORJA atualiza o painel sem apagar o histórico

```mermaid
sequenceDiagram
    participant F as "FORJA"
    participant E as "Histórico do caso"
    participant S as "Atualização da gestão"
    participant Side as "Registro auxiliar da FORJA"
    participant Base as "Demandas e ajustes humanos"
    participant P as "Painel do escritório"

    F->>E: registrar etapa, impedimento, material ou entrega
    E->>S: informar caso, demanda, ordem e arquivos
    S->>S: confirmar a ligação e a ordem dos registros
    alt informação repetida ou produzida em teste
        S-->>E: ignorar sem alterar a situação real
    else informação nova e válida
        S->>Side: atualizar o registro auxiliar com segurança
        Side->>Base: reunir as informações sem apagar o histórico
        Base->>P: mostrar etapa, impedimentos, revisão visual e próxima ação
        P-->>S: confirmar versão e horário da atualização
    end
```

### 16.2 Gestão de prazos sem confundir lembrete com prova

```mermaid
stateDiagram-v2
    state "Data apenas mencionada" as prazo_mencionado
    state "Data a conferir" as a_conferir
    state "Prazo confirmado" as prazo_confirmado
    state "Prazo ainda indefinido" as sem_prazo_definido
    state "Alerta: faltam 48 horas" as alerta_48h
    state "Trabalho em andamento" as em_execucao
    state "Peça pronta para revisão" as pronta_para_revisao
    state "Aguardando envio ou protocolo" as aguardando_envio
    state "Entrega comprovada" as cumprida
    state "Prazo vencido sem prova de entrega" as vencida
    state "Providência após o vencimento" as contingencia
    [*] --> prazo_mencionado
    prazo_mencionado --> a_conferir: "data extraída de mensagem ou documento"
    a_conferir --> prazo_confirmado: "marco, regra, calendário e responsável conferidos"
    a_conferir --> sem_prazo_definido: "não há base suficiente"
    prazo_confirmado --> alerta_48h: "janela crítica"
    prazo_confirmado --> em_execucao: "trabalho iniciado"
    alerta_48h --> em_execucao
    em_execucao --> pronta_para_revisao: "peça e revisão visual concluídos"
    pronta_para_revisao --> aguardando_envio: "revisão ainda não é entrega"
    aguardando_envio --> cumprida: "protocolo ou envio comprovado"
    aguardando_envio --> vencida: "prazo passou sem evidência"
    sem_prazo_definido --> a_conferir: "nova informação"
    vencida --> contingencia: "ação humana e registro do ocorrido"
    cumprida --> [*]
    contingencia --> [*]
```

### 16.3 Entrada por e-mail, WhatsApp/Hermes e validação humana

```mermaid
flowchart TD
    Email["E-mail<br/>orientação, anexos e conversa relacionada"] --> Normalize["Registrar a demanda sem alterar a mensagem original"]
    Whats["WhatsApp ou Hermes<br/>informação essencial ou áudio transcrito"] --> Normalize
    Manual["Inclusão manual · decisão e contexto"] --> Normalize
    Normalize --> Identity{"Cliente, caso, tipo de peça e prazo estão claros?"}
    Identity -->|"não"| Clarify["Validação por e-mail, WhatsApp ou decisão humana registrada"]
    Clarify --> Identity
    Identity -->|"sim"| Link["Ligar a demanda à pasta correta do caso"]
    Link --> Intake["Conferir a entrada e organizar os documentos"]
    Intake --> Draft["Executar as etapas da FORJA"]
    Draft --> Review["Igor e Fábio revisam a versão correta"]
    Review --> Channel{"Canal autorizado?"}
    Channel -->|"não"| Local["Manter o material no escritório<br/>sem registrar entrega inexistente"]
    Channel -->|"sim"| Deliver["Criar rascunho ou enviar manualmente"]
    Deliver --> Proof["Guardar o rascunho, a conversa,<br/>o protocolo ou o comprovante"]
    Proof --> Management["Atualizar a gestão como concluída"]

    classDef active fill:#e8f1ef,stroke:#395c60,color:#21383b;
    classDef human fill:#fff4d8,stroke:#9a6b18,color:#4b370d;
    classDef blocker fill:#fdecea,stroke:#a33b2b,color:#64251b;
    class Email,Whats,Manual,Normalize,Link,Intake,Draft,Proof,Management active;
    class Clarify,Review,Channel human;
    class Local blocker;
```

## 17. Verificações jurídicas mais profundas

### 17.1 Coerência dos termos, das datas e dos cálculos

```mermaid
flowchart TD
    Sources["Decisões, documentos e dispositivos"] --> Canon["Nome correto de cada ato processual"]
    Canon --> Scan["Conferir texto, quadros, diagramas e pedidos"]
    Scan --> Conflict{"O mesmo evento recebeu qualificações incompatíveis?"}
    Conflict -->|"sim"| Explained{"Contraste deliberado e explicado?"}
    Explained -->|"não"| P0["Impedimento grave<br/>o texto pode ter mudado o sentido do ato"]
    Explained -->|"sim"| Time["Regras aplicáveis em cada momento"]
    Conflict -->|"não"| Time
    Time --> Act["Ato juridicamente relevante"]
    Act --> Date["Data comprovada"]
    Date --> Regime["Regra de transição e regime aplicável"]
    Regime --> Quant{"Há questão mensurável?"}
    Quant -->|"não"| Global["Conferir a coerência do documento inteiro"]
    Quant -->|"sim"| Formula["Definir fórmula, unidades e valores conhecidos"]
    Formula --> Range["Apresentar uma faixa objetiva<br/>ou explicar por que o cálculo ainda não é possível"]
    Range --> Global
    P0 --> Reopen["Voltar à confirmação das fontes<br/>e ao planejamento da estratégia"]

    classDef audit fill:#edf2f8,stroke:#315f8c,color:#243f5c;
    classDef blocker fill:#fdecea,stroke:#a33b2b,color:#64251b;
    class Sources,Canon,Scan,Conflict,Explained,Time,Act,Date,Regime,Quant,Formula,Range,Global audit;
    class P0,Reopen blocker;
```

### 17.2 Ciclo de confiança de uma fonte acadêmica

```mermaid
stateDiagram-v2
    state "Estudo encontrado" as descoberta
    state "Identidade ainda não confirmada" as identidade_pendente
    state "Identidade confirmada" as identidade_confirmada
    state "Estudo rejeitado" as rejeitada
    state "Incluído na pesquisa" as incluida
    state "Excluído por critério declarado" as excluida
    state "Conteúdo ainda não lido" as conteudo_pendente
    state "Somente o resumo foi lido" as apenas_resumo
    state "Conteúdo necessário conferido" as conteudo_verificado
    state "Método e limites avaliados" as avaliacao_metodologica
    state "Situação editorial conferida" as status_editorial
    state "Pode ser usado com limites" as utilizavel_com_limites
    state "Correção exige nova avaliação" as corrigida_reavaliar
    state "Estudo retirado ou inválido" as retratada_bloqueada
    state "Ligado à afirmação da peça" as mapeada_a_afirmacao
    state "Uso apenas secundário" as uso_limitado
    [*] --> descoberta
    descoberta --> identidade_pendente
    identidade_pendente --> identidade_confirmada: "autores, título e versão conferem"
    identidade_pendente --> rejeitada: "dados não correspondem ao estudo"
    identidade_confirmada --> incluida: "critérios atendidos"
    identidade_confirmada --> excluida: "motivo explícito"
    incluida --> conteudo_pendente
    conteudo_pendente --> apenas_resumo
    conteudo_pendente --> conteudo_verificado
    conteudo_verificado --> avaliacao_metodologica
    avaliacao_metodologica --> status_editorial
    status_editorial --> utilizavel_com_limites
    status_editorial --> corrigida_reavaliar
    status_editorial --> retratada_bloqueada
    corrigida_reavaliar --> avaliacao_metodologica
    utilizavel_com_limites --> mapeada_a_afirmacao
    apenas_resumo --> uso_limitado: "não sustenta sozinho uma afirmação decisiva"
    uso_limitado --> mapeada_a_afirmacao
    rejeitada --> [*]
    excluida --> [*]
    retratada_bloqueada --> [*]
    mapeada_a_afirmacao --> [*]
```

### 17.3 A FORJA também questiona o próprio raciocínio

```mermaid
flowchart TD
    Questions["Questões, requisitos e pontos que devem ser respondidos"] --> Tests["Perguntas objetivas e testes de sentido"]
    Tests --> Freeze["Fixar os critérios antes da versão final"]
    Freeze --> Candidate["Primeira versão completa"]
    Candidate --> Mechanical["Nomes, números, fontes, prazos e pedidos"]
    Candidate --> Semantic["Ato processual, tese, negação, ressalva e sentido do conjunto"]
    Candidate --> Adversarial["Melhor objeção e explicação rival"]
    Candidate --> Meta["Premissas, concordâncias automáticas,<br/>mudanças de posição e distorção dos indicadores"]
    Mechanical --> Result["Resultado de cada verificação<br/>sem esconder um problema grave em uma média"]
    Semantic --> Result
    Adversarial --> Result
    Meta --> Result
    Result --> Pass{"Todas as verificações obrigatórias foram aprovadas?"}
    Pass -->|"não"| Cause{"O problema está na fonte, na estratégia,<br/>na redação ou na apresentação?"}
    Cause --> Reopen["Voltar somente à etapa que causou o problema"]
    Reopen --> Tests
    Pass -->|"sim"| F8["Liberar para revisão visual"]

    classDef audit fill:#edf2f8,stroke:#315f8c,color:#243f5c;
    classDef blocker fill:#fdecea,stroke:#a33b2b,color:#64251b;
    class Questions,Tests,Freeze,Candidate,Mechanical,Semantic,Adversarial,Meta,Result,Pass,Cause audit;
    class Reopen blocker;
    style F8 fill:#e9f4ec,stroke:#2f6f54,color:#1f4c39;
```

### 17.4 O que a revisão humana ensina ao sistema

```mermaid
flowchart LR
    AI["Versão produzida pela FORJA"] --> Diff["Comparação com a versão humana aprovada"]
    Human["Versão revisada"] --> Diff
    Diff --> Cause{"Qual foi a causa real?"}
    Cause --> Fact["Fato ou prova"]
    Cause --> Law["Direito ou fonte"]
    Cause --> Plan["Diagnóstico ou estratégia"]
    Cause --> Meaning["Terminologia ou perda de sentido"]
    Cause --> Visual["Composição ou legibilidade"]
    Cause --> Style["Preferência de voz"]
    Fact --> Structural{"O mesmo tipo de erro pode ocorrer em outros casos?"}
    Law --> Structural
    Plan --> Structural
    Meaning --> Structural
    Visual --> Structural
    Structural -->|"sim"| Fixture["Criar um teste baseado na correção"]
    Fixture --> Review["Revisão humana do novo teste"]
    Review --> Battery["Aplicar o teste em trabalhos futuros"]
    Structural -->|"não"| Memory["Registrar como aprendizado específico do caso"]
    Style --> Preference["Registrar a preferência sem transformá-la em regra geral"]
```

## 18. Como escolher e conferir recursos visuais

### 18.1 Escolha do recurso visual conforme a necessidade do leitor

Os trabalhos reais mostram quatro formas especialmente úteis: cartões para números importantes, linha do tempo para a sequência dos fatos, árvore para decisões e convergência para fundamentos independentes. Um recurso visual só permanece na peça quando facilita a leitura e mantém todo o texto legível.

```mermaid
flowchart TD
    Need{"Que dificuldade do leitor precisa ser reduzida?"}
    Need -->|"memorizar números"| Cards["Cartões-síntese · até quatro dados decisivos"]
    Need -->|"entender ordem temporal"| Timeline["Linha do tempo · fatos, marcos e consequência"]
    Need -->|"comparar alternativas"| Table["Tabela · critérios constantes e células curtas"]
    Need -->|"seguir decisão"| Tree["Árvore · condição, bifurcação e resultado"]
    Need -->|"ver fundamentos independentes"| Converge["Convergência · múltiplas rotas ao mesmo pedido"]
    Need -->|"ver magnitude"| Chart["Gráfico · escala, unidade e fonte explícitas"]
    Cards --> Test["Teste de necessidade, precisão e legibilidade"]
    Timeline --> Test
    Table --> Test
    Tree --> Test
    Converge --> Test
    Chart --> Test
    Test --> Useful{"Reduz esforço sem alterar o sentido?"}
    Useful -->|"não"| Remove["Remover ou simplificar"]
    Useful -->|"sim"| VisualMap["Registrar no plano de apresentação da peça"]

    classDef visual fill:#fbf2ec,stroke:#9c5b38,color:#5b3522;
    classDef evidence fill:#e9f4ec,stroke:#2f6f54,color:#1f4c39;
    class Need,Cards,Timeline,Table,Tree,Converge,Chart,Test,Useful visual;
    class VisualMap evidence;
    style Remove fill:#fdecea,stroke:#a33b2b,color:#64251b;
```

### 18.2 Como impedir cortes, sobreposições e letras pequenas

```mermaid
flowchart TD
    Text["Texto jurídico aprovado para composição"] --> Map["Plano de apresentação<br/>tipo, função, posição e conteúdo"]
    Map --> Generate["Gerar tabela, diagrama nítido ou gráfico"]
    Generate --> Geometry["Conferir caixas, margens e tamanho mínimo das letras"]
    Geometry -->|"falha"| Redesign["Redesenhar; nunca apenas diminuir as letras"]
    Redesign --> Generate
    Geometry -->|"passa"| Vector["Preparar uma imagem nítida e compatível com o Word"]
    Vector --> Word["Inserir no modelo oficial do escritório"]
    Word --> PDF["PDF final pelo Microsoft Word"]
    PDF --> Pages["Gerar imagens de todas as páginas"]
    Pages --> Inspect["Examinar cada página em tamanho normal e ampliado"]
    Inspect --> Checks["Texto, cortes, sobreposição, contraste,<br/>timbre, número de página e rodapé"]
    Checks --> Pass{"Página e diagrama preservam leitura e sentido?"}
    Pass -->|"não"| Origin{"Falha de conteúdo ou composição?"}
    Origin -->|"conteúdo"| Map
    Origin -->|"composição"| Generate
    Pass -->|"sim"| Hash["Identificar a nova versão e liberá-la para revisão"]

    classDef visual fill:#fbf2ec,stroke:#9c5b38,color:#5b3522;
    classDef evidence fill:#e9f4ec,stroke:#2f6f54,color:#1f4c39;
    classDef blocker fill:#fdecea,stroke:#a33b2b,color:#64251b;
    class Text,Map,Generate,Geometry,Vector,Word,PDF,Pages,Inspect,Checks,Pass visual;
    class Hash evidence;
    class Redesign,Origin blocker;
```

## 19. Leitura final e roteiro de uso

### 19.1 Todo o funcionamento em uma única sequência

```mermaid
flowchart LR
    Intake["Demanda recebida"] --> Trust["Documentos conferidos"]
    Trust --> Problem["Problema bem definido"]
    Problem --> Alternatives["Alternativas comparadas"]
    Alternatives --> Thesis["Teses, fundamentos e pedidos ligados às fontes"]
    Thesis --> Challenge["Argumentos contrários, ciência e melhor objeção"]
    Challenge --> Draft["Peça limpa e persuasiva"]
    Draft --> Audit["Revisão jurídica, factual, de sentido e de apresentação"]
    Audit --> Human["Decisão humana"]
    Human --> Delivery["Entrega comprovada"]
    Delivery --> Management["Gestão atualizada"]
    Management --> Learn["Aprendizado organizado por causa"]
    Learn -. "melhora comprovada" .-> Problem

    classDef active fill:#e8f1ef,stroke:#395c60,color:#21383b;
    classDef human fill:#fff4d8,stroke:#9a6b18,color:#4b370d;
    classDef evidence fill:#e9f4ec,stroke:#2f6f54,color:#1f4c39;
    class Intake,Trust,Problem,Alternatives,Thesis,Challenge,Draft,Audit,Management,Learn active;
    class Human human;
    class Delivery evidence;
```

A FORJA controla a entrada da demanda, as fontes, a redação, as revisões, a apresentação, o material entregue e a prova da entrega. As melhorias em teste acrescentam uma ligação mais clara entre perguntas, fatos, fundamentos, teses e pedidos. Também exigem que o problema seja bem definido antes da redação e que outras soluções possíveis sejam comparadas.

Para uma leitura rápida, use as seções 1, 2, 12 e 19. Para compreender a inteligência jurídica, use 4 a 8 e 17. Para operação e integração com o escritório, use 14 a 16. Para auditoria e comunicação visual jurídica, use 9, 10 e 18.

O princípio final permanece: **informação bem organizada, fontes fáceis de conferir, alternativas reais e disposição para rever a primeira conclusão.**
