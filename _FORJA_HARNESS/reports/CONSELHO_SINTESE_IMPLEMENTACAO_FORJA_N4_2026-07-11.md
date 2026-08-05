# FORJA N4 - Síntese crítica do Conselho e implementação

**Data de corte:** 11/07/2026  
**Conselho:** Efesto, Helena, Cícero e Diabob  
**Decisão central:** preservar a arquitetura e o piloto; corrigir auto-certificação; não promover `default_on`.

## 1. Veredito integrado

Os quatro pareceres convergiram no ponto decisivo: a FORJA N4 já possui uma arquitetura útil de representação, rastreabilidade, testes, ciência, entrega e gestão, mas parte de sua evidência de qualidade ainda era produzida e aceita pelo próprio fluxo. O problema não exigia recomeçar. Exigia substituir declarações por recomputação.

O conselho também revelou uma falha jurídica que a auditoria mecânica não capturava: os três canários registravam `adopt_with_qualification` para Helena e Cícero, embora os pareceres reais não sustentassem esse consenso. Patrícia/Fábio e Libra Sul estavam expressamente bloqueados por Cícero; Helena havia produzido análise transversal ou parecer com inferências ainda pendentes. A decisão foi corrigida para `review_required`/`reject_current_version`.

## 2. Disposição das recomendações

| Recomendação | Decisão | Implementação |
|---|---|---|
| Reexecutar F7 contra o texto canônico | ACEITA | `validate_case()` localiza a fonte registrada, confere SHA-256, reexecuta testes e mutações e compara o núcleo do resultado |
| Vincular modo e tempo ao hash da suíte | ACEITA | hash inclui modo, declaração temporal, datas e justificativa; datas prospectivas exigem ISO 8601 com fuso |
| Rejeitar scores impossíveis ou sem detalhe | ACEITA | invariantes de faixa, total, mortos, lista aplicável e ordem dos testes |
| Caso vazio não pode ser aprovado | ACEITA | estado `not_evaluated`; `complete=false`; `approved=false` |
| Artefato aplicável em `draft` não aprova | ACEITA | `N4-ARTIFACT-STATUS` |
| Registro de fontes vazio em piloto não aprova | ACEITA | fonte aplicável exige hash registrado e caminho verificável |
| C1-C5 devem ser reproduzidas | ACEITA | replay de hashes, fidelidade, F7, questões e QA visual por página |
| QA visual em lote | ACEITA COM CORREÇÃO | execução página a página, imagem e hash; rotulada como automática, não revisão humana |
| Conselho obrigatório e verificável | ACEITA | decisões enumeradas, parecer e localizador obrigatórios; rejeição/pendência vira P1 e impede promoção/liberação |
| Citações materiais e regimento no status de liberação | ACEITA | `releaseGates` exige ledger de citações materiais, regimento registrado e entrega aplicável confirmada |
| Mutation score literal como prova semântica | REJEITADA | painel passa a chamar “mutações literais”; promoção exige também `semanticMutationScore >= 0,8` |
| “Sigma” como variância operacional | REJEITADA | renomeado para `scenarioDispersion`; relatório declara que variância operacional não foi medida |
| Mais agentes como substituto de prova | REJEITADA | independência nominal não basta; resultado crítico é recomputado |
| Travas genéricas de privacidade | REJEITADA | nenhuma barreira desse tipo foi acrescentada |

## 3. Estado real após a implementação

### Baselines retrospectivas

Patrícia/Fábio, Libra Sul e Saúde:

- 24/24 artefatos presentes;
- F7 reexecutado contra o texto canônico registrado;
- 10/10 testes literais e 10/10 mutações literais;
- C1-C5 reproduzidas;
- `approved=true` apenas no sentido estrutural de baseline;
- dois P1 por caso: Helena não aprovou para uso final e Cícero rejeitou a versão corrente;
- `promotionEligible=false`;
- `legalReleaseStatus=human_review_required`.

### Cafelana

