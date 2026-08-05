# -*- coding: utf-8 -*-
"""
test_forja_lastro.py — Regressão da blindagem contra lastro aparente.

Duas listas, dois deveres:
  DEVE_PEGAR      -> as frases e ledgers que produziram alucinação real no caso
                     CASO-23. Se alguma passar, a blindagem regrediu.
  NAO_PODE_TRAVAR -> texto correto que usa as mesmas palavras de forma legítima.
                     Se algum disparar P0, o gate virou trava.

O segundo bloco é o mais importante. Gate contra alucinação que reprova texto
honesto é pior que gate nenhum: ensina a contornar em vez de conferir.

Uso: python test_forja_lastro.py   (exit 0 = ok; exit 1 = regressão)
"""
import io
import hashlib
import json
import shutil
import sys
import tempfile
from pathlib import Path

import forja_acervo

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from forja_lastro import (  # noqa: E402
    analisar_texto,
    fatos_sem_lastro,
    exigir_criterio_vigente,
    validar_decisoes_revisao,
    validar_lastro_fatos,
    validar_gates_economicos,
    validar_valores_monetarios,
)

# --------------------------------------------------------------------------
# Gates lexicais — frases reais das versões defeituosas da minuta
# --------------------------------------------------------------------------
DEVE_PEGAR = [
    # L3 — o erro exato da versão 3: REsp não conhecido descrito como confirmação
    ("O Recurso Especial 780.605/RS não foi conhecido pela Segunda Turma. A delimitação "
     "foi confirmada em todas as instâncias.", "L3"),
    ("O recurso não foi conhecido, mas a decisão foi mantida pelo STJ.", "L3"),
    ("Questão encerrada nestes autos.", "L3"),
    ("A matéria foi decidida em três instâncias.", "L3"),
    ("O ponto é incontroverso.", "L3"),

    # L4 — troca de denominador no meio da frase
    ("Cerca de 93% dessa distância é explicada por uma quebra de escala monetária.", "L4"),
    ("Aproximadamente 80% da diferença decorre do critério de câmbio.", "L4"),

    # L5 — o P0 mais grave do caso
    ("O AI 9000015-00.2019.4.04.0000 envolve as mesmas partes e a mesma liquidação.", "L5"),
    ("Trata-se do mesmo título executivo já reconhecido.", "L5"),
    ("A controvérsia corre nos mesmos autos.", "L5"),

    # L6 — o ano que não existia
    ("Normas de 2002, 2016 e 2018 não podem explicar operações de 1982 a 1990.", "L6"),
    ("O laudo apoia-se em normas dos anos de 2004 e 2022.", "L6"),
]

NAO_PODE_TRAVAR = [
    # L3 — a formulação correta, que substituiu a errada na versão 5
    "O recurso especial não foi conhecido. A via recursal foi esgotada e o acórdão "
    "permaneceu incólume, sem substituição pelo tribunal superior.",
    # não conhecimento sozinho, sem afirmação de confirmação
    "O Recurso Especial 780.605/RS não foi conhecido por ausência de prequestionamento, "
    "com incidência da Súmula 211 do Superior Tribunal de Justiça.",
    # confirmação legítima, sem não conhecimento no documento
    "O acórdão foi confirmado pelo Superior Tribunal de Justiça no julgamento do agravo interno.",

    # L4 — percentual com base nomeada é o padrão desejado
    "A linha de janeiro de 1989 responde por 93,37% do principal corrigido do Anexo I.",
    "A SELIC corresponde a 423,94% do valor apurado a título de principal.",

    # L5 — identidade afirmada com os dois números à vista
    "O AI 9000015-00.2019.4.04.0000 foi julgado na liquidação 9000014-00.2016.4.04.0000, "
    "que não é a mesma liquidação destes autos, 9000011-00.2018.4.04.0000.",
    # negação de identidade não pode travar
    "Não se trata da mesma liquidação: os títulos executivos são distintos.",

    # L6 — normas nomeadas, que é exatamente o que o gate quer forçar
    "O laudo apura o crédito com base no art. 18 da Lei 10.637/2002, verifica a "
    "classificação pela TIPI do Decreto 8.950/2016 e converte o câmbio pelo art. 14 da "
    "Lei 9.430/1996. Normas de 2002, 2016 e 1996 não constituem direito material de 1982.",

    # As duas frases da versão corrigida da minuta que o gate reprovou na primeira
    # tentativa. São exatamente a redação que a blindagem quer produzir: negar a
    # identidade e negar o denominador vago. Se voltarem a travar, o gate virou
    # armadilha contra a própria correção que ele provocou.
    "Envolve as mesmas partes, o mesmo juízo e a mesma questão de direito, mas não a "
    "mesma liquidação.",
    "O que está demonstrado é que 93,37% do principal do Anexo I depende de uma linha "
    "inconsistente, e não que 93% da diferença para a conta judicial esteja explicada.",

    # texto neutro do domínio, que não pode disparar nada
    "A perícia deve produzir duas trilhas de cálculo e conservar fórmula visível em cada linha.",
]


def _rodar_lexicais() -> tuple[int, int]:
    falhas = 0
    for texto, gate in DEVE_PEGAR:
        achados = analisar_texto(texto)
        if not any(a["gate"].startswith(gate) for a in achados):
            print(f"  FALHOU (não pegou {gate}): {texto[:78]}")
            falhas += 1
    for texto in NAO_PODE_TRAVAR:
        p0 = [a for a in analisar_texto(texto) if a["sev"] == "P0"]
        if p0:
            print(f"  TRAVOU INDEVIDAMENTE ({p0[0]['gate']}): {texto[:78]}")
            falhas += 1
    return len(DEVE_PEGAR) + len(NAO_PODE_TRAVAR), falhas


