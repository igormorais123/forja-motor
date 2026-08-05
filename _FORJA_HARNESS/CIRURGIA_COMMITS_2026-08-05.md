# Cirurgia nos commits não publicados — o que foi feito e por que o push continua travado

**Data:** 2026-08-05. **Autorização:** Igor escolheu, entre três opções apresentadas,
"reescrever os 26 commits não publicados". **Backups:**
`backup/main-antes-do-reparo-20260805` e `backup/codex-antes-do-reparo-20260805`.

## Feito

Reescrita da faixa `origin/main..{main, codex/forja-v3-governanca-github}` removendo dos
commits 9 caminhos que apontavam para blobs acima de 100 MB. Resultado verificado:

| | antes | depois |
|---|---|---|
| blobs > 95 MB em `main` | 7 | **0** |
| blobs > 95 MB em `codex` | 8 | **0** |
| commits em `main` | 26 | **26** |
| commits em `codex` | 60 | **60** |
| `git fsck` | — | limpo |
| baseline / régua | — | 90/90 · APROVADO |

Mensagens, datas e autoria preservadas; nada foi esmagado. Os arquivos continuam no disco,
restaurados a partir do backup e conferidos por sha256 — as quatro cópias do ZIP de 375 MB
são byte-idênticas.

**A branch `codex` contém `main` inteira** (60 à frente, 0 atrás). Por isso a cirurgia cobriu
as duas: reescrever só `main` faria o merge devolver os blobs.

## Três erros meus no caminho, todos com custo real

1. **O checkout final do `filter-branch` apagou os arquivos do disco.** Eu não previ que
   remover o caminho dos commits removeria o arquivo da árvore de trabalho. Recuperados do
   backup, mas se a tag não existisse, 1,3 GB de material de caso teria sido perdido.
   *Lição: antes de `filter-branch`, a tag de backup não é higiene — é a única cópia.*
2. **Persegui um caminho por vez sem perceber que era um blob só.** O ZIP de 375 MB existe em
   quatro caminhos (o original e três "duplicatas verificadas"); meu detector guardava um
   dicionário `sha → caminho` e ficava com o último. A cada passada eu removia um caminho, o
   blob continuava alcançável pelos outros, e eu concluía que "sobrou mais um". Foram três
   passadas desnecessárias. *Um blob tem N caminhos; remover blob é remover todos eles.*
3. **`awk` mutilou caminho com acento**, devolvendo linha vazia, e `git rev-list --objects`
   ainda cita caminho de forma diferente conforme `core.quotepath`. A lista só ficou correta
   com Python e `-c core.quotepath=false`.

## O push continua travado, e por outro motivo

**A cirurgia era necessária e não é suficiente.** Medido depois dela:

```
origin/main..main = 36.040 objetos, 9,12 GB descomprimidos
o PRIMEIRO commit da faixa, sozinho = 2.681 objetos, 3,47 GB
```

O GitHub devolve `HTTP 500` na transferência. Tentado e recusado: push inteiro, push em lotes
de 4, push commit a commit pelo caminho de ancestralidade, push para ramo temporário,
`http.postBuffer` de 500 MB e `http.version HTTP/1.1`. **Um commit é atômico — não há como
fatiar 3,47 GB.** E não há chave SSH configurada nesta máquina (`Permission denied
(publickey)`), que é a rota que costuma escapar do limite do endpoint HTTP.

Ou seja: eu havia diagnosticado *um* bloqueio — arquivos acima de 100 MB — e existiam **dois**.
O segundo é o volume por commit, e ele não se resolve por reparo de engenharia.

## O que resolveria, e é decisão do Igor

1. **Git LFS para os binários volumosos.** Resolve os dois bloqueios de uma vez. Custo: a cota
   gratuita é 1 GB e o acervo passa disso — vira cobrança mensal recorrente. Exige autorização
   de gasto.
2. **O acervo não vai ao GitHub.** O remoto guarda o engine; o material de cliente passa a ter
   backup por outra via. Resolve junto a questão de onde o acervo mora, e é coerente com a
   separação engine/acervo que a campanha de lapidação já recomendara por outros motivos.
3. **Chave SSH**, como tentativa antes das duas acima. É barato de testar, mas eu não apostaria:
   3,47 GB num único push continua sendo muito, e a limitação pode não ser só do endpoint HTTP.

Enquanto nenhuma delas for tomada, vale registrar sem eufemismo: **o GitHub não é cópia de
segurança deste repositório.** Está congelado em 17/07/2026, e o
`git-tools/STATUS_SYNC.md` passará a dizer isso a cada execução da rotina.
