# Documentação arquitetural completa — FORJA Harness

> Versão aprofundada gerada em 2026-08-05T00:22:15-03:00. Escopo: `C:\Users\IgorPC\.claude\projects\Escritório fabio osório\fabricas de melhoria de petições\_FORJA_HARNESS`. Este documento explica estrutura, responsabilidades, decisões, cenários, confiança e falhas. Ele não lê nem reproduz conteúdo privado do workspace.

## 1. Resumo executivo

FORJA é um harness multiestágio com contratos e promoção fail-closed: cada fase transforma artefatos explícitos, preserva hashes/reason codes e impede que lacunas, instruções injetadas ou edição estilística alterem a substância jurídica.

O sistema é classificado como **harness jurídico multiestágio**. O mapa distingue cinco tipos de afirmação: estrutura observada no sistema de arquivos; documento marcador observado pelo nome; relação arquitetural curada; decisão registrada neste pacote; e estado vivo que precisa de verificação independente. Essa separação impede que um desenho conveniente seja tratado como prova de conteúdo, de operação ou de situação jurídica.

### O que está coberto

- **622 diretórios** mapeados até profundidade **6**.
- **8447 arquivos visíveis** contados nas subárvores expandidas.
- **547 documentos marcadores** representados sem ingestão de conteúdo privado.
- **745 arquivos sensíveis/binários** apenas contados e deliberadamente não lidos.
- Componentes lógicos, conexões, cenários, ADRs, fronteiras de confiança e falhas previsíveis.

### O que não está coberto

- Inteiro teor de autos, mensagens, anexos, bancos, planilhas, mídias, credenciais, telemetria ou estado privado.
- Saúde atual de serviços externos, conclusão de demandas, vigência normativa ou veracidade de alegações jurídicas.
- Dependências inferidas apenas por conteúdo de código que não tenha sido aberto no inventário metadata-only.

## 2. Autoridade e ordem de leitura

1. `README.md`
2. `FORJA_SPEC_MANIFEST.json`
3. `MAPA_IA.md`
4. `ARCHIFY_ARQUITETURA.md`
5. `GRAPHIFY_GRAFO.md`
6. `contrato da fase relevante`

O Archify explica o modelo e permite navegar por percursos. O Graphify responde perguntas de localização e relação. Nenhum deles substitui os documentos canônicos acima. Quando houver divergência, prevalece a fonte viva mais específica e a divergência deve ser registrada para regeneração.

## 3. Contexto e limites do sistema

### Propósito

Representar contratos de fase, artefatos, gates, fontes, renderização, telemetria e entrega da FORJA sem incorporar dados reais de casos ou estado privado.

### Entradas canônicas

- `README.md`
- `DOCUMENTACAO_TECNICA.md`
- `FORJA_SPEC_MANIFEST.json`
- `MAPA_IA.md`
- `planejamento/06_GATES_QUALIDADE_FORJA.md`

### Fronteiras declaradas

- state, telemetria, cache e renders reais são zonas privadas e não entram no corpus semântico.
- O grafo lista módulos e contratos; não registra alegações, clientes, mensagens ou credenciais.
- Backups permanecem locais; publicação externa não é autorizada por este mapa.

## 4. Decomposição em camadas

| Camada | Responsabilidade |
| --- | --- |
| Controle | runner, manifesto, contratos de fase e schemas |
| Intake e exploração | F1 e F2A estruturam corpus e perguntas antes de redigir |
| Pesquisa e conselho | fontes, busca jurídica, Helena e Cícero |
| Produção | blueprint, redação auditável e revisão editorial fiel |
| Verificação | citações, injeção, consistência factual, anti-IA e gates P0/P1 |
| Materialização | visual law, DOCX/PDF, fidelidade e QA por página |
| Estado e observabilidade | state, reports e telemetria separados do código |
| Entrega | pacote interno com evidência de conclusão da fábrica |
| Pós-protocolo | retorno humano, prova de protocolo, comparação exata e histórico por contentKey |
| Aprendizado | candidatos revisados, regras promovidas por fixture e gate prospectivo |
| Evolução arquitetural | candidatas isoladas, shadow, canário, revisão independente e rollback |

