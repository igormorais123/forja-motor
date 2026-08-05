# Adoção de Mutação Semântica na FORJA
## Medição real em 6 casos + Proposta de Rampa

**Data da medição:** 2026-08-05  
**Casos medidos:** 6 (auto, azimut, CASO-07/CASO-07, CASO-16, natura, patricia)  
**Status:** Proposição de rampa honesta para produção

---

## 1. Distribuição Real Medida

### 1.1 Por Família de Mutação

| Família | Score | Mortos | Aplicáveis | Casos | Status |
|---------|-------|--------|------------|-------|--------|
| **S1** (inversão tese) | 0.00 | 0 | 2 | 1 | Raro, sem cobertura |
| **S2** (troca de parte) | 0.00 | 0 | 23 | 5 | Zero cobertura |
| **S3** (valor/data) | 0.067 | 2 | 30 | 6 | Zero cobertura, 1 gate minimal |
| **S4** (troca de pedido) | 0.00 | 0 | 12 | 4 | Zero cobertura |
| **S5** (sobreabstração) | 0.00 | 0 | 23 | 6 | Zero cobertura |
| **S6** (deturpação precedente) | 0.75 | 9 | 12 | 5 | 3 casos em 1.0; 2 casos em 0.0 |

**Agregado geral:** 0.165 (11/67 mutantes mortos)

### 1.2 Por Caso

| Caso | Score | Mortos | Aplicáveis | Suite | Notas |
|------|-------|--------|------------|-------|-------|
| auto | 0.0 | 0 | 14 | Inválida | Suite reprova original |
| azimut | 0.0 | 0 | 21 | Válida | Zero gates disparados |
| CASO-07/CASO-07 | 0.0 | 0 | 12 | Válida | Zero gates disparados |
| CASO-16 | 0.2 | 4 | 20 | Válida | S6: 1.0 (4/4) |
| natura | 0.25 | 3 | 12 | Inválida | S6: 1.0 (3/3); suite reprova original |
| patricia | 0.174 | 4 | 23 | Válida | S6: 1.0 (2/2); S3: 0.286 (2/7) |

**Observação:** 2 de 6 suites reprovam o original — minuta possivelmente errada ou suite genérica demais. O harness degradou corretamente (score usa só verificador).

### 1.3 Controles Benignos

- **Espectro:** 5 paráfrases neutras (conectivos, verbos, advérbios)
- **Resultado:** 0 mortes em 6 casos
- **Conclusão:** Nenhuma rigidez excessiva detectada

---

## 2. Diagnóstico por Família

### S1 — Inversão de Tese (0.0)

**Dados:**
- Ocorrências: 2 mutantes em 1 de 6 casos (natura)
- Taxa de morte: 0/2 (0.0)

**Problema:** Suíte não percebe "é cabível" → "não é cabível"

**Causa provável:** Testes de suíte focam em afirmação positiva; negação é contexto raro em estudo preliminar

**Recomendação:** Não exigir hoje. S1 é falso negativo legítimo em documentos que não negam ativamente.

---

### S2 — Troca de Parte (0.0)

**Dados:**
- Ocorrências: 23 mutantes em 5 de 6 casos
- Taxa de morte: 0/23 (0.0)

**Problema:** Nenhum gate detecta agravante→agravado, autor→réu

**Cenário mais grave:** Trocar "agravante" por "agravado" passa intacto. Peça que pede provimento para a CASO-01 mas a identifica como agravada vai para produção.

**Causa:** Nenhum gate no verificador confere identidade de partes

**Recomendação:** **BLOQUEAR com gate G-PARTIDO (novo).** Proposta:
- Extrair nomes das partes do cabeçalho da peça
- Comparar com menções no corpo
- P0 se nome de parte trocada aparecer com papel oposto

**Risco de falso positivo:** Baixo (nomes únicos). Teste em 2 casos primeiro.

---

### S3 — Valor ou Data (0.067)

**Dados:**
- Ocorrências: 30 mutantes em 6 casos
- Taxa de morte: 2/30 (0.067)