# --------------------------------------------------------------------------
# L1/L2 — lastro do ledger
# --------------------------------------------------------------------------
def _rodar_lastro(tmp) -> tuple[int, int]:
    falhas = 0
    casos = 0

    # L1: a forma exata do F012 que passou por três camadas de revisão
    casos += 1
    f012 = {"facts": [{
        "id": "F012",
        "claim": "O AI 5039469, entre as mesmas partes e relacionado à mesma liquidação, "
                 "reconheceu a aplicabilidade da CIEX.",
        "status": "confirmed_document",
        "support": ["E252-ANEXO-AI-p20-31"],
    }]}
    achados = validar_lastro_fatos(f012)
    if not any(a["gate"] == "L1-lastro" and a["sev"] == "P0" for a in achados):
        print("  FALHOU: F012 sem transcrição não foi bloqueado")
        falhas += 1

    # L1: pendência declarada é P1, não P0 — mas continua bloqueando promoção.
    # Inventar a transcrição para o gate ficar verde é o comportamento que a
    # blindagem inteira existe para desencorajar.
    casos += 1
    pendente = {"facts": [{
        "id": "F001", "status": "confirmed_document", "support": ["E228-p1"],
        "groundingPending": True}]}
    ach = validar_lastro_fatos(pendente)
    if not ach or ach[0]["sev"] != "P1" or ach[0]["gate"] != "L1-lastro-pendente":
        print("  FALHOU: pendência declarada não foi classificada como P1 declarado")
        falhas += 1
    if "F001" not in fatos_sem_lastro(pendente):
        print("  FALHOU: pendência declarada saiu da lista de bloqueio de promoção")
        falhas += 1

    # L1 negativo: fato honesto sobre o que é não pode ser cobrado de transcrição
    casos += 1
    inferencia = {"facts": [{
        "id": "F024", "claim": "Homogeneizada a escala, o principal cairia para ~13,8 milhões.",
        "status": "legal_inference", "support": ["PARTE_8-p1002"]}]}
    if validar_lastro_fatos(inferencia):
        print("  FALHOU: inferência declarada como tal foi cobrada de transcrição")
        falhas += 1

    # L1 positivo: fato com transcrição passa
    casos += 1
    com_quote = {"facts": [{
        "id": "F016", "status": "confirmed_document", "support": ["PARTE_8-p637"],
        "quote": "Deverá apresentar dois cálculos de liquidação atualizados, um apurando "
                 "diferenças para o período de 10/1982 a 12/1988",
    }]}
    if [a for a in validar_lastro_fatos(com_quote) if a["sev"] == "P0"]:
        print("  FALHOU: fato com transcrição adequada foi bloqueado")
        falhas += 1

    # L2: transcrição que não existe na fonte apontada
    casos += 1
    fonte = tmp / "fonte.txt"
    fonte.write_text("A decisão determinou dois cálculos, um para 10/1982 a 12/1988.",
                     encoding="utf-8")
    inventado = {"facts": [{
        "id": "F900", "status": "confirmed_document", "support": ["p1"],
        "quote": "A decisão reconheceu expressamente a aplicabilidade da Resolução CIEX",
        "quoteSource": "fonte.txt"}]}
    if not any(a["gate"] == "L2-transcricao" and a["sev"] == "P0"
               for a in validar_lastro_fatos(inventado, base_dir=tmp)):
        print("  FALHOU: transcrição inexistente na fonte não foi bloqueada")
        falhas += 1

    # L2 negativo: transcrição real, com acento e quebra de linha, precisa passar
    casos += 1
    fonte2 = tmp / "fonte2.txt"
    fonte2.write_text("...um apurando diferenças para o perí-\nodo de 10/1982 a 12/1988, "
                      "uma vez que a análise da prescrição...", encoding="utf-8")
    real = {"facts": [{
        "id": "F901", "status": "confirmed_document", "support": ["p1"],
        "quote": "um apurando diferencas para o periodo de 10/1982 a 12/1988",
        "quoteSource": "fonte2.txt"}]}
    if [a for a in validar_lastro_fatos(real, base_dir=tmp) if a["sev"] == "P0"]:
        print("  FALHOU: transcrição real com acento/hifenação foi rejeitada")
        falhas += 1

    # Vocabulário: o ledger real da CASO-04 usava 'documented_fact' e
    # 'official_current_source' enquanto o gate só conhecia os prefixos
    # 'confirmed_'. Resultado medido em 04/08/2026: 0 de 11 fatos auditados, com
    # saída idêntica à de um ledger aprovado. Estes dois casos existem para que
    # essa cobertura silenciosamente vazia não volte.
    casos += 1
    vocab_real = {"facts": [{
        "id": "F-R-001", "classification": "documented_fact", "support": ["COMANDO.md"]}]}
    if not any(a["gate"] == "L1-lastro" and a["sev"] == "P0"
               for a in validar_lastro_fatos(vocab_real)):
        print("  FALHOU: 'documented_fact' sem transcrição não foi auditado")
        falhas += 1

    casos += 1
    vocab_oficial = {"facts": [{
        "id": "F-OFFICIAL-001", "classification": "official_current_source",
        "support": ["planalto.md"]}]}
    if not any(a["gate"] == "L1-lastro" for a in validar_lastro_fatos(vocab_oficial)):
        print("  FALHOU: 'official_current_source' sem transcrição não foi auditado")
        falhas += 1

    # Não-trava do par: status desconhecido AVISA em P1, nunca bloqueia — mas
    # também não pode passar calado, que era o defeito.
    casos += 1
    desconhecido = {"facts": [{"id": "F-X-001", "classification": "vocabulario_novo"}]}
    ach_desc = validar_lastro_fatos(desconhecido)
    if not any(a["gate"] == "L1-status-desconhecido" and a["sev"] == "P1" for a in ach_desc):
        print("  FALHOU: status desconhecido passou silenciosamente pelo gate")
        falhas += 1
    if any(a["sev"] == "P0" for a in ach_desc):
        print("  FALHOU: status desconhecido virou bloqueio em vez de aviso")
        falhas += 1

    casos += 1
    isento = {"facts": [{"id": "F-S-001", "classification": "documented_strategy"}]}
    if validar_lastro_fatos(isento):
        print("  FALHOU: status isento por natureza gerou achado")
        falhas += 1

    # L2 sobre fonte binária: antes desta guarda, transcrição correta tirada de
    # um PDF era acusada de ter sido reconstruída de memória — a acusação mais
    # grave do módulo, contra quem fez certo. E o laudo prevalente da CASO-04
    # tem 2,14 GB, que seriam lidos inteiros na memória.
    casos += 1
    pdf = tmp / "laudo.pdf"
    pdf.write_bytes(b"%PDF-1.4\n\xff\xfe\x00\x01binario\x80\x90\n%%EOF")
    do_pdf = {"facts": [{
        "id": "F-FP-001", "classification": "confirmed_document", "support": ["fls. 975/2.515"],
        "quote": "HOMOLOGO o laudo pericial carreado as fls. 975/2.515 dos autos, "
                 "determinando o regular prosseguimento do feito",
        "quoteSource": "laudo.pdf"}]}
    ach_pdf = validar_lastro_fatos(do_pdf, base_dir=tmp)
    if any(a["sev"] == "P0" for a in ach_pdf):
        print("  FALHOU: transcrição de fonte binária foi acusada de invenção (P0)")
        falhas += 1
    if not any(a["gate"] == "L2-transcricao-manual" and a["sev"] == "P1" for a in ach_pdf):
        print("  FALHOU: fonte binária não foi sinalizada para conferência humana")
        falhas += 1

    # Não-trava: fonte de texto continua sendo conferida de verdade. Sem este
    # caso, a guarda acima poderia ser afrouxada até desligar o L2 inteiro.
    casos += 1
    txt = tmp / "conferivel.txt"
    txt.write_text("trecho que existe mesmo no arquivo apontado", encoding="utf-8")
    falso = {"facts": [{
        "id": "F-FP-002", "classification": "confirmed_document", "support": ["p1"],
        "quote": "trecho que jamais foi escrito neste arquivo de apoio",
        "quoteSource": "conferivel.txt"}]}
    if not any(a["gate"] == "L2-transcricao" and a["sev"] == "P0"
               for a in validar_lastro_fatos(falso, base_dir=tmp)):
        print("  FALHOU: a guarda de binário desligou o L2 para fonte de texto")
        falhas += 1

    # L7: ausência de critério vigente declarado
    casos += 1
    if not any(a["gate"] == "L7-criterio-vigente" for a in exigir_criterio_vigente(f012)):
        print("  FALHOU: ausência de critério vigente não foi bloqueada")
        falhas += 1

    casos += 1
    com_criterio = {"facts": [{
        "id": "F030", "status": "confirmed_document", "role": "criterio_vigente",
        "support": ["PARTE_8-p1117"],
        "quote": "mantenho a decisão do evento 192.1 em todos os seus termos"}]}
    if exigir_criterio_vigente(com_criterio):
        print("  FALHOU: critério vigente devidamente declarado foi bloqueado")
        falhas += 1

    # L8: objeção acatada contra afirmação com lastro, sem reabrir a fonte
    casos += 1
    revisao = {"objections": [{
        "id": "sol-24-periodos", "decision": "acatada",
        "targetHadSupport": True, "sourceReopened": False}]}
    if not any(a["gate"] == "L8-objecao" for a in validar_decisoes_revisao(revisao)):
        print("  FALHOU: objeção acatada sem reabrir a fonte não foi bloqueada")
        falhas += 1

    casos += 1
    revisao_ok = {"objections": [
        {"id": "sol-24-periodos", "decision": "acatada",
         "targetHadSupport": True, "sourceReopened": True},
        {"id": "grok-a", "decision": "acatada", "targetHadSupport": False},
        {"id": "sol-tema333", "decision": "rejeitada", "targetHadSupport": True},
    ]}
    if validar_decisoes_revisao(revisao_ok):
        print("  FALHOU: decisões de revisão corretas foram bloqueadas")
        falhas += 1

    return casos, falhas