Cada camada existe para limitar autoridade. Navegação aponta; fonte sustenta; produção transforma; gate decide promoção; entrega materializa. Uma camada posterior não pode retroativamente criar lastro ausente na anterior.

## 5. Catálogo de componentes

| ID estável | Componente | Tipo | Responsabilidade | Conectividade |
| --- | --- | --- | --- | --- |
| intake | F1 Intake | messagebus | fontes classificadas | 0 entrada(s), 1 saída(s) |
| explore | F2A Exploração | backend | 100 perguntas | 1 entrada(s), 2 saída(s) |
| research | F3 Pesquisa | database | fontes oficiais | 1 entrada(s), 1 saída(s) |
| council | F4 Conselho | external | Helena + Cícero | 1 entrada(s), 1 saída(s) |
| blueprint | F5 Blueprint | cloud | arquitetura da peça | 3 entrada(s), 1 saída(s) |
| draft | F6 Redação | frontend | texto lastreado | 1 entrada(s), 1 saída(s) |
| audit | F7 Auditoria | security | fatos + citações | 1 entrada(s), 2 saída(s) |
| fable | F7-B Editorial | backend | forma com fidelidade | 1 entrada(s), 1 saída(s) |
| render | F8 Materialização | cloud | DOCX / PDF / visual | 2 entrada(s), 1 saída(s) |
| qa | QA final | security | render + invariantes | 1 entrada(s), 1 saída(s) |
| state | Estado / telemetria | database | trilha e métricas | 2 entrada(s), 0 saída(s) |
| delivery | F10 Entrega | external | pacote interno | 1 entrada(s), 1 saída(s) |
| postreturn | Retorno humano | messagebus | captura + prova + diff | 1 entrada(s), 2 saída(s) |
| learning | Aprendizado | database | decisão + teste prospectivo | 1 entrada(s), 2 saída(s) |
| arloop | AR Arquitetural | security | worktree + canário + rollback | 1 entrada(s), 1 saída(s) |

### Regras de responsabilidade

- Um componente não deve assumir a autoridade factual de outro só porque aparece depois no fluxo.
- Estado, cache, backup e telemetria são evidências operacionais, não contratos canônicos.
- Gate de segurança é bloqueante: falha ou ausência de evidência não equivale a aprovação.
- Saídas devem preservar referência suficiente para reconstruir de onde vieram.

## 6. Catálogo de relações

| Aresta | Origem | Destino | Semântica | Evidência/limite |
| --- | --- | --- | --- | --- |
| intake-explore | F1 Intake | F2A Exploração | precedes | F1 antecede a exploração F2A |
| explore-research | F2A Exploração | F3 Pesquisa | fluxo arquitetural | Relação curada no diagrama; validar no artefato local antes de usar como fato operacional. |
| explore-council | F2A Exploração | F4 Conselho | fluxo arquitetural | Relação curada no diagrama; validar no artefato local antes de usar como fato operacional. |
| research-blueprint | F3 Pesquisa | F5 Blueprint | fluxo arquitetural | Relação curada no diagrama; validar no artefato local antes de usar como fato operacional. |
| council-blueprint | F4 Conselho | F5 Blueprint | fluxo arquitetural | Relação curada no diagrama; validar no artefato local antes de usar como fato operacional. |
| blueprint-draft | F5 Blueprint | F6 Redação | fluxo arquitetural | Relação curada no diagrama; validar no artefato local antes de usar como fato operacional. |
| draft-audit | F6 Redação | F7 Auditoria | fluxo arquitetural | Relação curada no diagrama; validar no artefato local antes de usar como fato operacional. |
| audit-fable | F7 Auditoria | F7-B Editorial | gates | F7-B somente ocorre após gate F7 |
| fable-render | F7-B Editorial | F8 Materialização | fluxo arquitetural | Relação curada no diagrama; validar no artefato local antes de usar como fato operacional. |
| audit-render | F7 Auditoria | F8 Materialização | fluxo arquitetural | Relação curada no diagrama; validar no artefato local antes de usar como fato operacional. |
| render-qa | F8 Materialização | QA final | requires | materialização exige QA visual e de fidelidade |
| qa-delivery | QA final | F10 Entrega | fluxo arquitetural | Relação curada no diagrama; validar no artefato local antes de usar como fato operacional. |
| delivery-postreturn | F10 Entrega | Retorno humano | opens | retorno elegível abre ramo posterior independente |
| postreturn-state | Retorno humano | Estado / telemetria | evidences | hashes, estados e reason codes preservam a trilha |
| postreturn-learning | Retorno humano | Aprendizado | proposes | mudanças classificadas produzem candidatas |
| learning-blueprint | Aprendizado | F5 Blueprint | gates | somente regra promovida e testada retorna à produção |
| learning-arloop | Aprendizado | AR Arquitetural | signals | falhas recorrentes podem originar candidata arquitetural |
| arloop-state | AR Arquitetural | Estado / telemetria | evidences | shadow, canário e rollback ficam registrados |

