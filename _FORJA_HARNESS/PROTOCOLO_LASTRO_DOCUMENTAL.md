# Protocolo de lastro documental — FORJA-LASTRO-v2

Módulo: `forja_lastro.py`. Regressão: `test_forja_lastro.py` (92 verificações de script, no baseline e na régua rápida). Catálogo: § U12 e § U13 de `planejamento/06_GATES_QUALIDADE_FORJA.md`. Incidentes: `INCIDENTE_VALE_TRADING_LASTRO_APARENTE_2026-07-26.md` e o incidente Cafelana de 02/08/2026.

Criado em 26/07/2026 por ordem do Igor, depois de alucinações de nível moderado a grave no caso Vale Trading.

## 1. Finalidade

Impedir que uma proposição jurídica entre em peça, parecer ou ledger **afirmando lastro documental que ninguém verificou**.

O modo de falha não é inventar do nada. É a afirmação bem escrita, com status `confirmed_document` e localizador plausível — página, evento, ID —, cuja fonte diz o contrário. O texto passa em qualquer revisão textual porque o defeito não está no texto.

> **Eixo do protocolo: citar o localizador não é ter lido o localizador.**

A consequência prática é que a única prova barata de leitura é a **transcrição verbatim**. Um modelo que precisa apenas indicar a página pode produzi-la com aparência perfeita; um modelo obrigado a colar o trecho tem de abrir a fonte. Daí a exigência central do L1.

## 2. Regra da casa que este protocolo respeita

Gate novo exige **falha observada**, nunca hipótese (regra herdada do ciclo AR, `planejamento/22_PRD_AUTORESEARCH_FORJA.md`). Os treze gates funcionais L1–L13 abaixo têm cada um uma âncora real da execução de 26/07/2026 ou 02/08/2026. Guardas L0 e de conferência operacional acrescentam fail-closed quando o insumo é vazio, desconhecido ou inválido. Não há gate especulativo neste módulo, e nenhum deve ser acrescentado sem falha nominada.

## 3. Os treze gates funcionais

| Gate | Severidade | O que exige | Âncora real |
|---|---|---|---|
| **L1-lastro** | P0 | fato com status documental precisa de localizador **e** transcrição verbatim (mín. 25 caracteres normalizados) | F012 marcado `confirmed_document` sem transcrição; a fonte dizia o oposto |
| **L1-lastro-pendente** | P1 | mesma exigência, quando a falta é **declarada** com `groundingPending: true` | pendência honesta não pode receber a mesma pena da invenção |
| **L2-transcricao** | P0 | havendo transcrição e fonte alcançável, o trecho tem de existir mesmo naquele arquivo | trecho reconstruído de memória com aparência de citação |
| **L3-superlativo** | P0 / P1 | não conhecimento e confirmação no mesmo documento é P0; declaração de estabilidade sem nomear a categoria é P1 | "confirmada em todas as instâncias" sobre REsp **não conhecido** |
| **L4-denominador** | P1 | percentual precisa nomear a base exata | "93% dessa distância" — denominador trocado no meio da frase |
| **L5-identidade** | P0 | afirmar mesma liquidação/execução/título/autos exige os **dois** números CNJ na janela de ±400 caracteres | § 16: "mesmas partes e a mesma liquidação" — eram liquidações distintas |
| **L6-norma-por-ano** | P0 | norma citada só pelo ano precisa estar nomeada no texto (Lei/Decreto/IN + número + ano) | "normas de 2002, 2016 e 2018" — a de 2018 não existia |
| **L7-criterio-vigente** | P0 | em liquidação ou cumprimento, o ledger precisa ter um fato `role: criterio_vigente` **com transcrição** | recomendação de base de cálculo contra critério já fixado nos autos |
| **L8-objecao** | P0 | objeção externa acatada contra afirmação **com** lastro exige reabertura da fonte | objeção de revisor externo acatada contra minuta que estava certa |
| **L9-fonte-prevalente** | P0 | produto econômico exige fato `role: fonte_prevalente`, validação humana nominal e SHA-256 conferida no arquivo em disco | faixas em reais produzidas sem documento governante |
| **L10-data-base** | P0 | data-base expressa no produto coincide com a do fato prevalente, após normalização mensal | referência histórica usada no lugar da base do laudo |
| **L11-valor-orfao** | **P1** (medido) | valor calculado tem âncora na tabela U6 ligada à fonte prevalente; valor citado de terceiro só é exceção com origem declarada | números circularam sem fonte autorizadora |
| **L1-status-desconhecido** | P1 | status de fato que o gate não conhece é anunciado, para que "não auditado" nunca se pareça com "aprovado" | ledger da Cafelana: 0 de 11 fatos examinados por divergência de vocabulário |
| **L2-transcricao-manual** | P1 | fonte binária ou acima de 8 MB é declarada não conferível automaticamente, e não acusada de invenção | laudo prevalente de 2,14 GB; transcrição correta de PDF acusada de reconstrução de memória |
| **L12-hierarquia-fonte** | P0 | inventário físico do caso é confrontado com a fonte eleita; concorrente posterior/superior é eleito ou descartado por escrito | laudo disponível na pasta não eleito |
| **L13-aritmetica-derivada** | P0 | valor/faixa derivado é recomposto contra base, percentual, resultado e tolerância declarados | requisito 5: impedir número incompatível com premissa validada |

