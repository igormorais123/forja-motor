# PRD — Disciplinas de processo importadas (skills da fábrica)

> **SUBSTITUÍDO EM 05/08/2026** por `planejamento/45_PRD_INSTRUMENTACAO_FORJA.md`,
> que unifica este documento com o outro PRD da mesma data. Permanece legível
> como anexo histórico: os requisitos detalhados e os critérios de aceite aqui
> escritos seguem valendo por incorporação, e não foram redigitados no 45.

**Versão:** 1.1  
**Protocolo:** `FORJA-SKILLS-PROCESSO-v1.1`  
**Data:** 05/08/2026  
**Estado:** aprovado somente como especificação de piloto observado; não autoriza promoção, bloqueio nem alteração de contrato de produção  
**Plano de origem:** `planejamento/43_PLANO_SKILLS_IMPORTADAS_ONDREJ.md`  
**Revisões independentes:** `state/prd44-revisao/PARECER_HELENA_CODEX.md`, `state/prd44-revisao/PARECER_DIABOB_CODEX.md` e `state/prd44-revisao/PARECER_EFESTO_CODEX.md`  
**Consolidação:** `state/prd44-revisao/CONSOLIDACAO_EFESTO.md`  
**Contexto do gate de diversidade:** `LAPIDACAO_VEREDITO_FINAL_2026-08-05.md`  
**Governança experimental:** `planejamento/22_PRD_AUTORESEARCH_FORJA.md` e `planejamento/23_TDD_AUTORESEARCH_FORJA.md`  
**Fonte externa:** `davidondrej/skills`, commit `04bd15abae135f5744e3dc825a4ab9c75d61fbfc`

## 1. Decisão de produto

A FORJA manterá as seis skills já adaptadas, mas as tratará como **seis
hipóteses de processo independentes**, e não como um pacote comprovado de
qualidade. A versão 1.1 autoriza preparar e executar somente um piloto
prospectivo em modo de observação, governado pelo ciclo AR. Ela não autoriza:

- inserir artefato novo em `requiredOutputs` ou gate novo em `requiredGates`;
- interromper uma fase porque uma disciplina não disparou;
- promover o conjunto por média ou por presença de arquivos;
- atribuir às disciplinas a correção do bloqueio vivo do F2A;
- chamar recibo estrutural de melhora jurídica ou operacional.

Cada disciplina poderá, ao final, ser promovida, mantida apenas como recurso
interativo ou retirada. Nenhuma das seis é descartada nesta especificação:

| ID | Disciplina | Papel em teste | Estado na v1.1 |
|---|---|---|---|
| D1 | `forja-briefing-revisor` | reduzir contaminação e reabertura de decisão rejeitada na pauta F4 | candidata a piloto observado |
| D2 | `forja-briefing-pesquisa` | reduzir falha de atribuição e de localização na pesquisa oficial F5 | candidata a piloto observado |
| D3 | `peticao-tres-escolhas` | explicitar hipóteses rivais depois de F1, sem estabilizar decisão jurídica | candidata de alto risco; hipótese sempre provisória |
| D4 | `peticao-decisoes-incertas` | tornar dúvidas materiais auditáveis entre F7 e F9 | candidata a piloto observado |
| D5 | `forja-handoff-caso` | reduzir reconstrução antes do despacho de revisão cruzada | candidata a piloto observado somente no pré-despacho |
| D6 | `forja-adr` | impedir redescoberta e reabertura silenciosa de decisão rejeitada | candidata a piloto observado; migração documental primeiro |

R7 (`stop_reason`) permanece como melhoria diagnóstica independente. R8 passa a
registrar a rejeição do classificador semântico. R9 é infraestrutura de
descoberta explícita. Nenhum dos três conta como evidência causal a favor das
seis disciplinas.

## 2. Problema

Há quatro problemas operacionais plausivelmente atacáveis pelas disciplinas:

1. pautas de conselho podem carregar a conclusão do construtor, omitir fonte
   decisiva ou reabrir proposta rejeitada;
2. pesquisa jurisprudencial pode atribuir trecho à autoridade errada, omitir
   localizador preciso, ignorar vigência ou não ligar o achado à proposição que
   o demandou;
3. o bloco “Pontos que exigem o seu olho” pode ser genérico, retrospectivo ou
   não chegar ao `email_response` produzido em F9;
