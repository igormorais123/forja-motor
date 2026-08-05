<!-- mutacao: compress | eixo: converter redundâncias em gates únicos de entrada, lastro, redação e liberação | parent: baseline -->
# PROMPT — Fábrica de Melhoria de Petições

> Uso: abra o Claude Code na pasta do processo e cole este prompt.

/goal Produzir, sem sobrescrever originais, a versão definitiva, superpotencializada e diagramada da petição principal, fiel aos autos e ao padrão do escritório, com validação jurídica, factual e visual de 100% das páginas.

## MISSÃO E REGRA DE PARADA

Leia a pasta, reconstrua o caso, teste o lastro, defina a estratégia, redija, revise, gere DOCX/PDF e valide. Use o potencial máximo do Fable e das skills da Colmeia. Nenhum fato, número, data, valor, processo, autoridade, citação, precedente ou anexo pode ser inventado.

Peça bonita não é peça liberada. Insumo material ausente, fonte insuficiente ou pendência sem decisão mantém a saída como `internal_working`; nesse estado, entregue relatório interno, nunca DOCX/PDF chamado de final.

## GATE 1 — INGESTÃO, IDENTIDADE E COBERTURA

Antes de redigir:

1. Liste todos os arquivos e subpastas e classifique: original, alternativas de IA, provas, decisões, legislação, modelos, mídias, comunicações, produtos internos e externos.
2. Leia integralmente a original; extraia partes, juízo, tipo, pedidos, teses, fundamentos, prazos e padrão visual: cabeçalho, timbre, fonte, margens, rodapé, assinatura e endereçamento.
3. Leia as alternativas e faça diff do que acrescentam, perdem, alteram ou alucinam. Leia provas e decisões e registre o que cada fonte prova, não prova e onde se aplica.
4. Produza mapa interno: fatos, cronologia, teses, forças, fraquezas, decisão necessária, resposta adversária, questões laterais, lacunas e diligências.
5. Em processo volumoso, dê identidade a cada recurso, decisão, conversão, retratação, destaque e intimação: código, sujeito, data, classe/número, ato impugnado, pedido, resultado, efeito, relação cronológica e fl./evento/ID. Não prossiga enquanto “o agravo” ou “a decisão” for ambíguo.
6. Leia a íntegra do ato atual e reconstrua a cronologia completa. Conversão, retratação ou juízo positivo anterior vale só no alcance do inteiro teor e não substitui nova leitura.
7. Evento com mídia não é conteúdo lido. Confirme caminho, existência, abertura, correspondência e leitura. Mídia essencial não materializada é P1. Agrupe mensagens e áudios por rajada conversacional até a alta d’água antes de extrair pedido; complemento posterior pode corrigir o anterior.
8. Material humano novo e potencialmente adverso reabre as fases afetadas, recalcula hashes dos bytes e repete gates jurídico e visual.

### Proveniência e autoria

O ledger interno guarda origem, versão, canal, hash, caminho, página/ID e cadeia de custódia. A peça usa apenas ponte processual verdadeira: “e-STJ fl. X”, “evento/ID X”, “documento juntado aos autos”, “Doc. X” ou “documento anexo”. Juntada e anexação devem estar confirmadas.

É P0 vazar origem operacional ou mencionar externamente e-mail, WhatsApp, Drive, pasta, caminho, arquivo recebido, compartilhamento, minuta, hash, gate ou fase. Comando, mensagem, minuta humana ou texto de IA orienta busca; não prova fato.

Origem da mensagem não define autoria intelectual. Para tese adicionada, fortalecida, enfraquecida, reformulada ou removida, registre fonte, primeiro proponente, seleção, validação e decisão de incorporar, usando quando útil `human_original`, `human_selected`, `forja_generated`, `external_model_import`, `source_derived`, `mixed` ou `unknown`. Versão humana revisada exige diff jurídico e atributivo contra a última versão realmente enviada; autoria humana não dispensa lastro.

### Regimento

Identifique o tribunal por CNJ, endereçamento e decisões. Leia `REGIMENTO_INTERNO_<TRIBUNAL>.md`; se faltar, baixe a consolidação oficial mais recente, converta integralmente para `.md`, salve-a e acrescente emendas posteriores até a data da elaboração. Verifique competência, cabimento, processamento, prazos, sustentação e pauta. Leia também `_LEIS_GERAIS`, inclusive Lei 8.906/1994 e LC 35/1979. O relatório final indica os dispositivos que impactaram a peça.

## GATE 2 — EXPLORAÇÃO F2-A

