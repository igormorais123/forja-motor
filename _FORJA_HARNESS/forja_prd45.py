"""Porta operacional read-only/sidecar do PRD 45.

O comando não promove fases e não altera N3/N4. ``baseline`` grava apenas o
manifesto de observação por caso; ``map`` exige os ledgers fornecidos e grava a
ponte no namespace experimental; lints e métricas apenas leem.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from forja_baseline_canonico import freeze_all, verify_case
from forja_grafo_lint import lint_file
from forja_instrumentacao import metrics_for_case, validate_ledger
from forja_n3_common import atomic_write_json, sha256_file
from forja_proposition_evidence import build_map, validate_map


def _read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _main() -> int:
    parser = argparse.ArgumentParser(description="PRD 45 — ponte e instrumentação experimental da FORJA")
    sub = parser.add_subparsers(dest="command", required=True)
    baseline = sub.add_parser("baseline")
    baseline.add_argument("--state", type=Path)
    baseline.add_argument("--output", type=Path)
    verify = sub.add_parser("verify-baseline")
    verify.add_argument("case", type=Path)
    graph = sub.add_parser("lint-graph")
    graph.add_argument("path", type=Path)
    obs = sub.add_parser("observation")
    obs.add_argument("case", type=Path)
    bridge = sub.add_parser("map")
    bridge.add_argument("--case-id", required=True)
    bridge.add_argument("--run-id", required=True)
    bridge.add_argument("--propositions", type=Path, required=True)
    bridge.add_argument("--sources", type=Path, required=True)
    bridge.add_argument("--links", type=Path)
    bridge.add_argument("--blocked", type=Path)
    bridge.add_argument("--output", type=Path, required=True)
    lint = sub.add_parser("lint-map")
    lint.add_argument("path", type=Path)
    lint.add_argument("--propositions", type=Path)
    lint.add_argument("--sources", type=Path)
    args = parser.parse_args()
    if args.command == "baseline":
        report = freeze_all(args.state)
        if args.output:
            atomic_write_json(args.output, report)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0
    if args.command == "verify-baseline":
        report = verify_case(args.case)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if report.get("status") in {"pass", "not_verified"} else 1
    if args.command == "lint-graph":
        report = lint_file(args.path)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0
    if args.command == "observation":
        report = {"validation": validate_ledger(args.case), "metrics": metrics_for_case(args.case)}
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if report["validation"]["approved"] else 1
    propositions = _read(args.propositions)
    sources = _read(args.sources)
    links = _read(args.links) if args.links else []
    blocked = _read(args.blocked) if args.blocked else []
    payload = build_map(case_id=args.case_id, producer_run_id=args.run_id, proposition_ledger=propositions,
                        source_ledger=sources, links=links if isinstance(links, list) else links.get("links", []),
                        blocked_propositions=blocked if isinstance(blocked, list) else blocked.get("blockedPropositions", []),
                        proposition_hash=sha256_file(args.propositions), source_hash=sha256_file(args.sources))
    atomic_write_json(args.output, payload)
    findings = validate_map(payload, propositions, sources, source_base_dir=args.sources.parent)
    print(json.dumps({"output": str(args.output), "findings": findings, "approvedForObservation": not any(item.get("severity") == "p0" for item in findings)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
