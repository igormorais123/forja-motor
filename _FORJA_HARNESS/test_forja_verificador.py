# -*- coding: utf-8 -*-
"""
test_forja_verificador.py — Regressão do verificador (rodar após QUALQUER mudança nele).

Duas listas, dois deveres:
  DEVE_PEGAR  -> erros reais dos casos 1-5; se algum passar, o verificador regrediu.
  NAO_PODE_TRAVAR -> textos corretos que já geraram falso positivo; se algum disparar P0,
                     o verificador virou trava e precisa ser recalibrado.

Uso: python test_forja_verificador.py   (exit 0 = ok; exit 1 = regressão)
"""
import hashlib
import json
import sys, io
import tempfile
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from forja_verificador import verificar

DEVE_PEGAR = [
    # (texto com erro real de caso, gate esperado)
    ("A CASO-17 pode promover execução fiscal contra o Município após a inscrição em Dívida Ativa.", "G5"),
    ("Súmula 7 do STF veda o reexame de prova.", "G4"),
    ("prescrição trienal de 3 anos (Código Civil, art. 205) aplicável ao caso", "G4"),
    ("Mandado de Segurança (CPC arts. 30-46) é via sumária.", "G4"),
    ("Responsabilidade: Helena (decisão) + Efesto (execução técnica).", "G1"),
    ("Celebrado em 30/08/2023, foi anulado 5 meses depois (17/06/2026).", "G7"),
    ("Conclusão: memorial pronto ✅", "G6"),
    ("Penhora de receita tributária (IPTU, ISS) do município bloqueia o caixa da prefeitura.", "G5"),
    ("[BLOQUEADOR CRÍTICO F7: VERIFICAR NOS AUTOS]", "G2"),
    ("O advogado é [NOME], inscrito na [OAB].", "G2"),
    ("Brasília/DF, [dia] de julho de 2026.", "G2"),
    ("## SÍNTESE EXECUTIVA (art. 343-A do Regimento Interno do TJTO)", "G4"),
    ("A tese depende de confirmação. [VERIFICAR EM FONTE OFICIAL]", "G2"),
    ("O laudo foi compartilhado pelo escritório e recebido por e-mail.", "G9"),
    (r"A prova está no caminho C:\Users\Equipe\processo\laudo.pdf.", "G9"),
    ("Não apenas a tese é frágil, mas também carece de prova.", "G10"),
    ("Vale destacar que, claramente, a medida é adequada.", "G10"),
    # G11 (emenda E9, 25/07/2026): regimento é norma mutável; citação sem
    # verbatim arquivado bloqueia, inclusive quando o artigo existe de fato.
    ("Conforme o art. 999 do RISTJ, o recurso é cabível.", "G11"),
    ("Na forma do art. 34 do RITJTO, compete à Turma julgar.", "G11"),
    ("O art. 343 do RISTJ trata de precatórios.", "G11"),
    ("Sustentação oral na forma do art. 159 do RITRF4.", "G11"),
]

NAO_PODE_TRAVAR = [
    # textos CORRETOS que não podem gerar P0
    "Não existe penhora de bens, rendas ou contas do Município: os bens públicos são impenhoráveis.",
    "Qualquer estratégia que prometa bloqueio de caixa do Município é juridicamente inviável.",
    "A votação ocorrerá antes do fim de julho, com o fim de se preservar o cronograma.",
    "P1: Qual é a força jurídica do Parecer 0491/2026?",
    "Súmula 473 do STF autoriza a autotutela administrativa.",
    "Súmula 7 do STJ veda o reexame de matéria fática.",
    "A decisão foi proferida pela Ministra Regina Helena Costa, Relatora no Superior Tribunal de Justiça.",
    "Celebrado em 30/08/2023 e homologado cerca de 12 meses depois (04/09/2024).",
    # art. 343-A do RISTJ existe (ER 53/2026, DJe 01/07/2026) — não pode travar
    "Em atenção ao art. 343-A do RISTJ, apresenta-se a síntese dos fundamentos de fato e de direito.",
    "## SÍNTESE EXECUTIVA (art. 343-A do RISTJ)",
    "A decisão consta do documento juntado aos autos no evento 185, fls. 59-62.",
    "Conforme o Doc. 03, anexo a esta manifestação, o pagamento ocorreu em 5 de maio.",
    # links markdown não são placeholder (falso positivo do dossiê Roraima, 10/07/2026)
    "Fontes: [Perfil do Senador](https://www25.senado.leg.br/web/senadores/senador/-/perfil/470) e [Senadores de RR](https://www25.senado.leg.br/web/senadores/por-uf/-/uf/RR).",
    "Contudo, o evento 185 contém o comprovante bancário de 5 de maio.",
    # o art. 343-A tem verbatim arquivado e conferido: citá-lo ao STJ é correto
    "O art. 343-A do Regimento Interno do Superior Tribunal de Justiça exige o resumo.",
    "O art. 1.021 do CPC disciplina o agravo interno.",
    "O recurso não trata da perícia contábil juntada no evento 12.",
]

