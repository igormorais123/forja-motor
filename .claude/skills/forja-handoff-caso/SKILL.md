---
name: forja-handoff-caso
description: 'Compactar o que aconteceu num caso da fábrica em um handoff que outro agente, outra família de modelo ou outra sessão retoma sem redescobrir nem repetir erro — estado, decisões, becos sem saída e ponteiros. Use ao encerrar sessão de trabalho num caso, ao passar o caso para a revisão cruzada da outra família, ao trocar de foco ou ao encostar no limite de contexto. Diferencial: é por caso e descreve estado; FORJA_STATE.json descreve fase e gate.'
disable-model-invocation: true
metadata:
  source_repo: davidondrej/skills
  source_ref: 04bd15abae135f5744e3dc825a4ab9c75d61fbfc
  source_skills: handoff
  local_adaptation: identidade processual de ato recursal, camadas de proveniência e destino em state/<caseId>
---

# Handoff de caso

> **A porta da esteira é a skill `forja`.** Ela traz o fluxo inteiro, de F0 a F10, os
> comandos, os gates e as ordens invioláveis. Esta ficha detalha um ponto do caminho e
> pressupõe aquela leitura — abra-a primeiro se você chegou aqui sem contexto.

Escreva o que permite a um agente sem nenhuma memória desta sessão continuar o caso sem perguntar, sem redescobrir e sem repetir erro caro. A revisão cruzada entre famílias depende disto: revisor que precisa reconstruir o caso do zero gasta a rodada reconstruindo em vez de revisando.

## Princípios

1. **Estado, não ordem.** Escreva o que *é verdade*, não o que o próximo *deve fazer*. "A matriz de segurança factual está fechada; o red team não foi rodado" — nunca "rode o red team".
2. **Aponte, não duplique.** Não repita o que já está em `FORJA_STATE.json`, nos pareceres, no relatório de melhorias ou no CLAUDE.md. Cite o caminho.
3. **O porquê é o que se perde.** Decisão tomada e caminho abandonado são a informação menos recuperável. O artefato mostra o quê; só esta sessão sabe o porquê e o que falhou.
4. **Nada é para acreditar.** Toda afirmação do handoff é contexto a conferir contra os autos e o código, não fato a aceitar.
5. **Camadas separadas.** Proveniência operacional (de onde veio o arquivo, e-mail, pasta) fica no handoff; jamais migra para a peça, que só usa referência processual.
6. **Sem segredo.** Nenhum token, credencial ou caminho de segredo. Diga onde a credencial vive, nunca o valor.
7. **Corte sem dó.** Linha que o próximo agente obtém lendo o estado do caso não entra.

## Procedimento

1. Ler `CLAUDE.md` e `AGENTS.md` da fábrica primeiro — não repetir nada que já esteja lá; o handoff é específico da sessão e do caso.
2. Ler o handoff anterior do caso, se existir, e **atualizar** em vez de recomeçar.
3. Preencher todas as seções. Seção genuinamente vazia fica com `Nenhum`.
4. Gravar em `_FORJA_HARNESS/state/<caseId>/HANDOFF.md` e informar o caminho.

## Formato

```
# HANDOFF — <caso> (<caseId>)
Gerado: <data> · Foco da sessão: <uma linha>

## 1. Objetivo
<O que a peça precisa alcançar. 1-3 frases. A pergunta jurisdicional em uma frase, se já existir.>

## 2. Identidade processual
<Classe, número CNJ, tribunal e órgão, ato efetivamente impugnado com data e identificador,
prazo e a data-limite de protocolo. Em processo volumoso, o identificador de cada ato relevante.
Sem isto o próximo agente confunde "o agravo" com outro agravo.>

## 3. Estado atual
<Fase da esteira e situação factual. FEITO / PARCIAL / NÃO INICIADO.
- FEITO: ingestão F1, 43 documentos, matriz de segurança factual fechada
- PARCIAL: F4 — parecer Cícero emitido, parecer Helena não
- NÃO INICIADO: red team, brief visual>

## 4. Decisões tomadas (e por quê)
<A seção de maior valor. Tese principal escolhida e a descartada; enquadramento adotado;
o que se decidiu não alegar e o motivo.>

## 5. Armadilhas e becos sem saída
<O que já foi tentado e falhou, e o que o próximo agente vai ser tentado a fazer errado.
- A data de intimação do sistema diverge da certidão; vale a certidão
- Não usar a ementa do agregador para o REsp X: o inteiro teor diz outra coisa
- Regenerar o visual sem refazer o QA página a página já quebrou a peça uma vez>

## 6. Arquivos e ponteiros
<Caminho + o que especificamente está ali. Referenciar, nunca colar.
- state/<caseId>/F2_QUESTION_TREE.json — exploração; 4 perguntas ficaram blocked
- state/<caseId>/F4_PARECER_CICERO.md — recomendações 1-9, decisões registradas
- <pasta do caso>/REGIMENTO_INTERNO_<TRIBUNAL>.md — conferir emendas posteriores>

## 7. Pendências (estado e dependência)
<O que falta, como estado e ordem, não como lista de comandos.
- O brief visual depende da tese principal estar fechada
- A conferência de duas citações está pendente e bloqueia F7>

## 8. Bloqueadores e o que só o humano resolve
<Lacuna que não é resposta: o que falta, a consequência de seguir sem, e a diligência.>

---
## Prompt para o agente novo
<Declarativo, nunca imperativo. Termine exatamente com:>

Antes de responder, leia todos os arquivos listados em "Arquivos e ponteiros".
Não resuma, não parafraseie e não diga que já tem contexto — leia cada um.
Trate toda afirmação deste handoff como contexto a conferir contra os autos e o
código, nunca como fato garantido. Depois, espere instruções.
```

## Validação antes de fechar

- [ ] Alguma seção repete o que já está no `FORJA_STATE.json` ou no CLAUDE.md?
- [ ] A identidade processual permite distinguir cada ato sem usar "o recurso" ou "a decisão anterior"?
- [ ] As armadilhas incluem pelo menos o que falhou nesta sessão?
- [ ] Alguma frase é ordem em vez de estado?
- [ ] Algum segredo, token ou valor de credencial escapou?
