# Diagnóstico e plano — constância visual da FORJA

> **Lugar no plano geral:** esta é a **Trilha V** da § 26 de `40_PLANO_CONSOLIDADO_DIAGNOSTICO_E_DESIGN_FORJA_V2.md`, que é a fonte canônica de execução da FORJA. O estado resumido vive lá; o detalhe, aqui. Em divergência, vale o código.

> ## Estado da execução em 03/08/2026
>
> **Construído e verde.** Geração automática do mapa visual
> (`forja_visual_mapa_gen.py`); três geradores de diagrama em
> `medina_svg_kit.py` (cronologia, encadeamento de tese, matriz comparativa);
> extração do conteúdo das figuras (`forja_visual_figuras.py`); entrada única de
> produção (`forja_visual_build.py`); gate F8-S de assinatura visual
> (`forja_assinatura_visual.py`) com testes de mutação. Pipeline completo roda
> em **7 segundos por peça**, com fidelidade textual de 100%.
>
> **Prova.** A Impugnação CASO-04 V7 — apontada na auditoria como a pior
> regressão, 31 páginas com zero diagramas — foi recomposta em 27 páginas com
> capa institucional, quatro âncoras, treze linhas de síntese rotuladas, seis
> pull quotes, caixas e quatro elementos gráficos vetoriais, **conforme no gate
> F8-S sem nenhum achado**.
>
> **A medição que faltava.** O gate rodado sobre as 22 entregas mais recentes
> (27/07 a 03/08) dá **cobertura de 9% — duas peças conformes em vinte e duas**. O
> código mais frequente é `VIS-03`, ausência de elemento gráfico vetorial. Três
> das reprovadas são de 31/07, 02/08 e 03/08: a produção seguiu saindo fora do
> padrão enquanto a correção era construída. Este é o indicador que teria
> flagrado a regressão em 11/07/2026, quando a edição visual parou.
>
> **DECIDIDO pelo Igor em 03/08/2026 — não está mais aberto.** O `forja_render_docx`
> continua ativo como rota alternativa e o gate F8-S segue em **modo observação**
> (grava `F8S_ASSINATURA_VISUAL.json` e não bloqueia), mas isso agora tem prazo e
> ordem definidos. O Igor acatou a recomendação: **ligar depois do prazo de 05/08,
> nunca antes, e em duas etapas** — primeiro fechar a rota simples, que é o que de
> fato produz peça pobre, e só depois tornar o F8-S bloqueante.
>
> O motivo do adiamento é dele e está registrado: o risco concreto é uma peça com
> prazo travar num falso positivo do gate e alguém ter que destravar sob pressão.
> Nada disso relativiza a determinação de 30/07 — peça sem elementos visuais
> completos não sai, bloqueie o gate ou não. Sequência operacional na seção 10 e
> no plano 25.
>
> **Revisão cruzada com a família Codex (03/08/2026) — e o que ela derrubou.**
> O apontamento do Diabob de que havia **circularidade de autovalidação** (o
> gate escrito por quem produz as peças, a métrica calculada com esse gate, a
> peça aprovada por esse critério) foi endossado pelo Igor e levado a revisão
> cruzada. Ela confirmou um defeito material: a contagem de caixas de destaque
> casava qualquer célula sem borda superior, **inclusive as do quadro zebrado** —
> treze onde havia três, e 672 em documento cheio de tabela. O efeito não era
> estatístico: **mascarava a ausência total de destaque**, e o Aditamento CASO-07
> passava no critério de varredura por causa de 521 caixas fantasmas. Corrigido,
> ele reprova corretamente.
>
> Ao corrigir a checagem de timbre descobriu-se que a arte do cabeçalho usa
> `3a5c61` e `d9936a`, **um dígito fora dos tokens da paleta**. A primeira
> correção passou a exigir a paleta e reprovou a peça aprovada pelo escritório;
> o teste-âncora impediu a regressão de entrar. A prova passou a ser estrutural
> (desenho vetorial no cabeçalho), com controle negativo: peça nascida de
> `Document()` vazio reprova.
>
> Um achado da revisão foi **derrubado com evidência**: a alegação de que a
> contagem de molduras somava o rodapé institucional. As sete ocorrências estão
> no `document.xml` e os três cabeçalhos têm zero.
>
> **A cobertura anunciada estava errada por defeito do próprio gate: 5% viraram
> 9%.** A conclusão se mantém, a magnitude não.
>
> **O conselho de quatro personas não pegou nada disso.** Ele leu o dossiê
> escrito pelo construtor e recomendou integrar a composição dentro do render —
> arquitetura já analisada e rejeitada — citando uma função (`build_visual()`)
> que não existe. A data de ativação de 06/08 que ele fixou **não se sustenta**.
> Lições 93 a 95 em `RETROSPECTIVAS.md`.
>
> **Recomendação técnica atual, contrária à do conselho.** Manter o gate em
> observação. Em três dias este instrumento teve três defeitos materiais — dois
> achados por revisão externa e um por teste-âncora. Um gate com essa taxa de
> correção recente não deve barrar entrega de peça com prazo processual. A
> decisão de ligar volta quando ele acumular laudos da produção real sem defeito
> novo.
>
> **Correção de rumo registrada.** Dois "defeitos" listados na primeira versão
> deste documento — os retângulos cinza no topo da capa e o vazio na metade
> inferior — foram **derrubados** na comparação com a peça aprovada em
> 09/07/2026: são arte do timbre e estilo de capa da casa. Defeito só é defeito
> contra o padrão aprovado, não contra a impressão de quem olha.


