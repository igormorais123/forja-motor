# Onda −1 — cocriação testada antes de construída

**Data:** 25/07/2026
**Emenda:** E15 (Helena, H1–H6)
**Regra da onda:** nenhuma linha de código. Teto 08/08/2026.
**Razão de existir:** a consulta dialética é a aposta central do plano. Antes de construir `F2-B`, convém saber se uma consulta escrita a um advogado sênior ocupado produz resposta útil — ou latência pura.

---

## 1. Demonstração de recusa a partir de um bloqueio real

Helena pediu uma demonstração concreta, extraída do histórico, em vez de uma explicação abstrata sobre o valor do lastro. Encontrei uma melhor do que esperava.

**Caso:** `case-email-auto-19f3f25cb64df962` — o caso pessoal de plano de saúde do próprio titular.
**Data:** 09/07/2026.

### O que aconteceu, minuto a minuto

| Horário | Fato | Evidência |
|---|---|---|
| — | A pesquisa F3 localiza o **Tema Repetitivo 1365/STJ**, julgado em 11/03/2026: dano moral presumido por hipervulnerabilidade de consumidor com deficiência. O dossiê o classifica com força "altíssima" | `F3_DOSSIE_LEITURAS.md`, linhas 826-895 |
| — | O mesmo dossiê registra que a busca **não localizou o REsp vinculado** e recomenda acesso ao SCON autenticado | `F3_DOSSIE_LEITURAS.md`, linha 902 |
| 20:18:26 | As Súmulas 608 e 609 do STJ são capturadas verbatim da SCON/STJ, em Chrome real | `cache/fontes_oficiais/STJ_SUMULA_608.txt` e `609.txt` |
| 20:25:00 | O F7 é recomputado. As duas súmulas saem da lista de pendências. **O Tema 1365 permanece como `citacoesNaoConferidas`** no estudo estratégico e na minuta ao TJDFT | `producao/F7_VERIFICADOR_FORJA.json` |
| — | **O Tema 1365 não aparece em nenhum documento produzido.** Busca textual por "1365" nos markdowns de `producao/`: zero ocorrências | varredura de 25/07/2026 |

### Por que este episódio prova o ponto

O Tema 1365 era **o melhor argumento disponível**. Um repetitivo de 2026, recentíssimo, dizendo exatamente o que favorecia o cliente: dano moral presumido para consumidor hipervulnerável com deficiência. Qualquer sistema otimizado para parecer convincente o teria usado.

A FORJA não usou. Não porque duvidasse do tema, mas porque **não conseguiu o verbatim**. Registrou a pendência, manteve o registro visível na auditoria, e escreveu a peça sem o argumento mais atraente que havia encontrado.

E a mesma máquina que recusou o Tema 1365 **capturou** as Súmulas 608 e 609 sete minutos antes — o bloqueio não é preguiça nem excesso de zelo: é o gate produzindo trabalho onde o trabalho era possível, e recusando afirmação onde não era.

**Até hoje** o Tema 1365 não tem verbatim no cache. A pendência segue viva e honesta.

> Esta é a demonstração para usar com o titular. Ela responde, com um caso dele próprio, à pergunta que todo advogado faz sobre IA jurídica: *"e quando ela não sabe, o que ela faz?"*

## 2. Minuta de consulta sobre caso real

**Caso escolhido:** Vale Trading S.A. — Liquidação por Arbitramento nº 5020376-80.2018.4.04.7100/RS (TRF4).
**Por que este:** recebido em 23/07/2026, com entrega interna em 24/07; 4.604 páginas indexadas; nove volumes; três anexos técnico-contábeis. Sem prazo crítico incompatível. E, sobretudo: o `ADENDO_INTERNO_VALE_TRADING_MATRIZES_2026-07-24.md` **já produziu a matriz de premissas com a coluna "confirmação pendente"** — que é, na prática, a lista de perguntas que faltavam.

