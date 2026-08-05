# -*- coding: utf-8 -*-
"""
bancada_dossie.py — Congela o insumo único da bancada Cafelana V7.

Todo modelo recebe exatamente o mesmo dossiê, byte a byte, e o hash disso é
registrado com cada execução. Sem isso a comparação não vale: bastaria um
modelo ter recebido um documento a mais para a diferença de qualidade virar
diferença de insumo.

Produz também o **ledger fechado de autoridades** — o conjunto de julgados que
existe no dossiê. É a régua do gate de invenção: autoridade citada na peça e
ausente deste conjunto ou vem marcada `[A CONFERIR]`, ou é afirmação sem lastro.

Uso: python bancada_dossie.py [--verificar]
"""
from __future__ import annotations

import hashlib
import io
import json
import re
import sys
from pathlib import Path

BANCADA = Path(__file__).resolve().parent
FORJA = BANCADA.parent
FABRICA = FORJA.parent
CASO = FABRICA / "Cafelana" / "contrarrazões ao AgInt no AREsp nº 2.698.443D"

# Ordem deliberada: a peça-base primeiro, o diagnóstico depois, a voz do titular
# por último — é a ordem em que um advogado leria o caso ao assumir a V7.
PECAS_DO_DOSSIE = [
    ("PECA_BASE_V6", "_v6_2026-07-27/IMPUGNACAO_AGINT_CAFELANA_V6_27-07-2026_FONTE.md",
     "Texto integral da V6, entregue em 27/07/2026. É a base sobre a qual a V7 trabalha."),
    ("RELATORIO_V6", "_v6_2026-07-27/RELATORIO_V6_COMPARATIVO_E_MELHORIAS.md",
     "O que a V6 mudou, por quê, quais gates rodaram e quais pendências ficaram declaradas."),
    ("PARECER_HELENA_V6", "_v6_2026-07-27/F4_PARECER_HELENA.md",
     "Parecer estratégico obrigatório da fábrica sobre a V6."),
    ("PARECER_CICERO_V6", "_v6_2026-07-27/F4_PARECER_CICERO.md",
     "Parecer jurídico obrigatório da fábrica sobre a V6."),
    ("DIRETRIZES_HUMANAS", "PROTOCOLO_CAFELANA_AGINT_ARESP2698443_DIRETRIZES_HUMANAS.md",
     "Determinações do titular do escritório. Não são sugestões."),
    ("FEEDBACK_TITULAR", "PROTOCOLO_FEEDBACK_FABIO_2026-07-14.md",
     "Feedback humano registrado sobre versões anteriores."),
    ("CRONOLOGIA_AUDITADA", "CRONOLOGIA_PROCESSUAL_AUDITADA_2026-07-11.md",
     "Linha do tempo processual auditada, com identidade de cada ato."),
    ("MATRIZ_A8_A9", "MATRIZ_A8_X_A9_2026-07-14.md",
     "Matriz de comparação entre os dois acórdãos em disputa."),
    ("RED_TEAM_PROCESSUAL", "RED_TEAM_ACHADOS_PROCESSUAIS_2026-07-11.md",
     "Achados do red team processual sobre o caso."),
]

# Classes recursais e originárias que aparecem em peça de STJ. A captura é do
# NÚMERO, não do nome: o mesmo julgado aparece como "AgInt no AREsp n. 2.072.941"
# e como "AREsp 2.072.941", e tratá-los como autoridades diferentes inflaria
# artificialmente a contagem de invenção.
_CLASSES = (r"AgInt|AgRg|AgReg|EDcl|EREsp|EAREsp|EAg|REsp|AREsp|RE|ARE|QO|MS|HC|RHC|"
            r"Rcl|TP|SLS|SS|Pet|CC|IAC|ADI|ADC|ADPF")
# As fronteiras de palavra não são detalhe: sem elas, o "RE" da alternância casa
# dentro de "RECURSO", e "transitou em julgado em setembro de 2010" vira o
# julgado nº 2010. Foi assim que a bancada quase acusou o Opus 5 de inventar
# uma autoridade que era uma data.
_JULGADO = re.compile(
    rf"\b(?:{_CLASSES})\b[\s\w.º°]{{0,40}}?n?\.?\s*(\d{{1,3}}(?:\.\d{{3}})+|\d{{5,7}})",
    re.I)
