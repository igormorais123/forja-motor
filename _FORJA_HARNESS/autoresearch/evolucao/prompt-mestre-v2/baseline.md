# PROMPT — Fábrica de Melhoria de Petições (genérico, colar em qualquer pasta de processo)

> Uso: abra o Claude Code dentro da pasta do processo e cole o prompt abaixo.
> Ele não cita nenhum caso específico — o Claude descobre tudo lendo a pasta.

---

/goal Produzir a versão definitiva, superpotencializada e diagramada da petição principal desta pasta, validada visualmente página a página, mantendo o padrão do escritório.

## MISSÃO

Nesta pasta há uma petição principal e materiais de apoio (versões em .docx, .pdf, .md, rascunhos de outras IAs, provas, decisões, documentos do processo). Sua tarefa é produzir a **super-versão melhorada** dessa petição — a mais completa, persuasiva e elegante possível — usando o potencial máximo do Fable e das skills da Colmeia.

## FASE 1 — LEITURA ESTRATÉGICA DA PASTA (obrigatória antes de escrever qualquer linha)

1. Liste TODOS os arquivos da pasta (e subpastas) e classifique: petição original, versões melhoradas por outras IAs, provas/anexos, decisões judiciais, legislação, modelos do escritório.
2. Leia a petição original por inteiro. Extraia: partes, juízo, tipo de peça, pedidos, teses, fundamentos, prazos, estilo do escritório (cabeçalho, fonte, timbre, rodapé, forma de assinatura).
3. Leia as versões alternativas/melhoradas existentes e faça um diff estratégico: o que cada versão acrescentou, o que perdeu, o que está errado ou alucinado.
4. Leia provas e decisões: mapeie o que cada documento prova e onde encaixa na argumentação.
5. Produza um MAPA DO CASO (interno): fatos, cronologia, teses, pontos fortes, pontos fracos, o que o julgador precisa decidir e o que o adversário vai alegar.
5-A. **ACERVO EM DUAS CAMADAS:** registre no ledger interno a proveniência operacional completa (nome, versão, canal, hash, página/ID), mas elimine-a da peça. A manifestação judicial só pode usar referência processual verdadeira: “e-STJ fl. X”, “evento/ID X”, “documento juntado aos autos”, “Doc. X” ou “documento anexo”. Nunca escrever na peça “compartilhado pelo escritório”, “recebido por e-mail/WhatsApp”, “pasta interna”, “arquivo local/Drive” ou caminho de computador.
5-B. **IDENTIDADE DOS ATOS EM PROCESSO VOLUMOSO:** atribua um código a cada recurso, decisão, retratação, destaque e intimação. Para cada ato, registre data, sujeito, classe/número, ato impugnado, pedido, resultado, efeito jurídico e localização nos autos. Não redija enquanto “o agravo” ou “a decisão” puder designar mais de um ato.
5-C. **GATE DE COBERTURA:** a íntegra do ato atualmente impugnado e a cronologia completa são insumos obrigatórios. Se faltarem, produza somente relatório interno de pendências; não gere DOCX/PDF protocolável nem declare a demanda concluída.
6. **REGIMENTO DO TRIBUNAL (INVIOLÁVEL — exigência do chefe do escritório, 06/07/2026)**: identificar o tribunal de análise da peça (número CNJ, endereçamento, decisões). Ler o `REGIMENTO_INTERNO_<TRIBUNAL>.md` da pasta — se não existir, baixar a versão consolidada oficial mais recente, converter para .md INTEGRAL (nunca resumo) e salvar na pasta antes de redigir. Verificar emendas regimentais posteriores à consolidação **até o dia da elaboração da peça** e anexá-las na seção final do .md. A peça deve observar as peculiaridades regimentais: competência do órgão julgador, cabimento, processamento, prazos regimentais, sustentação oral, pauta. Considerar também a pasta mãe `_LEIS_GERAIS` (Estatuto da OAB — Lei 8.906/1994 — e LOMAN — LC 35/1979), aplicável a todas as peças. Registrar no relatório final quais dispositivos regimentais e das leis gerais impactaram a peça.
7. **Regra inviolável: nenhum fato, citação, jurisprudência ou número de processo pode ser inventado.** Tudo que entrar na peça tem de estar nos arquivos da pasta ou ser verificável. Se citar jurisprudência nova, verificar existência real; se não puder verificar, marcar [VERIFICAR] e avisar ao final.

