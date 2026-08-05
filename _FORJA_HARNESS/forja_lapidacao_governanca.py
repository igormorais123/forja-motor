# -*- coding: utf-8 -*-
"""forja_lapidacao_governanca.py — a governança da lapidação vira código conferível.

Ordem do Igor em 05/08/2026: "coloque /efesto e /helena para cuidar do processo e
decidir dúvidas e questões bem como limites de iterações ou desperdício de token ou
algo que piore ou tire dos trilhos o sistema. tudo deve ser registrado e documentado
no sistema mapeado recursos e funcionalidades".

Helena fixou o envelope em `GOVERNANCA_LAPIDACAO_2026-08-05.md`. Este módulo é a
camada do Efesto: os limites e os critérios de parada deixam de ser parágrafo e
passam a ser função que confere o estado vivo e devolve REPROVADO quando o sistema
sai dos trilhos.

Por que isto existe e não é burocracia. A lição 96 da casa diz que gate instalado em
rota que ninguém percorre é gate nenhum; a 189 diz que quem constrói o gate, mede com
ele e se aprova fecha um laço de autovalidação. Uma campanha de melhoria é exatamente
o momento em que os dois riscos se somam: há pressa, há muita mudança simultânea, e
quem julga é quem mexeu. Um invariante que roda a cada onda é o que impede a campanha
de destruir aquilo que ela deveria proteger.

O módulo é SOMENTE LEITURA sobre o estado da FORJA. Não promove fase, não altera caso,
não escreve em `state/`. Ele mede e reprova.

Uso:
    python forja_lapidacao_governanca.py --invariantes
    python forja_lapidacao_governanca.py --propriedade melhorias.json
    python forja_lapidacao_governanca.py --tudo --json
"""
from __future__ import annotations

import argparse
import ast
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

import forja_acervo

FORJA = Path(__file__).resolve().parent
FABRICA = FORJA.parent
STATE = FORJA / "state"
VERSAO = "FORJA-LAPIDACAO-GOV-v1"

# ---------------------------------------------------------------------------
# Limites decididos por Helena em 05/08/2026. Ficam aqui como DADO, para que
# ultrapassá-los seja uma alteração de código versionada e não uma decisão de
# momento tomada no meio de uma onda cansada.
# ---------------------------------------------------------------------------
LIMITES = {
    "ondas": 3,
    "tentativasPorMelhoria": 2,
    "agentesOnda1": 8,
    "agentesOnda2": 10,
    "agentesOnda3": 4,
    "agentesTotal": 22,
    "arquivosPorMelhoria": 6,
    "reprovacoesIguaisDaRegua": 3,
    "divergenciaTamanhoCegoPct": 20,
}

# Contagens medidas na versão congelada `forja-congelada-20260805` = 3866e1c16.
# Servem de piso: encolher qualquer uma destas é sinal de que a campanha removeu
# proteção em vez de acrescentar.
PISO_CONGELADO = {
    "reguaProtegidos": 139,
    "reguaSuites": 51,
    "baselineScripts": 41,
    "contratosFase": 11,
    "gatesLastro": 13,
}

GATES_LASTRO = (
    "L1-lastro", "L2-transcricao", "L3-superlativo", "L4-denominador",
    "L5-identidade", "L6-norma-por-ano", "L7-criterio-vigente", "L8-objecao",
    "L9-fonte-prevalente", "L10-data-base", "L11-valor-orfao",
    "L12-hierarquia-fonte", "L13-aritmetica-derivada",
)

CASO_FAIL_CLOSED = forja_acervo.caso("CASO-04-reconstrucao")

# Extensões que não podem estar versionadas no repositório do engine. A regra do
# dono: não levar casos, binários ou segredos ao repositório do engine.
BINARIOS_PROIBIDOS = {
    ".docx", ".doc", ".pdf", ".png", ".jpg", ".jpeg", ".emf", ".wmf",
    ".zip", ".rar", ".7z", ".xlsx", ".pptx", ".mp3", ".mp4", ".wav",
}

