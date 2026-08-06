# PRD — Disciplinas de processo importadas (skills da fábrica)

**Versão:** 1.0
**Protocolo:** `FORJA-SKILLS-PROCESSO-v1`
**Data:** 05/08/2026
**Estado:** especificação para execução; skills escritas, ligação à esteira não implementada
**Plano de origem:** `planejamento/43_PLANO_SKILLS_IMPORTADAS_ONDREJ.md` (revisado nesta data)
**Fonte externa:** `davidondrej/skills`, commit `04bd15abae135f5744e3dc825a4ab9c75d61fbfc`

## 1. Decisão de produto

Instalar na fábrica seis **disciplinas de processo** — briefing de revisor cego,
briefing de pesquisa com barra de conclusão, triagem de escolhas consequentes,
declaração de decisões incertas, handoff de caso e registro de decisões com
rejeição — e ligá-las aos pontos da esteira onde as falhas que elas fecham
foram medidas.

O produto não é seis arquivos SKILL.md: é a garantia de que cada disciplina
**acontece no ponto certo mesmo quando ninguém lembra dela**. Skill que depende
de alguém invocar é o recurso que "parou em 10/07 sem ninguém notar" (lição 87).
Por isso o desenho tem duas camadas:

1. **Camada interativa** — as skills em `.claude/skills/` da fábrica, para
   sessões humanas de Claude Code (e o conteúdo espelhado onde o Codex leia).
2. **Camada de esteira** — a mesma disciplina embutida em contrato de fase,
   prompt de workflow ou artefato exigido, porque `forja_headless.py` e os
   crons **não carregam skill de Claude Code**. Disciplina que só existe na
   camada 1 não existe para a produção automática.

## 2. Problema

Quatro falhas medidas e registradas, nenhuma coberta por gate existente:

1. **Circularidade de revisão** (lição 87-99): o conselho leu o dossiê do
   construtor, recomendou arquitetura já rejeitada e citou função inexistente.
   `forja_conselho.py` valida o parecer *pronto*; nada rege a montagem do
   briefing — conferido no código em 05/08.
2. **Atribuição errada de jurisprudência** (erro recorrente nº 1 das entregas
   reais): a pesquisa para no primeiro resultado plausível e entrega achado sem
   identificação completa, verbatim ou situação de vigência.
3. **Gate de presença não detecta pobreza** (diagnóstico F2A de 05/08): 100
   perguntas com um único valor de `unansweredConsequence`. Os gates
   determinísticos medem forma; a degradação é de substância.
4. **Conhecimento preso à sessão**: rejeições arquiteturais vivem em prosa
   espalhada; a revisão cruzada entre famílias recebe o caso sem estado
   compilado e gasta a rodada reconstruindo em vez de revisando.

## 3. Hipótese

Se as seis disciplinas rodarem nos pontos definidos na § 6, então:

- nenhuma pauta de conselho volta a conter conclusão pré-pronta do construtor
  nem proposta já rejeitada sem fato novo;
- todo achado jurisprudencial chega à redação com os seis campos que fecham os
  seis modos de falha de citação;
- o bloco "Pontos que exigem o seu olho" (U11) deixa de ser genérico, porque
  passa a nascer de uma lista de hesitações reais com página e alternativa
  descartada;
- a rodada de revisão cruzada começa do estado, não do zero.

Falsificável: cada consequência tem métrica na § 8. Se após 10 casos as
métricas não moverem, as disciplinas são formalismo e devem ser removidas —
remoção registrada em ficha `forja-adr`.

## 4. O risco número um: as disciplinas virarem formulário

É a mesma família da degradação do F2A, e seria irônico importar a cura e
reproduzir a doença. Mitigação de desenho, obrigatória em toda ligação da § 6:

- **Âncora concreta obrigatória.** Item de `peticao-decisoes-incertas` sem
  página/parágrafo e sem alternativa descartada não conta. Achado de pesquisa
  sem verbatim não conta. Handoff sem a seção "armadilhas" preenchida com o que
  falhou *nesta sessão* não conta.
