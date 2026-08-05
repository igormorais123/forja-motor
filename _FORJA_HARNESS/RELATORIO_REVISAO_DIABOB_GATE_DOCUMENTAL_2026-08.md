# Revisão Diabob — FORJA-LASTRO-v2 e Plano 41

**Data:** 04/08/2026  
**Revisor:** Diabob (red team anti-autoengano), aplicado pelo Codex  
**Escopo:** estado do código após a régua verde; foco em autoaprovação, fallback documental, distinção entre não examinado e aprovado, e coerência entre plano, contrato e evidência.

## Verdict

**Aprovado tecnicamente após correções materiais; a quinta contraprova desta revisão fechou a última rota de autodiscovery silencioso.** O estado anterior não estava pronto para ser chamado de fail-closed: o runner F7 tratava ledger canônico inválido como P0, mas o verificador usado pelas rotas visuais podia capturar o erro e usar um snapshot histórico válido. A peça econômica passava com a versão conveniente da fonte enquanto a fonte vigente estava quebrada. A revalidação também fechou a superfície em que um caller ad hoc podia passar `exigir=False` e desligar L9–L13 diante de texto econômico, fechou a perda de histórico por aliases antigos na memória de auditabilidade, tornou permanente a contraprova de que produto não econômico segue verde nas rotas direta e canônica e agora trata caminho `ledger_path` explicitamente ausente como erro, não como convite à descoberta.

A correção foi aplicada em `forja_verificador.py`: erro de leitura, UTF-8 ou schema no `fact_ledger.json` canônico devolve ledger vazio e impede a descoberta de snapshots. L9–L13 então reprovam P0. A mesma precedência foi aplicada a `PecaVisual`: um `ledger_path` explicitamente quebrado, inexistente ou não regular não pode ser trocado pelo ledger válido descoberto no `case_dir`. As contraprovas foram adicionadas em `test_forja_verificador.py` e T11 de `test_forja_lastro.py`, sob `MC-18` e `MC-22`.

## O autoengano encontrado

“Há um snapshot válido, então ainda temos algo para trabalhar” parece resiliência. Em uma cadeia de fonte prevalente, é apenas substituição silenciosa de autoridade. O sistema não estava escolhendo a verdade; estava escolhendo o arquivo que permitia seguir.

Também havia documentação atrasada: o protocolo dizia 67 casos e não distinguia claramente os guardas L0; o catálogo não narrava o fallback; a lição 115 registrava a colisão de nomes sem registrar sua correção. Esses pontos foram alinhados.

## Evidência

- Caso de contraprova: `fact_ledger.json` canônico quebrado + `fact_ledger-snapshot.json` válido.
- Antes da correção: `verificar(..., case_dir=..., exigir_economico=True)` não produzia achado econômico.
- Depois da correção: a mesma chamada produz `L9-fonte-prevalente` P0; o snapshot não é usado.
- Identificador de recomputo uniformizado: `L0-recomputo-sem-insumo`.
- Taxonomia: `MC-17` (ledger inválido silencioso), `MC-18` (snapshot mascara canônico inválido), `MC-19` (caller desliga gate econômico), `MC-20` (memória perde fase por alias histórico), `MC-21` (resumo não decompõe o total) e `MC-22` (caminho explícito ausente cai para autodiscovery).
- Regressões locais: `python test_forja_verificador.py` verde com 21 detecções, 17 não-travas e a contraprova de snapshot; `python test_forja_lastro.py` verde com 90 verificações, incluindo a precedência de `ledger_path` explícito presente e ausente, a contraprova `L0-economico-desativado` e as rotas não econômicas; `python test_forja_memoria_auditabilidade.py` verde com 3 testes, incluindo status, fase corrente e histórico com aliases.

## Risco real

Sem a correção, uma alteração ou corrupção do ledger vigente podia não bloquear uma peça visual se restasse um snapshot antigo no diretório. O risco não era apenas técnico: data-base, fonte prevalente, hierarquia e cálculo poderiam ser validados contra uma versão que já não governava o caso.

Depois da correção, o risco residual é humano: o hash prova identidade do arquivo, não suficiência jurídica; a fonte Cafelana continua `proposto`, e a conferência do PDF de 2,14 GB continua nominal e manual. O baseline v14 marcou 49/49 suítes, 540 testes pytest, 60 subtests e 7 regressões de script; a régua rápida de revalidação marcou 83 arquivos e 17 suítes verdes em 31,8 s. A saída da regressão também passou a decompor explicitamente os 30 cenários do Plano 41, em vez de deixar parte do total implícita; o defeito de evidência permanece catalogado como `MC-21`, e a nova precedência de origem como `MC-22`.

O bypass econômico também não permanece aberto: quando o texto é materialmente econômico, `exigir=False` produz `L0-economico-desativado` P0; apenas texto sem incidência pode retornar vazio. O mesmo princípio agora vale para a origem: `ledger_path` explícito ausente produz bloqueio, mesmo que o `case_dir` ofereça um ledger válido.

## Segunda mordida: a memória também pode apagar o passado

O código já tinha corrigido os aliases para calcular o status da fase, mas isso era uma meia-correção elegante demais para ser confiável. O `phaseHistory` filtrava somente nomes atuais; eventos gravados com `F1_INGESTAO_COBERTURA`, `F4_PLANEJAMENTO_ESTRATEGICO`, `F5_PESQUISA_FONTES_OFICIAIS` ou `F6_REDACAO_MINUTA` desapareciam do documento. E o estado corrente podia sair com o alias cru. Resultado: o sistema não mentia no gate, mas mentia na memória que o advogado receberia.

**Correção aplicada:** normalização para os identificadores canônicos de `phase_contracts` em `completedPhases`, `currentPhase`, `phaseHistory` e saída final; regressão própria; memória real da Cafelana reconstruída e validada, com F0–F6 `completed`, F7 `blocked` e F8–F10 `not_started`. O defeito foi catalogado como `MC-20`.

A rechecagem física de 04/08 às 02:40 confirmou que os hashes atuais de `F-FP-001` e `F-FP-002` coincidem com o ledger. Isso reforça a identidade dos arquivos, mas não autoriza a promoção humana do primeiro fato.

## Teste de realidade

O gate decisivo é destrutivo apenas na bancada: criar lado a lado um canônico inválido e um snapshot válido. O resultado aceitável é P0 em L9–L13. Se a execução terminar verde ou selecionar o snapshot, a regressão falhou e a produção deve parar.

O novo teste decisivo é ainda mais simples: fornecer um `ledger_path` que não existe ao lado de um `case_dir` com ledger válido. O resultado aceitável é `L9-fonte-prevalente` P0 e nenhum DOCX. Se a rota gravar a peça, a autoridade explícita foi substituída silenciosamente e a produção deve parar.

## Transparência

Este parecer não valida a fonte, não libera a peça, não autoriza protocolo e não envia e-mail. A régua verde prova coerência do mecanismo e das regressões, não a conclusão jurídica. A única próxima decisão de governança continua sendo a conferência humana nominal da fonte prevalente e a aprovação do advogado.