# Padrões de segredo. Deliberadamente estreitos: padrão largo produz falso
# positivo em massa, e nesta casa falso positivo em gate vira waiver diário.
PADROES_SEGREDO = (
    (r"\bsk-[A-Za-z0-9]{20,}", "chave OpenAI"),
    (r"\bghp_[A-Za-z0-9]{30,}", "token GitHub"),
    (r"\bAKIA[0-9A-Z]{16}\b", "chave AWS"),
    (r"\bxox[baprs]-[A-Za-z0-9-]{10,}", "token Slack"),
    (r"\bAIza[0-9A-Za-z_-]{30,}", "chave Google"),
)


def _achado(codigo: str, estado: str, evidencia: str, *, natureza: str = "comportamental") -> dict:
    """Estado é APROVADO, REPROVADO ou INDETERMINADO.

    `natureza` separa o que é conferido por comportamento do que é conferido por
    estrutura. A distinção não é cosmética: um invariante estrutural prova que o
    código continua lá, não que ele continua funcionando. Confundir os dois é o
    modo de falha "presença confundida com qualidade".
    """
    return {"codigo": codigo, "estado": estado, "evidencia": evidencia,
            "natureza": natureza}


# ---------------------------------------------------------------------------
# Invariantes — os critérios de parada imediata da Helena, computados
# ---------------------------------------------------------------------------

def inv_fail_closed_preservado(state: Path | None = None) -> dict:
    """I1: o caso travado por fonte não validada continua travado.

    Este é o invariante mais importante da campanha. Se a lapidação destravar
    sozinha um caso que estava fail-closed, ela quebrou exatamente o que deveria
    endurecer — e o faria em silêncio, porque destravar parece progresso.

    `state` existe para a contraprova: um invariante que nunca foi visto reprovando
    não é invariante, é decoração. O teste aponta para um estado forjado e exige
    REPROVADO.
    """
    estado = (state or STATE) / CASO_FAIL_CLOSED / "FORJA_N3_STATE.json"
    if not estado.is_file():
        return _achado("I1-fail-closed", "INDETERMINADO",
                       f"{CASO_FAIL_CLOSED}: FORJA_N3_STATE.json ausente")
    dados = json.loads(estado.read_text(encoding="utf-8", errors="replace"))
    bloqueios = dados.get("blockers") or []
    ciclo = str(dados.get("lifecycleStatus") or "")
    if not bloqueios:
        return _achado("I1-fail-closed", "REPROVADO",
                       f"{CASO_FAIL_CLOSED}: blockers esvaziou — o caso destravou "
                       "sem ato humano de validação da fonte prevalente")
    if ciclo in {"delivered", "completed", "protocolado"}:
        return _achado("I1-fail-closed", "REPROVADO",
                       f"{CASO_FAIL_CLOSED}: lifecycleStatus={ciclo} com bloqueio aberto")
    return _achado("I1-fail-closed", "APROVADO",
                   f"{CASO_FAIL_CLOSED}: {len(bloqueios)} bloqueio(s), "
                   f"lifecycleStatus={ciclo or 'não declarado'}, revision={dados.get('revision')}")


def inv_gates_lastro() -> dict:
    """I2-a: os treze gates L continuam emitindo achado sob o próprio código.

    Estrutural por desenho, e digo isso no retorno. A prova comportamental dos
    treze é `test_forja_lastro.py`, que o baseline roda; duplicá-la aqui custaria
    segundos a cada chamada sem acrescentar informação.
    """
    fonte = (FORJA / "forja_lastro.py").read_text(encoding="utf-8", errors="replace")
    faltando = [g for g in GATES_LASTRO if f'"{g}"' not in fonte]
    if faltando:
        return _achado("I2a-lastro-L1-L13", "REPROVADO",
                       f"gates ausentes em forja_lastro.py: {', '.join(faltando)}",
                       natureza="estrutural")
    versao = re.search(r'VERSAO\s*=\s*"([^"]+)"', fonte)
    return _achado("I2a-lastro-L1-L13", "APROVADO",
                   f"{len(GATES_LASTRO)}/13 gates presentes; "
                   f"VERSAO={versao.group(1) if versao else 'não lida'}; "
                   "prova comportamental em test_forja_lastro.py (baseline)",
                   natureza="estrutural")


