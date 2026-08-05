# CONSELHO INDEPENDENTE DA FORJA N4 - RELATORIO DIABOB

**Data da auditoria:** 11/07/2026  
**Auditor:** Diabob - red team de autoengano, validadores e metricas  
**Escopo examinado:** planejamento, implementacao N4, schemas, validadores, suites, telemetria, relatorios, canarios M6 e integracao com `gestao_escritorio`  
**Regra de trabalho:** auditoria somente leitura; nenhum codigo, schema, teste, estado ou painel foi alterado  

## 1. Verdict

**A FORJA N4 e uma candidata operacional util e substancialmente melhor que a versao anterior, mas a alegacao de “antifraude aprovada” e mais forte do que as provas atuais permitem.**

O sistema acertou ao corrigir a falsa classificacao dos tres canarios como prospectivos, ao manter `promotionEligible=false`, ao bloquear Cafelana e ao separar aprovacao estrutural de liberacao juridica. Esses acertos sao reais.

O ponto incomodo e este: o sistema ainda consegue certificar a propria narrativa. Parte relevante da evidencia e declarativa, a identidade dos revisores e apenas textual, a mutacao mede a remocao de literais escolhidos depois do texto, o avaliador antifraude nao executa o validador de ponta a ponta e o painel chama caso vazio de “N4 validada em sombra”.

**Veredito operacional:**

- `N4.0-candidate` pode continuar em `pilot_blocking` nos casos selecionados;
- as tres baselines retrospectivas servem para regressao, nao para promocao;
- `default_on` continua corretamente proibido;
- a auditoria `N4-ANTI-FRAUD-v1` deve ser reclassificada como **teste inicial do placar**, nao como prova antifraude do sistema;
- nenhum ciclo futuro deve se tornar `promotionEligible=true` antes da correcao dos bypasses P0/P1 deste relatorio.

## 2. O autoengano central

O sistema confunde quatro coisas diferentes:

1. **integridade de arquivo** - o hash atual corresponde ao conteudo atual;
2. **procedencia** - a fonte existe e foi localizada;
3. **independencia** - outra execucao realmente revisou o resultado;
4. **verdade material** - a fonte sustenta a afirmacao juridica e o documento final esta correto.

Hoje a FORJA faz razoavelmente bem o item 1, parcialmente o item 2 e ainda simula por campos textuais os itens 3 e 4. Um hash recalculavel detecta alteracao acidental; nao impede um produtor de regravar o JSON com uma conclusao conveniente. Um `reviewerRunId` diferente prova diferenca de texto; nao prova revisao independente. Uma evidencia `passed=true` com uma frase preenchida prova conformidade de formato; nao prova que a medicao ocorreu.

## 3. Achados por gravidade

### D-01 - CRITICA - A promocao pode aceitar resultados e mutation score fabricados

**Classificacao:** falha real, exploravel por artefato adulterado.

`validate_case()` chama `validate_results(results, suite)` sem fornecer o caminho do texto final. Assim, a verificacao de `draftHash` existente em `validate_results()` nao e executada.

**Evidencia:**

- `_FORJA_HARNESS/forja_n4_validate.py:264-278` carrega suite/resultados, valida sem `draft_path` e calcula promocao usando o `mutationScore` declarado;
- `_FORJA_HARNESS/forja_case_tests.py:137-149` somente confere `draftHash` se `draft_path` tiver sido informado;
- `_FORJA_HARNESS/forja_n4_validate.py:278` considera elegivel qualquer caso aprovado, marcado `prospective` e com numero declarado maior ou igual a `0.8`;
- `_FORJA_HARNESS/n4_schemas/F7_CASE_TEST_RESULTS.schema.json` nao define contrato para `antiFraud`, limites, contagens ou coerencia entre `killed`, `total` e `mutationScore`.

**Prova de contorno executada em memoria, sem gravar arquivos:** um resultado com `draftHash="inventado"`, `mutationScore=999`, `killed=999` e `total=1` retornou zero achados em `validate_results(fake, suite)`.

**Risco real:** um ciclo novo pode aparentar ser prospectivo e discriminante sem que a suite tenha sido reexecutada contra o texto final indicado.

**MUST:** na validacao agregada, localizar o artefato final canonico, recalcular seu hash, reexecutar a suite e comparar integralmente o resultado recalculado com `F7_CASE_TEST_RESULTS.json`. Resultado armazenado deve ser cache verificavel, nunca autoridade.

