<!-- mutacao: expand | eixo: ampliar gates de prova, admissibilidade e separação de produtos sem retirar comandos vigentes | parent: baseline -->
# PROMPT — Fábrica de Melhoria de Petições

> Uso: abra o Claude Code dentro da pasta do processo e cole o prompt abaixo.
> O prompt é genérico: o agente identifica o caso pela leitura integral da pasta.

---

/goal Produzir a versão definitiva, superpotencializada e diagramada da petição principal desta pasta, validada jurídica, factual e visualmente página a página, mantendo o padrão do escritório.

## MISSÃO

Nesta pasta há uma petição principal e materiais de apoio: versões em `.docx`, `.pdf` e `.md`, rascunhos de outras IAs, provas, decisões e documentos do processo. Produza a **super-versão melhorada** da petição — a mais completa, persuasiva, segura e elegante possível — usando o potencial máximo do Fable e das skills da Colmeia.

Qualidade visual, eloquência ou aparência de conclusão nunca substituem lastro. Se um gate material não for satisfeito, entregue o produto interno cabível e mantenha bloqueada a peça externa.

## FASE 1 — LEITURA ESTRATÉGICA DA PASTA

Obrigatória antes de escrever qualquer linha da peça.

1. Liste **todos** os arquivos da pasta e das subpastas e classifique-os: petição original; versões melhoradas por outras IAs; provas/anexos; decisões judiciais; legislação; modelos do escritório; mídias; comunicações; produtos internos; produtos externos.
2. Leia a petição original por inteiro. Extraia partes, juízo, tipo de peça, pedidos, teses, fundamentos, prazos e padrão do escritório: cabeçalho, fonte, timbre, rodapé, assinatura, margens e endereçamento.
3. Leia as versões alternativas existentes e faça um diff estratégico: o que cada uma acrescentou, perdeu, alterou, fortaleceu sem prova ou alucinou. Comando, e-mail, minuta humana e texto de outra IA orientam a busca, mas não substituem os autos.
4. Leia as provas e decisões e mapeie o que cada documento efetivamente prova, o que não prova e onde pode ser usado.
5. Produza um **MAPA DO CASO interno**: fatos; cronologia; teses; pontos fortes; pontos fracos; decisão necessária; provável resposta adversária; questões processuais laterais; lacunas; diligências.

### 1-A — Acervo em duas camadas

Mantenha no ledger interno a proveniência operacional completa: origem, autoria conhecida ou desconhecida, versão, canal, hash, página/ID, caminho e cadeia de custódia. Elimine essa metalinguagem da peça.

A manifestação judicial usa apenas pontes processuais verdadeiras, como “e-STJ fl. X”, “evento/ID X”, “documento juntado aos autos”, “Doc. X” ou “documento anexo”. “Documento juntado aos autos” exige juntada confirmada; “documento anexo” exige que o documento acompanhe efetivamente a manifestação.

É proibido escrever na peça ou em comunicação externa: “compartilhado pelo escritório”, “recebido por e-mail/WhatsApp”, “Drive”, “pasta interna”, “arquivo local”, caminho de computador, nome de artefato de auditoria, hash, gate, fase, minuta ou condição operacional. Vazamento de origem operacional no produto externo é falha P0.

### 1-B — Identidade dos atos e cronologia

Em processo volumoso, atribua um código inequívoco a cada recurso, decisão, conversão, retratação, destaque e intimação. Para cada ato, registre:

- sujeito;
- data;
- classe e número;
- ato impugnado;
- pedido;
- resultado;
- efeito jurídico;
- relação com os atos anteriores e posteriores;
- página, folha, evento ou ID nos autos.

Não redija enquanto expressões como “o agravo”, “o recurso” ou “a decisão” puderem designar mais de um ato. A íntegra do ato atualmente impugnado e a cronologia completa são insumos obrigatórios. Conversão, retratação ou juízo positivo anterior só valem no alcance do inteiro teor e não dispensam nova leitura integral do ato atual.

### 1-C — Cobertura, mídias e reabertura

Se faltar a íntegra do ato atualmente impugnado, a cronologia completa ou outro insumo material, produza somente relatório interno de pendências; não gere DOCX/PDF protocolável nem declare a demanda concluída.

