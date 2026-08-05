# Memória de evidências — FORJA-LASTRO-v2 e materialização visual sem renderização

**Data da execução:** 04–05/08/2026
**Escopo:** gate de fonte prevalente, data-base, valores econômicos e rota visual da FORJA  
**Estado:** implementação técnica concluída; liberação jurídica e envio externo não realizados

## 1. Veredito executivo

O plano 41 foi executado na camada técnica. A FORJA agora:

- exige fonte prevalente, data-base, âncora monetária, hierarquia física e aritmética derivada quando o texto é materialmente econômico;
- recomputa L1/L2/L7/L9–L13 no runner F7, no verificador da entrada visual, no ponto de persistência `PecaVisual.salvar()` e na entrega;
- prefere o `fact_ledger.json` canônico ao snapshot hash-específico quando ambos convivem no diretório da fase;
- materializa a peça pela rota `forja_visual_build.py → forja_visual.compor() → PecaVisual → forja_svg_docx.inserir_svgs()`;
- embute os diagramas como SVG nativo no pacote OOXML e faz QA estrutural de DOCX/SVG, sem Word COM, PDF, PNG ou `forja_render_docx.py`.

Isso prova que o mecanismo está instalado e reproduzível. Não prova que uma fonte jurídica foi validada pelo advogado nem autoriza protocolo ou envio ao cliente.

A revisão cruzada independente do código (família Codex, distinta do Opus que implementou) está registrada em `RELATORIO_REVISAO_CRUZADA_GATE_DOCUMENTAL_2026-08.md`; a revisão Diabob complementar está em `RELATORIO_REVISAO_DIABOB_GATE_DOCUMENTAL_2026-08.md`. Elas encontraram e corrigiram o hashing integral de fontes grandes, a ausência do gate econômico na régua rápida/manifesto, o contrato F8 ainda dependente de PDF/rerender, a ausência de uma memória de auditabilidade executável, o caminho em que ledger inválido podia parecer `not_applicable`, o fallback indevido para snapshot histórico, a superfície ad hoc que desligava L9–L13, a perda de histórico causada por aliases antigos de fase, a decomposição incompleta da saída da regressão e o caminho explícito de ledger ausente que caía para autodiscovery. A revisão final também normalizou o identificador público `L0-recomputo-sem-insumo`.

## 2. Requisito, mecanismo e evidência

| Requisito | Mecanismo efetivo | Evidência desta execução |
|---|---|---|
| Fonte governante para material econômico | `role: fonte_prevalente`, status `validado`, validador, data e SHA-256 | 98 verificações de lastro; Cafelana permanece `proposto` até conferência humana |
| Transcrição e lastro físico | L1/L2, com P1 manual para PDF binário/grande | vocabulário real do ledger e laudo de 2,14 GB cobertos |
| Critério vigente | L7 computado pelo runner | `COMPUTED_LASTRO_GATES.json` é produzido a partir dos artefatos, não do texto do agente |
| Data-base, valores, hierarquia e cálculo | L9–L13 em `forja_lastro.py` | testes T2–T10 e pares de não-trava |
| Rota que originou o incidente | `PecaVisual.salvar()` protegido antes do `doc.save()` | T11 reprova documento econômico sem contexto |
| Entrada visual oficial | pré-gate no `forja_visual_build.py` + repetição em `PecaVisual` | T11-B reprova antes de compor |
| Diagrama vetorial | SVG direto em `word/media/*.svg`, relação OOXML e lint geométrico | `test_forja_svg_docx.py` (4/4) |
| Fidelidade do texto | `FIDELIDADE_VISUAL.json` + comparação Markdown→DOCX | composições de teste imprimiram `fidelidade 100%` |
| Memória auditável | `forja_memoria_auditabilidade.py` + elo 13 da entrega | `MEMORIA_AUDITABILIDADE_FORJA.md`, `.html` e `.json`; bundle sanitizado e hash-bound |

## 3. Rota visual adotada

O caminho de produção não chama o módulo histórico de renderização. O compositor cria o DOCX a partir do template, preserva o texto do Markdown e deixa marcadores declarativos. `forja_svg_docx.inserir_svgs()` valida cada SVG, calcula a proporção pelo `viewBox`, cria a relação `image/svg+xml` no pacote OOXML e substitui exclusivamente um marcador que ocupa um parágrafo próprio. F8/F9 não exigem PDF, imagens de página ou rerender; o validador de PDF fica isolado para compatibilidade histórica.

```mermaid
flowchart LR
  MD[Markdown congelado] --> G[Verificador F7 + FORJA-LASTRO-v2]
  G --> C[forja_visual.compor]
  C --> P[PecaVisual.salvar]
  P --> S[forja_svg_docx.inserir_svgs]
  S --> Q[QA estrutural OOXML + lint SVG]
  Q --> H[abertura e decisão humana]
  H --> D[DOCX + memória auditável]
```

O laudo `F8_QA_ESTRUTURAL.json` registra:

1. integridade do ZIP OOXML e partes obrigatórias;
2. ausência de marcadores não consumidos;
3. fidelidade Markdown→DOCX, números e qualificadores;
4. tipografia e margens codificadas no OOXML;
5. presença e relação dos SVGs;
6. colisão, clipping, enumerações e geometria dos SVGs;
7. `renderingUsed: false`, `pdfCreated: false` e `pngCreated: false`.

A abertura humana do DOCX continua obrigatória para paginação, legibilidade e decisão de liberação. A QA estrutural não se apresenta como inspeção visual humana.

O contrato F8 mantém compatibilidade com pacotes históricos por uma fachada tardia: importar a rota canônica não carrega `forja_visual_qa`, e a regressão confirma que a fachada PDF não é chamada.

## 4. Resultado das verificações

### Baseline canônica

