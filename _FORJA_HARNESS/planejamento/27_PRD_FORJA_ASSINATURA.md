# PRD — FORJA-ASSINATURA

> **RECLASSIFICADO EM 25/07/2026 — visão experimental de longo prazo.**  
> O PRD vigente para execução é `planejamento/33_PRD_FORJA_ASSINATURA_LITE_COCRIACAO_PRECEDENTES.md`.

**Versão:** 1.0 revisada  
**Protocolo:** `FORJA-ASSINATURA-v1`  
**Data:** 24/07/2026  
**Estado:** especificação para execução; não implementada  
**Plano:** `planejamento/26_PLANO_IMPLEMENTACAO_FORJA_ASSINATURA.md`  
**TDD:** `planejamento/28_TDD_FORJA_ASSINATURA.md`  
**Revisão externa:** `reports/REVISAO_ADVERSARIAL_FABLE5_FORJA_ASSINATURA_2026-07-24.md`

## 1. Decisão de produto

Criar uma camada autônoma de **divergência estrutural, competição cega e
seleção conservadora** que aumente a identidade, a clareza decisória e a força
argumentativa das peças da FORJA sem reduzir segurança jurídica.

A camada chama-se FORJA-ASSINATURA. Ela não imita um autor, não adiciona
ornamento e não transforma “parecer humano” em um conjunto de maneirismos.
Seu trabalho é descobrir, para cada processo, a arquitetura argumentativa que
torna a conclusão mais necessária, específica e cognitivamente disponível.

O produto só substitui o fluxo vigente quando uma desafiante:

1. passa por todos os vetos jurídicos;
2. é comparada sob o mesmo snapshot;
3. vence de forma cega e estável;
4. mantém a integridade da assinatura até o `final_markdown`.

Na ausência dessa prova, o produto preserva o incumbente.

## 2. Problema

A FORJA já possui controles fortes de fonte, estilo, Fable 5, F7, package e
renderização. Esses controles evitam muitos textos ruins, mas não garantem que
um texto correto seja singular.

Os sintomas de mediania são:

- estrutura intercambiável entre processos;
- abertura que descreve o rito antes da fricção decisória;
- tese correta, mas sem frase-mãe;
- sequência de capítulos herdada do template, não da lógica do caso;
- argumento contrário tratado tarde ou genericamente;
- conclusão que repete pedidos sem mostrar a cadeia necessária;
- edição final elegante, porém incapaz de corrigir uma estratégia originalmente
  mediana;
- “humanização” reduzida a léxico e ritmo, vulnerável a gaming.

A causa é anterior ao estilo: o fluxo converge para uma arquitetura antes de
explorar alternativas genuínas.

## 3. Hipótese

Se a FORJA:

1. reconstruir a identidade decisória;
2. gerar geometrias realmente distintas;
3. filtrar lastro antes da prosa;
4. materializar o incumbente e uma desafiante sob condições comparáveis;
5. escolher às cegas com abstenção;
6. preservar a estrutura escolhida durante F7/F7-B;

então aumentará a preferência qualificada por seus textos sem aumentar
alucinação, omissão, custo fora do limite ou dependência humana por petição.

A hipótese é falsificável. Se não houver ganho prospectivo sobre o incumbente,
a camada não chega a `default_on`.

## 4. Usuários e decisões

### 4.1 Usuário primário

O escritório que recebe uma peça pronta para revisão ou entrega e precisa que o
texto:

- revele rapidamente o ponto que decide;
- seja juridicamente seguro;
- não pareça genérico ou intercambiável;
- resista ao melhor argumento contrário;
- preserve fatos, fontes, pedidos e posição processual.

### 4.2 Usuário operacional

O operador da FORJA, que precisa:

- saber qual arquitetura foi escolhida;
- distinguir incumbente, desafiante, vencedor cego e cânone jurídico;
- entender por que houve abstenção;
- desligar a camada sem migrar ou corromper artefatos;
- auditar custo, modelo, sessão, prompt e hashes.

### 4.3 Decisões suportadas

- Qual é a verdadeira fricção decisória?
- Que arquitetura é menos óbvia e ainda estritamente lastreada?
- A diferença é estrutural ou apenas verbal?
- A desafiante é juridicamente não inferior?
- A preferência permanece quando posição e rótulos mudam?
- O corpo torna questão, âncora, limite, consequência e providência
  recuperáveis?
