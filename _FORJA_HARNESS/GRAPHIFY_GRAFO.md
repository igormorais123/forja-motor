# Graphify — grafo de FORJA Harness

> Grafo arquitetural sanitizado, gerado em 2026-08-05T00:22:04-03:00. O conteúdo de arquivos privados não foi aberto nem enviado a modelo semântico.

## Resultado executivo

O Graphify materializou **1185 nós**, **1193 arestas dirigidas** e **110 comunidades**. O custo semântico foi **0 tokens**, pois a extração usa metadados do sistema de arquivos e relações arquiteturais explicitamente curadas.

Arquivos principais:

- [`graph.html`](00_MAPA_ARQUITETURA_IA/graphify-out/graph.html) — exploração interativa.
- [`graph.json`](00_MAPA_ARQUITETURA_IA/graphify-out/graph.json) — grafo GraphRAG-ready.
- [`GRAPH_REPORT.md`](00_MAPA_ARQUITETURA_IA/graphify-out/GRAPH_REPORT.md) — relatório nativo Graphify.
- [`ANALISE_ESTRUTURAL.json`](00_MAPA_ARQUITETURA_IA/graphify-out/ANALISE_ESTRUTURAL.json) — métricas e perguntas sugeridas.
- [`INVENTARIO_ESTRUTURAL.json`](00_MAPA_ARQUITETURA_IA/INVENTARIO_ESTRUTURAL.json) — cobertura e metadados usados.

## Modelo de confiança

| Relação/nó | Confiança | Origem |
| --- | --- | --- |
| `contains` | `EXTRACTED` | Relação pai-filho observada no sistema de arquivos |
| Documento marcador | `EXTRACTED` | Nome, caminho, tamanho e data; conteúdo não lido |
| Componente arquitetural | `INFERRED` | Curadoria baseada em instruções e marcadores vivos |
| Relações entre componentes | `EXTRACTED` quando há evidência nominal | Evidência registrada em cada aresta |

## Distribuição de relações

| Relação | Arestas |
| --- | --- |
| contains | 1169 |
| has_architecture_component | 15 |
| gates | 2 |
| evidences | 2 |
| precedes | 1 |
| requires | 1 |
| opens | 1 |
| proposes | 1 |
| signals | 1 |

## Categorias estruturais

| Categoria | Diretórios |
| --- | --- |
| domínio/projeto | 589 |
| configuração | 8 |
| código/contrato | 8 |
| qualidade/saída | 8 |
| documentação/planejamento | 5 |
| estado/dados | 4 |

## Nós centrais

| Nó | Grau | Tipo |
| --- | --- | --- |
| FORJA Harness | 55 | root |
| state | 55 | estado/dados |
| runs | 24 | domínio/projeto |
| runs | 14 | domínio/projeto |
| n3_artifacts | 13 | domínio/projeto |
| n3_artifacts | 12 | domínio/projeto |
| ciclo-2 | 11 | domínio/projeto |
| runs | 11 | domínio/projeto |
| n3_artifacts | 11 | domínio/projeto |
| runs | 11 | domínio/projeto |
| telemetria | 10 | estado/dados |
| case-email-auto-19f3f25cb64df962 | 10 | domínio/projeto |

## Documentos de entrada detectados

