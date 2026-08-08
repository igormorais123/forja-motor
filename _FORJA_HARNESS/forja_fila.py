"""FORJA FILA — priorização automática painel -> FORJA (R1.1 Helena, aprovada 12/07/2026).

Lê o painel (demandas.json) e os estados F0 da FORJA, classifica cada demanda em
pronta / bloqueada (com motivo) / em produção, calcula score determinístico e
explicável e grava a fila em três lugares:
  - state/FILA_PRIORIZADA.json                    (canônico, máquina)
  - reports/FILA_<data>.md                        (humano, score decomposto)
  - gestao_escritorio/data/forja_fila.json        (painel; só com flag filaPriorizadaV1)

Princípios (PRD planejamento/15, anti-requisitos §6):
  - A fila PROPÕE; o humano dispara. Nunca inicia produção sozinha.
  - NUNCA escreve em demandas.json (quadro de comando é humano/Hermes).
  - Score sem LLM, sem rede, sem relógio oculto ('hoje' é injetável para teste).
  - Artefato derivado e regenerável; ninguém edita a fila à mão.

Uso:
  python forja_fila.py             # gera a fila (painel só se flag ligada)
  python forja_fila.py --dry       # imprime classificação sem gravar nada
  python forja_fila.py --proxima   # imprime o caso do topo (exit 3 se fila vazia)
"""

import hashlib
import json
import re
import sys
import unicodedata
from datetime import date, datetime
from pathlib import Path

from forja_n3_common import atomic_write_json, feature_enabled, now_iso

FORJA = Path(__file__).resolve().parent
RAIZ = FORJA.parent
DATA = RAIZ / "gestao_escritorio" / "data"
STATE_DIR = FORJA / "state"
REPORTS_DIR = FORJA / "reports"

SCHEMA_VERSION = 1

COMANDOS = ["COMANDO_DO_EMAIL.md", "COMANDO_DO_WHATSAPP.md", "COMANDO_HERMES.md", "COMANDO_MANUAL.md"]

# Léxico fechado da regra 7 (bloqueada_decisao_cliente) — comparação sem acento e
# em minúsculas. Validado contra os 23 casos reais no gate M0 (18_MAPA §M0).
LEXICO_DECISAO_CLIENTE = [
    "decisao de fabio", "decisao do fabio", "fabio decidir", "aguardar fabio",
    "aguarda fabio", "aguardando fabio", "decisao do cliente", "decisao do chefe",
    "confirmacao do cliente", "confirmacao de fabio", "aguardar o cliente",
    "aguarda o cliente", "aguardando o cliente", "autorizacao do cliente",
    "autorizacao de fabio", "aguardando decisao", "aguardar decisao",
    "depende de fabio", "depende do cliente",
    # gate M0 (12/07/2026): caso real Roraima — "Fábio revisar o dossiê ... e decidir"
    "fabio revisar", "revisao de fabio", "revisao do fabio", "fabio validar",
]

CATEGORIAS_BLOQUEIO = (
    "bloqueada_pasta", "bloqueada_comando", "bloqueada_acesso", "bloqueada_decisao_cliente",
)


def _norm(texto):
    """minúsculas sem acento — léxico estável a variação de digitação."""
    nfkd = unicodedata.normalize("NFKD", texto or "")
    return "".join(c for c in nfkd if not unicodedata.combining(c)).lower()


def _parse_date(valor):
    """date ou None. Aceita 'YYYY-MM-DD' e ISO datetime; malformado -> None."""
    if not valor:
        return None
    try:
        return date.fromisoformat(str(valor)[:10])
    except ValueError:
        return None


def _fase_num(current_phase):
    """F0_...->0, F10_...->10; irreconhecível -> None."""
    texto = str(current_phase or "")
    if not texto.startswith("F"):
        return None
    digitos = ""
    for ch in texto[1:]:
        if ch.isdigit():
            digitos += ch
        else:
            break
    return int(digitos) if digitos else None


