"""Regressão do painel de vozes curtas e do placar de contribuição.

O que se afere aqui não é se os modelos respondem — isso a chamada real prova.
É se as **regras de contagem** resistem às formas conhecidas de o placar mentir:
amostra pequena com taxa perfeita, modelo que só concorda, e promoção que
ignora a bancada de fidelidade à fonte.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

import forja_contribuicao as fc
import forja_modelos as fm
import forja_painel_curto as pc


# --------------------------------------------------------------------------
# Tetos — cortados no código, não pedidos no prompt
# --------------------------------------------------------------------------

def test_corta_no_teto_de_observacoes_e_declara_o_corte():
    bruto = "\n".join(f"- observação {i}" for i in range(9))
    obs, corte = pc.extrair(bruto)
    assert len(obs) == pc.LIMITE_OBSERVACOES
    assert corte["observacoesDescartadas"] == 9 - pc.LIMITE_OBSERVACOES


def test_corta_no_teto_de_caracteres_e_declara():
    obs, corte = pc.extrair("- " + "a" * (pc.LIMITE_CARACTERES + 50))
    assert len(obs[0]) <= pc.LIMITE_CARACTERES + 1  # +1 pela reticência
    assert corte["observacoesTruncadas"] == 1


@pytest.mark.parametrize("linha", ["- ponto", "* ponto", "1. ponto", "2) ponto", "ponto"])
def test_aceita_os_formatos_que_o_modelo_de_fato_usa(linha):
    """Exigir o formato do molde trocaria conteúdo por obediência."""
    obs, _ = pc.extrair(linha)
    assert obs == ["ponto"]


def test_id_da_observacao_e_estavel_e_ignora_acento_e_caixa():
    a = pc.obs_id("m", "O  prazo  é  premissa")
    b = pc.obs_id("m", "o prazo e premissa")
    assert a == b
    assert a != pc.obs_id("outro", "o prazo e premissa")


def test_vozes_do_painel_estao_no_registro_e_sao_da_assinatura():
    for voz in pc.VOZES_PADRAO:
        modelo = fm.MODELOS[voz]
        assert modelo.provedor == "cursor", f"{voz} não roda pela assinatura do titular"
        assert modelo.usd_saida_por_milhao == 0.0


def test_kimi_k3_carrega_a_restricao_que_a_bancada_mediu():
    """A restrição não é opinião: 0 de 6 na condição solta, com 4 invenções."""
    assert "nao_afirma_fato" in fm.MODELOS["kimi-k3-cursor"].restricoes


def test_glm_nao_carrega_restricao_por_falta_de_medida():
    """Não aferido não é o mesmo que reprovado — os dois estados não colapsam."""
    assert fm.MODELOS["glm-5.2-cursor"].restricoes == ()
    assert fc._bancada("glm-5.2-cursor")["aferida"] is False


# --------------------------------------------------------------------------
# Placar
# --------------------------------------------------------------------------

def _painel(tmp_path: Path, caso: str, modelo: str, textos: list[str]) -> Path:
    obs = [{"obsId": pc.obs_id(modelo, t), "texto": t} for t in textos]
    dados = {
        "contrato": "FORJA-PAINEL-CURTO-v1", "caso": caso, "fase": "F4",
        "em": "2026-08-07T00:00:00-03:00", "natureza": "opinião interna",
        "vozes": [{"modelo": modelo, "familia": fm.MODELOS[modelo].familia,
                   "observacoes": obs}],
        "falhas": [],
        "decisoes": [{"obsId": o["obsId"], "modelo": modelo, "veredito": None,
                      "duplicadaDe": None, "motivo": None} for o in obs],
    }
    caminho = tmp_path / f"{caso}_PAINEL.json"
    caminho.write_text(json.dumps(dados, ensure_ascii=False), encoding="utf-8")
    return caminho


def _decidir(caminho: Path, vereditos: list[str], duplicada_de: str = "outro") -> None:
    dados = json.loads(caminho.read_text(encoding="utf-8"))
    for decisao, veredito in zip(dados["decisoes"], vereditos):
        decisao["veredito"] = veredito
        if veredito == "duplicada":
            decisao["duplicadaDe"] = duplicada_de
    caminho.write_text(json.dumps(dados, ensure_ascii=False), encoding="utf-8")


@pytest.fixture()
def registro_isolado(tmp_path, monkeypatch):
    monkeypatch.setattr(fc, "REGISTRO", tmp_path / "CONTRIBUICAO.json")
    return tmp_path


def test_amostra_pequena_nao_e_elegivel_mesmo_com_placar_perfeito(registro_isolado):
    """Dois acertos de dois dão 100% e não dizem nada."""
    caminho = _painel(registro_isolado, "C1", "glm-5.2-cursor", ["a", "b"])
    _decidir(caminho, ["acatada", "acatada"])
    fc.colher(caminho, por="teste")
    linha = fc.placar()["modelos"][0]
    assert linha["indice"] == 100.0
    assert linha["elegivel"] is False
    assert "mínimo" in linha["motivoInelegivel"]


def test_um_caso_longo_sozinho_nao_vira_padrao(registro_isolado):
    """Volume de um caso só é volume, não recorrência entre casos."""
    caminho = _painel(registro_isolado, "C1", "glm-5.2-cursor",
                      [f"obs {i}" for i in range(14)])
    _decidir(caminho, ["acatada"] * 14)
    fc.colher(caminho, por="teste")
    linha = fc.placar()["modelos"][0]
    assert linha["n"] == 14 and linha["casos"] == 1
    assert linha["elegivel"] is False
    assert "caso" in linha["motivoInelegivel"]


def test_quem_so_concorda_nao_pontua(registro_isolado):
    """`duplicada` conta no denominador e não soma — é a defesa contra o eco."""
    caminho = _painel(registro_isolado, "C1", "glm-5.2-cursor", ["a", "b", "c", "d"])
    _decidir(caminho, ["duplicada"] * 4)
    fc.colher(caminho, por="teste")
    linha = fc.placar()["modelos"][0]
    assert linha["indice"] == 0.0
    assert linha["eco"] == 100.0


def test_errada_desconta_e_nao_e_apenas_neutra(registro_isolado):
    """Observação errada custa verificação; empatar com rejeitada apagaria isso."""
    a = _painel(registro_isolado, "C1", "glm-5.2-cursor", ["a", "b"])
    _decidir(a, ["acatada", "rejeitada"])
    fc.colher(a, por="teste")
    so_rejeitada = fc.placar()["modelos"][0]["indice"]

    monkey = _painel(registro_isolado, "C2", "glm-5.2-cursor", ["c", "d"])
    _decidir(monkey, ["acatada", "errada"])
    fc.colher(monkey, por="teste")
    com_errada = fc.placar()["modelos"][0]["indice"]
    assert com_errada < so_rejeitada


def test_colher_e_idempotente(registro_isolado):
    caminho = _painel(registro_isolado, "C1", "glm-5.2-cursor", ["a", "b"])
    _decidir(caminho, ["acatada", "rejeitada"])
    fc.colher(caminho, por="teste")
    fc.colher(caminho, por="teste")
    assert fc.placar()["modelos"][0]["n"] == 2


def test_duplicada_sem_origem_e_recusada_na_colheita(registro_isolado):
    caminho = _painel(registro_isolado, "C1", "glm-5.2-cursor", ["a"])
    dados = json.loads(caminho.read_text(encoding="utf-8"))
    dados["decisoes"][0]["veredito"] = "duplicada"
    caminho.write_text(json.dumps(dados, ensure_ascii=False), encoding="utf-8")
    resultado = fc.colher(caminho, por="teste")
    assert resultado["colhidas"] == 0
    assert any("duplicada" in p for p in resultado["invalidas"])


def test_veredito_fora_do_vocabulario_nao_entra(registro_isolado):
    caminho = _painel(registro_isolado, "C1", "glm-5.2-cursor", ["a"])
    dados = json.loads(caminho.read_text(encoding="utf-8"))
    dados["decisoes"][0]["veredito"] = "genial"
    caminho.write_text(json.dumps(dados, ensure_ascii=False), encoding="utf-8")
    resultado = fc.colher(caminho, por="teste")
    assert resultado["colhidas"] == 0 and resultado["invalidas"]


def test_amostra_le_o_texto_do_painel_e_nao_do_ledger(registro_isolado):
    """O ledger guarda localizador, não conteúdo. Contar não é ler."""
    caminho = _painel(registro_isolado, "C1", "glm-5.2-cursor", ["texto que importa"])
    _decidir(caminho, ["acatada"])
    fc.colher(caminho, por="teste")
    guardado = json.loads((registro_isolado / "CONTRIBUICAO.json").read_text(encoding="utf-8"))
    assert "texto que importa" not in json.dumps(guardado, ensure_ascii=False)
    assert fc.amostra("glm-5.2-cursor")[0]["texto"] == "texto que importa"


# --------------------------------------------------------------------------
# Promoção
# --------------------------------------------------------------------------

def _elegivel(pasta: Path, modelo: str) -> None:
    for i in range(3):
        caminho = _painel(pasta, f"CASO{i}", modelo, [f"obs {i}-{j}" for j in range(5)])
        _decidir(caminho, ["acatada"] * 4 + ["rejeitada"])
        fc.colher(caminho, por="teste")


def test_promocao_exige_pessoa(registro_isolado):
    _elegivel(registro_isolado, "glm-5.2-cursor")
    with pytest.raises(fc.ContribuicaoError, match="aprovado-por"):
        fc.promover("glm-5.2-cursor", para="consultivo", aprovado_por="  ")


def test_nao_se_pula_degrau(registro_isolado):
    _elegivel(registro_isolado, "glm-5.2-cursor")
    with pytest.raises(fc.ContribuicaoError, match="próximo degrau"):
        fc.promover("glm-5.2-cursor", para="candidato", aprovado_por="Igor")


def test_promocao_congela_a_evidencia_do_momento(registro_isolado):
    _elegivel(registro_isolado, "glm-5.2-cursor")
    ficha = fc.promover("glm-5.2-cursor", para="consultivo", aprovado_por="Igor")
    assert ficha["degrau"] == "consultivo"
    assert ficha["evidencia"]["casos"] == 3
    assert ficha["evidencia"]["n"] == 15


def test_candidato_barrado_por_falta_de_bancada(registro_isolado):
    """Não aferido não é aprovado, e o placar de contribuição não mede invenção."""
    _elegivel(registro_isolado, "glm-5.2-cursor")
    fc.promover("glm-5.2-cursor", para="consultivo", aprovado_por="Igor")
    with pytest.raises(fc.ContribuicaoError, match="bancada"):
        fc.promover("glm-5.2-cursor", para="candidato", aprovado_por="Igor")


def test_candidato_barrado_por_restricao_medida(registro_isolado):
    """Bom de ângulo não revoga reprovação em fidelidade à fonte."""
    _elegivel(registro_isolado, "kimi-k3-cursor")
    fc.promover("kimi-k3-cursor", para="consultivo", aprovado_por="Igor")
    with pytest.raises(fc.ContribuicaoError, match="nao_afirma_fato"):
        fc.promover("kimi-k3-cursor", para="candidato", aprovado_por="Igor")


def test_bancada_casa_o_nome_de_hoje_com_o_da_epoca():
    """`kimi-k3-cursor` hoje é o `kimi-k3` que reprovou em 26/07/2026.

    Sem esse casamento, um modelo reprovado voltaria como "nunca aferido" só
    porque a rota mudou de nome — que é como uma medição ruim desaparece.
    """
    banca = fc._bancada("kimi-k3-cursor")
    assert banca["aferida"] is True
    assert banca["invencoes"] > 0


def test_revalidar_acusa_perda_de_lastro_sem_apagar_nada(registro_isolado):
    _elegivel(registro_isolado, "glm-5.2-cursor")
    fc.promover("glm-5.2-cursor", para="consultivo", aprovado_por="Igor")
    registro = fc.carregar()
    registro["decisoes"] = registro["decisoes"][:2]
    fc.gravar(registro)
    fichas = fc.revalidar()
    assert fichas[0]["divergencias"]
    assert fc.carregar()["degraus"]["glm-5.2-cursor"]["degrau"] == "consultivo"


# --------------------------------------------------------------------------
# Natureza — o que este subsistema não é
# --------------------------------------------------------------------------

def test_painel_declara_que_nao_e_gate_nem_fonte():
    natureza = pc.painel.__doc__ or ""
    contrato = pc.VERSAO
    assert contrato == "FORJA-PAINEL-CURTO-v1"
    assert "opinião" in natureza.casefold() or "opiniao" in natureza.casefold()


def test_a_instrucao_opcional_chega_a_f4_e_f7_com_o_arquivo_certo():
    """Recurso que o agente não lembra que existe é recurso ausente (Lição 270).

    E o nome do arquivo tem de seguir a fase: um `--saida F4_...` sugerido
    dentro da F7 põe o artefato da auditoria com nome do blueprint, e quem for
    procurá-lo depois não o acha.
    """
    origem = (Path(__file__).parent / "forja_run.py").read_text(
        encoding="utf-8", errors="replace")
    bloco = origem.split('context["instructions"]["painelCurto"]', 1)
    assert len(bloco) == 2, "a instrução opcional do painel sumiu do RUN_CONTEXT"
    anterior = origem.split('context["instructions"]["painelCurto"]')[0]
    assert 'F7_AUDITORIA_JURIDICA_FACTUAL' in anterior.rsplit("if phase in", 1)[-1]
    assert '_PAINEL_CURTO.json' in bloco[1][:900]
    assert '"opcional": True' in bloco[1][:200]


def test_o_painel_nao_e_saida_obrigatoria_de_nenhuma_fase():
    """Voz opcional que vira exigência dura contradiz o pedido de gastar pouco.

    E criaria dependência bloqueante de um modelo que reprovou a bancada. Se um
    dia isto mudar, muda por ADR — e este teste é onde a mudança aparece.
    """
    for contrato in (Path(__file__).parent / "phase_contracts").glob("*.json"):
        dados = json.loads(contrato.read_text(encoding="utf-8"))
        assert "painel_curto" not in dados.get("requiredOutputs", [])
        assert "painel_curto" not in dados.get("requiredGates", [])
