# FORJA N4 — Relatório final de implementação e auditoria

**Data:** 11/07/2026  
**Versão:** `N4.0-candidate`  
**Estado:** implementada em piloto, com três baselines retrospectivas mecanicamente reproduzidas, conselho pendente e sem promoção prospectiva  
**Especificação vigente geral:** N2; candidata operacional de base: N3

> **Atualização do Conselho:** este relatório foi corrigido e complementado por `CONSELHO_SINTESE_IMPLEMENTACAO_FORJA_N4_2026-07-11.md`. Em caso de divergência, prevalece a síntese do Conselho.

## 1. Veredito

A arquitetura N4 foi implementada de ponta a ponta sem substituir silenciosamente o fluxo vigente. Ela acrescenta representação verificável do problema, cobertura, relações entre afirmações e fontes, testes próprios do caso, consistência global, pesquisa científica interdisciplinar, integridade de entrega, aprendizado e visibilidade na gestão.

A auditoria antifraude corrigiu uma conclusão excessiva da versão anterior deste relatório: os três textos já existiam quando os testes foram criados. Portanto, são baselines retrospectivas fortes, não ciclos prospectivos novos. O estágio correto e funcional é:

- Cafelana AgInt: `pilot_blocking`, bloqueada por fonte de origem revogada;
- Patrícia/Fábio, Libra Sul e Saúde: `pilot_blocking`, 24/24, zero P0, dois P1 de conselho, cobertura de mutação literal de 100% e `promotionEligible=false`;
- demais casos: sombra;
- módulos estratégicos condicionais: consultivos;
- rollback: configuração, sem apagar histórico;
- fluxo N2/N3 existente: preservado.

## 2. O que foi implementado

### Contratos e rastreabilidade

- 24 artefatos N4 com envelope comum, versão, caso, fase, aplicabilidade, estado, hashes, produtor, revisor, datas e questões.
- JSON Schemas executados sobre cada artefato, não apenas documentados.
- Catálogo versionado e 11 contratos candidatos F0-F10.
- trilha `N4_EXECUTION_TRACE.jsonl`;
- invalidação sem apagar o artefato anterior;
- hash semântico e registro de fontes do caso.

### Raciocínio e prova

- árvore de questões materiais;
- matriz de cobertura ligada ao rascunho;
- grafo de raciocínio com referências cruzadas;
- identidade canônica de eventos processuais;
- comparação documental sem inferir automaticamente má-fé;
- mapa intertemporal;
- cenários quantitativos com cálculo restrito e reproduzível;
- maturidade de teses, objeção forte e decisões Helena/Cícero;
- contrato temporal que distingue teste prospectivo de baseline retrospectiva;
- auditoria global C1–C5 com evidência medida por camada, sem `pass` manual.

### Ciência interdisciplinar

- classificação de pertinência e intensidade da pesquisa;
- protocolo, inventário de estudos, síntese e mapa afirmação-evidência;
- adaptadores reais Crossref, PubMed/PMC e OpenAlex opcional;
- verificação de DOI/título, versão, revisão por pares e retratação/correção;
- busca de evidência contrária;
- limites entre associação, causalidade, população e indivíduo;
- indisponibilidade de uma base é registrada como degradação, não como ausência de evidência.

### Entrega e gestão

- seleção F9 vinculada aos bytes e ao hash do pacote auditado;
- confirmação F10 por hash real do canal ou por evidência externa vinculada ao hash pré-envio;
- sincronização da visão N4 no sidecar da gestão;
- painel mostra modo, perguntas, testes, ciência, bloqueios e próxima ação;
- artefatos N4 podem ser abertos pelo painel apenas quando estão no catálogo e o hash confere.

## 3. Correções feitas durante a auditoria

1. Caso sem artefatos em sombra deixou de aparecer como aprovado: agora `complete`, `approved` e `blocksCurrentFlow` são estados distintos.
2. Os schemas deixaram de ser apenas arquivos de referência e passaram a ser validados em execução.
3. Campos reservados do envelope não podem mais ser sobrescritos pelo conteúdo funcional.
4. `status` da síntese científica foi separado em `synthesisStatus`.
5. Fórmulas inseguras são rejeitadas mesmo quando não há variáveis declaradas.
6. Comparação de autores científicos passou a tolerar forma abreviada sem aceitar identidade incompatível.
7. Metadados finais são limpos depois do último salvamento do Word, antes do hash e do QA.
8. Estudos e diagnósticos internos não são tratados como petições protocoláveis.
9. A minuta TJDFT perdeu o placeholder de data e passou a usar “data da assinatura eletrônica”.
10. Referências entre perguntas, cobertura, teses e grafo agora são conferidas.
11. Piloto bloqueante foi limitado a casos listados e aos grupos promovidos pelo roadmap; estratégia condicional não trava o fluxo.
12. A declaração falsa `draftedBeforeFinalText=true` dos três canários foi substituída por `executionMode=retrospective_baseline` e `promotionEligible=false`.
13. Cada suíte passou de 5 para 10 testes e agora executa mutation testing literal; os três casos mataram 10/10 mutações literais. Isso não equivale a teste semântico.
14. C1–C4 deixaram de ser passes fixos; C1 verifica hashes, C2 fidelidade semântica origem→final, C3 testes/mutações e C4 referências das questões.
15. Hashes científicos opacos foram migrados para caminho + SHA-256 recalculável; pilotos rejeitam fonte sem caminho.
16. `issues` do envelope deixou de colidir com o mapa intertemporal, que agora usa `temporalIssues`.
17. A gestão revalida o estado corrente e separa aprovação estrutural, elegibilidade de promoção e revisão humana.
18. A telemetria separa `pipelineAprovado` de artefatos com P1; zero P0 deixou de significar documento sem ressalvas.
19. O caso Saúde deixou de usar DOCX volátil da telemetria como fonte primária; a origem agora é o Markdown estável, com fidelidade medida até DOCX/PDF.