4. revisão cruzada e decisões arquiteturais podem depender de reconstrução
   manual de contexto espalhado.

A v1.0 excedeu a evidência ao afirmar que seis disciplinas “fechavam” quatro
falhas. Elas podem reduzir parte desses riscos; isso ainda não foi observado
prospectivamente. A degradação substantiva do F2A também não é resultado que
este PRD possa reivindicar: continua sendo problema separado.

O segundo problema é experimental. A v1.0 media majoritariamente recibos que os
próprios requisitos mandavam produzir. Sem denominador de oportunidades
elegíveis, registro de não disparos, resultado material e custo, o placar fica
verde quando o formulário existe, mesmo que a falha de origem permaneça.

## 3. Linha de base F2A e decisão separada da Onda 0

### 3.1 Fato conferido pelo orquestrador

Foram executados os gates sobre todas as árvores localizadas no disco: **25
arquivos de árvore, referentes a 11 casos distintos, e os 25 reprovam
`exploration_100_complete`**. Em 21 arquivos, de 8 casos, as reprovações
limitam-se a `N4-Q-100-DIVERSITY` e, em vários deles, também
`N4-Q-100-NO-GAP`, ambos P1 e não mapeados nominalmente. Os outros 4 arquivos
reprovam por P0 legítimos de árvore incompleta ou stub.

Esse estado impede usar o fluxo real como bancada neutra do piloto. Ele não
prova nem refuta o mérito de D1–D6.

### 3.2 Opções reservadas ao Igor

| Opção | Efeito | Risco |
|---|---|---|
| **A — P1 observado, P0 bloqueante (recomendada)** | mapear diversidade e ausência de lacuna como `warn`, preservar bloqueio dos P0 e exigir árvore positiva aprovada mais teste ponta a ponta | evita parar caso legítimo enquanto a régua substantiva ainda não tem âncora positiva |
| B — formalizar P1 como bloqueante | manter a reprovação atual e documentar que diversidade é requisito de promoção | pode bloquear toda árvore real conhecida sem contraprova positiva aprovada |
| C — não alterar o F2A e restringir o PRD a ensaio histórico | adiar piloto prospectivo em rotas reais | preserva o estado, mas não produz denominador vivo nem testa sobrevivência ao volume |

**Decisão pendente:** Igor escolhe A, B ou C. Este PRD não altera código nem
antecipa a escolha. D3 não entra em caso prospectivo antes dessa decisão; D1,
D2, D4 e D5 podem ter ensaio histórico, mas não promoção.

## 4. Hipóteses falsificáveis por disciplina

| Hipótese | Oportunidade elegível | Resultado material esperado | Evidência que a refuta |
|---|---|---|---|
| H1 / D1 | cada despacho real de conselho F4 | menos propostas rejeitadas reapresentadas sem fato novo e menos omissões materiais confirmadas na auditoria humana | recibos perfeitos sem redução desses defeitos, ou perda de fonte útil causada pelo briefing |
| H2 / D2 | cada `propositionId` decisivo que exige pesquisa F5 | menos atribuições, trechos, localizadores ou estados de vigência corrigidos depois da pesquisa | seis campos completos e a mesma taxa de correção material da rota de comparação |
| H3 / D3 | caso após F1 com duas ou mais linhas materiais ainda abertas | hipóteses rivais úteis à F2A sem congelamento prematuro | hipótese contrariada pela fonte permanece tratada como decisão, ou custo/espera prejudica o fluxo |
| H4 / D4 | cada fechamento F7 | mais itens que levam a decisão, diligência ou correção humana e menos dúvidas materiais omitidas | listas formais consideradas genéricas, incorretas ou retrospectivas pelo revisor nominal |
| H5 / D5 | cada despacho de revisão cruzada | menor tempo de reconstrução, menos perguntas de identidade e menos erro de retomada | handoff consumido sem mudança desses resultados ou com conteúdo vencido |
| H6 / D6 | cada proposta de arquitetura/processo alcançada por decisão anterior | menos reabertura sem fato novo e menor tempo de reconstrução da decisão | fichas presentes e decisões rejeitadas reaparecendo na mesma taxa |

As seis hipóteses não compartilham denominador. “Dez casos” deixa de ser unidade
comum: a unidade é a oportunidade elegível definida em cada linha.

## 5. Escopo e não escopo

### 5.1 Escopo

