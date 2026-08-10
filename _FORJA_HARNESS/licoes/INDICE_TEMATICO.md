# Lições da FORJA — índice temático

> **Documento gerado.** Não edite aqui: a fonte é `RETROSPECTIVAS.md` e este arquivo é reescrito por `python forja_licoes.py --documentar`.


382 lições em 16 temas. Uma lição aparece em mais de um tema quando trata de mais de uma coisa (média de 1.5 por lição), então a soma das seções é maior que o total.


O tema sai do texto da própria lição, por vocabulário declarado em `forja_licoes.py`. O termo no título vale sozinho; no corpo, a lição curta precisa de uma ocorrência e a longa de duas, uma delas na abertura — sem isso, um registro denso de rodada cai em seis temas por mencionar seis assuntos uma vez cada.


É um mapa de navegação, não uma autoridade: leia a lição antes de citá-la. O tema diz onde procurar, não o que a lição decide.


## Sumário

| tema | lições |
|---|---:|
| [Gates: o que reprova e o que só parece reprovar](#gate) | 126 |
| [Lastro: afirmação conferida na fonte](#lastro) | 41 |
| [Citação, jurisprudência e dispositivo](#citacao) | 36 |
| [Redação, estilo e cara de IA](#redacao) | 24 |
| [Visual law: figura, diagrama e diagramação](#visual) | 42 |
| [Modelos, famílias e revisão cruzada](#modelos) | 24 |
| [Identidade processual e peça](#processual) | 11 |
| [Entrega ao destinatário e comunicação](#entrega) | 36 |
| [Retorno humano e aprendizado da casa](#aprendizado) | 2 |
| [Acoplamento: onde o código de fato passa](#acoplamento) | 7 |
| [Estado, artefatos e contratos de fase](#estado) | 44 |
| [Fronteira, sigilo e proveniência](#fronteira) | 15 |
| [Automação, agendamento e volume](#automacao) | 11 |
| [Prova, atestado e o que conta como evidência](#evidencia) | 37 |
| [Autoengano e autovalidação](#autoengano) | 14 |
| [Sem tema atribuído pelo vocabulário](#sem-tema) | 107 |

<a id="gate"></a>
## Gates: o que reprova e o que só parece reprovar

126 lições.

| nº | data | lição | onde | o que a faz reprovar |
|---:|---|---|---|---|
| 29 | 09/07/2026 | As lições viram código, não só prosa | [L77](../RETROSPECTIVAS.md#L77) | — |
| 34 | 09/07/2026 | Conferir o achado do auditor antes de corrigir | [L91](../RETROSPECTIVAS.md#L91) | — |
| 35 | 09/07/2026 | Circuito de gate só existe quando a etapa final é obrigada a consumi-lo | [L95](../RETROSPECTIVAS.md#L95) | — |
| 36 | 09/07/2026 | Auditoria cruzada entre IAs funciona e é barata | [L97](../RETROSPECTIVAS.md#L97) | — |
| 38 | 09/07/2026 | QA visual página a página continua achando o que nenhum gate pega | [L103](../RETROSPECTIVAS.md#L103) | — |
| 46 | 10/07/2026 | Metadado herdado de template é falha SISTÊMICA, não pontual: as 11 peças N3 saíram com autor "thais mulati" e título "Proposta de Serviços e Honorários" (DOCX E PDF) | [L127](../RETROSPECTIVAS.md#L127) | — |
| 48 | 10/07/2026 | Reconciliação painel×disco pegou o risco operacional mais grave da rodada: a versão ENVIADA ao Fábio (03:42) era anterior à N3 e ainda continha o pedido de honorários recursais removido por erro jurídico; a N3 corrigida não foi enviada | [L131](../RETROSPECTIVAS.md#L131) | forja_anonimizar.py, forja_delivery.py, forja_visual.py |
| 61 | 11/07/2026 | Gate bloqueante sem lastro persistido é gate que já passou uma versão errada | [L161](../RETROSPECTIVAS.md#L161) | — |
| 66 | 11/07/2026 | Avaliar a petição exige medir resultados diretos e testar explicações rivais | [L173](../RETROSPECTIVAS.md#L173) | — |
| 71 | 12/07/2026 | Gate de validação contra dados reais ANTES de codificar o motor paga em minutos o que custaria horas | [L187](../RETROSPECTIVAS.md#L187) | — |
| 80 | 15/07/2026 | Review externo produz hipóteses; regressão e execução real decidem | [L209](../RETROSPECTIVAS.md#L209) | — |
| 1 | 23/07/2026 | Plano bom nasce reprovado | [L221](../RETROSPECTIVAS.md#L221) | ⚠ citada, mas o número é ambíguo |
| 5 | 23/07/2026 | Limitação que permanece (decisão de gasto do Igor): | [L329](../RETROSPECTIVAS.md#L329) | — |
| 86 | 26/07/2026 | Citar o localizador não é ter lido o localizador | [L338](../RETROSPECTIVAS.md#L338) | — |
| 88 | 26/07/2026 | Punir pendência declarada com a pena da invenção ensina o sistema a esconder lacuna | [L342](../RETROSPECTIVAS.md#L342) | — |
| 89 | 26/07/2026 | Auditor que reprova o acerto é desligado na terceira vez | [L344](../RETROSPECTIVAS.md#L344) | ⚠ citada, mas o número é ambíguo |
| 90 | 26/07/2026 | Importável não é acoplado | [L346](../RETROSPECTIVAS.md#L346) | — |
| 97 | 27/07/2026 | O auditor errou três vezes no mesmo dia, sempre reprovando o acerto | [L364](../RETROSPECTIVAS.md#L364) | — |
| 88 | 03/08/2026 | Gate que só procura defeito nunca detecta pobreza | [L372](../RETROSPECTIVAS.md#L372) | — |
| 89 | 03/08/2026 | O gate na rota que ninguém percorre é gate nenhum | [L374](../RETROSPECTIVAS.md#L374) | ⚠ citada, mas o número é ambíguo |
| 92 | 03/08/2026 | O teste de mutação é o único que prova que o gate funciona | [L380](../RETROSPECTIVAS.md#L380) | — |
| 96 | 03/08/2026 | O padrão-ouro tinha defeito, e o gate não podia vê-lo | [L388](../RETROSPECTIVAS.md#L388) | ⚠ citada, mas o número é ambíguo |
| 98 | 03/08/2026 | O defeito que "só o zoom pega" estava legível no XML o tempo todo | [L392](../RETROSPECTIVAS.md#L392) | — |
| 100 | 03/08/2026 | Gate declarado não é gate computado; a casa escreveu a proteção certa e a deixou fora da estrada | [L396](../RETROSPECTIVAS.md#L396) | — |
| 101 | 03/08/2026 | "Rota única" é hipótese a medir, não intuição de arquiteto | [L398](../RETROSPECTIVAS.md#L398) | — |
| 102 | 03/08/2026 | Medir a especificação contra o acervo pega o defeito antes de existir código; persistir a medição é o que a torna evidência | [L400](../RETROSPECTIVAS.md#L400) | — |
| 107 | 03/08/2026 | Fonte prevalente e valor monetário precisam ser gates de produção, não campos de confiança | [L424](../RETROSPECTIVAS.md#L424) | — |
| 108 | 03/08/2026 | Gate computado sobre conjunto vazio é pior que gate declarado, porque parece trabalho feito | [L426](../RETROSPECTIVAS.md#L426) | — |
| 109 | 03/08/2026 | Hash de fonte grande também precisa de lastro de execução | [L436](../RETROSPECTIVAS.md#L436) | — |
| 110 | 03/08/2026 | Baseline longo não substitui a régua curta | [L438](../RETROSPECTIVAS.md#L438) | — |
| 114 | 03/08/2026 | O gate que nunca rodou é indistinguível do gate que aprovou | [L446](../RETROSPECTIVAS.md#L446) | — |
| 115 | 03/08/2026 | Duas sessões no mesmo arquivo batizam o mesmo gate com dois nomes | [L448](../RETROSPECTIVAS.md#L448) | — |
| 121 | 03/08/2026 | Parâmetro de conveniência não pode virar bypass de gate | [L460](../RETROSPECTIVAS.md#L460) | — |
| 124 | 03/08/2026 | Anti-overblocking precisa de contraprova na rota, não só no detector | [L466](../RETROSPECTIVAS.md#L466) | ⚠ citada, mas o número é ambíguo |
| 116 | 03/08/2026 | A esteira nunca soube quantos dos seus gates ela mesma computa | [L472](../RETROSPECTIVAS.md#L472) | — |
| 117 | 03/08/2026 | Quase publiquei o número errado por confundir ausência de código com ausência de execução | [L474](../RETROSPECTIVAS.md#L474) | — |
| 118 | 03/08/2026 | O contrato do F8 tinha 14 exigências que ninguém sabia cumprir, e o cumpridor estava do lado, calado | [L476](../RETROSPECTIVAS.md#L476) | — |
| 119 | 03/08/2026 | A métrica moveu a favor de quem a escreveu, no mesmo dia em que nasceu | [L478](../RETROSPECTIVAS.md#L478) | — |
| 127 | 03/08/2026 | Gate declarado na F10 precisa ser recomputado no evento que encerra o caso | [L480](../RETROSPECTIVAS.md#L480) | — |
| 120 | 03/08/2026 | O conselho obrigatório era atestado por quem tinha interesse em passar | [L482](../RETROSPECTIVAS.md#L482) | — |
| 121 | 03/08/2026 | Piso de tamanho é o antídoto barato contra o arquivo criado para o gate | [L484](../RETROSPECTIVAS.md#L484) | — |
| 122 | 03/08/2026 | O gate mais caro da esteira era o mais confiado | [L488](../RETROSPECTIVAS.md#L488) | — |
| 123 | 03/08/2026 | Quase criei a MC-15 dentro do gate feito para evitá-la | [L490](../RETROSPECTIVAS.md#L490) | — |
| 124 | 03/08/2026 | O gate de identidade nasceu cobrando tribunal de artigo do CPC | [L492](../RETROSPECTIVAS.md#L492) | ⚠ citada, mas o número é ambíguo |
| 125 | 03/08/2026 | A métrica contava comentário como implementação | [L494](../RETROSPECTIVAS.md#L494) | — |
| 126 | 03/08/2026 | O mesmo artefato existe em sete formatos, e cada gate novo tropeça nisso | [L496](../RETROSPECTIVAS.md#L496) | — |
| 127 | 03/08/2026 | Resumo com contagens zeradas é varredura limpa, não detecção | [L498](../RETROSPECTIVAS.md#L498) | — |
| 128 | 03/08/2026 | Um ledger real tinha dez fontes oficiais e nenhuma arquivada, e o gate chamado `official_sources_archived` dizia `pass` | [L500](../RETROSPECTIVAS.md#L500) | — |
| 129 | 03/08/2026 | Três quartos das execuções de um gate mediam o conjunto vazio | [L502](../RETROSPECTIVAS.md#L502) | — |
| 132 | 03/08/2026 | Grep não prova emissão, e foi grep que escondeu dois gates sem produtor | [L508](../RETROSPECTIVAS.md#L508) | — |
| 134 | 03/08/2026 | O validador da exploração existia e rodava; os gates que o atestam eram escritos à mão | [L512](../RETROSPECTIVAS.md#L512) | — |
| 136 | 03/08/2026 | Ausência de declaração não é declaração falsa, e a diferença decide a severidade | [L516](../RETROSPECTIVAS.md#L516) | — |
| 138 | 03/08/2026 | A dívida de esquema ganhou um medidor antes de ganhar uma solução | [L520](../RETROSPECTIVAS.md#L520) | — |
| 141 | 03/08/2026 | O gate mais perigoso da esteira protege o único artefato que o destinatário lê | [L526](../RETROSPECTIVAS.md#L526) | — |
| 142 | 03/08/2026 | Rótulo genérico satisfaz "o campo existe" e não define nada | [L528](../RETROSPECTIVAS.md#L528) | — |
| 143 | 03/08/2026 | O blueprint mora em markdown, e o primeiro gate só sabia ler JSON | [L530](../RETROSPECTIVAS.md#L530) | — |
| 144 | 03/08/2026 | Cometi contra mim mesmo, no censo, o erro que já tinha documentado horas antes | [L532](../RETROSPECTIVAS.md#L532) | — |
| 145 | 03/08/2026 | A superfície de autovalidação chegou a zero, e é aí que começa o risco novo | [L534](../RETROSPECTIVAS.md#L534) | — |
| 147 | 03/08/2026 | O único jeito de saber se um gate sabe dizer não é destruir o artefato e olhar | [L538](../RETROSPECTIVAS.md#L538) | — |
| 149 | 03/08/2026 | Metade das reprovações do censo era do gate, não do caso | [L542](../RETROSPECTIVAS.md#L542) | — |
| 150 | 03/08/2026 | Gate que nunca aprova é tão quebrado quanto gate que nunca reprova | [L544](../RETROSPECTIVAS.md#L544) | — |
| 151 | 03/08/2026 | A dívida de esquema perigosa não é o nome do campo, é a FORMA do arquivo | [L546](../RETROSPECTIVAS.md#L546) | — |
| 153 | 03/08/2026 | O canário pegou a primeira regressão dele contra quem o escreveu, no mesmo dia | [L550](../RETROSPECTIVAS.md#L550) | — |
| 155 | 03/08/2026 | Os dezesseis gates da F8 nunca conheceram uma peça real, e isso incide sobre a decisão de ligá-los | [L554](../RETROSPECTIVAS.md#L554) | — |
| 156 | 03/08/2026 | "O censo não chama o produtor" era hipótese confortável; o material é que não existe | [L556](../RETROSPECTIVAS.md#L556) | — |
| 157 | 03/08/2026 | O gate visual reprovava o próprio template do escritório, e ninguém sabia | [L558](../RETROSPECTIVAS.md#L558) | — |
| 158 | 03/08/2026 | A síntese executiva obrigatória era lida como defeito tipográfico | [L560](../RETROSPECTIVAS.md#L560) | — |
| 159 | 03/08/2026 | Depois de tirar os falsos positivos, o gate achou o que existia para achar | [L562](../RETROSPECTIVAS.md#L562) | — |
| 160 | 03/08/2026 | Corrigir o produtor muda o censo; não se corrige o histórico para melhorar o número | [L564](../RETROSPECTIVAS.md#L564) | — |
| 162 | 03/08/2026 | Contraprova real e veredito de produção não são a mesma coisa | [L568](../RETROSPECTIVAS.md#L568) | — |
| 168 | 03/08/2026 | O gate do fólio tinha um teto que o acervo inteiro respeitava | [L583](../RETROSPECTIVAS.md#L583) | — |
| 170 | 03/08/2026 | Um canário que não alcança o que o gate lê mede a própria cobertura | [L587](../RETROSPECTIVAS.md#L587) | — |
| 171 | 03/08/2026 | Os cinco gates da F9 nunca tiveram material porque o leitor abria o nome errado | [L589](../RETROSPECTIVAS.md#L589) | — |
| 172 | 03/08/2026 | Catraca que ninguém testa também é atestado | [L591](../RETROSPECTIVAS.md#L591) | — |
| 177 | 03/08/2026 | Quatro vezes num dia o gate reprovou o padrão aprovado, e o motivo é estrutural | [L601](../RETROSPECTIVAS.md#L601) | — |
| 178 | 03/08/2026 | Quatro afrouxamentos seguidos e um verde perfeito no fim são indistinguíveis de um gate moldado | [L603](../RETROSPECTIVAS.md#L603) | — |
| 180 | 03/08/2026 | Contar arquivo no pacote não é contar figura na página, e a diferença cabe num comando de cópia | [L607](../RETROSPECTIVAS.md#L607) | — |
| 182 | 03/08/2026 | Constante declarada, documentada e elogiada em comentário, nunca consultada com valor real | [L611](../RETROSPECTIVAS.md#L611) | — |
| 183 | 03/08/2026 | A saída óbvia era estimar, e a medição a proibiu | [L613](../RETROSPECTIVAS.md#L613) | — |
| 184 | 03/08/2026 | O gate estrutural tem um limite que ainda precisa ser exercitado | [L615](../RETROSPECTIVAS.md#L615) | — |
| 185 | 03/08/2026 | Terceira aparição do mesmo padrão: o gate guarda a porta que ninguém atravessa | [L617](../RETROSPECTIVAS.md#L617) | — |
| 187 | 03/08/2026 | O defeito de adoção foi descoberto por acaso três vezes, então virou instrumento | [L621](../RETROSPECTIVAS.md#L621) | — |
| 188 | 03/08/2026 | o gate verde por cegueira, cometido por quem construía a defesa contra ele | [L623](../RETROSPECTIVAS.md#L623) | forja_lapidacao_governanca.py, test_forja_lapidacao_governanca.py |
| 189 | 03/08/2026 | classifiquei estudo interno como petição e inventei uma crise de qualidade | [L625](../RETROSPECTIVAS.md#L625) | — |
| 190 | 03/08/2026 | o gate de estilo estava certo, e testar contra o padrão aprovado é o que provou isso | [L627](../RETROSPECTIVAS.md#L627) | — |
| 194 | 03/08/2026 | resumo de memória que inverte o diagnóstico | [L635](../RETROSPECTIVAS.md#L635) | — |
| 195 | 03/08/2026 | ler o código prova presença; só executar prova comportamento | [L637](../RETROSPECTIVAS.md#L637) | — |
| 196 | 03/08/2026 | o gate que reprova o padrão aprovado está errado, e o erro costuma ser de conceito | [L639](../RETROSPECTIVAS.md#L639) | — |
| 197 | 03/08/2026 | a catraca que confunde rigor novo com cegueira | [L641](../RETROSPECTIVAS.md#L641) | — |
| 198 | 03/08/2026 | a serialização auxiliar não pode ser capaz de derrubar a checagem | [L643](../RETROSPECTIVAS.md#L643) | — |
| 199 | 03/08/2026 | a checagem cuja precondição está nas mãos de quem ela deveria conferir | [L645](../RETROSPECTIVAS.md#L645) | — |
| 204 | 03/08/2026 | antes de planejar a campanha, abra o arquivo que ela manda consultar | [L655](../RETROSPECTIVAS.md#L655) | — |
| 217 | 03/08/2026 | a lista escrita à mão não estava errada, estava irrelevante | [L681](../RETROSPECTIVAS.md#L681) | forja_fronteira.py |
| 219 | 03/08/2026 | o gate que detecta nome de cliente não pode carregar a lista de nomes | [L685](../RETROSPECTIVAS.md#L685) | — |
| 221 | 03/08/2026 | `lstrip("./")` não remove o prefixo `./`: remove qualquer ponto ou barra do começo | [L689](../RETROSPECTIVAS.md#L689) | — |
| 225 | 03/08/2026 | o gate protegia o nome completo, e a casa escreve pelo primeiro nome | [L697](../RETROSPECTIVAS.md#L697) | — |
| 226 | 03/08/2026 | duas maneiras de errar ao automatizar a decisão do que é nome e o que é palavra | [L699](../RETROSPECTIVAS.md#L699) | — |
| 230 | 03/08/2026 | a fidelidade textual deu 100% e o documento estava quebrado; nenhum gate viu, porque todos mediam presença e nenhum media forma | [L707](../RETROSPECTIVAS.md#L707) | forja_visual.py |
| 233 | 03/08/2026 | entre escrever o dado e descobrir o problema havia cinco horas | [L713](../RETROSPECTIVAS.md#L713) | — |
| 236 | 03/08/2026 | a correção escrita para tornar a falha visível abriu a via de vazamento que o gate existe para fechar | [L719](../RETROSPECTIVAS.md#L719) | — |
| 240 | 06/08/2026 | o gate de aprendizado que parece certo é o errado | [L807](../RETROSPECTIVAS.md#L807) | — |
| 244 | 06/08/2026 | contagem de blocos preservados pune peça curta; proporção de texto em comum, não | [L816](../RETROSPECTIVAS.md#L816) | — |
| 251 | 06/08/2026 | o erro não é o número errado, é o número certo do processo errado | [L869](../RETROSPECTIVAS.md#L869) | — |
| 252 | 06/08/2026 | o gate da fronteira apanhou a mim, de novo, e de novo estava certo | [L871](../RETROSPECTIVAS.md#L871) | — |
| 253 | 06/08/2026 | escrita direta em arquivo de registro falha quando a publicação lê a mesma árvore | [L873](../RETROSPECTIVAS.md#L873) | — |
| 256 | 06/08/2026 | o rótulo da caixa afirmava um precedente que o parágrafo não tinha | [L879](../RETROSPECTIVAS.md#L879) | — |
| 258 | 06/08/2026 | quase ensinei o gate a aprovar um artefato que o Word não abre | [L883](../RETROSPECTIVAS.md#L883) | — |
| 263 | 06/08/2026 | o gate mais curto aprovou a árvore que o gate longo reprovou | [L909](../RETROSPECTIVAS.md#L909) | — |
| 264 | 06/08/2026 | a catraca tipográfica virou trava sem saída, e isso é decisão de dono, não de código | [L911](../RETROSPECTIVAS.md#L911) | — |
| 267 | 06/08/2026 | tirar arquivo do escopo afrouxa a catraca duas vezes, e a segunda é invisível | [L917](../RETROSPECTIVAS.md#L917) | forja_triagem_rapida.py |
| 271 | 06/08/2026 | o defeito não nascia no documento, nascia em dez geradores | [L980](../RETROSPECTIVAS.md#L980) | — |
| 271 | 06/08/2026 | o gate certo não lê o texto, lê de onde ele veio | [L990](../RETROSPECTIVAS.md#L990) | — |
| 272 | 06/08/2026 | inferi o comportamento do runner pelo desenho do validador, e o `unknown` que eu chamei de brando derrubava a fase | [L992](../RETROSPECTIVAS.md#L992) | — |
| 282 | 06/08/2026 | o gate certo não pergunta se o bloqueio foi bem escrito, pergunta se ainda há porta por abrir | [L1010](../RETROSPECTIVAS.md#L1010) | — |
| 284 | 06/08/2026 | o conselho e a revisão cruzada acharam erro que gate nenhum acharia, e os três erros eram de tipos diferentes | [L1024](../RETROSPECTIVAS.md#L1024) | — |
| 285 | 06/08/2026 | o gate que faltava era o do critério que o cliente escreveu, e ele é de uma espécie que a casa não tinha | [L1026](../RETROSPECTIVAS.md#L1026) | — |
| 286 | 06/08/2026 | o destaque na margem saiu cortado no meio de uma citação legal, e o gate que devia pegar isso olhava para o lado errado | [L1028](../RETROSPECTIVAS.md#L1028) | — |
| 288 | 06/08/2026 | o conserto do detector produziu um falso positivo, e só a medição contra o acervo inteiro o pegou | [L1032](../RETROSPECTIVAS.md#L1032) | — |
| 296 | 06/08/2026 | o subagente fabricou sete nomes de script, no padrão da casa, apresentados como citação | [L1050](../RETROSPECTIVAS.md#L1050) | — |
| 297 | 06/08/2026 | a seção que diz "regra escrita que não pega vira gate" não virou gate | [L1052](../RETROSPECTIVAS.md#L1052) | — |
| 307 | 06/08/2026 | dois revisores independentes leram o mesmo nome de gate ao contrário, com três dias de intervalo | [L1064](../RETROSPECTIVAS.md#L1064) | — |
| 300 | 06/08/2026 | a lição 297 estava errada, e o erro dela é o da 296, três parágrafos acima | [L1066](../RETROSPECTIVAS.md#L1066) | — |
| 308 | 06/08/2026 | o `grep` que a lição 296 mandou dar, eu dei, e ele mentiu por convenção de nome | [L1068](../RETROSPECTIVAS.md#L1068) | — |
| 310 | 06/08/2026 | o gate acusou de vazio um documento cheio, e isso é pior que não conferir | [L1072](../RETROSPECTIVAS.md#L1072) | — |
| 322 | 06/08/2026 | abrir a segunda porta é onde o risco mora, e o risco tinha data | [L1096](../RETROSPECTIVAS.md#L1096) | — |
| 326 | 06/08/2026 | identificador real de mensagem é dado do escritório, mesmo sem conteúdo | [L1104](../RETROSPECTIVAS.md#L1104) | — |

<a id="lastro"></a>
## Lastro: afirmação conferida na fonte

41 lições.

| nº | data | lição | onde | o que a faz reprovar |
|---:|---|---|---|---|
| 2 | 08/07/2026 | Alucinação de nomes de advogados | [L12](../RETROSPECTIVAS.md#L12) | — |
| 4 | 08/07/2026 | Aspas com paráfrase de súmula | [L14](../RETROSPECTIVAS.md#L14) | — |
| 10 | 08/07/2026 | Inversão de fatos espelhados | [L27](../RETROSPECTIVAS.md#L27) | — |
| 14 | 08/07/2026 | Dado divergente entre casos | [L31](../RETROSPECTIVAS.md#L31) | — |
| 15 | 08/07/2026 | Número agregado sem fonte literal é alucinação de precisão | [L37](../RETROSPECTIVAS.md#L37) | forja_verificador.py |
| 20 | 08/07/2026 | Documento "em tese" (sem autos) é o pior cenário para alucinação de dispositivo legal | [L53](../RETROSPECTIVAS.md#L53) | forja_citations.py, forja_verificador.py |
| 21 | 08/07/2026 | Alucinação de INSTITUTO é pior que a de dispositivo e sobrevive a auditorias de citação | [L55](../RETROSPECTIVAS.md#L55) | forja_verificador.py |
| 23 | 08/07/2026 | Marcador de verificação com número de súmula é melhor que marcador genérico | [L59](../RETROSPECTIVAS.md#L59) | — |
| 26 | 08/07/2026 | Precedente sem lastro nos autos deve cair, não ganhar marcador | [L69](../RETROSPECTIVAS.md#L69) | — |
| 28 | 09/07/2026 | Verificação em fonte oficial não é burocracia: muda o resultado da peça | [L75](../RETROSPECTIVAS.md#L75) | — |
| 30 | 09/07/2026 | Fontes abertas primeiro, navegador depois | [L79](../RETROSPECTIVAS.md#L79) | — |
| 34 | 09/07/2026 | Conferir o achado do auditor antes de corrigir | [L91](../RETROSPECTIVAS.md#L91) | — |
| 40 | 09/07/2026 | Os upgrades U1-U11 pagaram no primeiro caso em que rodaram juntos | [L111](../RETROSPECTIVAS.md#L111) | — |
| 42 | 09/07/2026 | Captura de fonte oficial em três atalhos que funcionaram: | [L115](../RETROSPECTIVAS.md#L115) | — |
| 61 | 11/07/2026 | Gate bloqueante sem lastro persistido é gate que já passou uma versão errada | [L161](../RETROSPECTIVAS.md#L161) | — |
| 65 | 11/07/2026 | Estratégia sem alternativa comparada corre o risco de apenas detalhar a primeira ideia | [L171](../RETROSPECTIVAS.md#L171) | — |
| 67 | 11/07/2026 | O produto final não pode provar sozinho as premissas usadas para produzi-lo | [L177](../RETROSPECTIVAS.md#L177) | — |
| 1 | 23/07/2026 | Plano bom nasce reprovado | [L221](../RETROSPECTIVAS.md#L221) | ⚠ citada, mas o número é ambíguo |
| 3 | 23/07/2026 | Gap v1 nº 2: | [L279](../RETROSPECTIVAS.md#L279) | ⚠ citada, mas o número é ambíguo |
| 5 | 23/07/2026 | Limitação que permanece (decisão de gasto do Igor): | [L329](../RETROSPECTIVAS.md#L329) | — |
| 86 | 26/07/2026 | Citar o localizador não é ter lido o localizador | [L338](../RETROSPECTIVAS.md#L338) | — |
| 88 | 26/07/2026 | Punir pendência declarada com a pena da invenção ensina o sistema a esconder lacuna | [L342](../RETROSPECTIVAS.md#L342) | — |
| 90 | 26/07/2026 | Importável não é acoplado | [L346](../RETROSPECTIVAS.md#L346) | — |
| 90 | 03/08/2026 | Conteúdo semântico de figura não é inferível de prosa argumentativa | [L376](../RETROSPECTIVAS.md#L376) | — |
| 95 | 03/08/2026 | Aceitar crítica sem conferir é o mesmo erro de aceitar elogio sem conferir | [L386](../RETROSPECTIVAS.md#L386) | — |
| 100 | 03/08/2026 | Gate declarado não é gate computado; a casa escreveu a proteção certa e a deixou fora da estrada | [L396](../RETROSPECTIVAS.md#L396) | — |
| 107 | 03/08/2026 | Fonte prevalente e valor monetário precisam ser gates de produção, não campos de confiança | [L424](../RETROSPECTIVAS.md#L424) | — |
| 108 | 03/08/2026 | Gate computado sobre conjunto vazio é pior que gate declarado, porque parece trabalho feito | [L426](../RETROSPECTIVAS.md#L426) | — |
| 109 | 03/08/2026 | Hash de fonte grande também precisa de lastro de execução | [L436](../RETROSPECTIVAS.md#L436) | — |
| 114 | 03/08/2026 | O gate que nunca rodou é indistinguível do gate que aprovou | [L446](../RETROSPECTIVAS.md#L446) | — |
| 118 | 03/08/2026 | Resolver a pasta do caso é parte do lastro, e isenção lexical precisa deixar recibo | [L454](../RETROSPECTIVAS.md#L454) | — |
| 120 | 03/08/2026 | Contagem histórica não pode sobreviver sem rótulo | [L458](../RETROSPECTIVAS.md#L458) | — |
| 133 | 03/08/2026 | A proveniência do VerifACT divergia por CRLF, não por conteúdo | [L510](../RETROSPECTIVAS.md#L510) | — |
| 160 | 03/08/2026 | Corrigir o produtor muda o censo; não se corrige o histórico para melhorar o número | [L564](../RETROSPECTIVAS.md#L564) | — |
| 164 | 03/08/2026 | Abri o XML, li errado, e escrevi um laudo alarmista | [L574](../RETROSPECTIVAS.md#L574) | — |
| 186 | 03/08/2026 | A rota declarada como "entrada única de produção" é chamada apenas por testes | [L619](../RETROSPECTIVAS.md#L619) | — |
| 192 | 03/08/2026 | laudo aprovado apontando para arquivo que não nasceu | [L631](../RETROSPECTIVAS.md#L631) | — |
| 212 | 03/08/2026 | emenda regimental recente muda peça pronta: o G11 pegou o que a memória não pegaria | [L671](../RETROSPECTIVAS.md#L671) | — |
| 222 | 03/08/2026 | mapa gerado que erra o motivo mente com aparência de autoridade | [L691](../RETROSPECTIVAS.md#L691) | — |
| 246 | 06/08/2026 | regra adotada carrega um lastro que pode deixar de existir | [L820](../RETROSPECTIVAS.md#L820) | — |
| 265 | 06/08/2026 | as regras lidas em e-mail exibiam lastro emprestado | [L913](../RETROSPECTIVAS.md#L913) | — |

<a id="citacao"></a>
## Citação, jurisprudência e dispositivo

36 lições.

| nº | data | lição | onde | o que a faz reprovar |
|---:|---|---|---|---|
| 1 | 08/07/2026 | PDF grande derruba leitor | [L11](../RETROSPECTIVAS.md#L11) | ⚠ citada, mas o número é ambíguo |
| 4 | 08/07/2026 | Aspas com paráfrase de súmula | [L14](../RETROSPECTIVAS.md#L14) | — |
| 9 | 08/07/2026 | Auditor de citações estourou contexto | [L26](../RETROSPECTIVAS.md#L26) | — |
| 15 | 08/07/2026 | Número agregado sem fonte literal é alucinação de precisão | [L37](../RETROSPECTIVAS.md#L37) | forja_verificador.py |
| 20 | 08/07/2026 | Documento "em tese" (sem autos) é o pior cenário para alucinação de dispositivo legal | [L53](../RETROSPECTIVAS.md#L53) | forja_citations.py, forja_verificador.py |
| 21 | 08/07/2026 | Alucinação de INSTITUTO é pior que a de dispositivo e sobrevive a auditorias de citação | [L55](../RETROSPECTIVAS.md#L55) | forja_verificador.py |
| 23 | 08/07/2026 | Marcador de verificação com número de súmula é melhor que marcador genérico | [L59](../RETROSPECTIVAS.md#L59) | — |
| 26 | 08/07/2026 | Precedente sem lastro nos autos deve cair, não ganhar marcador | [L69](../RETROSPECTIVAS.md#L69) | — |
| 28 | 09/07/2026 | Verificação em fonte oficial não é burocracia: muda o resultado da peça | [L75](../RETROSPECTIVAS.md#L75) | — |
| 29 | 09/07/2026 | As lições viram código, não só prosa | [L77](../RETROSPECTIVAS.md#L77) | — |
| 30 | 09/07/2026 | Fontes abertas primeiro, navegador depois | [L79](../RETROSPECTIVAS.md#L79) | — |
| 39 | 09/07/2026 | Confrontar o sistema com a literatura vale a pena quando há filtro de saída forte | [L107](../RETROSPECTIVAS.md#L107) | — |
| 41 | 09/07/2026 | Três defeitos de ferramenta descobertos em produção (consertar na próxima sessão de manutenção): | [L113](../RETROSPECTIVAS.md#L113) | forja_baseline.py, forja_citations.py, forja_metricas_f7.py, forja_render_docx.py, test_licao41.py, test_real_telemetria_licao41.py |
| 44 | 09/07/2026 | Review adversarial externo (Codex gpt-5.5, 09/07/2026 noite) pagou: 2 achados high reais que nenhum teste interno tinha pego | [L121](../RETROSPECTIVAS.md#L121) | — |
| 45 | 10/07/2026 | "Inexistência" de dispositivo também é afirmação factual e exige fonte DATADA | [L125](../RETROSPECTIVAS.md#L125) | — |
| 51 | 11/07/2026 | Matar a palavra procurada prova o detector literal, não a qualidade jurídica | [L139](../RETROSPECTIVAS.md#L139) | — |
| 54 | 11/07/2026 | Aprovação estrutural, liberação jurídica e promoção são estados independentes | [L145](../RETROSPECTIVAS.md#L145) | — |
| 58 | 11/07/2026 | Dispersão de cenários escolhidos não é variância operacional | [L153](../RETROSPECTIVAS.md#L153) | — |
| 77 | 15/07/2026 | Modelo de escrita não pode certificar a própria fidelidade | [L203](../RETROSPECTIVAS.md#L203) | — |
| 2 | 23/07/2026 | Taxa sem denominador congelado premia exclusão | [L228](../RETROSPECTIVAS.md#L228) | — |
| 1 | 23/07/2026 | O harness reprovou dois rounds de juiz antes de aceitar um | [L250](../RETROSPECTIVAS.md#L250) | ⚠ citada, mas o número é ambíguo |
| 96 | 27/07/2026 | Invenção de precedente parece ser função do vazio, não do modelo | [L362](../RETROSPECTIVAS.md#L362) | ⚠ citada, mas o número é ambíguo |
| 97 | 27/07/2026 | O auditor errou três vezes no mesmo dia, sempre reprovando o acerto | [L364](../RETROSPECTIVAS.md#L364) | — |
| 122 | 03/08/2026 | O gate mais caro da esteira era o mais confiado | [L488](../RETROSPECTIVAS.md#L488) | — |
| 124 | 03/08/2026 | O gate de identidade nasceu cobrando tribunal de artigo do CPC | [L492](../RETROSPECTIVAS.md#L492) | ⚠ citada, mas o número é ambíguo |
| 134 | 03/08/2026 | O validador da exploração existia e rodava; os gates que o atestam eram escritos à mão | [L512](../RETROSPECTIVAS.md#L512) | — |
| 209 | 03/08/2026 | o teste que prova a separação não é conferir a lista de arquivos: é clonar e rodar | [L665](../RETROSPECTIVAS.md#L665) | — |
| 214 | 03/08/2026 | o rascunho de agente segue errando nas mesmas quatro casas: partes, dispositivos, origem e autocontinência | [L675](../RETROSPECTIVAS.md#L675) | — |
| 254 | 06/08/2026 | a leitura dos e-mails devolveu, em uma tarde, mais padrão do que seis casos de diff automático | [L875](../RETROSPECTIVAS.md#L875) | — |
| 256 | 06/08/2026 | o rótulo da caixa afirmava um precedente que o parágrafo não tinha | [L879](../RETROSPECTIVAS.md#L879) | — |
| 258 | 06/08/2026 | havia uma hierarquia de pesquisa jurisprudencial escrita e a esteira não a conhecia | [L897](../RETROSPECTIVAS.md#L897) | — |
| 276 | 06/08/2026 | "a ferramenta não alcança" era falta de chave, e eu já tinha escrito isso ao cliente | [L994](../RETROSPECTIVAS.md#L994) | ⚠ citada, mas o número é ambíguo |
| 286 | 06/08/2026 | o destaque na margem saiu cortado no meio de uma citação legal, e o gate que devia pegar isso olhava para o lado errado | [L1028](../RETROSPECTIVAS.md#L1028) | — |
| 291 | 06/08/2026 | "limitação da ferramenta" era limitação de uma rota, e a rota certa cabia numa linha | [L1040](../RETROSPECTIVAS.md#L1040) | — |
| 292 | 06/08/2026 | o achado que a leitura trouxe era o oposto do que a citação sugeria | [L1042](../RETROSPECTIVAS.md#L1042) | — |
| 296 | 06/08/2026 | o subagente fabricou sete nomes de script, no padrão da casa, apresentados como citação | [L1050](../RETROSPECTIVAS.md#L1050) | — |

<a id="redacao"></a>
## Redação, estilo e cara de IA

24 lições.

| nº | data | lição | onde | o que a faz reprovar |
|---:|---|---|---|---|
| 2 | 08/07/2026 | Alucinação de nomes de advogados | [L12](../RETROSPECTIVAS.md#L12) | — |
| 3 | 08/07/2026 | Artefatos internos vazaram para a peça | [L13](../RETROSPECTIVAS.md#L13) | ⚠ citada, mas o número é ambíguo |
| 5 | 08/07/2026 | Cara de IA no fecho | [L15](../RETROSPECTIVAS.md#L15) | — |
| 12 | 08/07/2026 | E-mail do nível 2 vaza jargão interno | [L29](../RETROSPECTIVAS.md#L29) | — |
| 22 | 08/07/2026 | O produto do workflow pode precisar de reescrita integral e isso é aceitável no fluxo | [L57](../RETROSPECTIVAS.md#L57) | — |
| 24 | 08/07/2026 | O redator de workflow produz "relatório de teses", não peça, quando o produto é memorial | [L65](../RETROSPECTIVAS.md#L65) | forja_verificador.py |
| 29 | 09/07/2026 | As lições viram código, não só prosa | [L77](../RETROSPECTIVAS.md#L77) | — |
| 76 | 15/07/2026 | O redator final deve vir depois da auditoria material e antes da composição visual | [L201](../RETROSPECTIVAS.md#L201) | — |
| 77 | 15/07/2026 | Modelo de escrita não pode certificar a própria fidelidade | [L203](../RETROSPECTIVAS.md#L203) | — |
| 78 | 15/07/2026 | Retry editorial parte da origem imutável, não da versão rejeitada | [L205](../RETROSPECTIVAS.md#L205) | — |
| 79 | 15/07/2026 | Múltiplos documentos exigem identidade de bundle, não pareamento por conveniência | [L207](../RETROSPECTIVAS.md#L207) | — |
| 4 | 23/07/2026 | Resultado negativo é resultado | [L282](../RETROSPECTIVAS.md#L282) | — |
| 90 | 03/08/2026 | Conteúdo semântico de figura não é inferível de prosa argumentativa | [L376](../RETROSPECTIVAS.md#L376) | — |
| 91 | 03/08/2026 | Defeito só é defeito contra o padrão aprovado | [L378](../RETROSPECTIVAS.md#L378) | — |
| 98 | 03/08/2026 | O defeito que "só o zoom pega" estava legível no XML o tempo todo | [L392](../RETROSPECTIVAS.md#L392) | — |
| 146 | 03/08/2026 | A dívida de esquema fechou pelo caminho barato, e o caro continua aberto | [L536](../RETROSPECTIVAS.md#L536) | — |
| 158 | 03/08/2026 | A síntese executiva obrigatória era lida como defeito tipográfico | [L560](../RETROSPECTIVAS.md#L560) | — |
| 184 | 03/08/2026 | O gate estrutural tem um limite que ainda precisa ser exercitado | [L615](../RETROSPECTIVAS.md#L615) | — |
| 190 | 03/08/2026 | o gate de estilo estava certo, e testar contra o padrão aprovado é o que provou isso | [L627](../RETROSPECTIVAS.md#L627) | — |
| 193 | 03/08/2026 | a referência quebrada só aparece para quem tenta abrir | [L633](../RETROSPECTIVAS.md#L633) | — |
| 215 | 03/08/2026 | o comparador de fidelidade editorial amarra no artefato do executor, não nos arquivos passados na CLI | [L677](../RETROSPECTIVAS.md#L677) | — |
| 271 | 06/08/2026 | o defeito não nascia no documento, nascia em dez geradores | [L980](../RETROSPECTIVAS.md#L980) | — |
| 320 | 06/08/2026 | escrevi a lição sobre vazar nome de cliente e vazei de novo no mesmo dia | [L1092](../RETROSPECTIVAS.md#L1092) | — |
| 324 | 06/08/2026 | o resumo comeu a prova, e o censo acusou de mentira um trabalho que estava feito | [L1100](../RETROSPECTIVAS.md#L1100) | — |

<a id="visual"></a>
## Visual law: figura, diagrama e diagramação

42 lições.

| nº | data | lição | onde | o que a faz reprovar |
|---:|---|---|---|---|
| 19 | 08/07/2026 | Acesso a Drive de cliente: esgotar 3 vias antes de declarar bloqueio | [L45](../RETROSPECTIVAS.md#L45) | — |
| 30 | 09/07/2026 | Fontes abertas primeiro, navegador depois | [L79](../RETROSPECTIVAS.md#L79) | — |
| 35 | 09/07/2026 | Circuito de gate só existe quando a etapa final é obrigada a consumi-lo | [L95](../RETROSPECTIVAS.md#L95) | — |
| 38 | 09/07/2026 | QA visual página a página continua achando o que nenhum gate pega | [L103](../RETROSPECTIVAS.md#L103) | — |
| 43 | 09/07/2026 | Teste sintético verde não prova ferramenta sã: a bateria REAL achou o que o unitário não alcançava | [L119](../RETROSPECTIVAS.md#L119) | test_licao41.py |
| 47 | 10/07/2026 | Auditor multi-agente também erra: verificação adversarial matou ~40% dos achados, e 2 "confirmados" caíram na checagem manual | [L129](../RETROSPECTIVAS.md#L129) | — |
| 60 | 11/07/2026 | Documentação de fechamento precisa carregar as ressalvas reais, não apenas os números verdes | [L157](../RETROSPECTIVAS.md#L157) | — |
| 72 | 12/07/2026 | Painel com hidratação viva tem DOIS pontos de injeção de dados; alimentar só um cria seção fantasma | [L189](../RETROSPECTIVAS.md#L189) | — |
| 76 | 15/07/2026 | O redator final deve vir depois da auditoria material e antes da composição visual | [L201](../RETROSPECTIVAS.md#L201) | — |
| 4 | 23/07/2026 | Locks transitórios do Windows domados: | [L325](../RETROSPECTIVAS.md#L325) | — |
| 88 | 03/08/2026 | Gate que só procura defeito nunca detecta pobreza | [L372](../RETROSPECTIVAS.md#L372) | — |
| 90 | 03/08/2026 | Conteúdo semântico de figura não é inferível de prosa argumentativa | [L376](../RETROSPECTIVAS.md#L376) | — |
| 91 | 03/08/2026 | Defeito só é defeito contra o padrão aprovado | [L378](../RETROSPECTIVAS.md#L378) | — |
| 93 | 03/08/2026 | Quem constrói não pode ser quem valida, e comitê que lê o resumo do construtor não escapa disso | [L382](../RETROSPECTIVAS.md#L382) | — |
| 96 | 03/08/2026 | O padrão-ouro tinha defeito, e o gate não podia vê-lo | [L388](../RETROSPECTIVAS.md#L388) | ⚠ citada, mas o número é ambíguo |
| 97 | 03/08/2026 | Duas variantes de capa foram aprovadas, e a constância não exige escolher uma só | [L390](../RETROSPECTIVAS.md#L390) | — |
| 98 | 03/08/2026 | O defeito que "só o zoom pega" estava legível no XML o tempo todo | [L392](../RETROSPECTIVAS.md#L392) | — |
| 99 | 03/08/2026 | ~~Quatro peças já entregues carregam diagrama defeituoso~~ — AFIRMAÇÃO ERRADA, corrigida em 03/08/2026 (ver Lição 103) | [L394](../RETROSPECTIVAS.md#L394) | forja_conselho.py, forja_modelos.py, forja_painel_curto.py, test_forja_cursor_grok.py, test_forja_painel_contribuicao.py |
| 101 | 03/08/2026 | "Rota única" é hipótese a medir, não intuição de arquiteto | [L398](../RETROSPECTIVAS.md#L398) | — |
| 103 | 03/08/2026 | Arquivo de produção não é arquivo entregue, e a diferença muda a decisão inteira | [L402](../RETROSPECTIVAS.md#L402) | — |
| 112 | 03/08/2026 | A decisão de não renderizar precisa estar no contrato, não apenas no código da rota | [L442](../RETROSPECTIVAS.md#L442) | — |
| 118 | 03/08/2026 | Resolver a pasta do caso é parte do lastro, e isenção lexical precisa deixar recibo | [L454](../RETROSPECTIVAS.md#L454) | — |
| 118 | 03/08/2026 | O contrato do F8 tinha 14 exigências que ninguém sabia cumprir, e o cumpridor estava do lado, calado | [L476](../RETROSPECTIVAS.md#L476) | — |
| 132 | 03/08/2026 | Grep não prova emissão, e foi grep que escondeu dois gates sem produtor | [L508](../RETROSPECTIVAS.md#L508) | — |
| 155 | 03/08/2026 | Os dezesseis gates da F8 nunca conheceram uma peça real, e isso incide sobre a decisão de ligá-los | [L554](../RETROSPECTIVAS.md#L554) | — |
| 158 | 03/08/2026 | A síntese executiva obrigatória era lida como defeito tipográfico | [L560](../RETROSPECTIVAS.md#L560) | — |
| 168 | 03/08/2026 | O gate do fólio tinha um teto que o acervo inteiro respeitava | [L583](../RETROSPECTIVAS.md#L583) | — |
| 169 | 03/08/2026 | Compor a peça REAL achou dois defeitos de produção que nenhum teste sintético acharia | [L585](../RETROSPECTIVAS.md#L585) | — |
| 173 | 03/08/2026 | O cético do painel refutou uma medição fresca citando documentação antiga | [L593](../RETROSPECTIVAS.md#L593) | — |
| 180 | 03/08/2026 | Contar arquivo no pacote não é contar figura na página, e a diferença cabe num comando de cópia | [L607](../RETROSPECTIVAS.md#L607) | — |
| 184 | 03/08/2026 | O gate estrutural tem um limite que ainda precisa ser exercitado | [L615](../RETROSPECTIVAS.md#L615) | — |
| 211 | 03/08/2026 | o DOCX com SVG nativo que passa no QA estrutural pode não abrir no Word | [L669](../RETROSPECTIVAS.md#L669) | — |
| 231 | 03/08/2026 | "medi uma base e ela não servia" virou "não existe fonte pública", e a generalização foi para uma nota técnica ao cliente | [L709](../RETROSPECTIVAS.md#L709) | — |
| 241 | 06/08/2026 | um teste parametrizado pelo registro faz o custo marginal de aprender ser zero | [L809](../RETROSPECTIVAS.md#L809) | — |
| 256 | 06/08/2026 | o rótulo da caixa afirmava um precedente que o parágrafo não tinha | [L879](../RETROSPECTIVAS.md#L879) | — |
| 258 | 06/08/2026 | quase ensinei o gate a aprovar um artefato que o Word não abre | [L883](../RETROSPECTIVAS.md#L883) | — |
| 264 | 06/08/2026 | a catraca tipográfica virou trava sem saída, e isso é decisão de dono, não de código | [L911](../RETROSPECTIVAS.md#L911) | — |
| 271 | 06/08/2026 | o defeito não nascia no documento, nascia em dez geradores | [L980](../RETROSPECTIVAS.md#L980) | — |
| 277 | 06/08/2026 | a rota canônica produzia arquivo que o Word não abre, e o QA aprovava | [L996](../RETROSPECTIVAS.md#L996) | — |
| 278 | 06/08/2026 | a legenda afirma procedência, e por isso não pode ser fixa | [L998](../RETROSPECTIVAS.md#L998) | ⚠ citada, mas o número é ambíguo |
| 293 | 06/08/2026 | três defeitos visuais que o QA página a página aprovou | [L1044](../RETROSPECTIVAS.md#L1044) | — |
| 307 | 06/08/2026 | dois revisores independentes leram o mesmo nome de gate ao contrário, com três dias de intervalo | [L1064](../RETROSPECTIVAS.md#L1064) | — |

<a id="modelos"></a>
## Modelos, famílias e revisão cruzada

24 lições.

| nº | data | lição | onde | o que a faz reprovar |
|---:|---|---|---|---|
| 44 | 09/07/2026 | Review adversarial externo (Codex gpt-5.5, 09/07/2026 noite) pagou: 2 achados high reais que nenhum teste interno tinha pego | [L121](../RETROSPECTIVAS.md#L121) | — |
| 75 | 12/07/2026 | Visualização de estado precisa da regra "maior fase alcançada": cursor de fase mente após reconcile | [L197](../RETROSPECTIVAS.md#L197) | forja_local_context.py |
| 77 | 15/07/2026 | Modelo de escrita não pode certificar a própria fidelidade | [L203](../RETROSPECTIVAS.md#L203) | — |
| 79 | 15/07/2026 | Múltiplos documentos exigem identidade de bundle, não pareamento por conveniência | [L207](../RETROSPECTIVAS.md#L207) | — |
| 80 | 15/07/2026 | Review externo produz hipóteses; regressão e execução real decidem | [L209](../RETROSPECTIVAS.md#L209) | — |
| 1 | 23/07/2026 | Plano bom nasce reprovado | [L221](../RETROSPECTIVAS.md#L221) | ⚠ citada, mas o número é ambíguo |
| 4 | 23/07/2026 | Karpathy sobre trilhos anti-trapaça funciona: | [L263](../RETROSPECTIVAS.md#L263) | — |
| 1 | 23/07/2026 | Toda lição virou código, não disciplina de prompt: | [L315](../RETROSPECTIVAS.md#L315) | ⚠ citada, mas o número é ambíguo |
| 91 | 26/07/2026 | Ledger que apaga o erro perde a lição | [L348](../RETROSPECTIVAS.md#L348) | — |
| 92 | 27/07/2026 | Apelido de modelo não é modelo, e a esteira inteira pode estar rodando outro | [L354](../RETROSPECTIVAS.md#L354) | — |
| 94 | 27/07/2026 | Escrever bem e obedecer são capacidades distintas, e o mesmo modelo pode ter uma sem a outra | [L358](../RETROSPECTIVAS.md#L358) | — |
| 95 | 27/07/2026 | Auto-preferência de juiz é número, não suspeita | [L360](../RETROSPECTIVAS.md#L360) | — |
| 96 | 27/07/2026 | Invenção de precedente parece ser função do vazio, não do modelo | [L362](../RETROSPECTIVAS.md#L362) | ⚠ citada, mas o número é ambíguo |
| 97 | 27/07/2026 | O auditor errou três vezes no mesmo dia, sempre reprovando o acerto | [L364](../RETROSPECTIVAS.md#L364) | — |
| 93 | 03/08/2026 | Quem constrói não pode ser quem valida, e comitê que lê o resumo do construtor não escapa disso | [L382](../RETROSPECTIVAS.md#L382) | — |
| 109 | 03/08/2026 | Hash de fonte grande também precisa de lastro de execução | [L436](../RETROSPECTIVAS.md#L436) | — |
| 221 | 03/08/2026 | `lstrip("./")` não remove o prefixo `./`: remove qualquer ponto ou barra do começo | [L689](../RETROSPECTIVAS.md#L689) | — |
| 270 | 06/08/2026 | o base64 corrompido não levanta exceção: decodifica em lixo e o anexo some da conferência | [L978](../RETROSPECTIVAS.md#L978) | ⚠ citada, mas o número é ambíguo |
| 273 | 06/08/2026 | o placar de contribuição quase nasceu premiando quem só concorda | [L1000](../RETROSPECTIVAS.md#L1000) | — |
| 274 | 06/08/2026 | reprovado e não aferido não podem ter a mesma cor | [L1002](../RETROSPECTIVAS.md#L1002) | — |
| 276 | 06/08/2026 | o perfil de uso que eu esperava não existe, e o que existe é chato | [L1014](../RETROSPECTIVAS.md#L1014) | ⚠ citada, mas o número é ambíguo |
| 277 | 06/08/2026 | a régua lexical não distingue modelos por conteúdo, e descobrir isso vale mais do que o número que ela dava | [L1016](../RETROSPECTIVAS.md#L1016) | — |
| 284 | 06/08/2026 | o conselho e a revisão cruzada acharam erro que gate nenhum acharia, e os três erros eram de tipos diferentes | [L1024](../RETROSPECTIVAS.md#L1024) | — |
| 304 | 06/08/2026 | o sandbox somente-leitura do Codex não lê nada neste Windows, e quase produziu um parecer inteiro escrito de memória | [L1058](../RETROSPECTIVAS.md#L1058) | — |

<a id="processual"></a>
## Identidade processual e peça

11 lições.

| nº | data | lição | onde | o que a faz reprovar |
|---:|---|---|---|---|
| 38 | 09/07/2026 | QA visual página a página continua achando o que nenhum gate pega | [L103](../RETROSPECTIVAS.md#L103) | — |
| 45 | 10/07/2026 | "Inexistência" de dispositivo também é afirmação factual e exige fonte DATADA | [L125](../RETROSPECTIVAS.md#L125) | — |
| 54 | 11/07/2026 | Aprovação estrutural, liberação jurídica e promoção são estados independentes | [L145](../RETROSPECTIVAS.md#L145) | — |
| 63 | 11/07/2026 | O comando recebido não é a definição do problema | [L167](../RETROSPECTIVAS.md#L167) | — |
| 89 | 26/07/2026 | Auditor que reprova o acerto é desligado na terceira vez | [L344](../RETROSPECTIVAS.md#L344) | ⚠ citada, mas o número é ambíguo |
| 124 | 03/08/2026 | O gate de identidade nasceu cobrando tribunal de artigo do CPC | [L492](../RETROSPECTIVAS.md#L492) | ⚠ citada, mas o número é ambíguo |
| 140 | 03/08/2026 | Hash de cópia arquivada e hash de regimento significam coisas opostas | [L524](../RETROSPECTIVAS.md#L524) | — |
| 212 | 03/08/2026 | emenda regimental recente muda peça pronta: o G11 pegou o que a memória não pegaria | [L671](../RETROSPECTIVAS.md#L671) | — |
| 216 | 03/08/2026 | "separado" conferido por lista de arquivos não é separado; o dado de cliente mora DENTRO dos arquivos | [L679](../RETROSPECTIVAS.md#L679) | — |
| 218 | 03/08/2026 | anonimizar a doutrina sem matar a doutrina: pseudônimo estável, tradução no acervo | [L683](../RETROSPECTIVAS.md#L683) | — |
| 287 | 06/08/2026 | dois casos ficaram 37 horas fora da fila com um bloqueio que o próprio texto deles desmentia na primeira linha | [L1030](../RETROSPECTIVAS.md#L1030) | — |

<a id="entrega"></a>
## Entrega ao destinatário e comunicação

36 lições.

| nº | data | lição | onde | o que a faz reprovar |
|---:|---|---|---|---|
| 6 | 08/07/2026 | E-mail de resposta | [L16](../RETROSPECTIVAS.md#L16) | — |
| 12 | 08/07/2026 | E-mail do nível 2 vaza jargão interno | [L29](../RETROSPECTIVAS.md#L29) | — |
| 14 | 08/07/2026 | Dado divergente entre casos | [L31](../RETROSPECTIVAS.md#L31) | — |
| 35 | 09/07/2026 | Circuito de gate só existe quando a etapa final é obrigada a consumi-lo | [L95](../RETROSPECTIVAS.md#L95) | — |
| 48 | 10/07/2026 | Reconciliação painel×disco pegou o risco operacional mais grave da rodada: a versão ENVIADA ao Fábio (03:42) era anterior à N3 e ainda continha o pedido de honorários recursais removido por erro jurídico; a N3 corrigida não foi enviada | [L131](../RETROSPECTIVAS.md#L131) | forja_anonimizar.py, forja_delivery.py, forja_visual.py |
| 54 | 11/07/2026 | Aprovação estrutural, liberação jurídica e promoção são estados independentes | [L145](../RETROSPECTIVAS.md#L145) | — |
| 79 | 15/07/2026 | Múltiplos documentos exigem identidade de bundle, não pareamento por conveniência | [L207](../RETROSPECTIVAS.md#L207) | — |
| 5 | 23/07/2026 | Custo de execução é achado de primeira ordem: | [L286](../RETROSPECTIVAS.md#L286) | — |
| 84 | 23/07/2026 | Pendência não é sinônimo de bloqueador e checklist interno não é mensagem de entrega | [L292](../RETROSPECTIVAS.md#L292) | — |
| 5 | 23/07/2026 | Limitação que permanece (decisão de gasto do Igor): | [L329](../RETROSPECTIVAS.md#L329) | — |
| 90 | 26/07/2026 | Importável não é acoplado | [L346](../RETROSPECTIVAS.md#L346) | — |
| 88 | 03/08/2026 | Gate que só procura defeito nunca detecta pobreza | [L372](../RETROSPECTIVAS.md#L372) | — |
| 103 | 03/08/2026 | Arquivo de produção não é arquivo entregue, e a diferença muda a decisão inteira | [L402](../RETROSPECTIVAS.md#L402) | — |
| 111 | 03/08/2026 | Documento de auditabilidade descrito no plano não é documento obrigatório até bloquear a entrega | [L440](../RETROSPECTIVAS.md#L440) | — |
| 141 | 03/08/2026 | O gate mais perigoso da esteira protege o único artefato que o destinatário lê | [L526](../RETROSPECTIVAS.md#L526) | — |
| 162 | 03/08/2026 | B — No acervo desta fábrica, timbre não é sinal de entregável | [L570](../RETROSPECTIVAS.md#L570) | — |
| 210 | 03/08/2026 | a regra que existia no `.gitignore` antigo e não foi portada vira vazamento no repositório novo | [L667](../RETROSPECTIVAS.md#L667) | — |
| 224 | 03/08/2026 | dentro da pasta de caso, quem decide o destino é a extensão, e cada lado tem um porquê diferente | [L695](../RETROSPECTIVAS.md#L695) | — |
| 240 | 06/08/2026 | o gate de aprendizado que parece certo é o errado | [L807](../RETROSPECTIVAS.md#L807) | — |
| 247 | 06/08/2026 | a esteira era cega por construção para a correção que vem no corpo do e-mail | [L822](../RETROSPECTIVAS.md#L822) | — |
| 253 | 06/08/2026 | escrita direta em arquivo de registro falha quando a publicação lê a mesma árvore | [L873](../RETROSPECTIVAS.md#L873) | — |
| 254 | 06/08/2026 | a leitura dos e-mails devolveu, em uma tarde, mais padrão do que seis casos de diff automático | [L875](../RETROSPECTIVAS.md#L875) | — |
| 258 | 06/08/2026 | quase ensinei o gate a aprovar um artefato que o Word não abre | [L883](../RETROSPECTIVAS.md#L883) | — |
| 259 | 06/08/2026 | varri três fontes públicas o dia inteiro para redescobrir o que o sistema do escritório já sabia | [L886](../RETROSPECTIVAS.md#L886) | — |
| 265 | 06/08/2026 | as regras lidas em e-mail exibiam lastro emprestado | [L913](../RETROSPECTIVAS.md#L913) | — |
| 267 | 06/08/2026 | tirar arquivo do escopo afrouxa a catraca duas vezes, e a segunda é invisível | [L917](../RETROSPECTIVAS.md#L917) | forja_triagem_rapida.py |
| 271 | 06/08/2026 | o defeito não nascia no documento, nascia em dez geradores | [L980](../RETROSPECTIVAS.md#L980) | — |
| 276 | 06/08/2026 | "a ferramenta não alcança" era falta de chave, e eu já tinha escrito isso ao cliente | [L994](../RETROSPECTIVAS.md#L994) | ⚠ citada, mas o número é ambíguo |
| 277 | 06/08/2026 | a rota canônica produzia arquivo que o Word não abre, e o QA aprovava | [L996](../RETROSPECTIVAS.md#L996) | — |
| 279 | 06/08/2026 | a varredura de código morto quase apagou o servidor de e-mail que eu usara naquela sessão | [L1006](../RETROSPECTIVAS.md#L1006) | — |
| 289 | 06/08/2026 | a fila inteira de bloqueios da FORJA repousava sobre um campo que nunca afirmou o que dizia | [L1034](../RETROSPECTIVAS.md#L1034) | — |
| 290 | 06/08/2026 | o vigia viu, escreveu, e a informação não andou mais um metro | [L1036](../RETROSPECTIVAS.md#L1036) | — |
| 306 | 06/08/2026 | quatro auditorias adversariais encontraram, cada uma, o que a sua lente foi feita para ver | [L1062](../RETROSPECTIVAS.md#L1062) | — |
| 307 | 06/08/2026 | dois revisores independentes leram o mesmo nome de gate ao contrário, com três dias de intervalo | [L1064](../RETROSPECTIVAS.md#L1064) | — |
| 316 | 06/08/2026 | procurei a prova da entrega na pasta errada e quase inverti o diagnóstico; quem me pegou foi a lente adversarial | [L1084](../RETROSPECTIVAS.md#L1084) | — |
| 325 | 06/08/2026 | alerta que ninguém consegue baixar é alerta que ninguém lê | [L1102](../RETROSPECTIVAS.md#L1102) | — |

<a id="aprendizado"></a>
## Retorno humano e aprendizado da casa

2 lições.

| nº | data | lição | onde | o que a faz reprovar |
|---:|---|---|---|---|
| 240 | 06/08/2026 | o gate de aprendizado que parece certo é o errado | [L807](../RETROSPECTIVAS.md#L807) | — |
| 246 | 06/08/2026 | regra adotada carrega um lastro que pode deixar de existir | [L820](../RETROSPECTIVAS.md#L820) | — |

<a id="acoplamento"></a>
## Acoplamento: onde o código de fato passa

7 lições.

| nº | data | lição | onde | o que a faz reprovar |
|---:|---|---|---|---|
| 83 | 16/07/2026 | Utilitário duplicado diverge em silêncio | [L217](../RETROSPECTIVAS.md#L217) | — |
| 90 | 26/07/2026 | Importável não é acoplado | [L346](../RETROSPECTIVAS.md#L346) | — |
| 89 | 03/08/2026 | O gate na rota que ninguém percorre é gate nenhum | [L374](../RETROSPECTIVAS.md#L374) | ⚠ citada, mas o número é ambíguo |
| 100 | 03/08/2026 | Gate declarado não é gate computado; a casa escreveu a proteção certa e a deixou fora da estrada | [L396](../RETROSPECTIVAS.md#L396) | — |
| 101 | 03/08/2026 | "Rota única" é hipótese a medir, não intuição de arquiteto | [L398](../RETROSPECTIVAS.md#L398) | — |
| 113 | 03/08/2026 | Compatibilidade legada não precisa contaminar a rota canônica | [L444](../RETROSPECTIVAS.md#L444) | — |
| 186 | 03/08/2026 | A rota declarada como "entrada única de produção" é chamada apenas por testes | [L619](../RETROSPECTIVAS.md#L619) | — |

<a id="estado"></a>
## Estado, artefatos e contratos de fase

44 lições.

| nº | data | lição | onde | o que a faz reprovar |
|---:|---|---|---|---|
| 52 | 11/07/2026 | Caminho + SHA-256 prova identidade física do arquivo, não sustentação da proposição | [L141](../RETROSPECTIVAS.md#L141) | forja_ledger_material.py, test_forja_ledger_material.py |
| 56 | 11/07/2026 | A gestão deve revalidar o maior alvo N4 auditado, não apenas a fase corrente da N3 | [L149](../RETROSPECTIVAS.md#L149) | — |
| 57 | 11/07/2026 | Auditoria visual automática não deve se apresentar como revisão humana | [L151](../RETROSPECTIVAS.md#L151) | — |
| 60 | 11/07/2026 | Documentação de fechamento precisa carregar as ressalvas reais, não apenas os números verdes | [L157](../RETROSPECTIVAS.md#L157) | — |
| 82 | 16/07/2026 | Estado F0 defasado gera alarme falso no contexto de sessão | [L215](../RETROSPECTIVAS.md#L215) | — |
| 2 | 23/07/2026 | Taxa sem denominador congelado premia exclusão | [L228](../RETROSPECTIVAS.md#L228) | — |
| 5 | 23/07/2026 | Manifesto da Régua pode dormir defasado | [L242](../RETROSPECTIVAS.md#L242) | — |
| 2 | 23/07/2026 | Custo virou indicador formal: | [L319](../RETROSPECTIVAS.md#L319) | — |
| 5 | 23/07/2026 | Limitação que permanece (decisão de gasto do Igor): | [L329](../RETROSPECTIVAS.md#L329) | — |
| 86 | 26/07/2026 | Citar o localizador não é ter lido o localizador | [L338](../RETROSPECTIVAS.md#L338) | — |
| 87 | 26/07/2026 | Achado forte gera excesso na redação, e o excesso vem depois da revisão | [L340](../RETROSPECTIVAS.md#L340) | ⚠ citada, mas o número é ambíguo |
| 90 | 26/07/2026 | Importável não é acoplado | [L346](../RETROSPECTIVAS.md#L346) | — |
| 91 | 26/07/2026 | Ledger que apaga o erro perde a lição | [L348](../RETROSPECTIVAS.md#L348) | — |
| 100 | 03/08/2026 | Gate declarado não é gate computado; a casa escreveu a proteção certa e a deixou fora da estrada | [L396](../RETROSPECTIVAS.md#L396) | — |
| 107 | 03/08/2026 | Fonte prevalente e valor monetário precisam ser gates de produção, não campos de confiança | [L424](../RETROSPECTIVAS.md#L424) | — |
| 108 | 03/08/2026 | Gate computado sobre conjunto vazio é pior que gate declarado, porque parece trabalho feito | [L426](../RETROSPECTIVAS.md#L426) | — |
| 110 | 03/08/2026 | Baseline longo não substitui a régua curta | [L438](../RETROSPECTIVAS.md#L438) | — |
| 114 | 03/08/2026 | O gate que nunca rodou é indistinguível do gate que aprovou | [L446](../RETROSPECTIVAS.md#L446) | — |
| 116 | 03/08/2026 | Ledger inválido não pode desaparecer na mesma saída de “não aplicável” | [L450](../RETROSPECTIVAS.md#L450) | — |
| 117 | 03/08/2026 | Fallback de snapshot é uma regressão de fonte prevalente, não uma cortesia de compatibilidade | [L452](../RETROSPECTIVAS.md#L452) | — |
| 118 | 03/08/2026 | Resolver a pasta do caso é parte do lastro, e isenção lexical precisa deixar recibo | [L454](../RETROSPECTIVAS.md#L454) | — |
| 119 | 03/08/2026 | Caminho explícito inválido tem precedência sobre descoberta conveniente | [L456](../RETROSPECTIVAS.md#L456) | — |
| 126 | 03/08/2026 | Caminho explicitamente ausente não é ausência de escolha | [L470](../RETROSPECTIVAS.md#L470) | — |
| 117 | 03/08/2026 | Quase publiquei o número errado por confundir ausência de código com ausência de execução | [L474](../RETROSPECTIVAS.md#L474) | — |
| 121 | 03/08/2026 | Piso de tamanho é o antídoto barato contra o arquivo criado para o gate | [L484](../RETROSPECTIVAS.md#L484) | — |
| 122 | 03/08/2026 | O gate mais caro da esteira era o mais confiado | [L488](../RETROSPECTIVAS.md#L488) | — |
| 128 | 03/08/2026 | Um ledger real tinha dez fontes oficiais e nenhuma arquivada, e o gate chamado `official_sources_archived` dizia `pass` | [L500](../RETROSPECTIVAS.md#L500) | — |
| 144 | 03/08/2026 | Cometi contra mim mesmo, no censo, o erro que já tinha documentado horas antes | [L532](../RETROSPECTIVAS.md#L532) | — |
| 149 | 03/08/2026 | Metade das reprovações do censo era do gate, não do caso | [L542](../RETROSPECTIVAS.md#L542) | — |
| 152 | 03/08/2026 | O laudo de triagem também é artefato, e também errou | [L548](../RETROSPECTIVAS.md#L548) | — |
| 154 | 03/08/2026 | Consertei o termômetro e por um momento acreditei ter consertado a esteira | [L552](../RETROSPECTIVAS.md#L552) | — |
| 155 | 03/08/2026 | Os dezesseis gates da F8 nunca conheceram uma peça real, e isso incide sobre a decisão de ligá-los | [L554](../RETROSPECTIVAS.md#L554) | — |
| 156 | 03/08/2026 | "O censo não chama o produtor" era hipótese confortável; o material é que não existe | [L556](../RETROSPECTIVAS.md#L556) | — |
| 160 | 03/08/2026 | Corrigir o produtor muda o censo; não se corrige o histórico para melhorar o número | [L564](../RETROSPECTIVAS.md#L564) | — |
| 162 | 03/08/2026 | Contraprova real e veredito de produção não são a mesma coisa | [L568](../RETROSPECTIVAS.md#L568) | — |
| 165 | 03/08/2026 | Medir a versão superada foi a TERCEIRA reincidência do mesmo erro num só dia | [L577](../RETROSPECTIVAS.md#L577) | — |
| 171 | 03/08/2026 | Os cinco gates da F9 nunca tiveram material porque o leitor abria o nome errado | [L589](../RETROSPECTIVAS.md#L589) | — |
| 175 | 03/08/2026 | Três dos cinco achados de um painel de quinze agentes não sobreviveram a quinze minutos de conferência | [L597](../RETROSPECTIVAS.md#L597) | — |
| 195 | 03/08/2026 | ler o código prova presença; só executar prova comportamento | [L637](../RETROSPECTIVAS.md#L637) | — |
| 204 | 03/08/2026 | antes de planejar a campanha, abra o arquivo que ela manda consultar | [L655](../RETROSPECTIVAS.md#L655) | — |
| 232 | 03/08/2026 | o cadastro respondia "existe"; era o TEOR que respondia "quanto", e eu declarei ao cliente que faltava ir aos autos sem ter tentado ler o teor | [L721](../RETROSPECTIVAS.md#L721) | — |
| 241 | 06/08/2026 | um teste parametrizado pelo registro faz o custo marginal de aprender ser zero | [L809](../RETROSPECTIVAS.md#L809) | — |
| 261 | 06/08/2026 | apliquei metade do que a casa aprendeu num arquivo que rota nenhuma percorre | [L901](../RETROSPECTIVAS.md#L901) | — |
| 324 | 06/08/2026 | o resumo comeu a prova, e o censo acusou de mentira um trabalho que estava feito | [L1100](../RETROSPECTIVAS.md#L1100) | — |

<a id="fronteira"></a>
## Fronteira, sigilo e proveniência

15 lições.

| nº | data | lição | onde | o que a faz reprovar |
|---:|---|---|---|---|
| 52 | 11/07/2026 | Caminho + SHA-256 prova identidade física do arquivo, não sustentação da proposição | [L141](../RETROSPECTIVAS.md#L141) | forja_ledger_material.py, test_forja_ledger_material.py |
| 76 | 15/07/2026 | O redator final deve vir depois da auditoria material e antes da composição visual | [L201](../RETROSPECTIVAS.md#L201) | — |
| 77 | 15/07/2026 | Modelo de escrita não pode certificar a própria fidelidade | [L203](../RETROSPECTIVAS.md#L203) | — |
| 91 | 26/07/2026 | Ledger que apaga o erro perde a lição | [L348](../RETROSPECTIVAS.md#L348) | — |
| 133 | 03/08/2026 | A proveniência do VerifACT divergia por CRLF, não por conteúdo | [L510](../RETROSPECTIVAS.md#L510) | — |
| 195 | 03/08/2026 | ler o código prova presença; só executar prova comportamento | [L637](../RETROSPECTIVAS.md#L637) | — |
| 218 | 03/08/2026 | anonimizar a doutrina sem matar a doutrina: pseudônimo estável, tradução no acervo | [L683](../RETROSPECTIVAS.md#L683) | — |
| 219 | 03/08/2026 | o gate que detecta nome de cliente não pode carregar a lista de nomes | [L685](../RETROSPECTIVAS.md#L685) | — |
| 221 | 03/08/2026 | `lstrip("./")` não remove o prefixo `./`: remove qualquer ponto ou barra do começo | [L689](../RETROSPECTIVAS.md#L689) | — |
| 222 | 03/08/2026 | mapa gerado que erra o motivo mente com aparência de autoridade | [L691](../RETROSPECTIVAS.md#L691) | — |
| 223 | 03/08/2026 | não mover as pastas de caso foi decisão medida, não omissão | [L693](../RETROSPECTIVAS.md#L693) | — |
| 252 | 06/08/2026 | o gate da fronteira apanhou a mim, de novo, e de novo estava certo | [L871](../RETROSPECTIVAS.md#L871) | — |
| 269 | 06/08/2026 | a fronteira me pegou pela quarta vez, sempre pelo mesmo motivo | [L972](../RETROSPECTIVAS.md#L972) | — |
| 318 | 06/08/2026 | a fronteira reprovou a lição que eu estava escrevendo sobre disciplina | [L1088](../RETROSPECTIVAS.md#L1088) | — |
| 320 | 06/08/2026 | escrevi a lição sobre vazar nome de cliente e vazei de novo no mesmo dia | [L1092](../RETROSPECTIVAS.md#L1092) | — |

<a id="automacao"></a>
## Automação, agendamento e volume

11 lições.

| nº | data | lição | onde | o que a faz reprovar |
|---:|---|---|---|---|
| 33 | 09/07/2026 | Estado que não é atualizado pelo caminho real de execução mente | [L89](../RETROSPECTIVAS.md#L89) | — |
| 82 | 16/07/2026 | Estado F0 defasado gera alarme falso no contexto de sessão | [L215](../RETROSPECTIVAS.md#L215) | — |
| 4 | 23/07/2026 | Locks transitórios do Windows domados: | [L325](../RETROSPECTIVAS.md#L325) | — |
| 87 | 03/08/2026 | Recurso que depende de esforço manual por caso não sobrevive ao volume | [L370](../RETROSPECTIVAS.md#L370) | ⚠ citada, mas o número é ambíguo |
| 104 | 03/08/2026 | Varredura em massa não pode abortar por causa de um arquivo, e "erro de caminho inválido" nem sempre é do caminho | [L406](../RETROSPECTIVAS.md#L406) | — |
| 106 | 03/08/2026 | Repetir a operação inteira não converge quando a falha é transitória e itinerante; repescar converge | [L418](../RETROSPECTIVAS.md#L418) | — |
| 217 | 03/08/2026 | a lista escrita à mão não estava errada, estava irrelevante | [L681](../RETROSPECTIVAS.md#L681) | forja_fronteira.py |
| 253 | 06/08/2026 | escrita direta em arquivo de registro falha quando a publicação lê a mesma árvore | [L873](../RETROSPECTIVAS.md#L873) | — |
| 263 | 06/08/2026 | o gate mais curto aprovou a árvore que o gate longo reprovou | [L909](../RETROSPECTIVAS.md#L909) | — |
| 278 | 06/08/2026 | a legenda afirma procedência, e por isso não pode ser fixa | [L998](../RETROSPECTIVAS.md#L998) | ⚠ citada, mas o número é ambíguo |
| 299 | 06/08/2026 | a prudência do commit não se transferia para a publicação | [L1056](../RETROSPECTIVAS.md#L1056) | — |

<a id="evidencia"></a>
## Prova, atestado e o que conta como evidência

37 lições.

| nº | data | lição | onde | o que a faz reprovar |
|---:|---|---|---|---|
| 33 | 09/07/2026 | Estado que não é atualizado pelo caminho real de execução mente | [L89](../RETROSPECTIVAS.md#L89) | — |
| 43 | 09/07/2026 | Teste sintético verde não prova ferramenta sã: a bateria REAL achou o que o unitário não alcançava | [L119](../RETROSPECTIVAS.md#L119) | test_licao41.py |
| 49 | 11/07/2026 | Resultado gravado pelo próprio fluxo não é prova independente | [L135](../RETROSPECTIVAS.md#L135) | — |
| 50 | 11/07/2026 | Temporalidade precisa integrar o hash e ser interpretada, não comparada como texto | [L137](../RETROSPECTIVAS.md#L137) | — |
| 51 | 11/07/2026 | Matar a palavra procurada prova o detector literal, não a qualidade jurídica | [L139](../RETROSPECTIVAS.md#L139) | — |
| 52 | 11/07/2026 | Caminho + SHA-256 prova identidade física do arquivo, não sustentação da proposição | [L141](../RETROSPECTIVAS.md#L141) | forja_ledger_material.py, test_forja_ledger_material.py |
| 61 | 11/07/2026 | Gate bloqueante sem lastro persistido é gate que já passou uma versão errada | [L161](../RETROSPECTIVAS.md#L161) | — |
| 68 | 11/07/2026 | Dimensão não medida não recebe nota zero nem aprovação | [L179](../RETROSPECTIVAS.md#L179) | — |
| 80 | 15/07/2026 | Review externo produz hipóteses; regressão e execução real decidem | [L209](../RETROSPECTIVAS.md#L209) | — |
| 83 | 16/07/2026 | Utilitário duplicado diverge em silêncio | [L217](../RETROSPECTIVAS.md#L217) | — |
| 4 | 23/07/2026 | Karpathy sobre trilhos anti-trapaça funciona: | [L263](../RETROSPECTIVAS.md#L263) | — |
| 86 | 26/07/2026 | Citar o localizador não é ter lido o localizador | [L338](../RETROSPECTIVAS.md#L338) | — |
| 92 | 03/08/2026 | O teste de mutação é o único que prova que o gate funciona | [L380](../RETROSPECTIVAS.md#L380) | — |
| 102 | 03/08/2026 | Medir a especificação contra o acervo pega o defeito antes de existir código; persistir a medição é o que a torna evidência | [L400](../RETROSPECTIVAS.md#L400) | — |
| 118 | 03/08/2026 | Resolver a pasta do caso é parte do lastro, e isenção lexical precisa deixar recibo | [L454](../RETROSPECTIVAS.md#L454) | — |
| 124 | 03/08/2026 | Anti-overblocking precisa de contraprova na rota, não só no detector | [L466](../RETROSPECTIVAS.md#L466) | ⚠ citada, mas o número é ambíguo |
| 125 | 03/08/2026 | Total correto com subtotais errados ainda é evidência ruim | [L468](../RETROSPECTIVAS.md#L468) | — |
| 127 | 03/08/2026 | Gate declarado na F10 precisa ser recomputado no evento que encerra o caso | [L480](../RETROSPECTIVAS.md#L480) | — |
| 120 | 03/08/2026 | O conselho obrigatório era atestado por quem tinha interesse em passar | [L482](../RETROSPECTIVAS.md#L482) | — |
| 132 | 03/08/2026 | Grep não prova emissão, e foi grep que escondeu dois gates sem produtor | [L508](../RETROSPECTIVAS.md#L508) | — |
| 147 | 03/08/2026 | O único jeito de saber se um gate sabe dizer não é destruir o artefato e olhar | [L538](../RETROSPECTIVAS.md#L538) | — |
| 172 | 03/08/2026 | Catraca que ninguém testa também é atestado | [L591](../RETROSPECTIVAS.md#L591) | — |
| 178 | 03/08/2026 | Quatro afrouxamentos seguidos e um verde perfeito no fim são indistinguíveis de um gate moldado | [L603](../RETROSPECTIVAS.md#L603) | — |
| 188 | 03/08/2026 | o gate verde por cegueira, cometido por quem construía a defesa contra ele | [L623](../RETROSPECTIVAS.md#L623) | forja_lapidacao_governanca.py, test_forja_lapidacao_governanca.py |
| 192 | 03/08/2026 | laudo aprovado apontando para arquivo que não nasceu | [L631](../RETROSPECTIVAS.md#L631) | — |
| 193 | 03/08/2026 | a referência quebrada só aparece para quem tenta abrir | [L633](../RETROSPECTIVAS.md#L633) | — |
| 195 | 03/08/2026 | ler o código prova presença; só executar prova comportamento | [L637](../RETROSPECTIVAS.md#L637) | — |
| 207 | 03/08/2026 | diagnosticar UM bloqueio não prova que só existe um | [L661](../RETROSPECTIVAS.md#L661) | — |
| 209 | 03/08/2026 | o teste que prova a separação não é conferir a lista de arquivos: é clonar e rodar | [L665](../RETROSPECTIVAS.md#L665) | — |
| 229 | 03/08/2026 | a demonstração financeira só prova o que ela é obrigada a divulgar, e eu tratei o silêncio dela como prova | [L705](../RETROSPECTIVAS.md#L705) | — |
| 232 | 03/08/2026 | o cadastro respondia "existe"; era o TEOR que respondia "quanto", e eu declarei ao cliente que faltava ir aos autos sem ter tentado ler o teor | [L721](../RETROSPECTIVAS.md#L721) | — |
| 246 | 06/08/2026 | regra adotada carrega um lastro que pode deixar de existir | [L820](../RETROSPECTIVAS.md#L820) | — |
| 265 | 06/08/2026 | as regras lidas em e-mail exibiam lastro emprestado | [L913](../RETROSPECTIVAS.md#L913) | — |
| 270 | 06/08/2026 | o base64 corrompido não levanta exceção: decodifica em lixo e o anexo some da conferência | [L978](../RETROSPECTIVAS.md#L978) | ⚠ citada, mas o número é ambíguo |
| 277 | 06/08/2026 | a régua lexical não distingue modelos por conteúdo, e descobrir isso vale mais do que o número que ela dava | [L1016](../RETROSPECTIVAS.md#L1016) | — |
| 316 | 06/08/2026 | procurei a prova da entrega na pasta errada e quase inverti o diagnóstico; quem me pegou foi a lente adversarial | [L1084](../RETROSPECTIVAS.md#L1084) | — |
| 324 | 06/08/2026 | o resumo comeu a prova, e o censo acusou de mentira um trabalho que estava feito | [L1100](../RETROSPECTIVAS.md#L1100) | — |

<a id="autoengano"></a>
## Autoengano e autovalidação

14 lições.

| nº | data | lição | onde | o que a faz reprovar |
|---:|---|---|---|---|
| 39 | 09/07/2026 | Confrontar o sistema com a literatura vale a pena quando há filtro de saída forte | [L107](../RETROSPECTIVAS.md#L107) | — |
| 44 | 09/07/2026 | Review adversarial externo (Codex gpt-5.5, 09/07/2026 noite) pagou: 2 achados high reais que nenhum teste interno tinha pego | [L121](../RETROSPECTIVAS.md#L121) | — |
| 47 | 10/07/2026 | Auditor multi-agente também erra: verificação adversarial matou ~40% dos achados, e 2 "confirmados" caíram na checagem manual | [L129](../RETROSPECTIVAS.md#L129) | — |
| 1 | 23/07/2026 | Plano bom nasce reprovado | [L221](../RETROSPECTIVAS.md#L221) | ⚠ citada, mas o número é ambíguo |
| 93 | 03/08/2026 | Quem constrói não pode ser quem valida, e comitê que lê o resumo do construtor não escapa disso | [L382](../RETROSPECTIVAS.md#L382) | — |
| 100 | 03/08/2026 | Gate declarado não é gate computado; a casa escreveu a proteção certa e a deixou fora da estrada | [L396](../RETROSPECTIVAS.md#L396) | — |
| 129 | 03/08/2026 | Três quartos das execuções de um gate mediam o conjunto vazio | [L502](../RETROSPECTIVAS.md#L502) | — |
| 144 | 03/08/2026 | Cometi contra mim mesmo, no censo, o erro que já tinha documentado horas antes | [L532](../RETROSPECTIVAS.md#L532) | — |
| 145 | 03/08/2026 | A superfície de autovalidação chegou a zero, e é aí que começa o risco novo | [L534](../RETROSPECTIVAS.md#L534) | — |
| 148 | 03/08/2026 | O instrumento errou duas vezes na primeira execução, e as duas eram sobre o que ele NÃO alcançava | [L540](../RETROSPECTIVAS.md#L540) | — |
| 150 | 03/08/2026 | Gate que nunca aprova é tão quebrado quanto gate que nunca reprova | [L544](../RETROSPECTIVAS.md#L544) | — |
| 170 | 03/08/2026 | Um canário que não alcança o que o gate lê mede a própria cobertura | [L587](../RETROSPECTIVAS.md#L587) | — |
| 173 | 03/08/2026 | O cético do painel refutou uma medição fresca citando documentação antiga | [L593](../RETROSPECTIVAS.md#L593) | — |
| 316 | 06/08/2026 | procurei a prova da entrega na pasta errada e quase inverti o diagnóstico; quem me pegou foi a lente adversarial | [L1084](../RETROSPECTIVAS.md#L1084) | — |

<a id="sem-tema"></a>
## Sem tema atribuído pelo vocabulário

O vocabulário não alcançou estas. Não são lições piores — são as que ninguém classificou ainda, e ficam listadas para que a lacuna seja visível em vez de silenciosa.

107 lições.

| nº | data | lição | onde | o que a faz reprovar |
|---:|---|---|---|---|
| 7 | 08/07/2026 | gws autorizado para escrita | [L17](../RETROSPECTIVAS.md#L17) | — |
| 8 | 08/07/2026 | Retângulos cinza no topo direito da 1ª página são arte do template oficial | [L18](../RETROSPECTIVAS.md#L18) | — |
| 11 | 08/07/2026 | Meta-rótulos de produção | [L28](../RETROSPECTIVAS.md#L28) | — |
| 13 | 08/07/2026 | gws drafts | [L30](../RETROSPECTIVAS.md#L30) | — |
| 16 | 08/07/2026 | Aritmética de intervalos de datas deve ser recalculada pelo auditor | [L39](../RETROSPECTIVAS.md#L39) | forja_verificador.py |
| 17 | 08/07/2026 | Personas internas INTEIA vazam em documentos de cliente | [L41](../RETROSPECTIVAS.md#L41) | — |
| 25 | 08/07/2026 | Instrução de leitura funcionou: direção da tese veio correta dos autos | [L67](../RETROSPECTIVAS.md#L67) | — |
| 27 | 08/07/2026 | Numeração OAB em certidão do STJ vem no formato 'UF999999'; converter com fidelidade | [L71](../RETROSPECTIVAS.md#L71) | forja_anonimizar.py |
| 37 | 09/07/2026 | Agente que "transcreve" conteúdo para outra camada RESUME (5 de 5) | [L101](../RETROSPECTIVAS.md#L101) | forja_visual.py |
| 53 | 11/07/2026 | Presença de parecer não equivale a decisão favorável do conselho | [L143](../RETROSPECTIVAS.md#L143) | — |
| 55 | 11/07/2026 | Zero esperado não é completude; é ausência de avaliação | [L147](../RETROSPECTIVAS.md#L147) | — |
| 59 | 11/07/2026 | Auditor delegado também pode extrapolar o escopo de escrita | [L155](../RETROSPECTIVAS.md#L155) | — |
| 62 | 11/07/2026 | Reprovação silenciosa é meio caminho para aprovação de fato | [L163](../RETROSPECTIVAS.md#L163) | forja_delivery.py |
| 64 | 11/07/2026 | Diagnóstico útil é história causal e decisória, não inventário de defeitos | [L169](../RETROSPECTIVAS.md#L169) | — |
| 69 | 11/07/2026 | Indicador elegante deve revelar gargalo, não escondê-lo numa média | [L181](../RETROSPECTIVAS.md#L181) | — |
| 70 | 11/07/2026 | Teste antifraude precisa combinar mutação semântica e controle benigno | [L183](../RETROSPECTIVAS.md#L183) | — |
| 73 | 12/07/2026 | Score perfeito com um único matador é artefato, não qualidade; instrumento de medição valida a si mesmo contra o original antes de medir | [L193](../RETROSPECTIVAS.md#L193) | — |
| 74 | 12/07/2026 | Inversão por prefixo "não" atravessa qualquer teste `contains` | [L195](../RETROSPECTIVAS.md#L195) | — |
| 81 | 16/07/2026 | Projeto eliminado tem que sair do disco e do git, não só da documentação | [L213](../RETROSPECTIVAS.md#L213) | — |
| 3 | 23/07/2026 | Canário de falha única com atribuição por sensor | [L232](../RETROSPECTIVAS.md#L232) | ⚠ citada, mas o número é ambíguo |
| 4 | 23/07/2026 | O corpus histórico validou os sensores por acidente | [L237](../RETROSPECTIVAS.md#L237) | — |
| 2 | 23/07/2026 | Compress venceu expand na geração 0 | [L255](../RETROSPECTIVAS.md#L255) | — |
| 3 | 23/07/2026 | Gap de v1 descoberto em uso real: | [L260](../RETROSPECTIVAS.md#L260) | ⚠ citada, mas o número é ambíguo |
| 1 | 23/07/2026 | O vazamento de cegamento mais provável vem do ORQUESTRADOR, não do juiz | [L269](../RETROSPECTIVAS.md#L269) | ⚠ citada, mas o número é ambíguo |
| 2 | 23/07/2026 | Juiz LLM não rastreia artefato através do swap sem instrução explícita | [L275](../RETROSPECTIVAS.md#L275) | — |
| 3 | 23/07/2026 | Canários desentrelaçados da avaliação: | [L322](../RETROSPECTIVAS.md#L322) | ⚠ citada, mas o número é ambíguo |
| 85 | 26/07/2026 | Fonte primária não é revisão de texto, e nenhuma quantidade de revisão textual substitui abrir os autos | [L336](../RETROSPECTIVAS.md#L336) | — |
| 93 | 27/07/2026 | `--output-format json` devolve apenas o último turno | [L356](../RETROSPECTIVAS.md#L356) | — |
| 94 | 03/08/2026 | Detecção por cor quebra na primeira revisão da marca | [L384](../RETROSPECTIVAS.md#L384) | — |
| 105 | 03/08/2026 | "A ferramenta não está disponível" é conclusão que exige procurar pela coisa certa; e o validador de terceiro tem o escopo dele, não o seu | [L412](../RETROSPECTIVAS.md#L412) | — |
| 122 | 03/08/2026 | Revalidação depois da correção é parte da correção | [L462](../RETROSPECTIVAS.md#L462) | — |
| 123 | 03/08/2026 | Memória de auditabilidade também pode mentir por nome de fase | [L464](../RETROSPECTIVAS.md#L464) | — |
| 128 | 03/08/2026 | Scanner de fonte externa não pode escrever no lado da fonte | [L486](../RETROSPECTIVAS.md#L486) | — |
| 130 | 03/08/2026 | Exigir os nove do protocolo reprovaria o melhor relatório do acervo | [L504](../RETROSPECTIVAS.md#L504) | — |
| 131 | 03/08/2026 | O medidor de liveness dizia "inerte" para duas doenças diferentes | [L506](../RETROSPECTIVAS.md#L506) | — |
| 135 | 03/08/2026 | Os detectores certos estavam instalados tarde demais | [L514](../RETROSPECTIVAS.md#L514) | — |
| 137 | 03/08/2026 | Três regras "óbvias" sobre ingestão morreram na medição | [L518](../RETROSPECTIVAS.md#L518) | — |
| 139 | 03/08/2026 | O achado P0 mais assustador do dia era um defeito já corrigido | [L522](../RETROSPECTIVAS.md#L522) | — |
| 161 | 03/08/2026 | Forma de decisão também é contrato de entrada | [L566](../RETROSPECTIVAS.md#L566) | — |
| 163 | 03/08/2026 | Um padrão sem instrumento que o meça é uma intenção | [L572](../RETROSPECTIVAS.md#L572) | — |
| 166 | 03/08/2026 | O alarme caiu de 33 para 4, e nenhum dos 4 é petição | [L579](../RETROSPECTIVAS.md#L579) | — |
| 167 | 03/08/2026 | O escritório consertou sozinho, e isso é dado sobre o processo | [L581](../RETROSPECTIVAS.md#L581) | — |
| 174 | 03/08/2026 | Reprovei o padrão do dono pela terceira vez no mesmo dia, e desta vez cheguei a "corrigir" a peça | [L595](../RETROSPECTIVAS.md#L595) | — |
| 176 | 03/08/2026 | O erro que muda de vítima a cada execução não é de conteúdo | [L599](../RETROSPECTIVAS.md#L599) | — |
| 179 | 03/08/2026 | O conselho de quatro personas perdeu duas e o consolidador escreveu "o que os quatro concordam" | [L605](../RETROSPECTIVAS.md#L605) | — |
| 181 | 03/08/2026 | O canário anti-moldagem pagou o próprio custo em minutos | [L609](../RETROSPECTIVAS.md#L609) | — |
| 191 | 03/08/2026 | a porta é melhor que a proibição | [L629](../RETROSPECTIVAS.md#L629) | — |
| 201 | 03/08/2026 | a lição 200 estava errada na atribuição, e o erro tem causa estrutural | [L649](../RETROSPECTIVAS.md#L649) | — |
| 202 | 03/08/2026 | a automação que falha em silêncio some do mapa mental de todo mundo | [L651](../RETROSPECTIVAS.md#L651) | — |
| 203 | 03/08/2026 | laudo grande demais para ser lido é laudo que ninguém confere | [L653](../RETROSPECTIVAS.md#L653) | — |
| 205 | 03/08/2026 | antes de `filter-branch`, a tag de backup não é higiene: é a única cópia | [L657](../RETROSPECTIVAS.md#L657) | — |
| 206 | 03/08/2026 | um blob tem N caminhos; remover caminho não é remover blob | [L659](../RETROSPECTIVAS.md#L659) | — |
| 208 | 03/08/2026 | consolidar exclusão que não se entendeu é tão errado quanto restaurar o que foi limpo com razão | [L663](../RETROSPECTIVAS.md#L663) | — |
| 213 | 03/08/2026 | Drive bloqueado não é fim de linha: a conta logada no Chrome real resolve o que a API sem escopo não resolve | [L673](../RETROSPECTIVAS.md#L673) | — |
| 220 | 03/08/2026 | "não verifiquei" e "regressão" são coisas diferentes, e confundi-las corrói o instrumento | [L687](../RETROSPECTIVAS.md#L687) | — |
| 227 | 03/08/2026 | `write_text` no Windows traduz a quebra de linha, e um diff inflado esconde a mudança real | [L701](../RETROSPECTIVAS.md#L701) | — |
| 228 | 03/08/2026 | a rotina noturna que reprova por trabalho legítimo é a rotina que ninguém conserta | [L703](../RETROSPECTIVAS.md#L703) | — |
| 232 | 03/08/2026 | a rotina automática que não escreve como terminou é a rotina que falha em silêncio, de novo | [L711](../RETROSPECTIVAS.md#L711) | — |
| 234 | 03/08/2026 | `.git` vazio não é repositório, e é justamente por isso que engana | [L715](../RETROSPECTIVAS.md#L715) | — |
| 235 | 03/08/2026 | o que sai da pasta de trabalho sai também do alcance de todos os gates | [L717](../RETROSPECTIVAS.md#L717) | — |
| 237 | 06/08/2026 | o loop de aprendizado coletava 1.096 lições e promovia uma; a culpa era da porta, não de quem passa por ela | [L801](../RETROSPECTIVAS.md#L801) | — |
| 238 | 06/08/2026 | promova o padrão, não a ocorrência | [L803](../RETROSPECTIVAS.md#L803) | — |
| 239 | 06/08/2026 | o campo existia, o executor nunca foi escrito | [L805](../RETROSPECTIVAS.md#L805) | — |
| 242 | 06/08/2026 | a maior "correção do escritório" que eu media era ruído do meu próprio comparador | [L812](../RETROSPECTIVAS.md#L812) | — |
| 243 | 06/08/2026 | a pergunta que vem antes do diff: isto é revisão da nossa peça, ou é outro documento? | [L814](../RETROSPECTIVAS.md#L814) | — |
| 245 | 06/08/2026 | contar não é ler; sem comando de amostra, ninguém vê o ruído | [L818](../RETROSPECTIVAS.md#L818) | — |
| 248 | 06/08/2026 | o filtro certo é por quem manda, não por se veio anexo; e a conta era 45 contra 5 | [L825](../RETROSPECTIVAS.md#L825) | — |
| 249 | 06/08/2026 | registro que vive só no relatório da rodada não é registro | [L827](../RETROSPECTIVAS.md#L827) | — |
| 250 | 06/08/2026 | regra que já existia por escrito e continuou sendo violada: instrução não é gate | [L867](../RETROSPECTIVAS.md#L867) | — |
| 255 | 06/08/2026 | o destaque nascia da abertura do parágrafo, e o leitor lia a mesma frase duas vezes | [L877](../RETROSPECTIVAS.md#L877) | — |
| 257 | 06/08/2026 | gravei quatro linhas e o diff acusou 659 | [L881](../RETROSPECTIVAS.md#L881) | — |
| 260 | 06/08/2026 | os dois únicos comandos que gravavam eram os dois únicos que não falavam | [L888](../RETROSPECTIVAS.md#L888) | — |
| 255 | 06/08/2026 | o padrão mais recorrente do acervo não era sobre a peça: era sobre como dizemos que não conseguimos ler um documento | [L891](../RETROSPECTIVAS.md#L891) | — |
| 256 | 06/08/2026 | dizer o que faltou sem dizer o que foi lido não responde nada | [L893](../RETROSPECTIVAS.md#L893) | — |
| 257 | 06/08/2026 | a esteira escrevia como juiz, e o escritório queria advogado | [L895](../RETROSPECTIVAS.md#L895) | — |
| 259 | 06/08/2026 | 49 mensagens, 35 com lição, 14 sem: a proporção justifica ler tudo | [L899](../RETROSPECTIVAS.md#L899) | — |
| 261 | 06/08/2026 | erro de transporte lido como resposta do tribunal vira "não consta" | [L904](../RETROSPECTIVAS.md#L904) | — |
| 262 | 06/08/2026 | a fila de alto valor estava ordenada por um número que não era condenação | [L906](../RETROSPECTIVAS.md#L906) | — |
| 266 | 06/08/2026 | a camada do texto não é a camada do sistema | [L915](../RETROSPECTIVAS.md#L915) | — |
| 268 | 06/08/2026 | medir não é impedir, e a barreira tem de ficar onde a coisa passa | [L970](../RETROSPECTIVAS.md#L970) | — |
| 270 | 06/08/2026 | recurso que o agente não lembra que existe é recurso ausente, e a cura não é uma lista | [L974](../RETROSPECTIVAS.md#L974) | ⚠ citada, mas o número é ambíguo |
| 271 | 06/08/2026 | declarei irrecuperável o que estava desligado por uma linha nossa | [L976](../RETROSPECTIVAS.md#L976) | — |
| 272 | 06/08/2026 | o mesmo filtro precisava de duas sensibilidades, não de uma | [L982](../RETROSPECTIVAS.md#L982) | — |
| 273 | 06/08/2026 | dívida declarada não é alarme, e confundir as duas apaga as duas | [L984](../RETROSPECTIVAS.md#L984) | — |
| 274 | 06/08/2026 | a arqueologia era impossível por construção, e isso não aparecia em lugar nenhum | [L986](../RETROSPECTIVAS.md#L986) | — |
| 275 | 06/08/2026 | a resposta estava escrita e parou um passo antes de existir | [L988](../RETROSPECTIVAS.md#L988) | — |
| 281 | 06/08/2026 | o bloqueio declarado é uma afirmação sobre o mundo, e envelhece pior que qualquer outra | [L1004](../RETROSPECTIVAS.md#L1004) | — |
| 280 | 06/08/2026 | dezoito candidatos, dezoito vivos: o valor da varredura foi o que ela NÃO deixou apagar | [L1008](../RETROSPECTIVAS.md#L1008) | — |
| 275 | 06/08/2026 | o sistema sabia que tinha cortado o texto e não contou a quem ia trabalhar com ele | [L1012](../RETROSPECTIVAS.md#L1012) | — |
| 283 | 06/08/2026 | arquivo morto quase nunca é um arquivo; é um produtor que grava sempre | [L1018](../RETROSPECTIVAS.md#L1018) | — |
| 278 | 06/08/2026 | construí um subsistema inteiro que mandava documento de cliente para fora e a pergunta nunca apareceu | [L1020](../RETROSPECTIVAS.md#L1020) | ⚠ citada, mas o número é ambíguo |
| 279 | 06/08/2026 | li um parecer enquanto ele ainda estava sendo escrito e relatei como completo | [L1022](../RETROSPECTIVAS.md#L1022) | — |
| 290 | 06/08/2026 | A — o conserto da 290, e o que ele ensinou sobre logs | [L1038](../RETROSPECTIVAS.md#L1038) | — |
| 294 | 06/08/2026 | duas sessões trabalhando o mesmo caso produziram duas peças diferentes, e eu escrevi por cima da outra | [L1046](../RETROSPECTIVAS.md#L1046) | — |
| 295 | 06/08/2026 | o terceiro bloqueio falso do dia tinha a resposta escrita na seção de limites do próprio comando | [L1048](../RETROSPECTIVAS.md#L1048) | — |
| 298 | 06/08/2026 | a skill agora se confere sozinha, e é isso que a distingue de mais um documento | [L1054](../RETROSPECTIVAS.md#L1054) | — |
| 305 | 06/08/2026 | a skill mandava rodar o script errado, e o script errado sai com sucesso | [L1060](../RETROSPECTIVAS.md#L1060) | — |
| 309 | 06/08/2026 | a skill certa em cinco lugares, editada em um, e a cópia que ninguém sabe se está velha | [L1070](../RETROSPECTIVAS.md#L1070) | — |
| 311 | 06/08/2026 | o relatório do baseline dizia "0 falhas" em toda execução reprovada | [L1074](../RETROSPECTIVAS.md#L1074) | — |
| 312 | 06/08/2026 | `Path.write_text` reescreveu treze arquivos inteiros e quase entrou no commit | [L1076](../RETROSPECTIVAS.md#L1076) | — |
| 313 | 06/08/2026 | a fachada dizia "28 of 28 total" sobre 91 casos, e a demanda do topo da fila era um dos invisíveis | [L1078](../RETROSPECTIVAS.md#L1078) | — |
| 314 | 06/08/2026 | três leitores, três recortes, e nenhum deles avisando que era recorte | [L1080](../RETROSPECTIVAS.md#L1080) | — |
| 315 | 06/08/2026 | `fulfilled` queria dizer duas coisas incompatíveis, e foi isso que o titular sentiu como “deram por feito o que estava pela metade” | [L1082](../RETROSPECTIVAS.md#L1082) | — |
| 317 | 06/08/2026 | a raiz não estava em nenhum leitor: um escritor puxava toda a fábrica de volta para a primeira fase | [L1086](../RETROSPECTIVAS.md#L1086) | — |
| 319 | 06/08/2026 | o reparo preventivo do Word produziu um “documento defeituoso” que não existia | [L1090](../RETROSPECTIVAS.md#L1090) | — |
| 321 | 06/08/2026 | a esteira tinha seis arquivos prontos e respondeu que não dava para anexar | [L1094](../RETROSPECTIVAS.md#L1094) | — |
| 323 | 06/08/2026 | “o sistema saber que pode” é metade do trabalho, e tem teste próprio | [L1098](../RETROSPECTIVAS.md#L1098) | — |
