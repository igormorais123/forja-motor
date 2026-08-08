# -*- coding: utf-8 -*-
"""Mutação semântica (M3.1 do plano 19 — critério 3 de promoção N4).

A mutação literal (forja_case_tests.run_suite) remove/insere o texto exigido e
mede se a suíte percebe. Esta camada muda o SENTIDO JURÍDICO da minuta com
operadores determinísticos por família de risco e mede se o pipeline
(suíte de testes do caso + forja_verificador) mata o mutante:

  S1 inversão de tese        "é cabível" -> "não é cabível"
  S2 troca de parte          agravante <-> agravado, autor <-> réu
  S3 troca de valor/data     ano +1, primeiro dígito do valor rotacionado
  S4 troca de pedido         provimento <-> desprovimento, procedência <-> improcedência
  S5 sobreabstração          "REsp 1.234.567/DF" -> "a jurisprudência pacífica"
  S6 deturpação de precedente "firmou entendimento" -> "afastou o entendimento";
                              troca STJ <-> STF no par súmula×tribunal

Cada família também tem CONTROLES BENIGNOS (paráfrases neutras) que NÃO podem
ser mortos — suíte que mata controle é excesso de rigidez, não qualidade.

Determinismo: todas as regras são regex fixas aplicadas à N-ésima ocorrência;
mesmo texto -> mesmos mutantes -> mesmo score. O JSON de saída registra cada
mutante (família, regra, trecho antes/depois) e serve de corpus versionável.

Uso: python forja_mutation_semantic.py <case_dir|trecho-do-caseId> [--draft caminho.md]
Saída: n4_artifacts/F7_SEMANTIC_MUTATION.json + resumo no stdout.
Exit: 0 score >= 0.8 e nenhum controle morto; 1 caso contrário; 2 erro de uso.
"""
from __future__ import annotations

import io
import json
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

from forja_case_tests import _deterministic
from forja_verificador import verificar

RAIZ = Path(__file__).resolve().parent
ALVO_SCORE = 0.8
MAX_POR_REGRA = 2   # até 2 ocorrências mutadas por regra (mutantes distintos)

# ---------------------------------------------------------------- operadores
# Cada regra: (regex, substituição). A substituição pode usar grupos \1..\9.
OPERADORES: dict[str, list[tuple[str, str]]] = {
    "S1_inversao_tese": [
        # duas sutilezas propositais: "incabível" é pegável por teste `contains`
        # exigindo o trecho; "não é cabível" AINDA CONTÉM "é cabível" e por isso
        # atravessa qualquer suíte contains — sobrevivente aqui é sinal honesto
        # de que falta detector semântico, não defeito do motor.
        (r"\b([EéÉ]) cabível\b", r"\1 incabível"),
        (r"\b([EéÉ]|são) cabíve(l|is)\b", r"não \1 cabíve\2"),
        (r"\bdeve(m)? ser (provid[oa]s?|acolhid[oa]s?|reformad[oa]s?|mantid[oa]s?)\b",
         r"não deve\1 ser \2"),
        (r"\bmerece(m)? (provimento|acolhimento|reforma|prosperar)\b", r"não merece\1 \2"),
        (r"\brestou (comprovad[oa]|demonstrad[oa]|configurad[oa])\b", r"não restou \1"),
        (r"\bassiste razão\b", r"não assiste razão"),
        (r"\bfaz(em)? jus\b", r"não faz\1 jus"),
        (r"\b([EéÉ]) devid[oa]\b", r"não \1 devida"),
    ],
    "S2_troca_de_parte": [
        # troca simétrica via placeholder — altera quem pede e quem sofre
        (r"\bagravante(s)?\b", "__SWAP__agravado\\1"),
        (r"\bagravad[oa](s)?\b", "__SWAP__agravante\\1"),
        (r"\bapelante(s)?\b", "__SWAP__apelado\\1"),
        (r"\bapelad[oa](s)?\b", "__SWAP__apelante\\1"),
        (r"\bembargante(s)?\b", "__SWAP__embargado\\1"),
        (r"\bembargad[oa](s)?\b", "__SWAP__embargante\\1"),
        (r"\bautor(es|a|as)?\b", "__SWAP__réu"),
        (r"\bré[us]s?\b", "__SWAP__autor"),
        (r"\bexequente(s)?\b", "__SWAP__executado\\1"),
        (r"\bexecutad[oa](s)?\b", "__SWAP__exequente\\1"),
        (r"\brecorrente(s)?\b", "__SWAP__recorrido\\1"),
        (r"\brecorrid[oa](s)?\b", "__SWAP__recorrente\\1"),
    ],
    "S3_valor_ou_data": [
        # ano de data por extenso ou numérica: +1
        (r"\b(\d{1,2} de (?:janeiro|fevereiro|março|abril|maio|junho|julho|agosto|"
         r"setembro|outubro|novembro|dezembro) de )(\d{4})\b", "__ANO_MAIS_UM__"),
        (r"\b(\d{2}/\d{2}/)(\d{4})\b", "__ANO_MAIS_UM__"),
        # primeiro dígito do valor monetário rotacionado (R$ 165.000 -> R$ 265.000)
        (r"R\$ ?(\d)([\d\.]*,\d{2})", "__DIGITO_MAIS_UM__"),
        (r"\b(\d{1,3}(?:[\.,]\d)?) ?%", "__DIGITO_MAIS_UM_PCT__"),
    ],
    "S4_troca_de_pedido": [
        (r"\bprovimento\b", "desprovimento"),
        (r"\bdesprovimento\b", "provimento"),
        (r"\bprocedência\b", "improcedência"),
        (r"\bimprocedência\b", "procedência"),
        (r"\bacolhimento\b", "rejeição"),
        (r"\bpedido principal\b", "pedido subsidiário"),
    ],
    "S5_sobreabstracao": [
        (r"\b(?:AREsp|AgInt no AREsp|REsp|AgRg no REsp|RE|ARE)\s*(?:n[ºo.]?\s*)?"
         r"[\d\.\-–]+(?:/[A-Z]{2})?",
         "a jurisprudência pacífica dos tribunais superiores"),
        (r"\bSúmula\s*(?:n[ºo.]?\s*)?\d+(?:\s*(?:do|da|/)\s*(?:STJ|STF))?",
         "o entendimento sumulado aplicável"),
        (r"\bart(?:igo)?\.?\s*[\d\.]+(?:,\s*(?:§\s*\d+º?|inciso\s+[IVXL]+|caput))?"
         r"\s*(?:do|da)\s*(?:CPC|CC|CF|CDC|Código de Processo Civil|Código Civil)",
         "a legislação de regência"),
    ],
    "S6_deturpacao_precedente": [
        (r"\bfirmou(-se)? (o )?entendimento\b", r"afastou\1 \2entendimento"),
        (r"\bassentou\b", "rejeitou"),
        (r"\bconsolidou\b", "superou"),
        (r"\bpacificou\b", "controverteu"),
        # par súmula×tribunal trocado (G4 do verificador deve pegar)
        (r"\b(Súmula\s*(?:n[ºo.]?\s*)?\d+)(\s*(?:do|/)\s*)STJ\b", r"\1\2STF"),
        (r"\b(Súmula\s*(?:n[ºo.]?\s*)?\d+)(\s*(?:do|/)\s*)STF\b", r"\1\2STJ"),
    ],
}