**Data:** 30 de julho de 2026
**Origem:** investigação em seis frentes com verificação adversarial, retificada por conferência direta no código e nos arquivos
**Determinação que rege este documento:** ordem do Igor em 30/07/2026 — *nenhuma peça sai da FORJA sem elementos visuais completos; nenhum caminho que passou pela FORJA entrega sem padrão visual completo; sem atalhos; o visual vale tanto quanto o conteúdo.*

---

## 1. Veredito

A edição visual da FORJA não se degradou aos poucos. **Ela parou de acontecer em 10 de julho de 2026.**

Entre 8 e 10 de julho houve uma janela em que quase toda a produção saiu em edição visual law: CASO-04, CASO-14, José CASO-15, CASO-16, CASO-02, CASO-19, CASO-07 e CASO-17. São 25 arquivos `*VISUAL_LAW*.docx` no acervo, e **o mais recente é de 10/07/2026**. Nos vinte dias seguintes, com dezenas de entregas ao Fábio, a contagem é zero.

A causa é de acoplamento, não de competência. O compositor `forja_visual.compor()` existe, funciona e é coberto por testes — mas **nenhum módulo de produção o importa**. Quem o chama são os testes automatizados e cinco scripts artesanais escritos à mão dentro de pastas de caso. A peça só sai visual se alguém, naquele caso específico, sentar e escrever o mapa visual manualmente. Foi o que aconteceu naquela janela de três dias, quando o kit era novidade e havia atenção humana em cima. Quando a atenção migrou para outros casos, a esteira voltou ao seu comportamento padrão — e o comportamento padrão é pobre.

Um ponto precisa ser dito com clareza porque muda o plano: **o gate visual já existe e já é bloqueante.** O `forja_delivery.py` cria o elo *"4-B. Edição visual law (padrão Medina Osório)"*, exige lastro de fidelidade com conferência de SHA-256 do DOCX, e encerra o processo com `SystemExit(2)` quando qualquer elo falha. O defeito não é gate frouxo. É que esse gate mora numa rota que quase ninguém percorre: **três casos em toda a história da esteira têm trilha F10 executada.** A produção real passa por fora dele.

A consequência prática para a sua ordem é direta: fechar o gate hoje, sozinho, não recupera qualidade — **pararia a fábrica inteira**, porque nenhuma peça atual passaria. A sequência correta é inverter a dependência primeiro. O visual precisa ser o caminho padrão, gerado automaticamente, para só então o gate valer para todas as rotas de saída.

---

## 2. Evidência

### 2.1. Contagens conferidas diretamente

| Medida | Valor | Como foi conferido |
|---|---|---|
| Arquivos `*VISUAL_LAW*.docx` no acervo | 25 | `find` na árvore inteira |
| Data do mais recente | **10/07/2026** | carimbo de data dos mesmos arquivos |
| Mapas visuais declarativos `compor_*_mapa.py` | **5** (CASO-02, CASO-07, CASO-16, CASO-17, CASO-19) | `find` na árvore inteira |
| Casos em `state/` | mais de 30 | listagem do diretório |
| Casos com trilha de entrega F10 executada | **3** (CASO-02, CASO-04 AgInt, CASO-16) | `find` por `F10_TRILHA_EVIDENCIA.md` |
| Lastros `FIDELIDADE_VISUAL.json` | 20 | `find` na árvore inteira |
| Módulos de produção que importam `forja_visual` | **0** | `grep` em todos os `.py` do harness |

### 2.2. Medição automatizada dos DOCX

A frente de medição abriu os documentos como pacote e contou elementos. Os números abaixo vêm dessa medição automatizada; a direção é consistente com as contagens da seção 2.1, mas os valores por documento não foram reconferidos um a um.

| Período | Peça | Data | Vetoriais | Tabelas | Sombreado | % negrito |
|---|---|---|---|---|---|---|
| Modelo | EDcl José CASO-15 V1 | 09/07 | 5 | 9 | sim | 30,9% |
| Modelo | CASO-14 V2 | 09/07 | 3 | 6 | sim | 34,1% |
| Modelo | CASO-16 V2 | 09/07 | 3 | 7 | sim | 38,0% |
| Modelo | CASO-04 AgInt | 10/07 | 4 | 6 | sim | 33,6% |
| Recente | Parecer CASO-17 | 19/07 | 0 | 12 | não | 19,0% |
| Recente | Nota técnica | 21/07 | 0 | 26 | não | 87,8% |
| Recente | Matriz de títulos | 20/07 | 0 | 1 | não | 100,0% |
| Recente | Checklist CASO-07 | 29/07 | 0 | 5 | não | 88,7% |

