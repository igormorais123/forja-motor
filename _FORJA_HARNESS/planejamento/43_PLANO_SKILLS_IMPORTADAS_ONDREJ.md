# Plano 43 — o que vale importar de `davidondrej/skills` para a fábrica e para a FORJA

**05/08/2026.** Fonte estudada: `github.com/davidondrej/skills`, commit `04bd15abae135f5744e3dc825a4ab9c75d61fbfc`, 47 skills em cinco famílias. Repositório lido por inteiro (frontmatter das 47; corpo integral das candidatas).

Este plano é de adaptação, não de instalação. A maior parte daquele repositório é infraestrutura pessoal de macOS de outra pessoa e não tem tradução para cá. O que vale são **seis disciplinas de processo**, e cada uma foi adotada porque fecha uma falha que esta fábrica já mediu e registrou — não porque a skill de origem era elegante.

## 1. Triagem das 47

### 1.1 Já instaladas por você, em versão pt-BR (não fazer nada)

`anti-sleep`, `decisions`, `deep-research`, `git-worktree`, `global-agent-guardrails`, `goal-loop`, `setup-help` — todas com `metadata.source_repo: davidondrej/skills` no frontmatter global. Parte do repositório já foi colhida em ciclo anterior.

### 1.2 Sem tradução para cá — descartadas com motivo

| Skill | Por que cai |
|---|---|
| `cmux`, `herdr`, `corral-launch-agents` | Orquestração de terminal macOS. Windows + Codex CLI + Hermes já cobrem o papel. |
| `nuke-cursor-app`, `macbook-metrics-setup`, `pi-custom-model`, `pi-web-search` | Ferramenta ou máquina que não é a sua. |
| `deepapi`, `deep-research`, `online-shopping`, `youtube-transcript`, `fireflies-transcript` | Dependem de API paga de terceiro. A casa já tem rota autenticada por assinatura, e criar custo recorrente sem pedido é vedado. |
| `browser-harness` | `testar-navegador`, `playwright-cli` e Chrome com perfil `scraping` já resolvem, inclusive para SCON/STJ e STF. |
| `create-readonly-db-role`, `read-prod-database`, `prod-push`, `google-safe-browsing`, `cyber-audit`, `run-deep-swe` | Fora do domínio da fábrica. |
| `codex-subagent` | `codex-integrado` e o `codex:rescue` já fazem isso melhor e no ambiente certo. |
| `agent-self-scheduling` | Os crons da FORJA já rodam e estão medidos. |
| `distribute-skill-to-all-agents`, `push-skill-to-github` | O mecanismo é symlink em `~/.agents`. Aqui a distribuição Claude/Codex é o problema tratado no item 4.3, e não se resolve por symlink. |
| `short`, `remind`, `prompt-me`, `save-idea`, `read-all-adrs` isolada | Já cobertas pelo contrato de comunicação global, ou fragmento demais para virar skill (o `read-all-adrs` entrou dentro de `forja-adr`). |
| `effective-agent-skills` | Você já tem `skill-creator` e `skills-guide`. Ver item 3: o valor dela aqui é como **checklist de auditoria**, não como skill nova. |
| `fable-safe-prompt` | Não vira skill, mas gera uma observação real — item 5. |
| `level-up`, `teach` | Não agora. A inversão interessante (extrair o gosto jurídico do Fábio por entrevista adaptativa acumulativa) já tem dono: `29_REQUISITOS_ENTREVISTA_FABIO_MEDINA_OSORIO.md` e `25_GOSTO_JURIDICO_AUTONOMO_EDGE.md`. Registrado como candidato, não como pendência. |
| `folder-specific-claude-and-agents-md` | A receita (symlink) está errada para o seu caso, mas o conjunto de regras dela é aproveitável — item 4.3. |

### 1.3 Adotadas — seis skills, escritas em `.claude/skills/` da fábrica