Registro de mensagem com mídia prova apenas que houve um evento. Para afirmar que áudio, imagem ou documento foi considerado, confirme caminho, existência, abertura, correspondência e leitura. Mídia essencial não materializada é bloqueador P1; não pode ser inferida por mensagens vizinhas.

Agrupe comunicações contíguas por assunto, dependência e tempo. Leia a rajada conversacional até sua alta d’água antes de extrair pedido, contexto, prazo, pergunta e materialidade. Complemento posterior pode corrigir ou restringir a mensagem anterior.

Todo material humano novo e potencialmente adverso reabre formalmente o ciclo: invalide as fases subsequentes afetadas, recalcule hashes dos bytes entregues e repita os gates jurídico e visual do DOCX/PDF.

### 1-D — Autoria intelectual e diff atributivo

Origem da mensagem não prova autoria intelectual da tese. Para cada tese adicionada, fortalecida, enfraquecida, reformulada ou removida, registre quem a suscitou, qual fonte a sustenta, quem a selecionou, quem a validou e quem decidiu incorporá-la. Use, quando aplicável: `human_original`, `human_selected`, `forja_generated`, `external_model_import`, `source_derived`, `mixed` e `unknown`.

Quando voltar versão revisada ou assinada, compare-a com a última versão efetivamente enviada pela FORJA e produza ledger jurídico e atributivo por tese: `adicionada`, `fortalecida`, `enfraquecida`, `reformulada`, `removida` ou `inalterada`. Origem humana não certifica correção; tese nova ou fortalecida continua sujeita a fonte suficiente e decisão jurídica registrada.

### 1-E — Regimento do tribunal

Identifique o tribunal pela numeração CNJ, endereçamento e decisões. Leia o `REGIMENTO_INTERNO_<TRIBUNAL>.md` da pasta. Se não existir, baixe a versão consolidada oficial mais recente, converta-a para `.md` **integral**, nunca resumo, e salve-a antes de redigir. Verifique emendas regimentais posteriores à consolidação até o dia da elaboração e anexe-as na seção final do `.md`.

Observe competência do órgão julgador, cabimento, processamento, prazos regimentais, sustentação oral e pauta. Considere também a pasta mãe `_LEIS_GERAIS`, inclusive Estatuto da OAB — Lei 8.906/1994 — e LOMAN — LC 35/1979. Registre no relatório final os dispositivos regimentais e das leis gerais que impactaram a peça.

### 1-F — Regra de verdade

Nenhum fato, citação, jurisprudência, número de processo, data, valor, autoridade ou alegação sobre anexo pode ser inventado. Tudo que entrar na peça deve estar nos arquivos ou ser verificável em fonte idônea. Jurisprudência nova exige verificação real; se ainda não puder ser verificada, marque `[VERIFICAR]` apenas no rascunho e informe no produto interno. Nunca libere o documento final com esse marcador.

## FASE 1.2 — EXPLORAÇÃO PROBLEMATIZADORA EM 100 PERGUNTAS

Obrigatória em todo caso novo, depois da ingestão segura e da leitura integral, mas antes de pesquisa, conselho, blueprint ou redação.

Execute a subfase FORJA `F2-A`. Produza exatamente **100 perguntas inteligentes e adaptadas ao caso**, distribuídas em **10 óticas com 10 perguntas cada**:

1. mandato/resultado;
2. fatos/cronologia;
3. prova/fontes;
4. processo/competência;
5. direito/precedentes;
6. adversário/julgador;
7. riscos/ética/impactos;
8. alternativas/soluções;
9. quantificação/execução;
10. comunicação/visual/validação.

Responda cada pergunta com âncora do caso, importância, natureza epistemológica e fonte/localizador quando a resposta for factual, processual, jurisprudencial ou numérica. Sem resposta verificável, registre `blocked` + consequência + diligência; nunca complete a centena inventando.

Consolide definição do problema, síntese diagnóstica, ao menos duas hipóteses de solução com condições e riscos, questões materiais abertas e roteamento nominal para F3–F7.

Artefato interno canônico: `_FORJA_HARNESS\state\<caseId>\n4_artifacts\F2_QUESTION_TREE.json`, protocolo `FORJA-F2A-100-v1`. Questão material bloqueada impede F6/DOCX/PDF protocolável, mas segue à F3/F5 como pendência a resolver.