Média de elementos vetoriais nas peças-modelo listadas: **3,75 por peça** (intervalo de 3 a 5). Média nas entregas recentes: **0,14**. Proporção de entregas recentes com zero elemento vetorial: **92%**.

Repare no que a coluna de negrito revela. Nas peças-modelo o negrito fica entre 30% e 38% — é ênfase com hierarquia. Nas recentes ele oscila de 19% a 100%. Um documento com 100% de negrito não tem ênfase nenhuma: quando tudo é destaque, nada é destaque. Isso não é só ausência de diagrama, é perda do negrito estratégico como instrumento, exatamente como você percebeu.

### 2.3. Correção de um nexo causal falso

A frente de arqueologia atribuiu a queda ao commit `ef2fcf98` (15/07/2026, *"modularize Word render and independent visual QA"*), afirmando que ele removeu a integração visual. **O commit existe, mas a atribuição está errada e foi retirada deste documento.** A versão mais antiga de `forja_render_docx.py` disponível no repositório (`7da64020`, 11/07) também não importa `forja_visual`. A integração nunca existiu para ser removida. O refactor de 15/07 é inocente; o que houve foi o fim da janela de trabalho manual em 10/07.

Essa correção importa na prática: se a causa fosse uma regressão de commit, bastaria reverter. Como a causa é ausência de acoplamento desde sempre, é preciso construir.

---

## 3. Causas-raiz

### Causa 1 — O compositor está desligado da produção

`forja_visual.py` tem 469 linhas e expõe `compor(md_path, out_docx, mapa)` na linha 115. Nenhum módulo de produção o importa. O `forja_render_docx.py` importa, na linha 31, apenas o `forja_visual_review` — a revisão pendente, não o compositor. O render converte markdown em DOCX com parágrafos, negrito e tabelas simples, e termina ali.

**Classe:** capacidade existente, não acoplada.
**Peso:** é a causa dominante. Explica a totalidade das entregas sem elemento vetorial.

### Causa 2 — O mapa visual é uma dependência humana

`compor()` exige um dicionário `mapa` que declara o que vira linha de síntese, o que vira pull quote, o que vira caixa e onde entram as figuras. Não existe gerador automático desse mapa. Existem cinco mapas escritos à mão, todos datados de 9 e 10 de julho, nenhum posterior.

É aqui que mora a inconstância. Um recurso que depende de esforço manual por caso não sobrevive ao volume: funciona enquanto há atenção, some quando a atenção vai para outro lugar. As peças bonitas de que você lembra são exatamente as cinco que ganharam mapa manual.

**Classe:** capacidade ausente.
**Peso:** é o que impede a Causa 1 de ser resolvida com uma linha de import. Sem gerador de mapa, acoplar o compositor não produz nada.

### Causa 3 — O gate existe, mas na rota errada

`forja_delivery.py:185` implementa `visual_com_lastro()`, que confere o SHA-256 do DOCX contra o `FIDELIDADE_VISUAL.json` e rejeita versão desatualizada ou alterada depois do gate. A linha 268 registra o elo 4-B. A linha 476 encerra com `SystemExit(2)`. É um gate sério e bem construído.

Só que ele roda no fechamento F10, e o F10 foi executado em três casos. Todas as outras saídas — empacotamento, entrega manual, produto interno, anexo de e-mail — não passam por ele.

**Classe:** rota de fuga por ausência de ponto único de passagem.
**Peso:** é o que permite que a Causa 1 e a Causa 2 passem despercebidas por vinte dias sem nenhum alarme.

### Causa 4 — O QA visual só procura defeito, nunca pobreza

`forja_visual_qa.py` e `forja_visual_review.py` verificam se algo quebrou: texto estourando margem, legenda cortada, rodapé colidido, marcador esquecido. Nenhum deles pergunta se os elementos existem. Um documento de texto corrido puro, sem um único diagrama, passa limpo em ambos — porque não há nada quebrado para encontrar.

**Classe:** gate defensivo sem contraparte afirmativa.
**Peso:** explica por que a regressão foi silenciosa mesmo nos casos que rodaram QA.

---

## 4. Por que é heterogêneo

Existem hoje dois caminhos, e o que decide qual deles a peça percorre não é regra nenhuma — é se alguém escreveu um script à mão para aquele caso.

**Caminho padrão:** roda em todo caso, automático, produz DOCX de texto e tabelas simples, nunca chama o compositor. É o que 100% das entregas dos últimos vinte dias percorreram.

**Caminho visual:** não é automático. Exige que alguém crie o `compor_<caso>_mapa.py`, o execute manualmente e arquive o resultado. Foi percorrido por cinco casos, todos em 9 e 10 de julho.

A inconstância não é variação de qualidade dentro de um processo. São dois processos diferentes, e o gatilho entre eles é discricionário e humano. Por isso a variância é tão brutal: não há meio-termo entre uma peça com cinco diagramas e uma peça com zero. Ou alguém escreveu o mapa, ou não escreveu.

Isso também explica por que o problema não deu sinal. A capacidade técnica nunca faltou — os cinco modelos provam que a máquina sabe produzir excelência. O que faltou foi a excelência ser o caminho de menor resistência em vez do caminho que exige trabalho extra.