# --------------------------------------------------------------------------
# Acoplamento: o gate precisa ser elo bloqueante, não módulo decorativo
# --------------------------------------------------------------------------
def _rodar_acoplamento() -> tuple[int, int]:
    import json
    from pathlib import Path
    falhas = 0
    casos = 0

    # O contrato de F7 tem de exigir o gate; sem isso, forja_run nunca o cobra.
    casos += 1
    f7 = json.loads(Path("phase_contracts/F7.json").read_text(encoding="utf-8"))
    if "fact_grounding_verbatim" not in f7["requiredGates"]:
        print("  FALHOU: F7 não exige fact_grounding_verbatim")
        falhas += 1

    casos += 1
    if "fact_grounding_verbatim" not in (f7.get("gateNotes") or {}):
        print("  FALHOU: gate sem nota explicando a âncora — vira regra órfã")
        falhas += 1

    # A entrega tem de ter o elo 9-B; sem ele, o gate não bloqueia o que importa.
    casos += 1
    entrega = Path("forja_delivery.py").read_text(encoding="utf-8")
    if "fatos_sem_lastro" not in entrega or "9-B" not in entrega:
        print("  FALHOU: forja_delivery não usa fatos_sem_lastro no elo 9-B")
        falhas += 1

    # Verificador tem de rodar os gates lexicais em todo render.
    casos += 1
    verif = Path("forja_verificador.py").read_text(encoding="utf-8")
    if "forja_lastro" not in verif:
        print("  FALHOU: forja_verificador não chama os gates lexicais de lastro")
        falhas += 1

    # A entrada visual canônica e o compositor precisam carregar o mesmo
    # contexto documental; sem isso o produto econômico escapa do verificador
    # antes de chegar ao PecaVisual.salvar().
    casos += 1
    visual_build = Path("forja_visual_build.py").read_text(encoding="utf-8")
    visual = Path("forja_visual.py").read_text(encoding="utf-8")
    if ("exigir_economico=material_economico(texto)" not in visual_build
            or "case_dir=case_dir" not in visual_build
            or "exigir_economico=material_economico(texto_md)" not in visual
            or "case_dir=case_dir" not in visual):
        print("  FALHOU: rota visual canônica não propaga o gate econômico/contexto")
        falhas += 1

    # O runner precisa recomputar L1/L2/L7; verificar apenas strings de contrato
    # não prova que o agente não possa se autoaprovar.
    casos += 1
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        produto = root / "final_markdown.md"
        ledger = root / "fact_ledger.json"
        produto.write_text("# Parecer\n\nTexto factual sem transcrição.", encoding="utf-8")
        ledger.write_text(json.dumps({"facts": [{"id": "F-RUN", "status": "confirmed_document",
                                                   "support": ["fonte.txt"]}]}), encoding="utf-8")
        from forja_run import _compute_lastro_gates
        report = _compute_lastro_gates(
            "F7_AUDITORIA_JURIDICA_FACTUAL",
            [{"artifactId": "fact_ledger", "source": ledger},
             {"artifactId": "final_markdown", "source": produto}],
            {"inputs": {}, "lastro": {"exigirCriterioVigente": True}},
        )
        if not report.get("applicable") or report["computed"].get("fact_grounding_verbatim") != "fail" or not report["findings"]:
            print("  FALHOU: runner não recomputa L1/L2/L7 contra artefatos reais")
            falhas += 1

        # O caso acima declara `fact_ledger` — que NENHUMA execução real declara.
        # Medido em 04/08/2026: 7 F7 no acervo, 0 COMPUTED_LASTRO_GATES.json. O
        # teste passava e a produção não auditava nada, porque o ledger de fatos
        # é promovido pela F3 na pasta do caso e o F7 nunca o cita. Os dois
        # canários abaixo fixam a descoberta e a ausência.
        casos += 1
        caso_raiz = root / "case-x"
        promovido = caso_raiz / "n3_artifacts" / "F3_FONTES_REGIMENTO_LEIS"
        promovido.mkdir(parents=True)
        (promovido / "fact_ledger.json").write_text(ledger.read_text(encoding="utf-8"), encoding="utf-8")
        attempt = caso_raiz / "runs" / "r1" / "F7" / "attempt-1"
        attempt.mkdir(parents=True)
        produto_caso = attempt / "final_markdown.md"
        produto_caso.write_text("# Parecer\n\nTexto factual.", encoding="utf-8")
        report_desc = _compute_lastro_gates(
            "F7_AUDITORIA_JURIDICA_FACTUAL",
            [{"artifactId": "final_markdown", "source": produto_caso}],
            {"inputs": {}},
        )
        if not report_desc.get("applicable") or not report_desc["findings"] or \
                any(a["gate"] == "L0-recomputo-sem-insumo" for a in report_desc["findings"]):
            print("  FALHOU: runner não descobre o fact_ledger promovido pela F3 no caso")
            falhas += 1

        # Sem ledger em lugar nenhum, a saída não pode ser `not_applicable`:
        # essa saída é indistinguível de aprovação (MC-15).
        casos += 1
        report_sem = _compute_lastro_gates(
            "F7_AUDITORIA_JURIDICA_FACTUAL",
            [{"artifactId": "final_markdown", "source": produto}],
            {"inputs": {}},
        )
        if not any(a["gate"] == "L0-recomputo-sem-insumo" for a in report_sem.get("findings") or []):
            print("  FALHOU: F7 sem ledger de fatos passa em silêncio")
            falhas += 1

    # Ledger vazio, chave trocada e status ausente — as três formas de o gate
    # rodar sobre conjunto vazio e devolver verde.
    from forja_lastro import validar_lastro_fatos, validar_fonte_prevalente, validar_aritmetica_derivada
    for rotulo, entrada in (("ledger sem chave facts", {}),
                            ("facts vazio", {"facts": []}),
                            ("facts não-lista", {"facts": {}}),
                            ("chave 'claims' em vez de 'facts'",
                             {"claims": [{"status": "confirmed_document"}]})):
        casos += 1
        if not any(a["sev"] == "P0" for a in validar_lastro_fatos(entrada)):
            print(f"  FALHOU: {rotulo} não gera P0")
            falhas += 1

    casos += 1
    sem_status = validar_lastro_fatos({"facts": [{"id": "F-X", "support": ["a.md"]}]})
    if not any(a["gate"] == "L1-status-ausente" for a in sem_status):
        print("  FALHOU: fato sem status escapa de L1/L2 sem deixar rastro")
        falhas += 1

    # Traversal na fonte prevalente: o hash não pode provar um arquivo que o
    # próprio fato escolheu fora da pasta do caso.
    casos += 1
    with tempfile.TemporaryDirectory() as d:
        raiz = Path(d)
        caso_dir = raiz / "caso"
        caso_dir.mkdir()
        fora = raiz / "fora.md"
        fora.write_text("conteudo controlado pelo agente", encoding="utf-8")
        led = {"facts": [{"id": "F-TRAV", "role": "fonte_prevalente",
                          "validationStatus": "validado", "validadoPor": "x",
                          "validadoEm": "2026-08-04", "quoteSource": "../fora.md",
                          "sha256": hashlib.sha256(fora.read_bytes()).hexdigest()}]}
        if not validar_fonte_prevalente(led, base_dir=caso_dir):
            print("  FALHOU: fonte prevalente fora da pasta do caso é aceita por traversal")
            falhas += 1

    # O ataque descrito pela revisão Codex: prefixar o próprio cálculo com `>`
    # não pode mais tirá-lo da análise de órfão. A tipografia continua gerando
    # P2 para a proveniência incompleta, mas o valor também recebe a conferência
    # normal de âncora U6; apenas origem externa ou regra normativa é isenção.
    from forja_lastro import _valores_monetarios, validar_valores_monetarios
    casos += 1
    ataque = validar_valores_monetarios("> R$ 88.412.900,15 — cálculo próprio do escritório.", {})
    if not any(a["gate"] == "L11-isencao-tipografica" for a in ataque):
        print("  FALHOU: valor com '>' sem origem não registra a proveniência frágil")
        falhas += 1
    if not any(a["gate"] == "L11-valor-orfao" and a["sev"] == "P1" for a in ataque):
        print("  FALHOU: valor com '>' sem origem ainda escapa da âncora U6")
        falhas += 1
    valores_ataque = _valores_monetarios("> R$ 88.412.900,15 — cálculo próprio do escritório.")
    if not valores_ataque or valores_ataque[0].get("citado") or valores_ataque[0].get("proveniencia") != "tipografia_sem_origem":
        print("  FALHOU: tipografia sozinha foi aceita como citação confirmada")
        falhas += 1

    casos += 1
    lavado_depois = _valores_monetarios(
        "> R$ 88.412.900,15 — cálculo próprio do escritório. Consulte o laudo citado depois."
    )
    if not lavado_depois or lavado_depois[0].get("citado"):
        print("  FALHOU: referência alheia posterior lavou cálculo próprio tipografado")
        falhas += 1

    casos += 1
    legitima = validar_valores_monetarios('O laudo pericial fixou "R$ 524.141.077,62" na liquidação.', {})
    valores_legitima = _valores_monetarios('O laudo pericial fixou "R$ 524.141.077,62" na liquidação.')
    if any(a["gate"] == "L11-isencao-tipografica" for a in legitima) or not valores_legitima or not valores_legitima[0].get("citado"):
        print("  FALHOU: citação com origem alheia declarada não pode virar isenção frágil")
        falhas += 1

    # Escritores de DOCX dentro de `state/` gravam o produto sem passar pelo
    # verificador nem pelos gates de lastro. Os três abaixo são históricos —
    # registro do que foi feito naquelas entregas, e apagá-los destruiria trilha
    # de auditoria para fechar um buraco que só abre se alguém os rodar à mão.
    # O risco é o PRÓXIMO. Por isso o conjunto fica congelado: um escritor novo
    # sob `state/` reprova aqui e exige decisão explícita. Parecer Efesto de
    # 04/08/2026.
    casos += 1
    conhecidos = set(forja_acervo.valor("escritores-docx-sob-state-conhecidos") or [])
    if not conhecidos:
        print("  FALHOU: " + forja_acervo.motivo_da_ausencia(
            "escritores-docx-sob-state-conhecidos"))
        falhas += 1
    achados_state = set()
    for py in Path("state").rglob("*.py"):
        try:
            corpo = py.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if ".save(" in corpo and ("Document(" in corpo or "docx" in corpo.lower()):
            achados_state.add(py.relative_to("state").as_posix())
    novos = achados_state - conhecidos
    if novos:
        print(f"  FALHOU: escritor(es) de DOCX novo(s) sob state/ fora das rotas canônicas: {sorted(novos)}")
        falhas += 1

    # `economic_gates` tem de distinguir severidade: enquanto qualquer achado
    # L9-L13 virava `fail`, bloquear nessa flag promoveria o L11 a P0 pela porta
    # dos fundos, com os ~55% de falso positivo da heurística junto. Parecer
    # Helena de 04/08/2026: `fail` só com P0 econômico.
    from forja_run import _severidade_economica
    for rotulo, entrada, esperado in (
            ("sem achado econômico", [{"gate": "L2-transcricao", "sev": "P0"}], "pass"),
            ("só P1 econômico", [{"gate": "L11-valor-orfao", "sev": "P1"}], "warn"),
            ("P0 econômico", [{"gate": "L9-fonte-prevalente", "sev": "P0"}], "fail")):
        casos += 1
        if _severidade_economica(entrada) != esperado:
            print(f"  FALHOU: economic_gates com {rotulo} deveria ser {esperado}")
            falhas += 1

    # Operação desconhecida não pode cair no ramo da multiplicação.
    casos += 1
    led_sub = {"derivedCalculations": [{"id": "c1", "operation": "subtract",
                                        "baseValue": "R$ 100,00", "percentage": 10,
                                        "expectedValue": "R$ 10,00"}]}
    if not validar_aritmetica_derivada("Valor derivado: R$ 10,00.", led_sub):
        print("  FALHOU: L13 aprova subtração recomposta como multiplicação")
        falhas += 1

    return casos, falhas


