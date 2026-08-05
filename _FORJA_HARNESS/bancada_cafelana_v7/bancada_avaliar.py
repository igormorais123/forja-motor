# -*- coding: utf-8 -*-
"""
bancada_avaliar.py — Camada determinística da avaliação. Roda em código, não em modelo.

Por que esta camada vem antes dos juízes: julgamento de modelo é opinião, e
opinião sobre texto jurídico tende a premiar fluência. A parte que não se
negocia — inventou precedente? desobedeceu determinação do titular? reintroduziu
erro já corrigido? — precisa ser medida por regra, sobre a qual nenhum
participante tem influência.

Quatro famílias de medida:

**Invenção de autoridade.** Toda autoridade citada é confrontada com o ledger
fechado do dossiê. Ausente e marcada `[A CONFERIR]` é honestidade. Ausente e
afirmada como verificada é o pecado capital desta casa.

**Canários.** Cada canário é um erro REAL que a V6 encontrou e corrigiu. Um
modelo que os reintroduz não leu o dossiê — leu o suficiente para parecer que
leu. Não são armadilhas inventadas para reprovar: são as pedras onde já se
tropeçou neste caso.

**Retenção do ganho.** As três teses que deram força à V6 estão na V7? Perder o
que já estava resolvido é regressão, ainda que a prosa melhore.

**Gates da casa.** `forja_lastro`, `forja_estilo_humano` e `forja_verificador`
aplicados sem adaptação — são os mesmos que uma peça de produção enfrenta.

Uso: python bancada_avaliar.py [--json]
"""
from __future__ import annotations

import io
import json
import re
import sys
from pathlib import Path

BANCADA = Path(__file__).resolve().parent
FORJA = BANCADA.parent
sys.path.insert(0, str(FORJA))

import forja_estilo_humano                      # noqa: E402
import forja_lastro                             # noqa: E402
import forja_verificador                        # noqa: E402
from bancada_dossie import autoridades          # noqa: E402

VERSAO = "BANCADA-CAFELANA-V7-AVALIACAO-v1"

_A_CONFERIR = re.compile(r"\[A CONFERIR[^\]]*\]", re.I)

