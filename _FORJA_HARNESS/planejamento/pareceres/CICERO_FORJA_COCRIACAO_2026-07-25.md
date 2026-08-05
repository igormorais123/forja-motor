# Parecer jurídico — FORJA-COCRIACAO-v1

**Objeto:** `33_PRD`, `34_TDD`, `35_ROADMAP`, e a questão suscitada no parecer estratégico sobre a separabilidade entre J-B(acordo) e J-B(julgador).
**Natureza:** parecer consultivo interno. Não é peça, não é destinado a protocolo, não contém opinião sobre caso concreto de cliente.
**Data de corte:** 2026-07-25.
**Veredito:** **APROVADO COM UMA RESSALVA BLOQUEANTE.**

> ## CORREÇÃO DE 2026-07-25, MESMO DIA — a ressalva nº 1 caiu
>
> **Conferi na fonte. O art. 343-A do RISTJ existe e está vigente.** Introduzido pela **Emenda Regimental nº 53, de 30 de junho de 2026**, publicada no DJe de 1º de julho de 2026 e vigente desde então. Texto verbatim e proveniência em `cache/fontes_oficiais/RISTJ_ART_343A_ER53_2026.md`.
>
> **Eu estava errado no argumento estrutural.** Sustentei implausibilidade porque o art. 343 trata de precatórios. Não se confirmou: o dispositivo foi inserido em disposições gerais. A busca local nada retornava porque o `REGIMENTO_INTERNO_STJ.md` arquivado está consolidado até a ER 47/2024, com as ER 48 a 53 apenas listadas ao final, sem texto incorporado ao corpo.
>
> **A determinação do escritório estava correta e bem informada.** A emenda entrou em vigor em 01/07/2026; a determinação do titular veio em 07/07/2026, seis dias depois. Não há citação fictícia, não há exposição do art. 34, XIV, do Estatuto, e não há varredura retroativa a fazer. **R1 a R4 ficam prejudicados.**
>
> **O que sobrevive, em forma menor e real:** o art. 343-A obriga apenas **iniciais de ações originárias e petições de recurso dirigidas ao STJ**. O protocolo manda a síntese executiva em toda peça, de qualquer tribunal — correto como prática. Mas **citar o dispositivo em peça ao TJTO, TRF1 ou TRF4 é invocar norma que não rege aquele tribunal.** A prática vale em todo lugar; a etiqueta numérica, só no STJ. E no STJ ela deixa de ser estilo: é dever regimental.
>
> **R5 permanece e ganha força:** o gate de citação regimental não conferida teria resolvido isto em segundos, nos dois sentidos. Acrescento **R14**: atualizar os `REGIMENTO_INTERNO_*.md` das pastas de caso, incorporando as emendas ao corpo em vez de listá-las ao final — a desatualização foi a causa material do falso alarme.
>
> Registro sem atenuar: levantei um P0 e ele não se confirmou. O procedimento funcionou — bloqueio reversível, verificação barata, correção no mesmo dia. Foi o custo que a regra "fonte oficial ou silêncio" existe para pagar.

---

## 1. Resultado jurídico direto

1. O tratamento de precedentes do plano está **juridicamente correto** e é superior ao que existe hoje na esteira. A correção central — aderência governa a operação, não a força — é a leitura certa dos arts. 489, §1º, V e VI, e 927, §§1º a 4º, do CPC.
2. **J-B(acordo) é separável de J-B(julgador)**, e por razão mais forte do que a apontada no parecer estratégico: não é diferença de grau de risco, é diferença de **veículo processual**. Um tem; o outro não tem.
3. **Ressalva bloqueante nº 1, alheia ao plano e mais grave que ele:** a expressão *"art. 343-A do RISTJ"*, que o protocolo do escritório manda usar em toda peça, **não encontra correspondência no regimento arquivado**, e está chegando ao corpo de documentos como citação regimental. Ver §4.
4. **Ressalva bloqueante nº 2, interna ao plano:** o PRD `33` **eliminou do escopo** a triagem de conflito, sigilo e perímetro, que constava como lacuna G18 no documento `30` e como recomendação no `32`. O plano simultaneamente cria um corpus documental de múltiplos clientes (RF-7). Criar o corpus sem o perímetro é a ordem inversa da correta.

---

## 2. Estado real, cânone e lacunas

