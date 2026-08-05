# Diagnóstico arquitetural e propostas — FORJA Harness

Gerado em `2026-07-22T02:07:43-03:00`. Este documento é opinativo: distingue evidência observada, inferência arquitetural e proposta ainda não implementada.

## 1. Veredito executivo

FORJA possui muitos controles reais — contratos de fase, estado aditivo, validação e testes — mas a estrutura física plana virou o principal limitador. Sessenta e sete módulos de produção vivem na raiz; `forja_n3_common.py` recebe 48 imports e há um ciclo real entre packaging e validação N4. A próxima evolução deve reduzir acoplamento sem reescrever a esteira nem perder compatibilidade.

### Decisão recomendada

Começar por **P-J01 — Romper o ciclo package ↔ n4_validate**. É a intervenção com melhor relação entre redução de risco e superfície de mudança. Não executar uma reescrita ampla; usar migração incremental com fachadas compatíveis e testes de contrato.

## 2. Placar arquitetural

| Dimensão | Nota / 5 | Justificativa |
| --- | --- | --- |
| Contratos e gates | 4 | 52 schemas e validação extensa |
| Modularidade física | 1 | 67 módulos de produção na raiz |
| Testabilidade | 4 | 49 módulos têm consumidor direto |
| Acoplamento | 2 | Common hubs e um ciclo real |
| Segurança de migração | 3 | Fachadas podem preservar CLIs atuais |

## 3. Evidências que sustentam o diagnóstico

| ID | Achado | Fonte | Confiança |
| --- | --- | --- | --- |
| E-J01 | 67 módulos de produção somam 17.824 linhas; 21 excedem 300 e seis excedem 500. | 00_MAPA_ARQUITETURA_IA/INTERFACES_INFERIORES.json:1 | EXTRACTED |
| E-J02 | `forja_n3_common.py` recebe imports de 48 módulos; `forja_n4_common.py`, de 16. | forja_n3_common.py:1 | EXTRACTED |
| E-J03 | Existe ciclo qualificado real: `forja_n4_validate.py:292` importa `validate_f8` de package; `forja_package.py:635` importa `validate_case` do validador. | forja_n4_validate.py:292 | EXTRACTED |
| E-J04 | `forja_package.py` possui 703 linhas e fan-out de 14 módulos locais. | forja_package.py:1 | EXTRACTED |
| E-J05 | `forja_n4_validate.py` possui 587 linhas, 37 imports declarados e registry manual de validators. | forja_n4_validate.py:1 | EXTRACTED |
| E-J06 | Há 52 schemas/contratos JSON; 15 referências literais de validação foram observadas no código selecionado. | 00_MAPA_ARQUITETURA_IA/INTERFACES_INFERIORES.json:1 | EXTRACTED |
| E-J07 | 49 de 67 módulos de produção têm consumidor direto de teste; 38 arquivos de teste foram indexados. | 00_MAPA_ARQUITETURA_IA/INTERFACES_INFERIORES.json:1 | EXTRACTED |

## 4. Leitura dos sintomas

- O escopo analisado contém **67 módulos**, **17824 linhas**, **21 módulos acima de 300 linhas**, **151 imports locais qualificados** e **1 ciclo real de import**.
- **49 módulos** têm consumidor de teste direto. Isso mede acoplamento de teste observado, não cobertura de linhas.
- Tamanho não é defeito isolado. Ele vira problema quando o mesmo módulo agrega políticas, I/O, transporte e promoção ou quando muitos consumidores dependem dele.
- As propostas abaixo priorizam risco de mudança, integridade de contrato e clareza de dependência; não buscam apenas reorganizar pastas.

## 5. Propostas priorizadas

### P-J01 · P0 · Romper o ciclo package ↔ n4_validate

**Problema comprovado:** Packaging chama validação agregada e o validador chama regra F8 definida no packager.

**Mudança proposta:** Extrair `validate_f8` e contratos de pacote para módulo neutro `forja/validation/package_contract.py`; ambos dependem dele, nunca um do outro.

**Superfície afetada:** `forja_n4_validate.py:292`; `forja_package.py:635`

**Critério de aceite:** SCC de imports igual a zero; testes de package e N4 continuam verdes; sem import local dentro de função para quebrar ciclo.

**Risco de execução:** Baixo a médio; mover função sem alterar semântica.

**Ganho esperado:** Ordem de import previsível e fronteira de validação clara.

### P-J02 · P0 · Migrar raiz plana para pacote por responsabilidade

**Problema comprovado:** 67 módulos `forja_*.py` dificultam fronteiras e fazem commons virarem dependência universal.

**Mudança proposta:** Criar `forja/core`, `orchestration`, `contracts`, `validation`, `artifacts`, `delivery`, `adapters`; arquivos atuais permanecem shims até migração completa.

**Superfície afetada:** Raiz `_FORJA_HARNESS`; novo pacote `forja/`

**Critério de aceite:** Novos módulos não importam shims da raiz; CLIs antigas mantêm assinatura; migração por fatia vertical.

**Risco de execução:** Alto se big-bang; obrigatório strangler pattern.

**Ganho esperado:** Responsabilidade e direção de dependência explícitas.

### P-J03 · P1 · Substituir common hubs por serviços pequenos

**Problema comprovado:** `forja_n3_common.py` é dependência de 48 módulos e mistura paths, JSON, hashing, IDs e resolução de caso.

