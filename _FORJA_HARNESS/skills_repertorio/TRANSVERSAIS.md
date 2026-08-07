# Transversais — skills que servem à esteira, não a uma fase

> Cardápio, não contrato. Estas skills não pertencem a nenhuma fase: elas atuam sobre a
> própria FORJA, sobre a sessão de trabalho ou sobre casos em que o agente precisa de
> um recurso que qualquer fase pode demandar.

## Quando abrir este documento

| Situação | Skill |
|---|---|
| Vou propor mudança de método, gate ou pipeline | `forja-adr` |
| Vou acionar qualquer revisor independente | `forja-briefing-revisor` |
| Vou passar o caso para outra sessão ou agente | `forja-handoff-caso` |
| Vou mudar prompt ou template e chamar isso de melhoria | `autoresearch` |
| Quero auditar a esteira como sistema | `harness-engineering` |
| Um gate aprovou o que não devia | `anti-trapaca-evaluator` |
| Uma skill deste repertório precisa mudar | `skill-creator` |
| Preciso de imagem institucional, fora da peça | `ai-image-generation` |

---

## Fichas

### `forja-adr` — projeto

- **Faz:** registra e consulta decisões de arquitetura e método da fábrica em fichas curtas e numeradas, **inclusive as rejeitadas**.
- **Entra em:** F0, F2, F4, F7 e F10 — qualquer ponto onde se decide como a fábrica trabalha.
- **Para quê:** impedir que a rodada seja gasta reabrindo o que já foi decidido. Há decisão rejeitada com nome e motivo: integrar `compor()` dentro do render, RAG e GraphRAG, governança de confidencialidade por IA, LLM como juiz, RCT interno, firewall de saída dedicado, visualização 3D.
- **Ganho:** o conselho de 03/08 recomendou arquitetura já rejeitada, citando função inexistente. Consultar antes custa minutos.
- **Trade-off:** nenhum. **Consulte sempre antes de propor.**
- **Diferencial:** ADR registra decisão da fábrica; decisão sobre uma peça específica fica no relatório de melhorias do caso.
- **Marcadores:** contexto `baixo` · dependência `nenhuma` · fabricação `nulo` · reversibilidade `parcial` · confere depois: revisão humana da ficha.

### `forja-briefing-revisor` — projeto

- **Faz:** monta o briefing do revisor independente de modo que ele não receba pronta a conclusão de quem construiu.
- **Entra em:** F4 (conselho), F7 (red team e revisão cruzada), e qualquer segunda opinião sobre gate ou arquitetura.
- **Para quê:** quebrar a circularidade de autovalidação — quem constrói escreve o gate, mede com ele e se aprova.
- **Ganho:** é a diferença entre parecer independente e eco caro.
- **Trade-off:** nenhum. Custa minutos.
- **Diferencial:** rege a **montagem** do briefing; o `forja_conselho.py` valida o parecer depois de pronto. São coisas diferentes e ambas necessárias.
- **Marcadores:** contexto `baixo` · dependência `nenhuma` · fabricação `nulo` · reversibilidade `total` · confere depois: `forja_conselho.py`.

### `forja-handoff-caso` — projeto

- **Faz:** monta o pacote de continuidade do caso entre sessões e entre agentes.
- **Entra em:** F0 e o fim de qualquer sessão longa.
- **Para quê:** herdar decisão em vez de redescobrir. Contexto longo é resumido pelo harness; o que precisa sobreviver precisa estar em arquivo.
- **Trade-off:** nenhum.
- **Marcadores:** contexto `baixo` · dependência `nenhuma` · fabricação `nulo` · reversibilidade `parcial` · confere depois: `mapping_valid` na retomada.

### `autoresearch` — Claude

