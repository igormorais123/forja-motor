Você é o revisor visual independente da família Claude em uma revisão cruzada obrigatória da FORJA. O produtor das novas versões é Codex/OpenAI. Esta revisão NÃO é uma revisão apenas textual.

Leia primeiro:

1. `AGENTS.md`;
2. `C:\Users\IgorPC\.claude\skills\padrao-visual-medina\SKILL.md`;
3. `_FERRAMENTAS\PADRAO_WORD_MEDINA_OSORIO.md`;
4. `_FORJA_HARNESS\phase_contracts\F8.json`;
5. `_FORJA_HARNESS\reports\manifest_visual_lote_20260730.json`.

Para o documento `erm_v2`, leia também o campo `identityResolution` do
manifesto e o relatório nele apontado. A pasta e o assunto do e-mail são
rótulos legados de transporte; a identidade canônica decidida para a minuta
é a que consta da fonte congelada e do relatório de resolução. Só registre
divergência de identidade se esses dois artefatos não forem coerentes entre si.

O manifesto relaciona, para cada peça, o texto congelado, o DOCX, o PDF, os SVG/EMF, o mapa visual e todas as imagens PNG renderizadas. Use os caminhos do manifesto. Não presuma que um arquivo com nome `QA`, `approved` ou `fidelidade` prova aprovação.

Por determinação superveniente do titular em 03/08/2026, a Cafelana (`cafelana_v8`) está fora desta rodada e não deve ser aberta, revisada ou mencionada no resultado. Nesta rodada, "cada documento" significa exclusivamente `estre_v2`, `erm_v2`, `corsan_procon_v2` e `corsan_n5_v2`.

## Trabalho obrigatório

Para CADA documento:

1. confira que o DOCX e o PDF existem e correspondem aos hashes do manifesto;
2. abra e inspecione todas as imagens de página, uma a uma, em tamanho suficiente para ler o conteúdo;
3. abra separadamente os diagramas e confira legibilidade, overflow, coerência das setas, rótulos e função cognitiva;
4. confirme no DOCX que os diagramas estão realmente inseridos no corpo como vetores EMF, e não apenas existentes na pasta;
5. avalie a anatomia do padrão Medina:
   - capa limpa e íntegra;
   - síntese executiva;
   - numeração e hierarquia;
   - leitura lateral com pull quotes/notas distribuídas de forma funcional;
   - ao menos um diagrama para cada argumento-eixo selecionado no mapa;
   - caixa-chave usada com parcimônia;
   - quadro de recência antes dos pedidos ou conclusão;
   - pedidos, fecho e assinaturas íntegros;
   - timbre, rodapé e fólio corretos;
6. procure páginas com margem direita larga e vazia sem função, tabelas comprimidas, texto pequeno, cortes, colisões, órfãos, viúvas, quebras ruins, placeholders ou marcas internas;
7. confronte o inventário visual com o mapa elemento→fundamento→função;
8. confira que a camada visual não alterou fatos, datas, valores, citações, autoridades, pedidos, ressalvas, fecho ou assinaturas do conteúdo congelado.

Não marque uma página como revisada se não a abriu. Se qualquer imagem não puder ser lida, o veredito é `blocked`. Ausência de corte não basta para aprovação: completude e função cognitiva são gates separados.

## Severidade

- P0: alteração material, placeholder, conteúdo falso, diagrama enganoso, arquivo/hash divergente ou atestação sem inspeção.
- P1: falta de elemento obrigatório do padrão, margem visual estruturalmente vazia, diagrama ilegível, quebra grave, ou documento não apto à remessa interna como FORJA completa.
- P2: ajuste visual localizado que não impede a leitura nem muda a conclusão.

Responda SOMENTE com JSON válido:

{
  "reviewerModelRequested": "claude-opus-5",
  "verdict": "approved|approved_with_p2|blocked",
  "documents": [
    {
      "id": "...",
      "pageCount": 0,
      "pagesReviewed": [],
      "docxVectorDiagramCount": 0,
      "pullQuoteCount": 0,
      "visualElementsVerified": [],
      "p0": [],
      "p1": [],
      "p2": [],
      "approved": false,
      "summary": "..."
    }
  ],
  "p0Count": 0,
  "p1Count": 0,
  "p2Count": 0,
  "approvedForInternalResend": false,
  "summary": "..."
}
