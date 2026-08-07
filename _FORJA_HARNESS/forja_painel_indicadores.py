"""Indicadores automáticos das vozes curtas — e a fila do que vale a pena julgar.

Duas camadas, e a de cima nunca toca a de baixo:

- **Aqui (autônoma):** o que se mede sem julgamento humano — disciplina,
  originalidade, ancoragem no documento. Roda de graça, todo dia, e **não
  promove ninguém**. Nenhum número deste arquivo entra no placar de
  contribuição.
- **`forja_contribuicao.py` (humana):** os vereditos, que são a única coisa que
  faz uma voz subir degrau.

Misturar as duas seria o modo de falha previsível: indicador barato e diário
canibaliza métrica cara e rara, e em três semanas alguém promove um modelo por
ter 0% de violação — que é higiene, não contribuição.

**O indicador que carrega mais informação é o de violação da regra de não-fonte.**
O painel instrui, por escrito, a não citar lei, artigo, súmula, precedente,
número, data ou valor. Violar isso é detectável por regra, e é exatamente o modo
de falha que a bancada de 26/07/2026 mediu no Kimi K3 — 0 de 6 corretas na
condição solta, com quatro invenções. Se ele continua inventando dispositivo sob
instrução expressa, isso aparece sozinho, sem custar julgamento a ninguém.

**A fila não é cronológica.** Julgar observação em que as duas vozes concordam
quase não informa: o veredito move as duas notas na mesma direção e não separa
ninguém. A informação por segundo do tempo humano está no que **uma voz viu e a
outra não**. No primeiro painel real, metade das observações do GLM era eco do
K3 — julgá-las na ordem de saída gastaria metade do tempo em pares que não
discriminam nada.

Uso:
    python forja_painel_indicadores.py indicadores
    python forja_painel_indicadores.py fila --limite 6
"""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

FORJA = Path(__file__).resolve().parent
PAINEIS = FORJA / "telemetria" / "paineis_curtos"
VERSAO = "FORJA-PAINEL-INDICADORES-v1"

# Marcas de fonte jurídica. O painel proíbe todas por escrito; a regex encontra
# a violação. Deliberadamente conservadora: pega o que é inequivocamente uma
# citação, e deixa passar a menção genérica ("conferir o regimento"), que é o
# comportamento CORRETO — apontar o dado a conferir sem afirmar qual é.
PADROES_FONTE = (
    (r"\bart(?:igo)?s?\.?\s*\d", "artigo"),
    (r"\bs[úu]mula\s*(?:n\.?º?\s*)?\d", "súmula"),
    (r"\btema\s*(?:n\.?º?\s*)?\d{3,}", "tema repetitivo"),
    (r"\blei\s*(?:n\.?º?\s*)?\s*\d{1,2}\.?\d{3}", "lei numerada"),
    (r"\b(?:REsp|AREsp|AgInt|RE|ARE|HC|MS|ADI|ADPF)\s*(?:n\.?º?\s*)?\d", "recurso numerado"),
    (r"\b\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}\b", "número CNJ"),
    (r"\b\d{1,2}/\d{1,2}/\d{2,4}\b", "data"),
    (r"\bR\$\s*\d", "valor"),
    (r"\b\d{1,3}(?:\.\d{3})+(?:,\d+)?\b", "cifra"),
)

# Palavras que aparecem em qualquer texto jurídico e não provam leitura do
# documento. Sem esta lista, `ancoragem` daria alto para observação genérica.
VAZIAS = {
    "a", "o", "as", "os", "de", "da", "do", "das", "dos", "e", "em", "no", "na",
    "nos", "nas", "um", "uma", "para", "por", "com", "que", "se", "ao", "aos",
    "sem", "sobre", "ou", "mas", "como", "ja", "nao", "e", "ser", "sao", "foi",
    "pode", "deve", "esta", "este", "essa", "esse", "isso", "seu", "sua", "pelo",
    "pela", "mais", "menos", "muito", "quando", "onde", "porque", "ate", "entre",
    "peca", "caso", "autos", "processo", "decisao", "recurso", "parte", "texto",
    "documento", "argumento", "tese", "fato", "direito", "juiz", "tribunal",
}


