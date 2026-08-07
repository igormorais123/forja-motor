# Revisão cruzada do repertório — Codex GPT-5.5, 06/08/2026

Produtor: Claude Opus 5. Revisor: Codex GPT-5.5, família distinta, `reasoning: high`,
105.044 tokens. `familyAssurance` deste artefato: `cross_family`.

## Como a revisão foi feita, e por que isso importa

A primeira tentativa falhou de um jeito que vale registrar: o sandbox do Codex nesta
máquina negou spawn de processo (`CreateProcessAsUserW failed: 5`), e ele **não
conseguiu abrir um único arquivo**. Se o parecer tivesse sido aceito assim, seria o modo
de falha que a casa já conhece — parecer sem fonte com cara de parecer.

A segunda tentativa entregou o material **integral por stdin**: os 11 contratos de fase,
o argparse real de 11 scripts, o `CLAUDE.md` inteiro, os 14 arquivos do repertório e as
7 skills adaptadas. Assim a revisão foi sobre o texto real, não sobre memória do modelo.
Detalhe operacional que se repetiu: `codex exec` trava esperando stdin quando o prompt
vem por argumento — resolve com `< /dev/null`.

## Achados aplicados

**Risco de dano (os mais graves).**

1. O fluxo mandava **enviar o e-mail em F9**, antes da fase contratual de entrega. F9 é
   `PACOTE_REVISAO_DRAFT_OPCIONAL`; `delivery_evidence` e `external_identifier_valid`
   são de F10. Corrigido: F9 produz e **congela** o rascunho; o envio é F10.