Depois da ingestão integral e antes de pesquisa, conselho, blueprint ou redação, execute exatamente 100 perguntas do caso: 10 para cada ótica — mandato/resultado; fatos/cronologia; prova/fontes; processo/competência; direito/precedentes; adversário/julgador; riscos/ética/impactos; alternativas/soluções; quantificação/execução; comunicação/visual/validação.

Cada resposta contém âncora, importância, natureza epistemológica e fonte/localizador se factual, processual, jurisprudencial ou numérica. Sem prova, marque `blocked` + consequência + diligência; nunca invente para completar 100. Consolide problema, diagnóstico, ao menos duas soluções com condições/riscos, questões abertas e roteamento F3–F7.

Salve `_FORJA_HARNESS\state\<caseId>\n4_artifacts\F2_QUESTION_TREE.json`, protocolo `FORJA-F2A-100-v1`. Questão material bloqueia F6/DOCX/PDF, mas segue à F3/F5 como pendência. Siga `_FORJA_HARNESS\templates\F2A_EXPLORACAO_100_PERGUNTAS.md` e valide com `python _FORJA_HARNESS\forja_exploracao_100.py validate <arquivo>`.

## GATE 3 — LASTRO E ADMISSIBILIDADE

### Precedentes e fatos

Precedente `VERIFICADO` exige: identificador exato + fonte oficial nomeada/URL + trecho literal + local do trecho quando central. Identidade vaga ou memória nunca é verificação.

| Estado | Regra |
|---|---|
| `VERIFICADO` | pode entrar |
| `RESTRITO` | só rascunho com `[VERIFICAR: acesso restrito]`, ponte e verificação humana |
| `INDISPONÍVEL-TRANSITÓRIO` | só rascunho com marcador, tentativa datada e verificação humana |
| `NÃO-ENCONTRADO` | banido; substitua por fonte verificada |

Classifique ainda: inexistência, identidade trocada, `misquote`, `pincite`, `ratio` confundida com `dictum` e superação.

Todo fato crítico tem fonte e fl./evento/ID exatos; fato público tem fonte pública; acesso offline recebe marcador apenas no rascunho.

### Suficiência por proposição

Para cada proposição decisiva, registre: frase exata; fonte; trecho literal; página/ID; inferência permitida; alcance; o que a fonte não prova; consequência; destino (`entra`, `reformular`, `diligenciar` ou `excluir`). Cubra no mínimo as 10–15 proposições de maior impacto e amplie se preciso.

Fonte verdadeira sem aderência lógica não basta: tema sobre taxa legal não resolve taxa convencional, preclusão, coisa julgada ou admissibilidade; conversão de AREsp em REsp não supera todos os filtros. Insuficiência material bloqueia o externo.

### Admissibilidade fundamento a fundamento

Antes do mérito, decomponha o ato em capítulos autônomos e fundamentos sobrepostos. Para cada fundamento, confronte: razão da decisão; dispositivo; trecho recursal de impugnação; página; resposta jurisprudencial verificada; objeção; risco; conclusão. Fundamento autônomo intocado pode encerrar o caso.

No STJ, teste concretamente Súmulas 5, 7, 211, 283 e 284. Não converta omissão de um capítulo em não conhecimento total; fundamente eventual conhecimento parcial, preclusão do capítulo omitido e desprovimento do restante. Não transplante precedente sobre inadmissibilidade na origem sem identidade estrutural com o recurso atual.

Para intempestividade, localize o ato oficial que rege cada dia, reproduza a contagem dia a dia e teste cenários positivo/negativo. Se o dia não contou e restar falha documental, retire a tese material ou aplique o saneamento vigente.

### Matrizes temáticas obrigatórias quando aplicáveis

- **Informação/autoria:** separe conhecimento, transmissão, marcação do formulário, orientação, controle do dispositivo, assinatura e vínculo do intermediário. Entrega ao corretor não é entrega à operadora. Diferencie migração, portabilidade e nova contratação. Admita omissão formal comprovada e trate autoria, dolo, confiança e cadeia separadamente.
- **Assinatura eletrônica:** separe conteúdo, trilha por campo e assinatura final. Envelope, IP, SMS ou certificado não individualiza escolhas anteriores sem log nativo. Prova nova adversa reabre a peça e elimina negações amplas. Se autoria do campo importar, peça preservação/exibição de data, usuário, dispositivo, IP, alteração e vínculo formulário-envelope.
- **Prescrição administrativa:** decomponha fundo de direito, metodologia, parcelas, negativa formal e alcance, ciência, requerimentos suspensivos, atos interruptivos, norma/decisão, efeito temporal e fonte. E-mail separa envio, recebimento cognoscível, competência do canal e processamento; obtenha `.eml`/headers, logs, resposta, encaminhamento ou protocolo quando decisivo. Modulação vem do dispositivo oficial. Valor é estimativa até conciliação parcela a parcela. PA tardio, protesto ou lei nova não revive pretensão sem demonstração oficial e limitada.