Arquivo corrente: `telemetria/BASELINE_2026-08-05_011824.json` — **APROVADO: 83/83 suítes, 545 testes pytest, 60 subtestes e 41 regressões standalone**. A fotografia completa mais recente, após o endurecimento final da porta única, fechou **139/139 hashes íntegros, 52 registros de suíte (51 rápidas + 1 bateria real) e APROVADO em 133,0 s** (`telemetria/REGUA_2026-08-05_011415.json`, SHA-256 `0A7CAFCD8F294712D46C101F0D2883633A27E0D1543DD82C519244A3AC22AAC2`). A fotografia de 01:13 permanece histórica da mesma onda; v20–v24 também permanecem históricos.

Arquivo: `telemetria/BASELINE_GATE_DOCUMENTAL_2026-08-04-final-v20.json`  
Resultado: **APROVADO** — 56/56 suítes, 542 testes pytest, 60 subtestes e 14 regressões em script. A régua rápida de revalidação também fechou verde: 93 arquivos protegidos e 24 suítes rápidas aprovadas em 47,9 s (`telemetria/REGUA_2026-08-04_133952.json`), incluindo os testes da memória com aliases históricos e distinção de ledger, do F8 estático, do ledger inválido, da contraprova de snapshot, da precedência de `ledger_path` explícito presente e ausente, do bloqueio de bypass econômico, das rotas não econômicas, das catracas do conselho/F8, da política de citações, da identidade CNJ/tribunal, da triagem de injeção e da prova de isolamento UTF-8 dos PDFs externos.

### Liveness dos gates

Laudo corrente: `telemetria/GATE_LIVENESS_2026-08-05-final-v25.json` — **111 resultados, 73 gates computados (100%), 0 autodeclarados, 0 inexequíveis e 17 não exercitados históricos** (14 da F8 e 3 da F10). O registro anterior abaixo é mantido apenas para preservar a evolução da medição.

Laudo histórico v20: `telemetria/GATE_LIVENESS_2026-08-04-final.json`. Após o baseline e a régua rápida daquela fotografia, a execução examinou 111 resultados, com 73 gates declarados e 76 observados; 36 são computados por código, 37 são atestados pelo agente e 0 são inexequíveis. Há 17 gates inertes, isto é, declarados e nunca observados no acervo — 14 da F8 e 3 da F10. “Inerte” não significa “sem produtor”: o laudo separa essa condição em `inexequiveis`, que ficou zerada. A distinção evita apresentar dívida de evidência histórica como defeito de implementação.

### Regressões dirigidas

- `test_forja_svg_docx.py`: 4 testes, todos verdes;
- `test_forja_lastro.py`: 98 verificações no script (12 detecções, 11 não-travas lexicais, 16 de ledger, 22 de acoplamento e 37 cenários do Plano 41, incluindo hashing incremental, descoberta do ledger promovido, `L0-recomputo-sem-insumo` para JSON inválido, `L0-economico-desativado` para tentativa de bypass, escritores DOCX fora da rota, precedência da origem explícita presente e ausente, tipografia sem origem mantida na âncora e contraprovas de passagem não econômica nas rotas direta/canônica);
- `test_forja_memoria_auditabilidade.py`: 4 testes, cobrindo bundle sanitizado, adulteração de manifesto, normalização de aliases em status/fase corrente/histórico e distinção entre ledger canônico e snapshot histórico;
- `test_forja_politica_citacoes.py`: 9 verificações, cobrindo cobertura/liberação, uso bloqueado, ausência de citação e retorno `warn` para esquema não conferível;
- `test_forja_identidade_citacoes.py`: 16 verificações, cobrindo desencontro CNJ/tribunal, recursos que sobem a tribunal superior, normas sem tribunal e cinco peças reais;
- `test_forja_injection_gate.py`: 15 verificações, cobrindo cinco formas de pular a triagem e sete esquemas reais de varredura;
- `test_forja_paragrafos.py`: 18 verificações, cobrindo sete formas de lastro ausente/obsoleto e seis dialetos reais de proveniência sem travar os aprovados;
- `test_forja_fontes_oficiais.py`: 20 verificações, com seis ledgers reais e vereditos `pass`/`warn` sem aprovação silenciosa do conjunto vazio;
- `test_forja_red_team.py`: 28 verificações, com oito rechecks e seis relatórios reais sem reprovação;
- `test_forja_gates_emitidos.py`: emissão confirmada em 16/16 gates F8 e 3/3 gates F10, com 0 inexequíveis;
- `test_forja_lastro_rota_producao.py`: 3 verificações, incluindo materialização no disco do `COMPUTED_LASTRO_GATES.json`;
- `test_forja_ingestao.py`: 30 verificações, cobrindo seis índices, cinco ledgers e duas árvores reais da exploração de 100 sementes;
- `test_forja_contexto.py`: 17 verificações, cobrindo snapshot, escopo, digest e consistência dos seis casos reais;
- `test_forja_redacao.py`: 24 verificações, incluindo os 13 rascunhos reais nos gates de entidades, template e voz;
- `test_forja_artefatos.py`: 31 verificações, com 92 artefatos, 41 esquemas e vocabulário desconhecido fail-closed;
- `test_forja_p0.py`: 22 verificações sobre `p0_zero` e separação produtor/revisor, distinguindo achado aberto de resolução registrada;
- `test_forja_regimento_gate.py`: 17 verificações, incluindo quatro mapas reais e os estados `fail`/`pass`/`warn` esperados;
- `test_forja_produto.py`: 33 verificações, com 13 classificações reais e quatro blueprints Markdown;
- `test_forja_entrega.py`: 24 verificações de reconciliação e caminhos de manifesto reais;
- `test_forja_canario_catraca.py`: 18 catracas consultadas, com a contraprova de que a ruína não recebe aprovação;
- `test_forja_canario_mutacao.py`: 40 gates destruídos, 35 reprovações e 5 detecções de ausência, sem aprovação indevida;
- `test_forja_recomputo_censo.py`: 46 gates produziram veredito em 63 tentativas reais, com 8 reprovações e 19 resultados `pass` auditáveis;
- `test_forja_f8_pecas_reais.py`: 2 peças DOCX de referência aprovadas e 2 peças triadas com achados preservados;
- `test_forja_visual_build_peca_longa.py`: 10 verificações, fidelidade textual de 100% e composição longa pela rota SVG canônica, sem renderização;
- `test_forja_layout_antimoldagem.py`: quatro defeitos deliberados de OOXML acusados pelo gate, sem aprovação da peça estragada;
- `test_forja_baseline_aprovado.py`: três âncoras do padrão aprovado conferidas, com integridade e veredito estáveis;
- `test_forja_verificador.py`: 21 detecções e 17 não-travas;
- `test_forja_run.py`: 11 testes, incluindo preferência pelo ledger canônico e falha fechada para ledger ilegível;
- `test_forja_n3_visual.py`: 10 testes;
- `test_medina_svg_colisao.py`: 10 testes;
- `test_forja_citacoes.py`: 6 detecções e 6 não-travas;
- `test_licao41.py`: todos os casos verdes;
- compilação Python dos módulos alterados: verde.

