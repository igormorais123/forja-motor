# 36 — Consolidação do conselho e parecer final de execução

**Consolidador:** Efesto Tekhton. **Data:** 2026-07-25.
**Objeto:** pareceres de Helena e Cícero sobre `FORJA-COCRIACAO-v1`, mais a diretriz do Igor de 25/07/2026 sobre modelo editorial e revisão cruzada.
**Pareceres na íntegra:** `pareceres/HELENA_FORJA_COCRIACAO_2026-07-25.md` e `pareceres/CICERO_FORJA_COCRIACAO_2026-07-25.md`.
**Estado:** consolidado. **Nenhuma linha de código foi alterada nesta execução.**

---

## Resultado

**O plano é aprovado para execução, com quatro mudanças e uma inversão de prioridade.**

1. **Um achado é mais urgente que o plano inteiro** e não pertence a ele: a citação `art. 343-A do RISTJ` está entrando no corpo de peças e não encontra correspondência no regimento arquivado. Vira P0 de produção, com ação hoje.
2. Entra uma **Onda −1**, sem código, para testar barato a premissa comportamental mais cara do plano.
3. Entra a **migração do modelo editorial**: Fable 5 sai, Opus 5 entra, e revisão cruzada entre famílias de modelo passa a ser gate.
4. Entram **quatro refinamentos jurídicos**. ~~E o perímetro de sigilo~~ — revogado em 04/08/2026 por ordem do Igor; ver E6 e R6–R9 abaixo.

Superfície final: **1 tipo novo de artefato, 2 conchas do catálogo ativadas, 4 extensões aditivas, 2 subfases, 5 ondas.** Uma extensão a mais do que o PRD original, pelo motivo registrado no §3.

---

## 1. Evidência colhida nesta execução

Não repito afirmação de terceiro sem medir. O que verifiquei diretamente:

| Verificação | Resultado observado |
|---|---|
| `REGIMENTO_INTERNO_STJ.md` arquivado | `Art. 343` trata de precatórios de requisição de pagamento. **Zero ocorrências de `343-A`** no arquivo. |
| Ocorrências de `343-A` no acervo | todas em produção nossa; a string aparece como cabeçalho de peça — `### 3.1 Síntese Executiva (art. 343-A RISTJ)` |
| Superfície do Fable 5 | `forja_fable5.py` 27 ocorrências em 459 linhas; `forja_editorial_fidelity.py` 17 em 325; `FORJA_SPEC_MANIFEST.json` 19; protocolo 20; testes 19; `forja_run.py` 7; `phase_contracts/F7.json` 2 gates |
| Onde o modelo está fixado | `forja_fable5.py:31-32` — `MODEL_ALIAS = "fable"`, `MODEL_CANONICAL = "claude-fable-5"`; assertiva dura em `:343`. `forja_editorial_fidelity.py:170` — comparação literal com `"claude-fable-5"` |
| Catálogo N4 | 24 tipos declarados, envelope sem payload, **nenhum produzido em caso real** |
| Classes de contribuição | `CONTENT_CLASSES`, `CONTRIBUTION_ORIGINS`, `CONTRIBUTION_STATUS`, `CONFIDENCE` existem em `forja_learning.py` |

**[Não verificado]** Se emenda regimental posterior à consolidação arquivada criou dispositivo `343-A`. A conferência é na fonte oficial do STJ e não foi executada aqui.

---

## 2. Decisão sobre cada recomendação do conselho

### 2.1 Helena — estratégia