---

## 5. Assinatura visual da FORJA

Por determinação de 30/07/2026, os elementos abaixo são **obrigatórios em todo artefato que sai da esteira**. Não há nível dispensado, não há waiver, não há modo rápido. O tipo de artefato muda a **forma** que o elemento assume, nunca autoriza sua ausência.

Onde um elemento for genuinamente inaplicável, a regra está escrita nesta tabela e é verificada por código. Não fica a critério de quem produz.

| # | Elemento | Como o código prova a presença | Peça protocolável | Memorial/parecer | Produto interno |
|---|---|---|---|---|---|
| 1 | Template e timbre institucional | cabeçalho com imagem na 1ª página; origem no `TEMPLATE_MEDINA_OSORIO_PETICAO.docx` | timbre completo + rodapé | timbre completo + rodapé | timbre simplificado |
| 2 | Síntese executiva em tabela na abertura | 1ª tabela do documento, antes do corpo, com cabeçalho sombreado | modelo art. 343-A do RISTJ | síntese de recomendações | síntese de achados |
| 3 | Elemento gráfico vetorial | contagem de EMF/WMF embutidos | ≥ 2 (tese + cronologia) | ≥ 1 | ≥ 1 |
| 4 | Caixa de destaque | parágrafo com borda e preenchimento | precedente estruturante | norma ou risco central | achado crítico |
| 5 | Pull quote | bloco recuado com fonte diferenciada | ≥ 2 | ≥ 1 | ≥ 1 |
| 6 | Quadro comparativo ou zebrado | tabela com alternância de preenchimento | quando há comparação | quando há comparação | quando há comparação |
| 7 | Negrito estratégico | razão de runs em negrito sobre o total | 25%–35% | 20%–30% | 20%–30% |
| 8 | Hierarquia tipográfica | níveis de título distintos presentes | ≥ 2 níveis | ≥ 2 níveis | ≥ 2 níveis |
| 9 | Paleta institucional | presença de `#395C60` e `#D9926A` | ambas | ambas | ambas |
| 10 | Fólio e rodapé | shape de fólio nas páginas seguintes | obrigatório | obrigatório | obrigatório |

**O que "simplificado" significa.** Onde a tabela diz *simplificado*, trata-se de escala reduzida do mesmo elemento — logo menor, rodapé em corpo menor —, **nunca ausência**. Não existe artefato sem timbre, sem síntese de abertura ou sem elemento gráfico. Estas são as únicas variações de forma pré-aprovadas: escala do timbre (item 1) e quantidade mínima de elementos gráficos e pull quotes entre dois e um (itens 3 e 5). Nenhuma outra variação é admitida sem nova determinação escrita.

**Quando o item 6 é exigido.** É o único condicional, e a condição é programática, não interpretativa: o quadro comparativo passa a ser obrigatório quando o markdown auditado já contém tabela comparando dois ou mais elementos — precedentes, teses, marcos temporais, premissas. Comparação feita em prosa corrida não aciona o item. A existência do quadro é binária; a qualidade dele entra no índice da seção 8.

**Quem classifica o tipo do artefato.** Esta é a brecha mais óbvia de um padrão diferenciado por tipo: se quem produz classifica, todo artefato difícil vira "produto interno". A classificação é automática e derivada do conteúdo — peça protocolável quando há endereçamento a órgão julgador e número de processo; memorial ou parecer quando há destinatário identificado sem endereçamento judicial; produto interno apenas quando marcado explicitamente na abertura do caso. **Tipo não identificado é erro de entrada e bloqueia o artefato**, nunca cai no perfil mais permissivo por omissão.

**Regra de ouro preservada:** elemento que não reduz esforço cognitivo do leitor sai da peça. Ela não autoriza ausência do mínimo; ela governa o que se acrescenta **acima** do mínimo, e é a base da defesa anti-gaming da seção 8.

---

## 6. Plano de correção

A ordem das ondas é deliberada e não pode ser invertida. Exigência sem capacidade não produz qualidade, produz travamento: se o gate fechar antes de o compositor rodar sozinho, nenhuma peça sai e a fábrica para.

### Onda 1A — Gerar o mapa visual automaticamente

**Por que primeiro:** enquanto o mapa depender de mão humana, tudo o mais é decorativo.

**Onde:** novo módulo `_FORJA_HARNESS\forja_visual_mapa_gen.py`, acionado quando o caso não tem `mapa.json`.

**O que faz:** lê o markdown auditado e deriva o mapa por heurística estrutural — a abertura vira linha de síntese; parágrafos que citam precedente com identificador de julgado viram candidatos a pull quote; blocos de conclusão viram caixa; tabelas comparativas existentes viram quadro. Grava `mapa.json` na pasta do caso.

**Restrição técnica que o código impõe:** `compor()` valida cada âncora do mapa contra o texto (`_Mapa._valida`) e aborta se a âncora não existir literalmente no markdown. O gerador precisa emitir substrings exatas, não paráfrases. Isso é uma vantagem — torna o mapa gerado verificável — mas exige cuidado com normalização.

