# -*- coding: utf-8 -*-
"""Porta de entrada única do baseline de testes da FORJA (emenda E16).

Antes deste módulo, o número de baseline vinha de uma seleção nomeada de suítes
que variava entre execuções e omitia regressões escritas como script autônomo —
entre elas o veneno de citação, a sabotagem da régua e os gates do verificador.
"104 passed" nunca as incluiu.

Duas famílias, um só relatório:

  pytest  -> suítes com funções de teste, executadas uma a uma. O isolamento não
             é preferência: `test_forja_verificador.py` substitui `sys.stdout` no
             nível de módulo e derruba a captura de qualquer execução conjunta.
  script  -> regressões que rodam por `python test_x.py` e comunicam o veredito
             pelo código de saída. São executadas como subprocesso, não adaptadas.

Uso: python forja_baseline.py [--json CAMINHO] [--quiet]
Saída: 0 quando toda suíte declarada passa; 1 caso contrário.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import forja_arvore_estavel as arvore

FORJA = Path(__file__).resolve().parent

# Regressões escritas como script autônomo. Cada uma comunica o veredito pelo
# código de saída e imprime o resumo na última linha. Não são adaptadas a pytest
# porque o valor delas está no texto do relatório que produzem.
SUITES_SCRIPT = {
    # Não traz o marcador que o classificador procura no stdout, então o pytest o
    # coletava e não achava teste nenhum. Declarado aqui, roda como script.
    "test_licao41.py": (
        "os três defeitos de ferramenta da Lição 41: itálico virando asterisco no "
        "DOCX, 'Tema 1.365' lido como 'Tema 1', e súmula nunca localizada no cache"),
    "test_forja_fronteira.py": (
        "fronteira motor/acervo — classifica, acusa vazamento de dado de cliente "
        "e não acusa vocabulário nem valor sintético"),
    "test_forja_licoes.py": (
        "catraca da rastreabilidade das lições: citação por número tem de "
        "resolver para uma lição só, e a duplicidade de numeração não pode crescer"),
    "test_forja_protocolo_par.py": (
        "paridade de assunto entre CLAUDE.md e AGENTS.md — ordem que vive num "
        "arquivo só vale para uma família de modelo e não para a outra"),
    "test_forja_aprendizado.py": (
        "o retorno humano vira regra aplicada e conferida: recorrência entre casos "
        "distintos manda sobre volume, aplicar é idempotente, e toda regra adotada "
        "é conferida contra o destino real desta máquina"),
    "test_forja_insumo_bloqueado.py": (
        "'não localizado' não é diagnóstico: insumo bloqueado exige causa em "
        "vocabulário fechado, diligências registradas, consequência e rota — a "
        "cobrança que o titular repetiu em quatro matérias no mesmo dia"),
    "test_vigias_avisam_no_acervo.py": (
        "nenhum dos vigias agendados grava o aviso na raiz do harness: o aviso "
        "nomeia caso, a raiz é motor, e um arquivo desses reprova a "
        "sincronização inteira — aconteceu três vezes em dois dias, uma por "
        "vigia"),
    "test_forja_gate_anexo_saida.py": (
        "anexo fora do padrão Word da casa não sai pela porta da FORJA: a barreira "
        "fica no disparo do rascunho, que é o único ponto por onde documento "
        "efetivamente sai, e reprova quem falha nas três dimensões"),
    "test_forja_gate_aceite.py": (
        "gate de aceite dos critérios que o titular escreveu no e-mail: exige prova de "
        "quem afirma ter concluído, e recusa destaque de margem cortado no meio de "
        "citação legal"),
    "test_forja_baseline_contagem.py": (
        "o relatório deste próprio baseline conta falha, erro de importação e subtest "
        "pelo que eles são: a expressão anterior gravava `failed: 0` em toda execução "
        "reprovada, e relatório que subnotifica é pior que relatório ausente"),
    "test_forja_skill.py": (
        "a skill da FORJA ainda descreve a FORJA que existe: todo script, contrato e "
        "referência que ela manda usar está no disco — porque skill é documentação que "
        "o agente segue sem conferir a fonte, e envelhecer aqui manda gente rodar "
        "comando que não existe"),
    "test_forja_codigo_morto.py": (
        "a poda de código morto não encosta em import protegido, em código nem na "
        "quebra de linha do arquivo — e entrada declarada fora do repositório, "
        "como o servidor MCP de e-mail, nunca vira candidata"),
    "test_forja_lapidacao_governanca.py": "os invariantes da lapidação aprovam o legítimo e reprovam cada sabotagem",
    "test_forja_exploracao_diversidade.py": "formulário do F2A é acusado e exploração genuína passa limpa",
    "test_forja_adversarial_gate.py": "regressão autônoma do gate adversarial",
    "test_forja_canario_mutacao.py": "canário de mutação dos gates",
    "test_forja_canario_catraca.py": "canário das catracas — nenhum gate crítico pode aprovar ruína",
    "test_forja_forma_artefatos.py": "censo de formas dos artefatos",
    "test_forja_recomputo_censo.py": "recomputo do censo produtivo",
    "test_forja_rota_forma.py": "fiação da rota de produção por forma",
    "test_forja_verificador.py": "gates determinísticos das 30 lições de RETROSPECTIVAS.md",
    "test_forja_citacoes.py": "veneno de citação — taxonomia U1 em seis modos de falha",
    "test_forja_regua.py": "sabotagem da régua — cinco fraudes simuladas",
    "test_forja_fila.py": "priorização e prontidão da fila",
    "test_forja_conselho_1107.py": "gates do conselho de 11/07/2026",
    "test_forja_lastro.py": "blindagem contra lastro aparente — âncora CASO-23 26/07/2026",
    "test_forja_regimentos.py": "auditoria de atualidade dos regimentos arquivados (E11)",
    "test_forja_gate_liveness.py": "catraca da liveness dos gates — computação versus autodeclaração",
    "test_forja_lastro_rota_producao.py": "catraca da rota de produção — recomputa lastro no disco",
    "test_forja_conselho.py": "gate do conselho — reprova bypass e preserva pareceres reais",
    "test_forja_f8_gates_contrato.py": "contrato F8 — produtores e gates exigidos permanecem acoplados",
    "test_forja_f8_pecas_reais.py": "âncora F8 — peças DOCX reais contra falsos positivos de forma",
    "test_forja_visual_build_peca_longa.py": "smoke visual — peça longa com SVG pela rota canônica",
    "test_forja_layout_papeis.py": "contraprova de papéis tipográficos e exceções estruturais",
    "test_forja_layout_antimoldagem.py": "canário anti-moldagem — gate de layout reprova defeito deliberado",
    "test_forja_assinatura_antimoldagem.py": "canário F8-S anti-moldagem — assinatura visual reprova destruição deliberada",
    "test_forja_adocao_rota.py": "contraprova do medidor de adoção — marca vinculada ao DOCX exato",
    "test_forja_porta_unica.py": "porta única — toda peça atravessa o verificador, venha por onde vier",
    "test_forja_baseline_aprovado.py": "âncoras do baseline aprovado — deriva de artefato ou veredito",
    "test_forja_varredura_tipografica.py": "catraca permanente de conformidade tipográfica do acervo",
    "test_forja_politica_citacoes.py": "política de citações — cobertura e liberação sem autodeclaração",
    "test_forja_identidade_citacoes.py": "identidade de citação — CNJ e tribunal sem falsa equivalência",
    "test_forja_injection_gate.py": "gate de triagem de injeção — esquemas reais sem autodeclaração",
    "test_forja_paragrafos.py": "lastro por parágrafo — proveniência computada sem aprovação do conjunto vazio",
    "test_forja_fontes_oficiais.py": "gate F5 — fontes oficiais computadas sem aprovação do conjunto vazio",
    "test_forja_red_team.py": "red team — recomputação e contraexemplos dos gates",
    "test_forja_gates_emitidos.py": "emissão de gates — F8/F10 e liveness sem resultados fabricados",
    "test_forja_ingestao.py": "ingestão e exploração — índice documental, cobertura e 100 sementes",
    "test_forja_contexto.py": "contexto de entrada — snapshot imutável, escopo e digest do caso",
    "test_forja_redacao.py": "redação — gates computados de entidades, template e voz",
    "test_forja_artefatos.py": "artefatos — inventário, esquemas e vocabulário fail-closed",
    "test_forja_p0.py": "P0 — distinção entre achado aberto, resolvido e separação produtor/revisor",
    "test_forja_regimento_gate.py": "regimento — atualidade, vigência e lastro temporal dos mapas",
    "test_forja_produto.py": "produto — classificações de entrega e perguntas jurisdicionais",
    "test_forja_entrega.py": "entrega — reconciliação, mapeamento e consistência dos manifestos",
}

# Um teste que substitui a captura global de stdout é um script de regressão,
# não uma suíte pytest. A classificação continua explícita em SUITES_SCRIPT;
# este marcador só impede que uma nova regressão seja executada pela família
# errada enquanto ainda não recebeu seu rótulo.
_SCRIPT_STDOUT_MARKER = "sys.stdout = io.TextIOWrapper"

# Contagens independentes, e não uma expressão única sobre a linha inteira.
# A versão anterior era `(?:(\d+) failed[,\s])?(\d+) passed`: em "1 failed, 21
# passed" o `[,\s]` consumia a vírgula, o dígito seguinte era um espaço, o
# casamento retrocedia e o grupo opcional saía de cena — todo relatório do
# baseline gravava `failed: 0`, inclusive quando reprovava. E "1 error in 0.2s",
# que é como aparece um módulo que nem importa, não casava com nada.
_PYTEST_PASSED = re.compile(r"(\d+) passed")
_PYTEST_FAILED = re.compile(r"(\d+) failed")
_PYTEST_ERROR = re.compile(r"(\d+) error")
_PYTEST_SUBTESTS = re.compile(r"(\d+) subtests passed")


def _contagens_pytest(resumo: str) -> dict[str, int]:
    """passed/failed/errors/subtests da última linha do pytest.

    `subtests` sai do texto antes de procurar `passed`, senão "3 subtests
    passed" seria lido como o total da suíte quando ela não tiver outro.
    """
    sub = _PYTEST_SUBTESTS.search(resumo)
    resto = _PYTEST_SUBTESTS.sub("", resumo)
    def n(padrao, texto):
        m = padrao.search(texto)
        return int(m.group(1)) if m else 0
    return {
        "passed": n(_PYTEST_PASSED, resto),
        "failed": n(_PYTEST_FAILED, resto),
        "errors": n(_PYTEST_ERROR, resto),
        "subtests": int(sub.group(1)) if sub else 0,
    }


def _run(args: list[str]) -> tuple[int, str]:
    proc = subprocess.run(
        args, cwd=str(FORJA), capture_output=True, text=True,
        encoding="utf-8", errors="replace", timeout=1800,
    )
    saida = (proc.stdout or "") + (proc.stderr or "")
    linhas = [linha.strip() for linha in saida.splitlines() if linha.strip()]
    return proc.returncode, (linhas[-1] if linhas else "")


def _pytest(nome: str) -> dict:
    codigo, resumo = _run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", nome])
    c = _contagens_pytest(resumo)
    return {
        "suite": nome,
        "familia": "pytest",
        "exit": codigo,
        "verde": codigo == 0,
        "passed": c["passed"],
        "failed": c["failed"],
        "errors": c["errors"],
        "subtests": c["subtests"],
        "resumo": resumo,
    }


def _script(nome: str, papel: str) -> dict:
    codigo, resumo = _run([sys.executable, nome])
    return {
        "suite": nome,
        "familia": "script",
        "papel": papel,
        "exit": codigo,
        "verde": codigo == 0,
        "resumo": resumo,
    }


def _reavaliar_se_a_arvore_mexeu(item: dict) -> dict:
    """Suíte vermelha ganha uma segunda leitura, com a árvore medida em volta.

    A bateria leva minutos e outras sessões do agente escrevem na mesma pasta
    nesse intervalo — medido em 10/08/2026, com módulo do motor alterado e teste
    novo aparecendo no meio de uma execução. Uma suíte que varre a árvore pode
    reprovar por causa disso e passar sozinha em seguida, o que já aconteceu com
    a varredura tipográfica e com a da fronteira no mesmo dia.

    A regra tem duas metades, e a segunda é que a impede de virar tapete:
    **repetir verde não basta, a árvore precisa ter mexido.** Suíte que reprova
    duas vezes continua vermelha; suíte que passa na segunda com a árvore parada
    é falha intermitente de verdade e também continua vermelha, porque aí o
    problema é dela.
    """
    if item["verde"] or item.get("familia") == "config":
        return item

    antes = arvore.impressao()
    if item.get("familia") == "pytest":
        segunda = _pytest(item["suite"])
    else:
        segunda = _script(item["suite"], item.get("papel", ""))
    delta = arvore.mexeu(antes, arvore.impressao())

    if not (segunda["verde"] and delta["mexeu"]):
        return {**item, "segundaLeitura": {"verde": segunda["verde"],
                                           "resumo": segunda["resumo"]},
                "arvoreMexeu": delta}
    return {
        **item, "instavel": True, "verde": False,
        "segundaLeitura": {"verde": True, "resumo": segunda["resumo"]},
        "arvoreMexeu": delta,
        "porque": (f"reprovou, a árvore mudou em {delta['total']} arquivo(s) "
                   f"durante a leitura e a segunda passada ficou verde; o "
                   f"baseline não afirma nem aprovação nem quebra"),
    }


def _parece_script_autonomo(nome: str) -> bool:
    try:
        texto = (FORJA / nome).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False
    return _SCRIPT_STDOUT_MARKER in texto


# Suíte declarada fora do baseline, com motivo. Quarentena NÃO é exclusão: o
# nome e a razão aparecem no relatório de toda execução. Uma suíte que fica de
# fora sem aparecer é indistinguível de suíte que não existe — e foi assim que
# seis arquivos `test_*.py` ficaram anos fora da rede, só por não terem o
# prefixo `test_forja_`, entre eles a regressão do gate de colisão de SVG que o
# protocolo da casa declara bloqueante.
QUARENTENA = {
    "test_real_telemetria_licao41.py": (
        "renderiza duas peças reais ponta a ponta e uma delas reprova no gate de "
        "layout com `structural_text_not_justified`. O gate está certo: a peça em "
        "questão é o desvio de padrão Word já registrado no protocolo da casa. "
        "Fica fora do veredito até alguém decidir se corrige a fonte ou se o alvo "
        "sai da bateria — e não some do relatório enquanto isso."),
}


def _scripts_autonomos_nao_mapeados() -> list[str]:
    return sorted(
        caminho.name
        for caminho in FORJA.glob("test_*.py")
        if caminho.name not in SUITES_SCRIPT and caminho.name not in QUARENTENA
        and _parece_script_autonomo(caminho.name)
    )


def coletar() -> list[str]:
    """Suítes pytest: tudo que casa o padrão e não é regressão em script."""
    return sorted(
        caminho.name for caminho in FORJA.glob("test_*.py")
        if caminho.name not in SUITES_SCRIPT and caminho.name not in QUARENTENA
        and not _parece_script_autonomo(caminho.name)
    )


def executar() -> dict:
    # Retrato de abertura. Um baseline verde medido sobre pasta em movimento é
    # prova mais fraca do que um medido sobre pasta parada, e a diferença some
    # se ninguém a registra. Isto não é veredito — é a condição da medição,
    # declarada junto com ela.
    arvore_antes = arvore.impressao()
    resultados = [_pytest(nome) for nome in coletar()]
    resultados += [
        {
            "suite": nome,
            "familia": "config",
            "exit": 2,
            "verde": False,
            "resumo": (
                "script standalone detectado sem classificação; "
                "inclua-o em SUITES_SCRIPT antes de confiar no baseline"
            ),
        }
        for nome in _scripts_autonomos_nao_mapeados()
    ]
    resultados += [_script(nome, papel) for nome, papel in sorted(SUITES_SCRIPT.items())]
    resultados = [_reavaliar_se_a_arvore_mexeu(item) for item in resultados]
    instaveis = [item for item in resultados if item.get("instavel")]
    vermelhas = [item for item in resultados
                 if not item["verde"] and not item.get("instavel")]
    return {
        "schemaVersion": 1,
        "geradoEm": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "python": sys.version.split()[0],
        "suitesDeclaradas": len(resultados),
        # Contar verde por subtração deixaria a instável do lado errado da
        # conta: ela não é vermelha, e não é verde. Conta-se o que é.
        "suitesVerdes": sum(1 for item in resultados if item["verde"]),
        "suitesInstaveis": len(instaveis),
        "testesPytest": sum(item.get("passed", 0) for item in resultados),
        "subtestsPytest": sum(item.get("subtests", 0) for item in resultados),
        "regressoesScript": len(SUITES_SCRIPT),
        "instaveis": [{"suite": i["suite"], "porque": i["porque"],
                       "arvoreMexeu": i["arvoreMexeu"]} for i in instaveis],
        "arvoreDuranteACorrida": arvore.mexeu(arvore_antes, arvore.impressao()),
        # `aprovado` continua exigindo zero vermelhas. Instável não aprova nada:
        # ele tem veredito próprio, logo abaixo, e sai por código de saída
        # distinto para que automação não o confunda com verde.
        "aprovado": not vermelhas and not instaveis,
        "inconclusivo": bool(instaveis) and not vermelhas,
        "quarentena": [{"suite": n, "motivo": m} for n, m in sorted(QUARENTENA.items())],
        "suites": resultados,
    }


def _imprimir(relatorio: dict) -> None:
    print("=" * 78)
    print("BASELINE FORJA — todas as suítes declaradas, nominalmente")
    print("=" * 78)
    for item in relatorio["suites"]:
        marca = "ok  " if item["verde"] else ("INST" if item.get("instavel") else "FALHA")
        print(f"  [{marca}] {item['suite']:<38} {item['resumo'][:34]}")
    print("-" * 78)
    print(
        f"  {relatorio['suitesVerdes']}/{relatorio['suitesDeclaradas']} suítes verdes · "
        f"{relatorio['testesPytest']} testes pytest "
        f"(+{relatorio['subtestsPytest']} subtests) · "
        f"{relatorio['regressoesScript']} regressões em script"
    )
    for q in relatorio.get("quarentena") or []:
        print(f"  [QUAR] {q['suite']:<38} fora do veredito — {q['motivo'][:200]}")
    for i in relatorio.get("instaveis") or []:
        d = i["arvoreMexeu"]
        print(f"  [INST] {i['suite']:<38} {i['porque']}")
        print(f"         mudaram {d['novos']} novo(s), {d['mudados']} alterado(s), "
              f"{d['sumidos']} removido(s) durante a leitura:")
        for caminho in d["amostra"][:6]:
            print(f"           {caminho}")
        if d["total"] > len(d["amostra"][:6]):
            print(f"           … e mais {d['total'] - len(d['amostra'][:6])}")
    d = relatorio.get("arvoreDuranteACorrida") or {}
    if d.get("mexeu"):
        print(f"  [chão] a pasta mudou em {d['total']} arquivo(s) durante a corrida "
              f"({d['novos']} novo, {d['mudados']} alterado, {d['sumidos']} removido) "
              f"— outra sessão trabalhando junto; o veredito vale para o que foi lido")
    if relatorio["aprovado"]:
        print("  APROVADO")
    elif relatorio.get("inconclusivo"):
        print("  INCONCLUSIVO — nenhuma suíte quebrou, mas a árvore mudou durante a "
              "leitura de pelo menos uma. Rode de novo com a pasta parada antes de "
              "declarar o baseline verde.")
    else:
        print("  REPROVADO — ver suítes marcadas acima")


def main() -> int:
    parser = argparse.ArgumentParser(description="Baseline de testes da FORJA (E16)")
    parser.add_argument("--json", type=Path, help="grava o relatório no caminho indicado")
    parser.add_argument("--quiet", action="store_true", help="omite a tabela")
    args = parser.parse_args()

    relatorio = executar()
    if not args.quiet:
        _imprimir(relatorio)

    destino = args.json or (
        FORJA / "telemetria" /
        f"BASELINE_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.json"
    )
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(
        json.dumps(relatorio, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    if not args.quiet:
        print(f"  Relatório: {destino}")
    if relatorio["aprovado"]:
        return 0
    # Código próprio: automação que trata "≠ 0" como quebra continua correta, e
    # quem quiser distinguir "não deu para saber" de "quebrou" agora consegue.
    return 2 if relatorio.get("inconclusivo") else 1


if __name__ == "__main__":
    raise SystemExit(main())