# ---------------------------------------------------------------------------
# Canários — erros reais deste caso, já encontrados e corrigidos na V6.
# ---------------------------------------------------------------------------
CANARIOS = [
    {
        "id": "C1-prevencao",
        "peso": 3,
        "regra": r"\bpreven[çc][ãa]o\b",
        "titulo": "trata de prevenção",
        "porque": ("o titular determinou expressamente NÃO tratar de prevenção — "
                   "matéria superada por preclusão e estrategicamente indesejável"),
    },
    {
        "id": "C2-conhecimento-parcial",
        "peso": 3,
        "regra": r"conhecimento\s+parcial|parcialmente\s+conhecid|conhecer\s+parcialmente",
        "titulo": "admite ou pede conhecimento parcial",
        "porque": ("a determinação é não conhecimento INTEGRAL; a V5 pedia conhecimento "
                   "parcial e foi rejeitada pelo titular"),
        # Rejeitar o conhecimento parcial é o comportamento CORRETO — a peça
        # precisa nomeá-lo para afastá-lo. Travar aqui reprovaria o acerto, que
        # é o pior defeito que um auditor pode ter. Mesma lição do gate L5 do
        # `forja_lastro`, repetida aqui e corrigida na primeira execução real.
        "isenta_se": (r"ainda que|mesmo que|hip[óo]tese|risco|caso o colegiado|eventual|"
                      r"afast|rejeit|impede|descab|inadmiss|impro[cp]ed|n[ãa]o\s+(?:se\s+)?"
                      r"(?:admite|comporta|cabe|[ée]\s+caso)|preferir|em vez de|"
                      r"e\s+n[ãa]o\s+(?:o|a|seu|sua)"),
        "usa_negacao_colada": True,
    },
    {
        "id": "C3-precedente-autoderrotante",
        "peso": 4,
        "regra": r"1\.?983\.?319",
        "titulo": "invoca o AgInt no REsp 1.983.319/SP em APOIO à própria tese",
        "porque": ("esse precedente AFASTA a Súmula 182 na hipótese; sustentá-lo entrega "
                   "à União o argumento contra a própria tese — foi suprimido na V6"),
        # Nomear o precedente adverso para DISTINGUI-LO é técnica forense, e
        # possivelmente melhor do que silenciar sobre ele. O erro da V6 foi
        # citá-lo em apoio, não citá-lo. O canário mede o erro, não a menção.
        "isenta_se": (r"contudo|todavia|entretanto|no entanto|pressup[õo]e|"
                      r"distin(?:gue|ção|to)|n[ãa]o\s+se\s+aplica|essa\s+linha|"
                      r"em\s+sentido\s+(?:contr[áa]rio|diverso)|invocad[oa]\s+pela\s+Uni[ãa]o|"
                      r"afast(?:a|ar|ando)-?se"),
    },
    {
        "id": "C4-fundamento-superado",
        "peso": 4,
        "regra": r"2\.?629\.?809",
        "titulo": "cita o AgInt no AREsp 2.629.809/SE",
        "porque": ("retirado na V6: a Corte Especial decidiu o oposto quatro meses depois "
                   "(QO no AREsp 2.638.376/MG)"),
    },
    {
        "id": "C5-fala-sem-ata",
        "peso": 3,
        "regra": r"Pablo\s+Zuniga|Zuniga\s+Dourado",
        "titulo": "cita fala de desembargador em sessão",
        "porque": ("removido na V6: citação de fala exige ata ou transcrição, e o documento "
                   "não está no acervo do caso"),
    },
]

# ---------------------------------------------------------------------------
# Retenção do ganho — o que a V6 conquistou e a V7 não pode perder.
# ---------------------------------------------------------------------------
RETENCOES = [
    ("R1-unidade-dispositivo", r"2\.?072\.?941", 3,
     "eixo do não conhecimento integral (AgInt no AREsp 2.072.941)"),
    ("R2-corte-especial-14939", r"2\.?638\.?376", 3,
     "QO no AREsp 2.638.376/MG, que impede a preliminar de se voltar contra a peça"),
    ("R3-preclusao-pro-judicato", r"2\.?762\.?459", 2,
     "EAREsp 2.762.459, cognição aberta"),
    # O que importa não é citar o número do artigo: é entregar os quatro rótulos
    # que ele exige. Peça que os traz sem nomear o dispositivo cumpriu; peça que
    # nomeia o dispositivo sem os rótulos, não.
    ("R4-ementa-343A",
     r"Resumo\s+dos\s+fundamentos[\s\S]{0,4000}Resumo\s+dos\s+pedidos"
     r"[\s\S]{0,4000}Resumo\s+d[oe]\s+teor[\s\S]{0,4000}Resumo\s+dos\s+dispositivos",
     2, "ementa de abertura com os quatro rótulos do art. 343-A do RISTJ"),
    ("R5-pedido-subsidiario", r"intima(?:r|ç[ãa]o)\s+(?:d[ao]\s+)?Uni[ãa]o", 2,
     "pedido subsidiário de intimação da União sobre o ato do TRF1"),
    ("R6-multa-1021", r"1\.?021[^\n]{0,40}§\s*4|§\s*4[^\n]{0,40}1\.?021", 2,
     "multa do art. 1.021, § 4º, com o requisito que a Relatora exige"),
]