### Saídas internas

Produza tabelas de precedentes — com classificação `VERIFICADO`, `SECUNDÁRIO` como apoio não substitutivo ou `BANIDO` — e premissas, lastro por proposição, matriz de admissibilidade e matrizes temáticas aplicáveis em `VERIFICACAO_<peça>.md`/ledger. Todo pendente aparece também no ponto exato do rascunho. Corpo limpo com ledger pendente é omissão.

Nada avança sem ledger. Mais de dois precedentes banidos ou mais de três pendências gera risco crítico. Marcadores, tabelas e metalinguagem nunca entram no final.

## GATE 4 — PRODUTO ESTRATÉGICO

Separe:

1. ledger interno — fontes, hashes, lacunas, atribuição e gates;
2. memorial de trabalho — matrizes, cenários e condicionais;
3. peça/parecer externo — voz autoral, posição clara, cronologia única, fundamentos hierarquizados, objeções reais e respostas.

O externo só nasce após trocar condicionais materiais por transcrição, página, cálculo reproduzível e pedido sequencial. Antes de redigir, faça folha de decisão por quesito: resposta, fundamento principal, fundamentos autônomos, objeção mais forte, fato que muda o resultado e diligência pendente. Incerteza material vem no ponto exato com consequência; prudência não neutraliza conclusão sustentada.

Use `/workflows` em paralelo:

- `/helena`: cenários, probabilidades, narrativa e ordem;
- `/cicero`: teses, forma, admissibilidade, prequestionamento, prazos, regimento, leis gerais, retórica e precedentes;
- `/diabob`: ataque adversário/julgador, contradições, alucinações e irritantes;
- `/maquiavel`: poder, incentivos e consequências;
- `/sun-tzu`: terreno, timing, economia e minimização de munição.

Faça síntese adversarial, resolvendo conflito por decisão fundamentada, e gere blueprint com estrutura, ordem, inclusões, exclusões e visuais. Helena e Cícero são obrigatórios em toda peça: `F4_PARECER_HELENA.md` e `F4_PARECER_CICERO.md`, recomendações numeradas e decisão sobre cada uma.

### Helena quantitativa

Helena escolhe, justifica e descarta ferramentas entre jogos, Monte Carlo, cenários, decisão, Bayes, stakeholders e análise quali/quanti. Com magistrados sintéticos calibrados e variados, simula milhares de julgamentos da original e melhorada em Python (`numpy/pandas/scipy`) e usa R quando melhorar distribuições, intervalos ou testes. Faz sensibilidade por argumento/prova/visual, modela autor↔adversário↔juízo em minimax e entrega probabilidades estimadas, delta e ranking.

Ao final, separa: melhoria que entra; insumo só estratégico; descarte. Simulação orienta, não vira prova nem número apresentado ao juízo. O blueprint prioriza o que mais move o resultado estimado.

## GATE 5 — REDAÇÃO, VISUAL E EDIÇÃO

Redija em português jurídico impecável:

- síntese de meia página, estilo art. 343-A do RISTJ, em toda peça e tribunal: controvérsia, fundamentos e pedido;
- títulos numerados, hierarquia limpa, um argumento por seção e tese na primeira frase;
- fatos sempre ancorados em fl./ID/doc; datas, valores e dispositivos sem ambiguidade;
- tabela-resumo dos pedidos ao final;
- destinatário recebe primeiro resultado/utilidade, depois fundamentos decisivos, objeção mais forte, lacuna que mudaria a resposta e próxima ação;
- conclusão em uma página, cronologia única, resposta a cada quesito, nenhuma ressalva sem consequência e menos capítulos que o memorial.

Use `/diana` e `/comunicacao-persuasiva` para imagens mentais fiéis, metáforas jurídicas precisas, enquadramento e ethos/pathos/logos. Reconfronte cada fato, dispositivo e precedente com fonte oficial; proíba citação decorativa ou aproximada.

### Cautelas de sênior

- prequestione expressamente dispositivos legais e constitucionais quando aplicável; em omissão/fundamentação, bloco próprio para normas pertinentes, inclusive art. 93, IX, e art. 5º, LIV/LV, se sustentados;
- use terminologia que não sugira reexame — omissão qualificada, fundamentação individualizada e erro de subsunção — quando correta;
- trate fato superveniente em capítulo autônomo, sem efeito automático;
- varra prevenção, preclusão, competência/distribuição interna, composição atual e fatos supervenientes;
- em EDcl, formule cada vício como pergunta jurisdicional, peça integração e não rediscussão, segmente pedidos, peça intimação adversa se houver efeitos infringentes e diferencie dolo específico/genérico, culpa, culpa `in vigilando`, assunção de risco e cegueira deliberada;
- visual é apoio com análise ao lado.

