import json
import sys
import tempfile
import unittest
from datetime import date, datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import dashboard_enrichment  # noqa: E402
import gmail_gws_update  # noqa: E402
import hermes_bridge  # noqa: E402
import hermes_office_panel_remote  # noqa: E402
import office_io  # noqa: E402
import office_application  # noqa: E402
import server  # noqa: E402


class PersistenceTests(unittest.TestCase):
    def test_atomic_json_replaces_valid_document(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "state.json"
            office_io.atomic_write_json(path, {"ok": True, "texto": "acentuação"})
            self.assertEqual(json.loads(path.read_text(encoding="utf-8"))["texto"], "acentuação")
            self.assertEqual(list(path.parent.glob("*.tmp")), [])

    def test_read_only_snapshot_does_not_touch_demand_file(self):
        before = server.DATA.stat().st_mtime_ns
        payload = server.snapshot()
        after = server.DATA.stat().st_mtime_ns
        self.assertIn("demandas", payload)
        self.assertEqual(before, after)


class GmailExtractionTests(unittest.TestCase):
    def test_deadline_prefers_delivery_context_over_judgment_date(self):
        email_date = date.today() + timedelta(days=1)
        deadline = date.today() + timedelta(days=8)
        judgment = date.today() + timedelta(days=30)
        text = (
            f"Data do email: {email_date:%d/%m/%Y}. "
            f"Prazo interno para encaminhar a minuta até {deadline:%d/%m/%Y}. "
            f"Julgamento em {judgment:%d/%m/%Y}."
        )
        self.assertEqual(gmail_gws_update.extract_deadline(text), deadline.isoformat())

    def test_date_without_deadline_context_is_not_promoted(self):
        mentioned = date.today() + timedelta(days=10)
        self.assertIsNone(gmail_gws_update.extract_deadline(f"Reunião realizada em {mentioned:%d/%m/%Y}."))


class EnrichmentTests(unittest.TestCase):
    def test_quality_flags_missing_operational_links(self):
        item = {
            "id": "x",
            "titulo": "Teste",
            "origem": "manual",
            "status": "aberta",
            "pasta": "Pasta inexistente",
            "local": {"folderExists": False, "comandoMd": False},
            "anexos": {"externosPendentes": True},
        }
        enriched = dashboard_enrichment.enrich_item(item, ROOT.parent)
        codes = {issue["code"] for issue in enriched["derived"]["quality"]["issues"]}
        self.assertTrue({"missing_folder", "missing_command", "missing_deadline", "external_attachments"}.issubset(codes))

    def test_verified_management_delivery_suppresses_stale_forja_conflict(self):
        item = {
            "id": "entregue",
            "titulo": "Peça entregue",
            "status": "cumprida",
            "evidenciaResposta": "E-mail enviado ao escritório.",
        }
        forja = {"lifecycleStatus": "blocked", "deliveryEvidence": {"status": "manual_override"}}
        enriched = dashboard_enrichment.enrich_item(item, ROOT.parent, forja)
        codes = {issue["code"] for issue in enriched["derived"]["quality"]["issues"]}
        self.assertNotIn("forja_status_conflict", codes)
        self.assertNotIn("forja_delivery_conflict", codes)


class HermesBridgeContractTests(unittest.TestCase):
    def test_snapshot_exposes_only_open_items_as_actionable(self):
        snapshot = hermes_bridge.build_snapshot({
            "demandas": [
                {"id": "aberta", "titulo": "Concluir minuta", "status": "aberta", "origem": "email"},
                {"id": "entregue", "titulo": "Protocolar", "status": "cumprida", "origem": "email", "evidenciaResposta": "enviada ao escritório"},
            ]
        })
        self.assertEqual(snapshot["schema"], 2)
        self.assertEqual([item["id"] for item in snapshot["actionableItems"]], ["aberta"])
        self.assertTrue(snapshot["authority"]["factoryResponsibilityEndsOnDeliveryToOffice"])
        self.assertFalse(snapshot["authority"]["protocolOrReceiptRequiredFromIgor"])

    def test_remote_heartbeat_fails_closed_when_snapshot_is_stale(self):
        old = (datetime.now(timezone.utc) - timedelta(hours=4)).isoformat()
        health = hermes_office_panel_remote.snapshot_health({"updatedAt": old, "freshness": {"maxAgeMinutes": 180}})
        self.assertTrue(health["stale"])


class ProductContractTests(unittest.TestCase):
    def test_health_contract_is_fast_and_structured(self):
        health = server.health_payload()
        self.assertTrue(health["ok"])
        self.assertEqual(health["version"], "2.0.0")
        self.assertIn("integrations", health)
        self.assertIn("critical48h", health["counts"])

    def test_generated_panel_contains_all_operational_views(self):
        html = (ROOT / "painel_gestao_escritorio.html").read_text(encoding="utf-8")
        for marker in ("Visão de hoje", "Mapa de prazos", "Demandas", "Integrações e continuidade", "Entregas ao Fábio"):
            self.assertIn(marker, html)
        self.assertIn("O painel nunca exibe conversa bruta", html)

    def test_launcher_uses_lightweight_health_endpoint(self):
        launcher = (ROOT.parent / "ABRIR_GESTAO_ESCRITORIO.html").read_text(encoding="utf-8")
        self.assertIn("/api/health", launcher)
        self.assertIn("/api/update", launcher)
        self.assertIn("iniciar_painel_gestao_escritorio.ps1", launcher)

    def test_whatsapp_pairing_has_guided_recovery_without_chat_content(self):
        html = (ROOT / "painel_gestao_escritorio.html").read_text(encoding="utf-8")
        source = (SCRIPTS / "server.py").read_text(encoding="utf-8")
        self.assertIn("Parear WhatsApp", html)
        self.assertIn('"/api/whatsapp-pair"', source)
        self.assertNotIn("conversationBody", html)

    def test_whatsapp_sanitized_export_separates_direction_and_media_materialization(self):
        source = (SCRIPTS / "update_dashboard_local.ps1").read_text(encoding="utf-8")
        self.assertIn("for r in incoming:", source)
        self.assertIn("'audioPathRecordedWindow': len(audio_with_path)", source)
        self.assertIn("'audioMaterializedWindow': len(audio_materialized)", source)
        self.assertIn("'audioMissingMediaWindow': len(audio_missing)", source)
        self.assertIn("'incomingMediaMissingWindow': len(incoming_media_missing)", source)
        self.assertIn("Midia registrada sem arquivo acessivel nao pode ser tratada como lida", source)

    def test_completion_is_blocked_while_material_inputs_are_pending(self):
        item = {
            "id": "pendente",
            "status": "aberta",
            "anexos": {"externosPendentes": True, "diretosEsperados": 3, "diretosBaixados": 2},
        }
        blockers = server.completion_blockers(item)
        self.assertEqual(len(blockers), 2)
        self.assertTrue(any("mídias externas" in blocker for blocker in blockers))
        self.assertTrue(any("2 de 3" in blocker for blocker in blockers))

    def test_completion_gate_accepts_resolved_inputs(self):
        item = {
            "id": "pronta",
            "status": "aberta",
            "anexos": {"externosPendentes": False, "diretosEsperados": 3, "diretosBaixados": 3},
        }
        self.assertEqual(server.completion_blockers(item), [])

    def test_http_server_reexports_the_application_rule(self):
        self.assertIs(server.completion_blockers, office_application.completion_blockers)


if __name__ == "__main__":
    unittest.main()
