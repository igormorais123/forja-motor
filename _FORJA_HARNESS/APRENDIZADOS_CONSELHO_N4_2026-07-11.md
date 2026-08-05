# Aprendizados do Conselho FORJA N4

**Data:** 11/07/2026  
**Origem:** auditorias independentes de Efesto, Helena, Cícero e Diabob, síntese crítica e implementação validada.

## Decisão que deve sobreviver às próximas sessões

A FORJA N4 não deve ser reescrita nem promovida. Ela deve permanecer em `pilot_blocking` enquanto transforma declarações internas em evidência recomputável. As três baselines M6 são úteis para regressão mecânica, mas não são peças liberadas nem ciclos prospectivos.

## Estado canônico

| Caso | Estrutura | Conselho | Promoção | Liberação |
|---|---|---|---|---|
| Patrícia/Fábio | 24/24, zero P0, 10/10 testes e mutações literais | 2 P1 | não elegível | revisão humana |
| Libra Sul | 24/24, zero P0, 10/10 testes e mutações literais | 2 P1 | não elegível | revisão humana |
| Saúde | 24/24, zero P0, 10/10 testes e mutações literais | 2 P1 | não elegível | revisão humana |
| Cafelana | bloqueada por fonte revogada e ato primário ausente | não libera | não elegível | bloqueada |

## Invariantes incorporados

1. `validate_case()` reexecuta F7 contra o texto canônico; resultado salvo não se autocertifica.
2. `suiteHash` inclui o contrato temporal; data prospectiva exige fuso.
3. `0 <= killed <= total`, `score=killed/total` e lista de mutações coerente.
4. Caso vazio é `not_evaluated`.
5. Artefato aplicável precisa estar `approved`.
6. C1-C5 são reproduzidas a partir das evidências estruturadas.
7. Conselho exige decisão, parecer e localizador; parecer contrário não vira aprovação com ressalva.
8. QA visual automática não substitui revisão humana.
9. Gestão revalida o maior alvo N4 auditado.
10. Aprovação estrutural, liberação e promoção nunca são sinônimos.

## O que ainda falta

- operadores de mutação semântica por família de risco jurídico;
- três ciclos prospectivos novos;
- ledger de citações materiais e regimento por caso;
- pareceres Helena/Cícero específicos e anteriores ao produto final;
- corpus reservado com mais controles benignos e medição de falso bloqueio;
- resolução das objeções jurídicas das três peças antes de qualquer envio.

## Métricas que podem ser afirmadas

- 130 testes automatizados aprovados, com 2 omissões ambientais;
- E2E anti-autocertificação v3: 10/10;
- corpus atual: 3 válidos aceitos, 6 inválidos bloqueados, zero falsa aprovação/falso bloqueio;
- produção real: 3 documentos, 60 páginas, 15 DOCX e 21 P1 preservados;
- 54 citações detectadas, 15 conferidas e 39 pendentes no corpus amplo;
- 16 diagramas Mermaid renderizados;
- gestão sincronizada sem erro e painel HTTP 200.

Essas métricas não autorizam afirmar mérito jurídico, chance de êxito, prontidão para protocolo ou variância operacional.

## Documentos de autoridade

1. `FORJA_SPEC_MANIFEST.json`
2. `reports/CONSELHO_SINTESE_IMPLEMENTACAO_FORJA_N4_2026-07-11.md`
3. `planejamento/10_PRD_FORJA_N4_RACIOCINIO_PROVA_CIENCIA.md`
4. `planejamento/11_TDD_FORJA_N4_RACIOCINIO_PROVA_CIENCIA.md`
5. `planejamento/12_ROADMAP_FORJA_N4_RACIOCINIO_PROVA_CIENCIA.md`
6. `planejamento/13_DIAGRAMAS_FORJA_N4_RACIOCINIO_PROVA_CIENCIA.md`
7. `RETROSPECTIVAS.md`, Lições 49-60