**Calibração:** os cinco mapas manuais existentes são o conjunto de referência, e a cobertura é medida de forma operacional, não impressionista: para cada categoria (pulls, caixas, linhas de síntese), a fração de âncoras do mapa manual que o gerador também selecionou, por correspondência exata de substring. A cobertura reportada é a **menor** entre as categorias, não a média — média esconde categoria zerada.

**Critério de pronto:** todos os dez elementos obrigatórios da seção 5 contemplados no mapa gerado em 100% dos casos de teste; aderência às escolhas dos mapas de referência de ao menos 70% por categoria; `compor()` aceita todos os mapas sem abortar por âncora inválida.

Os dois números são coisas diferentes e não devem ser confundidos: **os dez elementos são piso e admitem 100%, só isso**; os 70% medem quanto o gosto do gerador se aproxima do gosto humano na escolha de *quais* trechos merecem destaque, e aí 70% é bom começo.

**Esforço revisado:** 12 a 14 horas.

### Onda 1B — Gerar os diagramas

**Este é o verdadeiro caminho crítico do plano, e a estimativa anterior o subestimava.**

`medina_svg_kit.py` tem 152 linhas e oferece apenas primitivas de desenho: bloco de texto, seta, caixa, cartões ancorados e a rotina de salvar com gate de legibilidade. Não existe gerador de cronologia processual, de diagrama de tese ou de matriz comparativa. E `compor()` apenas posiciona o marcador `{{FIG}}` e a legenda — **o desenho precisa chegar pronto**. Ou seja: gerar o mapa não gera o diagrama. Sem esta onda, o item 3 do padrão continua dependendo de mão humana, e a inconstância volta pela mesma porta por onde saiu.

**Onde:** extensão de `_FERRAMENTAS\medina_svg_kit.py` com três geradores compostos sobre as primitivas existentes.

**Os três:** cronologia processual, montada a partir das datas e atos que o markdown já cita em ordem; encadeamento da tese, montado a partir da estrutura de premissas e conclusão; matriz comparativa, montada a partir de tabela comparativa já presente no texto. Todos passam pelo gate de legibilidade e pelo gate de overflow que o kit já implementa.

**Critério de pronto:** os três geradores produzem SVG legível para os cinco casos de referência; nenhum texto abaixo do mínimo impresso; nenhum estouro de viewBox; conversão para EMF e inserção no Word sem degradação.

**Esforço:** 8 a 12 horas.

**Se esta onda escorregar**, o efeito é claro e deve ser dito agora: o item 3 do padrão fica dependente de trabalho manual e o gate da Onda 3 não pode ser ligado. Não há atalho aqui — é construir o gerador ou aceitar que a constância continua dependendo de atenção humana.

### Onda 2 — Tornar o visual o caminho padrão

**Onde:** `forja_render_docx.py`, função `render()`.

**O que faz:** ao final do render, carrega o `mapa.json` — gerando-o pela Onda 1 se não existir — e chama `compor()`. Grava `FIDELIDADE_VISUAL.json` com o SHA-256 do DOCX resultante, que é o lastro que o gate da Onda 3 vai conferir. O mapa escrito à mão deixa de ser pré-requisito e passa a ser refinamento opcional que sobrescreve o automático.

**Ponto de atenção conferido no código:** a composição extrai fragmentos do texto para virar pull quote e caixa, e o gate de fidelidade compara o texto do DOCX com o do markdown. Fragmento não é parágrafo inteiro, e a normalização precisa garantir que todo fragmento extraído continue sendo substring do parágrafo de origem — caso contrário o gate acusa divergência onde não há. Isso precisa ser testado sobre os cinco casos de referência **antes** de a composição virar padrão. Composição visual não pode alterar uma palavra do texto auditado; a regra é inegociável e o teste é a prova.

**Critério de pronto:** cinco casos processados de ponta a ponta produzem DOCX com todos os dez elementos da seção 5; fidelidade textual de 100% contra o markdown auditado; zero falso positivo do gate de fidelidade; nenhum caso exige intervenção manual.

**Esforço revisado:** 5 a 7 horas.

### Onda 3 — Ponto único de estrangulamento e gate bloqueante

**Por que só agora:** a partir daqui, o que não atende ao padrão não sai. Isso só é seguro depois que o padrão é atingido automaticamente.

**Onde, corrigido pelo red team:** a verificação nasce em `forja_render_docx.py`, **no ponto em que o DOCX é finalizado**, e não no fechamento F10. O motivo é que o F10 é justamente a rota que quase ninguém percorre — instalar o gate ali repetiria o erro atual. Quem produz o arquivo é quem o valida; as rotas seguintes (`forja_package.py`, `forja_delivery.py`, arquivamento em `gestao_escritorio\entregas_fabio_osorio`) passam a exigir o lastro `FIDELIDADE_VISUAL.json` com SHA-256 conferido, mecanismo que `visual_com_lastro()` já implementa e que basta antecipar.

Assim um DOCX sem conformidade não chega a existir em disco em estado entregável, e nenhuma rota posterior precisa ser confiável para o sistema ser seguro.