def inv_porta_unica(kit: Path | None = None) -> dict:
    """I2-b: `PecaVisual.salvar()` continua chamando a validação da porta única.

    Conferido por AST e não por grep. A diferença importa: grep encontra a string
    num comentário ou num método morto; a AST prova que a chamada está no corpo do
    `salvar`, que é o único lugar onde ela fecha a porta.
    """
    caminho = kit or (FABRICA / "_FERRAMENTAS" / "medina_visual_kit.py")
    if not caminho.is_file():
        return _achado("I2b-porta-unica", "REPROVADO", f"{caminho} não existe")
    arvore = ast.parse(caminho.read_text(encoding="utf-8", errors="replace"))
    for classe in ast.walk(arvore):
        if not (isinstance(classe, ast.ClassDef) and classe.name == "PecaVisual"):
            continue
        for metodo in classe.body:
            if not (isinstance(metodo, ast.FunctionDef) and metodo.name == "salvar"):
                continue
            chamadas = {
                n.func.attr for n in ast.walk(metodo)
                if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
            }
            exigidas = {"_validar_porta_unica", "_validar_lastro_documental",
                        "_sanitizar_metadados"}
            faltando = exigidas - chamadas
            if faltando:
                return _achado("I2b-porta-unica", "REPROVADO",
                               f"PecaVisual.salvar não chama: {', '.join(sorted(faltando))}")
            return _achado("I2b-porta-unica", "APROVADO",
                           f"PecaVisual.salvar (linha {metodo.lineno}) chama as três "
                           "validações obrigatórias")
        return _achado("I2b-porta-unica", "REPROVADO", "PecaVisual existe mas não tem salvar()")
    return _achado("I2b-porta-unica", "REPROVADO", "classe PecaVisual não encontrada")


def inv_gate_humano() -> dict:
    """I3: nenhum agente escreveu `validadoPor`.

    Veto permanente do conselho. Um validador nominal é a assinatura de um humano;
    se um agente a escreve, toda a cadeia de lastro passa a repousar numa ficção.
    Procuro por valores que denunciem autoria de máquina.
    """
    suspeitos = re.compile(
        r"(claude|opus|sonnet|fable|gpt|codex|agente|agent|bot|runner|forja-|"
        r"python-docx|automat)", re.I)
    achados = []
    for caminho in STATE.rglob("*.json"):
        try:
            texto = caminho.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if "validadoPor" not in texto:
            continue
        for valor in re.findall(r'"validadoPor"\s*:\s*"([^"]{1,120})"', texto):
            if suspeitos.search(valor):
                achados.append(f"{caminho.relative_to(FORJA)}: validadoPor={valor!r}")
    if achados:
        return _achado("I3-gate-humano", "REPROVADO",
                       f"{len(achados)} validador(es) com cara de máquina: " +
                       "; ".join(achados[:5]))
    return _achado("I3-gate-humano", "APROVADO",
                   "nenhum validadoPor com assinatura de agente em state/")