- as seis skills existentes e sua ligação experimental ao consumidor correto;
- schemas, IDs estáveis, hashes e recibos temporais necessários ao piloto;
- ledger prospectivo de oportunidades, inclusive inelegibilidade e não disparo;
- canários de falha única e contraprovas reais aprovadas;
- ciclo AR para toda mudança em prompt, template ou protocolo apresentada como
  melhoria;
- R7 como observabilidade independente, R8 como rejeição registrada e R9 como
  descoberta explícita entre famílias.

### 5.2 Não escopo

- corrigir o gate F2A nesta entrega;
- RAG, LLM-as-judge como gate, RCT interno, governança de confidencialidade por
  IA, firewall de saída, visual 3D, `compor()` dentro do render;
- resolver cache editorial por SHA, gates visuais, citações existentes, render
  ou entrega;
- reconciliar integralmente `CLAUDE.md` e `AGENTS.md`;
- instalar skills globalmente ou reescrever as seis skills antes de evidência
  do piloto;
- declarar eficácia jurídica por avaliação do mesmo modelo que produziu o
  artefato.

## 6. Princípios de contrato e medição

1. **Observação não é contrato obrigatório.** Enquanto o runner não possui
   `optionalOutputs` ou `observedGates`, os artefatos do piloto ficam fora de
   `requiredOutputs` e `requiredGates`, em área experimental identificada.
2. **Produtor, consumidor e ordem precisam de recibo.** `mtime` não prova ordem.
   O ledger append-only registra evento, sequência, caminho e SHA-256 antes do
   consumo.
3. **Toda oportunidade deixa rastro.** Elegibilidade falsa e não disparo têm
   motivo; caso urgente não desaparece do denominador.