**O que faz:** confere os dez elementos da seção 5 sobre o DOCX final e devolve conformidade binária. Não conforme, não empacota e não entrega. Sem `gate_waiver`, sem flag de emergência, sem exceção para produto interno. O que hoje é advisory no QA passa a ter contraparte afirmativa: além de procurar defeito, procura ausência.

**Fechamento das rotas:** hoje há saídas que não passam pelo F10. A Onda 3 as reconduz todas ao mesmo ponto. Uma varredura de chamadas confirma que não sobrou caminho lateral.

**Condição de ativação, explícita:** o gate só é ligado depois que **cinco casos reais de tipos diferentes** — ao menos uma peça protocolável, um memorial ou parecer e um produto interno — tiverem sido processados de ponta a ponta pelas Ondas 1 e 2 com conformidade integral nos dez elementos, e depois de você conferir esses cinco com os próprios olhos. Antes disso, a verificação roda em modo observação, registrando o que reprovaria sem bloquear nada.

**Critério de pronto:** as cinco peças-modelo históricas passam sem falso positivo; um documento de texto corrido é reprovado com mensagem que nomeia o elemento faltante e o comando que o gera; uma varredura de chamadas confirma que nenhuma rota de arquivamento alcança o disco sem o lastro.

**Esforço revisado:** 5 a 6 horas, mais o levantamento das rotas.

### Onda 4 — Invocação mecânica da skill

A skill visual é hoje invocada por lembrança do agente, o que é a mesma fragilidade do mapa manual num outro andar. A fase de produção passa a carregá-la pelo contrato de fase, não pelo texto do prompt.

**Esforço:** 2 a 3 horas.

### Total revisado

| Onda | Conteúdo | Esforço |
|---|---|---|
| 1A | Gerador de mapa visual | 12–14 h |
| 1B | Geradores de diagrama (caminho crítico) | 8–12 h |
| 2 | Composição por padrão no render | 5–7 h |
| 3 | Ponto único e gate bloqueante | 5–6 h |
| 4 | Invocação mecânica da skill | 2–3 h |
| | **Total** | **32–42 h** |

São cerca de cinco a seis dias úteis, e não os três a quatro da primeira estimativa. A revisão de engenharia mostrou que a estimativa original tratava geração de mapa e geração de diagrama como a mesma tarefa, quando são duas — e a segunda é a mais pesada. A fábrica opera normalmente durante todas as ondas; só a Onda 3 muda o comportamento de saída, e ela é a última.

### Escopo temporal da determinação

A exigência vale para todo artefato produzido **a partir da conclusão da Onda 2**. As peças já entregues não são regeneradas automaticamente: isso é decisão sua, com custo próprio, e está fora deste plano. Registro para não haver expectativa frustrada — o plano recupera o padrão daqui para frente, não corrige o passado.

### Custo de tempo por peça

A composição visual acrescenta tempo de processamento a cada render, e o volume atual da fábrica torna isso relevante. O número não foi medido e não vou estimá-lo no escuro: **a medição do tempo adicional por peça entra como critério de pronto da Onda 2**, com o resultado comparado ao ciclo atual. Se o acréscimo comprometer prazo em caso urgente, a resposta é otimizar a composição, nunca dispensá-la.

---

## 7. Loop de engenharia

O loop precisa distinguir duas coisas que, se misturadas, viram exatamente o atalho que a determinação de hoje proíbe.

### O piso é binário e não entra em loop

Os dez elementos da seção 5 são condição de saída, não meta de convergência. Não há iteração que autorize entrega abaixo deles, não há prazo que os dispense, não há waiver.

Quando o piso não é atingido, a ordem de tentativa é: **correção automática** (o gate nomeia o elemento faltante e dispara o gerador de mapa para produzi-lo) e, se ainda faltar, **correção humana dirigida** (o diagnóstico entrega o elemento, a página e o comando). Se nem assim o piso for atingido, **o artefato não sai** e o caso vira pendência nomeada com o motivo. Nunca entrega degradada, nunca entrega silenciosa.

Na prática, a correção automática deve resolver a quase totalidade dos casos depois da Onda 2 — é para isso que ela existe.

**A verificação do piso vem antes do loop e não consome iteração dele.** O artefato é composto, o piso é conferido, e só então ele entra — ou não — no refino. Artefato que falha no piso vai direto para diagnóstico, sem gastar iteração de excelência. Isso evita o efeito perverso de a peça queimar as duas iterações disponíveis tentando melhorar o que ainda nem atingiu o mínimo.

### A excelência acima do piso entra em loop, com teto

Acima do piso há espaço de refinamento: qualidade do diagrama, escolha do que merece pull quote, distribuição do negrito. Aqui vale medir, comparar com a banda, corrigir e remedir — e aqui vale a regra de parada, porque é aqui que o perfeccionismo trava produção.

**Teto: duas iterações por peça.** Se o índice da seção 8 estiver dentro da banda, para. Se estiver fora da banda depois de duas iterações e o piso estiver cumprido, a peça sai assim mesmo e o desvio vira dado para calibrar o gerador — não motivo para segurar a entrega.

**No nível da fábrica:** revisão semanal dos indicadores; um quesito que fique dentro da banda por duas semanas seguidas sai do ciclo ativo e passa a monitoramento reativo.

