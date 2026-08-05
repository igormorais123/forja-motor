"""Canonical F9/F10 closeout for hash-bound FORJA N3 packages."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from forja_n3_common import ForjaN3Error, atomic_write_json, canonical_hash, read_json, resolve_case_dir, sha256_file
from forja_f10_contract import compute_f10_gates, validate_f10_gates
from forja_package import build_package, revalidate_package_manifest
from forja_state_machine import derive_state, record_event


def _canonical_manifest(case_dir: Path, expected_revision: int) -> tuple[dict, dict]:
    state = derive_state(case_dir)
    if state["revision"] != expected_revision:
        raise ForjaN3Error(f"revisão mudou: {state['revision']}")
    package = state.get("package") or {}
    pointer = read_json(case_dir / "FORJA_PACKAGE.json", None)
    immutable_path = Path(str(package.get("path") or ""))
    immutable = read_json(immutable_path, None) if immutable_path.is_file() else None
    if not isinstance(pointer, dict) or not isinstance(immutable, dict):
        raise ForjaN3Error("pacote canônico ausente ou ilegível")
    for field in ("packageId", "packageHash"):
        if pointer.get(field) != package.get(field) or immutable.get(field) != package.get(field):
            raise ForjaN3Error(f"{field} diverge do evento canônico")
    if canonical_hash(pointer) != canonical_hash(immutable):
        raise ForjaN3Error("ponteiro do pacote diverge do manifesto imutável")
    revalidation = revalidate_package_manifest(case_dir, immutable)
    if not revalidation["approved"]:
        prefix = (
            "artefato diverge do pacote canônico: "
            if any("hash divergente" in item for item in revalidation["findings"])
            else "pacote obsoleto ou reprovado na política atual: "
        )
        raise ForjaN3Error(
            prefix + "; ".join(revalidation["findings"][:12])
        )
    return pointer, state


def create_package(case_dir: Path, definition: Path, *, expected_revision: int) -> dict:
    state = derive_state(case_dir)
    if state["revision"] != expected_revision:
        raise ForjaN3Error(f"revisão mudou: {state['revision']}")
    if state.get("phaseCursor") != "F9_PACOTE_REVISAO_DRAFT_OPCIONAL":
        raise ForjaN3Error("pacote só pode ser fechado com F9 em execução")
    manifest = build_package(case_dir, definition, publish_pointer=False)
    immutable_manifest = case_dir / "packages" / manifest["packageId"] / "FORJA_PACKAGE.json"
    _, state, _ = record_event(
        case_dir,
        "package_created",
        expected_revision=expected_revision,
        idempotency_key=f"{case_dir.name}:{manifest['packageId']}:created",
        phase=state.get("phaseCursor"),
        run_id=manifest.get("runId"),
        artifact_hashes={"package": manifest["packageHash"]},
        payload={
            "packageId": manifest["packageId"],
            "packageHash": manifest["packageHash"],
            "path": str(immutable_manifest),
            "attachments": [{"artifactId": item["artifactId"], "sha256": item["sha256"]} for item in manifest["attachments"]],
        },
    )
    atomic_write_json(case_dir / "FORJA_PACKAGE.json", manifest)
    _, state, _ = record_event(
        case_dir,
        "phase_completed",
        expected_revision=state["revision"],
        idempotency_key=f"{case_dir.name}:{manifest['packageId']}:f9-completed",
        phase="F9_PACOTE_REVISAO_DRAFT_OPCIONAL",
        run_id=manifest.get("runId"),
        artifact_hashes={"package": manifest["packageHash"]},
        payload={"result": "pass", "lifecycleStatus": "ready_for_review"},
    )
    return {"manifest": manifest, "state": state}


def register_draft(case_dir: Path, receipt_path: Path, *, expected_revision: int) -> dict:
    manifest, state = _canonical_manifest(case_dir, expected_revision)
    email = manifest.get("email") or {}
    email_path = Path(str(email.get("path") or ""))
    if not email_path.is_file() or sha256_file(email_path) != email.get("sha256"):
        raise ForjaN3Error("corpo do e-mail diverge do pacote canônico")
    from forja_estilo_humano import analisar as analisar_estilo_humano
    email_p0 = [
        item for item in analisar_estilo_humano(
            email_path.read_text(encoding="utf-8", errors="replace"), "email"
        )
        if item["sev"] == "P0"
    ]
    if email_p0:
        detalhes = "; ".join(f"{item['gate']}: {item['problema']}" for item in email_p0[:6])
        raise ForjaN3Error("corpo do e-mail reprovado pelo gate de escrita humana: " + detalhes)
    receipt = read_json(receipt_path, None)
    if not isinstance(receipt, dict):
        raise ForjaN3Error("recibo de draft inválido")
    if not receipt.get("draftId") or not receipt.get("threadId"):
        raise ForjaN3Error("recibo sem draftId/threadId")
    if receipt.get("bodySha256") != email.get("sha256"):
        raise ForjaN3Error("hash do corpo do rascunho diverge do e-mail aprovado")
    expected = sorted(
        (str(item["artifactId"]), item["sha256"], int(item["size"]))
        for item in manifest.get("attachments") or []
    )
    actual = sorted(
        (str(item.get("artifactId") or ""), str(item.get("sha256") or ""), int(item.get("size") or 0))
        for item in receipt.get("attachments") or []
    )
    if actual != expected:
        raise ForjaN3Error("anexos do draft divergem do manifesto")
    _, state, _ = record_event(
        case_dir,
        "draft_created",
        expected_revision=expected_revision,
        idempotency_key=f"{case_dir.name}:draft:{receipt['draftId']}",
        phase=state.get("phaseCursor"),
        payload={
            "draftId": receipt["draftId"],
            "threadId": receipt["threadId"],
            "packageId": manifest["packageId"],
            "packageHash": manifest["packageHash"],
            "bodySha256": receipt["bodySha256"],
            "attachments": receipt["attachments"],
        },
    )
    return state


def confirm_delivery(case_dir: Path, evidence_path: Path, *, expected_revision: int) -> dict:
    manifest, state = _canonical_manifest(case_dir, expected_revision)
    evidence = read_json(evidence_path, None)
    if not isinstance(evidence, dict):
        raise ForjaN3Error("evidência inválida")
    if evidence.get("packageHash") != manifest.get("packageHash"):
        raise ForjaN3Error("evidência vinculada a pacote diferente")
    evidence_type = evidence.get("type")
    if evidence_type not in {"email", "whatsapp", "protocolo", "arquivo", "reconciliacao"}:
        raise ForjaN3Error("tipo de evidência inválido")
    if not evidence.get("externalId") and not evidence.get("path"):
        raise ForjaN3Error("evidência exige identificador externo ou caminho")
    if evidence.get("path") and not Path(evidence["path"]).exists():
        raise ForjaN3Error("caminho da evidência não existe")
    if evidence.get("path"):
        if not evidence.get("sha256"):
            raise ForjaN3Error("evidência em arquivo exige sha256")
        if sha256_file(Path(evidence["path"])) != evidence.get("sha256"):
            raise ForjaN3Error("arquivo de evidência diverge do hash informado")
    if state.get("phaseCursor") != "F10_ENTREGA_EVIDENCIA_APRENDIZADO":
        _, state, _ = record_event(
            case_dir,
            "phase_started",
            expected_revision=expected_revision,
            idempotency_key=f"{case_dir.name}:f10:started:{manifest['packageHash']}",
            phase="F10_ENTREGA_EVIDENCIA_APRENDIZADO",
            payload={"packageHash": manifest["packageHash"]},
        )
        expected_revision = state["revision"]
    _, state, _ = record_event(
        case_dir,
        "delivery_confirmed",
        expected_revision=expected_revision,
        idempotency_key=f"{case_dir.name}:delivery:{canonical_hash(evidence)}",
        phase=state.get("phaseCursor"),
        payload=evidence,
    )
    return state


def fulfill(case_dir: Path, *, expected_revision: int) -> dict:
    _, state = _canonical_manifest(case_dir, expected_revision)
    if state.get("deliveryEvidence") is None:
        raise ForjaN3Error("cumprimento sem evidência de entrega")
    f10_gates = compute_f10_gates(
        state["package"],
        state["deliveryEvidence"],
        state,
        minimum_synced_event_seq=expected_revision - 1,
    )
    f10_validation = validate_f10_gates(f10_gates)
    if not f10_validation["approved"]:
        raise ForjaN3Error("gates F10 não aprovados: " + "; ".join(f10_validation["findings"]))
    for artifact_id in ("run_metrics", "retrospective"):
        entry = (state.get("artifacts") or {}).get(artifact_id) or {}
        path = Path(str(entry.get("path") or ""))
        if not path.is_file() or not entry.get("sha256") or sha256_file(path) != entry.get("sha256"):
            raise ForjaN3Error(f"F10 sem artefato íntegro obrigatório: {artifact_id}")
    from forja_n4_validate import validate_case as validate_n4

    n4_validation = validate_n4(case_dir, target_phase="F10_ENTREGA_EVIDENCIA_APRENDIZADO")
    if n4_validation.get("blocksCurrentFlow"):
        raise ForjaN3Error("F10 bloqueada pela N4: " + "; ".join(item["detail"] for item in n4_validation.get("findings") or [] if item.get("severity") == "p0"))
    if "F10_ENTREGA_EVIDENCIA_APRENDIZADO" not in (state.get("completedPhases") or []):
        _, state, _ = record_event(
            case_dir,
            "phase_completed",
            expected_revision=expected_revision,
            idempotency_key=f"{case_dir.name}:f10:completed:{state['package']['packageHash']}",
            phase="F10_ENTREGA_EVIDENCIA_APRENDIZADO",
            payload={"result": "pass", "lifecycleStatus": "sent_confirmed"},
        )
    _, state, _ = record_event(
        case_dir,
        "case_fulfilled",
        expected_revision=state["revision"],
        idempotency_key=f"{case_dir.name}:fulfilled:{state['package']['packageHash']}",
        phase=state.get("phaseCursor"),
        payload={"packageHash": state["package"]["packageHash"], "gates": f10_gates},
    )
    return state


def main() -> None:
    parser = argparse.ArgumentParser(description="Fechamento canônico FORJA N3")
    parser.add_argument("case")
    sub = parser.add_subparsers(dest="command", required=True)
    package = sub.add_parser("package")
    package.add_argument("definition", type=Path)
    package.add_argument("--expected-revision", type=int, required=True)
    draft = sub.add_parser("register-draft")
    draft.add_argument("receipt", type=Path)
    draft.add_argument("--expected-revision", type=int, required=True)
    delivery = sub.add_parser("confirm-delivery")
    delivery.add_argument("evidence", type=Path)
    delivery.add_argument("--expected-revision", type=int, required=True)
    done = sub.add_parser("fulfill")
    done.add_argument("--expected-revision", type=int, required=True)
    args = parser.parse_args()
    case_dir = resolve_case_dir(args.case)
    if args.command == "package":
        result = create_package(case_dir, args.definition, expected_revision=args.expected_revision)
    elif args.command == "register-draft":
        result = register_draft(case_dir, args.receipt, expected_revision=args.expected_revision)
    elif args.command == "confirm-delivery":
        result = confirm_delivery(case_dir, args.evidence, expected_revision=args.expected_revision)
    else:
        result = fulfill(case_dir, expected_revision=args.expected_revision)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