| Rec. | Conteúdo | Decisão | Fundamento |
|---|---|---|---|
| H1 | Onda −1: consulta manual sobre caso real da fila | **acatada** | testa a premissa mais cara do plano ao custo de uma hora, sem código |
| H2 | Gravar demonstração de recusa com a FORJA atual | **acatada com ajuste** | o ajuste é meu: **artefato real de caso real**, não encenação. Demo montada para a demo é teatro e viola a regra de evidência. Usar bloqueio já ocorrido no histórico |
| H3 | Separar J-B(acordo) de J-B(julgador) | **acatada, com a formulação do Cícero** | ver §2.2; a separação se sustenta, mas por veículo processual e não por perfil de risco |
| H4 | Três métricas de negócio | **acatada** | fecha a lacuna G19 do doc `29`, que o PRD identificou e não resolveu. Custo próximo de zero: derivam de artefato existente |
| H5 | Reordenar 1B antes de 1A | **acatada** | 1B não depende de comportamento humano e fecha falha já apontada no CASO-04; 1A fica condicionada ao resultado de H1 |
| H6 | Fechar Portão 0 em paralelo | **acatada** | Régua verde ou desvio classificado permanece bloqueante, conforme revisão adversarial de 24/07 |
| H7 | Nomear risco de concentração de cliente | **registrada, sem ação nesta versão** | é decisão de negócio do Igor, não de engenharia. Fica no registro para não ser descoberta tarde |

### 2.2 Cícero — jurídico

| Rec. | Conteúdo | Decisão |
|---|---|---|
| R1–R4 | Conferir `343-A` na fonte oficial; suspender a referência numérica; varredura retroativa; corrigir o `CLAUDE.md` | **acatadas integralmente**, elevadas a P0 acima do plano — ver §3 |
| R5 | Gate P0 de citação regimental não conferida no `forja_verificador.py` | **acatada** — entra na Onda 0. É bom em qualquer cenário, inclusive se `343-A` existir |
| R6–R9 | Perímetro por documento; corpus retém padrão e não conteúdo; segredo de justiça fora; consulta sob sigilo | ~~acatadas~~ → **REVOGADAS em 04/08/2026 por ordem do Igor.** Sobrevive só "corpus retém padrão, não conteúdo", que é decisão de produto (ver RNF-03 do doc 33). O resto era o G18, também rejeitado |
| R10–R11 | J-B(acordo) autorizado; **vedada** formulação que enderece consequência funcional pessoal ao gestor | **acatadas** |
| R12 | J-B(julgador) redefinido como insumo interno, com **vedação de saída** | **acatada** — e é melhoria material: deixa de ser "autorização caso a caso" e vira gate lexical verificável, que é infinitamente mais confiável |
| R13 | Base comparativa de origem legítima e registrada | **acatada** — já coberta pelo protocolo de 11/07, apenas explicitada |
| A1 | Nomear a inversão do art. 489 como ônus argumentativo da parte, não dever legal próprio | **acatada** — evita erro categorial vazar para a peça |
| A2 | "Vinculante" também é convenção operacional; afirmar o efeito pelo dispositivo, não pelo rótulo | **acatada** |
| A3 | `vigencia` com quatro estados: vigente, modulado, superado, afetado por tema posterior | **acatada** — fundir os três perdia a informação que decide o uso |
| A4 | Campo `precedenteContrarioConhecido[]` | **acatada** — sem ele a auditoria não distingue "não existe contrário" de "não procuramos" |

**Nada rejeitado.** Registro isso com desconfiança: conselho que concorda com tudo costuma não ter lido. Reli os dois pareceres procurando conflito material e encontrei um só — a separação do J-B —, resolvido em favor do Cícero por fundamento mais forte.

---

## 3. P0 de produção: a citação regimental — **RESOLVIDO EM 2026-07-25**

> ### Desfecho: o dispositivo existe. Bloqueio levantado.
>
> **Art. 343-A do RISTJ, introduzido pela Emenda Regimental nº 53, de 30/06/2026, publicada no DJe de 01/07/2026, vigente desde então.** Verbatim e proveniência em `cache/fontes_oficiais/RISTJ_ART_343A_ER53_2026.md`.
>
> A determinação do escritório de 07/07/2026 veio seis dias após a vigência e estava correta. **Não há defeito em produção, não há varredura retroativa, R1 a R4 caem.**
>
> Causa material do falso alarme: o `REGIMENTO_INTERNO_STJ.md` das pastas de caso está consolidado até a ER 47/2024, com as ER 48 a 53 apenas listadas na seção final, sem texto incorporado ao corpo. A busca local não tinha como encontrar.
>
> **Três itens reais sobreviveram, e valem mais do que o alarme:**
>
> | # | Item | Ação |
> |---|---|---|
> | **P0-a** | O art. 343-A alcança **apenas iniciais de ações originárias e petições de recurso dirigidas ao STJ**. Citá-lo em peça ao TJTO, TRF1 ou TRF4 é invocar norma que não rege aquele tribunal | a prática da síntese executiva permanece em toda peça; a **citação numérica só no STJ** |
> | **P0-b** | Regimentos arquivados desatualizados: emendas listadas ao final, não incorporadas ao corpo | atualizar `REGIMENTO_INTERNO_*.md`; entra na Onda 0 como R14 |
> | **P0-c** | O dispositivo remete a ato regulamentar da Presidência **ainda não editado** | não afirmar em peça que o resumo observa formato regulamentado; afirmar apenas o atendimento ao caput |
>
> **R5 permanece e sai reforçada:** o gate de citação regimental não conferida teria resolvido isto em segundos, nos dois sentidos. Custo do episódio: uma busca. Valor: a fonte agora está no cache, o âmbito está delimitado e a causa raiz — regimento desatualizado — foi encontrada.