**Problema:** Trocar data de "22 de fevereiro de 2013" por "22 de fevereiro de 2014" mata apenas em Patricia (CT-PATRICIA-001), e trocar "54,5%" por "55,5%" mata em Patricia (CT-PATRICIA-005).

**Achado:** Patricia tem suíte de testes robusta; outros 5 não.

**Causa:** Sem suíte ou com suíte genérica, datas/valores não viram teste determinístico

**Recomendação:** Não exigir hoje. Criar gate G-DATA-COERENCIA (novo) que:
- Extrai datas argumentativas e verifica contra campo de data da peça (cabeçalho/metadados)
- Dates < "data de protocolo" devem estar justificadas por contexto jurídico
- Valores declarados uma vez devem ser iguais em segunda menção

**Limiar sugerido:** P1 (aviso), não P0, até cobertura atingir 0.6.

---

### S4 — Troca de Pedido (0.0)

**Dados:**
- Ocorrências: 12 mutantes em 4 de 6 casos
- Taxa de morte: 0/12 (0.0)

**Problema:** "Provimento"→"desprovimento" passa intacto. Peça que pede desprovimento mas escreve "provimento" na síntese vai para produção.

**Cenário mais grave:** Toda peça recursal tem "pedido" — é campo estrutural, não contextual. Trocar aqui é falso negativo crítico.

**Causa:** Nenhum gate confere coerência entre pedido (§ estrutural) e corpo

**Recomendação:** **BLOQUEAR com gate G-PEDIDO (novo).** Proposta:
- Extrair marcador de pedido do cabeçalho/"PEDIDOS" ou § final
- Procurar por "provimento"/"desprovimento"/"procedência"/"improcedência" no corpo
- P0 se corpo contém pedido oposto ao marcador

**Risco:** Peças podem mencionar pedido da parte contrária para refutá-lo. Salvaguarda: permitir "pedido da..."/"alegação de...".

---

### S5 — Sobreabstração (0.0)

**Dados:**
- Ocorrências: 23 mutantes em 6 casos
- Taxa de morte: 0/23 (0.0)

**Problema:** "REsp 1.234.567/DF" → "a jurisprudência pacífica" passa. "Súmula 609 do STJ" → "o entendimento sumulado" passa.

**Cenário mais grave:** Argumento jurídico é citação concreta; converter para paráfrase genérica esvazia a defesa.

**Causa:** Nenhum gate exige lastro concreto (número de precedente) em campos de argumentação

**Recomendação:** **Criar gate G-CITACAO-LASTRO (novo).** Proposta:
- Seção de "jurisprudência", "precedente", "entendimento pacífico": obrigar número de REsp/ARE/STF/STJ
- Frase genérica sozinha é P1 (aviso) se não vem antecedida de citação concreta em 1-3 parágrafos
- Exceto: "jurisprudência dos tribunais superiores" e "entendimento consolidado" são genéricos permitidos

**Limiar:** P1 hoje, P0 após cobertura 0.7.

---

### S6 — Deturpação de Precedente (0.75)

**Dados:**
- Ocorrências: 12 mutantes em 5 de 6 casos
- Taxa de morte: 9/12 (0.75)
- Sucesso em 3 casos: libra (1.0), natura (1.0), patricia (1.0)
- Falha em 2 casos: auto (0.0 em 2 mutantes), CASO-07 (0.0 em 1 mutante)

**Problema:** "Firmou entendimento" → "afastou o entendimento" é detectado por verificador:G4-sumula em 75% dos casos. Por quê? G4 confere par súmula×tribunal:

| Mutação | Alvo | Atuação |
|---------|------|---------|
| Súmula 5 do STJ → Súmula 5 do STF | Troca tribunal | G4 dispara (1.0) |
| Súmula 609 do STJ → afastou entendimento | Muda verbo | G4 dispara? |

**Achado:** Verificador G4 está robocop em 3/5 casos — libra, natura e patricia têm contexto que permite detecção. Auto e CASO-07 são documentos diagnósticos sem Súmulas; mutante S6 não dispara gate.

