# -*- coding: utf-8 -*-
"""O mapa arquitetural gerado não pode envelhecer a skill por definição."""

from pathlib import Path

import forja_skill_deploy as deploy


def _skill(base: Path, texto: str = "---\nname: x\ndescription: y\n---\n") -> Path:
    (base / "reference").mkdir(parents=True)
    (base / "SKILL.md").write_text(texto, encoding="utf-8")
    (base / "reference" / "GUIA.md").write_text("guia\n", encoding="utf-8")
    return base


def test_inventario_ignora_mapa_arquitetural(tmp_path, monkeypatch):
    base = _skill(tmp_path / "skill")
    (base / "MAPA_IA.md").write_text("mapa da raiz\n", encoding="utf-8")
    (base / "reference" / "MAPA_IA.md").write_text(
        "mapa das referências\n", encoding="utf-8"
    )
    monkeypatch.setattr(deploy, "CANONICA", base)

    assert deploy._arquivos_da_canonica() == {
        "SKILL.md": "---\nname: x\ndescription: y\n---\n",
        "reference/GUIA.md": "guia\n",
    }


def test_deploy_nao_remove_nem_compara_mapa_gerado(tmp_path, monkeypatch):
    canonica = _skill(tmp_path / "canonica")
    destino = tmp_path / "loader" / "forja"
    monkeypatch.setattr(deploy, "CANONICA", canonica)
    monkeypatch.setattr(deploy, "DESTINOS", {"Teste": destino})

    deploy.espalhar()
    mapa = destino / "MAPA_IA.md"
    mapa.write_text("contexto específico do carregador\n", encoding="utf-8")

    resultado = deploy.espalhar(apenas_verificar=True)

    assert resultado["ok"]
    assert mapa.read_text(encoding="utf-8") == "contexto específico do carregador\n"
