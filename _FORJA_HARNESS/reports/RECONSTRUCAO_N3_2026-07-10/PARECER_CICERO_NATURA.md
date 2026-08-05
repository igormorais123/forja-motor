# Parecer de auditoria adversarial — Estudo Natura/Cabreúva

**Data de corte:** 10 de julho de 2026  
**Gênero auditado:** estudo preliminar em tese para futuro parecer consultivo  
**Objeto:** verificar premissas, autoridades, cenários, resposta aos quesitos e limites do que pode ser afirmado, sem reescrever o estudo  
**Resultado:** **APROVEITÁVEL COMO ARQUITETURA INTERNA CONDICIONAL; BLOQUEADO COMO PARECER FINAL À CLIENTE**

## 1. Resultado jurídico direto

[FONTE] A versão atual da FORJA é substancialmente melhor que os estudos intermediários: corrige execução fiscal pela credora privada, penhora de receitas municipais, uso de mandado de segurança como cobrança, dispositivos trocados e improbidade por mera negligência. Também declara que a base fática está inacessível e responde aos sete quesitos por condições explícitas.

[FONTE] Apesar disso, o único anexo material recebido localmente contém apenas os sete quesitos. A pasta `Docs_Cabreuva_Escritorio` permanecia sem acesso na captura local examinada. Não há contrato, faturas, datas, manifestação da Procuradoria, reconhecimento da dívida, processo, valor, fonte de custeio ou histórico de cobrança.

[INFERÊNCIA] O estudo não pode concordar nem discordar da tese de não prescrição, atribuir violação concreta de princípios, recomendar medida específica ou estimar viabilidade no caso Natura. Ele pode apenas organizar os testes jurídicos e listar o que precisa ser provado. A própria linha 51 reconhece esse limite; outras passagens, porém, voltam a usar generalizações e graus de viabilidade sem base documental.

## 2. Cânone, fontes e estado real

### 2.1 Versões examinadas

- [FONTE] Pedido: `Natura Cabreúva - Parecer e Quesitos - prazo 20-07-2026/COMANDO_DO_EMAIL.md` e `Comandos e emails/EMAIL_ORIGINAL_TRANSCRITO.md`.
- [FONTE] Anexo direto: `Cabreúva - Quesitos Dr. Fábio Osório.docx`, SHA-256 `102640BA...BBB2`; a cópia com nome corrompido tem o mesmo hash.
- [FONTE] Fonte substantiva mais recente da FORJA: `_FORJA_HARNESS/state/case-email-natura-cabreuva-19f3991ebc75fe03/producao/ESTUDO_PRELIMINAR_NATURA_CABREUVA.md`.
- [FONTE] Edições DOCX/PDF e edição visual preservam, em grau alto, o conteúdo do Markdown. O estado identifica a edição visual como rascunho atual para revisão.
- [FONTE] Relatório interno: `producao/RELATORIO_MELHORIAS.md`.
- [FONTE] Estudos intermediários na pasta do caso: `ESTUDO_PRELIMINAR_EM_TESE.md`, `ESTUDO_PRELIMINAR_PROCURADORIA_CABREUVA.md`, `RESUMO_EXECUTIVO.md` e `MATRIZ_LACUNAS_E_RECOMENDACOES.md`.

### 2.2 Estado probatório

[FONTE] A captura `drive_access_probe/tmp_drive_natura.png` mostra pedido de acesso ao Google Drive, sem conteúdo da pasta.

[FONTE] O anexo direto repete apenas os sete quesitos; não contém narrativa fática, datas, documentos contratuais ou manifestação municipal.

[LACUNA] A instrução do e-mail exige análise minuciosa da documentação da cliente e veda erro de premissa fática. Essa etapa ainda não ocorreu.

[FONTE] O estado FORJA mantém o gate `ANEXOS_EXTERNOS_PENDENTES` como P1, mas o documento F3 registra “nenhuma lacuna bloqueante”. Há contradição entre o estado real e a liberação para redação.

[INFERÊNCIA] O acesso ao caderno documental é bloqueio para parecer conclusivo, embora não impeça a produção de um roteiro interno em tese.

