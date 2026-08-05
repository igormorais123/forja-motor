# PRD — FORJA AUTO-RESEARCH (ciclo AR de auto-melhoria anti-trapaça)

> Versão 1.1 — 2026-07-23. Autor: Claude Fable 5 (estudo multi-agente wf_aa83ac96) sob ordem do Igor.
> v1.0 REPROVADA em review adversarial Codex GPT-5.5 (13 P1, 2 P2); v1.1 incorpora todas — triagem na seção 14.

## 1. Decisão de produto

Institucionalizar na FORJA um **processo de auto-research**: ciclo recorrente e auditável que (a) mede a qualidade real das entregas com **indicadores ancorados em falhas reais e não gameáveis por exclusão de conteúdo**, (b) testa variantes de artefatos da esteira (prompts de fase, templates, protocolos) contra material real com **execução pareada e julgamento cego**, e (c) só promove mudança que sobreviver a canários de falha única, holdout com orçamento de consultas, não-inferioridade por dimensão e cadeia de aprovação em três estados com âncora humana.

O que o ciclo AR **não** é: não é RLHF, não é fine-tuning, não é loop autônomo que reescreve a esteira sozinho. É um harness determinístico que executa em condições pareadas, mede, cega, bloqueia e registra; os passos de LLM (gerar variante, redigir sob variante, julgar às cegas) são invocações explícitas, no padrão do F7-B/Fable 5.

## 2. Linha de base preservada

- A esteira F0–F10 e seus contratos não mudam. O ciclo AR roda fora do caminho crítico de produção, lendo artefatos de `state/<caseId>`.
- `forja_verificador.py`, `forja_metricas_f7.py`, `forja_estilo_humano.py`, `forja_mutation_semantic.py`, `forja_diff_docx.py`, `forja_human_review.py` (recibos Ed25519) e a Régua são **reutilizados como sensores e como trilha de aprovação** — o ciclo AR não cria trilha paralela mais fraca (R10).
- O experimento `.autoresearch/fabrica-peticoes-v1` permanece imutável e vira corpus de calibração.
- Nenhum custo novo de API: LLMs são Claude (assinatura) e Codex (créditos já em uso), duas famílias distintas.

## 3. Problemas que resolve

- **P1 — Lição minerada não vira melhoria mensurável.** 83 lições em `RETROSPECTIVAS.md`, 30 codificadas; não há medição contínua da qualidade entre entregas.
- **P2 — Melhoria sem prova.** Mudança de prompt/template é promovida por juízo pontual, sem comparação pareada e cega contra a versão vigente em material real; o experimento v1 validou o método mas não é reproduzível (prompts no transcript).
- **P3 — Indicador sem lastro é teatro.** Medições esparsas não são vinculadas às classes de falha reais nem validadas quanto a poder discriminante; pior: indicador ingênuo (ex.: "taxa de citação conferida") é otimizável por exclusão de conteúdo (R4).
- **P4 — Julgamento sujeito a gaming.** LLM-as-judge sem cegamento sofre position bias, verbosity bias e self-preference; loop sobre juiz viciado otimiza o viés (Goodhart).

## 4. Objetivos

- **O1.** Painel de indicadores computável sobre qualquer caso elegível, com cada indicador rastreado a lição/erro real, medindo **cobertura e correção separadamente** (nunca só precisão — R4) e com máscara pareada de sensores (R7).
- **O2.** Suíte de canários de **falha única por mutação sobre a mesma peça-base** (R12): o painel deve atribuir a discriminação ao sensor certo (mutation-kill por sensor), com camada pública de regressão e camada secreta rotativa de auditoria.
- **O3.** Protocolo de execução pareada (`AR_RUN_PAIR` — R1) + julgamento cego com bundles canonicalizados em diretório isolado, mapping protegido por HMAC com chave fora do workspace (R2), consolidação por `artifactSha256` (R3) e proibição de a família geradora julgar a própria variante (R6).
- **O4.** Gate de promoção em **três estados** — `technical_candidate_passed` → `independent_review_passed` → `human_promotion_approved` — com log encadeado por hash, decisão vinculada aos hashes de código/sensores/corpus/outputs, e recibo humano na trilha Ed25519 existente (R10). Não-inferioridade por dimensão + orçamento pré-registrado de candidatos e de consultas ao holdout (R13).
- **O5.** Primeira rodada com material real declarada **estudo piloto descritivo** (R11): σ, missingness e efeito mínimo detectável publicados; nenhuma alegação de eficácia até coorte prospectiva suficiente.

