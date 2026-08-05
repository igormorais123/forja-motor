# Revisão cruzada independente — FORJA-LASTRO-v2

**Data:** 04/08/2026  
**Revisor:** Codex (família distinta da execução Opus 5)  
**Escopo:** leitura do código e dos testes da implementação do Plano 41, com foco em acoplamento real, execução sem renderização, fontes grandes e auditabilidade.  
**Estado:** revisão concluída; pendências jurídicas e de governança permanecem abertas.

## Veredito

**Aprovado com correções aplicadas.** A implementação cobre as três rotas declaradas no plano e a rota visual oficial não chama renderizador, Word COM, PDF ou PNG. A revisão encontrou uma falha operacional que não aparecia nos testes: L9 e L12 calculavam SHA-256 com `Path.read_bytes()`. Isso poderia carregar o laudo Cafelana de 2,14 GB inteiro na memória. A correção foi aplicada em `forja_lastro.py` com `_sha256_file()` em blocos de 1 MiB, e uma regressão estrutural foi acrescentada à suíte. Em seguida, a revisão de integração encontrou que o contrato F8 ainda exigia PDF/rerender e que a memória de auditabilidade não era um requisito executável; ambos foram corrigidos sem alterar o acervo do caso.

## Evidência lida

- `forja_lastro.py`: L1/L2/L7 e L9–L13, seleção de fonte, inventário e cálculo de hash.
- `forja_run.py`: recomputação independente de `COMPUTED_LASTRO_GATES.json` e preferência pelo `fact_ledger.json` canônico.
- `forja_verificador.py`, `forja_delivery.py`: pontos de consumo e bloqueio.
- `forja_visual_build.py`, `forja_visual.py` e `medina_visual_kit.PecaVisual.salvar()`: pré-gate, persistência e rota ad hoc.
- `forja_svg_docx.py` e `forja_visual_qa_structural.py`: materialização SVG nativa no OOXML e QA estático.
- `test_forja_lastro.py`, `test_forja_run.py`, `test_forja_svg_docx.py` e contratos F5/F7.

## Achados e decisões

| ID | Achado | Decisão | Evidência |
|---|---|---|---|
| CR-01 | A entrada canônica executa F7 antes de compor e propaga contexto econômico. | **PASS** | `forja_visual_build.py`, linhas de pré-gate e `test_forja_lastro.py` T11-B. |
| CR-02 | A entrada direta e o script ad hoc passam por `PecaVisual.salvar()`. | **PASS** | `_validar_lastro_documental()` e T11; P0 remove saída parcial. |
| CR-03 | O runner confiava originalmente no snapshot hash-específico para o ledger. | **CORRIGIDO antes desta revisão** | `_compute_lastro_gates()` seleciona o `fact_ledger.json` canônico e registra `ledgerDeclared`. |
| CR-04 | Hash do PDF grande usava leitura integral em L9/L12. | **CORRIGIDO nesta revisão** | `_sha256_file()` lê blocos de 1 MiB; T adicional impede regressão para `read_bytes()` nos dois usos. |
| CR-05 | A rota visual oficial usa renderização externa. | **PASS — não usa** | `forja_svg_docx.inserir_svgs()` grava `image/svg+xml` no OOXML; `VISUAL_BUILD.json` registra `renderingUsed: false`. |
| CR-06 | QA pode declarar paginação humana por inspeção estrutural. | **LIMITAÇÃO HONESTA** | F8-S permanece observacional; a paginação/legibilidade final exige abertura humana do DOCX. |
| CR-07 | A fonte prevalente Cafelana já está liberada. | **NÃO** | `F-FP-001` permanece `validationStatus: proposto`, `groundingPending: true`; estado N3 rev. 174 está bloqueado. |
| CR-08 | O gate econômico e sua regressão estavam fora da régua rápida e do manifesto de integridade. | **CORRIGIDO nesta revisão** | `forja_regua.py` agora protege `forja_lastro.py` e `test_forja_lastro.py`, e executa a suíte em `--rapida`; manifesto passou a 83 arquivos. |
| CR-09 | F8 ainda exigia PDF, hashes de página e `package_rerender_reproduced` apesar da decisão sem renderização. | **CORRIGIDO nesta revisão** | `phase_contracts/F8.json` v3 exige QA estática OOXML/SVG; `forja_f8_contract.py` despacha a rota estática e mantém PDF apenas para compatibilidade histórica; `test_forja_f8_static.py` prova que `inspect_pdf` não é chamado. |
| CR-10 | A memória de auditabilidade estava descrita no catálogo, mas não era um artefato obrigatório executável. | **CORRIGIDO nesta revisão** | `forja_memoria_auditabilidade.py` gera MD/HTML/JSON sanitizados; elo 13 de `forja_delivery.py` valida o bundle; F9 v2 exige os três derivados; `test_forja_memoria_auditabilidade.py` cobre criação e adulteração. |
| CR-11 | A compatibilidade histórica ainda carregava o módulo de renderização no import do contrato F8. | **CORRIGIDO nesta revisão** | Fachada `inspect_pdf` tardia; importar a rota canônica deixa `forja_visual_qa` e `fitz` fora do processo, e a suíte estática confirma ausência de chamada. |
| CR-12 | Ledger F7 ilegível ou fora do schema podia cair em `not_applicable` e parecer “sem achados”. | **CORRIGIDO nesta revisão** | `_compute_lastro_gates()` agora emite `L0-recomputo-sem-insumo` P0, `computed.status: fail`, conserva erro/caminhos e tem regressão dedicada em `test_forja_run.py`; a taxonomia registra `MC-17`. |
| CR-13 | Duas sessões batizaram o mesmo gate com e sem acento. | **CORRIGIDO nesta revisão** | O identificador público foi uniformizado em `L0-recomputo-sem-insumo`; a régua e o histórico do manifesto registram o rebaseline com motivo. |
| CR-14 | Verificador visual aceitava snapshot histórico quando o `fact_ledger.json` canônico estava quebrado. | **CORRIGIDO nesta revisão Diabob** | `_carregar_contexto_lastro()` encerra a descoberta com ledger vazio em erro do canônico; L9–L13 produzem P0. Contraprova em `test_forja_verificador.py`; taxonomia `MC-18`. |
| CR-15 | Caller ad hoc podia passar `exigir=False` e desligar L9–L13 em texto econômico. | **CORRIGIDO nesta continuação** | `validar_gates_economicos()` emite `L0-economico-desativado` P0 quando a incidência monetária é detectada; T2 em `test_forja_lastro.py`; taxonomia `MC-19`. |
| CR-16 | Memória de auditabilidade reconhecia aliases antigos apenas no status; histórico podia ser omitido e `currentPhase` sair fora do vocabulário atual. | **CORRIGIDO nesta continuação Diabob** | `forja_memoria_auditabilidade.py` normaliza aliases para `phase_contracts` em status, fase corrente e `phaseHistory`; contraprova em `test_forja_memoria_auditabilidade.py`; taxonomia `MC-20`. |
| CR-17 | D3 exigia provar que produto não econômico segue verde nas rotas direta e canônica, mas a regressão só cobria a função de detecção. | **CORRIGIDO nesta continuação** | `test_forja_lastro.py` adiciona T11-NE para `PecaVisual` e `forja_visual_build`; a suíte passa a 88 verificações e a régua confirma as duas rotas sem P0 econômico. |
| CR-18 | A linha final do teste afirmava 88, mas não exibia os 28 cenários do bloco do Plano 41 nos subtotais. | **CORRIGIDO nesta continuação** | formatter imprime `12 + 11 + 16 + 21 + 28 = 88`; taxonomia `MC-21` e Lição 125. |

