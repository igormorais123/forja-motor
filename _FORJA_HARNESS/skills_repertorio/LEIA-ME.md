# Repertório de skills da FORJA — cardápio mestre

> **Natureza deste diretório:** cardápio, não contrato — **com quatro exceções
> nomeadas** (abaixo). O que obriga é o contrato da fase (`phase_contracts/F*.json`), o
> `CLAUDE.md` da fábrica e o `AGENTS.md`. Este repertório existe para que o agente
> **saiba que o recurso existe** no momento em que ele resolveria o problema — e para
> que decida, com critério escrito, usar ou não usar.

Criado em 06/08/2026 por ordem do Igor. Motivo: 402 skills instaladas entre Claude,
Hermes, Codex e projeto, e nenhuma ligação entre elas e as fases da esteira. Skill que
o agente não lembra que existe no ponto certo é skill que não existe — o mesmo modo de
falha da Lição 89 (gate instalado na rota que ninguém percorre).

## Como usar sem queimar contexto

1. **Leia apenas o documento da fase em que você está.** Cada um tem 150–250 linhas.
   Ler os onze é desperdício e nenhum agente precisa disso.
2. Se você já sabe qual skill quer, vá direto à ficha dela — as fichas são
   autocontidas e repetidas em cada fase onde a skill serve. **A redundância é
   deliberada:** o agente de F7 não deve precisar abrir o documento de F1.
3. Para uma consulta programática (qual skill serve a qual fase, custo, risco), leia
   `CATALOGO_SKILLS.json` em vez dos markdowns. Ele é a fonte legível por máquina.

## As cinco skills que NÃO são opcionais

O resto do repertório é escolha. Estas cinco são ordem escrita e o cardápio não as
afrouxa:

| Skill | Onde | Fundamento |
|---|---|---|
| `helena` | F4 | ordem do Igor, 09/07/2026; gate `helena_present` e elo bloqueante do F10 |
| `cicero` | F4 | ordem do Igor, 09/07/2026; gate `cicero_present` e elo bloqueante do F10 |
| `diabob` | F4 e F7 | **ordem do Igor, 06/08/2026**; executor `forja_diabob.py` no Grok 4.5, por determinação do titular de 26/07/2026 |
| `fabrica-visual-peticoes` | F8 | "invocar em toda peça"; rege protocolo e pipeline visual |
| `padrao-visual-medina` | F6 (estrutura) e F8 | "referência visual OBRIGATÓRIA de toda petição" |

**O Diabob não é a mesma coisa que `forja` (red team das nove perguntas), e uma não substitui a outra.** A
`forja` (red team das nove perguntas) é o protocolo das nove perguntas, conduzido por dentro. O Diabob é o
contraditório por **outra família de modelo** — Grok 4.5, uma terceira família ao lado
de Claude e Codex. O motivo está escrito no próprio executor: red team feito pelo mesmo
modelo que produziu a análise repete os pontos cegos com voz mais dura. Nomear o modelo
é o que transforma o Diabob de tom em contraditório real.

O parecer do Diabob é **insumo interno de auditoria**: não vai para a peça, não vira
fundamento e não substitui o F7. Como todo modelo externo na FORJA, ele **propõe
objeções, não afirma fatos**.

Estado do gate, para não decorar errado: `forja_conselho.py` hoje valida os pareceres de
Helena e Cícero. A obrigatoriedade do Diabob é **de protocolo, ainda não verificada por
gate** — o que significa que depende de quem conduz a fase, e é exatamente o tipo de
regra que a casa já viu sumir por isso.

## Fases

Coluna de entregas é **resumo**, não a lista completa: as saídas obrigatórias de cada
fase estão no contrato, e só ele vale.

| Fase | Documento | Principais entregas |
|---|---|---|
| F0 | [`F0.md`](F0.md) | `case_manifest`, `reconciliation_report` |
| F1 | [`F1.md`](F1.md) | `document_index`, `coverage_ledger`, `injection_scan` |
| F2 / F2A | [`F2.md`](F2.md) | `product_classification`, `risk_classification`, `question_tree` |
| F3 | [`F3.md`](F3.md) | `fact_ledger`, `chronology`, `contradictions`, `sources_map`, `adversarial_audit` |
| F4 | [`F4.md`](F4.md) | `blueprint`, `proposition_ledger`, pareceres Helena e Cícero, `council_decisions` |
| F5 | [`F5.md`](F5.md) | `source_ledger`, `citation_checklist` |
| F6 | [`F6.md`](F6.md) | `draft_markdown`, `paragraph_provenance` |
| F7 / F7-B | [`F7.md`](F7.md) | `f7_gate_result`, `red_team_report`, `audited_markdown`, `final_markdown` |
| F8 / F8-S | [`F8.md`](F8.md) | `docx`, `visual_qa_ledger`, `visual_build_manifest` |
| F9 | [`F9.md`](F9.md) | `package_manifest`, `email_response`, memória de auditoria |
| F10 | [`F10.md`](F10.md) | `delivery_evidence`, `run_metrics`, `retrospective` |
| — | [`TRANSVERSAIS.md`](TRANSVERSAIS.md) | skills que servem à esteira inteira, não a uma fase |

## As oito perguntas que decidem se a skill entra

Não some as respostas. **Três delas são bloqueio absoluto** — uma só já veta, e nenhuma
quantidade de vantagem nas outras compensa:

- **Pergunta 7** — colide com regra inviolável: não use, ponto.
- **Pergunta 8** — a ação é irreversível (envio externo, publicação, exclusão): não use
  sem autorização expressa para aquela ação específica.
- **Pergunta 6** — ninguém confere a saída: não use até existir quem confira.