## 3. Acertos da versão atual

1. [FONTE] A advertência metodológica informa, logo no início, que os fatos do caso não foram acessados e que o produto é condicional.
2. [FONTE] O Quesito 1 termina com a resposta correta para a base atual: não é possível concordar ou discordar da tese de não prescrição.
3. [FONTE] A versão atual remove a execução fiscal em favor da Natura e explica que dívida ativa é instrumento da Fazenda contra seus devedores, não do particular contra o Município.
4. [FONTE] A versão atual afasta penhora ordinária de bens e receitas municipais e organiza ação de cobrança/monitória, cumprimento contra a Fazenda e precatório/RPV por cenários.
5. [FONTE] O mandado de segurança é corretamente afastado como substituto da ação de cobrança, com apoio nas Súmulas 269 e 271 do STF.
6. [FONTE] Improbidade é condicionada a dolo específico e prova de deliberação; a mera inadimplência é expressamente considerada insuficiente.
7. [FONTE] Há matriz final de 12 lacunas documentais vinculadas aos quesitos afetados.
8. [FONTE] As Súmulas 150, 269, 271 e 383 do STF e a Súmula 339 do STJ possuem cópias locais no cache oficial, capturadas em 08/07/2026, com enunciados compatíveis com as transcrições do estudo.
9. [INFERÊNCIA] A escada de medidas, usada apenas como mapa interno e não como recomendação fechada, é uma estrutura útil para a futura análise de proporcionalidade e sequenciamento.

## 4. Achados críticos e materiais

### 4.1 P0 para o parecer final — ausência total dos fatos do caso

[FONTE] Não estão disponíveis localmente: contrato/aditivos, notas fiscais, comprovantes de entrega, vencimentos, cobranças, respostas do Município, reconhecimento do débito, manifestação da Procuradoria, processo judicial/administrativo, precatório, valor atualizado e documentos orçamentários.

[LACUNA] Sem esses documentos não se conhece a natureza da obrigação, o termo inicial, eventuais parcelas, suspensão/interrupção, regime licitatório, prova do adimplemento da Natura, causa do não pagamento ou conteúdo da tese municipal.

[INFERÊNCIA] Isso bloqueia respostas concretas aos sete quesitos. O estudo atual é um roteiro de investigação, não um parecer sobre a relação Natura–Cabreúva.

### 4.2 P0 para o parecer final — pesquisa oficial exigida não concluída

[FONTE] O comando exige repercussão geral, repetitivos, súmula vinculante, precedentes qualificados do STF, repetitivos do STJ e pesquisa em tribunais estaduais.

[FONTE] A versão atual confirma localmente apenas cinco súmulas. Ela própria mantém marcadores de verificação para prazo do enriquecimento sem causa contra a Fazenda e protesto contra ente público.

[FONTE] O `sourceLedger` do estado registra apenas Estatuto da OAB e LOMAN, sem relação substantiva com as respostas. Não há ledger de precedentes, leis, proposições ou trechos de suporte do caso Natura.

[LACUNA] Não há relatório local demonstrando a varredura de repercussão geral, repetitivos, súmulas vinculantes ou jurisprudência de outros TJs solicitada pelo cliente.

[INFERÊNCIA] As cinco súmulas podem permanecer como pontos já confirmados. As demais proposições devem ser tratadas como não verificadas até receberem fonte oficial, trecho e aderência.

### 4.3 P1 — separação fato/hipótese boa, mas não completa

[FONTE] A maior parte das premissas centrais usa “se... então” e indica documentação necessária.

[NÃO VERIFICADO] A linha 51 afirma, com base em “experiência”, que atos de reconhecimento são frequentes e costumam desconstituir alegações genéricas de prescrição. Não há amostra ou fonte.

[NÃO VERIFICADO] A linha 94 afirma que a ação monitória “costuma abreviar” a fase de conhecimento. A Súmula 339 confirma cabimento, não desempenho temporal.

[NÃO VERIFICADO] A linha 138 afirma que o acordo costuma ser o desfecho de melhor valor presente para credores de municípios médios. Não há classe de referência nem dados econômicos.