A assimetria é o ponto central: o piso nunca cede, a excelência sempre tem teto de esforço.

---

## 8. Indicadores

São quatro, e cada um responde a uma pergunta diferente. Nenhum deles substitui o outro.

### Conformidade — binária

Percentual dos dez elementos obrigatórios presentes. **Alvo: 100%. Não é média, é condição.** Uma peça não compra a ausência de um elemento obrigatório com pontuação alta nos outros. Este indicador não se combina com nenhum outro e não é ponderado.

### Cobertura — a pergunta que ninguém estava fazendo

Percentual de artefatos entregues que passaram pelo gate visual. **Alvo: 100%.**

Este é o indicador que teria pegado o problema em 11 de julho. Hoje ele valeria em torno de 10% no acervo histórico e 0% nos últimos vinte dias. Qualquer valor abaixo de 100% é incidente a ser investigado, nunca estatística a ser reportada.

### IRV — Índice de Riqueza Visual, que mede excelência acima do piso

```
IRV = 0,30·D + 0,20·S + 0,20·P + 0,20·N + 0,10·C

D = densidade de elementos vetoriais, normalizada pela extensão do documento
S = qualidade estrutural da síntese de abertura (existe, é tabela, cobre pedido/fundamento/pergunta)
P = destaques estratégicos (pull quotes e caixas) por extensão
N = aderência do negrito à banda do tipo (1,0 no centro da banda, decaindo para as pontas)
C = presença e correção da paleta institucional
```

Bandas-alvo: peça protocolável **0,70 a 0,85**; memorial ou parecer **0,65 a 0,80**; produto interno **0,55 a 0,75**.

As bandas têm teto por desenho. Um IRV de 0,95 não é motivo de comemoração — é sinal de excesso de ornamento, e aciona a revisão da seção anti-gaming.

O componente N merece nota. Ele pune tanto a falta quanto o excesso, porque a medição mostrou documentos recentes com 88% e 100% de negrito. Negrito universal é ausência de ênfase, e o indicador precisa enxergar isso como defeito, não como riqueza.

**Uma objeção que rejeitei.** A revisão de engenharia propôs remover o negrito da lista de elementos obrigatórios, alegando detecção frágil porque muitos documentos recentes reprovariam. Isso confunde duas coisas: o documento com 100% de negrito não é falso positivo do gate — é o gate funcionando. A razão de negrito é das medidas mais confiáveis que existem num DOCX, contável run a run. O que aceito é refinar a base de cálculo, medindo sobre o corpo do texto e excluindo títulos, cabeçalhos de tabela e o próprio conteúdo das caixas de destaque, onde o negrito é estrutural e não ênfase. Com essa base, a banda de 25% a 35% é justa e a detecção é sólida.

### CVV — Coeficiente de Variação Visual, que mede constância

```
CVV = desvio padrão do IRV / média do IRV, entre artefatos do mesmo tipo no período
```

**Alvo: até 15%.** Acima de 25%, alarme.

Este é o indicador que responde ao que você descreveu, porque o que você percebeu foi variância antes de ser média. Uma fábrica com IRV médio de 0,72 e CVV de 40% entrega uma peça excelente e uma pobre alternadamente — e é essa alternância que quebra a confiança no sistema.

### Defesa anti-gaming

Quatro travas para a esteira não encher a peça de diagrama inútil só para bater métrica:

1. **Bandas com teto.** IRV acima da banda é desvio, não conquista.
2. **Normalização por extensão.** Diagrama contado por densidade, não por soma absoluta; empilhar figuras num documento curto derruba os outros componentes em vez de subir o índice.
3. **Amostra humana quinzenal.** Uma peça de cada tipo revisada pelo Fábio ou por auditor designado, com cada elemento marcado como útil, neutro ou prejudicial. Elemento reprovado duas vezes sai do repertório do gerador.
4. **Procedência registrada.** Cada elemento carrega no metadado se veio do mapa automático, do mapa manual ou de refinamento posterior, para distinguir crescimento genuíno de inflação.

A regra de ouro segue valendo por cima de tudo: elemento que não reduz esforço cognitivo do leitor sai da peça.

### Quando o gerador é recalibrado

Indicador sem gatilho de ação vira relatório decorativo. A revisão semanal dispara recalibração do gerador de mapa e dos geradores de diagrama quando qualquer uma destas condições ocorrer: o IRV médio do tipo sai da banda; o CVV ultrapassa 25%; ou um elemento é reprovado duas vezes na amostra humana quinzenal.

A recalibração ajusta heurística e pesos e revalida sobre os dez casos de teste. Ela **não** suspende o gate nem afrouxa o piso enquanto acontece — a fábrica continua entregando conforme o padrão, e o que se calibra é o gosto do gerador, não o mínimo exigido.

---

## 9. O que não fazer

**Fechar o gate antes da Onda 2.** Pararia a fábrica sem melhorar nenhuma peça. O gate é a última onda por necessidade, não por prudência excessiva.

**Waiver, flag de emergência ou modo rápido.** Vedado pela determinação de 30/07/2026. Nenhum prazo justifica saída abaixo do padrão; o que existe é pendência nomeada.