**Criterio de aceite:** adulterar apenas `draftHash`, `mutationScore`, `killed`, `total` ou qualquer `status=pass` deve produzir P0; `promotionEligible` deve permanecer `false`.

---

### D-02 - CRITICA - O QA visual M6 pode ser aprovado sem auditoria visual registrada

**Classificacao:** falha real.

O comando `approve()` nao analisa pagina, imagem, sobreposicao, corte, tabela, diagrama ou legibilidade. Ele troca `approved` para `true` e converte todas as paginas para `pass`.

**Evidencia:**

- `_FORJA_HARNESS/forja_n4_m6_prepare.py:119-129` recebe um nome de revisor, marca o ledger aprovado e muda todas as paginas para `pass` sem achados, observacoes ou hash de revisao;
- os tres `F8_QA_LEDGER_N4.json` possuem apenas `page`, `path` e `status` em cada pagina;
- `_FORJA_HARNESS/forja_consistency.py:61-68` aceita como independencia apenas `generatorRunId != reviewerRunId`;
- `_FORJA_HARNESS/forja_n4_m6_cycles.py:97-99` repete o mesmo criterio textual;
- `_FORJA_HARNESS/phase_contracts_n4/F8.json:22-24` exige todas as paginas revisadas, revisor independente, hash do PDF e fidelidade semantica, mas o ledger M6 nao prova o ato de revisao.

**Contraprova material:** `_FORJA_HARNESS/telemetria/TELEMETRIA_LICAO41_2026-07-11_0100.json` informa 3/3 artefatos renderizados com ressalvas, zero sem ressalvas e 21 P1. Apesar disso, os canarios foram resumidos como QA `6/6`, `7/7` e `12/12`.

**Risco real:** paginas com texto sobreposto, diagrama ilegivel ou conteudo cortado podem receber aprovacao em massa.

**MUST:** substituir a aprovacao em lote por ledger pagina a pagina produzido por `forja_visual_qa.py`, contendo hash da imagem, achados automaticos, decisao do revisor e justificativa para qualquer override. Proibir `approved=true` quando uma pagina nao possuir evidencia individual vinculada ao hash do PDF.

**Criterio de aceite:** introduzir sobreposicao ou corte em uma pagina deve reprovar o ledger; trocar apenas `reviewerRunId` nao pode alterar o resultado.

---

### D-03 - ALTA - A auditoria antifraude testa o proprio placar, nao o sistema de ponta a ponta

**Classificacao:** falha metodologica real.

`N4-ANTI-FRAUD-v1` le snapshots ja produzidos, altera campos em memoria e chama `evaluate()`. Ele nao grava fixtures isoladas, nao chama `validate_case()`, nao percorre schemas, nao reexecuta suites, nao sincroniza a gestao e nao verifica o que o painel exibiria.

**Evidencia:**

- `_FORJA_HARNESS/forja_n4_anti_fraud_audit.py:22-36` monta snapshots de JSONs prontos;
- linhas `111-135` alteram cinco campos de um unico caso-base;
- linhas `137-142` avaliam os snapshots diretamente;
- linhas `69-70` confiam no mutation score armazenado;
- linhas `72-80` confiam nos booleanos e textos de `layerEvidence`;
- linhas `82-86` comparam apenas dois campos do sidecar;
- linhas `154-156` gravam aprovacao sem que o processo termine com codigo de erro quando `approved=false`.

O resultado publicado - quatro casos reais, cinco fraudes, 100% de peso discriminante - descreve corretamente esse pequeno corpus. Nao demonstra resistencia geral.

**MUST:** criar corpus adversarial isolado que passe pelo mesmo entrypoint de producao e validacao. Cada ataque deve alterar arquivos reais de fixture, executar validator, sync e render do painel, e provar bloqueio observavel.

**Criterio de aceite:** no minimo 20 ataques independentes, cobrindo schemas, fonte, cronologia, mutacao, visual, entrega e gestao; zero ataque P0 aprovado; taxa de falso bloqueio medida em controles validos.

---

### D-04 - ALTA - Casos F0 vazios aparecem como completos e “N4 validada em sombra”

**Classificacao:** falha real de estado e comunicacao.