# Limiar do eco LEXICAL, e ele é fraco de propósito declarado.
#
# Medido em 07/08/2026 no primeiro painel real, contra dois pares que uma pessoa
# classificou como eco: 0,258 e **0,091**. O segundo par dizia a mesma coisa —
# "os fatos são mesmo incontroversos?" — com vocabulário quase disjunto. Jaccard
# de palavras não alcança paráfrase.
#
# A tentação era baixar o limiar até bater com as duas classificações. Seria
# moldar o instrumento até ele aprovar: n=2, e 0,091 fica ABAIXO de pares
# comprovadamente não relacionados (0,147). O limiar ficou em 0,25, que separa o
# par forte do ruído, e o resto do trabalho continua sendo do veredito
# `duplicada`, que é humano. Este indicador **sugere** candidatos a eco; ele não
# mede taxa de eco, e o relatório não o chama assim.
LIMIAR_ECO_LEXICAL = 0.25


def _norm(texto: str) -> str:
    sem = unicodedata.normalize("NFKD", texto or "")
    sem = "".join(c for c in sem if not unicodedata.combining(c))
    return sem.casefold()


def _palavras(texto: str) -> set[str]:
    return {p for p in re.findall(r"[a-z]{4,}", _norm(texto)) if p not in VAZIAS}


def _jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def citacoes_fora_do_documento(texto: str, alvo: str) -> list[str]:
    """Citações que a voz trouxe e que **não estão no documento** que ela leu.

    Este é o indicador que interessa, e ele nasceu de dois falsos positivos
    seguidos do detector puramente lexical. O primeiro foi o GLM escrevendo
    `"Súmula 7 ..." é a tese inteira comprada sem verificação` — citação entre
    aspas, resolvida excluindo aspas. O segundo foi `a própria Súmula 5/7 que
    ele invoca pode funcionar contra`, sem aspas nenhuma, e igualmente correto:
    a voz falava da súmula que **o documento** invoca.

    Continuar refinando a regex até ela concordar comigo seria moldar o
    instrumento. A distinção real não é sintática, é de origem: **citar o que o
    documento cita é ler; citar o que não está lá é inventar** — e inventar é o
    modo de falha que a bancada mediu no Kimi K3.

    Compara o número, não o rótulo: "Súmula 7", "súmula nº 7" e "Súmula 7/STJ"
    são a mesma coisa para este fim, e o que se procura no documento é o número
    ao lado da mesma palavra-chave.
    """
    alvo_norm = _norm(alvo)
    fora = []
    for bruto in re.findall(r"\b(?:s[úu]mula|art(?:igo)?s?\.?|tema|lei)\s*"
                            r"(?:n\.?º?\s*)?([\d./-]+)", _norm(ASPAS.sub(" ", texto or ""))):
        numeros = [n for n in re.split(r"[./-]", bruto) if n.isdigit()]
        # Basta um dos números aparecer no documento para que a menção seja
        # leitura, não invenção. "Súmula 5/7" casa com um documento que fale de
        # qualquer uma das duas.
        if numeros and not any(n in alvo_norm for n in numeros):
            fora.append(bruto)
    return fora


def ancoragem_de(alvo: str):
    """Devolve uma função que mede o quanto uma observação vem do documento.

    O painel chama isto com o alvo em mãos e grava **só o número** por
    observação. Guardar o texto do documento no artefato para medir depois
    duplicaria conteúdo do caso sem necessidade, e um número não reconstrói
    frase nenhuma.

    Ancoragem baixa não prova que a observação é ruim: "confira o regimento
    antes de prometer sustentação oral" pode ser o melhor conselho do painel e
    não repetir palavra do documento. O indicador serve para o extremo — a voz
    cujas observações inteiras não tocam o texto que ela deveria ter lido.
    """
    doc = _palavras(alvo)

    def medir(texto: str) -> float | None:
        if not doc:
            return None
        return round(_jaccard(_palavras(texto), doc), 3)

    return medir


# Aspas de todos os feitios que os modelos usam. Trecho entre aspas é a voz
# CITANDO o documento, não afirmando fonte própria — e a diferença decide.
ASPAS = re.compile(r'["“”‘’«»](.{1,400}?)["“”‘’«»]',
                   re.DOTALL)