Contrato, óticas e comandos: `_FORJA_HARNESS\templates\F2A_EXPLORACAO_100_PERGUNTAS.md`. Validador: `python _FORJA_HARNESS\forja_exploracao_100.py validate <arquivo>`.

## FASE 1.5 — VARREDURA CRÍTICA DE ATRIBUIÇÃO, SUFICIÊNCIA E ADMISSIBILIDADE

Antes de estratégia ou redação, faça uma passagem de fonte primária sobre tudo que a peça pretende afirmar. Esta fase valida fundações; não produz prosa persuasiva.

### 1.5-A — Precedentes verificáveis

Para cada jurisprudência, súmula, enunciado ou tema, o status `VERIFICADO` exige os quatro elementos:

1. número ou identificador exato;
2. fonte oficial nomeada — SCON/STJ, portal STF, DJe ou portal oficial do tribunal — com URL quando houver;
3. trecho literal, nunca paráfrase de memória;
4. localização do trecho — ementa, voto, página ou parágrafo — quando o teor sustentar tese central.

Identidade ambígua nunca é verificada. “Jurisprudência consolidada”, número aproximado ou julgado análogo de memória é pendente ou banido.

| Status | Hipótese | Consequência |
|---|---|---|
| `VERIFICADO` | quatro elementos presentes | pode entrar na peça |
| `RESTRITO` | fonte de acesso restrito | entra apenas no rascunho com `[VERIFICAR: acesso restrito]`, ponte declarada e verificação humana pré-protocolo |
| `INDISPONÍVEL-TRANSITÓRIO` | fonte pública fora do ar ou bloqueada na sessão | permanece só no rascunho com marcador, tentativa datada e verificação humana obrigatória |
| `NÃO-ENCONTRADO` | busca real em fonte aberta não localiza | banido; substituir por doutrina ou precedente verificado |

Faça ainda a taxonomia de falhas: inexistente; nome/identidade trocada; `misquote`; `pincite` incorreto; tese deturpada por confusão entre `ratio` e `dictum`; precedente superado.

### 1.5-B — Premissas fáticas localizáveis

Para cada fato crítico — data, evento processual, decisão, valor e documento — registre se está nos autos e a referência exata, como “Evento 185, fls. 59–62”. Fato público exige fonte pública. Fonte não acessível recebe `[VERIFICAR: acesso offline]` somente no rascunho.

O comando mais autorizado continua sendo hipótese até os autos o sustentarem. O red team deve perguntar expressamente se a peça aceitou premissa do comando, e-mail, mensagem ou minuta que a prova não confirma.

### 1.5-C — Teste de suficiência por proposição

Fonte verdadeira não basta. Para cada proposição decisiva, registre em tabela de lastro:

- proposição exata;
- fonte;
- trecho literal;
- página/ID;
- inferência permitida;
- alcance temporal e subjetivo;
- o que a fonte **não** prova;
- consequência da insuficiência;
- destino: `entra`, `reformular`, `condicionar internamente`, `diligenciar` ou `excluir`.

Teste a relação lógica entre o trecho e a frase que será escrita. Um tema que identifica a taxa legal não resolve, por si, taxa convencional, preclusão, coisa julgada ou admissibilidade. Conversão de AREsp em REsp não supera automaticamente todos os filtros. A tabela deve cobrir ao menos as 10–15 proposições de maior impacto e se expandir quando necessário. Insuficiência material bloqueia a versão externa.

### 1.5-D — Auditoria de admissibilidade fundamento a fundamento

Antes do mérito, decomponha o ato atual em capítulos autônomos e, dentro de cada capítulo, em fundamentos sobrepostos. Não transforme automaticamente a omissão de uma matéria em não conhecimento total.

Para cada fundamento, registre:

- razão exata da decisão;
- dispositivo federal ou constitucional pertinente;
- trecho do recurso que o impugnou;
- página/ID;
- resposta jurisprudencial verificada;
- objeção mais forte;
- risco;
- conclusão de superação ou não.

Fundamento autônomo intocado pode encerrar o caso antes do mérito. Em matéria destinada ao STJ, teste concretamente as Súmulas 5, 7, 211, 283 e 284, sem mera enumeração. Julgado sobre indivisibilidade da decisão de inadmissibilidade na origem não pode ser transplantado para Agravo Interno atual sem demonstrar identidade estrutural. O pedido seguro pode ser conhecimento parcial, preclusão do capítulo omitido e desprovimento do restante, conforme os autos e a lei.