Quando o alvo e F0, nenhum artefato N4 entra na contagem. Logo, `expected_count=0`, `present=0`, `complete=true` e `approved=true`. O resumo transforma isso em “N4 validada em sombra”.

**Evidencia:**

- `_FORJA_HARNESS/forja_n4_validate.py:273-275` define completude por igualdade de contagem e aprovacao por completude sem P0;
- linhas `328-331` produzem “N4 validada em sombra” para o caso aprovado;
- `gestao_escritorio/scripts/sync_forja_gestao.py:307-310` publica esse resumo no sidecar;
- o sidecar atual exibe varios casos com `0/0`, sem artefatos e com a mensagem de validacao;
- a prova sem escrita sobre `case-email-auto-19f38f30238ff4d3` retornou `complete=true`, `approved=true`, `questionCoverage=0/0`, `caseTests=0/0` e `nextAction="N4 validada em sombra."`.

**Risco real:** o painel transforma “nao executado” em “validado”. Isso e exatamente a especie de falsa conclusao que a N4 promete impedir.

**MUST:** introduzir estado explicito `not_started`/`not_evaluated`. Zero esperado em fase sem contrato N4 nao e completude. O painel deve mostrar “N4 ainda nao executada”.

**Criterio de aceite:** todo caso sem artefato N4 deve ter `approved=false`, `complete=false` ou estado triestatal equivalente; nunca usar badge verde nem a palavra “validada”.

---

### D-05 - ALTA - Registro de fontes vazio neutraliza a verificacao de sourceHashes

**Classificacao:** falha real.

O validador somente compara `sourceHashes` com o registro quando ambos existem e o conjunto registrado e nao vazio.

**Evidencia:**

- `_FORJA_HARNESS/forja_n4_validate.py:237` aceita registro vazio sem achado;
- linhas `252-255` executam a comparacao apenas sob `if payload.get("sourceHashes") and registered_hashes`;
- prova em memoria: `_source_registry_findings(..., {"n4SourceRegistry": {}}, require_verifiable=True)` retornou zero achados.

**Risco real:** um caso bloqueante pode declarar hashes arbitrarios em todos os artefatos com registro vazio e evitar o gate de proveniencia.

**MUST:** em `pilot_blocking/default_on`, registro vazio e P0 quando qualquer artefato aplicavel possuir fonte; `sourceHashes` vazio tambem deve ser P0 para artefatos que fazem afirmacoes factuais.

**Criterio de aceite:** caso com artefato aplicavel e registro vazio falha; hash nao registrado falha mesmo quando o conjunto registrado esta vazio.

---

### D-06 - ALTA - “Consistencia medida” ainda pode ser autodeclarada

**Classificacao:** falha real no validador; geracao atual tem calculos reais, mas o contrato aceita falsificacao.

`validate_global()` exige data, lista de checks, `passed=true` e algum texto em `evidence`. Nao reproduz a medicao nem valida o tipo de evidencia.

**Evidencia:**

- `_FORJA_HARNESS/forja_consistency.py:206-228` faz apenas validacao estrutural;
- `_FORJA_HARNESS/forja_n4_anti_fraud_audit.py:72-80` repete a confianca nos campos;
- prova em memoria: cinco camadas com `measuredAt="qualquer"` e evidencia `"eu afirmo"` retornaram zero achados.

**Acerto parcial:** `_FORJA_HARNESS/forja_n4_m6_cycles.py:205-229` calcula hashes, fidelidade, testes e referencias de forma concreta. O defeito esta na verificacao posterior, que nao distingue o artefato legitimo de um JSON reescrito.

**MUST:** cada check deve ter `checkType`, entradas com caminhos/hashes, resultado estruturado e funcao verificadora reproduzivel. O agregador deve recalcular os checks criticos.

**Criterio de aceite:** trocar `passed=false` para `true` e recalcular `contentHash` continua reprovando porque a medicao reproduzida falha.

---

### D-07 - ALTA - Mutation score de 100% e quase tautologico

**Classificacao:** metrica enganosa; divida metodologica grave.

Para cada teste `contains`, a mutacao remove exatamente o literal que o proprio teste exige. Para `not_contains`, adiciona exatamente o literal proibido. Depois considera a mutacao morta se qualquer teste bloqueante falhar.

**Evidencia:**

