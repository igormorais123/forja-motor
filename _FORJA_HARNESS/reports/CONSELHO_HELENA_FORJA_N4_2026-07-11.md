# CONSELHO INDEPENDENTE DA FORJA N4 — PARECER HELENA

**Data de corte:** 2026-07-11  
**Escopo examinado:** planejamento N4, código, schemas, testes, estados reais, telemetria, relatórios e integração com `gestao_escritorio`.  
**Método:** leitura direta dos artefatos, execução isolada dos 51 testes N4 e tentativas de burla em memória, sem alterar código ou estado do sistema.

## 1. Veredito

**A FORJA N4 é um piloto estruturalmente útil e substancialmente melhor que uma fábrica de texto, mas ainda não possui evidência antifraude suficiente para promoção geral.** A decisão atual de manter `pilot_blocking`, declarar as três experiências como baselines retrospectivas e conservar `promotionEligible=false` está correta.

O principal risco não está no desenho jurídico. Está na camada de medição: alguns indicadores de “100%” medem a presença de declarações produzidas pelo próprio sistema, não a verdade independente dessas declarações. Em particular, a prova temporal, o mutation score, a consistência C1–C5 e parte da sincronização com a gestão ainda podem ser satisfeitos por artefatos internamente coerentes, porém fabricados.

**Recomendação direta:** preservar o piloto e seus artefatos; não ativar `default_on`; substituir a confiança em resultados armazenados por recomputação a partir do texto, das fontes e do registro temporal; somente depois executar ciclos prospectivos novos.

**Confiança no diagnóstico:** 0,95. A confiança é alta porque três fragilidades foram reproduzidas diretamente contra as funções atuais. Não é uma probabilidade de falha futura.

## 2. O que está correto

1. **Honestidade do estágio.** Os documentos finais reconhecem que Patrícia/Fábio, Libra Sul e Saúde são baselines retrospectivas, não ciclos prospectivos. O Roadmap mantém M6.4 pendente (`planejamento/12_ROADMAP_FORJA_N4_RACIOCINIO_PROVA_CIENCIA.md:681-686`), e o relatório de implementação repete que `default_on` não foi promovido (`reports/IMPLEMENTACAO_FORJA_N4_2026-07-11.md:140-151`).
2. **Separação entre estrutura e liberação jurídica.** A telemetria passou a distinguir `pipelineAprovado` de qualidade do artefato (`test_real_telemetria_licao41.py:267-289`). Isso evita chamar 21 ressalvas P1 de documento pronto.
3. **Bloqueio real de Cafelana.** O caso permanece reprovado, com fonte revogada e seis P0. O sistema não apagou a evidência inconveniente para obter um painel verde.
4. **Proveniência física melhorada.** Em modo bloqueante, fontes precisam de caminho e SHA-256 recalculável. Isso é necessário e já captura hash opaco e fonte revogada.
5. **Cobertura de regras relevantes.** Os 51 testes de `test_forja_n4.py` passaram em 0,266 s nesta auditoria. Há testes para terminologia, conduta não verificada, temporalidade, quantificação, estudos retratados, causalidade indevida, cadeia de entrega, invalidação e integração entre artefatos.
6. **Integração operacional existe.** A ponte recalcula `management_summary` ao sincronizar (`gestao_escritorio/scripts/sync_forja_gestao.py:307-316`), usa sidecar separado e possui reconciliação de todos os casos (`gestao_escritorio/scripts/sync_forja_gestao.py:467-475`). O painel expõe promoção, revisão humana, testes e mutações (`gestao_escritorio/templates/dashboard.html:481-484`).
7. **Arquitetura incremental.** O N2 continua vigente, a N3 permanece candidata e a N4 está explicitamente rotulada como candidata no manifest. Essa gradação evita quebrar o fluxo já funcional.

## 3. Achados ordenados por gravidade

### H-01 — CRÍTICA — A elegibilidade prospectiva pode ser fabricada sem mudar o hash da suíte

**Classificação:** falha real.

