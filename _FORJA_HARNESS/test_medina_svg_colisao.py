# -*- coding: utf-8 -*-
"""Regressão do gate de desenho do SVG (SVGC-01..05).

Estrutura deliberada, aprendida no gate F8-S: o teste-âncora (um desenho bom
não pode reprovar) vale tanto quanto os de mutação (um desenho quebrado tem de
reprovar). Sem o âncora, aperta-se o limiar até o gate reprovar produção boa;
sem as mutações, afrouxa-se até ele não achar nada.

O caso real de 03/08/2026 está aqui como fixture verbatim: é o diagrama que o
Igor reprovou na conferência e que TODOS os gates anteriores aprovaram.
"""
import sys
import unittest
from pathlib import Path

FORJA = Path(__file__).resolve().parent
sys.path.insert(0, str(FORJA.parent / "_FERRAMENTAS"))

from medina_svg_colisao import analisar  # noqa: E402

# Recorte verbatim de `fig2_obices_convergentes.svg` (peça CASO-16, aprovada
# em 09/07/2026). O <rect> do fecho é pintado DEPOIS das caixas inferiores e
# cobre o texto delas; e o fill do rótulo vem sem "#".
DEFEITO_REAL = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 371.3 224">
<rect x="20.0" y="155.0" width="160.0" height="80.0" fill="#EFF4F3" stroke="#395C60"/>
<text x="100.0" y="187.0" font-family="Segoe UI" font-size="9" font-weight="normal" fill="#49494D" text-anchor="middle">Lei imperativa:</text>
<text x="100.0" y="197.0" font-family="Segoe UI" font-size="9" font-weight="normal" fill="#49494D" text-anchor="middle">art. 25, &#167;2&#186;</text>
<rect x="105.7" y="177.0" width="160.0" height="35.0" fill="#395C60" stroke="none"/>
<text x="185.7" y="192.0" font-family="Segoe UI" font-size="10" font-weight="bold" fill="ffffff" text-anchor="middle">NAO CONHECIMENTO</text>
</svg>"""

# Mesma figura com as duas correções: fecho reposicionado abaixo das caixas e
# cor do rótulo válida.
CORRIGIDO = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 371.3 260">
<rect x="20.0" y="155.0" width="160.0" height="80.0" fill="#EFF4F3" stroke="#395C60"/>
<text x="100.0" y="187.0" font-family="Segoe UI" font-size="9" font-weight="normal" fill="#49494D" text-anchor="middle">Lei imperativa:</text>
<text x="100.0" y="197.0" font-family="Segoe UI" font-size="9" font-weight="normal" fill="#49494D" text-anchor="middle">art. 25, &#167;2&#186;</text>
<rect x="105.7" y="242.0" width="160.0" height="35.0" fill="#395C60" stroke="none"/>
<text x="185.7" y="262.0" font-family="Segoe UI" font-size="10" font-weight="bold" fill="#ffffff" text-anchor="middle">NAO CONHECIMENTO</text>
</svg>"""