falhas = []
for texto, gate in DEVE_PEGAR:
    tipo = "peca" if gate == "G9" else "estudo"
    achados = [x for x in verificar(texto, tipo) if x["gate"].startswith(gate)]
    if not achados:
        falhas.append("NAO PEGOU (" + gate + "): " + texto[:80])

for texto in NAO_PODE_TRAVAR:
    p0 = [x for x in verificar(texto, "estudo") if x["sev"] == "P0"]
    if p0:
        falhas.append("TRAVOU (P0 indevido): " + texto[:80] + " -> " + p0[0]["gate"] + ": " + p0[0]["problema"][:60])

# Contraprova Diabob: um ledger canônico quebrado não pode ser mascarado por
# snapshot histórico válido. A rota visual deve reprovar o insumo vigente,
# não escolher a versão mais conveniente.
with tempfile.TemporaryDirectory() as td:
    caso = Path(td)
    f3 = caso / "n3_artifacts" / "F3_FONTES_REGIMENTO_LEIS"
    f3.mkdir(parents=True)
    fonte = caso / "parecer_2026-07.md"
    fonte.write_text("Fonte econômica governante. Data-base: 2026-07.", encoding="utf-8")
    sha = hashlib.sha256(fonte.read_bytes()).hexdigest()
    ledger = {
        "schemaVersion": 2,
        "facts": [{
            "id": "F-PREV-001", "role": "fonte_prevalente",
            "validationStatus": "validado", "validadoPor": "advogado-teste",
            "validadoEm": "2026-08-04", "dataBase": "2026-07",
            "quoteSource": fonte.name, "sha256": sha, "support": [fonte.name],
            "quote": "Fonte econômica governante. Data-base: 2026-07.",
        }],
        "documentosExaminados": [fonte.name],
        "monetaryAnchors": [{"id": "A-VALOR-001", "value": "R$ 100.000,00",
                             "sourceIds": ["F-PREV-001"],
                             "proposicao": "Valor calculado R$ 100.000,00"}],
    }
    (f3 / "fact_ledger.json").write_text("{ ledger quebrado", encoding="utf-8")
    (f3 / "fact_ledger-snapshot.json").write_text(json.dumps(ledger), encoding="utf-8")
    achados = verificar(
        "Plano econômico. Data-base: 2026-07. Valor: R$ 100.000,00.",
        case_dir=caso, exigir_economico=True,
    )
    if not any(item.get("gate") == "L9-fonte-prevalente" and item.get("sev") == "P0"
               for item in achados):
        falhas.append("LEDGER CANÔNICO INVÁLIDO CAIU PARA SNAPSHOT HISTÓRICO")

if falhas:
    print("REGRESSAO DETECTADA (" + str(len(falhas)) + "):")
    for f in falhas:
        print("  -", f)
    sys.exit(1)
print("ok: " + str(len(DEVE_PEGAR)) + " detecções + " + str(len(NAO_PODE_TRAVAR)) + " não-travas confirmadas")
