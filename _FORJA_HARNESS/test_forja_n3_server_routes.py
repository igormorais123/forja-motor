import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPTS = Path(__file__).resolve().parents[1] / "gestao_escritorio" / "scripts"
sys.path.insert(0, str(SCRIPTS))
import server  # noqa: E402


class ForjaServerRouteTests(unittest.TestCase):
    def test_artifact_with_spaces_and_accents_resolves_by_id_and_hash(self):
        harness = Path(__file__).resolve().parent
        with tempfile.TemporaryDirectory(dir=harness) as temp:
            state_root = Path(temp) / "state"
            case_dir = state_root / "case-rota-acentos"
            package_dir = case_dir / "packages" / "pkg-123"
            package_dir.mkdir(parents=True)
            artifact = package_dir / "Peça final com acentos.pdf"
            artifact.write_bytes(b"conteudo controlado")
            digest = hashlib.sha256(artifact.read_bytes()).hexdigest()
            manifest = {
                "packageId": "pkg-123",
                "attachments": [{
                    "artifactId": "peticao_pdf",
                    "packagePath": str(artifact),
                    "sha256": digest,
                }],
            }
            (case_dir / "FORJA_PACKAGE.json").write_text(
                json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
            with patch.object(server, "FORJA_STATE_ROOT", state_root):
                resolved_case, loaded = server.Handler._forja_package(case_dir.name)
                entry = server.Handler._artifact_entry(loaded, "peticao_pdf")
                resolved = server.Handler._verified_artifact_path(entry)
            self.assertEqual(case_dir.resolve(), resolved_case)
            self.assertEqual(artifact.resolve(), resolved)

    def test_tampered_artifact_is_rejected(self):
        harness = Path(__file__).resolve().parent
        with tempfile.TemporaryDirectory(dir=harness) as temp:
            artifact = Path(temp) / "arquivo.pdf"
            artifact.write_bytes(b"alterado")
            with self.assertRaises(ValueError):
                server.Handler._verified_artifact_path({
                    "path": str(artifact),
                    "sha256": "0" * 64,
                })

    def test_manual_audit_artifact_resolves_without_package(self):
        harness = Path(__file__).resolve().parent
        with tempfile.TemporaryDirectory(dir=harness) as temp:
            root = Path(temp)
            artifact = root / "Parecer auditado.pdf"
            artifact.write_bytes(b"produto n3")
            digest = hashlib.sha256(artifact.read_bytes()).hexdigest()
            sidecar = root / "forja_status.json"
            sidecar.write_text(json.dumps({
                "schemaVersion": 1,
                "items": {
                    "d1": {
                        "caseId": "case-manual-audit",
                        "artifacts": [{
                            "artifactId": "manual-1",
                            "path": str(artifact),
                            "sha256": digest,
                            "exists": True,
                        }],
                    },
                },
            }), encoding="utf-8")
            with patch.object(server, "FORJA_STATUS", sidecar):
                entry = server.Handler._sidecar_artifact("case-manual-audit", "manual-1")
                resolved = server.Handler._verified_artifact_path(entry)
            self.assertEqual(artifact.resolve(), resolved)

    def test_n4_artifact_resolves_only_from_catalog_and_current_hash(self):
        harness = Path(__file__).resolve().parent
        with tempfile.TemporaryDirectory(dir=harness) as temp:
            state_root = Path(temp) / "state"
            artifact = state_root / "case-n4-route" / "n4_artifacts" / "F2_QUESTION_TREE.json"
            artifact.parent.mkdir(parents=True)
            artifact.write_text('{"schemaVersion":1}', encoding="utf-8")
            with patch.object(server, "FORJA_STATE_ROOT", state_root):
                entry = server.Handler._n4_artifact("case-n4-route", "F2_QUESTION_TREE.json")
                resolved = server.Handler._verified_artifact_path(entry)
                rejected = server.Handler._n4_artifact("case-n4-route", "FORJA_CASE_MANIFEST.json")
            self.assertEqual(artifact.resolve(), resolved)
            self.assertIsNone(rejected)


if __name__ == "__main__":
    unittest.main()
