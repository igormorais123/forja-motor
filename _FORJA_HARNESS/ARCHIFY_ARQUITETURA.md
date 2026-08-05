# Archify — arquitetura de FORJA Harness

> Gerado em 2026-08-05T00:22:04-03:00. Documento complementar aos mapas canônicos existentes. A autoridade factual continua nos arquivos-fonte e nas instruções locais.

## Resultado executivo

Representar contratos de fase, artefatos, gates, fontes, renderização, telemetria e entrega da FORJA sem incorporar dados reais de casos ou estado privado.

O diagrama interativo está em [`FORJA_HARNESS_ARCHITECTURE.html`](00_MAPA_ARQUITETURA_IA/FORJA_HARNESS_ARCHITECTURE.html) e seu modelo verificável em [`FORJA_HARNESS_ARCHITECTURE.architecture.json`](00_MAPA_ARQUITETURA_IA/FORJA_HARNESS_ARCHITECTURE.architecture.json). Ele usa o preset `blueprint`, perfil `showcase`, movimento desativado e três percursos guiados.

## O que este mapa responde

- Onde uma pessoa ou IA deve entrar.
- Quais camadas têm autoridade, quais apenas apoiam e quais são saídas.
- Como dados, fontes, decisões de produção, gates e entregas se conectam.
- Onde existem fronteiras de privacidade, proveniência e estado vivo.
- Qual sequência reduz alucinação, duplicação e leitura indiscriminada.

## Entradas canônicas

- `README.md`
- `DOCUMENTACAO_TECNICA.md`
- `FORJA_SPEC_MANIFEST.json`
- `MAPA_IA.md`
- `planejamento/06_GATES_QUALIDADE_FORJA.md`

## Camadas arquiteturais

| Camada | Responsabilidade |
| --- | --- |
| Controle | runner, manifesto, contratos de fase e schemas |
| Intake e exploração | F1 e F2A estruturam corpus e perguntas antes de redigir |
| Pesquisa e conselho | fontes, busca jurídica, Helena e Cícero |
| Produção | blueprint, redação auditável e revisão editorial fiel |
| Verificação | citações, injeção, consistência factual, anti-IA e gates P0/P1 |
| Materialização | visual law, DOCX/PDF, fidelidade e QA por página |
| Estado e observabilidade | state, reports e telemetria separados do código |
| Entrega | pacote interno com evidência de conclusão da fábrica |
| Pós-protocolo | retorno humano, prova de protocolo, comparação exata e histórico por contentKey |
| Aprendizado | candidatos revisados, regras promovidas por fixture e gate prospectivo |
| Evolução arquitetural | candidatas isoladas, shadow, canário, revisão independente e rollback |

## Fluxo principal

1. F1 ingere e classifica fontes; conteúdo é dado, nunca instrução.
2. F2A formula 100 perguntas e mantém lacunas bloqueadas.
3. Pesquisa e conselho produzem insumos registrados.
4. Blueprint antecede redação e limita escopo.
5. F7 audita fatos/citações e F7-B altera apenas forma sob gate de fidelidade.
6. F8 materializa e inspeciona todas as páginas.
7. Pacote/entrega preserva manifestos, hashes e reason codes.
8. Retorno humano elegível abre ramo pós-protocolo sem reabrir a entrega.
9. Comparação usa a versão exata entregue e preserva histórico por contentKey.
10. Regra promovida retorna ao blueprint somente após decisão, fixture e teste prospectivo.
11. Candidata arquitetural roda isolada e permanece no teto estudo_descritivo.

## Fronteiras e confiança

- state, telemetria, cache e renders reais são zonas privadas e não entram no corpus semântico.
- O grafo lista módulos e contratos; não registra alegações, clientes, mensagens ou credenciais.
- Backups permanecem locais; publicação externa não é autorizada por este mapa.

## Riscos arquiteturais

| ID | Risco | Controle |
| --- | --- | --- |
| R01 | Arquivo de estado ou telemetria ser confundido com código canônico. | Mitigar pela rota de leitura, gates e regeneração do mapa |
| R02 | Fase promover artefato sem contrato, hash ou reason code correspondente. | Mitigar pela rota de leitura, gates e regeneração do mapa |
| R03 | Revisor editorial alterar substância jurídica. | Mitigar pela rota de leitura, gates e regeneração do mapa |
| R04 | Mapa gerado ficar desatualizado após mudança em contratos/manifesto. | Mitigar pela rota de leitura, gates e regeneração do mapa |
| R05 | Retorno humano ser nomeado como protocolado sem elo verificável de arquivo. | Mitigar pela rota de leitura, gates e regeneração do mapa |
| R06 | Lição promovida não ser aplicada na próxima peça compatível. | Mitigar pela rota de leitura, gates e regeneração do mapa |
| R07 | Candidata arquitetural alterar produção sem decisão externa ao AR. | Mitigar pela rota de leitura, gates e regeneração do mapa |

## Inventário observado

