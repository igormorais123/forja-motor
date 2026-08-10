"""Censo de casos: a única leitura que responde sobre a população inteira.

Por que este módulo existe
--------------------------
Em 09/08/2026 o titular cobrou que demandas dele não eram feitas e que a esteira
dava por cumprido o que estava pela metade. A medição mostrou algo pior e mais
específico do que a queixa: **não havia como saber**. Três defeitos somados:

1. Cada superfície de leitura enxergava uma fração e anunciava o total.
   `forja_fila.py` devolvia "4 prontas" sobre 89 casos porque só lê o esquema
   `FORJA_N3_STATE.json`; 60 casos gravam apenas o legado `FORJA_STATE.json`.
   `forja_axi.py` anunciava "28 of 28 total" sobre a mesma população — corrigido
   no mesmo dia, e a correção de um leitor não conserta a classe.

2. Os dois esquemas parecem discordar sobre o mesmo caso — e a medição de
   10/08/2026 mostrou que a pergunta estava mal feita. O exemplo que este texto
   trazia, `fulfilled` contra `fulfilled_by_forja_f10`, é a mesma situação em
   dois vocabulários, e a decisão de situação, logo abaixo, sempre os tratou como
   equivalentes. Dos 17 casos acusados de divergir, 5 eram só isso. Os outros 12
   têm o N3 em `mode: shadow`, declarado no manifesto do caso: **sombra não é um
   segundo registro da verdade, é o diário do executor**, e só sabe o que passou
   pelo runner. Cobrar coerência entre os dois era erro de categoria, e a
   acusação de divergência escondia o único achado real — um carimbo de cumprido
   sem prova nenhuma.

3. `fulfilled` significa duas coisas incompatíveis: "entregue" e "triado, não
   havia demanda". Como a palavra é a mesma, um caso substantivo abandonado é
   indistinguível de um e-mail administrativo corretamente descartado. Foi isso
   que produziu a experiência de "dado como feito".

O que este módulo faz de diferente
----------------------------------
- **Lê os dois esquemas e declara o denominador.** Nenhuma saída daqui informa
  quantidade sem informar sobre quantos casos ela foi apurada. Fração anunciada
  como total é o defeito que este arquivo existe para tornar impossível.

- **Conclusão exige prova, e a prova é o arquivo em disco.** Um caso só é
  `entregue` se houver entregável na pasta da demanda, com tamanho e hash. Note
  que a prova vive na pasta da demanda, **não** na pasta de estado: procurar no
  lugar errado foi o erro que quase fez este módulo nascer com o diagnóstico
  invertido.

- **Não inventa a distinção que não pode aferir.** A máquina não sabe se um
  caso sem entregável era lixo de ingestão ou trabalho abandonado. Então ela não
  chuta: classifica como `concluido_sem_prova` e exige declaração humana em
  `CENSO_RESOLUCOES.json`. Mesmo desenho de `forja_insumo_bloqueado.py` — causa
  em vocabulário fechado, declarada por quem sabe.

- **Idade honesta.** Mede do primeiro carimbo da fase corrente, nunca de
  `updatedAt`, que é reescrito por varredura e faz todo caso ler zero dia.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path

FORJA = Path(__file__).resolve().parent
WORKSPACE = FORJA.parent
STATE = FORJA / "state"
RESOLUCOES = STATE / "CENSO_RESOLUCOES.json"
CONFERENCIAS = STATE / "CENSO_CONFERENCIAS.json"

VERSAO = "FORJA-CENSO-v1"

# Vocabulário fechado. Situação fora desta tupla é erro de programação, não
# dado novo — pelo mesmo motivo que a causa de insumo bloqueado é fechada:
# rótulo livre deixa quem lê descobrindo sozinho qual era o problema.
SITUACOES = (
    "entregue",             # terminal com prova em disco
    "entrega_conferida",    # localizador conferido na fonte, com data e destinatário
    "entrega_declarada",    # sem artefato, mas com localizador conferível (ver abaixo)
    "triado_sem_demanda",   # terminal sem entregável, declarado por pessoa
    "aguardando_humano",    # esperando leitura, revisão ou ciência
    "bloqueado",            # impedimento declarado
    "aberto",               # trabalho por fazer
    "concluido_sem_prova",  # diz-se cumprido, sem artefato, sem localizador, sem declaração
    "ilegivel",             # o estado não pôde ser lido
)

# Situações que ainda devem alguma coisa a alguém. `entrega_declarada` está aqui
# de propósito: ela é conferível e não foi conferida, o que é dívida de auditoria
# e não de trabalho.
DEVENDO = ("aberto", "aguardando_humano", "bloqueado", "entrega_declarada",
           "concluido_sem_prova", "ilegivel")

# `deliveryEvidence` guarda o que o painel registrou sobre a entrega. Ele existe
# em 83 dos 89 casos legíveis — proporção que sozinha o desqualifica como prova,
# porque carimbo aplicado a 93% da população é padrão, não evidência. O que
# separa os dois é o **localizador**: 74 desses registros citam o identificador
# da mensagem enviada, que é conferível contra a caixa; 9 são prosa, que não é.
# A distinção nasceu de um quase-erro: eu ia perguntar ao titular do escritório
# se 19 demandas tinham sido entregues, e 19 traziam o ID do e-mail em que foram.
#
# Localizador tem mais de um alfabeto, e reconhecer um só é a mesma falha por
# outro lado. Medido em 10/08/2026 sobre as 88 pastas com estado: 77 registros
# citam o ID do Gmail, 1 cita o ID da mensagem do WhatsApp, 1 cita o arquivo
# entregue e 5 são prosa. Enquanto só o dialeto do Gmail contava, os dois
# primeiros caíam em `concluido_sem_prova` — P0 de "diz-se cumprido sem nada" —
# tendo prova conferível registrada. Gate que não sabe ler a prova não deve
# escolher a acusação mais grave.
_GMAIL = re.compile(r"\b(?:19[0-9a-f]{14}|[0-9a-f]{16})\b")
_WHATSAPP = re.compile(r"\b3[A-F0-9]{15,31}\b")
# O caminho só vale se o arquivo existir agora: citado e ausente é prosa com
# aparência de prova, que é pior do que prosa. Quase toda pasta desta casa tem
# espaço no nome, então o padrão precisa atravessá-los — e, por atravessar,
# arrasta as palavras da frase antes do caminho. Daí `_caminho_citado` ir
# descascando token a token: quem decide é o disco, não o recorte.
_ARQUIVO = re.compile(
    r"(?:[\w\-–—()\[\]&+.]+[ /\\])*[\w\-–—()\[\]&+.]+\.(?:docx|pdf|zip|md)\b", re.I)

_TERMINAIS = {"fulfilled", "fulfilled_by_forja_f10", "complete", "delivered", "closed",
              "superseded", "cumprida"}
_BLOQUEADOS = {"blocked", "bloqueada"}
_AGUARDANDO = {"draft_awaiting_review", "ready", "awaiting_review", "aguardando_revisao"}

# Divergência se apura por sentido, nunca por texto. Os dois esquemas nasceram
# em épocas diferentes e escrevem a mesma coisa com palavras diferentes:
# `fulfilled` e `fulfilled_by_forja_f10` são o mesmo estado, e a própria decisão
# de situação, logo acima, já os trata assim. Comparar as cadeias cruas
# contradizia esta linha algumas dezenas de linhas adiante. Medido em
# 10/08/2026: de 17 casos acusados de divergir, 4 eram só isto.
_CLASSES = (("terminal", _TERMINAIS), ("bloqueado", _BLOQUEADOS),
            ("aguardando", _AGUARDANDO))


def _classe(estado) -> str:
    e = str(estado or "").strip()
    for nome, conjunto in _CLASSES:
        if e in conjunto:
            return nome
    return e or "vazio"

_ENTREGAVEL = {".docx", ".pdf"}
_TAMANHO_MINIMO = 20_000  # abaixo disso é rascunho, gabarito ou placeholder

# "PRAZO 04 08 -", "prazo 30 07 -", "PRAZO 03 8 -": a pasta da demanda carrega o
# prazo no nome, e era a única fonte estruturada de prazo que a esteira tinha.
_PRAZO = re.compile(r"\bPRAZO\s+(\d{1,2})\s*[./ ]\s*(\d{1,2})\b", re.I)


class CensoError(RuntimeError):
    pass


def _ler_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError):
        return None


def _dt(valor) -> datetime | None:
    if not valor:
        return None
    try:
        d = datetime.fromisoformat(str(valor).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None
    return d if d.tzinfo else d.replace(tzinfo=timezone.utc)


def _idade_da_fase(legado: dict | None) -> tuple[int | None, str | None]:
    """Dias desde o PRIMEIRO carimbo da fase corrente.

    `updatedAt` não serve: cada varredura o reescreve, e por isso todo caso da
    casa lia zero dia, inclusive um parado desde 11/07.
    """
    if not legado:
        return None, None
    fase = legado.get("currentPhase") or legado.get("faseAtual")
    marcas = [_dt(e.get("at")) for e in (legado.get("phaseHistory") or [])
              if e.get("phase") == fase]
    marcas = sorted(m for m in marcas if m)
    if not marcas:
        return None, None
    primeiro = marcas[0]
    return (datetime.now(timezone.utc) - primeiro).days, primeiro.isoformat()


def _prazo_do_nome(nome: str, hoje: date) -> dict | None:
    achado = _PRAZO.search(nome)
    if not achado:
        return None
    dia, mes = int(achado.group(1)), int(achado.group(2))
    try:
        quando = date(hoje.year, mes, dia)
    except ValueError:
        return None
    return {"data": quando.isoformat(), "diasRestantes": (quando - hoje).days,
            "vencido": quando < hoje, "origem": "nome da pasta da demanda"}


def _entregaveis(pasta: Path) -> list[dict]:
    """Arquivos que provam entrega, na pasta da DEMANDA — não na de estado."""
    provas: list[dict] = []
    try:
        candidatos = [x for x in pasta.rglob("*")
                      if x.suffix.lower() in _ENTREGAVEL and x.is_file()]
    except OSError:
        return provas
    for arq in sorted(candidatos):
        try:
            tamanho = arq.stat().st_size
        except OSError:
            continue
        if tamanho < _TAMANHO_MINIMO:
            continue
        provas.append({"arquivo": arq.name, "bytes": tamanho})
    return provas


def _hash_do_maior(pasta: Path, provas: list[dict]) -> str | None:
    if not provas:
        return None
    alvo = max(provas, key=lambda p: p["bytes"])
    for arq in pasta.rglob(alvo["arquivo"]):
        try:
            digest = hashlib.sha256()
            with arq.open("rb") as fh:
                for pedaco in iter(lambda: fh.read(1 << 20), b""):
                    digest.update(pedaco)
            return digest.hexdigest()
        except OSError:
            return None
    return None


def carregar_resolucoes(path: Path | None = None) -> dict:
    dados = _ler_json(path or RESOLUCOES) or {}
    return dados.get("casos", {}) if isinstance(dados, dict) else {}


def _localizador(detalhe: str) -> tuple[str | None, str | None]:
    """(valor, dialeto) do primeiro localizador conferível no texto.

    Reconhecer o localizador não é conferir a entrega: continua sendo dívida de
    auditoria, e é por isso que `entrega_declarada` está em `DEVENDO`. O que
    muda é a acusação — de "cumprido sem nada" para "conferível e não conferido".
    """
    achado = _GMAIL.search(detalhe)
    if achado:
        return achado.group(0), "gmail"
    achado = _WHATSAPP.search(detalhe)
    if achado:
        return achado.group(0), "whatsapp"
    for bruto in _ARQUIVO.findall(detalhe):
        achado = _caminho_citado(bruto)
        if achado:
            return achado, "arquivo_em_disco"
    return None, None


def _caminho_citado(bruto: str) -> str | None:
    """O maior sufixo do trecho que é um arquivo existente. `None` se nenhum é.

    O recorte vem de prosa, então costuma trazer palavras a mais na frente
    ("Arquivo local: Pasta X/peça.docx"). Descascar da esquerda devolve o
    caminho real sem precisar adivinhar onde ele começava.
    """
    tokens = bruto.split(" ")
    for corte in range(len(tokens)):
        trecho = " ".join(tokens[corte:])
        alvo = Path(trecho)
        if not alvo.is_absolute():
            alvo = WORKSPACE / trecho
        try:
            if alvo.is_file():
                return trecho
        except OSError:  # caminho sintaticamente impossível no Windows
            continue
    return None


def _evidencia(legado, n3) -> tuple[str | None, str | None, str]:
    """(localizador, dialeto, detalhe) do que o painel registrou sobre a entrega."""
    for fonte in (legado, n3):
        ev = (fonte or {}).get("deliveryEvidence") or {}
        detalhe = str(ev.get("detail") or "").strip()
        if ev.get("status") in (None, "none", ""):
            continue
        valor, dialeto = _localizador(detalhe)
        return valor, dialeto, detalhe
    return None, None, ""


# O árbitro entre os dois esquemas não é a data do arquivo nem a autoridade de
# um deles: é o que dá para ver, mais o que cada esquema afirma ser.
#
# A medição de 10/08/2026 desmontou a pergunta original. Este módulo nasceu
# dizendo que o legado e o N3 eram "dois registros de verdade divergentes, nenhum
# árbitro" — e são 28 dos 29 registros N3 da casa em `mode: shadow`, declarado no
# próprio manifesto do caso. **Sombra não é um segundo registro da verdade: é o
# diário do executor**, e só sabe o que passou pelo runner. Caso entregue pela
# rota manual não emite evento nenhum ali, então o N3 fica legitimamente em fase
# intermediária. Os 12 divergentes eram todos sombra, um deles com 2.148 eventos
# e atualizado no mesmo dia: não estava parado, estava vivo e narrando outra
# coisa. Cobrar coerência entre os dois era erro de categoria, e a acusação de
# divergência escondia o único achado real — um carimbo de cumprido sem prova.
_ARBITRO = {
    "n3_e_sombra": ("o N3 declara `mode: shadow` no manifesto do caso: ele "
                    "registra o que passou pelo runner, não o que foi entregue. "
                    "Diferir do legado aqui é o comportamento esperado, e não "
                    "divergência a resolver"),
    "n3_parou_no_meio": ("o N3 não é sombra, declara fase intermediária, e a "
                         "evidência prova entrega: o registro deixou de ser "
                         "atualizado"),
    "legado_carimbou_sem_prova": ("o legado declara cumprido e não há entregável, "
                                  "localizador nem declaração: o carimbo não se sustenta"),
    "conflito_real": ("os dois estão informados e discordam; nenhum é desmentido "
                      "pela evidência, então a decisão é humana"),
}


def _modo_do_caso(pasta: Path) -> str | None:
    return ((_ler_json(pasta / "FORJA_CASE_MANIFEST.json") or {}).get("mode"))


def _arbitrar(situacao: str, estado_legado, estado_n3, modo) -> dict:
    """O que a evidência desmente — e o que sequer estava afirmando."""
    provado = situacao in ("entregue", "entrega_conferida")
    legado_terminal = _classe(estado_legado) == "terminal"

    if legado_terminal and situacao == "concluido_sem_prova":
        chave = "legado_carimbou_sem_prova"
    elif modo == "shadow":
        chave = "n3_e_sombra"
    elif provado and _classe(estado_n3) != "terminal":
        chave = "n3_parou_no_meio"
    else:
        chave = "conflito_real"
    return {"veredito": chave, "porque": _ARBITRO[chave],
            "evidencia": situacao, "modoDoN3": modo}


def carregar_conferencias(path: Path | None = None) -> dict:
    """O que já foi conferido na fonte, por `forja_conferir_entregas.py`.

    Conferir prova que a mensagem existe, quando saiu e para quem — não que o
    conteúdo era a peça certa. Por isso `entrega_conferida` é situação própria e
    não vira `entregue`: são graus de prova diferentes, e colapsá-los devolveria
    ao relatório a ambiguidade que a conferência acabou de tirar dele.
    """
    dados = _ler_json(path or CONFERENCIAS) or {}
    return dados.get("casos", {}) if isinstance(dados, dict) else {}


def _situacao(legado, n3, provas, resolucao, existem, conferencia=None) -> tuple[str, str]:
    if legado is None and n3 is None:
        # "Não localizado" não é diagnóstico: a pasta sem arquivo de estado e o
        # arquivo de estado corrompido pedem conserto diferente, e colapsá-los
        # transfere a quem lê o trabalho de descobrir qual era.
        return "ilegivel", ("arquivo de estado presente e ilegível" if existem
                            else "a pasta do caso não tem arquivo de estado algum")

    estados = {str(d.get("status") or d.get("lifecycleStatus") or "").strip()
               for d in (legado, n3) if d}
    estados.discard("")

    if provas:
        return "entregue", f"{len(provas)} entregável(is) na pasta da demanda"
    if estados & _BLOQUEADOS:
        return "bloqueado", "impedimento declarado no estado"
    if estados & _AGUARDANDO:
        return "aguardando_humano", "esperando leitura, revisão ou ciência"
    if estados & _TERMINAIS:
        if resolucao:
            return "triado_sem_demanda", (
                f"declarado por {resolucao.get('por','?')}: {resolucao.get('motivo','')}".strip())
        localizador, dialeto, _ = _evidencia(legado, n3)
        if localizador and (conferencia or {}).get("resultado") == "confere":
            quando = conferencia.get("data") or conferencia.get("conferidoEm")
            para = conferencia.get("para")
            return "entrega_conferida", (
                f"localizador {localizador} conferido na fonte"
                + (f", enviado a {para}" if para else "")
                + (f" em {quando}" if quando else "")
                + " — conferido que a mensagem existe, não que o conteúdo era o esperado")
        if localizador:
            # Tentada e sem rota daqui é diferente de nunca tentada, e chamar as
            # duas de "conferível e não conferida" produz um alerta que ninguém
            # consegue baixar — que é como um gate deixa de ser lido.
            if (conferencia or {}).get("resultado") == "sem_rota_automatica":
                return "entrega_declarada", (
                    f"entrega registrada com localizador {localizador}; a conferência "
                    f"foi tentada e não há rota automática daqui "
                    f"({conferencia.get('motivo', 'motivo não registrado')})")
            onde = {"gmail": "conferível contra a caixa de saída",
                    "whatsapp": "conferível contra o histórico da conversa",
                    "arquivo_em_disco": "o arquivo citado existe e foi conferido agora"}
            return "entrega_declarada", (
                f"entrega registrada com localizador {localizador} "
                f"({onde.get(dialeto, 'conferível')}); sem artefato arquivado aqui")
        return "concluido_sem_prova", (
            "declarado cumprido, sem entregável em disco, sem localizador conferível "
            "e sem declaração de que não havia demanda")
    return "aberto", "trabalho por fazer"


def censo(state_root: Path | None = None, *, resolucoes: dict | None = None,
          conferencias: dict | None = None) -> dict:
    raiz = state_root or STATE
    resolvidos = carregar_resolucoes() if resolucoes is None else resolucoes
    conferidos = carregar_conferencias() if conferencias is None else conferencias
    hoje = datetime.now().date()

    pastas = sorted(p for p in raiz.glob("case-*") if p.is_dir())
    casos: list[dict] = []

    for pasta in pastas:
        arq_legado, arq_n3 = pasta / "FORJA_STATE.json", pasta / "FORJA_N3_STATE.json"
        legado = _ler_json(arq_legado)
        n3 = _ler_json(arq_n3)
        existem = arq_legado.exists() or arq_n3.exists()
        case_id = pasta.name

        origem = (legado or {}).get("inputs", {}).get("caseFolder") or ""
        demanda = Path(origem) if origem else None
        titulo = demanda.name if demanda else ""

        provas = _entregaveis(demanda) if demanda and demanda.exists() else []
        resolucao = resolvidos.get(case_id)
        situacao, porque = _situacao(legado, n3, provas, resolucao, existem,
                                     conferidos.get(case_id))
        localizador, dialeto_localizador, detalhe_evidencia = _evidencia(legado, n3)

        estado_legado = (legado or {}).get("status")
        estado_n3 = (n3 or {}).get("lifecycleStatus")
        divergem = bool(legado and n3
                        and _classe(estado_legado) != _classe(estado_n3))
        arbitro = (_arbitrar(situacao, estado_legado, estado_n3, _modo_do_caso(pasta))
                   if divergem else None)

        dias, desde = _idade_da_fase(legado)
        carimbos = len((legado or {}).get("phaseHistory") or [])
        fases = len({e.get("phase") for e in ((legado or {}).get("phaseHistory") or [])})

        casos.append({
            "caseId": case_id,
            "titulo": titulo,
            "situacao": situacao,
            "porque": porque,
            "esquemas": [n for n, d in (("legado", legado), ("n3", n3)) if d],
            "estadoLegado": estado_legado,
            "estadoN3": estado_n3,
            "esquemasDivergem": divergem,
            "arbitro": arbitro,
            "fase": (legado or {}).get("currentPhase"),
            "diasNaFase": dias,
            "faseDesde": desde,
            "carimbosRepetidos": max(0, carimbos - fases),
            "entregaveis": len(provas),
            "localizadorDaEntrega": localizador,
            "dialetoDoLocalizador": dialeto_localizador,
            "evidenciaDeclarada": detalhe_evidencia[:220] or None,
            "conferencia": (conferidos.get(case_id) or {}).get("resultado"),
            "maiorEntregavel": max((p["bytes"] for p in provas), default=0),
            "prazo": _prazo_do_nome(titulo, hoje) if titulo else None,
            "pastaDaDemandaExiste": bool(demanda and demanda.exists()),
        })

    lidos = [c for c in casos if c["situacao"] != "ilegivel"]
    contagem = {s: sum(1 for c in casos if c["situacao"] == s) for s in SITUACOES}

    return {
        "versao": VERSAO,
        "geradoEm": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        # O denominador vem antes de qualquer número. Foi a sua ausência que
        # deixou "4 prontas" passar por retrato de 89 casos.
        "populacao": {
            "pastasDeCaso": len(pastas),
            "lidos": len(lidos),
            "completo": len(lidos) == len(pastas),
        },
        "situacoes": contagem,
        "divergentes": sum(1 for c in casos if c["esquemasDivergem"]),
        "casos": casos,
    }


def devendo(dados: dict) -> list[dict]:
    """O que ainda deve alguma coisa, com o que tem prazo na frente."""
    abertos = [c for c in dados["casos"] if c["situacao"] in DEVENDO]

    def chave(c):
        prazo = c.get("prazo")
        return (0 if prazo else 1,
                prazo["diasRestantes"] if prazo else 0,
                -(c.get("diasNaFase") or 0))

    return sorted(abertos, key=chave)


def gate_censo(dados: dict) -> list[dict]:
    """Achados que impedem afirmar que a fábrica sabe o próprio estado."""
    achados: list[dict] = []
    pop = dados["populacao"]
    if not pop["completo"]:
        achados.append({"id": "CEN1", "sev": "P0", "quantos": pop["pastasDeCaso"] - pop["lidos"],
                        "texto": "há caso cujo estado não pôde ser lido; o censo está incompleto "
                                 "e nenhum número derivado dele é retrato da população"})
    sem_prova = dados["situacoes"]["concluido_sem_prova"]
    if sem_prova:
        achados.append({"id": "CEN2", "sev": "P0", "quantos": sem_prova,
                        "texto": "caso dado por cumprido sem entregável em disco e sem declaração "
                                 "de que não havia demanda — 'feito' aqui é palavra, não prova"})
    declaradas = [c for c in dados["casos"] if c["situacao"] == "entrega_declarada"]
    sem_rota = [c for c in declaradas if c.get("conferencia") == "sem_rota_automatica"]
    nunca_olhadas = [c for c in declaradas if c not in sem_rota]
    if nunca_olhadas:
        achados.append({"id": "CEN5", "sev": "P1", "quantos": len(nunca_olhadas),
                        "texto": "entrega registrada com localizador e sem artefato arquivado — "
                                 "é conferível e não foi conferida, o que é dívida de auditoria "
                                 "e não de trabalho"})
    if sem_rota:
        achados.append({"id": "CEN6", "sev": "P1", "quantos": len(sem_rota),
                        "texto": "entrega cuja conferência foi tentada e não tem rota automática "
                                 "daqui — só se baixa abrindo a fonte à mão, e fica aberta até lá"})
    vereditos = {}
    for c in dados["casos"]:
        if c.get("arbitro"):
            vereditos[c["arbitro"]["veredito"]] = vereditos.get(
                c["arbitro"]["veredito"], 0) + 1
    if vereditos.get("n3_parou_no_meio"):
        achados.append({"id": "CEN3", "sev": "P1", "quantos": vereditos["n3_parou_no_meio"],
                        "texto": "o N3 não é sombra, declara fase intermediária e a entrega "
                                 "está provada — registro parado, não trabalho parado"})
    # `legado_carimbou_sem_prova` não vira achado próprio: por construção ele só
    # ocorre quando a situação já é `concluido_sem_prova`, então seria o CEN2
    # contado de novo com outro nome. O veredito fica no registro do caso, onde
    # explica a causa; a contagem fica onde já estava.
    if vereditos.get("conflito_real"):
        achados.append({"id": "CEN7", "sev": "P1", "quantos": vereditos["conflito_real"],
                        "texto": "os dois esquemas discordam e nenhum é desmentido pela "
                                 "evidência; a decisão é humana, caso a caso"})
    vencidos = [c for c in dados["casos"]
                if c["situacao"] in DEVENDO and (c.get("prazo") or {}).get("vencido")]
    if vencidos:
        achados.append({"id": "CEN4", "sev": "P0", "quantos": len(vencidos),
                        "texto": "caso com prazo vencido no nome da demanda e ainda em aberto"})
    return achados


def declarar(case_id: str, motivo: str, por: str, *, path: Path | None = None) -> Path:
    alvo = path or RESOLUCOES
    dados = _ler_json(alvo) or {"versao": VERSAO, "casos": {}}
    dados.setdefault("casos", {})[case_id] = {
        "situacao": "triado_sem_demanda",
        "motivo": motivo,
        "por": por,
        "em": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
    }
    alvo.parent.mkdir(parents=True, exist_ok=True)
    alvo.write_text(json.dumps(dados, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return alvo


def _linha(c: dict) -> str:
    prazo = c.get("prazo")
    marca = ""
    if prazo:
        d = prazo["diasRestantes"]
        marca = f"  [PRAZO {prazo['data']} {'VENCIDO' if prazo['vencido'] else f'em {d}d'}]"
    idade = f"{c['diasNaFase']}d" if c.get("diasNaFase") is not None else "?"
    return f"  {c['situacao']:<20} {idade:>5} na fase  {c['titulo'][:58] or c['caseId'][:58]}{marca}"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Censo de casos da FORJA sobre a população inteira.")
    ap.add_argument("--devendo", action="store_true", help="só o que ainda deve alguma coisa")
    ap.add_argument("--divergentes", action="store_true", help="casos em que os dois esquemas discordam")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--declarar", metavar="CASE_ID", help="declarar caso como triado sem demanda")
    ap.add_argument("--motivo")
    ap.add_argument("--por")
    args = ap.parse_args(argv)

    if args.declarar:
        if not args.motivo or not args.por:
            print("--declarar exige --motivo e --por: a declaração responde por quem a fez")
            return 2
        alvo = declarar(args.declarar, args.motivo, args.por)
        print(f"declarado em {alvo}")
        return 0

    dados = censo()
    achados = gate_censo(dados)
    pop = dados["populacao"]

    if args.json:
        print(json.dumps({**dados, "achados": achados}, ensure_ascii=False, indent=2))
        return 0

    print(f"{VERSAO} — {pop['lidos']} de {pop['pastasDeCaso']} pastas de caso lidas"
          f"{'' if pop['completo'] else '  (INCOMPLETO)'}")
    print()

    if args.divergentes:
        for c in dados["casos"]:
            if c["esquemasDivergem"]:
                print(f"  {c['caseId'][:52]:<52} legado={c['estadoLegado']} n3={c['estadoN3']}")
        return 0

    if args.devendo:
        fila = devendo(dados)
        print(f"devendo: {len(fila)} de {pop['pastasDeCaso']}")
        for c in fila:
            print(_linha(c))
    else:
        for s in SITUACOES:
            n = dados["situacoes"][s]
            if n:
                print(f"  {s:<20} {n:>3}")
        sombra = sum(1 for c in dados["casos"]
                     if (c.get("arbitro") or {}).get("veredito") == "n3_e_sombra")
        print(f"\n  esquemas divergentes {dados['divergentes']:>3}")
        if sombra:
            # Sem esta linha o número cai de 17 para 1 sem explicação, e quem lê
            # não distingue defeito consertado de defeito escondido.
            print(f"  destes, {sombra} são N3 em modo sombra, que registra o "
                  f"runner e não a entrega — esperado, não pendência")

    if achados:
        print("\nachados:")
        for a in achados:
            print(f"  [{a['sev']}] {a['id']} ({a['quantos']}) {a['texto']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
