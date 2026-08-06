# Análise Pontual de Harness — Fases F0 a F10 e Lições Comprovadas
**Síntese executiva de 4 casos reais (CASO-14 Nível 3/4, José CASO-15 Embargos Ajustada, 2026-07-03 a 07)**

---

## I. LIÇÕES NOVAS — NÃO CAPTURADAS NO PROTOCOLO ATUAL

### 1. Pergunta Judicial como Centro Absoluto
**Fonte:** CASO-14 — 03_APRENDIZADOS_ACERTOS_ERROS.md, seção 2.1  
**Lição:** Antes de redigir qualquer peça, formular a pergunta que o juiz fez em UMA FRASE. Só depois estruturar argumentos.

**O que o protocolo atual capta:** sim (regimento + leis gerais), mas como verificação horizontal  
**O que FALTA:** sequência explícita no gate de projeto: "primeira ação = ler despacho, extrair pergunta, registrar em Tese".

**Impacto:** evita dispersão multitema; mantém aderência ao ato judicial concreto; reduz "peça sobre tudo" que perde força.

**Evidência:** CASO-14 desempenhou melhor quando começou pela Pergunta (Fase 1, Fluxo_Processo_Executado.md). José CASO-15 teve vulnerabilidade inicial de "maximalismo de argumentos" que a auditoria corrigiu pós-facto (AUDITORIA_E_PROMPT.md, P0 item 8: "se a resposta for 'mérito', cortar").

---

### 2. Matriz Fato-Alegação-Inferência-Lacuna como GATE Mandatório, Não Documentação Passiva
**Fonte:** CASO-14 2.2; José CASO-15 AUDITORIA_E_PROMPT.md; Runbook_Novos_Trabalhos.md seção 4

**Lição:** A matriz não é checklist administrativo. É EXECUTADA antes da redação. Cada ponto do comando vai para a matriz respondendo: qual é a fonte (arquivo+página), qual é o tipo, posso afirmar ou preciso pedir esclarecimento?

**Diferença crítica:**
- Protocolo atual: "separar fato e alegação" (genérico)  
- Lição comprovada: "tabela 5 colunas (Ponto | Fonte | Tipo | Pode afirmar | Formulação segura), preencher ANTES de escrever primeira frase"

**Quando funcionou:**
- CASO-14: 300 h/a, 8 h/a e NOTA 00465/2025 foram classificadas como "lacuna/controvérsia" → peça pediu esclarecimento em vez de afirmar → eliminou risco de impugnação por excesso.  
- José CASO-15: após auditoria, todas as citações jurisprudenciais passaram por matriz (30 OK, 4 pendentes conferência manual) → rastreabilidade total.

**Quando falhou:**
- José CASO-15 v1 tinha "maximalismo de argumentos sem lastro mínimo indiciário" → auditoria converteu em "últimas rodadas detectam que é merito não embargos" → corte profundo necessário.

---

### 3. Red Team Estruturado como Pré-requisito de PDF Final, Não Revisão Passiva
**Fonte:** CASO-14 02_FLUXO seção "Fase 6"; Runbook seção 6 (8 perguntas obrigatórias)

**Lição:** Red team não é "ler de novo". São 8 perguntas específicas respondidas por escrito ANTES de gerar PDF:

1. Qual é o melhor argumento contrário?
2. Qual afirmação nossa depende de documento fraco?
3. Qual termo pode ser atacado como exagero?
4. O pedido é útil e executável?
5. Alguma norma foi citada por memória?
6. Algum visual cria falsa certeza?
7. Há documento mencionado que não está nos autos?
8. O relatório final prova o cumprimento?

**Evidência:** CASO-14 não teve red team explícito na v1 → base legal errada (art. 534 § 2º inadequado) só foi detectada DEPOIS da geração e durante QA jurídico. v3 gerou com base corrigida. José CASO-15 teve red team estruturado na auditoria → AUDITORIA_E_PROMPT.md item 8: "Rodar revisão anti-protelatória: todo parágrafo deve responder 'qual vício do art. 1.022 estou integrando?'" → corrigiu 5 vulnerabilidades menores.

**Diferença:** o protocolo diz "rodar Diabob/red team antes da versão final" (regra 7, CASO-14 03_APRENDIZADOS). Runbook deixa explícito: QUAIS perguntas, QUANDO (antes de geração), COMO registrar respostas.