## 5. Calibração econômica

Saída persistida em `CALIBRACAO_MONETARIA.json`, produzida por `forja_calibra_monetario.py`:

- 4.958 documentos examinados;
- regra ampla (moeda ou separador de milhar): 1.910 documentos (38,5%);
- regra estreita (marcador monetário explícito): 684 documentos (13,8%);
- somente a regra ampla tocaria 1.226 documentos;
- 16.997 de 57.031 ocorrências com separador de milhar eram referências jurídicas (29,8%).

Por isso a incidência de L9–L13 exige material econômico explícito. L11 permanece P1: sua promoção a P0 exige nova amostra classificada e nova execução do script.

## 6. Estado Cafelana e pendência humana

O ledger canônico é:

`state/case-cafelana-geral-reconstrucao-20260803/n3_artifacts/F3_FONTES_REGIMENTO_LEIS/fact_ledger.json`

O fato `F-FP-001` registra o laudo pericial como `role: fonte_prevalente`, data-base `1996-05-31`, SHA-256 `54ccf417df80d6947819c045f8eb07ea2be2c6e808301f01594d60f125c23497`, mas está com `validationStatus: proposto` e `groundingPending: true`. O arquivo PDF correspondente tem 2,14 GB e não possui camada de texto conferível automaticamente; a conferência verbatim e a validação nominal continuam humanas.

O estado N3 está na revisão 177, cursor F7, `lifecycleStatus: blocked`. O snapshot antigo `fact_ledger-f00067d94084.json` continua apontado como artefato histórico. O runner passou a registrar os dois caminhos e a calcular contra o `fact_ledger.json` canônico quando ele existe, sem editar o estado de caso fora do executor canônico.

### Rechecagem de integridade no disco — 04/08/2026, 02:40

| Fato | Arquivo referenciado | Tamanho | SHA-256 atual | Coincide com ledger |
|---|---|---:|---|---|
| `F-FP-001` | `8 - novo laudo técnico e-fls 1139 a 2699 (975-2515) (1).pdf` | 2.140.168.568 bytes | `54ccf417df80d6947819c045f8eb07ea2be2c6e808301f01594d60f125c23497` | **sim** |
| `F-FP-002` | `14 Sentença homologatória do laudo complementar.pdf` | 2.988.063 bytes | `02e3330f33365e611abcfb0a1d30ed1b88b1902e667a2bb59dfb8958ab4af7dd` | **sim** |

Esta reconfirmação prova identidade e integridade do arquivo no disco. Não prova, por si só, que o laudo é a fonte juridicamente prevalente nem substitui a conferência humana da transcrição; por isso `F-FP-001` permanece `validationStatus: proposto`.

### Canário sobre o artefato real

A execução direta de `validar_gates_economicos()` sobre o `_PLANO_TEXTO.txt` real, usando o ledger canônico atual e a raiz da fábrica como base, produziu **28 achados: 1 P0 e 27 P1**. O P0 foi exatamente `L9-fonte-prevalente` (`validationStatus: proposto`); os P1 restantes são valores ainda sem âncora U6. O documento econômico, portanto, continua bloqueado pelo motivo correto — não por ausência genérica de ficha nem por erro de integridade.

## 7. Limites que permanecem explícitos

Estes gates são escudos lexicais e estruturais. Eles verificam que uma fonte foi declarada, que o trecho e o arquivo existem, que o hash e a data-base são coerentes e que uma derivação bate com a fórmula registrada. Eles **não** decidem se o documento sustenta juridicamente a proposição, não substituem a leitura do advogado, não conferem a autenticidade processual por si só e não liberam a peça para protocolo.

Também não há contagem automática de páginas. O F8-S continua em observação e a decisão sobre paginação/legibilidade é humana no DOCX.

O recomputo F7 também não trata mais falha de parsing como ausência de insumo: JSON ilegível ou fora do objeto esperado produz `L0-recomputo-sem-insumo`, severidade P0 e `computed.status: fail`. A regressão cobre esse caminho e o nome do gate foi uniformizado em todo o código.

## 8. Como reexecutar sem usar renderização

Na raiz `_FORJA_HARNESS`:

```text
python test_forja_svg_docx.py
python test_forja_lastro.py
python test_forja_verificador.py
python test_forja_run.py
python forja_baseline.py --quiet --json telemetria\BASELINE_GATE_DOCUMENTAL_2026-08-04-final-v24.json
```

Para uma peça visual, usar `python forja_visual_build.py <markdown> <saida> [titulo]` e, quando o caso for econômico, fornecer `--case-dir`, `--ledger` e `--base-dir`. O resultado esperado é DOCX + `FIDELIDADE_VISUAL.json` + `F8_QA_ESTRUTURAL.json` + `VISUAL_BUILD.json`; a chave `renderingUsed` deve permanecer `false`. Para o pacote de revisão, executar `python forja_memoria_auditabilidade.py build <case-dir> --output-dir <case-dir>\pacote_revisao` e validar o manifesto com `python forja_memoria_auditabilidade.py validate <manifesto> --case-dir <case-dir>`.

## 9. Arquivos centrais e SHA-256

