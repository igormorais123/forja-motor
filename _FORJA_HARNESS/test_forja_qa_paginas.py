# -*- coding: utf-8 -*-
"""Regressão do QA de páginas (M4.2 do plano 19).

DEVE_PEGAR: densidade anômala, página em branco no meio, conteúdo na borda.
NÃO_PODE_TRAVAR: documento normal em silêncio; 1ª página com rodapé
institucional isenta da checagem de borda; pastas reais aprovadas continuam
aprovadas. Roda com: python test_forja_qa_paginas.py
"""
import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw

from forja_qa_paginas import analisar_pasta

A4 = (827, 1169)  # ~100dpi


def _pagina(path: Path, linhas_texto: int = 30, extra=None):
    img = Image.new("RGB", A4, "white")
    d = ImageDraw.Draw(img)
    for i in range(linhas_texto):          # simula massa de texto
        y = 90 + i * 30
        d.rectangle([100, y, 700, y + 12], fill=(40, 40, 40))
    if extra:
        extra(d)
    img.save(path)


def _pasta(tmp: Path, especial: dict | None = None, n: int = 5) -> Path:
    """n páginas normais; `especial` = {indice: construtor}."""
    especial = especial or {}
    for i in range(n):
        path = tmp / f"p{i+1:02d}.png"
        if i in especial:
            especial[i](path)
        else:
            _pagina(path)
    return tmp


class DevePegar(unittest.TestCase):

    def test_densidade_anomala_detectada(self):
        def estourada(path):
            img = Image.new("RGB", A4, "white")
            d = ImageDraw.Draw(img)
            d.rectangle([30, 30, 800, 1100], fill=(60, 60, 120))  # diagrama gigante
            img.save(path)
        with tempfile.TemporaryDirectory() as tmp:
            r = analisar_pasta(_pasta(Path(tmp), {2: estourada}))
        self.assertTrue(any("densidade anômala" in a["problema"] and
                            a["pagina"] == "p03.png" for a in r["achados"]), r["achados"])

    def test_pagina_em_branco_no_meio(self):
        def branca(path):
            Image.new("RGB", A4, "white").save(path)
        with tempfile.TemporaryDirectory() as tmp:
            r = analisar_pasta(_pasta(Path(tmp), {2: branca}))
        self.assertTrue(any("em branco" in a["problema"] for a in r["achados"]))

    def test_conteudo_cortado_na_borda_inferior(self):
        def cortada(path):
            _pagina(path, extra=lambda d: d.rectangle(
                [100, A4[1] - 20, 700, A4[1]], fill=(30, 30, 30)))
        with tempfile.TemporaryDirectory() as tmp:
            r = analisar_pasta(_pasta(Path(tmp), {3: cortada}))
        self.assertTrue(any("borda inferior" in a["problema"] and
                            a["pagina"] == "p04.png" for a in r["achados"]))


class NaoPodeTravar(unittest.TestCase):

    def test_documento_normal_em_silencio(self):
        with tempfile.TemporaryDirectory() as tmp:
            r = analisar_pasta(_pasta(Path(tmp)))
        self.assertEqual(r["achados"], [])
        self.assertTrue(r["aprovado"])

    def test_rodape_institucional_na_pagina_1_e_isento(self):
        def com_rodape(path):
            _pagina(path, extra=lambda d: d.rectangle(
                [0, A4[1] - 25, A4[0], A4[1]], fill=(57, 92, 96)))  # faixa petróleo
        with tempfile.TemporaryDirectory() as tmp:
            r = analisar_pasta(_pasta(Path(tmp), {0: com_rodape}))
        self.assertFalse(any(a["pagina"] == "p01.png" for a in r["achados"]),
                         r["achados"])

    def test_ultima_pagina_curta_nao_e_pagina_em_branco(self):
        def curta(path):
            _pagina(path, linhas_texto=2)
        with tempfile.TemporaryDirectory() as tmp:
            r = analisar_pasta(_pasta(Path(tmp), {4: curta}))
        self.assertFalse(any("em branco" in a["problema"] for a in r["achados"]))

    def test_pasta_real_aprovada_continua_aprovada(self):
        real = Path("state/case-email-patricia-fabio-memoriais-19f3c68ee6d8fef2/"
                    "producao/paginas")
        if not real.is_dir():
            self.skipTest("pasta real indisponível")
        r = analisar_pasta(real)
        self.assertTrue(r["aprovado"], r["achados"])

    def test_pasta_vazia_nao_explode(self):
        with tempfile.TemporaryDirectory() as tmp:
            r = analisar_pasta(Path(tmp))
        self.assertEqual(r["paginas"], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
