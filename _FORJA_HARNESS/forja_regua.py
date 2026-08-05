"""RÉGUA FORJA — validação canônica com teste real, telemetria e anti-fraude.

A régua é o veredito único de saúde da esteira. Ela existe para ser RESPEITADA:
nenhuma manutenção na FORJA é declarada concluída sem `python forja_regua.py` verde.

O que ela faz, nesta ordem:
  1. INTEGRIDADE — confere o sha256 de cada arquivo protegido (gates, extratores,
     composição OOXML/SVG, kits visuais, testes e a própria régua) contra REGUA_MANIFEST.json.
     Arquivo protegido alterado sem rebaseline = REPROVADO (exit 2). Isso impede a
     trapaça clássica de IA: "editar o teste até passar" sem ninguém perceber.
  2. SUÍTES — roda todas as suítes unitárias e de sabotagem (subprocessos reais,
     exit code é o que vale — nunca auto-declaração de sucesso).
  3. BATERIA REAL — test_real_telemetria_licao41.py: compatibilidade histórica e
     QA sobre artefatos reais de produção. A rota canônica atual é OOXML/SVG
     estática e a bateria usa `--sem-render`; `--rapida` pula só esta etapa.
  4. TELEMETRIA — grava telemetria/REGUA_<ts>.json com resultado por suíte, duração,
     hashes do manifesto e veredito. Evidência auditável, não narrativa.

Mudança legítima em arquivo protegido: revisar (humano ou review adversarial),
rodar `python forja_regua.py --rebaseline "motivo da mudança"` — o motivo e o par
hash antigo/novo ficam gravados no histórico do manifesto. Rebaseline sem motivo
substantivo é P0 de auditoria humana (ver 06_GATES_QUALIDADE_FORJA.md).

Limite declarado: a régua barra descuido e gaming casual de agente; um adversário
com acesso total ao disco pode rebaselinar — por isso o histórico é auditável e o
protocolo exige justificativa. Não há segurança absoluta local, há trilha.

Uso:
  python forja_regua.py                 # tudo (integridade + suítes + bateria real)
  python forja_regua.py --rapida        # sem a bateria real (sem Word COM)
  python forja_regua.py --rebaseline "motivo"   # aceita novos hashes com justificativa
"""

import hashlib
import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

# A régua precisa relatar achados e nomes em UTF-8 mesmo quando o host Windows
# expõe a saída como cp1252. Sem esta fronteira, uma suíte que falha ao imprimir
# um símbolo (por exemplo, ✓) derruba a própria régua antes do veredito.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

FORJA = Path(__file__).resolve().parent
FERRAMENTAS = FORJA.parent / "_FERRAMENTAS"
MANIFEST = FORJA / "REGUA_MANIFEST.json"
TELEDIR = FORJA / "telemetria"