- **Vazio exige justificativa, não passa em branco.** Lista de decisões
  incertas vazia em peça longa demanda justificativa escrita — o padrão medido
  da casa é que nenhuma v1 saiu protocolável.
- **Diversidade como sinal.** Quando houver medição (onda 3), o sinal é o mesmo
  do diagnóstico F2A: variedade dos campos entre itens. Seis hesitações com a
  mesma consequência declarada são um campo copiado seis vezes.
- **Nenhum elo vira bloqueante sem calibração** (regra da casa, como em todo
  gate): ondas 1-2 são disciplina observada; só a onda 3 decide bloqueio, com
  limiar calibrado nos casos reais das ondas anteriores.

## 5. Escopo e não-escopo

**Escopo:** as seis skills (feitas), migração inicial do registro de decisões,
ligação aos pontos da esteira, espelhamento para o Codex, registro de
`stop_reason` no editorial, métricas de adoção.

**Não-escopo:** resolver o F2A v2 (as disciplinas são contraparte, não
substituto do gate de diversidade de campo); reconciliar CLAUDE.md × AGENTS.md
(instrumento proposto em R8, decisão separada); qualquer mudança em gate visual,
citações ou render; instalação global de skill.

## 6. Requisitos

Cada requisito tem critério de aceite conferível. "Feito" sem o critério não é
feito.

**R1 — Registro de decisões operante.**
Criar `_FORJA_HARNESS/decisoes/` e migrar as 13 decisões da tabela da skill
`forja-adr`, cada uma com status, evidência e critério de reabertura.
*Aceite:* 13 fichas numeradas; toda ficha `Rejeitada` nomeia a falha ou o
documento de origem; `INDICE_FORJA.md` aponta a pasta.

**R2 — Pauta de conselho passa pelo briefing cego.**
O prompt/roteiro que monta F4 (Helena, Cícero, Diabob e red team) incorpora o
esqueleto e o checklist anti-contaminação de `forja-briefing-revisor`, incluindo
a seção "já decidido/já rejeitado" alimentada por R1.
*Aceite:* nos 3 primeiros casos após a mudança, o artefato de pauta arquivado
no caso contém as três perguntas obrigatórias e a lista de rejeitados; um
revisor consegue apontar, no arquivo, qual fonte primária recebeu.

**R3 — Pesquisa F3 nasce de briefing com barra de conclusão.**
Todo levantamento jurisprudencial gera antes um parágrafo no formato de
`forja-briefing-pesquisa`, arquivado em `state/<caseId>/`; os seis campos por
achado alimentam a tabela de lastro (U6).
*Aceite:* em caso novo, existe `F3_BRIEFING_PESQUISA.md` anterior ao primeiro
achado; nenhuma proposição decisiva entra na tabela de lastro sem os seis
campos.

**R4 — Triagem de escolhas na entrada.**
`peticao-tres-escolhas` roda no primeiro contato com demanda nova; as
respostas do humano viram entrada declarada da F2A.
*Aceite:* o `F2_QUESTION_TREE.json` (ou artefato de F2A vigente) faz referência
às escolhas triadas; a escolha rejeitada aparece com motivo.

**R5 — Decisões incertas antes de fechar F7.**
`peticao-decisoes-incertas` roda antes da entrega; a saída alimenta o bloco
"Pontos que exigem o seu olho" com página por item.
*Aceite:* nos 3 primeiros casos, o bloco do e-mail de entrega é rastreável
item a item à lista interna; lista vazia vem com justificativa escrita.

**R6 — Handoff em toda troca de contexto de caso.**
`forja-handoff-caso` grava `state/<caseId>/HANDOFF.md` ao encerrar sessão de
trabalho e **obrigatoriamente** antes de despachar revisão cruzada entre
famílias; o briefing do revisor aponta para ele.
*Aceite:* próxima revisão cruzada real parte de um HANDOFF.md existente; o
revisor não pergunta identidade processual básica.

