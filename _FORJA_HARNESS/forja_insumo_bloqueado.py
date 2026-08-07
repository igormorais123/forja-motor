# -*- coding: utf-8 -*-
"""forja_insumo_bloqueado.py — "não localizado" não é diagnóstico.

Este módulo existe por causa da correção mais recorrente que o titular já fez
à esteira. Em 04/08/2026 ele escreveu, quase palavra por palavra, a MESMA
cobrança em **quatro matérias distintas**, no mesmo dia:

    "Em relação a sua informação de que [os documentos] não estavam
     acessíveis, peço que esclareça objetivamente a natureza do impedimento
     encontrado. Precisamos distinguir, com precisão, quatro situações
     diferentes: 1. falta de acesso ao processo judicial ou ausência de
     habilitação nos autos; 2. restrição de permissão, link defeituoso ou
     dificuldade para abrir ou baixar o arquivo; 3. indisponibilidade efetiva
     do documento nas fontes consultadas; ou 4. limitação operacional da IA ou
     das ferramentas que você utiliza.
     [...] Antes de considerar um documento 'não localizado', peço que sejam
     esgotadas e registradas as diligências possíveis."

Nenhuma dessas quatro causas tem a mesma consequência. A primeira se resolve
com habilitação nos autos; a segunda, com um link novo, em minutos; a terceira
é fato do mundo; a quarta é limitação nossa e precisa ser dita com essas
letras. Colapsar as quatro em "não localizado" transfere ao titular o trabalho
de descobrir qual delas era — e foi isso que ele teve de fazer quatro vezes.

O vocabulário fechado aqui é o dele, e não uma taxonomia inventada. A exigência
de registrar as diligências também: sem elas, "indisponível na fonte" é
indistinguível de "não procurei".

Em 07/08/2026 o módulo ganhou uma segunda camada, por ordem do titular, depois de
dois bloqueios falsos declarados em dois dias. A causa em vocabulário fechado
resolvia o problema de comunicar o impedimento, e não o de **verificá-lo**: nada
exigia que as rotas conhecidas tivessem sido tentadas, e nada fazia um bloqueio
declarado voltar à fila. A partir daqui cada item se ancora num par fonte × tipo
de documento e conversa com ``forja_rotas_fonte``, que guarda o que cada tribunal
serve e o que ele não serve. Enquanto sobrar rota conhecida sem tentativa, o
bloqueio não está diagnosticado; e todo item nasce com data de revalidação,
porque bloqueio sem prazo some da fila e ninguém reaudita o que já tem causa.

Uso:
    python forja_insumo_bloqueado.py <case-dir>           # confere e reprova
    python forja_insumo_bloqueado.py <case-dir> --schema  # imprime o modelo
    python forja_insumo_bloqueado.py <raiz> --vencidos    # bloqueios a reauditar
"""
from __future__ import annotations

import json
import sys
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import forja_rotas_fonte as rotas_fonte  # noqa: E402

VERSAO = "FORJA-INSUMO-BLOQUEADO-v2"
ARQUIVO = "F1_INSUMO_BLOQUEADO.json"

# Bloqueio que não expira desaparece da fila: ninguém reaudita o que já tem
# causa registrada. Foi assim que uma decisão de acesso aberto ficou três
# semanas fora do campo de visão do caso.
REVALIDACAO_MAXIMA_DIAS = 45

# As quatro situações que o titular pediu para distinguir, e mais nada. Uma
# quinta categoria genérica reabriria a porta que este módulo fecha.
CAUSAS = {
    "sem_habilitacao_nos_autos":
        "falta de acesso ao processo ou ausência de habilitação — resolve-se com procuração/habilitação",
    "restricao_de_permissao_ou_link":
        "permissão restrita, link defeituoso ou falha ao abrir/baixar — resolve-se reenviando o arquivo",
    "indisponivel_na_fonte":
        "o documento não existe nas fontes consultadas — fato do mundo, exige diligência de terceiro",
    "limitacao_da_ferramenta":
        "limitação operacional nossa ou da ferramenta — precisa ser dito com essas letras",
}