| Arquivo | SHA-256 |
|---|---|
| `forja_baseline.py` | `92D2C000D9B04E3DBD4B2927E3890D2E979AC7BEEB555C8ED76F1C7A3EE74C57` |
| `forja_regua.py` | `7621697F0D50E7411248357C0591589BFCA64C24F0323CB46C8CBADEB153F9C9` |
| `forja_gate_liveness.py` | `EBFB247ED7C16240DFAC5D24040A5010646A9BBB350E467849FC5DC64B82D8F2` |
| `forja_lastro.py` | `7B09F1EEE772DFBF0BB158D3AA34B4C09FE873B9E7D6F6E7EFAF3397D43B47FC` |
| `forja_run.py` | `2EBD9A273D26A7297FB3ABEFD59BB456C507A25653B6054803761BBDBCB81D45` |
| `forja_verificador.py` | `51F6E9C931B1872711819433631FFD66C1044711ACDD5FEB00D7939AA4B5B682` |
| `forja_visual_build.py` | `350E03BB7069A8B0055B3881A0338F2DD781D01AC6ABADF0D4643BEAD7E03843` |
| `forja_svg_docx.py` | `62C0A8A115DF0404FF85878D8F634E4E8C64F2E5D76B7B499F97D9107B20C183` |
| `forja_visual_qa_structural.py` | `7ED3FFFB645E83CEB744AC443F93E7F64C089D9C12274BF7D87193405D5DF8A0` |
| `forja_fidelity.py` | `58B642749707921F8E346283CCB44D0D85410764A2AC5AA5EC96DBB20AAD5473` |
| `test_forja_svg_docx.py` | `CDA13133942B3219EE4254A273700B5D65CEF707E986303EB2FB61BCDC4499C1` |
| `test_forja_lastro.py` | `DE39C6E8D60CE66DF653CC79A7D2C1D49AFE1D022E95B3725AF5B431D69F02B1` |
| `test_forja_gate_liveness.py` | `CFF2E296B67CFBB2E3CC1E54772CDD1732587D5FBE46E85B99024FBE609AD2AD` |
| `test_forja_lastro_rota_producao.py` | `1C7BFD03720D0751512AF73CFE80368AE95F566F1593E6D9F9FB96AE516113CD` |
| `test_forja_conselho.py` | `FCB5F0A6A110A52BEE739AC0BB031E14D95C55329B9F8FEDEF60571A86658030` |
| `test_forja_f8_gates_contrato.py` | `305E91C0E129209AAC6030AF2B0F4938DAEDA71D59751F02AB6AEFF938F307E9` |
| `test_forja_politica_citacoes.py` | `E9C9593EE360C2374521771A05432039A29CE8E344855BFB52EDC4D409EB3FEB` |
| `test_forja_identidade_citacoes.py` | `7FE7D77ECFD6307F871E7694C6DA78592604E0EB8221EEFD7CA9F596CE791324` |
| `test_forja_injection_gate.py` | `CA8988AC91078BE67126651A2A453752A82CBC15A4F6A3AB9476F6EF7D0847D6` |
| `forja_memoria_auditabilidade.py` | `9DC3FDEC38754589E30362F195EA1B42CA937195B2218982DFD8AE9CA45FEEF7` |
| `test_forja_memoria_auditabilidade.py` | `8843E3973DA19050830A30BBCDD93D8520A32A3A374619C58C5DFBF436E11D5A` |
| `test_forja_injection.py` | `C2D4B246BF20EDCEF8CFB71889963D29C32CAD855282946D897DE250365BA25D` |
| `forja_f8_contract.py` | `B69362DB3631DF823F92E4165B5D94F69C37D1DAD0BF65A4174282CB7DAEEA95` |
| `test_forja_f8_static.py` | `E1D9DB8229E95FCEE2A1F757F474DE0049BE965BB0ECC92D0CC225C4DE57C6AF` |
| `forja_package.py` | `D23900CC029B432DCE58F1A09198542608D8CD209D9CBCD08991E0806C47B354` |
| `forja_delivery.py` | `9E0EE447E7F33DB5A499590191DC60BC3415FFFBBD5E753EBD7F406A6B507A78` |
| `forja_injection_scan.py` | `9EA2A46AAB5F1BD6B185BAF265290E9B985A8B848ACDEA44F345A359462CA532` |
| `phase_contracts/F8.json` | `65A81C23D1F7F3B03632E223D4EE2D381662E6E6630D9E346C7709A970BE41AC` |
| `phase_contracts/F9.json` | `166B1A32125538C7570FCABE9DF47A400DD39D5302BBC07E92E2CAB2AF83EF42` |
| `test_forja_run.py` | `9765FC2097395CAE5AB6CD7BD08E8F6CFD893AB0DDB808F9FD6A734D430ED502` |
| `test_forja_verificador.py` | `6D6025512D14CA425524186CCCF7AAD2D4352D069058CC62D400580B4D46DD07` |
| `../_FERRAMENTAS/medina_visual_kit.py` | `0CF3F5CD3868458E1AD9103A41C66C357D4EBA412651343DA6A560AC1E8A1368` |

### Hashes da onda v22 (estado final revalidado)

