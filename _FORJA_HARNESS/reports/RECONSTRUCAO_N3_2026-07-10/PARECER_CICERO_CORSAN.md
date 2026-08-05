# Parecer de auditoria adversarial — Diagnóstico CORSAN/AGERST

**Data de corte:** 10 de julho de 2026  
**Gênero auditado:** diagnóstico jurídico-regulatório preliminar e delimitação de escopo  
**Objeto:** verificar a confiabilidade jurídica e documental do diagnóstico produzido, sem reescrever o trabalho  
**Resultado:** **BLOQUEADO PARA CIRCULAÇÃO OU USO DECISÓRIO NA FORMA ATUAL**

## 1. Resultado jurídico direto

[FONTE] O diagnóstico tem boa organização temática e reconhece que a base é parcial, mas falha justamente nos controles centrais exigidos pela consulta: inventário completo, separação entre documento e inferência, classificação de risco sem percentuais rígidos e respeito ao limite do gênero consultivo.

[FONTE] A falha mais grave é objetiva: o diagnóstico afirma repetidamente que a Minuta de Resolução tem 8 páginas e que o Anexo Único não foi recebido. O arquivo local `MINUTA - RESOLUÇÃO.pdf` tem **22 páginas**; a página 10 inicia o **ANEXO ÚNICO**, e as páginas 11 a 22 contêm a matriz de cláusulas, dispositivos e fundamentos. A extração local encontrou 47 ocorrências de rótulos iniciados por “Cláusula/Cláusulas”, além de itens e subitens agrupados.

[FONTE] O segundo erro factual altera o cronograma: o edital informa consulta pública de **06/07/2026 a 04/08/2026** e audiência pública em **11/08/2026, às 14h**, na Câmara de Vereadores. O diagnóstico e o e-mail de encaminhamento dizem que a data estava indefinida, que a janela terminaria em 31/07 e que a votação seria provável ainda em julho.

[INFERÊNCIA] Como o documento não leu integralmente um anexo que estava disponível e construiu risco, prazo, estratégia, custos e probabilidades sobre essa premissa falsa, não basta corrigir trechos isolados. A análise substantiva precisa ser refeita desde o inventário documental.

## 2. Cânone, fontes e estado real

### 2.1 Versões examinadas

- [FONTE] Fonte substantiva: `_FORJA_HARNESS/state/case-email-corsan-agerst-19f3dc9ff92081cd/producao/DIAGNOSTICO_CORSAN_AGERST.md`, 565 linhas, modificado em 09/07/2026.
- [FONTE] Edições correspondentes: `DIAGNOSTICO_CORSAN_AGERST.docx` e `.pdf`; a comparação local encontrou cobertura textual praticamente integral da fonte Markdown.
- [FONTE] Edição visual: `producao/_visual/DIAGNOSTICO_CORSAN_AGERST_VISUAL_LAW.docx` e `.pdf`.
- [LACUNA] O estado FORJA aponta o rascunho visual como substituto, mas o DOCX/PDF não visual possui horário de modificação posterior. Não existe manifesto canônico que resolva, por hash, qual arquivo deve ser revisado. Esta auditoria usa o Markdown como fonte substantiva e trata todas as saídas como derivadas do mesmo conteúdo.

### 2.2 Documentos locais decisivos

