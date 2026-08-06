---
name: forja-adr
description: 'Registrar e consultar as decisões de arquitetura e de método da fábrica — inclusive as REJEITADAS — em fichas curtas e numeradas, para que nenhuma rodada seja gasta reabrindo o que já foi decidido. Use ao decidir método, gate, pipeline ou protocolo da esteira, ao rejeitar uma proposta, e SEMPRE antes de propor mudança arquitetural ou montar pauta de conselho. Diferencial: registra decisão da fábrica; decisão sobre uma peça específica fica no relatório de melhorias do caso.'
metadata:
  source_repo: davidondrej/skills
  source_ref: 04bd15abae135f5744e3dc825a4ab9c75d61fbfc
  source_skills: brain-to-docs, read-all-adrs
  local_adaptation: ficha com critério de reabertura, ênfase em rejeição e migração das rejeições já existentes
---

# Registro de decisões da fábrica

Existe porque esta casa já pagou por não ter: o conselho de personas recomendou arquitetura que havia sido rejeitada, e as rejeições vivem hoje em prosa espalhada por planos, retrospectivas e no CLAUDE.md — legíveis para quem já sabe, invisíveis para quem chega.

Local: `_FORJA_HARNESS/decisoes/NNNN-slug.md`. Numeração sequencial, sem reaproveitar número.

## Antes de propor qualquer mudança de arquitetura ou método

Leia **todas** as fichas da pasta, do início ao fim. Não amostre, não confie no título, não pule as `Rejeitada` — são justamente as que evitam a rodada perdida. Se a sua proposta coincidir com uma ficha rejeitada, só prossiga apresentando o **fato novo** que não existia quando ela foi rejeitada; sem fato novo, não prossiga.

Isso vale igualmente para pauta de conselho: briefing de revisor sem a lista do que já foi rejeitado devolve o que já foi descartado.

## Formato da ficha

```markdown
# NNNN — <decisão em uma linha>

- Status: Aceita | Rejeitada | Substituída por NNNN | Proposta
- Data: DD/MM/AAAA
- Quem decidiu: <Igor | Fábio | conselho | construtor>

## Contexto
<O que estava em jogo. O problema real, com a evidência que o mostrou —
de preferência a falha concreta em RETROSPECTIVAS.md ou na entrega.>

## Decisão
<O que foi decidido, em voz ativa.>

## Consequências
<O que passa a valer, o que fica proibido, o que se aceita perder.>

## Por que as alternativas caíram
<Uma linha por alternativa. É o que impede a reabertura.>

## O que reabriria esta decisão
<O fato novo específico que mudaria a conclusão. Se não existir nenhum, dizer isso.>
```

Ficha curta. Se passar de uma página, o detalhe pertence a um plano em `planejamento/`, e a ficha aponta para ele.

## Regras

- **Rejeição também é decisão.** Ficha com `Status: Rejeitada` é o produto mais valioso desta pasta.
- **Uma decisão por ficha.** Plano com cinco decisões vira cinco fichas apontando para o plano.
- **Não se edita decisão passada.** Decisão que muda ganha ficha nova, e a antiga passa a `Substituída por NNNN`.
- **Toda ficha nomeia a evidência.** Decisão de método sem falha real por trás é preferência, não decisão — registre como preferência e diga isso.
- **O campo "o que reabriria" é obrigatório.** Decisão sem critério de reabertura é dogma, e dogma envelhece sem aviso.

## Migração inicial (fazer uma vez)

Estas decisões já estão tomadas e hoje vivem só em prosa. Cada uma vira ficha, com o motivo que já está registrado:

| Decisão | Status | Onde está hoje |
|---|---|---|
| RAG/GraphRAG na esteira | Rejeitada | plano 07, seção de rejeições |
| Governança de confidencialidade por IA | Rejeitada | plano 07 |
| LLM-as-judge como gate | Rejeitada | plano 07 |
| RCT interno | Rejeitada | plano 07 |
| Firewall de saída dedicado | Rejeitada | plano 07 |
| Visualização 3D | Rejeitada | plano 19 / memória do projeto |
| Integrar `compor()` dentro de `forja_render_docx.render()` | Rejeitada | CLAUDE.md, assinatura visual |
| Inferir conteúdo semântico de figura a partir de prosa | Rejeitada | CLAUDE.md, brief F7.5 |
| Detectar identidade visual por valor de cor | Rejeitada | lição 87-99 |
| Limiar de contraste em 2,0:1 e não 3,0:1 da WCAG | Aceita | CLAUDE.md, gate de colisão SVG |
| Modelo editorial `claude-opus-5`, Fable 5 como legado | Aceita (substitui a de 15/07) | CLAUDE.md |
| Congelar o diagnóstico F2A v2 antes de medir a causa | Aceita | plano 40 § 21 |
| Entrada única de produção visual (`forja_visual_build.py`) | Aceita | CLAUDE.md |

## Ligações

- Escolha de peça de que não se tem confiança e que envolve método da fábrica: chega aqui pela skill `peticao-decisoes-incertas`.
- Pauta de conselho e revisão: a seção "já rejeitado" do briefing sai desta pasta — ver `forja-briefing-revisor`.
