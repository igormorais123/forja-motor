# Graphify — grafo de Fábrica de melhoria de petições

> Grafo arquitetural sanitizado, gerado em 2026-07-30T02:36:14-03:00. O conteúdo de arquivos privados não foi aberto nem enviado a modelo semântico.

## Resultado executivo

O Graphify materializou **1187 nós**, **1190 arestas dirigidas** e **136 comunidades**. O custo semântico foi **0 tokens**, pois a extração usa metadados do sistema de arquivos e relações arquiteturais explicitamente curadas.

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
| contains | 1174 |
| has_architecture_component | 12 |
| routes_through | 1 |
| routes_to | 1 |
| requires | 1 |
| feeds | 1 |

## Categorias estruturais

| Categoria | Diretórios |
| --- | --- |
| domínio/projeto | 727 |
| qualidade/saída | 35 |
| documentação/planejamento | 32 |
| configuração | 25 |
| código/contrato | 11 |
| estado/dados | 7 |

## Nós centrais

| Nó | Grau | Tipo |
| --- | --- | --- |
| entregas_fabio_osorio | 114 | domínio/projeto |
| Fábrica de melhoria de petições | 99 | root |
| state | 54 | estado/dados |
| _FORJA_HARNESS | 41 | domínio/projeto |
| Apresentação PPT Miami Fabio | 22 | domínio/projeto |
| Natura Cabreúva - Parecer e Quesitos - prazo 20-07-2026 | 18 | domínio/projeto |
| 12_REBUILD | 15 | domínio/projeto |
| Análise de caso pessoal Fábio Medina Osório - Plano de Saúde | 14 | domínio/projeto |
| Conteudo_Redes_Celina_Leao_VEJA_2026-07-17 | 14 | domínio/projeto |
| Jalusa Prestes Abaide - Proc. 5000447-02.2011.4.04.7102 | 14 | domínio/projeto |
| _entrega_v9_2026-07-19 | 13 | domínio/projeto |
| contrarrazões ao AgInt no AREsp nº 2.698.443D | 13 | domínio/projeto |

## Documentos de entrada detectados