def classificar_prontidao(demanda, forja_state):
    """(categoria, motivo) — TDD planejamento/16 §2, primeira regra que casar vence.
    Pré-condição: demanda não está 'cumprida' (o chamador filtra)."""
    # gate M0 (12/07/2026): o painel tem o status 'pronta_para_revisao' — peça já
    # produzida aguardando olho humano. Não é peça a fazer nem bloqueio de insumo.
    if demanda.get("status") == "pronta_para_revisao":
        return "aguardando_revisao_humana", "peça produzida aguardando revisão humana"
    state = forja_state or {}
    fase = _fase_num(state.get("currentPhase"))
    if fase is not None and 1 <= fase <= 9:
        return "em_producao", f"FORJA em {state.get('currentPhase')}"
    if state.get("status") == "waiting_delivery_evidence":
        return "aguardando_evidencia", "cumprida no painel aguardando evidência de entrega"

    gates = {g.get("code"): g for g in (state.get("gates") or [])}
    for code in ("PASTA_AUSENTE", "PASTA_INEXISTENTE", "ORIGEM_AUSENTE"):
        if code in gates:
            return "bloqueada_pasta", gates[code].get("detail") or code
    if "COMANDO_AUSENTE" in gates:
        return "bloqueada_comando", "nenhum COMANDO_*.md na pasta do caso"

    anexos = demanda.get("anexos") or {}
    if anexos.get("externosPendentes"):
        return "bloqueada_acesso", "anexos externos (Drive/TransferNow/WhatsApp) pendentes"
    if "ANEXOS_INCOMPLETOS" in gates:
        return "bloqueada_acesso", gates["ANEXOS_INCOMPLETOS"].get("detail") or "anexos incompletos"

    proxima = _norm(demanda.get("proximaAcao"))
    for marcador in LEXICO_DECISAO_CLIENTE:
        if marcador in proxima:
            return "bloqueada_decisao_cliente", f"próxima ação depende do cliente ('{marcador}')"

    return "pronta", "sem bloqueador conhecido"


def pontuar(demanda, hoje):
    """{'score', 'fatores', 'prazoVencido'} — tabela normativa do PRD §5."""
    fatores = []
    urgencia = _norm(demanda.get("urgenciaManual")) or "media"
    pts_urg = {"alta": 40, "media": 20, "baixa": 0}.get(urgencia, 20)
    fatores.append({"fator": f"urgenciaManual={urgencia}", "pontos": pts_urg})

    prazo = _parse_date(demanda.get("prazo"))
    prazo_vencido = False
    if demanda.get("prazo") and prazo is None:
        fatores.append({"fator": "PRAZO_ILEGIVEL", "pontos": 0})
        pts_prazo = 0
    elif prazo is None:
        fatores.append({"fator": "sem prazo", "pontos": 0})
        pts_prazo = 0
    else:
        dias = (prazo - hoje).days
        prazo_vencido = dias < 0
        if dias <= 3:
            pts_prazo, rotulo = 40, "prazo<=3d" if not prazo_vencido else "PRAZO_VENCIDO"
        elif dias <= 7:
            pts_prazo, rotulo = 30, "prazo<=7d"
        elif dias <= 14:
            pts_prazo, rotulo = 20, "prazo<=14d"
        elif dias <= 30:
            pts_prazo, rotulo = 10, "prazo<=30d"
        else:
            pts_prazo, rotulo = 0, f"prazo em {dias}d"
        fatores.append({"fator": rotulo, "pontos": pts_prazo})

    pts_valor = 10 if any(_norm(t) == "alto valor" for t in demanda.get("tags") or []) else 0
    if pts_valor:
        fatores.append({"fator": "tag alto valor", "pontos": pts_valor})

    recebido = _parse_date(demanda.get("recebidoEm"))
    idade = min(max((hoje - recebido).days, 0), 10) if recebido else 0
    if idade:
        fatores.append({"fator": f"idade {min((hoje - recebido).days, 999)}d (cap 10)", "pontos": idade})

    return {"score": pts_urg + pts_prazo + pts_valor + idade,
            "fatores": fatores, "prazoVencido": prazo_vencido}


