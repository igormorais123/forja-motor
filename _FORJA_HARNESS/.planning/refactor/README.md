# FORJA R1 — Plano mestre de refatoração estrutural

**Status:** planejado; execução não iniciada  
**Data-base:** 2026-07-15  
**Escopo:** limpeza, modularização, deduplicação, boas práticas, atlas Mermaid e preparação para mudanças futuras

## Leitura obrigatória

1. `00-CONTEXT.md` — decisões travadas e limites.
2. `01-PRD_REFATORACAO_FORJA.md` — requisitos e invariantes.
3. `02-TDD_REFATORACAO_FORJA.md` — desenho técnico e estratégia TDD.
4. `03-ROADMAP_REFATORACAO_FORJA.md` — ondas, dependências e gates.
5. `04-DIAGRAMAS_REFATORACAO_FORJA.md` — atlas Mermaid do trabalho.
6. `05-MATRIZ_RASTREABILIDADE.md` — requisito → plano → teste → evidência.
7. `06-TESTES_ROLLBACK_E_CUTOVER.md` — validação real, rollback e conclusão.
8. `plans/` — 18 planos executáveis por fase (P00–P16, com P13 dividido em A/B).

## Regra central

> Preservar o comportamento jurídico e a trilha de prova; centralizar fontes de verdade; migrar por fachadas; remover somente depois de equivalência comprovada.

## Estado normativo que o plano não altera

- N2 continua vigente.
- N3 continua base operacional em sombra, com sidecar de gestão ativo.
- N4 continua candidata em `pilot_blocking`.
- F2-A `FORJA-F2A-100-v1` continua obrigatório em casos novos.
- Refatoração estrutural não equivale a promoção de especificação.

## Pacote final

O documento consolidado será produzido em `deliverables/PLANO_MESTRE_REFATORACAO_FORJA_2026-07-15.pdf`, com versão DOCX editável e diagramas vetoriais.