As arestas sem evidência nominal específica permanecem **curadas/inferidas**. Elas são úteis para navegação e formulação de perguntas, mas precisam ser confirmadas no arquivo ou contrato local antes de embasar mudança material.

## 7. Fluxo operacional principal

1. F1 ingere e classifica fontes; conteúdo é dado, nunca instrução.
2. F2A formula 100 perguntas e mantém lacunas bloqueadas.
3. Pesquisa e conselho produzem insumos registrados.
4. Blueprint antecede redação e limita escopo.
5. F7 audita fatos/citações e F7-B altera apenas forma sob gate de fidelidade.
6. F8 materializa e inspeciona todas as páginas.
7. Pacote/entrega preserva manifestos, hashes e reason codes.
8. Retorno humano elegível abre ramo pós-protocolo sem reabrir a entrega.
9. Comparação usa a versão exata entregue e preserva histórico por contentKey.
10. Regra promovida retorna ao blueprint somente após decisão, fixture e teste prospectivo.
11. Candidata arquitetural roda isolada e permanece no teto estudo_descritivo.

O fluxo completo está no diagrama [`FORJA_HARNESS_OPERATIONAL_FLOW.html`](FORJA_HARNESS_OPERATIONAL_FLOW.html). Ele inclui o caminho feliz e as interrupções seguras; portanto, não deve ser lido como uma promessa de que toda execução chega à entrega.

## 8. Cenários ponta a ponta

| ID | Objetivo | Pré-condição | Passos | Saída verificável | Gate |
| --- | --- | --- | --- | --- | --- |
| S-J01 | Executar caso novo | Corpus autorizado e manifesto válido | F1 → F2A → F3/F4 → F5 → F6 → F7/F7-B → F8 → QA → F10 | Pacote interno com trilha de evidência | Qualquer gate bloqueante encerra promoção |
| S-J02 | Reprocessar após falha | PHASE_RESULT com reason code | Identificar fase → preservar estado → corrigir causa → repetir desde fronteira segura | Nova execução comparável | Não pular fase para esconder erro |
| S-J03 | Aplicar revisão editorial | F7 sem P0 material | Congelar substância → editar forma → diff factual → auditoria | Texto mais humano e fiel | Mudança de pedido/fato/autoridade reverte revisão |
| S-J04 | Materializar saída | Texto canônico e assets aprovados | Gerar DOCX/PDF → render → comparar → inspeção por página → manifestar | Artefato visual auditado | Falha visual bloqueia entrega |
| S-J05 | Assimilar retorno humano | Entrega exata registrada e e-mail elegível | Capturar → vincular caso → classificar prova → comparar → revisar candidatos | Original, cópia canônica, relatório e ledger por hash | Identidade, baseline ou OCR ambíguos bloqueiam o ramo |
| S-J06 | Aplicar lição promovida | Regra ativa compatível com o produto/caso | Resolver escopo → aplicar antes da redação → executar suíte prospectiva | Recibo verde e ausência da falha-alvo | Regra compatível não aplicada produz PP-LEARNING-NOT-APPLIED |
| S-J07 | Ensaiar evolução arquitetural | Falha recorrente e candidata declarada | Snapshot → worktree → shadow → canário → revisão → rollback | Relatório comparável em estudo_descritivo | Candidata não promove nem altera produção sozinha |