- `_FORJA_HARNESS/forja_case_tests.py:96-123` implementa essas duas mutacoes;
- `_FORJA_HARNESS/forja_n4_m6_cycles.py:37,54,71` define dez ancoras literais por caso;
- linhas `184-186` transformam essas ancoras em testes depois que os textos ja existiam.

Assim, 10/10 prova apenas que os verificadores detectam a retirada do texto que foram construidos para encontrar. Nao prova que detectam inversao de tese, troca de parte, valor incorreto, contradicao, precedente falso, pedido incompatível ou perda de contexto.

**MUST:** separar `literalMutationScore` de `semanticMutationScore`. A promocao deve depender do segundo. Incluir operadores de negacao, troca de sujeito, troca de recurso/decisao, datas, valores, unidades, pedidos, relacao causal, citacao inexistente, precedente com tese diversa e contradicao entre secoes.

**Criterio de aceite:** cada familia de risco material deve possuir ao menos uma mutacao que sobreviveria a busca literal e seja morta por verificacao estrutural ou semantica independente.

---

### D-08 - ALTA - Telemetria real mostra 39/54 citacoes nao conferidas, mas as baselines terminam com zero P1

**Classificacao:** lacuna real entre qualidade juridica e aprovacao estrutural.

**Evidencia:**

- `_FORJA_HARNESS/telemetria/TELEMETRIA_LICAO41_2026-07-11_0100.json`, bateria B1: 54 citacoes detectadas, 15 conferidas em fonte e 39 nao conferidas;
- a mesma telemetria declara `pipelineAprovado=true`, embora diferencie corretamente pipeline de liberacao do artefato;
- `_FORJA_HARNESS/reports/M6_*_ANTIFRAUD_RESULT.json` declara zero P0/P1 nas tres baselines;
- os testes M6 sao predominantemente ancoras literais e nao verificacao oficial de todos os precedentes.

Isso nao prova que as 39 citacoes estejam erradas. Prova que a FORJA nao verificou o suficiente para chama-las de certas.

**MUST:** incorporar cobertura de citacoes ao gate juridico: `verified/total`, fonte oficial, correspondencia de tese e localizador. Em produto juridico protocolavel, citacao material nao verificada deve impedir `structurally_clear`.

**Criterio de aceite:** zero citacao material sem fonte oficial ou sem justificativa explicita de retirada; numeros de cobertura visiveis no sidecar sem transformar “nao encontrada” automaticamente em “falsa”.

---

### D-09 - ALTA - `legalReleaseStatus` mede apenas gaps de tese e fase-alvo

**Classificacao:** falha real de agregacao.

**Evidencia:**

- `_FORJA_HARNESS/forja_n4_validate.py:316-317` conta apenas teses cujo campo `gaps` e verdadeiro;
- linha `341` retorna `structurally_clear` quando nao ha esses gaps e o alvo e F10;
- nao entram diretamente no calculo: cobertura de citacoes, QA visual detalhado, P1 materiais, comprovacao da independencia, entrega aplicavel, consistencia reproduzida ou pendencia de fonte oficial.

**Risco real:** um caso F10 sem `gaps` nas teses pode parecer estruturalmente liberado apesar de outras ressalvas materiais.

**MUST:** derivar o status de uma matriz explicita de liberacao. No minimo: fatos/fontes, citacoes, prazos, testes, visual, placeholders, entrega e revisao humana.

**Criterio de aceite:** qualquer P0 ou P1 classificado como material produz `human_review_required` ou `blocked`; `structurally_clear` exige lista positiva de gates satisfeitos.

---

### D-10 - ALTA - Artefatos `draft` podem compor caso “approved”

**Classificacao:** falha real.

O envelope aceita `draft`, `pending_review`, `approved`, `blocked`, `stale` e `not_applicable`. A aprovacao agregada depende de completude e ausencia de P0, mas nao exige que artefatos aplicaveis estejam com `status=approved`.

**Evidencia:**

- `_FORJA_HARNESS/forja_n4_common.py:24-25` define os estados;
- linhas `158-177` validam o estado, mas nao tornam `draft` ou `pending_review` bloqueantes;
- `_FORJA_HARNESS/forja_n4_validate.py:269-278` ignora o estado na formula final, salvo se algum validador particular gerar achado.

**MUST:** para aprovacao de fase/caso, artefato `required` deve estar `approved`; `draft`, `pending_review`, `blocked` e `stale` impedem aprovacao.

