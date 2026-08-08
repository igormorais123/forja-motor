# -*- coding: utf-8 -*-
"""forja_rotas_fonte.py — o que cada tribunal serve, por qual porta, e o que ele não serve.

Este módulo existe por causa de dois bloqueios falsos declarados no mesmo dia,
06 e 07/08/2026, com a mesma forma. Num deles a esteira anunciou ao titular, em
documento e em dois e-mails, que o inteiro teor de três acórdãos do STJ era
inalcançável pela automação; o obstáculo era um parâmetro de consulta. No outro,
o registro de um caso dizia havia semanas que uma decisão do STF dependia de
peticionamento eletrônico com procuração; a decisão tinha acesso aberto, e o que
faltava era o número de incidente.

Os dois erros têm a mesma causa e ela não é falta de esforço. Cada agente esgota
as rotas **que ele já conhece**, escreve "não há caminho", e a redação fechada
apaga o item da fila: ninguém reaudita o que já tem causa registrada. Faltava a
memória entre execuções — o registro do que alguém já conseguiu, com a armadilha
que quase o impediu.

Por isso o registro guarda as duas metades:

* as rotas que **funcionam**, com a chave exata e a armadilha que engana
  (``serve=True``). Elas transformam "tentei e não consegui" em algo conferível:
  o gate de insumo bloqueado reprova quem declara bloqueio sem ter tentado uma
  rota conhecida.
* os pares fonte × tipo que a fonte **não serve publicamente** (``serve=False``).
  Esta metade vale tanto quanto a outra. Ela é o que distingue
  ``indisponivel_na_fonte`` de ``limitacao_da_ferramenta``: quando o portal não
  divulga petição de parte alguma, o problema não é a nossa ferramenta, e chamá-lo
  assim manda o próximo agente procurar defeito onde não há.

``verificadoEm`` é data de conferência real, não de redação. Rota sem conferência
recente é palpite, e o comando ``--probe`` existe para que o registro não apodreça
em mais uma afirmação velha sobre o mundo.
"""
from __future__ import annotations

import argparse
import json
import ssl
import sys
import urllib.error
import urllib.request
from datetime import date, datetime

VERSAO = "FORJA-ROTAS-FONTE-v1"

# Prazo após o qual uma rota deixa de ser afirmação e volta a ser suposição.
# Portal de tribunal muda sem aviso, e o erro que este módulo combate nasceu
# justamente de tratar informação envelhecida como fato corrente.
VALIDADE_DIAS = 120

_UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
       "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")


