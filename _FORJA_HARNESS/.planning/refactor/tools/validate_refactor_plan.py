from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parents[1]
PLANS = ROOT / "plans"


def fail(message: str) -> None:
    print(f"ERROR: {message}")
    raise SystemExit(1)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_frontmatter(raw: str) -> dict[str, object]:
    if not raw.startswith("---\n"):
        fail("plan without frontmatter")
    front = raw.split("---", 2)[1]
    result: dict[str, object] = {}
    for key in ("plan", "phase", "type", "wave", "autonomous"):
        match = re.search(fr"^{key}:\s*(.+)$", front, flags=re.MULTILINE)
        if match:
            result[key] = match.group(1).strip()
    for key in ("depends_on", "requirements"):
        match = re.search(fr"^{key}:\s*\[(.*?)\]", front, flags=re.MULTILINE)
        result[key] = [item.strip() for item in match.group(1).split(",") if item.strip()] if match else []
    files_match = re.search(r"^files_modified:\s*\n((?:\s+-\s+.*\n?)+)", front, flags=re.MULTILINE)
    result["files_modified"] = (
        [line.split("-", 1)[1].strip() for line in files_match.group(1).splitlines()] if files_match else []
    )
    return result


def ancestors(plan_id: str, plans: dict[str, dict[str, object]]) -> set[str]:
    found: set[str] = set()

    def visit(current: str) -> None:
        for dependency in plans[current]["depends_on"]:
            if dependency not in found:
                found.add(dependency)
                visit(dependency)

    visit(plan_id)
    return found


def path_matches_product(path: str, product: str) -> bool:
    clean_path = path.replace("\\", "/").rstrip("/")
    clean_product = product.replace("\\", "/").rstrip("/")
    return clean_path == clean_product or clean_path.startswith(clean_product + "/")


def validate_plans(plan_files: list[Path], rf_expected: set[str]) -> tuple[dict[str, dict[str, object]], int]:
    required_tags = (
        "<objective>",
        "<threat_model>",
        "<tasks>",
        "<read_first>",
        "<action>",
        "<acceptance_criteria>",
        "<verification>",
        "<success_criteria>",
    )
    plans: dict[str, dict[str, object]] = {}
    rf_planned: set[str] = set()
    read_first_total = 0

    for plan_file in plan_files:
        raw = plan_file.read_text(encoding="utf-8")
        missing_tags = [tag for tag in required_tags if tag not in raw]
        if missing_tags:
            fail(f"{plan_file.name} missing tags: {missing_tags}")
        front = parse_frontmatter(raw)
        plan_id = str(front.get("plan", ""))
        if not plan_id or plan_id in plans:
            fail(f"invalid or duplicate plan ID in {plan_file.name}: {plan_id!r}")
        if str(front.get("autonomous", "")).lower() == "true":
            wildcard = [path for path in front["files_modified"] if "*" in path or "?" in path]
            if wildcard:
                fail(f"autonomous plan {plan_id} contains wildcard files_modified: {wildcard}")
        front["file"] = plan_file
        front["raw"] = raw
        front["read_first"] = re.findall(r"<file>(.*?)</file>", raw)
        read_first_total += len(front["read_first"])
        plans[plan_id] = front
        rf_planned.update(re.findall(r"RF-REF-\d{3}", raw.split("---", 2)[1]))

    if rf_planned != rf_expected:
        fail(
            "requirement coverage mismatch: "
            f"missing={sorted(rf_expected - rf_planned)} extra={sorted(rf_planned - rf_expected)}"
        )

    for plan_id, plan in plans.items():
        unknown = [dependency for dependency in plan["depends_on"] if dependency not in plans]
        if unknown:
            fail(f"{plan_id} has unknown dependencies: {unknown}")

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(plan_id: str) -> None:
        if plan_id in visiting:
            fail(f"dependency cycle detected at {plan_id}")
        if plan_id in visited:
            return
        visiting.add(plan_id)
        for dependency in plans[plan_id]["depends_on"]:
            visit(dependency)
        visiting.remove(plan_id)
        visited.add(plan_id)

    for plan_id in plans:
        visit(plan_id)

    unresolved: list[str] = []
    for plan_id, plan in plans.items():
        producers = ancestors(plan_id, plans) | {plan_id}
        products = [str(item) for producer in producers for item in plans[producer]["files_modified"]]
        for item in plan["read_first"]:
            resolved = (WORKSPACE / item).resolve()
            if resolved.exists():
                continue
            if any(path_matches_product(item, product) for product in products):
                continue
            unresolved.append(f"{plan_id}:{item}")
    if unresolved:
        fail(f"read_first paths neither present nor produced by dependency: {unresolved}")

    return plans, read_first_total