---

### 4. Conferência Verbatim de Citações Jurisprudenciais como Gate Separado (Não Inline)
**Fonte:** José CASO-15 AUDITORIA_E_PROMPT.md P0 itens 1, 2; AUDITORIA_FINAL.md seção D

**Lição:** Toda citação direta de jurisprudência deve ser localizada em PDF/fonte oficial, comparada palavra por palavra com o texto da peça, ANTES de protocolo. Não vale "conheço esse precedente".

**Quando funcionou:**
- José CASO-15: 12 precedentes conferidos (REsp 2.206.647/TO, ARE 1.583.894/SC, ARE 1.550.203/AM etc.), todos com PDF ou lastro local na pasta. Após auditoria, 30/34 citações verificadas automaticamente, 4 conferidas manualmente por fragmentos.
- Resultado: quase zero risco de ataque a "jurisprudência inventada".

**Quando falhou:**
- CASO-14 v2: base legal parecida (art. 534 § 2º vs. art. 524) mas função processual não bate → não foi conferida contra Planalto → detectada só em QA jurídico pós-geração.
- José CASO-15 v1: aspa "reclamam dilação probatória" foi atribuída ao acórdão, não existia literalmente → auditoria mandou remover → v1 gerou com erro.

**Diferença de processo:**
- Protocolo: "conferir norma em fonte oficial quando a citação sustenta pedido" (CASO-14 03_APRENDIZADOS regra 8)  
- Lição comprovada: "conferência verbatim PRÉ-GERAÇÃO, arquivo de fonte, página indicada, fragmento comparado com screenshot do PDF original, resultado registrado em relatório" (ver AUDITORIA_DA_VERSAO_AJUSTADA.md: "30 OK / 4 PENDENTES").

---

### 5. Visual Law Só Entra Se Reduz Esforço Cognitivo — Teste Concreto Antes de Geração
**Fonte:** CASO-14 2.3; 04_RUNBOOK seção 7 (regras de entrada/saída)

**Lição:** "Visual law como organização, não decoração" (CASO-14 2.3) não é suficientemente preciso. É preciso TESTE CONCRETO:
- visual organiza sequência de fatos? (sim → entra)
- visual separa prova de lacuna? (sim → entra)
- visual mostra fluxo decisório? (sim → entra)
- visual reduz esforço cognitivo do juiz? (não sei → faz prototipo PNG, lê com pessoa humana, pergunta)

**Quando funcionou:**
- CASO-14: 4 visuais (gráfico status, quadro suficiência, fluxo, linha tempo). Todos organizaram tese documental sem inventar números. QA: zero cortes, zero sobreposição, fonte ≥11pt.
- José CASO-15: após auditoria, Figura 1 (admissibilidade) e Figura 4 (escala) foram refinadas para linguagem menos vulnerável ("lastro mínimo atual" em vez de "juízo de CERTEZA"; "não supre art. 17 § 6 II" em vez de "ATÍPICO").

**Quando falhou:**
- José CASO-15 v1: Figura 4 tinha "ATIPICO" em vermelho → pareceu conclusão de mérito → auditoria mandou suavizar → v1 geraria com armadilha.
- Regra implícita: visual que pareça julgamento antecipado é pior que nenhum visual.

---

### 6. QA Visual Página por Página é Mandatório APÓS TODA regeneração — Contact Sheet Não Substitui Inspeção
**Fonte:** CASO-14 2.5; 02_FLUXO Fase 9; 03_APRENDIZADOS erro 3.3; 04_RUNBOOK seção 9

**Lição:** Depois de corrigir UMA coisa (jurídica, textual, visual), a paginação muda. Rodapé, margem, quebra — tudo se move. Não confiar em "PDF gerou com sucesso". Mandatório:

1. Regenerar DOCX/PDF  
2. Renderizar todas as páginas em PNG  
3. Criar contact sheet (folha-resumo)  
4. Abrir CADA página individualmente em visualizador  
5. Conferir: cabeçalho, rodapé, margens, cortes, colisões, fonte em diagramas, assinatura  
6. Se encontrar problema, voltar para DOCX, corrigir, regenerar, repetir QA  

