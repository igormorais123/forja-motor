# Lapidação da FORJA — Onda 1: medição e julgamento

**Data:** 2026-08-05. **Branch:** `forja/lapidacao-sqlite-grade-20260805`.
**Versão congelada de referência:** tag `forja-congelada-20260805` = `3866e1c16`.
**Envelope:** `GOVERNANCA_LAPIDACAO_2026-08-05.md` (Helena) + `forja_lapidacao_governanca.py` (Efesto).

**Custo da onda:** 8 agentes, 668.944 tokens de subagente, 265 chamadas de ferramenta,
16 minutos. Teto da Helena: 22 agentes no total da campanha.

---

## O achado que responde à pergunta do dono

O pedido foi levar a FORJA ao rigor do *SQLite test harness* — "não uma coleção de scripts
nem uma suíte que apenas fica verde". A medição respondeu com um número:

> **Escore de mutação semântica: 0,20. Alvo declarado pelo próprio harness: 0,80.**

Medido por execução em `state/case-email-libra-sul-agint-stj-19f3c9350d875062`:

| Família de mutação | Mortos / aplicáveis | Escore |
|---|---|---|
| S1 inversão de tese | 0 / 0 | não aplicável |
| S2 troca de parte | **0 / 6** | 0,00 |
| S3 troca de valor ou data | **0 / 2** | 0,00 |
| S4 troca de pedido | **0 / 5** | 0,00 |
| S5 sobreabstração | **0 / 3** | 0,00 |
| S6 deturpação de precedente | 4 / 4 | 1,00 |

Em português: numa petição real, **trocar agravante por agravado passou nas seis
tentativas**, e **trocar "provimento" por "desprovimento" — pedir ao tribunal que negue o
recurso da própria cliente — passou nas cinco**. Nada na esteira acusou. A única família
que a FORJA de fato pega é a deturpação de precedente, e essa pega inteira.

O agravante disso é o segundo número: **`forja_mutation_semantic.py` rodou em 2 dos 53
casos na história inteira do sistema.** O instrumento de rigor existe, tem alvo declarado,
tem controles benignos que não podem morrer — e quase ninguém o percorre. É a lição 96 da
casa aplicada ao próprio medidor de qualidade: gate instalado em rota que ninguém percorre
é gate nenhum.

---

## Premissas verificadas por execução

A onda 1 mediu lendo o código. Ler prova presença; executar prova comportamento. Antes de
implementar qualquer coisa, cada premissa consequente foi reexecutada.

| Premissa afirmada | Medido por execução | Veredito |
|---|---|---|
| L9–L13 dormentes, não rodam por padrão | `validar_gates_economicos` com `ledger=None`, `exigir=None` → **P0 `L9-fonte-prevalente`** | **REFUTADA** |
| Memória Auditável em 2 de 53 casos (3,8%) | 6 de 53 (11,3%) | **REFUTADA** |
| `unknown_provenance_reference` sem código de gate | **184** ocorrências em 75 artefatos F7, **zero** com gate L9–L13 | CONFIRMADA, pior que o alegado (48) |
| reason codes como strings soltas | 108 identificadores distintos, nenhum `Enum` de motivo | CONFIRMADA |
| `all()` sobre lista vazia aprova por vacuidade | 3 linhas sem guarda em `forja_axi.py`: 648, 654, 697 | CONFIRMADA |
| `forja_n3_common` é god module | 77 importadores (2º lugar: `forja_n4_common`, 24) | CONFIRMADA |
| `_validate_result` com complexidade ~36 | **45** pontos de decisão por AST | CONFIRMADA, pior que o alegado |
| F2A degradou em formulário | confirmado nas 16 árvores; consequência distinta ≤ 1 | CONFIRMADA |
| rota visual canônica é OOXML puro | **nenhuma** referência a `win32com`, `Dispatch`, `inkscape`, `cairosvg`, `PIL` em `forja_visual_build.py` | CONFIRMADA |
| `state/` versionado no git | **5.691** arquivos de 8.949 rastreados | CONFIRMADA |

### A refutação que mais importa

A proposta mais bem colocada da fronteira de gates era *"ativar L9–L13 por padrão quando
material econômico for detectado"*. O avaliador adversarial a aprovou citando
`forja_lastro.py:1147-1171` e afirmando que os gates não são invocados de
`forja_verificador.verificar()`.