def validate_deliverables(manifest: dict[str, object]) -> None:
    deliverables = manifest.get("deliverables")
    if not isinstance(deliverables, dict):
        fail("manifest has no deliverables section")
    for name in ("pdf", "docx", "visualQa", "buildReport", "mermaidReport", "hashManifest"):
        relative = deliverables.get(name)
        if not relative:
            fail(f"manifest deliverable missing: {name}")
        path = ROOT / str(relative)
        if not path.is_file() or path.stat().st_size == 0:
            fail(f"deliverable missing or empty: {relative}")

    qa = json.loads((ROOT / str(deliverables["visualQa"])).read_text(encoding="utf-8"))
    if not qa.get("allPagesInspected") or qa.get("issues"):
        fail("visual QA is incomplete or has unresolved issues")
    build = json.loads((ROOT / str(deliverables["buildReport"])).read_text(encoding="utf-8"))
    if build.get("diagramsEmbedded", 0) < 15 or build.get("executionAuthorized") is not False:
        fail("build report does not prove vector diagram coverage or planning-only status")
    mermaid = json.loads((ROOT / str(deliverables["mermaidReport"])).read_text(encoding="utf-8"))
    if not mermaid.get("ok") or mermaid.get("count", 0) < 30:
        fail("Mermaid atlas is incomplete")

    hash_manifest = json.loads((ROOT / str(deliverables["hashManifest"])).read_text(encoding="utf-8"))
    for item in hash_manifest.get("files", []):
        path = ROOT / item["path"]
        if not path.is_file() or sha256(path) != item["sha256"]:
            fail(f"planning snapshot hash mismatch: {item['path']}")


def main() -> None:
    preflight = "--preflight" in sys.argv
    manifest = json.loads((ROOT / "REFACTOR_PLAN_MANIFEST.json").read_text(encoding="utf-8"))
    if manifest.get("executionAuthorized") is not False:
        fail("executionAuthorized must remain false in a planning-only package")
    if manifest.get("schemaVersion") != "FORJA-REFACTOR-PLAN-1.0":
        fail("unexpected or missing schemaVersion")
    if manifest.get("pathResolutionRoot") != "_FORJA_HARNESS":
        fail("pathResolutionRoot must be _FORJA_HARNESS")

    required_docs = [ROOT / name for name in manifest["documents"]]
    missing_docs = [str(path.relative_to(ROOT)) for path in required_docs if not path.is_file()]
    if missing_docs:
        fail(f"missing canonical documents: {missing_docs}")

    prd = (ROOT / "01-PRD_REFATORACAO_FORJA.md").read_text(encoding="utf-8")
    rf_expected = {f"RF-REF-{number:03d}" for number in range(1, 23)}
    rf_defined = set(re.findall(r"RF-REF-\d{3}", prd))
    if not rf_expected <= rf_defined:
        fail(f"missing product requirements: {sorted(rf_expected - rf_defined)}")

    plan_files = sorted(PLANS.glob("P*-PLAN.md"))
    if len(plan_files) != 18:
        fail(f"expected 18 executable plans, found {len(plan_files)}")
    plans, read_first_total = validate_plans(plan_files, rf_expected)

    diagrams = (ROOT / "04-DIAGRAMAS_REFATORACAO_FORJA.md").read_text(encoding="utf-8")
    ids = re.findall(r"^## (D\d{2})", diagrams, flags=re.MULTILINE)
    blocks = re.findall(r"```mermaid\n(.*?)\n```", diagrams, flags=re.DOTALL)
    if ids != [f"D{number:02d}" for number in range(1, 23)]:
        fail(f"diagram IDs are incomplete or out of order: {ids}")
    if len(blocks) != len(ids):
        fail(f"diagram heading/block mismatch: {len(ids)} headings vs {len(blocks)} blocks")

    joined = "\n".join(
        (ROOT / name).read_text(encoding="utf-8")
        for name in ("02-TDD_REFATORACAO_FORJA.md", "03-ROADMAP_REFATORACAO_FORJA.md", "05-MATRIZ_RASTREABILIDADE.md")
    ) + "\n" + plans["P16"]["raw"]
    for token in ("G9A", "G9B", "compatibilidade dependente"):
        if token not in joined:
            fail(f"G9A/G9B separation missing token: {token}")

    if not preflight:
        validate_deliverables(manifest)

    print(
        json.dumps(
            {
                "ok": True,
                "mode": "preflight" if preflight else "final",
                "documents": len(required_docs),
                "plans": len(plan_files),
                "requirements": len(rf_expected),
                "readFirstChecked": read_first_total,
                "dagNodes": len(plans),
                "mermaidDiagrams": len(blocks),
                "executionAuthorized": manifest["executionAuthorized"],
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
