# Auditoria de perdas — o que a cirurgia apagou e o que foi recuperado

**Motivo:** durante a reescrita dos commits não publicados, o checkout final do
`git filter-branch` apagou do disco 1,3 GB de material de caso. Igor pediu conferência
completa. Este documento é o resultado, com o método, para que seja reproduzível.

## Resultado: nada foi perdido

Comparação da árvore de `backup/codex-antes-do-reparo-20260805` contra o disco, arquivo por
arquivo, por **hash do próprio git** (SHA-1 do blob), não por tamanho ou presença:

| | |
|---|---|
| arquivos na árvore do backup | 26.186 |
| saíram do índice do git | 10 (os pretendidos, todos > 100 MB) |
| **desses 10, idênticos ao backup no disco** | **10 de 10** |
| divergentes ou ausentes | **0** |
| demais arquivos ausentes do disco | **0** |

Os 10 aparecem como `D` em `git diff` porque saíram do **índice**; o conteúdo está no disco.
As quatro cópias do ZIP de 375 MB são byte-idênticas entre si e ao original.

Reprodução:

```python
# para cada caminho da árvore do backup ausente do HEAD:
#   sha1("blob <tamanho>\0" + conteúdo_do_disco) == sha_do_blob_no_backup
```

## Varredura ampliada: houve outros apagamentos?

Todos os apagamentos do repositório nos últimos 45 dias, com o ruído gerado
(MAPA_IA, telemetria, logs, cache, backups) filtrado:

| Data | Autor | O que | Veredito |
|---|---|---|---|
| 16/07 | Igor | 2.301 arquivos — 2.103 eram quadros de animação (`anim_quadros`, `anim_etapas_quadros`), mais assets Blender e o planejamento do app de concursos | **limpeza legítima**, documentada em `docs(forja): registrar expurgo seguro do FocoEdital` |
| 27/07 | Igor | `test_forja_fable5.py` | **legítimo** — substituído por `test_forja_editorial.py` quando o modelo editorial passou de Fable 5 a Opus 5 |
| 31/07 | Igor | 6 JPG de contact sheet do QA da Cafelana v7 | artefato de QA regenerável |
| 04/08 | automação | `graphify-out/graph.html` | gerado |
| 05/08 | eu | 5 `F2_IDENTIDADE_PROCESSUAL.json` | **correto** — eram declarações inventadas por agente (adverso `"TRANSPORTADORA OU ESTADO"`, sha256 `"[será preenchido]"`) |
| 05/08 | eu | `_tmp_erm.docx`, `_tmp_estre.docx`, `_tmp_natura.docx` | ver abaixo |

**Nenhum apagamento indevido de material de cliente em 45 dias.** O único evento de risco real
foi o meu, e ele foi revertido integralmente.

### O caso dos três `_tmp_`: eu errei duas vezes, em direções opostas

Eles estavam apagados do disco antes de eu chegar e eu **consolidei a exclusão sem olhar** —
erro, porque o conteúdo era peça real: dois Agravos de Instrumento ao TRF3 (ERM/OSV e Estre,
ambos contra a Transpetro) e a matriz da Natura/Cabreúva para o Dr. Fábio.

Ao auditar, restaurei os três. Depois comparei o texto extraído com o resto da árvore: os três
são **cópias de trabalho de entregáveis que existem com nome próprio** —
`MEMORIAIS_EDCL_ERM_OSV_TRANSPETRO_TRF3_REVISAO_INTERNA.docx`,
`MEMORIAIS_EDCL_ESTRE_TRANSPETRO_TRF3_REVISAO_INTERNA.docx` (6 cópias) e
`MATRIZ_CONSOLIDADA_QUATRO_FRENTES_E_CORPUS_OFICIAL_REVISAO_INTERNA.docx`. Era limpeza justa.
Removidos de novo, e seguem recuperáveis do histórico.

**A lição das duas pontas:** consolidar exclusão que não se entendeu é tão errado quanto
restaurar o que foi legitimamente limpo. O que decide não é o nome do arquivo — `_tmp_` não
prova que é descartável, nem `MEMORIAIS` que é único — é comparar o conteúdo com o resto da
árvore antes de decidir.

## Não apague estas tags

`backup/main-antes-do-reparo-20260805` e `backup/codex-antes-do-reparo-20260805` são a única
cópia do estado anterior à cirurgia. Foram elas que permitiram recuperar 1,3 GB.