`suite_hash()` vincula apenas `suiteId` e a lista de testes; não inclui `executionMode`, `draftedBeforeFinalText`, `frozenAt`, `finalProducedAt` ou a justificativa retrospectiva (`forja_case_tests.py:18-22`). A validação prospectiva verifica apenas strings não vazias e sua ordem lexicográfica (`forja_case_tests.py:34-40`). Os schemas aceitam datas como strings genéricas (`n4_schemas/f4_case_acceptance_tests.schema.json:86-90`) e não definem contrato específico para esses campos.

**Burla reproduzida:** uma suíte real retrospectiva foi alterada apenas em memória para:

```text
executionMode=prospective
draftedBeforeFinalText=true
frozenAt="0"
finalProducedAt="9"
```

O `suiteHash` permaneceu idêntico e `validate_suite()` retornou zero achados. Logo, a regra escrita no planejamento é mais forte que a prova executada.

O risco aumenta porque `promotionEligible` exige apenas aprovação agregada, rótulo `prospective` e mutation score declarado maior ou igual a 0,8 (`forja_n4_validate.py:275-278`). Não exige recibo temporal independente nem recomputação das medições C1–C5.

**Impacto:** um ciclo retrospectivo pode aparentar ser prospectivo e tornar-se elegível à promoção.

### H-02 — CRÍTICA — O agregador aceita mutation score e draft hash declarados sem refazer os testes

**Classificação:** falha real.

`validate_results()` só confere o hash do texto quando recebe `draft_path` (`forja_case_tests.py:137-149`). Porém, o agregador N4 chama `validate_results(results, suite)` sem fornecer o texto canônico (`forja_n4_validate.py:264-268`). Nesse caminho, um `draftHash` falso não é detectado.

O mesmo validador considera o mutation testing suficiente quando `total >= 1` e `mutationScore >= 0.8`; ele não recalcula mutações nem confere `killed`, `survivors` e a lista de mutações (`forja_case_tests.py:146-149`).

**Burla reproduzida:** em uma cópia apenas em memória do resultado Patrícia/Fábio, o `draftHash` foi substituído por 64 zeros e `antiFraud` por `{mutationScore: 1.0, killed: 10, total: 10}`, sem lista de mutações. `validate_results(forged, suite)` retornou zero achados.

**Impacto:** os dois números usados na promoção podem ser fornecidos pelo próprio artefato que deveriam auditar.

### H-03 — ALTA — O mutation score de 100% mede literais, não resistência a erro jurídico

**Classificação:** falha real de métrica.

O operador atual remove a expressão esperada em testes `contains` ou acrescenta a expressão proibida em `not_contains` (`forja_case_tests.py:96-120`). A mutação é considerada morta se qualquer teste bloqueante falhar. Isso prova que um detector de presença reage quando sua própria palavra-chave é removida. Não prova que ele detecta inversão de tese, troca de parte, erro de valor, negação, precedente incompatível, ato recursal errado ou perda de contexto.

Os 30 testes reais das três baselines são quase integralmente buscas literais. Exemplos: datas, valores, “Súmula 182 do STJ”, “teoria da asserção” e ausência de `[VERIFICAR]`. Um texto pode conter todas essas expressões e defender exatamente a conclusão oposta.

O teste automatizado que “prova discriminação” reproduz a mesma circularidade: remove `pedido correto` e injeta `[VERIFICAR]`, esperando 2/2 (`test_forja_n4.py:145-154`).

**Impacto:** mutation score de 100% tem alta aparência de rigor e baixa validade externa. Deve ser renomeado, por ora, para **cobertura de mutação literal**.

### H-04 — ALTA — C1–C5 aceitam evidência textual sem vínculo verificável

**Classificação:** falha real.

Para `N4-MEASURED-v1`, `validate_global()` exige `measuredAt`, pelo menos um check, `passed=true` e um campo `evidence` não vazio (`forja_consistency.py:206-223`). Não exige caminho, hash, versão do verificador, entradas medidas, saída reproduzível ou correspondência com o estado atual. O schema tampouco torna `measurementContract` e `layerEvidence` campos estruturados obrigatórios; seu contrato comum permite propriedades adicionais (`n4_schemas/f7_global_consistency.schema.json:133-164`).