def inv_repo_do_engine(versionados: list[str] | None = None) -> dict:
    """I4: casos, binários e segredos não entram no repositório do engine."""
    if versionados is None:
        try:
            saida = subprocess.run(
                ["git", "ls-files", "--", str(FORJA)],
                cwd=str(FORJA), capture_output=True, text=True, timeout=90,
                encoding="utf-8", errors="replace")
        except (OSError, subprocess.TimeoutExpired) as exc:
            return _achado("I4-repo-engine", "INDETERMINADO", f"git indisponível: {exc}")
        if saida.returncode != 0:
            return _achado("I4-repo-engine", "INDETERMINADO",
                           f"git ls-files retornou {saida.returncode}")
        versionados = [linha for linha in saida.stdout.splitlines() if linha.strip()]
    else:
        # Fixture controlável para a contraprova: a lógica de classificação não
        # pode ficar sem teste só porque o checkout real já está contaminado.
        versionados = [str(p) for p in versionados if str(p).strip()]
    binarios = [p for p in versionados if Path(p).suffix.lower() in BINARIOS_PROIBIDOS]
    # A primeira versão procurava "/state/" com barra inicial e nunca casava: o
    # `git ls-files` devolve caminho relativo, sem barra à frente. O invariante
    # deixou de reportar os casos de cliente versionados, que são justamente a
    # parte mais grave. Comparo por componente de caminho, que não depende de
    # como a barra caiu.
    casos = [p for p in versionados
             if "state" in Path(p.replace("\\", "/")).parts]
    problemas = []
    if binarios:
        problemas.append(f"{len(binarios)} binário(s) versionado(s), ex.: {binarios[0]}")
    if casos:
        pastas, arquivos_raiz = set(), 0
        for caminho in casos:
            partes = Path(caminho.replace("\\", "/")).parts
            indice_state = next(
                (i for i, parte in enumerate(partes) if parte.casefold() == "state"),
                None,
            )
            if indice_state is None:
                continue
            if len(partes) > indice_state + 2:
                pastas.add(partes[indice_state + 1])
            else:
                arquivos_raiz += 1
        detalhe = (
            f"{len(casos)} arquivo(s) de caso versionado(s) em {len(pastas)} pasta(s) "
            f"de state/, ex.: {sorted(pastas)[0] if pastas else '?'}"
        )
        if arquivos_raiz:
            detalhe += f"; {arquivos_raiz} arquivo(s) diretamente na raiz de state/"
        problemas.append(detalhe)
    if problemas:
        return _achado("I4-repo-engine", "REPROVADO", "; ".join(problemas))
    return _achado("I4-repo-engine", "APROVADO",
                   f"{len(versionados)} arquivos versionados, nenhum binário proibido, "
                   "nenhum material de caso")


def inv_segredos() -> dict:
    """I5: nenhum segredo em arquivo versionado do engine."""
    encontrados = []
    for caminho in FORJA.rglob("*"):
        if not caminho.is_file() or caminho.suffix.lower() not in {
                ".py", ".json", ".md", ".txt", ".yaml", ".yml", ".cfg", ".ini"}:
            continue
        partes = set(caminho.parts)
        if partes & {"__pycache__", ".git", "state", "telemetria", "cache"}:
            continue
        try:
            if caminho.stat().st_size > 2_000_000:
                continue
            texto = caminho.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for padrao, rotulo in PADROES_SEGREDO:
            if re.search(padrao, texto):
                encontrados.append(f"{caminho.relative_to(FORJA)}: {rotulo}")
    if encontrados:
        return _achado("I5-segredos", "REPROVADO",
                       f"{len(encontrados)}: " + "; ".join(encontrados[:5]))
    return _achado("I5-segredos", "APROVADO",
                   f"{len(PADROES_SEGREDO)} padrões de segredo varridos, nenhuma ocorrência")


def inv_piso_de_protecao() -> dict:
    """I6: a campanha não pode encolher a proteção que encontrou.

    Acrescentar gate é fácil de contar e fácil de fingir. Remover proteção é o
    que de fato piora o sistema, e passa despercebido porque a suíte fica verde
    justamente por ter menos coisa a conferir.
    """
    medido, problemas = {}, []
    try:
        sys.path.insert(0, str(FORJA))
        import forja_regua as regua
        import forja_baseline as baseline
        medido["reguaProtegidos"] = len(regua.PROTEGIDOS)
        medido["reguaSuites"] = len(regua.SUITES)
        medido["baselineScripts"] = len(baseline.SUITES_SCRIPT)
    except Exception as exc:  # noqa: BLE001 — qualquer falha aqui é indeterminação real
        return _achado("I6-piso-protecao", "INDETERMINADO",
                       f"não foi possível medir régua/baseline: {type(exc).__name__}: {exc}")
    medido["contratosFase"] = len(list((FORJA / "phase_contracts").glob("F*.json")))
    medido["gatesLastro"] = len(GATES_LASTRO)
    for chave, piso in PISO_CONGELADO.items():
        atual = medido.get(chave)
        if atual is None:
            continue
        if atual < piso:
            problemas.append(f"{chave}: {atual} < piso {piso}")
    if problemas:
        return _achado("I6-piso-protecao", "REPROVADO",
                       "proteção encolheu — " + "; ".join(problemas))
    return _achado("I6-piso-protecao", "APROVADO",
                   "; ".join(f"{k}={v}(piso {PISO_CONGELADO.get(k, '-')})"
                             for k, v in sorted(medido.items())))


