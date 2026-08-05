# Varredura tipográfica do acervo — 04/08/2026

Depois de calibrar o QA visual contra quatro peças aprovadas, passei a régua estática em todo
o acervo de DOCX da fábrica. Nenhum arquivo foi tocado: a auditoria lê o OOXML e não escreve.

> **Este documento foi reescrito duas vezes na mesma tarde, e o resultado final é o oposto do
> primeiro.** A primeira versão dizia "33 peças abaixo de 50% de justificação, cinco em 0%".
> A segunda corrigiu a leitura e ficou em 11. Esta terceira, depois de descontar as versões
> que o próprio escritório já havia corrigido, fica em **4 — e nenhuma delas é petição.**
> Os dois erros estão descritos abaixo porque são mais úteis que o número.

## Erro 1 — li o XML do jeito ingênuo

Contei `<w:jc>` cru no `document.xml`. Isso ignora que parágrafo herdando a justificação do
estilo não tem `w:jc` nenhum, e que o XML do corpo inclui tabelas e caixas de texto. Pelo
leitor correto — `audit_docx_layout`, que percorre a cadeia de estilos — o relatório final do
Cafelana, que eu tinha acusado de 0%, está em **100%**.

## Erro 2 — acusei uma versão que já tinha sido corrigida

O caso que eu apresentei como o mais grave do acervo era o
`01_PARECER_NATURA_CABREUVA_FINAL_LIMPO_PARA_ASSINATURA.docx`: 8,2% de justificação, corpo
inteiro em Verdana 10,5. É de **20/07 às 19h24**.

Na mesma pasta de caso, de **21/07 às 20h39**, está o `..._CORRIGIDO_JUSTIFICADO.docx`, com os
mesmos 245 parágrafos e **100% nas três dimensões**. O escritório detectou e consertou no dia
seguinte, sem harness nenhum.

Não havia buraco de processo. Havia um instrumento acusando história — o mesmo erro que o
censo de gates cometeu ao parear tentativa descartada com estratégia promovida. O instrumento
passou a reconhecer versão superada: mesma pasta de caso, contagem de parágrafos próxima e
conformidade estritamente melhor nas três dimensões.

## O retrato, depois das duas correções

**123 entregáveis distintos.** Justificação abaixo de 50%: **4**. Abaixo de 90%: 8. Tamanho
12 pt abaixo de 90%: 29. Times New Roman abaixo de 90%: 19.

A execução posterior incluiu a cópia técnica `CAFELANA_NONO_TÓPICO_V9_REVISAO_LIMPA_TIPOGRAFIA_CORRIGIDA.docx`, criada em `_CORRECOES_PROPOSTAS_2026-08-04`. Ela tem 48 parágrafos e 100% nas três dimensões; permanece proposta, não substitui automaticamente o original e não foi enviada. A inclusão explica a diferença de 122 para 123 sem alterar os achados de conformidade.

> **Reprodução corrente em 05/08/2026 — não confundir com a fotografia histórica.** O
> mesmo script, sem alteração de filtro, mediu novamente 123 entregáveis, mas acusou 14
> abaixo de 90% de justificação. O recibo anterior `varredura_output.json`, de 04/08 às
> 20:16, registra 122 e 8. A diferença não foi apagada nem corrigida silenciosamente:
> seis DOCX Natura que aparecem agora nos piores — incluindo `PARECER_NATURA_TRF_MEDINA`
> e cinco arquivos de `_experimento_trf_medina_2026-07-15` — estão no disco atual, não
> aparecem no recibo anterior e não são rastreados pelo Git. Até que sua classificação
> como entregável, experimento ou versão superada seja confirmada, a fotografia de
> 05/08 fica registrada como **divergente e não consolidada**; nenhum desses arquivos
> foi removido ou reclassificado automaticamente.

Na fotografia histórica, as quatro piores são relatório interno, plano de pesquisa, índice
analítico e relatório de revisão interna — **nenhuma é petição**. As peças propriamente ditas
que ficam abaixo de 90%
de justificação são `PETICAO_FINAL_NIVEL_2_JALUSA_EVENTO_183` (65,8%),
`PETICAO_FINAL_NIVEL_2_VISUAL_MEDINA_OSORIO` (84,2%),
`MEMORIAIS_NYLTON_EDCL_TRF2_REVISADO` (86,2%) e `MEMORIAIS_LIBRA_SUL` (88,4%), este último
já nomeado no protocolo da fábrica como desvio conhecido e agora dimensionado: 21 parágrafos
de 181 fora do padrão.

## O que sobra de verdade

Não há epidemia tipográfica. O que havia era **ausência de instrumento**: o padrão Word existe
desde 08/07/2026 e o gate capaz de medi-lo só era chamado dentro de uma F8 — a fase que menos
roda. Um padrão sem instrumento que o meça é uma intenção.

Agora existe `forja_varredura_tipografica.py`, com catraca em
`test_forja_varredura_tipografica.py` que guarda dois compromissos: o universo medido não pode
encolher (senão a conformidade fica ótima por falta de material) e o número de peças fora do
padrão não pode crescer.

**Nada a corrigir por minha conta, e nada pedindo sua decisão.** O único caso que parecia
exigir ação já estava resolvido antes de eu olhar.
