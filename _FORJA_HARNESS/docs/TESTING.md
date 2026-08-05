<!-- generated-by: gsd-doc-writer -->
# Testes

## Estratégia

A FORJA usa `unittest` e validadores executáveis. Não há limiar formal de cobertura nem pipeline de CI localizado neste harness; por isso, a evidência de aceite é a combinação de testes direcionados, regressão integrada, validação dos contratos, QA estática OOXML/SVG e memória de auditabilidade. Artefatos históricos podem ter testes de compatibilidade PDF, fora da rota canônica.

## Baseline — a porta de entrada única

```powershell
python forja_baseline.py [--json CAMINHO] [--quiet]
```

**Nunca use `pytest` direto como medida de baseline.** As regressões standalone da casa são escritas como scripts autônomos e comunicam o veredito pelo código de saída; o pytest não as coleta, e um "104 passed" nunca as incluiu. A fotografia corrente (05/08/2026) tem 41 scripts standalone, além das suítes pytest. Além da lista histórica abaixo, as ondas v23–v25 protegem `test_forja_adversarial_gate.py`, `test_forja_canario_mutacao.py`, `test_forja_canario_catraca.py`, `test_forja_forma_artefatos.py`, `test_forja_recomputo_censo.py`, `test_forja_rota_forma.py`, `test_forja_f8_pecas_reais.py`, `test_forja_visual_build_peca_longa.py`, `test_forja_layout_papeis.py`, `test_forja_varredura_tipografica.py`, `test_forja_layout_antimoldagem.py`, `test_forja_baseline_aprovado.py`, `test_forja_assinatura_antimoldagem.py`, `test_forja_adocao_rota.py` e `test_forja_porta_unica.py`. A lista completa e os papéis permanecem em `SUITES_SCRIPT`, dentro de `forja_baseline.py`; qualquer novo script que substitua `sys.stdout` e não esteja classificado produz falha explícita de configuração, em vez de ser executado pela família errada.

Snapshot histórico em 26/07/2026: **41/41 suítes verdes · 463 testes pytest (+44 subtests) · 7 regressões em script · APROVADO**. A fotografia corrente mais recente de 05/08/2026 registrou **83/83 suítes · 545 testes pytest · 60 subtestes · 41 regressões standalone · APROVADO** em `telemetria/BASELINE_2026-08-05_011824.json`; a bateria controlada v25 correspondente está em `telemetria/BASELINE_GATE_DOCUMENTAL_2026-08-05-final-v25.json`. Evidência datada não substitui nova execução depois de mudanças. O relatório vai para `telemetria/BASELINE_<data>.json`.

Complementos que não entram no baseline por serem caros ou dependerem de Word real: `python forja_regua.py` (hashes de arquivos protegidos + suítes sintéticas + bateria REAL) e `python forja_regimentos.py`.

## Testes do passe editorial (F7-B)

Teste direcionado:

```powershell
python -m unittest -v test_forja_editorial.py
```

Regressão integrada do editor, estilo, runner, pacote e modo headless:

```powershell
python -m unittest -v test_forja_editorial.py test_forja_estilo_humano.py test_forja_n3_runner.py test_forja_n3_package.py test_forja_n3_headless.py
```

Baseline validada em 15/07/2026: **42 testes aprovados**. Essa contagem é evidência datada, não substitui nova execução depois de mudanças.

Os testes devem cobrir, no mínimo:

- recusa quando F7 ainda contém P0;
- recusa de autenticação que não seja Claude Max OAuth;
- confirmação, pelo envelope real, de um modelo dentro da allowlist de `forja_editorial_model.py` (padrão `claude-opus-5` desde 25/07/2026; `claude-fable-5` segue autorizado como legado);
- hash de origem divergente;
- alteração de número, data, autoridade, citação, marcador processual, pedido ou fecho;
- retenção insuficiente do conteúdo;
- retry a partir do texto auditado original;
- bloqueio depois de três tentativas rejeitadas;
- bundle completo e pareado por sufixo;
- recusa de promoção ou pacote quando o bundle está incompleto/adulterado;
- consumo de `final_markdown` por F8 e pacote novo.