**Burla reproduzida:** cinco camadas `pass`, cada uma com `measuredAt="x"` e `evidence="ok"`, produziram zero achados.

O avaliador antifraude repete a mesma lógica (`forja_n4_anti_fraud_audit.py:72-80`). Assim, ele não é independente da fragilidade que deveria detectar.

**Impacto:** `measured_consistency=100` pode significar apenas que cinco textos livres foram preenchidos.

### H-05 — ALTA — A estatística antifraude não estima variância operacional

**Classificação:** falha metodológica real.

O relatório chama de “sigmas” o desvio-padrão calculado sobre quatro casos reais e cinco mutações artificiais extremas (`forja_n4_anti_fraud_audit.py:137-142`). Essa dispersão mede o desenho dos ataques escolhidos, não estabilidade, incerteza, repetibilidade ou variância do sistema em produção. A regra `sigma >= 10` premia justamente mutações binárias de 100 para 0; qualquer avaliador com ataques extremos parecerá “discriminante”.

Além disso:

- os cinco ataques derivam de um único caso-base, Saúde (`forja_n4_anti_fraud_audit.py:105-135`);
- não há conjunto adversarial oculto;
- não há rótulos independentes nem matriz de confusão;
- não há falso positivo, falso negativo, intervalo ou repetição;
- três casos positivos recebem 100 em todas as dimensões porque os indicadores são majoritariamente binários (`reports/N4_ANTI_FRAUD_AUDIT_RESULT.json:25-69`).

**Impacto:** `discriminatingWeight=1.0` e “nenhum indicador com variância zero” não sustentam a conclusão científica sugerida pelos nomes. As cinco fraudes selecionadas foram bloqueadas; somente isso está demonstrado.

### H-06 — ALTA — A aprovação estrutural não está suficientemente ligada à qualidade da peça real

**Classificação:** dívida crítica de produto, não erro de rotulagem no relatório.

A telemetria real mostra:

- 54 citações detectadas;
- 15 conferidas em fonte e 39 não conferidas (`telemetria/TELEMETRIA_LICAO41_2026-07-11_0100.json:289-290`), taxa observada de conferência de **27,8%**;
- três artefatos renderizados, nenhum sem ressalvas, 21 P1 (`telemetria/TELEMETRIA_LICAO41_2026-07-11_0100.json:347-350`);
- apesar disso, `pipelineAprovado=true` (`telemetria/TELEMETRIA_LICAO41_2026-07-11_0100.json:420-424`).

O relatório explica corretamente que isso não é liberação. O problema é operacional: `legalReleaseStatus` depende apenas da existência de `gaps` nas teses e da fase-alvo (`forja_n4_validate.py:306-342`). Não incorpora citações não verificadas, P1 visuais/editoriais, status da íntegra processual, identidade do ato impugnado ou aprovação jurídica humana.

**Impacto:** um caso F10 sem `gaps` textuais pode aparecer `structurally_clear` mesmo com citação não conferida ou ressalva visual. O painel reduz o risco com o selo “Revisão humana”, mas a regra de liberação continua incompleta.

### H-07 — MÉDIA — “Proveniência 100%” não mede sustentação da afirmação

**Classificação:** dívida de nomenclatura e de validação.

O avaliador de proveniência conta fontes ativas cujo caminho existe e cujo SHA-256 coincide (`forja_n4_anti_fraud_audit.py:39-58`). Isso prova identidade física da fonte, não que a fonte sustenta a proposição, que o trecho foi lido corretamente ou que a versão é juridicamente aplicável.

**Impacto:** a métrica pode induzir falsa equivalência entre “arquivo íntegro” e “afirmação comprovada”. O nome correto é **integridade física do registro de fontes**; sustentação deve ser medida no nível de afirmação/trecho.

