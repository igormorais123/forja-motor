"""Linhagem descritiva de AutoResearch para mudanças de arquitetura.

Ela mede e registra candidatos em diretório isolado. Não altera produção.
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from forja_n3_common import FORJA, ForjaN3Error, atomic_write_json, canonical_hash, new_id, now_iso, read_json, sha256_file


MANIFEST_PATH = FORJA / "AR_ARCH_MANIFEST.json"
SCHEMA_PATH = FORJA / "ar_architecture" / "schemas" / "architecture_candidate.schema.json"
CANDIDATE_ROOT = FORJA / "ar_architecture" / "candidates"
RELEVANT_MODULES = {
    "forja_post_protocol",
    "forja_document_compare",
    "forja_post_protocol_contracts",
    "forja_learning",
    "forja_learning_registry",
    "forja_n4_common",
    "forja_n4_validate",
    "forja_state_machine",
    "forja_delivery_integrity",
    "forja_package",
    "forja_f8_contract",
}
SHADOW_TESTS = [
    "test_forja_post_protocol.py",
    "test_gmail_management_matching.py",
    "test_forja_n3_state.py",
    "test_forja_architecture.py",
    "test_forja_n4.py",
]
CANARY_TESTS = [
    "test_gmail_management_matching.py::GmailManagementMatchingTests::test_cross_case_delivery_is_removed_from_whatsapp_demand",
    "test_forja_post_protocol.py::PostProtocolStateTests::test_concurrent_post_protocol_revision_conflict",
    "test_forja_post_protocol.py::PostProtocolPipelineTests::test_resent_attachment_does_not_duplicate_capture_or_diff",
    "test_forja_post_protocol.py::PostProtocolPipelineTests::test_baseline_hash_drift_blocks_diff_but_keeps_capture",
    "test_forja_post_protocol.py::PostProtocolStateTests::test_panel_projection_rejects_free_prose",
]
CANDIDATE_SOURCE_FILES = [
    "../.gitignore",
    "../gestao_escritorio/scripts/audit_delivered_docs.py",
    "../gestao_escritorio/scripts/gmail_gws_update.py",
    "../gestao_escritorio/scripts/sync_forja_gestao.py",
    "FORJA_N3_CONFIG.json",
    "AR_ARCH_MANIFEST.json",
    "ar_architecture/schemas/architecture_candidate.schema.json",
    "forja_post_protocol.py",
    "forja_document_compare.py",
    "forja_post_protocol_contracts.py",
    "forja_learning.py",
    "forja_learning_registry.py",
    "forja_n4_common.py",
    "forja_n4_validate.py",
    "forja_state_machine.py",
    "generate_n4_contracts.py",
    "test_forja_post_protocol.py",
    "test_forja_ar_architecture.py",
    "n4_schemas/ARTIFACT_CATALOG.json",
    "n4_schemas/post_protocol_return.schema.json",
    "n4_schemas/protocol_evidence.schema.json",
    "n4_schemas/post_protocol_baseline_backfill.schema.json",
    "n4_schemas/document_comparison.schema.json",
    "n4_schemas/learning_candidate.schema.json",
    "n4_fixtures/post_protocol/devolved_chapters_memoriais_apelacao.json",
    "n4_fixtures/post_protocol/prospective_memoriais_apelacao_suite.json",
]


def automation_enabled(config: dict) -> bool:
    return bool((config.get("features") or {}).get("n4PostProtocolV1"))


def _semantic(candidate: dict) -> dict:
    return {key: value for key, value in candidate.items() if key not in {"contentHash", "updatedAt"}}


def _write_candidate(path: Path, candidate: dict) -> None:
    candidate["updatedAt"] = now_iso()
    candidate["contentHash"] = canonical_hash(_semantic(candidate))
    atomic_write_json(path, candidate)


def validate_candidate(candidate: dict) -> list[str]:
    try:
        import jsonschema

        schema = read_json(SCHEMA_PATH, {})
        jsonschema.Draft202012Validator(schema).validate(candidate)
    except ImportError:
        required = set(read_json(SCHEMA_PATH, {}).get("required") or [])
        missing = sorted(required - set(candidate))
        return [f"campos ausentes: {missing}"] if missing else []
    except Exception as exc:
        return [str(exc)]
    if candidate.get("contentHash") != canonical_hash(_semantic(candidate)):
        return ["contentHash divergente"]
    return []


def validate_manifest(manifest: dict) -> list[str]:
    errors: list[str] = []
    if manifest.get("lineage") != "AR-Architecture":
        errors.append("lineage inválida")
    if manifest.get("maturityCeiling") != "estudo_descritivo":
        errors.append("maturityCeiling deve ser estudo_descritivo")
    if manifest.get("productionMutationAllowed") is not False:
        errors.append("productionMutationAllowed deve ser false")
    for key in (
        "targetedTestsPassed",
        "targetedTestsFailed",
        "trackedVaultLeakCount",
        "panelForbiddenKeyCount",
        "relevantImportCycleCount",
        "rollbackRehearsalPassed",
    ):
        if key not in (manifest.get("indicators") or {}):
            errors.append(f"indicador ausente: {key}")
    for gate in ("shadow", "canary", "independentReview", "rollback", "ceiling"):
        if gate not in (manifest.get("gates") or {}):
            errors.append(f"gate ausente: {gate}")
    return errors


def create_candidate(candidate_id: str, *, title: str, problem: str, hypothesis: str, scope: list[str]) -> Path:
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]+", candidate_id):
        raise ForjaN3Error("candidateId inválido")
    directory = CANDIDATE_ROOT / candidate_id
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "ARCHITECTURE_CANDIDATE.json"
    manifest = read_json(MANIFEST_PATH, {}) or {}
    manifest_errors = validate_manifest(manifest)
    if manifest_errors:
        raise ForjaN3Error("AR_ARCH_MANIFEST.json inválido: " + "; ".join(manifest_errors))
    snapshot = [
        {"path": name, "sha256": sha256_file(FORJA / name)}
        for name in CANDIDATE_SOURCE_FILES
        if (FORJA / name).is_file()
    ]
    source_hashes = sorted(set([item["sha256"] for item in snapshot] + [sha256_file(MANIFEST_PATH)]))
    baseline_tree = subprocess.run(
        ["git", "rev-parse", "HEAD^{tree}"],
        cwd=FORJA.parent,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    snapshot_hash = canonical_hash(snapshot)
    if path.exists():
        candidate = read_json(path, {}) or {}
        candidate.update({
            "sourceSnapshot": snapshot,
            "baselineTreeHash": baseline_tree,
            "candidateTreeHash": snapshot_hash,
            "candidatePatchHash": snapshot_hash,
            "sourceHashes": source_hashes,
        })
        _write_candidate(path, candidate)
        return path
    stamp = now_iso()
    candidate = {
        "schemaVersion": 1,
        "lineage": "AR-Architecture",
        "candidateId": candidate_id,
        "title": title,
        "status": "proposed",
        "producerRunId": new_id("ar-arch-producer"),
        "reviewerRunId": None,
        "sourceHashes": source_hashes,
        "sourceSnapshot": snapshot,
        "baselineTreeHash": baseline_tree,
        "candidateTreeHash": snapshot_hash,
        "candidatePatchHash": snapshot_hash,
        "proposal": {
            "problem": problem,
            "hypothesis": hypothesis,
            "scope": scope,
            "productionMutation": False,
            "isolation": "candidate_directory_read_only_production",
        },
        "experiments": {},
        "metrics": {},
        "review": None,
        "rollback": {
            "recipe": "set features.n4PostProtocolV1=false; preserve captured local evidence",
            "rehearsed": False,
            "passed": False,
        },
        "createdAt": stamp,
        "updatedAt": stamp,
    }
    _write_candidate(path, candidate)
    errors = validate_candidate(candidate)
    if errors:
        raise ForjaN3Error("candidato inválido: " + "; ".join(errors))
    return path


def _run_pytest(targets: list[str], *, cwd: Path = FORJA, timeout: int = 180) -> dict:
    started = now_iso()
    try:
        process = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", *targets],
            cwd=cwd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        output = ((exc.stdout or "") + "\n" + (exc.stderr or "")).strip()
        return {
            "passed": False,
            "timedOut": True,
            "timeoutSeconds": timeout,
            "exitCode": None,
            "testsPassed": 0,
            "testsFailed": 0,
            "outputHash": canonical_hash(output),
            "startedAt": started,
            "finishedAt": now_iso(),
        }
    output = (process.stdout + "\n" + process.stderr).strip()
    passed = 0
    failed = 0
    match = re.search(r"(\d+)\s+passed", output)
    if match:
        passed = int(match.group(1))
    match = re.search(r"(\d+)\s+failed", output)
    if match:
        failed = int(match.group(1))
    return {
        "passed": process.returncode == 0,
        "exitCode": process.returncode,
        "testsPassed": passed,
        "testsFailed": failed,
        "outputHash": canonical_hash(output),
        "timedOut": False,
        "timeoutSeconds": timeout,
        "startedAt": started,
        "finishedAt": now_iso(),
    }


def _relevant_import_graph() -> dict[str, set[str]]:
    graph = {name: set() for name in RELEVANT_MODULES}
    for name in RELEVANT_MODULES:
        path = FORJA / f"{name}.py"
        if not path.is_file():
            continue
        tree = ast.parse(path.read_text(encoding="utf-8-sig"))
        for node in ast.walk(tree):
            imported = None
            if isinstance(node, ast.ImportFrom):
                imported = (node.module or "").split(".")[0]
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    root = alias.name.split(".")[0]
                    if root in graph:
                        graph[name].add(root)
            if imported in graph:
                graph[name].add(imported)
    return graph


def _cycle_count(graph: dict[str, set[str]]) -> int:
    index = 0
    stack: list[str] = []
    indexes: dict[str, int] = {}
    low: dict[str, int] = {}
    on_stack: set[str] = set()
    cycles = 0

    def visit(node: str) -> None:
        nonlocal index, cycles
        indexes[node] = low[node] = index
        index += 1
        stack.append(node)
        on_stack.add(node)
        for neighbor in graph[node]:
            if neighbor not in indexes:
                visit(neighbor)
                low[node] = min(low[node], low[neighbor])
            elif neighbor in on_stack:
                low[node] = min(low[node], indexes[neighbor])
        if low[node] == indexes[node]:
            component = []
            while True:
                member = stack.pop()
                on_stack.remove(member)
                component.append(member)
                if member == node:
                    break
            if len(component) > 1 or (len(component) == 1 and component[0] in graph[component[0]]):
                cycles += 1

    for node in graph:
        if node not in indexes:
            visit(node)
    return cycles


def _tracked_vault_leaks(repo_root: Path | None = None) -> list[str]:
    root = repo_root or FORJA.parent
    process = subprocess.run(
        ["git", "-c", "core.quotepath=false", "ls-files", "-z", "--", "_FORJA_HARNESS/state"],
        cwd=root,
        capture_output=True,
        check=True,
    )
    return [
        line
        for line in process.stdout.decode("utf-8", errors="strict").split("\0")
        if line
        if "/private/post_protocol/" in line
        or "/PEÇA PROTOCOLADA — " in line
        or "/VERSÃO HUMANA FINAL — " in line
    ]


def _vault_ignore_failures(repo_root: Path) -> list[str]:
    probes = [
        "_FORJA_HARNESS/state/case-probe/private/post_protocol/evidence.pdf",
        "_FORJA_HARNESS/private/post_protocol/POST_PROTOCOL_LAST_RUN.json",
        "_FORJA_HARNESS/state/case-probe/PEÇA PROTOCOLADA — TESTE/evidence.pdf",
        "_FORJA_HARNESS/state/case-probe/VERSÃO HUMANA FINAL — TESTE/evidence.pdf",
    ]
    failures = []
    for probe in probes:
        result = subprocess.run(
            ["git", "-c", "core.quotepath=false", "check-ignore", "--no-index", "-q", "--", probe],
            cwd=repo_root,
            capture_output=True,
            check=False,
        )
        if result.returncode != 0:
            failures.append(probe)
    return failures


def _rollback_rehearsal(harness: Path) -> dict:
    config_path = harness / "state" / "FORJA_N3_CONFIG.json"
    config = read_json(config_path, {}) or {}
    disabled = json.loads(json.dumps(config))
    disabled.setdefault("features", {})["n4PostProtocolV1"] = False
    atomic_write_json(config_path, disabled)
    dummy = harness / "state" / "case-ar-rollback" / "private" / "post_protocol" / "captured.bin"
    dummy.parent.mkdir(parents=True, exist_ok=True)
    dummy.write_bytes(b"captured-evidence")
    before_hash = sha256_file(dummy)
    script = """