**Criterio de aceite:** mudar um artefato obrigatorio de `approved` para `draft`, recalcular `contentHash` e validar deve gerar P0.

---

### D-11 - ALTA - `not_applicable` pode esvaziar gates obrigatorios

**Classificacao:** falha de contrato com exploracao plausivel.

Arquivos requeridos podem ser apresentados como `applicability=not_applicable` com uma justificativa textual. Os validadores funcionais sao pulados. Nos canarios, F9 e F10 sao materializados como nao aplicaveis e, ainda assim, o alvo F10 fica completo e aprovado.

**Evidencia:**

- `_FORJA_HARNESS/forja_n4_validate.py:256-259` pula o validador funcional para `not_applicable`;
- `_FORJA_HARNESS/forja_n4_common.py:166-172` exige somente justificativa;
- `_FORJA_HARNESS/forja_n4_m6_cycles.py:231-235` marca ciencia, selecao, entrega e diff humano como nao aplicaveis conforme o perfil.

Nos canarios internos isso pode ser correto. O contrato de promocao, contudo, nao distingue claramente “baseline interna” de “peca pronta para entrega”.

**MUST:** criar matriz de aplicabilidade por tipo de produto e objetivo do ciclo. Para ciclo prospectivo de entrega, F9/F10 nao podem ser neutralizados por texto livre.

**Criterio de aceite:** justificativa fora da matriz gera P0; baseline interna nunca recebe status de liberacao externa.

---

### D-12 - MEDIA - Datas prospectivas aceitam strings arbitrarias e comparacao lexicografica

**Classificacao:** falha real, facilmente exploravel.

**Evidencia:**

- `_FORJA_HARNESS/forja_case_tests.py:34-40` compara `str(frozenAt) >= str(finalProducedAt)`;
- schemas aceitam datas como `type=string`, sem `format=date-time`;
- prova em memoria: `frozenAt="a"` e `finalProducedAt="b"` retornaram zero achados.

Mesmo timestamps ISO corretos nao provam congelamento historico; apenas declaram datas.

**MUST:** parse temporal estrito com timezone e ledger append-only vinculando hash da suite antes da criacao do primeiro hash do texto final.

**Criterio de aceite:** string nao ISO falha; alterar suite apos o freeze invalida o ciclo; a ordem e comprovada por eventos encadeados, nao por campos editaveis.

---

### D-13 - MEDIA - Independencia de agentes e identidade puramente nominal

**Classificacao:** divida estrutural.

`producerRunId != reviewerRunId` nao impede a mesma execucao de escolher dois nomes. O mesmo vale para Helena e Cicero quando seus pareceres entram como arquivos-fontes sem comprovacao de trajetoria distinta.

**Evidencia:**

- `_FORJA_HARNESS/forja_n4_common.py:173-177` verifica apenas igualdade textual;
- `_FORJA_HARNESS/forja_n4_m6_prepare.py:123-128` aceita qualquer `--reviewer`;
- `_FORJA_HARNESS/forja_n4_m6_cycles.py:95-112` incorpora pareceres Helena/Cicero como fontes e usa IDs fixos de produtor/revisor.

**SHOULD:** registrar execucao, modelo/ferramenta, entradas, saidas, hash e relacao de derivacao. Independencia deve significar que o revisor nao recebeu a conclusao pronta como unica fonte e produziu critica propria.

**Criterio de aceite:** duas etiquetas diferentes na mesma trajetoria nao contam como duas revisoes.

---

### D-14 - MEDIA - C1 prova existencia de fontes, nao sustentacao das proposicoes

**Classificacao:** divida conceitual.

Nos canarios, o registro inclui produto final, texto extraido, PDF, ledger F8 e pareceres do conselho. C1 confirma que os arquivos existem e seus hashes batem. Isso nao prova que cada fato, precedente ou pedido esteja sustentado por fonte primaria.

**Evidencia:**

- `_FORJA_HARNESS/forja_n4_m6_cycles.py:101-130` constroi o registro com fontes internas e produtos derivados;
- linha `222` chama o resultado de `registered_sources_have_current_hashes`;
- `_FORJA_HARNESS/forja_n4_anti_fraud_audit.py:39-58` atribui 100 em proveniencia quando caminho e hash conferem.

