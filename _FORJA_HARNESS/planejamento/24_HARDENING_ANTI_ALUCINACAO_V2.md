# Hardening anti-alucinação v2 — plano, execução e rollback

Data: 23/07/2026  
Método operacional: Efesto  
Escopo: F5, F7/F7-B, F9/F10 e pacotes já produzidos.

## Resultado pretendido

Nenhuma peça protocolável pode ser liberada apenas porque um JSON declarou
`pass`, porque existe um arquivo com nome convincente ou porque uma revisão
humana assinou uma afirmação genérica. A autoridade citada, a fonte oficial, o
trecho probatório, a proposição efetivamente escrita e o Markdown final precisam
formar uma cadeia verificável e hash-bound.

Isso reduz o risco; não cria garantia absoluta de correção jurídica. A leitura
humana continua responsável por contexto, ratio decidendi, vigência, distinção e
adequação da tese ao caso.

## Ameaças tratadas

| ID | Ameaça | Controle v2 |
|---|---|---|
| AH-01 | HC, RMS, Rcl ou norma escapam do extrator | inventário canônico compartilhado por F5/F7 |
| AH-02 | recibo assina claim genérico, mas a peça afirma outra coisa | vínculo a documento, parágrafo, proposição e autoridade |
| AH-03 | peça protocolável é rotulada como interna | classificação por papel, audiência e conteúdo; política só pode aumentar |
| AH-04 | pacote antigo continua “pronto” após mudança da régua | versão/hash da política e revalidação no draft, entrega e fulfillment |
| AH-05 | edição troca “não autoriza” por “autoriza” | assinatura de polaridade semântica ligada à autoridade |
| AH-06 | F10 legado confia em arquivo existente ou `p0=0` | recomputação do Markdown e exigência do pacote N3/v2 |

## Onda de implementação

1. Unificar o inventário de jurisprudência e normas.
2. Elevar o recibo humano jurídico para v2.
   O binder determinístico prepara os hashes, mas nunca assina.
3. Fazer F7 promover `verified_source_ledger` somente após recomputação.
4. Fazer F9/F10 revalidarem a política atual.
5. Bloquear inversões semânticas na revisão editorial.
6. Auditar pacotes históricos sem mutar estado.
7. Executar regressões unitárias, adversariais, integração e mapas.

Não há migração automática de recibos ou pacotes. Converter um recibo v1 em v2
sem nova leitura humana criaria prova fictícia.

## Critérios de aceite

- HC, RMS, RHC, MS, Rcl, classes STJ/STF cobertas, artigos e leis aparecem no inventário.
- autoridade de corte ambígua bloqueia `strict_protocol`;
- o recibo v2 falha se documento, parágrafo, proposição ou autoridade mudarem;
- `final_markdown` falso não é coberto por claim genérico;
- rebaixamento de peça protocolável falha;
- pacote schema v1 ou com política antiga é `stale`;
- F10 legado não fecha sem pacote canônico v2;
- inversão de negação ligada a autoridade falha;
- testes existentes não sofrem regressão.

## Rollback

Os arquivos de produção e o estado dos casos não são migrados nesta onda.
Rollback de código deve restaurar somente os arquivos listados no relatório de
execução da mudança e remover os novos módulos/documentos. Não usar reset amplo
porque o worktree contém alterações alheias. Pacotes v2 já gerados devem
permanecer arquivados e apenas perder a condição de liberáveis; nunca ser
reescritos em lugar.