2. O registro no painel também estava antecipado para F9 — o gate é `management_synced`,
   de F10. O próprio texto de F9 descrevia o dano ("painel dizendo entregue e caixa
   vazia") e mandava fazer assim mesmo. Corrigido.
3. A regra "cache recente, não recolete" da `forja-campo-tribunais` podia **burlar** o
   `live_official_source_replayed`. Corrigido: a regra passou a ser modulada por fase —
   cache serve em F1, F3 e F5; em F7 só evidência reproduzida nesta rodada.

**Contradição com regra inviolável.**

4. O cardápio dizia "nenhuma skill é obrigatória, salvo Helena e Cícero", mas o
   `CLAUDE.md` torna `fabrica-visual-peticoes` e `padrao-visual-medina` obrigatórias em
   toda peça. São **quatro** exceções, agora nomeadas no `LEIA-ME.md` e marcadas com
   `obrigatoria: true` no catálogo, cada uma com o fundamento normativo.
5. F3 omitia duas obrigações invioláveis: a leitura de `_LEIS_GERAIS` (OAB e LOMAN) e o
   registro, no relatório de melhorias, de **quais** dispositivos foram considerados e
   **como** impactaram a peça. Acrescentadas como seção própria, declaradas como
   obrigação sem skill.

**Fato errado.**

6. A síntese executiva estava atribuída ao gate **S7**. S6 é identidade do ato recursal
   e S7 é tema fora do `objeto.devolvido` — nenhum dos dois. A síntese é inviolável e
   **não tem gate lexical próprio**, o que muda quem a garante: pessoa, não script.
   Corrigido em `F6.md` e em `forja-saida-humana`.
7. A pergunta jurisdicional aparecia como critério de conclusão de F2; o gate
   `jurisdictional_question_defined` é de **F4**. Passou a ser antecipação e handoff.
8. `F2_IDENTIDADE_PROCESSUAL.json` era apresentado como se fosse saída de F2. É artefato
   **auxiliar**, produzido por `forja_identidade_processual.py`; existe e o gate S6 o lê,
   mas não consta de `F2.json`. Declarado como tal.
9. A tabela do cardápio mestre prometia "o que a fase entrega" e listava só parte.
   Renomeada para "principais entregas", com a ressalva de que só o contrato vale.
10. F5 admitia fechar com citação "pendente". Citação **destinada à peça** pendente
    impede fechar F5 — `official_sources_archived` e `quotes_compared` cobram. Pendente
    só vale para candidato descartado ou não usado, e a lista diz qual é qual.
11. O template `F10_EMAIL_RETORNO_E_AGRADECIMENTO.md` estava listado em F9. É do ciclo
    pós-retorno, de F10. Removido.
12. F7 dizia ter 22 gates; tem 21. (Achado pela verificação própria, não pelo Codex.)

**Lacuna.**

13. `F5.json` tem `conditionalGates.economic` com três gates que eu não havia lido —
    `fonte_prevalente_validada`, `data_base_registrada`,
    `documentos_economicos_inventariados`. `F7.json` tem outros cinco. Ambos agora têm
    seção própria, com a nota do contrato que importa: **proposta não equivale a
    validação humana** da fonte prevalente.
14. Sete gates de F7 e cinco de F8 não têm skill que os satisfaça — recibo assinado por
    pessoa, trust store externo, recomposição pelo orquestrador. Criada em cada um a
    seção **"gates sem skill"**, que diz qual é a rota real. Nenhuma skill foi inventada
    para preencher.
15. Os três artefatos de memória de auditoria de F9 saem do `forja_package.py`.
    Declarado.
16. `forja_fronteira.py` virou recurso transversal nomeado, com os comandos, em vez de
    a fronteira aparecer só como pergunta abstrata.

**Contradição interna.**

17. "A degradação não para o caso" contra "em `strict_protocol` só `cross_family`
    libera". Precisado: o trabalho interno continua, a **promoção** fica bloqueada.
18. O repertório se dizia opcional e chamava duas skills de "único caminho". Corrigido:
    obrigatório é o **resultado contratual** — a evidência recomputável —, não a
    implementação. Qualquer executor que a produza serve.
19. `ai-image-generation` estava em F9 no catálogo e proibida em F9 no markdown.
    Resolvido: F8 apenas, em material institucional separado do pacote de entrega.
20. "Sem brief é comportamento esperado" contra "nenhuma peça sai sem visual completo".
    Precisado: recusar-se a inventar figura é correto; entregar sem piso gráfico não é.
    O estado sem brief bloqueia a saída.

**Schema do catálogo.** `dependenciaExterna` virou lista (informação estava sendo
perdida no campo singular); `google-workspace` ganhou `reversibilidadePorOperacao`
(busca, download, rascunho e envio não têm o mesmo risco); `alimenta` foi duplicado em
`alimentaArtefatos` com nota de que o campo legado mistura artefato e gate; `diabob`,
`inteia-review-iterativo` e `revisar-anti-ia` foram marcadas `status: preterida` com o
campo `preferir` apontando a adaptada; `forja-revisao-cruzada` recuperou a fase F6.

## Achados verificados e derrubados

Três achados P1 do Codex **não** se sustentaram na conferência do código. Ficam
registrados porque a próxima revisão vai reencontrá-los:

| Achado | Por que caiu |
|---|---|
| "O executor de F7-B deve ser `forja_fable5.py`, como manda o `CLAUDE.md`" | `forja_editorial.py` tem 25,8 KB e é o executor real; `forja_fable5.py` tem 1,8 KB e o `INDICE_FORJA.md` o declara shim legado. **O `CLAUDE.md` é que está desatualizado.** Registrado como divergência declarada, não corrigido no repertório |
| "A Diretriz 28 é percorrida em F3, como manda o `CLAUDE.md`" | O contrato de F3 é `F3_FONTES_REGIMENTO_LEIS`; a fase de pesquisa é `F5_PESQUISA_OFICIAL`, que produz `source_ledger` e `citation_checklist`. Divergência real entre `CLAUDE.md` e contratos — o repertório passou a **expor** o conflito em vez de escolher em silêncio |
| "O gate `no_pdf_or_raster_rendering` contradiz o PDF final obrigatório" | Lido em `forja_f8_contract.py`, o gate exige `renderingUsed`, `pdfCreated` e `pngCreated` falsos com `mode == "static_ooxml_svg"`: ele diz que **a QA não rasterizou**, não que a entrega não tem PDF. O texto foi reescrito para não induzir ao erro, mas o gate está certo |

## Achado aceito em parte

O Codex apontou **excesso**: as fichas e as narrativas históricas se repetem entre as
fases, contra o objetivo de economia de contexto. A repetição das **fichas** é
deliberada e continua — é o que permite ler um arquivo só. A crítica procede quanto à
**narrativa**: incidente e justificativa histórica repetidos em cinco arquivos são peso
morto. Fica como dívida declarada, não corrigida nesta rodada, porque cortar narrativa
sem critério tira também o motivo pelo qual a regra existe — e regra sem motivo é a que
some na rodada seguinte.

## O que esta revisão prova, e o que não prova

Prova que o repertório foi lido por outra família de modelo contra os contratos, o
código e o protocolo, e que 20 achados viraram correção. **Não** prova que o repertório
está correto: gates automáticos e revisão cruzada são escudos, não certificado
semântico. A primeira peça que passar por ele é o teste de verdade.
