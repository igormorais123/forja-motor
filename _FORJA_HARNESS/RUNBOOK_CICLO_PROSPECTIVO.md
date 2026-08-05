# Runbook — Ciclo prospectivo N4 (M3.3 do plano 19)

> Criado em 12/07/2026. A promoção N4 e o destravamento do N3 exigem **3 ciclos NOVOS**
> (classes/tribunais distintos) com congelamento anterior à redação. Este runbook é o
> checklist de 1 página de cada ciclo. Regra de seleção: as próximas 3 demandas reais de
> classes distintas entram no piloto automaticamente, salvo urgência declarada pelo Igor
> (nesse caso a demanda roda N2 e não conta como ciclo).

## Antes da redação (congelamento)

1. [ ] Caso criado em `state/<caseId>/` com `FORJA_CASE_MANIFEST.json.mode = "pilot_blocking"`.
2. [ ] F4 completo: blueprint + árvore de questões geradas (`forja_reasoning.py`).
3. [ ] **Pareceres Helena e Cícero emitidos ANTES de qualquer artefato de F6**
       (a ordem é verificada pelo gate M2.1 do `forja_delivery.py` — parecer nascido
       depois do F6 reprova com `PARECER_POS_REDACAO`).
4. [ ] Congelar: registrar no event store o hash SHA-256 do blueprint e da árvore de
       questões (evento `artifact_created` com `payload.frozen = true`). Nada disso pode
       mudar depois que o F6 começar; mudança exige novo ciclo, não emenda.

## Durante o ciclo

5. [ ] Pipeline completo F5-F10 com gates normais (nenhuma exceção de piloto).
6. [ ] Validação N4 integral: `forja_n4_validate.py` + `forja_n4_e2e_adversarial.py`
       + `forja_case_tests.py` (C1-C5) sobre o caso.
6-b. [ ] Mutação semântica: `python forja_mutation_semantic.py <caseId>` →
       `n4_artifacts/F7_SEMANTIC_MUTATION.json` com `semanticMutationScore >= 0.8`,
       `suiteValida = true` e zero controles benignos mortos (critério 3 de promoção).
       Baselines de 12/07 para comparação: Patrícia 0.17, Libra Sul 0.20, Saúde 0.0 —
       famílias fracas nominadas no JSON indicam qual detector construir a seguir.
7. [ ] Toda ocorrência inesperada vira nota no `MAPA_IA.md` do caso na hora (não depois).

## Ao final do ciclo

8. [ ] Colher os 10 critérios de promoção (PRD N4 §promoção) e registrar cada um como
       atendido/não atendido no `FORJA_CASE_MANIFEST.json` (`n4Pilot.promotionChecklist`).
9. [ ] Registrar o par (`mode`, `promotionEligible`) — sem colapsar `approved` /
       `legalReleaseStatus` / `promotionEligible` (são três coisas distintas).
10. [ ] Artefatos congelados do ciclo entram no corpus antifraude
        (`n4_schemas/corpus_mutacao_semantica/` quando M3.1 existir) como caso de teste.
11. [ ] Lição nova → `RETROSPECTIVAS.md`; contagem de ciclos válidos atualizada abaixo.

## Contagem de ciclos válidos

| # | Caso | Classe/Tribunal | Congelado em | Resultado | Válido? |
|---|---|---|---|---|---|
| — | (nenhum ciclo prospectivo executado até 12/07/2026) | | | | |

Baselines retrospectivas (Patrícia, Libra Sul, Saúde) NÃO contam — não houve
congelamento anterior à redação. Cafelana AgInt: revogada (origem invalidada).
