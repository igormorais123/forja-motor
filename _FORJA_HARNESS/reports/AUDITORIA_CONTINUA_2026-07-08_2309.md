# FORJA N2 — Auditoria contínua

**Data:** 2026-07-08 23:09 BRT  
**Revisão:** 2026-07-08, após limpeza da camada de rótulos genéricos que não ajudava a execução.  
**Escopo:** auditoria dos artefatos FORJA gerados após a correção dos planejamentos N2.  
**Modo:** leitura + correções objetivas em scripts/estado, sem alterar painel `gestao_escritorio`.

---

## 1. Veredito

O trabalho avançou além da documentação: há scripts, estados, relatórios e pacote piloto. A direção geral está aderente ao N2, mas a auditoria encontrou falhas de integridade que poderiam gerar falsa segurança em execução futura. As falhas objetivas foram corrigidas.

Também foi removida uma camada de classificação genérica que não trazia ganho operacional. FORJA agora bloqueia por lacuna verificável: falta de pasta, comando, anexo, tribunal, regimento, fonte, QA ou evidência de entrega.

---

## 2. Achados corrigidos

### A1 — Ledger de citações duplicava IDs e mantinha versões antigas

**Problema:** Cafelana AgInt tinha entradas duplicadas no `sourceLedger`; algumas citações apareciam primeiro como `NAO_VERIFICADO` e depois como `FONTE_OFICIAL`.  
**Risco:** executor futuro poderia ler a versão antiga e bloquear ou liberar errado.  
**Correção:** `forja_citations.py` agora mescla por `id` e substitui versões antigas; estado Cafelana foi deduplicado.

### A2 — `currentPhase` não refletia fechamento F10

**Problema:** Cafelana AgInt estava `fulfilled`, mas `currentPhase` permanecia em `F3_FONTES_REGIMENTO_LEIS`.  
**Risco:** status contraditório na próxima execução.  
**Correção:** `forja_delivery.py` agora grava `currentPhase = F10_ENTREGA_EVIDENCIA_APRENDIZADO`; estado Cafelana corrigido.

### A3 — Gate de entrega aceitava texto como prova arquivada

**Problema:** `forja_delivery.py` considerava string simples, como assunto de e-mail, suficiente para o elo "Entrega arquivada".  
**Risco:** falso cumprimento.  
**Correção:** o elo de entrega agora exige pasta/arquivo salvo; texto simples só é aceito no campo separado de `evidenciaResposta`. A trilha Cafelana foi regenerada e continua aprovada com arquivos salvos.

### A4 — Relatório F10 cortava caminhos

**Problema:** `F10_TRILHA_EVIDENCIA.md` truncava referências longas.  
**Risco:** auditoria sem caminho verificável.  
**Correção:** `forja_delivery.py` agora escreve referências completas.

### A5 — `forja_headless.py` usava `shell=True`

**Problema:** chamada do Claude headless usava `shell=True` sem necessidade.  
**Risco:** superfície desnecessária para erro/injeção de comando.  
**Correção:** alterado para `shell=False`.

### A6 — Escrita repetida de gates, ledger e artefatos

**Problema:** novas rodadas de `forja_sources.py`, `forja_citations.py`, `forja_pilot_m4.py` e `forja_delivery.py` podiam acrescentar itens já existentes.  
**Risco:** estado inflado, leitura ambígua e auditoria futura mais fraca.  
**Correção:** scripts agora mesclam por chave estável e mantêm artefatos únicos.

### A7 — M4 não gravava fase real do piloto

**Problema:** `forja_pilot_m4.py` gerava DOCX/PDF/QA, mas não deixava `currentPhase` coerente com a execução.  
**Risco:** mapa de progresso errado.  
**Correção:** piloto M4 agora grava `currentPhase = F6_F8_PILOTO_M4` e artefatos únicos.

### A8 — Arquivos temporários Natura soltos no topo do harness

**Problema:** `tmp_drive_natura.js` e `tmp_drive_natura.png` estavam no topo de `_FORJA_HARNESS`.  
**Risco:** confusão entre temporário e artefato canônico.  
**Correção:** movidos para `state/case-email-natura-cabreuva-19f3991ebc75fe03/drive_access_probe/` e registrados como artefatos do estado Natura.

### A9 — Campo sem utilidade operacional no estado

**Problema:** estados e reconciliador carregavam um campo de classificação que não melhorava a execução e podia virar distração.  
**Risco:** novos agentes tratariam rótulo genérico como gate real.  
**Correção:** campo removido dos estados, do reconciliador, do manifesto e dos planejamentos.

---

## 3. Scripts alterados

- `forja_reconcile.py`: removeu campo sem utilidade operacional; continua reconciliando origem, pasta, comando, anexos, status, evidência e integrações.
- `forja_citations.py`: merge de `sourceLedger` por `id` e artefatos únicos.
- `forja_sources.py`: merge de gates, ledger e artefatos sem duplicação.
- `forja_pilot_m4.py`: `currentPhase` e artefatos únicos.
- `forja_delivery.py`: gate de evidência endurecido, `currentPhase` F10 e caminhos completos.
- `forja_headless.py`: chamada sem `shell=True` e artefatos únicos.

---

## 4. Validações realizadas

- `FORJA_SPEC_MANIFEST.json` continua JSON válido.
- Scripts Python alterados compilaram com `python -m py_compile`.
- Cafelana AgInt agora está:
  - `status: fulfilled`;
  - `currentPhase: F10_ENTREGA_EVIDENCIA_APRENDIZADO`;
  - `duplicateSourceIds: 0`;
  - `naoVerificadoFinalUse: 0`;
  - `duplicateArtifacts: 0`.
- Trilha F10 Cafelana foi regenerada e segue aprovada com arquivos de entrega arquivados.
- Topo de `_FORJA_HARNESS` não mantém `tmp_*` solto após a movimentação.

---

## 5. Pendências abertas

### P0 ativos

- `case-email-natura-cabreuva-19f3991ebc75fe03`: `TRIBUNAL_NAO_IDENTIFICADO`.
- `case-email-patricia-fabio-memoriais-19f3c68ee6d8fef2`: `REGIMENTO_AUSENTE`.

Esses bloqueios são corretos pelo N2: não devem ser resolvidos por suposição.

### Riscos P1/P2 relevantes

- Algumas demandas abertas seguem sem prazo estruturado.
- Algumas demandas têm anexos externos pendentes.
- O manifest declara M0-M5 concluídos em modo sombra; isso deve ser lido como validação de piloto/esteira, não autorização para produção automática plena.
- `forja_render_docx.py` ainda permite marcadores `[VERIFICAR...]` como deliberados no resumo; isso é aceitável para artefato consultivo/intermediário, mas continua bloqueando peça final pelo PRD/TDD.

---

## 6. Próxima auditoria recomendada

1. Validar `forja_render_docx.py` em um caso real com tabela e assinatura, conferindo se o achado M4 foi realmente resolvido.
2. Abrir os dois P0 ativos e confirmar se o bloqueio é factual: regimento TJRJ para Patrícia/Fábio e classificação Natura.
3. Auditar `gestao_escritorio/data/demandas.json` contra os estados N2 para garantir que o painel não mostre cumprimento maior que a evidência.
4. Rodar uma checagem de metadados DOCX/PDF nos pacotes piloto e entregas arquivadas.