# Rótulo em negrito seguido de frase corrida no MESMO <text>. Não é colisão: os
# tspans correm lado a lado. Foi o único falso positivo da primeira medição no
# acervo e por isso virou teste.
TSPAN_EM_FLUXO = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 60">
<text x="20" y="30" font-family="Times" font-size="12" fill="#2C3E50"><tspan font-weight="bold">Fase de conhecimento. </tspan><tspan>Dever de indenizar transitado em julgado</tspan></text>
</svg>"""


def codigos(svg_texto, gravidade=None):
    laudo = analisar(texto=svg_texto)
    return [a["codigo"] for a in laudo["achados"]
            if gravidade is None or a["gravidade"] == gravidade]


class TesteGateDesenhoSVG(unittest.TestCase):

    def test_caso_real_reprovado(self):
        """O diagrama que passou por todos os gates e o dono reprovou."""
        laudo = analisar(texto=DEFEITO_REAL)
        self.assertFalse(laudo["aprovado"])
        self.assertIn("SVGC-01", codigos(DEFEITO_REAL, "bloqueia"))
        self.assertIn("SVGC-04", codigos(DEFEITO_REAL, "bloqueia"))

    def test_correcao_do_caso_real_aprova(self):
        """Contraprova: corrigidos os dois defeitos, o gate libera.

        Sem esta metade o teste acima seria satisfeito por um gate que reprova
        tudo."""
        laudo = analisar(texto=CORRIGIDO)
        self.assertTrue(laudo["aprovado"], laudo["achados"])

    def test_tspan_em_fluxo_nao_e_colisao(self):
        self.assertNotIn("SVGC-02", codigos(TSPAN_EM_FLUXO))

    def test_important_no_style_nao_e_cor_invalida(self):
        svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 50">'
               '<rect x="0" y="0" width="50" height="20" style="fill:#e8f1ef !important"/>'
               '</svg>')
        self.assertNotIn("SVGC-04", codigos(svg))

    def test_texto_sobre_texto(self):
        svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 60">'
               '<text x="20" y="30" font-size="10" fill="#000">Resolucao 69</text>'
               '<text x="24" y="31" font-size="10" fill="#900">ALTA</text></svg>')
        self.assertIn("SVGC-02", codigos(svg, "bloqueia"))

    def test_forma_transparente_nao_oculta(self):
        """Retângulo só de borda (fill=none) por cima do texto é moldura, não
        oclusão — é assim que as caixas da casa emolduram conteúdo."""
        svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 60">'
               '<text x="20" y="30" font-size="10" fill="#000">texto emoldurado</text>'
               '<rect x="10" y="10" width="180" height="40" fill="none" stroke="#395C60"/>'
               '</svg>')
        self.assertNotIn("SVGC-01", codigos(svg))

    def test_ordem_importa(self):
        """Forma ANTES do texto é fundo; DEPOIS é oclusão. Só a ordem muda."""
        forma = '<rect x="10" y="10" width="180" height="40" fill="#395C60"/>'
        txt = '<text x="20" y="30" font-size="10" fill="#ffffff">rotulo</text>'
        cab = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 60">'
        self.assertNotIn("SVGC-01", codigos(cab + forma + txt + "</svg>"))
        self.assertIn("SVGC-01", codigos(cab + txt + forma + "</svg>", "bloqueia"))

    def test_paleta_aprovada_nao_reprova_por_contraste(self):
        """Terracota sobre painel terra dá 2,3:1 e é identidade da casa desde
        09/07 — calibrar na WCAG reprovaria o padrão do escritório."""
        svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 60">'
               '<rect x="0" y="0" width="200" height="60" fill="#FBF2EC"/>'
               '<text x="20" y="30" font-size="9" fill="#D9926A">Sumula 7</text></svg>')
        self.assertNotIn("SVGC-05", codigos(svg))

    def test_transform_nao_suportado_e_declarado(self):
        """Rotação não é analisada. O laudo diz isso em vez de aprovar por
        omissão — silêncio sobre o que não se mediu é como se fabrica atestado
        sem lastro."""
        svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 60">'
               '<g transform="rotate(30)"><text x="20" y="30" font-size="10">x</text></g>'
               '</svg>')
        self.assertTrue(analisar(texto=svg)["naoAnalisados"])

    def test_geradores_do_kit_passam(self):
        """Os geradores programáticos não conseguem produzir esta falha —
        empilham na vertical com altura calculada. Se um dia conseguirem, este
        teste cai antes da peça sair."""
        import tempfile
        import medina_svg_kit as kit
        with tempfile.TemporaryDirectory() as tmp:
            alvo = str(Path(tmp) / "crono.svg")
            kit.cronologia(alvo, [
                ("27/05/2005", "Assinatura do contrato de concessao"),
                ("2005-2007", "Execucao das obras contratadas"),
                ("14/03/2024", "Decisao que reconheceu o desequilibrio"),
            ], largura_cm=13.1, titulo="Cronologia")
            self.assertTrue(analisar(alvo)["aprovado"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
