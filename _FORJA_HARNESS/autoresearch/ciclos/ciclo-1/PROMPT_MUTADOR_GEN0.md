Você é o mutador da geração 0 do experimento evolutivo prompt-mestre-v2 da FORJA (modelo AutoResearch/Karpathy).

ALVO: o prompt-mestre real em `../PROMPT-FABRICA-MELHORIA-PETICAO.md` (relativo ao diretório atual `_FORJA_HARNESS` — leia-o integralmente).
CONTEXTO DE LIÇÕES NOVAS: leia `../APRENDIZADOS_FEEDBACK_HUMANO.md` (diretrizes 6 a 24, posteriores à última evolução do alvo em 08/07/2026).

TAREFA: escrever DUAS variantes completas do prompt-mestre (texto integral, prontas para uso — nunca resumo), cada uma com UMA estratégia de mutação declarada:

1. `autoresearch/evolucao/prompt-mestre-v2/gen-0/varA_expand.md` — estratégia EXPAND: incorporar ao prompt as cautelas das diretrizes 6-24 que ele ainda não cobre (origem operacional nunca na peça; cronologia com identidade própria de cada ato; teste de suficiência da fonte por proposição; separação produto interno × externo; admissibilidade fundamento a fundamento; prescrição por matriz). Preservar TUDO que o prompt vigente já manda.
2. `autoresearch/evolucao/prompt-mestre-v2/gen-0/varB_compress.md` — estratégia COMPRESS: mesma força normativa com menos texto — consolidar instruções redundantes em gates verificáveis e checklists enxutos, sem perder NENHUMA obrigação material do vigente.

REGRAS:
- Não editar nenhum outro arquivo.
- Cada arquivo começa com `<!-- mutacao: expand|compress | eixo: <1 frase> | parent: baseline -->`.
- Português com acentuação correta; o texto da variante não menciona este experimento.

AO FINAL, reporte: caminhos escritos, contagem de caracteres de cada arquivo e 1 frase por variante explicando o diff conceitual.