| Nova skill | Origem | Falha da casa que ela fecha |
|---|---|---|
| `forja-briefing-revisor` | `launch-subagent` + `gpt-review`/`fable-review` | Lição 87-99: o conselho leu o dossiê do construtor, recomendou arquitetura já rejeitada e citou função inexistente. Circularidade de autovalidação. |
| `forja-briefing-pesquisa` | `research-prompt` | Erro recorrente nº 1 das entregas reais: jurisprudência com atribuição errada; nota de rodapé não localizável. |
| `peticao-tres-escolhas` | `before-building` | Diagnóstico transversal: a IA acerta o eixo jurídico e erra por omissão nas cautelas de sênior. Custa um minuto, antes de qualquer leitura. |
| `peticao-decisoes-incertas` | `decisions` + `next-decision` | O U11 — bloco "Pontos que exigem o seu olho" — existe no protocolo e não tem procedimento. E é o tipo de gate que o formulário não satisfaz. |
| `forja-handoff-caso` | `handoff` | Revisão cruzada entre famílias é gate de produção, e o revisor hoje reconstrói o caso do zero. |
| `forja-adr` | `brain-to-docs` + `read-all-adrs` | As rejeições (RAG, 3D, `compor()` no render, inferir figura de prosa) vivem em prosa espalhada. Foi exatamente assim que uma rejeição foi reaberta pelo conselho. |

## 2. A ideia que mais importa

O achado central do estudo não é nenhuma skill isolada. É que **as duas melhores daquele repositório atacam o mesmo ponto que o `DIAGNOSTICO_F2A_DEGRADACAO_2026-08-05.md` identificou como o limite desta fábrica**: gate determinístico mede presença e forma, e a degradação é de substância.

`decisions` e `before-building` não são gates de presença. Não se satisfazem preenchendo campo, porque perguntam por hesitação e por consequência — coisas que só existem se o trabalho aconteceu. Cem perguntas com um único valor distinto de `unansweredConsequence` é um formulário; três escolhas consequentes nomeadas de intuição, ou seis decisões de que não se tem confiança, não têm caminho barato.

Não substituem o gate de diversidade de campo proposto no diagnóstico — são a contraparte humana dele, e mais baratas de instalar. Recomendo rodar as duas antes de construir o gate de diversidade, porque elas medem, na prática, se a exploração produziu substância.

## 3. Auditoria das skills existentes (não é skill nova)

De `effective-agent-skills`, seis regras que valem uma passada pelas skills desta casa — `fabrica-visual-peticoes`, `padrao-visual-medina`, `advogado-sobrehumano` e as seis novas:

1. **A descrição roteia, o corpo executa.** Se a skill não dispara, o problema está na descrição em 95% dos casos.
2. **Nunca resumir o fluxo na descrição.** O agente segue o resumo e não abre o corpo. A descrição responde "devo abrir isto agora?", nunca "quais são os passos?".
3. **Rigidez proporcional à fragilidade.** Heurística solta onde há muitos caminhos válidos; script exato onde variação é defeito. Você já faz isso por instinto no visual; vale checar se o inverso não aconteceu em algum lugar (script onde precisava de julgamento).
4. **Determinismo em código, julgamento em prompt.** Já é a doutrina da FORJA.
5. **Laço de validação declarado.** Verificar → corrigir → reverificar, escrito dentro da skill.
6. **`: ` sem aspas na descrição quebra parser estrito.** Vale para o Codex. As seis novas usam descrição entre aspas simples onde há dois-pontos.

Custo estimado: uma sessão. Não bloqueia nada.

## 4. Implementação

### 4.1 Onde ficam

`<fábrica>/.claude/skills/<nome>/SKILL.md` — escopo de projeto, versionadas com o repositório, e não poluem o catálogo global (que já passa de 200). Trade-off assumido: só aparecem trabalhando dentro da fábrica. É o que se quer.

### 4.2 Ligação com o que já roda — ordem sugerida

