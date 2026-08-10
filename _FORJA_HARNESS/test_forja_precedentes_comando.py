# -*- coding: utf-8 -*-
import json
from pathlib import Path

from forja_precedentes_comando import analisar, gate_tema_paradigma


def _caso(tmp_path: Path, ledger: dict | None = None) -> Path:
    anexos = tmp_path / "Anexos do email"
    anexos.mkdir()
    (anexos / "1 - RE 852475 - Tema 897 STF.pdf").write_bytes(b"%PDF-1.4")
    if ledger is not None:
        (tmp_path / "F7_PRECEDENTES_DO_COMANDO.json").write_text(
            json.dumps(ledger, ensure_ascii=False), encoding="utf-8")
    return tmp_path


def test_reprova_precedente_anexado_sem_ledger(tmp_path):
    achados = analisar("Tema 897/STF (RE 852.475).", _caso(tmp_path))
    assert any(a["gate"] == "G12-precedentes-comando" for a in achados)


def test_reprova_precedente_marcado_citado_mas_ausente_da_peca(tmp_path):
    ledger = {"commandPrecedents": [{
        "attachment": "1 - RE 852475 - Tema 897 STF.pdf",
        "destination": "cited",
        "pieceLocator": "item 3",
    }]}
    achados = analisar("Tema 897/STF.", _caso(tmp_path, ledger))
    assert any("não aparece" in a["problema"] for a in achados)


def test_reprova_nao_uso_sem_justificativa_e_localizador(tmp_path):
    ledger = {"commandPrecedents": [{
        "attachment": "1 - RE 852475 - Tema 897 STF.pdf",
        "destination": "not_used",
        "justification": "redundante",
    }]}
    achados = analisar("Sem temas nesta peça.", _caso(tmp_path, ledger))
    assert any("não utilização" in a["problema"] for a in achados)


def test_reprova_primeira_mencao_de_tema_sem_paradigma(tmp_path):
    achados = gate_tema_paradigma(
        "O Tema 897/STF restringe a imprescritibilidade.\n\nDepois vem o RE 852.475.",
        tmp_path,
    )
    assert len(achados) == 1
    assert achados[0]["gate"] == "G13-tema-paradigma"


def test_contraprova_aprova_citacao_completa_realista(tmp_path):
    ledger = {"commandPrecedents": [{
        "attachment": "1 - RE 852475 - Tema 897 STF.pdf",
        "destination": "cited",
        "pieceLocator": "item 17",
    }]}
    texto = "O Tema 897/STF (RE 852.475) restringe a imprescritibilidade."
    assert analisar(texto, _caso(tmp_path, ledger)) == []


def test_contraprova_aprova_nao_uso_documentado(tmp_path):
    ledger = {"commandPrecedents": [{
        "attachment": "1 - RE 852475 - Tema 897 STF.pdf",
        "destination": "not_used",
        "justification": "Não utilizado porque a questão jurídica foi abandonada no comando final.",
        "reportLocator": "Relatório de entrega, item 4",
    }]}
    assert analisar("Sem temas nesta peça.", _caso(tmp_path, ledger)) == []