| ID | Documento | Integridade local | Função |
|---|---|---:|---|
| C1 | `COMANDO_DO_EMAIL.md` | disponível | pedido interno do escritório |
| C2 | `Consulta preparatória para Diagnóstico Preliminar de Riscos e Escopo de Atuação Jurídica.docx` | SHA-256 `A32F0335...ACA5` | delimita o gênero e o escopo da consulta |
| C3 | `DIRETRIZES PARA ORIENTAR A IA NA ANÁLISE DOCUMENTAL.docx` | SHA-256 `AC3D4A73...ED2` | regras de análise e limites da entrega |
| C4 | `METODOLOGIA DE CLASSIFICAÇÃO DE RISCO JURÍDICO E PROBABILIDADE DE PERDA.docx` | SHA-256 `4B714914...7941` | método obrigatório de risco |
| C5 | `Parecer 491.2026 - Proc. Adm. 61.2026 - Apuração Desestatização.pdf` | 114 páginas; SHA-256 `D78A7856...CDAB` | posição jurídica da AGERST/Procuradoria |
| C6 | `MINUTA - RESOLUÇÃO.pdf` | 22 páginas; SHA-256 `5DE19177...6864` | minuta e Anexo Único |
| C7 | `EDITAL  DE CONVOCAÇÃO e REGULAMENTO.pdf` | 3 páginas; SHA-256 `9CCFECFE...AEC8` | datas, objeto e procedimento participativo |
| C8 | `ÍNDICE ANALÍTICO DO PARECER...docx` | SHA-256 `8CF78145...B9` | arquitetura esperada para trabalho futuro |

[FONTE] As cópias com nomes corrompidos por codificação têm o mesmo hash das cópias com nome correto; são duplicatas, não documentos adicionais.

[LACUNA] Continuam ausentes os documentos originários mais importantes: TAACC integral e seus anexos, Resolução 69/2024 integral, Resoluções 21/2019 e 22/2019, convênio/delegação, Processo Administrativo 61/2026 integral, autos e decisões sancionatórias, contrato de concessão e histórico documental das demais frentes. A existência do Anexo Único da minuta não supre essas faltas.

## 3. Achados críticos

### 3.1 P0 — inventário documental materialmente falso

[FONTE] O diagnóstico afirma, nas linhas 5, 55 e 67, que o Anexo Único não foi anexado. O e-mail de resposta repete a afirmação na linha 7. O anexo está no próprio PDF da minuta, páginas 10 a 22.

[FONTE] O relatório também registra “Minuta de Resolução AGERST (8 páginas)”. O arquivo tem 22 páginas. O erro não é meramente numérico: as 12 páginas ignoradas contêm o objeto principal da controvérsia, inclusive as cláusulas 2.2, 12.1.5.1, 17.8 e 21.4.3, tratadas depois como se seus fundamentos não estivessem disponíveis.

[INFERÊNCIA] A matriz de “10 cláusulas-chave”, a afirmação de “49 cláusulas restantes” e a recomendação de aceitar a maior parte das nulidades foram construídas sem análise documentada da matriz integral disponível. Essas conclusões não podem ser reaproveitadas.

### 3.2 P0 — prazo e evento oficial lidos incorretamente

[FONTE] O edital, página 1, fixa a consulta pública entre 06/07 e 04/08/2026 e a audiência para 11/08/2026 às 14h. O regulamento, página 2, confirma data, horário, local e duração de até três horas.

[FONTE] O diagnóstico usa “data a especificar”, “TBD”, “janela crítica até 31 julho” e “votação provável antes do fim de julho”. O e-mail de encaminhamento repete a tendência de votação em julho.

[NÃO VERIFICADO] Não há, no acervo local examinado, data de votação do Conselho Diretor. Logo, não pode ser afirmado que a votação ocorrerá em julho nem imediatamente após a audiência.

[INFERÊNCIA] O calendário correto deve ser reconstruído a partir de dois marcos comprovados: encerramento da consulta em 04/08 e audiência em 11/08. Prazos internos anteriores podem ser recomendados, mas devem ser identificados como gestão interna, não como prazo oficial.

### 3.3 P0 — violação expressa do escopo consultivo

[FONTE] A consulta preparatória, parágrafo 4, diz que esta etapa **não** se destina a parecer conclusivo, plano executivo, minuta de peças, estratégia negocial detalhada ou proposta final de honorários.

[FONTE] As diretrizes, parágrafos 43 e 267, repetem que a entrega não deve formular solução definitiva, plano, cronograma executivo, minutas, honorários ou previsão fechada de êxito.

