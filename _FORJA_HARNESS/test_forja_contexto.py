# -*- coding: utf-8 -*-
"""test_forja_contexto.py — regressão de `facts_rechecked` e `context_complete`.

A verificação que define esta leva é a última: nos três casos reais com questão
material pendente, os três negam liberação externa. A combinação "pendência
aberta + liberação externa aprovada" não existe no acervo, e é justamente ela
que o gate passa a impedir — um gate que só reproduzisse o acervo não impediria
nada.

Uso: python test_forja_contexto.py   (exit 0 = ok; exit 1 = regressão)
"""
from __future__ import annotations

import hashlib
import io
import json
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from forja_contexto import GATE_CONTEXTO, GATE_FATOS, validar_contexto  # noqa: E402

TEXTO = "# Manifestação\n\nO fato foi reconferido na fonte oficial.\n"
HASH = hashlib.sha256(TEXTO.encode("utf-8")).hexdigest()
BASE = {"factsRechecked": True, "tribunal": "TRF4", "approvedForExternalRelease": True}


def main() -> int:
    falhas = 0
    casos = 0

    def checar(nome, obtido, esperado):
        nonlocal falhas, casos
        casos += 1
        if obtido != esperado:
            print(f"  FALHOU: {nome} — esperado {esperado}, obtido {obtido}")
            falhas += 1

    def fatos(val, gr=None, texto=None):
        return validar_contexto(val, gr, texto)["gates"][GATE_FATOS]

    def contexto(val, gr=None, texto=None):
        return validar_contexto(val, gr, texto)["gates"][GATE_CONTEXTO]

    checar("validação ausente (fatos)", fatos(None), "fail")
    checar("validação ausente (contexto)", contexto(None), "fail")
    # Ausência de declaração não é declaração falsa: o caso Natura real cai
    # aqui, e o gate diz `warn` em vez de reprovar entrega aprovada.
    checar("recheque não declarado em dialeto nenhum",
           fatos({"approved": True, "tribunal": "TRF4"}), "warn")
    # O caso Cafelana é real: o artefato admite que não reconferiu.
    checar("recheque negado pelo próprio artefato",
           fatos({"factsRechecked": False, "tribunal": "TRF1"}), "fail")
    checar("recheque declarado no dialeto de checks",
           fatos({"tribunal": "TRF4"}, {"checks": {"factsRechecked": "pass"}}), "pass")
    checar("validação que descreve outro texto",
           fatos({**BASE, "auditedMarkdownSha256": "0" * 64}, None, TEXTO), "fail")
    checar("hash do texto auditado conferindo",
           fatos({**BASE, "auditedMarkdownSha256": HASH}, None, TEXTO), "pass")

    # A combinação que o gate existe para impedir e que o acervo nunca produziu.
    checar("pendência material com liberação externa aprovada",
           contexto({"factsRechecked": True, "tribunal": "TRF4",
                     "pendingMaterialQuestions": ["falta o laudo"],
                     "approvedForExternalRelease": True}), "fail")
    checar("pendência material com liberação externa negada",
           contexto({"factsRechecked": True, "tribunal": "TRF4",
                     "pendingMaterialQuestions": ["falta o laudo"],
                     "approvedForExternalRelease": False}), "pass")
    checar("pendência sem fronteira declarada",
           contexto({"factsRechecked": True, "tribunal": "TRF4",
                     "blockedQuestions": ["prazo não certificado"]}), "warn")
    checar("sem identidade processual declarada",
           contexto({"factsRechecked": True, "approvedForExternalRelease": False}), "warn")

    # CONTRAPROVA — artefatos reais. Nenhum pode ser REPROVADO por defeito meu.
    dialetos, vereditos = {}, []
    for arquivo in Path("state").rglob("context_validation.json"):
        try:
            dados = json.loads(arquivo.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            continue
        if not isinstance(dados, dict):
            continue
        chave = tuple(sorted(dados))
        if chave in dialetos:
            continue
        dialetos[chave] = arquivo

        gate_result = {}
        vizinho = arquivo.parent / "f7_gate_result.json"
        if vizinho.is_file():
            try:
                gate_result = json.loads(vizinho.read_text(encoding="utf-8"))
            except (ValueError, OSError):
                gate_result = {}
        texto = None
        for nome in ("audited_markdown.md", "final_markdown.md"):
            alvo = arquivo.parent / nome
            if alvo.is_file():
                texto = alvo.read_text(encoding="utf-8")
                break

        laudo = validar_contexto(dados, gate_result, texto)
        casos += 1
        vereditos.append((laudo["gates"][GATE_FATOS], laudo["gates"][GATE_CONTEXTO]))
        # O único `fail` legítimo do acervo é o do caso que admite não ter
        # reconferido. Qualquer outro é regressão minha.
        if laudo["gates"][GATE_FATOS] == "fail" and dados.get("factsRechecked") is not False:
            print(f"  TRAVOU O APROVADO: {arquivo}")
            for item in laudo["findings"]:
                print(f"      {item['gate']}: {item['problema']}")
            falhas += 1
        if laudo["gates"][GATE_CONTEXTO] == "fail":
            print(f"  TRAVOU O APROVADO (contexto): {arquivo}")
            falhas += 1

    if len(dialetos) < 4:
        print(f"  FALHOU: só {len(dialetos)} validações reais examinadas — "
              "a contraprova perdeu o acervo")
        falhas += 1

    # Se o acervo inteiro saísse `pass` nos dois gates, o gate não estaria
    # medindo nada: um dos casos reais admite não ter reconferido os fatos.
    if vereditos and all(v == ("pass", "pass") for v in vereditos):
        print("  FALHOU: todo o acervo saiu `pass` nos dois gates — um caso real declara "
              "factsRechecked=false e precisa aparecer")
        falhas += 1

    if falhas:
        print(f"REGRESSÃO: {falhas} de {casos} verificações de contexto falharam")
        return 1
    print(f"ok: {casos} verificações — {len(dialetos)} validações reais; vereditos do acervo: "
          f"{', '.join(sorted({f'{a}/{b}' for a, b in vereditos}))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