**Causa:** G4 assume presença de Súmula; em diagnósticos preambulares, não há.

**Recomendação:** **S6 é CANDIDATA a exigência, mas com salvaguarda.**

Proposta de implementação:
1. Criar gate G4-DETURPACAO-VERBO (novo):
   - Palavras-chave "afastou", "rejeitou", "superou", "controverteu" no contexto de precedente
   - Se precedente anterior no parágrafo era "firmou", "assentou", "consolidou": P0
   - Exceto se sujeito for claramente adversário ("a ré afastou o entendimento")

2. Gate G4-SUMULA permanece como está

3. Exigir S6 em MODO ALERTA:
   - P0 em peças de Justiça Federal (REsp/STJ/RE/STF)
   - P1 em peças de primeira/segunda instância
   - Porque: diagnósticos preambulares raramente têm precedentes consolidados

**Limiar sugerido:** P0 hoje para peças de STJ/STF; P1 para demais. Score 0.75 é aceitável para exigência de P1.

---

## 3. Proposta de Rampa Honesta

### Semana 1-2: Gates novos GR (Risco mínimo)

**Instalar em P1 (aviso, não trava):**

1. **G-PARTIDO** — Identidade de partes trocada (S2)
   - Implementação: `forja_gate_partido.py` (100 linhas)
   - Teste: auto + azimut (partes nominadas)
   - Métrica: zero falsos positivos em acervo
   
2. **G-DATA-COERENCIA** — Data argumentativa vs. cabeçalho (S3)
   - Implementação: extrair datas, comparar com "data de protocolo"
   - Teste: patricia + cabreuva
   - Métrica: revisar 3 avisos manualmente

3. **G-CITACAO-LASTRO** — Paráfrases genéricas sem número (S5)
   - Implementação: buscar "jurisprudência", "entendimento", "precedente" sem REsp/ARE/STF
   - Teste: todos os 6 (teste estrutural, sem executar)
   - Métrica: 1-2 avisos por peça é esperado

4. **G-PEDIDO** — Coerência de pedido (S4)
   - Implementação: extrair marcador de pedido, procurar oposto no corpo
   - Teste: libra + patricia
   - Métrica: zero falsos positivos

### Semana 3: Aumentar cobertura

**Observar P1s em produção:**
- Taxa de falsos positivos por gate
- Necessidade de ajuste de padrão
- Feedback de redator ("esse aviso é legítimo?")

**Criar casos de teste:**
- Sabotagem: peças com mutações S2-S5 injetadas manualmente
- Controle benigno: peças legítimas que não devem disparar

**Métricas de porta:**
- Nenhum gate P1 com >2 falsos positivos em 10 casos
- Todos os 4 gates rodáveis sem erro em lote
- Documentação: 1 página/gate explicando limiar

### Semana 4: Promover a P0

**Promoção de P1 → P0 (apenas se critério atendido):**

1. **G-PARTIDO**: Pronto para P0 imediato (zero ambiguidade)
2. **G-PEDIDO**: Pronto para P0 imediato (estrutural, não contextual)
3. **G-DATA-COERENCIA**: Promover a P0 se 0 falsos positivos em 5 casos
4. **G-CITACAO-LASTRO**: Manter em P1; feedback do Fábio define P0

### Semana 5+: S6 em Alerta

**Considerar S6 como critério de sucesso, não bloqueador:**

- Incorporar G4-DETURPACAO-VERBO (novo) ao verificador
- Manter G4-SUMULA como está
- P0 em REsp/STJ/RE/STF; P1 demais
- Score 0.75 (9/12) é aceitável para produção com recomendação (não rejeição)

---

## 4. Risco de Falso Positivo — Taxa Medida

### Taxa atual no acervo

| Gate | Taxa medida | Intervalo confiança |
|------|-------------|---------------------|
| G4-SUMULA (verificador atual) | 0/9 falsos positivos em 6 casos | [0%, 40%] |
| Controles benignos | 0/5 mortes em 6 casos | [0%, 52%] |

**Interpretação:** Com n pequeno (6 casos), margem de incerteza é larga. Não significa "seguro". Significa "0 visto até agora".