[FONTE] O diagnóstico, em sentido oposto, entrega modelos de requerimento e comunicação, cronogramas, recomendação fechada de negociação, fases de contratação e valores de R$ 40–60 mil, R$ 200–300 mil e R$ 500–800 mil.

[LACUNA] O comando interno menciona futura proposta de serviços, enquanto os documentos posteriores da própria consulta limitam esta etapa. Esse conflito de escopo deveria ter sido submetido ao responsável; não autorizava escolher silenciosamente o escopo mais amplo.

### 3.4 P0 — percentuais e impactos sem base defensável

[FONTE] A metodologia fornecida, parágrafos 73 a 78, veda percentuais rígidos por falta de respaldo nos padrões contábeis, salvo critério interno fornecido pela CORSAN/AEGEA.

[FONTE] O diagnóstico usa, reiteradamente, 60–70% de perda/implementação, 30–40% de êxito, 50–70% de reversão e base documental de 30–40%. Não identifica amostra, classe de referência, histórico comparável, escala interna da cliente ou regra que transforme cinco vetores qualitativos nesses números.

[FONTE] A conta “quatro de cinco vetores favorecem a AGERST” atribui o mesmo peso a prova, jurisprudência, enquadramento, processo e “coalizão pública”. Isso não é a metodologia do CPC 25, da ISO 31000 ou do COSO ERM descrita no documento recebido.

[FONTE] Os cenários de multas de R$ 20–50 milhões/ano e R$ 123–205 milhões/ano, investimento adicional de R$ 500 milhões–1 bilhão, custo de defesa e economia negocial não apresentam memória de cálculo nem documento financeiro de entrada.

[FONTE] O valor de R$ 4.104.152.317,84 aparece na minuta como preço de aquisição do controle acionário da CORSAN. O diagnóstico o converte em “Concessão CORSAN = R$ 4,1 bilhões” e em exposição econômica deste caso municipal. Essa mudança de categoria não é sustentada pelo documento.

[NÃO VERIFICADO] Provisão bilionária, violação de covenants, reação de mercado, cobertura nacional como “fraude em licitação” e bis in idem de R$ 200–500 milhões não têm suporte nos arquivos locais examinados.

### 3.5 P0 — base normativa atribuída incorretamente

[FONTE] A própria Minuta, página 5, transcreve o art. 53 da Lei 9.784/1999: a Administração deve anular atos ilegais e pode revogá-los por conveniência ou oportunidade, respeitados os direitos adquiridos. O texto não contém a proposição “autotutela não retroage”.

[FONTE] O diagnóstico atribui ao art. 53, em várias passagens, exatamente a frase “autotutela não retroage” e diz que a nulidade posterior viola esse artigo. Trata-se de erro de atribuição normativa.

[NÃO VERIFICADO] O acervo não sustenta a tese de que a anulação exigiria “vício novo” ou que a homologação com ressalvas teria criado automaticamente direito adquirido à manutenção de cláusula ilegal. Segurança jurídica, decadência, efeitos temporais e confiança legítima podem ser eixos defensivos, mas exigem fonte, regime municipal aplicável e exame da Resolução 69/2024 integral.

[FONTE] O diagnóstico afirma que o art. 21 da Lei 11.445/2007 estabelece competência exclusiva sobre tarifas, revisões e reequilíbrio. O trecho reproduzido na minuta usa o art. 21 para independência decisória e autonomia; não comprova essa proposição mais ampla.

[NÃO VERIFICADO] Também falta suporte oficial independente para a extensão atribuída à ADI 2095, para a incidência direta da Lei 9.784/1999 sobre a autarquia municipal e para a proposição de que o art. 27 da Lei 8.987/1995 asseguraria o reequilíbrio nos termos usados no diagnóstico.

### 3.6 P0 — fonte adversa tratada como prova independente