Cânone examinado: `33_PRD` (requisitos), `34_TDD` (payloads e invariantes), `35_ROADMAP` (portões), com os antecedentes `29`, `30`, `31` e `32`.

**Verificação executada nesta análise** — não por memória:

| Objeto | Resultado |
|---|---|
| `REGIMENTO_INTERNO_STJ.md` na pasta Cafelana | **Art. 343 trata de precatórios de requisição de pagamento.** Nenhuma ocorrência de "343-A" no arquivo. |
| Ocorrências de "343-A" no acervo da fábrica | **Todas** em produção nossa (`autoresearch/`), nenhuma em fonte regimental. |
| Uso na forma de citação | Confirmado em cabeçalho de peça: `### 3.1 Síntese Executiva (art. 343-A RISTJ)` — a referência está entrando no corpo do documento, não apenas no roteiro interno. |
| `CONTENT_CLASSES`, `CONTRIBUTION_ORIGINS`, `CONTRIBUTION_STATUS` em `forja_learning.py` | existem, conforme afirmado no PRD |

**Lacunas declaradas.** Não confirmei se emenda regimental posterior à consolidação do arquivo criou dispositivo 343-A; a consolidação disponível vai até ER 47/2024 com anotação de ER 48 a 53. A implausibilidade é estrutural — artigo inserido por letra permanece no capítulo do artigo-base, e o art. 343 está em matéria de precatórios —, mas implausibilidade não é prova. **A conferência na fonte oficial é obrigatória e não pode ser substituída por este parecer.**

---

## 3. Precedentes: o que o plano acertou e o que precisa de ajuste fino

### 3.1 Acertos

**RF-5.6 está correto.** Diante de precedente vinculante com moldura fática diversa, as operações são delimitar alcance, distinguir ou sustentar superação. Não existe "rebaixamento" de precedente vinculante por baixa similaridade fática — a vinculação é regime, e a similaridade define qual operação se abre. O art. 927, §1º, remete expressamente ao art. 489, §1º, e o inciso VI exige, de quem se afasta do precedente invocado, a demonstração de **distinção** ou de **superação**. O plano espelha a estrutura legal.

**RF-5.5 é a melhor regra do conjunto.** Precedente sem operação declarada não é citado. É a tradução exata do art. 489, §1º, V: não basta invocar o julgado; é preciso identificar os fundamentos determinantes e demonstrar o ajuste do caso a eles. Operação declarada é a forma verificável desse ônus.

**RF-5.8 está bem calibrada** na redação do documento `32`, que preferi à minha própria formulação anterior: ratio não se extrai de ementa **quando a íntegra for necessária para sustentar a proposição**. Ementa serve à descoberta e a descrição limitada, identificada como tal. A regra absoluta seria excessiva e geraria bloqueio de casos legítimos.

### 3.2 Ajustes recomendados

**A1 — A inversão do art. 489 sobre nós mesmos precisa ser nomeada corretamente.**
O art. 489, §1º, é dever de **fundamentação do juiz**, não do advogado. O plano faz coisa metodologicamente excelente — antecipar o padrão pelo qual a decisão será medida —, mas o artefato interno deve registrar isso como **ônus argumentativo da parte, derivado reflexivamente do dever do julgador**, e não como dever legal próprio. O dever do advogado tem outra sede: boa-fé e lealdade processual (art. 77 do CPC) e o Estatuto e o Código de Ética. A distinção evita que um artefato interno mal lido produza, na peça, a afirmação de que a parte "cumpre o art. 489", que é erro categorial.

**A2 — "Vinculante" também é convenção operacional, e não só "persuasivo qualificado".**
O TDD trata "persuasivo qualificado" como convenção interna a ser identificada como tal — correto. Falta simetria: **a força vinculante dos incisos do art. 927 não é pacífica em toda a extensão**. Súmula vinculante e controle concentrado vinculam por dispositivo constitucional; repetitivos, IRDR e IAC têm regime próprio de observância; enunciados de súmula simples e orientação do plenário ou órgão especial recebem tratamento doutrinário e jurisprudencial menos uniforme.

Consequência prática: escrever em peça *"trata-se de precedente vinculante"* onde há controvérsia é **abrir flanco**. Recomendo que o campo `regime` registre **a base normativa e o efeito**, e que a peça afirme o efeito com o dispositivo, não com o rótulo. `regime.tipoAutoridade` deve ser identificado como convenção da FORJA em **todas** as suas categorias, não apenas na intermediária.

