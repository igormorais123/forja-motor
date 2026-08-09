---
name: forja-briefing-revisor
description: 'Montar o briefing de um revisor independente da fábrica — conselho Helena/Cícero, Diabob, red team, revisão cruzada entre famílias de modelo, auditoria de segunda opinião — de modo que ele não receba pronta a conclusão de quem construiu. Use ao acionar parecer, conselho de personas, revisão cruzada, red team ou qualquer segunda opinião sobre peça, gate ou arquitetura. Diferencial: rege a MONTAGEM do briefing; forja_conselho.py valida o parecer depois de pronto.'
metadata:
  source_repo: davidondrej/skills
  source_ref: 04bd15abae135f5744e3dc825a4ab9c75d61fbfc
  source_skills: launch-subagent, gpt-review, fable-review
  local_adaptation: conselho Helena/Cícero/Diabob, revisão cruzada entre famílias e anticircularidade da lição 87-99
---

# Briefing de revisor independente

> **A porta da esteira é a skill `forja`.** Ela traz o fluxo inteiro, de F0 a F10, os
> comandos, os gates e as ordens invioláveis. Esta ficha detalha um ponto do caminho e
> pressupõe aquela leitura — abra-a primeiro se você chegou aqui sem contexto.

Existe por uma falha medida nesta casa (lição 87-99 de `_FORJA_HARNESS/RETROSPECTIVAS.md`): o conselho leu o dossiê do construtor, recomendou arquitetura já rejeitada e citou função inexistente. Quem constrói escreveu o gate, mediu com ele e se aprovou. A circularidade só quebrou quando a outra família de modelo leu a fonte primária em vez do resumo.

O revisor não é independente por ser outro modelo. É independente pelo que o briefing **não** contém.

## Antes de escrever o briefing — verificar estado

1. Existe parecer anterior da mesma persona neste caso (`_FORJA_HARNESS/state/<caseId>/F4_PARECER_*.md`)? Se sim, o revisor lê o dele, não o do construtor.
2. Existe decisão já registrada sobre o tema (ver skill `forja-adr`)? Se sim, o briefing declara a decisão e o motivo, para o revisor poder atacá-la com fato novo — nunca para redescobri-la do zero.
3. A fonte primária está acessível ao revisor (autos, XML do DOCX, código, JSON de gate)? Se não estiver, o briefing não sai: revisor sem fonte primária só pode concordar.

## Regras de montagem

- **O revisor começa cego.** Ele não vê o seu contexto. Escreva escopo, fatos, restrições e formato de saída por inteiro. Nada de "como discutimos".
- **Fonte primária, não resumo.** Aponte arquivo e trecho: os autos, o XML do documento, o `.py` do gate, o JSON do run. Dossiê do construtor entra, no máximo, como anexo declarado — nunca como leitura de partida.
- **Não empurre a solução.** Diga o que revisar, não o que encontrar. Proibido: "confirme que X está correto", "veja se concorda com a abordagem Y". Permitido: "o objetivo é Z; a implementação atual está em W; encontre o que falha".
- **Separe fato de tese.** No briefing, o que foi conferido em fonte vai como fato com a ponte; o que é interpretação do construtor vai rotulado como tese a testar.
- **Uma missão por revisor.** Revisor paralelo não toca o mesmo artefato de outro. Particione por dimensão (juridicidade, estratégia, forma, risco processual) ou mantenha em um só.
- **Saída curta e acionável.** Achados numerados com severidade, ponte para o arquivo e o que muda se estiver certo. Nunca transcrição, nunca dump de arquivo.
- **Peça o contraditório explícito.** Toda pauta inclui: "qual premissa do comando ou do e-mail os autos NÃO sustentam?" (a 9ª pergunta anti-bajulação do red team) e "o que aqui está certo pelo motivo errado?".
- **Declare o que já foi rejeitado.** Sem isso o revisor gasta a rodada reabrindo RAG, visual 3D ou integração do `compor()` no render.

## Esqueleto do briefing

```
OBJETIVO: <o que a peça/gate/arquitetura precisa alcançar, 1-2 frases>
ARTEFATO A REVISAR: <caminho exato> (linhas/páginas relevantes)
FONTE PRIMÁRIA OBRIGATÓRIA: <autos, XML, código, JSON — caminhos>
FATOS CONFERIDOS: <cada um com a ponte para a fonte>
TESES DO CONSTRUTOR (a testar, não a aceitar): <lista>
JÁ DECIDIDO / JÁ REJEITADO (não reabrir sem fato novo): <lista + motivo>
FORA DE ESCOPO: <o que não é para revisar>
SAÍDA: achados numerados <severidade | onde | o que falha | consequência se real>
PERGUNTAS OBRIGATÓRIAS: 1) que premissa os autos não sustentam? 2) o que está
certo pelo motivo errado? 3) que evidência mudaria a sua conclusão?
```

## Checklist anti-contaminação (rodar antes de disparar)

- [ ] O briefing afirma alguma conclusão que é justamente o que se quer verificar?
- [ ] Alguma frase sugere a resposta esperada ("apenas confirme", "deve estar ok")?
- [ ] O revisor recebe fonte primária ou só o resumo de quem construiu?
- [ ] Há mais de uma missão no mesmo briefing?
- [ ] O formato de saída está fixado?
- [ ] A pauta inclui as três perguntas obrigatórias?
- [ ] Se paralelo: dois revisores tocam o mesmo artefato?

Qualquer "sim" nas quatro primeiras, ou "não" nas duas seguintes, reprova o briefing — reescreva antes de disparar.

## Depois do parecer

O achado do revisor é hipótese, não veredito. Confira cada um contra a fonte antes de acatar, e registre a decisão (acatada / rejeitada / por quê) no artefato do caso — é o que `forja_conselho.py` valida. Achado que você rejeitar sem conferir na fonte é autovalidação com um passo a mais.

Revisão cruzada entre famílias: o campo `familyAssurance` é recomposto pelo orquestrador, nunca aceito por declaração. Briefing bem montado com revisor da mesma família ainda é `cross_session_same_family` — e o motivo da degradação vai registrado.
