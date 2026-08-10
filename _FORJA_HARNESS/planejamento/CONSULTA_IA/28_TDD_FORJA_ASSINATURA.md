# Consulta IA — TDD — FORJA-ASSINATURA

> Cópia de consulta derivada. O documento canônico permanece no caminho de origem indicado abaixo.

## Metadados e rastreabilidade

- **Documento de origem:** `28_TDD_FORJA_ASSINATURA.md`
- **Tipo:** TDD
- **SHA-256 da origem:** `1b7135cd4632b6961ae204a8d7c8c886fe4070f29e3dfb652cc0069ed1d92e8f`
- **Linhas da origem:** 1310
- **Blocos integralmente indexados:** 92
- **Geração:** 2026-08-10T13:53:35-03:00
- **Cobertura:** 100% das linhas e do texto da origem, sem omissão.
- **Links relativos normalizados:** 0 destino(s), apenas para preservar a navegação na cópia.

## Roteiro de consulta para IA

**Síntese de localização:** RECLASSIFICADO EM 25/07/2026 — desenho experimental de longo prazo. O TDD vigente para execução é planejamento/34TDDFORJAASSINATURALITECOCRIACAOPRECEDENTES.md.

**Termos de recuperação:** json, não, schema, recall, signature, f4-s, shortlist, configured_mode, snapshot, grounding, f7-b, modo.

Use o índice abaixo para localizar o bloco pertinente. Cada entrada informa as linhas exatas no documento de origem. Para afirmações materiais, leia o bloco integral e confira o arquivo canônico pelo SHA-256.

## Índice detalhado e cobertura integral

