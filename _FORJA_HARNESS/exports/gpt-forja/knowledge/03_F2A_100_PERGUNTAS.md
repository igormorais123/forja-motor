# F2A — Exploração do problema em 100 perguntas

## Quando aplicar

Aplicar a todo caso novo ou reconstrução ampla, depois do inventário e da leitura inicial e antes de pesquisa, conselho, blueprint ou redação.

## Resultado

Gerar exatamente 100 perguntas adaptadas ao caso, sem duplicatas: 10 perguntas em cada ótica. Cada pergunta deve ter âncora específica, relevância, resposta substantiva ou bloqueio honesto, classificação epistemológica e identificadores de suporte quando factual.

## Dez óticas canônicas

1. `mandato_resultado`: o que foi pedido, qual é o problema real e qual resultado é alcançável?
2. `fatos_cronologia`: o que ocorreu, em que ordem e qual fato muda a conclusão?
3. `prova_fontes`: o que sustenta cada premissa e onde está a ponte exata?
4. `processo_competencia`: qual ato, veículo, órgão, prazo, cognição e pedido são cabíveis?
5. `direito_precedentes`: que regra decide e quais são seus limites, regimes e precedentes contrários?
6. `adversario_julgador`: qual é a melhor objeção e o caminho mais estreito para negar o pedido?
7. `riscos_etica_impactos`: que danos à tese, ao cliente e à posição futura precisam ser controlados?
8. `alternativas_solucoes`: que intervenções concorrentes existem e quando trocar de estratégia?
9. `quantificacao_execucao`: o que precisa ser calculado, obtido, aprovado e comprovadamente entregue?
10. `comunicacao_visual_validacao`: como tornar decisão, prova, limites e testes imediatamente compreensíveis?

## Regras

- A pergunta-semente deve ser reescrita com atos, datas, documentos, pedidos e tensões do caso.
- Não responder por memória ou apenas para completar 100.
- Fonte ausente gera `blocked` + `not_verified` + consequência + diligência.
- Declaração do usuário permanece `office_declaration` até confirmação independente.
- Inferência jurídica e hipótese estratégica não recebem linguagem de certeza factual.
- Questão material bloqueada segue para pesquisa e impede redação externa.
- Produzir ao menos duas hipóteses de solução, com condições, riscos e perguntas que as sustentam.
- Consolidar definição do problema, diagnóstico e handoff para fontes, estratégia, pesquisa, redação e auditoria.

## Forma recomendada do item

```json
{
  "id": "Q-001",
  "lens": "mandato_resultado",
  "question": "Pergunta específica do caso",
  "caseAnchor": "ato, documento ou tensão concreta",
  "whyItMatters": "consequência jurídica ou estratégica",
  "answerStatus": "answered | blocked",
  "epistemicClass": "source | office_declaration | inference | not_verified",
  "answer": "resposta ou descrição honesta da lacuna",
  "supportIds": ["SRC-001"],
  "consequence": "impacto da resposta ou da falta",
  "diligence": "próxima verificação objetiva"
}
```

## Comunicação com o usuário

Não obrigar o usuário a ler as 100 perguntas no chat. Apresentar primeiro:

- problema consolidado;
- cinco a dez bloqueadores realmente materiais;
- duas ou mais soluções;
- diligências que mudam a decisão;
- oferta do arquivo completo quando útil.

