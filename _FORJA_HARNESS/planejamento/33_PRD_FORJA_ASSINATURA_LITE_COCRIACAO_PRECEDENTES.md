# 33 — PRD: FORJA-ASSINATURA Lite, cocrição e precedentes

> **EMENDAS NORMATIVAS — 25/07/2026.** Este documento vale **acrescido da seção 9 de `36_CONSOLIDACAO_CONSELHO_E_PARECER_FINAL.md`** (emendas E1 a E16: conselho Helena e Cícero, migração do modelo editorial Fable 5 para Opus 5 com revisão cruzada entre famílias, perímetro de sigilo, testes negativos, registro de escopo e Onda -1). Em conflito, prevalece a seção 9. Os `ANEXO_A/B/C` são histórico e não se executam.


**Versão:** 1.0  
**Protocolo:** `FORJA-ASSINATURA-LITE-v1`  
**Data:** 25/07/2026  
**Estado:** especificação consolidada para execução; não implementada  
**Arquitetura de origem:** `planejamento/32_PLANO_UNICO_CONSOLIDADO_V2_2026-07-25.md`  
**TDD canônico:** `planejamento/34_TDD_FORJA_ASSINATURA_LITE_COCRIACAO_PRECEDENTES.md`  
**Roadmap canônico:** `planejamento/35_ROADMAP_EXECUCAO_FORJA_ASSINATURA_LITE.md`

Este PRD substitui o documento 27 como especificação imediata. O PRD 27 permanece como visão experimental da arquitetura de múltiplos candidatos, cegamento N-way e recall, todos fora da v1 Lite.

---

## 1. Decisão de produto

Adicionar à FORJA uma camada anterior à redação que combine:

1. **cocrição dialética** com o advogado responsável;
2. **mapa verificável do destinatário**;
3. **brief estratégico único**, com rotas consideradas e decisão registrada;
4. **pesquisa topológica de precedentes**, profunda apenas nas âncoras;
5. **identidade editorial atribuível**, baseada em corpus curado;
6. **um único draft**, preservado por F7/F7-B.

O produto não cria uma segunda fábrica, não renumera F0–F10 e não torna estilo superior à juridicidade. A sua função é melhorar a decisão anterior à escrita e tornar essa decisão rastreável até o texto final.

## 2. Problema

A FORJA já possui controles fortes de exploração, fontes, proveniência, auditoria, edição final e entrega. Ainda assim, quatro lacunas reduzem a qualidade:

- a exploração F2-A é extensa, mas não se converte automaticamente em diálogo breve e material com o advogado;
- a rota pode ser escolhida sem conhecimento suficiente do órgão e das autoridades que decidirão;
- a pesquisa registra fontes utilizadas, mas não preserva de forma suficiente a genealogia da busca, rejeições e resultados negativos;
- a identidade do titular está dispersa em fala, peças, versões e feedbacks de autoria heterogênea.

O risco atual não é apenas texto genérico. É produzir uma peça correta que:

- responda à pergunta errada;
- adote uma estratégia que o responsável não escolheu;
- cite precedente verdadeiro, porém inadequado;
- trate ementa como ratio;
- pareça estilisticamente sofisticada, mas não represente o método de pensamento do escritório.

## 3. Resultado esperado

Para cada caso elegível, antes de F6:

- as dúvidas materiais dirigidas ao advogado foram respondidas ou bloqueadas;
- fatos, declarações do escritório, inferências e desconhecidos permanecem separados;
- o destinatário e a topologia decisória têm fonte e data;
- duas a quatro rotas reais foram consideradas, salvo justificativa para uma ou mais de quatro;
- uma rota foi selecionada por responsável identificável;
- as âncoras decisivas foram verificadas;
- a pesquisa negativa relevante foi registrada;
- o draft segue a rota e mantém vínculo com fatos, fontes e decisões humanas;
- F7/F7-B bloqueiam desvio estrutural, jurídico ou editorial.

## 4. Usuários e autoridades

### 4.1 Advogado responsável

Decide objetivo, limites, risco, narrativa material, rota e autorização de envio. Recebe consulta curta, com contexto e consequência da ausência de resposta.

### 4.2 Operador da FORJA

Produz e valida artefatos, distingue pendência de falha, executa pesquisa e consegue desligar a camada sem migrar casos.

### 4.3 Revisor jurídico

Confere fontes, ratio, regime, aderência, vigência e preservação da decisão estratégica.

### 4.4 Titular do padrão editorial

Fornece ou aprova amostras, corrige preferências e valida se o texto é aceitável para assinatura. Não precisa participar de toda petição.

### 4.5 Autoridade da IA

A IA pode investigar, perguntar, sugerir, comparar, explicar e redigir. Não pode:

