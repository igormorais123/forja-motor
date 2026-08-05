# Scripts pontuais / históricos (movidos da raiz em 16/07/2026)

Nenhum destes é importado como módulo vivo da esteira. Ficam aqui para consulta; a raiz do harness contém apenas módulos em operação. A exceção operacional explicitada abaixo é `validate_f7_integration.py`: o runner canônico o executa como teste legado pelo caminho `_scripts_oneoff/validate_f7_integration.py`.

| Script | Propósito | Situação |
|---|---|---|
| `build_f2a_igor_20260715.py` | Montagem das árvores F2-A dos casos Igor/Melissa em 15/07/2026 | uso único, datado |
| `neutralizar_marca_docx_puro.py` | Remoção de marca/metadados de DOCX (variante "pura") | utilitário pontual |
| `neutralizar_marca_peticao.py` | Remoção de marca/metadados de petição | utilitário pontual |
| `render_forja_sem_sanitize_corruptivo.py` | Render antigo SEM sanitização — **não usar**; o nome registra o defeito | descontinuado |
| `sanitize_pdfs_pendentes.py` | Sanitização em lote de PDFs pendentes (rodada específica) | uso único |
| `validate_f7_integration.py` | Validação da integração F7 na implantação N3 (plano 08) | validação histórica ainda executada por `validate_forja_n3.py`; não mover sem atualizar o runner |

Se algum voltar a ser necessário de forma recorrente, promover de volta à raiz e registrar em `DOCUMENTACAO_TECNICA.md`.
