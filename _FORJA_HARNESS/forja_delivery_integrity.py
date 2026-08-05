"""Create and verify the N4 F9/F10 delivery-integrity chain."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from forja_consistency import validate_delivery
from forja_n3_common import ForjaN3Error, atomic_write_json, now_iso, read_json, resolve_case_dir, sha256_file
from forja_n4_common import build_envelope, write_artifact
from forja_state_machine import derive_state, record_event


def _attachment(package: dict, artifact_id: str) -> dict:
    matches = [item for item in package.get("attachments") or [] if item.get("artifactId") == artifact_id]
    if len(matches) != 1:
        raise ForjaN3Error(f"artefato {artifact_id} não aparece uma única vez no pacote")
    item = matches[0]
    path = Path(str(item.get("packagePath") or item.get("path") or ""))
    if not path.is_file():
        raise ForjaN3Error(f"anexo selecionado ausente: {path}")
    actual = sha256_file(path)
    if actual != item.get("sha256"):
        raise ForjaN3Error("anexo selecionado diverge do hash registrado no pacote")
    return {**item, "path": str(path), "sha256": actual}


def select(case_dir: Path, artifact_id: str, *, layout_profile_id: str, producer_run_id: str, reviewer_run_id: str) -> dict:
    package = read_json(case_dir / "FORJA_PACKAGE.json", None)
    if not isinstance(package, dict):
        raise ForjaN3Error("FORJA_PACKAGE.json ausente")
    attachment = _attachment(package, artifact_id)
    content = {
        "packageArtifactId": package.get("packageId"),
        "selectedArtifactId": artifact_id,
        "auditPackageHash": package.get("packageHash"),
        "packageHash": attachment["sha256"],
        "selectedHash": attachment["sha256"],
        "selectedPath": attachment["path"],
        "preSendMatch": True,
        "layoutProfileId": layout_profile_id,
    }
    payload = build_envelope(
        case_dir,
        "F9_DELIVERY_SELECTION.json",
        content,
        source_hashes=[str(package.get("packageHash")), attachment["sha256"]],
        producer_run_id=producer_run_id,
        reviewer_run_id=reviewer_run_id,
        status="approved",
    )
    findings = validate_delivery(payload)
    if findings:
        raise ForjaN3Error("seleção de entrega reprovada: " + "; ".join(x["detail"] for x in findings))
    write_artifact(case_dir, "F9_DELIVERY_SELECTION.json", payload)
    state = derive_state(case_dir)
    if state.get("revision"):
        record_event(
            case_dir,
            "delivery_selection_verified",
            expected_revision=state["revision"],
            idempotency_key=f"n4-delivery-selection:{payload['contentHash']}",
            actor="forja-n4-delivery",
            payload={"artifactId": artifact_id, "selectedHash": attachment["sha256"]},
        )
    return payload


def confirm(
    case_dir: Path,
    *,
    mode: str,
    delivery_evidence_id: str | None,
    delivered_path: Path | None,
    producer_run_id: str,
    reviewer_run_id: str,
    delivered_at: str | None = None,
) -> dict:
    selection = read_json(case_dir / "n4_artifacts" / "F9_DELIVERY_SELECTION.json", None)
    if not isinstance(selection, dict):
        raise ForjaN3Error("seleção F9 ausente")
    if mode == "channel_hash":
        if not delivered_path or not delivered_path.is_file():
            raise ForjaN3Error("channel_hash exige arquivo entregue acessível")
        delivered_hash = sha256_file(delivered_path)
        post = {"mode": mode, "deliveredHash": delivered_hash, "deliveryEvidenceId": delivery_evidence_id, "status": "confirmed"}
    elif mode == "artifact_evidence":
        if not delivery_evidence_id:
            raise ForjaN3Error("artifact_evidence exige evidência externa")
        post = {"mode": mode, "deliveredHash": None, "deliveryEvidenceId": delivery_evidence_id, "status": "confirmed"}
    else:
        raise ForjaN3Error(f"modo inválido: {mode}")
    content = {
        key: selection.get(key)
        for key in ("packageArtifactId", "selectedArtifactId", "auditPackageHash", "packageHash", "selectedHash", "selectedPath", "preSendMatch", "layoutProfileId")
    }
    content["postDeliveryVerification"] = post
    content["deliveredAt"] = delivered_at or now_iso()
    payload = build_envelope(
        case_dir,
        "F10_DELIVERY_INTEGRITY.json",
        content,
        source_hashes=[selection["contentHash"], selection["selectedHash"]],
        producer_run_id=producer_run_id,
        reviewer_run_id=reviewer_run_id,
        status="approved",
    )
    findings = validate_delivery(payload)
    if findings:
        raise ForjaN3Error("integridade pós-entrega reprovada: " + "; ".join(x["detail"] for x in findings))
    write_artifact(case_dir, "F10_DELIVERY_INTEGRITY.json", payload)
    history_path = case_dir / "n4_artifacts" / "delivery_history" / f"{payload['contentHash']}.json"
    if not history_path.exists():
        atomic_write_json(history_path, payload)
    state = derive_state(case_dir)
    if state.get("revision"):
        record_event(
            case_dir,
            "delivery_integrity_recorded",
            expected_revision=state["revision"],
            idempotency_key=f"n4-delivery-integrity:{payload['contentHash']}",
            actor="forja-n4-delivery",
            payload={"mode": mode, "selectedHash": selection["selectedHash"]},
        )
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Integridade de seleção e entrega FORJA N4")
    parser.add_argument("case")
    sub = parser.add_subparsers(dest="command", required=True)
    choose = sub.add_parser("select")
    choose.add_argument("artifact_id")
    choose.add_argument("--layout-profile-id", required=True)
    choose.add_argument("--producer-run-id", required=True)
    choose.add_argument("--reviewer-run-id", required=True)
    done = sub.add_parser("confirm")
    done.add_argument("--mode", choices=["channel_hash", "artifact_evidence"], required=True)
    done.add_argument("--delivery-evidence-id")
    done.add_argument("--delivered-path", type=Path)
    done.add_argument("--delivered-at")
    done.add_argument("--producer-run-id", required=True)
    done.add_argument("--reviewer-run-id", required=True)
    args = parser.parse_args()
    case_dir = resolve_case_dir(args.case)
    if args.command == "select":
        result = select(case_dir, args.artifact_id, layout_profile_id=args.layout_profile_id, producer_run_id=args.producer_run_id, reviewer_run_id=args.reviewer_run_id)
    else:
        result = confirm(case_dir, mode=args.mode, delivery_evidence_id=args.delivery_evidence_id, delivered_path=args.delivered_path, delivered_at=args.delivered_at, producer_run_id=args.producer_run_id, reviewer_run_id=args.reviewer_run_id)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
