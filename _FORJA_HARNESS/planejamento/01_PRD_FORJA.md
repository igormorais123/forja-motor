# PRD — FORJA N2

**Produto:** FORJA, harness de produção assistida e auditável para a Fábrica de Melhoria de Petições Medina Osório  
**Versão:** N2.0  
**Data:** 2026-07-08  
**Status:** vigente para execução  
**Documento-mãe de correção:** `05_FORJA_NIVEL_2_ANALISE_E_PLANO_CORRIGIDO.md`  
**Manifest:** `_FORJA_HARNESS/FORJA_SPEC_MANIFEST.json`  

> Este PRD substitui o PRD v1.1 anterior. Qualquer execução do FORJA deve seguir esta versão N2.

---

## 1. Visão

FORJA N2 organiza a produção jurídica da fábrica em uma esteira auditável: entrada de demanda, reconciliação da fila, leitura de fontes, regimento, planejamento estratégico, redação, auditoria, QA visual, pacote de revisão e fechamento com evidência.

A premissa central mudou: FORJA não é uma máquina de "automação total" que promete entregar peça em qualquer condição. É um harness que acelera o trabalho sem produzir falsa segurança. Quando falta fonte, regimento, anexo, login, evidência de entrega ou validação oficial, o comportamento correto é bloquear, explicar e preservar a trilha.

Regra operacional curta:

**Painel resume; comando orienta; anexo prova.**

---

## 2. Problema

A fábrica tem demandas simultâneas vindas de e-mail, WhatsApp/Hermes, pastas locais e intervenções manuais. O risco não é apenas demora; é perder evidência, confundir status, aceitar jurisprudência não verificada, esquecer placeholder, usar regimento desatualizado, quebrar o padrão Word do escritório ou marcar uma demanda como cumprida sem prova real de entrega.

O PRD anterior acertava na ambição, mas misturava níveis de confiabilidade diferentes:

- painel tratado como se fosse prova;
- Google Calendar tratado como executor técnico;
- WhatsApp tratado como gatilho bruto;
- draft Gmail com destinatário hardcoded;
- probabilidades de êxito não auditáveis;
- fallback visual degradado como se fosse entrega final;
- documentos PRD/TDD/Roadmap/Diagramas em versões contraditórias.

FORJA N2 corrige isso.

---

## 3. Objetivos

1. **Reduzir fila mental e retrabalho** sem aumentar risco jurídico.
2. **Impedir entrega prematura** quando houver pendência de fonte, regimento, anexo, citação, prazo, visual ou evidência.
3. **Separar gestão de prova:** `demandas.json` organiza; anexos, autos, PDFs, DOCX, e-mails e fontes oficiais provam.
4. **Padronizar o ciclo F0-F10** com estado persistente, gates e artefatos verificáveis.
5. **Transformar comunicações em comando operacional:** e-mail, WhatsApp, Hermes e intervenção manual entram como pasta, comando, anexos, origem e evidência verificável.
6. **Garantir conformidade do tribunal:** regimento integral e emendas vigentes antes de redigir.
7. **Garantir padrão Medina Osório:** template ou peça anterior, Word COM, QA visual página a página.
8. **Fechar demanda somente com evidência:** e-mail enviado, WhatsApp entregue, protocolo, anexo arquivado ou intervenção manual documentada.

---

## 4. Não objetivos

- Enviar e-mail automaticamente.
- Protocolar judicialmente.
- Assinar digitalmente.
- Marcar demanda como `cumprida` com base apenas no painel.
- Transcrever áudio de WhatsApp sem permissão explícita.
- Expor conversa bruta de WhatsApp no painel, chat ou relatório público.
- Usar probabilidade numérica de vitória como métrica de qualidade.
- Citar jurisprudência final sem fonte oficial ou arquivo oficial arquivado.
- Criar documento protocolável fora do template ou de peça anterior do caso.
- Tratar fallback degradado como entrega final sem autorização humana explícita.

---

## 5. Personas

### Igor

Porteiro final e operador da fila. Precisa enxergar estado, bloqueios, próxima ação, urgência, anexos pendentes e evidência de entrega sem decidir detalhes técnicos de implementação.

### Fábio Medina Osório

Revisor jurídico e destinatário estratégico. Precisa de pacote claro, peça forte, relatório objetivo, caminhos de evidência e pendências que possam ser decididas rapidamente.

### Agentes IA

Executam leitura, triagem, pesquisa, blueprint, redação, auditoria e QA dentro de contratos explícitos. Não podem inventar fonte, ocultar pendência ou transformar divergência em consenso falso.

### FORJA

Orquestrador de fases, estado, artefatos, gates e evidências. Não é fonte jurídica; é controle de processo.

---

## 6. Fonte de verdade