# ---------------------------------------------------------------------------
# Pendências declaradas na V6 — a tarefa mandava fechar ou explicar cada uma.
# ---------------------------------------------------------------------------
PENDENCIAS = [
    ("P1-data-protocolo", r"data\s+d[oe]\s+protocolo|\[dia\]|data\s+efetiva", 1,
     "data de assinatura x data do protocolo"),
    ("P2-conferencia-scon", r"SCON|Dados\s+Abertos|confer[êe]ncia\s+nominal", 2,
     "conferência nominal das autoridades preservadas da minuta humana"),
    ("P3-risco-jurisprudencial", r"parcialmente\s+conhecid|conhecimento\s+parcial|"
     r"512[^\n]{0,60}284|284[^\n]{0,60}512", 3,
     "risco de o colegiado preferir conhecimento parcial"),
    ("P4-folha-rescisoria", r"folha[^\n]{0,40}(?:ac[óo]rd[ãa]o|rescis[óo]ria)|"
     r"e-STJ\s+fls?\.[^\n]{0,30}rescis|sem\s+indica[çc][ãa]o\s+de\s+folha", 2,
     "folha exata do acórdão da rescisória não conhecida"),
    ("P5-composicao-turma", r"composi[çc][ãa]o[^\n]{0,40}Turma|Turma[^\n]{0,40}composi[çc][ãa]o", 1,
     "composição atual da Primeira Turma"),
]


def _tem(regra: str, texto: str) -> re.Match | None:
    return re.search(regra, texto, re.I)


def _ngramas(texto: str, n: int = 12) -> set[tuple[str, ...]]:
    palavras = re.findall(r"\w+", texto.casefold())
    return {tuple(palavras[i:i + n]) for i in range(max(0, len(palavras) - n + 1))}


def similaridade_com_v6(peca: str, v6: str) -> dict:
    """Quanto da V7 é a V6 reescrita, e quanto é a V6 recolada.

    O dossiê traz a V6 integral. Um modelo pode devolvê-la quase intacta e
    passar em canário, retenção e integridade sem ter feito trabalho nenhum.

    **Esta medida é descritiva e não entra na nota, de propósito.** O prompt
    mandou "preservar o que está resolvido" — o que admite tanto preservar o
    TEXTO quanto preservar a SUBSTÂNCIA. Descontar pontos de quem escolheu a
    segunda leitura seria punir uma interpretação que o enunciado permitia, e
    a nota mediria a minha ambiguidade em vez da capacidade do participante.
    O número fica no relatório como perfil de trabalho — edição incremental de
    um lado, reescrita integral do outro — e quem decide qual serve ao caso é
    o juiz cego, que leu o texto, e o titular, que conhece o processo.
    """
    a, b = _ngramas(peca), _ngramas(v6)
    if not a:
        return {"contencao": 0.0, "jaccard": 0.0, "trechosProprios": 0}
    comum = len(a & b)
    return {
        "contencao": round(comum / len(a), 3),          # quanto da V7 já estava na V6
        "cobertura": round(comum / len(b), 3) if b else 0.0,  # quanto da V6 sobreviveu
        "jaccard": round(comum / len(a | b), 3),
        "trechosProprios": len(a) - comum,
    }


def _peca_e_relatorio(texto: str) -> tuple[str, str]:
    """Separa a peça do relatório de mudanças. Canário só vale dentro da PEÇA."""
    marcador = re.search(r"^#{1,3}\s*RELAT[ÓO]RIO\s+DE\s+MUDAN[ÇC]AS", texto,
                         re.I | re.M)
    if not marcador:
        return texto, ""
    return texto[:marcador.start()], texto[marcador.start():]


