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
        # Desde 06/08/2026 o conselho obrigatório tem TRÊS vozes: Helena, Cícero
        # e Diabob. O artefato do Diabob é o recibo da chamada, porque o que o
        # gate afere é a proveniência — contraditório de outra família de modelo,
        # não prosa dizendo que houve contraditório.
        diabob = _escrever(base, "diabob.json", json.dumps({
            "contrato": "FORJA-F4-PARECER-DIABOB-v1", "persona": "diabob",
            "modelo": "grok-4.5-cursor", "familia": "xai", "provedor": "cursor",
            "rotaDegradada": None, "parecer": "objeção fundamentada. " * 60,
        }, ensure_ascii=False))

        # Contraprova primeiro: o caminho íntegro não pode reprovar.
        casos += 1
        laudo = validar_conselho(helena=helena, cicero=cicero, decisoes=decisoes,
                                 diabob=diabob)
        if any(v != "pass" for v in laudo["gates"].values()):
            print(f"  FALHOU: conselho completo e bem formado reprovou: {laudo['gates']}")
            falhas += 1

        # O Diabob ausente não reprova retroativamente, mas também não passa:
        # fica sem veredito, que é a recusa de atestar o que não se viu.
        casos += 1
        sem_diabob = validar_conselho(helena=helena, cicero=cicero,
                                      decisoes=decisoes)["gates"]["diabob_present"]
        if sem_diabob != "unknown":
            print(f"  FALHOU: conselho sem Diabob devia ficar unknown, veio {sem_diabob!r}")
            falhas += 1

        # Contraditório da mesma família é eco, não red team.
        casos += 1
        eco = _escrever(base, "eco.json", json.dumps({
            "contrato": "FORJA-F4-PARECER-DIABOB-v1", "persona": "diabob",
            "modelo": "opus-5", "familia": "anthropic", "provedor": "local",
            "parecer": "objeção fundamentada. " * 60,
        }, ensure_ascii=False))
        if validar_conselho(helena=helena, cicero=cicero, decisoes=decisoes,
                            diabob=eco)["gates"]["diabob_present"] != "fail":
            print("  FALHOU: red team da mesma família do produtor não reprovou")
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

        # Recomendação numerada em negrito — como um parecer real da Helena a
        # escreveu, e como a primeira versão do gate a rejeitava. O gate acusava
        # de "sem recomendações numeradas" um documento com seis, porque cada
        # uma começava em `**1. ` e o `**` empurrava o dígito do início da linha.
        # Acusar de vazio o que está cheio é pior que não conferir: manda
        # reescrever o que já estava certo.
        casos += 1
        negrito = _escrever(base, "negrito.md",
                            "# F4 — PARECER HELENA\n\n" + ("Análise. " * 90) +
                            "\n\n## V. RECOMENDAÇÕES\n\n"
                            "**1. Estrutura narrativa:** iniciar pelo fumus.\n\n"
                            "**2. Peso do precedente:** diferenciar o voto divergente.\n\n"
                            "- **3.** conferir a data de intimação.\n")
        if validar_conselho(helena=negrito, cicero=cicero,
                            decisoes=decisoes)["gates"]["helena_present"] != "pass":
            print("  FALHOU: recomendação numerada em negrito foi tratada como ausente")
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
    em_curso = 0
    for pasta in sorted(Path("state").glob("case-*")):
        helena, cicero = pasta / "F4_PARECER_HELENA.md", pasta / "F4_PARECER_CICERO.md"
        if not helena.is_file() or not cicero.is_file():
            continue
        # Só ancora em caso que a esteira registrou. Um caso EM CURSO tem o
        # parecer no disco antes de estar pronto, e tratá-lo como aprovado faz o
        # teste dizer "TRAVOU O APROVADO" quando o gate está certo e o parecer é
        # que está incompleto — acusando o instrumento em vez do trabalho.
        if not (pasta / "FORJA_STATE.json").is_file():
            em_curso += 1
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
          f"e não trava nenhum dos {reais} pareceres reais aprovados"
          + (f"; {em_curso} caso(s) em curso ficaram de fora da âncora" if em_curso else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
