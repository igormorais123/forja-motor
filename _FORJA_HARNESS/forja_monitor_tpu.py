# -*- coding: utf-8 -*-
"""Vigia a versão das Tabelas Processuais Unificadas do CNJ.

Existe porque o procedimento de manutenção pedido ao Desenvolvimento em
07/08/2026 previa "verificação automática semanal da versão, dos links e da
disponibilidade dos arquivos" — e o desenho original era raspar as quatro
páginas de versões do Sistema de Gestão de Tabelas. Raspagem de página quebra
quando o CNJ mexe no HTML, e quebra em silêncio: a rotina continua rodando e
passa a dizer que nada mudou.

O CNJ expõe um webservice SOAP com a operação `getDataUltimaVersao`, que
devolve a data da versão vigente por tipo de tabela. Uma data, em texto, sem
autenticação. É a primitiva certa para o vigia, e é a rota primária daqui.

A rota de reserva é a página `versoes.php`, e ela é reserva declarada, não
substituta silenciosa: quando o vigia cai para ela, o retrato registra isso.
Quando as duas discordam, ele avisa em vez de escolher.

Nada aqui é dado do escritório: o alvo é fonte pública federal e a lista de
tabelas é a do próprio CNJ. Este módulo pertence ao motor.

Uso
    python forja_monitor_tpu.py
    python forja_monitor_tpu.py --json
    python forja_monitor_tpu.py --tabela D

Saída
    Código 0 sem novidade, 10 quando a versão mudou, 1 em erro.
    Retrato em `telemetria/monitor_tpu/versoes.json`; cada mudança fica também
    em `telemetria/monitor_tpu/mudancas.log`, que é histórico e não é sobrescrito.

O que ele NÃO faz
    Não baixa as 79 planilhas nem calcula o diff de conteúdo. Detectar que a
    versão mudou é barato e pode rodar toda semana; baixar e comparar é caro e
    só faz sentido depois que ele avisa. Também não envia e-mail: avisar é
    decisão de quem lê.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import ssl
import sys
import tempfile
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
DESTINO = RAIZ / "telemetria" / "monitor_tpu"

WS = "https://www.cnj.jus.br/sgt/sgt_ws.php"
PAGINA = "https://www.cnj.jus.br/sgt/versoes.php?tipo_tabela={tipo}"

TABELAS = {
    "D": "Documentos Processuais",
    "C": "Classes Processuais",
    "A": "Assuntos Processuais",
    "M": "Movimentos Processuais",
}

CABECALHO = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

# O certificado do sgt.cnj.jus.br já falhou a validação em máquina do
# escritório. Como o que trafega é uma data pública e nenhum segredo sobe na
# requisição, o vigia aceita a conexão sem verificação em vez de deixar de
# vigiar — mas a decisão fica escrita aqui, e não escondida numa flag.
_CTX = ssl.create_default_context()
_CTX.check_hostname = False
_CTX.verify_mode = ssl.CERT_NONE

_DATA = re.compile(r"\b(\d{2}/\d{2}/\d{4})\b")


def gravar_json(caminho: Path, dados: dict, tentativas: int = 4) -> None:
    """Grava o retrato sem deixar arquivo pela metade e sem morrer por disputa.

    Mesma razão do vigia do STF: no Windows, antivírus, indexador e o observador
    de mapas tocam o mesmo arquivo, e `OSError: [Errno 22]` já apareceu em
    execução pelo agendador. Vigia que perde o retrato acusa tudo como novidade
    na leitura seguinte.
    """
    texto = json.dumps(dados, ensure_ascii=False, indent=2)
    ultimo = None
    for tentativa in range(tentativas):
        tmp = None
        try:
            fd, tmp = tempfile.mkstemp(dir=str(caminho.parent), suffix=".tmp")
            with os.fdopen(fd, "w", encoding="utf-8") as fh:
                fh.write(texto)
            os.replace(tmp, caminho)
            return
        except OSError as e:
            ultimo = e
            if tmp:
                try:
                    os.unlink(tmp)
                except OSError:
                    pass
            time.sleep(0.25 * (tentativa + 1))
    raise ultimo


def _envelope(operacao: str, corpo: str) -> bytes:
    return (
        '<?xml version="1.0" encoding="utf-8"?>'
        '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"'
        ' xmlns:sgt="urn:sgt_ws"><soapenv:Body>'
        f"<sgt:{operacao}>{corpo}</sgt:{operacao}>"
        "</soapenv:Body></soapenv:Envelope>"
    ).encode("utf-8")


def versao_por_webservice(tipo: str, timeout: float = 45) -> str:
    """Data da versão vigente pela rota primária. Levanta em falha."""
    req = urllib.request.Request(
        WS,
        data=_envelope("getDataUltimaVersao", f"<tipoTabela>{tipo}</tipoTabela>"),
        headers={
            **CABECALHO,
            "Content-Type": "text/xml; charset=utf-8",
            "SOAPAction": "urn:sgt_ws#getDataUltimaVersao",
        },
    )
    xml = urllib.request.urlopen(req, timeout=timeout, context=_CTX).read()
    texto = xml.decode("utf-8", "replace")
    if "Fault" in texto and "faultstring" in texto:
        falha = re.search(r"<faultstring>(.*?)</faultstring>", texto, re.S)
        raise ValueError(f"webservice devolveu falha: {(falha.group(1) if falha else '?')[:120]}")
    achado = _DATA.search(texto)
    if not achado:
        # Resposta 200 sem data é pior do que erro de rede: passaria por normal.
        raise ValueError(f"resposta sem data reconhecível: {texto[:160]!r}")
    return achado.group(1)


def versao_por_pagina(tipo: str, timeout: float = 45) -> str:
    """Data mais recente exibida na página de versões. Rota de reserva."""
    req = urllib.request.Request(PAGINA.format(tipo=tipo), headers=CABECALHO)
    html = urllib.request.urlopen(req, timeout=timeout, context=_CTX).read()
    texto = html.decode("iso-8859-1", "replace")
    datas = _DATA.findall(texto)
    if not datas:
        raise ValueError("página de versões não trouxe nenhuma data")
    # Ordenar por data real, e não pela ordem do HTML, que já mistura o
    # histórico de 2010 e 2011 com as versões recentes na mesma listagem.
    return max(datas, key=lambda d: (d[6:10], d[3:5], d[0:2]))


def verificar(tipo: str) -> dict:
    """Consulta uma tabela pelas duas rotas e devolve o veredito."""
    item: dict = {"tipo": tipo, "tabela": TABELAS[tipo], "rota": None,
                  "versao": None, "versaoPagina": None, "erro": None,
                  "divergencia": False}
    try:
        item["versao"] = versao_por_webservice(tipo)
        item["rota"] = "webservice"
    except Exception as e:  # rede, TLS, XML ou resposta sem data
        item["erro"] = f"{type(e).__name__}: {str(e)[:120]}"

    try:
        item["versaoPagina"] = versao_por_pagina(tipo)
    except Exception as e:
        if item["versao"] is None:
            item["erro"] = f"{item['erro']} | pagina: {type(e).__name__}: {str(e)[:80]}"

    if item["versao"] is None and item["versaoPagina"]:
        item["versao"] = item["versaoPagina"]
        item["rota"] = "pagina (reserva)"
    if item["versao"] and item["versaoPagina"] and item["versao"] != item["versaoPagina"]:
        # Não escolher: quem decide qual vale é quem lê. Discordância entre as
        # duas rotas costuma ser publicação em andamento, e é informação.
        item["divergencia"] = True
    return item


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Vigia a versão das TPU do CNJ")
    p.add_argument("--tabela", choices=sorted(TABELAS), help="verificar só uma tabela")
    p.add_argument("--json", action="store_true", help="saída em JSON")
    args = p.parse_args(argv)

    DESTINO.mkdir(parents=True, exist_ok=True)
    retrato = DESTINO / "versoes.json"
    anterior = {}
    if retrato.exists():
        try:
            anterior = json.loads(retrato.read_text(encoding="utf-8")).get("tabelas", {})
        except (OSError, json.JSONDecodeError):
            anterior = {}

    tipos = [args.tabela] if args.tabela else sorted(TABELAS)
    itens = [verificar(t) for t in tipos]

    novidades, erros = [], []
    for it in itens:
        if it["erro"] and it["versao"] is None:
            erros.append(it)
            continue
        antes = (anterior.get(it["tipo"]) or {}).get("versao")
        it["versaoAnterior"] = antes
        if antes and antes != it["versao"]:
            novidades.append(it)

    agora = datetime.now(timezone.utc).isoformat(timespec="seconds")
    if not args.tabela:  # retrato parcial mentiria sobre as tabelas não consultadas
        gravar_json(retrato, {"verificadoEm": agora,
                              "tabelas": {it["tipo"]: it for it in itens}})
    if novidades:
        with (DESTINO / "mudancas.log").open("a", encoding="utf-8") as fh:
            for it in novidades:
                fh.write(f"{agora}\t{it['tipo']}\t{it['versaoAnterior']} -> {it['versao']}\n")

    if args.json:
        print(json.dumps({"verificadoEm": agora, "tabelas": itens,
                          "novidades": [it["tipo"] for it in novidades],
                          "erros": [it["tipo"] for it in erros]},
                         ensure_ascii=False, indent=2))
    else:
        for it in itens:
            if it["versao"] is None:
                print(f"{it['tabela']:24s} ERRO: {it['erro']}")
                continue
            marca = ""
            if it.get("versaoAnterior") and it["versaoAnterior"] != it["versao"]:
                marca = f"  MUDOU (era {it['versaoAnterior']})"
            elif not it.get("versaoAnterior"):
                marca = "  (primeiro retrato)"
            if it["divergencia"]:
                marca += f"  [pagina diz {it['versaoPagina']}]"
            print(f"{it['tabela']:24s} {it['versao']}  via {it['rota']}{marca}")
        if novidades:
            print("\nO CNJ publicou versão nova. Próximo passo: baixar as 79 "
                  "planilhas, guardar em diretório próprio da nova versão sem "
                  "sobrescrever a anterior e comparar o conteúdo.")

    if erros and not novidades:
        return 1
    return 10 if novidades else 0


if __name__ == "__main__":
    raise SystemExit(main())