| Caminho | Bytes | Modificado |
| --- | --- | --- |
| AGENTS.md | 3351 | 2026-08-04T21:16:30-03:00 |
| DOCUMENTACAO_TECNICA.md | 70654 | 2026-08-03T21:36:24-03:00 |
| FORJA_SPEC_MANIFEST.json | 26332 | 2026-08-03T12:34:35-03:00 |
| MAPA_IA.md | 53183 | 2026-08-03T22:54:09-03:00 |
| README.md | 9341 | 2026-08-04T23:08:55-03:00 |
| .agents/MAPA_IA.md | 2189 | 2026-08-03T22:54:03-03:00 |
| .agents/skills/MAPA_IA.md | 2158 | 2026-08-03T22:53:39-03:00 |
| .agents/skills/forja/MAPA_IA.md | 1987 | 2026-08-03T22:53:11-03:00 |
| .claude/MAPA_IA.md | 1979 | 2026-08-03T22:54:03-03:00 |
| .codex/MAPA_IA.md | 1785 | 2026-08-03T22:53:55-03:00 |
| .planning/MAPA_IA.md | 3267 | 2026-08-03T22:53:55-03:00 |
| .planning/architecture/MAPA_IA.md | 3852 | 2026-08-03T22:53:39-03:00 |
| .planning/codebase/MAPA_IA.md | 4134 | 2026-08-03T22:53:39-03:00 |
| .planning/codebase/README.md | 3503 | 2026-07-16T23:23:17-03:00 |
| .planning/refactor/MAPA_IA.md | 6103 | 2026-08-03T22:53:39-03:00 |
| .planning/refactor/README.md | 1544 | 2026-07-15T19:16:41-03:00 |
| .planning/refactor/deliverables/MAPA_IA.md | 5581 | 2026-08-03T22:53:11-03:00 |
| .planning/refactor/deliverables/diagramas/MAPA_IA.md | 22110 | 2026-08-03T22:52:43-03:00 |
| .planning/refactor/deliverables/diagramas_pdf/MAPA_IA.md | 7976 | 2026-08-03T22:52:43-03:00 |
| .planning/refactor/deliverables/qa_contact_sheets/MAPA_IA.md | 3946 | 2026-08-03T22:52:43-03:00 |
| .planning/refactor/deliverables/qa_docx_renderer/MAPA_IA.md | 2027 | 2026-08-03T22:52:43-03:00 |
| .planning/refactor/deliverables/qa_word_pdf/MAPA_IA.md | 8186 | 2026-08-03T22:52:43-03:00 |
| .planning/refactor/plans/MAPA_IA.md | 5550 | 2026-08-03T22:53:11-03:00 |
| .planning/refactor/tools/MAPA_IA.md | 2810 | 2026-08-03T22:53:11-03:00 |
| .planning/tmp/MAPA_IA.md | 2021 | 2026-08-03T22:53:39-03:00 |
| .playwright-mcp/MAPA_IA.md | 4446 | 2026-08-03T22:53:55-03:00 |
| _scripts_oneoff/LEIA-ME.md | 1351 | 2026-07-16T23:23:17-03:00 |
| _scripts_oneoff/MAPA_IA.md | 6262 | 2026-08-03T22:53:55-03:00 |
| ar_architecture/MAPA_IA.md | 2516 | 2026-08-03T22:53:55-03:00 |
| ar_architecture/candidates/MAPA_IA.md | 2297 | 2026-08-03T22:53:38-03:00 |
| ar_architecture/candidates/post-protocol-learning-loop-v1/MAPA_IA.md | 2151 | 2026-08-03T22:53:11-03:00 |
| ar_architecture/schemas/MAPA_IA.md | 2095 | 2026-08-03T22:53:38-03:00 |
| autoresearch/MAPA_IA.md | 4610 | 2026-08-03T22:53:55-03:00 |
| autoresearch/cache/MAPA_IA.md | 10290 | 2026-08-03T22:53:38-03:00 |
| autoresearch/canarios/MAPA_IA.md | 4132 | 2026-08-03T22:53:38-03:00 |
| autoresearch/canarios/citacao_removida_real/MAPA_IA.md | 3088 | 2026-08-03T22:53:11-03:00 |
| autoresearch/canarios/citacao_removida_real/README.md | 305 | 2026-07-23T23:14:53-03:00 |
| autoresearch/canarios/estilo_ia_real/MAPA_IA.md | 3060 | 2026-08-03T22:53:11-03:00 |
| autoresearch/canarios/estilo_ia_real/README.md | 278 | 2026-07-23T23:14:53-03:00 |
| autoresearch/canarios/exemplo_placeholder/MAPA_IA.md | 2839 | 2026-08-03T22:53:11-03:00 |
| autoresearch/canarios/exemplo_placeholder/README.md | 334 | 2026-07-23T01:56:55-03:00 |
| autoresearch/canarios/origem_operacional_real/MAPA_IA.md | 3096 | 2026-08-03T22:53:11-03:00 |
| autoresearch/canarios/origem_operacional_real/README.md | 296 | 2026-07-23T23:14:53-03:00 |
| autoresearch/canarios/placeholder_real/MAPA_IA.md | 3068 | 2026-08-03T22:53:11-03:00 |
| autoresearch/canarios/placeholder_real/README.md | 282 | 2026-07-23T23:14:53-03:00 |
| autoresearch/canarios/sumula_trocada_real/MAPA_IA.md | 3080 | 2026-08-03T22:53:11-03:00 |
| autoresearch/canarios/sumula_trocada_real/README.md | 285 | 2026-07-23T23:14:53-03:00 |
| autoresearch/candidates/MAPA_IA.md | 2435 | 2026-08-03T22:53:38-03:00 |
| autoresearch/candidates/materialidade-pendencias-v1/MAPA_IA.md | 3830 | 2026-08-03T22:53:11-03:00 |
| autoresearch/ciclos/MAPA_IA.md | 3069 | 2026-08-03T22:53:38-03:00 |
| autoresearch/ciclos/ciclo-0/MAPA_IA.md | 2385 | 2026-08-03T22:53:11-03:00 |
| autoresearch/ciclos/ciclo-1/MAPA_IA.md | 7666 | 2026-08-03T22:53:11-03:00 |
| autoresearch/ciclos/ciclo-1/blind/MAPA_IA.md | 5220 | 2026-08-03T22:52:43-03:00 |
| autoresearch/ciclos/ciclo-1/exec/MAPA_IA.md | 5443 | 2026-08-03T22:52:43-03:00 |
| autoresearch/ciclos/ciclo-1/judgments/MAPA_IA.md | 4651 | 2026-08-03T22:52:43-03:00 |
| autoresearch/ciclos/ciclo-1/judgments/round1_invalidado/MAPA_IA.md | 2799 | 2026-08-03T22:52:20-03:00 |
| autoresearch/ciclos/ciclo-1/runpair-varA/MAPA_IA.md | 2406 | 2026-08-03T22:52:43-03:00 |
| autoresearch/ciclos/ciclo-1/runpair-varB/MAPA_IA.md | 2406 | 2026-08-03T22:52:43-03:00 |
| autoresearch/ciclos/ciclo-2/MAPA_IA.md | 9523 | 2026-08-03T22:53:11-03:00 |
| autoresearch/ciclos/ciclo-2/blind/MAPA_IA.md | 4818 | 2026-08-03T22:52:43-03:00 |
| autoresearch/ciclos/ciclo-2/blind2/MAPA_IA.md | 4795 | 2026-08-03T22:52:43-03:00 |
| autoresearch/ciclos/ciclo-2/exec/MAPA_IA.md | 6873 | 2026-08-03T22:52:43-03:00 |
| autoresearch/ciclos/ciclo-2/exec2/MAPA_IA.md | 6477 | 2026-08-03T22:52:43-03:00 |
| autoresearch/ciclos/ciclo-2/judgments/MAPA_IA.md | 4139 | 2026-08-03T22:52:43-03:00 |
| autoresearch/ciclos/ciclo-2/judgments/round1_invalidado/MAPA_IA.md | 2722 | 2026-08-03T22:52:20-03:00 |
| autoresearch/ciclos/ciclo-2/runpair-t1/MAPA_IA.md | 2400 | 2026-08-03T22:52:43-03:00 |
| autoresearch/ciclos/ciclo-2/runpair-t1b/MAPA_IA.md | 2403 | 2026-08-03T22:52:43-03:00 |
| autoresearch/ciclos/ciclo-2/runpair-t2/MAPA_IA.md | 2400 | 2026-08-03T22:52:43-03:00 |
| autoresearch/ciclos/ciclo-2/runpair-t2b/MAPA_IA.md | 2403 | 2026-08-03T22:52:43-03:00 |
| autoresearch/evolucao/MAPA_IA.md | 2265 | 2026-08-03T22:53:38-03:00 |
| autoresearch/evolucao/prompt-mestre-v2/MAPA_IA.md | 3345 | 2026-08-03T22:53:11-03:00 |
| autoresearch/evolucao/prompt-mestre-v2/gen-0/MAPA_IA.md | 2456 | 2026-08-03T22:52:43-03:00 |
| autoresearch/evolucao/prompt-mestre-v2/gen-1/MAPA_IA.md | 2182 | 2026-08-03T22:52:43-03:00 |
| autoresearch/evolucao/prompt-mestre-v2/winners/MAPA_IA.md | 2164 | 2026-08-03T22:52:43-03:00 |
| autoresearch/prompts/MAPA_IA.md | 2550 | 2026-08-03T22:53:38-03:00 |
| bancada_cafelana_v7/LEIA-ME.md | 9644 | 2026-07-27T16:21:51-03:00 |
| bancada_cafelana_v7/MAPA_IA.md | 6405 | 2026-08-03T22:53:55-03:00 |
| bancada_cafelana_v7/avaliacao/MAPA_IA.md | 2789 | 2026-08-03T22:53:38-03:00 |
| bancada_cafelana_v7/avaliacao/juizes/MAPA_IA.md | 2855 | 2026-08-03T22:53:11-03:00 |
| bancada_cafelana_v7/cego/MAPA_IA.md | 3304 | 2026-08-03T22:53:38-03:00 |