Antes de alegar intempestividade material, localize o ato oficial do órgão competente para cada dia excluído. Reproduza o cálculo dia a dia e congele testes positivos e negativos. Se o ato oficial demonstrar que o dia não contou e restar apenas vício documental, retire a tese material ou trate-a conforme o regime de saneamento vigente.

### 1.5-E — Cadeia de informação, autoria e assinatura eletrônica

Em contratos mediados, não negue formulário objetivamente incorreto. Separe:

- quem conhecia o fato;
- quem o transmitiu ao canal;
- quem marcou o formulário;
- quem orientou;
- quem controlou o dispositivo;
- quem assinou;
- a quem o intermediário juridicamente se vinculava.

Entrega ao corretor não é entrega direta à operadora. “Migração” comercial, portabilidade regulatória e nova contratação são institutos distintos; não presuma transferência automática de prontuário, informação ou autorização entre operadoras. Admita a omissão formal quando comprovada e discuta separadamente autoria, dolo, confiança e cadeia.

Em contratação eletrônica, diferencie conteúdo preenchido, trilha de preenchimento por campo e ato final de assinatura. Certificado de conclusão, autenticação do envelope, IP, SMS ou assinatura móvel provam apenas o que a evidência registra e não individualizam, sem log nativo, quem escolheu cada resposta anterior. Se prova nova contrariar a narrativa, reabra a peça, reconheça o ato comprovado e retire afirmações amplas. Quando a autoria do preenchimento importar, peça preservação e exibição da trilha nativa por campo, com data, usuário, dispositivo, IP, alteração e vínculo entre formulário e envelope.

### 1.5-F — Matriz de prescrição administrativa

Em controvérsia contra a Fazenda, é proibido tratar “a prescrição” como etiqueta global. Construa matriz por:

- objeto: fundo de direito, metodologia de cálculo e parcelas sucessivas;
- ato: negativa formal, extensão objetiva da negativa e ciência inequívoca;
- parcela e período;
- requerimento potencialmente suspensivo;
- ato potencialmente interruptivo;
- norma ou decisão aplicável;
- efeito temporal demonstrado;
- fonte oficial;
- conclusão e incerteza residual.

Precedente sobre negativa do fundo de direito não resolve automaticamente todo o histórico.

Prova por e-mail exige quatro camadas independentes: envio; recebimento cognoscível; competência do canal destinatário; processamento administrativo. PDF, ata notarial ou captura podem provar envio sem provar ingresso na repartição competente. Quando decisivo, obtenha anexo original, `.eml`/headers, logs, resposta, encaminhamento interno ou protocolo; até lá, a tese permanece condicionada apenas no produto interno.

Extraia modulação temporal do dispositivo oficial, não da publicação isolada nem de resumo secundário. Trate valor apresentado pela parte como estimativa até haver conciliação reproduzível parcela a parcela. Processo administrativo tardio, protesto ou lei superveniente não revive automaticamente pretensão prescrita: demonstre cada efeito por fonte oficial e limite-o ao seu alcance.

### 1.5-G — Saídas e gates

Produza internamente:

- tabela **Precedentes Mapeados**: nome, tribunal, data, trecho, localizador, status (`VERIFICADO`, `SECUNDÁRIO` como apoio não substitutivo ou `BANIDO`) e falha taxonômica;
- tabela **Premissas Mapeadas**: premissa, fonte, local exato, suficiência e status;
- tabela de lastro por proposição;
- matriz de admissibilidade fundamento a fundamento;
- matrizes temáticas aplicáveis.

Todo item `RESTRITO`, `INDISPONÍVEL-TRANSITÓRIO` ou a verificar recebe também `[VERIFICAR: motivo]` no ponto exato do rascunho. A tabela organiza; o corpo confessa. Corpo limpo com tabela cheia é omissão.

As tabelas e matrizes vivem no ledger e em `VERIFICACAO_<peça>.md`, nunca no DOCX/PDF final. O documento protocolável não carrega `[VERIFICAR]`, tabela de auditoria, hash, gate ou metalinguagem. Nada avança sem registro no ledger. Mais de dois precedentes banidos ou mais de três pendências exige risco crítico no relatório.

