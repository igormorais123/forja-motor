# Graph Report - C:\Users\IgorPC\.claude\projects\Escritório fabio osório\fabricas de melhoria de petições\_FORJA_HARNESS  (2026-08-05)

## Corpus Check
- 8447 files · ~0 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 3156 nodes · 7416 edges · 111 communities
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 103 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `3866e1c1`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Entry-Document — forja
- Architecture-Decision — forja
- Failure-Mode — forja
- Architecture-Decision — forja
- Architecture-Decision — forja
- Failure-Mode — forja
- Interfaces inferiores v3
- Decisão arquitetural v4

## God Nodes (most connected - your core abstractions)
1. `FORJA Harness` - 2019 edges
2. `forja_n3_common.read_json(path: Path, fallback: Any = <default>) -> Any` - 97 edges
3. `forja_n3_common.sha256_file(path: Path) -> str` - 77 edges
4. `forja_n3_common.ForjaN3Error(RuntimeError)` - 71 edges
5. `forja_n3_common.atomic_write_json(path: Path, payload: Any) -> None` - 66 edges
6. `forja_n3_common.now_iso() -> str` - 60 edges
7. `forja_n4_common.issue(code: str, detail: str, *, severity: str = <default>, artifact: str | None = <default>) -> dict` - 50 edges
8. `forja_n4_validate.validate_case(case_dir: Path, *, target_phase: str | None = <default>, write: bool = <default>, mode_override: str | None = <default>) -> dict` - 35 edges
9. `forja_post_protocol.ingest_return(case_dir: Path, attachment_path: Path, *, account_id: str, thread_id: str, message_id: str, attachment_id: str, received_at: str, original_name: str | None = <default>, piece_name: str = <default>, process_id: str = <default>, declaration_text: str = <default>, evidence_paths: list[Path] | None = <default>, explicit_evidence_links: list[dict] | None = <default>, producer_run_id: str | None = <default>) -> dict` - 35 edges
10. `forja_n3_common.canonical_hash(payload: Any) -> str` - 32 edges

## Surprising Connections (you probably didn't know these)
- `FORJA Harness` --has_architecture_component--> `F1 Intake`  [INFERRED]
  . → FORJA_HARNESS_ARCHITECTURE.architecture.json
- `FORJA Harness` --has_architecture_component--> `F2A Exploração`  [INFERRED]
  . → FORJA_HARNESS_ARCHITECTURE.architecture.json
- `FORJA Harness` --has_architecture_component--> `F5 Blueprint`  [INFERRED]
  . → FORJA_HARNESS_ARCHITECTURE.architecture.json
- `FORJA Harness` --has_architecture_component--> `F7 Auditoria`  [INFERRED]
  . → FORJA_HARNESS_ARCHITECTURE.architecture.json
- `FORJA Harness` --has_architecture_component--> `F7-B Editorial`  [INFERRED]
  . → FORJA_HARNESS_ARCHITECTURE.architecture.json

## Import Cycles
- None detected.

## Communities (111 total, 0 thin omitted)

### Community 13 - "Entry-Document — forja"
Cohesion: 0.09
Nodes (11): FORJA Harness, F3 Pesquisa, F4 Conselho, F6 Redação, ADR-J03 — Conselho como insumo, ADR-J04 — F7 antes de F7-B, ADR-J06 — Render é etapa verificável, S-J01 — Executar caso novo (+3 more)

### Community 79 - "Architecture-Decision — forja"
Cohesion: 0.50
Nodes (4): F1 Intake, F2A Exploração, ADR-J01 — Contratos por fase, ADR-J02 — F2A bloqueante antes da redação

### Community 31 - "Failure-Mode — forja"
Cohesion: 0.25
Nodes (8): F5 Blueprint, Aprendizado, AR Arquitetural, ADR-J05 — Estado fora do código, S-J03 — Aplicar revisão editorial, F-J01 — Injeção no corpus, F-J10 — Lição promovida não entra na próxima peça, F-J11 — AR altera produção ou perde evidência

### Community 28 - "Architecture-Decision — forja"
Cohesion: 0.20
Nodes (10): F7 Auditoria, F7-B Editorial, ADR-J07 — Pós-protocolo é ramo de F10, ADR-J08 — Protocolo exige elo de arquivo, S-J05 — Assimilar retorno humano, S-J06 — Aplicar lição promovida, F-J03 — Lacuna material ignorada, F-J04 — Editorial altera substância (+2 more)

### Community 29 - "Architecture-Decision — forja"
Cohesion: 0.22
Nodes (9): F8 Materialização, QA final, ADR-J09 — Aprendizado tem autoridade crescente, ADR-J10 — Evolução arquitetural é isolada, S-J07 — Ensaiar evolução arquitetural, F-J05 — Estado confundido com código, F-J06 — Render defeituoso, Z2 — Produção (+1 more)

### Community 30 - "Failure-Mode — forja"
Cohesion: 0.22
Nodes (9): Estado / telemetria, F10 Entrega, Retorno humano, F-J07 — Baseline pós-protocolo errada, F-J08 — Falso protocolo, F-J09 — Reingestão apaga decisões, Z4 — Materialização/entrega, Z5 — Pós-protocolo (+1 more)

### Community 90001 - "Interfaces inferiores v3"
Cohesion: 0.00
Nodes (1647): calibrar_mapa_gen.carrega_manual(path), calibrar_mapa_gen.acha_md(base, nome), calibrar_mapa_gen.resolve(ancora, paragrafos), calibrar_mapa_gen.cobre(manuais, gerados, paragrafos), calibrar_mapa_gen.main(), forja_adocao_rota._sha_arquivo(caminho), forja_adocao_rota._entregas(limite), forja_adocao_rota._caminho_alvo(valor, marcador) (+1639 more)

