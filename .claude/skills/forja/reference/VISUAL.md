# VISUAL — a assinatura da FORJA

> Ordem do Igor, 30/07/2026, esteira reconstruída em 03/08/2026: **nenhuma peça sai da
> FORJA sem elementos visuais completos.** Nenhum caminho que passou pela FORJA entrega
> sem padrão visual completo. Sem atalho, sem waiver, sem modo rápido, sem exceção para
> produto interno. O visual vale tanto quanto o conteúdo.

## Índice

- [A entrada única](#a-entrada-única)
- [O brief F7.5, e por que ele existe](#o-brief-f75-e-por-que-ele-existe)
- [Os gates do desenho](#os-gates-do-desenho)
- [Identidade da casa](#identidade-da-casa)
- [O que já quebrou aqui](#o-que-já-quebrou-aqui)

## A entrada única

```
python forja_visual_build.py <peca.md> <saida_dir> "Título" --tipo peca \
  --case-dir <caso> --base-dir <caso> --ledger <caso>/.../fact_ledger.json
```

O fluxo interno, em 7 a 15 segundos: gates F7 → brief `F7_5_BRIEF_VISUAL.json` → mapa
automático (`forja_visual_mapa_gen.py`) → figuras (`forja_visual_figuras.py` sobre os
geradores de `_FERRAMENTAS/medina_svg_kit.py`) → `forja_visual.compor()` → inserção OOXML
com gate de colisão → QA estrutural → gate F8-S (`forja_assinatura_visual.py`).

O PDF, o render página a página e a inserção de EMF saem depois, por
`montar_visual.montar()`. O comando está em [COMANDOS.md](COMANDOS.md#produção-visual-f75-f8).

**Não integrar `compor()` dentro de `forja_render_docx.render()`.** Foi analisado e
rejeitado: constrói a peça duas vezes, uma pobre e uma rica, e deixa dois DOCX parecidos
na mesma pasta. O render simples é prévia; a produção passa pela entrada única.

**Fidelidade textual é 100% e não é negociável.** Nunca peça a um agente que transcreva
o texto da peça para compor: cinco de cinco resumiram entre 80% e 95%. O agente escreve
o mapa visual declarativo; o texto vem do markdown, inteiro, por conversão determinística.

## O brief F7.5, e por que ele existe

`F7_5_BRIEF_VISUAL.json`, na mesma pasta do markdown. Contrato em
`templates/F7_5_BRIEF_VISUAL.md`. Custa 1 a 2 minutos e o autor declara três coisas:
`ancoras` (o que a capa destaca), `cadeiaArgumentativa` (3 a 6 elos) e `cronologia`
(pares data/descrição).

Sem ele, só saem as figuras estruturalmente seguras, e peça longa não fecha o piso
gráfico — o gate acusa `VIS-03`, corretamente.

**Nunca inferir conteúdo semântico de figura a partir de prosa argumentativa.** Foi
tentado duas vezes e as duas produziram figura bonita afirmando coisa falsa: uma
cronologia que misturou a data do documento, um prazo interno e um fragmento de número
CNJ lido como data; e uma cadeia de tese que pôs a **tese da parte adversária** como elo
do raciocínio da cliente. Cada frase era verbatim e o conjunto mentia. Não é problema de
heurística, é de premissa: nenhum filtro separa "nossa tese" de "tese deles" numa frase
de abertura.

O validador é barato e pega o modo de falha real: número, data ou dispositivo que
aparece na figura e **não** aparece no texto é fato introduzido pela camada visual, e é
proibido.

## Os gates do desenho

| Gate | Onde roda | O que reprova | Bloqueia? |
|---|---|---|---|
| **SVGC-01** | `medina_svg_colisao.py`, dentro da inserção | texto ocluído por forma opaca pintada depois | sim |
| **SVGC-02** | idem | texto sobre texto | sim |
| **SVGC-04** | idem | cor sintaticamente inválida (`fill="ffffff"` sem `#`) | sim |
| **SVGC-03** | idem | traço cruzando texto | aviso |
| **SVGC-05** | idem | contraste ilegível | aviso |
| **legibilidade** | `svg_para_emf(..., largura_final_cm=)` | texto abaixo de 8pt impressos | sim |
| **overflow** | `medina_svg_kit` | conteúdo estourando o viewBox | sim |
| **F8-S** | `forja_assinatura_visual.py` | ausência de elementos (VIS-02 a VIS-11) | ver abaixo |

O gate de colisão roda em **todo** SVG que entra no Word, inclusive o desenhado à mão.
Ele existe porque o gate de presença, o de legibilidade e o de overflow aprovam, os três,
um diagrama internamente quebrado. Calibrado contra os 228 SVGs do acervo: 5 reprovações,
todas confirmadas por render como defeito real.

**O limiar de contraste é 2,0:1, e não os 3,0:1 da WCAG.** O rótulo terracota sobre
painel terra da identidade da casa dá 2,3:1 e está aprovado; calibrar na norma reprovaria
a paleta do escritório.

**Se o F8-S bloqueia ou apenas observa é estado, não regra — nunca decore.** Confira
`forja_assinatura_visual.py` e o último `F8S_ASSINATURA_VISUAL.json` antes de afirmar o
modo vigente. A ordem permanente do titular não depende disso: peça sem elementos
visuais completos não sai, bloqueie o gate ou não.

## Identidade da casa

Petróleo `#395C60`, terracota `#D9926A`, Times New Roman, rodapé institucional, logo em
`_FERRAMENTAS/assets/`. Corpo 12 justificado; entrelinhas 1,5 (federais e STJ) ou 1,15
(TJTO); recuo de primeira linha 2,0–2,5 cm — **nunca** 1,25 ABNT; margens esquerda 3,0,
direita 3,5, inferior 3,25.

**Nunca detecte identidade visual por valor de cor.** A arte do timbre usa `3a5c61` e
`d9936a`, um dígito fora dos tokens. Prova de identidade é estrutural.

Precedência entre as skills visuais: `fabrica-visual-peticoes` rege protocolo e pipeline;
`padrao-visual-medina` rege a linguagem visual. Em conflito, a primeira manda no processo
e a segunda na aparência.

Imagem gerada por IA só em material ao cliente ou institucional — **nunca** retratando
fato, pessoa ou prova em peça protocolada.

## O que já quebrou aqui

**Recurso que depende de esforço manual por caso não sobrevive ao volume.** Foi por isso
que a edição visual parou em 10/07 sem ninguém notar. O mapa manual virou refinamento
opcional; a rota automática é a padrão.

**Gate que só procura defeito nunca detecta pobreza.** É preciso a contraparte
afirmativa, que verifica presença. E gate instalado em rota que ninguém percorre é gate
nenhum — o elo bloqueante que existia rodou em três casos na história.

**Densidade gráfica por repetição é densidade falsa.** A matriz comparativa era desenhada
a partir de uma tabela do próprio markdown, sob a premissa de que "só troca o meio de
apresentação". Mas a composição preserva 100% do texto, então a tabela continua impressa
e o conteúdo sai duas vezes — uma como "Figura 1", outra como tabela. Saiu assim numa
entrega de 08/08/2026 e passou pelo QA página a página sem ser visto. A fonte foi
desligada; o caminho certo, substituir a tabela pela figura, exige mexer no contrato de
fidelidade e não se faz de passagem.

**Rótulo de caixa precisa de dígito.** A expressão regular de identificador de precedente
aceitava `AgInt`, que é classe de recurso e não identifica julgado nenhum — e ela casa
antes do número que vem depois dela na mesma frase. Saiu impresso "AGINT" numa peça.

**Destaque de margem não pode terminar no meio de citação legal.** O divisor de frases
quebra no ponto de "art." e em dois-pontos; impressa na margem, a metade resultante
termina em "…o dever de coerência do art." O filtro antigo pegava só a metade que
*começa* minúscula — a outra metade começa maiúscula e passava.

**Comitê de personas não substitui revisão de código.** O conselho leu o dossiê do
construtor e recomendou arquitetura já rejeitada, citando função inexistente. A
circularidade de autovalidação — quem constrói escreve o gate, mede com ele e se aprova
— só foi quebrada pela revisão cruzada com outra família de modelo, lendo o XML.

**Defeito só é defeito contra o padrão aprovado.** Mantenha o teste-âncora contra a peça
aprovada em 09/07: gate que reprova o padrão aprovado pelo dono está errado, não a peça.
Os retângulos cinza da capa e o vazio inferior são identidade, não erro.