Cobertura existente em `test_forja_editorial.py` na data deste documento: fluxo válido, alteração de número, alteração de pedidos, autenticação/modelo divergentes, título removido, geração do bundle, bloqueio por P0, retry desde a origem e encaixe contratual F7/F8. Permanecem como lacunas de regressão específica: invariantes individuais de aspas/autoridades/marcadores/origem operacional, terceiro retry reprovado, sufixos multi-documento, promoção F7 real, rejeição de Markdown anterior no pacote e render F8 consumindo efetivamente `final_markdown`. Esses caminhos podem estar implementados sem estarem comprovados de ponta a ponta.

## Validação N3 completa

```powershell
python validate_forja_n3.py --real-word --run-replay
```

As opções acima executam caminhos deliberadamente pesados e históricos: conversão Word/PDF real e replay. Use-as apenas para compatibilidade de acervo; a promoção atual deve usar a rota estática OOXML/SVG e não introduzir renderização.

## Contratos e JSON

```powershell
python forja_phase_contracts.py
python -m json.tool FORJA_SPEC_MANIFEST.json > $null
python -m json.tool FORJA_N3_CONFIG.json > $null
```

Valide também todos os contratos alterados em `phase_contracts/` e os schemas relacionados.

## Execução real do passe editorial

Uma chamada real deve ser feita apenas com texto auditado apropriado e gate F7 sem P0. O aceite exige:

- autenticação `claude.ai` e assinatura `max` registradas sem expor segredo;
- modelo canônico comprovado e dentro da allowlist (padrão `claude-opus-5`);
- `familyAssurance` recomposto pelo orquestrador — `unverified` bloqueia; em `strict_protocol`, só `cross_family` libera;
- todos os gates editoriais aprovados;
- diff disponível para inspeção;
- promoção somente depois da recomposição local.

A validação viva de 15/07/2026 usou uma peça auditada de aproximadamente 36 KB e passou na primeira tentativa. Ela comprova a execução standalone do Fable e seus gates, não promoção F7, render F8 nem pacote de ponta a ponta. Os artefatos sanitizados estão em `../reports/fable5_live_validation_20260715/`.

## Gate de lastro documental (L1-L8)

```powershell
python forja_lastro.py <peca.md> --ledger fact_ledger.json --base-dir <raiz-das-fontes> [--exigir-criterio]
python test_forja_lastro.py     # 37 casos; exit 0 = ok
```

A regressão é dupla por desenho: 12 casos de detecção e **11 de não-trava**. Recall sem especificidade premia trava excessiva, e um auditor que reprova o acerto é desligado na terceira vez — as duas frases reais corrigidas do caso Vale Trading estão fixadas em `NAO_PODE_TRAVAR`. Quatro casos verificam o acoplamento (contrato F7, `forja_delivery.py`, `forja_verificador.py`, baseline): gate importável mas desligado é decoração. Protocolo em `../PROTOCOLO_LASTRO_DOCUMENTAL.md`.

## QA visual estática e memória de auditabilidade

Qualquer mudança que alcance F8 exige:

1. inspeção do pacote OOXML, texto, layout estrutural e SVGs nativos;
2. recomputação da fidelidade Markdown→OOXML;
3. atestado humano da paginação e legibilidade antes de liberação estrita;
4. varredura de placeholders, marcas internas e origem operacional;
5. geração e validação de `MEMORIA_AUDITABILIDADE_FORJA.md`, `.html` e `.json`.

Um teste textual aprovado não comprova diagramação física correta; por isso o atestado humano continua obrigatório. A FORJA não usa renderização para produzir ou validar a rota canônica.

## Critério de encerramento

Uma mudança documental ou de código só está pronta quando:

- comandos relevantes terminam com sucesso;
- falhas esperadas são realmente bloqueadas;
- JSON e contratos permanecem válidos;
- links e caminhos documentados existem ou são explicitamente marcados como exemplos;
- nenhum segredo ou dado sensível entrou nos artefatos de documentação;
- limitações e evidências datadas estão registradas sem transformar teste técnico em aprovação jurídica.
