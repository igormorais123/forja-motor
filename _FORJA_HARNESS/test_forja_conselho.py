# -*- coding: utf-8 -*-
"""test_forja_conselho.py — o gate do conselho sabe dizer não, e não trava o certo.

Contexto. `helena_present`, `cicero_present` e `council_decisions_recorded` eram
escritos pelo próprio agente da fase F4: nove execuções, nove `pass`, zero
reprovações. Um `pass` falso ali significa peça indo para redação sem o conselho
que a casa tornou obrigatório em 09/07/2026.

As duas listas têm o mesmo peso:

  DEVE_REPROVAR   — as formas de burlar o conselho sem mentir explicitamente:
                    parecer ausente, esqueleto criado para o gate ficar verde,
                    parecer sem recomendações decidíveis, deliberação sem estado.
  NAO_PODE_TRAVAR — os pareceres REAIS já aprovados pelo escritório. Gate que
                    reprova o padrão aprovado pelo dono está errado, não a peça.

Uso: python test_forja_conselho.py   (exit 0 = ok; exit 1 = regressão)
"""
from __future__ import annotations

import io
import json
import sys
import tempfile
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from forja_conselho import validar_conselho  # noqa: E402

PARECER_OK = """# F4 — PARECER HELENA

**Caso:** teste
**Método:** revisão estratégica sequencial.

## Veredito

Aprovado como parecer interno, com bloqueio expresso de protocolo até a
confirmação do prazo e das provas críticas do caso em exame.

## Recomendações

1. **Liderar pela resposta franca:** não afirmar o que a prova não sustenta,
   e condicionar o núcleo relevante à segmentação por matriz.

2. **Priorizar o protesto:** tratar o prazo como ação imediata e separar esse
   procedimento da futura cobrança, para não misturar riscos distintos.

3. **Converter a comunicação em projeto probatório:** arquivo original, trace,
   anexos, canal oficial, resposta e registro.

## Riscos residuais

O risco dominante segue sendo a prova de recebimento, que não está nos autos.

## Liberação

Liberado para revisão humana, não para protocolo.
"""

DECISOES_OK = """# Deliberações do conselho — F4

| ID | Decisão | Estado | Responsável humano | Evidência |
|---|---|---|---|---|
| D01 | acatar a recomendação 1 | acatada | Fábio | ata da reunião |
| D02 | rejeitar a recomendação 2 por prazo | rejeitada | Fábio | despacho interno |
"""

DECISOES_JSON = {
    "schemaVersion": 1,
    "decisions": [
        {"id": "D001", "decision": "accept", "recommendation": "R1",
         "rationale": "convergência dos pareceres"},
        {"id": "D002", "decision": "reject", "recommendation": "R2",
         "rationale": "prova insuficiente"},
    ],
}


def _escrever(base: Path, nome: str, conteudo: str) -> Path:
    caminho = base / nome
    caminho.write_text(conteudo, encoding="utf-8")
    return caminho