- transformar declaração em prova externa;
- escolher sozinha risco material não autorizado;
- enviar comunicação externa sem autorização;
- atribuir autoria humana;
- dispensar revisão jurídica final.

---

## 5. Hipóteses separadas e falsificáveis

| Hipótese | Natureza | Prova |
|---|---|---|
| H1 — a consulta melhora o enquadramento | interação | perguntas materiais, não redundantes, que produzem decisões |
| H2 — o mapa reduz erro de destinatário | factual | conferência campo a campo e freshness |
| H3 — o brief melhora o draft | editorial | A/B cego contra incumbente, sem regressão jurídica |
| H4 — a ficha de âncora melhora o uso de precedentes | jurídica | quote check, ratio, aderência e vigência revisadas |
| H5 — o corpus reduz reescrita e aumenta aceitação | editorial | preferência cega, aceitação para assinatura e diff material |

Uma hipótese reprovada não invalida as demais. Correção factual não depende de vitória em A/B; ganho editorial não pode compensar erro jurídico.

---

## 6. Princípios invioláveis

1. **Verificação vence persuasão.**
2. **Silêncio não produz fato.**
3. **Resposta não é automaticamente aceite.**
4. **Declaração do escritório não substitui autos ou fonte oficial.**
5. **Ementa não basta para ratio decisiva.**
6. **Aderência e regime jurídico são dimensões distintas.**
7. **Identidade é método e aceitação editorial, não personificação.**
8. **O brief é decisão, não sumário para expansão mecânica.**
9. **Um draft por caso na v1.**
10. **F0–F10 e o cânone `draft_markdown → final_markdown` permanecem.**
11. **`off` preserva o comportamento anterior.**
12. **Nenhuma API paga nova ou ação paga do TeiaJus é habilitada sem autorização específica.**

---

## 7. Escopo funcional

### RF-01 — Modo efetivo e piloto

O produto deve suportar:

- `off`;
- `shadow`;
- `pilot_blocking`.

Em `pilot_blocking`, somente casos listados em `pilotCases` recebem gates bloqueantes; os demais operam em sombra. Não haverá `default_on` na primeira implementação.

### RF-02 — Seleção dialética

O sistema deve selecionar da árvore F2-A apenas perguntas que:

- não estejam respondidas no acervo;
- possam alterar decisão material;
- sejam dirigidas à autoridade humana adequada;
- declarem a consequência do silêncio.

Cinco a doze perguntas são alvo editorial, não limite técnico.

### RF-03 — Política de silêncio

Cada pergunta selecionada deve possuir política:

- `block_dependent`;
- `keep_options_open`;
- `explicit_reversible_default`;
- `not_applicable`.

Questões factuais materiais, autorizações e decisões estratégicas essenciais não admitem default factual.

### RF-04 — Consulta renderizada

O sistema deve produzir uma minuta legível de consulta contendo:

- síntese do entendimento;
- perguntas numeradas;
- razão concreta de cada pergunta;
- diligência já realizada;
- efeito da ausência de resposta;
- rotas ou decisões quando aplicável.

A minuta é uma view hash-bound do `F2_QUESTION_TREE.json`, não novo tipo de artefato obrigatório.

### RF-05 — Registro de respostas e decisões

Respostas de e-mail, WhatsApp, áudio ou reunião devem convergir para um ledger versionado contendo autoria, canal, natureza epistêmica, decisão produzida, artefatos afetados e pendências.

Resposta parcial não encerra a questão.

### RF-06 — Gate de envio

Na v1, a FORJA prepara a consulta. O envio depende de pessoa autorizada ou fluxo interno previamente autorizado, com allowlist e recibo. Nenhum conector de e-mail é requisito da capacidade técnica inicial.

### RF-07 — Mapa do destinatário

`F3_MAPA_DESTINATARIO.json` deve separar:

- competência;
- prevenção;
- composição atual;
- posição individual;
- posição colegiada;
- divergência;
- rota recursal.

Cada campo mutável deve registrar fonte, `checkedAt`, política de freshness e estado.

### RF-08 — Fonte adequada por campo

DataJud e TeiaJus podem orientar pesquisa, mas:

- DataJud não prova composição atual;
- prevenção exige autos, distribuição ou fundamento regimental;
- composição exige fonte oficial atual;
- ratio decisiva exige conteúdo suficiente da decisão.

### RF-09 — Signature brief

`F4_SIGNATURE_BRIEF.json` deve registrar:

- questão decisiva;
- consequência demonstrada;
- rotas plausíveis;
- rota selecionada;
- rotas rejeitadas e motivo;
- decisão humana associada;
- fatos e documentos decisivos;
- âncoras candidatas;
- melhor objeção e resposta;
- conteúdo obrigatório;
- pendências bloqueantes.

### RF-10 — Número de rotas

