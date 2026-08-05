# Evidência de validação ao vivo — Claude Fable 5

Data da execução: 15/07/2026, 20:40:56 (UTC-03:00), conforme os JSONs desta pasta.

## Escopo

Este diretório preserva a evidência de uma execução real da subfase
`F7-B_REVISAO_EDITORIAL_ESCRITA_FINAL` sobre o caso de validação
`case-email-auto-19f3f25cb64df962-live-validation`. A evidência demonstra que o executor recebeu
uma resposta do modelo `claude-fable-5`, registrou o uso da assinatura OAuth Claude Max sem API key,
produziu o bundle editorial e obteve aprovação dos gates determinísticos naquele resultado.

Ela não demonstra, por si só, a validade jurídica do texto, equivalência semântica integral, aprovação
humana, promoção da fase F7 nem conclusão de F8. O texto jurídico foi processado remotamente pelo
Claude Code; nenhum token ou credencial de autenticação é reproduzido neste README.

## Resultado registrado

| Campo | Valor derivado dos artefatos locais |
|---|---|
| Protocolo | `FORJA-FABLE5-FINAL-v1` |
| Status do fragmento | `pass` |
| Modelo | `claude-fable-5` |
| Autenticação | `claude.ai` / assinatura `max` / provedor `firstParty` |
| Cobrança declarada | assinatura OAuth Claude Max, sem API key |
| Tentativa aprovada | 1 |
| Tentativas rejeitadas anteriores | 0 |
| Tokens de entrada registrados | 4.568 |
| Tokens de saída registrados | 16.000 |
| Mudanças editoriais declaradas | 4 |
| Dúvidas editoriais registradas | 3 |
| SHA-256 de origem | `dffed4d7eff75bdb1aaac6bf0e3be21d776511668527b98d42257868df44a586` |
| SHA-256 final | `c67694761758985254116be73a1ef17dfcd746746e9d1e718a0ed9ea7baa1fb2` |
| Tamanho de `final_markdown.md` | 36.049 bytes |

Os quatro gates publicados em `editorial_fidelity.json` e `FABLE5_RESULT.json` estão em `pass`:

- `editorial_source_hash_match`;
- `editorial_fidelity_pass`;
- `human_style_final_pass`;
- `fable5_oauth_confirmed`.

`editorial_fidelity.json` registra `approved: true`, sem achados. O SHA-256 calculado do arquivo
`final_markdown.md` coincide com o hash final registrado no relatório e na evidência de uso.

## Inventário

| Arquivo | Papel | Tamanho |
|---|---|---:|
| `final_markdown.md` | texto final produzido | 36.049 bytes |
| `editorial_report.json` | relatório do modelo e hashes persistidos pelo executor | 2.443 bytes |
| `editorial_diff.patch` | diff unificado entre origem auditada e resultado | 4.958 bytes |
| `fable5_usage.json` | modelo, tipo de autenticação, sessão, hashes e uso | 723 bytes |
| `editorial_fidelity.json` | gates recompostos pelo orquestrador | 533 bytes |
| `FABLE5_RESULT.json` | fragmento para incorporação ao resultado F7 | 914 bytes |

## Como interpretar o fragmento

`FABLE5_RESULT.json` não é um `PHASE_RESULT.json` completo. Ele contém somente os gates e os cinco
artefatos produzidos por F7-B e deve ser incorporado ao `PHASE_RESULT.json` da tentativa F7 antes da
promoção. O runner `forja_run.py` não chama o Fable automaticamente; ele recompõe e valida o bundle
quando a fase é promovida. Em F8 e em pacotes novos, o cânone textual é `final_markdown`; o
`audited_markdown` continua como trilha interna.

## Limitações desta cópia de evidência

O `audited_markdown` de origem não foi copiado para este diretório. O hash de origem está preservado
nos três JSONs correspondentes, mas uma revalidação independente completa requer o arquivo original
da tentativa F7. Além disso, os gates automáticos verificam hashes, números, autoridades, marcadores,
aspas, títulos, retenção mínima, pedidos/fecho, origem operacional e padrões de estilo. Esses controles
detectam regressões importantes, mas não provam equivalência semântica completa; a auditoria F7 e a
leitura humana final permanecem obrigatórias.
