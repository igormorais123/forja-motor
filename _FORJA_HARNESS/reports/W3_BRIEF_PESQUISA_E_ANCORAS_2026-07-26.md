# W3 — brief de assinatura, trilha de pesquisa e precedente-âncora

**Data:** 26/07/2026
**Protocolos:** `FORJA-LEGAL-SEARCH-TRACE-v1`, `FORJA-PRECEDENT-ANCHOR-v1`
**Emendas incorporadas:** E7 (vigência em quatro estados), E8 (`precedenteContrarioConhecido[]`), E13 (regime como convenção interna)

---

## A pergunta que cada contrato responde

São dois, e a distinção não é organizacional.

`FORJA-LEGAL-SEARCH-TRACE-v1` responde **como se procurou**. Sem ela, "não há precedente contrário" é opinião; com ela, é o resultado reproduzível de uma busca declarada — base, consulta literal, filtros, o que voltou, o que foi descartado e por quê, e o que deliberadamente não se procurou.

`FORJA-PRECEDENT-ANCHOR-v1` responde **o que o precedente decide**. Ementa é resumo redigido por terceiro: serve para localizar o acórdão, não para afirmar o que ele julgou. A ficha exige íntegra, localizador e hash do trecho.

## 1. Trilha de pesquisa — bloco aditivo, sem reformatar histórico

Os ledgers reais existem em três formas históricas (`entries`, `sources`, lista direta). `searchRuns` é top-level e aditivo; nenhuma entrada antiga foi tocada. **Ledger sem o bloco não é irregular — é anterior ao protocolo.**

Verificado contra os 11 ledgers reais em `state/`: zero achados novos. A extensão é compatível de fato, não por promessa.

Gates: consulta incompleta, ID repetido, resultado aproveitado e descartado ao mesmo tempo, descarte sem motivo, negativo sem consulta executada, replay declarado e inexistente, ação vedada.

Uma distinção que o validador guarda: **filtro ausente e filtro vazio não são o mesmo estado.** `{}` afirma busca sem filtro; a ausência do campo não afirma nada.

## 2. Ficha de âncora — E7, E8 e E13

**E7 — vigência em quatro estados.** `superado` invocado para `apply` derruba a rota; para `argue_overruling` é exatamente o cabimento. `modulado` sem marco temporal bloqueia: sem a data não se sabe se o caso está dentro ou fora do efeito. `afetado_por_tema_posterior` aplicado exige registrar por que ainda decide.

**E8 — o contrário conhecido é examinado, não silenciado.** Campo ausente e lista vazia são estados distintos: a lista vazia declara exame sem achado, a ausência não declara nada. Contrário citado sem operação declarada é registro, não resposta.

**E13 — o regime é convenção interna.** Efeito afirmado sem dispositivo que o crie é bloqueado; nota universal de autoridade (`authorityScore` e congêneres) também. Autoridade antiga ou monocrática **não** é rebaixada automaticamente — há teste que garante que continua passando.

Acrescido dos critérios de aceite: sanção administrativa não é precedente judicial. CGU, TCU, CARF, CADE, CVM e correlatos bloqueiam como âncora — a confusão é fácil justamente porque a linguagem se parece (há relator, voto, ementa e acórdão). A detecção usa fronteira de palavra: "CADE" é órgão, "academia" não é.

## 3. Reabertura de F4

Âncora reprovada não é defeito de fonte: é a rota estratégica que deixou de se sustentar. `failed_anchor_routes()` nomeia a rota atingida, o empacotamento a registra como bloqueio próprio, e os gatilhos `precedent_anchor` e `recipient_map` marcam o brief e o que dele derivou como `stale`.

## 4. Cross-reference do brief

Um artefato pode estar íntegro sozinho e apontar para IDs que não existem em lugar nenhum. O passe cruzado confere teses contra `F4_THESIS_MATURITY`, fatos decisivos contra a árvore de perguntas e o grafo, documentos contra o catálogo do mapa.

**Sem o artefato de origem, não se acusa referência pendurada** — ausência de pool não é prova de ID inexistente.

Âncoras são caso à parte: em F4 nenhuma está verificada, porque a verificação é trabalho de F7. O que se exige é a candidata declarada com identidade no próprio brief. É isso que permite confrontar depois a ficha de F7 com o que F4 prometeu — e é isso que impede a candidata de nascer final. `finalAnchorIds` em F4 é bloqueio.

## 5. Um defeito que a DA-04 previu

Rodar o gerador de schemas apagou o bloco `feedbackAssimilation` de `f10_human_diff_classification.schema.json` — extensão aplicada **à mão** no arquivo gerado em 22/07/2026.

É exatamente a falha que a DA-04 existe para impedir: arquivo gerado editado à mão perde a edição na primeira regeneração. Restaurado como `SCHEMA_OVERRIDES`, onde regenera sozinho.

Não fosse a conferência do diff, a perda seria silenciosa e só apareceria quando algum `F10` com `feedbackAssimilation` fosse rejeitado pelo schema.

## 6. Verificação

```
python forja_baseline.py → 37/37 suítes verdes · 437 testes pytest (+21 subtests) · APROVADO
fachada de liberação      → ledger sintético com âncora inválida bloqueou por 9 gates e nomeou a rota R7
11 ledgers reais          → zero achados novos (compatibilidade medida, não presumida)
```

Baseline: 389 → 437 testes.

**Instabilidade observada:** uma execução isolada de `test_forja_n3_management.py` falhou (16,5 s contra 1,2 s normais) e passou em três repetições seguidas e em duas execuções completas do baseline. Não há uso de tempo, sono ou subprocesso na suíte. Fica registrado como pendente de causa, não como resolvido.

## 7. O que continua condicionado

Os critérios de aceite de W3 que dependem de dado externo — âncora com íntegra real, trilha com consulta efetivamente executada — não têm caso real para exercitar enquanto as fontes do STJ estiverem fora do ar e a consulta da Onda −1 não for enviada. O contrato está pronto e testado contra fixtures; o primeiro caso real é o que vai dizer se o formato serve ao advogado.