**SHOULD:** renomear a metrica para `file_traceability` e criar outra, `claim_support_coverage`, baseada em afirmacao -> fonte primaria -> trecho/localizador -> alcance.

**Criterio de aceite:** arquivo final nao pode servir como unica fonte do proprio fato que afirma.

---

### D-15 - MEDIA - O teste antifraude nao mede falso positivo

**Classificacao:** divida metodologica.

O criterio final exige que os tres casos escolhidos sejam aprovados e os cinco ataques bloqueados. Nao existem controles validos com variacoes benignas para medir excesso de bloqueio. O desvio-padrao das notas nao substitui sensibilidade/especificidade.

**Evidencia:** `_FORJA_HARNESS/forja_n4_anti_fraud_audit.py:137-152`.

**SHOULD:** incluir controles benignos: mudanca de formatacao, sinonimo juridicamente equivalente, ordem de secoes, numero com grafia equivalente, fonte oficial espelhada e justificativa valida de nao aplicabilidade.

**Criterio de aceite:** publicar matriz de confusao: verdadeiro bloqueio, falso bloqueio, verdadeira aprovacao e falsa aprovacao.

## 4. Acertos confirmados

1. **Correcao temporal honesta.** O roadmap e o manifesto agora dizem que os tres canarios sao baselines retrospectivas e mantem `promotionEligible=false`. Evidencia: `planejamento/12_ROADMAP_FORJA_N4_RACIOCINIO_PROVA_CIENCIA.md:680-686` e `FORJA_SPEC_MANIFEST.json:35-61`.
2. **Cafelana nao foi maquiada.** O caso permanece bloqueado por fonte revogada e ausencia documental material; o avaliador lhe atribui nota 10 e bloqueio.
3. **Separacao entre pipeline e artefato.** A telemetria declara expressamente que `pipelineAprovado` nao equivale a liberacao juridica/editorial e exibe 21 P1.
4. **Integridade de conteudo.** `contentHash` e recalculado sobre o payload sem o proprio hash e detecta drift acidental (`forja_n4_common.py:63-68,111-120,178-179`).
5. **Fonte opaca foi combatida em modo bloqueante.** Registros que sao apenas hash passam a gerar `N4-SOURCE-OPAQUE`; a lacuna restante e o registro totalmente vazio.
6. **Originais preservados.** Os canarios trabalham em `n4_cycle_m6`, sem sobrescrever os produtos originais.
7. **Painel distingue promocao.** O dashboard mostra “Nao promove” e “Revisao humana” nos canarios atuais (`gestao_escritorio/templates/dashboard.html:483`).
8. **Ciencia tem limites explicitos.** O caso Saude separa apoio contextual de prova individual e registra fontes cientificas verificaveis.
9. **Telemetria real existe.** Ha render Word/PDF, 60 paginas, varredura de 15 DOCX e contagem explicita de ressalvas; isso e melhor que smoke test.
10. **`default_on` nao foi ativado.** Essa e a decisao correta diante das lacunas acima.

## 5. Testes que eu tentaria burlar

| Ataque | Alteracao | Resultado correto |
|---|---|---|
| A01 Resultado inventado | `mutationScore=999`, `killed>total` | P0 e promocao falsa |
| A02 Texto trocado | substituir produto final apos F7 | hash e suite reexecutada bloqueiam |
| A03 Freeze falso | datas editadas depois do texto | ledger temporal invalida ciclo |
| A04 Datas lixo | `frozenAt=a`, `finalProducedAt=b` | schema temporal reprova |
| A05 Dois nomes, mesma execucao | produtor/revisor com IDs diferentes | independencia reprova |
| A06 QA em massa | todas as paginas `pass` sem evidencia | F8 reprova |
| A07 Sobreposicao real | diagrama com texto sobreposto | PDF/page QA reprova |
| A08 Registro vazio | hashes nos artefatos, registry vazio | proveniencia reprova |
| A09 Fonte circular | peticao final sustenta a propria afirmacao | cobertura de claims reprova |
| A10 Fonte existente, tese errada | acordao real citado por proposicao diversa | entailment juridico reprova |
| A11 Precedente inventado | numero plausivel, fonte ausente | citacao material bloqueia |
| A12 Troca de recurso | “agravo interno” por “recurso especial” em uma secao | identidade de evento reprova |
| A13 Troca de sujeito | autor/reu ou agravante/agravado invertido | grafo/consistencia reprova |
| A14 Negacao | inserir “nao” em tese decisiva | mutacao semantica reprova |
| A15 Valor | R$ 50.000 por R$ 500.000 em pedidos apenas | quantificacao/pedidos reprova |
| A16 Unidade | 48 horas por 48 dias | prazo/pedido reprova |
| A17 Secao contraditoria | fato correto na sintese e errado nos pedidos | consistencia global reprova |
| A18 NA abusivo | marcar F9/F10 como nao aplicavel em entrega real | matriz de aplicabilidade reprova |
| A19 Draft aprovado | artefato obrigatorio com `status=draft` | agregador reprova |
| A20 Caso vazio | F0 sem artefatos | painel mostra nao iniciado |
| A21 Sidecar stale | validacao muda sem nova sincronizacao | painel acusa obsolescencia |
| A22 Mudanca benigna | sinonimo sem perda material | controle valido continua aprovado |
| A23 Fonte espelhada | mesmo documento oficial em novo caminho/hash | reconciliacao controlada, sem falso bloqueio |
| A24 Reordenacao visual | mesma tese em outra secao | testes semanticos aprovam se coerente |