| Onde | O que muda | Esforço |
|---|---|---|
| Entrada de demanda (F0/F1) | `peticao-tres-escolhas` antes da F2A; as respostas viram entrada declarada da árvore | mínimo |
| F3 pesquisa | Todo levantamento jurisprudencial nasce de um briefing pela `forja-briefing-pesquisa`; os seis campos por achado alimentam a tabela de lastro | baixo |
| F4 conselho | O briefing de Helena e Cícero passa a ser montado pela `forja-briefing-revisor`, com checklist anti-contaminação. Hoje `forja_conselho.py` **valida** o parecer pronto (achados, decisões, veredito) e não toca a montagem do briefing — é o vão que a skill preenche | baixo |
| F7 / entrega | `peticao-decisoes-incertas` antes de fechar; a saída vira o bloco "Pontos que exigem o seu olho" | baixo |
| Fim de sessão / revisão cruzada | `forja-handoff-caso` grava `state/<caseId>/HANDOFF.md` | mínimo |
| Qualquer proposta de arquitetura | Leitura obrigatória de `_FORJA_HARNESS/decisoes/` antes; ficha nova depois | médio (migração inicial) |

### 4.3 A divergência CLAUDE.md × AGENTS.md

Medido em 03/08: dos 107 trechos substantivos do `AGENTS.md`, 78 não existem no `CLAUDE.md`, e 47 do `CLAUDE.md` não existem lá; 29 em comum.

A receita do repositório de origem — `ln -s CLAUDE.md AGENTS.md` — **não serve aqui**, por duas razões: symlink no Windows exige privilégio, e, mais importante, a divergência é em parte deliberada (o Codex precisa por escrito do que o Claude recebe pela memória do projeto). Symlink apagaria isso sem decisão.

O que vale importar são as regras de manutenção, e elas cabem numa ficha `forja-adr` mais um script:

- separar **Restrições** (proibições duras) de **Convenções** (o que se costuma fazer) — melhora a adesão;
- nada de ALWAYS/NEVER absoluto sem a exceção escrita, porque regra absoluta com caso de borda passa a ser ignorada inteira;
- **nunca resumir ou encurtar automaticamente** esses arquivos: crescimento deliberado, poda manual;
- **laço de manutenção**: quando o Igor corrige o agente sobre algo que o arquivo deveria ter evitado, a regra entra no arquivo na hora — não depois;
- nada de árvore de diretório nem detalhe que se obtém com `ls`: apodrece e gasta contexto.

Proposta de script: `forja_divergencia_instrucoes.py`, que recomputa a divergência entre os dois arquivos e classifica cada trecho em **núcleo comum** (deve estar nos dois), **específico do Codex** e **específico do Claude**. Sem isso, a reconciliação continua sendo trabalho manual que ninguém faz. Não implementado — é decisão sua se entra.

## 5. Observação sobre o modelo editorial (de `fable-safe-prompt`)

Aquela skill existe porque classificadores de entrada derrubam ou rebaixam o modelo por superfície de texto, quase independentemente da intenção. Peça de improbidade, crime, corrupção e investigação é exatamente o vocabulário que dispara esse tipo de filtro.

O protocolo editorial já exige confirmar o modelo efetivo na evidência. A pergunta a conferir — **não conferi, e por isso não afirmo** — é se o `EDITORIAL_RESULT.json` registra hoje o `stop_reason` e o modelo que de fato respondeu, ou só o modelo pedido. Se registrar só o pedido, um rebaixamento silencioso passa pelo gate `cross_model_review_verified` como se nada tivesse acontecido. Vale uma verificação em `forja_fable5.py` e `forja_editorial_model.py`.

## 6. O que este plano não faz

- Não instala nada globalmente e não altera skill existente.
- Não mexe em gate, contrato de fase ou pipeline. As seis skills são disciplina de processo; ligar cada uma ao ponto da esteira (item 4.2) é decisão separada, e a de maior custo é a migração das fichas de decisão.
- Não resolve o F2A. Oferece duas disciplinas que medem substância barato, enquanto o gate de diversidade de campo não existe.
- Não reconcilia CLAUDE.md e AGENTS.md. Dá o critério e propõe o instrumento.