## 4. Evidência real

### Correção do piloto Cafelana

- 24/24 artefatos presentes;
- a auditoria encontrou que a minuta usada pelo piloto derivava de arquivo que declarava a própria invalidação;
- o registro de fontes agora aceita estado `revoked`/`stale`, caminho, hash, motivo e origem;
- o validador bloqueia fonte revogada, ausente, alterada ou cuja origem declare invalidação;
- estado atual: 24/24 artefatos presentes, mas seis P0 bloqueantes intencionais ligados à fonte revogada;
- reconstrução depende da íntegra do AgInt da União de 24/06/2026, e-STJ fls. 938/949.

### Piloto científico de saúde

- consulta real a Crossref e PubMed/PMC;
- estudo validado por DOI `10.3399/bjgpopen20X101030`, PMID `32605913` e PMCID `PMC7465578`;
- conclusão usada apenas como apoio contextual;
- nenhuma inferência diagnóstica individual e nenhuma causalidade indevida;
- resultado científico aprovado em sombra, sem achados bloqueantes.

### Três baselines M6 reais

- Patrícia/Fábio: 6 páginas, quantificação reproduzível, 24/24, zero P0, dois P1 de conselho, 10/10 mutações literais mortas;
- Libra Sul: 7 páginas, comparação responsiva, 24/24, zero P0, dois P1 de conselho, 10/10 mutações literais mortas;
- Saúde: 12 páginas, evidência interdisciplinar, 24/24, zero P0, dois P1 de conselho, 10/10 mutações literais mortas;
- 25 páginas foram reinspecionadas visualmente nesses três canários, sem cortes, sobreposições ou diagramas ilegíveis;
- os originais permaneceram intocados; os produtos N4 estão em `state/<case>/n4_cycle_m6/`.
- os três casos estão estruturalmente aprovados para regressão, mas não contam como ciclos prospectivos de promoção.

### Regressão e produção

- corpus N4: 11/11 cenários aprovados;
- suíte automatizada final após o Conselho: 130 testes aprovados, com 2 testes standalone omitidos pelo ambiente principal;
- telemetria real: três documentos renderizados pelo Word, 60 páginas no total;
- varredura: 15 DOCX de produção sem asterisco de marcação;
- tipos reconhecidos corretamente: petição e estudo;
- cadeia F9/F10 testada com arquivo real de pacote e evidência externa.
- os diagramas Mermaid anteriores foram renderizados sem erro; o novo diagrama anti-autocertificação deve integrar a próxima bateria visual dos planejamentos.

Arquivos de evidência:

- `N4_M0_BASELINE_20260711T000646.json`;
- `N4_F5C_PILOT_HEALTH.json`;
- `../telemetria/N4_CORPUS_20260711T002250.json`;
- `../telemetria/TELEMETRIA_LICAO41_2026-07-11_0023.json`;
- `../telemetria/TELEMETRIA_LICAO41_2026-07-11_0047.json`;
- `../telemetria/TELEMETRIA_LICAO41_2026-07-11_0056.json`;
- `../telemetria/TELEMETRIA_LICAO41_2026-07-11_0100.json`;
- `../telemetria/TELEMETRIA_LICAO41_2026-07-11_0134.json` (bateria real final do Conselho);
- `M6_PATRICIA_ANTIFRAUD_RESULT.json`, `M6_LIBRA_ANTIFRAUD_RESULT.json` e `M6_HEALTH_ANTIFRAUD_RESULT.json`;
- `N4_ANTI_FRAUD_AUDIT_RESULT.json`;
- `../state/case-email-cafelana-agint-aresp-2698443-19f2f0876e358eab/n4_artifacts/N4_VALIDATION.json`.

## 5. O que não foi artificialmente declarado pronto

- Cafelana não pode ser refeita com segurança sem o AgInt primário de 24/06/2026; a minuta humana localizada é fonte secundária, não substituto dos autos.
- OpenAlex não foi tratado como obrigatório quando não havia credencial disponível; Crossref e PubMed/PMC forneceram a evidência do piloto.
- `default_on` não foi promovido: além do impacto legado, ainda faltam ciclos prospectivos com testes comprovadamente anteriores ao texto final.
- N4 não substitui decisão jurídica humana, não cria acusação de má-fé e não transforma artigo acadêmico em prova individual.

## 6. Política anti-trava aplicada

Não foram acrescentadas barreiras genéricas de sigilo, classificação de dados ou autorização abstrata. O bloqueio foi reservado a defeitos materiais verificáveis nos grupos promovidos: questão decisiva sem resposta, pedido sem cobertura, terminologia processual incompatível, teste bloqueante reprovado, citação científica inválida, inconsistência global e arquivo de entrega divergente.

Ausências em sombra geram pendência e visibilidade, não interrupção. Módulos condicionais sem aplicabilidade produzem justificativa curta, não burocracia simulada.

## 7. Fechamento

As correções antifraude e as baselines retrospectivas foram concluídas. O M6.4 continua aberto exclusivamente para evidência prospectiva: testes congelados e datados antes do texto final em ciclos novos. Essa pendência não bloqueia o uso piloto, mas impede a promoção geral por presunção.