def ordenar(pontuadas):
    """score desc; empate: prazo asc (None por último) -> recebidoEm asc -> id asc."""
    def chave(item):
        prazo = _parse_date(item.get("prazo"))
        recebido = _parse_date(item.get("recebidoEm"))
        return (-item["score"],
                prazo is None, prazo or date.max,
                recebido is None, recebido or date.max,
                item.get("demandaId") or "")
    return sorted(pontuadas, key=chave)


def pendencia_operacao_assistida(config, hoje):
    """Acompanhamento de marco interno DENTRO da FORJA (feedback Igor 12/07/2026:
    marco de engenharia nunca vira evento/alarme no calendário dele — pendência
    interna vive na fila e no painel). Lê config['fila']['operacaoAssistidaAte'].
    Retorna None (sem pendência) ou {'ate', 'fechamentoPendente', 'aviso'}."""
    ate = ((config or {}).get("fila") or {}).get("operacaoAssistidaAte")
    data_ate = _parse_date(ate)
    if data_ate is None:
        return None
    pendente = hoje >= data_ate
    aviso = (f"M4 vence hoje ou já venceu ({ate}) — fechar: revisar acertos da fila na semana, "
             f"recalibrar pesos ou promover em definitivo (planejamento/18 §M4)"
             if pendente else
             f"operação assistida (M4) até {ate} — anotar acertos/erros da fila a cada peça iniciada")
    return {"ate": ate, "fechamentoPendente": pendente, "aviso": aviso}


def _aguardando_desde(demanda):
    """Melhor estimativa de quando a espera começou: último comentário manual,
    senão recebidoEm. Base do destaque de 48h (FILA-R7, informativo)."""
    manual = demanda.get("manual") or {}
    return manual.get("updatedAt") or demanda.get("recebidoEm")


def montar_fila(demandas, states, hoje):
    """Documento canônico (TDD §3). Função pura: sem I/O, 'hoje' injetado."""
    producao, bloqueadas, em_producao, aguardando_ev, revisao_humana = [], [], [], [], []
    for demanda in demandas:
        if demanda.get("status") == "cumprida":
            state = states.get(demanda.get("id")) or {}
            if state.get("status") == "waiting_delivery_evidence":
                aguardando_ev.append(demanda.get("id"))
            continue
        categoria, motivo = classificar_prontidao(demanda, states.get(demanda.get("id")))
        base = {
            "demandaId": demanda.get("id"),
            "caseId": "case-" + (demanda.get("id") or "sem-id"),
            "titulo": demanda.get("titulo"),
            "pasta": demanda.get("pasta"),
            "prazo": demanda.get("prazo") or None,
        }
        base.update(pontuar(demanda, hoje))
        if categoria == "pronta":
            base["comando"] = next(
                (c for c in COMANDOS if demanda.get("pasta") and (RAIZ / demanda["pasta"] / c).exists()), None)
            producao.append({**base, "recebidoEm": demanda.get("recebidoEm")})
        elif categoria == "em_producao":
            em_producao.append(demanda.get("id"))
        elif categoria == "aguardando_revisao_humana":
            revisao_humana.append({"demandaId": demanda.get("id"), "titulo": demanda.get("titulo")})
        elif categoria == "aguardando_evidencia":
            aguardando_ev.append(demanda.get("id"))
        else:
            desde = _aguardando_desde(demanda) if categoria == "bloqueada_decisao_cliente" else None
            dias_espera = None
            if desde:
                d = _parse_date(desde)
                dias_espera = (hoje - d).days if d else None
            bloqueadas.append({**base, "categoria": categoria, "motivo": motivo,
                               "recebidoEm": demanda.get("recebidoEm"),
                               "aguardandoDesde": desde,
                               "esperaDias": dias_espera,
                               "destaque48h": bool(dias_espera is not None and dias_espera >= 2)})

    producao = ordenar(producao)
    for i, item in enumerate(producao, 1):
        item["posicao"] = i
        item.pop("recebidoEm", None)
    bloqueadas = ordenar(bloqueadas)
    for item in bloqueadas:
        item.pop("recebidoEm", None)

    return {
        "schemaVersion": SCHEMA_VERSION,
        "producao": producao,
        "bloqueadas": bloqueadas,
        "emProducao": sorted(em_producao),
        "aguardandoRevisaoHumana": sorted(revisao_humana, key=lambda x: x["demandaId"]),
        "aguardandoEvidencia": sorted(aguardando_ev),
        "resumo": {"prontas": len(producao), "bloqueadas": len(bloqueadas),
                   "emProducao": len(em_producao),
                   "aguardandoRevisaoHumana": len(revisao_humana),
                   "aguardandoEvidencia": len(aguardando_ev)},
    }