**Dispensar produto interno.** A versão anterior deste documento propunha isso e foi corrigida. Relatório interno tem o mesmo piso; o que muda é a forma dos elementos, não a existência deles.

**Geração de diagrama por modelo livre, sem mapa declarativo.** Já tentado; a taxa de ilegibilidade torna a revisão mais cara que a geração. O mapa declarativo mantém o agente decidindo o quê e o sistema decidindo o como.

**Modelo como juiz da qualidade visual.** Julgar se um diagrama reduz esforço cognitivo é subjetivo demais para automatizar. A amostra humana quinzenal é mais barata e mais confiável.

**Reabrir visualização 3D.** Eliminada pelo Igor em 12/07/2026 e fora do escopo.

---

## 10. Primeiro passo

Uma autorização só:

> **Executar as Ondas 1A, 1B e 2** — gerador de mapa visual, geradores de diagrama e composição por padrão no render — mantendo a fábrica operando normalmente, e voltar com cinco peças reais de tipos diferentes, compostas automaticamente, para a sua conferência visual antes de ligar o gate bloqueante da Onda 3.

Isso separa o risco. As três primeiras ondas não podem quebrar nada: no pior caso o resultado é o que já se tem hoje. A Onda 3, que é a que efetivamente impede peça pobre de sair, só entra depois que você olhar com os próprios olhos e confirmar que o automático atingiu o padrão que você aprovou em julho.

São cerca de 25 a 33 horas até esse ponto de conferência. A Onda 1B — construir os geradores de diagrama — é o trecho mais incerto, porque hoje só existem primitivas de desenho, e é onde o cronograma pode escorregar. Prefiro dizer isso agora a descobrir na entrega.

Tudo o que a execução precisa já existe: `forja_visual.py` implementado e testado, `medina_visual_kit.py` e `medina_svg_kit.py` em `_FERRAMENTAS`, o template com o timbre vetorial, e cinco mapas manuais servindo de referência de calibração.

---

## Apêndice — procedência das afirmações

**Conferido diretamente nesta sessão:** contagem e datas dos arquivos `*VISUAL_LAW*.docx`; os cinco `compor_*_mapa.py`; os três `F10_TRILHA_EVIDENCIA.md`; ausência de import de `forja_visual` em código de produção; `forja_visual.py` com 469 linhas e `compor()` na linha 115; `forja_render_docx.py:31` importando apenas `forja_visual_review`; `forja_delivery.py:185` (`visual_com_lastro`), `:268` (elo 4-B) e `:476` (`SystemExit(2)`); versão de 11/07 de `forja_render_docx.py` já sem integração visual, o que derruba a hipótese de regressão pelo commit `ef2fcf98`.

**Medição automatizada, direção consistente mas valores por documento não reconferidos:** a tabela da seção 2.2 e os percentuais dela derivados.

**[Não verificado] e por isso fora do corpo do diagnóstico:** a alegação de que nos casos CASO-19 e CASO-07 uma versão visual completa teria sido gerada e uma versão simples entregue em seu lugar, com divergência de hash. A investigação levantou a hipótese, mas ela não foi confirmada arquivo a arquivo. Se confirmada, acrescenta uma quinta causa — descarte deliberado da versão visual — que a Onda 3 já cobriria, pois o gate confere o SHA do arquivo efetivamente entregue.

**Revisão cruzada entre famílias de modelo (30/07/2026):** o documento passou por duas revisões independentes conduzidas pelo Claude Fable 5 — uma editorial e estratégica, outra de red team de engenharia com leitura do código. Foram incorporadas: a correção da média de elementos vetoriais; a definição de que *simplificado* é escala reduzida e nunca ausência; o gate de classificação automática do tipo de artefato; a definição programática do item 6; a separação da antiga Onda 1 em geração de mapa e geração de diagrama; a métrica operacional de cobertura; o teste de fidelidade textual sobre fragmentos; a instalação do gate no render em vez do F10; a condição de cinco casos conformes antes da ativação; o escopo temporal prospectivo; o gatilho de recalibração; e a revisão das estimativas de 20–25 para 32–42 horas.

Foi rejeitada, com motivo registrado, a proposta de remover o negrito estratégico da lista de obrigatórios por suposta fragilidade de detecção: documento com 100% de negrito reprovando é o gate funcionando, não falso positivo. Aceitou-se apenas o refino da base de cálculo. Também foram descartadas as estimativas numéricas de tempo de processamento por peça, que não tinham medição por trás; no lugar, a medição virou critério de pronto da Onda 2.

**Conferido diretamente após as revisões:** `medina_svg_kit.py` tem 152 linhas e apenas primitivas (`tblock`, `seta`, `caixa`, `cards_ancora`, `salvar`), sem gerador de cronologia, tese ou matriz; `compor()` posiciona somente o marcador e a legenda, exigindo o SVG pronto; `_Mapa._valida` aborta quando a âncora não existe literalmente no markdown.

**Histórico do repositório:** o backup privado começa em 11/07/2026, de modo que não há histórico versionado da janela de 8 a 10 de julho. A datação dessa janela vem dos carimbos de data dos artefatos, não de commits.