### Guardas de integridade e descoberta

Estes identificadores não substituem L1–L13; impedem que um caminho de erro pareça aprovação:

| Guarda | Severidade | Regra |
|---|---|---|
| **L0-ledger-vazio** / **L0-ledger-vocabulario** | P0 | ledger sem `facts`, com chave alternativa ou item fora do objeto não é “limpo”; é insumo não examinado |
| **L1-status-ausente** | P1 | fato sem status explícito não é isento por omissão |
| **L0-recomputo-sem-insumo** | P0 | `fact_ledger.json` inválido, fora do schema ou não legível produz `computed.status: fail`; o verificador não cai em snapshot histórico |
| **L0-economico-desativado** | P0 | caller não pode desligar L9–L13 (`exigir=False`) quando o texto contém material econômico; a tentativa é um bypass de lastro |
| **L11-isencao-tipografica** | P2 | `>` ou aspas sem origem declarada não isentam o valor: deixam recibo P2 e o valor continua na conferência de âncora |

O canônico inválido interrompe a descoberta em `_carregar_contexto_lastro()`; snapshots `fact_ledger-*.json` só são considerados quando não existe `fact_ledger.json` canônico. Um `ledger_path` explicitamente fornecido — inexistente, diretório ou ilegível — também encerra a rota direta `PecaVisual`, sem autodiscovery alternativo; a ausência de caminho, por outro lado, é a única situação que autoriza a descoberta no `case_dir`. Nessa falha, o verificador devolve `L9-fonte-prevalente` P0 com ledger vazio; não há novo identificador de gate. Essa fronteira reúne as contraprovas `MC-18` e `MC-22` do `FAILURE_TAXONOMY.md`.

O parâmetro `exigir=False` não é uma exceção de governança: se `material_economico(texto)` for verdadeiro, `validar_gates_economicos()` emite `L0-economico-desativado` P0 e não produz aprovação vazia. A contraprova está na regressão T2; texto sem material econômico continua sem L9–L13.

### Notas de leitura de cada gate

**L1 e L2 (ledger).** Só valem para os status que afirmam lastro: `confirmed_document`, `confirmed_official_source`, `documented_fact`, `official_current_source`, `PROVADO`, `CONFLITANTE`. `legal_inference`, `strategic_hypothesis`, `documented_strategy`, `not_verified`, `blocked` e `pending` são honestos sobre o que são e passam intactos — o protocolo não persegue hipótese assumida, persegue hipótese vestida de fato. O parâmetro `exigir_transcricao=False` rebaixa L1 a P1 para ledger legado, que não pode ser reprovado retroativamente.