# ---------------------------------------------------------------- I/O


def _read_json(path, fallback):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8-sig"))
    except FileNotFoundError:
        return fallback


def _carregar_states():
    states = {}
    for state_path in STATE_DIR.glob("case-*/FORJA_STATE.json"):
        state = _read_json(state_path, {})
        demand_id = (state.get("inputs") or {}).get("demandId")
        if demand_id:
            states[demand_id] = state
    return states


_SO_RELOGIO = (
    re.compile(r"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}(:\d{2})?([+-]\d{2}:\d{2})?"),
    re.compile(r"\b\d+(\.\d+)?\s*h\b"),
)


def _assinatura(texto: str) -> str:
    """Hash do relatório com o relógio apagado.

    Serve para responder uma pergunta só: mudou alguma coisa na fila, ou só
    passou o tempo? A hora da geração e o "parado há N h" mudam a cada
    execução e não são notícia.
    """
    for padrao in _SO_RELOGIO:
        texto = padrao.sub("<t>", texto)
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


def _gravar_relatorio(texto: str) -> Path:
    """Grava o relatório datado, mas só quando a fila mudou de fato.

    O vigia roda de meia em meia hora. Escrevendo sempre, em 27 dias saíram
    1.242 arquivos para **124 conteúdos distintos** — 90% de repetição, e
    ninguém relê nenhum deles: o artefato que os consumidores usam é o
    `state/FILA_PRIORIZADA.json`, que é sobrescrito. O que o arquivo datado
    tem de valor é marcar QUANDO a fila mudou, e isso o repetido apaga em vez
    de registrar.

    Quando nada mudou, devolve o arquivo anterior sem tocar no disco.
    """
    anteriores = sorted(REPORTS_DIR.glob("FILA_*.md"))
    nova = _assinatura(texto)
    if anteriores:
        ultimo = anteriores[-1]
        try:
            if _assinatura(ultimo.read_text(encoding="utf-8")) == nova:
                return ultimo
        except OSError:
            pass
    destino = REPORTS_DIR / f"FILA_{datetime.now().strftime('%Y-%m-%d_%H%M')}.md"
    destino.write_text(texto, encoding="utf-8")
    return destino