### Como usar os cenários

1. Identifique o cenário mais próximo da tarefa.
2. Confirme a pré-condição antes de abrir conteúdo amplo.
3. Execute os passos na ordem, registrando a fonte de cada promoção.
4. Verifique a saída pelo critério indicado, não apenas pela existência de arquivo.
5. Se o gate falhar, pare no ponto seguro e preserve o estado para diagnóstico.

## 9. Fluxo de dados e confiança

O diagrama [`FORJA_HARNESS_TRUST_DATAFLOW.html`](FORJA_HARNESS_TRUST_DATAFLOW.html) mostra a linhagem da entrada ao consumo. Ele distingue dados externos, controles, proveniência, persistência e saídas. A regra central é: **movimento no pipeline não aumenta confiança sozinho; confiança aumenta somente por classificação, fonte e validação explícitas**.

| Zona | Nome | Ativos | Regra de confiança |
| --- | --- | --- | --- |
| Z0 | Corpus | Fontes tratadas como dados | Defesa contra injeção |
| Z1 | Controle | Runner, manifesto e schemas | Autoridade de contrato |
| Z2 | Produção | Fases e artefatos intermediários | Promoção por gate |
| Z3 | Estado | Telemetria, cache e runs | Privado e restaurável |
| Z4 | Materialização/entrega | DOCX/PDF e pacote | Somente após QA |
| Z5 | Pós-protocolo | Original, diff e evidência | Conteúdo integral no cofre local |
| Z6 | Aprendizado | Candidatos, regras e candidatas arquiteturais | Autoridade cresce somente por decisão e teste |

### Classificação prática

- **EXTRACTED:** observado diretamente no metadado estrutural ou em relação pai-filho.
- **CURATED/INFERRED:** modelo explícito criado para explicar responsabilidades; exige confirmação local para ações materiais.
- **STATE-LIVE:** fato sujeito a mudança; deve ser verificado no serviço, banco, painel ou fonte operacional correspondente.
- **PRIVATE-EXCLUDED:** conteúdo deliberadamente fora do grafo; acesso somente pelo fluxo autorizado e com escopo mínimo.

## 10. Decisões arquiteturais

| ID | Decisão | Status | Escolha | Consequência | Regra operacional |
| --- | --- | --- | --- | --- | --- |
| ADR-J01 | Contratos por fase | Aceita | Cada fase declara entradas, saídas, invariantes e resultado. | Torna promoção reproduzível e auditável. | Mudança de contrato exige manifesto, schema e teste coerentes. |
| ADR-J02 | F2A bloqueante antes da redação | Aceita | Exploração de perguntas e lacunas antecede blueprint/texto. | Evita redigir sobre corpus insuficiente. | Lacuna P0/P1 impede promoção. |
| ADR-J03 | Conselho como insumo | Aceita | Helena/Cícero produzem pareceres; não substituem fonte nem decisão final. | Preserva diversidade analítica sem criar autoridade fictícia. | Parecer deve ser rastreado e confrontado com evidência. |
| ADR-J04 | F7 antes de F7-B | Aceita | Auditoria factual/citacional precede revisão editorial. | Estilo não mascara erro material. | F7-B altera forma sob gate de fidelidade. |
| ADR-J05 | Estado fora do código | Aceita | State, telemetria, cache e renders são zonas operacionais separadas. | Evita confundir execução particular com contrato canônico. | Backups e limpeza preservam restauração verificável. |
| ADR-J06 | Render é etapa verificável | Aceita | Materialização inclui comparação de fidelidade e inspeção de páginas. | Captura falhas de Word/PDF/layout. | Entrega somente após QA multimodal. |
| ADR-J07 | Pós-protocolo é ramo de F10 | Aceita | O retorno humano não cria F11 nem reabre a entrega ao escritório. | Preserva o limite operacional e acrescenta aprendizado posterior. | Ausência de retorno não desfaz entrega concluída. |
| ADR-J08 | Protocolo exige elo de arquivo | Aceita | Nome, assunto ou assinatura isolados não bastam. | Evita nomear como protocolada uma simples versão final humana. | Só protocol_verified autoriza PEÇA PROTOCOLADA. |
| ADR-J09 | Aprendizado tem autoridade crescente | Aceita | Candidato passa por decisão, fixture, teste e promoção no menor escopo. | Feedback real melhora peças futuras sem universalização silenciosa. | Nenhuma regra ativa sem âncora humana e recibo verde. |
| ADR-J10 | Evolução arquitetural é isolada | Aceita | Candidata roda em worktree separado com shadow, canário e rollback. | A arquitetura aprende sem autoeditar produção. | Teto automático estudo_descritivo; promoção é externa ao AR. |

