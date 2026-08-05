# Quem commita sozinho — diagnóstico fechado

**Data:** 2026-08-05. Pergunta do Igor: *"descobrir qual processo commita sozinho"*.

## O processo

`git-tools/sync_github.ps1`, escrito em 11/07/2026. Faz três coisas, nesta ordem:

```powershell
git -C $repositoryRoot add -A                      # tudo, sem seleção
git -C $repositoryRoot commit -m "sync: <data>"    # no branch ATUAL
git -C $repositoryRoot push origin main            # sempre em main
```

Log em `%LOCALAPPDATA%\Codex\logs\fabricas-peticoes-github-sync.log`, cadência diária por
volta de 21:03 UTC. **O gatilho não foi localizado**: não há tarefa agendada, hook de git,
entrada de registro nem atalho de inicialização que o invoque. Ele roda — o log prova —, mas
por caminho que não aparece em nenhuma das rotas inspecionadas. Fica como lacuna.

## Duas correções ao que eu havia relatado antes

**1. Os commits de 03:22, 03:35 e 03:54 de hoje NÃO foram dele.** São meus, de subagentes da
campanha — trazem mensagens minhas (`fix: consolidar artefatos protegidos da regua` etc.), não
o padrão `sync: <data>`. A confusão veio de todo commit desta máquina usar
`igormorais123+noreply@users.noreply.github.com`, o que apaga a distinção entre autor humano,
agente e automação. A troca de branch às 03:08 também foi de subagente, não do script.

**2. O script tem um defeito real, e é outro.** `commit` usa o branch corrente, mas `push` é
sempre `origin main`. Quando o checkout está em branch de trabalho — como esteve em 03 e 04 de
agosto —, o commit `sync:` **cai no branch de trabalho** e o push não o leva a lugar nenhum.
Foi assim que `3866e1c16 sync: 2026-08-04 21:02:50` virou a base da campanha.

## O que isso escondeu: o push está quebrado há cinco dias

```
2026-07-31 10:43Z  ERRO: Falha ao enviar o commit ao GitHub.
2026-07-31 21:04Z  ERRO: ...
2026-08-01 21:03Z  ERRO: ...
2026-08-02 21:04Z  ERRO: ...
2026-08-03 20:51Z / 20:56Z / 21:02Z  ERRO: ...
2026-08-04 21:05Z  ERRO: ...
```

`main` local está **26 commits à frente** de `origin/main`, zero atrás. A causa é o limite
rígido de 100 MB por arquivo do GitHub: entre os objetos não enviados há pelo menos seis acima
disso.

| Tamanho | Objeto |
|---|---|
| 375,0 MB | CORSAN |
| **291,3 MB** | `_FORJA_HARNESS/state/case-email-auto-19f8cec883a0ac31/n3_artifacts/F1_INGESTAO_SEGURA/injection_scan.json` |
| 212,0 MB | CORSAN |
| 156,7 MB | Jalusa |
| 108,4 MB | Memoriais |
| 105,8 MB | Memoriais |

`git push --dry-run` passa, porque não transfere objeto; o push real morre na transferência.
Existe maquinário para isso — `refresh_large_assets_manifest.ps1` e `publish_large_assets.ps1`
— mas o manifesto `large-assets-manifest.json` não é atualizado desde 11/07, e `add -A` empacota
o arquivo grande antes que qualquer política o intercepte.

**O `injection_scan.json` de 291 MB é defeito da FORJA, não do acervo.** Um laudo de varredura
de injeção não tem por que ter esse tamanho; ele existe em duas cópias (`n3_artifacts/` e
`runs/.../attempt-.../`), ambas ainda no disco. Vale investigar à parte.

## Consequências para quem trabalha aqui

1. **Trabalho em branch nesta pasta tem risco de fundo**: às 21:03 UTC, o que estiver no disco
   é varrido para dentro de um commit no branch corrente, validado ou não.
2. **O remoto está congelado em 17/07.** Quem confiar no GitHub como cópia de segurança do
   acervo está confiando em fotografia de três semanas atrás.
