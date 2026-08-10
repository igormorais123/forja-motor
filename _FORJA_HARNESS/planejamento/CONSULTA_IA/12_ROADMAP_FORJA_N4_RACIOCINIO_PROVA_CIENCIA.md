# Consulta IA — ROADMAP — FORJA N4: Raciocínio, Prova e Ciência

> Cópia de consulta derivada. O documento canônico permanece no caminho de origem indicado abaixo.

## Metadados e rastreabilidade

- **Documento de origem:** `12_ROADMAP_FORJA_N4_RACIOCINIO_PROVA_CIENCIA.md`
- **Tipo:** Roadmap
- **SHA-256 da origem:** `a38536399f8a49927ce7ad8245ec35b8ff785ddb271fc7933ef470d6e29098a3`
- **Linhas da origem:** 748
- **Blocos integralmente indexados:** 79
- **Geração:** 2026-08-10T13:53:35-03:00
- **Cobertura:** 100% das linhas e do texto da origem, sem omissão.
- **Links relativos normalizados:** 0 destino(s), apenas para preservar a navegação na cópia.

## Roteiro de consulta para IA

**Síntese de localização:** Versão proposta: N4.0 Data: 2026-07-10 Status: versão final do plano de implementação; execução não iniciada Revisão do documento: final-r2, após auditoria cruzada de 2026-07-10 PRD: 10PRDFORJAN4RACIOCINIOPROVACIENCIA.md TDD: 11TDDFORJAN4RACIOCINIOPROVACIENCIA.md Diagramas: 13DIAGRAMASFORJAN4RACIOCINIOPROVACIENCIA.md

**Termos de recuperação:** não, testes, critério, rollback, caso, objetivo, pronto, base, entregáveis, escopo, criar, cobertura.

Use o índice abaixo para localizar o bloco pertinente. Cada entrada informa as linhas exatas no documento de origem. Para afirmações materiais, leia o bloco integral e confira o arquivo canônico pelo SHA-256.

## Índice detalhado e cobertura integral

