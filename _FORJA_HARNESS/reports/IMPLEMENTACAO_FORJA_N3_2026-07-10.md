# FORJA N3 — IMPLEMENTAÇÃO, REVISÃO E AUDITORIA FINAL

## Veredito

A arquitetura N3.0-r2 foi implementada de forma aditiva. A camada de gestão está ativa; os componentes que alteram o ciclo produtivo permanecem em sombra até os bloqueios do corpus serem resolvidos. A N2 não foi removida nem reescrita.

## Capacidades entregues

1. **Estado confiável:** eventos atômicos, sequência contínua, `expectedRevision`, idempotência, lock curto, reconstrução e reabertura formal de gate.
2. **Execução isolada:** cada agente trabalha em `runs/<run>/<fase>/<tentativa>`; somente resultado aprovado por contrato é promovido.
3. **Contexto rastreável:** índice documental, cobertura por página, fatos classificados, proposições e vínculo de cada bloco argumentativo.
4. **Fidelidade semântica:** comparação Markdown→Word→PDF por blocos, números, datas, percentuais e ressalvas como “não”, “salvo” e “subsidiariamente”.
5. **QA visual V2:** parser SVG/XML, detecção de texto fora da área, sobreposição, forma opaca posterior, linhas sobre texto, vazamento Markdown, páginas vazias/cortadas e revisão independente.
6. **Pacote fechado por identidade:** artefatos escolhidos por ID, hash e tamanho; F7, contexto, fontes, fidelidade, F8, e-mail e anexos precisam corresponder à mesma versão.
7. **Fechamento F10:** entrega exige evidência, sincronização da gestão, métricas e retrospectiva íntegras.
8. **Gestão viva:** 20 estados vinculados ao sidecar; a 21ª demanda aparece como `not_run`; nenhum status foi escrito em `demandas.json`.
9. **Abertura segura:** artefatos e pacotes são resolvidos por ID e hash; espaços e acentos têm teste próprio.
10. **Word resiliente:** conversão em processo privado, PDF temporário, promoção atômica, limite de tempo e uma retomada; processo travado é encerrado sem tocar no Word visível do usuário.

## Falhas encontradas e corrigidas durante a implementação

| Falha | Correção |
|---|---|
| existência de artefatos invertida no sidecar | N3 exibe somente arquivo existente; legado não oferece link sem hash |
| teste F7 dependia da pasta de execução | caminho passou a ser relativo ao próprio harness |
| headless N3 podia gravar estado antigo | em N3 escreve somente dentro da tentativa; N2 permanece compatível |
| gates legados apareciam como `0: unknown` | normalização por código e severidade |
| N2 podia substituir vínculo N3 | N3 canônica tem precedência; troca N3→outro caso é rejeitada |
| replay em cópia temporária atualizava o sidecar como se fosse caso real | ponte aceita apenas casos diretamente em `state/`; reconciliação rebaixa entrada N3 sem estado canônico e restaura o N2 real |
| ponte de gestão devolvia revisão anterior ao ACK | estado retornado é recalculado após sincronização |
| importação esquecia a fase mais alta do legado | F9→F5 agora exige `gate_reopened` |
| Súmula 5 tinha cache sem URL oficial completa | URL SCON corrigida; tese atribuída à súmula errada voltou a ser detectada |
| Word travava e o `finally` falhava | worker isolado, limpeza defensiva, timeout e retry |
| pacote podia publicar ponteiro antes do evento | ponteiro só é promovido depois do evento canônico |
| recibo de draft ignorava `artifactId` | comparação exata de ID + hash + bytes |
| F10 encerrava sem métricas/retrospectiva | ambos agora são artefatos obrigatórios e verificados |
| F7 podia pertencer a Markdown antigo | `mdSha256` obrigatório e comparado no pacote |
| não havia prova MD→DOCX→PDF | `forja_fidelity.py` e gate `semantic_fidelity_pass` |
| JSON visual Patrícia/Fábio inválido | caminho normalizado; texto pré-correção preservado ao lado |

## Replay do acervo

- 21/21 estados N2 reproduzidos em cópia temporária.
- 21/21 hashes originais preservados.
- 15 casos compatíveis sem bloqueio estrutural.
- 6 casos bloqueados pela N3.
- 20 SVGs examinados; 9 reprovados.

Bloqueios objetivos:

- **Plano de Saúde:** regressão F9→F5 e Tema 1.365 ainda com `finalUseAllowed=false` no ciclo de revisão.
- **Azimut:** 1 SVG reprovado.
- **CORSAN:** 3 SVGs reprovados.
- **Libra Sul:** 2 SVGs reprovados.
- **Natura:** 2 SVGs reprovados.
- **Patrícia/Fábio:** 1 SVG reprovado; o JSON inválido foi corrigido.

Os diagramas históricos não foram reescritos. Eles permanecem como corpus para provar que o gate captura o defeito.

## Verificação executada

- 11/11 grupos do validador aprovados.
- 44 testes unitários N3 após as correções finais.
- 11/11 contratos de fase válidos.
- 82 arquivos JSON verificados no ciclo consolidado, sem inválido.
- Telemetria real: três produtos, 60 páginas Word/PDF e 15 DOCX históricos; zero P0 e zero processo Word órfão.
- Painel validado em 1440×900 e 390×844, sem estouro horizontal.
- `demandas.json` não foi alterado pela reconciliação final: SHA-256 antes/depois `479A2A9211C25B9C7383D324EF81E8A3A949679267330B2CB9A44A45E0A607A9`.
- Replay temporário provado sem efeito no sidecar por comparação de hash; o sidecar final contém 20 estados `N2.0-compat`, sendo 14 compatíveis e 6 bloqueados pelo replay. A demanda sem caso continua `not_run` na junção do painel.

Relatórios verificáveis: `N3_VALIDATION_2026-07-10.json` e `N3_SHADOW_REPLAY_2026-07-09.json`.

## Estado de promoção

Não promover N3 como padrão ainda. Faltam:

1. corrigir ou justificar formalmente os nove SVGs reprovados;
2. resolver a regressão e a fonte pendente do Plano de Saúde;
3. concluir três casos novos completos com eventos, contexto, fidelidade, pacote, draft, entrega e painel sem divergência.

Até isso ocorrer, os flags produtivos permanecem limitados à gestão. Essa decisão evita quebrar o fluxo atual e cumpre o plano de promoção gradual.