### Filtro do acervo aplicado

O gabarito exige zero pergunta respondível pelo material já lido. Descartei, entre outras: qual foi o pedido originário, o que decidiu o REsp 1.181.982/RS, o que a Contadoria afirmou nos eventos 166 e 243, o que diz a Informação Fiscal nº 1.690, e onde está o erro de escala de janeiro/1989. **Todas já respondidas no adendo.**

O que sobrou são perguntas de três naturezas que nenhum acervo responde: **decisão estratégica**, **autorização** e **informação que só existe fora dos autos**.

---

### Minuta — para revisão e envio pelo Igor

> **Assunto:** Vale Trading — seis pontos que decidem o formato da consulta técnico-pericial
>
> Prezado Dr. Fábio,
>
> Concluí a leitura integral dos nove volumes e dos três anexos contábeis, e o adendo interno de 24/07 consolida as matrizes. Antes de fechar a consulta técnico-pericial, há seis pontos que **não estão nos autos** e que mudam materialmente o produto. Indico, em cada um, o que acontece se não houver resposta.
>
> **1. Cenários condicionais ou tese única.** O material sustenta afastar a liquidação zero, mas não sustenta certificar 12%, 24% ou qualquer quantum. Posso (a) apresentar cenários condicionais com as condições de escolha explícitas, ou (b) sustentar a CIEX de 12% como cenário principal e tratar os 24% como alternativa subsidiária. A opção (a) é tecnicamente mais defensável e menos vulnerável em contraditório; a (b) é mais direta e pode ser o que o cliente espera.
> *Sem resposta:* sigo com (a), que é o que o estado da prova autoriza.
>
> **2. Tabela CIEX autêntica por NBM.** A disputa 12% × 24% não fecha sem a tabela da Resolução CIEX nº 2/1979 por classificação NBM e período, em fonte autêntica. Não a localizei em base pública. O escritório tem acesso, por acervo próprio ou por diligência ao arquivo do extinto CIEX ou à PGFN?
> *Sem resposta:* a consulta registra a alíquota como questão aberta e nenhum dos dois percentuais é apresentado como resultado necessário.
>
> **3. Planilhas nativas.** O Laudo nº 149/2025 chega a R$ 1.072.604.895, mas recebi apenas PDF assinado. Sem as planilhas nativas com fórmulas e chaves de guia, o total não é reproduzível — e o mês de janeiro/1989 aparenta misturar cruzado e cruzado novo sem reconciliação da redenominação de 1.000 para 1. Podemos solicitá-las ao cliente ou ao perito autor do laudo?
> *Sem resposta:* a consulta bloqueia a certificação do total e o registra como não auditável, o que enfraquece a peça exatamente no número que mais interessa.
>
> **4. Identidade Calçados Marcela × Calçados Pamper.** O AI nº 5039469-52.2019.4.04.0000 é o precedente comparativo mais forte que encontrei sobre alíquota, prova SECEX e data de efetivação — mas é de outro título, outro CNPJ e período próprio. Existe documentação societária, fora dos autos, que ligue as duas empresas ou explique a incorporação?
> *Sem resposta:* uso o precedente apenas como ratio persuasiva, sem qualquer sugestão de extensão da coisa julgada — que seria o uso mais forte, e o mais arriscado.
>
> **5. Momento em relação aos embargos do evento 239.** A tese da CIEX está submetida a julgamento pendente. Entrego a consulta agora, com o estado atual, ou aguardo o julgamento para calibrar?
> *Sem resposta:* entrego agora, com o estado registrado e a ressalva de recalibração — mas o documento nasce com validade condicionada.
>
> **6. Expectativa já formada no cliente.** Preciso saber se o número de R$ 1,072 bilhão já circulou junto à Vale Trading. Se já foi apresentado como expectativa, a consulta precisa tratar da distância entre esse total e o que a prova hoje sustenta — o que é um problema de comunicação com o cliente, não de técnica.
> *Sem resposta:* redijo em termos neutros, sem endereçar a expectativa; se ela existir, a diferença aparecerá depois, em pior momento.
>
> Qualquer resposta parcial já destrava o restante. Os pontos 2 e 3 são os que mais mudam o produto: são os únicos que podem transformar cenários condicionais em conta reproduzível.

