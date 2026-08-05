Você é o mutador da geração 1 do experimento evolutivo prompt-mestre-v2 da FORJA (modelo AutoResearch/Karpathy).

PARENT (winner da geração 0): `autoresearch/evolucao/prompt-mestre-v2/winners/gen-0.md` (estratégia compress — leia-o integralmente; ele é a base do seu trabalho).
CONTEXTO: o parecer independente do ciclo AR-1 (`autoresearch/ciclos/ciclo-1/AR_PARECER_INDEPENDENTE_varB.md` — leia-o) aprovou o parent COM RESSALVAS: a compressão enfraqueceu 3 obrigações materiais do prompt vigente. Para referência de força normativa original, o vigente está em `../PROMPT-FABRICA-MELHORIA-PETICAO.md`.

TAREFA: escrever UMA variante completa (texto integral, pronta para uso — nunca resumo):

`autoresearch/evolucao/prompt-mestre-v2/gen-1/varH_hybrid.md` — estratégia HYBRID: manter a concisão e a estrutura de gates verificáveis do parent, RESTAURANDO com força normativa explícita e inequívoca as 4 recomendações do parecer:
1. Cobertura incompleta do ato impugnado mantém a produção em `internal_working` e PROÍBE gerar DOCX/PDF final.
2. A simulação quantitativa de Helena é gate NÃO-ELETIVO (nunca pode ser pulada, resumida ou substituída).
3. `forja_editorial_fidelity.py` valida o resultado do Fable; qualquer falha de fidelidade recomeça do texto auditado.
4. Risco crítico (>2 precedentes banidos OU >3 pendências abertas) BLOQUEIA a liberação no gate final.

REGRAS:
- Nenhuma obrigação material do parent pode ser perdida; os 4 reforços entram como obrigações duras (verbo proibitivo/bloqueante), não como recomendações.
- Não editar nenhum outro arquivo.
- O arquivo começa com `<!-- mutacao: hybrid | eixo: parent compress + reforço das 4 recomendações do parecer AR-1 | parent: gen-0/varB -->`.
- Português com acentuação correta; o texto da variante não menciona este experimento.

AO FINAL, reporte: caminho escrito, contagem de caracteres e 1 frase explicando o diff conceitual em relação ao parent.
