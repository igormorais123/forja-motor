# AUDITORIA ULTRACODE DA RODADA FORJA N3 — 10/07/2026 (tarde)

**Método:** 12 auditores independentes (1 por entrega + 1 de integridade da gestão), cada achado P0/P1 submetido a verificador adversarial independente instruído a REFUTAR; 56 agentes no total; checagens manuais finais sobre os achados divergentes. Fontes: artefatos reais no disco, fontes oficiais locais, verificador determinístico (`forja_verificador.py`), fontes oficiais online quando a divergência exigiu (ER 53/2026).

**Balanço:** 44 achados P0/P1 levantados → 26 confirmados pela verificação adversarial → 2 desses caíram em checagem manual final (margens visual law; MS 26.106/DF). ~45% dos achados iniciais eram falsos positivos — a verificação adversarial pagou.

## 1. Veredito executivo

A rodada N3 é substancialmente sólida no eixo jurídico: nenhuma peça teve erro de tese, citação inventada ou premissa fabricada confirmados. Os defeitos reais encontrados foram (a) um erro de fato normativo do próprio sistema de controle (art. 343-A), (b) uma contaminação sistêmica de metadados, (c) duas exposições de processo interno, e (d) um risco operacional grave de versão: **o Fábio está com a versão errada dos memoriais Patrícia/Fábio**.

## 2. Correções APLICADAS nesta auditoria

| # | Correção | Onde |
|---|---|---|
| 1 | **Regra invertida do art. 343-A**: o RISTJ CONTÉM o art. 343-A desde a ER 53/2026 (DJe 01/07/2026 — resumo obrigatório nas petições ao STJ). Regra do verificador corrigida (agora só flagra 343-A atribuído a TJ/TRF); ER 53 capturada no cache de fontes oficiais; nota apensa às 4 cópias locais do regimento STJ; testes de regressão atualizados (13 detecções + 11 não-travas, verde) | `forja_verificador.py`, `cache/fontes_oficiais/STJ_ER_53_2026_DJe_2026-07-01.pdf`, regimentos locais |
| 2 | **Metadados sistêmicos**: 15 DOCX + 15 PDFs sanitizados (autor "thais mulati"/título "Proposta de Serviços e Honorários" herdados do template em TODAS as 11 peças N3 e cópias de entrega). Causa raiz corrigida: `PecaVisual.salvar()` agora sanitiza sempre | `medina_visual_kit.py` + artefatos |
| 3 | **Cafelana AgInt — metodologia interna exposta**: removidas as 3 frases "…pelo escritório" (síntese, cronologia, cotejo); peça re-renderizada via Word COM com fidelidade 100% e QA 10/10 páginas; verificador 0 violações | `MINUTA_CAFELANA_AGINT_N3_FONTE.md` + DOCX/PDF |
| 4 | **Jorge Haroldo item 27 — pincites completados**: MS 26.106/DF verificado no Informativo STJ 25E (Primeira Seção, Rel. Min. Marco Aurélio Bellizze, j. 5/6/2025, DJEN 13/6/2025) e precedente do Informativo 870 (Rel. Min. Paulo Sérgio Domingues, j. 2/10/2025, DJEN 7/10/2025) — ambos agora com relator/data/DJEN na peça; re-renderizada, fidelidade 100%, QA 10/10 | `MINUTA_EDCL_JORGE_HAROLDO_N3_FONTE.md` + DOCX/PDF |
| 5 | **Falso positivo de links markdown** no gate de placeholder corrigido + teste de regressão | `forja_verificador.py`, `test_forja_verificador.py` |
| 6 | **Gestão reconciliada**: pasta do Azimut corrigida (Fwd→Re); alerta urgente na demanda Patrícia/Fábio; nota de auditoria nas 2 cumpridas por marcação manual sem comprovante; `respondidoComConteudo=false` na demanda WhatsApp "não é tarefa"; painel re-renderizado; reconciliação FORJA×gestão limpa | `demandas.json`, painel |
| 7 | **Pareceres F4 canônicos** criados para Libra Sul e Patrícia/Fábio (com nota de proveniência honesta: conselho atuou como revisão corretiva em 10/07, depois da 1ª redação) | `state/<caseId>/F4_PARECER_*.md` |
| 8 | **Natura**: responsável nominal (Igor, escalação Fábio) + Plano B com marco de 14/07 registrados no parecer Helena (prazo do parecer: 20/07) | `PARECER_HELENA_N3.md` |
| 9 | **Erratas** apensas aos dois relatórios da rodada + Lições 45-48 na RETROSPECTIVAS | `reports/`, `RETROSPECTIVAS.md` |

**Pendência técnica (1 comando):** 2 PDFs continuam com metadado antigo porque estão abertos no PDFelement (Mateus V6 e Libra Sul N3). Fechar o programa e rodar `python _FORJA_HARNESS/sanitize_pdfs_pendentes.py`.