---

**Estado:** minuta pronta, **não enviada**. O envio é ato externo e depende de decisão do Igor. A v1 do plano é explícita: a FORJA prepara a consulta; o envio depende de pessoa autorizada.

## 3. Três métricas de negócio

Helena observou que o projeto media qualidade técnica e não media valor. As três abaixo são as que sobrevivem ao teste de "mudaria uma decisão do escritório".

| # | Métrica | Definição operacional | Instrumentação hoje |
|---|---|---|---|
| **N1** | **Taxa de resposta útil à consulta** | consultas respondidas com decisão material sobre ao menos um ponto ÷ consultas enviadas, por janela de 7 dias | **não instrumentada.** Depende da Onda −1 produzir o primeiro dado. É a métrica que decide o destino de F2-B: se ficar baixa, o escopo encolhe para os Blocos 1 e 5, conforme o cenário pessimista de Helena |
| **N2** | **Distância da versão protocolada** | proporção de parágrafos alterados entre a nossa entrega e a versão efetivamente protocolada pelo escritório | **parcialmente instrumentada**: `forja_diff_docx.py` existe e roda no pós-entrega (upgrade U7). Falta a série histórica com denominador declarado — quantas entregas tiveram versão protocolada recuperada |
| **N3** | **Tempo entre entrega e uso** | dias entre a entrega ao escritório e o primeiro sinal de uso — protocolo, resposta substantiva ou pedido de ajuste | **não instrumentada.** O painel de demandas tem os eventos, mas "entregue" e "usado" não são hoje campos distintos. Um caso em `draft_awaiting_review` há 353 horas é exatamente o que N3 tornaria visível |

**Por que não mais que três.** Métrica sem dono e sem decisão associada vira relatório. Cada uma acima responde a uma pergunta que o Igor faz de fato: a cocriação funciona (N1), a nossa peça é a peça que sai (N2), o escritório usa o que entregamos (N3).

**Advertência de método, herdada do ciclo AR:** nenhuma dessas métricas serve para promover variante. São indicadores de negócio, medidos sobre denominadores declarados, não julgamento cego pareado.

## 4. Registro da decisão sobre J-B

O parecer do Cícero de 25/07/2026 já resolveu a separabilidade, e a Onda −1 apenas registra a decisão:

- **J-B(julgador) — proibido sair.** Não há veículo processual: as hipóteses dos arts. 144-145 do CPC são lista fechada e divergência estatística não está entre elas; o art. 41 da LOMAN protege o magistrado; e perfil comportamental é dado pessoal sob o art. 12, §2º, da LGPD. Uso interno apenas, com **vedação de saída verificável por gate lexical**.
- **J-B(acordo) — autorizado**, com fundamento no art. 20 da LINDB, na Lei 13.140/2015 arts. 32-40, na Lei 14.133/2021 e no art. 17-B da Lei 8.429/1992. **Veto**: é proibida qualquer formulação que enderece consequência funcional pessoal ao gestor público.

Nada a decidir; item encerrado por registro.

---

## Estado da onda

| Item | Estado |
|---|---|
| Demonstração de recusa | **concluída**, com evidência datada |
| Minuta de consulta | **pronta**, aguardando decisão de envio |
| Três métricas | **definidas**, com instrumentação declarada honestamente |
| Registro J-B | **encerrado** |

**Bloqueio para o resto da onda:** o dado de N1 só nasce quando a consulta for enviada e respondida. Enquanto isso, a Onda 1A permanece condicionada — como Helena determinou —, e a **Onda 1B pode prosseguir**, por não depender deste resultado.