[NÃO VERIFICADO] A linha 143 diz que alegações genéricas de procuradorias municipais frequentemente não resistem ao escrutínio e atribui “viabilidade alta” ao reexame. Sem conhecer a manifestação da Procuradoria, não é possível calibrar essa viabilidade.

[NÃO VERIFICADO] A linha 147 afirma que a solução negociada melhora com alternância de gestão. Trata-se de hipótese política sem evidência do caso.

[INFERÊNCIA] Essas frases rompem a promessa do relatório interno de “zero fatos assumidos”. Devem ser removidas ou claramente convertidas em hipóteses a testar na reconstrução.

### 4.4 P1 — risco jurídico sem método explícito

[FONTE] O estudo usa “viabilidade alta”, “média”, “média-baixa” e “baixa”, mas não define critérios, drivers, confiança nem sinais de mudança.

[INFERÊNCIA] Em parecer consultivo, cada cenário deveria separar: chance jurídica, impacto para a cliente e confiança da análise. Aqui, a confiança deveria ser baixa enquanto os fatos estão inacessíveis, ainda que a regra geral seja conhecida.

[NÃO VERIFICADO] A pretensão de enriquecimento sem causa é classificada como viabilidade média enquanto o próprio texto reconhece conflito de prazo, subsidiariedade e falta de prova do proveito. Não é possível atribuir viabilidade antes de definir termo inicial, causa jurídica e jurisprudência aplicável.

### 4.5 P1 — pontos jurídicos residuais que exigem correção ou fonte

#### Prescrição e notificação

[FONTE] A linha 126 atribui à notificação formal efeito de interrupção com base no Código Civil, art. 202, III e VI, “conforme o instrumento”. O inciso VI trata de ato inequívoco do **devedor** que reconhece o direito; uma notificação unilateral do credor não é, por si, reconhecimento municipal.

[NÃO VERIFICADO] A aplicação do inciso III, o efeito de protesto contra a Fazenda e a relação entre interrupção civil, suspensão administrativa e os arts. 8º e 9º do Decreto 20.910/1932 precisam de fonte oficial e jurisprudência aderente. O estudo não deve prometer interrupção como efeito automático da notificação.

#### Princípios e responsabilização

[INFERÊNCIA] Inadimplemento de obrigação válida pode contrariar legalidade contratual e boa-fé, mas não prova automaticamente violação simultânea de moralidade, eficiência, transparência, ordem cronológica ou equilíbrio econômico-financeiro. Cada princípio depende da natureza do crédito e de conduta concreta.

[LACUNA] Não há prova de pagamentos posteriores a outros credores, dolo específico, quebra da ordem cronológica, omissão contábil ou fonte federal de recursos.

[NÃO VERIFICADO] A afirmação de que o TCE-SP poderá produzir multa, rejeição de contas e reflexos de inelegibilidade precisa distinguir contas do prefeito, atos de gestão, competência da Câmara e condições da LC 64/1990.

#### Vias institucionais

[NÃO VERIFICADO] O uso da CF, art. 74, § 2º, “por simetria” para denúncia ao TCE-SP precisa ser substituído ou confirmado pela base estadual/regimental específica.

[NÃO VERIFICADO] A intervenção estadual por dívida fundada ou descumprimento de ordem judicial é medida excepcional; o estudo não possui precedente ou fato que autorize tratá-la como mecanismo real deste crédito.

[NÃO VERIFICADO] A possibilidade de o MP-SP firmar compromisso de ajustamento com cronograma de pagamento de dívida privada depende do objeto coletivo, da legalidade do acordo e do papel institucional do MP; não pode ser apresentada como sucedâneo de cobrança sem essa análise.

#### Atualização e alternativas pós-prescrição

[NÃO VERIFICADO] O estudo identifica a EC 113/2021 como “parâmetro constitucional vigente”, mas simultaneamente manda conferir a redação na versão final. O regime temporal de juros/correção deve ser verificado na data do parecer e conforme a natureza e o período do crédito.

[NÃO VERIFICADO] Enriquecimento sem causa não pode ser usado automaticamente para reconstruir, com outro nome, a mesma pretensão contratual já prescrita. A autonomia da causa, o termo inicial, a subsidiariedade do art. 886 e o prazo contra a Fazenda devem ser demonstrados.

