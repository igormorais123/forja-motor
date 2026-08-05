# W1 — linguagem do sistema, schemas e modo `off`

**Data:** 25/07/2026
**Emendas incorporadas:** E5 (cobertura de famílias), E7 e E8 (ficha de âncora — parcial), E13 (regime como convenção interna)
**Decisões arquiteturais respeitadas:** DA-01 (sem fase nova), DA-02 (namespace próprio), DA-04 (schemas gerados), DA-05 (um draft)

---

## O que esta onda entrega — e o que ela deliberadamente não faz

Contratos e vocabulário entram; comportamento não. A prova central da onda é negativa: **com `mode=off`, nada muda**. Contrato novo que altera comportamento antes de ser ligado não é contrato — é mudança disfarçada de contrato.

## 1. Namespace próprio (DA-02)

Em `FORJA_N3_CONFIG.json`, ao lado de `n4`:

```json
"forjaAssinaturaLite": {
  "schemaVersion": 1,
  "mode": "off",
  "pilotCases": [],
  "consultationOutboundPolicy": "manual_review_only",
  "recipientMapFreshnessHours": 24,
  "allowPaidResearch": false
}
```

`n4.mode` **não foi reutilizado** — ele tem quatro pilotos vivos e emprestá-lo misturaria populações. Há teste que verifica que `n4` continua em `pilot_blocking` com os mesmos quatro casos.

`_effective_named_mode()` generaliza a resolução preservando a fachada: `_effective_mode()` continua existindo com a assinatura de sempre, agora delegando. Modo desconhecido levanta erro; namespace ausente equivale a `off`; em `pilot_blocking`, só bloqueia caso nomeado, e os demais ficam em `shadow`.

## 2. Dois tipos novos, não duas conchas ocupadas

`F3_MAPA_DESTINATARIO.json` (`recipient_map`) e `F4_SIGNATURE_BRIEF.json` (`signature_brief`) entraram como tipos próprios em `ARTIFACT_SPECS`.

Registro por que não reaproveitei as conchas vazias do catálogo, já que a ideia era minha e foi descartada: "decision factor map" e "signature brief" não são o mesmo objeto, e um nome que guarda outra coisa é um nome que mente. Como DA-04 gera os schemas a partir da tabela, acrescentar uma entrada custa o mesmo que preencher uma concha — a economia que eu supunha não existia. As 24 conchas seguem como dívida de catálogo própria (E1).

O catálogo passou de 24 para 26 artefatos. O gerador foi executado duas vezes e os 43 arquivos gerados mantiveram hash idêntico: **idempotente**.

## 3. O que os validadores recusam

Escritos em `forja_reasoning.py`, ao lado dos irmãos, e registrados em `forja_reasoning.VALIDATORS` e `forja_n4_validate.VALIDATORS`.

**Mapa do destinatário** — a regra que organiza tudo: *o que orienta a busca não prova a distribuição*.

| Recusa | Razão |
|---|---|
| identidade `confirmed` sem fonte | declaração não é lastro |
| prevenção `confirmed` só por DataJud | `orgaoJulgador` é metadado de processo: diz onde procurar, não decide distribuição |
| composição `confirmed` sem data de conferência | composição de órgão muda; lastro sem data não sustenta |
| posição sem `decisionIds` | posição sem decisão identificada é impressão |
| topologia além do órgão sem justificativa | escopo amplo tem de ser escolhido, não herdado |

`unknown` é estado legítimo e passa. Não saber é resposta aceitável; fingir que sabe não é.

**Signature brief:**

| Recusa | Razão |
|---|---|
| sem pergunta jurisdicional | o brief existe para responder uma |
| rotas com mesmas teses, âncoras e objeção | rotas que só diferem no texto simulam deliberação |
| rota única sem motivo; mais de quatro sem justificativa | ambos são sinais de rota artificial |
| `selectedRouteId` divergente da rota marcada | inconsistência interna |
| rota selecionada sem `humanDecisionId` | a escolha material é do advogado |
| pendência bloqueante com rota selecionada | bloqueio não convive com seleção |
| família de tese ausente ou descartada sem motivo | E5 |

**E5 na prática:** nove famílias — competência, admissibilidade, prejudiciais, prescrição/decadência, nulidades, mérito principal, mérito subsidiário, constitucional/prequestionamento, consequência institucional. Cada uma `examinada_proposta`, `examinada_descartada` com motivo, ou `nao_aplicavel` com motivo. **Não há mínimo numérico de teses**, e há teste que verifica a ausência desse campo no schema gerado: o dever é examinar cada frente, não produzir quantidade.

## 4. Verificação

```
python generate_n4_contracts.py (2×)  → 43 arquivos, hash estável
python forja_phase_contracts.py       → 11 fases, ordem preservada
python -m pytest test_forja_assinatura_lite.py → 29 passed
python forja_baseline.py              → 37/37 suítes · 345 testes · APROVADO
forja_n4_validate sobre 3 casos reais → exit 0, sem alteração
```

Baseline: 316 → 345 testes, os 29 da suíte nova. Zero regressão.

## 5. O que fica para as ondas seguintes

E7 (`vigencia` com quatro estados) e E8 (`precedenteContrarioConhecido[]`) pertencem à **ficha de âncora**, que vive no `verified_source_ledger` e é entregue na W3. E13 (regime como convenção interna, nunca afirmado pelo rótulo) idem. O que a W1 fez foi preparar o terreno sem antecipar contrato de artefato que ainda não existe.

Próxima onda pela ordem da emenda E15: **W2B — mapa do destinatário e TeiaJus em sombra**, antes de W2A.