### Community 90002 - "Decisão arquitetural v4"
Cohesion: 0.15
Nodes (13): E-J01 — 67 módulos de produção somam 17.824 linhas; 21 excedem 300 e seis excedem 500., E-J02 — `forja_n3_common.py` recebe imports de 48 módulos; `forja_n4_common.py`, de 16., E-J03 — Existe ciclo qualificado real: `forja_n4_validate.py:292` importa `validate_f8` de package, E-J04 — `forja_package.py` possui 703 linhas e fan-out de 14 módulos locais., E-J05 — `forja_n4_validate.py` possui 587 linhas, 37 imports declarados e registry manual de valid, E-J06 — Há 52 schemas/contratos JSON; 15 referências literais de validação foram observadas no cód, E-J07 — 49 de 67 módulos de produção têm consumidor direto de teste; 38 arquivos de teste foram in, P-J01 — Romper o ciclo package ↔ n4_validate (+5 more)

## Ambiguous Edges - Review These
- `forja_axi.AxiError.__init__(self, message: str, *, code: str = <default>, exit_code: int = <default>, help_commands: Sequence[str] = <default>) -> None` → `forja_axi.AxiArgumentParser.__init__(self, *args: Any, **kwargs: Any) -> None`  [AMBIGUOUS]
  forja_axi.py · relation: calls
- `forja_axi.AxiArgumentParser.__init__(self, *args: Any, **kwargs: Any) -> None` → `forja_axi.AxiError.__init__(self, message: str, *, code: str = <default>, exit_code: int = <default>, help_commands: Sequence[str] = <default>) -> None`  [AMBIGUOUS]
  forja_axi.py · relation: calls

## Knowledge Gaps
- **7 isolated node(s):** `E-J01 — 67 módulos de produção somam 17.824 linhas; 21 excedem 300 e seis excedem 500.`, `E-J02 — `forja_n3_common.py` recebe imports de 48 módulos; `forja_n4_common.py`, de 16.`, `E-J03 — Existe ciclo qualificado real: `forja_n4_validate.py:292` importa `validate_f8` de package`, `E-J04 — `forja_package.py` possui 703 linhas e fan-out de 14 módulos locais.`, `E-J05 — `forja_n4_validate.py` possui 587 linhas, 37 imports declarados e registry manual de valid` (+2 more)
  These have ≤1 connection - possible missing edges or undocumented components.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `forja_axi.AxiError.__init__(self, message: str, *, code: str = <default>, exit_code: int = <default>, help_commands: Sequence[str] = <default>) -> None` and `forja_axi.AxiArgumentParser.__init__(self, *args: Any, **kwargs: Any) -> None`?**
  _Edge tagged AMBIGUOUS (relation: calls) - confidence is low._
- **What is the exact relationship between `forja_axi.AxiArgumentParser.__init__(self, *args: Any, **kwargs: Any) -> None` and `forja_axi.AxiError.__init__(self, message: str, *, code: str = <default>, exit_code: int = <default>, help_commands: Sequence[str] = <default>) -> None`?**
  _Edge tagged AMBIGUOUS (relation: calls) - confidence is low._
- **Are the 56 inferred relationships involving `FORJA Harness` (e.g. with `F1 Intake` and `F2A Exploração`) actually correct?**
  _`FORJA Harness` has 56 INFERRED edges - model-reasoned connections that need verification._
- **What connects `E-J01 — 67 módulos de produção somam 17.824 linhas; 21 excedem 300 e seis excedem 500.`, `E-J02 — `forja_n3_common.py` recebe imports de 48 módulos; `forja_n4_common.py`, de 16.`, `E-J03 — Existe ciclo qualificado real: `forja_n4_validate.py:292` importa `validate_f8` de package` to the rest of the system?**
  _7 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Entry-Document — forja` be split into smaller, more focused modules?**
  _Cohesion score 0.08994708994708994 - nodes in this community are weakly interconnected._
- **Should `Entry-Document — forja` be split into smaller, more focused modules?**
  _Cohesion score 0.07142857142857142 - nodes in this community are weakly interconnected._
- **Should `Entry-Document — forja` be split into smaller, more focused modules?**
  _Cohesion score 0.04878048780487805 - nodes in this community are weakly interconnected._

## Detalhamento de cobertura por profundidade

| Profundidade | Diretórios mapeados |
| --- | ---: |
| 1 | 35 |
| 2 | 94 |
| 3 | 146 |
| 4 | 177 |
| 5 | 100 |
| 6 | 70 |

A extração foi metadata-only: nomes, extensões, tamanhos, datas e relações pai-filho. Foram considerados **8447** arquivos visíveis até a profundidade **6**; **745** itens sensíveis/binários foram apenas contados e **84** subárvores foram podadas.

## Integridade estrutural do multigrafo

- Arestas brutas: **9136**.
- Pares dirigidos únicos: **7416**.
- Arestas exatamente repetidas: **376**.
- Relações adicionais no mesmo par fonte-destino: **1720**.
- As repetições são preservadas para manter evidência de múltiplos call sites/relacionamentos; não há endpoints ausentes, órfãos ou self-loops.

## Camadas complementares

| Camada | Nós |
| --- | ---: |
| base | 1185 |
| v2 | 35 |
| v3-interface | 1923 |
| v4-strategy | 13 |