# Frases que descrevem o sintoma e não a causa. Aceitá-las como diagnóstico é
# exatamente o que o titular recusou.
NAO_SAO_CAUSA = (
    "não localizado", "nao localizado", "não encontrado", "nao encontrado",
    "inacessível", "inacessivel", "indisponível", "indisponivel",
    "não foi possível", "nao foi possivel", "faltante", "ausente",
)


def caminho(case_dir: Path | str) -> Path:
    return Path(case_dir) / "n4_artifacts" / ARQUIVO


def modelo() -> dict:
    return {
        "schema": VERSAO,
        "porque": ("Insumo que a esteira não conseguiu ler. Cada item declara a CAUSA "
                   "em vocabulário fechado, as diligências efetivamente tentadas, o que "
                   "fica sem lastro na peça e quem pode destravar. 'Não localizado' "
                   "é sintoma, não diagnóstico."),
        "caseId": "<preenchido pelo harness>",
        # A outra metade da pergunta do titular, feita numa quinta matéria:
        # "todo o material foi encaminhado a você — a documentação não foi
        # aberta? A IA poderia diagnosticar, por checklist exaustivo, qual foi
        # a documentação recebida e conferida detalhadamente?". Dizer o que
        # faltou sem dizer o que foi lido não responde nada: o que dá sentido a
        # um bloqueio é o inventário do que entrou.
        "recebidos": [{
            "documento": "o que chegou",
            "conferido": "true|false — foi efetivamente aberto e lido",
            "observacao": "opcional: páginas, evento, o que dele foi aproveitado",
        }],
        "itens": [{
            "documento": "identificação objetiva do que falta (peça, evento, anexo)",
            # O par abaixo é o que liga o bloqueio ao registro de rotas. Sem ele
            # não há como saber se sobrou porta conhecida por tentar, e o gate
            # volta a ser uma checagem de redação.
            "fonte": "STF, STJ, DJEN, TRF4, cliente, e-mail... quem deveria entregar",
            "tipoDocumento": ("acordao, decisao, peticao_de_parte, comunicacao, "
                              "andamentos, planilha, audio..."),
            "rotasTentadas": ["chaves de forja_rotas_fonte já exercitadas"],
            "causa": f"enum ({', '.join(sorted(CAUSAS))})",
            "diligencias": [{
                "onde": "portal, base ou pessoa consultada",
                "quando": "AAAA-MM-DD",
                "resultado": "o que aconteceu, em uma frase",
            }],
            "consequencia": "o que da peça fica sem lastro por causa disto",
            "rotaDeSolucao": "quem pode destravar e como",
            "revalidarApos": ("AAAA-MM-DD — quando este bloqueio volta à fila. "
                              f"No máximo {REVALIDACAO_MAXIMA_DIAS} dias à frente"),
        }],
    }