## 3. O que exige DECISÃO HUMANA (Igor/Fábio) — em ordem de urgência

1. **Patrícia/Fábio (sessão 14/07):** reenviar ao Fábio a N3 corrigida em substituição à versão de 03:42, que ainda pede majoração de honorários recursais (erro removido pela N3). O painel está com alerta urgente. Nenhum reenvio foi feito pela auditoria — decisão de comunicação é humana.
2. **Deltan:** confirmar com o consulente (Leandro Souza Rosa, OAB/PR 30.474) o cargo pretendido (deputado federal × Senado) e obter certidão CNMP reconciliando a Sindicância 1.00145.2020-06 × -16. Sem isso, não liberar versão externa.
3. **Jorge Haroldo:** bloqueadores de protocolo mantidos (corretos): ler as peças do Drive (28 links sem acesso), confirmar a formulação exata da sanção no título e a devolução específica do capítulo da aposentadoria no agravo interno.
4. **Cafelana (EDcl e AgInt):** conferências no PJe antes de protocolo — ids 461442081/459633274/452695224, relator/órgão atual, estado do AREsp 2.698.443/DF, vigência das OABs dos 5 signatários, data do fecho no dia do protocolo.
5. **Libra Sul:** localizar fls. da Tomada de Contas Final (evento 273, OUT5, fls. 61/63 — já rastreada nos autos) e decidir se entra pincite; confirmar pauta/modalidade/fecho.
6. **Natura (prazo 20/07):** liberar o acesso ao caderno do Drive até 11/07; se não chegar até 14/07, ativar o Plano B registrado.
7. **Mateus/SulAmérica V6:** protocolável após procuração conjunta, manifesto de provas e relatório bucomaxilofacial atual (bloqueadores já listados pela própria FORJA — confirmados corretos).

## 4. Falsos positivos relevantes derrubados (para não retrabalhar)

- **Margens 2,5/5,4 das peças N3**: desenho deliberado da edição visual law (corpo 13,1cm + margem de pull quotes) — padrão aprovado `padrao-visual-medina`. Não corrigir.
- **MS 26.106/DF "não conferível"**: verificado no Informativo STJ 25E na própria pasta do caso.
- **Data "7 de agosto de 2026" no Jorge Haroldo**: deliberada — prazos do STJ suspensos de 2 a 31/07 (Portaria STJ/GP 455/2026), reinício 3/08.
- **Personas "Controles Cícero/Helena" no dossiê Roraima**: documento interno de descoberta em F0, não entregável — gate não se aplica.
- **REsp 1.795.982/SP (Patrícia)**: citação vem dos autos e foi conferida no SCON (documentado no relatório de melhorias de 09/07).
- **Citações Jorge Haroldo (REsp 2.107.601/MG e AgInt REsp 1.558.863/RJ)**: conferidas palavra a palavra nos PDFs oficiais locais — corretas.

## 5. Qualidade das entregas bloqueadas (Natura/CORSAN)

Confirmado o acerto da decisão de NÃO inventar conclusão: os dois estudos são honestos sobre o que falta, com matriz acionável. Melhorias sugeridas de baixa prioridade registradas nos achados P2 (síntese metodológica no roteiro Natura; priorização de coleta por impacto no CORSAN — TAACC + Resolução 69/2024 + Edital 01/2022 cobrem ~80% da matriz A01-A54).

## 6. Roraima

Dossiê de descoberta apropriado. Sugestões P2: citar art. 54 da CF nos controles de conformidade (incompatibilidades de parlamentar) e carimbar data/método de verificação das fontes do Senado se o documento circular além do uso interno.

## 7. Adendo — defeitos achados e corrigidos DEPOIS do fechamento do workflow (QA de amostra manual)

| # | Defeito | Correção |
|---|---|---|
| 10 | **Título de card estourando a borda** (só o zoom pegou): "4 FUNDAMENTOS"/"1 SEM ATAQUE" (Cafelana AgInt), "PROVEITO REAL" (Cafelana EDcl), cards "R$ ..." (Patrícia). Causa: `cards_ancora` usava fonte fixa 15pt | Auto-ajuste de fonte no `medina_svg_kit.cards_ancora` (piso 9pt); 3 peças re-renderizadas via Word COM; páginas 1 reconferidas visualmente — títulos íntegros |
| 11 | **Hashes SHA-256 defasados** após sanitização/re-render (o painel valida hash antes de abrir) | 8 registros atualizados em `forja_status.json` com carimbo de revalidação; painel re-renderizado |
| 12 | **Cópia de revisão da Patrícia desatualizada** em Anexos do email | Substituída pela N3 re-renderizada (mesmos nomes) |

Total de re-renders Word COM na auditoria: 5 (Cafelana AgInt ×2, Jorge Haroldo, Cafelana EDcl, Patrícia/Fábio), todos com fidelidade 100% e QA página a página.