**A3 — `vigencia` precisa distinguir três estados que o TDD funde em um.**
Superação, modulação e afetação posterior produzem efeitos distintos: o precedente superado perde a razão de decidir; o modulado a conserva com recorte temporal (art. 927, §3º); o afetado por tema posterior permanece íntegro, mas sob risco. Fundi-los em `vigencia` faz perder a informação que decide o uso. Recomendo enum de quatro estados — `vigente`, `modulado`, `superado`, `afetado_por_tema_posterior` — com campo próprio para o marco temporal da modulação.

**A4 — Falta o registro do precedente contrário conhecido.**
O art. 489, §1º, VI, opera quando o precedente é **invocado pela parte**. Espelhando: se conhecemos precedente contrário e não o enfrentamos, entregamos ao adversário o argumento e ao julgador a via curta de indeferimento. O `anchorProfile` tem `distinguishingAdversario`, que é o passo seguinte. Falta o passo anterior: **`precedenteContrarioConhecido[]`**, com a operação que pretendemos opor. Sem ele, a auditoria não distingue "não existe contrário" de "não procuramos". O campo `negativeResult` do `source_ledger` resolve metade do problema; esta é a outra metade.

---

## 4. Ressalva bloqueante nº 1 — a citação regimental

**Situação.** O protocolo da fábrica determina, para toda peça e todo tribunal, "síntese executiva estilo art. 343-A do RISTJ", com origem declarada em determinação do titular por e-mail de 07/07/2026. A taxonomia de falhas da própria disciplina jurídica interna já classifica *"art. 343-A do RISTJ"* como bloqueio P0 por fundamento regimental fictício. Há, portanto, **contradição viva entre dois documentos internos**, e a produção real vem seguindo o primeiro.

**Gravidade.** O conteúdo da prática é irretocável: síntese executiva no início da peça reduz esforço do julgador e é exatamente o que o titular pediu na entrevista. **O problema não é a prática — é a etiqueta.** Uma peça que escreve `Síntese Executiva (art. 343-A RISTJ)` afirma ao órgão julgador a existência de um dispositivo regimental. Se ele não existe com esse conteúdo, tem-se citação de norma inexistente em documento protocolado, com exposição no art. 34, XIV, do Estatuto da Advocacia — deturpar o teor de dispositivo — e, pior que a exposição disciplinar, o efeito que o próprio titular nomeou na entrevista: **desmoralização**. Ele disse que pesquisa falsa desmoraliza a ferramenta e quem a usa. Uma citação regimental falsa, repetida em todas as peças, é a forma mais eficiente de provar-lhe que ele estava certo.

**Recomendações:**

**R1.** Abrir o RISTJ na fonte oficial, na versão vigente com as emendas de 2026, e confirmar se existe dispositivo 343-A e qual o seu conteúdo. Prazo: imediato, antes da próxima peça.
**R2.** Enquanto não confirmado, **remover a referência numérica do corpo de qualquer peça**. Escrever "Síntese executiva" sem citação regimental. A prática permanece integralmente; some apenas a etiqueta.
**R3.** Se confirmada a inexistência, executar varredura retroativa nas peças já protocoladas desde 07/07/2026, classificar o alcance e decidir, com o titular, sobre eventual correção. É decisão dele, não nossa.
**R4.** Corrigir o `CLAUDE.md` da fábrica para descrever a prática sem a citação, e registrar a origem correta: é determinação do escritório, e a autoridade dela não depende de dispositivo regimental nenhum.
**R5.** Incluir no `forja_verificador.py` gate P0 de **citação regimental não conferida**: todo "art. X do RI\<Tribunal>" no texto final exige entrada correspondente no ledger de fontes com trecho literal. Este gate pertence ao plano e deve entrar na Onda 0.

---

## 5. Ressalva bloqueante nº 2 — sigilo, conflito e perímetro

O documento `30` levantou a lacuna G18. O `32` a manteve como agregado necessário. O **PRD `33` a eliminou do escopo** e, no mesmo documento, criou o `IDENTITY_CORPUS_MANIFEST.jsonl`, que inventaria peças de múltiplos clientes com hash e proveniência.

