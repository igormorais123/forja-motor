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

2. Os dois esquemas discordam sobre o mesmo caso. O caso do plano de saúde
   tem 94 arquivos entregues na pasta da demanda; o legado o descreve como
   `F0_RECONCILIACAO_FILA / fulfilled`, carimbado vinte e três vezes, e o N3 o
   descreve como `fulfilled_by_forja_f10`. Dois registros de verdade divergentes,
   nenhum árbitro.

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

VERSAO = "FORJA-CENSO-v1"

# Vocabulário fechado. Situação fora desta tupla é erro de programação, não
# dado novo — pelo mesmo motivo que a causa de insumo bloqueado é fechada:
# rótulo livre deixa quem lê descobrindo sozinho qual era o problema.
SITUACOES = (
    "entregue",             # terminal com prova em disco
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
_LOCALIZADOR = re.compile(r"\b(?:19[0-9a-f]{14}|[0-9a-f]{16})\b")

_TERMINAIS = {"fulfilled", "fulfilled_by_forja_f10", "complete", "delivered", "closed",
              "superseded", "cumprida"}
_BLOQUEADOS = {"blocked", "bloqueada"}
_AGUARDANDO = {"draft_awaiting_review", "ready", "awaiting_review", "aguardando_revisao"}

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


def _evidencia(legado, n3) -> tuple[str | None, str]:
    """(localizador, detalhe) do que o painel registrou sobre a entrega."""
    for fonte in (legado, n3):
        ev = (fonte or {}).get("deliveryEvidence") or {}
        detalhe = str(ev.get("detail") or "").strip()
        if ev.get("status") in (None, "none", ""):
            continue
        achado = _LOCALIZADOR.search(detalhe)
        return (achado.group(0) if achado else None), detalhe
    return None, ""


def _situacao(legado, n3, provas, resolucao, existem) -> tuple[str, str]:
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
        localizador, _ = _evidencia(legado, n3)
        if localizador:
            return "entrega_declarada", (
                f"entrega registrada com localizador {localizador}, conferível contra a "
                "caixa de saída; sem artefato arquivado aqui")
        return "concluido_sem_prova", (
            "declarado cumprido, sem entregável em disco, sem localizador conferível "
            "e sem declaração de que não havia demanda")
    return "aberto", "trabalho por fazer"


def censo(state_root: Path | None = None, *, resolucoes: dict | None = None) -> dict:
    raiz = state_root or STATE
    resolvidos = carregar_resolucoes() if resolucoes is None else resolucoes
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
        situacao, porque = _situacao(legado, n3, provas, resolucao, existem)
        localizador, detalhe_evidencia = _evidencia(legado, n3)

        estado_legado = (legado or {}).get("status")
        estado_n3 = (n3 or {}).get("lifecycleStatus")
        divergem = bool(legado and n3 and estado_legado != estado_n3)

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
            "fase": (legado or {}).get("currentPhase"),
            "diasNaFase": dias,
            "faseDesde": desde,
            "carimbosRepetidos": max(0, carimbos - fases),
            "entregaveis": len(provas),
            "localizadorDaEntrega": localizador,
            "evidenciaDeclarada": detalhe_evidencia[:220] or None,
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
    declarada = dados["situacoes"]["entrega_declarada"]
    if declarada:
        achados.append({"id": "CEN5", "sev": "P1", "quantos": declarada,
                        "texto": "entrega registrada com localizador e sem artefato arquivado — "
                                 "é conferível e não foi conferida, o que é dívida de auditoria "
                                 "e não de trabalho"})
    if dados["divergentes"]:
        achados.append({"id": "CEN3", "sev": "P1", "quantos": dados["divergentes"],
                        "texto": "os dois esquemas de estado discordam sobre o mesmo caso; "
                                 "não há árbitro entre eles"})
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
        print(f"\n  esquemas divergentes {dados['divergentes']:>3}")

    if achados:
        print("\nachados:")
        for a in achados:
            print(f"  [{a['sev']}] {a['id']} ({a['quantos']}) {a['texto']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