# Ano solto nunca é número de processo. O filtro é explícito para que a regra
# fique legível, em vez de escondida no quantificador.
_ANO = re.compile(r"^(?:1[89]|20)\d{2}$")
_SUMULA = re.compile(r"S[úu]mula\s+(?:n\.?\s*)?(\d{1,3})", re.I)
_TEMA = re.compile(r"Tema\s+(?:Repetitivo\s+)?(?:n\.?\s*)?(\d{1,4})", re.I)


def _num(bruto: str) -> str:
    """Normaliza o número do julgado para comparação estável."""
    return re.sub(r"\D", "", bruto)


def autoridades(texto: str) -> dict[str, set[str]]:
    """Conjunto de autoridades citadas, por espécie."""
    return {
        "julgados": {_num(m.group(1)) for m in _JULGADO.finditer(texto)
                     if len(_num(m.group(1))) >= 5 and not _ANO.match(_num(m.group(1)))},
        "sumulas": {m.group(1) for m in _SUMULA.finditer(texto)},
        "temas": {m.group(1) for m in _TEMA.finditer(texto)},
    }


def montar() -> tuple[str, dict]:
    partes = [
        "# DOSSIÊ ÚNICO — CAFELANA V7 (bancada de modelos)",
        "",
        "Este dossiê é o insumo integral e exclusivo da tarefa. Ele é idêntico para",
        "todos os participantes e seu hash está registrado. Nenhum outro documento",
        "do acervo foi disponibilizado, e nenhum participante tem acesso ao trabalho",
        "de outro participante.",
        "",
    ]
    manifesto = []
    for rotulo, rel, papel in PECAS_DO_DOSSIE:
        caminho = CASO / rel
        if not caminho.is_file():
            raise SystemExit(f"insumo ausente do acervo: {rel}")
        conteudo = caminho.read_text(encoding="utf-8", errors="replace")
        manifesto.append({
            "rotulo": rotulo, "arquivo": rel, "papel": papel,
            "bytes": len(conteudo.encode("utf-8")),
            "sha256": hashlib.sha256(conteudo.encode("utf-8")).hexdigest(),
        })
        partes += [f"\n\n{'=' * 78}", f"## [{rotulo}] {papel}", f"{'=' * 78}\n", conteudo]

    dossie = "\n".join(partes)
    achados = autoridades(dossie)
    ledger = {
        "versao": "BANCADA-CAFELANA-V7-DOSSIE-v1",
        "sha256Dossie": hashlib.sha256(dossie.encode("utf-8")).hexdigest(),
        "bytes": len(dossie.encode("utf-8")),
        "pecas": manifesto,
        "autoridadesFechadas": {k: sorted(v) for k, v in achados.items()},
        "totalJulgados": len(achados["julgados"]),
    }
    return dossie, ledger


def main() -> int:
    dossie, ledger = montar()
    (BANCADA / "protocolo").mkdir(parents=True, exist_ok=True)
    alvo = BANCADA / "protocolo" / "DOSSIE.md"
    if "--verificar" in sys.argv and alvo.is_file():
        atual = hashlib.sha256(alvo.read_text(encoding="utf-8").encode("utf-8")).hexdigest()
        ok = atual == ledger["sha256Dossie"]
        print(f"dossiê {'ÍNTEGRO' if ok else 'DIVERGENTE'}: {atual[:16]}")
        return 0 if ok else 1
    alvo.write_text(dossie, encoding="utf-8")
    (BANCADA / "protocolo" / "DOSSIE_LEDGER.json").write_text(
        json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"dossiê congelado: {ledger['bytes'] / 1024:.0f} KB · "
          f"{len(ledger['pecas'])} peças · sha256 {ledger['sha256Dossie'][:16]}")
    print(f"ledger fechado: {ledger['totalJulgados']} julgados · "
          f"{len(ledger['autoridadesFechadas']['sumulas'])} súmulas · "
          f"{len(ledger['autoridadesFechadas']['temas'])} temas")
    return 0


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    raise SystemExit(main())
