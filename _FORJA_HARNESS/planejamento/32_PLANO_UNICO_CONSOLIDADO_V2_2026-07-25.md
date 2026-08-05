# 32 — Plano único consolidado v2: cocrição, identidade e precedentes

**Data:** 25/07/2026.  
**Estado:** pesquisa e planejamento revisados. **Não autoriza implementação nem envio externo.**

**Substitui como roteiro de execução:** `31_PLANO_UNICO_CONSOLIDADO_2026-07-25.md`. O documento 31 permanece preservado como registro da consolidação anterior. Os documentos 26 a 30 continuam como visão longa, requisitos, evidência de origem e backlog experimental; em caso de conflito operacional, prevalece este documento.

**Decisão:** manter a arquitetura Lite do documento 31, mas corrigir seis premissas antes de qualquer implementação:

1. a consulta ao advogado é uma etapa de **cocrição e decisão**, não mera projeção de perguntas;
2. silêncio, resposta estratégica e prova factual têm efeitos diferentes;
3. o mapa do destinatário exige fontes complementares; o TeiaJus não contém sozinho todos os dados;
4. pesquisa topológica de precedentes não deve ser chamada de jurimetria;
5. a identidade Medina exige corpus com autoria e proveniência curadas, não imitação da fala;
6. extensões de artefatos existentes dispensam novo tipo de artefato, mas **não dispensam versão de schema, migração aditiva e validação de consumidores**.

A solução continua pequena: **dois novos tipos de artefato de execução**, quatro extensões aditivas de contratos existentes e um corpus curatorial fora do caminho crítico de produção.

---

## 1. Resultado pretendido

A FORJA deve funcionar como parceiro intelectual do advogado responsável antes de redigir:

1. lê os autos e fontes disponíveis;
2. identifica o que já sabe, o que é inferência e o que depende de decisão humana;
3. pesquisa também a **cabeça do advogado**: objetivo, restrições, intuição do caso, risco aceitável e rota preferida;
4. apresenta alternativas reais, seus custos e a razão de descartar as demais;
5. pesquisa e verifica as autoridades adequadas ao destinatário;
6. registra a decisão humana;
7. só então produz um único texto;
8. preserva, na redação, o método argumentativo e o grau de sofisticação aceito pelo titular, sem fabricar uma persona.

O produto não é “uma IA que pergunta tudo” nem “uma IA que faz tudo sozinha”. É um ciclo de **investigação, confronto, escolha, verificação e redação** em que a máquina amplia o espaço de decisão e o advogado conserva as decisões que alteram a estratégia, a narrativa factual ou o risco do caso.

---

## 2. Linha de base verificada: o que existe e o que realmente falta

| Capacidade | Estado atual verificado | Lacuna que este plano cobre |
|---|---|---|
| Exploração F2-A | cem perguntas, estados `answered`, `blocked` e `not_applicable`; respostas factuais exigem `supportIds`; há perguntas sobre prevenção e ratio/obiter | seleção material, linguagem endereçada, iteração com o advogado e registro das decisões estratégicas |
| F4 | já existe definição da questão jurisdicional e há infraestrutura de pareceres | brief único com rotas, rejeições, consequência decisória e âncoras |
| F5/F7 | já há `source_ledger`, `verified_source_ledger`, checklist de citações e artefatos F5C para pesquisa científica extrajurídica | trilha reproduzível da pesquisa **jurídica**, resultados negativos e ficha profunda apenas das âncoras |
| TeiaJus | base viva com pesquisa de casos e camadas STJ; o agente anuncia 31 ações | o bridge da FORJA expõe superfície menor; composição atual, prevenção e íntegra decisiva exigem fontes e gates próprios |
| Identidade | `_MODELOS` não contém peças canônicas; o acervo possui centenas de DOCX de proveniências heterogêneas; há `forja_diff_docx.py`, feedback humano e classes de atribuição em `forja_learning.py` | inventário de autoria, seleção de corpus escrito, padrões estáveis e avaliação cega |
| Fontes administrativas | há dados de CEIS, CEAF, CNEP, CEPIM e acordos de leniência | esses registros são dados sancionatórios e de integridade, **não jurisprudência administrativa**; decisões de TCU, CGU/CRG, CADE, CVM, CNJ e CNMP exigem conectores ou coleta próprios |