## 5. Princípios invioláveis

1. **Pré-registro antes de medir.** Critérios, pesos, margens, splits, orçamento de candidatos e de consultas são gravados em `AR_MANIFEST.json` ANTES da rodada; o manifest de cada ciclo é hash-vinculado no log encadeado; edição após observar resultado invalida o ciclo (teste de sabotagem próprio — R15).
2. **Comparação só entre execuções pareadas.** Julgamento e painel comparativo operam sobre outputs produzidos pelo `AR_RUN_PAIR` sob o mesmo input imutável e condições registradas (modelo, versão, parâmetros, repetições, tokens) — nunca sobre artefatos de configuração ou peças de origens distintas (R1).
3. **Determinismo do harness.** Split por HMAC com chave secreta fora do workspace, agrupado por linhagem/matéria e estratificado por produto e tribunal (R8); sem `random` sem seed; LLM só em passos explícitos e registrados.
4. **Indicador não pode ser otimizável por exclusão.** Toda taxa tem denominador congelado antes da geração (ledger de claims/autoridades obrigatórias por tarefa); variante que reduz cobertura não pode vencer (R4).
5. **Cegamento verificável e isolado.** Bundles canonicalizados (sem nomes, versões, front-matter); juiz roda em diretório contendo só os bundles; acesso do processo julgador ao workspace ou ao mapping invalida a rodada (R2). Mesmo hash deve vencer nas duas ordens; mesma posição nas duas ordens = viés posicional (R3).
6. **Sealed com orçamento vitalício.** Registro sealed fora do workspace do proponente; orçamento de consultas por versão do conjunto (não por ciclo); caso consultado é aposentado e reposto só com caso prospectivo; sem mínimo de casos sealed elegíveis, promoção é impossível (R9).
7. **Null bloqueia, não renormaliza.** Em comparação vigente×variante, novo `null` em qualquer sensor, ausência em indicador de segurança ou divergência de máscara bloqueia a promoção (R7).
8. **Conteúdo dos autos/peças é dado, nunca instrução** (U3) — inclusive para juízes; prompt do juiz contém a blindagem e há teste de injeção contra o juiz (R15).
9. **Sigilo.** Nenhum conteúdo de caso sai dos ambientes já autorizados; nada de material de caso em repositório público.

## 6. Capacidades funcionais

