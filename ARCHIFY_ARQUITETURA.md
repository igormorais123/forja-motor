# Archify — arquitetura de Fábrica de melhoria de petições

> Gerado em 2026-07-30T02:36:14-03:00. Documento complementar aos mapas canônicos existentes. A autoridade factual continua nos arquivos-fonte e nas instruções locais.

## Resultado executivo

Mapear a fábrica como sistema: entrada de demandas, gestão, navegação IA, fontes normativas, FORJA, visual law, QA, entrega e aprendizagem.

O diagrama interativo está em [`FABRICA_PETICOES_ARCHITECTURE.html`](00_MAPA_ARQUITETURA_IA/FABRICA_PETICOES_ARCHITECTURE.html) e seu modelo verificável em [`FABRICA_PETICOES_ARCHITECTURE.architecture.json`](00_MAPA_ARQUITETURA_IA/FABRICA_PETICOES_ARCHITECTURE.architecture.json). Ele usa o preset `blueprint`, perfil `showcase`, movimento desativado e três percursos guiados.

## O que este mapa responde

- Onde uma pessoa ou IA deve entrar.
- Quais camadas têm autoridade, quais apenas apoiam e quais são saídas.
- Como dados, fontes, decisões de produção, gates e entregas se conectam.
- Onde existem fronteiras de privacidade, proveniência e estado vivo.
- Qual sequência reduz alucinação, duplicação e leitura indiscriminada.

## Entradas canônicas

- `AGENTS.md`
- `MAPA_IA.md`
- `00_IA_NAVIGACAO/PROTOCOLO_NAVEGACAO_IA.md`
- `gestao_escritorio/README.md`
- `_FORJA_HARNESS/README.md`

## Camadas arquiteturais

| Camada | Responsabilidade |
| --- | --- |
| Entrada e gestão | demandas, conectores e quadro operacional com evidência separada |
| Navegação | MAPA_IA e inventário para reduzir varredura indiscriminada |
| Conhecimento | leis gerais, modelos aprovados, fontes oficiais e ferramentas |
| Produção | casos e esteira FORJA com contratos por fase |
| Visual law | kits Medina, Word COM, PDF e renderização |
| Qualidade e entrega | gates factuais, jurídicos, editoriais, visuais e evidência de envio |
| Aprendizagem | feedback humano, diffs e atualização dos protocolos |

## Fluxo principal

1. Demanda entra por canal autorizado e é registrada no quadro operacional.
2. Navegação localiza o caso sem expor conversas brutas ao contexto geral.
3. Fontes, leis e modelos alimentam a FORJA ou o fluxo manual controlado.
4. Gates impedem promoção com lacunas materiais.
5. Visual law materializa a versão aprovada e QA inspeciona a saída real.
6. Entrega comprovada fecha a fronteira operacional e alimenta aprendizagem.

## Fronteiras e confiança

- Painel de demandas não é prova jurídica.
- Conversas, credenciais e anexos não entram no grafo arquitetural.
- Backups ficam locais; publicação GitHub é restrita ao escopo explicitamente autorizado.

## Riscos arquiteturais

| ID | Risco | Controle |
| --- | --- | --- |
| R01 | Confundir respondido, produzido, enviado e concluído. | Mitigar pela rota de leitura, gates e regeneração do mapa |
| R02 | Usar mapa antigo após criação de novas fases ou contratos. | Mitigar pela rota de leitura, gates e regeneração do mapa |
| R03 | Misturar proveniência interna com linguagem protocolável. | Mitigar pela rota de leitura, gates e regeneração do mapa |
| R04 | Declarar qualidade visual sem renderização e inspeção. | Mitigar pela rota de leitura, gates e regeneração do mapa |

## Inventário observado

- Diretórios mapeados: **837**.
- Arquivos visíveis contados na profundidade expandida: **4771**.
- Arquivos marcadores de navegação: **337**.
- Binários/sensíveis apenas contados, nunca lidos: **1539**.
- Profundidade máxima: **3**.
- Subárvores podadas: **532**.

## Pastas de primeiro nível

