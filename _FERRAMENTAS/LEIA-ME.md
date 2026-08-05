# _FERRAMENTAS — Arsenal de diagramação de excelência (Word + LaTeX)

Instalado e validado em 07/07/2026 (teste ponta a ponta SVG→EMF→docx→PDF aprovado). Toda IA que produzir peça nesta fábrica deve usar este arsenal.

**Lição crítica**: python-docx NÃO reconhece EMF. O fluxo correto é: montar o docx com python-docx deixando parágrafos-marcador `{{FIG1}}` e chamar `inserir_emf_word_com` (o próprio Word insere o EMF vetorial no lugar). Nunca tentar `add_picture` com EMF.

**Identidade Medina Osório** (extraída da peça original): logo em `_FERRAMENTASssets\logo_medina.png` (600 dpi); cores: verde-petróleo `#395C60`, terracota `#D9926A` (escura `#9C5B38`), grafite `#49494D`; rodapé: linha petróleo + `www.medinaosorio.com.br` | `Brasília | Porto Alegre | Rio de Janeiro`; corpo Times New Roman; fólio no topo direito.

**Estilo e legibilidade (novo, 08/07/2026)**: `estilo_medina.py` é a fonte única de tokens (CORES, fontes, `ESTILO_GRAPHVIZ`, `TEMA_MERMAID`, `aplicar_estilo_matplotlib()`). Regra de fonte mínima: **8pt no tamanho final impresso** (viewBox 600 @ 15cm → font-size ≥ 12px). O gate é automático em `svg_para_emf(svg, emf, largura_final_cm=...)` — reprova e explica a correção. Auditoria avulsa: `checar_fontes_svg(svg, largura_cm)`.

**Bateria exaustiva de 08/07/2026** (`.autoresearch\pipeline-visual-medina\`, 21 casos + E2E Word + smoke Tectonic): o gate agora cobre shorthand CSS `font: 400 9px ...`, unidades `pt`/`em`/`rem`, texto SEM font-size (avalia o default 16px), viewBox com decimais/vírgulas/offset (formato do Graphviz); `aplicar_estilo_matplotlib()` força `svg.fonttype='none'` (senão o texto vira caminho e escapa da auditoria). **Regra nova contra "diagrama gigante"**: nunca inserir a 15cm fixo — usar `largura_recomendada_cm(svg, alvo_pt=10)` para calcular a largura em que a menor fonte imprime ~10pt (ex.: fluxo Graphviz de 3 nós → 8,6cm).

**Imagens geradas por IA (novo)**: `gerar_imagem_ia(prompt, png)` no pipeline (inference.sh/infsh). Permitido: capas de relatórios/pareceres ao cliente, ilustração institucional sóbria, ícones. PROIBIDO em peça protocolada: retratar fatos, pessoas ou provas do caso. Política completa na skill `fabrica-visual-peticoes`.

## Regra de ouro para Word (formato usual do escritório)

**Diagramas dentro do Word devem ser VETORIAIS (EMF).** PNG serrilha em zoom e impressão. O caminho é: desenhar em SVG → converter para EMF com Inkscape → inserir no docx → gerar PDF pelo próprio Word (COM) → inspecionar página a página.

Script pronto: `word_visual_pipeline.py` (nesta pasta) com todas as funções: `svg_para_emf`, `mermaid_para_svg`, `dot_para_svg`, `inserir_imagem_docx`, `docx_para_pdf` (Word COM, fidelidade máxima), `render_paginas` (gate de QA visual).

## Ferramentas instaladas

| Ferramenta | Função | Como chamar |
|---|---|---|
| **Inkscape 1.4** | SVG → EMF vetorial (chave do Word) e SVG → PNG 300dpi | `inkscape arquivo.svg --export-type=emf --export-filename=saida.emf` |
| **Graphviz** | Fluxogramas/organogramas por código (DOT) | `dot -Tsvg fluxo.dot -o fluxo.svg` |
| **mermaid-cli (mmdc)** | Linhas do tempo, fluxos, gantt por texto | `mmdc -i diag.mmd -o diag.svg -b transparent` |
| **ImageMagick** | Ajustes raster, recortes, composição | `magick ...` |
| **Tectonic (XeTeX)** | LaTeX autocontido, baixa pacotes sozinho | `C:\Users\IgorPC\.local\tectonic\tectonic.exe peca.tex` |
| **Pandoc 3.10** | Conversões docx↔md↔tex | `pandoc in.docx -t markdown -o out.md` |
| **MS Word (COM)** | docx → PDF com fidelidade total; suporta SVG nativo (M365) | via `word_visual_pipeline.docx_para_pdf` |
| **python-docx + docxtpl + docxcompose + pywin32** | Montagem programática de docx, templates com timbre do escritório, mesclagem | `import docx` etc. |
| **matplotlib + pymupdf (fitz)** | Gráficos quantitativos; render de PDF para QA visual | — |

## Pipeline padrão de uma peça Word com visual law

1. **Texto**: partir do template/timbre do escritório (nunca inventar diagramação de página — regra CLAUDE.md global, item 4 das correções recorrentes).
2. **Diagramas**: desenhar SVG próprio (TikZ standalone→SVG, Graphviz, Mermaid ou SVG manual), paleta sóbria forense: navy `#1B2A4A`, grafite `#3A3F47`, bronze `#8C6A2F`, painéis `#F4F2ED`/`#EEF1F6`. Fontes: a da peça (Arial/Palatino) — sem "cara de IA".
3. **Converter cada SVG para EMF** (Inkscape) e inserir com `inserir_imagem_docx` (legenda itálica 9pt cinza, "Figura N — ...").
4. **PDF**: gerar SEMPRE pelo Word COM (`docx_para_pdf`) — LibreOffice/pandoc alteram quebras e fontes.
5. **Gate visual obrigatório**: `render_paginas` + inspecionar TODAS as páginas antes de declarar pronto.

## Pipeline LaTeX (edições estilo revista/visual law)

- Compilador: **Tectonic** em `C:\Users\IgorPC\.local\tectonic\tectonic.exe`.
- Modelo de referência pronto: `o modelo LaTeX registrado no acervo sob a chave `modelo-revista-latex`` (capa editorial, pull quotes na margem, caixas tcolorbox para acórdão/precedente, diagramas TikZ, tabela zebrada, numeração de parágrafos).
- Armadilhas conhecidas do Tectonic/PGF: (a) `\\` NÃO pode ficar aninhado dentro de grupos `{...}` em nós TikZ — deixar `\\` sempre no nível do nó; (b) `\rowcolors` exige `\usepackage[table]{xcolor}`; (c) Palatino Linotype não tem o glifo "→" — usar `$\to$`; (d) fontes do Windows funcionam via fontspec (Palatino Linotype, Segoe UI).

## O que NÃO usar

- `claude-in-chrome` (regra global).
- PNG de baixa resolução dentro de peça.
- Conversão docx→pdf por pandoc/LibreOffice para versão final.
- Elementos decorativos "cara de IA": linhas divisórias gratuitas, sombras, gradientes chamativos, excesso de negrito.

## Contexto de pesquisa (07/07/2026)

Ferramentas de mercado para visual law (Jigsaw, Canva, Visio, UX Doc) são interativas; nosso fluxo é programático e reprodutível, com resultado equivalente ou superior. Word aceita vetor apenas em EMF/WMF (ou SVG nativo no M365); a rota SVG→EMF via Inkscape é o padrão de excelência.