Consequência arquitetural: não se deve criar um sistema paralelo, mas também não se deve declarar uma lacuna “resolvida” apenas porque uma pergunta, um campo genérico ou uma ação distante existe em outro subsistema.

---

## 3. Princípios não negociáveis

### 3.1 Verificação antes de persuasão

Nenhuma melhoria de assinatura pode reduzir os gates factuais e jurídicos. Citação, número, órgão, relator, composição, data, trecho, ratio e estado do precedente continuam sujeitos a fonte oficial e recomputação independente.

O CPC exige demonstração dos fundamentos determinantes e da adequação do precedente ao caso, bem como fundamentação para distinção ou superação; isso impede substituir análise por etiqueta ou escore. Regime jurídico e aderência factual são dimensões relacionadas, mas diferentes.

### 3.2 Identidade como método, não personificação

“Escrever como Medina” significa aproximar:

- forma de identificar a questão decisiva;
- movimento entre autoridade, isonomia e consequência;
- densidade doutrinária útil;
- modo de antecipar objeções;
- nível de precisão e acabamento que ele aceitaria assinar.

Não significa reproduzir cacoetes de fala, inserir vocabulário ornamental ou alegar autoria humana inexistente. A transcrição serve primeiro como corpus de **pensamento oral**. Só peças de autoria ou revisão atribuídas servem como evidência forte de estilo escrito.

### 3.3 Cocrição com responsabilidade epistêmica

Uma declaração do escritório pode definir objetivo, preferência, autorização ou leitura estratégica. Ela não prova, por si, fato externo do processo. O registro deve manter separadas:

- `record_evidence`: dado sustentado nos autos ou fonte oficial;
- `office_declaration`: declaração do advogado ou do escritório;
- `inference`: conclusão analítica ainda não confirmada;
- `unknown`: ponto material não resolvido.

### 3.4 Proporcionalidade

O custo da pesquisa e do fichamento cresce com a materialidade:

- precedentes de descoberta recebem metadados mínimos;
- precedentes citados recebem verificação de citação e vigência;
- precedentes-âncora recebem confronto profundo de ratio, fatos e operação;
- nenhuma peça recebe dossiês extensos sobre autoridades que não afetam a rota escolhida.

### 3.5 Sem pseudoprecisão

Não usar percentuais intuitivos, notas de aderência ou pesos arbitrários para simular certeza. Quando houver medida estatística, ela deve ter população, janela, denominador, incerteza e finalidade declarados. Quando não houver, usar categorias verificáveis e justificativa em linguagem natural.

---

## 4. Fluxo-alvo corrigido

```mermaid
flowchart LR
    F2A["F2-A: exploração dos autos"] --> F2B["F2-B: consulta dialética"]
    F2B --> D["Registro de decisões e pendências"]
    F3B["F3-B: mapa do destinatário"] --> F4["F4: signature brief"]
    D --> F4
    F4 --> F5["F5: pesquisa e verificação das âncoras"]
    F5 -->|"âncora válida"| F6["F6: um único draft"]
    F5 -->|"âncora rejeitada ou rota inviável"| F4
    F6 --> F7["F7/F7-B: auditoria, fidelidade e estilo"]
    F7 --> R["Revisão humana e entrega"]
```

O fluxo tem duas frentes paralelas antes da redação:

- **dialética:** compreender o caso junto com o advogado;
- **topológica:** compreender quem decide e quais autoridades realmente governam a controvérsia.

Uma não substitui a outra. O mapa do destinatário sem intenção do advogado produz estratégia tecnicamente informada, porém desalinhada. A intenção do advogado sem pesquisa topológica produz estratégia alinhada, porém abstrata.

---

## 5. F2-B — consulta dialética ao advogado responsável

### 5.1 O que a consulta deve produzir

A consulta não é um questionário integral. É uma seleção adaptativa das dúvidas que podem mudar:

- a identidade do produto;
- o objetivo do cliente;
- a tese ou a ordem das teses;
- a narrativa factual material;
- o pedido;
- a tolerância a risco;
- a pesquisa necessária;
- a escolha entre rotas plausíveis.

O alvo de cinco a doze perguntas é uma heurística editorial, não um gate. Caso simples pode exigir menos; caso complexo pode exigir rodadas sucessivas. A regra é **materialidade por pergunta**, não quantidade.