> **Por que as duas listas são explícitas, e por que existe um gate para o que sobra.** Em 04/08/2026, ao medir o L1/L2 recém-computado contra o ledger real da Cafelana, o resultado foi **0 de 11 fatos auditados**: o caso escrevia `documented_fact` e `official_current_source`, o gate conhecia os prefixos `confirmed_`. Ele percorria os 11, pulava todos e devolvia aprovação **com saída idêntica à de um ledger integralmente conferido**. Acrescentar os sinônimos resolve o caso; declarar as duas listas e emitir `L1-status-desconhecido` para o que não está em nenhuma resolve a classe. Vocabulário novo vai surgir de novo — o que não pode voltar é ele significar aprovação. Uma terceira camada da mesma divergência: os fatos usam `locator` + `quoteSource` + `sha256`, e o gate exigia a palavra `support`, reprovando em P0 seis fatos bem formados. Localizador agora é reconhecido por qualquer um desses campos.
>
> **L2 e fonte não textual.** A conferência só é tentada em extensão de texto conhecida e abaixo de 8 MB. Antes disso o gate lia qualquer arquivo como UTF-8 e, não achando o trecho no binário, emitia P0 dizendo que a transcrição "pode ter sido reconstruída de memória" — a acusação mais grave do módulo, contra quem transcreveu corretamente de um PDF. Fonte não conferível vira `L2-transcricao-manual` em P1: o gate declara que não sabe, em vez de fingir que sabe.

**L3.** A coocorrência dos dois campos semânticos no mesmo documento é bloqueadora porque, se ambos estão lá, o texto está afirmando em algum ponto que um não conhecimento confirmou algo. A troca correta é "via recursal esgotada, acórdão incólume". Os superlativos isolados ("questão encerrada", "incontroverso", "em definitivo") não são proibidos: são P1 e pedem que se nomeie a categoria — coisa julgada material, preclusão, estabilidade de interlocutória ou esgotamento da via.

**L5.** Identidade processual é conclusão jurídica sobre dois documentos, jamais semelhança percebida. Por isso a exigência é de dois identificadores à vista, não de convicção.

**L7.** Não é um gate sobre o texto: é sobre a existência de um registro. Se o estado do caso não diz qual decisão fixa **hoje** o critério em disputa, a peça está opinando no escuro.

**L8.** Convergência entre revisores não substitui a fonte. O revisor externo, por definição, não tem os autos.

## 4. Duas regras de calibração

Ambas nasceram de erro do próprio gate e valem para qualquer gate futuro da FORJA.

**Pendência declarada é P1.** `groundingPending: true` mantém o bloqueio de promoção, mas não é tratado como alucinação. Punir a honestidade com a mesma severidade da invenção ensina o sistema a fabricar transcrição para deixar o gate verde — exatamente o comportamento que o protocolo existe para desencorajar.

**Severidade se mede, não se estima — e a medição pode rebaixar o gate.** O L11 foi projetado como P0 e **nasceu em P1**. A calibração de 04/08 (`forja_calibra_gates_economicos.py`, 2.286 documentos, 2.491 valores) mostrou que a separação entre valor que a peça CITA e valor que ela CALCULA reconhecia só 2,9% como citação; corrigidas duas causas nominais — aspas retas não eram aceitas, e não havia marcador de origem alheia nem de limiar normativo — subiu para 6,9%, e uma amostra de 20 classificada à mão ainda deu **~55% de falso positivo**. A tentação de continuar mexendo na heurística até o número agradar é a autovalidação circular que este protocolo existe para impedir: quem escreve o gate escolhe a métrica e ajusta até passar. A regra que fica: **gate cuja calibração não fecha entra em P1 com caso de regressão fixando a severidade**, para que a promoção a P0 seja uma decisão medida e não um efeito colateral silencioso.

**Negação nunca trava.** O L5 chegou a bloquear "não se trata da mesma liquidação", que é a correção desejada. A detecção usa `_negado()` sobre uma janela curta (45 caracteres) antes da afirmação — janela curta de propósito, para que um "não" distante no parágrafo não limpe o gate. As duas frases reais corrigidas do caso estão fixadas na lista `NAO_PODE_TRAVAR` da regressão. **Um auditor que reprova o acerto é desligado na terceira vez** — por isso 11 casos lexicais da regressão são não-travas, além das contraprovas específicas dos gates econômicos.

## 5. Uso

### Linha de comando

```powershell
python forja_lastro.py <arquivo.md> [--ledger fact_ledger.json] [--base-dir DIR] [--revisao revisao.json] [--exigir-criterio]
```