## FASE 1.7 — ARQUITETURA DOS PRODUTOS E FOLHA DE DECISÃO

Trate como produtos distintos:

1. **ledger interno**: proveniência, lacunas, hashes, gates, atribuição e evidência;
2. **memorial de trabalho**: matrizes, cenários, condicionais e hipóteses;
3. **peça ou parecer externo**: voz autoral, posição clara, uma cronologia, fundamentos hierarquizados, objeções reais e respostas conclusivas.

O externo só nasce quando condicionais materiais forem substituídas por transcrição, página, cálculo reproduzível e pedido sequencial. Se isso não for possível, classifique a saída como `internal_working`, ainda que esteja visualmente pronta.

Antes da escrita final, produza folha de decisão com: resposta por quesito; fundamento principal; fundamentos autônomos; objeção mais forte; fato que mudaria o resultado; diligência material pendente. Prudência não deve neutralizar opinião sustentada; incerteza material deve ser localizada com sua consequência.

No produto externo: conclusão inicial; metodologia curta quando necessária; cronologia única; resposta expressa a cada quesito; nenhuma ressalva sem consequência; menos capítulos que no memorial; quadros apenas se comprimirem comparação. O destinatário recebe resultado e utilidade, fundamentos decisivos, objeção mais forte, lacuna capaz de mudar a resposta e próxima ação. O ledger permanece interno.

## FASE 2 — CONSELHO DE GUERRA

Use `/workflows` com agentes paralelos. Cada persona recebe o mapa do caso e a petição original e devolve contribuição estruturada:

- **/helena** — estratégia geral: cenários, probabilidades, narrativa que maximiza êxito e ordem dos argumentos;
- **/cicero** — jurídico: solidez, requisitos formais, admissibilidade, prequestionamento, prazos, técnica processual, regimento, leis gerais, retórica e jurisprudência;
- **/diabob** — red team: ataque adversário e julgador cético; fraquezas, contradições, alucinações herdadas e pontos que irritam o juízo;
- **/maquiavel** — poder e incentivos: consequências institucionais, reputação e alinhamento do pedido;
- **/sun-tzu** — terreno e timing: onde lutar ou ceder, o que guardar e como não dar munição ao adversário.

Depois do fan-out, faça síntese adversarial: resolva conflitos por decisão fundamentada, nunca por média, e gere o blueprint final com estrutura, ordem, inclusões, exclusões e diagramas.

Os pareceres de Helena e Cícero são obrigatórios em toda peça, em `F4_PARECER_HELENA.md` e `F4_PARECER_CICERO.md`, com recomendações numeradas e decisão registrada sobre cada uma.

## FASE 2-B — ARSENAL HELENA E SIMULAÇÃO QUANTITATIVA

Além do conselho, `/helena` atua como cientista-chefe:

1. Revise teoria dos jogos, Monte Carlo, cenários, decisão, Bayes, stakeholders e análise quantitativa/qualitativa. Escolha e justifique apenas as ferramentas úteis ao caso; descarte explicitamente o restante.
2. Construa painel de magistrados sintéticos com perfis variados e calibrados pelo tipo de juízo e pela peça original.
3. Para original e versão melhorada, simule milhares de julgamentos em Python, com `numpy`, `pandas` e `scipy`; use R para distribuições, intervalos e testes quando houver ganho.
4. Faça análise de sensibilidade para medir qual argumento, prova ou diagrama mais altera a probabilidade estimada de êxito.
5. Aplique teoria dos jogos ao autor, adversário e juízo; antecipe a melhor resposta contrária e escolha formulação robusta no pior cenário, sem entregar munição.
6. Entregue probabilidade estimada da original e da melhorada, delta atribuído a cada melhoria e ranking por impacto.
7. Helena revisa o próprio trabalho e separa: melhoria com suporte quantitativo que entra; insumo apenas estratégico; descarte justificado.

A simulação orienta a redação, não vira conteúdo da peça nem prova. Número sintético nunca é apresentado ao juízo como fato. O blueprint prioriza argumentos e diagramas de maior impacto estimado.

## FASE 3 — REDAÇÃO DA SUPER-VERSÃO

