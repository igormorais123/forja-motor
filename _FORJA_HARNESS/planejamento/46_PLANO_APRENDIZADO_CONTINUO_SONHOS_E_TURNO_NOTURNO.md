# 46 — Aprendizado contínuo, sonho noturno e turno automático da FORJA

> Plano de alterações. Escrito em 10/08/2026 a partir de leitura direta do sistema
> Hermes na VPS (via Tailscale) e do estado real da FORJA no disco. Nada aqui foi
> executado ainda.
>
> **Escopo:** fechar o vão entre "a regra está escrita" e "a regra pegou"; criar um
> ciclo noturno que aprende dos casos do dia; e dar à FORJA uma janela diária de
> trabalho automático seguro. Inclui os recursos do Hermes que valem ser trazidos e,
> explicitamente, os que não valem.

## Índice

- [1. O problema, medido](#1-o-problema-medido)
- [2. O que o Hermes tem, medido](#2-o-que-o-hermes-tem-medido)
- [3. Bloco A — reaprendizado vira defeito](#3-bloco-a--reaprendizado-vira-defeito)
- [4. Bloco B — verificação de efeito com prazo](#4-bloco-b--verificação-de-efeito-com-prazo)
- [5. Bloco C — a rejeição também é decisão](#5-bloco-c--a-rejeição-também-é-decisão)
- [6. Bloco D — o sonho noturno da FORJA](#6-bloco-d--o-sonho-noturno-da-forja)
- [7. Bloco E — turno noturno de trabalho automático](#7-bloco-e--turno-noturno-de-trabalho-automático)
- [8. Bloco F — outros recursos do Hermes que valem](#8-bloco-f--outros-recursos-do-hermes-que-valem)
- [9. O que não fazer, e por quê](#9-o-que-não-fazer-e-por-quê)
- [10. Ordem de execução e custo](#10-ordem-de-execução-e-custo)
- [11. Como se mede que este plano funcionou](#11-como-se-mede-que-este-plano-funcionou)
- [12. O que exige decisão do titular](#12-o-que-exige-decisão-do-titular)

---

## 1. O problema, medido

O ciclo de aprendizado da FORJA existe e funciona até certo ponto: `forja_aprendizado.py`
tem `padroes`, `adotar`, `aplicar`, `amostra`, `revalidar` e `conferir`; o registro tem
**20 regras, todas com `aplicadaEm`**; o elo 5-B do `forja_delivery.py` barra entrega se
uma regra sair do destino.

O que ele **não** tem:

**a) Não sabe quando está reaprendendo.** `conferir` prova que a frase está no arquivo de
destino. `revalidar` prova que a evidência que motivou a regra ainda existe. **Nenhum dos
dois pergunta se a regra funcionou.** Entre "escrita" e "pegou" não há instrumento.

Medida: das 277 lições do `RETROSPECTIVAS.md`, **27 admitem por escrito que aquilo já
tinha acontecido antes** — cada uma em prosa, isolada, sem que nada no sistema some duas.
As mais recentes são explícitas: uma diz "quarta ocorrência em dois dias", outra diz "de
novo", outra "outra vez". A detecção foi humana, caso a caso.

Três âncoras reais, todas com regra escrita em vigor no momento da violação:

| Regra | Em vigor desde | Reincidências depois |
|---|---|---|
| Fronteira motor/acervo (dado do escritório não entra no motor) | inviolável no `CLAUDE.md` + gate instalado | 4 em dois dias |
| Identidade dos atos recursais | 11/07/2026, declarada inviolável | 2 clientes, 2 tribunais |
| "Não localizado" não é diagnóstico | 06/08/2026 | a mesma cobrança em 5 matérias |

Nos três casos a resposta certa não era escrever a lição de novo: era reconhecer que a
regra existente não estava funcionando. Nos três, isso só apareceu quando alguém contou à
mão.

**b) Não registra a rejeição.** `padroes` lista classes candidatas; se uma é examinada e
descartada, nada guarda a decisão. O mesmo candidato pode voltar todo ciclo e consumir
leitura humana de novo.

**c) Não tem teto nem prazo.** Não há limite de adoções por ciclo, nem vencimento para
regra adotada e não verificada. O `RETROSPECTIVAS.md` chegou a 1.104 linhas.

**d) Não aprende fora do retorno humano.** O único gatilho de aprendizado é a correção do
titular, que chega dias depois do protocolo. O que a própria esteira produz todo dia —
gate que reprovou, fase que travou, suíte que ficou vermelha, insumo bloqueado — não
alimenta aprendizado nenhum.

## 2. O que o Hermes tem, medido

O Hermes roda em `/root/.hermes/memory_pipeline` desde 16/05/2026: colheita automática das
sessões → triagem que descarta o transitório → recombinação que procura padrão entre
sessões → promoção seletiva para memória, skill ou sonho. O sonho noturno é cron às 21:30.

**Resultado real:** o ciclo de 10/08 colheu 6 candidatos e promoveu **0**. O livro de
aprovações tem **1 aprovada contra 9 rejeitadas**, e há cerca de 20 pendentes desde maio.
Vários relatórios diários seguidos fecham com "Promovidos: 0".

O diagnóstico está escrito pelo próprio sistema, em 02/08/2026:

> "O problema dos sonhos não é falta de inteligência nem falta de insights. É falta de
> aplicação. O sistema identificou corretamente o mesmo defeito 57 vezes, mas nunca
> converteu a lição em filtro, regra ou código."

*(Citação de artefato interno do Hermes; é a autoavaliação deles, não medição minha.)*

A resposta que construíram em 02–03/08 é o que vale trazer: um detector de reaprendizado,
um catálogo fechado de defeitos com prazo, verificação agendada de efeito, e um placar de
valor. **A parte da frente — a colheita — é justamente a que não rende.**

Isso importa para a decisão: copiamos a metade de trás, não a de frente. A nossa entrada é
melhor que a deles (correção escrita do titular, com o par de textos no cofre), e a nossa
esteira produz sinal estruturado que o chat deles não produz.

Ressalva de honestidade: o mecanismo do `relearn` tem **oito dias de vida**. O único
defeito aberto por ele até agora é sobre o próprio runtime dele, e continua aberto. Isso
prova que o detector detecta; não prova que o ciclo fecha.

## 3. Bloco A — reaprendizado vira defeito

A tese, na primeira linha do módulo deles: **conceito recorrente vira defeito, não lição
nova.**

### Regra de classificação

Quando uma classe de correção reaparece dentro de uma janela de 30 dias:

- **`aplicacao_ausente`** — reapareceu e não há regra adotada para ela. É a adoção normal,
  pelo caminho que já existe.
- **`regra_ineficaz`** — reapareceu **e já existe regra adotada e aplicada**. Isto não é
  aprendizado novo: é prova de que a regra em vigor não está funcionando. Severidade alta
  por definição.

A distinção é exatamente o campo `aplicadaEm`/`destinoArquivo` que o registro já tem.

### Ciclo de vida do defeito

- nasce `aberto`, com `venceEm` = abertura + 7 dias;
- sobe para severidade alta se `regra_ineficaz`, ou se as ocorrências chegam a 3, ou se
  vence o prazo;
- **reabre sozinho** se estava `corrigido` e o conceito reaparece — o estado volta a
  `aberto` e as ocorrências acumulam;
- só fecha com **efeito exigido declarado e critério de aceite atendido**, no formato que
  o Hermes usa: o que precisa existir para o defeito estar fechado, verificável por
  terceiro. Prosa dizendo "corrigido" não fecha.

### Alterações

| Arquivo | Alteração |
|---|---|
| `forja_reaprendizado.py` | **novo.** Detector, classificação, abertura e reabertura de defeito, listagem por severidade e vencimento. |
| `learning_registry/DEFEITOS.json` | **novo.** Registro dos defeitos, com `dedupeKey` para idempotência. |
| `forja_aprendizado.py` | `padroes` passa a consultar o detector e marcar cada classe como `novo`, `aplicacao_ausente` ou `regra_ineficaz`. |
| `forja_delivery.py` | elo 5-B passa a barrar também por **defeito de severidade alta vencido**, não só por regra fora do destino. |
| `forja_censo.py` | um achado novo (`CEN7`) para defeito de aprendizado vencido, na mesma leitura que já mostra a população. |
| `test_forja_reaprendizado.py` | **novo.** Fixtures: as três âncoras reais da tabela do §1, anonimizadas por classe. Cada uma deve produzir `regra_ineficaz`. |

### Âncora de projeto

O teste de aceitação do bloco: alimentado com o histórico real das três reincidências da
tabela, o detector abre **três** defeitos `regra_ineficaz` — nenhum a menos. Se abrir
menos, a janela ou a chave de equivalência estão erradas. Se abrir muito mais, está
confundindo ocorrência com classe, e vira ruído.

## 4. Bloco B — verificação de efeito com prazo

Hoje `conferir` responde "a frase está no arquivo". O Hermes tem um catálogo fechado de
quatro tipos de verificação, agendada 14 dias depois da aplicação, e o que interessa é o
tipo `policy_effect`: roda um **verificador registrado** e compara o observado, em vez de
aceitar declaração. Quando não há como conferir, o resultado é `pulado` — **nunca
`passou` presumido**.

### Como isto se encaixa na FORJA

Nós temos o melhor verificador possível já pronto: **os gates**. Uma regra cujo destino é
`gate_computado` tem verificador natural — o próprio gate. As demais precisam de um
verificador declarado no momento da adoção, e é isso que muda o desenho: **adotar passa a
exigir dizer como se saberá que funcionou.**

Catálogo fechado proposto:

| Tipo | O que faz | Quando usar |
|---|---|---|
| `destino_presente` | o texto/`regraId` está no arquivo de destino | é o `conferir` de hoje; continua, rebaixado a mínimo |
| `gate_registrado` | roda um gate nomeado e exige veredito | regra com destino `gate_computado` |
| `efeito_na_producao` | conta ocorrências da classe **depois** da adoção contra as de antes | regra de checklist/template |
| `sem_rota` | declara que não há como conferir daqui, com motivo | quando é verdade — e nunca vira `passou` |

`efeito_na_producao` é o coração: se a classe continua aparecendo na mesma taxa depois da
regra, a verificação **falha** e abre defeito `regra_ineficaz` — fechando o laço com o
Bloco A sem intervenção humana.

### Alterações

| Arquivo | Alteração |
|---|---|
| `forja_aprendizado.py` | `adotar` ganha `--verificador <tipo>` obrigatório e `--verificador-param`; `aplicar` agenda a verificação; comando novo `verificar` roda as vencidas. |
| `learning_registry/VERIFICACOES.json` | **novo.** Agendadas, com `previstaPara`, estado e observado. |
| `learning_registry/REGRAS_APRENDIDAS.json` | campos novos: `verificador`, `verificadorParams`, `verificadaEm`, `resultadoDaVerificacao`. Regras existentes ficam `verificador: null` e são migradas por decisão humana, não por padrão. |
| `test_forja_aprendizado.py` | casos novos: verificação vencida que falha abre defeito; `sem_rota` nunca conta como aprovada; verificação não pode ser fechada sem observado. |

**Dívida honesta a declarar no primeiro run:** as 20 regras já adotadas não têm
verificador. Elas entram como `verificador: null` e aparecem no placar como *não
verificáveis*, com esse nome. Não inventar verificador retroativo: seria exatamente o
autoengano que o bloco existe para impedir.

## 5. Bloco C — a rejeição também é decisão

O relatório noturno do Hermes nomeia cada candidato descartado e por quê, com vocabulário
curto: eco de ciclo anterior, status datado, incidente transitório, entrega específica,
procedimento já coberto. É barato e evita que o mesmo candidato volte todo ciclo.

### Alterações

| Arquivo | Alteração |
|---|---|
| `forja_aprendizado.py` | comandos `rejeitar <classe> --motivo <vocabulário> --por <nome>` e `adiar <classe> --ate <data>`. |
| `learning_registry/DECISOES.json` | **novo.** Uma linha por decisão, com chave de idempotência. |
| `forja_aprendizado.py padroes` | passa a esconder classe rejeitada, **exibindo o total escondido e o motivo agregado** — nunca omitir em silêncio. |

Vocabulário fechado proposto: `eco_de_ciclo_anterior`, `status_datado`,
`incidente_transitorio`, `especifico_do_caso`, `ja_coberto_por_regra`, `sem_lastro`,
`ruido_de_comparacao`.

O último existe por causa de fato medido nesta casa: três retornos com 0,7%, 3,1% e 13,4%
de texto em comum não eram revisão de peça nossa, e sozinhos respondiam por 496 mudanças
agregadas com forma de padrão. O gate `PP-NOT-A-REVISION` já barra na entrada; o
vocabulário registra quando barrou.

## 6. Bloco D — o sonho noturno da FORJA

**O pedido:** toda noite, gerar sonhos de aprendizado de todos os casos do dia, revisão da
FORJA e das causas, gerando insights.

**A armadilha, escrita pelo próprio Hermes na lista de antipadrões dele:** "fazer sonho
poético sem extração operacional". E a nossa: já temos 326 lições. Um gerador diário de
lições que ninguém lê não é aprendizado — é o `RETROSPECTIVAS.md` crescendo até virar
inútil.

Por isso o desenho tem três travas antes de qualquer coisa:

1. **O sonho não escreve no `RETROSPECTIVAS.md`.** Ele só abre candidato no registro de
   aprendizado, abre defeito, ou escreve o relatório da noite. Promoção a lição ou regra
   continua sendo humana, com `--aprovado-por`.
2. **Teto de 3 candidatos por noite**, e "0 candidatos" é resultado legítimo e esperado na
   maioria das noites.
3. **O sonho lê estrutura, não a peça.** Ele nunca abre o texto do documento do cliente.
   Trabalha sobre veredito de gate, situação de caso, causa declarada e classe — e por
   isso não pode vazar dado do escritório para o insight.

### O que ele lê (tudo já existe no disco)

| Fonte | O que extrai |
|---|---|
| `forja_censo.py` (hoje × ontem) | caso que mudou de situação, caso que não mudou há N dias, prazo se aproximando |
| `f7_gate_result.json` do dia, em todos os casos | qual gate reprovou, em quantos casos distintos |
| `forja_verificador.py` / `forja_lastro.py` | P0 recorrentes por classe |
| último `telemetria/BASELINE_*.json` | suíte que ficou vermelha, quarentena que envelheceu |
| `F1_INSUMO_BLOQUEADO.json` | causa de bloqueio por fonte, e bloqueio vencido |
| `F10_RETORNO_SEM_ANEXO.json` + loop pós-protocolo | correção humana chegada no dia |
| `learning_registry/` | regra vencida sem verificação, defeito aberto |

### O que ele faz com isso

Duas passagens, com nomes emprestados do Hermes porque descrevem bem o que são:

**Triagem (o que o Hermes chama de NREM).** Determinística, em Python, sem modelo:
descarta o que é datado e transitório; agrupa por classe; e aplica a **regra de ouro dos 7
dias** — o que envelhece em uma semana não vira aprendizado. Saída: uma lista curta de
sinais do dia, com contagem e denominador.

**Recombinação (o que o Hermes chama de REM).** Aqui entra modelo, e só aqui. A pergunta
que ele responde não é "o que aconteceu hoje" — é **"o que aconteceu hoje que já tinha
acontecido antes, e que a esteira deveria ter impedido"**. Insumo: os sinais da triagem
mais o registro de regras e defeitos. Saída obrigatoriamente estruturada: candidato com
classe, evidência apontada por localizador, e uma hipótese de destino. Sem localizador,
o candidato é descartado no próprio validador.

### Alterações

| Arquivo | Alteração |
|---|---|
| `forja_sonho.py` | **novo.** `triagem`, `recombinar`, `relatorio`, `--seco` (roda sem modelo, só a triagem). |
| `state/SONHOS/<data>.json` e `.md` | **novo.** O artefato da noite: sinais, candidatos, descartes com motivo, lacunas. |
| `templates/SONHO_NOTURNO.md` | **novo.** Contrato do relatório, com as seções obrigatórias — inclusive **"Lacunas"**, que é onde a noite declara o que não conseguiu fazer. |
| `test_forja_sonho.py` | **novo.** Candidato sem localizador é rejeitado; teto de 3 respeitado; sonho não escreve em `RETROSPECTIVAS.md`; nenhum nome de cliente atravessa para o insight (teste de fronteira dedicado). |

### Modelo

Roda com a mesma disciplina de revisão cruzada que a casa já exige: o produtor do sonho
não pode ser a família que produziu as peças do dia. Como as peças saem majoritariamente
no Claude, o sonho roda no Codex (`gpt-5.6-luna`, esforço `max`) ou no Grok pela assinatura
do Cursor. Isso não é preciosismo: red team feito pelo modelo que produziu o trabalho
repete os próprios pontos cegos com voz mais dura — é o motivo declarado do Diabob.

## 7. Bloco E — turno noturno de trabalho automático

Hoje a FORJA já tem **sete tarefas agendadas no Windows**, todas com último resultado 0:
loop pós-protocolo, sync dos repositórios, fios abertos, monitores de DJEN, STF e TPU, e
backup. Ou seja: a infraestrutura de agendamento existe e funciona.

Faltam três coisas: (a) as tarefas **não avisam ninguém quando falham** — "resultado 0"
significa que a tarefa rodou, não que fez algo; (b) não há janela onde a esteira **avança
trabalho**, só onde ela observa; (c) não há relatório de manhã dizendo o que a noite fez.

### O turno

Janela proposta: **01:00 às 05:00**, em ordem fixa, cada passo com registro próprio:

1. `forja_reconcile.py` — reconciliação da fila.
2. `forja_censo.py` + `forja_conferir_entregas.py --conferir` — a população e a dívida de auditoria.
3. `forja_insumo_bloqueado.py --vencidos` e `--probe` — devolve à fila o que o bloqueio tirou dela e testa as rotas ao vivo.
4. `forja_regimentos.py --limite-dias 90` — atualidade dos regimentos arquivados.
5. `forja_aprendizado.py verificar` — as verificações vencidas do Bloco B.
6. `forja_reaprendizado.py` — abre e reabre defeitos.
7. `forja_sonho.py` — a noite propriamente dita.
8. `forja_baseline.py` — a corrida completa, que hoje ninguém roda todo dia.
9. Relatório da manhã.

### A trava que define o turno

**O turno noturno nunca promove fase, nunca envia nada para fora e nunca toca no texto de
uma peça.** Ele reconcilia, confere, revalida, mede, aprende e relata.

Isto não é conservadorismo: `promote` autônomo às 3h da manhã, sem humano, é a maneira mais
eficiente de industrializar exatamente a queixa que originou tudo isto — trabalho pela
metade dado como feito. A ordem inviolável do conselho (Helena, Cícero, Diabob em F4) e a
revisão editorial de F7 pressupõem decisão; a noite prepara o terreno para elas.

### Alterações

| Arquivo | Alteração |
|---|---|
| `forja_turno_noturno.ps1` | **novo.** Orquestra os nove passos, com trava anti-concorrência e registro por passo. |
| `forja_job_com_alerta.ps1` | **novo.** Equivalente ao `hermes-run-with-alert`: roda o comando, e **só** avisa quando falha, com as últimas linhas do log. Aplicar às **sete tarefas que já existem**, não só ao turno. |
| `reports/TURNO_NOTURNO_<data>.md` | **novo.** O que rodou, o que mudou, o que falhou, o que ficou para o humano. |
| Tarefa agendada `FORJA-Turno-Noturno` | **nova.** |

### Briefing da manhã

O Hermes tem briefing às 07:00 e às 14:00 em dias úteis. A FORJA merece um às 08:00:
resultado do turno, o que o sonho propôs, defeitos vencidos, prazos da semana e o que
espera decisão sua. Um parágrafo, não um painel.

## 8. Bloco F — outros recursos do Hermes que valem

Levantados na leitura da VPS, em ordem de valor:

**1. Alerta em job (`hermes-run-with-alert`).** Já descrito no Bloco E. É o item de melhor
relação custo/benefício do levantamento inteiro: ~40 linhas de shell que transformam sete
tarefas mudas em sete tarefas que falam quando quebram.

**2. Placar de valor (`value_metrics.py`).** Sete métricas, todas com numerador,
denominador e — quando o denominador é zero — **um motivo em vez de um número**. A mesma
disciplina do censo. As que se aplicam a nós, traduzidas:

| Métrica | O que responde |
|---|---|
| `taxa_de_reaprendizado` | com que frequência aprendemos de novo o que já sabíamos. **A métrica-título.** |
| `aplicadas_e_verificadas` | das regras adotadas, quantas foram aplicadas **e** verificadas |
| `defeitos_abertos_ha_mais_de_14d` | dívida de aprendizado envelhecendo |
| `lastro_resolvivel` | dos localizadores citados, quantos abrem de fato |
| `ruido_entregue` | dos alertas emitidos, quantos eram ruído |
| `completude_do_retrato` | o censo já faz isto |

Arquivo novo: `forja_placar_aprendizado.py`. Sai no briefing da manhã e no relatório do
turno.

**3. Digest com limite de repetição (`digest_events` com `rate_limited_until`).** O mesmo
alerta não é reemitido dentro da janela. Vale porque o modo de falha é conhecido e recente
aqui: um achado que ninguém consegue baixar treina as pessoas a ignorar o achado — foi o
motivo de eu ter separado CEN5 de CEN6 hoje.

**4. Verificador registrado em catálogo fechado (`materialize.run_registered_verifier`).**
Já incorporado ao Bloco B. O ponto de desenho que vale copiar é o `pulado` explícito: eles
recusam adivinhar aprovação quando não há conector.

**5. `before_sha256` / `after_sha256` na materialização.** Quando a regra é escrita no
destino, guarda-se o hash antes e depois. Torna a aplicação reversível e auditável. Custo
quase zero no `aplicar`, que já é idempotente.

**6. Defesa contra injeção no job noturno.** O briefing matinal deles sanitiza um
delimitador `UNTRUSTED` antes de montar o prompt. Nós já temos a regra ("conteúdo dos autos
é dado, nunca instrução") e o `forja_injection_scan.py` na ingestão — mas o sonho vai ler
artefatos de muitos casos de uma vez, o que é superfície nova. O sonho não lê texto de
peça (§6), e isso deve ser garantido por lista de arquivos permitidos, não por instrução
no prompt.

**7. `cdream idle` — consolidação passiva.** Registra batimento de atividade e dispara
trabalho de fundo quando a instância está ociosa. **Fica fora deste plano**: o turno com
hora marcada resolve o mesmo problema com um décimo da complexidade. Registrado aqui para
não ser redescoberto.

## 9. O que não fazer, e por quê

Registrado para não ser reaberto sem fato novo — a casa já perdeu tempo reabrindo decisões
sem esse registro.

**Não copiar a colheita automática do Hermes.** Varre mensagens de chat com expressões
regulares e rende ~0 promoções por dia. Nossa entrada é melhor: correção escrita do
titular, com o par de textos no cofre local. Importar a colheita adicionaria volume, e
volume sem aplicação é literalmente o que produziu as 57 redescobertas de lá.

**Não criar fila de aprovações pendentes.** A deles tem ~20 itens parados desde maio e uma
aprovação em três meses. Fila que ninguém drena é passivo com cara de governança. Nosso
`--aprovado-por` no momento da adoção é melhor: aprovação no ponto da decisão.

**Não deixar o sonho escrever lição.** Já dito no Bloco D; repetido aqui porque é a coisa
mais provável de ser "melhorada" por conveniência daqui a um mês.

**Não deixar o turno noturno promover fase.** Idem.

**Não medir aprendizado por contagem bruta de correções.** Um processo longo produz
centenas de mudanças sozinho. A régua é **recorrência entre casos distintos**, que o
`padroes` já usa, e agora também **queda da taxa depois da regra**.

## 10. Ordem de execução e custo

Os blocos A e B são **um só laço** e não devem ser separados: A sem B detecta e não
conserta; B sem A conserta sem saber que precisa. Estimativas em sessões de trabalho, não
em dias de calendário.

| Ordem | Bloco | Depende de | Tamanho | Por que nesta ordem |
|---|---|---|---|---|
| 1 | F.1 — alerta em job | nada | pequeno | melhor razão valor/custo; independente de tudo |
| 2 | A + B — reaprendizado e verificação | nada | grande | é o núcleo do pedido |
| 3 | C — registro da rejeição | A | pequeno | barato, e limpa o `padroes` |
| 4 | F.2 — placar de valor | A, B | pequeno | sem A e B não há o que medir |
| 5 | E — turno noturno | A, B, C | médio | orquestra o que já existe |
| 6 | D — sonho noturno | E | médio | é um passo do turno; nasce dentro dele |
| 7 | F.3/F.5 — digest e hashes | E | pequeno | polimento |

**Nada aqui exige serviço novo, chave nova ou gasto novo.** Roda no agendador do Windows
que já hospeda sete tarefas, com os modelos já contratados. A única linha de custo variável
é a chamada de modelo do sonho: uma por noite, sobre um insumo pequeno e estruturado.

## 11. Como se mede que este plano funcionou

Critérios observáveis, definidos antes de construir para não serem ajustados depois:

1. **Detecção retroativa.** Alimentado com o histórico das três reincidências do §1, o
   detector abre três defeitos `regra_ineficaz`. Este é o teste de aceite do Bloco A.
2. **Taxa de reaprendizado cai.** Medida na janela de 90 dias, contra a linha de base que o
   primeiro run estabelecer. Se não cair em dois meses, o plano falhou e isso deve ser dito.
3. **Nenhuma regra adotada sem verificador** depois da data de corte. As 20 antigas
   aparecem no placar como não verificáveis, com esse nome, até serem migradas uma a uma.
4. **Falha de job vira aviso em menos de uma hora.** Hoje é indefinido.
5. **O sonho promove pouco.** Se estiver propondo três candidatos toda noite, o filtro está
   frouxo. A expectativa honesta é a maioria das noites fechar em zero — como as do Hermes,
   com a diferença de que as nossas terão de dizer por que descartaram.
6. **Ruído entregue perto de zero.** Alerta repetido dentro da janela não é reemitido.

## 12. O que exige decisão do titular

1. **Janela do turno.** 01:00–05:00 é proposta. Se o PC não fica ligado, o turno migra para
   a VPS e isso muda o desenho de acesso ao disco local — é a única decisão com efeito
   arquitetural real.
2. **Canal do alerta de falha.** O Hermes usa WhatsApp. Para a FORJA, e-mail é o caminho
   já autorizado e instrumentado.
3. **Migração das 20 regras existentes.** Atribuir verificador a cada uma é trabalho humano
   de leitura. Alternativa honesta: deixá-las declaradas como não verificáveis e migrar só
   quando cada uma reaparecer. **Recomendo a segunda**: migrar por demanda gasta esforço
   onde há sinal, e a primeira produziria vinte verificadores escritos de uma vez, a maioria
   nunca exercitada.
