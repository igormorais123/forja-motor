# -*- coding: utf-8 -*-
"""Regressão do registro de rotas e do gate de insumo bloqueado.

As fixtures são os dois bloqueios falsos reais de 06 e 07/08/2026, e não casos
inventados. Se um dia alguém afrouxar o gate, o teste falha com a mesma frase
que a esteira mandou ao titular naquela semana.

Nenhum teste aqui vai à rede. A conferência ao vivo é do comando ``--probe``,
que é outra coisa: teste de regressão que depende de portal de tribunal fica
vermelho por queda de servidor e ensina a equipe a ignorá-lo.
"""
from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path

import pytest

import forja_insumo_bloqueado as gate
import forja_rotas_fonte as rf


HOJE = date(2026, 8, 7)


_PADRAO = object()


def _caso(tmp_path: Path, itens, recebidos=_PADRAO) -> Path:
    # `recebidos=[]` precisa chegar vazio ao gate: é o cenário do teste de
    # inventário ausente. Um `or` aqui repõe o padrão e o teste passa por
    # engano, medindo outra coisa.
    if recebidos is _PADRAO:
        recebidos = [{"documento": "autos em PDF", "conferido": True}]
    case = tmp_path / "case-x"
    (case / "n4_artifacts").mkdir(parents=True)
    (case / "n4_artifacts" / gate.ARQUIVO).write_text(json.dumps({
        "schema": gate.VERSAO,
        "caseId": "case-x",
        "recebidos": recebidos,
        "itens": itens,
    }, ensure_ascii=False), encoding="utf-8")
    return case


def _item(**kw):
    base = {
        "documento": "acórdão do agravo interno",
        "fonte": "STJ",
        "tipoDocumento": "acordao",
        "rotasTentadas": ["stj-acordao-integra"],
        "causa": "indisponivel_na_fonte",
        "diligencias": [{"onde": "portal do STJ", "quando": "2026-08-07",
                         "resultado": "serviço fora do ar durante todo o dia"}],
        "consequencia": "a distinção do precedente fica sem lastro",
        "rotaDeSolucao": "advogado do caso abre a página à mão",
        "revalidarApos": "2026-08-20",
    }
    base.update(kw)
    return base


# --------------------------------------------------------------- o registro

def test_registro_traz_as_duas_metades():
    """Rota que serve e par que não é servido têm o mesmo peso.

    Sem a metade negativa não se distingue 'a fonte não entrega isso a ninguém'
    de 'a nossa ferramenta não deu conta', que é a confusão do erro do STF.
    """
    assert any(r.get("serve") for r in rf.ROTAS.values())
    assert any(r.get("serve") is False for r in rf.ROTAS.values())


def test_toda_rota_que_serve_tem_armadilha_e_amostra():
    """Rota sem armadilha registrada é rota que o próximo agente vai perder.

    Nos dois casos reais o obstáculo não foi a existência da porta, foi o
    detalhe que fazia a porta parecer fechada.

    A amostra do ``--probe`` só é exigida de rota de rede. Rota local declara
    ``local: True`` e fica dispensada — a dispensa é explícita justamente para
    que a próxima rota de rede não herde a folga por descuido.
    """
    for chave, rota in rf.ROTAS.items():
        if not rota.get("serve"):
            continue
        assert rota.get("armadilha"), f"{chave} sem armadilha declarada"
        assert rota.get("url"), f"{chave} sem url"
        if rota.get("local"):
            assert rota.get("probe") is None, (
                f"{chave} se declara local e mesmo assim traz probe; "
                f"decida qual das duas coisas ela é")
            continue
        assert rota.get("probe"), f"{chave} sem amostra para --probe"


def test_dispensa_de_probe_e_excecao_declarada_e_rara():
    """A folga do probe não pode virar o caminho de menor resistência.

    Se a maioria das rotas passar a se declarar local, o registro deixa de ser
    conferível contra o mundo e vira documentação interna.
    """
    servem = [r for r in rf.ROTAS.values() if r.get("serve")]
    locais = [r for r in servem if r.get("local")]
    assert len(locais) < len(servem) / 2, (
        "mais da metade das rotas que servem se declara local — o registro "
        "parou de ser exercitável")


def test_entrada_negativa_diz_a_causa_certa():
    for chave, rota in rf.ROTAS.items():
        if rota.get("serve") is not False:
            continue
        assert rota.get("causaCorreta") in gate.CAUSAS, f"{chave}: causa fora do vocabulário"
        for c in rota.get("causasAdmissiveis") or ():
            assert c in gate.CAUSAS, f"{chave}: causa admissível fora do vocabulário"


def test_limitacao_da_ferramenta_nunca_e_admissivel_em_entrada_negativa():
    """O erro exato do STF: chamar de limitação nossa o que a fonte não entrega."""
    for chave, rota in rf.ROTAS.items():
        if rota.get("serve") is False:
            admissiveis = rota.get("causasAdmissiveis") or (rota.get("causaCorreta"),)
            assert "limitacao_da_ferramenta" not in admissiveis, chave


def test_nao_tentadas_aponta_a_porta_que_sobrou():
    assert rf.nao_tentadas("STJ", "acordao", []) == ["stj-acordao-integra"]
    assert rf.nao_tentadas("STJ", "acordao", ["stj-acordao-integra"]) == []