Permanece bloqueada. A fonte da minuta está revogada e o AgInt primário da União de 24/06/2026 ainda não foi incorporado. Nenhuma correção mecânica substitui esse documento.

## 4. Métricas válidas e limites

O avaliador v2 mede apenas resistência à auto-certificação mecânica. Ele não mede mérito jurídico, prontidão para protocolo, aprovação do conselho nem chance de êxito.

- matriz de confusão: 3 controles válidos aceitos, 6 entradas inválidas bloqueadas, zero falsa aprovação e zero falso bloqueio no corpus pequeno;
- bateria E2E v3: 10/10 cenários;
- alteração benigna de formatação JSON: aceita;
- adulterações de score literal, score semântico, hash do texto, registro de fontes, status do artefato, evidência C1 e classificação temporal: bloqueadas;
- `scenarioDispersion` mede separação entre cenários escolhidos, não estabilidade em produção;
- mutação literal não mede inversão de tese, troca de parte, valor, recurso ou relação entre precedente e proposição.

## 5. Pendências deliberadamente mantidas

1. Criar operadores de mutação semântica e corpus reservado antes de qualquer promoção.
2. Executar ao menos três ciclos prospectivos novos, com testes congelados antes da redação.
3. Produzir pareceres Helena e Cícero específicos, anteriores à versão final e ligados à tese por localizador.
4. Registrar regimento do tribunal e ledger de citações materiais no manifesto do ciclo.
5. Resolver as objeções jurídicas das três peças antes de qualquer envio.
6. Incorporar controles benignos adicionais para medir excesso de bloqueio.

## 6. Critério de promoção

`promotionEligible=true` somente quando todos os requisitos forem verdadeiros: aprovação agregada, suíte prospectiva, cobertura de mutação literal >= 80%, cobertura de mutação semântica >= 80%, consistência global reproduzida e decisões verificáveis de Helena e Cícero. Score médio não compensa falha crítica.

## 7. Evidências

- `reports/CONSELHO_EFESTO_FORJA_N4_2026-07-11.md`
- `reports/CONSELHO_HELENA_FORJA_N4_2026-07-11.md`
- `reports/CONSELHO_CICERO_FORJA_N4_2026-07-11.md`
- `reports/CONSELHO_DIABOB_FORJA_N4_2026-07-11.md`
- `reports/N4_E2E_ANTI_SELF_CERTIFICATION_2026-07-11.json`
- `reports/N4_ANTI_FRAUD_AUDIT_RESULT.json`
- `telemetria/N4_E2E_ANTI_SELF_CERTIFICATION_2026-07-11.json`
- `telemetria/N4_ANTI_FRAUD_AUDIT_2026-07-11.json`

### Verificação final executada

- 130 testes automatizados aprovados; 2 dependentes do ambiente principal foram omitidos;
- bateria E2E anti-autocertificação v3: 10/10;
- matriz mecânica: 3 válidos aceitos, 6 inválidos bloqueados, zero falsa aprovação e zero falso bloqueio no corpus atual;
- regressão de citações: 6/6 falhas detectadas e 6/6 controles legítimos preservados;
- produção real: 3 produtos renderizados pelo Word COM, 60 páginas, 15 DOCX varridos e zero asterisco residual;
- ressalvas reais preservadas: 21 P1 nos três renders e 39/54 citações ainda não conferidas no corpus amplo;
- 16 diagramas Mermaid renderizados sem erro;
- gestão: 20 casos sincronizados, um duplicado ignorado de forma explícita e zero erro;
- painel local respondeu HTTP 200 e contém os indicadores “Conselho pendente”, “Mutações literais” e “QA visual automática”.

## 8. Conclusão

A N4 ficou mais confiável porque perdeu dois falsos confortos: o score autoatribuído e o consenso fictício do conselho. O piloto continua funcionando; a gestão continua recebendo seu estado; e nenhuma peça original foi sobrescrita. O que ainda não existe permanece visível como pendência, sem bloquear genericamente o restante da fábrica.