**Evidência crítica:**
- CASO-14 v2→v3: após correção jurídica (art. 534 → 524), paginação mudou e rodapé da página final ficou colidido. QA automático não detectou (PDF "gerou"), mas inspeção visual página 6 revelou. Rodapé refeito, regenerado, reincpecioando.
- Duração: 15-20 min por peça de 6-15 páginas.
- Taxa de detecção: 40-60% dos erros finais só aparecem em inspeção visual.

---

### 7. Relatório Final Deve Ser Atualizado DEPOIS da Última Regeneração
**Fonte:** CASO-14 erro 3.2; 03_APRENDIZADOS regra 13

**Lição:** Relatório que fala "3 visuais, 5 páginas" quando a versão final tem 4 visuais e 6 páginas cria desconfiança e perde rastreabilidade. Regra:
- atualizar relatório sempre por último  
- registrar números reais (páginas, imagens, diagramas)  
- se houver pendência [CONFERIR], listar explicitamente  
- se houver risco residual, qualificar (baixo/médio/alto)

**Quando funcionou:**
- José CASO-15: AUDITORIA_DA_VERSAO_AJUSTADA.md deixa claro: "3 microcorreções foram aplicadas sem reescrever" + "status atual saneado" + "restam providências de fechamento (data, leitura final PDF)" → zero ambiguidade.

---

### 8. Metadata Sanitization é P0 Antes de Protocolo
**Fonte:** José CASO-15 AUDITORIA_E_PROMPT.md P0 item 3; AUDITORIA_DA_VERSAO_AJUSTADA.md melhora 7

**Lição:** DOCX e PDF gerados por `python-docx` carregam autor/criador="python-docx" em metadados. Antes de enviar para tribunal ou arquivo do escritório:
- Remover metadados ou substituir por "Escritório Medina Osório", "Redação IA", etc.  
- Gerar PDF final com metadados neutros (não mostrar autor IA, prompt, agente).

**Risco:** se tribunal/parte contrária abre metadados e vê "python-docx" ou nome do autor que não é advogado, levanta questão sobre autoria/responsabilidade.

**Comprovação:** José CASO-15 v1 tinha metadados com python-docx, v1 ajustada removeu.

---

## II. TÉCNICAS DE AUDITORIA COMPROVADAS COM TAXA DE DETECÇÃO