def test_conferencia_das_rotas_esta_dentro_da_validade():
    """Registro vencido é a mesma doença que ele trata, com outra roupa."""
    assert rf.desatualizadas(HOJE) == []


# ------------------------------------------------------- o gate, nos 2 erros

def test_reprova_bloqueio_com_rota_conhecida_por_tentar(tmp_path):
    """O erro de 06/08: 'a automação não alcança' com a porta do STJ fechada por parâmetro."""
    caso = _caso(tmp_path, [_item(rotasTentadas=[], causa="limitacao_da_ferramenta")])
    problemas = gate.validar(caso, hoje=HOJE)
    assert any("não foi tentada" in p and "stj-acordao-integra" in p for p in problemas)


def test_reprova_limitacao_da_ferramenta_quando_a_fonte_nao_entrega(tmp_path):
    """O erro de 07/08: o portal não divulga petição de parte alguma, e isso não é falha nossa."""
    caso = _caso(tmp_path, [_item(
        documento="petição da PGR",
        fonte="STF", tipoDocumento="peticao_de_parte",
        rotasTentadas=[], causa="limitacao_da_ferramenta")])
    problemas = gate.validar(caso, hoje=HOJE)
    assert any("causa admissível é indisponivel_na_fonte" in p for p in problemas)


def test_reprova_habilitacao_onde_a_restricao_e_uniforme(tmp_path):
    """A outra metade do mesmo erro: culpar a nossa procuração por regra que vale para todos."""
    caso = _caso(tmp_path, [_item(
        documento="petição da parte adversa",
        fonte="STF", tipoDocumento="peticao_de_parte",
        rotasTentadas=[], causa="sem_habilitacao_nos_autos")])
    problemas = gate.validar(caso, hoje=HOJE)
    assert any("causa admissível é indisponivel_na_fonte" in p for p in problemas)


def test_aceita_habilitacao_no_stj_onde_existe_rota_autenticada(tmp_path):
    """No STJ há rota autenticada real, então a habilitação é diagnóstico legítimo.

    A distinção importa: lá a diligência é executável por quem tem procuração;
    no STF, no processo em que não somos parte, ela não tinha objeto.
    """
    caso = _caso(tmp_path, [_item(
        documento="AgInt da parte adversa",
        fonte="STJ", tipoDocumento="peticao_de_parte",
        rotasTentadas=[], causa="sem_habilitacao_nos_autos")])
    assert gate.validar(caso, hoje=HOJE) == []


def test_reprova_rota_citada_que_nao_existe_no_registro(tmp_path):
    caso = _caso(tmp_path, [_item(rotasTentadas=["stj-acordao-integra", "rota-imaginaria"])])
    problemas = gate.validar(caso, hoje=HOJE)
    assert any("rota-imaginaria" in p for p in problemas)


# ------------------------------------------------------------- revalidação

@pytest.mark.parametrize("valor,trecho", [
    (None, "falta 'revalidarApos'"),
    ("2026-07-01", "já venceu"),
    ("2027-01-01", "prazo longo demais"),
])
def test_bloqueio_precisa_de_prazo_curto_para_voltar_a_fila(tmp_path, valor, trecho):
    item = _item()
    if valor is None:
        item.pop("revalidarApos")
    else:
        item["revalidarApos"] = valor
    problemas = gate.validar(_caso(tmp_path, [item]), hoje=HOJE)
    assert any(trecho in p for p in problemas)


def test_vencidos_devolve_o_item_a_fila(tmp_path):
    _caso(tmp_path, [_item(revalidarApos="2026-07-01")])
    achados = gate.vencidos(tmp_path, hoje=HOJE)
    assert len(achados) == 1 and achados[0]["situacao"] == "vencido"


def test_par_fonte_tipo_e_obrigatorio(tmp_path):
    item = _item()
    item.pop("fonte")
    problemas = gate.validar(_caso(tmp_path, [item]), hoje=HOJE)
    assert any("falta 'fonte'" in p for p in problemas)


# ------------------------------------------------------- o que não mudou

def test_caso_sem_artefato_continua_aprovado(tmp_path):
    """Ausência nunca vira reprovação: a maioria dos casos não tem bloqueio."""
    assert gate.validar(tmp_path / "vazio", hoje=HOJE) == []


def test_sintoma_continua_reprovado_como_causa(tmp_path):
    caso = _caso(tmp_path, [_item(causa="não localizado")])
    problemas = gate.validar(caso, hoje=HOJE)
    assert any("descreve o sintoma" in p for p in problemas)


def test_bloqueio_sem_inventario_de_recebidos_continua_reprovado(tmp_path):
    caso = _caso(tmp_path, [_item()], recebidos=[])
    problemas = gate.validar(caso, hoje=HOJE)
    assert any("recebidos" in p for p in problemas)


def test_item_integro_passa(tmp_path):
    assert gate.validar(_caso(tmp_path, [_item()]), hoje=HOJE) == []


def test_prazo_no_limite_exato_passa(tmp_path):
    limite = (HOJE + timedelta(days=gate.REVALIDACAO_MAXIMA_DIAS)).isoformat()
    assert gate.validar(_caso(tmp_path, [_item(revalidarApos=limite)]), hoje=HOJE) == []
