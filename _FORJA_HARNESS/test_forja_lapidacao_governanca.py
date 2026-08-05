# -*- coding: utf-8 -*-
"""test_forja_lapidacao_governanca.py — cada invariante é visto reprovando.

A regra desta suíte vem do harness do SQLite e não do costume desta casa: um
controle que nunca foi observado FALHANDO não prova nada. Suíte verde por não
enxergar é o modo de falha mais caro que existe, porque compra confiança sem
entregar cobertura.

Então cada invariante com dependência isolável aparece aqui em contraprova:

  - **controle benigno**: entrada legítima que ele NÃO pode acusar;
  - **sabotagem**: dano deliberado que ele TEM de acusar.

Os casos de regressão abaixo são bugs reais cometidos na construção deste
mesmo módulo, em 05/08/2026, e é por isso que eles existem:

  1. `inv_f2a_congelado` lia `schemaVersion`. As 16 árvores trazem
     `schemaVersion="1"` e declaram o protocolo em `protocolVersion`. O invariante
     estava cego e teria aprovado um v2 para sempre. (Lição 188 repetida.)
  2. `inv_repo_do_engine` procurava a substring "/state/" com barra inicial, mas
     `git ls-files` devolve caminho relativo. O invariante reportava 759 binários e
     ZERO arquivos de caso, quando havia 5.691 arquivos de caso versionados. O bug
     escondia justamente a parte mais grave do achado.
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ))

import forja_lapidacao_governanca as gov  # noqa: E402


SALVAR_INTEGRO = '''
class PecaVisual:
    def salvar(self):
        self._sanitizar_metadados()
        self._validar_porta_unica()
        self._validar_lastro_documental()
        self.doc.save(self.saida)
        return self.saida
'''

SALVAR_SABOTADO = '''
class PecaVisual:
    def salvar(self):
        # A porta foi removida do caminho e deixada num metodo morto logo abaixo.
        # Um grep por "_validar_porta_unica" encontraria a string e aprovaria.
        self._sanitizar_metadados()
        self._validar_lastro_documental()
        self.doc.save(self.saida)
        return self.saida

    def _rota_antiga(self):
        self._validar_porta_unica()
'''


def _estado_com_caso(tmp: Path, blockers, ciclo="blocked") -> Path:
    d = tmp / "state" / gov.CASO_FAIL_CLOSED
    d.mkdir(parents=True, exist_ok=True)
    (d / "FORJA_N3_STATE.json").write_text(
        json.dumps({"blockers": blockers, "lifecycleStatus": ciclo, "revision": 177},
                   ensure_ascii=False), encoding="utf-8")
    return tmp / "state"


def _arvore(tmp: Path, nome: str, campos: dict) -> Path:
    d = tmp / "state" / nome
    d.mkdir(parents=True, exist_ok=True)
    (d / "F2_QUESTION_TREE.json").write_text(
        json.dumps(campos, ensure_ascii=False), encoding="utf-8")
    return tmp / "state"


def rodar() -> int:
    falhas = []

    def caso(nome, ok, detalhe=""):
        if ok:
            return
        print(f"  FALHOU: {nome} {detalhe}")
        falhas.append(nome)

    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)

        # --- I1 fail-closed -------------------------------------------------
        st = _estado_com_caso(tmp / "i1ok", ["fonte prevalente não validada"])
        r = gov.inv_fail_closed_preservado(st)
        caso("I1 controle: caso travado é aprovado", r["estado"] == "APROVADO", r["evidencia"])

        st = _estado_com_caso(tmp / "i1sab", [])
        r = gov.inv_fail_closed_preservado(st)
        caso("I1 sabotagem: blockers esvaziado é reprovado",
             r["estado"] == "REPROVADO", r["evidencia"])

        st = _estado_com_caso(tmp / "i1sab2", ["ainda travado"], ciclo="delivered")
        r = gov.inv_fail_closed_preservado(st)
        caso("I1 sabotagem: entregue com bloqueio aberto é reprovado",
             r["estado"] == "REPROVADO", r["evidencia"])

        r = gov.inv_fail_closed_preservado(tmp / "nao-existe")
        caso("I1 estado ausente vira INDETERMINADO, nunca APROVADO",
             r["estado"] == "INDETERMINADO", r["evidencia"])

        # --- I2b porta única ------------------------------------------------
        kit_ok = tmp / "kit_ok.py"
        kit_ok.write_text(SALVAR_INTEGRO, encoding="utf-8")
        r = gov.inv_porta_unica(kit_ok)
        caso("I2b controle: salvar com as três validações é aprovado",
             r["estado"] == "APROVADO", r["evidencia"])

        kit_mau = tmp / "kit_mau.py"
        kit_mau.write_text(SALVAR_SABOTADO, encoding="utf-8")
        r = gov.inv_porta_unica(kit_mau)
        caso("I2b sabotagem: porta movida para método morto é reprovada",
             r["estado"] == "REPROVADO", r["evidencia"])
        caso("I2b acusa nominalmente a validação que sumiu",
             "_validar_porta_unica" in r["evidencia"], r["evidencia"])

        # --- I7 congelamento do F2A ----------------------------------------
        st = _arvore(tmp / "i7ok", "caso-a",
                     {"schemaVersion": "1", "protocolVersion": "FORJA-F2A-100-v1"})
        r = gov.inv_f2a_congelado(st)
        caso("I7 controle: protocolo v1 é aprovado", r["estado"] == "APROVADO", r["evidencia"])

        # REGRESSÃO do bug real: o marcador vive em protocolVersion. Se alguém
        # voltar a ler só schemaVersion, este caso passa a APROVAR um v2.
        st = _arvore(tmp / "i7sab", "caso-b",
                     {"schemaVersion": "1", "protocolVersion": "FORJA-F2A-100-v2"})
        r = gov.inv_f2a_congelado(st)
        caso("I7 sabotagem: v2 declarado em protocolVersion é reprovado",
             r["estado"] == "REPROVADO", r["evidencia"])

        st = _arvore(tmp / "i7mudo", "caso-c", {"schemaVersion": "1", "outroCampo": "x"})
        r = gov.inv_f2a_congelado(st)
        caso("I7 árvore sem marcador nenhum vira INDETERMINADO, não APROVADO",
             r["estado"] == "INDETERMINADO", r["evidencia"])

    # --- propriedade de arquivo ---------------------------------------------
    p = gov.propriedade_arquivo([
        {"id": "m1", "arquivos": ["forja_lastro.py"]},
        {"id": "m2", "arquivos": ["forja_verificador.py"]},
    ])
    caso("propriedade controle: melhorias disjuntas correm em paralelo",
         p["veredito"] == "APROVADO" and len(p["lotesSerializados"]) == 1,
         json.dumps(p["lotesSerializados"], ensure_ascii=False))

    p = gov.propriedade_arquivo([
        {"id": "m1", "arquivos": ["forja_lastro.py", "a.py"]},
        {"id": "m2", "arquivos": ["FORJA_LASTRO.PY"]},
    ])
    caso("propriedade sabotagem: colisão é detectada apesar da caixa diferente",
         len(p["arquivosDisputados"]) == 1, json.dumps(p["arquivosDisputados"]))
    caso("propriedade sabotagem: colidentes vão para lotes distintos",
         len(p["lotesSerializados"]) == 2,
         json.dumps(p["lotesSerializados"], ensure_ascii=False))

    p = gov.propriedade_arquivo([
        {"id": "gigante", "arquivos": [f"f{i}.py" for i in range(7)]},
    ])
    caso("propriedade sabotagem: melhoria de 7 arquivos é reprovada",
         p["veredito"] == "REPROVADO", p["motivo"])

    # --- sinais de desperdício ----------------------------------------------
    d = gov.sinais_desperdicio([
        {"id": "a", "arquivos": ["x.py"], "sabotagemMaliciosa": "valor sem fonte"},
    ])
    caso("desperdício controle: proposta bem formada não acusa",
         d["veredito"] == "APROVADO", json.dumps(d["sinais"], ensure_ascii=False))

    d = gov.sinais_desperdicio([
        {"id": "a", "arquivos": ["x.py"], "sabotagemMaliciosa": "s"},
        {"id": "b", "arquivos": ["x.py"], "sabotagemMaliciosa": "s"},
    ])
    caso("desperdício sabotagem: duas propostas no mesmo arquivo acusam duplicidade",
         any(s["sinal"] == "propostas-duplicadas" for s in d["sinais"]),
         json.dumps(d["sinais"], ensure_ascii=False))

    d = gov.sinais_desperdicio([{"id": "a", "arquivos": [], "sabotagemMaliciosa": "s"}])
    caso("desperdício sabotagem: proposta sem arquivo é mudança documental",
         any(s["sinal"] == "proposta-sem-arquivo" for s in d["sinais"]),
         json.dumps(d["sinais"], ensure_ascii=False))

    d = gov.sinais_desperdicio([{"id": "a", "arquivos": ["x.py"]}])
    caso("desperdício sabotagem: proposta sem contraprova é acusada",
         any(s["sinal"] == "sem-contraprova" for s in d["sinais"]),
         json.dumps(d["sinais"], ensure_ascii=False))

    d = gov.sinais_desperdicio([], agentes_gastos=gov.LIMITES["agentesTotal"] + 1)
    caso("desperdício sabotagem: teto de agentes estourado é acusado",
         any(s["sinal"] == "teto-de-agentes-estourado" for s in d["sinais"]),
         json.dumps(d["sinais"], ensure_ascii=False))

    # --- REGRESSÃO do caminho relativo do git -------------------------------
    # O bug real: "state" era procurado como "/state/" e nunca casava com o
    # caminho relativo do `git ls-files`. Provo aqui a semântica corrigida.
    caminhos = ["state/case-x/prova.png", "forja_run.py", "telemetria/a.json"]
    casos_detectados = [c for c in caminhos if "state" in Path(c.replace("\\", "/")).parts]
    caso("regressão: caminho relativo do git é reconhecido como material de caso",
         casos_detectados == ["state/case-x/prova.png"], str(casos_detectados))
    caso("regressão: a busca antiga por '/state/' de fato falhava",
         not any("/state/" in c for c in caminhos),
         "se este caso falhar, o bug original não era o que se descreveu")

    # A expressão acima é apenas a explicação da regressão. A contraprova chama
    # a função real com fixture controlável; sem isso o teste poderia passar
    # enquanto inv_repo_do_engine estivesse olhando para outra coisa.
    r = gov.inv_repo_do_engine([
        "forja_run.py", "state/case-x/prova.json", "state/FILA_PRIORIZADA.json",
    ])
    caso("I4 sabotagem: função real detecta material em state",
         r["estado"] == "REPROVADO"
         and "1 pasta(s) de state/" in r["evidencia"]
         and "1 arquivo(s) diretamente na raiz" in r["evidencia"],
         r["evidencia"])

    r = gov.inv_repo_do_engine(["forja_run.py", "forja_lastro.py"])
    caso("I4 controle: função real aprova checkout sem material proibido",
         r["estado"] == "APROVADO", r["evidencia"])

    # --- o veredito agregado nunca aprova com indeterminado -----------------
    agregado = gov.verificar_invariantes()
    caso("veredito agregado é um dos três estados válidos",
         agregado["veredito"] in {"APROVADO", "REPROVADO", "INDETERMINADO"},
         agregado["veredito"])
    caso("todo invariante devolve natureza declarada",
         all(r.get("natureza") in {"comportamental", "estrutural"}
             for r in agregado["invariantes"]),
         str([r.get("natureza") for r in agregado["invariantes"]]))

    if falhas:
        print(f"\nFALHOU: {len(falhas)} verificação(ões) — {', '.join(falhas)}")
        return 1
    print("ok: os invariantes da lapidação foram vistos aprovando o legítimo e "
          "reprovando cada sabotagem, incluindo as duas cegueiras reais de 05/08")
    return 0


if __name__ == "__main__":  # pragma: no cover
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    raise SystemExit(rodar())
