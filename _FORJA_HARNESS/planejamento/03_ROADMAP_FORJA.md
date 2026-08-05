# ROADMAP — FORJA N2

**Versão:** N2.0  
**Data:** 2026-07-08  
**Status:** vigente para execução  
**PRD:** `01_PRD_FORJA.md`  
**TDD:** `02_TDD_FORJA.md`  
**Manifest:** `_FORJA_HARNESS/FORJA_SPEC_MANIFEST.json`

> Este roadmap substitui o roadmap v1.0. O objetivo agora é executar o plano novo: evidência primeiro, automação depois.

---

## 1. Princípios de rollout

1. **Não começar por Claude headless.** Começar por estado, evidência, fontes e bloqueios.
2. **Modo sombra não move arquivos.** Sombra compara e propõe promoção; nunca sobrescreve caso real.
3. **Integração degradada é estado válido.** Gmail/Hermes sem login ou sem acesso não são "ok".
4. **Cumprida exige prova.** Pacote pronto não fecha demanda.
5. **Regimento é gate duro.** Sem regimento integral e emendas, não há redação final.
6. **WhatsApp é sanitizado.** Áudio/transcrição bruta ficam fora sem permissão explícita.
7. **Visual law é funcional.** Diagrama que não reduz esforço cognitivo sai.
8. **Fallback não é final.** Degradação técnica precisa de autorização antes de entrega final.

---

## 2. Marcos

### M0 — Travar especificação e segurança operacional

**Duração sugerida:** 2 a 4 dias  
**Risco:** médio  
**Objetivo:** impedir que agentes executem o plano antigo.

**Escopo:**

- manifest vigente em `_FORJA_HARNESS/FORJA_SPEC_MANIFEST.json`;
- PRD, TDD, Roadmap e Diagramas reescritos para N2;
- estados válidos definidos;
- regra de evidência para `cumprida`;
- regra de Calendar como lembrete, não executor;
- regra de WhatsApp sanitizado;
- regra de fonte oficial para citação final.

**Critério de pronto:**

- os quatro documentos originais apontam para N2;
- `FORJA_SPEC_MANIFEST.json` é JSON válido;
- mapas de navegação reconhecem os documentos atualizados;
- nenhum documento vigente promete envio automático, protocolo automático, probabilidade numérica de vitória ou cumprimento sem evidência.

**Reversão:**

- se algum agente depender do texto antigo, usar `05_FORJA_NIVEL_2_ANALISE_E_PLANO_CORRIGIDO.md` como justificativa e manter execução bloqueada até atualizar o agente.

---

### M1 — Reconciliação da fila e ingestão degradável

**Duração sugerida:** 1 semana  
**Risco:** alto  
**Objetivo:** saber o estado real da fábrica antes de produzir.

**Escopo:**

- ler `gestao_escritorio/data/demandas.json`;
- ler `intervencoes_manuais.json`;
- ler `status_integracoes.json`;
- listar pastas de demanda;
- localizar comandos `COMANDO_DO_EMAIL.md`, `COMANDO_DO_WHATSAPP.md`, `COMANDO_MANUAL.md`;
- classificar Gmail/Hermes como `ok`, `degraded`, `needs_login` ou `offline`;
- identificar demandas abertas, vencidas, <=48h, sem resposta com peça e pendência de anexos;
- gerar ou atualizar `FORJA_STATE.json` para piloto.

**Casos piloto:**

- Azimut, porque há duplicidade `Fwd Relatório Azimut` e `Re Relatório Azimut`;
- José Eduardo Siqueira Campos, porque há entregável final local mas status pode precisar reconciliação;
- Laudo Pericial Contábil, pelo mesmo motivo.

**Critério de pronto:**

- 10 demandas reais auditadas;
- nenhuma duplicidade apagada;
- nenhuma demanda marcada como cumprida sem prova;
- estados degradados aparecem como degradados;
- relatório de pendências criado.

**Reversão:**

- se reconciliação falhar, manter painel inalterado e produzir apenas relatório manual de diferenças.

---

### M2 — Gate de fontes, regimento e leis gerais

**Duração sugerida:** 1 a 2 semanas  
**Risco:** alto  
**Objetivo:** bloquear redação sem base normativa e documental.

**Escopo:**

- identificar tribunal pelo CNJ, endereçamento, decisão e classe;
- ler `REGIMENTO_INTERNO_<TRIBUNAL>.md` na pasta;
- validar metadados do regimento: fonte, versão, data de download, emendas posteriores;
- consultar `_LEIS_GERAIS`;
- criar `F3_MAPA_FONTES_E_REGIMENTO.md`;
- montar `sourceLedger`;
- marcar fatos como fonte, declaração, inferência, hipótese ou não verificado.

**Casos piloto:**

- Cafelana, por ter TRF1/STJ;
- Siqueira Campos, por TJTO;
- Memoriais Cautelar Fiscal, por TRF4.

**Critério de pronto:**

- 5 casos com tribunal identificado;
- 5 casos com regimento lido e metadados conferidos;
- pendências P0 nominadas;
- nenhum caso segue para redação final com regimento ausente.

**Reversão:**

- se regimento não for encontrado online, bloquear e pedir PDF oficial manual; não usar resumo.

---

### M3 — Pesquisa oficial e ledger de citações

**Duração sugerida:** 2 semanas  
**Risco:** médio  
**Objetivo:** impedir jurisprudência inventada ou mal atribuída.

