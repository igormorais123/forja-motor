# AUDITORIA COMPLETA DA FORJA — REVISÃO 5.6

**Data da auditoria:** 09/07/2026  
**Objeto:** planejamento, execução real, estados, peças produzidas, controle de contexto, diagramação, gates de qualidade, entrega e integração com a gestão do escritório.  
**Escopo da intervenção:** auditoria e planejamento. Nenhuma peça, estado, script operacional ou documento N2 foi alterado.

---

## 1. Veredito executivo

A FORJA já possui uma base acima da média: separação em fases F0–F10, fontes oficiais, conselho Helena/Cícero, red team, verificador determinístico, geração Word/PDF, visual law e rastros de entrega. O problema atual não é ausência de capacidade. É a falta de um **fechamento único e verificável do ciclo**.

Hoje, cinco versões da verdade podem divergir:

1. o `FORJA_STATE.json`;
2. o resultado do verificador F7;
3. o relatório de QA visual;
4. o rascunho/entrega no Gmail;
5. o painel `gestao_escritorio`.

Isso já aconteceu em casos reais. Foram encontrados rascunho montado com citação marcada como não verificada, fase que voltou de F9 para F5, painel afirmando que todas as fontes estavam conferidas quando o estado dizia o contrário, relatórios aprovando peças com diagramas sobrepostos e painel sem o bloco `forja` previsto no TDD.

**Conclusão:** a FORJA N2 produz trabalho juridicamente rico, mas ainda não garante que o que foi produzido, verificado, diagramado, anexado e exibido no painel seja exatamente o mesmo conjunto de artefatos e o mesmo estado. A próxima versão deve priorizar **integridade operacional, continuidade de contexto, QA visual real e sincronização automática**, sem reescrever os componentes que já funcionam.

---

## 2. Como a auditoria foi feita

### 2.1 Documentos e implementação

Foram lidos integralmente os sete documentos canônicos de planejamento:

- `planejamento/01_PRD_FORJA.md`;
- `planejamento/02_TDD_FORJA.md`;
- `planejamento/03_ROADMAP_FORJA.md`;
- `planejamento/04_DIAGRAMAS_FORJA.md`;
- `planejamento/05_FORJA_NIVEL_2_ANALISE_E_PLANO_CORRIGIDO.md`;
- `planejamento/06_GATES_QUALIDADE_FORJA.md`;
- `planejamento/07_PLANO_UPGRADE_ESTADO_DA_ARTE_2026.md`.

Também foram confrontados o manifesto, a documentação técnica, as retrospectivas, os módulos de execução, o pipeline visual, o servidor da gestão e os dados reais do painel.

### 2.2 Universo inspecionado

Inventário atual da `_FORJA_HARNESS` no momento da auditoria:

| Item | Quantidade |
|---|---:|
| Estados de casos | 21 |
| Markdown | 143 |
| JSON | 48 |
| Módulos Python | 41 |
| PDF | 22 |
| DOCX | 20 |
| SVG | 14 |
| EMF | 14 |
| PNG | 345 |

Os 48 JSON foram submetidos a leitura estrutural; um é inválido. Os 14 SVG foram examinados quanto à estrutura e atributos. Foram localizados 17 PDFs dentro dos estados dos casos.

### 2.3 Revisão visual

Foi feita triagem visual de **120 páginas** por contact sheets:

- 84 páginas das cinco edições visual law finais: Azimut, CORSAN, Libra Sul, Natura e Patrícia/Fábio;
- 36 páginas dos cinco produtos mais recentes do caso Plano de Saúde.

As páginas com indício de defeito foram abertas e examinadas em resolução integral. Portanto, esta auditoria não confunde “página renderizada” com “página aprovada”.

### 2.4 Testes executados

| Teste | Resultado |
|---|---|
| `test_forja_verificador.py` | passou: 10 detecções + 8 não-travas |
| `test_forja_citacoes.py` | passou: 6 detecções + 6 não-travas |
| `test_forja_injection.py` | passou nos 15 PDFs reais e no PDF sintético |
| `test_f7_campos.py` | passou |
| `test_licao41.py` | passou |
| `validate_f7_integration.py` | **falhou** por caminho relativo incorreto |

