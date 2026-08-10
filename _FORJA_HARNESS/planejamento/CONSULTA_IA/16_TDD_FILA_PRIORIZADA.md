# Consulta IA — TDD — FORJA FILA: desenho técnico e plano de testes

> Cópia de consulta derivada. O documento canônico permanece no caminho de origem indicado abaixo.

## Metadados e rastreabilidade

- **Documento de origem:** `16_TDD_FILA_PRIORIZADA.md`
- **Tipo:** TDD
- **SHA-256 da origem:** `0c4e961b2db7887e31cbb008115b98ff6daed86385fe47ca45e704965c835bab`
- **Linhas da origem:** 143
- **Blocos integralmente indexados:** 9
- **Geração:** 2026-08-10T13:53:35-03:00
- **Cobertura:** 100% das linhas e do texto da origem, sem omissão.
- **Links relativos normalizados:** 0 destino(s), apenas para preservar a navegação na cópia.

## Roteiro de consulta para IA

**Síntese de localização:** Par do PRD 15PRDFILAPRIORIZADA.md. Estilo da casa: módulo único, funções puras testáveis, escrita atômica, feature flag, modo sombra primeiro.

**Termos de recuperação:** fila, json, painel, não, prazo, dict, score, forja_fila, fator, demandas, novo, cliente.

Use o índice abaixo para localizar o bloco pertinente. Cada entrada informa as linhas exatas no documento de origem. Para afirmações materiais, leia o bloco integral e confira o arquivo canônico pelo SHA-256.

## Índice detalhado e cobertura integral

