# Scripts pontuais / históricos (movidos da raiz em 16/07/2026)

Nenhum destes é importado como módulo vivo da esteira. Ficam aqui para consulta; a raiz do harness contém apenas módulos em operação. A exceção operacional explicitada abaixo é `validate_f7_integration.py`: o runner canônico o executa como teste legado pelo caminho `_scripts_oneoff/validate_f7_integration.py`.

| Script | Propósito | Situação |
|---|---|---|
| `build_f2a_igor_20260715.py` | Montagem das árvores F2-A dos casos Igor/Melissa em 15/07/2026 | uso único, datado |
| `neutralizar_marca_docx_puro.py` | Remoção de marca/metadados de DOCX (variante "pura") | utilitário pontual |
| `neutralizar_marca_peticao.py` | Remoção de marca/metadados de petição | utilitário pontual |
| `render_forja_sem_sanitize_corruptivo.py` | Render antigo SEM sanitização — **não usar**; o nome registra o defeito | descontinuado |
| `sanitize_pdfs_pendentes.py` | Sanitização em lote de PDFs pendentes (rodada específica) | uso único |
| `validate_f7_integration.py` | Validação da integração F7 na implantação N3 (plano 08) | validação histórica ainda executada por `validate_forja_n3.py`; não mover sem atualizar o runner |

## Ciclo AR (auto-research) — rodadas já executadas

Catorze scripts do ciclo AR chegaram aqui sem passar por esta tabela, e ficaram
sem registro até a varredura de código morto de 08/08/2026. **Nenhum é chamado
por nada** — zero referências em todo o acervo —, e é exatamente por isso que
precisam estar descritos: script sem chamador e sem descrição é indistinguível
de lixo, e o próximo a varrer apaga. O que eles guardam é o **procedimento** de
uma rodada que já rodou; quem for montar a rodada seguinte lê aqui como a
anterior foi montada, e não reinventa o cegamento.

A ordem abaixo é a dos ciclos, não a alfabética.

| Script | Propósito | Situação |
|---|---|---|
| `ar_painel_piloto.py` | Painel descritivo do ciclo **AR-0** (estudo piloto): n, média, sigma e ausências por indicador sobre o corpus e as peças reais do experimento `fabrica-peticoes-v1` | rodada concluída |
| `ar_spotcheck_i6.py` | Spot-check dos flags I6 (origem operacional) do painel AR-0 | rodada concluída |
| `ar_montar_exec_prompts.py` | Monta os prompts de execução pareada do **AR-1** (vigente, varA, varB) | rodada concluída |
| `ar_registrar_execucoes.py` | Constrói os manifests de execução pareada do AR-1 a partir dos logs reais | rodada concluída |
| `ar_selecionar_gen0.py` | Seleção do vencedor da geração 0, com hashes canônicos e eventos no log | rodada concluída |
| `ar_consolidar_julgamentos.py` | Divide as devolutivas dos juízes por par e consolida na bancada cega | rodada concluída |
| `ar_debug_ancoras.py` | Depuração: em quais bundles cada âncora do round 2 existe de fato | diagnóstico pontual |
| `ar_consolidar_round3.py` | Consolida o round 3 (votos por par) e computa a comparação de indicadores | rodada concluída |
| `ar2_montar_exec_prompts.py` | Prompts de execução pareada do **AR-2** (vigente e varH, tarefas t1 e t2) | rodada concluída |
| `ar2_registrar_execucoes.py` | Manifests de execução pareada do AR-2 a partir dos logs reais | rodada concluída |
| `ar2b_montar_exec_prompts.py` | Prompts da **rodada 2 do AR-2**, com nomes de saída opacos e sem cabeçalho de mutação | correção de defeito; ver abaixo |
| `ar2b_registrar_execucoes.py` | Manifests da rodada 2 do AR-2 e validação de paridade em `runpair-t1b/t2b` | rodada concluída |
| `ar_build_canarios_reais.py` | Monta os canários reais de falha única (camadas pública e secreta) sobre peça real **fora de `state/`**, para não contaminar nenhum split do corpus | procedimento reaproveitável |
| `ar_diagrama_arquitetura.py` | Diagrama SVG do subsistema de auto-research, como construído | gerador de figura |

O par `ar2b_*` merece o destaque: ele existe porque a rodada 1 do AR-2 foi
**invalidada por cegamento comprometido** — os nomes dos arquivos de saída
correlacionavam lado e tarefa, e as instruções carregavam no cabeçalho os
metadados da mutação. Quem julgava conseguia inferir o que estava julgando. A
correção foi trocar os nomes por `OUT_e1..e4` e remover os cabeçalhos. Isso não
é história do ciclo AR, é a única cópia escrita de um modo de falha que volta
sozinho na próxima vez que alguém montar uma bancada cega às pressas.

`MAPA_IA.md`, nesta pasta, é inventário auto-gerado e não é script.

---

Se algum voltar a ser necessário de forma recorrente, promover de volta à raiz e registrar em `DOCUMENTACAO_TECNICA.md`.