def inv_f2a_congelado(state: Path | None = None) -> dict:
    """I7: o F2A v2 continua congelado (§ 21 do plano 40, decisão unânime de 05/08).

    Confere o que está EM USO nos casos, não o que está escrito no plano. Plano
    diz intenção; árvore de perguntas diz o que rodou.

    A primeira versão deste invariante lia `schemaVersion` e teria sido cega para
    sempre: as 16 árvores trazem `schemaVersion="1"`, e o protocolo do F2A vive em
    `protocolVersion` ("FORJA-F2A-100-v1", em 14 delas). É a lição 188 da casa
    repetida em código novo — gate que lê a chave errada aprova por não enxergar.
    Por isso a varredura agora cobre os dois campos e devolve o que encontrou, para
    que o silêncio nunca seja confundido com aprovação.
    """
    protocolos, campos_lidos = Counter(), ("protocolVersion", "schemaVersion")
    total = 0
    for caminho in (state or STATE).rglob("F2_QUESTION_TREE.json"):
        try:
            dados = json.loads(caminho.read_text(encoding="utf-8", errors="replace"))
        except (OSError, json.JSONDecodeError):
            continue
        total += 1
        for campo in campos_lidos:
            valor = dados.get(campo)
            if isinstance(valor, str) and "F2A" in valor.upper():
                protocolos[valor] += 1
    v2 = [p for p in protocolos if re.search(r"F2A[^0-9]*100[^0-9]*v[2-9]|F2A.*-v[2-9]\b", p, re.I)]
    if v2:
        return _achado("I7-f2a-congelado", "REPROVADO",
                       f"protocolo F2A v2+ em uso apesar do congelamento de 05/08: {v2}")
    if total and not protocolos:
        return _achado("I7-f2a-congelado", "INDETERMINADO",
                       f"{total} árvore(s) F2 e nenhum marcador F2A em "
                       f"{'/'.join(campos_lidos)} — o invariante pode ter ficado cego "
                       "de novo; conferir onde o protocolo passou a ser declarado")
    return _achado("I7-f2a-congelado", "APROVADO",
                   f"{total} árvore(s) F2; protocolos F2A em uso: {dict(protocolos)}")


INVARIANTES = (
    inv_fail_closed_preservado,
    inv_gates_lastro,
    inv_porta_unica,
    inv_gate_humano,
    inv_repo_do_engine,
    inv_segredos,
    inv_piso_de_protecao,
    inv_f2a_congelado,
)


def verificar_invariantes() -> dict:
    resultados = []
    for funcao in INVARIANTES:
        try:
            resultados.append(funcao())
        except Exception as exc:  # noqa: BLE001
            resultados.append(_achado(
                funcao.__name__, "INDETERMINADO",
                f"invariante levantou {type(exc).__name__}: {exc}"))
    reprovados = [r for r in resultados if r["estado"] == "REPROVADO"]
    indeterminados = [r for r in resultados if r["estado"] == "INDETERMINADO"]
    return {
        "schemaVersion": VERSAO,
        # Indeterminado não é aprovação. Um invariante que não conseguiu medir
        # deixa a campanha em estado de não saber, e não saber não libera onda.
        "veredito": "REPROVADO" if reprovados else (
            "INDETERMINADO" if indeterminados else "APROVADO"),
        "reprovados": [r["codigo"] for r in reprovados],
        "indeterminados": [r["codigo"] for r in indeterminados],
        "invariantes": resultados,
    }


# ---------------------------------------------------------------------------
# Propriedade de arquivo — serializa a escrita da onda 2
# ---------------------------------------------------------------------------

