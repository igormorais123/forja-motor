# Os 34 gates de contrato sem veredito real — 04/08/2026

Dos 73 gates declarados nos contratos de fase, 39 produzem veredito sobre as 63 tentativas
reais do acervo. O censo também emite dois diagnósticos auxiliares (`criterio_vigente` e
`economic_gates`), por isso o relatório mede 41 nomes de gate. Os outros 34 gates de contrato
estavam registrados como um número solto, e número solto vira conforto: dá para ler "39 de 73"
como progresso e nunca perguntar o que há nos 34.

Há três coisas diferentes ali dentro, e só uma delas é defeito.

## 1. Aritmética honesta — a fase nunca rodou (3 gates)

`F10_ENTREGA_EVIDENCIA_APRENDIZADO`: zero tentativas no acervo. `external_identifier_valid`,
`management_synced` e `package_hash_matches` não têm material sobre o qual se pronunciar.
Nada a fazer; o número diz só isso.

## 2. F8-S: zero no censo, primeira contraprova real fora dele (16 gates)

O censo das 63 tentativas ainda não atribui veredito aos dezesseis gates da `F8_QA_VISUAL`.
Existem três tentativas históricas, mas `forja_f8_contract` despacha entre a rota estática,
vigente desde 30/07/2026, e a rota legada por PDF — e **nenhum dos quatro ledgers visuais do
acervo declara `mode: static_ooxml_svg`**. Esses artefatos antigos continuam fora do numerador.

Isso não significa mais que a F8 nunca viu um DOCX real. O relatório
`F8_PRIMEIRA_EXECUCAO_REAL_2026-08-04.md` registra uma contraprova direta contra quatro peças
reais e entregues: a primeira execução reprovou todas, separou falsos positivos de achados
reais e confirmou a calibração do fólio do template e dos papéis estruturais. A regressão
`test_forja_f8_pecas_reais.py` preserva essa evidência sem maquiar o resultado: duas peças de
referência passam, enquanto a V9 e a V8 permanecem como peças triadas com seus achados reais.

Essa contraprova é evidência de calibração, mas não é um ledger de tentativa F8 produzido pela
rota de promoção. Portanto, não conto esses dezesseis nomes como novos vereditos do censo nem
forço a rota estática sobre os ledgers antigos. O que foi fechado é o risco de barrar o padrão
aprovado por dois falsos positivos; o que permanece aberto é exercitar a F8 dentro de uma fase
real, com os insumos de origem, revisão humana e artefatos estáticos registrados no contrato.

Isso incide diretamente sobre a decisão de tornar o gate F8-S bloqueante, prevista para depois
de 05/08: a decisão deixou de ser ligar o gate completamente no escuro, mas o primeiro caso
real dentro da fase ainda deve ser acompanhado de perto em vez de confiado ao verde da
contraprova isolada.

## 3. F7/F9 sem veredito de contrato (15 gates)

A comparação dos nomes dos contratos com o censo deixa dez gates da F7 e cinco da F9 sem
veredito real. A primeira versão deste documento media apenas arquivos locais da tentativa F7 e
concluía que o lastro não existia. Isso não era verdade para todo o acervo: a rota canônica
resolve o `fact_ledger.json` promovido pela F3 no caso.

Na revalidação, o contrato atual da F7 já declara `fact_ledger` como entrada obrigatória e o
censo passou a chamar o mesmo `_compute_lastro_gates` usado pelo runner. Resultado: quatro
`fact_grounding_verbatim` foram produzidos sobre tentativas reais; os quatro reprovaram por
pendências de fonte explicitamente registradas, e o caso Vale também expôs a ausência de fonte
econômica prevalente. O resultado não é mais “sem objeto” nem “pass” autodeclarado.

Ainda há duas tentativas históricas de F7 sem ledger promovido localizável (Nylton e Natura);
o censo não inventa veredito para elas. O `package_manifest.json` continua inexistente no
acervo, portanto os cinco gates da F9 seguem sem material.

## O que este documento pede

Nada urgente. Ele existe para que “39 de 73” não seja lido como se os gates restantes fossem
todos a mesma coisa — e para que a conversa sobre ligar o F8-S distinga a contraprova real já
feita da ausência de ledger estático dentro da rota de promoção.

A decisão humana que permanece é a ativação bloqueante do F8-S depois de 05/08. O primeiro caso
real nesse modo deve ser acompanhado de perto. No plano F7, as pendências de lastro e a ausência
de manifesto F9 são bloqueios de material ou de conferência; não devem ser “resolvidas” por
autodeclaração nem por backfill silencioso de tentativas históricas.
