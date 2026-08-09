# -*- coding: utf-8 -*-
"""Mantém os dois repositórios da FORJA atuais a partir da pasta de trabalho.

Por que existe. O repositório único anterior misturava o motor com 17 GB de
acervo processual e por isso deixou de conseguir subir: o primeiro commit não
publicado sozinho tinha 3,47 GB, e commit é atômico. O push falhava todo dia
desde 31/07/2026, num log que ninguém abria, e o GitHub parecia ser cópia de
segurança sem ser.

    forja-motor       o sistema. Vai ser compartilhado com outros advogados e
                      depois aberto. Não carrega nome de cliente.
    forja-auditoria   o que prova o que a esteira fez: `state/`, relatórios de
                      execução, modelos aprovados, painel. Carrega cliente.

Os autos — laudos, anexos, PDFs dos processos — não vão a nenhum dos dois. Ficam
no disco, e a origem deles é o e-mail.

**Quem decide o destino de cada arquivo é `forja_fronteira.classificar()`, e não
este script.** A primeira versão trazia os próprios mapas, entre eles uma lista
de quatro arquivos chamada `FORA_DO_MOTOR` escrita à mão. Medido em 05/08/2026,
o repositório do motor tinha 1.843 arquivos com sinal de cliente: a lista não
estava errada, estava irrelevante diante do volume. Política em uma função só,
com dois consumidores — o gate e esta rotina; os destinos físicos continuam
separados.

Os dois destinos são pastas e repositórios Git fisicamente independentes. Cada
um recebe somente o conjunto de caminhos classificado para o seu lado, sempre
preservando o caminho relativo da pasta de montagem. Isso mantém a porta
`forja_acervo` estável sem fingir que o motor genérico e a auditoria privada
ocupam uma única árvore pública. O motor pode ser compartilhado com outro
escritório; informação específica da instalação pertence ao acervo.

Uso:
    python sync_forja_repos.py            # sincroniza e envia
    python sync_forja_repos.py --seco     # mostra o que faria, sem tocar em nada
"""
from __future__ import annotations

import argparse
import filecmp
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

TRABALHO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TRABALHO / "_FORJA_HARNESS"))

import forja_fronteira as fronteira  # noqa: E402

REPOS = Path(os.environ.get("USERPROFILE", "C:/Users/IgorPC")) / "repos"
DESTINOS = {
    fronteira.MOTOR: REPOS / "forja-motor",
    fronteira.ACERVO: REPOS / "forja-auditoria",
}

LIMITE_BYTES = fronteira.LIMITE_BYTES

# Arquivos que pertencem ao repositório e não à pasta de trabalho: não são
# apagados na varredura de sobras.
PROPRIOS_DO_REPO = {"README.md", ".gitignore", ".gitattributes",
                    "ARTEFATOS_FORA_DO_REPOSITORIO.json",
                    # Aviso que só existe nesta máquina, ignorado pelo git de
                    # cada repositório: o espelho do motor recebe `CLAUDE.md`,
                    # `AGENTS.md` e as pastas de instrução de agente, então
                    # parece uma pasta de trabalho completa e um agente aberto
                    # ali funcionaria — até a sincronização seguinte apagar o
                    # que foi escrito. Quem clona o motor em outro escritório
                    # está numa pasta de trabalho legítima, e é por isso que o
                    # aviso não vai ao GitHub.
                    "NAO_TRABALHE_AQUI.md"}

# Pastas que nem são percorridas. Diferente da classificação: aqui a razão é
# custo — não adianta caminhar por 16 GB de autos para descartar tudo no fim.
NAO_PERCORRER = {".git", "__pycache__", "node_modules", ".venv", ".pytest_cache",
                 ".mypy_cache", ".ruff_cache", "telemetria"}


def _iguais(a: Path, b: Path) -> bool:
    """Compara por tamanho e conteúdo, nunca por data de modificação.

    Data engana: o observador de mapas reescreve arquivo com conteúdo idêntico e
    a data muda. Sincronizar por data produziria commit vazio de substância todo
    dia, e commit assim treina o leitor a ignorar o histórico.
    """
    try:
        if a.stat().st_size != b.stat().st_size:
            return False
    except OSError:
        return False
    return filecmp.cmp(a, b, shallow=False)


