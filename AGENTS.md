# AGENTS.md — Fábrica de Melhoria de Petições (instruções para Codex e qualquer agente de IA)

Este arquivo é o protocolo desta pasta para agentes não-Claude (Codex/GPT). As regras valem para TODA peça produzida, melhorada ou revisada em qualquer subpasta.

**Ele não é espelho do `CLAUDE.md`.** Medido em 03/08/2026: dos 107 trechos substantivos daqui, 78 não existem no `CLAUDE.md`, e 47 de lá não existem aqui — os dois compartilham 29. Antes de decidir com base neste arquivo, confira o outro; ao alterar um, decida explicitamente se a mudança vale para o outro. A reconciliação está pendente.

## 1. REGRA INVIOLÁVEL — Regimento do tribunal (exigência do chefe do escritório, 06/07/2026)

1. **Identificar o tribunal de análise** da peça (número CNJ, endereçamento, decisões nos autos). Segmento J4 = Justiça Federal (TR indica o TRF); 8.27 = TJTO; AREsp/REsp = STJ; RE/ARE = STF.
2. **Ler o `REGIMENTO_INTERNO_<TRIBUNAL>.md` da pasta do caso ANTES de redigir** (competência do órgão julgador, cabimento, processamento, prazos regimentais, sustentação oral, pauta, embargos, agravo interno). Se não existir, baixar a consolidação oficial mais recente, converter para .md com texto INTEGRAL (nunca resumo) e salvar na pasta com cabeçalho de metadados (fonte, versão/última emenda, data do download).
3. **Atualização até o dia da elaboração da peça**: pesquisar emendas regimentais/resoluções posteriores à consolidação indicada no cabeçalho e anexá-las na seção final do .md. A peça deve refletir o regimento vigente NA DATA DO PROTOCOLO.
4. **Considerar a pasta mãe `_LEIS_GERAIS`** em toda peça: Estatuto da OAB (Lei 8.906/1994) e LOMAN (LC 35/1979). Ver `_LEIS_GERAIS\LEIA-ME.md`.
5. **Registrar no relatório de melhorias** quais dispositivos regimentais e das leis gerais impactaram a peça (endereçamento, órgão competente, cabimento, prazo, sustentação oral etc.).

## 2. Mapa de tribunais das pastas existentes (verificado em 06/07/2026)

| Pasta | Tribunal | Regimento na pasta |
|---|---|---|
| Assunto Laudo Pericial Contábil – Proc. 0003453-28.1997.4.01.3400 | Justiça Federal / TRF1 | `REGIMENTO_INTERNO_TRF1.md` |
| Cafelana (Ação Rescisória 0037913-65.2011.4.01.0000) | TRF1 | `REGIMENTO_INTERNO_TRF1.md` |
| Cafelana\contrarrazões ao AgInt no AREsp nº 2.698.443D | STJ | `REGIMENTO_INTERNO_STJ.md` (também na raiz de Cafelana) |
| Memoriais Cautelar Fiscal | TRF4 | `REGIMENTO_INTERNO_TRF4.md` |
| Minuta de Embargos de Declaração — José Eduardo Siqueira Campos (AI 0011025-31.2023.8.27.2700) | TJTO | `REGIMENTO_INTERNO_TJTO.md` |

Avisos de atualidade: STJ consolidado até ER 47/2024 + ER 48–51 e 53 (junho/2026, mudaram competências de Turmas/Seções) em adendo; TRF1 consolidado até ER 5/2022 + posteriores em adendo (conferir Diário Eletrônico antes de peça crítica); TRF4 até Assento 35/2025; TJTO = Resolução 004/2001 integral + alterações posteriores em adendo.

## 3. Diagramação de excelência (obrigatório)

Arsenal instalado nesta máquina, documentado em `_FERRAMENTAS\LEIA-ME.md`:

- **Inkscape** (`C:\Program Files\Inkscape\bin\inkscape.exe`) — SVG → EMF vetorial (única forma de vetor de qualidade dentro do Word).
- **Graphviz** (`C:\Program Files\Graphviz\bin\dot.exe`) — fluxogramas por código DOT.
- **mermaid-cli** (`mmdc`, npm global) — timelines/fluxos por texto.
- **ImageMagick** (`magick`) — ajustes raster.
- **Tectonic** (`C:\Users\IgorPC\.local\tectonic\tectonic.exe`) — LaTeX autocontido (XeTeX), para edições visual law estilo revista.
- **MS Word via COM** (pywin32) — inserção de EMF e conversão docx→PDF de fidelidade máxima.
- Script pronto com todas as funções: `_FERRAMENTAS\word_visual_pipeline.py`.

Regras de ouro:
1. Diagramas dentro do Word SEMPRE vetoriais (EMF). Fluxo: SVG → `svg_para_emf` (Inkscape) → docx com parágrafos-marcador `{{FIG1}}` → `inserir_emf_word_com` (o próprio Word insere). **python-docx NÃO reconhece EMF — nunca usar `add_picture` com EMF.**
2. PDF final SEMPRE via Word COM (`docx_para_pdf`). Nunca pandoc/LibreOffice para a versão final.
3. Gate de QA visual obrigatório: `render_paginas` (pymupdf) + inspecionar TODAS as páginas antes de declarar pronto.
4. Edição LaTeX estilo revista: modelo validado em `Cafelana\_revista\CAFELANA_CR_EDCL_REVISTA.tex`. Armadilhas conhecidas: `\\` não pode ficar aninhado em grupos `{...}` de nós TikZ; `\rowcolors` exige `\usepackage[table]{xcolor}`; Palatino/Times não têm o glifo "→" — usar `$\to$`.
5. **Legibilidade (resolve fontes pequenas)**: texto de diagrama nunca abaixo de 8pt no tamanho final impresso (viewBox 600 @ 15cm → font-size ≥ 12px). `svg_para_emf(..., largura_final_cm=...)` reprova automaticamente; tokens únicos de estilo em `_FERRAMENTAS\estilo_medina.py` (CORES, `ESTILO_GRAPHVIZ`, `TEMA_MERMAID`, `aplicar_estilo_matplotlib()`). Contra o efeito inverso ("diagrama gigante"), calcular a largura de inserção com `estilo_medina.largura_recomendada_cm(svg, alvo_pt=10)` em vez de 15cm fixo.
6. **Imagens geradas por IA**: `gerar_imagem_ia(prompt, png)` (inference.sh). Permitido em capas de relatórios/pareceres ao cliente e ilustração institucional sóbria; PROIBIDO retratar fatos, pessoas ou provas em peça protocolada.

## 3-A. Padrão Word do escritório (obrigatório — extraído das peças reais)

Especificação completa: `_FERRAMENTAS\PADRAO_WORD_MEDINA_OSORIO.md`. Regras de ouro:
1. **Toda peça nova parte de `_FERRAMENTAS\TEMPLATE_MEDINA_OSORIO_PETICAO.docx`** ou de cópia da peça anterior do caso — o timbre é arte vetorial no cabeçalho da 1ª página, irreproduzível por código; documento criado do zero é PROIBIDO.
2. Times New Roman 12, justificado; entrelinhas 1,5 (federais/STJ) ou 1,15 (TJTO — seguir a peça anterior do caso); recuo de 1ª linha 2,0–2,5 cm (nunca 1,25 ABNT); margens esq 3,0 / dir 3,5 / inf 3,25.
3. 1ª página diferente: timbre + rodapé institucional; demais páginas: fólio (PAGE) em shape na margem direita, centralizado VERTICALMENTE na página, com filete inferior (design do template — confirmado no XML e no PDF protocolado).
4. Parágrafos numerados; títulos de seção em romanos negrito sem recuo; endereçamento em caixa alta negrito; fecho "Nestes termos, pede deferimento." + assinaturas centralizadas.


