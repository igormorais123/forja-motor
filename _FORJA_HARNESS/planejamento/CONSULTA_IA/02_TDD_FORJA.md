# Consulta IA — TDD — FORJA N2

> Cópia de consulta derivada. O documento canônico permanece no caminho de origem indicado abaixo.

## Metadados e rastreabilidade

- **Documento de origem:** `02_TDD_FORJA.md`
- **Tipo:** TDD
- **SHA-256 da origem:** `ca0f8cd28bdae0589eb47da2f46dabd1ed4110c26216dd2baf99b394875e7d9a`
- **Linhas da origem:** 400
- **Blocos integralmente indexados:** 39
- **Geração:** 2026-08-10T13:53:35-03:00
- **Cobertura:** 100% das linhas e do texto da origem, sem omissão.
- **Links relativos normalizados:** 0 destino(s), apenas para preservar a navegação na cópia.

## Roteiro de consulta para IA

**Síntese de localização:** Produto: FORJA, harness técnico para produção jurídica auditável Versão: N2.0 Data: 2026-07-08 Status: vigente para implementação PRD: 01PRDFORJA.md Roadmap: 03ROADMAPFORJA.md Diagramas: 04DIAGRAMASFORJA.md Manifest: FORJAHARNESS/FORJASPECMANIFEST.json Gates de qualidade: 06GATESQUALIDADEFORJA.md — catálogo canônico minerado das entregas reais; os contratos…

**Termos de recuperação:** json, não, entrada, oficial, saída, bloqueia, fontes, final, deve, status, fase, draft.

Use o índice abaixo para localizar o bloco pertinente. Cada entrada informa as linhas exatas no documento de origem. Para afirmações materiais, leia o bloco integral e confira o arquivo canônico pelo SHA-256.

## Índice detalhado e cobertura integral