Saída em JSON: `arquivo`, `versao`, `total`, `p0` e a lista de achados. Cada achado traz `gate`, `sev`, `problema`, `acao` e o `trecho` com contexto.

- `--base-dir` liga o L2: sem ele, a transcrição é exigida mas não conferida contra a fonte.
- `--exigir-criterio` liga o L7. Use em liquidação e cumprimento de sentença.

### Como biblioteca

```python
from forja_lastro import (
    analisar_texto,            # L3-L6 sobre qualquer texto
    validar_lastro_fatos,      # L1-L2 sobre o ledger
    exigir_criterio_vigente,   # L7
    validar_decisoes_revisao,  # L8
    fatos_sem_lastro,          # lista de ids bloqueantes, usada pela entrega
    verificar_tudo,            # conveniência: roda o que o material permitir
)
```

### Campos que o ledger precisa ter

| Campo | Aceita também | Função |
|---|---|---|
| `id` | `factId` | identificação do fato |
| `status` | `classification` | decide se o fato entra nos gates |
| `support` | `sources` | localizador |
| `quote` | `trechoSuporte` | **a transcrição verbatim** |
| `quoteSource` | `arquivoFonte` | caminho relativo a `--base-dir`, para o L2 conferir |
| `groundingPending` | — | declara honestamente que a fonte não foi reaberta |
| `role: criterio_vigente` | `papel` | marca a decisão que fixa o critério hoje (L7) |

Para a revisão externa (L8), cada objeção precisa de `id`, `decision` (`acatada`/`rejeitada`/`parcial`), `targetHadSupport` e `sourceReopened`.

## 6. Onde o gate está acoplado

Importável não é acoplado. O bloco final da regressão verifica os quatro pontos de ligação abaixo — mas **verificar a ligação não é verificar o cálculo**, e a distinção custou caro.

> ⚠ **Correção de 03/08/2026 — declarado ≠ computado.** Uma revisão adversarial mediu quem chama cada função em produção. Resultado: **`validar_lastro_fatos` (L1/L2), `exigir_criterio_vigente` (L7) e `validar_decisoes_revisao` (L8) não têm chamador nenhum fora de `test_forja_lastro.py`.** Da produção sobrevivem `analisar_texto` (L3–L6, pelo verificador) e `fatos_sem_lastro` (elo 9-B da entrega). O ponto 1 abaixo é **declarativo**: `forja_run._validate_result` confere `requiredGates` lendo o campo `gates` do `PHASE_RESULT.json`, que é escrito pelo próprio agente da fase — de modo que o `fact_grounding_verbatim` está declarado no contrato e não é calculado por ninguém. A blindagem certa foi escrita em julho e ficou majoritariamente fora da estrada. Ligar isso é o passo 1 do plano 41, anterior a qualquer gate novo: **acrescentar gate a contrato que ninguém computa aumenta a autoatestação em vez de reduzi-la.**

1. **`phase_contracts/F7.json`** — `fact_grounding_verbatim` nos `requiredGates` (agora 21), com a âncora registrada em `gateNotes`.
2. **`forja_delivery.py`** — elo bloqueante **9-B**: `fatos_sem_lastro()` impede o fechamento da demanda enquanto houver fato de status documental sem transcrição, ainda que a pendência esteja declarada.
3. **`forja_visual_build.py` + `forja_visual.compor()` + `forja_svg_docx.inserir_svgs()`** — a entrada oficial da FORJA roda o verificador com contexto documental antes da composição, persiste no template, embute SVG nativo no OOXML e executa QA estrutural; `forja_render_docx.py` está fora da FORJA e não é rota de produção.
4. **`forja_baseline.py` e `forja_regua.py`** — `test_forja_lastro.py` no registro `SUITES_SCRIPT` e na régua rápida, porque é regressão em script e o pytest não a coletaria; o módulo e a suíte também estão no manifesto de hashes protegidos.
5. **`forja_memoria_auditabilidade.py` e `forja_delivery.py`** — a entrega gera e valida a memória sanitizada de processo em Markdown, HTML e manifesto JSON; o elo 13 bloqueia o fechamento quando qualquer derivado ou hash do estado estiver ausente. O gerador normaliza aliases históricos de F0–F10 para os IDs canônicos de `phase_contracts`, inclusive na fase corrente e no histórico; a saída não pode transformar fase concluída em `not_started` por divergência nominal (`MC-20`).

