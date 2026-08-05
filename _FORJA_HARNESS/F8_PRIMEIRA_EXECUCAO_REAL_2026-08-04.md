# Os 16 gates da F8 encontraram uma peça pela primeira vez — 04/08/2026

Antes de hoje, os dezesseis gates de QA visual tinham regressão unitária e nenhuma história:
os quatro ledgers visuais do acervo são anteriores ao regime estático de 30/07 e não acionam
a rota que hoje é produção. Como a decisão de tornar o F8-S bloqueante estava marcada para
depois de 05/08, deixá-los sem uma execução real seria ligar um gate no escuro.

Exerci o contrato estático contra **quatro peças reais, entregues e aprovadas** — V8 e V9 do
Cafelana, o plano estratégico da reconstrução e os memoriais do AI 0011621-15. Nenhum caso foi
tocado; a auditoria roda sobre o `.docx` e não escreve nada.

## O resultado da primeira rodada: o gate reprovou as quatro

De 4 a 7 gates reprovados por peça. Trabalho aprovado pelo escritório sendo barrado em massa é
o sinal clássico de gate mal calibrado, não de peça ruim — e foi o que se confirmou.

## Três falsos positivos estruturais, corrigidos

**1. A síntese executiva.** Cinco parágrafos dos memoriais estavam a 10,5 pt e o gate os leu
como "corpo fora de 12 pt". A síntese no estilo do art. 343-A do RISTJ é **obrigatória em toda
peça desde 07/07/2026**, por determinação do Prof. Fábio, e é deliberadamente menor. Um gate
que a reprova reprova a regra da casa.

**2. O bloco de qualificação das partes.** Mesma coisa na V8 do Cafelana.

**3. A citação recuada.** Um trecho transcrito do próprio acórdão impugnado, a 10,5 pt, como
manda a convenção do texto jurídico.

Os três viraram papéis reconhecidos em `forja_docx_layout._role_for`, com o afrouxamento
limitado ao TAMANHO — família tipográfica e justificação continuam cobradas nesses blocos.
`test_forja_layout_papeis.py` é o teste-âncora, escrito com o texto real das peças.

## O falso positivo mais grave: o gate reprovava o próprio template

`docx_folio_collision_safe` exigia fólio de no máximo **36 pt**. O shape do fólio no
`TEMPLATE_MEDINA_OSORIO_PETICAO.docx` — o template aprovado, do qual toda peça é obrigada a
nascer — mede **57,3 pt**. O limiar não vinha de medição nenhuma.

Ou seja: o gate reprovava, por diagramação insegura, toda peça produzida do único jeito
autorizado de produzir uma peça. Recalibrado para 61 pt, medido no template com 4 pt de folga;
a margem direita do padrão tem 99,2 pt, então o fólio cabe com sobra. Os quatro documentos
deixaram de ser barrados pelos falsos positivos; os dois achados reais descritos abaixo
permaneceram visíveis.

## E então apareceu o defeito real

Com os falsos positivos fora do caminho, sobrou o que o gate existe para achar:

**`CAFELANA_NONO_TOPICO_V9_REVISAO_LIMPA.docx` — 30 de 48 parágrafos do corpo a 11 pt.** Os
outros 18 estão a 12 pt. **11 pt não existe no padrão da casa**: o corpo é 12, e os elementos
estruturais são 10,5. É documento com duas tipografias de corpo misturadas, entregue em
31/07 como revisão interna. Cobertura de tamanho: 37,5%.

> **CORREÇÃO, ainda em 04/08/2026:** o parágrafo abaixo estava ERRADO e fica aqui porque
> apagá-lo ensinaria menos. Segoe UI **é** da identidade da casa: `medina_visual_kit`
> define `SANS = "Segoe UI"` e a usa em rótulo de tabela desde o padrão aprovado em
> 09/07/2026; a V4 de 15/07, também entregue, tem a mesma mistura. Era falso positivo do
> gate contra o padrão do dono — o mesmo erro do fólio e da síntese executiva, na terceira
> vez no mesmo dia. O gate foi recalibrado e a peça nunca teve esse defeito.

**`IMPUGNACAO_AGINT_CAFELANA_V8` — tabela 1 mistura Segoe UI 8 pt com Times New Roman 10,5 pt.**
Segoe UI não pertence à identidade da casa; o cheiro é de tabela colada de outra fonte.

Nenhum dos dois é catástrofe, e nenhum dos dois teria sido encontrado por leitura — são
defeitos que só aparecem no XML.

## O que isso muda para a decisão sobre o F8-S

Quatro gates continuam reprovando as quatro peças por artefato da minha invocação, e não da
peça: `semantic_fidelity_recomputed` e `docx_content_and_tracking_fidelity_pass` exigem o
markdown de origem, que eu não passei; `independent_human_or_visual_agent_reviewer` e
`document_scope_reviewed_at_100_percent` exigem revisor humano declarado, que só existe dentro
da fase. Numa execução de F8 de verdade esses insumos existem.

A recomendação, que continua sendo sua decisão: **ligar o F8-S depois de 05/08 ficou mais
seguro do que era hoje de manhã**, porque os dois falsos positivos que barrariam toda peça —
a síntese executiva e o fólio do template — estão corrigidos e ancorados em teste. O que
permanece verdadeiro é que o primeiro caso real será também o primeiro teste do gate dentro da
fase, e merece ser acompanhado em vez de confiado.