- [SRC-S001 · L1–L11 · TDD — FORJA-ASSINATURA](#src-s001)
  - Assuntos: tdd, planejamento, forja-assinatura, desenho, reclassificado, experimental, longo, prazo
  - Trecho-guia: RECLASSIFICADO EM 25/07/2026 — desenho experimental de longo prazo. O TDD vigente para execução é planejamento/34TDDFORJAASSINATURALITECOCRIACAOPRECEDENTES.md.
  - SHA-256 do bloco: `d60bb3568496b132bba99a25baa65454a6e8ef61fe513437270a3ec23d619e26`
  - [SRC-S002 · L12–L28 · 1. Objetivo técnico](#src-s002)
    - Caminho: TDD — FORJA-ASSINATURA > 1. Objetivo técnico
    - Assuntos: objetivo, técnico, f4-s, f5-s, f6-a, adicionar, subesteira, hash-bound
    - Trecho-guia: Adicionar à FORJA uma subesteira hash-bound que:
    - SHA-256 do bloco: `50a6e9f2f629159abcc6d3dc89d02f593d4f0801763d0b84014d9fd2020511f3`
  - [SRC-S003 · L29–L44 · 2. Restrições do sistema vivo](#src-s003)
    - Caminho: TDD — FORJA-ASSINATURA > 2. Restrições do sistema vivo
    - Assuntos: não, restrições, sistema, vivo, contratos, possui, recompõe, forja_phase_contracts
    - Trecho-guia: 1. forjaphasecontracts.py resolve os contratos F0–F10. 2. phasecontracts/F6.json não possui inputs condicionais. 3. forjarun.py publica artefatos e recompõe gates; exit 0 não é promoção. 4. forjan4validate.py possui FLAGFILES, VALIDATORS e modo efetivo por pilotCases. 5. forjaarb
    - SHA-256 do bloco: `dca2f8ce50d577b07201631050f404b977fcb0489df9bb9b7fcb1ed36f23d3cb`
  - [SRC-S004 · L45–L84 · 3. Topologia](#src-s004)
    - Caminho: TDD — FORJA-ASSINATURA > 3. Topologia
    - Assuntos: signature, topologia, f4-s, flow, text, inputs, snapshot, map
    - Trecho-guia: Documento de consulta sobre 3. Topologia.
    - SHA-256 do bloco: `4226e2713c7a2e8fee6adf1689eb71affc4b7c895268a320b92f43bbfc8a6ee2`
  - [SRC-S005 · L85–L127 · 4. Estrutura de arquivos-alvo](#src-s005)
    - Caminho: TDD — FORJA-ASSINATURA > 4. Estrutura de arquivos-alvo
    - Assuntos: schema, json, estrutura, arquivos-alvo, raiz, padrão, text, signature
    - Trecho-guia: Compatibilidade com o layout real prevalece. Se os testes permanecerem na raiz, não criar um segundo padrão apenas para esta feature.
    - SHA-256 do bloco: `bb45697b46d843ffad906fa29e4b29cd1d070757830da1c71355a85edf756f56`
  - [SRC-S006 · L128–L129 · 5. Fronteiras de responsabilidade](#src-s006)
    - Caminho: TDD — FORJA-ASSINATURA > 5. Fronteiras de responsabilidade
    - Assuntos: fronteiras, responsabilidade
    - Trecho-guia: Documento de consulta sobre 5. Fronteiras de responsabilidade.
    - SHA-256 do bloco: `25fb3d7130260a18a447f1c100da43cbeca278141fabd71bd2918e328df6ccec`
    - [SRC-S007 · L130–L142 · 5.1 Domínio puro](#src-s007)
      - Caminho: TDD — FORJA-ASSINATURA > 5. Fronteiras de responsabilidade > 5.1 Domínio puro
      - Assuntos: domínio, puro, módulos, filesystem, subprocesso, rede, models, geometry
      - Trecho-guia: Módulos sem filesystem, subprocesso ou rede:
      - SHA-256 do bloco: `4de5c28a047ef1a031d70bc765036ea18361e51c04df86bbb330efe2aecbc41e`
    - [SRC-S008 · L143–L157 · 5.2 Adapters](#src-s008)
      - Caminho: TDD — FORJA-ASSINATURA > 5. Fronteiras de responsabilidade > 5.2 Adapters
      - Assuntos: adapters, invocações, execução, contracts, schema, catalog, config, resolução
      - Trecho-guia: contracts.py: schema/catalog; config.py: resolução de modo e budget; snapshot.py: leitura e hash; grounding.py: integração com ledgers; candidates.py: invocações isoladas; blind.py: bundles, mapping e julgadores; recall.py: invocações leitor/verificador; memory.py: append-only; t
      - SHA-256 do bloco: `d81295d68c7f7d365a6f432ace49bb081c600ef7baf02936dc20c07fe0015e49`
    - [SRC-S009 · L158–L168 · 5.3 Integrações existentes](#src-s009)
      - Caminho: TDD — FORJA-ASSINATURA > 5. Fronteiras de responsabilidade > 5.3 Integrações existentes
      - Assuntos: integrações, existentes, sidecars, mapa, geometria, source, ledger, execução
      - Trecho-guia: F4: sidecars de mapa/geometria; F5: source ledger; F6: execução interna e um output canônico; F7: correção jurídica; F7-B: edição local e validação; N4: catálogo, schemas, flag e modo por caso; AUTO-RESEARCH: avaliação offline; state machine: eventos e supersession.
      - SHA-256 do bloco: `44153aaa6d606eb76b066257796df362fb2f0ca0b2fe0924f8a8ef62af7aef2d`
  - [SRC-S010 · L169–L192 · 6. Modelo de dados comum](#src-s010)
    - Caminho: TDD — FORJA-ASSINATURA > 6. Modelo de dados comum
    - Assuntos: hex, modelo, dados, comum, artifactsha256, todo, artefato, json
    - Trecho-guia: O artifactSha256 é calculado sobre payload canônico sem o próprio campo.
    - SHA-256 do bloco: `7eab8cedd65302232062c9e2c5ea7fd765e177a830978c30b2620f52bfff15e3`
    - [SRC-S011 · L193–L216 · 6.1 Enums](#src-s011)
      - Caminho: TDD — FORJA-ASSINATURA > 6. Modelo de dados comum > 6.1 Enums
      - Assuntos: enums, text, signaturemode, off, shadow, pilot_blocking, default_on, executionassurance
      - Trecho-guia: Enums desconhecidos falham no schema.
      - SHA-256 do bloco: `fd43f8187f3ef5127b289e2e2e6afc810d11fd18756ccb48facf426f87a21e92`
  - [SRC-S012 · L217–L248 · 7. Configuração](#src-s012)
    - Caminho: TDD — FORJA-ASSINATURA > 7. Configuração
    - Assuntos: configuração, signature, json, mode, off, true, adicionar, seção
    - Trecho-guia: Adicionar seção signature em FORJAN3CONFIG.json somente na W1, com mode=off.
    - SHA-256 do bloco: `a717d0818d5870a71111a96cec15537546e06c9b1d86e8025ed5dbd3984ebbd4`
    - [SRC-S013 · L249–L265 · 7.1 Resolução do modo](#src-s013)
      - Caminho: TDD — FORJA-ASSINATURA > 7. Configuração > 7.1 Resolução do modo
      - Assuntos: configured_mode, return, override, resolução, modo, effective_mode, pilot_cases, case_identity
      - Trecho-guia: Reutilizar/refatorar o comportamento atual de forjan4validate.effectivemode() para uma API pública comum. Não copiar a lógica em dois módulos.
      - SHA-256 do bloco: `fbc44049401e73c892c9512aa6eceebfb373bf938e43f80e9c33b5e4cd3f5683`
    - [SRC-S014 · L266–L294 · 7.2 Budget profile](#src-s014)
      - Caminho: TDD — FORJA-ASSINATURA > 7. Configuração > 7.2 Budget profile
      - Assuntos: budget, profile, schema, obrigatório, json, profileid, signature-pilot-v1, measuredat
      - Trecho-guia: Zeros acima ilustram tipos, não valores aceitos. O validador exige inteiros positivos. W0 mede o baseline; W1 grava números e hash antes de W2.
      - SHA-256 do bloco: `2e53dc3cccabf6f5123115b8cc10547a4977dde6082c5e08e3492ce64edbb351`
  - [SRC-S015 · L295–L296 · 8. Snapshot](#src-s015)
    - Caminho: TDD — FORJA-ASSINATURA > 8. Snapshot
    - Assuntos: snapshot
    - Trecho-guia: Documento de consulta sobre 8. Snapshot.
    - SHA-256 do bloco: `885c422e9d757a0b6a61b1b4ee5b1cce7962fec9b13bb17240b75225bd7a2cec`
    - [SRC-S016 · L297–L300 · 8.1 Input](#src-s016)
      - Caminho: TDD — FORJA-ASSINATURA > 8. Snapshot > 8.1 Input
      - Assuntos: input, referências, artefatos, canônicos, não, cópias, soltas
      - Trecho-guia: Referências aos artefatos canônicos, não cópias soltas.
      - SHA-256 do bloco: `0b1cce9f960adbfbe84bdfe61d0fc9a7bd4876df73bb93b9b650a87a40296b06`
    - [SRC-S017 · L301–L311 · 8.2 Algoritmo](#src-s017)
      - Caminho: TDD — FORJA-ASSINATURA > 8. Snapshot > 8.2 Algoritmo
      - Assuntos: algoritmo, paths, confirmar, resolver, existência, recomputar, sha-256, ledger
      - Trecho-guia: 1. resolver paths; 2. confirmar existência; 3. recomputar SHA-256; 4. confirmar ledger/version; 5. montar objeto com paths relativos, hashes e papéis; 6. canonicalizar JSON; 7. calcular inputSnapshotSha256; 8. persistir antes da primeira chamada.
      - SHA-256 do bloco: `584fb9218b891fc00a88c400bd6ec8b0e550e4d4f30ba98ad0ed3fae18051acb`
    - [SRC-S018 · L312–L316 · 8.3 Proibição](#src-s018)
      - Caminho: TDD — FORJA-ASSINATURA > 8. Snapshot > 8.3 Proibição
      - Assuntos: proibição, nenhum, candidato, julgamento, recall, pode, referir, snapshot
      - Trecho-guia: Nenhum candidato, julgamento ou recall pode referir snapshot distinto no mesmo lote. Mudança posterior cria nova tentativa.
      - SHA-256 do bloco: `9735d807e4dd7dbde1d3af245aac7262c7ac7d2a4ba9a5909335f2395467e341`
  - [SRC-S019 · L317–L318 · 9. F4-S — mapa e geometrias](#src-s019)
    - Caminho: TDD — FORJA-ASSINATURA > 9. F4-S — mapa e geometrias
    - Assuntos: f4-s, mapa, geometrias
    - Trecho-guia: Documento de consulta sobre 9. F4-S — mapa e geometrias.
    - SHA-256 do bloco: `0a118affc185841a53ad134c305207fce387bcda60894603a2d8a6a67fffa473`
    - [SRC-S020 · L319–L352 · 9.1 F4SIGNATUREMAP.json](#src-s020)
      - Caminho: TDD — FORJA-ASSINATURA > 9. F4-S — mapa e geometrias > 9.1 F4SIGNATUREMAP.json
      - Assuntos: não, json, knowngapids, f4signaturemap, f4_signature_map, campos, domínio, decisionquestion
      - Trecho-guia: strings não vazias; todos os IDs resolvem; knownGapIds não aparecem como fatos; providência pertence ao blueprint/pedidos; frase-mãe não adiciona certeza; conteúdo dos autos não é interpretado como instrução.
      - SHA-256 do bloco: `ea7ba69f1a591723150cd96559f7394c0af11bc36d5ac8e0f0f7c07e4c58f837`
    - [SRC-S021 · L353–L376 · 9.2 F4SIGNATUREGEOMETRIES.json](#src-s021)
      - Caminho: TDD — FORJA-ASSINATURA > 9. F4-S — mapa e geometrias > 9.2 F4SIGNATUREGEOMETRIES.json
      - Assuntos: json, f4signaturegeometries, f4_signature_geometries, cada, geometria, geometryid, primaryaxis, causality
      - Trecho-guia: Documento de consulta sobre 9.2 F4SIGNATUREGEOMETRIES.json.
      - SHA-256 do bloco: `42015d708a2b8da15e70c5a6fe13900744db306ae56ca968584e47d091fae192`
    - [SRC-S022 · L377–L396 · 9.3 Diversidade determinística](#src-s022)
      - Caminho: TDD — FORJA-ASSINATURA > 9. F4-S — mapa e geometrias > 9.3 Diversidade determinística
      - Assuntos: diversidade, determinística, claim_id, for, step, limiar, não, representação
      - Trecho-guia: Dois candidatos são materialmente diversos quando:
      - SHA-256 do bloco: `93ac362be10ab91069a99bcb811a6e853232622ac423b2f74ad702fc80acbb3b`
  - [SRC-S023 · L397–L421 · 10. F5 — grounding](#src-s023)
    - Caminho: TDD — FORJA-ASSINATURA > 10. F5 — grounding
    - Assuntos: referência, grounding, missing, stale, revoked, função, pura, python
    - Trecho-guia: resolved; missing; stale; revoked; unsupportedrelation.
    - SHA-256 do bloco: `ef4b317564e78e45e98a347fd3330d6233f28c7dbd12f4afeb4b79a449059fd6`
  - [SRC-S024 · L422–L423 · 11. F5-S — microbrief e shortlist](#src-s024)
    - Caminho: TDD — FORJA-ASSINATURA > 11. F5-S — microbrief e shortlist
    - Assuntos: f5-s, microbrief, shortlist
    - Trecho-guia: Documento de consulta sobre 11. F5-S — microbrief e shortlist.
    - SHA-256 do bloco: `1102e02082473b49d634efd1ceba726f1dd58b93ad61f84b484c60fb177fbca1`
    - [SRC-S025 · L424–L437 · 11.1 Execução isolada](#src-s025)
      - Caminho: TDD — FORJA-ASSINATURA > 11. F5-S — microbrief e shortlist > 11.1 Execução isolada
      - Assuntos: execução, isolada, output, orquestrador, seleciona, geometrias, grounded, monta
      - Trecho-guia: 1. seleciona geometrias grounded; 2. monta prompt por geometria sem output irmão; 3. calcula promptSha256; 4. cria sessão; 5. registra envelope real ou atestação; 6. invoca; 7. persiste output antes da próxima decisão.
      - SHA-256 do bloco: `e8a75466614b7a21e465dd2bccccc874973cc7daf0c98da9a38037c3dc3e82b0`
    - [SRC-S026 · L438–L472 · 11.2 Shortlist](#src-s026)
      - Caminho: TDD — FORJA-ASSINATURA > 11. F5-S — microbrief e shortlist > 11.2 Shortlist
      - Assuntos: shortlist, json, false, strategies, fallback, abstained, vetos, primeiro
      - Trecho-guia: Vetos primeiro. Entre elegíveis, executar comparação estrutural curta. Saída:
      - SHA-256 do bloco: `5e60fb29350b937728fab81a8d6d242cd5d717c74f7b00f3a522add4a433f2f8`
  - [SRC-S027 · L473–L474 · 12. F6-A — candidatos](#src-s027)
    - Caminho: TDD — FORJA-ASSINATURA > 12. F6-A — candidatos
    - Assuntos: f6-a, candidatos
    - Trecho-guia: Documento de consulta sobre 12. F6-A — candidatos.
    - SHA-256 do bloco: `dacbbe6ec7d3583ee87cac43895617ac43325f019cd42f8f645cdf68fe5d0551`
    - [SRC-S028 · L475–L486 · 12.1 candidate0](#src-s028)
      - Caminho: TDD — FORJA-ASSINATURA > 12. F6-A — candidatos > 12.1 candidate0
      - Assuntos: candidate_0, candidate0, contrato, candidateid, candidaterole, incumbent, generationmode, incumbent_pipeline
      - Trecho-guia: candidateId = "candidate0"; candidateRole = "incumbent"; generationMode = "incumbentpipeline"; mesmo inputSnapshotSha256; sessão própria; prompt incumbente atual, sem mapa/geometrias/shortlist; texto integral persistido antes do cegamento.
      - SHA-256 do bloco: `5b7f16155423b3ad4681bd50ba6ada31a98181ecd1eb939aa2270d557af09b78`
    - [SRC-S029 · L487–L494 · 12.2 Desafiante](#src-s029)
      - Caminho: TDD — FORJA-ASSINATURA > 12. F6-A — candidatos > 12.2 Desafiante
      - Assuntos: recebe, desafiante, não, shortlist, ledgers, hash, texto, incumbente
      - Trecho-guia: recebe a shortlist e ledgers por hash; não recebe texto do incumbente; não recebe memória decisória; preserva conteúdo obrigatório; produz paragraphprovenance.
      - SHA-256 do bloco: `493feec4f53de977f2270db6a1a63fe00fc9895f691229cc29a9fa34e40325fc`
    - [SRC-S030 · L495–L509 · 12.3 Terceiro candidato](#src-s030)
      - Caminho: TDD — FORJA-ASSINATURA > 12. F6-A — candidatos > 12.3 Terceiro candidato
      - Assuntos: terceiro, shortlist, ambiguity, candidato, config, and, existe, python
      - Trecho-guia: Não gerar terceiro draft para resolver desacordo ocorrido depois no julgamento. Isso mudaria o orçamento com base no resultado.
      - SHA-256 do bloco: `858ad7e2d55dfaec2d60598994dadee56e4bf89c4fc3b46d41547f2f8cf3d697`
    - [SRC-S031 · L510–L537 · 12.4 Manifesto](#src-s031)
      - Caminho: TDD — FORJA-ASSINATURA > 12. F6-A — candidatos > 12.4 Manifesto
      - Assuntos: hex, manifesto, json, candidates, candidateid, candidate_0, candidaterole, incumbent
      - Trecho-guia: Documento de consulta sobre 12.4 Manifesto.
      - SHA-256 do bloco: `e52eefc0b87e21b45d5266e537a8deda118b4bfbf05b918680139646fd7297ee`
  - [SRC-S032 · L538–L557 · 13. Elegibilidade](#src-s032)
    - Caminho: TDD — FORJA-ASSINATURA > 13. Elegibilidade
    - Assuntos: elegibilidade, eligibility, candidate, ledgers, gates, eligibilitydecision, ordem, schema
    - Trecho-guia: eligibility(candidate, ledgers, gates) - EligibilityDecision
    - SHA-256 do bloco: `31442a7475ae67cc7784d45c28c3bef8057038aedb197bd86cf1a34baa226d62`
  - [SRC-S033 · L558–L559 · 14. F6-B — cegamento e julgamento](#src-s033)
    - Caminho: TDD — FORJA-ASSINATURA > 14. F6-B — cegamento e julgamento
    - Assuntos: f6-b, cegamento, julgamento
    - Trecho-guia: Documento de consulta sobre 14. F6-B — cegamento e julgamento.
    - SHA-256 do bloco: `e0aa5b2c20426709c866d0f92e34359a3ec05a2c051e42c6bf7c9b4947c82ab6`
    - [SRC-S034 · L560–L572 · 14.1 Extensão, não mutação do A/B](#src-s034)
      - Caminho: TDD — FORJA-ASSINATURA > 14. F6-B — cegamento e julgamento > 14.1 Extensão, não mutação do A/B
      - Assuntos: não, extensão, mutação, criar, primitives, n-way, signature, blind
      - Trecho-guia: Criar primitives N-way em forja/signature/blind.py. Reutilizar:
      - SHA-256 do bloco: `6ab9b1fb86287faeee36ec8da97dbbc804aa8006df7cc101c1df19cc361f1899`
    - [SRC-S035 · L573–L584 · 14.2 Bundles](#src-s035)
      - Caminho: TDD — FORJA-ASSINATURA > 14. F6-B — cegamento e julgamento > 14.2 Bundles
      - Assuntos: bundles, workspace, cada, par, elegível, nomes, opacos, mesmo
      - Trecho-guia: A/B; B/A; nomes opacos; mesmo conteúdo canonicalizado; mapping fora do workspace; commitment dentro do workspace; hash por bundle.
      - SHA-256 do bloco: `1ac51c57c6ec346b9514365efccc395d9b91fd618ee7087fcd40d0062dec6070`
    - [SRC-S036 · L585–L614 · 14.3 Julgadores](#src-s036)
      - Caminho: TDD — FORJA-ASSINATURA > 14. F6-B — cegamento e julgamento > 14.3 Julgadores
      - Assuntos: inválido, modo, julgadores, sessionid, juiz, degradado, planner, bancada
      - Trecho-guia: O planner de bancada recebe famílias disponíveis e produz:
      - SHA-256 do bloco: `81b7e0c2934bbc3a2fe8ea09fb1c8966dee620ef8361f54333dd5df486588c3d`
    - [SRC-S037 · L615–L638 · 14.4 Voto](#src-s037)
      - Caminho: TDD — FORJA-ASSINATURA > 14. F6-B — cegamento e julgamento > 14.4 Voto
      - Assuntos: voto, abstain, json, pairid, judgeid, order, winnerposition, anchor
      - Trecho-guia: Diagnósticos explicam; não são somados por média.
      - SHA-256 do bloco: `7a7be2560a7015000565af47a5e923c957af3dd32819518d990f7b3832aa8d10`
  - [SRC-S038 · L639–L643 · 15. Primitivas de seleção](#src-s038)
    - Caminho: TDD — FORJA-ASSINATURA > 15. Primitivas de seleção
    - Assuntos: primitivas, seleção, esta, seção, calcula, elegibilidade, grafo, vencedor
    - Trecho-guia: Esta seção calcula elegibilidade, grafo e vencedor potencial. A função final só é chamada em F6-C depois de os resultados de recall e steelman estarem válidos.
    - SHA-256 do bloco: `8badb8a5aa6d701d235a821231f0b2c3dd24f0e011571749414a8491a9d826fe`
    - [SRC-S039 · L644–L651 · 15.1 Vetos](#src-s039)
      - Caminho: TDD — FORJA-ASSINATURA > 15. Primitivas de seleção > 15.1 Vetos
      - Assuntos: vetos, falha, remover, candidatos, inelegíveis, candidate_0, for, inelegível
      - Trecho-guia: Se candidate0 for inelegível, o fluxo inteiro falha juridicamente: não usar uma desafiante editorial para encobrir falha do baseline. Retornar para a fase que originou o veto.
      - SHA-256 do bloco: `76e4aa066e66ce49aa6aa52e08d7b0600de9d9548d969cb4583713f945900cdc`
    - [SRC-S040 · L652–L660 · 15.2 Matriz](#src-s040)
      - Caminho: TDD — FORJA-ASSINATURA > 15. Primitivas de seleção > 15.2 Matriz
      - Assuntos: matriz, sob, cada, par, elegível, consolidar, somente, voto
      - Trecho-guia: Para cada par elegível, consolidar somente voto:
      - SHA-256 do bloco: `f3303c91bbc3dbb1a554963415ef36e0b6676f6bfd0481c0e81383618b45c504`
    - [SRC-S041 · L661–L686 · 15.3 Vencedor](#src-s041)
      - Caminho: TDD — FORJA-ASSINATURA > 15. Primitivas de seleção > 15.3 Vencedor
      - Assuntos: return, winner, preserve_incumbent, config, eligible, stable, vencedor, candidates
      - Trecho-guia: Nunca ordenar por SHA para mérito. SHA serve apenas para identidade e determinismo de armazenamento.
      - SHA-256 do bloco: `40a1764735376e703f1b29a484f614ff462ef6540707f6f729e7c99d594ea7f4`
    - [SRC-S042 · L687–L696 · 15.4 Terceiro juiz](#src-s042)
      - Caminho: TDD — FORJA-ASSINATURA > 15. Primitivas de seleção > 15.4 Terceiro juiz
      - Assuntos: terceiro, juiz, permitido, somente, regra, estiver, manifest, quais
      - Trecho-guia: É permitido somente se a regra já estiver no manifest:
      - SHA-256 do bloco: `142ff2ff75320441a235234f678ee90ff97c061920e0b260ea01987054719f54`
  - [SRC-S043 · L697–L698 · 16. Recall e conclusão F6-C](#src-s043)
    - Caminho: TDD — FORJA-ASSINATURA > 16. Recall e conclusão F6-C
    - Assuntos: recall, conclusão, f6-c
    - Trecho-guia: Documento de consulta sobre 16. Recall e conclusão F6-C.
    - SHA-256 do bloco: `ae820739794fdbea79cc2401450e6a89c0e093893ce1f070d465157e60cf1229`
    - [SRC-S044 · L699–L716 · 16.1 Remoção da síntese](#src-s044)
      - Caminho: TDD — FORJA-ASSINATURA > 16. Recall e conclusão F6-C > 16.1 Remoção da síntese
      - Assuntos: síntese, remoção, marcadores, deve, produzir, canônicos, início, fim
      - Trecho-guia: F6 deve produzir marcadores canônicos de início/fim da síntese. Função:
      - SHA-256 do bloco: `d0f24cec4d9198e1ce8f91e4a0ad1f10bc79ce512f710ce0d6497f8a8472acbd`
    - [SRC-S045 · L717–L726 · 16.2 Leitor e verificador](#src-s045)
      - Caminho: TDD — FORJA-ASSINATURA > 16. Recall e conclusão F6-C > 16.2 Leitor e verificador
      - Assuntos: leitor, verificador, cartão, mapa, não, recebe, sessões, separadas
      - Trecho-guia: leitor: corpo → cartão; verificador: cartão + mapa → fidelidade.
      - SHA-256 do bloco: `cc4004d6bc9228dd590e5a2c865da1918ccc208707f192a621bfee12652384a3`
    - [SRC-S046 · L727–L734 · 16.3 Uso na seleção](#src-s046)
      - Caminho: TDD — FORJA-ASSINATURA > 16. Recall e conclusão F6-C > 16.3 Uso na seleção
      - Assuntos: uso, seleção, não, falso, elimina, desafiante, questão, providência
      - Trecho-guia: falso → elimina desafiante; questão/providência ausente → impede vitória; demais campos → diagnóstico; resultado não reabre candidato já inelegível; recall não compensa veto.
      - SHA-256 do bloco: `db99574b8f99ca05fe3ffd6bf3f28d99d8c705f1b83ff6885c595bc1b32b657d`
    - [SRC-S047 · L735–L746 · 16.4 Seleção final](#src-s047)
      - Caminho: TDD — FORJA-ASSINATURA > 16. Recall e conclusão F6-C > 16.4 Seleção final
      - Assuntos: seleção, final, recall, falha, f6-c, combina, matriz, válida
      - Trecho-guia: F6-C combina a matriz válida da seção 15, recall e steelman. Só então:
      - SHA-256 do bloco: `bbe0abe31a0e37bee6647d58ccaf2014dde305eb95ffc08b7ffc44f272a2240c`
  - [SRC-S048 · L747–L748 · 17. Topologia de assinatura](#src-s048)
    - Caminho: TDD — FORJA-ASSINATURA > 17. Topologia de assinatura
    - Assuntos: topologia, assinatura
    - Trecho-guia: Documento de consulta sobre 17. Topologia de assinatura.
    - SHA-256 do bloco: `f71c763fae6112daac87e3ecceb7988ef5ec30866cc9ff13c3ecf52ae6a2e325`
    - [SRC-S049 · L749–L774 · 17.1 Canonicalização](#src-s049)
      - Caminho: TDD — FORJA-ASSINATURA > 17. Topologia de assinatura > 17.1 Canonicalização
      - Assuntos: canonicalização, json, mothersentencenormalized, sections, sectionid, thesisid, claimids, ordinal
      - Trecho-guia: pontuação; fronteira de frase; conectivos; escolhas lexicais; tamanho de parágrafo.
      - SHA-256 do bloco: `915bc8ca0e6df97f24711d60945b8ccc9349640fcac3083a4c172af918a3821e`
    - [SRC-S050 · L775–L784 · 17.2 Comparação](#src-s050)
      - Caminho: TDD — FORJA-ASSINATURA > 17. Topologia de assinatura > 17.2 Comparação
      - Assuntos: comparação, passa, classes, local_editorial_change, legal_correction_nonstructural, registra, structural_change, invalida
      - Trecho-guia: localeditorialchange: passa; legalcorrectionnonstructural: passa e registra; structuralchange: invalida seleção; requestorpolaritychange: P0; unclassifiable: fail-closed.
      - SHA-256 do bloco: `195bb89becb11535fbe2808330dd3eebdd748235bdcfba9410e38b69ae8b28a0`
    - [SRC-S051 · L785–L797 · 17.3 Integração F7-B](#src-s051)
      - Caminho: TDD — FORJA-ASSINATURA > 17. Topologia de assinatura > 17.3 Integração F7-B
      - Assuntos: integração, f7-b, recibo, extrair, validador, forja_fable5, taste_receipt_findings, api
      - Trecho-guia: Extrair o validador de recibo de forjafable5.tastereceiptfindings() para API pública. validateeditorialbundle() chama:
      - SHA-256 do bloco: `ae2b5b2642b01472eda3d40771168249df50cf5f2bd3ef1a48b53df3a1ab63f1`
  - [SRC-S052 · L798–L799 · 18. Memória](#src-s052)
    - Caminho: TDD — FORJA-ASSINATURA > 18. Memória
    - Assuntos: memória
    - Trecho-guia: Documento de consulta sobre 18. Memória.
    - SHA-256 do bloco: `87c540d4934c3ae2e28ca7bcefac7f3e537045e8c6957225a3a91a74b8b93ecb`
    - [SRC-S053 · L800–L817 · 18.1 Evento](#src-s053)
      - Caminho: TDD — FORJA-ASSINATURA > 18. Memória > 18.1 Evento
      - Assuntos: evento, json, decisionid, caselineage, product, selectedcandidatehash, rejectedcandidatehashes, reasoncodes
      - Trecho-guia: Documento de consulta sobre 18.1 Evento.
      - SHA-256 do bloco: `ea056a44135f5143791b2a2ea91a98558ba43e8aaddd43a6748660f63da210ae`
    - [SRC-S054 · L818–L831 · 18.2 Política de acesso](#src-s054)
      - Caminho: TDD — FORJA-ASSINATURA > 18. Memória > 18.2 Política de acesso
      - Assuntos: política, acesso, teste, python, def, load_production_generation_context, assert, config
      - Trecho-guia: Teste por instrumentação deve registrar os arquivos e blocos passados a cada invocação. Regex isolada no prompt não basta; o teste compara allowlist de inputs.
      - SHA-256 do bloco: `baec1191cf0c4796e3b38017bd8ff00bedb40192356e3bd11b7829f19da70da6`
  - [SRC-S055 · L832–L857 · 19. Invalidação](#src-s055)
    - Caminho: TDD — FORJA-ASSINATURA > 19. Invalidação
    - Assuntos: invalidação, evento, stale, mapa, dependências, text, snapshot, map
    - Trecho-guia: 1. receber evento de mudança; 2. recomputar hash da origem; 3. localizar nós descendentes; 4. marcar stale, nunca apagar; 5. emitir evento append-only; 6. reabrir no primeiro subestágio afetado; 7. impedir promoção de descendente stale.
    - SHA-256 do bloco: `d6d8e1ad0dac97d27b80b4afcfc8a08d9b0a4929e2775e9f00ec8cabbd0406c5`
  - [SRC-S056 · L858–L859 · 20. Registro N4](#src-s056)
    - Caminho: TDD — FORJA-ASSINATURA > 20. Registro N4
    - Assuntos: registro
    - Trecho-guia: Documento de consulta sobre 20. Registro N4.
    - SHA-256 do bloco: `3b471d85b79e0e34fb510345f40f95f162802e55f6bb9d655bf1066c186fabf9`
    - [SRC-S057 · L860–L870 · 20.1 Catálogo](#src-s057)
      - Caminho: TDD — FORJA-ASSINATURA > 20. Registro N4 > 20.1 Catálogo
      - Assuntos: catálogo, adicionar, artefatos, generate_n4_contracts, regenerar, schemas, artifact_catalog, json
      - Trecho-guia: Adicionar artefatos ao generaten4contracts.py, regenerar:
      - SHA-256 do bloco: `2db09349ed01189dc017379eb18cb2052d91782cf05d572774ef7de076f843ca`
    - [SRC-S058 · L871–L884 · 20.2 Flag](#src-s058)
      - Caminho: TDD — FORJA-ASSINATURA > 20. Registro N4 > 20.2 Flag
      - Assuntos: flag, arquivos, piloto, feature, sugerida, text, n4signaturev1, exigidos
      - Trecho-guia: Arquivos exigidos dependem do modo efetivo do caso. A validação deve provar:
      - SHA-256 do bloco: `5bef73b2f94f3c43ddb6cdc67b7000d234f48febb7b2fae8df75d869b64ce924`
  - [SRC-S059 · L885–L911 · 21. Eventos](#src-s059)
    - Caminho: TDD — FORJA-ASSINATURA > 21. Eventos
    - Assuntos: eventos, adicionar, state, machine, apenas, após, contratos, text
    - Trecho-guia: Adicionar ao state machine apenas após contratos:
    - SHA-256 do bloco: `782b66db2b9e8ea363017965e09f8c68cabd85bc00614b2dfec6e8a4bceb066a`
  - [SRC-S060 · L912–L940 · 22. Reason codes mínimos](#src-s060)
    - Caminho: TDD — FORJA-ASSINATURA > 22. Reason codes mínimos
    - Assuntos: reason, codes, mínimos, text, sig-config-invalid, sig-budget-profile-missing, sig-budget-exceeded, sig-snapshot-drift
    - Trecho-guia: Reason code desconhecido não é aceito como texto livre em decisão.
    - SHA-256 do bloco: `508f379e7d18c59e36aa114645dbf2e9f93881d307c22e435cb640c7689dbd0b`
  - [SRC-S061 · L941–L958 · 23. CLI proposta](#src-s061)
    - Caminho: TDD — FORJA-ASSINATURA > 23. CLI proposta
    - Assuntos: python, forja_signature, case-id, cli, proposta, status, powershell, snapshot
    - Trecho-guia: Toda mutação exige --attempt-id explícito ou resolve a tentativa viva de modo unívoco. status é read-only.
    - SHA-256 do bloco: `a0dea38e99d78b241c82459bbde6ab8525284fa34a11441102f27278dd02f75c`
  - [SRC-S062 · L959–L960 · 24. Testes](#src-s062)
    - Caminho: TDD — FORJA-ASSINATURA > 24. Testes
    - Assuntos: testes
    - Trecho-guia: Documento de consulta sobre 24. Testes.
    - SHA-256 do bloco: `533395235bfb0dce4ae9bc671b207c75204bf761663f4f51ad071a3c8ad8ceeb`
    - [SRC-S063 · L961–L977 · 24.1 Unidade](#src-s063)
      - Caminho: TDD — FORJA-ASSINATURA > 24. Testes > 24.1 Unidade
      - Assuntos: unidade, config, modo, efetivo, budget, profile, positivo, canonical
      - Trecho-guia: config e modo efetivo; budget profile positivo; canonical hash; resolução de IDs; distância estrutural; grounding; expansão de terceiro draft; veto filter; Condorcet; ciclo/empate; remoção de síntese; topologia; invalidation graph; reason codes.
      - SHA-256 do bloco: `b09efb8e65bf0023fa6d78089e76a277024e8898c8a93b1f8af09611c8d031ae`
    - [SRC-S064 · L978–L990 · 24.2 Contrato](#src-s064)
      - Caminho: TDD — FORJA-ASSINATURA > 24. Testes > 24.2 Contrato
      - Assuntos: contrato, enum, todos, sete, schemas, válido, inválido, candidate_0
      - Trecho-guia: todos os sete schemas válido/inválido; candidate0 obrigatório; assurance enum; independence enum; fallback de shortlist; decision com âncora; recall com hash; seleção com snapshot; artifacts no catálogo; gerador e derivados sem drift.
      - SHA-256 do bloco: `fd4b032292f449244d9ba1c0de45dac3791eb0ef8494513a224feee95ee09c21`
    - [SRC-S065 · L991–L1005 · 24.3 Integração](#src-s065)
      - Caminho: TDD — FORJA-ASSINATURA > 24. Testes > 24.3 Integração
      - Assuntos: seleção, estrutural, integração, piloto, lista, não, bloqueia, desafiante
      - Trecho-guia: 1. off sem invocações e sem diff de output; 2. shadow produz sidecars e mantém incumbente; 3. piloto fora da lista não bloqueia; 4. piloto dentro da lista bloqueia sem artefatos; 5. baseline + desafiante → seleção; 6. abstenção → hash de candidate0; 7. desafiante vence → único dr
      - SHA-256 do bloco: `64b45d5b401b43d20a25cf32c948f61d9db09f2b5ce2f34aa5dd6f015df62206`
    - [SRC-S066 · L1006–L1019 · 24.4 Metamórficos](#src-s066)
      - Caminho: TDD — FORJA-ASSINATURA > 24. Testes > 24.4 Metamórficos
      - Assuntos: metamórficos, trocar, palavras, mudar, mantendo, inverter, posição, renomear
      - Trecho-guia: inverter posição; renomear candidato; trocar autor/modelo no rótulo; aumentar comprimento sem conteúdo; repetir palavras da rubrica; preservar palavras e mudar nexo; trocar nomes mantendo relações; remover âncora; retirar síntese antes do recall; fundir frases sem mudar topologia
      - SHA-256 do bloco: `b38298f73926e52af5e3b182fb457a6538f4691989637be2bffd14efae6ff531`
    - [SRC-S067 · L1020–L1037 · 24.5 Sabotagem](#src-s067)
      - Caminho: TDD — FORJA-ASSINATURA > 24. Testes > 24.5 Sabotagem
      - Assuntos: sabotagem, mapping, prompt, true, após, adulterado, dentro, workspace
      - Trecho-guia: mapping adulterado; mapping dentro do workspace; prompt irmão; memória decisória no prompt; verified=true sem envelope; mesma sessão como juiz; family spoofing; âncora inexistente; snapshot alterado após julgamento; approved=true sem recomputação; menor SHA como desempate; tercei
      - SHA-256 do bloco: `95825db4347390850b1885b6517fd264d1624c50c045800f4018a03337c7da13`
    - [SRC-S068 · L1038–L1049 · 24.6 Canários de detector](#src-s068)
      - Caminho: TDD — FORJA-ASSINATURA > 24. Testes > 24.6 Canários de detector
      - Assuntos: canários, detector, mudança, pedido, inversão, polaridade, troca, frase-mãe
      - Trecho-guia: mudança de pedido; inversão de polaridade; troca de frase-mãe; reordenação de tese; remoção de conteúdo obrigatório; edição local legítima; falso positivo de fusão de frases; síntese não marcada; recall com elemento inventado.
      - SHA-256 do bloco: `10913afdecbe71d69b8eef1147cc1fa1d6df904cca96ce2cffc9e7c3af4af0ea`
  - [SRC-S069 · L1050–L1069 · 25. Matriz requisito → teste](#src-s069)
    - Caminho: TDD — FORJA-ASSINATURA > 25. Matriz requisito → teste
    - Assuntos: requisito, matriz, teste, fallback, testes, principais, rf-01, modo
    - Trecho-guia: Documento de consulta sobre 25. Matriz requisito → teste.
    - SHA-256 do bloco: `1bee9bbb6110df3fa6fda98b20ee4b1316034b8f9707ff26a81b5b93b1d15954`
  - [SRC-S070 · L1070–L1103 · 26. Testes de promoção da política](#src-s070)
    - Caminho: TDD — FORJA-ASSINATURA > 26. Testes de promoção da política
    - Assuntos: testes, promoção, política, technical_candidate_passed, harness, avaliação, deve, pré-registrar
    - Trecho-guia: O harness de avaliação deve pré-registrar:
    - SHA-256 do bloco: `25d0d6f0a67ba33796d1a87069c482aaa171c8860a12b2919e4af275938ec989`
  - [SRC-S071 · L1104–L1105 · 27. Observabilidade](#src-s071)
    - Caminho: TDD — FORJA-ASSINATURA > 27. Observabilidade
    - Assuntos: observabilidade
    - Trecho-guia: Documento de consulta sobre 27. Observabilidade.
    - SHA-256 do bloco: `b15c750adbf2107525a4f37f492a41009109474757448435b41a857233749cb7`
    - [SRC-S072 · L1106–L1117 · 27.1 Eventos por caso](#src-s072)
      - Caminho: TDD — FORJA-ASSINATURA > 27. Observabilidade > 27.1 Eventos por caso
      - Assuntos: eventos, caso, tempo, tokens, estágio, candidatos, tentados, elegíveis
      - Trecho-guia: tempo e tokens por estágio; candidatos tentados/elegíveis; reason codes; modo de independência; matriz pareada; recall; decisão; fallback; alterações em F7/F7-B.
      - SHA-256 do bloco: `7b468ec64688324b39949527e98d18307cdd8b52f4b9408252da8c404dea4980`
    - [SRC-S073 · L1118–L1131 · 27.2 Agregados](#src-s073)
      - Caminho: TDD — FORJA-ASSINATURA > 27. Observabilidade > 27.2 Agregados
      - Assuntos: agregados, separar, produto, tribunal, fase, processual, linhagem, modo
      - Trecho-guia: produto; tribunal; fase processual; linhagem; modo; família/modelo; garantia de execução.
      - SHA-256 do bloco: `4b2dade6c217501d6c42b40642a0947387ac04a71685961f76f94aaf9b39576c`
    - [SRC-S074 · L1132–L1144 · 27.3 Alertas](#src-s074)
      - Caminho: TDD — FORJA-ASSINATURA > 27. Observabilidade > 27.3 Alertas
      - Assuntos: alertas, taxa, baseline, unverified, aumento, abstenção, terceiro, draft
      - Trecho-guia: taxa de P0 baseline; taxa de unverified; aumento de abstenção; terceiro draft acima do esperado; estouro de budget; mudança estrutural em F7/F7-B; recall inválido; regressão package/F8.
      - SHA-256 do bloco: `4480513a486c5b69a89024ef4b7e1455eaae1724adcd0622405fec6ccd69c167`
  - [SRC-S075 · L1145–L1175 · 28. Desempenho e cache](#src-s075)
    - Caminho: TDD — FORJA-ASSINATURA > 28. Desempenho e cache
    - Assuntos: muda, cache, desempenho, não, schema, chave, text, protocolversion
    - Trecho-guia: modelo não é verificável; source ledger muda; rubrica muda; prompt muda; candidato muda; schema muda.
    - SHA-256 do bloco: `2fbf6489a0ac484e95c063db8ed7b1a9da1cad83405cf4da015f38e2a0933cd7`
  - [SRC-S076 · L1176–L1187 · 29. Segurança e privacidade](#src-s076)
    - Caminho: TDD — FORJA-ASSINATURA > 29. Segurança e privacidade
    - Assuntos: segurança, privacidade, fora, workspace, nenhum, hmac, key, mapping
    - Trecho-guia: HMAC key fora do workspace; mapping fora do workspace; logs sem conteúdo integral quando hashes bastarem; corpus público somente sanitizado; prompt injection tratada nos inputs jurídicos e nos bundles de juiz; nenhum segredo em telemetry; paths externos validados; nenhuma API pag
    - SHA-256 do bloco: `878f9c2a00a4b78b610dc374716d744b2f06010a944809b920f476bb2609e078`
  - [SRC-S077 · L1188–L1189 · 30. Ordem de implementação e commits](#src-s077)
    - Caminho: TDD — FORJA-ASSINATURA > 30. Ordem de implementação e commits
    - Assuntos: ordem, implementação, commits
    - Trecho-guia: Documento de consulta sobre 30. Ordem de implementação e commits.
    - SHA-256 do bloco: `968db0cf0357710950adb1c38c62b26cdd75eae6cf81b5ccab66c58f8b1c160b`
    - [SRC-S078 · L1190–L1193 · W0 — baseline](#src-s078)
      - Caminho: TDD — FORJA-ASSINATURA > 30. Ordem de implementação e commits > W0 — baseline
      - Assuntos: baseline, somente, medição, classificação, drift, relatório
      - Trecho-guia: Somente medição, classificação de drift e relatório.
      - SHA-256 do bloco: `aeb52bdd98f022a35dec5ed34e7086ca7b254d0eb744d498c801c81a4ceb55eb`
    - [SRC-S079 · L1194–L1206 · W1 — linguagem](#src-s079)
      - Caminho: TDD — FORJA-ASSINATURA > 30. Ordem de implementação e commits > W1 — linguagem
      - Assuntos: linguagem, arquivos, pacote, vazio, tipos, schemas, config, off
      - Trecho-guia: pacote vazio + tipos; schemas; config off; reason codes; tests de contrato; budget profile.
      - SHA-256 do bloco: `9ddddf78619bd4f21719ae19961234b870516ea5a57988db0e941f4ab64aed34`
    - [SRC-S080 · L1207–L1210 · W2 — F4-S](#src-s080)
      - Caminho: TDD — FORJA-ASSINATURA > 30. Ordem de implementação e commits > W2 — F4-S
      - Assuntos: f4-s, mapa, geometria, diversidade, shadow, checkpoint
      - Trecho-guia: Mapa, geometria, diversidade, shadow e checkpoint.
      - SHA-256 do bloco: `305b2a575c073537b508acd11ae6c19ffefacd76550c5c0fe11d187db4e6e4d9`
    - [SRC-S081 · L1211–L1214 · W3 — grounding](#src-s081)
      - Caminho: TDD — FORJA-ASSINATURA > 30. Ordem de implementação e commits > W3 — grounding
      - Assuntos: grounding, integração, invalidação, fonte
      - Trecho-guia: Integração F5 e invalidação por fonte.
      - SHA-256 do bloco: `7265eae82e6cc63c978f228c99563ff929833815b541971efdf64c4aa8c0016a`
    - [SRC-S082 · L1215–L1218 · W4 — microbrief/shortlist](#src-s082)
      - Caminho: TDD — FORJA-ASSINATURA > 30. Ordem de implementação e commits > W4 — microbrief/shortlist
      - Assuntos: microbrief, shortlist, adapters, invocação, isolamento, fallback
      - Trecho-guia: Adapters de invocação, isolamento e fallback.
      - SHA-256 do bloco: `49d078042a5b864241309a20a226b82796ea6ae050f90ec109fc7c2335a4a9c6`
    - [SRC-S083 · L1219–L1222 · W5 — candidatos](#src-s083)
      - Caminho: TDD — FORJA-ASSINATURA > 30. Ordem de implementação e commits > W5 — candidatos
      - Assuntos: candidatos, materialização, candidate_0, desafiante, gate
      - Trecho-guia: Materialização de candidate0, desafiante e gate.
      - SHA-256 do bloco: `3a557f74d9417557141aeef540a765e59ebdd45fb32c2f969a4bda345e9d1e12`
    - [SRC-S084 · L1223–L1226 · W6 — blind/selection](#src-s084)
      - Caminho: TDD — FORJA-ASSINATURA > 30. Ordem de implementação e commits > W6 — blind/selection
      - Assuntos: blind, selection, primitives, n-way, modo, independência, seleção
      - Trecho-guia: Primitives N-way, modo de independência e seleção.
      - SHA-256 do bloco: `5c6dec11fe3a9c7890e9458e08cc78beae6e03b01e54dee09fc112a1fe838506`
    - [SRC-S085 · L1227–L1230 · W7 — recall/steelman](#src-s085)
      - Caminho: TDD — FORJA-ASSINATURA > 30. Ordem de implementação e commits > W7 — recall/steelman
      - Assuntos: recall, steelman, marcadores, síntese, leitor, verificador, canários
      - Trecho-guia: Marcadores de síntese, leitor/verificador e canários.
      - SHA-256 do bloco: `6fda2df149135d3cc77a5607c089ad80353e2b2ae314bd18e26b0bc38b958386`
    - [SRC-S086 · L1231–L1234 · W8 — F7/F7-B](#src-s086)
      - Caminho: TDD — FORJA-ASSINATURA > 30. Ordem de implementação e commits > W8 — F7/F7-B
      - Assuntos: f7-b, topologia, recibo, público, recomputação, package
      - Trecho-guia: Topologia, recibo público e recomputação no package.
      - SHA-256 do bloco: `55193ef2eae62fb9b0f225388c61297f6e480002d02d52ec015744fb83fb5003`
    - [SRC-S087 · L1235–L1238 · W9 — memória/AR](#src-s087)
      - Caminho: TDD — FORJA-ASSINATURA > 30. Ordem de implementação e commits > W9 — memória/AR
      - Assuntos: memória, write-only, produção, leitura, offline, indicadores
      - Trecho-guia: Write-only em produção; leitura offline; indicadores.
      - SHA-256 do bloco: `64d9b71f3016ae10a2fe13b06d636f228a6d1a6b36b8495301aa2e79feebafdc`
    - [SRC-S088 · L1239–L1242 · W10 — calibração](#src-s088)
      - Caminho: TDD — FORJA-ASSINATURA > 30. Ordem de implementação e commits > W10 — calibração
      - Assuntos: w10, calibração, manifest, amostral, julgamento, contra, pares, humanos
      - Trecho-guia: Manifest amostral e julgamento contra pares humanos.
      - SHA-256 do bloco: `5cc418f0b43278866070d01212b26a382fa1fa8739c25a03608f8e07404c8755`
    - [SRC-S089 · L1243–L1246 · W11–W13 — rollout](#src-s089)
      - Caminho: TDD — FORJA-ASSINATURA > 30. Ordem de implementação e commits > W11–W13 — rollout
      - Assuntos: w11, w13, rollout, shadow, piloto, default-on, promoção, vez
      - Trecho-guia: Shadow, piloto e default-on, uma promoção por vez.
      - SHA-256 do bloco: `45048df601f51e1a4096f6598c58a4d1687c30ec2218f56efeb9238208193635`
    - [SRC-S090 · L1247–L1259 · W14 — documentação](#src-s090)
      - Caminho: TDD — FORJA-ASSINATURA > 30. Ordem de implementação e commits > W14 — documentação
      - Assuntos: w14, documentação, manifest, contratos, catálogo, mapas, hashes, cada
      - Trecho-guia: Manifest, contratos, catálogo, mapas e hashes.
      - SHA-256 do bloco: `e443902db5df02e99989f8cd7e82fb2b10274cec3fcad12206a560a78668bd43`
  - [SRC-S091 · L1260–L1290 · 31. Comandos de verificação](#src-s091)
    - Caminho: TDD — FORJA-ASSINATURA > 31. Comandos de verificação
    - Assuntos: python, comandos, verificação, powershell, json, users, igorpc, claude
    - Trecho-guia: Documento de consulta sobre 31. Comandos de verificação.
    - SHA-256 do bloco: `fbb55a05e86bfdde996dab3f18aa80360968be88859e4de3472e7cce29e33ab6`
  - [SRC-S092 · L1291–L1310 · 32. Critério técnico de concluído](#src-s092)
    - Caminho: TDD — FORJA-ASSINATURA > 32. Critério técnico de concluído
    - Assuntos: não, critério, técnico, concluído, têm, todos, schemas, validator
    - Trecho-guia: 1. todos os schemas têm validator, owner e teste; 2. candidate0 é material e sempre recuperável; 3. piloto é condicional por caso; 4. isolamento tem evidência do orquestrador; 5. modo de julgamento real é persistido; 6. self-judge e menor SHA são impossíveis; 7. recall não vê sín
    - SHA-256 do bloco: `9f3ad1a44b38f8bfad9a71ccbeebda4fc1c49c45b6d90d35de61dea8d790c62c`

## Conteúdo integral indexado

Os marcadores HTML abaixo são apenas âncoras de navegação. O texto reproduz integralmente a origem normalizada em UTF-8; somente destinos de links relativos podem ter sido recalculados para apontar ao mesmo arquivo a partir desta pasta.

<a id="src-s001"></a>

# TDD — FORJA-ASSINATURA

> **RECLASSIFICADO EM 25/07/2026 — desenho experimental de longo prazo.**  
> O TDD vigente para execução é `planejamento/34_TDD_FORJA_ASSINATURA_LITE_COCRIACAO_PRECEDENTES.md`.

**Versão:** 1.0 revisada  
**Data:** 24/07/2026  
**Estado:** desenho técnico para implementação  
**PRD:** `planejamento/27_PRD_FORJA_ASSINATURA.md`  
**Plano:** `planejamento/26_PLANO_IMPLEMENTACAO_FORJA_ASSINATURA.md`


<a id="src-s002"></a>

## 1. Objetivo técnico

Adicionar à FORJA uma subesteira hash-bound que:

1. explora geometrias em F4-S;
2. confirma lastro em F5;
3. produz microbriefs e shortlist em F5-S;
4. materializa incumbente e desafiante em F6-A;
5. julga cegamente em F6-B;
6. promove um único `draft_markdown` em F6-C;
7. mede recall/steelman;
8. garante preservação estrutural em F7/F7-B;
9. registra decisão para análise offline sem alimentar o gerador.

Não criar nova fase canônica. F4-S, F5-S e F6-A/B/C são subestágios internos
observáveis; a tupla F0–F10 permanece.


<a id="src-s003"></a>

## 2. Restrições do sistema vivo

1. `forja_phase_contracts.py` resolve os contratos F0–F10.
2. `phase_contracts/F6.json` não possui inputs condicionais.
3. `forja_run.py` publica artefatos e recompõe gates; `exit 0` não é promoção.
4. `forja_n4_validate.py` possui `FLAG_FILES`, `VALIDATORS` e modo efetivo por
   `pilotCases`.
5. `forja_ar_blind.py` é binário; N-way exige componente novo.
6. `forja_ar_evolucao.py` usa menor SHA em desempate múltiplo; a nova camada
   não pode chamar esse caminho para decidir mérito.
7. `forja_fable5.py` valida `gostoJuridico` em função privada.
8. `forja_editorial_fidelity.py` recompõe o bundle F7-B e deve receber o
   validador público de assinatura.
9. F8 consome `final_markdown`; essa interface não muda.
10. contratos N4 e catálogo são gerados; não criar fonte paralela.


<a id="src-s004"></a>

## 3. Topologia

```text
F4 inputs
  │
  ├─ signature.snapshot ─────────────┐
  ├─ F4-S map                        │
  └─ F4-S geometries                 │
           │                         │
           ▼                         │
      F5 grounding                   │
           │                         │
           ▼                         │
   F5-S microbriefs + shortlist      │
           │                         │
           ├──────────────┐          │
           ▼              ▼          │
 candidate_0        challenger_1     │
 incumbent flow     signature flow   │
           └──────┬───────┘          │
                  ▼                  │
           legal eligibility         │
                  ▼                  │
           blind N-way judge         │
                  ▼                  │
        recall + steelman diagnostics│
                  ▼                  │
             selection              │
                  ▼                  │
       one canonical draft_markdown │
                  ▼                  │
                 F7 ── structural revalidation
                  ▼
                F7-B ── final signature fidelity
                  ▼
             final_markdown
                  ▼
                  F8
```


<a id="src-s005"></a>

## 4. Estrutura de arquivos-alvo

```text
forja/
  signature/
    __init__.py
    models.py
    contracts.py
    config.py
    snapshot.py
    geometry.py
    grounding.py
    candidates.py
    blind.py
    selection.py
    recall.py
    topology.py
    invalidation.py
    memory.py
    telemetry.py
    reason_codes.py

forja_signature.py

n4_schemas/
  f4_signature_map.schema.json
  f4_signature_geometries.schema.json
  f5_signature_shortlist.schema.json
  f6_signature_candidates.schema.json
  f6_signature_judgment.schema.json
  f6_signature_selection.schema.json
  f6_signature_recall.schema.json

tests/ ou raiz conforme padrão atual:
  test_forja_assinatura.py
  test_forja_assinatura_contracts.py
  test_forja_assinatura_blind.py
  test_forja_assinatura_integration.py
```

Compatibilidade com o layout real prevalece. Se os testes permanecerem na raiz,
não criar um segundo padrão apenas para esta feature.


<a id="src-s006"></a>

## 5. Fronteiras de responsabilidade


<a id="src-s007"></a>

### 5.1 Domínio puro

Módulos sem filesystem, subprocesso ou rede:

- `models.py`;
- `geometry.py`;
- `selection.py`;
- `topology.py`;
- `invalidation.py`;
- `reason_codes.py`.

Entradas e saídas são estruturas Python imutáveis ou cópias defensivas.


<a id="src-s008"></a>

### 5.2 Adapters

I/O e execução:

- `contracts.py`: schema/catalog;
- `config.py`: resolução de modo e budget;
- `snapshot.py`: leitura e hash;
- `grounding.py`: integração com ledgers;
- `candidates.py`: invocações isoladas;
- `blind.py`: bundles, mapping e julgadores;
- `recall.py`: invocações leitor/verificador;
- `memory.py`: append-only;
- `telemetry.py`: eventos;
- `forja_signature.py`: CLI/fachada.


<a id="src-s009"></a>

### 5.3 Integrações existentes

- F4: sidecars de mapa/geometria;
- F5: source ledger;
- F6: execução interna e um output canônico;
- F7: correção jurídica;
- F7-B: edição local e validação;
- N4: catálogo, schemas, flag e modo por caso;
- AUTO-RESEARCH: avaliação offline;
- state machine: eventos e supersession.


<a id="src-s010"></a>

## 6. Modelo de dados comum

Todo artefato:

```json
{
  "schemaVersion": 1,
  "protocolVersion": "FORJA-ASSINATURA-v1",
  "caseId": "case-...",
  "attemptId": "attempt-...",
  "generatedAt": "ISO-8601",
  "producer": {
    "component": "forja.signature...",
    "version": "..."
  },
  "inputSnapshotSha256": "64-hex",
  "configSha256": "64-hex",
  "artifactSha256": "64-hex",
  "supersedes": null
}
```

O `artifactSha256` é calculado sobre payload canônico sem o próprio campo.


<a id="src-s011"></a>

### 6.1 Enums

```text
SignatureMode =
  off | shadow | pilot_blocking | default_on

ExecutionAssurance =
  envelope_verified | orchestrator_attested | self_declared

JudgeIndependenceMode =
  cross_family | cross_session_same_family | unverified

CandidateRole =
  incumbent | challenger

CandidateStatus =
  generated | blocked | eligible | rejected | selected

SelectionStatus =
  incumbent_preserved | challenger_selected | abstained_invalid
```

Enums desconhecidos falham no schema.


<a id="src-s012"></a>

## 7. Configuração

Adicionar seção `signature` em `FORJA_N3_CONFIG.json` somente na W1, com
`mode=off`.

Campos obrigatórios:

```json
{
  "signature": {
    "protocolVersion": "FORJA-ASSINATURA-v1",
    "mode": "off",
    "pilotCases": [],
    "minGeometries": 5,
    "maxGeometries": 7,
    "microbriefCandidates": 3,
    "fullDraftCandidates": 2,
    "maxFullDraftCandidates": 3,
    "ambiguityRuleId": "signature-shortlist-margin-v1",
    "recallCardMaxWords": 80,
    "recallInputPolicy": "body_without_executive_summary",
    "judgeIndependencePolicy": "prefer_cross_family",
    "allowedDegradedJudgeMode": "cross_session_same_family",
    "rejectSelfJudge": true,
    "productionMemoryReadPolicy": "deny",
    "budgetProfileId": "signature-pilot-v1",
    "preserveIncumbentOnTie": true,
    "newPaidApiAllowed": false
  }
}
```


<a id="src-s013"></a>

### 7.1 Resolução do modo

```python
def effective_mode(configured_mode, pilot_cases, case_identity, override=None):
    if override is not None:
        return configured_mode, validate_mode(override)
    if configured_mode != "pilot_blocking":
        return configured_mode, configured_mode
    if case_identity in pilot_cases:
        return configured_mode, "pilot_blocking"
    return configured_mode, "shadow"
```

Reutilizar/refatorar o comportamento atual de
`forja_n4_validate._effective_mode()` para uma API pública comum. Não copiar a
lógica em dois módulos.


<a id="src-s014"></a>

### 7.2 Budget profile

Schema obrigatório:

```json
{
  "profileId": "signature-pilot-v1",
  "measuredAt": "ISO-8601",
  "baselineReportSha256": "64-hex",
  "maxCallsByStage": {
    "f4s": 0,
    "f5s": 0,
    "f6a": 0,
    "f6b": 0,
    "recall": 0
  },
  "maxInputTokensPerCase": 0,
  "maxOutputTokensPerCase": 0,
  "maxElapsedSecondsPerCase": 0,
  "maxJudgesPerPair": 0,
  "maxBlindComparisonsPerCase": 0,
  "maxRetriesByStage": {},
  "onExceeded": "preserve_incumbent"
}
```

Zeros acima ilustram tipos, não valores aceitos. O validador exige inteiros
positivos. W0 mede o baseline; W1 grava números e hash antes de W2.


<a id="src-s015"></a>

## 8. Snapshot


<a id="src-s016"></a>

### 8.1 Input

Referências aos artefatos canônicos, não cópias soltas.


<a id="src-s017"></a>

### 8.2 Algoritmo

1. resolver paths;
2. confirmar existência;
3. recomputar SHA-256;
4. confirmar ledger/version;
5. montar objeto com paths relativos, hashes e papéis;
6. canonicalizar JSON;
7. calcular `inputSnapshotSha256`;
8. persistir antes da primeira chamada.


<a id="src-s018"></a>

### 8.3 Proibição

Nenhum candidato, julgamento ou recall pode referir snapshot distinto no mesmo
lote. Mudança posterior cria nova tentativa.


<a id="src-s019"></a>

## 9. F4-S — mapa e geometrias


<a id="src-s020"></a>

### 9.1 `F4_SIGNATURE_MAP.json`

Campos de domínio:

```json
{
  "decisionQuestion": "...",
  "motherSentence": "...",
  "defaultVersion": "...",
  "decisiveAnchor": {
    "factIds": [],
    "sourceIds": []
  },
  "legalLimit": {
    "claimIds": [],
    "authorityIds": []
  },
  "bestCounterargument": "...",
  "demonstratedConsequence": "...",
  "requestedDisposition": "...",
  "mandatoryContentIds": [],
  "knownGapIds": []
}
```

Validações:

- strings não vazias;
- todos os IDs resolvem;
- `knownGapIds` não aparecem como fatos;
- providência pertence ao blueprint/pedidos;
- frase-mãe não adiciona certeza;
- conteúdo dos autos não é interpretado como instrução.


<a id="src-s021"></a>

### 9.2 `F4_SIGNATURE_GEOMETRIES.json`

Cada geometria:

```json
{
  "geometryId": "g-...",
  "primaryAxis": "causality",
  "coreQuestion": "...",
  "openingMove": "...",
  "argumentOrder": [
    {"position": 1, "claimIds": ["c-1"], "purpose": "..."}
  ],
  "factIds": [],
  "authorityIds": [],
  "issueIds": [],
  "counterargument": "...",
  "response": "...",
  "decisionalConsequence": "...",
  "whyNotDefault": "...",
  "groundingStatus": "pending"
}
```


<a id="src-s022"></a>

### 9.3 Diversidade determinística

Representação:

```python
signature(geometry) = (
    primary_axis,
    tuple(claim_id for step in argument_order for claim_id in step.claim_ids),
)
```

Dois candidatos são materialmente diversos quando:

1. `primaryAxis` difere; e
2. a distância normalizada de edição entre sequências de `claimIds` é maior ou
   igual ao limiar do protocolo.

O limiar é congelado no config/rubrica. Léxico ou metáfora não entram no cálculo.
Um juiz semântico pode gerar diagnóstico, mas não aprova o gate sozinho.


<a id="src-s023"></a>

## 10. F5 — grounding

Função pura:

```python
ground_geometry(geometry, source_ledger, proposition_ledger) -> GroundingResult
```

Resultado por referência:

- `resolved`;
- `missing`;
- `stale`;
- `revoked`;
- `unsupported_relation`.

Agregação:

- qualquer referência central `missing|stale|revoked` → `blocked`;
- referência periférica ausente → `partially_grounded`;
- todas válidas → `grounded`.

Não realizar busca web dentro do domínio. Pesquisa adicional retorna ao fluxo
F5 existente.


<a id="src-s024"></a>

## 11. F5-S — microbrief e shortlist


<a id="src-s025"></a>

### 11.1 Execução isolada

O orquestrador:

1. seleciona geometrias grounded;
2. monta prompt por geometria sem output irmão;
3. calcula `promptSha256`;
4. cria sessão;
5. registra envelope real ou atestação;
6. invoca;
7. persiste output antes da próxima decisão.

Retry conserva `candidateId` e incrementa `retryIndex`; não aumenta diversidade.


<a id="src-s026"></a>

### 11.2 Shortlist

Vetos primeiro. Entre elegíveis, executar comparação estrutural curta. Saída:

```json
{
  "microbriefs": [],
  "challengerRanking": [],
  "primaryChallengerGeometryId": "g-...",
  "secondaryChallengerGeometryId": "g-...",
  "ambiguity": {
    "ruleId": "signature-shortlist-margin-v1",
    "observedMargin": 0.0,
    "threshold": 0.0,
    "expand": false
  },
  "strategies": ["g-..."],
  "fallback": null,
  "abstained": false
}
```

Se nenhuma desafiante passa:

```json
{
  "strategies": [],
  "fallback": "candidate_0",
  "abstained": true,
  "reasonCode": "SIG-SHORTLIST-NO-ELIGIBLE-CHALLENGER"
}
```

O limiar vem da configuração; não é escolhido após ver os outputs.


<a id="src-s027"></a>

## 12. F6-A — candidatos


<a id="src-s028"></a>

### 12.1 `candidate_0`

Contrato:

- `candidateId = "candidate_0"`;
- `candidateRole = "incumbent"`;
- `generationMode = "incumbent_pipeline"`;
- mesmo `inputSnapshotSha256`;
- sessão própria;
- prompt incumbente atual, sem mapa/geometrias/shortlist;
- texto integral persistido antes do cegamento.


<a id="src-s029"></a>

### 12.2 Desafiante

- recebe a shortlist e ledgers por hash;
- não recebe texto do incumbente;
- não recebe memória decisória;
- preserva conteúdo obrigatório;
- produz `paragraph_provenance`.


<a id="src-s030"></a>

### 12.3 Terceiro candidato

Só existe se:

```python
expand = (
    config.expandToThirdDraftOnAmbiguity
    and shortlist.ambiguity.ruleId == config.ambiguityRuleId
    and shortlist.ambiguity.observedMargin <= shortlist.ambiguity.threshold
)
```

Não gerar terceiro draft para resolver desacordo ocorrido depois no julgamento.
Isso mudaria o orçamento com base no resultado.


<a id="src-s031"></a>

### 12.4 Manifesto

```json
{
  "candidates": [
    {
      "candidateId": "candidate_0",
      "candidateRole": "incumbent",
      "generationMode": "incumbent_pipeline",
      "geometryId": null,
      "artifactPath": "...",
      "artifactSha256": "64-hex",
      "inputSnapshotSha256": "64-hex",
      "promptSha256": "64-hex",
      "executor": {
        "family": "...",
        "model": "...",
        "sessionId": "...",
        "assurance": "orchestrator_attested"
      },
      "siblingAccess": false,
      "paragraphProvenancePath": "...",
      "status": "eligible"
    }
  ]
}
```


<a id="src-s032"></a>

## 13. Elegibilidade

`eligibility(candidate, ledgers, gates) -> EligibilityDecision`

Ordem:

1. schema e hashes;
2. snapshot;
3. proveniência;
4. fatos/números/datas;
5. autoridades;
6. pedidos/polaridade;
7. conteúdo obrigatório;
8. origem operacional;
9. injeção/vazamento;
10. estilo como sentinela.

Saída contém todos os achados; não parar no primeiro, salvo risco de segurança
que impeça leitura.


<a id="src-s033"></a>

## 14. F6-B — cegamento e julgamento


<a id="src-s034"></a>

### 14.1 Extensão, não mutação do A/B

Criar primitives N-way em `forja/signature/blind.py`. Reutilizar:

- `canonicalize`;
- `leak_scan`;
- HMAC externo;
- âncoras;
- swap;
- verificação de hashes.

Não alterar a semântica binária existente até os testes de regressão passarem.


<a id="src-s035"></a>

### 14.2 Bundles

Para cada par elegível:

- A/B;
- B/A;
- nomes opacos;
- mesmo conteúdo canonicalizado;
- mapping fora do workspace;
- commitment dentro do workspace;
- hash por bundle.


<a id="src-s036"></a>

### 14.3 Julgadores

O planner de bancada recebe famílias disponíveis e produz:

```json
{
  "requestedMode": "prefer_cross_family",
  "effectiveMode": "cross_session_same_family",
  "judges": [
    {
      "judgeId": "...",
      "family": "...",
      "sessionId": "...",
      "assurance": "orchestrator_attested",
      "promptSha256": "..."
    }
  ],
  "correlated": true
}
```

Regras:

- mesma `sessionId` de gerador e juiz → inválido;
- juiz com acesso ao mapping/workspace → inválido;
- `self_declared` em modo bloqueante → inválido;
- ausência de segunda família não é falsa falha se o modo degradado está
  permitido;
- modo degradado exige swap e prompts disjuntos.


<a id="src-s037"></a>

### 14.4 Voto

```json
{
  "pairId": "...",
  "judgeId": "...",
  "order": 1,
  "winnerPosition": "L|R|ABSTAIN",
  "anchor": "trecho literal",
  "holisticPreference": "L|R|ABSTAIN",
  "diagnostics": {
    "caseIdentity": "...",
    "decisionalClarity": "...",
    "groundedSpecificity": "...",
    "counterargumentStrength": "...",
    "economy": "...",
    "editorialHumanity": "..."
  },
  "confidenceBand": "low|medium|high"
}
```

Diagnósticos explicam; não são somados por média.


<a id="src-s038"></a>

## 15. Primitivas de seleção

Esta seção calcula elegibilidade, grafo e vencedor potencial. A função final só
é chamada em F6-C depois de os resultados de recall e steelman estarem válidos.


<a id="src-s039"></a>

### 15.1 Vetos

Remover candidatos inelegíveis.

Se `candidate_0` for inelegível, o fluxo inteiro falha juridicamente: não usar
uma desafiante editorial para encobrir falha do baseline. Retornar para a fase
que originou o veto.


<a id="src-s040"></a>

### 15.2 Matriz

Para cada par elegível, consolidar somente voto:

- válido;
- consistente sob swap;
- ancorado;
- produzido sob modo permitido.


<a id="src-s041"></a>

### 15.3 Vencedor

```python
def select(candidates, pairwise, config):
    eligible = veto_filter(candidates)
    if not eligible:
        return invalid("SIG-NO-LEGAL-CANDIDATE")

    if only_incumbent(eligible):
        return preserve_incumbent("SIG-NO-ELIGIBLE-CHALLENGER")

    stable = stable_pairwise_graph(pairwise, config)
    winner = unique_condorcet_winner(stable)

    if winner is None:
        return preserve_incumbent("SIG-ABSTAIN-CYCLE-OR-TIE")
    if winner == "candidate_0":
        return preserve_incumbent("SIG-INCUMBENT-WON")
    if not minimum_margin_met(winner, stable, config):
        return preserve_incumbent("SIG-ABSTAIN-LOW-MARGIN")
    return select_challenger(winner)
```

Nunca ordenar por SHA para mérito. SHA serve apenas para identidade e
determinismo de armazenamento.


<a id="src-s042"></a>

### 15.4 Terceiro juiz

É permitido somente se a regra já estiver no manifest:

- quais desacordos o acionam;
- limite de chamadas;
- família/sessão permitida;
- como o voto resolve;
- quando ainda deve haver abstenção.


<a id="src-s043"></a>

## 16. Recall e conclusão F6-C


<a id="src-s044"></a>

### 16.1 Remoção da síntese

F6 deve produzir marcadores canônicos de início/fim da síntese. Função:

```python
strip_executive_summary(markdown) -> body_markdown
```

Falha fechada quando:

- nenhum marcador;
- marcadores múltiplos;
- ordem inválida;
- corpo vazio;
- remoção atinge seção além da síntese.

Não usar LLM para localizar a síntese.


<a id="src-s045"></a>

### 16.2 Leitor e verificador

Sessões separadas:

- leitor: corpo → cartão;
- verificador: cartão + mapa → fidelidade.

O leitor não recebe mapa, rubrica de campos nem síntese. O verificador não
recebe a peça.


<a id="src-s046"></a>

### 16.3 Uso na seleção

- falso → elimina desafiante;
- questão/providência ausente → impede vitória;
- demais campos → diagnóstico;
- resultado não reabre candidato já inelegível;
- recall não compensa veto.


<a id="src-s047"></a>

### 16.4 Seleção final

F6-C combina a matriz válida da seção 15, recall e steelman. Só então:

1. emite `F6_SIGNATURE_SELECTION.json`;
2. altera o estado de `blind_preferred` para `selected_for_f7`;
3. promove exatamente o hash selecionado para `draft_markdown`.

Falha de recall, empate ou margem insuficiente seleciona `candidate_0`; falha
jurídica do próprio incumbente reabre a fase de origem e não é mascarada por
uma desafiante.


<a id="src-s048"></a>

## 17. Topologia de assinatura


<a id="src-s049"></a>

### 17.1 Canonicalização

```json
{
  "motherSentenceNormalized": "...",
  "sections": [
    {
      "sectionId": "...",
      "thesisId": "...",
      "claimIds": ["..."],
      "ordinal": 1
    }
  ],
  "requestedDispositionIds": [],
  "polarityVector": []
}
```

Não incluir:

- pontuação;
- fronteira de frase;
- conectivos;
- escolhas lexicais;
- tamanho de parágrafo.


<a id="src-s050"></a>

### 17.2 Comparação

Classes:

- `local_editorial_change`: passa;
- `legal_correction_nonstructural`: passa e registra;
- `structural_change`: invalida seleção;
- `request_or_polarity_change`: P0;
- `unclassifiable`: fail-closed.


<a id="src-s051"></a>

### 17.3 Integração F7-B

Extrair o validador de recibo de `forja_fable5._taste_receipt_findings()` para
API pública. `validate_editorial_bundle()` chama:

1. fidelidade existente;
2. recibo de gosto;
3. topologia de assinatura;
4. hashes de seleção;
5. policy version.

O package recompõe; não confia no relatório.


<a id="src-s052"></a>

## 18. Memória


<a id="src-s053"></a>

### 18.1 Evento

```json
{
  "decisionId": "...",
  "caseLineage": "...",
  "product": "...",
  "selectedCandidateHash": "...",
  "rejectedCandidateHashes": [],
  "reasonCodes": [],
  "anchors": [],
  "judgeIndependenceMode": "...",
  "previousDecisionId": null,
  "eventSha256": "...",
  "previousEventSha256": "..."
}
```


<a id="src-s054"></a>

### 18.2 Política de acesso

```python
def load_production_generation_context(...):
    assert config.productionMemoryReadPolicy == "deny"
    return context_without_decision_memory
```

Teste por instrumentação deve registrar os arquivos e blocos passados a cada
invocação. Regex isolada no prompt não basta; o teste compara allowlist de
inputs.

AR offline pode ler memória somente depois de formar corpus sanitizado e split.


<a id="src-s055"></a>

## 19. Invalidação

Mapa de dependências:

```text
snapshot
 ├─ map
 ├─ geometries
 ├─ grounding
 ├─ shortlist
 ├─ candidates
 ├─ judgments
 ├─ recall
 └─ selection
```

Algoritmo:

1. receber evento de mudança;
2. recomputar hash da origem;
3. localizar nós descendentes;
4. marcar `stale`, nunca apagar;
5. emitir evento append-only;
6. reabrir no primeiro subestágio afetado;
7. impedir promoção de descendente stale.


<a id="src-s056"></a>

## 20. Registro N4


<a id="src-s057"></a>

### 20.1 Catálogo

Adicionar artefatos ao `generate_n4_contracts.py`, regenerar:

- schemas;
- `ARTIFACT_CATALOG.json`;
- `phase_contracts_n4`;
- mapas derivados.

Não editar catálogo e gerador como fontes concorrentes.


<a id="src-s058"></a>

### 20.2 Flag

Feature sugerida:

```text
n4SignatureV1
```

Arquivos exigidos dependem do modo efetivo do caso. A validação deve provar:

- fora do piloto + configurado `pilot_blocking` → shadow, não bloqueia;
- dentro do piloto → arquivos e validators obrigatórios;
- `default_on` → contrato F6 formal.


<a id="src-s059"></a>

## 21. Eventos

Adicionar ao state machine apenas após contratos:

```text
signature_snapshot_created
signature_geometries_created
signature_shortlist_created
signature_candidates_materialized
signature_blind_completed
signature_recall_completed
signature_selection_decided
signature_selection_invalidated
signature_final_fidelity_validated
```

Cada evento:

- `runId`;
- `attemptId`;
- `caseId`;
- `expectedRevision`;
- `idempotencyKey`;
- `artifactHashes`;
- `previousEventHash`;
- payload versionado.


<a id="src-s060"></a>

## 22. Reason codes mínimos

```text
SIG-CONFIG-INVALID
SIG-BUDGET-PROFILE-MISSING
SIG-BUDGET-EXCEEDED
SIG-SNAPSHOT-DRIFT
SIG-GEOMETRY-NOT-DIVERSE
SIG-GEOMETRY-UNGROUNDED
SIG-SHORTLIST-NO-ELIGIBLE-CHALLENGER
SIG-CANDIDATE0-MISSING
SIG-CANDIDATE-SIBLING-LEAK
SIG-EXECUTION-UNVERIFIED
SIG-JUDGE-SELF
SIG-JUDGE-FAMILY-CORRELATED
SIG-BLIND-MAPPING-LEAK
SIG-BLIND-POSITION-BIAS
SIG-ABSTAIN-CYCLE-OR-TIE
SIG-ABSTAIN-LOW-MARGIN
SIG-INCUMBENT-WON
SIG-RECALL-SUMMARY-NOT-STRIPPED
SIG-RECALL-FALSE
SIG-TOPOLOGY-CHANGED
SIG-MEMORY-READ-DENIED
SIG-SELECTION-STALE
```

Reason code desconhecido não é aceito como texto livre em decisão.


<a id="src-s061"></a>

## 23. CLI proposta

```powershell
python forja_signature.py snapshot --case-id <id>
python forja_signature.py map --case-id <id>
python forja_signature.py ground --case-id <id>
python forja_signature.py shortlist --case-id <id>
python forja_signature.py candidates --case-id <id>
python forja_signature.py blind --case-id <id>
python forja_signature.py recall --case-id <id>
python forja_signature.py select --case-id <id>
python forja_signature.py validate --case-id <id>
python forja_signature.py status --case-id <id>
```

Toda mutação exige `--attempt-id` explícito ou resolve a tentativa viva de modo
unívoco. `status` é read-only.


<a id="src-s062"></a>

## 24. Testes


<a id="src-s063"></a>

### 24.1 Unidade

- config e modo efetivo;
- budget profile positivo;
- canonical hash;
- resolução de IDs;
- distância estrutural;
- grounding;
- expansão de terceiro draft;
- veto filter;
- Condorcet;
- ciclo/empate;
- remoção de síntese;
- topologia;
- invalidation graph;
- reason codes.


<a id="src-s064"></a>

### 24.2 Contrato

- todos os sete schemas válido/inválido;
- `candidate_0` obrigatório;
- assurance enum;
- independence enum;
- fallback de shortlist;
- decision com âncora;
- recall com hash;
- seleção com snapshot;
- artifacts no catálogo;
- gerador e derivados sem drift.


<a id="src-s065"></a>

### 24.3 Integração

1. `off` sem invocações e sem diff de output;
2. shadow produz sidecars e mantém incumbente;
3. piloto fora da lista não bloqueia;
4. piloto dentro da lista bloqueia sem artefatos;
5. baseline + desafiante → seleção;
6. abstenção → hash de `candidate_0`;
7. desafiante vence → único `draft_markdown`;
8. F7 não estrutural → seleção válida;
9. F7 estrutural → seleção stale;
10. F7-B local → `final_markdown`;
11. F7-B estrutural → bloqueio;
12. F8/package sem regressão.


<a id="src-s066"></a>

### 24.4 Metamórficos

- inverter posição;
- renomear candidato;
- trocar autor/modelo no rótulo;
- aumentar comprimento sem conteúdo;
- repetir palavras da rubrica;
- preservar palavras e mudar nexo;
- trocar nomes mantendo relações;
- remover âncora;
- retirar síntese antes do recall;
- fundir frases sem mudar topologia;
- reordenar teses mantendo vocabulário.


<a id="src-s067"></a>

### 24.5 Sabotagem

- mapping adulterado;
- mapping dentro do workspace;
- prompt irmão;
- memória decisória no prompt;
- `verified=true` sem envelope;
- mesma sessão como juiz;
- family spoofing;
- âncora inexistente;
- snapshot alterado após julgamento;
- `approved=true` sem recomputação;
- menor SHA como desempate;
- terceiro draft fora da regra;
- budget editado após resultado;
- tentativa de sair do shadow sem denominador;
- seleção histórica stale promovida.


<a id="src-s068"></a>

### 24.6 Canários de detector

- mudança de pedido;
- inversão de polaridade;
- troca de frase-mãe;
- reordenação de tese;
- remoção de conteúdo obrigatório;
- edição local legítima;
- falso positivo de fusão de frases;
- síntese não marcada;
- recall com elemento inventado.


<a id="src-s069"></a>

## 25. Matriz requisito → teste

| Requisito | Testes principais |
|---|---|
| RF-01 | modo efetivo, off, piloto dentro/fora |
| RF-02 | snapshot drift, hash chain |
| RF-03/04 | mapa, IDs, diversidade, injection |
| RF-05 | grounding e invalidação por fonte |
| RF-06 | isolamento, shortlist, fallback |
| RF-07/08 | candidate0, terceiro draft, assurance |
| RF-09 | gates jurídicos e estilo |
| RF-10/11 | HMAC, swap, família, self-judge |
| RF-12 | Condorcet, margem, empate, SHA |
| RF-13/14 | síntese removida, falso recall, steelman |
| RF-15 | único cânone e estados |
| RF-16/17 | topologia, F7/F7-B, stale |
| RF-18 | negative prompt access |
| RF-19 | budget e fallback |
| RF-20 | telemetry schema e missingness |


<a id="src-s070"></a>

## 26. Testes de promoção da política

O harness de avaliação deve pré-registrar:

- split por linhagem;
- produtos e tribunais;
- mínimo por estrato;
- margem de preferência;
- concordância;
- função sequencial de parada;
- missingness;
- budget;
- hashes de código/sensor/corpus.

Estados:

```text
technical_candidate_passed
→ independent_review_passed
→ human_promotion_approved
→ pilot_blocking
→ default_on
```

`technical_candidate_passed` requer:

- suíte e Régua;
- canários;
- zero regressão;
- ganho prospectivo sobre `candidate_0`;
- custo dentro do profile;
- rollback testado;
- nenhuma evidência stale.


<a id="src-s071"></a>

## 27. Observabilidade


<a id="src-s072"></a>

### 27.1 Eventos por caso

- tempo e tokens por estágio;
- candidatos tentados/elegíveis;
- reason codes;
- modo de independência;
- matriz pareada;
- recall;
- decisão;
- fallback;
- alterações em F7/F7-B.


<a id="src-s073"></a>

### 27.2 Agregados

Separar por:

- produto;
- tribunal;
- fase processual;
- linhagem;
- modo;
- família/modelo;
- garantia de execução.

Não publicar média global de qualidade.


<a id="src-s074"></a>

### 27.3 Alertas

- taxa de P0 > baseline;
- taxa de `unverified`;
- aumento de abstenção;
- terceiro draft acima do esperado;
- estouro de budget;
- mudança estrutural em F7/F7-B;
- recall inválido;
- regressão package/F8.

Limiares vêm do manifest de rollout.


<a id="src-s075"></a>

## 28. Desempenho e cache

Chave de cache:

```text
protocolVersion
+ componentVersion
+ inputSnapshotSha256
+ promptSha256
+ configSha256
+ modelIdentity
```

Não reutilizar cache quando:

- modelo não é verificável;
- source ledger muda;
- rubrica muda;
- prompt muda;
- candidato muda;
- schema muda.

Filtros baratos precedem LLM:

1. schema;
2. IDs;
3. hash;
4. grounding;
5. gates determinísticos;
6. só então geração/julgamento/recall.


<a id="src-s076"></a>

## 29. Segurança e privacidade

- HMAC key fora do workspace;
- mapping fora do workspace;
- logs sem conteúdo integral quando hashes bastarem;
- corpus público somente sanitizado;
- prompt injection tratada nos inputs jurídicos e nos bundles de juiz;
- nenhum segredo em telemetry;
- paths externos validados;
- nenhuma API paga nova;
- nenhum envio externo de peça.


<a id="src-s077"></a>

## 30. Ordem de implementação e commits


<a id="src-s078"></a>

### W0 — baseline

Somente medição, classificação de drift e relatório.


<a id="src-s079"></a>

### W1 — linguagem

Arquivos:

- pacote vazio + tipos;
- schemas;
- config `off`;
- reason codes;
- tests de contrato;
- budget profile.

Sem chamada a modelo.


<a id="src-s080"></a>

### W2 — F4-S

Mapa, geometria, diversidade, shadow e checkpoint.


<a id="src-s081"></a>

### W3 — grounding

Integração F5 e invalidação por fonte.


<a id="src-s082"></a>

### W4 — microbrief/shortlist

Adapters de invocação, isolamento e fallback.


<a id="src-s083"></a>

### W5 — candidatos

Materialização de `candidate_0`, desafiante e gate.


<a id="src-s084"></a>

### W6 — blind/selection

Primitives N-way, modo de independência e seleção.


<a id="src-s085"></a>

### W7 — recall/steelman

Marcadores de síntese, leitor/verificador e canários.


<a id="src-s086"></a>

### W8 — F7/F7-B

Topologia, recibo público e recomputação no package.


<a id="src-s087"></a>

### W9 — memória/AR

Write-only em produção; leitura offline; indicadores.


<a id="src-s088"></a>

### W10 — calibração

Manifest amostral e julgamento contra pares humanos.


<a id="src-s089"></a>

### W11–W13 — rollout

Shadow, piloto e default-on, uma promoção por vez.


<a id="src-s090"></a>

### W14 — documentação

Manifest, contratos, catálogo, mapas e hashes.

Cada onda:

- commit atômico;
- teste próprio;
- regressão;
- relatório;
- rollback;
- decisão de avanço.


<a id="src-s091"></a>

## 31. Comandos de verificação

```powershell
python -m pytest -q -p no:cacheprovider `
  test_forja_assinatura.py `
  test_forja_assinatura_contracts.py `
  test_forja_assinatura_blind.py `
  test_forja_assinatura_integration.py `
  test_forja_autoresearch.py `
  test_forja_fable5.py `
  test_forja_estilo_humano.py `
  test_forja_run.py `
  test_forja_anti_hallucination_v2.py `
  test_forja_n4.py `
  test_forja_pso_pet.py `
  test_forja_mutation_semantic.py

python forja_phase_contracts.py
python -m json.tool FORJA_SPEC_MANIFEST.json
python validate_forja_n3.py --real-word --run-replay
python forja_regua.py
```

Na W14:

```powershell
python "C:\Users\IgorPC\.claude\projects\00_MAPA_ARQUITETURA_IA\REGENERAR_MAPAS_ARQUITETURA.py"
python "C:\Users\IgorPC\.claude\projects\00_MAPA_ARQUITETURA_IA\APROFUNDAR_MAPAS_ARQUITETURA.py"
graphify update .
```


<a id="src-s092"></a>

## 32. Critério técnico de concluído

1. todos os schemas têm validator, owner e teste;
2. `candidate_0` é material e sempre recuperável;
3. piloto é condicional por caso;
4. isolamento tem evidência do orquestrador;
5. modo de julgamento real é persistido;
6. self-judge e menor SHA são impossíveis;
7. recall não vê síntese;
8. F7/F7-B preservam topologia ou invalidam;
9. memória não entra em geração;
10. budget degrada para incumbente;
11. F7 recebe um draft e F8 um final;
12. rollback `off` foi exercitado;
13. suíte e Régua estão verdes;
14. mapas e hashes foram regenerados;
15. promoção prospectiva satisfez os critérios do PRD.

Sem o item 15, a implementação pode ser marcada
`technical_capability_complete`, mas não `default_on_approved`.