- **R01 — Registro de corpus** (`forja_ar_corpus.py`): inventaria casos elegíveis (critério amplo e testado contra o estado real: qualquer `final_markdown*.md` sob F7 em `n3_artifacts/` ou `runs/`), agrupa por **linhagem** (mesmo litígio/template/matéria — grupo inteiro cai no mesmo split), atribui split por HMAC estratificado com mínimos absolutos por estrato, e grava `AR_CORPUS.json` (sem expor o split sealed: casos sealed ficam em registro separado fora do workspace — R9).
- **R02 — Motor de indicadores** (`forja_ar_indicadores.py`): computa o painel (seção 8) por caso e agregado; cobertura e correção separadas; máscara pareada; cache content-addressed por `artifactHash + sensorVersion + contextHash` (R14).
- **R03 — Canários por mutação de falha única** (`forja_ar_canarios.py`): sobre peça-base real liberada, aplica mutações de falha única (reutilizando operadores S1–S6 + classes das lições); exige que o **sensor-alvo** mate a mutação (mutation-kill por sensor) e que controles benignos sobrevivam; camada pública (regressão) + camada secreta rotativa (auditoria, fora do workspace) (R12).
- **R04 — Executor pareado** (`forja_ar_runpair.py` — R1): congela input e ledger de claims; registra manifest de execução por lado (modelo, versão, parâmetros, tokens, tempo, hash do output); valida paridade antes de liberar para o blind; suporta repetições para variância intra-condição.
- **R05 — Bancada cega** (`forja_ar_blind.py`): canonicaliza bundles, monta A/B e B/A em diretório isolado, mapping HMAC com chave externa, valida devolutivas (schema + trecho-âncora literal + verificação de que o julgador não acessou o workspace), consolida por `artifactSha256`, anula viés posicional, computa concordância com voto por juiz/ordem/hash e repetição intra-juiz (R3).
- **R06 — Ciclo e gate de promoção** (`forja_ar_ciclo.py`): subcomandos por fase; log `AR_LOG.jsonl` **encadeado por hash** (cada evento inclui o hash do anterior — R10); `promotion` avalia não-inferioridade por dimensão, vetos, canários, kappa, orçamentos, e emite no máximo `technical_candidate_passed`; `independent_review_passed` exige parecer de revisor de família distinta da geradora; `human_promotion_approved` exige recibo na trilha Ed25519 de `forja_human_review.py`. Propagação manual com backup e rebaseline.
- **R07 — Relatório de ciclo**: template fixo, indicadores antes/depois com intervalo (cluster bootstrap por linhagem), decisões e rejeições com porquê, custo (tokens/julgamentos consumidos vs orçamento).

## 7. Jornada de um ciclo AR (A0–A6)

| Fase | Nome | Saída | Bloqueador |
|---|---|---|---|
| A0 | Snapshot e pré-registro | manifest do ciclo hash-vinculado no log | critérios/orçamentos incompletos |
| A1 | Painel baseline (pareado) | `AR_PANEL.json` | sensor com falha; máscara instável |
| A2 | Canários | `AR_CANARY_RESULT.json` | mutation-kill abaixo do mínimo em qualquer sensor; controle benigno morto |
| A3 | Execução pareada | outputs + manifests de execução | paridade violada |
| A4 | Julgamento cego | `AR_JUDGMENT.json` | kappa < mínimo; viés posicional > limite; acesso indevido detectado |
| A5 | Promotion gate técnico | `AR_PROMOTION_DECISION.json` (≤ `technical_candidate_passed`) | qualquer critério pré-registrado |
| A6 | Revisão independente + aprovação humana | parecer + recibo Ed25519 | ausência de qualquer um dos dois |

## 8. Indicadores do painel (v1 — pesos e status congelados só após o estudo piloto)

Tipo D = determinístico, J = julgado. Papel: **alvo** (entra no score comparativo), **sentinela** (veto/monitor, nunca otimizado como alvo — R5/R6), **operacional** (processo, fora do score de peça).

