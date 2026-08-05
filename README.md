# FORJA — motor

Esteira de produção de peças jurídicas com fluxo fail-closed F0–F10, contratos de fase,
schemas, gates determinísticos e cadeia de auditoria. Este repositório contém **apenas o
sistema**: código, contratos, schemas, testes, templates e a doutrina de operação.

**Não há dado de cliente aqui.** Nenhum caso, nenhum autos, nenhum número CNJ de processo
real, nenhum artefato de execução. O `.gitignore` barra `_FORJA_HARNESS/state/` na raiz da
regra, e a rotina de sincronização recusa qualquer arquivo acima de 95 MB.

## O par de repositórios

Este sistema só reconstrói inteiro com **dois** repositórios privados:

| | conteúdo | tamanho |
|---|---|---|
| `forja-harness` (este) | motor: código, contratos, schemas, testes, doutrina | ~152 MB |
| `forja-acervo-auditoria` | `state/` (cadeia de auditoria por caso), modelos aprovados, painel de gestão | ~189 MB |

Separados de propósito. O motor evolui e é revisável por qualquer engenheiro; o acervo carrega
nome de cliente e número de processo e tem outro regime de acesso. Quem só precisa entender ou
melhorar o sistema clona apenas este.

O acervo processual em si — autos, laudos, anexos de e-mail — **não vai para nenhum dos dois**.
Ele fica no disco de trabalho, e a origem dele é o e-mail, que é onde os documentos chegaram.

## Como o repositório se posiciona no disco

O motor espera ser executado dentro da pasta de trabalho onde o acervo também existe. A
correspondência é por caminho: `_FORJA_HARNESS/` deste repositório sobre `_FORJA_HARNESS/` da
pasta de trabalho, e o mesmo para `_FERRAMENTAS/`, `git-tools/` e a doutrina da raiz.

## Por onde começar

- `_FORJA_HARNESS/INDICE_FORJA.md` — mapa dos recursos e do estado real de cada um
- `_FORJA_HARNESS/RETROSPECTIVAS.md` — as lições, cada uma ancorada numa falha medida
- `CLAUDE.md` e `AGENTS.md` — o protocolo obrigatório de operação
- `_FORJA_HARNESS/forja_baseline.py` — o runner autoritativo das suítes (não use `pytest` direto)
- `_FORJA_HARNESS/forja_regua.py` — integridade dos arquivos protegidos, hash-bound

## Verificação

```
python -X utf8 forja_baseline.py    # 90/90 suítes
python -X utf8 forja_regua.py       # integridade + bateria real com telemetria
```