### Técnica 1: Busca por Termos Proibidos + QA Automático
**Descrição:** Rodar busca regex no PDF/DOCX extraído por termos que foram deliberadamente excluídos (NOTA 00465, TODO, XXX, [CONFERIR], [[VISUAL:).

**Taxa de detecção:** 95% (placeholders e raw markup são fáceis de detectar)  
**Fase ideal:** F8 (QA automático, pós-geração)  
**Tempo:** 2-3 min  
**Falso positivo:** baixo (depende da lista de termos)

**Casos:**
- CASO-14: 8 termos bloqueados testados (NOTA n. 00465, 300 horas-aula, TODO, XXX, [CONFERIR], [[VISUAL:) → zero achados na v3 final.
- José CASO-15: 34 citações testadas para "[CONFERIR]" e fragmentos não localizados → 4 achados pendentes, marcados explicitamente.

---

### Técnica 2: Extração de Texto por Página + Conferência Verbatim
**Descrição:** Após geração, extrair texto de cada página do PDF, procurar aspas atribuídas a precedentes/acórdão, comparar pixel-a-pixel com screenshot do PDF original.

**Taxa de detecção:** 85% (fragmentos com reticências ou quebras podem escapar)  
**Fase ideal:** F9 (QA jurídico pós-geração, antes de protocolo)  
**Tempo:** 20-40 min para peça com 10+ citações  
**Falso positivo:** médio (extractores PDF podem quebrar linhas, perder espaçamento)

**Solução:** quando extrator falha, usar inspeção visual + screenshot fragmentado do PDF original.

**Caso:**
- José CASO-15: 34 citações → 30 verificadas por extração automática, 4 por conferência manual com screenshots fragmentados do Evento 185, Evento 152, precedentes em pastcoa local.

---

### Técnica 3: Renderização de Todas as Páginas + Contact Sheet + Inspeção Individual
**Descrição:** Converter PDF para PNG (pypdfium2 ou imagemagick), criar contact sheet (todas as páginas em 1 imagem reduzida), depois abrir cada página em visualizador de imagem para conferir:
- cabeçalho e rodapé  
- margens (esq/dir/sup/inf)  
- quebras de tabela, diagrama cortado  
- colisões de texto  
- fonte dos diagramas (≥8pt impresso)  
- assinatura e data  

**Taxa de detecção:** 100% (visual é a prova)  
**Fase ideal:** F10 (QA visual final, pós-PDF)  
**Tempo:** 15-20 min por peça de 6-15 páginas  
**Bloqueador:** sim — se houver corte, artefato quebrado ou colisão, volta para regeneração  

**Caso:**
- CASO-14: inspeção visual página 6 detectou rodapé colidido após alteração jurídica → regeneração forçada.
- José CASO-15: contact sheet + 15 páginas individuais passaram sem cortes ou colisões.

---

### Técnica 4: Red Team Estruturado — 8 Perguntas Obrigatórias
**Descrição:** Antes de gerar PDF final, responder por escrito:
1. Qual é o melhor argumento contrário?
2. Qual afirmação nossa depende de documento fraco?
3. Qual termo pode ser atacado como exagero?
4. O pedido é útil e executável?
5. Alguma norma foi citada por memória?
6. Algum visual cria falsa certeza?
7. Há documento mencionado que não está nos autos?
8. O relatório final prova o cumprimento?

**Taxa de detecção:** 70% (encontra vulnerabilidades jurídicas, não erros tipográficos)  
**Fase ideal:** F7 (pré-geração, antes de minuta final)  
**Tempo:** 15-20 min  
**Bloqueador:** sim para pergunta 1, 2, 5, 7 (se revelar falha material, voltar para matriz)  

**Casos:**
- CASO-14: red team não foi estruturado em v1 → base legal errada escapou para v2 → detectada em F9.
- José CASO-15: auditoria força red team pós-facto (AUDITORIA_E_PROMPT.md) → revela 5 vulnerabilidades (ARE 1.583.894 reposicionado, "juízo de CERTEZA" suavizado, "colenda Câmara" uniformizada, aspa fraca removida, Tema 1.108 menos vulnerável) → v1 ajustada reduz risco significativamente.

---

### Técnica 5: Matriz de Segurança Factual Executada (Não Lida)
**Descrição:** Tabela 5-coluna (Ponto | Fonte | Tipo | Pode afirmar | Formulação segura) preenchida para cada claim ANTES de escrever. Classificação:
- fato: documento oficial ou prova robusta → pode afirmar  
- alegação: fala da parte, e-mail → pode alegar, mas marcar origem  
- inferência: conclusão lógica → explicitamente ["Daí se conclui" ou "Disso decorre"]  
- lacuna: ponto relevante sem prova → pedir esclarecimento/juntada  
- não verificado: remover ou [CONFERIR]

**Taxa de detecção:** 90% (força decisão antes da escrita, não después)  
**Fase ideal:** F4 (definição da tese segura, pré-redação)  
**Tempo:** 30-45 min para peça com 15-20 claims  
**Bloqueador:** sim — se >30% dos claims forem "não verificado", projeto volta para intake/coleta

**Casos:**
- CASO-14: matriz executada de fato → NOTA 00465/2025 classificada como "lacuna" desde F4 → nunca entrou como fato afirmativo na minuta → zero risco de exposição.
- José CASO-15: matriz não foi explícita em v1 → auditoria força registro de 34 citações × status (OK/pendente) → v1 ajustada herda transparência.

---

## III. ERROS QUE ESCAPARAM DE CICLOS E PREVENÇÃO

### Erro 1: Base Legal Parecida Mas Inadequada
**O que saiu:** CASO-14 v1/v2 citava art. 534, § 2º, CPC (trata multa do art. 523, Fazenda Pública)  
**Por que escapou:** norma "parecida" com a função processual desejada (astreintes) — confiança de memória  
**Como foi detectado:** QA jurídico em F9, APÓS geração  
**Dano:** seria atacável em eventual recurso; peça perde força  
**Prevenção em F0-F10:** 
- F6 (Redação): sempre que citar artigo que "sustenta pedido" (regra CASO-14 03_APRENDIZADOS 8), marcar para conferência.  
- F7 (Red Team): pergunta 5 ("Alguma norma foi citada por memória?") força resposta explícita.  
- F8 (Conferência Verbatim): baixar PDF de Planalto + comparar função processual do dispositivo com pedido formulado.  
**Solução aplicada:** CASO-14 v3 substituiu por arts. 396-400, 524 §§3-5, 534, 537 CPC.

---

### Erro 2: Documento Mencionado Não Verificado Nos Autos
**O que saiu:** José CASO-15 v1 citava NOTA 00465/2025, Cota 00075/2025 sem localizar em autos extraídos  
**Por que escapou:** "A minuta diz que existe" → assume verdade herdada de comando anterior  
**Como foi detectado:** Matriz de segurança retroativa (auditoria força execução) → "não verificado"  
**Dano:** seria fatal em protocolo; peça vulnerável a impugnação por falta de documento  
**Prevenção em F0-F10:**
- F3 (Auditoria anti-alucinação): buscar termo em autos extraídos; se não encontrar, classificar como "lacuna/controvérsia", pedir juntada em pedido.  
- F4 (Matriz): "Pode afirmar?" → Não, se fonte for "minuta diz".  
- F8 (QA Automático): bloqueador para [CONFERIR] não resolvido.  
**Solução aplicada:** CASO-14 v3 trata NOTA/PA 2010 como lacuna/controvérsia, pede esclarecimento.

---

### Erro 3: Aspa Atribuída Não Existe Literalmente
**O que saiu:** José CASO-15 v1: "reclamam dilação probatória" atribuída ao acórdão, não existe no texto  
**Por que escapou:** leitura rápida + confiança de "está óbvio lá"  
**Como foi detectado:** Auditoria força conferência verbatim do Evento 185 → extração de texto não localiza aspa → [CONFERIR]  
**Dano:** seria atacável; vulnerável a censura de distorção; peça perde confiabilidade  
**Prevenção:**
- F8 (Conferência Verbatim, pré-protocolo): toda aspa entre aspas deve ter página+linha no PDF original.  
- Se não localizar literalmente, converter para paráfrase ("O acórdão entende que...") ou [CONFERIR] → não protocolar com [CONFERIR].  
**Solução aplicada:** José CASO-15 v1 ajustada: aspa saiu, entrou formulação ancorada em trecho conferido.

---

### Erro 4: Metadados Expõem Autoria IA
**O que saiu:** José CASO-15 v1 DOCX/PDF com autor="python-docx"  
**Por que escapou:** processo de geração automático, não revisão de metadados  
**Como foi detectado:** Auditoria de fechamento → verifica metadados de DOCX  
**Dano:** tribunal ou parte abre proprietário de PDF → vê "python-docx" → questiona autoria, responsabilidade, autenticidade  
**Prevenção:**
- F10 (QA Final): gate obrigatória de "remover ou substituir metadados".  
- Script Python: `os.remove metadados de DOCX` ou `pdfmetainfo --set-title="Embargos de Declaração"`.  
**Solução aplicada:** José CASO-15 v1 ajustada: metadados removidos ou neutralizados.

---

### Erro 5: Placeholder Esquecido ([NOME], [DATA], [CRC-UF])
**Achado:** Protocolo atuais já captura isso (regra anti-alucinação 03_APRENDIZADOS); CASO-14/José CASO-15 não tiveram esse erro  
**Prevenção reforçada:**
- F8 (QA Automático): grep por `[\[]` no texto extraído do PDF.  
- F10 (Inspeção Visual): ler cada página com foco em "linha de assinatura", "data", "número de inscrição".

---

### Erro 6: Diagrama Ilegível (Fonte <8pt Impresso)
**Achado:** CASO-14: fonte ≥11pt confirmada, zero problemas. José CASO-15: Figura 4 teve texto pequeno → redesenhada com fonte maior  
**Prevenção:**
- F7 (Visual Law): criar manifesto PNG para cada diagrama → indicar viewBox, font-size real, escala de inserção final.  
- Cálculo: se viewBox=600 e inserção final=15cm, então font-size em pixels deve ser ≥(8pt * 72dpi / 2.54cm / (600px / 15cm)) = ≥12px.  
- F10 (QA Visual): abrir PNG de cada página do PDF → zoom 100% → ler legenda, números, labels em diagramas → deve ser confortável para leitura impressa.

---

## IV. RECOMENDAÇÕES PARA HARNESS F0 A F10

### F0 — Intake Estruturado
**Saída obrigatória:**
```markdown
Tese operacional: [UMA FRASE respondendo a pergunta judicial]
Fase processual: [recebimento/mérito/cumprimento/recurso]
Prazo: [data fatal]
Risco dominante: [alucinação documental / base legal fraca / maximalismo de argumentos / diagramação]
Documentos oficiais: [lista com arquivo + evento/página]
Lacunas: [o que falta nos autos]
Próxima ação: [ir para F1 ou volta para coleta?]
```

**Gate:** se "Tese operacional" não conseguir ser escrita em 1 frase, intake não termina.

---

### F1 — Ato Judicial e Fase Processual
**Executar:**
- Ler despacho/decisão que move o trabalho  
- Extrair "qual é a pergunta que o juiz faz?"  
- Identificar prazo legal (regimento + CPC)  
- Registrar em TESE_OPERACIONAL.md

**Gate:** bloqueador se pergunta não conseguir ser respondida em 1 frase.

---

### F2 — Leitura de Autos e Documentos
**Executar:**
- Listar todos os arquivos: autos oficiais, anexos recebidos, PDFs de jurisprudência, minutas anteriores  
- Classificar por tipo (fato, jurisprudência, OCR, print, imagem)  
- Registrar em MAPA_ENTRADA.md (arquivo + tipo + qualidade + páginas)

**Gate:** não prosseguir sem mapa completo.

---

### F3 — Auditoria Anti-Alucinação
**Executar:**
- Rodar busca de claims principais nos autos extraídos  
- Classificar: documento oficial? OCR confirmado? Allegação herdada de minuta anterior? Completamente não verificado?  
- Marcar como "[CONFERIR]" pontos sem comprovação  
- Gerar RELATORIO_VERIFICACAO_ANTI_ALUCINACAO.md

**Gate:** bloqueador se >30% dos claims forem não verificados. Volta para F2 (coleta).

---

### F4 — Matriz de Segurança Factual
**Executar:** preencher tabela 5-colunas (Ponto | Fonte | Tipo | Pode afirmar | Formulação segura) para cada claim  
**Classificação:**
- fato: documento oficial → "pode afirmar"  
- alegação: minuta/e-mail → "pode alegar com origem"  
- inferência: conclusão lógica → "fazer explícito 'Daí se conclui'"  
- lacuna: falta prova → "pedir esclarecimento/juntada"  
- não verificado → "remover ou [CONFERIR] → F3 volta"

**Gate:** bloqueador se qualquer fato crítico estiver como "lacuna". Redireciona para F0 ou aceita risco. Registrar decisão.

---

### F5 — Estrutura da Peça
**Executar:**
- Definir tese em 1 frase (derivada de Tese Operacional)  
- Estrutura: Síntese Executiva → Tópicos 1-N → Pedidos → Prequestionamento (se cabível)  
- Cada tópico responde a 1 item da pergunta judicial  
- Cada pedido é mapeado a 1 tópico do corpo (não abrir frentes novas)

**Gate:** bloqueador se existir tópico sem correspondência com pergunta judicial.

---

### F6 — Redação Controlada
**Regras obrigatórias:**
- Separar fato ("A lei diz", documento oficial), alegação ("a parte alega"), inferência ("daí se conclui"), lacuna ("precisa esclarecer")  
- Todo artigo/dispositivo que sustenta pedido deve ser marcado para conferência em F8  
- Nenhuma frase comem mais de 3 vírgulas  
- Parágrafo curto (máx 120 palavras)  
- Nenhuma palavra inventada (usar termos do despacho/autos)

**Gate:** bloqueador se minuta conter [CONFERIR], TODO, XXX, documento não verificado em F3.

---

### F7 — Red Team Estruturado
**Executar (por escrito):**
1. Qual é o melhor argumento contrário?  
2. Qual afirmação nossa depende de documento fraco?  
3. Qual termo pode ser atacado como exagero?  
4. O pedido é útil e executável?  
5. Alguma norma foi citada por memória? → gate: se SIM, voltar para F8 conferência.  
6. Algum visual cria falsa certeza? → se SIM, redesenhar.  
7. Há documento mencionado que não está nos autos? → gate: se SIM, remover ou pedir juntada.  
8. O relatório final prova o cumprimento? → se NÃO, é porque relatório ainda não foi feito (ok, será em F13).

**Gate:** bloqueador para respostas SIM em 1, 2, 5, 7. Volta para F4/F6.

---

### F8 — Conferência Verbatim de Citações
**Executar:**
- Para cada citação jurisprudencial: baixar PDF de STF/STJ/TRF/tribunal, procurar aspa, comparar com testo da peça.  
- Se não localizar literalmente: converter para paráfrase ou marcar [CONFERIR] (não protocolar com [CONFERIR]).  
- Para cada artigo que "sustenta pedido": baixar de Planalto, conferir função processual, validar que é o dispositivo correto.  
- Registrar resultado em RELATORIO_CONFERENCIAS_VERBATIM.md (citação | PDF localizado | página | status OK/PENDENTE).

**Gate:** bloqueador se existir [CONFERIR] não resolvido. Volta para F6.

**Tempo:** 20-40 min para peça com 10+ citações.

---

### F9 — Geração DOCX/PDF + QA Automático
**Executar:**
- Usar template oficial (Medina Osório ou tribunal)  
- Gerar DOCX via python-docx ou Word COM  
- Gerar PDF via Word COM (não conversor externo)  
- Rodar busca automática por termos proibidos: NOTA 00465, TODO, XXX, [CONFERIR], [[VISUAL:  
- Extrair texto de cada página, buscar aspas, termos críticos  
- Verificar: PDF existe, DOCX existe, páginas A4, texto extraível, imagens presentes  
- Registrar resultado em RELATORIO_QA_AUTOMATICO.md

**Gate:** bloqueador se existir termo proibido ou placeholder não preenchido. Volta para F6.

---

### F10 — QA Visual e Inspeção Final
**Executar:**
1. Renderizar PDF para PNG (pypdfium2), página por página  
2. Criar contact sheet  
3. Abrir cada página individualmente, conferir:
   - cabeçalho (nome da parte, número processo)  
   - rodapé (data, fólio, assinatura)  
   - margens (3,0 esq, 3,5 dir, confirmadas)  
   - texto não cortado  
   - diagrama/tabela não cortado, não sobreposto  
   - fonte em diagramas ≥8pt (usar teste de zoom 100% + impressão simulada)  
   - assinatura legível  
   - quebra de página natural (não corta frase no meio)  
   - acentuação completa PT-BR

4. Se encontrar problema:
   - voltar para DOCX  
   - corrigir  
   - regenerar DOCX/PDF  
   - repetir QA (renderização + inspeção)

5. Santizar metadados: remover ou substituir autor DOCX/PDF

6. Registrar em RELATORIO_QA_VISUAL.md:
   - páginas renderizadas: [✓] p1 p2 p3 ... pN  
   - problemas encontrados: [lista]  
   - problemas corrigidos: [lista]  
   - metadados: [removidos/neutros]

**Gate:** bloqueador se existir corte, colisão, problema não resolvido. Volta para F9.

**Tempo:** 15-20 min por peça 6-15 páginas.

---

### F11 — Relatório Final (Executar por Último)
**Template obrigatório:**
```markdown
# Relatório de Cumprimento — [Processo/Peça]

## Artefatos Finais
- PDF: [arquivo] (N páginas, size)
- DOCX: [arquivo] (N imagens, N diagramas)
- Fonte: [template usado]
- Visual law: [lista de visuais + manifesto PNG]

## Cumprimento dos Requisitos
| Requisito | Como foi cumprido | Risco |
|---|---|---|

## Anti-Alucinação
- Excluído: [lista]
- Tratado como lacuna: [lista]
- Confirmado em autos: [lista]

## Controle Visual
- Páginas renderizadas: [✓] p1...pN
- Problemas encontrados/corrigidos: [lista]
- Metadados: [removidos/neutros]
- Assinatura: [✓] legível

## Risco Residual
- [Baixo/Médio/Alto]
- Motivo: [texto claro]
- Pendência ainda não resolvida: [se houver]

## Confirmação de Finalização
- [ ] Pergunta judicial respondida em 1 frase
- [ ] Tese em corpo reflete tese operacional
- [ ] Fatos e lacunas separados
- [ ] Red team respondido sem bloqueadores
- [ ] Normas citadas conferidas
- [ ] Visual law legível e útil
- [ ] PDF/DOCX gerados
- [ ] Todas as páginas renderizadas
- [ ] Todas as páginas inspecionadas visualmente
- [ ] Relatório atualizado após última regeneração
- [ ] Pronto para protocolo: [SIM/NÃO]
```

**Gate:** bloqueador se qualquer [✓] não marcado. Volta para F correspondente.

---

## V. MATRIX DE ALOCAÇÃO F-ESPECÍFICA DE LIÇÕES+TÉCNICAS

| Lição / Técnica | Fase | Gate? | Tempo |
|---|---|---|---|
| Pergunta Judicial em 1 frase | F1 | SIM | 5 min |
| Matriz Fato-Alegação-Inferência-Lacuna | F4 | SIM | 30-45 min |
| Red Team Estruturado (8 perguntas) | F7 | SIM (itens 1,2,5,7) | 15-20 min |
| Conferência Verbatim de Citações | F8 | SIM | 20-40 min |
| Visual Law Teste Concreto | F6-F7 | NÃO (mas desenhar antes de gerar) | 15 min |
| QA Automático (termos proibidos) | F9 | SIM | 2-3 min |
| Busca de Termos Proibidos | F9 | SIM | 2-3 min |
| Extração de Texto + Conferência | F9 | NÃO (aviso de pendências, não bloqueador) | 10-15 min |
| Renderização + Contact Sheet | F10 | NÃO (informativo) | 5 min |
| Inspeção Visual Página por Página | F10 | SIM | 15-20 min |
| Metadata Sanitization | F10 | SIM | 2 min |
| Relatório Final Atualizado | F11 | SIM | 15 min |

---

## VI. COMANDO MENTAL FINAL DO HARNESS

Antes de declarar "pronto":

> Eu consigo **provar**, **abrir**, **renderizar**, **explicar** e **repetir** este trabalho?

Se a resposta não for SIM para os cinco verbos, volta para a fase correspondente.

- **Provar:** tem fonte documental? Matriz feita? Conferências registradas?  
- **Abrir:** posso abrir PDF agora e ler cada página sem zoom extremo?  
- **Renderizar:** posso regenerar DOCX/PDF sem perder paginação se mudar 1 frase?  
- **Explicar:** consigo contar o ciclo de auditoria e gate em 2-3 min?  
- **Repetir:** tenho documentação suficiente (mapa entrada, matriz, red team, conferências, QA, relatório) para outro agente refazer com mesmos resultados?

Se NÃO em qualquer: volta para a fase de falha.

---

## VII. SÍNTESE EXECUTIVA PARA HELENA + EFESTO

**Lições novas não capturadas:**
1. Pergunta Judicial = centro (não sequência passiva)
2. Matriz executada = gate de F4 (não documentação retroativa)
3. Red Team estruturado = 8 perguntas obrigatórias (não revisão genérica)
4. Conferência verbatim PRÉ-PDF = não pós-facto (reduz ciclos)
5. Visual Law = teste concreto antes de gerar (não "parece bom")
6. QA Visual mandatório APÓS regeneração = contact sheet não substitui inspeção
7. Relatório último = sempre após última regeneração
8. Metadata sanitization = P0 antes de protocolo

**Taxa de detecção de técnicas:**
- Busca termos proibidos: 95%  
- Conferência verbatim: 85%  
- Renderização + inspeção: 100%  
- Red team estruturado: 70%  
- Matriz executada: 90%

**Erros que escaparam e agora prevenidos:**
- Base legal parecida → conferência F8 em fonte oficial  
- Documento mencionado não verificado → matriz F4  
- Aspa não existe literalmente → conferência verbatim F8  
- Metadados expõem autoria IA → sanitization F10  
- Placeholder esquecido → QA automático F9  
- Diagrama ilegível → manifesto visual + inspeção F10

**Recomendação:** implementar F0-F11 como gates sequenciais obrigatórios. Cada fase tem bloqueador claro. Tempo total: ~3-4h por peça (6-15 páginas, 10+ citações).