[INFERÊNCIA] A solução negociada para dívida prescrita exige fundamento público específico, disponibilidade jurídica, autorização e motivação do gestor. A referência civil à obrigação natural não basta para autorizar pagamento por Município.

### 4.6 P1 — cenários ainda não são exaustivos nem personalizados

[FONTE] O estudo usa três ramos: contrato administrativo, título judicial e fornecimento sem contrato formal válido.

[INFERÊNCIA] A árvore é útil, mas pode não cobrir todas as qualificações possíveis do crédito, como indenização por rescisão, reconhecimento administrativo, termo de ajuste, restituição, decisão arbitral ou obrigação parcelada. O caderno real deve definir a causa antes de escolher o ramo.

[LACUNA] Não existe cronologia parcela a parcela, valor, data de exigibilidade, evento interruptivo/suspensivo nem tese exata da Procuradoria. Portanto, nenhum cenário pode receber probabilidade ou recomendação de via.

### 4.7 P1 — risco de versão errada

[FONTE] Os arquivos intermediários na pasta do caso continuam acessíveis e não possuem marca inequívoca de “superado”. Eles contêm erros que o relatório de melhorias reconhece ter corrigido: execução fiscal pela Natura, penhora de FPM/receitas, mandado de segurança como cobrança, improbidade por negligência, compensação de crédito prescrito e acordo político de 80%.

[INFERÊNCIA] Enquanto essas versões não forem claramente segregadas no futuro fluxo, há risco de alguém reutilizar trechos juridicamente rejeitados. Esta auditoria não altera esses arquivos por determinação expressa.

### 4.8 P1 — QA e edição visual apresentam conflitos

[FONTE] O `F7_VERIFICADOR_FORJA.json` informa zero achados, embora o texto contenha marcadores de verificação e pesquisa oficial pendente. O verificador não testou profundidade de fonte nem conclusão fática.

[FONTE] O replay N3 encontrou 21 achados nos dois SVGs Natura: texto fora do quadro, sobreposições, conectores cruzando texto, atributo SVG inválido e forma cobrindo conteúdo. Isso conflita com `RETORNO.json`, que declarava os diagramas validados.

[FONTE] O e-mail de resposta diz que o material já entrega “critério completo” e “mapa realista”, linguagem mais forte do que o estado probatório permite.

## 5. Resposta aos sete quesitos: grau de atendimento atual

| Quesito | Atendimento atual | O que falta para resposta ao cliente |
|---|---|---|
| 1. Prescrição | [FONTE] critério geral organizado; conclusão corretamente recusada | contrato/título, parcelas, exigibilidade, cobranças, reconhecimento, tese da Procuradoria e pesquisa oficial |
| 2. Princípios | [INFERÊNCIA] lista de princípios em tese | fato específico que demonstre incidência de cada princípio e regime contratual aplicável |
| 3. Consequências | [INFERÊNCIA] mapa amplo, mas excessivo para os fatos disponíveis | prova de ordem de pagamentos, dolo, dano, contas e conduta do gestor |
| 4. Mecanismos | [FONTE] vias gerais corrigidas | natureza e liquidez do crédito, título, alçada, prova escrita, prescrição e estratégia de custo |
| 5. Órgãos | [INFERÊNCIA] instituições mapeadas | competência concreta, legitimidade, objeto da representação e fonte estadual/regimental |
| 6. Estratégias | [INFERÊNCIA] sequência abstrata útil | objetivo da cliente, valor, urgência, tolerância reputacional, fatos e resposta municipal |
| 7. Alternativa se prescrita | [LACUNA] opções listadas, mas nenhuma viabilidade comprovada | causa autônoma, prazo, subsidiariedade, autorização para acordo e precedentes oficiais |

## 6. O que pode e o que não pode ser afirmado

### Pode ser afirmado agora

