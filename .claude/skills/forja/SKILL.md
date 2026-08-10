---
name: forja
description: 'A esteira FORJA inteira, de ponta a ponta: as onze fases (F0 a F10), os comandos literais, os gates que reprovam, as ordens invioláveis do escritório e as armadilhas com o caso real atrás de cada uma. Use ao trabalhar qualquer caso da fábrica de petições — ingerir autos, explorar o problema, pesquisar fonte oficial, reunir o conselho, redigir, auditar, produzir a peça em Word e PDF com a assinatura visual da casa, entregar e aprender do retorno humano. Use também ao mexer no próprio harness. Substitui as onze skills forja-* anteriores, que cobriam fases isoladas.'
metadata:
  substitui: [forja-adr, forja-briefing-pesquisa, forja-briefing-revisor, forja-campo-tribunais, forja-exploracao-problema, forja-handoff-caso, forja-ingestao-autos, forja-pesquisa-jurisprudencia, forja-red-team, forja-revisao-cruzada, forja-saida-humana]
  verificador: python forja_skill_doctor.py
  criada_em: 2026-08-09
---

# FORJA

Esteira de produção de peças jurídicas auditáveis. Onze fases, do comando do cliente à
prova de entrega, cada uma com contrato próprio, artefatos nomeados e gates que o runner
**recomputa** — ele não acredita no que o agente declara.

Trabalhe de dentro de `_FORJA_HARNESS`. Os caminhos abaixo são relativos a ela.

## A regra que organiza todas as outras

**Declarar não é fazer.** Todo gate desta casa nasceu de uma vez em que alguém escreveu
que tinha feito. Em F1 a F7 o runner recomputa doze famílias de gate — onze funções
`_recompute_*` mais o lastro documental — e sobrescreve o que você declarou; o gate de
aceite confere o artefato no disco; o gate do Diabob afere a proveniência da chamada, e
não o texto. Escreva o que for verdade, e produza a prova.

Corolário: **`unknown` não é `pass`.** Gate obrigatório sem veredito bloqueia a fase.

Segundo corolário, de 09/08/2026: **"feito" também é declaração, e por muito tempo não
teve prova.** O estado dizia `fulfilled` para duas coisas incompatíveis — *entregue* e
*triado, não havia demanda* — e a palavra sendo a mesma, um caso substantivo abandonado
ficava indistinguível de um e-mail administrativo corretamente descartado. É essa
ambiguidade que produz a experiência de "deram por feito o que estava pela metade".
`forja_censo.py` só chama de `entregue` o que tem arquivo em disco, com tamanho, **na
pasta da demanda e não na de estado**; o resto vira `concluido_sem_prova` e espera
declaração humana. A máquina não sabe distinguir lixo de ingestão de trabalho
abandonado, então ela não chuta: ela pergunta.

