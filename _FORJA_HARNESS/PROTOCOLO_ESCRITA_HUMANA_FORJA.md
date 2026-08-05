# Protocolo de escrita humana da FORJA

Versão: `FORJA-ESTILO-HUMANO-v2`  
Vigência: 15/07/2026  
Aplicação: toda peça, memorial, parecer, manifestação e todo corpo de e-mail produzido pela FORJA.

## Regra de liberação

A FORJA não estima “probabilidade de autoria por IA”. Esse número não é verificável e não serve como prova editorial. A liberação depende de sinais observáveis, contados no próprio texto e acompanhados do trecho exato.

Um achado `P0` impede a conclusão de F6, a aprovação de F7, o render simples, a composição visual, o pacote de revisão, o registro do rascunho e a entrega. Um achado `P1` exige leitura editorial e justificativa quando mantido.

O gate é recomputado sobre o Markdown real. Marcar manualmente `p0=0` ou `anti_ai_style_passed=pass` não contorna a verificação.

## Proibições bloqueantes

- Fórmulas de contraste: “não apenas... mas também”, “a questão não é X, mas Y” e “não se trata de X, mas de Y”.
- Metadiscurso vazio: “vale destacar”, “cumpre ressaltar”, “em outras palavras”, “isso significa que” e “em conclusão”.
- Metáforas genéricas e clichês que substituem consequência jurídica concreta.
- Intensificadores dogmáticos: “obviamente”, “claramente”, “sem dúvida”, “indiscutivelmente” e equivalentes.
- “Sempre”, “nunca” e equivalentes sem lastro aparente no mesmo parágrafo.
- Conectores automáticos em série, travessões explicativos repetidos, quatro frases curtas com o mesmo ritmo e parágrafos matematicamente simétricos.
- Duas frases consecutivas que reformulam a mesma proposição sem dado, regra, aplicação ou consequência nova.
- Conclusão iniciada por conector que apenas recapitula o texto e não formula pedido ou consequência processual concreta.

## Corpo dos e-mails em F9

O e-mail não é relatório nem resumo ornamental da peça. Ele deve parecer escrito por quem trabalhou no caso e sabe exatamente o que entrega, o que mudou e qual decisão ainda depende do destinatário.

Além das proibições gerais, bloqueiam o e-mail:

- aberturas de aquecimento, como “espero que este e-mail o encontre bem”;
- fórmulas burocráticas, como “venho por meio deste” e “gostaria de informar”;
- autonarração do esforço, como “realizei uma análise detalhada”;
- fechos traduzidos ou inflados, como “não hesite em entrar em contato” e “permaneço à disposição para quaisquer esclarecimentos adicionais”;
- cabeçalhos de relatório no corpo, como “Resumo executivo”, “Contexto”, “Visão geral” e “Considerações finais”.

A mensagem abre com a entrega, a mudança relevante ou a decisão necessária. O contexto limita-se ao necessário para compreender os anexos e o próximo passo. Quando houver pendências de revisão, preserva-se o bloco “Pontos que exigem o seu olho”, com alertas concretos e indicação de página. O fecho deve ser simples e natural.

O gate analisa apenas a mensagem nova: histórico citado com `>` e bloco de mensagem encaminhada não contaminam o resultado. O corpo aprovado integra o manifesto do pacote por `sha256`. O registro do rascunho exige `bodySha256` idêntico; qualquer edição posterior invalida a aprovação e obriga nova validação.

## Método de redação em F6

Antes de redigir, fixar em uma frase a questão jurisdicional e o resultado pretendido. Cada parágrafo recebe uma função única e verificável:

1. fato ou prova;
2. regra aplicável;
3. aplicação da regra ao fato;
4. refutação de argumento identificável;
5. pedido ou consequência processual.

Parágrafo sem função sai. Frase cuja exclusão não altera compreensão, demonstração ou pedido sai. Não se apresentam “todos os lados” por ritual, nem se responde além do problema que o órgão julgador deve decidir.