# Arquivos cuja alteração muda a régua ou os gates — protegidos por hash.
PROTEGIDOS = [
    FORJA / "forja_regua.py",
    # Mede quantos gates a esteira computa e quantos o agente atesta a si
    # mesmo. Alterar este módulo muda o número que a casa usa para saber o
    # tamanho da própria superfície de autovalidação.
    FORJA / "forja_gate_liveness.py",
    FORJA / "forja_conselho.py",
    FORJA / "forja_citations.py",
    # O baseline define a fronteira entre pytest e regressões standalone;
    # deixá-lo fora do manifesto permitiria ocultar uma suíte por classificação.
    FORJA / "forja_baseline.py",
    FORJA / "forja_verificador.py",
    FORJA / "forja_estilo_humano.py",
    FORJA / "forja_run.py",
    FORJA / "forja_headless.py",
    FORJA / "forja_editorial.py",
    FORJA / "forja_fable5.py",  # shim de compatibilidade (M9)
    FORJA / "forja_editorial_fidelity.py",
    FORJA / "forja_package.py",
    FORJA / "forja_fidelity.py",
    FORJA / "forja_f8_contract.py",
    FORJA / "forja_visual_qa.py",
    FORJA / "forja_visual_review.py",
    FORJA / "forja_docx_layout.py",
    # Prova adversarial do layout: protege a evidência de que o gate continua
    # reprovando defeitos reais depois dos ajustes de calibração.
    FORJA / "test_forja_layout_antimoldagem.py",
    # Mesma prova para o gate de assinatura visual: sem ela, "a rota canônica
    # passa no F8-S" é indistinguível de um gate calibrado até aprová-la.
    FORJA / "forja_assinatura_visual.py",
    FORJA / "test_forja_assinatura_antimoldagem.py",
    # Mede se a rota que tem os gates é de fato percorrida. Nenhum outro
    # instrumento faz essa pergunta, e o defeito já apareceu três vezes.
    FORJA / "forja_adocao_rota.py",
    FORJA / "test_forja_adocao_rota.py",
    # Contraprova da porta única. O `medina_visual_kit.py`, onde a porta mora,
    # já está protegido mais abaixo nesta mesma lista desde antes de 05/08 —
    # conferi depois de quase acrescentá-lo em duplicata aqui, acreditando que
    # estava desprotegido só porque eu não o tinha visto.
    FORJA / "test_forja_porta_unica.py",
    # O baseline aprovado é evidência confiável apenas se o medidor, o teste e
    # o snapshot de hashes/vereditos permanecerem protegidos juntos.
    FORJA / "forja_baseline_aprovado.py",
    FORJA / "test_forja_baseline_aprovado.py",
    FORJA / "state" / "BASELINE_APROVADO.json",
    # O instrumento tipográfico é fonte de números de conformidade e sua
    # catraca decide se uma regressão entra na régua; ambos precisam ser
    # hash-bound, não apenas executados como suíte.
    FORJA / "forja_varredura_tipografica.py",
    FORJA / "test_forja_varredura_tipografica.py",
    # Os instrumentos que auditam o próprio alcance também são superfície de
    # confiança: se um canário ou o censo de formas puder mudar sem hash, a
    # régua passa a atestar a si mesma.
    FORJA / "forja_canario_mutacao.py",
    FORJA / "test_forja_canario_mutacao.py",
    FORJA / "forja_canario_catraca.py",
    FORJA / "test_forja_canario_catraca.py",
    FORJA / "forja_forma_artefatos.py",
    FORJA / "test_forja_forma_artefatos.py",
    FORJA / "forja_official_sources.py",
    FORJA / "forja_human_review.py",
    FORJA / "forja_n4_validate.py",
    FORJA / "forja_close_cycle.py",
    # A F10 só pode encerrar depois de recomputar identidade, hash e sincronização;
    # estes dois módulos formam a fronteira de decisão e ficam hash-bound.
    FORJA / "forja_f10_contract.py",
    FORJA / "forja_state_machine.py",
    FORJA / "forja_metricas_f7.py",
    FORJA / "forja_lastro.py",
    FORJA / "forja_memoria_auditabilidade.py",
    # Os calibradores produzem os números que vão ao cliente como evidência
    # (incidência monetária, taxa de falso positivo dos gates econômicos). Ficaram
    # fora do manifesto até 04/08/2026 — que é o `MC-16` da taxonomia: medição
    # que sustenta afirmação externa e pode ser alterada sem deixar rastro.
    FORJA / "forja_calibra_monetario.py",
    FORJA / "forja_calibra_gates_economicos.py",
    # Envio real ao cliente. Alterar quem envia, para quem ou com que texto é a
    # mudança de maior consequência externa do harness — tem de deixar rastro.
    FORJA / "forja_email.py",
    FORJA / "forja_render_docx.py",  # legado arquivado; não é rota da FORJA
    FORJA / "forja_visual_build.py",
    FORJA / "forja_svg_docx.py",
    FORJA / "forja_visual_qa_structural.py",
    FORJA / "forja_delivery.py",
    FORJA / "forja_injection_scan.py",
    FORJA / "forja_visual.py",
    FORJA / "forja_fila.py",
    FORJA / "test_forja_fila.py",
    FORJA / "test_licao41.py",
    FORJA / "test_forja_citacoes.py",
    FORJA / "test_forja_lastro.py",
    FORJA / "test_forja_gate_liveness.py",
    FORJA / "test_forja_lastro_rota_producao.py",
    FORJA / "test_forja_memoria_auditabilidade.py",
    FORJA / "test_forja_f8_static.py",
    # Âncora contra peças reais: protege tanto a calibração do template quanto
    # a permanência dos achados XML já triados na primeira execução da F8.
    FORJA / "test_forja_f8_pecas_reais.py",
    FORJA / "test_forja_verificador.py",
    FORJA / "test_forja_politica_citacoes.py",
    FORJA / "test_forja_identidade_citacoes.py",
    FORJA / "forja_replay.py",
    FORJA / "forja_adversarial_gate.py",
    FORJA / "forja_recomputo_censo.py",
    FORJA / "test_forja_adversarial_gate.py",
    FORJA / "test_forja_recomputo_censo.py",
    FORJA / "forja_p0.py",
    FORJA / "forja_regimento_gate.py",
    FORJA / "forja_produto.py",
    FORJA / "forja_entrega.py",
    FORJA / "test_forja_p0.py",
    FORJA / "test_forja_regimento_gate.py",
    FORJA / "test_forja_produto.py",
    FORJA / "test_forja_entrega.py",
    FORJA / "forja_artefatos.py",
    FORJA / "test_forja_artefatos.py",
    FORJA / "forja_ingestao.py",
    FORJA / "forja_contexto.py",
    FORJA / "forja_redacao.py",
    FORJA / "test_forja_ingestao.py",
    FORJA / "test_forja_contexto.py",
    FORJA / "test_forja_redacao.py",
    FORJA / "forja_paragrafos.py",
    FORJA / "forja_fontes_oficiais.py",
    FORJA / "forja_red_team.py",
    FORJA / "test_forja_injection_gate.py",
    FORJA / "test_forja_paragrafos.py",
    FORJA / "test_forja_fontes_oficiais.py",
    FORJA / "test_forja_red_team.py",
    FORJA / "test_forja_gates_emitidos.py",
    FORJA / "test_forja_estilo_humano.py",
    FORJA / "test_forja_editorial.py",
    FORJA / "test_forja_run.py",
    FORJA / "test_forja_n3_package.py",
    FORJA / "test_forja_n3_visual.py",
    FORJA / "test_forja_svg_docx.py",
    FORJA / "test_forja_anti_cheat.py",
    FORJA / "test_f7_campos.py",
    FORJA / "test_forja_injection.py",
    FORJA / "test_forja_regua.py",
    FORJA / "test_real_telemetria_licao41.py",
    FERRAMENTAS / "medina_visual_kit.py",
    FERRAMENTAS / "medina_svg_kit.py",
    FERRAMENTAS / "word_visual_pipeline.py",
    FERRAMENTAS / "montar_visual.py",
    FERRAMENTAS / "estilo_medina.py",
    FORJA / "phase_contracts" / "F6.json",
    FORJA / "phase_contracts" / "F7.json",
    FORJA / "phase_contracts" / "F8.json",
    FORJA / "phase_contracts" / "F9.json",
    FORJA / "phase_contracts_n4" / "F6.json",
    FORJA / "phase_contracts_n4" / "F7.json",
    FORJA / "phase_contracts_n4" / "F8.json",
    FORJA / "phase_contracts_n4" / "F9.json",
    FORJA / "n4_schemas" / "N4_LAYOUT_PROFILES.json",
    FORJA / "cache" / "fontes_oficiais" / "OFFICIAL_SOURCE_MANIFEST.json",
    FORJA / "FORJA_HUMAN_REVIEW_TRUST.example.json",
    FORJA / "FORJA_HUMAN_REVIEW_TRUST_PIN.json",
    FORJA / "PROTOCOLO_ESCRITA_HUMANA_FORJA.md",
    FORJA / "PROTOCOLO_EDITORIAL_ESCRITA_FINAL.md",
    FORJA / "forja_ar_corpus.py",
    FORJA / "forja_ar_indicadores.py",
    FORJA / "forja_ar_canarios.py",
    FORJA / "forja_ar_runpair.py",
    FORJA / "forja_ar_blind.py",
    FORJA / "forja_ar_ciclo.py",
    FORJA / "forja_ar_evolucao.py",
    FORJA / "test_forja_autoresearch.py",
    FORJA / "autoresearch" / "AR_MANIFEST.json",
    FORJA / "autoresearch" / "canarios" / "CANARIOS_MANIFEST.json",
    FORJA / "autoresearch" / "prompts" / "JUIZ_CEGO_PROMPT.md",
    FORJA / "autoresearch" / "prompts" / "GERACAO_VARIANTE_PROMPT.md",
    FORJA / "autoresearch" / "prompts" / "REDACAO_PAR_PROMPT.md",
]

