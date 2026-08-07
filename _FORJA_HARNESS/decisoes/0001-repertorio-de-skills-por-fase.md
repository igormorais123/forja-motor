# 0001 — Repertório de skills por fase, como cardápio e não como contrato

- Status: Aceita
- Data: 06/08/2026
- Quem decidiu: Igor

## Contexto

Havia 402 skills instaladas na máquina — 238 no Claude, 132 no Hermes, 26 no Codex e 6
no projeto — e nenhuma ligação entre elas e as fases F0–F10 da esteira. Na prática o
agente usava a skill que lembrava, não a que servia, e a maioria do repertório era
inalcançável por desconhecimento.

O modo de falha é conhecido e já está catalogado: a Lição 89 registra que **gate
instalado na rota que ninguém percorre é gate nenhum** — o elo 4-B era sério e rodou em
três casos na história inteira. Recurso que existe e não é lembrado no ponto de decisão
é equivalente a recurso ausente.

O risco oposto também é real: transformar as skills em obrigação criaria uma segunda
máquina de processo ao lado dos contratos de fase, do ADR e da fila — exatamente o que
motivou a rejeição da família `gsd-*`.

## Decisão

Criar `_FORJA_HARNESS/skills_repertorio/` com **um documento por fase** (`F0.md` a
`F10.md`, mais `TRANSVERSAIS.md` e o cardápio mestre `LEIA-ME.md`), declarados como
**cardápio, não contrato**. Nenhuma skill listada é obrigatória; as únicas obrigatórias
continuam sendo `helena` e `cicero` em F4, por ordem anterior.

Cada ficha declara cinco eixos fixos — custo de contexto, dependência externa, risco de
fabricação, reversibilidade e **quem confere depois** — e responde a mesma pergunta
inicial: qual artefato do contrato de fase esta skill alimenta.

O agente lê **apenas** o documento da fase corrente. As fichas se repetem nas fases onde
a mesma skill serve; a redundância é deliberada e é o que permite a leitura isolada.

Copiar e adaptar sete skills genéricas para a fábrica, em `.claude/skills/`:
`forja-ingestao-autos`, `forja-exploracao-problema`, `forja-campo-tribunais`,
`forja-pesquisa-jurisprudencia`, `forja-red-team`, `forja-revisao-cruzada` e
`forja-saida-humana`. Elas **chamam** os scripts da casa e não substituem nenhum.

## Consequências

- Passa a valer: consultar o documento da fase antes de trabalhar nela.
- Fica proibido: tratar o cardápio como obrigação, ou deixar skill externa produzir
  conclusão sem gate que a confira.
- Precedência: regra inviolável do `CLAUDE.md` vence skill; contrato de fase vence
  cardápio; **script da casa vence skill externa equivalente**.
- Aceita-se perder: a chance de o agente descobrir sozinho uma skill fora da lista. O
  repertório é fechado de propósito — lista longa não é lida.
- Manutenção: `skill-creator` é a rota para alterar as sete adaptadas, e toda alteração
  exige caso real de contraprova, como o teste-âncora do gate visual.

## Rejeitado junto, para não ser reaberto

- **Diagramação genérica** (`paperbanana-diagramas`, `visual-thinking`,
  `visual-law-inteia`, `dataviz`, `data-visualization`, `archify` em peça): produzem
  figura fora da identidade Medina Osório e sem os gates de legibilidade, overflow e
  colisão do `medina_svg_kit.py`.
- **Navegador redundante** (`browse`, `gstack`, `playwright-cli`, `browser-harness`,
  `dogfood`): `forja-campo-tribunais` tem o perfil logado que os portais exigem;
  `fetch-rendered` cobre o resto.
- **Jurídico duplicado** (`themis-nomos`, `colmeia-juridico-peticoes`,
  `osa-themis-juridico`, `ciceromini`, `helenamini`).
- **UI e frontend** (`impeccable`, `ui-ux-pro-max`, `interface-design`,
  `refactoring-ui`, `frontend-design`, `ux-heuristics`, `design-dna`, `omni-figma`).
