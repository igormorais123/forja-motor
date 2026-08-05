# Parecer independente — variante varB (ciclo AR-1, revisor família claude)

VEREDITO: APTA COM RESSALVAS — preserva as 28 obrigações materiais mapeadas do prompt vigente
(25 PRESERVADAS, 3 ENFRAQUECIDAS: bloqueio de cobertura do ato impugnado, obrigatoriedade da
simulação de Helena, elo entre risco crítico e liberação), acrescenta rastreabilidade de origem
intelectual e protocolo de mídia/rajada, e traz 5 riscos concretos (R1-R5).

RECOMENDAÇÕES (resumo — íntegra na devolutiva do revisor, transcrita no relatório do ciclo):
1. Reforçar que cobertura incompleta do ato impugnado mantém `internal_working` e proíbe DOCX/PDF final.
2. Explicitar que a simulação quantitativa de Helena é gate não-eletivo.
3. Explicitar que `forja_editorial_fidelity.py` valida o resultado Fable e que falha recomeça do auditado.
4. Ligar "risco crítico" (>2 precedentes banidos ou >3 pendências) ao bloqueio de liberação no gate final.
5. Detalhar a consequência operacional de "material novo reabre fases".
6. (Opcional) Exemplos de aplicação nas matrizes temáticas.

DECISÃO EVOLUTIVA REGISTRADA: aprovação condicionada → varB permanece vencedora da geração 0,
SEM propagação; as recomendações 1-4 tornam-se a mutação `hybrid` da geração 1 (varB + reforços),
a ser testada em novo ciclo AR antes de qualquer adoção. Gate humano (recibo Ed25519 do Igor)
permanece pendente e obrigatório para qualquer propagação.