### Registro do alarme original, preservado para auditoria

**Isto não é item de plano. É defeito ativo.**

Enquanto três documentos de arquitetura eram escritos hoje, peças seguem sendo produzidas com a etiqueta `art. 343-A do RISTJ` no corpo. A prática que a etiqueta nomeia — síntese executiva na abertura — é irretocável e foi determinada pelo próprio titular. **O problema é exclusivamente a citação numérica.**

**Ação imediata, hoje, antes de qualquer onda:**

1. Conferir o dispositivo na fonte oficial do STJ, na versão vigente com as emendas de 2026.
2. Até a conferência, **remover a referência numérica do corpo de toda peça**. Escrever "Síntese executiva", sem citação regimental. A prática permanece integralmente.
3. Se confirmada a inexistência: varredura retroativa desde 07/07/2026, classificação do alcance e decisão do titular sobre correção. A decisão é dele.
4. Corrigir o `CLAUDE.md` da fábrica para descrever a prática sem a etiqueta.
5. Gate P0 permanente no `forja_verificador.py`: todo `art. X do RI<Tribunal>` no texto final exige entrada no ledger de fontes com trecho literal.

O item 5 é bom independentemente do resultado do item 1, e por isso entra na Onda 0 de qualquer forma.

**Custo total do item 1: dez minutos.** É a melhor relação entre esforço e consequência de tudo o que foi produzido hoje.

---

## 4. Diretriz do Igor: modelo editorial e revisão cruzada

### 4.1 O que muda

Ordem de 25/07/2026, que supera a determinação de 15/07/2026 sobre o Fable 5:

- **Opus 5 substitui o Fable 5** na subfase F7-B — melhor, mais barato e mais rápido, conforme avaliação do Igor;
- **revisão cruzada entre famílias de modelo passa a ser obrigatória**: o processo pode ser iniciado no Claude ou no Codex, e obrigatoriamente **a outra família revisa**;
- o comitê adversarial é integrado a esse arranjo, em vez de rodar em paralelo.

### 4.2 Por que isto não é obra nova

A FORJA **já tem** o vocabulário e metade da máquina:

- `producer_reviewer_separation` já é gate de F7;
- o ciclo AR já classifica independência em `cross_family`, `cross_session_same_family` e `unverified` — decisão R2 da revisão adversarial de 24/07;
- `forja_editorial_fidelity.validate_editorial_bundle()` já recompõe hashes e não confia em declaração do modelo;
- o mecanismo de prova pelo envelope — o orquestrador confirma qual modelo executou, em vez de acreditar no que ele diz — já existe e é a parte valiosa.

A diretriz, portanto, **promove `cross_family` de critério de avaliação do AR para gate de produção**. É mudança de configuração e de contrato, não de arquitetura.

### 4.3 Desenho da migração

**Princípio: parametrizar, não reescrever.** O que tem valor em `forja_fable5.py` não é o nome do modelo — é a recusa em aceitar a autodeclaração dele. Isso fica.

