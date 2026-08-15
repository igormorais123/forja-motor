# -*- coding: utf-8 -*-
"""forja_entrega.py — gates computados de reconciliação e entrega.

    F0   `mapping_valid`, `status_consistent`
    F9   `attachments_exact`, `hashes_current`, `email_claims_true`

`email_claims_true` é o mais perigoso da esteira inteira, e por um motivo que
não tem nada de técnico: é o único artefato que o Fábio lê antes de decidir. Um
e-mail que anuncia o que a peça não faz produz decisão errada com peça certa, e
o erro só aparece quando alguém abre o anexo. Nenhum revisor de código pega
isso, e o agente que escreve o e-mail é o mesmo que atesta que ele é verdadeiro.

O que se computa não é a veracidade retórica do texto — isso é leitura humana.
É a coerência entre o que o e-mail anuncia e o que o pacote contém:

    LE1  o e-mail cita anexo que o manifesto não lista
    LE2  o e-mail anuncia liberação que a política do pacote nega
    LE3  o manifesto aponta artefato que não existe
    LE4  o manifesto declara hash que não confere com o arquivo

`mapping_valid` fecha o buraco que custou meia manhã hoje: o `caseFolder` do
manifesto é a única fonte confiável da pasta do cliente, e o recomputo de lastro
depende dele. Manifesto apontando para pasta inexistente faz o L2 acusar de
"fonte não localizada" quem transcreveu corretamente.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

_GATE_VERSAO = "FORJA-ENTREGA-v1"
GATE_MAPEAMENTO = "mapping_valid"
GATE_STATUS = "status_consistent"
GATE_ANEXOS = "attachments_exact"
GATE_HASHES = "hashes_current"
GATE_EMAIL = "email_claims_true"
# Declarado no contrato da F9 desde sempre e sem nenhum produtor em Python até
# 04/08/2026 — o instrumento de liveness o classificava como complacente, isto é,
# atestado por quem escreve o e-mail. `forja_estilo_humano` já sabia analisar
# texto de e-mail (`tipo="email"`); faltava alguém chamá-lo e emitir o veredito.
GATE_EMAIL_ESTILO = "email_human_style_passed"

_LIMITE_EXEMPLOS = 4
# Promessas de liberação que o e-mail pode fazer e o pacote pode desmentir.
_PROMESSA_EXTERNA = re.compile(
    r"(?i)\b(pront[oa]s? para (?:o )?protocolo|pode ser protocolad|protocol[áa]vel|"
    r"pront[oa]s? para o cliente|liberad[oa]s? para o cliente|"
    r"pode ser enviad[oa]s? ao cliente)\b")
_POLITICA_INTERNA = re.compile(r"(?i)internal|interno|decision_support|office_review|draft")


# O relatório de reconciliação é MARKDOWN em todo o acervo — `forja_reconcile.py`
# nunca emitiu a versão JSON que este gate procurava. Resultado medido em
# 04/08/2026: `status_consistent` respondeu `warn` nas três tentativas reais e
# jamais conseguiu dizer `pass`. Gate que não sabe aprovar é tão inútil quanto
# o que não sabe reprovar: vira ruído que o operador aprende a ignorar, e aí
# deixa de ver também o dia em que ele reprova de verdade.
_SECAO_STATUS = re.compile(r"(?im)^#{1,6}\s*status\b[^\n]*\n((?:(?!^#{1,6}\s).*\n?)*)")
_SEM_DIVERGENCIA = re.compile(
    r"(?i)nenhuma (?:inconsist[êe]ncia|diverg[êe]ncia)|sem (?:inconsist[êe]ncia|diverg[êe]ncia)|"
    r"consistente|nada a reconciliar")
_COM_DIVERGENCIA = re.compile(
    r"(?im)^\s*[-*]\s*(?:diverg[êe]ncia|inconsist[êe]ncia|conflito)\b")


def _reconciliacao_em_texto(texto: str):
    """Lê status e divergências do relatório em markdown.

    Devolve `(None, None)` quando o relatório não tem seção de status: aí o gate
    fica em `warn` por não ter o que ler, e não por ter lido algo errado.
    """
    secao = _SECAO_STATUS.search(texto)
    if not secao:
        return None, None
    corpo = secao.group(1)
    divergencias = _COM_DIVERGENCIA.findall(corpo)
    if _SEM_DIVERGENCIA.search(corpo) and not divergencias:
        return "consistente", []
    return ("divergente" if divergencias else "declarado"), divergencias


def validar_reconciliacao(manifesto, relatorio=None):
    """Gates da F0: o manifesto aponta para lugares que existem."""
    achados = []
    fonte = manifesto if isinstance(manifesto, dict) else {}
    if not fonte:
        return {"versao": _GATE_VERSAO,
                "findings": [{"gate": "LE0-manifesto-ausente", "sev": "P0",
                              "problema": "case_manifest ausente ou vazio",
                              "acao": "emita o manifesto do caso na F0",
                              "versao": _GATE_VERSAO}],
                "gates": {GATE_MAPEAMENTO: "fail", GATE_STATUS: "fail"}}

    quebrados = []
    for campo in ("caseFolder", "commandFile"):
        valor = fonte.get(campo)
        if not valor:
            quebrados.append(f"{campo} nao declarado")
            continue
        alvo = Path(str(valor))
        if not alvo.exists():
            quebrados.append(f"{campo} aponta para caminho inexistente")

    if quebrados:
        achados.append({
            "gate": "LE1-mapeamento-quebrado", "sev": "P0",
            "problema": ("o manifesto do caso nao mapeia para o material real: "
                         + "; ".join(quebrados)),
            "acao": ("corrija caseFolder e commandFile - o recomputo de lastro depende deles "
                     "para localizar as fontes do cliente"),
            "versao": _GATE_VERSAO})

    identidade = [c for c in ("caseId", "demandId") if not fonte.get(c)]
    if identidade:
        achados.append({
            "gate": "LE2-identidade-incompleta", "sev": "P1",
            "problema": f"o manifesto nao declara {', '.join(identidade)}",
            "acao": "declare a identidade do caso e da demanda",
            "versao": _GATE_VERSAO})

    mapeamento = "fail" if any(a["sev"] == "P0" for a in achados) else "pass"
    status = "pass"
    if isinstance(relatorio, str) and relatorio.strip():
        declarado, divergencias = _reconciliacao_em_texto(relatorio)
    elif isinstance(relatorio, dict) and relatorio:
        declarado = str(relatorio.get("status") or "").strip().lower()
        divergencias = relatorio.get("divergences") or relatorio.get("divergencias") or []
    else:
        declarado, divergencias = None, None

    if declarado is None:
        status = "warn"
    elif divergencias:
        achados.append({
            "gate": "LE3-status-contradiz-divergencias", "sev": "P0",
            "problema": (f"o relatorio se declara '{declarado}' e a fila continua "
                         f"com {len(divergencias)} divergencia(s) em aberto"),
            "acao": ("resolva a divergencia entre painel e estado - `status_consistent` afirma "
                     "que os dois contam a mesma historia, e enquanto houver divergencia listada "
                     "isso e falso, com ou sem rotulo honesto"),
            "versao": _GATE_VERSAO})
        status = "fail"

    return {"versao": _GATE_VERSAO, "findings": achados,
            "gates": {GATE_MAPEAMENTO: mapeamento, GATE_STATUS: status}}


def _entregaveis(manifesto: dict) -> list:
    for campo in ("deliverables", "entregaveis", "artifacts", "attachments"):
        valor = manifesto.get(campo)
        if isinstance(valor, list) and valor:
            return [item for item in valor if isinstance(item, dict)]
    return []


def _corpo_email(email) -> str:
    """Extrai o corpo real sem confundir metadados JSON com a redação."""
    if isinstance(email, str):
        return email
    if not isinstance(email, dict):
        return ""
    for chave in ("body", "corpo", "text", "texto", "markdown", "content"):
        valor = email.get(chave)
        if isinstance(valor, str) and valor.strip():
            return valor
    for chave in ("email", "message", "mensagem"):
        valor = email.get(chave)
        if isinstance(valor, dict):
            corpo = _corpo_email(valor)
            if corpo:
                return corpo
    return ""


def validar_pacote(manifesto, email=None, base_dir=None, artefatos_existentes=None):
    """Gates da F9: anexos exatos, hashes atuais e e-mail que não promete demais."""
    achados = []
    fonte = manifesto if isinstance(manifesto, dict) else {}
    if not fonte:
        return {"versao": _GATE_VERSAO,
                "findings": [{"gate": "LE4-manifesto-ausente", "sev": "P0",
                              "problema": "package_manifest ausente ou vazio",
                              "acao": "emita o manifesto do pacote na F9",
                              "versao": _GATE_VERSAO}],
                "gates": {GATE_ANEXOS: "fail", GATE_HASHES: "fail", GATE_EMAIL: "fail"}}

    entregaveis = _entregaveis(fonte)
    if not entregaveis:
        achados.append({
            "gate": "LE5-pacote-sem-entregavel", "sev": "P0",
            "problema": ("o manifesto do pacote nao lista nenhum entregavel - o gate seria "
                         "calculado sobre conjunto vazio"),
            "acao": "liste os entregaveis do pacote",
            "versao": _GATE_VERSAO})
        return {"versao": _GATE_VERSAO, "findings": achados,
                "gates": {GATE_ANEXOS: "fail", GATE_HASHES: "fail", GATE_EMAIL: "fail"}}

    # LE3 — o manifesto aponta para artefatos que existem.
    conhecidos = set(artefatos_existentes or [])
    faltando = []
    if conhecidos:
        for item in entregaveis:
            for chave, valor in item.items():
                if chave.endswith("ArtifactId") and isinstance(valor, str) and valor:
                    if valor not in conhecidos:
                        faltando.append(f"{item.get('id') or '?'}: {valor}")
    if faltando:
        achados.append({
            "gate": "LE6-anexo-inexistente", "sev": "P0",
            "problema": (f"o manifesto aponta {len(faltando)} artefato(s) que a fase nao produziu: "
                         f"{', '.join(faltando[:_LIMITE_EXEMPLOS])}"),
            "acao": "corrija as referencias do manifesto ou produza os artefatos faltantes",
            "versao": _GATE_VERSAO})
    anexos = "fail" if faltando else ("pass" if conhecidos else "warn")

    # LE4 — hashes declarados conferem.
    divergentes, conferidos = [], 0
    for item in entregaveis:
        caminho = item.get("path") or item.get("file")
        digest = item.get("sha256") or item.get("hash")
        if not caminho or not digest:
            continue
        alvo = Path(str(caminho))
        if not alvo.is_absolute() and base_dir:
            alvo = Path(base_dir) / alvo
        if not alvo.is_file():
            divergentes.append(f"{item.get('id') or caminho}: arquivo ausente")
            continue
        conferidos += 1
        if hashlib.sha256(alvo.read_bytes()).hexdigest().lower() != str(digest).lower():
            divergentes.append(f"{item.get('id') or caminho}: hash divergente")
    if divergentes:
        achados.append({
            "gate": "LE7-hash-desatualizado", "sev": "P0",
            "problema": (f"{len(divergentes)} entregavel(is) com hash que nao confere: "
                         f"{', '.join(divergentes[:_LIMITE_EXEMPLOS])}"),
            "acao": "regere o pacote a partir dos arquivos atuais",
            "versao": _GATE_VERSAO})
    hashes = "fail" if divergentes else ("pass" if conferidos else "warn")

    # LE1/LE2 — o e-mail não promete o que o pacote não entrega.
    texto = email if isinstance(email, str) else (
        json.dumps(email, ensure_ascii=False) if isinstance(email, dict) else "")
    corpo_email = _corpo_email(email)
    if not texto.strip():
        achados.append({
            "gate": "LE8-email-ausente", "sev": "P1",
            "problema": "nao ha texto de e-mail para conferir contra o pacote",
            "acao": "emita email_response na F9",
            "versao": _GATE_VERSAO})
        emails = "warn"
    else:
        politicas = " ".join(str(item.get("releasePolicy") or item.get("audience") or "")
                             for item in entregaveis)
        promessa = _PROMESSA_EXTERNA.search(texto)
        if promessa and _POLITICA_INTERNA.search(politicas) and "strict_protocol" not in politicas:
            achados.append({
                "gate": "LE9-email-promete-alem-do-pacote", "sev": "P0",
                "problema": (f"o e-mail anuncia '{promessa.group(0)}' enquanto o pacote classifica "
                             f"os entregaveis como uso interno ({politicas[:80]})"),
                "acao": ("alinhe o e-mail a politica de liberacao do pacote - e o unico artefato "
                         "que o destinatario le antes de decidir"),
                "versao": _GATE_VERSAO})
            emails = "fail"
        elif not entregaveis:
            # Sem entregáveis no pacote não há o que o e-mail possa desmentir, e
            # `pass` aqui é atestado sobre o vazio: o canário de mutação zerou o
            # manifesto e este gate continuou aprovando. Nada a conferir é `warn`,
            # nunca aprovação — `fail` fica reservado ao verificavelmente falso.
            achados.append({
                "gate": "LE9-email-sem-pacote-a-conferir", "sev": "P1",
                "problema": "o pacote nao lista entregaveis, entao as promessas do e-mail "
                            "nao podem ser conferidas contra coisa nenhuma",
                "acao": "emita o manifesto com os entregaveis antes de cobrar o e-mail",
                "versao": _GATE_VERSAO})
            emails = "warn"
        else:
            emails = "pass"

    # Estilo humano do e-mail. `warn` quando não há texto — ausência não é
    # reprovação —, `fail` só diante de achado P0 do analisador, que é o
    # verificavelmente artificial: cabeçalho de máquina, fórmula pronta,
    # metadiscurso vazio. Achado leve fica em `warn` porque o analisador mede
    # indício, e indício de estilo não derruba entrega.
    if not corpo_email:
        estilo = "warn"
    else:
        from forja_estilo_humano import analisar as _analisar_estilo

        achados_estilo = _analisar_estilo(corpo_email, tipo="email")
        p0_estilo = [x for x in achados_estilo if x.get("sev") == "P0"]
        achados.extend({**x, "versao": _GATE_VERSAO} for x in p0_estilo)
        estilo = "fail" if p0_estilo else ("warn" if achados_estilo else "pass")

    return {"versao": _GATE_VERSAO, "findings": achados,
            "gates": {GATE_ANEXOS: anexos, GATE_HASHES: hashes, GATE_EMAIL: emails,
                      GATE_EMAIL_ESTILO: estilo}}


if __name__ == "__main__":  # pragma: no cover
    import sys

    pasta = Path(sys.argv[1] if len(sys.argv) > 1 else ".")

    def _ler(nome):
        alvo = pasta / nome
        if not alvo.is_file():
            return {}
        try:
            return json.loads(alvo.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            return {}

    saida = validar_reconciliacao(_ler("case_manifest.json"), _ler("reconciliation_report.json"))
    pacote = validar_pacote(_ler("package_manifest.json"), _ler("email_response.json"), pasta)
    saida["findings"].extend(pacote["findings"])
    saida["gates"].update(pacote["gates"])
    print(json.dumps(saida, ensure_ascii=False, indent=2))