| Arquivo | SHA-256 |
|---|---|
| `forja_baseline.py` | `12BCB83741CD37CD63CD8D7E405034919001D7BF9C485B09BF364AC30D388CB8` |
| `forja_run.py` | `4689A73A8B5633D78523E469544B561D4F5CAF65CAD0C08E53EA848EAF158802` |
| `test_forja_n3_runner.py` | `D9B9D732649D7E561ED9472118FC31AD3D6224F10F2AF75E5334C59981A0DD5D` |
| `test_forja_run.py` | `1D93B7091F8995F9B2735049BCE3574A7F939870ADA573F5EA8AFF579F8155D6` |
| `forja_entrega.py` | `0D5147D629868795FA809691E60721C9889B1D59E9970326965BC5D0D88D1AC9` |
| `forja_ingestao.py` | `7FAC1A20172147D361756BD1064B406A37C2BB8CBA7B543A80F5A818BA950ECB` |
| `forja_contexto.py` | `7360944F3128D8C48FFB013696DE9A0A898C4EC6E853C5266F05330272F0A054` |
| `forja_redacao.py` | `CCC1268F6D7843956082CADADB5C4264F09AC09CFB2C788A00C43EC2E4B4385D` |
| `forja_artefatos.py` | `A41728E59847FBE629D84AAC6B8D772D5037079AC501F610D4ABF09287E44817` |
| `forja_p0.py` | `598F689E46457D4B83E6109BB1F188CD4E916C9EF33E972B46AF6ADBD32D299B` |
| `forja_regimento_gate.py` | `2905A812FB0164793A72152D220A4F02E4F41D917F8061592F3404045B5F0325` |
| `forja_produto.py` | `9C48E354670B7A0B35FBC59EAC90813C8F63E1019654A63A5EF697D269EF0AB8` |
| `telemetria/BASELINE_GATE_DOCUMENTAL_2026-08-04-final-v20.json` | `8EDB91DFFAD83F30F7A2C58CA821F2C18DDAC69575455A653AAA024541E5E257` |
| `telemetria/BASELINE_GATE_DOCUMENTAL_2026-08-04-final-v21.json` | `268182764BD245C578E491D7B4164A4C4F4E162BEC3992A5B8221155B81397DD` |
| `telemetria/BASELINE_GATE_DOCUMENTAL_2026-08-04-final-v22.json` | `B303BCDE359472319CFD3575E6B2AADF5A193AA84935952CBF6BC6886385547A` |
| `telemetria/REGUA_2026-08-04_133952.json` | `A9AFA05CFF880E31A73ACF9E1D88AA36246EFFBCE928FCE029C774497F63AA8F` |
| `telemetria/REGUA_2026-08-04_135608.json` | `08575E0327DE3EE0CF55891A26EFAF4AFFD0A1798D44D9A9DEBD32B89F29324` |
| `telemetria/REGUA_2026-08-04_142640.json` | `26358AE4A6F2EEDF1C9FCCDB14A32ADD24137F5FA0636DD2D47D5A492B406874` |
| `telemetria/GATE_LIVENESS_2026-08-04-final.json` | `39EDEF4B9BC0D6E7719572104F1462029541D67548B64F9EA61D5855D38AB539` |
| `telemetria/GATE_LIVENESS_2026-08-04-final-v21.json` | `DCB7360D9692A93A28B56B3162E8F77FBDCB7F52474A0D40EB997AA6EBD46EE5` |
| `telemetria/GATE_LIVENESS_2026-08-04-final-v22.json` | `D537DB1E36C85B07A83E63D7D9E4248D6C0A65E9E2901434E97B1F4C235458EC` |
| `telemetria/REGUA_2026-08-04_151616.json` | `88F18FE8C45ADE8F59EB36CC41F4008E6F5A61A5CFDFCDC0D87C7A7B78849A14` |
| `telemetria/REGUA_2026-08-04_152032.json` | `B27D7F400494234839D88FB75249D4875D782C361355466147627FF3316763A1` |
| `state/case-cafelana-geral-reconstrucao-20260803/pacote_revisao/MEMORIA_AUDITABILIDADE_FORJA.json` | `AE944092021D75EC804F408DEB8369B5BBFB770FDED3C5FC1681FA551F02B1B9` |

### Hashes da onda v23 — fotografia histórica

| Arquivo | SHA-256 |
|---|---|
| `forja_baseline.py` | `F709E7D10220FC3B7F329D4015126F5D032841983EDFF4D22E8B964860E1944E` |
| `forja_docx_layout.py` | `FBB7531BA5E8842A4F849B58C07EC471BA7BF0ED47F7178605384D477A77EFBD` |
| `forja_lastro.py` | `7B09F1EEE772DFBF0BB158D3AA34B4C09FE873B9E7D6F6E7EFAF3397D43B47FC` |
| `forja_injection_scan.py` | `9EA2A46AAB5F1BD6B185BAF265290E9B985A8B848ACDEA44F345A359462CA532` |
| `forja_visual_build.py` | `41F977EEF75DBA7B23F55E65922FF268433DB5723ED91F48DE1AE6988F35172B` |
| `test_forja_f8_pecas_reais.py` | `308DCBFE1274018C32BA1B5A73B4F4DCD668D3EFC669533D248E3DE631E0F227` |
| `test_forja_canario_catraca.py` | `6EBF0C25F54C1D99AB34B9AAA28C4F3984CB1C7566751C3210C69CBA8E6255DA` |
| `test_forja_canario_mutacao.py` | `13A1A464F58C90A97875B35A39B4F6710E6430BE151C3664D976B18354C20416` |
| `test_forja_recomputo_censo.py` | `0F15076C8F9D086E571B2D9046105FEB987B805816DAC441039778FABF7012C2` |
| `test_forja_visual_build_peca_longa.py` | `4344C1ABB89529259A8A91927B344A846E868B42FFDD670C61507250A003D0EF` |
| `telemetria/BASELINE_GATE_DOCUMENTAL_2026-08-04-final-v23.json` | `6FE0DFC50044D94323A24665B6480B87AEA8CAA03127D731A7B75CA522931A9A` |
| `telemetria/REGUA_2026-08-04_224349.json` | `3C114958FBB097C1347333B405EB6E04039CF5236D746E939A0AD377C0F402E2` |
| `telemetria/GATE_LIVENESS_2026-08-04-final-v23.json` | `9B190E320AB97FB03881F6CC8513B7A5D03A94CC9ED77DB5E02A12D9A81B1A7F` |
| `REGUA_MANIFEST.json` | `D8E5C3CC9B555882B0BE7F8EE45F9BB54EF57E6A3AF3C2AF575FDEF7750CD268` |

### Hashes da onda v24 — fotografia da execução rápida (23:03–23:06)

