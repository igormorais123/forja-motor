# TDD — FORJA FILA: desenho técnico e plano de testes

Par do PRD `15_PRD_FILA_PRIORIZADA.md`. Estilo da casa: módulo único, funções puras testáveis, escrita atômica, feature flag, modo sombra primeiro.

---

## 1. Componentes

| Componente | Arquivo | Natureza |
|---|---|---|
| Motor da fila | `_FORJA_HARNESS/forja_fila.py` | NOVO — módulo único, sem dependência nova |
| Regressão | `_FORJA_HARNESS/test_forja_fila.py` | NOVO — padrão das suítes da casa (script, exit 0/1, DEVE_PEGAR + NÃO_PODE_TRAVAR) |
| Seção no painel | `gestao_escritorio/scripts/render_dashboard.py` | ALTERAÇÃO PEQUENA — bloco isolado com degradação limpa |
| Encadeamento F0 | `_FORJA_HARNESS/forja_reconcile.py` | ALTERAÇÃO MÍNIMA — chamada opcional ao fim do `main()` sob flag |
| Flag | `FORJA_N3_CONFIG.json` → `features.filaPriorizadaV1` | NOVO campo, default `false` até M4 |
| Régua | `forja_regua.py` | adicionar `forja_fila.py` ao manifesto de protegidos |

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
      "demandaId": "email-corsan-agerst-19f3dc9ff92081cd",
      "caseId": "case-email-corsan-agerst-19f3dc9ff92081cd",
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

## 4. Integração com o painel (`render_dashboard.py`)

- Novo bloco `secao_fila()` que lê `data/forja_fila.json`; se ausente, malformado ou flag off → retorna string vazia (painel idêntico ao atual — FILA-R5).
- Conteúdo: tabela top 5 de `producao` (posição, título, prazo, score com tooltip dos fatores), linha de resumo ("9 bloqueadas: 4 acesso, 3 decisão do cliente, 2 comando"), badge amarelo para `aguardandoDesde` > 48h (FILA-R7) e vermelho para `prazoVencido`.
- Estilo: reusar tokens visuais existentes do painel (identidade Medina Osório já embutida) — **nenhum CSS novo além de classes existentes**.
- Aviso de frescor: se `origem.demandasUpdatedAt` ≠ `updatedAt` atual do `demandas.json`, mostrar "fila desatualizada — regenerar" (mitiga risco de divergência do PRD §7).

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

## 6. `--proxima` (FILA-R6)

`python forja_fila.py --proxima` → regenera a fila e imprime JSON de 1 caso (topo de `producao`): `demandaId`, `caseId`, `pasta`, `comando`, `score`, `fatores`, `prazo`. Exit 3 se não houver demanda pronta (sinal claro para automação; espelha o padrão exit 2 do `forja_delivery`).

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

## 8. O que este desenho conscientemente NÃO faz

- Não altera `demandas.json`, `sync_forja_gestao.py`, `forja_status.json` nem o fluxo de eventos N3 — superfície de mudança mínima em código que roda em produção.
- Não cria estado novo por caso — a fila é um documento global, derivado, regenerável.
- Não usa `manual.lastComment` no score (texto livre de humano; léxico fechado só na `proximaAcao`, que já é campo operacional).