def propriedade_arquivo(melhorias: list[dict]) -> dict:
    """Reparte os arquivos entre as melhorias e serializa quem colide.

    Paralelizar dois agentes que escrevem no mesmo arquivo custa duas vezes o
    trabalho e uma terceira para resolver o conflito. Aqui a colisão é detectada
    antes de qualquer agente ser lançado.

    Cada melhoria é {"id": str, "arquivos": [str, ...]}. Devolve os lotes que
    podem correr em paralelo e as violações de limite.
    """
    dono: dict[str, list[str]] = {}
    for m in melhorias:
        for arquivo in m.get("arquivos") or []:
            dono.setdefault(_normalizar(arquivo), []).append(str(m.get("id")))
    disputados = {a: ids for a, ids in dono.items() if len(set(ids)) > 1}

    excesso = [
        {"id": str(m.get("id")), "arquivos": len(m.get("arquivos") or [])}
        for m in melhorias
        if len(m.get("arquivos") or []) > LIMITES["arquivosPorMelhoria"]
    ]

    # Coloração gulosa: uma melhoria entra no primeiro lote em que não encontra
    # arquivo já reservado. Não busco o ótimo — buscar o mínimo de lotes aqui
    # gastaria mais do que economiza, e qualquer partição correta já elimina o
    # conflito, que é o objetivo.
    lotes: list[dict] = []
    for m in sorted(melhorias, key=lambda x: -len(x.get("arquivos") or [])):
        arquivos = {_normalizar(a) for a in (m.get("arquivos") or [])}
        for lote in lotes:
            if not (arquivos & lote["arquivos"]):
                lote["melhorias"].append(str(m.get("id")))
                lote["arquivos"] |= arquivos
                break
        else:
            lotes.append({"melhorias": [str(m.get("id"))], "arquivos": set(arquivos)})

    maior = max((len(l["melhorias"]) for l in lotes), default=0)
    return {
        "schemaVersion": VERSAO,
        "melhorias": len(melhorias),
        "arquivosDistintos": len(dono),
        "arquivosDisputados": {a: sorted(set(ids)) for a, ids in disputados.items()},
        "excedemLimiteDeArquivos": excesso,
        "lotesSerializados": [
            {"ordem": i + 1, "melhorias": l["melhorias"],
             "arquivos": sorted(l["arquivos"])}
            for i, l in enumerate(lotes)
        ],
        "paraleloMaximoSeguro": min(maior, LIMITES["agentesOnda2"]),
        "veredito": "REPROVADO" if excesso else "APROVADO",
        "motivo": (
            f"{len(excesso)} melhoria(s) tocam mais de {LIMITES['arquivosPorMelhoria']} "
            "arquivos — nesta casa isso é refatoração disfarçada, não melhoria"
        ) if excesso else "nenhuma melhoria excede o limite de arquivos",
    }


def _normalizar(caminho: str) -> str:
    return str(caminho).replace("\\", "/").lstrip("./").lower()


# ---------------------------------------------------------------------------
# Sinais de desperdício
# ---------------------------------------------------------------------------