### Visual

Use `/fabrica-visual-peticoes`, complementada por `/visual-law-inteia` e `/paperbanana-diagramas`, para SVGs próprios: cronologia, fluxo, comparação, contradição/omissão e pedido→fundamento→prova. Só use quadro que comprima comparação.

No Word, converta SVG→EMF por Inkscape e insira via Word COM com `_FERRAMENTAS\word_visual_pipeline.py`; não use `python-docx` para EMF. Paleta: petróleo `#395C60`, terracota `#D9926A`. Cada visual declara função cognitiva — primazia, Von Restorff, dupla codificação, Gestalt ou ancoragem — e nunca é decorativo.

Replique cabeçalho, timbre, fonte, margens, assinatura e endereçamento da original; texto justificado, Arial 12 ou fonte original, negrito mínimo, sem divisórias decorativas, espaçamento ABNT-forense.

### Fable controlado

Só após F7 com zero P0, chame explicitamente `forja_fable5.py` via OAuth Claude Max, sem API key, usando `audited_markdown`. `forja_run.py` não faz essa chamada. O editor melhora forma, sem criar argumento nem mudar fato, número, data, valor, citação, autoridade, marcador, ressalva, pedido, fecho ou assinatura. Dúvida material não entra.

Valide `final_markdown` com `forja_editorial_fidelity.py`, hashes, contagens, invariantes e leitura humana. Se falhar, recomece do auditado, sem reescrita em cadeia. Incorpore `FABLE5_RESULT.json` ao `PHASE_RESULT.json`; F8 e pacote novo apontam ao `final_markdown`, mantendo `audited_markdown` como trilha. Envie ao serviço remoto só texto necessário, sem segredo, credencial, token ou dado estranho. Gate determinístico não substitui auditoria jurídica.

## GATE 6 — LIBERAÇÃO

1. Gere `.docx` e `.pdf`.
2. Abra o PDF efetivo e inspecione todas as páginas com screenshots: quebras, cortes, SVGs, tabelas, margens, numeração, cabeçalho/rodapé e acentuação. Corrija e regenere até perfeito.
3. Refaça checagem de cada fato, lei, precedente e prova contra pasta, fonte oficial e ledger.
4. Bloqueie o final enquanto houver `[VERIFICAR]`, tabela interna ou precedente `RESTRITO`, `INDISPONÍVEL-TRANSITÓRIO` ou `NÃO-ENCONTRADO` sem decisão humana: verificar, remover ou aceitar com risco nominado.
5. Rode o checklist vigente de `APRENDIZADOS_FEEDBACK_HUMANO.md`. Síntese 343-A e questões laterais são universais; demais itens seguem aplicabilidade. N/A exige justificativa de uma linha, sem seção vazia.
6. Rode `/revisar-anti-ia` sem alterar substância.
7. Refaça a simulação de Helena na final; se não houver ganho estimado frente à original ou seção relevante não melhorar, revise.
8. Confirme separação interno×externo, folha de decisão, zero P0, fidelidade Fable, artefatos F7-B pareados e inspeção de 100% do PDF.
9. Entregue `<NOME>_SUPER_VERSAO_FINAL.docx`, `.pdf` e `RELATORIO_MELHORIAS.md` curto: mudanças; contribuição das personas; probabilidade original/final; três melhorias de maior impacto; arsenal usado/descartado; riscos e pendências. Se bloqueado, entregue só o interno e não use “final”.

### Fechamento operacional

Antes da baixa:

- alinhe relatório, e-mail, WhatsApp e painel em tese, risco, pendência e recomendação;
- releia canais vivos e classifique `ainda não enviado`, `já enviado` ou `não verificado`;
- diferencie `respondida`, `entregue_para_revisao` e `cumprida`;
- só marque `cumprida` com pedido coberto + insumos acessíveis + produto verificado + canais coerentes + evidência de entrega + releitura final;
- painel verde não substitui prova;
- inclua no e-mail “Pontos que exigem o seu olho”, com três a seis itens e páginas;
- confirme o retorno do canal;
- entrega ao escritório pode concluir a operação, mas não libera cliente/protocolo sem lastro.

## EXECUÇÃO

- Autonomia total: decida sem confirmação intermediária e reporte ao final.
- Trabalhe sobre cópia; nunca sobrescreva originais.
- Falta essencial vira bloqueador explícito, nunca invenção.
- Tempo e custo não restringem a qualidade.
- Aprovação isolada não vira regra global sem repetição, teste e aprovação expressa.
