# -*- coding: utf-8 -*-
"""test_forja_artefatos.py — catraca de deriva do vocabulário dos artefatos.

O censo de 04/08/2026 encontrou 83 campos que nenhum dialeto conhece, em 92
artefatos e 41 esquemas distintos. A maioria é informação extra que gate nenhum
precisa — e por isso um relatório que apenas os liste seria ignorado na segunda
semana. Ruído ensina a ignorar o instrumento, e foi assim que a lição 124 nasceu.

O que este teste protege é o movimento, não o número absoluto:

  1. o número de campos desconhecidos NÃO PODE CRESCER. Um caso novo que
     invente `fontesConferidas` empurra o contador e derruba a suíte, forçando
     uma decisão consciente — mapear o nome ou declará-lo estrutural.
  2. todo conceito que os módulos de gate usam precisa existir no mapa
     canônico, para que a fonte única não se torne uma cópia desatualizada dos
     quatorze mapas que ela veio substituir.
  3. o acervo não pode encolher sem aviso: se o censo passar a examinar muito
     menos artefatos, a catraca ficaria verde por falta de dados.

Uso: python test_forja_artefatos.py   (exit 0 = ok; exit 1 = regressão)
"""
from __future__ import annotations

import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from forja_artefatos import DIALETOS, campo, censo, lista, nomes  # noqa: E402

# Medido em 04/08/2026. Só pode descer.
DESCONHECIDOS_MAX = 83
ARTEFATOS_MIN = 80

# Conceitos que os módulos de gate consomem. Se um deles sumir do mapa
# canônico, o gate correspondente passa a ler o vazio em silêncio.
CONCEITOS_EM_USO = [
    ("paragraph_provenance", "unidades"), ("paragraph_provenance", "lastro"),
    ("paragraph_provenance", "hash_do_texto"), ("paragraph_provenance", "amostra_do_texto"),
    ("source_ledger", "fontes"), ("source_ledger", "caminho_arquivado"),
    ("source_ledger", "hash_arquivado"), ("source_ledger", "url_oficial"),
    ("citation_checklist", "itens"), ("citation_checklist", "usou_transcricao"),
    ("document_index", "documentos"), ("document_index", "criticos_no_topo"),
    ("coverage_ledger", "declaracao"), ("coverage_ledger", "lacunas"),
    ("injection_scan", "escopo_varrido"), ("injection_scan", "triagem"),
    ("context_validation", "pendencias"), ("context_validation", "identidade"),
    ("context_validation", "recheque_de_fatos"),
    ("adversarial_recheck", "itens_rechecados"), ("adversarial_recheck", "aplicabilidade"),
]


def main() -> int:
    falhas = 0
    casos = 0

    # 1 — os acessores canônicos funcionam sobre dialetos distintos.
    for dados, esperado in (
            ({"paragraphs": [{"id": "P1"}]}, 1),
            ({"blocks": [{"blockId": "b1"}]}, 1),
            ({"unidades": [{"id": "u1"}, {"id": "u2"}]}, 2),
            ({}, 0)):
        casos += 1
        if len(lista(dados, "paragraph_provenance", "unidades")) != esperado:
            print(f"  FALHOU: acessor de unidades não leu {sorted(dados)}")
            falhas += 1

    casos += 1
    if campo({"draftSha256": "abc"}, "paragraph_provenance", "hash_do_texto") != "abc":
        print("  FALHOU: acessor não reconheceu o dialeto draftSha256")
        falhas += 1

    # Conceito inexistente erra alto em vez de devolver vazio — devolver nada
    # silenciosamente é a MC-15 embutida no próprio leitor.
    for especie, conceito in (("paragraph_provenance", "conceito_que_nao_existe"),
                              ("especie_que_nao_existe", "unidades")):
        casos += 1
        try:
            nomes(especie, conceito)
            print(f"  FALHOU: {especie}/{conceito} deveria erguer KeyError")
            falhas += 1
        except KeyError:
            pass

    # 2 — todo conceito em uso existe no mapa.
    for especie, conceito in CONCEITOS_EM_USO:
        casos += 1
        try:
            if not nomes(especie, conceito):
                print(f"  FALHOU: {especie}/{conceito} está no mapa mas sem nome algum")
                falhas += 1
        except KeyError:
            print(f"  FALHOU: conceito em uso sumiu do mapa canônico: {especie}/{conceito}")
            falhas += 1

    # 3 — a catraca de deriva.
    laudo = censo()
    total = sum(len(v) for v in laudo["camposDesconhecidos"].values())
    casos += 1
    if total > DESCONHECIDOS_MAX:
        novos = []
        for especie, campos in laudo["camposDesconhecidos"].items():
            novos.extend(f"{especie}.{nome}" for nome in campos)
        print(f"  FALHOU: campos fora do vocabulário subiram de {DESCONHECIDOS_MAX} para {total}. "
              "Um artefato novo inventou nome — mapeie-o em DIALETOS ou declare-o estrutural, "
              "mas não deixe o gate lendo o vazio em silêncio.")
        print(f"          desconhecidos atuais: {', '.join(sorted(novos)[:12])}")
        falhas += 1

    casos += 1
    if laudo["artefatosExaminados"] < ARTEFATOS_MIN:
        print(f"  FALHOU: o censo examinou {laudo['artefatosExaminados']} artefatos, abaixo do "
              f"piso de {ARTEFATOS_MIN} — a catraca ficaria verde por falta de dados")
        falhas += 1

    # 4 — o mapa cobre todas as espécies que o acervo tem em volume.
    casos += 1
    faltando = [e for e in laudo["esquemasPorEspecie"] if e not in DIALETOS]
    if faltando:
        print(f"  FALHOU: espécies no acervo sem entrada no mapa: {', '.join(faltando)}")
        falhas += 1

    if falhas:
        print(f"REGRESSÃO: {falhas} de {casos} verificações de vocabulário falharam")
        return 1
    print(f"ok: {casos} verificações — {laudo['artefatosExaminados']} artefatos, "
          f"{sum(laudo['esquemasPorEspecie'].values())} esquemas distintos, "
          f"{total} campos fora do vocabulário (teto {DESCONHECIDOS_MAX})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