Essas ADRs registram o raciocínio atualmente adotado. Uma mudança estrutural que contradiga uma ADR deve atualizar a decisão, o diagrama, o grafo e o protocolo local na mesma entrega; não basta editar um HTML gerado.

## 11. Modos de falha e recuperação

| ID | Falha | Sinal | Prevenção | Recuperação |
| --- | --- | --- | --- | --- |
| F-J01 | Injeção no corpus | Documento tenta instruir o agente | Dados nunca são instruções | Quarentenar trecho e registrar detecção |
| F-J02 | Promoção sem contrato | Arquivo aparece sem PHASE_RESULT/hash | Manifesto + schemas | Rejeitar e reexecutar a fase |
| F-J03 | Lacuna material ignorada | P0/P1 chega à redação | F2A/F7 fail-closed | Bloquear e pedir fonte/decisão |
| F-J04 | Editorial altera substância | Diff muda fato/pedido/citação | Gate de fidelidade | Reverter e refazer somente a forma |
| F-J05 | Estado confundido com código | Execução particular vira regra | Zonas separadas | Restaurar contrato canônico e isolar state |
| F-J06 | Render defeituoso | Paginação/elemento visual quebra | QA página a página | Corrigir materialização sem alterar texto canônico |
| F-J07 | Baseline pós-protocolo errada | Hash não coincide com o envio | Resolver por artefato, hash e deliveredAt | Criar backfill próprio em pending_review; nunca sobrescrever F9/F10 |
| F-J08 | Falso protocolo | E-mail diz protocolada sem elo verificável | Separar claimed de verified | Preservar como versão humana final e solicitar comprovante |
| F-J09 | Reingestão apaga decisões | Mesmo contentKey volta como candidato novo | Idempotência por fingerprint e histórico | Revalidar recibos e preservar decisões compatíveis |
| F-J10 | Lição promovida não entra na próxima peça | Suíte compatível não encontra requisito | Registry ativo + validador prospectivo | Bloquear com PP-LEARNING-NOT-APPLIED |
| F-J11 | AR altera produção ou perde evidência | Candidata escreve fora do worktree | Snapshot, overlay isolado e rollback ensaiado | Desabilitar feature preservando capturas e registrar falha |

### Política de falha

- Falha de fonte, validação ou autorização deve ser visível e rastreável.
- Não promover saída parcial como completa.
- Não reconstruir silenciosamente contexto privado para “preencher” lacuna.
- Preservar versão anterior e evidência de comparação quando houver correção.
- Revalidar o ponto de saída após recuperação; corrigir arquivo intermediário não prova sucesso final.

## 12. Inventário físico observado

| Diretório de primeiro nível | Classificação pelo nome | Expandido |
| --- | --- | --- |
| .agents | configuração | sim |
| .claude | configuração | sim |
| .codex | configuração | sim |
| .git | configuração | não |
| .planning | configuração | sim |
| .playwright-mcp | configuração | sim |
| .pytest_cache | configuração | não |
| .ruff_cache | configuração | não |
| 00_MAPA_ARQUITETURA_IA | documentação/planejamento | não |
| __pycache__ | domínio/projeto | não |
| _scripts_oneoff | código/contrato | sim |
| ar_architecture | domínio/projeto | sim |
| autoresearch | domínio/projeto | sim |
| bancada_cafelana_v7 | domínio/projeto | sim |
| blender_atlas | domínio/projeto | sim |
| cache | estado/dados | sim |
| contracts | código/contrato | sim |
| docs | documentação/planejamento | sim |
| FORJA | código/contrato | sim |
| graphify-out | domínio/projeto | não |
| learning_registry | domínio/projeto | sim |
| n4_fixtures | domínio/projeto | sim |
| n4_schemas | domínio/projeto | sim |
| PETICAO_ACORDO_DOUTORADO_FORJA_20260715 | domínio/projeto | sim |
| PETICAO_ENDERECO_EXEQUIBILIDADE_FORJA_20260715 | domínio/projeto | sim |
| phase_contracts | domínio/projeto | sim |
| phase_contracts_n4 | domínio/projeto | sim |
| planejamento | documentação/planejamento | sim |
| private | domínio/projeto | sim |
| pso_schemas | domínio/projeto | sim |
| reports | qualidade/saída | sim |
| state | estado/dados | sim |
| telemetria | estado/dados | sim |
| templates | código/contrato | sim |
| youtube-transcript | código/contrato | sim |

