---
name: forja-revisao-cruzada
description: 'Executar a revisão cruzada entre famílias de modelo que é gate de produção da FORJA — o trabalho nasce no Claude ou no Codex e a outra família revisa —, devolvendo producerModel, reviewerModel e o motivo quando a segunda família está indisponível. Use ao fechar F7, ao resolver cross_model_review_verified em unverified e ao decidir quem produz e quem revisa em F6. Diferencial: codex-integrado é o transporte e inteia-review-iterativo é o protocolo genérico; esta amarra os dois ao contrato do run, onde familyAssurance é recomposto pelo orquestrador e nunca aceito por declaração.'
metadata:
  adaptada_de: [codex-integrado, inteia-review-iterativo]
  fases: [F6, F7]
  contrato: phase_contracts/F7.json
  criada_em: 2026-08-06
---

# Revisão cruzada entre famílias — gate de produção

## A regra

O trabalho pode nascer no Claude ou no Codex, mas **a outra família revisa**. O contrato
do run declara `producerModel` e `reviewerModel`; o campo `familyAssurance` assume:

| Valor | Significa | Efeito no gate |
|---|---|---|
| `cross_family` | produtor e revisor de famílias diferentes | libera em qualquer modo |
| `cross_session_same_family` | mesma família, sessões distintas | libera fora de `strict_protocol` |
| `unverified` | não comprovado | **bloqueia sempre** |

**`familyAssurance` é recomposto pelo orquestrador e nunca aceito por declaração.**
Declarar não é comprovar — esta é a diferença que a skill genérica não conhece.

## Degradação é permitida; silêncio não

Se a segunda família estiver indisponível, **o trabalho interno continua** e rebaixa
para `cross_session_same_family` **com o motivo registrado**. Não confunda: continuar
trabalhando não é continuar liberando — em `strict_protocol`, só `cross_family` libera,
e o caso rebaixado fica com a **promoção bloqueada** até a outra família revisar.

O que é proibido é chegar em `unverified` sem dizer por quê, ou declarar `cross_family`
sem execução.

## Sequência

1. **Em F6**, decida quem produz. Se o redator foi o Claude, o revisor é o Codex — e
   vice-versa. Decidir isso cedo evita improviso na auditoria.
2. **Em F7**, monte o briefing por `forja-briefing-revisor`: o revisor **não** recebe a
   conclusão de quem construiu, recebe o material e a pergunta.
3. Execute a revisão pela outra família (`codex-integrado` quando o revisor é o Codex).
4. **Confirme que o revisor leu os arquivos.** Ver armadilhas abaixo.
5. Registre `producerModel`, `reviewerModel`, o `familyAssurance` alcançado e, se
   houve rebaixamento, o motivo.
6. Deixe o orquestrador recompor. Não escreva o campo à mão.

**Esta skill não é o único caminho.** O que o gate exige é a **evidência recomputável**
de revisão independente. Qualquer executor que a produza serve; estas são as rotas
conhecidas e testadas, não uma exclusividade.

## Armadilhas conhecidas do Codex no Windows

Estão na memória do projeto e já custaram uma rodada:

- **stdin trava.** Não alimente por stdin.
- **pipe derruba** a execução em lote.
- **O executor às vezes não lê o workspace** — e então devolve **parecer sem fonte com
  cara de parecer**: bem escrito, bem estruturado, sobre nada. Antes de aceitar o
  veredito, confira que ele citou trecho real dos arquivos.

Um parecer que não cita o material não é revisão. Rejeite e reexecute.

## O protocolo iterativo

Herdado do `inteia-review-iterativo`: o **primeiro round de fix cria regressões maiores
que o bug original**. Em mudança de sistema — script, gate, contrato, template — a
revisão é iterativa: fix, revisão independente, fix do que a revisão apontou, nova
revisão. Não pare no primeiro verde.

## Por que este gate existe

Lição 99, 03/08/2026: o comitê de personas leu o dossiê do construtor e recomendou
arquitetura já rejeitada, citando função inexistente. A circularidade de autovalidação
— quem constrói escreve o gate, mede com ele e se aprova — **só foi quebrada pela
revisão cruzada com a outra família de modelo, lendo o XML**.

Comitê de personas não substitui revisão de código. Nem revisão de outra família.

## Limites do que este gate prova

Os gates automáticos são escudos lexicais e estruturais. Eles **não** provam
equivalência semântica nem substituem a auditoria F7 e a revisão humana. Revisão
cruzada verde com peça errada é possível — o gate mede que houve revisão independente,
não que a peça está certa.

## Critério de conclusão

- `producerModel` e `reviewerModel` declarados no contrato do run.
- `familyAssurance` recomposto pelo orquestrador, não escrito à mão.
- Se rebaixado, motivo registrado.
- Parecer do revisor citando trecho real do material.
- `cross_model_review_verified` satisfeito.

## Repertório das fases

`_FORJA_HARNESS\skills_repertorio\F6.md` e `F7.md`.
