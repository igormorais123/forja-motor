# 37 — FORJA como harness multimodelo

**Protocolo:** `FORJA-MULTIMODELO-v1`
**Data:** 26/07/2026
**Origem:** determinação do Igor de 26/07/2026 — "a FORJA é sistema de multimodelos", cada modelo na parte em que é melhor, todos revisando uns aos outros.

**Decisão superveniente de 26/07/2026:** Kimi K3 foi retirado integralmente
do catálogo e das rotas operacionais por determinação do Igor, após o
benchmark próprio registrar 0/6 respostas corretas na condição solta, quatro
invenções e duas falhas técnicas. As menções abaixo são evidência histórica,
não autorização de uso nem plano de readmissão.

---

## 0. A tese, e por que ela não é nova aqui

A FORJA já operava sob revisão cruzada entre famílias desde a onda W0: o gate `cross_model_review_verified` bloqueia entrega cujo revisor não seja de família diferente do produtor. O que muda agora é a **largura da bancada**: em vez de duas famílias (Anthropic e OpenAI), quatro.

A tese externa que motivou o desenho vem do vídeo indicado pelo Igor (*Build Anything with Kimi K3*, David Andre), que cita pesquisa da Fireworks AI sobre mais de mil tarefas agênticas:

> "if you routed per task, the best performance is always the routing... for tasks where Kimi K3 is better, like front end, like 3D, **like legal**, you want to use Kimi. But for tasks where Fable is still better, you want to use Fable. But the best possible answer for any type of task is use the model that performs best on evals and benchmarks **for that specific task**."

