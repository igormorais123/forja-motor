# F2-A — Exploração problematizadora em 100 perguntas

**Natureza:** artefato interno. Nunca copiar perguntas, rótulos epistemológicos, caminhos ou proveniência operacional para a peça protocolável.

**Quando executar:** em todo caso novo vindo de e-mail, WhatsApp/Hermes ou comando manual, depois da ingestão segura, inventário e leitura dos documentos e antes de pesquisa, conselho, blueprint ou redação.

## Resultado obrigatório

Produzir `F2_QUESTION_TREE.json` com `protocolVersion: FORJA-F2A-100-v1`:

- exatamente 100 perguntas adaptadas ao caso, sem duplicatas;
- 10 perguntas em cada uma das 10 óticas canônicas;
- resposta substantiva para cada pergunta ou bloqueio honesto com consequência;
- `caseAnchor` e `whyItMatters` específicos;
- natureza epistemológica da resposta;
- `supportIds` para resposta factual, processual, jurisprudencial ou numérica;
- pelo menos duas hipóteses de solução, com condições, riscos e perguntas que as sustentam;
- síntese diagnóstica e definição do problema;
- handoff explícito para F3, F4, F5, F6 e F7;
- `draftRelease: blocked` enquanto houver questão material bloqueada.
- envelope N4 coerente: fontes registradas, produtor/revisor independentes, `status` e `contentHash` recalculados antes da promoção.

## Dez óticas canônicas

| Ótica | Pergunta-mãe |
|---|---|
| `mandato_resultado` | O que foi pedido, qual problema real existe e qual resultado é alcançável? |
| `fatos_cronologia` | O que ocorreu, em que ordem e qual fato muda a conclusão? |
| `prova_fontes` | O que sustenta cada premissa e onde está a ponte exata? |
| `processo_competencia` | Qual ato, veículo, órgão, prazo, cognição e pedido são cabíveis? |
| `direito_precedentes` | Que regra decide e quais são seus limites, regimes e precedentes contrários? |
| `adversario_julgador` | Qual é a melhor objeção e o caminho mais estreito para negar o pedido? |
| `riscos_etica_impactos` | Que danos à tese, ao cliente e à posição futura precisam ser controlados? |
| `alternativas_solucoes` | Que intervenções concorrentes existem e quando trocar de estratégia? |
| `quantificacao_execucao` | O que precisa ser calculado, obtido, aprovado e comprovadamente entregue? |
| `comunicacao_visual_validacao` | Como tornar decisão, prova, limites e testes imediatamente compreensíveis? |

## Regras de resposta

1. A pergunta-semente é ponto de partida; reescrevê-la com nomes de atos, pedidos, datas, documentos e tensões do caso.
2. Não responder por memória ou para “fechar 100”. Se a fonte não existir, usar `blocked` + `not_verified` + consequência + rota de diligência.
3. Declaração do comando não vira fato dos autos. Usar `office_declaration` até confirmação independente.
4. Inferência jurídica e hipótese estratégica devem ser nomeadas como tal; não recebem linguagem de certeza factual.
5. Questão material bloqueada segue para F3/F5 como pendência e bloqueia F6; ela não desaparece do mapa.
6. F3 usa perguntas sobre fontes, fatos, atos, prazos e direito; F4 usa problema, objeções, riscos e alternativas; F5 recebe pesquisas; F6 recebe apenas afirmações autorizadas; F7 transforma perguntas materiais em testes.

## Comandos locais

```powershell
python forja_exploracao_100.py init --case-id <caseId> --case-anchor "<processo/ato/produto>" --output <attempt>\F2_QUESTION_TREE.json
python forja_exploracao_100.py validate <attempt>\F2_QUESTION_TREE.json
```

O arquivo criado por `init` é um envelope N4 em `draft`, deliberadamente bloqueado e com marcadores de andaime. Ele só passa após adaptação, respostas, lastro, síntese, hipóteses, handoff, fontes registradas, revisão independente e recálculo do `contentHash`.