| Passo | Mudança | Superfície |
|---|---|---|
| M1 | `MODEL_CANONICAL` deixa de ser constante e passa a vir de allowlist configurável de modelos editoriais autorizados | `forja_fable5.py:31-32` |
| M2 | A assertiva dura de `:343` passa a comparar com o modelo **declarado no contrato do run**, não com uma constante literal | `forja_fable5.py:343` |
| M3 | Idem em `forja_editorial_fidelity.py:170`, hoje comparação literal com `"claude-fable-5"` | `forja_editorial_fidelity.py` |
| M4 | Contrato de execução ganha `producerModel` e `reviewerModel`, cada um com `family`, `canonicalId` e `sessionId` | contrato F7 |
| M5 | Novo campo `familyAssurance`, com o enum já aprovado do AR: `cross_family`, `cross_session_same_family`, `unverified` | contrato F7 |
| M6 | Gate `fable5_oauth_confirmed` → `editor_model_confirmed`; **novo gate** `cross_model_review_verified` | `phase_contracts/F7.json` |
| M7 | Artefato `FABLE5_RESULT.json` → `EDITORIAL_RESULT.json`; campo `fable5_usage` → `editor_usage`. Leitores aceitam os nomes antigos; escritores emitem os novos | contratos e `forja_run.py` |
| M8 | `PROTOCOLO_FABLE5_ESCRITA_FINAL.md` → `PROTOCOLO_EDITORIAL_ESCRITA_FINAL.md`, com registro da supersessão e da data | documentação |
| M9 | Renomear `forja_fable5.py` → `forja_editorial.py` **apenas depois** de M1 a M7 verdes, com shim de compatibilidade | módulo |

### 4.4 Onde a revisão cruzada se aplica — e onde não

Aplicar em todas as onze fases multiplicaria custo sem ganho proporcional. Aplico onde o erro é caro e difícil de reverter:

| Ponto | Regra |
|---|---|
| **F7 — auditoria jurídica e factual** | **quem produziu o texto não pode ser da mesma família que o audita** |
| **F7-B — escrita final** | o editor é de família distinta da que auditou, ou o mesmo editor é auditado pela outra família |
| **F8 — QA visual** | mantém o revisor independente que já exige; a família distinta é preferencial, não obrigatória |
| Demais fases | livre; a separação produtor/revisor existente basta |

**Modo estrito.** Em `strict_protocol`, `familyAssurance` precisa ser `cross_family`. Fora dele, `cross_session_same_family` é permitido **com registro explícito da degradação** — nunca silenciosamente. `unverified` não libera entrega em nenhum modo.

**Degradação real.** Se a segunda família estiver indisponível, o caso **não para**: rebaixa para `cross_session_same_family`, registra o motivo e fica bloqueado apenas para liberação estrita. É o mesmo padrão que a revisão adversarial já aprovou para o AR e evita criar dependência dura de fornecedor externo.

### 4.5 A ordem importa — e é onde vejo o único risco sério da diretriz

**Não editar o `CLAUDE.md` antes do código.**

O `CLAUDE.md` da fábrica determina hoje o Fable 5 em F7-B. Se o protocolo passar a exigir Opus 5 enquanto `forja_fable5.py:343` ainda levanta erro quando o envelope não comprova `claude-fable-5`, **toda demanda em F7 para de fechar**. Não é hipótese: é assertiva dura, medida nesta execução.

Sequência obrigatória: **M1 a M7 verdes com testes → atualizar `CLAUDE.md` e o protocolo → M8 e M9.** Inverter isso derruba a produção.

Registro também que a determinação de 15/07 está marcada como "ordem do Igor, inviolável". A de 25/07 a supera. A supersessão precisa ficar **escrita e datada** no protocolo, e não apenas aplicada — senão a próxima sessão vai encontrar duas ordens invioláveis em conflito e travar.

---

## 5. Superfície e ondas finais

### 5.1 Placar consolidado

| | PRD `33` | **Consolidado** | Origem da mudança |
|---|---:|---:|---|
| Tipos novos de artefato | 1 | **1** | — |
| Conchas do catálogo ativadas | 2 | **2** | — |
| Extensões aditivas | 3 | **4** | R6: perímetro por documento |
| Subfases novas | 2 | **2** | — |
| Módulos novos | 4 arquivos | **4 arquivos** | — |
| Migração de módulo existente | 0 | **1** | M1–M9, modelo editorial |
| Ondas | 4 | **5** | H1: Onda −1 |
| Drafts por petição | 1 | **1** | — |

