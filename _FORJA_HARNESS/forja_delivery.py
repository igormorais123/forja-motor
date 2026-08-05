"""FORJA N2 - M5/F10: pacote de revisão + trilha de evidência (modo leitura / sombra).

Para a demanda piloto, verifica CADA elo da trilha exigida pela spec N2 para uma
demanda ir de aberta a cumprida:
  comando -> fontes -> minuta -> auditoria -> QA visual -> entrega -> evidência

Gera F10_TRILHA_EVIDENCIA.md e monta o pacote de revisão em
state/<caseId>/pacote_revisao/ (cópias; nada é movido). Gate N2: `cumprida`
sem evidência arquivada = reprovado.
"""

import json
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

from forja_adversarial_audit import response_product_required, validate_adversarial_audit
from forja_memoria_auditabilidade import build_bundle, validate_bundle
from forja_n3_common import now_iso, read_json

FORJA = Path(__file__).resolve().parent
RAIZ = FORJA.parent
DATA = RAIZ / "gestao_escritorio" / "data"

COMANDOS = ["COMANDO_DO_EMAIL.md", "COMANDO_DO_WHATSAPP.md", "COMANDO_HERMES.md", "COMANDO_MANUAL.md"]


def achar(pasta, padroes):
    for pat in padroes:
        hits = sorted(pasta.glob(pat))
        if hits:
            return hits[0]
    return None


def ref_ok(ref, allow_text=False):
    if ref is None:
        return False
    if isinstance(ref, Path):
        return ref.exists()
    if isinstance(ref, list):
        return bool(ref) and all(ref_ok(x, allow_text=False) for x in ref)
    if isinstance(ref, str):
        if allow_text:
            return bool(ref.strip())
        return Path(ref).exists()
    return False


def ref_text(ref):
    if isinstance(ref, list):
        return "; ".join(str(x) for x in ref)
    return str(ref) if ref is not None else "NAO LOCALIZADO"


def append_unique(existing, value):
    items = list(existing or [])
    if value not in items:
        items.append(value)
    return items


def f7_com_lastro(f7):
    """Régua anti-fraude (10/07/2026): F7 só vale se p0 == 0 E o hash do fonte bater.

    A entrada canônica grava mdSha256 do markdown no F7; aqui o hash é RECOMPUTADO
    do arquivo real. F7 escrito à mão, com hash errado ou apontando para fonte
    alterado depois da composição — não fecha demanda. Aceita o formato simples
    (arquivo+mdSha256 na raiz) e o consolidado (documentos: {nome: {arquivo, mdSha256}}).
    Retorna (ok: bool, motivo: str)."""
    import hashlib

    def hash_bate(entrada):
        arq, sha = entrada.get("arquivo"), entrada.get("mdSha256")
        if not arq or not sha:
            return False, "sem mdSha256/arquivo (F7 antigo ou forjado — reexecutar a entrada canônica da FORJA)"
        p = Path(arq)
        if not p.exists():
            return False, f"fonte não existe: {arq}"
        real = hashlib.sha256(p.read_text(encoding="utf-8").encode("utf-8")).hexdigest()
        if real != sha:
            return False, f"hash do fonte NÃO bate ({Path(arq).name}: F7 desatualizado ou forjado)"
        from forja_metricas_f7 import metricas_f7
        from forja_verificador import verificar

        texto = p.read_text(encoding="utf-8", errors="replace")
        p0 = [item for item in verificar(texto, "peca") if item.get("sev") == "P0"]
        if p0:
            return False, f"gate recomputado reprovou: {p0[0]['gate']}"
        metrics = metricas_f7(texto, require_live=True)
        pending = metrics.get("citacoesNaoConferidas") or []
        if pending:
            return False, "autoridades sem lastro atual: " + ", ".join(map(str, pending[:5]))
        return True, "hash e inventário jurídico recomputados"

    if f7.get("p0") != 0:
        return False, f"p0={f7.get('p0')}"
    docs = f7.get("documentos")
    if isinstance(docs, dict) and docs:
        for nome, entrada in docs.items():
            if entrada.get("p0") != 0:
                return False, f"{nome}: p0={entrada.get('p0')}"
            ok, motivo = hash_bate(entrada)
            if not ok:
                return False, f"{nome}: {motivo}"
        return True, f"lastro ok em {len(docs)} documento(s)"
    return hash_bate(f7)


