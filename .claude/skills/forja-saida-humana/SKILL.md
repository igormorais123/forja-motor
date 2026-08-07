---
name: forja-saida-humana
description: 'Tirar do texto os tiques que denunciam geração automática antes que o gate bloqueie, usando a mesma régua do forja_estilo_humano.py em vez de inventar uma segunda. Use ao fechar a redação em F6, nos dois passes de estilo de F7 (antes e depois da revisão editorial) e no corpo do e-mail de entrega em F9. Diferencial: revisar-anti-ia traz uma lista genérica de tiques; esta orquestra o script que efetivamente bloqueia F6, F7, F9, o render, o pacote e o rascunho, e conhece os pontos da esteira em que ele é chamado.'
metadata:
  adaptada_de: [revisar-anti-ia]
  fases: [F6, F7, F9]
  script: forja_estilo_humano.py
  protocolo: PROTOCOLO_ESCRITA_HUMANA_FORJA.md
  criada_em: 2026-08-06
---

# Saída humana — estilo antes do gate

## Uma régua só

O `forja_estilo_humano.py` é quem bloqueia. Esta skill **não cria segunda régua** — ela
lê a do script, explica o que fazer e roda a verificação antes que o gate a rode por
você. Duas réguas divergentes seriam pior que uma.

```
python _FORJA_HARNESS\forja_estilo_humano.py <arquivo> --tipo peca
python _FORJA_HARNESS\forja_estilo_humano.py <arquivo> --tipo estudo
python _FORJA_HARNESS\forja_estilo_humano.py <arquivo> --tipo email
```

Protocolo completo: `PROTOCOLO_ESCRITA_HUMANA_FORJA.md`.

## Onde ele bloqueia

F6, F7, F9, o render, o pacote e o rascunho de e-mail. **O corpo do e-mail é vinculado
por hash** — o texto verificado é o texto que sai.

Em F7 há **dois** passes, e é o segundo que costuma ser esquecido:

1. `anti_ai_style_passed` — sobre o `audited_markdown`, antes da revisão editorial.
2. `human_style_final_pass` — sobre o `final_markdown`, **depois** que o editor
   reescreveu a forma. O editor pode reintroduzir o que o primeiro passe tirou.

## O que se procura

- hedge e ressalva vazia que não muda a afirmação
- disclaimer genérico, ladainha de ética e de proteção de dados
- separador decorativo, negrito excessivo, estrutura com aparência artificial
- jargão de inteligência artificial e vocabulário de assistente
- emoji
- frase de abertura que anuncia o que o parágrafo vai dizer
- simetria mecânica: três itens sempre, sempre com a mesma forma
- preenchimento genérico onde deveria haver o fato do caso

## O que **não** é tique, e não se corrige

- Vocabulário técnico jurídico. "Omissão qualificada", "fundamentação individualizada" e
  "erro de subsunção" são terminologia blindada exigida pelo escritório, não jargão.
- A síntese executiva no início da peça. É determinação do Prof. Fábio de 07/07 e virou
  o gate **S7** — instrução escrita disputa atenção com o resto do prompt e perde, então
  virou verificação.
- Marcador de auditoria em artefato interno. `[FONTE:]`, `[DECLARAÇÃO]`, `[INFERÊNCIA]` e
  `[VERIFICAR]` pertencem ao ledger — o que é proibido é aparecerem no protocolável.

## Placeholder é P0

`[NOME]`, `[CRC-UF]`, `[dia]` esquecidos no arquivo final são bloqueador P0. Faça a
varredura por colchete no texto final e a inspeção visual. A única exceção documentada
é o `[dia]` da data de protocolo.

## Estilo não conserta substância

Esta skill mexe na forma. Se o texto está ruim porque a proposição não tem lastro, o
problema é de F3, F5 ou F7 — e reescrever bonito o que não tem fonte só torna o defeito
mais difícil de ver.

E, em revisão editorial, vale a regra de sempre: melhoria de estilo **não autoriza**
alterar fato, número, citação, autoridade, pedido, ressalva, fecho ou identidade
processual.

## Critério de conclusão

- `forja_estilo_humano.py` sem bloqueio, no tipo certo do artefato.
- Nenhum placeholder no texto final.
- Em F7, os **dois** passes executados.
- Em F9, o corpo do e-mail verificado antes de gerar o hash.

## Repertório das fases

`_FORJA_HARNESS\skills_repertorio\F6.md`, `F7.md` e `F9.md`.
