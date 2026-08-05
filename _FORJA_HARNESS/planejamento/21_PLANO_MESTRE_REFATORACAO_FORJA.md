# Plano mestre de refatoração segura da FORJA

**Status:** planejamento concluído; execução não autorizada  
**Data-base:** 15/07/2026  
**Pacote canônico:** `../.planning/refactor/`

Este arquivo integra o novo programa de refatoração ao índice histórico da FORJA sem duplicar documentos normativos nem substituir os planos N2, N3 ou N4 já existentes.

## Fonte de verdade

1. `../.planning/refactor/README.md` — índice e ordem de leitura.
2. `../.planning/refactor/01-PRD_REFATORACAO_FORJA.md` — produto, requisitos e invariantes.
3. `../.planning/refactor/02-TDD_REFATORACAO_FORJA.md` — desenho técnico e estratégia TDD.
4. `../.planning/refactor/03-ROADMAP_REFATORACAO_FORJA.md` — ondas, gates, esforço e dependências.
5. `../.planning/refactor/04-DIAGRAMAS_REFATORACAO_FORJA.md` — atlas Mermaid.
6. `../.planning/refactor/05-MATRIZ_RASTREABILIDADE.md` — requisitos, planos, testes e evidências.
7. `../.planning/refactor/06-TESTES_ROLLBACK_E_CUTOVER.md` — validação, rollback e encerramento.
8. `../.planning/refactor/plans/` — 18 planos executáveis P00–P16, com P13 dividido em P13A/P13B.

## Limite desta entrega

O pacote descreve como limpar, deduplicar, modularizar e documentar o sistema preservando comportamento jurídico, trilha de prova e compatibilidade. Nenhuma refatoração funcional, migração física, remoção de arquivo, promoção normativa ou cutover foi executado nesta etapa.