- **Faz:** loop de otimização com variantes, avaliação e seleção, para artefato mensurável.
- **Entra em:** F10 e qualquer proposta de mudar prompt, template ou protocolo de fase.
- **Para quê:** a regra da casa é que mudança apresentada como melhoria passa pelo ciclo AR: execução pareada, julgamento cego com swap, duas famílias de juiz, canários de falha única, gate de promoção em três estados com recibo Ed25519.
- **Trade-off:** enquanto não houver sealed prospectivo consumível, o subsistema opera em `estudo_descritivo` e nenhuma variante vai a produção. Os segredos do ciclo vivem em `%USERPROFILE%\.forja_ar_secrets\` e jamais entram em repositório ou prompt.
- **Não use quando:** o que se está fazendo é corrigir defeito. Defeito se conserta e se testa; melhoria se mede.
- **Marcadores:** contexto `alto` · dependência `nenhuma` · fabricação `alto` · reversibilidade `parcial` · confere depois: gate de promoção do ciclo AR.

### `harness-engineering` — Claude

- **Faz:** disciplina de orquestração de agentes: contrato de tarefa, estado em arquivos, verificação alinhada, traces brutos, poda de complexidade.
- **Entra em:** F10 e revisões de arquitetura.
- **Para quê:** perguntar por que o gate não pegou, em vez de só corrigir o que ele não pegou.
- **Trade-off:** cara e abstrata. Aplicada a caso individual, produz diagnóstico genérico.
- **Marcadores:** contexto `alto` · dependência `nenhuma` · fabricação `alto` · reversibilidade `total` · confere depois: ADR e regressão.

### `anti-trapaca-evaluator` — Claude

- **Faz:** template de avaliador resistente a keyword-stuffing, hedge, citação alucinada e peso morto.
- **Entra em:** F7 e F10, sempre que um gate aprova o que não devia.
- **Para quê:** a casa tem gates que já mentiram conforme o comando — laudo declarado, lastro sem `--base-dir`, régua de prosa em DOCX composto, gate curto com critério mais fraco que a sincronização completa.
- **Ganho:** conserta a causa. A peça corrigida sem o gate corrigido garante repetição.
- **Trade-off:** é trabalho de harness. Não misture com a entrega do caso; registre como ADR.
- **Marcadores:** contexto `médio` · dependência `nenhuma` · fabricação `baixo` · reversibilidade `parcial` · confere depois: teste de regressão nomeando o caso que passou indevidamente.

### `skill-creator` — Claude

- **Faz:** cria, edita, mede e calibra a descrição de skills para disparo correto.
- **Entra em:** manutenção deste repertório.
- **Para quê:** skill que não dispara na hora certa é skill que não existe. A descrição é o que decide o disparo.
- **Trade-off:** alterar skill é alterar produção sem teste automático. Exija caso real de contraprova.
- **Marcadores:** contexto `médio` · dependência `nenhuma` · fabricação `alto` · reversibilidade `parcial` · confere depois: caso real.

### `ai-image-generation` — Claude

- **Faz:** gera imagem por modelos de difusão.
- **Entra em:** F8 e F9, exclusivamente em material institucional ou ao cliente.
- **Para quê:** capa de apresentação, ilustração de relatório. **Nunca** retratando fato, pessoa ou prova em peça protocolada — a autorização do protocolo é expressa e limitada.
- **Trade-off:** raster; não passa pelos gates de legibilidade e colisão porque não tem texto em SVG. Diagrama de peça é vetorial por regra.
- **Marcadores:** contexto `médio` · dependência `crédito pago`, `rede` · fabricação `alto` · reversibilidade `parcial` · confere depois: decisão humana sobre uso externo.

---

## O que ficou fora do repertório, e por quê

Registrado para não ser reaberto a cada rodada. Estas foram avaliadas em 06/08/2026
contra as 402 skills instaladas e **rejeitadas com motivo**:

| Família | Exemplos | Motivo |
|---|---|---|
| Diagramação genérica | `paperbanana-diagramas`, `visual-thinking`, `visual-law-inteia`, `dataviz`, `data-visualization`, `archify` | Produzem figura fora da identidade Medina Osório e sem os gates de legibilidade, overflow e colisão do `medina_svg_kit.py`. `archify` ainda serve para documentar o harness, mas não gera EMF e não entra em peça. |
| Navegador redundante | `browse`, `gstack`, `playwright-cli`, `browser-harness`, `dogfood` | Quatro rotas para a mesma coisa. `forja-campo-tribunais` tem o perfil logado que os portais exigem; `fetch-rendered` cobre o resto. |
| Jurídico duplicado | `themis-nomos`, `colmeia-juridico-peticoes`, `osa-themis-juridico`, `ciceromini`, `helenamini` | `cicero` e `advogado-sobrehumano` cobrem com mais profundidade e já são os nomes que o protocolo cita. |
| UI e frontend | `impeccable`, `ui-ux-pro-max`, `interface-design`, `refactoring-ui`, `frontend-design`, `ux-heuristics`, `design-dna`, `omni-figma` | A FORJA entrega Word e PDF. Não há interface. |
| Planejamento paralelo | a família `gsd-*` (cerca de 70 skills) | A FORJA já tem contrato de fase (F0–F10), ADR e fila. Duas máquinas de planejamento produzem gate que ninguém percorre. |
| Segurança de sessão | `careful`, `guard`, `freeze`, `decisions` | Cobertos por `peticao-decisoes-incertas`, `forja-adr` e pelo protocolo de escopo. |
| Coleta e campanha | as 11 skills `apify-*`, eleitorais, Mirante, finanças, mídia, voz e vídeo | Nada disso toca peça. |

**Duas em observação, não adotadas:**

- `proj-analise-juridica-preditiva` (Hermes) — perfil de magistrado e predição de decisão. Alinha-se à Diretriz 28, que persegue quem vai julgar. Entraria como insumo interno de estratégia em F4, jamais como texto protocolável. Não adotada: predição sem lastro é o oposto do que a fábrica exige.
- `archify` — diagrama de arquitetura validado em HTML. Inútil para peça; útil para documentar o próprio harness. Reavaliar se a documentação de arquitetura crescer.
