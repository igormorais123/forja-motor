# Instruções locais para agentes

## Porta de entrada AI-friendly

- Ao iniciar trabalho neste projeto, execute `python forja_axi.py`: a execução
  sem argumentos devolve contexto vivo, agregado e somente de leitura.
- Para navegação operacional, prefira `cases`, `case`, `queue`, `health` e
  `commands`; a saída padrão é TOON e `--json` é a alternativa explícita.
- Antes de mutação, consulte `python forja_axi.py commands <nome>`, confirme o
  estado canônico e use o CLI original. A fachada não promove fase, não entrega,
  não libera juridicamente e não substitui gates humanos.
- A especificação da interface está em `docs/AGENT_INTERFACE.md`; a orientação
  portátil está em `.agents/skills/forja/SKILL.md`.

<!-- architecture-map-protocol:start -->
## Protocolo Archify + Graphify

- Antes de responder sobre arquitetura, dependências, organização ou localização, leia `00_MAPA_ARQUITETURA_IA/LEIA_PRIMEIRO.md` e `00_MAPA_ARQUITETURA_IA/DOCUMENTACAO_ARQUITETURAL_COMPLETA.md`.
- Use o diagrama de componentes `00_MAPA_ARQUITETURA_IA/FORJA_HARNESS_ARCHITECTURE.html`, o fluxo operacional `00_MAPA_ARQUITETURA_IA/FORJA_HARNESS_OPERATIONAL_FLOW.html` e o fluxo de confiança `00_MAPA_ARQUITETURA_IA/FORJA_HARNESS_TRUST_DATAFLOW.html` conforme a pergunta.
- Consulte `00_MAPA_ARQUITETURA_IA/graphify-out/graph.json`/`graph.html` antes de varrer a pasta. O grafo diferencia estrutura extraída de decisões, cenários, falhas e fronteiras curadas.
- Relação `CURATED` ou `INFERRED` orienta navegação; confirme-a no contrato/arquivo local antes de mudança material. Estado vivo sempre exige verificação atual.
- Depois de mudança estrutural relevante, execute `C:\Users\IgorPC\.claude\projects\00_MAPA_ARQUITETURA_IA\REGENERAR_MAPAS_ARQUITETURA.py` e `C:\Users\IgorPC\.claude\projects\00_MAPA_ARQUITETURA_IA\APROFUNDAR_MAPAS_ARQUITETURA.py`, renderize e valide todos os HTMLs, consulte o grafo e atualize hashes.
- Em raízes jurídicas, não execute extração semântica crua sobre autos, mensagens, anexos, bancos, estado, telemetria ou credenciais. O mapa oficial é sanitizado e metadata-only.
- Estes artefatos complementam mapas canônicos; não substituem `MAPA.md`, `MAPA_IA.md`, `ESTADO_ATUAL.md`, manifestos, schemas ou documentação técnica local.
<!-- architecture-map-protocol:end -->

<!-- architecture-map-interfaces-v3:start -->
## Protocolo de interfaces inferiores

- Antes de alterar API interna, CLI, AXI, schema ou runner, leia `00_MAPA_ARQUITETURA_IA/INTERFACES_INFERIORES.md` e consulte `00_MAPA_ARQUITETURA_IA/graphify-out/graph.json`.
- Confirme arestas `AMBIGUOUS` no código; não trate resolução por nome como binding comprovado.
- Depois de mudança de contrato, regenere a camada v3, valide consumidores e execute os testes do subsistema.
<!-- architecture-map-interfaces-v3:end -->

<!-- strategy-v4:start -->
## Protocolo de decisão arquitetural

- Antes de refatorar, leia `00_MAPA_ARQUITETURA_IA/ANALISE_ARQUITETURAL_E_PROPOSTAS.md`.
- Proposta não é implementação concluída. Execute uma onda por vez e cumpra o critério de aceite.
- Preserve fachadas e consumidores durante migração; não execute big-bang.
- Recalcule o Graphify e atualize arquitetura-alvo quando uma proposta mudar de status.
<!-- strategy-v4:end -->

## Descoberta das disciplinas instrumentadas (PRD 45)

| Disciplina | Skill/caminho | Gatilho | Modo | Fonte prevalente |
| --- | --- | --- | --- | --- |
| D1 briefing de conselho | `forja_disciplinas.build_d1_briefing` / `F4_COUNSEL_BRIEFING.json` | antes do despacho F4 | manual assistido | question tree, proposition ledger e fontes hashadas |
| D2 ponte evidencial | `forja_proposition_evidence.py` / `F5_PROPOSITION_EVIDENCE_MAP.json` | cada proposição decisiva em F5 | observe | proposition ledger + source ledger + reconciliação F7 |
| D3 hipóteses de intake | `forja_disciplinas.build_d3_hypotheses` / `F2_INTAKE_HYPOTHESES.json` | depois de F1 com linhas abertas | manual assistido | acervo lido e declaração humana; sempre provisória |
| D4 decisões incertas | `forja_disciplinas.build_d4_uncertain_decisions` / `F7_UNCERTAIN_DECISIONS.json` | antes do fechamento F7 | manual assistido | auditoria F7 e localizador da fonte |
| D5 handoff cruzado | `forja_disciplinas.write_handoff` / `HANDOFF.md` | antes do despacho de revisão | manual | hash do artefato e recibo do revisor |
| D6 fichas de decisão | `forja_disciplinas.write_d6_decision` / `decisoes/` | decisão de arquitetura/processo | manual | decisão nominal, fonte e critério de reabertura |

As disciplinas não são disparadas automaticamente por semelhança semântica. O
classificador de instruções recusado pelo R7 não existe; uma ferramenta futura
pode comparar hashes e diffs, mas não classificar mérito sem nova decisão.

## Padrão configurado de escrita da casa

- Todo e-mail ou mensagem redigido pelo ARCANO/FORJA usa o perfil privado
  resolvido pela chave de acervo `perfil-estilo-casa`. O motor não contém nome,
  corpus, exemplos privados nem identidade do escritório.
- Em F9, `forja_estilo_humano.mandatory_prompt_for_phase()` injeta o perfil de
  e-mail automaticamente. Fora da esteira, carregue
  `mandatory_prompt_for_channel("email"|"mensagem")` antes de redigir.
- Antes de criar rascunho, enviar e-mail ou liberar resposta no pacote, execute
  `forja_estilo_humano.analisar(texto, tipo="email"|"mensagem")`. P0 bloqueia;
  P1 pede ajuste editorial fundamentado.
- O perfil mede método profissional e adequação ao canal. Não prova autoria,
  não autoriza personificação e não permite inventar opinião, fato ou mandato.