Esse inventário é deliberadamente físico e raso. A classificação pelo nome ajuda a navegar, mas é inferência; ela não afirma o conteúdo interno nem a situação operacional da pasta.

## 13. Análise Graphify

O grafo atual possui **3156 nós**, **9136 arestas dirigidas** e relações com evidência por aresta. As entidades de decisão, cenário, fronteira de confiança e falha foram incorporadas ao grafo para tornar perguntas arquiteturais mais precisas.

### Distribuição de relações

| Relação | Quantidade |
| --- | --- |
| contains | 1169 |
| applies_to | 35 |
| has_architecture_component | 15 |
| documents_failure-mode | 11 |
| documents_architecture-decision | 10 |
| documents_operational-scenario | 7 |
| documents_trust-boundary | 7 |
| gates | 2 |
| evidences | 2 |
| precedes | 1 |
| requires | 1 |
| opens | 1 |
| proposes | 1 |
| signals | 1 |

### Nós mais conectados

| Nó | Grau | Tipo | Origem |
| --- | --- | --- | --- |
| FORJA Harness | 90 | root | . |
| state | 55 | estado/dados | state |
| runs | 24 | domínio/projeto | state/case-cafelana-geral-reconstrucao-20260803/runs |
| runs | 14 | domínio/projeto | state/case-email-auto-19f3f25cb64df962/runs |
| n3_artifacts | 13 | domínio/projeto | state/case-email-auto-19f81838ad4d83ce/n3_artifacts |
| n3_artifacts | 12 | domínio/projeto | state/case-email-auto-19f3f25cb64df962/n3_artifacts |
| ciclo-2 | 11 | domínio/projeto | autoresearch/ciclos/ciclo-2 |
| runs | 11 | domínio/projeto | state/case-email-auto-19f8cec883a0ac31/runs |
| n3_artifacts | 11 | domínio/projeto | state/case-email-natura-cabreuva-19f3991ebc75fe03/n3_artifacts |
| runs | 11 | domínio/projeto | state/case-email-natura-cabreuva-19f3991ebc75fe03/runs |
| case-email-auto-19f3f25cb64df962 | 10 | domínio/projeto | state/case-email-auto-19f3f25cb64df962 |
| n3_artifacts | 10 | domínio/projeto | state/case-email-auto-19f8cec883a0ac31/n3_artifacts |
| case-email-natura-cabreuva-19f3991ebc75fe03 | 10 | domínio/projeto | state/case-email-natura-cabreuva-19f3991ebc75fe03 |
| telemetria | 10 | estado/dados | telemetria |
| bancada_cafelana_v7 | 9 | domínio/projeto | bancada_cafelana_v7 |

### Perguntas úteis ao grafo

- Qual documento ou componente governa a tarefa que pretendo executar?
- Que decisão arquitetural explica esta separação de responsabilidades?
- Qual cenário atravessa este componente e qual gate pode interrompê-lo?
- Que modo de falha ameaça esta saída e qual é a recuperação registrada?
- Onde a confiança muda e que evidência é exigida antes do consumo?
- Quais nós são apenas estrutura física e quais são conceitos curados?

## 14. Rotas de leitura para IAs

### Pergunta de localização