4. **Forma e mérito não se confundem.** Schema, ID, hash e sequência são
   computáveis. Omissão decisiva, utilidade jurídica, *ratio*/*dictum* e
   vigência material recebem decisão humana nominal e fonte, sem gate semântico
   por IA.
5. **Promoção é individual.** D1 não compensa falha de D3; R7 não melhora o
   placar causal de nenhuma disciplina.
6. **Ciclo AR prevalece.** Mudança de prompt, template ou protocolo só pode ser
   promovida com o recibo e os estados previstos no protocolo AR. Sem sealed
   prospectivo consumível, o resultado permanece `estudo_descritivo`.
7. **Canário tem contraprova.** Cada medidor deve reprovar a sabotagem nominal e
   aprovar artefato real aceito pela casa.

## 7. Requisitos e critérios de aceite

### R0 — Instrumento prospectivo antes da intervenção

Criar o schema do ledger de observação com, no mínimo:
`opportunityId`, `caseId`, `disciplineId`, `triggerEvent`, `eligible`,
`eligibilityReason`, `registeredAt`, `dispatchEvent`, `nonDispatchReason`,
`artifactPath`, `artifactSha256`, `consumerEvent`, `consumedSha256`,
`humanAudit`, `materialOutcome`, `costMinutes` e `schemaVersion`.

**Aceite:**

- cada evento de gatilho gera registro antes da possível execução;
- `eligible=false` exige motivo e permanece no censo;
- `eligible=true` sem despacho exige `nonDispatchReason`;
- o consumidor só conta como exposto quando o hash consumido coincide com o
  hash produzido e a sequência é posterior;
- fórmula, denominador, canários, contraprovas e auditor humano ficam congelados
  no registro AR antes do primeiro caso prospectivo;
- nenhum campo do piloto entra em `requiredOutputs` ou `requiredGates`.

**Mudança em relação à v1.0:** requisito novo. Fecha a ausência de denominador,
não disparo e vínculo temporal.

### R1 — Registro de decisões operante

Criar `_FORJA_HARNESS/decisoes/` e migrar as 13 decisões inventariadas pela skill
`forja-adr`, com ID estável, status, fonte, evidência, consequência e critério de
reabertura. O índice da FORJA aponta a pasta.

**Aceite:** 13 fichas; IDs únicos e estáveis; status em vocabulário fechado;
toda rejeição aponta sua fonte e seu critério de reabertura; a fidelidade da
migração é conferida por leitor humano contra o documento de origem; linter
estrutural não é gate de produção durante o piloto.

**Mudança em relação à v1.0:** mantido, com IDs estáveis e separação entre
validação estrutural e fidelidade histórica humana.

### R2 — Briefing cego ligado ao despacho F4

Antes de cada despacho de conselho F4, o produtor experimental gera briefing
com três perguntas obrigatórias, fontes primárias por caminho e hash, restrições
relevantes e IDs de decisões já tomadas ou rejeitadas. O recibo de despacho leva
o SHA-256 do briefing; a resposta do revisor ou seu envelope repete o hash
consumido.

**Aceite:** schema válido; briefing anterior ao despacho por sequência
append-only; hashes coincidentes; IDs de decisão resolvíveis; mutações que
retiram uma pergunta, uma fonte ou a lista de rejeitados são detectadas;
contraprova real aprovada não é bloqueada. Auditor nominal decide se houve
omissão ou contaminação material.

**Mudança em relação à v1.0:** “arquivo presente” deixa de bastar. O requisito
passa a provar produção anterior e consumo, sem tornar o artefato obrigatório no
contrato durante o piloto.

### R3 — Pesquisa oficial F5 nasce de briefing e usa um fluxo de ledgers

O briefing de pesquisa pertence à F5. F4 produz o `proposition_ledger`, que é a
fonte canônica das demandas de pesquisa. F5 consome seus `propositionId` e
produz o `source_ledger`, fonte canônica dos achados. U6/
`F5_LEDGER_MATERIAL.json`, enquanto existir, é somente projeção derivada desses
IDs; não recebe segunda digitação e não escreve de volta em F4.

Cada achado decisivo traz, no mínimo:

1. identificação completa da autoridade e do precedente;
2. fonte oficial arquivada com caminho e hash;
3. localizador preciso ou *pincite*;
4. trecho exato conferível;
5. função e situação do precedente, incluindo a classificação e vigência que
   exigirem revisão humana;
6. `propositionId` e razão objetiva de relevância.

**Aceite:** briefing registrado antes do primeiro evento de busca; todo
`propositionId` decisivo tem achado ou bloqueio justificado; verbatim confere com
a fonte arquivada; U6 reproduz os IDs canônicos sem divergência; mutação que
troca verbatim entre precedentes é detectada; julgamento material permanece em
recibo humano nominal.

**Mudança em relação à v1.0:** R3 sai de F3 e passa a F5. A ambiguidade entre
`proposition_ledger`, `source_ledger` e U6 é resolvida por direção única e
projeção, não por sincronização bidirecional.

### R4 — Três escolhas viram hipóteses provisórias depois de F1

`peticao-tres-escolhas` não roda no primeiro contato. Depois de F1, quando o
acervo mínimo estiver identificado e restarem duas ou mais linhas materiais, a
disciplina pode gerar `F2_INTAKE_HYPOTHESES.json`. Recomendações do agente e
respostas humanas são hipóteses de exploração, nunca decisão jurídica
vinculante. Toda hipótese é revalidada contra F1/F2A e pode ser reaberta em
qualquer fase quando surgir fonte ou contradição.

**Aceite:** IDs de hipótese resolvíveis na árvore F2A; status explícito
`provisional`, `confirmed`, `rejected` ou `reopened`; referências às fontes de
revalidação; alternativa rejeitada com motivo; hipótese contrariada pela fonte
é reaberta, não congelada; ausência de resposta humana gera não disparo e não
interrompe rota automatizada.

**Mudança em relação à v1.0:** mudou de triagem decisória anterior à fonte para
elicitação provisória após F1. Cai a regra de escolha que “não se reabre”.

### R5 — Decisões incertas têm ponte explícita F7 → F9

Antes do fechamento F7, produzir `F7_UNCERTAIN_DECISIONS.json` com ID, decisão,
alternativa, motivo, localizador e, quando vazio, justificativa nominal. F9
produz mapa interno que liga cada ID pertinente ao trecho e à página do
`email_response`. O e-mail não precisa expor IDs internos.

**Aceite:** conjuntos de IDs conciliados; páginas/localizadores válidos; trecho
normalizado encontrado no e-mail; evento F9 posterior ao artefato F7; item
resolvido ou superado tem status atualizado, não é copiado como dúvida vencida;
auditor humano classifica utilidade, correção, omissão e fabricação
retrospectiva.

**Mudança em relação à v1.0:** a ponte antes implícita recebe artefato, IDs,
estado e consumidor definidos. Presença da lista continua sendo adoção, não
resultado.

### R6 — Handoff somente antes do despacho de revisão cruzada

`forja-handoff-caso` produz `state/<caseId>/HANDOFF.md` antes do despacho real de
revisão cruzada. O recibo de despacho registra hash do handoff, versão do estado
e evento consumido.

**Aceite:** handoff com identidade, estado, fontes, armadilhas e pendências;
hash anterior ao despacho; versão de estado coerente; revisor recebe o mesmo
hash. Tempo de reconstrução, perguntas básicas e erros de retomada são métricas
humanas separadas.

**Mudança em relação à v1.0:** cai “toda troca de contexto/encerramento de
sessão”, porque o runner não possui esse evento. O requisito fica restrito ao
pré-despacho verificável.

### R7 — Recibo de tentativa editorial preserva `stop_reason`

R7 é patch de observabilidade independente. O recibo de tentativa precisa ser
gravado assim que o envelope retorna, antes de parse, fidelidade ou qualquer
exceção que possa encerrar a execução. No sucesso, o mesmo recibo é enriquecido.

**Aceite:** testes de sucesso com valor, sucesso sem campo gravando `null`,
recusa/saída inválida preservando o valor antes do erro e divergência de modelo
continuando bloqueada; hashes finais nulos em tentativa não concluída; o campo
não altera os invariantes textuais.

**Mudança em relação à v1.0:** deixa de ser gravação tardia no `editor_usage` e
passa a cobrir o caminho real de recusa. Sai do argumento causal e das métricas
de eficácia das seis disciplinas.

### R8 — Rejeição registrada do classificador semântico de instruções

Registrar em ficha R1 que **não será construído** classificador automático de
trechos em núcleo comum, específico-Codex e específico-Claude. Classificação de
texto livre criaria nova fonte semântica sujeita a deriva. Se houver necessidade
futura, ferramenta separada pode calcular somente hashes e diffs determinísticos,
sem classificar o mérito.

**Aceite:** ADR com decisão `Rejeitada`, motivo, fonte e critério de reabertura;
nenhum `forja_divergencia_instrucoes.py` sem nova decisão expressa.

**Mudança em relação à v1.0:** a proposta aberta cai. R8 vira registro de
rejeição, não compromisso de software.

### R9 — Descoberta explícita para Codex e Claude

Documentar no `AGENTS.md` aplicável uma tabela com as seis skills, caminho,
gatilho, modo automático ou explícito/manual e o artefato/contrato que prevalece.
R4, R5 e R6 não podem ser anunciadas como disparo automático enquanto o
frontmatter o desabilitar.

**Aceite:** seis caminhos existentes e seis entradas válidas; linter estrutural;
smoke prospectivo em sessão Codex limpa e sessão Claude limpa; pergunta indireta
para skills automáticas e comando explícito para as manuais. Descoberta não
conta como consumo nem eficácia.

**Mudança em relação à v1.0:** R9 sobe para a Onda 0 e abandona a afirmação
absoluta, não comprovada, de que o runtime headless jamais descobre skill. A
justificativa passa a ser acoplamento explícito e auditável.

## 8. Ondas de execução

### Onda 0 — baseline, instrumentos e decisões

Sem integração das disciplinas na produção:

1. obter a decisão de Igor sobre o F2A (§ 3);
2. congelar R0, schemas, IDs, fórmulas, canários e contraprovas;
3. abrir o registro do ciclo AR e confirmar se há sealed prospectivo
   consumível;
4. executar R1 documental, registrar a rejeição R8 e preparar a descoberta R9;
5. tratar R7 em trilha independente, sem crédito no piloto;
6. testar os medidores contra canários: verbatim trocado, fonte decisiva omitida,
   hesitação retrospectiva e handoff sem a armadilha material.

**Saída:** instrumento apto a observar, nenhum contrato bloqueante novo e
decisão F2A registrada.

### Onda 1 — ensaio assistido de três oportunidades elegíveis por disciplina

Executar a variante apenas no ambiente experimental previsto pelo ciclo AR. Os
artefatos ficam fora dos contratos obrigatórios. Registrar todos os gatilhos,
inclusive inelegibilidade e não disparo. Corrigir apenas defeitos do instrumento;
não promover disciplina.

**Saída:** três oportunidades elegíveis por disciplina ou declaração explícita
de denominador insuficiente; canários e contraprovas aprovados.

### Onda 2 — piloto prospectivo observado

Executar por 30 dias. Somente a disciplina que acumular pelo menos dez
oportunidades elegíveis poderá ter leitura exploratória de resultado; abaixo
desse piso, o resultado permanece inconclusivo e não há extensão automática.
Separar adoção, resultado material e custo; preservar não disparos.

**Saída:** ledger congelado, auditorias humanas nominais e relatório por
disciplina. Dez oportunidades são piso descritivo, não substituto do ciclo AR.

### Onda 3 — decisão individual de promoção

Para cada disciplina, registrar um dos três estados: `promover`,
`continuar_estudo` ou `retirar`. Promoção de prompt, template ou protocolo exige
recibo válido do ciclo AR, canários mortos, contraprovas preservadas, ausência de
regressão material e custo aceito. Somente depois disso a disciplina pode entrar
em `requiredOutputs`/`requiredGates` ou em injeção obrigatória de produção.

Não existe promoção do pacote por média. R7, R8 e R9 não entram no placar.

## 9. Métricas

### 9.1 Denominadores e fórmulas comuns

- `N_considered`: todos os eventos de gatilho avaliados após o início do piloto;
- `N_eligible`: eventos com `eligible=true` e motivo congelado;
- `N_dispatched`: elegíveis com recibo de despacho;
- `N_consumed`: elegíveis cujo consumidor confirma o mesmo SHA-256;
- `N_non_dispatch`: elegíveis sem despacho, sempre com motivo;
- `N_human_audited`: elegíveis com decisão humana nominal e fonte.

Fórmulas:

- adoção verificável = `N_consumed / N_eligible`;
- não disparo = `N_non_dispatch / N_eligible`;
- cobertura de auditoria = `N_human_audited / N_eligible`;
- custo = mediana e maior valor observado de minutos por oportunidade, sem
  excluir urgências;
- resultado material = fórmula própria da disciplina, abaixo.

Denominador zero produz `não aplicável`, nunca 100%.

### 9.2 Resultado por disciplina

| Disciplina | Métrica de resultado | Fonte |
|---|---|---|
| D1 | propostas rejeitadas reapresentadas sem fato novo por parecer com proposta pertinente; omissões materiais confirmadas por briefing consumido | parecer, ADR, fonte primária e recibo humano |
| D2 | achados corrigidos por atribuição, verbatim, *pincite*, vigência ou relevância por `propositionId` auditado | `source_ledger`, fonte oficial e auditoria humana |
| D3 | hipóteses contraditas pela fonte que foram reabertas; hipóteses contraditas que permaneceram ancoradas | artefato F1/F2, árvore F2A e decisão humana |
| D4 | itens que geraram decisão/diligência/correção e dúvidas materiais omitidas por F7 auditado | lista F7, mapa F9 e auditoria humana |
| D5 | minutos de reconstrução, perguntas de identidade e erros de retomada por despacho | recibo de revisão e registro nominal do revisor |
| D6 | propostas rejeitadas reabertas sem fato novo e minutos gastos reconstruindo decisão | ADR, proposta e auditoria humana |

Métricas estruturais devem atingir 100% de vínculo quando o artefato for
produzido e detectar 100% dos canários nominados. Isso prova o instrumento, não
o benefício. Resultado material só sustenta promoção quando superar a
comparação pré-registrada no AR sem regressão e com custo aceito. Na ausência de
sealed prospectivo, o relatório é descritivo e não promove nada.

## 10. O que mudou da v1.0 e por quê

| Tema | v1.0 | v1.1 | Motivo |
|---|---|---|---|
| Estado | especificação para execução | piloto observado, sem promoção ou bloqueio | os três pareceres rejeitaram execução literal |
| Hipótese | seis disciplinas fecham quatro falhas | seis hipóteses independentes | não há evidência causal comum |
| F2A | contraparte fora de escopo, sem efeito no rollout | bloqueio vivo registrado em Onda 0 separada | 25/25 árvores reprovam o gate atual |
| Onda sem bloqueio | contrato exigiria artefato sem bloquear | artefato experimental fora de `requiredOutputs`/`requiredGates` | esse estado intermediário não existe no runner |
| R3 | pesquisa em F3 e tabela de lastro ambígua | pesquisa em F5; F4 demanda, F5 responde e U6 projeta | contratos vivos confirmam F3/F4/F5 |
| R4 | escolha no primeiro contato alimenta F2A | hipótese provisória depois de F1, sempre revalidável | evitar ancoragem jurídica anterior à fonte |
| R5 | lista F7 alimentaria e-mail sem ponte | IDs e mapa explícito F7 → F9 | `email_response` é produto de F9 |
| R6 | toda troca de contexto | somente pré-despacho de revisão cruzada | não existe evento de encerramento de sessão no runner |
| R7 | campo tardio e métrica do pacote | recibo anterior ao parse, trilha diagnóstica independente | a recusa ocorre antes da gravação literal proposta |
| R8 | classificador semântico aberto | classificador rejeitado por ADR | custo e nova fonte de verdade sem benefício demonstrado |
| R9 | espelhamento tardio e afirmação absoluta de invisibilidade | descoberta explícita na Onda 0, com smoke por runtime | falta de injeção auditável é o fato sustentado |
| Métricas | presença e dez casos comuns | elegibilidade, não disparo, resultado e custo por disciplina | evitar recibo de rigor tratado como prova de rigor |
| Governança | decisão por ADR após dez casos | ciclo AR obrigatório e decisão individual em três estados | protocolo vigente da casa não pode ser substituído |

## 11. Riscos e controles

| Risco | Controle |
|---|---|
| F2A bloquear toda rota real e contaminar o baseline | decisão separada da Onda 0; nenhum efeito atribuído às skills |
| formulário retrospectivo convincente | sequência append-only, canário de falha única e auditoria humana nominal |
| seleção dos casos fáceis | censo de todos os gatilhos, inclusive inelegíveis e não disparos |
| briefing criado sem consumo | SHA-256 no despacho e no recibo do consumidor |
| duas fontes de verdade em pesquisa | direção única `proposition_ledger` → `source_ledger`; U6 somente projeção |
| ancoragem de D3 | execução depois de F1, status provisório, reabertura obrigatória e nenhuma espera bloqueante |
| julgamento semântico automatizado | IA não decide mérito como gate; decisão humana com fonte |
| custo sob prazo | minutos por oportunidade incluem urgências; disciplina pode ser retirada individualmente |
| circularidade de autoria | comparação e auditoria pré-registradas; autor do artefato não valida sozinho o resultado material |
| promoção por métrica verde | promoção individual, AR, canários, contraprovas e resultado material |

## 12. Decisão sobre os três pareceres

- **Helena — acatado em parte.** Acatados: bloqueio F2A como baseline separado,
  F3 → F5, hipóteses e denominadores próprios, métricas de resultado/custo,
  ciclo AR, R4 provisório e vínculo temporal por hash. Não foi acatada a
  inclusão da correção de cache editorial por SHA: é problema válido, porém
  fora do escopo deste produto. A correção do F2A também não foi executada; por
  ordem do dono, virou decisão autônoma da Onda 0.
- **Diabob — acatado em parte.** Acatados: piloto observado, distinção entre
  recibo e resultado, registro de não disparos, canários, crítica causal,
  correções R3/R5 e mudança de natureza de R7/R8. Rejeito retirar D3 antes de
  testá-la: ela permanece, mas foi reduzida a hipótese provisória pós-F1, sem
  poder vinculante e com critério explícito de retirada.
- **Efesto — acatado em parte.** Acatados: inexistência de contrato
  observacional no runner, topologia F3/F4/F5, schemas/IDs, ponte F7 → F9,
  recorte pré-despacho de R6, recibo antecipado de R7, métricas humanas separadas
  e rejeição do classificador R8. O parecer anterior foi endurecido: a
  implementabilidade técnica deixou de bastar para autorizar produção; o ciclo
  AR e o denominador prospectivo agora precedem qualquer promoção.

O detalhamento de cada aceite, rejeição e mudança de opinião está em
`state/prd44-revisao/CONSOLIDACAO_EFESTO.md`.

## 13. Pendências e decisões abertas

1. **Igor:** escolher A, B ou C para o F2A (§ 3.2).
2. **Igor:** nomear o auditor humano do resultado material e o custo aceitável
   por disciplina antes do registro AR.
3. **Execução futura:** comprovar se existe sealed prospectivo consumível. Se
   não existir, manter `estudo_descritivo`.
4. **Após o piloto:** decidir D1–D6 individualmente em `promover`,
   `continuar_estudo` ou `retirar`.

Não há decisão técnica pendente sobre fase, ledger, R6, R7 ou R8 nesta versão.