def f5_checklist_ok(path):
    """Checklist legado só satisfaz o elo quando declara zero pendências."""
    path = Path(path)
    if not path.is_file():
        return False, "checklist F5 ausente"
    text = path.read_text(encoding="utf-8", errors="replace")
    match = re.search(
        r"Pendentes de conferência[^:]*:\s*\*\*(\d+)\*\*",
        text,
        re.I,
    )
    if not match:
        return False, "checklist F5 sem balanço de pendências verificável"
    pending = int(match.group(1))
    return pending == 0, f"pendências declaradas: {pending}"


def parecer_valido(path):
    """Régua anti-fraude (10/07/2026): parecer do conselho só vale com conteúdo real.

    Exige: >= 800 caracteres, >= 3 recomendações numeradas e nenhum placeholder de
    template. Arquivo vazio ou esqueleto criado só para o gate passar — reprova.
    Retorna (ok: bool, motivo: str)."""
    import re as _re
    if path is None or not Path(path).exists():
        return False, "arquivo não existe"
    texto = Path(path).read_text(encoding="utf-8", errors="replace")
    if len(texto.strip()) < 800:
        return False, f"conteúdo insuficiente ({len(texto.strip())} chars < 800)"
    recomendacoes = _re.findall(r"^\s{0,3}(?:\*\*)?\d{1,2}[\.\)]\s+\S", texto, _re.M)
    if len(recomendacoes) < 3:
        return False, f"menos de 3 recomendações numeradas ({len(recomendacoes)})"
    if _re.search(r"\[(?:preencher|todo|xxx|inserir)[^\]]*\]|lorem ipsum", texto, _re.I):
        return False, "placeholder de template no parecer"
    return True, f"{len(recomendacoes)} recomendações numeradas, {len(texto)} chars"


# M2.1 (plano 19, ordem do Igor 09/07 + lição 62): parecer do conselho deve ser
# ANTERIOR ao início da redação (F6). Casos com F6 iniciado antes do corte seguem
# a regra antiga (mesma transição usada nos formatos legados de metadados).
CORTE_ORDEM_PARECER = datetime.fromisoformat("2026-07-12T00:00:00-03:00")


def _parse_iso(texto):
    try:
        return datetime.fromisoformat(texto)
    except (ValueError, TypeError):
        return None


def parecer_antes_da_redacao(parecer, state):
    """Verifica a ordem parecer -> redação usando o phaseHistory (dado registrado)
    contra o nascimento do arquivo de parecer (st_ctime no Windows = criação).
    Retorna (ok: bool, motivo: str)."""
    hist = state.get("phaseHistory") or []
    inicios_f6 = [_parse_iso(h.get("at")) for h in hist
                  if str(h.get("phase", "")).startswith("F6")]
    inicios_f6 = [t for t in inicios_f6 if t]
    if not inicios_f6:
        return True, "redação (F6) ainda não registrada"
    f6_inicio = min(inicios_f6)
    if f6_inicio < CORTE_ORDEM_PARECER:
        return True, "caso legado (F6 anterior a 12/07/2026) — regra de ordem não retroage"
    if parecer is None or not Path(parecer).exists():
        return False, "parecer inexistente com redação já iniciada"
    st = Path(parecer).stat()
    nascimento = datetime.fromtimestamp(min(st.st_ctime, st.st_mtime)).astimezone()
    if nascimento <= f6_inicio:
        return True, f"parecer criado antes do F6 ({nascimento.isoformat(timespec='seconds')})"
    return False, ("PARECER_POS_REDACAO: parecer nasceu após o início do F6 "
                   f"({nascimento.isoformat(timespec='seconds')} > {f6_inicio.isoformat(timespec='seconds')}) "
                   "— conselho deve opinar ANTES da redação (ordem do Igor 09/07)")


