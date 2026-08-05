# Runbook — auditoria de atualidade dos regimentos (FORJA-REGIMENTOS-v1)

Módulo: `forja_regimentos.py`. Regressão: `test_forja_regimentos.py` (14 casos, no `SUITES_SCRIPT` do baseline). Fecha o item **E11** do plano de execução, concluído em 26/07/2026.

## Por que existe

O protocolo da fábrica (`..\CLAUDE.md`) manda, para toda peça, ler o regimento do tribunal e conferir emendas posteriores à consolidação, porque a peça precisa refletir o regimento vigente **na data do protocolo**. Isso vinha sendo varredura manual por tribunal — e varredura manual não sobrevive ao tempo: dez pastas depois ninguém sabe qual arquivo está velho.

O obstáculo não era indisciplina, era falta de forma. Cada regimento arquivado usa cabeçalho diferente. Sem cabeçalho previsível não há auditoria; e uma auditoria que erra o parsing produz o pior resultado possível, que é declarar desatualizado um arquivo correto e mandar refazer trabalho pronto.

## Quando rodar

- Antes de redigir peça para tribunal cujo regimento importe (endereçamento, órgão competente, cabimento, prazo, sustentação oral, pauta);
- ao arquivar regimento novo em pasta de caso nova;
- na manutenção periódica do acervo, junto com o baseline.

## Comandos

```powershell
python forja_regimentos.py                      # audita a fábrica inteira (raiz = pasta-mãe)
python forja_regimentos.py --raiz DIR           # audita outra raiz
python forja_regimentos.py --limite-dias 30     # rigor de frescor (padrão 30)
python forja_regimentos.py --json               # saída estruturada
python forja_regimentos.py --hoje 2026-07-26    # data de referência, para teste
```

Varre recursivamente `REGIMENTO_INTERNO_*.md`, ignorando `.git`, `node_modules` e `__pycache__`. **Exit 1 se houver qualquer bloqueio; 0 caso contrário.**

## Códigos

| Código | Severidade | Significado |
|---|---|---|
| `sem_versao` | **P0** | o arquivo não declara até que emenda está consolidado |
| `sem_data_verificacao` | **P0** | não há data de conferência — e ausência de data não é data recente |
| `verificacao_vencida` | P1 | conferência mais antiga que o limite: o arquivo não está errado, está **por conferir** |
| `sem_fonte` | P1 | não há URL oficial de onde o texto veio |
| `sem_secao_emendas` | P1 | falta a seção "Emendas posteriores", onde entra o que veio depois da consolidação |

A regra de leitura é conservadora: **na dúvida, reporta desconhecido, nunca aprovado**. Verificação vencida é ressalva e não bloqueio, de propósito — tratá-la como erro faria o operador desligar a checagem.

## Cabeçalho auditável

O módulo tolera as variações que já existem no acervo, em vez de exigir retrofit. Reconhece três formas de cabeçalho — prosa, célula de tabela markdown e frontmatter YAML — e três formatos de data (`2026-07-23`, `09/07/2026`, `06 de julho de 2026`).

Um cabeçalho novo, escrito hoje, deve trazer:

```markdown
**Consolidação oficial vigente:** incorporado até o Assento Regimental nº 37/2026
**Fonte oficial:** https://www.trf4.jus.br/...
**Data da verificação e do download:** 2026-07-23

## Emendas posteriores
Nenhuma localizada até a data acima.
```

Rótulos de versão aceitos, do mais específico ao mais genérico: `Consolidação oficial vigente`, `Versão`, `Consolidado até`, `incorporado até`, `Última emenda`, `compilado até`, `versao:`/`versao_oficial:` (YAML), `Atualizado pelos Assentos Regimentais`, `Ato Normativo Base`. Rótulos de data: `Data da verificação`, `Data de Download`, `Conferido em`, `Baixado em`, os campos YAML `data_verificacao`/`data_download`/`download_em`/`data_conferencia` e, por último e deliberadamente fraco, `atualizado em`.

## O parser errou três vezes antes de acertar — não perder estas correções

Dos 8 bloqueios da primeira execução, **7 eram defeito do auditor, não do acervo**:

1. **Regex guloso** truncava a data em célula de tabela e devolvia data inválida. Pior que não achar: produz confiança falsa. Por isso o rótulo agora só localiza a **linha**; a data é extraída dela por `_extrai_data`.
2. **Frontmatter YAML ignorado** — metade do acervo traz a data na primeira linha, e o auditor acusava "sem data".
3. **Primeira data da linha, em vez da data depois do rótulo** — a linha de versão do TJRJ tem duas datas, e o parser devolvia 2024 para arquivo conferido em 2026. Daí também a ordenação por especificidade: "Data do download e conferência" tem de vencer "atualizado em".

Por isso a regressão fixa **quatro cabeçalhos reais do acervo** (TRF4/CASO-23, STJ/CASO-04, TJDFT/plano de saúde, TRF1/tabela) como não-travas.

## Estado do acervo em 26/07/2026

**16 arquivos · 0 com bloqueio · 0 com ressalva · 16 em ordem.**

| Tribunal | Arquivos | Consolidação | Conferido em |
|---|---:|---|---|
| STJ | 4 | ER 47, de 19/12/2024 (+ ER 48 a 53 na seção de emendas) | 06/07/2026 |
| TJDFT | 1 | ER 36 | 09/07/2026 |
| TJRJ | 1 | consolidado, vigente desde 09/03/2024 | 09/07/2026 |
| TJSP | 1 | compilação de 30/04/2026 | 15/07/2026 |
| TJTO | 1 | Resolução 104/2018 (republicação) | 06/07/2026 |
| TRE-PR | 1 | Res. 792/2017 compilada até a Res. 957/2025 | 26/07/2026 |
| TRF1 | 3 | ER 1 a 5 (até 11/04/2022) | 06/07/2026 |
| TRF2 | 1 | 14ª edição, até a ER 56, de 07/05/2026 | 20/07/2026 |
| TRF4 | 3 | AR 37/2026 (CASO-23); AR 35 nos dois legados | 23 e 06/07/2026 |

### Conferência em fonte oficial feita nesta rodada

- **TRF4**: AR 37/2026 é o mais recente — sem posterior.
- **TRF2**: ER 56, de 07/05/2026 — sem posterior.
- **TRE-PR**: Res. 792/2017 compilada até a Res. 957/2025.
- **TRF1**: nenhuma emenda posterior à ER 5/2022 localizada.
- **TJSP**: **os AR 594/2026 e 595/2026 são posteriores à compilação arquivada de 30/04/2026** (alteram o art. 29-A e incluem o 29-F). Ressalva registrada dentro do próprio arquivo, delimitando as matérias comprometidas.

### Decisões de manuseio que devem ser repetidas

- Os dois arquivos do TRF4 parados no AR 35 (Jalusa e Memoriais Cautelar Fiscal) receberam **aviso expresso de desatualização** com a lista do que mudou e o endereço da íntegra atual. O corpo **não** foi reescrito: substituir texto de regimento por conta própria destrói rastreabilidade.
- Onde a conferência dependia de diário eletrônico não aberto (TJTO, TJRJ), a pendência ficou **declarada no próprio arquivo**, não suprida.

## Limites

A auditoria confere **metadados de atualidade**, não conteúdo. Ela diz que o arquivo declara estar consolidado até a emenda X e que isso foi conferido em tal data; não diz que o texto do arquivo corresponde ao texto oficial, nem que a emenda X é a última existente hoje. A conferência na fonte oficial continua sendo ato humano — este módulo apenas impede que ele seja esquecido.
