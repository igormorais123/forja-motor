# CONSELHO DA FORJA N4 - RELATORIO EFESTO

**Data de corte:** 11/07/2026  
**Escopo:** arquitetura, contratos, estados, reexecucao, rastreabilidade, observabilidade, testes e integracao com a gestao.  
**Metodo:** leitura dos artefatos atuais e reproducao local dos validadores; nenhuma peca original foi alterada.

## Veredito

A N4 possui uma boa arquitetura de evolucao incremental: artefatos versionados, modos `off/shadow/pilot_blocking/default_on`, sidecar de gestao, rollback por flags e separacao correta entre baseline retrospectiva e promocao. Ela pode continuar em `pilot_blocking`.

Ainda nao e promovivel. O agregador usa como autoridade resultados, hashes, mutation score e medicoes que foram gravados pelo proprio fluxo. Em engenharia, recibo sem reexecucao e apenas uma declaracao bem formatada. O risco principal nao e indisponibilidade; e falso verde.

## Acertos confirmados

1. `management_summary()` revalida o estado atual, em vez de apenas repetir o snapshot salvo (`forja_n4_validate.py:306-307`).
2. As tres execucoes M6 foram corrigidas para `retrospective_baseline`, com `promotionEligible=false`.
3. Fontes ativas possuem caminho e hash, e fontes revogadas bloqueiam Cafelana (`forja_n4_validate.py:134-172`).
4. A integracao com `gestao_escritorio` e idempotente, compara revisoes e nao substitui estado N3 canonico por replay legado (`gestao_escritorio/scripts/sync_forja_gestao.py:409-464` e `540-546`).
5. O corpus de regressao, os testes N4 e a telemetria de producao existem e sao separados do texto promocional.

## Falhas por severidade

### E-01 - CRITICA - Resultado F7 nao e reexecutado pelo agregador

`validate_case()` chama `validate_results(results, suite)` sem localizar o texto final (`forja_n4_validate.py:264-267`). A conferencia de `draftHash` so ocorre quando `draft_path` e informado (`forja_case_tests.py:137-142`). O mutation score declarado entra diretamente na promocao (`forja_n4_validate.py:276-278`).

**Consequencia:** alterar o JSON de resultado pode produzir um falso verde sem mudar a peca.

**MUST:** resolver o texto canonico pelo registro de fontes, reexecutar `run_suite()` e comparar os campos determinantes. O F7 salvo passa a ser cache, nao autoridade.

### E-02 - CRITICA - QA visual pode ser aprovado em massa

`approve()` muda todas as paginas para `pass` sem consumir achados ou evidencia por pagina (`forja_n4_m6_prepare.py:119-129`).

**MUST:** exigir ledger por pagina com hash da imagem, lint automatico, decisao do revisor e observacao; nenhuma aprovacao em lote.

### E-03 - ALTA - Estado vazio equivale a completo

Quando `expected_count=0`, a igualdade `present == expected` gera `complete=true` (`forja_n4_validate.py:273-275`) e a gestao pode dizer “N4 validada em sombra” (`328-331`).

**MUST:** estado triestatal explicito: `not_evaluated`, `evaluated_blocked`, `evaluated_approved`. Zero artefato nunca e validacao.

### E-04 - ALTA - Registro vazio neutraliza o gate de fontes

A comparacao de hashes so ocorre quando ha hashes no artefato e no registro (`forja_n4_validate.py:252-255`).

**MUST:** em modo bloqueante, artefato aplicavel com afirmacao material exige ao menos uma fonte registrada e verificavel; hash nao registrado falha mesmo se o conjunto registrado estiver vazio.

### E-05 - ALTA - Contrato temporal nao integra o hash da suite

`suite_hash()` usa apenas `suiteId` e testes (`forja_case_tests.py:18-22`). Trocar `executionMode` ou datas nao invalida o resultado.

**MUST:** incluir modo e recibos temporais no hash e fazer parse ISO estrito com timezone.

### E-06 - ALTA - Estado dos artefatos nao participa da aprovacao

`effective_approved` depende de contagem e P0 (`forja_n4_validate.py:273-275`), sem exigir `status=approved` para artefato requerido.

**MUST:** `draft`, `pending_review`, `blocked` e `stale` impedem aprovacao. `not_applicable` depende de matriz por tipo de ciclo, nao texto livre.

### E-07 - ALTA - Consistencia C1-C5 e estrutural, nao reproduzida

O validador confere presença de texto de evidencia, mas nao recalcula a medicao (`forja_consistency.py:212-228`).

**MUST:** cada check critico deve apontar entradas, hashes e funcao verificadora; a promocao depende da recomputacao.

### E-08 - MEDIA - A telemetria mede pipeline e artefato em planos diferentes

O resultado real registra 21 P1 visuais e 39/54 citacoes nao conferidas, enquanto baselines estruturais terminam aprovadas. A separacao e legitima, mas o painel ainda permite leitura otimista.

**SHOULD:** publicar `pipelineStatus`, `artifactReleaseStatus`, `citationCoverage` e `visualFindings` como campos independentes.

### E-09 - MEDIA - Auditoria antifraude atual e pequena e nao ponta a ponta

O avaliador usa snapshots e cinco adulteracoes; nao percorre o mesmo entrypoint, sincronizacao e painel.

**SHOULD:** corpus isolado de adulteracoes e controles benignos, com taxa de falso bloqueio e codigo de saida nao zero quando falhar.

## Recomendacoes rejeitadas

- **REJECT:** reescrever a FORJA ou trocar toda a arquitetura. Os contratos existentes sao aproveitaveis.
- **REJECT:** promover por quantidade de agentes, nomes diferentes ou score medio.
- **REJECT:** acrescentar camadas genericas de privacidade que nao melhorem exatidao, recuperacao ou auditabilidade.
- **REJECT:** usar sucesso dos testes unitarios como substituto da inspecao dos artefatos reais.

## Criterios objetivos de aceite

1. Adulterar `draftHash`, `results`, `killed`, `total` ou `mutationScore` reprova pela reexecucao.
2. Alterar modo ou data temporal invalida o hash da suite.
3. Caso sem artefatos retorna `not_evaluated`, nunca aprovado.
4. Registro de fontes vazio reprova ciclo bloqueante aplicavel.
5. Artefato requerido em `draft` reprova.
6. QA visual exige evidencia individual para 100% das paginas.
7. Sidecar reproduz os mesmos estados recalculados pelo agregador.
8. Controles validos nao sao bloqueados por mudanca apenas editorial.
9. Testes unitarios, regressao real, sincronizacao e HTTP do painel passam depois das correcoes.
10. `default_on` permanece proibido ate tres ciclos prospectivos reais, distintos e sem P0 material.

## Decisao Efesto

Implementar E-01 a E-06 imediatamente. Iniciar E-07 com contrato reproduzivel, sem fingir que texto livre e medicao. Tratar E-08 e E-09 na telemetria e no corpus. Preservar a arquitetura e os originais.