**E não confunda isso com cobertura total**, porque a metade que falta é justamente onde
você trabalha sem rede: **F8 e F10 não têm recomputação no runner**; `helena_present` e
`cicero_present` só conferem que o parecer existe, tem corpo e traz itens numerados;
`template_selected` aprova qualquer texto não vazio no campo. Onde a máquina não olha, a
disciplina é sua — e [GATES.md](reference/GATES.md#o-que-cada-gate-não-prova) diz onde ela
não olha.

## Comece aqui, sempre

```
python forja_censo.py               # a população inteira, com denominador declarado
python forja_censo.py --devendo     # o que ainda se deve, prazo na frente
python forja_axi.py case <case-id>  # um caso, sem corpo de artefato
python forja_fila.py --proxima      # o que fazer agora
python forja_avisos.py              # o que está esperando alguém dar ciência
```

**Comece pelo censo, e não pela fila.** Em 09/08/2026 a fila oficial respondia "4
prontas" sobre 91 pastas de caso, `forja_avisos.py` dizia "nenhum aviso" havendo caso
parado desde 11/07, e `forja_axi.py` anunciava "28 of 28 total". Nenhuma das três mentia
por bug isolado: as três liam um recorte e o anunciavam como retrato. `forja_censo.py` lê
os dois esquemas de estado, **informa sobre quantos casos apurou antes de qualquer
número** e se recusa a chamar de total o que é parcial. As outras três continuam úteis
para o que fazem; nenhuma delas responde "o que a fábrica está devendo".

`forja_axi.py` nunca promove fase, entrega ou libera juridicamente. **`PASS` técnico,
pacote existente ou fila verde não são aprovação jurídica.**

**E ela não vê todos os casos.** A fachada lê `FORJA_N3_STATE.json`; boa parte do acervo
ainda grava o estado no esquema anterior, `FORJA_STATE.json`. Ela declara essa população
no `count` e em `legacySchemaCases`, e responde `LEGACY_SCHEMA` — não "não encontrado" —
quando você pedir um deles pelo nome. **Caso que ela não lê existe:** abra
`state/<case-id>/FORJA_STATE.json`. Medido em 09/08/2026: 91 casos no disco, 28 legíveis
aqui, e a demanda do topo da fila estava entre os 61 invisíveis.

Ao abrir uma tentativa, nesta ordem, antes de escolher qualquer comando:

1. **`RUN_CONTEXT.json`** da tentativa — traz o contrato inteiro e as instruções da fase.
2. O **`checklistAprendido`** do contrato: são as regras que o escritório pagou para
   aprender, e nenhuma delas vira gate.
3. **`skills_repertorio/<Fn>.md`** — só o da fase corrente; as fichas se repetem de
   propósito.
4. A referência **desta** skill que a decisão de agora exigir, e não mais que ela.

## O fluxo

| Fase | Nome | Produz | Gates |
|---|---|---|---|
| **F0** | reconciliação com a fila | `case_manifest`, `reconciliation_report` | 2 |
| **F1** | ingestão segura | `document_index`, `coverage_ledger`, `injection_scan` | 3 |
| **F2** | produto e risco (+ exploração 100) | `product_classification`, `risk_classification`, `question_tree` | 6 |
| **F3** | fontes, regimento e leis | `fact_ledger`, `chronology`, `contradictions`, `sources_map`, `adversarial_audit` | 5 |
| **F4** | blueprint e conselho | `blueprint`, `proposition_ledger`, pareceres de Helena, Cícero e Diabob, `council_decisions`, `adversarial_strategy` | 6 |
| **F5** | pesquisa oficial | `source_ledger`, `citation_checklist` | 3 |
| **F6** | redação | `draft_markdown`, `paragraph_provenance` | 4 |
| **F7** | auditoria jurídica e factual | 11 artefatos, entre eles `final_markdown` | **21** |
| **F8** | QA visual | `docx`, `visual_qa_ledger`, `visual_build_manifest` e mais 3 | 16 |
| **F9** | pacote de revisão | `package_manifest`, `email_response`, memória de auditoria | 5 |
| **F10** | entrega, evidência e aprendizado | `delivery_evidence`, `run_metrics`, `retrospective` | 3 |

Três comandos movem tudo:

```
python forja_run.py <caso> start <FASE> --expected-revision <N>
python forja_run.py <caso> promote <attempt-dir> --expected-revision <N>
python forja_run.py <caso> block <FASE> --expected-revision <N> --reason "..."
```

Fase a fase, com entradas, artefatos exatos e o que cada gate afere:
**[reference/FLUXO.md](reference/FLUXO.md)**.

## Rotas — o que abrir, conforme o que você vai fazer

| Você vai… | Abra | E rode |
|---|---|---|
| começar um caso, ler autos | [FLUXO.md](reference/FLUXO.md#f1--ingestão-segura) | `forja_injection_scan.py`, `forja_triagem_rapida.py` |
| explorar o problema | [FLUXO.md](reference/FLUXO.md#f2--classificação-de-produto-e-risco) | `forja_exploracao_100.py` |
| identificar tribunal e regimento | [INVARIANTES.md](reference/INVARIANTES.md#regimento-do-tribunal) | `forja_regimentos.py`, `forja_regimento_pdf.py` |
| pesquisar jurisprudência | [INVARIANTES.md](reference/INVARIANTES.md#ordem-de-pesquisa-jurisprudencial) | `forja_legal_search.py`, `forja_rotas_fonte.py` |
| reunir o conselho | [INVARIANTES.md](reference/INVARIANTES.md#conselho-obrigatório) | `/helena`, `/cicero`, `forja_diabob.py`, `forja_conselho.py` |
| redigir | [INVARIANTES.md](reference/INVARIANTES.md#o-que-a-peça-precisa-conter) | os 7 itens obrigatórios, antes de escrever a primeira linha |
| citar os autos na peça | [INVARIANTES.md](reference/INVARIANTES.md#tratamento-e-citação-do-acervo) | só referência processual verdadeira |
| auditar antes de fechar | [GATES.md](reference/GATES.md) | `forja_verificador.py`, `forja_lastro.py` |
| passar pela revisão editorial | [INVARIANTES.md](reference/INVARIANTES.md#modelo-editorial) | `forja_editorial.py` |
| produzir Word e PDF | [VISUAL.md](reference/VISUAL.md) | `forja_visual_build.py`, depois `montar_visual.montar()` |
| montar o pacote de entrega | [FLUXO.md](reference/FLUXO.md#f9--pacote-de-revisão) | `package_manifest` e `email_response` — nenhum dos dois envia |
| reconciliar depois de enviado | [FLUXO.md](reference/FLUXO.md#f10--entrega-evidência-e-aprendizado) | `forja_delivery.py <caseKey>` confere a trilha |
| expor documento a modelo externo | [MODELOS.md](reference/MODELOS.md) | `forja_envio_externo.py` — recusa material dos autos |
| processar retorno humano | [INVARIANTES.md](reference/INVARIANTES.md#aprendizado-contínuo-do-retorno-humano) | `forja_post_protocol.py`, `forja_aprendizado.py` |
| escolher ou justificar modelo | [MODELOS.md](reference/MODELOS.md) | `forja_modelos.py` é a allowlist |
| entender por que algo quebrou antes | [ARMADILHAS.md](reference/ARMADILHAS.md) | `RETROSPECTIVAS.md` tem o detalhe |
| mexer no harness | — | `forja_baseline.py` é a porta única de testes |

Todos os comandos, com as flags reais: **[reference/COMANDOS.md](reference/COMANDOS.md)**.

## O que nunca se faz

1. **Origem operacional na peça.** E-mail, WhatsApp, Drive, pasta, caminho local: P0
   (`G9-proveniencia`). Na peça só existe referência processual verdadeira.
2. **Marcador interno no protocolável.** `[FONTE: ...]`, `[VERIFICAR]`, `[INFERÊNCIA]`
   ficam nos artefatos internos.
3. **Citar sem abrir a fonte.** Existência não é atribuição, e atribuição não é aderência
   da *ratio* — [ARMADILHAS.md](reference/ARMADILHAS.md#citação-seis-modos-de-falha-não-um).
4. **Peça sem elementos visuais completos.** Ordem permanente do titular.
5. **Conselho por prosa.** O Diabob entra pelo comando; o gate afere a proveniência.
6. **Modelo fora da allowlist.** GPT-5.5 e Kimi K2 estão travados no código.
7. **`Document()` vazio.** Toda peça parte do template — o timbre é arte vetorial.
8. **Declarar bloqueio sem testar rota.** Consulte `forja_rotas_fonte.py` e dê prazo de
   revalidação.
9. **Adotar o risco do cliente.** Objeção e precedente contrário se enfrentam para
   vencer, não para conceder.
10. **Dizer que está pronto sem o QA página a página.** É o único detector de defeito de
    render — e mesmo ele já deixou passar.

## Antes de dizer "concluído"

- Os artefatos de `requiredOutputs` existem no disco, não só na declaração.
- `forja_verificador.py` sem P0 — **e sem exceção executável**. O `[dia]` da data de
  protocolo é P0 como qualquer outro placeholder (`G2-placeholder` casa `[DIA`, `[DATA`,
  `[NOME`…) e derruba o build. Preencha a data, ainda que prevista, e reconfira; enquanto
  ela estiver pendente, o artefato é `internal_working` e não se chama protocolável.
- QA página a página feito **depois** da última regeneração — toda regeneração invalida o
  QA anterior.
- Se houve retorno humano, o ciclo de aprendizado rodou até `aplicar`.
- Se algo ficou de fora, está declarado com causa, e não omitido.

## Esta skill pode estar errada — confira

```
python forja_skill_doctor.py
```

Ele confere seis coisas, e só essas seis: que existem no disco os **scripts**, os
**contratos de fase**, os **templates Markdown** e os **arquivos de referência** citados
aqui; que toda **flag** `--assim` passada a um comando aparece no código dele; e que todo
**elo com âncora** encontra a seção de destino. Mais o frontmatter mínimo.

**O que ele deixa passar** — a lista importa mais que a anterior: subcomando errado,
argumento posicional omitido, contagem de gate desatualizada, divergência entre esta skill
e `requiredOutputs`/`requiredGates`, template `.docx`, e **se o texto está certo**. Nenhum
script sabe se a descrição de uma fase corresponde ao que ela faz. `APROVADO` significa
"os nomes citados existem", nunca "a skill está correta".

O motivo de ele existir está no próprio problema que esta skill resolve: uma skill é
documentação que o agente segue **sem conferir a fonte** — é esse o ponto dela —, e isso
a torna o lugar mais perigoso da casa para uma afirmação envelhecida.

**Onde a fonte diverge**, nesta ordem:

1. **Fase, entradas, saídas e gates:** o contrato (`phase_contracts/F*.json`), que é o que
   o runner lê. Esta skill nunca vence o contrato.
2. **Flags e comportamento de comando:** o código do script. Esta skill descreve; ele
   executa.
3. **Regra jurídica e do escritório:** `CLAUDE.md` **e** `AGENTS.md` da fábrica, os dois,
   cumulativamente. O `AGENTS.md` **não é cópia** do outro — eles divergiram, cada um tem
   dezenas de trechos que o outro não tem, e nenhum revoga o outro genericamente. Em
   conflito real sobre a mesma matéria, vale a ordem mais recente **quando ela declara
   que supera a anterior**; sem essa declaração, registre a contradição e não libere.
4. **Esta skill:** mapa operacional. Onde ela contrariar os três acima, ela está errada —
   conserte-a.

## Repertório

Que *outras* skills servem à fase em que você está: `_FORJA_HARNESS/skills_repertorio/`,
um documento por fase (`F0.md` … `F10.md`, mais `TRANSVERSAIS.md`) e o catálogo legível
por máquina `CATALOGO_SKILLS.json`. **Leia só o documento da fase corrente** — as fichas
se repetem de propósito. É cardápio, não contrato; o contrato da fase prevalece.
