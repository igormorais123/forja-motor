---
name: forja-campo-tribunais
description: 'Acessar fontes oficiais e portais de tribunal que só respondem a navegador real com sessão — e-SAJ, PJe, projudi, DJEN, SCON/STJ, STF e o cadastro nacional do CNJ — para baixar a íntegra do ato, o regimento vigente, confirmar órgão julgador e relatoria, e reproduzir citação ao vivo. Use ao buscar documento dos autos, conferir citação na fonte, auditar atualidade de regimento ou confirmar composição do órgão. Diferencial: testar-navegador é QA de site; esta é coleta processual com regra de cache, identidade do ato e o que pode ou não virar referência na peça.'
metadata:
  adaptada_de: [testar-navegador]
  fases: [F1, F3, F5, F7]
  criada_em: 2026-08-06
---

# Campo — fontes oficiais e portais

> **A porta da esteira é a skill `forja`.** Ela traz o fluxo inteiro, de F0 a F10, os
> comandos, os gates e as ordens invioláveis. Esta ficha detalha um ponto do caminho e
> pressupõe aquela leitura — abra-a primeiro se você chegou aqui sem contexto.

Chrome real com perfil persistente (`scraping`). Esta é a rota para o que exige sessão
autenticada e para as fontes que não respondem a busca simples.

## Antes de abrir o navegador: três verificações que economizam horas

1. **O TeiaJus já tem?** São 33.591 casos e 12 fontes indexados.
   `python -m teiajus fontes` diz o que ele cobre. Mas atenção: o score do TeiaJus
   ordena a fila; **evidência documental sustenta afirmação**, e prova documental existe
   em 2.155 casos, não nos 33 mil.
2. **Já está em `cache/fontes_oficiais/`?** Com data de conferência. E a regra **muda
   conforme a fase**:
   - **F1, F3 e F5** — cache recente serve; não recolete.
   - **F7** — não serve. O gate `live_official_source_replayed` exige reprodução ao
     vivo, e `source_excerpt_hash_match` compara o recorte. Só vale cache com hash e
     data conferidos **nesta rodada**. Reaproveitar cache antigo aqui é burlar o gate.
3. **A fonte responde sem login?** Planalto e a API do BCB respondem direto — use
   `fetch-rendered`, que é ordens de grandeza mais barata. SCON/STJ e STF **não**: só
   por aqui.

## O que só sai por esta rota

| Alvo | Para quê | Fase |
|---|---|---|
| Íntegra do ato impugnado | sem ela a produção fica `internal_working` | F1 |
| Regimento interno consolidado vigente | gate `regimento_available` | F3 |
| Emendas regimentais posteriores à consolidação | a peça reflete o regimento vigente **na data do protocolo** | F3 |
| Órgão julgador e relatoria pelo número no cadastro do CNJ | níveis 2, 5 e 8 da Diretriz 28 | F3, F5 |
| Composição **atual** da turma ou câmara | nunca de memória | F3 |
| Recorte verbatim de acórdão em SCON/STJ e STF | `source_excerpt_hash_match` | F5, F7 |
| Reprodução ao vivo da fonte citada | `live_official_source_replayed` | F7 |

## Regimento: o cabeçalho não prova vigência

Nenhum `REGIMENTO_INTERNO_<TRIBUNAL>.md` da fábrica pode ser tratado como vigente pelo
que está escrito nele. O procedimento é: abrir o cabeçalho de metadados do arquivo
(fonte, versão, data do download), ler a seção final de emendas posteriores, e
**pesquisar na fonte oficial o que saiu depois disso**. As emendas encontradas entram
na seção "Emendas posteriores" do próprio .md.

```
python _FORJA_HARNESS\forja_regimentos.py
```

Sai com código 1 quando bloqueia. Runbook: `RUNBOOK_AUDITORIA_REGIMENTOS.md`.

## Citação: existir não é bastar

A taxonomia da casa tem seis modos de falha, e a rota de campo resolve os que dependem
da fonte:

- **inexistente** — o julgado não existe.
- **nome trocado** — existe, com outro número ou outro relator.
- **misquote** — a frase não está no acórdão, ou está com outras palavras.
- **pincite** — a frase existe, em página ou item diferente do indicado.
- **tese deturpada** — a frase é *dictum*, e foi citada como *ratio*.
- **superado** — o precedente existe e não vale mais.

Trazer a **íntegra**, não a ementa. Misquote e tese deturpada nascem na ementa.

## O que fazer com o que se coletou

- Arquivar em `cache/fontes_oficiais/` com data de conferência e a URL exata.
- Guardar o recorte verbatim; é o que o gate compara por hash.
- **Caminho local, URL do Drive e nome de arquivo nunca entram na peça.** A peça usa
  referência processual verdadeira; a origem operacional vive só no ledger.

## Falhas conhecidas desta rota

- Não roda em execução agendada nem headless — depende de sessão viva.
- Portal cai, certificado expira, sessão morre no meio. Trate como esperado.
- Captcha e limite de consulta existem. Não contorne: registre como insumo bloqueado
  com a causa "indisponibilidade na fonte" ou "limitação da ferramenta".
- Varredura por parte não sai de fonte pública genérica: o DJEN indexa parte com polo,
  e o título do arquivo não é conclusão. O valor da causa não está no cadastro do CNJ.

## Critério de conclusão

- O documento buscado está em mãos, ou existe `F1_INSUMO_BLOQUEADO.json` com a causa
  correta do vocabulário fechado — nunca "não localizado".
- Cada citação conferida tem recorte verbatim e data de conferência.
- Órgão e relatoria confirmados pelo cadastro, não por informação de terceiro.

## Repertório das fases

`skills_repertorio\F1.md`, `F3.md`, `F5.md`, `F7.md`.