Falha concreta do teste de integração: ele procura `state/case-...` a partir da raiz do workspace, mas o caso está em `_FORJA_HARNESS/state/case-...`.

---

## 3. Acertos que devem ser preservados

### A1. Decomposição F0–F10

O processo já separa ingestão, classificação, leitura, estratégia, pesquisa, redação, auditoria, QA visual, pacote de revisão e evidência. Essa decomposição é correta e deve continuar sendo o esqueleto da FORJA.

### A2. Separação entre organização e prova

O planejamento distingue corretamente painel/comando de anexos e fontes oficiais. O painel organiza o trabalho; não prova fato jurídico. Essa regra é essencial.

### A3. Verificação determinística

O verificador detecta placeholders, marcadores de conferência, problemas de citações e outros bloqueadores com testes de regressão. A correção anterior que fez F10 consumir `F7_VERIFICADOR_FORJA.json` e exigir `p0 == 0` foi um avanço real e está implementada em `forja_delivery.py:120-136`.

### A4. Fontes oficiais e ledger

Há cache de fontes, classificação de uso final e registro `finalUseAllowed`. Isso permite construir um gate forte sem inventar um sistema novo.

### A5. Helena, Cícero e red team

Os casos novos já registram pareceres de Helena e Cícero e um red team escrito. O caso Plano de Saúde demonstra a utilização de quatro leitores, quatro pesquisadores e conselho obrigatório em `FORJA_STATE.json:32-35`.

### A6. Pipeline Word/PDF e padrão visual

O uso do template do escritório, Word COM, conversão SVG→EMF e renderização de páginas é tecnicamente adequado. O defeito está no gate de aprovação, não na escolha da base.

### A7. Preservação do conteúdo no visual law

`forja_visual.py` passou a reconstruir a peça a partir do Markdown de origem e adicionou conferência de cobertura. Isso corrigiu um problema anterior de reescritas visuais que omitiam grandes blocos de conteúdo. A direção é correta, embora a conferência ainda seja parcial.

### A8. Entrega conservadora

Os rascunhos do Gmail não são enviados automaticamente. A decisão final continua humana, o que é adequado ao fluxo do escritório.

---

## 4. Falhas críticas confirmadas

## F1. O painel previsto no TDD não foi integrado à FORJA

**Severidade:** crítica para controle operacional.

O TDD prevê um bloco `forja` em cada demanda (`02_TDD_FORJA.md:142-166`) e endpoints próprios (`02_TDD_FORJA.md:300-309`). Na base real:

- demandas existentes: **20**;
- demandas com bloco `forja`: **0**;
- endpoints `/api/forja/*` implementados no servidor: **0**.

A documentação operacional manda publicar comentários manualmente em `/api/comment` (`DOCUMENTACAO_TECNICA.md:194-200`). Isso não é integração; é uma convenção dependente de execução manual.

**Consequência observada:** o caso Plano de Saúde já tem 10 anexos em rascunho, mas `proximaAcao` ainda diz “Conferir anexos, confirmar prazo e transformar o pedido em peça/documento”. O painel exibe parte do avanço em comentários, mas não deriva o estado real do ciclo.

**Causa-raiz:** o estado da FORJA e a demanda do painel não compartilham um manifesto de caso nem um sincronizador transacional.

## F2. A máquina de estados permite regressão e contradição

**Severidade:** crítica.

No caso `case-email-auto-19f3f25cb64df962`:

- F9 foi registrado como concluído às 20:25 (`FORJA_STATE.json:66-69`);
- uma atualização posterior de pesquisa às 20:52 gravou F5 novamente (`FORJA_STATE.json:71-74`);
- `currentPhase` passou a ser `F5_PESQUISA_OFICIAL` (`FORJA_STATE.json:6`);
- o status continuou `draft_awaiting_review` (`FORJA_STATE.json:7`).

Não existe guarda de transição, tentativa identificada, reabertura formal de gate ou cálculo derivado da fase atual. Qualquer etapa pode sobrescrever `currentPhase`.

**Risco:** o painel e os agentes não sabem se o caso está em pesquisa, pronto para revisão ou reaberto por pendência.

## F3. F9 foi alcançado com fonte explicitamente não verificada

**Severidade:** crítica para a confiabilidade jurídica.

No mesmo caso:

- `Tema 1.365` está classificado como `NAO_VERIFICADO` e `finalUseAllowed: false` (`FORJA_STATE.json:140-146`);
- o F7 agregado registra `citacoesNaoConferidas: ["TEMA 1365"]` (`producao/F7_VERIFICADOR_FORJA.json:8-12`);
- o estudo utiliza o Tema 1.365 como fundamento material;
- mesmo assim, F9 criou rascunho Gmail com 10 anexos (`FORJA_STATE.json:66-69`, `149-154`).

O painel ainda publicou “Toda citação normativa conferida verbatim em fonte oficial”. Essa frase é incompatível com o próprio ledger.

**Causa-raiz:** o gate atual bloqueia P0, mas não exige que todo artefato classificável como peça final tenha `citacoesNaoConferidas == []` e nenhum item `finalUseAllowed == false`.

## F4. O QA visual aprova páginas materialmente defeituosas

**Severidade:** crítica para entrega profissional.

Erros confirmados em resolução integral:

| Caso/página | Falha material |
|---|---|
| Natura, p. 10 | degrau 5 cobre o conteúdo do degrau 4; legenda duplicada “FIGURA 1 | FIGURA 2” |
| Libra Sul, p. 9 | caixa “NÃO CONHECIMENTO” cobre textos dos dois quadros inferiores |
| Patrícia/Fábio, p. 6 | valores, percentuais, rótulos e total se sobrepõem; total fica oculto |
| CORSAN, p. 3 | texto das duas colunas ultrapassa os cartões e se mistura |
| CORSAN, p. 15 | rótulos “MÉDIA/ALTA” colidem com os textos e com a linha temporal |
| Libra Sul, p. 12 | `####` aparece literalmente em três subtítulos |
| Natura, p. 11 | numeração de legenda “FIGURA 2 | FIGURA 1” |

Arquivos de prova:

- `state/case-email-natura-cabreuva-19f3991ebc75fe03/producao/_visual/qa/p10.png`;
- `state/case-email-libra-sul-agint-stj-19f3c9350d875062/producao/_visual/qa/p09.png`;
- `state/case-email-patricia-fabio-memoriais-19f3c68ee6d8fef2/producao/_visual/qa/p06.png`;
- `state/case-email-corsan-agerst-19f3dc9ff92081cd/producao/_visual/qa/p03.png`;
- `state/case-email-corsan-agerst-19f3dc9ff92081cd/producao/_visual/qa/p15.png`.

O gate atual em `medina_svg_kit.py:68-104` verifica tamanho de fonte e texto fora do `viewBox`. Ele não verifica colisão entre texto e caixas, sobreposição de formas, conteúdo dentro do próprio cartão, conectores atravessando rótulos, legenda duplicada ou atributos inválidos.

`montar_visual.py:57-59` renderiza páginas e retorna sua lista, mas não registra inspeção nem veredito. Renderizar não equivale a revisar.

## F5. O parser visual deixa gramática Markdown vazar para o PDF

**Severidade:** alta.

`forja_visual.py:177` reconhece apenas títulos `#`, `##` e `###`. Os títulos `####` do memorial Libra Sul, existentes desde `MEMORIAIS_LIBRA_SUL_AGINT_ARESP_2578181.md:52`, foram tratados como texto comum e apareceram literalmente no PDF. O marcador `>` de blockquote também vazou.

O verificador F7 marcou a peça sem P0/P1, pois não há gate para “gramática de origem visível no documento final”.

## F6. O relatório de QA se autoaprova sem prova de inspeção integral

**Severidade:** alta.

Há relatórios que declaram qualidade final apesar de terem examinado só páginas iniciais ou “páginas críticas”. No caso Plano de Saúde, F8 afirma: “36 páginas renderizadas; contact sheets + páginas críticas inspecionadas” (`FORJA_STATE.json:60-63`). O gate formal exige inspeção de todas as páginas.

O problema não é ter contact sheet. É não existir um registro página a página com:

- hash da imagem examinada;
- resultado `aprovada/reprovada`;
- achado;
- correção;
- revalidação após nova geração.

Sem isso, o próprio gerador declara que seu resultado está correto.

## F7. Não existe um fechamento canônico único F7→F8→F9→F10

**Severidade:** crítica.