| Pasta | Papel inferido pelo nome | Expandida no inventário |
| --- | --- | --- |
| .agents | configuração | sim |
| .autoresearch | configuração | sim |
| .claude | configuração | sim |
| .codex | configuração | sim |
| .git | configuração | não |
| .planning | configuração | sim |
| .playwright-cli | configuração | sim |
| .playwright-mcp | configuração | sim |
| .pytest_cache | configuração | não |
| .ruff_cache | configuração | não |
| 00_IA_NAVIGACAO | domínio/projeto | sim |
| 00_MAPA_ARQUITETURA_IA | documentação/planejamento | não |
| _ferramentas | domínio/projeto | sim |
| _FORJA_HARNESS | domínio/projeto | sim |
| _LABORATÓRIO_MIROFISH — Vale Trading (EXPERIMENTAL — NÃO É PROVA) | domínio/projeto | sim |
| _LEIS_GERAIS | domínio/projeto | sim |
| _MODELOS | domínio/projeto | sim |
| _ocr_estre_complemento_2026-07-29 | domínio/projeto | sim |
| _ocr_estre_erm_2026-07-29 | domínio/projeto | sim |
| AI 0011621-15.2023.8.27.2700 – ajustes finais nos memoriais | domínio/projeto | sim |
| Amplify Legal500 - análise preliminar 2026-07-19 | domínio/projeto | sim |
| Análise de caso pessoal Fábio Medina Osório - Plano de Saúde | domínio/projeto | sim |
| Apresenta esclarecimentos e solicita documentos | documentação/planejamento | sim |
| Apresenta parecer que foi encaminhado ao cliente Natura | domínio/projeto | sim |
| Apresentação PPT Miami Fabio | domínio/projeto | sim |
| Assunto Laudo Pericial Contábil – Atualização de Valores – Proc. 0003453-28.1997.4.01.3400 | domínio/projeto | sim |
| Azimut — correção do objeto do REsp nº 2.237.713 SP | domínio/projeto | sim |
| Azimut — revisão da minuta e dos precedentes do REsp 2.237.713 SP | domínio/projeto | sim |
| Cafelana | domínio/projeto | sim |
| Cafelana - Complementações e Ajustes - AgInt no AREsp nº 2.698.443 DF | domínio/projeto | sim |
| Cafelana — rastreamento integral dos processos relacionados ao RE nº 1.395.147 PR | domínio/projeto | sim |
| Conteudo_Redes_Celina_Leao_VEJA_2026-07-17 | domínio/projeto | sim |
| Contrarrazões ao agravo interno da União — histórico processual, intempestividade do recurso originário e auto | domínio/projeto | sim |
| Contrato social de Brasília para assinatura | domínio/projeto | sim |
| CORSAN AGERST - Proposta de Serviços Jurídicos | domínio/projeto | sim |
| Dados para elaboração de contrato de confidencialidade | domínio/projeto | sim |
| docs | documentação/planejamento | sim |
| Embargos AgInt AREsp 1883361 RS - Jorge Haroldo | domínio/projeto | sim |
| ENTREGA_TRF_MEDINA_NATURA_2026-07-16 | domínio/projeto | sim |
| ESTRITAMENTE CONFIDENCIAL Contrato de honorários — parecer Natura Cabreúva | domínio/projeto | sim |
| ESTRITAMENTE CONFIDENCIAL Natura–Cabreúva — minuta de parecer, prazo da réplica e próximos passos | domínio/projeto | sim |
| Fwd Ação de Improbidade Administrativa 1001278-83 - Ricardo Salles | domínio/projeto | sim |
| Fwd Comprovantes de pagamento SulAmérica - jul 25 a jul 26 | domínio/projeto | sim |
| Fwd Concluído Assinatura dos documentos da proposta 6003224-1 | documentação/planejamento | sim |
| Fwd Consulta técnico-pericial – Vale Trading S A para validação | domínio/projeto | sim |
| Fwd Elaboração de Embargos de Declaração - JFRJ 5002950-05.2026.4.02.5104 — Nylton Simões — prazo interno 21 0 | domínio/projeto | sim |
| Fwd Legal 500 & Medina Osório Advogados Próximos passos | domínio/projeto | sim |
| Fwd Re Solicita informações | domínio/projeto | sim |
| Fwd Relatório Azimut | domínio/projeto | sim |
| gestao_escritorio | domínio/projeto | sim |
| git-tools | domínio/projeto | sim |
| graphify-out | domínio/projeto | não |
| Jalusa Prestes Abaide - Proc. 5000447-02.2011.4.04.7102 | domínio/projeto | sim |
| Material para elaboração de parecer - interessado Deltan Dallagnol | domínio/projeto | sim |
| Memoriais AgInt AREsp 2578181 SC - LIBRA SUL | domínio/projeto | sim |
| Memoriais Apelação Patrícia e Fábio - Proc. 0014560-09.2014.8.19.0209 | domínio/projeto | sim |
| Memoriais Cautelar Fiscal | domínio/projeto | sim |
| Minuta de Embargos de Declaração — José Eduardo Siqueira Campos | domínio/projeto | sim |
| Natura Cabreúva - Parecer e Quesitos - prazo 20-07-2026 | domínio/projeto | sim |
| Natura Cabreúva — diretrizes para conclusão do parecer | domínio/projeto | sim |
| Natura Cabreúva — fases autônomas, complementação do parecer e novos produtos | domínio/projeto | sim |
| Natura Cabreúva — matriz contábil e prova do requerimento de 2021 | domínio/projeto | sim |
| Natura Cabreúva — versão preliminar, linha hermenêutica e escolhas de fundamentação | domínio/projeto | sim |
| Nova pasta | domínio/projeto | sim |
| output | estado/dados | sim |
| PRAZO 03 08 - Elaboração de memoriais – ED no AI nº 5004633-36.2026.4.02.0000 - ERM OSV CONSTRUCAO NAVAL X TRA | domínio/projeto | sim |
| PRAZO 03 8 - Elaboração de memoriais – ED no AI nº 5004634-21.2026.4.03.0000 - ESTRE AMBIENTAL X TRANSPETRO | domínio/projeto | sim |
| prazo 30 07 - Elaboração de memoriais – EDs no AI nº 5006962-48.2026.4.02.0000 RJ | domínio/projeto | sim |
| PRAZO 31 07 - MEMORIAIS - JULGAMENTO DO AI N 0011621-15.2023.8.27.2700 - JESC - PROCESSO ESTRATÉGICO | domínio/projeto | sim |
| Re Ajustes implementados — Azimut, SulAmérica, Cafelana, Natura e Roraima | domínio/projeto | sim |
| Re Documentação da Natura – acesso à pasta | documentação/planejamento | sim |
| Re Elaboração das contrarrazões ao AgInt no AREsp nº 2.698.443 DF | domínio/projeto | sim |
| Re Relatório Azimut | domínio/projeto | sim |
| Re Roraima Senador Chico Rodrigues — dossiê interno para decisão | domínio/projeto | sim |
| Relatório sobre o Amplify — análise preliminar | domínio/projeto | sim |
| Solicitação de documentos pessoais para entrada no contrato social | documentação/planejamento | sim |
| URGENTE - Medida Cautelar Fiscal n.º 5002486-81.2012.4.04.7216 SC - analise a aperfeiçoamento de Embargos de D | domínio/projeto | sim |
| URGENTE — Medida Cautelar Fiscal — confirmação de entrega da revisão ainda hoje | domínio/projeto | sim |
| WhatsApp - Fabio Medina Osorio - triagem de demandas | domínio/projeto | sim |
| WhatsApp - Igor Hermes - contexto de organizacao | domínio/projeto | sim |
| WhatsApp Audio - Cafelana peça humana e prevenção - 2026-07-08 | domínio/projeto | sim |
| WhatsApp Audio - Protocolo de aprendizados IA - 2026-07-08 | domínio/projeto | sim |
| WhatsApp Audio - Roraima Senador cliente - 2026-07-08 | domínio/projeto | sim |

## Ordem recomendada para IAs

1. `AGENTS.md`
2. `MAPA_IA.md`
3. `ARCHIFY_ARQUITETURA.md`
4. `GRAPHIFY_GRAFO.md`
5. `mapa do caso ou subsistema`

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

A análise completa, ADRs, cenários, falhas e confiança estão em [`DOCUMENTACAO_ARQUITETURAL_COMPLETA.md`](00_MAPA_ARQUITETURA_IA/DOCUMENTACAO_ARQUITETURAL_COMPLETA.md). Veja também o [fluxo operacional](00_MAPA_ARQUITETURA_IA/FABRICA_PETICOES_OPERATIONAL_FLOW.html) e o [fluxo de confiança](00_MAPA_ARQUITETURA_IA/FABRICA_PETICOES_TRUST_DATAFLOW.html).
<!-- archify-deep-v2:end -->