## 6. Mudancas MUST

1. Reexecutar F7 e mutacoes contra o artefato final corrente durante `validate_case()`.
2. Vincular `draftHash` a caminho/artefato canonico e impedir score/contagens impossiveis.
3. Substituir aprovacao visual em lote por ledger pagina a pagina com evidencia e hashes.
4. Tratar caso N4 vazio como `not_started`, nunca aprovado.
5. Reprovar registro de fontes vazio quando houver artefato factual aplicavel.
6. Tornar checks C1-C5 reproduziveis, nao apenas declarativos.
7. Criar mutacoes semanticas e separar sua nota da mutacao literal.
8. Integrar cobertura de citacoes e fontes oficiais ao status de liberacao juridica.
9. Exigir `status=approved` para todos os artefatos obrigatorios de uma fase aprovada.
10. Aplicar matriz de nao aplicabilidade por produto/ciclo.
11. Validar timestamps reais e provar ordem por ledger encadeado.
12. Executar o corpus antifraude pelo entrypoint real, incluindo sync e painel.

## 7. Mudancas SHOULD

1. Publicar matriz de confusao e taxa de falso bloqueio.
2. Renomear proveniencia atual para `file_traceability`.
3. Criar cobertura afirmacao-fonte-localizador-alcance.
4. Registrar trajetorias de produtor e revisor para demonstrar independencia.
5. Exibir no painel: estado N4, aprovacao estrutural, liberacao juridica, cobertura de citacoes e QA visual separadamente.
6. Usar selecao aleatoria/estratificada de casos para o corpus, reduzindo ajuste aos tres canarios conhecidos.
7. Guardar fixtures adversariais versionadas e imutaveis por versao do avaliador.
8. Fazer o processo de auditoria retornar codigo diferente de zero quando `approved=false`.

## 8. Mudancas REJECT

Estas propostas nao melhoram o problema e devem ser rejeitadas:

1. **Adicionar mais disclaimers genericos.** Texto de cautela nao corrige validador burlavel.
2. **Criar bloqueios amplos por “dados sensiveis”.** Nao aumenta precisao juridica nem resistencia de metrica e pode inutilizar o fluxo local.
3. **Aumentar o numero de agentes sem independencia verificavel.** Cinco nomes repetindo a mesma fonte nao sao cinco auditorias.
4. **Elevar arbitrariamente o limiar de 80% para 90% ou 100%.** Uma metrica tautologica continua ruim em qualquer limiar.
5. **Confiar em assinatura textual do revisor.** Identificador diferente nao e evidencia de revisao.
6. **Adicionar mais campos JSON declarativos.** Sem recomputacao, apenas aumenta a superficie de teatro de conformidade.
7. **Promover `default_on` porque a suite unitaria passou.** O problema esta nos contornos e na integracao, nao no caminho feliz.
8. **Bloquear toda peca com P1 indistintamente.** P1 editorial e P1 material precisam classificacao; burocracia cega aumenta falso bloqueio.

## 9. Criterios objetivos de aceite para uma N4 promovivel

### 9.1 Integridade e procedencia