def visual_com_lastro(docx):
    """Lastro do visual (conselho 11/07/2026, achado D3): DOCX visual só vale com
    FIDELIDADE_VISUAL.json (gravado pelo gate do forja_visual) cujo docxSha256 bata com
    o arquivo real. Pega versão errada/desatualizada (Lição 48 — caso CASO-19).
    Composições anteriores ao gate são aceitas por evidência legada
    (RELATORIO_VISUAL_LAW.json ou resultado.json na mesma pasta).
    Retorna (ok: bool, motivo: str)."""
    import hashlib
    if docx is None:
        return False, "sem edição visual law"
    docx = Path(docx)
    fid_path = docx.with_name("FIDELIDADE_VISUAL.json")
    if fid_path.exists():
        fid = read_json(fid_path, {})
        sha = fid.get("docxSha256")
        if not sha:
            return False, "FIDELIDADE_VISUAL.json sem docxSha256 — re-rodar forja_visual"
        real = hashlib.sha256(docx.read_bytes()).hexdigest()
        if real != sha:
            return False, "DOCX visual NÃO bate com o lastro (versão errada ou alterada após o gate) — re-rodar forja_visual"
        return True, "lastro de fidelidade ok"
    # nomes legados encontrados nos casos reais pré-gate (CASO-19, Libra, CASO-02,
    # CASO-07, CASO-17) — composições novas sempre gravam FIDELIDADE_VISUAL.json
    for legado in ("RELATORIO_VISUAL_LAW.json", "RELATORIO_FINAL_VISUAL_LAW.json",
                   "resultado.json", "retorno.json", "visual_law_metadata.json"):
        if docx.with_name(legado).exists():
            return True, f"lastro legado ({legado}, composição pré-11/07/2026)"
    return False, "sem lastro de fidelidade (FIDELIDADE_VISUAL.json) — re-rodar forja_visual"


def f3_com_regimento(path):
    """Elo 2 com conteúdo (conselho 11/07/2026, achado C6 — lição CASO-16): o mapa de
    fontes deve CITAR o regimento interno do tribunal usado, não apenas existir.
    Retorna (ok: bool, motivo: str)."""
    path = Path(path)
    if not path.exists():
        return False, "F3_MAPA_FONTES_E_REGIMENTO.md não existe"
    texto = path.read_text(encoding="utf-8", errors="replace").upper()
    if "REGIMENTO" not in texto:
        return False, "F3 não cita o regimento interno do tribunal (REGIMENTO_INTERNO_<TRIBUNAL>.md) — protocolo da fábrica"
    return True, "regimento citado no mapa de fontes"