Leia `LEIA_PRIMEIRO.md`, consulte o Graphify e abra apenas o arquivo marcador ou diretório retornado. Não carregue toda a raiz.

### Pergunta de arquitetura

Leia este documento, abra o diagrama de componentes e use o fluxo operacional para identificar handoffs. Confirme relações inferidas no contrato local antes de propor alteração.

### Mudança de código ou processo

Localize a ADR aplicável, o cenário afetado, o gate e o modo de falha. Depois altere a menor superfície coerente, valide o resultado real e regenere mapas se a estrutura mudou.

### Trabalho jurídico ou privado

O mapa só roteia. A afirmação continua dependente da fonte autorizada. Não use o grafo sanitizado para completar fatos, citações, datas, valores, anexos ou estado de casos.

## 15. Artefatos e regeneração

- Diagrama de componentes: [`FORJA_HARNESS_ARCHITECTURE.html`](FORJA_HARNESS_ARCHITECTURE.html)
- Fluxo operacional: [`FORJA_HARNESS_OPERATIONAL_FLOW.html`](FORJA_HARNESS_OPERATIONAL_FLOW.html)
- Fluxo de dados/confiança: [`FORJA_HARNESS_TRUST_DATAFLOW.html`](FORJA_HARNESS_TRUST_DATAFLOW.html)
- Grafo interativo: [`graphify-out/graph.html`](graphify-out/graph.html)
- Grafo verificável: [`graphify-out/graph.json`](graphify-out/graph.json)
- Inventário: [`INVENTARIO_ESTRUTURAL.json`](INVENTARIO_ESTRUTURAL.json)
- ADRs estruturadas: [`DECISOES_ARQUITETURAIS.json`](DECISOES_ARQUITETURAIS.json)
- Cenários e falhas: [`CENARIOS_E_FALHAS.json`](CENARIOS_E_FALHAS.json)

Regeneração: execute o gerador central com o Python do Graphify, renderize os três JSONs Archify, valide com perfil `showcase`, execute `check` nos HTMLs, faça consultas de fumaça e recompute `SHA256SUMS.json`.

## 16. Critério de completude

Este pacote está completo para **navegação e compreensão arquitetural** quando: componentes e responsabilidades estão enumerados; relações trazem limite/evidência; cenário principal e falhas estão documentados; confiança é explícita; diagramas passam schema e composição; grafo não tem arestas pendentes; consulta de fumaça retorna entidades relevantes; hashes correspondem aos arquivos; e mapas canônicos locais continuam preservados.

Ele não está completo para provar conteúdo jurídico, saúde externa ou execução operacional viva — esses pontos exigem verificação nas fontes próprias.

<!-- interfaces-v3:start -->
## Aprofundamento v3 — interfaces inferiores

A camada executável está em [`INTERFACES_INFERIORES.md`](INTERFACES_INFERIORES.md): **128 módulos/scripts**, **591 símbolos públicos**, **136 comandos/subcomandos**, **59 schemas/contratos** e **4304 relações locais** com arquivo/linha e confiança. Veja também a [sequência de interfaces](FORJA_HARNESS_INTERFACE_CALLS.html), o [JSON para agentes](INTERFACES_INFERIORES.json) e a [matriz CSV](MATRIZ_RASTREABILIDADE_INTERFACES.csv).
<!-- interfaces-v3:end -->

<!-- strategy-v4:start -->
## Diagnóstico arquitetural, arquitetura-alvo e propostas v4

A análise opinativa está em [`ANALISE_ARQUITETURAL_E_PROPOSTAS.md`](ANALISE_ARQUITETURAL_E_PROPOSTAS.md). Ela registra evidências, avaliação por dimensão, problemas comprovados, propostas P0–P2, superfícies de mudança, riscos, critérios de aceite e roadmap incremental. A arquitetura-alvo está em [`FORJA_HARNESS_TARGET_ARCHITECTURE.html`](FORJA_HARNESS_TARGET_ARCHITECTURE.html); o plano em [`FORJA_HARNESS_IMPROVEMENT_ROADMAP.html`](FORJA_HARNESS_IMPROVEMENT_ROADMAP.html). Proposta não significa implementação concluída.
<!-- strategy-v4:end -->