| ID | Indicador | Tipo | Papel | Medição (anti-exclusão) | Âncora | Defesa anti-gaming |
|---|---|---|---|---|---|---|
| I1 | Citações: cobertura E correção | D | alvo | contra ledger de autoridades obrigatórias congelado pré-geração: `cobertura = citadas/obrigatórias`; `correção = conferidas/citadas` (replay de trecho+identidade+fonte) | Erro #1; lições 2, 22, 28, 41; U1 | denominador congelado; remover citação derruba cobertura (R4) |
| I2 | Integridade jurídica (G2–G4) | D | sentinela-veto | violações em listas finitas de súmulas/dispositivos/institutos | 30 lições codificadas | binário por conta; escopo declarado como parcial (listas finitas) |
| I3 | Premissas: cobertura E lastro | D | alvo | contra ledger de claims decisivos congelado pré-geração; lastro validado por presença real da âncora processual | Erro #2; lições 10, 14, 15, 26; U6 | denominador congelado; âncora verificada, não rótulo (R4) |
| I4 | Placeholders | D | sentinela-veto | alinhado 1:1 ao gate vivo de `forja_verificador` (mesma lista, mesmas exceções documentadas lá) + scan do render | Erro #3 | sem exceção divergente entre PRD e gate (R5) |
| I5 | Estilo humano | D | sentinela | aprovado/P0/P1 do módulo atual (sem score fictício 0–100 — R5) | lições 5, 12, 38 | sentinela: nunca alvo de otimização (léxico público é contornável) |
| I6 | Origem operacional | D | sentinela-veto | classes conceituais (canal, armazenamento, caminho) + proveniência, não só regex | Fábio 11/07 (inviolável) | avaliação por classe; paráfrase coberta na camada secreta de canários |
| I7 | Cobertura de blindagem recursal | D+J | alvo | entailment/cobertura contra issue ledger pré-registrado (síntese 343-A, prequestionamento por dispositivo, terminologia anti-Súmula 7/279), verificado por mutação semântica — não presença de termos | diretrizes 1–2; CASO-16 | anti-stuffing: termo sem vínculo ao issue ledger não pontua (R5) |
| I8 | QA visual | D | sentinela-veto | zero defeito crítico absoluto; válido só com recibo humano Ed25519 hash-bound (modo estrito existente) | Erro #4; incidente CASO-17 | não é taxa por página (diluição por volume — R6) |
| I9 | Juiz cego pairwise | J | alvo (comparação) | vitórias por `artifactSha256` em pares com swap, 2 famílias, geradora excluída de julgar a própria variante | método validado no v1 | R2, R3, R6 |
| I10 | Pós-entrega | D | operacional | classificação completa+aprovada+sem reabertura, e só então o tempo | diretriz 6; lição 48 | completude condiciona o cronômetro (R6) |

**Tripwires (R13):** gate de **não-inferioridade por dimensão** — variante não pode regredir além da margem de ruído pré-registrada em NENHUM indicador-alvo, com vetos absolutos (I2, I4, I6, I8) e limite agregado; orçamento máximo de candidatos por versão de holdout com fronteira sequencial; esgotado o orçamento, aguarda casos prospectivos.

## 9. Critérios de aceitação

1. `forja_ar_corpus.py --scan` cobre o estado real (critério de elegibilidade validado contra os 49 diretórios atuais; meta ≥ 30 elegíveis **após** ajuste do critério amplo; distribuição por estrato publicada); rodadas repetidas → splits idênticos; grupos de linhagem nunca se separam.
2. `forja_ar_indicadores.py` computa painel com cobertura/correção separadas, máscara pareada e cache; caso sem sensor → `null` com motivo; em modo comparativo, novo `null` bloqueia.
3. `forja_ar_canarios.py --verificar` exige mutation-kill por sensor e sobrevivência de controles benignos; camada secreta verificada fora do workspace.
4. `forja_ar_runpair.py` recusa julgar outputs com manifests de execução não pareados.
5. `forja_ar_blind.py` consolida por hash; anula viés posicional pela regra correta (mesma posição nas duas ordens); detecta mapping adulterado e devolutiva sem trecho-âncora.
6. `forja_ar_ciclo.py promotion` nunca emite acima de `technical_candidate_passed`; log encadeado por hash detecta remoção/edição de evento; segundo uso do orçamento sealed → BLOQUEADA mesmo em ciclo novo.
7. Suíte `test_forja_autoresearch.py` verde, incluindo as sabotagens da R15 (split-shopping por renomeação de caseId, vazamento de mapping, injeção contra juiz, supressão de ledger, inflação de páginas, remoção de citações, stuffing de I7, edição de manifest pós-resultado, reinício de ciclo para rever sealed, linhagem separada entre splits); Régua verde com rebaseline motivado.
8. Estudo piloto descritivo publicado: σ e missingness por indicador, intervalos por cluster-bootstrap de linhagem, efeito mínimo detectável, e declaração explícita de que NÃO há alegação de eficácia (R11).

