# Fechamento da implantação — loop pós-protocolo da FORJA

**Data:** 29/07/2026  
**Estado:** implantado e ativo  
**Escopo:** captura de retorno humano por e-mail, preservação local, prova de
protocolo, comparação com a versão exata entregue, aprendizado prospectivo e
ensaio de melhoria arquitetural.

## Resultado

O ramo pós-protocolo foi incorporado a F10 sem criar F11 e sem reabrir a
entrega já concluída ao escritório. O sistema:

1. consulta o Gmail por tarefa horária;
2. aplica allowlist e correspondência fail-closed;
3. preserva original e cópia canônica em pasta nomeada;
4. distingue `protocol_claimed` de `protocol_verified`;
5. resolve o baseline pelo envio exato e por SHA-256;
6. gera comparação privada, ledger sanitizado e Markdown;
7. preserva retornos sucessivos por `contentKey`;
8. produz candidatos de aprendizado;
9. promove regra somente após decisão, fixture e teste prospectivo;
10. ensaia candidata arquitetural em worktree isolado, com shadow, canário,
    revisão independente e rollback.

## Piloto real

- Caso:
  `case-email-patricia-fabio-memoriais-19f3c68ee6d8fef2`.
- Retorno:
  `b50c7d05a93dd3a327c4c24da5a2da0dfe60371cf6d26b02ff47d2a03d87074b`.
- Estado: `protocol_claimed` / `review_pending`.
- Pasta: `VERSÃO HUMANA FINAL — ...`.
- Motivo: a mensagem declara protocolo, mas não há elo externo bastante para
  `protocol_verified`.
- Comparação: 130 mudanças; 38 materiais; 92 não materiais; 74 com origem
  documental ainda `unknown/incerto`.
- Hash da comparação:
  `6ccf9aa801db7e5d438b2c82f52d3cf1c4b3e3ee84715615dafa1fad7ddaa38c`.

F9 e F10 históricos foram preservados byte a byte. A reconstrução do baseline
foi isolada em `F10_POST_PROTOCOL_BASELINE_BACKFILL.json`, com
`status=pending_review`.

## Aprendizado demonstrado

A candidata `learn-b80a07dd026116a8` foi promovida como
`rule-learn-b80a07dd026116a8`, no escopo `product_type` para
`memoriais de apelação`. A fixture e a suíte prospectiva exigem, antes da
redação, cobertura de todos os capítulos devolvidos e dos pedidos acessórios.

Evidência:

- `learning_registry/ACTIVE_RULES.json`;
- `n4_fixtures/post_protocol/devolved_chapters_memoriais_apelacao.json`;
- `n4_fixtures/post_protocol/prospective_memoriais_apelacao_suite.json`;
- `reports/POST_PROTOCOL_PROSPECTIVE_LEARNING_CANARY_20260729.json`.

## Revisão adversarial

Foram executadas três revisões no Claude Code com `claude-opus-5`:

1. reprovação inicial, com críticos e altos;
2. nova reprovação após os reparos, por perda de decisões em reingestão;
3. aprovação final, sem achados críticos ou altos.

Os três achados não bloqueantes da aprovação final também foram corrigidos:
comparação assimétrica de métricas AR, chave duplicada em ingestão e carryover
de promoção sem revalidar fixture/recibo.

## Verificação executada

- Suíte focal: **116 testes + 12 subtestes**, todos verdes.
- Baseline nominal: **44/44 suítes**, **516 testes pytest + 58 subtestes** e
  **7 regressões em script**, estado `APROVADO`.
- AR arquitetural: baseline isolado 75/0; candidata 110/0; canário 5/0;
  rollback aprovado; zero vazamentos do cofre; maturidade
  `estudo_descritivo`.
- Archify: componentes, fluxo operacional, fluxo de confiança e sequência de
  interfaces em perfil `showcase`, sem erros ou avisos; oito HTMLs passaram em
  `check`.
- Graphify: grafo regenerado, enriquecido por interfaces e consultado com as
  novas relações.
- Git: cofre, relatório de execução e pastas humanas/protocoladas ignorados;
  zero item privado apareceu no status.

O comando bruto `pytest` de toda a raiz continua inadequado porque testes
legados substituem e fecham `sys.stdout` no Python 3.14. O runner canônico
`forja_baseline.py` executa cada suíte isoladamente e comprovou toda a baseline.

## Automação ativa

Tarefa: `FORJA - Loop Pos-Protocolo`.

- Estado após execução: `Ready`.
- Resultado da última execução: `0`.
- Periodicidade: horária.
- Primeira execução ampla validada: 150 mensagens examinadas, 6 retornos
  processados e 139 itens mantidos em quarentena/revisão fail-closed.
- Nenhuma pasta foi nomeada `PEÇA PROTOCOLADA` sem `protocol_verified`.

## Limite deliberado

O loop aprende automaticamente a partir de evidência, mas não se dá autoridade
ilimitada. Regra jurídica ou de produto exige decisão humana e teste
prospectivo. Candidata arquitetural pode ser medida e criticada automaticamente,
mas não se promove nem altera produção sozinha.