**Por que a ordem importa juridicamente.** O sigilo profissional é dever do advogado e direito do cliente — inviolabilidade prevista no art. 7º, II, do Estatuto, infração no art. 34, VII, e disciplina própria no Código de Ética. Constituir um repositório transversal de peças de clientes distintos, para fim de calibração de estilo, é tratamento de material sob sigilo com finalidade diversa daquela para a qual foi produzido. Não é proibido; é **condicionado**.

Distingo dois objetos que o plano funde:

- **Padrão de forma** — ordem das seções, ritmo, densidade de citação, movimento argumentativo. Não é informação do cliente. Extrair e reter isso é inofensivo.
- **Conteúdo** — fatos, partes, valores, estratégia. É do cliente. Reter isso num corpus transversal é o que exige base e perímetro.

**Recomendações:**

**R6.** Restabelecer no escopo, na Onda 0, um artefato mínimo de **perímetro por documento**: classificação de sigilo, presença de segredo de justiça, dados pessoais sensíveis e o que pode ser processado fora do caso de origem. Não precisa ser a triagem completa de conflito de interesses proposta no `30`; precisa existir antes do corpus.
**R7.** O corpus de identidade retém **padrão, não conteúdo**. `IDENTITY_CORPUS_MANIFEST.jsonl` guarda hash, atribuição e metadado; os padrões extraídos são estruturais e anonimizados; **excerto literal de peça de cliente não é armazenado** fora da pasta do próprio caso.
**R8.** Documento sob segredo de justiça fica fora do corpus, sem exceção configurável.
**R9.** A consulta ao advogado é documento sob sigilo profissional e segue o mesmo perímetro. O RF-2.7, que proíbe envio autônomo, está correto e deve ser lido também sob esta ótica: a allowlist é de destinatários internos.

---

## 6. J-B(acordo) e J-B(julgador): a separação e o seu fundamento

O parecer estratégico separou os dois por perfil de risco e registrou dúvida honesta na contra-hipótese 2 — se a separação não seria cosmética, já que ambos operam o mesmo motor de constrangimento. **A separação se sustenta, mas não pelo motivo apresentado.**

### 6.1 J-B(julgador) — o problema não é o risco, é a ausência de destino

A alegação de parcialidade de magistrado tem **veículo processual próprio e taxativo**: impedimento e suspeição, arts. 144 a 148 do CPC. As hipóteses de suspeição do art. 145 são de rol fechado — amizade íntima, inimizade, interesse no julgamento, relação de crédito ou débito, entre outras. **Divergência estatística de entendimento não figura em nenhuma delas.** Nem poderia: o art. 41 da Lei Complementar 35/1979 protege o magistrado de ser prejudicado pelas opiniões que manifestar ou pelo teor das decisões que proferir, salvo excesso de linguagem.

Consequência: um achado jurimétrico sobre comportamento de julgador, levado "aos autos" — expressão da entrevista —, **não tem onde pousar**. Fora da exceção de suspeição, vira imputação gratuita, com exposição de litigância de má-fé (art. 80 do CPC), de infração disciplinar e, conforme a formulação, de ilícito penal contra a honra. Some-se a isso o art. 12, §2º, da Lei 13.709/2018: dado que possa formar **perfil comportamental de pessoa natural identificada** é dado pessoal, e a decisão judicial ser pública não torna pública a construção do perfil.

Não é, portanto, questão de "alto risco a ser autorizado". É questão de **inexistência de via**. A contenção do plano deve ser reescrita nesses termos: J-B(julgador) produz insumo de **estratégia interna** — escolher tese, escolher via, calibrar expectativa — e **jamais produz alegação dirigida ao órgão**. Com essa redação, o módulo deixa de ser radioativo e passa a ser simplesmente interno.

### 6.2 J-B(acordo) — tem veículo, tem base e tem sujeito diferente

O objeto da análise é uma **proposta**, não uma pessoa. E o ordenamento não só admite como estrutura o argumento de vantajosidade:

- **LINDB, art. 20** (redação da Lei 13.655/2018): não se decidirá com base em valores jurídicos abstratos sem consideração das consequências práticas. Comparação objetiva de deságios em situações análogas é precisamente consequência prática documentada.
- **Lei 13.140/2015, arts. 32 a 40**: autocomposição envolvendo a Administração Pública e câmaras de prevenção e resolução de conflitos.
- **Lei 14.133/2021**: meios alternativos de prevenção e resolução de controvérsias em contratação pública.
- **Lei 8.429/1992, art. 17-B**, na redação da Lei 14.230/2021: o acordo de não persecução civil exige demonstração de adequação e vantajosidade — a análise comparativa é insumo natural desse juízo.