**R7 — `stop_reason` no editorial.**
`forja_editorial.py` passa a gravar o `stop_reason` do envelope no
`editor_usage` (o bloqueio de modelo efetivo **já existe** — `_actual_model`,
linhas 98-104 e 399-404; conferido em 05/08). Mudança pequena, diagnóstica,
não bloqueante: recusa hoje reprova por fidelidade sem dizer o motivo real.
*Aceite:* `editor_usage` de um run novo contém o campo; teste cobre o caso de
campo ausente no envelope (grava `null`, não quebra).

**R8 — Instrumento de divergência de instruções (proposta, não compromisso).**
`forja_divergencia_instrucoes.py` recomputa a divergência CLAUDE.md × AGENTS.md
e classifica cada trecho em núcleo comum / específico-Codex / específico-Claude.
*Aceite:* decisão registrada em ficha R1 — construir ou rejeitar com motivo.

**R9 — Espelhamento para o Codex.**
O Codex não lê `.claude/skills/`. As disciplinas que o Codex executa (R2, R3,
R6, quando o produtor for da família GPT) entram como seção do `AGENTS.md` da
fábrica ou como referência apontada por ele — decisão consciente, dado que os
dois documentos divergem por desenho.
*Aceite:* `AGENTS.md` aponta para as seis skills com uma linha de gatilho cada;
a mudança consta como decisão deliberada (regra da casa sobre os dois arquivos).

## 7. Rollout em três ondas

**Onda 1 — disciplina manual (imediato, sem código).** R1, R4, R5, R6 nos
próximos casos interativos. Nenhum gate muda. Custo: a migração das fichas
(uma sessão) e minutos por caso.

**Onda 2 — ligação à esteira (após 3 casos da onda 1).** R2, R3, R7, R9.
Prompts e contratos passam a exigir os artefatos; ainda nada bloqueia.

**Onda 3 — medição e decisão de bloqueio (após 10 casos).** Medir as métricas
da § 8, calibrar limiares, e decidir por ficha `forja-adr` quais elos viram
bloqueantes (candidatos naturais: R3 na tabela de lastro, R6 na revisão
cruzada). Bloquear antes de calibrar é vedado.

## 8. Métricas (recomputáveis, não autodeclaradas)

| Métrica | Fonte | Alvo após 10 casos |
|---|---|---|
| Pautas de conselho com seção "já rejeitado" e 3 perguntas | artefato de pauta no caso | 100% |
| Proposta já-rejeitada reaparecendo em parecer sem fato novo | leitura dos pareceres | 0 |
| Proposições decisivas com os 6 campos na tabela de lastro | tabela de lastro | 100% |
| Blocos "seu olho" rastreáveis à lista de hesitações | e-mail × artefato interno | 100% |
| Diversidade de consequências declaradas nas listas (anti-formulário) | contagem de valores distintos | cresce com o nº de itens |
| Revisões cruzadas partindo de HANDOFF.md | state/<caseId>/ | 100% |
| `editor_usage` com `stop_reason` | JSON de runs novos | 100% dos runs pós-R7 |

## 9. Riscos além do formulário (§ 4)

- **Skill não dispara** — descrição é o roteador; testar com pergunta indireta
  em sessão nova e ajustar descrição, não corpo. Skills de projeto só carregam
  dentro da pasta da fábrica: limite aceito.
- **Sobrecarga por caso** — as disciplinas somam minutos, não horas; se em
  algum caso a triagem R4 custar mais que isso, está sendo feita com pesquisa,
  o que a própria skill proíbe.
- **Dupla fonte de verdade (skill × contrato de fase)** — quando a onda 2
  embutir a disciplina no contrato, a skill vira a explicação e o contrato a
  exigência; divergência entre os dois se resolve no contrato e a skill é
  atualizada na sequência, nunca deixada para depois.

## 10. Pendências e decisões abertas

1. R8 construir ou rejeitar — decisão do Igor, registrada em ficha.
2. Onde exatamente a onda 2 pendura R2 e R3 (prompt de workflow vs. contrato
   de fase) — proposta: contrato, porque prompt não é auditável por recomputo.
3. Se a entrevista adaptativa de gosto jurídico (candidato `level-up`/`teach`
   invertido) entra no ciclo do plano 29/25-EDGE — fora deste PRD.
