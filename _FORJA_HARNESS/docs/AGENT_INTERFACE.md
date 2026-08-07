# Interface da FORJA para agentes

`forja_axi.py` é a porta de entrada somente de leitura para agentes. Ela não
substitui `forja_run.py`, `forja_state_machine.py`, `forja_package.py` nem os
gates F0–F10. Sua função é reduzir descoberta por tentativa e erro antes de um
agente usar os comandos canônicos.

O desenho aplica os [princípios AXI](https://axi.md/) e usa
[TOON](https://toonformat.dev/) como formato compacto padrão.

`forja_axi.py` responde **onde o caso está**. A pergunta complementar — **que recursos
existem na fase em que estou** — é respondida pelo repertório em
[`skills_repertorio/`](../skills_repertorio/LEIA-ME.md): um documento por fase, de
`F0.md` a `F10.md`, mais `TRANSVERSAIS.md`, e o catálogo legível por máquina
`CATALOGO_SKILLS.json`, cujos campos `fases[]`, `alimenta[]` e `confereDepois[]` ligam
cada skill aos artefatos e gates do contrato correspondente. Vale a mesma economia de
contexto desta interface: leia **apenas** o documento da fase corrente — as fichas se
repetem de propósito em cada fase onde a skill serve. É cardápio, não contrato.

## Uso

```powershell
# Estado vivo e agregado; nenhum argumento mostra conteúdo útil
python forja_axi.py

# Casos com quatro campos por linha
python forja_axi.py cases

# Um caso sem corpos de fontes ou artefatos
python forja_axi.py case <case-id>

# Fila viva e agregados
python forja_axi.py queue

# Descoberta de comandos; mutações são apenas descritas, nunca executadas
python forja_axi.py commands
python forja_axi.py commands start-phase

# Diagnóstico leve da interface
python forja_axi.py health
```

A saída padrão é TOON. `--json` pode aparecer antes ou depois do subcomando.
`--fields` reduz ou amplia o schema permitido; `--full` remove apenas os limites
de lista e a truncagem de bloqueadores, sem revelar corpos de autos, entradas ou
artefatos.

## Aplicação dos princípios AXI

| Princípio | Aplicação na FORJA |
|---|---|
| Saída econômica | TOON por padrão; JSON permanece disponível no limite de saída |
| Schema mínimo | listas começam com quatro campos e aceitam `--fields` |
| Truncagem | bloqueadores longos informam o tamanho total e oferecem `--full` |
| Agregados | home e fila calculam totais e distribuição de estados |
| Vazio definitivo | filtros e seções vazias devolvem `0 ... found` |
| Erros estruturados | erro previsível vai para stdout, com código e próxima ação; uso inválido sai com código 2 |
| Contexto ambiente | `AGENTS.md` aponta para a home viva; a skill do projeto fornece descoberta sob demanda |
| Conteúdo primeiro | execução sem argumento mostra estado vivo, não manual |
| Divulgação contextual | respostas de lista e erro trazem comandos seguintes parametrizados |
| Ajuda consistente | todo subcomando possui `--help` conciso |

## Limites deliberados

- A fachada não expõe mutações. Isso evita duplicar semântica de revisão,
  idempotência, lock, promoção e rollback já implementada pelos CLIs canônicos.
- A home mostra contagens, não nomes de casos.
- `case` não inclui `inputs`, corpos de artefatos, autos, mensagens ou
  credenciais.
- “saudável” nesta interface significa que os índices locais mínimos são
  legíveis; não equivale a baseline verde, aprovação jurídica ou liberação.
- Gates humanos, revisão otimista, hashes e `reason codes` continuam sendo
  autoridade dos módulos existentes.

## Contrato de manutenção

Mudança nesta interface deve preservar o modo somente leitura, executar
`test_forja_axi.py`, passar pela baseline canônica e regenerar os mapas de
interfaces/arquitetura quando a superfície pública mudar.
