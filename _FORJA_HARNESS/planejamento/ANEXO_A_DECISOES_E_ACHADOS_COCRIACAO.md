# 33 — PRD: cocriação, mapa do destinatário e precedentes estratégicos

**Protocolo:** `FORJA-COCRIACAO-v1`
**Data:** 25/07/2026. **Estado:** requisitos de produto aprovados para detalhamento técnico. **Não autoriza implementação.**

**Cadeia documental.** Requisitos do titular: `29`. Arquitetura dos três eixos: `30`. Consolidação v1: `31`. Consolidação v2 do Codex: `32`. **Este documento revisa o 32 e o converte em requisito.** O TDD é o `34`; ondas e portões, o `35`. Os documentos `26`, `27` e `28` seguem reclassificados como visão longa.

**Precedência.** Em conflito operacional, prevalecem, nesta ordem: os gates anti-alucinação AH-01 a AH-08 em `strict_protocol`; este PRD; o TDD `34`; o roteiro `35`.

---

## 1. Revisão do documento 32 — registro de decisão

Aplico o padrão de conselho da fábrica: cada ponto recebe **acatado**, **acatado com ajuste** ou **rejeitado**, com motivo.

### 1.1 Acatados sem reserva — e três deles corrigem erro meu

| # | Ponto do documento 32 | Decisão | Motivo |
|---|---|---|---|
| C1 | **Efeito do silêncio por classe de pergunta** | acatado | É a melhor correção do documento. O `31` tratava "toda pergunta tem premissa declarada" como regra geral. Fato material, autorização e escolha estratégica decisiva **não podem** virar premissa por silêncio. Converte-se em requisito RF-2.4. |
| C2 | Extensão aditiva **não dispensa** versão de schema, migração e validação de consumidores | acatado | O `31` dizia "sem schema novo", o que era enganoso. Corrigido no RF-6 e no TDD. |
| C3 | Resposta do advogado **não é aceite automático** | acatado | Resposta parcial, ambígua ou lateral não fecha a questão. RF-2.5. |
| C4 | TeiaJus **não contém sozinho** composição atual, prevenção e ratio | acatado | Erro meu de ênfase no `31`. `orgaoJulgador` do DataJud é metadado processual: orienta a busca, não prova composição nem prevenção. RF-3.2 e RF-3.4. |
| C5 | CEIS, CNEP, CEPIM, CEAF e leniência são **dados sancionatórios**, não jurisprudência administrativa | acatado | Erro meu no `30`, §3.6. Decisão administrativa de TCU, CGU/CRG, CADE, CVM, CNJ e CNMP exige conector próprio. Sai do escopo v1. |
| C6 | "Jurimetria de seleção" é nome errado | acatado | Passa a ser **pesquisa topológica e estratégica de precedentes**. O nome importa: chamar de jurimetria transporta para uma atividade de risco nulo o perfil de risco do módulo J-B. |
| C7 | Corpus de identidade exige **inventário de autoria** antes de extração | acatado | Um diff entre a nossa versão e a protocolada não prova alteração de Fábio. Reutilizar `CONTRIBUTION_ORIGINS`, `CONTENT_CLASSES` e `CONTRIBUTION_STATUS`, que já existem em `forja_learning.py` — verificado. |
| C8 | Consulta começa **em sombra**; envio real só por pessoa autorizada | acatado | Envio de e-mail a sócio é ação externa. RF-2.7. |
| C9 | Topologia **condicional**, não escada fixa; prequestionamento é ledger paralelo | acatado | Nem todo tribunal tem seção e Corte Especial. O prequestionamento deriva da decisão recorrida, não do degrau de busca. |
| C10 | Regime do precedente **não comprimido em peso numérico**; monocrática e antiga não recebem peso baixo automático | acatado | Coerente com a rejeição da nota de aderência. |
| C11 | Ratio não se extrai de ementa **quando a íntegra é necessária para sustentar a proposição** | acatado | Formulação melhor que a minha, que era absoluta. Ementa serve à descoberta e a descrição limitada, identificada como tal. |
| C12 | Existe família `F5C` de protocolo de pesquisa; a lacuna jurídica é **parcial** | acatado | Verificado: `f5c_research_protocol` e `f5c_study_ledger` existem no catálogo. |

### 1.2 Acatados com ajuste