### H-08 — MÉDIA — Gestão e validação podem estar obsoletas juntas e ainda concordar

**Classificação:** falha real de frescor.

O avaliador antifraude compara `approved` e `promotionEligible` do sidecar com o `N4_VALIDATION.json` armazenado (`forja_n4_anti_fraud_audit.py:82-86`). Se ambos estiverem obsoletos, a métrica dá 100. A sincronização normal recalcula o resumo, o que é um acerto, mas isso só ocorre quando `sync_case`/reconciliação é executado. Não há no avaliador uma comparação contra `validate_case(write=False)` nem um gate de frescor do `validationHash`.

O sidecar atual possui 21 itens e os quatro pilotos estão sincronizados; portanto, não constatei falha atual nesses quatro. A fragilidade é reproduzível pelo desenho e deve ser corrigida antes da promoção.

### H-09 — MÉDIA — Independência de revisão é inferida por nomes diferentes

**Classificação:** dívida de verificabilidade.

Nos testes de caso, autorrevisão é detectada apenas quando `producerRunId == reviewerRunId` (`forja_case_tests.py:84-87`). Dois nomes diferentes podem representar a mesma execução. O mesmo padrão aparece nos artefatos das baselines.

**Impacto:** o sistema comprova separação nominal, não independência de execução ou de julgamento.

### H-10 — BAIXA — O painel comprime estados diferentes na expressão “Baseline validada”

**Classificação:** melhoria opcional.

O painel mostra “Baseline validada” para qualquer `approved=true` com `promotionEligible=false`, sem usar `caseTestMode` (`gestao_escritorio/templates/dashboard.html:481-484`). Hoje o rótulo coincide com os três casos retrospectivos. No futuro, um ciclo prospectivo aprovado mas inelegível por outro motivo receberia o mesmo rótulo.

## 4. Testes que eu tentaria burlar

| Ataque | Resultado esperado correto |
|---|---|
| Trocar retrospectivo por prospectivo sem mudar os testes | hash temporal diverge e promoção bloqueia |
| Usar datas `0` e `9`, timezone inválido ou data impossível | schema e parser rejeitam |
| Declarar mutation score 1,0 sem lista de mutações | agregador recalcula e bloqueia |
| Alterar o texto após F7 mantendo o JSON de resultado | agregador detecta `draftHash` obsoleto |
| Manter a palavra-chave e inverter a tese por negação | mutante semântico é morto |
| Trocar parte, número, data, valor ou espécie recursal | pelo menos um teste específico falha |
| Inserir precedente correto em parágrafo que diz que ele não se aplica | teste de relação tese-fonte detecta conflito |
| Registrar fonte íntegra, mas irrelevante para a afirmação | claim-evidence gate reprova sustentação |
| Preencher C1–C5 com `evidence="ok"` | schema bloqueia por ausência de `evidenceRef`, hash e verificador |
| Manter sidecar e `N4_VALIDATION.json` igualmente antigos | comparação com validação fresca marca `stale` |
| Usar dois `runId` diferentes na mesma execução | recibo de execução/revisor acusa falta de independência |
| Obter 100% em ataques conhecidos e falhar em mutantes ocultos | conjunto holdout reprova promoção |

## 5. Mudanças recomendadas

### MUST — antes de qualquer promoção