### 5.2 Ondas

**P0 — hoje, fora do plano.** Conferência do `art. 343-A`; suspensão da referência numérica. Não é onda: é correção de defeito ativo.

**Onda −1 — sem código, teto 2026-08-08.** Consulta manual sobre caso real; demonstração de recusa a partir de bloqueio já ocorrido; três métricas de negócio; parecer do Cícero sobre J-B(acordo) dirigido a gestor — este último já está entregue no parecer de hoje, R10 e R11, e o item se reduz a registrar a decisão.

**Onda 0 — contratos, sem mudança de saída.** O escopo original mais: gate de citação regimental (R5); perímetro por documento (R6–R8); quatro estados de vigência (A3); `precedenteContrarioConhecido[]` (A4); e **M1 a M7 da migração do modelo editorial**, que é pré-requisito de tudo o que toca F7.
*Portão:* Régua verde ou desvio classificado; nenhuma capacidade afirmada por semelhança de nome; **`cross_model_review_verified` passando em caso de teste**.

**Onda 1B — destinatário e precedentes em sombra.** Antes de 1A, conforme H5.

**Onda 1A — cocriação em sombra.** Condicionada ao resultado da Onda −1. Se a consulta manual não obtiver resposta útil, reduzir o escopo de F2-B ao Bloco 1 e ao Bloco 5, conforme o cenário pessimista de Helena.

**Onda 2 — identidade e variante de redação.** Corpus só depois do perímetro (R6).

**Onda 3 — piloto controlado.** Inalterada.

---

## 6. Risco e pendência

| Risco | Estado | Mitigação |
|---|---|---|
| `art. 343-A` inexistente em peças protocoladas | **ativo, não mitigado** | P0 do §3; ação hoje |
| Protocolo alterado antes do código quebra F7 | **previsível e evitável** | ordem obrigatória do §4.5 |
| Segunda família indisponível trava produção | mitigado por desenho | degradação registrada para `cross_session_same_family` |
| Corpus de identidade antes do perímetro | mitigado | R6 vira pré-requisito da Onda 2 |
| Consulta sem resposta vira latência pura | mitigado | Onda −1 testa antes de construir; efeito do silêncio por classe |
| Concentração de cliente | **registrado, sem ação** | decisão de negócio do Igor, não de engenharia |
| Escolha melhor sem peça melhor | irredutível | ondas 2 e 3; se não confirmar, sombra ou desligamento |

**Pendência de verificação declarada:** não confirmei a existência do `art. 343-A` na fonte oficial. Não afirmo que seja fictício. Afirmo o que medi: não está no regimento arquivado, e o `art. 343` trata de outra matéria.

---

## 7. Parecer final

**Execução autorizada, na ordem abaixo. O plano não muda de mérito; muda de sequência.**

O conjunto `33`–`35` é o melhor documento de planejamento que esta fábrica produziu: encolheu a cada revisão, corrigiu erros próprios em público e chegou a uma superfície que cabe num mês. Não tenho reparo de engenharia a fazer nele.

Tenho um reparo de foco, e é o mesmo que Helena e Cícero apontaram por caminhos diferentes: **hoje foram escritos seis documentos e nenhuma linha de produção melhorou.** Cícero encontrou uma citação regimental provavelmente inexistente saindo em peças. Helena observou que ninguém escreveu ao homem cuja entrevista originou tudo isso. Os dois estão dizendo a mesma coisa em idiomas distintos: o plano amadureceu mais rápido que a prática.

Por isso o P0 vem antes da Onda −1, e a Onda −1 antes da Onda 0. Arquitetura boa com defeito ativo em produção é arquitetura que ninguém vai confiar depois.

---

## 7-A. Reconciliação de cânone — colisão detectada e resolvida

Durante esta consolidação, detectei que **dois conjuntos 33/34/35 foram escritos no mesmo intervalo**, por linhas de trabalho paralelas, com minutos de diferença. Registro por evidência, não por relato:

| Documento | Escrito às | Origem |
|---|---|---|
| `33_PRD_COCRIACAO_DESTINATARIO_PRECEDENTES.md` | 15:43 | linha Claude |
| `34_TDD_COCRIACAO_DESTINATARIO_PRECEDENTES.md` | 15:46 | linha Claude |
| `35_ROADMAP_E_GATES_COCRIACAO.md` | 15:47 | linha Claude |
| `33_PRD_FORJA_ASSINATURA_LITE_COCRIACAO_PRECEDENTES.md` | 15:54 | linha Codex |
| `34_TDD_FORJA_ASSINATURA_LITE_COCRIACAO_PRECEDENTES.md` | 15:59 | linha Codex |
| `35_ROADMAP_EXECUCAO_FORJA_ASSINATURA_LITE.md` | 15:59 | linha Codex |

**Diagnóstico: complementares, não contraditórios.** Comparei estrutura e escopo. O conjunto Codex é mais profundo em **mecânica de execução** — decisões arquiteturais DA-01 a DA-05, namespace de feature, propriedade de arquivos por onda, critérios de aceite, comandos, rollback e commit sugerido. O conjunto Claude é mais profundo em **decisão e verificação**.

**Decisão: o conjunto Codex é o cânone de execução.** É o mais recente, é o referenciado pelos documentos `26` e `32`, e traz a mecânica que uma implementação precisa. Os documentos da linha Claude foram renomeados para anexos, e a colisão de numeração está encerrada:

- `ANEXO_A_DECISOES_E_ACHADOS_COCRIACAO.md`
- `ANEXO_B_INVARIANTES_E_TESTES_COCRIACAO.md`
- `ANEXO_C_GOVERNANCA_E_INSTRUMENTOS_COCRIACAO.md`

**Quatro itens dos anexos precisam ser absorvidos pelo cânone antes da Onda 0.** Não são preferência de redação; são conteúdo ausente do outro lado:

| # | Item | Onde está | Por que importa |
|---|---|---|---|
| **F1** | **As 24 conchas do catálogo N4**: o signature brief é payload de `F4_DECISION_FACTOR_MAP.json` e a cobertura de famílias é payload de `F4_COVERAGE_MATRIX.json` — em vez de tipos novos | Anexo A, §2.2 | é o achado que **reduz superfície**. O catálogo já declara 24 tipos com envelope e sem payload, e nenhum é produzido em caso real. Criar tipo novo por cima disso repete o erro com nome novo. A decisão DA-02 do TDD Codex, sobre namespace de feature próprio, precisa ser conferida contra este achado |
| **F2** | Registro de decisão sobre o documento `32`, item a item, com o que foi acatado, ajustado e rejeitado | Anexo A, §1 | rastreabilidade de por que cada correção entrou; sem isso, a próxima revisão reabre o que já foi decidido |
| **F3** | Treze testes negativos, cada um amarrado a uma proibição do PRD | Anexo B, §7.3 | proibição sem teste negativo é comentário. É o que transforma "não pode" em gate |
| **F4** | Registro de escopo que barra a onda quando a superfície cresce sem justificativa escrita | Anexo C, §2 | trava de governança contra recrescimento silencioso, que é o modo de falha histórico deste projeto |

**Não executei a fusão nesta execução, e explico por quê.** Fundir exige ler os três documentos Codex por inteiro — 59 KB somados — e editar sobre trabalho de outra linha. Fazer isso no fim de uma execução longa é como se produz perda de conteúdo. Parar a colisão é barato e reversível; fundir é caro e destrutivo se malfeito. Separei as duas coisas de propósito.

**A fusão é a tarefa 0 da Onda 0**, antes de qualquer schema.

---

## 7-B. Ressalva sobre a linha de base declarada

O pacote de execução reporta `104 passed, 3 subtests passed`. O documento `26`, §3.3, registrou em 24/07/2026 `131 passed, 3 subtests passed` sobre uma seleção nomeada de cinco suítes, **e registrou que a Régua estava reprovada** por alterações em arquivos de EDGE, Fable e estilo ainda não rebaselinadas.

Duas observações de engenharia, sem juízo sobre o pacote:

1. **104 e 131 não são comparáveis sem saber a seleção.** Números de suítes diferentes não medem a mesma coisa. Antes de tratar 104 como linha de base, W0 precisa registrar **quais suítes** compõem o número.
2. **"Testes passando" não é "Régua verde".** São controles distintos. A condição bloqueante da revisão adversarial de 24/07 é sobre a Régua, não sobre a contagem de testes. W0 existe justamente para fechar isso, e é a leitura correta de começar por ela — desde que o portão exija o estado da Régua explicitamente, e não a contagem.

Nenhuma das duas invalida o pacote. Ambas são o que W0 tem de resolver antes do primeiro commit de código.

---

## 9. EMENDAS AO CÂNONE — versão final única para execução

**Esta seção é normativa.** O cânone de execução é o trio `33`/`34`/`35` do Codex, **acrescido das emendas abaixo**. Um único plano será executado. Os `ANEXO_A/B/C` passam a ser histórico e não se executam.

### 9.1 F1 — concedido ao Codex, com o diagnóstico preservado

Levantei que o catálogo N4 tem 24 tipos declarados sem payload e sem produção em caso real, e propus que o brief fosse payload de `F4_DECISION_FACTOR_MAP` em vez de tipo novo. **Reli o TDD `34`, §6.1 e §7.1, e a proposta do Codex é melhor. Retiro a minha.**

Três razões, e a primeira é decisiva:

1. **Honestidade semântica.** "Decision factor map" e "signature brief" não são o mesmo objeto. Ocupar um nome declarado para guardar outra coisa cria um nome que mente. Quem ler o catálogo em seis meses vai esperar fatores de decisão e encontrar rotas.
2. **Não há economia real.** DA-04 estabelece que os schemas são **gerados** por `generate_n4_contracts.py` a partir de `forja_n4_common.ARTIFACT_SPECS`. Acrescentar uma entrada custa o mesmo que preencher uma concha. O ganho que eu supunha não existe.
3. **Squat não é higiene.** As 24 conchas são dívida de catálogo. Ocupar duas delas esconde a dívida em vez de pagá-la.

**O que sobrevive, e é o valor real do achado:**

> **E1 — Higiene do catálogo N4.** Registrar como item próprio: o `ARTIFACT_CATALOG.json` declara 24 tipos com envelope, sem payload e sem produção em nenhum caso real. Cada um deve receber **payload, produtor, consumidor e teste**, ou ser **removido do catálogo**. Não bloqueia nenhuma onda; entra no backlog de manutenção com dono. Enquanto não decidido, vale a regra: **nenhuma concha é ativada sem consumidor**.

### 9.2 Emendas que entram no cânone