As outras cinco são graduais e se pesam entre si: custo de contexto, dependência
externa, risco de fabricação, o que já existe na casa e o artefato alimentado. Elas
informam a escolha; não a vetam sozinhas.

| # | Pergunta | Por que importa |
|---|---|---|
| 1 | **Qual artefato do contrato ela alimenta?** | Skill que não termina em artefato nomeado é passeio. Se você não sabe responder, não invoque. |
| 2 | **O que já existe na casa faz isso?** | `forja_lastro.py`, `forja_verificador.py`, `medina_svg_kit.py` e os demais são a primeira opção sempre. Skill externa entra onde não há script. |
| 3 | **Ela pode fabricar conteúdo?** | Skill generativa (pesquisa, imagem, diagrama semântico) exige lastro depois. Skill de leitura e extração, não. |
| 4 | **Ela depende de rede, login ou crédito pago?** | Dependência externa falha em execução headless e agendada. Tenha o caminho sem ela. |
| 5 | **Quanto custa em contexto?** | Skill pesada carregada por hábito é o que faz a janela estourar antes de F7. |
| 6 | **Quem confere a saída dela?** | Toda saída de skill entra na esteira como insumo, nunca como conclusão. Se ninguém confere, o gate correspondente é seu. |
| 7 | **Ela colide com regra inviolável?** | Paleta, identidade visual, fronteira motor/acervo, origem operacional do insumo, "advogado, não juiz". |
| 8 | **A decisão é reversível?** | Skill que escreve arquivo em pasta de caso, dispara e-mail ou faz publicação externa é irreversível na prática. Confirme antes. |

## Eixos de modulação usados nas fichas

Cada ficha traz cinco marcadores fixos, sempre com o mesmo vocabulário:

- **Custo de contexto** — `baixo` (menos de 2k tokens), `médio` (2k a 8k), `alto` (mais de 8k ou abre muitos arquivos).
- **Dependência externa** — `nenhuma`, `rede`, `login`, `crédito pago`.
- **Risco de fabricação** — `nulo` (só lê e extrai), `baixo` (transforma o que recebeu), `alto` (gera conteúdo novo).
- **Reversibilidade** — `total` (só produz texto na sessão), `parcial` (escreve arquivo), `nenhuma` (dispara envio, faz publicação externa, apaga).
- **Quem confere depois** — o gate, script ou pessoa que valida a saída. Nunca "ninguém".

## Precedência em conflito

1. Regra inviolável do `CLAUDE.md` da fábrica vence qualquer skill.
2. Contrato da fase (`phase_contracts/F*.json`) vence o cardápio.
3. Script da casa vence skill externa que faça a mesma coisa.
4. Entre skills visuais: `fabrica-visual-peticoes` rege protocolo e pipeline;
   `padrao-visual-medina` rege a linguagem de design.
5. Entre duas skills equivalentes, vence a de menor dependência externa.

## Divergências declaradas entre o `CLAUDE.md` e os contratos

Estas duas existem hoje e o repertório **não escolhe um lado em silêncio**. Quem
trabalhar nelas confira as duas fontes antes de agir, e quem for reconciliar decida
explicitamente qual prevalece.

| Assunto | `CLAUDE.md` diz | O contrato ou o código diz | Como o repertório trata |
|---|---|---|---|
| Onde a Diretriz 28 é percorrida | "a pesquisa de **F3** percorre os níveis nesta ordem" | `F3` é `F3_FONTES_REGIMENTO_LEIS`; a fase de pesquisa é `F5_PESQUISA_OFICIAL`, que produz `source_ledger` e `citation_checklist` | a ficha fica em **F5**, e F3 aponta a divergência. A ordem em si não muda em nenhuma leitura |
| Executor da subfase F7-B | "a chamada é explícita por `forja_fable5.py`" | `forja_editorial.py` tem 25,8 KB e é o executor; `forja_fable5.py` tem 1,8 KB e o `INDICE_FORJA.md` o declara **shim legado** | o repertório cita `forja_editorial.py` e nomeia o shim. O `CLAUDE.md` está desatualizado neste ponto |

## Skills adaptadas à FORJA

Sete skills genéricas foram copiadas e reescritas para esta fábrica, em
`..\..\.claude\skills\`. Elas **não substituem** nenhum script existente — chamam os
scripts da casa e acrescentam o que a versão genérica não sabe (ordem de pesquisa do
escritório, vocabulário fechado de bloqueio, gates S6 e S7, `familyAssurance`).

| Skill adaptada | Origem genérica | Fase |
|---|---|---|
| `forja` (ingestão dos autos) | `pdf`, `docx` | F1 |
| `forja` (exploração do problema) | `problem-solving-vila` | F2 / F2A |
| `forja` (conferência ao vivo nos tribunais) | `testar-navegador` | F1, F3, F5, F7 |
| `forja` (pesquisa de jurisprudência) | `garimpo-tribunais`, `deep-research` | F5 |
| `forja` (red team das nove perguntas) | `diabob` | F4, F7 |
| `forja` (revisão cruzada entre famílias) | `codex-integrado`, `inteia-review-iterativo` | F7 |
| `forja` (saída com voz humana) | `revisar-anti-ia` | F6, F7, F9 |

As versões genéricas continuam disponíveis e são citadas nas fichas quando o caso sai
do escopo da fábrica.

## Registro

Este diretório está declarado em `INDICE_FORJA.md`, `DOCUMENTACAO_TECNICA.md`,
`docs/ARCHITECTURE.md`, `ARCHIFY_ARQUITETURA.md` e `GRAPHIFY_GRAFO.md`. O `MAPA_IA.md`
local é gerado por `..\..\ATUALIZAR_MAPA_IA.ps1`.
