# -*- coding: utf-8 -*-
"""Regressão do gate de aceite e do recorte de frase para destaque na margem.

Os dois nasceram do mesmo caso e do mesmo dia, e por isso ficam juntos: um
confere se o artefato prometido existe, o outro impede que o destaque impresso
na margem termine no meio de uma citação legal.

As fixtures são os defeitos reais, e não casos inventados — fixture inventada
mede a imaginação de quem escreveu o gate.
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import forja_gate_aceite as ga
import forja_visual_mapa_gen as mg

falhas = 0
casos = 0


def checar(nome, condicao, detalhe=""):
    global falhas, casos
    casos += 1
    if not condicao:
        falhas += 1
        print(f"  FALHOU: {nome}" + (f" — {detalhe}" if detalhe else ""))


def registro(itens):
    return {"schemaVersion": 1, "origem": {}, "regrasDeEncerramento": [], "itens": itens}


with tempfile.TemporaryDirectory() as tmp:
    base = Path(tmp)
    (base / "real.md").write_text("x" * 2000, encoding="utf-8")
    (base / "vazio.md").write_text("nada", encoding="utf-8")
    (base / "dados.json").write_text(json.dumps({"a": 1}) + " " * 2000, encoding="utf-8")
    (base / "INTEIRO_TEOR_algo.md").write_text("y" * 2000, encoding="utf-8")

    # --- o defeito central: declarar concluído sem artefato ------------------
    r = ga.avaliar(registro([{"id": 1, "titulo": "t", "exige": ["artefato"],
                              "artefatos": [], "estado": "concluido"}]), base)
    checar("concluído sem artefato algum reprova",
           any(a["gate"] == "ACE2-sem-artefato" for a in r["findings"]))

    r = ga.avaliar(registro([{"id": 1, "titulo": "t", "exige": ["artefato"],
                              "artefatos": ["nao_existe.md"], "estado": "concluido"}]), base)
    checar("artefato prometido e inexistente reprova",
           any(a["gate"] == "ACE1-artefato-inexistente" for a in r["findings"]))

    # --- e o seu contrário: item aberto declarado não é falha de prova -------
    r = ga.avaliar(registro([{"id": 1, "titulo": "t", "exige": ["artefato"],
                              "artefatos": [], "estado": "aberto"}]), base)
    checar("item aberto declarado não gera achado de artefato",
           not any(a["gate"].startswith(("ACE1", "ACE2")) for a in r["findings"]))
    checar("mas item aberto barra a remessa, pela sexta regra",
           any(a["gate"] == "ACE7-entrega-fragmentaria" for a in r["findings"]))

    # --- arquivo existe e está vazio: pior que ausente, porque parece pronto -
    r = ga.avaliar(registro([{"id": 1, "titulo": "t", "exige": ["artefato"],
                              "artefatos": ["vazio.md"], "estado": "concluido"}]), base)
    checar("artefato existente e vazio reprova",
           any(a["gate"] == "ACE3-artefato-vazio" for a in r["findings"]))

    # --- nenhum número sem reprodução: PDF lê resultado, não reproduz --------
    r = ga.avaliar(registro([{"id": 15, "titulo": "cálculo", "exige": ["artefato", "nativo"],
                              "artefatos": ["real.md"], "estado": "concluido"}]), base)
    checar("item quantitativo sem formato nativo reprova",
           any(a["gate"] == "ACE4-sem-formato-nativo" for a in r["findings"]))
    r = ga.avaliar(registro([{"id": 15, "titulo": "cálculo", "exige": ["artefato", "nativo"],
                              "artefatos": ["dados.json"], "estado": "concluido"}]), base)
    checar("item quantitativo com JSON passa",
           not any(a["gate"] == "ACE4-sem-formato-nativo" for a in r["findings"]))

    # --- nenhum precedente sem inteiro teor ---------------------------------
    r = ga.avaliar(registro([{"id": 8, "titulo": "precedentes",
                              "exige": ["artefato", "inteiro_teor"],
                              "artefatos": ["real.md"], "estado": "concluido"}]), base)
    checar("precedente sem artefato de teor integral reprova",
           any(a["gate"] == "ACE5-sem-inteiro-teor" for a in r["findings"]))
    r = ga.avaliar(registro([{"id": 8, "titulo": "precedentes",
                              "exige": ["artefato", "inteiro_teor"],
                              "artefatos": ["INTEIRO_TEOR_algo.md"], "estado": "concluido"}]), base)
    checar("precedente com inteiro teor passa",
           not any(a["gate"] == "ACE5-sem-inteiro-teor" for a in r["findings"]))

    # --- a lista inteira fechada libera -------------------------------------
    r = ga.avaliar(registro([{"id": 1, "titulo": "t", "exige": ["artefato"],
                              "artefatos": ["real.md"], "estado": "concluido"}]), base)
    checar("lista inteira concluída com prova libera a remessa", r["liberado"],
           json.dumps(r["findings"], ensure_ascii=False)[:200])

    # --- o registro localiza por nome quando a pasta foi reorganizada -------
    (base / "sub").mkdir()
    (base / "sub" / "movido.md").write_text("z" * 2000, encoding="utf-8")
    r = ga.avaliar(registro([{"id": 1, "titulo": "t", "exige": ["artefato"],
                              "artefatos": ["movido.md"], "estado": "concluido"}]), base)
    checar("artefato movido de pasta ainda é localizado pelo nome", r["liberado"])

# --- recorte de frase para a margem -----------------------------------------
# O divisor de frases quebra no ponto de "art." e em dois-pontos. Impressa na
# margem, a metade resultante termina no meio da citação legal — foi o que saiu
# no memorial de 08/08/2026, com "…o dever de coerência do art."
TRUNCADAS = [
    "Não se invoca coisa julgada, e sim o dever de coerência do art",
    "Não se invoca coisa julgada, e sim o dever de coerência do art.",
    "Não se sustenta que ela vincule este juízo, nem que imponha idêntico resultado:",
    "A regra está no §",
    "Consta dos autos, conforme fls",
]
INTEIRAS = [
    "Vício intrínseco à decisão é, por definição, matéria de embargos de declaração.",
    "Três precedentes foram invocados e nenhum foi examinado.",
    "Qualquer das duas respostas altera o conteúdo da decisão, porque hoje não existe resposta alguma.",
    "O relatório registra 2.210 operações de exportação",
]
for f in TRUNCADAS:
    checar(f"frase truncada é recusada: {f[:40]}", bool(mg._TERMINA_MAL.search(f)))
for f in INTEIRAS:
    checar(f"frase inteira é aceita: {f[:40]}", not mg._TERMINA_MAL.search(f))

if falhas:
    print(f"REGRESSÃO: {falhas} de {casos} casos falharam")
    raise SystemExit(1)
print(f"ok: {casos} casos — o gate de aceite exige prova de quem afirma ter concluído, "
      f"e o destaque de margem não sai cortado no meio de citação legal")