### 5.2 Filtros de admissão

Cada pergunta precisa passar por quatro filtros:

1. **não está respondida** nos autos, nas mensagens ou em fonte oficial acessível;
2. **pode mudar** decisão material do trabalho;
3. está endereçada à pessoa capaz de respondê-la ou decidir;
4. informa o efeito da ausência de resposta.

Pergunta que a FORJA poderia resolver pesquisando o próprio acervo é falha do sistema, não colaboração humana.

### 5.3 Efeito do silêncio

O plano 31 é corrigido neste ponto:

| Tipo de pergunta | Efeito de ausência de resposta |
|---|---|
| fato material, documento essencial ou identidade processual | bloqueia a alegação ou o produto dependente; nunca vira premissa protocolável |
| autorização, pedido, renúncia, reconhecimento ou exposição de risco | bloqueia a ação correspondente |
| objetivo do cliente ou escolha estratégica decisiva | mantém alternativas abertas e impede seleção final da rota |
| preferência não material de forma, prioridade ou apresentação | pode receber default explícito, reversível e visível |
| escolha estratégica não material | pode receber default apenas se a consulta tiver declarado a consequência e o risco |

Portanto, `default_on_silence` não é propriedade global. É decisão por pergunta e nunca converte ignorância em fato.

### 5.4 Resposta não é aceite automático

A resposta cumpre a função de fixação de escopo apenas quando efetivamente resolve os pontos materiais. Não haverá uma subfase F2-C separada, mas haverá um **registro explícito de decisão** dentro dos contratos existentes:

- pergunta;
- resposta literal ou síntese aprovada;
- autor e canal;
- natureza epistêmica;
- decisão produzida;
- artefatos afetados;
- pendência remanescente;
- data e versão.

Uma resposta parcial, ambígua ou lateral não fecha a questão.

### 5.5 Forma de interação

Um único e-mail consolidado é o padrão inicial, não uma ontologia rígida. Respostas podem chegar por e-mail, WhatsApp, áudio ou reunião e devem ser incorporadas ao mesmo ledger versionado.

No piloto:

- a FORJA gera minuta de consulta e destinatário sugerido;
- uma pessoa autorizada revisa e envia;
- o envio e a resposta recebem vínculo de proveniência;
- não há envio autônomo até existir autorização expressa, allowlist de destinatários internos e trilha de auditoria.

---

## 6. F3-B — mapa do destinatário com fontes separadas

### 6.1 Dois novos tipos de artefato

Mantêm-se os dois novos tipos de artefato de execução:

1. `F3_MAPA_DESTINATARIO.json`;
2. `F4_SIGNATURE_BRIEF.json`.

Cada um exigirá schema próprio, registro no catálogo, contrato de fase, validação cruzada, migração compatível e testes de consumidores. “Dois artefatos” não significa “zero schema”.

### 6.2 Conteúdo do mapa

O mapa deve separar campos e fontes:

| Bloco | Conteúdo | Fonte adequada |
|---|---|---|
| competência | órgão competente e fundamento | lei, regimento e autos |
| prevenção | existência, origem, processo relacionado e fundamento | autos, distribuição e regimento |
| composição atual | membros e data de conferência | página oficial atual do tribunal |
| posição individual | decisões do relator sobre a questão | íntegra oficial ou reprodução oficial verificável |
| posição colegiada | órgão, seção ou plenário competente | precedentes verificados |
| divergência | posições incompatíveis ou linhas distintas | conjunto comparável de decisões |
| rota recursal | via possível e pressupostos | lei, regimento e situação processual |

O campo `orgaoJulgador` do DataJud é metadado processual. Pode orientar a pesquisa, mas não prova composição atual nem prevenção. Espelho mensal ajuda na descoberta; íntegra e fonte oficial são necessárias para extrair fundamentos determinantes de uma âncora.

### 6.3 Topologia condicional

A ordem de busca deve seguir a competência e o problema concreto, não uma escada fixa. Outra turma da seção, seção ou Corte Especial só entra quando a estrutura do tribunal e a matéria tornarem esse nível relevante.

Prequestionamento não é o último degrau da topologia. É um ledger paralelo, derivado da decisão recorrida e da rota recursal projetada.

### 6.4 Perecibilidade

Cada dado mutável precisa de:

- `checkedAt`;
- `sourceId` ou URL oficial;
- `freshnessPolicy`;
- `status`: `confirmed`, `stale`, `unknown` ou `not_applicable`.

Dado vencido não é reutilizado silenciosamente. “Não apurado” é melhor que composição antiga apresentada como atual.

---

## 7. F4 — signature brief como centro único de decisão

O brief absorve o leque de teses e evita lugares concorrentes de decisão. Seus campos mínimos:

- questão decisiva;
- consequência jurídica e prática demonstrada nos autos;
- rotas realmente plausíveis;
- rota selecionada e responsável pela decisão;
- rotas rejeitadas e motivo;
- frase-mãe provisória;
- fatos e documentos decisivos por ID;
- precedentes-âncora candidatos por ID;
- melhor contra-argumento e resposta;
- conteúdo obrigatório e limites;
- pendências que impedem a redação.

“Exatamente três rotas” passa a ser orientação de exploração, não obrigação. O padrão é duas a quatro quando houver pluralidade real. Uma única rota é válida se as alternativas seriam artificiais; mais de quatro exige justificativa de complexidade.

O brief é uma decisão estruturada, não um sumário para expansão mecânica. F6 recebe a rota e os vínculos necessários, mas não deve transformar cada campo em subtítulo.

---

## 8. F5/F7 — precedentes estratégicos e auditáveis

### 8.1 Nome correto

O que o documento 31 chamou de “jurimetria de seleção” passa a chamar-se:

> **pesquisa topológica e estratégica de precedentes**

É recuperação, classificação jurídica e confronto de autoridades. Só será jurimetria quando houver análise quantitativa com população e método declarados.

### 8.2 Trilha de busca dentro do `source_ledger`

O caderno separado continua cortado. A trilha jurídica passa a existir por extensão versionada do `source_ledger`, com:

- `queryId`;
- base e endpoint consultados;
- data e hora;
- termos e filtros;
- órgão e recorte temporal;
- IDs retornados;
- IDs descartados e motivo;
- bases não consultadas e motivo;
- resultado negativo;
- referência de replay ou telemetria;
- limitações conhecidas.

Os artefatos F5C mostram que a FORJA já sabe representar protocolo de pesquisa, mas hoje essa família é voltada à ciência extrajurídica e há casos reais em que aparece como não aplicável. A lacuna jurídica é parcial, não total.

### 8.3 Extensão do `verified_source_ledger`

Somente precedentes-âncora recebem ficha aprofundada:

- identidade completa;
- fonte e hash da íntegra;
- trecho literal e localização;
- questão decidida;
- fundamentos determinantes;
- obiter potencialmente confundível;
- moldura fática determinante;
- confronto elemento a elemento com o caso;
- operação pretendida: aplicar, distinguir, delimitar ou sustentar superação;
- regime jurídico;
- vigência conferida em;
- revisor humano quando decisivo.

Não se extrai ratio de ementa quando a íntegra é necessária para sustentar a proposição. Ementa pode servir à descoberta e a uma descrição limitada, identificada como tal.

### 8.4 Regime sem rótulo simplificador

O campo `regime` deve registrar:

- base normativa;
- tipo de autoridade;
- dever ou efeito jurídico;
- órgão competente;
- caminho de distinção, revisão ou superação;
- estado de vigência.

As categorias do art. 927 do CPC não devem ser comprimidas em um único peso numérico. “Persuasivo qualificado” pode existir como categoria interna, desde que identificada como convenção da FORJA, não como classe legal.

Decisão monocrática ou antiga não recebe peso baixo automaticamente. Importam competência, contexto, estabilidade, aderência e vigência.

### 8.5 Integração real com o TeiaJus

O plano de implementação deverá tratar a diferença entre:

- capacidades anunciadas pelo agente TeiaJus;
- ações efetivamente permitidas pelo `FORJA_SEARCH_CONFIG.json`;
- comandos diretos STJ já expostos pelo bridge;
- fontes externas ainda não integradas.

Antes de dizer “integração completa”, deverá existir contrato explícito para as ações necessárias de plano, missão e pesquisa, com allowlist, somente leitura, telemetria, limites e teste de proveniência.

### 8.6 Precedente administrativo

Separar dois objetos:

- **evidência administrativa e dados de integridade:** CEIS, CEAF, CNEP, CEPIM, leniência;
- **precedente administrativo decisório:** acórdãos, decisões colegiadas, enunciados e julgados de TCU, CGU/CRG, CADE, CVM, CNJ ou CNMP.

Uma tabela de autoridades em `forja_authorities.py` não cria a fonte nem prova a decisão. Cada família só entra quando houver coleta oficial, identidade, íntegra ou conteúdo decisório suficiente, atualização e gate de citação.

---

## 9. Identidade Medina — corpus progressivo e atribuível

### 9.1 Não esperar por corpus perfeito

O trabalho pode começar com o acervo atual, mas não com a premissa de que todos os DOCX são produção do escritório ou autoria de Fábio. O primeiro produto é um inventário curatorial, fora do caminho crítico:

`IDENTITY_CORPUS_MANIFEST.jsonl`

Campos mínimos:

- arquivo e hash;
- tipo de documento;
- data;
- autor declarado;
- papel de Fábio: autor, coautor, revisor, aprovador, desconhecido;
- confiança da atribuição;
- canal de origem;
- versão: inicial, revisada, enviada ou protocolada;
- relação com outra versão;
- uso permitido: pensamento, estilo escrito, preferência editorial ou negativo;
- observações de proveniência.

Esse manifest é ativo de pesquisa, não novo artefato obrigatório por caso.

### 9.2 Quatro corpora, com pesos diferentes

1. **Peças assinadas ou atribuídas com alta confiança:** melhor evidência de estilo escrito.
2. **Diffs entre versões:** melhor evidência de preferência editorial, desde que se saiba quem alterou ou aprovou.
3. **Feedback humano registrado:** evidência direta de aceitação e rejeição.
4. **Transcrição da entrevista:** evidência forte de método de pensamento e linguagem oral; evidência fraca de forma escrita.

As classes de contribuição intelectual já existentes em `forja_learning.py` devem ser reutilizadas. Uma alteração entre nossa versão e a protocolada não é automaticamente alteração de Fábio.

### 9.3 O que extrair

- movimentos argumentativos recorrentes;
- ordem de apresentação;
- relação entre autoridade, igualdade e consequência;
- padrões de distinção;
- ritmo e extensão de parágrafos;
- uso de doutrina;
- formas de transição;
- preferências de abertura e conclusão;
- alterações que ele aceita, desfaz ou introduz.

Não usar lista rígida de palavras proibidas como substituto de estilo. O detector deve observar fenômenos: densidade artificial, redundância, simetria mecânica, erudição decorativa, abstração sem lastro e agressividade improdutiva.

O “movimento Medina” é técnica opcional, aplicável quando fatos e autoridades o sustentarem. Não é fórmula obrigatória em toda peça.

### 9.4 Validação

O objetivo não é “enganar o leitor” nem provar imitação. É aumentar:

- preferência cega do revisor;
- aceitação para assinatura;
- preservação de fatos, pedidos e autoridades;
- redução de reescrita material;
- adequação ao tipo de peça.

Saídas estilométricas permanecem internas e auxiliares. Não devem ser apresentadas como autenticidade humana ou autoria.

---

## 10. Superfície técnica consolidada

### 10.1 Novos tipos de artefato de execução

1. `F3_MAPA_DESTINATARIO.json`;
2. `F4_SIGNATURE_BRIEF.json`.

### 10.2 Extensões aditivas

1. F2-A/F2-B: seleção, decisão, proveniência e efeito do silêncio;
2. `source_ledger`: trilha de busca jurídica e resultados negativos;
3. `verified_source_ledger`: ficha profunda das âncoras;
4. recibo `gostoJuridico`: hash do brief, rota selecionada e recomposição final.

Cada extensão exige:

- incremento de versão;
- defaults compatíveis para casos legados;
- atualização de schema e catálogo;
- validação de produtores e consumidores;
- replay de fixtures;
- proibição de rebaseline automático.

### 10.3 Ativo curatorial

- `IDENTITY_CORPUS_MANIFEST.jsonl`, sem obrigatoriedade por caso e sem bloquear produção.

### 10.4 O que continua fora

- múltiplos drafts por petição;
- votação N-way ou Condorcet;
- recall;
- pacote novo com dezenas de módulos;
- jurimetria comportamental de julgadores;
- inferência psicológica;
- automação de envio externo sem autorização;
- escore numérico de aderência;
- imitação declarada de autoria.

