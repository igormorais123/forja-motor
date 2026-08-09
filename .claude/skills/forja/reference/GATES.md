# GATES — o que reprova, quem implementa

> **Este catálogo foi extraído do código em 09/08/2026**, varrendo os identificadores
> literais nos scripts, e não da documentação. A distinção importa: a documentação da
> casa cita gates que não existem, e a seção final registra quais.
>
> Os gates **de contrato** (os que o runner exige por fase, como `helena_present` ou
> `p0_zero`) estão em [FLUXO.md](FLUXO.md). Aqui ficam os **findings** — os
> identificadores que aparecem quando algo reprova.

## Índice

- [Como ler um finding](#como-ler-um-finding)
- [As 29 famílias](#as-29-famílias)
- [As famílias que você mais vai encontrar](#as-famílias-que-você-mais-vai-encontrar)
- [O que cada gate não prova](#o-que-cada-gate-não-prova)
- [Gates citados na documentação que não existem no código](#gates-citados-na-documentação-que-não-existem-no-código)

## Como ler um finding

Todo finding tem `gate`, `sev` e `problema`. `sev` é `P0` (bloqueia) ou `P1` (registra e
exige justificativa). O identificador diz de onde veio: o prefixo é a família, o sufixo
descreve o defeito — `L9-fonte-prevalente`, `SVGC-01`, `ACE7-entrega-fragmentaria`.

**Nenhum P0 é justificável por prosa, e não há exceção executável.** A documentação da
casa já tratou o `[dia]` da data de protocolo como exceção tolerada; **o código não a
concede** — `G2-placeholder` casa `[DIA`, `[DATA`, `[NOME`, `[CRC` e companhia, e
`forja_visual_build.py` aborta diante de qualquer P0. Preencha a data, mesmo que prevista,
e reconfira antes da liberação.

## As 29 famílias

| Prefixo | Famílias de quê | Implementado em | nº |
|---|---|---|---|
| `L0`–`L13` | lastro documental e econômico | `forja_lastro.py` | 14 |
| `LP` | P0 e política de citações | `forja_p0.py`, `forja_citations.py` | 22 |
| `LAD` | auditoria adversarial | `forja_adversarial_gate.py` | 16 |
| `LAR`, `LRT` | red team e recheck | `forja_red_team.py` | 9 |
| `G1`–`G11` | verificador de peça | `forja_verificador.py` | 14 |
| `LE` | entrega e pacote | `forja_entrega.py` | 11 |
| `LC` | conselho | `forja_conselho.py` | 11 |
| `LRG` | regimento do tribunal | `forja_regimento_gate.py` | 9 |
| `LRP` | replay de fonte oficial | `forja_replay.py` | 9 |
| `LQC`, `LFA` | fontes oficiais e cotejo | `forja_fontes_oficiais.py` | 15 |
| `ACE` | aceite dos critérios do cliente | `forja_gate_aceite.py` | 8 |
| `DOC` | integridade desta skill | `forja_skill_doctor.py` | 9 |
| `LPS` | parágrafos lastreados | `forja_paragrafos.py` | 7 |
| `I` | invariantes de governança | `forja_lapidacao_governanca.py` | 6 |
| `LRD` | redação e voz humana | `forja_redacao.py` | 6 |
| `ADV` | antifraude N4 | `forja_n4_anti_fraud_audit.py` | 5 |
| `LCD`, `LDI` | ingestão e cobertura | `forja_ingestao.py` | 10 |
| `LPD` | definição de produto | `forja_produto.py` | 5 |
| `LCC`, `LCX`, `LFR` | contexto e reconferência | `forja_contexto.py` | 6 |
| `S` | identidade processual e sobreabstração | `forja_identidade_processual.py`, `forja_verificador.py` | 4 |
| `LJ` | injeção de prompt | `forja_injection_scan.py` | 2 |
| `LI` | identidade de citação | `forja_citations.py` | 2 |
| `SVGC` | colisão em SVG | `_FERRAMENTAS/medina_svg_colisao.py` | 5 |
| `VIS` | assinatura visual | `forja_assinatura_visual.py` | — |
| `P` | bancada de modelos | `forja_bench_modelos.py` | 6 |

## As famílias que você mais vai encontrar

### Lastro — `forja_lastro.py`

O gate que impede alucinação por lastro aparente. Citar não basta: exige o trecho
transcrito.

| Gate | Reprova |
|---|---|
| `L1-lastro`, `L1-status-ausente`, `L1-status-desconhecido` | fato afirmado sem status de verificação no ledger |
| `L2-transcricao` | fato com status de lastro e sem transcrição verbatim |
| `L3-superlativo` | superlativo sem base |
| `L4-denominador` | percentual sem denominador declarado |
| `L5-identidade` | identidade de parte ou ato trocada |
| `L6-norma-por-ano` | norma citada pelo ano errado |
| `L7-criterio-vigente` | critério revogado tratado como vigente |
| `L8-objecao` | objeção conhecida não enfrentada |
| `L9-fonte-prevalente` | material econômico sem fato com `role='fonte_prevalente'` |
| `L10-data-base` | data-base do produto não coincide com a do fato prevalente |
| `L11-valor-orfao` | cifra sem âncora ligada à fonte (**P1**, não P0) |
| `L12-hierarquia-fonte` | documento econômico posterior não eleito nem descartado |
| `L13-aritmetica-derivada` | valor derivado que não recomputa contra base e percentual |

Os econômicos (L9–L13) só acordam com `--exigir-economico` ou quando o build recebe
`--ledger`. **`L9` reprovando parece erro do build e é erro de lastro.**

### Verificador de peça — `forja_verificador.py`

Roda automaticamente dentro de `forja_visual_build.py`.

`G1-personas` (nome de persona interna no produto) · `G1-jargao` · `G2-placeholder`
(`[NOME]`, `[CRC-UF]`, `[dia]`) · `G3-contagem` (contagem sem fonte) · `G4-sumula` (par
súmula × tribunal) · `G4-dispositivo` (dispositivo notório trocado) · `G5-instituto`
(instituto jurídico na direção errada) · `G6-cara-ia` e `G6-emoji` · `G7-datas`
(aritmética de intervalos) · `G8-formato` (formato protocolável) · `G9-proveniencia`
(origem operacional no corpo — **o P0 da fronteira**) · `G10-escrita-humana` (travessão
explicativo repetido, entre outros) · `G11-regimento`.

### Regimento — `forja_regimento_gate.py`

`LRG2-tribunal-nao-identificado` · `LRG4-regimento-nao-declarado` ·
`LRG5-regimento-inexistente` · `LRG6-regimento-mudou-desde-a-f3` ·
`LRG7-sem-secao-de-emendas` · `LRG9-fato-sem-lastro`.

O `LRG6` percebe que o arquivo do regimento **mudou desde a F3** — ele compara hash. Isso
não é o mesmo que vigência: um arquivo velho, estável e com a seção de emendas passa
tranquilamente. A atualidade até a data do protocolo continua exigindo pesquisa oficial
registrada, e o `LRG7` só confere que a expressão "emendas posteriores" existe no texto,
não que alguém as procurou.

### Red team — `forja_red_team.py`

`LRT1-relatorio-ausente` · `LRT2-sem-objecoes-enumeradas` · `LRT3-abaixo-do-protocolo` ·
`LAR1-recheck-ausente` · `LAR4-aplicavel-sem-item` · `LAR6-alegacao-sem-resultado`.

São **nove** perguntas desde 09/07/2026; a nona é anti-bajulação: *a peça aceita premissa
do comando ou do e-mail que os autos não sustentam?*

### Injeção — `forja_injection_scan.py`

`LJ1-sem-varredura` · `LJ2-p0-sem-triagem`. O segundo é o que importa: achar não basta,
o achado precisa de triagem humana registrada.

### Aceite — `forja_gate_aceite.py`

Confere os critérios que **o cliente** escreveu, não os da casa. `ACE1` a `ACE6` exigem
prova de quem afirmou ter concluído: artefato existente, não vazio, em formato nativo
quando é número, com inteiro teor quando é precedente. `ACE7-entrega-fragmentaria`
bloqueia a remessa quando ela foi contratada como única e conclusiva e ainda há item
parcial ou aberto.

**O gate mede o estado do mundo, nunca a qualidade da declaração.** Ele não lê o
conteúdo do artefato — confere existência, tipo e tamanho.

### Colisão em SVG — `_FERRAMENTAS/medina_svg_colisao.py`

`SVGC-01` a `SVGC-05`. Detalhe e limiares em [VISUAL.md](VISUAL.md#os-gates-do-desenho).

## O que cada gate não prova

Levantado lendo os produtores em 09/08/2026, depois de uma auditoria adversarial. **Um
gate verde é prova do que ele mede, e de nada além.** A lista abaixo é o contrário do
resto deste documento: aqui está onde a máquina não olha, e onde portanto a peça depende
inteiramente de quem a conduz.

| Gate | O que ele realmente afere | O que ele **não** prova |
|---|---|---|
| `helena_present`, `cicero_present` | o parecer existe, passa de um piso de bytes e traz itens numerados | que Helena ou Cícero foram de fato consultados. **Não há verificação de proveniência** — ela existe só para o Diabob |
| `template_selected` | há texto não vazio no campo de template do `paragraph_provenance` | que o DOCX nasceu do template do escritório. Não confere arquivo, hash, timbre nem cabeçalho |
| `LRG6-regimento-mudou-desde-a-f3` | o hash do regimento arquivado mudou desde a F3 | que o regimento está **vigente**. Arquivo velho, estável e com seção de emendas passa. A atualidade continua exigindo pesquisa oficial registrada |
| `LRG7-sem-secao-de-emendas` | a expressão "emendas posteriores" aparece no arquivo | que as emendas foram pesquisadas, quanto mais anexadas |
| `no_pdf_or_raster_rendering` | a QA do F8 foi estática sobre OOXML (`renderingUsed`, `pdfCreated` e `pngCreated` falsos) | **nada sobre o PDF da entrega**, que continua obrigatório por Word COM em derivação posterior |
| gates de aceite `ACE1`–`ACE6` | o artefato existe, não está vazio e tem o tipo certo | que o conteúdo responde ao que o cliente pediu. O gate mede o estado do mundo, nunca a qualidade |
| `conditionalGates` dos contratos | — | **nada: o runner não lê esse campo.** Os "gates econômicos" de F5 e F7 são metadado contratual sem execução; em F7 o lastro econômico é acionado pela detecção de material econômico, não por ele |

Corolário para o dia a dia: quando alguém disser "passou em todos os gates", a pergunta
seguinte é **quais**, e a de depois é o que aqueles gates medem.

## Gates citados na documentação que não existem no código

Conferido no disco em 09/08/2026. **Não tente rodar estes:**

<!-- doctor:ignora -->
| Citado como | Onde aparece | Estado real |
|---|---|---|
| gates **S6** e **S7** | `CLAUDE.md`, seção "Regra escrita que não pega vira gate" | **não implementados.** O código de `forja_identidade_processual.py` tem `S2-pareamento-nome-papel`, `S4-direcao-no-requerimento` e `S4-presenca-direcao`; `S5-sobreabstracao` está no verificador. S6 e S7 não existem em lugar nenhum |
<!-- /doctor:ignora -->

A ironia merece registro, porque ela é a lição: a seção que criou S6 e S7 argumenta que
**instrução escrita disputa atenção com o resto do prompt e perde**, e que por isso a
regra precisava virar gate verificável. A regra virou texto sobre virar gate. Enquanto
S6 e S7 não existirem, a identidade dos atos recursais e o objeto devolvido continuam
dependendo de quem conduz a fase — que é exatamente a condição em que a casa já os viu
serem violados em dois clientes e dois tribunais.

**Antes de citar um gate por memória, procure o identificador no código.** Uma varredura
que custa segundos:

```
grep -rn "NOME-DO-GATE" --include="*.py" .
```