| Informação | Fonte de verdade |
|---|---|
| Estado da fila | `gestao_escritorio/data/demandas.json` + `intervencoes_manuais.json` |
| Comando da demanda | `COMANDO_DO_EMAIL.md`, `COMANDO_DO_WHATSAPP.md` ou `COMANDO_MANUAL.md` |
| Fato jurídico | anexo, autos, PDF, DOCX, e-mail arquivado ou fonte oficial |
| Tribunal e regimento | CNJ, endereçamento, decisão, classe e `REGIMENTO_INTERNO_<TRIBUNAL>.md` |
| Citação jurisprudencial | portal oficial ou arquivo oficial arquivado |
| Entrega | prova de envio/protocolo/WhatsApp/anexo ou intervenção manual documentada |
| Custo | log real por fase |

---

## 7. Escopo funcional

### RF-01 — Reconciliação da fila

FORJA deve ler painel, comandos, pastas, status de integrações e evidências antes de criar ou alterar estado. Gmail/Hermes podem estar `ok`, `degraded`, `needs_login` ou `offline`.

### RF-02 — Ingestão segura

FORJA deve criar ou reconciliar demanda sem sobrescrever pasta existente, sem apagar duplicidade e sem assumir que anexos estão completos. Anexo faltante vira pendência.

### RF-03 — Classificação do produto

FORJA deve classificar a demanda como petição, memorial, embargos, parecer, laudo, proposta ou administrativo antes de aplicar molde de peça.

### RF-04 — Classificação operacional

FORJA deve classificar a demanda por tipo de produto, tribunal provável, prazo, urgência, pasta, anexos esperados, destinatário de revisão e evidência mínima para avançar. O bloqueio nasce de lacuna operacional concreta, não de rótulo genérico.

Como subfase obrigatória da F2 em todo caso novo, a FORJA deve executar a exploração `FORJA-F2A-100-v1`: exatamente 100 perguntas adaptadas ao caso, 10 óticas × 10, respostas com natureza epistemológica e lastro quando factual, ao menos duas hipóteses de solução e handoff explícito para F3–F7. Pergunta material sem resposta verificável permanece bloqueada e impede redação externa; não pode ser completada por memória.

### RF-05 — Regimento e leis gerais

Antes de redigir, FORJA deve identificar tribunal, ler o regimento integral da pasta, conferir metadados e emendas posteriores, e consultar `_LEIS_GERAIS`.

### RF-06 — Ledger de fontes

FORJA deve classificar afirmações críticas como:

- `[FONTE: arquivo]`
- `[FONTE: oficial]`
- `[DECLARAÇÃO DO ESCRITÓRIO/CLIENTE]`
- `[INFERÊNCIA]`
- `[HIPÓTESE ESTRATÉGICA]`
- `[NÃO VERIFICADO]`

### RF-07 — Blueprint estratégico

FORJA deve gerar blueprint com teses, riscos, lacunas, ordem argumentativa e divergências reais do conselho. Decisão acatada ou rejeitada precisa de motivo.

### RF-08 — Pesquisa oficial

FORJA pode usar buscadores e IA como descoberta, mas citação final só passa com fonte oficial ou arquivo oficial arquivado.

### RF-09 — Redação em template

Peça protocolável deve partir de `TEMPLATE_MEDINA_OSORIO_PETICAO.docx` ou cópia de peça anterior do caso. Documento vazio criado por código é proibido para entrega final.

### RF-10 — Auditoria

FORJA deve verificar fatos, citações, prazos, placeholders, anexos mencionados, regimento, leis gerais, metadados sensíveis e coerência jurídica.

### RF-11 — QA visual

FORJA deve gerar PDF via Word COM quando for Word, renderizar todas as páginas e inspecionar timbre, fólio, rodapé, margens, fontes, diagramas e sobreposição.

### RF-12 — Pacote de revisão

FORJA deve produzir DOCX, PDF, relatório, checklist de fontes/pendências e preview visual. Draft Gmail é opcional e exige `approvedRecipients`.

### RF-13 — Fechamento com evidência

FORJA só pode marcar `cumprida` quando houver evidência real de entrega ou intervenção manual documentada.

---

## 8. Fases do produto