def _pastas_de_topo() -> list[Path]:
    """Só as pastas de topo que podem conter algo versionável.

    A sonda é um caminho de markdown, e não um nome qualquer, porque dentro de
    pasta de caso é a extensão que decide: o `.md` de trabalho vai ao acervo e o
    binário dos autos fica no disco. Sondar com `"/sonda"` seco devolvia LOCAL
    para toda pasta de caso e as excluía da varredura inteira — a decisão por
    arquivo em `levantar()` nunca chegava a ser tomada.

    Percorrer a árvore dos casos custa: são cerca de cem pastas somando 16 GB.
    O custo é de caminhada em metadado, não de leitura — nenhum PDF é aberto —,
    e o gate de fronteira já paga essa mesma caminhada a cada execução.
    """
    alvos = []
    for p in sorted(TRABALHO.iterdir()):
        if not p.is_dir() or p.name in NAO_PERCORRER:
            continue
        destino, _ = fronteira.classificar(p.name + "/sonda.md")
        if destino != fronteira.LOCAL:
            alvos.append(p)
    return alvos


def levantar() -> tuple[dict[str, list[tuple[Path, str]]], list[tuple[str, int]]]:
    """Percorre a pasta de trabalho e agrupa por destino.

    Devolve (por_destino, grandes). `grandes` são os que excedem o limite do
    GitHub: ficam fora do commit e entram no manifesto, nunca em silêncio.
    """
    por_destino: dict[str, list[tuple[Path, str]]] = {
        fronteira.MOTOR: [], fronteira.ACERVO: []}
    grandes: list[tuple[str, int]] = []

    def considerar(caminho: Path) -> None:
        rel = caminho.relative_to(TRABALHO).as_posix()
        destino, _ = fronteira.classificar(rel)
        if destino == fronteira.LOCAL:
            return
        try:
            tamanho = caminho.stat().st_size
        except OSError:
            return
        if tamanho > LIMITE_BYTES:
            grandes.append((rel, tamanho))
            return
        por_destino[destino].append((caminho, rel))

    for arq in TRABALHO.iterdir():
        if arq.is_file():
            considerar(arq)

    for topo in _pastas_de_topo():
        for raiz, dirs, arqs in os.walk(topo):
            dirs[:] = [d for d in dirs if d not in NAO_PERCORRER]
            for nome in arqs:
                considerar(Path(raiz) / nome)

    return por_destino, grandes


def estado_no_git(rels: list[str]) -> tuple[set[str], set[str], str | None]:
    """Como a pasta de trabalho enxerga cada arquivo. (ignorados, novos, indisponível).

    Por que existe. Esta rotina copia da **pasta de trabalho**, não do índice do
    Git, e é a decisão certa: os ledgers de evento do acervo nascem a cada
    execução e nunca estariam commitados na hora da sincronização — exigir
    rastreamento pararia a publicação da cadeia de auditoria toda noite. O preço
    era o silêncio: em 09/08/2026 um script que outra sessão ainda estava
    escrevendo foi deliberadamente deixado fora do commit local e mesmo assim
    subiu ao motor, porque a prudência do commit não se transferia para a
    publicação.

    São dois casos com respostas diferentes, e colapsá-los seria repetir o erro
    da lição 295 — o gate que não sabe decidir escolhendo a resposta mais cara:

    `ignorados`  alguém escreveu no `.gitignore` que aquilo não é para
                 versionar. É declaração humana explícita, e publicar contra ela
                 é contrariar quem declarou. **Não vão.** Medido em 09/08/2026
                 eram 27 arquivos, todos documentação de dependência de terceiro
                 copiada para dentro de uma pasta de caso.
    `novos`      arquivo que existe e ainda não foi commitado. É o estado normal
                 de quem trabalha; a resposta é **declarar**, não barrar.

    Sem Git disponível, ou fora de repositório, devolve conjuntos vazios e o
    motivo. A publicação segue — degradar aberto é o certo aqui, porque a
    alternativa é a sincronização das 20:00 parar por uma conferência auxiliar —,
    mas o laudo diz que não foi possível conferir.
    """
    def git(*args, entrada: bytes | None = None):
        return subprocess.run(["git", "-C", str(TRABALHO), *args],
                              input=entrada, capture_output=True)

    try:
        r = git("ls-files", "-z")
    except OSError as e:
        return set(), set(), f"git indisponível ({e.__class__.__name__})"
    if r.returncode != 0:
        return set(), set(), "a pasta de trabalho não é um repositório Git"

    rastreados = set(r.stdout.decode("utf-8", "replace").split("\0")) - {""}
    novos = sorted(set(rels) - rastreados)
    if not novos:
        return set(), set(), None

    ign = git("check-ignore", "--stdin", "-z", entrada="\0".join(novos).encode())
    # 0 = ignorou algum, 1 = nenhum ignorado. Qualquer outro código é erro real.
    if ign.returncode not in (0, 1):
        return set(), set(novos), "não foi possível consultar o .gitignore"
    ignorados = set(ign.stdout.decode("utf-8", "replace").split("\0")) - {""}
    return ignorados, set(novos) - ignorados, None


