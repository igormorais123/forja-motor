# -*- coding: utf-8 -*-
"""test_forja_fontes_oficiais.py — regressão de `official_sources_archived` e
`quotes_compared`.

A contraprova aqui é diferente das levas anteriores, e o motivo precisa ficar
escrito: os seis `source_ledger` reais NÃO podem todos sair `pass`. Dois casos
do acervo não arquivam nenhuma fonte, e o gate que os aprovasse estaria
repetindo a mentira que ele existe para pegar. A regra da contraprova passa a
ser mais fraca e mais honesta — **nenhum artefato real pode ser reprovado (P0)**
—, e os `warn` são o achado, não um defeito de calibração.

Uso: python test_forja_fontes_oficiais.py   (exit 0 = ok; exit 1 = regressão)
"""
from __future__ import annotations

import hashlib
import io
import json
import sys
import tempfile
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from forja_fontes_oficiais import (  # noqa: E402
    GATE_ARQUIVO, GATE_COTEJO, validar_cotejo_citacoes, validar_fontes_arquivadas)


def _arquivo(veredito_de, base=None):
    return validar_fontes_arquivadas(veredito_de, base)["gates"][GATE_ARQUIVO]


def _cotejo(checklist, ledger=None):
    return validar_cotejo_citacoes(checklist, ledger)["gates"][GATE_COTEJO]


