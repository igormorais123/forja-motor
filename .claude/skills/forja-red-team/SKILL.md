---
name: forja-red-team
description: 'Atacar por escrito o blueprint ou a peça da FORJA com as nove perguntas estruturadas do protocolo, incluindo a nona, anti-bajulação — a peça aceita premissa do comando ou do e-mail que os autos não sustentam? Use ao classificar risco em F2, auditar peça adversária em F3, fechar o blueprint em F4 e satisfazer red_team_completed em F7. Diferencial: diabob é contrarian genérico e, aplicado cru a caso de cliente, produz texto que concede; esta carrega a calibragem advogado-não-juiz e registra a decisão sobre cada objeção.'
metadata:
  adaptada_de: [diabob]
  fases: [F2, F3, F4, F6, F7]
  criada_em: 2026-08-06
---

# Red team — as nove perguntas

> **A porta da esteira é a skill `forja`.** Ela traz o fluxo inteiro, de F0 a F10, os
> comandos, os gates e as ordens invioláveis. Esta ficha detalha um ponto do caminho e
> pressupõe aquela leitura — abra-a primeiro se você chegou aqui sem contexto.

Estruturado e **por escrito**. Não é a impressão de que o texto está bom.

## A calibragem que a versão genérica não tem

**Advogado, não juiz.** Diretriz escrita do titular, 06/08/2026. Risco, objeção e
precedente contrário são **identificados e enfrentados** — inclusive por distinção
tecnicamente sustentável — e jamais adotados nem antecipados como juízo desfavorável ao
cliente.

Lê-se junto com a regra de enfrentar a objeção mais forte da adversa: **enfrentar serve
para vencer, não para conceder**. Isoladas, as duas se degradam — uma vira otimismo
cego, a outra vira parecer contra o próprio cliente.

## Esta skill NÃO substitui o Diabob

Ordem do Igor de 06/08/2026: `diabob` é **obrigatório** em F4 e F7, ao lado de Helena e
Cícero. As duas coisas são diferentes e as duas rodam:

- **`forja-red-team` (esta)** — o protocolo das nove perguntas, conduzido por dentro,
  com a calibragem "advogado, não juiz" e a decisão registrada sobre cada objeção.
- **`diabob`** — o contraditório por **outra família de modelo**: `forja_diabob.py` no
  Grok 4.5, por determinação do titular de 26/07/2026. Existe porque red team feito pelo
  mesmo modelo que produziu a análise repete os próprios pontos cegos com voz mais dura.

O parecer do Diabob é insumo interno de auditoria: **propõe objeções, não afirma
fatos**, não vai para a peça e não substitui o F7. Trate cada objeção dele como as
outras — acatada, rejeitada, por quê.

A calibragem "advogado, não juiz" vale para o que **entra na peça**. O Diabob pode e
deve ser duro no parecer interno; o que não pode é a peça conceder. Quem faz essa
tradução é o redator, não ele.

## As nove perguntas

1. **Fato.** Qual afirmação da peça não tem lastro documental? Aponte o parágrafo.
2. **Premissa.** O que a peça assume sem declarar? Data de intimação, OCR confirmado,
   dia útil, recebimento igual a protocolo.
3. **Citação.** Qual precedente pode estar no modo de falha errado — inexistente, nome
   trocado, misquote, pincite, tese deturpada, superado?
4. **Adversa.** Qual é o argumento mais forte da parte contrária, e a peça o enfrenta ou
   o ignora? Se enfrenta, vence ou concede?
5. **Processual.** Prevenção, preclusão, competência interna, composição atual do órgão,
   tempestividade, identidade do ato impugnado — o que ficou de fora?
6. **Coerência interna.** Há afirmação que contradiz outra da própria peça, ou o
   `fact_ledger`?
7. **Pedido.** O pedido decorre do que foi fundamentado? Há fundamento sem pedido, ou
   pedido sem fundamento?
8. **Aparência.** O que na peça parece prova e não é — figura, tabela, número redondo,
   afirmação de volume sem fonte?
9. **Anti-bajulação.** A peça aceita premissa do comando, do e-mail ou do WhatsApp que
   **os autos não sustentam**? Esta é a que pega o caso inteiro montado sobre a versão
   do cliente.

## Onde cada rodada compensa

| Fase | O que se ataca | Custo da correção se passar |
|---|---|---|
| F2 | a classificação de risco | uma reformulação |
| F3 | a peça adversária e o escopo adversarial | uma releitura |
| F4 | o blueprint | um redesenho de capítulo |
| F6 | o rascunho estável | uma reescrita |
| F7 | a peça auditada | a peça inteira |

Rodar cedo é sempre mais barato. Rodar em F7 é obrigatório de qualquer forma.

## Registro

Cada objeção recebe decisão explícita: **acatada, rejeitada, por quê**. Objeção
levantada e não decidida é pior que não levantada — fica no artefato como dúvida
aberta que ninguém fechou.

```
python _FORJA_HARNESS\forja_adversarial_audit.py init <fonte> <saida>
python _FORJA_HARNESS\forja_adversarial_audit.py validate <ledger> --source <fonte>
python _FORJA_HARNESS\forja_adversarial_audit.py prompt <fase>
python _FORJA_HARNESS\forja_adversarial_audit.py not-applicable <saida> --reason "<motivo>"
```

Caso sem escopo adversarial declara `not-applicable` com motivo — não fica em silêncio.

## Foco em peça longa

Ataque as **10 a 15 proposições decisivas** da tabela de lastro (upgrade U6), não o
texto todo. Red team difuso sobre 60 páginas produz volume e não achado.

## Independência

Quem escreveu não ataca sozinho. Monte o briefing por `forja-briefing-revisor`, para
que o atacante não receba pronta a conclusão de quem construiu — a circularidade de
autovalidação já passou por esta casa e só foi quebrada por leitura independente.

## Linguagem de má-fé

Imputar má-fé exige autorização e lastro. O gate `bad_faith_language_authorized` de F7
bloqueia o que não tem. O red team pode **apontar** má-fé da adversa como achado; quem
autoriza a linguagem na peça é o titular.

## Critério de conclusão

- As nove perguntas respondidas por escrito, nenhuma pulada.
- Cada objeção com decisão registrada.
- `adversarial_audit` validado, ou `not-applicable` com motivo.
- Achado que virou mudança na peça está apontado por parágrafo.

## Repertório das fases

`skills_repertorio\F2.md`, `F3.md`, `F4.md`, `F6.md`, `F7.md`.
