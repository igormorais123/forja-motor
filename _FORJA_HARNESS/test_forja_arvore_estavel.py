# -*- coding: utf-8 -*-
"""Regressão do terceiro estado do baseline: verde ≠ instável ≠ vermelho.

Origem medida em 10/08/2026. Duas suítes que varrem a árvore reprovaram dentro
da bateria e passaram sozinhas minutos depois. A explicação que escrevi primeiro
— "a bateria renderiza peça na própria árvore" — foi desmentida por fotografia:
dos 30.866 arquivos, **nenhum `.docx` ou `.pdf` mudou** durante uma execução
completa. O que mudou foi obra de **outra sessão do agente trabalhando na mesma
pasta**, incluindo um módulo do motor alterado e um teste novo aparecendo no
meio da corrida, que leva quase nove minutos.

Por isso o conserto não está nas suítes: nada nelas impede a pasta de mudar
debaixo delas. Está na bateria, que passa a distinguir "não deu para saber" de
"quebrou".

O que estes testes protegem é a **salvaguarda**, não a conveniência. Repetir
verde não basta para ser instável: a árvore precisa ter mexido. Sem isso, a
regra viraria "roda de novo até passar", que é o modo clássico de esconder
falha intermitente de verdade.
"""

import tempfile
import unittest
from pathlib import Path

import forja_arvore_estavel as arvore
import forja_baseline


class TestImpressaoDaArvore(unittest.TestCase):
    def test_arquivo_novo_e_alterado_aparecem(self):
        with tempfile.TemporaryDirectory() as tmp:
            raiz = Path(tmp)
            (raiz / "a.txt").write_text("um", encoding="utf-8")
            antes = arvore.impressao(raiz)
            (raiz / "b.txt").write_text("dois", encoding="utf-8")
            (raiz / "a.txt").write_text("um mais longo", encoding="utf-8")
            d = arvore.mexeu(antes, arvore.impressao(raiz))
        self.assertTrue(d["mexeu"])
        self.assertEqual((d["novos"], d["mudados"], d["sumidos"]), (1, 1, 0))

    def test_arvore_parada_nao_acusa_movimento(self):
        """Contraprova: sem esta, `mexeu` poderia devolver True sempre e a regra
        inteira viraria 'roda de novo até passar'."""
        with tempfile.TemporaryDirectory() as tmp:
            raiz = Path(tmp)
            (raiz / "a.txt").write_text("um", encoding="utf-8")
            antes = arvore.impressao(raiz)
            d = arvore.mexeu(antes, arvore.impressao(raiz))
        self.assertFalse(d["mexeu"])
        self.assertEqual(d["total"], 0)

    def test_ruido_de_execucao_fica_de_fora(self):
        """Telemetria e cache mudam a cada corrida; contá-los faria toda execução
        parecer instável, que é o mesmo que não medir instabilidade nenhuma."""
        with tempfile.TemporaryDirectory() as tmp:
            raiz = Path(tmp)
            (raiz / "telemetria").mkdir()
            (raiz / "__pycache__").mkdir()
            antes = arvore.impressao(raiz)
            (raiz / "telemetria" / "BASELINE_x.json").write_text("{}", encoding="utf-8")
            (raiz / "__pycache__" / "m.pyc").write_bytes(b"x")
            (raiz / "z.log").write_text("linha", encoding="utf-8")
            d = arvore.mexeu(antes, arvore.impressao(raiz))
        self.assertFalse(d["mexeu"], d["amostra"])

    def test_amostra_nao_se_passa_por_lista_completa(self):
        with tempfile.TemporaryDirectory() as tmp:
            raiz = Path(tmp)
            antes = arvore.impressao(raiz)
            for n in range(30):
                (raiz / f"f{n}.txt").write_text("x", encoding="utf-8")
            d = arvore.mexeu(antes, arvore.impressao(raiz), limite=5)
        self.assertEqual(len(d["amostra"]), 5)
        self.assertEqual(d["total"], 30)


class TestTerceiroEstado(unittest.TestCase):
    """A reavaliação da suíte vermelha, com as duas metades da regra."""

    def _reavaliar(self, primeira_verde, segunda_verde, arvore_mexeu):
        chamadas = {"n": 0}

        def _segunda(nome, papel=""):
            chamadas["n"] += 1
            return {"suite": nome, "familia": "script", "verde": segunda_verde,
                    "resumo": "segunda leitura"}

        real_script, real_pytest = forja_baseline._script, forja_baseline._pytest
        real_impressao, real_mexeu = arvore.impressao, arvore.mexeu
        forja_baseline._script = _segunda
        forja_baseline._pytest = lambda nome: _segunda(nome)
        arvore.impressao = lambda raiz=None: {}
        arvore.mexeu = lambda a, b, limite=12: {
            "mexeu": arvore_mexeu, "total": 3 if arvore_mexeu else 0,
            "novos": 3 if arvore_mexeu else 0, "sumidos": 0, "mudados": 0,
            "amostra": ["x.md"] if arvore_mexeu else []}
        try:
            return forja_baseline._reavaliar_se_a_arvore_mexeu(
                {"suite": "t.py", "familia": "script", "verde": primeira_verde,
                 "resumo": "primeira", "papel": "p"}), chamadas["n"]
        finally:
            forja_baseline._script, forja_baseline._pytest = real_script, real_pytest
            arvore.impressao, arvore.mexeu = real_impressao, real_mexeu

    def test_vermelha_que_repete_verde_com_arvore_mexida_e_instavel(self):
        item, _ = self._reavaliar(False, True, True)
        self.assertTrue(item["instavel"])
        self.assertFalse(item["verde"], "instável não pode virar verde")

    def test_vermelha_que_repete_verde_com_arvore_parada_continua_vermelha(self):
        """A metade que impede 'roda de novo até passar': falha intermitente com
        a pasta parada é problema da suíte, e continua sendo reprovação."""
        item, _ = self._reavaliar(False, True, False)
        self.assertFalse(item.get("instavel"))
        self.assertFalse(item["verde"])

    def test_vermelha_duas_vezes_continua_vermelha_mesmo_com_arvore_mexida(self):
        item, _ = self._reavaliar(False, False, True)
        self.assertFalse(item.get("instavel"))
        self.assertFalse(item["verde"])

    def test_verde_nao_e_relida(self):
        """Reler as 122 suítes verdes dobraria a bateria por nada."""
        item, chamadas = self._reavaliar(True, True, True)
        self.assertEqual(chamadas, 0)
        self.assertTrue(item["verde"])


class TestVeredito(unittest.TestCase):
    def _relatorio(self, suites):
        vermelhas = [s for s in suites if not s["verde"] and not s.get("instavel")]
        instaveis = [s for s in suites if s.get("instavel")]
        return {"aprovado": not vermelhas and not instaveis,
                "inconclusivo": bool(instaveis) and not vermelhas}

    def test_instavel_sozinho_nao_aprova_e_e_inconclusivo(self):
        r = self._relatorio([{"verde": True}, {"verde": False, "instavel": True}])
        self.assertFalse(r["aprovado"])
        self.assertTrue(r["inconclusivo"])

    def test_vermelha_junto_de_instavel_ainda_e_reprovacao(self):
        """Instabilidade não pode encobrir quebra de verdade na mesma corrida."""
        r = self._relatorio([{"verde": False}, {"verde": False, "instavel": True}])
        self.assertFalse(r["aprovado"])
        self.assertFalse(r["inconclusivo"])


if __name__ == "__main__":
    unittest.main()