# --------------------------------------------------------------------------
# FORJA-LASTRO-v2 — fonte prevalente, valores e as três rotas do D3
# --------------------------------------------------------------------------
def _fonte_ledger(base: Path, *, nome="parecer_2026-07.md", data="2026-07",
                  status="validado", sha_override=None, anchors=None, **extra):
    caso = base / ("fixture_" + Path(nome).stem)
    caso.mkdir(parents=True, exist_ok=True)
    fonte = caso / nome
    fonte.write_text("Fonte econômica governante. Data-base: " + data + ".", encoding="utf-8")
    sha = hashlib.sha256(fonte.read_bytes()).hexdigest()
    fato = {
        "id": "F-PREV-001", "role": "fonte_prevalente", "validationStatus": status,
        "validadoPor": "advogado-teste", "validadoEm": "2026-08-04T10:00:00-03:00",
        "dataBase": data, "quoteSource": nome, "sha256": sha_override or sha,
        "support": [nome], "quote": "Fonte econômica governante. Data-base: " + data + ".",
    }
    ledger = {
        "schemaVersion": 2, "facts": [fato],
        "documentosExaminados": [nome],
        "monetaryAnchors": anchors or [],
    }
    ledger.update(extra)
    return ledger, fonte


def _ancora(raw="R$ 100.000,00"):
    return {"id": "A-VALOR-001", "value": raw, "sourceIds": ["F-PREV-001"],
            "proposicao": f"Valor calculado {raw} da fonte prevalente F-PREV-001"}