## FASE 1.2 — EXPLORAÇÃO PROBLEMATIZADORA EM 100 PERGUNTAS (obrigatória em todo caso novo)

Depois da ingestão segura e da leitura integral, mas antes de pesquisa, conselho, blueprint ou redação, executar a subfase FORJA `F2-A`. Produzir exatamente **100 perguntas inteligentes, adaptadas ao caso**, distribuídas em **10 óticas com 10 perguntas cada**: mandato/resultado; fatos/cronologia; prova/fontes; processo/competência; direito/precedentes; adversário/julgador; riscos/ética/impactos; alternativas/soluções; quantificação/execução; comunicação/visual/validação.

Responder cada pergunta com âncora do caso, importância, natureza epistemológica e fonte/localizador quando a resposta for factual, processual, jurisprudencial ou numérica. Se não houver resposta verificável, registrar `blocked` + consequência + diligência; nunca completar a centena inventando. Consolidar: definição do problema, síntese diagnóstica, ao menos duas hipóteses de solução com condições e riscos, questões materiais abertas e roteamento nominal para F3–F7. Artefato interno canônico: `_FORJA_HARNESS\state\<caseId>\n4_artifacts\F2_QUESTION_TREE.json`, protocolo `FORJA-F2A-100-v1`. Questão material bloqueada impede F6/DOCX/PDF protocolável, mas segue a F3/F5 como pendência a resolver.

Contrato, óticas e comandos: `_FORJA_HARNESS\templates\F2A_EXPLORACAO_100_PERGUNTAS.md`. Validador: `python _FORJA_HARNESS\forja_exploracao_100.py validate <arquivo>`.

## FASE 1.5 — VARREDURA CRÍTICA DE ATRIBUIÇÃO + PREMISSA (obrigatória — vencedora do AutoResearch gen-0/gen-1, 08/07/2026)

Antes de qualquer estratégia ou redação, executar uma passagem de **verificação de fonte
primária** sobre tudo o que a peça vai citar. Esta fase não produz conteúdo — valida fundações.

**1.5-A — Precedentes verificáveis (gate DETERMINÍSTICO — endurecido pós-review adversarial 09/07/2026).**
Para cada precedente (jurisprudência, súmula, enunciado, tema), o status VERIFICADO só existe com
os QUATRO elementos: (1) número/identificador EXATO do julgado; (2) fonte oficial nomeada
(SCON STJ, portal STF, DJe do tribunal) com URL quando houver; (3) trecho LITERAL transcrito
(nunca paráfrase de memória — o erro real nº 1 da fábrica é atribuição errada, não inexistência);
(4) localização do trecho na decisão (ementa, voto, parágrafo) quando o teor sustentar tese central.
**Identidade ambígua nunca é VERIFICADO**: "jurisprudência consolidada", número aproximado,
julgado "análogo de memória" = pendente ou banido. Os 4 estados possíveis:

| Status | Quando | Consequência |
|---|---|---|
| VERIFICADO | 4 elementos presentes | entra na peça |
| RESTRITO | fonte de acesso restrito (autos sigilosos, repositório pago) | entra com [VERIFICAR: acesso restrito] + ponte declarada (Evento/fl. dos autos) + verificação humana pré-protocolo |
| INDISPONÍVEL-TRANSITÓRIO | fonte pública fora do ar/bloqueada NA SESSÃO | NÃO banir precedente possivelmente válido: reter com [VERIFICAR: indisponibilidade transitória] + registrar tentativa (data/fonte) + verificação humana obrigatória pré-protocolo |
| NÃO-ENCONTRADO | busca real em fonte aberta não localiza | BANIDO da redação; substituir por doutrina ou jurisprudência verificada |

**1.5-B — Premissas fáticas localizáveis.** Para cada fato crítico (data, evento processual,
decisão, documento): está nos autos? Referência exata ("Evento 185, fl. 59-62"). Fato público
(feriado, vigência de lei): fonte pública. Não acessível: [VERIFICAR: acesso offline].

**1.5-C — Proveniência interna × citação processual.** O ledger interno preserva a cadeia de
custódia e a versão da fonte. A peça converte essa informação em ponte processual e nunca revela
e-mail, WhatsApp, Drive, pasta, caminho local ou compartilhamento. “Documento juntado aos autos”
só pode ser usado se a juntada estiver confirmada; “documento anexo” apenas se o documento
acompanhar efetivamente a manifestação. Vazamento de origem operacional no produto final = P0.