**Escopo:**

- usar pesquisa externa como descoberta;
- validar citação final em fonte oficial;
- registrar citações confirmadas;
- registrar citações removidas;
- bloquear citações sem fonte oficial;
- preservar arquivo oficial quando usado como fonte.

**Casos piloto:**

- Cafelana;
- Siqueira Campos;
- LIBRA SUL ou Jorge Haroldo, se houver urgência STJ.

**Critério de pronto:**

- 2 casos com `F5_JURISPRUDENCIA_VERIFICADA.md`;
- 100% das citações finais com fonte oficial ou arquivo oficial arquivado;
- relatório de citações removidas;
- nenhum `[VERIFICAR]` em artefato final.

**Reversão:**

- se portal oficial cair, remover citação do texto final ou bloquear; não substituir por Jusbrasil/Google Scholar como validação.

---

### M4 — Redação com template e visual law controlado

**Duração sugerida:** 2 a 4 semanas  
**Risco:** alto  
**Objetivo:** gerar minuta forte sem quebrar padrão Medina Osório.

**Escopo:**

- partir de `TEMPLATE_MEDINA_OSORIO_PETICAO.docx` ou peça anterior do caso;
- usar blueprint e ledger de fontes;
- aplicar padrão Word do escritório;
- inserir visual law apenas quando funcional;
- usar SVG -> EMF -> Word COM quando houver diagrama vetorial;
- nunca criar peça final de documento vazio.

**Casos piloto:**

- Jalusa, por ter documentação final e QA anterior;
- Cafelana, por ter auditorias e versões comparáveis.

**Critério de pronto:**

- 1 peça piloto DOCX/PDF;
- 0 placeholders;
- padrão Medina preservado;
- diagramas legíveis;
- relatório de alterações e pendências.

**Reversão:**

- se Word COM ou visual falhar, voltar para template/peça anterior; fallback degradado não vira final sem autorização.

---

### M5 — Auditoria, QA visual e fechamento com evidência

**Duração sugerida:** 1 a 2 semanas  
**Risco:** médio  
**Objetivo:** fechar demanda somente quando ela estiver pronta e comprovada.

**Escopo:**

- rodar auditoria jurídica/factual;
- verificar placeholders;
- conferir anexos mencionados;
- renderizar 100% das páginas;
- inspecionar visual;
- gerar pacote de revisão;
- criar draft opcional se autorizado;
- arquivar evidência de envio/protocolo/entrega;
- atualizar painel para `cumprida` apenas com prova.

**Critério de pronto:**

- uma demanda piloto passa de aberta a cumprida com trilha completa:
  comando, fontes, regimento, blueprint, pesquisa, minuta, auditoria, QA, pacote, entrega e evidência.

**Reversão:**

- sem evidência, manter `pronta_para_revisao` ou `aguardando_evidencia_entrega`; nunca `cumprida`.

---

## 3. Tabela de rollout

| Marco | Entrega principal | Sombra | Gate de saída |
|---|---|---|---|
| M0 | docs N2 + manifest | não aplicável | todos os planos originais reescritos |
| M1 | reconciliação da fila | sim | 10 demandas auditadas sem falso cumprimento |
| M2 | fontes/regimento | sim | 5 casos com regimento e pendências claras |
| M3 | citações oficiais | sim | 2 casos com citações finais verificadas |
| M4 | minuta em template | sim | 1 DOCX/PDF com padrão visual aprovado |
| M5 | fechamento evidenciado | sim | 1 demanda cumprida com prova arquivada |

---

## 4. Ordem de casos recomendada

1. **Jalusa:** melhor para validar QA visual e comparação com entrega final.
2. **Cafelana:** melhor para validar estratégia, STJ/TRF1, citações e auditoria.
3. **Siqueira Campos:** melhor para validar regimento TJTO e embargos.
4. **Azimut:** melhor para validar duplicidade de pastas e consolidação sem apagar.
5. **Plano de Saúde Fábio/Mateus:** só depois de pasta, comando, anexos, órgão responsável e evidência mínima estarem mapeados.

---

## 5. Backlog pós-N2

- Transcrição de áudio WhatsApp com permissão explícita.
- Consolidação multi-e-mail por thread/caso.
- Interface móvel sanitizada.
- Banco local de citações oficiais verificadas.
- Automação Codex recorrente com logs de execução.
- Integração mais profunda com painel para aprovações.

---

## 6. O que nunca será automatizado

1. Envio de e-mail ao cliente, escritório ou tribunal.
2. Protocolo judicial.
3. Assinatura digital.
4. Decisão jurídica final grave.
5. Marcação de comunicação informal como evidência final sem arquivo, mensagem, protocolo ou intervenção manual documentada.
6. Marcação de cumprimento sem evidência.
7. Uso de probabilidade numérica de vitória como promessa ou relatório final.

---

## 7. Critério de sucesso FORJA N2

FORJA N2 estará operacional quando Igor puder abrir o painel, escolher uma demanda e obter um pacote de revisão com:

- fontes classificadas;
- regimento conferido;
- pesquisa oficial;
- minuta em padrão Medina Osório;
- auditoria jurídica/factual;
- QA visual completo;
- pendências claras;
- draft opcional autorizado;
- cumprimento somente após evidência.

Isso é mais importante que prometer prazo fixo de 2 ou 4 horas. Velocidade sem prova é risco.