# Suítes rápidas (sem Word COM; a materialização oficial é OOXML/SVG estático).
SUITES = [
    "test_forja_verificador.py",
    "test_forja_estilo_humano.py",
    "test_forja_editorial.py",
    "test_forja_run.py",
    "test_forja_n3_package.py",
    "test_forja_n3_visual.py",
    "test_forja_svg_docx.py",
    "test_forja_anti_cheat.py",
    "test_forja_citacoes.py",
    "test_forja_lastro.py",
    "test_forja_lastro_rota_producao.py",
    "test_forja_memoria_auditabilidade.py",
    "test_forja_f8_static.py",
    "test_forja_f8_gates_contrato.py",
    "test_f7_campos.py",
    "test_forja_injection.py",
    "test_licao41.py",
    "test_forja_conselho.py",
    "test_forja_politica_citacoes.py",
    "test_forja_identidade_citacoes.py",
    "test_forja_injection_gate.py",
    "test_forja_paragrafos.py",
    "test_forja_ingestao.py",
    "test_forja_artefatos.py",
    "test_forja_p0.py",
    "test_forja_regimento_gate.py",
    "test_forja_produto.py",
    "test_forja_entrega.py",
    "test_forja_adversarial_gate.py",
    "test_forja_recomputo_censo.py",
    "test_forja_canario_mutacao.py",
    "test_forja_canario_catraca.py",
    "test_forja_forma_artefatos.py",
    "test_forja_rota_forma.py",
    "test_forja_layout_papeis.py",
    "test_forja_layout_antimoldagem.py",
    "test_forja_assinatura_antimoldagem.py",
    "test_forja_adocao_rota.py",
    "test_forja_porta_unica.py",
    "test_forja_baseline_aprovado.py",
    "test_forja_varredura_tipografica.py",
    "test_forja_visual_build_peca_longa.py",
    "test_forja_f8_pecas_reais.py",
    "test_forja_contexto.py",
    "test_forja_redacao.py",
    "test_forja_fontes_oficiais.py",
    "test_forja_red_team.py",
    "test_forja_gates_emitidos.py",
    "test_forja_gate_liveness.py",
    "test_forja_regua.py",
    "test_forja_autoresearch.py",
]
BATERIA_REAL = ("test_real_telemetria_licao41.py", "--sem-render")


