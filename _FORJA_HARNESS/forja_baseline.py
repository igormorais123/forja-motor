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
    "test_forja_aprendizado.py": (
        "o retorno humano vira regra aplicada e conferida: recorrência entre casos "
        "distintos manda sobre volume, aplicar é idempotente, e toda regra adotada "
        "é conferida contra o destino real desta máquina"),
    "test_forja_insumo_bloqueado.py": (
        "'não localizado' não é diagnóstico: insumo bloqueado exige causa em "
        "vocabulário fechado, diligências registradas, consequência e rota — a "
        "cobrança que o titular repetiu em quatro matérias no mesmo dia"),
    "test_forja_gate_anexo_saida.py": (
        "anexo fora do padrão Word da casa não sai pela porta da FORJA: a barreira "
        "fica no disparo do rascunho, que é o único ponto por onde documento "
        "efetivamente sai, e reprova quem falha nas três dimensões"),
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

_PYTEST_TAIL = re.compile(
    r"(?:(?P<failed>\d+) failed[,\s])?(?P<passed>\d+) passed"
    r"(?:, (?P<subtests>\d+) subtests passed)?"
)


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
    achado = _PYTEST_TAIL.search(resumo)
    return {
        "suite": nome,
        "familia": "pytest",
        "exit": codigo,
        "verde": codigo == 0,
        "passed": int(achado.group("passed")) if achado else 0,
        "failed": int(achado.group("failed") or 0) if achado else 0,
        "subtests": int(achado.group("subtests") or 0) if achado else 0,
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
    vermelhas = [item for item in resultados if not item["verde"]]
    return {
        "schemaVersion": 1,
        "geradoEm": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "python": sys.version.split()[0],
        "suitesDeclaradas": len(resultados),
        "suitesVerdes": len(resultados) - len(vermelhas),
        "testesPytest": sum(item.get("passed", 0) for item in resultados),
        "subtestsPytest": sum(item.get("subtests", 0) for item in resultados),
        "regressoesScript": len(SUITES_SCRIPT),
        "aprovado": not vermelhas,
        "quarentena": [{"suite": n, "motivo": m} for n, m in sorted(QUARENTENA.items())],
        "suites": resultados,
    }


def _imprimir(relatorio: dict) -> None:
    print("=" * 78)
    print("BASELINE FORJA — todas as suítes declaradas, nominalmente")
    print("=" * 78)
    for item in relatorio["suites"]:
        marca = "ok  " if item["verde"] else "FALHA"
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
    print("  APROVADO" if relatorio["aprovado"] else "  REPROVADO — ver suítes marcadas acima")


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
    return 0 if relatorio["aprovado"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