- Diretórios mapeados: **622**.
- Arquivos visíveis contados na profundidade expandida: **8447**.
- Arquivos marcadores de navegação: **547**.
- Binários/sensíveis apenas contados, nunca lidos: **745**.
- Profundidade máxima: **6**.
- Subárvores podadas: **84**.

## Pastas de primeiro nível

| Pasta | Papel inferido pelo nome | Expandida no inventário |
| --- | --- | --- |
| .agents | configuração | sim |
| .claude | configuração | sim |
| .codex | configuração | sim |
| .git | configuração | não |
| .planning | configuração | sim |
| .playwright-mcp | configuração | sim |
| .pytest_cache | configuração | não |
| .ruff_cache | configuração | não |
| 00_MAPA_ARQUITETURA_IA | documentação/planejamento | não |
| __pycache__ | domínio/projeto | não |
| _scripts_oneoff | código/contrato | sim |
| ar_architecture | domínio/projeto | sim |
| autoresearch | domínio/projeto | sim |
| bancada_cafelana_v7 | domínio/projeto | sim |
| blender_atlas | domínio/projeto | sim |
| cache | estado/dados | sim |
| contracts | código/contrato | sim |
| docs | documentação/planejamento | sim |
| FORJA | código/contrato | sim |
| graphify-out | domínio/projeto | não |
| learning_registry | domínio/projeto | sim |
| n4_fixtures | domínio/projeto | sim |
| n4_schemas | domínio/projeto | sim |
| PETICAO_ACORDO_DOUTORADO_FORJA_20260715 | domínio/projeto | sim |
| PETICAO_ENDERECO_EXEQUIBILIDADE_FORJA_20260715 | domínio/projeto | sim |
| phase_contracts | domínio/projeto | sim |
| phase_contracts_n4 | domínio/projeto | sim |
| planejamento | documentação/planejamento | sim |
| private | domínio/projeto | sim |
| pso_schemas | domínio/projeto | sim |
| reports | qualidade/saída | sim |
| state | estado/dados | sim |
| telemetria | estado/dados | sim |
| templates | código/contrato | sim |
| youtube-transcript | código/contrato | sim |

## Ordem recomendada para IAs

1. `README.md`
2. `FORJA_SPEC_MANIFEST.json`
3. `MAPA_IA.md`
4. `ARCHIFY_ARQUITETURA.md`
5. `GRAPHIFY_GRAFO.md`
6. `contrato da fase relevante`

## Protocolo de manutenção

1. Mudança estrutural relevante exige regenerar este pacote.
2. Não editar o HTML Archify diretamente; editar o JSON e renderizar novamente.
3. Não executar Graphify sem exclusões sobre casos, mensagens, bancos ou anexos.
4. Validar o Archify em perfil `showcase` e executar `check` no HTML.
5. Verificar número de nós/arestas e consulta de fumaça no Graphify.
6. Atualizar o mapa canônico preexistente quando suas regras locais exigirem.
7. Registrar data, cobertura, exclusões e limitações em toda regeneração.

## Limites

Este documento é arquitetura operacional. Não prova fatos jurídicos, estado de serviços externos, conclusão de demandas, vigência normativa nem conteúdo de arquivos privados. Relações semânticas curadas são acompanhadas de evidência no grafo; agrupamentos pelo nome de pasta são marcados como inferência.

<!-- archify-deep-v2:start -->
## Aprofundamento arquitetural v2

A análise completa, ADRs, cenários, falhas e confiança estão em [`DOCUMENTACAO_ARQUITETURAL_COMPLETA.md`](00_MAPA_ARQUITETURA_IA/DOCUMENTACAO_ARQUITETURAL_COMPLETA.md). Veja também o [fluxo operacional](00_MAPA_ARQUITETURA_IA/FORJA_HARNESS_OPERATIONAL_FLOW.html) e o [fluxo de confiança](00_MAPA_ARQUITETURA_IA/FORJA_HARNESS_TRUST_DATAFLOW.html).
<!-- archify-deep-v2:end -->

<!-- archify-interfaces-v3:start -->
## Interfaces inferiores v3

Sequência Archify: [`FORJA_HARNESS_INTERFACE_CALLS.html`](00_MAPA_ARQUITETURA_IA/FORJA_HARNESS_INTERFACE_CALLS.html). Matriz completa: [`INTERFACES_INFERIORES.md`](00_MAPA_ARQUITETURA_IA/INTERFACES_INFERIORES.md).
<!-- archify-interfaces-v3:end -->

<!-- strategy-v4:start -->
## Arquitetura-alvo e roadmap v4

- [Diagnóstico e propostas](00_MAPA_ARQUITETURA_IA/ANALISE_ARQUITETURAL_E_PROPOSTAS.md)
- [Arquitetura-alvo](00_MAPA_ARQUITETURA_IA/FORJA_HARNESS_TARGET_ARCHITECTURE.html)
- [Roadmap](00_MAPA_ARQUITETURA_IA/FORJA_HARNESS_IMPROVEMENT_ROADMAP.html)
<!-- strategy-v4:end -->