- [SRC-S001 · L1–L16 · TDD — FORJA N2](#src-s001)
  - Assuntos: tdd, técnico, manifest, gates, catálogo, este, produto, harness
  - Trecho-guia: Produto: FORJA, harness técnico para produção jurídica auditável Versão: N2.0 Data: 2026-07-08 Status: vigente para implementação PRD: 01PRDFORJA.md Roadmap: 03ROADMAPFORJA.md Diagramas: 04DIAGRAMASFORJA.md Manifest: FORJAHARNESS/FORJASPECMANIFEST.json Gates de qualidade: 06GATES
  - SHA-256 do bloco: `8b4f67cee4a86834d454a4b949608c904725829826340d1c09041d29daefb402`
  - [SRC-S002 · L17–L24 · 1. Objetivo técnico](#src-s002)
    - Caminho: TDD — FORJA N2 > 1. Objetivo técnico
    - Assuntos: técnico, objetivo, sistema, deve, pesquisa, oficial, visual, evidência
    - Trecho-guia: Implementar FORJA como orquestrador local, persistente e bloqueante para demandas jurídicas da fábrica. O sistema deve coordenar ingestão, fontes, regimento, planejamento, pesquisa oficial, redação, auditoria, QA visual, pacote de revisão e fechamento com evidência.
    - SHA-256 do bloco: `ee2090376325ef152206dde5fce36006e1a27df2ec5c6ebd7d32aa9c2c74885d`
  - [SRC-S003 · L25–L26 · 2. Topologia](#src-s003)
    - Caminho: TDD — FORJA N2 > 2. Topologia
    - Assuntos: topologia
    - Trecho-guia: Documento de consulta sobre 2. Topologia.
    - SHA-256 do bloco: `632daf06867ecf82c58160cba01d2ea53b93d79b62ba52c46ca60f5a1e2ea61e`
    - [SRC-S004 · L27–L33 · PC local Igor](#src-s004)
      - Caminho: TDD — FORJA N2 > 2. Topologia > PC local Igor
      - Assuntos: local, igor, gestao_escritorio, painel, dados, fila, forja_harness, orquestrador
      - Trecho-guia: gestaoescritorio como painel e dados de fila. FORJAHARNESS como orquestrador, estado, logs e documentação. Word COM para DOCX/PDF final. Inkscape, Graphviz, Mermaid CLI e Tectonic para visual law quando aplicável.
      - SHA-256 do bloco: `fec08c8ec0052b7e1a2ab0fe53db97f7914aa48e1c74674d0e50914679dc2239`
    - [SRC-S005 · L34–L39 · VPS Hermes](#src-s005)
      - Caminho: TDD — FORJA N2 > 2. Topologia > VPS Hermes
      - Assuntos: vps, hermes, não, fonte, sinais, whatsapp, apenas, quando
      - Trecho-guia: Fonte de sinais WhatsApp apenas quando sanitizados. Não processar nem expor conversa bruta. Não usar VPS antiga como destino padrão.
      - SHA-256 do bloco: `e3648016fe3a20fef10749acbd60793f64d5fb1b23a3eec0075095e3ca8548e0`
    - [SRC-S006 · L40–L47 · Google](#src-s006)
      - Caminho: TDD — FORJA N2 > 2. Topologia > Google
      - Assuntos: google, gmail, gws, leitura, draft, quando, autenticado, calendar
      - Trecho-guia: Gmail/gws para leitura/draft quando autenticado. Calendar é lembrete humano, não executor técnico. Automação real deve ser Codex automation, Windows Task Scheduler ou serviço local validado.
      - SHA-256 do bloco: `0b2609f5fc0ab3ef49e2f59e80339a95f4b0a2b15dee2fc410271c555615b24f`
  - [SRC-S007 · L48–L68 · 3. Componentes](#src-s007)
    - Caminho: TDD — FORJA N2 > 3. Componentes
    - Assuntos: gerar, componentes, json, fonte, anexos, citações, registrar, componente
    - Trecho-guia: Nomes acima são contratos funcionais. A implementação pode usar scripts ou serviços diferentes, desde que preserve entradas, saídas e gates.
    - SHA-256 do bloco: `927e4a947f43fde87bbef6a57fb6b42e19965c7eb610b88390f376bb1dbf9628`
  - [SRC-S008 · L69–L95 · 4. Estrutura de arquivos](#src-s008)
    - Caminho: TDD — FORJA N2 > 4. Estrutura de arquivos
    - Assuntos: json, estrutura, arquivos, state, text, forja_harness, forja_spec_manifest, planejamento
    - Trecho-guia: Se a pasta state/ ainda não existir, a primeira implementação deve criá-la.
    - SHA-256 do bloco: `8b80bdbc43eaa5be9179179cd01149c21c5e3ab9edf7d3b0b4ea27ffe16ced0b`
  - [SRC-S009 · L96–L97 · 5. Schema de estado](#src-s009)
    - Caminho: TDD — FORJA N2 > 5. Schema de estado
    - Assuntos: schema, estado
    - Trecho-guia: Documento de consulta sobre 5. Schema de estado.
    - SHA-256 do bloco: `15fe94d0f57865ae112072f0bbb75d8aefe0a4494944c3943420b87bec1d8926`
    - [SRC-S010 · L98–L121 · FORJASTATE.json](#src-s010)
      - Caminho: TDD — FORJA N2 > 5. Schema de estado > FORJASTATE.json
      - Assuntos: json, t00, forjastate, forja_state, caseid, case-, specversion, createdat
      - Trecho-guia: Documento de consulta sobre FORJASTATE.json.
      - SHA-256 do bloco: `7f28247238fdea6f803f19244de2df165ca715a5f57bf71380d68bcee96c543a`
    - [SRC-S011 · L122–L133 · Status válidos](#src-s011)
      - Caminho: TDD — FORJA N2 > 5. Schema de estado > Status válidos
      - Assuntos: status, válidos, pending, running, blocked, degraded, ready_for_review, waiting_delivery_evidence
      - Trecho-guia: pending running blocked degraded readyforreview waitingdeliveryevidence fulfilled cancelled failed
      - SHA-256 do bloco: `466ea3d9da1b18219d09f35224a7229d3776b28cfcced2c67358702921c314f2`
    - [SRC-S012 · L134–L141 · Severidade de bloqueio](#src-s012)
      - Caminho: TDD — FORJA N2 > 5. Schema de estado > Severidade de bloqueio
      - Assuntos: severidade, bloqueio, impede, peça, final, draft, marcação, pronta
      - Trecho-guia: P0: impede peça final, draft ou marcação como pronta. P1: permite continuar fase interna, mas exige correção antes de F9. P2: melhoria ou alerta de qualidade.
      - SHA-256 do bloco: `890a0d8f570ea8a30b94caaebac97e5430b64a889aea6fb8cab45786c9ef02c8`
  - [SRC-S013 · L142–L173 · 6. Extensão em demandas.json](#src-s013)
    - Caminho: TDD — FORJA N2 > 6. Extensão em demandas.json
    - Assuntos: json, null, extensão, demandas, version, enabled, true, caseid
    - Trecho-guia: Regra: o JSON operacional registra somente o que serve para execução e auditoria: IDs, pasta, comando, anexos, gates, fontes, evidências, artefatos e custos. Conteúdo completo de comunicação só entra quando for artefato necessário do caso, com caminho e origem.
    - SHA-256 do bloco: `0a791dd129b33c05b0b75c3f6138e93bf1f2c128777717317f2439b1f7965316`
  - [SRC-S014 · L174–L175 · 7. Contratos por fase](#src-s014)
    - Caminho: TDD — FORJA N2 > 7. Contratos por fase
    - Assuntos: contratos, fase
    - Trecho-guia: Documento de consulta sobre 7. Contratos por fase.
    - SHA-256 do bloco: `7df3bd9dd39cd784fa22acef54175b7bbfb04ab3e3696a92657f80568a295233`
    - [SRC-S015 · L176–L182 · F0 — Reconciliação da fila](#src-s015)
      - Caminho: TDD — FORJA N2 > 7. Contratos por fase > F0 — Reconciliação da fila
      - Assuntos: json, reconciliação, fila, entrada, demandas, intervencoes_manuais, status_integracoes, comandos
      - Trecho-guia: Entrada: demandas.json, intervencoesmanuais.json, statusintegracoes.json, comandos, pastas, evidências. Saída: estado de integrações, pendências e FORJASTATE.json criado/atualizado. Bloqueia se: demanda sem pasta, sem comando, sem origem ou com status contraditório. Observação: G
      - SHA-256 do bloco: `6a71de7898d69c4c8655e9149842ea1970266ee37d9442c9b3aa98b222887df9`
    - [SRC-S016 · L183–L188 · F1 — Ingestão segura](#src-s016)
      - Caminho: TDD — FORJA N2 > 7. Contratos por fase > F1 — Ingestão segura
      - Assuntos: comando, ingestão, segura, entrada, pasta, e-mail, sinal, sanitizado
      - Trecho-guia: Entrada: e-mail/comando/sinal sanitizado. Saída: pasta, comando, lista de anexos, hashes quando viável, entrada do painel. Bloqueia se: anexo essencial faltando, pasta ambígua sem deduplicação ou comando vazio.
      - SHA-256 do bloco: `24e7b6cfaaabe70415a75139e1eb319d2ca4372d9ddb728206c249799394d003`
    - [SRC-S017 · L189–L195 · F2 — Classificação produto/risco](#src-s017)
      - Caminho: TDD — FORJA N2 > 7. Contratos por fase > F2 — Classificação produto/risco
      - Assuntos: produto, classificação, risco, comando, tipo, tribunal, resposta, rota
      - Trecho-guia: Entrada: comando e inventário inicial. Saída: tipo de produto, tribunal provável, prazo, urgência, destinatário de revisão, evidência mínima e F2QUESTIONTREE.json no protocolo FORJA-F2A-100-v1. Contrato F2-A: exatamente 100 perguntas Q001..Q100; 10 óticas × 10; pergunta, âncora, 
      - SHA-256 do bloco: `8d949d3b12b166d82968819e2cfa907ad3ca62badf007a6d90ad9124f6fc14fa`
    - [SRC-S018 · L196–L201 · F3 — Fontes, regimento e leis gerais](#src-s018)
      - Caminho: TDD — FORJA N2 > 7. Contratos por fase > F3 — Fontes, regimento e leis gerais
      - Assuntos: regimento, fontes, leis, gerais, entrada, pasta, caso, comando
      - Trecho-guia: Entrada: pasta do caso, comando, LEISGERAIS, regimento e F2QUESTIONTREE.json. Saída: F3MAPAFONTESEREGIMENTO.md e ledger de fontes. Bloqueia se: regimento ausente/incompleto, emendas sem conferência, fonte crítica não localizada.
      - SHA-256 do bloco: `92cda2ad62c93e7dfac4c6f9448d41f43234a1ba04e98e2031a9963cfe15a0d2`
    - [SRC-S019 · L202–L207 · F4 — Blueprint estratégico](#src-s019)
      - Caminho: TDD — FORJA N2 > 7. Contratos por fase > F4 — Blueprint estratégico
      - Assuntos: blueprint, estratégico, entrada, mapa, fontes, documentos, produto, risco
      - Trecho-guia: Entrada: mapa de fontes, documentos, produto, risco e F2QUESTIONTREE.json. Saída: F4BLUEPRINTESTRATEGICO.md. Bloqueia se: tese depende de fato não documentado sem marcação, ou divergência estratégica grave sem decisão.
      - SHA-256 do bloco: `7082ec4ee357a772feceb2dcc7c8634bf3f80f22293ef1b482d72718fc913cee`
    - [SRC-S020 · L208–L213 · F5 — Pesquisa oficial](#src-s020)
      - Caminho: TDD — FORJA N2 > 7. Contratos por fase > F5 — Pesquisa oficial
      - Assuntos: oficial, pesquisa, entrada, blueprint, temas, saída, f5_jurisprudencia_verificada, f5_citacoes_removidas
      - Trecho-guia: Entrada: blueprint e temas de pesquisa. Saída: F5JURISPRUDENCIAVERIFICADA.md, F5CITACOESREMOVIDAS.md. Bloqueia se: citação final não tem fonte oficial ou arquivo oficial arquivado.
      - SHA-256 do bloco: `91621b7ac94c2370666ad4289439aedf4f348fde8d016e1ed89b3d5305575b94`
    - [SRC-S021 · L214–L219 · F6 — Redação em template](#src-s021)
      - Caminho: TDD — FORJA N2 > 7. Contratos por fase > F6 — Redação em template
      - Assuntos: template, redação, entrada, peça, anterior, blueprint, fontes, citações
      - Trecho-guia: Entrada: template/peça anterior, blueprint, fontes e citações verificadas. Saída: minuta DOCX. Bloqueia se: documento nasceu de arquivo vazio, quebrou timbre/padrão, contém placeholder ou usa fato sem fonte.
      - SHA-256 do bloco: `04e948d71f3c19d536b73bcc4723c14b1ef622746ef2d845df4e989a2f0b1f0e`
    - [SRC-S022 · L220–L225 · F7 — Auditoria jurídica/factual](#src-s022)
      - Caminho: TDD — FORJA N2 > 7. Contratos por fase > F7 — Auditoria jurídica/factual
      - Assuntos: auditoria, jurídica, factual, entrada, minuta, ledger, jurisprudência, anexos
      - Trecho-guia: Entrada: minuta, ledger, jurisprudência, anexos e regimento. Saída: F7RELATORIOAUDITORIA.md, CHECKLISTFONTESEPENDENCIAS.md. Bloqueia se: qualquer P0 estiver aberto.
      - SHA-256 do bloco: `37341f9babdb9963ce6118682c5a5ad781882f6cb50d83574bc0cd8c09612ed1`
      - [SRC-S023 · L226–L247 · F7-B — Revisão editorial e escrita final pelo Claude Fable 5](#src-s023)
        - Caminho: TDD — FORJA N2 > 7. Contratos por fase > F7 — Auditoria jurídica/factual > F7-B — Revisão editorial e escrita final pelo Claude Fable 5
        - Assuntos: não, claude, json, fragmento, editorial, final, fable, audited_markdown
        - Trecho-guia: Posição: subfase de F7 executada somente depois de f7gateresult comprovar zero P0 e antes de F8.
        - SHA-256 do bloco: `a9a3788c526e0eec04ffc86c4305b575f256302ba5ab50fcf9263bd546f84e0b`
    - [SRC-S024 · L248–L253 · F8 — QA visual](#src-s024)
      - Caminho: TDD — FORJA N2 > 7. Contratos por fase > F8 — QA visual
      - Assuntos: visual, entrada, docx, auditado, saída, pdf, imagens, renderizadas
      - Trecho-guia: Entrada: DOCX auditado. Saída: PDF, imagens renderizadas, relatório de inspeção. Bloqueia se: qualquer página não foi inspecionada, diagrama ilegível, rodapé/timbre/folio quebrado ou sobreposição.
      - SHA-256 do bloco: `c3d2cf8d1f3b242539c0d3f265c926f0d1140b262787772f693cd6fc1c5b5fc2`
    - [SRC-S025 · L254–L259 · F9 — Pacote de revisão e draft opcional](#src-s025)
      - Caminho: TDD — FORJA N2 > 7. Contratos por fase > F9 — Pacote de revisão e draft opcional
      - Assuntos: draft, pacote, revisão, opcional, gmail, entrada, docx, pdf
      - Trecho-guia: Entrada: DOCX/PDF aprovados e checklist sem P0. Saída: pacote de revisão; draft Gmail apenas se autorizado. Bloqueia se: approvedRecipients vazio para draft, anexos errados, Gmail degradado sem fallback manual.
      - SHA-256 do bloco: `2092d2d5dba8efa909ab41a3d69b621f827ab892bf64272d30fbc97e5db96ca6`
    - [SRC-S026 · L260–L267 · F10 — Entrega, evidência e aprendizado](#src-s026)
      - Caminho: TDD — FORJA N2 > 7. Contratos por fase > F10 — Entrega, evidência e aprendizado
      - Assuntos: evidência, entrega, aprendizado, f10, entrada, protocolo, envio, intervenção
      - Trecho-guia: Entrada: evidência de entrega/protocolo/envio ou intervenção manual. Saída: F10DOCUMENTACAOFINAL/, atualização de painel, aprendizado. Bloqueia se: não houver evidência real.
      - SHA-256 do bloco: `ff5f589adaaf9047a268cb52a7995d094696f385f3c0f94bc11f7319fe2eb6ad`
  - [SRC-S027 · L268–L287 · 8. Ledger de fontes](#src-s027)
    - Caminho: TDD — FORJA N2 > 8. Ledger de fontes
    - Assuntos: ledger, fontes, item, nao_verificado, finaluseallowed, cada, crítico, deve
    - Trecho-guia: Cada item crítico deve ser gravado com:
    - SHA-256 do bloco: `f975a6cf947e828154271a43815e3409410e8df31f81085d1aef2e45ebd7389f`
  - [SRC-S028 · L288–L289 · 9. Adaptadores técnicos](#src-s028)
    - Caminho: TDD — FORJA N2 > 9. Adaptadores técnicos
    - Assuntos: adaptadores, técnicos
    - Trecho-guia: Documento de consulta sobre 9. Adaptadores técnicos.
    - SHA-256 do bloco: `11e0f212b4d68c2bca1f1c7578b91b588f624c37ea6ba52e83e732080545e492`
    - [SRC-S029 · L290–L296 · Gmail/gws](#src-s029)
      - Caminho: TDD — FORJA N2 > 9. Adaptadores técnicos > Gmail/gws
      - Assuntos: gws, gmail, preferir, cmd, powershell, invalid_grant, precisa_login, vira
      - Trecho-guia: Preferir gws.cmd em PowerShell. invalidgrant ou precisalogin vira needslogin. Draft depende de autorização e destinatários da demanda. Nunca enviar automaticamente.
      - SHA-256 do bloco: `7bc2d7ca7938f3cf4a5ff45eb42ee81904107855fc21206cb07da8266583073e`
    - [SRC-S030 · L297–L301 · Hermes/WhatsApp](#src-s030)
      - Caminho: TDD — FORJA N2 > 9. Adaptadores técnicos > Hermes/WhatsApp
      - Assuntos: hermes, whatsapp, entrada, permitida, sinal, sanitizado, card, triagem
      - Trecho-guia: Entrada permitida: sinal sanitizado, card de triagem, COMANDODOWHATSAPP.md. Proibido: conversa bruta em painel, chat ou relatório público.
      - SHA-256 do bloco: `4128040b535cbaf694b802abde228bd56524edf08ef986a1558e997c6001a61e`
    - [SRC-S031 · L302–L306 · Pesquisa oficial](#src-s031)
      - Caminho: TDD — FORJA N2 > 9. Adaptadores técnicos > Pesquisa oficial
      - Assuntos: oficial, pesquisa, fonte, não, apenas, descoberta, arquivo, arquivado
      - Trecho-guia: Fonte não oficial é apenas descoberta. Fonte oficial ou arquivo oficial arquivado é obrigatório para citação final.
      - SHA-256 do bloco: `bbdb04eb086858dd1be154b2f89950831eb86be2a5dedac86a70a2a29d0bf4bc`
    - [SRC-S032 · L307–L313 · Word/visual law](#src-s032)
      - Caminho: TDD — FORJA N2 > 9. Adaptadores técnicos > Word/visual law
      - Assuntos: word, visual, law, final, via, docx, deve, partir
      - Trecho-guia: DOCX final deve partir de template ou peça anterior. PDF final via Word COM. SVG para EMF via Inkscape quando houver diagrama vetorial. Render e inspeção de todas as páginas.
      - SHA-256 do bloco: `58c06808be125de655cf913c2d4debd49d96728ce66e6806ba1a97eef9ce8999`
    - [SRC-S033 · L314–L320 · Custos](#src-s033)
      - Caminho: TDD — FORJA N2 > 9. Adaptadores técnicos > Custos
      - Assuntos: custo, custos, registrar, modelo, tokens, estimado, real, quando
      - Trecho-guia: Registrar modelo, tokens, custo estimado e custo real quando disponível. Se custo exceder limite configurado, bloquear e pedir autorização.
      - SHA-256 do bloco: `84ee9a878b4ecd1e3421898cd65411ba3131eddaede72a4f3634f42795394c70`
  - [SRC-S034 · L321–L337 · 10. APIs locais sugeridas](#src-s034)
    - Caminho: TDD — FORJA N2 > 10. APIs locais sugeridas
    - Assuntos: api, post, caseid, apis, locais, sugeridas, endpoints, get
    - Trecho-guia: Se integradas ao painel local, usar endpoints com semântica conservadora:
    - SHA-256 do bloco: `d56896ce9467d5aa70266c09caa42e071dfacfd1c5b3bf17ffe53a29584a9ae1`
  - [SRC-S035 · L338–L351 · 11. Tratamento de erros](#src-s035)
    - Caminho: TDD — FORJA N2 > 11. Tratamento de erros
    - Assuntos: blocked, não, tratamento, erros, login, degraded, fallback, ausente
    - Trecho-guia: Documento de consulta sobre 11. Tratamento de erros.
    - SHA-256 do bloco: `9bf66ccbbaef90de66420c02e658c0b6eaf97f3dde85d3ee51e1ce8f5a7d37ea`
  - [SRC-S036 · L352–L363 · 12. Proibições técnicas](#src-s036)
    - Caminho: TDD — FORJA N2 > 12. Proibições técnicas
    - Assuntos: não, usar, proibições, técnicas, final, git, reset, hard
    - Trecho-guia: Não usar git reset --hard ou checkout destrutivo. Não mover conteúdo de SOMBRA para pasta principal automaticamente. Não apagar duplicidades sem inventário e recomendação. Não transformar conversa, anotação ou resumo em prova de entrega sem evidência arquivada. Não usar Document(
    - SHA-256 do bloco: `9bb0b0501ab6db0888b4e6d9845b0a4cb6fcc128f053a69fc570a7f30223dac2`
  - [SRC-S037 · L364–L378 · 13. Ordem de implementação recomendada](#src-s037)
    - Caminho: TDD — FORJA N2 > 13. Ordem de implementação recomendada
    - Assuntos: ordem, implementação, recomendada, evidência, estado, schema, manifest, reconciliação
    - Trecho-guia: 1. Estado, schema e manifest. 2. Reconciliação de fila e evidência. 3. Gate de fontes/regimento. 4. Pesquisa oficial e ledger. 5. Redação com template. 6. Auditoria e QA visual. 7. Draft opcional. 8. Fechamento com evidência.
    - SHA-256 do bloco: `c6996523a5a8379b2b9496b6cee054ee3ada793a02370bbfcdc71576e86ae6a0`
  - [SRC-S038 · L379–L395 · 14. Subsistema de auditoria adversarial — A1](#src-s038)
    - Caminho: TDD — FORJA N2 > 14. Subsistema de auditoria adversarial — A1
    - Assuntos: produz, vinculado, audit, subsistema, auditoria, adversarial, peças, hashes
    - Trecho-guia: forjaadversarialaudit.py implementa um ledger encadeado para peças responsivas:
    - SHA-256 do bloco: `d2e633ff1f91beb40c88f3f7fb0824201af7814a4a3633caf2c0385679c470a9`
  - [SRC-S039 · L396–L400 · 15. Adendo técnico implementado — cânone editorial F7-B (15/07/2026)](#src-s039)
    - Caminho: TDD — FORJA N2 > 15. Adendo técnico implementado — cânone editorial F7-B (15/07/2026)
    - Assuntos: adendo, técnico, implementado, cânone, editorial, f7-b, contrato, final_markdown
    - Trecho-guia: A integração acima é aditiva ao desenho N2 histórico. O contrato vigente de F7 inclui finalmarkdown, editorialreport, editorialdiff, fable5usage e editorialfidelity; o contrato F8 exige finalmarkdown junto da trilha auditada. Para múltiplos textos, IDs e nomes usam sufixo seguro 
    - SHA-256 do bloco: `ad141894e9d0f23b45e492c0b9da67c54cd4407a85da84cc97dfada030167590`

## Conteúdo integral indexado

Os marcadores HTML abaixo são apenas âncoras de navegação. O texto reproduz integralmente a origem normalizada em UTF-8; somente destinos de links relativos podem ter sido recalculados para apontar ao mesmo arquivo a partir desta pasta.

<a id="src-s001"></a>

# TDD — FORJA N2

**Produto:** FORJA, harness técnico para produção jurídica auditável  
**Versão:** N2.0  
**Data:** 2026-07-08  
**Status:** vigente para implementação  
**PRD:** `01_PRD_FORJA.md`  
**Roadmap:** `03_ROADMAP_FORJA.md`  
**Diagramas:** `04_DIAGRAMAS_FORJA.md`  
**Manifest:** `_FORJA_HARNESS/FORJA_SPEC_MANIFEST.json`  
**Gates de qualidade:** `06_GATES_QUALIDADE_FORJA.md` — catálogo canônico minerado das entregas reais; os contratos por fase da seção 7 DEVEM implementar os gates G* correspondentes (em conflito, o catálogo detalha e o manifest arbitra).

> Este TDD substitui o desenho técnico v1.0. Nenhum agente deve usar flags, custos, escopo ou estados do TDD antigo sem validar contra este documento.

---


<a id="src-s002"></a>

## 1. Objetivo técnico

Implementar FORJA como orquestrador local, persistente e bloqueante para demandas jurídicas da fábrica. O sistema deve coordenar ingestão, fontes, regimento, planejamento, pesquisa oficial, redação, auditoria, QA visual, pacote de revisão e fechamento com evidência.

O design técnico é conservador: primeiro estado, contratos e evidência; depois automação headless. O sistema deve degradar explicitamente quando Gmail, Hermes, pesquisa oficial, Word COM ou ferramenta visual falhar.

---


<a id="src-s003"></a>

## 2. Topologia


<a id="src-s004"></a>

### PC local Igor

- `gestao_escritorio` como painel e dados de fila.
- `_FORJA_HARNESS` como orquestrador, estado, logs e documentação.
- Word COM para DOCX/PDF final.
- Inkscape, Graphviz, Mermaid CLI e Tectonic para visual law quando aplicável.


<a id="src-s005"></a>

### VPS Hermes

- Fonte de sinais WhatsApp apenas quando sanitizados.
- Não processar nem expor conversa bruta.
- Não usar VPS antiga como destino padrão.


<a id="src-s006"></a>

### Google

- Gmail/gws para leitura/draft quando autenticado.
- Calendar é lembrete humano, não executor técnico.
- Automação real deve ser Codex automation, Windows Task Scheduler ou serviço local validado.

---


<a id="src-s007"></a>

## 3. Componentes

| Componente | Responsabilidade |
|---|---|
| `FORJA_SPEC_MANIFEST.json` | fonte normativa de versão, regras e fases |
| `FORJA_STATE.json` | estado persistente por caso |
| `forja_reconcile` | ler painel, comandos, pastas e evidências |
| `forja_ingest` | criar/reconciliar demanda, pasta e anexos |
| `forja_sources` | montar ledger de fontes, regimento e leis gerais |
| `forja_blueprint` | produzir plano jurídico com divergências registradas |
| `forja_official_search` | validar citações em fonte oficial |
| `forja_draft` | gerar DOCX a partir de template ou peça anterior |
| `forja_audit` | verificar fatos, citações, prazos, anexos, placeholders e metadados |
| `forja_visual_qa` | gerar PDF, renderizar páginas e registrar inspeção |
| `forja_delivery` | gerar pacote, draft opcional e reconciliação de evidência |
| `forja_costs` | registrar custo real por fase |

Nomes acima são contratos funcionais. A implementação pode usar scripts ou serviços diferentes, desde que preserve entradas, saídas e gates.

---


<a id="src-s008"></a>

## 4. Estrutura de arquivos

```text
_FORJA_HARNESS/
  FORJA_SPEC_MANIFEST.json
  planejamento/
    01_PRD_FORJA.md
    02_TDD_FORJA.md
    03_ROADMAP_FORJA.md
    04_DIAGRAMAS_FORJA.md
    05_FORJA_NIVEL_2_ANALISE_E_PLANO_CORRIGIDO.md
  state/
    <caseId>/
      FORJA_STATE.json
      logs/
      checkpoints/
      artifacts.json
  cache/
    fontes_oficiais/
    jurisprudencia/
  reports/
```

Se a pasta `state/` ainda não existir, a primeira implementação deve criá-la.

---


<a id="src-s009"></a>

## 5. Schema de estado


<a id="src-s010"></a>

### `FORJA_STATE.json`

```json
{
  "caseId": "case-...",
  "specVersion": "N2.0",
  "createdAt": "2026-07-08T00:00:00-03:00",
  "updatedAt": "2026-07-08T00:00:00-03:00",
  "currentPhase": "F0_RECONCILIACAO_FILA",
  "status": "running",
  "inputs": {
    "demandId": "demanda-...",
    "caseFolder": "C:/...",
    "commandFile": "COMANDO_DO_EMAIL.md"
  },
  "phaseHistory": [],
  "artifacts": [],
  "gates": [],
  "sourceLedger": [],
  "deliveryEvidence": null,
  "costLog": []
}
```


<a id="src-s011"></a>

### Status válidos

- `pending`
- `running`
- `blocked`
- `degraded`
- `ready_for_review`
- `waiting_delivery_evidence`
- `fulfilled`
- `cancelled`
- `failed`


<a id="src-s012"></a>

### Severidade de bloqueio

- `P0`: impede peça final, draft ou marcação como pronta.
- `P1`: permite continuar fase interna, mas exige correção antes de F9.
- `P2`: melhoria ou alerta de qualidade.

---


<a id="src-s013"></a>

## 6. Extensão em `demandas.json`

```json
{
  "forja": {
    "version": "N2.0",
    "enabled": true,
    "caseId": "case-...",
    "phase": "F0_RECONCILIACAO_FILA",
    "phaseStatus": "running",
    "caseFolder": "C:/...",
    "commandFile": "COMANDO_DO_EMAIL.md",
    "approvedRecipients": [],
    "blockedReasons": [],
    "deliveryEvidence": {
      "status": "none|draft_created|sent_confirmed|manual_override",
      "path": null,
      "confirmedAt": null
    },
    "costs": {
      "budgetUsd": null,
      "actualUsd": null,
      "requiresApproval": false
    }
  }
}
```

Regra: o JSON operacional registra somente o que serve para execução e auditoria: IDs, pasta, comando, anexos, gates, fontes, evidências, artefatos e custos. Conteúdo completo de comunicação só entra quando for artefato necessário do caso, com caminho e origem.

---


<a id="src-s014"></a>

## 7. Contratos por fase


<a id="src-s015"></a>

### F0 — Reconciliação da fila

**Entrada:** `demandas.json`, `intervencoes_manuais.json`, `status_integracoes.json`, comandos, pastas, evidências.  
**Saída:** estado de integrações, pendências e `FORJA_STATE.json` criado/atualizado.  
**Bloqueia se:** demanda sem pasta, sem comando, sem origem ou com status contraditório.  
**Observação:** Gmail sem login vira `degraded` ou `needs_login`, nunca `ok`.


<a id="src-s016"></a>

### F1 — Ingestão segura

**Entrada:** e-mail/comando/sinal sanitizado.  
**Saída:** pasta, comando, lista de anexos, hashes quando viável, entrada do painel.  
**Bloqueia se:** anexo essencial faltando, pasta ambígua sem deduplicação ou comando vazio.


<a id="src-s017"></a>

### F2 — Classificação produto/risco

**Entrada:** comando e inventário inicial.
**Saída:** tipo de produto, tribunal provável, prazo, urgência, destinatário de revisão, evidência mínima e `F2_QUESTION_TREE.json` no protocolo `FORJA-F2A-100-v1`.
**Contrato F2-A:** exatamente 100 perguntas `Q001..Q100`; 10 óticas × 10; pergunta, âncora, importância, resposta, natureza epistemológica e rota; fatos/eventos/precedentes/cálculos com `supportIds`; lacunas com consequência; duas soluções comparadas; definição do problema, diagnóstico e handoff F3–F7.
**Bloqueia se:** tipo de produto indefinido, tribunal indefinido quando necessário, pasta/comando ausente, anexos esperados não mapeados, contagem/diversidade inválida, resposta factual sem lastro, rota ausente ou questão material bloqueada para fins de F6.


<a id="src-s018"></a>

### F3 — Fontes, regimento e leis gerais

**Entrada:** pasta do caso, comando, `_LEIS_GERAIS`, regimento e `F2_QUESTION_TREE.json`.
**Saída:** `F3_MAPA_FONTES_E_REGIMENTO.md` e ledger de fontes.  
**Bloqueia se:** regimento ausente/incompleto, emendas sem conferência, fonte crítica não localizada.


<a id="src-s019"></a>

### F4 — Blueprint estratégico

**Entrada:** mapa de fontes, documentos, produto, risco e `F2_QUESTION_TREE.json`.
**Saída:** `F4_BLUEPRINT_ESTRATEGICO.md`.  
**Bloqueia se:** tese depende de fato não documentado sem marcação, ou divergência estratégica grave sem decisão.


<a id="src-s020"></a>

### F5 — Pesquisa oficial

**Entrada:** blueprint e temas de pesquisa.  
**Saída:** `F5_JURISPRUDENCIA_VERIFICADA.md`, `F5_CITACOES_REMOVIDAS.md`.  
**Bloqueia se:** citação final não tem fonte oficial ou arquivo oficial arquivado.


<a id="src-s021"></a>

### F6 — Redação em template

**Entrada:** template/peça anterior, blueprint, fontes e citações verificadas.  
**Saída:** minuta DOCX.  
**Bloqueia se:** documento nasceu de arquivo vazio, quebrou timbre/padrão, contém placeholder ou usa fato sem fonte.


<a id="src-s022"></a>

### F7 — Auditoria jurídica/factual

**Entrada:** minuta, ledger, jurisprudência, anexos e regimento.  
**Saída:** `F7_RELATORIO_AUDITORIA.md`, `CHECKLIST_FONTES_E_PENDENCIAS.md`.  
**Bloqueia se:** qualquer P0 estiver aberto.


<a id="src-s023"></a>

#### F7-B — Revisão editorial e escrita final pelo Claude Fable 5

**Posição:** subfase de F7 executada somente depois de `f7_gate_result` comprovar zero P0 e antes de F8.

**Executor:** `forja_fable5.py`; o runner genérico não a dispara automaticamente.

**Entrada:** `audited_markdown`, `f7_gate_result`, `RUN_CONTEXT.json` da tentativa F7.

**Saída canônica:** `final_markdown`; F8 e pacotes novos não usam `audited_markdown` como texto final.

**Evidências:** `editorial_report`, `editorial_diff`, `fable5_usage`, `editorial_fidelity` e o fragmento `FABLE5_RESULT`.

**Bloqueia se:** OAuth Claude Max não for comprovado, o modelo real não for `claude-fable-5`, houver divergência de hash/invariante ou gate editorial reprovado.

O executor chama `claude -p --model fable --output-format json --permission-mode dontAsk --tools ""`, fornece o conteúdo por stdin e valida previamente `claude auth status` (`loggedIn=true`, `authMethod=claude.ai`, `subscriptionType=max`). Não usa API key. O envelope de uso deve registrar sessão, modelo, autenticação, hashes e tokens observados.

`forja_editorial_fidelity.py` recompõe, diretamente dos arquivos, quatro gates contratuais: `fable5_oauth_confirmed`, `editorial_source_hash_match`, `editorial_fidelity_pass` e `human_style_final_pass`. A fidelidade compara números/datas/valores, marcadores processuais, autoridades, aspas, marcadores de auditoria, títulos, retenção mínima de conteúdo, pedidos/fecho e ausência de origem operacional. O modelo não autocertifica a aprovação.

São permitidas três candidatas internas no total: a inicial e até dois retries. Cada retry recebe os achados determinísticos da candidata anterior, mas recomeça do `audited_markdown` original; não edita incrementalmente a saída rejeitada. Esse laço não altera `retryPolicy.maxAttempts=4` da fase F7: quatro tentativas de fase e três candidatas editoriais internas são contadores distintos.

`FABLE5_RESULT.json` contém apenas o fragmento `status`, `producer`, `producerRole`, `gates` e `artifacts`. Para promoção, o orquestrador deve incorporar esse fragmento ao `PHASE_RESULT.json` da tentativa, preservando também os artefatos jurídicos F7. O fragmento isolado nunca constitui resultado completo da fase.


<a id="src-s024"></a>

### F8 — QA visual

**Entrada:** DOCX auditado.  
**Saída:** PDF, imagens renderizadas, relatório de inspeção.  
**Bloqueia se:** qualquer página não foi inspecionada, diagrama ilegível, rodapé/timbre/folio quebrado ou sobreposição.


<a id="src-s025"></a>

### F9 — Pacote de revisão e draft opcional

**Entrada:** DOCX/PDF aprovados e checklist sem P0.  
**Saída:** pacote de revisão; draft Gmail apenas se autorizado.  
**Bloqueia se:** `approvedRecipients` vazio para draft, anexos errados, Gmail degradado sem fallback manual.


<a id="src-s026"></a>

### F10 — Entrega, evidência e aprendizado

**Entrada:** evidência de entrega/protocolo/envio ou intervenção manual.  
**Saída:** `F10_DOCUMENTACAO_FINAL/`, atualização de painel, aprendizado.  
**Bloqueia se:** não houver evidência real.

---


<a id="src-s027"></a>

## 8. Ledger de fontes

Cada item crítico deve ser gravado com:

```json
{
  "id": "src-001",
  "claim": "Fato ou citação usada",
  "classification": "FONTE_ARQUIVO|FONTE_OFICIAL|DECLARACAO|INFERENCIA|HIPOTESE|NAO_VERIFICADO",
  "sourcePathOrUrl": "C:/... ou URL oficial",
  "pageOrEvent": "p. 12 / evento 183 / item 4",
  "verifiedAt": "2026-07-08T00:00:00-03:00",
  "finalUseAllowed": true
}
```

`NAO_VERIFICADO` sempre tem `finalUseAllowed=false`.

---


<a id="src-s028"></a>

## 9. Adaptadores técnicos


<a id="src-s029"></a>

### Gmail/gws

- Preferir `gws.cmd` em PowerShell.
- `invalid_grant` ou `precisa_login` vira `needs_login`.
- Draft depende de autorização e destinatários da demanda.
- Nunca enviar automaticamente.


<a id="src-s030"></a>

### Hermes/WhatsApp

- Entrada permitida: sinal sanitizado, card de triagem, `COMANDO_DO_WHATSAPP.md`.
- Proibido: conversa bruta em painel, chat ou relatório público.


<a id="src-s031"></a>

### Pesquisa oficial

- Fonte não oficial é apenas descoberta.
- Fonte oficial ou arquivo oficial arquivado é obrigatório para citação final.


<a id="src-s032"></a>

### Word/visual law

- DOCX final deve partir de template ou peça anterior.
- PDF final via Word COM.
- SVG para EMF via Inkscape quando houver diagrama vetorial.
- Render e inspeção de todas as páginas.


<a id="src-s033"></a>

### Custos

- Registrar modelo, tokens, custo estimado e custo real quando disponível.
- Se custo exceder limite configurado, bloquear e pedir autorização.

---


<a id="src-s034"></a>

## 10. APIs locais sugeridas

Se integradas ao painel local, usar endpoints com semântica conservadora:

- `POST /api/forja/reconcile`
- `POST /api/forja/start`
- `GET /api/forja/status/<caseId>`
- `POST /api/forja/phase/<caseId>/advance`
- `POST /api/forja/block/<caseId>`
- `POST /api/forja/approve-draft/<caseId>`
- `POST /api/forja/delivery-evidence/<caseId>`
- `GET /api/forja/artifacts/<caseId>`

Endpoints não devem aceitar `cumprida` sem payload de evidência.

---


<a id="src-s035"></a>

## 11. Tratamento de erros

| Erro | Estado | Ação |
|---|---|---|
| Gmail sem login | `degraded` ou `needs_login` | mostrar login/fallback, não alegar leitura completa |
| Pasta/comando ausente | `blocked` P0 | pedir reconciliação manual |
| Regimento ausente | `blocked` P0 | obter PDF oficial integral e converter |
| Fonte oficial indisponível | `blocked` P0 se citação final depende disso | remover citação ou aguardar validação |
| Word COM falha | `degraded` | tentar novamente; fallback não vira final sem autorização |
| QA visual incompleto | `blocked` P0 | renderizar/inspecionar páginas faltantes |
| Sem evidência de entrega | `waiting_delivery_evidence` | manter pronta, não cumprida |

---


<a id="src-s036"></a>

## 12. Proibições técnicas

- Não usar `git reset --hard` ou checkout destrutivo.
- Não mover conteúdo de `_SOMBRA_*` para pasta principal automaticamente.
- Não apagar duplicidades sem inventário e recomendação.
- Não transformar conversa, anotação ou resumo em prova de entrega sem evidência arquivada.
- Não usar `Document()` vazio para peça final.
- Não usar Google Calendar como executor técnico.
- Não criar simulação de probabilidade de vitória como relatório final.

---


<a id="src-s037"></a>

## 13. Ordem de implementação recomendada

1. Estado, schema e manifest.
2. Reconciliação de fila e evidência.
3. Gate de fontes/regimento.
4. Pesquisa oficial e ledger.
5. Redação com template.
6. Auditoria e QA visual.
7. Draft opcional.
8. Fechamento com evidência.

Claude/headless ou multiagente só entram depois dos contratos acima existirem.

---


<a id="src-s038"></a>

## 14. Subsistema de auditoria adversarial — A1

`forja_adversarial_audit.py` implementa um ledger encadeado para peças responsivas:

1. F3 produz `adversarial_audit`, vinculado pelo SHA-256 à peça adversária;
2. F4 produz `adversarial_strategy`, vinculado ao hash do audit aprovado;
3. F7 produz `adversarial_recheck`, vinculado aos hashes do audit e da estratégia;
4. `forja_run.py` impede promoção quando o validador da fase rejeita o artefato;
5. `forja_package.py` incorpora os três hashes ao pacote N3;
6. `forja_delivery.py` exige o audit no fechamento N2 de novas peças detectadas como resposta.

O adaptador `forja_headless.py` injeta o protocolo obrigatório em F3, F4 e F7 independentemente do prompt fornecido ao agente. A classificação de produto normaliza acentos e reconhece as classes usuais de resposta. Casos não aplicáveis exigem justificativa explícita; não basta omitir o artefato.

O modelo de confiança é conservador: descoberta ampla, confirmação por fonte oficial, tentativa de refutação independente e autorização humana para qualquer acusação externa ou pedido sancionatório. Especificação integral em `planejamento/09_AUDITORIA_ADVERSARIAL_PONTOS_DECISIVOS.md`.

---


<a id="src-s039"></a>

## 15. Adendo técnico implementado — cânone editorial F7-B (15/07/2026)

A integração acima é aditiva ao desenho N2 histórico. O contrato vigente de F7 inclui `final_markdown`, `editorial_report`, `editorial_diff`, `fable5_usage` e `editorial_fidelity`; o contrato F8 exige `final_markdown` junto da trilha auditada. Para múltiplos textos, IDs e nomes usam sufixo seguro compartilhado, como `final_markdown_nota` e `audited_markdown_nota`, evitando associação por ordem ou nome aproximado.

Qualquer mudança material desejável identificada pelo editor deve permanecer em `duvidas` no relatório, sem entrar no texto. O limite semântico é de produto e não pode ser relaxado por prompt, retry ou decisão do modelo.