### Recomendação operacional

- **Nunca** instalar P0 novo sem par controle benigno + sabotagem
- **Sempre** rodar em lote de 6 casos novos antes de promover de P1
- **Aceitar** P1 como status permanente se taxa de falso positivo > 1 em 20 casos

---

## 5. O que NÃO fazer

### Anti-padrões detectados

1. **Não calibrar gate contra string gerada por mutador**
   - Exemplo: detectar "desprovimento" porque S4 troca "provimento"→"desprovimento"
   - Armadilha: gate passa 100% em mutantes S4 mas falha em variações legítimas
   - Teste: peça onde adversário pede desprovimento (menção legítima)

2. **Não exigir score 0.8 hoje em nenhuma família**
   - Atual: 0.165 geral
   - Objetivo: 0.8
   - Rampa: P1 semanas 1-4, P0 semana 5+, score 0.5 aceito em P0 até semana 8

3. **Não deitar berço em gate de P0 fraco**
   - Exemplo: S2 em 0.0 não é "falha do harness", é "falha do gate"
   - Responsabilidade: escrever G-PARTIDO, não "ajustar" S2

4. **Não injetar gate P0 bloqueante sem testar sabotagem**
   - Obrigação: matar cada mutante planejado em 2 de 3 exemplos
   - Prova: JSON com mutante injetado + gate dispara

---

## 6. Cronograma Proposto (aprovação pendente)

| Fase | Data | Atividade | Gate | Status |
|------|------|-----------|------|--------|
| 1 | 2026-08-05 | Medição (realizado) | - | ✓ |
| 2ª | 2026-08-06 | Design G-PARTIDO + G-PEDIDO | S2, S4 | Proposto |
| 2b | 2026-08-07 | Implementação + casos teste | S2, S4 | Proposto |
| 3ª | 2026-08-08 | Design G-DATA + G-CITACAO | S3, S5 | Proposto |
| 3b | 2026-08-09 | Implementação + rodada P1 | S3, S5 | Proposto |
| 4 | 2026-08-12 | Monitorar P1s em produção | S2-S5 | Proposto |
| 5 | 2026-08-15 | Revisar + promover P0 | S2, S4, (S3?) | Proposto |
| 6 | 2026-08-22 | G4-DETURPACAO-VERBO + S6 alerta | S6 | Proposto |

---

## 7. Tabela Resumida de Decisões

| Família | Score | Ação Recomendada | Justificativa |
|---------|-------|------------------|---------------|
| S1 | 0.0 | Ignorar | Raro (1 caso); contexto legítimo |
| S2 | 0.0 | P1 → P0 | Crítico (5 casos); gate novo GR |
| S3 | 0.067 | P1 → esperar | Baixo (1 caso mata); suíte fraca |
| S4 | 0.0 | P1 → P0 | Crítico (4 casos); gate estrutural |
| S5 | 0.0 | P1 → esperar | Exige regra complexa; feedback primeiro |
| S6 | 0.75 | Alerta | Forte em 3 casos; fraco em 2 |

---

## 8. Próximos Passos

1. **Aprovação:** Este documento vai ao Fábio/Igor para decisão sobre cronograma
2. **Infraestrutura:** Registrar em `phase_contracts/` que harness é rodável; decisão de bloqueio é fora de F7
3. **Implementação:** Não começa até aprovação explícita + alocação de tempo
4. **Revalidação:** Depois de cada gate novo, rodar harness em lote de 6 casos novos

---

## Apêndice A: Comando para Rodada Completa

```bash
python3 forja_mutation_lote.py state/case-email-* --output mutation_panel.json
```

(Script a criar em próxima fase)

---

## Apêndice B: Fonte de Dados

**Arquivo:** `mutation_results_temp.json`  
**Data:** 2026-08-05 02:22:47  
**Casos:** 6 (auto, azimut, CASO-07, libra, natura, patricia)  
**Formato:** JSON, uno por harness

---

**Aprovado por:** Pendente  
**Revisor:** Pendente  
**Data de vigência:** Aguardando aprovação
