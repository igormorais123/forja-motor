# AUDITORIA ANTIFRAUDE DA FORJA N4

**Data:** 11/07/2026  
**Escopo:** implementação N4, três canários M6, Cafelana, métricas, proveniência, QA, gestão e telemetria real.  
**Veredito:** arquitetura piloto endurecida e baselines retrospectivas mecanicamente reproduzidas; conselho e promoção prospectiva ainda pendentes.

> Atualização: a auditoria do Conselho substituiu o avaliador v1 pelo v2 e a bateria E2E v3. A síntese normativa está em `CONSELHO_SINTESE_IMPLEMENTACAO_FORJA_N4_2026-07-11.md`.

## 1. Falhas encontradas na auditoria do próprio fechamento

| Severidade | Falha | Consequência | Correção |
|---|---|---|---|
| Crítica | Testes criados depois dos textos foram marcados como `draftedBeforeFinalText=true` | Transformava baseline retrospectiva em falso ciclo prospectivo | `executionMode=retrospective_baseline`, declaração temporal honesta e `promotionEligible=false` |
| Alta | C1–C4 estavam preenchidas com `pass` sem medição própria | A consistência global podia ser aprovada por escrita manual | `N4-MEASURED-v1` exige checks, evidência e data em cada camada |
| Alta | Registro científico antigo aceitava hash sem caminho | Um hash inventado poderia aparentar proveniência | Pilotos rejeitam fonte opaca; ciência migrada para caminho + SHA-256 recalculável |
| Alta | Cinco testes escolhidos após o texto discriminavam pouco | Cobertura 5/5 podia ser inflada por critérios fáceis | 10 testes por caso e mutation testing obrigatório com piso de 80% |
| Média | Gestão podia ler `N4_VALIDATION.json` anterior à mudança de configuração | O painel mostrou sombra quando o caso já era piloto | `management_summary` revalida o estado atual sem confiar no snapshot antigo |
| Média | `issues` servia ao envelope e ao mapa intertemporal | Colisão semântica e possibilidade de ocultar ocorrências | Conteúdo funcional renomeado para `temporalIssues` |
| Média | Telemetria dizia apenas “APROVADO” com P1 existentes | Aprovação da ferramenta parecia liberação do documento | Resultado separa `pipelineAprovado`, total P0/P1 e artefatos com ressalvas |
| Média | Saúde usava como origem um DOCX volátil produzido pela própria telemetria | Cada novo render alterava bytes e invalidava o baseline sem mudança jurídica | Fonte primária passou a ser o Markdown estável; DOCX/PDF são derivados conferidos por fidelidade |

## 2. Testes antifraude

O avaliador `N4-ANTI-FRAUD-v2` usa cinco dimensões mecânicas. Ele não avalia mérito jurídico, aprovação do conselho ou prontidão para protocolo:

| Dimensão | Peso | Conta medida |
|---|---:|---|
| Integridade física do registro de fontes | 30% | proporção de fontes ativas com caminho existente e SHA-256 atual |
| Honestidade temporal | 20% | modo retrospectivo declarado ou ordem `frozenAt < finalProducedAt` |
| Cobertura de mutação literal | 25% | mutation score literal dos testes bloqueantes |
| Consistência medida | 15% | C1–C5 com checks, evidência e data |
| Verdade na gestão | 10% | igualdade entre validação e sidecar para aprovação e promoção |

Corpus: quatro casos reais e cinco adversariais. As fraudes simuladas foram: hash opaco, mentira temporal, ausência de mutation testing, passes globais sem evidência e sidecar obsoleto.

Resultados mecânicos:

- três baselines reais: nota 100 e zero P1 no avaliador;
- Cafelana: nota 10 e bloqueada;
- cinco fraudes: todas bloqueadas, inclusive as que mantiveram nota bruta alta;
- dispersão entre os cenários escolhidos: 33,33 a 41,57; isso não é variância operacional;
- peso em dimensões discriminantes: 100%;
- matriz observada: 3 válidos aceitos, 6 inválidos bloqueados, zero falsa aprovação e zero falso bloqueio nesse corpus pequeno;
- bateria E2E v3: 10/10, incluindo controle benigno de reformatação.

Evidência: `telemetria/N4_ANTI_FRAUD_AUDIT_2026-07-11.json`.

## 3. Três baselines reais

| Caso | Artefatos | Testes | Mutações | C1–C5 | QA visual | Promoção |
|---|---:|---:|---:|---:|---:|---|
| Patrícia/Fábio | 24/24 | 10/10 | 10/10 literais | reproduzidas | 6/6 automática | não elegível: retrospectivo + conselho pendente |
| Libra Sul | 24/24 | 10/10 | 10/10 literais | reproduzidas | 7/7 automática | não elegível: retrospectivo + conselho pendente |
| Saúde | 24/24 | 10/10 | 10/10 literais | reproduzidas | 12/12 automática | não elegível: retrospectivo + conselho pendente |

`approved=true` nesses casos significa aprovação estrutural da baseline. Não significa protocolo liberado nem promoção da N4. As três teses ainda possuem ressalvas materiais de Helena/Cícero e a gestão registra `human_review_required`.

## 4. Regressão e dados reais

- 130 testes automatizados aprovados; 2 testes de ambiente ficam omitidos na descoberta principal;
- corpus imutável N4: 11/11;
- regressão de citações: 6 erros detectados e 6 não-travas preservadas;
- render real Word COM: 60 páginas em três produtos;
- 15 DOCX de produção varridos, zero asterisco de marcação;
- telemetria agora informa separadamente os 21 P1 dos renders testados;
- novo render completo foi executado depois da mudança de origem; Saúde permaneceu `approved=true`, demonstrando estabilidade sem relaxar hashes;
- 16 diagramas Mermaid dos planejamentos renderizados sem erro.

## 5. Estado final honesto

1. A N4 está implementada e pode operar em `pilot_blocking`.
2. Patrícia/Fábio, Libra Sul e Saúde são baselines retrospectivas úteis para regressão mecânica, com dois P1 de conselho cada.
3. Cafelana continua bloqueada até a obtenção do AgInt primário de 24/06/2026.
4. `default_on` não está autorizado.
5. M6.4 exige ciclos realmente novos: suíte congelada antes da produção final, mutação literal e semântica mínimas de 80%, fontes e citações materiais verificadas, C1–C5 reproduzidas e decisões específicas de Helena/Cícero.

Essa pendência é evidância faltante, não uma trava burocrática. O piloto continua funcional sem falsear maturidade.