## 7. O que estes gates não fazem

São escudos **lexicais e estruturais**. Eles obrigam a colar o trecho e conferem que o trecho está no arquivo apontado. Não julgam se o trecho **sustenta** a proposição — isso é leitura jurídica, e continua sendo trabalho da auditoria F7 e do revisor humano.

Passar em FORJA-LASTRO-v2 significa apenas que a peça satisfez os requisitos lexicais/estruturais aplicáveis: ninguém afirmou lastro sem colar prova de leitura e, quando há material econômico, a fonte e a âncora foram registradas e conferidas. Não significa que a peça está certa.

## 7-A. Extensão implementada — v2, fonte prevalente e valor monetário (04/08/2026)

O incidente Cafelana de 02/08/2026 (e-mail do Fábio, thread `19fbfa33e7ce7df9`) expôs o complemento deste módulo: **o v1 ancora proposição, não número.** Faixas em reais foram produzidas sem que nenhum documento tivesse sido declarado governante da base econômica, e nenhum gate perguntou "qual arquivo autoriza estes números e em que data-base?".

A extensão acrescenta L9 (fonte prevalente validada), L10 (data-base coincidente), L11 (valor monetário sem âncora), L12 (hierarquia física) e L13 (recomputo aritmético), **aqui dentro** e não em módulo próprio. A fonte prevalente entra como fato com `role: fonte_prevalente` — mesmo mecanismo do `criterio_vigente` do L7, que já resolve "qual registro governa hoje". A incidência é estreita e reexecutável por `material_economico()`; número com separador de milhar sem marcador de moeda não aciona a família. Plano completo, com sequência e critérios: `planejamento/41_PLANO_GATE_DOCUMENTAL_E_REGRESSAO_FONTE_PREVALENTE.md`; catálogo: § U13 de `planejamento/06_GATES_QUALIDADE_FORJA.md`.

O limite do § 7 vale integralmente para os gates novos: eles conferem que o número tem âncora declarada e íntegra, **não** que a fonte sustenta o número.

## 8. Como estender

1. A falha tem de ser **real e nominada** — caso, data, trecho.
2. Todo gate novo entra com **dois** casos na regressão: um que ele deve detectar e outro que ele não pode bloquear (recall sem especificidade premia trava excessiva — Lição 70).
3. Se o gate puder ser satisfeito por algo que a IA escreve livremente, ele não é gate: é declaração. A transcrição funciona porque exige o trabalho; o localizador não funciona porque não exige.
4. Registrar a âncora no docstring do módulo e a linha correspondente em § U12 do catálogo de gates.

### 8.1. Campos do ledger v2

O fato prevalente usa os campos `role: fonte_prevalente`, `dataBase`, `sha256`,
`validationStatus`, `validadoPor`, `validadoEm`, `quoteSource`/`arquivoFonte` e
`documentosExaminados[]` no cabeçalho do ledger. A tabela U6 pode registrar
`monetaryAnchors[]` (ou `economicAnchors[]`), cada entrada contendo o valor e
uma referência ao fato prevalente. Memórias de cálculo derivadas entram em
`derivedCalculations[]` com `baseValue`, `percentage`, `expectedValue` e
`tolerance`. Nenhum desses campos substitui a leitura jurídica da fonte.

### 8.2. Incidência e rotas

Os gates L9--L13 são calculados pela entrada visual canônica
(`forja_visual_build.py`), pelo verificador chamado nessa entrada, pelo
runner F7 (`forja_run._compute_lastro_gates`) e pela persistência visual
`PecaVisual.salvar()`. A rota `forja_delivery` repete a prova no elo 9-B. A
entrada visual única e o script ad hoc são pontos distintos: todos precisam
falhar fechados. A materialização usa somente `forja_svg_docx` e QA OOXML/SVG;
`forja_render_docx.py` é legado arquivado, não é executado e não é critério de liberação. Cada gate tem par de detecção/não-trava na
regressão; valor entre aspas ou em transcrição identificada como terceiro não
exige âncora própria.