Duas a quatro rotas são o padrão quando houver pluralidade real. Uma rota é válida com justificativa; mais de quatro exige razão de complexidade. Alternativas artificiais devem falhar no gate de utilidade.

### RF-11 — Trilha jurídica de pesquisa

O `source_ledger` deve registrar query, base, filtros, horário, resultados, descartes, limitações, bases não consultadas, resultados negativos e referência de replay.

### RF-12 — Ficha de precedente-âncora

Somente precedentes declarados como âncoras recebem:

- íntegra e hash;
- trecho e localização;
- questão decidida;
- fundamentos determinantes;
- obiter confundível;
- moldura fática;
- confronto com o caso;
- operação jurídica;
- regime e vigência.

### RF-13 — Integração TeiaJus

O produto deve distinguir capacidades anunciadas daquelas efetivamente permitidas pelo bridge. Na v1, podem ser avaliadas para allowlist apenas ações de leitura sem custo novo:

- `research_sources`;
- `research_plan`;
- `research_search`;
- `research_mission_get`;
- ações STJ já autorizadas.

`research_mission`, CAPTCHA pago e qualquer ação `read_paid` permanecem fora.

### RF-14 — Fontes administrativas

Dados de CEIS, CEAF, CNEP, CEPIM e leniência devem ser classificados como evidência administrativa. Só decisões oficiais com conteúdo decisório suficiente podem ser classificadas como precedentes administrativos.

### RF-15 — Corpus de identidade

O ativo `autoresearch/IDENTITY_CORPUS_MANIFEST.jsonl` deve inventariar autoria, papel de Fábio, confiança, versão, canal, relação entre versões e uso permitido.

Diff sem atribuição intelectual não pode virar preferência Medina.

### RF-16 — Aplicação da identidade

O draft pode usar padrões validados de método, estrutura, densidade e ritmo. Não pode:

- imitar cacoetes orais;
- inserir vocabulário ornamental para “parecer Medina”;
- declarar autoria;
- aplicar o mesmo movimento argumentativo a todo caso.

### RF-17 — Um draft e preservação

F6 produz um único `draft_markdown`. F7/F7-B devem recompor:

- hash do brief;
- `selectedRouteId`;
- fatos e âncoras obrigatórios;
- pedidos e polaridade;
- integridade do recibo `gostoJuridico`.

### RF-18 — Invalidação

Mudança material deve invalidar descendentes:

- resposta humana material → mapa/brief/pesquisa/draft afetados;
- composição ou prevenção stale → mapa e brief dependente;
- âncora rejeitada → brief e draft;
- rota alterada → draft e validações posteriores;
- fonte removida ou hash divergente → citação, âncora e produto.

### RF-19 — Compatibilidade

Casos legados continuam válidos:

- novos artefatos são condicionais enquanto o modo não for bloqueante;
- campos novos possuem defaults explícitos;
- schemas gerados aceitam artefatos históricos;
- F8 e package continuam consumindo um único cânone.

### RF-20 — Observabilidade

Cada execução deve registrar modo configurado e efetivo, hashes, decisões humanas, queries, status de freshness, reason codes, custo, latência e resultado dos gates.

---

## 8. Requisitos não funcionais

### RNF-01 — Fail-closed proporcional

Em `pilot_blocking`, ausência ou inconsistência material bloqueia o produto dependente. Em `shadow`, gera achado visível sem alterar a saída canônica.

### RNF-02 — Determinismo

Schemas, hashes, seleção de perguntas, resolução de modo, cross-references, freshness e invalidação são determinísticos. LLM não autocertifica gates.

### RNF-03 — Escopo do corpus

> Este requisito era "Privacidade" e foi reescrito no expurgo de 04/08/2026: a
> parte de dados privados saiu por ordem do Igor. Ficou o que é decisão de
> produto — o corpus é do caso, não global.

Conteúdo de um caso não entra em corpus global. Relatório de pesquisa cita o
necessário para a conclusão, não o documento inteiro.

### RNF-04 — Reversibilidade

Rollback é alteração de modo para `off`. Histórico não é apagado.

### RNF-05 — Atualidade

Composição, prevenção, vigência e posições decisórias registram quando foram verificadas e quando precisam ser revistas.

### RNF-06 — Eficiência

Perguntas redundantes, fichamento indiscriminado e múltiplos drafts são proibidos. Pesquisa profunda limita-se às âncoras.

### RNF-07 — Sem custo novo implícito

Ações pagas, API nova, CAPTCHA pago ou coleta de alto volume exigem decisão separada.

---

## 9. Métricas

### 9.1 Segurança

- fatos materiais convertidos por silêncio: zero;
- citações sem identidade ou lastro: zero;
- ratio decisiva baseada apenas em ementa: zero;
- composição apresentada como atual sem fonte/freshness: zero;
- falsa atribuição humana no corpus: zero;
- regressões AH-01 a AH-08: zero em `strict_protocol`.