| Caminho | Bytes | Modificado |
| --- | --- | --- |
| AGENTS.md | 21109 | 2026-07-29T01:31:43-03:00 |
| ATUALIZAR_MAPA_IA.ps1 | 578 | 2026-07-08T04:22:22-03:00 |
| CLAUDE.md | 23273 | 2026-07-25T18:53:19-03:00 |
| MAPA_IA.md | 610430 | 2026-07-30T02:35:39-03:00 |
| .agents/MAPA_IA.md | 1801 | 2026-07-30T02:35:38-03:00 |
| .autoresearch/MAPA_IA.md | 3242 | 2026-07-30T02:35:38-03:00 |
| .autoresearch/fabrica-peticoes-v1/MAPA_IA.md | 5940 | 2026-07-30T02:35:37-03:00 |
| .autoresearch/forja-arch-diagram-v1/MAPA_IA.md | 4479 | 2026-07-30T02:35:37-03:00 |
| .claude/MAPA_IA.md | 1801 | 2026-07-30T02:35:38-03:00 |
| .codex/MAPA_IA.md | 1798 | 2026-07-30T02:35:38-03:00 |
| .planning/MAPA_IA.md | 2222 | 2026-07-30T02:35:38-03:00 |
| .planning/architecture/MAPA_IA.md | 3845 | 2026-07-30T02:35:37-03:00 |
| .playwright-cli/MAPA_IA.md | 5585 | 2026-07-30T02:35:38-03:00 |
| .playwright-mcp/MAPA_IA.md | 14256 | 2026-07-30T02:35:38-03:00 |
| 00_IA_NAVIGACAO/STATUS_MAPA_IA.md | 934 | 2026-07-30T02:35:39-03:00 |
| _ferramentas/LEIA-ME.md | 6094 | 2026-07-08T04:13:19-03:00 |
| _ferramentas/MAPA_IA.md | 5934 | 2026-07-30T02:35:38-03:00 |
| _ferramentas/.autoresearch/MAPA_IA.md | 3651 | 2026-07-30T02:35:37-03:00 |
| _FORJA_HARNESS/AGENTS.md | 3346 | 2026-07-29T22:56:39-03:00 |
| _FORJA_HARNESS/DOCUMENTACAO_TECNICA.md | 62932 | 2026-07-27T17:31:13-03:00 |
| _FORJA_HARNESS/FORJA_SPEC_MANIFEST.json | 26109 | 2026-07-29T00:17:54-03:00 |
| _FORJA_HARNESS/MAPA_IA.md | 50939 | 2026-07-30T02:35:38-03:00 |
| _FORJA_HARNESS/README.md | 8758 | 2026-07-29T22:47:47-03:00 |
| _FORJA_HARNESS/.agents/MAPA_IA.md | 2189 | 2026-07-30T02:35:37-03:00 |
| _FORJA_HARNESS/.claude/MAPA_IA.md | 1979 | 2026-07-30T02:35:37-03:00 |
| _FORJA_HARNESS/.codex/MAPA_IA.md | 1785 | 2026-07-30T02:35:37-03:00 |
| _FORJA_HARNESS/.planning/MAPA_IA.md | 3267 | 2026-07-30T02:35:37-03:00 |
| _FORJA_HARNESS/.playwright-mcp/MAPA_IA.md | 4446 | 2026-07-30T02:35:37-03:00 |
| _FORJA_HARNESS/_scripts_oneoff/LEIA-ME.md | 1351 | 2026-07-16T23:23:17-03:00 |
| _FORJA_HARNESS/_scripts_oneoff/MAPA_IA.md | 6262 | 2026-07-30T02:35:37-03:00 |
| _FORJA_HARNESS/ar_architecture/MAPA_IA.md | 2516 | 2026-07-30T02:35:37-03:00 |
| _FORJA_HARNESS/autoresearch/MAPA_IA.md | 4610 | 2026-07-30T02:35:37-03:00 |
| _FORJA_HARNESS/bancada_cafelana_v7/LEIA-ME.md | 9644 | 2026-07-27T16:21:51-03:00 |
| _FORJA_HARNESS/bancada_cafelana_v7/MAPA_IA.md | 6405 | 2026-07-30T02:35:37-03:00 |
| _FORJA_HARNESS/blender_atlas/MAPA_IA.md | 1806 | 2026-07-30T02:35:37-03:00 |
| _FORJA_HARNESS/cache/MAPA_IA.md | 4510 | 2026-07-30T02:35:37-03:00 |
| _FORJA_HARNESS/contracts/MAPA_IA.md | 2429 | 2026-07-30T02:35:37-03:00 |
| _FORJA_HARNESS/docs/MAPA_IA.md | 3269 | 2026-07-30T02:35:37-03:00 |
| _FORJA_HARNESS/FORJA/MAPA_IA.md | 2171 | 2026-07-30T02:35:37-03:00 |
| _FORJA_HARNESS/learning_registry/MAPA_IA.md | 2027 | 2026-07-30T02:35:37-03:00 |
| _FORJA_HARNESS/n4_fixtures/MAPA_IA.md | 2443 | 2026-07-30T02:35:37-03:00 |
| _FORJA_HARNESS/n4_schemas/MAPA_IA.md | 9504 | 2026-07-30T02:35:37-03:00 |
| _FORJA_HARNESS/PETICAO_ACORDO_DOUTORADO_FORJA_20260715/MAPA_IA.md | 3461 | 2026-07-30T02:35:37-03:00 |
| _FORJA_HARNESS/PETICAO_ENDERECO_EXEQUIBILIDADE_FORJA_20260715/MAPA_IA.md | 3479 | 2026-07-30T02:35:37-03:00 |
| _FORJA_HARNESS/phase_contracts/MAPA_IA.md | 3259 | 2026-07-30T02:35:37-03:00 |
| _FORJA_HARNESS/phase_contracts_n4/MAPA_IA.md | 3433 | 2026-07-30T02:35:36-03:00 |
| _FORJA_HARNESS/planejamento/MAPA_IA.md | 19137 | 2026-07-30T02:35:36-03:00 |
| _FORJA_HARNESS/private/MAPA_IA.md | 2190 | 2026-07-30T02:35:36-03:00 |
| _FORJA_HARNESS/pso_schemas/MAPA_IA.md | 2205 | 2026-07-30T02:35:36-03:00 |
| _FORJA_HARNESS/reports/MAPA_IA.md | 316587 | 2026-07-30T02:35:36-03:00 |
| _FORJA_HARNESS/state/MAPA_IA.md | 19282 | 2026-07-30T02:35:36-03:00 |
| _FORJA_HARNESS/telemetria/MAPA_IA.md | 37962 | 2026-07-30T02:35:36-03:00 |
| _FORJA_HARNESS/templates/MAPA_IA.md | 3202 | 2026-07-30T02:35:36-03:00 |
| _FORJA_HARNESS/youtube-transcript/MAPA_IA.md | 2564 | 2026-07-30T02:35:36-03:00 |
| _LABORATÓRIO_MIROFISH — Vale Trading (EXPERIMENTAL — NÃO É PROVA)/MAPA_IA.md | 6357 | 2026-07-30T02:35:38-03:00 |
| _LABORATÓRIO_MIROFISH — Vale Trading (EXPERIMENTAL — NÃO É PROVA)/MIROFISH_EVOLUTION_REPORT_4e333c5ce6bb/MAPA_IA.md | 2692 | 2026-07-30T02:35:36-03:00 |
| _LEIS_GERAIS/LEIA-ME.md | 1495 | 2026-07-06T19:37:27-03:00 |
| _LEIS_GERAIS/MAPA_IA.md | 2883 | 2026-07-30T02:35:38-03:00 |
| _MODELOS/LEIA-ME.md | 2591 | 2026-07-09T16:49:10-03:00 |
| _MODELOS/MAPA_IA.md | 2219 | 2026-07-30T02:35:38-03:00 |
| _ocr_estre_complemento_2026-07-29/MAPA_IA.md | 3098 | 2026-07-30T02:35:38-03:00 |
| _ocr_estre_complemento_2026-07-29/contatos/MAPA_IA.md | 2501 | 2026-07-30T02:35:36-03:00 |
| _ocr_estre_complemento_2026-07-29/paginas/MAPA_IA.md | 8773 | 2026-07-30T02:35:36-03:00 |
| _ocr_estre_erm_2026-07-29/MAPA_IA.md | 3403 | 2026-07-30T02:35:38-03:00 |
| _ocr_estre_erm_2026-07-29/contatos/MAPA_IA.md | 4466 | 2026-07-30T02:35:36-03:00 |
| _ocr_estre_erm_2026-07-29/paginas/MAPA_IA.md | 47143 | 2026-07-30T02:35:36-03:00 |
| AI 0011621-15.2023.8.27.2700 – ajustes finais nos memoriais/MAPA_IA.md | 3509 | 2026-07-30T02:35:38-03:00 |
| AI 0011621-15.2023.8.27.2700 – ajustes finais nos memoriais/Anexos do email/MAPA_IA.md | 2564 | 2026-07-30T02:35:36-03:00 |
| Amplify Legal500 - análise preliminar 2026-07-19/MAPA_IA.md | 3028 | 2026-07-30T02:35:38-03:00 |
| Análise de caso pessoal Fábio Medina Osório - Plano de Saúde/MAPA_IA.md | 23601 | 2026-07-30T02:35:38-03:00 |
| Análise de caso pessoal Fábio Medina Osório - Plano de Saúde/.agents/MAPA_IA.md | 1937 | 2026-07-30T02:35:36-03:00 |
| Análise de caso pessoal Fábio Medina Osório - Plano de Saúde/.codex/MAPA_IA.md | 1934 | 2026-07-30T02:35:36-03:00 |
| Análise de caso pessoal Fábio Medina Osório - Plano de Saúde/_entrega_v9_2026-07-19/MAPA_IA.md | 41345 | 2026-07-30T02:35:36-03:00 |
| Análise de caso pessoal Fábio Medina Osório - Plano de Saúde/_forja_n3_reabertura_verifact_2026-07-15/MAPA_IA.md | 5798 | 2026-07-30T02:35:36-03:00 |
| Análise de caso pessoal Fábio Medina Osório - Plano de Saúde/_forja_n3_reconstrucao_2026-07-10/MAPA_IA.md | 13620 | 2026-07-30T02:35:36-03:00 |
| Análise de caso pessoal Fábio Medina Osório - Plano de Saúde/_forja_n3_reconstrucao_2026-07-14/MAPA_IA.md | 6182 | 2026-07-30T02:35:36-03:00 |
| Análise de caso pessoal Fábio Medina Osório - Plano de Saúde/_nivel_sol_qa/MAPA_IA.md | 6618 | 2026-07-30T02:35:36-03:00 |
| Análise de caso pessoal Fábio Medina Osório - Plano de Saúde/_nivel_sol_work/MAPA_IA.md | 5986 | 2026-07-30T02:35:36-03:00 |
| Análise de caso pessoal Fábio Medina Osório - Plano de Saúde/Anexos do email/MAPA_IA.md | 20679 | 2026-07-30T02:35:36-03:00 |
| Análise de caso pessoal Fábio Medina Osório - Plano de Saúde/Anexos WhatsApp 2026-07-14/MAPA_IA.md | 3473 | 2026-07-30T02:35:35-03:00 |

## Cobertura e exclusões

- Profundidade máxima: **3**.
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

O grafo agora incorpora decisões, cenários, modos de falha e fronteiras de confiança curados, totalizando **1206 nós**, **1228 arestas** e **141 comunidades**. A origem conceitual está em [`DOCUMENTACAO_ARQUITETURAL_COMPLETA.md`](00_MAPA_ARQUITETURA_IA/DOCUMENTACAO_ARQUITETURAL_COMPLETA.md).
<!-- graphify-deep-v2:end -->
