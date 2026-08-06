---
name: peticao-decisoes-incertas
description: 'Levantar as escolhas feitas durante a produção de uma peça ou de um artefato da fábrica das quais quem produziu NÃO tem confiança, com a alternativa que foi descartada. Use antes de fechar F7, ao montar o bloco "Pontos que exigem o seu olho" do e-mail de entrega, ou quando o usuário pedir /peticao-decisoes-incertas. Diferencial: olha para trás, sobre escolhas já feitas; a triagem de escolhas ainda em aberto é peticao-tres-escolhas.'
disable-model-invocation: true
metadata:
  source_repo: davidondrej/skills
  source_ref: 04bd15abae135f5744e3dc825a4ab9c75d61fbfc
  source_skills: decisions, next-decision
  local_adaptation: especialização jurídica da skill global `decisions`, com as sete dúvidas caras da fábrica e roteamento para o bloco de entrega
---

# Decisões de que não tenho confiança

Nasce do diagnóstico do F2A: gate determinístico mede presença e forma, e a degradação é de substância. Um formulário de cem perguntas se preenche; uma lista de baixa confiança, não — porque só quem produziu sabe onde hesitou, e declarar hesitação não tem atalho barato.

## O que produzir

Ao trabalhar nesta peça/artefato, quais escolhas importantes você fez das quais **não** está confiante?

Pense a fundo. Percorra as decisões que realmente mudam o resultado e pergunte, para cada uma, se existe alternativa boa que não foi considerada.

**NÃO liste** aquilo em que a solução já é claramente a melhor possível. Lista longa é ruído; o valor está em três a seis itens verdadeiros.

## Formato de cada item

```
<o que foi escolhido> — em vez de <a alternativa descartada>
Por que fica em dúvida: <o que faria a escolha estar errada>
Onde está: <página, parágrafo ou arquivo>
Quem resolve: <eu com mais pesquisa | Fábio | cliente | só o tribunal dirá>
```

## Onde olhar primeiro nesta fábrica

As dúvidas que mais custaram nas entregas reais, na ordem em que costumam aparecer:

- premissa de data e de contagem de prazo assumida sem prova nos autos;
- identidade do ato impugnado quando há mais de um recurso, decisão ou retratação possível;
- tese que ficou principal versus a que virou subsidiária, e a que se decidiu não alegar;
- atribuição de frase a precedente, e *ratio* tomada por *dictum*;
- enquadramento de prescrição por matriz (fundo de direito, metodologia, parcelas, negativa, ciência) quando a peça acabou usando um rótulo global;
- questão processual lateral que se decidiu não tratar: prevenção, preclusão, competência interna, composição atual do órgão, fato superveniente;
- elemento visual mantido sem que se saiba se reduz esforço cognitivo do julgador.

## Para onde vai

1. Cada item vira uma linha do bloco **"Pontos que exigem o seu olho"** do e-mail de entrega, com página. O bloco é anti-complacência: se ele sair vazio ou genérico, a peça não está pronta — está mal auditada.
2. Item cuja resposta é "eu com mais pesquisa" vira briefing pela skill `forja-briefing-pesquisa` antes da entrega, não depois.
3. Item que envolve escolha de arquitetura ou de método da fábrica (não da peça) vira registro de decisão pela skill `forja-adr`.
4. Nada disto entra no DOCX protocolável. É artefato interno.

## Gate

Peça declarada pronta com esta lista vazia exige justificativa escrita de por que não houve nenhuma escolha incerta. Em peça longa, lista vazia é sinal de auditoria que não aconteceu — o padrão medido nesta casa é que nenhuma peça saiu protocolável na v1.