# paráfrases neutras — mutante benigno que NÃO pode ser morto
CONTROLES_BENIGNOS: list[tuple[str, str, str]] = [
    ("neutro_conectivo", r"\bNesse contexto\b", "Nesse cenário"),
    ("neutro_conectivo2", r"\bAdemais\b", "Outrossim"),
    ("neutro_conectivo3", r"\bDessa forma\b", "Desse modo"),
    ("neutro_verbo", r"\bcumpre (destacar|registrar)\b", r"cabe \1"),
    ("neutro_adverbio", r"\bportanto\b", "por conseguinte"),
]


def _ano_mais_um(m: re.Match) -> str:
    return m.group(1) + str(int(m.group(2)) + 1)


def _aplicar(texto: str, padrao: str, subst: str, ocorrencia: int) -> str | None:
    """Aplica a regra na N-ésima ocorrência (0-based). None se não aplicável."""
    matches = list(re.finditer(padrao, texto, re.I))
    if len(matches) <= ocorrencia:
        return None
    m = matches[ocorrencia]
    if subst == "__ANO_MAIS_UM__":
        novo = _ano_mais_um(m)
    elif subst in ("__DIGITO_MAIS_UM__", "__DIGITO_MAIS_UM_PCT__"):
        if subst == "__DIGITO_MAIS_UM__":
            novo = "R$ " + str((int(m.group(1)) + 1) % 10 or 1) + m.group(2)
        else:
            bruto = m.group(1)
            primeiro = str((int(bruto[0]) + 1) % 10 or 1)
            novo = primeiro + bruto[1:] + "%"
    else:
        novo = m.expand(subst).replace("__SWAP__", "")
    mutado = texto[:m.start()] + novo + texto[m.end():]
    return mutado if mutado != texto else None


def _ocorrencias_a_mutar(texto: str, padrao: str) -> list[int]:
    """Índices das ocorrências a mutar: as primeiras MAIS a última.

    O orçamento por regra continua sendo `MAX_POR_REGRA`; muda só *quais*
    ocorrências entram. Incluir a última é o que faz a bateria alcançar o
    requerimento, no fim da peça. O número de mutantes por regra não aumenta,
    então o escore permanece comparável em denominador.
    """
    total = len(list(re.finditer(padrao, texto, re.I)))
    if total <= MAX_POR_REGRA:
        return list(range(total))
    escolhidos = list(range(MAX_POR_REGRA - 1)) + [total - 1]
    return sorted(set(escolhidos))


