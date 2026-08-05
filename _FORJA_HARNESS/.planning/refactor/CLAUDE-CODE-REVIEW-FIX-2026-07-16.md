---
status: all_fixed
findings_in_scope: 8
fixed: 8
skipped: 0
deferred: 0
iteration: 1
source_commit: 2c76ee4e
branch: codex/forja-claude-audit-fixes
---

# Correções da auditoria da mudança do Claude Code

## Resultado

Todos os defeitos de código, estado, documentação e organização local identificados na auditoria foram corrigidos. Por decisão do Igor, o backup privado permanece exclusivamente neste computador e serviços de nuvem não fazem parte da política de recuperação da FORJA.

## Correções aplicadas

1. `validate_forja_n3.py` executa o validador F7 pelo caminho real em `_scripts_oneoff/`.
2. O validador F7 movido recompõe o `sys.path` e resolve `state/` a partir da raiz da FORJA.
3. `forja_reconcile.py` mantém gates atuais em `gates` e registra gates encerrados em `gateHistory`, com data, responsável e motivo.
4. O histórico apagado em quatro estados foi recuperado a partir do commit anterior à reconciliação.
5. `REGUA_MANIFEST.json` foi rebaselinado somente para os três utilitários protegidos revisados.
6. A documentação técnica e o plano P14 refletem o arquivo visual externo e o limite de domínio do FocoEdital.
7. O FocoEdital duplicado e seus documentos saíram do arquivo visual; a duplicata foi eliminada após backup portátil e restauração verificada.

## Evidência de recuperação

- 2.427 blobs rastreados inspecionados; zero ausentes e zero divergências substantivas.
- Backup privado do FocoEdital: SHA-256 `48F1436624E71CEA6F8E5129F3E979C0D63EE6B430053B4E242F714FA809E616`.
- 955 arquivos restaurados e comparados; zero divergências.
- Manifesto privado: `C:\Users\IgorPC\.claude\backups\forja-cleanup-20260716\MANIFESTO_RESTAURACAO.md`.
- Manifesto versionado da movimentação: `MIGRATION_MANIFEST.json`.

## Validação

- `python validate_forja_n3.py`: aprovado, 9 comandos, 11 contratos e 1.180 JSONs verificados.
- `python -m unittest discover -s . -p "test_*.py"`: 245 testes aprovados; 2 ignorados por dependência opcional.
- `python forja_regua.py --rapida`: aprovado nas 10 suítes canônicas após rebaseline revisado.
- `git diff --check`: aprovado.
- Varredura do diff por segredos: nenhuma credencial encontrada.

## Política de backup

O backup é privado, local e verificado. Deve permanecer neste computador; não sugerir nem configurar OneDrive ou outro armazenamento em nuvem para estes artefatos. Essa é uma decisão operacional consciente do Igor, não uma pendência desta correção.
