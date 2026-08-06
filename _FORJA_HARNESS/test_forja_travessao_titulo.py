# -*- coding: utf-8 -*-
"""Catraca da exceção de travessão em título de seção (G10-escrita-humana).

Origem: em 05/08/2026 o gate contava como "aparte explicativo" o travessão que o
compositor injeta ao numerar as seções ("I — CABIMENTO E TEMPESTIVIDADE"). O
efeito era invertido: quanto mais o autor seccionasse a peça, mais vício o gate
enxergava, embora o markdown auditado tivesse 3 travessões em 3.504 palavras.

A primeira exceção escrita para resolver isso era permissiva demais, e a revisão
cruzada com a outra família de modelo a quebrou no mesmo dia. Este arquivo
guarda as quebras que ela encontrou, mais duas de lavra própria, para que a
exceção não volte a virar escape. A última asserção é a contraprova: o padrão
legítimo da casa continua passando.
"""
import unittest

from forja_estilo_humano import _travessoes

ENCHIMENTO = " palavra" * 30
ROMANOS = ("I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII")


def _p0(texto: str) -> bool:
    return any(a["sev"] == "P0" for a in _travessoes(texto))


class ExcecaoDeTituloNumerado(unittest.TestCase):
    def test_romano_malformado_nao_escapa(self):
        """`[IVXLCDM]+` aceitava 'XXXXXXXXXXXXXX', que não é algarismo romano."""
        texto = "\n".join(f"XXXXXXXXXXXXXX — COISA {i}" for i in range(6)) + ENCHIMENTO
        self.assertTrue(_p0(texto))

    def test_romano_precedido_de_prosa_nao_escapa(self):
        """Olhar só o token anterior deixava passar prosa terminada em romano."""
        texto = "\n".join(f"Precedente VIII — Sem Fundamento numero {i}"
                          for i in range(6)) + ENCHIMENTO
        self.assertTrue(_p0(texto))

    def test_inciso_no_meio_da_frase_nao_escapa(self):
        """Inciso é a citação romana mais comum em peça, e não abre linha."""
        texto = "\n".join(f"o art. 489, § 1º, IV — O julgador enfrenta o ponto {i}"
                          for i in range(6)) + ENCHIMENTO
        self.assertTrue(_p0(texto))

    def test_aparte_explicativo_continua_reprovando(self):
        """O vício que o gate existe para pegar segue sendo pego."""
        texto = "\n".join(f"A tese {i} — que é assim — não vinga aqui"
                          for i in range(5)) + ENCHIMENTO
        self.assertTrue(_p0(texto))

    def test_titulo_de_secao_da_casa_passa(self):
        """Contraprova: reprovar o padrão aprovado seria defeito do gate."""
        texto = "\n".join(f"{r} — TITULO DA SECAO" for r in ROMANOS) + ENCHIMENTO
        self.assertFalse(_p0(texto))


if __name__ == "__main__":
    unittest.main(verbosity=2)