def _rodar_v2(tmp: Path) -> tuple[int, int]:
    """Cenários do plano 41 + pares de não-trava, com fixture real T1."""
    falhas = 0
    casos = 0

    def caso(nome, cond, detalhe=""):
        nonlocal falhas, casos
        casos += 1
        if not cond:
            print(f"  FALHOU v2: {nome}" + (f" — {detalhe}" if detalhe else ""))
            falhas += 1

    # O insumo é material de cliente e vem do acervo por chave: o motor não
    # escreve caminho de pasta de caso. Acervo ausente NÃO vira aprovação — o
    # caso é reportado como não verificado.
    real = forja_acervo.caminho("plano-economico-real")
    caso("T1 fixture real do acervo existe", real is not None and real.is_file(),
         str(real) if real else forja_acervo.motivo_da_ausencia("plano-economico-real"))
    texto_real = real.read_text(encoding="utf-8", errors="replace") if (real and real.is_file()) else ""
    ach = validar_gates_economicos(texto_real, ledger={})
    caso("T1 produto real sem fonte prevalente bloqueia L9", any(a["gate"] == "L9-fonte-prevalente" for a in ach), str(ach[:2]))

    texto_ok = "Plano econômico CASO-04. Data-base: jul/2026. Valor da faixa: R$ 100.000,00."
    ledger_ok, fonte_ok = _fonte_ledger(tmp, anchors=[_ancora()])
    ach = validar_gates_economicos(texto_ok, ledger=ledger_ok, base_dir=fonte_ok.parent)
    caso("T2 fonte validada, data-base e âncora completas passam", not ach, str(ach))
    ach_desativado = validar_gates_economicos(
        texto_ok, ledger=ledger_ok, base_dir=fonte_ok.parent, exigir=False
    )
    caso("T2 caller não pode desligar L9-L13 em produto econômico",
         any(a["gate"] == "L0-economico-desativado" and a["sev"] == "P0"
             for a in ach_desativado), str(ach_desativado))

    ach_l11_desativado = validar_valores_monetarios(
        texto_ok, ledger_ok, exigir=False
    )
    caso("T2 chamada direta não pode desligar L11 em produto econômico",
         any(a["gate"] == "L0-economico-desativado" and a["sev"] == "P0"
             for a in ach_l11_desativado), str(ach_l11_desativado))

    texto_t3 = texto_ok.replace("jul/2026", "ago/2026")
    ach = validar_gates_economicos(texto_t3, ledger=ledger_ok, base_dir=fonte_ok.parent)
    caso("T3 data-base divergente bloqueia L10", any(a["gate"] == "L10-data-base" for a in ach), str(ach))

    ledger_t4, fonte_t4 = _fonte_ledger(tmp, nome="parecer_t4_2026-07.md", anchors=[])
    ach = validar_gates_economicos(texto_ok, ledger=ledger_t4, base_dir=fonte_t4.parent)
    caso("T4 valor sem âncora bloqueia L11", any(a["gate"] == "L11-valor-orfao" for a in ach), str(ach))

    ledger_t5, fonte_t5 = _fonte_ledger(tmp, nome="parecer_t5_2026-07.md", sha_override="0" * 64, anchors=[_ancora()])
    ach = validar_gates_economicos(texto_ok, ledger=ledger_t5, base_dir=fonte_t5.parent)
    caso("T5 hash divergente bloqueia L9", any(a["gate"] == "L9-fonte-prevalente" for a in ach), str(ach))

    # A fonte prevalente real da CASO-04 é um PDF de 2,14 GB. A integridade
    # precisa ser conferida em fluxo; read_bytes() aqui seria um risco de OOM.
    lastro_src = Path(__file__).with_name("forja_lastro.py").read_text(encoding="utf-8")
    caso("L9 calcula SHA-256 da fonte em fluxo",
         "def _sha256_file" in lastro_src
         and "atual = _sha256_file(caminho)" in lastro_src
         and "sha = _sha256_file(caminho)" in lastro_src)

    texto_t6 = "O RE 1.395.147/PR e a Lei 10.201/2020 são citados apenas como autoridades."
    caso("T6 peça jurídica sem conteúdo econômico não incide", not validar_gates_economicos(texto_t6, ledger={}, base_dir=tmp))

    ledger_t7, fonte_t7 = _fonte_ledger(tmp, nome="parecer_t7_2026-07.md", status="proposto", anchors=[_ancora()])
    ach = validar_gates_economicos(texto_ok, ledger=ledger_t7, base_dir=fonte_t7.parent)
    caso("T7 fonte proposta (não validada) bloqueia L9", any(a["gate"] == "L9-fonte-prevalente" for a in ach), str(ach))

    pasta_hier = tmp / "hierarquia"
    pasta_hier.mkdir()
    parecer = pasta_hier / "parecer_eleito_2026-06.md"
    laudo = pasta_hier / "laudo_posterior_2026-07.md"
    parecer.write_text("Parecer econômico. Data-base: 2026-06.", encoding="utf-8")
    laudo.write_text("Laudo econômico posterior. Data-base: 2026-07.", encoding="utf-8")
    sha_parecer = hashlib.sha256(parecer.read_bytes()).hexdigest()
    ledger_hier = {
        "facts": [{"id": "F-HIER", "role": "fonte_prevalente", "validationStatus": "validado",
                   "validadoPor": "advogado-teste", "validadoEm": "2026-08-04", "dataBase": "2026-06",
                   "quoteSource": parecer.name, "sha256": sha_parecer}],
        "documentosExaminados": [parecer.name, laudo.name],
        "monetaryAnchors": [_ancora()],
    }
    texto_hier = "Plano econômico. Data-base: 2026-06. Valor: R$ 100.000,00."
    ach = validar_gates_economicos(texto_hier, ledger=ledger_hier, base_dir=pasta_hier)
    caso("T8 laudo posterior não eleito bloqueia L12", any(a["gate"] == "L12-hierarquia-fonte" for a in ach), str(ach))

    ledger_hier["descartesFonte"] = [{"path": laudo.name, "motivo": "laudo posterior fora do escopo da base validada"}]
    caso("T9 concorrente com descarte escrito não trava", not any(a["gate"] == "L12-hierarquia-fonte" for a in validar_gates_economicos(texto_hier, ledger=ledger_hier, base_dir=pasta_hier)))

    ledger_t10, fonte_t10 = _fonte_ledger(tmp, nome="parecer_t10_2026-07.md", anchors=[_ancora("R$ 120.000,00")],
                                  derivedCalculations=[{"id": "faixa", "label": "faixa derivada", "baseValue": "R$ 100.000,00",
                                                        "percentage": 10, "expectedValue": "R$ 120.000,00", "tolerance": 0.01}])
    texto_t10 = "Plano econômico. Data-base: 2026-07. Faixa derivada: R$ 120.000,00."
    ach = validar_gates_economicos(texto_t10, ledger=ledger_t10, base_dir=fonte_t10.parent)
    caso("T10 derivação incompatível bloqueia L13", any(a["gate"] == "L13-aritmetica-derivada" for a in ach), str(ach))

    # T11 — rota visual única/ad hoc. O builder não recebe ledger e, portanto,
    # não pode persistir o DOCX econômico.
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_FERRAMENTAS"))
        from medina_visual_kit import PecaVisual
        alvo = tmp / "ad_hoc.docx"
        pv = PecaVisual(str(alvo))
        pv.par("Valor econômico: R$ 100.000,00")
        try:
            pv.salvar()
            t11_bloqueou = False
        except RuntimeError:
            t11_bloqueou = True
        caso("T11 PecaVisual.salvar bloqueia script ad hoc econômico", t11_bloqueou)
        caso("T11 nenhum DOCX econômico parcial permanece", not alvo.exists())

        # Contraprova Diabob da rota direta: ledger explicitamente apontado
        # quebrado não pode ser trocado pelo canônico válido do caso.
        caso_exp = tmp / "case-ledger-explicito-invalido"
        promovido_exp = caso_exp / "n3_artifacts" / "F3_FONTES_REGIMENTO_LEIS"
        promovido_exp.mkdir(parents=True)
        fonte_exp = caso_exp / "parecer_2026-07.md"
        fonte_exp.write_text("Fonte econômica governante. Data-base: 2026-07.", encoding="utf-8")
        ledger_exp, _ = _fonte_ledger(tmp, nome="parecer_2026-07.md", anchors=[_ancora()])
        # A fixture helper calcula o hash da cópia equivalente; a fonte precisa
        # ser a mesma do case para L9 não mascarar o teste de precedência.
        ledger_exp["facts"][0]["sha256"] = hashlib.sha256(fonte_exp.read_bytes()).hexdigest()
        ledger_exp["facts"][0]["quoteSource"] = fonte_exp.name
        ledger_exp["facts"][0]["support"] = [fonte_exp.name]
        ledger_exp["facts"][0]["quote"] = fonte_exp.read_text(encoding="utf-8")
        ledger_exp["documentosExaminados"] = [fonte_exp.name]
        (promovido_exp / "fact_ledger.json").write_text(json.dumps(ledger_exp), encoding="utf-8")
        invalido_exp = tmp / "ledger-explicito-quebrado.json"
        invalido_exp.write_text("{ ledger quebrado", encoding="utf-8")
        alvo_exp = tmp / "ad_hoc_com_ledger_invalido.docx"
        pv_exp = PecaVisual(str(alvo_exp), case_dir=str(caso_exp),
                            ledger_path=str(invalido_exp), base_dir=str(caso_exp))
        pv_exp.par("Valor econômico: R$ 100.000,00")
        try:
            pv_exp.salvar()
            explicito_bloqueou = False
        except RuntimeError:
            explicito_bloqueou = True
        caso("T11 ledger explícito inválido não cai para canônico do caso", explicito_bloqueou)
        caso("T11 nenhum DOCX nasce com ledger explícito inválido", not alvo_exp.exists())

        # Contraprova Diabob: caminho explicitamente escolhido, mas ausente,
        # também é insumo quebrado. Não pode ser tratado como convite para
        # autodiscovery do ledger válido no case_dir.
        ausente_exp = tmp / "ledger-explicito-ausente.json"
        alvo_ausente = tmp / "ad_hoc_com_ledger_ausente.docx"
        pv_ausente = PecaVisual(str(alvo_ausente), case_dir=str(caso_exp),
                                ledger_path=str(ausente_exp), base_dir=str(caso_exp))
        pv_ausente.par("Plano econômico. Data-base: 2026-07. Valor: R$ 100.000,00.")
        try:
            pv_ausente.salvar()
            ausente_bloqueou = False
        except RuntimeError:
            ausente_bloqueou = True
        caso("T11 ledger explícito ausente não cai para canônico do caso", ausente_bloqueou)
        caso("T11 nenhum DOCX nasce com ledger explícito ausente", not alvo_ausente.exists())
    except Exception as exc:
        caso("T11 rota visual executável", False, repr(exc))

    # T11-B — entrada oficial visual. O pré-gate deve bloquear antes de
    # gerar mapa, figuras ou DOCX quando falta contexto econômico.
    md = tmp / "visual_build_economico.md"
    md.write_text("# Estudo econômico\n\nData-base: 2026-07. Valor: R$ 100.000,00.", encoding="utf-8")
    out = tmp / "visual_build_out"
    try:
        from forja_visual_build import build
        build(md, out, "Estudo econômico", montar_word=False)
        t11b_bloqueou = False
    except RuntimeError:
        t11b_bloqueou = True
    caso("T11-B entrada forja_visual_build bloqueia antes da composição", t11b_bloqueou)
    caso("T11-B nenhum DOCX nasce antes do lastro", not list(out.glob("*.docx")) if out.exists() else True)

    # Contraprova obrigatória do D3: a proteção econômica não pode transformar
    # toda entrada visual em bloqueio. As rotas direta e canônica precisam
    # continuar produzindo um documento não econômico sem contexto de ledger.
    texto_ne = "A autoridade competente decidiu pela manutenção do ato administrativo."
    alvo_ne = tmp / "ad_hoc_nao_economico.docx"
    try:
        pv_ne = PecaVisual(str(alvo_ne))
        pv_ne.par(texto_ne)
        pv_ne.salvar()
        caso("T11-NE PecaVisual não econômica permanece verde", alvo_ne.is_file())
    except Exception as exc:
        caso("T11-NE PecaVisual não econômica permanece verde", False, repr(exc))

    md_ne = tmp / "visual_build_nao_economico.md"
    md_ne.write_text("# Estudo\n\n" + texto_ne, encoding="utf-8")
    out_ne = tmp / "visual_build_nao_economico_out"
    try:
        resumo_ne = build(md_ne, out_ne, "Estudo", montar_word=False)
        docx_ne = Path(resumo_ne["docx"])
        caso("T11-NE entrada visual canônica permanece verde", docx_ne.is_file())
        caso("T11-NE entrada visual sem P0 econômico", resumo_ne["gatesForjaVerificador"]["p0"] == 0)
        # A régua tipográfica sempre rodou dentro do build; até 04/08/2026 o
        # veredito dela morria no F8_QA_ESTRUTURAL.json e não aparecia no resumo
        # que o operador lê. Medição sem consequência visível é a mesma coisa que
        # medição nenhuma — este caso guarda a presença do veredito, não o seu
        # valor: reprovar a peça é decisão de política presa ao F8-S.
        vl = resumo_ne.get("veredictoLayout") or {}
        caso("T11-NE veredito de layout chega ao resumo do build",
             "aprovado" in vl and isinstance(vl.get("achadosP0"), list)
             and isinstance(vl.get("cobertura"), dict))
        caso("T11-NE veredito de layout traz as três coberturas medidas",
             {"justificationCoverage", "fontCoverage", "sizeCoverage"}
             <= set(vl.get("cobertura") or {}))
    except Exception as exc:
        caso("T11-NE entrada visual canônica permanece verde", False, repr(exc))

    # Par de não-trava do L10, L11 e L13, e determinismo (T12).
    texto_fmt = texto_ok.replace("jul/2026", "2026-07")
    caso("não-trava L10 jul/2026 e 2026-07 são equivalentes", not any(a["gate"] == "L10-data-base" for a in validar_gates_economicos(texto_fmt, ledger=ledger_ok, base_dir=fonte_ok.parent)))
    citado = 'Conforme o acórdão, “o valor de R$ 9.000.000,00 foi mencionado pela parte adversária”.'
    caso("não-trava L11 valor de terceiro em transcrição", not any(a["gate"] == "L11-valor-orfao" for a in validar_gates_economicos(citado, ledger={}, base_dir=tmp)))

    # O marcador de moeda decide se os gates L9-L13 rodam. "R $" com espaço não
    # é português correto e não existe no acervo (conferido em 04/08/2026 sobre
    # todos os .md), mas nasce de OCR e de colagem de PDF — e a falha seria
    # silenciosa: peça com cifra sem lastro simplesmente não seria auditada.
    # A não-trava logo abaixo guarda o outro lado: número grande sem marcador de
    # moeda continua não acionando a família econômica.
    from forja_lastro import material_economico as _mat
    for variante in ("R$ 524.141.077,62", "R $ 524.141.077,62", "R $524.141.077,62"):
        caso(f"marcador de moeda reconhece {variante[:6]!r}",
             _mat(f"A proposta resulta em {variante} no cenário central."))
    caso("não-trava do marcador: número grande sem moeda não é material econômico",
         not _mat("O processo 1234567-89.2020.4.01.3400 tramita desde 2020."))

    # Não-trava do L11: limiar normativo não é valor do caso. Amostrado no
    # acervo em 04/08/2026 e classificado à mão como falso positivo.
    normativo = ("O Decreto 10.201/2020 fixa as alçadas: acordo igual ou superior a "
                 "R$ 50 milhões exige autorização prévia da autoridade competente.")
    caso("não-trava L11 limiar normativo de alçada",
         not any(a["gate"] == "L11-valor-orfao"
                 for a in validar_gates_economicos(normativo, ledger={}, base_dir=tmp)))

    # L11 nasce em P1 por medição de falso positivo (§ 5 do plano 41). Este caso
    # existe para que a promoção a P0 seja uma DECISÃO, com nova medição, e não
    # um efeito colateral silencioso de outra mudança.
    orfao_txt = "A proposta do escritório resulta em R$ 88.412.900,15 para o cenário central."
    ach_orfao = [a for a in validar_gates_economicos(orfao_txt, ledger={}, base_dir=tmp)
                 if a["gate"] == "L11-valor-orfao"]
    caso("L11 permanece P1 enquanto a separação citado x calculado não for confiável",
         bool(ach_orfao) and all(a["sev"] == "P1" for a in ach_orfao),
         str(ach_orfao))
    ledger_tol, fonte_tol = _fonte_ledger(tmp, nome="parecer_tol_2026-07.md", anchors=[_ancora("R$ 110.000,40")],
                                  derivedCalculations=[{"id": "faixa", "label": "faixa derivada", "baseValue": "R$ 100.000,00",
                                                        "percentage": 10, "expectedValue": "R$ 110.000,40", "tolerance": 1.0}])
    texto_tol = "Plano econômico. Data-base: 2026-07. Faixa derivada: R$ 110.000,40."
    caso("não-trava L13 valor arredondado dentro da tolerância", not any(a["gate"] == "L13-aritmetica-derivada" for a in validar_gates_economicos(texto_tol, ledger=ledger_tol, base_dir=fonte_tol.parent)))
    r1 = validar_gates_economicos(texto_t10, ledger=ledger_t10, base_dir=fonte_t10.parent)
    r2 = validar_gates_economicos(texto_t10, ledger=ledger_t10, base_dir=fonte_t10.parent)
    caso("T12 reexecução L9-L13 é determinística", r1 == r2, f"{r1} != {r2}")
    return casos, falhas


if __name__ == "__main__":
    import tempfile
    from pathlib import Path

    print(f"Regressão de lastro — âncora: caso CASO-23, 26/07/2026")
    n1, f1 = _rodar_lexicais()
    with tempfile.TemporaryDirectory() as d:
        n2, f2 = _rodar_lastro(Path(d))
    n3, f3 = _rodar_acoplamento()
    with tempfile.TemporaryDirectory() as d:
        n4, f4 = _rodar_v2(Path(d))

    total, falhas = n1 + n2 + n3 + n4, f1 + f2 + f3 + f4
    if falhas:
        print(f"REGRESSÃO: {falhas} de {total} casos falharam")
        sys.exit(1)
    print(f"ok: {len(DEVE_PEGAR)} detecções + {len(NAO_PODE_TRAVAR)} não-travas lexicais "
          f"+ {n2} de ledger + {n3} de acoplamento + {n4} cenários do Plano 41 "
          f"conferem ({total} no total)")
    sys.exit(0)