| Arquivo | SHA-256 |
|---|---|
| `forja_baseline.py` | `2927F65FC2C5022DF04410A00B0565B963D243F58BAE3CA32A9841A973F0C16C` |
| `forja_baseline_aprovado.py` | `8E421061BBE0CBEAB3E2697AEE9BA53B3888E7C46DEED603F8667E5CC160F855` |
| `test_forja_baseline_aprovado.py` | `FC9B34932C50CB4588C6C745EB1208F2A208AACB29EC7BE5373F8D591CF065F1` |
| `test_forja_layout_antimoldagem.py` | `4E2DD041514BF9E9AC949F2735A62E04A87401C360FDF84FCDE4C8687C41FB94` |
| `forja_regua.py` | `ED518EDF67F2C2F049D2EE4F5D91AEAB277155A19C210E82FF3295ACB184D8FE` |
| `BASELINE_APROVADO.json` | `F8360C72DEAD2A5145554D2E03A81F256CB1A181B268D8A440E38E6CDAB3E0B7` |
| `telemetria/BASELINE_GATE_DOCUMENTAL_2026-08-04-final-v24.json` | `9CD58BF574E0839986458B92EBFDFA20A60EFC1DCA1F8E4E0AA2D6DB05C6FE73` |
| `telemetria/REGUA_2026-08-04_230635.json` | `010C83A3EA8F8FD56C863763982B39942F523510CCAA388B5915C73E66793899` |
| `telemetria/GATE_LIVENESS_2026-08-04-final-v24.json` | `9B190E320AB97FB03881F6CC8513B7A5D03A94CC9ED77DB5E02A12D9A81B1A7F` |
| `REGUA_MANIFEST.json` | `D689ECD094E74BE8FB500366F461E2FF5CD3DCB5798CE46715FD795D32224635` |

**Próxima ação necessária:** conferência humana da fonte prevalente Cafelana e decisão do advogado sobre a peça; sem essa confirmação, o estado permanece bloqueado e este relatório não deve ser lido como autorização de envio.

**Revalidação posterior (04/08/2026, 13:56):** a régua rápida foi repetida sem alteração de código e confirmou novamente 93 arquivos protegidos e 24 suítes aprovadas em 50,5 s. O registro corrente é `telemetria/REGUA_2026-08-04_135608.json`; a execução de 13:39 permanece como evidência histórica da mesma versão.

**Onda posterior de gates computados (04/08/2026, 14:26):** o Opus integrou recomputação de proveniência por parágrafo, fontes oficiais, red team, emissão F8/F10 e rota de lastro. Após corrigir a materialização do `COMPUTED_LASTRO_GATES.json` e classificar três scripts standalone, o baseline v21 ficou em **60/60 suítes, 542 testes pytest, 60 subtestes e 18 regressões**. A régua atual ficou em **100 arquivos protegidos, 28 suítes, APROVADO em 52,2 s**. A liveness passou a **43 computados, 30 autodeclarados, 0 inexequíveis e 17 não exercitados**; os 17 têm produtor, mas ainda não têm execução histórica F8/F10.

**Onda final de gates de entrada, produto e entrega (04/08/2026, 15:16–15:20):** foram integradas as recomputações de ingestão/exploração F1/F2, contexto F7, redação F6, inventário de artefatos, P0, regimento, produto, reconciliação F0 e entrega F9. A auditoria encontrou e corrigiu a incompatibilidade entre `reconciliation_report` em Markdown e o parser JSON do runner, sem relaxar o bloqueio de manifesto vazio; o teste direcionado do runner fechou 14/14. O baseline v22 fechou **68/68 suítes, 542 testes pytest, 60 subtestes e 26 regressões standalone** (`telemetria/BASELINE_GATE_DOCUMENTAL_2026-08-04-final-v22.json`). A régua rápida confirmou novamente **116 arquivos protegidos, 36 suítes e APROVADO em 51,9 s** (`telemetria/REGUA_2026-08-04_152032.json`); a execução de 15:16 permanece como evidência da mesma versão. A liveness atual registrou **65 gates computados, 8 autodeclarados, 0 inexequíveis e 17 não exercitados** (`telemetria/GATE_LIVENESS_2026-08-04-final-v22.json`).

**Onda de QA real, mutação e liveness total — fotografia histórica (04/08/2026, 22:41–22:43):** o inventário passou a incluir os canários de catraca e mutação, o censo de recomputação, as âncoras F8 em peças DOCX reais e o smoke test de peça longa com SVG. O baseline v23 fechou **78/78 suítes, 545 testes pytest, 60 subtestes e 36 regressões standalone** (`telemetria/BASELINE_GATE_DOCUMENTAL_2026-08-04-final-v23.json`, SHA-256 `6FE0DFC50044D94323A24665B6480B87AEA8CAA03127D731A7B75CA522931A9A`). A régua rápida confirmou **130 arquivos protegidos, 46 suítes e APROVADO em 127,6 s**, em modo rápido sem bateria real (`telemetria/REGUA_2026-08-04_224349.json`, SHA-256 `3C114958FBB097C1347333B405EB6E04039CF5236D746E939A0AD377C0F402E2`). A liveness examinou 111 resultados e chegou a **73 gates computados, 0 autodeclarados, 0 inexequíveis e 17 inertes históricos** (`telemetria/GATE_LIVENESS_2026-08-04-final-v23.json`, SHA-256 `9B190E320AB97FB03881F6CC8513B7A5D03A94CC9ED77DB5E02A12D9A81B1A7F`). A onda permaneceu sem PDF, PNG ou renderização e não alterou o bloqueio humano da Cafelana; foi sucedida pela fotografia v24 abaixo.