---

## 11. Validação por natureza da capacidade

| Capacidade | Prova adequada | Gate irredutível |
|---|---|---|
| consulta dialética | materialidade, taxa de resposta, decisões produzidas, perguntas redundantes e rodadas | zero fato material convertido em premissa por silêncio |
| mapa do destinatário | conferência campo a campo em fonte oficial e política de freshness | prevenção e composição sem fonte não podem ser tratadas como confirmadas |
| brief | cobertura das decisões materiais e vínculo com ledgers | rota não pode depender de fato ou âncora bloqueados |
| precedentes | replay da busca, íntegra, hash, quote check, vigência e revisão | ratio decisiva não pode depender só de ementa |
| brief → redação | A/B cego no AUTO-RESEARCH, além dos gates jurídicos | ganho editorial nunca compensa regressão factual ou jurídica |
| identidade | preferência cega, aceitação para assinatura, diff material e preservação semântica | autoria e proveniência do corpus precisam ser atribuíveis |

O A/B serve para testar se brief e identidade melhoram a redação. Não serve para decidir se um dado factual está correto nem para legitimar uma interação pedida pelo titular.

---

## 12. Ondas revisadas

### Onda 0 — contratos e proveniência

Sem mudança no output:

- fixar semântica dos estados epistêmicos;
- definir efeito do silêncio por pergunta;
- mapear produtores e consumidores dos artefatos a estender;
- especificar schemas, versões e migração;
- especificar fontes por campo do mapa;
- inventariar o bridge TeiaJus real;
- criar plano de corpus e regras de atribuição.

**Saída:** pacote de contratos revisável, sem código de produção.  
**Gate:** nenhuma afirmação de capacidade existente pode depender apenas de nome semelhante.

### Onda 1A — cocrição em sombra

- selecionar perguntas materiais;
- gerar minuta de consulta;
- registrar respostas históricas e simular decisões;
- validar que perguntas não estavam respondidas no acervo;
- testar múltiplas rodadas e silêncio material.

**Saída:** consulta interna e ledger de decisão em sombra.  
**Gate:** nenhuma consulta externa automática; nenhuma resposta estratégica usada como prova factual.

### Onda 1B — destinatário e precedentes em sombra

- produzir mapa com fontes separadas;
- pesquisar topologia relevante;
- produzir brief;
- verificar três a seis âncoras;
- reabrir F4 quando âncora cair.

**Saída:** mapa, brief e âncoras sem alterar F6.  
**Gate:** composição, prevenção, ratio e vigência conferidas conforme a natureza do dado.

As ondas 1A e 1B podem correr em paralelo depois da Onda 0.

### Onda 2 — identidade e variante de redação

- curar o corpus disponível;
- separar escrita, edição, feedback e fala;
- extrair padrões candidatos;
- produzir um único draft variante que consome brief e padrões;
- comparar cegamente com o incumbente;
- rejeitar melhorias que reduzam fidelidade jurídica.

**Saída:** evidência de ganho ou ausência de ganho, não promoção automática.

### Onda 3 — piloto controlado

- poucos casos por `pilotCases`;
- consulta enviada apenas por pessoa autorizada ou fluxo interno autorizado;
- mapa e brief ativos;
- F7/F7-B recompõem rota, âncoras e conteúdo obrigatório;
- rollback por flag;
- revisão humana final obrigatória.

**Gate de ampliação:** ganho prospectivo, ausência de regressão jurídica, rastreabilidade completa e custo operacional aceitável.

### Trilha posterior e condicional

- conectores de jurisprudência administrativa conforme demanda real;
- jurimetria comportamental J-B somente após autorização, protocolo ético-jurídico específico e desenho estatístico válido;
- nenhum desses itens bloqueia as ondas centrais.

---

## 13. Critérios de aceite do plano antes de implementação

O plano estará pronto para implementação quando:

- [ ] os novos artefatos tiverem donos, schemas, consumidores e invalidadores definidos;
- [ ] o efeito do silêncio estiver codificado por classe de pergunta;
- [ ] resposta, aceite estratégico e prova factual estiverem separados;
- [ ] cada campo do mapa tiver fonte, freshness e comportamento de falha;
- [ ] o bridge TeiaJus necessário estiver distinguido das capacidades apenas anunciadas;
- [ ] ratio decisiva exigir conteúdo suficiente e localização verificável;
- [ ] o regime do precedente não for reduzido a peso numérico;
- [ ] o corpus tiver política de autoria e contribuição intelectual;
- [ ] A/B, conferência factual e métrica de interação não forem confundidos;
- [ ] o envio externo permanecer sujeito a autorização;
- [ ] casos legados preservarem compatibilidade;
- [ ] os gates anti-alucinação AH-01 a AH-08 permanecerem fail-closed em `strict_protocol`.

---

## 14. Decisões humanas reservadas

A FORJA pode sugerir, comparar e explicar. Permanecem reservadas ao advogado responsável:

- objetivo final do trabalho;
- fatos que dependam de declaração do cliente ou do escritório;
- escolha estratégica quando houver risco material;
- desistência, concessão, reconhecimento ou pedido sensível;
- autorização de envio;
- seleção final da rota;
- aprovação do texto para assinatura.

Se o advogado não decidir ponto essencial, a FORJA pode avançar nas partes independentes, mas não deve encobrir a pendência.

---

## 15. O que mudou em relação ao documento 31

| Tema | Documento 31 | Versão 32 |
|---|---|---|
| TeiaJus | “já tem o dado” | contém parte dos insumos; composição, prevenção e ratio exigem fontes e gates distintos |
| consulta | resposta equivale a aceite | só equivale quando resolve materialmente o ponto; resposta parcial mantém pendência |
| silêncio | default pouco delimitado | default apenas não material; fato, autorização e estratégia decisiva bloqueiam o dependente |
| rotas | exatamente três | duas a quatro como heurística; sem alternativas artificiais |
| schema | extensões “sem schema novo” | sem novo tipo de artefato, mas com versão, migração e validação de consumidores |
| pesquisa | só resultado negativo seria novo | F5C já cobre parte do raciocínio científico; pesquisa jurídica precisa genealogia de queries e rejeições |
| J-A | jurimetria de seleção | pesquisa topológica e estratégica de precedentes |
| CGU | precedente administrativo implícito | dados sancionatórios separados de decisões administrativas |
| identidade | Corpus B começa com diffs | corpus começa por inventário de autoria; diff sem atribuição não prova preferência de Fábio |
| implantação da consulta | entra diretamente em operação | começa em sombra; envio real requer pessoa ou fluxo interno autorizado |

---

## 16. Evidências e referências usadas nesta revisão

### Evidência local

- `forja_exploracao_100.py` e contratos F2-A;
- `FORJA_SEARCH_CONFIG.json` e `forja_legal_search.py`;
- `n4_schemas/f5c_research_protocol.schema.json`;
- `n4_schemas/f5c_study_ledger.schema.json`;
- artefatos reais `F5C_RESEARCH_PROTOCOL.json` e `F5C_STUDY_LEDGER.json`;
- `forja_learning.py`;
- `forja_diff_docx.py`;
- `../_MODELOS/`;
- `FAILURE_TAXONOMY_ANTI_ALUCINACAO.md`;
- mapas Archify/Graphify e `INTERFACES_INFERIORES.md`.

### Fontes oficiais para os limites jurídicos

- Código de Processo Civil, especialmente arts. 489, § 1º, V e VI, e 927: <https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105.htm>
- Glossário da API Pública do DataJud: <https://datajud-wiki.cnj.jus.br/api-publica/glossario/>
- LOMAN, art. 41: <https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp35.htm>
- Estatuto da Advocacia, art. 34 e incisos aplicáveis ao caso concreto: <https://www.planalto.gov.br/ccivil_03/leis/l8906.htm>

---

## 17. Próxima ação

A conversão documental foi concluída:

- PRD: `planejamento/33_PRD_FORJA_ASSINATURA_LITE_COCRIACAO_PRECEDENTES.md`;
- TDD: `planejamento/34_TDD_FORJA_ASSINATURA_LITE_COCRIACAO_PRECEDENTES.md`;
- roadmap: `planejamento/35_ROADMAP_EXECUCAO_FORJA_ASSINATURA_LITE.md`.

A próxima ação de execução é a W0 do roadmap. Até que uma onda seja executada e validada, os artefatos e fluxos permanecem **arquitetura proposta**, não capacidade implementada.