def violacoes_de_fonte(texto: str) -> list[str]:
    """Citações que a instrução proibiu. Mede disciplina, não acerto.

    Uma observação pode estar certíssima e ainda assim violar: o ponto é que a
    voz curta **não é fonte**, e o custo de conferir o que ela citou é do
    escritório. Ela deve apontar o dado a verificar, não afirmá-lo.

    **Trecho entre aspas é descartado antes da medição, e isso veio de um falso
    positivo real.** Na primeira execução o indicador acusou o GLM 5.2 de citar
    súmula. Ele tinha escrito `"Súmula 7 sobre matéria de qualificação jurídica"
    é a tese inteira comprada sem verificação` — estava **citando o blueprint
    para criticá-lo**, que é o comportamento desejado. Sem esta exclusão, o
    indicador puniria justamente a voz que aponta o dado a conferir.

    Isso torna a medida conservadora: uma voz poderia contornar o indicador
    escrevendo a invenção entre aspas. Não é o modo de falha que interessa — o
    que se persegue aqui é o modelo que **afirma** dispositivo inventado, e esse
    não põe aspas em nada.
    """
    baixo = _norm(ASPAS.sub(" ", texto or ""))
    achados = []
    for padrao, nome in PADROES_FONTE:
        if re.search(padrao, baixo, re.IGNORECASE):
            achados.append(nome)
    return achados


def medir_painel(dados: dict) -> dict:
    """Indicadores de um painel: disciplina, sobreposição entre vozes, ancoragem."""
    por_voz = {}
    conjuntos: dict[str, list[tuple[str, set[str]]]] = {}

    for bloco in dados.get("vozes") or []:
        modelo = bloco["modelo"]
        conjuntos[modelo] = [(o["obsId"], _palavras(o["texto"]))
                             for o in bloco.get("observacoes") or []]

    for bloco in dados.get("vozes") or []:
        modelo = bloco["modelo"]
        observacoes = bloco.get("observacoes") or []
        linhas = []
        for obs in observacoes:
            palavras = _palavras(obs["texto"])
            # Sobreposição com a MAIOR semelhança encontrada nas outras vozes.
            # Máximo, não média: basta uma outra voz ter dito o mesmo para que
            # esta observação deixe de discriminar.
            melhor, de_quem = 0.0, None
            for outro, itens in conjuntos.items():
                if outro == modelo:
                    continue
                for outro_id, outro_conj in itens:
                    valor = _jaccard(palavras, outro_conj)
                    if valor > melhor:
                        melhor, de_quem = valor, outro_id
            violou = violacoes_de_fonte(obs["texto"])
            linhas.append({
                "obsId": obs["obsId"],
                "sobreposicao": round(melhor, 3),
                "ecoLexicalDe": de_quem if melhor >= LIMIAR_ECO_LEXICAL else None,
                # Gravada pelo painel no momento da geração; painel antigo não a
                # tem, e `None` é o veredito honesto para isso.
                "ancoragem": obs.get("ancoragem"),
                # Lexical: só olha a forma. Fica para painel antigo, que não
                # tem o campo abaixo, e para a fila, onde vale como aviso.
                "violouNaoFonte": violou,
                # De origem: o que a voz citou e o documento não tem. É o que
                # distingue ler de inventar, e o que conta no agregado.
                "citouForaDoDocumento": obs.get("citouForaDoDocumento"),
            })
        n = len(linhas) or 1
        por_voz[modelo] = {
            "modelo": modelo,
            "familia": bloco.get("familia"),
            "observacoes": len(linhas),
            "violacoes": sum(1 for l in linhas if l["citouForaDoDocumento"]),
            "violacoesLexicais": sum(1 for l in linhas if l["violouNaoFonte"]),
            "semMedidaDeOrigem": sum(1 for l in linhas if l["citouForaDoDocumento"] is None),
            "taxaViolacao": round(100.0 * sum(1 for l in linhas if l["citouForaDoDocumento"]) / n, 1),
            "ecoLexical": sum(1 for l in linhas if l["ecoLexicalDe"]),
            "sobreposicaoMedia": round(sum(l["sobreposicao"] for l in linhas) / n, 3),
            "segundos": bloco.get("segundos"),
            "truncadas": bloco.get("observacoesTruncadas", 0),
            "descartadas": bloco.get("observacoesDescartadas", 0),
            "itens": linhas,
        }
    return {"caso": dados.get("caso"), "fase": dados.get("fase"),
            "arquivo": dados.get("_arquivo"), "vozes": por_voz}