**Fechamento anti-moldagem e baseline aprovado (04/08/2026, 23:03–23:06):** o novo canário de layout estragou deliberadamente uma peça aprovada em quatro dimensões e o gate acusou todos os quatro defeitos; o canário do baseline aprovado conferiu três âncoras intactas com o mesmo veredito. O baseline v24 fechou **80/80 suítes, 545 testes pytest, 60 subtestes e 38 regressões standalone** (`telemetria/BASELINE_GATE_DOCUMENTAL_2026-08-04-final-v24.json`, SHA-256 `9CD58BF574E0839986458B92EBFDFA20A60EFC1DCA1F8E4E0AA2D6DB05C6FE73`). A régua rebaselinada fechou **134 arquivos protegidos, 48 suítes e APROVADO em 137,1 s**, em modo rápido sem bateria real (`telemetria/REGUA_2026-08-04_230635.json`, SHA-256 `010C83A3EA8F8FD56C863763982B39942F523510CCAA388B5915C73E66793899`). A liveness v24 manteve **73 gates computados, 0 autodeclarados, 0 inexequíveis e 17 inertes históricos** (`telemetria/GATE_LIVENESS_2026-08-04-final-v24.json`). A alteração não promoveu a fonte prevalente nem liberou a peça.

**Reexecução completa posterior (04/08/2026, 23:07):** sem alteração de código, a régua repetiu as 48 suítes rápidas e a bateria real da Lição 41. Resultado: **134/134 hashes íntegros, 49 registros de suíte e APROVADO em 137,3 s**, em `telemetria/REGUA_2026-08-04_230706.json` (SHA-256 `BAB7571C0398E9C783D2B7B69EB68FE788C0500004BFAEBD0AD7E9DEEDB6D310`). A execução confirma o estado corrente; a atualização posterior dos documentos apenas reconciliou os ponteiros, sem alterar código, casos ou decisão humana.

## Revisão cruzada Codex de 04/08/2026 — 17 achados, 12 corrigidos, 5 declarados como limite

A revisão adversarial independente (família de modelo distinta, lendo o código, sem alterar arquivos) devolveu 17 achados. O mais grave derruba a premissa do trabalho de 03/08: **o recomputo de lastro do F7 nunca executou**. Procurava o artefato `fact_ledger`, que o contrato F7 não exige e nenhuma execução emite — o ledger de fatos nasce em F3 e é promovido para `n3_artifacts/`. Medição: 7 fases F7 no acervo, zero `COMPUTED_LASTRO_GATES.json`.

### Corrigidos, com canário

| # | Achado | Correção |
|---|---|---|
| 1 | recomputo inerte por nome de artefato | descoberta do ledger promovido a partir do caminho da tentativa; ausência vira achado |
| 2 | `economic_gates=fail` não bloqueava | flag passa a distinguir severidade (`fail` só com P0, `warn` com P1); runner bloqueia em `fail` |
| 3 | ledger vazio, `{}` ou chave `claims` passava | `L0-ledger-vazio` e `L0-ledger-vocabulario`, ambos P0; `None` deixou de estourar |
| 4 | status ausente escapava de L1/L2 | `L1-status-ausente` P1 |
| 5 | `quoteSource` aceitava `../` e absoluto | confinamento à pasta do caso; L9 falha fechado |
| 7 | L11 gameável por `>` ou aspas | tipografia sozinha deixa de ser citação: gera `L11-isencao-tipografica` P2 e mantém o valor na conferência `L11-valor-orfao` |
| 9 | `caseFolder` ausente deixava L12 sem inventário | resolvido pelo `FORJA_CASE_MANIFEST.json` |
| 11 | operação desconhecida no L13 caía na multiplicação | `add`/`multiply`/`subtract` explícitos; desconhecida vira achado |
| 13-14 | escritores de DOCX one-off sob `state/` | conjunto congelado; escritor novo reprova a regressão |
| 16 | `inserir_svgs` regrava o DOCX após o último gate | invariante: a única diferença legítima é o desaparecimento dos marcadores |
| 17 | elo 9-B isentava status desconhecido | só status declaradamente isentos saem da lista |

Efeito colateral do #9, medido: com a pasta do cliente resolvida, o L2 deixou de acusar "fonte não localizada" contra transcrição correta. O que restou levou a uma distinção nova — `quoteSource` usado como nome legível da fonte ("Portaria Normativa PGU/AGU nº 29") não é arquivo sumido, e passou a ser `L2-transcricao-manual`.

O detector do #13-14 encontrou, na primeira execução, um quarto escritor que a própria revisão Codex não viu, com consequência real. Ver o adendo de 04/08 em `INCIDENTE_VALE_TRADING_LASTRO_APARENTE_2026-07-26.md`.

### Correção adicional após a revisão Diabob

- **#10 fechado:** `validar_gates_economicos(..., exigir=False)` agora emite `L0-economico-desativado` P0 quando o texto contém material econômico. A contraprova entrou no T2; texto não econômico continua sem incidência. O caso foi catalogado como `MC-19`.
- **#11 fechado:** a memória de auditabilidade normaliza aliases históricos de F1/F4/F5/F6 para os identificadores canônicos dos contratos, inclusive no histórico e na fase corrente, e explicita o ledger canônico separado do snapshot histórico. A regressão passou a 4 testes; o caso foi catalogado como `MC-20` e a memória real da Cafelana foi regenerada/validada.
- **#12 fechado (snapshot intermediário):** a saída da regressão passou a nomear todos os blocos que formam o total — então `12 + 11 + 16 + 21 + 28 = 88` — em vez de deixar os cenários do Plano 41 implícitos. O caso foi catalogado como `MC-21` e registrado na Lição 125.
- **#13 fechado (snapshot intermediário) na continuação Diabob:** `PecaVisual` não trata `ledger_path` explicitamente ausente como opção de autodiscovery; fixa ledger vazio, bloqueia L9–L13 e remove qualquer DOCX parcial. T11 acrescentou duas contraprovas, levando a regressão a 90 verificações; o caso foi catalogado como `MC-22` e registrado na Lição 126. O baseline histórico daquele registro consolidava 92 verificações, 51 suítes e 9 regressões; a execução intermediária v18 ampliou a cobertura para 53 suítes e 11 regressões, antes da inclusão da suíte de política de citações no v19.

### Limites declarados, não corrigidos

