# W2A — cocriação F2-B em sombra

**Data:** 25/07/2026
**Protocolo:** `FORJA-F2B-DIALECTIC-v1`
**Escopo:** núcleo que vale nos dois cenários de Helena. Ela condicionou a *extensão* de F2-B ao resultado da consulta da Onda −1, não o início: o que foi construído aqui — seleção, política de silêncio, renderização e ledger — é necessário tanto no cenário completo quanto no reduzido aos Blocos 1 e 5.

---

## A regra que separa cocriação de incômodo

A subfase existe porque o titular determinou que a IA não deve "matar no peito e entregar pronto". Mas perguntar não é virtude por si: **cada pergunta enviada custa atenção de um advogado ocupado**, e pergunta redundante gasta esse crédito sem devolver decisão.

Daí a regra central: **não se pergunta o que o acervo já responde.** Uma pergunta só entra na consulta se estiver aberta, for material, tiver âncora no caso, tiver autoridade humana competente, declarar política de silêncio com consequência concreta — e não houver fonte registrada que já a responda.

## 1. Seleção determinística

A ordem não é arbitrária nem alfabética: identidade do produto primeiro (erra-se cedo e caro), depois risco factual e de autorização (porque bloqueia), depois rota, depois dependências downstream, e o ID como desempate. Duas execuções sobre a mesma árvore produzem a mesma consulta — há teste que embaralha a entrada e compara.

**Nada é truncado.** Acima de doze perguntas, emite-se `FAL-F2B-QUESTION-VOLUME` como P1 e exige-se justificativa da rodada. Cortar perguntas materiais para caber num número é esconder trabalho, não organizá-lo.

## 2. Política de silêncio — e o que nunca admite padrão

Toda pergunta declara o que acontece se não for respondida: `block_dependent`, `keep_options_open`, `explicit_reversible_default` ou `not_applicable`.

**Fato, prova e autorização nunca admitem valor padrão.** Presumir fato é inventar; presumir autorização é agir sem mandato. Os dois ou têm resposta, ou bloqueiam — `FAL-F2B-FACT-DEFAULT`, com teste para cada um dos três tipos. Estratégia e apresentação podem ter padrão reversível declarado, e é isso que permite ao caso seguir sem resposta.

## 3. Declaração do escritório não vira fato

`office_declaration` é natureza epistemológica legítima e resolve questões de objetivo, estratégia e autorização. Mas quando responde questão **factual** sem `supportIds`, o validador acusa `FAL-F2B-OFFICE-AS-FACT`.

É o modo mais silencioso de inventar: alguém confiável afirma algo, a afirmação vira premissa, e a premissa vira fato na peça sem nunca ter passado por documento.

## 4. Renderização — e um defeito meu que vale registrar

O renderizador não responde, não reordena por conveniência, recusa pergunta sem consequência declarada, grava o hash do texto no artefato e **nomeia o que ficou de fora, com o motivo**, para que quem revisa possa discordar da triagem.

Na primeira versão usei `_norm()` para compor o texto — função que dobra a caixa e remove diacríticos **para efeito de comparação**. A consulta saiu com o texto mutilado: sem acentuação, sem maiúsculas e sem pontuação, com cifras e datas desmontadas em dígitos soltos. Seria constrangedor chegar assim ao titular.

Corrigido com `_texto()`, definido ao lado do outro e com a distinção documentada, mais teste que verifica acentuação, caixa e pontuação preservadas na saída. **O defeito só apareceu porque rodei a renderização de verdade** em vez de confiar no teste estrutural — que passava.

## 5. Ledger append-only

Uma decisão registrada é o rastro de que alguém respondeu algo em determinado dia. Corrigir apagando destrói a trilha; corrigir é acrescentar. Registrar a mesma `decisionId` duas vezes levanta erro.

Resposta parcial mantém a pendência visível: o status vira `partially_answered` e `remainingQuestionIds` lista o que falta. Dar a consulta por respondida com pendência é `FAL-F2B-PARTIAL-CLOSED`.

**Envio autônomo continua proibido.** `outboundPolicy` diferente de `manual_review_only` é recusado, e consulta marcada como enviada sem recibo humano também.

## 6. Limpeza de estado que enfraquecia um gate

O TDD mandava remover ou versionar os estados `retired` e `accepted_by_human`. Verifiquei antes de decidir: **treze árvores reais, 1.096 perguntas `answered` e 14 `blocked` — nenhuma usa os dois estados.** Eram código morto, e ali código morto tinha custo: uma questão material marcada `retired` escapava do `N4-Q-UNRESOLVED`.

Removi. E ao remover apareceu uma lacuna maior: pergunta **não material** com estado inválido não passava por exame algum. Fechei com `N4-Q-STATUS`, que agora vale para toda pergunta, material ou não. A regra ficou mais forte do que era antes da limpeza.

O teste que cobria o comportamento antigo foi substituído por dois: um que recusa três estados fora do contrato, outro que confirma que os três canônicos passam.

## 7. Verificação

```
python forja_baseline.py → 37/37 suítes · 389 testes · APROVADO
fluxo completo executado  → seleção, render, resposta parcial, segunda rodada
```

Baseline: 361 → 389 testes. Uma regressão apareceu no caminho (`test_retired_question_keeps_reason`) e foi resolvida corrigindo o contrato, não o teste.

## 8. O que continua condicionado

A extensão de F2-B — quantos blocos temáticos, quantas rodadas, qual tom — depende do resultado da consulta real da Onda −1. Se a resposta não vier ou não for útil, o escopo encolhe para os Blocos 1 e 5, conforme o cenário pessimista de Helena. **O núcleo construído aqui serve aos dois.**

Próxima onda: **W3 — signature brief, pesquisa jurídica e âncoras**, que traz as emendas E7 (vigência em quatro estados), E8 (`precedenteContrarioConhecido[]`) e E13 (regime como convenção interna).
