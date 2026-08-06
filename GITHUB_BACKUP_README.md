# Onde cada coisa fica: disco e GitHub

Você trabalha em **um lugar só** — esta pasta. A separação em dois repositórios
acontece na publicação, não no seu trabalho: nada muda no caminho dos arquivos,
nas importações do código ou na forma de abrir um caso.

## Os três lugares

| Lugar | Onde | O que guarda |
|---|---|---|
| **Pasta de trabalho** | `…\Escritório fabio osório\fabricas de melhoria de petições\` | tudo, inclusive os autos |
| **Motor** | `C:\Users\IgorPC\repos\forja-motor` → `github.com/igormorais123/forja-motor` | o sistema, sem dado de cliente |
| **Acervo** | `C:\Users\IgorPC\repos\forja-auditoria` → `github.com/igormorais123/forja-auditoria` | a prova do que a esteira fez, com dado de cliente |

Os dois repositórios espelham a **mesma estrutura de caminhos** da pasta de
trabalho. Reconstituir a árvore é copiar um sobre o outro, sem tradução.

As pastas em `repos\` são espelhos de publicação: **não edite nada lá**. O que
você escrever nelas é apagado na próxima sincronização, porque a rotina remove
do repositório o que não existe mais na pasta de trabalho.

## O que vai para cada lado

**Motor** — código, contratos de fase, schemas, testes, templates, doutrina de
operação, identidade visual. É o que será compartilhado com outros escritórios e
depois aberto. Não pode conter nome de cliente, número de processo, CPF, CNPJ
nem inscrição na OAB.

**Acervo** — `_FORJA_HARNESS/state/`, relatórios de execução, modelos aprovados,
painel de gestão, e **o markdown de cada processo concreto**: análise,
cronologia, minuta, parecer, relatório de melhorias. É privado justamente porque
carrega o nome do cliente.

**Só no disco** — os autos. PDF, DOCX protocolado, áudio, imagem digitalizada,
OCR intermediário, o cofre pós-protocolo, caches e o que passa de 95 MB por
arquivo. São os 16 GB que quebraram o repositório único, e voltam do e-mail e do
próprio processo. Dentro de uma pasta de caso a regra é a extensão: `.md` sobe
ao acervo, o resto fica.

Quem decide isso arquivo por arquivo é `_FORJA_HARNESS/forja_fronteira.py`, e
não uma lista escrita à mão. Para conferir um caminho específico:

```powershell
python _FORJA_HARNESS\forja_fronteira.py --classificar "Pasta Do Caso\ANALISE.md"
```

## O que protege isso de dar errado

**Na escrita.** O hook em `.claude/settings.json` roda
`_FORJA_HARNESS/forja_hook_fronteira.py` a cada Write/Edit: se o arquivo vai
para o motor e carrega CNJ, CPF, CNPJ, OAB ou nome de cliente, o aviso sai na
hora, para quem ainda tem o contexto na cabeça. Sem ele, quem escreve às 15h só
descobre às 20h, quando a rotina reprova.

**Na publicação.** O gate de fronteira, descrito acima. É ele que impede — o
hook apenas avisa cedo.

**Depois da publicação.** `_FORJA_HARNESS/reports/GIT_SYNC_STATUS.md`, no acervo
privado, é reescrito a **cada** execução, inclusive quando ela falha, com o
veredito, a hora e o que resolve. `git-tools/STATUS_SYNC.md` é somente o ponteiro
fixo para esse laudo e nunca recebe caminhos ou identificadores da reprovação.
Era o elo que faltava: a rotina roda sozinha às 20:00 e, sem o laudo privado, o
resultado existia apenas no código de saída da tarefa agendada — que ninguém
consulta. Foi assim que o repositório único passou cinco dias sem conseguir
subir enquanto parecia ser cópia de segurança.

## Onde NÃO deve haver cópia

Auditado em 05/08/2026 e saneado em 06/08/2026. A pasta de trabalho é o único git; as duas cascas `.git`
vazias que existiam dentro dela (em `_FORJA_HARNESS/` e numa pasta de caso)
foram removidas — não eram repositórios, mas convidavam a virar um.

Nenhuma cópia solta vaza para o GitHub, porque nenhuma está versionada. O risco
é outro: material sensível fora do alcance do gate, e cópia antiga parecida com
a pasta de trabalho o bastante para alguém abrir por engano.

Duas foram removidas em 06/08/2026, depois da verificação de redundância:

- `Downloads\_FORJA_HARNESS` — 3.312 arquivos, 146 MB, retrato de 19/07, com
  **1.187 arquivos carregando CNJ, CPF, CNPJ, OAB e nome de cliente**. A
  comparação por hash contra a árvore atual mostrou 2.693 idênticos, 547 em
  versão mais velha e apenas 7 exclusivos substantivos — destes, dois só haviam
  mudado de lugar (hoje em `state/`), três eram temporários do Word e dois foram
  renomeados na reforma editorial de 25/07 e seguem verdes no baseline. Nada
  insubstituível.
- `repos\_teste_reconstituicao` — 16.022 arquivos, 649 MB, sobra do teste de
  reconstituição do dia; refaz-se com `git-tools/montar_forja.py`.

O pacote menor com dado de cliente não tinha duplicata inequívoca na pasta de
trabalho. Por isso não foi apagado: saiu de `Downloads` e foi preservado em
`_FORJA_HARNESS\private\quarentena_copias_externas\2026-08-06\Peticao_FORJA_2026-07-23`,
classificado como `LOCAL` e fora dos dois repositórios. A mudança conservou
34/34 arquivos e 17.615.404 bytes.

Fora da pasta de trabalho resta apenas a cópia de pesquisa sem sinal de cliente:

| caminho | tamanho | dado de cliente |
|---|---|---|
| `Documents\FORJA_Valor_Unico_..._20260724` | 16 arquivos, 1,5 MB | nenhum |

**Lacuna conhecida:** não foi possível confirmar se o disco `C:` está
criptografado — a leitura do BitLocker exige elevação. Enquanto isso não for
verificado, o pacote local em quarentena continua legível por quem tiver a
máquina em mãos. Conferir com `manage-bde -status C:` como
administrador.

## Sincronizar

```powershell
python git-tools\sync_forja_repos.py --seco   # mostra o que faria
python git-tools\sync_forja_repos.py          # espelha, commita e envia
```

Roda sozinho todo dia às 20:00, na tarefa agendada
**"FORJA - Sync GitHub (motor + acervo)"**.

Antes de qualquer publicação a rotina passa pelo gate de fronteira. Se houver
sinal de cliente no que iria para o motor, **nada é publicado** — nem o acervo.
O gate roda em modo `nominal` quando encontra o registro de nomes protegidos no
acervo, e em modo `estrutural` quando não encontra; ele declara em qual dos dois
rodou, porque "passou" significa coisas diferentes em cada um.

## Arquivos acima do limite do GitHub

Arquivos com mais de 95 MB ficam fora do commit e entram em
`ARTEFATOS_FORA_DO_REPOSITORIO.json`, na raiz do repositório a que pertenceriam
— nunca em silêncio. Quando estão presos por hash num ledger de auditoria, não
podem ser encolhidos sem quebrar a cadeia.

O esquema anterior de assets de release (`git-tools/restore_github_release_assets.ps1`,
`large-assets-manifest.json`) atendia o repositório único e não é mais usado pela
rotina; permanece no disco como forma de recuperar o que já foi enviado por ele.

## O repositório único anterior, e o que isso significa para o histórico

`igormorais123/fabricas-de-melhoria-de-peticoes` misturava o motor com o acervo
processual e deixou de conseguir subir em 31/07/2026: o primeiro commit não
publicado sozinho tinha 3,47 GB, e commit é atômico. O script daquela rotina,
`git-tools/sync_github.ps1`, está aposentado e sai sem fazer nada se for chamado.
O repositório foi **arquivado** em 05/08/2026 — continua privado e legível, e
deixou de aceitar escrita, para que ninguém volte a tratá-lo como cópia de
segurança viva. Arquivamento é reversível pelo painel do GitHub.

A consequência a ter em mente: o **histórico git desta pasta de trabalho existe
só neste PC**. São 148 commits em 8 branches sem destino remoto, e não há como
publicá-los sem antes filtrar os 16 GB que os acompanham. Você pode continuar
commitando aqui normalmente; o que a sincronização protege é o **estado atual
dos arquivos**, espelhado nos dois repositórios novos, não a linha do tempo que
levou até ele.

## Dois repositórios órfãos: desativados, exclusão pendente

`igormorais123/forja-harness` e `igormorais123/forja-acervo-auditoria` foram
criados na manhã de 05/08/2026, na primeira tentativa de separar motor de
acervo, e abandonados no mesmo dia quando a fronteira passou a ser decidida por
código. Ficaram no GitHub, privados, carregando **22 e 504 caminhos do cofre
pós-protocolo** — a peça efetivamente protocolada e a versão humana final, o
material mais sensível do acervo, que por regra não sai desta máquina.

Tratamento aplicado em 05/08/2026: os dois receberam um aviso no topo do README
e na descrição, dizendo que estão desativados e para onde o conteúdo vivo foi, e
em seguida foram arquivados — ficam somente-leitura e não voltam a receber
escrita por engano.

**Exclusão pendente.** Arquivar tira do caminho, mas não remove: o cofre
continua legível por quem tiver acesso à conta. O que fecha isso é apagar os
dois, decisão já tomada e adiada por praticidade. A remoção pelo `gh` exige o
escopo `delete_repo`, que o token não tem, e o guard global de comandos
perigosos bloqueia o subcomando — então a rota simples é o painel do GitHub, em
Settings → Danger Zone de cada um. Nada se perde: `forja-motor` e
`forja-auditoria` cobrem o que deve ficar versionado, e o cofre pós-protocolo é
exatamente o que não deve.

O repositório único anterior está arquivado desde a mesma data e, por isso, não
aceita nem edição de descrição — o GitHub já exibe o aviso de arquivado a quem
o abre.
