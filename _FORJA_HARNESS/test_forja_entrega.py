# -*- coding: utf-8 -*-
"""test_forja_entrega.py — regressão dos gates de reconciliação e entrega.

O caso que define esta leva é o `email_claims_true`: o e-mail é o único artefato
que o destinatário lê antes de decidir, e um e-mail que anuncia "pronto para
protocolo" sobre um pacote classificado como uso interno produz decisão errada
com peça certa. O gate não julga a retórica — confronta a promessa com a
política de liberação declarada no próprio pacote.

Uso: python test_forja_entrega.py   (exit 0 = ok; exit 1 = regressão)
"""
from __future__ import annotations

import hashlib
import io
import json
import sys
import tempfile
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from forja_entrega import (  # noqa: E402
    GATE_ANEXOS, GATE_EMAIL, GATE_HASHES, GATE_MAPEAMENTO, GATE_STATUS,
    validar_pacote, validar_reconciliacao)


def main() -> int:
    falhas = 0
    casos = 0
    temp = Path(tempfile.mkdtemp(prefix="forja_entrega_"))
    (temp / "pasta_do_caso").mkdir()
    comando = temp / "pasta_do_caso" / "COMANDO_DO_CASO.md"
    comando.write_text("# Comando\n", encoding="utf-8")
    peca = temp / "peca.docx"
    peca.write_bytes(b"conteudo da peca")
    digest = hashlib.sha256(peca.read_bytes()).hexdigest()

    MANIFESTO_OK = {"caseId": "case-x", "demandId": "d-1",
                    "caseFolder": str(temp / "pasta_do_caso"), "commandFile": str(comando)}

    def checar(nome, obtido, esperado):
        nonlocal falhas, casos
        casos += 1
        if obtido != esperado:
            print(f"  FALHOU: {nome} — esperado {esperado}, obtido {obtido}")
            falhas += 1

    def rec(m, r=None, gate=GATE_MAPEAMENTO):
        return validar_reconciliacao(m, r)["gates"][gate]

    checar("manifesto ausente", rec(None), "fail")
    checar("caseFolder inexistente",
           rec({**MANIFESTO_OK, "caseFolder": str(temp / "nao_existe")}), "fail")
    checar("commandFile não declarado",
           rec({k: v for k, v in MANIFESTO_OK.items() if k != "commandFile"}), "fail")
    checar("mapeamento íntegro", rec(MANIFESTO_OK), "pass")
    checar("status consistente contradiz divergências",
           rec(MANIFESTO_OK, {"status": "consistent", "divergences": ["fila x painel"]},
               GATE_STATUS), "fail")
    checar("status sem relatório", rec(MANIFESTO_OK, None, GATE_STATUS), "warn")

    # O relatório real é MARKDOWN — `forja_reconcile.py` nunca emitiu a versão
    # JSON que este gate procurava, e por isso `status_consistent` respondeu
    # `warn` nas três tentativas do acervo e jamais soube dizer `pass`. Estas
    # contraprovas usam a forma real do artefato.
    MD_LIMPO = ("# Relatório de reconciliação\n\n## Mapeamento\n- ok\n\n"
                "## Status\n- Painel: demanda `aberta`.\n"
                "- Nenhuma inconsistência painel ↔ estado detectada após o reconcile.\n")
    MD_DIVERGENTE = ("# Relatório\n\n## Status\n"
                     "- Divergência: o painel dá a demanda por cumprida e o estado diz `aberta`.\n"
                     "- Nenhuma inconsistência além dessa.\n")
    MD_SEM_STATUS = "# Relatório\n\n## Mapeamento\n- demanda x caso\n"
    checar("markdown sem divergência aprova", rec(MANIFESTO_OK, MD_LIMPO, GATE_STATUS), "pass")
    checar("markdown que se diz limpo e lista divergência reprova",
           rec(MANIFESTO_OK, MD_DIVERGENTE, GATE_STATUS), "fail")
    checar("markdown sem seção de status fica em warn",
           rec(MANIFESTO_OK, MD_SEM_STATUS, GATE_STATUS), "warn")

    def pac(m, email=None, gate=GATE_ANEXOS, existentes=None):
        return validar_pacote(m, email, temp, existentes)["gates"][gate]

    PACOTE = {"caseId": "case-x",
              "deliverables": [{"id": "peca-v1", "releasePolicy": "internal_review_only",
                                "path": "peca.docx", "sha256": digest,
                                "mdArtifactId": "final_markdown"}]}

    checar("pacote ausente", pac(None), "fail")
    checar("pacote sem entregável", pac({"deliverables": []}), "fail")
    checar("manifesto aponta artefato inexistente",
           pac(PACOTE, None, GATE_ANEXOS, existentes={"outro_artefato"}), "fail")
    checar("manifesto aponta artefato que existe",
           pac(PACOTE, None, GATE_ANEXOS, existentes={"final_markdown"}), "pass")
    checar("hash do entregável confere", pac(PACOTE, None, GATE_HASHES), "pass")
    checar("hash do entregável divergente",
           pac({"deliverables": [{"id": "p", "path": "peca.docx", "sha256": "0" * 64}]},
               None, GATE_HASHES), "fail")
    checar("entregável declarado que não existe no disco",
           pac({"deliverables": [{"id": "p", "path": "sumiu.docx", "sha256": digest}]},
               None, GATE_HASHES), "fail")

    # O gate que mais importa.
    checar("e-mail promete protocolo sobre pacote interno",
           pac(PACOTE, "Segue a peça, já pronta para protocolo.", GATE_EMAIL), "fail")
    checar("e-mail promete envio ao cliente sobre pacote interno",
           pac(PACOTE, "O parecer está liberado para o cliente.", GATE_EMAIL), "fail")
    checar("e-mail alinhado à política interna",
           pac(PACOTE, "Segue minuta para sua revisão interna antes de qualquer decisão.",
               GATE_EMAIL), "pass")
    # Pacote realmente protocolável pode prometer protocolo.
    checar("e-mail promete protocolo sobre pacote protocolável",
           pac({"deliverables": [{"id": "p", "releasePolicy": "strict_protocol"}]},
               "A peça está pronta para protocolo.", GATE_EMAIL), "pass")
    checar("sem e-mail para conferir", pac(PACOTE, None, GATE_EMAIL), "warn")

    # CONTRAPROVA — os artefatos reais.
    reais = 0
    for arquivo in Path("state").rglob("case_manifest.json"):
        try:
            dados = json.loads(arquivo.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            continue
        if not isinstance(dados, dict) or not dados.get("caseFolder"):
            continue
        reais += 1
        casos += 1
        # Só é regressão minha se o caminho EXISTE e mesmo assim reprova.
        if (Path(str(dados["caseFolder"])).exists()
                and validar_reconciliacao(dados)["gates"][GATE_MAPEAMENTO] == "fail"):
            print(f"  TRAVOU O APROVADO: {arquivo}")
            for item in validar_reconciliacao(dados)["findings"]:
                print(f"      {item['gate']}: {item['problema'][:140]}")
            falhas += 1

    if reais < 2:
        print(f"  FALHOU: só {reais} manifestos reais examinados")
        falhas += 1

    if falhas:
        print(f"REGRESSÃO: {falhas} de {casos} verificações de entrega falharam")
        return 1
    print(f"ok: {casos} verificações — {reais} manifestos reais, nenhum travado com caminho válido")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
