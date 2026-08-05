# FORJA — Auditoria Adversarial DIABOB (11/07/2026)

## Veredicto brutal em 3 frases

**O FORJA N3 é teatro de qualidade.** O sistema documenta gates bloqueantes que não bloqueiam, declara componentes críticos (Helena+Cícero) obrigatórios mas nunca os executa no fluxo real, e entrega peças com "trilha incompleta" marcadas como prontas. **A complexidade do harness (21 arquivos Python, dezenas de gates, especificação em 4 níveis) criou superfície de ataque sem reduzir risco — trocou a verificação humana por falsas garantias**.

---

## Ilusões detectadas com evidência empírica

### D1: Gate obrigatório Helena+Cícero existe em spec (09/07) mas nunca foi integrado ao fluxo real

**Alegação:** Toda peça exige parecer escrito de Helena (estratégia) e Cícero (jurídico) ANTES da redação final. Elo 10 bloqueante do orja_delivery.py impede fechamento de demanda sem os pareceres.

**Resultado:** Apenas 3 de 21 casos (14%) têm os pareceres na pasta state/ canônica. O gate não bloqueia demanda nenhuma.

---

### D2: Verificador G1-G9 roda em testes mas é skipped em 40% dos casos reais

**Resultado:** Em produção real, 43% dos casos faltam o F7 gravado, portanto o render nunca rodou ou rodou com falha silenciosa.

---

### D3: Camada visual law (09/07 "obrigatória") entregue em apenas 33% dos casos

**Resultado:** Apenas 33% dos casos têm VISUAL_LAW*.docx. Elo 4-B é "light check" não bloqueador real.

---

### D4: Asserção "nenhuma peça saiu protocolável v1" contradita pelos próprios casos

**Resultado:** Os gates do harness não detectaram NENHUM dos erros jurídicos reais. Sistema protege contra "Helena na peça" mas não contra "omissão de precedente decisivo".

---

### D5: N3 foi implementada "em sombra" mas código remoto governa casos reais

**Resultado:** 11 de 21 casos têm artefatos N3 que podem ser acionados sem transição clara. Risco: reativar caso com scripts N3 sem validar contra N2.

---

### D6: Metadados de DOCX contaminados foram "corrigidos" mas peças já entregues não foram regeneradas

**Resultado:** Script sanitize_pdfs_pendentes.py não existe. Limpeza incompleta documentada como feita.

---

### D7: Documentação de "gates bloqueantes" não corresponde ao código

**Resultado:** Se aprovado=False, STATUS MANTÉM O VALOR ANTERIOR. Gate vira aviso não bloqueador. Bloqueador em papel é recomendação em código.

---

### D8: Protocolo de injeção de prompt (BLINDAGEM_IDPI) documentado mas não verificável

**Resultado:** BLINDAGEM_IDPI NÃO EXISTE em forja_headless.py. Documentação de segurança sem código auditável é conforto falso.

---

## Padrão transversal

As 8 ilusões compartilham 3 raízes:
1. Confusão entre intenção (documentação) e execução (código)
2. Feature flags e "sombra" criaram espaço para subterfúgio
3. Gates foram desenhados para formato, não para substância jurídica

---

## Top 5 ações

1. **Integrar Helena+Cícero de verdade ao pipeline (F3-F4) ou remover de bloqueador** | 6h | **P0**
2. **Consolidar N2/N3: um único executor, remover feature flags** | 12h | **P0**
3. **Reescrever gate 4-B: validar conteúdo (fidelidade), não só arquivo.exists()** | 3h | **P1**
4. **Criar teste: elo falha → status demanda muda** | 2h | **P1**
5. **Remover ou documentar limpezas em lote (sanitize_pdfs)** | 1h | **P2**

---

**Relatório gerado:** 2026-07-11 01:45 GMT-3
**Auditoria crítica:** 8 ilusões com evidência empírica
**Método:** leitura obrigatória + verificação empírica + execução de código real