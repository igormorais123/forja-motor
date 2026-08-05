# W2B — mapa do destinatário e TeiaJus em sombra

**Data:** 25/07/2026
**Ordem:** 1B antes de 1A, conforme a emenda E15
**Princípio que organiza a onda:** descoberta não é prova. O que orienta a busca não decide a distribuição.

---

## 1. Contrato do TeiaJus confirmado por `capabilities`, não por semelhança de nome

O roadmap condicionava a integração a uma verificação, e ela foi feita antes de qualquer código. As trinta ações do TeiaJus foram lidas do próprio serviço:

| Ação | Modo | Decisão |
|---|---|---|
| `research_sources` | `read`, sem rede | **admitida** |
| `research_plan` | `read`, sem rede | **admitida** |
| `research_search` | `read`, com rede | **admitida** |
| `research_mission_get` | `read`, sem rede | **admitida** |
| `research_mission` | **`read_paid`** | **negada** |
| `captcha_solve` | **`read_paid`** | **negada** |
| `apify_contact_enrich` | **`read_paid`** | **negada** |

**A negação passou a ser explícita.** A allowlist já recusaria as pagas por omissão, mas omissão é defesa frágil: bastaria alguém acrescentar `research_mission` a `readActions` por distração para autorizar gasto sem que ninguém tivesse decidido isso. Agora há `deniedActions` conferida **antes** da allowlist, com teste que simula exatamente essa inclusão distraída e verifica que a negação prevalece.

**Verificação ao vivo:** `research_sources` devolveu o catálogo de fontes com `paid` e `access_mode` por fonte; `research_plan` planejou uma missão com `max_cost_usd: 0.0` nos passos gratuitos; `research_mission` foi recusada com a mensagem certa. Nenhuma ação de escrita entrou na ampliação, e `cgu_update` — que existe no TeiaJus e nunca foi listada — continua recusada pela allowlist, com teste próprio.

## 2. Nível probatório: o que a fonte é decide o que o mapa pode afirmar

Três níveis, e a distinção não é acadêmica:

| Nível | Fontes | O que sustenta |
|---|---|---|
| **decide** | `decisao_integra`, `acordao_integra`, `ato_oficial_tribunal` | o próprio ato, lido na íntegra |
| **corrobora** | `ementa`, `espelho_oficial`, `diario_eletronico` | publicação oficial que noticia o ato sem substituí-lo |
| **orienta** | `metadado_datajud`, `dado_administrativo`, `resultado_busca` | dizem onde procurar |

**Tipo desconhecido nunca é promovido a prova** — cai em `orienta`. É a única direção segura para o default.

Cada fonte se declara no bloco `sourceCatalog`, e o validador recusa afirmação sustentada apenas por fonte que orienta: prevenção `confirmed` só com metadado, composição `confirmed` só com metadado.

## 3. Freshness: o relógio decide, não o campo

`status=confirmed` autodeclarado não sobrevive ao tempo. O validador calcula a idade de `checkedAt` contra `recipientMapFreshnessHours` (24h na config) e marca `FAL-F3-COMPOSITION-STALE` quando vencida. Sem limite configurado, não inventa prazo — há teste para isso também.

## 4. O teste real: um mapa do caso Cafelana, com o STJ fora do ar

Construí o mapa do `AREsp 2.698.443` (STJ, Primeira Turma) e a circunstância foi melhor do que qualquer fixture: **as fontes oficiais do STJ estavam indisponíveis no momento da consulta** — `stj_search` devolveu HTTP 520 e o DataJud falhou após retentativas.

O que o mapa registrou:

- **relator e competência `confirmed`**, lastreados no acórdão dos autos (`decisao_integra`);
- **composição `unknown`** — a fonte oficial não respondeu;
- **prevenção `unknown`** — nenhuma fonte adequada, e metadado não decide distribuição;
- **duas `searchRuns` com `negativeResult: true`**, cada uma apontando o arquivo de telemetria para replay e declarando a limitação real: *"fonte oficial do STJ retornou HTTP 520 no momento da consulta"*.

**O validador aprovou esse mapa.** Não saber, declarado com a tentativa registrada, é estado legítimo.

E a contraprova, no mesmo mapa: bastou trocar a composição para `confirmed` com metadado do DataJud e sem data para o validador acusar as duas coisas — falta de fonte oficial e falta de data de conferência.

Exemplo preservado em `reports/EXEMPLO_F3_MAPA_DESTINATARIO_ARESP_2698443.json`.

## 5. Verificação

```
capabilities do TeiaJus       → 30 ações inventariadas, 3 pagas identificadas
research_sources / _plan      → executadas ao vivo, custo zero
research_mission              → negada, mensagem correta
python forja_baseline.py      → 37/37 suítes · 361 testes · APROVADO
```

Baseline: 345 → 361 testes, os 16 novos da onda. Zero regressão. **Nenhuma mutação no TeiaJus, nenhuma ação paga, nenhum caso alterado.**

## 6. O que fica

Os itens da W2B que dependiam de rede — composição verificada em fonte oficial atual e mapas históricos para outros casos do STJ — ficam pendentes da disponibilidade das fontes. Não é bloqueio de desenho: é o desenho funcionando, porque a indisponibilidade produziu `unknown` em vez de invenção.

Próxima onda: **W2A — cocrição F2-B em sombra**, condicionada ao resultado da consulta da Onda −1, conforme H5 e o cenário pessimista de Helena.