1. Escreva a peça completa em português jurídico impecável, seguindo o blueprint.
2. Atenda à dupla audiência humana e algorítmica:
   - títulos numerados e hierarquia limpa;
   - um argumento por seção;
   - tese na primeira frase de cada seção;
   - síntese executiva no início, em meia página, com controvérsia, fundamentos e pedido;
   - tabela-resumo dos pedidos ao final;
   - fatos ancorados em fl./ID/doc;
   - zero ambiguidade em datas, valores e dispositivos.
3. Use `/diana` e `/comunicacao-persuasiva`. Aplique as melhorias priorizadas pela simulação: imagens mentais fiéis, metáforas jurídicas precisas, enquadramento favorável e ethos/pathos/logos. Persuasão não distorce fatos.
4. Reconfronte cada dispositivo, precedente e afirmação com a pasta, a fonte oficial e o ledger. Corrija número, órgão, data, teor e localizador. Não use citação decorativa ou aproximada.
5. Use `/fabrica-visual-peticoes` como pipeline oficial e crie SVGs próprios para ideias relevantes: cronologia, fluxo processual, comparação de teses, mapa de contradição/omissão e matriz pedido→fundamento→prova. Complemente com `/visual-law-inteia` e `/paperbanana-diagramas`.
6. No Word, insira vetores por SVG→EMF via Inkscape e Word COM usando `_FERRAMENTAS\word_visual_pipeline.py`; `python-docx` não aceita EMF. Use a paleta Medina Osório — petróleo `#395C60` e terracota `#D9926A` — com sobriedade. Declare a função cognitiva de cada visual: primazia, Von Restorff, dupla codificação, Gestalt ou ancoragem. Nada decorativo.
7. Reproduza exatamente cabeçalho, timbre, fonte, margens, assinatura e endereçamento da original. Texto justificado, Arial 12 ou fonte original, negrito mínimo, sem linhas divisórias decorativas e com espaçamento ABNT-forense.

### Cautelas de sênior

- Síntese executiva estilo art. 343-A do RISTJ no início de toda peça, em qualquer tribunal.
- Prequestionamento expresso dos dispositivos legais e constitucionais quando aplicável. Em omissão ou fundamentação, use bloco constitucional próprio quando sustentado, em especial art. 93, IX, e art. 5º, LIV/LV.
- Linguagem de admissibilidade que não sugira reexame de prova: “omissão qualificada”, “ausência de fundamentação individualizada” e “erro de subsunção normativa”, quando corretas.
- Fato superveniente em capítulo autônomo, com relevância delimitada e sem efeito automático inventado.
- Varredura de prevenção, preclusão, distribuição/competência interna, composição atual do órgão e fatos supervenientes.
- Em EDcl: vício como pergunta jurisdicional objetiva; integração, não rediscussão; pedidos por vício; intimação adversa se houver efeitos infringentes; separação entre dolo específico, dolo genérico, culpa, culpa `in vigilando`, assunção de risco e cegueira deliberada.
- Visual como apoio, sempre acompanhado de fundamento analítico.

## FASE 3.5 — EDIÇÃO FINAL CONTROLADA

A revisão de escrita pelo Claude Fable 5 só começa depois de F7 registrar zero P0. O insumo é o `audited_markdown`; o aprovado é o `final_markdown`, cânone textual de F8 e dos novos pacotes.

O editor pode melhorar apenas forma. Não pode resolver lacuna, criar argumento, nem alterar fatos, números, datas, valores, citações, autoridades, marcadores processuais, ressalvas, pedidos, fecho ou assinaturas. Mudança material vira dúvida editorial e não entra silenciosamente.

Faça a chamada explícita por `forja_fable5.py`, autenticada por OAuth Claude Max, sem API key; `forja_run.py` não substitui essa chamada. `forja_editorial_fidelity.py` deve recomputar hashes, contagens e invariantes diretamente dos arquivos. Se reprovar, recomece do `audited_markdown`, sem encadear reescritas. `FABLE5_RESULT.json` é fragmento a incorporar ao `PHASE_RESULT.json`; promoção e empacotamento continuam sujeitos ao contrato integral da fase.

Envie ao serviço remoto apenas o texto necessário. Nunca inclua segredo, credencial, token ou dado estranho ao caso. Gates determinísticos complementam, mas não substituem, auditoria jurídica/factual e leitura humana.

## FASE 4 — VALIDAÇÃO E LIBERAÇÃO

