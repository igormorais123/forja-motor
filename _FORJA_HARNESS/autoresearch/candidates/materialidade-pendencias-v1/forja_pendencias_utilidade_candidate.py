"""Validador candidato da materialidade de pendências da FORJA.

Este módulo não integra o caminho crítico de produção. Ele existe em
``autoresearch/candidates`` e só pode ser promovido após o ciclo AR.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

PROTOCOL_VERSION = "FORJA-PEND-MAT-v1-candidate"
CLASSIFICATIONS = {
    "essential_to_product",
    "essential_to_claim",
    "useful_nonblocking",
    "irrelevant",
    "superseded",
}
TREATMENTS = {
    "hold_product",
    "exclude_claim",
    "qualify_claim",
    "deliver_and_optional_adendum",
    "drop",
}


def _words(text: str) -> int:
    return len(re.findall(r"\b[\wÀ-ÿ'-]+\b", text or "", flags=re.UNICODE))


def validate(payload: dict) -> list[str]:
    errors: list[str] = []
    if payload.get("protocolVersion") != PROTOCOL_VERSION:
        errors.append("protocolVersion inválido")
    if not str(payload.get("productObjective") or "").strip():
        errors.append("productObjective obrigatório")

    delivery = payload.get("deliveryDecision")
    if delivery not in {"proceed", "hold"}:
        errors.append("deliveryDecision deve ser proceed ou hold")

    message = str(payload.get("lawyerMessage") or "").strip()
    if not message:
        errors.append("lawyerMessage obrigatório")
    elif _words(message) > 70:
        errors.append("lawyerMessage excede 70 palavras")

    items = payload.get("items")
    if not isinstance(items, list) or not items:
        errors.append("items deve ser lista não vazia")
        return errors

    seen: set[str] = set()
    product_blockers = 0
    mentioned_ids = set(payload.get("mentionedItemIds") or [])

    for index, item in enumerate(items, start=1):
        prefix = f"item {index}"
        item_id = str(item.get("id") or "").strip()
        if not item_id:
            errors.append(f"{prefix}: id obrigatório")
        elif item_id in seen:
            errors.append(f"{prefix}: id duplicado")
        seen.add(item_id)

        classification = item.get("classification")
        treatment = item.get("treatment")
        if classification not in CLASSIFICATIONS:
            errors.append(f"{prefix}: classification inválida")
            continue
        if treatment not in TREATMENTS:
            errors.append(f"{prefix}: treatment inválido")

        affected = str(item.get("affectedClaim") or "").strip()
        consequence = str(item.get("consequence") or "").strip()
        if classification in {"essential_to_product", "essential_to_claim"}:
            if not affected:
                errors.append(f"{prefix}: affectedClaim obrigatório para item essencial")
            if not consequence:
                errors.append(f"{prefix}: consequence obrigatória para item essencial")

        request_before = item.get("requestBeforeDelivery")
        if not isinstance(request_before, bool):
            errors.append(f"{prefix}: requestBeforeDelivery deve ser booleano")

        if classification == "essential_to_product":
            product_blockers += 1
            if treatment != "hold_product":
                errors.append(f"{prefix}: essential_to_product exige hold_product")
            if request_before is not True:
                errors.append(f"{prefix}: essential_to_product exige diligência antes da entrega")

        if classification == "essential_to_claim":
            if treatment not in {"exclude_claim", "qualify_claim"}:
                errors.append(f"{prefix}: essential_to_claim exige excluir ou qualificar a afirmação")

        if classification == "useful_nonblocking":
            if request_before is not False:
                errors.append(f"{prefix}: useful_nonblocking não pode atrasar a entrega")
            if treatment != "deliver_and_optional_adendum":
                errors.append(f"{prefix}: useful_nonblocking exige adendo opcional")

        if classification in {"irrelevant", "superseded"}:
            if request_before is not False or treatment != "drop":
                errors.append(f"{prefix}: item descartado não pode gerar espera ou diligência")
            if item_id and item_id in mentioned_ids:
                errors.append(f"{prefix}: item descartado não pode aparecer na mensagem")

    if product_blockers and delivery != "hold":
        errors.append("deliveryDecision deve ser hold quando há essential_to_product")
    if not product_blockers and delivery != "proceed":
        errors.append("deliveryDecision deve ser proceed sem essential_to_product")

    valid_ids = seen
    unknown_mentions = mentioned_ids - valid_ids
    if unknown_mentions:
        errors.append("mentionedItemIds contém id desconhecido")

    if len(mentioned_ids) > 2:
        errors.append("mensagem ao advogado não deve listar mais de duas pendências")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida PENDENCY_DECISION candidato")
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    payload = json.loads(args.path.read_text(encoding="utf-8"))
    errors = validate(payload)
    print(json.dumps({"ok": not errors, "errors": errors}, ensure_ascii=False, indent=2))
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())

