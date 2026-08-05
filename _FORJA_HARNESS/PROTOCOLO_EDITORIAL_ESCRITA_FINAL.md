# Protocolo editorial — revisão e escrita final

**Versão do bundle:** `FORJA-FABLE5-FINAL-v1` (identificador mantido para não invalidar os bundles já promovidos)
**Vigência:** 15/07/2026, com a supersessão de 25/07/2026 registrada abaixo
**Posição:** subfase bloqueante `F7-B_REVISAO_EDITORIAL_ESCRITA_FINAL`, depois da auditoria jurídica/factual e antes de F8.

## 0. Supersessão de 25/07/2026 — modelo editorial e revisão cruzada

A determinação de 15/07/2026, que fixava o Claude Fable 5 como redator editorial
final, **foi superada por determinação do titular do projeto em 25/07/2026**. Ambas
foram registradas como invioláveis; prevalece a mais recente, e este parágrafo
existe para que a próxima leitura não encontre duas ordens em conflito.

O que mudou:

1. **O modelo editorial padrão passa a ser o `claude-opus-5`.** O Fable 5 continua
   autorizado, como legado, na allowlist de `forja_editorial_model.py`.
2. **O modelo deixou de ser constante do código.** Vem da allowlist e do contrato
   do run. O que não mudou é a única coisa que realmente protegia a fase: o
   orquestrador confere no envelope do executor qual modelo consumiu tokens e
   nunca aceita a autodeclaração do relatório.
3. **A revisão entre famílias distintas de modelo passou a ser gate de produção.**
   O trabalho pode nascer no Claude ou no Codex, mas a outra família revisa. O
   campo `familyAssurance` assume `cross_family`, `cross_session_same_family` ou
   `unverified`, e o gate `cross_model_review_verified` bloqueia o último em
   qualquer modo. Em `strict_protocol`, só `cross_family` libera.
4. **A degradação é permitida e nunca é silenciosa.** Sem a segunda família
   disponível, o caso não para: rebaixa para `cross_session_same_family` com o
   motivo registrado, e fica bloqueado apenas para liberação estrita.
5. **Artefatos renomeados:** `FABLE5_RESULT*.json` passou a `EDITORIAL_RESULT*.json`
   e `fable5_usage` passou a `editor_usage`. Escritores emitem os nomes novos;
   leitores continuam aceitando os antigos, para que tentativas promovidas antes
   desta data sigam validando.

## 1. Finalidade

O Fable 5 é o redator editorial final da FORJA. Ele recebe um texto já aprovado na auditoria F7 e melhora clareza, fluidez, ritmo, coesão, concisão, precisão vocabular e organização retórica. Ele não pesquisa, não completa lacunas, não muda estratégia e não aprova a própria saída.

`final_markdown` é o cânone textual de F8 e dos pacotes novos. `audited_markdown` permanece imutável como origem e trilha de auditoria.

Antes de devolver o texto, o Fable executa `FORJA-GOSTO-EDGE-v1`: concebe três
direções editoriais, rejeita a versão óbvia, escolhe por poder de decisão,
especificidade, lastro e economia, e registra a seleção em `gostoJuridico`.
Esse processo não amplia a autoridade editorial: todas as invariantes abaixo
continuam prevalecendo.

## 2. Gate zero

Como regra do workflow, F7-B só pode iniciar quando:

- existe `audited_markdown` não vazio;
- existe resultado auditável de F7;
- não há achado P0 aberto;
- fatos e fontes materiais já foram conferidos;
- pedidos, ressalvas, fecho e assinaturas já estão definidos;
- o texto não contém os marcadores reservados do envelope Fable.

Se qualquer condição falhar, a peça volta à etapa responsável. Fable 5 não é ferramenta de cura de bloqueio jurídico. O executor standalone verifica imediatamente apenas a existência dos arquivos e a ausência recursiva de `p0 > 0`; os demais gates F7 são impostos pelo resultado integral e pela promoção. Portanto, ausência de P0 isolada não equivale a aprovação jurídica completa.

## 3. Autenticação e custo

O executor chama o Claude Code instalado localmente e exige:

- `loggedIn=true`;
- `authMethod=claude.ai`;
- `subscriptionType=max`;
- modelo efetivo igual ao declarado no contrato do run e presente na allowlist editorial; por padrão `claude-opus-5`, solicitado pelo alias `opus`.

