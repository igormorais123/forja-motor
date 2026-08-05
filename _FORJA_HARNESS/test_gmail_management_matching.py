from __future__ import annotations

import sys
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "gestao_escritorio" / "scripts"
sys.path.insert(0, str(SCRIPTS))
from gmail_gws_update import repair_false_response_matches  # noqa: E402
from audit_delivered_docs import match_demands  # noqa: E402


def message(message_id: str, thread_id: str, subject: str) -> dict:
    return {
        "id": message_id,
        "threadId": thread_id,
        "payload": {"headers": [{"name": "Subject", "value": subject}]},
    }


class GmailManagementMatchingTests(unittest.TestCase):
    def test_cross_case_delivery_is_removed_from_whatsapp_demand(self) -> None:
        data = {"demandas": [{
            "id": "whatsapp-fabio",
            "origem": "whatsapp",
            "titulo": "WhatsApp Fabio Medina Osorio",
            "clienteOuCaso": "Fabio Medina Osorio",
            "pasta": "WhatsApp Fabio",
            "threadIds": ["thread-jalusa"],
            "emailsResposta": ["jalusa-1"],
            "respondidoComConteudo": True,
            "status": "cumprida",
            "evidenciaResposta": "E-mail da Jalusa.",
        }]}
        repaired = repair_false_response_matches(
            data,
            [message("jalusa-1", "thread-jalusa", "Re: Fotos enviadas por whatsapp cliente Jalusa")],
        )
        item = data["demandas"][0]
        self.assertEqual(1, repaired)
        self.assertEqual([], item["emailsResposta"])
        self.assertFalse(item["respondidoComConteudo"])
        self.assertEqual("aberta", item["status"])
        self.assertEqual("", item["evidenciaResposta"])

    def test_matching_email_thread_is_preserved(self) -> None:
        data = {"demandas": [{
            "id": "email-case",
            "origem": "email",
            "titulo": "Caso Mateus",
            "clienteOuCaso": "Mateus",
            "pasta": "Caso Mateus",
            "threadIds": ["thread-mateus"],
            "emailsResposta": ["mateus-1"],
            "respondidoComConteudo": True,
            "status": "cumprida",
            "evidenciaResposta": "Entrega correta.",
        }]}
        repaired = repair_false_response_matches(
            data,
            [message("mateus-1", "thread-mateus", "Re: Caso Mateus")],
        )
        self.assertEqual(0, repaired)
        self.assertEqual(["mateus-1"], data["demandas"][0]["emailsResposta"])

    def test_delivery_audit_does_not_match_generic_whatsapp_words(self) -> None:
        demands = [{
            "id": "roraima",
            "origem": "whatsapp_audio",
            "titulo": "Roraima senador - possível cliente",
            "clienteOuCaso": "Cliente de Roraima",
            "pasta": "WhatsApp Audio - Roraima Senador cliente",
            "emailsResposta": [],
            "threadIds": ["thread-jalusa"],
        }]
        result = match_demands(
            message("jalusa-1", "thread-jalusa", "Re: Fotos enviadas por whatsapp cliente Jalusa"),
            demands,
        )
        self.assertEqual([], result)


if __name__ == "__main__":
    unittest.main(verbosity=2)
