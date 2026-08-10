# Consulta IA — 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes

> Cópia de consulta derivada. O documento canônico permanece no caminho de origem indicado abaixo.

## Metadados e rastreabilidade

- **Documento de origem:** `34_TDD_FORJA_ASSINATURA_LITE_COCRIACAO_PRECEDENTES.md`
- **Tipo:** TDD
- **SHA-256 da origem:** `bc81292493f3ce291dc1a29fc8c0c00e85a59ba5dc4cf6d440ca5f728aeafd05`
- **Linhas da origem:** 1001
- **Blocos integralmente indexados:** 59
- **Geração:** 2026-08-10T13:53:35-03:00
- **Cobertura:** 100% das linhas e do texto da origem, sem omissão.
- **Links relativos normalizados:** 0 destino(s), apenas para preservar a navegação na cópia.

## Roteiro de consulta para IA

**Síntese de localização:** EMENDAS NORMATIVAS — 25/07/2026. Este documento vale acrescido da seção 9 de 36CONSOLIDACAOCONSELHOEPARECERFINAL.md (emendas E1 a E16: conselho Helena e Cícero, migração do modelo editorial Fable 5 para Opus 5 com revisão cruzada entre famílias, perímetro de sigilo, testes negativos, registro de escopo e Onda -1). Em conflito, prevalece a seção 9. Os ANEXOA/…

**Termos de recuperação:** json, não, adicionar, fonte, status, null, namespace, modo, schema, override, not_applicable, tdd.

Use o índice abaixo para localizar o bloco pertinente. Cada entrada informa as linhas exatas no documento de origem. Para afirmações materiais, leia o bloco integral e confira o arquivo canônico pelo SHA-256.

## Índice detalhado e cobertura integral

