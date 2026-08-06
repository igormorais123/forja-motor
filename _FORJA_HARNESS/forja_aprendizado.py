# -*- coding: utf-8 -*-
"""forja_aprendizado.py — transforma correção humana em mudança no sistema.

O que já existia e o que faltava. O loop pós-protocolo captura a peça que o
titular efetivamente protocolou, compara com a nossa e classifica cada mudança
por camada, causa e impacto. Ele funciona: medido em 06/08/2026, seis casos
reais produziram **1.096 candidatos a lição**. Destes, **1.095 estavam em
`observed` e exatamente um havia sido promovido** — 0,09%.

A causa não foi desleixo. Promover um candidato exigia seis argumentos na linha
de comando, entre eles um `--fixture-id` e um `--test-id` que alguém precisava
criar à mão, e um SHA-256 de 64 caracteres copiado a dedo. Com mil candidatos
isso é a lição 87 outra vez: recurso que depende de esforço manual por caso não
sobrevive ao volume. A porta de saída foi construída estreita demais.

**A virada deste módulo: promove-se o padrão, não a ocorrência.** Uma correção
isolada num caso é anedota; a mesma classe de correção aparecendo em casos
diferentes é padrão do escritório, e é isso que vale virar regra. Os 1.096
candidatos colapsam em poucas dezenas de classes `(camada, causa)`, e a
recorrência entre casos distintos é o critério de prioridade — não a contagem
bruta, que um único caso longo infla sozinho.

O que este módulo NÃO faz, por decisão. Ele não lê o texto da peça. Todo o
pipeline pós-protocolo é sanitizado por hash — guarda `beforeHash`, `afterHash`
e localizador, nunca o trecho —, e o texto vive apenas no cofre local, fora de
qualquer repositório. Manter essa disciplina custa não poder gerar fixture
textual automaticamente; quebrá-la colocaria peça protocolada dentro do acervo
versionado. O custo é aceito.

Verbos:
    padroes    agrega os candidatos de todos os casos e mostra o que se repete
    adotar     promove uma classe a regra ativa, com destino declarado
    aplicar    escreve a regra no destino e registra o que mudou
    conferir   verifica que toda regra ativa está presente no seu destino

Uso:
    python forja_aprendizado.py padroes
    python forja_aprendizado.py padroes --minimo-casos 2
    python forja_aprendizado.py adotar reasoning:reasoning --destino checklist \\
        --fase F7 --regra "texto da regra" --aprovado-por igor
    python forja_aprendizado.py aplicar
    python forja_aprendizado.py conferir
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
STATE = RAIZ / "state"
REGISTRO = RAIZ / "learning_registry" / "REGRAS_APRENDIDAS.json"
CONTRATOS = RAIZ / "phase_contracts"
TEMPLATES = RAIZ / "templates"

# Destinos possíveis de uma regra aprendida. Cada um tem custo e efeito
# diferentes, e a escolha é do humano que adota — não do algoritmo.
#
#   checklist  vira item de conferência no contrato da fase. Barato, e o efeito
#              aparece na próxima peça, porque a fase lê o contrato.
#   template   vira instrução no template que o redator recebe. Muda o texto
#              gerado, não a conferência dele.
#   doutrina   vira lição no protocolo da casa. Para o que é julgamento humano
#              e não se reduz a item conferível.
#
# `fixture` não está aqui de propósito: o pipeline é sanitizado por hash e o
# texto da peça não sai do cofre local, então uma fixture textual não pode ser
# gerada por este módulo. Quando uma regra pedir teste, ele é escrito à mão e
# referenciado — o que é raro e caro, e deve continuar sendo.
DESTINOS = {
    "checklist": "item de conferência no contrato da fase",
    "template": "instrução no template que o redator recebe",
    "doutrina": "lição no protocolo da casa",
}

MARCA_INICIO = "<!-- APRENDIDO-DO-RETORNO-HUMANO: início (gerado por forja_aprendizado.py) -->"
MARCA_FIM = "<!-- APRENDIDO-DO-RETORNO-HUMANO: fim -->"


def _agora() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def _ler_json(caminho: Path, padrao=None):
    try:
        return json.loads(caminho.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return padrao


def _escrever_json(caminho: Path, dados) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(json.dumps(dados, ensure_ascii=False, indent=2) + "\n",
                       encoding="utf-8", newline="")


# --------------------------------------------------------------------------
# Leitura dos candidatos
# --------------------------------------------------------------------------
def levantar_candidatos() -> list[dict]:
    """Todos os candidatos de todos os casos, com o caso de origem junto."""
    saida: list[dict] = []
    if not STATE.is_dir():
        return saida
    for arq in STATE.rglob("F10_LEARNING_CANDIDATE.json"):
        dados = _ler_json(arq)
        if not isinstance(dados, dict):
            continue
        caso = dados.get("caseId") or arq.parent.parent.name
        for c in dados.get("candidates") or []:
            if isinstance(c, dict):
                saida.append({**c, "_caso": caso})
    return saida


def agrupar(candidatos: list[dict]) -> list[dict]:
    """Agrupa por (camada, causa) e mede recorrência ENTRE casos.

    A contagem bruta engana: um caso longo sozinho produz centenas de mudanças e
    dominaria o ranking sem revelar padrão nenhum. O que distingue padrão do
    escritório de particularidade de um processo é aparecer em casos DIFERENTES,
    e por isso a ordenação é por número de casos primeiro.
    """
    grupos: dict[tuple[str, str], dict] = defaultdict(
        lambda: {"casos": set(), "total": 0, "materiais": 0, "confianca": []})
    for c in candidatos:
        chave = (str(c.get("layer") or "unknown"), str(c.get("cause") or "other"))
        g = grupos[chave]
        g["casos"].add(c.get("_caso"))
        g["total"] += 1
        if c.get("impact") == "material":
            g["materiais"] += 1
        try:
            g["confianca"].append(float(c.get("confidence") or 0))
        except (TypeError, ValueError):
            pass

    saida = []
    for (camada, causa), g in grupos.items():
        conf = g["confianca"]
        saida.append({
            "classe": f"{camada}:{causa}",
            "camada": camada,
            "causa": causa,
            "casos": len(g["casos"]),
            "ocorrencias": g["total"],
            "materiais": g["materiais"],
            "confiancaMedia": round(sum(conf) / len(conf), 2) if conf else None,
        })
    saida.sort(key=lambda x: (-x["casos"], -x["materiais"], -x["ocorrencias"]))
    return saida


# --------------------------------------------------------------------------
# Registro de regras
# --------------------------------------------------------------------------
def carregar_registro() -> dict:
    return _ler_json(REGISTRO, None) or {
        "schema": "FORJA-APRENDIZADO-v1",
        "porque": ("Regras aprendidas do retorno humano sobre peças protocoladas. "
                   "Cada uma nasceu de uma classe de correção que se repetiu, foi "
                   "adotada por decisão humana e é aplicada num destino verificável. "
                   "Nenhum trecho de peça entra aqui."),
        "regras": [],
    }


def adotar(classe: str, *, destino: str, fase: str, regra: str,
           aprovado_por: str, grupos: list[dict]) -> dict:
    """Registra a decisão de transformar uma classe de correção em regra."""
    if destino not in DESTINOS:
        raise SystemExit(f"destino inválido: {destino}. Use um de {sorted(DESTINOS)}")
    grupo = next((g for g in grupos if g["classe"] == classe), None)
    if grupo is None:
        raise SystemExit(f"classe não observada nos candidatos: {classe}")
    if not regra.strip():
        raise SystemExit("a regra não pode ser vazia")

    reg = carregar_registro()
    ident = "regra-" + hashlib.sha256(
        f"{classe}|{destino}|{fase}|{regra}".encode("utf-8")).hexdigest()[:12]
    if any(r["regraId"] == ident for r in reg["regras"]):
        raise SystemExit(f"regra idêntica já registrada: {ident}")

    nova = {
        "regraId": ident,
        "classe": classe,
        "destino": destino,
        "fase": fase,
        "texto": regra.strip(),
        "aprovadoPor": aprovado_por,
        "adotadaEm": _agora(),
        # A evidência é a recorrência medida no momento da adoção. Guardá-la
        # permite responder depois "por que esta regra existe?" sem reabrir os
        # casos — e mostra se ela nasceu de padrão ou de episódio isolado.
        "evidencia": {k: grupo[k] for k in
                      ("casos", "ocorrencias", "materiais", "confiancaMedia")},
        "aplicadaEm": None,
        "destinoArquivo": None,
    }
    reg["regras"].append(nova)
    _escrever_json(REGISTRO, reg)
    return nova


# --------------------------------------------------------------------------
# Aplicação: a regra vira texto no destino
# --------------------------------------------------------------------------
def _arquivo_de_destino(regra: dict) -> Path:
    fase = regra["fase"]
    if regra["destino"] == "checklist":
        return CONTRATOS / f"{fase}.json"
    if regra["destino"] == "template":
        candidatos = sorted(TEMPLATES.glob(f"{fase}*.md"))
        if not candidatos:
            raise SystemExit(f"nenhum template para a fase {fase} em {TEMPLATES}")
        return candidatos[0]
    return RAIZ.parent / "APRENDIZADOS_FEEDBACK_HUMANO.md"


def _aplicar_em_markdown(caminho: Path, regras: list[dict]) -> bool:
    """Reescreve o bloco marcado do arquivo. Devolve True se mudou algo.

    O bloco é delimitado por marcas HTML para que a aplicação seja idempotente:
    rodar duas vezes produz o mesmo arquivo, e o que estiver fora do bloco nunca
    é tocado. Sem isso, cada execução acrescentaria as regras de novo e o
    documento cresceria até ninguém mais lê-lo.
    """
    linhas = [MARCA_INICIO,
              "",
              "> Regras que vieram do retorno humano sobre peças protocoladas.",
              "> Escritas por `forja_aprendizado.py aplicar` — não edite à mão:",
              "> este bloco é reescrito. Para mudar uma regra, altere o registro",
              "> em `_FORJA_HARNESS/learning_registry/REGRAS_APRENDIDAS.json`.",
              ""]
    for r in regras:
        ev = r["evidencia"]
        linhas.append(f"- **{r['texto']}**")
        linhas.append(f"  <br>_{r['regraId']} — classe `{r['classe']}`, observada em "
                      f"{ev['casos']} caso(s), {ev['materiais']} mudança(s) material(is)._")
    linhas += ["", MARCA_FIM]
    bloco = "\n".join(linhas)

    texto = caminho.read_text(encoding="utf-8", newline="") if caminho.is_file() else ""
    if MARCA_INICIO in texto and MARCA_FIM in texto:
        novo = re.sub(re.escape(MARCA_INICIO) + r".*?" + re.escape(MARCA_FIM),
                      bloco.replace("\\", "\\\\"), texto, flags=re.S)
    else:
        novo = (texto.rstrip("\n") + "\n\n" + bloco + "\n") if texto else bloco + "\n"
    if novo == texto:
        return False
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(novo, encoding="utf-8", newline="")
    return True


def _aplicar_em_contrato(caminho: Path, regras: list[dict]) -> bool:
    """Acrescenta os itens ao contrato da fase, sob chave própria."""
    dados = _ler_json(caminho, None)
    if not isinstance(dados, dict):
        raise SystemExit(f"contrato de fase ilegível: {caminho}")
    itens = [{"regraId": r["regraId"], "classe": r["classe"], "texto": r["texto"],
              "origem": "retorno_humano_pos_protocolo"} for r in regras]
    if dados.get("checklistAprendido") == itens:
        return False
    dados["checklistAprendido"] = itens
    _escrever_json(caminho, dados)
    return True


def aplicar(seco: bool = False) -> list[tuple[str, Path, bool]]:
    """Escreve cada regra adotada no seu destino. Idempotente."""
    reg = carregar_registro()
    if not reg["regras"]:
        return []
    por_arquivo: dict[Path, list[dict]] = defaultdict(list)
    for r in reg["regras"]:
        por_arquivo[_arquivo_de_destino(r)].append(r)

    resultado = []
    for caminho, regras in sorted(por_arquivo.items(), key=lambda x: str(x[0])):
        if seco:
            resultado.append((regras[0]["destino"], caminho, True))
            continue
        if caminho.suffix == ".json":
            mudou = _aplicar_em_contrato(caminho, regras)
        else:
            mudou = _aplicar_em_markdown(caminho, regras)
        agora = _agora()
        for r in regras:
            r["aplicadaEm"] = agora
            r["destinoArquivo"] = caminho.relative_to(RAIZ.parent).as_posix()
        resultado.append((regras[0]["destino"], caminho, mudou))
    if not seco:
        _escrever_json(REGISTRO, reg)
    return resultado


def conferir() -> list[str]:
    """Toda regra adotada está de fato presente no seu destino?

    Esta é a diferença entre registrar uma lição e aplicá-la. Sem esta
    conferência, uma regra pode ser adotada, o arquivo de destino ser reescrito
    por outra mão, e o registro seguir dizendo que a casa aprendeu — que é
    exatamente o modo de falha que este módulo existe para fechar.
    """
    problemas = []
    for r in carregar_registro()["regras"]:
        if not r.get("aplicadaEm"):
            problemas.append(f"{r['regraId']}: adotada e nunca aplicada")
            continue
        caminho = _arquivo_de_destino(r)
        if not caminho.is_file():
            problemas.append(f"{r['regraId']}: destino ausente — {caminho}")
            continue
        conteudo = caminho.read_text(encoding="utf-8", errors="ignore")
        if r["texto"] not in conteudo and r["regraId"] not in conteudo:
            problemas.append(f"{r['regraId']}: ausente do destino — {caminho.name}")
    return problemas


# --------------------------------------------------------------------------
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="verbo", required=True)

    p = sub.add_parser("padroes", help="o que se repete no retorno humano")
    p.add_argument("--minimo-casos", type=int, default=1,
                   help="só classes observadas em pelo menos N casos distintos")
    p.add_argument("--json", action="store_true")

    a = sub.add_parser("adotar", help="promove uma classe a regra ativa")
    a.add_argument("classe", help="no formato camada:causa, como aparece em `padroes`")
    a.add_argument("--destino", required=True, choices=sorted(DESTINOS))
    a.add_argument("--fase", required=True, help="F0..F10")
    a.add_argument("--regra", required=True, help="a regra, em uma frase imperativa")
    a.add_argument("--aprovado-por", required=True)

    ap_ = sub.add_parser("aplicar", help="escreve as regras nos destinos")
    ap_.add_argument("--seco", action="store_true")

    sub.add_parser("conferir", help="as regras estão presentes nos destinos?")

    args = ap.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    if args.verbo == "padroes":
        grupos = [g for g in agrupar(levantar_candidatos())
                  if g["casos"] >= args.minimo_casos]
        if args.json:
            print(json.dumps(grupos, ensure_ascii=False, indent=2))
            return 0
        if not grupos:
            print("nenhuma classe de correção observada.")
            return 0
        print(f"{'casos':>5} {'mater.':>6} {'ocorr.':>6}  classe")
        print("-" * 62)
        for g in grupos:
            print(f"{g['casos']:>5} {g['materiais']:>6} {g['ocorrencias']:>6}  {g['classe']}")
        print("\nOrdenado por número de CASOS distintos: é a recorrência entre casos,")
        print("e não a contagem bruta, que distingue padrão do escritório de")
        print("particularidade de um processo longo.")
        return 0

    if args.verbo == "adotar":
        nova = adotar(args.classe, destino=args.destino, fase=args.fase,
                      regra=args.regra, aprovado_por=args.aprovado_por,
                      grupos=agrupar(levantar_candidatos()))
        ev = nova["evidencia"]
        print(f"adotada {nova['regraId']} — {nova['classe']} → {nova['destino']}/{nova['fase']}")
        print(f"  evidência: {ev['casos']} caso(s), {ev['materiais']} material(is)")
        print("  aplique com: python forja_aprendizado.py aplicar")
        return 0

    if args.verbo == "aplicar":
        res = aplicar(seco=args.seco)
        if not res:
            print("nenhuma regra adotada ainda.")
            return 0
        for destino, caminho, mudou in res:
            marca = "[seco]" if args.seco else ("alterado" if mudou else "já estava")
            print(f"  {destino:9} {marca:10} {caminho.name}")
        return 0

    problemas = conferir()
    if problemas:
        for p_ in problemas:
            print(f"  {p_}")
        print(f"REPROVADO — {len(problemas)} regra(s) fora do destino.")
        return 1
    print("APROVADO — toda regra adotada está presente no seu destino.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
