# -*- coding: utf-8 -*-
"""Regressão do vigia das TPU do CNJ.

Nada aqui toca a rede: o que precisa ser garantido é o comportamento diante das
respostas, e essas ficam como fixture. As duas primeiras são captura real do
webservice e da página em 09/08/2026.

O caso que mais importa é o `_sem_data`: resposta HTTP 200 que não traz data
nenhuma. Sem tratamento explícito, ela viraria "nada mudou" e o vigia passaria
anos calado enquanto a fonte mudava de formato — que é exatamente o modo de
falha silenciosa pelo qual a raspagem de página foi descartada.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

import forja_monitor_tpu as mt  # noqa: E402

RESPOSTA_WS = (
    '<?xml version="1.0" encoding="UTF-8"?>'
    '<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">'
    "<SOAP-ENV:Body><ns1:getDataUltimaVersaoResponse>"
    '<return xsi:type="xsd:string">26/05/2026</return>'
    "</ns1:getDataUltimaVersaoResponse></SOAP-ENV:Body></SOAP-ENV:Envelope>"
)

RESPOSTA_FALHA = (
    '<?xml version="1.0"?><SOAP-ENV:Envelope '
    'xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"><SOAP-ENV:Body>'
    "<SOAP-ENV:Fault><faultcode>SOAP-ENV:Server</faultcode>"
    "<faultstring>tipo de tabela invalido</faultstring>"
    "</SOAP-ENV:Fault></SOAP-ENV:Body></SOAP-ENV:Envelope>"
)

# A listagem real mistura o histórico antigo com as versões recentes, e não vem
# ordenada. Se o vigia pegar a primeira data do HTML, devolve 2010.
PAGINA_REAL = (
    "<table><tr><td>08/09/2010</td></tr><tr><td>30/12/2011</td></tr>"
    "<tr><td>15/04/2026</td></tr><tr><td>26/05/2026</td></tr></table>"
)


class _Resposta:
    def __init__(self, corpo: str, enc: str = "utf-8"):
        self._b = corpo.encode(enc)

    def read(self):
        return self._b

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def test_webservice_devolve_a_data(monkeypatch):
    monkeypatch.setattr(mt.urllib.request, "urlopen",
                        lambda *a, **k: _Resposta(RESPOSTA_WS))
    assert mt.versao_por_webservice("D") == "26/05/2026"


def test_webservice_em_falha_levanta(monkeypatch):
    monkeypatch.setattr(mt.urllib.request, "urlopen",
                        lambda *a, **k: _Resposta(RESPOSTA_FALHA))
    with pytest.raises(ValueError, match="falha"):
        mt.versao_por_webservice("Z")


def test_resposta_200_sem_data_nao_passa_por_normal(monkeypatch):
    monkeypatch.setattr(mt.urllib.request, "urlopen",
                        lambda *a, **k: _Resposta("<html>manutencao</html>"))
    with pytest.raises(ValueError, match="sem data"):
        mt.versao_por_webservice("D")


def test_pagina_escolhe_a_data_mais_recente_e_nao_a_primeira(monkeypatch):
    monkeypatch.setattr(mt.urllib.request, "urlopen",
                        lambda *a, **k: _Resposta(PAGINA_REAL, "iso-8859-1"))
    assert mt.versao_por_pagina("D") == "26/05/2026"


def test_cai_para_a_pagina_e_declara_a_rota(monkeypatch):
    monkeypatch.setattr(mt, "versao_por_webservice",
                        lambda *a, **k: (_ for _ in ()).throw(OSError("timeout")))
    monkeypatch.setattr(mt, "versao_por_pagina", lambda *a, **k: "26/05/2026")
    item = mt.verificar("D")
    assert item["versao"] == "26/05/2026"
    assert item["rota"] == "pagina (reserva)"
    assert item["erro"], "queda para a reserva tem de ficar registrada"


def test_divergencia_entre_rotas_e_reportada_sem_escolher(monkeypatch):
    monkeypatch.setattr(mt, "versao_por_webservice", lambda *a, **k: "26/05/2026")
    monkeypatch.setattr(mt, "versao_por_pagina", lambda *a, **k: "01/07/2026")
    item = mt.verificar("D")
    assert item["divergencia"] is True
    assert item["versao"] == "26/05/2026" and item["versaoPagina"] == "01/07/2026"


def _saida(destino: Path) -> dict:
    return json.loads((destino / "versoes.json").read_text(encoding="utf-8"))


def test_primeiro_retrato_nao_e_novidade(monkeypatch, tmp_path):
    monkeypatch.setattr(mt, "DESTINO", tmp_path)
    monkeypatch.setattr(mt, "verificar", lambda t: {
        "tipo": t, "tabela": mt.TABELAS[t], "rota": "webservice",
        "versao": "26/05/2026", "versaoPagina": "26/05/2026",
        "erro": None, "divergencia": False})
    assert mt.main([]) == 0
    assert _saida(tmp_path)["tabelas"]["D"]["versao"] == "26/05/2026"


def test_versao_nova_devolve_10_e_registra(monkeypatch, tmp_path):
    monkeypatch.setattr(mt, "DESTINO", tmp_path)
    tmp_path.mkdir(exist_ok=True)
    (tmp_path / "versoes.json").write_text(json.dumps({"tabelas": {
        t: {"tipo": t, "versao": "15/04/2026"} for t in mt.TABELAS}}),
        encoding="utf-8")
    monkeypatch.setattr(mt, "verificar", lambda t: {
        "tipo": t, "tabela": mt.TABELAS[t], "rota": "webservice",
        "versao": "26/05/2026", "versaoPagina": "26/05/2026",
        "erro": None, "divergencia": False})
    assert mt.main([]) == 10
    log = (tmp_path / "mudancas.log").read_text(encoding="utf-8")
    assert "15/04/2026 -> 26/05/2026" in log
    assert len(log.strip().splitlines()) == 4, "uma linha por tabela"


def test_erro_total_nao_vira_silencio(monkeypatch, tmp_path):
    monkeypatch.setattr(mt, "DESTINO", tmp_path)
    monkeypatch.setattr(mt, "verificar", lambda t: {
        "tipo": t, "tabela": mt.TABELAS[t], "rota": None, "versao": None,
        "versaoPagina": None, "erro": "OSError: timeout", "divergencia": False})
    assert mt.main([]) == 1


def test_consulta_de_uma_tabela_nao_sobrescreve_o_retrato(monkeypatch, tmp_path):
    """Retrato parcial mentiria sobre as três tabelas não consultadas."""
    monkeypatch.setattr(mt, "DESTINO", tmp_path)
    tmp_path.mkdir(exist_ok=True)
    antes = {"verificadoEm": "x", "tabelas": {
        t: {"tipo": t, "versao": "26/05/2026"} for t in mt.TABELAS}}
    (tmp_path / "versoes.json").write_text(json.dumps(antes), encoding="utf-8")
    monkeypatch.setattr(mt, "verificar", lambda t: {
        "tipo": t, "tabela": mt.TABELAS[t], "rota": "webservice",
        "versao": "26/05/2026", "versaoPagina": "26/05/2026",
        "erro": None, "divergencia": False})
    assert mt.main(["--tabela", "D"]) == 0
    assert _saida(tmp_path) == antes