from pathlib import Path
from forja_post_protocol import ingest_return, promote_learning, rebuild_comparison, scan_gmail
calls = [
    lambda: ingest_return(Path('state/case-ar-rollback'), Path('missing.pdf'), account_id='a', thread_id='t', message_id='m', attachment_id='x', received_at='2026-01-01T00:00:00-03:00'),
    lambda: promote_learning(Path('state/case-ar-rollback'), 'missing', approved_by='x', fixture_id='x', test_id='x', evidence_runs=['x']),
    lambda: rebuild_comparison(Path('state/case-ar-rollback'), 'missing'),
]
blocked = 0
for call in calls:
    try:
        call()
    except Exception as exc:
        blocked += 'desabilitado' in str(exc)
scan = scan_gmail(query='noop', max_results=0)
raise SystemExit(0 if blocked == 3 and scan.get('status') == 'disabled' else 4)
"""
    process = subprocess.run(
        [sys.executable, "-c", script],
        cwd=harness,
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    return {
        "passed": (
            automation_enabled(config)
            and not automation_enabled(disabled)
            and process.returncode == 0
            and dummy.is_file()
            and sha256_file(dummy) == before_hash
        ),
        "featureBefore": automation_enabled(config),
        "featureAfter": automation_enabled(disabled),
        "entryPointsBlocked": process.returncode == 0,
        "preservesCapturedEvidence": dummy.is_file() and sha256_file(dummy) == before_hash,
        "configHash": canonical_hash(disabled),
        "outputHash": canonical_hash(process.stdout + process.stderr),
    }


def _overlay_candidate(worktree_harness: Path, snapshot: list[dict]) -> None:
    source_root = FORJA.parent.resolve()
    target_root = worktree_harness.parent.resolve()
    for item in snapshot:
        relative = Path(item["path"])
        source = (FORJA / relative).resolve()
        target = (worktree_harness / relative).resolve()
        if source_root not in source.parents and source != source_root:
            raise ForjaN3Error(f"snapshot fora do repositório: {relative}")
        if target_root not in target.parents and target != target_root:
            raise ForjaN3Error(f"overlay fora do worktree: {relative}")
        if not source.is_file() or sha256_file(source) != item["sha256"]:
            raise ForjaN3Error(f"snapshot do candidato mudou: {relative}")
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def evaluate_candidate(path: Path, *, review_path: Path) -> dict:
    candidate = read_json(path, None)
    if not isinstance(candidate, dict):
        raise ForjaN3Error("candidato ausente")
    manifest = read_json(MANIFEST_PATH, {}) or {}
    manifest_errors = validate_manifest(manifest)
    if manifest_errors:
        raise ForjaN3Error("AR_ARCH_MANIFEST.json inválido: " + "; ".join(manifest_errors))
    with tempfile.TemporaryDirectory(prefix="forja-ar-worktree-") as temp:
        worktree_root = Path(temp) / "repo"
        add = subprocess.run(
            ["git", "worktree", "add", "--detach", str(worktree_root), "HEAD"],
            cwd=FORJA.parent,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
        if add.returncode != 0:
            raise ForjaN3Error("não foi possível criar worktree isolado: " + add.stderr.strip())
        try:
            worktree_harness = worktree_root / FORJA.name
            baseline_targets = [target for target in SHADOW_TESTS if (worktree_harness / target.split("::", 1)[0]).is_file()]
            baseline = _run_pytest(baseline_targets or ["test_forja_architecture.py"], cwd=worktree_harness)
            _overlay_candidate(worktree_harness, candidate.get("sourceSnapshot") or [])
            candidate_shadow = _run_pytest(SHADOW_TESTS, cwd=worktree_harness)
            candidate["experiments"]["isolatedWorktree"] = {
                "baseCommit": subprocess.run(
                    ["git", "rev-parse", "HEAD"],
                    cwd=worktree_root,
                    capture_output=True,
                    text=True,
                    check=True,
                ).stdout.strip(),
                "baseline": baseline,
                "baselineTargets": baseline_targets or ["test_forja_architecture.py"],
                "candidate": candidate_shadow,
                "candidateTargets": SHADOW_TESTS,
                "deltaComparable": (baseline_targets or ["test_forja_architecture.py"]) == SHADOW_TESTS,
                "productionMutation": False,
            }
            candidate["experiments"]["shadow"] = candidate_shadow
            if not candidate_shadow["passed"]:
                candidate["status"] = "rejected"
                _write_candidate(path, candidate)
                return candidate
            candidate["status"] = "shadow_passed"
            canary = _run_pytest(CANARY_TESTS, cwd=worktree_harness)
            candidate["experiments"]["canary"] = canary
            if not canary["passed"]:
                candidate["status"] = "rejected"
                _write_candidate(path, candidate)
                return candidate
            candidate["status"] = "canary_passed"
            rollback = _rollback_rehearsal(worktree_harness)
            leaks = _tracked_vault_leaks(worktree_root)
            ignore_failures = _vault_ignore_failures(worktree_root)
        finally:
            subprocess.run(
                ["git", "worktree", "remove", "--force", str(worktree_root)],
                cwd=FORJA.parent,
                capture_output=True,
                text=True,
                timeout=60,
                check=False,
            )
    review = read_json(review_path, None)
    if not isinstance(review, dict):
        raise ForjaN3Error("revisão independente ausente")
    if review.get("reviewerRunId") == candidate.get("producerRunId"):
        raise ForjaN3Error("revisor independente coincide com produtor")
    if review.get("verdict") != "approve":
        candidate["review"] = review
        candidate["status"] = "rejected"
        _write_candidate(path, candidate)
        return candidate
    candidate["review"] = review
    candidate["reviewerRunId"] = review.get("reviewerRunId")
    candidate["status"] = "independently_reviewed"
    candidate["rollback"].update({
        "rehearsed": True,
        "passed": rollback["passed"],
        "evidence": rollback,
    })
    candidate["status"] = "rollback_rehearsed" if rollback["passed"] else "rejected"
    baseline_metrics = candidate["experiments"]["isolatedWorktree"]["baseline"]
    candidate["metrics"] = {
        "targetedTestsPassed": candidate_shadow["testsPassed"] + canary["testsPassed"],
        "targetedTestsFailed": candidate_shadow["testsFailed"] + canary["testsFailed"],
        "trackedVaultLeakCount": len(leaks) + len(ignore_failures),
        "trackedVaultLeaks": leaks,
        "vaultIgnoreFailures": ignore_failures,
        "panelForbiddenKeyCount": 0 if canary["passed"] else 1,
        "relevantImportCycleCount": _cycle_count(_relevant_import_graph()),
        "rollbackRehearsalPassed": rollback["passed"],
        "baselineTestsPassed": baseline_metrics["testsPassed"],
        "baselineTestsFailed": baseline_metrics["testsFailed"],
        "candidateVsBaselinePassedDelta": (
            candidate_shadow["testsPassed"] - baseline_metrics["testsPassed"]
            if candidate["experiments"]["isolatedWorktree"]["deltaComparable"]
            else None
        ),
    }
    indicators = manifest.get("indicators") or {}
    metrics_pass = (
        candidate["metrics"]["targetedTestsPassed"] >= indicators["targetedTestsPassed"]["minimum"]
        and candidate["metrics"]["targetedTestsFailed"] <= indicators["targetedTestsFailed"]["maximum"]
        and candidate["metrics"]["trackedVaultLeakCount"] <= indicators["trackedVaultLeakCount"]["maximum"]
        and candidate["metrics"]["panelForbiddenKeyCount"] <= indicators["panelForbiddenKeyCount"]["maximum"]
        and candidate["metrics"]["relevantImportCycleCount"] <= indicators["relevantImportCycleCount"]["maximum"]
        and candidate["metrics"]["rollbackRehearsalPassed"] is True
    )
    if candidate["status"] == "rollback_rehearsed" and metrics_pass:
        candidate["status"] = "estudo_descritivo"
    _write_candidate(path, candidate)
    errors = validate_candidate(candidate)
    if errors:
        raise ForjaN3Error("avaliação produziu candidato inválido: " + "; ".join(errors))
    return candidate


def main() -> None:
    parser = argparse.ArgumentParser(description="AR-Architecture descritivo da FORJA")
    sub = parser.add_subparsers(dest="command", required=True)
    create = sub.add_parser("create")
    create.add_argument("candidate_id")
    create.add_argument("--title", required=True)
    create.add_argument("--problem", required=True)
    create.add_argument("--hypothesis", required=True)
    create.add_argument("--scope", action="append", required=True)
    evaluate = sub.add_parser("evaluate")
    evaluate.add_argument("candidate_id")
    evaluate.add_argument("--review", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "create":
        result = create_candidate(
            args.candidate_id,
            title=args.title,
            problem=args.problem,
            hypothesis=args.hypothesis,
            scope=args.scope,
        )
        print(json.dumps({"candidate": str(result)}, ensure_ascii=False, indent=2))
    else:
        path = CANDIDATE_ROOT / args.candidate_id / "ARCHITECTURE_CANDIDATE.json"
        result = evaluate_candidate(path, review_path=args.review)
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
