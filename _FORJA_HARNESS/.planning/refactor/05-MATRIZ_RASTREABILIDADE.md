# Matriz de rastreabilidade — FORJA R1

**Objetivo:** provar que cada requisito possui plano, teste, gate e evidência esperada

## 1. Requisitos funcionais

| Requisito | Onda/plano | Teste ou verificação | Evidência de conclusão |
|---|---|---|---|
| RF-REF-001 baseline | R0 / P00 | inventário + restore | manifest, hashes, log de restore |
| RF-REF-002 régua | R1 / P01 | teste órfão reprova | relatório 100% classificado |
| RF-REF-003 P0 | R1 / P02–P04 | negativos/benignos | quatro gates fail-closed |
| RF-REF-004 reproduzibilidade | R2 / P05 | instalação limpa | lock + suíte não-real |
| RF-REF-005 fachadas | R2–R7 | contratos de import/CLI | equivalência e telemetria |
| RF-REF-006 catálogos | R3-B / P07 | cobertura de catálogo | zero definição órfã |
| RF-REF-007 geração | R3-B / P07 | `--check` | geração determinística |
| RF-REF-008 event store | R4 / P08 | replay/concorrência | stateHash/equivalência |
| RF-REF-009 promoção | R4 / P08 | fault injection | zero parcialidade |
| RF-REF-010 resolução | R4 / P08 | 0/1/N matches | ambiguidade explícita |
| RF-REF-011 entrega | R5 / P09 | dois DOCX/hash divergente | receipt por ID/hash |
| RF-REF-012 outbox | R5 / P10 | pane/retry | sync uma vez |
| RF-REF-013 render | R6-A / P11 | Word/PDF/EMF | QA todas as páginas |
| RF-REF-014 hotspots | R6 / P11–P13 | caracterização | complexidade reduzida |
| RF-REF-015 separação | R7 / P14 | imports/paths | fonte sem outputs |
| RF-REF-016 sanitização | R7 / P14 | manifesto/restore | zero perda |
| RF-REF-017 CLI | R6-C / P13A–P13B | args/help/exit/effect + allowlist | framework e wrappers equivalentes |
| RF-REF-018 erros | R2/R6-C | teste de mapeamento | biblioteca sem SystemExit |
| RF-REF-019 Mermaid | R8 / P15 | render 100% | atlas validado |
| RF-REF-020 navegação IA | R8 / P15 | roteiro de localização | matriz de impacto completa |
| RF-REF-021 remoção shims | R9 / P16 | telemetria/referências | evidência individual |
| RF-REF-022 F2-A | R1/R9 | corpus F2-A | contrato/legacy preservados |

## 2. RNFs

| RNF | Gates | Métrica |
|---|---|---|
| RNF-001 segurança jurídica | G1, G6, G9A/G9B | zero gate degradado |
| RNF-002 compatibilidade | G3–G9A; G9B para promoção | 100% corpus legível |
| RNF-003 auditabilidade | G0–G9 | todo movimento com hash/razão |
| RNF-004 fail-closed | G1 | erro nunca vira ok |
| RNF-005 determinismo | G3/G4/G8 | execuções equivalentes |
| RNF-006 modularidade | G2/G3/G6 | zero import proibido |
| RNF-007 manutenibilidade | G6 | tipos/complexidade não pioram |
| RNF-008 reprodutibilidade | G2 | ambiente limpo verde |
| RNF-009 desempenho | G4–G9 | regressão dentro do orçamento |
| RNF-010 portabilidade | G2/G6 | core sem Word |
| RNF-011 observabilidade | G4/G5/G8 | IDs/hashes/duração/erro |
| RNF-012 privacidade | todos | secret/provenance scan limpo |
| RNF-013 legibilidade | G8 | Mermaid 100%; ≥8 pt |
| RNF-014 recuperabilidade | todos | restore por onda |
| RNF-015 limite normativo | todos | manifest preservado |

## 3. Invariantes e sentinelas

| Grupo | Invariantes | Sentinela |
|---|---|---|
| estado normativo | INV-01, INV-20, INV-21 | diff do manifest/config/contratos |
| fonte e prova | INV-02–INV-08, INV-22–INV-24 | gates negativos + fonte oficial |
| fluxo F2-A/conselho | INV-09–INV-11 | corpus F2-A + pareceres |
| documento final | INV-12–INV-15 | Word COM, EMF, PDF, metadata, QA |
| entrega | INV-16–INV-19 | receipt/evidência/outbox |

## 4. Requisito do usuário → resultado

| Pedido | Resultado planejado |
|---|---|
| limpeza/sanitização | R0 + R7, com backup e restore |
| tirar duplicidade | R3/R5/R6, distinguindo defesa independente |
| boas práticas | pacote, typing, portas, erros, testes arquiteturais |
| modularidade | core/domain/application/ports/adapters |
| alterar sem quebrar | matriz de impacto, TDD, wrappers e replay |
| fácil para IA | README, atlas vivo, ownership e fontes canônicas |
| PDF | deliverable consolidado e QA página a página |
| TDD | 14 comportamentos RED–GREEN–REFACTOR |
| roadmap | ondas R0–R9, gates G0–G9 |
| diagramas | 22 diagramas-base + Gantt |

## 5. Cobertura dos planos executáveis

| Plano | Tipo | Requisitos principais |
|---|---|---|
| P00 baseline | execute | 001, 016 |
| P01 régua | tdd | 002, 022 |
| P02 regimento | tdd | 003, 006 |
| P03 citações | tdd | 003, 018 |
| P04 injection | tdd | 003, 018 |
| P05 ambiente | execute | 004, 005, 018 |
| P06 core | tdd | 005, 008 |
| P07 catálogos | tdd | 006, 007, 022 |
| P08 estado/promoção | tdd | 008, 009, 010 |
| P09 entrega | tdd | 011, 013 |
| P10 gestão | tdd | 012, 018 |
| P11 render | tdd | 013, 014 |
| P12 validadores | tdd | 014, 018 |
| P13A CLI framework | execute | 005, 017, 018 |
| P13B CLI wrappers | execute | 005, 017, 018, 021 |
| P14 sanitização física | execute | 015, 016 |
| P15 atlas | execute | 019, 020 |
| P16 replay/cutover | execute | 021, 022 |

## 6. Gate de cobertura

O pacote só está pronto para execução se:

- todo RF aparece em pelo menos um plano;
- todo RNF possui gate e métrica;
- todo invariante possui sentinela;
- todo plano possui leitura prévia, ação concreta, verificação e aceite;
- nenhum requisito histórico já implementado foi reespecificado como funcionalidade nova.
