<!-- generated-by: gsd-doc-writer -->
# Configuração da FORJA

## Fontes de configuração

| Arquivo | Escopo |
|---|---|
| `FORJA_N3_CONFIG.json` | feature flags, modo N4, caminhos, locks e fila |
| `FORJA_SPEC_MANIFEST.json` | regras normativas, fases, componentes e documentação canônica |
| `phase_contracts/F0.json` … `F10.json` | contrato executável de cada fase N3 |
| `phase_contracts_n4/F0.json` … `F10.json` | requisitos adicionais da candidata N4 |
| `FORJA_SEARCH_CONFIG.json` | ponte de pesquisa jurídica TeiaJus/STJ |
| `REGUA_MANIFEST.json` | composição da régua de validação |

Não há arquivo `.env` obrigatório para o fluxo F7-B. A autenticação vem do login local do Claude Code e é conferida em cada execução.

## Configuração do modelo editorial (F7-B)

> **Renomeação de 25 e 26/07/2026.** O executor era `forja_fable5.py` e passou a ser `forja_editorial.py`; o nome antigo continua funcionando como shim com `DeprecationWarning`. O protocolo passou de `PROTOCOLO_FABLE5_ESCRITA_FINAL.md` para `PROTOCOLO_EDITORIAL_ESCRITA_FINAL.md`. Os **nomes de artefato e de gate não mudaram** — `FABLE5_RESULT.json`, `fable5_usage` e `fable5_oauth_confirmed` continuam válidos, agora com os apelidos `EDITORIAL_RESULT.json` e `editor_usage`.

A escolha de modelo fica em `forja_editorial_model.py`; as demais constantes operacionais, em `forja_editorial.py`:

| Parâmetro | Valor vigente | Efeito |
|---|---:|---|
| `DEFAULT_EDITORIAL_MODEL` | `claude-opus-5` | modelo editorial padrão desde 25/07/2026 |
| allowlist `EDITORIAL_MODELS` | `claude-opus-5` (alias `opus`), `claude-fable-5` (alias `fable`, legado), `gpt-5.6-sol` (sem alias) | modelo fora dela **não executa**; sem alias, o modelo é reconhecido apenas como revisor declarado, operado fora daqui — reconhecer não é saber executar |
| `FAMILY_ASSURANCE_LEVELS` | `cross_family`, `cross_session_same_family`, `unverified` | recomposto pelo orquestrador; `unverified` bloqueia em qualquer modo, e em `strict_protocol` só `cross_family` libera |
| `--model` (CLI) | opcional | só aceita valor dentro da allowlist |
| `TIMEOUT_S` | `1800` | limite de cada chamada editorial |
| `MAX_REWRITE_ATTEMPTS` | `3` | máximo de tentativas internas antes do bloqueio |
| `PHASE` | `F7_AUDITORIA_JURIDICA_FACTUAL` | fase que hospeda F7-B |

Alterar o modelo, a autenticação aceita ou os invariantes exige atualização conjunta do protocolo, dos contratos e dos testes.

## Feature flags

`FORJA_N3_CONFIG.json` registra `fable5FinalWritingV1: true`. Essa flag documenta a capacidade ativa, mas a obrigatoriedade executável vem do contrato F7 e da validação em `forja_run.py`.

As flags `phaseRunnerV1` e outras capacidades N3 podem continuar desligadas globalmente enquanto o código é usado em modo sombra ou por chamadas controladas. Não confunda disponibilidade do módulo com promoção global da N3.

## Contrato F7

As saídas adicionais obrigatórias são:

```json
[
  "final_markdown",
  "editorial_report",
  "editorial_diff",
  "fable5_usage",
  "editorial_fidelity"
]
```

Os gates adicionais obrigatórios são:

```json
[
  "fable5_oauth_confirmed",
  "editorial_source_hash_match",
  "editorial_fidelity_pass",
  "human_style_final_pass"
]
```

F8 recebe `final_markdown`, `audited_markdown` e `editorial_report`: o primeiro é o cânone de composição; os demais formam a trilha de auditoria.

## Autenticação Claude Code

Antes de executar F7-B:

```powershell
claude auth status
```

O executor exige:

- `loggedIn: true`;
- `authMethod: claude.ai`;
- `subscriptionType: max`;
- envelope `modelUsage` compatível com `claude-fable-5`.

O artefato `fable5_usage` persiste apenas os campos necessários à auditoria; não grava e-mail da conta nem credenciais.

## Múltiplos documentos

Use um sufixo seguro e pareado:

```powershell
python forja_editorial.py <caso> <attempt-dir> --source audited_markdown_note.md --f7-gate f7_gate_result.json --artifact-suffix _note
```

Isso produz `final_markdown_note`, `editorial_report_note`, `editorial_diff_note`, `fable5_usage_note` e `editorial_fidelity_note`. O pacote revalida o bundle correspondente ao `mdArtifactId` selecionado. No contrato vigente, esses bundles adicionais coexistem com o bundle-base sem sufixo, que continua obrigatório para a fase F7.

## Locks e tentativas

Os locks da máquina de estados vêm de `FORJA_N3_CONFIG.json`:

- `timeoutSeconds`: espera máxima para adquirir o lock;
- `staleAfterSeconds`: idade a partir da qual um lock abandonado pode ser tratado como obsoleto.

A repetição editorial ocorre dentro da mesma tentativa F7. Ela não cria evento de fase novo nem consome outra tentativa do contrato.

## Valores externos

Endereços de VPS, tokens, chaves, senhas e rotas externas não pertencem a esta configuração. O fluxo Fable 5 não usa API key e nenhum segredo deve ser incluído nos documentos ou no repositório.