O fluxo usa a assinatura OAuth Claude Max do Igor. Não aceita API key e não possui fallback automático para cobrança de API. O texto auditado integral é processado remotamente pela conta `claude.ai` do Igor. O prompt segue por `stdin`, evitando o limite de linha de comando do Windows, e a sessão editorial não recebe ferramentas.

## 4. Invariantes

Fable 5 não pode criar, retirar ou alterar:

- fatos, eventos, sujeitos e relações processuais;
- números, valores, percentuais, datas e prazos;
- dispositivos, precedentes, autoridades e números de processo;
- citações diretas e seus sentidos;
- identificadores de evento, ID, folha, e-STJ ou documento;
- premissas, ressalvas, teses, argumentos e pedidos;
- endereçamento, fecho e assinaturas;
- marcadores internos que deveriam permanecer apenas na auditoria.

Também é proibido introduzir referência à origem operacional dos insumos — e-mail, WhatsApp, Drive, pasta, caminho local ou compartilhamento — no texto protocolável.

## 5. Execução

```powershell
python forja_fable5.py <case-dir> <attempt-dir> --source audited_markdown.md --f7-gate f7_gate_result.json
```

Para um segundo documento na mesma tentativa:

```powershell
python forja_fable5.py <case-dir> <attempt-dir> --source audited_markdown_nota.md --f7-gate f7_gate_result.json --artifact-suffix _nota
```

O sufixo precisa ser um identificador seguro e é aplicado a todo o bundle. O consumidor deve parear artefatos pelo sufixo, não apenas pelo prefixo.

## 6. Artefatos

| ID | Arquivo padrão | Papel |
|---|---|---|
| `audited_markdown` | `audited_markdown.md` | origem imutável aprovada em F7 |
| `final_markdown` | `final_markdown.md` | texto final canônico |
| `editorial_report` | `editorial_report.json` | declaração estruturada e métricas da edição |
| `editorial_diff` | `editorial_diff.patch` | mudanças linha a linha para auditoria humana |
| `fable5_usage` | `fable5_usage.json` | sessão, modelo, autenticação e hashes |
| `editorial_fidelity` | `editorial_fidelity.json` | recomposição local dos gates |
| fragmento | `FABLE5_RESULT.json` | artefatos e gates para `PHASE_RESULT.json` |

## 7. Gates determinísticos

O modelo devolve texto e relatório, mas a FORJA recalcula os critérios. A promoção exige os quatro gates contratuais:

| Gate | Prova exigida |
|---|---|
| `fable5_oauth_confirmed` | OAuth Claude Max e modelo canônico comprovados |
| `editorial_source_hash_match` | relatório e uso apontam para o SHA-256 real da origem |
| `editorial_fidelity_pass` | invariantes de conteúdo e proveniência aprovados |
| `human_style_final_pass` | texto final passa no protocolo de escrita humana |

O gate de fidelidade compara, entre outros itens, números, datas, autoridades, processos, citações, headings, pedidos, fecho, origem operacional e retenção de conteúdo não branco. O piso vigente de retenção é 90%; ele é um detector de perda grosseira, não permissão para eliminar 10% da peça.

O campo `duvidas` do relatório do Fable não é autocertificante nem possui gate automático. Antes de F8, uma pessoa deve classificá-lo: dúvida material sobre fato, tese, estrutura, pedido ou sentido bloqueia a composição e volta a F7; dúvida apenas editorial pode ser mantida com decisão registrada.

O executor também exige que `gostoJuridico` contenha: protocolo correto, versão
óbvia rejeitada, três direções distintas, uma única direção selecionada, duas
âncoras literais existentes tanto na origem quanto no texto final e consequência
sem dramatização. Recibo ausente ou inconsistente descarta a candidata e aciona
o retry. O recibo prova que o processo foi declarado e que as âncoras existem;
não prova, isoladamente, que a escolha foi superior. Essa comparação pertence
ao julgamento cego do AUTO-RESEARCH.

## 8. Retry e bloqueio

Cada chamada tem limite de 1.800 segundos. O executor admite no máximo três candidatas internas no total — a inicial e até dois retries. Se uma candidata reprovar fidelidade, ela é descartada. Cada retry:

1. parte de `audited_markdown` original;
2. recebe os achados determinísticos da tentativa anterior;
3. não herda a redação rejeitada;
4. precisa refazer todos os gates.

