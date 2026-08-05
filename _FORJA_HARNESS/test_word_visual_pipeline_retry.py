import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


TOOLS = Path(__file__).resolve().parents[1] / "_FERRAMENTAS"
sys.path.insert(0, str(TOOLS))
import word_visual_pipeline  # noqa: E402


class WordPdfRetryTests(unittest.TestCase):
    def test_transient_failure_retries_and_promotes_atomically(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "origem.docx"
            output = Path(temp) / "saída final.pdf"
            source.write_bytes(b"docx")
            output.write_bytes(b"pdf anterior")
            calls = []

            def converter(_, target):
                calls.append(target)
                if len(calls) == 1:
                    Path(target).write_bytes(b"parcial")
                    raise RuntimeError("RPC transitório")
                Path(target).write_bytes(b"pdf novo")

            with (
                patch.object(word_visual_pipeline, "_docx_para_pdf_once", side_effect=converter),
                patch.object(word_visual_pipeline.time, "sleep", return_value=None),
            ):
                word_visual_pipeline.docx_para_pdf(str(source), str(output))
            self.assertEqual(2, len(calls))
            self.assertEqual(b"pdf novo", output.read_bytes())

    def test_permanent_failure_preserves_previous_pdf(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "origem.docx"
            output = Path(temp) / "saída.pdf"
            source.write_bytes(b"docx")
            output.write_bytes(b"pdf anterior")
            with (
                patch.object(word_visual_pipeline, "_docx_para_pdf_once", side_effect=RuntimeError("falha")),
                patch.object(word_visual_pipeline.time, "sleep", return_value=None),
            ):
                with self.assertRaises(RuntimeError):
                    word_visual_pipeline.docx_para_pdf(str(source), str(output))
            self.assertEqual(b"pdf anterior", output.read_bytes())


if __name__ == "__main__":
    unittest.main()