| # | Ponto | Ajuste |
|---|---|---|
| C13 | "Cinco a doze perguntas é heurística, não gate" | Acato que não é gate. **Mas permanece indicador observável com gatilho de revisão:** se os filtros produzirem mais de vinte perguntas materiais, isso é sinal sobre a leitura do caso, não apenas sobre a complexidade dele. Vira métrica, não bloqueio. |
| C14 | "Exatamente três rotas" vira "duas a quatro" | Acato a faixa e o motivo — forçar três produz alternativa artificial, o mesmo Goodhart que matou o mínimo de teses. **Ajuste:** rota única exige justificativa registrada de por que as alternativas seriam artificiais; não pode ser o caminho de menor esforço. |
| C15 | "Movimento Medina é técnica opcional" | Acato que não é fórmula obrigatória por peça. **Ajuste:** permanece a **hipótese padrão** do campo `consequenciaDemonstrada` do brief, porque o titular o executou três vezes de forma não solicitada e porque a camada EDGE já o implementa sob o nome de saliência decisória. Opcional na aplicação, padrão na consideração. |

### 1.3 O que o documento 32 perdeu e este PRD restaura

| # | Item | Por que restaurar |
|---|---|---|
| C16 | **A convergência entre `F4_SIGNATURE_BRIEF` e o leque de teses do titular** | É o argumento que sustenta construir **um** mecanismo. Sem ele registrado, um leitor futuro reabre o caminho de dois sistemas. Restaurado no §2.1. |
| C17 | **Condição da Régua** | A revisão adversarial Fable 5 de 24/07 tornou bloqueante: a Régua verde, ou o desvio classificado e aceito como baseline conhecido, antes de gerar. Rebaseline automático continua proibido. Restaurado no `35`. |
| C18 | **Placar de superfície** | Governança precisa do comparativo explícito para impedir recrescimento silencioso. Restaurado no §4.4. |
| C19 | **Corte do recall, com motivo** | O `32` lista recall como fora, sem o motivo. O motivo importa: recall mede memorabilidade, e o modelo de leitor do titular é o julgador com fila, cuja métrica é esforço de decisão. Restaurado no §5. |

### 1.4 Rejeitado

| # | Ponto | Motivo |
|---|---|---|
| C20 | Criar `F3_MAPA_DESTINATARIO.json` e `F4_SIGNATURE_BRIEF.json` como **dois tipos novos de artefato** | Ver §2.2. O catálogo N4 já declara 24 tipos com envelope e sem payload, e **nenhum é produzido em caso real**. Criar dois tipos novos por cima disso agrava o problema em vez de resolvê-lo. |

---

## 2. Fundamentos do produto

### 2.1 Um mecanismo, não dois — e por quê

Dois planos independentes convergiram para o mesmo objeto. O `F4_SIGNATURE_BRIEF`, que nasceu de teoria de seleção editorial contra o *synthetic sameness*, e o "leque de teses" que Fábio Medina Osório descreveu na entrevista, são **o mesmo artefato visto de dois ângulos**: rotas plausíveis, versão óbvia rejeitada com motivo, âncoras, contra-argumento antecipado e consequência demonstrada.

A tabela EDGE do documento `25` fecha a equivalência por um terceiro caminho: o que ela chama de **Emotional**, já traduzido pela FORJA como **saliência decisória** — *"fazer o julgador perceber a consequência que os autos já provam"* —, é o terceiro tempo do movimento argumentativo do titular: estabelecer o que a autoridade já decidiu, mostrar que decidir diferente rompe isonomia, nomear a consequência para quem decide.

**Requisito de governança:** qualquer proposta futura que crie um segundo lugar de decisão estratégica deve ser rejeitada por referência a este parágrafo.

### 2.2 A descoberta que reduz a superfície: 24 conchas vazias

Verificado em 25/07/2026:

- `n4_schemas/ARTIFACT_CATALOG.json` declara **24 tipos de artefato**, entre eles `F4_DECISION_FACTOR_MAP.json`, `F4_COVERAGE_MATRIX.json`, `F4_THESIS_MATURITY.json`, `F4_SETTLEMENT_MAP.json` e `F3_EVENT_IDENTITY.json`;
- cada schema traz **apenas o envelope N4** — `schemaVersion`, `specVersion`, `caseId`, `artifactType`, `phase`, `applicability`, `status`, `sourceHashes`, `producerRunId`, `reviewerRunId`, `createdAt`, `updatedAt`, `contentHash`, `issues`, `justification` — **e nenhum payload de domínio**;
- varredura em `state/*/runs/*/*/attempt-*/`: **nenhum dos 24 aparece em caso real.** Os casos produzem os artefatos N2 e N3 — `document_index`, `coverage_ledger`, `fact_ledger`, `source_ledger`, `blueprint`, `f7_gate_result` e afins.