| ID | Emenda | Destino | Origem |
|---|---|---|---|
| **E2** | Registro de decisão item a item sobre o documento `32` | `33`, seção nova ao final | Anexo A, §1 |
| **E3** | **Treze testes negativos**, cada um amarrado a uma proibição do PRD: silêncio em fato material; pergunta respondível pelo acervo; prevenção por DataJud; composição vencida; ratio de ementa sem íntegra; precedente sem operação; vinculante com moldura diversa; regime como número; rota com pendência material; família ausente na cobertura; envio autônomo; concha sem consumidor; campo do brief virado subtítulo | `34`, matriz de testes | Anexo B, §7.3 |
| **E4** | **Registro de escopo** que barra a onda quando a superfície cresce sem justificativa escrita | `35`, portão de cada onda | Anexo C, §2 |
| **E5** | **Cobertura de famílias de tese** — nove famílias, cada uma `examinada_proposta`, `examinada_descartada` com motivo ou `nao_aplicavel` com motivo. Proibido mínimo numérico de teses | `33` e `34`, junto ao brief | Anexo A, RF-1 |
| ~~**E6**~~ | ~~Perímetro por documento: classificação de sigilo, segredo de justiça, dados sensíveis~~ — **REVOGADA em 04/08/2026 (Igor).** Permanece apenas: corpus retém padrão, não conteúdo | `33` RNF-03 | Cícero R6–R9, revogada |
| **E7** | **`vigencia` com quatro estados**: `vigente`, `modulado`, `superado`, `afetado_por_tema_posterior`, com marco temporal da modulação | `34`, ficha de âncora | Cícero A3 |
| **E8** | **`precedenteContrarioConhecido[]`** com a operação que se pretende opor | `34`, ficha de âncora | Cícero A4 |
| **E9** | **Gate P0 de citação regimental não conferida**: todo `art. X do RI<Tribunal>` no texto final exige entrada no ledger com trecho literal e data de conferência | `34`, `forja_verificador.py` | Cícero R5 |
| **E10** | **Âmbito da citação regimental**: `art. 343-A do RISTJ` só é citável em peça dirigida ao STJ. A prática da síntese executiva permanece em toda peça | `34`, gate lexical | P0-a, §3 |
| **E11** | **Atualizar os `REGIMENTO_INTERNO_*.md`** das pastas de caso, incorporando emendas ao corpo em vez de listá-las ao final | `35`, Onda 0 | P0-b, Cícero R14 |
| **E12** | **J-B(julgador) com vedação de saída**, verificável por gate lexical: nenhum achado sobre comportamento de julgador compõe texto externo. **J-B(acordo) autorizado**, vedada formulação que enderece consequência funcional pessoal ao gestor | `33`, escopo | Cícero R10–R12 |
| **E13** | **`regime` e `tipoAutoridade` são convenção interna da FORJA em todas as categorias**, inclusive "vinculante". A peça afirma o efeito pelo dispositivo, nunca pelo rótulo. A inversão do art. 489, §1º, é **ônus argumentativo da parte**, não dever legal próprio | `34`, ficha de âncora | Cícero A1–A2 |
| **E14** | **Migração do modelo editorial** M1 a M9: Opus 5 substitui Fable 5; `familyAssurance` com `cross_family`, `cross_session_same_family` e `unverified`; gate `cross_model_review_verified` em F7 e F7-B; **`CLAUDE.md` só depois de M1–M7 verdes** | `34` e `35`, Onda 0 | diretriz de 25/07 |
| **E15** | **Onda −1 sem código**: consulta manual sobre caso real; demonstração de recusa a partir de bloqueio já ocorrido; três métricas de negócio; **1B antes de 1A** | `35`, antes de W0 | Helena H1–H6 |
| **E16** | **Portão de baseline pela Régua, não pela contagem de testes.** Registrar quais suítes compõem o número declarado | `35`, W0 | §7-B |

### 9.3 O que fica de fora, confirmado

Múltiplos drafts por petição; N-way e Condorcet; recall; memória decisória em produção; pacote e CLI próprios; escore numérico de aderência; conectores de jurisprudência administrativa na v1; envio externo autônomo; ações pagas de pesquisa; `default_on` antes do piloto; ativação de concha sem consumidor.

### 9.4 Ordem final de execução

```
Onda −1  (sem código)   E15
W0                      E9 · E11 · E14(M1–M7) · E16 · freeze · Régua
W1                      E2 · E5 · E7 · E8 · E13 · schemas gerados por DA-04
W2A / W2B               1B antes de 1A (E15)
W3+                     E6 antes do corpus · E4 em todo portão
backlog com dono        E1 · E3 incorporado às suítes · E10 · E12
```

---

## 8. Próxima ação

0. **Fundir F1 a F4 dos anexos no cânone `33`–`35`** — tarefa 0 da Onda 0, antes de qualquer schema. Especialmente F1: conferir a decisão DA-02 do TDD contra o achado das 24 conchas.
1. **Conferir `art. 343-A` do RISTJ na fonte oficial** — hoje. Suspender a referência numérica no corpo das peças até a resposta.
2. **Enviar a consulta manual** sobre um caso real da fila, com o gabarito do `35`, §3, e zero pergunta reprovada no filtro do acervo — até 2026-07-31.
3. **Localizar no histórico um bloqueio real de citação sem íntegra** e registrá-lo como demonstração — até 2026-08-01.
4. **Aplicar M1 a M7** da migração do modelo editorial, com testes verdes, **antes** de tocar o `CLAUDE.md` — Onda 0.
5. **Incorporar ao `33`, `34` e `35`** as decisões deste documento: R5, R6–R9, A1–A4, R10–R12, migração M1–M9, Onda −1 e reordenação 1B antes de 1A.

Não executei nenhuma dessas ações. Este documento é consolidação e decisão, não implementação.