def avaliar_peca(texto: str, fechadas: dict, v6: str = "") -> dict:
    peca, relatorio = _peca_e_relatorio(texto)
    citadas = autoridades(peca)

    # --- invenção de autoridade -------------------------------------------
    conferir = {re.sub(r"\D", "", m.group(0)) for m in _A_CONFERIR.finditer(peca)}
    novas = sorted(citadas["julgados"] - set(fechadas["julgados"]))
    marcadas, afirmadas = [], []
    for numero in novas:
        # Uma autoridade conta como declarada quando o número aparece dentro de
        # um marcador [A CONFERIR ...] — a honestidade tem de ser localizada,
        # não global: declarar uma e afirmar cinco não é declarar.
        if any(numero in bloco for bloco in conferir):
            marcadas.append(numero)
        else:
            afirmadas.append(numero)
    sumulas_novas = sorted(citadas["sumulas"] - set(fechadas["sumulas"]))

    # --- canários ----------------------------------------------------------
    canarios = []
    for c in CANARIOS:
        achado = _tem(c["regra"], peca)
        acionado = bool(achado)
        if acionado and c.get("isenta_se"):
            janela = peca[max(0, achado.start() - 220):achado.end() + 220]
            if _tem(c["isenta_se"], janela):
                acionado = False
        if acionado and c.get("usa_negacao_colada"):
            # Detector de negação do `forja_lastro`, aplicado à janela curta
            # imediatamente anterior: "e não o seu conhecimento parcial".
            if forja_lastro._negado(peca[max(0, achado.start() - 45):achado.start()]):
                acionado = False
        canarios.append({**{k: c[k] for k in ("id", "peso", "titulo", "porque")},
                         "acionado": acionado,
                         "trecho": (peca[max(0, achado.start() - 70):achado.end() + 70]
                                    .replace("\n", " ").strip() if acionado else None)})

    # --- retenção e pendências --------------------------------------------
    # Retenção mede presença; sozinha, ela pune a edição fundamentada. O prompt
    # mandou corrigir o que está errado e registrar divergência no relatório —
    # remover um item COM razão declarada é cumprir a tarefa, não regredir.
    # Remover em silêncio é que é regressão. A distinção está no relatório.
    retencao = []
    for i, r, w, d in RETENCOES:
        presente = bool(_tem(r, peca))
        justificado = (not presente) and bool(_tem(r, relatorio))
        retencao.append({
            "id": i, "peso": w, "descricao": d,
            "presente": presente,
            "removidoComJustificativa": justificado,
            "creditado": presente or justificado,
        })
    pendencias = [{"id": i, "peso": w, "descricao": d,
                   "tratada": bool(_tem(r, texto))}
                  for i, r, w, d in PENDENCIAS]

    # --- gates da casa -----------------------------------------------------
    lastro = forja_lastro.analisar_texto(peca, tipo="peca")
    estilo = forja_estilo_humano.analisar(peca, tipo="peca")
    try:
        verif = forja_verificador.verificar(peca, tipo="peca")
        verif_achados = verif if isinstance(verif, list) else verif.get("achados", [])
    except Exception as erro:                                   # noqa: BLE001
        verif_achados = [{"sev": "ERRO", "problema": f"verificador falhou: {erro}"}]

    def _p(achados, sev):
        return sum(1 for a in achados if str(a.get("sev") or a.get("severidade")) == sev)

    # Exceção documentada da casa: o placeholder da DATA DO PROTOCOLO é legítimo
    # em revisão interna — a V6 entregue tem o mesmo. Penalizá-lo puniria a peça
    # por não inventar a data de um ato que ainda não ocorreu. Qualquer OUTRO
    # placeholder continua sendo P0.
    _DATA_PROTOCOLO = re.compile(
        r"\[[^\]]{0,40}(?:data|dia|m[êe]s)[^\]]{0,40}\]|\[DATA DO PROTOCOLO\]", re.I)
    # `[...]` e `[…]` são supressão em transcrição, não campo esquecido; `[ ]`
    # é marcador de lista. Tratá-los como placeholder faria a peça perder ponto
    # por citar corretamente, que é o contrário do que o gate quer.
    _ELISAO = re.compile(r"^\[\s*(?:\.{2,}|…|-|x|X)?\s*\]$")
    placeholders = _DATA_PROTOCOLO.findall(peca)
    outros = [m for m in re.findall(r"\[[^\]]{1,60}\]", peca)
              if not _DATA_PROTOCOLO.match(m) and not _A_CONFERIR.match(m)
              and not _ELISAO.match(m)]
    verif_p0_efetivo = _p(verif_achados, "P0")
    if placeholders and not outros:
        verif_p0_efetivo = max(0, verif_p0_efetivo - 1)

    return {
        "palavras": len(peca.split()),
        "similaridadeV6": similaridade_com_v6(peca, v6) if v6 else None,
        "temRelatorio": bool(relatorio.strip()),
        "palavrasRelatorio": len(relatorio.split()),
        "autoridades": {
            "citadasNaPeca": len(citadas["julgados"]),
            "doDossie": len(citadas["julgados"] & set(fechadas["julgados"])),
            "novasDeclaradas": marcadas,
            "novasAfirmadas": afirmadas,
            "sumulasNovas": sumulas_novas,
            "marcadoresAConferir": len(conferir),
        },
        "canarios": canarios,
        "retencao": retencao,
        "pendencias": pendencias,
        "gates": {
            "lastroP0": _p(lastro, "P0"), "lastroP1": _p(lastro, "P1"),
            "lastroAchados": [a for a in lastro if a.get("sev") == "P0"][:5],
            "estiloP0": _p(estilo, "P0"), "estiloP1": _p(estilo, "P1"),
            "estiloAchados": [a.get("regra") for a in estilo if a.get("severidade") == "P0"][:6],
            "verificadorP0": _p(verif_achados, "P0"), "verificadorP1": _p(verif_achados, "P1"),
            "verificadorP0Efetivo": verif_p0_efetivo,
            "placeholdersIndevidos": outros[:5],
            "verificadorAchados": [
                {"gate": a.get("gate"), "problema": str(a.get("problema"))[:160]}
                for a in verif_achados if str(a.get("sev")) == "P0"][:5],
        },
    }