[FONTE] O `sourceLedger` do estado CORSAN está vazio. O diagnóstico contabiliza como “documentos acessados” leis e julgados apenas referenciados no Parecer 0491 e na Minuta.

[FONTE] A Resolução 69/2024, o TAACC, o edital de leilão e o contrato de compra e venda não estão disponíveis em versão originária na pasta examinada. Mesmo assim, afirmações extraídas do Parecer 0491 são classificadas como “fatos comprovados”.

[INFERÊNCIA] O Parecer 0491 e a Minuta comprovam que a AGERST/Procuradoria **afirmaram** determinadas proposições; não comprovam, sozinhos, a correção do conteúdo originário citado por essa parte interessada.

### 3.7 P1 — resposta ao cliente insuficiente e prematuramente conclusiva

[FONTE] O diagnóstico lista 42 quesitos recebidos, declara responder 6 de 9 eixos e depois 8 de 15 perguntas, sem matriz estável entre quesito, documento, conclusão e lacuna.

[LACUNA] Sem TAACC, lei/convênio de delegação, contrato de concessão, Resolução 69, processo administrativo integral, autos e manifestações da CORSAN, não é possível concluir sobre competência desconstitutiva da AGERST, contraditório, bis in idem, tipicidade, conflito de papéis, fundo, MP ou histórico do procurador.

[INFERÊNCIA] A resposta útil nesta etapa seria uma delimitação documentada das questões e das frentes a aprofundar. A recomendação de aceitar a maioria das nulidades e preferir negociação excede o que os documentos permitem afirmar.

### 3.8 P1 — controles de qualidade e relatório não detectaram o problema

[FONTE] O `F7_VERIFICADOR_FORJA.json` classificou o diagnóstico como `peca`, reclamou de endereçamento e assinatura e não detectou o anexo ignorado, os percentuais vedados, o prazo falso ou a atribuição errada do art. 53.

[FONTE] O replay N3 registrou 22 achados visuais em três SVGs CORSAN, incluindo textos fora do quadro, sobreposições e elementos cobrindo texto. Isso conflita com os relatórios visuais que declaravam os SVGs aprovados.

[FONTE] O e-mail de encaminhamento repete os erros de Anexo Único ausente, votação em julho, percentuais, custos e recomendação. Portanto, o erro não ficou restrito ao relatório técnico; contaminou a comunicação de entrega.

## 4. Acertos preserváveis

1. [FONTE] O documento identifica corretamente o gênero como diagnóstico preliminar e anuncia base parcial.
2. [FONTE] Há esforço explícito de separar fatos, alegações e interpretações nas Seções II e III.
3. [FONTE] Foram nominadas lacunas reais e importantes: TAACC/Anexo IV, Resoluções 21/22/69, processo integral, autos, inquéritos, convênio, fundo e comunicações.
4. [FONTE] O diagnóstico reconhece que conflito de interesses, coordenação com MP e atuação institucional não podem ser afirmados sem prova.
5. [INFERÊNCIA] A distinção entre competência regulatória, poder concedente, gestão contratual, sanção e reequilíbrio é um bom eixo de reconstrução, desde que seja aplicada aos documentos originários e não presumida.

## 5. O que pode e o que não pode ser afirmado

### Pode ser afirmado agora

- [FONTE] Existe o Parecer Jurídico 0491/2026, de 17/06/2026, no Processo Administrativo 61/2026, com 114 páginas.
- [FONTE] Existe minuta de resolução ainda não numerada nem datada, com 22 páginas e Anexo Único, que propõe nulidade/ineficácia de várias cláusulas e interpretação restritiva de outras.
- [FONTE] A minuta invoca Lei 11.445/2007, Lei 8.987/1995, Lei municipal 9.316/2023, ADI 2095 e Súmula 473, entre outras autoridades.
- [FONTE] A consulta pública está prevista de 06/07 a 04/08/2026 e a audiência para 11/08/2026 às 14h.
- [FONTE] O acervo originário necessário para conclusão segura está incompleto.