- **#6** `validadoPor`/`validadoEm` continuam nominais. O hash prova que o arquivo não mudou e o confinamento prova que ele está no caso; que a fonte eleita seja a correta é ato humano nomeado, por decisão de protocolo — não há recibo externo.
- **#8** `.txt` binário pequeno ainda é lido como texto com `errors="replace"`. Risco residual estreito: exige um arquivo que contenha a sequência da citação.
- **#12** L13 não liga o resultado recomposto ao número exibido quando os rótulos divergem.
- **#15** `forja_pilot_m4.py` grava DOCX antes de verificação documental, em pasta de piloto, fora da rota de entrega.

Regressão: 98 verificações atuais em `test_forja_lastro.py`, cuja saída decompõe 12 detecções + 11 não-travas lexicais + 16 de ledger + 22 de acoplamento + 37 cenários do Plano 41, 11 em `test_forja_run.py`, 4 em `test_forja_memoria_auditabilidade.py`, contraprova de snapshot em `test_forja_verificador.py`, contraprovas de `ledger_path` explícito presente e ausente na rota `PecaVisual`, contraprova de bypass econômico, contraprova de lavagem por referência posterior, tipografia sem origem mantida na âncora, contraprovas não econômicas nas rotas direta/canônica, régua rápida APROVADO.

## Revisão Diabob complementar de 04/08/2026

O parecer independente está em `RELATORIO_REVISAO_DIABOB_GATE_DOCUMENTAL_2026-08.md`. Ele encontrou `MC-18`: o verificador visual podia capturar um `fact_ledger.json` canônico inválido e cair para um snapshot histórico válido. A correção encerra a descoberta com ledger vazio, força P0 em L9–L13 e deixa snapshot apenas como fallback quando o canônico não existe. A continuação da auditoria fechou também `MC-19`: um caller não pode desligar L9–L13 em texto econômico. As contraprovas rodam em `test_forja_verificador.py` e `test_forja_lastro.py`.

O parecer Diabob não muda o limite de governança: a fonte Cafelana continua `proposto`, e nenhuma aprovação jurídica, protocolo ou comunicação externa foi inferida. A memória real validada está em `state/case-cafelana-geral-reconstrucao-20260803/pacote_revisao/` e não contém autos, segredos ou caminhos absolutos. A contraprova nova também confirma que um `ledger_path` explícito ausente bloqueia antes de qualquer gravação, ainda que exista ledger válido no caso.

## Atualização corrente — 05/08/2026, 01:00–01:06

Esta seção substitui os números anteriores como fotografia de execução; as ondas
v20–v24 permanecem acima como histórico. O baseline controlado e a régua completa
foram executados depois da correção da porta única e da classificação explícita dos
canários. A rota continua sem PDF, PNG, Word COM ou renderização.

- **Baseline v25:** `telemetria/BASELINE_2026-08-05_011824.json`, 83/83 suítes,
  545 testes pytest, 60 subtestes e 41 regressões standalone, aprovado. A execução
  controlada equivalente está em
  `telemetria/BASELINE_GATE_DOCUMENTAL_2026-08-05-final-v25.json`, SHA-256
  `92F00A45F0F1A0AF3017BEF10A257283BA2ED1F6E69147B375F3D6D4CCE4250A`.
- **Régua rápida:** 140 arquivos protegidos, 51 suítes, 141,0 s, aprovado em
  `telemetria/REGUA_2026-08-05_010327.json`.
- **Régua completa:** 140/140 hashes íntegros, 52 registros (51 suítes + a bateria
  real da Lição 41 com `--sem-render`), aprovado em 148,1 s. Evidência:
  `telemetria/REGUA_2026-08-05_010600.json`, SHA-256
  `DEBE45FE6385C8F192D2DF3679FB9CCB2170EFDEABB88731976F343F1D1CEEEB`.
- **Liveness:** 111 resultados, 73 gates computados (100%), 0 autodeclarados, 0
  inexequíveis e 17 não exercitados históricos, em
  `telemetria/GATE_LIVENESS_2026-08-05-final-v25.json`.
- **Canário F8-S:** `test_forja_assinatura_antimoldagem.py` acusou as seis
  destruições deliberadas. O próprio teste registra a limitação: ainda não prova
  resistência à adição adversarial de elementos vazios.
- **Porta única:** `test_forja_porta_unica.py` passou; `PecaVisual.salvar()` grava
  `<peça>_PORTA_UNICA.json` e bloqueia placeholder, origem operacional, regimento e
  lastro. Achados `G10-escrita-humana` ficam no laudo como observação e não travam
  a persistência, conforme calibração documentada.
- **Adoção:** o medidor hash-bound, após colapsar 20 cópias, encontrou **1 de 40
  obras (2%)** atravessando a rota canônica. A porta única cobre os DOCX que passam
  por `PecaVisual.salvar()`, mas a maioria da produção ainda não usa a rota que
  tem os gates; este é o principal risco operacional aberto.

O estado jurídico permanece inalterado: `F-FP-001` segue `proposto`, Cafelana segue
`blocked` na revisão 177, e não houve promoção, protocolo, envio ao advogado ou
qualquer decisão humana inferida pela régua.

### Correção final de proveniência do F8-S — 05/08/2026, 01:11–01:13

O laudo do contador de páginas não usa mais o rótulo `pdf_renderizado`, que era
impreciso. `forja_assinatura_visual.py` agora informa `pdf_existente_ao_lado`
quando apenas lê um PDF já existente para obter a contagem, distingue
`parametro_do_chamador` quando a página foi fornecida explicitamente e mantém
`desconhecida` sem prova. Nenhum PDF é criado e nenhum renderizador é chamado.

As contraprovas direcionadas permaneceram verdes: `test_forja_assinatura_visual.py`
5/5, `test_forja_assinatura_antimoldagem.py` com seis destruições acusadas e
`test_forja_porta_unica.py` aprovado. O rebaseline registrou a alteração no
manifesto; a régua completa final confirmou **139/139 arquivos protegidos, 52
registros e APROVADO em 138,2 s**, em
`telemetria/REGUA_2026-08-05_011415.json` (SHA-256
`0A7CAFCD8F294712D46C101F0D2883633A27E0D1543DD82C519244A3AC22AAC2`).