3. **A autoria em git não distingue humano de automação.** Enquanto isso valer, "quem fez este
   commit" não é pergunta respondível pelo histórico.

## Recomendação

Não mexer no script sem decidir antes o que ele deve ser. Três reparos independentes, em ordem
de custo:

1. **`push` no branch corrente, ou `commit` só em `main`.** Hoje as duas metades discordam, e é
   isso que espalha commit `sync:` por branch de trabalho. Reparo de uma linha.
2. **Barrar arquivo acima de 100 MB antes do `add -A`**, encaminhando-o à rota de large assets
   que já existe. Sem isso o push continua morrendo todo dia em silêncio — o erro só aparece
   num log que ninguém abre.
3. **Identidade de commit distinta para a automação** (`forja-sync@…`), para que o histórico
   volte a responder quem fez o quê.

## Executado em 05/08/2026, por determinação do Igor ("resolva tudo diagnosticado")

**Os três reparos do script foram feitos.** `git-tools/sync_github.ps1`:

1. **A automação só age em `main`.** Em branch de trabalho ela registra e sai sem tocar em
   nada. Escolhi isto em vez de "empurrar o branch corrente" porque publicar branch de
   trabalho no remoto é efeito colateral que ninguém pediu, e varrer trabalho em curso para
   dentro de um commit é pior do que não sincronizar naquele dia.
2. **Arquivo acima de 95 MB é retirado do commit antes de ele existir**, por descoberta de
   tamanho sobre o índice — não sobre o disco, porque é o índice que diz o que entraria. A
   margem de 5 MB existe porque o limite do GitHub vale para o objeto após compressão.
   *Por que não bastava o maquinário que já existia:* `refresh_large_assets_manifest.ps1` é
   uma **lista fixa de três arquivos** escrita em 11/07. Ele nunca protegeu contra o arquivo
   grande que aparece amanhã, e foi exatamente por isso que CORSAN, Jalusa, os Memoriais e o
   nosso próprio `injection_scan` passaram direto.
3. **Identidade própria** (`FORJA sync <forja-sync@localhost>`), para o histórico voltar a
   responder quem fez o quê.

E um quarto, que não estava na lista e é o que mais importa: **a falha passou a aparecer fora
do log.** `git-tools/STATUS_SYNC.md` registra a última execução, e em caso de erro diz com
todas as letras que o GitHub não é cópia de segurança atual. Automação que grava o próprio
fracasso onde ninguém olha produz a confiança sem produzir o efeito.

Contraprova em `git-tools/test_sync_github.ps1`, incluindo o exercício real num repositório
descartável: o arquivo grande é retirado **e o pequeno continua** — filtro que esvazia o
commit também "resolveria" o push, resolvendo parar de sincronizar. Verificado ponta a ponta
no repositório real: rodando fora de `main`, o script adiou e não tocou em nada.

## O artefato de 291 MB NÃO foi encolhido, e isso é deliberado

O `injection_scan.json` do caso Vale Trading está **preso por hash em três pontos do ledger de
eventos** (`FORJA_EVENTS.jsonl` e dois eventos numerados). Regenerá-lo com o scanner corrigido
produziria conteúdo equivalente e quebraria a cadeia de auditoria — exatamente o que o sistema
existe para preservar. Evidência não se encolhe retroativamente. A correção do scanner vale
para os próximos laudos; este permanece como está, e sai do versionamento pela regra de
tamanho.

## Higiene de acesso, conferida

Repositório **privado**, **zero forks**, **um único colaborador** (o próprio Igor).
Duas ressalvas honestas: o estado do 2FA **não pôde ser lido** — o token do `gh` não tem
escopo para isso, então é `[INDETERMINADO]`, não "desligado"; e o bloqueio de forks **não é
aplicável** a repositório privado de conta pessoal, o GitHub recusa a alteração. Este segundo
ponto é, por si, um argumento a favor da opção "organização do escritório": controles que
existem em repositório de organização simplesmente não existem em conta pessoal.