Há veículo, há base e o sujeito da análise não é pessoa identificada. **Separação confirmada.**

### 6.3 O veto que a separação exige

A dúvida do parecer estratégico está certa num ponto preciso, e é onde eu imponho veto.

A formulação da entrevista — *"se houver uma recusa, vejam, de repente o gestor público pode ser responsabilizado perante o Tribunal de Contas da União"* — dirigida ao próprio gestor, **muda a natureza do ato**. Deixa de ser demonstração de vantajosidade e passa a ser advertência pessoal sobre consequência funcional. É intimidação, ainda que polida, e é contraproducente antes de ser irregular: gestor advertido não transige, porque transigir depois da advertência parece ceder a ela — e ceder a ameaça é, para ele, risco maior do que não transigir.

**R10.** J-B(acordo) é **autorizado** para produzir demonstração comparativa de vantajosidade, com metodologia, universo, janela e limitações declaradas.
**R11.** **Vedada** a formulação que enderece ao agente público consequência funcional pessoal. O dever de buscar a solução vantajosa pode ser invocado como **fundamento jurídico impessoal**; a responsabilização pessoal do gestor não entra em manifestação dirigida a ele.
**R12.** J-B(julgador) é **redefinido** como insumo estritamente interno de estratégia, com vedação absoluta de compor alegação, petição, representação ou manifestação. Não é matéria de autorização caso a caso: é vedação de saída.
**R13.** Ambos exigem, antes de qualquer uso, que a base comparativa seja composta por dados de acesso legítimo, com origem registrada, e que a peça jamais revele proveniência operacional do insumo — o protocolo de 11/07 já rege isso.

---

## 7. Risco e sinais de reversão

| Risco | Sinal de que se materializou | Reversão |
|---|---|---|
| Citação regimental fictícia em peça protocolada | conferência na fonte oficial não localiza o dispositivo | R2 e R3, com decisão do titular sobre alcance retroativo |
| Corpus de identidade formado antes do perímetro | manifesto criado sem classificação de sigilo por documento | suspender o corpus até o R6; nenhum trabalho perdido, apenas adiado |
| Rótulo "vinculante" atacado pelo adversário | contrarrazões que discutem o regime em vez do mérito | A2: afirmar o efeito pelo dispositivo, não pelo rótulo |
| Achado jurimétrico vaza para peça | qualquer menção a comportamento de julgador em texto externo | R12 é vedação de saída, verificável por gate lexical no `forja_verificador.py` |
| Precedente contrário não enfrentado | decisão que indefere invocando julgado que não tratamos | A4: `precedenteContrarioConhecido[]` |

**Onde eu posso estar errado.** Sobre o art. 343-A, minha conclusão é de forte implausibilidade estrutural, não de inexistência provada: o arquivo consolidado pode estar defasado em relação a emenda recente. Se o dispositivo existir com conteúdo compatível, R2 a R4 caem e permanece apenas R5, que é bom em qualquer cenário. **A verificação custa dez minutos e resolve.**

---

## +1. Próximo ato

1. **Conferir o art. 343-A na fonte oficial do STJ.** Prazo: antes da próxima peça. É o ato de maior relação entre custo e consequência de todo este conjunto de documentos.
2. Suspender a referência numérica no corpo das peças até a conferência.
3. Incluir no PRD `33`, como requisito de Onda 0: perímetro por documento (R6 a R8), gate de citação regimental (R5), estados de vigência (A3) e `precedenteContrarioConhecido[]` (A4).
4. Reescrever o item de jurimetria do PRD `33`, §5, nos termos de R10 a R12: J-B(acordo) autorizado com veto de formulação; J-B(julgador) redefinido como insumo interno com vedação de saída.
5. Registrar no `35`, §6, a pergunta de aceite correspondente: *nenhum achado sobre comportamento de julgador pode compor texto externo*.

O plano é bom. A urgência, hoje, está fora dele: três documentos de arquitetura foram escritos enquanto uma citação regimental provavelmente inexistente segue entrando em peças protocoladas. Fundamentação que não se confere não é fundamentação — é aposta com a assinatura de outra pessoa.
