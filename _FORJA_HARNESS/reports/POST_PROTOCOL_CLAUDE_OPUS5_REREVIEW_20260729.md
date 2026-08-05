# Segunda revisão adversarial — Claude Code Opus 5

- Modelo: `claude-opus-5`
- Veredito: `REJECT`
- Estado dos sete bloqueios críticos iniciais: resolvidos

## Único achado alto

`PP-LEARN-DECISION-RESET-ON-SECOND-INGEST`: uma segunda peça humana no mesmo caso recriava candidatos e decisões como `observed/pending`, podendo apagar rejeição, origem e revisão humana anteriores.

Correção aplicada:

- o segundo `ingest` reaproveita candidatos pelo `changeFingerprint`;
- `reviewDecision`, `origin`, `decision`, aprovações e estágios são preservados;
- artefatos da rodada anterior são arquivados por `contentKey`;
- promoção e resolução de origem agora exigem o `contentKey`;
- teste de regressão usa dois retornos com hashes diferentes e a mesma alteração semântica.

## Achados médios também corrigidos

- Métrica AR agora combina arquivos rastreados com probes reais de `git check-ignore` sobre o overlay candidato.
- Artefatos de cada retorno são arquivados em `post_protocol_history/<contentKey>`.
- Backfill inicializa o caso antes de registrar evento.
- O avaliador AR passou a usar `sys.executable`.