ROTAS: dict[str, dict] = {
    # ------------------------------------------------------------------ STJ
    "stj-acordao-integra": {
        "fonte": "STJ",
        "tipoDocumento": "acordao",
        "serve": True,
        "url": ("https://processo.stj.jus.br/SCON/GetInteiroTeorDoAcordao"
                "?num_registro={num_registro}&dt_publicacao={dt_publicacao}"),
        "chaves": {
            "num_registro": "14 dígitos, SEM barra e SEM hífen (2023/0066594-7 vira 202300665947)",
            "dt_publicacao": "DD/MM/AAAA, a data exata de publicação no Diário",
        },
        "armadilha": ("data errada devolve HTTP 200 com o texto 'Acórdão não encontrado', "
                      "e não um erro. A primeira tentativa parece resposta definitiva. "
                      "O número de registro sai do DJEN junto com a data de DIVULGAÇÃO; "
                      "varra duas semanas a partir dela e pare na primeira resposta acima "
                      "de 500 bytes"),
        "observacao": ("funciona nos dias em que a busca textual do SCON cai com erro do "
                       "mecanismo Oracle, porque é outro serviço"),
        "probe": {"num_registro": "202300665947", "dt_publicacao": "15/06/2026",
                  "esperaTipo": "application/pdf", "minimoBytes": 50000},
        "verificadoEm": "2026-08-07",
    },
    "stj-peticao-de-parte": {
        "fonte": "STJ",
        "tipoDocumento": "peticao_de_parte",
        "serve": False,
        "porQue": ("a consulta pública lista número e data das petições e não entrega o "
                   "documento. Existe rota autenticada — Ciência Antecipada no portal de "
                   "peticionamento —, que recusa com 'Usuário logado não é "
                   "Parte(Ente)/Advogado do processo!' quando a OAB autenticada não está "
                   "habilitada naqueles autos"),
        "causaCorreta": "sem_habilitacao_nos_autos",
        "causasAdmissiveis": ("sem_habilitacao_nos_autos", "indisponivel_na_fonte"),
        "condicao": ("só vale quando somos parte no processo. Se não somos, a causa é "
                     "indisponivel_na_fonte e não há diligência de habilitação a fazer"),
        "verificadoEm": "2026-07-12",
    },
    # ------------------------------------------------------------------ STF
    "stf-incidente-por-classe-numero": {
        "fonte": "STF",
        "tipoDocumento": "localizador",
        "serve": True,
        "url": ("https://portal.stf.jus.br/processos/listarProcessos.asp"
                "?classe={classe}&numeroProcesso={numero}"),
        "chaves": {"classe": "sigla da classe, por exemplo RE ou ARE",
                   "numero": "número do processo, só dígitos"},
        "armadilha": ("o portal não trabalha por classe e número nas abas internas: tudo "
                      "depende do 'incidente', que só aparece no HTML desta busca, em "
                      "'incidente=NNNNNNN'. Sem ele nada mais funciona, e é este o "
                      "localizador que costuma faltar nos nossos registros"),
        "probe": {"classe": "RE", "numero": "1395147",
                  "esperaTexto": "incidente=", "minimoBytes": 10000},
        "verificadoEm": "2026-08-07",
    },
    "stf-abas-do-processo": {
        "fonte": "STF",
        "tipoDocumento": "andamentos",
        "serve": True,
        "url": "https://portal.stf.jus.br/processos/{aba}.asp?incidente={incidente}",
        "chaves": {"aba": "abaInformacoes, abaAndamentos, abaPeticoes ou abaDecisoes",
                   "incidente": "obtido por stf-incidente-por-classe-numero"},
        "armadilha": ("sem os cabeçalhos Referer apontando para detalhe.asp do mesmo "
                      "incidente e X-Requested-With: XMLHttpRequest, todas as abas "
                      "devolvem HTTP 403. O 403 parece bloqueio de robô e é só cabeçalho"),
        "probe": {"aba": "abaDecisoes", "incidente": "6454003",
                  "esperaTexto": "downloadPeca", "minimoBytes": 5000},
        "verificadoEm": "2026-08-07",
    },
    "stf-decisao-ou-acordao-peca": {
        "fonte": "STF",
        "tipoDocumento": "decisao",
        "serve": True,
        "url": "https://portal.stf.jus.br/processos/downloadPeca.asp?id={id}&ext=.pdf",
        "chaves": {"id": "id numérico que aparece em downloadPeca.asp?id=... dentro das abas"},
        "armadilha": ("exige Referer de detalhe.asp. Serve o PDF sem autenticação e sem "
                      "procuração: decisão monocrática, acórdão, intimação e termo de "
                      "autuação saem por aqui"),
        "probe": {"id": "15388803672", "esperaTipo": "application/pdf", "minimoBytes": 50000},
        "verificadoEm": "2026-08-07",
    },
    "stf-peticao-de-parte": {
        "fonte": "STF",
        "tipoDocumento": "peticao_de_parte",
        "serve": False,
        "porQue": ("a aba de petições traz número, data e unidade de recebimento, e "
                   "nenhum link de documento — para nenhuma parte. Conferido num processo "
                   "com dezoito petições de quatro partes distintas: zero downloads"),
        "causaCorreta": "indisponivel_na_fonte",
        "causasAdmissiveis": ("indisponivel_na_fonte",),
        "condicao": ("não confunda com falta de habilitação nossa: a restrição é uniforme "
                     "e não é dirigida a ninguém. Registrar como limitacao_da_ferramenta "
                     "manda o próximo agente caçar defeito inexistente"),
        "verificadoEm": "2026-08-07",
    },
    # ----------------------------------------------------------------- DJEN
    "djen-comunicacao-por-processo": {
        "fonte": "DJEN",
        "tipoDocumento": "comunicacao",
        "serve": True,
        "url": ("https://comunicaapi.pje.jus.br/api/v1/comunicacao"
                "?numeroProcesso={numero_unico}&itensPorPagina=50"),
        "chaves": {"numero_unico": "CNJ com 20 dígitos, sem pontuação"},
        "armadilha": ("devolve o texto integral da comunicação, o que inclui dispositivo "
                      "de acórdão e decisão monocrática publicados. É a porta que funciona "
                      "quando a busca de jurisprudência do tribunal está fora do ar, mas "
                      "não traz ementa nem voto"),
        "probe": {"numero_unico": "50197289020104047000",
                  "esperaTexto": "\"", "minimoBytes": 2},
        "verificadoEm": "2026-08-07",
    },
}


