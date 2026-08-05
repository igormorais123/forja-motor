# Interfaces inferiores — FORJA Harness

Gerado em `2026-08-05T00:53:26-03:00` a partir do código e dos contratos declarativos selecionados.

## 1. O que este documento resolve

Esta camada desce da visão de componentes até os contratos que uma IA ou pessoa precisa para alterar o sistema sem adivinhar: módulos, símbolos, assinaturas, comandos, opções, schemas, dependências locais, chamadas e consumidores. Ela complementa — não substitui — a arquitetura de sistema e os mapas canônicos locais.

## 2. Limite de confiança e privacidade

- `EXTRACTED`: declaração ou relação observada no código, com arquivo e linha.
- `AMBIGUOUS`: candidato de chamada resolvido por nome; confirme o binding/import antes de mudança material.
- Valores literais de defaults não são copiados; o documento registra apenas que há default.
- Bancos, estados, telemetria, mensagens, anexos, conteúdo jurídico, caches e segredos não foram lidos.

## 3. Cobertura executável

| Métrica | Quantidade |
| --- | --- |
| Módulos/scripts | 128 |
| Símbolos públicos | 591 |
| Símbolos internos indexados | 556 |
| Comandos/subcomandos | 136 |
| Opções CLI | 364 |
| Schemas/contratos JSON | 59 |
| Módulos consumidores de teste | 89 |
| Relações locais | 4304 |
| Falhas de parse | 0 |


## 4. Módulos e superfície pública

### `calibrar_mapa_gen.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | carrega_manual | `(path)` | 37 | — |
| function | acha_md | `(base, nome)` | 44 | — |
| function | resolve | `(ancora, paragrafos)` | 49 | — |
| function | cobre | `(manuais, gerados, paragrafos)` | 63 | — |
| function | main | `()` | 77 | — |


### `forja_adocao_rota.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | medir | `(limite = <default>)` | 185 | — |
| function | main | `()` | 222 | — |


### `forja_adversarial_audit.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | mandatory_prompt_for_phase | `(phase: str) -> str` | 96 | — |
| function | response_product_required | `(text: str) -> bool` | 102 | — |
| function | initialize_audit | `(source: Path, *, applicable: bool = <default>, reason: str = <default>) -> dict` | 120 | — |
| function | validate_adversarial_audit | `(payload: dict, *, source_path: Path \| None = <default>) -> dict` | 206 | — |
| function | validate_adversarial_strategy | `(payload: dict, audit_path: Path) -> dict` | 344 | — |
| function | validate_adversarial_recheck | `(payload: dict, audit_path: Path, strategy_path: Path) -> dict` | 403 | — |
| function | validate_phase_artifacts | `(phase: str, artifacts: dict[str, Path], inputs: dict[str, dict]) -> list[str]` | 456 | — |
| function | main | `() -> None` | 482 | — |


### `forja_adversarial_gate.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | validar_auditoria_adversarial | `(auditoria, estrategia = <default>, caminho_auditoria = <default>)` | 62 | — |
| function | validar_politica_liberacao | `(manifesto, gate_result = <default>)` | 224 | — |


### `forja_alertas.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | notificar_p0 | `(case_dir, gate: str, motivo: str, origem: str = <default>, demand_id: str \| None = <default>) -> dict` | 167 | — |
| function | notificar_resolucao | `(case_dir, gate: str, demand_id: str \| None = <default>) -> dict` | 185 | — |
| function | drenar_pendentes | `(case_dir) -> dict` | 199 | — |


### `forja_ar_architecture.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | automation_enabled | `(config: dict) -> bool` | 81 | — |
| function | validate_candidate | `(candidate: dict) -> list[str]` | 95 | — |
| function | validate_manifest | `(manifest: dict) -> list[str]` | 112 | — |
| function | create_candidate | `(candidate_id: str, *, title: str, problem: str, hypothesis: str, scope: list[str]) -> Path` | 136 | — |
| function | evaluate_candidate | `(path: Path, *, review_path: Path) -> dict` | 422 | — |
| function | main | `() -> None` | 543 | — |


### `forja_ar_blind.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | canonicalize | `(text: str) -> str` | 20 | — |
| function | leak_scan | `(text: str) -> list[str]` | 44 | — |
| function | prepare | `(runpair_dir: Path, blind_dir: Path, pair_id: str, *, key: bytes \| None = <default>) -> dict` | 68 | — |
| function | consolidate | `(blind_dir: Path, judgment_paths: list[Path], pair_id: str, *, key: bytes \| None = <default>, workspace: Path = <default>) -> dict` | 159 | — |
| function | main | `(argv = <default>) -> int` | 251 | — |


### `forja_ar_canarios.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | verificar_manifest | `(manifest_path: Path) -> dict` | 36 | — |
| function | verificar | `(*, public_manifest: Path = <default>, secreto: bool = <default>) -> dict` | 95 | — |
| function | main | `(argv = <default>) -> int` | 122 | — |


### `forja_ar_ciclo.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | append_log | `(log_path: Path, ciclo: str, acao: str, inputs, resultado) -> dict` | 46 | — |
| function | verify_log | `(log_path: Path) -> list[str]` | 71 | — |
| function | snapshot | `(cycle_dir: Path, manifest_path: Path, *, corpus_path: Path \| None = <default>, log_path: Path \| None = <default>) -> Path` | 96 | — |
| function | consume_sealed | `(version: str, limit: int, evaluation: dict \| None = <default>) -> tuple[bool, str]` | 140 | — |
| function | promotion | `(cycle_dir: Path, manifest_path: Path, *, comparison_path: Path \| None, canary_path: Path \| None, judgment_path: Path \| None, use_sealed: bool = <default>, variant_sha: str \| None = <default>, sealed_eval_path: Path \| None = <default>) -> dict` | 169 | — |
| function | independent_review | `(decision_path: Path, opinion_path: Path, family: str, generator_family: str) -> dict` | 264 | — |
| function | human_approve | `(decision_path: Path, receipt_path: Path) -> dict` | 282 | — |
| function | cluster_interval | `(values_by_lineage: dict[str, list[float]], corpus_hash: str, samples: int = <default>) -> dict` | 309 | — |
| function | relatorio | `(cycle_dir: Path, panel_path: Path, output_path: Path \| None = <default>) -> Path` | 331 | — |
| function | main | `(argv = <default>) -> int` | 389 | — |


### `forja_ar_corpus.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | secrets_dir | `(*, create: bool = <default>) -> Path` | 42 | — |
| function | load_hmac_key | `(*, create_dir: bool = <default>) -> bytes` | 56 | — |
| function | derivar_linhagem | `(case_id: str, case_folder: str = <default>, equivalencias: dict \| None = <default>) -> str` | 75 | — |
| function | atribuir_split | `(lineage_id: str, key: bytes, split_config: dict \| None = <default>) -> str` | 92 | — |
| function | scan_corpus | `(state_dir: Path = <default>, *, manifest: dict \| None = <default>, key: bytes \| None = <default>, sealed_sink: list[dict] \| None = <default>) -> dict` | 155 | — |
| function | register_sealed_inventory | `(items: list[dict], manifest: dict) -> Path` | 260 | — |
| function | check_corpus | `(corpus: dict, root: Path = <default>) -> list[str]` | 281 | — |
| function | report | `(corpus: dict) -> dict` | 298 | — |
| function | main | `(argv = <default>) -> int` | 313 | — |


### `forja_ar_evolucao.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | init_experimento | `(experimento: str, alvo: Path, *, convergencia_ganho_min: float = <default>, convergencia_geracoes: int = <default>, top_k: int = <default>) -> dict` | 44 | — |
| function | registrar_geracao | `(experimento: str, variantes: list[dict]) -> dict` | 70 | — |
| function | selecionar_winner | `(experimento: str, geracao: int, resultados: list[dict]) -> dict` | 103 | — |
| function | verificar_convergencia | `(experimento: str) -> dict` | 150 | — |
| function | main | `(argv = <default>) -> int` | 169 | — |


### `forja_ar_indicadores.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | computar_indicadores | `(md_texto: str, contexto: dict \| None = <default>) -> dict` | 182 | — |
| function | comparar | `(baseline: dict, variante: dict, manifest: dict \| None = <default>) -> dict` | 244 | — |
| function | cache_key | `(md_texto: str, contexto: dict, sensor_versions: dict \| None = <default>) -> str` | 286 | — |
| function | computar_com_cache | `(md_texto: str, contexto: dict, cache_dir: Path = <default>) -> tuple[dict, bool]` | 292 | — |
| function | main | `(argv = <default>) -> int` | 322 | — |


### `forja_ar_runpair.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | freeze_input | `(runpair_dir: Path, case_id: str, target: Path, *, claims_ledger: list \| None = <default>, authorities_ledger: list \| None = <default>, repetition: int = <default>) -> Path` | 36 | — |
| function | sanitize_instructions | `(text: str) -> str` | 68 | — |
| function | register_manifest | `(runpair_dir: Path, side: str, manifest_path: Path) -> Path` | 79 | — |
| function | validate_pair | `(runpair_dir: Path) -> dict` | 105 | — |
| function | main | `(argv = <default>) -> int` | 162 | — |


### `forja_artefatos.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | ler | `(caminho) -> dict` | 121 | — |
| function | nomes | `(especie: str, conceito: str) -> tuple` | 135 | — |
| function | campo | `(dados: dict, especie: str, conceito: str, padrao = <default>)` | 145 | — |
| function | lista | `(dados: dict, especie: str, conceito: str) -> list` | 160 | — |
| function | censo | `(raiz = <default>) -> dict` | 170 | — |


### `forja_assinatura_visual.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | paginas_reais | `(docx)` | 55 | — |
| function | avaliar | `(docx, paginas = <default>, tipo = <default>)` | 259 | — |
| function | main | `()` | 320 | — |


### `forja_authorities.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | normalize_number | `(value: str \| None) -> str` | 80 | — |
| function | tribunal_from_cnj | `(value: str \| None) -> str \| None` | 84 | — |
| function | authority_key | `(item: dict) -> tuple[str, str, str]` | 92 | — |
| function | extract_authorities | `(text: str) -> list[dict]` | 152 | — |


### `forja_axi.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| class | AxiError | `(RuntimeError)` | 112 | — |
| method | AxiError.__init__ | `(self, message: str, *, code: str = <default>, exit_code: int = <default>, help_commands: Sequence[str] = <default>) -> None` | 115 | — |
| class | AxiArgumentParser | `(argparse.ArgumentParser)` | 129 | — |
| method | AxiArgumentParser.__init__ | `(self, *args: Any, **kwargs: Any) -> None` | 132 | — |
| method | AxiArgumentParser.error | `(self, message: str) -> None` | 136 | — |
| function | now_iso | `() -> str` | 145 | — |
| function | compact_path | `(path: Path) -> str` | 149 | — |
| function | home_payload | `(state_root: Path = <default>) -> dict[str, Any]` | 294 | — |
| function | cases_payload | `(state_root: Path = <default>, *, status: str \| None = <default>, limit: int = <default>, fields: str \| None = <default>, full: bool = <default>) -> dict[str, Any]` | 333 | — |
| function | case_payload | `(case_id: str, state_root: Path = <default>, *, fields: str \| None = <default>, full: bool = <default>) -> dict[str, Any]` | 402 | — |
| function | queue_payload | `(state_root: Path = <default>, *, section: str = <default>, limit: int = <default>, fields: str \| None = <default>, full: bool = <default>) -> dict[str, Any]` | 456 | — |
| function | commands_payload | `(name: str \| None = <default>) -> dict[str, Any]` | 517 | — |
| function | health_payload | `(state_root: Path = <default>) -> dict[str, Any]` | 552 | — |
| function | encode_toon | `(value: Any) -> str` | 740 | — |
| function | render | `(payload: dict[str, Any], output_format: str) -> str` | 748 | — |
| function | build_parser | `() -> AxiArgumentParser` | 785 | — |
| function | main | `(argv: Sequence[str] \| None = <default>, *, state_root: Path = <default>, stdout: TextIO \| None = <default>) -> int` | 867 | — |


### `forja_baseline.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | coletar | `() -> list[str]` | 144 | — |
| function | executar | `() -> dict` | 152 | — |
| function | main | `() -> int` | 200 | — |


### `forja_baseline_aprovado.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | conferir | `() -> dict` | 97 | — |
| function | gravar | `(motivo: str) -> dict` | 138 | — |


### `forja_bench_modelos.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| class | Prova | `()` | 60 | dataclass(frozen=True) |
| function | gabarito | `(prova: Prova) -> str` | 138 | — |
| function | avaliar | `(prova: Prova, resposta: str) -> dict` | 170 | — |
| function | rodar | `(modelos: list[str], *, teto_usd: float = <default>, max_tokens: int = <default>, condicoes: tuple[str, ...] = <default>) -> dict` | 224 | — |
| function | reavaliar | `(caminho: Path) -> dict` | 268 | — |
| function | main | `() -> None` | 318 | — |


### `forja_calibra_gates_economicos.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | relevante | `(caminho: Path) -> bool` | 59 | — |
| function | main | `(argv: list[str]) -> int` | 69 | — |


### `forja_calibra_monetario.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | ocorrencias_ampla | `(texto)` | 63 | — |
| function | economico_estreito | `(texto)` | 75 | — |
| function | economico_amplo | `(texto)` | 80 | — |
| function | varrer | `(raiz, extensoes = <default>, limite_bytes = <default>)` | 84 | — |
| function | calibrar | `(raiz, amostra = <default>)` | 100 | — |
| function | main | `()` | 166 | — |


### `forja_canario_catraca.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | catracas | `(suites: list[str] \| None = <default>) -> list[dict]` | 57 | — |
| function | canario | `(suites: list[str] \| None = <default>) -> dict` | 113 | — |


### `forja_canario_mutacao.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | canario | `(raiz = <default>, mutacoes = <default>, limite_por_gate: int = <default>) -> dict` | 207 | — |


### `forja_case_tests.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | suite_hash | `(payload: dict) -> str` | 19 | — |
| function | validate_suite | `(payload: dict) -> list[dict]` | 48 | — |
| function | run_suite | `(suite: dict, draft_path: Path, *, reviewer_run_id: str, producer_run_id: str \| None = <default>) -> dict` | 109 | — |
| function | validate_results | `(payload: dict, suite: dict \| None = <default>, draft_path: Path \| None = <default>) -> list[dict]` | 162 | — |
| function | main | `() -> None` | 192 | — |


### `forja_citations.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | tribunal_numero_cnj | `(value)` | 52 | — |
| function | texto_da_peca | `(path)` | 56 | — |
| function | normalizar_numero | `(n)` | 76 | — |
| function | url_oficial | `(tipo, dados)` | 80 | — |
| function | extrair_citacoes | `(texto)` | 115 | — |
| function | procurar_cache_oficial | `(citacao, *, require_live = <default>)` | 119 | — |
| function | normalizar_aspa | `(texto)` | 167 | — |
| function | conferir_aspas | `(texto_peca, arquivo_fonte)` | 172 | — |
| function | procurar_fonte_local | `(citacao, pasta_caso)` | 196 | — |
| function | merge_by_id | `(existing, new_items)` | 225 | — |
| function | append_unique | `(existing, value)` | 239 | — |
| function | processar | `(case_key, peca_path)` | 246 | — |
| function | validar_politica_citacoes | `(texto, ledger)` | 415 | — |
| function | validar_identidade_citacoes | `(texto, ledger = <default>)` | 517 | — |
| function | main | `()` | 575 | — |


### `forja_claim_binding.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | bind_claims | `(markdown_path: Path, ledger_path: Path, output_path: Path) -> dict` | 26 | — |
| function | main | `() -> int` | 91 | — |


### `forja_close_cycle.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | create_package | `(case_dir: Path, definition: Path, *, expected_revision: int) -> dict` | 43 | — |
| function | register_draft | `(case_dir: Path, receipt_path: Path, *, expected_revision: int) -> dict` | 80 | — |
| function | confirm_delivery | `(case_dir: Path, evidence_path: Path, *, expected_revision: int) -> dict` | 131 | — |
| function | fulfill | `(case_dir: Path, *, expected_revision: int) -> dict` | 171 | — |
| function | main | `() -> None` | 214 | — |


### `forja_conselho.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | validar_conselho | `(*, helena: Path \| None, cicero: Path \| None, decisoes: Path \| None) -> dict` | 229 | — |
| function | main | `(argv: list[str]) -> int` | 252 | — |


### `forja_consistency.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | inspect_physical_document | `(*, docx_path: Path, pdf_path: Path, f8_path: Path, layout_profile_id: str, expected_docx_hash: str \| None = <default>, expected_pdf_hash: str \| None = <default>) -> dict` | 17 | — |
| function | validate_event_identity | `(payload: dict) -> list[dict]` | 80 | — |
| function | validate_comparison | `(payload: dict) -> list[dict]` | 99 | — |
| function | validate_intertemporal | `(payload: dict) -> list[dict]` | 116 | — |
| function | validate_quantification | `(payload: dict) -> list[dict]` | 147 | — |
| function | validate_delivery | `(payload: dict) -> list[dict]` | 185 | — |
| function | validate_global | `(payload: dict) -> list[dict]` | 206 | — |
| function | validate_case | `(case_dir: Path) -> dict` | 244 | — |
| function | main | `() -> None` | 252 | — |


### `forja_context.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | markdown_blocks | `(text: str) -> list[dict]` | 22 | — |
| function | validate_document_index | `(index_payload: dict) -> list[dict]` | 97 | — |
| function | validate_coverage | `(index_payload: dict, coverage_payload: dict) -> list[dict]` | 138 | — |
| function | validate_fact_ledger | `(fact_payload: dict, source_ids: Iterable[str]) -> list[dict]` | 167 | — |
| function | validate_paragraph_provenance | `(markdown_text: str, provenance_payload: dict, fact_payload: dict, proposition_payload: dict) -> tuple[list[dict], list[dict]]` | 194 | — |
| function | validate_context | `(case_dir: Path) -> dict` | 228 | — |
| function | main | `() -> None` | 294 | — |


### `forja_contexto.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | validar_contexto | `(validacao, gate_result = <default>, texto_auditado = <default>)` | 101 | — |


### `forja_delivery.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | achar | `(pasta, padroes)` | 30 | — |
| function | ref_ok | `(ref, allow_text = <default>)` | 38 | — |
| function | ref_text | `(ref)` | 52 | — |
| function | append_unique | `(existing, value)` | 58 | — |
| function | f7_com_lastro | `(f7)` | 65 | — |
| function | f5_checklist_ok | `(path)` | 112 | — |
| function | parecer_valido | `(path)` | 129 | — |
| function | parecer_antes_da_redacao | `(parecer, state)` | 162 | — |
| function | visual_com_lastro | `(docx)` | 186 | — |
| function | f3_com_regimento | `(path)` | 216 | — |
| function | main | `(case_key)` | 229 | — |


### `forja_delivery_integrity.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | select | `(case_dir: Path, artifact_id: str, *, layout_profile_id: str, producer_run_id: str, reviewer_run_id: str) -> dict` | 29 | — |
| function | confirm | `(case_dir: Path, *, mode: str, delivery_evidence_id: str \| None, delivered_path: Path \| None, producer_run_id: str, reviewer_run_id: str, delivered_at: str \| None = <default>) -> dict` | 70 | — |
| function | main | `() -> None` | 129 | — |


### `forja_diabob.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | red_team | `(alvo: str, *, modelo: str = <default>, max_tokens: int = <default>, orcamento: fm.Orcamento \| None = <default>, caso: str \| None = <default>) -> dict` | 55 | — |
| function | main | `() -> None` | 75 | — |


### `forja_diff_docx.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | extrair_paragrafos_docx | `(caminho_docx)` | 24 | — |
| function | similaridade_ratio | `(s1, s2)` | 50 | — |
| function | classificar_mudanca | `(texto_nosso, texto_protocolado)` | 58 | — |
| function | gerar_diff_markdown | `(paragrafos_nosso, paragrafos_protocolado, saida_path = <default>)` | 90 | — |
| function | main | `()` | 231 | — |


### `forja_document_compare.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| class | Unit | `()` | 48 | dataclass(frozen=True) |
| class | Extracted | `()` | 55 | dataclass |
| method | Extracted.visible_text | `(self) -> str` | 65 | property |
| function | comparable_units | `(units: Iterable[Unit], *, cross_format: bool = <default>) -> list[Unit]` | 81 | — |
| function | extract_docx | `(path: Path) -> Extracted` | 145 | — |
| function | extract_pdf | `(path: Path, *, allow_ocr: bool = <default>) -> Extracted` | 184 | — |
| function | extract_document | `(path: Path, *, allow_ocr: bool = <default>) -> Extracted` | 253 | — |
| function | classify_change | `(before: str, after: str) -> tuple[str, str, str, float, list[str]]` | 272 | — |
| function | compare_documents | `(baseline_path: Path, human_path: Path, *, allow_ocr: bool = <default>) -> dict` | 362 | — |
| function | render_markdown | `(comparison: dict, *, protocol_status: str, baseline_artifact_id: str, human_artifact_id: str) -> str` | 507 | — |
| function | write_comparison | `(baseline_path: Path, human_path: Path, *, json_path: Path, markdown_path: Path, protocol_status: str, baseline_artifact_id: str, human_artifact_id: str, allow_ocr: bool = <default>) -> dict` | 575 | — |
| function | main | `() -> None` | 600 | — |


### `forja_docx_layout.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | docx_content_signature | `(path: Path) -> dict` | 113 | — |
| function | compare_docx_content | `(source: Path, output: Path) -> dict` | 219 | — |
| function | audit_docx_layout | `(path: Path, *, exceptions: Path \| None = <default>) -> dict` | 621 | — |
| function | normalize_medina_body | `(source: Path, output: Path) -> dict` | 861 | — |
| function | main | `() -> int` | 951 | — |


### `forja_editorial.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | run_editorial_pass | `(source_path: Path, output_dir: Path, *, gate_path: Path, case_id: str, artifact_suffix: str = <default>, editor_model: str \| None = <default>, reviewer_model: str \| None = <default>, reviewer_session: str \| None = <default>, invoke = <default>) -> dict` | 332 | — |
| function | main | `() -> int` | 517 | — |


### `forja_editorial_fidelity.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | validate_editorial_bundle | `(audited_path: Path, final_path: Path, report_path: Path, usage_path: Path \| None = <default>, *, expected_model: str \| None = <default>, strict_family: bool = <default>) -> dict` | 191 | — |
| function | main | `() -> int` | 389 | — |


### `forja_editorial_model.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| class | EditorialModel | `()` | 23 | dataclass(frozen=True) |
| method | EditorialModel.can_execute | `(self) -> bool` | 31 | property |
| method | EditorialModel.cli_model | `(self) -> str` | 35 | property |
| function | resolve | `(canonical_id: str \| None = <default>) -> EditorialModel` | 68 | — |
| function | resolve_executable | `(canonical_id: str \| None = <default>) -> EditorialModel` | 80 | — |
| function | is_authorized | `(canonical_id: str \| None) -> bool` | 91 | — |
| function | family_of | `(canonical_id: str \| None) -> str \| None` | 95 | — |
| function | family_assurance | `(producer_id: str \| None, reviewer_id: str \| None, *, producer_session: str \| None = <default>, reviewer_session: str \| None = <default>) -> str` | 100 | — |
| function | describe | `(canonical_id: str \| None, session_id: str \| None = <default>) -> dict` | 126 | — |


### `forja_email.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | listar | `(svc, limite: int = <default>) -> int` | 71 | — |
| function | enviar_rascunho | `(svc, draft_id: str, confirmar: bool) -> int` | 94 | — |
| function | main | `(argv: list[str]) -> int` | 126 | — |


### `forja_entrega.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | validar_reconciliacao | `(manifesto, relatorio = <default>)` | 84 | — |
| function | validar_pacote | `(manifesto, email = <default>, base_dir = <default>, artefatos_existentes = <default>)` | 158 | — |


### `forja_estilo_humano.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | mandatory_prompt_for_phase | `(phase: str) -> str` | 152 | — |
| function | analisar | `(texto: str, tipo: str = <default>) -> list[dict]` | 508 | — |
| function | relatorio | `(texto: str, tipo: str = <default>) -> dict` | 536 | — |
| function | main | `() -> int` | 549 | — |


### `forja_exploracao_100.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | selectable_findings | `(question: dict) -> list[dict]` | 97 | — |
| function | select_consultation_questions | `(payload: dict) -> tuple[list[str], list[dict]]` | 152 | — |
| function | validate_dialectic | `(payload: dict) -> list[dict]` | 178 | — |
| function | mandatory_prompt_for_phase | `(phase: str) -> str` | 285 | — |
| function | build_scaffold | `(case_id: str, case_anchor: str) -> dict` | 454 | — |
| function | validate_exploration_100 | `(payload: dict, *, require_protocol: bool = <default>) -> list[dict]` | 514 | — |
| function | gates_da_exploracao | `(payload: dict, *, require_protocol: bool = <default>) -> dict` | 650 | — |
| function | render_consultation | `(payload: dict, *, template: Path \| None = <default>) -> str` | 686 | — |
| function | record_response | `(payload: dict, entry: dict) -> dict` | 757 | — |
| function | main | `() -> int` | 786 | — |


### `forja_f10_contract.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | compute_f10_gates | `(package_manifest: dict, evidence: dict, state: dict, *, minimum_synced_event_seq: int \| None = <default>) -> dict[str, str]` | 55 | — |
| function | validate_f10_gates | `(gates: dict \| None) -> dict` | 89 | — |


### `forja_f2_check.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | tribunal_do_cnj | `(numero: str) -> str \| None` | 42 | — |
| function | tribunais_do_texto | `(texto: str) -> set[str]` | 59 | — |
| function | validar_classificacao | `(classificacao: dict, textos_do_caso: str = <default>) -> list[dict]` | 73 | — |
| function | main | `(argv = <default>) -> int` | 99 | — |


### `forja_f8_contract.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | inspect_pdf | `(*args, **kwargs)` | 22 | — |
| function | validate_f8 | `(artifact: dict, *, files: dict, release_policy: str = <default>) -> dict` | 391 | — |


### `forja_fidelity.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | compare_fidelity | `(markdown: Path, docx: Path, pdf: Path) -> dict` | 147 | — |
| function | compare_docx_fidelity | `(markdown: Path, docx: Path) -> dict` | 204 | — |
| function | write_fidelity | `(markdown: Path, docx: Path, pdf: Path, output: Path) -> dict` | 256 | — |
| function | main | `() -> None` | 262 | — |


### `forja_fila.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | classificar_prontidao | `(demanda, forja_state)` | 89 | — |
| function | pontuar | `(demanda, hoje)` | 124 | — |
| function | ordenar | `(pontuadas)` | 167 | — |
| function | pendencia_operacao_assistida | `(config, hoje)` | 179 | — |
| function | montar_fila | `(demandas, states, hoje)` | 203 | — |
| function | gerar | `(hoje = <default>, gravar = <default>, publicar_painel = <default>)` | 330 | — |
| function | main | `(argv = <default>)` | 363 | — |


### `forja_fontes_oficiais.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | validar_fontes_arquivadas | `(ledger, base_dir = <default>)` | 95 | — |
| function | validar_cotejo_citacoes | `(checklist, ledger = <default>)` | 279 | — |
| function | validar_pesquisa_oficial | `(ledger, checklist, base_dir = <default>)` | 347 | — |


### `forja_forma_artefatos.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | censo_de_formas | `(raiz = <default>) -> dict` | 64 | — |


### `forja_gate_liveness.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | medir | `() -> dict` | 163 | — |
| function | relatar | `(laudo: dict) -> None` | 222 | — |
| function | main | `(argv: list[str]) -> int` | 273 | — |


### `forja_headless.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | append_unique | `(existing, value)` | 53 | — |
| function | run_phase | `(case_key, fase, prompt, *, attempt_dir = <default>)` | 146 | — |
| function | main | `()` | 199 | — |


### `forja_human_review.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | public_key_id | `(public_key_raw: bytes) -> str` | 31 | — |
| function | canonical_receipt_bytes | `(payload: dict) -> bytes` | 35 | — |
| function | build_unsigned_claim_receipt | `(*, reviewer_id: str, reviewed_at: str, public_key_id_value: str, generator_run_id: str, claim: str, claim_sha256: str, source_excerpt: str, source_excerpt_sha256: str, source_sha256: str, source_url: str, source_identity: dict, source_identity_sha256: str, document_sha256: str, document_proposition: str, document_proposition_sha256: str, document_paragraph_index: int, document_paragraph_sha256: str, authority_identity: dict, authority_identity_sha256: str) -> dict` | 45 | — |
| function | build_unsigned_visual_receipt | `(*, reviewer_id: str, reviewed_at: str, public_key_id_value: str, generator_run_id: str, reviewer_run_id: str, pdf_sha256: str, docx_sha256: str, page_count: int, page_image_sha256: list[str], required_checks: list[str], visual_attestation_sha256: str) -> dict` | 95 | — |
| function | validate_claim_review_receipt | `(receipt_path: Path, *, expected: dict, trust_store_path: Path \| None = <default>, trust_store_pin_path: Path \| None = <default>) -> dict` | 245 | — |
| function | validate_visual_review_receipt | `(receipt_path: Path, *, expected: dict, trust_store_path: Path \| None = <default>, trust_store_pin_path: Path \| None = <default>) -> dict` | 263 | — |


### `forja_import_audited_cycle.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | role_for | `(path: Path) -> str` | 27 | — |
| function | import_cycle | `(case_dir: Path, source_dir: Path) -> dict` | 34 | — |
| function | main | `() -> None` | 66 | — |


### `forja_ingestao.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | validar_indice_documentos | `(indice, base_dir = <default>)` | 70 | — |
| function | validar_cobertura | `(ledger)` | 158 | — |
| function | validar_ingestao | `(indice, ledger, base_dir = <default>)` | 224 | — |


### `forja_injection_scan.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | distancia_rgb | `(cor1, cor2)` | 153 | — |
| function | analisar_pdf | `(caminho_pdf)` | 167 | — |
| function | processar_entrada | `(entrada)` | 284 | — |
| function | validar_triagem_injecao | `(scan)` | 399 | — |
| function | main | `()` | 432 | — |


### `forja_lastro.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | validar_lastro_fatos | `(ledger: dict, *, base_dir: Path \| str \| None = <default>, exigir_transcricao: bool = <default>) -> list[dict]` | 278 | — |
| function | exigir_criterio_vigente | `(ledger: dict) -> list[dict]` | 436 | — |
| function | validar_decisoes_revisao | `(payload: dict) -> list[dict]` | 464 | — |
| function | analisar_texto | `(texto: str, tipo: str = <default>) -> list[dict]` | 496 | — |
| function | fatos_sem_lastro | `(ledger: dict) -> list[str]` | 565 | — |
| function | material_economico | `(texto: str) -> bool` | 592 | — |
| function | validar_fonte_prevalente | `(ledger: dict \| None, *, base_dir: Path \| str \| None = <default>, exigir: bool = <default>) -> list[dict]` | 798 | — |
| function | validar_data_base | `(texto: str, ledger: dict \| None, *, exigir: bool = <default>) -> list[dict]` | 875 | — |
| function | validar_valores_monetarios | `(texto: str, ledger: dict \| None, *, exigir: bool = <default>) -> list[dict]` | 898 | — |
| function | validar_hierarquia_fontes | `(ledger: dict \| None, *, base_dir: Path \| str \| None = <default>, exigir: bool = <default>) -> list[dict]` | 1041 | — |
| function | validar_aritmetica_derivada | `(texto: str, ledger: dict \| None, *, exigir: bool = <default>) -> list[dict]` | 1083 | — |
| function | validar_gates_economicos | `(texto: str, *, ledger: dict \| None = <default>, base_dir: Path \| str \| None = <default>, exigir: bool \| None = <default>) -> list[dict]` | 1147 | — |
| function | verificar_tudo | `(texto: str, *, ledger: dict \| None = <default>, revisao: dict \| None = <default>, base_dir: Path \| str \| None = <default>, tipo: str = <default>, exigir_criterio: bool = <default>, exigir_economico: bool \| None = <default>) -> list[dict]` | 1174 | — |


### `forja_learning.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | validate_feedback_assimilation | `(payload: dict) -> list[dict]` | 56 | — |
| function | validate_learning | `(payload: dict) -> list[dict]` | 158 | — |
| function | validate_case | `(case_dir: Path) -> dict` | 202 | — |
| function | main | `() -> None` | 207 | — |


### `forja_learning_registry.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | register_promoted_rule | `(*, source_case_id: str, candidate: dict, scope_key: str \| None) -> dict` | 33 | — |
| function | active_rules | `(*, case_id: str, product_type: str \| None = <default>, tribunal: str \| None = <default>) -> list[dict]` | 82 | — |
| function | suite_learning_findings | `(case_dir: Path, suite: dict) -> list[dict]` | 100 | — |


### `forja_ledger_material.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | montar | `(case_dir: Path, draft: Path) -> dict` | 87 | — |
| function | main | `(argv = <default>) -> int` | 167 | — |


### `forja_legal_search.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| class | LegalSearchError | `(RuntimeError)` | 22 | — |
| function | load_config | `(path: Path = <default>) -> dict` | 57 | — |
| class | TeiaJusBridge | `()` | 67 | — |
| method | TeiaJusBridge.__init__ | `(self, *, config_path: Path = <default>, telemetry_root: Path \| None = <default>, python_executable: str \| None = <default>) -> None` | 68 | — |
| method | TeiaJusBridge.read_actions | `(self) -> set[str]` | 90 | property |
| method | TeiaJusBridge.mutation_actions | `(self) -> set[str]` | 94 | property |
| method | TeiaJusBridge.denied_actions | `(self) -> set[str]` | 98 | property |
| method | TeiaJusBridge.execute | `(self, action: str, params: dict \| None = <default>, *, allow_mutation: bool = <default>, artifact_dir: Path \| None = <default>) -> dict` | 107 | — |
| function | main | `() -> None` | 287 | — |


### `forja_local_context.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | main | `()` | 65 | — |


### `forja_management_bridge.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | sync_after_event | `(case_dir: Path, event: dict) -> dict` | 20 | — |


### `forja_memoria_auditabilidade.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | sha256_file | `(path: Path, block_size: int = <default>) -> str` | 79 | — |
| function | build_payload | `(case_dir: Path, *, generated_at: str \| None = <default>) -> dict[str, Any]` | 288 | — |
| function | build_bundle | `(case_dir: Path, output_dir: Path \| None = <default>) -> dict[str, Any]` | 461 | — |
| function | validate_bundle | `(manifest_path: Path, *, expected_case_dir: Path \| None = <default>) -> dict[str, Any]` | 489 | — |
| function | main | `(argv: list[str] \| None = <default>) -> int` | 529 | — |


### `forja_metacognition.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | validate_metacognition | `(payload: dict) -> list[dict]` | 13 | — |
| function | validate_case | `(case_dir: Path) -> dict` | 43 | — |
| function | main | `() -> None` | 48 | — |


### `forja_metadata.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | retry_transient_io | `(operation, *, tries: int = <default>, base_delay: float = <default>)` | 22 | — |
| function | sanitize_docx | `(path: Path) -> None` | 62 | — |
| function | sanitize_pdf | `(path: Path) -> None` | 86 | — |
| function | sanitize_final_artifacts | `(docx: str \| Path, pdf: str \| Path) -> None` | 108 | — |


### `forja_metricas_f7.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | tribunal_numero_cnj | `(value)` | 18 | — |
| function | extrair_citacoes_basico | `(md_texto)` | 23 | — |
| function | cache_com_lastro | `(path, *, require_live = <default>)` | 36 | — |
| function | procurar_em_cache_oficial | `(citacao, *, require_live = <default>)` | 55 | — |
| function | extrair_marcadores_verificar | `(md_texto)` | 97 | — |
| function | metricas_f7 | `(md_texto, *, require_live = <default>)` | 112 | — |


### `forja_metricas_gates.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | coletar | `()` | 47 | — |
| function | main | `(argv = <default>)` | 127 | — |


### `forja_modelos.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| class | ForjaModeloError | `(RuntimeError)` | 46 | — |
| class | Modelo | `()` | 51 | dataclass(frozen=True) |
| function | modelo_remoto_proibido | `(remoto: str \| None) -> bool` | 150 | — |
| class | Orcamento | `()` | 175 | dataclass |
| method | Orcamento.restante | `(self) -> float` | 182 | — |
| method | Orcamento.registrar | `(self, recibo: dict) -> None` | 185 | — |
| function | custo_usd | `(modelo: Modelo, entrada: int, saida: int) -> float` | 204 | — |
| function | chamar | `(modelo_id: str, prompt: str, *, sistema: str \| None = <default>, max_tokens: int = <default>, timeout: int = <default>, fase: str \| None = <default>, papel: str \| None = <default>, orcamento: Orcamento \| None = <default>, registrar: bool = <default>) -> dict` | 250 | — |
| function | registrar_no_ledger | `(recibo: dict) -> None` | 317 | — |
| function | familia_de | `(modelo_id: str) -> str` | 326 | — |
| function | revisores_de | `(modelo_id: str, *, fase: str \| None = <default>) -> list[str]` | 333 | — |
| function | modelos_da_fase | `(fase: str) -> list[str]` | 346 | — |
| function | gasto_acumulado | `() -> dict` | 350 | — |
| function | main | `() -> None` | 375 | — |


### `forja_mutation_semantic.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | rodar | `(suite: dict, draft_path: Path) -> dict` | 179 | — |
| function | main | `(argv = <default>) -> int` | 286 | — |


### `forja_n3_common.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | name_with_legacy | `(name: str) -> tuple[str, ...]` | 43 | — |
| function | resolve_name | `(name: str, available) -> str \| None` | 48 | — |
| class | ForjaN3Error | `(RuntimeError)` | 56 | — |
| class | RevisionConflict | `(ForjaN3Error)` | 60 | — |
| class | TransitionError | `(ForjaN3Error)` | 64 | — |
| class | LockTimeout | `(ForjaN3Error)` | 68 | — |
| function | now_iso | `() -> str` | 72 | — |
| function | new_id | `(prefix: str) -> str` | 76 | — |
| function | read_json | `(path: Path, fallback: Any = <default>) -> Any` | 80 | — |
| function | atomic_write_text | `(path: Path, text: str, *, encoding: str = <default>) -> None` | 87 | — |
| function | atomic_write_json | `(path: Path, payload: Any) -> None` | 101 | — |
| function | sha256_bytes | `(value: bytes) -> str` | 105 | — |
| function | sha256_file | `(path: Path) -> str` | 109 | — |
| function | canonical_hash | `(payload: Any) -> str` | 117 | — |
| function | load_config | `() -> dict` | 122 | — |
| function | feature_enabled | `(name: str) -> bool` | 129 | — |
| function | resolve_case_dir | `(case_key: str \| Path, *, state_root: Path \| None = <default>) -> Path` | 133 | — |
| function | ensure_within | `(path: Path, root: Path) -> Path` | 150 | — |
| class | InterProcessLock | `()` | 170 | — |
| method | InterProcessLock.__init__ | `(self, path: Path, *, timeout: float = <default>, stale_after: float = <default>)` | 173 | — |


### `forja_n3_shadow_replay.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | replay_case | `(case_dir: Path, *, label: str \| None, state_root: Path) -> dict` | 113 | — |
| function | run_replay | `(state_root: Path, output_json: Path, output_md: Path) -> dict` | 226 | — |
| function | main | `() -> None` | 255 | — |


### `forja_n4_anti_fraud_audit.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | evaluate | `(snapshot: dict) -> dict` | 40 | — |
| function | run | `() -> dict` | 106 | — |


### `forja_n4_baseline.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | run | `(*, initialize_n3: bool) -> dict` | 32 | — |
| function | main | `() -> None` | 74 | — |


### `forja_n4_common.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | issue | `(code: str, detail: str, *, severity: str = <default>, artifact: str \| None = <default>) -> dict` | 99 | — |
| function | semantic_payload | `(payload: dict) -> dict` | 106 | — |
| function | expected_content_hash | `(payload: dict) -> str` | 110 | — |
| function | artifact_path | `(case_dir: Path, filename: str) -> Path` | 114 | — |
| function | build_envelope | `(case_dir: Path, filename: str, content: dict, *, source_hashes: list[str], producer_run_id: str, reviewer_run_id: str \| None = <default>, applicability: str = <default>, status: str = <default>) -> dict` | 120 | — |
| function | write_artifact | `(case_dir: Path, filename: str, payload: dict) -> Path` | 158 | — |
| function | append_trace | `(case_dir: Path, action: str, *, run_id: str, detail: dict, status: str = <default>) -> None` | 173 | — |
| function | validate_envelope | `(case_dir: Path, filename: str, payload: Any) -> list[dict]` | 186 | — |
| function | load_artifact | `(case_dir: Path, filename: str) -> dict \| None` | 226 | — |
| function | validate_file | `(case_dir: Path, filename: str, validator: Callable[[dict], list[dict]] \| None = <default>) -> tuple[dict \| None, list[dict]]` | 230 | — |
| function | ids_unique | `(items: list[dict], key: str, code: str) -> list[dict]` | 242 | — |


### `forja_n4_corpus.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | run | `() -> dict` | 27 | — |


### `forja_n4_e2e_adversarial.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | run | `(source: Path = <default>) -> dict` | 41 | — |
| function | main | `() -> None` | 137 | — |


### `forja_n4_invalidation.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | invalidate | `(case_dir: Path, trigger: str, *, reason: str, actor: str = <default>) -> dict` | 32 | — |
| function | main | `() -> None` | 59 | — |


### `forja_n4_m6_cycles.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | run | `(key: str) -> dict` | 87 | — |


### `forja_n4_m6_prepare.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | prepare | `(key: str) -> dict` | 82 | — |
| function | approve | `(key: str, reviewer: str) -> dict` | 119 | — |
| function | main | `() -> None` | 144 | — |


### `forja_n4_pilot_cafelana.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | run | `() -> dict` | 21 | — |


### `forja_n4_pilot_science.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | run | `() -> dict` | 27 | — |


### `forja_n4_validate.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | effective_signature_lite_mode | `(config: dict, case_dir: Path, override: str \| None = <default>) -> tuple[str, str]` | 384 | — |
| function | validate_case | `(case_dir: Path, *, target_phase: str \| None = <default>, write: bool = <default>, mode_override: str \| None = <default>) -> dict` | 435 | — |
| function | management_summary | `(case_dir: Path) -> dict` | 564 | — |
| function | main | `() -> None` | 656 | — |


### `forja_official_sources.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| method | _OfficialHtmlText.__init__ | `(self) -> None` | 45 | — |
| method | _OfficialHtmlText.handle_starttag | `(self, tag: str, attrs) -> None` | 50 | — |
| method | _OfficialHtmlText.handle_endtag | `(self, tag: str) -> None` | 54 | — |
| method | _OfficialHtmlText.handle_data | `(self, data: str) -> None` | 58 | — |
| function | normalize_evidence_text | `(value: str) -> str` | 63 | — |
| function | source_excerpt_sha256 | `(value: str) -> str` | 72 | — |
| function | validate_live_official_source | `(path: Path, record: dict, *, required_excerpt: str \| None = <default>, fetcher = <default>) -> dict` | 166 | — |
| function | build_manifest | `(cache_dir: Path = <default>, output: Path = <default>) -> dict` | 300 | — |
| function | validate_cached_source | `(path: Path, manifest_path: Path = <default>, *, cache_dir: Path = <default>, require_live: bool = <default>, required_excerpt: str \| None = <default>, fetcher = <default>) -> dict` | 334 | — |
| function | sidecar_path | `(source: Path) -> Path` | 376 | — |
| function | validate_archived_source | `(path: Path, *, require_live: bool = <default>, required_excerpt: str \| None = <default>, fetcher = <default>) -> dict` | 380 | — |
| function | validate_source_path | `(path: Path, *, require_live: bool = <default>, required_excerpt: str \| None = <default>, fetcher = <default>) -> dict` | 447 | — |
| function | main | `() -> int` | 472 | — |


### `forja_p0.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | validar_p0 | `(resultado, *, produtor = <default>, revisor = <default>)` | 105 | — |


### `forja_package.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | release_policy_hash | `() -> str` | 48 | — |
| function | validate_f7 | `(artifact: dict, *, document_key: str \| None, release_policy: str, markdown: dict) -> dict` | 153 | — |
| function | validate_source_ledger | `(artifact: dict, *, release_policy: str, expected_citations: list[dict] \| None = <default>, markdown: dict \| None = <default>, case_dir: Path \| None = <default>) -> dict` | 292 | — |
| function | validate_context_artifact | `(artifact: dict, *, markdown: dict, release_policy: str) -> dict` | 420 | — |
| function | validate_fidelity | `(artifact: dict, *, files: dict) -> dict` | 435 | — |
| function | validate_adversarial_bundle | `(state: dict, item: dict) -> dict` | 506 | — |
| function | validate_definition | `(case_dir: Path, definition: dict) -> dict` | 554 | — |
| function | build_package | `(case_dir: Path, definition_path: Path, *, publish_pointer: bool = <default>) -> dict` | 767 | — |
| function | revalidate_package_manifest | `(case_dir: Path, manifest: dict) -> dict` | 851 | — |


### `forja_paragrafos.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | validar_paragrafos_lastreados | `(prov, draft_texto = <default>)` | 117 | — |
| function | carregar_e_validar | `(pasta)` | 212 | — |


### `forja_phase_contracts.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | load_contract | `(phase: str) -> dict` | 14 | — |
| function | validate_all | `() -> list[dict]` | 49 | — |


### `forja_pilot_m4.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | append_unique_many | `(existing, values)` | 42 | — |
| function | limpar_corpo | `(doc)` | 50 | — |
| function | eh_titulo | `(texto)` | 58 | — |
| function | montar_piloto | `(case_key, peca_fonte)` | 67 | — |


### `forja_post_protocol.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | safe_component | `(value: str, fallback: str, *, limit: int = <default>) -> str` | 105 | — |
| function | content_key | `(case_id: str, attachment_hash: str) -> str` | 111 | — |
| function | evidence_key | `(account_id: str, thread_id: str, message_id: str, attachment_id: str) -> str` | 115 | — |
| function | resolve_ai_baseline | `(case_dir: Path, *, received_at: str) -> tuple[dict \| None, list[str]]` | 179 | — |
| function | backfill_baseline_from_gmail | `(case_dir: Path, demand: dict, *, human_suffix: str, received_at: str, get_message, get_attachment, shadow: bool) -> dict \| None` | 286 | — |
| function | classify_protocol | `(human_path: Path, *, declaration_text: str = <default>, evidence_paths: list[Path] \| None = <default>, explicit_links: list[dict] \| None = <default>) -> tuple[str, list[dict], list[str]]` | 447 | — |
| function | ingest_return | `(case_dir: Path, attachment_path: Path, *, account_id: str, thread_id: str, message_id: str, attachment_id: str, received_at: str, original_name: str \| None = <default>, piece_name: str = <default>, process_id: str = <default>, declaration_text: str = <default>, evidence_paths: list[Path] \| None = <default>, explicit_evidence_links: list[dict] \| None = <default>, producer_run_id: str \| None = <default>) -> dict` | 777 | — |
| function | promote_learning | `(case_dir: Path, candidate_id: str, *, content_key_value: str = <default>, approved_by: str, fixture_id: str, test_id: str, evidence_runs: list[str], evidence_case_ids: list[str] \| None = <default>, scope: str = <default>, scope_key: str \| None = <default>) -> dict` | 1269 | — |
| function | resolve_learning_origin | `(case_dir: Path, candidate_id: str, *, content_key_value: str, origin: str, evidence_id: str, decided_by: str) -> dict` | 1485 | — |
| function | rebuild_comparison | `(case_dir: Path, ckey: str, *, producer_run_id: str \| None = <default>) -> dict` | 1539 | — |
| function | scan_gmail | `(*, query: str, max_results: int = <default>, shadow: bool = <default>) -> dict` | 1762 | — |
| function | main | `() -> None` | 1995 | — |


### `forja_post_protocol_contracts.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | validate_post_protocol_return | `(payload: dict) -> list[dict]` | 104 | — |
| function | validate_protocol_evidence | `(payload: dict) -> list[dict]` | 125 | — |
| function | validate_document_comparison | `(payload: dict) -> list[dict]` | 165 | — |
| function | validate_learning_candidate | `(payload: dict) -> list[dict]` | 185 | — |
| function | validate_post_protocol_baseline_backfill | `(payload: dict) -> list[dict]` | 246 | — |


### `forja_precedente.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | validate_legal_research_trace | `(payload: dict, mode: str = <default>, *, denied_actions: set[str] \| None = <default>, case_dir: Path \| None = <default>) -> list[dict]` | 66 | — |
| function | validate_anchor_cards | `(entries: list[dict], *, selected_route_id: str \| None = <default>, compared_route_ids: set[str] \| None = <default>) -> list[dict]` | 294 | — |
| function | anchor_ids | `(entries: list[dict]) -> set[str]` | 407 | — |
| function | failed_anchor_routes | `(findings: list[dict], entries: list[dict]) -> set[str]` | 416 | — |


### `forja_produto.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | validar_definicao_produto | `(classificacao)` | 96 | — |
| function | validar_pergunta_jurisdicional | `(blueprint)` | 136 | — |
| function | validar_uso_final | `(ledger)` | 168 | — |


### `forja_pso_pet.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | issue | `(code: str, detail: str, *, severity: str = <default>, dimension: str \| None = <default>) -> dict` | 26 | — |
| function | validate_plan | `(payload: dict) -> list[dict]` | 96 | — |
| function | measure_plan | `(payload: dict) -> dict` | 272 | — |
| function | audit_n4_case | `(case_dir: Path) -> dict` | 371 | — |
| function | mutation_benchmark | `() -> dict` | 536 | — |
| function | benchmark | `(state_root: Path) -> dict` | 588 | — |
| function | main | `() -> None` | 610 | — |


### `forja_qa_paginas.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | analisar_pasta | `(pasta: Path) -> dict` | 48 | — |
| function | main | `(argv = <default>) -> int` | 103 | — |


### `forja_reasoning.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | validate_question_tree | `(payload: dict) -> list[dict]` | 31 | — |
| function | validate_coverage | `(payload: dict) -> list[dict]` | 89 | — |
| function | validate_graph | `(payload: dict) -> list[dict]` | 138 | — |
| function | validate_theses | `(payload: dict) -> list[dict]` | 160 | — |
| function | validate_conducts | `(payload: dict) -> list[dict]` | 184 | — |
| function | validate_decision_factors | `(payload: dict) -> list[dict]` | 199 | — |
| function | nivel_probatorio | `(kind: str \| None) -> str` | 237 | — |
| function | validate_recipient_map | `(payload: dict, *, freshness_hours: int \| None = <default>, agora: datetime \| None = <default>) -> list[dict]` | 262 | — |
| function | validate_signature_brief | `(payload: dict) -> list[dict]` | 352 | — |
| function | validate_brief_references | `(brief: dict, case_dir: Path) -> list[dict]` | 445 | — |
| function | validate_case | `(case_dir: Path) -> dict` | 520 | — |
| function | main | `() -> None` | 535 | — |


### `forja_recomputo_censo.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | censo | `(raiz = <default>) -> dict` | 260 | — |


### `forja_reconcile.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | classificar_integracoes | `(status, bridge)` | 38 | — |
| function | finding | `(code, severity, detail)` | 65 | — |
| function | reconciliar_gates | `(gates_anteriores, historico_anterior, findings, *, at)` | 69 | — |
| function | evidencia_de_entrega | `(item, entregas, manual_entry)` | 114 | — |
| function | auditar_demanda | `(item, entregas, manual_items, pastas_vistas, threads_vistos)` | 134 | — |
| function | gravar_state | `(demanda, findings, case_status, evidence, integracoes)` | 197 | — |
| function | main | `()` | 250 | — |


### `forja_red_team.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | validar_red_team | `(relatorio)` | 47 | — |
| function | validar_recheck_adversarial | `(recheck)` | 98 | — |
| function | validar_exame_adversarial | `(relatorio, recheck)` | 174 | — |


### `forja_redacao.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | validar_redacao | `(prov, draft_texto = <default>)` | 54 | — |


### `forja_regimento_gate.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | validar_regimento | `(sources_map, fact_ledger = <default>)` | 114 | — |


### `forja_regimentos.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| class | Regimento | `()` | 152 | dataclass |
| method | Regimento.bloqueia | `(self) -> bool` | 163 | property |
| function | auditar_arquivo | `(caminho: Path, *, hoje: date, limite_dias: int) -> Regimento` | 167 | — |
| function | auditar | `(raiz: Path, *, hoje: date \| None = <default>, limite_dias: int = <default>) -> list[Regimento]` | 212 | — |
| function | main | `() -> int` | 243 | — |


### `forja_regua.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | sha256_arquivo | `(path)` | 282 | — |
| function | hashes_atuais | `()` | 291 | — |
| function | verificar_integridade | `(manifest = <default>)` | 296 | — |
| function | rebaseline | `(motivo)` | 322 | — |
| function | rodar_suite | `(nome, timeout = <default>)` | 350 | — |
| function | main | `()` | 373 | — |


### `forja_release_audit.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | audit_packages | `(state_root: Path) -> dict` | 13 | — |
| function | main | `() -> int` | 46 | — |


### `forja_render_docx.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | limpar_corpo | `(doc)` | 40 | — |
| function | add_runs_com_negrito | `(p, texto, base_bold = <default>)` | 47 | — |
| function | eh_assinatura | `(linha, contexto_pos_deferimento)` | 69 | — |
| function | render | `(md_path, out_dir, titulo = <default>, tipo = <default>, *, case_dir = <default>, ledger_path = <default>, base_dir = <default>)` | 85 | — |


### `forja_replay.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | validar_replay | `(ledger, *, hoje = <default>, limite_dias = <default>)` | 82 | — |


### `forja_run.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | prepare_attempt | `(case_dir: Path, phase: str, *, expected_revision: int, run_id: str \| None = <default>, actor: str = <default>) -> dict` | 90 | — |
| function | promote_attempt | `(case_dir: Path, attempt_dir: Path, *, expected_revision: int, actor: str = <default>) -> dict` | 1103 | — |
| function | block_phase | `(case_dir: Path, phase: str, *, expected_revision: int, reason: str, blockers: list[str]) -> dict` | 1178 | — |
| function | main | `() -> None` | 1190 | — |


### `forja_run_metrics.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | build_metrics | `(case_dir: Path) -> dict` | 22 | — |
| function | write_metrics | `(case_dir: Path, output: Path \| None = <default>) -> dict` | 121 | — |
| function | main | `() -> None` | 128 | — |


### `forja_science.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | crossref_search | `(query: str, *, rows: int = <default>) -> dict` | 28 | — |
| function | crossref_by_doi | `(doi: str) -> dict` | 36 | — |
| function | pubmed_search | `(query: str, *, rows: int = <default>) -> dict` | 49 | — |
| function | ncbi_fetch | `(identifier: str, *, database: str = <default>) -> dict` | 62 | — |
| function | openalex_search | `(query: str, *, rows: int = <default>, api_key: str \| None = <default>) -> dict` | 76 | — |
| function | discover | `(query: str, *, rows: int = <default>) -> dict` | 87 | — |
| function | normalize_doi | `(value: object) -> str \| None` | 93 | — |
| function | validate_classification | `(payload: dict) -> list[dict]` | 103 | — |
| function | validate_protocol | `(payload: dict) -> list[dict]` | 116 | — |
| function | validate_studies | `(payload: dict) -> list[dict]` | 127 | — |
| function | validate_claims | `(payload: dict, study_ledger: dict \| None = <default>) -> list[dict]` | 171 | — |
| function | validate_synthesis | `(payload: dict) -> list[dict]` | 198 | — |
| function | validate_audit | `(payload: dict) -> list[dict]` | 210 | — |
| function | validate_case | `(case_dir: Path) -> dict` | 222 | — |
| function | main | `() -> None` | 244 | — |


### `forja_sources.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | classificar_produto | `(texto)` | 32 | — |
| function | detectar_tribunal | `(texto)` | 45 | — |
| function | validar_regimento | `(path)` | 65 | — |
| function | localizar_regimento | `(tribunal, case_folder)` | 81 | — |
| function | merge_by_id | `(existing, new_items)` | 94 | — |
| function | merge_gates | `(existing, new_items)` | 107 | — |
| function | append_unique | `(existing, value)` | 119 | — |
| function | processar_caso | `(state_path)` | 126 | — |
| function | main | `()` | 246 | — |


### `forja_state_machine.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | event_paths | `(case_dir: Path) -> list[Path]` | 100 | — |
| function | load_events | `(case_dir: Path) -> list[dict]` | 108 | — |
| function | derive_state | `(case_dir: Path, events: list[dict] \| None = <default>) -> dict` | 162 | — |
| function | record_event | `(case_dir: Path, event_type: str, *, expected_revision: int, idempotency_key: str, phase: str \| None = <default>, actor: str = <default>, run_id: str \| None = <default>, attempt_id: str \| None = <default>, demand_id: str \| None = <default>, artifact_hashes: dict \| None = <default>, payload: dict \| None = <default>) -> tuple[dict, dict, bool]` | 357 | — |
| function | tempfile_event | `(directory: Path, event_id: str) -> tuple[int, str]` | 436 | — |
| function | initialize_case | `(case_dir: Path, *, demand_id: str \| None = <default>, from_legacy: bool = <default>) -> dict` | 442 | — |
| function | main | `() -> None` | 491 | — |


### `forja_svg_docx.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | inserir_svgs | `(docx_path: str \| Path, figuras: dict) -> dict` | 193 | — |


### `forja_varredura_tipografica.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | varrer | `(raiz = <default>, piso = <default>) -> dict` | 188 | — |


### `forja_verificador.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | gate_g11 | `(texto, fontes = <default>)` | 161 | — |
| function | gate_g1 | `(texto)` | 210 | — |
| function | gate_g2 | `(texto, tipo = <default>)` | 231 | — |
| function | gate_g3 | `(texto)` | 258 | — |
| function | gate_g4 | `(texto)` | 268 | — |
| function | gate_g5 | `(texto)` | 290 | — |
| function | gate_g6 | `(texto, tipo = <default>)` | 302 | — |
| function | gate_g7 | `(texto)` | 317 | — |
| function | gate_g8 | `(texto, tipo)` | 334 | — |
| function | gate_g9 | `(texto, tipo)` | 354 | — |
| function | verificar | `(texto, tipo = <default>, *, ledger = <default>, base_dir = <default>, case_dir = <default>, exigir_economico = <default>)` | 410 | — |


### `forja_visual.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| method | _Mapa.__init__ | `(self, mapa, texto_md)` | 83 | — |
| function | compor | `(md_path, out_docx, mapa, *, case_dir = <default>, ledger_path = <default>, base_dir = <default>)` | 145 | — |


### `forja_visual_build.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | build | `(md_path, out_dir, titulo = <default>, tipo = <default>, montar_word = <default>, *, case_dir = <default>, ledger_path = <default>, base_dir = <default>)` | 44 | — |


### `forja_visual_figuras.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | extrair_cronologia | `(texto_md, minimo = <default>, maximo = <default>)` | 152 | — |
| function | carregar_brief | `(md_path)` | 220 | — |
| function | validar_brief | `(brief, texto_md)` | 229 | — |
| function | extrair_encadeamento | `(texto_md, brief = <default>, minimo = <default>, maximo = <default>)` | 267 | — |
| function | extrair_comparacao | `(texto_md, min_linhas = <default>, max_linhas = <default>)` | 287 | — |
| function | gerar_figuras | `(texto_md, out_dir, mapa, largura_cm = <default>, brief = <default>)` | 313 | — |


### `forja_visual_mapa_gen.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | gerar_mapa | `(md_path, tipo = <default>, com_figuras = <default>, max_pulls = <default>, max_caixas = <default>)` | 328 | — |
| function | gravar_mapa | `(md_path, destino = <default>, **kw)` | 499 | — |


### `forja_visual_qa.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | lint_text | `(text: str) -> list[dict]` | 27 | — |
| function | lint_docx | `(path: Path) -> dict` | 41 | — |
| function | inspect_pdf | `(pdf: Path, qa_dir: Path, *, generator_run_id: str, reviewer_run_id: str, dpi: int = <default>) -> dict` | 62 | — |
| function | run_visual_qa | `(pdf: Path, output: Path, *, qa_dir: Path, generator_run_id: str, reviewer_run_id: str, docx: Path \| None = <default>, markdown: Path \| None = <default>, fidelity_output: Path \| None = <default>, svgs: list[Path] \| None = <default>, manual_review: Path \| None = <default>, pending_review_output: Path \| None = <default>, layout_exceptions: Path \| None = <default>) -> dict` | 127 | — |
| function | main | `() -> None` | 221 | — |


### `forja_visual_qa_structural.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | auditar_documento | `(docx: str \| Path, *, markdown: str \| Path \| None = <default>, svgs: list[str \| Path] \| None = <default>) -> dict` | 94 | — |
| function | write_audit | `(docx: str \| Path, output: str \| Path, *, markdown = <default>, svgs = <default>) -> dict` | 127 | — |


### `forja_visual_review.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | build_pending_review | `(output: Path, *, pdf: Path, rendered_pages: list[dict], generator_run_id: str, docx: Path \| None = <default>) -> dict` | 48 | — |
| function | validate_visual_review | `(review_path: Path, *, pdf: Path, rendered_pages: list[dict], generator_run_id: str, expected_reviewer_run_id: str \| None = <default>, docx: Path \| None = <default>) -> dict` | 86 | — |


### `generate_n4_contracts.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | generate | `() -> None` | 545 | — |


### `render_forja_atlas.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | slugify | `(value: str) -> str` | 22 | — |
| function | mermaid_command | `() -> str` | 28 | — |
| function | namespace_svg_ids | `(svg: str, diagram_index: int) -> str` | 35 | — |
| function | render_diagrams | `(markdown: str, assets: Path) -> tuple[str, list[dict]]` | 49 | — |
| function | build_html | `(source: Path, output: Path) -> dict` | 104 | — |
| function | main | `() -> None` | 284 | — |


### `validate_forja_n3.py`

Linguagem: `python`. Contratos públicos observados:

| Tipo | Símbolo | Assinatura | Linha | Decoradores |
| --- | --- | --- | --- | --- |
| function | run_command | `(name: str, command: list[str], *, timeout: int) -> dict` | 54 | — |
| function | validate_json_files | `() -> dict` | 88 | — |
| function | main | `() -> None` | 101 | — |


## 5. Entradas de linha de comando

### `forja_adocao_rota.py` → `<global>`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| --ultimas | não/declarativo | — | 224 |
| --json | não/declarativo | — | 225 |


### `forja_adversarial_audit.py` → `<global>`

_Nenhum item observado neste escopo._


### `forja_adversarial_audit.py` → `init`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| source | não/declarativo | — | 486 |
| output | não/declarativo | — | 487 |


### `forja_adversarial_audit.py` → `not-applicable`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| output | não/declarativo | — | 489 |
| --reason | sim | — | 490 |


### `forja_adversarial_audit.py` → `prompt`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| phase | não/declarativo | — | 496 |


### `forja_adversarial_audit.py` → `validate`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| ledger | não/declarativo | — | 492 |
| --source | não/declarativo | — | 493 |
| --output | não/declarativo | — | 494 |


### `forja_ar_architecture.py` → `<global>`

_Nenhum item observado neste escopo._


### `forja_ar_architecture.py` → `create`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| candidate_id | não/declarativo | — | 547 |
| --title | sim | — | 548 |
| --problem | sim | — | 549 |
| --hypothesis | sim | — | 550 |
| --scope | sim | — | 551 |


### `forja_ar_architecture.py` → `evaluate`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| candidate_id | não/declarativo | — | 553 |
| --review | sim | — | 554 |


### `forja_ar_blind.py` → `<global>`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| --prepare | não/declarativo | — | 254 |
| --consolidate | não/declarativo | — | 255 |
| --pair-id | sim | — | 256 |
| --runpair-dir | não/declarativo | — | 257 |
| --blind-dir | sim | — | 258 |
| --judgment | não/declarativo | — | 259 |


### `forja_ar_canarios.py` → `<global>`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| --verificar | sim | — | 124 |
| --secreto | não/declarativo | — | 125 |
| --manifest | não/declarativo | — | 126 |


### `forja_ar_ciclo.py` → `<global>`

_Nenhum item observado neste escopo._


### `forja_ar_ciclo.py` → `human-approve`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| --decision | sim | — | 414 |
| --receipt | sim | — | 415 |


### `forja_ar_ciclo.py` → `independent-review`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| --decision | sim | — | 409 |
| --parecer | sim | — | 410 |
| --familia | sim | — | 411 |
| --familia-geradora | sim | — | 412 |


### `forja_ar_ciclo.py` → `promotion`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| --cycle-dir | sim | — | 400 |
| --manifest | sim | — | 401 |
| --comparison | não/declarativo | — | 402 |
| --canary | não/declarativo | — | 403 |
| --judgment | não/declarativo | — | 404 |
| --no-sealed | não/declarativo | — | 405 |
| --variant-sha | não/declarativo | — | 406 |
| --sealed-eval | não/declarativo | — | 407 |


### `forja_ar_ciclo.py` → `relatorio`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| --cycle-dir | sim | — | 417 |
| --panel | sim | — | 418 |
| --output | não/declarativo | — | 419 |


### `forja_ar_ciclo.py` → `snapshot`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| --cycle-dir | sim | — | 395 |
| --manifest | sim | — | 396 |
| --corpus | não/declarativo | — | 397 |
| --log | não/declarativo | — | 398 |


### `forja_ar_ciclo.py` → `verify-log`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| --log | sim | — | 393 |


### `forja_ar_corpus.py` → `<global>`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| --scan | não/declarativo | — | 316 |
| --check | não/declarativo | — | 317 |
| --report | não/declarativo | — | 318 |
| --state-dir | não/declarativo | — | 319 |
| --manifest | não/declarativo | — | 320 |


### `forja_ar_evolucao.py` → `<global>`

_Nenhum item observado neste escopo._


### `forja_ar_evolucao.py` → `convergencia`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| --experimento | sim | — | 184 |


### `forja_ar_evolucao.py` → `init`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| --experimento | sim | — | 173 |
| --alvo | sim | — | 174 |


### `forja_ar_evolucao.py` → `nova-geracao`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| --experimento | sim | — | 176 |
| --variantes | sim | — | 177 |


### `forja_ar_evolucao.py` → `selecionar`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| --experimento | sim | — | 179 |
| --geracao | sim | — | 180 |
| --resultados | sim | — | 181 |


### `forja_ar_indicadores.py` → `<global>`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| --md | não/declarativo | — | 325 |
| --comparar | não/declarativo | — | 326 |
| --caso | não/declarativo | — | 327 |
| --painel | não/declarativo | — | 328 |
| --ledgers | não/declarativo | — | 329 |
| --split | não/declarativo | ('train', 'holdout') | 330 |
| --manifest | não/declarativo | — | 331 |


### `forja_ar_runpair.py` → `<global>`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| --freeze | não/declarativo | — | 165 |
| --register | não/declarativo | — | 166 |
| --validate | não/declarativo | — | 167 |
| --runpair-dir | sim | — | 168 |
| --caso | não/declarativo | — | 169 |
| --alvo | não/declarativo | — | 170 |
| --lado | não/declarativo | ('vigente', 'variante') | 171 |
| --manifest | não/declarativo | — | 172 |
| --claims-ledger | não/declarativo | — | 173 |
| --authorities-ledger | não/declarativo | — | 174 |
| --repeticao | não/declarativo | — | 175 |


### `forja_artefatos.py` → `<global>`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| --json | não/declarativo | — | 226 |


### `forja_assinatura_visual.py` → `<global>`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| docx | não/declarativo | — | 322 |
| --paginas | não/declarativo | — | 323 |
| --tipo | não/declarativo | — | 324 |
| --saida | não/declarativo | — | 325 |


### `forja_axi.py` → `<global>`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| --version | não/declarativo | — | 794 |


### `forja_axi.py` → `case`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| case_id | não/declarativo | — | 806 |
| --fields | não/declarativo | — | 807 |
| --full | não/declarativo | — | 808 |


### `forja_axi.py` → `cases`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| --status | não/declarativo | — | 800 |
| --limit | não/declarativo | — | 801 |
| --fields | não/declarativo | — | 802 |
| --full | não/declarativo | — | 803 |


### `forja_axi.py` → `commands`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| name | não/declarativo | — | 823 |


### `forja_axi.py` → `health`

_Nenhum item observado neste escopo._


### `forja_axi.py` → `home`

_Nenhum item observado neste escopo._


### `forja_axi.py` → `queue`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| --section | não/declarativo | ('all', *QUEUE_SECTIONS) | 811 |
| --limit | não/declarativo | — | 816 |
| --fields | não/declarativo | — | 817 |
| --full | não/declarativo | — | 818 |


### `forja_baseline.py` → `<global>`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| --json | não/declarativo | — | 202 |
| --quiet | não/declarativo | — | 203 |


### `forja_baseline_aprovado.py` → `<global>`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| --gravar | não/declarativo | — | 159 |


### `forja_bench_modelos.py` → `<global>`

_Nenhum item observado neste escopo._


### `forja_bench_modelos.py` → `reavaliar`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| --arquivo | sim | — | 328 |


### `forja_bench_modelos.py` → `rodar`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| --modelos | não/declarativo | — | 322 |
| --teto-usd | não/declarativo | — | 323 |
| --condicoes | não/declarativo | — | 324 |


### `forja_bench_modelos.py` → `ver`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| --arquivo | não/declarativo | — | 326 |


### `forja_calibra_monetario.py` → `<global>`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| --raiz | não/declarativo | — | 168 |
| --saida | não/declarativo | — | 169 |


### `forja_canario_catraca.py` → `<global>`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| --json | não/declarativo | — | 166 |
| --suite | não/declarativo | — | 167 |


### `forja_canario_mutacao.py` → `<global>`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| --json | não/declarativo | — | 330 |
| --limite | não/declarativo | — | 331 |


### `forja_case_tests.py` → `<global>`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| case | não/declarativo | — | 194 |
| draft | não/declarativo | — | 195 |
| --reviewer-run-id | sim | — | 196 |
| --producer-run-id | não/declarativo | — | 197 |
| --output | não/declarativo | — | 198 |


### `forja_claim_binding.py` → `<global>`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| markdown | não/declarativo | — | 93 |
| ledger | não/declarativo | — | 94 |
| output | não/declarativo | — | 95 |


### `forja_close_cycle.py` → `<global>`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| case | não/declarativo | — | 216 |


### `forja_close_cycle.py` → `confirm-delivery`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| evidence | não/declarativo | — | 225 |
| --expected-revision | sim | — | 226 |


### `forja_close_cycle.py` → `fulfill`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| --expected-revision | sim | — | 228 |


### `forja_close_cycle.py` → `package`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| definition | não/declarativo | — | 219 |
| --expected-revision | sim | — | 220 |


### `forja_close_cycle.py` → `register-draft`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| receipt | não/declarativo | — | 222 |
| --expected-revision | sim | — | 223 |


### `forja_consistency.py` → `<global>`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| case | não/declarativo | — | 254 |


### `forja_context.py` → `<global>`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| case_dir | não/declarativo | — | 296 |


### `forja_delivery_integrity.py` → `<global>`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| case | não/declarativo | — | 131 |


### `forja_delivery_integrity.py` → `confirm`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| --mode | sim | ['channel_hash', 'artifact_evidence'] | 139 |
| --delivery-evidence-id | não/declarativo | — | 140 |
| --delivered-path | não/declarativo | — | 141 |
| --delivered-at | não/declarativo | — | 142 |
| --producer-run-id | sim | — | 143 |
| --reviewer-run-id | sim | — | 144 |


### `forja_delivery_integrity.py` → `select`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| artifact_id | não/declarativo | — | 134 |
| --layout-profile-id | sim | — | 135 |
| --producer-run-id | sim | — | 136 |
| --reviewer-run-id | sim | — | 137 |


### `forja_diabob.py` → `<global>`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| --arquivo | não/declarativo | — | 77 |
| --texto | não/declarativo | — | 78 |
| --modelo | não/declarativo | — | 79 |
| --caso | não/declarativo | — | 80 |
| --json | não/declarativo | — | 81 |


### `forja_document_compare.py` → `<global>`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| baseline | não/declarativo | — | 602 |
| human | não/declarativo | — | 603 |
| --json | sim | — | 604 |
| --markdown | sim | — | 605 |
| --protocol-status | não/declarativo | — | 606 |
| --baseline-artifact-id | não/declarativo | — | 607 |
| --human-artifact-id | não/declarativo | — | 608 |
| --allow-ocr | não/declarativo | — | 609 |


### `forja_docx_layout.py` → `<global>`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| docx | não/declarativo | — | 953 |
| --output | não/declarativo | — | 954 |
| --json | não/declarativo | — | 955 |
| --exceptions | não/declarativo | — | 956 |


### `forja_editorial.py` → `<global>`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| case | não/declarativo | — | 519 |
| attempt_dir | não/declarativo | — | 520 |
| --source | não/declarativo | — | 521 |
| --f7-gate | não/declarativo | — | 522 |
| --artifact-suffix | não/declarativo | — | 523 |
| --editor-model | não/declarativo | — | 524 |
| --reviewer-model | não/declarativo | — | 528 |
| --reviewer-session | não/declarativo | — | 532 |


### `forja_editorial_fidelity.py` → `<global>`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| audited | não/declarativo | — | 391 |
| final | não/declarativo | — | 392 |
| report | não/declarativo | — | 393 |


### `forja_email.py` → `<global>`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| --listar | não/declarativo | — | 128 |
| --enviar-rascunho | não/declarativo | — | 129 |
| --confirmar | não/declarativo | — | 130 |


### `forja_estilo_humano.py` → `<global>`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| arquivo | não/declarativo | — | 551 |
| --tipo | não/declarativo | ('peca', 'estudo', 'email') | 552 |


### `forja_exploracao_100.py` → `<global>`

_Nenhum item observado neste escopo._


### `forja_exploracao_100.py` → `init`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| --case-id | sim | — | 790 |
| --case-anchor | sim | — | 791 |
| --output | sim | — | 792 |


### `forja_exploracao_100.py` → `record-response`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| path | não/declarativo | — | 801 |
| --response | sim | — | 802 |


### `forja_exploracao_100.py` → `render-consultation`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| path | não/declarativo | — | 798 |
| --output | sim | — | 799 |


### `forja_exploracao_100.py` → `select-consultation`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| path | não/declarativo | — | 796 |


### `forja_exploracao_100.py` → `validate`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| path | não/declarativo | — | 794 |


### `forja_fidelity.py` → `<global>`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| markdown | não/declarativo | — | 264 |
| docx | não/declarativo | — | 265 |
| pdf | não/declarativo | — | 266 |
| output | não/declarativo | — | 267 |


### `forja_forma_artefatos.py` → `<global>`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| --json | não/declarativo | — | 144 |


### `forja_gate_liveness.py` → `<global>`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| --json | não/declarativo | — | 275 |
| --estrito | não/declarativo | — | 276 |


### `forja_headless.py` → `<global>`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| case | não/declarativo | — | 201 |
| phase | não/declarativo | — | 202 |
| prompt | não/declarativo | — | 203 |
| --attempt-dir | não/declarativo | — | 204 |


### `forja_import_audited_cycle.py` → `<global>`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| case | não/declarativo | — | 68 |
| source_dir | não/declarativo | — | 69 |


### `forja_learning.py` → `<global>`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| case | não/declarativo | — | 209 |


### `forja_legal_search.py` → `<global>`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| --db | não/declarativo | — | 223 |


### `forja_legal_search.py` → `capabilities`

_Nenhum item observado neste escopo._


### `forja_legal_search.py` → `case`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| numero_cnj | não/declarativo | — | 242 |
| --include-raw | não/declarativo | — | 243 |
| --artifact-dir | não/declarativo | — | 244 |


### `forja_legal_search.py` → `execute`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| action | não/declarativo | — | 247 |
| --params | não/declarativo | — | 248 |
| --allow-mutation | não/declarativo | — | 249 |
| --artifact-dir | não/declarativo | — | 250 |


### `forja_legal_search.py` → `health`

_Nenhum item observado neste escopo._


### `forja_legal_search.py` → `search`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| query | não/declarativo | — | 229 |
| --tribunal | não/declarativo | — | 230 |
| --phase | não/declarativo | — | 231 |
| --min-case-value | não/declarativo | — | 232 |
| --min-conviction-value | não/declarativo | — | 233 |
| --min-score | não/declarativo | — | 234 |
| --has-conviction-value | não/declarativo | — | 235 |
| --has-parties | não/declarativo | — | 236 |
| --limit | não/declarativo | — | 237 |
| --order | não/declarativo | ['potential', 'value', 'score', 'newest', 'cnj'] | 238 |
| --artifact-dir | não/declarativo | — | 239 |


### `forja_legal_search.py` → `stj-catalog`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| --dataset | não/declarativo | — | 255 |
| --include-resources | não/declarativo | — | 256 |
| --artifact-dir | não/declarativo | — | 257 |


### `forja_legal_search.py` → `stj-collect`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| --max | não/declarativo | — | 281 |
| --allow-mutation | não/declarativo | — | 282 |
| --artifact-dir | não/declarativo | — | 283 |


### `forja_legal_search.py` → `stj-daily`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| query | não/declarativo | — | 268 |
| --days | não/declarativo | — | 269 |
| --limit | não/declarativo | — | 270 |
| --include-text | não/declarativo | — | 271 |
| --match-mode | não/declarativo | ['all', 'any', 'phrase'] | 272 |
| --artifact-dir | não/declarativo | — | 273 |


### `forja_legal_search.py` → `stj-datajud`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| --limit | não/declarativo | — | 276 |
| --source-timeout | não/declarativo | — | 277 |
| --artifact-dir | não/declarativo | — | 278 |


### `forja_legal_search.py` → `stj-health`

_Nenhum item observado neste escopo._


### `forja_legal_search.py` → `stj-search`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| query | não/declarativo | — | 260 |
| --orgao | não/declarativo | — | 261 |
| --limit | não/declarativo | — | 262 |
| --resources-per-dataset | não/declarativo | — | 263 |
| --match-mode | não/declarativo | ['all', 'any', 'phrase'] | 264 |
| --artifact-dir | não/declarativo | — | 265 |


### `forja_memoria_auditabilidade.py` → `<global>`

_Nenhum item observado neste escopo._


### `forja_memoria_auditabilidade.py` → `build`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| case_dir | não/declarativo | — | 533 |
| --output-dir | não/declarativo | — | 534 |


### `forja_memoria_auditabilidade.py` → `validate`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| manifest | não/declarativo | — | 536 |
| --case-dir | não/declarativo | — | 537 |


### `forja_metacognition.py` → `<global>`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| case | não/declarativo | — | 50 |


### `forja_modelos.py` → `<global>`

_Nenhum item observado neste escopo._


### `forja_modelos.py` → `chamar`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| modelo | não/declarativo | — | 383 |
| prompt | não/declarativo | — | 384 |
| --max-tokens | não/declarativo | — | 385 |
| --fase | não/declarativo | — | 386 |
| --papel | não/declarativo | — | 387 |


### `forja_modelos.py` → `gasto`

_Nenhum item observado neste escopo._


### `forja_modelos.py` → `listar`

_Nenhum item observado neste escopo._


### `forja_n3_shadow_replay.py` → `<global>`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| --state-root | não/declarativo | — | 257 |
| --output-json | não/declarativo | — | 258 |
| --output-md | não/declarativo | — | 259 |


### `forja_n4_baseline.py` → `<global>`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| --initialize-n3 | não/declarativo | — | 76 |


### `forja_n4_e2e_adversarial.py` → `<global>`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| --case | não/declarativo | — | 139 |
| --output | não/declarativo | — | 140 |


### `forja_n4_invalidation.py` → `<global>`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| case | não/declarativo | — | 61 |
| trigger | não/declarativo | sorted(DEPENDENCIES) | 62 |
| reason | não/declarativo | — | 63 |


### `forja_n4_m6_cycles.py` → `<global>`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| case | não/declarativo | sorted(CASES) | 253 |


### `forja_n4_m6_prepare.py` → `<global>`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| command | não/declarativo | ['prepare', 'approve'] | 146 |
| case | não/declarativo | sorted(CASES) | 147 |
| --reviewer | não/declarativo | — | 148 |


### `forja_n4_validate.py` → `<global>`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| case | não/declarativo | — | 658 |
| --target-phase | não/declarativo | PHASES | 659 |
| --no-write | não/declarativo | — | 660 |


### `forja_official_sources.py` → `<global>`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| --build-manifest | não/declarativo | — | 474 |
| --validate | não/declarativo | — | 475 |
| --live | não/declarativo | — | 476 |


### `forja_post_protocol.py` → `<global>`

_Nenhum item observado neste escopo._


### `forja_post_protocol.py` → `ingest`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| case | não/declarativo | — | 1999 |
| attachment | não/declarativo | — | 2000 |
| --account-id | sim | — | 2001 |
| --thread-id | sim | — | 2002 |
| --message-id | sim | — | 2003 |
| --attachment-id | sim | — | 2004 |
| --received-at | sim | — | 2005 |
| --original-name | não/declarativo | — | 2006 |
| --piece-name | não/declarativo | — | 2007 |
| --process-id | não/declarativo | — | 2008 |
| --declaration-text | não/declarativo | — | 2009 |
| --evidence | não/declarativo | — | 2010 |


### `forja_post_protocol.py` → `promote`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| case | não/declarativo | — | 2016 |
| candidate_id | não/declarativo | — | 2017 |
| --content-key | sim | — | 2018 |
| --approved-by | sim | — | 2019 |
| --fixture-id | sim | — | 2020 |
| --test-id | sim | — | 2021 |
| --evidence-run | sim | — | 2022 |
| --evidence-case | sim | — | 2023 |
| --scope | não/declarativo | ['case', 'product_type', 'tribunal', 'office', 'global'] | 2024 |
| --scope-key | não/declarativo | — | 2025 |


### `forja_post_protocol.py` → `rebuild`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| case | não/declarativo | — | 2027 |
| content_key | não/declarativo | — | 2028 |


### `forja_post_protocol.py` → `resolve-origin`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| case | não/declarativo | — | 2030 |
| candidate_id | não/declarativo | — | 2031 |
| --content-key | sim | — | 2032 |
| --origin | sim | — | 2033 |
| --evidence-id | sim | — | 2034 |
| --decided-by | sim | — | 2035 |


### `forja_post_protocol.py` → `scan-gmail`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| --query | não/declarativo | — | 2012 |
| --max-results | não/declarativo | — | 2013 |
| --shadow | não/declarativo | — | 2014 |


### `forja_pso_pet.py` → `<global>`

_Nenhum item observado neste escopo._


### `forja_pso_pet.py` → `audit-case`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| case | não/declarativo | — | 616 |


### `forja_pso_pet.py` → `benchmark`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| --state-root | não/declarativo | — | 618 |
| --output | não/declarativo | — | 619 |


### `forja_pso_pet.py` → `validate-plan`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| plan | não/declarativo | — | 614 |


### `forja_pso_pet.py` → `write-example`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| --output | não/declarativo | — | 621 |


### `forja_reasoning.py` → `<global>`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| case | não/declarativo | — | 537 |


### `forja_recomputo_censo.py` → `<global>`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| --json | não/declarativo | — | 323 |


### `forja_regimentos.py` → `<global>`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| --raiz | não/declarativo | — | 245 |
| --limite-dias | não/declarativo | — | 246 |
| --json | não/declarativo | — | 247 |
| --hoje | não/declarativo | — | 248 |


### `forja_release_audit.py` → `<global>`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| --state-root | não/declarativo | — | 48 |
| --output | não/declarativo | — | 49 |
| --fail-on-blocked | não/declarativo | — | 50 |


### `forja_run.py` → `<global>`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| case | não/declarativo | — | 1192 |


### `forja_run.py` → `block`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| phase | não/declarativo | — | 1202 |
| --expected-revision | sim | — | 1203 |
| --reason | sim | — | 1204 |
| --blocker | não/declarativo | — | 1205 |


### `forja_run.py` → `promote`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| attempt_dir | não/declarativo | — | 1199 |
| --expected-revision | sim | — | 1200 |


### `forja_run.py` → `start`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| phase | não/declarativo | — | 1195 |
| --expected-revision | sim | — | 1196 |
| --run-id | não/declarativo | — | 1197 |


### `forja_run_metrics.py` → `<global>`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| case | não/declarativo | — | 130 |
| --output | não/declarativo | — | 131 |


### `forja_science.py` → `<global>`

_Nenhum item observado neste escopo._


### `forja_science.py` → `search`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| query | não/declarativo | — | 250 |
| --rows | não/declarativo | — | 251 |


### `forja_science.py` → `validate`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| case | não/declarativo | — | 248 |


### `forja_state_machine.py` → `<global>`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| case | não/declarativo | — | 493 |
| --state-root | não/declarativo | — | 494 |


### `forja_state_machine.py` → `event`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| type | não/declarativo | sorted(EVENT_TYPES) | 501 |
| --phase | não/declarativo | PHASES | 502 |
| --expected-revision | sim | — | 503 |
| --idempotency-key | sim | — | 504 |
| --actor | não/declarativo | — | 505 |
| --payload | não/declarativo | — | 506 |


### `forja_state_machine.py` → `init`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| --demand-id | não/declarativo | — | 497 |
| --from-legacy | não/declarativo | — | 498 |


### `forja_state_machine.py` → `status`

_Nenhum item observado neste escopo._


### `forja_varredura_tipografica.py` → `<global>`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| --json | não/declarativo | — | 288 |
| --limite | não/declarativo | — | 289 |


### `forja_visual_build.py` → `<global>`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| md_path | não/declarativo | — | 200 |
| out_dir | não/declarativo | — | 201 |
| titulo | não/declarativo | — | 202 |
| --case-dir | não/declarativo | — | 203 |
| --ledger | não/declarativo | — | 204 |
| --base-dir | não/declarativo | — | 205 |


### `forja_visual_qa.py` → `<global>`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| pdf | não/declarativo | — | 223 |
| output | não/declarativo | — | 224 |
| --qa-dir | sim | — | 225 |
| --generator-run | sim | — | 226 |
| --reviewer-run | sim | — | 227 |
| --docx | não/declarativo | — | 228 |
| --markdown | não/declarativo | — | 229 |
| --fidelity-output | não/declarativo | — | 230 |
| --svg | não/declarativo | — | 231 |
| --manual-review | não/declarativo | — | 232 |
| --pending-review-output | não/declarativo | — | 233 |
| --layout-exceptions | não/declarativo | — | 234 |


### `render_forja_atlas.py` → `<global>`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| --source | não/declarativo | — | 286 |
| --output | não/declarativo | — | 287 |


### `run_post_protocol_job.ps1` → `run_post_protocol_job.ps1`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| $Query | não/declarativo | — | 2 |
| $MaxResults | não/declarativo | — | 3 |


### `validate_forja_n3.py` → `<global>`

| Opção/argumento | Obrigatório | Choices | Linha |
| --- | --- | --- | --- |
| --real-word | não/declarativo | — | 103 |
| --run-replay | não/declarativo | — | 104 |
| --output | não/declarativo | — | 105 |


## 6. Schemas e contratos declarativos

| Arquivo | Título/ID | Tipo | Required | Propriedades | Defs | additionalProperties |
| --- | --- | --- | --- | --- | --- | --- |
| phase_contracts/F0.json | — | object | — | — | — | unspecified |
| phase_contracts/F1.json | — | object | — | — | — | unspecified |
| phase_contracts/F10.json | — | object | — | — | — | unspecified |
| phase_contracts/F2.json | — | object | — | — | — | unspecified |
| phase_contracts/F3.json | — | object | — | — | — | unspecified |
| phase_contracts/F4.json | — | object | — | — | — | unspecified |
| phase_contracts/F5.json | — | object | — | — | — | unspecified |
| phase_contracts/F6.json | — | object | — | — | — | unspecified |
| phase_contracts/F7.json | — | object | — | — | — | unspecified |
| phase_contracts/F8.json | — | object | — | — | — | unspecified |
| phase_contracts/F9.json | — | object | — | — | — | unspecified |
| phase_contracts_n4/EXTENSIONS.json | — | object | — | — | — | unspecified |
| phase_contracts_n4/F0.json | — | object | — | — | — | unspecified |
| phase_contracts_n4/F1.json | — | object | — | — | — | unspecified |
| phase_contracts_n4/F10.json | — | object | — | — | — | unspecified |
| phase_contracts_n4/F2.json | — | object | — | — | — | unspecified |
| phase_contracts_n4/F3.json | — | object | — | — | — | unspecified |
| phase_contracts_n4/F4.json | — | object | — | — | — | unspecified |
| phase_contracts_n4/F5.json | — | object | — | — | — | unspecified |
| phase_contracts_n4/F6.json | — | object | — | — | — | unspecified |
| phase_contracts_n4/F7.json | — | object | — | — | — | unspecified |
| phase_contracts_n4/F8.json | — | object | — | — | — | unspecified |
| phase_contracts_n4/F9.json | — | object | — | — | — | unspecified |
| n4_schemas/ARTIFACT_CATALOG.json | — | object | — | — | — | unspecified |
| n4_schemas/common.schema.json | common.schema.json | object | schemaVersion, specVersion, caseId, artifactType, phase, applicability, status, sourceHashes, producerRunId, createdAt, updatedAt, contentHash, issues | applicability, artifactType, caseId, contentHash, createdAt, issues, justification, phase, producerRunId, reviewerRunId, schemaVersion, sourceHashes, specVersion, status, updatedAt | — | True |
| n4_schemas/document_comparison.schema.json | document_comparison.schema.json | object | — | — | — | unspecified |
| n4_schemas/f10_delivery_integrity.schema.json | f10_delivery_integrity.schema.json | object | — | — | — | unspecified |
| n4_schemas/f10_human_diff_classification.schema.json | f10_human_diff_classification.schema.json | object | — | — | — | unspecified |
| n4_schemas/f2_n4_classification.schema.json | f2_n4_classification.schema.json | object | — | — | — | unspecified |
| n4_schemas/f2_question_tree.schema.json | f2_question_tree.schema.json | object | — | — | — | unspecified |
| n4_schemas/f3_conduct_ledger.schema.json | f3_conduct_ledger.schema.json | object | — | — | — | unspecified |
| n4_schemas/f3_document_comparison.schema.json | f3_document_comparison.schema.json | object | — | — | — | unspecified |
| n4_schemas/f3_event_identity.schema.json | f3_event_identity.schema.json | object | — | — | — | unspecified |
| n4_schemas/f3_mapa_destinatario.schema.json | f3_mapa_destinatario.schema.json | object | — | — | — | unspecified |
| n4_schemas/f3_reasoning_graph.schema.json | f3_reasoning_graph.schema.json | object | — | — | — | unspecified |
| n4_schemas/f4_case_acceptance_tests.schema.json | f4_case_acceptance_tests.schema.json | object | — | — | — | unspecified |
| n4_schemas/f4_coverage_matrix.schema.json | f4_coverage_matrix.schema.json | object | — | — | — | unspecified |
| n4_schemas/f4_decision_factor_map.schema.json | f4_decision_factor_map.schema.json | object | — | — | — | unspecified |
| n4_schemas/f4_intertemporal_map.schema.json | f4_intertemporal_map.schema.json | object | — | — | — | unspecified |
| n4_schemas/f4_quantification_scenarios.schema.json | f4_quantification_scenarios.schema.json | object | — | — | — | unspecified |
| n4_schemas/f4_settlement_map.schema.json | f4_settlement_map.schema.json | object | — | — | — | unspecified |
| n4_schemas/f4_signature_brief.schema.json | f4_signature_brief.schema.json | object | — | — | — | unspecified |
| n4_schemas/f4_thesis_maturity.schema.json | f4_thesis_maturity.schema.json | object | — | — | — | unspecified |
| n4_schemas/f5c_claim_evidence_map.schema.json | f5c_claim_evidence_map.schema.json | object | — | — | — | unspecified |
| n4_schemas/f5c_evidence_synthesis.schema.json | f5c_evidence_synthesis.schema.json | object | — | — | — | unspecified |
| n4_schemas/f5c_research_protocol.schema.json | f5c_research_protocol.schema.json | object | — | — | — | unspecified |
| n4_schemas/f5c_study_ledger.schema.json | f5c_study_ledger.schema.json | object | — | — | — | unspecified |
| n4_schemas/f7_case_test_results.schema.json | f7_case_test_results.schema.json | object | — | — | — | unspecified |
| n4_schemas/f7_global_consistency.schema.json | f7_global_consistency.schema.json | object | — | — | — | unspecified |
| n4_schemas/f7_metacognitive_audit.schema.json | f7_metacognitive_audit.schema.json | object | — | — | — | unspecified |
| n4_schemas/f7_science_audit.schema.json | f7_science_audit.schema.json | object | — | — | — | unspecified |
| n4_schemas/f9_delivery_selection.schema.json | f9_delivery_selection.schema.json | object | — | — | — | unspecified |
| n4_schemas/learning_candidate.schema.json | learning_candidate.schema.json | object | — | — | — | unspecified |
| n4_schemas/N4_LAYOUT_PROFILES.json | — | object | — | — | — | unspecified |
| n4_schemas/post_protocol_baseline_backfill.schema.json | post_protocol_baseline_backfill.schema.json | object | — | — | — | unspecified |
| n4_schemas/post_protocol_return.schema.json | post_protocol_return.schema.json | object | — | — | — | unspecified |
| n4_schemas/protocol_evidence.schema.json | protocol_evidence.schema.json | object | — | — | — | unspecified |
| pso_schemas/pso_case.schema.json | FORJA PSO-Pet case design | object | schemaVersion, methodVersion, caseId, profile, executionMode, sourceRegistry, contextPlan, problemDefinition, diagnosis, requirements, options, selection, validation, interventionPlan, evaluationPlan | caseId, contextPlan, diagnosis, evaluationPlan, executionMode, interventionPlan, methodVersion, options, problemDefinition, profile, requirements, schemaVersion, selection, sourceRegistry, validation | — | True |
| pso_schemas/PSO_CASE_EXAMPLE.json | — | object | — | — | — | unspecified |


## 7. Dependências e chamadas locais

As arestas abaixo são as interfaces entre módulos/símbolos. `imports_from` é vínculo sintático direto. `calls` só é `EXTRACTED` quando resolvido no mesmo módulo; resolução entre módulos por nome fica `AMBIGUOUS`.

| Origem | Relação | Destino | Confiança | Evidência |
| --- | --- | --- | --- | --- |
| calibrar_mapa_gen.py | imports_from | forja_visual_mapa_gen.py | EXTRACTED | calibrar_mapa_gen.py:23 |
| calibrar_mapa_gen.py | imports_from | forja_visual_mapa_gen.py | EXTRACTED | calibrar_mapa_gen.py:23 |
| calibrar_mapa_gen.py | imports_from | forja_visual_mapa_gen.py | EXTRACTED | calibrar_mapa_gen.py:96 |
| calibrar_mapa_gen.py::resolve | calls | forja_visual_mapa_gen.py::_norm | EXTRACTED | calibrar_mapa_gen.py:54 |
| calibrar_mapa_gen.py::cobre | calls | calibrar_mapa_gen.py::resolve | EXTRACTED | calibrar_mapa_gen.py:67 |
| calibrar_mapa_gen.py::cobre | calls | calibrar_mapa_gen.py::resolve | EXTRACTED | calibrar_mapa_gen.py:69 |
| calibrar_mapa_gen.py::main | calls | calibrar_mapa_gen.py::acha_md | EXTRACTED | calibrar_mapa_gen.py:82 |
| calibrar_mapa_gen.py::main | calls | calibrar_mapa_gen.py::carrega_manual | EXTRACTED | calibrar_mapa_gen.py:86 |
| calibrar_mapa_gen.py::main | calls | forja_visual_mapa_gen.py::_varre | EXTRACTED | calibrar_mapa_gen.py:97 |
| calibrar_mapa_gen.py::main | calls | calibrar_mapa_gen.py::cobre | EXTRACTED | calibrar_mapa_gen.py:101 |
| calibrar_mapa_gen.py::main | calls | calibrar_mapa_gen.py::cobre | EXTRACTED | calibrar_mapa_gen.py:103 |
| calibrar_mapa_gen.py::main | calls | calibrar_mapa_gen.py::acha_md | EXTRACTED | calibrar_mapa_gen.py:141 |
| calibrar_mapa_gen.py::main | calls | forja_visual_mapa_gen.py::_norm | EXTRACTED | calibrar_mapa_gen.py:154 |
| calibrar_mapa_gen.py::main | calls | forja_visual_mapa_gen.py::gerar_mapa | EXTRACTED | calibrar_mapa_gen.py:88 |
| calibrar_mapa_gen.py::main | calls | forja_visual_mapa_gen.py::_norm | EXTRACTED | calibrar_mapa_gen.py:106 |
| calibrar_mapa_gen.py::main | calls | forja_visual_mapa_gen.py::_norm | EXTRACTED | calibrar_mapa_gen.py:107 |
| calibrar_mapa_gen.py::main | calls | forja_visual_mapa_gen.py::gerar_mapa | EXTRACTED | calibrar_mapa_gen.py:146 |
| calibrar_mapa_gen.py::main | calls | forja_visual_mapa_gen.py::_norm | EXTRACTED | calibrar_mapa_gen.py:155 |
| forja_adocao_rota.py::_entregas | calls | forja_adocao_rota.py::_sha_arquivo | EXTRACTED | forja_adocao_rota.py:105 |
| forja_adocao_rota.py::_marca_aplica | calls | forja_adocao_rota.py::_alvo_do_marcador | EXTRACTED | forja_adocao_rota.py:161 |
| forja_adocao_rota.py::_marca_aplica | calls | forja_adocao_rota.py::_caminho_alvo | EXTRACTED | forja_adocao_rota.py:165 |
| forja_adocao_rota.py::_marcas_do_docx | calls | forja_adocao_rota.py::_marca_aplica | EXTRACTED | forja_adocao_rota.py:181 |
| forja_adocao_rota.py::medir | calls | forja_adocao_rota.py::_entregas | EXTRACTED | forja_adocao_rota.py:186 |
| forja_adocao_rota.py::medir | calls | forja_adocao_rota.py::_marcas_do_docx | EXTRACTED | forja_adocao_rota.py:195 |
| forja_adocao_rota.py::main | calls | forja_adocao_rota.py::medir | EXTRACTED | forja_adocao_rota.py:231 |
| forja_adversarial_audit.py | imports_from | forja_citations.py | EXTRACTED | forja_adversarial_audit.py:17 |
| forja_adversarial_audit.py | imports_from | forja_citations.py | EXTRACTED | forja_adversarial_audit.py:17 |
| forja_adversarial_audit.py | imports_from | forja_citations.py | EXTRACTED | forja_adversarial_audit.py:17 |
| forja_adversarial_audit.py | imports_from | forja_n3_common.py | EXTRACTED | forja_adversarial_audit.py:18 |
| forja_adversarial_audit.py | imports_from | forja_n3_common.py | EXTRACTED | forja_adversarial_audit.py:18 |
| forja_adversarial_audit.py | imports_from | forja_n3_common.py | EXTRACTED | forja_adversarial_audit.py:18 |
| forja_adversarial_audit.py | imports_from | forja_n3_common.py | EXTRACTED | forja_adversarial_audit.py:18 |
| forja_adversarial_audit.py | imports_from | forja_n3_common.py | EXTRACTED | forja_adversarial_audit.py:18 |
| forja_adversarial_audit.py::initialize_audit | calls | forja_citations.py::texto_da_peca | EXTRACTED | forja_adversarial_audit.py:122 |
| forja_adversarial_audit.py::initialize_audit | calls | forja_citations.py::extrair_citacoes | EXTRACTED | forja_adversarial_audit.py:123 |
| forja_adversarial_audit.py::initialize_audit | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_adversarial_audit.py:149 |
| forja_adversarial_audit.py::initialize_audit | calls | forja_adversarial_audit.py::_citation_id | EXTRACTED | forja_adversarial_audit.py:127 |
| forja_adversarial_audit.py::initialize_audit | calls | forja_citations.py::url_oficial | EXTRACTED | forja_adversarial_audit.py:135 |
| forja_adversarial_audit.py::initialize_audit | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_adversarial_audit.py:154 |
| forja_adversarial_audit.py::_validate_source | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_adversarial_audit.py:190 |
| forja_adversarial_audit.py::_validate_inventory_completeness | calls | forja_citations.py::extrair_citacoes | EXTRACTED | forja_adversarial_audit.py:199 |
| forja_adversarial_audit.py::_validate_inventory_completeness | calls | forja_citations.py::texto_da_peca | EXTRACTED | forja_adversarial_audit.py:199 |
| forja_adversarial_audit.py::validate_adversarial_audit | calls | forja_adversarial_audit.py::_validate_source | EXTRACTED | forja_adversarial_audit.py:219 |
| forja_adversarial_audit.py::validate_adversarial_audit | calls | forja_adversarial_audit.py::_validate_inventory_completeness | EXTRACTED | forja_adversarial_audit.py:220 |
| forja_adversarial_audit.py::validate_adversarial_audit | calls | forja_adversarial_audit.py::_official_url | EXTRACTED | forja_adversarial_audit.py:246 |
| forja_adversarial_audit.py::validate_adversarial_audit | calls | forja_adversarial_audit.py::_official_url | EXTRACTED | forja_adversarial_audit.py:259 |
| forja_adversarial_audit.py::validate_adversarial_audit | calls | forja_adversarial_audit.py::_official_url | EXTRACTED | forja_adversarial_audit.py:264 |
| forja_adversarial_audit.py::validate_adversarial_strategy | calls | forja_n3_common.py::read_json | EXTRACTED | forja_adversarial_audit.py:346 |
| forja_adversarial_audit.py::validate_adversarial_strategy | calls | forja_adversarial_audit.py::validate_adversarial_audit | EXTRACTED | forja_adversarial_audit.py:347 |
| forja_adversarial_audit.py::validate_adversarial_strategy | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_adversarial_audit.py:352 |
| forja_adversarial_audit.py::validate_adversarial_recheck | calls | forja_n3_common.py::read_json | EXTRACTED | forja_adversarial_audit.py:405 |
| forja_adversarial_audit.py::validate_adversarial_recheck | calls | forja_n3_common.py::read_json | EXTRACTED | forja_adversarial_audit.py:406 |
| forja_adversarial_audit.py::validate_adversarial_recheck | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_adversarial_audit.py:409 |
| forja_adversarial_audit.py::validate_adversarial_recheck | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_adversarial_audit.py:411 |
| forja_adversarial_audit.py::validate_phase_artifacts | calls | forja_adversarial_audit.py::validate_adversarial_audit | EXTRACTED | forja_adversarial_audit.py:464 |
| forja_adversarial_audit.py::validate_phase_artifacts | calls | forja_n3_common.py::read_json | EXTRACTED | forja_adversarial_audit.py:464 |
| forja_adversarial_audit.py::validate_phase_artifacts | calls | forja_adversarial_audit.py::validate_adversarial_strategy | EXTRACTED | forja_adversarial_audit.py:471 |
| forja_adversarial_audit.py::validate_phase_artifacts | calls | forja_adversarial_audit.py::validate_adversarial_recheck | EXTRACTED | forja_adversarial_audit.py:478 |
| forja_adversarial_audit.py::validate_phase_artifacts | calls | forja_n3_common.py::read_json | EXTRACTED | forja_adversarial_audit.py:471 |
| forja_adversarial_audit.py::validate_phase_artifacts | calls | forja_n3_common.py::read_json | EXTRACTED | forja_adversarial_audit.py:478 |
| forja_adversarial_audit.py::main | calls | forja_adversarial_audit.py::initialize_audit | EXTRACTED | forja_adversarial_audit.py:499 |
| forja_adversarial_audit.py::main | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_adversarial_audit.py:500 |
| forja_adversarial_audit.py::main | calls | forja_n3_common.py::atomic_write_text | EXTRACTED | forja_adversarial_audit.py:501 |
| forja_adversarial_audit.py::main | calls | forja_adversarial_audit.py::initialize_audit | EXTRACTED | forja_adversarial_audit.py:504 |
| forja_adversarial_audit.py::main | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_adversarial_audit.py:505 |
| forja_adversarial_audit.py::main | calls | forja_adversarial_audit.py::validate_adversarial_audit | EXTRACTED | forja_adversarial_audit.py:509 |
| forja_adversarial_audit.py::main | calls | forja_n3_common.py::read_json | EXTRACTED | forja_adversarial_audit.py:508 |
| forja_adversarial_audit.py::main | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_adversarial_audit.py:511 |
| forja_adversarial_audit.py::main | calls | forja_adversarial_audit.py::mandatory_prompt_for_phase | EXTRACTED | forja_adversarial_audit.py:513 |
| forja_adversarial_audit.py::main | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_adversarial_audit.py:511 |
| forja_adversarial_gate.py::validar_auditoria_adversarial | calls | forja_adversarial_gate.py::_motivo | EXTRACTED | forja_adversarial_gate.py:79 |
| forja_adversarial_gate.py::validar_auditoria_adversarial | calls | forja_adversarial_gate.py::_hashes_do_arquivo | EXTRACTED | forja_adversarial_gate.py:145 |
| forja_adversarial_gate.py::validar_auditoria_adversarial | calls | forja_adversarial_gate.py::_motivo | EXTRACTED | forja_adversarial_gate.py:155 |
| forja_adversarial_gate.py::validar_auditoria_adversarial | calls | forja_adversarial_gate.py::_motivo | EXTRACTED | forja_adversarial_gate.py:156 |
| forja_alertas.py::_now_iso | calls | forja_alertas.py::_now | EXTRACTED | forja_alertas.py:39 |
| forja_alertas.py::_dedup_ok | calls | forja_alertas.py::_ler_json | EXTRACTED | forja_alertas.py:59 |
| forja_alertas.py::_dedup_ok | calls | forja_alertas.py::_registro_enviados | EXTRACTED | forja_alertas.py:59 |
| forja_alertas.py::_dedup_ok | calls | forja_alertas.py::_now | EXTRACTED | forja_alertas.py:64 |
| forja_alertas.py::_marcar_enviado | calls | forja_alertas.py::_registro_enviados | EXTRACTED | forja_alertas.py:70 |
| forja_alertas.py::_marcar_enviado | calls | forja_alertas.py::_ler_json | EXTRACTED | forja_alertas.py:71 |
| forja_alertas.py::_marcar_enviado | calls | forja_alertas.py::_now_iso | EXTRACTED | forja_alertas.py:72 |
| forja_alertas.py::_demand_id_do_caso | calls | forja_alertas.py::_ler_json | EXTRACTED | forja_alertas.py:86 |
| forja_alertas.py::_comentar_no_painel | calls | forja_alertas.py::_ler_json | EXTRACTED | forja_alertas.py:110 |
| forja_alertas.py::_comentar_no_painel | calls | forja_alertas.py::_now_iso | EXTRACTED | forja_alertas.py:120 |
| forja_alertas.py::_comentar_no_painel | calls | forja_alertas.py::_now_iso | EXTRACTED | forja_alertas.py:121 |
| forja_alertas.py::_comentar_no_painel | calls | forja_alertas.py::_now_iso | EXTRACTED | forja_alertas.py:110 |
| forja_alertas.py::_comentar_no_painel | calls | forja_alertas.py::_now_iso | EXTRACTED | forja_alertas.py:115 |
| forja_alertas.py::_comentar_no_painel | calls | forja_alertas.py::_now | EXTRACTED | forja_alertas.py:114 |
| forja_alertas.py::_emitir | calls | forja_alertas.py::_dedup_ok | EXTRACTED | forja_alertas.py:138 |
| forja_alertas.py::_emitir | calls | forja_alertas.py::_demand_id_do_caso | EXTRACTED | forja_alertas.py:141 |
| forja_alertas.py::_emitir | calls | forja_alertas.py::_log_global | EXTRACTED | forja_alertas.py:145 |
| forja_alertas.py::_emitir | calls | forja_alertas.py::_comentar_no_painel | EXTRACTED | forja_alertas.py:151 |
| forja_alertas.py::_emitir | calls | forja_alertas.py::_marcar_enviado | EXTRACTED | forja_alertas.py:154 |
| forja_alertas.py::_emitir | calls | forja_alertas.py::_marcar_enviado | EXTRACTED | forja_alertas.py:161 |
| forja_alertas.py::_emitir | calls | forja_alertas.py::_pendentes | EXTRACTED | forja_alertas.py:159 |
| forja_alertas.py::_emitir | calls | forja_alertas.py::_pendentes | EXTRACTED | forja_alertas.py:162 |
| forja_alertas.py::notificar_p0 | calls | forja_alertas.py::_emitir | EXTRACTED | forja_alertas.py:182 |
| forja_alertas.py::notificar_p0 | calls | forja_alertas.py::_now_iso | EXTRACTED | forja_alertas.py:172 |
| forja_alertas.py::notificar_resolucao | calls | forja_alertas.py::_emitir | EXTRACTED | forja_alertas.py:196 |
| forja_alertas.py::notificar_resolucao | calls | forja_alertas.py::_now_iso | EXTRACTED | forja_alertas.py:189 |
| forja_alertas.py::drenar_pendentes | calls | forja_alertas.py::_pendentes | EXTRACTED | forja_alertas.py:201 |
| forja_alertas.py::drenar_pendentes | calls | forja_alertas.py::_comentar_no_painel | EXTRACTED | forja_alertas.py:210 |
| forja_ar_architecture.py | imports_from | forja_n3_common.py | EXTRACTED | forja_ar_architecture.py:18 |
| forja_ar_architecture.py | imports_from | forja_n3_common.py | EXTRACTED | forja_ar_architecture.py:18 |
| forja_ar_architecture.py | imports_from | forja_n3_common.py | EXTRACTED | forja_ar_architecture.py:18 |
| forja_ar_architecture.py | imports_from | forja_n3_common.py | EXTRACTED | forja_ar_architecture.py:18 |
| forja_ar_architecture.py | imports_from | forja_n3_common.py | EXTRACTED | forja_ar_architecture.py:18 |
| forja_ar_architecture.py | imports_from | forja_n3_common.py | EXTRACTED | forja_ar_architecture.py:18 |
| forja_ar_architecture.py | imports_from | forja_n3_common.py | EXTRACTED | forja_ar_architecture.py:18 |
| forja_ar_architecture.py | imports_from | forja_n3_common.py | EXTRACTED | forja_ar_architecture.py:18 |
| forja_ar_architecture.py::_write_candidate | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_ar_architecture.py:90 |
| forja_ar_architecture.py::_write_candidate | calls | forja_n3_common.py::canonical_hash | EXTRACTED | forja_ar_architecture.py:91 |
| forja_ar_architecture.py::_write_candidate | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_ar_architecture.py:92 |
| forja_ar_architecture.py::_write_candidate | calls | forja_ar_architecture.py::_semantic | EXTRACTED | forja_ar_architecture.py:91 |
| forja_ar_architecture.py::validate_candidate | calls | forja_n3_common.py::read_json | EXTRACTED | forja_ar_architecture.py:99 |
| forja_ar_architecture.py::validate_candidate | calls | forja_n3_common.py::canonical_hash | EXTRACTED | forja_ar_architecture.py:107 |
| forja_ar_architecture.py::validate_candidate | calls | forja_ar_architecture.py::_semantic | EXTRACTED | forja_ar_architecture.py:107 |
| forja_ar_architecture.py::validate_candidate | calls | forja_n3_common.py::read_json | EXTRACTED | forja_ar_architecture.py:102 |
| forja_ar_architecture.py::create_candidate | calls | forja_ar_architecture.py::validate_manifest | EXTRACTED | forja_ar_architecture.py:143 |
| forja_ar_architecture.py::create_candidate | calls | forja_n3_common.py::canonical_hash | EXTRACTED | forja_ar_architecture.py:159 |
| forja_ar_architecture.py::create_candidate | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_ar_architecture.py:171 |
| forja_ar_architecture.py::create_candidate | calls | forja_ar_architecture.py::_write_candidate | EXTRACTED | forja_ar_architecture.py:203 |
| forja_ar_architecture.py::create_candidate | calls | forja_ar_architecture.py::validate_candidate | EXTRACTED | forja_ar_architecture.py:204 |
| forja_ar_architecture.py::create_candidate | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_ar_architecture.py:138 |
| forja_ar_architecture.py::create_candidate | calls | forja_n3_common.py::read_json | EXTRACTED | forja_ar_architecture.py:142 |
| forja_ar_architecture.py::create_candidate | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_ar_architecture.py:145 |
| forja_ar_architecture.py::create_candidate | calls | forja_ar_architecture.py::_write_candidate | EXTRACTED | forja_ar_architecture.py:169 |
| forja_ar_architecture.py::create_candidate | calls | forja_n3_common.py::new_id | EXTRACTED | forja_ar_architecture.py:178 |
| forja_ar_architecture.py::create_candidate | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_ar_architecture.py:206 |
| forja_ar_architecture.py::create_candidate | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_ar_architecture.py:147 |
| forja_ar_architecture.py::create_candidate | calls | forja_n3_common.py::read_json | EXTRACTED | forja_ar_architecture.py:161 |
| forja_ar_architecture.py::create_candidate | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_ar_architecture.py:151 |
| forja_ar_architecture.py::_run_pytest | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_ar_architecture.py:211 |
| forja_ar_architecture.py::_run_pytest | calls | forja_n3_common.py::canonical_hash | EXTRACTED | forja_ar_architecture.py:249 |
| forja_ar_architecture.py::_run_pytest | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_ar_architecture.py:253 |
| forja_ar_architecture.py::_run_pytest | calls | forja_n3_common.py::canonical_hash | EXTRACTED | forja_ar_architecture.py:231 |
| forja_ar_architecture.py::_run_pytest | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_ar_architecture.py:233 |
| forja_ar_architecture.py::_rollback_rehearsal | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_ar_architecture.py:358 |
| forja_ar_architecture.py::_rollback_rehearsal | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_ar_architecture.py:362 |
| forja_ar_architecture.py::_rollback_rehearsal | calls | forja_n3_common.py::read_json | EXTRACTED | forja_ar_architecture.py:355 |
| forja_ar_architecture.py::_rollback_rehearsal | calls | forja_ar_architecture.py::automation_enabled | EXTRACTED | forja_ar_architecture.py:396 |
| forja_ar_architecture.py::_rollback_rehearsal | calls | forja_ar_architecture.py::automation_enabled | EXTRACTED | forja_ar_architecture.py:397 |
| forja_ar_architecture.py::_rollback_rehearsal | calls | forja_n3_common.py::canonical_hash | EXTRACTED | forja_ar_architecture.py:400 |
| forja_ar_architecture.py::_rollback_rehearsal | calls | forja_n3_common.py::canonical_hash | EXTRACTED | forja_ar_architecture.py:401 |
| forja_ar_architecture.py::_rollback_rehearsal | calls | forja_ar_architecture.py::automation_enabled | EXTRACTED | forja_ar_architecture.py:390 |
| forja_ar_architecture.py::_rollback_rehearsal | calls | forja_ar_architecture.py::automation_enabled | EXTRACTED | forja_ar_architecture.py:391 |
| forja_ar_architecture.py::_rollback_rehearsal | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_ar_architecture.py:394 |
| forja_ar_architecture.py::_rollback_rehearsal | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_ar_architecture.py:399 |
| forja_ar_architecture.py::_overlay_candidate | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_ar_architecture.py:413 |
| forja_ar_architecture.py::_overlay_candidate | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_ar_architecture.py:415 |
| forja_ar_architecture.py::_overlay_candidate | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_ar_architecture.py:417 |
| forja_ar_architecture.py::_overlay_candidate | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_ar_architecture.py:416 |
| forja_ar_architecture.py::evaluate_candidate | calls | forja_n3_common.py::read_json | EXTRACTED | forja_ar_architecture.py:423 |
| forja_ar_architecture.py::evaluate_candidate | calls | forja_ar_architecture.py::validate_manifest | EXTRACTED | forja_ar_architecture.py:427 |
| forja_ar_architecture.py::evaluate_candidate | calls | forja_n3_common.py::read_json | EXTRACTED | forja_ar_architecture.py:488 |
| forja_ar_architecture.py::evaluate_candidate | calls | forja_ar_architecture.py::_write_candidate | EXTRACTED | forja_ar_architecture.py:536 |
| forja_ar_architecture.py::evaluate_candidate | calls | forja_ar_architecture.py::validate_candidate | EXTRACTED | forja_ar_architecture.py:537 |
| forja_ar_architecture.py::evaluate_candidate | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_ar_architecture.py:425 |
| forja_ar_architecture.py::evaluate_candidate | calls | forja_n3_common.py::read_json | EXTRACTED | forja_ar_architecture.py:426 |
| forja_ar_architecture.py::evaluate_candidate | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_ar_architecture.py:429 |
| forja_ar_architecture.py::evaluate_candidate | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_ar_architecture.py:490 |
| forja_ar_architecture.py::evaluate_candidate | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_ar_architecture.py:492 |
| forja_ar_architecture.py::evaluate_candidate | calls | forja_ar_architecture.py::_write_candidate | EXTRACTED | forja_ar_architecture.py:496 |
| forja_ar_architecture.py::evaluate_candidate | calls | forja_ar_architecture.py::_cycle_count | EXTRACTED | forja_ar_architecture.py:515 |
| forja_ar_architecture.py::evaluate_candidate | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_ar_architecture.py:539 |
| forja_ar_architecture.py::evaluate_candidate | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_ar_architecture.py:441 |
| forja_ar_architecture.py::evaluate_candidate | calls | forja_ar_architecture.py::_run_pytest | EXTRACTED | forja_ar_architecture.py:445 |
| forja_ar_architecture.py::evaluate_candidate | calls | forja_ar_architecture.py::_overlay_candidate | EXTRACTED | forja_ar_architecture.py:446 |
| forja_ar_architecture.py::evaluate_candidate | calls | forja_ar_architecture.py::_run_pytest | EXTRACTED | forja_ar_architecture.py:447 |
| forja_ar_architecture.py::evaluate_candidate | calls | forja_ar_architecture.py::_run_pytest | EXTRACTED | forja_ar_architecture.py:469 |
| forja_ar_architecture.py::evaluate_candidate | calls | forja_ar_architecture.py::_rollback_rehearsal | EXTRACTED | forja_ar_architecture.py:476 |
| forja_ar_architecture.py::evaluate_candidate | calls | forja_ar_architecture.py::_tracked_vault_leaks | EXTRACTED | forja_ar_architecture.py:477 |
| forja_ar_architecture.py::evaluate_candidate | calls | forja_ar_architecture.py::_vault_ignore_failures | EXTRACTED | forja_ar_architecture.py:478 |
| forja_ar_architecture.py::evaluate_candidate | calls | forja_ar_architecture.py::_relevant_import_graph | EXTRACTED | forja_ar_architecture.py:515 |
| forja_ar_architecture.py::evaluate_candidate | calls | forja_ar_architecture.py::_write_candidate | EXTRACTED | forja_ar_architecture.py:466 |
| forja_ar_architecture.py::evaluate_candidate | calls | forja_ar_architecture.py::_write_candidate | EXTRACTED | forja_ar_architecture.py:473 |
| forja_ar_architecture.py::main | calls | forja_ar_architecture.py::create_candidate | EXTRACTED | forja_ar_architecture.py:557 |
| forja_ar_architecture.py::main | calls | forja_ar_architecture.py::evaluate_candidate | EXTRACTED | forja_ar_architecture.py:567 |
| forja_ar_blind.py | imports_from | forja_ar_corpus.py | EXTRACTED | forja_ar_blind.py:13 |
| forja_ar_blind.py | imports_from | forja_ar_corpus.py | EXTRACTED | forja_ar_blind.py:13 |
| forja_ar_blind.py | imports_from | forja_ar_corpus.py | EXTRACTED | forja_ar_blind.py:13 |
| forja_ar_blind.py | imports_from | forja_ar_runpair.py | EXTRACTED | forja_ar_blind.py:14 |
| forja_ar_blind.py::_sha_file | calls | forja_ar_blind.py::_sha_bytes | EXTRACTED | forja_ar_blind.py:54 |
| forja_ar_blind.py::_mapping_path | calls | forja_ar_corpus.py::secrets_dir | EXTRACTED | forja_ar_blind.py:63 |
| forja_ar_blind.py::prepare | calls | forja_ar_runpair.py::validate_pair | EXTRACTED | forja_ar_blind.py:70 |
| forja_ar_blind.py::prepare | calls | forja_ar_blind.py::_mapping_path | EXTRACTED | forja_ar_blind.py:111 |
| forja_ar_blind.py::prepare | calls | forja_ar_blind.py::canonicalize | EXTRACTED | forja_ar_blind.py:82 |
| forja_ar_blind.py::prepare | calls | forja_ar_blind.py::leak_scan | EXTRACTED | forja_ar_blind.py:83 |
| forja_ar_blind.py::prepare | calls | forja_ar_blind.py::_sha_bytes | EXTRACTED | forja_ar_blind.py:86 |
| forja_ar_blind.py::prepare | calls | forja_ar_corpus.py::load_hmac_key | EXTRACTED | forja_ar_blind.py:109 |
| forja_ar_blind.py::prepare | calls | forja_ar_blind.py::_sha_file | EXTRACTED | forja_ar_blind.py:119 |
| forja_ar_blind.py::prepare | calls | forja_ar_blind.py::_sha_bytes | EXTRACTED | forja_ar_blind.py:120 |
| forja_ar_blind.py::prepare | calls | forja_ar_blind.py::_canonical | EXTRACTED | forja_ar_blind.py:120 |
| forja_ar_blind.py::prepare | calls | forja_ar_blind.py::_sha_file | EXTRACTED | forja_ar_blind.py:101 |
| forja_ar_blind.py::prepare | calls | forja_ar_blind.py::_canonical | EXTRACTED | forja_ar_blind.py:110 |
| forja_ar_blind.py::_verify_mapping | calls | forja_ar_blind.py::_canonical | EXTRACTED | forja_ar_blind.py:128 |
| forja_ar_blind.py::_mapping_leaked | calls | forja_ar_blind.py::_sha_file | EXTRACTED | forja_ar_blind.py:140 |
| forja_ar_blind.py::consolidate | calls | forja_ar_blind.py::_mapping_path | EXTRACTED | forja_ar_blind.py:168 |
| forja_ar_blind.py::consolidate | calls | forja_ar_blind.py::_mapping_leaked | EXTRACTED | forja_ar_blind.py:176 |
| forja_ar_blind.py::consolidate | calls | forja_ar_corpus.py::load_hmac_key | EXTRACTED | forja_ar_blind.py:172 |
| forja_ar_blind.py::consolidate | calls | forja_ar_blind.py::_verify_mapping | EXTRACTED | forja_ar_blind.py:174 |
| forja_ar_blind.py::consolidate | calls | forja_ar_blind.py::_sha_file | EXTRACTED | forja_ar_blind.py:176 |
| forja_ar_blind.py::consolidate | calls | forja_ar_blind.py::_cohen_kappa | EXTRACTED | forja_ar_blind.py:236 |
| forja_ar_blind.py::consolidate | calls | forja_ar_blind.py::_sha_file | EXTRACTED | forja_ar_blind.py:201 |
| forja_ar_blind.py::main | calls | forja_ar_blind.py::prepare | EXTRACTED | forja_ar_blind.py:263 |
| forja_ar_blind.py::main | calls | forja_ar_blind.py::consolidate | EXTRACTED | forja_ar_blind.py:265 |
| forja_ar_canarios.py | imports_from | forja_ar_corpus.py | EXTRACTED | forja_ar_canarios.py:11 |
| forja_ar_canarios.py | imports_from | forja_ar_indicadores.py | EXTRACTED | forja_ar_canarios.py:12 |
| forja_ar_canarios.py::verificar_manifest | calls | forja_ar_canarios.py::_load | EXTRACTED | forja_ar_canarios.py:38 |
| forja_ar_canarios.py::verificar_manifest | calls | forja_ar_indicadores.py::computar_indicadores | EXTRACTED | forja_ar_canarios.py:58 |
| forja_ar_canarios.py::verificar_manifest | calls | forja_ar_indicadores.py::computar_indicadores | EXTRACTED | forja_ar_canarios.py:59 |
| forja_ar_canarios.py::verificar_manifest | calls | forja_ar_indicadores.py::computar_indicadores | EXTRACTED | forja_ar_canarios.py:60 |
| forja_ar_canarios.py::verificar_manifest | calls | forja_ar_canarios.py::_adverse | EXTRACTED | forja_ar_canarios.py:62 |
| forja_ar_canarios.py::verificar_manifest | calls | forja_ar_canarios.py::_adverse | EXTRACTED | forja_ar_canarios.py:63 |
| forja_ar_canarios.py::verificar_manifest | calls | forja_ar_canarios.py::_sha | EXTRACTED | forja_ar_canarios.py:52 |
| forja_ar_canarios.py::verificar | calls | forja_ar_canarios.py::verificar_manifest | EXTRACTED | forja_ar_canarios.py:97 |
| forja_ar_canarios.py::verificar | calls | forja_ar_canarios.py::verificar_manifest | EXTRACTED | forja_ar_canarios.py:112 |
| forja_ar_canarios.py::verificar | calls | forja_ar_corpus.py::secrets_dir | EXTRACTED | forja_ar_canarios.py:107 |
| forja_ar_canarios.py::main | calls | forja_ar_canarios.py::verificar | EXTRACTED | forja_ar_canarios.py:129 |
| forja_ar_ciclo.py | imports_from | forja_ar_corpus.py | EXTRACTED | forja_ar_ciclo.py:13 |
| forja_ar_ciclo.py | imports_from | forja_ar_corpus.py | EXTRACTED | forja_ar_ciclo.py:13 |
| forja_ar_ciclo.py | imports_from | forja_human_review.py | EXTRACTED | forja_ar_ciclo.py:290 |
| forja_ar_ciclo.py | imports_from | forja_human_review.py | EXTRACTED | forja_ar_ciclo.py:294 |
| forja_ar_ciclo.py::_sha_file | calls | forja_ar_ciclo.py::_sha_bytes | EXTRACTED | forja_ar_ciclo.py:43 |
| forja_ar_ciclo.py::append_log | calls | forja_ar_ciclo.py::_sha_bytes | EXTRACTED | forja_ar_ciclo.py:64 |
| forja_ar_ciclo.py::append_log | calls | forja_ar_ciclo.py::_sha_bytes | EXTRACTED | forja_ar_ciclo.py:61 |
| forja_ar_ciclo.py::append_log | calls | forja_ar_ciclo.py::_canonical | EXTRACTED | forja_ar_ciclo.py:64 |
| forja_ar_ciclo.py::append_log | calls | forja_ar_ciclo.py::_canonical | EXTRACTED | forja_ar_ciclo.py:61 |
| forja_ar_ciclo.py::verify_log | calls | forja_ar_ciclo.py::_sha_bytes | EXTRACTED | forja_ar_ciclo.py:89 |
| forja_ar_ciclo.py::verify_log | calls | forja_ar_ciclo.py::_canonical | EXTRACTED | forja_ar_ciclo.py:89 |
| forja_ar_ciclo.py::snapshot | calls | forja_ar_ciclo.py::_sha_file | EXTRACTED | forja_ar_ciclo.py:115 |
| forja_ar_ciclo.py::snapshot | calls | forja_ar_ciclo.py::append_log | EXTRACTED | forja_ar_ciclo.py:125 |
| forja_ar_ciclo.py::snapshot | calls | forja_ar_ciclo.py::_sha_file | EXTRACTED | forja_ar_ciclo.py:116 |
| forja_ar_ciclo.py::snapshot | calls | forja_ar_ciclo.py::_sha_file | EXTRACTED | forja_ar_ciclo.py:117 |
| forja_ar_ciclo.py::snapshot | calls | forja_ar_ciclo.py::_sha_file | EXTRACTED | forja_ar_ciclo.py:118 |
| forja_ar_ciclo.py::consume_sealed | calls | forja_ar_ciclo.py::_sha_bytes | EXTRACTED | forja_ar_ciclo.py:163 |
| forja_ar_ciclo.py::consume_sealed | calls | forja_ar_corpus.py::secrets_dir | EXTRACTED | forja_ar_ciclo.py:146 |
| forja_ar_ciclo.py::consume_sealed | calls | forja_ar_ciclo.py::_canonical | EXTRACTED | forja_ar_ciclo.py:163 |
| forja_ar_ciclo.py::promotion | calls | forja_ar_ciclo.py::_load_required | EXTRACTED | forja_ar_ciclo.py:187 |
| forja_ar_ciclo.py::promotion | calls | forja_ar_ciclo.py::_load_required | EXTRACTED | forja_ar_ciclo.py:190 |
| forja_ar_ciclo.py::promotion | calls | forja_ar_ciclo.py::_load_required | EXTRACTED | forja_ar_ciclo.py:191 |
| forja_ar_ciclo.py::promotion | calls | forja_ar_ciclo.py::_load_required | EXTRACTED | forja_ar_ciclo.py:192 |
| forja_ar_ciclo.py::promotion | calls | forja_ar_ciclo.py::consume_sealed | EXTRACTED | forja_ar_ciclo.py:236 |
| forja_ar_ciclo.py::promotion | calls | forja_ar_ciclo.py::_sha_file | EXTRACTED | forja_ar_ciclo.py:188 |
| forja_ar_ciclo.py::independent_review | calls | forja_ar_ciclo.py::_sha_file | EXTRACTED | forja_ar_ciclo.py:276 |
| forja_ar_ciclo.py::independent_review | calls | forja_ar_ciclo.py::_sha_file | EXTRACTED | forja_ar_ciclo.py:277 |
| forja_ar_ciclo.py::human_approve | calls | forja_ar_ciclo.py::_sha_file | EXTRACTED | forja_ar_ciclo.py:284 |
| forja_ar_ciclo.py::human_approve | calls | forja_human_review.py::validate_visual_review_receipt | EXTRACTED | forja_ar_ciclo.py:292 |
| forja_ar_ciclo.py::human_approve | calls | forja_human_review.py::validate_claim_review_receipt | EXTRACTED | forja_ar_ciclo.py:296 |
| forja_ar_ciclo.py::relatorio | calls | forja_ar_ciclo.py::cluster_interval | EXTRACTED | forja_ar_ciclo.py:359 |
| forja_ar_ciclo.py::main | calls | forja_ar_ciclo.py::verify_log | EXTRACTED | forja_ar_ciclo.py:423 |
| forja_ar_ciclo.py::main | calls | forja_ar_ciclo.py::snapshot | EXTRACTED | forja_ar_ciclo.py:426 |
| forja_ar_ciclo.py::main | calls | forja_ar_ciclo.py::promotion | EXTRACTED | forja_ar_ciclo.py:429 |
| forja_ar_ciclo.py::main | calls | forja_ar_ciclo.py::independent_review | EXTRACTED | forja_ar_ciclo.py:440 |
| forja_ar_ciclo.py::main | calls | forja_ar_ciclo.py::human_approve | EXTRACTED | forja_ar_ciclo.py:442 |
| forja_ar_ciclo.py::main | calls | forja_ar_ciclo.py::relatorio | EXTRACTED | forja_ar_ciclo.py:444 |
| forja_ar_corpus.py::load_hmac_key | calls | forja_ar_corpus.py::secrets_dir | EXTRACTED | forja_ar_corpus.py:58 |
| forja_ar_corpus.py::derivar_linhagem | calls | forja_ar_corpus.py::_fold | EXTRACTED | forja_ar_corpus.py:89 |
| forja_ar_corpus.py::derivar_linhagem | calls | forja_ar_corpus.py::_fold | EXTRACTED | forja_ar_corpus.py:85 |
| forja_ar_corpus.py::_case_metadata | calls | forja_ar_corpus.py::_read_json | EXTRACTED | forja_ar_corpus.py:106 |
| forja_ar_corpus.py::_case_metadata | calls | forja_ar_corpus.py::_read_json | EXTRACTED | forja_ar_corpus.py:107 |
| forja_ar_corpus.py::_artifact_candidates | calls | forja_ar_corpus.py::_fold | EXTRACTED | forja_ar_corpus.py:143 |
| forja_ar_corpus.py::scan_corpus | calls | forja_ar_corpus.py::_read_json | EXTRACTED | forja_ar_corpus.py:163 |
| forja_ar_corpus.py::scan_corpus | calls | forja_ar_corpus.py::_artifact_candidates | EXTRACTED | forja_ar_corpus.py:169 |
| forja_ar_corpus.py::scan_corpus | calls | forja_ar_corpus.py::_case_metadata | EXTRACTED | forja_ar_corpus.py:173 |
| forja_ar_corpus.py::scan_corpus | calls | forja_ar_corpus.py::derivar_linhagem | EXTRACTED | forja_ar_corpus.py:174 |
| forja_ar_corpus.py::scan_corpus | calls | forja_ar_corpus.py::_sha256_file | EXTRACTED | forja_ar_corpus.py:183 |
| forja_ar_corpus.py::scan_corpus | calls | forja_ar_corpus.py::atribuir_split | EXTRACTED | forja_ar_corpus.py:186 |
| forja_ar_corpus.py::register_sealed_inventory | calls | forja_ar_corpus.py::secrets_dir | EXTRACTED | forja_ar_corpus.py:262 |
| forja_ar_corpus.py::register_sealed_inventory | calls | forja_ar_corpus.py::_read_json | EXTRACTED | forja_ar_corpus.py:263 |
| forja_ar_corpus.py::register_sealed_inventory | calls | forja_ar_corpus.py::_canonical | EXTRACTED | forja_ar_corpus.py:271 |
| forja_ar_corpus.py::check_corpus | calls | forja_ar_corpus.py::_sha256_file | EXTRACTED | forja_ar_corpus.py:289 |
| forja_ar_corpus.py::main | calls | forja_ar_corpus.py::_read_json | EXTRACTED | forja_ar_corpus.py:336 |
| forja_ar_corpus.py::main | calls | forja_ar_corpus.py::load_hmac_key | EXTRACTED | forja_ar_corpus.py:325 |
| forja_ar_corpus.py::main | calls | forja_ar_corpus.py::scan_corpus | EXTRACTED | forja_ar_corpus.py:327 |
| forja_ar_corpus.py::main | calls | forja_ar_corpus.py::register_sealed_inventory | EXTRACTED | forja_ar_corpus.py:333 |
| forja_ar_corpus.py::main | calls | forja_ar_corpus.py::check_corpus | EXTRACTED | forja_ar_corpus.py:340 |
| forja_ar_corpus.py::main | calls | forja_ar_corpus.py::_read_json | EXTRACTED | forja_ar_corpus.py:324 |
| forja_ar_corpus.py::main | calls | forja_ar_corpus.py::report | EXTRACTED | forja_ar_corpus.py:349 |
| forja_ar_evolucao.py::init_experimento | calls | forja_ar_evolucao.py::_save | EXTRACTED | forja_ar_evolucao.py:66 |
| forja_ar_evolucao.py::init_experimento | calls | forja_ar_evolucao.py::_sha_file | EXTRACTED | forja_ar_evolucao.py:56 |
| forja_ar_evolucao.py::init_experimento | calls | forja_ar_evolucao.py::_manifest_path | EXTRACTED | forja_ar_evolucao.py:66 |
| forja_ar_evolucao.py::registrar_geracao | calls | forja_ar_evolucao.py::_load | EXTRACTED | forja_ar_evolucao.py:72 |
| forja_ar_evolucao.py::registrar_geracao | calls | forja_ar_evolucao.py::_save | EXTRACTED | forja_ar_evolucao.py:99 |
| forja_ar_evolucao.py::registrar_geracao | calls | forja_ar_evolucao.py::_manifest_path | EXTRACTED | forja_ar_evolucao.py:72 |
| forja_ar_evolucao.py::registrar_geracao | calls | forja_ar_evolucao.py::_manifest_path | EXTRACTED | forja_ar_evolucao.py:99 |
| forja_ar_evolucao.py::registrar_geracao | calls | forja_ar_evolucao.py::_sha_file | EXTRACTED | forja_ar_evolucao.py:87 |
| forja_ar_evolucao.py::selecionar_winner | calls | forja_ar_evolucao.py::_load | EXTRACTED | forja_ar_evolucao.py:110 |
| forja_ar_evolucao.py::selecionar_winner | calls | forja_ar_evolucao.py::_save | EXTRACTED | forja_ar_evolucao.py:146 |
| forja_ar_evolucao.py::selecionar_winner | calls | forja_ar_evolucao.py::_manifest_path | EXTRACTED | forja_ar_evolucao.py:110 |
| forja_ar_evolucao.py::selecionar_winner | calls | forja_ar_evolucao.py::_load | EXTRACTED | forja_ar_evolucao.py:120 |
| forja_ar_evolucao.py::selecionar_winner | calls | forja_ar_evolucao.py::_load | EXTRACTED | forja_ar_evolucao.py:121 |
| forja_ar_evolucao.py::selecionar_winner | calls | forja_ar_evolucao.py::_manifest_path | EXTRACTED | forja_ar_evolucao.py:146 |
| forja_ar_evolucao.py::verificar_convergencia | calls | forja_ar_evolucao.py::_load | EXTRACTED | forja_ar_evolucao.py:152 |
| forja_ar_evolucao.py::verificar_convergencia | calls | forja_ar_evolucao.py::_manifest_path | EXTRACTED | forja_ar_evolucao.py:152 |
| forja_ar_evolucao.py::main | calls | forja_ar_evolucao.py::init_experimento | EXTRACTED | forja_ar_evolucao.py:188 |
| forja_ar_evolucao.py::main | calls | forja_ar_evolucao.py::registrar_geracao | EXTRACTED | forja_ar_evolucao.py:190 |
| forja_ar_evolucao.py::main | calls | forja_ar_evolucao.py::selecionar_winner | EXTRACTED | forja_ar_evolucao.py:192 |
| forja_ar_evolucao.py::main | calls | forja_ar_evolucao.py::verificar_convergencia | EXTRACTED | forja_ar_evolucao.py:195 |
| forja_ar_indicadores.py | imports_from | forja_metricas_f7.py | EXTRACTED | forja_ar_indicadores.py:69 |
| forja_ar_indicadores.py | imports_from | forja_verificador.py | EXTRACTED | forja_ar_indicadores.py:187 |
| forja_ar_indicadores.py | imports_from | forja_estilo_humano.py | EXTRACTED | forja_ar_indicadores.py:216 |
| forja_ar_indicadores.py | imports_from | forja_human_review.py | EXTRACTED | forja_ar_indicadores.py:158 |
| forja_ar_indicadores.py::_i1 | calls | forja_ar_indicadores.py::_entries | EXTRACTED | forja_ar_indicadores.py:62 |
| forja_ar_indicadores.py::_i1 | calls | forja_ar_indicadores.py::_null | EXTRACTED | forja_ar_indicadores.py:64 |
| forja_ar_indicadores.py::_i1 | calls | forja_ar_indicadores.py::_null | EXTRACTED | forja_ar_indicadores.py:67 |
| forja_ar_indicadores.py::_i1 | calls | forja_metricas_f7.py::extrair_citacoes_basico | EXTRACTED | forja_ar_indicadores.py:71 |
| forja_ar_indicadores.py::_i1 | calls | forja_ar_indicadores.py::_terms | EXTRACTED | forja_ar_indicadores.py:76 |
| forja_ar_indicadores.py::_i1 | calls | forja_ar_indicadores.py::_contains | EXTRACTED | forja_ar_indicadores.py:77 |
| forja_ar_indicadores.py::_i1 | calls | forja_ar_indicadores.py::_null | EXTRACTED | forja_ar_indicadores.py:73 |
| forja_ar_indicadores.py::_i3 | calls | forja_ar_indicadores.py::_entries | EXTRACTED | forja_ar_indicadores.py:97 |
| forja_ar_indicadores.py::_i3 | calls | forja_ar_indicadores.py::_null | EXTRACTED | forja_ar_indicadores.py:99 |
| forja_ar_indicadores.py::_i3 | calls | forja_ar_indicadores.py::_null | EXTRACTED | forja_ar_indicadores.py:102 |
| forja_ar_indicadores.py::_i3 | calls | forja_ar_indicadores.py::_terms | EXTRACTED | forja_ar_indicadores.py:105 |
| forja_ar_indicadores.py::_i3 | calls | forja_ar_indicadores.py::_terms | EXTRACTED | forja_ar_indicadores.py:106 |
| forja_ar_indicadores.py::_i3 | calls | forja_ar_indicadores.py::_contains | EXTRACTED | forja_ar_indicadores.py:107 |
| forja_ar_indicadores.py::_i3 | calls | forja_ar_indicadores.py::_contains | EXTRACTED | forja_ar_indicadores.py:110 |
| forja_ar_indicadores.py::_i7 | calls | forja_ar_indicadores.py::_entries | EXTRACTED | forja_ar_indicadores.py:121 |
| forja_ar_indicadores.py::_i7 | calls | forja_ar_indicadores.py::_entries | EXTRACTED | forja_ar_indicadores.py:123 |
| forja_ar_indicadores.py::_i7 | calls | forja_ar_indicadores.py::_null | EXTRACTED | forja_ar_indicadores.py:126 |
| forja_ar_indicadores.py::_i7 | calls | forja_ar_indicadores.py::_terms | EXTRACTED | forja_ar_indicadores.py:129 |
| forja_ar_indicadores.py::_i7 | calls | forja_ar_indicadores.py::_terms | EXTRACTED | forja_ar_indicadores.py:130 |
| forja_ar_indicadores.py::_i7 | calls | forja_ar_indicadores.py::_contains | EXTRACTED | forja_ar_indicadores.py:131 |
| forja_ar_indicadores.py::_i7 | calls | forja_ar_indicadores.py::_contains | EXTRACTED | forja_ar_indicadores.py:131 |
| forja_ar_indicadores.py::_i8 | calls | forja_ar_indicadores.py::_null | EXTRACTED | forja_ar_indicadores.py:143 |
| forja_ar_indicadores.py::_i8 | calls | forja_ar_indicadores.py::_null | EXTRACTED | forja_ar_indicadores.py:146 |
| forja_ar_indicadores.py::_i8 | calls | forja_ar_indicadores.py::_null | EXTRACTED | forja_ar_indicadores.py:150 |
| forja_ar_indicadores.py::_i8 | calls | forja_ar_indicadores.py::_null | EXTRACTED | forja_ar_indicadores.py:156 |
| forja_ar_indicadores.py::_i8 | calls | forja_human_review.py::validate_visual_review_receipt | EXTRACTED | forja_ar_indicadores.py:160 |
| forja_ar_indicadores.py::_i8 | calls | forja_ar_indicadores.py::_null | EXTRACTED | forja_ar_indicadores.py:169 |
| forja_ar_indicadores.py::computar_indicadores | calls | forja_ar_indicadores.py::_i1 | EXTRACTED | forja_ar_indicadores.py:228 |
| forja_ar_indicadores.py::computar_indicadores | calls | forja_ar_indicadores.py::_i3 | EXTRACTED | forja_ar_indicadores.py:229 |
| forja_ar_indicadores.py::computar_indicadores | calls | forja_ar_indicadores.py::_i7 | EXTRACTED | forja_ar_indicadores.py:230 |
| forja_ar_indicadores.py::computar_indicadores | calls | forja_ar_indicadores.py::_i8 | EXTRACTED | forja_ar_indicadores.py:231 |
| forja_ar_indicadores.py::computar_indicadores | calls | forja_ar_indicadores.py::_null | EXTRACTED | forja_ar_indicadores.py:232 |
| forja_ar_indicadores.py::computar_indicadores | calls | forja_ar_indicadores.py::_null | EXTRACTED | forja_ar_indicadores.py:233 |
| forja_ar_indicadores.py::computar_indicadores | calls | forja_verificador.py::verificar | EXTRACTED | forja_ar_indicadores.py:189 |
| forja_ar_indicadores.py::computar_indicadores | calls | forja_estilo_humano.py::relatorio | EXTRACTED | forja_ar_indicadores.py:218 |
| forja_ar_indicadores.py::computar_indicadores | calls | forja_ar_indicadores.py::_sha | EXTRACTED | forja_ar_indicadores.py:238 |
| forja_ar_indicadores.py::computar_indicadores | calls | forja_ar_indicadores.py::_sensor_versions | EXTRACTED | forja_ar_indicadores.py:239 |
| forja_ar_indicadores.py::computar_indicadores | calls | forja_ar_indicadores.py::_null | EXTRACTED | forja_ar_indicadores.py:227 |
| forja_ar_indicadores.py::computar_indicadores | calls | forja_ar_indicadores.py::_null | EXTRACTED | forja_ar_indicadores.py:213 |
| forja_ar_indicadores.py::cache_key | calls | forja_ar_indicadores.py::_sha | EXTRACTED | forja_ar_indicadores.py:289 |
| forja_ar_indicadores.py::cache_key | calls | forja_ar_indicadores.py::_sha | EXTRACTED | forja_ar_indicadores.py:288 |
| forja_ar_indicadores.py::cache_key | calls | forja_ar_indicadores.py::_sha | EXTRACTED | forja_ar_indicadores.py:288 |
| forja_ar_indicadores.py::cache_key | calls | forja_ar_indicadores.py::_sha | EXTRACTED | forja_ar_indicadores.py:288 |
| forja_ar_indicadores.py::cache_key | calls | forja_ar_indicadores.py::_canonical | EXTRACTED | forja_ar_indicadores.py:288 |
| forja_ar_indicadores.py::cache_key | calls | forja_ar_indicadores.py::_canonical | EXTRACTED | forja_ar_indicadores.py:288 |
| forja_ar_indicadores.py::cache_key | calls | forja_ar_indicadores.py::_sensor_versions | EXTRACTED | forja_ar_indicadores.py:288 |
| forja_ar_indicadores.py::computar_com_cache | calls | forja_ar_indicadores.py::cache_key | EXTRACTED | forja_ar_indicadores.py:294 |
| forja_ar_indicadores.py::computar_com_cache | calls | forja_ar_indicadores.py::computar_indicadores | EXTRACTED | forja_ar_indicadores.py:298 |
| forja_ar_indicadores.py::main | calls | forja_ar_indicadores.py::computar_indicadores | EXTRACTED | forja_ar_indicadores.py:336 |
| forja_ar_indicadores.py::main | calls | forja_ar_indicadores.py::_load_ledgers | EXTRACTED | forja_ar_indicadores.py:336 |
| forja_ar_indicadores.py::main | calls | forja_ar_indicadores.py::comparar | EXTRACTED | forja_ar_indicadores.py:341 |
| forja_ar_runpair.py::freeze_input | calls | forja_ar_runpair.py::_sha | EXTRACTED | forja_ar_runpair.py:55 |
| forja_ar_runpair.py::freeze_input | calls | forja_ar_runpair.py::_canonical | EXTRACTED | forja_ar_runpair.py:60 |
| forja_ar_runpair.py::register_manifest | calls | forja_ar_runpair.py::_sha | EXTRACTED | forja_ar_runpair.py:88 |
| forja_ar_runpair.py::main | calls | forja_ar_runpair.py::freeze_input | EXTRACTED | forja_ar_runpair.py:181 |
| forja_ar_runpair.py::main | calls | forja_ar_runpair.py::register_manifest | EXTRACTED | forja_ar_runpair.py:193 |
| forja_ar_runpair.py::main | calls | forja_ar_runpair.py::validate_pair | EXTRACTED | forja_ar_runpair.py:196 |
| forja_ar_runpair.py::main | calls | forja_ar_runpair.py::_read_ledger | EXTRACTED | forja_ar_runpair.py:185 |
| forja_ar_runpair.py::main | calls | forja_ar_runpair.py::_read_ledger | EXTRACTED | forja_ar_runpair.py:186 |
| forja_artefatos.py::campo | calls | forja_artefatos.py::nomes | EXTRACTED | forja_artefatos.py:149 |
| forja_artefatos.py::lista | calls | forja_artefatos.py::campo | EXTRACTED | forja_artefatos.py:162 |
| forja_artefatos.py::censo | calls | forja_artefatos.py::ler | EXTRACTED | forja_artefatos.py:186 |
| forja_assinatura_visual.py::_caixas | calls | forja_assinatura_visual.py::_tabelas | EXTRACTED | forja_assinatura_visual.py:134 |
| forja_assinatura_visual.py::_inventario | calls | forja_assinatura_visual.py::_tabelas | EXTRACTED | forja_assinatura_visual.py:201 |
| forja_assinatura_visual.py::_inventario | calls | forja_assinatura_visual.py::_figuras_exibidas | EXTRACTED | forja_assinatura_visual.py:189 |
| forja_assinatura_visual.py::_inventario | calls | forja_assinatura_visual.py::_caixas | EXTRACTED | forja_assinatura_visual.py:239 |
| forja_assinatura_visual.py::avaliar | calls | forja_assinatura_visual.py::_inventario | EXTRACTED | forja_assinatura_visual.py:261 |
| forja_assinatura_visual.py::avaliar | calls | forja_assinatura_visual.py::_faixa | EXTRACTED | forja_assinatura_visual.py:265 |
| forja_assinatura_visual.py::avaliar | calls | forja_assinatura_visual.py::paginas_reais | EXTRACTED | forja_assinatura_visual.py:263 |
| forja_assinatura_visual.py::main | calls | forja_assinatura_visual.py::avaliar | EXTRACTED | forja_assinatura_visual.py:327 |
| forja_authorities.py::authority_key | calls | forja_authorities.py::normalize_number | EXTRACTED | forja_authorities.py:103 |
| forja_authorities.py::_entry | calls | forja_authorities.py::normalize_number | EXTRACTED | forja_authorities.py:141 |
| forja_authorities.py::_entry | calls | forja_authorities.py::_context | EXTRACTED | forja_authorities.py:146 |
| forja_authorities.py::_entry | calls | forja_authorities.py::normalize_number | EXTRACTED | forja_authorities.py:136 |
| forja_authorities.py::extract_authorities | calls | forja_authorities.py::authority_key | EXTRACTED | forja_authorities.py:157 |
| forja_authorities.py::extract_authorities | calls | forja_authorities.py::tribunal_from_cnj | EXTRACTED | forja_authorities.py:165 |
| forja_authorities.py::extract_authorities | calls | forja_authorities.py::_entry | EXTRACTED | forja_authorities.py:166 |
| forja_authorities.py::extract_authorities | calls | forja_authorities.py::_entry | EXTRACTED | forja_authorities.py:188 |
| forja_authorities.py::extract_authorities | calls | forja_authorities.py::_entry | EXTRACTED | forja_authorities.py:197 |
| forja_authorities.py::extract_authorities | calls | forja_authorities.py::_entry | EXTRACTED | forja_authorities.py:228 |
| forja_authorities.py::extract_authorities | calls | forja_authorities.py::normalize_number | EXTRACTED | forja_authorities.py:241 |
| forja_authorities.py::extract_authorities | calls | forja_authorities.py::normalize_number | EXTRACTED | forja_authorities.py:242 |
| forja_authorities.py::extract_authorities | calls | forja_authorities.py::_entry | EXTRACTED | forja_authorities.py:244 |
| forja_authorities.py::extract_authorities | calls | forja_authorities.py::_entry | EXTRACTED | forja_authorities.py:177 |
| forja_authorities.py::extract_authorities | calls | forja_authorities.py::normalize_number | EXTRACTED | forja_authorities.py:214 |
| forja_authorities.py::extract_authorities | calls | forja_authorities.py::_entry | EXTRACTED | forja_authorities.py:216 |
| forja_axi.py::AxiError.__init__ | calls | forja_axi.py::AxiError.__init__ | AMBIGUOUS | forja_axi.py:123 |
| forja_axi.py::AxiError.__init__ | calls | forja_axi.py::AxiArgumentParser.__init__ | AMBIGUOUS | forja_axi.py:123 |
| forja_axi.py::AxiArgumentParser.__init__ | calls | forja_axi.py::AxiError.__init__ | AMBIGUOUS | forja_axi.py:134 |
| forja_axi.py::AxiArgumentParser.__init__ | calls | forja_axi.py::AxiArgumentParser.__init__ | AMBIGUOUS | forja_axi.py:134 |
| forja_axi.py::AxiArgumentParser.error | calls | forja_axi.py::AxiError | EXTRACTED | forja_axi.py:137 |
| forja_axi.py::_read_json | calls | forja_axi.py::AxiError | EXTRACTED | forja_axi.py:161 |
| forja_axi.py::_read_json | calls | forja_axi.py::AxiError | EXTRACTED | forja_axi.py:167 |
| forja_axi.py::_load_cases | calls | forja_axi.py::_case_files | EXTRACTED | forja_axi.py:242 |
| forja_axi.py::_load_cases | calls | forja_axi.py::_read_json | EXTRACTED | forja_axi.py:244 |
| forja_axi.py::_load_cases | calls | forja_axi.py::AxiError | EXTRACTED | forja_axi.py:246 |
| forja_axi.py::_load_cases | calls | forja_axi.py::_case_summary | EXTRACTED | forja_axi.py:247 |
| forja_axi.py::_parse_fields | calls | forja_axi.py::AxiError | EXTRACTED | forja_axi.py:272 |
| forja_axi.py::home_payload | calls | forja_axi.py::_load_cases | EXTRACTED | forja_axi.py:295 |
| forja_axi.py::home_payload | calls | forja_axi.py::_read_json | EXTRACTED | forja_axi.py:299 |
| forja_axi.py::home_payload | calls | forja_axi.py::compact_path | EXTRACTED | forja_axi.py:307 |
| forja_axi.py::home_payload | calls | forja_axi.py::now_iso | EXTRACTED | forja_axi.py:310 |
| forja_axi.py::home_payload | calls | forja_axi.py::_queue_summary | EXTRACTED | forja_axi.py:301 |
| forja_axi.py::cases_payload | calls | forja_axi.py::_parse_fields | EXTRACTED | forja_axi.py:348 |
| forja_axi.py::cases_payload | calls | forja_axi.py::_load_cases | EXTRACTED | forja_axi.py:349 |
| forja_axi.py::cases_payload | calls | forja_axi.py::AxiError | EXTRACTED | forja_axi.py:342 |
| forja_axi.py::cases_payload | calls | forja_axi.py::_select_fields | EXTRACTED | forja_axi.py:358 |
| forja_axi.py::_resolve_case_path | calls | forja_axi.py::AxiError | EXTRACTED | forja_axi.py:395 |
| forja_axi.py::_resolve_case_path | calls | forja_axi.py::AxiError | EXTRACTED | forja_axi.py:376 |
| forja_axi.py::_resolve_case_path | calls | forja_axi.py::_case_files | EXTRACTED | forja_axi.py:387 |
| forja_axi.py::case_payload | calls | forja_axi.py::_parse_fields | EXTRACTED | forja_axi.py:409 |
| forja_axi.py::case_payload | calls | forja_axi.py::_resolve_case_path | EXTRACTED | forja_axi.py:410 |
| forja_axi.py::case_payload | calls | forja_axi.py::_read_json | EXTRACTED | forja_axi.py:411 |
| forja_axi.py::case_payload | calls | forja_axi.py::_case_summary | EXTRACTED | forja_axi.py:414 |
| forja_axi.py::case_payload | calls | forja_axi.py::AxiError | EXTRACTED | forja_axi.py:413 |
| forja_axi.py::case_payload | calls | forja_axi.py::_truncate | EXTRACTED | forja_axi.py:418 |
| forja_axi.py::case_payload | calls | forja_axi.py::_select_fields | EXTRACTED | forja_axi.py:424 |
| forja_axi.py::case_payload | calls | forja_axi.py::_blocker_text | EXTRACTED | forja_axi.py:418 |
| forja_axi.py::queue_payload | calls | forja_axi.py::_parse_fields | EXTRACTED | forja_axi.py:471 |
| forja_axi.py::queue_payload | calls | forja_axi.py::_read_json | EXTRACTED | forja_axi.py:472 |
| forja_axi.py::queue_payload | calls | forja_axi.py::AxiError | EXTRACTED | forja_axi.py:465 |
| forja_axi.py::queue_payload | calls | forja_axi.py::AxiError | EXTRACTED | forja_axi.py:474 |
| forja_axi.py::queue_payload | calls | forja_axi.py::AxiError | EXTRACTED | forja_axi.py:476 |
| forja_axi.py::queue_payload | calls | forja_axi.py::_queue_summary | EXTRACTED | forja_axi.py:498 |
| forja_axi.py::queue_payload | calls | forja_axi.py::_select_fields | EXTRACTED | forja_axi.py:501 |
| forja_axi.py::queue_payload | calls | forja_axi.py::_queue_item | EXTRACTED | forja_axi.py:491 |
| forja_axi.py::commands_payload | calls | forja_axi.py::AxiError | EXTRACTED | forja_axi.py:521 |
| forja_axi.py::health_payload | calls | forja_axi.py::_read_json | EXTRACTED | forja_axi.py:571 |
| forja_axi.py::_toon_string | calls | forja_axi.py::_needs_quote | EXTRACTED | forja_axi.py:609 |
| forja_axi.py::_toon_primitive | calls | forja_axi.py::_toon_string | EXTRACTED | forja_axi.py:640 |
| forja_axi.py::_uniform_primitive_rows | calls | forja_axi.py::_is_primitive | EXTRACTED | forja_axi.py:654 |
| forja_axi.py::_encode_toon_value | calls | forja_axi.py::_is_primitive | EXTRACTED | forja_axi.py:668 |
| forja_axi.py::_encode_toon_value | calls | forja_axi.py::_uniform_primitive_rows | EXTRACTED | forja_axi.py:686 |
| forja_axi.py::_encode_toon_value | calls | forja_axi.py::_encode_toon_value | EXTRACTED | forja_axi.py:675 |
| forja_axi.py::_encode_toon_value | calls | forja_axi.py::_toon_string | EXTRACTED | forja_axi.py:687 |
| forja_axi.py::_encode_toon_value | calls | forja_axi.py::_is_primitive | EXTRACTED | forja_axi.py:703 |
| forja_axi.py::_encode_toon_value | calls | forja_axi.py::_toon_string | EXTRACTED | forja_axi.py:737 |
| forja_axi.py::_encode_toon_value | calls | forja_axi.py::_toon_string | EXTRACTED | forja_axi.py:667 |
| forja_axi.py::_encode_toon_value | calls | forja_axi.py::_toon_primitive | EXTRACTED | forja_axi.py:669 |
| forja_axi.py::_encode_toon_value | calls | forja_axi.py::_is_primitive | EXTRACTED | forja_axi.py:697 |
| forja_axi.py::_encode_toon_value | calls | forja_axi.py::_toon_string | EXTRACTED | forja_axi.py:689 |
| forja_axi.py::_encode_toon_value | calls | forja_axi.py::_toon_primitive | EXTRACTED | forja_axi.py:698 |
| forja_axi.py::_encode_toon_value | calls | forja_axi.py::_is_primitive | EXTRACTED | forja_axi.py:708 |
| forja_axi.py::_encode_toon_value | calls | forja_axi.py::_toon_primitive | EXTRACTED | forja_axi.py:704 |
| forja_axi.py::_encode_toon_value | calls | forja_axi.py::_toon_string | EXTRACTED | forja_axi.py:673 |
| forja_axi.py::_encode_toon_value | calls | forja_axi.py::_encode_toon_value | EXTRACTED | forja_axi.py:715 |
| forja_axi.py::_encode_toon_value | calls | forja_axi.py::_encode_toon_value | EXTRACTED | forja_axi.py:724 |
| forja_axi.py::_encode_toon_value | calls | forja_axi.py::_toon_string | EXTRACTED | forja_axi.py:734 |
| forja_axi.py::_encode_toon_value | calls | forja_axi.py::_toon_primitive | EXTRACTED | forja_axi.py:694 |
| forja_axi.py::_encode_toon_value | calls | forja_axi.py::_toon_primitive | EXTRACTED | forja_axi.py:712 |
| forja_axi.py::_encode_toon_value | calls | forja_axi.py::_toon_string | EXTRACTED | forja_axi.py:711 |
| forja_axi.py::encode_toon | calls | forja_axi.py::_encode_toon_value | EXTRACTED | forja_axi.py:744 |
| forja_axi.py::render | calls | forja_axi.py::encode_toon | EXTRACTED | forja_axi.py:751 |
| forja_axi.py::_extract_output_format | calls | forja_axi.py::AxiError | EXTRACTED | forja_axi.py:766 |
| forja_axi.py::_extract_output_format | calls | forja_axi.py::AxiError | EXTRACTED | forja_axi.py:774 |
| forja_axi.py::build_parser | calls | forja_axi.py::AxiArgumentParser | EXTRACTED | forja_axi.py:786 |
| forja_axi.py::_dispatch | calls | forja_axi.py::AxiError | EXTRACTED | forja_axi.py:860 |
| forja_axi.py::_dispatch | calls | forja_axi.py::home_payload | EXTRACTED | forja_axi.py:832 |
| forja_axi.py::_dispatch | calls | forja_axi.py::cases_payload | EXTRACTED | forja_axi.py:834 |
| forja_axi.py::_dispatch | calls | forja_axi.py::case_payload | EXTRACTED | forja_axi.py:842 |
| forja_axi.py::_dispatch | calls | forja_axi.py::queue_payload | EXTRACTED | forja_axi.py:849 |
| forja_axi.py::_dispatch | calls | forja_axi.py::commands_payload | EXTRACTED | forja_axi.py:857 |
| forja_axi.py::_dispatch | calls | forja_axi.py::health_payload | EXTRACTED | forja_axi.py:859 |
| forja_axi.py::main | calls | forja_axi.py::_extract_output_format | EXTRACTED | forja_axi.py:876 |
| forja_axi.py::main | calls | forja_axi.py::_dispatch | EXTRACTED | forja_axi.py:878 |
| forja_axi.py::main | calls | forja_axi.py::render | EXTRACTED | forja_axi.py:879 |
| forja_axi.py::main | calls | forja_axi.py::build_parser | EXTRACTED | forja_axi.py:877 |
| forja_axi.py::main | calls | forja_axi.py::render | EXTRACTED | forja_axi.py:901 |
| forja_baseline.py::_pytest | calls | forja_baseline.py::_run | EXTRACTED | forja_baseline.py:102 |
| forja_baseline.py::_script | calls | forja_baseline.py::_run | EXTRACTED | forja_baseline.py:117 |
| forja_baseline.py::_scripts_autonomos_nao_mapeados | calls | forja_baseline.py::_parece_script_autonomo | EXTRACTED | forja_baseline.py:140 |
| forja_baseline.py::coletar | calls | forja_baseline.py::_parece_script_autonomo | EXTRACTED | forja_baseline.py:148 |
| forja_baseline.py::executar | calls | forja_baseline.py::_pytest | EXTRACTED | forja_baseline.py:153 |
| forja_baseline.py::executar | calls | forja_baseline.py::_script | EXTRACTED | forja_baseline.py:167 |
| forja_baseline.py::executar | calls | forja_baseline.py::coletar | EXTRACTED | forja_baseline.py:153 |
| forja_baseline.py::executar | calls | forja_baseline.py::_scripts_autonomos_nao_mapeados | EXTRACTED | forja_baseline.py:165 |
| forja_baseline.py::main | calls | forja_baseline.py::executar | EXTRACTED | forja_baseline.py:206 |
| forja_baseline.py::main | calls | forja_baseline.py::_imprimir | EXTRACTED | forja_baseline.py:208 |
| forja_baseline_aprovado.py | imports_from | forja_docx_layout.py | EXTRACTED | forja_baseline_aprovado.py:83 |
| forja_baseline_aprovado.py | imports_from | forja_n3_common.py | EXTRACTED | forja_baseline_aprovado.py:139 |
| forja_baseline_aprovado.py::_medir | calls | forja_docx_layout.py::audit_docx_layout | EXTRACTED | forja_baseline_aprovado.py:85 |
| forja_baseline_aprovado.py::conferir | calls | forja_baseline_aprovado.py::_resolver | EXTRACTED | forja_baseline_aprovado.py:107 |
| forja_baseline_aprovado.py::conferir | calls | forja_baseline_aprovado.py::_medir | EXTRACTED | forja_baseline_aprovado.py:113 |
| forja_baseline_aprovado.py::gravar | calls | forja_baseline_aprovado.py::_resolver | EXTRACTED | forja_baseline_aprovado.py:143 |
| forja_baseline_aprovado.py::gravar | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_baseline_aprovado.py:149 |
| forja_baseline_aprovado.py::gravar | calls | forja_baseline_aprovado.py::_medir | EXTRACTED | forja_baseline_aprovado.py:147 |
| forja_bench_modelos.py | imports_from | forja_modelos.py | EXTRACTED | forja_bench_modelos.py:27 |
| forja_bench_modelos.py::avaliar | calls | forja_bench_modelos.py::_norm | EXTRACTED | forja_bench_modelos.py:179 |
| forja_bench_modelos.py::avaliar | calls | forja_bench_modelos.py::_sinal_afirmado | EXTRACTED | forja_bench_modelos.py:183 |
| forja_bench_modelos.py::avaliar | calls | forja_bench_modelos.py::_norm | EXTRACTED | forja_bench_modelos.py:180 |
| forja_bench_modelos.py::avaliar | calls | forja_bench_modelos.py::_norm | EXTRACTED | forja_bench_modelos.py:183 |
| forja_bench_modelos.py::avaliar | calls | forja_bench_modelos.py::_norm | EXTRACTED | forja_bench_modelos.py:185 |
| forja_bench_modelos.py::rodar | calls | forja_modelos.py::Orcamento | EXTRACTED | forja_bench_modelos.py:226 |
| forja_bench_modelos.py::rodar | calls | forja_bench_modelos.py::_resumir | EXTRACTED | forja_bench_modelos.py:256 |
| forja_bench_modelos.py::rodar | calls | forja_modelos.py::chamar | EXTRACTED | forja_bench_modelos.py:233 |
| forja_bench_modelos.py::rodar | calls | forja_bench_modelos.py::avaliar | EXTRACTED | forja_bench_modelos.py:242 |
| forja_bench_modelos.py::reavaliar | calls | forja_bench_modelos.py::_resumir | EXTRACTED | forja_bench_modelos.py:288 |
| forja_bench_modelos.py::reavaliar | calls | forja_bench_modelos.py::avaliar | EXTRACTED | forja_bench_modelos.py:278 |
| forja_bench_modelos.py::main | calls | forja_bench_modelos.py::_imprimir | EXTRACTED | forja_bench_modelos.py:332 |
| forja_bench_modelos.py::main | calls | forja_bench_modelos.py::rodar | EXTRACTED | forja_bench_modelos.py:332 |
| forja_bench_modelos.py::main | calls | forja_bench_modelos.py::_imprimir | EXTRACTED | forja_bench_modelos.py:339 |
| forja_bench_modelos.py::main | calls | forja_bench_modelos.py::_imprimir | EXTRACTED | forja_bench_modelos.py:341 |
| forja_bench_modelos.py::main | calls | forja_bench_modelos.py::reavaliar | EXTRACTED | forja_bench_modelos.py:341 |
| forja_calibra_gates_economicos.py | imports_from | forja_lastro.py | EXTRACTED | forja_calibra_gates_economicos.py:38 |
| forja_calibra_gates_economicos.py | imports_from | forja_lastro.py | EXTRACTED | forja_calibra_gates_economicos.py:38 |
| forja_calibra_gates_economicos.py | imports_from | forja_lastro.py | EXTRACTED | forja_calibra_gates_economicos.py:38 |
| forja_calibra_gates_economicos.py | imports_from | forja_lastro.py | EXTRACTED | forja_calibra_gates_economicos.py:38 |
| forja_calibra_gates_economicos.py::main | calls | forja_lastro.py::_valores_monetarios | EXTRACTED | forja_calibra_gates_economicos.py:92 |
| forja_calibra_gates_economicos.py::main | calls | forja_lastro.py::validar_valores_monetarios | EXTRACTED | forja_calibra_gates_economicos.py:98 |
| forja_calibra_gates_economicos.py::main | calls | forja_calibra_gates_economicos.py::relevante | EXTRACTED | forja_calibra_gates_economicos.py:81 |
| forja_calibra_gates_economicos.py::main | calls | forja_lastro.py::material_economico | EXTRACTED | forja_calibra_gates_economicos.py:88 |
| forja_calibra_monetario.py::calibrar | calls | forja_calibra_monetario.py::varrer | EXTRACTED | forja_calibra_monetario.py:101 |
| forja_calibra_monetario.py::calibrar | calls | forja_calibra_monetario.py::_texto | EXTRACTED | forja_calibra_monetario.py:107 |
| forja_calibra_monetario.py::calibrar | calls | forja_calibra_monetario.py::ocorrencias_ampla | EXTRACTED | forja_calibra_monetario.py:114 |
| forja_calibra_monetario.py::calibrar | calls | forja_calibra_monetario.py::economico_amplo | EXTRACTED | forja_calibra_monetario.py:111 |
| forja_calibra_monetario.py::calibrar | calls | forja_calibra_monetario.py::economico_estreito | EXTRACTED | forja_calibra_monetario.py:111 |
| forja_calibra_monetario.py::calibrar | calls | forja_calibra_monetario.py::ocorrencias_ampla | EXTRACTED | forja_calibra_monetario.py:118 |
| forja_calibra_monetario.py::calibrar | calls | forja_calibra_monetario.py::_amostrar_contexto | EXTRACTED | forja_calibra_monetario.py:122 |
| forja_calibra_monetario.py::main | calls | forja_calibra_monetario.py::calibrar | EXTRACTED | forja_calibra_monetario.py:171 |
| forja_canario_catraca.py::canario | calls | forja_canario_catraca.py::catracas | EXTRACTED | forja_canario_catraca.py:114 |
| forja_canario_catraca.py::canario | calls | forja_canario_catraca.py::_aperta | EXTRACTED | forja_canario_catraca.py:121 |
| forja_canario_mutacao.py | imports_from | forja_recomputo_censo.py | EXTRACTED | forja_canario_mutacao.py:124 |
| forja_canario_mutacao.py | imports_from | forja_recomputo_censo.py | EXTRACTED | forja_canario_mutacao.py:211 |
| forja_canario_mutacao.py::_muta | calls | forja_canario_mutacao.py::_muta | EXTRACTED | forja_canario_mutacao.py:111 |
| forja_canario_mutacao.py::_muta | calls | forja_canario_mutacao.py::_muta | EXTRACTED | forja_canario_mutacao.py:117 |
| forja_canario_mutacao.py::_vereditos | calls | forja_recomputo_censo.py::_produtores | EXTRACTED | forja_canario_mutacao.py:127 |
| forja_canario_mutacao.py::_muta_arquivo | calls | forja_canario_mutacao.py::_muta_texto | EXTRACTED | forja_canario_mutacao.py:153 |
| forja_canario_mutacao.py::_muta_arquivo | calls | forja_canario_mutacao.py::_muta | EXTRACTED | forja_canario_mutacao.py:146 |
| forja_canario_mutacao.py::_internaliza_externos | calls | forja_canario_mutacao.py::_muta_arquivo | EXTRACTED | forja_canario_mutacao.py:201 |
| forja_canario_mutacao.py::canario | calls | forja_canario_mutacao.py::_tentativas | EXTRACTED | forja_canario_mutacao.py:218 |
| forja_canario_mutacao.py::canario | calls | forja_recomputo_censo.py::_ler | EXTRACTED | forja_canario_mutacao.py:219 |
| forja_canario_mutacao.py::canario | calls | forja_canario_mutacao.py::_vereditos | EXTRACTED | forja_canario_mutacao.py:221 |
| forja_canario_mutacao.py::canario | calls | forja_canario_mutacao.py::_internaliza_externos | EXTRACTED | forja_canario_mutacao.py:263 |
| forja_canario_mutacao.py::canario | calls | forja_canario_mutacao.py::_vereditos | EXTRACTED | forja_canario_mutacao.py:266 |
| forja_canario_mutacao.py::canario | calls | forja_canario_mutacao.py::_muta_texto | EXTRACTED | forja_canario_mutacao.py:261 |
| forja_canario_mutacao.py::canario | calls | forja_canario_mutacao.py::_muta | EXTRACTED | forja_canario_mutacao.py:253 |
| forja_case_tests.py | imports_from | forja_n3_common.py | EXTRACTED | forja_case_tests.py:11 |
| forja_case_tests.py | imports_from | forja_n3_common.py | EXTRACTED | forja_case_tests.py:11 |
| forja_case_tests.py | imports_from | forja_n3_common.py | EXTRACTED | forja_case_tests.py:11 |
| forja_case_tests.py | imports_from | forja_n3_common.py | EXTRACTED | forja_case_tests.py:11 |
| forja_case_tests.py | imports_from | forja_n4_common.py | EXTRACTED | forja_case_tests.py:12 |
| forja_case_tests.py | imports_from | forja_n4_common.py | EXTRACTED | forja_case_tests.py:12 |
| forja_case_tests.py | imports_from | forja_n4_common.py | EXTRACTED | forja_case_tests.py:12 |
| forja_case_tests.py::suite_hash | calls | forja_n3_common.py::canonical_hash | EXTRACTED | forja_case_tests.py:34 |
| forja_case_tests.py::validate_suite | calls | forja_n4_common.py::ids_unique | EXTRACTED | forja_case_tests.py:50 |
| forja_case_tests.py::validate_suite | calls | forja_n4_common.py::issue | EXTRACTED | forja_case_tests.py:53 |
| forja_case_tests.py::validate_suite | calls | forja_n4_common.py::issue | EXTRACTED | forja_case_tests.py:72 |
| forja_case_tests.py::validate_suite | calls | forja_case_tests.py::suite_hash | EXTRACTED | forja_case_tests.py:84 |
| forja_case_tests.py::validate_suite | calls | forja_n4_common.py::issue | EXTRACTED | forja_case_tests.py:85 |
| forja_case_tests.py::validate_suite | calls | forja_case_tests.py::_parse_aware_iso | EXTRACTED | forja_case_tests.py:60 |
| forja_case_tests.py::validate_suite | calls | forja_case_tests.py::_parse_aware_iso | EXTRACTED | forja_case_tests.py:61 |
| forja_case_tests.py::validate_suite | calls | forja_n4_common.py::issue | EXTRACTED | forja_case_tests.py:76 |
| forja_case_tests.py::validate_suite | calls | forja_n4_common.py::issue | EXTRACTED | forja_case_tests.py:78 |
| forja_case_tests.py::validate_suite | calls | forja_n4_common.py::issue | EXTRACTED | forja_case_tests.py:80 |
| forja_case_tests.py::validate_suite | calls | forja_n4_common.py::issue | EXTRACTED | forja_case_tests.py:82 |
| forja_case_tests.py::validate_suite | calls | forja_n4_common.py::issue | EXTRACTED | forja_case_tests.py:56 |
| forja_case_tests.py::validate_suite | calls | forja_n4_common.py::issue | EXTRACTED | forja_case_tests.py:59 |
| forja_case_tests.py::validate_suite | calls | forja_n4_common.py::issue | EXTRACTED | forja_case_tests.py:63 |
| forja_case_tests.py::validate_suite | calls | forja_n4_common.py::issue | EXTRACTED | forja_case_tests.py:68 |
| forja_case_tests.py::validate_suite | calls | forja_n4_common.py::issue | EXTRACTED | forja_case_tests.py:70 |
| forja_case_tests.py::validate_suite | calls | forja_n4_common.py::issue | EXTRACTED | forja_case_tests.py:65 |
| forja_case_tests.py::run_suite | calls | forja_case_tests.py::validate_suite | EXTRACTED | forja_case_tests.py:110 |
| forja_case_tests.py::run_suite | calls | forja_case_tests.py::suite_hash | EXTRACTED | forja_case_tests.py:152 |
| forja_case_tests.py::run_suite | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_case_tests.py:153 |
| forja_case_tests.py::run_suite | calls | forja_n4_common.py::issue | EXTRACTED | forja_case_tests.py:112 |
| forja_case_tests.py::run_suite | calls | forja_case_tests.py::_deterministic | EXTRACTED | forja_case_tests.py:117 |
| forja_case_tests.py::run_suite | calls | forja_n4_common.py::issue | EXTRACTED | forja_case_tests.py:150 |
| forja_case_tests.py::run_suite | calls | forja_n4_common.py::issue | EXTRACTED | forja_case_tests.py:120 |
| forja_case_tests.py::run_suite | calls | forja_case_tests.py::_deterministic | EXTRACTED | forja_case_tests.py:141 |
| forja_case_tests.py::validate_results | calls | forja_case_tests.py::suite_hash | EXTRACTED | forja_case_tests.py:164 |
| forja_case_tests.py::validate_results | calls | forja_n4_common.py::issue | EXTRACTED | forja_case_tests.py:165 |
| forja_case_tests.py::validate_results | calls | forja_n4_common.py::issue | EXTRACTED | forja_case_tests.py:167 |
| forja_case_tests.py::validate_results | calls | forja_n4_common.py::issue | EXTRACTED | forja_case_tests.py:178 |
| forja_case_tests.py::validate_results | calls | forja_n4_common.py::issue | EXTRACTED | forja_case_tests.py:182 |
| forja_case_tests.py::validate_results | calls | forja_n4_common.py::issue | EXTRACTED | forja_case_tests.py:184 |
| forja_case_tests.py::validate_results | calls | forja_n4_common.py::issue | EXTRACTED | forja_case_tests.py:188 |
| forja_case_tests.py::validate_results | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_case_tests.py:166 |
| forja_case_tests.py::validate_results | calls | forja_n4_common.py::issue | EXTRACTED | forja_case_tests.py:170 |
| forja_case_tests.py::main | calls | forja_n3_common.py::resolve_case_dir | EXTRACTED | forja_case_tests.py:200 |
| forja_case_tests.py::main | calls | forja_n4_common.py::validate_file | EXTRACTED | forja_case_tests.py:201 |
| forja_case_tests.py::main | calls | forja_case_tests.py::run_suite | EXTRACTED | forja_case_tests.py:205 |
| forja_case_tests.py::main | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_case_tests.py:209 |
| forja_citations.py | imports_from | forja_authorities.py | EXTRACTED | forja_citations.py:23 |
| forja_citations.py | imports_from | forja_authorities.py | EXTRACTED | forja_citations.py:23 |
| forja_citations.py | imports_from | forja_authorities.py | EXTRACTED | forja_citations.py:23 |
| forja_citations.py | imports_from | forja_n3_common.py | EXTRACTED | forja_citations.py:24 |
| forja_citations.py | imports_from | forja_n3_common.py | EXTRACTED | forja_citations.py:24 |
| forja_citations.py | imports_from | forja_official_sources.py | EXTRACTED | forja_citations.py:25 |
| forja_citations.py | imports_from | forja_official_sources.py | EXTRACTED | forja_citations.py:25 |
| forja_citations.py | imports_from | forja_metricas_f7.py | EXTRACTED | forja_citations.py:156 |
| forja_citations.py::tribunal_numero_cnj | calls | forja_authorities.py::tribunal_from_cnj | EXTRACTED | forja_citations.py:53 |
| forja_citations.py::normalizar_numero | calls | forja_authorities.py::normalize_number | EXTRACTED | forja_citations.py:77 |
| forja_citations.py::url_oficial | calls | forja_citations.py::tribunal_numero_cnj | EXTRACTED | forja_citations.py:82 |
| forja_citations.py::extrair_citacoes | calls | forja_authorities.py::extract_authorities | EXTRACTED | forja_citations.py:116 |
| forja_citations.py::procurar_cache_oficial | calls | forja_citations.py::normalizar_numero | EXTRACTED | forja_citations.py:127 |
| forja_citations.py::procurar_cache_oficial | calls | forja_metricas_f7.py::cache_com_lastro | EXTRACTED | forja_citations.py:159 |
| forja_citations.py::conferir_aspas | calls | forja_citations.py::normalizar_aspa | EXTRACTED | forja_citations.py:183 |
| forja_citations.py::conferir_aspas | calls | forja_citations.py::normalizar_aspa | EXTRACTED | forja_citations.py:189 |
| forja_citations.py::procurar_fonte_local | calls | forja_citations.py::normalizar_numero | EXTRACTED | forja_citations.py:202 |
| forja_citations.py::procurar_fonte_local | calls | forja_citations.py::normalizar_numero | EXTRACTED | forja_citations.py:211 |
| forja_citations.py::procurar_fonte_local | calls | forja_official_sources.py::validate_archived_source | EXTRACTED | forja_citations.py:211 |
| forja_citations.py::procurar_fonte_local | calls | forja_citations.py::normalizar_numero | EXTRACTED | forja_citations.py:216 |
| forja_citations.py::procurar_fonte_local | calls | forja_official_sources.py::validate_archived_source | EXTRACTED | forja_citations.py:217 |
| forja_citations.py::processar | calls | forja_citations.py::texto_da_peca | EXTRACTED | forja_citations.py:255 |
| forja_citations.py::processar | calls | forja_citations.py::extrair_citacoes | EXTRACTED | forja_citations.py:256 |
| forja_citations.py::processar | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_citations.py:316 |
| forja_citations.py::processar | calls | forja_citations.py::merge_by_id | EXTRACTED | forja_citations.py:321 |
| forja_citations.py::processar | calls | forja_citations.py::append_unique | EXTRACTED | forja_citations.py:322 |
| forja_citations.py::processar | calls | forja_citations.py::procurar_cache_oficial | EXTRACTED | forja_citations.py:272 |
| forja_citations.py::processar | calls | forja_citations.py::procurar_fonte_local | EXTRACTED | forja_citations.py:273 |
| forja_citations.py::processar | calls | forja_citations.py::url_oficial | EXTRACTED | forja_citations.py:274 |
| forja_citations.py::processar | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_citations.py:319 |
| forja_citations.py::processar | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_citations.py:261 |
| forja_citations.py::processar | calls | forja_official_sources.py::validate_cached_source | EXTRACTED | forja_citations.py:276 |
| forja_citations.py::processar | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_citations.py:297 |
| forja_citations.py::processar | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_citations.py:301 |
| forja_citations.py::processar | calls | forja_official_sources.py::validate_archived_source | EXTRACTED | forja_citations.py:282 |
| forja_citations.py::_indice_do_ledger | calls | forja_citations.py::_chave_autoridade | EXTRACTED | forja_citations.py:388 |
| forja_citations.py::_indice_do_ledger | calls | forja_citations.py::extrair_citacoes | EXTRACTED | forja_citations.py:396 |
| forja_citations.py::_indice_do_ledger | calls | forja_citations.py::_chave_autoridade | EXTRACTED | forja_citations.py:397 |
| forja_citations.py::validar_politica_citacoes | calls | forja_citations.py::extrair_citacoes | EXTRACTED | forja_citations.py:418 |
| forja_citations.py::validar_politica_citacoes | calls | forja_citations.py::_indice_do_ledger | EXTRACTED | forja_citations.py:426 |
| forja_citations.py::validar_politica_citacoes | calls | forja_citations.py::_chave_autoridade | EXTRACTED | forja_citations.py:453 |
| forja_citations.py::validar_identidade_citacoes | calls | forja_citations.py::extrair_citacoes | EXTRACTED | forja_citations.py:547 |
| forja_citations.py::validar_identidade_citacoes | calls | forja_citations.py::tribunal_numero_cnj | EXTRACTED | forja_citations.py:525 |
| forja_citations.py::validar_identidade_citacoes | calls | forja_citations.py::_indice_do_ledger | EXTRACTED | forja_citations.py:545 |
| forja_citations.py::validar_identidade_citacoes | calls | forja_citations.py::_normalizar_tribunal | EXTRACTED | forja_citations.py:530 |
| forja_citations.py::validar_identidade_citacoes | calls | forja_citations.py::_normalizar_tribunal | EXTRACTED | forja_citations.py:536 |
| forja_citations.py::main | calls | forja_citations.py::processar | EXTRACTED | forja_citations.py:582 |
| forja_claim_binding.py | imports_from | forja_authorities.py | EXTRACTED | forja_claim_binding.py:13 |
| forja_claim_binding.py | imports_from | forja_authorities.py | EXTRACTED | forja_claim_binding.py:13 |
| forja_claim_binding.py | imports_from | forja_n3_common.py | EXTRACTED | forja_claim_binding.py:14 |
| forja_claim_binding.py | imports_from | forja_n3_common.py | EXTRACTED | forja_claim_binding.py:14 |
| forja_claim_binding.py | imports_from | forja_n3_common.py | EXTRACTED | forja_claim_binding.py:14 |
| forja_claim_binding.py | imports_from | forja_n3_common.py | EXTRACTED | forja_claim_binding.py:14 |
| forja_claim_binding.py | imports_from | forja_n3_common.py | EXTRACTED | forja_claim_binding.py:14 |
| forja_claim_binding.py | imports_from | forja_official_sources.py | EXTRACTED | forja_claim_binding.py:15 |
| forja_claim_binding.py::_entries | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_claim_binding.py:23 |
| forja_claim_binding.py::bind_claims | calls | forja_n3_common.py::read_json | EXTRACTED | forja_claim_binding.py:28 |
| forja_claim_binding.py::bind_claims | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_claim_binding.py:35 |
| forja_claim_binding.py::bind_claims | calls | forja_claim_binding.py::_entries | EXTRACTED | forja_claim_binding.py:37 |
| forja_claim_binding.py::bind_claims | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_claim_binding.py:87 |
| forja_claim_binding.py::bind_claims | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_claim_binding.py:30 |
| forja_claim_binding.py::bind_claims | calls | forja_authorities.py::authority_key | EXTRACTED | forja_claim_binding.py:33 |
| forja_claim_binding.py::bind_claims | calls | forja_authorities.py::authority_key | EXTRACTED | forja_claim_binding.py:50 |
| forja_claim_binding.py::bind_claims | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_claim_binding.py:80 |
| forja_claim_binding.py::bind_claims | calls | forja_authorities.py::extract_authorities | EXTRACTED | forja_claim_binding.py:33 |
| forja_claim_binding.py::bind_claims | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_claim_binding.py:45 |
| forja_claim_binding.py::bind_claims | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_claim_binding.py:48 |
| forja_claim_binding.py::bind_claims | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_claim_binding.py:52 |
| forja_claim_binding.py::bind_claims | calls | forja_official_sources.py::source_excerpt_sha256 | EXTRACTED | forja_claim_binding.py:69 |
| forja_claim_binding.py::bind_claims | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_claim_binding.py:72 |
| forja_claim_binding.py::bind_claims | calls | forja_n3_common.py::canonical_hash | EXTRACTED | forja_claim_binding.py:62 |
| forja_claim_binding.py::bind_claims | calls | forja_n3_common.py::canonical_hash | EXTRACTED | forja_claim_binding.py:64 |
| forja_claim_binding.py::bind_claims | calls | forja_n3_common.py::canonical_hash | EXTRACTED | forja_claim_binding.py:65 |
| forja_claim_binding.py::bind_claims | calls | forja_authorities.py::authority_key | EXTRACTED | forja_claim_binding.py:77 |
| forja_claim_binding.py::main | calls | forja_claim_binding.py::bind_claims | EXTRACTED | forja_claim_binding.py:97 |
| forja_close_cycle.py | imports_from | forja_n3_common.py | EXTRACTED | forja_close_cycle.py:9 |
| forja_close_cycle.py | imports_from | forja_n3_common.py | EXTRACTED | forja_close_cycle.py:9 |
| forja_close_cycle.py | imports_from | forja_n3_common.py | EXTRACTED | forja_close_cycle.py:9 |
| forja_close_cycle.py | imports_from | forja_n3_common.py | EXTRACTED | forja_close_cycle.py:9 |
| forja_close_cycle.py | imports_from | forja_n3_common.py | EXTRACTED | forja_close_cycle.py:9 |
| forja_close_cycle.py | imports_from | forja_n3_common.py | EXTRACTED | forja_close_cycle.py:9 |
| forja_close_cycle.py | imports_from | forja_f10_contract.py | EXTRACTED | forja_close_cycle.py:10 |
| forja_close_cycle.py | imports_from | forja_f10_contract.py | EXTRACTED | forja_close_cycle.py:10 |
| forja_close_cycle.py | imports_from | forja_package.py | EXTRACTED | forja_close_cycle.py:11 |
| forja_close_cycle.py | imports_from | forja_package.py | EXTRACTED | forja_close_cycle.py:11 |
| forja_close_cycle.py | imports_from | forja_state_machine.py | EXTRACTED | forja_close_cycle.py:12 |
| forja_close_cycle.py | imports_from | forja_state_machine.py | EXTRACTED | forja_close_cycle.py:12 |
| forja_close_cycle.py | imports_from | forja_estilo_humano.py | EXTRACTED | forja_close_cycle.py:86 |
| forja_close_cycle.py | imports_from | forja_n4_validate.py | EXTRACTED | forja_close_cycle.py:189 |
| forja_close_cycle.py::_canonical_manifest | calls | forja_state_machine.py::derive_state | EXTRACTED | forja_close_cycle.py:16 |
| forja_close_cycle.py::_canonical_manifest | calls | forja_n3_common.py::read_json | EXTRACTED | forja_close_cycle.py:20 |
| forja_close_cycle.py::_canonical_manifest | calls | forja_package.py::revalidate_package_manifest | EXTRACTED | forja_close_cycle.py:30 |
| forja_close_cycle.py::_canonical_manifest | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_close_cycle.py:18 |
| forja_close_cycle.py::_canonical_manifest | calls | forja_n3_common.py::read_json | EXTRACTED | forja_close_cycle.py:22 |
| forja_close_cycle.py::_canonical_manifest | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_close_cycle.py:24 |
| forja_close_cycle.py::_canonical_manifest | calls | forja_n3_common.py::canonical_hash | EXTRACTED | forja_close_cycle.py:28 |
| forja_close_cycle.py::_canonical_manifest | calls | forja_n3_common.py::canonical_hash | EXTRACTED | forja_close_cycle.py:28 |
| forja_close_cycle.py::_canonical_manifest | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_close_cycle.py:29 |
| forja_close_cycle.py::_canonical_manifest | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_close_cycle.py:37 |
| forja_close_cycle.py::_canonical_manifest | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_close_cycle.py:27 |
| forja_close_cycle.py::create_package | calls | forja_state_machine.py::derive_state | EXTRACTED | forja_close_cycle.py:44 |
| forja_close_cycle.py::create_package | calls | forja_package.py::build_package | EXTRACTED | forja_close_cycle.py:49 |
| forja_close_cycle.py::create_package | calls | forja_state_machine.py::record_event | EXTRACTED | forja_close_cycle.py:51 |
| forja_close_cycle.py::create_package | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_close_cycle.py:66 |
| forja_close_cycle.py::create_package | calls | forja_state_machine.py::record_event | EXTRACTED | forja_close_cycle.py:67 |
| forja_close_cycle.py::create_package | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_close_cycle.py:46 |
| forja_close_cycle.py::create_package | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_close_cycle.py:48 |
| forja_close_cycle.py::register_draft | calls | forja_close_cycle.py::_canonical_manifest | EXTRACTED | forja_close_cycle.py:81 |
| forja_close_cycle.py::register_draft | calls | forja_n3_common.py::read_json | EXTRACTED | forja_close_cycle.py:96 |
| forja_close_cycle.py::register_draft | calls | forja_state_machine.py::record_event | EXTRACTED | forja_close_cycle.py:113 |
| forja_close_cycle.py::register_draft | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_close_cycle.py:85 |
| forja_close_cycle.py::register_draft | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_close_cycle.py:95 |
| forja_close_cycle.py::register_draft | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_close_cycle.py:98 |
| forja_close_cycle.py::register_draft | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_close_cycle.py:100 |
| forja_close_cycle.py::register_draft | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_close_cycle.py:102 |
| forja_close_cycle.py::register_draft | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_close_cycle.py:112 |
| forja_close_cycle.py::register_draft | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_close_cycle.py:84 |
| forja_close_cycle.py::register_draft | calls | forja_estilo_humano.py::analisar | EXTRACTED | forja_close_cycle.py:88 |
| forja_close_cycle.py::confirm_delivery | calls | forja_close_cycle.py::_canonical_manifest | EXTRACTED | forja_close_cycle.py:132 |
| forja_close_cycle.py::confirm_delivery | calls | forja_n3_common.py::read_json | EXTRACTED | forja_close_cycle.py:133 |
| forja_close_cycle.py::confirm_delivery | calls | forja_state_machine.py::record_event | EXTRACTED | forja_close_cycle.py:160 |
| forja_close_cycle.py::confirm_delivery | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_close_cycle.py:135 |
| forja_close_cycle.py::confirm_delivery | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_close_cycle.py:137 |
| forja_close_cycle.py::confirm_delivery | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_close_cycle.py:140 |
| forja_close_cycle.py::confirm_delivery | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_close_cycle.py:142 |
| forja_close_cycle.py::confirm_delivery | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_close_cycle.py:144 |
| forja_close_cycle.py::confirm_delivery | calls | forja_state_machine.py::record_event | EXTRACTED | forja_close_cycle.py:151 |
| forja_close_cycle.py::confirm_delivery | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_close_cycle.py:147 |
| forja_close_cycle.py::confirm_delivery | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_close_cycle.py:148 |
| forja_close_cycle.py::confirm_delivery | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_close_cycle.py:149 |
| forja_close_cycle.py::confirm_delivery | calls | forja_n3_common.py::canonical_hash | EXTRACTED | forja_close_cycle.py:164 |
| forja_close_cycle.py::fulfill | calls | forja_close_cycle.py::_canonical_manifest | EXTRACTED | forja_close_cycle.py:172 |
| forja_close_cycle.py::fulfill | calls | forja_f10_contract.py::compute_f10_gates | EXTRACTED | forja_close_cycle.py:175 |
| forja_close_cycle.py::fulfill | calls | forja_f10_contract.py::validate_f10_gates | EXTRACTED | forja_close_cycle.py:181 |
| forja_close_cycle.py::fulfill | calls | forja_n4_validate.py::validate_case | EXTRACTED | forja_close_cycle.py:191 |
| forja_close_cycle.py::fulfill | calls | forja_state_machine.py::record_event | EXTRACTED | forja_close_cycle.py:203 |
| forja_close_cycle.py::fulfill | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_close_cycle.py:174 |
| forja_close_cycle.py::fulfill | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_close_cycle.py:183 |
| forja_close_cycle.py::fulfill | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_close_cycle.py:193 |
| forja_close_cycle.py::fulfill | calls | forja_state_machine.py::record_event | EXTRACTED | forja_close_cycle.py:195 |
| forja_close_cycle.py::fulfill | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_close_cycle.py:188 |
| forja_close_cycle.py::fulfill | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_close_cycle.py:187 |
| forja_close_cycle.py::main | calls | forja_n3_common.py::resolve_case_dir | EXTRACTED | forja_close_cycle.py:230 |
| forja_close_cycle.py::main | calls | forja_close_cycle.py::create_package | EXTRACTED | forja_close_cycle.py:232 |
| forja_close_cycle.py::main | calls | forja_close_cycle.py::register_draft | EXTRACTED | forja_close_cycle.py:234 |
| forja_close_cycle.py::main | calls | forja_close_cycle.py::confirm_delivery | EXTRACTED | forja_close_cycle.py:236 |
| forja_close_cycle.py::main | calls | forja_close_cycle.py::fulfill | EXTRACTED | forja_close_cycle.py:238 |
| forja_conselho.py::_achados_parecer | calls | forja_conselho.py::_ler | EXTRACTED | forja_conselho.py:64 |
| forja_conselho.py::_achados_decisoes | calls | forja_conselho.py::_ler | EXTRACTED | forja_conselho.py:191 |
| forja_conselho.py::_achados_decisoes | calls | forja_conselho.py::_achados_decisoes_json | EXTRACTED | forja_conselho.py:198 |
| forja_conselho.py::_achados_decisoes | calls | forja_conselho.py::_linhas_de_decisao | EXTRACTED | forja_conselho.py:201 |
| forja_conselho.py::validar_conselho | calls | forja_conselho.py::_achados_parecer | EXTRACTED | forja_conselho.py:232 |
| forja_conselho.py::validar_conselho | calls | forja_conselho.py::_achados_parecer | EXTRACTED | forja_conselho.py:233 |
| forja_conselho.py::validar_conselho | calls | forja_conselho.py::_achados_decisoes | EXTRACTED | forja_conselho.py:234 |
| forja_conselho.py::main | calls | forja_conselho.py::validar_conselho | EXTRACTED | forja_conselho.py:256 |
| forja_consistency.py | imports_from | forja_n3_common.py | EXTRACTED | forja_consistency.py:13 |
| forja_consistency.py | imports_from | forja_n3_common.py | EXTRACTED | forja_consistency.py:13 |
| forja_consistency.py | imports_from | forja_n4_common.py | EXTRACTED | forja_consistency.py:14 |
| forja_consistency.py | imports_from | forja_n4_common.py | EXTRACTED | forja_consistency.py:14 |
| forja_consistency.py | imports_from | forja_n4_common.py | EXTRACTED | forja_consistency.py:14 |
| forja_consistency.py::inspect_physical_document | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_consistency.py:34 |
| forja_consistency.py::inspect_physical_document | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_consistency.py:35 |
| forja_consistency.py::validate_event_identity | calls | forja_n4_common.py::ids_unique | EXTRACTED | forja_consistency.py:82 |
| forja_consistency.py::validate_event_identity | calls | forja_n4_common.py::issue | EXTRACTED | forja_consistency.py:86 |
| forja_consistency.py::validate_event_identity | calls | forja_n4_common.py::issue | EXTRACTED | forja_consistency.py:89 |
| forja_consistency.py::validate_event_identity | calls | forja_n4_common.py::issue | EXTRACTED | forja_consistency.py:95 |
| forja_consistency.py::validate_comparison | calls | forja_n4_common.py::ids_unique | EXTRACTED | forja_consistency.py:100 |
| forja_consistency.py::validate_comparison | calls | forja_n4_common.py::ids_unique | EXTRACTED | forja_consistency.py:104 |
| forja_consistency.py::validate_comparison | calls | forja_n4_common.py::issue | EXTRACTED | forja_consistency.py:103 |
| forja_consistency.py::validate_comparison | calls | forja_n4_common.py::issue | EXTRACTED | forja_consistency.py:108 |
| forja_consistency.py::validate_comparison | calls | forja_n4_common.py::issue | EXTRACTED | forja_consistency.py:110 |
| forja_consistency.py::validate_comparison | calls | forja_n4_common.py::issue | EXTRACTED | forja_consistency.py:112 |
| forja_consistency.py::validate_intertemporal | calls | forja_n4_common.py::ids_unique | EXTRACTED | forja_consistency.py:118 |
| forja_consistency.py::validate_intertemporal | calls | forja_n4_common.py::issue | EXTRACTED | forja_consistency.py:122 |
| forja_consistency.py::validate_intertemporal | calls | forja_n4_common.py::issue | EXTRACTED | forja_consistency.py:124 |
| forja_consistency.py::validate_intertemporal | calls | forja_n4_common.py::issue | EXTRACTED | forja_consistency.py:126 |
| forja_consistency.py::validate_quantification | calls | forja_n4_common.py::ids_unique | EXTRACTED | forja_consistency.py:148 |
| forja_consistency.py::validate_quantification | calls | forja_n4_common.py::issue | EXTRACTED | forja_consistency.py:158 |
| forja_consistency.py::validate_quantification | calls | forja_n4_common.py::issue | EXTRACTED | forja_consistency.py:154 |
| forja_consistency.py::validate_quantification | calls | forja_consistency.py::_eval_formula | EXTRACTED | forja_consistency.py:177 |
| forja_consistency.py::validate_quantification | calls | forja_n4_common.py::issue | EXTRACTED | forja_consistency.py:181 |
| forja_consistency.py::validate_quantification | calls | forja_consistency.py::_eval_formula | EXTRACTED | forja_consistency.py:171 |
| forja_consistency.py::validate_quantification | calls | forja_consistency.py::_eval_formula | EXTRACTED | forja_consistency.py:171 |
| forja_consistency.py::validate_quantification | calls | forja_n4_common.py::issue | EXTRACTED | forja_consistency.py:175 |
| forja_consistency.py::validate_quantification | calls | forja_n4_common.py::issue | EXTRACTED | forja_consistency.py:179 |
| forja_consistency.py::validate_delivery | calls | forja_n4_common.py::issue | EXTRACTED | forja_consistency.py:188 |
| forja_consistency.py::validate_delivery | calls | forja_n4_common.py::issue | EXTRACTED | forja_consistency.py:191 |
| forja_consistency.py::validate_delivery | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_consistency.py:190 |
| forja_consistency.py::validate_delivery | calls | forja_n4_common.py::issue | EXTRACTED | forja_consistency.py:197 |
| forja_consistency.py::validate_delivery | calls | forja_n4_common.py::issue | EXTRACTED | forja_consistency.py:202 |
| forja_consistency.py::validate_delivery | calls | forja_n4_common.py::issue | EXTRACTED | forja_consistency.py:200 |
| forja_consistency.py::validate_global | calls | forja_n4_common.py::issue | EXTRACTED | forja_consistency.py:210 |
| forja_consistency.py::validate_global | calls | forja_n4_common.py::issue | EXTRACTED | forja_consistency.py:215 |
| forja_consistency.py::validate_global | calls | forja_n4_common.py::issue | EXTRACTED | forja_consistency.py:229 |
| forja_consistency.py::validate_global | calls | forja_n4_common.py::issue | EXTRACTED | forja_consistency.py:220 |
| forja_consistency.py::validate_global | calls | forja_n4_common.py::issue | EXTRACTED | forja_consistency.py:222 |
| forja_consistency.py::validate_global | calls | forja_n4_common.py::issue | EXTRACTED | forja_consistency.py:224 |
| forja_consistency.py::validate_case | calls | forja_n4_common.py::validate_file | EXTRACTED | forja_consistency.py:247 |
| forja_consistency.py::main | calls | forja_consistency.py::validate_case | EXTRACTED | forja_consistency.py:256 |
| forja_consistency.py::main | calls | forja_n3_common.py::resolve_case_dir | EXTRACTED | forja_consistency.py:256 |
| forja_context.py | imports_from | forja_n3_common.py | EXTRACTED | forja_context.py:11 |
| forja_context.py | imports_from | forja_n3_common.py | EXTRACTED | forja_context.py:11 |
| forja_context.py | imports_from | forja_n3_common.py | EXTRACTED | forja_context.py:11 |
| forja_context.py | imports_from | forja_n3_common.py | EXTRACTED | forja_context.py:11 |
| forja_context.py | imports_from | forja_n3_common.py | EXTRACTED | forja_context.py:11 |
| forja_context.py::markdown_blocks | calls | forja_context.py::_norm | EXTRACTED | forja_context.py:84 |
| forja_context.py::markdown_blocks | calls | forja_n3_common.py::canonical_hash | EXTRACTED | forja_context.py:92 |
| forja_context.py::markdown_blocks | calls | forja_n3_common.py::canonical_hash | EXTRACTED | forja_context.py:85 |
| forja_context.py::validate_coverage | calls | forja_context.py::_covered_pages | EXTRACTED | forja_context.py:154 |
| forja_context.py::validate_paragraph_provenance | calls | forja_context.py::markdown_blocks | EXTRACTED | forja_context.py:200 |
| forja_context.py::validate_paragraph_provenance | calls | forja_context.py::_norm | EXTRACTED | forja_context.py:206 |
| forja_context.py::validate_context | calls | forja_n3_common.py::read_json | EXTRACTED | forja_context.py:257 |
| forja_context.py::validate_context | calls | forja_n3_common.py::read_json | EXTRACTED | forja_context.py:258 |
| forja_context.py::validate_context | calls | forja_n3_common.py::read_json | EXTRACTED | forja_context.py:259 |
| forja_context.py::validate_context | calls | forja_n3_common.py::read_json | EXTRACTED | forja_context.py:260 |
| forja_context.py::validate_context | calls | forja_n3_common.py::read_json | EXTRACTED | forja_context.py:261 |
| forja_context.py::validate_context | calls | forja_context.py::validate_document_index | EXTRACTED | forja_context.py:265 |
| forja_context.py::validate_context | calls | forja_context.py::validate_coverage | EXTRACTED | forja_context.py:266 |
| forja_context.py::validate_context | calls | forja_context.py::validate_fact_ledger | EXTRACTED | forja_context.py:268 |
| forja_context.py::validate_context | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_context.py:290 |
| forja_context.py::validate_context | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_context.py:255 |
| forja_context.py::validate_context | calls | forja_context.py::validate_paragraph_provenance | EXTRACTED | forja_context.py:271 |
| forja_context.py::validate_context | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_context.py:285 |
| forja_context.py::validate_context | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_context.py:288 |
| forja_context.py::validate_context | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_context.py:249 |
| forja_context.py::main | calls | forja_context.py::validate_context | EXTRACTED | forja_context.py:298 |
| forja_contexto.py | imports_from | forja_artefatos.py | EXTRACTED | forja_contexto.py:30 |
| forja_contexto.py::validar_contexto | calls | forja_contexto.py::_declarado_bool | EXTRACTED | forja_contexto.py:117 |
| forja_contexto.py::validar_contexto | calls | forja_contexto.py::_pendencias | EXTRACTED | forja_contexto.py:170 |
| forja_contexto.py::validar_contexto | calls | forja_contexto.py::_liberacao_externa | EXTRACTED | forja_contexto.py:171 |
| forja_contexto.py::validar_contexto | calls | forja_contexto.py::_hashes_do_texto | EXTRACTED | forja_contexto.py:143 |
| forja_delivery.py | imports_from | forja_adversarial_audit.py | EXTRACTED | forja_delivery.py:19 |
| forja_delivery.py | imports_from | forja_adversarial_audit.py | EXTRACTED | forja_delivery.py:19 |
| forja_delivery.py | imports_from | forja_memoria_auditabilidade.py | EXTRACTED | forja_delivery.py:20 |
| forja_delivery.py | imports_from | forja_memoria_auditabilidade.py | EXTRACTED | forja_delivery.py:20 |
| forja_delivery.py | imports_from | forja_n3_common.py | EXTRACTED | forja_delivery.py:21 |
| forja_delivery.py | imports_from | forja_n3_common.py | EXTRACTED | forja_delivery.py:21 |
| forja_delivery.py | imports_from | forja_metricas_f7.py | EXTRACTED | forja_delivery.py:85 |
| forja_delivery.py | imports_from | forja_verificador.py | EXTRACTED | forja_delivery.py:86 |
| forja_delivery.py | imports_from | forja_lastro.py | EXTRACTED | forja_delivery.py:329 |
| forja_delivery.py | imports_from | forja_lastro.py | EXTRACTED | forja_delivery.py:329 |
| forja_delivery.py | imports_from | forja_lastro.py | EXTRACTED | forja_delivery.py:329 |
| forja_delivery.py | imports_from | forja_package.py | EXTRACTED | forja_delivery.py:416 |
| forja_delivery.py | imports_from | forja_alertas.py | EXTRACTED | forja_delivery.py:520 |
| forja_delivery.py::ref_ok | calls | forja_delivery.py::ref_ok | EXTRACTED | forja_delivery.py:44 |
| forja_delivery.py::f7_com_lastro | calls | forja_metricas_f7.py::metricas_f7 | EXTRACTED | forja_delivery.py:92 |
| forja_delivery.py::f7_com_lastro | calls | forja_verificador.py::verificar | EXTRACTED | forja_delivery.py:89 |
| forja_delivery.py::parecer_antes_da_redacao | calls | forja_delivery.py::_parse_iso | EXTRACTED | forja_delivery.py:167 |
| forja_delivery.py::visual_com_lastro | calls | forja_n3_common.py::read_json | EXTRACTED | forja_delivery.py:199 |
| forja_delivery.py::main | calls | forja_n3_common.py::read_json | EXTRACTED | forja_delivery.py:240 |
| forja_delivery.py::main | calls | forja_delivery.py::f3_com_regimento | EXTRACTED | forja_delivery.py:251 |
| forja_delivery.py::main | calls | forja_delivery.py::f5_checklist_ok | EXTRACTED | forja_delivery.py:255 |
| forja_delivery.py::main | calls | forja_delivery.py::visual_com_lastro | EXTRACTED | forja_delivery.py:268 |
| forja_delivery.py::main | calls | forja_delivery.py::achar | EXTRACTED | forja_delivery.py:388 |
| forja_delivery.py::main | calls | forja_delivery.py::achar | EXTRACTED | forja_delivery.py:397 |
| forja_delivery.py::main | calls | forja_memoria_auditabilidade.py::build_bundle | EXTRACTED | forja_delivery.py:446 |
| forja_delivery.py::main | calls | forja_memoria_auditabilidade.py::validate_bundle | EXTRACTED | forja_delivery.py:447 |
| forja_delivery.py::main | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_delivery.py:492 |
| forja_delivery.py::main | calls | forja_delivery.py::append_unique | EXTRACTED | forja_delivery.py:501 |
| forja_delivery.py::main | calls | forja_memoria_auditabilidade.py::build_bundle | EXTRACTED | forja_delivery.py:506 |
| forja_delivery.py::main | calls | forja_memoria_auditabilidade.py::validate_bundle | EXTRACTED | forja_delivery.py:507 |
| forja_delivery.py::main | calls | forja_n3_common.py::read_json | EXTRACTED | forja_delivery.py:238 |
| forja_delivery.py::main | calls | forja_delivery.py::ref_ok | EXTRACTED | forja_delivery.py:245 |
| forja_delivery.py::main | calls | forja_delivery.py::achar | EXTRACTED | forja_delivery.py:249 |
| forja_delivery.py::main | calls | forja_delivery.py::achar | EXTRACTED | forja_delivery.py:262 |
| forja_delivery.py::main | calls | forja_delivery.py::achar | EXTRACTED | forja_delivery.py:265 |
| forja_delivery.py::main | calls | forja_delivery.py::achar | EXTRACTED | forja_delivery.py:266 |
| forja_delivery.py::main | calls | forja_delivery.py::achar | EXTRACTED | forja_delivery.py:267 |
| forja_delivery.py::main | calls | forja_delivery.py::achar | EXTRACTED | forja_delivery.py:272 |
| forja_delivery.py::main | calls | forja_n3_common.py::read_json | EXTRACTED | forja_delivery.py:306 |
| forja_delivery.py::main | calls | forja_delivery.py::f7_com_lastro | EXTRACTED | forja_delivery.py:307 |
| forja_delivery.py::main | calls | forja_n3_common.py::read_json | EXTRACTED | forja_delivery.py:330 |
| forja_delivery.py::main | calls | forja_lastro.py::fatos_sem_lastro | EXTRACTED | forja_delivery.py:331 |
| forja_delivery.py::main | calls | forja_delivery.py::parecer_valido | EXTRACTED | forja_delivery.py:381 |
| forja_delivery.py::main | calls | forja_delivery.py::parecer_antes_da_redacao | EXTRACTED | forja_delivery.py:383 |
| forja_delivery.py::main | calls | forja_adversarial_audit.py::response_product_required | EXTRACTED | forja_delivery.py:396 |
| forja_delivery.py::main | calls | forja_delivery.py::achar | EXTRACTED | forja_delivery.py:399 |
| forja_delivery.py::main | calls | forja_adversarial_audit.py::validate_adversarial_audit | EXTRACTED | forja_delivery.py:404 |
| forja_delivery.py::main | calls | forja_delivery.py::ref_text | EXTRACTED | forja_delivery.py:270 |
| forja_delivery.py::main | calls | forja_lastro.py::material_economico | EXTRACTED | forja_delivery.py:349 |
| forja_delivery.py::main | calls | forja_delivery.py::achar | EXTRACTED | forja_delivery.py:378 |
| forja_delivery.py::main | calls | forja_delivery.py::achar | EXTRACTED | forja_delivery.py:379 |
| forja_delivery.py::main | calls | forja_package.py::revalidate_package_manifest | EXTRACTED | forja_delivery.py:418 |
| forja_delivery.py::main | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_delivery.py:497 |
| forja_delivery.py::main | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_delivery.py:500 |
| forja_delivery.py::main | calls | forja_delivery.py::ref_text | EXTRACTED | forja_delivery.py:247 |
| forja_delivery.py::main | calls | forja_lastro.py::validar_gates_economicos | EXTRACTED | forja_delivery.py:356 |
| forja_delivery.py::main | calls | forja_delivery.py::ref_text | EXTRACTED | forja_delivery.py:385 |
| forja_delivery.py::main | calls | forja_n3_common.py::read_json | EXTRACTED | forja_delivery.py:404 |
| forja_delivery.py::main | calls | forja_delivery.py::ref_text | EXTRACTED | forja_delivery.py:408 |
| forja_delivery.py::main | calls | forja_n3_common.py::read_json | EXTRACTED | forja_delivery.py:420 |
| forja_delivery.py::main | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_delivery.py:478 |
| forja_delivery.py::main | calls | forja_alertas.py::notificar_p0 | EXTRACTED | forja_delivery.py:523 |
| forja_delivery.py::main | calls | forja_n3_common.py::read_json | EXTRACTED | forja_delivery.py:352 |
| forja_delivery_integrity.py | imports_from | forja_consistency.py | EXTRACTED | forja_delivery_integrity.py:9 |
| forja_delivery_integrity.py | imports_from | forja_n3_common.py | EXTRACTED | forja_delivery_integrity.py:10 |
| forja_delivery_integrity.py | imports_from | forja_n3_common.py | EXTRACTED | forja_delivery_integrity.py:10 |
| forja_delivery_integrity.py | imports_from | forja_n3_common.py | EXTRACTED | forja_delivery_integrity.py:10 |
| forja_delivery_integrity.py | imports_from | forja_n3_common.py | EXTRACTED | forja_delivery_integrity.py:10 |
| forja_delivery_integrity.py | imports_from | forja_n3_common.py | EXTRACTED | forja_delivery_integrity.py:10 |
| forja_delivery_integrity.py | imports_from | forja_n3_common.py | EXTRACTED | forja_delivery_integrity.py:10 |
| forja_delivery_integrity.py | imports_from | forja_n4_common.py | EXTRACTED | forja_delivery_integrity.py:11 |
| forja_delivery_integrity.py | imports_from | forja_n4_common.py | EXTRACTED | forja_delivery_integrity.py:11 |
| forja_delivery_integrity.py | imports_from | forja_state_machine.py | EXTRACTED | forja_delivery_integrity.py:12 |
| forja_delivery_integrity.py | imports_from | forja_state_machine.py | EXTRACTED | forja_delivery_integrity.py:12 |
| forja_delivery_integrity.py::_attachment | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_delivery_integrity.py:23 |
| forja_delivery_integrity.py::_attachment | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_delivery_integrity.py:18 |
| forja_delivery_integrity.py::_attachment | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_delivery_integrity.py:22 |
| forja_delivery_integrity.py::_attachment | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_delivery_integrity.py:25 |
| forja_delivery_integrity.py::select | calls | forja_n3_common.py::read_json | EXTRACTED | forja_delivery_integrity.py:30 |
| forja_delivery_integrity.py::select | calls | forja_delivery_integrity.py::_attachment | EXTRACTED | forja_delivery_integrity.py:33 |
| forja_delivery_integrity.py::select | calls | forja_n4_common.py::build_envelope | EXTRACTED | forja_delivery_integrity.py:44 |
| forja_delivery_integrity.py::select | calls | forja_consistency.py::validate_delivery | EXTRACTED | forja_delivery_integrity.py:53 |
| forja_delivery_integrity.py::select | calls | forja_n4_common.py::write_artifact | EXTRACTED | forja_delivery_integrity.py:56 |
| forja_delivery_integrity.py::select | calls | forja_state_machine.py::derive_state | EXTRACTED | forja_delivery_integrity.py:57 |
| forja_delivery_integrity.py::select | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_delivery_integrity.py:32 |
| forja_delivery_integrity.py::select | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_delivery_integrity.py:55 |
| forja_delivery_integrity.py::select | calls | forja_state_machine.py::record_event | EXTRACTED | forja_delivery_integrity.py:59 |
| forja_delivery_integrity.py::confirm | calls | forja_n3_common.py::read_json | EXTRACTED | forja_delivery_integrity.py:80 |
| forja_delivery_integrity.py::confirm | calls | forja_n4_common.py::build_envelope | EXTRACTED | forja_delivery_integrity.py:100 |
| forja_delivery_integrity.py::confirm | calls | forja_consistency.py::validate_delivery | EXTRACTED | forja_delivery_integrity.py:109 |
| forja_delivery_integrity.py::confirm | calls | forja_n4_common.py::write_artifact | EXTRACTED | forja_delivery_integrity.py:112 |
| forja_delivery_integrity.py::confirm | calls | forja_state_machine.py::derive_state | EXTRACTED | forja_delivery_integrity.py:116 |
| forja_delivery_integrity.py::confirm | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_delivery_integrity.py:82 |
| forja_delivery_integrity.py::confirm | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_delivery_integrity.py:86 |
| forja_delivery_integrity.py::confirm | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_delivery_integrity.py:99 |
| forja_delivery_integrity.py::confirm | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_delivery_integrity.py:111 |
| forja_delivery_integrity.py::confirm | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_delivery_integrity.py:115 |
| forja_delivery_integrity.py::confirm | calls | forja_state_machine.py::record_event | EXTRACTED | forja_delivery_integrity.py:118 |
| forja_delivery_integrity.py::confirm | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_delivery_integrity.py:85 |
| forja_delivery_integrity.py::confirm | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_delivery_integrity.py:93 |
| forja_delivery_integrity.py::confirm | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_delivery_integrity.py:90 |
| forja_delivery_integrity.py::main | calls | forja_n3_common.py::resolve_case_dir | EXTRACTED | forja_delivery_integrity.py:146 |
| forja_delivery_integrity.py::main | calls | forja_delivery_integrity.py::select | EXTRACTED | forja_delivery_integrity.py:148 |
| forja_delivery_integrity.py::main | calls | forja_delivery_integrity.py::confirm | EXTRACTED | forja_delivery_integrity.py:150 |
| forja_diabob.py | imports_from | forja_modelos.py | EXTRACTED | forja_diabob.py:23 |
| forja_diabob.py::red_team | calls | forja_modelos.py::chamar | EXTRACTED | forja_diabob.py:66 |
| forja_diabob.py::red_team | calls | forja_modelos.py::ForjaModeloError | EXTRACTED | forja_diabob.py:65 |
| forja_diabob.py::main | calls | forja_diabob.py::red_team | EXTRACTED | forja_diabob.py:91 |
| forja_diff_docx.py::classificar_mudanca | calls | forja_diff_docx.py::similaridade_ratio | EXTRACTED | forja_diff_docx.py:65 |
| forja_diff_docx.py::gerar_diff_markdown | calls | forja_diff_docx.py::classificar_mudanca | EXTRACTED | forja_diff_docx.py:111 |
| forja_diff_docx.py::main | calls | forja_diff_docx.py::extrair_paragrafos_docx | EXTRACTED | forja_diff_docx.py:249 |
| forja_diff_docx.py::main | calls | forja_diff_docx.py::extrair_paragrafos_docx | EXTRACTED | forja_diff_docx.py:253 |
| forja_diff_docx.py::main | calls | forja_diff_docx.py::gerar_diff_markdown | EXTRACTED | forja_diff_docx.py:257 |
| forja_document_compare.py | imports_from | forja_n3_common.py | EXTRACTED | forja_document_compare.py:20 |
| forja_document_compare.py | imports_from | forja_n3_common.py | EXTRACTED | forja_document_compare.py:20 |
| forja_document_compare.py | imports_from | forja_n3_common.py | EXTRACTED | forja_document_compare.py:20 |
| forja_document_compare.py | imports_from | forja_n3_common.py | EXTRACTED | forja_document_compare.py:20 |
| forja_document_compare.py | imports_from | forja_n3_common.py | EXTRACTED | forja_document_compare.py:20 |
| forja_document_compare.py | imports_from | forja_post_protocol_contracts.py | EXTRACTED | forja_document_compare.py:21 |
| forja_document_compare.py | imports_from | forja_post_protocol_contracts.py | EXTRACTED | forja_document_compare.py:21 |
| forja_document_compare.py | imports_from | forja_post_protocol_contracts.py | EXTRACTED | forja_document_compare.py:21 |
| forja_document_compare.py::comparable_units | calls | forja_document_compare.py::_normalized_text | EXTRACTED | forja_document_compare.py:84 |
| forja_document_compare.py::comparable_units | calls | forja_document_compare.py::_is_protocol_noise | EXTRACTED | forja_document_compare.py:87 |
| forja_document_compare.py::comparable_units | calls | forja_document_compare.py::Unit | EXTRACTED | forja_document_compare.py:91 |
| forja_document_compare.py::_paragraph_text | calls | forja_document_compare.py::_normalized_text | EXTRACTED | forja_document_compare.py:117 |
| forja_document_compare.py::_docx_part_units | calls | forja_document_compare.py::_paragraph_text | EXTRACTED | forja_document_compare.py:129 |
| forja_document_compare.py::_docx_part_units | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_document_compare.py:124 |
| forja_document_compare.py::_docx_part_units | calls | forja_document_compare.py::Unit | EXTRACTED | forja_document_compare.py:133 |
| forja_document_compare.py::extract_docx | calls | forja_document_compare.py::Extracted | EXTRACTED | forja_document_compare.py:181 |
| forja_document_compare.py::extract_docx | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_document_compare.py:181 |
| forja_document_compare.py::extract_docx | calls | forja_document_compare.py::_docx_part_units | EXTRACTED | forja_document_compare.py:158 |
| forja_document_compare.py::extract_pdf | calls | forja_document_compare.py::Extracted | EXTRACTED | forja_document_compare.py:242 |
| forja_document_compare.py::extract_pdf | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_document_compare.py:244 |
| forja_document_compare.py::extract_pdf | calls | forja_document_compare.py::_normalized_text | EXTRACTED | forja_document_compare.py:197 |
| forja_document_compare.py::extract_pdf | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_document_compare.py:238 |
| forja_document_compare.py::extract_pdf | calls | forja_document_compare.py::Unit | EXTRACTED | forja_document_compare.py:199 |
| forja_document_compare.py::extract_pdf | calls | forja_document_compare.py::_normalized_text | EXTRACTED | forja_document_compare.py:232 |
| forja_document_compare.py::extract_pdf | calls | forja_document_compare.py::Unit | EXTRACTED | forja_document_compare.py:217 |
| forja_document_compare.py::extract_pdf | calls | forja_document_compare.py::Unit | EXTRACTED | forja_document_compare.py:234 |
| forja_document_compare.py::extract_document | calls | forja_document_compare.py::Extracted | EXTRACTED | forja_document_compare.py:269 |
| forja_document_compare.py::extract_document | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_document_compare.py:256 |
| forja_document_compare.py::extract_document | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_document_compare.py:259 |
| forja_document_compare.py::extract_document | calls | forja_document_compare.py::extract_docx | EXTRACTED | forja_document_compare.py:261 |
| forja_document_compare.py::extract_document | calls | forja_document_compare.py::extract_pdf | EXTRACTED | forja_document_compare.py:263 |
| forja_document_compare.py::extract_document | calls | forja_document_compare.py::Unit | EXTRACTED | forja_document_compare.py:265 |
| forja_document_compare.py::extract_document | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_document_compare.py:269 |
| forja_document_compare.py::extract_document | calls | forja_document_compare.py::_normalized_text | EXTRACTED | forja_document_compare.py:265 |
| forja_document_compare.py::extract_document | calls | forja_document_compare.py::_normalized_text | EXTRACTED | forja_document_compare.py:267 |
| forja_document_compare.py::compare_documents | calls | forja_document_compare.py::extract_document | EXTRACTED | forja_document_compare.py:363 |
| forja_document_compare.py::compare_documents | calls | forja_document_compare.py::extract_document | EXTRACTED | forja_document_compare.py:364 |
| forja_document_compare.py::compare_documents | calls | forja_document_compare.py::comparable_units | EXTRACTED | forja_document_compare.py:366 |
| forja_document_compare.py::compare_documents | calls | forja_document_compare.py::comparable_units | EXTRACTED | forja_document_compare.py:367 |
| forja_document_compare.py::compare_documents | calls | forja_document_compare.py::_tokens_with_locators | EXTRACTED | forja_document_compare.py:368 |
| forja_document_compare.py::compare_documents | calls | forja_document_compare.py::_tokens_with_locators | EXTRACTED | forja_document_compare.py:369 |
| forja_document_compare.py::compare_documents | calls | forja_n3_common.py::canonical_hash | EXTRACTED | forja_document_compare.py:503 |
| forja_document_compare.py::compare_documents | calls | forja_document_compare.py::_change_regions | EXTRACTED | forja_document_compare.py:383 |
| forja_document_compare.py::compare_documents | calls | forja_n3_common.py::canonical_hash | EXTRACTED | forja_document_compare.py:429 |
| forja_document_compare.py::compare_documents | calls | forja_document_compare.py::classify_change | EXTRACTED | forja_document_compare.py:392 |
| forja_document_compare.py::compare_documents | calls | forja_n3_common.py::canonical_hash | EXTRACTED | forja_document_compare.py:393 |
| forja_document_compare.py::compare_documents | calls | forja_n3_common.py::canonical_hash | EXTRACTED | forja_document_compare.py:401 |
| forja_document_compare.py::compare_documents | calls | forja_document_compare.py::_unique_ordered | EXTRACTED | forja_document_compare.py:397 |
| forja_document_compare.py::compare_documents | calls | forja_document_compare.py::_unique_ordered | EXTRACTED | forja_document_compare.py:398 |
| forja_document_compare.py::compare_documents | calls | forja_document_compare.py::_unique_ordered | EXTRACTED | forja_document_compare.py:412 |
| forja_document_compare.py::compare_documents | calls | forja_document_compare.py::_unique_ordered | EXTRACTED | forja_document_compare.py:413 |
| forja_document_compare.py::render_markdown | calls | forja_document_compare.py::_normalized_text | EXTRACTED | forja_document_compare.py:538 |
| forja_document_compare.py::render_markdown | calls | forja_document_compare.py::_normalized_text | EXTRACTED | forja_document_compare.py:539 |
| forja_document_compare.py::write_comparison | calls | forja_document_compare.py::compare_documents | EXTRACTED | forja_document_compare.py:586 |
| forja_document_compare.py::write_comparison | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_document_compare.py:587 |
| forja_document_compare.py::write_comparison | calls | forja_n3_common.py::atomic_write_text | EXTRACTED | forja_document_compare.py:588 |
| forja_document_compare.py::write_comparison | calls | forja_document_compare.py::render_markdown | EXTRACTED | forja_document_compare.py:590 |
| forja_document_compare.py::main | calls | forja_document_compare.py::write_comparison | EXTRACTED | forja_document_compare.py:611 |
| forja_docx_layout.py | imports_from | forja_n3_common.py | EXTRACTED | forja_docx_layout.py:35 |
| forja_docx_layout.py | imports_from | forja_n3_common.py | EXTRACTED | forja_docx_layout.py:35 |
| forja_docx_layout.py | imports_from | forja_n3_common.py | EXTRACTED | forja_docx_layout.py:35 |
| forja_docx_layout.py::docx_content_signature | calls | forja_docx_layout.py::_text_sha256 | EXTRACTED | forja_docx_layout.py:205 |
| forja_docx_layout.py::docx_content_signature | calls | forja_docx_layout.py::_text_sha256 | EXTRACTED | forja_docx_layout.py:211 |
| forja_docx_layout.py::docx_content_signature | calls | forja_docx_layout.py::_text_sha256 | EXTRACTED | forja_docx_layout.py:213 |
| forja_docx_layout.py::docx_content_signature | calls | forja_docx_layout.py::_text_sha256 | EXTRACTED | forja_docx_layout.py:181 |
| forja_docx_layout.py::docx_content_signature | calls | forja_docx_layout.py::_text_sha256 | EXTRACTED | forja_docx_layout.py:185 |
| forja_docx_layout.py::docx_content_signature | calls | forja_docx_layout.py::_text_sha256 | EXTRACTED | forja_docx_layout.py:187 |
| forja_docx_layout.py::compare_docx_content | calls | forja_docx_layout.py::docx_content_signature | EXTRACTED | forja_docx_layout.py:220 |
| forja_docx_layout.py::compare_docx_content | calls | forja_docx_layout.py::docx_content_signature | EXTRACTED | forja_docx_layout.py:221 |
| forja_docx_layout.py::compare_docx_content | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_docx_layout.py:232 |
| forja_docx_layout.py::compare_docx_content | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_docx_layout.py:233 |
| forja_docx_layout.py::_folios_com_margem | calls | forja_docx_layout.py::_right_margin_pt | EXTRACTED | forja_docx_layout.py:306 |
| forja_docx_layout.py::_folio_rectangles | calls | forja_docx_layout.py::_unique_header_parts | EXTRACTED | forja_docx_layout.py:341 |
| forja_docx_layout.py::_effective_alignment | calls | forja_docx_layout.py::_style_chain | EXTRACTED | forja_docx_layout.py:383 |
| forja_docx_layout.py::_style_font_size | calls | forja_docx_layout.py::_style_chain | EXTRACTED | forja_docx_layout.py:418 |
| forja_docx_layout.py::_style_font_size | calls | forja_docx_layout.py::_font_from_rpr | EXTRACTED | forja_docx_layout.py:420 |
| forja_docx_layout.py::_style_font_size | calls | forja_docx_layout.py::_size_from_rpr | EXTRACTED | forja_docx_layout.py:422 |
| forja_docx_layout.py::_effective_run_font_size | calls | forja_docx_layout.py::_font_from_rpr | EXTRACTED | forja_docx_layout.py:430 |
| forja_docx_layout.py::_effective_run_font_size | calls | forja_docx_layout.py::_size_from_rpr | EXTRACTED | forja_docx_layout.py:431 |
| forja_docx_layout.py::_effective_run_font_size | calls | forja_docx_layout.py::_style_font_size | EXTRACTED | forja_docx_layout.py:432 |
| forja_docx_layout.py::_is_heading | calls | forja_docx_layout.py::_norm | EXTRACTED | forja_docx_layout.py:458 |
| forja_docx_layout.py::_role_for | calls | forja_docx_layout.py::_norm | EXTRACTED | forja_docx_layout.py:534 |
| forja_docx_layout.py::_role_for | calls | forja_docx_layout.py::_has_visual_container | EXTRACTED | forja_docx_layout.py:555 |
| forja_docx_layout.py::_role_for | calls | forja_docx_layout.py::_is_heading | EXTRACTED | forja_docx_layout.py:561 |
| forja_docx_layout.py::_role_for | calls | forja_docx_layout.py::_is_caption | EXTRACTED | forja_docx_layout.py:563 |
| forja_docx_layout.py::_role_for | calls | forja_docx_layout.py::_is_signature | EXTRACTED | forja_docx_layout.py:565 |
| forja_docx_layout.py::_role_for | calls | forja_docx_layout.py::_has_visual_container | EXTRACTED | forja_docx_layout.py:579 |
| forja_docx_layout.py::_role_for | calls | forja_docx_layout.py::_is_heading | EXTRACTED | forja_docx_layout.py:539 |
| forja_docx_layout.py::_role_for | calls | forja_docx_layout.py::_e_titulo_centralizado | EXTRACTED | forja_docx_layout.py:577 |
| forja_docx_layout.py::_role_for | calls | forja_docx_layout.py::_is_heading | EXTRACTED | forja_docx_layout.py:543 |
| forja_docx_layout.py::audit_docx_layout | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_docx_layout.py:624 |
| forja_docx_layout.py::audit_docx_layout | calls | forja_docx_layout.py::_load_exceptions | EXTRACTED | forja_docx_layout.py:625 |
| forja_docx_layout.py::audit_docx_layout | calls | forja_docx_layout.py::_paragraph_text | EXTRACTED | forja_docx_layout.py:647 |
| forja_docx_layout.py::audit_docx_layout | calls | forja_docx_layout.py::_role_for | EXTRACTED | forja_docx_layout.py:650 |
| forja_docx_layout.py::audit_docx_layout | calls | forja_docx_layout.py::_effective_alignment | EXTRACTED | forja_docx_layout.py:657 |
| forja_docx_layout.py::audit_docx_layout | calls | forja_docx_layout.py::_folios_com_margem | EXTRACTED | forja_docx_layout.py:778 |
| forja_docx_layout.py::audit_docx_layout | calls | forja_docx_layout.py::_vml_width_pt | EXTRACTED | forja_docx_layout.py:782 |
| forja_docx_layout.py::audit_docx_layout | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_docx_layout.py:815 |
| forja_docx_layout.py::audit_docx_layout | calls | forja_docx_layout.py::_substantial_run_text | EXTRACTED | forja_docx_layout.py:660 |
| forja_docx_layout.py::audit_docx_layout | calls | forja_docx_layout.py::_effective_run_font_size | EXTRACTED | forja_docx_layout.py:663 |
| forja_docx_layout.py::audit_docx_layout | calls | forja_docx_layout.py::_text_sha256 | EXTRACTED | forja_docx_layout.py:671 |
| forja_docx_layout.py::audit_docx_layout | calls | forja_docx_layout.py::_text_sha256 | EXTRACTED | forja_docx_layout.py:653 |
| forja_docx_layout.py::audit_docx_layout | calls | forja_docx_layout.py::_norm | EXTRACTED | forja_docx_layout.py:689 |
| forja_docx_layout.py::audit_docx_layout | calls | forja_docx_layout.py::_norm | EXTRACTED | forja_docx_layout.py:754 |
| forja_docx_layout.py::audit_docx_layout | calls | forja_docx_layout.py::_norm | EXTRACTED | forja_docx_layout.py:764 |
| forja_docx_layout.py::audit_docx_layout | calls | forja_docx_layout.py::_norm | EXTRACTED | forja_docx_layout.py:764 |
| forja_docx_layout.py::audit_docx_layout | calls | forja_docx_layout.py::_norm | EXTRACTED | forja_docx_layout.py:694 |
| forja_docx_layout.py::audit_docx_layout | calls | forja_docx_layout.py::_norm | EXTRACTED | forja_docx_layout.py:695 |
| forja_docx_layout.py::audit_docx_layout | calls | forja_docx_layout.py::_norm | EXTRACTED | forja_docx_layout.py:695 |
| forja_docx_layout.py::audit_docx_layout | calls | forja_docx_layout.py::_paragraph_text | EXTRACTED | forja_docx_layout.py:728 |
| forja_docx_layout.py::audit_docx_layout | calls | forja_docx_layout.py::_substantial_run_text | EXTRACTED | forja_docx_layout.py:732 |
| forja_docx_layout.py::audit_docx_layout | calls | forja_docx_layout.py::_effective_run_font_size | EXTRACTED | forja_docx_layout.py:735 |
| forja_docx_layout.py::normalize_medina_body | calls | forja_docx_layout.py::compare_docx_content | EXTRACTED | forja_docx_layout.py:932 |
| forja_docx_layout.py::normalize_medina_body | calls | forja_docx_layout.py::audit_docx_layout | EXTRACTED | forja_docx_layout.py:938 |
| forja_docx_layout.py::normalize_medina_body | calls | forja_docx_layout.py::_paragraph_text | EXTRACTED | forja_docx_layout.py:868 |
| forja_docx_layout.py::normalize_medina_body | calls | forja_docx_layout.py::_role_for | EXTRACTED | forja_docx_layout.py:871 |
| forja_docx_layout.py::normalize_medina_body | calls | forja_docx_layout.py::_folio_rectangles | EXTRACTED | forja_docx_layout.py:921 |
| forja_docx_layout.py::normalize_medina_body | calls | forja_docx_layout.py::_vml_width_pt | EXTRACTED | forja_docx_layout.py:922 |
| forja_docx_layout.py::normalize_medina_body | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_docx_layout.py:941 |
| forja_docx_layout.py::normalize_medina_body | calls | forja_docx_layout.py::_set_vml_width_pt | EXTRACTED | forja_docx_layout.py:924 |
| forja_docx_layout.py::normalize_medina_body | calls | forja_docx_layout.py::_substantial_run_text | EXTRACTED | forja_docx_layout.py:876 |
| forja_docx_layout.py::normalize_medina_body | calls | forja_docx_layout.py::_set_run_font_size | EXTRACTED | forja_docx_layout.py:877 |
| forja_docx_layout.py::normalize_medina_body | calls | forja_docx_layout.py::_set_run_font_size | EXTRACTED | forja_docx_layout.py:912 |
| forja_docx_layout.py::normalize_medina_body | calls | forja_docx_layout.py::_substantial_run_text | EXTRACTED | forja_docx_layout.py:888 |
| forja_docx_layout.py::normalize_medina_body | calls | forja_docx_layout.py::_effective_run_font_size | EXTRACTED | forja_docx_layout.py:891 |
| forja_docx_layout.py::main | calls | forja_docx_layout.py::normalize_medina_body | EXTRACTED | forja_docx_layout.py:961 |
| forja_docx_layout.py::main | calls | forja_docx_layout.py::audit_docx_layout | EXTRACTED | forja_docx_layout.py:963 |
| forja_docx_layout.py::main | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_docx_layout.py:965 |
| forja_editorial.py | imports_from | forja_editorial_model.py | EXTRACTED | forja_editorial.py:23 |
| forja_editorial.py | imports_from | forja_editorial_fidelity.py | EXTRACTED | forja_editorial.py:24 |
| forja_editorial.py | imports_from | forja_editorial_fidelity.py | EXTRACTED | forja_editorial.py:24 |
| forja_editorial.py | imports_from | forja_n3_common.py | EXTRACTED | forja_editorial.py:25 |
| forja_editorial.py | imports_from | forja_n3_common.py | EXTRACTED | forja_editorial.py:25 |
| forja_editorial.py | imports_from | forja_n3_common.py | EXTRACTED | forja_editorial.py:25 |
| forja_editorial.py | imports_from | forja_n3_common.py | EXTRACTED | forja_editorial.py:25 |
| forja_editorial.py | imports_from | forja_n3_common.py | EXTRACTED | forja_editorial.py:25 |
| forja_editorial.py | imports_from | forja_n3_common.py | EXTRACTED | forja_editorial.py:25 |
| forja_editorial.py | imports_from | forja_n3_common.py | EXTRACTED | forja_editorial.py:25 |
| forja_editorial.py | imports_from | forja_n3_common.py | EXTRACTED | forja_editorial.py:25 |
| forja_editorial.py::_recompor_stream | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_editorial.py:134 |
| forja_editorial.py::_invoke | calls | forja_editorial.py::_recompor_stream | EXTRACTED | forja_editorial.py:194 |
| forja_editorial.py::_invoke | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_editorial.py:145 |
| forja_editorial.py::_invoke | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_editorial.py:165 |
| forja_editorial.py::_invoke | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_editorial.py:193 |
| forja_editorial.py::_invoke | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_editorial.py:196 |
| forja_editorial.py::_invoke | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_editorial.py:189 |
| forja_editorial.py::_parse_result | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_editorial.py:215 |
| forja_editorial.py::_parse_result | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_editorial.py:218 |
| forja_editorial.py::_parse_result | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_editorial.py:222 |
| forja_editorial.py::_parse_result | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_editorial.py:228 |
| forja_editorial.py::_parse_result | calls | forja_editorial.py::_strip_json_fence | EXTRACTED | forja_editorial.py:224 |
| forja_editorial.py::_parse_result | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_editorial.py:226 |
| forja_editorial.py::_taste_receipt_findings | calls | forja_editorial.py::_normalize_anchor | EXTRACTED | forja_editorial.py:286 |
| forja_editorial.py::_taste_receipt_findings | calls | forja_editorial.py::_normalize_anchor | EXTRACTED | forja_editorial.py:287 |
| forja_editorial.py::_taste_receipt_findings | calls | forja_editorial.py::_normalize_anchor | EXTRACTED | forja_editorial.py:271 |
| forja_editorial.py::_taste_receipt_findings | calls | forja_editorial.py::_normalize_anchor | EXTRACTED | forja_editorial.py:273 |
| forja_editorial.py::_taste_receipt_findings | calls | forja_editorial.py::_normalize_anchor | EXTRACTED | forja_editorial.py:291 |
| forja_editorial.py::_taste_receipt_findings | calls | forja_editorial.py::_normalize_anchor | EXTRACTED | forja_editorial.py:292 |
| forja_editorial.py::_taste_receipt_findings | calls | forja_editorial.py::_normalize_anchor | EXTRACTED | forja_editorial.py:290 |
| forja_editorial.py::_gate_is_clear | calls | forja_n3_common.py::read_json | EXTRACTED | forja_editorial.py:309 |
| forja_editorial.py::run_editorial_pass | calls | forja_editorial_model.py::resolve_executable | EXTRACTED | forja_editorial.py:351 |
| forja_editorial.py::run_editorial_pass | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_editorial.py:366 |
| forja_editorial.py::run_editorial_pass | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_editorial.py:513 |
| forja_editorial.py::run_editorial_pass | calls | forja_editorial.py::_gate_is_clear | EXTRACTED | forja_editorial.py:357 |
| forja_editorial.py::run_editorial_pass | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_editorial.py:358 |
| forja_editorial.py::run_editorial_pass | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_editorial.py:363 |
| forja_editorial.py::run_editorial_pass | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_editorial.py:365 |
| forja_editorial.py::run_editorial_pass | calls | forja_editorial.py::_actual_model | EXTRACTED | forja_editorial.py:399 |
| forja_editorial.py::run_editorial_pass | calls | forja_editorial.py::_parse_result | EXTRACTED | forja_editorial.py:405 |
| forja_editorial.py::run_editorial_pass | calls | forja_editorial.py::_taste_receipt_findings | EXTRACTED | forja_editorial.py:408 |
| forja_editorial.py::run_editorial_pass | calls | forja_n3_common.py::atomic_write_text | EXTRACTED | forja_editorial.py:420 |
| forja_editorial.py::run_editorial_pass | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_editorial.py:421 |
| forja_editorial.py::run_editorial_pass | calls | forja_editorial_model.py::describe | EXTRACTED | forja_editorial.py:423 |
| forja_editorial.py::run_editorial_pass | calls | forja_editorial_model.py::family_assurance | EXTRACTED | forja_editorial.py:428 |
| forja_editorial.py::run_editorial_pass | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_editorial.py:448 |
| forja_editorial.py::run_editorial_pass | calls | forja_n3_common.py::atomic_write_text | EXTRACTED | forja_editorial.py:455 |
| forja_editorial.py::run_editorial_pass | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_editorial.py:458 |
| forja_editorial.py::run_editorial_pass | calls | forja_editorial_fidelity.py::validate_editorial_bundle | EXTRACTED | forja_editorial.py:480 |
| forja_editorial.py::run_editorial_pass | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_editorial.py:484 |
| forja_editorial.py::run_editorial_pass | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_editorial.py:493 |
| forja_editorial.py::run_editorial_pass | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_editorial.py:401 |
| forja_editorial.py::run_editorial_pass | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_editorial.py:407 |
| forja_editorial.py::run_editorial_pass | calls | forja_editorial_model.py::describe | EXTRACTED | forja_editorial.py:425 |
| forja_editorial.py::run_editorial_pass | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_editorial.py:445 |
| forja_editorial.py::run_editorial_pass | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_editorial.py:478 |
| forja_editorial.py::main | calls | forja_n3_common.py::resolve_case_dir | EXTRACTED | forja_editorial.py:534 |
| forja_editorial.py::main | calls | forja_n3_common.py::ensure_within | EXTRACTED | forja_editorial.py:535 |
| forja_editorial.py::main | calls | forja_n3_common.py::read_json | EXTRACTED | forja_editorial.py:536 |
| forja_editorial.py::main | calls | forja_n3_common.py::ensure_within | EXTRACTED | forja_editorial.py:539 |
| forja_editorial.py::main | calls | forja_n3_common.py::ensure_within | EXTRACTED | forja_editorial.py:540 |
| forja_editorial.py::main | calls | forja_editorial.py::run_editorial_pass | EXTRACTED | forja_editorial.py:545 |
| forja_editorial.py::main | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_editorial.py:538 |
| forja_editorial_fidelity.py | imports_from | forja_editorial_model.py | EXTRACTED | forja_editorial_fidelity.py:21 |
| forja_editorial_fidelity.py | imports_from | forja_estilo_humano.py | EXTRACTED | forja_editorial_fidelity.py:22 |
| forja_editorial_fidelity.py | imports_from | forja_n3_common.py | EXTRACTED | forja_editorial_fidelity.py:23 |
| forja_editorial_fidelity.py | imports_from | forja_n3_common.py | EXTRACTED | forja_editorial_fidelity.py:23 |
| forja_editorial_fidelity.py::_counter | calls | forja_editorial_fidelity.py::_fold | EXTRACTED | forja_editorial_fidelity.py:88 |
| forja_editorial_fidelity.py::_heading_counter | calls | forja_editorial_fidelity.py::_fold | EXTRACTED | forja_editorial_fidelity.py:108 |
| forja_editorial_fidelity.py::_heading_counter | calls | forja_editorial_fidelity.py::_is_upper_title | EXTRACTED | forja_editorial_fidelity.py:109 |
| forja_editorial_fidelity.py::_heading_counter | calls | forja_editorial_fidelity.py::_fold | EXTRACTED | forja_editorial_fidelity.py:110 |
| forja_editorial_fidelity.py::_pedidos | calls | forja_editorial_fidelity.py::_is_upper_title | EXTRACTED | forja_editorial_fidelity.py:120 |
| forja_editorial_fidelity.py::_pedidos | calls | forja_editorial_fidelity.py::_fold | EXTRACTED | forja_editorial_fidelity.py:122 |
| forja_editorial_fidelity.py::_authority_semantic_counter | calls | forja_editorial_fidelity.py::_fold | EXTRACTED | forja_editorial_fidelity.py:141 |
| forja_editorial_fidelity.py::_authority_semantic_counter | calls | forja_editorial_fidelity.py::_fold | EXTRACTED | forja_editorial_fidelity.py:137 |
| forja_editorial_fidelity.py::_family_findings | calls | forja_editorial_model.py::family_assurance | EXTRACTED | forja_editorial_fidelity.py:164 |
| forja_editorial_fidelity.py::_family_findings | calls | forja_editorial_fidelity.py::_finding | EXTRACTED | forja_editorial_fidelity.py:171 |
| forja_editorial_fidelity.py::_family_findings | calls | forja_editorial_fidelity.py::_finding | EXTRACTED | forja_editorial_fidelity.py:177 |
| forja_editorial_fidelity.py::_family_findings | calls | forja_editorial_fidelity.py::_finding | EXTRACTED | forja_editorial_fidelity.py:183 |
| forja_editorial_fidelity.py::validate_editorial_bundle | calls | forja_n3_common.py::read_json | EXTRACTED | forja_editorial_fidelity.py:206 |
| forja_editorial_fidelity.py::validate_editorial_bundle | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_editorial_fidelity.py:207 |
| forja_editorial_fidelity.py::validate_editorial_bundle | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_editorial_fidelity.py:208 |
| forja_editorial_fidelity.py::validate_editorial_bundle | calls | forja_editorial_fidelity.py::_authority_semantic_counter | EXTRACTED | forja_editorial_fidelity.py:300 |
| forja_editorial_fidelity.py::validate_editorial_bundle | calls | forja_editorial_fidelity.py::_authority_semantic_counter | EXTRACTED | forja_editorial_fidelity.py:301 |
| forja_editorial_fidelity.py::validate_editorial_bundle | calls | forja_editorial_fidelity.py::_heading_counter | EXTRACTED | forja_editorial_fidelity.py:309 |
| forja_editorial_fidelity.py::validate_editorial_bundle | calls | forja_editorial_fidelity.py::_heading_counter | EXTRACTED | forja_editorial_fidelity.py:310 |
| forja_editorial_fidelity.py::validate_editorial_bundle | calls | forja_editorial_fidelity.py::_pedidos | EXTRACTED | forja_editorial_fidelity.py:327 |
| forja_editorial_fidelity.py::validate_editorial_bundle | calls | forja_editorial_fidelity.py::_pedidos | EXTRACTED | forja_editorial_fidelity.py:328 |
| forja_editorial_fidelity.py::validate_editorial_bundle | calls | forja_editorial_fidelity.py::_family_findings | EXTRACTED | forja_editorial_fidelity.py:250 |
| forja_editorial_fidelity.py::validate_editorial_bundle | calls | forja_n3_common.py::read_json | EXTRACTED | forja_editorial_fidelity.py:259 |
| forja_editorial_fidelity.py::validate_editorial_bundle | calls | forja_editorial_fidelity.py::_counter | EXTRACTED | forja_editorial_fidelity.py:291 |
| forja_editorial_fidelity.py::validate_editorial_bundle | calls | forja_editorial_fidelity.py::_counter | EXTRACTED | forja_editorial_fidelity.py:292 |
| forja_editorial_fidelity.py::validate_editorial_bundle | calls | forja_editorial_fidelity.py::_finding | EXTRACTED | forja_editorial_fidelity.py:212 |
| forja_editorial_fidelity.py::validate_editorial_bundle | calls | forja_editorial_fidelity.py::_finding | EXTRACTED | forja_editorial_fidelity.py:215 |
| forja_editorial_fidelity.py::validate_editorial_bundle | calls | forja_editorial_fidelity.py::_finding | EXTRACTED | forja_editorial_fidelity.py:217 |
| forja_editorial_fidelity.py::validate_editorial_bundle | calls | forja_editorial_fidelity.py::_finding | EXTRACTED | forja_editorial_fidelity.py:224 |
| forja_editorial_fidelity.py::validate_editorial_bundle | calls | forja_editorial_fidelity.py::_finding | EXTRACTED | forja_editorial_fidelity.py:232 |
| forja_editorial_fidelity.py::validate_editorial_bundle | calls | forja_editorial_model.py::is_authorized | EXTRACTED | forja_editorial_fidelity.py:238 |
| forja_editorial_fidelity.py::validate_editorial_bundle | calls | forja_editorial_fidelity.py::_finding | EXTRACTED | forja_editorial_fidelity.py:245 |
| forja_editorial_fidelity.py::validate_editorial_bundle | calls | forja_editorial_fidelity.py::_finding | EXTRACTED | forja_editorial_fidelity.py:253 |
| forja_editorial_fidelity.py::validate_editorial_bundle | calls | forja_editorial_fidelity.py::_finding | EXTRACTED | forja_editorial_fidelity.py:303 |
| forja_editorial_fidelity.py::validate_editorial_bundle | calls | forja_editorial_fidelity.py::_finding | EXTRACTED | forja_editorial_fidelity.py:312 |
| forja_editorial_fidelity.py::validate_editorial_bundle | calls | forja_editorial_fidelity.py::_finding | EXTRACTED | forja_editorial_fidelity.py:321 |
| forja_editorial_fidelity.py::validate_editorial_bundle | calls | forja_editorial_fidelity.py::_finding | EXTRACTED | forja_editorial_fidelity.py:330 |
| forja_editorial_fidelity.py::validate_editorial_bundle | calls | forja_estilo_humano.py::analisar | EXTRACTED | forja_editorial_fidelity.py:346 |
| forja_editorial_fidelity.py::validate_editorial_bundle | calls | forja_editorial_fidelity.py::_finding | EXTRACTED | forja_editorial_fidelity.py:348 |
| forja_editorial_fidelity.py::validate_editorial_bundle | calls | forja_editorial_fidelity.py::_finding | EXTRACTED | forja_editorial_fidelity.py:239 |
| forja_editorial_fidelity.py::validate_editorial_bundle | calls | forja_editorial_fidelity.py::_finding | EXTRACTED | forja_editorial_fidelity.py:261 |
| forja_editorial_fidelity.py::validate_editorial_bundle | calls | forja_editorial_fidelity.py::_finding | EXTRACTED | forja_editorial_fidelity.py:281 |
| forja_editorial_fidelity.py::validate_editorial_bundle | calls | forja_editorial_fidelity.py::_finding | EXTRACTED | forja_editorial_fidelity.py:294 |
| forja_editorial_fidelity.py::validate_editorial_bundle | calls | forja_editorial_fidelity.py::_finding | EXTRACTED | forja_editorial_fidelity.py:340 |
| forja_editorial_fidelity.py::validate_editorial_bundle | calls | forja_editorial_fidelity.py::_finding | EXTRACTED | forja_editorial_fidelity.py:274 |
| forja_editorial_fidelity.py::validate_editorial_bundle | calls | forja_editorial_fidelity.py::_counter_delta | EXTRACTED | forja_editorial_fidelity.py:306 |
| forja_editorial_fidelity.py::validate_editorial_bundle | calls | forja_editorial_fidelity.py::_counter_delta | EXTRACTED | forja_editorial_fidelity.py:315 |
| forja_editorial_fidelity.py::validate_editorial_bundle | calls | forja_editorial_fidelity.py::_counter_delta | EXTRACTED | forja_editorial_fidelity.py:297 |
| forja_editorial_fidelity.py::main | calls | forja_editorial_fidelity.py::validate_editorial_bundle | EXTRACTED | forja_editorial_fidelity.py:395 |
| forja_editorial_model.py | imports_from | forja_n3_common.py | EXTRACTED | forja_editorial_model.py:19 |
| forja_editorial_model.py::resolve | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_editorial_model.py:74 |
| forja_editorial_model.py::resolve_executable | calls | forja_editorial_model.py::resolve | EXTRACTED | forja_editorial_model.py:82 |
| forja_editorial_model.py::resolve_executable | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_editorial_model.py:84 |
| forja_editorial_model.py::family_assurance | calls | forja_editorial_model.py::family_of | EXTRACTED | forja_editorial_model.py:114 |
| forja_editorial_model.py::family_assurance | calls | forja_editorial_model.py::family_of | EXTRACTED | forja_editorial_model.py:115 |
| forja_editorial_model.py::describe | calls | forja_editorial_model.py::resolve | EXTRACTED | forja_editorial_model.py:128 |
| forja_email.py::listar | calls | forja_email.py::_cabecalho | EXTRACTED | forja_email.py:81 |
| forja_email.py::listar | calls | forja_email.py::_cabecalho | EXTRACTED | forja_email.py:82 |
| forja_email.py::enviar_rascunho | calls | forja_email.py::_cabecalho | EXTRACTED | forja_email.py:97 |
| forja_email.py::enviar_rascunho | calls | forja_email.py::_cabecalho | EXTRACTED | forja_email.py:98 |
| forja_email.py::enviar_rascunho | calls | forja_email.py::_registrar | EXTRACTED | forja_email.py:120 |
| forja_email.py::main | calls | forja_email.py::_servico | EXTRACTED | forja_email.py:137 |
| forja_email.py::main | calls | forja_email.py::enviar_rascunho | EXTRACTED | forja_email.py:140 |
| forja_email.py::main | calls | forja_email.py::listar | EXTRACTED | forja_email.py:139 |
| forja_entrega.py | imports_from | forja_estilo_humano.py | EXTRACTED | forja_entrega.py:270 |
| forja_entrega.py::validar_reconciliacao | calls | forja_entrega.py::_reconciliacao_em_texto | EXTRACTED | forja_entrega.py:126 |
| forja_entrega.py::validar_pacote | calls | forja_entrega.py::_entregaveis | EXTRACTED | forja_entrega.py:170 |
| forja_entrega.py::validar_pacote | calls | forja_estilo_humano.py::analisar | EXTRACTED | forja_entrega.py:272 |
| forja_estilo_humano.py::_tokens | calls | forja_estilo_humano.py::_sem_acentos | EXTRACTED | forja_estilo_humano.py:238 |
| forja_estilo_humano.py::_padroes_fixos | calls | forja_estilo_humano.py::_achado | EXTRACTED | forja_estilo_humano.py:251 |
| forja_estilo_humano.py::_padroes_fixos | calls | forja_estilo_humano.py::_achado | EXTRACTED | forja_estilo_humano.py:258 |
| forja_estilo_humano.py::_padroes_fixos | calls | forja_estilo_humano.py::_achado | EXTRACTED | forja_estilo_humano.py:265 |
| forja_estilo_humano.py::_padroes_fixos | calls | forja_estilo_humano.py::_contexto | EXTRACTED | forja_estilo_humano.py:252 |
| forja_estilo_humano.py::_padroes_fixos | calls | forja_estilo_humano.py::_contexto | EXTRACTED | forja_estilo_humano.py:259 |
| forja_estilo_humano.py::_padroes_fixos | calls | forja_estilo_humano.py::_contexto | EXTRACTED | forja_estilo_humano.py:266 |
| forja_estilo_humano.py::_conectores | calls | forja_estilo_humano.py::_sem_acentos | EXTRACTED | forja_estilo_humano.py:281 |
| forja_estilo_humano.py::_conectores | calls | forja_estilo_humano.py::_achado | EXTRACTED | forja_estilo_humano.py:286 |
| forja_estilo_humano.py::_conectores | calls | forja_estilo_humano.py::_achado | EXTRACTED | forja_estilo_humano.py:293 |
| forja_estilo_humano.py::_conectores | calls | forja_estilo_humano.py::_contexto | EXTRACTED | forja_estilo_humano.py:287 |
| forja_estilo_humano.py::_conectores | calls | forja_estilo_humano.py::_contexto | EXTRACTED | forja_estilo_humano.py:294 |
| forja_estilo_humano.py::_travessoes | calls | forja_estilo_humano.py::_achado | EXTRACTED | forja_estilo_humano.py:307 |
| forja_estilo_humano.py::_travessoes | calls | forja_estilo_humano.py::_achado | EXTRACTED | forja_estilo_humano.py:315 |
| forja_estilo_humano.py::_travessoes | calls | forja_estilo_humano.py::_contexto | EXTRACTED | forja_estilo_humano.py:308 |
| forja_estilo_humano.py::_travessoes | calls | forja_estilo_humano.py::_contexto | EXTRACTED | forja_estilo_humano.py:316 |
| forja_estilo_humano.py::_dogmatismo | calls | forja_estilo_humano.py::_achado | EXTRACTED | forja_estilo_humano.py:328 |
| forja_estilo_humano.py::_dogmatismo | calls | forja_estilo_humano.py::_achado | EXTRACTED | forja_estilo_humano.py:339 |
| forja_estilo_humano.py::_dogmatismo | calls | forja_estilo_humano.py::_contexto | EXTRACTED | forja_estilo_humano.py:329 |
| forja_estilo_humano.py::_redundancia | calls | forja_estilo_humano.py::_sentencas | EXTRACTED | forja_estilo_humano.py:351 |
| forja_estilo_humano.py::_redundancia | calls | forja_estilo_humano.py::_sem_acentos | EXTRACTED | forja_estilo_humano.py:368 |
| forja_estilo_humano.py::_redundancia | calls | forja_estilo_humano.py::_sem_acentos | EXTRACTED | forja_estilo_humano.py:369 |
| forja_estilo_humano.py::_redundancia | calls | forja_estilo_humano.py::_tokens | EXTRACTED | forja_estilo_humano.py:353 |
| forja_estilo_humano.py::_redundancia | calls | forja_estilo_humano.py::_tokens | EXTRACTED | forja_estilo_humano.py:353 |
| forja_estilo_humano.py::_redundancia | calls | forja_estilo_humano.py::_achado | EXTRACTED | forja_estilo_humano.py:361 |
| forja_estilo_humano.py::_redundancia | calls | forja_estilo_humano.py::_achado | EXTRACTED | forja_estilo_humano.py:374 |
| forja_estilo_humano.py::_ritmo_robotico | calls | forja_estilo_humano.py::_sentencas | EXTRACTED | forja_estilo_humano.py:383 |
| forja_estilo_humano.py::_ritmo_robotico | calls | forja_estilo_humano.py::_cv | EXTRACTED | forja_estilo_humano.py:389 |
| forja_estilo_humano.py::_ritmo_robotico | calls | forja_estilo_humano.py::_achado | EXTRACTED | forja_estilo_humano.py:391 |
| forja_estilo_humano.py::_simetria | calls | forja_estilo_humano.py::_cv | EXTRACTED | forja_estilo_humano.py:408 |
| forja_estilo_humano.py::_simetria | calls | forja_estilo_humano.py::_achado | EXTRACTED | forja_estilo_humano.py:417 |
| forja_estilo_humano.py::_simetria | calls | forja_estilo_humano.py::_sentencas | EXTRACTED | forja_estilo_humano.py:409 |
| forja_estilo_humano.py::_conclusao_tautologica | calls | forja_estilo_humano.py::_tokens | EXTRACTED | forja_estilo_humano.py:432 |
| forja_estilo_humano.py::_conclusao_tautologica | calls | forja_estilo_humano.py::_tokens | EXTRACTED | forja_estilo_humano.py:433 |
| forja_estilo_humano.py::_conclusao_tautologica | calls | forja_estilo_humano.py::_achado | EXTRACTED | forja_estilo_humano.py:444 |
| forja_estilo_humano.py::_email_especifico | calls | forja_estilo_humano.py::_achado | EXTRACTED | forja_estilo_humano.py:466 |
| forja_estilo_humano.py::_email_especifico | calls | forja_estilo_humano.py::_sentencas | EXTRACTED | forja_estilo_humano.py:475 |
| forja_estilo_humano.py::_email_especifico | calls | forja_estilo_humano.py::_achado | EXTRACTED | forja_estilo_humano.py:478 |
| forja_estilo_humano.py::_email_especifico | calls | forja_estilo_humano.py::_achado | EXTRACTED | forja_estilo_humano.py:488 |
| forja_estilo_humano.py::_email_especifico | calls | forja_estilo_humano.py::_achado | EXTRACTED | forja_estilo_humano.py:497 |
| forja_estilo_humano.py::_email_especifico | calls | forja_estilo_humano.py::_achado | EXTRACTED | forja_estilo_humano.py:457 |
| forja_estilo_humano.py::_email_especifico | calls | forja_estilo_humano.py::_contexto | EXTRACTED | forja_estilo_humano.py:469 |
| forja_estilo_humano.py::_email_especifico | calls | forja_estilo_humano.py::_contexto | EXTRACTED | forja_estilo_humano.py:460 |
| forja_estilo_humano.py::analisar | calls | forja_estilo_humano.py::_limpar_markdown | EXTRACTED | forja_estilo_humano.py:511 |
| forja_estilo_humano.py::analisar | calls | forja_estilo_humano.py::_paragrafos | EXTRACTED | forja_estilo_humano.py:512 |
| forja_estilo_humano.py::analisar | calls | forja_estilo_humano.py::_limpar_email | EXTRACTED | forja_estilo_humano.py:510 |
| forja_estilo_humano.py::analisar | calls | forja_estilo_humano.py::_padroes_fixos | EXTRACTED | forja_estilo_humano.py:514 |
| forja_estilo_humano.py::analisar | calls | forja_estilo_humano.py::_conectores | EXTRACTED | forja_estilo_humano.py:515 |
| forja_estilo_humano.py::analisar | calls | forja_estilo_humano.py::_travessoes | EXTRACTED | forja_estilo_humano.py:516 |
| forja_estilo_humano.py::analisar | calls | forja_estilo_humano.py::_dogmatismo | EXTRACTED | forja_estilo_humano.py:517 |
| forja_estilo_humano.py::analisar | calls | forja_estilo_humano.py::_redundancia | EXTRACTED | forja_estilo_humano.py:518 |
| forja_estilo_humano.py::analisar | calls | forja_estilo_humano.py::_ritmo_robotico | EXTRACTED | forja_estilo_humano.py:519 |
| forja_estilo_humano.py::analisar | calls | forja_estilo_humano.py::_simetria | EXTRACTED | forja_estilo_humano.py:521 |
| forja_estilo_humano.py::analisar | calls | forja_estilo_humano.py::_conclusao_tautologica | EXTRACTED | forja_estilo_humano.py:522 |
| forja_estilo_humano.py::analisar | calls | forja_estilo_humano.py::_email_especifico | EXTRACTED | forja_estilo_humano.py:524 |
| forja_estilo_humano.py::relatorio | calls | forja_estilo_humano.py::analisar | EXTRACTED | forja_estilo_humano.py:537 |
| forja_estilo_humano.py::main | calls | forja_estilo_humano.py::relatorio | EXTRACTED | forja_estilo_humano.py:554 |
| forja_exploracao_100.py | imports_from | forja_n3_common.py | EXTRACTED | forja_exploracao_100.py:21 |
| forja_exploracao_100.py | imports_from | forja_n4_common.py | EXTRACTED | forja_exploracao_100.py:22 |
| forja_exploracao_100.py | imports_from | forja_n4_common.py | EXTRACTED | forja_exploracao_100.py:22 |
| forja_exploracao_100.py::selectable_findings | calls | forja_exploracao_100.py::_issue | EXTRACTED | forja_exploracao_100.py:102 |
| forja_exploracao_100.py::selectable_findings | calls | forja_exploracao_100.py::_norm | EXTRACTED | forja_exploracao_100.py:106 |
| forja_exploracao_100.py::selectable_findings | calls | forja_exploracao_100.py::_issue | EXTRACTED | forja_exploracao_100.py:109 |
| forja_exploracao_100.py::selectable_findings | calls | forja_exploracao_100.py::_norm | EXTRACTED | forja_exploracao_100.py:113 |
| forja_exploracao_100.py::selectable_findings | calls | forja_exploracao_100.py::_norm | EXTRACTED | forja_exploracao_100.py:113 |
| forja_exploracao_100.py::selectable_findings | calls | forja_exploracao_100.py::_issue | EXTRACTED | forja_exploracao_100.py:114 |
| forja_exploracao_100.py::selectable_findings | calls | forja_exploracao_100.py::_issue | EXTRACTED | forja_exploracao_100.py:119 |
| forja_exploracao_100.py::selectable_findings | calls | forja_exploracao_100.py::_issue | EXTRACTED | forja_exploracao_100.py:124 |
| forja_exploracao_100.py::selectable_findings | calls | forja_exploracao_100.py::_issue | EXTRACTED | forja_exploracao_100.py:130 |
| forja_exploracao_100.py::selectable_findings | calls | forja_exploracao_100.py::_norm | EXTRACTED | forja_exploracao_100.py:134 |
| forja_exploracao_100.py::selectable_findings | calls | forja_exploracao_100.py::_issue | EXTRACTED | forja_exploracao_100.py:143 |
| forja_exploracao_100.py::selectable_findings | calls | forja_exploracao_100.py::_issue | EXTRACTED | forja_exploracao_100.py:148 |
| forja_exploracao_100.py::selectable_findings | calls | forja_exploracao_100.py::_issue | EXTRACTED | forja_exploracao_100.py:135 |
| forja_exploracao_100.py::select_consultation_questions | calls | forja_exploracao_100.py::selectable_findings | EXTRACTED | forja_exploracao_100.py:158 |
| forja_exploracao_100.py::select_consultation_questions | calls | forja_exploracao_100.py::_norm | EXTRACTED | forja_exploracao_100.py:164 |
| forja_exploracao_100.py::select_consultation_questions | calls | forja_exploracao_100.py::_issue | EXTRACTED | forja_exploracao_100.py:169 |
| forja_exploracao_100.py::validate_dialectic | calls | forja_exploracao_100.py::_issue | EXTRACTED | forja_exploracao_100.py:185 |
| forja_exploracao_100.py::validate_dialectic | calls | forja_exploracao_100.py::_issue | EXTRACTED | forja_exploracao_100.py:191 |
| forja_exploracao_100.py::validate_dialectic | calls | forja_exploracao_100.py::_issue | EXTRACTED | forja_exploracao_100.py:195 |
| forja_exploracao_100.py::validate_dialectic | calls | forja_exploracao_100.py::_norm | EXTRACTED | forja_exploracao_100.py:199 |
| forja_exploracao_100.py::validate_dialectic | calls | forja_exploracao_100.py::_issue | EXTRACTED | forja_exploracao_100.py:202 |
| forja_exploracao_100.py::validate_dialectic | calls | forja_exploracao_100.py::selectable_findings | EXTRACTED | forja_exploracao_100.py:213 |
| forja_exploracao_100.py::validate_dialectic | calls | forja_exploracao_100.py::_issue | EXTRACTED | forja_exploracao_100.py:250 |
| forja_exploracao_100.py::validate_dialectic | calls | forja_exploracao_100.py::_issue | EXTRACTED | forja_exploracao_100.py:211 |
| forja_exploracao_100.py::validate_dialectic | calls | forja_exploracao_100.py::_issue | EXTRACTED | forja_exploracao_100.py:219 |
| forja_exploracao_100.py::validate_dialectic | calls | forja_exploracao_100.py::_norm | EXTRACTED | forja_exploracao_100.py:223 |
| forja_exploracao_100.py::validate_dialectic | calls | forja_exploracao_100.py::_issue | EXTRACTED | forja_exploracao_100.py:224 |
| forja_exploracao_100.py::validate_dialectic | calls | forja_exploracao_100.py::_issue | EXTRACTED | forja_exploracao_100.py:230 |
| forja_exploracao_100.py::validate_dialectic | calls | forja_exploracao_100.py::_issue | EXTRACTED | forja_exploracao_100.py:263 |
| forja_exploracao_100.py::validate_dialectic | calls | forja_exploracao_100.py::_issue | EXTRACTED | forja_exploracao_100.py:221 |
| forja_exploracao_100.py::validate_dialectic | calls | forja_exploracao_100.py::_issue | EXTRACTED | forja_exploracao_100.py:244 |
| forja_exploracao_100.py::_placeholder | calls | forja_exploracao_100.py::_norm | EXTRACTED | forja_exploracao_100.py:450 |
| forja_exploracao_100.py::build_scaffold | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_exploracao_100.py:476 |
| forja_exploracao_100.py::build_scaffold | calls | forja_n4_common.py::expected_content_hash | EXTRACTED | forja_exploracao_100.py:510 |
| forja_exploracao_100.py::validate_exploration_100 | calls | forja_exploracao_100.py::_norm | EXTRACTED | forja_exploracao_100.py:539 |
| forja_exploracao_100.py::validate_exploration_100 | calls | forja_exploracao_100.py::_placeholder | EXTRACTED | forja_exploracao_100.py:583 |
| forja_exploracao_100.py::validate_exploration_100 | calls | forja_exploracao_100.py::_placeholder | EXTRACTED | forja_exploracao_100.py:585 |
| forja_exploracao_100.py::validate_exploration_100 | calls | forja_exploracao_100.py::_issue | EXTRACTED | forja_exploracao_100.py:518 |
| forja_exploracao_100.py::validate_exploration_100 | calls | forja_exploracao_100.py::_issue | EXTRACTED | forja_exploracao_100.py:520 |
| forja_exploracao_100.py::validate_exploration_100 | calls | forja_exploracao_100.py::_issue | EXTRACTED | forja_exploracao_100.py:524 |
| forja_exploracao_100.py::validate_exploration_100 | calls | forja_exploracao_100.py::_issue | EXTRACTED | forja_exploracao_100.py:529 |
| forja_exploracao_100.py::validate_exploration_100 | calls | forja_exploracao_100.py::_issue | EXTRACTED | forja_exploracao_100.py:537 |
| forja_exploracao_100.py::validate_exploration_100 | calls | forja_exploracao_100.py::_issue | EXTRACTED | forja_exploracao_100.py:541 |
| forja_exploracao_100.py::validate_exploration_100 | calls | forja_exploracao_100.py::_placeholder | EXTRACTED | forja_exploracao_100.py:549 |
| forja_exploracao_100.py::validate_exploration_100 | calls | forja_exploracao_100.py::_issue | EXTRACTED | forja_exploracao_100.py:581 |
| forja_exploracao_100.py::validate_exploration_100 | calls | forja_exploracao_100.py::_issue | EXTRACTED | forja_exploracao_100.py:584 |
| forja_exploracao_100.py::validate_exploration_100 | calls | forja_exploracao_100.py::_issue | EXTRACTED | forja_exploracao_100.py:586 |
| forja_exploracao_100.py::validate_exploration_100 | calls | forja_exploracao_100.py::_issue | EXTRACTED | forja_exploracao_100.py:590 |
| forja_exploracao_100.py::validate_exploration_100 | calls | forja_exploracao_100.py::_placeholder | EXTRACTED | forja_exploracao_100.py:593 |
| forja_exploracao_100.py::validate_exploration_100 | calls | forja_exploracao_100.py::_issue | EXTRACTED | forja_exploracao_100.py:606 |
| forja_exploracao_100.py::validate_exploration_100 | calls | forja_exploracao_100.py::_issue | EXTRACTED | forja_exploracao_100.py:609 |
| forja_exploracao_100.py::validate_exploration_100 | calls | forja_exploracao_100.py::_issue | EXTRACTED | forja_exploracao_100.py:534 |
| forja_exploracao_100.py::validate_exploration_100 | calls | forja_exploracao_100.py::_issue | EXTRACTED | forja_exploracao_100.py:552 |
| forja_exploracao_100.py::validate_exploration_100 | calls | forja_exploracao_100.py::_issue | EXTRACTED | forja_exploracao_100.py:555 |
| forja_exploracao_100.py::validate_exploration_100 | calls | forja_exploracao_100.py::_issue | EXTRACTED | forja_exploracao_100.py:557 |
| forja_exploracao_100.py::validate_exploration_100 | calls | forja_exploracao_100.py::_issue | EXTRACTED | forja_exploracao_100.py:559 |
| forja_exploracao_100.py::validate_exploration_100 | calls | forja_exploracao_100.py::_issue | EXTRACTED | forja_exploracao_100.py:570 |
| forja_exploracao_100.py::validate_exploration_100 | calls | forja_exploracao_100.py::_issue | EXTRACTED | forja_exploracao_100.py:579 |
| forja_exploracao_100.py::validate_exploration_100 | calls | forja_exploracao_100.py::_issue | EXTRACTED | forja_exploracao_100.py:594 |
| forja_exploracao_100.py::validate_exploration_100 | calls | forja_exploracao_100.py::_issue | EXTRACTED | forja_exploracao_100.py:596 |
| forja_exploracao_100.py::validate_exploration_100 | calls | forja_exploracao_100.py::_issue | EXTRACTED | forja_exploracao_100.py:602 |
| forja_exploracao_100.py::validate_exploration_100 | calls | forja_exploracao_100.py::_issue | EXTRACTED | forja_exploracao_100.py:548 |
| forja_exploracao_100.py::validate_exploration_100 | calls | forja_exploracao_100.py::_issue | EXTRACTED | forja_exploracao_100.py:550 |
| forja_exploracao_100.py::validate_exploration_100 | calls | forja_exploracao_100.py::_issue | EXTRACTED | forja_exploracao_100.py:562 |
| forja_exploracao_100.py::validate_exploration_100 | calls | forja_exploracao_100.py::_issue | EXTRACTED | forja_exploracao_100.py:567 |
| forja_exploracao_100.py::gates_da_exploracao | calls | forja_exploracao_100.py::validate_exploration_100 | EXTRACTED | forja_exploracao_100.py:652 |
| forja_exploracao_100.py::render_consultation | calls | forja_exploracao_100.py::selectable_findings | EXTRACTED | forja_exploracao_100.py:733 |
| forja_exploracao_100.py::render_consultation | calls | forja_exploracao_100.py::_norm | EXTRACTED | forja_exploracao_100.py:704 |
| forja_exploracao_100.py::render_consultation | calls | forja_exploracao_100.py::_texto | EXTRACTED | forja_exploracao_100.py:719 |
| forja_exploracao_100.py::render_consultation | calls | forja_exploracao_100.py::_texto | EXTRACTED | forja_exploracao_100.py:720 |
| forja_exploracao_100.py::render_consultation | calls | forja_exploracao_100.py::_texto | EXTRACTED | forja_exploracao_100.py:721 |
| forja_exploracao_100.py::render_consultation | calls | forja_exploracao_100.py::_texto | EXTRACTED | forja_exploracao_100.py:724 |
| forja_exploracao_100.py::render_consultation | calls | forja_exploracao_100.py::_texto | EXTRACTED | forja_exploracao_100.py:749 |
| forja_exploracao_100.py::main | calls | forja_exploracao_100.py::select_consultation_questions | EXTRACTED | forja_exploracao_100.py:813 |
| forja_exploracao_100.py::main | calls | forja_exploracao_100.py::render_consultation | EXTRACTED | forja_exploracao_100.py:821 |
| forja_exploracao_100.py::main | calls | forja_exploracao_100.py::record_response | EXTRACTED | forja_exploracao_100.py:835 |
| forja_exploracao_100.py::main | calls | forja_exploracao_100.py::validate_dialectic | EXTRACTED | forja_exploracao_100.py:837 |
| forja_exploracao_100.py::main | calls | forja_exploracao_100.py::validate_exploration_100 | EXTRACTED | forja_exploracao_100.py:844 |
| forja_exploracao_100.py::main | calls | forja_exploracao_100.py::validate_dialectic | EXTRACTED | forja_exploracao_100.py:844 |
| forja_exploracao_100.py::main | calls | forja_exploracao_100.py::build_scaffold | EXTRACTED | forja_exploracao_100.py:806 |
| forja_f10_contract.py | imports_from | forja_n3_common.py | EXTRACTED | forja_f10_contract.py:18 |
| forja_f10_contract.py::_external_identifier_valid | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_f10_contract.py:41 |
| forja_f10_contract.py::compute_f10_gates | calls | forja_f10_contract.py::_pass | EXTRACTED | forja_f10_contract.py:81 |
| forja_f10_contract.py::compute_f10_gates | calls | forja_f10_contract.py::_pass | EXTRACTED | forja_f10_contract.py:82 |
| forja_f10_contract.py::compute_f10_gates | calls | forja_f10_contract.py::_pass | EXTRACTED | forja_f10_contract.py:83 |
| forja_f10_contract.py::compute_f10_gates | calls | forja_f10_contract.py::_external_identifier_valid | EXTRACTED | forja_f10_contract.py:81 |
| forja_f10_contract.py::compute_f10_gates | calls | forja_f10_contract.py::_management_synced | EXTRACTED | forja_f10_contract.py:84 |
| forja_f2_check.py::tribunais_do_texto | calls | forja_f2_check.py::tribunal_do_cnj | EXTRACTED | forja_f2_check.py:63 |
| forja_f2_check.py::validar_classificacao | calls | forja_f2_check.py::tribunais_do_texto | EXTRACTED | forja_f2_check.py:89 |
| forja_f2_check.py::main | calls | forja_f2_check.py::validar_classificacao | EXTRACTED | forja_f2_check.py:123 |
| forja_f8_contract.py | imports_from | forja_docx_layout.py | EXTRACTED | forja_f8_contract.py:15 |
| forja_f8_contract.py | imports_from | forja_human_review.py | EXTRACTED | forja_f8_contract.py:16 |
| forja_f8_contract.py | imports_from | forja_n3_common.py | EXTRACTED | forja_f8_contract.py:17 |
| forja_f8_contract.py | imports_from | forja_n3_common.py | EXTRACTED | forja_f8_contract.py:17 |
| forja_f8_contract.py | imports_from | forja_n3_common.py | EXTRACTED | forja_f8_contract.py:17 |
| forja_f8_contract.py | imports_from | forja_visual_review.py | EXTRACTED | forja_f8_contract.py:18 |
| forja_f8_contract.py | imports_from | forja_visual_review.py | EXTRACTED | forja_f8_contract.py:18 |
| forja_f8_contract.py | imports_from | forja_fidelity.py | EXTRACTED | forja_f8_contract.py:19 |
| forja_f8_contract.py | imports_from | forja_visual_qa.py | EXTRACTED | forja_f8_contract.py:24 |
| forja_f8_contract.py::inspect_pdf | calls | forja_visual_qa.py::inspect_pdf | EXTRACTED | forja_f8_contract.py:26 |
| forja_f8_contract.py::_validate_static_f8 | calls | forja_n3_common.py::read_json | EXTRACTED | forja_f8_contract.py:31 |
| forja_f8_contract.py::_validate_static_f8 | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_f8_contract.py:33 |
| forja_f8_contract.py::_validate_static_f8 | calls | forja_f8_contract.py::_gates_do_contrato | EXTRACTED | forja_f8_contract.py:97 |
| forja_f8_contract.py::_validate_static_f8 | calls | forja_docx_layout.py::audit_docx_layout | EXTRACTED | forja_f8_contract.py:57 |
| forja_f8_contract.py::_validate_static_f8 | calls | forja_fidelity.py::compare_docx_fidelity | EXTRACTED | forja_f8_contract.py:75 |
| forja_f8_contract.py::_validate_static_f8 | calls | forja_n3_common.py::read_json | EXTRACTED | forja_f8_contract.py:86 |
| forja_f8_contract.py::_validate_static_f8 | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_f8_contract.py:54 |
| forja_f8_contract.py::_gates_do_contrato | calls | forja_f8_contract.py::_svg_lint | EXTRACTED | forja_f8_contract.py:201 |
| forja_f8_contract.py::_gates_do_contrato | calls | forja_f8_contract.py::_markdown_lint | EXTRACTED | forja_f8_contract.py:202 |
| forja_f8_contract.py::_validate_legacy_f8 | calls | forja_n3_common.py::read_json | EXTRACTED | forja_f8_contract.py:254 |
| forja_f8_contract.py::_validate_legacy_f8 | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_f8_contract.py:256 |
| forja_f8_contract.py::_validate_legacy_f8 | calls | forja_docx_layout.py::audit_docx_layout | EXTRACTED | forja_f8_contract.py:302 |
| forja_f8_contract.py::_validate_legacy_f8 | calls | forja_f8_contract.py::inspect_pdf | EXTRACTED | forja_f8_contract.py:320 |
| forja_f8_contract.py::_validate_legacy_f8 | calls | forja_visual_review.py::validate_visual_review | EXTRACTED | forja_f8_contract.py:339 |
| forja_f8_contract.py::_validate_legacy_f8 | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_f8_contract.py:336 |
| forja_f8_contract.py::_validate_legacy_f8 | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_f8_contract.py:355 |
| forja_f8_contract.py::_validate_legacy_f8 | calls | forja_human_review.py::validate_visual_review_receipt | EXTRACTED | forja_f8_contract.py:358 |
| forja_f8_contract.py::_validate_legacy_f8 | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_f8_contract.py:363 |
| forja_f8_contract.py::_validate_legacy_f8 | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_f8_contract.py:364 |
| forja_f8_contract.py::_validate_legacy_f8 | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_f8_contract.py:368 |
| forja_f8_contract.py::validate_f8 | calls | forja_n3_common.py::read_json | EXTRACTED | forja_f8_contract.py:393 |
| forja_f8_contract.py::validate_f8 | calls | forja_f8_contract.py::_validate_legacy_f8 | EXTRACTED | forja_f8_contract.py:399 |
| forja_f8_contract.py::validate_f8 | calls | forja_f8_contract.py::_validate_static_f8 | EXTRACTED | forja_f8_contract.py:398 |
| forja_fable5.py | imports_from | forja_editorial.py | EXTRACTED | forja_fable5.py:26 |
| forja_fable5.py | imports_from | forja_editorial.py | EXTRACTED | forja_fable5.py:27 |
| forja_fable5.py | imports_from | forja_editorial.py | EXTRACTED | forja_fable5.py:27 |
| forja_fable5.py | imports_from | forja_editorial.py | EXTRACTED | forja_fable5.py:27 |
| forja_fable5.py | imports_from | forja_editorial.py | EXTRACTED | forja_fable5.py:27 |
| forja_fable5.py | imports_from | forja_editorial.py | EXTRACTED | forja_fable5.py:27 |
| forja_fable5.py | imports_from | forja_editorial.py | EXTRACTED | forja_fable5.py:27 |
| forja_fable5.py | imports_from | forja_editorial.py | EXTRACTED | forja_fable5.py:27 |
| forja_fable5.py | imports_from | forja_editorial.py | EXTRACTED | forja_fable5.py:27 |
| forja_fable5.py | imports_from | forja_editorial.py | EXTRACTED | forja_fable5.py:27 |
| forja_fidelity.py | imports_from | forja_context.py | EXTRACTED | forja_fidelity.py:17 |
| forja_fidelity.py | imports_from | forja_n3_common.py | EXTRACTED | forja_fidelity.py:18 |
| forja_fidelity.py | imports_from | forja_n3_common.py | EXTRACTED | forja_fidelity.py:18 |
| forja_fidelity.py | imports_from | forja_n3_common.py | EXTRACTED | forja_fidelity.py:18 |
| forja_fidelity.py::_segments | calls | forja_fidelity.py::_norm | EXTRACTED | forja_fidelity.py:68 |
| forja_fidelity.py::_coverage | calls | forja_fidelity.py::_norm | EXTRACTED | forja_fidelity.py:75 |
| forja_fidelity.py::_missing_numbers | calls | forja_fidelity.py::_number_tokens | EXTRACTED | forja_fidelity.py:132 |
| forja_fidelity.py::_qualifier_counts | calls | forja_fidelity.py::_norm | EXTRACTED | forja_fidelity.py:143 |
| forja_fidelity.py::_qualifier_counts | calls | forja_fidelity.py::_norm | EXTRACTED | forja_fidelity.py:144 |
| forja_fidelity.py::compare_fidelity | calls | forja_fidelity.py::_docx_text | EXTRACTED | forja_fidelity.py:149 |
| forja_fidelity.py::compare_fidelity | calls | forja_fidelity.py::_pdf_text | EXTRACTED | forja_fidelity.py:150 |
| forja_fidelity.py::compare_fidelity | calls | forja_context.py::markdown_blocks | EXTRACTED | forja_fidelity.py:151 |
| forja_fidelity.py::compare_fidelity | calls | forja_fidelity.py::_coverage | EXTRACTED | forja_fidelity.py:162 |
| forja_fidelity.py::compare_fidelity | calls | forja_fidelity.py::_coverage | EXTRACTED | forja_fidelity.py:163 |
| forja_fidelity.py::compare_fidelity | calls | forja_fidelity.py::_number_tokens | EXTRACTED | forja_fidelity.py:164 |
| forja_fidelity.py::compare_fidelity | calls | forja_fidelity.py::_qualifier_counts | EXTRACTED | forja_fidelity.py:165 |
| forja_fidelity.py::compare_fidelity | calls | forja_fidelity.py::_missing_numbers | EXTRACTED | forja_fidelity.py:171 |
| forja_fidelity.py::compare_fidelity | calls | forja_fidelity.py::_missing_numbers | EXTRACTED | forja_fidelity.py:172 |
| forja_fidelity.py::compare_fidelity | calls | forja_fidelity.py::_missing_counter | EXTRACTED | forja_fidelity.py:177 |
| forja_fidelity.py::compare_fidelity | calls | forja_fidelity.py::_missing_counter | EXTRACTED | forja_fidelity.py:178 |
| forja_fidelity.py::compare_fidelity | calls | forja_fidelity.py::_segments | EXTRACTED | forja_fidelity.py:154 |
| forja_fidelity.py::compare_fidelity | calls | forja_fidelity.py::_qualifier_counts | EXTRACTED | forja_fidelity.py:177 |
| forja_fidelity.py::compare_fidelity | calls | forja_fidelity.py::_qualifier_counts | EXTRACTED | forja_fidelity.py:178 |
| forja_fidelity.py::compare_fidelity | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_fidelity.py:185 |
| forja_fidelity.py::compare_fidelity | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_fidelity.py:186 |
| forja_fidelity.py::compare_fidelity | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_fidelity.py:187 |
| forja_fidelity.py::compare_fidelity | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_fidelity.py:188 |
| forja_fidelity.py::compare_docx_fidelity | calls | forja_fidelity.py::_docx_text | EXTRACTED | forja_fidelity.py:213 |
| forja_fidelity.py::compare_docx_fidelity | calls | forja_context.py::markdown_blocks | EXTRACTED | forja_fidelity.py:214 |
| forja_fidelity.py::compare_docx_fidelity | calls | forja_fidelity.py::_coverage | EXTRACTED | forja_fidelity.py:225 |
| forja_fidelity.py::compare_docx_fidelity | calls | forja_fidelity.py::_number_tokens | EXTRACTED | forja_fidelity.py:226 |
| forja_fidelity.py::compare_docx_fidelity | calls | forja_fidelity.py::_qualifier_counts | EXTRACTED | forja_fidelity.py:227 |
| forja_fidelity.py::compare_docx_fidelity | calls | forja_fidelity.py::_missing_numbers | EXTRACTED | forja_fidelity.py:228 |
| forja_fidelity.py::compare_docx_fidelity | calls | forja_fidelity.py::_missing_counter | EXTRACTED | forja_fidelity.py:229 |
| forja_fidelity.py::compare_docx_fidelity | calls | forja_fidelity.py::_segments | EXTRACTED | forja_fidelity.py:217 |
| forja_fidelity.py::compare_docx_fidelity | calls | forja_fidelity.py::_qualifier_counts | EXTRACTED | forja_fidelity.py:229 |
| forja_fidelity.py::compare_docx_fidelity | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_fidelity.py:239 |
| forja_fidelity.py::compare_docx_fidelity | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_fidelity.py:241 |
| forja_fidelity.py::compare_docx_fidelity | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_fidelity.py:242 |
| forja_fidelity.py::write_fidelity | calls | forja_fidelity.py::compare_fidelity | EXTRACTED | forja_fidelity.py:257 |
| forja_fidelity.py::write_fidelity | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_fidelity.py:258 |
| forja_fidelity.py::main | calls | forja_fidelity.py::write_fidelity | EXTRACTED | forja_fidelity.py:269 |
| forja_fila.py | imports_from | forja_n3_common.py | EXTRACTED | forja_fila.py:29 |
| forja_fila.py | imports_from | forja_n3_common.py | EXTRACTED | forja_fila.py:29 |
| forja_fila.py | imports_from | forja_n3_common.py | EXTRACTED | forja_fila.py:29 |
| forja_fila.py | imports_from | forja_n3_common.py | EXTRACTED | forja_fila.py:337 |
| forja_fila.py::classificar_prontidao | calls | forja_fila.py::_fase_num | EXTRACTED | forja_fila.py:97 |
| forja_fila.py::classificar_prontidao | calls | forja_fila.py::_norm | EXTRACTED | forja_fila.py:116 |
| forja_fila.py::pontuar | calls | forja_fila.py::_parse_date | EXTRACTED | forja_fila.py:131 |
| forja_fila.py::pontuar | calls | forja_fila.py::_parse_date | EXTRACTED | forja_fila.py:158 |
| forja_fila.py::pontuar | calls | forja_fila.py::_norm | EXTRACTED | forja_fila.py:127 |
| forja_fila.py::pontuar | calls | forja_fila.py::_norm | EXTRACTED | forja_fila.py:154 |
| forja_fila.py::ordenar | calls | forja_fila.py::_parse_date | EXTRACTED | forja_fila.py:170 |
| forja_fila.py::ordenar | calls | forja_fila.py::_parse_date | EXTRACTED | forja_fila.py:171 |
| forja_fila.py::pendencia_operacao_assistida | calls | forja_fila.py::_parse_date | EXTRACTED | forja_fila.py:185 |
| forja_fila.py::montar_fila | calls | forja_fila.py::ordenar | EXTRACTED | forja_fila.py:243 |
| forja_fila.py::montar_fila | calls | forja_fila.py::ordenar | EXTRACTED | forja_fila.py:247 |
| forja_fila.py::montar_fila | calls | forja_fila.py::classificar_prontidao | EXTRACTED | forja_fila.py:212 |
| forja_fila.py::montar_fila | calls | forja_fila.py::pontuar | EXTRACTED | forja_fila.py:220 |
| forja_fila.py::montar_fila | calls | forja_fila.py::_aguardando_desde | EXTRACTED | forja_fila.py:232 |
| forja_fila.py::montar_fila | calls | forja_fila.py::_parse_date | EXTRACTED | forja_fila.py:235 |
| forja_fila.py::_carregar_states | calls | forja_fila.py::_read_json | EXTRACTED | forja_fila.py:278 |
| forja_fila.py::gerar | calls | forja_fila.py::montar_fila | EXTRACTED | forja_fila.py:336 |
| forja_fila.py::gerar | calls | forja_fila.py::pendencia_operacao_assistida | EXTRACTED | forja_fila.py:338 |
| forja_fila.py::gerar | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_fila.py:339 |
| forja_fila.py::gerar | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_fila.py:348 |
| forja_fila.py::gerar | calls | forja_fila.py::_carregar_states | EXTRACTED | forja_fila.py:336 |
| forja_fila.py::gerar | calls | forja_n3_common.py::load_config | EXTRACTED | forja_fila.py:338 |
| forja_fila.py::gerar | calls | forja_fila.py::_relatorio_md | EXTRACTED | forja_fila.py:351 |
| forja_fila.py::gerar | calls | forja_n3_common.py::feature_enabled | EXTRACTED | forja_fila.py:354 |
| forja_fila.py::gerar | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_fila.py:356 |
| forja_fila.py::main | calls | forja_fila.py::gerar | EXTRACTED | forja_fila.py:377 |
| forja_fila.py::main | calls | forja_fila.py::gerar | EXTRACTED | forja_fila.py:366 |
| forja_fila.py::main | calls | forja_fila.py::gerar | EXTRACTED | forja_fila.py:370 |
| forja_fontes_oficiais.py | imports_from | forja_artefatos.py | EXTRACTED | forja_fontes_oficiais.py:44 |
| forja_fontes_oficiais.py::validar_fontes_arquivadas | calls | forja_fontes_oficiais.py::_fontes | EXTRACTED | forja_fontes_oficiais.py:107 |
| forja_fontes_oficiais.py::validar_fontes_arquivadas | calls | forja_fontes_oficiais.py::_primeiro | EXTRACTED | forja_fontes_oficiais.py:129 |
| forja_fontes_oficiais.py::validar_fontes_arquivadas | calls | forja_fontes_oficiais.py::_primeiro | EXTRACTED | forja_fontes_oficiais.py:130 |
| forja_fontes_oficiais.py::validar_fontes_arquivadas | calls | forja_fontes_oficiais.py::_resolver | EXTRACTED | forja_fontes_oficiais.py:134 |
| forja_fontes_oficiais.py::validar_fontes_arquivadas | calls | forja_fontes_oficiais.py::_primeiro | EXTRACTED | forja_fontes_oficiais.py:118 |
| forja_fontes_oficiais.py::validar_fontes_arquivadas | calls | forja_fontes_oficiais.py::_primeiro | EXTRACTED | forja_fontes_oficiais.py:118 |
| forja_fontes_oficiais.py::validar_fontes_arquivadas | calls | forja_fontes_oficiais.py::_rotulo | EXTRACTED | forja_fontes_oficiais.py:150 |
| forja_fontes_oficiais.py::validar_fontes_arquivadas | calls | forja_fontes_oficiais.py::_rotulo | EXTRACTED | forja_fontes_oficiais.py:123 |
| forja_fontes_oficiais.py::validar_cotejo_citacoes | calls | forja_fontes_oficiais.py::_itens_checklist | EXTRACTED | forja_fontes_oficiais.py:297 |
| forja_fontes_oficiais.py::validar_cotejo_citacoes | calls | forja_fontes_oficiais.py::_cotejo_em_texto | EXTRACTED | forja_fontes_oficiais.py:286 |
| forja_fontes_oficiais.py::validar_cotejo_citacoes | calls | forja_fontes_oficiais.py::_usou_citacao_textual | EXTRACTED | forja_fontes_oficiais.py:307 |
| forja_fontes_oficiais.py::validar_cotejo_citacoes | calls | forja_fontes_oficiais.py::_cotejo_registrado | EXTRACTED | forja_fontes_oficiais.py:317 |
| forja_fontes_oficiais.py::validar_pesquisa_oficial | calls | forja_fontes_oficiais.py::validar_fontes_arquivadas | EXTRACTED | forja_fontes_oficiais.py:349 |
| forja_fontes_oficiais.py::validar_pesquisa_oficial | calls | forja_fontes_oficiais.py::validar_cotejo_citacoes | EXTRACTED | forja_fontes_oficiais.py:350 |
| forja_forma_artefatos.py::censo_de_formas | calls | forja_forma_artefatos.py::_lidos_pelo_censo | EXTRACTED | forja_forma_artefatos.py:80 |
| forja_forma_artefatos.py::censo_de_formas | calls | forja_forma_artefatos.py::_radical | EXTRACTED | forja_forma_artefatos.py:73 |
| forja_gate_liveness.py | imports_from | forja_n3_common.py | EXTRACTED | forja_gate_liveness.py:68 |
| forja_gate_liveness.py::_alias | calls | forja_n3_common.py::name_with_legacy | EXTRACTED | forja_gate_liveness.py:72 |
| forja_gate_liveness.py::_sem_produtor | calls | forja_gate_liveness.py::_alias | EXTRACTED | forja_gate_liveness.py:158 |
| forja_gate_liveness.py::medir | calls | forja_gate_liveness.py::_nomes_declarados | EXTRACTED | forja_gate_liveness.py:164 |
| forja_gate_liveness.py::medir | calls | forja_gate_liveness.py::_observados | EXTRACTED | forja_gate_liveness.py:165 |
| forja_gate_liveness.py::medir | calls | forja_gate_liveness.py::_alias | EXTRACTED | forja_gate_liveness.py:184 |
| forja_gate_liveness.py::medir | calls | forja_gate_liveness.py::_alias | EXTRACTED | forja_gate_liveness.py:170 |
| forja_gate_liveness.py::medir | calls | forja_gate_liveness.py::_sem_produtor | EXTRACTED | forja_gate_liveness.py:191 |
| forja_gate_liveness.py::main | calls | forja_gate_liveness.py::medir | EXTRACTED | forja_gate_liveness.py:280 |
| forja_gate_liveness.py::main | calls | forja_gate_liveness.py::relatar | EXTRACTED | forja_gate_liveness.py:281 |
| forja_headless.py | imports_from | forja_n3_common.py | EXTRACTED | forja_headless.py:17 |
| forja_headless.py | imports_from | forja_n3_common.py | EXTRACTED | forja_headless.py:17 |
| forja_headless.py | imports_from | forja_n3_common.py | EXTRACTED | forja_headless.py:17 |
| forja_headless.py | imports_from | forja_n3_common.py | EXTRACTED | forja_headless.py:17 |
| forja_headless.py | imports_from | forja_n3_common.py | EXTRACTED | forja_headless.py:17 |
| forja_headless.py | imports_from | forja_n3_common.py | EXTRACTED | forja_headless.py:17 |
| forja_headless.py | imports_from | forja_n3_common.py | EXTRACTED | forja_headless.py:17 |
| forja_headless.py | imports_from | forja_n3_common.py | EXTRACTED | forja_headless.py:17 |
| forja_headless.py | imports_from | forja_adversarial_audit.py | EXTRACTED | forja_headless.py:27 |
| forja_headless.py | imports_from | forja_exploracao_100.py | EXTRACTED | forja_headless.py:28 |
| forja_headless.py | imports_from | forja_estilo_humano.py | EXTRACTED | forja_headless.py:29 |
| forja_headless.py::_invoke_headless | calls | forja_headless.py::_confirmar_modelo | EXTRACTED | forja_headless.py:86 |
| forja_headless.py::_invoke_headless | calls | forja_estilo_humano.py::mandatory_prompt_for_phase | EXTRACTED | forja_headless.py:62 |
| forja_headless.py::_invoke_headless | calls | forja_adversarial_audit.py::mandatory_prompt_for_phase | EXTRACTED | forja_headless.py:62 |
| forja_headless.py::_invoke_headless | calls | forja_exploracao_100.py::mandatory_prompt_for_phase | EXTRACTED | forja_headless.py:61 |
| forja_headless.py::_validate_n3_attempt | calls | forja_n3_common.py::resolve_case_dir | EXTRACTED | forja_headless.py:111 |
| forja_headless.py::_validate_n3_attempt | calls | forja_n3_common.py::ensure_within | EXTRACTED | forja_headless.py:112 |
| forja_headless.py::_validate_n3_attempt | calls | forja_n3_common.py::read_json | EXTRACTED | forja_headless.py:113 |
| forja_headless.py::_validate_n3_attempt | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_headless.py:115 |
| forja_headless.py::_validate_n3_attempt | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_headless.py:117 |
| forja_headless.py::_write_n3_attempt | calls | forja_n3_common.py::atomic_write_text | EXTRACTED | forja_headless.py:124 |
| forja_headless.py::_write_n3_attempt | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_headless.py:129 |
| forja_headless.py::_write_n3_attempt | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_headless.py:135 |
| forja_headless.py::_write_n3_attempt | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_headless.py:126 |
| forja_headless.py::run_phase | calls | forja_n3_common.py::feature_enabled | EXTRACTED | forja_headless.py:147 |
| forja_headless.py::run_phase | calls | forja_headless.py::_invoke_headless | EXTRACTED | forja_headless.py:162 |
| forja_headless.py::run_phase | calls | forja_n3_common.py::atomic_write_text | EXTRACTED | forja_headless.py:178 |
| forja_headless.py::run_phase | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_headless.py:183 |
| forja_headless.py::run_phase | calls | forja_headless.py::append_unique | EXTRACTED | forja_headless.py:187 |
| forja_headless.py::run_phase | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_headless.py:193 |
| forja_headless.py::run_phase | calls | forja_headless.py::_validate_n3_attempt | EXTRACTED | forja_headless.py:152 |
| forja_headless.py::run_phase | calls | forja_headless.py::_write_n3_attempt | EXTRACTED | forja_headless.py:165 |
| forja_headless.py::run_phase | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_headless.py:186 |
| forja_headless.py::run_phase | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_headless.py:189 |
| forja_headless.py::run_phase | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_headless.py:180 |
| forja_headless.py::main | calls | forja_headless.py::run_phase | EXTRACTED | forja_headless.py:206 |
| forja_human_review.py | imports_from | forja_n3_common.py | EXTRACTED | forja_human_review.py:22 |
| forja_human_review.py | imports_from | forja_n3_common.py | EXTRACTED | forja_human_review.py:22 |
| forja_human_review.py::_load_pinned_trust_store | calls | forja_n3_common.py::read_json | EXTRACTED | forja_human_review.py:153 |
| forja_human_review.py::_load_pinned_trust_store | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_human_review.py:168 |
| forja_human_review.py::_load_pinned_trust_store | calls | forja_n3_common.py::read_json | EXTRACTED | forja_human_review.py:171 |
| forja_human_review.py::_validate_signed_receipt | calls | forja_n3_common.py::read_json | EXTRACTED | forja_human_review.py:185 |
| forja_human_review.py::_validate_signed_receipt | calls | forja_human_review.py::_load_pinned_trust_store | EXTRACTED | forja_human_review.py:208 |
| forja_human_review.py::_validate_signed_receipt | calls | forja_human_review.py::_trusted_key | EXTRACTED | forja_human_review.py:216 |
| forja_human_review.py::_validate_signed_receipt | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_human_review.py:238 |
| forja_human_review.py::_validate_signed_receipt | calls | forja_human_review.py::public_key_id | EXTRACTED | forja_human_review.py:221 |
| forja_human_review.py::_validate_signed_receipt | calls | forja_human_review.py::canonical_receipt_bytes | EXTRACTED | forja_human_review.py:227 |
| forja_human_review.py::validate_claim_review_receipt | calls | forja_human_review.py::_validate_signed_receipt | EXTRACTED | forja_human_review.py:253 |
| forja_human_review.py::validate_visual_review_receipt | calls | forja_human_review.py::_validate_signed_receipt | EXTRACTED | forja_human_review.py:271 |
| forja_import_audited_cycle.py | imports_from | forja_n3_common.py | EXTRACTED | forja_import_audited_cycle.py:10 |
| forja_import_audited_cycle.py | imports_from | forja_n3_common.py | EXTRACTED | forja_import_audited_cycle.py:10 |
| forja_import_audited_cycle.py | imports_from | forja_state_machine.py | EXTRACTED | forja_import_audited_cycle.py:11 |
| forja_import_audited_cycle.py | imports_from | forja_state_machine.py | EXTRACTED | forja_import_audited_cycle.py:11 |
| forja_import_audited_cycle.py::import_cycle | calls | forja_state_machine.py::derive_state | EXTRACTED | forja_import_audited_cycle.py:37 |
| forja_import_audited_cycle.py::import_cycle | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_import_audited_cycle.py:39 |
| forja_import_audited_cycle.py::import_cycle | calls | forja_import_audited_cycle.py::role_for | EXTRACTED | forja_import_audited_cycle.py:40 |
| forja_import_audited_cycle.py::import_cycle | calls | forja_state_machine.py::record_event | EXTRACTED | forja_import_audited_cycle.py:53 |
| forja_import_audited_cycle.py::main | calls | forja_import_audited_cycle.py::import_cycle | EXTRACTED | forja_import_audited_cycle.py:73 |
| forja_import_audited_cycle.py::main | calls | forja_n3_common.py::resolve_case_dir | EXTRACTED | forja_import_audited_cycle.py:73 |
| forja_ingestao.py | imports_from | forja_artefatos.py | EXTRACTED | forja_ingestao.py:33 |
| forja_ingestao.py::validar_indice_documentos | calls | forja_ingestao.py::_lista | EXTRACTED | forja_ingestao.py:82 |
| forja_ingestao.py::validar_indice_documentos | calls | forja_ingestao.py::_tem_conteudo | EXTRACTED | forja_ingestao.py:85 |
| forja_ingestao.py::validar_indice_documentos | calls | forja_ingestao.py::_tem_conteudo | EXTRACTED | forja_ingestao.py:102 |
| forja_ingestao.py::validar_cobertura | calls | forja_ingestao.py::_tem_conteudo | EXTRACTED | forja_ingestao.py:171 |
| forja_ingestao.py::validar_cobertura | calls | forja_ingestao.py::_tem_conteudo | EXTRACTED | forja_ingestao.py:204 |
| forja_ingestao.py::validar_ingestao | calls | forja_ingestao.py::validar_indice_documentos | EXTRACTED | forja_ingestao.py:226 |
| forja_ingestao.py::validar_ingestao | calls | forja_ingestao.py::validar_cobertura | EXTRACTED | forja_ingestao.py:227 |
| forja_injection_scan.py | imports_from | forja_metadata.py | EXTRACTED | forja_injection_scan.py:33 |
| forja_injection_scan.py::_gravar_json_seguro | calls | forja_metadata.py::retry_transient_io | EXTRACTED | forja_injection_scan.py:149 |
| forja_injection_scan.py::analisar_pdf | calls | forja_injection_scan.py::distancia_rgb | EXTRACTED | forja_injection_scan.py:250 |
| forja_injection_scan.py::analisar_pdf | calls | forja_injection_scan.py::distancia_rgb | EXTRACTED | forja_injection_scan.py:265 |
| forja_injection_scan.py::_achatar | calls | forja_injection_scan.py::_achatar | EXTRACTED | forja_injection_scan.py:342 |
| forja_injection_scan.py::_achatar | calls | forja_injection_scan.py::_achatar | EXTRACTED | forja_injection_scan.py:345 |
| forja_injection_scan.py::_houve_varredura | calls | forja_injection_scan.py::_achatar | EXTRACTED | forja_injection_scan.py:349 |
| forja_injection_scan.py::_p0_detectado | calls | forja_injection_scan.py::_achatar | EXTRACTED | forja_injection_scan.py:361 |
| forja_injection_scan.py::_tem_triagem | calls | forja_injection_scan.py::_achatar | EXTRACTED | forja_injection_scan.py:387 |
| forja_injection_scan.py::validar_triagem_injecao | calls | forja_injection_scan.py::_houve_varredura | EXTRACTED | forja_injection_scan.py:411 |
| forja_injection_scan.py::validar_triagem_injecao | calls | forja_injection_scan.py::_p0_detectado | EXTRACTED | forja_injection_scan.py:419 |
| forja_injection_scan.py::validar_triagem_injecao | calls | forja_injection_scan.py::_tem_triagem | EXTRACTED | forja_injection_scan.py:419 |
| forja_injection_scan.py::main | calls | forja_injection_scan.py::_esta_dentro_de | EXTRACTED | forja_injection_scan.py:477 |
| forja_injection_scan.py::main | calls | forja_injection_scan.py::processar_entrada | EXTRACTED | forja_injection_scan.py:443 |
| forja_injection_scan.py::main | calls | forja_injection_scan.py::analisar_pdf | EXTRACTED | forja_injection_scan.py:460 |
| forja_injection_scan.py::main | calls | forja_injection_scan.py::_gravar_json_seguro | EXTRACTED | forja_injection_scan.py:490 |
| forja_injection_scan.py::main | calls | forja_injection_scan.py::_gravar_json_seguro | EXTRACTED | forja_injection_scan.py:544 |
| forja_injection_scan.py::main | calls | forja_injection_scan.py::_gravar_json_seguro | EXTRACTED | forja_injection_scan.py:527 |
| forja_injection_scan.py::main | calls | forja_injection_scan.py::_gravar_json_seguro | EXTRACTED | forja_injection_scan.py:499 |
| forja_injection_scan.py::main | calls | forja_injection_scan.py::_id_origem | EXTRACTED | forja_injection_scan.py:484 |
| forja_injection_scan.py::main | calls | forja_injection_scan.py::_id_origem | EXTRACTED | forja_injection_scan.py:487 |
| forja_injection_scan.py::main | calls | forja_injection_scan.py::_id_origem | EXTRACTED | forja_injection_scan.py:524 |
| forja_injection_scan.py::main | calls | forja_injection_scan.py::_id_origem | EXTRACTED | forja_injection_scan.py:498 |
| forja_lastro.py::validar_lastro_fatos | calls | forja_lastro.py::_norm | EXTRACTED | forja_lastro.py:378 |
| forja_lastro.py::validar_lastro_fatos | calls | forja_lastro.py::_conferivel_como_texto | EXTRACTED | forja_lastro.py:404 |
| forja_lastro.py::validar_lastro_fatos | calls | forja_lastro.py::_norm | EXTRACTED | forja_lastro.py:423 |
| forja_lastro.py::validar_lastro_fatos | calls | forja_lastro.py::_norm | EXTRACTED | forja_lastro.py:423 |
| forja_lastro.py::analisar_texto | calls | forja_lastro.py::_negado | EXTRACTED | forja_lastro.py:524 |
| forja_lastro.py::analisar_texto | calls | forja_lastro.py::_negado | EXTRACTED | forja_lastro.py:536 |
| forja_lastro.py::analisar_texto | calls | forja_lastro.py::_ctx | EXTRACTED | forja_lastro.py:505 |
| forja_lastro.py::analisar_texto | calls | forja_lastro.py::_ctx | EXTRACTED | forja_lastro.py:528 |
| forja_lastro.py::analisar_texto | calls | forja_lastro.py::_ctx | EXTRACTED | forja_lastro.py:516 |
| forja_lastro.py::analisar_texto | calls | forja_lastro.py::_ctx | EXTRACTED | forja_lastro.py:556 |
| forja_lastro.py::analisar_texto | calls | forja_lastro.py::_ctx | EXTRACTED | forja_lastro.py:542 |
| forja_lastro.py::_data_base_do_produto | calls | forja_lastro.py::_normalizar_data_base | EXTRACTED | forja_lastro.py:645 |
| forja_lastro.py::_valores_monetarios | calls | forja_lastro.py::_numero_monetario | EXTRACTED | forja_lastro.py:747 |
| forja_lastro.py::validar_fonte_prevalente | calls | forja_lastro.py::_fonte_prevalente | EXTRACTED | forja_lastro.py:810 |
| forja_lastro.py::validar_fonte_prevalente | calls | forja_lastro.py::_fonte_path | EXTRACTED | forja_lastro.py:826 |
| forja_lastro.py::validar_fonte_prevalente | calls | forja_lastro.py::_achado | EXTRACTED | forja_lastro.py:812 |
| forja_lastro.py::validar_fonte_prevalente | calls | forja_lastro.py::_achado | EXTRACTED | forja_lastro.py:816 |
| forja_lastro.py::validar_fonte_prevalente | calls | forja_lastro.py::_achado | EXTRACTED | forja_lastro.py:823 |
| forja_lastro.py::validar_fonte_prevalente | calls | forja_lastro.py::_achado | EXTRACTED | forja_lastro.py:828 |
| forja_lastro.py::validar_fonte_prevalente | calls | forja_lastro.py::_achado | EXTRACTED | forja_lastro.py:835 |
| forja_lastro.py::validar_fonte_prevalente | calls | forja_lastro.py::_sha256_file | EXTRACTED | forja_lastro.py:831 |
| forja_lastro.py::validar_fonte_prevalente | calls | forja_lastro.py::_achado | EXTRACTED | forja_lastro.py:833 |
| forja_lastro.py::_ancora_aponta_prevalente | calls | forja_lastro.py::_texto_da_ancora | EXTRACTED | forja_lastro.py:865 |
| forja_lastro.py::validar_data_base | calls | forja_lastro.py::_fonte_prevalente | EXTRACTED | forja_lastro.py:879 |
| forja_lastro.py::validar_data_base | calls | forja_lastro.py::_normalizar_data_base | EXTRACTED | forja_lastro.py:883 |
| forja_lastro.py::validar_data_base | calls | forja_lastro.py::_data_base_do_produto | EXTRACTED | forja_lastro.py:884 |
| forja_lastro.py::validar_data_base | calls | forja_lastro.py::_achado | EXTRACTED | forja_lastro.py:886 |
| forja_lastro.py::validar_data_base | calls | forja_lastro.py::_achado | EXTRACTED | forja_lastro.py:889 |
| forja_lastro.py::validar_data_base | calls | forja_lastro.py::_achado | EXTRACTED | forja_lastro.py:892 |
| forja_lastro.py::validar_valores_monetarios | calls | forja_lastro.py::_valores_monetarios | EXTRACTED | forja_lastro.py:912 |
| forja_lastro.py::validar_valores_monetarios | calls | forja_lastro.py::_fonte_prevalente | EXTRACTED | forja_lastro.py:934 |
| forja_lastro.py::validar_valores_monetarios | calls | forja_lastro.py::_anchor_entries | EXTRACTED | forja_lastro.py:935 |
| forja_lastro.py::validar_valores_monetarios | calls | forja_lastro.py::material_economico | EXTRACTED | forja_lastro.py:905 |
| forja_lastro.py::validar_valores_monetarios | calls | forja_lastro.py::_texto_da_ancora | EXTRACTED | forja_lastro.py:941 |
| forja_lastro.py::validar_valores_monetarios | calls | forja_lastro.py::_achado | EXTRACTED | forja_lastro.py:906 |
| forja_lastro.py::validar_valores_monetarios | calls | forja_lastro.py::_achado | EXTRACTED | forja_lastro.py:924 |
| forja_lastro.py::validar_valores_monetarios | calls | forja_lastro.py::_ancora_aponta_prevalente | EXTRACTED | forja_lastro.py:939 |
| forja_lastro.py::validar_valores_monetarios | calls | forja_lastro.py::_achado | EXTRACTED | forja_lastro.py:954 |
| forja_lastro.py::validar_valores_monetarios | calls | forja_lastro.py::_numero_monetario | EXTRACTED | forja_lastro.py:943 |
| forja_lastro.py::_inventario_economico | calls | forja_lastro.py::_sha256_file | EXTRACTED | forja_lastro.py:1009 |
| forja_lastro.py::_inventario_economico | calls | forja_lastro.py::_normalizar_data_base | EXTRACTED | forja_lastro.py:1001 |
| forja_lastro.py::validar_hierarquia_fontes | calls | forja_lastro.py::_inventario_economico | EXTRACTED | forja_lastro.py:1051 |
| forja_lastro.py::validar_hierarquia_fontes | calls | forja_lastro.py::_fonte_path | EXTRACTED | forja_lastro.py:1054 |
| forja_lastro.py::validar_hierarquia_fontes | calls | forja_lastro.py::_descartes | EXTRACTED | forja_lastro.py:1057 |
| forja_lastro.py::validar_hierarquia_fontes | calls | forja_lastro.py::_normalizar_data_base | EXTRACTED | forja_lastro.py:1058 |
| forja_lastro.py::validar_hierarquia_fontes | calls | forja_lastro.py::_descartado | EXTRACTED | forja_lastro.py:1065 |
| forja_lastro.py::validar_hierarquia_fontes | calls | forja_lastro.py::_fonte_prevalente | EXTRACTED | forja_lastro.py:1046 |
| forja_lastro.py::validar_hierarquia_fontes | calls | forja_lastro.py::_examinado | EXTRACTED | forja_lastro.py:1067 |
| forja_lastro.py::validar_hierarquia_fontes | calls | forja_lastro.py::_achado | EXTRACTED | forja_lastro.py:1068 |
| forja_lastro.py::validar_hierarquia_fontes | calls | forja_lastro.py::_achado | EXTRACTED | forja_lastro.py:1073 |
| forja_lastro.py::validar_hierarquia_fontes | calls | forja_lastro.py::_achado | EXTRACTED | forja_lastro.py:1077 |
| forja_lastro.py::validar_aritmetica_derivada | calls | forja_lastro.py::_valores_monetarios | EXTRACTED | forja_lastro.py:1100 |
| forja_lastro.py::validar_aritmetica_derivada | calls | forja_lastro.py::_numero_monetario | EXTRACTED | forja_lastro.py:1103 |
| forja_lastro.py::validar_aritmetica_derivada | calls | forja_lastro.py::_numero_monetario | EXTRACTED | forja_lastro.py:1105 |
| forja_lastro.py::validar_aritmetica_derivada | calls | forja_lastro.py::_achado | EXTRACTED | forja_lastro.py:1098 |
| forja_lastro.py::validar_aritmetica_derivada | calls | forja_lastro.py::_achado | EXTRACTED | forja_lastro.py:1107 |
| forja_lastro.py::validar_aritmetica_derivada | calls | forja_lastro.py::_achado | EXTRACTED | forja_lastro.py:1136 |
| forja_lastro.py::validar_aritmetica_derivada | calls | forja_lastro.py::_achado | EXTRACTED | forja_lastro.py:1115 |
| forja_lastro.py::validar_aritmetica_derivada | calls | forja_lastro.py::_achado | EXTRACTED | forja_lastro.py:1129 |
| forja_lastro.py::validar_gates_economicos | calls | forja_lastro.py::material_economico | EXTRACTED | forja_lastro.py:1151 |
| forja_lastro.py::validar_gates_economicos | calls | forja_lastro.py::validar_aritmetica_derivada | EXTRACTED | forja_lastro.py:1170 |
| forja_lastro.py::validar_gates_economicos | calls | forja_lastro.py::_achado | EXTRACTED | forja_lastro.py:1157 |
| forja_lastro.py::validar_gates_economicos | calls | forja_lastro.py::validar_hierarquia_fontes | EXTRACTED | forja_lastro.py:1169 |
| forja_lastro.py::validar_gates_economicos | calls | forja_lastro.py::validar_valores_monetarios | EXTRACTED | forja_lastro.py:1168 |
| forja_lastro.py::validar_gates_economicos | calls | forja_lastro.py::validar_fonte_prevalente | EXTRACTED | forja_lastro.py:1166 |
| forja_lastro.py::validar_gates_economicos | calls | forja_lastro.py::validar_data_base | EXTRACTED | forja_lastro.py:1167 |
| forja_lastro.py::verificar_tudo | calls | forja_lastro.py::analisar_texto | EXTRACTED | forja_lastro.py:1184 |
| forja_lastro.py::verificar_tudo | calls | forja_lastro.py::validar_gates_economicos | EXTRACTED | forja_lastro.py:1189 |
| forja_lastro.py::verificar_tudo | calls | forja_lastro.py::validar_lastro_fatos | EXTRACTED | forja_lastro.py:1186 |
| forja_lastro.py::verificar_tudo | calls | forja_lastro.py::validar_decisoes_revisao | EXTRACTED | forja_lastro.py:1193 |
| forja_lastro.py::verificar_tudo | calls | forja_lastro.py::exigir_criterio_vigente | EXTRACTED | forja_lastro.py:1188 |
| forja_learning.py | imports_from | forja_n3_common.py | EXTRACTED | forja_learning.py:10 |
| forja_learning.py | imports_from | forja_n4_common.py | EXTRACTED | forja_learning.py:11 |
| forja_learning.py | imports_from | forja_n4_common.py | EXTRACTED | forja_learning.py:11 |
| forja_learning.py | imports_from | forja_n4_common.py | EXTRACTED | forja_learning.py:11 |
| forja_learning.py | imports_from | forja_post_protocol_contracts.py | EXTRACTED | forja_learning.py:12 |
| forja_learning.py | imports_from | forja_post_protocol_contracts.py | EXTRACTED | forja_learning.py:12 |
| forja_learning.py | imports_from | forja_post_protocol_contracts.py | EXTRACTED | forja_learning.py:12 |
| forja_learning.py::_raw_keys | calls | forja_learning.py::_raw_keys | EXTRACTED | forja_learning.py:49 |
| forja_learning.py::_raw_keys | calls | forja_learning.py::_raw_keys | EXTRACTED | forja_learning.py:52 |
| forja_learning.py::validate_feedback_assimilation | calls | forja_n4_common.py::ids_unique | EXTRACTED | forja_learning.py:64 |
| forja_learning.py::validate_feedback_assimilation | calls | forja_n4_common.py::ids_unique | EXTRACTED | forja_learning.py:65 |
| forja_learning.py::validate_feedback_assimilation | calls | forja_n4_common.py::ids_unique | EXTRACTED | forja_learning.py:66 |
| forja_learning.py::validate_feedback_assimilation | calls | forja_n4_common.py::ids_unique | EXTRACTED | forja_learning.py:67 |
| forja_learning.py::validate_feedback_assimilation | calls | forja_learning.py::_raw_keys | EXTRACTED | forja_learning.py:68 |
| forja_learning.py::validate_feedback_assimilation | calls | forja_learning.py::_duplicates | EXTRACTED | forja_learning.py:86 |
| forja_learning.py::validate_feedback_assimilation | calls | forja_n4_common.py::issue | EXTRACTED | forja_learning.py:69 |
| forja_learning.py::validate_feedback_assimilation | calls | forja_n4_common.py::issue | EXTRACTED | forja_learning.py:87 |
| forja_learning.py::validate_feedback_assimilation | calls | forja_n4_common.py::issue | EXTRACTED | forja_learning.py:77 |
| forja_learning.py::validate_feedback_assimilation | calls | forja_n4_common.py::issue | EXTRACTED | forja_learning.py:79 |
| forja_learning.py::validate_feedback_assimilation | calls | forja_n4_common.py::issue | EXTRACTED | forja_learning.py:83 |
| forja_learning.py::validate_feedback_assimilation | calls | forja_n4_common.py::issue | EXTRACTED | forja_learning.py:85 |
| forja_learning.py::validate_feedback_assimilation | calls | forja_n4_common.py::issue | EXTRACTED | forja_learning.py:94 |
| forja_learning.py::validate_feedback_assimilation | calls | forja_n4_common.py::issue | EXTRACTED | forja_learning.py:96 |
| forja_learning.py::validate_feedback_assimilation | calls | forja_n4_common.py::issue | EXTRACTED | forja_learning.py:98 |
| forja_learning.py::validate_feedback_assimilation | calls | forja_n4_common.py::issue | EXTRACTED | forja_learning.py:100 |
| forja_learning.py::validate_feedback_assimilation | calls | forja_n4_common.py::issue | EXTRACTED | forja_learning.py:102 |
| forja_learning.py::validate_feedback_assimilation | calls | forja_n4_common.py::issue | EXTRACTED | forja_learning.py:104 |
| forja_learning.py::validate_feedback_assimilation | calls | forja_n4_common.py::issue | EXTRACTED | forja_learning.py:106 |
| forja_learning.py::validate_feedback_assimilation | calls | forja_n4_common.py::issue | EXTRACTED | forja_learning.py:115 |
| forja_learning.py::validate_feedback_assimilation | calls | forja_n4_common.py::issue | EXTRACTED | forja_learning.py:117 |
| forja_learning.py::validate_feedback_assimilation | calls | forja_n4_common.py::issue | EXTRACTED | forja_learning.py:119 |
| forja_learning.py::validate_feedback_assimilation | calls | forja_n4_common.py::issue | EXTRACTED | forja_learning.py:121 |
| forja_learning.py::validate_feedback_assimilation | calls | forja_n4_common.py::issue | EXTRACTED | forja_learning.py:123 |
| forja_learning.py::validate_feedback_assimilation | calls | forja_n4_common.py::issue | EXTRACTED | forja_learning.py:133 |
| forja_learning.py::validate_feedback_assimilation | calls | forja_n4_common.py::issue | EXTRACTED | forja_learning.py:135 |
| forja_learning.py::validate_feedback_assimilation | calls | forja_n4_common.py::issue | EXTRACTED | forja_learning.py:144 |
| forja_learning.py::validate_feedback_assimilation | calls | forja_n4_common.py::issue | EXTRACTED | forja_learning.py:146 |
| forja_learning.py::validate_feedback_assimilation | calls | forja_n4_common.py::issue | EXTRACTED | forja_learning.py:148 |
| forja_learning.py::validate_feedback_assimilation | calls | forja_n4_common.py::issue | EXTRACTED | forja_learning.py:150 |
| forja_learning.py::validate_feedback_assimilation | calls | forja_n4_common.py::issue | EXTRACTED | forja_learning.py:154 |
| forja_learning.py::validate_feedback_assimilation | calls | forja_n4_common.py::issue | EXTRACTED | forja_learning.py:109 |
| forja_learning.py::validate_feedback_assimilation | calls | forja_n4_common.py::issue | EXTRACTED | forja_learning.py:138 |
| forja_learning.py::validate_learning | calls | forja_n4_common.py::ids_unique | EXTRACTED | forja_learning.py:162 |
| forja_learning.py::validate_learning | calls | forja_n4_common.py::ids_unique | EXTRACTED | forja_learning.py:162 |
| forja_learning.py::validate_learning | calls | forja_n4_common.py::issue | EXTRACTED | forja_learning.py:164 |
| forja_learning.py::validate_learning | calls | forja_learning.py::validate_feedback_assimilation | EXTRACTED | forja_learning.py:198 |
| forja_learning.py::validate_learning | calls | forja_n4_common.py::issue | EXTRACTED | forja_learning.py:169 |
| forja_learning.py::validate_learning | calls | forja_n4_common.py::issue | EXTRACTED | forja_learning.py:172 |
| forja_learning.py::validate_learning | calls | forja_n4_common.py::issue | EXTRACTED | forja_learning.py:176 |
| forja_learning.py::validate_learning | calls | forja_n4_common.py::issue | EXTRACTED | forja_learning.py:180 |
| forja_learning.py::validate_learning | calls | forja_n4_common.py::issue | EXTRACTED | forja_learning.py:182 |
| forja_learning.py::validate_learning | calls | forja_n4_common.py::issue | EXTRACTED | forja_learning.py:184 |
| forja_learning.py::validate_learning | calls | forja_n4_common.py::issue | EXTRACTED | forja_learning.py:189 |
| forja_learning.py::validate_learning | calls | forja_n4_common.py::issue | EXTRACTED | forja_learning.py:192 |
| forja_learning.py::validate_learning | calls | forja_n4_common.py::issue | EXTRACTED | forja_learning.py:194 |
| forja_learning.py::validate_learning | calls | forja_n4_common.py::issue | EXTRACTED | forja_learning.py:196 |
| forja_learning.py::validate_learning | calls | forja_n4_common.py::issue | EXTRACTED | forja_learning.py:174 |
| forja_learning.py::validate_case | calls | forja_n4_common.py::validate_file | EXTRACTED | forja_learning.py:203 |
| forja_learning.py::main | calls | forja_learning.py::validate_case | EXTRACTED | forja_learning.py:211 |
| forja_learning.py::main | calls | forja_n3_common.py::resolve_case_dir | EXTRACTED | forja_learning.py:211 |
| forja_learning_registry.py | imports_from | forja_n3_common.py | EXTRACTED | forja_learning_registry.py:11 |
| forja_learning_registry.py | imports_from | forja_n3_common.py | EXTRACTED | forja_learning_registry.py:11 |
| forja_learning_registry.py | imports_from | forja_n3_common.py | EXTRACTED | forja_learning_registry.py:11 |
| forja_learning_registry.py | imports_from | forja_n3_common.py | EXTRACTED | forja_learning_registry.py:11 |
| forja_learning_registry.py | imports_from | forja_n3_common.py | EXTRACTED | forja_learning_registry.py:11 |
| forja_learning_registry.py | imports_from | forja_n3_common.py | EXTRACTED | forja_learning_registry.py:11 |
| forja_learning_registry.py | imports_from | forja_n3_common.py | EXTRACTED | forja_learning_registry.py:11 |
| forja_learning_registry.py | imports_from | forja_n4_common.py | EXTRACTED | forja_learning_registry.py:20 |
| forja_learning_registry.py::_load | calls | forja_n3_common.py::read_json | EXTRACTED | forja_learning_registry.py:27 |
| forja_learning_registry.py::register_promoted_rule | calls | forja_n3_common.py::canonical_hash | EXTRACTED | forja_learning_registry.py:68 |
| forja_learning_registry.py::register_promoted_rule | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_learning_registry.py:63 |
| forja_learning_registry.py::register_promoted_rule | calls | forja_n3_common.py::InterProcessLock | EXTRACTED | forja_learning_registry.py:69 |
| forja_learning_registry.py::register_promoted_rule | calls | forja_learning_registry.py::_load | EXTRACTED | forja_learning_registry.py:70 |
| forja_learning_registry.py::register_promoted_rule | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_learning_registry.py:74 |
| forja_learning_registry.py::register_promoted_rule | calls | forja_n3_common.py::canonical_hash | EXTRACTED | forja_learning_registry.py:75 |
| forja_learning_registry.py::register_promoted_rule | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_learning_registry.py:78 |
| forja_learning_registry.py::active_rules | calls | forja_learning_registry.py::_load | EXTRACTED | forja_learning_registry.py:84 |
| forja_learning_registry.py::suite_learning_findings | calls | forja_learning_registry.py::active_rules | EXTRACTED | forja_learning_registry.py:105 |
| forja_learning_registry.py::suite_learning_findings | calls | forja_n3_common.py::read_json | EXTRACTED | forja_learning_registry.py:101 |
| forja_learning_registry.py::suite_learning_findings | calls | forja_n3_common.py::read_json | EXTRACTED | forja_learning_registry.py:103 |
| forja_learning_registry.py::suite_learning_findings | calls | forja_n4_common.py::issue | EXTRACTED | forja_learning_registry.py:112 |
| forja_ledger_material.py | imports_from | forja_citations.py | EXTRACTED | forja_ledger_material.py:30 |
| forja_ledger_material.py | imports_from | forja_citations.py | EXTRACTED | forja_ledger_material.py:30 |
| forja_ledger_material.py | imports_from | forja_citations.py | EXTRACTED | forja_ledger_material.py:30 |
| forja_ledger_material.py | imports_from | forja_mutation_semantic.py | EXTRACTED | forja_ledger_material.py:31 |
| forja_ledger_material.py | imports_from | forja_mutation_semantic.py | EXTRACTED | forja_ledger_material.py:31 |
| forja_ledger_material.py::montar | calls | forja_ledger_material.py::_source_ledger | EXTRACTED | forja_ledger_material.py:89 |
| forja_ledger_material.py::montar | calls | forja_citations.py::extrair_citacoes | EXTRACTED | forja_ledger_material.py:100 |
| forja_ledger_material.py::montar | calls | forja_ledger_material.py::_parse_proposicoes | EXTRACTED | forja_ledger_material.py:136 |
| forja_ledger_material.py::montar | calls | forja_citations.py::procurar_cache_oficial | EXTRACTED | forja_ledger_material.py:102 |
| forja_ledger_material.py::montar | calls | forja_ledger_material.py::_casar_source_ledger | EXTRACTED | forja_ledger_material.py:111 |
| forja_ledger_material.py::montar | calls | forja_citations.py::procurar_fonte_local | EXTRACTED | forja_ledger_material.py:107 |
| forja_ledger_material.py::main | calls | forja_mutation_semantic.py::_achar_caso | EXTRACTED | forja_ledger_material.py:173 |
| forja_ledger_material.py::main | calls | forja_ledger_material.py::montar | EXTRACTED | forja_ledger_material.py:179 |
| forja_ledger_material.py::main | calls | forja_mutation_semantic.py::_achar_draft | EXTRACTED | forja_ledger_material.py:174 |
| forja_legal_search.py::_sanitize | calls | forja_legal_search.py::_sanitize | EXTRACTED | forja_legal_search.py:53 |
| forja_legal_search.py::_sanitize | calls | forja_legal_search.py::_sanitize | EXTRACTED | forja_legal_search.py:49 |
| forja_legal_search.py::load_config | calls | forja_legal_search.py::LegalSearchError | EXTRACTED | forja_legal_search.py:63 |
| forja_legal_search.py::load_config | calls | forja_legal_search.py::LegalSearchError | EXTRACTED | forja_legal_search.py:61 |
| forja_legal_search.py::TeiaJusBridge.__init__ | calls | forja_legal_search.py::load_config | EXTRACTED | forja_legal_search.py:75 |
| forja_legal_search.py::TeiaJusBridge.__init__ | calls | forja_legal_search.py::LegalSearchError | EXTRACTED | forja_legal_search.py:87 |
| forja_legal_search.py::TeiaJusBridge.execute | calls | forja_legal_search.py::_now | EXTRACTED | forja_legal_search.py:134 |
| forja_legal_search.py::TeiaJusBridge.execute | calls | forja_legal_search.py::_atomic_write_json | EXTRACTED | forja_legal_search.py:186 |
| forja_legal_search.py::TeiaJusBridge.execute | calls | forja_legal_search.py::LegalSearchError | EXTRACTED | forja_legal_search.py:117 |
| forja_legal_search.py::TeiaJusBridge.execute | calls | forja_legal_search.py::LegalSearchError | EXTRACTED | forja_legal_search.py:119 |
| forja_legal_search.py::TeiaJusBridge.execute | calls | forja_legal_search.py::LegalSearchError | EXTRACTED | forja_legal_search.py:121 |
| forja_legal_search.py::TeiaJusBridge.execute | calls | forja_legal_search.py::_now | EXTRACTED | forja_legal_search.py:170 |
| forja_legal_search.py::TeiaJusBridge.execute | calls | forja_legal_search.py::_sanitize | EXTRACTED | forja_legal_search.py:174 |
| forja_legal_search.py::TeiaJusBridge.execute | calls | forja_legal_search.py::_canonical_hash | EXTRACTED | forja_legal_search.py:175 |
| forja_legal_search.py::TeiaJusBridge.execute | calls | forja_legal_search.py::_canonical_hash | EXTRACTED | forja_legal_search.py:178 |
| forja_legal_search.py::TeiaJusBridge.execute | calls | forja_legal_search.py::_atomic_write_json | EXTRACTED | forja_legal_search.py:209 |
| forja_legal_search.py::TeiaJusBridge.execute | calls | forja_legal_search.py::LegalSearchError | EXTRACTED | forja_legal_search.py:214 |
| forja_legal_search.py::TeiaJusBridge.execute | calls | forja_legal_search.py::_sanitize | EXTRACTED | forja_legal_search.py:181 |
| forja_legal_search.py::TeiaJusBridge.execute | calls | forja_legal_search.py::_now | EXTRACTED | forja_legal_search.py:201 |
| forja_legal_search.py::TeiaJusBridge.execute | calls | forja_legal_search.py::_sanitize | EXTRACTED | forja_legal_search.py:204 |
| forja_legal_search.py::main | calls | forja_legal_search.py::TeiaJusBridge | EXTRACTED | forja_legal_search.py:289 |
| forja_legal_search.py::main | calls | forja_legal_search.py::_common_parser | EXTRACTED | forja_legal_search.py:288 |
| forja_legal_search.py::main | calls | forja_legal_search.py::LegalSearchError | EXTRACTED | forja_legal_search.py:362 |
| forja_local_context.py::_caso | calls | forja_local_context.py::_ts | EXTRACTED | forja_local_context.py:49 |
| forja_local_context.py::_caso | calls | forja_local_context.py::_fase | EXTRACTED | forja_local_context.py:43 |
| forja_local_context.py::_caso | calls | forja_local_context.py::_fase | EXTRACTED | forja_local_context.py:47 |
| forja_local_context.py::main | calls | forja_local_context.py::_caso | EXTRACTED | forja_local_context.py:70 |
| forja_management_bridge.py | imports_from | forja_n3_common.py | EXTRACTED | forja_management_bridge.py:12 |
| forja_management_bridge.py | imports_from | forja_n3_common.py | EXTRACTED | forja_management_bridge.py:12 |
| forja_management_bridge.py | imports_from | forja_n3_common.py | EXTRACTED | forja_management_bridge.py:12 |
| forja_management_bridge.py | imports_from | forja_n3_common.py | EXTRACTED | forja_management_bridge.py:12 |
| forja_management_bridge.py | imports_from | forja_n3_common.py | EXTRACTED | forja_management_bridge.py:12 |
| forja_management_bridge.py::sync_after_event | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_management_bridge.py:53 |
| forja_management_bridge.py::sync_after_event | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_management_bridge.py:29 |
| forja_management_bridge.py::sync_after_event | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_management_bridge.py:33 |
| forja_management_bridge.py::sync_after_event | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_management_bridge.py:27 |
| forja_management_bridge.py::sync_after_event | calls | forja_n3_common.py::feature_enabled | EXTRACTED | forja_management_bridge.py:31 |
| forja_management_bridge.py::sync_after_event | calls | forja_n3_common.py::feature_enabled | EXTRACTED | forja_management_bridge.py:31 |
| forja_management_bridge.py::sync_after_event | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_management_bridge.py:32 |
| forja_management_bridge.py::sync_after_event | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_management_bridge.py:44 |
| forja_management_bridge.py::sync_after_event | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_management_bridge.py:51 |
| forja_memoria_auditabilidade.py::_state | calls | forja_memoria_auditabilidade.py::_state_path | EXTRACTED | forja_memoria_auditabilidade.py:131 |
| forja_memoria_auditabilidade.py::_state | calls | forja_memoria_auditabilidade.py::_read_json | EXTRACTED | forja_memoria_auditabilidade.py:132 |
| forja_memoria_auditabilidade.py::_artifact_inventory | calls | forja_memoria_auditabilidade.py::_redact | EXTRACTED | forja_memoria_auditabilidade.py:168 |
| forja_memoria_auditabilidade.py::_artifact_inventory | calls | forja_memoria_auditabilidade.py::_redact | EXTRACTED | forja_memoria_auditabilidade.py:169 |
| forja_memoria_auditabilidade.py::_artifact_inventory | calls | forja_memoria_auditabilidade.py::sha256_file | EXTRACTED | forja_memoria_auditabilidade.py:181 |
| forja_memoria_auditabilidade.py::_artifact_inventory | calls | forja_memoria_auditabilidade.py::sha256_file | EXTRACTED | forja_memoria_auditabilidade.py:194 |
| forja_memoria_auditabilidade.py::_artifact_inventory | calls | forja_memoria_auditabilidade.py::_relative | EXTRACTED | forja_memoria_auditabilidade.py:184 |
| forja_memoria_auditabilidade.py::_artifact_inventory | calls | forja_memoria_auditabilidade.py::_relative | EXTRACTED | forja_memoria_auditabilidade.py:197 |
| forja_memoria_auditabilidade.py::_summary_for_control | calls | forja_memoria_auditabilidade.py::_relative | EXTRACTED | forja_memoria_auditabilidade.py:224 |
| forja_memoria_auditabilidade.py::_summary_for_control | calls | forja_memoria_auditabilidade.py::sha256_file | EXTRACTED | forja_memoria_auditabilidade.py:225 |
| forja_memoria_auditabilidade.py::_summary_for_control | calls | forja_memoria_auditabilidade.py::_read_json | EXTRACTED | forja_memoria_auditabilidade.py:229 |
| forja_memoria_auditabilidade.py::_source_summary | calls | forja_memoria_auditabilidade.py::_read_json | EXTRACTED | forja_memoria_auditabilidade.py:251 |
| forja_memoria_auditabilidade.py::_source_summary | calls | forja_memoria_auditabilidade.py::_relative | EXTRACTED | forja_memoria_auditabilidade.py:265 |
| forja_memoria_auditabilidade.py::_source_summary | calls | forja_memoria_auditabilidade.py::sha256_file | EXTRACTED | forja_memoria_auditabilidade.py:266 |
| forja_memoria_auditabilidade.py::build_payload | calls | forja_memoria_auditabilidade.py::_state | EXTRACTED | forja_memoria_auditabilidade.py:290 |
| forja_memoria_auditabilidade.py::build_payload | calls | forja_memoria_auditabilidade.py::_summary_for_control | EXTRACTED | forja_memoria_auditabilidade.py:294 |
| forja_memoria_auditabilidade.py::build_payload | calls | forja_memoria_auditabilidade.py::_canonical_phase | EXTRACTED | forja_memoria_auditabilidade.py:299 |
| forja_memoria_auditabilidade.py::build_payload | calls | forja_memoria_auditabilidade.py::_artifact_inventory | EXTRACTED | forja_memoria_auditabilidade.py:340 |
| forja_memoria_auditabilidade.py::build_payload | calls | forja_memoria_auditabilidade.py::_source_summary | EXTRACTED | forja_memoria_auditabilidade.py:342 |
| forja_memoria_auditabilidade.py::build_payload | calls | forja_memoria_auditabilidade.py::_visual_summary | EXTRACTED | forja_memoria_auditabilidade.py:343 |
| forja_memoria_auditabilidade.py::build_payload | calls | forja_memoria_auditabilidade.py::_control_files | EXTRACTED | forja_memoria_auditabilidade.py:294 |
| forja_memoria_auditabilidade.py::build_payload | calls | forja_memoria_auditabilidade.py::_phase_status | EXTRACTED | forja_memoria_auditabilidade.py:309 |
| forja_memoria_auditabilidade.py::build_payload | calls | forja_memoria_auditabilidade.py::_relative | EXTRACTED | forja_memoria_auditabilidade.py:321 |
| forja_memoria_auditabilidade.py::build_payload | calls | forja_memoria_auditabilidade.py::sha256_file | EXTRACTED | forja_memoria_auditabilidade.py:322 |
| forja_memoria_auditabilidade.py::build_payload | calls | forja_memoria_auditabilidade.py::_canonical_phase | EXTRACTED | forja_memoria_auditabilidade.py:324 |
| forja_memoria_auditabilidade.py::build_payload | calls | forja_memoria_auditabilidade.py::_redact | EXTRACTED | forja_memoria_auditabilidade.py:346 |
| forja_memoria_auditabilidade.py::build_payload | calls | forja_memoria_auditabilidade.py::_redact | EXTRACTED | forja_memoria_auditabilidade.py:345 |
| forja_memoria_auditabilidade.py::build_payload | calls | forja_memoria_auditabilidade.py::_redact | EXTRACTED | forja_memoria_auditabilidade.py:304 |
| forja_memoria_auditabilidade.py::build_payload | calls | forja_memoria_auditabilidade.py::_redact | EXTRACTED | forja_memoria_auditabilidade.py:305 |
| forja_memoria_auditabilidade.py::build_bundle | calls | forja_memoria_auditabilidade.py::build_payload | EXTRACTED | forja_memoria_auditabilidade.py:465 |
| forja_memoria_auditabilidade.py::build_bundle | calls | forja_memoria_auditabilidade.py::_write_text | EXTRACTED | forja_memoria_auditabilidade.py:470 |
| forja_memoria_auditabilidade.py::build_bundle | calls | forja_memoria_auditabilidade.py::sha256_file | EXTRACTED | forja_memoria_auditabilidade.py:471 |
| forja_memoria_auditabilidade.py::build_bundle | calls | forja_memoria_auditabilidade.py::_md | EXTRACTED | forja_memoria_auditabilidade.py:472 |
| forja_memoria_auditabilidade.py::build_bundle | calls | forja_memoria_auditabilidade.py::_html_document | EXTRACTED | forja_memoria_auditabilidade.py:473 |
| forja_memoria_auditabilidade.py::build_bundle | calls | forja_memoria_auditabilidade.py::_write_text | EXTRACTED | forja_memoria_auditabilidade.py:474 |
| forja_memoria_auditabilidade.py::build_bundle | calls | forja_memoria_auditabilidade.py::_write_text | EXTRACTED | forja_memoria_auditabilidade.py:475 |
| forja_memoria_auditabilidade.py::validate_bundle | calls | forja_memoria_auditabilidade.py::_read_json | EXTRACTED | forja_memoria_auditabilidade.py:492 |
| forja_memoria_auditabilidade.py::validate_bundle | calls | forja_memoria_auditabilidade.py::sha256_file | EXTRACTED | forja_memoria_auditabilidade.py:499 |
| forja_memoria_auditabilidade.py::validate_bundle | calls | forja_memoria_auditabilidade.py::_state_path | EXTRACTED | forja_memoria_auditabilidade.py:517 |
| forja_memoria_auditabilidade.py::validate_bundle | calls | forja_memoria_auditabilidade.py::sha256_file | EXTRACTED | forja_memoria_auditabilidade.py:518 |
| forja_memoria_auditabilidade.py::main | calls | forja_memoria_auditabilidade.py::build_bundle | EXTRACTED | forja_memoria_auditabilidade.py:540 |
| forja_memoria_auditabilidade.py::main | calls | forja_memoria_auditabilidade.py::validate_bundle | EXTRACTED | forja_memoria_auditabilidade.py:542 |
| forja_metacognition.py | imports_from | forja_n3_common.py | EXTRACTED | forja_metacognition.py:9 |
| forja_metacognition.py | imports_from | forja_n4_common.py | EXTRACTED | forja_metacognition.py:10 |
| forja_metacognition.py | imports_from | forja_n4_common.py | EXTRACTED | forja_metacognition.py:10 |
| forja_metacognition.py | imports_from | forja_n4_common.py | EXTRACTED | forja_metacognition.py:10 |
| forja_metacognition.py::validate_metacognition | calls | forja_n4_common.py::ids_unique | EXTRACTED | forja_metacognition.py:15 |
| forja_metacognition.py::validate_metacognition | calls | forja_n4_common.py::issue | EXTRACTED | forja_metacognition.py:37 |
| forja_metacognition.py::validate_metacognition | calls | forja_n4_common.py::issue | EXTRACTED | forja_metacognition.py:39 |
| forja_metacognition.py::validate_metacognition | calls | forja_n4_common.py::issue | EXTRACTED | forja_metacognition.py:20 |
| forja_metacognition.py::validate_metacognition | calls | forja_n4_common.py::issue | EXTRACTED | forja_metacognition.py:22 |
| forja_metacognition.py::validate_metacognition | calls | forja_n4_common.py::issue | EXTRACTED | forja_metacognition.py:24 |
| forja_metacognition.py::validate_metacognition | calls | forja_n4_common.py::issue | EXTRACTED | forja_metacognition.py:31 |
| forja_metacognition.py::validate_metacognition | calls | forja_n4_common.py::issue | EXTRACTED | forja_metacognition.py:35 |
| forja_metacognition.py::validate_metacognition | calls | forja_n4_common.py::issue | EXTRACTED | forja_metacognition.py:28 |
| forja_metacognition.py::validate_case | calls | forja_n4_common.py::validate_file | EXTRACTED | forja_metacognition.py:44 |
| forja_metacognition.py::main | calls | forja_metacognition.py::validate_case | EXTRACTED | forja_metacognition.py:52 |
| forja_metacognition.py::main | calls | forja_n3_common.py::resolve_case_dir | EXTRACTED | forja_metacognition.py:52 |
| forja_metadata.py::sanitize_docx | calls | forja_metadata.py::retry_transient_io | EXTRACTED | forja_metadata.py:83 |
| forja_metadata.py::sanitize_docx | calls | forja_metadata.py::_replace_core_text | EXTRACTED | forja_metadata.py:76 |
| forja_metadata.py::sanitize_docx | calls | forja_metadata.py::_replace_core_text | EXTRACTED | forja_metadata.py:77 |
| forja_metadata.py::sanitize_pdf | calls | forja_metadata.py::retry_transient_io | EXTRACTED | forja_metadata.py:105 |
| forja_metadata.py::sanitize_final_artifacts | calls | forja_metadata.py::sanitize_docx | EXTRACTED | forja_metadata.py:109 |
| forja_metadata.py::sanitize_final_artifacts | calls | forja_metadata.py::sanitize_pdf | EXTRACTED | forja_metadata.py:110 |
| forja_metricas_f7.py | imports_from | forja_authorities.py | EXTRACTED | forja_metricas_f7.py:25 |
| forja_metricas_f7.py | imports_from | forja_official_sources.py | EXTRACTED | forja_metricas_f7.py:42 |
| forja_metricas_f7.py::extrair_citacoes_basico | calls | forja_authorities.py::extract_authorities | EXTRACTED | forja_metricas_f7.py:28 |
| forja_metricas_f7.py::cache_com_lastro | calls | forja_official_sources.py::validate_cached_source | EXTRACTED | forja_metricas_f7.py:47 |
| forja_metricas_f7.py::procurar_em_cache_oficial | calls | forja_metricas_f7.py::cache_com_lastro | EXTRACTED | forja_metricas_f7.py:88 |
| forja_metricas_f7.py::metricas_f7 | calls | forja_metricas_f7.py::extrair_citacoes_basico | EXTRACTED | forja_metricas_f7.py:122 |
| forja_metricas_f7.py::metricas_f7 | calls | forja_metricas_f7.py::extrair_marcadores_verificar | EXTRACTED | forja_metricas_f7.py:144 |
| forja_metricas_f7.py::metricas_f7 | calls | forja_metricas_f7.py::procurar_em_cache_oficial | EXTRACTED | forja_metricas_f7.py:129 |
| forja_metricas_gates.py::coletar | calls | forja_metricas_gates.py::_ler | EXTRACTED | forja_metricas_gates.py:63 |
| forja_metricas_gates.py::coletar | calls | forja_metricas_gates.py::_ler | EXTRACTED | forja_metricas_gates.py:64 |
| forja_metricas_gates.py::coletar | calls | forja_metricas_gates.py::_fase | EXTRACTED | forja_metricas_gates.py:102 |
| forja_metricas_gates.py::coletar | calls | forja_metricas_gates.py::_ts | EXTRACTED | forja_metricas_gates.py:102 |
| forja_metricas_gates.py::main | calls | forja_metricas_gates.py::coletar | EXTRACTED | forja_metricas_gates.py:129 |
| forja_modelos.py::_confirmar_modelo_reportado | calls | forja_modelos.py::modelo_remoto_proibido | EXTRACTED | forja_modelos.py:169 |
| forja_modelos.py::_confirmar_modelo_reportado | calls | forja_modelos.py::ForjaModeloError | EXTRACTED | forja_modelos.py:170 |
| forja_modelos.py::_segredo | calls | forja_modelos.py::ForjaModeloError | EXTRACTED | forja_modelos.py:201 |
| forja_modelos.py::_segredo | calls | forja_modelos.py::ForjaModeloError | EXTRACTED | forja_modelos.py:195 |
| forja_modelos.py::_post | calls | forja_modelos.py::ForjaModeloError | EXTRACTED | forja_modelos.py:219 |
| forja_modelos.py::_post | calls | forja_modelos.py::ForjaModeloError | EXTRACTED | forja_modelos.py:221 |
| forja_modelos.py::_openrouter | calls | forja_modelos.py::_post | EXTRACTED | forja_modelos.py:228 |
| forja_modelos.py::_openrouter | calls | forja_modelos.py::_confirmar_modelo_reportado | EXTRACTED | forja_modelos.py:235 |
| forja_modelos.py::_openrouter | calls | forja_modelos.py::_segredo | EXTRACTED | forja_modelos.py:230 |
| forja_modelos.py::chamar | calls | forja_modelos.py::custo_usd | EXTRACTED | forja_modelos.py:281 |
| forja_modelos.py::chamar | calls | forja_modelos.py::ForjaModeloError | EXTRACTED | forja_modelos.py:269 |
| forja_modelos.py::chamar | calls | forja_modelos.py::modelo_remoto_proibido | EXTRACTED | forja_modelos.py:270 |
| forja_modelos.py::chamar | calls | forja_modelos.py::ForjaModeloError | EXTRACTED | forja_modelos.py:271 |
| forja_modelos.py::chamar | calls | forja_modelos.py::ForjaModeloError | EXTRACTED | forja_modelos.py:273 |
| forja_modelos.py::chamar | calls | forja_modelos.py::ForjaModeloError | EXTRACTED | forja_modelos.py:283 |
| forja_modelos.py::chamar | calls | forja_modelos.py::ForjaModeloError | EXTRACTED | forja_modelos.py:287 |
| forja_modelos.py::chamar | calls | forja_modelos.py::ForjaModeloError | EXTRACTED | forja_modelos.py:296 |
| forja_modelos.py::chamar | calls | forja_modelos.py::registrar_no_ledger | EXTRACTED | forja_modelos.py:313 |
| forja_modelos.py::chamar | calls | forja_modelos.py::custo_usd | EXTRACTED | forja_modelos.py:305 |
| forja_modelos.py::familia_de | calls | forja_modelos.py::ForjaModeloError | EXTRACTED | forja_modelos.py:329 |
| forja_modelos.py::revisores_de | calls | forja_modelos.py::familia_de | EXTRACTED | forja_modelos.py:339 |
| forja_modelos.py::main | calls | forja_modelos.py::chamar | EXTRACTED | forja_modelos.py:398 |
| forja_modelos.py::main | calls | forja_modelos.py::gasto_acumulado | EXTRACTED | forja_modelos.py:396 |
| forja_mutation_semantic.py | imports_from | forja_case_tests.py | EXTRACTED | forja_mutation_semantic.py:38 |
| forja_mutation_semantic.py | imports_from | forja_verificador.py | EXTRACTED | forja_mutation_semantic.py:39 |
| forja_mutation_semantic.py::_aplicar | calls | forja_mutation_semantic.py::_ano_mais_um | EXTRACTED | forja_mutation_semantic.py:145 |
| forja_mutation_semantic.py::_p0_por_gate | calls | forja_verificador.py::verificar | EXTRACTED | forja_mutation_semantic.py:161 |
| forja_mutation_semantic.py::_suite_mata | calls | forja_case_tests.py::_deterministic | EXTRACTED | forja_mutation_semantic.py:173 |
| forja_mutation_semantic.py::rodar | calls | forja_mutation_semantic.py::_p0_por_gate | EXTRACTED | forja_mutation_semantic.py:181 |
| forja_mutation_semantic.py::rodar | calls | forja_mutation_semantic.py::_suite_mata | EXTRACTED | forja_mutation_semantic.py:186 |
| forja_mutation_semantic.py::rodar | calls | forja_mutation_semantic.py::_suite_mata | EXTRACTED | forja_mutation_semantic.py:192 |
| forja_mutation_semantic.py::rodar | calls | forja_mutation_semantic.py::_p0_por_gate | EXTRACTED | forja_mutation_semantic.py:195 |
| forja_mutation_semantic.py::rodar | calls | forja_mutation_semantic.py::_aplicar | EXTRACTED | forja_mutation_semantic.py:224 |
| forja_mutation_semantic.py::rodar | calls | forja_mutation_semantic.py::_aplicar | EXTRACTED | forja_mutation_semantic.py:206 |
| forja_mutation_semantic.py::main | calls | forja_mutation_semantic.py::_achar_caso | EXTRACTED | forja_mutation_semantic.py:292 |
| forja_mutation_semantic.py::main | calls | forja_mutation_semantic.py::rodar | EXTRACTED | forja_mutation_semantic.py:301 |
| forja_mutation_semantic.py::main | calls | forja_mutation_semantic.py::_achar_draft | EXTRACTED | forja_mutation_semantic.py:293 |
| forja_n3_common.py::resolve_name | calls | forja_n3_common.py::name_with_legacy | EXTRACTED | forja_n3_common.py:50 |
| forja_n3_common.py::atomic_write_json | calls | forja_n3_common.py::atomic_write_text | EXTRACTED | forja_n3_common.py:102 |
| forja_n3_common.py::canonical_hash | calls | forja_n3_common.py::sha256_bytes | EXTRACTED | forja_n3_common.py:119 |
| forja_n3_common.py::load_config | calls | forja_n3_common.py::read_json | EXTRACTED | forja_n3_common.py:123 |
| forja_n3_common.py::load_config | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_n3_common.py:125 |
| forja_n3_common.py::feature_enabled | calls | forja_n3_common.py::load_config | EXTRACTED | forja_n3_common.py:130 |
| forja_n3_common.py::resolve_case_dir | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_n3_common.py:146 |
| forja_n3_common.py::resolve_case_dir | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_n3_common.py:139 |
| forja_n3_common.py::ensure_within | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_n3_common.py:154 |
| forja_n3_common.py::InterProcessLock.__init__ | calls | forja_n3_common.py::new_id | EXTRACTED | forja_n3_common.py:177 |
| forja_n3_common.py::InterProcessLock._can_reclaim | calls | forja_n3_common.py::read_json | EXTRACTED | forja_n3_common.py:181 |
| forja_n3_common.py::InterProcessLock._can_reclaim | calls | forja_n3_common.py::_pid_alive | EXTRACTED | forja_n3_common.py:183 |
| forja_n3_common.py::InterProcessLock.__enter__ | calls | forja_n3_common.py::InterProcessLock._can_reclaim | EXTRACTED | forja_n3_common.py:199 |
| forja_n3_common.py::InterProcessLock.__enter__ | calls | forja_n3_common.py::LockTimeout | EXTRACTED | forja_n3_common.py:206 |
| forja_n3_common.py::InterProcessLock.__enter__ | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_n3_common.py:194 |
| forja_n3_common.py::InterProcessLock.__exit__ | calls | forja_n3_common.py::read_json | EXTRACTED | forja_n3_common.py:211 |
| forja_n3_shadow_replay.py | imports_from | forja_n3_common.py | EXTRACTED | forja_n3_shadow_replay.py:13 |
| forja_n3_shadow_replay.py | imports_from | forja_n3_common.py | EXTRACTED | forja_n3_shadow_replay.py:13 |
| forja_n3_shadow_replay.py | imports_from | forja_n3_common.py | EXTRACTED | forja_n3_shadow_replay.py:13 |
| forja_n3_shadow_replay.py | imports_from | forja_n3_common.py | EXTRACTED | forja_n3_shadow_replay.py:13 |
| forja_n3_shadow_replay.py | imports_from | forja_n3_common.py | EXTRACTED | forja_n3_shadow_replay.py:13 |
| forja_n3_shadow_replay.py | imports_from | forja_n3_common.py | EXTRACTED | forja_n3_shadow_replay.py:13 |
| forja_n3_shadow_replay.py | imports_from | forja_n3_common.py | EXTRACTED | forja_n3_shadow_replay.py:13 |
| forja_n3_shadow_replay.py | imports_from | forja_state_machine.py | EXTRACTED | forja_n3_shadow_replay.py:14 |
| forja_n3_shadow_replay.py | imports_from | forja_state_machine.py | EXTRACTED | forja_n3_shadow_replay.py:14 |
| forja_n3_shadow_replay.py::_phase_regressions | calls | forja_n3_shadow_replay.py::_phase_number | EXTRACTED | forja_n3_shadow_replay.py:41 |
| forja_n3_shadow_replay.py::_artifact_audit | calls | forja_n3_shadow_replay.py::_artifact_candidates | EXTRACTED | forja_n3_shadow_replay.py:70 |
| forja_n3_shadow_replay.py::_artifact_audit | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_n3_shadow_replay.py:73 |
| forja_n3_shadow_replay.py::_visual_audit | calls | forja_n3_shadow_replay.py::_visual_roots | EXTRACTED | forja_n3_shadow_replay.py:101 |
| forja_n3_shadow_replay.py::replay_case | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_n3_shadow_replay.py:115 |
| forja_n3_shadow_replay.py::replay_case | calls | forja_n3_common.py::read_json | EXTRACTED | forja_n3_shadow_replay.py:116 |
| forja_n3_shadow_replay.py::replay_case | calls | forja_n3_shadow_replay.py::_phase_regressions | EXTRACTED | forja_n3_shadow_replay.py:131 |
| forja_n3_shadow_replay.py::replay_case | calls | forja_n3_shadow_replay.py::_artifact_audit | EXTRACTED | forja_n3_shadow_replay.py:132 |
| forja_n3_shadow_replay.py::replay_case | calls | forja_n3_shadow_replay.py::_json_audit | EXTRACTED | forja_n3_shadow_replay.py:133 |
| forja_n3_shadow_replay.py::replay_case | calls | forja_n3_shadow_replay.py::_visual_audit | EXTRACTED | forja_n3_shadow_replay.py:141 |
| forja_n3_shadow_replay.py::replay_case | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_n3_shadow_replay.py:155 |
| forja_n3_shadow_replay.py::replay_case | calls | forja_state_machine.py::initialize_case | EXTRACTED | forja_n3_shadow_replay.py:123 |
| forja_n3_shadow_replay.py::replay_case | calls | forja_state_machine.py::derive_state | EXTRACTED | forja_n3_shadow_replay.py:124 |
| forja_n3_shadow_replay.py::run_replay | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_n3_shadow_replay.py:250 |
| forja_n3_shadow_replay.py::run_replay | calls | forja_n3_common.py::atomic_write_text | EXTRACTED | forja_n3_shadow_replay.py:251 |
| forja_n3_shadow_replay.py::run_replay | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_n3_shadow_replay.py:244 |
| forja_n3_shadow_replay.py::run_replay | calls | forja_n3_shadow_replay.py::_render_markdown | EXTRACTED | forja_n3_shadow_replay.py:251 |
| forja_n3_shadow_replay.py::run_replay | calls | forja_n3_shadow_replay.py::replay_case | EXTRACTED | forja_n3_shadow_replay.py:230 |
| forja_n3_shadow_replay.py::main | calls | forja_n3_shadow_replay.py::run_replay | EXTRACTED | forja_n3_shadow_replay.py:261 |
| forja_n4_anti_fraud_audit.py | imports_from | forja_n3_common.py | EXTRACTED | forja_n4_anti_fraud_audit.py:10 |
| forja_n4_anti_fraud_audit.py | imports_from | forja_n3_common.py | EXTRACTED | forja_n4_anti_fraud_audit.py:10 |
| forja_n4_anti_fraud_audit.py | imports_from | forja_n3_common.py | EXTRACTED | forja_n4_anti_fraud_audit.py:10 |
| forja_n4_anti_fraud_audit.py | imports_from | forja_n3_common.py | EXTRACTED | forja_n4_anti_fraud_audit.py:10 |
| forja_n4_anti_fraud_audit.py | imports_from | forja_n3_common.py | EXTRACTED | forja_n4_anti_fraud_audit.py:10 |
| forja_n4_anti_fraud_audit.py | imports_from | forja_n4_e2e_adversarial.py | EXTRACTED | forja_n4_anti_fraud_audit.py:11 |
| forja_n4_anti_fraud_audit.py::_snapshot | calls | forja_n3_common.py::read_json | EXTRACTED | forja_n4_anti_fraud_audit.py:24 |
| forja_n4_anti_fraud_audit.py::_snapshot | calls | forja_n3_common.py::read_json | EXTRACTED | forja_n4_anti_fraud_audit.py:26 |
| forja_n4_anti_fraud_audit.py::_snapshot | calls | forja_n3_common.py::read_json | EXTRACTED | forja_n4_anti_fraud_audit.py:31 |
| forja_n4_anti_fraud_audit.py::_snapshot | calls | forja_n3_common.py::read_json | EXTRACTED | forja_n4_anti_fraud_audit.py:32 |
| forja_n4_anti_fraud_audit.py::_snapshot | calls | forja_n3_common.py::read_json | EXTRACTED | forja_n4_anti_fraud_audit.py:33 |
| forja_n4_anti_fraud_audit.py::evaluate | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_n4_anti_fraud_audit.py:55 |
| forja_n4_anti_fraud_audit.py::run | calls | forja_n4_e2e_adversarial.py::run | EXTRACTED | forja_n4_anti_fraud_audit.py:151 |
| forja_n4_anti_fraud_audit.py::run | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_n4_anti_fraud_audit.py:187 |
| forja_n4_anti_fraud_audit.py::run | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_n4_anti_fraud_audit.py:189 |
| forja_n4_anti_fraud_audit.py::run | calls | forja_n3_common.py::read_json | EXTRACTED | forja_n4_anti_fraud_audit.py:107 |
| forja_n4_anti_fraud_audit.py::run | calls | forja_n4_anti_fraud_audit.py::_snapshot | EXTRACTED | forja_n4_anti_fraud_audit.py:108 |
| forja_n4_anti_fraud_audit.py::run | calls | forja_n4_anti_fraud_audit.py::evaluate | EXTRACTED | forja_n4_anti_fraud_audit.py:138 |
| forja_n4_anti_fraud_audit.py::run | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_n4_anti_fraud_audit.py:162 |
| forja_n4_baseline.py | imports_from | forja_n3_common.py | EXTRACTED | forja_n4_baseline.py:13 |
| forja_n4_baseline.py | imports_from | forja_n3_common.py | EXTRACTED | forja_n4_baseline.py:13 |
| forja_n4_baseline.py | imports_from | forja_n3_common.py | EXTRACTED | forja_n4_baseline.py:13 |
| forja_n4_baseline.py | imports_from | forja_n3_common.py | EXTRACTED | forja_n4_baseline.py:13 |
| forja_n4_baseline.py | imports_from | forja_n3_common.py | EXTRACTED | forja_n4_baseline.py:13 |
| forja_n4_baseline.py | imports_from | forja_n4_validate.py | EXTRACTED | forja_n4_baseline.py:14 |
| forja_n4_baseline.py | imports_from | forja_state_machine.py | EXTRACTED | forja_n4_baseline.py:15 |
| forja_n4_baseline.py::_protected | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_n4_baseline.py:28 |
| forja_n4_baseline.py::run | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_n4_baseline.py:69 |
| forja_n4_baseline.py::run | calls | forja_n4_baseline.py::_protected | EXTRACTED | forja_n4_baseline.py:35 |
| forja_n4_baseline.py::run | calls | forja_n4_validate.py::validate_case | EXTRACTED | forja_n4_baseline.py:40 |
| forja_n4_baseline.py::run | calls | forja_n4_baseline.py::_protected | EXTRACTED | forja_n4_baseline.py:41 |
| forja_n4_baseline.py::run | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_n4_baseline.py:60 |
| forja_n4_baseline.py::run | calls | forja_state_machine.py::initialize_case | EXTRACTED | forja_n4_baseline.py:38 |
| forja_n4_baseline.py::run | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_n4_baseline.py:67 |
| forja_n4_baseline.py::main | calls | forja_n4_baseline.py::run | EXTRACTED | forja_n4_baseline.py:78 |
| forja_n4_common.py | imports_from | forja_n3_common.py | EXTRACTED | forja_n4_common.py:12 |
| forja_n4_common.py | imports_from | forja_n3_common.py | EXTRACTED | forja_n4_common.py:12 |
| forja_n4_common.py | imports_from | forja_n3_common.py | EXTRACTED | forja_n4_common.py:12 |
| forja_n4_common.py | imports_from | forja_n3_common.py | EXTRACTED | forja_n4_common.py:12 |
| forja_n4_common.py | imports_from | forja_n3_common.py | EXTRACTED | forja_n4_common.py:12 |
| forja_n4_common.py | imports_from | forja_n3_common.py | EXTRACTED | forja_n4_common.py:12 |
| forja_n4_common.py::expected_content_hash | calls | forja_n3_common.py::canonical_hash | EXTRACTED | forja_n4_common.py:111 |
| forja_n4_common.py::expected_content_hash | calls | forja_n4_common.py::semantic_payload | EXTRACTED | forja_n4_common.py:111 |
| forja_n4_common.py::artifact_path | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_n4_common.py:116 |
| forja_n4_common.py::build_envelope | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_n4_common.py:132 |
| forja_n4_common.py::build_envelope | calls | forja_n4_common.py::expected_content_hash | EXTRACTED | forja_n4_common.py:154 |
| forja_n4_common.py::build_envelope | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_n4_common.py:151 |
| forja_n4_common.py::write_artifact | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_n4_common.py:160 |
| forja_n4_common.py::write_artifact | calls | forja_n4_common.py::expected_content_hash | EXTRACTED | forja_n4_common.py:161 |
| forja_n4_common.py::write_artifact | calls | forja_n4_common.py::artifact_path | EXTRACTED | forja_n4_common.py:162 |
| forja_n4_common.py::write_artifact | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_n4_common.py:163 |
| forja_n4_common.py::write_artifact | calls | forja_n4_common.py::append_trace | EXTRACTED | forja_n4_common.py:164 |
| forja_n4_common.py::append_trace | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_n4_common.py:177 |
| forja_n4_common.py::append_trace | calls | forja_n3_common.py::InterProcessLock | EXTRACTED | forja_n4_common.py:178 |
| forja_n4_common.py::validate_envelope | calls | forja_n4_common.py::expected_content_hash | EXTRACTED | forja_n4_common.py:221 |
| forja_n4_common.py::validate_envelope | calls | forja_n4_common.py::issue | EXTRACTED | forja_n4_common.py:189 |
| forja_n4_common.py::validate_envelope | calls | forja_n4_common.py::issue | EXTRACTED | forja_n4_common.py:204 |
| forja_n4_common.py::validate_envelope | calls | forja_n4_common.py::issue | EXTRACTED | forja_n4_common.py:206 |
| forja_n4_common.py::validate_envelope | calls | forja_n4_common.py::issue | EXTRACTED | forja_n4_common.py:208 |
| forja_n4_common.py::validate_envelope | calls | forja_n4_common.py::issue | EXTRACTED | forja_n4_common.py:222 |
| forja_n4_common.py::validate_envelope | calls | forja_n4_common.py::issue | EXTRACTED | forja_n4_common.py:200 |
| forja_n4_common.py::validate_envelope | calls | forja_n4_common.py::issue | EXTRACTED | forja_n4_common.py:211 |
| forja_n4_common.py::validate_envelope | calls | forja_n4_common.py::issue | EXTRACTED | forja_n4_common.py:218 |
| forja_n4_common.py::validate_envelope | calls | forja_n4_common.py::issue | EXTRACTED | forja_n4_common.py:220 |
| forja_n4_common.py::validate_envelope | calls | forja_n4_common.py::issue | EXTRACTED | forja_n4_common.py:215 |
| forja_n4_common.py::load_artifact | calls | forja_n3_common.py::read_json | EXTRACTED | forja_n4_common.py:227 |
| forja_n4_common.py::load_artifact | calls | forja_n4_common.py::artifact_path | EXTRACTED | forja_n4_common.py:227 |
| forja_n4_common.py::validate_file | calls | forja_n4_common.py::load_artifact | EXTRACTED | forja_n4_common.py:235 |
| forja_n4_common.py::validate_file | calls | forja_n4_common.py::validate_envelope | EXTRACTED | forja_n4_common.py:236 |
| forja_n4_common.py::ids_unique | calls | forja_n4_common.py::issue | EXTRACTED | forja_n4_common.py:248 |
| forja_n4_common.py::ids_unique | calls | forja_n4_common.py::issue | EXTRACTED | forja_n4_common.py:250 |
| forja_n4_corpus.py | imports_from | forja_consistency.py | EXTRACTED | forja_n4_corpus.py:8 |
| forja_n4_corpus.py | imports_from | forja_consistency.py | EXTRACTED | forja_n4_corpus.py:8 |
| forja_n4_corpus.py | imports_from | forja_consistency.py | EXTRACTED | forja_n4_corpus.py:8 |
| forja_n4_corpus.py | imports_from | forja_consistency.py | EXTRACTED | forja_n4_corpus.py:8 |
| forja_n4_corpus.py | imports_from | forja_consistency.py | EXTRACTED | forja_n4_corpus.py:8 |
| forja_n4_corpus.py | imports_from | forja_consistency.py | EXTRACTED | forja_n4_corpus.py:8 |
| forja_n4_corpus.py | imports_from | forja_n3_common.py | EXTRACTED | forja_n4_corpus.py:9 |
| forja_n4_corpus.py | imports_from | forja_n3_common.py | EXTRACTED | forja_n4_corpus.py:9 |
| forja_n4_corpus.py | imports_from | forja_n3_common.py | EXTRACTED | forja_n4_corpus.py:9 |
| forja_n4_corpus.py | imports_from | forja_n3_common.py | EXTRACTED | forja_n4_corpus.py:9 |
| forja_n4_corpus.py | imports_from | forja_reasoning.py | EXTRACTED | forja_n4_corpus.py:10 |
| forja_n4_corpus.py | imports_from | forja_science.py | EXTRACTED | forja_n4_corpus.py:11 |
| forja_n4_corpus.py | imports_from | forja_science.py | EXTRACTED | forja_n4_corpus.py:11 |
| forja_n4_corpus.py::run | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_n4_corpus.py:50 |
| forja_n4_corpus.py::run | calls | forja_n3_common.py::read_json | EXTRACTED | forja_n4_corpus.py:29 |
| forja_n4_corpus.py::run | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_n4_corpus.py:41 |
| forja_n4_corpus.py::run | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_n4_corpus.py:48 |
| forja_n4_e2e_adversarial.py | imports_from | forja_case_tests.py | EXTRACTED | forja_n4_e2e_adversarial.py:12 |
| forja_n4_e2e_adversarial.py | imports_from | forja_n4_common.py | EXTRACTED | forja_n4_e2e_adversarial.py:13 |
| forja_n4_e2e_adversarial.py | imports_from | forja_n4_validate.py | EXTRACTED | forja_n4_e2e_adversarial.py:14 |
| forja_n4_e2e_adversarial.py::_save | calls | forja_n4_common.py::expected_content_hash | EXTRACTED | forja_n4_e2e_adversarial.py:27 |
| forja_n4_e2e_adversarial.py::run | calls | forja_n4_e2e_adversarial.py::_copy_case | EXTRACTED | forja_n4_e2e_adversarial.py:46 |
| forja_n4_e2e_adversarial.py::run | calls | forja_n4_validate.py::validate_case | EXTRACTED | forja_n4_e2e_adversarial.py:47 |
| forja_n4_e2e_adversarial.py::run | calls | forja_n4_e2e_adversarial.py::_copy_case | EXTRACTED | forja_n4_e2e_adversarial.py:50 |
| forja_n4_e2e_adversarial.py::run | calls | forja_n4_e2e_adversarial.py::_load | EXTRACTED | forja_n4_e2e_adversarial.py:52 |
| forja_n4_e2e_adversarial.py::run | calls | forja_n4_validate.py::validate_case | EXTRACTED | forja_n4_e2e_adversarial.py:54 |
| forja_n4_e2e_adversarial.py::run | calls | forja_n4_e2e_adversarial.py::_copy_case | EXTRACTED | forja_n4_e2e_adversarial.py:57 |
| forja_n4_e2e_adversarial.py::run | calls | forja_n4_e2e_adversarial.py::_load | EXTRACTED | forja_n4_e2e_adversarial.py:59 |
| forja_n4_e2e_adversarial.py::run | calls | forja_n4_e2e_adversarial.py::_save | EXTRACTED | forja_n4_e2e_adversarial.py:61 |
| forja_n4_e2e_adversarial.py::run | calls | forja_n4_validate.py::validate_case | EXTRACTED | forja_n4_e2e_adversarial.py:62 |
| forja_n4_e2e_adversarial.py::run | calls | forja_n4_e2e_adversarial.py::_codes | EXTRACTED | forja_n4_e2e_adversarial.py:63 |
| forja_n4_e2e_adversarial.py::run | calls | forja_n4_e2e_adversarial.py::_copy_case | EXTRACTED | forja_n4_e2e_adversarial.py:66 |
| forja_n4_e2e_adversarial.py::run | calls | forja_n4_e2e_adversarial.py::_load | EXTRACTED | forja_n4_e2e_adversarial.py:68 |
| forja_n4_e2e_adversarial.py::run | calls | forja_n4_e2e_adversarial.py::_save | EXTRACTED | forja_n4_e2e_adversarial.py:70 |
| forja_n4_e2e_adversarial.py::run | calls | forja_n4_validate.py::validate_case | EXTRACTED | forja_n4_e2e_adversarial.py:71 |
| forja_n4_e2e_adversarial.py::run | calls | forja_n4_e2e_adversarial.py::_codes | EXTRACTED | forja_n4_e2e_adversarial.py:72 |
| forja_n4_e2e_adversarial.py::run | calls | forja_n4_e2e_adversarial.py::_copy_case | EXTRACTED | forja_n4_e2e_adversarial.py:75 |
| forja_n4_e2e_adversarial.py::run | calls | forja_n4_e2e_adversarial.py::_load | EXTRACTED | forja_n4_e2e_adversarial.py:77 |
| forja_n4_e2e_adversarial.py::run | calls | forja_n4_e2e_adversarial.py::_save | EXTRACTED | forja_n4_e2e_adversarial.py:79 |
| forja_n4_e2e_adversarial.py::run | calls | forja_n4_validate.py::validate_case | EXTRACTED | forja_n4_e2e_adversarial.py:80 |
| forja_n4_e2e_adversarial.py::run | calls | forja_n4_e2e_adversarial.py::_codes | EXTRACTED | forja_n4_e2e_adversarial.py:81 |
| forja_n4_e2e_adversarial.py::run | calls | forja_n4_e2e_adversarial.py::_copy_case | EXTRACTED | forja_n4_e2e_adversarial.py:84 |
| forja_n4_e2e_adversarial.py::run | calls | forja_n4_e2e_adversarial.py::_load | EXTRACTED | forja_n4_e2e_adversarial.py:86 |
| forja_n4_e2e_adversarial.py::run | calls | forja_n4_e2e_adversarial.py::_save | EXTRACTED | forja_n4_e2e_adversarial.py:88 |
| forja_n4_e2e_adversarial.py::run | calls | forja_n4_validate.py::validate_case | EXTRACTED | forja_n4_e2e_adversarial.py:89 |
| forja_n4_e2e_adversarial.py::run | calls | forja_n4_e2e_adversarial.py::_codes | EXTRACTED | forja_n4_e2e_adversarial.py:90 |
| forja_n4_e2e_adversarial.py::run | calls | forja_n4_e2e_adversarial.py::_copy_case | EXTRACTED | forja_n4_e2e_adversarial.py:93 |
| forja_n4_e2e_adversarial.py::run | calls | forja_n4_e2e_adversarial.py::_load | EXTRACTED | forja_n4_e2e_adversarial.py:95 |
| forja_n4_e2e_adversarial.py::run | calls | forja_n4_e2e_adversarial.py::_save | EXTRACTED | forja_n4_e2e_adversarial.py:97 |
| forja_n4_e2e_adversarial.py::run | calls | forja_n4_validate.py::validate_case | EXTRACTED | forja_n4_e2e_adversarial.py:98 |
| forja_n4_e2e_adversarial.py::run | calls | forja_n4_e2e_adversarial.py::_codes | EXTRACTED | forja_n4_e2e_adversarial.py:99 |
| forja_n4_e2e_adversarial.py::run | calls | forja_n4_e2e_adversarial.py::_copy_case | EXTRACTED | forja_n4_e2e_adversarial.py:102 |
| forja_n4_e2e_adversarial.py::run | calls | forja_n4_e2e_adversarial.py::_load | EXTRACTED | forja_n4_e2e_adversarial.py:104 |
| forja_n4_e2e_adversarial.py::run | calls | forja_n4_e2e_adversarial.py::_save | EXTRACTED | forja_n4_e2e_adversarial.py:107 |
| forja_n4_e2e_adversarial.py::run | calls | forja_n4_validate.py::validate_case | EXTRACTED | forja_n4_e2e_adversarial.py:108 |
| forja_n4_e2e_adversarial.py::run | calls | forja_n4_e2e_adversarial.py::_codes | EXTRACTED | forja_n4_e2e_adversarial.py:109 |
| forja_n4_e2e_adversarial.py::run | calls | forja_n4_e2e_adversarial.py::_copy_case | EXTRACTED | forja_n4_e2e_adversarial.py:112 |
| forja_n4_e2e_adversarial.py::run | calls | forja_n4_e2e_adversarial.py::_load | EXTRACTED | forja_n4_e2e_adversarial.py:114 |
| forja_n4_e2e_adversarial.py::run | calls | forja_case_tests.py::suite_hash | EXTRACTED | forja_n4_e2e_adversarial.py:115 |
| forja_n4_e2e_adversarial.py::run | calls | forja_case_tests.py::suite_hash | EXTRACTED | forja_n4_e2e_adversarial.py:118 |
| forja_n4_e2e_adversarial.py::run | calls | forja_n4_e2e_adversarial.py::_save | EXTRACTED | forja_n4_e2e_adversarial.py:119 |
| forja_n4_e2e_adversarial.py::run | calls | forja_n4_e2e_adversarial.py::_load | EXTRACTED | forja_n4_e2e_adversarial.py:121 |
| forja_n4_e2e_adversarial.py::run | calls | forja_n4_e2e_adversarial.py::_save | EXTRACTED | forja_n4_e2e_adversarial.py:123 |
| forja_n4_e2e_adversarial.py::run | calls | forja_n4_validate.py::validate_case | EXTRACTED | forja_n4_e2e_adversarial.py:124 |
| forja_n4_e2e_adversarial.py::run | calls | forja_n4_validate.py::validate_case | EXTRACTED | forja_n4_e2e_adversarial.py:130 |
| forja_n4_e2e_adversarial.py::run | calls | forja_n4_e2e_adversarial.py::_codes | EXTRACTED | forja_n4_e2e_adversarial.py:48 |
| forja_n4_e2e_adversarial.py::run | calls | forja_n4_e2e_adversarial.py::_codes | EXTRACTED | forja_n4_e2e_adversarial.py:55 |
| forja_n4_e2e_adversarial.py::run | calls | forja_n4_e2e_adversarial.py::_codes | EXTRACTED | forja_n4_e2e_adversarial.py:125 |
| forja_n4_e2e_adversarial.py::run | calls | forja_n4_e2e_adversarial.py::_codes | EXTRACTED | forja_n4_e2e_adversarial.py:131 |
| forja_n4_e2e_adversarial.py::main | calls | forja_n4_e2e_adversarial.py::run | EXTRACTED | forja_n4_e2e_adversarial.py:142 |
| forja_n4_invalidation.py | imports_from | forja_n3_common.py | EXTRACTED | forja_n4_invalidation.py:9 |
| forja_n4_invalidation.py | imports_from | forja_n3_common.py | EXTRACTED | forja_n4_invalidation.py:9 |
| forja_n4_invalidation.py | imports_from | forja_n4_common.py | EXTRACTED | forja_n4_invalidation.py:10 |
| forja_n4_invalidation.py | imports_from | forja_n4_common.py | EXTRACTED | forja_n4_invalidation.py:10 |
| forja_n4_invalidation.py | imports_from | forja_state_machine.py | EXTRACTED | forja_n4_invalidation.py:11 |
| forja_n4_invalidation.py | imports_from | forja_state_machine.py | EXTRACTED | forja_n4_invalidation.py:11 |
| forja_n4_invalidation.py::invalidate | calls | forja_n4_common.py::append_trace | EXTRACTED | forja_n4_invalidation.py:45 |
| forja_n4_invalidation.py::invalidate | calls | forja_state_machine.py::derive_state | EXTRACTED | forja_n4_invalidation.py:46 |
| forja_n4_invalidation.py::invalidate | calls | forja_n3_common.py::read_json | EXTRACTED | forja_n4_invalidation.py:38 |
| forja_n4_invalidation.py::invalidate | calls | forja_n4_common.py::write_artifact | EXTRACTED | forja_n4_invalidation.py:43 |
| forja_n4_invalidation.py::invalidate | calls | forja_state_machine.py::record_event | EXTRACTED | forja_n4_invalidation.py:48 |
| forja_n4_invalidation.py::main | calls | forja_n4_invalidation.py::invalidate | EXTRACTED | forja_n4_invalidation.py:65 |
| forja_n4_invalidation.py::main | calls | forja_n3_common.py::resolve_case_dir | EXTRACTED | forja_n4_invalidation.py:65 |
| forja_n4_m6_cycles.py | imports_from | forja_case_tests.py | EXTRACTED | forja_n4_m6_cycles.py:10 |
| forja_n4_m6_cycles.py | imports_from | forja_case_tests.py | EXTRACTED | forja_n4_m6_cycles.py:10 |
| forja_n4_m6_cycles.py | imports_from | forja_consistency.py | EXTRACTED | forja_n4_m6_cycles.py:11 |
| forja_n4_m6_cycles.py | imports_from | forja_fidelity.py | EXTRACTED | forja_n4_m6_cycles.py:12 |
| forja_n4_m6_cycles.py | imports_from | forja_n3_common.py | EXTRACTED | forja_n4_m6_cycles.py:13 |
| forja_n4_m6_cycles.py | imports_from | forja_n3_common.py | EXTRACTED | forja_n4_m6_cycles.py:13 |
| forja_n4_m6_cycles.py | imports_from | forja_n3_common.py | EXTRACTED | forja_n4_m6_cycles.py:13 |
| forja_n4_m6_cycles.py | imports_from | forja_n3_common.py | EXTRACTED | forja_n4_m6_cycles.py:13 |
| forja_n4_m6_cycles.py | imports_from | forja_n3_common.py | EXTRACTED | forja_n4_m6_cycles.py:13 |
| forja_n4_m6_cycles.py | imports_from | forja_n3_common.py | EXTRACTED | forja_n4_m6_cycles.py:13 |
| forja_n4_m6_cycles.py | imports_from | forja_n4_common.py | EXTRACTED | forja_n4_m6_cycles.py:14 |
| forja_n4_m6_cycles.py | imports_from | forja_n4_common.py | EXTRACTED | forja_n4_m6_cycles.py:14 |
| forja_n4_m6_cycles.py | imports_from | forja_n4_validate.py | EXTRACTED | forja_n4_m6_cycles.py:15 |
| forja_n4_m6_cycles.py::run | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_n4_m6_cycles.py:134 |
| forja_n4_m6_cycles.py::run | calls | forja_case_tests.py::suite_hash | EXTRACTED | forja_n4_m6_cycles.py:186 |
| forja_n4_m6_cycles.py::run | calls | forja_case_tests.py::run_suite | EXTRACTED | forja_n4_m6_cycles.py:205 |
| forja_n4_m6_cycles.py::run | calls | forja_consistency.py::inspect_physical_document | EXTRACTED | forja_n4_m6_cycles.py:207 |
| forja_n4_m6_cycles.py::run | calls | forja_n4_m6_cycles.py::_docx_semantic_text | EXTRACTED | forja_n4_m6_cycles.py:208 |
| forja_n4_m6_cycles.py::run | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_n4_m6_cycles.py:222 |
| forja_n4_m6_cycles.py::run | calls | forja_n4_validate.py::validate_case | EXTRACTED | forja_n4_m6_cycles.py:239 |
| forja_n4_m6_cycles.py::run | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_n4_m6_cycles.py:245 |
| forja_n4_m6_cycles.py::run | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_n4_m6_cycles.py:246 |
| forja_n4_m6_cycles.py::run | calls | forja_n3_common.py::read_json | EXTRACTED | forja_n4_m6_cycles.py:97 |
| forja_n4_m6_cycles.py::run | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_n4_m6_cycles.py:113 |
| forja_n4_m6_cycles.py::run | calls | forja_n3_common.py::read_json | EXTRACTED | forja_n4_m6_cycles.py:114 |
| forja_n4_m6_cycles.py::run | calls | forja_n4_common.py::build_envelope | EXTRACTED | forja_n4_m6_cycles.py:138 |
| forja_n4_m6_cycles.py::run | calls | forja_n4_common.py::write_artifact | EXTRACTED | forja_n4_m6_cycles.py:139 |
| forja_n4_m6_cycles.py::run | calls | forja_fidelity.py::compare_fidelity | EXTRACTED | forja_n4_m6_cycles.py:210 |
| forja_n4_m6_cycles.py::run | calls | forja_n4_m6_cycles.py::_docx_semantic_text | EXTRACTED | forja_n4_m6_cycles.py:215 |
| forja_n4_m6_cycles.py::run | calls | forja_n3_common.py::read_json | EXTRACTED | forja_n4_m6_cycles.py:240 |
| forja_n4_m6_cycles.py::run | calls | forja_n3_common.py::canonical_hash | EXTRACTED | forja_n4_m6_cycles.py:216 |
| forja_n4_m6_cycles.py::run | calls | forja_n3_common.py::canonical_hash | EXTRACTED | forja_n4_m6_cycles.py:216 |
| forja_n4_m6_cycles.py::run | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_n4_m6_cycles.py:128 |
| forja_n4_m6_cycles.py::run | calls | forja_n3_common.py::canonical_hash | EXTRACTED | forja_n4_m6_cycles.py:217 |
| forja_n4_m6_cycles.py::run | calls | forja_n3_common.py::canonical_hash | EXTRACTED | forja_n4_m6_cycles.py:217 |
| forja_n4_m6_cycles.py::run | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_n4_m6_cycles.py:228 |
| forja_n4_m6_cycles.py::run | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_n4_m6_cycles.py:228 |
| forja_n4_m6_cycles.py::run | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_n4_m6_cycles.py:228 |
| forja_n4_m6_cycles.py::run | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_n4_m6_cycles.py:224 |
| forja_n4_m6_prepare.py | imports_from | forja_metadata.py | EXTRACTED | forja_n4_m6_prepare.py:14 |
| forja_n4_m6_prepare.py | imports_from | forja_n3_common.py | EXTRACTED | forja_n4_m6_prepare.py:15 |
| forja_n4_m6_prepare.py | imports_from | forja_n3_common.py | EXTRACTED | forja_n4_m6_prepare.py:15 |
| forja_n4_m6_prepare.py | imports_from | forja_n3_common.py | EXTRACTED | forja_n4_m6_prepare.py:15 |
| forja_n4_m6_prepare.py | imports_from | forja_n3_common.py | EXTRACTED | forja_n4_m6_prepare.py:15 |
| forja_n4_m6_prepare.py | imports_from | forja_visual_qa.py | EXTRACTED | forja_n4_m6_prepare.py:125 |
| forja_n4_m6_prepare.py::prepare | calls | forja_metadata.py::sanitize_final_artifacts | EXTRACTED | forja_n4_m6_prepare.py:95 |
| forja_n4_m6_prepare.py::prepare | calls | forja_n4_m6_prepare.py::_render | EXTRACTED | forja_n4_m6_prepare.py:98 |
| forja_n4_m6_prepare.py::prepare | calls | forja_n4_m6_prepare.py::_contact_sheet | EXTRACTED | forja_n4_m6_prepare.py:100 |
| forja_n4_m6_prepare.py::prepare | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_n4_m6_prepare.py:115 |
| forja_n4_m6_prepare.py::prepare | calls | forja_n4_m6_prepare.py::_extract_text | EXTRACTED | forja_n4_m6_prepare.py:97 |
| forja_n4_m6_prepare.py::prepare | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_n4_m6_prepare.py:104 |
| forja_n4_m6_prepare.py::prepare | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_n4_m6_prepare.py:113 |
| forja_n4_m6_prepare.py::prepare | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_n4_m6_prepare.py:113 |
| forja_n4_m6_prepare.py::prepare | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_n4_m6_prepare.py:113 |
| forja_n4_m6_prepare.py::approve | calls | forja_visual_qa.py::run_visual_qa | EXTRACTED | forja_n4_m6_prepare.py:128 |
| forja_n4_m6_prepare.py::approve | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_n4_m6_prepare.py:140 |
| forja_n4_m6_prepare.py::main | calls | forja_n4_m6_prepare.py::prepare | EXTRACTED | forja_n4_m6_prepare.py:150 |
| forja_n4_m6_prepare.py::main | calls | forja_n4_m6_prepare.py::approve | EXTRACTED | forja_n4_m6_prepare.py:150 |
| forja_n4_pilot_cafelana.py | imports_from | forja_case_tests.py | EXTRACTED | forja_n4_pilot_cafelana.py:8 |
| forja_n4_pilot_cafelana.py | imports_from | forja_case_tests.py | EXTRACTED | forja_n4_pilot_cafelana.py:8 |
| forja_n4_pilot_cafelana.py | imports_from | forja_consistency.py | EXTRACTED | forja_n4_pilot_cafelana.py:9 |
| forja_n4_pilot_cafelana.py | imports_from | forja_n3_common.py | EXTRACTED | forja_n4_pilot_cafelana.py:10 |
| forja_n4_pilot_cafelana.py | imports_from | forja_n3_common.py | EXTRACTED | forja_n4_pilot_cafelana.py:10 |
| forja_n4_pilot_cafelana.py | imports_from | forja_n3_common.py | EXTRACTED | forja_n4_pilot_cafelana.py:10 |
| forja_n4_pilot_cafelana.py | imports_from | forja_n3_common.py | EXTRACTED | forja_n4_pilot_cafelana.py:10 |
| forja_n4_pilot_cafelana.py | imports_from | forja_n4_common.py | EXTRACTED | forja_n4_pilot_cafelana.py:11 |
| forja_n4_pilot_cafelana.py | imports_from | forja_n4_common.py | EXTRACTED | forja_n4_pilot_cafelana.py:11 |
| forja_n4_pilot_cafelana.py | imports_from | forja_n4_validate.py | EXTRACTED | forja_n4_pilot_cafelana.py:12 |
| forja_n4_pilot_cafelana.py::run | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_n4_pilot_cafelana.py:44 |
| forja_n4_pilot_cafelana.py::run | calls | forja_case_tests.py::suite_hash | EXTRACTED | forja_n4_pilot_cafelana.py:150 |
| forja_n4_pilot_cafelana.py::run | calls | forja_case_tests.py::run_suite | EXTRACTED | forja_n4_pilot_cafelana.py:165 |
| forja_n4_pilot_cafelana.py::run | calls | forja_consistency.py::inspect_physical_document | EXTRACTED | forja_n4_pilot_cafelana.py:168 |
| forja_n4_pilot_cafelana.py::run | calls | forja_n4_validate.py::validate_case | EXTRACTED | forja_n4_pilot_cafelana.py:188 |
| forja_n4_pilot_cafelana.py::run | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_n4_pilot_cafelana.py:39 |
| forja_n4_pilot_cafelana.py::run | calls | forja_n3_common.py::read_json | EXTRACTED | forja_n4_pilot_cafelana.py:40 |
| forja_n4_pilot_cafelana.py::run | calls | forja_n4_common.py::build_envelope | EXTRACTED | forja_n4_pilot_cafelana.py:49 |
| forja_n4_pilot_cafelana.py::run | calls | forja_n4_common.py::write_artifact | EXTRACTED | forja_n4_pilot_cafelana.py:54 |
| forja_n4_pilot_science.py | imports_from | forja_n3_common.py | EXTRACTED | forja_n4_pilot_science.py:10 |
| forja_n4_pilot_science.py | imports_from | forja_n3_common.py | EXTRACTED | forja_n4_pilot_science.py:10 |
| forja_n4_pilot_science.py | imports_from | forja_n3_common.py | EXTRACTED | forja_n4_pilot_science.py:10 |
| forja_n4_pilot_science.py | imports_from | forja_n3_common.py | EXTRACTED | forja_n4_pilot_science.py:10 |
| forja_n4_pilot_science.py | imports_from | forja_n3_common.py | EXTRACTED | forja_n4_pilot_science.py:10 |
| forja_n4_pilot_science.py | imports_from | forja_n4_common.py | EXTRACTED | forja_n4_pilot_science.py:11 |
| forja_n4_pilot_science.py | imports_from | forja_n4_common.py | EXTRACTED | forja_n4_pilot_science.py:11 |
| forja_n4_pilot_science.py | imports_from | forja_science.py | EXTRACTED | forja_n4_pilot_science.py:12 |
| forja_n4_pilot_science.py | imports_from | forja_science.py | EXTRACTED | forja_n4_pilot_science.py:12 |
| forja_n4_pilot_science.py | imports_from | forja_science.py | EXTRACTED | forja_n4_pilot_science.py:12 |
| forja_n4_pilot_science.py | imports_from | forja_science.py | EXTRACTED | forja_n4_pilot_science.py:12 |
| forja_n4_pilot_science.py::run | calls | forja_science.py::discover | EXTRACTED | forja_n4_pilot_science.py:32 |
| forja_n4_pilot_science.py::run | calls | forja_science.py::crossref_by_doi | EXTRACTED | forja_n4_pilot_science.py:33 |
| forja_n4_pilot_science.py::run | calls | forja_science.py::ncbi_fetch | EXTRACTED | forja_n4_pilot_science.py:34 |
| forja_n4_pilot_science.py::run | calls | forja_n4_pilot_science.py::_article_text | EXTRACTED | forja_n4_pilot_science.py:37 |
| forja_n4_pilot_science.py::run | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_n4_pilot_science.py:46 |
| forja_n4_pilot_science.py::run | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_n4_pilot_science.py:47 |
| forja_n4_pilot_science.py::run | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_n4_pilot_science.py:56 |
| forja_n4_pilot_science.py::run | calls | forja_science.py::validate_case | EXTRACTED | forja_n4_pilot_science.py:157 |
| forja_n4_pilot_science.py::run | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_n4_pilot_science.py:159 |
| forja_n4_pilot_science.py::run | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_n4_pilot_science.py:49 |
| forja_n4_pilot_science.py::run | calls | forja_n3_common.py::read_json | EXTRACTED | forja_n4_pilot_science.py:50 |
| forja_n4_pilot_science.py::run | calls | forja_n4_common.py::build_envelope | EXTRACTED | forja_n4_pilot_science.py:59 |
| forja_n4_pilot_science.py::run | calls | forja_n4_common.py::write_artifact | EXTRACTED | forja_n4_pilot_science.py:63 |
| forja_n4_pilot_science.py::run | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_n4_pilot_science.py:158 |
| forja_n4_pilot_science.py::run | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_n4_pilot_science.py:49 |
| forja_n4_pilot_science.py::run | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_n4_pilot_science.py:94 |
| forja_n4_validate.py | imports_from | forja_case_tests.py | EXTRACTED | forja_n4_validate.py:12 |
| forja_n4_validate.py | imports_from | forja_case_tests.py | EXTRACTED | forja_n4_validate.py:12 |
| forja_n4_validate.py | imports_from | forja_case_tests.py | EXTRACTED | forja_n4_validate.py:12 |
| forja_n4_validate.py | imports_from | forja_consistency.py | EXTRACTED | forja_n4_validate.py:13 |
| forja_n4_validate.py | imports_from | forja_consistency.py | EXTRACTED | forja_n4_validate.py:13 |
| forja_n4_validate.py | imports_from | forja_consistency.py | EXTRACTED | forja_n4_validate.py:13 |
| forja_n4_validate.py | imports_from | forja_consistency.py | EXTRACTED | forja_n4_validate.py:13 |
| forja_n4_validate.py | imports_from | forja_consistency.py | EXTRACTED | forja_n4_validate.py:13 |
| forja_n4_validate.py | imports_from | forja_consistency.py | EXTRACTED | forja_n4_validate.py:13 |
| forja_n4_validate.py | imports_from | forja_learning.py | EXTRACTED | forja_n4_validate.py:21 |
| forja_n4_validate.py | imports_from | forja_learning_registry.py | EXTRACTED | forja_n4_validate.py:22 |
| forja_n4_validate.py | imports_from | forja_post_protocol_contracts.py | EXTRACTED | forja_n4_validate.py:23 |
| forja_n4_validate.py | imports_from | forja_post_protocol_contracts.py | EXTRACTED | forja_n4_validate.py:23 |
| forja_n4_validate.py | imports_from | forja_post_protocol_contracts.py | EXTRACTED | forja_n4_validate.py:23 |
| forja_n4_validate.py | imports_from | forja_post_protocol_contracts.py | EXTRACTED | forja_n4_validate.py:23 |
| forja_n4_validate.py | imports_from | forja_post_protocol_contracts.py | EXTRACTED | forja_n4_validate.py:23 |
| forja_n4_validate.py | imports_from | forja_metacognition.py | EXTRACTED | forja_n4_validate.py:30 |
| forja_n4_validate.py | imports_from | forja_f8_contract.py | EXTRACTED | forja_n4_validate.py:31 |
| forja_n4_validate.py | imports_from | forja_n3_common.py | EXTRACTED | forja_n4_validate.py:32 |
| forja_n4_validate.py | imports_from | forja_n3_common.py | EXTRACTED | forja_n4_validate.py:32 |
| forja_n4_validate.py | imports_from | forja_n3_common.py | EXTRACTED | forja_n4_validate.py:32 |
| forja_n4_validate.py | imports_from | forja_n3_common.py | EXTRACTED | forja_n4_validate.py:32 |
| forja_n4_validate.py | imports_from | forja_n3_common.py | EXTRACTED | forja_n4_validate.py:32 |
| forja_n4_validate.py | imports_from | forja_n3_common.py | EXTRACTED | forja_n4_validate.py:32 |
| forja_n4_validate.py | imports_from | forja_n3_common.py | EXTRACTED | forja_n4_validate.py:32 |
| forja_n4_validate.py | imports_from | forja_n3_common.py | EXTRACTED | forja_n4_validate.py:32 |
| forja_n4_validate.py | imports_from | forja_n4_common.py | EXTRACTED | forja_n4_validate.py:42 |
| forja_n4_validate.py | imports_from | forja_n4_common.py | EXTRACTED | forja_n4_validate.py:42 |
| forja_n4_validate.py | imports_from | forja_n4_common.py | EXTRACTED | forja_n4_validate.py:42 |
| forja_n4_validate.py | imports_from | forja_n4_common.py | EXTRACTED | forja_n4_validate.py:42 |
| forja_n4_validate.py | imports_from | forja_n4_common.py | EXTRACTED | forja_n4_validate.py:42 |
| forja_n4_validate.py | imports_from | forja_reasoning.py | EXTRACTED | forja_n4_validate.py:43 |
| forja_n4_validate.py | imports_from | forja_reasoning.py | EXTRACTED | forja_n4_validate.py:43 |
| forja_n4_validate.py | imports_from | forja_reasoning.py | EXTRACTED | forja_n4_validate.py:43 |
| forja_n4_validate.py | imports_from | forja_reasoning.py | EXTRACTED | forja_n4_validate.py:43 |
| forja_n4_validate.py | imports_from | forja_reasoning.py | EXTRACTED | forja_n4_validate.py:43 |
| forja_n4_validate.py | imports_from | forja_reasoning.py | EXTRACTED | forja_n4_validate.py:43 |
| forja_n4_validate.py | imports_from | forja_reasoning.py | EXTRACTED | forja_n4_validate.py:43 |
| forja_n4_validate.py | imports_from | forja_reasoning.py | EXTRACTED | forja_n4_validate.py:43 |
| forja_n4_validate.py | imports_from | forja_science.py | EXTRACTED | forja_n4_validate.py:53 |
| forja_n4_validate.py | imports_from | forja_science.py | EXTRACTED | forja_n4_validate.py:53 |
| forja_n4_validate.py | imports_from | forja_science.py | EXTRACTED | forja_n4_validate.py:53 |
| forja_n4_validate.py | imports_from | forja_science.py | EXTRACTED | forja_n4_validate.py:53 |
| forja_n4_validate.py | imports_from | forja_science.py | EXTRACTED | forja_n4_validate.py:53 |
| forja_n4_validate.py | imports_from | forja_science.py | EXTRACTED | forja_n4_validate.py:53 |
| forja_n4_validate.py | imports_from | forja_fidelity.py | EXTRACTED | forja_n4_validate.py:288 |
| forja_n4_validate.py::_settlement | calls | forja_n4_common.py::issue | EXTRACTED | forja_n4_validate.py:70 |
| forja_n4_validate.py::_settlement | calls | forja_n4_common.py::issue | EXTRACTED | forja_n4_validate.py:73 |
| forja_n4_validate.py::_settlement | calls | forja_n4_common.py::issue | EXTRACTED | forja_n4_validate.py:77 |
| forja_n4_validate.py::_recipient_map_validator | calls | forja_reasoning.py::validate_recipient_map | EXTRACTED | forja_n4_validate.py:122 |
| forja_n4_validate.py::_target_phase | calls | forja_n3_common.py::read_json | EXTRACTED | forja_n4_validate.py:155 |
| forja_n4_validate.py::_source_registry_findings | calls | forja_n4_common.py::issue | EXTRACTED | forja_n4_validate.py:184 |
| forja_n4_validate.py::_source_registry_findings | calls | forja_n4_common.py::issue | EXTRACTED | forja_n4_validate.py:191 |
| forja_n4_validate.py::_source_registry_findings | calls | forja_n4_common.py::issue | EXTRACTED | forja_n4_validate.py:181 |
| forja_n4_validate.py::_source_registry_findings | calls | forja_n4_common.py::issue | EXTRACTED | forja_n4_validate.py:195 |
| forja_n4_validate.py::_source_registry_findings | calls | forja_n4_common.py::issue | EXTRACTED | forja_n4_validate.py:200 |
| forja_n4_validate.py::_source_registry_findings | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_n4_validate.py:201 |
| forja_n4_validate.py::_source_registry_findings | calls | forja_n4_common.py::issue | EXTRACTED | forja_n4_validate.py:202 |
| forja_n4_validate.py::_source_registry_findings | calls | forja_n4_common.py::issue | EXTRACTED | forja_n4_validate.py:210 |
| forja_n4_validate.py::_registered_source_path | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_n4_validate.py:226 |
| forja_n4_validate.py::_global_replay_findings | calls | forja_f8_contract.py::validate_f8 | EXTRACTED | forja_n4_validate.py:333 |
| forja_n4_validate.py::_global_replay_findings | calls | forja_n4_common.py::issue | EXTRACTED | forja_n4_validate.py:301 |
| forja_n4_validate.py::_global_replay_findings | calls | forja_n4_common.py::issue | EXTRACTED | forja_n4_validate.py:309 |
| forja_n4_validate.py::_global_replay_findings | calls | forja_n3_common.py::read_json | EXTRACTED | forja_n4_validate.py:317 |
| forja_n4_validate.py::_global_replay_findings | calls | forja_n4_common.py::issue | EXTRACTED | forja_n4_validate.py:320 |
| forja_n4_validate.py::_global_replay_findings | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_n4_validate.py:266 |
| forja_n4_validate.py::_global_replay_findings | calls | forja_n4_common.py::issue | EXTRACTED | forja_n4_validate.py:267 |
| forja_n4_validate.py::_global_replay_findings | calls | forja_fidelity.py::compare_fidelity | EXTRACTED | forja_n4_validate.py:290 |
| forja_n4_validate.py::_global_replay_findings | calls | forja_n4_common.py::issue | EXTRACTED | forja_n4_validate.py:296 |
| forja_n4_validate.py::_global_replay_findings | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_n4_validate.py:314 |
| forja_n4_validate.py::_global_replay_findings | calls | forja_n4_common.py::issue | EXTRACTED | forja_n4_validate.py:315 |
| forja_n4_validate.py::_global_replay_findings | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_n4_validate.py:324 |
| forja_n4_validate.py::_global_replay_findings | calls | forja_n4_common.py::issue | EXTRACTED | forja_n4_validate.py:325 |
| forja_n4_validate.py::_global_replay_findings | calls | forja_n4_common.py::issue | EXTRACTED | forja_n4_validate.py:341 |
| forja_n4_validate.py::_global_replay_findings | calls | forja_n4_common.py::issue | EXTRACTED | forja_n4_validate.py:346 |
| forja_n4_validate.py::_global_replay_findings | calls | forja_n3_common.py::canonical_hash | EXTRACTED | forja_n4_validate.py:282 |
| forja_n4_validate.py::_global_replay_findings | calls | forja_n3_common.py::canonical_hash | EXTRACTED | forja_n4_validate.py:282 |
| forja_n4_validate.py::_global_replay_findings | calls | forja_n4_common.py::issue | EXTRACTED | forja_n4_validate.py:283 |
| forja_n4_validate.py::_global_replay_findings | calls | forja_n4_common.py::issue | EXTRACTED | forja_n4_validate.py:285 |
| forja_n4_validate.py::_global_replay_findings | calls | forja_n4_common.py::issue | EXTRACTED | forja_n4_validate.py:292 |
| forja_n4_validate.py::_global_replay_findings | calls | forja_n4_common.py::issue | EXTRACTED | forja_n4_validate.py:294 |
| forja_n4_validate.py::_global_replay_findings | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_n4_validate.py:336 |
| forja_n4_validate.py::_global_replay_findings | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_n4_validate.py:337 |
| forja_n4_validate.py::_effective_named_mode | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_n4_validate.py:369 |
| forja_n4_validate.py::_effective_named_mode | calls | forja_n3_common.py::read_json | EXTRACTED | forja_n4_validate.py:375 |
| forja_n4_validate.py::_effective_mode | calls | forja_n4_validate.py::_effective_named_mode | EXTRACTED | forja_n4_validate.py:381 |
| forja_n4_validate.py::effective_signature_lite_mode | calls | forja_n4_validate.py::_effective_named_mode | EXTRACTED | forja_n4_validate.py:388 |
| forja_n4_validate.py::_schema_findings | calls | forja_n3_common.py::read_json | EXTRACTED | forja_n4_validate.py:397 |
| forja_n4_validate.py::_schema_findings | calls | forja_n3_common.py::read_json | EXTRACTED | forja_n4_validate.py:393 |
| forja_n4_validate.py::_schema_findings | calls | forja_n4_common.py::issue | EXTRACTED | forja_n4_validate.py:402 |
| forja_n4_validate.py::_schema_findings | calls | forja_n4_common.py::issue | EXTRACTED | forja_n4_validate.py:396 |
| forja_n4_validate.py::_schema_findings | calls | forja_n4_common.py::issue | EXTRACTED | forja_n4_validate.py:399 |
| forja_n4_validate.py::_cross_reference_findings | calls | forja_n4_common.py::issue | EXTRACTED | forja_n4_validate.py:431 |
| forja_n4_validate.py::_cross_reference_findings | calls | forja_n4_common.py::issue | EXTRACTED | forja_n4_validate.py:421 |
| forja_n4_validate.py::_cross_reference_findings | calls | forja_n4_common.py::issue | EXTRACTED | forja_n4_validate.py:426 |
| forja_n4_validate.py::validate_case | calls | forja_n3_common.py::load_config | EXTRACTED | forja_n4_validate.py:436 |
| forja_n4_validate.py::validate_case | calls | forja_n4_validate.py::_effective_mode | EXTRACTED | forja_n4_validate.py:437 |
| forja_n4_validate.py::validate_case | calls | forja_n4_validate.py::_required_files | EXTRACTED | forja_n4_validate.py:440 |
| forja_n4_validate.py::validate_case | calls | forja_n4_validate.py::effective_signature_lite_mode | EXTRACTED | forja_n4_validate.py:444 |
| forja_n4_validate.py::validate_case | calls | forja_n4_validate.py::_source_registry_findings | EXTRACTED | forja_n4_validate.py:449 |
| forja_n4_validate.py::validate_case | calls | forja_n4_validate.py::_council_ready | EXTRACTED | forja_n4_validate.py:517 |
| forja_n4_validate.py::validate_case | calls | forja_n3_common.py::canonical_hash | EXTRACTED | forja_n4_validate.py:556 |
| forja_n4_validate.py::validate_case | calls | forja_n4_validate.py::_target_phase | EXTRACTED | forja_n4_validate.py:438 |
| forja_n4_validate.py::validate_case | calls | forja_n3_common.py::read_json | EXTRACTED | forja_n4_validate.py:448 |
| forja_n4_validate.py::validate_case | calls | forja_n3_common.py::read_json | EXTRACTED | forja_n4_validate.py:456 |
| forja_n4_validate.py::validate_case | calls | forja_n4_validate.py::_registered_source_path | EXTRACTED | forja_n4_validate.py:489 |
| forja_n4_validate.py::validate_case | calls | forja_n4_validate.py::_global_replay_findings | EXTRACTED | forja_n4_validate.py:502 |
| forja_n4_validate.py::validate_case | calls | forja_n4_validate.py::_cross_reference_findings | EXTRACTED | forja_n4_validate.py:503 |
| forja_n4_validate.py::validate_case | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_n4_validate.py:559 |
| forja_n4_validate.py::validate_case | calls | forja_n4_common.py::append_trace | EXTRACTED | forja_n4_validate.py:560 |
| forja_n4_validate.py::validate_case | calls | forja_n4_validate.py::_schema_findings | EXTRACTED | forja_n4_validate.py:462 |
| forja_n4_validate.py::validate_case | calls | forja_n4_common.py::validate_envelope | EXTRACTED | forja_n4_validate.py:463 |
| forja_n4_validate.py::validate_case | calls | forja_science.py::validate_claims | EXTRACTED | forja_n4_validate.py:483 |
| forja_n4_validate.py::validate_case | calls | forja_learning_registry.py::suite_learning_findings | EXTRACTED | forja_n4_validate.py:487 |
| forja_n4_validate.py::validate_case | calls | forja_case_tests.py::validate_results | EXTRACTED | forja_n4_validate.py:490 |
| forja_n4_validate.py::validate_case | calls | forja_case_tests.py::run_suite | EXTRACTED | forja_n4_validate.py:494 |
| forja_n4_validate.py::validate_case | calls | forja_n4_common.py::issue | EXTRACTED | forja_n4_validate.py:459 |
| forja_n4_validate.py::validate_case | calls | forja_n4_common.py::issue | EXTRACTED | forja_n4_validate.py:466 |
| forja_n4_validate.py::validate_case | calls | forja_n4_common.py::issue | EXTRACTED | forja_n4_validate.py:471 |
| forja_n4_validate.py::validate_case | calls | forja_n4_validate.py::_recipient_map_validator | EXTRACTED | forja_n4_validate.py:474 |
| forja_n4_validate.py::validate_case | calls | forja_n4_common.py::issue | EXTRACTED | forja_n4_validate.py:492 |
| forja_n4_validate.py::validate_case | calls | forja_n3_common.py::canonical_hash | EXTRACTED | forja_n4_validate.py:500 |
| forja_n4_validate.py::validate_case | calls | forja_n3_common.py::canonical_hash | EXTRACTED | forja_n4_validate.py:500 |
| forja_n4_validate.py::validate_case | calls | forja_n4_common.py::issue | EXTRACTED | forja_n4_validate.py:469 |
| forja_n4_validate.py::validate_case | calls | forja_n4_validate.py::_result_core | EXTRACTED | forja_n4_validate.py:500 |
| forja_n4_validate.py::validate_case | calls | forja_n4_validate.py::_result_core | EXTRACTED | forja_n4_validate.py:500 |
| forja_n4_validate.py::validate_case | calls | forja_n4_common.py::issue | EXTRACTED | forja_n4_validate.py:501 |
| forja_n4_validate.py::validate_case | calls | forja_n4_validate.py::_pilot_blocking_finding | EXTRACTED | forja_n4_validate.py:506 |
| forja_n4_validate.py::management_summary | calls | forja_n4_validate.py::_target_phase | EXTRACTED | forja_n4_validate.py:567 |
| forja_n4_validate.py::management_summary | calls | forja_n4_validate.py::validate_case | EXTRACTED | forja_n4_validate.py:572 |
| forja_n4_validate.py::management_summary | calls | forja_n3_common.py::read_json | EXTRACTED | forja_n4_validate.py:565 |
| forja_n4_validate.py::management_summary | calls | forja_n3_common.py::read_json | EXTRACTED | forja_n4_validate.py:573 |
| forja_n4_validate.py::management_summary | calls | forja_n3_common.py::read_json | EXTRACTED | forja_n4_validate.py:575 |
| forja_n4_validate.py::management_summary | calls | forja_n3_common.py::read_json | EXTRACTED | forja_n4_validate.py:577 |
| forja_n4_validate.py::management_summary | calls | forja_n3_common.py::read_json | EXTRACTED | forja_n4_validate.py:579 |
| forja_n4_validate.py::management_summary | calls | forja_n3_common.py::read_json | EXTRACTED | forja_n4_validate.py:580 |
| forja_n4_validate.py::management_summary | calls | forja_n3_common.py::read_json | EXTRACTED | forja_n4_validate.py:581 |
| forja_n4_validate.py::management_summary | calls | forja_n3_common.py::read_json | EXTRACTED | forja_n4_validate.py:603 |
| forja_n4_validate.py::management_summary | calls | forja_n4_validate.py::_council_ready | EXTRACTED | forja_n4_validate.py:621 |
| forja_n4_validate.py::management_summary | calls | forja_n4_validate.py::_required_files | EXTRACTED | forja_n4_validate.py:628 |
| forja_n4_validate.py::management_summary | calls | forja_n3_common.py::load_config | EXTRACTED | forja_n4_validate.py:628 |
| forja_n4_validate.py::main | calls | forja_n4_validate.py::validate_case | EXTRACTED | forja_n4_validate.py:662 |
| forja_n4_validate.py::main | calls | forja_n3_common.py::resolve_case_dir | EXTRACTED | forja_n4_validate.py:662 |
| forja_official_sources.py | imports_from | forja_n3_common.py | EXTRACTED | forja_official_sources.py:24 |
| forja_official_sources.py | imports_from | forja_n3_common.py | EXTRACTED | forja_official_sources.py:24 |
| forja_official_sources.py | imports_from | forja_n3_common.py | EXTRACTED | forja_official_sources.py:24 |
| forja_official_sources.py | imports_from | forja_n3_common.py | EXTRACTED | forja_official_sources.py:24 |
| forja_official_sources.py::_OfficialHtmlText.__init__ | calls | forja_official_sources.py::_OfficialHtmlText.__init__ | EXTRACTED | forja_official_sources.py:46 |
| forja_official_sources.py::source_excerpt_sha256 | calls | forja_official_sources.py::normalize_evidence_text | EXTRACTED | forja_official_sources.py:73 |
| forja_official_sources.py::_response_text | calls | forja_official_sources.py::_OfficialHtmlText | EXTRACTED | forja_official_sources.py:111 |
| forja_official_sources.py::_fetch_official | calls | forja_official_sources.py::_response_text | EXTRACTED | forja_official_sources.py:140 |
| forja_official_sources.py::_fetch_official | calls | forja_official_sources.py::_official_url | EXTRACTED | forja_official_sources.py:135 |
| forja_official_sources.py::_candidate_anchors | calls | forja_official_sources.py::normalize_evidence_text | EXTRACTED | forja_official_sources.py:159 |
| forja_official_sources.py::validate_live_official_source | calls | forja_official_sources.py::normalize_evidence_text | EXTRACTED | forja_official_sources.py:195 |
| forja_official_sources.py::validate_live_official_source | calls | forja_official_sources.py::normalize_evidence_text | EXTRACTED | forja_official_sources.py:196 |
| forja_official_sources.py::validate_live_official_source | calls | forja_official_sources.py::_official_url | EXTRACTED | forja_official_sources.py:180 |
| forja_official_sources.py::validate_live_official_source | calls | forja_official_sources.py::_official_url | EXTRACTED | forja_official_sources.py:187 |
| forja_official_sources.py::validate_live_official_source | calls | forja_official_sources.py::_extract_source_text | EXTRACTED | forja_official_sources.py:190 |
| forja_official_sources.py::validate_live_official_source | calls | forja_official_sources.py::normalize_evidence_text | EXTRACTED | forja_official_sources.py:199 |
| forja_official_sources.py::validate_live_official_source | calls | forja_official_sources.py::_candidate_anchors | EXTRACTED | forja_official_sources.py:209 |
| forja_official_sources.py::validate_live_official_source | calls | forja_official_sources.py::_identity_present | EXTRACTED | forja_official_sources.py:192 |
| forja_official_sources.py::validate_live_official_source | calls | forja_official_sources.py::source_excerpt_sha256 | EXTRACTED | forja_official_sources.py:207 |
| forja_official_sources.py::build_manifest | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_official_sources.py:330 |
| forja_official_sources.py::build_manifest | calls | forja_official_sources.py::_identity_from_name | EXTRACTED | forja_official_sources.py:307 |
| forja_official_sources.py::build_manifest | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_official_sources.py:325 |
| forja_official_sources.py::build_manifest | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_official_sources.py:318 |
| forja_official_sources.py::build_manifest | calls | forja_official_sources.py::_urls_from_text | EXTRACTED | forja_official_sources.py:312 |
| forja_official_sources.py::build_manifest | calls | forja_official_sources.py::_official_url | EXTRACTED | forja_official_sources.py:312 |
| forja_official_sources.py::build_manifest | calls | forja_official_sources.py::_identity_present | EXTRACTED | forja_official_sources.py:313 |
| forja_official_sources.py::validate_cached_source | calls | forja_n3_common.py::read_json | EXTRACTED | forja_official_sources.py:350 |
| forja_official_sources.py::validate_cached_source | calls | forja_official_sources.py::_official_url | EXTRACTED | forja_official_sources.py:357 |
| forja_official_sources.py::validate_cached_source | calls | forja_official_sources.py::validate_live_official_source | EXTRACTED | forja_official_sources.py:366 |
| forja_official_sources.py::validate_cached_source | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_official_sources.py:355 |
| forja_official_sources.py::validate_cached_source | calls | forja_official_sources.py::_identity_present | EXTRACTED | forja_official_sources.py:362 |
| forja_official_sources.py::validate_archived_source | calls | forja_official_sources.py::sidecar_path | EXTRACTED | forja_official_sources.py:394 |
| forja_official_sources.py::validate_archived_source | calls | forja_n3_common.py::read_json | EXTRACTED | forja_official_sources.py:395 |
| forja_official_sources.py::validate_archived_source | calls | forja_official_sources.py::_official_url | EXTRACTED | forja_official_sources.py:404 |
| forja_official_sources.py::validate_archived_source | calls | forja_official_sources.py::validate_cached_source | EXTRACTED | forja_official_sources.py:418 |
| forja_official_sources.py::validate_archived_source | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_official_sources.py:402 |
| forja_official_sources.py::validate_source_path | calls | forja_official_sources.py::validate_cached_source | EXTRACTED | forja_official_sources.py:459 |
| forja_official_sources.py::validate_source_path | calls | forja_official_sources.py::validate_archived_source | EXTRACTED | forja_official_sources.py:464 |
| forja_official_sources.py::main | calls | forja_official_sources.py::build_manifest | EXTRACTED | forja_official_sources.py:479 |
| forja_official_sources.py::main | calls | forja_official_sources.py::validate_source_path | EXTRACTED | forja_official_sources.py:481 |
| forja_p0.py::_severidade | calls | forja_p0.py::_payload | EXTRACTED | forja_p0.py:60 |
| forja_p0.py::_resolvido | calls | forja_p0.py::_payload | EXTRACTED | forja_p0.py:69 |
| forja_p0.py::validar_p0 | calls | forja_p0.py::_achados | EXTRACTED | forja_p0.py:117 |
| forja_p0.py::validar_p0 | calls | forja_p0.py::_declarado | EXTRACTED | forja_p0.py:120 |
| forja_p0.py::validar_p0 | calls | forja_p0.py::_resolvido | EXTRACTED | forja_p0.py:119 |
| forja_p0.py::validar_p0 | calls | forja_p0.py::_resolvido | EXTRACTED | forja_p0.py:118 |
| forja_p0.py::validar_p0 | calls | forja_p0.py::_severidade | EXTRACTED | forja_p0.py:118 |
| forja_p0.py::validar_p0 | calls | forja_p0.py::_severidade | EXTRACTED | forja_p0.py:119 |
| forja_package.py | imports_from | forja_n3_common.py | EXTRACTED | forja_package.py:13 |
| forja_package.py | imports_from | forja_n3_common.py | EXTRACTED | forja_package.py:13 |
| forja_package.py | imports_from | forja_n3_common.py | EXTRACTED | forja_package.py:13 |
| forja_package.py | imports_from | forja_n3_common.py | EXTRACTED | forja_package.py:13 |
| forja_package.py | imports_from | forja_n3_common.py | EXTRACTED | forja_package.py:13 |
| forja_package.py | imports_from | forja_n3_common.py | EXTRACTED | forja_package.py:13 |
| forja_package.py | imports_from | forja_n3_common.py | EXTRACTED | forja_package.py:13 |
| forja_package.py | imports_from | forja_n3_common.py | EXTRACTED | forja_package.py:13 |
| forja_package.py | imports_from | forja_state_machine.py | EXTRACTED | forja_package.py:23 |
| forja_package.py | imports_from | forja_adversarial_audit.py | EXTRACTED | forja_package.py:24 |
| forja_package.py | imports_from | forja_adversarial_audit.py | EXTRACTED | forja_package.py:24 |
| forja_package.py | imports_from | forja_adversarial_audit.py | EXTRACTED | forja_package.py:24 |
| forja_package.py | imports_from | forja_editorial_fidelity.py | EXTRACTED | forja_package.py:29 |
| forja_package.py | imports_from | forja_fidelity.py | EXTRACTED | forja_package.py:30 |
| forja_package.py | imports_from | forja_official_sources.py | EXTRACTED | forja_package.py:31 |
| forja_package.py | imports_from | forja_official_sources.py | EXTRACTED | forja_package.py:31 |
| forja_package.py | imports_from | forja_human_review.py | EXTRACTED | forja_package.py:32 |
| forja_package.py | imports_from | forja_f8_contract.py | EXTRACTED | forja_package.py:33 |
| forja_package.py | imports_from | forja_memoria_auditabilidade.py | EXTRACTED | forja_package.py:34 |
| forja_package.py | imports_from | forja_authorities.py | EXTRACTED | forja_package.py:35 |
| forja_package.py | imports_from | forja_precedente.py | EXTRACTED | forja_package.py:38 |
| forja_package.py | imports_from | forja_precedente.py | EXTRACTED | forja_package.py:38 |
| forja_package.py | imports_from | forja_precedente.py | EXTRACTED | forja_package.py:38 |
| forja_package.py | imports_from | forja_precedente.py | EXTRACTED | forja_package.py:38 |
| forja_package.py | imports_from | forja_estilo_humano.py | EXTRACTED | forja_package.py:747 |
| forja_package.py | imports_from | forja_n4_validate.py | EXTRACTED | forja_package.py:774 |
| forja_package.py | imports_from | forja_verificador.py | EXTRACTED | forja_package.py:175 |
| forja_package.py | imports_from | forja_metricas_f7.py | EXTRACTED | forja_package.py:176 |
| forja_package.py::release_policy_hash | calls | forja_n3_common.py::canonical_hash | EXTRACTED | forja_package.py:64 |
| forja_package.py::release_policy_hash | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_package.py:67 |
| forja_package.py::_artifact | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_package.py:125 |
| forja_package.py::_artifact | calls | forja_n3_common.py::resolve_name | EXTRACTED | forja_package.py:118 |
| forja_package.py::_artifact | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_package.py:121 |
| forja_package.py::_artifact | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_package.py:124 |
| forja_package.py::_artifact | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_package.py:127 |
| forja_package.py::_f7_metrics | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_package.py:135 |
| forja_package.py::validate_f7 | calls | forja_n3_common.py::read_json | EXTRACTED | forja_package.py:154 |
| forja_package.py::validate_f7 | calls | forja_package.py::_f7_metrics | EXTRACTED | forja_package.py:157 |
| forja_package.py::validate_f7 | calls | forja_package.py::_pending_citations | EXTRACTED | forja_package.py:159 |
| forja_package.py::validate_f7 | calls | forja_package.py::_unresolved_markers | EXTRACTED | forja_package.py:160 |
| forja_package.py::validate_f7 | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_package.py:156 |
| forja_package.py::validate_f7 | calls | forja_metricas_f7.py::metricas_f7 | EXTRACTED | forja_package.py:183 |
| forja_package.py::validate_f7 | calls | forja_package.py::_pending_citations | EXTRACTED | forja_package.py:184 |
| forja_package.py::validate_f7 | calls | forja_verificador.py::verificar | EXTRACTED | forja_package.py:178 |
| forja_package.py::_citation_key | calls | forja_authorities.py::authority_key | EXTRACTED | forja_package.py:215 |
| forja_package.py::_document_binding | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_package.py:230 |
| forja_package.py::_document_binding | calls | forja_package.py::_markdown_paragraphs | EXTRACTED | forja_package.py:242 |
| forja_package.py::_document_binding | calls | forja_n3_common.py::canonical_hash | EXTRACTED | forja_package.py:236 |
| forja_package.py::_document_binding | calls | forja_n3_common.py::canonical_hash | EXTRACTED | forja_package.py:248 |
| forja_package.py::_document_binding | calls | forja_n3_common.py::canonical_hash | EXTRACTED | forja_package.py:254 |
| forja_package.py::_document_binding | calls | forja_n3_common.py::canonical_hash | EXTRACTED | forja_package.py:259 |
| forja_package.py::_document_binding | calls | forja_n3_common.py::canonical_hash | EXTRACTED | forja_package.py:261 |
| forja_package.py::_document_binding | calls | forja_n3_common.py::canonical_hash | EXTRACTED | forja_package.py:263 |
| forja_package.py::_document_binding | calls | forja_package.py::_citation_key | EXTRACTED | forja_package.py:251 |
| forja_package.py::_denied_search_actions | calls | forja_n3_common.py::read_json | EXTRACTED | forja_package.py:270 |
| forja_package.py::_brief_routes | calls | forja_n3_common.py::read_json | EXTRACTED | forja_package.py:280 |
| forja_package.py::validate_source_ledger | calls | forja_n3_common.py::read_json | EXTRACTED | forja_package.py:300 |
| forja_package.py::validate_source_ledger | calls | forja_package.py::_ledger_entries | EXTRACTED | forja_package.py:301 |
| forja_package.py::validate_source_ledger | calls | forja_precedente.py::validate_legal_research_trace | EXTRACTED | forja_package.py:305 |
| forja_package.py::validate_source_ledger | calls | forja_package.py::_brief_routes | EXTRACTED | forja_package.py:311 |
| forja_package.py::validate_source_ledger | calls | forja_precedente.py::validate_anchor_cards | EXTRACTED | forja_package.py:312 |
| forja_package.py::validate_source_ledger | calls | forja_official_sources.py::validate_source_path | EXTRACTED | forja_package.py:369 |
| forja_package.py::validate_source_ledger | calls | forja_package.py::_denied_search_actions | EXTRACTED | forja_package.py:308 |
| forja_package.py::validate_source_ledger | calls | forja_package.py::_document_binding | EXTRACTED | forja_package.py:340 |
| forja_package.py::validate_source_ledger | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_package.py:381 |
| forja_package.py::validate_source_ledger | calls | forja_package.py::_citation_key | EXTRACTED | forja_package.py:392 |
| forja_package.py::validate_source_ledger | calls | forja_precedente.py::anchor_ids | EXTRACTED | forja_package.py:410 |
| forja_package.py::validate_source_ledger | calls | forja_precedente.py::failed_anchor_routes | EXTRACTED | forja_package.py:412 |
| forja_package.py::validate_source_ledger | calls | forja_package.py::_citation_key | EXTRACTED | forja_package.py:389 |
| forja_package.py::validate_source_ledger | calls | forja_official_sources.py::source_excerpt_sha256 | EXTRACTED | forja_package.py:338 |
| forja_package.py::validate_source_ledger | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_package.py:346 |
| forja_package.py::validate_source_ledger | calls | forja_human_review.py::validate_claim_review_receipt | EXTRACTED | forja_package.py:349 |
| forja_package.py::validate_source_ledger | calls | forja_n3_common.py::canonical_hash | EXTRACTED | forja_package.py:354 |
| forja_package.py::validate_source_ledger | calls | forja_official_sources.py::source_excerpt_sha256 | EXTRACTED | forja_package.py:356 |
| forja_package.py::validate_source_ledger | calls | forja_n3_common.py::canonical_hash | EXTRACTED | forja_package.py:360 |
| forja_package.py::validate_source_ledger | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_package.py:357 |
| forja_package.py::validate_context_artifact | calls | forja_n3_common.py::read_json | EXTRACTED | forja_package.py:421 |
| forja_package.py::validate_context_artifact | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_package.py:423 |
| forja_package.py::validate_fidelity | calls | forja_n3_common.py::read_json | EXTRACTED | forja_package.py:436 |
| forja_package.py::validate_fidelity | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_package.py:438 |
| forja_package.py::validate_fidelity | calls | forja_fidelity.py::compare_fidelity | EXTRACTED | forja_package.py:479 |
| forja_package.py::validate_adversarial_bundle | calls | forja_package.py::_artifact | EXTRACTED | forja_package.py:516 |
| forja_package.py::validate_adversarial_bundle | calls | forja_adversarial_audit.py::validate_adversarial_audit | EXTRACTED | forja_package.py:526 |
| forja_package.py::validate_adversarial_bundle | calls | forja_n3_common.py::read_json | EXTRACTED | forja_package.py:518 |
| forja_package.py::validate_adversarial_bundle | calls | forja_adversarial_audit.py::validate_adversarial_audit | EXTRACTED | forja_package.py:523 |
| forja_package.py::validate_adversarial_bundle | calls | forja_package.py::_artifact | EXTRACTED | forja_package.py:532 |
| forja_package.py::validate_adversarial_bundle | calls | forja_adversarial_audit.py::validate_adversarial_strategy | EXTRACTED | forja_package.py:534 |
| forja_package.py::validate_adversarial_bundle | calls | forja_package.py::_artifact | EXTRACTED | forja_package.py:540 |
| forja_package.py::validate_adversarial_bundle | calls | forja_adversarial_audit.py::validate_adversarial_recheck | EXTRACTED | forja_package.py:543 |
| forja_package.py::validate_adversarial_bundle | calls | forja_n3_common.py::read_json | EXTRACTED | forja_package.py:534 |
| forja_package.py::validate_adversarial_bundle | calls | forja_n3_common.py::read_json | EXTRACTED | forja_package.py:544 |
| forja_package.py::validate_definition | calls | forja_state_machine.py::derive_state | EXTRACTED | forja_package.py:555 |
| forja_package.py::validate_definition | calls | forja_package.py::_artifact | EXTRACTED | forja_package.py:561 |
| forja_package.py::validate_definition | calls | forja_package.py::_email_claims | EXTRACTED | forja_package.py:745 |
| forja_package.py::validate_definition | calls | forja_estilo_humano.py::relatorio | EXTRACTED | forja_package.py:748 |
| forja_package.py::validate_definition | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_package.py:557 |
| forja_package.py::validate_definition | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_package.py:560 |
| forja_package.py::validate_definition | calls | forja_package.py::_artifact | EXTRACTED | forja_package.py:646 |
| forja_package.py::validate_definition | calls | forja_package.py::validate_f7 | EXTRACTED | forja_package.py:647 |
| forja_package.py::validate_definition | calls | forja_package.py::validate_adversarial_bundle | EXTRACTED | forja_package.py:685 |
| forja_package.py::validate_definition | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_package.py:572 |
| forja_package.py::validate_definition | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_package.py:576 |
| forja_package.py::validate_definition | calls | forja_package.py::_protocolable_content | EXTRACTED | forja_package.py:600 |
| forja_package.py::validate_definition | calls | forja_package.py::_artifact | EXTRACTED | forja_package.py:663 |
| forja_package.py::validate_definition | calls | forja_package.py::validate_source_ledger | EXTRACTED | forja_package.py:664 |
| forja_package.py::validate_definition | calls | forja_package.py::_artifact | EXTRACTED | forja_package.py:690 |
| forja_package.py::validate_definition | calls | forja_package.py::validate_context_artifact | EXTRACTED | forja_package.py:691 |
| forja_package.py::validate_definition | calls | forja_package.py::_artifact | EXTRACTED | forja_package.py:694 |
| forja_package.py::validate_definition | calls | forja_package.py::_artifact | EXTRACTED | forja_package.py:724 |
| forja_package.py::validate_definition | calls | forja_package.py::validate_fidelity | EXTRACTED | forja_package.py:725 |
| forja_package.py::validate_definition | calls | forja_package.py::_artifact | EXTRACTED | forja_package.py:592 |
| forja_package.py::validate_definition | calls | forja_package.py::_artifact | EXTRACTED | forja_package.py:617 |
| forja_package.py::validate_definition | calls | forja_package.py::_artifact | EXTRACTED | forja_package.py:618 |
| forja_package.py::validate_definition | calls | forja_package.py::_artifact | EXTRACTED | forja_package.py:619 |
| forja_package.py::validate_definition | calls | forja_editorial_fidelity.py::validate_editorial_bundle | EXTRACTED | forja_package.py:620 |
| forja_package.py::validate_definition | calls | forja_n3_common.py::read_json | EXTRACTED | forja_package.py:698 |
| forja_package.py::validate_definition | calls | forja_memoria_auditabilidade.py::validate_bundle | EXTRACTED | forja_package.py:712 |
| forja_package.py::build_package | calls | forja_n3_common.py::read_json | EXTRACTED | forja_package.py:768 |
| forja_package.py::build_package | calls | forja_package.py::validate_definition | EXTRACTED | forja_package.py:771 |
| forja_package.py::build_package | calls | forja_n4_validate.py::validate_case | EXTRACTED | forja_package.py:776 |
| forja_package.py::build_package | calls | forja_n3_common.py::canonical_hash | EXTRACTED | forja_package.py:792 |
| forja_package.py::build_package | calls | forja_n3_common.py::read_json | EXTRACTED | forja_package.py:845 |
| forja_package.py::build_package | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_package.py:770 |
| forja_package.py::build_package | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_package.py:773 |
| forja_package.py::build_package | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_package.py:778 |
| forja_package.py::build_package | calls | forja_package.py::release_policy_hash | EXTRACTED | forja_package.py:781 |
| forja_package.py::build_package | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_package.py:847 |
| forja_package.py::build_package | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_package.py:840 |
| forja_package.py::build_package | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_package.py:819 |
| forja_package.py::build_package | calls | forja_n3_common.py::canonical_hash | EXTRACTED | forja_package.py:822 |
| forja_package.py::build_package | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_package.py:807 |
| forja_package.py::build_package | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_package.py:808 |
| forja_package.py::revalidate_package_manifest | calls | forja_package.py::release_policy_hash | EXTRACTED | forja_package.py:862 |
| forja_package.py::revalidate_package_manifest | calls | forja_n3_common.py::canonical_hash | EXTRACTED | forja_package.py:868 |
| forja_package.py::revalidate_package_manifest | calls | forja_n3_common.py::canonical_hash | EXTRACTED | forja_package.py:878 |
| forja_package.py::revalidate_package_manifest | calls | forja_package.py::validate_definition | EXTRACTED | forja_package.py:872 |
| forja_package.py::revalidate_package_manifest | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_package.py:882 |
| forja_paragrafos.py | imports_from | forja_artefatos.py | EXTRACTED | forja_paragrafos.py:45 |
| forja_paragrafos.py::validar_paragrafos_lastreados | calls | forja_paragrafos.py::_unidades | EXTRACTED | forja_paragrafos.py:129 |
| forja_paragrafos.py::validar_paragrafos_lastreados | calls | forja_paragrafos.py::_norm | EXTRACTED | forja_paragrafos.py:164 |
| forja_paragrafos.py::validar_paragrafos_lastreados | calls | forja_paragrafos.py::_rotulo | EXTRACTED | forja_paragrafos.py:142 |
| forja_paragrafos.py::validar_paragrafos_lastreados | calls | forja_paragrafos.py::_hashes_do_texto | EXTRACTED | forja_paragrafos.py:156 |
| forja_paragrafos.py::validar_paragrafos_lastreados | calls | forja_paragrafos.py::_tem_lastro | EXTRACTED | forja_paragrafos.py:140 |
| forja_paragrafos.py::validar_paragrafos_lastreados | calls | forja_paragrafos.py::_e_editorial | EXTRACTED | forja_paragrafos.py:140 |
| forja_paragrafos.py::validar_paragrafos_lastreados | calls | forja_paragrafos.py::_norm | EXTRACTED | forja_paragrafos.py:172 |
| forja_paragrafos.py::validar_paragrafos_lastreados | calls | forja_paragrafos.py::_rotulo | EXTRACTED | forja_paragrafos.py:170 |
| forja_paragrafos.py::carregar_e_validar | calls | forja_paragrafos.py::validar_paragrafos_lastreados | EXTRACTED | forja_paragrafos.py:230 |
| forja_phase_contracts.py | imports_from | forja_n3_common.py | EXTRACTED | forja_phase_contracts.py:7 |
| forja_phase_contracts.py | imports_from | forja_n3_common.py | EXTRACTED | forja_phase_contracts.py:7 |
| forja_phase_contracts.py | imports_from | forja_n3_common.py | EXTRACTED | forja_phase_contracts.py:7 |
| forja_phase_contracts.py | imports_from | forja_n3_common.py | EXTRACTED | forja_phase_contracts.py:7 |
| forja_phase_contracts.py | imports_from | forja_n3_common.py | EXTRACTED | forja_phase_contracts.py:7 |
| forja_phase_contracts.py::load_contract | calls | forja_n3_common.py::read_json | EXTRACTED | forja_phase_contracts.py:18 |
| forja_phase_contracts.py::load_contract | calls | forja_n3_common.py::canonical_hash | EXTRACTED | forja_phase_contracts.py:35 |
| forja_phase_contracts.py::load_contract | calls | forja_n3_common.py::read_json | EXTRACTED | forja_phase_contracts.py:36 |
| forja_phase_contracts.py::load_contract | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_phase_contracts.py:16 |
| forja_phase_contracts.py::load_contract | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_phase_contracts.py:20 |
| forja_phase_contracts.py::load_contract | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_phase_contracts.py:27 |
| forja_phase_contracts.py::load_contract | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_phase_contracts.py:29 |
| forja_phase_contracts.py::load_contract | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_phase_contracts.py:31 |
| forja_phase_contracts.py::load_contract | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_phase_contracts.py:33 |
| forja_phase_contracts.py::load_contract | calls | forja_n3_common.py::canonical_hash | EXTRACTED | forja_phase_contracts.py:44 |
| forja_phase_contracts.py::validate_all | calls | forja_phase_contracts.py::load_contract | EXTRACTED | forja_phase_contracts.py:50 |
| forja_pilot_m4.py | imports_from | forja_n3_common.py | EXTRACTED | forja_pilot_m4.py:21 |
| forja_pilot_m4.py | imports_from | forja_visual_qa_structural.py | EXTRACTED | forja_pilot_m4.py:31 |
| forja_pilot_m4.py::montar_piloto | calls | forja_pilot_m4.py::limpar_corpo | EXTRACTED | forja_pilot_m4.py:83 |
| forja_pilot_m4.py::montar_piloto | calls | forja_visual_qa_structural.py::auditar_documento | EXTRACTED | forja_pilot_m4.py:111 |
| forja_pilot_m4.py::montar_piloto | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_pilot_m4.py:132 |
| forja_pilot_m4.py::montar_piloto | calls | forja_pilot_m4.py::append_unique_many | EXTRACTED | forja_pilot_m4.py:137 |
| forja_pilot_m4.py::montar_piloto | calls | forja_pilot_m4.py::eh_titulo | EXTRACTED | forja_pilot_m4.py:93 |
| forja_pilot_m4.py::montar_piloto | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_pilot_m4.py:135 |
| forja_pilot_m4.py::montar_piloto | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_pilot_m4.py:119 |
| forja_post_protocol.py | imports_from | forja_document_compare.py | EXTRACTED | forja_post_protocol.py:23 |
| forja_post_protocol.py | imports_from | forja_document_compare.py | EXTRACTED | forja_post_protocol.py:23 |
| forja_post_protocol.py | imports_from | forja_document_compare.py | EXTRACTED | forja_post_protocol.py:23 |
| forja_post_protocol.py | imports_from | forja_n3_common.py | EXTRACTED | forja_post_protocol.py:24 |
| forja_post_protocol.py | imports_from | forja_n3_common.py | EXTRACTED | forja_post_protocol.py:24 |
| forja_post_protocol.py | imports_from | forja_n3_common.py | EXTRACTED | forja_post_protocol.py:24 |
| forja_post_protocol.py | imports_from | forja_n3_common.py | EXTRACTED | forja_post_protocol.py:24 |
| forja_post_protocol.py | imports_from | forja_n3_common.py | EXTRACTED | forja_post_protocol.py:24 |
| forja_post_protocol.py | imports_from | forja_n3_common.py | EXTRACTED | forja_post_protocol.py:24 |
| forja_post_protocol.py | imports_from | forja_n3_common.py | EXTRACTED | forja_post_protocol.py:24 |
| forja_post_protocol.py | imports_from | forja_n3_common.py | EXTRACTED | forja_post_protocol.py:24 |
| forja_post_protocol.py | imports_from | forja_n3_common.py | EXTRACTED | forja_post_protocol.py:24 |
| forja_post_protocol.py | imports_from | forja_n3_common.py | EXTRACTED | forja_post_protocol.py:24 |
| forja_post_protocol.py | imports_from | forja_n3_common.py | EXTRACTED | forja_post_protocol.py:24 |
| forja_post_protocol.py | imports_from | forja_n3_common.py | EXTRACTED | forja_post_protocol.py:24 |
| forja_post_protocol.py | imports_from | forja_n3_common.py | EXTRACTED | forja_post_protocol.py:24 |
| forja_post_protocol.py | imports_from | forja_n3_common.py | EXTRACTED | forja_post_protocol.py:24 |
| forja_post_protocol.py | imports_from | forja_n3_common.py | EXTRACTED | forja_post_protocol.py:24 |
| forja_post_protocol.py | imports_from | forja_n3_common.py | EXTRACTED | forja_post_protocol.py:24 |
| forja_post_protocol.py | imports_from | forja_n4_common.py | EXTRACTED | forja_post_protocol.py:42 |
| forja_post_protocol.py | imports_from | forja_n4_common.py | EXTRACTED | forja_post_protocol.py:42 |
| forja_post_protocol.py | imports_from | forja_post_protocol_contracts.py | EXTRACTED | forja_post_protocol.py:43 |
| forja_post_protocol.py | imports_from | forja_post_protocol_contracts.py | EXTRACTED | forja_post_protocol.py:43 |
| forja_post_protocol.py | imports_from | forja_post_protocol_contracts.py | EXTRACTED | forja_post_protocol.py:43 |
| forja_post_protocol.py | imports_from | forja_post_protocol_contracts.py | EXTRACTED | forja_post_protocol.py:43 |
| forja_post_protocol.py | imports_from | forja_post_protocol_contracts.py | EXTRACTED | forja_post_protocol.py:43 |
| forja_post_protocol.py | imports_from | forja_learning.py | EXTRACTED | forja_post_protocol.py:50 |
| forja_post_protocol.py | imports_from | forja_learning_registry.py | EXTRACTED | forja_post_protocol.py:51 |
| forja_post_protocol.py | imports_from | forja_state_machine.py | EXTRACTED | forja_post_protocol.py:52 |
| forja_post_protocol.py | imports_from | forja_state_machine.py | EXTRACTED | forja_post_protocol.py:52 |
| forja_post_protocol.py | imports_from | forja_state_machine.py | EXTRACTED | forja_post_protocol.py:52 |
| forja_post_protocol.py | imports_from | forja_state_machine.py | EXTRACTED | forja_post_protocol.py:52 |
| forja_post_protocol.py | imports_from | forja_n4_common.py | EXTRACTED | forja_post_protocol.py:1393 |
| forja_post_protocol.py | imports_from | forja_n4_common.py | EXTRACTED | forja_post_protocol.py:1465 |
| forja_post_protocol.py | imports_from | forja_n4_common.py | EXTRACTED | forja_post_protocol.py:1478 |
| forja_post_protocol.py::content_key | calls | forja_n3_common.py::sha256_bytes | EXTRACTED | forja_post_protocol.py:112 |
| forja_post_protocol.py::evidence_key | calls | forja_n3_common.py::sha256_bytes | EXTRACTED | forja_post_protocol.py:116 |
| forja_post_protocol.py::_record | calls | forja_n3_common.py::RevisionConflict | EXTRACTED | forja_post_protocol.py:142 |
| forja_post_protocol.py::_record | calls | forja_state_machine.py::derive_state | EXTRACTED | forja_post_protocol.py:128 |
| forja_post_protocol.py::_record | calls | forja_state_machine.py::record_event | EXTRACTED | forja_post_protocol.py:130 |
| forja_post_protocol.py::_baseline_records | calls | forja_n3_common.py::read_json | EXTRACTED | forja_post_protocol.py:157 |
| forja_post_protocol.py::_baseline_records | calls | forja_n3_common.py::read_json | EXTRACTED | forja_post_protocol.py:160 |
| forja_post_protocol.py::_baseline_records | calls | forja_n3_common.py::read_json | EXTRACTED | forja_post_protocol.py:166 |
| forja_post_protocol.py::_baseline_records | calls | forja_n3_common.py::canonical_hash | EXTRACTED | forja_post_protocol.py:174 |
| forja_post_protocol.py::resolve_ai_baseline | calls | forja_post_protocol.py::_parse_timestamp | EXTRACTED | forja_post_protocol.py:180 |
| forja_post_protocol.py::resolve_ai_baseline | calls | forja_post_protocol.py::_baseline_records | EXTRACTED | forja_post_protocol.py:183 |
| forja_post_protocol.py::resolve_ai_baseline | calls | forja_post_protocol.py::_parse_timestamp | EXTRACTED | forja_post_protocol.py:184 |
| forja_post_protocol.py::resolve_ai_baseline | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_post_protocol.py:194 |
| forja_post_protocol.py::_delivery_timestamp | calls | forja_post_protocol.py::_message_header | EXTRACTED | forja_post_protocol.py:225 |
| forja_post_protocol.py::_delivery_timestamp | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_post_protocol.py:232 |
| forja_post_protocol.py::_sent_baseline_candidates | calls | forja_post_protocol.py::_parse_timestamp | EXTRACTED | forja_post_protocol.py:242 |
| forja_post_protocol.py::_sent_baseline_candidates | calls | forja_post_protocol.py::_delivery_timestamp | EXTRACTED | forja_post_protocol.py:248 |
| forja_post_protocol.py::_sent_baseline_candidates | calls | forja_post_protocol.py::_parse_timestamp | EXTRACTED | forja_post_protocol.py:249 |
| forja_post_protocol.py::_sent_baseline_candidates | calls | forja_post_protocol.py::_walk_gmail_parts | EXTRACTED | forja_post_protocol.py:253 |
| forja_post_protocol.py::_sent_baseline_candidates | calls | forja_post_protocol.py::_parse_timestamp | EXTRACTED | forja_post_protocol.py:274 |
| forja_post_protocol.py::_walk_gmail_parts | calls | forja_post_protocol.py::_walk_gmail_parts | EXTRACTED | forja_post_protocol.py:283 |
| forja_post_protocol.py::backfill_baseline_from_gmail | calls | forja_post_protocol.py::_sent_baseline_candidates | EXTRACTED | forja_post_protocol.py:298 |
| forja_post_protocol.py::backfill_baseline_from_gmail | calls | forja_n3_common.py::sha256_bytes | EXTRACTED | forja_post_protocol.py:322 |
| forja_post_protocol.py::backfill_baseline_from_gmail | calls | forja_n3_common.py::new_id | EXTRACTED | forja_post_protocol.py:349 |
| forja_post_protocol.py::backfill_baseline_from_gmail | calls | forja_n4_common.py::build_envelope | EXTRACTED | forja_post_protocol.py:360 |
| forja_post_protocol.py::backfill_baseline_from_gmail | calls | forja_post_protocol_contracts.py::validate_post_protocol_baseline_backfill | EXTRACTED | forja_post_protocol.py:368 |
| forja_post_protocol.py::backfill_baseline_from_gmail | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_post_protocol.py:373 |
| forja_post_protocol.py::backfill_baseline_from_gmail | calls | forja_n4_common.py::write_artifact | EXTRACTED | forja_post_protocol.py:374 |
| forja_post_protocol.py::backfill_baseline_from_gmail | calls | forja_post_protocol.py::_record | EXTRACTED | forja_post_protocol.py:375 |
| forja_post_protocol.py::backfill_baseline_from_gmail | calls | forja_state_machine.py::load_events | EXTRACTED | forja_post_protocol.py:296 |
| forja_post_protocol.py::backfill_baseline_from_gmail | calls | forja_state_machine.py::initialize_case | EXTRACTED | forja_post_protocol.py:297 |
| forja_post_protocol.py::backfill_baseline_from_gmail | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_post_protocol.py:328 |
| forja_post_protocol.py::backfill_baseline_from_gmail | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_post_protocol.py:329 |
| forja_post_protocol.py::backfill_baseline_from_gmail | calls | forja_n3_common.py::read_json | EXTRACTED | forja_post_protocol.py:331 |
| forja_post_protocol.py::backfill_baseline_from_gmail | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_post_protocol.py:370 |
| forja_post_protocol.py::_text_similarity | calls | forja_document_compare.py::extract_document | EXTRACTED | forja_post_protocol.py:423 |
| forja_post_protocol.py::_text_similarity | calls | forja_document_compare.py::extract_document | EXTRACTED | forja_post_protocol.py:424 |
| forja_post_protocol.py::_verified_protocol_link | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_post_protocol.py:444 |
| forja_post_protocol.py::classify_protocol | calls | forja_post_protocol.py::_verified_protocol_link | EXTRACTED | forja_post_protocol.py:457 |
| forja_post_protocol.py::classify_protocol | calls | forja_document_compare.py::extract_document | EXTRACTED | forja_post_protocol.py:471 |
| forja_post_protocol.py::classify_protocol | calls | forja_post_protocol.py::_text_similarity | EXTRACTED | forja_post_protocol.py:481 |
| forja_post_protocol.py::classify_protocol | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_post_protocol.py:500 |
| forja_post_protocol.py::classify_protocol | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_post_protocol.py:484 |
| forja_post_protocol.py::classify_protocol | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_post_protocol.py:490 |
| forja_post_protocol.py::_folder_labels | calls | forja_post_protocol.py::safe_component | EXTRACTED | forja_post_protocol.py:517 |
| forja_post_protocol.py::_folder_labels | calls | forja_post_protocol.py::safe_component | EXTRACTED | forja_post_protocol.py:518 |
| forja_post_protocol.py::_folder_labels | calls | forja_post_protocol.py::safe_component | EXTRACTED | forja_post_protocol.py:519 |
| forja_post_protocol.py::_load_index | calls | forja_n3_common.py::read_json | EXTRACTED | forja_post_protocol.py:532 |
| forja_post_protocol.py::_load_index | calls | forja_post_protocol.py::_index_path | EXTRACTED | forja_post_protocol.py:532 |
| forja_post_protocol.py::_set_index_state | calls | forja_n3_common.py::InterProcessLock | EXTRACTED | forja_post_protocol.py:540 |
| forja_post_protocol.py::_set_index_state | calls | forja_post_protocol.py::_load_index | EXTRACTED | forja_post_protocol.py:541 |
| forja_post_protocol.py::_set_index_state | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_post_protocol.py:547 |
| forja_post_protocol.py::_set_index_state | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_post_protocol.py:548 |
| forja_post_protocol.py::_set_index_state | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_post_protocol.py:544 |
| forja_post_protocol.py::_set_index_state | calls | forja_post_protocol.py::_index_path | EXTRACTED | forja_post_protocol.py:548 |
| forja_post_protocol.py::_require_post_protocol_enabled | calls | forja_n3_common.py::feature_enabled | EXTRACTED | forja_post_protocol.py:552 |
| forja_post_protocol.py::_require_post_protocol_enabled | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_post_protocol.py:553 |
| forja_post_protocol.py::_block_capture | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_post_protocol.py:571 |
| forja_post_protocol.py::_block_capture | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_post_protocol.py:572 |
| forja_post_protocol.py::_block_capture | calls | forja_post_protocol.py::_set_index_state | EXTRACTED | forja_post_protocol.py:573 |
| forja_post_protocol.py::_block_capture | calls | forja_post_protocol.py::_record | EXTRACTED | forja_post_protocol.py:574 |
| forja_post_protocol.py::_block_capture | calls | forja_n3_common.py::canonical_hash | EXTRACTED | forja_post_protocol.py:577 |
| forja_post_protocol.py::_write_artifact_checked | calls | forja_n4_common.py::build_envelope | EXTRACTED | forja_post_protocol.py:605 |
| forja_post_protocol.py::_write_artifact_checked | calls | forja_n4_common.py::write_artifact | EXTRACTED | forja_post_protocol.py:618 |
| forja_post_protocol.py::_write_artifact_checked | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_post_protocol.py:615 |
| forja_post_protocol.py::_archive_prior_post_protocol_artifacts | calls | forja_n3_common.py::read_json | EXTRACTED | forja_post_protocol.py:625 |
| forja_post_protocol.py::_archive_prior_post_protocol_artifacts | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_post_protocol.py:639 |
| forja_post_protocol.py::_archive_prior_post_protocol_artifacts | calls | forja_n3_common.py::read_json | EXTRACTED | forja_post_protocol.py:633 |
| forja_post_protocol.py::_archive_prior_post_protocol_artifacts | calls | forja_n3_common.py::canonical_hash | EXTRACTED | forja_post_protocol.py:637 |
| forja_post_protocol.py::_sanitize_changes | calls | forja_n3_common.py::sha256_bytes | EXTRACTED | forja_post_protocol.py:650 |
| forja_post_protocol.py::_sanitize_changes | calls | forja_n3_common.py::sha256_bytes | EXTRACTED | forja_post_protocol.py:651 |
| forja_post_protocol.py::_learning_candidates | calls | forja_n3_common.py::read_json | EXTRACTED | forja_post_protocol.py:723 |
| forja_post_protocol.py::_learning_candidates | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_post_protocol.py:727 |
| forja_post_protocol.py::ingest_return | calls | forja_post_protocol.py::_require_post_protocol_enabled | EXTRACTED | forja_post_protocol.py:794 |
| forja_post_protocol.py::ingest_return | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_post_protocol.py:804 |
| forja_post_protocol.py::ingest_return | calls | forja_post_protocol.py::content_key | EXTRACTED | forja_post_protocol.py:805 |
| forja_post_protocol.py::ingest_return | calls | forja_post_protocol.py::evidence_key | EXTRACTED | forja_post_protocol.py:806 |
| forja_post_protocol.py::ingest_return | calls | forja_post_protocol.py::_record | EXTRACTED | forja_post_protocol.py:807 |
| forja_post_protocol.py::ingest_return | calls | forja_post_protocol.py::classify_protocol | EXTRACTED | forja_post_protocol.py:818 |
| forja_post_protocol.py::ingest_return | calls | forja_post_protocol.py::_archive_prior_post_protocol_artifacts | EXTRACTED | forja_post_protocol.py:824 |
| forja_post_protocol.py::ingest_return | calls | forja_post_protocol.py::_folder_labels | EXTRACTED | forja_post_protocol.py:826 |
| forja_post_protocol.py::ingest_return | calls | forja_n3_common.py::InterProcessLock | EXTRACTED | forja_post_protocol.py:828 |
| forja_post_protocol.py::ingest_return | calls | forja_post_protocol.py::_write_artifact_checked | EXTRACTED | forja_post_protocol.py:978 |
| forja_post_protocol.py::ingest_return | calls | forja_post_protocol.py::_record | EXTRACTED | forja_post_protocol.py:986 |
| forja_post_protocol.py::ingest_return | calls | forja_post_protocol.py::_write_artifact_checked | EXTRACTED | forja_post_protocol.py:1004 |
| forja_post_protocol.py::ingest_return | calls | forja_post_protocol.py::resolve_ai_baseline | EXTRACTED | forja_post_protocol.py:1031 |
| forja_post_protocol.py::ingest_return | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_post_protocol.py:1077 |
| forja_post_protocol.py::ingest_return | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_post_protocol.py:1078 |
| forja_post_protocol.py::ingest_return | calls | forja_post_protocol.py::_set_index_state | EXTRACTED | forja_post_protocol.py:1079 |
| forja_post_protocol.py::ingest_return | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_post_protocol.py:1108 |
| forja_post_protocol.py::ingest_return | calls | forja_n3_common.py::atomic_write_text | EXTRACTED | forja_post_protocol.py:1110 |
| forja_post_protocol.py::ingest_return | calls | forja_post_protocol.py::_preserve_change_reviews | EXTRACTED | forja_post_protocol.py:1127 |
| forja_post_protocol.py::ingest_return | calls | forja_post_protocol.py::_write_artifact_checked | EXTRACTED | forja_post_protocol.py:1152 |
| forja_post_protocol.py::ingest_return | calls | forja_post_protocol.py::_learning_candidates | EXTRACTED | forja_post_protocol.py:1161 |
| forja_post_protocol.py::ingest_return | calls | forja_post_protocol.py::_write_artifact_checked | EXTRACTED | forja_post_protocol.py:1165 |
| forja_post_protocol.py::ingest_return | calls | forja_post_protocol.py::_write_artifact_checked | EXTRACTED | forja_post_protocol.py:1182 |
| forja_post_protocol.py::ingest_return | calls | forja_post_protocol.py::_record | EXTRACTED | forja_post_protocol.py:1190 |
| forja_post_protocol.py::ingest_return | calls | forja_post_protocol.py::_record | EXTRACTED | forja_post_protocol.py:1211 |
| forja_post_protocol.py::ingest_return | calls | forja_post_protocol.py::_record | EXTRACTED | forja_post_protocol.py:1228 |
| forja_post_protocol.py::ingest_return | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_post_protocol.py:1250 |
| forja_post_protocol.py::ingest_return | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_post_protocol.py:1251 |
| forja_post_protocol.py::ingest_return | calls | forja_post_protocol.py::_set_index_state | EXTRACTED | forja_post_protocol.py:1252 |
| forja_post_protocol.py::ingest_return | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_post_protocol.py:798 |
| forja_post_protocol.py::ingest_return | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_post_protocol.py:800 |
| forja_post_protocol.py::ingest_return | calls | forja_state_machine.py::load_events | EXTRACTED | forja_post_protocol.py:801 |
| forja_post_protocol.py::ingest_return | calls | forja_state_machine.py::initialize_case | EXTRACTED | forja_post_protocol.py:802 |
| forja_post_protocol.py::ingest_return | calls | forja_n3_common.py::new_id | EXTRACTED | forja_post_protocol.py:803 |
| forja_post_protocol.py::ingest_return | calls | forja_post_protocol.py::_load_index | EXTRACTED | forja_post_protocol.py:831 |
| forja_post_protocol.py::ingest_return | calls | forja_post_protocol.py::_record | EXTRACTED | forja_post_protocol.py:1018 |
| forja_post_protocol.py::ingest_return | calls | forja_post_protocol.py::_record | EXTRACTED | forja_post_protocol.py:1033 |
| forja_post_protocol.py::ingest_return | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_post_protocol.py:1047 |
| forja_post_protocol.py::ingest_return | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_post_protocol.py:1048 |
| forja_post_protocol.py::ingest_return | calls | forja_post_protocol.py::_set_index_state | EXTRACTED | forja_post_protocol.py:1049 |
| forja_post_protocol.py::ingest_return | calls | forja_document_compare.py::compare_documents | EXTRACTED | forja_post_protocol.py:1081 |
| forja_post_protocol.py::ingest_return | calls | forja_post_protocol.py::_block_capture | EXTRACTED | forja_post_protocol.py:1097 |
| forja_post_protocol.py::ingest_return | calls | forja_document_compare.py::render_markdown | EXTRACTED | forja_post_protocol.py:1112 |
| forja_post_protocol.py::ingest_return | calls | forja_n3_common.py::read_json | EXTRACTED | forja_post_protocol.py:1119 |
| forja_post_protocol.py::ingest_return | calls | forja_n3_common.py::read_json | EXTRACTED | forja_post_protocol.py:1123 |
| forja_post_protocol.py::ingest_return | calls | forja_post_protocol.py::_sanitize_changes | EXTRACTED | forja_post_protocol.py:1128 |
| forja_post_protocol.py::ingest_return | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_post_protocol.py:1148 |
| forja_post_protocol.py::ingest_return | calls | forja_post_protocol.py::_regression_proposals | EXTRACTED | forja_post_protocol.py:1180 |
| forja_post_protocol.py::ingest_return | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_post_protocol.py:825 |
| forja_post_protocol.py::ingest_return | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_post_protocol.py:837 |
| forja_post_protocol.py::ingest_return | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_post_protocol.py:839 |
| forja_post_protocol.py::ingest_return | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_post_protocol.py:891 |
| forja_post_protocol.py::ingest_return | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_post_protocol.py:893 |
| forja_post_protocol.py::ingest_return | calls | forja_post_protocol.py::safe_component | EXTRACTED | forja_post_protocol.py:902 |
| forja_post_protocol.py::ingest_return | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_post_protocol.py:917 |
| forja_post_protocol.py::ingest_return | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_post_protocol.py:948 |
| forja_post_protocol.py::ingest_return | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_post_protocol.py:949 |
| forja_post_protocol.py::ingest_return | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_post_protocol.py:956 |
| forja_post_protocol.py::ingest_return | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_post_protocol.py:957 |
| forja_post_protocol.py::ingest_return | calls | forja_post_protocol.py::_block_capture | EXTRACTED | forja_post_protocol.py:1083 |
| forja_post_protocol.py::ingest_return | calls | forja_n3_common.py::read_json | EXTRACTED | forja_post_protocol.py:835 |
| forja_post_protocol.py::ingest_return | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_post_protocol.py:842 |
| forja_post_protocol.py::ingest_return | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_post_protocol.py:843 |
| forja_post_protocol.py::ingest_return | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_post_protocol.py:864 |
| forja_post_protocol.py::ingest_return | calls | forja_post_protocol.py::_index_path | EXTRACTED | forja_post_protocol.py:893 |
| forja_post_protocol.py::ingest_return | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_post_protocol.py:915 |
| forja_post_protocol.py::ingest_return | calls | forja_post_protocol.py::_index_path | EXTRACTED | forja_post_protocol.py:917 |
| forja_post_protocol.py::ingest_return | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_post_protocol.py:921 |
| forja_post_protocol.py::ingest_return | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_post_protocol.py:944 |
| forja_post_protocol.py::ingest_return | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_post_protocol.py:945 |
| forja_post_protocol.py::ingest_return | calls | forja_post_protocol.py::_index_path | EXTRACTED | forja_post_protocol.py:957 |
| forja_post_protocol.py::ingest_return | calls | forja_post_protocol.py::_index_path | EXTRACTED | forja_post_protocol.py:843 |
| forja_post_protocol.py::ingest_return | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_post_protocol.py:863 |
| forja_post_protocol.py::ingest_return | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_post_protocol.py:863 |
| forja_post_protocol.py::ingest_return | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_post_protocol.py:888 |
| forja_post_protocol.py::ingest_return | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_post_protocol.py:920 |
| forja_post_protocol.py::ingest_return | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_post_protocol.py:920 |
| forja_post_protocol.py::ingest_return | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_post_protocol.py:951 |
| forja_post_protocol.py::ingest_return | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_post_protocol.py:952 |
| forja_post_protocol.py::ingest_return | calls | forja_state_machine.py::derive_state | EXTRACTED | forja_post_protocol.py:964 |
| forja_post_protocol.py::ingest_return | calls | forja_post_protocol.py::safe_component | EXTRACTED | forja_post_protocol.py:854 |
| forja_post_protocol.py::promote_learning | calls | forja_post_protocol.py::_require_post_protocol_enabled | EXTRACTED | forja_post_protocol.py:1282 |
| forja_post_protocol.py::promote_learning | calls | forja_post_protocol.py::_learning_payload_for_content | EXTRACTED | forja_post_protocol.py:1285 |
| forja_post_protocol.py::promote_learning | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_post_protocol.py:1362 |
| forja_post_protocol.py::promote_learning | calls | forja_post_protocol_contracts.py::validate_learning_candidate | EXTRACTED | forja_post_protocol.py:1389 |
| forja_post_protocol.py::promote_learning | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_post_protocol.py:1392 |
| forja_post_protocol.py::promote_learning | calls | forja_n4_common.py::expected_content_hash | EXTRACTED | forja_post_protocol.py:1395 |
| forja_post_protocol.py::promote_learning | calls | forja_post_protocol.py::_write_learning_payload | EXTRACTED | forja_post_protocol.py:1396 |
| forja_post_protocol.py::promote_learning | calls | forja_learning.py::validate_learning | EXTRACTED | forja_post_protocol.py:1402 |
| forja_post_protocol.py::promote_learning | calls | forja_post_protocol.py::_write_human_diff_payload | EXTRACTED | forja_post_protocol.py:1407 |
| forja_post_protocol.py::promote_learning | calls | forja_learning_registry.py::register_promoted_rule | EXTRACTED | forja_post_protocol.py:1408 |
| forja_post_protocol.py::promote_learning | calls | forja_state_machine.py::derive_state | EXTRACTED | forja_post_protocol.py:1413 |
| forja_post_protocol.py::promote_learning | calls | forja_post_protocol.py::_record | EXTRACTED | forja_post_protocol.py:1415 |
| forja_post_protocol.py::promote_learning | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_post_protocol.py:1284 |
| forja_post_protocol.py::promote_learning | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_post_protocol.py:1293 |
| forja_post_protocol.py::promote_learning | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_post_protocol.py:1296 |
| forja_post_protocol.py::promote_learning | calls | forja_post_protocol_contracts.py::validate_learning_candidate | EXTRACTED | forja_post_protocol.py:1300 |
| forja_post_protocol.py::promote_learning | calls | forja_learning.py::validate_learning | EXTRACTED | forja_post_protocol.py:1314 |
| forja_post_protocol.py::promote_learning | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_post_protocol.py:1323 |
| forja_post_protocol.py::promote_learning | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_post_protocol.py:1325 |
| forja_post_protocol.py::promote_learning | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_post_protocol.py:1330 |
| forja_post_protocol.py::promote_learning | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_post_protocol.py:1336 |
| forja_post_protocol.py::promote_learning | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_post_protocol.py:1352 |
| forja_post_protocol.py::promote_learning | calls | forja_n3_common.py::sha256_bytes | EXTRACTED | forja_post_protocol.py:1353 |
| forja_post_protocol.py::promote_learning | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_post_protocol.py:1364 |
| forja_post_protocol.py::promote_learning | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_post_protocol.py:1367 |
| forja_post_protocol.py::promote_learning | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_post_protocol.py:1369 |
| forja_post_protocol.py::promote_learning | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_post_protocol.py:1391 |
| forja_post_protocol.py::promote_learning | calls | forja_n3_common.py::read_json | EXTRACTED | forja_post_protocol.py:1398 |
| forja_post_protocol.py::promote_learning | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_post_protocol.py:1404 |
| forja_post_protocol.py::promote_learning | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_post_protocol.py:1302 |
| forja_post_protocol.py::promote_learning | calls | forja_post_protocol.py::_write_learning_payload | EXTRACTED | forja_post_protocol.py:1306 |
| forja_post_protocol.py::promote_learning | calls | forja_n3_common.py::read_json | EXTRACTED | forja_post_protocol.py:1308 |
| forja_post_protocol.py::promote_learning | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_post_protocol.py:1316 |
| forja_post_protocol.py::promote_learning | calls | forja_post_protocol.py::_write_human_diff_payload | EXTRACTED | forja_post_protocol.py:1320 |
| forja_post_protocol.py::promote_learning | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_post_protocol.py:1387 |
| forja_post_protocol.py::promote_learning | calls | forja_post_protocol.py::safe_component | EXTRACTED | forja_post_protocol.py:1360 |
| forja_post_protocol.py::promote_learning | calls | forja_post_protocol.py::_regression_proposals | EXTRACTED | forja_post_protocol.py:1401 |
| forja_post_protocol.py::promote_learning | calls | forja_post_protocol.py::_regression_proposals | EXTRACTED | forja_post_protocol.py:1312 |
| forja_post_protocol.py::_learning_payload_for_content | calls | forja_n3_common.py::read_json | EXTRACTED | forja_post_protocol.py:1447 |
| forja_post_protocol.py::_learning_payload_for_content | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_post_protocol.py:1453 |
| forja_post_protocol.py::_write_learning_payload | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_post_protocol.py:1467 |
| forja_post_protocol.py::_write_learning_payload | calls | forja_n4_common.py::expected_content_hash | EXTRACTED | forja_post_protocol.py:1468 |
| forja_post_protocol.py::_write_learning_payload | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_post_protocol.py:1469 |
| forja_post_protocol.py::_write_learning_payload | calls | forja_n4_common.py::write_artifact | EXTRACTED | forja_post_protocol.py:1463 |
| forja_post_protocol.py::_write_human_diff_payload | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_post_protocol.py:1480 |
| forja_post_protocol.py::_write_human_diff_payload | calls | forja_n4_common.py::expected_content_hash | EXTRACTED | forja_post_protocol.py:1481 |
| forja_post_protocol.py::_write_human_diff_payload | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_post_protocol.py:1482 |
| forja_post_protocol.py::_write_human_diff_payload | calls | forja_n4_common.py::write_artifact | EXTRACTED | forja_post_protocol.py:1476 |
| forja_post_protocol.py::resolve_learning_origin | calls | forja_post_protocol.py::_require_post_protocol_enabled | EXTRACTED | forja_post_protocol.py:1494 |
| forja_post_protocol.py::resolve_learning_origin | calls | forja_post_protocol.py::_learning_payload_for_content | EXTRACTED | forja_post_protocol.py:1499 |
| forja_post_protocol.py::resolve_learning_origin | calls | forja_post_protocol_contracts.py::validate_learning_candidate | EXTRACTED | forja_post_protocol.py:1516 |
| forja_post_protocol.py::resolve_learning_origin | calls | forja_post_protocol.py::_write_learning_payload | EXTRACTED | forja_post_protocol.py:1519 |
| forja_post_protocol.py::resolve_learning_origin | calls | forja_learning.py::validate_learning | EXTRACTED | forja_post_protocol.py:1530 |
| forja_post_protocol.py::resolve_learning_origin | calls | forja_post_protocol.py::_write_human_diff_payload | EXTRACTED | forja_post_protocol.py:1535 |
| forja_post_protocol.py::resolve_learning_origin | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_post_protocol.py:1496 |
| forja_post_protocol.py::resolve_learning_origin | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_post_protocol.py:1498 |
| forja_post_protocol.py::resolve_learning_origin | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_post_protocol.py:1506 |
| forja_post_protocol.py::resolve_learning_origin | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_post_protocol.py:1509 |
| forja_post_protocol.py::resolve_learning_origin | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_post_protocol.py:1518 |
| forja_post_protocol.py::resolve_learning_origin | calls | forja_n3_common.py::read_json | EXTRACTED | forja_post_protocol.py:1521 |
| forja_post_protocol.py::resolve_learning_origin | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_post_protocol.py:1532 |
| forja_post_protocol.py::resolve_learning_origin | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_post_protocol.py:1514 |
| forja_post_protocol.py::resolve_learning_origin | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_post_protocol.py:1528 |
| forja_post_protocol.py::rebuild_comparison | calls | forja_post_protocol.py::_require_post_protocol_enabled | EXTRACTED | forja_post_protocol.py:1541 |
| forja_post_protocol.py::rebuild_comparison | calls | forja_post_protocol.py::_load_index | EXTRACTED | forja_post_protocol.py:1543 |
| forja_post_protocol.py::rebuild_comparison | calls | forja_n3_common.py::read_json | EXTRACTED | forja_post_protocol.py:1548 |
| forja_post_protocol.py::rebuild_comparison | calls | forja_document_compare.py::compare_documents | EXTRACTED | forja_post_protocol.py:1563 |
| forja_post_protocol.py::rebuild_comparison | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_post_protocol.py:1581 |
| forja_post_protocol.py::rebuild_comparison | calls | forja_n3_common.py::atomic_write_text | EXTRACTED | forja_post_protocol.py:1582 |
| forja_post_protocol.py::rebuild_comparison | calls | forja_post_protocol.py::_preserve_change_reviews | EXTRACTED | forja_post_protocol.py:1595 |
| forja_post_protocol.py::rebuild_comparison | calls | forja_post_protocol.py::_write_artifact_checked | EXTRACTED | forja_post_protocol.py:1623 |
| forja_post_protocol.py::rebuild_comparison | calls | forja_post_protocol.py::_learning_candidates | EXTRACTED | forja_post_protocol.py:1632 |
| forja_post_protocol.py::rebuild_comparison | calls | forja_post_protocol.py::_write_artifact_checked | EXTRACTED | forja_post_protocol.py:1636 |
| forja_post_protocol.py::rebuild_comparison | calls | forja_post_protocol.py::_write_artifact_checked | EXTRACTED | forja_post_protocol.py:1644 |
| forja_post_protocol.py::rebuild_comparison | calls | forja_post_protocol.py::_record | EXTRACTED | forja_post_protocol.py:1661 |
| forja_post_protocol.py::rebuild_comparison | calls | forja_post_protocol.py::_record | EXTRACTED | forja_post_protocol.py:1679 |
| forja_post_protocol.py::rebuild_comparison | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_post_protocol.py:1702 |
| forja_post_protocol.py::rebuild_comparison | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_post_protocol.py:1703 |
| forja_post_protocol.py::rebuild_comparison | calls | forja_post_protocol.py::_set_index_state | EXTRACTED | forja_post_protocol.py:1704 |
| forja_post_protocol.py::rebuild_comparison | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_post_protocol.py:1546 |
| forja_post_protocol.py::rebuild_comparison | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_post_protocol.py:1550 |
| forja_post_protocol.py::rebuild_comparison | calls | forja_n3_common.py::read_json | EXTRACTED | forja_post_protocol.py:1551 |
| forja_post_protocol.py::rebuild_comparison | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_post_protocol.py:1559 |
| forja_post_protocol.py::rebuild_comparison | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_post_protocol.py:1561 |
| forja_post_protocol.py::rebuild_comparison | calls | forja_n3_common.py::new_id | EXTRACTED | forja_post_protocol.py:1562 |
| forja_post_protocol.py::rebuild_comparison | calls | forja_post_protocol.py::_block_capture | EXTRACTED | forja_post_protocol.py:1568 |
| forja_post_protocol.py::rebuild_comparison | calls | forja_document_compare.py::render_markdown | EXTRACTED | forja_post_protocol.py:1584 |
| forja_post_protocol.py::rebuild_comparison | calls | forja_n3_common.py::read_json | EXTRACTED | forja_post_protocol.py:1591 |
| forja_post_protocol.py::rebuild_comparison | calls | forja_post_protocol.py::_sanitize_changes | EXTRACTED | forja_post_protocol.py:1596 |
| forja_post_protocol.py::rebuild_comparison | calls | forja_n3_common.py::read_json | EXTRACTED | forja_post_protocol.py:1599 |
| forja_post_protocol.py::rebuild_comparison | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_post_protocol.py:1619 |
| forja_post_protocol.py::rebuild_comparison | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_post_protocol.py:1700 |
| forja_post_protocol.py::rebuild_comparison | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_post_protocol.py:1558 |
| forja_post_protocol.py::rebuild_comparison | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_post_protocol.py:1560 |
| forja_post_protocol.py::rebuild_comparison | calls | forja_post_protocol.py::_regression_proposals | EXTRACTED | forja_post_protocol.py:1654 |
| forja_post_protocol.py::rebuild_comparison | calls | forja_state_machine.py::derive_state | EXTRACTED | forja_post_protocol.py:1660 |
| forja_post_protocol.py::rebuild_comparison | calls | forja_state_machine.py::derive_state | EXTRACTED | forja_post_protocol.py:1621 |
| forja_post_protocol.py::_case_for_demand | calls | forja_n3_common.py::read_json | EXTRACTED | forja_post_protocol.py:1723 |
| forja_post_protocol.py::_case_for_demand | calls | forja_n3_common.py::read_json | EXTRACTED | forja_post_protocol.py:1736 |
| forja_post_protocol.py::_case_for_demand | calls | forja_n3_common.py::read_json | EXTRACTED | forja_post_protocol.py:1737 |
| forja_post_protocol.py::_sender_allowed | calls | forja_n3_common.py::load_config | EXTRACTED | forja_post_protocol.py:1747 |
| forja_post_protocol.py::_sender_allowed | calls | forja_post_protocol.py::_message_header | EXTRACTED | forja_post_protocol.py:1753 |
| forja_post_protocol.py::scan_gmail | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_post_protocol.py:1991 |
| forja_post_protocol.py::scan_gmail | calls | forja_n3_common.py::feature_enabled | EXTRACTED | forja_post_protocol.py:1764 |
| forja_post_protocol.py::scan_gmail | calls | forja_n3_common.py::read_json | EXTRACTED | forja_post_protocol.py:1787 |
| forja_post_protocol.py::scan_gmail | calls | forja_post_protocol.py::_select_return_parts | EXTRACTED | forja_post_protocol.py:1814 |
| forja_post_protocol.py::scan_gmail | calls | forja_post_protocol.py::_message_header | EXTRACTED | forja_post_protocol.py:1833 |
| forja_post_protocol.py::scan_gmail | calls | forja_post_protocol.py::_case_for_demand | EXTRACTED | forja_post_protocol.py:1839 |
| forja_post_protocol.py::scan_gmail | calls | forja_post_protocol.py::resolve_ai_baseline | EXTRACTED | forja_post_protocol.py:1850 |
| forja_post_protocol.py::scan_gmail | calls | forja_post_protocol.py::_message_header | EXTRACTED | forja_post_protocol.py:1906 |
| forja_post_protocol.py::scan_gmail | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_post_protocol.py:1989 |
| forja_post_protocol.py::scan_gmail | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_post_protocol.py:1775 |
| forja_post_protocol.py::scan_gmail | calls | forja_post_protocol.py::_sender_allowed | EXTRACTED | forja_post_protocol.py:1798 |
| forja_post_protocol.py::scan_gmail | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_post_protocol.py:1838 |
| forja_post_protocol.py::scan_gmail | calls | forja_post_protocol.py::backfill_baseline_from_gmail | EXTRACTED | forja_post_protocol.py:1856 |
| forja_post_protocol.py::scan_gmail | calls | forja_post_protocol.py::resolve_ai_baseline | EXTRACTED | forja_post_protocol.py:1888 |
| forja_post_protocol.py::scan_gmail | calls | forja_post_protocol.py::ingest_return | EXTRACTED | forja_post_protocol.py:1956 |
| forja_post_protocol.py::scan_gmail | calls | forja_n3_common.py::sha256_bytes | EXTRACTED | forja_post_protocol.py:1952 |
| forja_post_protocol.py::scan_gmail | calls | forja_n3_common.py::sha256_bytes | EXTRACTED | forja_post_protocol.py:1921 |
| forja_post_protocol.py::main | calls | forja_post_protocol.py::scan_gmail | EXTRACTED | forja_post_protocol.py:2038 |
| forja_post_protocol.py::main | calls | forja_post_protocol.py::promote_learning | EXTRACTED | forja_post_protocol.py:2040 |
| forja_post_protocol.py::main | calls | forja_n3_common.py::resolve_case_dir | EXTRACTED | forja_post_protocol.py:2041 |
| forja_post_protocol.py::main | calls | forja_post_protocol.py::resolve_learning_origin | EXTRACTED | forja_post_protocol.py:2053 |
| forja_post_protocol.py::main | calls | forja_n3_common.py::resolve_case_dir | EXTRACTED | forja_post_protocol.py:2054 |
| forja_post_protocol.py::main | calls | forja_post_protocol.py::rebuild_comparison | EXTRACTED | forja_post_protocol.py:2062 |
| forja_post_protocol.py::main | calls | forja_post_protocol.py::ingest_return | EXTRACTED | forja_post_protocol.py:2064 |
| forja_post_protocol.py::main | calls | forja_n3_common.py::resolve_case_dir | EXTRACTED | forja_post_protocol.py:2062 |
| forja_post_protocol.py::main | calls | forja_n3_common.py::resolve_case_dir | EXTRACTED | forja_post_protocol.py:2065 |
| forja_post_protocol_contracts.py | imports_from | forja_n4_common.py | EXTRACTED | forja_post_protocol_contracts.py:11 |
| forja_post_protocol_contracts.py | imports_from | forja_n4_common.py | EXTRACTED | forja_post_protocol_contracts.py:11 |
| forja_post_protocol_contracts.py | imports_from | forja_n3_common.py | EXTRACTED | forja_post_protocol_contracts.py:259 |
| forja_post_protocol_contracts.py | imports_from | forja_n3_common.py | EXTRACTED | forja_post_protocol_contracts.py:152 |
| forja_post_protocol_contracts.py::_hash_findings | calls | forja_n4_common.py::issue | EXTRACTED | forja_post_protocol_contracts.py:87 |
| forja_post_protocol_contracts.py::_raw_key_findings | calls | forja_post_protocol_contracts.py::_raw_key_findings | EXTRACTED | forja_post_protocol_contracts.py:97 |
| forja_post_protocol_contracts.py::_raw_key_findings | calls | forja_n4_common.py::issue | EXTRACTED | forja_post_protocol_contracts.py:96 |
| forja_post_protocol_contracts.py::_raw_key_findings | calls | forja_post_protocol_contracts.py::_raw_key_findings | EXTRACTED | forja_post_protocol_contracts.py:100 |
| forja_post_protocol_contracts.py::validate_post_protocol_return | calls | forja_post_protocol_contracts.py::_raw_key_findings | EXTRACTED | forja_post_protocol_contracts.py:105 |
| forja_post_protocol_contracts.py::validate_post_protocol_return | calls | forja_post_protocol_contracts.py::_hash_findings | EXTRACTED | forja_post_protocol_contracts.py:106 |
| forja_post_protocol_contracts.py::validate_post_protocol_return | calls | forja_post_protocol_contracts.py::_hash_findings | EXTRACTED | forja_post_protocol_contracts.py:118 |
| forja_post_protocol_contracts.py::validate_post_protocol_return | calls | forja_n4_common.py::issue | EXTRACTED | forja_post_protocol_contracts.py:109 |
| forja_post_protocol_contracts.py::validate_post_protocol_return | calls | forja_n4_common.py::issue | EXTRACTED | forja_post_protocol_contracts.py:112 |
| forja_post_protocol_contracts.py::validate_post_protocol_return | calls | forja_n4_common.py::issue | EXTRACTED | forja_post_protocol_contracts.py:114 |
| forja_post_protocol_contracts.py::validate_post_protocol_return | calls | forja_n4_common.py::issue | EXTRACTED | forja_post_protocol_contracts.py:116 |
| forja_post_protocol_contracts.py::validate_post_protocol_return | calls | forja_n4_common.py::issue | EXTRACTED | forja_post_protocol_contracts.py:121 |
| forja_post_protocol_contracts.py::validate_protocol_evidence | calls | forja_post_protocol_contracts.py::_raw_key_findings | EXTRACTED | forja_post_protocol_contracts.py:126 |
| forja_post_protocol_contracts.py::validate_protocol_evidence | calls | forja_post_protocol_contracts.py::_hash_findings | EXTRACTED | forja_post_protocol_contracts.py:127 |
| forja_post_protocol_contracts.py::validate_protocol_evidence | calls | forja_n4_common.py::issue | EXTRACTED | forja_post_protocol_contracts.py:134 |
| forja_post_protocol_contracts.py::validate_protocol_evidence | calls | forja_n4_common.py::issue | EXTRACTED | forja_post_protocol_contracts.py:159 |
| forja_post_protocol_contracts.py::validate_protocol_evidence | calls | forja_n4_common.py::issue | EXTRACTED | forja_post_protocol_contracts.py:161 |
| forja_post_protocol_contracts.py::validate_protocol_evidence | calls | forja_n4_common.py::issue | EXTRACTED | forja_post_protocol_contracts.py:139 |
| forja_post_protocol_contracts.py::validate_protocol_evidence | calls | forja_n4_common.py::issue | EXTRACTED | forja_post_protocol_contracts.py:141 |
| forja_post_protocol_contracts.py::validate_protocol_evidence | calls | forja_n4_common.py::issue | EXTRACTED | forja_post_protocol_contracts.py:147 |
| forja_post_protocol_contracts.py::validate_protocol_evidence | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_post_protocol_contracts.py:154 |
| forja_post_protocol_contracts.py::validate_protocol_evidence | calls | forja_n4_common.py::issue | EXTRACTED | forja_post_protocol_contracts.py:155 |
| forja_post_protocol_contracts.py::validate_document_comparison | calls | forja_post_protocol_contracts.py::_raw_key_findings | EXTRACTED | forja_post_protocol_contracts.py:166 |
| forja_post_protocol_contracts.py::validate_document_comparison | calls | forja_post_protocol_contracts.py::_hash_findings | EXTRACTED | forja_post_protocol_contracts.py:167 |
| forja_post_protocol_contracts.py::validate_document_comparison | calls | forja_post_protocol_contracts.py::_hash_findings | EXTRACTED | forja_post_protocol_contracts.py:174 |
| forja_post_protocol_contracts.py::validate_document_comparison | calls | forja_post_protocol_contracts.py::_hash_findings | EXTRACTED | forja_post_protocol_contracts.py:170 |
| forja_post_protocol_contracts.py::validate_document_comparison | calls | forja_n4_common.py::issue | EXTRACTED | forja_post_protocol_contracts.py:181 |
| forja_post_protocol_contracts.py::validate_document_comparison | calls | forja_n4_common.py::issue | EXTRACTED | forja_post_protocol_contracts.py:172 |
| forja_post_protocol_contracts.py::validate_learning_candidate | calls | forja_post_protocol_contracts.py::_raw_key_findings | EXTRACTED | forja_post_protocol_contracts.py:187 |
| forja_post_protocol_contracts.py::validate_learning_candidate | calls | forja_post_protocol_contracts.py::_hash_findings | EXTRACTED | forja_post_protocol_contracts.py:188 |
| forja_post_protocol_contracts.py::validate_learning_candidate | calls | forja_n4_common.py::ids_unique | EXTRACTED | forja_post_protocol_contracts.py:189 |
| forja_post_protocol_contracts.py::validate_learning_candidate | calls | forja_n4_common.py::issue | EXTRACTED | forja_post_protocol_contracts.py:193 |
| forja_post_protocol_contracts.py::validate_learning_candidate | calls | forja_n4_common.py::issue | EXTRACTED | forja_post_protocol_contracts.py:195 |
| forja_post_protocol_contracts.py::validate_learning_candidate | calls | forja_n4_common.py::issue | EXTRACTED | forja_post_protocol_contracts.py:197 |
| forja_post_protocol_contracts.py::validate_learning_candidate | calls | forja_n4_common.py::issue | EXTRACTED | forja_post_protocol_contracts.py:199 |
| forja_post_protocol_contracts.py::validate_learning_candidate | calls | forja_n4_common.py::issue | EXTRACTED | forja_post_protocol_contracts.py:201 |
| forja_post_protocol_contracts.py::validate_learning_candidate | calls | forja_n4_common.py::issue | EXTRACTED | forja_post_protocol_contracts.py:203 |
| forja_post_protocol_contracts.py::validate_learning_candidate | calls | forja_n4_common.py::issue | EXTRACTED | forja_post_protocol_contracts.py:242 |
| forja_post_protocol_contracts.py::validate_learning_candidate | calls | forja_n4_common.py::issue | EXTRACTED | forja_post_protocol_contracts.py:206 |
| forja_post_protocol_contracts.py::validate_learning_candidate | calls | forja_n4_common.py::issue | EXTRACTED | forja_post_protocol_contracts.py:217 |
| forja_post_protocol_contracts.py::validate_learning_candidate | calls | forja_n4_common.py::issue | EXTRACTED | forja_post_protocol_contracts.py:220 |
| forja_post_protocol_contracts.py::validate_learning_candidate | calls | forja_n4_common.py::issue | EXTRACTED | forja_post_protocol_contracts.py:222 |
| forja_post_protocol_contracts.py::validate_learning_candidate | calls | forja_n4_common.py::issue | EXTRACTED | forja_post_protocol_contracts.py:226 |
| forja_post_protocol_contracts.py::validate_learning_candidate | calls | forja_n4_common.py::issue | EXTRACTED | forja_post_protocol_contracts.py:236 |
| forja_post_protocol_contracts.py::validate_learning_candidate | calls | forja_n4_common.py::issue | EXTRACTED | forja_post_protocol_contracts.py:240 |
| forja_post_protocol_contracts.py::validate_post_protocol_baseline_backfill | calls | forja_post_protocol_contracts.py::_raw_key_findings | EXTRACTED | forja_post_protocol_contracts.py:247 |
| forja_post_protocol_contracts.py::validate_post_protocol_baseline_backfill | calls | forja_post_protocol_contracts.py::_hash_findings | EXTRACTED | forja_post_protocol_contracts.py:254 |
| forja_post_protocol_contracts.py::validate_post_protocol_baseline_backfill | calls | forja_n4_common.py::issue | EXTRACTED | forja_post_protocol_contracts.py:249 |
| forja_post_protocol_contracts.py::validate_post_protocol_baseline_backfill | calls | forja_n4_common.py::issue | EXTRACTED | forja_post_protocol_contracts.py:251 |
| forja_post_protocol_contracts.py::validate_post_protocol_baseline_backfill | calls | forja_n4_common.py::issue | EXTRACTED | forja_post_protocol_contracts.py:253 |
| forja_post_protocol_contracts.py::validate_post_protocol_baseline_backfill | calls | forja_n4_common.py::issue | EXTRACTED | forja_post_protocol_contracts.py:257 |
| forja_post_protocol_contracts.py::validate_post_protocol_baseline_backfill | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_post_protocol_contracts.py:261 |
| forja_post_protocol_contracts.py::validate_post_protocol_baseline_backfill | calls | forja_n4_common.py::issue | EXTRACTED | forja_post_protocol_contracts.py:262 |
| forja_precedente.py | imports_from | forja_n4_common.py | EXTRACTED | forja_precedente.py:22 |
| forja_precedente.py | imports_from | forja_official_sources.py | EXTRACTED | forja_precedente.py:23 |
| forja_precedente.py::validate_legal_research_trace | calls | forja_n4_common.py::issue | EXTRACTED | forja_precedente.py:86 |
| forja_precedente.py::validate_legal_research_trace | calls | forja_n4_common.py::issue | EXTRACTED | forja_precedente.py:91 |
| forja_precedente.py::validate_legal_research_trace | calls | forja_n4_common.py::issue | EXTRACTED | forja_precedente.py:96 |
| forja_precedente.py::validate_legal_research_trace | calls | forja_n4_common.py::issue | EXTRACTED | forja_precedente.py:101 |
| forja_precedente.py::validate_legal_research_trace | calls | forja_n4_common.py::issue | EXTRACTED | forja_precedente.py:120 |
| forja_precedente.py::validate_legal_research_trace | calls | forja_n4_common.py::issue | EXTRACTED | forja_precedente.py:170 |
| forja_precedente.py::validate_legal_research_trace | calls | forja_n4_common.py::issue | EXTRACTED | forja_precedente.py:103 |
| forja_precedente.py::validate_legal_research_trace | calls | forja_n4_common.py::issue | EXTRACTED | forja_precedente.py:115 |
| forja_precedente.py::validate_legal_research_trace | calls | forja_n4_common.py::issue | EXTRACTED | forja_precedente.py:129 |
| forja_precedente.py::validate_legal_research_trace | calls | forja_n4_common.py::issue | EXTRACTED | forja_precedente.py:134 |
| forja_precedente.py::validate_legal_research_trace | calls | forja_n4_common.py::issue | EXTRACTED | forja_precedente.py:139 |
| forja_precedente.py::validate_legal_research_trace | calls | forja_n4_common.py::issue | EXTRACTED | forja_precedente.py:146 |
| forja_precedente.py::validate_legal_research_trace | calls | forja_n4_common.py::issue | EXTRACTED | forja_precedente.py:152 |
| forja_precedente.py::validate_legal_research_trace | calls | forja_n4_common.py::issue | EXTRACTED | forja_precedente.py:163 |
| forja_precedente.py::_regime_findings | calls | forja_n4_common.py::issue | EXTRACTED | forja_precedente.py:184 |
| forja_precedente.py::_regime_findings | calls | forja_n4_common.py::issue | EXTRACTED | forja_precedente.py:191 |
| forja_precedente.py::_regime_findings | calls | forja_n4_common.py::issue | EXTRACTED | forja_precedente.py:198 |
| forja_precedente.py::_regime_findings | calls | forja_n4_common.py::issue | EXTRACTED | forja_precedente.py:208 |
| forja_precedente.py::_regime_findings | calls | forja_n4_common.py::issue | EXTRACTED | forja_precedente.py:215 |
| forja_precedente.py::_vigencia_findings | calls | forja_n4_common.py::issue | EXTRACTED | forja_precedente.py:228 |
| forja_precedente.py::_vigencia_findings | calls | forja_n4_common.py::issue | EXTRACTED | forja_precedente.py:230 |
| forja_precedente.py::_vigencia_findings | calls | forja_n4_common.py::issue | EXTRACTED | forja_precedente.py:239 |
| forja_precedente.py::_vigencia_findings | calls | forja_n4_common.py::issue | EXTRACTED | forja_precedente.py:245 |
| forja_precedente.py::_vigencia_findings | calls | forja_n4_common.py::issue | EXTRACTED | forja_precedente.py:253 |
| forja_precedente.py::_contrario_findings | calls | forja_n4_common.py::issue | EXTRACTED | forja_precedente.py:264 |
| forja_precedente.py::_contrario_findings | calls | forja_n4_common.py::issue | EXTRACTED | forja_precedente.py:272 |
| forja_precedente.py::_contrario_findings | calls | forja_n4_common.py::issue | EXTRACTED | forja_precedente.py:278 |
| forja_precedente.py::_contrario_findings | calls | forja_n4_common.py::issue | EXTRACTED | forja_precedente.py:282 |
| forja_precedente.py::_contrario_findings | calls | forja_n4_common.py::issue | EXTRACTED | forja_precedente.py:286 |
| forja_precedente.py::validate_anchor_cards | calls | forja_precedente.py::_vigencia_findings | EXTRACTED | forja_precedente.py:401 |
| forja_precedente.py::validate_anchor_cards | calls | forja_precedente.py::_contrario_findings | EXTRACTED | forja_precedente.py:402 |
| forja_precedente.py::validate_anchor_cards | calls | forja_precedente.py::_regime_findings | EXTRACTED | forja_precedente.py:403 |
| forja_precedente.py::validate_anchor_cards | calls | forja_n4_common.py::issue | EXTRACTED | forja_precedente.py:317 |
| forja_precedente.py::validate_anchor_cards | calls | forja_n4_common.py::issue | EXTRACTED | forja_precedente.py:324 |
| forja_precedente.py::validate_anchor_cards | calls | forja_n4_common.py::issue | EXTRACTED | forja_precedente.py:331 |
| forja_precedente.py::validate_anchor_cards | calls | forja_n4_common.py::issue | EXTRACTED | forja_precedente.py:342 |
| forja_precedente.py::validate_anchor_cards | calls | forja_n4_common.py::issue | EXTRACTED | forja_precedente.py:358 |
| forja_precedente.py::validate_anchor_cards | calls | forja_n4_common.py::issue | EXTRACTED | forja_precedente.py:361 |
| forja_precedente.py::validate_anchor_cards | calls | forja_official_sources.py::source_excerpt_sha256 | EXTRACTED | forja_precedente.py:365 |
| forja_precedente.py::validate_anchor_cards | calls | forja_n4_common.py::issue | EXTRACTED | forja_precedente.py:366 |
| forja_precedente.py::validate_anchor_cards | calls | forja_n4_common.py::issue | EXTRACTED | forja_precedente.py:373 |
| forja_precedente.py::validate_anchor_cards | calls | forja_n4_common.py::issue | EXTRACTED | forja_precedente.py:390 |
| forja_precedente.py::validate_anchor_cards | calls | forja_n4_common.py::issue | EXTRACTED | forja_precedente.py:319 |
| forja_precedente.py::validate_anchor_cards | calls | forja_n4_common.py::issue | EXTRACTED | forja_precedente.py:334 |
| forja_precedente.py::validate_anchor_cards | calls | forja_n4_common.py::issue | EXTRACTED | forja_precedente.py:349 |
| forja_precedente.py::validate_anchor_cards | calls | forja_n4_common.py::issue | EXTRACTED | forja_precedente.py:396 |
| forja_produto.py::_conferir | calls | forja_produto.py::_texto | EXTRACTED | forja_produto.py:69 |
| forja_produto.py::validar_definicao_produto | calls | forja_produto.py::_conferir | EXTRACTED | forja_produto.py:110 |
| forja_produto.py::validar_definicao_produto | calls | forja_produto.py::_conferir | EXTRACTED | forja_produto.py:112 |
| forja_produto.py::validar_definicao_produto | calls | forja_produto.py::_conferir | EXTRACTED | forja_produto.py:114 |
| forja_produto.py::validar_pergunta_jurisdicional | calls | forja_produto.py::_texto | EXTRACTED | forja_produto.py:148 |
| forja_produto.py::validar_uso_final | calls | forja_produto.py::_texto | EXTRACTED | forja_produto.py:187 |
| forja_produto.py::validar_uso_final | calls | forja_produto.py::_texto | EXTRACTED | forja_produto.py:188 |
| forja_pso_pet.py | imports_from | forja_n3_common.py | EXTRACTED | forja_pso_pet.py:17 |
| forja_pso_pet.py | imports_from | forja_n3_common.py | EXTRACTED | forja_pso_pet.py:17 |
| forja_pso_pet.py | imports_from | forja_n3_common.py | EXTRACTED | forja_pso_pet.py:17 |
| forja_pso_pet.py | imports_from | forja_n3_common.py | EXTRACTED | forja_pso_pet.py:17 |
| forja_pso_pet.py::_ids | calls | forja_pso_pet.py::issue | EXTRACTED | forja_pso_pet.py:46 |
| forja_pso_pet.py::_ids | calls | forja_pso_pet.py::issue | EXTRACTED | forja_pso_pet.py:48 |
| forja_pso_pet.py::_parse_iso | calls | forja_pso_pet.py::_text | EXTRACTED | forja_pso_pet.py:54 |
| forja_pso_pet.py::_registry | calls | forja_pso_pet.py::_ids | EXTRACTED | forja_pso_pet.py:66 |
| forja_pso_pet.py::_registry | calls | forja_pso_pet.py::issue | EXTRACTED | forja_pso_pet.py:71 |
| forja_pso_pet.py::_registry | calls | forja_pso_pet.py::_text | EXTRACTED | forja_pso_pet.py:72 |
| forja_pso_pet.py::_registry | calls | forja_pso_pet.py::issue | EXTRACTED | forja_pso_pet.py:73 |
| forja_pso_pet.py::_check_refs | calls | forja_pso_pet.py::issue | EXTRACTED | forja_pso_pet.py:87 |
| forja_pso_pet.py::_check_refs | calls | forja_pso_pet.py::issue | EXTRACTED | forja_pso_pet.py:91 |
| forja_pso_pet.py::_check_refs | calls | forja_pso_pet.py::issue | EXTRACTED | forja_pso_pet.py:93 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::_registry | EXTRACTED | forja_pso_pet.py:116 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::_ids | EXTRACTED | forja_pso_pet.py:121 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::_check_refs | EXTRACTED | forja_pso_pet.py:144 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::_ids | EXTRACTED | forja_pso_pet.py:154 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::_ids | EXTRACTED | forja_pso_pet.py:199 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::_text | EXTRACTED | forja_pso_pet.py:103 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::_parse_iso | EXTRACTED | forja_pso_pet.py:107 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::_text | EXTRACTED | forja_pso_pet.py:122 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::_check_refs | EXTRACTED | forja_pso_pet.py:130 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::_text | EXTRACTED | forja_pso_pet.py:145 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::_text | EXTRACTED | forja_pso_pet.py:147 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::_text | EXTRACTED | forja_pso_pet.py:155 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::_text | EXTRACTED | forja_pso_pet.py:157 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::_check_refs | EXTRACTED | forja_pso_pet.py:163 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::_ids | EXTRACTED | forja_pso_pet.py:184 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::_text | EXTRACTED | forja_pso_pet.py:222 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::_text | EXTRACTED | forja_pso_pet.py:250 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::issue | EXTRACTED | forja_pso_pet.py:99 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::issue | EXTRACTED | forja_pso_pet.py:102 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::issue | EXTRACTED | forja_pso_pet.py:104 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::_parse_iso | EXTRACTED | forja_pso_pet.py:108 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::issue | EXTRACTED | forja_pso_pet.py:123 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::issue | EXTRACTED | forja_pso_pet.py:125 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::_text | EXTRACTED | forja_pso_pet.py:128 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::_text | EXTRACTED | forja_pso_pet.py:142 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::_norm | EXTRACTED | forja_pso_pet.py:145 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::_norm | EXTRACTED | forja_pso_pet.py:145 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::issue | EXTRACTED | forja_pso_pet.py:146 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::_norm | EXTRACTED | forja_pso_pet.py:147 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::_norm | EXTRACTED | forja_pso_pet.py:147 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::issue | EXTRACTED | forja_pso_pet.py:148 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::issue | EXTRACTED | forja_pso_pet.py:150 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::issue | EXTRACTED | forja_pso_pet.py:156 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::issue | EXTRACTED | forja_pso_pet.py:158 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::_text | EXTRACTED | forja_pso_pet.py:168 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::issue | EXTRACTED | forja_pso_pet.py:172 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::issue | EXTRACTED | forja_pso_pet.py:203 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::_norm | EXTRACTED | forja_pso_pet.py:207 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::_norm | EXTRACTED | forja_pso_pet.py:207 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::_norm | EXTRACTED | forja_pso_pet.py:207 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::issue | EXTRACTED | forja_pso_pet.py:221 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::issue | EXTRACTED | forja_pso_pet.py:223 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::_text | EXTRACTED | forja_pso_pet.py:224 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::issue | EXTRACTED | forja_pso_pet.py:225 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::issue | EXTRACTED | forja_pso_pet.py:232 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::_text | EXTRACTED | forja_pso_pet.py:240 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::_text | EXTRACTED | forja_pso_pet.py:240 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::issue | EXTRACTED | forja_pso_pet.py:241 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::issue | EXTRACTED | forja_pso_pet.py:243 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::issue | EXTRACTED | forja_pso_pet.py:247 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::issue | EXTRACTED | forja_pso_pet.py:249 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::issue | EXTRACTED | forja_pso_pet.py:251 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::_text | EXTRACTED | forja_pso_pet.py:254 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::issue | EXTRACTED | forja_pso_pet.py:110 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::issue | EXTRACTED | forja_pso_pet.py:112 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::issue | EXTRACTED | forja_pso_pet.py:114 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::issue | EXTRACTED | forja_pso_pet.py:129 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::issue | EXTRACTED | forja_pso_pet.py:132 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::issue | EXTRACTED | forja_pso_pet.py:134 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::issue | EXTRACTED | forja_pso_pet.py:143 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::issue | EXTRACTED | forja_pso_pet.py:162 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::issue | EXTRACTED | forja_pso_pet.py:167 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::issue | EXTRACTED | forja_pso_pet.py:169 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::_text | EXTRACTED | forja_pso_pet.py:174 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::_text | EXTRACTED | forja_pso_pet.py:174 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::issue | EXTRACTED | forja_pso_pet.py:175 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::issue | EXTRACTED | forja_pso_pet.py:183 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::issue | EXTRACTED | forja_pso_pet.py:186 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::_text | EXTRACTED | forja_pso_pet.py:191 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::issue | EXTRACTED | forja_pso_pet.py:209 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::_text | EXTRACTED | forja_pso_pet.py:212 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::issue | EXTRACTED | forja_pso_pet.py:216 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::issue | EXTRACTED | forja_pso_pet.py:235 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::issue | EXTRACTED | forja_pso_pet.py:237 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::issue | EXTRACTED | forja_pso_pet.py:239 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::issue | EXTRACTED | forja_pso_pet.py:255 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::issue | EXTRACTED | forja_pso_pet.py:192 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::issue | EXTRACTED | forja_pso_pet.py:194 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::issue | EXTRACTED | forja_pso_pet.py:196 |
| forja_pso_pet.py::validate_plan | calls | forja_pso_pet.py::issue | EXTRACTED | forja_pso_pet.py:213 |
| forja_pso_pet.py::measure_plan | calls | forja_pso_pet.py::_dimension | EXTRACTED | forja_pso_pet.py:288 |
| forja_pso_pet.py::measure_plan | calls | forja_pso_pet.py::_dimension | EXTRACTED | forja_pso_pet.py:298 |
| forja_pso_pet.py::measure_plan | calls | forja_pso_pet.py::_dimension | EXTRACTED | forja_pso_pet.py:308 |
| forja_pso_pet.py::measure_plan | calls | forja_pso_pet.py::_dimension | EXTRACTED | forja_pso_pet.py:316 |
| forja_pso_pet.py::measure_plan | calls | forja_pso_pet.py::_dimension | EXTRACTED | forja_pso_pet.py:325 |
| forja_pso_pet.py::measure_plan | calls | forja_pso_pet.py::_dimension | EXTRACTED | forja_pso_pet.py:333 |
| forja_pso_pet.py::measure_plan | calls | forja_pso_pet.py::_dimension | EXTRACTED | forja_pso_pet.py:342 |
| forja_pso_pet.py::measure_plan | calls | forja_pso_pet.py::_dimension | EXTRACTED | forja_pso_pet.py:350 |
| forja_pso_pet.py::measure_plan | calls | forja_pso_pet.py::_text | EXTRACTED | forja_pso_pet.py:289 |
| forja_pso_pet.py::measure_plan | calls | forja_pso_pet.py::_text | EXTRACTED | forja_pso_pet.py:292 |
| forja_pso_pet.py::measure_plan | calls | forja_pso_pet.py::_text | EXTRACTED | forja_pso_pet.py:293 |
| forja_pso_pet.py::measure_plan | calls | forja_pso_pet.py::_text | EXTRACTED | forja_pso_pet.py:296 |
| forja_pso_pet.py::measure_plan | calls | forja_pso_pet.py::_text | EXTRACTED | forja_pso_pet.py:299 |
| forja_pso_pet.py::measure_plan | calls | forja_pso_pet.py::_text | EXTRACTED | forja_pso_pet.py:306 |
| forja_pso_pet.py::measure_plan | calls | forja_pso_pet.py::_text | EXTRACTED | forja_pso_pet.py:314 |
| forja_pso_pet.py::measure_plan | calls | forja_pso_pet.py::_text | EXTRACTED | forja_pso_pet.py:329 |
| forja_pso_pet.py::measure_plan | calls | forja_pso_pet.py::_text | EXTRACTED | forja_pso_pet.py:330 |
| forja_pso_pet.py::measure_plan | calls | forja_pso_pet.py::_text | EXTRACTED | forja_pso_pet.py:334 |
| forja_pso_pet.py::measure_plan | calls | forja_pso_pet.py::_text | EXTRACTED | forja_pso_pet.py:335 |
| forja_pso_pet.py::measure_plan | calls | forja_pso_pet.py::_text | EXTRACTED | forja_pso_pet.py:338 |
| forja_pso_pet.py::measure_plan | calls | forja_pso_pet.py::_text | EXTRACTED | forja_pso_pet.py:339 |
| forja_pso_pet.py::measure_plan | calls | forja_pso_pet.py::_text | EXTRACTED | forja_pso_pet.py:354 |
| forja_pso_pet.py::measure_plan | calls | forja_pso_pet.py::_text | EXTRACTED | forja_pso_pet.py:291 |
| forja_pso_pet.py::measure_plan | calls | forja_pso_pet.py::_text | EXTRACTED | forja_pso_pet.py:295 |
| forja_pso_pet.py::measure_plan | calls | forja_pso_pet.py::_text | EXTRACTED | forja_pso_pet.py:340 |
| forja_pso_pet.py::measure_plan | calls | forja_pso_pet.py::_norm | EXTRACTED | forja_pso_pet.py:291 |
| forja_pso_pet.py::measure_plan | calls | forja_pso_pet.py::_norm | EXTRACTED | forja_pso_pet.py:291 |
| forja_pso_pet.py::measure_plan | calls | forja_pso_pet.py::_norm | EXTRACTED | forja_pso_pet.py:295 |
| forja_pso_pet.py::measure_plan | calls | forja_pso_pet.py::_norm | EXTRACTED | forja_pso_pet.py:295 |
| forja_pso_pet.py::measure_plan | calls | forja_pso_pet.py::_text | EXTRACTED | forja_pso_pet.py:355 |
| forja_pso_pet.py::measure_plan | calls | forja_pso_pet.py::_text | EXTRACTED | forja_pso_pet.py:302 |
| forja_pso_pet.py::measure_plan | calls | forja_pso_pet.py::_text | EXTRACTED | forja_pso_pet.py:305 |
| forja_pso_pet.py::measure_plan | calls | forja_pso_pet.py::_text | EXTRACTED | forja_pso_pet.py:311 |
| forja_pso_pet.py::measure_plan | calls | forja_pso_pet.py::_text | EXTRACTED | forja_pso_pet.py:312 |
| forja_pso_pet.py::measure_plan | calls | forja_pso_pet.py::_text | EXTRACTED | forja_pso_pet.py:327 |
| forja_pso_pet.py::measure_plan | calls | forja_pso_pet.py::_text | EXTRACTED | forja_pso_pet.py:328 |
| forja_pso_pet.py::measure_plan | calls | forja_pso_pet.py::_norm | EXTRACTED | forja_pso_pet.py:310 |
| forja_pso_pet.py::measure_plan | calls | forja_pso_pet.py::_norm | EXTRACTED | forja_pso_pet.py:310 |
| forja_pso_pet.py::measure_plan | calls | forja_pso_pet.py::_norm | EXTRACTED | forja_pso_pet.py:310 |
| forja_pso_pet.py::audit_n4_case | calls | forja_n3_common.py::read_json | EXTRACTED | forja_pso_pet.py:410 |
| forja_pso_pet.py::audit_n4_case | calls | forja_pso_pet.py::validate_plan | EXTRACTED | forja_pso_pet.py:412 |
| forja_pso_pet.py::audit_n4_case | calls | forja_pso_pet.py::measure_plan | EXTRACTED | forja_pso_pet.py:414 |
| forja_pso_pet.py::audit_n4_case | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_pso_pet.py:430 |
| forja_pso_pet.py::audit_n4_case | calls | forja_n3_common.py::read_json | EXTRACTED | forja_pso_pet.py:374 |
| forja_pso_pet.py::audit_n4_case | calls | forja_pso_pet.py::issue | EXTRACTED | forja_pso_pet.py:392 |
| forja_pso_pet.py::audit_n4_case | calls | forja_pso_pet.py::issue | EXTRACTED | forja_pso_pet.py:396 |
| forja_pso_pet.py::audit_n4_case | calls | forja_pso_pet.py::issue | EXTRACTED | forja_pso_pet.py:398 |
| forja_pso_pet.py::audit_n4_case | calls | forja_pso_pet.py::issue | EXTRACTED | forja_pso_pet.py:406 |
| forja_pso_pet.py::audit_n4_case | calls | forja_pso_pet.py::issue | EXTRACTED | forja_pso_pet.py:409 |
| forja_pso_pet.py::mutation_benchmark | calls | forja_pso_pet.py::_valid_fixture | EXTRACTED | forja_pso_pet.py:537 |
| forja_pso_pet.py::mutation_benchmark | calls | forja_pso_pet.py::validate_plan | EXTRACTED | forja_pso_pet.py:572 |
| forja_pso_pet.py::mutation_benchmark | calls | forja_pso_pet.py::validate_plan | EXTRACTED | forja_pso_pet.py:557 |
| forja_pso_pet.py::benchmark | calls | forja_pso_pet.py::mutation_benchmark | EXTRACTED | forja_pso_pet.py:593 |
| forja_pso_pet.py::benchmark | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_pso_pet.py:607 |
| forja_pso_pet.py::benchmark | calls | forja_pso_pet.py::audit_n4_case | EXTRACTED | forja_pso_pet.py:592 |
| forja_pso_pet.py::main | calls | forja_n3_common.py::read_json | EXTRACTED | forja_pso_pet.py:624 |
| forja_pso_pet.py::main | calls | forja_pso_pet.py::validate_plan | EXTRACTED | forja_pso_pet.py:625 |
| forja_pso_pet.py::main | calls | forja_pso_pet.py::measure_plan | EXTRACTED | forja_pso_pet.py:625 |
| forja_pso_pet.py::main | calls | forja_pso_pet.py::audit_n4_case | EXTRACTED | forja_pso_pet.py:627 |
| forja_pso_pet.py::main | calls | forja_n3_common.py::resolve_case_dir | EXTRACTED | forja_pso_pet.py:627 |
| forja_pso_pet.py::main | calls | forja_pso_pet.py::benchmark | EXTRACTED | forja_pso_pet.py:629 |
| forja_pso_pet.py::main | calls | forja_pso_pet.py::_valid_fixture | EXTRACTED | forja_pso_pet.py:633 |
| forja_pso_pet.py::main | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_pso_pet.py:634 |
| forja_pso_pet.py::main | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_pso_pet.py:631 |
| forja_qa_paginas.py::analisar_pasta | calls | forja_qa_paginas.py::_densidade | EXTRACTED | forja_qa_paginas.py:54 |
| forja_qa_paginas.py::analisar_pasta | calls | forja_qa_paginas.py::_densidade | EXTRACTED | forja_qa_paginas.py:56 |
| forja_qa_paginas.py::main | calls | forja_qa_paginas.py::analisar_pasta | EXTRACTED | forja_qa_paginas.py:113 |
| forja_reasoning.py | imports_from | forja_n4_common.py | EXTRACTED | forja_reasoning.py:14 |
| forja_reasoning.py | imports_from | forja_n4_common.py | EXTRACTED | forja_reasoning.py:14 |
| forja_reasoning.py | imports_from | forja_n4_common.py | EXTRACTED | forja_reasoning.py:14 |
| forja_reasoning.py | imports_from | forja_n3_common.py | EXTRACTED | forja_reasoning.py:15 |
| forja_reasoning.py | imports_from | forja_exploracao_100.py | EXTRACTED | forja_reasoning.py:16 |
| forja_reasoning.py | imports_from | forja_exploracao_100.py | EXTRACTED | forja_reasoning.py:16 |
| forja_reasoning.py | imports_from | forja_exploracao_100.py | EXTRACTED | forja_reasoning.py:16 |
| forja_reasoning.py::validate_question_tree | calls | forja_n4_common.py::ids_unique | EXTRACTED | forja_reasoning.py:33 |
| forja_reasoning.py::validate_question_tree | calls | forja_exploracao_100.py::validate_exploration_100 | EXTRACTED | forja_reasoning.py:83 |
| forja_reasoning.py::validate_question_tree | calls | forja_n4_common.py::issue | EXTRACTED | forja_reasoning.py:39 |
| forja_reasoning.py::validate_question_tree | calls | forja_n4_common.py::issue | EXTRACTED | forja_reasoning.py:41 |
| forja_reasoning.py::validate_question_tree | calls | forja_n4_common.py::issue | EXTRACTED | forja_reasoning.py:48 |
| forja_reasoning.py::validate_question_tree | calls | forja_n4_common.py::issue | EXTRACTED | forja_reasoning.py:78 |
| forja_reasoning.py::validate_question_tree | calls | forja_n4_common.py::issue | EXTRACTED | forja_reasoning.py:59 |
| forja_reasoning.py::validate_question_tree | calls | forja_n4_common.py::issue | EXTRACTED | forja_reasoning.py:61 |
| forja_reasoning.py::validate_question_tree | calls | forja_n4_common.py::issue | EXTRACTED | forja_reasoning.py:73 |
| forja_reasoning.py::validate_question_tree | calls | forja_n4_common.py::issue | EXTRACTED | forja_reasoning.py:65 |
| forja_reasoning.py::validate_coverage | calls | forja_n4_common.py::ids_unique | EXTRACTED | forja_reasoning.py:91 |
| forja_reasoning.py::validate_coverage | calls | forja_n4_common.py::issue | EXTRACTED | forja_reasoning.py:96 |
| forja_reasoning.py::validate_coverage | calls | forja_n4_common.py::issue | EXTRACTED | forja_reasoning.py:99 |
| forja_reasoning.py::validate_coverage | calls | forja_n4_common.py::issue | EXTRACTED | forja_reasoning.py:101 |
| forja_reasoning.py::validate_coverage | calls | forja_n4_common.py::issue | EXTRACTED | forja_reasoning.py:108 |
| forja_reasoning.py::validate_coverage | calls | forja_n4_common.py::issue | EXTRACTED | forja_reasoning.py:104 |
| forja_reasoning.py::validate_coverage | calls | forja_n4_common.py::issue | EXTRACTED | forja_reasoning.py:106 |
| forja_reasoning.py::validate_graph | calls | forja_reasoning.py::_dependency_cycles | EXTRACTED | forja_reasoning.py:155 |
| forja_reasoning.py::validate_graph | calls | forja_n4_common.py::ids_unique | EXTRACTED | forja_reasoning.py:141 |
| forja_reasoning.py::validate_graph | calls | forja_n4_common.py::ids_unique | EXTRACTED | forja_reasoning.py:141 |
| forja_reasoning.py::validate_graph | calls | forja_n4_common.py::issue | EXTRACTED | forja_reasoning.py:156 |
| forja_reasoning.py::validate_graph | calls | forja_n4_common.py::issue | EXTRACTED | forja_reasoning.py:150 |
| forja_reasoning.py::validate_graph | calls | forja_n4_common.py::issue | EXTRACTED | forja_reasoning.py:152 |
| forja_reasoning.py::validate_graph | calls | forja_n4_common.py::issue | EXTRACTED | forja_reasoning.py:154 |
| forja_reasoning.py::validate_graph | calls | forja_n4_common.py::issue | EXTRACTED | forja_reasoning.py:147 |
| forja_reasoning.py::validate_theses | calls | forja_n4_common.py::ids_unique | EXTRACTED | forja_reasoning.py:162 |
| forja_reasoning.py::validate_theses | calls | forja_n4_common.py::issue | EXTRACTED | forja_reasoning.py:167 |
| forja_reasoning.py::validate_theses | calls | forja_n4_common.py::issue | EXTRACTED | forja_reasoning.py:169 |
| forja_reasoning.py::validate_theses | calls | forja_n4_common.py::issue | EXTRACTED | forja_reasoning.py:171 |
| forja_reasoning.py::validate_theses | calls | forja_n4_common.py::issue | EXTRACTED | forja_reasoning.py:176 |
| forja_reasoning.py::validate_theses | calls | forja_n4_common.py::issue | EXTRACTED | forja_reasoning.py:178 |
| forja_reasoning.py::validate_theses | calls | forja_n4_common.py::issue | EXTRACTED | forja_reasoning.py:180 |
| forja_reasoning.py::validate_conducts | calls | forja_n4_common.py::ids_unique | EXTRACTED | forja_reasoning.py:186 |
| forja_reasoning.py::validate_conducts | calls | forja_n4_common.py::issue | EXTRACTED | forja_reasoning.py:191 |
| forja_reasoning.py::validate_conducts | calls | forja_n4_common.py::issue | EXTRACTED | forja_reasoning.py:193 |
| forja_reasoning.py::validate_conducts | calls | forja_n4_common.py::issue | EXTRACTED | forja_reasoning.py:195 |
| forja_reasoning.py::validate_decision_factors | calls | forja_n4_common.py::ids_unique | EXTRACTED | forja_reasoning.py:200 |
| forja_reasoning.py::validate_decision_factors | calls | forja_n4_common.py::issue | EXTRACTED | forja_reasoning.py:203 |
| forja_reasoning.py::validate_decision_factors | calls | forja_n4_common.py::issue | EXTRACTED | forja_reasoning.py:206 |
| forja_reasoning.py::validate_recipient_map | calls | forja_reasoning.py::_fontes_do_mapa | EXTRACTED | forja_reasoning.py:286 |
| forja_reasoning.py::validate_recipient_map | calls | forja_n4_common.py::issue | EXTRACTED | forja_reasoning.py:277 |
| forja_reasoning.py::validate_recipient_map | calls | forja_n4_common.py::issue | EXTRACTED | forja_reasoning.py:302 |
| forja_reasoning.py::validate_recipient_map | calls | forja_n4_common.py::issue | EXTRACTED | forja_reasoning.py:345 |
| forja_reasoning.py::validate_recipient_map | calls | forja_n4_common.py::issue | EXTRACTED | forja_reasoning.py:285 |
| forja_reasoning.py::validate_recipient_map | calls | forja_reasoning.py::nivel_probatorio | EXTRACTED | forja_reasoning.py:294 |
| forja_reasoning.py::validate_recipient_map | calls | forja_n4_common.py::issue | EXTRACTED | forja_reasoning.py:310 |
| forja_reasoning.py::validate_recipient_map | calls | forja_n4_common.py::issue | EXTRACTED | forja_reasoning.py:320 |
| forja_reasoning.py::validate_recipient_map | calls | forja_reasoning.py::_idade_em_horas | EXTRACTED | forja_reasoning.py:327 |
| forja_reasoning.py::validate_recipient_map | calls | forja_n4_common.py::issue | EXTRACTED | forja_reasoning.py:336 |
| forja_reasoning.py::validate_recipient_map | calls | forja_n4_common.py::issue | EXTRACTED | forja_reasoning.py:315 |
| forja_reasoning.py::validate_recipient_map | calls | forja_n4_common.py::issue | EXTRACTED | forja_reasoning.py:329 |
| forja_reasoning.py::validate_signature_brief | calls | forja_n4_common.py::ids_unique | EXTRACTED | forja_reasoning.py:358 |
| forja_reasoning.py::validate_signature_brief | calls | forja_n4_common.py::issue | EXTRACTED | forja_reasoning.py:356 |
| forja_reasoning.py::validate_signature_brief | calls | forja_n4_common.py::issue | EXTRACTED | forja_reasoning.py:380 |
| forja_reasoning.py::validate_signature_brief | calls | forja_n4_common.py::issue | EXTRACTED | forja_reasoning.py:382 |
| forja_reasoning.py::validate_signature_brief | calls | forja_n4_common.py::issue | EXTRACTED | forja_reasoning.py:372 |
| forja_reasoning.py::validate_signature_brief | calls | forja_n4_common.py::issue | EXTRACTED | forja_reasoning.py:388 |
| forja_reasoning.py::validate_signature_brief | calls | forja_n4_common.py::issue | EXTRACTED | forja_reasoning.py:398 |
| forja_reasoning.py::validate_signature_brief | calls | forja_n4_common.py::issue | EXTRACTED | forja_reasoning.py:403 |
| forja_reasoning.py::validate_signature_brief | calls | forja_n4_common.py::issue | EXTRACTED | forja_reasoning.py:393 |
| forja_reasoning.py::validate_signature_brief | calls | forja_n4_common.py::issue | EXTRACTED | forja_reasoning.py:413 |
| forja_reasoning.py::validate_signature_brief | calls | forja_n4_common.py::issue | EXTRACTED | forja_reasoning.py:419 |
| forja_reasoning.py::validate_brief_references | calls | forja_reasoning.py::_pool_de_ids | EXTRACTED | forja_reasoning.py:461 |
| forja_reasoning.py::validate_brief_references | calls | forja_reasoning.py::_pool_de_ids | EXTRACTED | forja_reasoning.py:462 |
| forja_reasoning.py::validate_brief_references | calls | forja_reasoning.py::_pool_de_ids | EXTRACTED | forja_reasoning.py:456 |
| forja_reasoning.py::validate_brief_references | calls | forja_reasoning.py::_pool_de_ids | EXTRACTED | forja_reasoning.py:458 |
| forja_reasoning.py::validate_brief_references | calls | forja_n4_common.py::issue | EXTRACTED | forja_reasoning.py:487 |
| forja_reasoning.py::validate_brief_references | calls | forja_n4_common.py::issue | EXTRACTED | forja_reasoning.py:501 |
| forja_reasoning.py::validate_brief_references | calls | forja_n4_common.py::issue | EXTRACTED | forja_reasoning.py:472 |
| forja_reasoning.py::validate_brief_references | calls | forja_n4_common.py::issue | EXTRACTED | forja_reasoning.py:496 |
| forja_reasoning.py::validate_case | calls | forja_n4_common.py::validate_file | EXTRACTED | forja_reasoning.py:524 |
| forja_reasoning.py::validate_case | calls | forja_reasoning.py::validate_brief_references | EXTRACTED | forja_reasoning.py:531 |
| forja_reasoning.py::main | calls | forja_reasoning.py::validate_case | EXTRACTED | forja_reasoning.py:539 |
| forja_reasoning.py::main | calls | forja_n3_common.py::resolve_case_dir | EXTRACTED | forja_reasoning.py:539 |
| forja_recomputo_censo.py | imports_from | forja_injection_scan.py | EXTRACTED | forja_recomputo_censo.py:97 |
| forja_recomputo_censo.py | imports_from | forja_ingestao.py | EXTRACTED | forja_recomputo_censo.py:98 |
| forja_recomputo_censo.py | imports_from | forja_exploracao_100.py | EXTRACTED | forja_recomputo_censo.py:99 |
| forja_recomputo_censo.py | imports_from | forja_produto.py | EXTRACTED | forja_recomputo_censo.py:100 |
| forja_recomputo_censo.py | imports_from | forja_produto.py | EXTRACTED | forja_recomputo_censo.py:100 |
| forja_recomputo_censo.py | imports_from | forja_produto.py | EXTRACTED | forja_recomputo_censo.py:100 |
| forja_recomputo_censo.py | imports_from | forja_regimento_gate.py | EXTRACTED | forja_recomputo_censo.py:102 |
| forja_recomputo_censo.py | imports_from | forja_adversarial_gate.py | EXTRACTED | forja_recomputo_censo.py:103 |
| forja_recomputo_censo.py | imports_from | forja_adversarial_gate.py | EXTRACTED | forja_recomputo_censo.py:103 |
| forja_recomputo_censo.py | imports_from | forja_conselho.py | EXTRACTED | forja_recomputo_censo.py:104 |
| forja_recomputo_censo.py | imports_from | forja_fontes_oficiais.py | EXTRACTED | forja_recomputo_censo.py:105 |
| forja_recomputo_censo.py | imports_from | forja_paragrafos.py | EXTRACTED | forja_recomputo_censo.py:106 |
| forja_recomputo_censo.py | imports_from | forja_redacao.py | EXTRACTED | forja_recomputo_censo.py:107 |
| forja_recomputo_censo.py | imports_from | forja_contexto.py | EXTRACTED | forja_recomputo_censo.py:108 |
| forja_recomputo_censo.py | imports_from | forja_red_team.py | EXTRACTED | forja_recomputo_censo.py:109 |
| forja_recomputo_censo.py | imports_from | forja_p0.py | EXTRACTED | forja_recomputo_censo.py:110 |
| forja_recomputo_censo.py | imports_from | forja_replay.py | EXTRACTED | forja_recomputo_censo.py:111 |
| forja_recomputo_censo.py | imports_from | forja_entrega.py | EXTRACTED | forja_recomputo_censo.py:112 |
| forja_recomputo_censo.py | imports_from | forja_entrega.py | EXTRACTED | forja_recomputo_censo.py:112 |
| forja_recomputo_censo.py | imports_from | forja_run.py | EXTRACTED | forja_recomputo_censo.py:205 |
| forja_recomputo_censo.py | imports_from | forja_fontes_oficiais.py | EXTRACTED | forja_recomputo_censo.py:179 |
| forja_recomputo_censo.py::_irmao_promovido | calls | forja_recomputo_censo.py::_raiz_do_caso | EXTRACTED | forja_recomputo_censo.py:85 |
| forja_recomputo_censo.py::_produtores | calls | forja_recomputo_censo.py::_ler | EXTRACTED | forja_recomputo_censo.py:130 |
| forja_recomputo_censo.py::_produtores | calls | forja_recomputo_censo.py::_texto | EXTRACTED | forja_recomputo_censo.py:131 |
| forja_recomputo_censo.py::_produtores | calls | forja_recomputo_censo.py::_ler | EXTRACTED | forja_recomputo_censo.py:132 |
| forja_recomputo_censo.py::_produtores | calls | forja_recomputo_censo.py::_texto | EXTRACTED | forja_recomputo_censo.py:133 |
| forja_recomputo_censo.py::_produtores | calls | forja_recomputo_censo.py::_ler | EXTRACTED | forja_recomputo_censo.py:183 |
| forja_recomputo_censo.py::_produtores | calls | forja_recomputo_censo.py::_texto | EXTRACTED | forja_recomputo_censo.py:184 |
| forja_recomputo_censo.py::_produtores | calls | forja_recomputo_censo.py::_ler | EXTRACTED | forja_recomputo_censo.py:206 |
| forja_recomputo_censo.py::_produtores | calls | forja_run.py::_compute_lastro_gates | EXTRACTED | forja_recomputo_censo.py:207 |
| forja_recomputo_censo.py::_produtores | calls | forja_recomputo_censo.py::_ler | EXTRACTED | forja_recomputo_censo.py:251 |
| forja_recomputo_censo.py::_produtores | calls | forja_injection_scan.py::validar_triagem_injecao | EXTRACTED | forja_recomputo_censo.py:115 |
| forja_recomputo_censo.py::_produtores | calls | forja_ingestao.py::validar_ingestao | EXTRACTED | forja_recomputo_censo.py:117 |
| forja_recomputo_censo.py::_produtores | calls | forja_exploracao_100.py::gates_da_exploracao | EXTRACTED | forja_recomputo_censo.py:120 |
| forja_recomputo_censo.py::_produtores | calls | forja_produto.py::validar_definicao_produto | EXTRACTED | forja_recomputo_censo.py:122 |
| forja_recomputo_censo.py::_produtores | calls | forja_regimento_gate.py::validar_regimento | EXTRACTED | forja_recomputo_censo.py:135 |
| forja_recomputo_censo.py::_produtores | calls | forja_recomputo_censo.py::_irmao_promovido | EXTRACTED | forja_recomputo_censo.py:139 |
| forja_recomputo_censo.py::_produtores | calls | forja_recomputo_censo.py::_irmao_promovido | EXTRACTED | forja_recomputo_censo.py:152 |
| forja_recomputo_censo.py::_produtores | calls | forja_conselho.py::validar_conselho | EXTRACTED | forja_recomputo_censo.py:161 |
| forja_recomputo_censo.py::_produtores | calls | forja_recomputo_censo.py::_texto | EXTRACTED | forja_recomputo_censo.py:172 |
| forja_recomputo_censo.py::_produtores | calls | forja_produto.py::validar_uso_final | EXTRACTED | forja_recomputo_censo.py:181 |
| forja_recomputo_censo.py::_produtores | calls | forja_paragrafos.py::validar_paragrafos_lastreados | EXTRACTED | forja_recomputo_censo.py:185 |
| forja_recomputo_censo.py::_produtores | calls | forja_redacao.py::validar_redacao | EXTRACTED | forja_recomputo_censo.py:186 |
| forja_recomputo_censo.py::_produtores | calls | forja_recomputo_censo.py::_texto | EXTRACTED | forja_recomputo_censo.py:188 |
| forja_recomputo_censo.py::_produtores | calls | forja_recomputo_censo.py::_texto | EXTRACTED | forja_recomputo_censo.py:188 |
| forja_recomputo_censo.py::_produtores | calls | forja_contexto.py::validar_contexto | EXTRACTED | forja_recomputo_censo.py:189 |
| forja_recomputo_censo.py::_produtores | calls | forja_red_team.py::validar_exame_adversarial | EXTRACTED | forja_recomputo_censo.py:192 |
| forja_recomputo_censo.py::_produtores | calls | forja_p0.py::validar_p0 | EXTRACTED | forja_recomputo_censo.py:195 |
| forja_recomputo_censo.py::_produtores | calls | forja_recomputo_censo.py::_artefatos_da_tentativa | EXTRACTED | forja_recomputo_censo.py:208 |
| forja_recomputo_censo.py::_produtores | calls | forja_replay.py::validar_replay | EXTRACTED | forja_recomputo_censo.py:217 |
| forja_recomputo_censo.py::_produtores | calls | forja_recomputo_censo.py::_texto | EXTRACTED | forja_recomputo_censo.py:235 |
| forja_recomputo_censo.py::_produtores | calls | forja_recomputo_censo.py::_ler | EXTRACTED | forja_recomputo_censo.py:236 |
| forja_recomputo_censo.py::_produtores | calls | forja_entrega.py::validar_reconciliacao | EXTRACTED | forja_recomputo_censo.py:237 |
| forja_recomputo_censo.py::_produtores | calls | forja_recomputo_censo.py::_artefatos_da_tentativa | EXTRACTED | forja_recomputo_censo.py:246 |
| forja_recomputo_censo.py::_produtores | calls | forja_recomputo_censo.py::_texto | EXTRACTED | forja_recomputo_censo.py:253 |
| forja_recomputo_censo.py::_produtores | calls | forja_entrega.py::validar_pacote | EXTRACTED | forja_recomputo_censo.py:254 |
| forja_recomputo_censo.py::_produtores | calls | forja_adversarial_gate.py::validar_politica_liberacao | EXTRACTED | forja_recomputo_censo.py:256 |
| forja_recomputo_censo.py::_produtores | calls | forja_recomputo_censo.py::_ler | EXTRACTED | forja_recomputo_censo.py:115 |
| forja_recomputo_censo.py::_produtores | calls | forja_recomputo_censo.py::_ler | EXTRACTED | forja_recomputo_censo.py:117 |
| forja_recomputo_censo.py::_produtores | calls | forja_recomputo_censo.py::_ler | EXTRACTED | forja_recomputo_censo.py:118 |
| forja_recomputo_censo.py::_produtores | calls | forja_recomputo_censo.py::_ler | EXTRACTED | forja_recomputo_censo.py:120 |
| forja_recomputo_censo.py::_produtores | calls | forja_recomputo_censo.py::_ler | EXTRACTED | forja_recomputo_censo.py:122 |
| forja_recomputo_censo.py::_produtores | calls | forja_recomputo_censo.py::_texto | EXTRACTED | forja_recomputo_censo.py:125 |
| forja_recomputo_censo.py::_produtores | calls | forja_recomputo_censo.py::_ler | EXTRACTED | forja_recomputo_censo.py:125 |
| forja_recomputo_censo.py::_produtores | calls | forja_produto.py::validar_pergunta_jurisdicional | EXTRACTED | forja_recomputo_censo.py:126 |
| forja_recomputo_censo.py::_produtores | calls | forja_adversarial_gate.py::validar_auditoria_adversarial | EXTRACTED | forja_recomputo_censo.py:157 |
| forja_recomputo_censo.py::_produtores | calls | forja_recomputo_censo.py::_ler | EXTRACTED | forja_recomputo_censo.py:173 |
| forja_recomputo_censo.py::_produtores | calls | forja_fontes_oficiais.py::validar_pesquisa_oficial | EXTRACTED | forja_recomputo_censo.py:176 |
| forja_recomputo_censo.py::_produtores | calls | forja_fontes_oficiais.py::validar_fontes_arquivadas | EXTRACTED | forja_recomputo_censo.py:180 |
| forja_recomputo_censo.py::_produtores | calls | forja_recomputo_censo.py::_ler | EXTRACTED | forja_recomputo_censo.py:181 |
| forja_recomputo_censo.py::_produtores | calls | forja_recomputo_censo.py::_ler | EXTRACTED | forja_recomputo_censo.py:189 |
| forja_recomputo_censo.py::_produtores | calls | forja_recomputo_censo.py::_ler | EXTRACTED | forja_recomputo_censo.py:190 |
| forja_recomputo_censo.py::_produtores | calls | forja_recomputo_censo.py::_texto | EXTRACTED | forja_recomputo_censo.py:192 |
| forja_recomputo_censo.py::_produtores | calls | forja_recomputo_censo.py::_ler | EXTRACTED | forja_recomputo_censo.py:193 |
| forja_recomputo_censo.py::_produtores | calls | forja_recomputo_censo.py::_ler | EXTRACTED | forja_recomputo_censo.py:195 |
| forja_recomputo_censo.py::_produtores | calls | forja_recomputo_censo.py::_ler | EXTRACTED | forja_recomputo_censo.py:217 |
| forja_recomputo_censo.py::_produtores | calls | forja_recomputo_censo.py::_ler | EXTRACTED | forja_recomputo_censo.py:237 |
| forja_recomputo_censo.py::_produtores | calls | forja_recomputo_censo.py::_texto | EXTRACTED | forja_recomputo_censo.py:253 |
| forja_recomputo_censo.py::_produtores | calls | forja_recomputo_censo.py::_ler | EXTRACTED | forja_recomputo_censo.py:256 |
| forja_recomputo_censo.py::_produtores | calls | forja_recomputo_censo.py::_ler | EXTRACTED | forja_recomputo_censo.py:158 |
| forja_recomputo_censo.py::_produtores | calls | forja_recomputo_censo.py::_ler | EXTRACTED | forja_recomputo_censo.py:158 |
| forja_recomputo_censo.py::_produtores | calls | forja_recomputo_censo.py::_ler | EXTRACTED | forja_recomputo_censo.py:176 |
| forja_recomputo_censo.py::_produtores | calls | forja_recomputo_censo.py::_ler | EXTRACTED | forja_recomputo_censo.py:180 |
| forja_recomputo_censo.py::censo | calls | forja_recomputo_censo.py::_ler | EXTRACTED | forja_recomputo_censo.py:273 |
| forja_recomputo_censo.py::censo | calls | forja_recomputo_censo.py::_produtores | EXTRACTED | forja_recomputo_censo.py:278 |
| forja_reconcile.py | imports_from | forja_n3_common.py | EXTRACTED | forja_reconcile.py:21 |
| forja_reconcile.py | imports_from | forja_n3_common.py | EXTRACTED | forja_reconcile.py:21 |
| forja_reconcile.py | imports_from | forja_n3_common.py | EXTRACTED | forja_reconcile.py:334 |
| forja_reconcile.py | imports_from | forja_fila.py | EXTRACTED | forja_reconcile.py:336 |
| forja_reconcile.py::auditar_demanda | calls | forja_reconcile.py::evidencia_de_entrega | EXTRACTED | forja_reconcile.py:181 |
| forja_reconcile.py::auditar_demanda | calls | forja_reconcile.py::finding | EXTRACTED | forja_reconcile.py:141 |
| forja_reconcile.py::auditar_demanda | calls | forja_reconcile.py::finding | EXTRACTED | forja_reconcile.py:147 |
| forja_reconcile.py::auditar_demanda | calls | forja_reconcile.py::finding | EXTRACTED | forja_reconcile.py:172 |
| forja_reconcile.py::auditar_demanda | calls | forja_reconcile.py::finding | EXTRACTED | forja_reconcile.py:174 |
| forja_reconcile.py::auditar_demanda | calls | forja_reconcile.py::finding | EXTRACTED | forja_reconcile.py:178 |
| forja_reconcile.py::auditar_demanda | calls | forja_reconcile.py::finding | EXTRACTED | forja_reconcile.py:183 |
| forja_reconcile.py::auditar_demanda | calls | forja_reconcile.py::finding | EXTRACTED | forja_reconcile.py:149 |
| forja_reconcile.py::auditar_demanda | calls | forja_reconcile.py::finding | EXTRACTED | forja_reconcile.py:159 |
| forja_reconcile.py::auditar_demanda | calls | forja_reconcile.py::finding | EXTRACTED | forja_reconcile.py:164 |
| forja_reconcile.py::auditar_demanda | calls | forja_reconcile.py::finding | EXTRACTED | forja_reconcile.py:152 |
| forja_reconcile.py::gravar_state | calls | forja_n3_common.py::read_json | EXTRACTED | forja_reconcile.py:202 |
| forja_reconcile.py::gravar_state | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_reconcile.py:213 |
| forja_reconcile.py::gravar_state | calls | forja_reconcile.py::reconciliar_gates | EXTRACTED | forja_reconcile.py:214 |
| forja_reconcile.py::gravar_state | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_reconcile.py:223 |
| forja_reconcile.py::main | calls | forja_n3_common.py::read_json | EXTRACTED | forja_reconcile.py:251 |
| forja_reconcile.py::main | calls | forja_n3_common.py::read_json | EXTRACTED | forja_reconcile.py:252 |
| forja_reconcile.py::main | calls | forja_n3_common.py::read_json | EXTRACTED | forja_reconcile.py:253 |
| forja_reconcile.py::main | calls | forja_n3_common.py::read_json | EXTRACTED | forja_reconcile.py:254 |
| forja_reconcile.py::main | calls | forja_n3_common.py::read_json | EXTRACTED | forja_reconcile.py:255 |
| forja_reconcile.py::main | calls | forja_reconcile.py::classificar_integracoes | EXTRACTED | forja_reconcile.py:257 |
| forja_reconcile.py::main | calls | forja_reconcile.py::auditar_demanda | EXTRACTED | forja_reconcile.py:262 |
| forja_reconcile.py::main | calls | forja_reconcile.py::gravar_state | EXTRACTED | forja_reconcile.py:265 |
| forja_reconcile.py::main | calls | forja_n3_common.py::feature_enabled | EXTRACTED | forja_reconcile.py:335 |
| forja_reconcile.py::main | calls | forja_fila.py::gerar | EXTRACTED | forja_reconcile.py:337 |
| forja_reconcile.py::main | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_reconcile.py:287 |
| forja_red_team.py::validar_red_team | calls | forja_red_team.py::_itens_enumerados | EXTRACTED | forja_red_team.py:63 |
| forja_red_team.py::validar_recheck_adversarial | calls | forja_red_team.py::_itens_rechecados | EXTRACTED | forja_red_team.py:111 |
| forja_red_team.py::validar_exame_adversarial | calls | forja_red_team.py::validar_red_team | EXTRACTED | forja_red_team.py:176 |
| forja_red_team.py::validar_exame_adversarial | calls | forja_red_team.py::validar_recheck_adversarial | EXTRACTED | forja_red_team.py:177 |
| forja_redacao.py | imports_from | forja_editorial_fidelity.py | EXTRACTED | forja_redacao.py:40 |
| forja_redacao.py | imports_from | forja_estilo_humano.py | EXTRACTED | forja_redacao.py:50 |
| forja_redacao.py::_estilo_p0 | calls | forja_estilo_humano.py::analisar | EXTRACTED | forja_redacao.py:51 |
| forja_redacao.py::validar_redacao | calls | forja_redacao.py::_origem_operacional | EXTRACTED | forja_redacao.py:71 |
| forja_redacao.py::validar_redacao | calls | forja_redacao.py::_estilo_p0 | EXTRACTED | forja_redacao.py:80 |
| forja_regimento_gate.py::validar_regimento | calls | forja_regimento_gate.py::_bloco | EXTRACTED | forja_regimento_gate.py:136 |
| forja_regimento_gate.py::validar_regimento | calls | forja_regimento_gate.py::_bloco | EXTRACTED | forja_regimento_gate.py:158 |
| forja_regimento_gate.py::validar_regimento | calls | forja_regimento_gate.py::_mapa_em_texto | EXTRACTED | forja_regimento_gate.py:120 |
| forja_regimento_gate.py::validar_regimento | calls | forja_regimento_gate.py::_fatos_em_texto | EXTRACTED | forja_regimento_gate.py:122 |
| forja_regimentos.py::_data_do_rotulo | calls | forja_regimentos.py::_extrai_data | EXTRACTED | forja_regimentos.py:145 |
| forja_regimentos.py::auditar_arquivo | calls | forja_regimentos.py::Regimento | EXTRACTED | forja_regimentos.py:171 |
| forja_regimentos.py::auditar_arquivo | calls | forja_regimentos.py::_primeiro | EXTRACTED | forja_regimentos.py:173 |
| forja_regimentos.py::auditar_arquivo | calls | forja_regimentos.py::_data_do_rotulo | EXTRACTED | forja_regimentos.py:174 |
| forja_regimentos.py::auditar | calls | forja_regimentos.py::auditar_arquivo | EXTRACTED | forja_regimentos.py:217 |
| forja_regimentos.py::main | calls | forja_regimentos.py::auditar | EXTRACTED | forja_regimentos.py:252 |
| forja_regimentos.py::main | calls | forja_regimentos.py::_relatorio | EXTRACTED | forja_regimentos.py:258 |
| forja_regua.py::hashes_atuais | calls | forja_regua.py::sha256_arquivo | EXTRACTED | forja_regua.py:292 |
| forja_regua.py::verificar_integridade | calls | forja_regua.py::hashes_atuais | EXTRACTED | forja_regua.py:311 |
| forja_regua.py::verificar_integridade | calls | forja_regua.py::_manifest_key | EXTRACTED | forja_regua.py:305 |
| forja_regua.py::rebaseline | calls | forja_regua.py::hashes_atuais | EXTRACTED | forja_regua.py:327 |
| forja_regua.py::rebaseline | calls | forja_regua.py::_manifest_key | EXTRACTED | forja_regua.py:326 |
| forja_regua.py::main | calls | forja_regua.py::verificar_integridade | EXTRACTED | forja_regua.py:391 |
| forja_regua.py::main | calls | forja_regua.py::rebaseline | EXTRACTED | forja_regua.py:378 |
| forja_regua.py::main | calls | forja_regua.py::rodar_suite | EXTRACTED | forja_regua.py:411 |
| forja_regua.py::main | calls | forja_regua.py::rodar_suite | EXTRACTED | forja_regua.py:422 |
| forja_release_audit.py | imports_from | forja_n3_common.py | EXTRACTED | forja_release_audit.py:9 |
| forja_release_audit.py | imports_from | forja_n3_common.py | EXTRACTED | forja_release_audit.py:9 |
| forja_release_audit.py | imports_from | forja_n3_common.py | EXTRACTED | forja_release_audit.py:9 |
| forja_release_audit.py | imports_from | forja_package.py | EXTRACTED | forja_release_audit.py:10 |
| forja_release_audit.py | imports_from | forja_package.py | EXTRACTED | forja_release_audit.py:10 |
| forja_release_audit.py | imports_from | forja_package.py | EXTRACTED | forja_release_audit.py:10 |
| forja_release_audit.py::audit_packages | calls | forja_n3_common.py::read_json | EXTRACTED | forja_release_audit.py:17 |
| forja_release_audit.py::audit_packages | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_release_audit.py:36 |
| forja_release_audit.py::audit_packages | calls | forja_package.py::release_policy_hash | EXTRACTED | forja_release_audit.py:38 |
| forja_release_audit.py::audit_packages | calls | forja_package.py::revalidate_package_manifest | EXTRACTED | forja_release_audit.py:22 |
| forja_release_audit.py::main | calls | forja_release_audit.py::audit_packages | EXTRACTED | forja_release_audit.py:52 |
| forja_release_audit.py::main | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_release_audit.py:54 |
| forja_render_docx.py | imports_from | forja_docx_layout.py | EXTRACTED | forja_render_docx.py:29 |
| forja_render_docx.py | imports_from | forja_n3_common.py | EXTRACTED | forja_render_docx.py:30 |
| forja_render_docx.py | imports_from | forja_n3_common.py | EXTRACTED | forja_render_docx.py:30 |
| forja_render_docx.py | imports_from | forja_visual_review.py | EXTRACTED | forja_render_docx.py:31 |
| forja_render_docx.py | imports_from | forja_metadata.py | EXTRACTED | forja_render_docx.py:32 |
| forja_render_docx.py | imports_from | forja_verificador.py | EXTRACTED | forja_render_docx.py:95 |
| forja_render_docx.py | imports_from | forja_lastro.py | EXTRACTED | forja_render_docx.py:96 |
| forja_render_docx.py | imports_from | forja_metricas_f7.py | EXTRACTED | forja_render_docx.py:97 |
| forja_render_docx.py | imports_from | forja_metadata.py | EXTRACTED | forja_render_docx.py:120 |
| forja_render_docx.py | imports_from | forja_metadata.py | EXTRACTED | forja_render_docx.py:282 |
| forja_render_docx.py::render | calls | forja_verificador.py::verificar | EXTRACTED | forja_render_docx.py:106 |
| forja_render_docx.py::render | calls | forja_metadata.py::retry_transient_io | EXTRACTED | forja_render_docx.py:121 |
| forja_render_docx.py::render | calls | forja_render_docx.py::limpar_corpo | EXTRACTED | forja_render_docx.py:135 |
| forja_render_docx.py::render | calls | forja_docx_layout.py::normalize_medina_body | EXTRACTED | forja_render_docx.py:222 |
| forja_render_docx.py::render | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_render_docx.py:223 |
| forja_render_docx.py::render | calls | forja_metadata.py::sanitize_final_artifacts | EXTRACTED | forja_render_docx.py:230 |
| forja_render_docx.py::render | calls | forja_visual_review.py::build_pending_review | EXTRACTED | forja_render_docx.py:246 |
| forja_render_docx.py::render | calls | forja_render_docx.py::_tipo_produto | EXTRACTED | forja_render_docx.py:99 |
| forja_render_docx.py::render | calls | forja_metricas_f7.py::metricas_f7 | EXTRACTED | forja_render_docx.py:118 |
| forja_render_docx.py::render | calls | forja_metadata.py::retry_transient_io | EXTRACTED | forja_render_docx.py:283 |
| forja_render_docx.py::render | calls | forja_lastro.py::material_economico | EXTRACTED | forja_render_docx.py:108 |
| forja_render_docx.py::render | calls | forja_render_docx.py::add_runs_com_negrito | EXTRACTED | forja_render_docx.py:190 |
| forja_render_docx.py::render | calls | forja_render_docx.py::eh_assinatura | EXTRACTED | forja_render_docx.py:195 |
| forja_render_docx.py::render | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_render_docx.py:241 |
| forja_render_docx.py::render | calls | forja_render_docx.py::add_runs_com_negrito | EXTRACTED | forja_render_docx.py:155 |
| forja_render_docx.py::render | calls | forja_render_docx.py::add_runs_com_negrito | EXTRACTED | forja_render_docx.py:196 |
| forja_render_docx.py::render | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_render_docx.py:236 |
| forja_render_docx.py::render | calls | forja_render_docx.py::add_runs_com_negrito | EXTRACTED | forja_render_docx.py:158 |
| forja_render_docx.py::render | calls | forja_render_docx.py::add_runs_com_negrito | EXTRACTED | forja_render_docx.py:201 |
| forja_render_docx.py::render | calls | forja_render_docx.py::add_runs_com_negrito | EXTRACTED | forja_render_docx.py:206 |
| forja_replay.py::validar_replay | calls | forja_replay.py::_fontes | EXTRACTED | forja_replay.py:95 |
| forja_replay.py::validar_replay | calls | forja_replay.py::_replays | EXTRACTED | forja_replay.py:134 |
| forja_replay.py::validar_replay | calls | forja_replay.py::_data | EXTRACTED | forja_replay.py:164 |
| forja_run.py | imports_from | forja_n3_common.py | EXTRACTED | forja_run.py:18 |
| forja_run.py | imports_from | forja_n3_common.py | EXTRACTED | forja_run.py:18 |
| forja_run.py | imports_from | forja_n3_common.py | EXTRACTED | forja_run.py:18 |
| forja_run.py | imports_from | forja_n3_common.py | EXTRACTED | forja_run.py:18 |
| forja_run.py | imports_from | forja_n3_common.py | EXTRACTED | forja_run.py:18 |
| forja_run.py | imports_from | forja_n3_common.py | EXTRACTED | forja_run.py:18 |
| forja_run.py | imports_from | forja_n3_common.py | EXTRACTED | forja_run.py:18 |
| forja_run.py | imports_from | forja_n3_common.py | EXTRACTED | forja_run.py:18 |
| forja_run.py | imports_from | forja_n3_common.py | EXTRACTED | forja_run.py:18 |
| forja_run.py | imports_from | forja_n3_common.py | EXTRACTED | forja_run.py:18 |
| forja_run.py | imports_from | forja_n3_common.py | EXTRACTED | forja_run.py:18 |
| forja_run.py | imports_from | forja_n3_common.py | EXTRACTED | forja_run.py:18 |
| forja_run.py | imports_from | forja_n3_common.py | EXTRACTED | forja_run.py:18 |
| forja_run.py | imports_from | forja_phase_contracts.py | EXTRACTED | forja_run.py:33 |
| forja_run.py | imports_from | forja_state_machine.py | EXTRACTED | forja_run.py:34 |
| forja_run.py | imports_from | forja_state_machine.py | EXTRACTED | forja_run.py:34 |
| forja_run.py | imports_from | forja_state_machine.py | EXTRACTED | forja_run.py:34 |
| forja_run.py | imports_from | forja_adversarial_audit.py | EXTRACTED | forja_run.py:35 |
| forja_run.py | imports_from | forja_n4_common.py | EXTRACTED | forja_run.py:36 |
| forja_run.py | imports_from | forja_exploracao_100.py | EXTRACTED | forja_run.py:37 |
| forja_run.py | imports_from | forja_editorial_fidelity.py | EXTRACTED | forja_run.py:38 |
| forja_run.py | imports_from | forja_lastro.py | EXTRACTED | forja_run.py:337 |
| forja_run.py | imports_from | forja_lastro.py | EXTRACTED | forja_run.py:337 |
| forja_run.py | imports_from | forja_lastro.py | EXTRACTED | forja_run.py:337 |
| forja_run.py | imports_from | forja_lastro.py | EXTRACTED | forja_run.py:337 |
| forja_run.py | imports_from | forja_injection_scan.py | EXTRACTED | forja_run.py:385 |
| forja_run.py | imports_from | forja_citations.py | EXTRACTED | forja_run.py:411 |
| forja_run.py | imports_from | forja_citations.py | EXTRACTED | forja_run.py:419 |
| forja_run.py | imports_from | forja_replay.py | EXTRACTED | forja_run.py:429 |
| forja_run.py | imports_from | forja_regimento_gate.py | EXTRACTED | forja_run.py:541 |
| forja_run.py | imports_from | forja_adversarial_gate.py | EXTRACTED | forja_run.py:550 |
| forja_run.py | imports_from | forja_contexto.py | EXTRACTED | forja_run.py:584 |
| forja_run.py | imports_from | forja_p0.py | EXTRACTED | forja_run.py:603 |
| forja_run.py | imports_from | forja_red_team.py | EXTRACTED | forja_run.py:634 |
| forja_run.py | imports_from | forja_conselho.py | EXTRACTED | forja_run.py:667 |
| forja_run.py | imports_from | forja_adversarial_gate.py | EXTRACTED | forja_run.py:678 |
| forja_run.py | imports_from | forja_ingestao.py | EXTRACTED | forja_run.py:717 |
| forja_run.py | imports_from | forja_exploracao_100.py | EXTRACTED | forja_run.py:749 |
| forja_run.py | imports_from | forja_fontes_oficiais.py | EXTRACTED | forja_run.py:789 |
| forja_run.py | imports_from | forja_paragrafos.py | EXTRACTED | forja_run.py:828 |
| forja_run.py | imports_from | forja_redacao.py | EXTRACTED | forja_run.py:846 |
| forja_run.py | imports_from | forja_authorities.py | EXTRACTED | forja_run.py:977 |
| forja_run.py | imports_from | forja_package.py | EXTRACTED | forja_run.py:978 |
| forja_run.py | imports_from | forja_estilo_humano.py | EXTRACTED | forja_run.py:1053 |
| forja_run.py | imports_from | forja_n4_validate.py | EXTRACTED | forja_run.py:1146 |
| forja_run.py | imports_from | forja_produto.py | EXTRACTED | forja_run.py:458 |
| forja_run.py | imports_from | forja_produto.py | EXTRACTED | forja_run.py:464 |
| forja_run.py | imports_from | forja_produto.py | EXTRACTED | forja_run.py:475 |
| forja_run.py | imports_from | forja_entrega.py | EXTRACTED | forja_run.py:480 |
| forja_run.py | imports_from | forja_entrega.py | EXTRACTED | forja_run.py:496 |
| forja_run.py | imports_from | forja_adversarial_gate.py | EXTRACTED | forja_run.py:505 |
| forja_run.py::_read_gate_artifact | calls | forja_n3_common.py::read_json | EXTRACTED | forja_run.py:58 |
| forja_run.py::_resolve_input | calls | forja_run.py::_artifact_path | EXTRACTED | forja_run.py:84 |
| forja_run.py::_resolve_input | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_run.py:73 |
| forja_run.py::_resolve_input | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_run.py:76 |
| forja_run.py::_resolve_input | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_run.py:82 |
| forja_run.py::prepare_attempt | calls | forja_phase_contracts.py::load_contract | EXTRACTED | forja_run.py:98 |
| forja_run.py::prepare_attempt | calls | forja_state_machine.py::derive_state | EXTRACTED | forja_run.py:99 |
| forja_run.py::prepare_attempt | calls | forja_state_machine.py::load_events | EXTRACTED | forja_run.py:111 |
| forja_run.py::prepare_attempt | calls | forja_n3_common.py::new_id | EXTRACTED | forja_run.py:125 |
| forja_run.py::prepare_attempt | calls | forja_state_machine.py::record_event | EXTRACTED | forja_run.py:126 |
| forja_run.py::prepare_attempt | calls | forja_n3_common.py::canonical_hash | EXTRACTED | forja_run.py:168 |
| forja_run.py::prepare_attempt | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_run.py:169 |
| forja_run.py::prepare_attempt | calls | forja_run.py::_resolve_input | EXTRACTED | forja_run.py:103 |
| forja_run.py::prepare_attempt | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_run.py:109 |
| forja_run.py::prepare_attempt | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_run.py:122 |
| forja_run.py::prepare_attempt | calls | forja_n3_common.py::new_id | EXTRACTED | forja_run.py:124 |
| forja_run.py::prepare_attempt | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_run.py:151 |
| forja_run.py::_lastro_context_base | calls | forja_run.py::_raiz_do_caso | EXTRACTED | forja_run.py:202 |
| forja_run.py::_achar_fact_ledger | calls | forja_run.py::_raiz_do_caso | EXTRACTED | forja_run.py:228 |
| forja_run.py::_compute_lastro_gates | calls | forja_run.py::_achar_fact_ledger | EXTRACTED | forja_run.py:277 |
| forja_run.py::_compute_lastro_gates | calls | forja_run.py::_lastro_context_base | EXTRACTED | forja_run.py:336 |
| forja_run.py::_compute_lastro_gates | calls | forja_lastro.py::validar_lastro_fatos | EXTRACTED | forja_run.py:343 |
| forja_run.py::_compute_lastro_gates | calls | forja_lastro.py::material_economico | EXTRACTED | forja_run.py:351 |
| forja_run.py::_compute_lastro_gates | calls | forja_run.py::_severidade_economica | EXTRACTED | forja_run.py:367 |
| forja_run.py::_compute_lastro_gates | calls | forja_lastro.py::exigir_criterio_vigente | EXTRACTED | forja_run.py:350 |
| forja_run.py::_compute_lastro_gates | calls | forja_lastro.py::validar_gates_economicos | EXTRACTED | forja_run.py:353 |
| forja_run.py::_recompute_injecao | calls | forja_injection_scan.py::validar_triagem_injecao | EXTRACTED | forja_run.py:389 |
| forja_run.py::_recompute_injecao | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_run.py:390 |
| forja_run.py::_recompute_injecao | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_run.py:396 |
| forja_run.py::_recompute_injecao | calls | forja_n3_common.py::read_json | EXTRACTED | forja_run.py:388 |
| forja_run.py::_recompute_injecao | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_run.py:394 |
| forja_run.py::_recompute_politica_citacoes | calls | forja_citations.py::validar_politica_citacoes | EXTRACTED | forja_run.py:422 |
| forja_run.py::_recompute_politica_citacoes | calls | forja_citations.py::validar_identidade_citacoes | EXTRACTED | forja_run.py:423 |
| forja_run.py::_recompute_politica_citacoes | calls | forja_replay.py::validar_replay | EXTRACTED | forja_run.py:431 |
| forja_run.py::_recompute_politica_citacoes | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_run.py:434 |
| forja_run.py::_recompute_politica_citacoes | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_run.py:442 |
| forja_run.py::_recompute_politica_citacoes | calls | forja_n3_common.py::read_json | EXTRACTED | forja_run.py:418 |
| forja_run.py::_recompute_politica_citacoes | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_run.py:439 |
| forja_run.py::_recompute_definicao | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_run.py:517 |
| forja_run.py::_recompute_definicao | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_run.py:525 |
| forja_run.py::_recompute_definicao | calls | forja_produto.py::validar_definicao_produto | EXTRACTED | forja_run.py:459 |
| forja_run.py::_recompute_definicao | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_run.py:522 |
| forja_run.py::_recompute_definicao | calls | forja_produto.py::validar_pergunta_jurisdicional | EXTRACTED | forja_run.py:472 |
| forja_run.py::_recompute_definicao | calls | forja_n3_common.py::read_json | EXTRACTED | forja_run.py:460 |
| forja_run.py::_recompute_definicao | calls | forja_produto.py::validar_uso_final | EXTRACTED | forja_run.py:476 |
| forja_run.py::_recompute_definicao | calls | forja_run.py::_read_gate_artifact | EXTRACTED | forja_run.py:490 |
| forja_run.py::_recompute_definicao | calls | forja_entrega.py::validar_reconciliacao | EXTRACTED | forja_run.py:491 |
| forja_run.py::_recompute_definicao | calls | forja_n3_common.py::read_json | EXTRACTED | forja_run.py:471 |
| forja_run.py::_recompute_definicao | calls | forja_n3_common.py::read_json | EXTRACTED | forja_run.py:476 |
| forja_run.py::_recompute_definicao | calls | forja_n3_common.py::read_json | EXTRACTED | forja_run.py:481 |
| forja_run.py::_recompute_definicao | calls | forja_entrega.py::validar_pacote | EXTRACTED | forja_run.py:504 |
| forja_run.py::_recompute_definicao | calls | forja_adversarial_gate.py::validar_politica_liberacao | EXTRACTED | forja_run.py:507 |
| forja_run.py::_recompute_definicao | calls | forja_n3_common.py::read_json | EXTRACTED | forja_run.py:502 |
| forja_run.py::_recompute_definicao | calls | forja_n3_common.py::read_json | EXTRACTED | forja_run.py:501 |
| forja_run.py::_recompute_definicao | calls | forja_n3_common.py::read_json | EXTRACTED | forja_run.py:509 |
| forja_run.py::_recompute_regimento | calls | forja_run.py::_read_gate_artifact | EXTRACTED | forja_run.py:544 |
| forja_run.py::_recompute_regimento | calls | forja_run.py::_read_gate_artifact | EXTRACTED | forja_run.py:545 |
| forja_run.py::_recompute_regimento | calls | forja_regimento_gate.py::validar_regimento | EXTRACTED | forja_run.py:547 |
| forja_run.py::_recompute_regimento | calls | forja_adversarial_gate.py::validar_auditoria_adversarial | EXTRACTED | forja_run.py:553 |
| forja_run.py::_recompute_regimento | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_run.py:559 |
| forja_run.py::_recompute_regimento | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_run.py:567 |
| forja_run.py::_recompute_regimento | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_run.py:564 |
| forja_run.py::_recompute_regimento | calls | forja_n3_common.py::read_json | EXTRACTED | forja_run.py:554 |
| forja_run.py::_recompute_contexto | calls | forja_contexto.py::validar_contexto | EXTRACTED | forja_run.py:599 |
| forja_run.py::_recompute_contexto | calls | forja_p0.py::validar_p0 | EXTRACTED | forja_run.py:605 |
| forja_run.py::_recompute_contexto | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_run.py:611 |
| forja_run.py::_recompute_contexto | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_run.py:619 |
| forja_run.py::_recompute_contexto | calls | forja_n3_common.py::read_json | EXTRACTED | forja_run.py:587 |
| forja_run.py::_recompute_contexto | calls | forja_n3_common.py::read_json | EXTRACTED | forja_run.py:589 |
| forja_run.py::_recompute_contexto | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_run.py:616 |
| forja_run.py::_recompute_red_team | calls | forja_red_team.py::validar_exame_adversarial | EXTRACTED | forja_run.py:644 |
| forja_run.py::_recompute_red_team | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_run.py:645 |
| forja_run.py::_recompute_red_team | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_run.py:653 |
| forja_run.py::_recompute_red_team | calls | forja_n3_common.py::read_json | EXTRACTED | forja_run.py:642 |
| forja_run.py::_recompute_red_team | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_run.py:650 |
| forja_run.py::_recompute_conselho | calls | forja_conselho.py::validar_conselho | EXTRACTED | forja_run.py:670 |
| forja_run.py::_recompute_conselho | calls | forja_run.py::_raiz_do_caso | EXTRACTED | forja_run.py:680 |
| forja_run.py::_recompute_conselho | calls | forja_adversarial_gate.py::validar_auditoria_adversarial | EXTRACTED | forja_run.py:685 |
| forja_run.py::_recompute_conselho | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_run.py:693 |
| forja_run.py::_recompute_conselho | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_run.py:702 |
| forja_run.py::_recompute_conselho | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_run.py:698 |
| forja_run.py::_recompute_conselho | calls | forja_n3_common.py::read_json | EXTRACTED | forja_run.py:686 |
| forja_run.py::_recompute_conselho | calls | forja_n3_common.py::read_json | EXTRACTED | forja_run.py:687 |
| forja_run.py::_recompute_ingestao | calls | forja_ingestao.py::validar_ingestao | EXTRACTED | forja_run.py:725 |
| forja_run.py::_recompute_ingestao | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_run.py:727 |
| forja_run.py::_recompute_ingestao | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_run.py:735 |
| forja_run.py::_recompute_ingestao | calls | forja_n3_common.py::read_json | EXTRACTED | forja_run.py:721 |
| forja_run.py::_recompute_ingestao | calls | forja_n3_common.py::read_json | EXTRACTED | forja_run.py:723 |
| forja_run.py::_recompute_ingestao | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_run.py:732 |
| forja_run.py::_recompute_exploracao | calls | forja_exploracao_100.py::gates_da_exploracao | EXTRACTED | forja_run.py:757 |
| forja_run.py::_recompute_exploracao | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_run.py:758 |
| forja_run.py::_recompute_exploracao | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_run.py:769 |
| forja_run.py::_recompute_exploracao | calls | forja_n3_common.py::read_json | EXTRACTED | forja_run.py:755 |
| forja_run.py::_recompute_exploracao | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_run.py:766 |
| forja_run.py::_recompute_pesquisa_oficial | calls | forja_run.py::_read_gate_artifact | EXTRACTED | forja_run.py:799 |
| forja_run.py::_recompute_pesquisa_oficial | calls | forja_fontes_oficiais.py::validar_pesquisa_oficial | EXTRACTED | forja_run.py:801 |
| forja_run.py::_recompute_pesquisa_oficial | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_run.py:803 |
| forja_run.py::_recompute_pesquisa_oficial | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_run.py:811 |
| forja_run.py::_recompute_pesquisa_oficial | calls | forja_n3_common.py::read_json | EXTRACTED | forja_run.py:793 |
| forja_run.py::_recompute_pesquisa_oficial | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_run.py:808 |
| forja_run.py::_recompute_paragrafos | calls | forja_paragrafos.py::validar_paragrafos_lastreados | EXTRACTED | forja_run.py:841 |
| forja_run.py::_recompute_paragrafos | calls | forja_redacao.py::validar_redacao | EXTRACTED | forja_run.py:848 |
| forja_run.py::_recompute_paragrafos | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_run.py:852 |
| forja_run.py::_recompute_paragrafos | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_run.py:860 |
| forja_run.py::_recompute_paragrafos | calls | forja_n3_common.py::read_json | EXTRACTED | forja_run.py:832 |
| forja_run.py::_recompute_paragrafos | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_run.py:857 |
| forja_run.py::_validate_result | calls | forja_n3_common.py::read_json | EXTRACTED | forja_run.py:865 |
| forja_run.py::_validate_result | calls | forja_run.py::_recompute_injecao | EXTRACTED | forja_run.py:917 |
| forja_run.py::_validate_result | calls | forja_run.py::_recompute_ingestao | EXTRACTED | forja_run.py:918 |
| forja_run.py::_validate_result | calls | forja_run.py::_recompute_exploracao | EXTRACTED | forja_run.py:919 |
| forja_run.py::_validate_result | calls | forja_run.py::_recompute_regimento | EXTRACTED | forja_run.py:920 |
| forja_run.py::_validate_result | calls | forja_run.py::_recompute_definicao | EXTRACTED | forja_run.py:921 |
| forja_run.py::_validate_result | calls | forja_run.py::_recompute_conselho | EXTRACTED | forja_run.py:922 |
| forja_run.py::_validate_result | calls | forja_run.py::_recompute_pesquisa_oficial | EXTRACTED | forja_run.py:923 |
| forja_run.py::_validate_result | calls | forja_run.py::_recompute_paragrafos | EXTRACTED | forja_run.py:924 |
| forja_run.py::_validate_result | calls | forja_run.py::_recompute_contexto | EXTRACTED | forja_run.py:925 |
| forja_run.py::_validate_result | calls | forja_run.py::_recompute_red_team | EXTRACTED | forja_run.py:926 |
| forja_run.py::_validate_result | calls | forja_run.py::_recompute_politica_citacoes | EXTRACTED | forja_run.py:927 |
| forja_run.py::_validate_result | calls | forja_run.py::_compute_lastro_gates | EXTRACTED | forja_run.py:928 |
| forja_run.py::_validate_result | calls | forja_adversarial_audit.py::validate_phase_artifacts | EXTRACTED | forja_run.py:960 |
| forja_run.py::_validate_result | calls | forja_run.py::_validate_fable5_editorial | EXTRACTED | forja_run.py:967 |
| forja_run.py::_validate_result | calls | forja_run.py::_validate_f7_source_ledger | EXTRACTED | forja_run.py:968 |
| forja_run.py::_validate_result | calls | forja_run.py::_validate_human_style | EXTRACTED | forja_run.py:969 |
| forja_run.py::_validate_result | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_run.py:867 |
| forja_run.py::_validate_result | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_run.py:869 |
| forja_run.py::_validate_result | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_run.py:871 |
| forja_run.py::_validate_result | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_run.py:873 |
| forja_run.py::_validate_result | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_run.py:880 |
| forja_run.py::_validate_result | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_run.py:884 |
| forja_run.py::_validate_result | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_run.py:887 |
| forja_run.py::_validate_result | calls | forja_n3_common.py::ensure_within | EXTRACTED | forja_run.py:893 |
| forja_run.py::_validate_result | calls | forja_n3_common.py::read_json | EXTRACTED | forja_run.py:916 |
| forja_run.py::_validate_result | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_run.py:930 |
| forja_run.py::_validate_result | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_run.py:958 |
| forja_run.py::_validate_result | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_run.py:966 |
| forja_run.py::_validate_result | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_run.py:892 |
| forja_run.py::_validate_result | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_run.py:895 |
| forja_run.py::_validate_result | calls | forja_n3_common.py::read_json | EXTRACTED | forja_run.py:897 |
| forja_run.py::_validate_result | calls | forja_exploracao_100.py::validate_exploration_100 | EXTRACTED | forja_run.py:900 |
| forja_run.py::_validate_result | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_run.py:941 |
| forja_run.py::_validate_result | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_run.py:947 |
| forja_run.py::_validate_result | calls | forja_n3_common.py::resolve_name | EXTRACTED | forja_run.py:885 |
| forja_run.py::_validate_result | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_run.py:899 |
| forja_run.py::_validate_result | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_run.py:906 |
| forja_run.py::_validate_result | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_run.py:913 |
| forja_run.py::_validate_result | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_run.py:939 |
| forja_run.py::_validate_result | calls | forja_n3_common.py::name_with_legacy | EXTRACTED | forja_run.py:877 |
| forja_run.py::_validate_result | calls | forja_n3_common.py::name_with_legacy | EXTRACTED | forja_run.py:955 |
| forja_run.py::_validate_f7_source_ledger | calls | forja_package.py::validate_source_ledger | EXTRACTED | forja_run.py:993 |
| forja_run.py::_validate_f7_source_ledger | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_run.py:989 |
| forja_run.py::_validate_f7_source_ledger | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_run.py:1000 |
| forja_run.py::_validate_f7_source_ledger | calls | forja_authorities.py::extract_authorities | EXTRACTED | forja_run.py:996 |
| forja_run.py::_validate_fable5_editorial | calls | forja_editorial_fidelity.py::validate_editorial_bundle | EXTRACTED | forja_run.py:1027 |
| forja_run.py::_validate_fable5_editorial | calls | forja_n3_common.py::resolve_name | EXTRACTED | forja_run.py:1018 |
| forja_run.py::_validate_fable5_editorial | calls | forja_n3_common.py::resolve_name | EXTRACTED | forja_run.py:1019 |
| forja_run.py::_validate_fable5_editorial | calls | forja_n3_common.py::resolve_name | EXTRACTED | forja_run.py:1020 |
| forja_run.py::_validate_fable5_editorial | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_run.py:1024 |
| forja_run.py::_validate_fable5_editorial | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_run.py:1038 |
| forja_run.py::_validate_fable5_editorial | calls | forja_n3_common.py::resolve_name | EXTRACTED | forja_run.py:1012 |
| forja_run.py::_validate_human_style | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_run.py:1063 |
| forja_run.py::_validate_human_style | calls | forja_estilo_humano.py::analisar | EXTRACTED | forja_run.py:1055 |
| forja_run.py::_promote_file | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_run.py:1078 |
| forja_run.py::_promote_file | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_run.py:1080 |
| forja_run.py::_promote_file | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_run.py:1095 |
| forja_run.py::_promote_file | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_run.py:1096 |
| forja_run.py::promote_attempt | calls | forja_n3_common.py::ensure_within | EXTRACTED | forja_run.py:1104 |
| forja_run.py::promote_attempt | calls | forja_n3_common.py::read_json | EXTRACTED | forja_run.py:1105 |
| forja_run.py::promote_attempt | calls | forja_phase_contracts.py::load_contract | EXTRACTED | forja_run.py:1108 |
| forja_run.py::promote_attempt | calls | forja_run.py::_validate_result | EXTRACTED | forja_run.py:1111 |
| forja_run.py::promote_attempt | calls | forja_state_machine.py::derive_state | EXTRACTED | forja_run.py:1112 |
| forja_run.py::promote_attempt | calls | forja_n4_validate.py::validate_case | EXTRACTED | forja_run.py:1148 |
| forja_run.py::promote_attempt | calls | forja_state_machine.py::record_event | EXTRACTED | forja_run.py:1163 |
| forja_run.py::promote_attempt | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_run.py:1107 |
| forja_run.py::promote_attempt | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_run.py:1110 |
| forja_run.py::promote_attempt | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_run.py:1114 |
| forja_run.py::promote_attempt | calls | forja_run.py::_promote_file | EXTRACTED | forja_run.py:1118 |
| forja_run.py::promote_attempt | calls | forja_state_machine.py::record_event | EXTRACTED | forja_run.py:1132 |
| forja_run.py::promote_attempt | calls | forja_state_machine.py::record_event | EXTRACTED | forja_run.py:1151 |
| forja_run.py::promote_attempt | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_run.py:1162 |
| forja_run.py::block_phase | calls | forja_state_machine.py::record_event | EXTRACTED | forja_run.py:1179 |
| forja_run.py::block_phase | calls | forja_n3_common.py::canonical_hash | EXTRACTED | forja_run.py:1183 |
| forja_run.py::main | calls | forja_n3_common.py::resolve_case_dir | EXTRACTED | forja_run.py:1207 |
| forja_run.py::main | calls | forja_run.py::prepare_attempt | EXTRACTED | forja_run.py:1209 |
| forja_run.py::main | calls | forja_run.py::promote_attempt | EXTRACTED | forja_run.py:1211 |
| forja_run.py::main | calls | forja_run.py::block_phase | EXTRACTED | forja_run.py:1213 |
| forja_run_metrics.py | imports_from | forja_n3_common.py | EXTRACTED | forja_run_metrics.py:10 |
| forja_run_metrics.py | imports_from | forja_n3_common.py | EXTRACTED | forja_run_metrics.py:10 |
| forja_run_metrics.py | imports_from | forja_n3_common.py | EXTRACTED | forja_run_metrics.py:10 |
| forja_run_metrics.py | imports_from | forja_n3_common.py | EXTRACTED | forja_run_metrics.py:10 |
| forja_run_metrics.py | imports_from | forja_n3_common.py | EXTRACTED | forja_run_metrics.py:10 |
| forja_run_metrics.py | imports_from | forja_state_machine.py | EXTRACTED | forja_run_metrics.py:11 |
| forja_run_metrics.py | imports_from | forja_state_machine.py | EXTRACTED | forja_run_metrics.py:11 |
| forja_run_metrics.py::_safe_ledger | calls | forja_n3_common.py::read_json | EXTRACTED | forja_run_metrics.py:18 |
| forja_run_metrics.py::build_metrics | calls | forja_state_machine.py::load_events | EXTRACTED | forja_run_metrics.py:23 |
| forja_run_metrics.py::build_metrics | calls | forja_state_machine.py::derive_state | EXTRACTED | forja_run_metrics.py:24 |
| forja_run_metrics.py::build_metrics | calls | forja_run_metrics.py::_safe_ledger | EXTRACTED | forja_run_metrics.py:37 |
| forja_run_metrics.py::build_metrics | calls | forja_run_metrics.py::_safe_ledger | EXTRACTED | forja_run_metrics.py:38 |
| forja_run_metrics.py::build_metrics | calls | forja_run_metrics.py::_safe_ledger | EXTRACTED | forja_run_metrics.py:42 |
| forja_run_metrics.py::build_metrics | calls | forja_run_metrics.py::_safe_ledger | EXTRACTED | forja_run_metrics.py:43 |
| forja_run_metrics.py::build_metrics | calls | forja_run_metrics.py::_safe_ledger | EXTRACTED | forja_run_metrics.py:44 |
| forja_run_metrics.py::build_metrics | calls | forja_run_metrics.py::_safe_ledger | EXTRACTED | forja_run_metrics.py:45 |
| forja_run_metrics.py::build_metrics | calls | forja_run_metrics.py::_safe_ledger | EXTRACTED | forja_run_metrics.py:46 |
| forja_run_metrics.py::build_metrics | calls | forja_run_metrics.py::_safe_ledger | EXTRACTED | forja_run_metrics.py:47 |
| forja_run_metrics.py::build_metrics | calls | forja_run_metrics.py::_safe_ledger | EXTRACTED | forja_run_metrics.py:48 |
| forja_run_metrics.py::build_metrics | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_run_metrics.py:58 |
| forja_run_metrics.py::write_metrics | calls | forja_run_metrics.py::build_metrics | EXTRACTED | forja_run_metrics.py:122 |
| forja_run_metrics.py::write_metrics | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_run_metrics.py:124 |
| forja_run_metrics.py::main | calls | forja_n3_common.py::resolve_case_dir | EXTRACTED | forja_run_metrics.py:133 |
| forja_run_metrics.py::main | calls | forja_run_metrics.py::write_metrics | EXTRACTED | forja_run_metrics.py:134 |
| forja_science.py | imports_from | forja_n3_common.py | EXTRACTED | forja_science.py:13 |
| forja_science.py | imports_from | forja_n4_common.py | EXTRACTED | forja_science.py:14 |
| forja_science.py | imports_from | forja_n4_common.py | EXTRACTED | forja_science.py:14 |
| forja_science.py | imports_from | forja_n4_common.py | EXTRACTED | forja_science.py:14 |
| forja_science.py::crossref_search | calls | forja_science.py::_get_json | EXTRACTED | forja_science.py:30 |
| forja_science.py::crossref_by_doi | calls | forja_science.py::normalize_doi | EXTRACTED | forja_science.py:37 |
| forja_science.py::pubmed_search | calls | forja_science.py::_get_json | EXTRACTED | forja_science.py:51 |
| forja_science.py::pubmed_search | calls | forja_science.py::_get_json | EXTRACTED | forja_science.py:55 |
| forja_science.py::openalex_search | calls | forja_science.py::_get_json | EXTRACTED | forja_science.py:81 |
| forja_science.py::discover | calls | forja_science.py::crossref_search | EXTRACTED | forja_science.py:89 |
| forja_science.py::discover | calls | forja_science.py::pubmed_search | EXTRACTED | forja_science.py:89 |
| forja_science.py::discover | calls | forja_science.py::openalex_search | EXTRACTED | forja_science.py:89 |
| forja_science.py::validate_classification | calls | forja_n4_common.py::issue | EXTRACTED | forja_science.py:107 |
| forja_science.py::validate_classification | calls | forja_n4_common.py::issue | EXTRACTED | forja_science.py:110 |
| forja_science.py::validate_classification | calls | forja_n4_common.py::issue | EXTRACTED | forja_science.py:112 |
| forja_science.py::validate_protocol | calls | forja_n4_common.py::issue | EXTRACTED | forja_science.py:123 |
| forja_science.py::validate_protocol | calls | forja_n4_common.py::issue | EXTRACTED | forja_science.py:120 |
| forja_science.py::validate_studies | calls | forja_n4_common.py::ids_unique | EXTRACTED | forja_science.py:129 |
| forja_science.py::validate_studies | calls | forja_science.py::normalize_doi | EXTRACTED | forja_science.py:134 |
| forja_science.py::validate_studies | calls | forja_science.py::_bibliographic_text | EXTRACTED | forja_science.py:144 |
| forja_science.py::validate_studies | calls | forja_science.py::_bibliographic_text | EXTRACTED | forja_science.py:145 |
| forja_science.py::validate_studies | calls | forja_science.py::_bibliographic_text | EXTRACTED | forja_science.py:148 |
| forja_science.py::validate_studies | calls | forja_science.py::_bibliographic_text | EXTRACTED | forja_science.py:149 |
| forja_science.py::validate_studies | calls | forja_n4_common.py::issue | EXTRACTED | forja_science.py:157 |
| forja_science.py::validate_studies | calls | forja_n4_common.py::issue | EXTRACTED | forja_science.py:159 |
| forja_science.py::validate_studies | calls | forja_n4_common.py::issue | EXTRACTED | forja_science.py:161 |
| forja_science.py::validate_studies | calls | forja_n4_common.py::issue | EXTRACTED | forja_science.py:163 |
| forja_science.py::validate_studies | calls | forja_n4_common.py::issue | EXTRACTED | forja_science.py:165 |
| forja_science.py::validate_studies | calls | forja_n4_common.py::issue | EXTRACTED | forja_science.py:167 |
| forja_science.py::validate_studies | calls | forja_n4_common.py::issue | EXTRACTED | forja_science.py:147 |
| forja_science.py::validate_studies | calls | forja_n4_common.py::issue | EXTRACTED | forja_science.py:155 |
| forja_science.py::validate_studies | calls | forja_n4_common.py::issue | EXTRACTED | forja_science.py:139 |
| forja_science.py::validate_claims | calls | forja_n4_common.py::ids_unique | EXTRACTED | forja_science.py:173 |
| forja_science.py::validate_claims | calls | forja_n4_common.py::issue | EXTRACTED | forja_science.py:178 |
| forja_science.py::validate_claims | calls | forja_n4_common.py::issue | EXTRACTED | forja_science.py:187 |
| forja_science.py::validate_claims | calls | forja_n4_common.py::issue | EXTRACTED | forja_science.py:190 |
| forja_science.py::validate_claims | calls | forja_n4_common.py::issue | EXTRACTED | forja_science.py:192 |
| forja_science.py::validate_claims | calls | forja_n4_common.py::issue | EXTRACTED | forja_science.py:194 |
| forja_science.py::validate_claims | calls | forja_n4_common.py::issue | EXTRACTED | forja_science.py:183 |
| forja_science.py::validate_synthesis | calls | forja_n4_common.py::issue | EXTRACTED | forja_science.py:201 |
| forja_science.py::validate_synthesis | calls | forja_n4_common.py::issue | EXTRACTED | forja_science.py:204 |
| forja_science.py::validate_synthesis | calls | forja_n4_common.py::issue | EXTRACTED | forja_science.py:206 |
| forja_science.py::validate_audit | calls | forja_n4_common.py::issue | EXTRACTED | forja_science.py:218 |
| forja_science.py::validate_audit | calls | forja_n4_common.py::issue | EXTRACTED | forja_science.py:212 |
| forja_science.py::validate_audit | calls | forja_n4_common.py::issue | EXTRACTED | forja_science.py:216 |
| forja_science.py::validate_case | calls | forja_n4_common.py::validate_file | EXTRACTED | forja_science.py:224 |
| forja_science.py::validate_case | calls | forja_n4_common.py::validate_file | EXTRACTED | forja_science.py:231 |
| forja_science.py::validate_case | calls | forja_n4_common.py::validate_file | EXTRACTED | forja_science.py:233 |
| forja_science.py::validate_case | calls | forja_n4_common.py::validate_file | EXTRACTED | forja_science.py:235 |
| forja_science.py::validate_case | calls | forja_n4_common.py::validate_file | EXTRACTED | forja_science.py:237 |
| forja_science.py::validate_case | calls | forja_n4_common.py::validate_file | EXTRACTED | forja_science.py:239 |
| forja_science.py::validate_case | calls | forja_n4_common.py::validate_file | EXTRACTED | forja_science.py:228 |
| forja_science.py::validate_case | calls | forja_science.py::validate_claims | EXTRACTED | forja_science.py:237 |
| forja_science.py::main | calls | forja_science.py::validate_case | EXTRACTED | forja_science.py:253 |
| forja_science.py::main | calls | forja_science.py::discover | EXTRACTED | forja_science.py:253 |
| forja_science.py::main | calls | forja_n3_common.py::resolve_case_dir | EXTRACTED | forja_science.py:253 |
| forja_sources.py | imports_from | forja_n3_common.py | EXTRACTED | forja_sources.py:20 |
| forja_sources.py | imports_from | forja_n3_common.py | EXTRACTED | forja_sources.py:20 |
| forja_sources.py::processar_caso | calls | forja_n3_common.py::read_json | EXTRACTED | forja_sources.py:127 |
| forja_sources.py::processar_caso | calls | forja_sources.py::classificar_produto | EXTRACTED | forja_sources.py:141 |
| forja_sources.py::processar_caso | calls | forja_sources.py::detectar_tribunal | EXTRACTED | forja_sources.py:142 |
| forja_sources.py::processar_caso | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_sources.py:234 |
| forja_sources.py::processar_caso | calls | forja_sources.py::merge_gates | EXTRACTED | forja_sources.py:237 |
| forja_sources.py::processar_caso | calls | forja_sources.py::merge_by_id | EXTRACTED | forja_sources.py:238 |
| forja_sources.py::processar_caso | calls | forja_sources.py::append_unique | EXTRACTED | forja_sources.py:239 |
| forja_sources.py::processar_caso | calls | forja_sources.py::localizar_regimento | EXTRACTED | forja_sources.py:175 |
| forja_sources.py::processar_caso | calls | forja_sources.py::validar_regimento | EXTRACTED | forja_sources.py:181 |
| forja_sources.py::processar_caso | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_sources.py:236 |
| forja_sources.py::processar_caso | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_sources.py:148 |
| forja_sources.py::processar_caso | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_sources.py:163 |
| forja_sources.py::processar_caso | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_sources.py:211 |
| forja_sources.py::processar_caso | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_sources.py:216 |
| forja_sources.py::processar_caso | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_sources.py:169 |
| forja_sources.py::processar_caso | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_sources.py:178 |
| forja_sources.py::processar_caso | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_sources.py:197 |
| forja_sources.py::processar_caso | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_sources.py:185 |
| forja_sources.py::processar_caso | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_sources.py:187 |
| forja_sources.py::main | calls | forja_sources.py::processar_caso | EXTRACTED | forja_sources.py:252 |
| forja_state_machine.py | imports_from | forja_n3_common.py | EXTRACTED | forja_state_machine.py:16 |
| forja_state_machine.py | imports_from | forja_n3_common.py | EXTRACTED | forja_state_machine.py:16 |
| forja_state_machine.py | imports_from | forja_n3_common.py | EXTRACTED | forja_state_machine.py:16 |
| forja_state_machine.py | imports_from | forja_n3_common.py | EXTRACTED | forja_state_machine.py:16 |
| forja_state_machine.py | imports_from | forja_n3_common.py | EXTRACTED | forja_state_machine.py:16 |
| forja_state_machine.py | imports_from | forja_n3_common.py | EXTRACTED | forja_state_machine.py:16 |
| forja_state_machine.py | imports_from | forja_n3_common.py | EXTRACTED | forja_state_machine.py:16 |
| forja_state_machine.py | imports_from | forja_n3_common.py | EXTRACTED | forja_state_machine.py:16 |
| forja_state_machine.py | imports_from | forja_n3_common.py | EXTRACTED | forja_state_machine.py:16 |
| forja_state_machine.py | imports_from | forja_n3_common.py | EXTRACTED | forja_state_machine.py:16 |
| forja_state_machine.py | imports_from | forja_n3_common.py | EXTRACTED | forja_state_machine.py:16 |
| forja_state_machine.py | imports_from | forja_n3_common.py | EXTRACTED | forja_state_machine.py:16 |
| forja_state_machine.py | imports_from | forja_management_bridge.py | EXTRACTED | forja_state_machine.py:426 |
| forja_state_machine.py::_phase_index | calls | forja_n3_common.py::TransitionError | EXTRACTED | forja_state_machine.py:89 |
| forja_state_machine.py::_highest_completed_index | calls | forja_state_machine.py::_phase_index | EXTRACTED | forja_state_machine.py:93 |
| forja_state_machine.py::_highest_completed_index | calls | forja_state_machine.py::_phase_index | EXTRACTED | forja_state_machine.py:96 |
| forja_state_machine.py::load_events | calls | forja_state_machine.py::event_paths | EXTRACTED | forja_state_machine.py:110 |
| forja_state_machine.py::load_events | calls | forja_n3_common.py::read_json | EXTRACTED | forja_state_machine.py:112 |
| forja_state_machine.py::load_events | calls | forja_n3_common.py::TransitionError | EXTRACTED | forja_state_machine.py:114 |
| forja_state_machine.py::load_events | calls | forja_n3_common.py::TransitionError | EXTRACTED | forja_state_machine.py:116 |
| forja_state_machine.py::load_events | calls | forja_n3_common.py::TransitionError | EXTRACTED | forja_state_machine.py:118 |
| forja_state_machine.py::derive_state | calls | forja_state_machine.py::_base_state | EXTRACTED | forja_state_machine.py:163 |
| forja_state_machine.py::derive_state | calls | forja_n3_common.py::canonical_hash | EXTRACTED | forja_state_machine.py:299 |
| forja_state_machine.py::derive_state | calls | forja_state_machine.py::load_events | EXTRACTED | forja_state_machine.py:164 |
| forja_state_machine.py::derive_state | calls | forja_state_machine.py::_phase_index | EXTRACTED | forja_state_machine.py:208 |
| forja_state_machine.py::_validate_transition | calls | forja_state_machine.py::derive_state | EXTRACTED | forja_state_machine.py:306 |
| forja_state_machine.py::_validate_transition | calls | forja_n3_common.py::TransitionError | EXTRACTED | forja_state_machine.py:305 |
| forja_state_machine.py::_validate_transition | calls | forja_state_machine.py::_phase_index | EXTRACTED | forja_state_machine.py:308 |
| forja_state_machine.py::_validate_transition | calls | forja_n3_common.py::TransitionError | EXTRACTED | forja_state_machine.py:313 |
| forja_state_machine.py::_validate_transition | calls | forja_n3_common.py::TransitionError | EXTRACTED | forja_state_machine.py:315 |
| forja_state_machine.py::_validate_transition | calls | forja_n3_common.py::TransitionError | EXTRACTED | forja_state_machine.py:317 |
| forja_state_machine.py::_validate_transition | calls | forja_state_machine.py::_highest_completed_index | EXTRACTED | forja_state_machine.py:321 |
| forja_state_machine.py::_validate_transition | calls | forja_state_machine.py::_phase_index | EXTRACTED | forja_state_machine.py:322 |
| forja_state_machine.py::_validate_transition | calls | forja_state_machine.py::_highest_completed_index | EXTRACTED | forja_state_machine.py:335 |
| forja_state_machine.py::_validate_transition | calls | forja_n3_common.py::TransitionError | EXTRACTED | forja_state_machine.py:343 |
| forja_state_machine.py::_validate_transition | calls | forja_n3_common.py::TransitionError | EXTRACTED | forja_state_machine.py:320 |
| forja_state_machine.py::_validate_transition | calls | forja_n3_common.py::TransitionError | EXTRACTED | forja_state_machine.py:326 |
| forja_state_machine.py::_validate_transition | calls | forja_n3_common.py::TransitionError | EXTRACTED | forja_state_machine.py:328 |
| forja_state_machine.py::_validate_transition | calls | forja_n3_common.py::TransitionError | EXTRACTED | forja_state_machine.py:331 |
| forja_state_machine.py::_validate_transition | calls | forja_n3_common.py::TransitionError | EXTRACTED | forja_state_machine.py:334 |
| forja_state_machine.py::_validate_transition | calls | forja_state_machine.py::_phase_index | EXTRACTED | forja_state_machine.py:336 |
| forja_state_machine.py::_validate_transition | calls | forja_n3_common.py::TransitionError | EXTRACTED | forja_state_machine.py:337 |
| forja_state_machine.py::_validate_transition | calls | forja_n3_common.py::TransitionError | EXTRACTED | forja_state_machine.py:341 |
| forja_state_machine.py::_validate_transition | calls | forja_n3_common.py::TransitionError | EXTRACTED | forja_state_machine.py:346 |
| forja_state_machine.py::_materialize_locked | calls | forja_state_machine.py::derive_state | EXTRACTED | forja_state_machine.py:350 |
| forja_state_machine.py::_materialize_locked | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_state_machine.py:351 |
| forja_state_machine.py::_materialize_locked | calls | forja_n3_common.py::atomic_write_text | EXTRACTED | forja_state_machine.py:353 |
| forja_state_machine.py::record_event | calls | forja_n3_common.py::load_config | EXTRACTED | forja_state_machine.py:372 |
| forja_state_machine.py::record_event | calls | forja_n3_common.py::InterProcessLock | EXTRACTED | forja_state_machine.py:374 |
| forja_state_machine.py::record_event | calls | forja_state_machine.py::load_events | EXTRACTED | forja_state_machine.py:380 |
| forja_state_machine.py::record_event | calls | forja_state_machine.py::_validate_transition | EXTRACTED | forja_state_machine.py:388 |
| forja_state_machine.py::record_event | calls | forja_n3_common.py::new_id | EXTRACTED | forja_state_machine.py:389 |
| forja_state_machine.py::record_event | calls | forja_state_machine.py::tempfile_event | EXTRACTED | forja_state_machine.py:412 |
| forja_state_machine.py::record_event | calls | forja_state_machine.py::_materialize_locked | EXTRACTED | forja_state_machine.py:423 |
| forja_state_machine.py::record_event | calls | forja_n3_common.py::RevisionConflict | EXTRACTED | forja_state_machine.py:386 |
| forja_state_machine.py::record_event | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_state_machine.py:406 |
| forja_state_machine.py::record_event | calls | forja_management_bridge.py::sync_after_event | EXTRACTED | forja_state_machine.py:428 |
| forja_state_machine.py::record_event | calls | forja_state_machine.py::derive_state | EXTRACTED | forja_state_machine.py:429 |
| forja_state_machine.py::record_event | calls | forja_state_machine.py::derive_state | EXTRACTED | forja_state_machine.py:383 |
| forja_state_machine.py::initialize_case | calls | forja_state_machine.py::record_event | EXTRACTED | forja_state_machine.py:464 |
| forja_state_machine.py::initialize_case | calls | forja_n3_common.py::read_json | EXTRACTED | forja_state_machine.py:443 |
| forja_state_machine.py::initialize_case | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_state_machine.py:475 |
| forja_state_machine.py::initialize_case | calls | forja_n3_common.py::canonical_hash | EXTRACTED | forja_state_machine.py:459 |
| forja_state_machine.py::main | calls | forja_n3_common.py::resolve_case_dir | EXTRACTED | forja_state_machine.py:508 |
| forja_state_machine.py::main | calls | forja_state_machine.py::initialize_case | EXTRACTED | forja_state_machine.py:510 |
| forja_state_machine.py::main | calls | forja_state_machine.py::derive_state | EXTRACTED | forja_state_machine.py:512 |
| forja_state_machine.py::main | calls | forja_state_machine.py::record_event | EXTRACTED | forja_state_machine.py:514 |
| forja_svg_docx.py::_svg_ratio | calls | forja_svg_docx.py::_number | EXTRACTED | forja_svg_docx.py:54 |
| forja_svg_docx.py::_svg_ratio | calls | forja_svg_docx.py::_number | EXTRACTED | forja_svg_docx.py:55 |
| forja_svg_docx.py::_paragraphs | calls | forja_svg_docx.py::_paragraphs | EXTRACTED | forja_svg_docx.py:68 |
| forja_svg_docx.py::_inline_svg | calls | forja_svg_docx.py::_svg_ratio | EXTRACTED | forja_svg_docx.py:89 |
| forja_svg_docx.py::_inline_svg | calls | forja_svg_docx.py::_new_svg_part | EXTRACTED | forja_svg_docx.py:92 |
| forja_svg_docx.py::inserir_svgs | calls | forja_svg_docx.py::_next_docpr_id | EXTRACTED | forja_svg_docx.py:210 |
| forja_svg_docx.py::inserir_svgs | calls | forja_svg_docx.py::_paragraphs | EXTRACTED | forja_svg_docx.py:203 |
| forja_svg_docx.py::inserir_svgs | calls | forja_svg_docx.py::_validate_svg | EXTRACTED | forja_svg_docx.py:217 |
| forja_svg_docx.py::inserir_svgs | calls | forja_svg_docx.py::_inline_svg | EXTRACTED | forja_svg_docx.py:226 |
| forja_svg_docx.py::inserir_svgs | calls | forja_svg_docx.py::_paragraphs | EXTRACTED | forja_svg_docx.py:246 |
| forja_varredura_tipografica.py | imports_from | forja_docx_layout.py | EXTRACTED | forja_varredura_tipografica.py:189 |
| forja_varredura_tipografica.py::_mesmo_caso | calls | forja_varredura_tipografica.py::_caso_de | EXTRACTED | forja_varredura_tipografica.py:128 |
| forja_varredura_tipografica.py::_mesmo_caso | calls | forja_varredura_tipografica.py::_caso_de | EXTRACTED | forja_varredura_tipografica.py:128 |
| forja_varredura_tipografica.py::_mesmo_caso | calls | forja_varredura_tipografica.py::_tokens_do_caminho | EXTRACTED | forja_varredura_tipografica.py:132 |
| forja_varredura_tipografica.py::_mesmo_caso | calls | forja_varredura_tipografica.py::_tokens_do_caminho | EXTRACTED | forja_varredura_tipografica.py:132 |
| forja_varredura_tipografica.py::_marcar_superadas | calls | forja_varredura_tipografica.py::_familia_de | EXTRACTED | forja_varredura_tipografica.py:163 |
| forja_varredura_tipografica.py::_marcar_superadas | calls | forja_varredura_tipografica.py::_familia_de | EXTRACTED | forja_varredura_tipografica.py:173 |
| forja_varredura_tipografica.py::_marcar_superadas | calls | forja_varredura_tipografica.py::_tem_marca_correcao | EXTRACTED | forja_varredura_tipografica.py:171 |
| forja_varredura_tipografica.py::_marcar_superadas | calls | forja_varredura_tipografica.py::_familia_de | EXTRACTED | forja_varredura_tipografica.py:174 |
| forja_varredura_tipografica.py::_marcar_superadas | calls | forja_varredura_tipografica.py::_mesmo_caso | EXTRACTED | forja_varredura_tipografica.py:176 |
| forja_varredura_tipografica.py::varrer | calls | forja_varredura_tipografica.py::_marcar_superadas | EXTRACTED | forja_varredura_tipografica.py:230 |
| forja_varredura_tipografica.py::varrer | calls | forja_varredura_tipografica.py::_e_entregavel | EXTRACTED | forja_varredura_tipografica.py:196 |
| forja_varredura_tipografica.py::varrer | calls | forja_docx_layout.py::audit_docx_layout | EXTRACTED | forja_varredura_tipografica.py:201 |
| forja_verificador.py | imports_from | forja_estilo_humano.py | EXTRACTED | forja_verificador.py:422 |
| forja_verificador.py | imports_from | forja_lastro.py | EXTRACTED | forja_verificador.py:427 |
| forja_verificador.py | imports_from | forja_lastro.py | EXTRACTED | forja_verificador.py:427 |
| forja_verificador.py | imports_from | forja_alertas.py | EXTRACTED | forja_verificador.py:454 |
| forja_verificador.py::gate_g11 | calls | forja_verificador.py::_indice_fontes_oficiais | EXTRACTED | forja_verificador.py:165 |
| forja_verificador.py::gate_g11 | calls | forja_verificador.py::_ctx | EXTRACTED | forja_verificador.py:192 |
| forja_verificador.py::gate_g11 | calls | forja_verificador.py::_ctx | EXTRACTED | forja_verificador.py:201 |
| forja_verificador.py::gate_g1 | calls | forja_verificador.py::_ctx | EXTRACTED | forja_verificador.py:218 |
| forja_verificador.py::gate_g1 | calls | forja_verificador.py::_ctx | EXTRACTED | forja_verificador.py:222 |
| forja_verificador.py::gate_g1 | calls | forja_verificador.py::_ctx | EXTRACTED | forja_verificador.py:226 |
| forja_verificador.py::gate_g4 | calls | forja_verificador.py::_ctx | EXTRACTED | forja_verificador.py:282 |
| forja_verificador.py::gate_g6 | calls | forja_verificador.py::_ctx | EXTRACTED | forja_verificador.py:305 |
| forja_verificador.py::gate_g6 | calls | forja_verificador.py::_ctx | EXTRACTED | forja_verificador.py:312 |
| forja_verificador.py::gate_g8 | calls | forja_verificador.py::_ctx | EXTRACTED | forja_verificador.py:339 |
| forja_verificador.py::gate_g8 | calls | forja_verificador.py::_ctx | EXTRACTED | forja_verificador.py:343 |
| forja_verificador.py::gate_g9 | calls | forja_verificador.py::_ctx | EXTRACTED | forja_verificador.py:361 |
| forja_verificador.py::verificar | calls | forja_verificador.py::_carregar_contexto_lastro | EXTRACTED | forja_verificador.py:429 |
| forja_verificador.py::verificar | calls | forja_verificador.py::gate_g2 | EXTRACTED | forja_verificador.py:415 |
| forja_verificador.py::verificar | calls | forja_verificador.py::gate_g6 | EXTRACTED | forja_verificador.py:416 |
| forja_verificador.py::verificar | calls | forja_verificador.py::gate_g8 | EXTRACTED | forja_verificador.py:417 |
| forja_verificador.py::verificar | calls | forja_verificador.py::gate_g9 | EXTRACTED | forja_verificador.py:418 |
| forja_verificador.py::verificar | calls | forja_verificador.py::gate_g11 | EXTRACTED | forja_verificador.py:419 |
| forja_verificador.py::verificar | calls | forja_estilo_humano.py::analisar | EXTRACTED | forja_verificador.py:423 |
| forja_verificador.py::verificar | calls | forja_lastro.py::analisar_texto | EXTRACTED | forja_verificador.py:428 |
| forja_verificador.py::verificar | calls | forja_lastro.py::validar_gates_economicos | EXTRACTED | forja_verificador.py:431 |
| forja_visual.py | imports_from | forja_verificador.py | EXTRACTED | forja_visual.py:149 |
| forja_visual.py | imports_from | forja_lastro.py | EXTRACTED | forja_visual.py:150 |
| forja_visual.py::_larguras_tabela | calls | forja_visual.py::_norm | EXTRACTED | forja_visual.py:74 |
| forja_visual.py::_Mapa.__init__ | calls | forja_visual.py::_norm | EXTRACTED | forja_visual.py:85 |
| forja_visual.py::_Mapa.__init__ | calls | forja_visual.py::_norm | EXTRACTED | forja_visual.py:93 |
| forja_visual.py::_Mapa.__init__ | calls | forja_visual.py::_Mapa._valida | EXTRACTED | forja_visual.py:96 |
| forja_visual.py::_Mapa.__init__ | calls | forja_visual.py::_Mapa._valida | EXTRACTED | forja_visual.py:126 |
| forja_visual.py::_Mapa.__init__ | calls | forja_visual.py::_Mapa._valida | EXTRACTED | forja_visual.py:129 |
| forja_visual.py::_Mapa.__init__ | calls | forja_visual.py::_Mapa._valida | EXTRACTED | forja_visual.py:132 |
| forja_visual.py::_Mapa.__init__ | calls | forja_visual.py::_Mapa._valida | EXTRACTED | forja_visual.py:135 |
| forja_visual.py::_Mapa.__init__ | calls | forja_visual.py::_norm | EXTRACTED | forja_visual.py:127 |
| forja_visual.py::_Mapa.__init__ | calls | forja_visual.py::_norm | EXTRACTED | forja_visual.py:130 |
| forja_visual.py::_Mapa.__init__ | calls | forja_visual.py::_norm | EXTRACTED | forja_visual.py:133 |
| forja_visual.py::_Mapa.__init__ | calls | forja_visual.py::_norm | EXTRACTED | forja_visual.py:136 |
| forja_visual.py::_Mapa._valida | calls | forja_visual.py::_norm | EXTRACTED | forja_visual.py:141 |
| forja_visual.py::_Mapa._valida | calls | forja_visual.py::_norm | EXTRACTED | forja_visual.py:141 |
| forja_visual.py::compor | calls | forja_visual.py::_Mapa | EXTRACTED | forja_visual.py:161 |
| forja_visual.py::compor | calls | forja_visual.py::_norm | EXTRACTED | forja_visual.py:546 |
| forja_visual.py::compor | calls | forja_visual.py::_norm | EXTRACTED | forja_visual.py:436 |
| forja_visual.py::compor | calls | forja_verificador.py::verificar | EXTRACTED | forja_visual.py:151 |
| forja_visual.py::compor | calls | forja_visual.py::_consome_tabela | EXTRACTED | forja_visual.py:242 |
| forja_visual.py::compor | calls | forja_visual.py::_e_enderecamento | EXTRACTED | forja_visual.py:387 |
| forja_visual.py::compor | calls | forja_visual.py::_norm | EXTRACTED | forja_visual.py:555 |
| forja_visual.py::compor | calls | forja_lastro.py::material_economico | EXTRACTED | forja_visual.py:156 |
| forja_visual.py::compor | calls | forja_visual.py::_norm | EXTRACTED | forja_visual.py:300 |
| forja_visual.py::compor | calls | forja_visual.py::_e_enderecamento | EXTRACTED | forja_visual.py:331 |
| forja_visual.py::compor | calls | forja_visual.py::_larguras_tabela | EXTRACTED | forja_visual.py:282 |
| forja_visual.py::compor | calls | forja_visual.py::_norm | EXTRACTED | forja_visual.py:302 |
| forja_visual.py::compor | calls | forja_visual.py::_norm | EXTRACTED | forja_visual.py:398 |
| forja_visual.py::compor | calls | forja_visual.py::_norm | EXTRACTED | forja_visual.py:402 |
| forja_visual_build.py | imports_from | forja_visual_mapa_gen.py | EXTRACTED | forja_visual_build.py:30 |
| forja_visual_build.py | imports_from | forja_visual_figuras.py | EXTRACTED | forja_visual_build.py:31 |
| forja_visual_build.py | imports_from | forja_visual_figuras.py | EXTRACTED | forja_visual_build.py:31 |
| forja_visual_build.py | imports_from | forja_visual_figuras.py | EXTRACTED | forja_visual_build.py:31 |
| forja_visual_build.py | imports_from | forja_visual_figuras.py | EXTRACTED | forja_visual_build.py:31 |
| forja_visual_build.py | imports_from | forja_verificador.py | EXTRACTED | forja_visual_build.py:54 |
| forja_visual_build.py | imports_from | forja_lastro.py | EXTRACTED | forja_visual_build.py:55 |
| forja_visual_build.py | imports_from | forja_metricas_f7.py | EXTRACTED | forja_visual_build.py:56 |
| forja_visual_build.py | imports_from | forja_visual.py | EXTRACTED | forja_visual_build.py:93 |
| forja_visual_build.py | imports_from | forja_visual_qa_structural.py | EXTRACTED | forja_visual_build.py:104 |
| forja_visual_build.py | imports_from | forja_assinatura_visual.py | EXTRACTED | forja_visual_build.py:139 |
| forja_visual_build.py | imports_from | forja_svg_docx.py | EXTRACTED | forja_visual_build.py:102 |
| forja_visual_build.py::build | calls | forja_verificador.py::verificar | EXTRACTED | forja_visual_build.py:57 |
| forja_visual_build.py::build | calls | forja_visual_figuras.py::carregar_brief | EXTRACTED | forja_visual_build.py:80 |
| forja_visual_build.py::build | calls | forja_visual_mapa_gen.py::gerar_mapa | EXTRACTED | forja_visual_build.py:88 |
| forja_visual_build.py::build | calls | forja_visual_figuras.py::gerar_figuras | EXTRACTED | forja_visual_build.py:89 |
| forja_visual_build.py::build | calls | forja_visual.py::compor | EXTRACTED | forja_visual_build.py:95 |
| forja_visual_build.py::build | calls | forja_visual_qa_structural.py::auditar_documento | EXTRACTED | forja_visual_build.py:105 |
| forja_visual_build.py::build | calls | forja_assinatura_visual.py::avaliar | EXTRACTED | forja_visual_build.py:145 |
| forja_visual_build.py::build | calls | forja_visual_build.py::_tipo_produto | EXTRACTED | forja_visual_build.py:51 |
| forja_visual_build.py::build | calls | forja_metricas_f7.py::metricas_f7 | EXTRACTED | forja_visual_build.py:70 |
| forja_visual_build.py::build | calls | forja_visual_figuras.py::validar_brief | EXTRACTED | forja_visual_build.py:81 |
| forja_visual_build.py::build | calls | forja_svg_docx.py::inserir_svgs | EXTRACTED | forja_visual_build.py:103 |
| forja_visual_build.py::build | calls | forja_lastro.py::material_economico | EXTRACTED | forja_visual_build.py:62 |
| forja_visual_build.py::build | calls | forja_lastro.py::material_economico | EXTRACTED | forja_visual_build.py:175 |
| forja_visual_figuras.py | imports_from | forja_visual_mapa_gen.py | EXTRACTED | forja_visual_figuras.py:154 |
| forja_visual_figuras.py | imports_from | forja_visual_mapa_gen.py | EXTRACTED | forja_visual_figuras.py:412 |
| forja_visual_figuras.py | imports_from | forja_visual_mapa_gen.py | EXTRACTED | forja_visual_figuras.py:383 |
| forja_visual_figuras.py::_datas | calls | forja_visual_figuras.py::_mascara | EXTRACTED | forja_visual_figuras.py:63 |
| forja_visual_figuras.py::_datas | calls | forja_visual_figuras.py::_chave | EXTRACTED | forja_visual_figuras.py:69 |
| forja_visual_figuras.py::_datas | calls | forja_visual_figuras.py::_chave | EXTRACTED | forja_visual_figuras.py:77 |
| forja_visual_figuras.py::_oracao | calls | forja_visual_figuras.py::_limpa | EXTRACTED | forja_visual_figuras.py:88 |
| forja_visual_figuras.py::extrair_cronologia | calls | forja_visual_figuras.py::_fonte_cronologica | EXTRACTED | forja_visual_figuras.py:155 |
| forja_visual_figuras.py::extrair_cronologia | calls | forja_visual_mapa_gen.py::_varre | EXTRACTED | forja_visual_figuras.py:158 |
| forja_visual_figuras.py::extrair_cronologia | calls | forja_visual_figuras.py::_datas | EXTRACTED | forja_visual_figuras.py:164 |
| forja_visual_figuras.py::extrair_cronologia | calls | forja_visual_figuras.py::_oracao | EXTRACTED | forja_visual_figuras.py:175 |
| forja_visual_figuras.py::validar_brief | calls | forja_visual_figuras.py::_limpa | EXTRACTED | forja_visual_figuras.py:238 |
| forja_visual_figuras.py::extrair_comparacao | calls | forja_visual_figuras.py::_limpa | EXTRACTED | forja_visual_figuras.py:300 |
| forja_visual_figuras.py::extrair_comparacao | calls | forja_visual_figuras.py::_limpa | EXTRACTED | forja_visual_figuras.py:307 |
| forja_visual_figuras.py::gerar_figuras | calls | forja_visual_figuras.py::extrair_comparacao | EXTRACTED | forja_visual_figuras.py:335 |
| forja_visual_figuras.py::gerar_figuras | calls | forja_visual_figuras.py::extrair_encadeamento | EXTRACTED | forja_visual_figuras.py:341 |
| forja_visual_figuras.py::gerar_figuras | calls | forja_visual_figuras.py::extrair_comparacao | EXTRACTED | forja_visual_figuras.py:347 |
| forja_visual_figuras.py::gerar_figuras | calls | forja_visual_mapa_gen.py::_varre | EXTRACTED | forja_visual_figuras.py:395 |
| forja_visual_figuras.py::gerar_figuras | calls | forja_visual_figuras.py::extrair_cronologia | EXTRACTED | forja_visual_figuras.py:330 |
| forja_visual_mapa_gen.py::_varre | calls | forja_visual_mapa_gen.py::_e_enderecamento | EXTRACTED | forja_visual_mapa_gen.py:131 |
| forja_visual_mapa_gen.py::_varre | calls | forja_visual_mapa_gen.py::_norm | EXTRACTED | forja_visual_mapa_gen.py:188 |
| forja_visual_mapa_gen.py::_varre | calls | forja_visual_mapa_gen.py::_e_enderecamento | EXTRACTED | forja_visual_mapa_gen.py:109 |
| forja_visual_mapa_gen.py::_varre | calls | forja_visual_mapa_gen.py::_norm | EXTRACTED | forja_visual_mapa_gen.py:94 |
| forja_visual_mapa_gen.py::_ancora | calls | forja_visual_mapa_gen.py::_limpa | EXTRACTED | forja_visual_mapa_gen.py:211 |
| forja_visual_mapa_gen.py::_ancora | calls | forja_visual_mapa_gen.py::_norm | EXTRACTED | forja_visual_mapa_gen.py:218 |
| forja_visual_mapa_gen.py::_frase | calls | forja_visual_mapa_gen.py::_limpa | EXTRACTED | forja_visual_mapa_gen.py:227 |
| forja_visual_mapa_gen.py::_rotulos_sintese | calls | forja_visual_mapa_gen.py::_rotulo_curto | EXTRACTED | forja_visual_mapa_gen.py:319 |
| forja_visual_mapa_gen.py::gerar_mapa | calls | forja_visual_mapa_gen.py::_varre | EXTRACTED | forja_visual_mapa_gen.py:331 |
| forja_visual_mapa_gen.py::gerar_mapa | calls | forja_visual_mapa_gen.py::_norm | EXTRACTED | forja_visual_mapa_gen.py:340 |
| forja_visual_mapa_gen.py::gerar_mapa | calls | forja_visual_mapa_gen.py::_rotulos_sintese | EXTRACTED | forja_visual_mapa_gen.py:356 |
| forja_visual_mapa_gen.py::gerar_mapa | calls | forja_visual_mapa_gen.py::_autovalidar | EXTRACTED | forja_visual_mapa_gen.py:470 |
| forja_visual_mapa_gen.py::gerar_mapa | calls | forja_visual_mapa_gen.py::_frase | EXTRACTED | forja_visual_mapa_gen.py:349 |
| forja_visual_mapa_gen.py::gerar_mapa | calls | forja_visual_mapa_gen.py::_limpa | EXTRACTED | forja_visual_mapa_gen.py:364 |
| forja_visual_mapa_gen.py::gerar_mapa | calls | forja_visual_mapa_gen.py::_frase | EXTRACTED | forja_visual_mapa_gen.py:396 |
| forja_visual_mapa_gen.py::gerar_mapa | calls | forja_visual_mapa_gen.py::_ancora | EXTRACTED | forja_visual_mapa_gen.py:378 |
| forja_visual_mapa_gen.py::gerar_mapa | calls | forja_visual_mapa_gen.py::_titulo_precedente | EXTRACTED | forja_visual_mapa_gen.py:378 |
| forja_visual_mapa_gen.py::gerar_mapa | calls | forja_visual_mapa_gen.py::_ancora | EXTRACTED | forja_visual_mapa_gen.py:420 |
| forja_visual_mapa_gen.py::gerar_mapa | calls | forja_visual_mapa_gen.py::_frase | EXTRACTED | forja_visual_mapa_gen.py:420 |
| forja_visual_mapa_gen.py::gerar_mapa | calls | forja_visual_mapa_gen.py::_frase | EXTRACTED | forja_visual_mapa_gen.py:408 |
| forja_visual_mapa_gen.py::gerar_mapa | calls | forja_visual_mapa_gen.py::_ancora | EXTRACTED | forja_visual_mapa_gen.py:433 |
| forja_visual_mapa_gen.py::gerar_mapa | calls | forja_visual_mapa_gen.py::_ancora | EXTRACTED | forja_visual_mapa_gen.py:440 |
| forja_visual_mapa_gen.py::gerar_mapa | calls | forja_visual_mapa_gen.py::_norm | EXTRACTED | forja_visual_mapa_gen.py:382 |
| forja_visual_mapa_gen.py::gerar_mapa | calls | forja_visual_mapa_gen.py::_norm | EXTRACTED | forja_visual_mapa_gen.py:424 |
| forja_visual_mapa_gen.py::gerar_mapa | calls | forja_visual_mapa_gen.py::_ancora | EXTRACTED | forja_visual_mapa_gen.py:454 |
| forja_visual_mapa_gen.py::gerar_mapa | calls | forja_visual_mapa_gen.py::_norm | EXTRACTED | forja_visual_mapa_gen.py:382 |
| forja_visual_mapa_gen.py::gerar_mapa | calls | forja_visual_mapa_gen.py::_limpa | EXTRACTED | forja_visual_mapa_gen.py:408 |
| forja_visual_mapa_gen.py::gerar_mapa | calls | forja_visual_mapa_gen.py::_norm | EXTRACTED | forja_visual_mapa_gen.py:424 |
| forja_visual_mapa_gen.py::gerar_mapa | calls | forja_visual_mapa_gen.py::_limpa | EXTRACTED | forja_visual_mapa_gen.py:437 |
| forja_visual_mapa_gen.py::gerar_mapa | calls | forja_visual_mapa_gen.py::_limpa | EXTRACTED | forja_visual_mapa_gen.py:451 |
| forja_visual_mapa_gen.py::_autovalidar | calls | forja_visual_mapa_gen.py::_norm | EXTRACTED | forja_visual_mapa_gen.py:477 |
| forja_visual_mapa_gen.py::_autovalidar | calls | forja_visual_mapa_gen.py::_checa | EXTRACTED | forja_visual_mapa_gen.py:483 |
| forja_visual_mapa_gen.py::_autovalidar | calls | forja_visual_mapa_gen.py::_checa | EXTRACTED | forja_visual_mapa_gen.py:485 |
| forja_visual_mapa_gen.py::_autovalidar | calls | forja_visual_mapa_gen.py::_checa | EXTRACTED | forja_visual_mapa_gen.py:481 |
| forja_visual_mapa_gen.py::_checa | calls | forja_visual_mapa_gen.py::_norm | EXTRACTED | forja_visual_mapa_gen.py:489 |
| forja_visual_mapa_gen.py::gravar_mapa | calls | forja_visual_mapa_gen.py::gerar_mapa | EXTRACTED | forja_visual_mapa_gen.py:502 |
| forja_visual_qa.py | imports_from | forja_n3_common.py | EXTRACTED | forja_visual_qa.py:11 |
| forja_visual_qa.py | imports_from | forja_n3_common.py | EXTRACTED | forja_visual_qa.py:11 |
| forja_visual_qa.py | imports_from | forja_n3_common.py | EXTRACTED | forja_visual_qa.py:11 |
| forja_visual_qa.py | imports_from | forja_n3_common.py | EXTRACTED | forja_visual_qa.py:11 |
| forja_visual_qa.py | imports_from | forja_n3_common.py | EXTRACTED | forja_visual_qa.py:11 |
| forja_visual_qa.py | imports_from | forja_docx_layout.py | EXTRACTED | forja_visual_qa.py:15 |
| forja_visual_qa.py | imports_from | forja_fidelity.py | EXTRACTED | forja_visual_qa.py:16 |
| forja_visual_qa.py | imports_from | forja_visual_review.py | EXTRACTED | forja_visual_qa.py:17 |
| forja_visual_qa.py | imports_from | forja_visual_review.py | EXTRACTED | forja_visual_qa.py:17 |
| forja_visual_qa.py::lint_docx | calls | forja_visual_qa.py::lint_text | EXTRACTED | forja_visual_qa.py:47 |
| forja_visual_qa.py::lint_docx | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_visual_qa.py:50 |
| forja_visual_qa.py::inspect_pdf | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_visual_qa.py:66 |
| forja_visual_qa.py::inspect_pdf | calls | forja_visual_qa.py::lint_text | EXTRACTED | forja_visual_qa.py:75 |
| forja_visual_qa.py::inspect_pdf | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_visual_qa.py:116 |
| forja_visual_qa.py::inspect_pdf | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_visual_qa.py:100 |
| forja_visual_qa.py::inspect_pdf | calls | forja_visual_qa.py::_overlap_ratio | EXTRACTED | forja_visual_qa.py:81 |
| forja_visual_qa.py::inspect_pdf | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_visual_qa.py:108 |
| forja_visual_qa.py::run_visual_qa | calls | forja_visual_qa.py::inspect_pdf | EXTRACTED | forja_visual_qa.py:145 |
| forja_visual_qa.py::run_visual_qa | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_visual_qa.py:217 |
| forja_visual_qa.py::run_visual_qa | calls | forja_visual_qa.py::lint_docx | EXTRACTED | forja_visual_qa.py:143 |
| forja_visual_qa.py::run_visual_qa | calls | forja_docx_layout.py::audit_docx_layout | EXTRACTED | forja_visual_qa.py:144 |
| forja_visual_qa.py::run_visual_qa | calls | forja_fidelity.py::write_fidelity | EXTRACTED | forja_visual_qa.py:151 |
| forja_visual_qa.py::run_visual_qa | calls | forja_visual_review.py::build_pending_review | EXTRACTED | forja_visual_qa.py:164 |
| forja_visual_qa.py::run_visual_qa | calls | forja_visual_review.py::validate_visual_review | EXTRACTED | forja_visual_qa.py:179 |
| forja_visual_qa.py::run_visual_qa | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_visual_qa.py:205 |
| forja_visual_qa.py::run_visual_qa | calls | forja_n3_common.py::ForjaN3Error | EXTRACTED | forja_visual_qa.py:149 |
| forja_visual_qa.py::run_visual_qa | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_visual_qa.py:174 |
| forja_visual_qa.py::main | calls | forja_visual_qa.py::run_visual_qa | EXTRACTED | forja_visual_qa.py:236 |
| forja_visual_qa_structural.py | imports_from | forja_fidelity.py | EXTRACTED | forja_visual_qa_structural.py:17 |
| forja_visual_qa_structural.py | imports_from | forja_n3_common.py | EXTRACTED | forja_visual_qa_structural.py:18 |
| forja_visual_qa_structural.py | imports_from | forja_n3_common.py | EXTRACTED | forja_visual_qa_structural.py:18 |
| forja_visual_qa_structural.py | imports_from | forja_visual_qa.py | EXTRACTED | forja_visual_qa_structural.py:83 |
| forja_visual_qa_structural.py | imports_from | forja_docx_layout.py | EXTRACTED | forja_visual_qa_structural.py:84 |
| forja_visual_qa_structural.py::_svg_check | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_visual_qa_structural.py:39 |
| forja_visual_qa_structural.py::_docx_lint | calls | forja_visual_qa.py::lint_docx | EXTRACTED | forja_visual_qa_structural.py:86 |
| forja_visual_qa_structural.py::_docx_lint | calls | forja_docx_layout.py::audit_docx_layout | EXTRACTED | forja_visual_qa_structural.py:88 |
| forja_visual_qa_structural.py::auditar_documento | calls | forja_visual_qa_structural.py::_package_audit | EXTRACTED | forja_visual_qa_structural.py:98 |
| forja_visual_qa_structural.py::auditar_documento | calls | forja_visual_qa_structural.py::_docx_lint | EXTRACTED | forja_visual_qa_structural.py:99 |
| forja_visual_qa_structural.py::auditar_documento | calls | forja_fidelity.py::compare_docx_fidelity | EXTRACTED | forja_visual_qa_structural.py:100 |
| forja_visual_qa_structural.py::auditar_documento | calls | forja_visual_qa_structural.py::_svg_check | EXTRACTED | forja_visual_qa_structural.py:101 |
| forja_visual_qa_structural.py::auditar_documento | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_visual_qa_structural.py:111 |
| forja_visual_qa_structural.py::auditar_documento | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_visual_qa_structural.py:116 |
| forja_visual_qa_structural.py::write_audit | calls | forja_visual_qa_structural.py::auditar_documento | EXTRACTED | forja_visual_qa_structural.py:128 |
| forja_visual_review.py | imports_from | forja_n3_common.py | EXTRACTED | forja_visual_review.py:20 |
| forja_visual_review.py | imports_from | forja_n3_common.py | EXTRACTED | forja_visual_review.py:20 |
| forja_visual_review.py | imports_from | forja_n3_common.py | EXTRACTED | forja_visual_review.py:20 |
| forja_visual_review.py | imports_from | forja_n3_common.py | EXTRACTED | forja_visual_review.py:20 |
| forja_visual_review.py::build_pending_review | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | forja_visual_review.py:82 |
| forja_visual_review.py::build_pending_review | calls | forja_n3_common.py::now_iso | EXTRACTED | forja_visual_review.py:69 |
| forja_visual_review.py::build_pending_review | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_visual_review.py:75 |
| forja_visual_review.py::build_pending_review | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_visual_review.py:76 |
| forja_visual_review.py::validate_visual_review | calls | forja_n3_common.py::read_json | EXTRACTED | forja_visual_review.py:97 |
| forja_visual_review.py::validate_visual_review | calls | forja_visual_review.py::_rendered_page_map | EXTRACTED | forja_visual_review.py:137 |
| forja_visual_review.py::validate_visual_review | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_visual_review.py:115 |
| forja_visual_review.py::validate_visual_review | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_visual_review.py:174 |
| forja_visual_review.py::validate_visual_review | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_visual_review.py:117 |
| forja_visual_review.py::validate_visual_review | calls | forja_n3_common.py::sha256_file | EXTRACTED | forja_visual_review.py:152 |
| generate_n4_contracts.py | imports_from | forja_n3_common.py | EXTRACTED | generate_n4_contracts.py:8 |
| generate_n4_contracts.py | imports_from | forja_n3_common.py | EXTRACTED | generate_n4_contracts.py:8 |
| generate_n4_contracts.py | imports_from | forja_n3_common.py | EXTRACTED | generate_n4_contracts.py:8 |
| generate_n4_contracts.py | imports_from | forja_n3_common.py | EXTRACTED | generate_n4_contracts.py:8 |
| generate_n4_contracts.py | imports_from | forja_n4_common.py | EXTRACTED | generate_n4_contracts.py:9 |
| generate_n4_contracts.py | imports_from | forja_n4_common.py | EXTRACTED | generate_n4_contracts.py:9 |
| generate_n4_contracts.py::generate | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | generate_n4_contracts.py:550 |
| generate_n4_contracts.py::generate | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | generate_n4_contracts.py:583 |
| generate_n4_contracts.py::generate | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | generate_n4_contracts.py:597 |
| generate_n4_contracts.py::generate | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | generate_n4_contracts.py:581 |
| generate_n4_contracts.py::generate | calls | forja_n3_common.py::read_json | EXTRACTED | generate_n4_contracts.py:585 |
| generate_n4_contracts.py::generate | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | generate_n4_contracts.py:596 |
| render_forja_atlas.py::render_diagrams | calls | render_forja_atlas.py::mermaid_command | EXTRACTED | render_forja_atlas.py:51 |
| render_forja_atlas.py::render_diagrams | calls | render_forja_atlas.py::namespace_svg_ids | EXTRACTED | render_forja_atlas.py:74 |
| render_forja_atlas.py::build_html | calls | render_forja_atlas.py::render_diagrams | EXTRACTED | render_forja_atlas.py:107 |
| render_forja_atlas.py::build_html | calls | render_forja_atlas.py::slugify | EXTRACTED | render_forja_atlas.py:114 |
| render_forja_atlas.py::main | calls | render_forja_atlas.py::build_html | EXTRACTED | render_forja_atlas.py:290 |
| validate_forja_n3.py | imports_from | forja_n3_common.py | EXTRACTED | validate_forja_n3.py:13 |
| validate_forja_n3.py | imports_from | forja_n3_common.py | EXTRACTED | validate_forja_n3.py:13 |
| validate_forja_n3.py | imports_from | forja_n3_common.py | EXTRACTED | validate_forja_n3.py:13 |
| validate_forja_n3.py | imports_from | forja_n3_common.py | EXTRACTED | validate_forja_n3.py:13 |
| validate_forja_n3.py | imports_from | forja_phase_contracts.py | EXTRACTED | validate_forja_n3.py:14 |
| validate_forja_n3.py::main | calls | forja_phase_contracts.py::validate_all | EXTRACTED | validate_forja_n3.py:130 |
| validate_forja_n3.py::main | calls | validate_forja_n3.py::validate_json_files | EXTRACTED | validate_forja_n3.py:131 |
| validate_forja_n3.py::main | calls | forja_n3_common.py::atomic_write_json | EXTRACTED | validate_forja_n3.py:143 |
| validate_forja_n3.py::main | calls | validate_forja_n3.py::run_command | EXTRACTED | validate_forja_n3.py:110 |
| validate_forja_n3.py::main | calls | validate_forja_n3.py::run_command | EXTRACTED | validate_forja_n3.py:111 |
| validate_forja_n3.py::main | calls | forja_n3_common.py::now_iso | EXTRACTED | validate_forja_n3.py:135 |
| validate_forja_n3.py::main | calls | validate_forja_n3.py::run_command | EXTRACTED | validate_forja_n3.py:117 |
| validate_forja_n3.py::main | calls | validate_forja_n3.py::run_command | EXTRACTED | validate_forja_n3.py:119 |
| validate_forja_n3.py::main | calls | validate_forja_n3.py::run_command | EXTRACTED | validate_forja_n3.py:125 |
| forja_ar_architecture.py | validates_against | n4_schemas/ARTIFACT_CATALOG.json | EXTRACTED | forja_ar_architecture.py:70 |
| forja_ar_architecture.py | validates_against | n4_schemas/document_comparison.schema.json | EXTRACTED | forja_ar_architecture.py:74 |
| forja_ar_architecture.py | validates_against | n4_schemas/learning_candidate.schema.json | EXTRACTED | forja_ar_architecture.py:75 |
| forja_ar_architecture.py | validates_against | n4_schemas/post_protocol_baseline_backfill.schema.json | EXTRACTED | forja_ar_architecture.py:73 |
| forja_ar_architecture.py | validates_against | n4_schemas/post_protocol_return.schema.json | EXTRACTED | forja_ar_architecture.py:71 |
| forja_ar_architecture.py | validates_against | n4_schemas/protocol_evidence.schema.json | EXTRACTED | forja_ar_architecture.py:72 |
| forja_consistency.py | validates_against | n4_schemas/N4_LAYOUT_PROFILES.json | EXTRACTED | forja_consistency.py:30 |
| forja_f8_contract.py | validates_against | phase_contracts/F8.json | EXTRACTED | forja_f8_contract.py:102 |
| forja_f8_contract.py | validates_against | phase_contracts_n4/F8.json | EXTRACTED | forja_f8_contract.py:102 |
| forja_n4_common.py | validates_against | n4_schemas/document_comparison.schema.json | EXTRACTED | forja_n4_common.py:87 |
| forja_n4_common.py | validates_against | n4_schemas/learning_candidate.schema.json | EXTRACTED | forja_n4_common.py:93 |
| forja_n4_common.py | validates_against | n4_schemas/post_protocol_baseline_backfill.schema.json | EXTRACTED | forja_n4_common.py:73 |
| forja_n4_common.py | validates_against | n4_schemas/post_protocol_return.schema.json | EXTRACTED | forja_n4_common.py:61 |
| forja_n4_common.py | validates_against | n4_schemas/protocol_evidence.schema.json | EXTRACTED | forja_n4_common.py:67 |
| forja_n4_validate.py | validates_against | n4_schemas/ARTIFACT_CATALOG.json | EXTRACTED | forja_n4_validate.py:393 |
| forja_package.py | validates_against | phase_contracts/F7.json | EXTRACTED | forja_package.py:60 |
| forja_package.py | validates_against | phase_contracts/F8.json | EXTRACTED | forja_package.py:61 |
| forja_package.py | validates_against | phase_contracts/F9.json | EXTRACTED | forja_package.py:62 |
| forja_package.py | validates_against | phase_contracts_n4/F7.json | EXTRACTED | forja_package.py:60 |
| forja_package.py | validates_against | phase_contracts_n4/F8.json | EXTRACTED | forja_package.py:61 |
| forja_package.py | validates_against | phase_contracts_n4/F9.json | EXTRACTED | forja_package.py:62 |
| forja_pso_pet.py | validates_against | pso_schemas/PSO_CASE_EXAMPLE.json | EXTRACTED | forja_pso_pet.py:621 |
| forja_regua.py | validates_against | phase_contracts/F6.json | EXTRACTED | forja_regua.py:197 |
| forja_regua.py | validates_against | phase_contracts/F7.json | EXTRACTED | forja_regua.py:198 |
| forja_regua.py | validates_against | phase_contracts/F8.json | EXTRACTED | forja_regua.py:199 |
| forja_regua.py | validates_against | phase_contracts/F9.json | EXTRACTED | forja_regua.py:200 |
| forja_regua.py | validates_against | phase_contracts_n4/F6.json | EXTRACTED | forja_regua.py:197 |
| forja_regua.py | validates_against | phase_contracts_n4/F7.json | EXTRACTED | forja_regua.py:198 |
| forja_regua.py | validates_against | phase_contracts_n4/F8.json | EXTRACTED | forja_regua.py:199 |
| forja_regua.py | validates_against | phase_contracts_n4/F9.json | EXTRACTED | forja_regua.py:200 |
| forja_regua.py | validates_against | n4_schemas/N4_LAYOUT_PROFILES.json | EXTRACTED | forja_regua.py:205 |
| generate_n4_contracts.py | validates_against | phase_contracts_n4/EXTENSIONS.json | EXTRACTED | generate_n4_contracts.py:597 |
| generate_n4_contracts.py | validates_against | n4_schemas/ARTIFACT_CATALOG.json | EXTRACTED | generate_n4_contracts.py:583 |
| generate_n4_contracts.py | validates_against | n4_schemas/common.schema.json | EXTRACTED | generate_n4_contracts.py:14 |
| forja_metricas_f7.py | tested_by | test_f7_campos.py | EXTRACTED | test_f7_campos.py:1 |
| forja_adocao_rota.py | tested_by | test_forja_adocao_rota.py | EXTRACTED | test_forja_adocao_rota.py:1 |
| forja_adversarial_audit.py | tested_by | test_forja_adversarial_audit.py | EXTRACTED | test_forja_adversarial_audit.py:1 |
| forja_n3_common.py | tested_by | test_forja_adversarial_audit.py | EXTRACTED | test_forja_adversarial_audit.py:1 |
| forja_adversarial_gate.py | tested_by | test_forja_adversarial_gate.py | EXTRACTED | test_forja_adversarial_gate.py:1 |
| forja_replay.py | tested_by | test_forja_adversarial_gate.py | EXTRACTED | test_forja_adversarial_gate.py:1 |
| forja_alertas.py | tested_by | test_forja_alertas.py | EXTRACTED | test_forja_alertas.py:1 |
| forja_citations.py | tested_by | test_forja_anti_cheat.py | EXTRACTED | test_forja_anti_cheat.py:1 |
| forja_docx_layout.py | tested_by | test_forja_anti_cheat.py | EXTRACTED | test_forja_anti_cheat.py:1 |
| forja_human_review.py | tested_by | test_forja_anti_cheat.py | EXTRACTED | test_forja_anti_cheat.py:1 |
| forja_metricas_f7.py | tested_by | test_forja_anti_cheat.py | EXTRACTED | test_forja_anti_cheat.py:1 |
| forja_n3_common.py | tested_by | test_forja_anti_cheat.py | EXTRACTED | test_forja_anti_cheat.py:1 |
| forja_official_sources.py | tested_by | test_forja_anti_cheat.py | EXTRACTED | test_forja_anti_cheat.py:1 |
| forja_package.py | tested_by | test_forja_anti_cheat.py | EXTRACTED | test_forja_anti_cheat.py:1 |
| forja_visual_qa.py | tested_by | test_forja_anti_cheat.py | EXTRACTED | test_forja_anti_cheat.py:1 |
| forja_visual_review.py | tested_by | test_forja_anti_cheat.py | EXTRACTED | test_forja_anti_cheat.py:1 |
| forja_authorities.py | tested_by | test_forja_anti_hallucination_v2.py | EXTRACTED | test_forja_anti_hallucination_v2.py:1 |
| forja_claim_binding.py | tested_by | test_forja_anti_hallucination_v2.py | EXTRACTED | test_forja_anti_hallucination_v2.py:1 |
| forja_delivery.py | tested_by | test_forja_anti_hallucination_v2.py | EXTRACTED | test_forja_anti_hallucination_v2.py:1 |
| forja_editorial_fidelity.py | tested_by | test_forja_anti_hallucination_v2.py | EXTRACTED | test_forja_anti_hallucination_v2.py:1 |
| forja_n3_common.py | tested_by | test_forja_anti_hallucination_v2.py | EXTRACTED | test_forja_anti_hallucination_v2.py:1 |
| forja_official_sources.py | tested_by | test_forja_anti_hallucination_v2.py | EXTRACTED | test_forja_anti_hallucination_v2.py:1 |
| forja_package.py | tested_by | test_forja_anti_hallucination_v2.py | EXTRACTED | test_forja_anti_hallucination_v2.py:1 |
| forja_ar_architecture.py | tested_by | test_forja_ar_architecture.py | EXTRACTED | test_forja_ar_architecture.py:1 |
| forja_n3_common.py | tested_by | test_forja_ar_architecture.py | EXTRACTED | test_forja_ar_architecture.py:1 |
| forja_post_protocol.py | tested_by | test_forja_ar_architecture.py | EXTRACTED | test_forja_ar_architecture.py:1 |
| forja_f8_contract.py | tested_by | test_forja_architecture.py | EXTRACTED | test_forja_architecture.py:1 |
| forja_package.py | tested_by | test_forja_architecture.py | EXTRACTED | test_forja_architecture.py:1 |
| forja_artefatos.py | tested_by | test_forja_artefatos.py | EXTRACTED | test_forja_artefatos.py:1 |
| forja_assinatura_visual.py | tested_by | test_forja_assinatura_antimoldagem.py | EXTRACTED | test_forja_assinatura_antimoldagem.py:1 |
| forja_exploracao_100.py | tested_by | test_forja_assinatura_lite.py | EXTRACTED | test_forja_assinatura_lite.py:1 |
| forja_legal_search.py | tested_by | test_forja_assinatura_lite.py | EXTRACTED | test_forja_assinatura_lite.py:1 |
| forja_n3_common.py | tested_by | test_forja_assinatura_lite.py | EXTRACTED | test_forja_assinatura_lite.py:1 |
| forja_n4_common.py | tested_by | test_forja_assinatura_lite.py | EXTRACTED | test_forja_assinatura_lite.py:1 |
| forja_n4_invalidation.py | tested_by | test_forja_assinatura_lite.py | EXTRACTED | test_forja_assinatura_lite.py:1 |
| forja_n4_validate.py | tested_by | test_forja_assinatura_lite.py | EXTRACTED | test_forja_assinatura_lite.py:1 |
| forja_official_sources.py | tested_by | test_forja_assinatura_lite.py | EXTRACTED | test_forja_assinatura_lite.py:1 |
| forja_precedente.py | tested_by | test_forja_assinatura_lite.py | EXTRACTED | test_forja_assinatura_lite.py:1 |
| forja_reasoning.py | tested_by | test_forja_assinatura_lite.py | EXTRACTED | test_forja_assinatura_lite.py:1 |
| forja_assinatura_visual.py | tested_by | test_forja_assinatura_visual.py | EXTRACTED | test_forja_assinatura_visual.py:1 |
| forja_ar_blind.py | tested_by | test_forja_autoresearch.py | EXTRACTED | test_forja_autoresearch.py:1 |
| forja_ar_canarios.py | tested_by | test_forja_autoresearch.py | EXTRACTED | test_forja_autoresearch.py:1 |
| forja_ar_ciclo.py | tested_by | test_forja_autoresearch.py | EXTRACTED | test_forja_autoresearch.py:1 |
| forja_ar_corpus.py | tested_by | test_forja_autoresearch.py | EXTRACTED | test_forja_autoresearch.py:1 |
| forja_ar_evolucao.py | tested_by | test_forja_autoresearch.py | EXTRACTED | test_forja_autoresearch.py:1 |
| forja_ar_indicadores.py | tested_by | test_forja_autoresearch.py | EXTRACTED | test_forja_autoresearch.py:1 |
| forja_ar_runpair.py | tested_by | test_forja_autoresearch.py | EXTRACTED | test_forja_autoresearch.py:1 |
| forja_axi.py | tested_by | test_forja_axi.py | EXTRACTED | test_forja_axi.py:1 |
| forja_baseline_aprovado.py | tested_by | test_forja_baseline_aprovado.py | EXTRACTED | test_forja_baseline_aprovado.py:1 |
| forja_bench_modelos.py | tested_by | test_forja_bench_modelos.py | EXTRACTED | test_forja_bench_modelos.py:1 |
| forja_canario_catraca.py | tested_by | test_forja_canario_catraca.py | EXTRACTED | test_forja_canario_catraca.py:1 |
| forja_canario_mutacao.py | tested_by | test_forja_canario_mutacao.py | EXTRACTED | test_forja_canario_mutacao.py:1 |
| forja_citations.py | tested_by | test_forja_citacoes.py | EXTRACTED | test_forja_citacoes.py:1 |
| forja_conselho.py | tested_by | test_forja_conselho.py | EXTRACTED | test_forja_conselho.py:1 |
| forja_delivery.py | tested_by | test_forja_conselho_1107.py | EXTRACTED | test_forja_conselho_1107.py:1 |
| forja_contexto.py | tested_by | test_forja_contexto.py | EXTRACTED | test_forja_contexto.py:1 |
| forja_editorial.py | tested_by | test_forja_editorial.py | EXTRACTED | test_forja_editorial.py:1 |
| forja_editorial_fidelity.py | tested_by | test_forja_editorial.py | EXTRACTED | test_forja_editorial.py:1 |
| forja_editorial_model.py | tested_by | test_forja_editorial.py | EXTRACTED | test_forja_editorial.py:1 |
| forja_n3_common.py | tested_by | test_forja_editorial.py | EXTRACTED | test_forja_editorial.py:1 |
| forja_phase_contracts.py | tested_by | test_forja_editorial.py | EXTRACTED | test_forja_editorial.py:1 |
| forja_entrega.py | tested_by | test_forja_entrega.py | EXTRACTED | test_forja_entrega.py:1 |
| forja_estilo_humano.py | tested_by | test_forja_estilo_humano.py | EXTRACTED | test_forja_estilo_humano.py:1 |
| forja_n3_common.py | tested_by | test_forja_estilo_humano.py | EXTRACTED | test_forja_estilo_humano.py:1 |
| forja_package.py | tested_by | test_forja_estilo_humano.py | EXTRACTED | test_forja_estilo_humano.py:1 |
| forja_render_docx.py | tested_by | test_forja_estilo_humano.py | EXTRACTED | test_forja_estilo_humano.py:1 |
| forja_run.py | tested_by | test_forja_estilo_humano.py | EXTRACTED | test_forja_estilo_humano.py:1 |
| forja_exploracao_100.py | tested_by | test_forja_exploracao_100.py | EXTRACTED | test_forja_exploracao_100.py:1 |
| forja_n3_common.py | tested_by | test_forja_exploracao_100.py | EXTRACTED | test_forja_exploracao_100.py:1 |
| forja_n4_common.py | tested_by | test_forja_exploracao_100.py | EXTRACTED | test_forja_exploracao_100.py:1 |
| forja_n4_validate.py | tested_by | test_forja_exploracao_100.py | EXTRACTED | test_forja_exploracao_100.py:1 |
| forja_phase_contracts.py | tested_by | test_forja_exploracao_100.py | EXTRACTED | test_forja_exploracao_100.py:1 |
| forja_reconcile.py | tested_by | test_forja_exploracao_100.py | EXTRACTED | test_forja_exploracao_100.py:1 |
| forja_run.py | tested_by | test_forja_exploracao_100.py | EXTRACTED | test_forja_exploracao_100.py:1 |
| forja_f2_check.py | tested_by | test_forja_f2_check.py | EXTRACTED | test_forja_f2_check.py:1 |
| forja_f8_contract.py | tested_by | test_forja_f8_gates_contrato.py | EXTRACTED | test_forja_f8_gates_contrato.py:1 |
| forja_docx_layout.py | tested_by | test_forja_f8_pecas_reais.py | EXTRACTED | test_forja_f8_pecas_reais.py:1 |
| forja_visual_qa_structural.py | tested_by | test_forja_f8_pecas_reais.py | EXTRACTED | test_forja_f8_pecas_reais.py:1 |
| forja_f8_contract.py | tested_by | test_forja_f8_static.py | EXTRACTED | test_forja_f8_static.py:1 |
| forja_n3_common.py | tested_by | test_forja_f8_static.py | EXTRACTED | test_forja_f8_static.py:1 |
| forja_fila.py | tested_by | test_forja_fila.py | EXTRACTED | test_forja_fila.py:1 |
| forja_fontes_oficiais.py | tested_by | test_forja_fontes_oficiais.py | EXTRACTED | test_forja_fontes_oficiais.py:1 |
| forja_forma_artefatos.py | tested_by | test_forja_forma_artefatos.py | EXTRACTED | test_forja_forma_artefatos.py:1 |
| forja_gate_liveness.py | tested_by | test_forja_gate_liveness.py | EXTRACTED | test_forja_gate_liveness.py:1 |
| forja_f10_contract.py | tested_by | test_forja_gates_emitidos.py | EXTRACTED | test_forja_gates_emitidos.py:1 |
| forja_f8_contract.py | tested_by | test_forja_gates_emitidos.py | EXTRACTED | test_forja_gates_emitidos.py:1 |
| forja_gate_liveness.py | tested_by | test_forja_gates_emitidos.py | EXTRACTED | test_forja_gates_emitidos.py:1 |
| forja_citations.py | tested_by | test_forja_identidade_citacoes.py | EXTRACTED | test_forja_identidade_citacoes.py:1 |
| forja_editorial.py | tested_by | test_forja_identidade_modelo.py | EXTRACTED | test_forja_identidade_modelo.py:1 |
| forja_editorial_model.py | tested_by | test_forja_identidade_modelo.py | EXTRACTED | test_forja_identidade_modelo.py:1 |
| forja_headless.py | tested_by | test_forja_identidade_modelo.py | EXTRACTED | test_forja_identidade_modelo.py:1 |
| forja_exploracao_100.py | tested_by | test_forja_ingestao.py | EXTRACTED | test_forja_ingestao.py:1 |
| forja_ingestao.py | tested_by | test_forja_ingestao.py | EXTRACTED | test_forja_ingestao.py:1 |
| forja_metadata.py | tested_by | test_forja_injection.py | EXTRACTED | test_forja_injection.py:1 |
| forja_injection_scan.py | tested_by | test_forja_injection_gate.py | EXTRACTED | test_forja_injection_gate.py:1 |
| forja_lastro.py | tested_by | test_forja_lastro.py | EXTRACTED | test_forja_lastro.py:1 |
| forja_run.py | tested_by | test_forja_lastro.py | EXTRACTED | test_forja_lastro.py:1 |
| forja_visual_build.py | tested_by | test_forja_lastro.py | EXTRACTED | test_forja_lastro.py:1 |
| forja_phase_contracts.py | tested_by | test_forja_lastro_rota_producao.py | EXTRACTED | test_forja_lastro_rota_producao.py:1 |
| forja_run.py | tested_by | test_forja_lastro_rota_producao.py | EXTRACTED | test_forja_lastro_rota_producao.py:1 |
| forja_docx_layout.py | tested_by | test_forja_layout_antimoldagem.py | EXTRACTED | test_forja_layout_antimoldagem.py:1 |
| forja_docx_layout.py | tested_by | test_forja_layout_papeis.py | EXTRACTED | test_forja_layout_papeis.py:1 |
| forja_ledger_material.py | tested_by | test_forja_ledger_material.py | EXTRACTED | test_forja_ledger_material.py:1 |
| forja_legal_search.py | tested_by | test_forja_legal_search.py | EXTRACTED | test_forja_legal_search.py:1 |
| forja_memoria_auditabilidade.py | tested_by | test_forja_memoria_auditabilidade.py | EXTRACTED | test_forja_memoria_auditabilidade.py:1 |
| forja_metadata.py | tested_by | test_forja_metadata.py | EXTRACTED | test_forja_metadata.py:1 |
| forja_modelos.py | tested_by | test_forja_modelos.py | EXTRACTED | test_forja_modelos.py:1 |
| forja_mutation_semantic.py | tested_by | test_forja_mutation_semantic.py | EXTRACTED | test_forja_mutation_semantic.py:1 |
| forja_context.py | tested_by | test_forja_n3_context.py | EXTRACTED | test_forja_n3_context.py:1 |
| forja_n3_common.py | tested_by | test_forja_n3_context.py | EXTRACTED | test_forja_n3_context.py:1 |
| forja_fidelity.py | tested_by | test_forja_n3_fidelity.py | EXTRACTED | test_forja_n3_fidelity.py:1 |
| forja_headless.py | tested_by | test_forja_n3_headless.py | EXTRACTED | test_forja_n3_headless.py:1 |
| forja_management_bridge.py | tested_by | test_forja_n3_management.py | EXTRACTED | test_forja_n3_management.py:1 |
| forja_n3_common.py | tested_by | test_forja_n3_management.py | EXTRACTED | test_forja_n3_management.py:1 |
| forja_state_machine.py | tested_by | test_forja_n3_management.py | EXTRACTED | test_forja_n3_management.py:1 |
| forja_n3_common.py | tested_by | test_forja_n3_metrics.py | EXTRACTED | test_forja_n3_metrics.py:1 |
| forja_run_metrics.py | tested_by | test_forja_n3_metrics.py | EXTRACTED | test_forja_n3_metrics.py:1 |
| forja_state_machine.py | tested_by | test_forja_n3_metrics.py | EXTRACTED | test_forja_n3_metrics.py:1 |
| forja_close_cycle.py | tested_by | test_forja_n3_package.py | EXTRACTED | test_forja_n3_package.py:1 |
| forja_f10_contract.py | tested_by | test_forja_n3_package.py | EXTRACTED | test_forja_n3_package.py:1 |
| forja_fidelity.py | tested_by | test_forja_n3_package.py | EXTRACTED | test_forja_n3_package.py:1 |
| forja_human_review.py | tested_by | test_forja_n3_package.py | EXTRACTED | test_forja_n3_package.py:1 |
| forja_n3_common.py | tested_by | test_forja_n3_package.py | EXTRACTED | test_forja_n3_package.py:1 |
| forja_package.py | tested_by | test_forja_n3_package.py | EXTRACTED | test_forja_n3_package.py:1 |
| forja_state_machine.py | tested_by | test_forja_n3_package.py | EXTRACTED | test_forja_n3_package.py:1 |
| forja_visual_qa.py | tested_by | test_forja_n3_package.py | EXTRACTED | test_forja_n3_package.py:1 |
| forja_visual_review.py | tested_by | test_forja_n3_package.py | EXTRACTED | test_forja_n3_package.py:1 |
| forja_n3_common.py | tested_by | test_forja_n3_runner.py | EXTRACTED | test_forja_n3_runner.py:1 |
| forja_phase_contracts.py | tested_by | test_forja_n3_runner.py | EXTRACTED | test_forja_n3_runner.py:1 |
| forja_run.py | tested_by | test_forja_n3_runner.py | EXTRACTED | test_forja_n3_runner.py:1 |
| forja_state_machine.py | tested_by | test_forja_n3_runner.py | EXTRACTED | test_forja_n3_runner.py:1 |
| forja_n3_common.py | tested_by | test_forja_n3_state.py | EXTRACTED | test_forja_n3_state.py:1 |
| forja_state_machine.py | tested_by | test_forja_n3_state.py | EXTRACTED | test_forja_n3_state.py:1 |
| forja_n3_common.py | tested_by | test_forja_n3_visual.py | EXTRACTED | test_forja_n3_visual.py:1 |
| forja_visual.py | tested_by | test_forja_n3_visual.py | EXTRACTED | test_forja_n3_visual.py:1 |
| forja_visual_qa.py | tested_by | test_forja_n3_visual.py | EXTRACTED | test_forja_n3_visual.py:1 |
| forja_visual_review.py | tested_by | test_forja_n3_visual.py | EXTRACTED | test_forja_n3_visual.py:1 |
| forja_case_tests.py | tested_by | test_forja_n4.py | EXTRACTED | test_forja_n4.py:1 |
| forja_consistency.py | tested_by | test_forja_n4.py | EXTRACTED | test_forja_n4.py:1 |
| forja_delivery_integrity.py | tested_by | test_forja_n4.py | EXTRACTED | test_forja_n4.py:1 |
| forja_learning.py | tested_by | test_forja_n4.py | EXTRACTED | test_forja_n4.py:1 |
| forja_metacognition.py | tested_by | test_forja_n4.py | EXTRACTED | test_forja_n4.py:1 |
| forja_n4_common.py | tested_by | test_forja_n4.py | EXTRACTED | test_forja_n4.py:1 |
| forja_n4_invalidation.py | tested_by | test_forja_n4.py | EXTRACTED | test_forja_n4.py:1 |
| forja_n4_validate.py | tested_by | test_forja_n4.py | EXTRACTED | test_forja_n4.py:1 |
| forja_reasoning.py | tested_by | test_forja_n4.py | EXTRACTED | test_forja_n4.py:1 |
| forja_render_docx.py | tested_by | test_forja_n4.py | EXTRACTED | test_forja_n4.py:1 |
| forja_science.py | tested_by | test_forja_n4.py | EXTRACTED | test_forja_n4.py:1 |
| forja_delivery.py | tested_by | test_forja_ordem_parecer.py | EXTRACTED | test_forja_ordem_parecer.py:1 |
| forja_p0.py | tested_by | test_forja_p0.py | EXTRACTED | test_forja_p0.py:1 |
| forja_paragrafos.py | tested_by | test_forja_paragrafos.py | EXTRACTED | test_forja_paragrafos.py:1 |
| forja_citations.py | tested_by | test_forja_politica_citacoes.py | EXTRACTED | test_forja_politica_citacoes.py:1 |
| forja_verificador.py | tested_by | test_forja_porta_unica.py | EXTRACTED | test_forja_porta_unica.py:1 |
| forja_document_compare.py | tested_by | test_forja_post_protocol.py | EXTRACTED | test_forja_post_protocol.py:1 |
| forja_learning.py | tested_by | test_forja_post_protocol.py | EXTRACTED | test_forja_post_protocol.py:1 |
| forja_learning_registry.py | tested_by | test_forja_post_protocol.py | EXTRACTED | test_forja_post_protocol.py:1 |
| forja_n3_common.py | tested_by | test_forja_post_protocol.py | EXTRACTED | test_forja_post_protocol.py:1 |
| forja_n4_common.py | tested_by | test_forja_post_protocol.py | EXTRACTED | test_forja_post_protocol.py:1 |
| forja_post_protocol.py | tested_by | test_forja_post_protocol.py | EXTRACTED | test_forja_post_protocol.py:1 |
| forja_post_protocol_contracts.py | tested_by | test_forja_post_protocol.py | EXTRACTED | test_forja_post_protocol.py:1 |
| forja_state_machine.py | tested_by | test_forja_post_protocol.py | EXTRACTED | test_forja_post_protocol.py:1 |
| forja_produto.py | tested_by | test_forja_produto.py | EXTRACTED | test_forja_produto.py:1 |
| forja_pso_pet.py | tested_by | test_forja_pso_pet.py | EXTRACTED | test_forja_pso_pet.py:1 |
| forja_qa_paginas.py | tested_by | test_forja_qa_paginas.py | EXTRACTED | test_forja_qa_paginas.py:1 |
| forja_recomputo_censo.py | tested_by | test_forja_recomputo_censo.py | EXTRACTED | test_forja_recomputo_censo.py:1 |
| forja_n3_common.py | tested_by | test_forja_reconcile.py | EXTRACTED | test_forja_reconcile.py:1 |
| forja_reconcile.py | tested_by | test_forja_reconcile.py | EXTRACTED | test_forja_reconcile.py:1 |
| validate_forja_n3.py | tested_by | test_forja_reconcile.py | EXTRACTED | test_forja_reconcile.py:1 |
| forja_red_team.py | tested_by | test_forja_red_team.py | EXTRACTED | test_forja_red_team.py:1 |
| forja_redacao.py | tested_by | test_forja_redacao.py | EXTRACTED | test_forja_redacao.py:1 |
| forja_regimento_gate.py | tested_by | test_forja_regimento_gate.py | EXTRACTED | test_forja_regimento_gate.py:1 |
| forja_regimentos.py | tested_by | test_forja_regimentos.py | EXTRACTED | test_forja_regimentos.py:1 |
| forja_delivery.py | tested_by | test_forja_regua.py | EXTRACTED | test_forja_regua.py:1 |
| forja_metricas_f7.py | tested_by | test_forja_regua.py | EXTRACTED | test_forja_regua.py:1 |
| forja_official_sources.py | tested_by | test_forja_regua.py | EXTRACTED | test_forja_regua.py:1 |
| forja_regua.py | tested_by | test_forja_regua.py | EXTRACTED | test_forja_regua.py:1 |
| forja_entrega.py | tested_by | test_forja_rota_forma.py | EXTRACTED | test_forja_rota_forma.py:1 |
| forja_fontes_oficiais.py | tested_by | test_forja_rota_forma.py | EXTRACTED | test_forja_rota_forma.py:1 |
| forja_produto.py | tested_by | test_forja_rota_forma.py | EXTRACTED | test_forja_rota_forma.py:1 |
| forja_regimento_gate.py | tested_by | test_forja_rota_forma.py | EXTRACTED | test_forja_rota_forma.py:1 |
| forja_run.py | tested_by | test_forja_rota_forma.py | EXTRACTED | test_forja_rota_forma.py:1 |
| forja_n3_common.py | tested_by | test_forja_run.py | EXTRACTED | test_forja_run.py:1 |
| forja_run.py | tested_by | test_forja_run.py | EXTRACTED | test_forja_run.py:1 |
| forja_state_machine.py | tested_by | test_forja_run.py | EXTRACTED | test_forja_run.py:1 |
| forja_svg_docx.py | tested_by | test_forja_svg_docx.py | EXTRACTED | test_forja_svg_docx.py:1 |
| forja_visual_qa_structural.py | tested_by | test_forja_svg_docx.py | EXTRACTED | test_forja_svg_docx.py:1 |
| forja_varredura_tipografica.py | tested_by | test_forja_varredura_tipografica.py | EXTRACTED | test_forja_varredura_tipografica.py:1 |
| forja_verificador.py | tested_by | test_forja_verificador.py | EXTRACTED | test_forja_verificador.py:1 |
| forja_visual_build.py | tested_by | test_forja_visual_build_peca_longa.py | EXTRACTED | test_forja_visual_build_peca_longa.py:1 |
| forja_citations.py | tested_by | test_licao41.py | EXTRACTED | test_licao41.py:1 |
| forja_metricas_f7.py | tested_by | test_licao41.py | EXTRACTED | test_licao41.py:1 |
| forja_official_sources.py | tested_by | test_licao41.py | EXTRACTED | test_licao41.py:1 |
| forja_render_docx.py | tested_by | test_licao41.py | EXTRACTED | test_licao41.py:1 |
| forja_citations.py | tested_by | test_real_telemetria_licao41.py | EXTRACTED | test_real_telemetria_licao41.py:1 |
| forja_metricas_f7.py | tested_by | test_real_telemetria_licao41.py | EXTRACTED | test_real_telemetria_licao41.py:1 |
| forja_render_docx.py | tested_by | test_real_telemetria_licao41.py | EXTRACTED | test_real_telemetria_licao41.py:1 |


## 8. Consumidores de teste

Esta matriz mostra quais módulos de teste importam contratos locais. O conteúdo das fixtures não foi copiado.

| Teste | Módulos locais importados | Casos de teste | Amostra de entradas |
| --- | --- | --- | --- |
| test_f7_campos.py | forja_metricas_f7 | 2 | test_f7_campos_sintetico:8, test_f7_campos_real:37 |
| test_forja_adocao_rota.py | forja_adocao_rota | 0 | — |
| test_forja_adversarial_audit.py | forja_adversarial_audit, forja_n3_common | 12 | test_initial_inventory_is_blocked_until_verified:62, test_not_located_requires_two_official_channels:69, test_complete_cautious_audit_passes:76, test_detected_citation_cannot_be_removed_from_inventory:80, test_confirmed_citation_requires_all_verification_dimensions:87, test_bad_faith_language_requires_human_authorization:103, test_decisive_point_requires_traceable_finding:120, test_not_applicable_still_requires_reason:138 |
| test_forja_adversarial_gate.py | forja_adversarial_gate, forja_replay | 0 | — |
| test_forja_alertas.py | forja_alertas | 9 | test_p0_novo_notifica_painel:44, test_p0_repetido_em_6h_deduplica:54, test_p0_apos_janela_notifica_de_novo:60, test_gates_distintos_nao_deduplicam_entre_si:71, test_resolucao_notifica_uma_vez:77, test_painel_indisponivel_cai_no_fallback_sem_excecao:86, test_drenagem_reentrega_quando_painel_volta:95, test_caso_sem_state_nao_explode:106 |
| test_forja_anti_cheat.py | forja_citations, forja_docx_layout, forja_human_review, forja_metricas_f7, forja_n3_common, forja_official_sources, forja_package, forja_visual_qa, forja_visual_review | 13 | test_state_court_cnj_adi_cannot_masquerade_as_stf_authority:109, test_layout_mutations_are_all_killed:123, test_wide_folio_collision_is_blocked_and_normalized:143, test_folio_margin_collision_and_unreadable_margin_are_blocked:166, test_visual_normalizer_cannot_silently_change_legal_text:187, test_visual_attestation_mutations_are_all_killed:204, test_strict_visual_release_requires_signed_human_receipt:264, test_fake_jurisprudence_and_unregistered_sidecar_do_not_pass:373 |
| test_forja_anti_hallucination_v2.py | forja_authorities, forja_claim_binding, forja_delivery, forja_editorial_fidelity, forja_n3_common, forja_official_sources, forja_package | 7 | test_inventory_covers_less_common_classes_and_norms:22, test_ambiguous_high_court_reference_is_explicit:34, test_legacy_f7_recomputes_fake_hc_and_law:38, test_generic_claim_cannot_cover_false_final_proposition:53, test_editorial_semantic_inversion_is_blocked:116, test_protocolable_content_cannot_be_downgraded_and_old_package_is_stale:145, test_binding_tool_covers_inventory_and_resets_signature:161 |
| test_forja_ar_architecture.py | forja_ar_architecture, forja_n3_common, forja_post_protocol | 6 | test_feature_off_is_real_rollback_switch:23, test_cycle_counter_detects_relevant_scc:27, test_missing_manifest_contract_fails_closed:31, test_feature_off_blocks_every_mutating_entry_point:34, test_git_leak_detection_handles_accented_paths:60, test_candidate_is_separate_descriptive_lineage:72 |
| test_forja_architecture.py | forja_f8_contract, forja_package | 2 | test_package_and_n4_do_not_form_an_import_cycle:25, test_public_validate_f8_is_the_neutral_contract:34 |
| test_forja_artefatos.py | forja_artefatos | 0 | — |
| test_forja_assinatura_antimoldagem.py | forja_assinatura_visual | 0 | — |
| test_forja_assinatura_lite.py | forja_exploracao_100, forja_legal_search, forja_n3_common, forja_n4_common, forja_n4_invalidation, forja_n4_validate, forja_official_sources, forja_precedente, forja_reasoning | 120 | test_namespace_declarado_na_config_nasce_off:112, test_namespace_ausente_equivale_a_off:120, test_modo_desconhecido_falha:125, test_pilot_blocking_so_bloqueia_caso_nomeado:131, test_off_nao_exige_os_artefatos_novos:141, test_modo_ligado_exige_os_dois:155, test_modo_do_n4_nao_foi_alterado:166, test_catalogo_e_specs_coincidem:174 |
| test_forja_assinatura_visual.py | forja_assinatura_visual | 5 | test_faixa_por_extensao:42, test_referencia_aprovada_e_conforme:48, test_mutacoes_sao_detectadas:68, test_negrito_universal_reprova:96, test_docx_fora_do_template_reprova:115 |
| test_forja_autoresearch.py | forja_ar_blind, forja_ar_canarios, forja_ar_ciclo, forja_ar_corpus, forja_ar_evolucao, forja_ar_indicadores, forja_ar_runpair | 32 | test_split_estavel_e_agrupado_por_linhagem:71, test_scan_estado_real_encontra_vinte:78, test_painel_discrimina_placeholder_e_null_motivado:84, test_cache_round_trip:91, test_runpair_recusa_paridade_violada:126, test_consolidacao_por_hash:170, test_regra_posicional_correta:180, test_mapping_adulterado_e_detectado:188 |
| test_forja_axi.py | forja_axi | 7 | test_toon_tabular_and_quoting:80, test_home_is_live_aggregate_without_case_names:94, test_cases_default_schema_and_definitive_empty_state:105, test_case_truncates_blocker_and_full_is_escape_hatch:116, test_queue_uses_minimal_default_schema:128, test_unknown_flag_is_structured_stdout_and_exit_2:135, test_case_id_cannot_escape_state_root:149 |
| test_forja_baseline_aprovado.py | forja_baseline_aprovado | 0 | — |
| test_forja_bench_modelos.py | forja_bench_modelos | 6 | test_negacao_correta_nao_vira_sinal_de_invencao:17, test_negacao_correta_nao_salva_dispositivo_inventado:25, test_sumula_correta_com_cancelamento_inventado_reprova:35, test_artigo_correto_com_capitulo_errado_reprova:42, test_resposta_exata_sem_complemento_passa:50, test_reavalia_sem_nova_chamada:57 |
| test_forja_canario_catraca.py | forja_canario_catraca | 0 | — |
| test_forja_canario_mutacao.py | forja_canario_mutacao | 0 | — |
| test_forja_citacoes.py | forja_citations | 0 | — |
| test_forja_conselho.py | forja_conselho | 0 | — |
| test_forja_conselho_1107.py | forja_delivery | 0 | — |
| test_forja_contexto.py | forja_contexto | 0 | — |
| test_forja_editorial.py | forja_editorial, forja_editorial_fidelity, forja_editorial_model, forja_n3_common, forja_phase_contracts | 22 | test_rewrite_preserving_invariants_passes:89, test_changed_number_is_blocked_even_if_model_claims_success:96, test_changed_orders_are_blocked:104, test_wrong_model_or_billing_is_blocked:112, test_removed_argumentative_chapter_is_blocked:122, test_prompt_exige_selecao_edge_e_recibo_de_gosto:143, test_mocked_claude_code_writes_hash_bound_artifacts:149, test_fable_does_not_run_while_f7_has_p0:188 |
| test_forja_entrega.py | forja_entrega | 0 | — |
| test_forja_estilo_humano.py | forja_estilo_humano, forja_n3_common, forja_package, forja_render_docx, forja_run | 17 | test_formulas_contrastivas:22, test_metadiscurso_cliche_e_dogmatismo:36, test_lugar_comum_juridico_sem_fonte:40, test_ritmo_robotico:50, test_conclusao_tautologica:57, test_pacote_recomputa_p0_forjado:69, test_executor_f6_recomputa_gate:85, test_render_persiste_relatorio_e_nao_gera_word_com_p0:96 |
| test_forja_exploracao_100.py | forja_exploracao_100, forja_n3_common, forja_n4_common, forja_n4_validate, forja_phase_contracts, forja_reconcile, forja_run | 12 | test_scaffold_has_exactly_ten_lenses_and_one_hundred_questions:66, test_complete_exploration_passes:76, test_ninety_nine_questions_fail:79, test_repeated_question_fails:88, test_answered_fact_without_support_fails:93, test_blocked_material_question_blocks_drafting:99, test_missing_downstream_handoff_fails:112, test_contract_makes_exploration_output_and_downstream_input_mandatory:117 |
| test_forja_f2_check.py | forja_f2_check | 11 | test_cnj_federal_trf1:15, test_cnj_federal_trf4:19, test_cnj_estadual_tjto:23, test_cnj_estadual_tjrj:27, test_classe_aresp_infere_stj:31, test_tribunal_declarado_divergente_vira_p1:34, test_perfil_pso_invalido_vira_p1:40, test_produto_vazio_vira_p1:45 |
| test_forja_f8_gates_contrato.py | forja_f8_contract | 0 | — |
| test_forja_f8_pecas_reais.py | forja_docx_layout, forja_visual_qa_structural | 0 | — |
| test_forja_f8_static.py | forja_f8_contract, forja_n3_common | 2 | test_rota_estatica_nao_chama_inspect_pdf:43, test_rota_estatica_reprova_sinal_de_render:56 |
| test_forja_fila.py | forja_fila | 0 | — |
| test_forja_fontes_oficiais.py | forja_fontes_oficiais | 0 | — |
| test_forja_forma_artefatos.py | forja_forma_artefatos | 0 | — |
| test_forja_gate_liveness.py | forja_gate_liveness | 0 | — |
| test_forja_gates_emitidos.py | forja_f10_contract, forja_f8_contract, forja_gate_liveness | 0 | — |
| test_forja_identidade_citacoes.py | forja_citations | 0 | — |
| test_forja_identidade_modelo.py | forja_editorial, forja_editorial_model, forja_headless | 12 | test_cli_model_devolve_id_canonico:41, test_apelido_continua_existindo_mas_nao_vai_ao_cli:49, test_headless_pede_modelo_por_id_canonico:56, test_nenhum_modulo_de_producao_passa_apelido_ao_cli:61, test_headless_falha_alto_quando_o_envelope_diverge:76, test_headless_aceita_o_modelo_pedido:84, test_headless_nao_afirma_nada_sem_telemetria:88, test_stream_recompoe_todos_os_turnos_na_ordem:93 |
| test_forja_ingestao.py | forja_exploracao_100, forja_ingestao | 0 | — |
| test_forja_injection.py | forja_metadata | 2 | testar_pdf_envenenado:105, testar_pdfs_reais:155 |
| test_forja_injection_gate.py | forja_injection_scan | 0 | — |
| test_forja_lastro.py | forja_lastro, forja_run, forja_visual_build | 0 | — |
| test_forja_lastro_rota_producao.py | forja_phase_contracts, forja_run | 0 | — |
| test_forja_layout_antimoldagem.py | forja_docx_layout | 0 | — |
| test_forja_layout_papeis.py | forja_docx_layout | 0 | — |
| test_forja_ledger_material.py | forja_ledger_material | 7 | test_citacao_sem_fonte_vira_p1_nominada:41, test_proposicao_sem_fonte_vira_p1:49, test_tabela_ausente_gera_template_e_pendencia:56, test_citacao_casada_com_source_ledger_e_silencio:67, test_proposicao_preenchida_integra_sem_pendencia:82, test_template_nao_e_parseado_como_proposicao:92, test_estado_ausente_nao_explode:98 |
| test_forja_legal_search.py | forja_legal_search | 3 | test_capabilities_and_health_use_real_gateway:65, test_search_writes_f5_evidence_and_telemetry:77, test_mutation_and_unknown_actions_fail_closed:95 |
| test_forja_memoria_auditabilidade.py | forja_memoria_auditabilidade | 4 | test_bundle_tem_memoria_sanitizada_e_no_render:61, test_tamper_no_manifesto_reprova:74, test_inventario_distingue_ledger_canonico_de_snapshot_historico:84, test_fases_usam_identificadores_canonicos_e_aliases_historicos:110 |
| test_forja_metadata.py | forja_metadata | 1 | test_final_sanitization_preserves_content_and_normalizes_authors:15 |
| test_forja_modelos.py | forja_modelos | 20 | test_toda_familia_tem_revisor_de_outra_familia:26, test_kimi_k2_esta_vedado_por_decisao_do_titular:35, test_novo_sufixo_kimi_k2_tambem_e_vedado:42, test_modelo_fora_do_registro_nao_e_chamado:53, test_modelo_local_nao_sai_por_http:57, test_cada_fase_do_registro_tem_pelo_menos_um_modelo:63, test_kimi_k3_foi_retirado_de_todo_o_registro:69, test_resposta_vazia_levanta_em_vez_de_virar_string_vazia:82 |
| test_forja_mutation_semantic.py | forja_mutation_semantic | 10 | test_todas_familias_geram_mutantes_no_texto_sintetico:47, test_inversao_de_tese_e_morta_pela_suite:51, test_troca_sumula_tribunal_e_morta_pelo_verificador:56, test_mutacao_de_valor_e_morta:60, test_gate_de_sanidade_suite_quebrada_nunca_da_score_falso:64, test_familias_fracas_sao_nominadas:78, test_controles_benignos_nao_sao_mortos:88, test_texto_sem_padroes_nao_explode:93 |
| test_forja_n3_context.py | forja_context, forja_n3_common | 5 | test_markdown_parser_preserves_h4_and_blockquote:17, test_coverage_detects_missing_page:22, test_unverified_fact_cannot_allow_final_use:29, test_complete_context_is_approved:36, test_missing_ledgers_write_blocking_validation_artifact:52 |
| test_forja_n3_fidelity.py | forja_fidelity | 3 | test_exact_semantic_content_passes:32, test_lost_negation_and_number_are_blocked:43, test_reconstructed_structural_paragraph_number_does_not_break_fidelity:57 |
| test_forja_n3_headless.py | forja_headless | 3 | test_f2_prompt_always_carries_exploration_contract:25, test_n3_writes_only_inside_attempt:32, test_legacy_mode_preserves_existing_contract:56 |
| test_forja_n3_management.py | forja_management_bridge, forja_n3_common, forja_state_machine | 12 | test_sidecar_does_not_modify_demands_and_is_idempotent:43, test_replay_copy_is_ignored_by_automatic_bridge:62, test_two_cases_are_not_lost_under_concurrency:66, test_batch_reconcile_skips_cases_outside_office_management:83, test_dashboard_join_marks_unlinked_demand_not_run:99, test_legacy_reconcile_is_read_only_and_never_overwrites_n3:113, test_legacy_reconcile_repairs_noncanonical_n3_sidecar_entry:148, test_manual_audit_overlay_replaces_stale_legacy_delivery_without_touching_state:179 |
| test_forja_n3_metrics.py | forja_n3_common, forja_run_metrics, forja_state_machine | 1 | test_metrics_follow_events_and_are_materialized:11 |
| test_forja_n3_package.py | forja_close_cycle, forja_f10_contract, forja_fidelity, forja_human_review, forja_n3_common, forja_package, forja_state_machine, forja_visual_qa, forja_visual_review | 12 | test_full_close_cycle_is_hash_bound:229, test_f10_recomputes_hash_and_sync_instead_of_accepting_declaration:272, test_draft_receipt_requires_exact_artifact_ids:287, test_draft_rejects_tampered_package_pointer:300, test_package_blocks_email_with_ai_writing_vices:320, test_draft_requires_hash_of_approved_email_body:347, test_changed_email_after_package_cannot_be_registered:362, test_revision_conflict_does_not_replace_package_pointer:379 |
| test_forja_n3_runner.py | forja_n3_common, forja_phase_contracts, forja_run, forja_state_machine | 3 | test_contracts_are_complete:76, test_attempt_promotes_only_validated_outputs:79, test_failed_gate_does_not_promote:91 |
| test_forja_n3_server_routes.py | — | 4 | test_artifact_with_spaces_and_accents_resolves_by_id_and_hash:16, test_tampered_artifact_is_rejected:43, test_manual_audit_artifact_resolves_without_package:54, test_n4_artifact_resolves_only_from_catalog_and_current_hash:81 |
| test_forja_n3_state.py | forja_n3_common, forja_state_machine | 7 | test_progression_and_recovery:39, test_regression_requires_reopen:50, test_idempotency:66, test_concurrent_revision_conflict:74, test_partial_event_is_ignored:94, test_returned_state_includes_synchronous_management_ack:99, test_legacy_highest_phase_blocks_silent_regression:115 |
| test_forja_n3_visual.py | forja_n3_common, forja_visual, forja_visual_qa, forja_visual_review | 10 | test_valid_svg_passes:19, test_later_opaque_shape_covering_text_fails:31, test_production_diagrams_are_checked_after_correction:43, test_markdown_and_duplicate_caption_leaks_fail:75, test_pdf_reviewer_must_be_independent:82, test_visual_parser_handles_h4_blockquote_and_weighted_table:95, test_visual_qa_runs_semantic_fidelity_gate:120, test_composer_accepts_only_declared_visual_markers:193 |
| test_forja_n4.py | forja_case_tests, forja_consistency, forja_delivery_integrity, forja_learning, forja_metacognition, forja_n4_common, forja_n4_invalidation, forja_n4_validate, forja_reasoning, forja_render_docx, forja_science | 63 | test_schema_catalog_covers_every_artifact_and_resolves:44, test_render_classifies_internal_diagnostic_without_weakening_petitions:52, test_envelope_hash_and_independent_review:56, test_required_cannot_be_not_applicable:62, test_material_question_requires_answer_or_block:66, test_answered_fact_requires_support:70, test_estado_fora_do_contrato_e_recusado:74, test_estados_canonicos_passam:85 |
| test_forja_ordem_parecer.py | forja_delivery | 6 | test_parecer_depois_do_f6_reprova_caso_novo:32, test_parecer_inexistente_com_f6_iniciado_reprova:44, test_caso_legado_nao_retroage:53, test_sem_f6_no_historico_aprova:62, test_parecer_antes_do_f6_aprova:66, test_timestamp_invalido_no_historico_nao_explode:75 |
| test_forja_p0.py | forja_p0 | 0 | — |
| test_forja_paragrafos.py | forja_paragrafos | 0 | — |
| test_forja_politica_citacoes.py | forja_citations | 0 | — |
| test_forja_porta_unica.py | forja_verificador | 0 | — |
| test_forja_post_protocol.py | forja_document_compare, forja_learning, forja_learning_registry, forja_n3_common, forja_n4_common, forja_post_protocol, forja_post_protocol_contracts, forja_state_machine | 36 | test_catalog_uses_exact_new_schema_names:62, test_layer_to_cause_is_total_and_default_deny:76, test_tracked_comparison_rejects_raw_legal_text:85, test_idempotency_keys_separate_content_from_evidence:94, test_post_protocol_does_not_reopen_fulfilled_delivery:113, test_concurrent_post_protocol_revision_conflict:131, test_panel_projection_rejects_free_prose:156, test_reason_codes_are_not_erased_by_later_success_events:173 |
| test_forja_produto.py | forja_produto | 0 | — |
| test_forja_pso_pet.py | forja_pso_pet | 11 | test_valid_fixture_has_no_findings_and_no_hidden_composite:23, test_output_cannot_prove_input_state:31, test_direct_and_ultimate_outcome_must_be_separate:36, test_full_profile_requires_distinct_viable_alternative:41, test_duplicate_labelled_option_does_not_count:46, test_material_requirement_needs_validation_trace:55, test_context_dump_is_detected_without_becoming_silent:60, test_prospective_timing_is_interpreted:67 |
| test_forja_qa_paginas.py | forja_qa_paginas | 8 | test_densidade_anomala_detectada:45, test_pagina_em_branco_no_meio:56, test_conteudo_cortado_na_borda_inferior:63, test_documento_normal_em_silencio:75, test_rodape_institucional_na_pagina_1_e_isento:81, test_ultima_pagina_curta_nao_e_pagina_em_branco:90, test_pasta_real_aprovada_continua_aprovada:97, test_pasta_vazia_nao_explode:105 |
| test_forja_recomputo_censo.py | forja_recomputo_censo | 0 | — |
| test_forja_reconcile.py | forja_n3_common, forja_reconcile, validate_forja_n3 | 2 | test_gate_que_deixa_de_ser_atual_e_resolvido_sem_sumir:37, test_runner_referencia_o_script_f7_no_destino_atual:91 |
| test_forja_red_team.py | forja_red_team | 0 | — |
| test_forja_redacao.py | forja_redacao | 0 | — |
| test_forja_regimento_gate.py | forja_regimento_gate | 0 | — |
| test_forja_regimentos.py | forja_regimentos | 0 | — |
| test_forja_regua.py | forja_delivery, forja_metricas_f7, forja_official_sources, forja_regua | 0 | — |
| test_forja_rota_forma.py | forja_entrega, forja_fontes_oficiais, forja_produto, forja_regimento_gate, forja_run | 0 | — |
| test_forja_run.py | forja_n3_common, forja_run, forja_state_machine | 13 | test_fase_inexistente_falha_claro:93, test_entrada_obrigatoria_faltante:97, test_resultado_reprovado_nao_promove:106, test_autorrevisao_reprovada:117, test_gate_faltando_reprova:131, test_excesso_de_tentativas:145, test_fluxo_feliz_f0_promove_e_avanca:166, test_replay_idempotente:178 |
| test_forja_svg_docx.py | forja_svg_docx, forja_visual_qa_structural | 4 | test_embute_svg_sem_pdf_png_ou_marker:32, test_qa_registra_explicitamente_ausencia_de_render:44, test_marcador_multiplo_bloqueia:54, test_svg_invalido_bloqueia_antes_de_alterar_docx:60 |
| test_forja_varredura_tipografica.py | forja_varredura_tipografica | 0 | — |
| test_forja_verificador.py | forja_verificador | 0 | — |
| test_forja_visual_build_peca_longa.py | forja_visual_build | 0 | — |
| test_gmail_management_matching.py | — | 3 | test_cross_case_delivery_is_removed_from_whatsapp_demand:23, test_matching_email_thread_is_preserved:47, test_delivery_audit_does_not_match_generic_whatsapp_words:67 |
| test_licao41.py | forja_citations, forja_metricas_f7, forja_official_sources, forja_render_docx | 0 | — |
| test_medina_svg_colisao.py | — | 10 | test_caso_real_reprovado:58, test_correcao_do_caso_real_aprova:65, test_tspan_em_fluxo_nao_e_colisao:73, test_important_no_style_nao_e_cor_invalida:76, test_texto_sobre_texto:82, test_forma_transparente_nao_oculta:88, test_ordem_importa:97, test_paleta_aprovada_nao_reprova_por_contraste:105 |
| test_real_telemetria_licao41.py | forja_citations, forja_metricas_f7, forja_render_docx | 0 | — |
| test_word_visual_pipeline_retry.py | — | 2 | test_transient_failure_retries_and_promotes_atomically:14, test_permanent_failure_preserves_previous_pdf:37 |


## 9. Símbolos internos relevantes

Símbolos internos são registrados porque frequentemente implementam handlers, gates e adaptadores chamados por uma interface pública.

| Módulo | Tipo | Símbolo | Assinatura | Linha |
| --- | --- | --- | --- | --- |
| forja_adocao_rota.py | function | _sha_arquivo | `(caminho)` | 59 |
| forja_adocao_rota.py | function | _entregas | `(limite)` | 70 |
| forja_adocao_rota.py | function | _caminho_alvo | `(valor, marcador)` | 122 |
| forja_adocao_rota.py | function | _alvo_do_marcador | `(dados)` | 145 |
| forja_adocao_rota.py | function | _marca_aplica | `(marcador, docx)` | 155 |
| forja_adocao_rota.py | function | _marcas_do_docx | `(caminho)` | 177 |
| forja_adversarial_audit.py | function | _official_url | `(value: object) -> bool` | 108 |
| forja_adversarial_audit.py | function | _citation_id | `(index: int) -> str` | 116 |
| forja_adversarial_audit.py | function | _validate_source | `(payload: dict, source_path: Path \| None, p0: list[str]) -> None` | 184 |
| forja_adversarial_audit.py | function | _validate_inventory_completeness | `(payload: dict, source_path: Path \| None, p0: list[str]) -> None` | 194 |
| forja_adversarial_gate.py | function | _motivo | `(dados: dict) -> str \| None` | 42 |
| forja_adversarial_gate.py | function | _hashes_do_arquivo | `(caminho) -> set` | 50 |
| forja_alertas.py | function | _now | `()` | 34 |
| forja_alertas.py | function | _now_iso | `()` | 38 |
| forja_alertas.py | function | _registro_enviados | `(case_dir: Path) -> Path` | 42 |
| forja_alertas.py | function | _pendentes | `(case_dir: Path) -> Path` | 46 |
| forja_alertas.py | function | _ler_json | `(path: Path, fallback)` | 50 |
| forja_alertas.py | function | _dedup_ok | `(case_dir: Path, chave: str) -> bool` | 57 |
| forja_alertas.py | function | _marcar_enviado | `(case_dir: Path, chave: str)` | 69 |
| forja_alertas.py | function | _log_global | `(evento: dict)` | 78 |
| forja_alertas.py | function | _demand_id_do_caso | `(case_dir: Path) -> str \| None` | 84 |
| forja_alertas.py | function | _comentar_no_painel | `(demand_id: str, texto: str) -> bool` | 93 |
| forja_alertas.py | function | _emitir | `(case_dir: Path, evento: dict, chave_dedup: str) -> dict` | 136 |
| forja_ar_architecture.py | function | _semantic | `(candidate: dict) -> dict` | 85 |
| forja_ar_architecture.py | function | _write_candidate | `(path: Path, candidate: dict) -> None` | 89 |
| forja_ar_architecture.py | function | _run_pytest | `(targets: list[str], *, cwd: Path = <default>, timeout: int = <default>) -> dict` | 210 |
| forja_ar_architecture.py | function | _relevant_import_graph | `() -> dict[str, set[str]]` | 257 |
| forja_ar_architecture.py | function | _cycle_count | `(graph: dict[str, set[str]]) -> int` | 278 |
| forja_ar_architecture.py | function | _tracked_vault_leaks | `(repo_root: Path \| None = <default>) -> list[str]` | 315 |
| forja_ar_architecture.py | function | _vault_ignore_failures | `(repo_root: Path) -> list[str]` | 333 |
| forja_ar_architecture.py | function | _rollback_rehearsal | `(harness: Path) -> dict` | 353 |
| forja_ar_architecture.py | function | _overlay_candidate | `(worktree_harness: Path, snapshot: list[dict]) -> None` | 405 |
| forja_ar_blind.py | function | _sha_bytes | `(data: bytes) -> str` | 49 |
| forja_ar_blind.py | function | _sha_file | `(path: Path) -> str` | 53 |
| forja_ar_blind.py | function | _canonical | `(value) -> bytes` | 57 |
| forja_ar_blind.py | function | _mapping_path | `(pair_id: str) -> Path` | 61 |
| forja_ar_blind.py | function | _verify_mapping | `(mapping: dict, key: bytes) -> bool` | 125 |
| forja_ar_blind.py | function | _mapping_leaked | `(workspace: Path, mapping_sha: str, external_path: Path) -> bool` | 132 |
| forja_ar_blind.py | function | _cohen_kappa | `(votes_a: list[str], votes_b: list[str]) -> float \| None` | 147 |
| forja_ar_canarios.py | function | _sha | `(path: Path) -> str` | 20 |
| forja_ar_canarios.py | function | _load | `(path: Path) -> dict` | 24 |
| forja_ar_canarios.py | function | _adverse | `(indicator: str, base: dict, changed: dict) -> bool` | 28 |
| forja_ar_ciclo.py | function | _canonical | `(value) -> bytes` | 34 |
| forja_ar_ciclo.py | function | _sha_bytes | `(value: bytes) -> str` | 38 |
| forja_ar_ciclo.py | function | _sha_file | `(path: Path) -> str` | 42 |
| forja_ar_ciclo.py | function | _load_required | `(path: Path \| None, name: str, errors: list[str]) -> dict` | 129 |
| forja_ar_corpus.py | function | _read_json | `(path: Path, fallback = <default>)` | 23 |
| forja_ar_corpus.py | function | _sha256_file | `(path: Path) -> str` | 30 |
| forja_ar_corpus.py | function | _canonical | `(value) -> bytes` | 38 |
| forja_ar_corpus.py | function | _fold | `(value: str) -> str` | 70 |
| forja_ar_corpus.py | function | _case_metadata | `(case_dir: Path) -> dict` | 105 |
| forja_ar_corpus.py | function | _artifact_candidates | `(case_dir: Path) -> list[tuple[int, Path, str]]` | 134 |
| forja_ar_evolucao.py | function | _sha_file | `(path: Path) -> str` | 27 |
| forja_ar_evolucao.py | function | _load | `(path: Path) -> dict` | 31 |
| forja_ar_evolucao.py | function | _save | `(path: Path, payload: dict) -> None` | 35 |
| forja_ar_evolucao.py | function | _manifest_path | `(experimento: str) -> Path` | 40 |
| forja_ar_indicadores.py | function | _canonical | `(value) -> bytes` | 18 |
| forja_ar_indicadores.py | function | _sha | `(value: bytes \| str) -> str` | 22 |
| forja_ar_indicadores.py | function | _null | `(reason: str, evidence: list \| None = <default>) -> dict` | 26 |
| forja_ar_indicadores.py | function | _entries | `(context: dict, name: str) -> list[dict] \| None` | 30 |
| forja_ar_indicadores.py | function | _terms | `(item: dict, *keys: str) -> list[str]` | 37 |
| forja_ar_indicadores.py | function | _contains | `(text: str, terms: list[str]) -> bool` | 48 |
| forja_ar_indicadores.py | function | _sensor_versions | `() -> dict[str, str]` | 53 |
| forja_ar_indicadores.py | function | _i1 | `(text: str, context: dict) -> dict` | 61 |
| forja_ar_indicadores.py | function | _i3 | `(text: str, context: dict) -> dict` | 96 |
| forja_ar_indicadores.py | function | _i7 | `(text: str, context: dict) -> dict` | 120 |
| forja_ar_indicadores.py | function | _i8 | `(context: dict) -> dict` | 140 |
| forja_ar_indicadores.py | function | _load_ledgers | `(directory: Path \| None) -> dict` | 304 |
| forja_ar_runpair.py | function | _sha | `(path: Path) -> str` | 28 |
| forja_ar_runpair.py | function | _canonical | `(value) -> bytes` | 32 |
| forja_ar_runpair.py | function | _read_ledger | `(path: Path \| None) -> list` | 153 |
| forja_artefatos.py | function | _relatar | `(laudo: dict) -> None` | 204 |
| forja_assinatura_visual.py | function | _faixa | `(paginas)` | 48 |
| forja_assinatura_visual.py | function | _tabelas | `(doc, todos_os_niveis = <default>)` | 108 |
| forja_assinatura_visual.py | function | _caixas | `(doc)` | 131 |
| forja_assinatura_visual.py | function | _figuras_exibidas | `(z, doc, nomes)` | 143 |
| forja_assinatura_visual.py | function | _inventario | `(docx)` | 181 |
| forja_authorities.py | function | _context | `(text: str, start: int, end: int) -> str` | 116 |
| forja_authorities.py | function | _entry | `(*, tipo: str, classe: str, numero: str, corte: str, rotulo: str, dados: tuple, text: str, start: int, end: int, identity: dict \| None = <default>) -> dict` | 120 |
| forja_axi.py | function | _read_json | `(path: Path) -> Any` | 157 |
| forja_axi.py | function | _case_files | `(state_root: Path) -> list[Path]` | 174 |
| forja_axi.py | function | _blocker_text | `(blocker: Any) -> str` | 180 |
| forja_axi.py | function | _truncate | `(text: str, limit: int, *, full: bool) -> tuple[str, bool]` | 193 |
| forja_axi.py | function | _case_summary | `(path: Path, data: dict[str, Any]) -> dict[str, Any]` | 202 |
| forja_axi.py | function | _load_cases | `(state_root: Path) -> tuple[list[dict[str, Any]], list[str]]` | 239 |
| forja_axi.py | function | _select_fields | `(item: dict[str, Any], fields: Sequence[str]) -> dict[str, Any]` | 260 |
| forja_axi.py | function | _parse_fields | `(raw: str \| None, allowed: Sequence[str], default: Sequence[str]) -> list[str]` | 266 |
| forja_axi.py | function | _queue_summary | `(queue: dict[str, Any]) -> dict[str, Any]` | 281 |
| forja_axi.py | function | _resolve_case_path | `(state_root: Path, case_id: str) -> Path` | 372 |
| forja_axi.py | function | _queue_item | `(item: dict[str, Any]) -> dict[str, Any]` | 443 |
| forja_axi.py | function | _needs_quote | `(value: str, delimiter: str = <default>) -> bool` | 594 |
| forja_axi.py | function | _toon_string | `(value: str, delimiter: str = <default>) -> str` | 608 |
| forja_axi.py | function | _toon_primitive | `(value: Any, delimiter: str = <default>) -> str` | 625 |
| forja_axi.py | function | _is_primitive | `(value: Any) -> bool` | 643 |
| forja_axi.py | function | _uniform_primitive_rows | `(items: list[Any]) -> tuple[bool, list[str]]` | 647 |
| forja_axi.py | function | _encode_toon_value | `(key: str \| None, value: Any, *, depth: int, lines: list[str]) -> None` | 659 |
| forja_axi.py | function | _extract_output_format | `(argv: list[str]) -> tuple[list[str], str]` | 754 |
| forja_axi.py | function | _dispatch | `(args: argparse.Namespace, state_root: Path) -> dict[str, Any]` | 829 |
| forja_baseline.py | function | _run | `(args: list[str]) -> tuple[int, str]` | 91 |
| forja_baseline.py | function | _pytest | `(nome: str) -> dict` | 101 |
| forja_baseline.py | function | _script | `(nome: str, papel: str) -> dict` | 116 |
| forja_baseline.py | function | _parece_script_autonomo | `(nome: str) -> bool` | 128 |
| forja_baseline.py | function | _scripts_autonomos_nao_mapeados | `() -> list[str]` | 136 |
| forja_baseline.py | function | _imprimir | `(relatorio: dict) -> None` | 183 |
| forja_baseline_aprovado.py | function | _resolver | `(relativo: str) -> Path \| None` | 74 |
| forja_baseline_aprovado.py | function | _medir | `(caminho: Path) -> dict` | 82 |
| forja_bench_modelos.py | function | _norm | `(texto: str) -> str` | 129 |
| forja_bench_modelos.py | function | _sinal_afirmado | `(texto: str, sinal: str) -> bool` | 145 |
| forja_bench_modelos.py | function | _resumir | `(resultados: list[dict]) -> dict[str, dict]` | 209 |
| forja_bench_modelos.py | function | _imprimir | `(relatorio: dict) -> None` | 300 |
| forja_calibra_monetario.py | function | _texto | `(caminho)` | 56 |
| forja_calibra_monetario.py | function | _amostrar_contexto | `(texto, n)` | 152 |
| forja_canario_catraca.py | function | _aperta | `(entrada: dict) -> dict` | 91 |
| forja_canario_catraca.py | function | _relatar | `(laudo: dict) -> None` | 136 |
| forja_canario_mutacao.py | function | _muta_texto | `(texto: str, modo: str) -> str` | 84 |
| forja_canario_mutacao.py | function | _muta | `(dados, modo: str)` | 95 |
| forja_canario_mutacao.py | function | _vereditos | `(pasta: Path, resultado: dict) -> dict` | 122 |
| forja_canario_mutacao.py | function | _tentativas | `(base: Path) -> list` | 132 |
| forja_canario_mutacao.py | function | _muta_arquivo | `(arquivo: Path, modo: str) -> None` | 139 |
| forja_canario_mutacao.py | function | _internaliza_externos | `(pasta: Path, espelho: Path, resultado: dict, modo: str) -> dict` | 156 |
| forja_canario_mutacao.py | function | _relatar | `(laudo: dict) -> None` | 299 |
| forja_case_tests.py | function | _parse_aware_iso | `(value: object) -> datetime \| None` | 37 |
| forja_case_tests.py | function | _deterministic | `(test: dict, text: str) -> tuple[str, str]` | 89 |
| forja_citations.py | function | _chave_autoridade | `(identidade)` | 351 |
| forja_citations.py | function | _indice_do_ledger | `(ledger)` | 368 |
| forja_citations.py | function | _normalizar_tribunal | `(bruto)` | 513 |
| forja_claim_binding.py | function | _entries | `(payload: dict) -> list[dict]` | 18 |
| forja_close_cycle.py | function | _canonical_manifest | `(case_dir: Path, expected_revision: int) -> tuple[dict, dict]` | 15 |
| forja_conselho.py | function | _ler | `(caminho: Path \| None) -> str \| None` | 53 |
| forja_conselho.py | function | _achados_parecer | `(persona: str, caminho: Path \| None) -> list[dict]` | 62 |
| forja_conselho.py | function | _linhas_de_decisao | `(texto: str) -> list[list[str]]` | 92 |
| forja_conselho.py | function | _achados_decisoes_json | `(texto: str) -> list[dict] \| None` | 111 |
| forja_conselho.py | function | _achados_decisoes | `(caminho: Path \| None) -> list[dict]` | 189 |
| forja_consistency.py | function | _eval_formula | `(formula: str, values: dict[str, float]) -> float` | 133 |
| forja_context.py | function | _norm | `(text: str) -> str` | 18 |
| forja_context.py | function | _covered_pages | `(entry: dict, page_count: int) -> set[int]` | 119 |
| forja_contexto.py | function | _hashes_do_texto | `(texto: str) -> set` | 47 |
| forja_contexto.py | function | _declarado_bool | `(*fontes, chaves)` | 53 |
| forja_contexto.py | function | _pendencias | `(*fontes) -> list` | 77 |
| forja_contexto.py | function | _liberacao_externa | `(*fontes)` | 91 |
| forja_delivery.py | function | _parse_iso | `(texto)` | 155 |
| forja_delivery_integrity.py | function | _attachment | `(package: dict, artifact_id: str) -> dict` | 15 |
| forja_document_compare.py | function | _normalized_text | `(value: str) -> str` | 69 |
| forja_document_compare.py | function | _is_protocol_noise | `(value: str) -> bool` | 77 |
| forja_document_compare.py | function | _paragraph_text | `(element: ET.Element) -> tuple[str, dict]` | 95 |
| forja_document_compare.py | function | _docx_part_units | `(raw: bytes, part: str) -> tuple[list[Unit], dict]` | 120 |
| forja_document_compare.py | function | _tokens_with_locators | `(units: list[Unit]) -> tuple[list[str], list[str]]` | 329 |
| forja_document_compare.py | function | _unique_ordered | `(values: list[str]) -> list[str]` | 339 |
| forja_document_compare.py | function | _change_regions | `(opcodes: list[tuple[str, int, int, int, int]], *, bridge_tokens: int = <default>)` | 343 |
| forja_docx_layout.py | function | _norm | `(value: str \| None) -> str` | 105 |
| forja_docx_layout.py | function | _text_sha256 | `(text: str) -> str` | 109 |
| forja_docx_layout.py | function | _paragraph_text | `(paragraph) -> str` | 238 |
| forja_docx_layout.py | function | _unique_header_parts | `(document)` | 244 |
| forja_docx_layout.py | function | _right_margin_pt | `(section) -> tuple[float \| None, bool]` | 257 |
| forja_docx_layout.py | function | _folios_com_margem | `(document)` | 288 |
| forja_docx_layout.py | function | _folio_rectangles | `(document)` | 339 |
| forja_docx_layout.py | function | _vml_width_pt | `(rect) -> float \| None` | 350 |
| forja_docx_layout.py | function | _set_vml_width_pt | `(rect, width_pt: float) -> None` | 356 |
| forja_docx_layout.py | function | _style_chain | `(style)` | 372 |
| forja_docx_layout.py | function | _effective_alignment | `(paragraph) -> int` | 380 |
| forja_docx_layout.py | function | _font_from_rpr | `(rpr) -> str \| None` | 390 |
| forja_docx_layout.py | function | _size_from_rpr | `(rpr) -> float \| None` | 403 |
| forja_docx_layout.py | function | _style_font_size | `(style) -> tuple[str \| None, float \| None]` | 415 |
| forja_docx_layout.py | function | _effective_run_font_size | `(run_element, paragraph) -> tuple[str \| None, float \| None]` | 428 |
| forja_docx_layout.py | function | _substantial_run_text | `(run_element) -> str` | 436 |
| forja_docx_layout.py | function | _has_visual_container | `(paragraph) -> bool` | 444 |
| forja_docx_layout.py | function | _is_heading | `(paragraph, text: str) -> bool` | 457 |
| forja_docx_layout.py | function | _is_caption | `(text: str) -> bool` | 471 |
| forja_docx_layout.py | function | _is_signature | `(text: str) -> bool` | 475 |
| forja_docx_layout.py | function | _e_titulo_centralizado | `(paragraph, text: str) -> bool` | 521 |
| forja_docx_layout.py | function | _role_for | `(paragraph, text: str, index: int, previous_role: str \| None) -> str` | 533 |
| forja_docx_layout.py | function | _load_exceptions | `(path: Path \| None, docx_sha256: str) -> tuple[dict[int, dict], list[dict]]` | 588 |
| forja_docx_layout.py | function | _set_run_font_size | `(run_element, font_name: str, size_pt: float) -> None` | 841 |
| forja_editorial.py | function | _actual_model | `(payload: dict, canonical: str) -> str \| None` | 98 |
| forja_editorial.py | function | _recompor_stream | `(saida: str) -> dict` | 108 |
| forja_editorial.py | function | _invoke | `(prompt: str, *, alias: str, timeout_s: int = <default>) -> dict` | 141 |
| forja_editorial.py | function | _strip_json_fence | `(value: str) -> str` | 206 |
| forja_editorial.py | function | _parse_result | `(result: str) -> tuple[str, dict]` | 213 |
| forja_editorial.py | function | _normalize_anchor | `(value: str) -> str` | 232 |
| forja_editorial.py | function | _taste_receipt_findings | `(report: dict, source: str, final: str) -> list[dict]` | 236 |
| forja_editorial.py | function | _gate_is_clear | `(path: Path) -> bool` | 308 |
| forja_editorial_fidelity.py | function | _fold | `(value: str) -> str` | 79 |
| forja_editorial_fidelity.py | function | _counter | `(pattern: re.Pattern, text: str) -> Counter` | 84 |
| forja_editorial_fidelity.py | function | _is_upper_title | `(value: str) -> bool` | 97 |
| forja_editorial_fidelity.py | function | _heading_counter | `(text: str) -> Counter` | 102 |
| forja_editorial_fidelity.py | function | _pedidos | `(text: str) -> str \| None` | 114 |
| forja_editorial_fidelity.py | function | _counter_delta | `(source: Counter, final: Counter) -> dict` | 127 |
| forja_editorial_fidelity.py | function | _authority_semantic_counter | `(text: str) -> Counter` | 133 |
| forja_editorial_fidelity.py | function | _finding | `(gate: str, detail: str, **extra) -> dict` | 149 |
| forja_editorial_fidelity.py | function | _family_findings | `(report: dict, strict: bool) -> list[dict]` | 153 |
| forja_email.py | function | _servico | `()` | 42 |
| forja_email.py | function | _cabecalho | `(msg: dict, nome: str) -> str` | 64 |
| forja_email.py | function | _registrar | `(evento: dict) -> None` | 87 |
| forja_entrega.py | function | _reconciliacao_em_texto | `(texto: str)` | 68 |
| forja_entrega.py | function | _entregaveis | `(manifesto: dict) -> list` | 150 |
| forja_estilo_humano.py | function | _sem_acentos | `(value: str) -> str` | 161 |
| forja_estilo_humano.py | function | _limpar_markdown | `(texto: str) -> str` | 166 |
| forja_estilo_humano.py | function | _limpar_email | `(texto: str) -> str` | 179 |
| forja_estilo_humano.py | function | _contexto | `(texto: str, inicio: int, fim: int, alcance: int = <default>) -> str` | 201 |
| forja_estilo_humano.py | function | _achado | `(regra: str, severidade: str, trecho: str, problema: str, acao: str, **extra) -> dict` | 205 |
| forja_estilo_humano.py | function | _paragrafos | `(texto: str) -> list[str]` | 218 |
| forja_estilo_humano.py | function | _sentencas | `(paragrafo: str) -> list[str]` | 232 |
| forja_estilo_humano.py | function | _tokens | `(texto: str) -> list[str]` | 237 |
| forja_estilo_humano.py | function | _cv | `(valores: list[int]) -> float` | 242 |
| forja_estilo_humano.py | function | _padroes_fixos | `(texto: str) -> list[dict]` | 247 |
| forja_estilo_humano.py | function | _conectores | `(texto: str, paragrafos: list[str]) -> list[dict]` | 273 |
| forja_estilo_humano.py | function | _travessoes | `(texto: str) -> list[dict]` | 302 |
| forja_estilo_humano.py | function | _dogmatismo | `(texto: str, paragrafos: list[str]) -> list[dict]` | 324 |
| forja_estilo_humano.py | function | _redundancia | `(paragrafos: list[str]) -> list[dict]` | 348 |
| forja_estilo_humano.py | function | _ritmo_robotico | `(paragrafos: list[str]) -> list[dict]` | 382 |
| forja_estilo_humano.py | function | _simetria | `(paragrafos: list[str]) -> list[dict]` | 401 |
| forja_estilo_humano.py | function | _conclusao_tautologica | `(paragrafos: list[str]) -> list[dict]` | 425 |
| forja_estilo_humano.py | function | _email_especifico | `(texto: str, paragrafos: list[str]) -> list[dict]` | 453 |
| forja_exploracao_100.py | function | _selection_rank | `(question: dict) -> tuple` | 82 |
| forja_exploracao_100.py | function | _issue | `(code: str, detail: str, severity: str = <default>) -> dict` | 429 |
| forja_exploracao_100.py | function | _norm | `(text: object) -> str` | 433 |
| forja_exploracao_100.py | function | _texto | `(value: object) -> str` | 439 |
| forja_exploracao_100.py | function | _placeholder | `(text: object) -> bool` | 449 |
| forja_f10_contract.py | function | _pass | `(ok: bool) -> str` | 28 |
| forja_f10_contract.py | function | _external_identifier_valid | `(evidence: dict) -> bool` | 32 |
| forja_f10_contract.py | function | _management_synced | `(state: dict, *, minimum_event_seq: int) -> bool` | 46 |
| forja_f8_contract.py | function | _validate_static_f8 | `(artifact: dict, *, files: dict, release_policy: str) -> dict` | 29 |
| forja_f8_contract.py | function | _svg_lint | `(svg) -> str` | 109 |
| forja_f8_contract.py | function | _markdown_lint | `(ledger: dict) -> str` | 160 |
| forja_f8_contract.py | function | _gates_do_contrato | `(ledger: dict, layout: dict \| None, fidelity: dict \| None, findings: list[str], *, release_policy: str) -> dict` | 181 |
| forja_f8_contract.py | function | _validate_legacy_f8 | `(artifact: dict, *, files: dict, release_policy: str = <default>) -> dict` | 252 |
| forja_fidelity.py | function | _norm | `(value: str) -> str` | 33 |
| forja_fidelity.py | function | _docx_text | `(path: Path) -> str` | 40 |
| forja_fidelity.py | function | _pdf_text | `(path: Path) -> tuple[str, int]` | 49 |
| forja_fidelity.py | function | _segments | `(block: dict) -> list[str]` | 56 |
| forja_fidelity.py | function | _coverage | `(segments: list[dict], target: str) -> tuple[float, list[dict]]` | 72 |
| forja_fidelity.py | function | _number_tokens | `(value: str) -> Counter` | 100 |
| forja_fidelity.py | function | _missing_counter | `(source: Counter, target: Counter) -> list[dict]` | 123 |
| forja_fidelity.py | function | _missing_numbers | `(source: Counter, target_text: str) -> list[dict]` | 131 |
| forja_fidelity.py | function | _qualifier_counts | `(value: str) -> Counter` | 142 |
| forja_fila.py | function | _norm | `(texto)` | 59 |
| forja_fila.py | function | _parse_date | `(valor)` | 65 |
| forja_fila.py | function | _fase_num | `(current_phase)` | 75 |
| forja_fila.py | function | _aguardando_desde | `(demanda)` | 196 |
| forja_fila.py | function | _read_json | `(path, fallback)` | 268 |
| forja_fila.py | function | _carregar_states | `()` | 275 |
| forja_fila.py | function | _relatorio_md | `(fila)` | 285 |
| forja_fontes_oficiais.py | function | _fontes | `(ledger: dict) -> list` | 64 |
| forja_fontes_oficiais.py | function | _rotulo | `(fonte: dict) -> str` | 72 |
| forja_fontes_oficiais.py | function | _primeiro | `(fonte: dict, campos) -> str \| None` | 80 |
| forja_fontes_oficiais.py | function | _resolver | `(caminho: str, base_dir) -> Path` | 88 |
| forja_fontes_oficiais.py | function | _itens_checklist | `(checklist: dict) -> list` | 192 |
| forja_fontes_oficiais.py | function | _usou_citacao_textual | `(item: dict) -> bool` | 200 |
| forja_fontes_oficiais.py | function | _cotejo_registrado | `(item: dict) -> bool` | 211 |
| forja_fontes_oficiais.py | function | _cotejo_em_texto | `(texto: str) -> dict` | 239 |
| forja_forma_artefatos.py | function | _radical | `(caminho: Path) -> str` | 49 |
| forja_forma_artefatos.py | function | _lidos_pelo_censo | `() -> set` | 53 |
| forja_forma_artefatos.py | function | _relatar | `(laudo: dict) -> None` | 119 |
| forja_gate_liveness.py | function | _nomes_declarados | `() -> dict[str, set[str]]` | 51 |
| forja_gate_liveness.py | function | _alias | `(nome: str) -> set[str]` | 65 |
| forja_gate_liveness.py | function | _observados | `() -> tuple[dict[str, dict], int]` | 77 |
| forja_gate_liveness.py | function | _sem_produtor | `(declarados: dict[str, set[str]]) -> list[dict]` | 117 |
| forja_headless.py | function | _invoke_headless | `(case_key, fase, prompt)` | 60 |
| forja_headless.py | function | _confirmar_modelo | `(payload, fase)` | 93 |
| forja_headless.py | function | _validate_n3_attempt | `(case_key, fase, attempt_dir)` | 110 |
| forja_headless.py | function | _write_n3_attempt | `(case_dir, fase, payload, resultado, uso, custo, attempt, context)` | 121 |
| forja_human_review.py | function | _trusted_key | `(trust_store: dict, reviewer_id: str, key_id: str) -> tuple[dict \| None, list[str]]` | 129 |
| forja_human_review.py | function | _load_pinned_trust_store | `(trust_store_path: Path \| None, trust_store_pin_path: Path \| None) -> tuple[dict, list[str]]` | 146 |
| forja_human_review.py | function | _validate_signed_receipt | `(receipt_path: Path, *, expected: dict, attestation_version: str, review_purpose: str, trust_store_path: Path \| None = <default>, trust_store_pin_path: Path \| None = <default>) -> dict` | 174 |
| forja_ingestao.py | function | _lista | `(valor) -> list` | 54 |
| forja_ingestao.py | function | _tem_conteudo | `(valor) -> bool` | 62 |
| forja_injection_scan.py | function | _esta_dentro_de | `(caminho, raiz)` | 97 |
| forja_injection_scan.py | function | _id_origem | `(caminho)` | 106 |
| forja_injection_scan.py | function | _gravar_json_seguro | `(caminho, payload)` | 112 |
| forja_injection_scan.py | function | _achatar | `(valor, profundidade = <default>)` | 335 |
| forja_injection_scan.py | function | _houve_varredura | `(scan)` | 348 |
| forja_injection_scan.py | function | _p0_detectado | `(scan)` | 359 |
| forja_injection_scan.py | function | _tem_triagem | `(scan)` | 386 |
| forja_lastro.py | function | _negado | `(antes: str) -> bool` | 214 |
| forja_lastro.py | function | _norm | `(texto: str) -> str` | 237 |
| forja_lastro.py | function | _ctx | `(texto: str, ini: int, fim: int, alcance: int = <default>) -> str` | 249 |
| forja_lastro.py | function | _conferivel_como_texto | `(alvo: Path) -> bool` | 269 |
| forja_lastro.py | function | _sha256_file | `(caminho: Path, *, bloco: int = <default>) -> str` | 602 |
| forja_lastro.py | function | _normalizar_data_base | `(valor: object) -> str \| None` | 614 |
| forja_lastro.py | function | _data_base_do_produto | `(texto: str) -> str \| None` | 643 |
| forja_lastro.py | function | _numero_monetario | `(valor: str) -> float \| None` | 651 |
| forja_lastro.py | function | _valores_monetarios | `(texto: str) -> list[dict]` | 677 |
| forja_lastro.py | function | _fonte_path | `(fato: dict, base_dir: Path \| None) -> Path \| None` | 762 |
| forja_lastro.py | function | _fonte_prevalente | `(ledger: dict) -> list[dict]` | 783 |
| forja_lastro.py | function | _achado | `(gate: str, problema: str, *, sev: str = <default>, acao: str \| None = <default>, **extra) -> dict` | 789 |
| forja_lastro.py | function | _anchor_entries | `(ledger: dict) -> list[dict]` | 841 |
| forja_lastro.py | function | _texto_da_ancora | `(entrada: dict) -> str` | 857 |
| forja_lastro.py | function | _ancora_aponta_prevalente | `(entrada: dict, fontes: list[dict]) -> bool` | 864 |
| forja_lastro.py | function | _descartes | `(ledger: dict) -> list[dict]` | 973 |
| forja_lastro.py | function | _inventario_economico | `(base_dir: Path \| None) -> list[dict]` | 982 |
| forja_lastro.py | function | _examinado | `(item: dict, examinados: list) -> bool` | 1017 |
| forja_lastro.py | function | _descartado | `(item: dict, descartes: list[dict]) -> bool` | 1030 |
| forja_learning.py | function | _duplicates | `(values: list[str]) -> set[str]` | 37 |
| forja_learning.py | function | _raw_keys | `(value: object, prefix: str = <default>) -> list[str]` | 42 |
| forja_learning_registry.py | function | _load | `() -> dict` | 26 |
| forja_ledger_material.py | function | _parse_proposicoes | `(path: Path) -> list[dict]` | 46 |
| forja_ledger_material.py | function | _source_ledger | `(case_dir: Path) -> list[dict]` | 70 |
| forja_ledger_material.py | function | _casar_source_ledger | `(rotulo: str, ledger: list[dict]) -> dict \| None` | 78 |
| forja_legal_search.py | function | _now | `() -> str` | 26 |
| forja_legal_search.py | function | _canonical_hash | `(value: Any) -> str` | 30 |
| forja_legal_search.py | function | _atomic_write_json | `(path: Path, payload: Any) -> None` | 35 |
| forja_legal_search.py | function | _sanitize | `(value: Any) -> Any` | 45 |
| forja_legal_search.py | function | _common_parser | `() -> argparse.ArgumentParser` | 221 |
| forja_local_context.py | function | _fase | `(nome)` | 24 |
| forja_local_context.py | function | _ts | `(texto)` | 29 |
| forja_local_context.py | function | _caso | `(pasta)` | 36 |
| forja_memoria_auditabilidade.py | function | _write_text | `(path: Path, text: str) -> None` | 93 |
| forja_memoria_auditabilidade.py | function | _read_json | `(path: Path) -> Any` | 100 |
| forja_memoria_auditabilidade.py | function | _redact | `(value: Any) -> str` | 107 |
| forja_memoria_auditabilidade.py | function | _relative | `(path: Path, case_dir: Path) -> str` | 115 |
| forja_memoria_auditabilidade.py | function | _state_path | `(case_dir: Path) -> Path \| None` | 122 |
| forja_memoria_auditabilidade.py | function | _state | `(case_dir: Path) -> tuple[dict[str, Any], Path \| None]` | 130 |
| forja_memoria_auditabilidade.py | function | _phase_status | `(phase: str, state: dict[str, Any]) -> str` | 136 |
| forja_memoria_auditabilidade.py | function | _canonical_phase | `(value: Any) -> str` | 150 |
| forja_memoria_auditabilidade.py | function | _artifact_inventory | `(case_dir: Path, state: dict[str, Any]) -> list[dict[str, Any]]` | 155 |
| forja_memoria_auditabilidade.py | function | _control_files | `(case_dir: Path) -> list[Path]` | 210 |
| forja_memoria_auditabilidade.py | function | _summary_for_control | `(path: Path, case_dir: Path) -> dict[str, Any]` | 222 |
| forja_memoria_auditabilidade.py | function | _source_summary | `(case_dir: Path) -> dict[str, Any]` | 246 |
| forja_memoria_auditabilidade.py | function | _visual_summary | `(controls: list[dict[str, Any]]) -> dict[str, Any]` | 274 |
| forja_memoria_auditabilidade.py | function | _md | `(payload: dict[str, Any], manifest_sha: str) -> str` | 363 |
| forja_memoria_auditabilidade.py | function | _html_document | `(markdown: str, payload: dict[str, Any], manifest_sha: str) -> str` | 446 |
| forja_metadata.py | function | _replace_core_text | `(xml: bytes, tag: str, value: str) -> bytes` | 41 |
| forja_metricas_gates.py | function | _fase | `(nome)` | 26 |
| forja_metricas_gates.py | function | _ts | `(texto)` | 32 |
| forja_metricas_gates.py | function | _ler | `(caminho)` | 39 |
| forja_modelos.py | function | _confirmar_modelo_reportado | `(modelo: Modelo, payload: dict) -> None` | 164 |
| forja_modelos.py | function | _segredo | `(nome: str) -> str` | 190 |
| forja_modelos.py | function | _post | `(url: str, cabecalhos: dict, corpo: dict, timeout: int) -> dict` | 209 |
| forja_modelos.py | function | _openrouter | `(modelo: Modelo, prompt: str, sistema: str \| None, max_tokens: int, timeout: int) -> tuple[str, int, int, int]` | 224 |
| forja_mutation_semantic.py | function | _ano_mais_um | `(m: re.Match) -> str` | 126 |
| forja_mutation_semantic.py | function | _digito_mais_um | `(m: re.Match) -> str` | 130 |
| forja_mutation_semantic.py | function | _aplicar | `(texto: str, padrao: str, subst: str, ocorrencia: int) -> str \| None` | 138 |
| forja_mutation_semantic.py | function | _p0_por_gate | `(texto: str) -> Counter` | 159 |
| forja_mutation_semantic.py | function | _suite_mata | `(suite: dict, texto: str) -> str \| None` | 166 |
| forja_mutation_semantic.py | function | _achar_caso | `(chave: str) -> Path` | 256 |
| forja_mutation_semantic.py | function | _achar_draft | `(case_dir: Path) -> Path \| None` | 266 |
| forja_n3_common.py | function | _pid_alive | `(pid: int) -> bool` | 158 |
| forja_n3_common.py | method | InterProcessLock._can_reclaim | `(self) -> bool` | 179 |
| forja_n3_common.py | method | InterProcessLock.__enter__ | `(self) -> 'InterProcessLock'` | 187 |
| forja_n3_common.py | method | InterProcessLock.__exit__ | `(self, exc_type: object, exc: object, tb: object) -> None` | 209 |
| forja_n3_shadow_replay.py | function | _phase_number | `(value: object) -> int \| None` | 30 |
| forja_n3_shadow_replay.py | function | _phase_regressions | `(history: list[dict]) -> list[dict]` | 35 |
| forja_n3_shadow_replay.py | function | _artifact_candidates | `(case_dir: Path, raw: str, state_root: Path) -> list[Path]` | 57 |
| forja_n3_shadow_replay.py | function | _artifact_audit | `(case_dir: Path, legacy: dict, state_root: Path) -> dict` | 64 |
| forja_n3_shadow_replay.py | function | _json_audit | `(case_dir: Path) -> list[dict]` | 79 |
| forja_n3_shadow_replay.py | function | _visual_roots | `(case_dir: Path, legacy: dict) -> list[Path]` | 89 |
| forja_n3_shadow_replay.py | function | _visual_audit | `(case_dir: Path, legacy: dict, *, deep: bool) -> dict` | 97 |
| forja_n3_shadow_replay.py | function | _render_markdown | `(report: dict) -> str` | 184 |
| forja_n4_anti_fraud_audit.py | function | _snapshot | `(case_dir: Path, sidecar: dict) -> dict` | 23 |
| forja_n4_baseline.py | function | _protected | `(case_dir: Path) -> dict[str, str]` | 18 |
| forja_n4_e2e_adversarial.py | function | _load | `(path: Path) -> dict` | 21 |
| forja_n4_e2e_adversarial.py | function | _save | `(path: Path, payload: dict) -> None` | 25 |
| forja_n4_e2e_adversarial.py | function | _copy_case | `(source: Path, parent: Path) -> Path` | 31 |
| forja_n4_e2e_adversarial.py | function | _codes | `(report: dict) -> set[str]` | 37 |
| forja_n4_m6_cycles.py | function | _docx_semantic_text | `(path: Path) -> str` | 76 |
| forja_n4_m6_prepare.py | function | _extract_text | `(docx_path: Path) -> str` | 42 |
| forja_n4_m6_prepare.py | function | _render | `(pdf_path: Path, pages_dir: Path) -> list[Path]` | 53 |
| forja_n4_m6_prepare.py | function | _contact_sheet | `(pages: list[Path], target: Path) -> None` | 64 |
| forja_n4_pilot_science.py | function | _article_text | `(xml: str) -> str` | 22 |
| forja_n4_validate.py | function | _settlement | `(payload: dict) -> list[dict]` | 66 |
| forja_n4_validate.py | function | _recipient_map_validator | `(config: dict) -> Validator` | 119 |
| forja_n4_validate.py | function | _pilot_blocking_finding | `(item: dict) -> bool` | 150 |
| forja_n4_validate.py | function | _target_phase | `(case_dir: Path) -> str` | 154 |
| forja_n4_validate.py | function | _required_files | `(config: dict) -> set[str]` | 162 |
| forja_n4_validate.py | function | _source_registry_findings | `(case_dir: Path, case_manifest: dict, *, require_verifiable: bool = <default>) -> tuple[set[str], list[dict]]` | 173 |
| forja_n4_validate.py | function | _registered_source_path | `(case_dir: Path, case_manifest: dict, digest: str) -> Path \| None` | 214 |
| forja_n4_validate.py | function | _result_core | `(payload: dict) -> dict` | 231 |
| forja_n4_validate.py | function | _council_ready | `(theses: dict) -> bool` | 238 |
| forja_n4_validate.py | function | _global_replay_findings | `(files: dict[str, dict]) -> list[dict]` | 252 |
| forja_n4_validate.py | function | _effective_named_mode | `(config: dict, case_dir: Path, namespace: str, override: str \| None = <default>) -> tuple[str, str]` | 353 |
| forja_n4_validate.py | function | _effective_mode | `(config: dict, case_dir: Path, override: str \| None = <default>) -> tuple[str, str]` | 380 |
| forja_n4_validate.py | function | _schema_findings | `(filename: str, payload: dict) -> list[dict]` | 391 |
| forja_n4_validate.py | function | _cross_reference_findings | `(files: dict[str, dict]) -> list[dict]` | 411 |
| forja_official_sources.py | class | _OfficialHtmlText | `(HTMLParser)` | 42 |
| forja_official_sources.py | function | _extract_source_text | `(path: Path) -> str` | 76 |
| forja_official_sources.py | function | _response_text | `(body: bytes, content_type: str) -> str` | 98 |
| forja_official_sources.py | function | _fetch_official | `(url: str, timeout: int = <default>) -> dict` | 117 |
| forja_official_sources.py | function | _candidate_anchors | `(text: str) -> list[str]` | 148 |
| forja_official_sources.py | function | _official_url | `(value: str) -> bool` | 224 |
| forja_official_sources.py | function | _urls_from_text | `(text: str) -> list[str]` | 233 |
| forja_official_sources.py | function | _identity_from_name | `(path: Path) -> dict \| None` | 237 |
| forja_official_sources.py | function | _identity_present | `(text: str, identity: dict \| None) -> bool` | 256 |
| forja_p0.py | function | _payload | `(achado: dict) -> dict` | 37 |
| forja_p0.py | function | _severidade | `(achado: dict) -> str` | 59 |
| forja_p0.py | function | _resolvido | `(achado: dict) -> bool` | 68 |
| forja_p0.py | function | _achados | `(resultado: dict) -> list` | 79 |
| forja_p0.py | function | _declarado | `(resultado: dict)` | 88 |
| forja_package.py | function | _protocolable_content | `(item: dict, markdown: dict, files: dict \| None = <default>) -> bool` | 74 |
| forja_package.py | function | _artifact | `(state: dict, artifact_id: str) -> dict` | 114 |
| forja_package.py | function | _f7_metrics | `(payload: dict, document_key: str \| None) -> dict` | 131 |
| forja_package.py | function | _pending_citations | `(metrics: dict) -> list[str]` | 140 |
| forja_package.py | function | _unresolved_markers | `(metrics: dict) -> list[str]` | 145 |
| forja_package.py | function | _ledger_entries | `(payload: Any) -> list[dict]` | 202 |
| forja_package.py | function | _citation_key | `(item: dict) -> tuple[str, str, str]` | 214 |
| forja_package.py | function | _markdown_paragraphs | `(markdown_path: Path) -> list[str]` | 218 |
| forja_package.py | function | _document_binding | `(item: dict, markdown: dict) -> tuple[dict, list[str]]` | 223 |
| forja_package.py | function | _denied_search_actions | `() -> set[str]` | 268 |
| forja_package.py | function | _brief_routes | `(case_dir: Path \| None) -> tuple[str \| None, set[str]]` | 276 |
| forja_package.py | function | _email_claims | `(email_text: str, pending: list[str]) -> list[str]` | 494 |
| forja_paragrafos.py | function | _norm | `(texto: str) -> str` | 67 |
| forja_paragrafos.py | function | _unidades | `(prov: dict) -> list` | 71 |
| forja_paragrafos.py | function | _tem_lastro | `(unidade: dict) -> bool` | 79 |
| forja_paragrafos.py | function | _e_editorial | `(unidade: dict) -> bool` | 89 |
| forja_paragrafos.py | function | _rotulo | `(unidade: dict) -> str` | 99 |
| forja_paragrafos.py | function | _hashes_do_texto | `(texto: str) -> set` | 110 |
| forja_post_protocol.py | function | _record | `(case_dir: Path, event_type: str, key: str, payload: dict, *, artifact_hashes: dict \| None = <default>) -> tuple[dict, bool]` | 119 |
| forja_post_protocol.py | function | _parse_timestamp | `(value: str \| None) -> datetime \| None` | 145 |
| forja_post_protocol.py | function | _baseline_records | `(case_dir: Path) -> list[dict]` | 155 |
| forja_post_protocol.py | function | _delivery_timestamp | `(message: dict) -> str` | 224 |
| forja_post_protocol.py | function | _sent_baseline_candidates | `(demand: dict, *, human_suffix: str, received_at: str, get_message) -> list[dict]` | 235 |
| forja_post_protocol.py | function | _walk_gmail_parts | `(payload: dict)` | 278 |
| forja_post_protocol.py | function | _select_return_parts | `(parts: list[dict]) -> tuple[list[dict], list[dict], str \| None]` | 398 |
| forja_post_protocol.py | function | _text_similarity | `(first: Path, second: Path) -> float` | 422 |
| forja_post_protocol.py | function | _verified_protocol_link | `(link: dict) -> bool` | 439 |
| forja_post_protocol.py | function | _folder_labels | `(protocol_status: str, piece_name: str, process_id: str, date_label: str) -> tuple[str, str]` | 514 |
| forja_post_protocol.py | function | _index_path | `(case_dir: Path) -> Path` | 527 |
| forja_post_protocol.py | function | _load_index | `(case_dir: Path) -> dict` | 531 |
| forja_post_protocol.py | function | _set_index_state | `(case_dir: Path, ckey: str, state: str, **updates: Any) -> None` | 538 |
| forja_post_protocol.py | function | _require_post_protocol_enabled | `() -> None` | 551 |
| forja_post_protocol.py | function | _block_capture | `(case_dir: Path, ckey: str, manifest_path: Path, manifest: dict, *, reason_codes: list[str], detail: str, human_artifact_id: str, protocol_status: str) -> dict` | 556 |
| forja_post_protocol.py | function | _write_artifact_checked | `(case_dir: Path, filename: str, content: dict, source_hashes: list[str], validator, *, producer_run_id: str) -> dict` | 596 |
| forja_post_protocol.py | function | _archive_prior_post_protocol_artifacts | `(case_dir: Path, incoming_content_key: str) -> None` | 622 |
| forja_post_protocol.py | function | _sanitize_changes | `(changes: list[dict]) -> list[dict]` | 642 |
| forja_post_protocol.py | function | _preserve_change_reviews | `(changes: list[dict], prior_changes: list[dict]) -> list[dict]` | 666 |
| forja_post_protocol.py | function | _learning_candidates | `(changes: list[dict], existing: list[dict] \| None = <default>) -> list[dict]` | 681 |
| forja_post_protocol.py | function | _regression_proposals | `(candidates: list[dict]) -> list[dict]` | 750 |
| forja_post_protocol.py | function | _learning_payload_for_content | `(case_dir: Path, candidate_id: str, content_key_value: str = <default>) -> tuple[Path, dict]` | 1434 |
| forja_post_protocol.py | function | _write_learning_payload | `(case_dir: Path, path: Path, payload: dict) -> None` | 1459 |
| forja_post_protocol.py | function | _write_human_diff_payload | `(case_dir: Path, path: Path, payload: dict) -> None` | 1472 |
| forja_post_protocol.py | function | _message_header | `(message: dict, name: str) -> str` | 1715 |
| forja_post_protocol.py | function | _case_for_demand | `(demand_id: str, demands: list[dict]) -> str \| None` | 1722 |
| forja_post_protocol.py | function | _sender_allowed | `(message: dict) -> bool` | 1746 |
| forja_post_protocol_contracts.py | function | _hash_findings | `(value: object, field: str, code: str) -> list[dict]` | 86 |
| forja_post_protocol_contracts.py | function | _raw_key_findings | `(value: object, prefix: str = <default>) -> list[dict]` | 90 |
| forja_precedente.py | function | _regime_findings | `(rotulo: str, regime: dict) -> list[dict]` | 181 |
| forja_precedente.py | function | _vigencia_findings | `(rotulo: str, card: dict, operation: str) -> list[dict]` | 223 |
| forja_precedente.py | function | _contrario_findings | `(rotulo: str, card: dict) -> list[dict]` | 261 |
| forja_produto.py | function | _texto | `(fonte: dict, campos) -> str \| None` | 52 |
| forja_produto.py | function | _conferir | `(fonte, campos, gate, rotulo, piso, achados, *, obrigatorio = <default>)` | 68 |
| forja_pso_pet.py | function | _text | `(value: Any) -> bool` | 33 |
| forja_pso_pet.py | function | _norm | `(value: Any) -> str` | 37 |
| forja_pso_pet.py | function | _ids | `(items: list[dict], key: str, code: str, findings: list[dict]) -> set[str]` | 41 |
| forja_pso_pet.py | function | _parse_iso | `(value: Any) -> datetime \| None` | 53 |
| forja_pso_pet.py | function | _registry | `(payload: dict) -> tuple[dict[str, dict], list[dict]]` | 63 |
| forja_pso_pet.py | function | _check_refs | `(refs: list[str], registry: dict[str, dict], findings: list[dict], *, owner: str, allow_final: bool = <default>) -> None` | 78 |
| forja_pso_pet.py | function | _dimension | `(code: str, checks: list[tuple[str, bool, str]]) -> dict` | 259 |
| forja_pso_pet.py | function | _valid_fixture | `() -> dict` | 454 |
| forja_qa_paginas.py | function | _densidade | `(img: Image.Image, y0: int = <default>, y1: int \| None = <default>) -> float` | 36 |
| forja_reasoning.py | function | _dependency_cycles | `(edges: list[dict]) -> list[list[str]]` | 112 |
| forja_reasoning.py | function | _fontes_do_mapa | `(payload: dict) -> dict[str, str]` | 242 |
| forja_reasoning.py | function | _idade_em_horas | `(momento: str \| None, agora: datetime \| None = <default>) -> float \| None` | 251 |
| forja_reasoning.py | function | _pool_de_ids | `(case_dir: Path, filename: str, chave: str, bloco: str) -> set[str] \| None` | 426 |
| forja_recomputo_censo.py | function | _ler | `(caminho) -> dict` | 32 |
| forja_recomputo_censo.py | function | _texto | `(caminho) -> str \| None` | 45 |
| forja_recomputo_censo.py | function | _artefatos_da_tentativa | `(pasta: Path, resultado: dict) -> list[dict]` | 52 |
| forja_recomputo_censo.py | function | _raiz_do_caso | `(pasta: Path) -> Path \| None` | 70 |
| forja_recomputo_censo.py | function | _irmao_promovido | `(pasta: Path, fase: str, nome: str) -> Path \| None` | 77 |
| forja_recomputo_censo.py | function | _produtores | `(pasta: Path, resultado: dict \| None = <default>) -> list` | 92 |
| forja_recomputo_censo.py | function | _relatar | `(laudo: dict) -> None` | 294 |
| forja_red_team.py | function | _itens_enumerados | `(texto: str) -> int` | 43 |
| forja_red_team.py | function | _itens_rechecados | `(recheck: dict) -> list` | 88 |
| forja_redacao.py | function | _origem_operacional | `(texto: str) -> list` | 39 |
| forja_redacao.py | function | _estilo_p0 | `(texto: str) -> list` | 49 |
| forja_regimento_gate.py | function | _bloco | `(dados: dict, campos) -> dict` | 49 |
| forja_regimento_gate.py | function | _mapa_em_texto | `(texto: str) -> dict` | 79 |
| forja_regimento_gate.py | function | _fatos_em_texto | `(texto: str) -> list` | 94 |
| forja_regimentos.py | function | _extrai_data | `(bruto: str) -> date \| None` | 90 |
| forja_regimentos.py | function | _primeiro | `(padroes: list[str], texto: str) -> str \| None` | 114 |
| forja_regimentos.py | function | _data_do_rotulo | `(texto: str) -> date \| None` | 124 |
| forja_regimentos.py | function | _relatorio | `(regs: list[Regimento]) -> str` | 220 |
| forja_regua.py | function | _manifest_key | `(value)` | 286 |
| forja_render_docx.py | function | _tipo_produto | `(texto, titulo)` | 76 |
| forja_replay.py | function | _fontes | `(ledger: dict) -> list` | 44 |
| forja_replay.py | function | _identificador | `(fonte: dict) -> str` | 52 |
| forja_replay.py | function | _replays | `(ledger: dict) -> dict` | 60 |
| forja_replay.py | function | _data | `(valor) -> date \| None` | 73 |
| forja_run.py | function | _artifact_path | `(entry: dict) -> Path \| None` | 44 |
| forja_run.py | function | _read_gate_artifact | `(path_value: Path \| str \| None) -> Any` | 49 |
| forja_run.py | function | _resolve_input | `(case_dir: Path, state: dict, input_id: str) -> dict \| None` | 61 |
| forja_run.py | function | _raiz_do_caso | `(alguma_saida: Path) -> Path \| None` | 173 |
| forja_run.py | function | _lastro_context_base | `(context: dict, referencia: Path \| None = <default>) -> Path \| None` | 188 |
| forja_run.py | function | _achar_fact_ledger | `(artifacts: list[dict], referencia: Path \| None) -> Path \| None` | 216 |
| forja_run.py | function | _severidade_economica | `(findings: list[dict]) -> str` | 239 |
| forja_run.py | function | _compute_lastro_gates | `(phase: str, artifacts: list[dict], context: dict) -> dict` | 247 |
| forja_run.py | function | _recompute_injecao | `(contract: dict, artifacts: list[dict], attempt_dir: Path, result: dict) -> None` | 374 |
| forja_run.py | function | _recompute_politica_citacoes | `(contract: dict, artifacts: list[dict], attempt_dir: Path, result: dict) -> None` | 399 |
| forja_run.py | function | _recompute_definicao | `(contract: dict, artifacts: list[dict], attempt_dir: Path, result: dict) -> None` | 445 |
| forja_run.py | function | _recompute_regimento | `(contract: dict, artifacts: list[dict], attempt_dir: Path, result: dict) -> None` | 528 |
| forja_run.py | function | _recompute_contexto | `(contract: dict, artifacts: list[dict], attempt_dir: Path, result: dict) -> None` | 570 |
| forja_run.py | function | _recompute_red_team | `(contract: dict, artifacts: list[dict], attempt_dir: Path, result: dict) -> None` | 622 |
| forja_run.py | function | _recompute_conselho | `(contract: dict, artifacts: list[dict], attempt_dir: Path, result: dict) -> None` | 656 |
| forja_run.py | function | _recompute_ingestao | `(contract: dict, artifacts: list[dict], attempt_dir: Path, result: dict) -> None` | 705 |
| forja_run.py | function | _recompute_exploracao | `(contract: dict, artifacts: list[dict], attempt_dir: Path, result: dict) -> None` | 738 |
| forja_run.py | function | _recompute_pesquisa_oficial | `(contract: dict, artifacts: list[dict], attempt_dir: Path, result: dict) -> None` | 772 |
| forja_run.py | function | _recompute_paragrafos | `(contract: dict, artifacts: list[dict], attempt_dir: Path, result: dict) -> None` | 814 |
| forja_run.py | function | _validate_result | `(attempt_dir: Path, contract: dict) -> tuple[dict, list[dict]]` | 863 |
| forja_run.py | function | _validate_f7_source_ledger | `(phase: str, artifacts: list[dict]) -> None` | 973 |
| forja_run.py | function | _validate_fable5_editorial | `(phase: str, artifacts: list[dict]) -> None` | 1006 |
| forja_run.py | function | _validate_human_style | `(phase: str, artifacts: list[dict]) -> None` | 1041 |
| forja_run.py | function | _promote_file | `(case_dir: Path, phase: str, artifact: dict) -> Path` | 1066 |
| forja_run_metrics.py | function | _safe_ledger | `(path_value: str \| None) -> dict` | 14 |
| forja_science.py | function | _get_json | `(base: str, params: dict, *, timeout: int = <default>) -> dict` | 21 |
| forja_science.py | function | _bibliographic_text | `(value: object) -> str` | 99 |
| forja_state_machine.py | function | _phase_index | `(phase: str) -> int` | 85 |
| forja_state_machine.py | function | _highest_completed_index | `(state: dict) -> int` | 92 |
| forja_state_machine.py | function | _base_state | `(case_dir: Path) -> dict` | 123 |
| forja_state_machine.py | function | _validate_transition | `(events: list[dict], event_type: str, phase: str \| None, payload: dict) -> None` | 303 |
| forja_state_machine.py | function | _materialize_locked | `(case_dir: Path, events: list[dict]) -> dict` | 349 |
| forja_svg_docx.py | function | _local | `(tag: str) -> str` | 39 |
| forja_svg_docx.py | function | _number | `(value: object, default: float = <default>) -> float` | 43 |
| forja_svg_docx.py | function | _svg_ratio | `(path: Path) -> float` | 48 |
| forja_svg_docx.py | function | _paragraphs | `(container)` | 61 |
| forja_svg_docx.py | function | _next_docpr_id | `(document) -> int` | 71 |
| forja_svg_docx.py | function | _new_svg_part | `(document, path: Path)` | 81 |
| forja_svg_docx.py | function | _inline_svg | `(document, path: Path, width_cm: float, docpr_id: int)` | 88 |
| forja_svg_docx.py | function | _validate_svg | `(path: Path) -> dict` | 174 |
| forja_varredura_tipografica.py | function | _e_entregavel | `(caminho: Path) -> bool` | 64 |
| forja_varredura_tipografica.py | function | _caso_de | `(caminho: Path) -> str` | 72 |
| forja_varredura_tipografica.py | function | _familia_de | `(caminho: Path) -> tuple[str, ...]` | 91 |
| forja_varredura_tipografica.py | function | _tem_marca_correcao | `(nome: str) -> bool` | 102 |
| forja_varredura_tipografica.py | function | _tokens_do_caminho | `(caminho: Path) -> set[str]` | 114 |
| forja_varredura_tipografica.py | function | _mesmo_caso | `(a: Path, b: Path, familia: tuple[str, ...]) -> bool` | 127 |
| forja_varredura_tipografica.py | function | _marcar_superadas | `(medidas: list) -> None` | 136 |
| forja_varredura_tipografica.py | function | _relatar | `(laudo: dict, limite: int) -> None` | 258 |
| forja_verificador.py | function | _ctx | `(texto, ini, fim, alcance = <default>)` | 113 |
| forja_verificador.py | function | _indice_fontes_oficiais | `()` | 142 |
| forja_verificador.py | function | _carregar_contexto_lastro | `(case_dir = <default>, ledger = <default>, base_dir = <default>)` | 365 |
| forja_visual.py | function | _norm | `(s)` | 46 |
| forja_visual.py | function | _e_enderecamento | `(linha)` | 53 |
| forja_visual.py | function | _consome_tabela | `(linhas, i)` | 58 |
| forja_visual.py | function | _larguras_tabela | `(header, corpo, total = <default>)` | 66 |
| forja_visual.py | class | _Mapa | `()` | 82 |
| forja_visual.py | method | _Mapa._valida | `(anc, texto_md, tipo)` | 140 |
| forja_visual_build.py | function | _tipo_produto | `(texto, titulo)` | 35 |
| forja_visual_figuras.py | function | _limpa | `(t)` | 32 |
| forja_visual_figuras.py | function | _chave | `(d, m, a)` | 36 |
| forja_visual_figuras.py | function | _mascara | `(texto)` | 52 |
| forja_visual_figuras.py | function | _datas | `(texto)` | 57 |
| forja_visual_figuras.py | function | _oracao | `(frase, pos_data, limite = <default>)` | 84 |
| forja_visual_figuras.py | function | _fonte_cronologica | `(texto_md)` | 116 |
| forja_visual_mapa_gen.py | function | _norm | `(s)` | 38 |
| forja_visual_mapa_gen.py | function | _e_enderecamento | `(linha)` | 45 |
| forja_visual_mapa_gen.py | function | _varre | `(texto_md)` | 58 |
| forja_visual_mapa_gen.py | function | _limpa | `(t)` | 200 |
| forja_visual_mapa_gen.py | function | _ancora | `(par, alvo_norm = <default>, minimo = <default>, maximo = <default>)` | 204 |
| forja_visual_mapa_gen.py | function | _frase | `(par, minimo = <default>, maximo = <default>)` | 224 |
| forja_visual_mapa_gen.py | function | _titulo_precedente | `(texto)` | 262 |
| forja_visual_mapa_gen.py | function | _rotulo_curto | `(texto, limite = <default>)` | 268 |
| forja_visual_mapa_gen.py | function | _rotulos_sintese | `(sintese_linhas, maximo = <default>)` | 286 |
| forja_visual_mapa_gen.py | function | _autovalidar | `(mapa, texto_md)` | 474 |
| forja_visual_mapa_gen.py | function | _checa | `(anc, alvo, vistos, origem)` | 488 |
| forja_visual_qa.py | function | _overlap_ratio | `(left: tuple[float, float, float, float], right: tuple[float, float, float, float]) -> float` | 53 |
| forja_visual_qa_structural.py | function | _svg_check | `(path: Path) -> dict` | 21 |
| forja_visual_qa_structural.py | function | _package_audit | `(docx: Path) -> dict` | 47 |
| forja_visual_qa_structural.py | function | _docx_lint | `(docx: Path) -> dict` | 82 |
| forja_visual_review.py | function | _rendered_page_map | `(rendered_pages: list[dict]) -> dict[int, dict]` | 37 |


## 10. Como uma IA deve usar este mapa

1. Localize o comando, símbolo ou schema nesta matriz ou por consulta Graphify.
2. Siga `imports_from`, `defines`, `calls`, `accepts_option` e `validates_against` até o contrato inferior.
3. Abra apenas os arquivos e linhas indicados; confirme arestas `AMBIGUOUS` antes de editar.
4. Identifique consumidores (handlers, runners, testes) antes de mudar assinatura ou schema.
5. Execute testes e validações do subsistema; existência de arquivo não prova compatibilidade.

## 11. Limitações materiais

- Dispatch dinâmico, reflexão, imports construídos em runtime e subprocessos com comandos montados podem não aparecer.
- Este é um mapa de contratos, não um inventário de dados nem prova de saúde operacional.
- As linhas são válidas para a versão hashada neste pacote; mudanças posteriores exigem regeneração.
