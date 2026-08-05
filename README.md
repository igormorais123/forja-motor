# FORJA — motor

Esteira de produção de peças jurídicas com fluxo fail-closed F0–F10, contratos de fase,
schemas, gates determinísticos e cadeia de auditoria. Este repositório contém **apenas o
sistema**: código, contratos, schemas, testes, templates e a doutrina de operação.

## Não há dado de cliente aqui, e isso é verificável

Não é promessa: é gate. `_FORJA_HARNESS/forja_fronteira.py` varre a árvore e reprova
nome de cliente, número CNJ, CPF, CNPJ e inscrição na OAB dentro de qualquer arquivo
destinado ao motor. Ele roda no baseline (`test_forja_fronteira.py`) e antes de cada
publicação.

```
python -X utf8 _FORJA_HARNESS/forja_fronteira.py
```

Fora da máquina onde o acervo está montado, o gate roda em modo `estrutural` — encontra
CNJ, CPF, CNPJ e OAB, mas não a lista de nomes, que é dado de cliente e vive no outro
repositório. Ele **diz em que modo rodou**; "aprovado" nunca significa duas coisas
diferentes sem avisar.

A doutrina cita casos reais como âncora de cada lição, porque regra sem âncora não se
confere. Eles aparecem como `CASO-04`, `CASO-19`: a tradução para o nome verdadeiro vive
no acervo, e quem tem os dois lê a lição com o caso na cabeça.

## O par de repositórios

Este sistema só reconstrói inteiro com **dois** repositórios privados:

| | conteúdo |
|---|---|
| `forja-motor` (este) | código, contratos, schemas, testes, doutrina |
| `forja-auditoria` | `_FORJA_HARNESS/state/` (cadeia de auditoria por caso), modelos aprovados, relatórios de execução, painel de gestão |

Os dois usam a **mesma estrutura de caminhos**. Reconstituir a árvore de trabalho é
copiar um sobre o outro, sem tradução:

```
git clone https://github.com/igormorais123/forja-motor.git trabalho
git clone https://github.com/igormorais123/forja-auditoria.git /tmp/acervo
cp -r /tmp/acervo/. trabalho/          # sem o .git
cd trabalho && python -X utf8 _FORJA_HARNESS/forja_baseline.py
```

O acervo processual em si — autos, laudos, anexos de e-mail — **não vai para nenhum dos
dois**. Fica no disco de trabalho, e a origem dele é o e-mail.

## Como o motor alcança o acervo

Por uma porta só: `_FORJA_HARNESS/forja_acervo.py`. O motor pede por chave
(`forja_acervo.caminho("peca-ancora-longa")`, `forja_acervo.caso("CASO-04")`) e o acervo
responde com o caminho ou o identificador verdadeiro. Nenhum módulo do motor escreve
caminho de pasta de cliente.

Sem o acervo montado, `forja_acervo.disponivel()` é falso e quem depende dele precisa
dizer que **não pôde verificar** — nunca tratar ausência como aprovação.

## Levar o motor para outro escritório

A identidade visual da casa está isolada em `_FERRAMENTAS/assets/` (logo, marca, rodapé)
e no bloco de tokens de `_FERRAMENTAS/estilo_medina.py`. Trocar esses dois pontos troca a
identidade. A marca é do escritório; o sistema, não.

## Por onde começar

- `_FORJA_HARNESS/INDICE_FORJA.md` — mapa dos recursos e do estado real de cada um
- `_FORJA_HARNESS/RETROSPECTIVAS.md` — as lições, cada uma ancorada numa falha medida
- `CLAUDE.md` e `AGENTS.md` — o protocolo obrigatório de operação
- `_FORJA_HARNESS/forja_baseline.py` — o runner autoritativo das suítes (não use `pytest` direto)
- `_FORJA_HARNESS/forja_regua.py` — integridade dos arquivos protegidos, hash-bound

## Verificação

```
python -X utf8 _FORJA_HARNESS/forja_baseline.py    # suítes declaradas
python -X utf8 _FORJA_HARNESS/forja_regua.py       # integridade + bateria com telemetria
python -X utf8 _FORJA_HARNESS/forja_fronteira.py   # nenhum dado de cliente no motor
```

Algumas suítes precisam do acervo montado para conferir contra peça real; sem ele elas
dizem que não verificaram, em vez de passar caladas.
