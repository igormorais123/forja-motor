# PADRÃO WORD MEDINA OSÓRIO — especificação canônica (extraída das peças reais)

Extraído programaticamente em 08/07/2026 de 4 peças ORIGINAIS do escritório (CASO-04 CR EDcl, Memoriais CASO-19 e Fábio, EDcl José Eduardo, Quesitos CASO-17) e conferido contra 5 finais da fábrica. Evidência bruta: `.autoresearch\padrao_word_extraido.json`.

## REGRA NÚMERO 1 — nunca criar documento do zero

O timbre "MEDINA OSÓRIO ADVOGADOS" é **arte vetorial** embutida no cabeçalho da 1ª página (32 formas desenhadas, letras como curvas — irreproduzível por código). Portanto:

> **TODA peça nova parte de `_FERRAMENTAS\TEMPLATE_MEDINA_OSORIO_PETICAO.docx`** (template oficial com timbre, rodapé institucional, fólio e estilos já embutidos — validado em PDF) **ou de cópia da peça anterior do mesmo caso.** `Document()` vazio do python-docx é PROIBIDO para peça do escritório.

## Especificação da página

| Item | Valor extraído |
|---|---|
| Papel | A4 (21,0 × 29,7 cm) |
| Margens | esquerda **3,0** · direita **3,5** · inferior **3,25** · superior **3,0** (contrarrazões) ou 2,5 (memoriais/EDcl — seguir a peça anterior do caso) |
| Distância cabeçalho/rodapé | 1,25 / 1,2 cm |
| 1ª página diferente | SIM (`different_first_page_header_footer=True`) |

## Cabeçalhos e rodapés (como estão no arquivo)

- **1ª página, cabeçalho** (`header3.xml`): timbre vetorial (logo coluna + wordmark) + "ADVOGADOS" espaçado em cor `#3A5C61` + filete horizontal.
- **1ª página, rodapé** (`footer3.xml`): `www.medinaosorio.com.br` + `Brasília | Porto Alegre | Rio de Janeiro` com ícones, 10,5pt, cor `#4A4A4D`, + elementos decorativos de canto (faixas petróleo/terracota).
- **Demais páginas, cabeçalho** (`header2.xml`): **fólio** (campo PAGE) com filete inferior, em shape ancorado à **margem direita, centralizado VERTICALMENTE na página** (`positionH relativeFrom="rightMargin"` + `positionV relativeFrom="margin" align="center"`) — confirmado no XML do template e no PDF protocolado da CASO-04 (08/07/2026); não é "topo direito". Rodapé das demais páginas: vazio.

## Corpo do texto (o DNA tipográfico)

| Item | Valor (100% das peças originais) |
|---|---|
| Fonte | **Times New Roman 12** em todos os runs (356/356 na CASO-04) |
| Alinhamento | **Justificado** em todos os parágrafos |
| Entrelinhas | **1,5** nas peças federais/STJ; 1,15 na EDcl TJTO (seguir a peça anterior do caso) |
| Recuo de 1ª linha | **2,5 cm** (contrarrazões) ou 2,0 cm (memoriais/EDcl) — NUNCA os 1,25 cm da ABNT genérica |
| Parágrafos | numerados (1., 2., 3. ...), topic sentence pode levar negrito |
| Negrito | mínimo e estratégico; títulos de seção em romanos (I –, II –) em negrito, sem recuo |
| Endereçamento | CAIXA ALTA em negrito, sem recuo, 1ª linha da peça |
| Fecho | "Nestes termos, pede deferimento." + local/data + bloco de assinaturas centralizado (FÁBIO MEDINA OSÓRIO — OAB/DF 29.7860-A) |

## Diagramas dentro da peça

Regras da skill `fabrica-visual-peticoes` (autoridade): SVG → **EMF** via `svg_para_emf` (gate de legibilidade automático) → inserção via `inserir_emf_word_com` com largura de `estilo_medina.largura_recomendada_cm(svg)` → PDF pelo Word COM → QA visual página a página. As finais antigas (CASO-04, Jalusa) usaram PNG — daqui em diante é EMF.

## Desvios já flagrados (não repetir)

1. **MEMORIAIS_LIBRA_SUL.docx** fugiu do padrão: margens 3/2/3/2 (default de editor), sem recuo de 1ª linha, sem timbre. É o retrato do que acontece quando não se parte do template.
2. Documento sem `different_first_page` perde o timbre da capa.
3. Recuo de 1,25 cm (ABNT genérica) não é o padrão da casa — é 2,0–2,5 cm.

## Checklist de conformidade antes de entregar (Claude, Codex e Cícero)

- [ ] Partiu do TEMPLATE ou de cópia da peça anterior do caso (timbre presente na 1ª página do PDF).
- [ ] Times New Roman 12, justificado, entrelinhas e recuo conforme a família da peça.
- [ ] Fólio na margem direita (centralizado verticalmente, filete inferior) a partir da página 2; rodapé institucional só na 1ª página.
- [ ] Margens conferidas (esq 3,0 / dir 3,5 / inf 3,25).
- [ ] Diagramas EMF com gate de legibilidade e largura recomendada.
- [ ] PDF gerado pelo Word COM e QA visual página a página (timbre, colisões, órfãos, placeholders `[...]`).
