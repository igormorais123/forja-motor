# Backup privado no GitHub

Este repositório é a cópia privada e versionada da pasta **Fábricas de Melhoria de Petições**.

## Arquivos acima de 100 MiB

O GitHub bloqueia arquivos Git comuns acima de 100 MiB. Como a conta não possui orçamento disponível no Git LFS, os quatro itens maiores são preservados como assets da release privada `large-files`, sem cobrança adicional de LFS.

O ZIP de laudos, que ultrapassa 2 GiB por poucos megabytes, é enviado em duas partes menores. O PDF de laudo, o banco SQLite privado e as duas partes ficam descritos, com caminho de destino, tamanho e SHA-256, em `git-tools/large-assets-manifest.json`.

Para baixar e restaurar todos os itens nos caminhos originais:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\git-tools\restore_github_release_assets.ps1
```

O script recompõe o ZIP e valida o SHA-256 de todos os arquivos contra o manifesto versionado.

## Atualização

O script `git-tools/sync_github.ps1` atualiza o manifesto e as partes grandes quando necessário, registra as mudanças comuns na branch `main` e envia assets ainda ausentes à release privada. A execução recorrente é gerenciada pelo Codex.