- [SRC-S001 · L1–L6 · TDD — FORJA FILA: desenho técnico e plano de testes](#src-s001)
  - Assuntos: tdd, fila, desenho, técnico, plano, testes, par, prd
  - Trecho-guia: Par do PRD 15PRDFILAPRIORIZADA.md. Estilo da casa: módulo único, funções puras testáveis, escrita atômica, feature flag, modo sombra primeiro.
  - SHA-256 do bloco: `4447bbf30dc4e90127d4bb71247badd60dee0a79e4171b6400d8560288c93c34`
  - [SRC-S002 · L7–L17 · 1. Componentes](#src-s002)
    - Caminho: TDD — FORJA FILA: desenho técnico e plano de testes > 1. Componentes
    - Assuntos: forja_harness, novo, componentes, forja_fila, alteração, flag, componente, arquivo
    - Trecho-guia: Documento de consulta sobre 1. Componentes.
    - SHA-256 do bloco: `e49d9aff40b5725259f8abc2746cb3248e1a6a9bd20bb2e295ecd9c051756b30`
  - [SRC-S003 · L18–L53 · 2. Contratos das funções (núcleo puro — sem I/O)](#src-s003)
    - Caminho: TDD — FORJA FILA: desenho técnico e plano de testes > 2. Contratos das funções (núcleo puro — sem I/O)
    - Assuntos: dict, nao, fila, def, status, painel, cliente, forja_state
    - Trecho-guia: I/O fica em main(): ler JSONs (utf-8-sig, padrão da casa), chamar montarfila, gravar os 3 artefatos (R4) com atomicwritejson do forjan3common.
    - SHA-256 do bloco: `eaec29bf3c36f2caa1879cc907323ace6cad2dc56bac3dc27d59616b38270f7e`
  - [SRC-S004 · L54–L89 · 3. Schema de state/FILAPRIORIZADA.json (canônico)](#src-s004)
    - Caminho: TDD — FORJA FILA: desenho técnico e plano de testes > 3. Schema de state/FILAPRIORIZADA.json (canônico)
    - Assuntos: json, fator, pontos, schema, state, canônico, gestao_escritorio, data
    - Trecho-guia: gestaoescritorio/data/forjafila.json é o MESMO documento (cópia atômica) — o painel não lê de dentro do harness (separação já usada por forjastatus.json).
    - SHA-256 do bloco: `deed327ae756f33ebd5360323f179e98f669d577bc0028973294016d769a6562`
  - [SRC-S005 · L90–L96 · 4. Integração com o painel (renderdashboard.py)](#src-s005)
    - Caminho: TDD — FORJA FILA: desenho técnico e plano de testes > 4. Integração com o painel (renderdashboard.py)
    - Assuntos: painel, integração, novo, json, atual, existentes, renderdashboard, render_dashboard
    - Trecho-guia: Novo bloco secaofila() que lê data/forjafila.json; se ausente, malformado ou flag off → retorna string vazia (painel idêntico ao atual — FILA-R5). Conteúdo: tabela top 5 de producao (posição, título, prazo, score com tooltip dos fatores), linha de resumo ("9 bloqueadas: 4 acesso,
    - SHA-256 do bloco: `33b25ea13ffc275f52680ddfc108b69a50682e235ca0fa149eab803d252f90b5`
  - [SRC-S006 · L97–L110 · 5. Encadeamento com o F0](#src-s006)
    - Caminho: TDD — FORJA FILA: desenho técnico e plano de testes > 5. Encadeamento com o F0
    - Assuntos: fila, encadeamento, main, forja_fila, exc, stderr, fim, forja_reconcile
    - Trecho-guia: No fim de forjareconcile.main() (após gravar o relatório), sob featureenabled("filaPriorizadaV1"):
    - SHA-256 do bloco: `0630981452874758fd970b6800642a5ba1d31b9dac427baa48a2562a9098bd41`
  - [SRC-S007 · L111–L114 · 6. --proxima (FILA-R6)](#src-s007)
    - Caminho: TDD — FORJA FILA: desenho técnico e plano de testes > 6. --proxima (FILA-R6)
    - Assuntos: proxima, fila-r6, exit, python, forja_fila, regenera, fila, imprime
    - Trecho-guia: python forjafila.py --proxima → regenera a fila e imprime JSON de 1 caso (topo de producao): demandaId, caseId, pasta, comando, score, fatores, prazo. Exit 3 se não houver demanda pronta (sinal claro para automação; espelha o padrão exit 2 do forjadelivery).
    - SHA-256 do bloco: `b05aabd27286ada09a479b782289706463dadad5a4d159f1c7201e7fab4cc449`
  - [SRC-S008 · L115–L138 · 7. Plano de testes (testforjafila.py)](#src-s008)
    - Caminho: TDD — FORJA FILA: desenho técnico e plano de testes > 7. Plano de testes (testforjafila.py)
    - Assuntos: prazo, fila, json, painel, não, plano, testes, hoje
    - Trecho-guia: Fixtures 100% sintéticas em tempfile (nenhum caso real, determinismo com hoje fixo).
    - SHA-256 do bloco: `c80caf8b0f524860dd66f306babfbfe23b697bf76cbababed890a026adf61267`
  - [SRC-S009 · L139–L143 · 8. O que este desenho conscientemente NÃO faz](#src-s009)
    - Caminho: TDD — FORJA FILA: desenho técnico e plano de testes > 8. O que este desenho conscientemente NÃO faz
    - Assuntos: não, este, desenho, conscientemente, faz, json, altera, demandas
    - Trecho-guia: Não altera demandas.json, syncforjagestao.py, forjastatus.json nem o fluxo de eventos N3 — superfície de mudança mínima em código que roda em produção. Não cria estado novo por caso — a fila é um documento global, derivado, regenerável. Não usa manual.lastComment no score (texto 
    - SHA-256 do bloco: `9a6c1ccd3d053656b35c851dd13c5b290a0d671d449a4add16234481e4f03b26`

## Conteúdo integral indexado

Os marcadores HTML abaixo são apenas âncoras de navegação. O texto reproduz integralmente a origem normalizada em UTF-8; somente destinos de links relativos podem ter sido recalculados para apontar ao mesmo arquivo a partir desta pasta.

<a id="src-s001"></a>

# TDD — FORJA FILA: desenho técnico e plano de testes

Par do PRD `15_PRD_FILA_PRIORIZADA.md`. Estilo da casa: módulo único, funções puras testáveis, escrita atômica, feature flag, modo sombra primeiro.

---


<a id="src-s002"></a>

## 1. Componentes

| Componente | Arquivo | Natureza |
|---|---|---|
| Motor da fila | `_FORJA_HARNESS/forja_fila.py` | NOVO — módulo único, sem dependência nova |
| Regressão | `_FORJA_HARNESS/test_forja_fila.py` | NOVO — padrão das suítes da casa (script, exit 0/1, DEVE_PEGAR + NÃO_PODE_TRAVAR) |
| Seção no painel | `gestao_escritorio/scripts/render_dashboard.py` | ALTERAÇÃO PEQUENA — bloco isolado com degradação limpa |
| Encadeamento F0 | `_FORJA_HARNESS/forja_reconcile.py` | ALTERAÇÃO MÍNIMA — chamada opcional ao fim do `main()` sob flag |
| Flag | `FORJA_N3_CONFIG.json` → `features.filaPriorizadaV1` | NOVO campo, default `false` até M4 |
| Régua | `forja_regua.py` | adicionar `forja_fila.py` ao manifesto de protegidos |


<a id="src-s003"></a>

## 2. Contratos das funções (núcleo puro — sem I/O)

```python
def classificar_prontidao(demanda: dict, forja_state: dict | None) -> tuple[str, str]:
    """(categoria, motivo). Categorias: pronta | bloqueada_acesso | bloqueada_comando |
    bloqueada_decisao_cliente | bloqueada_pasta | em_producao | aguardando_evidencia.
    Regras, na ordem (primeira que casar vence):
      0. status painel 'pronta_para_revisao'               -> aguardando_revisao_humana
         (gate M0 de 12/07: status real do painel nao previsto no PRD original)
      1. status painel 'cumprida'                          -> fora da fila (não retorna categoria de fila)
      2. FORJA_STATE.currentPhase entre F1 e F9            -> em_producao
      3. FORJA_STATE.status == 'waiting_delivery_evidence' -> aguardando_evidencia
      4. finding P0 PASTA_* ou ORIGEM_AUSENTE no F0        -> bloqueada_pasta
      5. finding P0 COMANDO_AUSENTE no F0                  -> bloqueada_comando
      6. anexos.externosPendentes ou ANEXOS_INCOMPLETOS    -> bloqueada_acesso
      7. proximaAcao contém marcador de decisão do cliente -> bloqueada_decisao_cliente
         (léxico fechado, minúsculo, sem acento-sensível: 'fabio decidir', 'decisao de fabio',
          'aguarda(r) fabio', 'confirmacao do cliente', 'aguarda(r) o cliente', 'autorizacao do cliente')
      8. caso contrário                                    -> pronta
    Léxico da regra 7 é constante do módulo (LEXICO_DECISAO_CLIENTE) — ajustável por edição, testável."""

def pontuar(demanda: dict, hoje: date) -> dict:
    """Retorna {'score': int, 'fatores': [{'fator', 'pontos'}], 'prazoVencido': bool}.
    Tabela normativa do PRD §5. 'hoje' é parâmetro (determinismo em teste).
    Datas malformadas em 'prazo' -> trata como sem prazo e acrescenta fator 'PRAZO_ILEGIVEL' (0 pts)
    para aparecer no relatório (não derruba a fila — lição: reprovação silenciosa não, FILA não trava painel)."""

def ordenar(pontuadas: list[dict]) -> list[dict]:
    """Ordena por score desc; empate: prazo asc (None por último), recebidoEm asc, id asc."""

def montar_fila(demandas: list[dict], states: dict[str, dict], hoje: date) -> dict:
    """Documento canônico da fila (schema §3). Função pura — toda a lógica testável sem disco."""
```

I/O fica em `main()`: ler JSONs (`utf-8-sig`, padrão da casa), chamar `montar_fila`, gravar os 3 artefatos (R4) com `atomic_write_json` do `forja_n3_common`.


<a id="src-s004"></a>

## 3. Schema de `state/FILA_PRIORIZADA.json` (canônico)

```json
{
  "schemaVersion": 1,
  "geradoEm": "2026-07-12T09:00:00-03:00",
  "origem": {
    "demandasPath": "gestao_escritorio/data/demandas.json",
    "demandasSha256": "<hash do arquivo lido — rastreio de divergência painel×fila>",
    "demandasUpdatedAt": "<updatedAt do demandas.json>"
  },
  "producao": [
    {
      "posicao": 1,
      "demandaId": "email-<caso>-<id>",
      "caseId": "case-email-<caso>-<id>",
      "titulo": "...",
      "pasta": "...",
      "prazo": "2026-08-04",
      "prazoVencido": false,
      "score": 63,
      "fatores": [{"fator": "urgenciaManual=alta", "pontos": 40}, {"fator": "prazo<=30d", "pontos": 10}, {"fator": "tag alto valor", "pontos": 10}, {"fator": "idade 3d", "pontos": 3}],
      "comando": "COMANDO_DO_EMAIL.md"
    }
  ],
  "bloqueadas": [
    {"demandaId": "...", "categoria": "bloqueada_acesso", "motivo": "Anexos diretos 5/8 baixados", "score": 50, "aguardandoDesde": null}
  ],
  "emProducao": ["..."],
  "aguardandoEvidencia": ["..."],
  "resumo": {"prontas": 5, "bloqueadas": 9, "emProducao": 2, "aguardandoEvidencia": 3}
}
```

`gestao_escritorio/data/forja_fila.json` é o MESMO documento (cópia atômica) — o painel não lê de dentro do harness (separação já usada por `forja_status.json`).


<a id="src-s005"></a>

## 4. Integração com o painel (`render_dashboard.py`)

- Novo bloco `secao_fila()` que lê `data/forja_fila.json`; se ausente, malformado ou flag off → retorna string vazia (painel idêntico ao atual — FILA-R5).
- Conteúdo: tabela top 5 de `producao` (posição, título, prazo, score com tooltip dos fatores), linha de resumo ("9 bloqueadas: 4 acesso, 3 decisão do cliente, 2 comando"), badge amarelo para `aguardandoDesde` > 48h (FILA-R7) e vermelho para `prazoVencido`.
- Estilo: reusar tokens visuais existentes do painel (identidade Medina Osório já embutida) — **nenhum CSS novo além de classes existentes**.
- Aviso de frescor: se `origem.demandasUpdatedAt` ≠ `updatedAt` atual do `demandas.json`, mostrar "fila desatualizada — regenerar" (mitiga risco de divergência do PRD §7).


<a id="src-s006"></a>

## 5. Encadeamento com o F0

No fim de `forja_reconcile.main()` (após gravar o relatório), sob `feature_enabled("filaPriorizadaV1")`:

```python
try:
    import forja_fila
    forja_fila.main(hoje=None)  # usa data corrente em produção
except Exception as exc:
    print(f"[fila] falhou sem bloquear o F0: {exc}", file=sys.stderr)
```

Falha da fila NUNCA derruba o reconcile (fila é derivada; o F0 é autoridade). O erro sai em stderr e o painel mostra a fila anterior com aviso de frescor.


<a id="src-s007"></a>

## 6. `--proxima` (FILA-R6)

`python forja_fila.py --proxima` → regenera a fila e imprime JSON de 1 caso (topo de `producao`): `demandaId`, `caseId`, `pasta`, `comando`, `score`, `fatores`, `prazo`. Exit 3 se não houver demanda pronta (sinal claro para automação; espelha o padrão exit 2 do `forja_delivery`).


<a id="src-s008"></a>

## 7. Plano de testes (`test_forja_fila.py`)

Fixtures 100% sintéticas em `tempfile` (nenhum caso real, determinismo com `hoje` fixo).

**DEVE_PEGAR (detecções):**
1. Demanda com `externosPendentes=true` classificada `bloqueada_acesso`, nunca `pronta`.
2. Sem `COMANDO_*.md` (finding F0) → `bloqueada_comando`.
3. `proximaAcao` = "aguardar decisão de Fábio sobre proposta" → `bloqueada_decisao_cliente`.
4. Espera > 48h → campo `aguardandoDesde` preenchido e destaque (R7).
5. Prazo vencido → `prazoVencido=true`, score de prazo máximo, permanece na fila (nunca some).
6. `demandas.json` alterado após gerar fila → hash de origem diverge (detectável pelo aviso de frescor).
7. Data de prazo malformada → fator `PRAZO_ILEGIVEL`, sem exceção.

**NÃO_PODE_TRAVAR (não-travas):**
8. Demanda limpa (comando presente, anexos completos, sem pendência de cliente) → `pronta`.
9. Score reproduzível: duas execuções com mesmo input → JSON idêntico (exceto `geradoEm`).
10. Ordem: urgência alta + prazo 5d vence urgência média + prazo 2d (40+30 > 20+40); empate exato resolve por prazo→recebidoEm→id.
11. Anti-inanição: baixa prioridade com 30 dias soma +10 e entra no top 10 da fixture (R8).
12. `demandas.json` intocado: bytes idênticos antes/depois de `montar e gravar` (R1).
13. Fila vazia (todas cumpridas) → documento válido com listas vazias, painel degrada limpo, `--proxima` exit 3.
14. Flag off → `forja_reconcile` não gera fila e painel não muda (R9).

**Painel (gate manual no M2, não automatizável):** QA visual da seção nova + confirmação de que o painel sem `forja_fila.json` renderiza como hoje (screenshot antes/depois).


<a id="src-s009"></a>

## 8. O que este desenho conscientemente NÃO faz

- Não altera `demandas.json`, `sync_forja_gestao.py`, `forja_status.json` nem o fluxo de eventos N3 — superfície de mudança mínima em código que roda em produção.
- Não cria estado novo por caso — a fila é um documento global, derivado, regenerável.
- Não usa `manual.lastComment` no score (texto livre de humano; léxico fechado só na `proximaAcao`, que já é campo operacional).
