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

## Critério de reabertura

Fato novo que mostre skill do repertório sem uso em três casos consecutivos (sinal de
que a ficha está no lugar errado), ou skill rejeitada que passe a resolver problema que
nenhuma da lista resolve. Aumento do catálogo de skills instaladas, por si, não é fato
novo.