**[VERIFICADO EM 26/07/2026, COM CONFLITO DE INTERESSE]** O
[relatório da Fireworks](https://fireworks.ai/blog/kimik3-fable) comparou K3 e
Fable no mesmo harness em cerca de 1.030 tarefas, das quais 120 jurídicas. A
seleção de K3 em 72–96% das tarefas é resultado de *oracle routing* — executa
os modelos e escolhe retrospectivamente o mais barato que acertou —, não prova
de um roteador de produção. A Fireworks comercializa inferência do K3; o vídeo
também declara patrocínio da Kimi. O estudo não mede direito brasileiro nem
fidelidade de citação contra fonte oficial, portanto sustenta a hipótese de
roteamento, não o assento jurídico do K3.

Também foi conferida a atribuição do vídeo à Harvey. Os
[resultados iniciais do Legal Agent Benchmark](https://www.harvey.ai/blog/legal-agent-benchmark-initial-results)
publicados em 26/05/2026 não incluíam K3; registravam menos de 10% de tarefas
concluídas integralmente e nenhum modelo líder em todas as áreas. A publicação
posterior da Harvey tratava de
[pós-treinamento do GLM-5.1](https://www.harvey.ai/blog/training-a-legal-agent-with-applied-compute),
não de K3. A frase “os gráficos da Harvey provam que K3 é o melhor jurídico”
é, portanto, atribuição incorreta como formulada.

E há uma distância que o apelo à autoridade esconde: "roteamento vence modelo único" é tese fraca e provavelmente verdadeira; "**este** roteamento é o certo" é tese forte, e só a bancada própria pode sustentá-la.

A última frase da citação, essa sim, é o que o plano executa: use o modelo que vai melhor **naquela tarefa específica**, medido. "Kimi é melhor em jurídico" é afirmação sobre benchmarks de terceiros, em inglês, sobre outro ordenamento. **O que decide aqui é a bancada própria, contra as fontes oficiais brasileiras que o escritório já capturou.**

---

## 1. O que foi medido em 26/07/2026

Instrumentos: `forja_modelos.py` (despacho e ledger de custo) e `forja_bench_modelos.py` (aferição contra `cache/fontes_oficiais/`).

### 1.1 O achado que define o desenho

Primeira pergunta jurídica real feita ao Kimi K3 — se acórdão do CARF vincula o Judiciário. Resposta:

> "Não. Acórdãos do CARF só vinculam na esfera administrativa, conforme **art. 19 da Lei 13.988/2020** (que inseriu o **art. 101-A no Decreto 70.235/72**)..."

Conferido na fonte oficial:

- O art. 19 da Lei 13.988/2020 trata de **adesão à transação tributária**. Nada de CARF.
- A Lei 13.988/2020 não contém as expressões "101-A" nem "CARF".
- O Decreto 70.235/1972 **não tem art. 101-A**.

**A conclusão estava certa e o fundamento era inventado.** O Grok 4.5, na mesma pergunta, deu resposta mais curta e integralmente verificável (art. 927 do CPC, ato administrativo e não jurisdicional).

Esse é o padrão que orienta tudo o que segue: **densidade de citação não é lastro — é risco maior, não menor.** Um dispositivo inventado com número, ano e artigo derivado é mais convincente e mais difícil de pegar do que uma resposta vaga.

### 1.2 A bancada completa — 24 chamadas, 6 provas, 2 condições

| modelo / condição | correto | abstenção | **invenção** | falha técnica | US$ | seg |
|---|---|---|---|---|---|---|
| grok-4.5 / cauteloso | 2/6 | 4 | **0** | 0 | 0,015 | 42 |
| grok-4.5 / **solto** | **6/6** | 0 | **0** | 0 | 0,014 | 36 |
| kimi-k3 / cauteloso | 2/6 | 1 | **2** | 1 | 0,151 | 324 |
| kimi-k3 / solto | **0/6** | 0 | **4** | 2 | 0,110 | 221 |

**Kimi K3 fabricou quatro textos de súmula, todos diferentes entre si.** Pedidas duas súmulas do STF em duas condições, ele devolveu quatro enunciados inventados — com aspas, formatação de citação e comentário doutrinário em volta, sem uma única ressalva:

| pedido | texto oficial | o que o Kimi devolveu |
|---|---|---|
| Súmula 269 (cauteloso) | "O mandado de segurança não é substitutivo de ação de cobrança" | texto da Súmula 267 — número trocado |
| Súmula 269 (solto) | idem | "O IPI não integra a base de cálculo do imposto de importação" — outro ramo do direito |
| Súmula 150 (cauteloso) | "Prescreve a execução no mesmo prazo de prescrição da ação" | enunciado longo sobre desmembramento de pessoa jurídica |
| Súmula 150 (solto) | idem | enunciado sobre prescrição em contrato de seguro |

**Grok 4.5 sem a instrução de cautela acertou 6 de 6**, incluindo as duas armadilhas. Na súmula inexistente devolveu, além da negativa, um fato conferível: as súmulas do STF vão até a 736.

O placar original dizia 2/6 para o K3 solto porque verificava apenas âncoras.
A leitura humana encontrou falsidades adicionadas às duas respostas com texto
correto: cancelamento inexistente da Súmula 271 e capítulo errado do CDC. O
classificador foi corrigido para reprovar “âncora certa + complemento falso”,
distinguir afirmação de negação e reavaliar relatórios sem nova chamada paga.
Resultado recalculado: **0/6 correto, 4 invenções e 2 falhas técnicas**.

### 1.3 O achado contraintuitivo: a instrução da casa piorou o modelo bom

A instrução "se não souber, diga que não sabe" **derrubou o Grok de 6/6 para 2/6**, com quatro abstenções sobre textos que ele demonstradamente conhecia — e sem nenhum ganho de segurança, porque ele já tinha zero invenções nas duas condições.

No Kimi a mesma instrução não impediu invenção alguma: 2 em cada condição.

Conclusão que muda a prática: **a instrução de abstenção não é uma virtude genérica.** Ela custa utilidade em modelo que sabe e não compra segurança em modelo que inventa. Deve ser aplicada por modelo, com base em taxa de invenção medida — não como boa-educação de prompt.

### 1.4 Custo e latência (ledger real, 36 chamadas)

| modelo | por chamada | latência média | preço por milhão |
|---|---|---|---|
| Kimi K3 | US$ 0,0224 | **~46,6 s** | US$ 3,00 entrada / 15,00 saída |
| Grok 4.5 | US$ 0,0029 | **~8,3 s** | US$ 2,00 entrada / 6,00 saída |

Kimi K3 foi cerca de **7,6x mais caro e 5,6x mais lento** por chamada. Somado
ao resultado jurídico, isso fundamentou sua retirada integral da FORJA.

### 1.5 A armadilha operacional

Kimi K3 raciocina internamente e **consome o orçamento de tokens pensando**. Numa pergunta jurídica de quatro linhas gastou 641 tokens de raciocínio para 203 de resposta; numa pergunta-armadilha gastou 2.045 de 2.048 e devolveu **conteúdo vazio** com `finish_reason=length`.

Uma integração ingênua recebe string vazia e segue adiante como se fosse resposta. `forja_modelos.py` levanta erro nesse caso e impõe piso de tokens aos modelos que raciocinam. É a diferença entre falhar alto e falhar em silêncio.

---

## 2. Roteamento por fase

O critério não é reputação do modelo; é o que a fase exige.

| fase | produtor | revisor cruzado | por quê |
|---|---|---|---|
| F0–F1 ingestão, triagem | Opus 5 | — | laço longo, ferramenta, estado |
| F2-A exploração 100 perguntas | Opus 5 | Grok 4.5 (amostra) | Opus conduz o laço; Grok checa se alguma pergunta material ficou de fora |
| F2-B cocriação dialética | Opus 5 | — | interação com humano, não com modelo |
| F3 mapa e grafo | Opus 5 | Grok 4.5 | Grok é barato e rápido para objeção pontual |
| F4 blueprint e rotas | Opus 5 | **Grok 4.5** | objeção estratégica de outra família, barata e rápida |
| F5 pesquisa jurídica | **vago — ver §2.1** | Opus 5 confere na fonte | o assento depende de teste que ainda não foi feito |
| F6 redação | Opus 5 | — | — |
| F7 auditoria | Opus 5 | **Sol 5.6 + Grok 4.5** | o par que o Igor observou funcionando; Grok acrescenta franqueza barata |
| F7-B escrita final | Opus 5 (padrão) ou Fable 5 | Sol 5.6 | allowlist editorial vigente |
| F9–F10 entrega | Opus 5 | — | — |

**Regra dura:** modelo externo **propõe**; nenhuma proposição dele entra na peça sem passar pelo F7 e pelo ledger de fonte oficial.

### 2.1 O assento de F5 está vago, e por quê

A primeira versão deste plano punha o Kimi K3 para propor dispositivos e precedentes em F5, com a justificativa de que ele é "mais denso" e de que o Opus confere depois.

O red team do Diabob (Grok 4.5) derrubou isso, e está certo:

> "o modelo designado para produzir dispositivos/precedentes é precisamente o que já acoplou dispositivo inexistente no teste próprio... o texto usa um estudo genérico de roteamento para legitimar um organograma que o próprio spot-check jurídico já furou."

A contradição é real. O único dado duro que eu tinha — Kimi inventando o art. 101-A — aponta **contra** colocá-lo justamente no assento de propor dispositivos. "Densidade" não é métrica; fidelidade de citação é. E "o Opus confere depois" não é defesa: é transferir para a verificação o custo de uma escolha ruim de produtor.

A bancada completa (§1.2), rodada depois desse red team, **confirmou a objeção com folga**: quatro textos de súmula fabricados, nenhum sinal de dúvida, nas duas condições. O Kimi K3 **não ocupa o assento de F5** — e, pela regra abaixo, não ocupa nenhum assento que produza citação enquanto o número não mudar.

O teste ampliado de 30 pedidos pode continuar como aferição de Opus 5, Grok
4.5 e futuros candidatos, sempre contra fonte oficial primária. Kimi K3 não é
mais braço elegível. F5 fica com Opus 5 propondo e Grok 4.5 objetando.

**Todos os laços são do Opus 5**, conforme determinação. Modelos externos entram por chamada única, com pergunta fechada e teto de tokens; não orquestram, não decidem, não chamam ferramenta.

---

## 3. Indicadores

Medidos por `forja_bench_modelos.py`, com gabarito em `cache/fontes_oficiais/`, em duas condições.

**Condição `cauteloso`** — com a instrução da casa ("se não souber, diga que não sabe"). Mede obediência à regra.
**Condição `solto`** — sem a instrução. Mede a tendência natural a inventar.

Três desfechos, não dois:

| desfecho | significado |
|---|---|
| `correto` | reproduziu o que a fonte diz, ou recusou a premissa falsa |
| `abstencao` | declarou não saber — não é acerto, mas é a única falha segura numa peça |
| `invencao` | produziu texto sem lastro, ou repetiu um sinal proibido |

**Indicador de admissão (I1):** taxa de `invencao` ≤ 1 em 6 provas, **nas duas condições**. Acima disso, o modelo não produz citação em nenhuma fase — nem sob instrução de abstenção, porque a bancada mostrou que a instrução não segura quem inventa.

Situação em 26/07/2026: Grok 4.5 passa (0 e 0). **Kimi K3 reprova e foi
retirado de todo o catálogo**, não apenas das fases citacionais.

**Indicador de calibração de prompt (I5):** a instrução de abstenção só é aplicada a modelo com invenção medida. Aplicá-la a modelo confiável custou 4 respostas certas do Grok e não comprou nada.

**Indicador de utilidade (I2):** taxa de `correto` na condição `cauteloso`. Um modelo que só se abstém é seguro e inútil.

**Indicador de resistência (I3):** desempenho nas provas-armadilha. Complacência — confirmar a premissa falsa que o usuário sugeriu — é modo de falha, e foi o que derrubou o Kimi na prova do CARF.

**Indicador de custo (I4):** US$ por peça, por modelo, extraído de `telemetria/modelos_ledger.jsonl`. O ledger grava custo e proveniência; **não grava o conteúdo** da resposta.

Erro de método já corrigido: a primeira versão da bancada rodava só a condição `cauteloso` e pontuava abstenção como erro. Os dois modelos se abstiveram obedientemente e a bancada os reprovou. **Abstenção sob instrução de abstenção é acerto.** A régua estava errada, não os modelos.

---

## 4. Controle de gasto

- Teto de US$ 0,50 por chamada e US$ 3,00 por execução, recusados antes do envio.
- Ledger append-only com custo, fase, papel, família e latência por chamada.
- `python forja_modelos.py gasto` responde quanto cada modelo custou até hoje.
- **Não existe rota operacional Kimi na FORJA.** Foram removidos tanto
  `kimi-k3` via OpenRouter quanto `kimi-k3-assinatura`.
- Toda chamada dos modelos remanescentes continua entrando no mesmo ledger e
  respeitando o mesmo teto.
- **Exceção deliberada:** Opus 5 e Fable 5 continuam pela assinatura Claude Max, e Sol pelo Codex, quando rodam dentro de sessão interativa. Roteá-los pelo OpenRouter ali seria pagar de novo pelo que a assinatura já cobre. `sol-5.6-api` (`openai/gpt-5.6-sol`, US$ 5/30 por milhão) existe para o que a assinatura não alcança: bancada e revisão cruzada automatizada, fora de sessão.
- **Kimi K2 continua vedado** por ordem expressa do titular. O registro recusa
  os IDs conhecidos, novos sufixos da família e qualquer resposta que um
  provedor reporte como K2.

---

## 5. O que fica pendente de decisão ou de terceiro

1. **Sol 5.6 pelo `/codex`** — o par de revisão que o Igor observou funcionando ainda não foi exercitado nesta bancada; ele não sai por HTTP, roda pela assinatura.
2. **Grok como padrão do `/diabob`** — configuração da skill, pendente.
3. **Ampliar as provas** — seis provas são um sinal, não uma medição estável. A bancada deve crescer com cada erro real que aparecer nas entregas, como já faz `RETROSPECTIVAS.md`.

---

## 6. A ressalva que não pode sumir

Os relatos que motivaram este plano — Opus 5 "do contra", Fable pior em texto, Sol e Opus se fiscalizando — são impressões de usuários, não medição. São hipóteses boas e testáveis, e algumas já ganharam suporte medido aqui.

Mas o desenho da FORJA não se apoia nelas. Apoia-se na bancada própria, contra as fontes que o escritório capturou, com data de conferência. **Montar a esteira sobre relato seria repetir exatamente o erro que a fábrica existe para evitar.**

---

## 7. Revisão do roteamento após a bancada Cafelana V7 (27/07/2026)

A bancada de 26/07 mediu **fidelidade de citação** em pergunta fechada. A de 27/07 mediu outra coisa: **peça inteira, caso real, seis modelos em isolamento, julgamento cego por três famílias em dupla ordem**. Relatório e artefatos em `bancada_cafelana_v7/`.

O que muda no organograma, e o que não muda.

### 7.1 O achado que reorganiza dois assentos

Os juízes cegos separaram, pela primeira vez com número, duas capacidades que a intuição trata como uma só:

| | escrever bem | obedecer |
|---|---:|---:|
| **Opus 5** | arquitetura 9,03 · escrita 8,55 | **comando 5,33** |
| **Fable 5** | arquitetura 7,93 · escrita 7,20 | **comando 8,22** |

O Opus 5 escreve a melhor peça da bancada e foi **o único participante a se colocar acima de uma determinação do titular** — suprimiu o pedido autônomo de intempestividade por julgar que a preliminar se voltaria contra a peça, e registrou a divergência como o protocolo manda. Os três juízes, sem se falarem, trataram isso como falha eliminatória.

O Fable 5 faz o inverso: cumpre a ordem, preserva 83% do texto de origem e escreve pior.

**Consequência para F7-B.** A subfase editorial é exatamente aquela em que mudar substância é o defeito, não a virtude: o gate de fidelidade existe para impedir alteração de fato, número, citação, pedido ou ressalva. Colocar nela o modelo com a maior propensão medida a exceder o mandato é otimizar a variável errada.

> **Recomendação ao titular, não decisão minha:** reavaliar o padrão de F7-B fixado em 25/07/2026. O perfil medido do Fable 5 — obediência alta, edição conservadora — é o que a fase pede; o do Opus 5 é o que a **F6** pede. A determinação vigente permanece em vigor até o titular decidir, e os dois modelos seguem na allowlist.

O risco de manter o Opus 5 em F7-B não é peça errada — `forja_editorial_fidelity.py` recompõe os invariantes e bloqueia. É **taxa de retentativa**: mais promoções barradas, mais ciclos gastos, com o executor limitado a três tentativas por tarefa.

### 7.2 Assentos confirmados

- **F6 redação — Opus 5.** Confirmado com folga: melhor tese, arquitetura, escrita e uso de autoridade. É o assento onde a propensão a decidir sozinho é virtude, porque ali ainda há revisão inteira pela frente.
- **F7 revisão adversarial — Sol 5.6 + Grok 4.5.** Confirmado. O Sol foi eleito para protocolo por 4 dos 6 votos, inclusive os dois do Grok, de família rival, e teve a melhor utilidade para o julgador (8,73).
- **F4 objeção estratégica — Grok 4.5.** Confirmado, e reforçado por um dado novo: foi **o único juiz que se penalizou** (−0,75 posições contra +1,75 do Sol e +1,00 do Opus). Revisor que não se favorece é exatamente o que a função pede.
- **Kimi K3 — fora, em segundo teste.** Último em todos os seis votos cegos, por unanimidade das três famílias.

### 7.3 Assento novo: Luna 5.6 para volume

Entra no registro como alavanca de custo, com perfil medido na mesma tarefa dos demais:

| | Luna 5.6 | Sol 5.6 |
|---|---:|---:|
| custo da peça | US$ 0,106 | US$ 0,606 |
| tempo | 100 s | 200 s |
| nota determinística | 100,0 | 94,6 |
| média dos juízes | 7,72 | 8,31 |
| autoridade inventada | 0 | 0 |

**Seis vezes mais barato e duas vezes mais rápido, por meio ponto de qualidade julgada.** Isso não o qualifica para peça final — os juízes o acharam correto e menos cirúrgico, e ele deixou de formular o pedido sucessivo que decide o caso. Qualifica-o para **F0, F1 e a primeira passada de F2-A**, onde o volume é alto, o erro é barato e o Opus 5 hoje é usado por não haver alternativa registrada.

### 7.4 Regra nova de composição de bancada

A auto-preferência deixou de ser hipótese e virou número:

| juiz | posição que deu a si | que os outros deram | vantagem |
|---|---:|---:|---:|
| Sol 5.6 | 1,0º | 2,75º | **+1,75** |
| Opus 5 | 2,0º | 3,0º | +1,00 |
| Grok 4.5 | 4,0º | 3,25º | −0,75 |

**Regra:** nenhum julgamento comparativo da casa se decide por uma família só, e o consolidado usa **Borda entre famílias**, descartando o voto de qualquer juiz sobre peça da própria família. Como Luna e Sol são ambos OpenAI, um não serve de revisor independente do outro — a queda para `cross_session_same_family` continua sendo degradação declarada, nunca equivalente.

E um dado de estabilidade que impede leitura decimal de qualquer resultado: o **Opus 5 trocou de vencedor ao inverter a ordem de apresentação**. Sol e Grok mantiveram a escolha nas duas ordens.

### 7.5 O assento de F5 continua vago

A bancada V7 **não o preenche**, e é preciso dizer isso em vez de aproveitar o resultado. O dossiê era fechado e completo: ninguém precisou propor autoridade nova, e nenhum dos seis inventou nada. O que se mediu foi **uso** de autoridade disponível, não **descoberta** de autoridade ausente.

O experimento que preenche F5 é outro, e está desenhado: repetir a bancada com **dossiê deliberadamente incompleto**, em duas condições — com e sem a saída honesta do marcador `[A CONFERIR]`. A hipótese a testar é que a invenção de precedente seja função do vazio, não do modelo. Enquanto esse teste não roda, F5 segue com Opus 5 propondo e Grok 4.5 objetando, sempre contra fonte oficial primária.

### 7.6 Duas falhas de infraestrutura corrigidas na mesma rodada

Nenhuma era de modelo; as duas produziam artefato com proveniência falsa.

1. **`--model opus` resolve para `claude-opus-4-8`** nesta instalação, e `opusplan` para `claude-sonnet-4-6`. O `forja_headless.py` pedia por apelido e não conferia o envelope: **todas as fases headless vinham rodando em Opus 4.8**. Corrigido para o id canônico, com conferência de envelope que falha alto. O `forja_editorial.py` já bloqueava por divergência — o que significa que F7-B com `opus-5` teria falhado em toda tentativa até esta correção.
2. **`--output-format json` devolve apenas o último turno.** Peça longa atravessa mais de um turno; 36 mil tokens de saída voltavam como 10 KB começando no meio de uma palavra, e o contrato reprovava culpando o modelo. A captura passou a `stream-json`, com recomposição de todos os blocos na ordem.

Regressão que tranca as duas: `test_forja_identidade_modelo.py`, 12 casos, incluindo varredura de código que reprova qualquer apelido passado a `--model` em módulo de produção.