def _relatorio_md(fila):
    linhas = [
        "# FORJA FILA — priorização painel → FORJA",
        "",
        f"Gerada em: {fila['geradoEm']} | fonte: demandas.json de {fila['origem']['demandasUpdatedAt']}",
        "",
        f"**Resumo:** {fila['resumo']['prontas']} prontas | {fila['resumo']['bloqueadas']} bloqueadas | "
        f"{fila['resumo']['emProducao']} em produção | {fila['resumo']['aguardandoRevisaoHumana']} aguardando revisão humana | "
        f"{fila['resumo']['aguardandoEvidencia']} aguardando evidência",
        "",
        "## Próximas peças (prontas para produção)",
        "",
        "| # | Demanda | Prazo | Score | Fatores |",
        "|---|---|---|---|---|",
    ]
    for item in fila["producao"]:
        fatores = "; ".join(f"{f['fator']} +{f['pontos']}" for f in item["fatores"])
        prazo = (item["prazo"] or "—") + (" **VENCIDO**" if item["prazoVencido"] else "")
        linhas.append(f"| {item['posicao']} | {item['titulo']} | {prazo} | **{item['score']}** | {fatores} |")
    if not fila["producao"]:
        linhas.append("| — | nenhuma demanda pronta | | | |")
    linhas += ["", "## Bloqueadas (ordenadas pela mesma régua — orientam o desbloqueio)", "",
               "| Demanda | Categoria | Motivo | Score | Espera |", "|---|---|---|---|---|"]
    for item in fila["bloqueadas"]:
        espera = f"{item['esperaDias']}d" if item.get("esperaDias") is not None else "—"
        if item.get("destaque48h"):
            espera = f"**{espera} — aguardando decisão há mais de 48h**"
        linhas.append(f"| {item['titulo']} | `{item['categoria']}` | {item['motivo']} | {item['score']} | {espera} |")
    if not fila["bloqueadas"]:
        linhas.append("| — | | | | |")
    if fila["emProducao"]:
        linhas += ["", "## Em produção", ""] + [f"- {d}" for d in fila["emProducao"]]
    if fila["aguardandoRevisaoHumana"]:
        linhas += ["", "## Aguardando revisão humana (peça pronta — gargalo é gente, não máquina)", ""] + [
            f"- {d['titulo']} (`{d['demandaId']}`)" for d in fila["aguardandoRevisaoHumana"]]
    if fila["aguardandoEvidencia"]:
        linhas += ["", "## Aguardando evidência de entrega", ""] + [f"- {d}" for d in fila["aguardandoEvidencia"]]
    oa = fila.get("operacaoAssistida")
    if oa:
        marcador = "**PENDENTE** — " if oa["fechamentoPendente"] else ""
        linhas += ["", f"> {marcador}{oa['aviso']}"]
    linhas += ["", "A fila propõe; o humano dispara. Para consumir o topo: `python forja_fila.py --proxima`.", ""]
    return "\n".join(linhas)


def gerar(hoje=None, gravar=True, publicar_painel=None):
    """Gera a fila. gravar=False -> só retorna o documento (modo --dry).
    publicar_painel: None -> segue a flag filaPriorizadaV1; bool -> força."""
    demandas_bytes = (DATA / "demandas.json").read_bytes()
    demandas_doc = json.loads(demandas_bytes.decode("utf-8-sig"))
    hoje = hoje or date.today()
    fila = montar_fila(demandas_doc.get("demandas") or [], _carregar_states(), hoje)
    from forja_n3_common import load_config
    fila["operacaoAssistida"] = pendencia_operacao_assistida(load_config(), hoje)
    fila["geradoEm"] = now_iso()
    fila["origem"] = {
        "demandasPath": "gestao_escritorio/data/demandas.json",
        "demandasSha256": hashlib.sha256(demandas_bytes).hexdigest(),
        "demandasUpdatedAt": demandas_doc.get("updatedAt"),
    }
    if not gravar:
        return fila

    atomic_write_json(STATE_DIR / "FILA_PRIORIZADA.json", fila)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    rel_path = _gravar_relatorio(_relatorio_md(fila))

    if publicar_painel is None:
        publicar_painel = feature_enabled("filaPriorizadaV1")
    if publicar_painel:
        atomic_write_json(DATA / "forja_fila.json", fila)
    fila["_artefatos"] = {"canonico": str(STATE_DIR / "FILA_PRIORIZADA.json"),
                          "relatorio": str(rel_path),
                          "painel": str(DATA / "forja_fila.json") if publicar_painel else None}
    return fila


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    if "--dry" in argv:
        fila = gerar(gravar=False)
        print(json.dumps(fila, ensure_ascii=False, indent=2))
        return 0
    if "--proxima" in argv:
        fila = gerar()
        if not fila["producao"]:
            print(json.dumps({"proxima": None, "motivo": "nenhuma demanda pronta"}, ensure_ascii=False))
            return 3
        topo = fila["producao"][0]
        print(json.dumps({"proxima": topo}, ensure_ascii=False, indent=2))
        return 0
    fila = gerar()
    print(json.dumps({"ok": True, "resumo": fila["resumo"], "artefatos": fila["_artefatos"]},
                     ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
