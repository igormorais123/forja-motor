# -*- coding: utf-8 -*-
"""Confere se o workflow da FORJA descreve a FORJA que existe no disco.

Um script de workflow tem o mesmo problema de uma skill, com uma agravante: ele
não é lido por ninguém antes de rodar. O agente recebe o prompt já montado e
executa o comando que estiver ali. Se a ordem das fases divergir dos contratos,
ou se um script tiver sido renomeado, o erro só aparece com um caso real em
cima da mesa.

E há uma limitação que o formato impõe: **script de workflow não lê arquivo**.
A ordem das onze fases precisa estar literal dentro dele, o que cria uma segunda
cópia da verdade. Este teste é o que impede as duas de divergirem — ele compara
a lista literal com a cadeia `nextPhase` dos contratos, que é o que o runner de
fato obedece.

O que ele afere:

- a ordem das fases no workflow é exatamente a cadeia dos contratos;
- todo script citado existe no disco;
- toda flag passada a um script aparece no código dele;
- os subcomandos do runner citados são os que `forja_run.py` aceita;
- os títulos de `meta.phases` batem com as chamadas `phase()`.

O que ele **não** afere: se o texto dos prompts é bom. Isso continua sendo
leitura humana.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from forja_n3_common import PHASES
from forja_skill_doctor import _FLAG, _INVOCACAO, _SCRIPT

HARNESS = Path(__file__).resolve().parent
RAIZ = HARNESS.parent
WORKFLOW = RAIZ / ".claude" / "workflows" / "forja.js"


@pytest.fixture(scope="module")
def texto() -> str:
    if not WORKFLOW.exists():
        pytest.fail(f"workflow ausente: {WORKFLOW}")
    return WORKFLOW.read_text(encoding="utf-8")


def _cadeia_dos_contratos() -> list[str]:
    """A ordem que o runner obedece, reconstruída pelo `nextPhase` de cada contrato."""
    contratos = {}
    for arq in (HARNESS / "phase_contracts").glob("F*.json"):
        d = json.loads(arq.read_text(encoding="utf-8"))
        contratos[d["phase"]] = d.get("nextPhase")
    atual, ordem = PHASES[0], []
    while atual:
        ordem.append(atual)
        atual = contratos.get(atual)
        if atual in ordem:  # ciclo: devolve o que tem, o teste acusa
            break
    return ordem


def _lista_js(texto: str, nome: str) -> list[str]:
    bloco = re.search(rf"const {nome} = \[(.*?)\]", texto, re.S)
    assert bloco, f"não achei a lista {nome} no workflow"
    return re.findall(r"'([^']+)'", bloco.group(1))


class TestAOrdemNaoPodeDivergirDoContrato:
    """A cópia literal existe porque o formato exige; ela não pode virar segunda verdade."""

    def test_ordem_do_workflow_e_a_cadeia_dos_contratos(self, texto):
        assert _lista_js(texto, "ORDEM") == _cadeia_dos_contratos()

    def test_ordem_do_workflow_e_a_do_runner(self, texto):
        assert _lista_js(texto, "ORDEM") == list(PHASES)

    def test_toda_fase_citada_existe(self, texto):
        """Nome de artefato tem a mesma cara de nome de fase, e não é.

        `F2_QUESTION_TREE.json` é saída da F2, não uma fase — o que separa os dois
        aqui é a extensão. A consequência é que uma fase inventada escrita com
        `.json` passaria: o teste pega o erro de nomear fase, não o de nomear
        arquivo, e é bom que isso esteja dito.
        """
        citadas = set(re.findall(r"\bF\d+[A-Z_]*_[A-Z_]+\b(?!\.json)", texto))

        assert citadas <= set(PHASES), f"fases inventadas: {sorted(citadas - set(PHASES))}"


class TestOsComandosSaoOsQueExistem:
    def test_todo_script_citado_existe_no_disco(self, texto):
        faltando = [s for s in {Path(m.group(1)).name for m in _SCRIPT.finditer(texto)}
                    if not (HARNESS / s).exists()]

        assert not faltando, f"scripts citados e inexistentes: {faltando}"

    def test_toda_flag_existe_no_script_que_a_recebe(self, texto):
        problemas = []
        for m in _INVOCACAO.finditer(texto):
            script = HARNESS / Path(m.group(1)).name
            if not script.exists():
                continue
            fonte = script.read_text(encoding="utf-8", errors="replace")
            for flag in _FLAG.findall(m.group(2)):
                if flag not in fonte:
                    problemas.append(f"{script.name} {flag}")

        assert not problemas, f"flags que o script não conhece: {problemas}"

    def test_subcomandos_do_runner_sao_os_aceitos(self, texto):
        usados = set(re.findall(r"forja_run\.py \S+ (\w+)", texto))
        aceitos = set(re.findall(r'sub\.add_parser\("(\w+)"\)',
                                 (HARNESS / "forja_run.py").read_text(encoding="utf-8")))

        assert usados <= aceitos, f"subcomandos inventados: {sorted(usados - aceitos)}"

    def test_toda_fase_com_script_proprio_esta_na_ordem(self, texto):
        bloco = re.search(r"const SCRIPTS = \{(.*?)\n\}", texto, re.S)
        chaves = set(re.findall(r"^  (F\w+):", bloco.group(1), re.M))

        assert chaves <= set(PHASES)


class TestOAnuncioBateComOQueRoda:
    """`meta.phases` é o que o usuário vê no progresso; divergir dele é ruído."""

    def test_titulos_declarados_e_chamados_coincidem(self, texto):
        declarados = set(re.findall(r"\{ title: '([^']+)'", texto))
        chamados = set(re.findall(r"phase\('([^']+)'\)", texto))
        chamados |= set(re.findall(r"phase: '([^']+)'", texto))

        assert chamados == declarados

    def test_o_workflow_exige_o_caso_em_args(self, texto):
        assert "args" in texto and "throw new Error" in texto

    def test_a_conferencia_nao_depende_do_relato_do_executor(self, texto):
        """O invariante do arquivo: quem confere lê o disco, não o retorno de quem executou."""
        assert "promocaoConfirmada" in texto
        assert "conferencia.promocaoConfirmada !== true" in texto