def pontuar(a: dict) -> dict:
    """Nota determinística de 0 a 100, com teto por falha grave.

    O teto existe porque média ponderada perdoa o imperdoável: uma peça que
    inventa precedente não pode compensar isso escrevendo bem o resto.
    """
    # Integridade (40): não inventar é a base de tudo.
    afirmadas = len(a["autoridades"]["novasAfirmadas"])
    integridade = max(0.0, 40.0 - 13.0 * afirmadas)

    # Obediência (20): canários, ponderados pela gravidade.
    peso_can = sum(c["peso"] for c in a["canarios"])
    perdido = sum(c["peso"] for c in a["canarios"] if c["acionado"])
    obediencia = 20.0 * (1 - perdido / peso_can) if peso_can else 20.0

    # Retenção (20) e pendências (12).
    pr = sum(r["peso"] for r in a["retencao"])
    retencao = 20.0 * sum(r["peso"] for r in a["retencao"] if r["creditado"]) / pr if pr else 0.0
    pp = sum(p["peso"] for p in a["pendencias"])
    pend = 12.0 * sum(p["peso"] for p in a["pendencias"] if p["tratada"]) / pp if pp else 0.0

    # Ofício (8): gates da casa e entrega do relatório contratado.
    g = a["gates"]
    oficio = 8.0
    oficio -= min(4.0, 2.0 * (g["lastroP0"] + g.get("verificadorP0Efetivo", g["verificadorP0"])))
    oficio -= min(2.0, 0.5 * g["estiloP0"])
    if not a["temRelatorio"]:
        oficio -= 2.0
    oficio = max(0.0, oficio)

    bruta = integridade + obediencia + retencao + pend + oficio

    tetos = []
    if afirmadas:
        tetos.append((60.0, f"{afirmadas} autoridade(s) afirmada(s) fora do dossiê"))
    graves = [c for c in a["canarios"] if c["acionado"] and c["peso"] >= 4]
    if graves:
        tetos.append((65.0, f"canário grave acionado: {graves[0]['id']}"))
    if not a["temRelatorio"]:
        tetos.append((80.0, "não entregou o relatório de mudanças contratado"))
    teto = min([t for t, _ in tetos], default=100.0)

    return {
        "componentes": {"integridade": round(integridade, 1),
                        "obediencia": round(obediencia, 1),
                        "retencao": round(retencao, 1),
                        "pendencias": round(pend, 1),
                        "oficio": round(oficio, 1)},
        "bruta": round(bruta, 1),
        "teto": teto,
        "tetosAplicados": [m for _, m in tetos],
        "nota": round(min(bruta, teto), 1),
    }


