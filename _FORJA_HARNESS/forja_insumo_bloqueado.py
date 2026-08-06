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

Uso:
    python forja_insumo_bloqueado.py <case-dir>          # confere e reprova
    python forja_insumo_bloqueado.py <case-dir> --schema # imprime o modelo
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

VERSAO = "FORJA-INSUMO-BLOQUEADO-v1"
ARQUIVO = "F1_INSUMO_BLOQUEADO.json"

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
            "causa": f"enum ({', '.join(sorted(CAUSAS))})",
            "diligencias": [{
                "onde": "portal, base ou pessoa consultada",
                "quando": "AAAA-MM-DD",
                "resultado": "o que aconteceu, em uma frase",
            }],
            "consequencia": "o que da peça fica sem lastro por causa disto",
            "rotaDeSolucao": "quem pode destravar e como",
        }],
    }


def carregar(case_dir: Path | str):
    alvo = caminho(case_dir)
    if not alvo.is_file():
        return None
    try:
        dados = json.loads(alvo.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return dados if isinstance(dados, dict) else None


def validar(case_dir: Path | str) -> list[str]:
    """Problemas encontrados. Lista vazia significa aprovado.

    Caso sem o artefato é APROVADO, e não reprovado: a maioria dos casos não
    tem insumo bloqueado, e exigir o arquivo de todos transformaria um gate
    sobre qualidade de diagnóstico num obstáculo burocrático. O gate morde
    quando alguém declara bloqueio — e aí exige que o bloqueio seja diagnóstico.
    """
    dados = carregar(case_dir)
    if dados is None:
        return []
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
    return problemas


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if "--schema" in argv:
        print(json.dumps(modelo(), ensure_ascii=False, indent=2))
        return 0
    if not argv:
        print("uso: python forja_insumo_bloqueado.py <case-dir> [--schema]")
        return 2
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