def main(case_key):
    matches = list((FORJA / "state").glob(f"case-*{case_key}*/FORJA_STATE.json"))
    if not matches:
        raise SystemExit(f"estado nao encontrado para {case_key}")
    state_path = matches[0]
    state = json.loads(state_path.read_text(encoding="utf-8-sig"))
    demanda_id = (state.get("inputs") or {}).get("demandId")
    pasta = Path((state.get("inputs") or {}).get("caseFolder") or "")

    demandas = read_json(DATA / "demandas.json", {"demandas": []})["demandas"]
    demanda = next((d for d in demandas if d.get("id") == demanda_id), {})
    entregas = read_json(DATA / "entregas_fabio_osorio.json", {})

    elos = []

    def elo(nome, caminho, obs="", allow_text=False):
        ok = ref_ok(caminho, allow_text=allow_text)
        elos.append({"elo": nome, "ok": bool(ok),
                     "ref": ref_text(caminho), "obs": obs})

    elo("1. Comando da demanda", achar(pasta, COMANDOS))
    f3_path = state_path.parent / "F3_MAPA_FONTES_E_REGIMENTO.md"
    f3_ok, f3_motivo = f3_com_regimento(f3_path)
    elos.append({"elo": "2. Mapa de fontes/regimento (F3)", "ok": f3_ok,
                 "ref": str(f3_path), "obs": f3_motivo})
    f5_path = state_path.parent / "F5_CHECKLIST_CITACOES.md"
    f5_ok, f5_reason = f5_checklist_ok(f5_path)
    elos.append({
        "elo": "3. Checklist de citações (F5)",
        "ok": f5_ok,
        "ref": str(f5_path),
        "obs": f5_reason,
    })
    elo("4. Minuta final", achar(pasta, ["*NIVEL2*.docx", "*FINAL*.docx", "*.docx"]))
    # 4-B. Edição visual law (ordem do Igor, 09/07/2026): toda entrega da esteira
    # sai em edição visual composta por forja_visual.py (kit padrao-visual-medina).
    visual = achar(state_path.parent / "producao" / "_visual", ["*VISUAL_LAW*.docx"]) \
        or achar(state_path.parent / "producao", ["*VISUAL_LAW*.docx"]) \
        or achar(pasta, ["*VISUAL_LAW*.docx"])
    v_ok, v_motivo = visual_com_lastro(visual)
    elos.append({"elo": "4-B. Edição visual law (padrão Medina Osório)",
                 "ok": bool(visual) and v_ok, "ref": ref_text(visual),
                 "obs": v_motivo + "; composta via forja_visual.compor + mapa declarativo"})
    elo("5. Auditoria do caso", achar(pasta, ["*APRENDIZADOS*.md", "*AUDITORIA*.md", "CHECKLIST_FONTES*.md"]))
    elo("6. QA visual estrutural (piloto M4)", state_path.parent / "piloto" / "F8_QA_ESTRUTURAL.json",
        "OOXML, fidelidade, tipografia, metadados e SVG auditados sem renderização")

    # entrega arquivada
    entrega_hit = None
    ids = set(demanda.get("emailsRecebidos") or []) | set(demanda.get("threadIds") or [])
    for d in entregas.get("deliveries", []):
        if (d.get("messageId") in ids) or (d.get("threadId") in ids) or (
                demanda.get("clienteOuCaso", "zzz").split()[0].lower() in (d.get("subject") or "").lower()):
            entrega_hit = d
            break
    entrega_ref = None
    entrega_obs = ""
    if entrega_hit:
        saved = [Path(p) for p in (entrega_hit.get("savedFiles") or [])]
        entrega_ref = saved if saved else Path(entrega_hit.get("folder") or "")
        entrega_obs = f"e-mail enviado ao escritório com anexo; subject: {entrega_hit.get('subject', '')}"
    elo("7. Entrega arquivada", entrega_ref, entrega_obs)

    evid = (demanda.get("evidenciaResposta") or "").strip()
    elo("8. Evidência de cumprimento", evid[:160] if evid else None,
        "campo evidenciaResposta da demanda", allow_text=True)

    # 9. Gate bloqueante do verificador (F7 -> F10): peça só fecha com p0 == 0.
    # O F7_VERIFICADOR_FORJA.json é gravado pela entrada canônica da FORJA.
    f7_path = None
    f7 = {}
    for cand in [state_path.parent / "producao" / "F7_VERIFICADOR_FORJA.json",
                 state_path.parent / "piloto" / "F7_VERIFICADOR_FORJA.json"]:
        if cand.exists():
            f7_path = cand
            break
    if f7_path:
        f7 = read_json(f7_path, {})
        f7_ok, lastro_motivo = f7_com_lastro(f7)
        f7_obs = (f"p0={f7.get('p0')}, p1={f7.get('p1')} | lastro: {lastro_motivo} "
                  f"({f7.get('geradoEm', '?')})")
    else:
        f7_ok = False
        f7_obs = "F7_VERIFICADOR_FORJA.json não encontrado — reexecutar a entrada canônica da FORJA (sem renderização)"
    elos.append({"elo": "9. Verificador FORJA (F7, p0 == 0 + lastro do fonte)", "ok": f7_ok,
                 "ref": str(f7_path) if f7_path else "NAO LOCALIZADO", "obs": f7_obs})

    # 9-B. Lastro verbatim do ledger de fatos (FORJA-LASTRO-v2, 26/07/2026).
    # Âncora: no caso CASO-23, o fato F012 estava marcado `confirmed_document`
    # com localizador plausível e afirmava o OPOSTO do documento que citava. Passou
    # pelo red team interno, pelo gate F7 e por dois revisores externos de famílias
    # distintas — porque nenhum abriu a página. Citar o localizador não é ter lido o
    # localizador; a prova barata de leitura é a transcrição colada.
    ledger_path = None
    for cand in [state_path.parent / "n3_artifacts" / "F3_FONTES_REGIMENTO_LEIS" / "fact_ledger.json",
                 state_path.parent / "F3_FACT_LEDGER.json"]:
        if cand.exists():
            ledger_path = cand
            break
    if ledger_path:
        from forja_lastro import fatos_sem_lastro, material_economico, validar_gates_economicos
        ledger = read_json(ledger_path, {})
        pendentes = fatos_sem_lastro(ledger)
        lastro_ok = not pendentes
        lastro_obs = ("todos os fatos confirmados têm transcrição verbatim" if lastro_ok else
                      f"{len(pendentes)} fato(s) afirmam lastro documental sem transcrição: "
                      f"{', '.join(pendentes[:8])}{'...' if len(pendentes) > 8 else ''}")
        # Elo 9-B também é a última barreira de produção para a fonte
        # prevalente. O cálculo é refeito contra o ledger e a pasta do caso;
        # nenhum campo de F7 escrito pelo agente é aceito como prova.
        f7_text_path = None
        try:
            f7_text_path = Path(str((f7 or {}).get("arquivo") or ""))
        except (TypeError, ValueError):
            f7_text_path = None
        if not f7_text_path or not f7_text_path.is_file():
            possiveis = sorted((state_path.parent / "producao").glob("final*.md"))
            f7_text_path = possiveis[0] if possiveis else None
        if f7_text_path and f7_text_path.is_file():
            texto_f7 = f7_text_path.read_text(encoding="utf-8", errors="replace")
            if material_economico(texto_f7):
                base_dir = None
                try:
                    estado = read_json(state_path.parent / "FORJA_STATE.json", {})
                    base_dir = (estado.get("inputs") or {}).get("caseFolder")
                except (OSError, TypeError):
                    base_dir = None
                achados_economicos = validar_gates_economicos(
                    texto_f7, ledger=ledger, base_dir=base_dir
                )
                if achados_economicos:
                    lastro_ok = False
                    lastro_obs += "; " + "; ".join(
                        f"{a['gate']}: {a['problema']}" for a in achados_economicos[:6]
                    )
    else:
        # Ausência de ledger não inventa aprovação: casos N2 antigos não têm o
        # artefato, e o elo registra isso em vez de passar em silêncio.
        lastro_ok = False
        lastro_obs = "fact_ledger.json não localizado — caso sem ledger de fatos não fecha entrega"
    elos.append({"elo": "9-B. Lastro verbatim do ledger de fatos (FORJA-LASTRO-v2)",
                 "ok": lastro_ok, "ref": str(ledger_path) if ledger_path else "NAO LOCALIZADO",
                 "obs": lastro_obs})

    # 10. Gate bloqueante do conselho (ordem do Igor, 09/07/2026): TODA peça exige
    # parecer escrito de Helena (estratégia) e de Cícero (jurídico), com recomendações
    # e decisão registrada (acatado/rejeitado/por quê). Arquivos canônicos na pasta do
    # caso em state/: F4_PARECER_HELENA.md e F4_PARECER_CICERO.md (aceita variações).
    for persona in ("HELENA", "CICERO"):
        parecer = achar(state_path.parent, [f"F4_PARECER_{persona}*.md", f"*PARECER*{persona}*.md"]) \
            or achar(state_path.parent / "producao", [f"*PARECER*{persona}*.md"])
        # régua anti-fraude: existência de arquivo não basta — conteúdo é validado
        p_ok, p_motivo = parecer_valido(parecer)
        # M2.1: além do conteúdo, a ORDEM — parecer antes do início da redação
        ordem_ok, ordem_motivo = parecer_antes_da_redacao(parecer, state)
        elos.append({"elo": f"10. Parecer {persona.title()} (conselho obrigatório)",
                     "ok": p_ok and ordem_ok, "ref": ref_text(parecer),
                     "obs": p_motivo + "; " + ordem_motivo + " (skill /" + persona.lower() + ")"})

    command = achar(pasta, COMANDOS)
    command_text = command.read_text(encoding="utf-8", errors="replace") if command else ""
    product_text = " ".join([
        str(demanda.get("titulo") or ""),
        str(demanda.get("resumo") or ""),
        str(demanda.get("proximaAcao") or ""),
        command_text[:12000],
    ])
    adversarial_required = bool(demanda.get("adversarialAuditRequired")) or response_product_required(product_text)
    adversarial_path = achar(state_path.parent, ["F3_AUDITORIA_PECA_ADVERSARIA.json"])
    if adversarial_path is None:
        adversarial_path = achar(
            state_path.parent / "n3_artifacts" / "F3_FONTES_REGIMENTO_LEIS",
            ["adversarial_audit*.json"],
        )
    if adversarial_required or adversarial_path is not None:
        result = validate_adversarial_audit(read_json(adversarial_path, {}) if adversarial_path else {})
        elos.append({
            "elo": "11. Auditoria da peça adversária (citações, contradições e pontos decisivos)",
            "ok": bool(result.get("approved")),
            "ref": ref_text(adversarial_path),
            "obs": "; ".join(result.get("p0") or []) or "ledger adversarial aprovado",
        })

    # O fechamento legado não pode mais contornar o pacote canônico N3/v2.
    package_pointer = state_path.parent / "FORJA_PACKAGE.json"
    if package_pointer.is_file():
        try:
            from forja_package import revalidate_package_manifest

            package_result = revalidate_package_manifest(
                state_path.parent,
                read_json(package_pointer, {}),
            )
            package_ok = package_result["approved"]
            package_reason = (
                "pacote canônico revalidado na política atual"
                if package_ok
                else "; ".join(package_result["findings"][:8])
            )
        except Exception as exc:
            package_ok = False
            package_reason = f"revalidação do pacote falhou: {exc}"
    else:
        package_ok = False
        package_reason = "pacote canônico FORJA_PACKAGE.json ausente"
    elos.append({
        "elo": "12. Pacote canônico N3/v2 revalidado",
        "ok": package_ok,
        "ref": str(package_pointer),
        "obs": package_reason,
    })

    # Memória obrigatória: ela acompanha a minuta e registra fases, hashes,
    # gates, decisões e limites sem copiar autos ou segredos. A geração é
    # estática e não usa Word, PDF, PNG ou renderizador.
    pacote = state_path.parent / "pacote_revisao"
    pacote.mkdir(exist_ok=True)
    memory = build_bundle(state_path.parent, pacote)
    memory_check = validate_bundle(Path(memory["manifest"]), expected_case_dir=state_path.parent)
    elos.append({
        "elo": "13. Memória obrigatória de auditabilidade (Markdown + HTML + manifesto)",
        "ok": bool(memory.get("approved") and memory_check.get("approved")),
        "ref": "; ".join(memory[key] for key in ("markdown", "html", "manifest")),
        "obs": "processo, métodos, hashes, gates e limites; sem renderização e sem conteúdo bruto",
    })

    aprovado = all(e["ok"] for e in elos)
    status_final = "cumprida com evidência (trilha completa)" if aprovado else "TRILHA INCOMPLETA - nao pode ser cumprida"
    # Conselho 11/07/2026 (achado D7): reprovação precisa deixar rastro legível por
    # máquina, não só texto no .md — o painel e os agentes leem daqui.
    bloqueadores = [e["elo"] + (" — " + e["obs"] if e.get("obs") else "") for e in elos if not e["ok"]]

    # pacote de revisão (cópias)
    origens = [state_path.parent / "piloto" / "PILOTO_M4_TEMPLATE.docx",
               state_path.parent / "F5_CHECKLIST_CITACOES.md",
               state_path.parent / "F3_MAPA_FONTES_E_REGIMENTO.md",
               state_path.parent / "F3_AUDITORIA_PECA_ADVERSARIA.json",
               Path(memory["markdown"]), Path(memory["html"]), Path(memory["manifest"])]
    # PDF do piloto é compatibilidade histórica. Nunca o copia para o pacote
    # quando a produção canônica registra VISUAL_BUILD.json em SVG/OOXML.
    if not (state_path.parent / "producao" / "VISUAL_BUILD.json").is_file():
        origens.insert(1, state_path.parent / "piloto" / "PILOTO_M4_TEMPLATE.pdf")
    for origem in origens:
        if origem.exists():
            shutil.copy2(origem, pacote / origem.name)

    linhas = [
        "# F10 — Trilha de evidência da demanda piloto (M5)",
        "",
        f"Demanda: `{demanda_id}` | Status no painel: `{demanda.get('status')}` | Gerado: {now_iso()}",
        "",
        "| Elo | OK | Referência |",
        "|---|---|---|",
    ]
    for e in elos:
        marca = "SIM" if e["ok"] else "**FALHOU**"
        ref = e["ref"] + (" — " + e["obs"] if e["obs"] else "")
        linhas.append(f"| {e['elo']} | {marca} | {ref} |")
    linhas += ["", f"## Veredito: {status_final}", "",
               f"Pacote de revisão montado em: `pacote_revisao/` ({len(list(pacote.iterdir()))} arquivos)"]
    out = state_path.parent / "F10_TRILHA_EVIDENCIA.md"
    out.write_text("\n".join(linhas) + "\n", encoding="utf-8")

    state["updatedAt"] = now_iso()
    state["currentPhase"] = "F10_ENTREGA_EVIDENCIA_APRENDIZADO"
    state["status"] = "fulfilled" if aprovado else state.get("status")
    state["trilhaBloqueadores"] = bloqueadores
    state.setdefault("phaseHistory", []).append(
        {"phase": "F10_ENTREGA_EVIDENCIA_APRENDIZADO", "at": now_iso(),
         "status": "ok" if aprovado else "reprovado"})
    state["deliveryEvidence"] = {"status": "manual_override" if evid else "none",
                                 "path": str(out), "confirmedAt": now_iso() if aprovado else None}
    state["artifacts"] = append_unique(state.get("artifacts") or [], str(out))
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

    # O estado mudou ao registrar F10. Regera a memória uma última vez para
    # que o hash do estado de origem corresponda exatamente ao estado entregue.
    memory = build_bundle(state_path.parent, pacote)
    memory_check = validate_bundle(Path(memory["manifest"]), expected_case_dir=state_path.parent)
    if not (memory.get("approved") and memory_check.get("approved")):
        aprovado = False
        status_final = "TRILHA INCOMPLETA - memoria de auditabilidade inválida"
        bloqueadores.append("13. Memória obrigatória de auditabilidade — manifesto ou hash do estado inválido")
        state["status"] = state.get("status")
        state["trilhaBloqueadores"] = bloqueadores
        state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

    if not aprovado:
        # M1.1 (plano 19): P0 no fechamento notifica o painel na hora, com
        # deduplicação de 6h — fail-open, nunca quebra a trilha.
        try:
            from forja_alertas import notificar_p0
            for b in bloqueadores:
                gate_curto = b.split(".", 1)[0].strip() or "F10"
                notificar_p0(state_path.parent, gate=f"F10-elo-{gate_curto}",
                             motivo=b, origem="forja_delivery",
                             demand_id=demanda_id)
        except Exception:
            pass

    print(json.dumps({"aprovado": aprovado, "veredito": status_final,
                      "bloqueadores": bloqueadores,
                      "auditMemory": memory,
                      "elos": [{k: e[k] for k in ("elo", "ok")} for e in elos],
                      "trilha": str(out)}, ensure_ascii=False, indent=2))
    if not aprovado:
        # trilha incompleta sai com código 2: automação que encadeia a entrega
        # falha alto em vez de seguir em silêncio (conselho 11/07/2026)
        raise SystemExit(2)


if __name__ == "__main__":
    main(sys.argv[1])