def main() -> int:
    falhas = 0
    casos = 0

    with tempfile.TemporaryDirectory() as d:
        base = Path(d)
        helena = _escrever(base, "helena.md", PARECER_OK)
        cicero = _escrever(base, "cicero.md", PARECER_OK.replace("HELENA", "CÍCERO"))
        decisoes = _escrever(base, "decisoes.md", DECISOES_OK)

        # Contraprova primeiro: o caminho íntegro não pode reprovar.
        casos += 1
        laudo = validar_conselho(helena=helena, cicero=cicero, decisoes=decisoes)
        if any(v != "pass" for v in laudo["gates"].values()):
            print(f"  FALHOU: conselho completo e bem formado reprovou: {laudo['gates']}")
            falhas += 1

        # Parecer ausente.
        casos += 1
        if validar_conselho(helena=None, cicero=cicero,
                            decisoes=decisoes)["gates"]["helena_present"] != "fail":
            print("  FALHOU: parecer de Helena ausente não reprovou")
            falhas += 1

        # Esqueleto criado só para o gate ficar verde.
        casos += 1
        vazio = _escrever(base, "vazio.md", "# F4 — PARECER HELENA\n\n1. ok\n")
        if validar_conselho(helena=vazio, cicero=cicero,
                            decisoes=decisoes)["gates"]["helena_present"] != "fail":
            print("  FALHOU: parecer-esqueleto passou como parecer")
            falhas += 1

        # Parecer longo, porém sem recomendação decidível.
        casos += 1
        sem_rec = _escrever(base, "sem_rec.md",
                            "# F4 — PARECER HELENA\n\n## Veredito\n\n" + ("Texto de análise. " * 90))
        if validar_conselho(helena=sem_rec, cicero=cicero,
                            decisoes=decisoes)["gates"]["helena_present"] != "fail":
            print("  FALHOU: parecer sem recomendações numeradas passou")
            falhas += 1

        # Deliberações ausentes.
        casos += 1
        if validar_conselho(helena=helena, cicero=cicero,
                            decisoes=None)["gates"]["council_decisions_recorded"] != "fail":
            print("  FALHOU: ausência de deliberações não reprovou")
            falhas += 1

        # Deliberação sem estado — a forma silenciosa de não decidir.
        casos += 1
        sem_estado = _escrever(base, "sem_estado.md", DECISOES_OK.replace("| acatada |", "|  |"))
        if validar_conselho(helena=helena, cicero=cicero,
                            decisoes=sem_estado)["gates"]["council_decisions_recorded"] != "fail":
            print("  FALHOU: deliberação sem estado passou")
            falhas += 1

        # Responsável ausente é P1: registra sem bloquear, porque decisão sem
        # dono é defeito de governança e não afirmação falsa.
        casos += 1
        sem_dono = _escrever(base, "sem_dono.md", DECISOES_OK.replace("| Fábio |", "| |"))
        laudo_dono = validar_conselho(helena=helena, cicero=cicero, decisoes=sem_dono)
        if laudo_dono["gates"]["council_decisions_recorded"] != "pass" or not any(
                a["sev"] == "P1" for a in laudo_dono["findings"]):
            print("  FALHOU: responsável ausente deveria gerar P1 sem bloquear")
            falhas += 1

        # O CASO-23 usa o dialeto JSON `decisions[]`. Ele deve ser lido
        # como deliberação real; a ausência de responsável continua sendo P1,
        # não motivo para transformar um registro existente em "ausente".
        casos += 1
        decisoes_json = _escrever(base, "decisoes.json", json.dumps(
            DECISOES_JSON, ensure_ascii=False))
        laudo_json = validar_conselho(helena=helena, cicero=cicero,
                                      decisoes=decisoes_json)
        if (laudo_json["gates"]["council_decisions_recorded"] != "pass"
                or not any(a["sev"] == "P1" for a in laudo_json["findings"])):
            print("  FALHOU: decisões JSON existentes foram tratadas como ausentes")
            falhas += 1

        # Resumo JSON sem uma decisão por recomendação permanece bloqueado.
        casos += 1
        resumo = _escrever(base, "resumo.json", json.dumps(
            {"decision": "approve", "rationale": ["prazo confirmado"]},
            ensure_ascii=False))
        if validar_conselho(helena=helena, cicero=cicero,
                            decisoes=resumo)["gates"]["council_decisions_recorded"] != "fail":
            print("  FALHOU: resumo JSON sem decisões por recomendação passou")
            falhas += 1

    # NÃO PODE TRAVAR — os pareceres reais do acervo, já aprovados.
    reais = 0
    for pasta in sorted(Path("state").glob("case-*")):
        helena, cicero = pasta / "F4_PARECER_HELENA.md", pasta / "F4_PARECER_CICERO.md"
        if not helena.is_file() or not cicero.is_file():
            continue
        reais += 1
        casos += 1
        laudo = validar_conselho(helena=helena, cicero=cicero, decisoes=None)
        travados = [nome for nome in ("helena_present", "cicero_present")
                    if laudo["gates"][nome] != "pass"]
        if travados:
            print(f"  TRAVOU O APROVADO: {pasta.name} reprovou em {travados}")
            falhas += 1

    if reais < 3:
        print(f"  FALHOU: só {reais} pareceres reais examinados — a contraprova perdeu o acervo")
        falhas += 1

    if falhas:
        print(f"REGRESSÃO: {falhas} de {casos} verificações do conselho falharam")
        return 1
    print(f"ok: {casos} verificações — o gate do conselho reprova as seis formas de burlá-lo "
          f"e não trava nenhum dos {reais} pareceres reais aprovados")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
