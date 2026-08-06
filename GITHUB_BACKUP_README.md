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

## O repositório único anterior

`igormorais123/fabricas-de-melhoria-de-peticoes` misturava o motor com o acervo
processual e deixou de conseguir subir em 31/07/2026: o primeiro commit não
publicado sozinho tinha 3,47 GB, e commit é atômico. O script daquela rotina,
`git-tools/sync_github.ps1`, está aposentado e sai sem fazer nada se for chamado.
