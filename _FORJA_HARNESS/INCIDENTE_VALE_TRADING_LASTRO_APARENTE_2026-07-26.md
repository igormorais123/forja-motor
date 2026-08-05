# Incidente Vale Trading — lastro aparente e endurecimento da FORJA

Data da correção: 26/07/2026. Caso `case-email-auto-19f8cec883a0ac31` (consulta técnico-pericial, liquidação 5020376-80.2018.4.04.7100/RS, 13ª Vara Federal de Porto Alegre, TRF4). Este registro não altera o conteúdo jurídico do caso: documenta a falha, o que a produziu, o que foi corrigido e os gates criados para impedir recorrência. Segue a linha do `INCIDENTE_NATURA_QA_VISUAL_2026-07-21.md`.

Nenhuma peça foi enviada, protocolada ou liberada com os erros descritos. Todos foram detectados antes da entrega e o caso permanece `internal_working`, bloqueado em F7 pelos dois gates humanos.

## O que aconteceu, em uma frase

Três camadas de revisão devolveram **zero P0** sobre uma minuta que continha **quatro P0**. Todas as três examinaram o texto. Os erros estavam na fonte, e a fonte não tinha sido aberta.

## As três camadas que falharam juntas

| Camada | O que fez | O que devolveu |
|---|---|---|
| Red team interno (9 perguntas do U4, ampliado para 12) | leu a minuta e procurou fragilidade argumentativa | zero P0 |
| Gate F7 automático | rodou os gates determinísticos sobre o texto | zero P0 |
| Revisão cruzada externa (Grok 4.5 + Sol 5.6, famílias distintas) | leu a minuta e formulou objeções | zero P0 sobre os quatro erros reais |

A revisão cruzada entre famílias funcionou para o que ela sabe fazer — Sol 5.6 pegou dois erros que eu havia **introduzido ao incorporar um achado forte**, e isso está registrado como acerto. O que nenhuma das três camadas podia pegar é o que não estava no texto: uma proposição bem escrita, com localizador plausível, cuja fonte diz o contrário.

## Os quatro P0

### 1. Identidade de liquidação inexistente (o mais grave)

O § 16 afirmava que o AI 5039469-52.2019.4.04.0000 tratava "das mesmas partes e da mesma liquidação". Eram liquidações distintas: aquele agravo veio da liquidação 5072582-42.2016.4.04.7100, da Pamper. A afirmação de identidade processual é conclusão jurídica sobre dois documentos, e foi produzida por semelhança.

Origem: `fact_ledger` F012, marcado `confirmed_document`, com apoio em `E252-ANEXO-AI-p20-31`. A página existia. O documento existia. O documento dizia outra coisa.

### 2. Norma inexistente

"Normas de 2002, 2016 e 2018" — a de 2018 nunca existiu. Abrir o laudo mostrou as normas reais: Lei 10.637/2002, Decreto 5.172/2004, Decreto 8.950/2016, Lei 9.430/1996 e IN RFB 2.022/2022. O ano solto tinha aparência de precisão e não apontava para norma alguma.

### 3. "Confirmada em todas as instâncias"

O REsp 780.605/RS **não foi conhecido** em 12/12/2006. Não conhecer recurso não é confirmar mérito — o tribunal superior não substitui o acórdão recorrido. A formulação correta, adotada, é "via recursal esgotada, acórdão incólume".

Este erro e o seguinte foram **introduzidos por mim ao redigir a incorporação de um achado forte**, não herdados do ledger. Estão registrados como Lição 87 em `RETROSPECTIVAS.md` e na memória persistente da sessão (`forja-licao-achado-forte-gera-excesso`).

### 4. Denominador trocado no meio da frase

"93% dessa distância" — o denominador da primeira metade da frase não era o da segunda. Substituído por enunciado que declara exatamente o que a conta demonstra.

## Um quinto, encontrado pelo próprio gate novo

Ao coletar as transcrições verbatim exigidas pelo gate L1, apareceu um **misquote** (modo 3 da taxonomia U1): o F017 dizia que o TRF4 havia adotado a data do Siscomex. O acórdão cita o Siscomex "por exemplo" e mantém o critério "data de comprovação/efetivação da operação". Corrigido no ledger e no § 38.

O gate encontrou um erro que as três camadas de revisão não tinham encontrado, no primeiro uso, antes de estar acoplado. Isso é a evidência mais direta de que o eixo escolhido está certo.

## Causa sistêmica: lastro aparente

A falha comum não foi invenção do nada. Foi **afirmação marcada como confirmada em documento, com localizador plausível, cujo localizador ninguém abriu**.

O diagnóstico que o sistema não tinha:

> Citar o localizador não é ter lido o localizador.

Um modelo que precisa apenas indicar a página pode produzi-la com aparência perfeita. Um modelo obrigado a colar o trecho tem de abrir a fonte. A transcrição verbatim é a única prova barata de leitura — e virou o eixo do gate L1.

## O que foi corrigido no caso

Todos os artefatos abaixo estão em `state/case-email-auto-19f8cec883a0ac31/n3_artifacts/`, nas pastas de fase indicadas.