1. **Vincular o tempo ao hash.** Incluir no hash da suíte `executionMode`, `draftedBeforeFinalText`, `frozenAt`, `finalProducedAt`, `retrospectiveReason`, versão e identidade do texto-alvo. Datas devem ser RFC 3339 reais, parseadas e normalizadas.
2. **Criar recibo de congelamento prospectivo.** Registrar antes da redação: hash da suíte, hash/identidade do corpus de entrada, evento sequencial e horário produzido pela própria FORJA. A promoção deve usar esse recibo, não campos editáveis no JSON final.
3. **Reexecutar F7 no agregador.** Resolver o texto canônico pelo manifesto, conferir seu hash e executar novamente suíte e mutações. `F7_CASE_TEST_RESULTS.json` passa a ser evidência histórica, não autoridade.
4. **Validar internamente `antiFraud`.** Exigir consistência entre `total`, `killed`, `survivors` e `mutations`; impedir score declarado sem mutações reproduzíveis.
5. **Expandir operadores de mutação.** Cobrir ao menos: negação; números/datas/valores; partes e polos; classe e identidade de atos recursais; número/tribunal/tese de precedentes; remoção de ressalva; troca de pedido principal/subsidiário. Medir resultado global e por família.
6. **Transformar C1–C5 em evidência reproduzível.** Cada check deve conter `checkerId`, `checkerVersion`, `inputHashes`, `outputHash` ou `evidenceRef`, horário válido e resultado recomputável. Texto livre fica como explicação, não prova.
7. **Separar quatro estados no painel e na API:** `pipeline_status`, `baseline_status`, `legal_release_status` e `promotion_status`. Nenhum deve ser derivado apenas do outro.
8. **Ampliar `legalReleaseStatus`.** Bloquear liberação quando houver citação material não conferida, fonte primária ausente, ato impugnado ambíguo, P0, P1 sem disposição, QA visual incompleto ou aprovações humanas obrigatórias ausentes.
9. **Comparar gestão com estado fresco.** O sidecar deve carregar o hash de uma validação recalculada. Se divergir de `validate_case(write=False).validationHash`, o painel mostra `stale`, não verde.

### SHOULD — melhora material depois dos MUST

1. Construir corpus adversarial versionado, com mutantes mantidos fora do código do avaliador e revisão de rótulos por Helena/Cícero.
2. Reportar matriz de confusão: fraudes críticas detectadas, casos válidos aceitos, falso bloqueio e fraude escapada. Não chamar dispersão de ataques de variância operacional.
3. Reservar casos holdout e variar tribunal, classe processual, tipo de peça e volume documental.
4. Medir taxa de citação material verificada por peça, cobertura de afirmações materiais, P1 por página e distância entre versão FORJA e versão humana aprovada.
5. Registrar identidade de execução independente além do nome: recibo, início/fim, família do modelo/revisor ou aprovação humana autenticada no fluxo.
6. Mostrar no painel `caseTestMode` de forma literal: retrospectivo, prospectivo ou legado.
7. Renomear as métricas atuais: `mutation_discrimination` para `literalMutationCoverage` e `provenance` para `sourceRegistryPhysicalIntegrity`, até os contratos mais fortes existirem.

### REJECT — não implementar

1. **Não ativar `default_on` para “obter dados”.** O piloto já permite aprender sem transformar ausência de evidência em bloqueio geral.
2. **Não aumentar o número de agentes ou modelos como substituto de verificação.** Mais pareceres autorreferentes não resolvem medição autorreferente.
3. **Não exigir infraestrutura cara, fine-tuning ou banco vetorial novo para corrigir estas falhas.** Os defeitos são de contrato, recomputação e desenho de experimento.
4. **Não criar travas genéricas de privacidade, classificação de sigilo ou burocracia sem relação causal com os erros observados.** Elas não melhoram precisão jurídica nem validade das métricas aqui auditadas.
5. **Não perseguir “100%” agregado.** Um único bloqueador crítico deve vencer a média; scores altos não compensam fraude temporal ou fonte não sustentadora.
6. **Não reescrever as três baselines apenas para fazê-las parecer prospectivas.** Elas são úteis exatamente porque agora estão corretamente classificadas.

## 6. Critérios objetivos de aceite para M6.4

Uma candidata à promoção somente deve avançar quando todos os itens abaixo forem comprovados:

1. **Três ou mais ciclos prospectivos novos**, de classes/tribunais distintos, com recibo de congelamento anterior ao primeiro texto final.
2. **Hash temporal íntegro:** qualquer alteração de modo, datas, testes ou texto muda o hash relevante e invalida resultados anteriores.
3. **Reexecução limpa:** o agregador reproduz, do zero, os resultados F7 a partir do texto canônico e das fontes registradas.
4. **Mutation testing material:** score global >= 80%, nenhuma família crítica sem mutação aplicável e nenhum mutante crítico sobrevivente.
5. **C1–C5 reproduzíveis:** 100% dos checks com entrada, versão, referência de evidência e saída conferível; nenhum `pass` baseado apenas em texto livre.
6. **Citações materiais:** 100% verificadas em fonte primária ou marcadas como bloqueio interno; zero citação material “não conferida” em peça candidata à liberação.
7. **Qualidade visual:** todas as páginas renderizadas e inspecionadas; zero P0; todo P1 resolvido ou aceito nominalmente com razão.
8. **Legal release independente:** Helena e Cícero registram análise material; revisão humana decide liberação; aprovação estrutural não a substitui.
9. **Gestão fresca:** `validationHash` do painel coincide com validação recalculada e o painel distingue claramente baseline, promoção e liberação.
10. **Corpus adversarial holdout:** 100% das fraudes críticas bloqueadas e nenhum caso válido bloqueado sem explicação reproduzível. Com amostra pequena, apresentar contagens; não inventar significância estatística.
11. **Regressão:** os 51 testes N4 atuais e a suíte global permanecem aprovados, sem reduzir gates existentes.
12. **Cafelana continua bloqueada** até a fonte primária faltante ser incorporada e toda derivação obsoleta ser regenerada.

## 7. Cenários

### Base

Os MUST são implementados sem mexer na produção legada; três ciclos novos são executados; a N4 permanece em piloto até apresentar evidência prospectiva. **Sinal:** resultados F7 podem ser apagados e reproduzidos identicamente pelo agregador.

### Otimista

Os novos operadores encontram erros antes da revisão humana e reduzem a distância entre minuta FORJA e versão aprovada. **Sinal:** queda sustentada de P1 e de citações não conferidas em ciclos distintos, sem aumento relevante de falso bloqueio.

### Pessimista

Mantêm-se os scores atuais como critério de promoção; um JSON coerente, mas fabricado, torna-se elegível. **Sinal:** ciclo prospectivo com 100% em todas as dimensões sem recibo temporal, reexecução ou evidência vinculada.

## 8. Próximo movimento

1. Corrigir o contrato temporal e o hash — responsável: Efesto; aceite: as quatro alterações temporais do H-01 invalidam a suíte.
2. Tornar o agregador reexecutável — responsável: Efesto; aceite: `draftHash` falso e `antiFraud` fabricado são bloqueados sem confiar no F7 salvo.
3. Definir operadores jurídicos de mutação — responsáveis: Cícero e Helena; aceite: ao menos seis famílias materiais com fixtures positivas e negativas.
4. Estruturar a evidência C1–C5 — responsável: Efesto; aceite: `evidence="ok"` deixa de ser suficiente e cada check é reproduzível.
5. Corrigir métricas e painel — responsáveis: Helena e integração de gestão; aceite: baseline, promoção, pipeline e liberação aparecem como estados independentes e frescos.
6. Executar M6.4 real — conselho completo; aceite: todos os 12 critérios da seção anterior satisfeitos sem regressão.

## 9. Síntese decisória

| Decisão | Parecer Helena |
|---|---|
| Preservar N4 em `pilot_blocking` | **APROVADO** |
| Usar as três baselines para regressão | **APROVADO, com o rótulo retrospectivo** |
| Considerar mutation score atual como prova jurídica | **REPROVADO** |
| Considerar C1–C5 atuais prova independente | **REPROVADO até vínculo de evidência** |
| Ativar `default_on` agora | **REPROVADO** |
| Implementar recomputação, recibo temporal e mutantes materiais | **OBRIGATÓRIO** |
| Acrescentar travas genéricas sem relação com precisão | **REJEITADO** |

**Assinatura analítica:** O sistema já aprendeu a não mentir sobre o passado. Agora precisa aprender a não aceitar como prova aquilo que ele próprio apenas declarou. Café preto, sem açúcar.
