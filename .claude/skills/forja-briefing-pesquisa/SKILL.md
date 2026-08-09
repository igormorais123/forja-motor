---
name: forja-briefing-pesquisa
description: 'Transformar uma necessidade vaga de pesquisa jurídica em um briefing único e autossuficiente, com barra de conclusão e rodada de lacunas, para entregar a um pesquisador humano, a um subagente ou à fase F3. Use quando for pesquisar jurisprudência, precedente, tese, alteração legislativa, emenda regimental ou histórico de órgão julgador. Diferencial: produz o pedido de pesquisa; a conferência de citação já pesquisada é do gate de citações.'
metadata:
  source_repo: davidondrej/skills
  source_ref: 04bd15abae135f5744e3dc825a4ab9c75d61fbfc
  source_skills: research-prompt
  local_adaptation: hierarquia de fontes jurídicas, seis modos de falha de citação e marcadores de auditoria da fábrica
---

# Briefing de pesquisa jurídica

> **A porta da esteira é a skill `forja`.** Ela traz o fluxo inteiro, de F0 a F10, os
> comandos, os gates e as ordens invioláveis. Esta ficha detalha um ponto do caminho e
> pressupõe aquela leitura — abra-a primeiro se você chegou aqui sem contexto.

O erro mais caro medido nas entregas reais não foi não achar julgado — foi achar e atribuir errado: frase real colada no precedente errado, nota de rodapé não localizável, tese confundida com *obiter dictum*. Briefing frouxo produz pesquisa que para no primeiro resultado plausível.

Meta: **um parágrafo** que alguém sem nenhum contexto do caso executa sem fazer uma única pergunta de volta.

## Antes de escrever

1. Ler o que já existe: `_FORJA_HARNESS/cache/fontes_oficiais/` (súmulas, temas, dispositivos compilados, com data de conferência). Pesquisa que o cache já responde não vira briefing.
2. Fixar a **pergunta jurisdicional em uma frase** — se ela não couber em uma frase, a pesquisa ainda não tem alvo.
3. Identificar o tribunal e a data de protocolo pretendida: regimento e composição do órgão valem na data do protocolo, não na data do arquivo.

## Regras do briefing

- **Um parágrafo.** Sem títulos, sem lista solta. Numere as subperguntas dentro do texto: (1), (2), (3) — de três a seis, uma missão só.
- **Abra explicando o caso a quem nunca ouviu falar dele**: o que se discute, em que fase, contra que decisão, e qual decisão do escritório a pesquisa informa.
- **Peça o trabalho, não o tema.** Dê alças de busca: recorte temporal, órgão, classe processual, tipo de fonte, e o critério de escolha entre resultados.
- **Hierarquia de fontes, nesta ordem:** repositório oficial do tribunal (inteiro teor) → publicação oficial (DJe, Diário) → cache de fontes oficiais da fábrica → repositório secundário. Blog, ementa solta de agregador e memória de modelo **não são fonte**; entram, quando muito, como pista a confirmar.
- **Verbatim obrigatório.** Toda proposição vem com o trecho copiado da fonte, não parafraseado.
- **Contradição não vira consenso.** Fonte que conflita com fonte fica separada em: confirmado / inferência / não resolvido. Rotule na saída com `[FONTE: …]`, `[INFERÊNCIA]`, `[VERIFICAR]` — marcadores de auditoria, que nunca chegam à peça.
- **Barra de conclusão.** Não parar na primeira resposta plausível: cada proposição decisiva corroborada em fonte primária independente; onde não houver, dizer que não há em vez de encher linguiça. Ausência em corpus amostral não prova inexistência — declare o corpus varrido.
- **Rodada de lacunas antes de fechar.** Autocrítica: o que ficou de fonte única, o que ficou contraditório, o que ficou sem verbatim. Nova rodada de busca sobre isso. Repetir até limpar.
- **Saída fixa, método livre.** Prenda o formato do achado; deixe o caminho da busca aberto.

## Formato obrigatório por achado

| Campo | Conteúdo |
|---|---|
| Identificação | classe, número, órgão julgador, relator, data de julgamento e de publicação |
| Localizador | link ou caminho da fonte oficial consultada |
| Verbatim | o trecho, copiado |
| Papel | *ratio decidendi* ou *obiter dictum* — dizer qual, e por quê |
| Vigência | superado, distinguido, mantido; se houver tema/súmula, qual |
| Por que importa | uma linha ligando à pergunta jurisdicional |

Sem os seis campos, o achado não entra na peça.

## Os seis modos de falha a fechar na redação

Todo achado passa depois pelo checklist nominal: julgado inexistente; nome/órgão trocado; *misquote*; *pincite* errado; tese deturpada (*ratio* × *dictum*); precedente superado. O briefing já pede os dados que fecham os seis — é para isso que a tabela acima tem esses campos, e não outros.

## Modelo

> [Uma a duas frases em português simples: quem é a parte, o que se discute, em que fase está e contra o quê.] Pesquisar [tema + marcos identificadores] para responder a uma pergunta: [a pergunta jurisdicional] — decisão que isso informa: [uso concreto na peça]. Levantar: (1) …; (2) …; (3) …; (4) …. Incluir [recorte]; excluir [o que não interessa]. Preferir inteiro teor do repositório oficial e publicação oficial; ementa de agregador e resumo secundário são pista a confirmar, nunca prova; se as fontes divergirem, separar confirmado, inferência e não resolvido em vez de forçar consenso. Não parar no primeiro resultado plausível: corroborar cada proposição decisiva em fonte primária independente e, onde não existir, dizer expressamente que não existe, declarando o corpus varrido. Antes de encerrar, fazer uma rodada de autocrítica listando fonte única, contradição e proposição sem verbatim, e nova busca para fechar cada uma, repetindo até limpar. Para cada achado, entregar identificação completa (classe, número, órgão, relator, data de julgamento e de publicação), localizador da fonte, o trecho verbatim, se é ratio ou obiter, situação de vigência e uma linha de por que importa. Só fato citável e conferível. Entregar tudo em um único arquivo markdown.

## Depois da pesquisa

O resultado alimenta a tabela de lastro das proposições decisivas do relatório de melhorias. Proposição decisiva sem os seis campos preenchidos é bloqueador — não se resolve na revisão de forma.