Executado, o oposto é verdade. Os gates econômicos são **fail-closed por construção**: sem
ledger, sem `exigir`, com ledger vazio — nas três configurações emitem P0
`L9-fonte-prevalente`. E `PecaVisual.salvar()` chama as duas validações em sequência
(`_validar_porta_unica`, lexical e incondicional; `_validar_lastro_documental`, econômica e
com ledger), de modo que a porta cobre ambos os caminhos.

O que era verdade na leitura: uma chamada crua `verificar(texto, tipo)`, sem `case_dir` nem
ledger, de fato não computa L1/L2/L7/L8 e L9–L13 — e isso está documentado de propósito em
`forja_verificador.py:424-426`, porque sem contexto documental esses gates não têm o que
conferir. A leitura viu a condição e concluiu ausência.

**Se essa proposta tivesse sido implementada, teria sido falso progresso perfeito:** código
novo, teste verde, "gate ativado", zero segurança acrescentada — consertando algo que já
funcionava. Foi barrada porque a premissa foi executada em vez de discutida.

---

## Julgamento adversarial da onda 1

20 propostas: **12 aprovadas, 6 aprovadas com emenda, 2 rejeitadas.**

**Rejeitadas** — e as duas rejeições são boas:
1. *Consolidar `forja_verificador` + `forja_consistency` + `forja_n4_validate` num módulo.*
   Motivo: falsa equivalência. Mesmo nome `validate_case` em três módulos não prova
   semântica idêntica; podem ter divergido de propósito (ciclo AR × F7 × N4). Unificar
   mascara intenção.
2. *Documentar L9–L13 como condicionais.* Classificada corretamente como **mudança
   documental sem mudança operacional**.

**Síntese do avaliador**, que vale além das propostas: *o sistema mede presença — o artefato
existe, o campo está preenchido — e não substância.* O F2A não degradou por falta de gate;
degradou porque as 14 condições que o gate confere são todas estruturais, e formulário bem
preenchido as satisfaz. O mesmo padrão explica a rota visual (existe, é boa, é OOXML pura, e
97,5% das entregas saem por outro caminho) e a Memória Auditável (prometida, entregue em
11% dos casos).

---

## Achados de segurança do repositório

`forja_lapidacao_governanca.py --invariantes` reprova `I4-repo-engine` de propósito:

- **759 binários versionados, 159,8 MB** (623 PNG, 47 PDF, 46 DOCX, 35 EMF).
- **5.691 arquivos de caso versionados em 55 pastas de `state/`** — Corsan, Libra Sul,
  Natura, Patrícia, Cafelana, com nomes de cliente, números CNJ e peças.

Isto contraria a restrição expressa do dono para esta campanha: *não levar casos, binários
ou segredos ao repositório do engine*. **Não foi corrigido por conta própria**: a correção
exige `git rm --cached` com reescrita de histórico, não é reversível de leve, e é ato do
Igor. Segredos: cinco padrões varridos, nenhuma ocorrência.

---

## Dois defeitos no código de governança escrito hoje

Registrados porque são o próprio método funcionando, e porque a casa aprende com defeito
real e não com acerto:

1. `inv_f2a_congelado` lia `schemaVersion`. As 16 árvores trazem `schemaVersion: "1"` e
   declaram o protocolo em `protocolVersion` (`FORJA-F2A-100-v1`, em 14 delas). O
   invariante estava cego e teria aprovado um v2 para sempre. É a **lição 188 repetida em
   código escrito no mesmo dia**.
2. `inv_repo_do_engine` procurava a substring `"/state/"` com barra inicial; `git ls-files`
   devolve caminho relativo. Reportava 759 binários e **zero** arquivos de caso, escondendo
   a parte grave do achado.

Ambos têm regressão em `test_forja_lapidacao_governanca.py`, onde cada invariante é visto
reprovando uma sabotagem. Controle que nunca falhou não prova nada.

---

## Lacunas que ninguém mediu

O avaliador apontou oito; estas três mudam decisão e ficam registradas como dívida:

1. **Taxa de edição humana pós-entrega.** Se as peças saem de F10 e são editadas à mão
   depois, os gates não estão evitando defeito — estão sendo contornados em silêncio, e
   toda métrica de gate vira ficção.
2. **Correlação entre severidade e ação humana.** Quantas vezes um P1 é ignorado e a peça
   protocolada? Sem isso, elevar qualquer gate de P1 para P0 é decisão cega.
3. **Quais dos 53 casos são produção real** versus piloto, estudo ou teste. Sem isso,
   "2,5% de adoção da rota visual" é número sem denominador honesto.