Conclusão de produto: a FORJA não sofre de falta de tipos de artefato. Sofre de **tipos declarados sem payload e sem produção**. Criar dois tipos novos repetiria o erro com nomes novos.

**Decisão:** o brief **não é tipo novo**. É o **payload de `F4_DECISION_FACTOR_MAP.json`**, que já está declarado no catálogo, já pertence à fase F4 e já herda envelope, hashes, separação produtor/revisor e recomputação de `contentHash`. A cobertura de famílias de tese é o **payload de `F4_COVERAGE_MATRIX.json`**. Nenhum outro shell é ativado nesta versão — ativar concha que o plano não precisa é a mesma doença.

O mapa do destinatário é o **único tipo genuinamente novo**, porque nenhum shell corresponde a ele: `F3_EVENT_IDENTITY` trata da identidade dos atos processuais, que é problema vizinho e distinto.

### 2.3 Princípios herdados, que este PRD não reabre

Verificação antes de persuasão; identidade como método e não personificação; responsabilidade epistêmica com `record_evidence`, `office_declaration`, `inference` e `unknown` separados; proporcionalidade do fichamento à materialidade; ausência de pseudoprecisão numérica. Todos do documento `32`, §3.

---

## 3. Usuários e resultado pretendido

**Usuário primário:** o advogado responsável pelo caso — em regra Fábio Medina Osório ou sócio que ele designe.
**Usuário secundário:** o operador da FORJA, que revisa e envia.
**Não usuário:** o cliente final e o juízo. Nenhum artefato desta versão é endereçado a eles.

Resultado pretendido, em uma frase: **antes de escrever, a FORJA sabe o que o advogado quer, sabe quem vai decidir, e sabe com qual autoridade vai constranger — e registra as três coisas de modo verificável.**

---

## 4. Requisitos funcionais

### RF-1 — Cobertura de famílias de tese (payload de `F4_COVERAGE_MATRIX`)

RF-1.1 Para cada família — competência, admissibilidade, prejudiciais, prescrição e decadência, nulidades, mérito principal, mérito subsidiário, matéria constitucional a prequestionar, consequência institucional — registrar `examinada_e_proposta`, `examinada_e_descartada` com motivo, ou `nao_aplicavel` com motivo.
RF-1.2 Proibido mínimo numérico de teses. A cobertura é de famílias examinadas, não de teses afirmadas.
RF-1.3 Nenhuma família pode ficar sem registro. Ausência silenciosa é falha de completude.

### RF-2 — Consulta dialética ao advogado (F2-B)

RF-2.1 A consulta é **ato endereçado**, com objeto, motivação e dever de resposta. Não é formulário nem conversa por turnos.
RF-2.2 Cinco blocos: compreensão declarada; perguntas decisórias; diligências documentais motivadas; rotas para provocação; decisões reservadas ao advogado.
RF-2.3 **Filtros de admissão**, todos obrigatórios: a pergunta não está respondida nos autos, nas mensagens nem em fonte oficial acessível; pode mudar decisão material; está endereçada a quem pode decidir; declara o efeito da ausência de resposta.
**Pergunta que a FORJA poderia responder pesquisando o próprio acervo é falha do sistema, e é bloqueador de emissão.**

RF-2.4 **Efeito do silêncio, por classe** — requisito derivado de C1:

| Classe da pergunta | Efeito da ausência de resposta |
|---|---|
| fato material, documento essencial, identidade processual | **bloqueia** a alegação ou o produto dependente; **nunca vira premissa protocolável** |
| autorização, pedido, renúncia, reconhecimento, exposição de risco | **bloqueia** a ação correspondente |
| objetivo do cliente ou escolha estratégica decisiva | mantém alternativas abertas e **impede a seleção final da rota** |
| preferência não material de forma, prioridade ou apresentação | admite **default explícito, reversível e visível** |
| escolha estratégica não material | admite default **apenas** se a consulta houver declarado consequência e risco |

`default_on_silence` é propriedade **por pergunta**, jamais global, e em nenhuma hipótese converte desconhecimento em fato.