- 100% dos artefatos obrigatorios com `status=approved`;
- 100% das fontes materiais com caminho, hash atual, tipo de fonte e localizador;
- zero fonte circular como unico suporte de afirmacao material;
- alteracao de arquivo final invalida automaticamente F7, F8, F9 e F10.

### 9.2 Testes e antifraude

- suite congelada antes do primeiro artefato final, comprovada por ledger encadeado;
- F7 reexecutado no momento da validacao agregada;
- invariantes: `0 <= killed <= total`, `score=killed/total`, `0 <= score <= 1`;
- nota literal publicada separadamente da nota semantica;
- no minimo 20 ataques E2E e 10 controles benignos;
- zero falsa aprovacao P0;
- taxa de falso bloqueio material inferior a 5% no corpus reservado;
- corpus nao pode ser composto apenas por casos usados para desenvolver as regras.

### 9.3 Qualidade juridica

- 100% das citacoes materiais verificadas em fonte oficial ou retiradas;
- cada precedente ligado a proposicao, trecho/localizador, alcance e eventual distincao;
- zero identidade processual ambigua em processos com multiplos recursos/decisoes;
- prazos com evento inicial, fonte, regra, calendario e dupla verificacao;
- toda pendencia material impede `structurally_clear`.

### 9.4 Visual

- 100% das paginas renderizadas e ligadas ao hash do PDF final;
- cada pagina com resultado automatico e decisao humana/independente registrada;
- zero sobreposicao, corte, placeholder ou diagrama ilegivel;
- qualquer regeneracao invalida a aprovacao visual anterior.

### 9.5 Gestao

- caso vazio = `not_started`;
- sidecar recalculado a partir do estado atual, com indicador de staleness;
- painel nunca transforma sombra em aprovacao;
- badges distintos para: execucao, aprovacao estrutural, promocao, revisao humana e entrega;
- divergencia entre validator e sidecar bloqueia a mensagem de conclusao.

### 9.6 Promocao

- tres ciclos realmente prospectivos, novos e completos;
- todos passam o corpus E2E e controles benignos;
- nenhum usa `not_applicable` fora da matriz do produto;
- decisao de promocao baseada em evidencia reservada, nao nos tres canarios de desenvolvimento;
- `default_on` somente apos relatorio de promocao que liste versao, corpus, falhas, falso positivo, rollback e responsavel pela decisao.

## 10. Prioridade pratica

Ordem correta de execucao:

1. fechar D-01 e D-02, porque hoje resultado e QA podem ser certificados por declaracao;
2. fechar D-04 e D-05, porque o painel e a proveniencia produzem falsos positivos claros;
3. transformar o antifraude em E2E e incluir controles benignos;
4. integrar citacoes e status de liberacao juridica;
5. somente entao iniciar os tres ciclos prospectivos M6.4.

Fazer novos ciclos antes disso apenas produziria evidencia elegante sobre validadores ainda burlaveis.

## 11. Transparencia

### Fatos verificados

- `default_on` nao esta promovido;
- os tres canarios sao retrospectivos e `promotionEligible=false`;
- Cafelana esta bloqueada;
- o painel recebe o resumo N4 do validador atual;
- caso F0 vazio retorna aprovado/validado em sombra;
- datas arbitrarias, mutation score impossivel e checks autodeclarados passaram nas provas em memoria;
- a telemetria registra 39/54 citacoes nao conferidas e 21 P1 em tres renders.

### Inferencias tecnicas

- os bypasses permitem falsa aprovacao futura se alguem produzir ou adulterar artefatos de modo conveniente;
- a nota 100 das baselines superestima resistencia semantica;
- a independencia nominal pode ocultar revisao pela mesma trajetoria.

### O que este relatorio nao afirma

- nao afirma que as 39 citacoes nao conferidas sejam falsas;
- nao afirma que as tres pecas atuais estejam juridicamente erradas;
- nao afirma que houve fraude humana intencional;
- nao invalida o valor das baselines como regressao;
- nao recomenda travas genericas de privacidade ou seguranca de dados.

## 12. Teste de realidade final

Uma FORJA antifraude deve sobreviver a esta pergunta: **se eu editar os campos que dizem que o trabalho foi aprovado, o sistema refaz o trabalho critico ou apenas confere se preenchi o formulario corretamente?**

No estado atual, em varios gates centrais, a resposta ainda e: confere o formulario. A proxima versao precisa recalcular a verdade operacional.