1. Gere o documento final em `.docx` e `.pdf`.
2. Abra o PDF efetivo e inspecione visualmente **todas** as páginas, com screenshot página a página: quebras; diagramas; cortes; tabelas; margens; numeração; cabeçalho/rodapé; acentuação.
3. Corrija e regenere até a diagramação ficar perfeita. Não entregue defeito visual “pequeno”.
4. Faça checagem anti-alucinação final de cada citação legal, precedente, fato e referência de prova contra a pasta, a fonte oficial e o ledger.
5. Bloqueie a versão final enquanto houver no texto `[VERIFICAR]`, tabela interna, precedente `RESTRITO`, `INDISPONÍVEL-TRANSITÓRIO` ou `NÃO-ENCONTRADO` sem decisão humana registrada: verificado, removido ou aceito com risco nominado. Pendência não resolvida mantém o documento como rascunho.
6. Rode o checklist operacional **vigente** de `APRENDIZADOS_FEEDBACK_HUMANO.md`, usando a versão do dia. Aplique matriz de aplicabilidade: síntese 343-A e questões laterais são universais; prequestionamento, terminologia recursal, fato superveniente, EDcl e matrizes temáticas dependem da peça e dos autos. Registre N/A com justificativa de uma linha; não crie seção vazia. Item universal ausente impede liberação.
7. Rode `/revisar-anti-ia` e elimine marcas artificiais sem alterar substância.
8. Refaça a simulação de Helena sobre a versão final e confirme aumento estimado frente à original. Se seção relevante não melhorar o número, revise-a.
9. Confirme a separação dos produtos: o externo não contém ledger, matriz operacional, condição documental, metalinguagem, hash, nome de fase ou fonte operacional.
10. Confirme a folha de decisão: conclusão em uma página; cronologia única; resposta a cada quesito; nenhuma ressalva sem consequência; objeção mais forte enfrentada; próxima ação útil.
11. Confira que Fable 5 recebeu `audited_markdown` apenas depois de zero P0; que `FABLE5_RESULT.json` foi incorporado ao `PHASE_RESULT.json`; que artefatos F7-B estão pareados; que `forja_editorial_fidelity.py` aprovou hashes/invariantes; e que F8/pacote apontam para `final_markdown`.
12. Entregue na pasta:
    - `<NOME>_SUPER_VERSAO_FINAL.docx`;
    - `<NOME>_SUPER_VERSAO_FINAL.pdf`;
    - `RELATORIO_MELHORIAS.md`, curto e leigo, com mudanças, contribuições das personas, estimativa original/final, três melhorias de maior impacto, arsenal usado/descartado, riscos e pendências. Se houver bloqueador, não chame DOCX/PDF de final; entregue apenas os produtos internos cabíveis.

### Gate operacional de comunicação e encerramento

Antes de baixar a demanda:

- compare relatório, e-mail, WhatsApp e painel numa matriz curta de tese, risco, pendência e recomendação; extensões podem variar, substância não;
- classifique a cronologia da entrega como `ainda não enviado`, `já enviado` ou `não verificado`; releia os canais imediatamente antes do fechamento e não use fórmula prospectiva depois de envio já informado;
- trate `respondida`, `entregue_para_revisao` e `cumprida` como estados diferentes;
- só marque `cumprida` com a conjunção: pedido integralmente coberto + insumos críticos acessíveis + produto verificado + comunicação multicanal coerente + evidência de entrega + releitura final das fontes vivas;
- não use painel verde como substituto de e-mail enviado, mídia recuperada, artefato entregue ou registro manual auditável;
- no e-mail de entrega, inclua “Pontos que exigem o seu olho”, com três a seis itens e páginas;
- confirme por leitura do retorno do canal que o ciclo de envio fechou;
- a entrega ao escritório pode encerrar a demanda operacional, mas não libera cliente ou protocolo quando faltarem lastros materiais.

## REGRAS DE EXECUÇÃO

- Autonomia total: não pedir confirmação intermediária; decidir e reportar ao final.
- Trabalhar sobre cópia; nunca sobrescrever os arquivos originais da pasta.
- Se faltar informação essencial, sinalizar no produto interno em vez de inventar.
- Tempo e custo não são restrição; qualidade máxima é o objetivo.
- Aprovação, elogio ou preferência isolada não vira regra global sem repetição independente, teste e aprovação expressa.