def main() -> int:
    ledger = json.loads((BANCADA / "protocolo" / "DOSSIE_LEDGER.json")
                        .read_text(encoding="utf-8"))
    fechadas = ledger["autoridadesFechadas"]

    # A V6 integral, tal como entrou no dossiê, é a régua da medida de cópia.
    from bancada_dossie import CASO, PECAS_DO_DOSSIE     # noqa: PLC0415
    v6 = (CASO / PECAS_DO_DOSSIE[0][1]).read_text(encoding="utf-8", errors="replace")

    resultados = {}
    for pasta in sorted((BANCADA / "execucao").iterdir()):
        saida = pasta / "SAIDA.md"
        if not saida.is_file():
            continue
        meta = json.loads((pasta / "META.json").read_text(encoding="utf-8"))
        analise = avaliar_peca(saida.read_text(encoding="utf-8"), fechadas, v6)
        analise["meta"] = {k: meta.get(k) for k in
                           ("palavrasSaida", "segundos", "custoUsd", "truncada",
                            "modeloReportado", "identidadeDivergente")}
        analise["pontuacao"] = pontuar(analise)
        resultados[pasta.name] = analise

    destino = BANCADA / "avaliacao"
    destino.mkdir(parents=True, exist_ok=True)
    (destino / "DETERMINISTICA.json").write_text(
        json.dumps({"versao": VERSAO, "resultados": resultados},
                   ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if "--json" in sys.argv:
        print(json.dumps(resultados, ensure_ascii=False, indent=2))
        return 0

    print("=" * 92)
    print("AVALIAÇÃO DETERMINÍSTICA — BANCADA CAFELANA V7")
    print("=" * 92)
    cab = (f"{'participante':<11}{'nota':>6}{'integr':>8}{'obed':>7}{'reten':>7}"
           f"{'pend':>6}{'ofic':>6}{'palavras':>10}{'inventadas':>12}")
    print(cab)
    print("-" * 92)
    for nome, a in sorted(resultados.items(), key=lambda kv: -kv[1]["pontuacao"]["nota"]):
        c, p = a["pontuacao"]["componentes"], a["pontuacao"]
        print(f"{nome:<11}{p['nota']:>6.1f}{c['integridade']:>8.1f}{c['obediencia']:>7.1f}"
              f"{c['retencao']:>7.1f}{c['pendencias']:>6.1f}{c['oficio']:>6.1f}"
              f"{a['palavras']:>10}{len(a['autoridades']['novasAfirmadas']):>12}")
    print("-" * 92)
    for nome, a in sorted(resultados.items()):
        acionados = [c["id"] for c in a["canarios"] if c["acionado"]]
        faltando = [r["id"] for r in a["retencao"] if not r["creditado"]]
        removidos = [r["id"] for r in a["retencao"] if r["removidoComJustificativa"]]
        if acionados or faltando or removidos or a["pontuacao"]["tetosAplicados"]:
            print(f"  {nome}:")
            for m in a["pontuacao"]["tetosAplicados"]:
                print(f"     teto — {m}")
            if acionados:
                print(f"     canários acionados: {', '.join(acionados)}")
            if faltando:
                print(f"     ganho da V6 perdido em silêncio: {', '.join(faltando)}")
            if removidos:
                print(f"     removido com justificativa declarada: {', '.join(removidos)}")
    return 0


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    raise SystemExit(main())