def fora_da_publicacao(ignorados: set[str], novos: set[str],
                       so_rastreados: bool) -> set[str]:
    """Quem fica de fora. Regra em uma função só, para poder ser testada.

    O ignorado sempre fica: é exclusão declarada por uma pessoa no `.gitignore`.
    O novo só fica com `--so-rastreados`, porque no dia a dia ele é o ledger de
    evento recém-escrito, não descuido.
    """
    return set(ignorados) | (set(novos) if so_rastreados else set())


def espelhar(itens: list[tuple[Path, str]], repo: Path, seco: bool) -> tuple[int, int]:
    """Copia o que mudou e apaga o que sumiu. Devolve (copiados, removidos)."""
    esperados = {(repo / rel).resolve() for _, rel in itens}
    copiados = removidos = 0

    for fonte, rel in itens:
        alvo = repo / rel
        if alvo.is_file() and _iguais(fonte, alvo):
            continue
        if not seco:
            alvo.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(fonte, alvo)
        copiados += 1

    # Apagar do repositório o que não existe mais na pasta de trabalho — senão o
    # repositório vira acúmulo e deixa de retratar o estado real.
    if repo.is_dir():
        for raiz, dirs, arqs in os.walk(repo):
            dirs[:] = [d for d in dirs if d != ".git"]
            for nome in arqs:
                alvo = Path(raiz) / nome
                if alvo.relative_to(repo).as_posix() in PROPRIOS_DO_REPO:
                    continue
                if alvo.resolve() not in esperados:
                    if not seco:
                        alvo.unlink(missing_ok=True)
                    removidos += 1

    # Pasta que ficou oca depois da remoção. O Git não versiona diretório vazio,
    # então o repositório já estava certo — mas quem abre a pasta vê onze nomes
    # de skill que não existem mais e conclui que a remoção falhou. Aconteceu em
    # 09/08/2026, comigo. Poda de baixo para cima, e só o que estiver vazio.
    if repo.is_dir() and not seco:
        for raiz, dirs, arqs in os.walk(repo, topdown=False):
            atual = Path(raiz)
            if atual == repo or ".git" in atual.parts:
                continue
            try:
                if not any(atual.iterdir()):
                    atual.rmdir()
            except OSError:
                pass
    return copiados, removidos


def publicar(repo: Path, seco: bool) -> str:
    def git(*args):
        return subprocess.run(["git", "-C", str(repo), *args], capture_output=True,
                              text=True, encoding="utf-8", errors="replace")

    git("add", "-A")
    if git("diff", "--cached", "--quiet").returncode == 0:
        return "sem mudanças"
    if seco:
        n = len([l for l in git("diff", "--cached", "--name-only").stdout.splitlines() if l])
        return f"[seco] {n} arquivo(s) entrariam no commit"
    msg = "sync: {:%Y-%m-%d %H:%M:%S}".format(datetime.now())
    c = git("-c", "user.name=FORJA sync", "-c", "user.email=forja-sync@localhost",
            "commit", "-m", msg)
    if c.returncode != 0:
        return f"ERRO no commit: {c.stderr.strip()[:200]}"
    p = git("push", "origin", "main")
    if p.returncode != 0:
        return f"ERRO no push: {(p.stderr or p.stdout).strip()[:300]}"
    return f"enviado: {msg}"


