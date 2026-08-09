"""Placar de contribuição dos modelos — quanto cada voz agrega, medido no uso.

A pergunta que este arquivo responde é a que decide se um modelo novo continua
na esteira: **do que ele disse, o que mudou a peça?** Ela não se responde com
impressão, e não se responde com contagem bruta.

Três armadilhas conhecidas, e o que aqui as evita:

1. **Taxa de acatamento sozinha premia o óbvio.** Um modelo que só diz o que
   todo mundo já ia dizer tem acatamento alto e contribuição zero. Por isso o
   veredito `duplicada` existe e conta no denominador sem somar no numerador:
   estar certo depois dos outros não é agregar.
2. **Amostra pequena mente com confiança.** Duas observações acatadas de duas
   dão 100%. Abaixo de `MIN_OBSERVACOES` e `MIN_CASOS` o placar sai com
   `elegivel: false` e o motivo escrito. É a mesma lição do gate de
   comparabilidade do aprendizado: agregado de ruído tem a forma de padrão.
3. **Contar não é ler.** `amostra` abre as observações reais do artefato do
   caso e mostra na tela sem gravar nada. Nenhuma promoção deveria acontecer
   sem alguém ter lido exemplos — foi olhando só a contagem que a casa quase
   adotou uma regra tirada de ruído.

O ledger central guarda **decisão e localizador, nunca o texto**: a observação
vive no artefato do caso, e quem quiser lê-la abre o painel. E a promoção é
sempre humana, com a evidência congelada no momento em que foi tomada — para
que `revalidar` possa depois dizer se o lastro ainda existe, sem apagar nada.

Uso:
    python forja_contribuicao.py colher --painel F4_PAINEL_CURTO.json --por Igor
    python forja_contribuicao.py placar
    python forja_contribuicao.py amostra glm-5.2-cursor
    python forja_contribuicao.py promover glm-5.2-cursor --para consultivo --aprovado-por Igor
    python forja_contribuicao.py revalidar
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import forja_modelos as fm

VERSAO = "FORJA-CONTRIBUICAO-MODELOS-v1"
FORJA = Path(__file__).resolve().parent
REGISTRO = FORJA / "learning_registry" / "CONTRIBUICAO_MODELOS.json"
BANCADA = FORJA / "telemetria" / "bench_modelos"

# Vocabulário fechado. Prosa livre num campo de veredito vira lixo agregável em
# seis meses, e o placar passa a somar coisas que não são a mesma coisa.
VEREDITOS = {
    "acatada": "mudou a peça",
    "acatada_parcial": "provocou verificação que mudou algo, mas não como proposto",
    "duplicada": "correta e já dita por outra voz — não agregou",
    "rejeitada": "considerada e descartada",
    "errada": "factualmente errada; custou verificação à toa",
}

# Degraus. Nenhum é automático e nenhum se pula: quem está em `observador` não
# vai a `candidato` sem passar por `consultivo`, porque o degrau do meio é onde
# a voz aparece no relatório interno e alguém a lê com atenção.
DEGRAUS = ("observador", "consultivo", "candidato")
DESCRICAO_DEGRAUS = {
    "observador": "opinião avulsa; não entra em artefato que sai da casa",
    "consultivo": "resumida no relatório interno de melhorias da peça",
    "candidato": "elegível a ser proposto para papel real, por ADR próprio",
}

MIN_OBSERVACOES = 12
MIN_CASOS = 3
INDICE_MINIMO = {"consultivo": 25.0, "candidato": 40.0}


class ContribuicaoError(RuntimeError):
    pass


def _agora() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def _ler_json(caminho: Path, padrao=None):
    try:
        return json.loads(caminho.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return padrao


def _sha_do_painel(caminho: Path) -> str | None:
    """SHA-256 do artefato lido, para amarrar o veredito ao texto julgado."""
    try:
        return hashlib.sha256(caminho.read_bytes()).hexdigest()
    except OSError:
        return None


def carregar() -> dict:
    dados = _ler_json(REGISTRO, None)
    if not isinstance(dados, dict):
        return {"contrato": VERSAO, "decisoes": [], "degraus": {}}
    dados.setdefault("decisoes", [])
    dados.setdefault("degraus", {})
    return dados


def gravar(dados: dict) -> None:
    REGISTRO.parent.mkdir(parents=True, exist_ok=True)
    REGISTRO.write_text(json.dumps(dados, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8")


# --------------------------------------------------------------------------
# Colheita
# --------------------------------------------------------------------------

def colher(painel: Path, *, por: str) -> dict:
    """Lê os vereditos preenchidos no artefato do painel e os leva ao ledger.

    Idempotente por (obsId, caso): reprocessar o mesmo painel não duplica nem
    apaga — atualiza a decisão, porque quem revisa a própria decisão está
    corrigindo, não fraudando.
    """
    dados = _ler_json(painel, None)
    if not isinstance(dados, dict) or dados.get("contrato") != "FORJA-PAINEL-CURTO-v1":
        raise ContribuicaoError(f"{painel} não é um painel curto da FORJA")

    familia = {bloco["modelo"]: bloco.get("familia") for bloco in dados.get("vozes") or []}
    caso = dados.get("caso")
    registro = carregar()
    indice = {(d["obsId"], d.get("caso")): d for d in registro["decisoes"]}

    novas, ignoradas, invalidas = 0, 0, []
    for decisao in dados.get("decisoes") or []:
        veredito = decisao.get("veredito")
        if not veredito:
            ignoradas += 1
            continue
        if veredito not in VEREDITOS:
            invalidas.append(f"{decisao.get('obsId')}: veredito {veredito!r} fora do vocabulário")
            continue
        if veredito == "duplicada" and not decisao.get("duplicadaDe"):
            # Sem apontar de quem é o eco, `duplicada` viraria o depósito de
            # tudo que se quer neutralizar sem julgar — e o placar perderia
            # justamente a distinção que ele existe para fazer.
            invalidas.append(f"{decisao.get('obsId')}: `duplicada` exige --duplicada-de")
            continue
        chave = (decisao["obsId"], caso)
        indice[chave] = {
            "obsId": decisao["obsId"],
            "modelo": decisao.get("modelo"),
            "familia": familia.get(decisao.get("modelo")),
            "caso": caso,
            "fase": dados.get("fase"),
            "veredito": veredito,
            "duplicadaDe": decisao.get("duplicadaDe"),
            "motivo": decisao.get("motivo"),
            "por": por,
            "em": _agora(),
            # Localizador, não conteúdo: o texto da observação fica no painel.
            "painel": str(painel),
            # Hash do painel no momento do julgamento. Sem ele, a "evidência
            # congelada" da promoção não estava congelada: o artefato podia ser
            # reescrito depois e nada denunciaria que o veredito foi dado sobre
            # outro texto. `revalidar` compara e acusa. Achado do revisor
            # externo em 09/08/2026.
            "painelSha256": _sha_do_painel(painel),
        }
        novas += 1

    registro["decisoes"] = sorted(indice.values(), key=lambda d: (d["modelo"] or "", d["obsId"]))
    gravar(registro)
    return {"colhidas": novas, "semVeredito": ignoradas, "invalidas": invalidas}


def registrar_uma(painel: Path, obs: str, veredito: str, *, por: str,
                  duplicada_de: str | None = None, motivo: str | None = None) -> dict:
    """Anota um veredito direto no artefato do painel, e colhe em seguida."""
    if veredito not in VEREDITOS:
        raise ContribuicaoError(
            f"veredito {veredito!r} fora do vocabulário: {', '.join(VEREDITOS)}")
    if veredito == "duplicada" and not duplicada_de:
        # Recusado ANTES de escrever no painel. A checagem existe também em
        # `colher`, e não é redundância boba: sem esta, o veredito inválido é
        # gravado no artefato do caso e só recusado na colheita — o painel fica
        # com um estado que o ledger não reconhece, e ninguém percebe.
        raise ContribuicaoError(
            "`duplicada` exige --duplicada-de: sem apontar de quem é o eco, o "
            "veredito vira depósito do que se quer neutralizar sem julgar")
    dados = _ler_json(painel, None)
    if not isinstance(dados, dict):
        raise ContribuicaoError(f"{painel} ilegível")
    achou = False
    for decisao in dados.get("decisoes") or []:
        if decisao.get("obsId") == obs:
            decisao.update({"veredito": veredito, "duplicadaDe": duplicada_de,
                            "motivo": motivo})
            achou = True
    if not achou:
        raise ContribuicaoError(f"observação {obs!r} não existe em {painel.name}")
    painel.write_text(json.dumps(dados, ensure_ascii=False, indent=2) + "\n",
                      encoding="utf-8")
    return colher(painel, por=por)


# --------------------------------------------------------------------------
# Placar
# --------------------------------------------------------------------------

def _bancada(modelo_id: str) -> dict:
    """O que a bancada de fidelidade à fonte já mediu deste modelo.

    A bancada nomeia o modelo pela rota que usou na época (`kimi-k3`), e o
    registro atual o nomeia pela rota de hoje (`kimi-k3-cursor`). Casar pelo
    prefixo é o que evita tratar como "nunca aferido" um modelo que reprovou.
    """
    base = modelo_id.replace("-cursor", "").replace("-api", "")
    achados = []
    for arquivo in sorted(BANCADA.glob("*.json")):
        dados = _ler_json(arquivo, {}) or {}
        for chave, linha in (dados.get("resumo") or {}).items():
            nome = chave.split("/")[0].strip()
            if nome.replace("-api", "") != base:
                continue
            achados.append({"arquivo": arquivo.name, "condicao": chave, **linha})
    if not achados:
        return {"aferida": False, "motivo": "nunca passou pela bancada da casa"}
    invencoes = sum(int(a.get("invencao") or 0) for a in achados)
    provas = sum(int(a.get("provas") or 0) for a in achados)
    corretas = sum(int(a.get("correto") or 0) for a in achados)
    return {"aferida": True, "provas": provas, "corretas": corretas,
            "invencoes": invencoes, "execucoes": achados}


def placar(registro: dict | None = None) -> dict:
    """Agrega por modelo. O índice é auxílio de ordenação, não veredito."""
    registro = registro or carregar()
    por_modelo: dict[str, dict] = {}
    for decisao in registro["decisoes"]:
        modelo = decisao.get("modelo") or "?"
        alvo = por_modelo.setdefault(modelo, {
            "modelo": modelo, "familia": decisao.get("familia"),
            "n": 0, "casos": set(), **{v: 0 for v in VEREDITOS},
        })
        alvo["n"] += 1
        alvo["casos"].add(decisao.get("caso"))
        alvo[decisao["veredito"]] += 1

    saida = []
    for linha in por_modelo.values():
        n = linha["n"]
        casos = len(linha.pop("casos"))
        uteis = linha["acatada"] + 0.5 * linha["acatada_parcial"]
        # Uma frase explica o índice, e essa é a razão de ele ser assim: de cada
        # cem observações, quantas mudaram a peça, descontadas as que estavam
        # erradas. `duplicada` e `rejeitada` ficam no denominador e não somam —
        # dizer o óbvio dilui, como tem de diluir.
        indice = max(0.0, 100.0 * (uteis - linha["errada"]) / n) if n else 0.0
        registro_modelo = fm.MODELOS.get(linha["modelo"])
        elegivel, motivo = True, None
        if n < MIN_OBSERVACOES:
            elegivel, motivo = False, f"{n} observações; o mínimo para ler o placar é {MIN_OBSERVACOES}"
        elif casos < MIN_CASOS:
            elegivel, motivo = False, f"{casos} caso(s); o mínimo é {MIN_CASOS} — um caso longo sozinho não é padrão"
        saida.append({
            **linha, "casos": casos,
            "indice": round(indice, 1),
            "aproveitamento": round(100.0 * uteis / n, 1) if n else 0.0,
            "eco": round(100.0 * linha["duplicada"] / n, 1) if n else 0.0,
            "elegivel": elegivel, "motivoInelegivel": motivo,
            "restricoes": list(registro_modelo.restricoes) if registro_modelo else [],
            "degrau": (registro["degraus"].get(linha["modelo"]) or {}).get("degrau", "observador"),
        })
    saida.sort(key=lambda linha: (-linha["indice"], linha["modelo"]))
    return {"contrato": VERSAO, "em": _agora(), "modelos": saida,
            "minimos": {"observacoes": MIN_OBSERVACOES, "casos": MIN_CASOS},
            "vereditos": VEREDITOS}


# --------------------------------------------------------------------------
# Amostra — contar não é ler
# --------------------------------------------------------------------------

def amostra(modelo: str, *, limite: int = 8, veredito: str | None = None) -> list[dict]:
    """Abre as observações reais a partir dos painéis. Não grava nada."""
    registro = carregar()
    linhas = []
    cache: dict[str, dict] = {}
    for decisao in registro["decisoes"]:
        if decisao.get("modelo") != modelo:
            continue
        if veredito and decisao.get("veredito") != veredito:
            continue
        caminho = decisao.get("painel") or ""
        painel = cache.get(caminho)
        if painel is None:
            painel = _ler_json(Path(caminho), {}) or {}
            cache[caminho] = painel
        texto = None
        for bloco in painel.get("vozes") or []:
            for obs in bloco.get("observacoes") or []:
                if obs.get("obsId") == decisao["obsId"]:
                    texto = obs.get("texto")
        linhas.append({**decisao,
                       "texto": texto or "[painel não encontrado no disco]"})
        if len(linhas) >= limite:
            break
    return linhas


# --------------------------------------------------------------------------
# Promoção e revalidação
# --------------------------------------------------------------------------

def _evidencia(modelo: str) -> dict:
    linha = next((l for l in placar()["modelos"] if l["modelo"] == modelo), None)
    return {
        "n": linha["n"] if linha else 0,
        "casos": linha["casos"] if linha else 0,
        "indice": linha["indice"] if linha else 0.0,
        "eco": linha["eco"] if linha else 0.0,
        "bancada": _bancada(modelo),
    }


def promover(modelo: str, *, para: str, aprovado_por: str,
             observacao: str | None = None) -> dict:
    """Sobe um degrau. Decisão humana, com a evidência do momento congelada."""
    if para not in DEGRAUS:
        raise ContribuicaoError(f"degrau {para!r} não existe: {', '.join(DEGRAUS)}")
    if not aprovado_por.strip():
        raise ContribuicaoError("promoção exige --aprovado-por: a decisão é de uma pessoa")
    if modelo not in fm.MODELOS:
        raise ContribuicaoError(f"modelo fora do registro da FORJA: {modelo!r}")

    registro = carregar()
    atual = (registro["degraus"].get(modelo) or {}).get("degrau", "observador")
    if DEGRAUS.index(para) != DEGRAUS.index(atual) + 1:
        raise ContribuicaoError(
            f"{modelo} está em {atual!r}; o próximo degrau é "
            f"{DEGRAUS[min(DEGRAUS.index(atual) + 1, len(DEGRAUS) - 1)]!r}, não {para!r}")

    linha = next((l for l in placar(registro)["modelos"] if l["modelo"] == modelo), None)
    if linha is None:
        raise ContribuicaoError(f"{modelo} não tem nenhuma decisão registrada")
    if not linha["elegivel"]:
        raise ContribuicaoError(f"{modelo} inelegível: {linha['motivoInelegivel']}")
    minimo = INDICE_MINIMO.get(para, 0.0)
    if linha["indice"] < minimo:
        raise ContribuicaoError(
            f"{modelo} tem índice {linha['indice']}; {para!r} pede {minimo}")

    restricoes = fm.MODELOS[modelo].restricoes
    if para == "candidato" and "nao_afirma_fato" in restricoes:
        banca = _bancada(modelo)
        raise ContribuicaoError(
            f"{modelo} não pode ser candidato a papel real enquanto carregar "
            f"`nao_afirma_fato`: a bancada mediu {banca.get('invencoes')} invenção(ões) "
            f"em {banca.get('provas')} provas. Bom de ângulo não é o mesmo que "
            "confiável como fonte, e o placar de contribuição não revoga a bancada")
    if para == "candidato" and not _bancada(modelo)["aferida"]:
        raise ContribuicaoError(
            f"{modelo} nunca passou pela bancada de fidelidade à fonte. Rode "
            "`forja_bench_modelos.py rodar` antes: não aferido não é o mesmo que "
            "aprovado, e o placar de contribuição não mede invenção")

    registro["degraus"][modelo] = {
        "degrau": para, "de": atual, "aprovadoPor": aprovado_por.strip(),
        "em": _agora(), "observacao": observacao,
        "evidencia": _evidencia(modelo),
    }
    gravar(registro)
    return registro["degraus"][modelo]


def revalidar() -> list[dict]:
    """A evidência de cada promoção ainda existe hoje?

    Não apaga e não reescreve nada: devolve a divergência para quem promoveu
    decidir entre manter, corrigir a evidência ou rebaixar. Uma voz pode
    continuar simpática e ter perdido o lastro.
    """
    registro = carregar()
    saida = []
    for modelo, ficha in sorted(registro["degraus"].items()):
        antes = ficha.get("evidencia") or {}
        agora = _evidencia(modelo)
        divergencias = []
        if agora["n"] < antes.get("n", 0):
            divergencias.append(
                f"decisões caíram de {antes.get('n')} para {agora['n']} — o ledger encolheu")
        if agora["indice"] + 5 < antes.get("indice", 0.0):
            divergencias.append(
                f"índice caiu de {antes.get('indice')} para {agora['indice']}")
        if agora["casos"] < MIN_CASOS:
            divergencias.append(f"hoje só há {agora['casos']} caso(s) distinto(s)")
        banca = agora["bancada"]
        if ficha["degrau"] == "candidato" and banca.get("invencoes"):
            divergencias.append(
                f"a bancada acusa {banca['invencoes']} invenção(ões) — candidato não sustenta")
        saida.append({"modelo": modelo, "degrau": ficha["degrau"],
                      "aprovadoPor": ficha.get("aprovadoPor"),
                      "evidenciaNaAdocao": antes, "evidenciaHoje": agora,
                      "divergencias": divergencias})
    return saida


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def _imprimir_placar(relatorio: dict) -> None:
    if not relatorio["modelos"]:
        print("nenhuma decisão registrada ainda — rode o painel e colha os vereditos")
        return
    print(f"{'modelo':<20} {'degrau':<11} {'n':>4} {'casos':>6} {'índice':>7} "
          f"{'aprov%':>7} {'eco%':>6}  situação")
    for linha in relatorio["modelos"]:
        situacao = "elegível" if linha["elegivel"] else linha["motivoInelegivel"]
        if linha["restricoes"]:
            situacao += f" · {','.join(linha['restricoes'])}"
        print(f"{linha['modelo']:<20} {linha['degrau']:<11} {linha['n']:>4} "
              f"{linha['casos']:>6} {linha['indice']:>7.1f} "
              f"{linha['aproveitamento']:>7.1f} {linha['eco']:>6.1f}  {situacao}")
    print("\níndice = de cada 100 observações, quantas mudaram a peça, "
          "descontadas as erradas.\n`duplicada` e `rejeitada` contam no "
          "denominador e não somam — dizer o óbvio dilui.")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("colher", help="leva os vereditos preenchidos no painel ao ledger")
    c.add_argument("--painel", type=Path, required=True)
    c.add_argument("--por", required=True)

    r = sub.add_parser("registrar", help="anota um veredito e colhe")
    r.add_argument("--painel", type=Path, required=True)
    r.add_argument("--obs", required=True)
    r.add_argument("--veredito", required=True, choices=sorted(VEREDITOS))
    r.add_argument("--duplicada-de")
    r.add_argument("--motivo")
    r.add_argument("--por", required=True)

    sub.add_parser("placar", help="quanto cada voz agregou")

    a = sub.add_parser("amostra", help="abre as observações reais (não grava nada)")
    a.add_argument("modelo")
    a.add_argument("--limite", type=int, default=8)
    a.add_argument("--veredito", choices=sorted(VEREDITOS))

    p = sub.add_parser("promover", help="sobe um degrau; decisão humana")
    p.add_argument("modelo")
    p.add_argument("--para", required=True, choices=DEGRAUS)
    p.add_argument("--aprovado-por", required=True)
    p.add_argument("--observacao")

    sub.add_parser("revalidar", help="a evidência da promoção ainda existe?")
    sub.add_parser("degraus", help="o que cada degrau autoriza")

    args = ap.parse_args(argv)

    if args.cmd == "colher":
        resultado = colher(args.painel, por=args.por)
        print(f"{resultado['colhidas']} veredito(s) colhido(s); "
              f"{resultado['semVeredito']} sem veredito ainda")
        for problema in resultado["invalidas"]:
            print(f"  [inválido] {problema}")
        return 1 if resultado["invalidas"] else 0

    if args.cmd == "registrar":
        try:
            resultado = registrar_uma(args.painel, args.obs, args.veredito, por=args.por,
                                      duplicada_de=args.duplicada_de, motivo=args.motivo)
        except ContribuicaoError as erro:
            print(f"recusado: {erro}")
            return 1
        print(f"registrado; {resultado['colhidas']} veredito(s) no ledger")
        # Um veredito inválido em OUTRA linha do mesmo painel não pode sair
        # calado só porque este comando tratou de uma linha válida.
        for problema in resultado["invalidas"]:
            print(f"  [inválido, ainda no painel] {problema}")
        return 1 if resultado["invalidas"] else 0

    if args.cmd == "placar":
        _imprimir_placar(placar())
        return 0

    if args.cmd == "amostra":
        linhas = amostra(args.modelo, limite=args.limite, veredito=args.veredito)
        if not linhas:
            print("nada registrado para este modelo com esse filtro")
            return 0
        for linha in linhas:
            print(f"\n[{linha['veredito']}] {linha['caso']} · {linha['obsId']}")
            print(f"  {linha['texto']}")
            if linha.get("motivo"):
                print(f"  motivo: {linha['motivo']}")
        print(f"\n{len(linhas)} observação(ões) lida(s). Nada foi gravado.")
        return 0

    if args.cmd == "promover":
        try:
            ficha = promover(args.modelo, para=args.para,
                             aprovado_por=args.aprovado_por, observacao=args.observacao)
        except ContribuicaoError as erro:
            print(f"promoção recusada: {erro}")
            return 1
        print(f"{args.modelo}: {ficha['de']} → {ficha['degrau']} "
              f"(por {ficha['aprovadoPor']}, {ficha['em']})")
        return 0

    if args.cmd == "revalidar":
        fichas = revalidar()
        if not fichas:
            print("nenhuma promoção registrada")
            return 0
        problemas = 0
        for ficha in fichas:
            print(f"\n{ficha['modelo']} — {ficha['degrau']} (por {ficha['aprovadoPor']})")
            if not ficha["divergencias"]:
                print("  lastro mantido")
                continue
            problemas += 1
            for item in ficha["divergencias"]:
                print(f"  [divergência] {item}")
        print("\nNada foi alterado. A decisão de manter, corrigir ou rebaixar é de "
              "quem promoveu.")
        return 1 if problemas else 0

    if args.cmd == "degraus":
        for degrau in DEGRAUS:
            print(f"{degrau:<12} {DESCRICAO_DEGRAUS[degrau]}")
        print(f"\nmínimos para ler o placar: {MIN_OBSERVACOES} observações e "
              f"{MIN_CASOS} casos distintos")
        for degrau, minimo in INDICE_MINIMO.items():
            print(f"índice mínimo para {degrau}: {minimo}")
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
