# W0 — baseline vivo, freeze e migração do modelo editorial

**Data:** 25/07/2026
**Cânone executado:** `planejamento/33`, `34` e `35`, acrescidos da seção 9 do `36` (emendas E1–E16)
**Escopo desta onda:** E16 (baseline pela Régua), E9 e E10 (citação regimental), E11 (regimentos), E14/M1–M9 (modelo editorial)
**Estado:** concluída, com as pendências nominadas na seção 7

---

## 1. Baseline vivo — o número e o que ele significa

A emenda E16 exigiu registrar **quais suítes** compõem o número declarado, porque `104 passed` e `131 passed` circulavam como se fossem comparáveis. Não eram: mediam seleções diferentes.

Ao levantar isso, apareceu um problema maior que a ambiguidade.

**Cinco das trinta e seis suítes não executavam sob `pytest`.** São regressões escritas como script autônomo, que comunicam o veredito pelo código de saída:

| Suíte | O que guarda |
|---|---|
| `test_forja_verificador.py` | gates determinísticos das 30 lições de `RETROSPECTIVAS.md` |
| `test_forja_citacoes.py` | veneno de citação — taxonomia U1 em seis modos de falha |
| `test_forja_regua.py` | sabotagem da Régua — cinco fraudes simuladas |
| `test_forja_fila.py` | priorização e prontidão da fila |
| `test_forja_conselho_1107.py` | gates do conselho de 11/07/2026 |

Sob `pytest` elas reportavam `no tests ran`. Pior: `test_forja_verificador.py` substitui `sys.stdout` no nível de módulo, o que **derrubava a coleta conjunta inteira** com `ValueError: I/O operation on closed file` — motivo pelo qual todo baseline histórico usou seleção nomeada e nenhum incluiu estas cinco.

Nenhuma delas estava quebrada: as cinco passam quando executadas do jeito certo. O defeito era de porta de entrada, não de qualidade.

**Correção:** `forja_baseline.py`, porta única que executa as duas famílias — pytest suíte a suíte, scripts como subprocesso — e emite relatório nominal em JSON.

```
36/36 suítes verdes · 316 testes pytest (+8 subtests) · 5 regressões em script
```

Relatório: `reports/BASELINE_W0_FINAL_2026-07-25.json`. O número inicial da onda foi 305 testes; os 11 acrescidos são a cobertura nova descrita adiante.

## 2. Régua — desvio classificado, sem rebaseline

A Régua reprovou por integridade no início e ao fim da onda. **Nenhum rebaseline foi executado**, conforme a regra do roadmap.

**Desvio preexistente (8 arquivos), classificado:** implementação do protocolo `FORJA-GOSTO-EDGE-v1` de 24/07/2026 mais dois filtros anti-clichê, em `forja_estilo_humano.py`, `forja_fable5.py`, os dois testes correspondentes, os dois protocolos e os dois prompts do auto-research. Alteração revisada adversarialmente, com as quatro suítes correspondentes verdes.

**Desvio desta onda (6 arquivos):** `forja_verificador.py`, `forja_run.py`, `forja_editorial_fidelity.py`, `forja_package.py`, `phase_contracts/F7.json` e `test_forja_verificador.py`.

O rebaseline dos catorze é decisão do titular, com motivo escrito, após revisão — não é ato do executor.

## 3. E14 — migração do modelo editorial (M1 a M9)

**A armadilha era real e foi medida antes de qualquer edição.** `forja_fable5.py:343` levantava erro duro quando o envelope não comprovasse `claude-fable-5`, e `forja_editorial_fidelity.py:170` comparava com a mesma constante literal. Alterar o `CLAUDE.md` antes do código teria parado toda demanda em F7. A ordem M1–M7 → protocolo → M8/M9 foi cumprida na íntegra.

**Princípio da migração: parametrizar, não reescrever.** O que tinha valor não era o nome do modelo — era a recusa em aceitar a autodeclaração dele. Isso ficou intacto.

| Passo | Entrega |
|---|---|
| M1 | `forja_editorial_model.py`: allowlist com `claude-opus-5` (padrão), `claude-fable-5` (legado) e `gpt-5.6-sol` (revisor sem executor local) |
| M2 | a assertiva dura passou a comparar com o modelo declarado no contrato do run |
| M3 | idem em `forja_editorial_fidelity.py`, agora contra allowlist ou modelo esperado |
| M4 | `producerModel` e `reviewerModel`, cada um com `canonicalId`, `family` e `sessionId` |
| M5 | `familyAssurance` com `cross_family`, `cross_session_same_family` e `unverified` |
| M6 | gate `fable5_oauth_confirmed` → `editor_model_confirmed`; **novo** `cross_model_review_verified` em `phase_contracts/F7.json` |
| M7 | `FABLE5_RESULT*.json` → `EDITORIAL_RESULT*.json`; `fable5_usage` → `editor_usage` |
| M8 | `PROTOCOLO_FABLE5_ESCRITA_FINAL.md` → `PROTOCOLO_EDITORIAL_ESCRITA_FINAL.md`, com a supersessão datada na seção 0 |
| M9 | **não executado** — ver seção 7 |

**Retrocompatibilidade num só lugar.** `LEGACY_NAMES` e `resolve_name()` em `forja_n3_common.py` mapeiam nome corrente → nomes anteriores. Escritores emitem só o nome novo; a resolução acontece na leitura, em `forja_run.py` (gates e saídas obrigatórias) e em `_artifact()` de `forja_package.py` — este último faz com que todo consumidor do pacote herde a compatibilidade de uma vez, sem duplicar artefato.