| Fase | Nome | Resultado esperado |
|---|---|---|
| F0 | Reconciliação da fila | estado real, integrações classificadas, pendências visíveis |
| F1 | Ingestão segura | pasta, comando, anexos, demanda e hashes/lista de anexos |
| F2 | Classificação produto/risco + F2-A exploratória | classificação + `F2_QUESTION_TREE.json` com 100 perguntas, respostas, diagnóstico, soluções e handoff |
| F3 | Fontes/regimento/leis | `F3_MAPA_FONTES_E_REGIMENTO.md` e ledger inicial |
| F4 | Blueprint estratégico | `F4_BLUEPRINT_ESTRATEGICO.md` com divergências registradas |
| F5 | Pesquisa oficial | `F5_JURISPRUDENCIA_VERIFICADA.md` e citações removidas |
| F6 | Redação em template | minuta DOCX baseada no padrão Medina Osório |
| F7 | Auditoria jurídica/factual + F7-B editorial | `F7_RELATORIO_AUDITORIA.md`, checklist de pendências, `audited_markdown`, `final_markdown` e evidências editoriais |
| F8 | QA visual | PDF final renderizado e inspecionado em 100% das páginas |
| F9 | Pacote de revisão | pacote para Igor/Fábio; draft opcional autorizado |
| F10 | Entrega/evidência/aprendizado | demanda cumprida somente com prova e aprendizado registrado |

---

## 9. Estados

Estados de alto nível:

- `nova`
- `em_reconciliacao`
- `em_fontes`
- `em_planejamento`
- `em_pesquisa`
- `em_redacao`
- `em_auditoria`
- `em_qa_visual`
- `pronta_para_revisao`
- `aguardando_evidencia_entrega`
- `cumprida`
- `blocked`
- `degraded`
- `cancelada`

Regra: `pronta_para_revisao` não é `cumprida`.

---

## 10. Gates humanos

| Gate | Quando dispara | Quem decide | Regra |
|---|---|---|---|
| G1 | origem/pasta/comando incompleto | Igor | corrigir entrada ou cancelar |
| G2 | regimento/fonte P0 ausente | Igor/agente técnico | obter fonte ou bloquear |
| G3 | divergência estratégica grave | Igor/Fábio | escolher tese ou pedir novo blueprint |
| G4 | citação/fato crítico não confirmado | Igor/Fábio | remover, confirmar ou bloquear |
| G5 | fallback visual degradado | Igor | autorizar degradação ou exigir correção |
| G6 | draft Gmail | Igor | autorizar destinatários e anexos |
| G7 | marcação `cumprida` | Igor/sistema com evidência | só com prova arquivada |

---

## 11. Requisitos não funcionais

### Segurança

- Nunca enviar e-mail.
- Nunca protocolar.
- Nunca tratar anotação solta como prova de entrega.
- Nunca avançar demanda sem comando, pasta e anexos esperados registrados.

### Confiabilidade

- Toda fase grava estado e artefatos.
- Falha técnica vira `blocked` ou `degraded`, não `ok`.
- Retentativas automáticas têm limite e log.

### Auditabilidade

- Cada artefato final deve indicar fontes, pendências, decisões e evidência de QA.
- Custos reais devem ser registrados por fase quando houver custo de modelo/API.

### Organização operacional

- Painel remoto, quando existir, mostra campos úteis de execução: caso, fase, P0/P1/P2, próximo passo, evidência e caminhos de artefatos.
- WhatsApp, e-mail, Hermes e intervenção manual entram como comando, anexos, origem e evidência arquivada.

### Visual

- Usar identidade Medina Osório.
- Diagramas só entram se reduzirem esforço cognitivo.
- Texto de diagrama nunca abaixo de 8 pt no tamanho final impresso.

---

## 12. Critérios de aceite

1. Nenhuma fase final aceita `[NÃO VERIFICADO]`, `[VERIFICAR]`, `[NOME]`, `[DATA]`, `[CRC-UF]` ou placeholder equivalente.
2. Nenhuma citação final entra sem fonte oficial ou arquivo oficial arquivado.
3. Nenhum regimento é aceito sem fonte, versão, data de download e seção de emendas posteriores.
4. Nenhum DOCX protocolável nasce fora do template ou peça anterior.
5. Nenhum PDF final é aprovado sem render e inspeção de todas as páginas.
6. Nenhuma demanda vira `cumprida` sem evidência de entrega.
7. Nenhuma entrada de WhatsApp, e-mail ou Hermes vira tarefa acionável sem comando, pasta e anexos esperados registrados.
8. Nenhum custo pago novo é assumido sem limite e registro.
9. Nenhum fallback degradado vira entrega final sem autorização explícita.
10. Nenhum agente pode alterar o escopo sem atualizar o manifest.
11. Nenhuma tentativa F7 nova segue para F8 sem o F7-B aprovado e sem `final_markdown` vinculado por hash ao `audited_markdown`.

---

## 13. Métricas

### Qualidade

- citações removidas por falta de fonte oficial;
- fatos reclassificados de fato documental para declaração/inferência;
- pendências P0 detectadas antes do draft;
- placeholders encontrados antes do PDF final;
- páginas com defeito visual detectadas no render.

### Operação