### Não pode ser afirmado na base atual

- [NÃO VERIFICADO] Probabilidade de votação, perda, êxito ou reversão em qualquer percentual.
- [NÃO VERIFICADO] Valor anual de multas, impacto bilionário, provisão contábil, covenant, dano reputacional ou economia de uma estratégia.
- [NÃO VERIFICADO] Votação antes do fim de julho ou qualquer data de deliberação.
- [NÃO VERIFICADO] Existência de coalizão AGERST–MP–Município, perseguição, captura, conflito de interesse ou viés do procurador.
- [NÃO VERIFICADO] Direito adquirido à manutenção do TAACC, impossibilidade de autotutela ou exigência de vício novo.
- [NÃO VERIFICADO] Superioridade da negociação sobre o contencioso e conveniência de aceitar a maior parte das nulidades.
- [NÃO VERIFICADO] Classificação contábil como provável, possível ou remota sem avaliação por frente, prova e obrigação específica.

## 6. Método exigido para a reconstrução posterior

1. [FONTE] Definir o cânone por manifesto e hash.
2. [FONTE] Inventariar todos os arquivos, remover duplicatas lógicas por hash e registrar páginas, origem, autoria e função.
3. [FONTE] Extrair integralmente a Minuta, inclusive o Anexo Único, em matriz cláusula–fundamento–efeito.
4. [LACUNA] Obter os documentos originários citados e comparar, cláusula por cláusula, a transcrição da AGERST com o texto real.
5. [LACUNA] Obter o Processo 61/2026 integral e verificar competência, instauração, manifestação da concessionária, notas técnicas, consulta, audiência e futura decisão.
6. [LACUNA] Verificar cada autoridade em fonte oficial, registrando proposição, trecho, atualidade, contexto e aderência.
7. [INFERÊNCIA] Classificar risco qualitativamente por frente: evento, probabilidade jurídica, impacto, confiança, drivers e sinais de revisão. Percentual só pode reaparecer se a cliente fornecer escala ou base empírica defensável.
8. [FONTE] Responder cada quesito em matriz própria e manter fora desta etapa plano executivo, peças, cronograma detalhado, honorários e previsão fechada de êxito, salvo nova autorização expressa do responsável.
9. [FONTE] Refazer o e-mail de encaminhamento apenas depois da auditoria substantiva e visual.

## 7. Red Team

[INFERÊNCIA] A melhor resposta contrária à CORSAN, com o acervo atual, é que a própria Minuta individualiza dezenas de cláusulas e invoca autonomia regulatória, vedação do art. 11, § 3º, da Lei 11.445/2007 e ressalvas já constantes da Resolução 69/2024. A defesa baseada apenas em “retroatividade”, “direito adquirido” e ausência de “vício novo” é vulnerável porque o diagnóstico atribuiu ao art. 53 uma regra que o texto local não contém e não leu a Resolução 69 originária.

[INFERÊNCIA] A melhor resposta favorável à CORSAN não é a manutenção automática de todas as cláusulas. É exigir competência legal específica, devido processo, motivação individualizada, aderência entre cláusula real e vício apontado, tratamento do equilíbrio econômico-financeiro e distinção entre regulação, sanção e alteração do contrato. Essa defesa depende dos documentos ainda ausentes.

## 8. Conclusão

**Status Cícero:** **BLOQUEADO.**  
**Destino permitido:** uso interno como registro de uma tentativa anterior e como lista inicial de temas.  
**Destino vedado:** cliente, precificação, decisão estratégica, manifestação à AGERST ou base de parecer conclusivo.  
**Condição de liberação:** reconstrução desde o inventário, análise integral do Anexo Único, correção do calendário, retirada das quantificações sem base, verificação das autoridades e resposta rastreável aos quesitos dentro do escopo consultivo.
