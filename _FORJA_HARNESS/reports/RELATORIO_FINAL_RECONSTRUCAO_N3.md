
---

## ERRATA (auditoria ultracode, 10/07/2026 tarde)

1. **Art. 343-A do RISTJ existe.** A afirmação de "referência inexistente ao art. 343-A" (seções 2 e 6 deste relatório) estava errada: a Emenda Regimental nº 53/2026 do STJ (DJe 01/07/2026) criou o art. 343-A, que exige resumo dos fundamentos de fato e de direito, dos pedidos e das decisões impugnadas nas petições dirigidas ao STJ. Fonte capturada em `_FORJA_HARNESS/cache/fontes_oficiais/STJ_ER_53_2026_DJe_2026-07-01.pdf`. A regra do verificador foi corrigida em 10/07/2026 (ver Lição 45 da RETROSPECTIVAS). A remoção da citação nas peças N3 não causou dano (a síntese executiva permaneceu), mas a citação ao dispositivo é legítima em peças dirigidas ao STJ.
2. **Metadados.** Os DOCX/PDF N3 saíram com autor "thais mulati" e título "Proposta de Serviços e Honorários" herdados do template (pipeline visual não sanitizava). Corrigido na raiz (`PecaVisual.salvar()`) e nos artefatos em 10/07/2026 (ver Lição 46).
3. **Patrícia/Fábio.** A frase "a N3 não foi enviada" estava correta, mas omitia o essencial: a versão que FOI enviada às 03:42 (e-mail 19f4ac2a) é anterior à N3 e contém o pedido de honorários recursais removido por erro jurídico. Pendência de reenvio registrada no painel com urgência (sessão de 14/07). Ver Lição 48.