def _achados_por_gate(texto: str, case_dir: Path | None = None) -> Counter:
    """Conta detecções por gate e severidade, inclusive avisos P1.

    O escore mede se a alteração semântica foi percebida. Um P1 continua sendo
    não bloqueante no fluxo de produção, mas é uma detecção válida no medidor;
    limitar a comparação a P0 tornaria o S5 impossível de medir.
    """
    try:
        return Counter((v["gate"], v.get("sev", "P0")) for v in verificar(texto, "peca", case_dir=case_dir))
    except Exception:
        return Counter()


def _suite_mata(suite: dict, texto: str) -> str | None:
    """Retorna o testId que reprovou, ou None se a suíte não percebeu."""
    for t in suite.get("tests") or []:
        if t.get("severity") != "blocking":
            continue
        if t.get("method") not in {"deterministic", "deterministic_plus_semantic"}:
            continue
        status, _ = _deterministic(t, texto)
        if status != "pass":
            return t.get("testId")
    return None


def rodar(suite: dict, draft_path: Path, case_dir: Path | None = None) -> dict:
    texto = draft_path.read_text(encoding="utf-8-sig", errors="replace")
    base_achados = _achados_por_gate(texto, case_dir=case_dir)

    # Gate de sanidade (anti-autocertificação): se a suíte reprova o ORIGINAL,
    # o canal case_test mataria QUALQUER mutante e o score 1.0 seria falso
    # (visto no primeiro run real, 12/07 — minuta errada dava 24/24 fake).
    killer_original = _suite_mata(suite, texto)
    suite_valida = killer_original is None
    if not suite_valida:
        suite = {"tests": []}  # só o canal do verificador conta; score fica honesto

    def matou(mutado: str) -> tuple[bool, str | None]:
        killer = _suite_mata(suite, mutado)
        if killer:
            return True, f"case_test:{killer}"
        novos = _achados_por_gate(mutado, case_dir=case_dir)
        for (gate, sev), n in novos.items():
            if n > base_achados.get((gate, sev), 0):
                return True, f"verificador:{gate}:{sev}"
        return False, None

    mutantes, por_familia = [], {}
    for familia, regras in OPERADORES.items():
        stats = {"aplicaveis": 0, "mortos": 0}
        for i_regra, (padrao, subst) in enumerate(regras):
            # Quais ocorrências mutar. Antes eram sempre as `MAX_POR_REGRA`
            # PRIMEIRAS, e isso deixava um buraco sistemático: a mutação caía
            # sempre no começo do documento, e o REQUERIMENTO — que fica no fim
            # e é onde a cliente pede em nome próprio — nunca era exercitado.
            # Inverter o pedido no fecho é a alteração mais perigosa que existe
            # numa peça, e era justamente a que a bateria não gerava. Agora as
            # ocorrências são amostradas ao longo do texto, incluindo sempre a
            # última. O total por regra não muda.
            for oc in _ocorrencias_a_mutar(texto, padrao):
                mutado = _aplicar(texto, padrao, subst, oc)
                if mutado is None:
                    break
                stats["aplicaveis"] += 1
                killed, killer = matou(mutado)
                stats["mortos"] += killed
                m = list(re.finditer(padrao, texto, re.I))[oc]
                mutantes.append({
                    "mutationId": f"SEM-{familia}-r{i_regra}-o{oc}",
                    "familia": familia, "regra": padrao,
                    "antes": texto[max(0, m.start()-30):m.end()+30].replace("\n", " "),
                    "killed": killed, "killer": killer,
                })
        stats["score"] = round(stats["mortos"] / stats["aplicaveis"], 4) if stats["aplicaveis"] else None
        por_familia[familia] = stats

    controles = []
    for nome, padrao, subst in CONTROLES_BENIGNOS:
        mutado = _aplicar(texto, padrao, subst, 0)
        if mutado is None:
            continue
        killed, killer = matou(mutado)
        controles.append({"controle": nome, "killed": killed, "killer": killer})

    aplicaveis = sum(f["aplicaveis"] for f in por_familia.values())
    mortos = sum(f["mortos"] for f in por_familia.values())
    score = round(mortos / aplicaveis, 4) if aplicaveis else 0.0
    fam_fracas = [f for f, s in por_familia.items()
                  if s["aplicaveis"] and (s["score"] or 0) < ALVO_SCORE]
    controles_mortos = [c for c in controles if c["killed"]]

    return {
        "schemaVersion": 1,
        "artifactType": "F7_SEMANTIC_MUTATION",
        "generatedAt": datetime.now().astimezone().isoformat(timespec="seconds"),
        "draft": str(draft_path),
        "semanticMutationScore": score,
        "alvo": ALVO_SCORE,
        "suiteValida": suite_valida,
        "suiteReprovaOriginal": killer_original,
        "aprovado": score >= ALVO_SCORE and not controles_mortos and suite_valida,
        "aplicaveis": aplicaveis, "mortos": mortos,
        "porFamilia": por_familia,
        "familiasAbaixoDoAlvo": fam_fracas,           # pendência nominada, nunca silenciosa
        "controlesBenignos": controles,
        "controlesMortos": [c["controle"] for c in controles_mortos],
        "mutantes": mutantes,
    }


