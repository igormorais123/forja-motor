# Runbook - validação do Conselho FORJA N4

## Quando usar

- depois de alterar testes, schemas, validador, consistência, QA ou gestão;
- antes de declarar uma baseline válida;
- antes de iniciar M6.4;
- depois de qualquer regeneração dos canários.

## Sequência obrigatória

Executar na raiz da fábrica:

```powershell
python -m unittest discover -s _FORJA_HARNESS -p 'test_*.py'
python _FORJA_HARNESS\test_forja_citacoes.py
python _FORJA_HARNESS\forja_n4_e2e_adversarial.py --output _FORJA_HARNESS\telemetria\N4_E2E_ANTI_SELF_CERTIFICATION_2026-07-11.json
python _FORJA_HARNESS\forja_n4_anti_fraud_audit.py
python _FORJA_HARNESS\test_real_telemetria_licao41.py
python -m unittest discover -s _FORJA_HARNESS -p 'test_forja_pso_pet.py' -v
python _FORJA_HARNESS\forja_pso_pet.py benchmark --output _FORJA_HARNESS\reports\PSO_PET_BENCHMARK_REAL_2026-07-11.json
python gestao_escritorio\scripts\sync_forja_gestao.py --reconcile --apply
python gestao_escritorio\scripts\render_dashboard.py
```

## Critérios de aceite do piloto

- testes automatizados sem falha;
- E2E aprovado e controle benigno aceito;
- `invalidAccepted=0`;
- canários com `caseTestMode=retrospective_baseline`;
- `promotionEligible=false` enquanto não houver mutação semântica e ciclos prospectivos;
- conselho pendente visível;
- CASO-04 bloqueada;
- sidecar sem erro e painel HTTP 200;
- P1 e citações não verificadas continuam visíveis.

## Critérios de promoção futura

Todos, sem compensação por média:

1. ciclo prospectivo com congelamento anterior à redação;
2. mutação literal >= 80%;
3. mutação semântica >= 80% e nenhuma família crítica vazia;
4. C1-C5 reproduzidas;
5. Helena e Cícero aprovam com parecer específico e localizador;
6. citações materiais 100% verificadas ou retiradas;
7. regimento vigente registrado;
8. QA automática e revisão humana completas;
9. entrega aplicável confirmada;
10. três ciclos novos de classes/tribunais distintos.

## Interpretação correta

- `approved=true`: estrutura avaliada passou sem P0.
- `legalReleaseStatus=human_review_required`: não protocolar com base no status estrutural.
- `promotionEligible=false`: não ligar `default_on`.
- `mutationScore=1.0`: cobertura literal; não significa sentido preservado.
- `operationalVarianceMeasured=false`: não usar `scenarioDispersion` como estabilidade produtiva.

## Rollback

Em regressão, manter N2/N3 e colocar N4 em `shadow` ou `off` no `FORJA_N3_CONFIG.json`. Não apagar artefatos nem reescrever estados históricos. Reconciliar a gestão depois da mudança.

## PSO-Pet

- ausência de `PSO_CASE.json` significa `not_evaluated`, não reprovação retroativa;
- `PSO_CASE.json` deve ser congelado antes do texto final em ciclo prospectivo;
- perfis `full` e `intensive` exigem alternativa substantivamente distinta;
- nenhum score agregado compensa P0 ou dimensão crítica baixa;
- circularidade de fonte gera correção de proveniência, não remoção automática da tese;
- promoção depende de três casos prospectivos e medição de retrabalho real.