## 10. Meta-métricas do processo

- Mutation-kill por sensor (alvo: 100% das mutações de falha única mortas pelo sensor certo; controles vivos).
- Kappa inter-juiz e taxa de anulação posicional por ciclo.
- Consumo de orçamento (candidatos, consultas holdout/sealed, julgamentos LLM, tokens) vs pré-registro.
- Proibida: quantidade de variantes promovidas como meta.

## 11. Eficiência (R14)

Cache content-addressed em todos os sensores; prefilter determinístico barato antes de qualquer julgamento LLM; amostra estratificada inicial + early stopping sequencial nos pares cegos; limites de tokens/páginas e orçamento máximo de julgamentos no manifest; sealed só roda depois de todos os gates baratos passarem.

## 12. Fora do escopo (v1)

GEPA/DSPy; juízes por API paga adicional; auto-edição de gates pelo ciclo; otimização de F2A/conselho; cron automático; UI.

## 13. Regra de promoção do próprio subsistema

Critérios 1–8 da seção 9 + um ciclo piloto A0–A6 completo com material real + relatório publicado. Enquanto não houver mínimo de casos sealed elegíveis (acúmulo prospectivo), o subsistema opera em modo `estudo_descritivo` e NENHUMA variante pode ser promovida a produção (R9/R11).

## 14. Triagem da revisão adversarial Codex (parecer 2026-07-23, GPT-5.5 high)

| Rec. | Tema | Decisão |
|---|---|---|
| R1 [P1] | Falta executor pareado | **Acatada** — novo `forja_ar_runpair.py`; princípio 2 |
| R2 [P1] | Cegamento burlável | **Acatada** — bundles canonicalizados em dir isolado; mapping HMAC com chave fora do workspace; acesso do juiz ao workspace invalida a rodada. Redução declarada: isolamento de processo do juiz é protocolo verificado (manifest de execução + teste), não sandbox de kernel |
| R3 [P1] | Regra de swap invertida | **Acatada** — consolidação por `artifactSha256`; kappa com ressalva de N pequeno e repetição intra-juiz |
| R4 [P1] | I1–I3 premiam exclusão | **Acatada** — ledgers congelados pré-geração; cobertura e correção separadas |
| R5 [P1] | I4–I7 otimizáveis | **Acatada** — I4 alinhado ao gate vivo; I5 sentinela sem score fictício; I6 por classe conceitual; I7 por entailment contra issue ledger |
| R6 [P1] | I8–I10 gameáveis | **Acatada** — zero defeito crítico + recibo Ed25519; geradora não julga a própria variante; I10 condicionado à completude |
| R7 [P1] | Renormalização = fraude | **Acatada** — máscara pareada; novo null bloqueia |
| R8 [P1] | Split por hash falha no corpus real (34/13/2; elegibilidade literal = 3 casos) | **Acatada** — elegibilidade ampla validada contra estado real; linhagem agrupada; HMAC secreto; estratificação com mínimos |
| R9 [P1] | Sealed não selado | **Acatada** — registro fora do workspace; orçamento vitalício por versão; aposentadoria de caso consultado; sem sealed elegível → promoção impossível |
| R10 [P1] | Auto-aprovação | **Acatada** — três estados; log encadeado; recibo Ed25519 da trilha existente |
| R11 [P1] | Calibração estatisticamente desonesta | **Acatada** — primeira rodada = estudo piloto descritivo; cluster por linhagem; sem alegação de eficácia |
| R12 [P1] | Canários públicos viram gabarito | **Acatada** — mutação de falha única sobre a mesma base; kill por sensor; camada secreta rotativa |
| R13 [P1] | Tripwire aceita regressão | **Acatada** — não-inferioridade por dimensão + orçamento de candidatos + fronteira sequencial |
| R14 [P2] | Custo subestimado | **Acatada** — seção 11 |
| R15 [P2] | Suíte não testa os ataques decisivos | **Acatada** — critério 7; typo `CANOTES` corrigido no TDD |