RF-2.5 A resposta cumpre função de fixação de escopo **apenas quando resolve materialmente o ponto**. Resposta parcial, ambígua ou lateral mantém a pendência aberta. Não existe subfase separada de aceite; existe registro de decisão com pergunta, resposta, autor, canal, natureza epistêmica, decisão produzida, artefatos afetados, pendência remanescente, data e versão.
RF-2.6 Rodadas sucessivas são permitidas. Teto por classe de caso é parâmetro de configuração, a preencher com o titular.
RF-2.7 **Nenhum envio externo autônomo.** A FORJA produz a minuta e o destinatário sugerido; pessoa autorizada revisa e envia; envio e resposta recebem vínculo de proveniência.
RF-2.8 Marcadores internos de auditoria — `[FONTE: arquivo]`, caminhos locais, proveniência operacional — são proibidos no texto da consulta, na forma do protocolo de 11/07.

### RF-3 — Mapa do destinatário (tipo novo, fase F3, subfase F3-B)

RF-3.1 Blocos, cada um com fonte declarada: competência; prevenção; composição atual; posição individual do relator; posição colegiada; divergência conhecida; rota recursal projetada.
RF-3.2 **Fonte adequada por campo.** Composição atual exige página oficial vigente do tribunal. Prevenção exige autos, distribuição e regimento. Posição individual e ratio exigem íntegra ou reprodução oficial verificável. `orgaoJulgador` do DataJud e espelho mensal **orientam a busca e não provam** composição, prevenção nem fundamento determinante.
RF-3.3 **Topologia condicional.** A ordem de busca segue a estrutura real do tribunal e a matéria. Outra turma da seção, seção e Corte Especial só entram quando forem relevantes. Prequestionamento não é degrau da escada: é ledger paralelo derivado da decisão recorrida e da rota recursal.
RF-3.4 **Perecibilidade.** Todo dado mutável carrega `checkedAt`, `sourceId` ou URL oficial, `freshnessPolicy` e `status` em `confirmed`, `stale`, `unknown` ou `not_applicable`. Dado vencido não é reutilizado em silêncio. **"Não apurado" é preferível a composição antiga apresentada como atual.**
RF-3.5 Campo não apurado é aceitável; campo não apurado **sem motivo** é falha de completude.

### RF-4 — Signature brief (payload de `F4_DECISION_FACTOR_MAP`)

RF-4.1 Campos mínimos: questão decisiva; consequência demonstrada nos autos; rotas plausíveis; rota selecionada e responsável pela decisão; rotas rejeitadas com motivo; frase-mãe provisória; fatos e documentos decisivos por ID; precedentes-âncora candidatos por ID; melhor contra-argumento e resposta; conteúdo obrigatório e limites; pendências que impedem a redação.
RF-4.2 **Duas a quatro rotas** quando houver pluralidade real. Rota única é válida e exige justificativa registrada de que as alternativas seriam artificiais. Mais de quatro exige justificativa de complexidade.
RF-4.3 O brief é produzido **dentro da execução F4 atual**, após os pareceres de Helena e Cícero, sem chamada adicional.
RF-4.4 **Lugar único de decisão estratégica.** O leque de teses da consulta é renderização deste artefato; não há segunda origem de rotas.
RF-4.5 O brief é decisão, não sumário para expansão. F6 recebe a rota e os vínculos; **é proibido converter campo do brief em subtítulo da peça.**
RF-4.6 Rota não pode depender de fato ou âncora bloqueados. Depender de pendência material impede a seleção final.
RF-4.7 O campo `consequenciaDemonstrada` tem como hipótese padrão o movimento de constrangimento por incoerência, aplicável quando fatos e autoridades o sustentarem; não é obrigatório e não pode ser preenchido por fórmula.

### RF-5 — Precedentes estratégicos e auditáveis