**Sobre a garantia de independência.** Ela é recomposta das fichas dos dois modelos, não lida do campo declarado: declarar `cross_family` sem segunda família não compra liberação. Bundles anteriores a esta emenda não trazem as fichas e ficam em `unverified`, que bloqueia — comportamento correto, porque a independência daquelas execuções de fato não foi verificada.

**Cobertura nova:** 11 testes em `test_forja_fable5.py` (11 → 22), incluindo modelo fora da allowlist, modelo reconhecido sem executor local, envelope de modelo divergente do contrato, os três níveis de garantia, garantia declarada a maior, recusa da degradação em modo estrito e leitura de nome legado.

## 4. E9 — gate G11 de citação regimental

Todo `art. X do RI<Tribunal>` no texto exige verbatim arquivado em `cache/fontes_oficiais/`. Sem lastro, P0. Com lastro sem data de conferência, P1 — regimento é norma mutável e lastro sem data não sustenta citação.

Duas exigências independentes, e ambas nasceram de defeitos encontrados durante a implementação:

1. **O tribunal é reconhecido pelo nome do arquivo, nunca por menção no corpo.** A primeira versão dava por lastreado um dispositivo do TJTO porque o arquivo do RISTJ citava o TJTO de passagem.
2. **O lastro é a linha que define o dispositivo** — `Art. 343-A. Nos termos…` — e não qualquer menção a ele. A primeira versão aceitava como transcrição a prosa de um comentário sobre o artigo. O defeito foi encontrado pela própria regressão, depois que uma frase explicativa que escrevi no arquivo de cache virou falso lastro.

Medido contra 23 markdowns reais do acervo: **zero falso positivo**.

## 5. E10 — âmbito da citação

Já estava implementado em `forja_verificador.py` desde 10/07/2026: citar `art. 343-A` em peça a TJ ou TRF é P0, porque aqueles tribunais não se regem pelo RISTJ. A prática da síntese executiva permanece obrigatória em toda peça por determinação do escritório; a citação numérica, só ao STJ.

**Varredura do acervo:** as citações reais ao art. 343-A estão na peça do Cafelana ao STJ, onde são corretas. As ocorrências no auto-research são material interno e já se dizem "adaptado". **O risco P0-a não se materializou em peça protocolada.**

## 6. E11 e a correção de um diagnóstico meu

**Registro o erro porque ele muda como o próximo alarme deve ser tratado.**

O documento `36`, §3, e o parecer do Cícero afirmaram que o falso alarme de 25/07 se explicava por regimentos arquivados "consolidados até a ER 47/2024, com as emendas apenas listadas ao final". **Isso estava errado.**

A auditoria de 10/07/2026 já havia: registrado a ER 53/2026 nos quatro `REGIMENTO_INTERNO_STJ.md`, arquivado o PDF oficial do DJe em `cache/fontes_oficiais/STJ_ER_53_2026_DJe_2026-07-01.pdf` e corrigido a regra do verificador que negava a existência do artigo. O alarme de 25/07 foi **redundante**: reabriu, com custo, uma questão já resolvida quinze dias antes.

O que de fato faltava era menor e específico: o dispositivo constava como **descrição em prosa na seção de complementos**, não como **texto de artigo no corpo articulado**. Quem lesse o regimento em ordem, entre os arts. 343 e 344, não o encontrava.

**Corrigido:** o caput foi incorporado ao corpo dos quatro arquivos, entre os arts. 343 e 344, com nota de origem e data de conferência. E a pendência de ledger que eu havia declarado em aberto foi **encerrada contra a fonte primária**: o texto confere caractere a caractere com o PDF do DJe n. 4336, disponibilização 30/06/2026, publicação 01/07/2026.

**Lição operacional, gravada em memória:** antes de tratar uma citação como suspeita, ler a seção de complementos do regimento e o `cache/fontes_oficiais/`. O G11 agora torna esse hábito verificável.

## 7. Pendências nomeadas

| # | Pendência | Por quê |
|---|---|---|
| 1 | **M9** — renomear `forja_fable5.py` → `forja_editorial.py` com shim | é a maior superfície e o menor valor dos nove passos; o módulo já não depende de nome de modelo. Fazê-lo ao lado do rebaseline da Régua, em mudança isolada |
| 2 | **E11 para 12 regimentos não-STJ** | TRF1 ×2, TRF2, TRF4 ×3, TJTO, TJRJ, TJSP, TJDFT, TRE-PR. Exige diários eletrônicos de cada tribunal. Até lá, o G11 bloqueia — corretamente — citação a esses regimentos |
| 3 | **Rebaseline da Régua** | catorze arquivos alterados, todos classificados acima. Decisão do titular, com motivo escrito |
| 4 | **`PROTOCOL_VERSION` ainda é `FORJA-FABLE5-FINAL-v1`** | mantido de propósito: mudá-lo invalidaria os bundles já promovidos, que comparam a constante por igualdade. Trocar exige aceitar as duas versões na leitura, e isso não estava no escopo M1–M9 |

## 8. Verificação executada

```
python forja_baseline.py     → 36/36 suítes verdes · 316 testes · APROVADO
python forja_regua.py        → reprovado por integridade; 14 desvios classificados, sem rebaseline
python test_forja_verificador.py → 21 detecções + 17 não-travas
gate G11 sobre 23 peças reais    → zero falso positivo
art. 343-A × PDF oficial do DJe  → coincidência literal
```

Nenhum caso foi executado, promovido ou entregue durante esta onda. Nenhuma ação externa foi disparada.
