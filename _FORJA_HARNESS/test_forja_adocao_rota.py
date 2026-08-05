# -*- coding: utf-8 -*-
"""O medidor de adoção não pode atribuir a marca de um DOCX ao seu vizinho."""
from __future__ import annotations

import hashlib
import json
import tempfile
from pathlib import Path

import forja_adocao_rota as modulo


def main():
    with tempfile.TemporaryDirectory() as temporario:
        raiz = Path(temporario)
        pasta = raiz / "saida"
        pasta.mkdir()
        aprovado = pasta / "aprovado.docx"
        vizinho = pasta / "vizinho.docx"
        aprovado.write_bytes(b"docx aprovado")
        vizinho.write_bytes(b"docx vizinho")
        sha = hashlib.sha256(aprovado.read_bytes()).hexdigest()
        (pasta / "FIDELIDADE_VISUAL.json").write_text(
            json.dumps({"docx": {"path": str(aprovado), "sha256": sha}}),
            encoding="utf-8",
        )

        anterior = modulo.FABRICA
        modulo.FABRICA = raiz
        try:
            resultado = modulo.medir(20)
        finally:
            modulo.FABRICA = anterior

        linhas = {linha["docx"]: linha for linha in resultado["linhas"]}
        assert linhas[aprovado.name]["passouPelaRota"] is True
        assert linhas[vizinho.name]["passouPelaRota"] is False

        aprovado.write_bytes(b"docx alterado depois do lastro")
        assert modulo._marcas_do_docx(aprovado) == []

    print("ok: o medidor vincula a marca ao DOCX exato e rejeita hash divergente")


if __name__ == "__main__":
    main()