- F7 ou F7-B alteraram a estratégia selecionada?
- Há evidência suficiente para habilitar a política autonomamente?

## 5. Princípios invioláveis

1. **Juridicidade é veto.** Nenhuma qualidade estética compensa erro de fato,
   fonte, autoridade, pedido, polaridade ou posição processual.
2. **Incumbente material.** `candidate_0` é texto, snapshot e hash; nunca um
   rótulo abstrato.
3. **Comparabilidade.** Candidatos disputam sob o mesmo snapshot e critérios
   congelados.
4. **Divergência antes da prosa.** F4-S busca geometrias; F5 confirma lastro;
   F6 redige.
5. **Abstenção é resultado válido.** Empate, ciclo, baixa confiança ou
   independência insuficiente preservam o incumbente.
6. **Autonomia honesta.** O sistema registra a garantia real de independência;
   sessões distintas da mesma família não são chamadas de famílias
   independentes.
7. **Memória sem contaminação.** Em produção v1, geradores não leem vencedores
   passados. Memória comparativa é escrita para auditoria e AR offline.
8. **Métrica não vira objetivo isolado.** Recall, humanidade e comprimento são
   diagnósticos; não podem dominar o resultado.
9. **Um cânone.** F7 recebe um `draft_markdown`; F8 recebe um
   `final_markdown`.
10. **Compatibilidade e rollback.** F0–F10 permanecem; `mode=off` restaura o
    comportamento anterior.

## 6. Escopo funcional v1

### RF-01 — Configuração e modo efetivo

O sistema deve suportar:

- `off`;
- `shadow`;
- `pilot_blocking`;
- `default_on`.

Em `pilot_blocking`, somente `signature.pilotCases` é bloqueante. Casos fora da
lista operam em sombra. A semântica deve reutilizar o padrão de
`forja_n4_validate._effective_mode()`.

Critérios:

- a configuração efetiva é persistida no artefato;
- override explícito é auditável;
- modo desconhecido falha fechado;
- `off` não chama modelos nem altera outputs.

### RF-02 — Snapshot jurídico congelado

Antes de gerar alternativas, o sistema deve produzir um compromisso que inclua:

- `blueprint`;
- `fact_ledger`;
- `proposition_ledger`;
- `source_ledger`;
- questão e pedidos;
- versões de rubrica, prompts e schemas;
- budget profile.

Qualquer mudança invalida os descendentes conforme a tabela do Plano 26.

### RF-03 — Mapa de assinatura

F4-S deve produzir:

- questão decisória;
- frase-mãe;
- versão óbvia;
- âncora factual/probatória;
- limite jurídico;
- melhor contra-argumento;
- consequência demonstrada;
- providência;
- conteúdo obrigatório;
- lacunas conhecidas.

Ausência de questão, âncora, limite ou providência bloqueia F4-S.

### RF-04 — Geometrias divergentes

F4-S deve produzir de cinco a sete geometrias baratas, sem petição completa.

Uma geometria contém:

- eixo primário;
- movimento inicial;
- ordem de argumentos;
- `claimIds`, `factIds`, `authorityIds` e `issueIds`;
- objeção e resposta;
- consequência decisória;
- explicação de como difere da versão óbvia.

Diversidade válida exige simultaneamente:

- eixos primários distintos;
- distância mínima entre sequências de claims/ordem;
- referências válidas;
- ausência de tese ou autoridade nova.

### RF-05 — Grounding antes da redação

F5 deve classificar cada geometria:

- `grounded`;
- `partially_grounded`;
- `blocked`.

Geometria bloqueada não gera microbrief ou draft. `partially_grounded` só avança
se os gaps não atingirem questão, providência, tese central ou conteúdo
obrigatório e se a política congelada permitir.

### RF-06 — Microbriefs isolados e shortlist

F5-S deve produzir três microbriefs em sessões separadas, sem acesso entre si.
Cada um contém estrutura mínima, não peça integral.

A shortlist:

- registra os três artefatos e seus hashes;
- executa vetos preliminares;
- seleciona a melhor desafiante;
- calcula a margem objetiva de ambiguidade;
- mantém a segunda desafiante apenas para eventual terceiro draft;
- produz fallback válido para `candidate_0` se nenhuma superar o piso.

### RF-07 — Materialização de candidatos

F6-A deve produzir por padrão:

1. `candidate_0`: fluxo incumbente, sem artefatos de assinatura no prompt;
2. `candidate_1`: melhor desafiante.

O terceiro draft é permitido somente quando o critério de ambiguidade já
congelado for satisfeito antes da geração.

Cada candidato deve registrar:

- texto e SHA-256;
- snapshot;
- prompt e SHA-256;
- modelo, família e sessão;
- nível de garantia;
- proveniência por parágrafo;
- custo e latência;
- acesso a irmãos;
- vetos e status.

### RF-08 — Garantia de execução

O sistema deve distinguir:

- `envelope_verified`;
- `orchestrator_attested`;
- `self_declared`.

`orchestrator_attested` exige evidência de que o harness criou sessão nova,
forneceu prompt sem candidato irmão e persistiu o hash do prompt. Em modo
bloqueante, `self_declared` não comprova isolamento.

### RF-09 — Elegibilidade jurídica

Antes do julgamento editorial, cada candidato passa por:

- fatos e números;
- autoridades e fontes;
- pedidos e polaridade;
- cobertura obrigatória;
- origem operacional;
- placeholders;
- injeção;
- protocolo de voz humana existente.

P0 ou veto elimina. P1 permitido deve permanecer visível e não pode ser
renormalizado.

### RF-10 — Cegamento N-way

F6-B deve:

- canonicalizar textos;
- remover rótulos e metadados reveladores;
- armazenar mapping HMAC fora do workspace;
- balancear posições;
- executar comparações pareadas;
- exigir âncora literal;
- verificar hashes no momento da decisão;
- detectar vazamento, adulteração e viés de posição.

O protocolo atual A/B será reutilizado como base, não modificado para fingir
N-way.

### RF-11 — Independência de julgamento

Modos:

- `cross_family`;
- `cross_session_same_family`;
- `unverified`.

Política v1:

- preferir `cross_family`;
- permitir `cross_session_same_family` com sessões novas, prompts disjuntos,
  swap e correlação explícita;
- proibir mesma sessão e gerador julgando o próprio texto;
- em `unverified`, abster em modo bloqueante.

Nenhuma API paga nova é requisito da v1.

### RF-12 — Preferência preliminar conservadora

O algoritmo forma a matriz de preferência em três camadas:

1. vetos jurídicos;
2. preferência holística entre elegíveis;
3. estabilidade sob swap, juízes e margem.

A matriz pode identificar `blind_preferred`, mas ainda não promove texto. A
desafiante só substitui `candidate_0` depois dos gates de recall e steelman,
quando existe vencedor único e estável. Empate, ciclo, desacordo não resolvido,
baixa margem ou falha de garantia preservam o incumbente.

O menor hash nunca é critério de mérito.

### RF-13 — Recall fiel do corpo

O leitor recebe o candidato sem síntese executiva, removida por marcador
determinístico, e produz cartão de até 80 palavras. O verificador recebe apenas
o cartão e o mapa.

O diagnóstico procura:

- questão;
- âncora;
- regra/limite;
- consequência;
- providência.

Elemento falso é P0. Questão ou providência ausente impede a desafiante de
vencer. O recall não é prova de memória humana e não decide sozinho.

### RF-14 — Steelman

Cada candidato elegível deve confrontar o melhor argumento contrário
identificado no mapa. O teste verifica:

- fidelidade do argumento contrário;
- resposta lastreada;
- ausência de espantalho;
- efeito sobre a providência.

### RF-15 — Seleção final e cânone

Depois de RF-13 e RF-14, F6-C deve produzir
`F6_SIGNATURE_SELECTION.json` e promover exatamente um texto para
`draft_markdown`.

Os estados são distintos:

- `generated`;
- `legally_eligible`;
- `blind_preferred`;
- `selected_for_f7`;
- `audited_in_f7`;
- `finalized_in_f7b`.

Vencedor cego não significa política promovida nem peça liberada.

### RF-16 — Preservação em F7/F7-B

F7 pode corrigir juridicidade. Toda correção é classificada.

Se F7 mudar eixo, sequência de teses ou providência, a seleção fica stale e deve
ser revalidada. F7-B pode editar frase, transição, concisão e vocabulário, mas
não pode escolher nova geometria.

A topologia canônica usa:

- frase-mãe;
- teses;
- sequência de `claimIds`;
- ordem das seções;
- pedidos;
- polaridade.

Ela é insensível a fronteiras locais de frase.