def sha256_arquivo(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _manifest_key(value):
    """Chave estável entre Windows e Linux; separador não muda identidade."""
    return str(value).replace("\\", "/")


def hashes_atuais():
    return {p.relative_to(FORJA.parent).as_posix(): (sha256_arquivo(p) if p.exists() else "AUSENTE")
            for p in PROTEGIDOS}


def verificar_integridade(manifest=None):
    """Compara hashes atuais com o manifesto. Retorna (ok, divergentes)."""
    manifest = manifest if manifest is not None else json.loads(
        MANIFEST.read_text(encoding="utf-8")) if MANIFEST.exists() else None
    if not manifest:
        return False, ["REGUA_MANIFEST.json inexistente — rode --rebaseline \"baseline inicial\""]
    esperados = {}
    colisoes = []
    for nome, esperado in (manifest.get("hashes", {}) or {}).items():
        chave = _manifest_key(nome)
        if chave in esperados and esperados[chave] != esperado:
            colisoes.append(f"chave canônica duplicada com hashes distintos: {chave}")
        esperados[chave] = esperado
    if colisoes:
        return False, colisoes
    atuais = hashes_atuais()
    divergentes = []
    for nome, esperado in esperados.items():
        atual = atuais.get(nome, "AUSENTE")
        if atual != esperado:
            divergentes.append(nome)
    novos = [n for n in atuais if n not in esperados]
    divergentes.extend(f"{n} (novo, fora do manifesto)" for n in novos)
    return not divergentes, divergentes


def rebaseline(motivo):
    if not motivo or len(motivo.strip()) < 15:
        raise SystemExit("rebaseline exige motivo substantivo (>= 15 caracteres) — a justificativa fica no histórico auditável")
    antigo = json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.exists() else {"hashes": {}, "historico": []}
    hashes_antigos = {_manifest_key(nome): valor for nome, valor in (antigo.get("hashes") or {}).items()}
    atuais = hashes_atuais()
    mudados = sorted(set(list(hashes_antigos.keys()) + list(atuais.keys())))
    mudados = [n for n in mudados if hashes_antigos.get(n) != atuais.get(n)]
    novo = {
        "atualizadoEm": datetime.now().astimezone().isoformat(timespec="seconds"),
        "hashes": atuais,
        "historico": (antigo.get("historico") or []) + [{
            "em": datetime.now().astimezone().isoformat(timespec="seconds"),
            "motivo": motivo.strip(),
            "arquivosMudados": mudados,
        }],
    }
    MANIFEST.write_text(
        json.dumps(novo, ensure_ascii=False, indent=2),
        encoding="utf-8",
        newline="\n",
    )
    print(f"Manifesto rebaselinado: {len(mudados)} arquivo(s) atualizado(s). Motivo registrado no histórico.")
    for m in mudados:
        print("  ~", m)
    return novo


def rodar_suite(nome, timeout=1200):
    t0 = time.perf_counter()
    comando_nome = " ".join(nome) if isinstance(nome, (tuple, list)) else str(nome)
    script = nome[0] if isinstance(nome, (tuple, list)) else nome
    extras = list(nome[1:]) if isinstance(nome, (tuple, list)) else []
    try:
        r = subprocess.run(
            [sys.executable, str(FORJA / script), *extras],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            cwd=str(FORJA),
        )
        exit_code, saida = r.returncode, (r.stdout or "") + (r.stderr or "")
    except subprocess.TimeoutExpired:
        exit_code, saida = 124, f"TIMEOUT após {timeout}s"
    dur = round(time.perf_counter() - t0, 1)
    return {"suite": comando_nome, "exitCode": exit_code, "ok": exit_code == 0,
            "duracaoS": dur, "tail": saida.strip()[-600:]}


def main():
    args = sys.argv[1:]
    if "--rebaseline" in args:
        i = args.index("--rebaseline")
        motivo = args[i + 1] if len(args) > i + 1 else ""
        rebaseline(motivo)
        return 0

    rapida = "--rapida" in args
    TELEDIR.mkdir(exist_ok=True)
    inicio = time.perf_counter()
    tele = {"executadoEm": datetime.now().astimezone().isoformat(timespec="seconds"),
            "modo": "rapida (sem bateria real)" if rapida else "completa",
            "python": sys.version.split()[0]}

    print("=" * 72)
    print("RÉGUA FORJA — 1/3 integridade dos arquivos protegidos")
    print("=" * 72)
    integra_ok, divergentes = verificar_integridade()
    tele["integridade"] = {"ok": integra_ok, "divergentes": divergentes}
    if not integra_ok:
        for d in divergentes:
            print("  ALTERADO:", d)
        tele["veredito"] = "REGUA ADULTERADA — arquivo protegido mudou sem rebaseline"
        saida = TELEDIR / f"REGUA_{datetime.now():%Y-%m-%d_%H%M%S}.json"
        saida.write_text(json.dumps(tele, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\nREPROVADO (integridade). Se a mudança é legítima e revisada: "
              f"python forja_regua.py --rebaseline \"motivo\"\nTelemetria: {saida}")
        return 2
    print(f"  OK: {len(PROTEGIDOS)} arquivos batem com o manifesto de "
          f"{json.loads(MANIFEST.read_text(encoding='utf-8'))['atualizadoEm']}")

    print()
    print("=" * 72)
    print("RÉGUA FORJA — 2/3 suítes (exit code real, sem auto-declaração)")
    print("=" * 72)
    resultados = []
    for s in SUITES:
        r = rodar_suite(s)
        resultados.append(r)
        print(f"  [{'OK    ' if r['ok'] else 'FALHOU'}] {s} ({r['duracaoS']}s)")
        if not r["ok"]:
            print("    " + r["tail"].replace("\n", "\n    ")[-400:])

    if not rapida:
        print()
        print("=" * 72)
        print("RÉGUA FORJA — 3/3 bateria REAL com telemetria (pipeline verdadeira)")
        print("=" * 72)
        r = rodar_suite(BATERIA_REAL, timeout=1800)
        resultados.append(r)
        print(f"  [{'OK    ' if r['ok'] else 'FALHOU'}] {BATERIA_REAL} ({r['duracaoS']}s)")
        if not r["ok"]:
            print("    " + r["tail"].replace("\n", "\n    ")[-400:])

    tele["suites"] = resultados
    aprovado = all(r["ok"] for r in resultados)
    tele["veredito"] = "APROVADO" if aprovado else "REPROVADO"
    tele["duracaoTotalS"] = round(time.perf_counter() - inicio, 1)
    saida = TELEDIR / f"REGUA_{datetime.now():%Y-%m-%d_%H%M%S}.json"
    saida.write_text(json.dumps(tele, ensure_ascii=False, indent=2), encoding="utf-8")

    print()
    print("=" * 72)
    print(f"RÉGUA: {tele['veredito']} em {tele['duracaoTotalS']}s | telemetria: {saida.name}")
    print("=" * 72)
    return 0 if aprovado else 1


if __name__ == "__main__":
    raise SystemExit(main())
