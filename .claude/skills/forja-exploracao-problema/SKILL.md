---
name: forja-exploracao-problema
description: 'Conduzir a exploração inicial obrigatória em 100 perguntas (subfase F2A da FORJA) com as técnicas de Van Aken e Berends adaptadas a caso jurídico, recusando a pergunta de enchimento que existe só para bater a cota. Use ao abrir caso novo depois de F1 e antes de pesquisa, conselho, blueprint ou redação, e ao montar ou revisar F2_QUESTION_TREE.json. Diferencial: problem-solving-vila traz o método organizacional cru; esta produz a árvore no contrato FORJA-F2A-100-v1 com classificação epistemológica e lacuna declarada como bloqueio.'
metadata:
  adaptada_de: [problem-solving-vila]
  fases: [F2]
  contrato: templates/F2A_EXPLORACAO_100_PERGUNTAS.md
  validador: forja_exploracao_100.py
  criada_em: 2026-08-06
---

# Exploração do problema — F2A

Inviolável desde 14/07/2026. Todo caso novo recebido por e-mail, WhatsApp ou comando
manual passa por aqui **depois de F1 e antes** de pesquisa, conselho, blueprint ou
redação.

## O contrato

`F2_QUESTION_TREE.json` com contrato `FORJA-F2A-100-v1`: exatamente 100 perguntas
adaptadas ao caso, 10 em cada ótica canônica, cada uma respondida com classificação
epistemológica e lastro quando factual.

```
python _FORJA_HARNESS\forja_exploracao_100.py init --case-id <id> --case-anchor <ancora> --output <arquivo>
python _FORJA_HARNESS\forja_exploracao_100.py validate <arquivo>
```

Há ainda `select-consultation`, `render-consultation` e `record-response`, para o que
precisa ir ao humano. Use-os: pergunta que só o titular responde não vira inferência.

## O alerta que motivou esta skill

`DIAGNOSTICO_F2A_DEGRADACAO_2026-08-05.md` registra que o sistema de cota degrada.
**Pergunta preenchida para bater 100 é pior que pergunta ausente**, porque o validador
aprova e o gate `exploration_100_complete` fica verde sobre nada.

Portanto: a qualidade da pergunta é o produto. A contagem é consequência.

## Divergência primeiro, convergência depois

O erro é começar pela árvore. A ordem que funciona:

1. **Divergir** (Van Aken): listar tudo que pode estar em jogo sem filtrar — fatos,
   atores, prazos, riscos, hipóteses concorrentes, o que o cliente quer e o que o
   processo permite. Nesta etapa não se descarta nada.
2. **Convergir** (árvore de questões): organizar o que divergiu em perguntas
   mutuamente excludentes dentro de cada ótica, e coletivamente exaustivas na ótica.
3. **Responder**, classificando cada resposta.
4. **Fechar**: problema, diagnóstico, ao menos **duas** soluções e handoff para F3–F7.

## Classificação de cada resposta

| Classe | Significa | O que exige |
|---|---|---|
| `fato` | está nos autos | lastro: documento e localizador |
| `declaracao` | o cliente ou o escritório afirma | quem afirmou, quando, onde |
| `inferencia` | conclusão nossa | as premissas de que ela depende |
| `blocked` | não se conseguiu responder | consequência e rota de diligência |

**Lacuna não é resposta.** `blocked` é estado legítimo e declarado; resposta inventada
para não deixar campo vazio é o modo de falha que esta skill existe para impedir.
Questão material bloqueada impede peça protocolável — e está certo que impeça.

## As perguntas que a IA esquece

O diagnóstico transversal da casa é que a IA acerta o eixo jurídico e erra **por
omissão** nas cautelas de advogado sênior. Estas entram na árvore por obrigação, não
por lembrança:

- prevenção e preclusão
- competência interna do tribunal e do órgão
- **composição atual** da turma ou câmara, confirmada na fonte
- fato superveniente, e se pede capítulo autônomo
- prazo, com dupla contagem e sem sábado como dia útil
- identidade dos atos: quantos recursos, quantas decisões, qual está sendo impugnada
- o que a parte adversária vai alegar de mais forte

Para o repertório completo, a skill `advogado-sobrehumano` tem o catálogo — puxe a
seção de estratégia processual, não o arsenal inteiro.

## A pergunta que fecha a fase

**A pergunta jurisdicional, em uma frase.** Se ela não cabe numa frase, o blueprint de
F4 vai ser coleção de argumentos sem eixo. É gate do catálogo e o custo de respondê-la
é de minutos.

## Quando esta skill não vale o custo

- Caso continuação com `question_tree` válida da rodada anterior: herde por
  `forja-handoff-caso` e atualize o que mudou.
- Peça repetitiva de baixo risco: o template sozinho basta, e o custo em contexto desta
  skill é o mais alto do repertório.

## Critério de conclusão

- 100 perguntas adaptadas ao caso, 10 por ótica, nenhuma de enchimento.
- Toda resposta classificada; todo `blocked` com consequência e rota.
- Pergunta jurisdicional em uma frase.
- Pelo menos duas soluções desenhadas.
- `validate` sem erro, e o gate `answers_provenance_classified` satisfeito de fato, não
  por preenchimento.

## Repertório da fase

`_FORJA_HARNESS\skills_repertorio\F2.md`.