def _data(valor):
    try:
        return datetime.strptime(str(valor), "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return None


def carregar(case_dir: Path | str):
    alvo = caminho(case_dir)
    if not alvo.is_file():
        return None
    try:
        dados = json.loads(alvo.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return dados if isinstance(dados, dict) else None


def validar(case_dir: Path | str, hoje=None) -> list[str]:
    """Problemas encontrados. Lista vazia significa aprovado.

    Caso sem o artefato é APROVADO, e não reprovado: a maioria dos casos não
    tem insumo bloqueado, e exigir o arquivo de todos transformaria um gate
    sobre qualidade de diagnóstico num obstáculo burocrático. O gate morde
    quando alguém declara bloqueio — e aí exige que o bloqueio seja diagnóstico.
    """
    dados = carregar(case_dir)
    if dados is None:
        return []
    hoje = hoje or date.today()
    problemas = []
    itens = dados.get("itens")
    if not isinstance(itens, list):
        return [f"{ARQUIVO}: campo 'itens' ausente ou fora de formato"]

    # Um bloqueio só ganha sentido contra o inventário do que foi lido. Sem
    # ele, "faltou tal peça" não distingue material que não chegou de material
    # que chegou e não foi aberto — que é exatamente a dúvida que o titular
    # levantou numa das cinco matérias.
    if itens:
        recebidos = dados.get("recebidos")
        if not isinstance(recebidos, list) or not recebidos:
            problemas.append(
                "há bloqueio declarado e nenhum inventário em 'recebidos': falta dizer "
                "o que chegou e foi conferido, e sem isso não se distingue documento "
                "que não veio de documento que veio e não foi aberto")
        else:
            for k, r in enumerate(recebidos, 1):
                if not isinstance(r, dict) or not str(r.get("documento") or "").strip():
                    problemas.append(f"recebido {k}: sem identificação do documento")
                elif r.get("conferido") is None:
                    problemas.append(
                        f"recebido {k}: falta dizer se foi efetivamente aberto e lido")
    for i, item in enumerate(itens, 1):
        if not isinstance(item, dict):
            problemas.append(f"item {i}: não é um objeto")
            continue
        doc = str(item.get("documento") or "").strip()
        rotulo = f"item {i}" + (f" ({doc[:40]})" if doc else "")
        if not doc:
            problemas.append(f"{rotulo}: sem identificação do documento")

        causa = str(item.get("causa") or "").strip()
        if causa not in CAUSAS:
            baixa = causa.casefold()
            if any(s in baixa for s in NAO_SAO_CAUSA):
                problemas.append(
                    f"{rotulo}: '{causa}' descreve o sintoma, não a causa. "
                    f"Use uma de {sorted(CAUSAS)}")
            else:
                problemas.append(
                    f"{rotulo}: causa '{causa}' fora do vocabulário {sorted(CAUSAS)}")

        diligencias = item.get("diligencias")
        if not isinstance(diligencias, list) or not diligencias:
            problemas.append(
                f"{rotulo}: nenhuma diligência registrada. Sem elas, "
                f"'indisponível na fonte' é indistinguível de 'não procurei'")
        else:
            for j, d in enumerate(diligencias, 1):
                if not isinstance(d, dict):
                    problemas.append(f"{rotulo}, diligência {j}: não é um objeto")
                    continue
                faltam = [c for c in ("onde", "quando", "resultado")
                          if not str(d.get(c) or "").strip()]
                if faltam:
                    problemas.append(
                        f"{rotulo}, diligência {j}: falta {', '.join(faltam)}")

        for campo, explicacao in (
            ("consequencia", "o que da peça fica sem lastro"),
            ("rotaDeSolucao", "quem pode destravar e como"),
        ):
            if not str(item.get(campo) or "").strip():
                problemas.append(f"{rotulo}: '{campo}' vazio — falta dizer {explicacao}")

        problemas.extend(_conferir_rotas(item, rotulo, causa))
        problemas.extend(_conferir_revalidacao(item, rotulo, hoje))
    return problemas


def _conferir_rotas(item: dict, rotulo: str, causa: str) -> list[str]:
    """As duas perguntas que os bloqueios falsos de 06 e 07/08/2026 não responderam.

    A primeira é se ainda existe porta conhecida por tentar. A segunda é se a
    causa declarada corresponde ao que a fonte de fato faz: quando o portal não
    entrega aquele tipo de documento a ninguém, o impedimento não é nosso, e
    chamá-lo de limitação da ferramenta manda o próximo agente procurar defeito
    onde não há.
    """
    fonte = str(item.get("fonte") or "").strip()
    tipo = str(item.get("tipoDocumento") or "").strip()
    if not fonte or not tipo:
        return [f"{rotulo}: falta 'fonte' e/ou 'tipoDocumento' — sem esse par não se "
                f"confere quais rotas conhecidas já foram tentadas"]

    problemas = []
    tentadas = item.get("rotasTentadas")
    if tentadas is not None and not isinstance(tentadas, list):
        problemas.append(f"{rotulo}: 'rotasTentadas' deve ser lista")
        tentadas = []

    desconhecidas = [str(r) for r in (tentadas or []) if str(r) not in rotas_fonte.ROTAS]
    if desconhecidas:
        problemas.append(
            f"{rotulo}: rota(s) {desconhecidas} não existem em forja_rotas_fonte — "
            f"registre a rota lá antes de citá-la aqui, senão a tentativa não é conferível")

    faltam = rotas_fonte.nao_tentadas(fonte, tipo, tentadas)
    if faltam:
        problemas.append(
            f"{rotulo}: há rota conhecida que serve este par e não foi tentada: "
            f"{', '.join(faltam)}. Enquanto sobrar porta por abrir, o bloqueio não "
            f"está diagnosticado")

    negativa = rotas_fonte.nao_servida(fonte, tipo)
    if negativa and causa in CAUSAS:
        admissiveis = tuple(negativa.get("causasAdmissiveis")
                            or (negativa.get("causaCorreta"),))
        if causa not in admissiveis:
            problemas.append(
                f"{rotulo}: a fonte não entrega '{tipo}' a ninguém ({negativa['porQue']}). "
                f"Com isso a causa admissível é {' ou '.join(admissiveis)}, e não "
                f"'{causa}'. {negativa['condicao']}")
    return problemas


def _conferir_revalidacao(item: dict, rotulo: str, hoje) -> list[str]:
    """Bloqueio sem prazo sai da fila e não volta.

    O prazo não promete que o impedimento caia; obriga alguém a olhar de novo.
    Foi a ausência disso que deixou uma decisão de acesso aberto três semanas
    fora do campo de visão de um caso que dependia dela.
    """
    bruto = item.get("revalidarApos")
    quando = _data(bruto)
    if quando is None:
        return [f"{rotulo}: falta 'revalidarApos' (AAAA-MM-DD). Bloqueio sem data de "
                f"revalidação sai da fila e ninguém o reaudita"]
    if quando < hoje:
        return [f"{rotulo}: 'revalidarApos' {quando.isoformat()} já venceu — "
                f"reaudite o impedimento ou empurre a data com uma diligência nova"]
    if (quando - hoje).days > REVALIDACAO_MAXIMA_DIAS:
        return [f"{rotulo}: 'revalidarApos' {quando.isoformat()} está a mais de "
                f"{REVALIDACAO_MAXIMA_DIAS} dias — prazo longo demais equivale a "
                f"não revalidar"]
    return []


def vencidos(raiz: Path | str, hoje=None) -> list[dict]:
    """Todos os bloqueios cuja revalidação venceu, em qualquer caso sob a raiz.

    É o comando que devolve à fila aquilo que o bloqueio havia removido dela.
    """
    hoje = hoje or date.today()
    achados = []
    for alvo in sorted(Path(raiz).rglob(ARQUIVO)):
        case_dir = alvo.parent.parent
        dados = carregar(case_dir) or {}
        for item in dados.get("itens") or []:
            if not isinstance(item, dict):
                continue
            quando = _data(item.get("revalidarApos"))
            if quando is None or quando < hoje:
                achados.append({
                    "caso": case_dir.name,
                    "documento": str(item.get("documento") or "")[:80],
                    "causa": item.get("causa"),
                    "revalidarApos": item.get("revalidarApos"),
                    "situacao": "sem data" if quando is None else "vencido",
                })
    return achados


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if "--schema" in argv:
        print(json.dumps(modelo(), ensure_ascii=False, indent=2))
        return 0
    if not argv:
        print("uso: python forja_insumo_bloqueado.py <case-dir> [--schema|--vencidos]")
        return 2
    if "--vencidos" in argv:
        raiz = next((a for a in argv if not a.startswith("--")), ".")
        achados = vencidos(raiz)
        if not achados:
            print("Nenhum bloqueio vencido. Todos têm revalidação em dia.")
            return 0
        for a in achados:
            print(f"  [{a['situacao']}] {a['caso']}: {a['documento']} "
                  f"(causa={a['causa']}, revalidarApos={a['revalidarApos']})")
        print(f"\n{len(achados)} bloqueio(s) a reauditar. Bloqueio vencido volta à fila: "
              f"foi por não voltar que um documento de acesso aberto ficou semanas parado.")
        return 1
    problemas = validar(argv[0])
    if not problemas:
        dados = carregar(argv[0])
        n = len(dados.get("itens") or []) if dados else 0
        print(f"APROVADO — {n} insumo(s) bloqueado(s) com causa e diligências declaradas."
              if n else "APROVADO — nenhum insumo bloqueado declarado neste caso.")
        return 0
    for p in problemas:
        print(f"  {p}")
    print(f"REPROVADO — {len(problemas)} problema(s). "
          f"'Não localizado' não é diagnóstico: quatro causas distintas têm "
          f"quatro soluções distintas.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