# O laudo de falha pode citar caminho, nome e identificador do arquivo que o
# gate barrou. Portanto ele pertence ao acervo privado, nunca ao diretório
# `git-tools/`, que é publicado no motor. Mantê-lo no motor faria o relatório
# de uma reprovação virar a causa da reprovação seguinte.
ESTADO = TRABALHO / "_FORJA_HARNESS" / "reports" / "GIT_SYNC_STATUS.md"


def registrar_estado(veredito: str, linhas: list[str]) -> None:
    """Escreve, em lugar fixo, como terminou a última sincronização.

    Esta rotina roda sozinha às 20:00. Sem isto, o resultado dela existe apenas
    no código de saída da tarefa agendada, que ninguém consulta — e foi
    exatamente assim que o repositório único passou cinco dias sem conseguir
    subir enquanto parecia ser cópia de segurança. Em 05/08/2026 o gate reprovou
    três publicações seguidas por arquivo recém-criado com dado de caso: se
    tivesse acontecido de madrugada, o silêncio seria idêntico.

    **O laudo vai para o acervo, não para `git-tools/`.** A primeira versão desta
    função gravava em `git-tools/STATUS_SYNC.md`, que é publicado no repositório
    do motor — e o laudo de uma reprovação lista justamente os caminhos e nomes
    que fizeram o gate reprovar. Ou seja: a correção escrita para tornar a falha
    visível criava, ela própria, a via de vazamento que o gate existe para
    fechar. O ponteiro em `git-tools/` continua lá, sem conteúdo, para quem
    procura o estado no lugar antigo.
    """
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    corpo = [f"# Última sincronização com o GitHub", "",
             f"**{veredito}** — {agora}", ""]
    corpo += linhas
    corpo += ["", "---", "",
              "Gerado por `git-tools/sync_forja_repos.py` a cada execução, "
              "inclusive quando ela falha.",
              "Para rodar à mão, a partir da pasta de trabalho: "
              "`python git-tools\\sync_forja_repos.py`."]
    try:
        ESTADO.write_text("\n".join(corpo) + "\n", encoding="utf-8", newline="")
    except OSError:
        pass