def main() -> int:
    falhas = 0
    casos = 0
    temp = Path(tempfile.mkdtemp(prefix="forja_fontes_"))
    real = temp / "acordao.pdf"
    real.write_bytes(b"inteiro teor do acordao")
    digest = hashlib.sha256(real.read_bytes()).hexdigest()

    DEVE_REPROVAR = [
        ("ledger ausente", None, None),
        ("ledger vazio", {}, None),
        ("ledger sem nenhuma fonte", {"schemaVersion": 1, "sources": []}, None),
        ("fonte sem URL nem autoridade",
         {"sources": [{"id": "S1", "claim": "algo"}]}, None),
        ("copia arquivada que nao existe",
         {"sources": [{"id": "S1", "authority": "STJ", "archivedPath": "nao_existe.pdf",
                       "sha256": digest}]}, temp),
        ("hash declarado que nao confere",
         {"sources": [{"id": "S1", "authority": "STJ", "archivedPath": "acordao.pdf",
                       "sha256": "0" * 64}]}, temp),
    ]
    NAO_PODE_TRAVAR = [
        ("arquivamento integro com hash conferindo",
         {"sources": [{"id": "S1", "authority": "STJ", "officialUrl": "https://stj.jus.br/x",
                       "archivedPath": "acordao.pdf", "sha256": digest}]}, temp),
    ]

    for nome, ledger, base in DEVE_REPROVAR:
        casos += 1
        if _arquivo(ledger, base) != "fail":
            print(f"  FALHOU (não pegou): {nome}")
            falhas += 1
    for nome, ledger, base in NAO_PODE_TRAVAR:
        casos += 1
        if _arquivo(ledger, base) != "pass":
            print(f"  TRAVOU INDEVIDAMENTE: {nome}")
            falhas += 1

    # Nenhuma fonte arquivada: não bloqueia, mas para de dizer `pass`.
    casos += 1
    if _arquivo({"sources": [{"id": "S1", "authority": "STJ",
                              "officialUrl": "https://stj.jus.br/x"}]}) != "warn":
        print("  FALHOU: ledger sem arquivamento algum deveria ser `warn`, não aprovação")
        falhas += 1

    # Arquivamento parcial num caso que arquiva: P1, também `warn`.
    casos += 1
    if _arquivo({"sources": [{"id": "S1", "authority": "STJ", "archivedPath": "acordao.pdf",
                              "sha256": digest},
                             {"id": "S2", "authority": "STF"}]}, temp) != "warn":
        print("  FALHOU: arquivamento parcial deveria ser `warn`")
        falhas += 1

    # quotes_compared
    casos += 1
    if _cotejo(None) != "fail":
        print("  FALHOU: checklist ausente deveria reprovar")
        falhas += 1
    casos += 1
    if _cotejo({"items": []}) != "fail":
        print("  FALHOU: checklist sem itens deveria reprovar (conjunto vazio)")
        falhas += 1

    # A MC-15 em estado puro: nenhuma citação textual usada. Nove execuções
    # reportaram `pass`; o correto é dizer que o gate não se aplica.
    casos += 1
    if _cotejo({"items": [{"citation": "CPC, art. 300", "quoteUsed": False},
                          {"citation": "CPC, art. 903", "quoteUsed": False}]}) != "not_applicable":
        print("  FALHOU: sem citação textual o gate deveria ser `not_applicable`, não `pass`")
        falhas += 1

    casos += 1
    if _cotejo({"items": [{"citation": "STJ REsp 1", "quoteUsed": True}]}) != "fail":
        print("  FALHOU: citação textual sem cotejo registrado deveria reprovar")
        falhas += 1
    casos += 1
    if _cotejo({"items": [{"citation": "STJ REsp 1", "quoteUsed": True,
                           "locator": "voto, pp. 8-9"}]}) != "pass":
        print("  TRAVOU INDEVIDAMENTE: citação textual com localizador registrado")
        falhas += 1

    # A forma MARKDOWN do checklist — sete dos nove artefatos reais. Enquanto o
    # gate só lia JSON, `quotes_compared` não produzia veredito nenhum sobre
    # esses sete: um gate que não alcança o artefato não protege coisa alguma.
    MD_PARAFRASE = ("# Checklist de citações\n\n## Resultado\n"
                    "- [x] As quatro decisões do STJ foram arquivadas de endereços oficiais.\n"
                    "- [x] O parecer usará paráfrases fiéis. Não haverá transcrição literal "
                    "não comparada.\n")
    MD_PENDENTE = ("# Checklist\n\n"
                   "- [x] Acórdão do Tema 333 arquivado da fonte oficial.\n"
                   "- [ ] Conferir o inteiro teor do REsp 1.999.999 na fonte oficial.\n")
    MD_COTEJADO = ("# Checklist\n\n"
                   "- [x] Transcrição literal conferida contra o inteiro teor, voto pp. 8-9.\n")
    MD_MUDO = "# Checklist\n\n- [x] As fontes oficiais foram arquivadas em 03/08/2026.\n"
    casos += 1
    if _cotejo(MD_PARAFRASE) != "not_applicable":
        print("  FALHOU: checklist que declara paráfrase deveria ser not_applicable")
        falhas += 1
    casos += 1
    if _cotejo(MD_PENDENTE) != "fail":
        print("  FALHOU: caixa aberta é conferência pendente e deveria reprovar")
        falhas += 1
    casos += 1
    if _cotejo(MD_COTEJADO) != "pass":
        print("  TRAVOU INDEVIDAMENTE: transcrição declarada cotejada com localizador")
        falhas += 1
    casos += 1
    if _cotejo(MD_MUDO) != "warn":
        print("  FALHOU: checklist que não diz se houve transcrição deveria ficar em warn — "
              "afirmar cotejo aqui seria inventar prova")
        falhas += 1

    # CONTRAPROVA — os artefatos reais. Nenhum pode ser REPROVADO; `warn` é o achado.
    dialetos = {}
    resumo = []
    for arquivo in Path("state").rglob("source_ledger.json"):
        try:
            ledger = json.loads(arquivo.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            continue
        if not isinstance(ledger, dict):
            continue
        chave = tuple(sorted(ledger))
        if chave in dialetos:
            continue
        dialetos[chave] = arquivo
        casos += 1
        veredito = _arquivo(ledger, arquivo.parent)
        resumo.append(veredito)
        if veredito == "fail":
            print(f"  TRAVOU O APROVADO: {arquivo.parent}")
            for item in validar_fontes_arquivadas(ledger, arquivo.parent)["findings"]:
                if item["sev"] == "P0":
                    print(f"      {item['gate']}: {item['problema']}")
            falhas += 1

    if len(dialetos) < 4:
        print(f"  FALHOU: só {len(dialetos)} ledgers reais examinados — "
              "a contraprova perdeu o acervo")
        falhas += 1

    # Se TODO o acervo saísse `pass`, o gate não estaria medindo arquivamento:
    # há dois casos reais sem fonte arquivada nenhuma.
    if resumo and all(v == "pass" for v in resumo):
        print("  FALHOU: todos os ledgers reais saíram `pass` — dois deles não arquivam "
              "fonte alguma, então o gate não pode estar medindo o que afirma")
        falhas += 1

    if falhas:
        print(f"REGRESSÃO: {falhas} de {casos} verificações de fonte oficial falharam")
        return 1
    print(f"ok: {casos} verificações — nenhum dos {len(dialetos)} ledgers reais é reprovado; "
          f"vereditos do acervo: {', '.join(sorted(set(resumo)))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
