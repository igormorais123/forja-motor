---
name: forja-pesquisa-jurisprudencia
description: 'Pesquisar jurisprudência na ordem de nove níveis determinada pelo Prof. Fábio (Diretriz 28), que persegue quem vai julgar e não a hierarquia abstrata dos tribunais, começando pela confirmação de órgão e relatoria no cadastro do CNJ e pelo TeiaJus antes de qualquer varredura nova. Use na fase F5 da FORJA, ao montar source_ledger e citation_checklist, e ao conferir citação remanescente em F7. Diferencial: garimpo-tribunais varre por tese e deep-research busca amplo; esta impõe a ordem do escritório, registra em que nível a peça se apoiou e trata os seis modos de falha de citação.'
metadata:
  adaptada_de: [garimpo-tribunais, deep-research]
  fases: [F5, F7]
  contrato: phase_contracts/F5.json
  criada_em: 2026-08-06
---

# Pesquisa de jurisprudência — F5

## A ordem não é opcional

Diretriz nº 28, transmitida pelo Dr. Alessandro em 28/07/2026. Percorra **nesta ordem**
e pare de subir quando encontrar material aderente:

1. STF — Plenário
2. **STF — pelo relator**, quando já há processo no tribunal ou prevenção, e pelos demais integrantes das turmas
3. STF — demais turmas
4. STJ — Órgão Especial
5. **STJ — pelo relator**, quando o processo já está no STJ ou há prevenção, e pelos demais integrantes das turmas
6. STJ — demais turmas
7. Tribunal local — Pleno ou Órgão Especial
8. **Tribunal local — decisões do relator**, quando já está no TJ ou há competência por prevenção
9. Tribunal local — da câmara ou turma julgadora, relatoria dos demais integrantes

Os níveis 2, 5 e 8 quebram a escada de propósito: a ordem **persegue quem vai julgar**.
E desde 06/08 o órgão julgador e a relatoria de qualquer processo se confirmam pelo
número no cadastro nacional do CNJ, sem depender de informação de terceiro — então
esses três níveis são a **primeira parada real**, não uma hipótese.

Sem competência ou relatoria conhecidas, a pesquisa fica genérica entre turmas e
câmaras dos respectivos tribunais — e isso se declara.

**O relatório de melhorias registra em que nível a peça se apoiou.** É o item que fecha
o ciclo com o titular.

## Sequência de trabalho

1. `forja-briefing-pesquisa` define o recorte, e também o que **refutaria** a tese.
   Pesquisa sem isso traz só o que confirma.
2. Confirmar órgão e relatoria no cadastro do CNJ (`forja-campo-tribunais`).
3. Consultar o TeiaJus: `python -m teiajus fontes` e depois a busca. Não abrir varredura
   nova sobre o que já está indexado.
4. `forja_legal_search.py` para a busca integrada (TeiaJus + STJ): `search`, `case`,
   `stj-search`, `stj-catalog`, `stj-daily`, `stj-datajud`.
5. Só então varredura ampla, se ainda faltar — `garimpo-tribunais` para levantar
   universo por tese.
6. Conferência nominal de **cada** citação que a peça vai usar, na fonte, por
   `forja-campo-tribunais`.

## Os seis modos de falha de citação

Existência do julgado **não prova** atribuição correta da frase. O checklist nominal:

| Modo | Pergunta que o resolve |
|---|---|
| inexistente | o julgado existe, com esse número, nesse tribunal? |
| nome trocado | o relator, o órgão e a data conferem? |
| misquote | a frase está no acórdão, com essas palavras? |
| pincite | está na página, item ou fólio indicado? |
| tese deturpada | é *ratio decidendi* ou *dictum*? |
| superado | continua vigente, ou foi superado por julgado ou tema posterior? |

A fábrica já mandou ao escritório peça com frase real atribuída ao precedente errado, e
com nota de rodapé não localizável. Nunca confie na memória do modelo.

Par súmula contra tribunal é gate próprio do `forja_verificador.py` — súmula do STJ
atribuída ao STF, e vice-versa, é achado recorrente.

## O checklist, em planilha

Uma linha por citação: tribunal, órgão, relator, número, data, trecho transcrito, onde
foi conferido, data da conferência, status. É de onde sai a lista de **citações não
conferidas nominalmente** que o `F7_VERIFICADOR_FORJA.json` exige — e é o que torna
contável o que em prosa vira "praticamente tudo conferido".

## Fontes já capturadas

`cache/fontes_oficiais/` guarda súmulas do STF e do STJ, o Tema 1368/STJ, o art. 406 do
Código Civil compilado, a Lei 14.905/2024 e a Selic acumulada do BCB, com data de
conferência. **Confira lá antes de citar.** Se faltar, capture: a API do BCB e o
Planalto respondem direto; SCON/STJ e STF só via Chrome real com o perfil `scraping`.

## Risco desta skill

Alto para fabricação. Busca por modelo produz número de acórdão, relator e data
plausíveis e inexistentes com a mesma fluência da verdade. **Nada que sai daqui é fonte
— tudo é candidato** até conferência na fonte oficial. A regressão de veneno de citação
(`test_forja_citacoes.py`) roda após qualquer mudança no processo de conferência.

## Critério de conclusão

- `source_ledger` com toda citação conferida nominalmente, ou listada como pendente.
- `citation_checklist` fechado, com o nível da Diretriz 28 em que a pesquisa parou.
- Recorte verbatim arquivado para cada citação que a peça usa.
- Vigência conferida, não presumida.

## Repertório das fases

`_FORJA_HARNESS\skills_repertorio\F5.md` e `F7.md`.