Depois de três reprovações, a tentativa permanece bloqueada e nenhum artefato é promovido. Timeout, autenticação inválida, modelo não comprovado, envelope malformado ou hash divergente falham imediatamente.

## 9. Promoção e F8

O fragmento `FABLE5_RESULT*.json` deve ser incorporado ao resultado integral da fase. Ele não substitui `PHASE_RESULT.json`: preserve o produtor `forja-auditor-juridico`, o revisor `forja-gate-controller` e todos os demais artefatos/gates de F7. `forja_run.py` não chama o Fable automaticamente; na promoção, ele recompõe cada bundle `final_markdown*` contra `audited_markdown*`, `editorial_report*` e `fable5_usage*`. Um par ausente, trocado ou adulterado bloqueia a promoção.

O comando direto `python forja_editorial_fidelity.py <audited> <final> <report>` é útil para comparação textual, mas não recebe `fable5_usage.json` e, sozinho, não recompõe a prova OAuth completa. Para aceite, use o executor e as validações da promoção/pacote.

F8 compõe o documento a partir de `final_markdown*`. O pacote revalida o bundle referente ao entregável selecionado. Pacotes históricos continuam legíveis segundo o contrato de sua época, mas tentativas F7 novas não podem usar essa compatibilidade para contornar F7-B.

## 10. Falhas e resposta operacional

| Sintoma | Classificação | Ação |
|---|---|---|
| F7 contém P0 | bloqueio jurídico | corrigir em F6/F7; não chamar Fable |
| Claude Code ausente | bloqueio de ambiente | instalar/restaurar o comando e repetir |
| conta não é OAuth Max | bloqueio de autenticação | autenticar na assinatura correta; não usar API paga |
| modelo efetivo divergente | bloqueio de proveniência | interromper e verificar disponibilidade/alias |
| timeout | bloqueio operacional | preservar origem; diagnosticar e repetir conscientemente |
| saída sem marcadores/JSON válido | bloqueio de contrato | descartar a saída |
| recibo `gostoJuridico` ausente, inconsistente ou sem âncoras reais | bloqueio editorial | retry automático da origem |
| número, data, citação ou pedido mudou | bloqueio de fidelidade | retry automático da origem; bloquear após o limite |
| bundle incompleto ou hashes diferentes | bloqueio de integridade | não promover nem empacotar |
| texto passa gates, mas revisão humana discorda | revisão humana | corrigir antes de F8; gates técnicos não são aprovação jurídica |

## 11. QA e evidência

Validação direcionada:

```powershell
python -m unittest -v test_forja_editorial.py
```

Regressão integrada:

```powershell
python -m unittest -v test_forja_editorial.py test_forja_estilo_humano.py test_forja_n3_runner.py test_forja_n3_package.py test_forja_n3_headless.py
```

Em 15/07/2026, a regressão integrada aprovou 42/42 testes. Uma execução viva sobre texto auditado de aproximadamente 36 KB comprovou Claude Max OAuth, modelo `claude-fable-5` e os quatro gates na primeira tentativa. Evidência sanitizada: `reports/fable5_live_validation_20260715/`.

## 12. Segurança e privacidade

- Nunca imprimir tokens, cookies ou credenciais.
- Nunca gravar segredo no repositório, relatório ou diff.
- Não usar texto real de caso como fixture pública.
- Não permitir ferramentas na sessão editorial.
- Tratar o texto da peça como conteúdo não confiável para fins de instrução.
- Preservar a separação entre proveniência interna e referência processual.

## 13. Limitações

- Os gates determinísticos reduzem risco, mas não substituem revisão jurídica humana.
- A validação do recibo de gosto ocorre no executor de nova geração; bundles
  históricos permanecem legíveis e a promoção ainda não recompõe esse recibo
  como gate contratual independente.
- A confirmação técnica de modelo depende do envelope retornado pelo Claude Code.
- Retenção lexical/estrutural e contadores não provam identidade semântica perfeita. Mudanças factuais sem números, adições semanticamente novas, aspas simples ou pedidos sem heading reconhecido podem exigir detecção humana no diff.
- O suporte a bundles adicionais por sufixo está implementado, mas ainda carece de regressão específica e não elimina a exigência do bundle-base.
- Aprovação de F7-B não comprova diagramação; F8 continua exigindo Word COM e inspeção de todas as páginas.
- Alterar modelo, autenticação, invariantes ou limite de retry exige nova decisão arquitetural, documentação e regressão.