- `F3_FONTES_REGIMENTO_LEIS/fact_ledger.json` reconstruído na origem: de 12 para **30 fatos** e 4 limites; F012 corrigido com a alegação falsa **preservada** no campo `correction` (previousClaim, motivo, severidade, quem detectou), 19 fatos com transcrição verbatim e 11 declarados pendentes em vez de suprimidos;
- `F6_REDACAO_TEMPLATE/draft_markdown.md` refeito de v1 a v6 (42 → 78 parágrafos), com capítulo autônomo novo sobre a delimitação já fixada nos autos;
- `F7_AUDITORIA_JURIDICA_FACTUAL/nota_tecnica_escala_monetaria.md` criada: a quebra de escala monetária de janeiro de 1989 no Anexo I (valor em cruzados multiplicado por índice de cruzados novos), reproduzida à vírgula sobre os próprios números do anexo — a linha afetada é 93,37% do principal;
- `F7_AUDITORIA_JURIDICA_FACTUAL/revisao_multimodelo_v5.md` registrando cada objeção externa como acatada, parcial ou rejeitada, com motivo;
- `F7_AUDITORIA_JURIDICA_FACTUAL/f7_gate_result.json` v7, com `familyAssurance: cross_family`, 18 citações conferidas nominalmente e bloco `grounding`.

## Controles incorporados ao sistema

1. **`forja_lastro.py` (FORJA-LASTRO-v1)** — oito gates, cada um ancorado em uma falha real desta execução, sem gate especulativo. Protocolo completo em `PROTOCOLO_LASTRO_DOCUMENTAL.md`.
2. **Elo bloqueante 9-B no `forja_delivery.py`** — `fatos_sem_lastro()` impede o fechamento da demanda enquanto houver fato de status documental sem transcrição.
3. **`fact_grounding_verbatim` nos `requiredGates` do `phase_contracts/F7.json`**, com o registro da âncora em `gateNotes`.
4. **`test_forja_lastro.py`** — 37 casos: 12 detecções, 11 não-travas, 10 de ledger e 4 de acoplamento. O bloco de acoplamento verifica que o gate está de fato ligado ao contrato, à entrega e ao verificador, não apenas importável.
5. **`forja_regimentos.py` (FORJA-REGIMENTOS-v1)** — a auditoria de atualidade dos regimentos deixou de ser varredura manual. Runbook em `RUNBOOK_AUDITORIA_REGIMENTOS.md`.
6. **§ U12 em `planejamento/06_GATES_QUALIDADE_FORJA.md`** — a blindagem entra no catálogo canônico de gates.

## Duas regras de calibração que não podem ser perdidas

**Pendência declarada é P1, não P0.** Um fato que se assume não conferido (`groundingPending: true`) é honesto; ainda bloqueia a promoção, mas não é tratado como alucinação. Punir a honestidade com a mesma severidade da invenção ensina o sistema a esconder lacuna.

**Negar identidade nunca pode travar.** O gate L5 chegou a bloquear a frase corrigida — "não se trata da mesma liquidação" —, que é exatamente o resultado desejado. Corrigido com detector de negação por janela curta, e as duas frases reais corrigidas foram fixadas na lista `NAO_PODE_TRAVAR` da regressão. Um auditor que reprova o acerto é desligado na terceira vez.

## Limites deste endurecimento

Os oito gates são escudos lexicais e estruturais. Eles obrigam a colar o trecho e conferem que o trecho está na fonte apontada; **não julgam se o trecho sustenta a proposição**. Isso continua sendo trabalho humano e da auditoria F7. Nenhum destes gates substitui abrir os autos.

## Pendências declaradas do caso

Nenhuma foi silenciosamente descartada; todas constam dos artefatos:

- certidão de trânsito em julgado do acórdão do AI 5039469 — não está no acervo, exige obtenção externa;
- consulta ao eproc na data do ato — ato externo, não autorizado;
- enquadramento TIPI dos calçados nos Decretos 83.263/1979, 89.241/1983 e 97.410/1988 — decide se o cenário TIPI é economicamente relevante ou quase nulo;
- teste amostral de rendimento documental sobre 30 a 50 guias do evento 80 — trabalho pericial;
- os dois gates humanos de F7 (`human_claim_review_signed_receipt` e `external_human_trust_store_verified`), que nenhum modelo pode satisfazer.

## Adendo de 04/08/2026 — o parecer interno de 24/07 ficou fora da correção

Este registro afirma, acima, que nenhuma peça foi enviada ou liberada com os erros descritos. Isso continua verdadeiro **para as peças**. Não é verdadeiro para todo artefato do caso.

Um escritor de DOCX fora das rotas canônicas — `build_internal_report.py`, dentro da própria tentativa de F7 — gerou `PARECER_INTERNO_VALE_TRADING_FORJA_REVISAO.docx` a partir do `final_markdown.md`, gravando direto na pasta do caso, sem passar por `forja_verificador` nem pelos gates de lastro. O arquivo está arquivado em `gestao_escritorio/entregas_fabio_osorio/2026-07-24 Re Fwd Consulta técnico-pericial – Vale Trading S A para validação 19f92548/`.

Conferido no arquivo entregue, em 04/08/2026: o § 16 traz, verbatim, "O AI 5039469-52.2019.4.04.0000 envolve as mesmas partes e a mesma liquidação" — exatamente a proposição que este incidente, dois dias depois, classificou como o P0 mais grave, por serem liquidações distintas (aquele agravo veio da liquidação 5072582-42.2016.4.04.7100, da Pamper).

O ciclo corretivo de 26/07 fechou o laço sobre a minuta e não sobre o parecer que já estava com o Fábio. Pendência aberta, com decisão humana: corrigir e reenviar o parecer interno, ou registrar por escrito que ele foi superado. Não é decisão de agente, porque envolve o que o cliente interno já leu e pode ter usado.

Como o buraco foi encontrado: o detector de escritores de DOCX sob `state/`, criado em 04/08 por recomendação do Efesto, acusou este arquivo na primeira execução. A revisão cruzada Codex, que havia apontado a classe do problema, não tinha visto este caso.
