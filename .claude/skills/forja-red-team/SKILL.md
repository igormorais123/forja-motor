---
name: forja-red-team
description: 'Atacar por escrito o blueprint ou a peça da FORJA com as nove perguntas estruturadas do protocolo, incluindo a nona, anti-bajulação — a peça aceita premissa do comando ou do e-mail que os autos não sustentam? Use ao classificar risco em F2, auditar peça adversária em F3, fechar o blueprint em F4 e satisfazer red_team_completed em F7. Diferencial: diabob é contrarian genérico e, aplicado cru a caso de cliente, produz texto que concede; esta carrega a calibragem advogado-não-juiz e registra a decisão sobre cada objeção.'
metadata:
  adaptada_de: [diabob]
  fases: [F2, F3, F4, F6, F7]
  criada_em: 2026-08-06
---

# Red team — as nove perguntas

Estruturado e **por escrito**. Não é a impressão de que o texto está bom.

## A calibragem que a versão genérica não tem

**Advogado, não juiz.** Diretriz escrita do titular, 06/08/2026. Risco, objeção e
precedente contrário são **identificados e enfrentados** — inclusive por distinção
tecnicamente sustentável — e jamais adotados nem antecipados como juízo desfavorável ao
cliente.

Lê-se junto com a regra de enfrentar a objeção mais forte da adversa: **enfrentar serve
para vencer, não para conceder**. Isoladas, as duas se degradam — uma vira otimismo
cego, a outra vira parecer contra o próprio cliente.

O Diabob genérico é contrarian por construção. Aplicado cru a caso de cliente, ele
produz texto que concede. Use esta versão.

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