- **Família `gsd-*` inteira** (cerca de 70 skills): segunda máquina de planejamento.
- **Segurança de sessão** (`careful`, `guard`, `freeze`, `decisions`): já coberta.
- **Coleta e campanha** (`apify-*`, eleitorais, Mirante, finanças, mídia, voz, vídeo).

## Em observação, não adotado

- `proj-analise-juridica-preditiva` — alinha-se à Diretriz 28, que persegue quem vai
  julgar, mas predição sem lastro contraria o que a fábrica exige de toda afirmação.
  Entraria como insumo interno de F4, jamais como texto protocolável.
- `archify` — inútil para peça, útil para documentar o próprio harness.

## Revisão cruzada (06/08/2026)

Revisado por Codex no `gpt-5.6-sol`, família distinta, sobre o material integral entregue por
stdin — 105.044 tokens. `familyAssurance` deste artefato: `cross_family`. Registro
completo em `skills_repertorio/REVISAO_CODEX_2026-08-06.md`.

Vinte achados viraram correção, três dos quais de risco: envio de e-mail e
sincronização de painel estavam antecipados de F10 para F9, e a regra de cache da
`forja-campo-tribunais` podia burlar o `live_official_source_replayed`. Duas obrigações
invioláveis estavam ausentes: `_LEIS_GERAIS` em F3 e a obrigatoriedade de
`fabrica-visual-peticoes` e `padrao-visual-medina` — que passaram a ser as **quatro**
exceções nomeadas à natureza opcional do cardápio, ao lado de Helena e Cícero.

Três achados P1 do revisor foram **derrubados** pela conferência do código, e ficam
registrados para não voltarem: o executor de F7-B é `forja_editorial.py` e não o shim
`forja_fable5.py` que o `CLAUDE.md` ainda nomeia; a Diretriz 28 roda em F5 pelos
contratos, embora o `CLAUDE.md` diga F3; e `no_pdf_or_raster_rendering` afirma que a QA
não rasterizou, não que a entrega dispensa PDF. As duas primeiras viraram **divergências
declaradas** no `LEIA-ME.md` — o repertório expõe o conflito em vez de escolher em
silêncio, e a reconciliação do `CLAUDE.md` fica pendente para o Igor.

Um achado foi aceito em parte: a repetição de **narrativa histórica** entre fases é peso
morto, embora a repetição das **fichas** siga deliberada. Fica como dívida declarada.

## Correção de 06/08/2026 — Diabob é obrigatório

Ordem do Igor, no mesmo dia. O conselho obrigatório passou de duas para **três** vozes:
Helena, Cícero e **Diabob**. Com as duas skills visuais, são **cinco** as exceções à
natureza opcional do cardápio.

Isto corrigiu um erro de classificação meu, não só uma omissão: o catálogo marcava
`diabob` como `status: preterida`, em favor da `forja-red-team`. Estava errado. As duas
não são substitutas — a `forja-red-team` conduz as nove perguntas **por dentro**, e o
Diabob traz o contraditório de **outra família de modelo** (`forja_diabob.py`, Grok 4.5,
por determinação do titular de 26/07/2026). O próprio executor explica por quê: red team
feito pelo mesmo modelo que produziu a análise repete os próprios pontos cegos com voz
mais dura.

Somado à `forja-revisao-cruzada` no Codex, F7 passa a ter **três famílias** sobre a mesma
peça. O parecer do Diabob é insumo interno: propõe objeções, não afirma fatos, e não
substitui o F7.

`CLAUDE.md` e `AGENTS.md` atualizados. **Pendência declarada:** `forja_conselho.py`
valida apenas Helena e Cícero — a obrigatoriedade do Diabob é de protocolo e ainda não
é verificada por gate. Pela própria regra da casa, regra escrita que não pega vira gate.

## Critério de reabertura

Fato novo que mostre skill do repertório sem uso em três casos consecutivos (sinal de
que a ficha está no lugar errado), ou skill rejeitada que passe a resolver problema que
nenhuma da lista resolve. Aumento do catálogo de skills instaladas, por si, não é fato
novo.
