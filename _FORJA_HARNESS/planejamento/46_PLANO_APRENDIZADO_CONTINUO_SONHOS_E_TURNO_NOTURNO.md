# 46 — Aprendizado contínuo, sonho noturno e turno automático da FORJA

> Plano de alterações. Escrito em 10/08/2026 a partir de leitura direta do sistema
> Hermes na VPS (via Tailscale) e do estado real da FORJA no disco. Nada aqui foi
> executado ainda.
>
> **Ampliado no mesmo dia por segunda leitura independente (Fable 5)**, que varreu as
> partes da VPS que a primeira passagem não abriu. As adições estão marcadas ao longo
> do texto; as afirmações de segunda mão que puderam ser conferidas na fonte foram
> conferidas — a tabela dos dois corpora do §2 foi verificada no arquivo original.
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
- [13. Consolidação das revisões externas](#13-consolidação-das-revisões-externas-11082026)

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

### 2.1 O que a segunda leitura acrescentou (Fable 5, conferido na fonte)

**Precisão sobre a arquitetura.** "O Hermes roda em `memory_pipeline`" é simplificação:
são quatro subsistemas separados — colheita (`memory_pipeline/`), sonhos narrativos
(`/root/.harness/dreams/daily/`), a lógica de verificação (`colmeia_dream/core/`) e a
fila de aprovação manual. A colheita não rende zero por falta de material: o inbox tem
**~2.470 candidatos acumulados**; é o filtro de durabilidade + a exigência de decisão
humana que fecham a saída. O problema deles não é colher — é decidir e aplicar.

**Os dois corpora, e a entrega invertida.** A revisão forense de 02/08 do próprio Hermes
(`docs/plans/2026-08-02-claude-opus5-review-sonhos-v08.md`, tabela conferida por mim no
arquivo original) mediu os 179 sonhos registrados e achou dois corpora com naturezas
opostas:

| Medida | sonho `diagnostico` (n=84) | sonho `operacional` (n=80) |
|---|---|---|
| referência verificável a arquivo | **0%** | **76%** |
| contém número/quantidade | **0%** | **82%** |
| verbo de ação ("salvei", "verifiquei") | 23% | 81% |
| é o que chega ao titular | **sim (WhatsApp)** | **não (fica local)** |

O ritual verbal sem ancoragem é o único entregue; o sonho com lastro fica na prateleira.
**A entrega está invertida** — e a frase-síntese do parecer de lá merece ser a epígrafe
do nosso Bloco D: *"o sistema diagnosticou corretamente o próprio defeito 57 vezes e
nunca o corrigiu, porque a lição nasce como prosa e morre como prosa."*

Duas consequências diretas para este plano: (a) o sonho da FORJA nasce estruturado ou
não nasce — está no Bloco D como trava; (b) **o que se entrega de manhã tem de ser o
artefato com lastro, não um resumo bonito dele** — o modo de falha do Hermes foi entregar
o ritual e engavetar a substância.

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
| `forja_censo.py` | um achado novo (`CEN8`) para defeito de aprendizado vencido, na mesma leitura que já mostra a população. (`CEN7` já existe — conflito real entre esquemas; a primeira versão deste plano propunha o código colidente, apanhado pela revisão externa.) |
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

**Objeção da segunda leitura, acatada em parte.** O Fable 5 propôs descartar
`efeito_na_producao` por inteiro: no Hermes o equivalente (`policy_effect`) opera sobre
sonhos diários; a FORJA produz peças em volume baixo, e a classe pode simplesmente não
ter oportunidade de reaparecer na janela — **ausência de recorrência não é prova de
efeito**. A objeção está certa quanto ao risco e errada quanto ao remédio: descartar o
tipo deixaria as regras de checklist/template de novo sem verificador nenhum, que é o
buraco de hoje. O desenho fica assim: `efeito_na_producao` só emite veredito quando houve
**denominador** — casos da mesma matéria produzidos na janela. Sem denominador, o
resultado é `sem_sinal_ainda` e a verificação se reagenda; `sem_sinal_ainda` não é
`passou`, pela mesma regra que `pulado` não é. O que o tipo afirma quando aprova é "a
classe teve N oportunidades de reaparecer e não reapareceu", com N declarado.

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

Por isso o desenho tem quatro travas antes de qualquer coisa:

1. **O sonho não escreve no `RETROSPECTIVAS.md`.** Ele só abre candidato no registro de
   aprendizado, abre defeito, ou escreve o relatório da noite. Promoção a lição ou regra
   continua sendo humana, com `--aprovado-por`.
2. **Teto de 3 candidatos por noite**, e "0 candidatos" é resultado legítimo e esperado na
   maioria das noites.
3. **O sonho lê estrutura, não a peça.** Ele nunca abre o texto do documento do cliente.
   Trabalha sobre veredito de gate, situação de caso, causa declarada e classe — e por
   isso não pode vazar dado do escritório para o insight.
4. **Sonho estruturado, nunca verbal.** Candidato sem `{classe, localizador, destino
   proposto}` é descartado no validador, antes de qualquer leitura humana. A âncora é a
   medição dos dois corpora do §2.1: no Hermes, o corpus com 0% de referência verificável
   é o que virou ritual — e o ritual foi o único entregue. Corolário de entrega: **o
   briefing da manhã anexa o artefato estruturado da noite**, nunca só uma prosa sobre
   ele.

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

1. `forja_baseline.py` — **primeiro**, como preflight: vermelho bloqueia a recombinação
   do sonho e qualquer passo que grave; inconclusivo vira lacuna declarada. (A primeira
   versão deste plano punha o baseline depois do sonho — o sonho raciocinaria sobre um
   verde velho e descobriria o vermelho tarde demais. Apanhado pela revisão externa.)
2. `forja_reconcile.py` — reconciliação da fila.
3. `forja_censo.py` + `forja_conferir_entregas.py --conferir` — a população e a dívida de auditoria.
4. `forja_insumo_bloqueado.py <raiz> --vencidos` — devolve à fila o que o bloqueio tirou
   dela; em passo separado, `forja_rotas_fonte.py --probe` testa as rotas ao vivo. (São
   dois scripts; a primeira versão atribuía `--probe` ao módulo errado.)
5. `forja_regimentos.py --limite-dias 90` — atualidade dos regimentos arquivados.
6. `forja_aprendizado.py verificar` — as verificações vencidas do Bloco B.
7. `forja_reaprendizado.py` — abre e reabre defeitos.
8. `forja_sonho.py` — a noite propriamente dita, só com o preflight verde.
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

**Não trazer o `promote.py` (decay/fitness/imunidade).** [Adição da segunda leitura,
acatada.] O Hermes dá a cada memória um fitness que decai com o tempo e uma poda
periódica. Faz sentido para memória procedural de longo prazo; não faz para o nosso
registro: aqui uma regra foi adotada ou não, foi verificada ou não, e se o conceito
reaparece vira defeito. Regra "dormindo com fitness baixo" é exatamente o estado ambíguo
que o Bloco A existe para eliminar. O voto nominal no momento da adoção substitui o
fitness.

**Não trazer o ciclo REM especulativo (`rem.py`).** [Adição da segunda leitura.] No
Hermes ele gera hipóteses e ameaças especulativas, e a varredura encontrou os registros
dominados por stubs sem ancoragem. A FORJA não precisa de ameaça especulativa; precisa de
defeito real com localizador. A recombinação do nosso Bloco D responde outra pergunta —
"o que de hoje já tinha acontecido antes" — sobre insumo estruturado, não sobre
imaginação.

**Não trazer o `orchestrator.py` de consolidação multi-ciclo.** [Adição da segunda
leitura.] Consolidar exige vários ciclos de produção por dia; o turno da FORJA é um ciclo
por noite. Complexidade sem substrato.

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
4. **Janela do limite de repetição do alerta.** [Levantada pela segunda leitura.] Janela
   longa silencia falha nova da mesma classe; curta reintroduz o ruído. Proposta: 3 dias,
   e o alerta silenciado conta no placar como `ruido_evitado` — silêncio também é decisão
   e também se mede.

## 13. Consolidação das revisões externas (11/08/2026)

O plano passou por três famílias de modelo: a primeira e a segunda leitura (Claude —
Opus 5 e Fable 5, §§ marcados ao longo do texto), a revisão técnica do **Codex
`gpt-5.6-sol` em esforço alto** (17 achados, veredito REPROVADO até três correções) e o
contraditório do **Diabob** (`grok-4.5-cursor`, parecer em
`reports/PARECER_DIABOB_PLANO46_2026-08-11.json`; o titular pediu Grok 4.6, e foi
conferido nas duas rotas — Cursor e OpenRouter — que a versão 4.6 não existe em nenhuma;
o 4.5 é o Grok mais novo alcançável, registrado aqui como ressalva e não como escolha).

As afirmações verificáveis dos revisores foram conferidas no código antes de aceitas —
as quatro checadas bateram: o `CEN7` já existia, o `--probe` era do módulo errado, o
agrupamento é só `(camada, causa)`, e `aplicar()` carimba `aplicadaEm` mesmo sem
mudança. Os erros factuais foram corrigidos no corpo (§§3 e 7). O que segue são as
decisões sobre o restante.

### 13.1 A objeção central do Diabob — acatada, e ela muda a tese do plano

**Objeção:** nas três âncoras do §1, a regra já estava escrita — e numa delas havia
gate — no momento da violação. Logo, "saber que é reincidência" pode não ser o gargalo;
o plano corre o risco de ser a 58ª pessoa a diagnosticar o mesmo defeito e chamar isso
de progresso. A pergunta que o plano evitava: **depois do defeito aberto, quem muda o
quê no caminho quente da peça, antes do próximo protocolo?**

**Decisão: acatada, com a seguinte reformulação da tese.** O detector não é o remédio;
é o disparador que a casa hoje não tem. O remédio a FORJA já conhece e já praticou:
**regra escrita que não pega vira gate** (S6 e S7 nasceram exatamente assim — na mão,
por dor). O que o Bloco A automatiza não é o aprendizado: é a *convocação* dele. Por
isso o fechamento de defeito muda de definição:

> **Defeito `regra_ineficaz` só fecha com mudança executável no caminho quente** — gate
> novo ou endurecido, item recomputado no contrato da fase, verificação no runner — com
> o identificador da mudança no registro. Reescrever a regra em prosa, em qualquer
> destino, **não fecha**.

E, antes de construir A+B, roda-se o **teste de realidade** que o Diabob propôs, como
Fase 0 do §10: classificar à mão as três âncoras e as próximas cinco reincidências do
`RETROSPECTIVAS.md` entre (I) "ninguém reconheceu a equivalência" e (II) "a classe era
óbvia e a esteira avançou assim mesmo". Se a maioria for (II), o investimento migra do
detector para a conversão em gate — e o plano diz isso com todas as letras em vez de
construir o detector primeiro porque ele é a parte divertida.

### 13.2 A segunda objeção do Diabob — acatada como métrica de guarda

Barrar entrega por defeito vencido (elo 5-B ampliado) pode produzir o equilíbrio
perverso: fechar defeito na véspera para destravar prazo — a prosa "corrigido" de volta,
disfarçada de checkbox. **Decisão:** todo defeito nasce com **dono nominal**, e o placar
do Bloco F ganha a coluna que o Diabob pediu: **defeitos fechados na véspera de uma
entrega ou para destravar o 5-B**. Se essa coluna passar de metade dos fechamentos em 30
dias, o dente do 5-B é teatro coercitivo e sai — critério escrito antes de instalar.

### 13.3 A terceira objeção do Diabob + achado 8 do Codex — acatados juntos

`efeito_na_producao` num sistema de volume baixo pode degradar em névoa: tudo
`sem_sinal_ainda` para sempre, parecendo que o laço roda sem nunca emitir veredito.
**Decisão:** (a) o denominador deixa de ser declarado e vira **computado** — cada regra
adotada com esse verificador traz um `opportunityPredicate` executável sobre campos
estruturados dos casos, que registra elegíveis, excluídos e motivo; (b) métrica de
guarda: **se menos de 20% das verificações desse tipo emitirem veredito em 60 dias, o
tipo está morto por falta de sangue** e a conclusão é essa, não um placar cinza.

### 13.4 Os três P0 do Codex — acatados integralmente

**(1) Chave de equivalência.** O ponto mais frágil do plano, como o próprio §3 não
admitia. `(camada, causa)` não separa as seis regras distintas que hoje vivem sob
`correspondencia:diretriz_escrita` — usar isso abriria falsos `regra_ineficaz` em série.
Decisão: duas chaves distintas — `occurrenceKey` (hash de artefato, gate, localizador e
evento: identifica o fato) e `equivalenceKey` (ontologia versionada
`{invarianteViolada, camadaSistema, fase, gateId, objeto}`: identifica a classe) — com
fixtures de pares equivalentes E contraprovas de pares que não podem ser equiparados.
A ontologia nasce pequena e cresce por alias aprovado, nunca por regex esperta.

**(2) Fronteira no sonho.** A trava 3 do Bloco D afirmava que ler estrutura basta para
não vazar — e é falso: `caseId`, caminho e mensagem de gate são dado da instalação.
Decisão: os registros de ocorrência e lastro vivem no **acervo/state**, nunca no motor;
o modelo do sonho recebe **agregados sanitizados com IDs opacos**; e a sanitização é
validada por **validador estrutural de campos** (allowlist do que PODE atravessar),
não por lista de nomes proibidos — a lição 326 já mostrou que chave opaca vaza sem
disparar gate lexical.

**(3) Concorrência.** Mutex no PowerShell impede dois turnos, não impede a sessão humana
das 2h da manhã — e o baseline desta semana já registrou árvore mudando durante a
corrida. Decisão: **lease cooperativo global** (arquivo com owner, heartbeat e validade,
respeitado por todos os mutadores novos), e cada passo do turno confere a revisão da
árvore antes e depois — deriva detectada aborta o passo **sem gravar**, e o relatório da
manhã diz qual passo abortou e por quê.

### 13.5 Demais achados do Codex — decisões em uma linha cada

| # | Achado | Decisão |
|---|---|---|
| 4 | idempotência sem chave definida; `aplicadaEm` carimba sem mudança | acatado — IDs determinísticos por ocorrência/aplicação/verificação/decisão; verificação só agenda em transição real (e o carimbo incondicional do `aplicar()` é bug a corrigir junto) |
| 5 | sonho antes do baseline | acatado — já corrigido no §7 (preflight primeiro) |
| 6 | janela de 30 dias atravessando o legado sem série temporal | acatado — ledger de ocorrências com `occurredAt`; legado importa como `tempo_desconhecido`; detector roda em sombra até o corte confiável |
| 7 | `--verificador` ainda é declaração | acatado — o tipo resolve em catálogo de callables, com dry-run na adoção e recibo (hash do código, população examinada, veredito) |
| 9 | `destino_presente` contaminando a métrica de verificadas | acatado — `materializacaoVerificada` não é `efeitoVerificado`; presença nunca entra no numerador de efeito |
| 10 | colisão CEN7 | acatado — corrigido no corpo para CEN8 |
| 11 | `--probe` no módulo errado | acatado — corrigido no §7 |
| 12 | exit codes com semânticas incompatíveis sob um wrapper único | acatado — adaptador por job (`ok/finding/inconclusive/error`); "não zero" não é sinônimo de falha |
| 13 | "resultado 0 = funciona" contradiz a regra da casa | acatado — canário por tarefa: execução recente + artefato esperado + frescor, antes de envelopar as sete |
| 14 | rejeição de classe escondendo evidência nova para sempre | acatado — decisão vincula a `{versãoDaEquivalência, hashDoConjuntoDeEvidência}`; ocorrência nova ou defeito reaberto invalida a ocultação; defeito ativo prevalece sobre rejeição e adiamento |
| 15 | "nunca envia nada" contra alerta/briefing | acatado — worker escreve **outbox** local; um notifier separado, com canal allowlisted e deduplicação, envia; a promessa do turno passa a ser "não envia diretamente" |
| 16 | família do produtor sem prova computada | acatado — famílias derivadas dos recibos dos runs do dia; sem família disjunta autenticada, o sonho roda só a triagem determinística e registra `cross_family_unavailable` |
| 17 | custo subestimado | acatado em parte — orçamento por noite (tempo, timeout, teto de retries) entra no desenho do turno; a estimativa de horas humanas fica para depois da Fase 0, porque depende do resultado dela |

### 13.6 O que foi rejeitado das revisões

**Do Codex, nada foi rejeitado no mérito** — os 17 achados sobreviveram à conferência
(os 4 verificáveis batidos no código; os demais são de desenho e se sustentam sozinhos).
O veredito REPROVADO é aceito como estado do plano *antes* desta seção: as três
correções indispensáveis dele são exatamente os §§13.4(1), 13.4(3) e o par 13.3/13.4(2).

**Do Diabob, rejeita-se a conclusão maximalista** de que "sobram F.1 e talvez hashes".
Ela só segue se o teste de realidade der (II) maciço — e é para isso que a Fase 0
existe. Se der misto, detector E conversão em gate são ambos necessários: o detector
convoca, o gate corrige. A provocação dele fica registrada como o critério de desempate
do §11: *se a reincidência das classes-âncora não cair antes de o placar ficar bonito,
o plano errou o mecanismo.*

### 13.7 Efeito na ordem de execução (§10 revisado)

| Ordem | Etapa | Novidade desta consolidação |
|---|---|---|
| 0 | **Teste de realidade** (classificar 8 reincidências à mão) + piloto de 14 dias do F.1 | novo — barato, e decide onde vai o investimento |
| 1 | F.1 — alerta em job, com adaptador de exit code e canário por tarefa | endurecido (achados 12 e 13) |
| 2 | Ontologia de equivalência + ledger de ocorrências (em sombra) | novo pré-requisito dos blocos A e B |
| 3 | A + B — com fechamento por mudança executável, dono nominal e verificador com recibo | reformulados |
| 4 | C — rejeição vinculada a evidência | endurecido (achado 14) |
| 5 | F.2 — placar, com as métricas de guarda 13.2 e 13.3 | ampliado |
| 6 | E — turno com lease global, preflight de baseline e outbox | endurecido |
| 7 | D — sonho, com sanitização estrutural validada | endurecido |

A Fase 0 não é enfeite processual: é a diferença entre construir o instrumento certo e
construir o instrumento divertido. Custa uma sessão de leitura e catorze dias de
observação passiva — e o resto do plano fica melhor definido em qualquer um dos
desfechos dela.