- [SRC-S001 · L1–L15 · ROADMAP — FORJA N4: Raciocínio, Prova e Ciência](#src-s001)
  - Assuntos: roadmap, raciocínio, prova, ciência, versão, não, proposta, data
  - Trecho-guia: Versão proposta: N4.0 Data: 2026-07-10 Status: versão final do plano de implementação; execução não iniciada Revisão do documento: final-r2, após auditoria cruzada de 2026-07-10 PRD: 10PRDFORJAN4RACIOCINIOPROVACIENCIA.md TDD: 11TDDFORJAN4RACIOCINIOPROVACIENCIA.md Diagramas: 13DIA
  - SHA-256 do bloco: `4e9bfe3b36b609c1b7d9e014cd12589dcee976b607d3f62e29064945e09ea3e1`
  - [SRC-S002 · L16–L33 · 1. Estratégia de rollout](#src-s002)
    - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 1. Estratégia de rollout
    - Assuntos: entregar, estratégia, rollout, será, implantada, sete, marcos, comprovar
    - Trecho-guia: A N4 será implantada em sete marcos:
    - SHA-256 do bloco: `0a5e08630da7404886fd3192e58042990a241ddccf49c1f856698ba20e92f163`
  - [SRC-S003 · L34–L49 · 2. Regras de execução](#src-s003)
    - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 2. Regras de execução
    - Assuntos: não, regras, execução, marco, peça, fluxo, nenhum, altera
    - Trecho-guia: 1. Nenhum marco altera peça histórica original. 2. Todo replay trabalha sobre cópia imutável. 3. Toda nova capacidade começa com flag false. 4. Sombra produz comparação, não autoridade para bloquear o fluxo vigente. 5. Piloto bloqueante é limitado a caso explicitamente escolhido.
    - SHA-256 do bloco: `6e3aa4f48dfe0eeff2ebdc4d61ce25c1b2a1ba6899566e2c91115392af01804d`
  - [SRC-S004 · L50–L65 · 3. Dependências entre marcos](#src-s004)
    - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 3. Dependências entre marcos
    - Assuntos: dependências, marcos, promoção, text, base, núcleo, raciocínio, relações
    - Trecho-guia: M3 e M4 podem ser desenvolvidos em paralelo depois de M2, mas a promoção conjunta depende de M5 e M6.
    - SHA-256 do bloco: `3041dd59df918ed9aa8957cf6fd2c48680b04e9714589d3564ba4cd60ee9b051`
  - [SRC-S005 · L66–L67 · 4. M0 — Comprovação da base N3](#src-s005)
    - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 4. M0 — Comprovação da base N3
    - Assuntos: comprovação, base
    - Trecho-guia: Documento de consulta sobre 4. M0 — Comprovação da base N3.
    - SHA-256 do bloco: `c98a7f96c84a11fe5a3bc8a5ba09b01e20f1c0bd1905e0dadd0fae6039abb366`
    - [SRC-S006 · L68–L71 · Objetivo](#src-s006)
      - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 4. M0 — Comprovação da base N3 > Objetivo
      - Assuntos: objetivo, transformar, arquitetura, escrita, parcialmente, implementada, linha, base
      - Trecho-guia: Transformar a arquitetura N3 já escrita e parcialmente implementada em linha de base observável para a N4.
      - SHA-256 do bloco: `dc1eaf86f78fb440f5e188629643deab13299bdd20d767b8df45b8eea4d98e20`
    - [SRC-S007 · L72–L75 · Motivo](#src-s007)
      - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 4. M0 — Comprovação da base N3 > Motivo
      - Assuntos: motivo, fatos, proposições, proveniência, contexto, validado, hashes, execução
      - Trecho-guia: Sem fatos, proposições, proveniência, contexto validado, hashes e execução real, os artefatos N4 virariam uma segunda camada de planejamento sem base operacional.
      - SHA-256 do bloco: `c93f94d356dc79583dd1de6cb07acace47df195f5d0ba3f11828783aa8c9c783`
    - [SRC-S008 · L76–L106 · Escopo](#src-s008)
      - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 4. M0 — Comprovação da base N3 > Escopo
      - Assuntos: escopo, registrar, estado, gestão, real, ledger, auditoria, apenas
      - Trecho-guia: 1. registrar snapshot de: manifest; contratos F0–F10; configuração N3; 21 diretórios de estado; sidecar da gestão; testes vigentes; 2. confirmar o status real dos seis replays previstos na N3; 3. executar ciclos N3 novos em casos controlados; 4. materializar e validar: índice doc
      - SHA-256 do bloco: `7bedaf35c33f602c1d9cac9237d155333176d6af4d9a24171d31ea143bc4523e`
    - [SRC-S009 · L107–L113 · Casos mínimos](#src-s009)
      - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 4. M0 — Comprovação da base N3 > Casos mínimos
      - Assuntos: caso, casos, mínimos, responsivo, visual, law, complexo, documentos
      - Trecho-guia: um caso responsivo; um caso com visual law complexo; um caso com documentos extensos; um caso em que a integração com a gestão tenha evidência de entrega.
      - SHA-256 do bloco: `b33d8e8daec0d409111e5720f9b652ed732813de8f18c8bbf60ee1e7ac572bd4`
    - [SRC-S010 · L114–L122 · Entregáveis](#src-s010)
      - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 4. M0 — Comprovação da base N3 > Entregáveis
      - Assuntos: entregáveis, n4_m0_baseline_inventory, json, n4_m0_n3_real_cycles, corpus, imutável, fixtures, mapa
      - Trecho-guia: N4M0BASELINEINVENTORY.json; N4M0N3REALCYCLES.md; corpus imutável de fixtures; mapa de lacunas N3; plano de rollback; lista de defeitos que a N4 deve capturar.
      - SHA-256 do bloco: `abf4a07b0d933c5b41244341daef595a88a27e02458de39842a10e355d3fbc99`
    - [SRC-S011 · L123–L132 · Testes](#src-s011)
      - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 4. M0 — Comprovação da base N3 > Testes
      - Assuntos: testes, replay, reproduzível, zero, alteração, originais, hashes, coerentes
      - Trecho-guia: replay reproduzível; zero alteração em originais; hashes coerentes; sidecar idempotente; A1 aplicável materializada; F7/F8 invalidados quando o arquivo muda; links por artifactId abrindo no painel.
      - SHA-256 do bloco: `0212989440f701e7bf09ae56ddd92e590639daeea79b5980f4637ebc1d06d322`
    - [SRC-S012 · L133–L139 · Critério de pronto](#src-s012)
      - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 4. M0 — Comprovação da base N3 > Critério de pronto
      - Assuntos: critério, pronto, base, necessária, existe, artefatos, reais, lacunas
      - Trecho-guia: a base N3 necessária à N4 existe em artefatos reais; lacunas restantes estão explicitamente aceitas ou bloqueadas; o corpus tem resultados esperados verificáveis; nenhum novo módulo N4 precisa inventar uma fonte de verdade ausente.
      - SHA-256 do bloco: `9b39158a04dc0f5450e49c1d2e5d8bc1965b38e7ffea3283073de34010d55d45`
    - [SRC-S013 · L140–L145 · Rollback](#src-s013)
      - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 4. M0 — Comprovação da base N3 > Rollback
      - Assuntos: rollback, nenhuma, mudança, comportamento, deve, existir, remover, relatórios
      - Trecho-guia: Nenhuma mudança de comportamento deve existir. Remover os relatórios de comparação do caminho do runner restaura o estado anterior; os snapshots permanecem como evidência.
      - SHA-256 do bloco: `e3fa63b7046a72627440942befdbb2efc926597c00f424eafef07eea2fcb3da9`
  - [SRC-S014 · L146–L147 · 5. M1 — Núcleo de raciocínio: questões, cobertura e TDD jurídico](#src-s014)
    - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 5. M1 — Núcleo de raciocínio: questões, cobertura e TDD jurídico
    - Assuntos: núcleo, raciocínio, questões, cobertura, tdd, jurídico
    - Trecho-guia: Documento de consulta sobre 5. M1 — Núcleo de raciocínio: questões, cobertura e TDD jurídico.
    - SHA-256 do bloco: `305ca829f70d9c102d319c680f5f9ce40ad81fc4a3664a62222c1b4b668cf31c`
    - [SRC-S015 · L148–L151 · Objetivo](#src-s015)
      - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 5. M1 — Núcleo de raciocínio: questões, cobertura e TDD jurídico > Objetivo
      - Assuntos: objetivo, respondido, criar, menor, versão, útil, saber, precisa
      - Trecho-guia: Criar a menor versão útil da N4: saber o que precisa ser respondido, provar que foi respondido e testar a peça pelos critérios do próprio caso.
      - SHA-256 do bloco: `8ec03be3413c05e3b7a92817242b5b632f9637e530cb5e6fc41351f652c93deb`
    - [SRC-S016 · L152–L168 · Escopo](#src-s016)
      - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 5. M1 — Núcleo de raciocínio: questões, cobertura e TDD jurídico > Escopo
      - Assuntos: testes, escopo, cobertura, implementar, perguntas, criar, schemas, classificação
      - Trecho-guia: 1. criar schemas de: classificação N4; árvore de questões; matriz de cobertura; testes do caso; resultados dos testes; 2. implementar forjareasoning.py para perguntas e cobertura; 3. implementar forjacasetests.py; 4. integrar F2, F4, F6 e F7 em sombra; 5. gerar 20–100 perguntas c
      - SHA-256 do bloco: `f319209380c8bb8a288d2484c226767c611cbcfa17cfe0410530b82e51594122`
    - [SRC-S017 · L169–L183 · Primeiras classes de perguntas](#src-s017)
      - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 5. M1 — Núcleo de raciocínio: questões, cobertura e TDD jurídico > Primeiras classes de perguntas
      - Assuntos: primeiras, classes, perguntas, identidade, processo, partes, tribunal, prazo
      - Trecho-guia: identidade do processo, partes e tribunal; prazo e regime; fatos comprovados, declarados e inferidos; eventos processuais; pedidos próprios e adversários; resposta judicial anterior; precedentes decisivos; cálculo; objeção mais forte; fontes faltantes; visual necessário; LCI pote
      - SHA-256 do bloco: `5aa0ede589915a55699a6e9d09370ed0ac213d278e3017f5edbf5cfb539e244f`
    - [SRC-S018 · L184–L192 · Entregáveis](#src-s018)
      - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 5. M1 — Núcleo de raciocínio: questões, cobertura e TDD jurídico > Entregáveis
      - Assuntos: entregáveis, schemas, json, módulos, validadores, contratos, candidatos, substituir
      - Trecho-guia: schemas JSON v1; módulos e validadores; contratos F2/F4/F7 candidatos v2, sem substituir os vigentes; fixtures positivas e negativas; relatório sombra por caso; documentação de versionamento dos testes.
      - SHA-256 do bloco: `739d513a899482a053e6c3092bf0f4c7ab29db24b2f0240886a64c1534691407`
    - [SRC-S019 · L193–L202 · Testes essenciais](#src-s019)
      - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 5. M1 — Núcleo de raciocínio: questões, cobertura e TDD jurídico > Testes essenciais
      - Assuntos: testes, essenciais, material, questão, alterado, pedido, resposta, classificada
      - Trecho-guia: pedido material sem resposta; questão material classificada como irrelevante sem justificativa; parágrafo sem item de cobertura; teste alterado após falha; hash da peça alterado depois dos testes; questão retirada sem histórico; caso simples sem inflar perguntas.
      - SHA-256 do bloco: `b031d2a004cc423034d98121920b104af05644d4beaae119c33fbe3fe4efeee8`
    - [SRC-S020 · L203–L211 · Critério de pronto](#src-s020)
      - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 5. M1 — Núcleo de raciocínio: questões, cobertura e TDD jurídico > Critério de pronto
      - Assuntos: critério, pronto, toda, material, possui, questão, piloto, estado
      - Trecho-guia: 1. toda questão material do piloto possui estado; 2. toda alegação/pedido material possui tratamento; 3. todos os testes bloqueantes são reproduzíveis; 4. mudança de critério invalida o resultado; 5. sombra encontra pelo menos os defeitos conhecidos do corpus; 6. casos simples nã
      - SHA-256 do bloco: `ac1bc6567b01aff860088576e25b1398d9f5959af25e72df5e7d6e1129e513d7`
    - [SRC-S021 · L212–L217 · Rollback](#src-s021)
      - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 5. M1 — Núcleo de raciocínio: questões, cobertura e TDD jurídico > Rollback
      - Assuntos: rollback, desligar, n4questiontreev1, n4coveragematrixv1, n4casetestsv1, artefatos, ficam, fora
      - Trecho-guia: Desligar n4QuestionTreeV1, n4CoverageMatrixV1 e n4CaseTestsV1. Os artefatos ficam fora do caminho vigente.
      - SHA-256 do bloco: `d099a7ee170eb77db6e2658539d838750789126da04e5034b96f26a18cebeb09`
  - [SRC-S022 · L218–L219 · 6. M2 — Relações, identidade e consistência global](#src-s022)
    - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 6. M2 — Relações, identidade e consistência global
    - Assuntos: relações, identidade, consistência, global
    - Trecho-guia: Documento de consulta sobre 6. M2 — Relações, identidade e consistência global.
    - SHA-256 do bloco: `7e61120e50209e1fccaec7a828b16688d2bb94606cc69ddbe0185aff04e90d9d`
    - [SRC-S023 · L220–L223 · Objetivo](#src-s023)
      - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 6. M2 — Relações, identidade e consistência global > Objetivo
      - Assuntos: objetivo, impedir, perda, sentido, documentos, fases, versões, peça
      - Trecho-guia: Impedir perda de sentido entre documentos, fases e versões da peça.
      - SHA-256 do bloco: `1f79b438c3bf1a2c04e273b85d90f0a286f3861ab9164cb460aca771a1a2eeaf`
    - [SRC-S024 · L224–L240 · Escopo](#src-s024)
      - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 6. M2 — Relações, identidade e consistência global > Escopo
      - Assuntos: implementar, criar, escopo, próximo, mas, grafo, jurídico, leve
      - Trecho-guia: 1. implementar grafo jurídico leve sobre IDs existentes; 2. criar identidade canônica de eventos e termos; 3. comparar documentos sucessivos por unidade argumentativa; 4. mapear alcance e limite de precedentes diretos/analógicos; 5. implementar verificador intertemporal; 6. imple
      - SHA-256 do bloco: `08b19ac16e206adcfc102897cff6f53865602f13d34a746a8b229d93748261bb`
    - [SRC-S025 · L241–L251 · Entregáveis](#src-s025)
      - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 6. M2 — Relações, identidade e consistência global > Entregáveis
      - Assuntos: schema, entregáveis, forja_consistency, grafo, identidade, eventos, comparação, intertemporal
      - Trecho-guia: forjaconsistency.py; schema do grafo; schema da identidade de eventos; schema de comparação; schema intertemporal; schema de quantificação; F7 global consistency report; corpus de hard negatives.
      - SHA-256 do bloco: `f7097d979fdf859d5cdc736acf4ae0aa36420f5dc18d1efc4477629c45258be8`
    - [SRC-S026 · L252–L259 · Pilotos indicados](#src-s026)
      - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 6. M2 — Relações, identidade e consistência global > Pilotos indicados
      - Assuntos: caso, pilotos, indicados, embargos, sucessivos, peça, não, conhecimento
      - Trecho-guia: embargos sucessivos; peça em que “não conhecimento” e “rejeição” apareçam como risco; caso com precedente por analogia; caso com transição CPC/lei/regimento; caso com proveito econômico ou cálculo.
      - SHA-256 do bloco: `ff77d884ca782df2c24e91766e44a3c2dd3421bd79d47d9e027bc0015a1f7b21`
    - [SRC-S027 · L260–L270 · Testes essenciais](#src-s027)
      - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 6. M2 — Relações, identidade e consistência global > Testes essenciais
      - Assuntos: testes, essenciais, evento, idêntico, labels, incompatíveis, data, divergente
      - Trecho-guia: evento idêntico com labels incompatíveis; data divergente entre cronologia e pedido; tese subsidiária contradiz principal sem condição; precedente sustenta apenas uma subproposição; similaridade elevada tratada como triagem, não sanção; cálculo com variável sem fonte; ressalva pe
      - SHA-256 do bloco: `4778ecbb891511a6734c39a25d116e5b4b5b29338805dc1e944d6ee59b594645`
    - [SRC-S028 · L271–L280 · Critério de pronto](#src-s028)
      - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 6. M2 — Relações, identidade e consistência global > Critério de pronto
      - Assuntos: critério, pronto, zero, referência, órfã, grafo, conflito, terminológico
      - Trecho-guia: 1. zero referência órfã no grafo; 2. zero conflito terminológico material não explicado; 3. comparação documental separa repetição, novidade e possível prequestionamento; 4. precedentes têm alcance e limites registrados; 5. intertemporalidade usa ato e data comprovados; 6. quanti
      - SHA-256 do bloco: `0bfc5a05684ec3064d1979a87dbbe311cc562ca0c599871f770c2fec218331f1`
    - [SRC-S029 · L281–L286 · Rollback](#src-s029)
      - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 6. M2 — Relações, identidade e consistência global > Rollback
      - Assuntos: rollback, desligar, flags, grafo, terminologia, comparação, temporalidade, quantificação
      - Trecho-guia: Desligar flags de grafo, terminologia, comparação, temporalidade e quantificação. Nenhum ledger N3 é alterado.
      - SHA-256 do bloco: `25a58e45d79b784afba78fc3612a39cb22bf05dd0fd5274528f0a5d73d616210`
  - [SRC-S030 · L287–L288 · 7. M3 — Lastro Científico Interdisciplinar](#src-s030)
    - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 7. M3 — Lastro Científico Interdisciplinar
    - Assuntos: lastro, científico, interdisciplinar
    - Trecho-guia: Documento de consulta sobre 7. M3 — Lastro Científico Interdisciplinar.
    - SHA-256 do bloco: `3073765fd7bb07cd33cd094864765c62f1230375a674062c879b8fc689276152`
    - [SRC-S031 · L289–L292 · Objetivo](#src-s031)
      - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 7. M3 — Lastro Científico Interdisciplinar > Objetivo
      - Assuntos: objetivo, permitir, use, conhecimento, acadêmico, outras, áreas, apoio
      - Trecho-guia: Permitir que a FORJA use conhecimento acadêmico de outras áreas como apoio sério, verificável e proporcional às teses jurídicas.
      - SHA-256 do bloco: `077c87bf85819cf154f795f4eb9627473752c2c4a0d16f3e7d074d89a1b8dfe0`
    - [SRC-S032 · L293–L311 · Escopo](#src-s032)
      - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 7. M3 — Lastro Científico Interdisciplinar > Escopo
      - Assuntos: criar, escopo, busca, evidência, classificação, not_applicable, rapid, strict
      - Trecho-guia: 1. criar classificação notapplicable | rapid | strict; 2. implementar protocolo de busca; 3. criar adaptadores iniciais: Crossref; OpenAlex, quando houver chave/acesso disponível; NCBI E-utilities/PubMed/PMC; 4. permitir busca manual registrada e encadeamento de referências; 5. d
      - SHA-256 do bloco: `da98874d7713b2214c8d487654ef9f466d990c045a8feaf5af92e2d7fb7956dd`
    - [SRC-S033 · L312–L322 · Princípios de implementação](#src-s033)
      - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 7. M3 — Lastro Científico Interdisciplinar > Princípios de implementação
      - Assuntos: não, prova, princípios, implementação, modo, metadado, conteúdo, artigo
      - Trecho-guia: metadado não prova conteúdo; artigo existente não significa pertinente; revisão sistemática ruim não recebe prioridade automática; estudo populacional não prova fato individual; associação não vira causalidade; ausência em uma base não prova inexistência; evidência contrária deve
      - SHA-256 do bloco: `aae3d3effb68e109e27a7601fe5aa97949aa651aaf182b947d716fed38b665b9`
    - [SRC-S034 · L323–L329 · Primeiros domínios-piloto](#src-s034)
      - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 7. M3 — Lastro Científico Interdisciplinar > Primeiros domínios-piloto
      - Assuntos: primeiros, domínios-piloto, saúde, psicologia, comportamental, medicina, contabilidade, economia
      - Trecho-guia: 1. psicologia/saúde comportamental; 2. medicina/saúde; 3. contabilidade/economia; 4. políticas públicas ou organização, se houver caso adequado.
      - SHA-256 do bloco: `9f6849f42854ddd9f77bd84b4d54ba8b850cc997d294c03987adddd12196e1da`
    - [SRC-S035 · L330–L340 · Entregáveis](#src-s035)
      - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 7. M3 — Lastro Científico Interdisciplinar > Entregáveis
      - Assuntos: entregáveis, modelo, forja_science, adaptadores, cache, bibliográfico, schemas, f5c
      - Trecho-guia: forjascience.py; adaptadores e cache bibliográfico; schemas F5C; fixtures de fontes válidas, divergentes, corrigidas e retratadas; modelo de síntese rápida; modelo estrito; gate científico F7; integração visual para tabelas/gráficos científicos.
      - SHA-256 do bloco: `5a07f760c9534a0f13075ce71de151aa9e08ef4f9cf06df3c8483478ad53182f`
    - [SRC-S036 · L341–L356 · Testes essenciais](#src-s036)
      - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 7. M3 — Lastro Científico Interdisciplinar > Testes essenciais
      - Assuntos: artigo, testes, essenciais, resultado, tratada, doi, real, errado
      - Trecho-guia: DOI real para artigo errado; título semelhante com autores diferentes; preprint tratado como versão publicada; artigo retratado; correção relevante não considerada; estudo observacional com linguagem causal; amostra incompatível; resultado estatístico sem relevância prática; gráf
      - SHA-256 do bloco: `141b6fd11cba0d62e6bcb163ff98b6e104e61417495db50e460b6f142d5dc06b`
    - [SRC-S037 · L357–L368 · Critério de pronto](#src-s037)
      - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 7. M3 — Lastro Científico Interdisciplinar > Critério de pronto
      - Assuntos: modo, critério, pronto, todas, referências-piloto, têm, identidade, confirmada
      - Trecho-guia: 1. todas as referências-piloto têm identidade confirmada; 2. todas as frases científicas apontam para estudo e trecho/resultado adequado; 3. limites e evidência contrária estão registrados; 4. modo notapplicable funciona sem custo adicional; 5. modo rapid é reproduzível; 6. modo 
      - SHA-256 do bloco: `43351c62bf3a92c5a52bc3e357bdc531d5a6a486dd6f717cc9d71cfc8560d3b7`
    - [SRC-S038 · L369–L374 · Rollback](#src-s038)
      - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 7. M3 — Lastro Científico Interdisciplinar > Rollback
      - Assuntos: rollback, desligar, n4scienceevidencev1, remover, claims, científicos, candidatos, entrada
      - Trecho-guia: Desligar n4ScienceEvidenceV1; remover claims científicos candidatos da entrada F6; manter protocolo e ledger para auditoria.
      - SHA-256 do bloco: `1157ac90ca4f8a1d28e1d7f40d9fda3a6f5dee1d045611000273cbb8b4c99026`
  - [SRC-S039 · L375–L376 · 8. M4 — Módulos estratégicos condicionais](#src-s039)
    - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 8. M4 — Módulos estratégicos condicionais
    - Assuntos: módulos, estratégicos, condicionais
    - Trecho-guia: Documento de consulta sobre 8. M4 — Módulos estratégicos condicionais.
    - SHA-256 do bloco: `990e7f1ac8cba71771e8be221cea4301c441c66ba263fcef326b45f36638fa22`
    - [SRC-S040 · L377–L380 · Objetivo](#src-s040)
      - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 8. M4 — Módulos estratégicos condicionais > Objetivo
      - Assuntos: objetivo, integrar, técnicas, aprovadas, aumentam, visão, estratégica, obrigar
      - Trecho-guia: Integrar técnicas aprovadas que aumentam visão estratégica sem obrigar todos os casos a carregar a mesma complexidade.
      - SHA-256 do bloco: `0ff631bb9ae0d94ae6881edcc448a05ece178459b11dcc927d9bc9f8b6bea20a`
    - [SRC-S041 · L381–L382 · Módulos](#src-s041)
      - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 8. M4 — Módulos estratégicos condicionais > Módulos
      - Assuntos: módulos
      - Trecho-guia: Documento de consulta sobre Módulos.
      - SHA-256 do bloco: `396d380890733818e90af066c566f29b27c40210c00a7b086dbe331c3026f557`
      - [SRC-S042 · L383–L390 · 4A — Maturidade e contaminação de teses](#src-s042)
        - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 8. M4 — Módulos estratégicos condicionais > Módulos > 4A — Maturidade e contaminação de teses
        - Assuntos: maturidade, contaminação, teses, papel, principal, subsidiário, reserva, força
        - Trecho-guia: papel principal/subsidiário/reserva; força documental e jurídica separadas; melhor objeção; risco de contaminar tese superior; gatilho e veículo.
        - SHA-256 do bloco: `eeca308eb5e505f87d73ac3b42b0425792565b9972713ff518436f94729de48e`
      - [SRC-S043 · L391–L399 · 4B — Ledger longitudinal de condutas](#src-s043)
        - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 8. M4 — Módulos estratégicos condicionais > Módulos > 4B — Ledger longitudinal de condutas
        - Assuntos: ledger, longitudinal, condutas, dois, polos, linha, tempo, verified
        - Trecho-guia: dois polos; linha do tempo; verified | partial | notverified | contradicted; correção posterior; frase externa autorizada; integração A1 e aprovação de Cícero para acusações.
        - SHA-256 do bloco: `9e7b2103fbaf498eead2bef5bbe9e4d307f906db102f50720cbb7f0bcd466bdf`
      - [SRC-S044 · L400–L407 · 4C — Mapa de fatores decisórios](#src-s044)
        - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 8. M4 — Módulos estratégicos condicionais > Módulos > 4C — Mapa de fatores decisórios
        - Assuntos: mapa, fatores, decisórios, requisito, expresso, decisão, prova, aceita
        - Trecho-guia: requisito expresso em decisão; prova aceita/recusada; cautela; questão em aberto; consequência para a próxima peça.
        - SHA-256 do bloco: `8abecf17391d400dcf536bf6b8a95f0d7ea784219a8e56cecc4c9c1a18555ec7`
      - [SRC-S045 · L408–L416 · 4D — Composição condicional](#src-s045)
        - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 8. M4 — Módulos estratégicos condicionais > Módulos > 4D — Composição condicional
        - Assuntos: composição, condicional, interesses, não, negociáveis, concessões, gatilhos, alternativa
        - Trecho-guia: interesses; não negociáveis; concessões; gatilhos; alternativa sem acordo; faixa qualitativa, sem probabilidade inventada.
        - SHA-256 do bloco: `9a8b50bc37ecf4aec1d4d7fe3edeb10388f73538a7e89737fdfaee88759ea5fe`
    - [SRC-S046 · L417–L426 · Entregáveis](#src-s046)
      - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 8. M4 — Módulos estratégicos condicionais > Entregáveis
      - Assuntos: fixtures, entregáveis, tese, não, schemas, validadores, regras, aplicabilidade
      - Trecho-guia: schemas e validadores; regras de aplicabilidade; integração aos pareceres Helena/Cícero; fixtures de tese forte contaminada por tese fraca; fixtures de conduta não confirmada; fixtures de decisão com critério explícito; fixtures de composição não aplicável.
      - SHA-256 do bloco: `24460689a6d9b0165854aa2e6d22ea8f7f98d6c76762a55bc502028e408eaa2b`
    - [SRC-S047 · L427–L435 · Critério de pronto](#src-s047)
      - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 8. M4 — Módulos estratégicos condicionais > Critério de pronto
      - Assuntos: não, critério, pronto, módulos, aplicáveis, geram, apenas, justificativa
      - Trecho-guia: 1. módulos não aplicáveis geram apenas justificativa mínima; 2. tese fraca não é promovida por retórica; 3. conduta não verificada não é externalizada como fato; 4. mapa decisório cita decisão e localizador; 5. composição não inventa vontade, número ou probabilidade; 6. Helena e 
      - SHA-256 do bloco: `09597f3f51da7f20723659b382c5856581322a7a459ab4bc18eb394c4986041a`
    - [SRC-S048 · L436–L441 · Rollback](#src-s048)
      - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 8. M4 — Módulos estratégicos condicionais > Rollback
      - Assuntos: rollback, desligar, n4conditionalstrategyv1, blueprint, permanece, válido
      - Trecho-guia: Desligar n4ConditionalStrategyV1; blueprint N3 permanece válido.
      - SHA-256 do bloco: `0abb84375472b4503c9b71b181acac31b5f9e71a19a43fc2eb13ab3781fe5be4`
  - [SRC-S049 · L442–L443 · 9. M5 — Metacognição, aprendizado e gestão](#src-s049)
    - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 9. M5 — Metacognição, aprendizado e gestão
    - Assuntos: metacognição, aprendizado, gestão
    - Trecho-guia: Documento de consulta sobre 9. M5 — Metacognição, aprendizado e gestão.
    - SHA-256 do bloco: `648bf2627940c465d68370f73cfa31bff18066e8f46a45cf5cd6443f8f98f08a`
    - [SRC-S050 · L444–L447 · Objetivo](#src-s050)
      - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 9. M5 — Metacognição, aprendizado e gestão > Objetivo
      - Assuntos: objetivo, fechar, ciclo, produção, revisão, humana, correção, estrutural
      - Trecho-guia: Fechar o ciclo entre produção, revisão humana, correção estrutural e painel do escritório.
      - SHA-256 do bloco: `82310fa3b596cff082b9488f1f405a83b604ad2463fb3fffef227f4c52428452`
    - [SRC-S051 · L448–L470 · Escopo](#src-s051)
      - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 9. M5 — Metacognição, aprendizado e gestão > Escopo
      - Assuntos: escopo, implementar, registrar, estender, auditoria, metacognitiva, origem, premissas
      - Trecho-guia: 1. implementar auditoria metacognitiva; 2. registrar origem das premissas; 3. medir independência real das fontes de concordância; 4. registrar por que uma recomendação mudou; 5. detectar manipulação de métricas; 6. classificar diff humano por causa; 7. criar fila de propostas de
      - SHA-256 do bloco: `2adf3cd9af0c79e1c0deab675138d51b4b16b6d29df07444106e5191d273448c`
    - [SRC-S052 · L471–L482 · Entregáveis](#src-s052)
      - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 9. M5 — Metacognição, aprendizado e gestão > Entregáveis
      - Assuntos: entregáveis, extensão, json, forja_metacognition, forja_learning, classificação, diff, fila
      - Trecho-guia: forjametacognition.py; forjalearning.py; classificação do diff; fila de testes propostos; extensão de métricas; extensão idempotente do sidecar; F9DELIVERYSELECTION.json e F10DELIVERYINTEGRITY.json; componentes do painel e links por artifactId; runbook de reabertura e aprendizado
      - SHA-256 do bloco: `37698d688c11ac4481fe6ebf96f1e9e829fcc71ff1cf1d910a5620898761f8ba`
    - [SRC-S053 · L483–L494 · Testes essenciais](#src-s053)
      - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 9. M5 — Metacognição, aprendizado e gestão > Testes essenciais
      - Assuntos: testes, essenciais, fonte, três, agentes, comum, instrução, usuário
      - Trecho-guia: três agentes com uma fonte comum; instrução do usuário tratada como fato sem fonte; correção de estilo promovida indevidamente a regra jurídica; P0 escondido por 100% de cobertura numérica; refresh do painel perde estado N4; link com espaço/acento; dois casos atualizam sidecar si
      - SHA-256 do bloco: `2b49a486ced05f2e544c30b9c73522356e8a8f7f04a831ced32fa2056f5b19c4`
    - [SRC-S054 · L495–L506 · Critério de pronto](#src-s054)
      - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 9. M5 — Metacognição, aprendizado e gestão > Critério de pronto
      - Assuntos: critério, pronto, têm, premissas, origem, status, consenso, artificial
      - Trecho-guia: 1. premissas têm origem e status; 2. consenso artificial é detectado; 3. mudanças estratégicas têm causa; 4. correções humanas são classificadas; 5. nenhum aprendizado vira regra sem teste; 6. sidecar é idempotente; 7. painel mostra bloqueio acima do percentual; 8. gestão e estad
      - SHA-256 do bloco: `973023feadbddf93cb52b63ca49ce775175d16f3304b42f9cd01f732bae68f10`
    - [SRC-S055 · L507–L512 · Rollback](#src-s055)
      - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 9. M5 — Metacognição, aprendizado e gestão > Rollback
      - Assuntos: rollback, desligar, flags, metacognitiva, aprendizado, integridade, entrega, gestão
      - Trecho-guia: Desligar flags metacognitiva, aprendizado, integridade de entrega e gestão N4. O sidecar N3 continua e as propostas ficam arquivadas.
      - SHA-256 do bloco: `b0ca7098e97ae25c61aa8754205fd862042bfb5ac821dc4ebddff628b9471cf9`
  - [SRC-S056 · L513–L514 · 10. M6 — Sombra, pilotos bloqueantes e promoção](#src-s056)
    - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 10. M6 — Sombra, pilotos bloqueantes e promoção
    - Assuntos: sombra, pilotos, bloqueantes, promoção
    - Trecho-guia: Documento de consulta sobre 10. M6 — Sombra, pilotos bloqueantes e promoção.
    - SHA-256 do bloco: `6bd6f006820ffef49c87d496fb113e2274bbdbd2f299513c775b25e1da73c3e5`
    - [SRC-S057 · L515–L518 · Objetivo](#src-s057)
      - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 10. M6 — Sombra, pilotos bloqueantes e promoção > Objetivo
      - Assuntos: objetivo, provar, melhora, resultado, real, criar, regressões, burocracia
      - Trecho-guia: Provar que a N4 melhora o resultado real sem criar regressões, burocracia vazia ou falsa confiança.
      - SHA-256 do bloco: `b1b549e2e93933ed8194862115e249569740e83773ce3c9b08d0b08a45d4c430`
    - [SRC-S058 · L519–L529 · Etapa 6.1 — Replay offline](#src-s058)
      - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 10. M6 — Sombra, pilotos bloqueantes e promoção > Etapa 6.1 — Replay offline
      - Assuntos: etapa, replay, offline, medir, não, executar, corpus, completo
      - Trecho-guia: Executar o corpus completo em cópias:
      - SHA-256 do bloco: `bf855e4c5f8449dc229ec4ad99223026e9279e1dfe7c9adfb8dfe98cc24e3ecd`
    - [SRC-S059 · L530–L540 · Etapa 6.2 — Sombra em casos novos](#src-s059)
      - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 10. M6 — Sombra, pilotos bloqueantes e promoção > Etapa 6.2 — Sombra em casos novos
      - Assuntos: etapa, sombra, casos, novos, produz, relatórios, mas, fluxo
      - Trecho-guia: N4 produz relatórios, mas o fluxo vigente decide. Revisores humanos registram:
      - SHA-256 do bloco: `2191e26d99da0f7f45bf29ae5a8e47fb68bdcd8bf0d1c08fc80fb841437c9dbf`
    - [SRC-S060 · L541–L553 · Etapa 6.3 — Piloto bloqueante](#src-s060)
      - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 10. M6 — Sombra, pilotos bloqueantes e promoção > Etapa 6.3 — Piloto bloqueante
      - Assuntos: etapa, piloto, bloqueante, ativar, inicialmente, apenas, questão, material
      - Trecho-guia: 1. questão material sem resposta; 2. cobertura de pedidos; 3. identidade terminológica; 4. testes do caso; 5. citação científica inválida, quando aplicável; 6. consistência global.
      - SHA-256 do bloco: `d5972991a324520d88f6fce65502f1c64d16b9e6f3e5f3ebdcf96e161fe491b3`
    - [SRC-S061 · L554–L566 · Etapa 6.4 — Promoção gradual](#src-s061)
      - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 10. M6 — Sombra, pilotos bloqueantes e promoção > Etapa 6.4 — Promoção gradual
      - Assuntos: etapa, promoção, gradual, ordem, sugerida, árvore, questões, cobertura
      - Trecho-guia: 1. árvore de questões; 2. cobertura; 3. testes do caso; 4. terminologia e consistência; 5. comparação/intertemporal/quantificação; 6. LCI; 7. metacognição/aprendizado; 8. módulos estratégicos condicionais.
      - SHA-256 do bloco: `09ae3ec9e76c3381a3cf4aace8f41041d35701dfd8821ab5c52c2aa6a603e7b1`
    - [SRC-S062 · L567–L576 · Casos mínimos de promoção](#src-s062)
      - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 10. M6 — Sombra, pilotos bloqueantes e promoção > Casos mínimos de promoção
      - Assuntos: pelo, menos, caso, casos, mínimos, promoção, ciclos, novos
      - Trecho-guia: pelo menos um caso responsivo completo; pelo menos um caso com LCI; pelo menos um caso quantitativo; pelo menos um caso longo com visual complexo; ciclos novos suficientes para demonstrar estabilidade, além dos replays.
      - SHA-256 do bloco: `24d8eaa4716fdaf549f493af51ef9388ac6637f29b1cc5f5199ce5c33e19770e`
    - [SRC-S063 · L577–L590 · Critérios de promoção](#src-s063)
      - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 10. M6 — Sombra, pilotos bloqueantes e promoção > Critérios de promoção
      - Assuntos: promoção, hash, critérios, zero, aprovada, comprovado, conhecido, escapando
      - Trecho-guia: 1. zero P0 conhecido escapando no corpus; 2. zero regressão material em peça antes aprovada; 3. falsos positivos bloqueantes dentro do limite aprovado pelos revisores; 4. rollback comprovado; 5. todos os artefatos e hashes coerentes; 6. sidecar e painel idempotentes; 7. ganho dem
      - SHA-256 do bloco: `e2a5b3dd339c4e9b185403bb1c71898471092c9040f9063f71238d34ef456934`
    - [SRC-S064 · L591–L601 · Rollback](#src-s064)
      - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 10. M6 — Sombra, pilotos bloqueantes e promoção > Rollback
      - Assuntos: rollback, desligar, módulo, inteira, recalcular, visão, painel, preservar
      - Trecho-guia: desligar módulo ou N4 inteira; recalcular visão do painel; preservar eventos e artefatos; retomar N3/N2; abrir retrospectiva do defeito; nenhuma limpeza destrutiva.
      - SHA-256 do bloco: `2dfb43bad2ec80ba4013d8a48f62b9400963fd80daf0cc653ea0123e79ee3ca0`
  - [SRC-S065 · L602–L617 · 11. Matriz consolidada de entregas](#src-s065)
    - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 11. Matriz consolidada de entregas
    - Assuntos: não, sombra, matriz, consolidada, entregas, esforço, relativo, real
    - Trecho-guia: Esforço relativo (P/M/G) orienta priorização, não calendário: o roadmap continua sequencial por evidência.
    - SHA-256 do bloco: `fc488df9f9947a720fab3e97f496f92684e44e11819351638bbeaac8c469d275`
  - [SRC-S066 · L618–L634 · 12. Critérios de parada](#src-s066)
    - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 12. Critérios de parada
    - Assuntos: não, critérios, parada, possui, frente, deve, ser, pausada
    - Trecho-guia: Uma frente deve ser pausada quando:
    - SHA-256 do bloco: `154157d4ac38542ee449ce3d960f567375e6e6b78c2f3b9ae7fadb6dc4cb30b1`
  - [SRC-S067 · L635–L651 · 13. Backlog posterior à N4](#src-s067)
    - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 13. Backlog posterior à N4
    - Assuntos: backlog, posterior, local, eventual, somente, depois, promoção, dados
    - Trecho-guia: Somente depois da promoção e de dados reais:
    - SHA-256 do bloco: `3b935f8047a9827d8936b910ed40f6ea5620cf04d743abf9df96ccc3acf30205`
  - [SRC-S068 · L652–L670 · 14. Definition of Done geral](#src-s068)
    - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 14. Definition of Done geral
    - Assuntos: definition, done, geral, estará, implementada, não, apenas, documentada
    - Trecho-guia: A N4 estará implementada, e não apenas documentada, quando:
    - SHA-256 do bloco: `c41039f9882f62c51d73f445e0a11c80e8979658fda2c2d34db0b9c5d5ee3793`
  - [SRC-S069 · L671–L685 · 15. Fechamento dos marcos em 11/07/2026](#src-s069)
    - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 15. Fechamento dos marcos em 11/07/2026
    - Assuntos: concluído, sombra, fechamento, marcos, testes, real, correção, três
    - Trecho-guia: Documento de consulta sobre 15. Fechamento dos marcos em 11/07/2026.
    - SHA-256 do bloco: `8f2146394d5f2f58be75424e5066be35c5b6de0fe47407481c6eaa64bd42c4c8`
    - [SRC-S070 · L686–L692 · Revisão M6.4 pelo Conselho - 11/07/2026](#src-s070)
      - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 15. Fechamento dos marcos em 11/07/2026 > Revisão M6.4 pelo Conselho - 11/07/2026
      - Assuntos: pelo, conselho, três, revisão, ciclos, prospectivos, materiais, final
      - Trecho-guia: M6.4 continua pendente e ganhou critérios adicionais. Antes dos três ciclos prospectivos, o sistema deve provar: mutação semântica por famílias materiais; zero falsa aprovação P0 no corpus reservado; controles benignos com taxa de falso bloqueio publicada; pareceres Helena/Cícero
      - SHA-256 do bloco: `34d0ed29b0265a12836795b794db458bf417e08526fde5e361ff709971c9a81d`
  - [SRC-S071 · L693–L694 · 16. M6.5 — Piloto prospectivo do perfil PSO-Pet](#src-s071)
    - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 16. M6.5 — Piloto prospectivo do perfil PSO-Pet
    - Assuntos: piloto, prospectivo, perfil, pso-pet
    - Trecho-guia: Documento de consulta sobre 16. M6.5 — Piloto prospectivo do perfil PSO-Pet.
    - SHA-256 do bloco: `d8103bc0140591291014f2c2da5fd2797feddfcf870077562dbfebbd75545e53`
    - [SRC-S072 · L695–L698 · Objetivo](#src-s072)
      - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 16. M6.5 — Piloto prospectivo do perfil PSO-Pet > Objetivo
      - Assuntos: objetivo, testar, definição, explícita, problema, história, diagnóstica, comparação
      - Trecho-guia: Testar se a definição explícita do problema, a história diagnóstica, a comparação de alternativas e a validação por requisitos reduzem erro e retrabalho sem burocratizar casos simples.
      - SHA-256 do bloco: `18be663faca2e93d44e503b84a96941c033ea012dc2378008b12bd65f3f1b010`
    - [SRC-S073 · L699–L708 · Execução](#src-s073)
      - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 16. M6.5 — Piloto prospectivo do perfil PSO-Pet > Execução
      - Assuntos: execução, comparar, selecionar, três, casos, novos, leve, completo
      - Trecho-guia: 1. selecionar três casos novos: um leve, um completo e um intensivo; 2. congelar o roteiro metodológico antes da redação final; 3. manter histórico das iterações e reaberturas; 4. comparar requisitos planejados com a peça e com as revisões humanas; 5. colher decisões separadas de
      - SHA-256 do bloco: `f7ef988fbf4bf1d9b696fd1977a0bb006d0ae8c9680ea92f2c6d8f921d9f015f`
    - [SRC-S074 · L709–L717 · Critério de pronto](#src-s074)
      - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 16. M6.5 — Piloto prospectivo do perfil PSO-Pet > Critério de pronto
      - Assuntos: critério, pronto, pelo, três, execuções, prospectivas, completas, zero
      - Trecho-guia: três execuções prospectivas completas; zero falsa alegação de preenchimento anterior à redação; alternativa real examinada nos perfis completo e intensivo; utilidade reconhecida pelo conselho sem P0 novo causado pelo método; perfil leve sem aumento material injustificado de tempo
      - SHA-256 do bloco: `9737dc550ff6fa0e0d52dfd75da9b3b37cbfcfe98f6020a641baca9d3e664f19`
    - [SRC-S075 · L718–L723 · Rollback](#src-s075)
      - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 16. M6.5 — Piloto prospectivo do perfil PSO-Pet > Rollback
      - Assuntos: rollback, remover, exigência, roteiro, casos, seguintes, preservando, três
      - Trecho-guia: Remover a exigência do roteiro nos casos seguintes, preservando os três pilotos para análise. Nenhum artefato N2/N3/N4 existente é apagado ou reclassificado.
      - SHA-256 do bloco: `ee1384b9612a40391a9373bb482c31a84cea832d57b04c6057827000768e3fa1`
  - [SRC-S076 · L724–L727 · 17. Trilha de compatibilidade obrigatória — F7-B vigente (adendo de 15/07/2026)](#src-s076)
    - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 17. Trilha de compatibilidade obrigatória — F7-B vigente (adendo de 15/07/2026)
    - Assuntos: f7-b, adendo, trilha, compatibilidade, obrigatória, vigente, este, não
    - Trecho-guia: Este adendo não altera os sete marcos históricos nem afirma que a N4 foi promovida. Ele acrescenta uma condição de integração: qualquer marco que toque F7, F8, pacote ou replay deve preservar o F7-B implementado na base.
    - SHA-256 do bloco: `a56ad619c1355a1bdf50bacd31d111a07df80fc17e20f6643ce2fa2c26efc57d`
    - [SRC-S077 · L728–L737 · Trabalho necessário em cada marco afetado](#src-s077)
      - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 17. Trilha de compatibilidade obrigatória — F7-B vigente (adendo de 15/07/2026) > Trabalho necessário em cada marco afetado
      - Assuntos: devem, deve, trabalho, necessário, cada, marco, afetado, audited_markdown
      - Trecho-guia: 1. fixtures e replays devem produzir auditedmarkdown, passar F7 com zero P0 e então acionar forjafable5.py explicitamente; não se deve pressupor chamada automática por forjarun.py; 2. a infraestrutura de teste deve comprovar Claude Code em OAuth Claude Max e modelo claude-fable-5
      - SHA-256 do bloco: `25c9640c573d9a9870ace1b78c0cb944ef3b6c8f4d1da399d7d88c15e479e666`
    - [SRC-S078 · L738–L745 · Critério de pronto adicional](#src-s078)
      - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 17. Trilha de compatibilidade obrigatória — F7-B vigente (adendo de 15/07/2026) > Critério de pronto adicional
      - Assuntos: zero, critério, pronto, adicional, contador, promoção, fragmento, isolado
      - Trecho-guia: zero promoção de fragmento isolado; zero pacote novo baseado apenas em auditedmarkdown; zero relaxamento dos limites semânticos pela N4; replays distinguem corretamente o contador editorial interno do contador da fase; falha de OAuth/modelo ou esgotamento das três candidatas bloq
      - SHA-256 do bloco: `3a8c23a4a6f4133aeb35e3b879e6474ffb953f0f877f77645ed38deca831629b`
    - [SRC-S079 · L746–L748 · Rollback](#src-s079)
      - Caminho: ROADMAP — FORJA N4: Raciocínio, Prova e Ciência > 17. Trilha de compatibilidade obrigatória — F7-B vigente (adendo de 15/07/2026) > Rollback
      - Assuntos: rollback, desligar, funcionalidades, candidatas, continua, sendo, f7-b, pertence
      - Trecho-guia: Desligar funcionalidades candidatas N4 continua sendo o rollback da N4. O F7-B pertence à base vigente e não é removido por esse rollback; eventual retorno dele exige decisão normativa separada, mantendo os bundles já produzidos como evidência histórica.
      - SHA-256 do bloco: `47afc50e32e79f26c0da13b999bef2dad361af32f37c596338ec8cbc0a0f5ef2`

## Conteúdo integral indexado

Os marcadores HTML abaixo são apenas âncoras de navegação. O texto reproduz integralmente a origem normalizada em UTF-8; somente destinos de links relativos podem ter sido recalculados para apontar ao mesmo arquivo a partir desta pasta.

<a id="src-s001"></a>

# ROADMAP — FORJA N4: Raciocínio, Prova e Ciência

**Versão proposta:** N4.0  
**Data:** 2026-07-10  
**Status:** versão final do plano de implementação; execução não iniciada  
**Revisão do documento:** final-r2, após auditoria cruzada de 2026-07-10  
**PRD:** `10_PRD_FORJA_N4_RACIOCINIO_PROVA_CIENCIA.md`  
**TDD:** `11_TDD_FORJA_N4_RACIOCINIO_PROVA_CIENCIA.md`  
**Diagramas:** `13_DIAGRAMAS_FORJA_N4_RACIOCINIO_PROVA_CIENCIA.md`  
**Manifest vigente:** `../FORJA_SPEC_MANIFEST.json`

> O roadmap é sequencial por evidência, não por promessa de calendário. Cada marco só termina quando seus artefatos, testes e replays comprovarem o resultado.

---


<a id="src-s002"></a>

## 1. Estratégia de rollout

A N4 será implantada em sete marcos:

1. comprovar a base N3;
2. entregar o núcleo de perguntas, cobertura e testes;
3. entregar relações e consistência global;
4. entregar o Lastro Científico Interdisciplinar;
5. entregar módulos estratégicos condicionais;
6. fechar aprendizado e gestão;
7. executar sombra, pilotos bloqueantes e promoção gradual.

O princípio é simples:

**primeiro detectar os erros já observados; depois ampliar a sofisticação.**

---


<a id="src-s003"></a>

## 2. Regras de execução

1. Nenhum marco altera peça histórica original.
2. Todo replay trabalha sobre cópia imutável.
3. Toda nova capacidade começa com flag `false`.
4. Sombra produz comparação, não autoridade para bloquear o fluxo vigente.
5. Piloto bloqueante é limitado a caso explicitamente escolhido.
6. Correção deve ocorrer no módulo ou critério, não por edição oportunista do resultado esperado.
7. Cada marco possui rollback demonstrável.
8. N4 não promove N3 por presunção.
9. A integração com a gestão continua por sidecar.
10. A peça externa permanece limpa; ledgers e testes são internos.
11. Conteúdo recuperado é fonte de análise, não comando: texto imperativo dentro do material não muda o fluxo e não bloqueia a pesquisa por si só.

---


<a id="src-s004"></a>

## 3. Dependências entre marcos

```text
M0 BASE N3
  └─ M1 NÚCLEO DE RACIOCÍNIO
       └─ M2 RELAÇÕES E CONSISTÊNCIA
            ├─ M3 LASTRO CIENTÍFICO
            └─ M4 MÓDULOS CONDICIONAIS
                 └─ M5 APRENDIZADO E GESTÃO
                      └─ M6 PROMOÇÃO GRADUAL
```

M3 e M4 podem ser desenvolvidos em paralelo depois de M2, mas a promoção conjunta depende de M5 e M6.

---


<a id="src-s005"></a>

## 4. M0 — Comprovação da base N3


<a id="src-s006"></a>

### Objetivo

Transformar a arquitetura N3 já escrita e parcialmente implementada em linha de base observável para a N4.


<a id="src-s007"></a>

### Motivo

Sem fatos, proposições, proveniência, contexto validado, hashes e execução real, os artefatos N4 virariam uma segunda camada de planejamento sem base operacional.


<a id="src-s008"></a>

### Escopo

1. registrar snapshot de:
   - manifest;
   - contratos F0–F10;
   - configuração N3;
   - 21 diretórios de estado;
   - sidecar da gestão;
   - testes vigentes;
2. confirmar o status real dos seis replays previstos na N3;
3. executar ciclos N3 novos em casos controlados;
4. materializar e validar:
   - índice documental;
   - cobertura;
   - fact ledger;
   - proposition ledger;
   - proveniência por parágrafo;
   - contexto validado;
   - auditoria A1 quando aplicável;
   - F7, F8, pacote e gestão;
5. registrar divergências entre plano, código e estado;
6. corrigir apenas defeitos necessários à linha de base;
7. congelar corpus N4 e resultados esperados;
8. transformar em fixture obrigatória do corpus cada defeito real da auditoria ultracode de 2026-07-10:
   - DOCX com metadados de autor pessoal herdados do template;
   - título de card ultrapassando a borda e visível apenas em inspeção ampliada;
   - registro de hashes divergente dos arquivos em disco;
   - versão anterior à auditada expedida ao revisor humano;
   - verificador com regra normativa invertida apesar de execução determinística;
9. transformar o falso positivo das margens visual law em teste de não regressão: perfil visual aprovado não pode ser reprovado pelo padrão Word ordinário.


<a id="src-s009"></a>

### Casos mínimos

- um caso responsivo;
- um caso com visual law complexo;
- um caso com documentos extensos;
- um caso em que a integração com a gestão tenha evidência de entrega.


<a id="src-s010"></a>

### Entregáveis

- `N4_M0_BASELINE_INVENTORY.json`;
- `N4_M0_N3_REAL_CYCLES.md`;
- corpus imutável de fixtures;
- mapa de lacunas N3;
- plano de rollback;
- lista de defeitos que a N4 deve capturar.


<a id="src-s011"></a>

### Testes

- replay reproduzível;
- zero alteração em originais;
- hashes coerentes;
- sidecar idempotente;
- A1 aplicável materializada;
- F7/F8 invalidados quando o arquivo muda;
- links por `artifactId` abrindo no painel.


<a id="src-s012"></a>

### Critério de pronto

- a base N3 necessária à N4 existe em artefatos reais;
- lacunas restantes estão explicitamente aceitas ou bloqueadas;
- o corpus tem resultados esperados verificáveis;
- nenhum novo módulo N4 precisa inventar uma fonte de verdade ausente.


<a id="src-s013"></a>

### Rollback

Nenhuma mudança de comportamento deve existir. Remover os relatórios de comparação do caminho do runner restaura o estado anterior; os snapshots permanecem como evidência.

---


<a id="src-s014"></a>

## 5. M1 — Núcleo de raciocínio: questões, cobertura e TDD jurídico


<a id="src-s015"></a>

### Objetivo

Criar a menor versão útil da N4: saber o que precisa ser respondido, provar que foi respondido e testar a peça pelos critérios do próprio caso.


<a id="src-s016"></a>

### Escopo

1. criar schemas de:
   - classificação N4;
   - árvore de questões;
   - matriz de cobertura;
   - testes do caso;
   - resultados dos testes;
2. implementar `forja_reasoning.py` para perguntas e cobertura;
3. implementar `forja_case_tests.py`;
4. integrar F2, F4, F6 e F7 em sombra;
5. gerar 20–100 perguntas conforme complexidade, sem preenchimento artificial;
6. ligar pedidos, alegações, omissões e decisões a parágrafos da minuta;
7. congelar 10–25 testes antes da versão final;
8. impedir alteração silenciosa do teste;
9. registrar bloqueios materiais no sidecar temporário.


<a id="src-s017"></a>

### Primeiras classes de perguntas

- identidade do processo, partes e tribunal;
- prazo e regime;
- fatos comprovados, declarados e inferidos;
- eventos processuais;
- pedidos próprios e adversários;
- resposta judicial anterior;
- precedentes decisivos;
- cálculo;
- objeção mais forte;
- fontes faltantes;
- visual necessário;
- LCI potencial.


<a id="src-s018"></a>

### Entregáveis

- schemas JSON v1;
- módulos e validadores;
- contratos F2/F4/F7 candidatos v2, sem substituir os vigentes;
- fixtures positivas e negativas;
- relatório sombra por caso;
- documentação de versionamento dos testes.


<a id="src-s019"></a>

### Testes essenciais

- pedido material sem resposta;
- questão material classificada como irrelevante sem justificativa;
- parágrafo sem item de cobertura;
- teste alterado após falha;
- hash da peça alterado depois dos testes;
- questão retirada sem histórico;
- caso simples sem inflar perguntas.


<a id="src-s020"></a>

### Critério de pronto

1. toda questão material do piloto possui estado;
2. toda alegação/pedido material possui tratamento;
3. todos os testes bloqueantes são reproduzíveis;
4. mudança de critério invalida o resultado;
5. sombra encontra pelo menos os defeitos conhecidos do corpus;
6. casos simples não sofrem regressão de fluxo.


<a id="src-s021"></a>

### Rollback

Desligar `n4QuestionTreeV1`, `n4CoverageMatrixV1` e `n4CaseTestsV1`. Os artefatos ficam fora do caminho vigente.

---


<a id="src-s022"></a>

## 6. M2 — Relações, identidade e consistência global


<a id="src-s023"></a>

### Objetivo

Impedir perda de sentido entre documentos, fases e versões da peça.


<a id="src-s024"></a>

### Escopo

1. implementar grafo jurídico leve sobre IDs existentes;
2. criar identidade canônica de eventos e termos;
3. comparar documentos sucessivos por unidade argumentativa;
4. mapear alcance e limite de precedentes diretos/analógicos;
5. implementar verificador intertemporal;
6. implementar cenários objetivos de quantificação;
7. criar auditoria global F7;
8. integrar texto, quadros, diagramas, pedidos, relatório e e-mail;
9. criar hard negatives:
   - termo próximo, mas processualmente diferente;
   - precedente semanticamente próximo, mas juridicamente insuficiente;
   - DOI real de artigo incorreto;
   - argumento repetido com novidade material;
   - valor correto com data-base errada.


<a id="src-s025"></a>

### Entregáveis

- `forja_consistency.py`;
- schema do grafo;
- schema da identidade de eventos;
- schema de comparação;
- schema intertemporal;
- schema de quantificação;
- F7 global consistency report;
- corpus de hard negatives.


<a id="src-s026"></a>

### Pilotos indicados

- embargos sucessivos;
- peça em que “não conhecimento” e “rejeição” apareçam como risco;
- caso com precedente por analogia;
- caso com transição CPC/lei/regimento;
- caso com proveito econômico ou cálculo.


<a id="src-s027"></a>

### Testes essenciais

- evento idêntico com labels incompatíveis;
- data divergente entre cronologia e pedido;
- tese subsidiária contradiz principal sem condição;
- precedente sustenta apenas uma subproposição;
- similaridade elevada tratada como triagem, não sanção;
- cálculo com variável sem fonte;
- ressalva perdida em tabela ou diagrama;
- e-mail declara “tudo conferido” com P0.


<a id="src-s028"></a>

### Critério de pronto

1. zero referência órfã no grafo;
2. zero conflito terminológico material não explicado;
3. comparação documental separa repetição, novidade e possível prequestionamento;
4. precedentes têm alcance e limites registrados;
5. intertemporalidade usa ato e data comprovados;
6. quantificação é reproduzível ou declara impossibilidade;
7. consistência global detecta divergências entre todos os formatos.


<a id="src-s029"></a>

### Rollback

Desligar flags de grafo, terminologia, comparação, temporalidade e quantificação. Nenhum ledger N3 é alterado.

---


<a id="src-s030"></a>

## 7. M3 — Lastro Científico Interdisciplinar


<a id="src-s031"></a>

### Objetivo

Permitir que a FORJA use conhecimento acadêmico de outras áreas como apoio sério, verificável e proporcional às teses jurídicas.


<a id="src-s032"></a>

### Escopo

1. criar classificação `not_applicable | rapid | strict`;
2. implementar protocolo de busca;
3. criar adaptadores iniciais:
   - Crossref;
   - OpenAlex, quando houver chave/acesso disponível;
   - NCBI E-utilities/PubMed/PMC;
4. permitir busca manual registrada e encadeamento de referências;
5. deduplicar por DOI, PMID, título, autoria e ano;
6. verificar versão, revisão por pares e estado editorial;
7. criar ficha de estudo;
8. avaliar método por disciplina e proposição;
9. buscar evidência contrária;
10. criar síntese e mapa claim→evidência;
11. integrar citações científicas à proveniência do parágrafo;
12. auditar gráficos, tabelas e linguagem causal;
13. produzir relatório interno e citação externa limpa.


<a id="src-s033"></a>

### Princípios de implementação

- metadado não prova conteúdo;
- artigo existente não significa pertinente;
- revisão sistemática ruim não recebe prioridade automática;
- estudo populacional não prova fato individual;
- associação não vira causalidade;
- ausência em uma base não prova inexistência;
- evidência contrária deve aparecer na síntese;
- PRISMA é referência de transparência no modo estrito, não ritual obrigatório no modo rápido.


<a id="src-s034"></a>

### Primeiros domínios-piloto

1. psicologia/saúde comportamental;
2. medicina/saúde;
3. contabilidade/economia;
4. políticas públicas ou organização, se houver caso adequado.


<a id="src-s035"></a>

### Entregáveis

- `forja_science.py`;
- adaptadores e cache bibliográfico;
- schemas F5C;
- fixtures de fontes válidas, divergentes, corrigidas e retratadas;
- modelo de síntese rápida;
- modelo estrito;
- gate científico F7;
- integração visual para tabelas/gráficos científicos.


<a id="src-s036"></a>

### Testes essenciais

- DOI real para artigo errado;
- título semelhante com autores diferentes;
- preprint tratado como versão publicada;
- artigo retratado;
- correção relevante não considerada;
- estudo observacional com linguagem causal;
- amostra incompatível;
- resultado estatístico sem relevância prática;
- gráfico com eixo ou unidade alterados;
- evidência mista apresentada como consenso;
- ausência em OpenAlex tratada indevidamente como inexistência;
- base indisponível tratada como resultado negativo;
- artigo que estuda prompt injection contém texto imperativo e é falsamente bloqueado em vez de ser analisado como fonte.


<a id="src-s037"></a>

### Critério de pronto

1. todas as referências-piloto têm identidade confirmada;
2. todas as frases científicas apontam para estudo e trecho/resultado adequado;
3. limites e evidência contrária estão registrados;
4. modo `not_applicable` funciona sem custo adicional;
5. modo `rapid` é reproduzível;
6. modo `strict` registra seleção e exclusões;
7. nenhum P0 científico do corpus passa;
8. falha de API degrada explicitamente sem falsa conclusão;
9. texto imperativo em fonte acadêmica não altera o fluxo nem produz falso bloqueio; anomalia técnica real continua registrada pelo scanner existente.


<a id="src-s038"></a>

### Rollback

Desligar `n4ScienceEvidenceV1`; remover claims científicos candidatos da entrada F6; manter protocolo e ledger para auditoria.

---


<a id="src-s039"></a>

## 8. M4 — Módulos estratégicos condicionais


<a id="src-s040"></a>

### Objetivo

Integrar técnicas aprovadas que aumentam visão estratégica sem obrigar todos os casos a carregar a mesma complexidade.


<a id="src-s041"></a>

### Módulos


<a id="src-s042"></a>

#### 4A — Maturidade e contaminação de teses

- papel principal/subsidiário/reserva;
- força documental e jurídica separadas;
- melhor objeção;
- risco de contaminar tese superior;
- gatilho e veículo.


<a id="src-s043"></a>

#### 4B — Ledger longitudinal de condutas

- dois polos;
- linha do tempo;
- `verified | partial | not_verified | contradicted`;
- correção posterior;
- frase externa autorizada;
- integração A1 e aprovação de Cícero para acusações.


<a id="src-s044"></a>

#### 4C — Mapa de fatores decisórios

- requisito expresso em decisão;
- prova aceita/recusada;
- cautela;
- questão em aberto;
- consequência para a próxima peça.


<a id="src-s045"></a>

#### 4D — Composição condicional

- interesses;
- não negociáveis;
- concessões;
- gatilhos;
- alternativa sem acordo;
- faixa qualitativa, sem probabilidade inventada.


<a id="src-s046"></a>

### Entregáveis

- schemas e validadores;
- regras de aplicabilidade;
- integração aos pareceres Helena/Cícero;
- fixtures de tese forte contaminada por tese fraca;
- fixtures de conduta não confirmada;
- fixtures de decisão com critério explícito;
- fixtures de composição não aplicável.


<a id="src-s047"></a>

### Critério de pronto

1. módulos não aplicáveis geram apenas justificativa mínima;
2. tese fraca não é promovida por retórica;
3. conduta não verificada não é externalizada como fato;
4. mapa decisório cita decisão e localizador;
5. composição não inventa vontade, número ou probabilidade;
6. Helena e Cícero registram decisões materiais e divergências.


<a id="src-s048"></a>

### Rollback

Desligar `n4ConditionalStrategyV1`; blueprint N3 permanece válido.

---


<a id="src-s049"></a>

## 9. M5 — Metacognição, aprendizado e gestão


<a id="src-s050"></a>

### Objetivo

Fechar o ciclo entre produção, revisão humana, correção estrutural e painel do escritório.


<a id="src-s051"></a>

### Escopo

1. implementar auditoria metacognitiva;
2. registrar origem das premissas;
3. medir independência real das fontes de concordância;
4. registrar por que uma recomendação mudou;
5. detectar manipulação de métricas;
6. classificar diff humano por causa;
7. criar fila de propostas de regressão;
8. exigir aprovação antes de transformar proposta em gate;
9. estender telemetria;
10. estender sidecar N4;
11. mostrar no painel:
   - N4 desligada/sombra/piloto;
   - cobertura material;
   - testes pendentes;
   - modo e estado LCI;
   - bloqueios;
   - próximo passo;
   - artefatos;
12. preservar regra de que rascunho não conclui demanda;
13. implementar a seleção pré-envio e a confirmação pós-entrega nos dois modos previstos pelo canal.


<a id="src-s052"></a>

### Entregáveis

- `forja_metacognition.py`;
- `forja_learning.py`;
- classificação do diff;
- fila de testes propostos;
- extensão de métricas;
- extensão idempotente do sidecar;
- `F9_DELIVERY_SELECTION.json` e `F10_DELIVERY_INTEGRITY.json`;
- componentes do painel e links por `artifactId`;
- runbook de reabertura e aprendizado.


<a id="src-s053"></a>

### Testes essenciais

- três agentes com uma fonte comum;
- instrução do usuário tratada como fato sem fonte;
- correção de estilo promovida indevidamente a regra jurídica;
- P0 escondido por 100% de cobertura numérica;
- refresh do painel perde estado N4;
- link com espaço/acento;
- dois casos atualizam sidecar simultaneamente;
- canal sem acesso ao anexo pós-envio confirma a entrega pela cadeia alternativa sem falso bloqueio;
- erro estrutural vira teste e impede reincidência.


<a id="src-s054"></a>

### Critério de pronto

1. premissas têm origem e status;
2. consenso artificial é detectado;
3. mudanças estratégicas têm causa;
4. correções humanas são classificadas;
5. nenhum aprendizado vira regra sem teste;
6. sidecar é idempotente;
7. painel mostra bloqueio acima do percentual;
8. gestão e estado canônico não divergem;
9. versão entregue está ligada ao pacote por uma das duas cadeias válidas de evidência.


<a id="src-s055"></a>

### Rollback

Desligar flags metacognitiva, aprendizado, integridade de entrega e gestão N4. O sidecar N3 continua e as propostas ficam arquivadas.

---


<a id="src-s056"></a>

## 10. M6 — Sombra, pilotos bloqueantes e promoção


<a id="src-s057"></a>

### Objetivo

Provar que a N4 melhora o resultado real sem criar regressões, burocracia vazia ou falsa confiança.


<a id="src-s058"></a>

### Etapa 6.1 — Replay offline

Executar o corpus completo em cópias:

- comparar N3 versus N4;
- medir defeitos adicionais encontrados;
- medir falsos positivos;
- verificar tempo e volume de artefatos;
- eliminar perguntas e campos que não gerem decisão útil;
- corrigir módulo, não a história do caso.


<a id="src-s059"></a>

### Etapa 6.2 — Sombra em casos novos

N4 produz relatórios, mas o fluxo vigente decide. Revisores humanos registram:

- achado correto;
- falso positivo;
- omissão;
- impacto real na peça;
- custo de revisão;
- módulo responsável.


<a id="src-s060"></a>

### Etapa 6.3 — Piloto bloqueante

Ativar inicialmente apenas:

1. questão material sem resposta;
2. cobertura de pedidos;
3. identidade terminológica;
4. testes do caso;
5. citação científica inválida, quando aplicável;
6. consistência global.

Módulos estratégicos permanecem consultivos até acumularem evidência.


<a id="src-s061"></a>

### Etapa 6.4 — Promoção gradual

Ordem sugerida:

1. árvore de questões;
2. cobertura;
3. testes do caso;
4. terminologia e consistência;
5. comparação/intertemporal/quantificação;
6. LCI;
7. metacognição/aprendizado;
8. módulos estratégicos condicionais.


<a id="src-s062"></a>

### Casos mínimos de promoção

- pelo menos um caso responsivo completo;
- pelo menos um caso com LCI;
- pelo menos um caso quantitativo;
- pelo menos um caso longo com visual complexo;
- ciclos novos suficientes para demonstrar estabilidade, além dos replays.

O número final deve ser definido no relatório M6 com base na variedade e nos defeitos observados, sem reduzir o piso de três ciclos novos estáveis já exigido pelo manifest para a candidata N3.


<a id="src-s063"></a>

### Critérios de promoção

1. zero P0 conhecido escapando no corpus;
2. zero regressão material em peça antes aprovada;
3. falsos positivos bloqueantes dentro do limite aprovado pelos revisores;
4. rollback comprovado;
5. todos os artefatos e hashes coerentes;
6. sidecar e painel idempotentes;
7. ganho demonstrado em cobertura, coerência ou detecção;
8. nenhum módulo obrigatório sem utilidade comprovada;
9. documentação e contratos correspondem ao código;
10. gate de expedição comprovado: hash do arquivo selecionado igual ao pacote auditado e registro reconciliado; após o envio, hash real quando o canal o fornecer ou `artifactId` + hash pré-envio + evidência externa nos demais canais;
11. promoção aprovada e manifest atualizado em operação única.


<a id="src-s064"></a>

### Rollback

- desligar módulo ou N4 inteira;
- recalcular visão do painel;
- preservar eventos e artefatos;
- retomar N3/N2;
- abrir retrospectiva do defeito;
- nenhuma limpeza destrutiva.

---


<a id="src-s065"></a>

## 11. Matriz consolidada de entregas

| Marco | Resultado principal | Bloqueia produção vigente? | Dependência | Esforço relativo |
|---|---|---:|---|---|
| M0 | baseline N3 real | não | manifest/N3 | M — depende do estado real dos 21 casos |
| M1 | perguntas, cobertura e testes | não, em sombra | M0 | G — núcleo da N4 |
| M2 | relações e consistência | não, em sombra | M1 | G — maior superfície de validação |
| M3 | LCI | não, em sombra | M2 | G — adaptadores externos e validação científica |
| M4 | estratégia condicional | não, em sombra | M2 | M — schemas e regras de aplicabilidade |
| M5 | metacognição, aprendizado e gestão | não, em sombra | M3/M4 | M — integra o que já existe |
| M6 | piloto e promoção | apenas casos escolhidos | M0–M5 | M — execução e medição, pouco código novo |

Esforço relativo (P/M/G) orienta priorização, não calendário: o roadmap continua sequencial por evidência.

---


<a id="src-s066"></a>

## 12. Critérios de parada

Uma frente deve ser pausada quando:

- duplica artefato N3 sem ganho;
- cria mais revisão manual do que defeitos reais detectados;
- depende de dado que a FORJA não possui;
- produz falso positivo bloqueante recorrente;
- não possui fixture reproduzível;
- exige infraestrutura nova sem benefício demonstrado;
- altera fonte canônica para fazer o teste passar;
- enfraquece visual, prazo ou gestão já estáveis.

Pausa não cancela o roadmap inteiro. Isola-se o módulo e preserva-se o núcleo útil.

---


<a id="src-s067"></a>

## 13. Backlog posterior à N4

Somente depois da promoção e de dados reais:

- busca científica monitorada por tema;
- banco local de fontes acadêmicas validadas;
- expansão para bases disciplinares específicas;
- recomendação automática de novos hard negatives;
- avaliações comparativas de modelos por tarefa;
- eventual indexação semântica local;
- eventual treinamento comportamental sobre corpus classificado;
- geração assistida de revisão sistemática formal.

Nenhum desses itens é requisito para a N4.

---


<a id="src-s068"></a>

## 14. Definition of Done geral

A N4 estará implementada, e não apenas documentada, quando:

- a linha de base N3 estiver comprovada;
- os módulos existirem com schemas, flags e testes;
- os casos-piloto produzirem artefatos reais;
- defeitos conhecidos forem detectados;
- a pesquisa científica for verificável e calibrada;
- a consistência global alcançar peça, visual, relatório e e-mail;
- o painel refletir a realidade;
- rollback funcionar;
- a promoção atualizar todo o conjunto normativo;
- a revisão humana encontrar menos erros materiais sem receber burocracia inútil.

Até lá, o status correto é **candidata em planejamento, desenvolvimento ou sombra**, nunca “N4 implantada”.

---


<a id="src-s069"></a>

## 15. Fechamento dos marcos em 11/07/2026

| Marco | Estado | Evidência |
|---|---|---|
| M0 | concluído | 21 estados inventariados sem alteração destrutiva; `N4_M0_BASELINE_20260711T000646.json` |
| M1 | concluído em sombra | perguntas, cobertura, testes congelados e regressões automatizadas |
| M2 | concluído em sombra | grafo, terminologia, comparação, intertemporal, quantificação e consistência global |
| M3 | concluído em sombra | piloto real Crossref + PubMed/PMC; OpenAlex degrada sem falso bloqueio quando indisponível |
| M4 | concluído em sombra | condutas, maturidade de teses, decisão, solução consensual e limites de uso externo |
| M5 | concluído | metacognição, classificação de correção humana, sidecar, painel e abertura de artefatos |
| M6.1 | concluído | corpus 11/11 e telemetria real com Word e documentos de produção |
| M6.2 | concluído como baseline | três casos reais com 24/24, zero P0/P1, QA integral e mutation score 100% |
| M6.3 | concluído com correção | CASO-19/Fábio, CASO-16 e Saúde validados retrospectivamente; CASO-04 revogada e bloqueada |
| M6.4 | pendente de ciclos prospectivos | os três textos antecedem os testes e, por isso, `promotionEligible=false`; `default_on` não promovido |


<a id="src-s070"></a>

### Revisão M6.4 pelo Conselho - 11/07/2026
M6.4 continua pendente e ganhou critérios adicionais. Antes dos três ciclos prospectivos, o sistema deve provar: mutação semântica por famílias materiais; zero falsa aprovação P0 no corpus reservado; controles benignos com taxa de falso bloqueio publicada; pareceres Helena/Cícero específicos e anteriores ao produto final; regimento e citações materiais no ledger; e reexecução integral pelo agregador. Os três canários atuais possuem dois P1 de conselho cada e não servem como evidência de liberação jurídica.

Portanto, o estado final correto é **N4 implementada em modo piloto, com três baselines retrospectivas antifraude aprovadas, mas ainda sem os ciclos prospectivos exigidos para promoção geral**.

---


<a id="src-s071"></a>

## 16. M6.5 — Piloto prospectivo do perfil PSO-Pet


<a id="src-s072"></a>

### Objetivo

Testar se a definição explícita do problema, a história diagnóstica, a comparação de alternativas e a validação por requisitos reduzem erro e retrabalho sem burocratizar casos simples.


<a id="src-s073"></a>

### Execução

1. selecionar três casos novos: um leve, um completo e um intensivo;
2. congelar o roteiro metodológico antes da redação final;
3. manter histórico das iterações e reaberturas;
4. comparar requisitos planejados com a peça e com as revisões humanas;
5. colher decisões separadas de Helena e Cícero;
6. registrar resultado direto e explicações rivais após entrega;
7. comparar retrabalho, perda de sentido e omissões com baselines anteriores.


<a id="src-s074"></a>

### Critério de pronto

- três execuções prospectivas completas;
- zero falsa alegação de preenchimento anterior à redação;
- alternativa real examinada nos perfis completo e intensivo;
- utilidade reconhecida pelo conselho sem P0 novo causado pelo método;
- perfil leve sem aumento material injustificado de tempo;
- decisão documentada sobre manter em sombra, revisar ou promover itens específicos.


<a id="src-s075"></a>

### Rollback

Remover a exigência do roteiro nos casos seguintes, preservando os três pilotos para análise. Nenhum artefato N2/N3/N4 existente é apagado ou reclassificado.

---


<a id="src-s076"></a>

## 17. Trilha de compatibilidade obrigatória — F7-B vigente (adendo de 15/07/2026)

Este adendo não altera os sete marcos históricos nem afirma que a N4 foi promovida. Ele acrescenta uma condição de integração: qualquer marco que toque F7, F8, pacote ou replay deve preservar o F7-B implementado na base.


<a id="src-s077"></a>

### Trabalho necessário em cada marco afetado

1. fixtures e replays devem produzir `audited_markdown`, passar F7 com zero P0 e então acionar `forja_fable5.py` explicitamente; não se deve pressupor chamada automática por `forja_run.py`;
2. a infraestrutura de teste deve comprovar Claude Code em OAuth Claude Max e modelo `claude-fable-5`, sem substituir a assinatura por API key;
3. gates N4 adicionais devem ser executados antes do editor e recompostos novamente quando dependerem do texto final; nenhum score N4 pode suplantar `editorial_fidelity` bloqueado;
4. `FABLE5_RESULT` deve ser mesclado ao `PHASE_RESULT` de F7 junto das saídas jurídicas, científicas e adversariais;
5. F8, F9, mutações e entrega devem selecionar `final_markdown` como cânone e manter `audited_markdown`, diff, relatório, uso e fidelidade como cadeia de auditoria;
6. o harness de retry deve testar separadamente três candidatas internas no total (inicial + até dois retries) desde a origem e até quatro tentativas externas da fase, comprovando que uma candidata rejeitada nunca vira base incremental;
7. testes negativos devem alterar, um por vez, fato, data, número, citação, autoridade, marcador, ressalva, título, pedido/fecho, origem operacional e hash, esperando bloqueio determinístico.


<a id="src-s078"></a>

### Critério de pronto adicional

- zero promoção de fragmento isolado;
- zero pacote novo baseado apenas em `audited_markdown`;
- zero relaxamento dos limites semânticos pela N4;
- replays distinguem corretamente o contador editorial interno do contador da fase;
- falha de OAuth/modelo ou esgotamento das três candidatas bloqueia sem substituir a última versão válida.


<a id="src-s079"></a>

### Rollback

Desligar funcionalidades candidatas N4 continua sendo o rollback da N4. O F7-B pertence à base vigente e não é removido por esse rollback; eventual retorno dele exige decisão normativa separada, mantendo os bundles já produzidos como evidência histórica.