**Saídas:** tabela "Precedentes Mapeados" (nome, tribunal, data, trecho, status VERIFICADO /
SECUNDÁRIO / BANIDO) e tabela "Premissas Mapeadas" (premissa, fonte, local exato, status).

**Marcação inline espelhada (inviolável, só no RASCUNHO):** todo item RESTRITO, INDISPONÍVEL-
TRANSITÓRIO ou A-VERIFICAR recebe TAMBÉM [VERIFICAR: motivo] no ponto exato do corpo do rascunho
onde é usado. A tabela organiza; o corpo confessa. Corpo limpo com tabela cheia = mentira por
omissão. **Separação ledger × peça (pós-review adversarial 09/07/2026):** as tabelas de
verificação e a Tabela de Premissas Críticas vivem em arquivo interno próprio
(`VERIFICACAO_<peça>.md` na pasta do caso) e nos rascunhos — NUNCA no .docx/.pdf final
protocolável; o documento final não carrega marcador [VERIFICAR] nem tabela de auditoria
interna (ver gate da Fase 4). **Gate:** nada avança sem estar no ledger; >2 precedentes
BANIDOS ou >3 pendências = declarar risco crítico no relatório.

## FASE 2 — CONSELHO DE GUERRA (usar /workflows com agentes paralelos)

Rodar um workflow multi-agente em que cada persona analisa o mapa do caso + a petição original e devolve contribuições estruturadas:

- **/helena** — estratégia geral: cenários de decisão, probabilidades, qual narrativa maximiza a chance de êxito, ordem dos argumentos.
- **/cicero** — jurídico: solidez das teses, requisitos formais da peça (admissibilidade, prequestionamento, prazos, técnica processual do tipo de peça), **conformidade com o regimento interno do tribunal (arquivo `REGIMENTO_INTERNO_*.md` da pasta) e com as leis gerais da pasta `_LEIS_GERAIS`**, retórica forense, jurisprudência aplicável.
- **/diabob** — red team: atacar a peça como faria a parte contrária e um julgador cético; listar toda fraqueza, contradição, alucinação herdada das versões de IA e ponto que pode irritar o juízo.
- **/maquiavel** — poder e incentivos: o que o julgador ganha/perde decidindo a favor; como alinhar o pedido aos incentivos institucionais do juízo; reputação e consequências práticas.
- **/sun-tzu** — terreno e timing: onde lutar e onde ceder; quais argumentos guardar; como vencer sem dar munição ao adversário; economia de esforço argumentativo.

Depois do fan-out, rodar uma etapa de **síntese adversarial**: consolidar as contribuições, resolver conflitos entre personas (decisão fundamentada, não média) e gerar o blueprint da peça final: estrutura, ordem dos argumentos, o que entra, o que sai, onde entram os diagramas.

## FASE 2B — ARSENAL HELENA + SIMULAÇÃO QUANTITATIVA DO JULGAMENTO

Além de participar do conselho, **/helena** atua como cientista-chefe e faz uma análise autônoma da causa. Ela deve:

1. **Curadoria do próprio arsenal**: revisar todo o instrumental dela (teoria dos jogos, Monte Carlo, análise de cenários, teoria da decisão, análise bayesiana, modelagem de stakeholders, análise quantitativa e qualitativa) e **escolher, justificando, quais ferramentas de fato ajudam ESTA petição** — não aplicar tudo por aplicar. Descartar explicitamente o que não agrega.

2. **Simulação Monte Carlo de julgamento com magistrados sintéticos**:
   - Construir um painel de **magistrados sintéticos** com perfis variados (garantista/legalista, formalista/pragmático, sensível a repercussão, avesso a risco, etc.), calibrados pelo tipo de juízo e pela peça original.
   - Para cada versão da peça (original vs. melhorada), simular milhares de julgamentos, cada magistrado sintético "votando" com base nos argumentos apresentados.
   - Rodar em **Python (numpy/pandas/scipy)** e, para as análises estatísticas e visualização, em **R** quando trouxer ganho (distribuições, intervalos de confiança, testes). Usar /python-executor e as skills de análise disponíveis.
   - Fazer análise de sensibilidade: **qual argumento/prova/diagrama, quando adicionado ou reforçado, mais move a probabilidade de êxito**. Isso vira uma priorização: onde investir persuasão.
   - Aplicar **teoria dos jogos** ao par autor↔adversário↔juízo: antecipar a melhor resposta da parte contrária e escolher a formulação da peça que maximiza o resultado esperado mesmo no pior cenário (minimax) — sem entregar munição.
   - Saída: estimativa quantitativa de probabilidade de vitória da versão original vs. melhorada, com o delta atribuído a cada melhoria, e ranking de melhorias por impacto.