### RF-17 — Invalidação append-only

Nenhuma decisão é sobrescrita. Alterações geram:

- `previousDecisionId`;
- `supersedes`;
- reason code;
- hashes anteriores e novos;
- escopo invalidado;
- ponto de reabertura.

### RF-18 — Memória decisória segura

Em produção v1:

- o sistema escreve selecionados e rejeitados;
- registra âncoras, razões, produto e linhagem;
- não copia conteúdo privado desnecessário;
- não injeta memória nos prompts de F4-S, F5-S ou F6-A.

Leitura ocorre somente no AUTO-RESEARCH offline, sob corpus, cegamento e gate de
promoção próprios.

### RF-19 — Budget e degradação

Antes de W2, um `budgetProfileId` deve resolver para limites numéricos de:

- chamadas por estágio;
- tokens de entrada e saída;
- tempo por estágio e por caso;
- drafts completos;
- juízes;
- comparações;
- retries.

Estouro:

- não pula gate;
- não promove desafiante incompleta;
- preserva `candidate_0`;
- registra reason code e consumo.

### RF-20 — Telemetria

Por caso e agregado:

- modo efetivo;
- taxa de abstenção;
- preferência por incumbente/desafiante;
- vetos por classe;
- estabilidade sob swap;
- garantia de independência;
- recall;
- custo e latência;
- alterações de F7/F7-B;
- falhas e fallback;
- missingness.

Sem média única de “qualidade”.

## 7. Requisitos não funcionais

### RNF-01 — Fail-closed

Hash ausente, schema inválido, snapshot divergente, mapping adulterado ou
proveniência insuficiente não pode ser convertido em warning em modo
bloqueante.

### RNF-02 — Determinismo do harness

Schemas, hashes, permutações, resolução de modo, diversidade estrutural,
invalidação e promoção devem ser determinísticos. LLM só participa dos passos
explicitamente generativos ou julgadores.

### RNF-03 — Privacidade

Nenhum conteúdo de caso é enviado a ambiente não autorizado. Mapping e chaves
ficam fora do workspace. Relatórios públicos usam apenas artefatos sanitizados.

### RNF-04 — Compatibilidade

- F0–F10 não são renumeradas;
- bundles históricos permanecem legíveis;
- `phase_contracts/F6.json` só muda no `default_on`;
- F8 continua consumindo um único `final_markdown`;
- `mode=off` preserva o output anterior.

### RNF-05 — Observabilidade

Toda alegação material de isolamento, modelo, decisão ou promoção deve apontar
para evidência persistida e recomputável.

### RNF-06 — Reversibilidade

Rollback é mudança de modo. Não apaga artefato, não reescreve histórico e não
reprocessa pacote já liberado.

### RNF-07 — Eficiência

Filtros determinísticos e grounding executam antes de drafts e juízes. Cache
somente para inputs hash-idênticos. Custo nunca é usado como sinal de qualidade.

## 8. Métricas e proteção contra Goodhart

### 8.1 Métricas de segurança

- regressão jurídica por dimensão;
- P0 por classe;
- alteração material detectada;
- integridade de hashes e snapshots;
- taxa de fallback por falha de garantia.

São vetos ou sentinelas, não metas de otimização.

### 8.2 Métricas de valor

- preferência cega estável sobre `candidate_0`;
- identidade do caso;
- clareza decisória;
- steelman;
- recall fiel do corpo;
- economia condicionada à cobertura;
- carga de correção humana em corpus de calibração.

Nenhuma isoladamente autoriza promoção.

### 8.3 Métricas operacionais

- tokens;
- chamadas;
- latência;
- custo marginal;
- taxa de terceiro draft;
- taxa de abstenção;
- disponibilidade de família;
- missingness.

### 8.4 Regra de evidência

Antes do primeiro caso prospectivo, registrar:

- estratos;
- mínimos por linhagem/produto;
- margem de preferência;
- métrica de concordância;
- regra sequencial de parada;
- tratamento de missingness;
- limites de custo;
- condições de invalidação.

O ponto de parada não pode ser escolhido depois de observar um resultado
favorável.

## 9. Rollout

### Etapa 0 — Baseline

- suíte viva verde;
- Régua verde ou desvio classificado;
- custo e latência incumbentes medidos;
- nenhum caso real alterado.

### Etapa 1 — Contratos em `off`