def _hoje() -> date:
    return date.today()


def _data(valor) -> date | None:
    try:
        return datetime.strptime(str(valor), "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return None


def rotas_para(fonte: str, tipo_documento: str) -> dict[str, dict]:
    """Rotas registradas para um par fonte × tipo, com a chave do registro."""
    f = str(fonte or "").strip().casefold()
    t = str(tipo_documento or "").strip().casefold()
    return {k: v for k, v in ROTAS.items()
            if str(v["fonte"]).casefold() == f
            and str(v["tipoDocumento"]).casefold() == t}


def rotas_que_servem(fonte: str, tipo_documento: str) -> dict[str, dict]:
    return {k: v for k, v in rotas_para(fonte, tipo_documento).items() if v.get("serve")}


def nao_servida(fonte: str, tipo_documento: str) -> dict | None:
    """A entrada negativa, quando existe: a fonte não entrega esse tipo.

    Devolver isto é o que permite ao gate corrigir a causa declarada em vez de
    apenas reprovar — a diferença entre dizer 'está errado' e dizer 'o certo é
    indisponivel_na_fonte, e a razão é esta'.
    """
    for v in rotas_para(fonte, tipo_documento).values():
        if v.get("serve") is False:
            return v
    return None


def nao_tentadas(fonte: str, tipo_documento: str, tentadas) -> list[str]:
    """Rotas conhecidas que funcionam e que não constam das tentativas.

    É o coração do gate: enquanto sobrar uma rota conhecida sem tentativa, o
    bloqueio ainda não foi diagnosticado. Foi exatamente a lacuna dos dois erros
    de 06 e 07/08/2026.
    """
    ja = {str(x).strip() for x in (tentadas or []) if str(x).strip()}
    return sorted(k for k in rotas_que_servem(fonte, tipo_documento) if k not in ja)


def desatualizadas(hoje: date | None = None) -> list[str]:
    """Rotas cuja conferência passou da validade — suposição, não fato."""
    ref = hoje or _hoje()
    fora = []
    for chave, rota in ROTAS.items():
        d = _data(rota.get("verificadoEm"))
        if d is None or (ref - d).days > VALIDADE_DIAS:
            fora.append(chave)
    return sorted(fora)


def _abrir(url: str, timeout: int = 60):
    cabecalhos = {"User-Agent": _UA}
    if "portal.stf.jus.br" in url:
        # As abas do STF respondem 403 sem estes dois. O 403 engana: parece
        # bloqueio deliberado a robô e é exigência de cabeçalho.
        cabecalhos["Referer"] = "https://portal.stf.jus.br/processos/detalhe.asp"
        cabecalhos["X-Requested-With"] = "XMLHttpRequest"
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return urllib.request.urlopen(
        urllib.request.Request(url, headers=cabecalhos), context=ctx, timeout=timeout)


def probe(chave: str, timeout: int = 60) -> dict:
    """Exercita de verdade uma rota que serve, e devolve o veredito.

    Sem isto o registro vira o mesmo tipo de afirmação envelhecida que ele
    existe para combater.
    """
    rota = ROTAS.get(chave)
    if rota is None:
        return {"rota": chave, "ok": False, "erro": "rota desconhecida"}
    if not rota.get("serve"):
        return {"rota": chave, "ok": None,
                "nota": "entrada negativa: não há o que exercitar, ela afirma ausência"}
    amostra = dict(rota.get("probe") or {})
    if not amostra:
        return {"rota": chave, "ok": None, "nota": "sem amostra de conferência"}
    espera_tipo = amostra.pop("esperaTipo", None)
    espera_texto = amostra.pop("esperaTexto", None)
    minimo = int(amostra.pop("minimoBytes", 1) or 1)
    try:
        url = rota["url"].format(**amostra)
    except KeyError as e:
        return {"rota": chave, "ok": False, "erro": f"amostra não preenche {e}"}
    try:
        resposta = _abrir(url, timeout=timeout)
        corpo = resposta.read()
    except (urllib.error.URLError, OSError, ValueError) as e:
        return {"rota": chave, "ok": False, "erro": f"{type(e).__name__}: {e}"}
    tipo = resposta.headers.get("Content-Type") or ""
    veredito = {"rota": chave, "ok": True, "bytes": len(corpo), "contentType": tipo}
    if len(corpo) < minimo:
        veredito.update(ok=False, erro=f"resposta menor que o mínimo ({len(corpo)} < {minimo})")
    if espera_tipo and espera_tipo not in tipo:
        veredito.update(ok=False, erro=f"Content-Type inesperado: {tipo!r}")
    if espera_texto and espera_texto.encode("utf-8") not in corpo:
        veredito.update(ok=False, erro=f"resposta não contém {espera_texto!r}")
    return veredito


def main(argv=None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--fonte")
    p.add_argument("--tipo")
    p.add_argument("--probe", action="store_true",
                   help="exercita de verdade cada rota que serve e atualiza o veredito")
    p.add_argument("--json", action="store_true")
    a = p.parse_args(argv)

    if a.probe:
        alvos = [k for k, v in ROTAS.items() if v.get("serve")]
        if a.fonte:
            alvos = [k for k in alvos
                     if str(ROTAS[k]["fonte"]).casefold() == a.fonte.casefold()]
        resultados = [probe(k) for k in alvos]
        if a.json:
            print(json.dumps(resultados, ensure_ascii=False, indent=2))
        else:
            for r in resultados:
                marca = "ok " if r.get("ok") else "FALHOU"
                print(f"  {marca} {r['rota']}: {r.get('erro') or str(r.get('bytes')) + ' bytes'}")
        velhas = desatualizadas()
        if velhas:
            print(f"\n  conferência vencida (> {VALIDADE_DIAS} dias): {', '.join(velhas)}")
        return 0 if all(r.get("ok") is not False for r in resultados) else 1

    selecao = ROTAS
    if a.fonte:
        selecao = {k: v for k, v in selecao.items()
                   if str(v["fonte"]).casefold() == a.fonte.casefold()}
    if a.tipo:
        selecao = {k: v for k, v in selecao.items()
                   if str(v["tipoDocumento"]).casefold() == a.tipo.casefold()}
    if a.json:
        print(json.dumps({"schema": VERSAO, "rotas": selecao}, ensure_ascii=False, indent=2))
        return 0
    for chave, rota in selecao.items():
        marca = "SERVE" if rota.get("serve") else "NAO SERVE"
        print(f"[{marca}] {chave}  ({rota['fonte']} / {rota['tipoDocumento']})")
        if rota.get("serve"):
            print(f"    {rota['url']}")
            print(f"    armadilha: {rota['armadilha']}")
        else:
            print(f"    por quê: {rota['porQue']}")
            print(f"    causa correta: {rota['causaCorreta']}")
            print(f"    condição: {rota['condicao']}")
        print(f"    conferido em {rota.get('verificadoEm')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