RF-5.1 **Nome.** A atividade chama-se pesquisa topológica e estratégica de precedentes. O termo jurimetria fica reservado a análise quantitativa com população, janela, denominador, incerteza e finalidade declarados.
RF-5.2 **Trilha de busca**, por extensão versionada do `source_ledger`: `queryId`; base e endpoint; data e hora; termos e filtros; órgão e recorte; IDs retornados; IDs descartados com motivo; bases não consultadas com motivo; **resultado negativo**; referência de replay ou telemetria; limitações conhecidas.
RF-5.3 O **resultado negativo** é requisito, não conveniência: a ausência de precedente favorável no órgão prevento altera a estratégia da peça inteira.
RF-5.4 **Ficha profunda apenas das âncoras** — tipicamente três a seis por peça —, por extensão do `verified_source_ledger`: identidade completa; fonte e hash da íntegra; trecho literal e localização; questão decidida; fundamentos determinantes; obiter potencialmente confundível; moldura fática determinante; confronto elemento a elemento; operação pretendida; regime; `vigenciaConferidaEm`; revisor humano quando decisivo.
RF-5.5 **Operação declarada**, em vez de escore: aplicar; distinguir; delimitar alcance; sustentar superação. Precedente sem operação declarada não é citado.
RF-5.6 **Aderência governa a operação, não a força.** Precedente vinculante com moldura diversa não é rebaixado: delimita-se o alcance, distingue-se ou sustenta-se superação, com a fundamentação exigida pelo art. 489, §1º, VI, e pelo art. 927, §§1º a 4º, do CPC.
RF-5.7 `regime` registra base normativa, tipo de autoridade, dever ou efeito, órgão competente, caminho de distinção ou superação e vigência. Não é peso numérico. "Persuasivo qualificado" é convenção interna da FORJA e deve ser identificada como tal, nunca como classe legal.
RF-5.8 Ratio decisiva **não pode depender apenas de ementa** quando a íntegra for necessária para sustentar a proposição. Ementa serve à descoberta e a descrição limitada, identificada como tal.
RF-5.9 **Integração TeiaJus:** distinguir capacidades anunciadas pelo agente, ações permitidas pelo `FORJA_SEARCH_CONFIG.json`, comandos já expostos pelo bridge e fontes não integradas. Só há "integração" onde houver contrato explícito com allowlist, somente leitura, telemetria, limites e teste de proveniência.

### RF-6 — Compatibilidade e migração

RF-6.1 Toda extensão de artefato existente exige incremento de versão de schema, defaults compatíveis para casos legados, atualização de catálogo, validação de produtores e consumidores, replay de fixtures e proibição de rebaseline automático.
RF-6.2 Casos legados continuam válidos sem os campos novos.
RF-6.3 Ativar um shell do catálogo exige definir payload, produtor, consumidor, invalidador e teste. **Shell ativado sem consumidor é proibido.**

### RF-7 — Identidade, fora do caminho crítico

RF-7.1 Primeiro produto é o inventário curatorial `IDENTITY_CORPUS_MANIFEST.jsonl`, com arquivo e hash, tipo, data, autor declarado, papel de Fábio, confiança da atribuição, canal, versão, relação com outra versão, uso permitido e observações de proveniência.
RF-7.2 Reutilizar as classes já existentes em `forja_learning.py` — `CONTENT_CLASSES`, `CONTRIBUTION_ORIGINS`, `CONTRIBUTION_STATUS`, `CONFIDENCE` —, verificadas em 25/07/2026. Não criar taxonomia paralela.
RF-7.3 Quatro corpora com pesos distintos: peças atribuídas com alta confiança, melhor evidência de estilo escrito; diffs entre versões, evidência de preferência editorial **desde que se saiba quem alterou**; feedback humano registrado, evidência direta de aceitação e rejeição; transcrição da entrevista, evidência forte de método de pensamento e **fraca** de forma escrita.
RF-7.4 Não usar lista rígida de palavras proibidas como substituto de estilo. O detector observa fenômenos: densidade artificial, redundância, simetria mecânica, erudição decorativa, abstração sem lastro, agressividade improdutiva.
RF-7.5 Validação mede preferência cega do revisor, aceitação para assinatura, preservação de fatos, pedidos e autoridades, e redução de reescrita material. **Não mede capacidade de passar por autoria humana**, e saída estilométrica é interna e auxiliar.
RF-7.6 O manifesto não é artefato obrigatório por caso e não bloqueia produção.

---

## 4.4 Placar de superfície

| | ASSINATURA v1 (doc 26) | Meu plano isolado (doc 30) | Consolidado v1 (doc 31) | **Este PRD** |
|---|---:|---:|---:|---:|
| Tipos novos de artefato | 6 | 4 | 2 | **1** |
| Shells do catálogo ativados | 0 | 0 | 0 | **2** |
| Extensões de artefato existente | 1 | 2 | 3 | **3** |
| Subfases novas | 5 | 6 | 1 | **2** (F2-B, F3-B) |
| Pacotes ou CLIs novos | 1 | 0 | 0 | **0** |
| Drafts por petição | 3 ou mais | 1 | 1 | **1** |
| Ondas | 15 | 3 blocos | 3 | **4** (0 a 3) |

