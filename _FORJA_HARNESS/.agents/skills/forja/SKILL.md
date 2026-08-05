---
name: forja
description: Use para orientar-se, inspecionar estado e descobrir comandos da FORJA sem contornar gates jurídicos ou humanos.
---

# FORJA

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
