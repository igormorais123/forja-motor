from __future__ import annotations

import sys
import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import patch

from forja_n3_common import PHASES, atomic_write_json, read_json, sha256_file
from forja_state_machine import initialize_case, record_event


SCRIPTS = Path(__file__).resolve().parents[1] / "gestao_escritorio" / "scripts"
sys.path.insert(0, str(SCRIPTS))
from dashboard_enrichment import enrich_snapshot  # noqa: E402
from sync_forja_gestao import reconcile, reconcile_legacy, sync_case  # noqa: E402
from forja_management_bridge import sync_after_event  # noqa: E402


class ForjaN3ManagementTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        self.demands = root / "demandas.json"
        self.links = root / "links.json"
        self.sidecar = root / "forja_status.json"
        self.manual = root / "intervencoes_manuais.json"
        atomic_write_json(self.demands, {"schema": 1, "demandas": [{"id": "d1", "titulo": "Um"}, {"id": "d2", "titulo": "Dois"}]})
        atomic_write_json(self.links, {"schemaVersion": 1, "links": {}})
        atomic_write_json(self.sidecar, {"schemaVersion": 1, "revision": 0, "updatedAt": None, "items": {}})
        atomic_write_json(self.manual, {"schema": 1, "items": {}})
        self.cases = []
        for demand_id in ("d1", "d2"):
            case = root / f"case-{demand_id}"
            case.mkdir()
            initialize_case(case, demand_id=demand_id)
            self.cases.append(case)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_sidecar_does_not_modify_demands_and_is_idempotent(self) -> None:
        before = sha256_file(self.demands)
        _, state, _ = record_event(
            self.cases[0], "phase_started", expected_revision=1,
            idempotency_key="d1:f0:start", phase=PHASES[0],
        )
        first = sync_case(
            self.cases[0], sidecar_path=self.sidecar, demands_path=self.demands,
            links_path=self.links, apply=True, record_sync_event=False,
        )
        second = sync_case(
            self.cases[0], sidecar_path=self.sidecar, demands_path=self.demands,
            links_path=self.links, apply=True, record_sync_event=False,
        )
        self.assertTrue(first["changed"])
        self.assertFalse(second["changed"])
        self.assertEqual(before, sha256_file(self.demands))
        self.assertEqual(1, read_json(self.sidecar)["revision"])

    def test_replay_copy_is_ignored_by_automatic_bridge(self) -> None:
        result = sync_after_event(self.cases[0], {"eventSeq": 1})
        self.assertEqual("ignored_noncanonical", result["status"])

    def test_two_cases_are_not_lost_under_concurrency(self) -> None:
        outcomes = []

        def worker(case: Path) -> None:
            outcomes.append(sync_case(
                case, sidecar_path=self.sidecar, demands_path=self.demands,
                links_path=self.links, apply=True, record_sync_event=False,
            ))

        threads = [threading.Thread(target=worker, args=(case,)) for case in self.cases]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        self.assertEqual(2, len(outcomes))
        self.assertEqual({"d1", "d2"}, set(read_json(self.sidecar)["items"]))

    def test_batch_reconcile_skips_cases_outside_office_management(self) -> None:
        external_root = Path(self.temp.name) / "external-root"
        external = external_root / "case-personal"
        external.mkdir(parents=True)
        initialize_case(external, demand_id="personal-demand")
        with (
            patch("sync_forja_gestao.STATE_ROOT", external_root),
            patch("sync_forja_gestao.DEMANDS", self.demands),
            patch("sync_forja_gestao.LINKS", self.links),
        ):
            result = reconcile(apply=False, sidecar_path=self.sidecar)
        skipped = {item["caseId"]: item["reason"] for item in result["skipped"]}
        self.assertTrue(result["ok"])
        self.assertIn("case-personal", skipped)
        self.assertEqual("fora do escopo da gestão do escritório", skipped["case-personal"])

    def test_dashboard_join_marks_unlinked_demand_not_run(self) -> None:
        sync_case(
            self.cases[0], sidecar_path=self.sidecar, demands_path=self.demands,
            links_path=self.links, apply=True, record_sync_event=False,
        )
        snapshot = {
            "demandas": read_json(self.demands),
            "forja": read_json(self.sidecar),
        }
        enriched = enrich_snapshot(snapshot, Path(self.temp.name))
        items = {item["id"]: item for item in enriched["demandas"]["demandas"]}
        self.assertEqual("queued", items["d1"]["forja"]["lifecycleStatus"])
        self.assertEqual("not_run", items["d2"]["forja"]["lifecycleStatus"])

    def test_legacy_reconcile_is_read_only_and_never_overwrites_n3(self) -> None:
        legacy_root = Path(self.temp.name)
        legacy_case = legacy_root / "case-legacy-d1"
        legacy_case.mkdir(parents=True)
        atomic_write_json(legacy_case / "FORJA_STATE.json", {
            "currentPhase": "F9_PACOTE_REVISAO_DRAFT_OPCIONAL",
            "status": "draft_awaiting_review",
            "updatedAt": "2026-07-09T10:00:00-03:00",
            "inputs": {"demandId": "d1"},
            "artifacts": [],
            "phaseHistory": [],
        })
        before = sha256_file(self.demands)
        first = reconcile_legacy(
            apply=True,
            sidecar_path=self.sidecar,
            demands_path=self.demands,
            state_root=legacy_root,
        )
        self.assertEqual(1, first["changed"])
        self.assertEqual("N2.0-compat", read_json(self.sidecar)["items"]["d1"]["version"])
        sync_case(
            self.cases[0], sidecar_path=self.sidecar, demands_path=self.demands,
            links_path=self.links, apply=True, record_sync_event=False,
        )
        second = reconcile_legacy(
            apply=True,
            sidecar_path=self.sidecar,
            demands_path=self.demands,
            state_root=legacy_root,
        )
        self.assertEqual(0, second["changed"])
        self.assertEqual("N3.0-r2", read_json(self.sidecar)["items"]["d1"]["version"])
        self.assertEqual(before, sha256_file(self.demands))

    def test_legacy_reconcile_repairs_noncanonical_n3_sidecar_entry(self) -> None:
        legacy_root = Path(self.temp.name) / "legacy-repair"
        legacy_case = legacy_root / "case-legacy-d1"
        legacy_case.mkdir(parents=True)
        atomic_write_json(legacy_case / "FORJA_STATE.json", {
            "currentPhase": "F8_COMPOSICAO_VISUAL_QA",
            "status": "draft_awaiting_review",
            "updatedAt": "2026-07-09T11:00:00-03:00",
            "inputs": {"demandId": "d1"},
            "artifacts": [],
            "phaseHistory": [],
        })
        sidecar = read_json(self.sidecar)
        sidecar["items"]["d1"] = {
            "version": "N3.0-r2",
            "caseId": "case-replay-copy",
            "demandId": "d1",
            "eventRevision": 1,
        }
        atomic_write_json(self.sidecar, sidecar)
        result = reconcile_legacy(
            apply=True,
            sidecar_path=self.sidecar,
            demands_path=self.demands,
            state_root=legacy_root,
        )
        self.assertEqual(1, result["changed"])
        repaired = read_json(self.sidecar)["items"]["d1"]
        self.assertEqual("N2.0-compat", repaired["version"])
        self.assertEqual("case-legacy-d1", repaired["caseId"])

    def test_manual_audit_overlay_replaces_stale_legacy_delivery_without_touching_state(self) -> None:
        legacy_root = Path(self.temp.name) / "legacy-overlay"
        legacy_case = legacy_root / "case-legacy-d1"
        legacy_case.mkdir(parents=True)
        state_path = legacy_case / "FORJA_STATE.json"
        atomic_write_json(state_path, {
            "currentPhase": "F0_RECONCILIACAO_FILA",
            "status": "pending",
            "updatedAt": "2026-07-08T10:00:00-03:00",
            "inputs": {"demandId": "d1"},
            "artifacts": [],
            "phaseHistory": [],
            "deliveryEvidence": {"status": "sent_confirmed", "detail": "e-mail de outro caso"},
        })
        artifact = Path(self.temp.name) / "produto.pdf"
        artifact.write_bytes(b"audited")
        atomic_write_json(self.manual, {
            "schema": 1,
            "items": {
                "d1": {
                    "updatedAt": "2026-07-10T12:00:00-03:00",
                    "forja": {
                        "lifecycleStatus": "ready_for_review",
                        "phaseCursor": "F9_PACOTE_REVISAO",
                        "completedPhases": ["F7_AUDITORIA", "F8_QA_VISUAL", "F9_PACOTE_REVISAO"],
                        "nextAction": "Revisar o produto.",
                        "visualQa": {"reviewed": 2, "total": 2, "status": "pass"},
                        "artifacts": [{"path": str(artifact)}],
                        "deliveryEvidence": None,
                    },
                },
            },
        })
        before = sha256_file(state_path)
        result = reconcile_legacy(
            apply=True,
            sidecar_path=self.sidecar,
            demands_path=self.demands,
            state_root=legacy_root,
            manual_path=self.manual,
        )
        self.assertEqual(1, result["changed"])
        current = read_json(self.sidecar)["items"]["d1"]
        self.assertEqual("N3.0-manual-audit", current["version"])
        self.assertEqual("ready_for_review", current["lifecycleStatus"])
        self.assertIsNone(current["deliveryEvidence"])
        self.assertEqual({"reviewed": 2, "total": 2, "status": "pass"}, current["visualQa"])
        self.assertTrue(current["artifacts"][0]["exists"])
        self.assertEqual(before, sha256_file(state_path))

    def test_manual_audit_overlay_also_wins_over_canonical_n3_sidecar(self) -> None:
        artifact = Path(self.temp.name) / "produto-n4.pdf"
        artifact.write_bytes(b"audited-n4")
        atomic_write_json(self.manual, {
            "schema": 1,
            "items": {
                "d1": {
                    "updatedAt": "2026-07-21T12:00:00-03:00",
                    "forja": {
                        "overrideCanonicalN3": True,
                        "lifecycleStatus": "blocked",
                        "phaseCursor": "F10_RECONCILIACAO_GESTAO",
                        "completedPhases": ["F7_AUDITORIA", "F8_QA_VISUAL", "F9_PACOTE_REVISAO"],
                        "blockers": ["Insumo externo pendente."],
                        "nextAction": "Obter o insumo externo.",
                        "visualQa": {"reviewed": 24, "total": 24, "status": "pass"},
                        "artifacts": [{"path": str(artifact)}],
                        "deliveryEvidence": None,
                    },
                },
            },
        })
        state_before = sha256_file(self.cases[0] / "FORJA_N3_STATE.json")
        result = sync_case(
            self.cases[0], sidecar_path=self.sidecar, demands_path=self.demands,
            links_path=self.links, manual_path=self.manual, apply=True,
            record_sync_event=False,
        )
        current = read_json(self.sidecar)["items"]["d1"]
        self.assertTrue(result["changed"])
        self.assertEqual("N3.0-manual-audit", current["version"])
        self.assertEqual("blocked", current["lifecycleStatus"])
        self.assertEqual({"reviewed": 24, "total": 24, "status": "pass"}, current["visualQa"])
        self.assertEqual("queued", current["legacySnapshot"]["lifecycleStatus"])
        self.assertIsNone(current["deliveryEvidence"])
        self.assertEqual(state_before, sha256_file(self.cases[0] / "FORJA_N3_STATE.json"))

    def test_management_evidence_closes_a_stale_legacy_queue(self) -> None:
        payload = read_json(self.demands)
        payload["demandas"][0].update({
            "status": "cumprida",
            "respondidoComConteudo": True,
            "evidenciaResposta": "E-mail enviado abc123 com o documento solicitado.",
            "evidenciaTipo": "email",
        })
        atomic_write_json(self.demands, payload)
        legacy_root = Path(self.temp.name) / "legacy-management"
        legacy_case = legacy_root / "case-legacy-d1"
        legacy_case.mkdir(parents=True)
        atomic_write_json(legacy_case / "FORJA_STATE.json", {
            "currentPhase": "F0_RECONCILIACAO_FILA",
            "status": "pending",
            "updatedAt": "2026-07-08T10:00:00-03:00",
            "inputs": {"demandId": "d1"},
            "artifacts": [],
            "phaseHistory": [],
            "deliveryEvidence": {"status": "none", "detail": "sem entrega"},
        })
        result = reconcile_legacy(
            apply=True,
            sidecar_path=self.sidecar,
            demands_path=self.demands,
            state_root=legacy_root,
            manual_path=self.manual,
        )
        self.assertEqual(1, result["changed"])
        current = read_json(self.sidecar)["items"]["d1"]
        self.assertEqual("N3.0-management", current["version"])
        self.assertEqual("fulfilled_by_reconciliation", current["lifecycleStatus"])
        self.assertEqual("management_verified", current["deliveryEvidence"]["status"])

    def test_fulfilled_management_only_demand_gets_explicit_sidecar_state(self) -> None:
        payload = read_json(self.demands)
        payload["demandas"][0].update({
            "status": "cumprida",
            "respondidoComConteudo": True,
            "evidenciaResposta": "Registro administrativo verificado.",
        })
        atomic_write_json(self.demands, payload)
        empty_state_root = Path(self.temp.name) / "no-forja-state"
        empty_state_root.mkdir()
        result = reconcile_legacy(
            apply=True,
            sidecar_path=self.sidecar,
            demands_path=self.demands,
            state_root=empty_state_root,
            manual_path=self.manual,
        )
        self.assertEqual(1, result["candidates"])
        current = read_json(self.sidecar)["items"]
        self.assertIn("d1", current)
        self.assertNotIn("d2", current)
        self.assertEqual("management_reconciliation", current["d1"]["mode"])

    def test_dashboard_surfaces_management_forja_status_conflict(self) -> None:
        # Cumprida SEM evidência + FORJA aberta => conflito (regra vigente:
        # cumprida COM evidência é reconciliável, não conflito — ver caso abaixo).
        payload = read_json(self.demands)
        payload["demandas"][0].update({"status": "cumprida"})
        atomic_write_json(self.demands, payload)
        sidecar = read_json(self.sidecar)
        sidecar["items"]["d1"] = {
            "version": "N2.0-compat",
            "caseId": "case-d1",
            "demandId": "d1",
            "lifecycleStatus": "queued",
            "deliveryEvidence": None,
            "artifacts": [],
        }
        atomic_write_json(self.sidecar, sidecar)
        enriched = enrich_snapshot({"demandas": payload, "forja": sidecar}, Path(self.temp.name))
        item = next(value for value in enriched["demandas"]["demandas"] if value["id"] == "d1")
        codes = {issue["code"] for issue in item["derived"]["quality"]["issues"]}
        self.assertIn("forja_status_conflict", codes)
        self.assertEqual(1, enriched["insights"]["forjaStatusConflicts"])

if __name__ == "__main__":
    unittest.main(verbosity=2)