**Mudança proposta:** Extrair `paths.py`, `json_io.py`, `hashing.py`, `ids.py`, `clock.py`, `workspace.py`; common reexporta durante transição.

**Superfície afetada:** `forja_n3_common.py`, `forja_n4_common.py`

**Critério de aceite:** Nenhum módulo novo importa `*_common`; cada utilitário tem testes e sem dependência reversa.

**Risco de execução:** Médio; preservar símbolos via reexport.

**Ganho esperado:** Menor blast radius e imports mais explicáveis.

### P-J04 · P1 · Gerar registry de validators a partir do catálogo de artefatos

**Problema comprovado:** Schemas, ARTIFACT_SPECS e `VALIDATORS` são fontes paralelas.

**Mudança proposta:** Cada ArtifactSpec referencia schema, fase, validator e política de promoção; compilador valida todos na inicialização/CI.

**Superfície afetada:** `n4_schemas/ARTIFACT_CATALOG.json`, `forja_n4_common.py`, `forja_n4_validate.py`

**Critério de aceite:** Todo schema tem owner/validator explícito ou `declarative_only`; zero artifact sem política.

**Risco de execução:** Médio; manter IDs e nomes de arquivos.

**Ganho esperado:** Menos drift e validação auditável.

### P-J05 · P1 · Separar construir, validar, publicar e entregar

**Problema comprovado:** `forja_package.py` concentra composição, checagem N4 e publicação de ponteiro.

**Mudança proposta:** Criar `PackageBuilder` puro, `PackageValidator`, `PackagePublisher` e `DeliveryService`; publicação recebe pacote imutável validado.

**Superfície afetada:** `forja_package.py`, `forja_delivery.py`, `forja_delivery_integrity.py`

**Critério de aceite:** Builder não escreve estado; validator não publica; publisher exige hash e resultado PASS; delivery registra evidência separada.

**Risco de execução:** Médio.

**Ganho esperado:** Falha não produz pacote parcialmente promovido.

### P-J06 · P2 · Orquestração dirigida por contrato de fase

**Problema comprovado:** Runner contém condicionais específicas de F7/F8/N4 além do contrato genérico.

**Mudança proposta:** Adicionar hooks declarativos de gate e promotion policy ao PhaseContract; runner executa interface comum.

**Superfície afetada:** `forja_run.py`, `forja_phase_contracts.py`, `phase_contracts/*.json`

**Critério de aceite:** Adicionar gate de fase não exige editar `forja_run.py`; política desconhecida falha fechada.

**Risco de execução:** Alto; migrar uma fase por vez.

**Ganho esperado:** Esteira extensível sem crescer o runner central.

## 6. Arquitetura-alvo

Abra [`FORJA_HARNESS_TARGET_ARCHITECTURE.html`](FORJA_HARNESS_TARGET_ARCHITECTURE.html). O diagrama não descreve o estado atual; ele define a direção de dependência desejada.

| Componente-alvo | Tipo | Responsabilidade |
| --- | --- | --- |
| CLI / Agente | external | contrato estável |
| Orchestration | frontend | runner e estado |
| Phase Contracts | security | schemas e políticas |
| Core | messagebus | IDs, hash, paths |
| Validation | security | registry por artefato |
| Artifact Services | backend | build + render |
| Event State | database | append-only |
| Adapters | cloud | LLM, busca, Office |
| Publish / Delivery | external | hash + evidência |

### Regras de dependência

1. Transporte e CLIs dependem da aplicação; a aplicação não depende do transporte.
2. Políticas de domínio não leem arquivos, banco, subprocesso, rede ou UI diretamente.
3. Schemas e contratos têm owner, versão e consumidor explícitos.
4. Validação precede promoção/publicação; falha não é convertida em saída parcial.
5. Fachadas antigas permanecem durante a migração e são removidas somente após inventário de consumidores.

## 7. Roadmap executável

| Onda | Objetivo | Tamanho | Saída verificável |
| --- | --- | --- | --- |
| W0 | Romper ciclo package/validator | 1 entrega | zero SCC |
| W1 | Extrair core com reexports | 2–3 entregas | novos imports direcionais |
| W2 | Package services + registry | 3 entregas | build/validate/publish separados |
| W3 | Migrar para pacote `forja/` | por fatias | shims removidos só após consumidores |

### Gates entre ondas

- Não iniciar a onda seguinte com testes de contrato vermelhos.
- Comparar artefatos antes/depois por hash, schema e comportamento observável.
- Mudança de caminho não autoriza mudança de conteúdo, regra jurídica ou estado operacional.
- Se uma fachada compatível esconder erro, falhar explicitamente e registrar consumidor pendente.

## 8. O que não fazer

- Não executar big-bang nem renomear toda a árvore de uma vez.
- Não introduzir framework apenas para obter aparência de arquitetura.
- Não migrar dados privados para novos formatos antes de contrato, backup e rollback.
- Não considerar diagrama ou pasta nova como prova de melhoria; os critérios de aceite precisam passar.
- Não tratar relações inferidas como binding confirmado.

## 9. Próxima ação técnica

Executar uma entrega curta para **P-J01**, com fixture de regressão e relatório antes/depois. As demais propostas permanecem registradas, mas não devem ser iniciadas em paralelo antes de estabilizar essa fronteira.
