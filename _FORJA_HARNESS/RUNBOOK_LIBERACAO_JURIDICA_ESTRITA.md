# Runbook — liberação jurídica estrita v2

## Pré-condições

1. O texto canônico é `final_markdown`.
2. F7 produz `verified_source_ledger`.
3. Cada autoridade inventariada tem fonte oficial capturada e hash-bound.
4. Cada entrada contém o trecho probatório e a proposição exata do documento.
5. Um revisor humano autorizado assina o recibo Ed25519 v2 após ler fonte e
   proposição.
6. O trust store externo está configurado e seu hash está pinado.

Sem qualquer dessas condições, o resultado correto é bloqueio. Não use
`decision_support` ou `internal_working` para contornar uma peça protocolável.

## Campos vinculados pelo recibo jurídico v2

- `sourceSha256`, `sourceUrl`, `sourceIdentity`;
- `sourceExcerpt` e `sourceExcerptSha256`;
- `documentSha256`;
- `documentProposition` e `documentPropositionSha256`;
- `documentParagraphIndex` e `documentParagraphSha256`;
- `authorityIdentity` e `authorityIdentitySha256`;
- produtor, revisor, chave e data da revisão.

O recibo é assinado fora da FORJA. A FORJA não cria chave privada e não
autoconfigura o trust store.

## Fluxo

1. Execute F5 e elimine todas as pendências.
2. Redija e audite o Markdown.
3. Depois da versão final, monte o ledger v2 com a proposição literal e o índice
   do parágrafo.
   Use `python forja_claim_binding.py final.md ledger_rascunho.json verified_source_ledger.json`;
   o comando recompõe hashes e falha se faltar autoridade, mas não assina.
4. Colha a assinatura humana externa.
5. Promova F7; o runner reabre o Markdown, o ledger, as fontes e os recibos.
6. Execute F8.
7. Gere um pacote novo em F9.
8. Registre draft, entrega e cumprimento somente pelo fechamento canônico.

Alteração de uma palavra na proposição, de um byte na fonte ou de uma regra de
liberação exige nova validação e, quando aplicável, novo recibo.

## Auditoria sem mutação

```powershell
python forja_release_audit.py
python forja_release_audit.py --output reports/ANTI_HALLUCINATION_RELEASE_AUDIT.json
```

Use `--fail-on-blocked` apenas em CI. Um pacote histórico bloqueado continua
legível, mas não pode ser registrado, entregue ou encerrado como atual.

## Recuperação

- Fonte oficial indisponível: mantenha a peça bloqueada; não substitua por URL,
  nome de arquivo ou resumo secundário.
- Trust store ausente: configure-o fora do workspace, faça revisão operacional
  do conteúdo e atualize o pin protegido.
- Pacote stale: retorne a F7, gere ledger/recibos v2, recomponha F8 e gere novo
  pacote. Não edite o manifesto antigo.
- Falso positivo do inventário: registre o caso de regressão antes de alterar o
  padrão; não suprima a autoridade só para liberar a peça.
