# Incidente Natura — falha de diagramação e endurecimento da FORJA

Data da correção: 21/07/2026. O parecer enviado ao escritório em 20/07/2026 não atendia ao padrão visual obrigatório. Este registro não altera nem substitui o conteúdo jurídico; documenta a falha, a correção local e os gates criados para impedir recorrência.

## Evidência do arquivo efetivamente enviado

O gate OOXML foi reexecutado sobre a cópia arquivada na pasta de entrega, não sobre um arquivo reconstruído:

- corpo principal: 245 parágrafos;
- justificados: 20/245 (8,1633%);
- desalinhados: 225;
- fonte fora de Times New Roman: 195;
- tamanho fora de 12 pt: 195;
- grupos de tabela tipograficamente inconsistentes: 10;
- fólio lateral com largura insegura: 1;
- resultado: reprovado.

Prova: `LAYOUT_AUDIT_ORIGINAL_SENT_CLEAN.json` na pasta `_correcao_visual_2026-07-21`.

## Causa sistêmica

O ledger anterior tratava o lint automático de PDF como se ele bastasse para aprovar a apresentação. Isso não provava alinhamento ou tipografia do DOCX, não exigia uma inspeção visual efetiva de todas as páginas e aceitava campos `approved/pass` produzidos pela própria etapa. O erro foi de gate, não apenas de acabamento do caso.

## Correção do Natura

- corpo limpo: 245/245 justificado, Times New Roman 12;
- controle de alterações: 246/246 justificado, Times New Roman 12;
- tabelas normalizadas com consistência e mínimo de 8 pt;
- fólio reduzido ao limite seguro de 36 pt;
- PDF final via Word COM: 79 páginas;
- inspeção visual: 79/79 páginas, oito checks obrigatórios por página;
- rerender independente do pacote: aprovado, sem achados;
- fidelidade textual e do conteúdo inserido/excluído: aprovada por hashes OOXML.

Artefatos probatórios: `LAYOUT_AUDIT_FINAL.json`, `LAYOUT_AUDIT_REDLINE_FINAL.json`, `VISUAL_REVIEW_ATTESTATION.json`, `VISUAL_QA_LEDGER.json`, `F8_REPLAY_VALIDATION.json` e `NATURA_TEXT_FIDELITY.json`.

## Controles anti-trapaça incorporados

1. `forja_docx_layout.py` recompõe alinhamento, fonte, tamanho, tabelas e largura do fólio diretamente no OOXML.
2. A normalização visual compara assinatura de conteúdo antes/depois e bloqueia alteração de texto ou do conteúdo das revisões controladas.
3. `forja_visual_review.py` exige hashes do DOCX, PDF e de cada PNG, 100% das páginas, checklist integral e execução revisora distinta da geradora; liberação estrita exige ainda recibo humano Ed25519.
4. `forja_package.py` não confia no ledger: reabre o DOCX, rerenderiza o PDF e revalida o atestado.
5. Jurisprudência não passa por nome de arquivo, URL ou JSON declaratório. O pacote exige cobertura de todas as citações, identidade correta do tribunal, captura viva em domínio oficial, trecho probatório reproduzido e recibo humano Ed25519 da aderência entre tese e trecho; escrever `type=human` não vale.
6. Falha de rede, WAF, ausência de fonte ou ambiguidade de tribunal bloqueia; jamais vira conferência presumida.
7. O extrator passou a reconhecer número CNJ de ADI estadual. A ADI 2080508-98.2020.8.26.0000 agora é TJSP, não STF.

## Estado jurídico do parecer corrigido

A correção visual está aprovada. O uso externo permanece bloqueado pelo novo gate jurídico: foram detectadas 21 autoridades e nenhuma possui, no pacote atual, o conjunto completo de captura oficial viva e revisão humana da proposição. O arquivo corrigido é, portanto, material de revisão interna; não foi reenviado nem liberado para cliente/protocolo.