- [SRC-S001 · L1–L16 · 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes](#src-s001)
  - Assuntos: tdd, planejamento, forja-assinatura, lite, cocrição, precedentes, emendas, este
  - Trecho-guia: EMENDAS NORMATIVAS — 25/07/2026. Este documento vale acrescido da seção 9 de 36CONSOLIDACAOCONSELHOEPARECERFINAL.md (emendas E1 a E16: conselho Helena e Cícero, migração do modelo editorial Fable 5 para Opus 5 com revisão cruzada entre famílias, perímetro de sigilo, testes negati
  - SHA-256 do bloco: `4f730161816c9982e61f031881f27c12197d0dce003cd5297b1191993417d01d`
  - [SRC-S002 · L17–L46 · 1. Objetivo técnico](#src-s002)
    - Caminho: 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes > 1. Objetivo técnico
    - Assuntos: json, objetivo, técnico, estender, esteira, criar, nova, fase
    - Trecho-guia: Estender a esteira F2–F7 sem criar nova fase canônica:
    - SHA-256 do bloco: `f8491346717b096e72461ae5bc8d69b92d522e9551310c602ce9283282763996`
  - [SRC-S003 · L47–L66 · 2. Restrições observadas no sistema vivo](#src-s003)
    - Caminho: 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes > 2. Restrições observadas no sistema vivo
    - Assuntos: não, restrições, observadas, sistema, vivo, são, generate_n4_contracts, fonte
    - Trecho-guia: 1. F0–F10 são resolvidas por forjaphasecontracts.py. 2. Schemas e contratos N4 são gerados por generaten4contracts.py. 3. forjan4common.ARTIFACTSPECS é fonte do catálogo gerado. 4. generaten4contracts.EXTENSIONS é fonte dos outputs e gates N4. 5. forjan4validate.VALIDATORS e sche
    - SHA-256 do bloco: `fc100df1b5876d9c630381e69a8fb7d3f7cf144d8585b533abf94b36f3a20c6a`
  - [SRC-S004 · L67–L68 · 3. Decisões arquiteturais](#src-s004)
    - Caminho: 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes > 3. Decisões arquiteturais
    - Assuntos: decisões, arquiteturais
    - Trecho-guia: Documento de consulta sobre 3. Decisões arquiteturais.
    - SHA-256 do bloco: `f2aae55a71dcaf082f513ba337532fc7e2181e97303c5c1f0951af90f386990b`
    - [SRC-S005 · L69–L72 · DA-01 — Sem nova fase](#src-s005)
      - Caminho: 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes > 3. Decisões arquiteturais > DA-01 — Sem nova fase
      - Assuntos: da-01, nova, fase, f2-b, f3-b, são, subestágios, observáveis
      - Trecho-guia: F2-B e F3-B são subestágios observáveis. A tupla F0–F10 permanece.
      - SHA-256 do bloco: `d4d49f6dce10bec53f2ea1ee5f5b8f2970cd62f2c996a45746f99911068cd950`
    - [SRC-S006 · L73–L93 · DA-02 — Namespace de feature próprio](#src-s006)
      - Caminho: 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes > 3. Decisões arquiteturais > DA-02 — Namespace de feature próprio
      - Assuntos: mode, da-02, namespace, feature, próprio, json, off, adicionar
      - Trecho-guia: Valores de mode: off, shadow, pilotblocking.
      - SHA-256 do bloco: `f99c39d5295a038a2b7c55d469f34ceb146645bd406ddd497ea44d48a45dc63f`
    - [SRC-S007 · L94–L106 · DA-03 — Compatibilidade por protocolo](#src-s007)
      - Caminho: 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes > 3. Decisões arquiteturais > DA-03 — Compatibilidade por protocolo
      - Assuntos: da-03, compatibilidade, protocolo, protocolos, envelope, continua, schemaversion, evolução
      - Trecho-guia: O envelope N4 continua schemaVersion: 1. A evolução aditiva será marcada por protocolos específicos:
      - SHA-256 do bloco: `e35d78e9cad48424cbefb9d303aa52a8aee7850749fe437062bf6685747f7cf0`
    - [SRC-S008 · L107–L122 · DA-04 — Schemas gerados, não editados isoladamente](#src-s008)
      - Caminho: 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes > 3. Decisões arquiteturais > DA-04 — Schemas gerados, não editados isoladamente
      - Assuntos: schemas, gerados, json, da-04, não, editados, isoladamente, phase_contracts_n4
      - Trecho-guia: forjan4common.py; generaten4contracts.py.
      - SHA-256 do bloco: `61750b309d9976050ed147d12575ce262d36f2b5c3b80f640ab240b7df03d34e`
    - [SRC-S009 · L123–L128 · DA-05 — Um draft](#src-s009)
      - Caminho: 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes > 3. Decisões arquiteturais > DA-05 — Um draft
      - Assuntos: da-05, draft, não, alterar, phase_contracts, json, múltiplos, candidatos
      - Trecho-guia: Não alterar phasecontracts/F6.json para múltiplos candidatos. F6 recebe um brief aprovado e produz um draftmarkdown.
      - SHA-256 do bloco: `f4f58583224283d5567f766fbb8b20207d0419d3d8cccddbeb455f753e04065a`
  - [SRC-S010 · L129–L173 · 4. Modo efetivo](#src-s010)
    - Caminho: 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes > 4. Modo efetivo
    - Assuntos: override, modo, config, case_dir, str, none, efetivo, def
    - Trecho-guia: Adicionar em forjan4validate.py uma resolução genérica preservando a fachada atual:
    - SHA-256 do bloco: `33f4af590d99a295a9c763d057573dd89e062a9b082dd85893fca6effaa20501`
  - [SRC-S011 · L174–L175 · 5. F2-B — extensão da árvore e consulta](#src-s011)
    - Caminho: 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes > 5. F2-B — extensão da árvore e consulta
    - Assuntos: f2-b, extensão, árvore, consulta
    - Trecho-guia: Documento de consulta sobre 5. F2-B — extensão da árvore e consulta.
    - SHA-256 do bloco: `8c41633bd34e14cff0d9f58223da2c1724aa6bb91e3df6b3b49bd7f762ab971b`
    - [SRC-S012 · L176–L185 · 5.1 Fonte canônica](#src-s012)
      - Caminho: 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes > 5. F2-B — extensão da árvore e consulta > 5.1 Fonte canônica
      - Assuntos: fonte, canônica, alterar, generate_n4_contracts, question_tree_schema, forja_exploracao_100, forja_reasoning, validate_question_tree
      - Trecho-guia: generaten4contracts.QUESTIONTREESCHEMA; forjaexploracao100.py; forjareasoning.validatequestiontree(); testforjaexploracao100.py; testforjan4.py.
      - SHA-256 do bloco: `ca3e63dbfade4c6f53a0f967e21cb5f24916f63cfa21e900fbc0f78d0b7cdb55`
    - [SRC-S013 · L186–L237 · 5.2 Estrutura aditiva](#src-s013)
      - Caminho: 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes > 5. F2-B — extensão da árvore e consulta > 5.2 Estrutura aditiva
      - Assuntos: json, null, estrutura, aditiva, not_applicable, q001, decisionledger, adicionar
      - Trecho-guia: Campos adicionais por pergunta selecionada:
      - SHA-256 do bloco: `b492a4d14c5c3f9fdf3a6485418fea1735dccff241c0a203fb8a50cfd1eebf0a`
    - [SRC-S014 · L238–L264 · 5.3 Seleção determinística](#src-s014)
      - Caminho: 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes > 5. F2-B — extensão da árvore e consulta > 5.3 Seleção determinística
      - Assuntos: seleção, determinística, pode, for, blocked, justificativa, existirem, impacto
      - Trecho-guia: Uma pergunta só pode entrar em selectedQuestionIds se:
      - SHA-256 do bloco: `6f2072f4515d081c8be7a797879a43b0eb36aced039a2556d841c7345864b50d`
    - [SRC-S015 · L265–L283 · 5.4 Gates](#src-s015)
      - Caminho: 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes > 5. F2-B — extensão da árvore e consulta > 5.4 Gates
      - Assuntos: gates, dialectic_questions_material, dialectic_questions_not_answered_in_record, silence_policy_safe, human_decisions_attributed, material_decisions_resolved_or_blocked, reason, codes
      - Trecho-guia: dialecticquestionsmaterial; dialecticquestionsnotansweredinrecord; silencepolicysafe; humandecisionsattributed; materialdecisionsresolvedorblocked.
      - SHA-256 do bloco: `882419c0fd55672624b799f87b9615f04b78f361c6dc15716b664330cb53e731`
    - [SRC-S016 · L284–L310 · 5.5 Renderização](#src-s016)
      - Caminho: 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes > 5. F2-B — extensão da árvore e consulta > 5.5 Renderização
      - Assuntos: json, não, renderização, resposta, adicionar, cli, existente, forja_exploracao_100
      - Trecho-guia: Adicionar ao CLI existente forjaexploracao100.py:
      - SHA-256 do bloco: `b776e8f641a97b567e0385e8eb6e8723bfd4fedef67777513cd2b10c0f1d82b5`
  - [SRC-S017 · L311–L312 · 6. F3-B — mapa do destinatário](#src-s017)
    - Caminho: 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes > 6. F3-B — mapa do destinatário
    - Assuntos: f3-b, mapa, destinatário
    - Trecho-guia: Documento de consulta sobre 6. F3-B — mapa do destinatário.
    - SHA-256 do bloco: `4eb7db113f590c86c510d8e0371b01c432fdff7e4867f7bea88c249272ed8591`
    - [SRC-S018 · L313–L326 · 6.1 Registro](#src-s018)
      - Caminho: 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes > 6. F3-B — mapa do destinatário > 6.1 Registro
      - Assuntos: registro, adicionar, recipient_map, forja_n4_common, artifact_specs, python, f3_mapa_destinatario, json
      - Trecho-guia: Adicionar a forjan4common.ARTIFACTSPECS:
      - SHA-256 do bloco: `2bfaa42993729dd1f3b2548414184f6f7fcd13fedc786ce79329cc3bf53684bd`
    - [SRC-S019 · L327–L375 · 6.2 Schema](#src-s019)
      - Caminho: 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes > 6. F3-B — mapa do destinatário > 6.2 Schema
      - Assuntos: confirmed, unknown, status, sourceids, null, not_applicable, schema, organ
      - Trecho-guia: positionId; nível: rapporteur, organ, samesectionotherorgan, section, specialcourt, plenary, other; issueId; decisionIds; status; asOf; summary; sourceIds.
      - SHA-256 do bloco: `f20e5e8b5bdfa8600340bbda35af59e475a8a331e6389a7f806b8bc063d88b07`
    - [SRC-S020 · L376–L401 · 6.3 Validador](#src-s020)
      - Caminho: 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes > 6. F3-B — mapa do destinatário > 6.3 Validador
      - Assuntos: validador, forja_reasoning, validators, adicionar, validate_recipient_map, registrá-lo, forja_n4_validate, cross_reference_findings
      - Trecho-guia: Adicionar validaterecipientmap() em forjareasoning.py e registrá-lo em:
      - SHA-256 do bloco: `45dd3d66ca56cb1a0a3b706886cc5874c3130938d13c6e2cd3360099d7afc1a7`
    - [SRC-S021 · L402–L407 · 6.4 Freshness](#src-s021)
      - Caminho: 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes > 6. F3-B — mapa do destinatário > 6.4 Freshness
      - Assuntos: freshness, validador, calcula, recipientmapfreshnesshours, não, confiar, status, confirmed
      - Trecho-guia: O validador calcula freshness com recipientMapFreshnessHours. Não confiar em status=confirmed autodeclarado. Em pilotblocking, composição stale vira P0 se a estratégia depender dela; caso contrário, P1 com uso proibido.
      - SHA-256 do bloco: `6cdcc3ceef6818a1df9870ae35f338b7a085969a5c5471ca046c156d22e44296`
  - [SRC-S022 · L408–L409 · 7. F4 — signature brief](#src-s022)
    - Caminho: 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes > 7. F4 — signature brief
    - Assuntos: signature, brief
    - Trecho-guia: Documento de consulta sobre 7. F4 — signature brief.
    - SHA-256 do bloco: `23e16bc8c14ea74339e615fdaab2f4a42179b6f442e7a8e12004f07e1cca96ec`
    - [SRC-S023 · L410–L423 · 7.1 Registro](#src-s023)
      - Caminho: 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes > 7. F4 — signature brief > 7.1 Registro
      - Assuntos: registro, adicionar, signature_brief, artifact_specs, python, f4_signature_brief, json, type
      - Trecho-guia: Adicionar signaturebrief aos outputs F4 N4.
      - SHA-256 do bloco: `53ae56e8b754e6a294971f637bf05241e3d39c9342645884476d30400947e686`
    - [SRC-S024 · L424–L452 · 7.2 Schema](#src-s024)
      - Caminho: 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes > 7. F4 — signature brief > 7.2 Schema
      - Assuntos: schema, json, protocolversion, forja-signature-brief-v1, decisivequestion, demonstratedconsequence, routes, routeid
      - Trecho-guia: Documento de consulta sobre 7.2 Schema.
      - SHA-256 do bloco: `13b812110c3979d4ed324860bc17a6c8886edd434b77c97d21a92673afe5d586`
    - [SRC-S025 · L453–L480 · 7.3 Validador](#src-s025)
      - Caminho: 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes > 7. F4 — signature brief > 7.3 Validador
      - Assuntos: rota, não, validador, exige, adicionar, validate_signature_brief, forja_reasoning, regras
      - Trecho-guia: Adicionar validatesignaturebrief() em forjareasoning.py.
      - SHA-256 do bloco: `a83cb56eed6531f7c5cdf80e3792b29bdd5873b2b43d42caaf2293bf82ddac04`
  - [SRC-S026 · L481–L482 · 8. F5 — trilha de pesquisa jurídica](#src-s026)
    - Caminho: 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes > 8. F5 — trilha de pesquisa jurídica
    - Assuntos: trilha, pesquisa, jurídica
    - Trecho-guia: Documento de consulta sobre 8. F5 — trilha de pesquisa jurídica.
    - SHA-256 do bloco: `5d7cbbbd857c4ca77e8a24cb8fbac309d67854fbbd488b54d015d2048a2975ff`
    - [SRC-S027 · L483–L519 · 8.1 Extensão do sourceledger](#src-s027)
      - Caminho: 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes > 8. F5 — trilha de pesquisa jurídica > 8.1 Extensão do sourceledger
      - Assuntos: extensão, não, bloco, searchruns, continua, sendo, liberação, sourceledger
      - Trecho-guia: Não criar novo artefato obrigatório. Adicionar bloco:
      - SHA-256 do bloco: `ca1336fa8d00fa8efab427e78fa64731ae6e96f0f2fd2a335ed81d067dde9885`
    - [SRC-S028 · L520–L539 · 8.2 Gates](#src-s028)
      - Caminho: 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes > 8. F5 — trilha de pesquisa jurídica > 8.2 Gates
      - Assuntos: gates, query, único, base, identificada, horário, filtros, presentes
      - Trecho-guia: query ID único; base identificada; horário e filtros presentes; resultados e descartes não sobrepostos; resultado negativo associado a query executada; replay existente quando declarado; ação TeiaJus permitida.
      - SHA-256 do bloco: `4e87564d217670cc3fd8bc5686d32f7d3c91131860c906d0107290718fc24f9c`
  - [SRC-S029 · L540–L541 · 9. F7 — precedente-âncora](#src-s029)
    - Caminho: 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes > 9. F7 — precedente-âncora
    - Assuntos: precedente-âncora
    - Trecho-guia: Documento de consulta sobre 9. F7 — precedente-âncora.
    - SHA-256 do bloco: `de123ac98186f1e7447c33af71d7f51cf43663756e0276fe33bc94209b89fa65`
    - [SRC-S030 · L542–L572 · 9.1 Extensão do verifiedsourceledger](#src-s030)
      - Caminho: 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes > 9. F7 — precedente-âncora > 9.1 Extensão do verifiedsourceledger
      - Assuntos: extensão, verifiedsourceledger, verified_source_ledger, entrada, marcada, anchor, true, deve
      - Trecho-guia: Entrada marcada anchor: true deve possuir:
      - SHA-256 do bloco: `bfd081ded00ab911a75ac5952eb0a80a83064735ef73fd7096654a7222545d85`
    - [SRC-S031 · L573–L601 · 9.2 Regras](#src-s031)
      - Caminho: 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes > 9. F7 — precedente-âncora > 9.2 Regras
      - Assuntos: regras, deve, rota, não, reason, routeid, ser, selecionada
      - Trecho-guia: routeId deve ser a rota selecionada ou uma rota explicitamente comparada; holding exige íntegra suficiente; ementa isolada produz fullTextStatus=insufficient; trecho e locator são hash-bound; elementComparison deve cobrir elementos declarados como determinantes; regime não recebe
      - SHA-256 do bloco: `ba4888ab6d3da827b6e1783cf311a444f6bea489fe13471e8be93f0394671630`
  - [SRC-S032 · L602–L603 · 10. TeiaJus](#src-s032)
    - Caminho: 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes > 10. TeiaJus
    - Assuntos: teiajus
    - Trecho-guia: Documento de consulta sobre 10. TeiaJus.
    - SHA-256 do bloco: `f0b4feb13861d9cb46d92ac802dde4853fbb543451b81204357c312f2fa377e7`
    - [SRC-S033 · L604–L620 · 10.1 Allowlist v1](#src-s033)
      - Caminho: 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes > 10. TeiaJus > 10.1 Allowlist v1
      - Assuntos: allowlist, adicionar, qualquer, atualizar, forja_search_config, json, somente, após
      - Trecho-guia: Atualizar FORJASEARCHCONFIG.json somente após teste de capabilities. Adicionar como leitura:
      - SHA-256 do bloco: `92527c68c67f36d922ce7c95ceaf55951b145d532d9497c50b144a5b58f6edae`
    - [SRC-S034 · L621–L630 · 10.2 CLI](#src-s034)
      - Caminho: 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes > 10. TeiaJus > 10.2 CLI
      - Assuntos: cli, capabilities, subcomando, genérico, execute, existe, primeira, versão
      - Trecho-guia: O subcomando genérico execute já existe. Na primeira versão, não criar aliases antes de provar uso recorrente. O TDD exige:
      - SHA-256 do bloco: `2bfee941f312c756f229d2b4e45b3e688e51c53fb964a2cf071d90f1c73821e5`
    - [SRC-S035 · L631–L648 · 10.3 Classificação de fonte](#src-s035)
      - Caminho: 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes > 10. TeiaJus > 10.3 Classificação de fonte
      - Assuntos: classificação, fonte, metadata_evidence, official_summary, official_full_text, administrative_data, cada, resultado
      - Trecho-guia: discoveryonly; metadataevidence; officialsummary; officialfulltext; administrativedata; administrativedecision.
      - SHA-256 do bloco: `ca059f69222ed01c0acb7c4cbe616ff42d9a6f6848d5bbfd2a98e62fcdc317bf`
  - [SRC-S036 · L649–L650 · 11. Identidade e AUTO-RESEARCH](#src-s036)
    - Caminho: 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes > 11. Identidade e AUTO-RESEARCH
    - Assuntos: identidade, auto-research
    - Trecho-guia: Documento de consulta sobre 11. Identidade e AUTO-RESEARCH.
    - SHA-256 do bloco: `afa89f3846dac444e589d752cdf3df501bead690c369012c014595c083d8e6ba`
    - [SRC-S037 · L651–L679 · 11.1 Manifest](#src-s037)
      - Caminho: 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes > 11. Identidade e AUTO-RESEARCH > 11.1 Manifest
      - Assuntos: manifest, criar, autoresearch, identity_corpus_manifest, jsonl, conteúdo, bruto, itemid
      - Trecho-guia: Criar autoresearch/IDENTITYCORPUSMANIFEST.jsonl, sem conteúdo bruto, com:
      - SHA-256 do bloco: `579247c07e71a006d9d35484a19c5bc5bcf9c3ae57aca3e4925100ce33660e64`
    - [SRC-S038 · L680–L696 · 11.2 Validação](#src-s038)
      - Caminho: 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes > 11. Identidade e AUTO-RESEARCH > 11.2 Validação
      - Assuntos: validação, não, exige, adicionar, forja_learning, validate_identity_corpus_entry, validate_identity_corpus_manifest, regras
      - Trecho-guia: validateidentitycorpusentry(); validateidentitycorpusmanifest().
      - SHA-256 do bloco: `755ae140b59b719f848feb5ab5349d3a642dcba63d487e2dbf0370c61e5469d4`
    - [SRC-S039 · L697–L709 · 11.3 Integração com AUTO-RESEARCH](#src-s039)
      - Caminho: 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes > 11. Identidade e AUTO-RESEARCH > 11.3 Integração com AUTO-RESEARCH
      - Assuntos: não, integração, auto-research, autorizados, corpus, identidade, altera, ar_corpus
      - Trecho-guia: O corpus de identidade não altera ARCORPUS.json. Ele é uma camada de metadados usada para:
      - SHA-256 do bloco: `b2a51d354b6632f8927564dcdacc75eab12469ab7d45b25390a7aa29c5947582`
  - [SRC-S040 · L710–L711 · 12. F6 e F7-B](#src-s040)
    - Caminho: 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes > 12. F6 e F7-B
    - Assuntos: f7-b
    - Trecho-guia: Documento de consulta sobre 12. F6 e F7-B.
    - SHA-256 do bloco: `f12f3f7524bfbc56250c7fdbef017e52c82995da76257f8c1f9bdbb502921380`
    - [SRC-S041 · L712–L722 · 12.1 Input de F6](#src-s041)
      - Caminho: 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes > 12. F6 e F7-B > 12.1 Input de F6
      - Assuntos: input, incumbente, sombra, continua, variante, experimental, recebe, f4_signature_brief
      - Trecho-guia: Em sombra, o incumbente continua. A variante experimental recebe:
      - SHA-256 do bloco: `f4a2de66df684dd307273c2b0301493ae1ed9d1869f6090e3cec88bb48680427`
    - [SRC-S042 · L723–L735 · 12.2 Recibo gostoJuridico v2](#src-s042)
      - Caminho: 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes > 12. F6 e F7-B > 12.2 Recibo gostoJuridico v2
      - Assuntos: recibo, gostojuridico, atualizar, forja_fable5, aceitar, forja-gosto-edge-v2, signaturebriefsha256, selectedrouteid
      - Trecho-guia: Atualizar forjafable5.py para aceitar FORJA-GOSTO-EDGE-v2:
      - SHA-256 do bloco: `853da95dbc37e527daa0895fc727a3e1313fa79ae7411e8b7e5f2dd230f28f58`
    - [SRC-S043 · L736–L762 · 12.3 Recomposição independente](#src-s043)
      - Caminho: 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes > 12. F6 e F7-B > 12.3 Recomposição independente
      - Assuntos: none, recomposição, independente, conferir, adicionar, assinatura, validate_editorial_bundle, parâmetros
      - Trecho-guia: Adicionar à assinatura de validateeditorialbundle() parâmetros opcionais:
      - SHA-256 do bloco: `a35803777941fc3f33e80088b1101f0d8f4132c281046e51adf0c5e019281f6a`
  - [SRC-S044 · L763–L788 · 13. Invalidação](#src-s044)
    - Caminho: 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes > 13. Invalidação
    - Assuntos: invalidação, brief, mapa, draft, anchor, hash, adicionar, arestas
    - Trecho-guia: Adicionar arestas ao mecanismo N4 de invalidação:
    - SHA-256 do bloco: `6fc6a8d8e0e91d5bc6fabd06df55795dc0907e5c5044f9994bcaae738bb4675b`
  - [SRC-S045 · L789–L790 · 14. Arquivos a alterar](#src-s045)
    - Caminho: 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes > 14. Arquivos a alterar
    - Assuntos: arquivos, alterar
    - Trecho-guia: Documento de consulta sobre 14. Arquivos a alterar.
    - SHA-256 do bloco: `586589810244d61012ba1c2298351396b54c8dc81675aa895c6ec282a8bca150`
    - [SRC-S046 · L791–L800 · Núcleo declarativo](#src-s046)
      - Caminho: 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes > 14. Arquivos a alterar > Núcleo declarativo
      - Assuntos: json, núcleo, declarativo, phase_contracts_n4, gerados, gerado, forja_n3_config, forja_n4_common
      - Trecho-guia: FORJAN3CONFIG.json; forjan4common.py; generaten4contracts.py; phasecontractsn4/F2.json a F7.json — gerados; phasecontractsn4/EXTENSIONS.json — gerado; n4schemas/ARTIFACTCATALOG.json — gerado; schemas novos e schema F2 — gerados.
      - SHA-256 do bloco: `3e33e760d2615a6bc0b25e9731e32c2cb89d5be4aa9fa0c4eb8d88230b3bda10`
    - [SRC-S047 · L801–L813 · Validadores e execução](#src-s047)
      - Caminho: 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes > 14. Arquivos a alterar > Validadores e execução
      - Assuntos: validadores, execução, forja_exploracao_100, forja_reasoning, forja_n4_validate, forja_package, forja_run, forja_fable5
      - Trecho-guia: forjaexploracao100.py; forjareasoning.py; forjan4validate.py; forjapackage.py; forjarun.py; forjafable5.py; forjaeditorialfidelity.py; forjalearning.py; forjan4invalidation.py; forjalegalsearch.py, apenas se a validação de action exigir mudança.
      - SHA-256 do bloco: `ac23b8f719236c602b847f73df85bfcbdc3c8e1dd18f556bb34af914ac0e1e32`
    - [SRC-S048 · L814–L819 · Configuração e templates](#src-s048)
      - Caminho: 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes > 14. Arquivos a alterar > Configuração e templates
      - Assuntos: templates, configuração, forja_search_config, json, f2_consulta_advogado, autoresearch, identity_corpus_manifest, jsonl
      - Trecho-guia: FORJASEARCHCONFIG.json; templates/F2CONSULTAADVOGADO.md; autoresearch/IDENTITYCORPUSMANIFEST.jsonl.
      - SHA-256 do bloco: `8501a30d276b3ff03c19faf29689ddfcb7344068f746cf5fae082dc3d37295d1`
    - [SRC-S049 · L820–L837 · Testes](#src-s049)
      - Caminho: 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes > 14. Arquivos a alterar > Testes
      - Assuntos: testes, novo, test_forja_assinatura_lite, test_forja_exploracao_100, test_forja_n4, test_forja_legal_search, test_forja_fable5, test_forja_run
      - Trecho-guia: novo testforjaassinaturalite.py; testforjaexploracao100.py; testforjan4.py; testforjalegalsearch.py; testforjafable5.py; testforjarun.py; testforjan3package.py; testforjaantihallucinationv2.py; testforjaanticheat.py; testforjaautoresearch.py; testforjaarchitecture.py.
      - SHA-256 do bloco: `5def002e7bb37f487387ddb591d82c4aaeec303598f3363e076b94153ca6ba6a`
  - [SRC-S050 · L838–L859 · 15. Matriz requisito → componente → teste](#src-s050)
    - Caminho: 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes > 15. Matriz requisito → componente → teste
    - Assuntos: requisito, componente, teste, matriz, principal, rf-01, resolver, modo
    - Trecho-guia: Documento de consulta sobre 15. Matriz requisito → componente → teste.
    - SHA-256 do bloco: `26d3bc53c5ec32c8b5a711cd538f4919cada7581df81ade2fe5ca42298f5aabc`
  - [SRC-S051 · L860–L861 · 16. Testes obrigatórios](#src-s051)
    - Caminho: 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes > 16. Testes obrigatórios
    - Assuntos: testes, obrigatórios
    - Trecho-guia: Documento de consulta sobre 16. Testes obrigatórios.
    - SHA-256 do bloco: `9c65d5626764c9e99daf558e791a6c0224ea47aaab5a93eb1d5b21ac596e4d4a`
    - [SRC-S052 · L862–L876 · 16.1 Unidade](#src-s052)
      - Caminho: 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes > 16. Testes obrigatórios > 16.1 Unidade
      - Assuntos: unidade, resolução, modo, seleção, ordenação, perguntas, política, silêncio
      - Trecho-guia: resolução de modo; seleção e ordenação de perguntas; política de silêncio; autoria da decisão; freshness; duplicidade de rotas; cross-reference; search trace; holding/locator/hash; classificação de fonte; manifest de identidade; recibo v2.
      - SHA-256 do bloco: `ab2a11dabcfc612da39383b6e6be49d941505d35989b11b4009929ff62763816`
    - [SRC-S053 · L877–L885 · 16.2 Contrato e migração](#src-s053)
      - Caminho: 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes > 16. Testes obrigatórios > 16.2 Contrato e migração
      - Assuntos: contrato, migração, sincronizados, artefatos, gerador, idempotente, catálogo, schemas
      - Trecho-guia: gerador idempotente; catálogo e schemas sincronizados; contratos N4 sincronizados; artefatos v1 legíveis; novos artefatos exigidos só no modo aplicável; chamadas antigas de validateeditorialbundle() válidas.
      - SHA-256 do bloco: `d610ca0e615c99d11989f9c03c59ddb82286708c50f49739b420080fa39b2e9c`
    - [SRC-S054 · L886–L895 · 16.3 Integração](#src-s054)
      - Caminho: 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes > 16. Testes obrigatórios > 16.3 Integração
      - Assuntos: brief, integração, f2-b, mapa, search, trace, anchor, inválida
      - Trecho-guia: F2-B → F4; mapa → brief; brief → search trace; anchor inválida → reabertura; brief → F6 variante; F7-B → package; TeiaJus artifact → source ledger.
      - SHA-256 do bloco: `b427f34274d4fe5abc4b2f17ed146e158ba431cb1dd63b7036220aae1c864fce`
    - [SRC-S055 · L896–L911 · 16.4 Adversariais](#src-s055)
      - Caminho: 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes > 16. Testes obrigatórios > 16.4 Adversariais
      - Assuntos: adversariais, apresentada, pergunta, respondida, enviada, fato, default, resposta
      - Trecho-guia: pergunta já respondida enviada; fato com default; resposta parcial marcada resolvida; officedeclaration usada como prova; composição stale apresentada como atual; DataJud apresentado como prevenção; ementa apresentada como ratio; anchor com locator falso; rota duplicada lexicalme
      - SHA-256 do bloco: `e5d485899725223d714b9b776a1417b2ec14f9a93af50de50c769d5364fc0c00`
    - [SRC-S056 · L912–L923 · 16.5 Metamórficos](#src-s056)
      - Caminho: 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes > 16. Testes obrigatórios > 16.5 Metamórficos
      - Assuntos: metamórficos, trocar, mudar, alterar, retirar, ordem, rotas, selecionado
      - Trecho-guia: trocar ordem das rotas sem mudar ID selecionado; renomear parte sem alterar relações; retirar decisão humana; retirar fonte da composição; alterar um termo do holding; trocar routeId no recibo; mudar hash do brief; converter transcript em peça escrita; remover query que sustenta 
      - SHA-256 do bloco: `851f20523b230b3386a57b0dc0ec76301044215a081dfb8de6ecf734a85c2da1`
    - [SRC-S057 · L924–L943 · 16.6 Regressão](#src-s057)
      - Caminho: 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes > 16. Testes obrigatórios > 16.6 Regressão
      - Assuntos: regressão, baseline, passed, dirigido, powershell, python, pytest, cacheprovider
      - Trecho-guia: Baseline observado antes da implementação: 104 passed, 3 subtests passed.
      - SHA-256 do bloco: `093696cc3be0a8e9456a9a65bf9d37fa9731dbbaaaeb0f78ba79b6cb1a76990d`
  - [SRC-S058 · L944–L978 · 17. Comandos de verificação por mudança](#src-s058)
    - Caminho: 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes > 17. Comandos de verificação por mudança
    - Assuntos: python, mudança, comandos, verificação, powershell, json, users, igorpc
    - Trecho-guia: Depois de mudança estrutural relevante:
    - SHA-256 do bloco: `970fcda129b13fba7503219dd4989dd66dd97c1ae94a6037e15a411e7e2f45b9`
  - [SRC-S059 · L979–L1001 · 18. Critério técnico de concluído](#src-s059)
    - Caminho: 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes > 18. Critério técnico de concluído
    - Assuntos: não, têm, critério, técnico, concluído, decisão, autoria, brief
    - Trecho-guia: 1. modos e pilotCases têm namespace próprio; 2. artefatos novos estão no catálogo, schemas e contratos gerados; 3. F2-B não pergunta o que o acervo responde; 4. silêncio material não cria fato; 5. resposta e decisão têm autoria e proveniência; 6. mapa não trata metadado como prov
    - SHA-256 do bloco: `fa27a76423d207d8b2fc45222fa67ec0901057977fb09dc67736f4cd096f3e22`

## Conteúdo integral indexado

Os marcadores HTML abaixo são apenas âncoras de navegação. O texto reproduz integralmente a origem normalizada em UTF-8; somente destinos de links relativos podem ter sido recalculados para apontar ao mesmo arquivo a partir desta pasta.

<a id="src-s001"></a>

# 34 — TDD: FORJA-ASSINATURA Lite, cocrição e precedentes

> **EMENDAS NORMATIVAS — 25/07/2026.** Este documento vale **acrescido da seção 9 de `36_CONSOLIDACAO_CONSELHO_E_PARECER_FINAL.md`** (emendas E1 a E16: conselho Helena e Cícero, migração do modelo editorial Fable 5 para Opus 5 com revisão cruzada entre famílias, perímetro de sigilo, testes negativos, registro de escopo e Onda -1). Em conflito, prevalece a seção 9. Os `ANEXO_A/B/C` são histórico e não se executam.


**Versão:** 1.0  
**Data:** 25/07/2026  
**Estado:** desenho técnico consolidado para implementação  
**PRD:** `planejamento/33_PRD_FORJA_ASSINATURA_LITE_COCRIACAO_PRECEDENTES.md`  
**Roadmap:** `planejamento/35_ROADMAP_EXECUCAO_FORJA_ASSINATURA_LITE.md`  
**Arquitetura:** `planejamento/32_PLANO_UNICO_CONSOLIDADO_V2_2026-07-25.md`

Este TDD substitui o documento 28 como desenho imediato. A arquitetura N-way do TDD 28 permanece fora da v1.

---


<a id="src-s002"></a>

## 1. Objetivo técnico

Estender a esteira F2–F7 sem criar nova fase canônica:

```text
F2-A question tree
  └─ F2-B seleção dialética + consulta + decisões
       ├─ F3-B mapa do destinatário
       └─ F4 signature brief
            └─ F5 trilha jurídica + verificação de âncoras
                 └─ F6 um draft
                      └─ F7/F7-B recomposição e preservação
```

Novos tipos de artefato N4:

- `F3_MAPA_DESTINATARIO.json`;
- `F4_SIGNATURE_BRIEF.json`.

Extensões:

- `F2_QUESTION_TREE.json`;
- `source_ledger`;
- `verified_source_ledger`;
- recibo `gostoJuridico`.

Ativo offline:

- `autoresearch/IDENTITY_CORPUS_MANIFEST.jsonl`.


<a id="src-s003"></a>

## 2. Restrições observadas no sistema vivo

1. F0–F10 são resolvidas por `forja_phase_contracts.py`.
2. Schemas e contratos N4 são gerados por `generate_n4_contracts.py`.
3. `forja_n4_common.ARTIFACT_SPECS` é fonte do catálogo gerado.
4. `generate_n4_contracts.EXTENSIONS` é fonte dos outputs e gates N4.
5. `forja_n4_validate.VALIDATORS` e `_schema_findings()` validam o catálogo.
6. `forja_reasoning.validate_question_tree()` já delega F2-A para `forja_exploracao_100`.
7. F2-A já bloqueia questão material não respondida e exige `supportIds` em respostas factuais.
8. `forja_run.py` recompõe o `verified_source_ledger` e o bundle F7-B durante promoção.
9. `forja_package.validate_source_ledger()` é fachada pública de liberação das fontes.
10. `forja_editorial_fidelity.validate_editorial_bundle()` não recompõe hoje o recibo `gostoJuridico`.
11. `FORJA_SEARCH_CONFIG.json` permite menos ações que o agente TeiaJus anuncia.
12. `forja_n4_validate._effective_mode()` resolve apenas o namespace global `n4`.
13. `FORJA_N3_CONFIG.json` já possui casos N4 em `pilot_blocking`; a feature nova não pode herdar esse estado implicitamente.
14. F8 continua consumindo um único `final_markdown`.
15. O baseline dirigido em 25/07/2026 passou: `104 passed, 3 subtests passed`.

---


<a id="src-s004"></a>

## 3. Decisões arquiteturais


<a id="src-s005"></a>

### DA-01 — Sem nova fase

F2-B e F3-B são subestágios observáveis. A tupla F0–F10 permanece.


<a id="src-s006"></a>

### DA-02 — Namespace de feature próprio

Adicionar a `FORJA_N3_CONFIG.json`:

```json
{
  "forjaAssinaturaLite": {
    "schemaVersion": 1,
    "mode": "off",
    "pilotCases": [],
    "consultationOutboundPolicy": "manual_review_only",
    "recipientMapFreshnessHours": 24,
    "allowPaidResearch": false
  }
}
```

Valores de `mode`: `off`, `shadow`, `pilot_blocking`.

Não reutilizar diretamente `n4.mode`, pois ele já possui pilotos vivos.


<a id="src-s007"></a>

### DA-03 — Compatibilidade por protocolo

O envelope N4 continua `schemaVersion: 1`. A evolução aditiva será marcada por protocolos específicos:

- `FORJA-F2B-DIALECTIC-v1`;
- `FORJA-RECIPIENT-MAP-v1`;
- `FORJA-SIGNATURE-BRIEF-v1`;
- `FORJA-LEGAL-SEARCH-TRACE-v1`;
- `FORJA-PRECEDENT-ANCHOR-v1`;
- `FORJA-GOSTO-EDGE-v2`.

Artefatos históricos permanecem legíveis. O modo bloqueante exige os protocolos novos somente para casos elegíveis.


<a id="src-s008"></a>

### DA-04 — Schemas gerados, não editados isoladamente

Alterar primeiro:

- `forja_n4_common.py`;
- `generate_n4_contracts.py`.

Depois executar o gerador e revisar o diff de:

- `n4_schemas/ARTIFACT_CATALOG.json`;
- schemas individuais;
- `phase_contracts_n4/F*.json`;
- `phase_contracts_n4/EXTENSIONS.json`.

Edição manual apenas dos arquivos gerados é proibida.


<a id="src-s009"></a>

### DA-05 — Um draft

Não alterar `phase_contracts/F6.json` para múltiplos candidatos. F6 recebe um brief aprovado e produz um `draft_markdown`.

---


<a id="src-s010"></a>

## 4. Modo efetivo

Adicionar em `forja_n4_validate.py` uma resolução genérica preservando a fachada atual:

```python
def _effective_named_mode(
    config: dict,
    case_dir: Path,
    namespace: str,
    override: str | None = None,
) -> tuple[str, str]:
    ...

def _effective_mode(config, case_dir, override=None):
    return _effective_named_mode(config, case_dir, "n4", override)

def effective_signature_lite_mode(config, case_dir, override=None):
    return _effective_named_mode(
        config, case_dir, "forjaAssinaturaLite", override
    )
```

Regras:

- modo desconhecido: erro;
- `off`: não materializa nem exige artefato;
- `shadow`: materializa e reporta, sem bloquear saída canônica;
- `pilot_blocking`: bloqueia somente `pilotCases`; fora deles, `shadow`;
- override é auditável;
- ausência de namespace equivale a `off`.

`validate_case()` deve resolver também o modo da feature e acrescentar
`F3_MAPA_DESTINATARIO.json` e `F4_SIGNATURE_BRIEF.json` ao conjunto requerido
somente quando o modo efetivo da feature não for `off`. Não adicionar esses
arquivos a `FLAG_FILES` sob um booleano concorrente: o namespace
`forjaAssinaturaLite.mode` é a fonte única de ativação.

Reason codes:

- `FAL-MODE-UNKNOWN`;
- `FAL-PILOT-IDENTITY-MISSING`;
- `FAL-OVERRIDE-RECORDED`.

---


<a id="src-s011"></a>

## 5. F2-B — extensão da árvore e consulta


<a id="src-s012"></a>

### 5.1 Fonte canônica

Alterar:

- `generate_n4_contracts.QUESTION_TREE_SCHEMA`;
- `forja_exploracao_100.py`;
- `forja_reasoning.validate_question_tree()`;
- `test_forja_exploracao_100.py`;
- `test_forja_n4.py`.


<a id="src-s013"></a>

### 5.2 Estrutura aditiva

Adicionar ao `F2_QUESTION_TREE.json`:

```json
{
  "dialecticProtocolVersion": "FORJA-F2B-DIALECTIC-v1",
  "dialecticConsultation": {
    "status": "not_selected|draft|awaiting_review|sent|partially_answered|answered|blocked|not_applicable",
    "selectedQuestionIds": ["Q001"],
    "renderedBodySha256": null,
    "outboundPolicy": "manual_review_only",
    "outboundReceiptId": null,
    "responseRefs": [],
    "round": 1
  },
  "decisionLedger": []
}
```

Campos adicionais por pergunta selecionada:

```json
{
  "questionType": "fact|evidence|authorization|objective|strategy|presentation",
  "selectionReason": "...",
  "alreadyResearched": ["source-id"],
  "humanAuthority": "responsible_lawyer|client|office|titular",
  "silencePolicy": "block_dependent|keep_options_open|explicit_reversible_default|not_applicable",
  "silenceConsequence": "...",
  "defaultValue": null
}
```

Entrada de `decisionLedger`:

```json
{
  "decisionId": "DEC-...",
  "questionIds": ["Q001"],
  "responseRef": "message-or-meeting-id",
  "responseAuthor": "...",
  "channel": "email|whatsapp|audio|meeting|other",
  "epistemicStatus": "office_declaration|confirmed_document|confirmed_official_source|legal_inference|strategic_hypothesis|not_verified",
  "decision": "...",
  "affectedArtifactIds": ["F4_SIGNATURE_BRIEF.json"],
  "remainingOpenIssues": [],
  "decidedAt": "...",
  "approvedBy": "..."
}
```


<a id="src-s014"></a>

### 5.3 Seleção determinística

Uma pergunta só pode entrar em `selectedQuestionIds` se:

- status atual for `blocked`;
- materialidade for `decisive` ou `material`, salvo justificativa;
- `caseAnchor` e `whyItMatters` existirem;
- nenhuma fonte registrada já a responder;
- `silencePolicy` e `humanAuthority` existirem.

O seletor deve ordenar por:

1. impacto sobre identidade do produto;
2. risco factual ou de autorização;
3. impacto sobre rota;
4. dependências downstream;
5. ID como desempate determinístico.

Não impor truncamento em 12. Acima de 12, emitir `FAL-F2B-QUESTION-VOLUME` P1 e exigir justificativa de rodada.

Os estados canônicos das perguntas continuam `answered`, `blocked` e
`not_applicable`. As ramificações legadas de
`forja_reasoning.validate_question_tree()` para `retired` e
`accepted_by_human`, hoje não admitidas pelo schema F2-A, devem ser removidas
ou explicitamente versionadas. Nenhum produtor novo pode emitir estado que o
schema gerado rejeite.


<a id="src-s015"></a>

### 5.4 Gates

- `dialectic_questions_material`;
- `dialectic_questions_not_answered_in_record`;
- `silence_policy_safe`;
- `human_decisions_attributed`;
- `material_decisions_resolved_or_blocked`.

Reason codes mínimos:

- `FAL-F2B-REDUNDANT`;
- `FAL-F2B-NO-MATERIALITY`;
- `FAL-F2B-NO-SILENCE-POLICY`;
- `FAL-F2B-FACT-DEFAULT`;
- `FAL-F2B-PARTIAL-CLOSED`;
- `FAL-F2B-DECISION-NO-AUTHOR`;
- `FAL-F2B-OFFICE-AS-FACT`;
- `FAL-F2B-OUTBOUND-UNAUTHORIZED`.


<a id="src-s016"></a>

### 5.5 Renderização

Adicionar ao CLI existente `forja_exploracao_100.py`:

- `render-consultation <json> --output <md>`;
- `record-response <json> --response <json>`.

Template:

- `templates/F2_CONSULTA_ADVOGADO.md`.

O renderizador:

- não altera respostas;
- inclui apenas perguntas selecionadas;
- grava hash no artefato;
- recusa render se houver pergunta sem consequência;
- não envia mensagem.

O gravador de resposta:

- é append-only para decisões;
- não converte automaticamente `office_declaration` em suporte factual;
- mantém questão aberta quando a resposta for parcial.

---


<a id="src-s017"></a>

## 6. F3-B — mapa do destinatário


<a id="src-s018"></a>

### 6.1 Registro

Adicionar a `forja_n4_common.ARTIFACT_SPECS`:

```python
"F3_MAPA_DESTINATARIO.json": {
    "type": "recipient_map",
    "phase": "F3_FONTES_REGIMENTO_LEIS",
    "keys": ["recipient", "competence", "prevention", "composition", "positions"]
}
```

Adicionar `recipient_map` aos outputs F3 de `generate_n4_contracts.EXTENSIONS`.


<a id="src-s019"></a>

### 6.2 Schema

Campos:

```json
{
  "protocolVersion": "FORJA-RECIPIENT-MAP-v1",
  "recipient": {
    "court": "...",
    "organ": "...",
    "rapporteur": "...",
    "identityStatus": "confirmed|unknown"
  },
  "competence": {
    "status": "confirmed|unknown|not_applicable",
    "basis": "...",
    "sourceIds": []
  },
  "prevention": {
    "status": "confirmed|unknown|not_applicable",
    "originCaseId": null,
    "basis": null,
    "sourceIds": []
  },
  "composition": {
    "status": "confirmed|stale|unknown|not_applicable",
    "members": [],
    "checkedAt": null,
    "validUntil": null,
    "sourceIds": []
  },
  "positions": [],
  "divergences": [],
  "appellateRoute": {},
  "limitations": []
}
```

Cada posição:

- `positionId`;
- nível: `rapporteur`, `organ`, `same_section_other_organ`, `section`, `special_court`, `plenary`, `other`;
- `issueId`;
- `decisionIds`;
- `status`;
- `asOf`;
- `summary`;
- `sourceIds`.


<a id="src-s020"></a>

### 6.3 Validador

Adicionar `validate_recipient_map()` em `forja_reasoning.py` e registrá-lo em:

- `forja_reasoning.VALIDATORS`;
- `forja_n4_validate.VALIDATORS`;
- `_cross_reference_findings()`.

Gates:

- `recipient_identity_sourced`;
- `competence_sourced_or_unknown`;
- `prevention_sourced_or_unknown`;
- `composition_current_or_unknown`;
- `positions_reference_sources`;
- `topology_scope_justified`.

Falhas:

- `FAL-F3-RECIPIENT-UNSOURCED`;
- `FAL-F3-PREVENTION-DATAJUD-ONLY`;
- `FAL-F3-COMPOSITION-STALE`;
- `FAL-F3-COMPOSITION-NO-OFFICIAL-SOURCE`;
- `FAL-F3-POSITION-NO-DECISION`;
- `FAL-F3-TOPOLOGY-UNJUSTIFIED`.


<a id="src-s021"></a>

### 6.4 Freshness

O validador calcula freshness com `recipientMapFreshnessHours`. Não confiar em `status=confirmed` autodeclarado. Em `pilot_blocking`, composição stale vira P0 se a estratégia depender dela; caso contrário, P1 com uso proibido.

---


<a id="src-s022"></a>

## 7. F4 — signature brief


<a id="src-s023"></a>

### 7.1 Registro

Adicionar a `ARTIFACT_SPECS`:

```python
"F4_SIGNATURE_BRIEF.json": {
    "type": "signature_brief",
    "phase": "F4_BLUEPRINT_ESTRATEGICO",
    "keys": ["decisiveQuestion", "routes", "selectedRouteId", "mandatoryContent"]
}
```

Adicionar `signature_brief` aos outputs F4 N4.


<a id="src-s024"></a>

### 7.2 Schema

```json
{
  "protocolVersion": "FORJA-SIGNATURE-BRIEF-v1",
  "decisiveQuestion": "...",
  "demonstratedConsequence": "...",
  "routes": [
    {
      "routeId": "R1",
      "thesisIds": [],
      "description": "...",
      "anchorCandidateIds": [],
      "bestObjection": "...",
      "response": "...",
      "decision": "selected|rejected|open",
      "decisionReason": "..."
    }
  ],
  "selectedRouteId": "R1",
  "humanDecisionId": "DEC-...",
  "motherSentence": "...",
  "decisiveFactIds": [],
  "decisiveDocumentIds": [],
  "mandatoryContent": [],
  "blockingIssues": []
}
```


<a id="src-s025"></a>

### 7.3 Validador

Adicionar `validate_signature_brief()` em `forja_reasoning.py`.

Regras:

- IDs referenciam `F2_QUESTION_TREE`, `F3_REASONING_GRAPH`, `F4_THESIS_MATURITY`, `source_ledger` ou mapa;
- exatamente uma rota `selected` quando não houver bloqueio;
- `selectedRouteId` coincide com a rota;
- rota material possui `humanDecisionId`;
- uma rota exige `singleRouteReason`;
- mais de quatro exige `complexityReason`;
- rotas não podem ter mesmo conjunto de teses, âncoras e objeção;
- âncora não verificada é candidata, nunca final;
- `blockingIssues` impede `draftRelease`.

Reason codes:

- `FAL-F4-NO-DECISIVE-QUESTION`;
- `FAL-F4-ROUTE-DUPLICATE`;
- `FAL-F4-ROUTE-ARTIFICIAL`;
- `FAL-F4-SELECTION-MISMATCH`;
- `FAL-F4-SELECTION-NO-HUMAN-DECISION`;
- `FAL-F4-ANCHOR-DANGLING`;
- `FAL-F4-BLOCKED-RELEASE`.

---


<a id="src-s026"></a>

## 8. F5 — trilha de pesquisa jurídica


<a id="src-s027"></a>

### 8.1 Extensão do `source_ledger`

Não criar novo artefato obrigatório. Adicionar bloco:

```json
{
  "legalResearchProtocol": "FORJA-LEGAL-SEARCH-TRACE-v1",
  "searchRuns": [
    {
      "queryId": "QRY-...",
      "database": "...",
      "endpointOrTool": "...",
      "executedAt": "...",
      "query": "...",
      "filters": {},
      "resultIds": [],
      "discarded": [{"resultId": "...", "reason": "..."}],
      "negativeResult": false,
      "notSearched": [],
      "replayRef": "...",
      "limitations": []
    }
  ]
}
```

Os ledgers reais existem em mais de uma forma histórica (`entries`, `sources`
ou lista direta). O bloco `searchRuns` é top-level e aditivo; a implementação
não deve reformatar entradas antigas. `_ledger_entries()` continua sendo a
normalização canônica para a liberação.

Atualizar produtores F5 e validar em uma função pública nova:

- `forja_package.validate_legal_research_trace(payload, mode)`.

`validate_source_ledger()` continua sendo a fachada de liberação e passa a incluir o resultado dessa validação.


<a id="src-s028"></a>

### 8.2 Gates

- query ID único;
- base identificada;
- horário e filtros presentes;
- resultados e descartes não sobrepostos;
- resultado negativo associado a query executada;
- replay existente quando declarado;
- ação TeiaJus permitida.

Reason codes:

- `FAL-F5-QUERY-INCOMPLETE`;
- `FAL-F5-RESULT-DISCARD-OVERLAP`;
- `FAL-F5-NEGATIVE-NO-QUERY`;
- `FAL-F5-REPLAY-MISSING`;
- `FAL-F5-PAID-ACTION-DENIED`.

---


<a id="src-s029"></a>

## 9. F7 — precedente-âncora


<a id="src-s030"></a>

### 9.1 Extensão do `verified_source_ledger`

Entrada marcada `anchor: true` deve possuir:

```json
{
  "anchorProtocol": "FORJA-PRECEDENT-ANCHOR-v1",
  "anchorId": "ANC-...",
  "routeId": "R1",
  "fullTextStatus": "verified|insufficient|not_applicable",
  "holding": {
    "text": "...",
    "locator": "...",
    "excerptSha256": "..."
  },
  "confusableObiter": [],
  "decisiveFacts": [],
  "elementComparison": [],
  "operation": "apply|distinguish|limit_scope|argue_overruling",
  "regime": {
    "legalBasis": [],
    "authorityType": "...",
    "dutyOrEffect": "...",
    "competentBody": "...",
    "changePath": "...",
    "validityStatus": "...",
    "checkedAt": "..."
  }
}
```


<a id="src-s031"></a>

### 9.2 Regras

- `routeId` deve ser a rota selecionada ou uma rota explicitamente comparada;
- `holding` exige íntegra suficiente;
- ementa isolada produz `fullTextStatus=insufficient`;
- trecho e locator são hash-bound;
- `elementComparison` deve cobrir elementos declarados como determinantes;
- regime não recebe score universal;
- autoridade antiga ou monocrática não é rebaixada automaticamente;
- âncora inválida retorna reason code de reabertura F4.

Atualizar:

- `forja_package.validate_source_ledger()`;
- `forja_run._validate_f7_source_ledger()`;
- `forja_claim_binding.py`, se o binding de parágrafo precisar conhecer `anchorId`;
- testes anti-alucinação e anti-cheat.

Reason codes:

- `FAL-F7-ANCHOR-NO-FULL-TEXT`;
- `FAL-F7-HOLDING-NO-LOCATOR`;
- `FAL-F7-HOLDING-HASH-MISMATCH`;
- `FAL-F7-FACT-FRAME-INCOMPLETE`;
- `FAL-F7-REGIME-INCOMPLETE`;
- `FAL-F7-ANCHOR-INVALIDATES-ROUTE`.

---


<a id="src-s032"></a>

## 10. TeiaJus


<a id="src-s033"></a>

### 10.1 Allowlist v1

Atualizar `FORJA_SEARCH_CONFIG.json` somente após teste de capabilities. Adicionar como leitura:

- `research_sources`;
- `research_plan`;
- `research_search`;
- `research_mission_get`.

Não adicionar:

- `research_mission`;
- `captcha_solve`;
- `apify_contact_enrich`;
- qualquer ação `read_paid`;
- qualquer mutação sem flag explícita.


<a id="src-s034"></a>

### 10.2 CLI

O subcomando genérico `execute` já existe. Na primeira versão, não criar aliases antes de provar uso recorrente. O TDD exige:

- validação de parâmetros por ação permitida;
- captura em `artifact_dir`;
- telemetria sanitizada;
- registro do action mode retornado por capabilities;
- recusa se capabilities divergir da política local.


<a id="src-s035"></a>

### 10.3 Classificação de fonte

Cada resultado recebe:

- `discovery_only`;
- `metadata_evidence`;
- `official_summary`;
- `official_full_text`;
- `administrative_data`;
- `administrative_decision`.

DataJud: no máximo `metadata_evidence`.  
Espelho/ementa STJ: `official_summary`.  
Texto diário com hash: candidato a `official_full_text`, sujeito aos gates.  
CGU CEIS/CNEP/CEAF/CEPIM/leniência: `administrative_data`.

---


<a id="src-s036"></a>

## 11. Identidade e AUTO-RESEARCH


<a id="src-s037"></a>

### 11.1 Manifest

Criar `autoresearch/IDENTITY_CORPUS_MANIFEST.jsonl`, sem conteúdo bruto, com:

- `itemId`;
- `path` ou referência controlada;
- `sha256`;
- `documentType`;
- `date`;
- `declaredAuthor`;
- `fabioRole`;
- `attributionConfidence`;
- `sourceChannel`;
- `versionRole`;
- `relatedItemIds`;
- `permittedUse`;
- `contentClass`;
- `reviewedBy`;
- `reviewedAt`.

Enums devem reutilizar, quando compatível:

- `CONTENT_CLASSES`;
- `CONTRIBUTION_ORIGINS`;
- `CONFIDENCE`;
- `CONTRIBUTION_STATUS`;

de `forja_learning.py`.


<a id="src-s038"></a>

### 11.2 Validação

Adicionar a `forja_learning.py`:

- `validate_identity_corpus_entry()`;
- `validate_identity_corpus_manifest()`.

Regras:

- hash obrigatório;
- arquivo ou referência existe;
- autoria desconhecida não recebe `human_authored`;
- transcript usa `permittedUse=thought_oral`;
- diff exige origem de cada mudança antes de promover preferência;
- conteúdo privado não é copiado para relatórios;
- regra global exige aprovação e duas evidências independentes, preservando disciplina atual.


<a id="src-s039"></a>

### 11.3 Integração com AUTO-RESEARCH

O corpus de identidade não altera `AR_CORPUS.json`. Ele é uma camada de metadados usada para:

- selecionar exemplos autorizados;
- estratificar avaliações;
- explicar proveniência;
- medir aceitação e reescrita.

F6 não lê itens `unknown` ou não autorizados. Nenhuma memória de caso é exposta por similaridade sem política.

---


<a id="src-s040"></a>

## 12. F6 e F7-B


<a id="src-s041"></a>

### 12.1 Input de F6

Em sombra, o incumbente continua. A variante experimental recebe:

- `F4_SIGNATURE_BRIEF.json`;
- anchors F5 verificadas;
- padrões de identidade autorizados;
- mesmos fatos, proposições e fontes do incumbente.

O Python não seleciona automaticamente um novo texto de produção na Onda 2. O AUTO-RESEARCH pareado compara outputs offline.


<a id="src-s042"></a>

### 12.2 Recibo `gostoJuridico` v2

Atualizar `forja_fable5.py` para aceitar `FORJA-GOSTO-EDGE-v2`:

- `signatureBriefSha256`;
- `selectedRouteId`;
- rotas consideradas em faixa flexível;
- âncoras por ID;
- consequência;
- protocolo anterior aceito em casos legados.

Remover o gate fixo de “três direções” para v2. Manter v1 legível.


<a id="src-s043"></a>

### 12.3 Recomposição independente

Adicionar à assinatura de `validate_editorial_bundle()` parâmetros opcionais:

```python
signature_brief_path: Path | None = None
```

Quando presente:

- recomputar hash do brief;
- conferir `selectedRouteId`;
- conferir âncoras e conteúdo obrigatório;
- validar recibo v2 sem confiar no relatório do modelo.

Preservar chamadas existentes por default `None`.

Atualizar consumidores:

- `forja_run._validate_fable5_editorial()`;
- `forja_package.py`;
- `test_forja_fable5.py`;
- `test_forja_run.py`;
- `test_forja_n3_package.py`.

---


<a id="src-s044"></a>

## 13. Invalidação

Adicionar arestas ao mecanismo N4 de invalidação:

| Mudança | Invalida |
|---|---|
| resposta/decisão F2-B | mapa ou brief que a referenciam |
| competência, prevenção ou composição | mapa e brief |
| `selectedRouteId` | pesquisa de âncoras, draft e F7 |
| anchor/full text/hash | brief selecionado e draft |
| padrão de identidade promovido | apenas variante editorial e avaliações |
| fonte ou trecho | ledger, anchor, parágrafo e package |

Invalidação é append-only e registra:

- artefato raiz;
- hash anterior e novo;
- dependentes;
- reason code;
- ação exigida;
- ator e horário.

Não apagar artefatos stale.

---


<a id="src-s045"></a>

## 14. Arquivos a alterar


<a id="src-s046"></a>

### Núcleo declarativo

- `FORJA_N3_CONFIG.json`;
- `forja_n4_common.py`;
- `generate_n4_contracts.py`;
- `phase_contracts_n4/F2.json` a `F7.json` — gerados;
- `phase_contracts_n4/EXTENSIONS.json` — gerado;
- `n4_schemas/ARTIFACT_CATALOG.json` — gerado;
- schemas novos e schema F2 — gerados.


<a id="src-s047"></a>

### Validadores e execução

- `forja_exploracao_100.py`;
- `forja_reasoning.py`;
- `forja_n4_validate.py`;
- `forja_package.py`;
- `forja_run.py`;
- `forja_fable5.py`;
- `forja_editorial_fidelity.py`;
- `forja_learning.py`;
- `forja_n4_invalidation.py`;
- `forja_legal_search.py`, apenas se a validação de action exigir mudança.


<a id="src-s048"></a>

### Configuração e templates

- `FORJA_SEARCH_CONFIG.json`;
- `templates/F2_CONSULTA_ADVOGADO.md`;
- `autoresearch/IDENTITY_CORPUS_MANIFEST.jsonl`.


<a id="src-s049"></a>

### Testes

- novo `test_forja_assinatura_lite.py`;
- `test_forja_exploracao_100.py`;
- `test_forja_n4.py`;
- `test_forja_legal_search.py`;
- `test_forja_fable5.py`;
- `test_forja_run.py`;
- `test_forja_n3_package.py`;
- `test_forja_anti_hallucination_v2.py`;
- `test_forja_anti_cheat.py`;
- `test_forja_autoresearch.py`;
- `test_forja_architecture.py`.

Não criar pacote `forja/signature/` nem CLI própria.

---


<a id="src-s050"></a>

## 15. Matriz requisito → componente → teste

| Requisito | Componente | Teste principal |
|---|---|---|
| RF-01 | resolver modo | `test_mode_off_shadow_pilot_cases` |
| RF-02, RF-03 | F2-B | `test_material_selection_and_silence_policy` |
| RF-04, RF-05 | render/ledger | `test_consultation_hash_and_partial_response` |
| RF-06 | outbound | `test_outbound_without_receipt_is_denied` |
| RF-07, RF-08 | recipient map | `test_datajud_cannot_confirm_composition_or_prevention` |
| RF-09, RF-10 | brief | `test_route_selection_and_non_artificiality` |
| RF-11 | search trace | `test_query_replay_negative_and_discarded_results` |
| RF-12 | anchor | `test_anchor_requires_full_text_holding_locator` |
| RF-13 | TeiaJus | `test_paid_and_non_allowlisted_actions_denied` |
| RF-14 | admin source | `test_cgu_registry_not_administrative_precedent` |
| RF-15, RF-16 | identity | `test_identity_attribution_and_permitted_use` |
| RF-17 | F6/F7-B | `test_single_draft_and_signature_recomposition` |
| RF-18 | invalidation | `test_anchor_change_reopens_brief_and_draft` |
| RF-19 | migration | `test_legacy_artifacts_remain_valid` |
| RF-20 | telemetry | `test_mode_hash_query_and_decision_are_recorded` |

---


<a id="src-s051"></a>

## 16. Testes obrigatórios


<a id="src-s052"></a>

### 16.1 Unidade

- resolução de modo;
- seleção e ordenação de perguntas;
- política de silêncio;
- autoria da decisão;
- freshness;
- duplicidade de rotas;
- cross-reference;
- search trace;
- holding/locator/hash;
- classificação de fonte;
- manifest de identidade;
- recibo v2.


<a id="src-s053"></a>

### 16.2 Contrato e migração

- gerador idempotente;
- catálogo e schemas sincronizados;
- contratos N4 sincronizados;
- artefatos v1 legíveis;
- novos artefatos exigidos só no modo aplicável;
- chamadas antigas de `validate_editorial_bundle()` válidas.


<a id="src-s054"></a>

### 16.3 Integração

- F2-B → F4;
- mapa → brief;
- brief → search trace;
- anchor inválida → reabertura;
- brief → F6 variante;
- F7-B → package;
- TeiaJus artifact → source ledger.


<a id="src-s055"></a>

### 16.4 Adversariais

- pergunta já respondida enviada;
- fato com default;
- resposta parcial marcada resolvida;
- `office_declaration` usada como prova;
- composição stale apresentada como atual;
- DataJud apresentado como prevenção;
- ementa apresentada como ratio;
- anchor com locator falso;
- rota duplicada lexicalmente;
- ação TeiaJus paga disfarçada de leitura;
- diff sem autoria atribuído a Fábio;
- recibo `gostoJuridico` adulterado;
- `approved=true` sem recomputação.


<a id="src-s056"></a>

### 16.5 Metamórficos

- trocar ordem das rotas sem mudar ID selecionado;
- renomear parte sem alterar relações;
- retirar decisão humana;
- retirar fonte da composição;
- alterar um termo do holding;
- trocar routeId no recibo;
- mudar hash do brief;
- converter transcript em peça escrita;
- remover query que sustenta resultado negativo.


<a id="src-s057"></a>

### 16.6 Regressão

Baseline dirigido:

```powershell
python -m pytest -q -p no:cacheprovider `
  test_forja_exploracao_100.py `
  test_forja_legal_search.py `
  test_forja_fable5.py `
  test_forja_n4.py `
  test_forja_run.py `
  test_forja_anti_hallucination_v2.py
```

Baseline observado antes da implementação: `104 passed, 3 subtests passed`.

A contagem futura deve vir da execução viva, não deste número histórico.

---


<a id="src-s058"></a>

## 17. Comandos de verificação por mudança

```powershell
python generate_n4_contracts.py
python -m json.tool n4_schemas\ARTIFACT_CATALOG.json > $null
python forja_phase_contracts.py

python -m pytest -q -p no:cacheprovider `
  test_forja_assinatura_lite.py `
  test_forja_exploracao_100.py `
  test_forja_n4.py `
  test_forja_legal_search.py `
  test_forja_fable5.py `
  test_forja_run.py `
  test_forja_n3_package.py `
  test_forja_anti_hallucination_v2.py `
  test_forja_anti_cheat.py `
  test_forja_autoresearch.py `
  test_forja_architecture.py

python validate_forja_n3.py --real-word --run-replay
python forja_regua.py
```

Depois de mudança estrutural relevante:

```powershell
python "C:\Users\IgorPC\.claude\projects\00_MAPA_ARQUITETURA_IA\REGENERAR_MAPAS_ARQUITETURA.py"
python "C:\Users\IgorPC\.claude\projects\00_MAPA_ARQUITETURA_IA\APROFUNDAR_MAPAS_ARQUITETURA.py"
```

Renderizar e inspecionar os HTMLs, consultar Graphify e atualizar hashes.

---


<a id="src-s059"></a>

## 18. Critério técnico de concluído

1. modos e `pilotCases` têm namespace próprio;
2. artefatos novos estão no catálogo, schemas e contratos gerados;
3. F2-B não pergunta o que o acervo responde;
4. silêncio material não cria fato;
5. resposta e decisão têm autoria e proveniência;
6. mapa não trata metadado como prova de composição/prevenção;
7. brief tem rota útil, decisão e referências válidas;
8. pesquisa jurídica é reproduzível;
9. anchor decisiva possui conteúdo, locator, hash, confronto e regime;
10. TeiaJus recusa ação paga ou não autorizada;
11. corpus não produz falsa autoria;
12. F6 mantém um draft;
13. F7/F7-B recompõem brief, rota e recibo;
14. invalidadores foram exercitados;
15. casos legados passam;
16. rollback `off` passa;
17. suíte dirigida, suíte ampliada, replay e Régua passam;
18. mapas arquiteturais foram regenerados e validados;
19. nenhuma alegação de eficácia excede a evidência.

Sem piloto, o estado máximo é `technical_capability_complete`. Promoção posterior exige os gates do PRD.