O aumento de zero para dois shells ativados **reduz** superfície: são tipos que já existem no catálogo e ganham payload, em vez de tipos novos que engrossariam a lista de conchas.

---

## 5. Fora de escopo, com motivo

| Item | Motivo |
|---|---|
| Múltiplos drafts por petição, N-way, Condorcet, terceiro juiz | a inteligência está na qualidade da escolha prévia, não no volume de versões; comitê tende à mediania |
| **Recall em duas sessões** | mede memorabilidade; o modelo de leitor do titular é o julgador com fila, cuja métrica é **esforço de decisão reduzido**. Recall é métrica de publicidade e otimizá-la produz o texto calculado que se quer evitar |
| Memória decisória em produção | risco de Goodhart e de contaminação; leitura apenas no AUTO-RESEARCH offline |
| Pacote `forja/signature/` e CLI própria | não há função que os módulos existentes não comportem |
| Escore numérico de aderência | pseudoprecisão |
| Jurimetria comportamental de julgadores (J-B) | alto valor e alto risco; exige autorização, protocolo ético-jurídico e desenho estatístico válido; não bloqueia as ondas centrais |
| Conectores de jurisprudência administrativa | exigem coleta oficial própria; entram por demanda real |
| Envio externo autônomo | ação externa sujeita a autorização |
| Ativação dos demais 22 shells do catálogo | shell sem consumidor é dívida, não capacidade |

---

## 6. Critérios de aceite por capacidade

| Capacidade | Prova adequada | Gate irredutível |
|---|---|---|
| Cobertura de famílias | toda família com registro e motivo | ausência silenciosa reprova |
| Consulta dialética | materialidade por pergunta, taxa de resposta, decisões produzidas, rodadas, **perguntas respondíveis pelo acervo** | zero fato material convertido em premissa por silêncio; zero envio autônomo |
| Mapa do destinatário | conferência campo a campo em fonte oficial e política de frescor | prevenção e composição sem fonte não podem constar como confirmadas |
| Signature brief | cobertura das decisões materiais e vínculo com ledgers | rota não pode depender de fato ou âncora bloqueados |
| Precedentes | replay da busca, íntegra, hash, conferência de trecho, vigência e revisão | ratio decisiva não pode depender só de ementa; precedente sem operação declarada não é citado |
| Brief para redação | A/B cego no AUTO-RESEARCH, além dos gates jurídicos | ganho editorial nunca compensa regressão factual ou jurídica |
| Identidade | preferência cega, aceitação para assinatura, diff material, preservação semântica | autoria e proveniência do corpus precisam ser atribuíveis |

**Separação metodológica que não pode ser confundida:** o A/B testa se o brief e a identidade melhoram a redação. Não decide se um dado factual está correto — isso é conferência em fonte oficial — nem legitima uma interação que o titular pediu por escrito — isso é métrica de interação.

---

## 7. Decisões reservadas ao advogado responsável

Objetivo final do trabalho; fatos que dependam de declaração do cliente ou do escritório; escolha estratégica com risco material; desistência, concessão, reconhecimento ou pedido sensível; autorização de envio; seleção final da rota; aprovação do texto para assinatura.

Se o advogado não decidir ponto essencial, a FORJA avança nas partes independentes **e não encobre a pendência**.

---

## 8. Riscos de produto

| Risco | Mitigação |
|---|---|
| Texto escrito para a rubrica | o brief é decisão, não roteiro; RF-4.5 proíbe converter campo em subtítulo; o gate de estilo humano permanece detector |
| Mediania por seleção | comparação apenas no AUTO-RESEARCH, fora da produção; sem comitê por petição |
| Perguntar o que está nos autos | bloqueador de emissão em RF-2.3; métrica de qualidade em §6 |
| Composição perecível apresentada como atual | RF-3.4; "não apurado" preferível |
| Ratio extraída de ementa por conveniência | RF-5.8 como bloqueador desde o primeiro dia |
| Recrescimento silencioso da superfície | §4.4 e RF-6.3 |
| Risco empírico: escolha melhor sem peça melhor | ondas 2 e 3 do documento `35`; se não confirmar, sombra ou desligamento, preservando a FORJA atual |

---

## 9. Dependências externas ao sistema

Vinte a trinta peças assinadas, estratificadas por tipo, incluindo duas ou três que ele considere ruins; preferência doutrinária por matéria; parâmetros por classe de caso em tabela **vazia**, preenchida com ele; autorização e limites do módulo J-B; textos dele sobre soberania cognitiva e espaço público não estatal.