- [FONTE] A cliente formulou sete quesitos sobre prescrição, princípios, consequências, cobrança, controle, estratégia e alternativas.
- [FONTE] A documentação fática da pasta compartilhada não estava acessível na evidência local examinada.
- [FONTE] Sem título executivo, ação de cobrança ou monitória podem ser hipóteses; havendo título judicial, o regime é cumprimento contra a Fazenda, precatório/RPV e regras próprias.
- [FONTE] Mandado de segurança não substitui ação de cobrança, conforme Súmulas 269 e 271 do STF.
- [FONTE] Ação monitória é cabível contra a Fazenda, conforme Súmula 339 do STJ.
- [FONTE] A execução prescreve no mesmo prazo da ação, conforme Súmula 150 do STF; a aplicação concreta depende do título e da cronologia.
- [FONTE] A contagem após interrupção no regime do Decreto 20.910 exige atenção à Súmula 383 do STF.

### Não pode ser afirmado agora

- [NÃO VERIFICADO] Que o crédito da Natura não está prescrito ou está prescrito.
- [NÃO VERIFICADO] Que o Município reconheceu a dívida, quebrou ordem cronológica, agiu dolosamente ou provocou a prescrição.
- [NÃO VERIFICADO] Que os sete princípios foram concretamente violados.
- [NÃO VERIFICADO] Que improbidade, crime de responsabilidade, ação popular, intervenção, TCE ou MP são medidas cabíveis neste caso.
- [NÃO VERIFICADO] Que enriquecimento sem causa possui viabilidade média ou prazo autônomo ainda aberto.
- [NÃO VERIFICADO] Que negociação é o melhor valor presente, que alternância de gestão melhora a solução ou que exposição pública é conveniente.
- [NÃO VERIFICADO] Qual atualização monetária, alçada de RPV, foro, procedimento ou custo se aplica ao crédito concreto.

## 7. Condições da futura reconstrução

1. [LACUNA] Acessar e inventariar integralmente a pasta da cliente.
2. [FONTE] Construir matriz fato–documento–página e cronologia parcela a parcela.
3. [FONTE] Reproduzir integralmente a manifestação da Procuradoria e decompor termo inicial, regime, fatos e autoridades usados por ela.
4. [FONTE] Definir a natureza jurídica do crédito antes de escolher ação, prescrição ou órgão.
5. [FONTE] Criar ledger de cada lei, súmula, tema, repetitivo e precedente com fonte oficial, proposição, trecho e aderência.
6. [FONTE] Executar a pesquisa qualificada exigida no e-mail: STF, STJ e TJs, registrando também quando não houver tema aplicável.
7. [INFERÊNCIA] Calibrar cada opção por chance jurídica, impacto, confiança, custo, prazo e gatilhos de reversão; não usar adjetivo de viabilidade sem método.
8. [FONTE] Responder diretamente cada quesito, distinguindo conclusão, condição, melhor objeção e documento que a sustenta.
9. [FONTE] Refazer QA jurídico e visual sobre a mesma versão final e invalidá-lo após qualquer alteração.

## 8. Red Team

[INFERÊNCIA] A melhor posição do Município será: prescrição consumada conforme o termo inicial adotado pela Procuradoria; ausência de causa interruptiva válida; eventual nulidade da contratação; restrição orçamentária; inexistência de quebra comprovada da ordem cronológica; impossibilidade de cobrança por vias de controle ou responsabilização pessoal sem dolo e prova.

[INFERÊNCIA] A melhor posição da Natura dependerá de: crédito válido e comprovado, cronologia individualizada, ato inequívoco de reconhecimento ou causa legal de suspensão/interrupção, recebimento da prestação pelo Município, manifestação municipal contraditória e eventual quebra documentada da ordem de pagamentos. Nenhum desses elementos está hoje no acervo local.

## 9. Conclusão

**Status Cícero:** **ALERTA INTERNO / BLOQUEADO COMO PARECER FINAL.**  
**Destino permitido:** roteiro interno de investigação e arquitetura de perguntas.  
**Destino vedado:** envio à Natura como resposta conclusiva aos quesitos ou uso para medida judicial, representação ou pressão política.  
**Condição de liberação:** acesso documental integral, cronologia do crédito, pesquisa oficial completa, correção dos pontos residuais, remoção de generalizações empíricas, calibração de risco e novo QA jurídico/visual.