- schemas, reason codes, tipos puros;
- configuração;
- budget profile;
- nenhum modelo chamado;
- nenhum output F4–F8 alterado.

### Etapa 2 — F4-S em sombra

Checkpoint empírico. Prosseguir apenas se as geometrias mudarem arquitetura, não
apenas palavras, no corpus congelado.

### Etapa 3 — Esteira completa em sombra

O incumbente segue para F7. A camada registra o que escolheria.

Saída exige:

- denominadores pré-registrados atingidos;
- zero regressão jurídica detectada;
- detector material aprovado nos canários;
- swaps e hashes íntegros;
- custo dentro do perfil.

### Etapa 4 — `pilot_blocking`

Somente casos, produtos e tribunais autorizados. Falha de integridade bloqueia;
ausência de superioridade preserva incumbente.

### Etapa 5 — `default_on`

Exige:

- ganho prospectivo estável sobre `candidate_0`;
- regra sequencial satisfeita;
- ausência de regressão;
- política de independência real registrada;
- rollback exercitado;
- revisão independente;
- recibo humano da política.

A redação de cada caso não exige mão humana para selecionar a arquitetura.

## 10. Critérios de aceitação do produto

1. `off` é comportamentalmente idêntico ao fluxo anterior.
2. caso fora de `pilotCases` não é bloqueado; caso dentro falha fechado sem os
   artefatos.
3. `candidate_0` possui texto, snapshot e hash antes do cegamento.
4. abstenção promove exatamente o hash de `candidate_0` para F7.
5. dois candidatos nunca leem o texto um do outro.
6. autodeclaração não comprova isolamento em modo bloqueante.
7. geometria sinônima falha no detector estrutural.
8. fonte removida invalida todos os descendentes afetados.
9. mesma sessão gerando e julgando produz abstenção.
10. mapping adulterado ou vazado anula a rodada.
11. troca de posição não muda o hash vencedor; se mudar, há abstenção.
12. ciclo Condorcet preserva incumbente.
13. recall não recebe síntese executiva.
14. recall falso elimina desafiante.
15. F7-B não altera topologia, pedidos ou polaridade.
16. memória decisória não aparece em prompts de produção.
17. estouro de budget preserva incumbente sem pular gate.
18. promoção recompõe evidência em vez de confiar em `approved=true`.
19. `default_on` não é alcançável sem ganho prospectivo.
20. F8 e package continuam recebendo um único cânone validado.

## 11. Fora do escopo v1

- fine-tuning ou RLHF;
- imitação nominal de advogado;
- treinamento online com decisões de produção;
- API paga nova;
- renumeração F0–F10;
- alteração autônoma de leis, fatos, pedidos ou fontes;
- protocolo judicial externo;
- UI nova;
- sete drafts completos;
- score universal de “gosto”;
- alegação de memória humana baseada em recall de LLM.

## 12. Riscos de produto

| Risco | Consequência | Controle |
|---|---|---|
| alternativas só parecem diferentes | custo sem valor | diversidade estrutural + checkpoint W2 |
| juiz prefere verbosidade | texto inflado | comprimento controlado + economia condicionada |
| mesma família se auto-confirma | falsa autonomia | modo real de independência + swap + abstenção |
| recall vira stuffing | métrica enganada | síntese removida + falsidade como P0 |
| memória homogeneíza a prosa | colapso de diversidade | write-only em produção |
| F7 corrige e muda a tese | seleção stale | topologia + reabertura |
| custo explode | fila mais lenta | budget profile + early exit + fallback |
| ausência de erro vira “excelência” | promoção sem valor | ganho sobre `candidate_0` |

## 13. Decisões já tomadas

- a camada é aditiva;
- `candidate_0` ocupa um dos dois drafts padrão;
- segunda família é preferível, não dependência obrigatória;
- modo same-family é explicitamente correlacionado;
- memória não entra em prompts de produção v1;
- recall usa corpo sem síntese;
- preferência é holística após vetos;
- promoção da política é humana; seleção por caso pode ser autônoma;
- nenhum novo custo de API;
- ausência de vencedor preserva o fluxo vigente.

## 14. Critério de encerramento

O produto está pronto quando todos os critérios de aceitação estiverem
automatizados, o rollout completo tiver sido exercitado com rollback, e a
evidência prospectiva autorizar `default_on`. Implementação de código sem essa
evidência significa apenas **capacidade técnica disponível**, não produto
promovido.