## Cobertura e exclusões

- Profundidade máxima: **6**.
- Symlinks/junctions não foram seguidos.
- Subárvores de dependências, caches, VCS e saídas geradas foram podadas.
- Backups/worktrees/restore zones do atlas geral aparecem como nós, mas não são expandidos.
- PDFs, DOCX, bancos, mensagens, planilhas, mídias, arquivos de ambiente e chaves foram somente contados por extensão; conteúdo não foi lido.
- O grafo não afirma atualidade operacional externa.

## Consultas úteis

1. Qual é a rota de entrada até o subsistema que preciso alterar?
2. Quais mapas e instruções governam este módulo?
3. Que diretórios são código, estado, documentação, qualidade ou saída?
4. Quais zonas foram deliberadamente podadas por privacidade ou duplicação?
5. Quais componentes arquiteturais conectam fontes, produção, gates e entrega?

## Regeneração

Use o script central `scripts/build_project_architecture_maps.py` com o Python do Graphify. A regeneração é sempre completa (`force`), compara contagens e revalida o HTML; modo incremental não deve substituir um grafo válido por extração vazia.

<!-- graphify-deep-v2:start -->
## Aprofundamento Graphify v2

O grafo agora incorpora decisões, cenários, modos de falha e fronteiras de confiança curados, totalizando **1220 nós**, **1263 arestas** e **109 comunidades**. A origem conceitual está em [`DOCUMENTACAO_ARQUITETURAL_COMPLETA.md`](00_MAPA_ARQUITETURA_IA/DOCUMENTACAO_ARQUITETURAL_COMPLETA.md).
<!-- graphify-deep-v2:end -->

<!-- graphify-interfaces-v3:start -->
## Interfaces inferiores v3

O grafo possui agora **3156 nós** e **9136 arestas**, incluindo módulos, funções, métodos, comandos, opções e schemas com evidência de arquivo/linha.
<!-- graphify-interfaces-v3:end -->

<!-- strategy-v4:start -->
## Diagnóstico e propostas v4

O grafo inclui achados observados, propostas e ordem de migração. Consulte por IDs `P-*` ou abra [`ANALISE_ARQUITETURAL_E_PROPOSTAS.md`](00_MAPA_ARQUITETURA_IA/ANALISE_ARQUITETURAL_E_PROPOSTAS.md). Grafo após a camada estratégica: **3156 nós / 9136 arestas**.
<!-- strategy-v4:end -->
