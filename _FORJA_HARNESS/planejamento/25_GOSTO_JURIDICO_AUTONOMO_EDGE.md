# Gosto jurídico autônomo na FORJA

**Protocolo:** `FORJA-GOSTO-EDGE-v1`  
**Fonte estudada:** transcrição integral, em inglês, do vídeo “The ONE Skill
Every High Performer Needs To Master (in the age of AI)”, de Sandeep Swadia,
publicado em 23/07/2026.  
**URL:** https://www.youtube.com/watch?v=Vko7hmwrJjc  
**Transcrição local auditável:** `youtube-transcript/sandeep-swadia/the-one-skill-every-high-performer-needs-to-master-in-the-age-of-ai/transcript.md`

## 1. O que o vídeo realmente sustenta

O vídeo chama de *synthetic sameness* o resultado aceitável, fluente e
intercambiável produzido quando todos usam o mesmo modelo pelos mesmos padrões
(`00:01:57–00:02:40`). A abundância de versões não gera originalidade. Ela
aumenta a necessidade de seleção.

O framework EDGE aparece em `00:04:18–00:05:10`:

- `Exacting`: padrão alto e rejeição do genérico;
- `Differentiated`: afastamento do default e adoção de ponto de vista;
- `Grounded`: ancoragem em realidade, dados e verificação;
- `Emotional`: capacidade de produzir efeito sentido, não apenas forma correta.

Entre `00:06:18–00:09:51`, a tese é operacional: como a IA gera variações sem
fim, o trabalho escasso passa a ser rejeitar. O exemplo apresentado seleciona
253 clipes entre mais de 16 mil. O número é ilustrativo; a lição aplicável à
FORJA é que “passou no gate” não equivale a “é a melhor versão”.

Em `00:13:43–00:14:13`, o vídeo propõe três perguntas antes de criar: qual é a
versão óbvia, quais ângulos se afastam dela e qual deles faria o leitor prestar
atenção — com uma razão. Esse é o trecho mais diretamente convertível em
programação de harness.

Em `00:16:36–00:17:19`, o vídeo impõe três formas de grounding: exigir fontes,
submeter a resposta a verificação independente e trabalhar sobre um corpus
fornecido. A FORJA já possui controles mais fortes que essa recomendação:
ledgers, hashes, replay de fonte, separação produtor/revisor e gates fail-closed.

Entre `00:17:22–00:19:45`, “emocional” é explicado como sentido dependente de
contexto. Para petições, isso não autoriza melodrama. A tradução juridicamente
segura é **saliência decisória**: fazer o julgador perceber a consequência
humana, institucional ou processual que os autos já provam.

## 2. Onde a tese do vídeo precisa ser corrigida

O vídeo afirma que originalidade e gosto são coisas que a IA não pode gerar. A
formulação é forte demais. A IA pode desenvolver uma competência funcional de
gosto quando o harness lhe oferece:

1. corpus de bons e maus exemplos;
2. geração deliberada de alternativas;
3. comparação cega e independente;
4. rubrica explícita;
5. rejeição com motivo;
6. memória de resultados;
7. promoção somente após prova fora da amostra usada para criar.

Isso não cria experiência humana subjetiva. Cria algo mais útil para a FORJA:
**capacidade estável de discriminar, selecionar e melhorar texto jurídico por
consequências observáveis**.

## 3. Tradução do EDGE para petições

| EDGE | Pergunta operacional | Falha bloqueada | Mecanismo FORJA |
|---|---|---|---|
| Exacting | Esta é a melhor entre alternativas ou apenas a primeira aceitável? | fluência mediana aprovada por inércia | três direções internas, revisão adversarial e julgamento pareado |
| Differentiated | Qual é o fio decisivo que só existe neste processo? | doutrina genérica, peça intercambiável | versão óbvia explicitamente rejeitada + âncoras do caso |
| Grounded | Que fonte sustenta cada afirmação que precisa ser verdadeira? | alucinação confiante | ledgers, hashes, replay oficial e lacuna preservada |
| Emotional | Que consequência já provada precisa ser percebida para decidir? | texto correto, mas sem peso | saliência humana/institucional/processual sem dramatização |

## 4. Arquitetura de autonomia

```text
corpus e ledgers congelados
          ↓
mapa da versão óbvia
          ↓
5 ângulos → filtro de lastro → 3 direções editoriais
          ↓
seleção interna EDGE + revisão adversarial
          ↓
gates determinísticos de fidelidade e estilo
          ↓
execução pareada no AUTO-RESEARCH
          ↓
juiz cego: correção não inferior + preferência EDGE
          ↓
holdout/canários → candidato técnico
```

A geração e a seleção editorial podem ser autônomas. A autorização jurídica
para protocolar continua separada: nenhum ganho de estilo transforma modelo em
fonte, advogado responsável ou autoridade de liberação.

## 5. O que foi implementado nesta onda

1. O prompt de F6/F7 agora executa `FORJA-GOSTO-EDGE-v1` internamente.
2. O passe F7-B produz três direções editoriais silenciosas, escolhe uma,
   registra o recibo `gostoJuridico` e descarta a candidata quando protocolo,
   unicidade da seleção ou âncoras literais forem inconsistentes.
3. O gerador de variantes do AUTO-RESEARCH identifica a versão óbvia, explora
   cinco ângulos e registra a hipótese escolhida.
4. O juiz cego passou a avaliar `exacting`, `differentiated`, `grounded`,
   `emotional` e poder decisório, sempre depois da não inferioridade jurídica.
5. O gate determinístico passou a bloquear aberturas jurídicas que apenas
   invocam consenso sem fonte, como “é cediço que” e “como se sabe”.

## 6. Questões essenciais para as próximas ondas

1. O texto permite que o julgador formule a questão decisiva em uma frase?
2. A abertura começa pela fricção real do caso ou por um prefácio que serviria
   em qualquer processo?
3. Cada capítulo contém pelo menos uma âncora verificável e uma consequência?
4. O ponto de vista decorre da prova e da escolha jurídica, ou apenas do tom?
5. Qual trecho seria idêntico se nomes, datas e números fossem trocados?
6. A peça dá o mesmo espaço a argumentos de pesos diferentes por simetria
   automática?
7. A consequência humana ou institucional está provada, ou foi insinuada para
   produzir emoção?
8. A melhor versão venceu de modo consistente quando a ordem A/B foi invertida?
9. Juízes de famílias diferentes preferem o mesmo texto pelos mesmos motivos?
10. O ganho de saliência preserva integralmente pedidos, ressalvas, autoridades,
    polaridade e grau de certeza?
11. O sistema aprende com rejeições ou apenas repete novas amostras do mesmo
    default?
12. O holdout confirma melhora fora dos casos usados para formular a variante?

## 7. Próxima onda recomendada

Transformar o recibo `gostoJuridico`, hoje validado no executor de geração, em
gate contratual recomposto também na promoção; acrescentar ao AUTO-RESEARCH uma
rubrica JSON estruturada por dimensão EDGE. A promoção deve exigir:

- âncoras declaradas existentes no texto auditado e no texto final;
- pelo menos três direções realmente distintas;
- não inferioridade em correção, cobertura e fidelidade;
- preferência cega estável após troca de posição;
- ausência de ganho obtido por cortar conteúdo obrigatório.

Essa onda exige alteração de contrato e deve ser feita separadamente, com
compatibilidade para bundles históricos.