def _achar_caso(chave: str) -> Path:
    p = Path(chave)
    if p.is_dir():
        return p
    if str(chave).startswith("case-"):
        m = sorted((RAIZ / "state").glob(str(chave)))
    else:
        m = sorted((RAIZ / "state").glob(f"case-*{chave}*"))
    if not m:
        raise SystemExit(f"caso não encontrado para '{chave}'")
    return m[0]


def _achar_draft(case_dir: Path) -> Path | None:
    # 1º o texto canônico do ciclo N4 (é contra ele que a suíte foi escrita)
    canonico = case_dir / "n4_cycle_m6" / "CANONICAL_TEXT_FROM_FINAL_DOCX.txt"
    if canonico.is_file():
        return canonico
    manifest = case_dir / "FORJA_CASE_MANIFEST.json"
    try:
        reg = json.loads(manifest.read_text(encoding="utf-8"))
        registro = reg.get("n4SourceRegistry") or {}
        # `canonical_markdown` entrou depois de `draft`: casos entregues não
        # guardam minuta, guardam o texto canônico da peça que saiu. Sem esta
        # chave o caso CASO-04 AgInt — que é a Impugnação ao Agravo Interno, o
        # caso mais difícil do acervo e o único com fonte externa registrada
        # para a identidade das partes — simplesmente não entrava na bateria.
        for chave in ("draft", "canonical_markdown"):
            cand = (registro.get(chave) or {}).get("path")
            if cand and Path(cand).is_file():
                return Path(cand)
    except (OSError, json.JSONDecodeError):
        pass
    md = sorted((case_dir / "producao").glob("*.md"),
                key=lambda x: x.stat().st_size, reverse=True)
    md = [x for x in md if x.name not in ("MAPA_IA.md", "RELATORIO_MELHORIAS.md",
                                          "F4_BLUEPRINT.md")]
    return md[0] if md else None


def main(argv=None) -> int:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    argv = argv if argv is not None else sys.argv[1:]
    if not argv:
        print(__doc__)
        return 2
    case_dir = _achar_caso(argv[0])
    draft = Path(argv[argv.index("--draft") + 1]) if "--draft" in argv else _achar_draft(case_dir)
    suite_path = case_dir / "n4_artifacts" / "F4_CASE_ACCEPTANCE_TESTS.json"
    if draft is None or not draft.is_file():
        print(json.dumps({"erro": "minuta não localizada", "caso": str(case_dir)}, ensure_ascii=False))
        return 2
    suite = {}
    if suite_path.is_file():
        suite = json.loads(suite_path.read_text(encoding="utf-8"))
    resultado = rodar(suite, draft, case_dir=case_dir)
    resultado["caseId"] = case_dir.name
    resultado["suite"] = str(suite_path) if suite_path.is_file() else None

    out = case_dir / "n4_artifacts" / "F7_SEMANTIC_MUTATION.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(resultado, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"caso: {case_dir.name}")
    print(f"semanticMutationScore: {resultado['semanticMutationScore']} "
          f"({resultado['mortos']}/{resultado['aplicaveis']} mortos, alvo {ALVO_SCORE})")
    for f, s in resultado["porFamilia"].items():
        print(f"  {f}: {s['mortos']}/{s['aplicaveis']}"
              + (f" (score {s['score']})" if s["score"] is not None else " (não aplicável)"))
    if resultado["familiasAbaixoDoAlvo"]:
        print("FAMÍLIAS ABAIXO DO ALVO: " + ", ".join(resultado["familiasAbaixoDoAlvo"]))
    if resultado["controlesMortos"]:
        print("CONTROLES BENIGNOS MORTOS (rigidez excessiva): "
              + ", ".join(resultado["controlesMortos"]))
    if not resultado["suiteValida"]:
        print(f"AVISO: suíte reprova o ORIGINAL ({resultado['suiteReprovaOriginal']}) — "
              "minuta errada? Score usa só o canal do verificador; reprovado por regra.")
    print(f"-> {out}")
    return 0 if resultado["aprovado"] else 1


if __name__ == "__main__":
    sys.exit(main())