### 9.2 Interação

- perguntas selecionadas;
- perguntas já respondidas no acervo;
- perguntas que produziram decisão;
- rodadas necessárias;
- pendências mantidas abertas;
- tempo entre consulta e decisão.

Não há meta numérica inicial. A baseline do piloto define intervalos aceitáveis.

### 9.3 Pesquisa

- âncoras com íntegra;
- âncoras com trecho localizado;
- resultados negativos registrados;
- queries reproduzíveis;
- âncoras rejeitadas antes de F6;
- dados stale detectados.

### 9.4 Valor editorial

- preferência cega da variante;
- aceitação para assinatura;
- redução de reescrita material;
- preservação de fatos, autoridades e pedidos;
- carga de revisão humana.

### 9.5 Operação

- latência e custo por subfluxo;
- taxa de fallback para incumbente;
- falhas por reason code;
- taxa de rollback;
- casos em `shadow` e `pilot_blocking`.

---

## 10. Critérios de aceitação

1. `off` não altera outputs nem chama capacidades novas.
2. caso fora de `pilotCases` permanece em sombra.
3. pergunta factual já respondida não é enviada ao advogado.
4. pergunta material sem resposta mantém o dependente bloqueado.
5. `office_declaration` não satisfaz gate de prova factual.
6. default só é aceito em categoria permitida e com consequência registrada.
7. resposta parcial não fecha decisão.
8. consulta renderizada corresponde ao hash da árvore.
9. nenhum envio ocorre sem recibo de autorização.
10. mapa diferencia `confirmed`, `stale`, `unknown` e `not_applicable`.
11. DataJud não certifica composição ou prevenção.
12. brief referencia apenas IDs existentes.
13. rota selecionada aponta para decisão humana quando material.
14. alternativa artificial é rejeitada.
15. query e resultados negativos são reproduzíveis.
16. âncora sem íntegra suficiente não recebe ratio final.
17. alteração da âncora reabre F4.
18. ação TeiaJus fora da allowlist é recusada.
19. ação `read_paid` é recusada sem autorização específica.
20. registro CGU não é rotulado como precedente decisório.
21. corpus sem autoria resolvida não gera regra de identidade.
22. transcript é classificado como pensamento oral.
23. F6 produz um único draft.
24. F7/F7-B recompõem brief, rota e recibo.
25. package continua exigindo `verified_source_ledger`.
26. casos legados continuam legíveis.
27. rollback `off` foi exercitado.
28. mapas e hashes arquiteturais foram regenerados após mudanças estruturais.

---

## 11. Fora do escopo v1

- múltiplos drafts por petição;
- N-way, Condorcet e recall;
- memória decisória alimentando geração;
- fine-tuning ou clonagem de voz;
- UI nova;
- envio externo autônomo;
- protocolo judicial;
- score universal de gosto ou aderência;
- jurimetria comportamental;
- inferência psicológica de julgador;
- ações pagas do TeiaJus;
- conectores completos de todas as autoridades administrativas.

---

## 12. Riscos e controles

| Risco | Controle |
|---|---|
| perguntas demais | filtros de materialidade e deduplicação |
| silêncio convertido em certeza | política por pergunta e gate fail-closed |
| resposta estratégica tratada como prova | epistemic status e support IDs |
| mapa stale | fonte, checkedAt e freshness |
| personalização excessiva ao julgador | adaptação de legibilidade, não manipulação |
| ementa tratada como ratio | gate de conteúdo suficiente |
| cherry-picking | trilha de busca, descartes e resultados negativos |
| três rotas artificiais | faixa flexível e teste de utilidade |
| identidade caricatural | corpus atribuído e validação cega |
| schema editado fora da fonte canônica | geração por `generate_n4_contracts.py` |
| feature contamina N4 existente | namespace e modo próprios, sem renumerar fases |
| ação TeiaJus paga | allowlist e recusa de `read_paid` |

---

## 13. Gate de liberação

Estados máximos:

```text
contracts_ready
→ shadow_evidence_ready
→ pilot_blocking_ready
→ pilot_completed
```

`default_on` exige PRD futuro, evidência prospectiva e aprovação humana específica. Não é consequência automática deste projeto.

## 14. Critério de concluído

A capacidade técnica estará concluída quando todos os critérios de aceitação tiverem testes, o modo `off` tiver identidade comportamental, as ondas de sombra e piloto tiverem rollback exercitado, e nenhum gate jurídico tiver regredido.

O produto só estará validado quando as hipóteses H1–H5 tiverem evidência compatível com sua natureza. Código completo sem essa evidência será registrado apenas como `technical_capability_complete`.
