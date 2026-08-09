# COMANDOS — o livro de receitas, por momento

> Todo comando aqui foi lido do `argparse` do próprio script em 09/08/2026. Flags entre
> colchetes são opcionais. Rode de dentro de `_FORJA_HARNESS`.
> `python forja_skill_doctor.py` confere se os scripts citados ainda existem.

## Índice

- [Orientar-se antes de agir](#orientar-se-antes-de-agir)
- [Mover um caso pela esteira](#mover-um-caso-pela-esteira)
- [Ingestão e triagem (F1)](#ingestão-e-triagem-f1)
- [Exploração e pesquisa (F2, F3, F5)](#exploração-e-pesquisa-f2-f3-f5)
- [Conselho e contraditório (F4)](#conselho-e-contraditório-f4)
- [Verificação (F7)](#verificação-f7)
- [Produção visual (F7.5, F8)](#produção-visual-f75-f8)
- [Entrega e pós-entrega (F9, F10)](#entrega-e-pós-entrega-f9-f10)
- [Manutenção do sistema](#manutenção-do-sistema)

---

## Orientar-se antes de agir

A fachada `forja_axi.py` é somente de leitura: ela responde **onde o caso está**, sem
tocar em nada. A saída padrão é TOON; `--json` só quando um consumidor exigir.

```
python forja_axi.py                    # estado vivo do workspace, compacto
python forja_axi.py cases              # todos os casos, schema mínimo
python forja_axi.py case <case-id>     # um caso, sem corpo de artefato
python forja_axi.py queue              # a fila priorizada
python forja_axi.py health             # pré-requisitos locais da interface
python forja_axi.py commands <nome>    # descobrir o comando canônico antes de mutar
```

Ela **não** promove fase, não entrega, não libera juridicamente e não substitui gate
humano. `PASS` técnico, pacote existente ou fila verde nunca são aprovação jurídica.

Fila e avisos:

```
python forja_fila.py --dry             # ver a fila sem gravar
python forja_fila.py --proxima         # a demanda do topo
python forja_alertas.py                # avisos pendentes (nasce naoVisto e assim fica)
python forja_alertas.py --visto <id> --por <nome> [--nota "..."]
```

## Mover um caso pela esteira

```
python forja_run.py <caso> start <FASE> --expected-revision <N> [--run-id <id>]
python forja_run.py <caso> promote <attempt-dir> --expected-revision <N>
python forja_run.py <caso> block <FASE> --expected-revision <N> --reason "..." [--blocker <item>]
```

`<FASE>` é o identificador inteiro: `F1_INGESTAO_SEGURA`, `F7_AUDITORIA_JURIDICA_FACTUAL`
e assim por diante — a lista está em [FLUXO.md](FLUXO.md).

## Ingestão e triagem (F1)

```
python forja_injection_scan.py <pasta-ou-arquivo.pdf>
python forja_triagem_rapida.py <arquivo-ou-pasta> [--modelo grok-4.5-cursor] \
    [--saida F1_TRIAGEM_RAPIDA.json] [--teto-usd 1.0] [--permitir-reserva] \
    [--contexto "numero-cnj partes orgao"]
python forja_insumo_bloqueado.py <case-dir>              # valida o declarado
python forja_insumo_bloqueado.py <case-dir> --schema     # modelo do artefato
python forja_insumo_bloqueado.py <raiz> --vencidos       # o que voltou para a fila
```

## Exploração e pesquisa (F2, F3, F5)

```
python forja_exploracao_100.py init --case-id <id> --case-anchor "..." --output <saida>
python forja_exploracao_100.py validate <F2_QUESTION_TREE.json>
python forja_exploracao_100.py select-consultation <F2_QUESTION_TREE.json>
python forja_exploracao_100.py render-consultation <F2_QUESTION_TREE.json> --output <saida>
python forja_exploracao_100.py record-response <F2_QUESTION_TREE.json> --response <resposta.json>

python forja_legal_search.py search [--query "..."] [--tribunal ...] [--limit 50]
python forja_legal_search.py case --numero-cnj <cnj>
python forja_legal_search.py stj-search [--query "..."] [--organs ...]
python forja_legal_search.py stj-daily [--query "..."] [--days 30]

python forja_rotas_fonte.py [--fonte STF] [--tipo acordao]
python forja_rotas_fonte.py --probe [--fonte STF]        # exercita as rotas ao vivo
```

**Consulte `forja_rotas_fonte.py` antes de declarar bloqueio.** Ele guarda o que cada
tribunal serve, a chave exata, a armadilha que engana — e os pares que a fonte não serve
a ninguém, que é o que distingue `indisponivel_na_fonte` de `limitacao_da_ferramenta`.

## Conselho e contraditório (F4)

```
python forja_diabob.py --arquivo <blueprint.md> [--modelo grok-4.5-cursor] [--caso <id>] \
    [--saida F4_PARECER_DIABOB.json] [--permitir-reserva] [--json]
python forja_conselho.py <helena.md> <cicero.md> <council_decisions.md> [F4_PARECER_DIABOB.json]
python forja_painel_curto.py --arquivo <doc> --caso <id> --fase F4 [--saida F4_PAINEL_CURTO.json]
```

Helena e Cícero entram pelas skills `/helena` e `/cicero`. O Diabob entra **pelo
comando** — o gate afere a proveniência da chamada, não o texto.

## Verificação (F7)

```
python forja_verificador.py <arquivo.md> [--tipo peca|estudo|email] [--case-dir <dir>]
python forja_lastro.py <arquivo.md> [--ledger fact_ledger.json] [--base-dir DIR] \
    [--revisao revisao.json] [--exigir-criterio] [--exigir-economico]
python forja_editorial.py <caseId> <attempt-dir> --source audited_markdown.md \
    --f7-gate f7_gate_result.json
```

O `forja_verificador.py` roda automaticamente dentro de `forja_visual_build.py`; rodá-lo
à mão serve para saber onde você está **antes** de tentar construir.

## Produção visual (F7.5, F8)

```
python forja_visual_build.py <peca.md> <saida_dir> ["Título"] [--tipo peca|estudo] \
    [--case-dir <dir>] [--base-dir <dir>] [--ledger <fact_ledger.json>]
```

Material econômico exige `--ledger` e `--case-dir`: sem eles o gate `L9-fonte-prevalente`
reprova a construção, e a mensagem parece um erro do build quando é um erro de lastro.

O PDF e o render página a página saem de `montar_visual.montar()`, em `_FERRAMENTAS`:

```python
import sys; sys.path.insert(0, r"<raiz>/_FERRAMENTAS")
import montar_visual as m
pdf, paginas = m.montar(r"<saida>/<peca>_VISUAL_LAW.docx", {}, qa_dir=r"<saida>/qa", dpi=100,
                        markdown_path=r"<peca.md>", fidelity_path=r"<saida>/FIDELIDADE_VISUAL.json")
```

**Caminho longo derruba o Word.** `OSError: [Errno 22]` ao salvar DOCX é MAX_PATH do
Windows, não corrupção: construa em `C:\vt` e copie de volta.

**Não rode o baseline em paralelo com a montagem.** As duas rotas passam pelo Word por
COM e uma trava a outra por meia hora, com o wrapper ainda reportando sucesso.

## Entrega e pós-entrega (F9, F10)

```
python forja_delivery.py <caseKey>
python forja_envio_externo.py ...            # porteiro de saída; nada externo sai fora dele
python forja_anexos_conferencia.py [--aplicar] [--todas]
python forja_post_protocol.py scan-gmail [--shadow]
```

Ciclo do aprendizado, na ordem — e nenhum passo é dispensável:

```
python forja_aprendizado.py padroes [--minimo-casos 1] [--json]
python forja_aprendizado.py amostra <classe:causa> [--limite 6]
python forja_aprendizado.py adotar <classe:causa> --destino checklist|template|doutrina \
    --fase Fn --regra "..." --aprovado-por <nome>
python forja_aprendizado.py aplicar [--seco]
python forja_aprendizado.py revalidar
```

`padroes` ordena por **recorrência entre casos distintos**, não por contagem bruta — um
processo longo produz centenas de mudanças sozinho. `amostra` abre o par real de textos
do cofre local e não grava nada: **contar não é ler**, e foi olhando só a contagem que
ruído virou quase-regra da casa.

## Manutenção do sistema

```
python forja_baseline.py [--json <caminho>] [--quiet]     # porta única de testes
python forja_skill_doctor.py [--skill <pasta>] [--json]   # esta skill ainda bate com o disco?
python forja_regimentos.py [--raiz <dir>] [--limite-dias 90] [--json] [--hoje AAAA-MM-DD]
python forja_regimento_pdf.py --pdf <arquivo> --tribunal STF --nome "..." \
    --url-oficial "..." --versao "..." --saida "REGIMENTO_INTERNO_STF.md"
python forja_contribuicao.py ...            # placar de contribuição das vozes
python forja_painel_indicadores.py ...      # indicadores automáticos das vozes
python forja_pso_pet.py validate-plan <arquivo>
python forja_pso_pet.py audit-case <caso>
```

**`forja_baseline.py` é a porta única.** Rodar `pytest` direto não cobre as regressões
que são scripts e que o pytest não coleta — o veredito da casa é o do baseline.
