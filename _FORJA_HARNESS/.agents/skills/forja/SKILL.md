---
name: forja
description: Ficha portátil da esteira FORJA - orientar-se, inspecionar o estado de um caso e descobrir o comando canônico sem contornar gate jurídico ou humano. Use ao trabalhar qualquer caso da fábrica de petições ou ao mexer no harness, e abra a skill completa `forja` para as onze fases, os gates e as ordens invioláveis.
---

# FORJA

> **Esta é a ficha portátil, e ela cobre só a navegação de estado.** A skill completa da
> esteira — as onze fases, os artefatos, os gates, as ordens invioláveis e a esteira
> visual — vive em `.claude/skills/forja/`, na raiz da fábrica, e é espalhada para os
> carregadores globais por `python _FORJA_HARNESS/forja_skill_deploy.py`. Neste PC o Codex
> a encontra em `~/.agents/skills/forja/`. Comece por lá; esta ficha existe para o agente
> que só enxerga a pasta do harness.

Comece pela home viva e econômica:

```powershell
python forja_axi.py
```

Comandos de leitura:

```powershell
python forja_axi.py cases
python forja_axi.py case <case-id>
python forja_axi.py queue
python forja_axi.py health
python forja_axi.py commands
```

Regras:

- A saída padrão é TOON; use `--json` somente quando um consumidor exigir JSON.
- Use `--fields` para pedir apenas os campos necessários e `--full` somente
  quando a truncagem indicada impedir a decisão.
- Antes de qualquer mutação, consulte
  `python forja_axi.py commands <name>` e confirme revisão e gates no estado
  canônico.
- Nunca trate `PASS` técnico, pacote existente, fila verde ou painel como
  aprovação jurídica, protocolo ou autorização de envio.
- Nunca use esta interface para inferir fatos, citações, anexos ou conteúdo
  privado que ela deliberadamente não mostra.
- Mutações permanecem nos CLIs canônicos; esta skill não cria atalhos de
  promoção, entrega ou liberação.

## O resto da esteira

Três comandos movem um caso, e nenhum deles passa por aqui:

```powershell
python forja_run.py <caso> start <FASE> --expected-revision <N>
python forja_run.py <caso> promote <attempt-dir> --expected-revision <N>
python forja_run.py <caso> block <FASE> --expected-revision <N> --reason "..."
```

O que cada fase exige, o que reprova e o que é inviolável está na skill completa. Não
tente reconstruir isso de memória: o runner **recomputa** os gates e não aceita
declaração.