`forja_delivery.py` melhorou ao consumir F7, mas continua específico do piloto:

- texto fixo “7/7 confirmadas” (`forja_delivery.py:92-95`);
- texto fixo “14 páginas” (`forja_delivery.py:97-98`);
- busca o primeiro DOCX/relatório por ordem alfabética (`forja_delivery.py:36-40`);
- considera qualquer texto de `evidenciaResposta` como evidência (`forja_delivery.py:116-118`);
- grava F10 mesmo quando reprovado (`forja_delivery.py:180-186`).

O caso Plano de Saúde chegou a F9 e gerou rascunho sem passar pelo fechamento F10. Logo, F10 não é a única porta de saída.

**Consequência:** o artefato verificado pode não ser o mesmo anexado ao e-mail; o arquivo escolhido pode ser antigo; o painel pode ser atualizado por comentário sem pacote canônico.

## F8. Perda de continuidade de contexto continua possível

**Severidade:** alta.

As retrospectivas mostram ocorrências de:

- `Prompt is too long` na leitura de PDF grande;
- auditor de citações excedendo contexto;
- execuções de subagentes com aproximadamente 746 mil, 916 mil e 1,5 milhão de tokens;
- versões visuais anteriores omitindo 80%–95% dos parágrafos;
- relatório Azimut contaminado por referência a “LIBRA SUL”.

O relatório Azimut ainda contém “nenhum débito LIBRA SUL” em `RELATORIO_FINAL_VISUAL_LAW.json:61-63`, embora a peça principal seja de outro caso.

O plano `07_PLANO_UPGRADE_ESTADO_DA_ARTE_2026.md` confia excessivamente em contexto longo e rejeita qualquer recuperação estruturada. O erro de premissa é tratar **capacidade de contexto** como garantia de **atenção, isolamento e cobertura**.

Não é necessário implantar RAG pesado. É necessário estruturar o que entra em cada fase: índice documental, fatos com origem, cronologia, teses aprovadas, pendências e referências por página.

## F9. O pacote real não possui manifesto de artefatos e hashes

**Severidade:** alta.

No caso Plano de Saúde:

- há cinco produtos em MD/DOCX/PDF;
- `artifacts` não lista todos os DOCX/PDF nem o texto do e-mail;
- `EMAIL_RESPOSTA.txt` não existe;
- `costLog` está vazio apesar do fluxo multiagente (`FORJA_STATE.json:163`);
- não há arquivo que diga quais dez anexos foram efetivamente ligados ao draft;
- não há hashes conectando MD, DOCX, PDF, F7, QA e rascunho.

Sem manifesto, não é possível provar que o PDF inspecionado é o mesmo PDF anexado.

## F10. Estado de integrações é copiado e fica falso

**Severidade:** alta.

O estado do caso registra `whatsapp: ok` (`FORJA_STATE.json:156-161`). No mesmo dia, `gestao_escritorio/data/status_integracoes.json` registra WhatsApp em erro. O estado estático do caso não deve fingir ser monitor em tempo real.

Integrações voláteis precisam de `checkedAt`, origem e validade. O caso deve apontar para a última leitura, não copiar um “ok” eterno.

## F11. JSON inválido e atributos SVG inválidos não são barrados

**Severidade:** média/alta.

Um dos 48 JSON é inválido:

`state/case-email-patricia-fabio-memoriais-19f3c68ee6d8fef2/producao/_visual/RELATORIO_VISUAL_LAW.json`

Erro: escape `\U` inválido no campo `pasta`, linha 2.

Também foram encontrados atributos SVG semanticamente inválidos:

- Azimut: `text-anchor="italic"` e `font-weight="middle"` em `fig2_selic_vs_juros.svg:19-21`;
- Natura: `font-weight="italic"` em `fig2_escada_estrategias.svg:37`;
- Patrícia/Fábio: múltiplos `font-weight="middle"` em `fig2_metodo_bifasico.svg:8-25`.

O SVG ainda pode renderizar por tolerância do navegador/Word, mas o gate deve rejeitar enumerações inválidas.

## F12. Os testes cobrem detectores isolados, não o ciclo real

**Severidade:** alta.

Os testes atuais são úteis, porém não existem testes para:

- transições de fase e regressão F9→F5;
- impedimento de F9 com `finalUseAllowed=false`;
- identidade por hash entre arquivo auditado e arquivo anexado;
- sincronização estado→painel;
- colisões visuais conhecidas;
- vazamento de `####` e `>`;
- numeração de figuras;
- invalidação do QA após regeneração;
- contaminação entre casos;
- validade de todos os JSON.

Além disso, `validate_f7_integration.py` falha no ambiente real por resolver o caminho a partir da pasta errada.

---

## 5. Problemas de gestão confirmados

### 5.1 `ABRIR_GESTAO_ESCRITORIO.html` funciona apenas como lançador

O arquivo abre a versão viva em `127.0.0.1:8765`, uma cópia salva ou a versão móvel. Ele não é responsável pela sincronização e não deve receber lógica de negócio da FORJA.

### 5.2 O servidor não conhece casos FORJA

O servidor expõe `/api/comment`, `/api/item-status` e `/api/manual-task` (`server.py:409-413`), mas não possui as rotas FORJA previstas no TDD.

### 5.3 “Cumprida” ainda aceita evidência fraca

`server.py:459-500` exige nota, tipo e oito caracteres, o que é melhor que conclusão sem justificativa. Porém `evidenceType=manual` mais texto livre ainda passa sem validar mensagem, protocolo, arquivo, hash ou identificador externo.

### 5.4 A base e os overrides são misturados

`apply_manual_updates.py` reaplica intervenções sobre `demandas.json`. Isso facilita a interface, mas dificulta saber o que veio da coleta, do operador e da FORJA. A próxima versão deve manter a origem de cada campo e produzir uma visão derivada.

---

## 6. Causas-raiz

As falhas não são do mesmo tipo, mas convergem em seis causas:

1. **Sem manifesto canônico por caso:** arquivos existem, mas não formam um pacote verificável.
2. **Estado gravado por atribuição direta:** cada fase pode sobrescrever a anterior.
3. **Gates independentes:** F7, F8, F9 e painel não validam o mesmo conjunto de hashes.
4. **QA visual baseado em existência:** contar páginas e gerar imagem é tratado como aprovação.
5. **Contexto monolítico:** agentes recebem material demais sem um caderno estruturado de fatos e fontes.
6. **Integração manual por comentários:** o painel não deriva o estágio real da FORJA.

---

## 7. O que não deve ser feito

Para não quebrar o que funciona:

- não reescrever F0–F10;
- não migrar em massa os 21 estados antigos;
- não substituir Word COM, template, EMF ou o padrão visual aprovado;
- não eliminar Helena, Cícero, red team ou verificadores atuais;
- não adotar banco, fila distribuída ou RAG pesado sem necessidade;
- não alterar `ABRIR_GESTAO_ESCRITORIO.html` para conter regras da FORJA;
- não corrigir retrospectivamente peças sem uma ordem de prioridade e sem preservar o original;
- não marcar casos antigos como aprovados apenas porque um novo gate não existia à época.

---

## 8. Prioridade recomendada

| Ordem | Correção | Motivo |
|---:|---|---|
| 1 | manifesto canônico + guarda de transição | impede divergência básica do ciclo |
| 2 | gate jurídico antes de F9 | impede pacote com fonte não autorizada |
| 3 | QA visual V2 com regressões reais | elimina sobreposição e Markdown vazado |
| 4 | sincronizador FORJA→gestão | mantém painel verdadeiro sem comentário manual |
| 5 | cadernos de evidência por fase | reduz perda de contexto e contaminação |
| 6 | fechamento único F7→F10 | garante identidade entre auditado e anexado |
| 7 | replay dos casos anteriores | prova compatibilidade e mede melhoria |

---

## 9. Resultado da auditoria

**Classificação atual:** funcional e potente, porém ainda **não íntegra de ponta a ponta**.

A FORJA não precisa de uma reconstrução. Precisa de uma camada incremental que faça quatro coisas com rigor:

1. impedir estados impossíveis;
2. vincular todas as aprovações ao mesmo arquivo por hash;
3. reprovar visualmente os defeitos que já escaparam;
4. atualizar automaticamente a gestão após cada mudança relevante.

Essa camada é especificada no documento `planejamento/08_PLANO_FORJA_N3_INTEGRIDADE_VISUAL_E_GESTAO.md`.