**Padrão visual aprovado (09/07/2026)**: a skill `padrao-visual-medina` (em `~\.claude\skills\`) é a referência visual OBRIGATÓRIA de toda petição desta fábrica — linguagem de design aprovada pelo Fábio/Igor (capa, síntese executiva, pull quotes, caixas, diagramas, quadro zebrado) nas versões LaTeX (V4) e Word (V1) do caso Cafelana, com processo de composição e receitas técnicas. Em conflito de precedência: fabrica-visual-peticoes rege protocolo/pipeline; padrao-visual-medina rege a linguagem visual. Kits reutilizáveis (09/07/2026): `_FERRAMENTAS\medina_visual_kit.py` (classe PecaVisual), `medina_svg_kit.py` (diagramas com gate de legibilidade + gate de overflow do viewBox) e `montar_visual.py` (EMF/PDF/render/anti-placeholder) — usar SEMPRE, nunca recriar. Peças validadas: Cafelana, EDcl José Eduardo (TJTO), Jalusa (TRF4), Memoriais LIBRA SUL (TRF4).

## 4. Identidade visual Medina Osório Advogados (obrigatória em toda peça)

- Logo em alta resolução: `Cafelana\_revista\logo_medina.png (fundo branco) / logo_medina_transp.png (fundo transparente — usar este sobre qualquer fundo que não seja branco puro)` (extraído da peça original, 600 dpi).
- Cores institucionais: verde-petróleo `#395C60`, terracota `#D9926A` (variante escura para impressão `#9C5B38`), grafite `#49494D`; painéis claros `#EFF4F3` (petróleo) e `#FBF2EC` (terracota).
- Corpo de texto: Times New Roman, justificado, parágrafos numerados; negrito mínimo e estratégico.
- Rodapé: linha fina petróleo + `www.medinaosorio.com.br` (esquerda) e `Brasília | Porto Alegre | Rio de Janeiro` (direita). Fólio na margem direita, centralizado verticalmente.
- Proibido "cara de IA": linhas divisórias decorativas, sombras, gradientes, excesso de negrito, fontes inconsistentes. Seguir o padrão das peças anteriores do escritório, nunca inventar diagramação de página.

## 5. Estratégia visual (não decorar — cada elemento tem função cognitiva)

Aplicar deliberadamente e documentar no relatório: primazia/recência (síntese executiva na abertura; quadro-resumo + pedidos no fim), Von Restorff (no máximo UMA caixa de destaque escuro por bloco argumentativo), fluência de processamento (numeração de parágrafos em cor institucional, topic sentences em negrito), dupla codificação (diagrama gêmeo junto de cada argumento-eixo), Gestalt (continuidade em timelines; destino comum em diagramas de convergência), ancoragem numérica (faixa de números-síntese do caso), padrão F (pull quotes na margem como camada de escaneamento). Referência aplicada: `Cafelana\_revista\RELATORIO_ESTRATEGIA_VISUAL.md`.

## 6. Erros recorrentes minerados das entregas reais (checar SEMPRE antes de entregar)

1. **Jurisprudência com atribuição errada** — verificar cada citação na fonte (SCON/STJ, STF); nunca confiar na memória do modelo.
2. **Premissa não declarada** (data de intimação, contagem de prazo, OCR não confirmado) — red team simulando a parte contrária; premissa sem prova vira "[VERIFICAR]" + bloqueador nominado.
3. **Placeholder esquecido no PDF final** (`[NOME]`, `[CRC-UF]`) — bloqueador P0; buscar `[` no texto final.
4. **Diagramação quebrada que só aparece no render** (texto estourando borda, legenda cortada, rodapé colidido) — o QA página a página é o único detector.

Casos-modelo: `Cafelana\AUDITORIA_FINAL_CAFELANA_SUPER.md` e `Jalusa...\DOCUMENTACAO_FINAL_APRENDIZADOS\03_APRENDIZADOS_ACERTOS_ERROS.md`. Visual law: se o elemento não reduz esforço cognitivo do julgador, sai da peça.

## 7. Anti-alucinação (inviolável)

Nenhum fato, citação, jurisprudência ou número de processo pode ser inventado. Tudo deve ser verificável nos arquivos da pasta ou em fonte oficial; o que não puder ser verificado recebe a marca [VERIFICAR] e é reportado ao final. Trabalhar sobre cópia; nunca sobrescrever os arquivos originais. Acentuação PT-BR completa em qualquer saída.

## 7-A. Tratamento e citação do acervo documental (inviolável — feedback Fábio, 11/07/2026)

1. Manter duas camadas rigorosamente separadas: **proveniência interna**, no ledger/relatório de auditoria, e **referência processual**, na peça.
2. A peça jamais revela a origem operacional do insumo. São proibidas fórmulas como “arquivo compartilhado pelo escritório”, “recebido por e-mail/WhatsApp”, “localizado na pasta”, “arquivo local/Drive” e caminhos de computador.
3. Na peça, usar apenas referências processuais verdadeiras: “documento juntado aos autos”, “e-STJ fl. X”, “evento/ID X”, “Doc. X — [título objetivo]” ou “documento anexo”. Não chamar de “juntado aos autos” o que ainda não foi protocolado nem de “anexo” o que não acompanhará a manifestação.
4. Marcadores de auditoria (`[FONTE: arquivo]`, `[DECLARAÇÃO]`, `[INFERÊNCIA]`, `[VERIFICAR]`) pertencem somente aos artefatos internos e nunca podem aparecer no DOCX/PDF protocolável.
5. Antes da liberação, executar o gate de origem operacional: qualquer menção a e-mail, WhatsApp, Drive, pasta interna, caminho local ou compartilhamento no corpo da peça é bloqueador P0.
6. Aplicar o protocolo canônico `PROTOCOLO_TRATAMENTO_E_CITACAO_ACERVO_PROCESSUAL.md`.

## 7-B. Processos volumosos e identidade dos atos recursais (inviolável — feedback Fábio, 11/07/2026)

Antes de redigir em processo volumoso, criar cronologia auditada e grafo dos atos. Cada recurso, decisão, retratação, destaque e intimação recebe identificador próprio, data, sujeito, classe/número, ato impugnado, pedido, efeito jurídico e ponte exata para os autos. É proibido usar “o recurso”, “o agravo” ou “a decisão anterior” quando houver mais de um ato possível. Sem a íntegra do ato atualmente impugnado e sem resposta às perguntas processuais críticas, a produção permanece `internal_working` e não gera nova versão protocolável.

## 7-C. Exploração inicial em 100 perguntas (inviolável — ordem do Igor, 14/07/2026)

Todo caso novo recebido por e-mail, WhatsApp/Hermes ou comando manual passa, após F1 e antes de pesquisa, conselho, blueprint ou redação, pela subfase `F2A_EXPLORACAO_PROBLEMA_100_PERGUNTAS`. O artefato `F2_QUESTION_TREE.json` deve usar `FORJA-F2A-100-v1`, conter exatamente 100 perguntas adaptadas ao caso, 10 em cada ótica canônica, e responder cada uma com classificação epistemológica e lastro quando factual. Lacuna não é resposta: fica `blocked`, com consequência e rota de diligência. A saída consolida problema, diagnóstico, pelo menos duas soluções e handoff para F3–F7. Questão material bloqueada impede peça protocolável. Contrato: `_FORJA_HARNESS\templates\F2A_EXPLORACAO_100_PERGUNTAS.md`; validador: `_FORJA_HARNESS\forja_exploracao_100.py`.

## 7-D. Prescrição administrativa e prova por e-mail (inviolável — Natura/Cabreúva, 15/07/2026)

Prescrição contra a Fazenda exige matriz por fundo de direito, metodologia, parcela, ato de negativa,
extensão e ciência; conclusão global sem essa decomposição é proibida. Requerimento por e-mail deve
separar envio, recebimento cognoscível, competência do canal e processamento. Modulação temporal vem
do dispositivo oficial, valor da parte é estimativa até conciliação parcela a parcela e PA, protesto
ou lei posterior não revivem automaticamente pretensão prescrita. Entrega ao escritório pode encerrar
a demanda operacional, mas não libera versão ao cliente/protocolo enquanto faltarem lastros materiais.

## 7-E. Revisão e escrita final pelo modelo editorial (inviolável — ordem do Igor, 25/07/2026)

**Esta determinação supera a de 15/07/2026, que fixava o Claude Fable 5.** Ambas foram registradas como invioláveis; prevalece a mais recente. O modelo editorial padrão é o **`claude-opus-5`**; o Fable 5 permanece autorizado como legado. A allowlist é `_FORJA_HARNESS\forja_editorial_model.py` — modelo fora dela não executa.

Toda nova tentativa F7 só entra na subfase controlada `F7-B_REVISAO_EDITORIAL_ESCRITA_FINAL` depois de `f7_gate_result.json` comprovar zero P0. O modelo é executado pelo Claude Code autenticado na assinatura OAuth Claude Max do Igor, sem API key, para revisar e reescrever exclusivamente a forma do texto auditado. A chamada é explícita por `forja_fable5.py`: `forja_run.py` não invoca o editor automaticamente. O texto jurídico é processado remotamente; não enviar segredos, credenciais ou material fora do caso e nunca registrar tokens de autenticação nos artefatos.

**Revisão cruzada entre famílias de modelo é gate de produção.** O trabalho pode nascer no Claude ou no Codex, mas a outra família revisa. O contrato do run declara `producerModel` e `reviewerModel`; o campo `familyAssurance` assume `cross_family`, `cross_session_same_family` ou `unverified`, recomposto pelo orquestrador e nunca aceito por declaração. O gate `cross_model_review_verified` bloqueia `unverified` em qualquer modo; em `strict_protocol` só `cross_family` libera. Se a segunda família estiver indisponível, o caso não para: rebaixa para `cross_session_same_family` **com o motivo registrado** — a degradação é permitida, o silêncio não.

O editor não pode criar ou alterar fatos, datas, números, valores, citações, autoridades, marcadores processuais, ressalvas, pedidos, fecho ou assinaturas. O orquestrador, e não o modelo, recompõe hashes e invariantes por `forja_editorial_fidelity.py`; divergência bloqueia a promoção e pode disparar nova tentativa a partir do `audited_markdown` original, até o limite do executor. `EDITORIAL_RESULT.json` é apenas o fragmento de gates e artefatos a incorporar ao `PHASE_RESULT.json`, nunca substituto deste — leitores ainda aceitam o nome anterior `FABLE5_RESULT.json`, assim como `editor_usage` aceita `fable5_usage`. `final_markdown` é o único cânone textual de F8 e dos pacotes novos; `audited_markdown` permanece como trilha interna. Os gates automáticos são escudos lexicais e estruturais, não prova de equivalência semântica nem substituto da auditoria F7 e da revisão humana. Contrato, executor e protocolo: `_FORJA_HARNESS\phase_contracts\F7.json`, `_FORJA_HARNESS\forja_fable5.py`, `_FORJA_HARNESS\forja_editorial_fidelity.py` e `_FORJA_HARNESS\PROTOCOLO_EDITORIAL_ESCRITA_FINAL.md`.

## 7-F. Assinatura visual da FORJA (inviolável — ordem do Igor, 30/07/2026; esteira reconstruída em 03/08/2026)

**Ordem:** nenhuma peça sai da FORJA sem elementos visuais completos. Nenhum caminho que passou pela FORJA entrega sem padrão visual completo. Sem atalhos, sem waiver, sem modo rápido, sem exceção para produto interno. O visual vale tanto quanto o conteúdo.

**Entrada ÚNICA de produção:** `_FORJA_HARNESS\forja_visual_build.py`. Fluxo: gates F7 → brief `F7_5_BRIEF_VISUAL.json` → mapa automático (`forja_visual_mapa_gen.py`) → figuras (`forja_visual_figuras.py` + geradores em `_FERRAMENTAS\medina_svg_kit.py`) → `forja_visual.compor()` → `montar_visual.py` (EMF/Word COM/PDF/QA) → gate F8-S (`forja_assinatura_visual.py`). ~7 a 15 segundos por peça, fidelidade textual 100%. O mapa manual `compor_<caso>_mapa.py` virou refinamento opcional, não pré-requisito.

**NÃO integrar `compor()` dentro de `forja_render_docx.render()`** — foi analisado e rejeitado: constrói a peça duas vezes, uma pobre e uma rica, e deixa dois DOCX parecidos na mesma pasta (modo de falha do caso Patrícia, Lição 48). O render simples é prévia; a produção passa pela entrada única.

**Brief F7.5** (`templates\F7_5_BRIEF_VISUAL.md`): o autor da peça declara âncoras da capa, cadeia argumentativa e cronologia. Custo de 1 a 2 minutos. Sem ele só saem as figuras estruturalmente seguras e peça longa não fecha o piso gráfico. **Nunca inferir conteúdo semântico de figura a partir de prosa argumentativa** — foi tentado e produziu cronologia misturando data do documento com prazo interno e fragmento de número CNJ lido como data, e cadeia de tese com a **tese da parte adversária** como elo do raciocínio da cliente. Cada frase era verbatim e o conjunto mentia. Figura fabricada é pior que figura ausente, porque parece prova.

**Estado do gate em 03/08/2026: modo OBSERVAÇÃO.** Grava `F8S_ASSINATURA_VISUAL.json` e não bloqueia; `forja_render_docx` segue ativo como rota alternativa. A ativação bloqueante foi ADIADA por decisão técnica, contrariando o conselho de quatro personas que fixara 06/08 — em três dias o gate teve três defeitos materiais, e instrumento com essa taxa de correção recente não pode barrar peça com prazo processual, onde o custo de errar é preclusão e não feiura. Reavaliar após período de produção real sem defeito novo. Ver nota de superação em `planejamento\25_CONSELHO_GATE_VISUAL_2026-08-03.md`.

**Gate de desenho do SVG (03/08/2026, bloqueante):** `_FERRAMENTAS\medina_svg_colisao.py` roda dentro de `word_visual_pipeline.svg_para_emf` — em TODO SVG que entra no Word, inclusive o desenhado à mão — e reprova oclusão de texto por forma opaca pintada depois (SVGC-01), texto sobre texto (SVGC-02) e cor sintaticamente inválida como `fill="ffffff"` sem `#` (SVGC-04); avisa sobre traço cruzando texto (SVGC-03) e contraste ilegível (SVGC-05). Existe porque o gate de presença (F8-S), o de legibilidade e o de overflow aprovam diagrama internamente quebrado. Calibrado nos 228 SVGs do acervo: 5 reprovações, todas confirmadas por render. **Contraste em 2,0:1 e não nos 3,0:1 da WCAG** — o terracota sobre painel terra da casa dá 2,3:1 e está aprovado. Regressão em `_FORJA_HARNESS\test_medina_svg_colisao.py`.

**Regras de engenharia que vieram das falhas (lições 87-99 em `RETROSPECTIVAS.md`):**
1. Recurso que depende de esforço manual por caso não sobrevive ao volume — foi por isso que a edição visual parou em 10/07 sem ninguém notar.
2. Gate que só procura defeito nunca detecta pobreza; é preciso a contraparte afirmativa, que verifica PRESENÇA.
3. Gate instalado na rota que ninguém percorre é gate nenhum — o elo 4-B era sério e rodou em 3 casos na história.
4. **Nunca detectar identidade visual por valor de cor**: a arte do timbre usa `3a5c61`/`d9936a`, um dígito fora dos tokens `395C60`/`D9926A`. Prova correta é estrutural.
5. Manter o **teste-âncora** contra a peça aprovada em 09/07: gate que reprova o padrão aprovado pelo dono está errado, não a peça.
6. Defeito só é defeito contra o padrão aprovado — os retângulos cinza da capa e o vazio inferior são identidade, não erro.
7. **Comitê de personas não substitui revisão de código**: o conselho leu o dossiê do construtor e recomendou arquitetura já rejeitada, citando função inexistente. A circularidade de autovalidação (quem constrói escreve o gate, mede com ele e se aprova) só foi quebrada pela revisão cruzada com a outra família de modelo, lendo o XML.

## 7-G. Gates computados — fim da autovalidação da esteira (04/08/2026)

Até 04/08/2026, 42 dos 73 gates declarados nos contratos de fase eram escritos pelo próprio agente que executava a fase: ele recebia `requiredGates` no `RUN_CONTEXT` e devolvia `pass` no `PHASE_RESULT`. Nenhum código conferia. Hoje os 73 são computados por produtor em Python.

**Se você vai afirmar algo sobre a cobertura da esteira, rode os medidores — não decore número daqui.**

- `python _FORJA_HARNESS/forja_gate_liveness.py` — quem decide cada gate (computado, autodeclarado, inexequível, não exercitado).
- `python _FORJA_HARNESS/forja_recomputo_censo.py` — o gate dispara sobre tentativa real? Executa cada produtor contra o acervo e conta vereditos.
- `python _FORJA_HARNESS/forja_artefatos.py` — vocabulário canônico dos artefatos e censo de deriva.

**Três vereditos, não dois.** `warn` existe para o que o gate não consegue conferir sem mentir `pass` nem reprovar formato aprovado. `not_applicable` existe para quando não há o que examinar — sem ele, "nada examinado" e "examinado e aprovado" saem idênticos.

**Ao construir ou alterar gate, as regras que vieram das falhas:**

1. Medir o acervo ANTES de fixar limiar. Três regras "óbvias" sobre ingestão morreram na medição; a pergunta jurisdicional é declarada em 4 de 15 blueprints; um `source_ledger` real tem dez fontes e nenhuma arquivada.
2. Toda regressão traz DUAS listas: o que deve reprovar e a contraprova com artefatos reais aprovados que não podem travar. Sem a segunda, o gate é calibrado contra a imaginação de quem o escreve.
3. Se TODOS os artefatos reais saem `pass`, suspeite de que o gate não mede o que afirma.
4. `fail` só para o verificavelmente falso; `warn` para o não verificável. Hash de cópia arquivada divergente é P0; hash de regimento divergente é `warn`, porque o protocolo manda atualizar aquele arquivo com as emendas posteriores.
5. Prova de que um gate existe é CHAMAR o produtor, nunca encontrar o nome por grep — dois gates do contrato F8 passavam no grep porque um script descartável escrevia `"pass"` à mão.
6. Vocabulário de artefato vem de `forja_artefatos.DIALETOS`, fonte única. Não recrie mapa de sinônimo local.

Detalhe por gate: `_FORJA_HARNESS/planejamento/06_GATES_QUALIDADE_FORJA.md`, seção "Levas 12 a 17". Lições 114-146 em `_FORJA_HARNESS/RETROSPECTIVAS.md`.

## 8. Hermes / gestão viva da fábrica (08/07/2026)

Quando a tarefa envolver painel de demandas, Gmail, WhatsApp/Hermes, entregas ao Fábio, áudios, status de cumprimento ou priorização de trabalho, usar a orientação persistente do Hermes:

- Skill: `C:\Users\IgorPC\.hermes\skills\fabrica-melhoria-peticoes\SKILL.md`
- Guia operacional: `C:\Users\IgorPC\.hermes\docs\HERMES-FABRICA-MELHORIA-PETICOES-2026-07-08.md`

O painel `gestao_escritorio\data\demandas.json` é quadro de comando, não prova jurídica. Antes de marcar uma demanda como cumprida, confirmar evidência de entrega em e-mail, WhatsApp, anexo arquivado ou intervenção manual documentada. Feedback do Fábio, erro detectado ou correção prática deve virar comentário/protocolo vinculado à demanda, sem transcrever conversa bruta de WhatsApp no chat ou no painel.

<!-- architecture-map-protocol:start -->
## Protocolo Archify + Graphify

- Antes de responder sobre arquitetura, dependências, organização ou localização, leia `00_MAPA_ARQUITETURA_IA/LEIA_PRIMEIRO.md` e `00_MAPA_ARQUITETURA_IA/DOCUMENTACAO_ARQUITETURAL_COMPLETA.md`.
- Use o diagrama de componentes `00_MAPA_ARQUITETURA_IA/FABRICA_PETICOES_ARCHITECTURE.html`, o fluxo operacional `00_MAPA_ARQUITETURA_IA/FABRICA_PETICOES_OPERATIONAL_FLOW.html` e o fluxo de confiança `00_MAPA_ARQUITETURA_IA/FABRICA_PETICOES_TRUST_DATAFLOW.html` conforme a pergunta.
- Consulte `00_MAPA_ARQUITETURA_IA/graphify-out/graph.json`/`graph.html` antes de varrer a pasta. O grafo diferencia estrutura extraída de decisões, cenários, falhas e fronteiras curadas.
- Relação `CURATED` ou `INFERRED` orienta navegação; confirme-a no contrato/arquivo local antes de mudança material. Estado vivo sempre exige verificação atual.
- Depois de mudança estrutural relevante, execute `C:\Users\IgorPC\.claude\projects\00_MAPA_ARQUITETURA_IA\REGENERAR_MAPAS_ARQUITETURA.py` e `C:\Users\IgorPC\.claude\projects\00_MAPA_ARQUITETURA_IA\APROFUNDAR_MAPAS_ARQUITETURA.py`, renderize e valide todos os HTMLs, consulte o grafo e atualize hashes.
- Em raízes jurídicas, não execute extração semântica crua sobre autos, mensagens, anexos, bancos, estado, telemetria ou credenciais. O mapa oficial é sanitizado e metadata-only.
- Estes artefatos complementam mapas canônicos; não substituem `MAPA.md`, `MAPA_IA.md`, `ESTADO_ATUAL.md`, manifestos, schemas ou documentação técnica local.
<!-- architecture-map-protocol:end -->
<!-- architecture-map-interfaces-v3:start -->
## Protocolo de interfaces inferiores

- Antes de alterar API interna, CLI, schema ou runner, leia `00_MAPA_ARQUITETURA_IA/INTERFACES_INFERIORES.md` e consulte `00_MAPA_ARQUITETURA_IA/graphify-out/graph.json`.
- Confirme arestas `AMBIGUOUS` no código; não trate resolução por nome como binding comprovado.
- Depois de mudança de contrato, regenere a camada v3, valide consumidores e execute os testes do subsistema.
<!-- architecture-map-interfaces-v3:end -->

<!-- strategy-v4:start -->
## Protocolo de decisão arquitetural

- Antes de refatorar, leia `00_MAPA_ARQUITETURA_IA/ANALISE_ARQUITETURAL_E_PROPOSTAS.md`.
- Proposta não é implementação concluída. Execute uma onda por vez e cumpra o critério de aceite.
- Preserve fachadas e consumidores durante migração; não execute big-bang.
- Recalcule o Graphify e atualize arquitetura-alvo quando uma proposta mudar de status.
<!-- strategy-v4:end -->

## Auto-research da fábrica — ciclo AR (23/07/2026)

A melhoria contínua da esteira tem processo próprio: o ciclo AR (`_FORJA_HARNESS\planejamento\22_PRD_AUTORESEARCH_FORJA.md` e `23_TDD_AUTORESEARCH_FORJA.md`, v1.1 pós-review adversarial Codex). Regras operacionais: (1) mudança em prompt/template/protocolo de fase que se pretenda "melhoria" deve passar pelo ciclo AR — execução pareada, julgamento cego com swap e duas famílias de juiz, canários de falha única e gate de promoção em três estados com recibo Ed25519; (2) indicadores de qualidade usam ledgers congelados pré-geração (cobertura E correção) — nunca criar métrica nova sem defesa anti-exclusão e âncora em falha real de `RETROSPECTIVAS.md`; (3) os segredos do ciclo (chave HMAC, registro sealed, canários secretos) vivem em `%USERPROFILE%\.forja_ar_secrets\` e jamais entram em repositório ou prompt; (4) enquanto não houver sealed prospectivo consumível, o subsistema opera em `estudo_descritivo` e NENHUMA variante é promovida a produção. Comandos e artefatos: ver bloco AUTO-RESEARCH em `_FORJA_HARNESS\INDICE_FORJA.md`.