- tempo até `pronta_para_revisao`;
- tempo bloqueado por fonte, anexo, login, regimento ou QA;
- demandas abertas, vencidas, <=48h, sem resposta com peça, pendência de anexos;
- demandas não marcadas como cumpridas por falta de evidência.

### Custo

- custo real por fase;
- retries por fase;
- diferença entre estimativa e custo real;
- casos bloqueados por orçamento.

---

## 14. Dependências locais verificadas

Checagem local em 2026-07-08:

| Ferramenta | Estado |
|---|---|
| Inkscape | presente em `C:\Program Files\Inkscape\bin\inkscape.exe` |
| Graphviz | presente em `C:\Program Files\Graphviz\bin\dot.exe` |
| Tectonic | presente em `C:\Users\IgorPC\.local\tectonic\tectonic.exe` |
| Mermaid CLI | presente no npm global |
| ImageMagick | não localizado no `PATH` nesta checagem |

---

## 15. Regra de execução

Antes de executar qualquer implementação, agente ou automação deve abrir:

1. `_FORJA_HARNESS/FORJA_SPEC_MANIFEST.json`
2. este PRD;
3. `02_TDD_FORJA.md`;
4. `03_ROADMAP_FORJA.md`;
5. `04_DIAGRAMAS_FORJA.md`;
6. `05_FORJA_NIVEL_2_ANALISE_E_PLANO_CORRIGIDO.md`, se precisar entender por que a versão antiga foi corrigida.

Se houver conflito, vence o manifest e a regra mais restritiva de segurança/evidência.

---

## 16. Dimensão obrigatória para peças de resposta — A1

Toda contrarrazão, contraminuta, contestação, réplica, impugnação, resposta ou manifestação que confronte peça adversária deve executar a auditoria descrita em `09_AUDITORIA_ADVERSARIAL_PONTOS_DECISIVOS.md`.

O produto deve: conferir todas as autoridades adversárias em fonte oficial; procurar citações falsas ou descontextualizadas, contradições, alterações factuais e pontos decisivos; separar erro, divergência interpretativa e indício sancionável; registrar a providência correspondente; e submeter linguagem acusatória a Cícero/revisor humano. A pesquisa sem resultado será tratada como “não localizada após diligência”, nunca como prova automática de inexistência.

São saídas obrigatórias `adversarial_audit` em F3, `adversarial_strategy` em F4 e `adversarial_recheck` em F7. A peça não avança quando um desses registros aplicáveis estiver pendente ou desvinculado da versão auditada.

---

## 17. Adendo vigente — F7-B revisão editorial e escrita final (15/07/2026)

Este adendo é posterior à redação histórica N2.0 e incorpora a decisão implementada sem renumerar as fases F0–F10: após a auditoria F7 alcançar **zero P0**, e antes de qualquer composição F8, o texto auditado passa por `F7-B_REVISAO_EDITORIAL_ESCRITA_FINAL`.

Requisitos de produto:

1. `forja_fable5.py` aciona explicitamente o Claude Code com o modelo canônico `claude-fable-5`, usando a assinatura OAuth Claude Max do Igor e sem API key ou cobrança de API;
2. o acionamento é controlado e separado: `forja_run.py` não chama Fable 5 automaticamente; o operador executa o F7-B dentro da tentativa F7 já criada;
3. `FABLE5_RESULT.json` é um fragmento de resultado, não substitui `PHASE_RESULT.json`; seus gates e artefatos devem ser incorporados ao resultado da fase antes da promoção;
4. `final_markdown` passa a ser o cânone textual de F8 e dos pacotes novos; `audited_markdown` permanece imutável como origem auditada e trilha de comparação;
5. o modelo só pode melhorar clareza, ritmo, precisão vocabular, encadeamento e concisão. É proibido criar, remover ou alterar fatos, datas, números, valores, citações, dispositivos, precedentes, marcadores processuais, ressalvas, capítulos, pedidos, fecho e assinaturas;
6. hashes e invariantes são recompostos por `forja_editorial_fidelity.py`. Declaração do próprio modelo não comprova fidelidade;
7. o executor admite no máximo três candidatas internas no total — a inicial e até dois retries —, sempre a partir do `audited_markdown` original. Esse limite é distinto das quatro tentativas máximas da fase F7 previstas no contrato;
8. falha de autenticação, modelo não comprovado, divergência de hash ou qualquer gate editorial bloqueado impede F8, sem promover o arquivo candidato.

Os artefatos mínimos são `final_markdown.md`, `editorial_report.json`, `editorial_diff.patch`, `fable5_usage.json`, `editorial_fidelity.json` e `FABLE5_RESULT.json`. Havendo mais de um texto na mesma tentativa, os seis artefatos usam o mesmo sufixo seguro para manter o pareamento inequívoco.
