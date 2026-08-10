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


class _FakeDoc:
    def __init__(self):
        self.exportado = None

    def ExportAsFixedFormat(self, destino, *_args):  # noqa: N802
        Path(destino).write_bytes(b"pdf")
        self.exportado = destino

    def Close(self, *_args):  # noqa: N802
        pass


class _FakeWord:
    """Word de mentira que registra COMO o documento foi aberto."""

    def __init__(self, falhar_sem_reparo=False):
        self.aberturas = []
        self.falhar_sem_reparo = falhar_sem_reparo
        self.Documents = self
        self.Options = type("Opcoes", (), {})()
        self.Visible = None
        self.DisplayAlerts = None
        self.AutomationSecurity = None

    def Open(self, **kwargs):  # noqa: N802
        self.aberturas.append(kwargs)
        if self.falhar_sem_reparo and not kwargs.get("OpenAndRepair"):
            raise RuntimeError("arquivo pede reparo")
        return _FakeDoc()

    def Quit(self):  # noqa: N802
        pass


class ReparoSoQuandoPreciso(unittest.TestCase):
    """`OpenAndRepair=True` em toda abertura travou o Word em documento saudável.

    Em 10/08/2026 três propostas reais estouraram os 75 segundos do processo pai
    sempre no mesmo ponto, `document_open_started`. A mesma máquina abria os
    mesmos arquivos em 0,3 segundo sem o parâmetro — inclusive o original
    intocado, o que descartou defeito de conteúdo. O prejuízo não é o tempo: é o
    diagnóstico falso, que manda investigar o arquivo em vez da ferramenta.
    """

    def _rodar(self, word):
        import word_pdf_worker

        fake_pythoncom = type("M", (), {"CoInitialize": staticmethod(lambda: None),
                                        "CoUninitialize": staticmethod(lambda: None)})
        fake_client = type("M", (), {"DispatchEx": staticmethod(lambda _p: word)})
        fake_win32com = type("M", (), {"client": fake_client})
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            (base / "e.docx").write_bytes(b"docx")
            argv = ["w", str(base / "e.docx"), str(base / "s.pdf"),
                    str(base / "pid"), str(base / "status")]
            with (
                patch.dict(sys.modules, {"pythoncom": fake_pythoncom,
                                         "win32com": fake_win32com,
                                         "win32com.client": fake_client}),
                patch.object(sys, "argv", argv),
            ):
                codigo = word_pdf_worker.main()
            return codigo, (base / "status").read_text(encoding="ascii")

    def test_documento_saudavel_abre_sem_passar_pelo_reparo(self):
        word = _FakeWord()

        codigo, status = self._rodar(word)

        self.assertEqual(0, codigo)
        self.assertEqual(1, len(word.aberturas))
        self.assertNotIn("OpenAndRepair", word.aberturas[0])
        self.assertEqual("exported", status)

    def test_documento_que_falha_ainda_recebe_a_tentativa_de_reparo(self):
        word = _FakeWord(falhar_sem_reparo=True)

        codigo, _status = self._rodar(word)

        self.assertEqual(0, codigo)
        self.assertEqual(2, len(word.aberturas))
        self.assertNotIn("OpenAndRepair", word.aberturas[0])
        self.assertTrue(word.aberturas[1]["OpenAndRepair"])


if __name__ == "__main__":
    unittest.main()