def _carregar(pastas: list[Path]) -> list[dict]:
    achados = []
    for pasta in pastas:
        if not pasta.exists():
            continue
        for arquivo in sorted(pasta.rglob("*PAINEL_CURTO*.json")):
            try:
                dados = json.loads(arquivo.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                continue
            if dados.get("contrato") != "FORJA-PAINEL-CURTO-v1":
                continue
            dados["_arquivo"] = str(arquivo)
            achados.append(dados)
    return achados


def indicadores(pastas: list[Path] | None = None) -> dict:
    paineis = _carregar(pastas or [PAINEIS, FORJA / "state"])
    agregado: dict[str, dict] = {}
    repeticao: dict[str, list[tuple[str, set[str]]]] = defaultdict(list)

    medidos = [medir_painel(p) for p in paineis]
    for medida in medidos:
        for modelo, linha in medida["vozes"].items():
            alvo = agregado.setdefault(modelo, {
                "modelo": modelo, "familia": linha["familia"], "paineis": 0,
                "casos": set(), "observacoes": 0, "violacoes": 0,
                "ecoLexical": 0, "truncadas": 0, "descartadas": 0,
                "violacoesLexicais": 0, "semMedidaDeOrigem": 0,
                "sobreposicoes": [], "segundos": [],
            })
            alvo["paineis"] += 1
            alvo["casos"].add(medida["caso"])
            alvo["observacoes"] += linha["observacoes"]
            alvo["violacoes"] += linha["violacoes"]
            alvo["violacoesLexicais"] += linha["violacoesLexicais"]
            alvo["semMedidaDeOrigem"] += linha["semMedidaDeOrigem"]
            alvo["ecoLexical"] += linha["ecoLexical"]
            alvo["truncadas"] += linha["truncadas"]
            alvo["descartadas"] += linha["descartadas"]
            alvo["sobreposicoes"].append(linha["sobreposicaoMedia"])
            if linha["segundos"]:
                alvo["segundos"].append(linha["segundos"])

    # Repetição entre casos: a mesma voz dizendo quase a mesma coisa em
    # documentos diferentes é texto genérico, não leitura. Só faz sentido com
    # dois ou mais painéis — abaixo disso o indicador fica `None`, e não zero.
    for painel in paineis:
        for bloco in painel.get("vozes") or []:
            for obs in bloco.get("observacoes") or []:
                repeticao[bloco["modelo"]].append(
                    (painel.get("caso") or "?", _palavras(obs["texto"])))

    saida = []
    for modelo, linha in agregado.items():
        casos = len(linha.pop("casos"))
        segundos = linha.pop("segundos")
        sobrep = linha.pop("sobreposicoes")
        n = linha["observacoes"] or 1
        itens = repeticao.get(modelo) or []
        pares = [
            _jaccard(a, b)
            for i, (caso_a, a) in enumerate(itens)
            for caso_b, b in itens[i + 1:]
            if caso_a != caso_b
        ]
        saida.append({
            **linha, "casos": casos,
            "taxaViolacao": round(100.0 * linha["violacoes"] / n, 1),
            "ecoLexicalSugerido": round(100.0 * linha["ecoLexical"] / n, 1),
            "sobreposicaoMedia": round(sum(sobrep) / len(sobrep), 3) if sobrep else 0.0,
            "repeticaoEntreCasos": round(max(pares), 3) if pares else None,
            "segundosMedio": round(sum(segundos) / len(segundos), 1) if segundos else None,
        })
    saida.sort(key=lambda l: (l["taxaViolacao"], -l["observacoes"]))
    return {
        "contrato": VERSAO,
        "em": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "natureza": (
            "Indicadores automáticos de DISCIPLINA e ORIGINALIDADE. Não medem "
            "se a observação é boa, não substituem o veredito humano e NÃO "
            "promovem ninguém. Promoção é `forja_contribuicao.py`."
        ),
        "paineis": len(paineis),
        "modelos": saida,
        "detalhe": medidos,
    }


def fila(limite: int = 6, pastas: list[Path] | None = None) -> list[dict]:
    """O que julgar primeiro: o que discrimina, não o que chegou antes.

    Ordem: menor sobreposição primeiro. Observação que só uma voz teve é a que
    separa as duas; observação em que as duas concordam move as duas notas na
    mesma direção e informa pouco.

    Já decidida não volta para a fila — a fila é de trabalho pendente, não de
    histórico.
    """
    import forja_contribuicao as fc

    decididas = {d["obsId"] for d in fc.carregar()["decisoes"]}
    candidatos = []
    for painel in _carregar(pastas or [PAINEIS, FORJA / "state"]):
        medida = medir_painel(painel)
        textos = {o["obsId"]: o["texto"]
                  for b in painel.get("vozes") or []
                  for o in b.get("observacoes") or []}
        for modelo, linha in medida["vozes"].items():
            for item in linha["itens"]:
                if item["obsId"] in decididas:
                    continue
                candidatos.append({
                    "obsId": item["obsId"], "modelo": modelo,
                    "caso": painel.get("caso"), "painel": painel["_arquivo"],
                    "sobreposicao": item["sobreposicao"], "ecoLexicalDe": item["ecoLexicalDe"],
                    "violouNaoFonte": item["violouNaoFonte"],
                    "texto": textos.get(item["obsId"], ""),
                })
    candidatos.sort(key=lambda c: (c["sobreposicao"], c["obsId"]))
    return candidatos[:limite]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    i = sub.add_parser("indicadores", help="disciplina e originalidade por voz")
    i.add_argument("--json", action="store_true")
    f = sub.add_parser("fila", help="o que julgar primeiro")
    f.add_argument("--limite", type=int, default=6)
    args = ap.parse_args(argv)

    if args.cmd == "indicadores":
        relatorio = indicadores()
        if args.json:
            print(json.dumps(relatorio, ensure_ascii=False, indent=2))
            return 0
        if not relatorio["modelos"]:
            print("nenhum painel encontrado — rode `forja_painel_curto.py` primeiro")
            return 0
        print(f"{relatorio['paineis']} painel(éis) medido(s)\n")
        print(f"{'modelo':<20} {'obs':>4} {'casos':>6} {'viol%':>6} {'ecoLex%':>8} "
              f"{'repet':>6} {'seg':>6}")
        parciais = 0
        for linha in relatorio["modelos"]:
            repet = linha["repeticaoEntreCasos"]
            # Painel gerado antes do campo de origem não tem a medida. Imprimir
            # 0,0% ali seria o zero silencioso que a casa proíbe: indistinguível
            # de "medimos e não houve violação".
            if linha["semMedidaDeOrigem"] >= linha["observacoes"]:
                viol = "   n/d"
                parciais += 1
            else:
                viol = f"{linha['taxaViolacao']:>6.1f}"
            print(f"{linha['modelo']:<20} {linha['observacoes']:>4} {linha['casos']:>6} "
                  f"{viol} {linha['ecoLexicalSugerido']:>7.1f} "
                  f"{(f'{repet:.2f}' if repet is not None else '  n/d'):>6} "
                  f"{(linha['segundosMedio'] or 0):>6.1f}")
        if parciais:
            print(f"\n[n/d] {parciais} voz(es) sem medida de origem: os painéis são "
                  "anteriores\n      ao campo `citouForaDoDocumento`. Rode o painel de "
                  "novo para medir —\n      zero por ausência de medição seria mentira.")
        print("\nviol% = citou fonte que NÃO está no documento — inventou, em vez de ler.")
        print("        Citar o que o documento cita é leitura, e dois falsos positivos")
        print("        do detector puramente lexical foram o que produziu a distinção.")
        print("ecoLex% = SUGESTÃO de eco por vocabulário compartilhado, limiar 0,25.")
        print("        NÃO é a taxa de eco: paráfrase passa batido — medido, um par")
        print("        real de eco deu 0,091. Quem mede eco de verdade é o veredito")
        print("        `duplicada`, que é humano.")
        print("repet = semelhança máxima da própria voz ENTRE casos distintos;")
        print("        alto significa texto genérico, não leitura do documento.")
        print("\nNada aqui promove ninguém. Promoção é `forja_contribuicao.py`.")
        return 0

    if args.cmd == "fila":
        itens = fila(limite=args.limite)
        if not itens:
            print("fila vazia — ou tudo já foi julgado, ou não há painel")
            return 0
        print(f"{len(itens)} observação(ões) por julgar, as que mais discriminam primeiro:\n")
        for item in itens:
            marca = " [violou não-fonte: " + ", ".join(item["violouNaoFonte"]) + "]" \
                if item["violouNaoFonte"] else ""
            eco = f" [eco lexical de {item['ecoLexicalDe']}]" if item["ecoLexicalDe"] else ""
            print(f"({item['obsId']}) {item['modelo']} · {item['caso']} "
                  f"· sobrep {item['sobreposicao']}{eco}{marca}")
            print(f"   {item['texto']}")
            print(f"   forja_contribuicao.py registrar --painel \"{item['painel']}\" "
                  f"--obs {item['obsId']} --veredito <v> --por <nome>\n")
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