def anonimizar_antes_do_gate() -> list[str]:
    """Troca nome de cliente por pseudônimo nos textos do motor. Devolve o que mudou.

    Por que a rotina faz isso em vez de só reprovar. Quem escreve doutrina e
    plano dentro do motor escreve citando o caso pelo nome — é assim que a lição
    fica verificável, e pedir que cada autor lembre do pseudônimo é a lição 87
    outra vez. Sem este passo, um plano escrito à tarde faz a sincronização das
    20:00 reprovar inteira, **inclusive a do acervo**, e o padrão histórico desta
    casa é a falha noturna ir para um log que ninguém abre.

    A troca é conservadora: só nomes que já estão no mapa de pseudônimos do
    acervo, com destino estável (`CASO-04` é sempre o mesmo caso), e restrita a
    `.md` e `.txt` — código e JSON não são reescritos automaticamente, porque
    ali o nome costuma ser chave de configuração ou caminho vivo, e trocá-lo
    quebra execução em vez de proteger.

    O que ela não resolve continua reprovando: nome dentro de identificador
    (`case-email-<cliente>`) exige decisão humana, e o gate logo abaixo é quem
    barra. Anonimizar não substitui o gate; tira dele o trabalho repetitivo.
    """
    try:
        import forja_anonimizar as anon
    except ImportError:
        return []
    regras = anon.carregar_mapa(TRABALHO)
    if not regras:
        return []
    trocados = []
    for caminho, rel, texto in anon.percorrer(TRABALHO, so_texto=True):
        novo, n, _ = anon.anonimizar_texto(texto, regras)
        if n:
            # `newline=""` porque `percorrer` já entrega o texto sem tradução:
            # gravar sem isso trocaria LF por CRLF no arquivo inteiro e faria uma
            # troca de nome aparecer no histórico como centenas de linhas.
            caminho.write_text(novo, encoding="utf-8", newline="")
            trocados.append(rel)
    return trocados


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--seco", action="store_true",
                    help="mostra o que faria, sem copiar, commitar ou enviar")
    ap.add_argument("--sem-gate", action="store_true",
                    help="publica mesmo com a fronteira reprovada (só para diagnóstico)")
    ap.add_argument("--sem-anonimizar", action="store_true",
                    help="não troca nome de cliente por pseudônimo antes do gate")
    ap.add_argument("--so-rastreados", action="store_true",
                    help="publica apenas o que já está rastreado no Git da pasta de "
                         "trabalho; o que ainda não foi commitado fica de fora")
    args = ap.parse_args(argv)

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    if not args.sem_anonimizar and not args.seco:
        trocados = anonimizar_antes_do_gate()
        if trocados:
            print(f"anonimização: {len(trocados)} arquivo(s) tiveram nome de "
                  f"cliente trocado por pseudônimo")
            for rel in trocados[:10]:
                print(f"  {rel}")

    # Gate ANTES de publicar. Publicar é irreversível na prática: histórico de
    # git não se limpa sem force-push, e foi assim que 40 arquivos do cofre
    # pós-protocolo acabaram em dois repositórios que tiveram de ser abandonados.
    laudo = fronteira.varrer(TRABALHO)
    print(f"fronteira: modo {laudo['modo']} | "
          f"motor {laudo['contagem'][fronteira.MOTOR]} | "
          f"acervo {laudo['contagem'][fronteira.ACERVO]} | "
          f"local {laudo['contagem'][fronteira.LOCAL]}")
    if not laudo["aprovado"]:
        for v in laudo["violacoes"][:10]:
            print(f"  [{v['classe']}] {v['caminho']}: {', '.join(v['sinais'][:3])}")
        if not args.sem_gate:
            print(f"REPROVADO — {len(laudo['violacoes'])} violação(ões) na fronteira. "
                  "Nada foi publicado.")
            if not args.seco:
                registrar_estado("REPROVADO — nada foi publicado", [
                    f"O gate da fronteira encontrou {len(laudo['violacoes'])} "
                    "arquivo(s) com sinal de cliente do lado do motor. "
                    "**Os dois repositórios ficaram parados**, inclusive o do "
                    "acervo: publicar é irreversível na prática, e meia "
                    "publicação seria pior.",
                    "",
                    "| arquivo | sinal |",
                    "|---|---|",
                ] + [f"| `{v['caminho']}` | {', '.join(v['sinais'][:3])} |"
                     for v in laudo["violacoes"][:15]] + [
                    "",
                    "O que costuma resolver, nesta ordem: se o sinal está em "
                    "`.md` ou `.txt`, `python _FORJA_HARNESS\\forja_anonimizar.py "
                    "--aplicar --so-texto` troca o nome por pseudônimo. Se está "
                    "em código ou JSON, a decisão é humana — o nome costuma ser "
                    "chave ou caminho vivo, e a saída é registrar o dado no "
                    "acervo e lê-lo por `forja_acervo`.",
                ])
            return 1
        print("AVISO: publicando com a fronteira reprovada, por --sem-gate.")

    por_destino, grandes = levantar()

    # O que a pasta de trabalho diz sobre cada arquivo. Ver `estado_no_git`.
    todos_rel = [rel for itens in por_destino.values() for _, rel in itens]
    ignorados, novos, indisponivel = estado_no_git(todos_rel)
    fora = fora_da_publicacao(ignorados, novos, args.so_rastreados)
    if fora:
        for destino in por_destino:
            por_destino[destino] = [(p, r) for p, r in por_destino[destino]
                                    if r not in fora]

    nota_git: list[str] = []
    if indisponivel:
        print(f"AVISO: não foi possível conferir o estado no Git — {indisponivel}. "
              "Tudo o que a fronteira aprovou foi publicado.")
        nota_git = ["", f"**Estado no Git não conferido**: {indisponivel}. "
                    "Publicou-se tudo o que a fronteira aprovou."]
    else:
        if ignorados:
            print(f"{len(ignorados)} arquivo(s) ignorados pelo .gitignore da pasta de "
                  "trabalho ficaram fora da publicação")
            for rel in sorted(ignorados)[:5]:
                print(f"  [ignorado] {rel}")
        if novos:
            verbo = "ficaram fora por --so-rastreados" if args.so_rastreados else \
                    "ainda não estão commitados e mesmo assim foram publicados"
            print(f"{len(novos)} arquivo(s) {verbo}")
            for rel in sorted(novos)[:5]:
                print(f"  [novo] {rel}")
        if ignorados or novos:
            nota_git = ["", "| estado na pasta de trabalho | arquivos | destino |",
                        "|---|---|---|"]
            if ignorados:
                nota_git.append(f"| ignorado pelo `.gitignore` | {len(ignorados)} | "
                                "**não publicado** — a exclusão é declaração humana |")
            if novos:
                nota_git.append(
                    f"| existe, ainda não commitado | {len(novos)} | "
                    + ("**não publicado** — `--so-rastreados` |" if args.so_rastreados
                       else "publicado, e declarado aqui |"))
            if novos and not args.so_rastreados:
                nota_git += ["", "Publicar o não commitado é deliberado: os ledgers de "
                             "evento do acervo nascem a cada execução e nunca estariam "
                             "commitados na hora da sincronização. O que não pode é "
                             "acontecer em silêncio. Para uma publicação estrita, "
                             "`--so-rastreados`."]

    falhou = False
    resumo: list[str] = ["| destino | arquivos | copiados | removidos | resultado |",
                         "|---|---|---|---|---|"]
    for destino, repo in DESTINOS.items():
        if not (repo / ".git").is_dir():
            print(f"{destino}: repositório ausente em {repo}")
            resumo.append(f"| {destino} | — | — | — | repositório ausente em `{repo}` |")
            falhou = True
            continue
        copiados, removidos = espelhar(por_destino[destino], repo, args.seco)
        if grandes and not args.seco:
            (repo / "ARTEFATOS_FORA_DO_REPOSITORIO.json").write_text(json.dumps({
                "schemaVersion": 1,
                "porQue": ("Acima do limite de 100 MB por arquivo do GitHub. Permanecem "
                           "no disco de trabalho. Quando estão presos por hash num ledger "
                           "de eventos, não podem ser regenerados nem encolhidos sem "
                           "quebrar a cadeia de auditoria."),
                "atualizadoEm": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "arquivos": [{"caminho": c, "bytes": b} for c, b in sorted(grandes)],
            }, ensure_ascii=False, indent=2), encoding="utf-8")
        estado = publicar(repo, args.seco)
        print(f"{destino:6} {len(por_destino[destino]):5} arquivo(s) | "
              f"copiados={copiados:4} removidos={removidos:4} | {estado}")
        resumo.append(f"| {destino} | {len(por_destino[destino])} | {copiados} | "
                      f"{removidos} | {estado} |")
        falhou |= estado.startswith("ERRO")
    if grandes:
        print(f"{len(grandes)} arquivo(s) acima do limite ficaram fora, "
              "listados em ARTEFATOS_FORA_DO_REPOSITORIO.json")
        resumo += ["", f"{len(grandes)} arquivo(s) acima do limite de 95 MB "
                   "ficaram fora do commit, listados em "
                   "`ARTEFATOS_FORA_DO_REPOSITORIO.json` na raiz de cada repositório."]
    if not args.seco:
        registrar_estado("FALHA ao publicar" if falhou else "OK",
                         resumo + nota_git + ["",
                                   f"Fronteira em modo `{laudo['modo']}`."
                                   + ("" if laudo["modo"] == "nominal" else
                                      " **Sem a lista de nomes do acervo**: o gate "
                                      "encontra CNJ, CPF, CNPJ e OAB, mas não nome "
                                      "de cliente.")])
    return 1 if falhou else 0


if __name__ == "__main__":
    sys.exit(main())