A voz autoral decorre de escolhas jurídicas explícitas: tese, limite, prioridade probatória e consequência. Ela não decorre de adjetivos de ênfase.

## Gosto jurídico autônomo

O gate negativo retira vícios observáveis, mas ausência de vício não produz
excelência. A camada `FORJA-GOSTO-EDGE-v1` acrescenta um processo positivo de
geração, rejeição e seleção:

1. `Exacting`: a IA produz internamente alternativas e não aceita a primeira
   versão fluente;
2. `Differentiated`: identifica a formulação óbvia e escolhe um fio decisivo
   específico do processo;
3. `Grounded`: conserva a separação entre afirmação, fonte e inferência;
4. `Emotional`: expõe uma consequência já demonstrada sem fabricar drama;
5. `Seleção`: compara alternativas por poder de decisão, especificidade, lastro
   e economia verbal.

F6 e F7 executam o método antes de devolver o texto. F7-B registra no
`editorial_report` a versão óbvia rejeitada, três direções consideradas, a
direção selecionada e âncoras literais do texto. O registro torna o raciocínio
editorial auditável, mas não prova sozinho a qualidade. O ciclo AUTO-RESEARCH
faz a prova comparativa: outputs pareados são julgados às cegas, com correção
jurídica e cobertura como condições de não inferioridade.

“Emocional” não significa sentimental. Em peça jurídica, significa permitir que
o leitor perceba a consequência humana, institucional ou processual que os autos
já demonstram. Nenhum efeito retórico autoriza criar sofrimento, intenção,
urgência, fato, nexo ou grau de certeza.

## Auditoria em F7

O revisor deve:

1. executar `python forja_estilo_humano.py <texto.md> --tipo peca`;
2. reescrever cada `P0` sem alterar fatos, fontes, citações ou pedidos;
3. conferir os `P1` no contexto;
4. executar o gate novamente;
5. só então declarar `anti_ai_style_passed=pass`.

O relatório JSON registra regra, severidade, trecho, problema e ação corretiva. Este gate não faz substituição automática de palavras: uma troca cega pode alterar a tese ou a precisão jurídica. Depois da auditoria F7 sem P0, a subfase controlada F7-B pode reescrever a peça com o Claude Fable 5; essa reescrita parte sempre do texto auditado, é limitada à edição de linguagem e só passa quando hashes, invariantes materiais e este gate de escrita humana forem recompostos por código. Ver `PROTOCOLO_FABLE5_ESCRITA_FINAL.md`.

## Auditoria do e-mail em F9

1. executar `python forja_estilo_humano.py <email.txt> --tipo email`;
2. cortar fórmulas, cerimônia e explicações que pertencem aos anexos;
3. conferir se entrega, alertas e próximo passo aparecem sem rodeios;
4. executar novamente o gate;
5. gerar o pacote e registrar no recibo do rascunho o `bodySha256` do corpo efetivamente inserido no Gmail.

## Exemplos de correção

Ruim: “Vale destacar que a questão não é a existência do contrato, mas a sua validade.”  
Direto: “O contrato existe. A controvérsia recai sobre sua validade, porque a cláusula 8 foi assinada sem a autorização exigida pelo art. X.”

Ruim: “Claramente, a parte nunca comprovou o pagamento.”  
Com lastro: “Os eventos 42, 51 e 63 não contêm recibo, comprovante bancário ou declaração de quitação.”

Ruim: “Em síntese, por todo o exposto, a decisão deve ser reformada.”  
Pedido: “Requer-se o provimento do agravo para afastar a intempestividade reconhecida no evento 185 e determinar o exame do mérito.”

Ruim: “Espero que este e-mail o encontre bem. Gostaria de informar que realizei uma revisão detalhada da peça.”  
Direto: “Fábio, revisei a impugnação e anexei as versões em Word e PDF. O pedido da página 9 agora está ligado ao documento do evento 42.”