def sinais_desperdicio(propostas: list[dict], *, agentes_gastos: int = 0) -> dict:
    """Mede se a onda está queimando esforço à toa.

    Os sinais são os da decisão da Helena, traduzidos em contagem. O mais útil é
    o de duplicidade: dois agentes que chegaram à mesma proposta com títulos
    diferentes provam que o fan-out foi mal particionado, e o custo já foi pago
    duas vezes — o que se evita é pagar a terceira.
    """
    sinais = []

    def assinatura(p: dict) -> str:
        arquivos = tuple(sorted(_normalizar(a) for a in (p.get("arquivos") or [])))
        return json.dumps(arquivos)

    por_arquivo = Counter(assinatura(p) for p in propostas if p.get("arquivos"))
    duplicadas = {k: v for k, v in por_arquivo.items() if v > 1}
    if duplicadas:
        sinais.append({
            "sinal": "propostas-duplicadas",
            "detalhe": f"{len(duplicadas)} conjunto(s) de arquivos propostos por mais "
                       "de um agente — fan-out mal particionado",
        })

    vazias = [p for p in propostas if not (p.get("arquivos") or [])]
    if vazias:
        sinais.append({
            "sinal": "proposta-sem-arquivo",
            "detalhe": f"{len(vazias)} proposta(s) não nomeiam arquivo — candidatas a "
                       "mudança documental sem mudança operacional",
        })

    sem_sabotagem = [p for p in propostas if not str(p.get("sabotagemMaliciosa") or "").strip()]
    if sem_sabotagem:
        sinais.append({
            "sinal": "sem-contraprova",
            "detalhe": f"{len(sem_sabotagem)} proposta(s) sem sabotagem declarada — "
                       "sem contraprova não há como saber se o gate enxerga",
        })

    if agentes_gastos > LIMITES["agentesTotal"]:
        sinais.append({
            "sinal": "teto-de-agentes-estourado",
            "detalhe": f"{agentes_gastos} > {LIMITES['agentesTotal']} — exige ato do Igor",
        })

    return {
        "schemaVersion": VERSAO,
        "propostas": len(propostas),
        "agentesGastos": agentes_gastos,
        "sinais": sinais,
        "veredito": "REPROVADO" if sinais else "APROVADO",
    }


# ---------------------------------------------------------------------------

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Governança executável da lapidação da FORJA (Helena + Efesto)")
    parser.add_argument("--invariantes", action="store_true",
                        help="confere os critérios de parada imediata contra o estado vivo")
    parser.add_argument("--propriedade", type=Path,
                        help="JSON com [{id, arquivos:[...]}] para serializar a onda 2")
    parser.add_argument("--desperdicio", type=Path,
                        help="JSON com as propostas da onda, para medir sinais de desperdício")
    parser.add_argument("--agentes-gastos", type=int, default=0)
    parser.add_argument("--tudo", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    saida: dict = {"schemaVersion": VERSAO, "limites": LIMITES}
    codigo = 0

    if args.invariantes or args.tudo:
        saida["invariantes"] = verificar_invariantes()
        if saida["invariantes"]["veredito"] != "APROVADO":
            codigo = 2

    if args.propriedade:
        dados = json.loads(args.propriedade.read_text(encoding="utf-8", errors="replace"))
        saida["propriedade"] = propriedade_arquivo(dados)
        if saida["propriedade"]["veredito"] != "APROVADO":
            codigo = 2

    if args.desperdicio:
        dados = json.loads(args.desperdicio.read_text(encoding="utf-8", errors="replace"))
        saida["desperdicio"] = sinais_desperdicio(dados, agentes_gastos=args.agentes_gastos)
        if saida["desperdicio"]["veredito"] != "APROVADO":
            codigo = 2

    if len(saida) == 2 and not args.tudo:
        parser.print_help()
        return 1

    if args.json:
        print(json.dumps(saida, ensure_ascii=False, indent=2))
        return codigo

    inv = saida.get("invariantes")
    if inv:
        print(f"INVARIANTES — {inv['veredito']}")
        for r in inv["invariantes"]:
            marca = {"APROVADO": "ok ", "REPROVADO": "XX ", "INDETERMINADO": "?? "}[r["estado"]]
            print(f"  {marca}{r['codigo']} [{r['natureza']}] {r['evidencia']}")
    prop = saida.get("propriedade")
    if prop:
        print(f"\nPROPRIEDADE DE ARQUIVO — {prop['veredito']}: {prop['motivo']}")
        for lote in prop["lotesSerializados"]:
            print(f"  lote {lote['ordem']}: {', '.join(lote['melhorias'])}")
        for arquivo, ids in prop["arquivosDisputados"].items():
            print(f"  disputado: {arquivo} <- {', '.join(ids)}")
    desp = saida.get("desperdicio")
    if desp:
        print(f"\nDESPERDÍCIO — {desp['veredito']}")
        for s in desp["sinais"]:
            print(f"  ! {s['sinal']}: {s['detalhe']}")
    return codigo


if __name__ == "__main__":  # pragma: no cover
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    raise SystemExit(main())