3. **Ao final, Helena julga o próprio trabalho**: revisar o que usou, declarar o que **merece entrar** na peça e o que **não se aproveita**, o que foi conclusivo e o que ficou especulativo. Distinguir claramente: (a) melhorias com suporte quantitativo que entram na peça; (b) insumos que só orientam a estratégia interna (não vão para o texto); (c) o que foi descartado e por quê. **A simulação orienta a redação — não vira conteúdo da peça nem é citada como prova.** Nenhum número inventado de simulação pode ser apresentado ao juízo como fato.

O blueprint da Fase 2 deve incorporar o ranking de impacto da Helena: os argumentos e diagramas de maior efeito na simulação recebem posição de destaque e maior desenvolvimento.

## FASE 3 — REDAÇÃO DA SUPER-VERSÃO

1. Escrever a peça completa em português jurídico impecável, seguindo o blueprint.
2. **Dupla audiência**: a peça será lida por humanos E por IAs (assessores e tribunais já usam IA para triagem e resumo). Portanto:
   - Estrutura hierárquica limpa (títulos numerados, um argumento por seção);
   - Cada seção com tese enunciada na primeira frase (topic sentence extraível por IA);
   - Síntese executiva no início (o que se pede e por quê, em meia página);
   - Tabela-resumo dos pedidos ao final;
   - Fatos sempre ancorados em referência explícita à prova (fl./ID/doc), nunca soltos;
   - Zero ambiguidade em datas, valores e dispositivos legais.
3. **Dimensão de persuasão (usar /diana e /comunicacao-persuasiva)**: aplicar as melhorias priorizadas pela simulação da Helena com técnica retórica de alto nível — construir **imagens mentais** vívidas dos fatos (o julgador precisa "ver" a cena), usar **metáforas** jurídicas precisas e memoráveis para as teses centrais, ancorar cada argumento em enquadramento favorável, e calibrar ethos/pathos/logos. A persuasão trabalha o texto, não distorce o fato: toda imagem e metáfora tem de ser fiel ao que os autos provam.
4. **Revisão de citações, jurisprudência e fatos**: antes de fechar a redação, reconferir cada dispositivo legal, cada precedente e cada afirmação de fato contra os arquivos da pasta e contra a fonte oficial. Corrigir número, órgão, data e teor de julgados; nada de citação decorativa ou aproximada.
5. **Visual law**: invocar a skill **/fabrica-visual-peticoes** (pipeline oficial da fábrica) e criar diagramas SVG próprios (não genéricos) para as melhores ideias da peça — cronologia dos fatos, fluxo processual, quadro comparativo de teses, mapa da contradição/omissão apontada, matriz pedido→fundamento→prova. Complementar com /visual-law-inteia e /paperbanana-diagramas. Em Word, os diagramas entram VETORIAIS (SVG→EMF via Inkscape, inseridos via Word COM — `_FERRAMENTAS\word_visual_pipeline.py`; python-docx não aceita EMF). Paleta institucional Medina Osório (petróleo `#395C60`, terracota `#D9926A`), sóbria, sem "cara de IA". Cada elemento visual deve ter função cognitiva declarada (primazia, Von Restorff, dupla codificação, Gestalt, ancoragem) — nada decorativo.
6. **Padrão do escritório (INVIOLÁVEL)**: reproduzir cabeçalho, timbre, fonte, margens, assinatura e endereçamento exatamente como na petição original da pasta. Texto justificado, Arial 12 (ou a fonte da peça original), negrito mínimo e estratégico, sem linhas divisórias decorativas, espaçamento padrão ABNT-forense.
7. **CAUTELAS DE SÊNIOR (INVIOLÁVEL — mineradas dos retornos reais do escritório, 08/07/2026; fonte: `APRENDIZADOS_FEEDBACK_HUMANO.md`)** — aplicar antes de fechar qualquer minuta:
   - **Síntese executiva estilo art. 343-A do RISTJ no início de TODA peça**, qualquer tribunal: controvérsia, fundamentos e pedido em meia página (determinação do Prof. Fábio, padrão do escritório).
   - **Prequestionamento expresso**: "carimbar" nominalmente os dispositivos legais E constitucionais da tese, pensando no recurso seguinte (quando aplicável ao tipo de peça). Os constitucionais entram em **bloco/parágrafo dedicado** (tipicamente art. 93, IX — fundamentação — e art. 5º, LIV/LV — devido processo — quando a peça ataca omissão ou fundamentação), não em menção difusa; vale também para memoriais e peças de integração.
   - **Terminologia blindada de admissibilidade**: nunca linguagem que soe reexame de prova (Súmula 7/STJ, 279/STF); usar "omissão qualificada", "ausência de fundamentação individualizada", "erro de subsunção normativa".
   - **Fato superveniente em capítulo autônomo**, com enquadramento fino (relevância para integração/decisão, sem pretender efeito automático) — nunca diluído no argumento.
   - **Varredura de questões processuais laterais no mapa do caso** (antes do blueprint): prevenção (e se o momento de argui-la já passou), preclusão, distribuição/competência interna, composição ATUAL do órgão julgador, fatos supervenientes — mesmo que o pedido seja só "melhorar a peça".
   - **Em EDcl**: cada vício como PERGUNTA JURISDICIONAL OBJETIVA; insurgência de integração, não rediscussão; pedidos segmentados por vício; intimação da parte adversa se houver efeitos infringentes; distinguir categorias dogmáticas (dolo específico ≠ genérico ≠ culpa ≠ culpa in vigilando ≠ assunção de risco ≠ cegueira deliberada) quando houver imputação subjetiva.
   - **Visual como apoio, nunca eixo**: todo quadro/diagrama com a fundamentação analítica correspondente ao lado.

