"""Contrato neutro do gate visual F8.

Não depende do empacotamento nem da validação N4. Ambos os fluxos podem assim
reproduzir o mesmo gate fail-closed sem formar um ciclo de imports.
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

FERRAMENTAS = Path(__file__).resolve().parent.parent / "_FERRAMENTAS"

from forja_docx_layout import audit_docx_layout
from forja_human_review import validate_visual_review_receipt
from forja_n3_common import ForjaN3Error, read_json, sha256_file
from forja_visual_review import REQUIRED_PAGE_CHECKS, validate_visual_review
from forja_fidelity import compare_docx_fidelity


def inspect_pdf(*args, **kwargs):
    """Fachada tardia de compatibilidade; só carrega o renderizador no legado."""
    from forja_visual_qa import inspect_pdf as _inspect_pdf

    return _inspect_pdf(*args, **kwargs)


def _validate_static_f8(artifact: dict, *, files: dict, release_policy: str) -> dict:
    """Valida a rota canônica OOXML/SVG sem criar páginas rasterizadas."""
    ledger = read_json(Path(artifact["path"]), None)
    if not isinstance(ledger, dict):
        raise ForjaN3Error(f"laudo F8 estático inválido: {artifact['path']}")
    findings: list[str] = []
    # Recomputados abaixo; ficam em None quando o insumo falta, e o gate
    # correspondente reprova por isso — nunca por omissão silenciosa.
    layout: dict | None = None
    fidelity: dict | None = None
    docx = files.get("docx") or {}
    markdown = files.get("md") or files.get("markdown") or {}
    docx_path = Path(str(docx.get("path") or ""))
    markdown_path = Path(str(markdown.get("path") or ""))
    if ledger.get("mode") != "static_ooxml_svg":
        findings.append("laudo F8 não identifica a rota static_ooxml_svg")
    for key in ("renderingUsed", "pdfCreated", "pngCreated"):
        if ledger.get(key) is not False:
            findings.append(f"laudo F8 declara {key} diferente de false")
    if ledger.get("approved") is not True:
        findings.append("laudo F8 estático não aprovado")
    if not docx_path.is_file():
        findings.append("DOCX ausente para recomputar a diagramação estática")
    else:
        expected_docx = ((ledger.get("docx") or {}).get("sha256") or docx.get("sha256"))
        if expected_docx and sha256_file(docx_path) != expected_docx:
            findings.append("hash do DOCX diverge do laudo F8 estático")
        try:
            layout = audit_docx_layout(docx_path)
            if not layout.get("approved"):
                findings.append("diagramação OOXML reprovada na recomputação estática")
        except Exception as exc:
            findings.append(f"não foi possível recomputar a diagramação OOXML: {exc}")
    for key in ("package", "docxLint", "layoutAudit", "fidelity"):
        section = ledger.get(key)
        if not isinstance(section, dict):
            findings.append(f"laudo F8 sem seção {key}")
        elif section.get("approved") is not True:
            findings.append(f"seção F8 reprovada: {key}")
    svg = ledger.get("svg")
    if not isinstance(svg, list):
        findings.append("laudo F8 sem inventário SVG")
    elif any(item.get("approved") is not True for item in svg if isinstance(item, dict)):
        findings.append("um ou mais SVGs reprovaram no lint estático")
    if markdown_path.is_file() and docx_path.is_file():
        try:
            fidelity = compare_docx_fidelity(markdown_path, docx_path)
            if not fidelity.get("approved"):
                findings.append("fidelidade Markdown→OOXML reprovada na recomputação")
        except Exception as exc:
            findings.append(f"não foi possível recomputar fidelidade OOXML: {exc}")
    if release_policy == "strict_protocol":
        attestation = files.get("visual_review_attestation") or {}
        attestation_path = Path(str(attestation.get("path") or ""))
        if not attestation_path.is_file():
            findings.append("revisão visual humana estrita ausente (atestado não rasterizado)")
        else:
            receipt = read_json(attestation_path, None)
            if not isinstance(receipt, dict) or receipt.get("approved") is not True:
                findings.append("atestado visual humano estrito não aprovado")
            if str(receipt.get("reviewMethod") or "").casefold() in {"automatic", "automated", "self"}:
                findings.append("atestado visual não pode ser autocertificação automática")
    return {
        "approved": not findings,
        "findings": findings,
        "mode": "static_ooxml_svg",
        "renderingUsed": False,
        "pdfRerendered": False,
        "gates": _gates_do_contrato(ledger, layout, fidelity, findings,
                                   release_policy=release_policy),
    }


# Cada chave é um gate exigido por `phase_contracts/F8.json`; cada valor é a
# evidência que ESTE validador já computava e não nomeava. Antes disto os 14
# gates existiam só no JSON do contrato: nenhum produtor no harness sabia
# emiti-los, `_validate_result` os cobrava e a fase não fechava — medido em
# 04/08/2026 por `forja_gate_liveness.py`. O F8 rodou 2 vezes na história,
# ambas antes de o contrato ser apertado, relatando 6 gates onde hoje se
# exigem 16. Nenhum limiar novo foi criado aqui: só o nome do que já era medido.
def _svg_lint(svg) -> str:
    """Roda o gate de desenho sobre os SVGs do ledger, em vez de acreditar nele.

    `medina_svg_colisao` já é a autoridade da casa sobre desenho quebrado —
    calibrado contra os 228 SVGs do acervo, com o limiar de contraste em 2,0:1
    porque a paleta terracota sobre terra do escritório dá 2,3:1 e a norma WCAG
    reprovaria a identidade aprovada. Aqui ele é reexecutado a partir do
    arquivo; o campo `approved` do ledger não decide nada.

    Sem SVG algum o veredito é `not_applicable`: não há desenho a conferir, e
    dizer `pass` seria medir o conjunto vazio.
    """
    entradas = [item for item in (svg or []) if isinstance(item, dict)]
    if not entradas:
        return "not_applicable"

    try:
        sys.path.insert(0, str(FERRAMENTAS))
        from medina_svg_colisao import analisar  # type: ignore
    except Exception:  # noqa: BLE001  -- ferramenta ausente não vira aprovação
        return "fail"

    conferidos = 0
    localizaveis = 0
    for item in entradas:
        caminho = item.get("path") or item.get("source") or item.get("file")
        if not caminho:
            continue
        localizaveis += 1
        alvo = Path(str(caminho))
        if not alvo.is_file():
            return "fail"
        try:
            laudo = analisar(svg_path=str(alvo))
        except Exception:  # noqa: BLE001
            return "fail"
        achados = laudo.get("findings") if isinstance(laudo, dict) else None
        if any(str(a.get("sev") or a.get("severidade") or "").upper().startswith("P0")
               for a in (achados or []) if isinstance(a, dict)):
            return "fail"
        conferidos += 1

    # Ledger que lista SVG sem dizer ONDE ele está não permite reexecutar o
    # gate de desenho. Isso não é reprovação — é impossibilidade, e chamá-la de
    # `fail` transformaria o gate em trava por detalhe de esquema, que é
    # exatamente o que o teste-âncora existe para impedir. Também não é `pass`.
    if not localizaveis:
        return "not_applicable"
    return "pass" if conferidos == localizaveis else "fail"


def _markdown_lint(ledger: dict) -> str:
    """Confere o lint do markdown de origem declarado no ledger.

    Não há linter de markdown próprio no harness, e inventar um aqui seria
    ampliar escopo. O que este gate garante é o mínimo honesto: se o ledger
    afirma que o lint passou, a afirmação precisa vir com o arquivo conferido e
    um resultado; afirmação nua vira `fail`, porque o gate existe justamente
    para não aceitar declaração.
    """
    lint = ledger.get("markdownLint") or ledger.get("markdown_lint")
    if lint is None:
        return "not_applicable"
    if lint is True:
        return "fail"
    if isinstance(lint, dict):
        aprovado = lint.get("approved") is True or str(lint.get("status") or "").lower() == "pass"
        tem_alvo = bool(lint.get("path") or lint.get("file") or lint.get("source"))
        return "pass" if (aprovado and tem_alvo) else "fail"
    return "fail"


def _gates_do_contrato(ledger: dict, layout: dict | None, fidelity: dict | None,
                       findings: list[str], *, release_policy: str) -> dict:
    def veredito(condicao: bool) -> str:
        return "pass" if condicao else "fail"

    codigos = {str(item.get("code") or "") for item in ((layout or {}).get("findings") or [])
               if isinstance(item, dict)}
    metricas = (layout or {}).get("metrics") or {}
    svg = ledger.get("svg")
    receipt = ledger.get("visualReviewReceipt") or {}
    metodo = str(receipt.get("reviewMethod") or "").casefold()
    estrito = release_policy == "strict_protocol"

    return {
        # Os dois gates de lint estavam no contrato do F8 desde sempre e nenhum
        # produtor do harness os emitia: as únicas três ocorrências no acervo
        # vêm de um `build_f8_v8.py` descartável dentro da pasta de um caso, com
        # a string "pass" escrita à mão. Achado em 04/08/2026 chamando o
        # produtor em vez de procurar o nome por grep — que é o que o medidor de
        # liveness faz, e por isso os dois não apareciam como dívida.
        "svg_lint_pass": _svg_lint(svg),
        "markdown_lint_pass": _markdown_lint(ledger),
        # Rota: nenhum PDF ou raster foi produzido.
        "no_pdf_or_raster_rendering": veredito(
            ledger.get("renderingUsed") is False
            and ledger.get("pdfCreated") is False
            and ledger.get("pngCreated") is False),
        # A QA estática rodou e aprovou.
        "static_ooxml_qa_pass": veredito(
            ledger.get("mode") == "static_ooxml_svg" and not findings),
        # O laudo não foi aceito por declaração: a diagramação foi recomputada
        # a partir do DOCX nesta execução.
        "static_qa_recomputed": veredito(layout is not None),
        "semantic_fidelity_recomputed": veredito(
            fidelity is not None and bool(fidelity.get("approved"))),
        "docx_content_and_tracking_fidelity_pass": veredito(
            fidelity is not None and bool(fidelity.get("approved"))),
        # Corpo em Times 12 justificado: cobertura integral nas três métricas.
        "docx_body_justified_times_12_pass": veredito(
            bool(metricas)
            and metricas.get("justificationCoverage") == 1.0
            and metricas.get("fontCoverage") == 1.0
            and metricas.get("sizeCoverage") == 1.0),
        "docx_folio_collision_safe": veredito(
            layout is not None and not any(c.startswith("folio_") for c in codigos)),
        "docx_table_typography_consistent_min_8pt": veredito(
            layout is not None and not any(c.startswith("table_typography") for c in codigos)),
        "svg_embeds_integrity_pass": veredito(
            isinstance(svg, list)
            and all(item.get("approved") is True for item in svg if isinstance(item, dict))),
        # Cobertura de revisão: todas as páginas do documento examinadas.
        "document_scope_reviewed_at_100_percent": veredito(
            bool(receipt.get("pages"))
            and receipt.get("pagesReviewed") == receipt.get("pageCount")),
        "independent_human_or_visual_agent_reviewer": veredito(
            str(receipt.get("reviewType") or "").casefold() in {"human", "agent_visual"}
            and bool(receipt.get("reviewer"))),
        "no_automated_self_certification": veredito(
            metodo not in {"automatic", "automated", "self"}),
        # Os dois gates estritos só se aplicam à liberação estrita. Fora dela
        # não são "pass" por conveniência: são `not_applicable`, para que a
        # medição de liveness não os conte como aprovados sem terem ocorrido.
        "human_visual_review_signed_receipt_for_strict_release": (
            veredito(receipt.get("approved") is True and bool(receipt.get("signedAt")))
            if estrito else "not_applicable"),
        "external_human_trust_store_verified_for_strict_release": (
            veredito(bool(ledger.get("externalTrustStoreVerified")))
            if estrito else "not_applicable"),
    }


def _validate_legacy_f8(artifact: dict, *, files: dict, release_policy: str = "internal_review") -> dict:
    """Reexecuta e valida o ledger F8 contra DOCX, PDF e atestados reais."""
    ledger = read_json(Path(artifact["path"]), None)
    if not isinstance(ledger, dict):
        raise ForjaN3Error(f"ledger F8 inválido: {artifact['path']}")
    findings = []
    pdf = files.get("pdf") or {}
    docx = files.get("docx") or {}
    pdf_path = Path(str(pdf.get("path") or ""))
    docx_path = Path(str(docx.get("path") or ""))
    if ledger.get("schemaVersion") != 2:
        findings.append("ledger F8 anterior ao gate visual anti-autocertificação v2")
    if ledger.get("pdfSha256") != pdf.get("sha256"):
        findings.append("hash do PDF não corresponde ao ledger")
    pages = ledger.get("pages") or []
    if ledger.get("pageCount") != len(pages) or not pages:
        findings.append("ledger não cobre todas as páginas")
    generator_run = ledger.get("generatorRunId")
    reviewer_run = ledger.get("reviewerRunId")
    if not generator_run or not reviewer_run:
        findings.append("ledger não identifica gerador e revisor")
    elif generator_run == reviewer_run:
        findings.append("ledger foi autoaprovado pelo gerador")
    page_numbers = [page.get("page") for page in pages]
    if page_numbers != list(range(1, len(pages) + 1)):
        findings.append("ledger possui páginas ausentes, duplicadas ou fora de ordem")
    for page in pages:
        number = page.get("page")
        if page.get("lint") != "pass":
            findings.append(f"página {number} sem lint aprovado")
        review = page.get("independentReview") or {}
        if review.get("status") != "pass":
            findings.append(f"página {number} sem revisão independente")
        if not reviewer_run or review.get("runId") != reviewer_run:
            findings.append(f"página {number} revisada por execução diferente do ledger")
        if generator_run and review.get("runId") == generator_run:
            findings.append(f"página {number} autoaprovada pelo gerador")
        if not page.get("imageSha256"):
            findings.append(f"página {number} sem hash de imagem")
        if review.get("reviewType") not in {"human", "agent_visual"}:
            findings.append(f"página {number} foi autocertificada por revisão automática")
        checks = review.get("checks") or {}
        if not checks or any(value is not True for value in checks.values()):
            findings.append(f"página {number} sem checklist visual integral")

    layout_result = None
    if not docx_path.is_file():
        findings.append("DOCX ausente para recomputar a diagramação")
    else:
        try:
            layout_result = audit_docx_layout(docx_path)
            if not layout_result["approved"]:
                codes = ", ".join(item["code"] for item in layout_result["findings"][:8])
                findings.append(f"diagramação Word reprovada na recomputação: {codes}")
            stored_layout = ledger.get("layoutAudit") or {}
            if ((stored_layout.get("docx") or {}).get("sha256")) != docx.get("sha256"):
                findings.append("ledger visual não está vinculado ao DOCX do pacote")
        except Exception as exc:
            findings.append(f"não foi possível recomputar a diagramação Word: {exc}")

    rerendered = None
    if pdf_path.is_file() and generator_run and reviewer_run and generator_run != reviewer_run:
        try:
            dpi = int(ledger.get("renderDpi") or 120)
            if dpi < 110 or dpi > 300:
                findings.append("DPI de revisão visual fora da faixa permitida")
            else:
                with tempfile.TemporaryDirectory(prefix="forja-f8-rerender-") as temp:
                    rerendered = inspect_pdf(
                        pdf_path,
                        Path(temp),
                        generator_run_id=str(generator_run),
                        reviewer_run_id=str(reviewer_run),
                        dpi=dpi,
                    )
                    if not rerendered["approved"]:
                        findings.append("lint visual automático falhou na recomputação")
                    rerender_hashes = [page.get("imageSha256") for page in rerendered["pages"]]
                    ledger_hashes = [page.get("imageSha256") for page in pages]
                    if rerender_hashes != ledger_hashes:
                        findings.append("imagens revisadas não correspondem ao rerender do PDF")

                    manual = ledger.get("manualVisualReview") or {}
                    review_path = Path(str(manual.get("reviewPath") or ""))
                    if not review_path.is_file() or manual.get("reviewSha256") != sha256_file(review_path):
                        findings.append("atestado visual independente ausente ou adulterado")
                    else:
                        verified_review = validate_visual_review(
                            review_path,
                            pdf=pdf_path,
                            docx=docx_path if docx_path.is_file() else None,
                            rendered_pages=rerendered["pages"],
                            generator_run_id=str(generator_run),
                            expected_reviewer_run_id=str(reviewer_run),
                        )
                        if not verified_review["approved"]:
                            codes = ", ".join(item["code"] for item in verified_review["findings"][:8])
                            findings.append(f"atestado visual independente reprovado: {codes}")
                        if release_policy == "strict_protocol":
                            signed = ledger.get("humanVisualReceipt") or {}
                            receipt_path = Path(str(signed.get("receiptPath") or ""))
                            if not receipt_path.is_file():
                                findings.append("revisão visual estrita sem recibo humano assinado")
                            elif signed.get("receiptSha256") != sha256_file(receipt_path):
                                findings.append("hash do recibo humano visual diverge")
                            else:
                                receipt = validate_visual_review_receipt(
                                    receipt_path,
                                    expected={
                                        "generatorRunId": str(generator_run),
                                        "reviewerRunId": str(reviewer_run),
                                        "pdfSha256": sha256_file(pdf_path),
                                        "docxSha256": sha256_file(docx_path),
                                        "pageCount": len(rerendered["pages"]),
                                        "pageImageSha256": rerender_hashes,
                                        "requiredChecks": list(REQUIRED_PAGE_CHECKS),
                                        "visualAttestationSha256": sha256_file(review_path),
                                    },
                                )
                                if not receipt["approved"]:
                                    findings.append(
                                        "recibo humano visual reprovado: "
                                        + ", ".join(receipt["findings"])
                                    )
        except Exception as exc:
            findings.append(f"não foi possível rerenderizar o PDF: {exc}")
    else:
        findings.append("PDF ou identidade dos runs insuficiente para rerender independente")
    if ledger.get("approved") is not True:
        findings.append("ledger F8 não aprovado")
    return {
        "approved": not findings,
        "findings": findings,
        "pageCount": len(pages),
        "layoutRecomputed": layout_result,
        "pdfRerendered": bool(rerendered),
    }


def validate_f8(artifact: dict, *, files: dict, release_policy: str = "internal_review") -> dict:
    """Despacha F8 estático; mantém o validador PDF apenas para artefatos legados."""
    ledger = read_json(Path(artifact["path"]), None)
    if isinstance(ledger, dict) and (
        ledger.get("mode") == "static_ooxml_svg"
        or not (files.get("pdf") or {}).get("path")
    ):
        return _validate_static_f8(artifact, files=files, release_policy=release_policy)
    return _validate_legacy_f8(artifact, files=files, release_policy=release_policy)
