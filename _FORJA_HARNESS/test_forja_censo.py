"""Regressão do censo: cada caso aqui é um erro real de 09/08/2026.

O censo nasceu porque a fábrica não sabia o próprio estado. Um instrumento de
leitura que degrada em silêncio é pior que a falta dele, porque responde com
confiança — foi exatamente assim que `forja_axi.py` anunciou "28 of 28" sobre 91
casos. Estes testes prendem os comportamentos que tornam a mentira impossível.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

import forja_censo as fc


def _agora(dias=0):
    return (datetime.now(timezone.utc) - timedelta(days=dias)).isoformat()


def _caso(raiz: Path, nome: str, *, legado=None, n3=None, demanda: Path | None = None):
    pasta = raiz / f"case-{nome}"
    pasta.mkdir(parents=True, exist_ok=True)
    if legado is not None:
        if demanda is not None:
            legado.setdefault("inputs", {})["caseFolder"] = str(demanda)
        (pasta / "FORJA_STATE.json").write_text(
            json.dumps(legado, ensure_ascii=False), encoding="utf-8")
    if n3 is not None:
        (pasta / "FORJA_N3_STATE.json").write_text(
            json.dumps(n3, ensure_ascii=False), encoding="utf-8")
    return pasta


def _entregavel(pasta: Path, nome: str, tamanho: int):
    pasta.mkdir(parents=True, exist_ok=True)
    (pasta / nome).write_bytes(b"x" * tamanho)


@pytest.fixture
def raiz(tmp_path):
    return tmp_path / "state"


class TestPopulacaoNuncaVirouTotal:
    """O defeito de origem: fração anunciada como retrato da população."""

    def test_caso_ilegivel_derruba_completo_e_gera_P0(self, raiz):
        _caso(raiz, "bom", legado={"status": "pending", "currentPhase": "F0"})
        podre = raiz / "case-podre"
        podre.mkdir(parents=True)
        (podre / "FORJA_STATE.json").write_text("{ isto nao e json", encoding="utf-8")

        dados = fc.censo(raiz, resolucoes={})

        assert dados["populacao"] == {"pastasDeCaso": 2, "lidos": 1, "completo": False}
        assert "CEN1" in {a["id"] for a in fc.gate_censo(dados)}

    def test_pasta_sem_estado_e_estado_corrompido_dao_causas_distintas(self, raiz):
        """'Não localizado' não é diagnóstico: cada causa pede conserto diferente."""
        (raiz / "case-nua").mkdir(parents=True)
        corrompido = raiz / "case-corrompido"
        corrompido.mkdir(parents=True)
        (corrompido / "FORJA_STATE.json").write_text("{{{", encoding="utf-8")

        porques = {c["caseId"]: c["porque"] for c in fc.censo(raiz, resolucoes={})["casos"]}

        assert "não tem arquivo de estado" in porques["case-nua"]
        assert "presente e ilegível" in porques["case-corrompido"]

    def test_populacao_integra_nao_inventa_achado(self, raiz):
        demanda = raiz.parent / "demanda-ok"
        _entregavel(demanda, "peca.docx", 50_000)
        _caso(raiz, "ok", legado={"status": "fulfilled", "currentPhase": "F10",
                                  "phaseHistory": [{"phase": "F10", "at": _agora(1)}]},
              demanda=demanda)

        dados = fc.censo(raiz, resolucoes={})

        assert dados["populacao"]["completo"] is True
        assert fc.gate_censo(dados) == []


class TestFeitoExigeProva:
    """'fulfilled' significava entregue E triado-sem-demanda. Agora são palavras distintas."""

    def test_cumprido_sem_entregavel_e_concluido_sem_prova(self, raiz):
        demanda = raiz.parent / "demanda-vazia"
        demanda.mkdir(parents=True)
        _caso(raiz, "vazio", legado={"status": "fulfilled", "currentPhase": "F0",
                                     "phaseHistory": [{"phase": "F0", "at": _agora(30)}]},
              demanda=demanda)

        dados = fc.censo(raiz, resolucoes={})

        assert dados["casos"][0]["situacao"] == "concluido_sem_prova"
        assert "CEN2" in {a["id"] for a in fc.gate_censo(dados)}

    def test_declaracao_humana_converte_em_triado_sem_demanda(self, raiz):
        demanda = raiz.parent / "demanda-admin"
        demanda.mkdir(parents=True)
        _caso(raiz, "admin", legado={"status": "fulfilled", "currentPhase": "F0"},
              demanda=demanda)

        dados = fc.censo(raiz, resolucoes={
            "case-admin": {"motivo": "e-mail administrativo, sem peça pedida", "por": "Igor"}})

        assert dados["casos"][0]["situacao"] == "triado_sem_demanda"
        assert fc.gate_censo(dados) == []

    def test_prova_e_procurada_na_pasta_da_demanda_nao_na_de_estado(self, raiz):
        """O erro que quase inverteu o diagnóstico: procurei no lugar errado."""
        demanda = raiz.parent / "demanda-com-peca"
        _entregavel(demanda, "MINUTA.docx", 90_000)
        pasta = _caso(raiz, "certo", legado={"status": "fulfilled", "currentPhase": "F0"},
                      demanda=demanda)
        assert not list(pasta.glob("*.docx"))  # a pasta de estado está vazia de peça

        assert fc.censo(raiz, resolucoes={})["casos"][0]["situacao"] == "entregue"

    def test_arquivo_pequeno_nao_conta_como_entrega(self, raiz):
        demanda = raiz.parent / "demanda-placeholder"
        _entregavel(demanda, "rascunho.docx", 500)
        _caso(raiz, "ph", legado={"status": "fulfilled", "currentPhase": "F0"}, demanda=demanda)

        assert fc.censo(raiz, resolucoes={})["casos"][0]["situacao"] == "concluido_sem_prova"


class TestRelogioHonesto:
    """`updatedAt` é reescrito por varredura; a idade se mede do carimbo da fase."""

    def test_idade_vem_do_primeiro_carimbo_e_ignora_updatedAt(self, raiz):
        _caso(raiz, "velho", legado={
            "status": "pending", "currentPhase": "F0",
            "updatedAt": _agora(0),  # a varredura de hoje diz que é novo
            "phaseHistory": [{"phase": "F0", "at": _agora(30)},
                             {"phase": "F0", "at": _agora(10)},
                             {"phase": "F0", "at": _agora(0)}]})

        caso = fc.censo(raiz, resolucoes={})["casos"][0]

        assert caso["diasNaFase"] == 30
        assert caso["carimbosRepetidos"] == 2


class TestDoisEsquemasSemArbitro:
    def test_divergencia_entre_legado_e_n3_e_acusada(self, raiz):
        demanda = raiz.parent / "d"
        _entregavel(demanda, "p.pdf", 60_000)
        _caso(raiz, "div", legado={"status": "fulfilled", "currentPhase": "F0"},
              n3={"lifecycleStatus": "blocked"}, demanda=demanda)

        dados = fc.censo(raiz, resolucoes={})

        assert dados["divergentes"] == 1
        assert "CEN3" in {a["id"] for a in fc.gate_censo(dados)}


class TestPrazoNaFrente:
    def test_prazo_vencido_em_caso_aberto_e_P0(self, raiz):
        ontem = datetime.now() - timedelta(days=3)
        demanda = raiz.parent / f"PRAZO {ontem.day:02d} {ontem.month:02d} - Contrarrazoes"
        demanda.mkdir(parents=True)
        _caso(raiz, "prazo", legado={"status": "pending", "currentPhase": "F0"}, demanda=demanda)

        dados = fc.censo(raiz, resolucoes={})

        assert dados["casos"][0]["prazo"]["vencido"] is True
        assert "CEN4" in {a["id"] for a in fc.gate_censo(dados)}

    def test_o_que_tem_prazo_vem_antes_na_lista_do_que_se_deve(self, raiz):
        amanha = datetime.now() + timedelta(days=1)
        com = raiz.parent / f"PRAZO {amanha.day:02d} {amanha.month:02d} - Memoriais"
        com.mkdir(parents=True)
        sem = raiz.parent / "Estudo sem prazo"
        sem.mkdir(parents=True)
        _caso(raiz, "sem", legado={"status": "pending", "currentPhase": "F0"}, demanda=sem)
        _caso(raiz, "com", legado={"status": "pending", "currentPhase": "F0"}, demanda=com)

        fila = fc.devendo(fc.censo(raiz, resolucoes={}))

        assert fila[0]["caseId"] == "case-com"


class TestVocabularioFechado:
    def test_toda_situacao_atribuida_pertence_ao_vocabulario(self, raiz):
        demanda = raiz.parent / "d"
        _entregavel(demanda, "p.docx", 40_000)
        _caso(raiz, "a", legado={"status": "blocked", "currentPhase": "F0"})
        _caso(raiz, "b", legado={"status": "draft_awaiting_review", "currentPhase": "F7"})
        _caso(raiz, "c", legado={"status": "fulfilled", "currentPhase": "F10"}, demanda=demanda)
        _caso(raiz, "d", legado={"status": "pending", "currentPhase": "F0"})

        dados = fc.censo(raiz, resolucoes={})

        assert {c["situacao"] for c in dados["casos"]} <= set(fc.SITUACOES)
        assert set(dados["situacoes"]) == set(fc.SITUACOES)