## FASE 4 — VALIDAÇÃO (gate obrigatório antes de declarar pronto)

1. Gerar o documento final em .docx E em .pdf.
2. Abrir o PDF e **inspecionar visualmente TODAS as páginas** (screenshot página a página): quebras de página, diagramas renderizados corretamente e não cortados, tabelas dentro da margem, numeração, cabeçalho/rodapé, acentuação completa.
3. Corrigir e regenerar até a diagramação estar perfeita — não entregar com defeito visual "pequeno".
4. Rodar checagem final anti-alucinação: reconferir cada citação legal, jurisprudencial e cada referência a prova contra os arquivos da pasta E contra o ledger da Fase 1.5.
4-bis. **Gate de pendências (BLOQUEANTE)**: o .docx/.pdf FINAL não sai enquanto existir no texto qualquer [VERIFICAR], tabela de auditoria interna ou precedente em status RESTRITO / INDISPONÍVEL-TRANSITÓRIO / NÃO-ENCONTRADO sem decisão humana registrada no ledger (verificado, aceito com risco nominado, ou removido). Pendência não resolvida = peça em rascunho, nunca "pronta".
4-ter. **Gate de Cautelas de Sênior**: rodar o checklist operacional VIGENTE de `APRENDIZADOS_FEEDBACK_HUMANO.md` (raiz da fábrica — arquivo vivo; usar a versão do dia, não contagem fixa de itens) aplicando a **matriz de aplicabilidade**: síntese 343-A e varredura de questões laterais são universais; prequestionamento, terminologia recursal, fato superveniente e regras de EDcl aplicam-se conforme o tipo de peça e o que existe nos autos — item inaplicável se registra como N/A com 1 linha de justificativa, sem criar seção vazia só para constar. Item universal ausente = peça NÃO está pronta.
5. Rodar /revisar-anti-ia no texto para eliminar marcas de texto de IA.
6. **Revalidar na simulação**: rodar a Monte Carlo da Helena sobre a versão FINAL redigida e confirmar que a probabilidade estimada de êxito subiu frente à original. Se alguma seção não melhorou o número, revisar antes de entregar.
7. Entregar na pasta: `<NOME>_SUPER_VERSAO_FINAL.docx` + `.pdf` + um `RELATORIO_MELHORIAS.md` curto explicando (para leigo): o que mudou em relação à original, quais contribuições de cada persona entraram, o que a simulação da Helena estimou (probabilidade original vs. final e as 3 melhorias de maior impacto), o que Helena escolheu do arsenal e o que descartou, quais riscos permanecem e o que ficou marcado [VERIFICAR], se houver.

## REGRAS DE EXECUÇÃO

- Autonomia total: não pedir confirmação intermediária; decidir e reportar ao final.
- Trabalhar sobre cópia; nunca sobrescrever os arquivos originais da pasta.
- Se faltar informação essencial (ex.: número do processo ilegível), sinalizar no relatório em vez de inventar.
- Tempo/custo não são restrição; qualidade máxima é o objetivo.