## Reexecução desta revisão

Comandos executados após a correção:

```text
python test_forja_lastro.py                         OK — 88 verificações
python test_forja_verificador.py                   OK — 21 detecções + 17 não-travas + contraprova de snapshot
python test_forja_run.py                           OK — 11 testes
python test_forja_svg_docx.py                      OK — 4 testes
python test_forja_n3_visual.py                     OK — 10 testes
python -m py_compile <módulos alterados>           OK
python forja_baseline.py --quiet --json telemetria\BASELINE_GATE_DOCUMENTAL_2026-08-04-final-v13.json OK — 49/49 suítes
```

O baseline final desta correção está em `telemetria/BASELINE_GATE_DOCUMENTAL_2026-08-04-final-v13.json`. Ele registra 49/49 suítes, 540 testes pytest, 60 subtests e 7 regressões em script. O manifesto foi rebaselinado com motivo auditável e a régua rápida de revalidação aprovou 83 arquivos protegidos e 17 suítes em 34,9 s (`telemetria/REGUA_2026-08-04_031358.json`). As contraprovas Diabob do fallback de snapshot, da precedência de `ledger_path` explícito, do bypass econômico e dos aliases históricos de fase, além das rotas não econômicas e da decomposição transparente da contagem, também ficaram verdes.

## Limites que não podem ser promovidos por este parecer

1. Hash e lastro físico provam identidade do arquivo, não que o conteúdo sustenta juridicamente a conclusão.
2. O PDF de 2,14 GB não tem camada de texto conferível automaticamente; a transcrição e a validação nominal continuam humanas.
3. A decisão de liberar a peça, responder ao Fábio ou enviar a memória é de governança; este parecer não envia nada.
4. A FORJA não deve voltar à rota de renderização. O script histórico `forja_render_docx.py` fica fora da rota oficial e não deve ser usado em produção. O pacote novo deve levar a memória MD/HTML/JSON e a validação estática F8, não PDF/rerender. A memória também deve manter os IDs canônicos de `phase_contracts`, mesmo quando lê estados históricos com aliases. A incidência econômica não pode contaminar produtos sem dinheiro: T11-NE agora fixa essa contraprova nas rotas direta e canônica.

## Próximo passo

Somente a revisão/aprovação do Igor e a validação humana da fonte podem mudar o estado bloqueado do caso; o ciclo técnico local já está rebaselinado e verificado.

## Adendo posterior — Diabob MC-22 (04/08/2026)

A revisão cruzada acima é um registro histórico da execução v13. A revisão Diabob posterior encontrou uma superfície que não estava coberta: `PecaVisual` recebia `ledger_path` inexistente, mas, por não ser arquivo, seguia para o ledger válido descoberto em `case_dir` e podia gravar produto econômico. A correção passou a distinguir “caminho explicitamente escolhido e quebrado” de “nenhum caminho informado”; no primeiro caso fixa ledger vazio, força `L9-fonte-prevalente` P0 e remove qualquer arquivo parcial. T11 acrescentou as contraprovas de bloqueio e ausência de DOCX, catalogadas como `MC-22`/Lição 126.

A régua curta v14 e o baseline v14 foram reexecutados após rebaseline justificado: 83 arquivos protegidos e 17 suítes em 31,8 s; 49/49 suítes, 540 testes pytest, 60 subtests e 7 regressões de script. O parecer Diabob complementar é a fonte primária desse achado; este adendo evita que a leitura do parecer Codex intermediário seja confundida com o estado final.
