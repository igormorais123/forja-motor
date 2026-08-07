# -*- coding: utf-8 -*-
"""Regressão do despacho multimodelo da FORJA.

Nenhum teste aqui chama modelo de verdade: o despacho é substituído por um
duplo. Suíte que gasta dinheiro do titular a cada execução não roda no
baseline, e suíte que não roda não protege nada.
"""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import forja_modelos as fm


def duplo(conteudo: str, entrada: int = 100, saida: int = 200, raciocinio: int = 0):
    def _despacho(modelo, prompt, sistema, max_tokens, timeout):
        _despacho.max_tokens = max_tokens
        return conteudo, entrada, saida, raciocinio
    return _despacho


class RegistroTests(unittest.TestCase):
    def test_toda_familia_tem_revisor_de_outra_familia(self):
        for modelo_id in fm.MODELOS:
            with self.subTest(modelo=modelo_id):
                revisores = fm.revisores_de(modelo_id)
                self.assertTrue(revisores)
                familia = fm.familia_de(modelo_id)
                for revisor in revisores:
                    self.assertNotEqual(familia, fm.familia_de(revisor))

    def test_kimi_k2_esta_vedado_por_decisao_do_titular(self):
        self.assertTrue(fm.MODELOS_PROIBIDOS)
        for proibido in fm.MODELOS_PROIBIDOS:
            self.assertIn("kimi-k2", proibido)
        remotos = {m.remoto for m in fm.MODELOS.values()}
        self.assertFalse(remotos & fm.MODELOS_PROIBIDOS)

    def test_novo_sufixo_kimi_k2_tambem_e_vedado(self):
        futuro = fm.Modelo(
            id="k2-futuro", familia="moonshot", provedor="openrouter",
            remoto="moonshotai/kimi-k2.99-future", forte_em=(), fases=("F5",),
        )
        fm.MODELOS[futuro.id] = futuro
        self.addCleanup(lambda: fm.MODELOS.pop(futuro.id, None))
        with self.assertRaises(fm.ForjaModeloError) as ctx:
            fm.chamar(futuro.id, "não deve sair", registrar=False)
        self.assertIn("vedado", str(ctx.exception))

    def test_modelo_fora_do_registro_nao_e_chamado(self):
        with self.assertRaises(fm.ForjaModeloError):
            fm.chamar("gpt-4o", "oi", registrar=False)

    def test_modelo_local_nao_sai_por_http(self):
        for local in ("opus-5", "fable-5", "sol-5.6"):
            with self.subTest(modelo=local), self.assertRaises(fm.ForjaModeloError) as ctx:
                fm.chamar(local, "oi", registrar=False)
            self.assertIn("assinatura", str(ctx.exception))

    def test_cada_fase_do_registro_tem_pelo_menos_um_modelo(self):
        for modelo in fm.MODELOS.values():
            for fase in modelo.fases:
                with self.subTest(fase=fase):
                    self.assertIn(modelo.id, fm.modelos_da_fase(fase))

    def test_kimi_k3_so_volta_como_voz_e_nunca_como_fonte(self):
        """O K3 voltou ao registro em 07/08/2026, por ordem do titular.

        Ele havia sido retirado em 26/07 por reprovar a bancada jurídica, e
        este teste afirmava a ausência. A ordem nova o reinstala **como ponto
        de vista curto**, não como trabalhador da esteira — então o que o teste
        precisa guardar deixou de ser "não está no registro" e passou a ser o
        motivo pelo qual ele saiu: 0 de 6 na condição solta, com 4 invenções.

        Enfraquecer isto para `assertIn("kimi-k3-cursor", MODELOS)` apagaria a
        medição. O que se afere é a restrição, as fases em que ele pode falar,
        e que a rota antiga (paga, sem restrição declarada) não voltou junto.
        """
        self.assertNotIn("kimi-k3", fm.MODELOS)
        self.assertNotIn("kimi-k3-assinatura", fm.MODELOS)
        k3 = fm.MODELOS["kimi-k3-cursor"]
        self.assertIn("nao_afirma_fato", k3.restricoes)
        self.assertEqual(k3.provedor, "cursor")
        self.assertEqual(set(k3.fases), {"F4", "F7"})
        # Nenhum modelo com `nao_afirma_fato` pode estar nas fases em que a
        # esteira colhe fonte oficial e confere citação.
        for modelo in fm.MODELOS.values():
            if "nao_afirma_fato" in modelo.restricoes:
                with self.subTest(modelo=modelo.id):
                    self.assertNotIn("F5", modelo.fases)
                    self.assertNotIn("F3", modelo.fases)


class ConteudoVazioTests(unittest.TestCase):
    """O defeito medido: modelo que raciocina devolve vazio e a integração segue."""

    def setUp(self):
        self._original = dict(fm.DESPACHO)
        self.addCleanup(lambda: fm.DESPACHO.update(self._original))

    def test_resposta_vazia_levanta_em_vez_de_virar_string_vazia(self):
        fm.DESPACHO["openrouter"] = duplo("", entrada=139, saida=400, raciocinio=400)
        with self.assertRaises(fm.ForjaModeloError) as ctx:
            fm.chamar("sol-5.6-api", "pergunta", registrar=False)
        self.assertIn("raciocínio", str(ctx.exception))

    def test_resposta_so_de_espaco_tambem_levanta(self):
        fm.DESPACHO["openrouter"] = duplo("   \n  ")
        with self.assertRaises(fm.ForjaModeloError):
            fm.chamar("grok-4.5", "pergunta", registrar=False)

    def test_modelo_que_raciocina_recebe_piso_de_tokens(self):
        stub = duplo("resposta")
        fm.DESPACHO["openrouter"] = stub
        fm.chamar("sol-5.6-api", "pergunta", max_tokens=200, registrar=False)
        self.assertGreaterEqual(stub.max_tokens, fm.MODELOS["sol-5.6-api"].min_tokens)

    def test_modelo_sem_raciocinio_respeita_o_teto_pedido(self):
        stub = duplo("resposta")
        fm.DESPACHO["openrouter"] = stub
        fm.chamar("grok-4.5", "pergunta", max_tokens=200, registrar=False)
        self.assertEqual(200, stub.max_tokens)


class OrcamentoTests(unittest.TestCase):
    def setUp(self):
        self._original = dict(fm.DESPACHO)
        self.addCleanup(lambda: fm.DESPACHO.update(self._original))
        fm.DESPACHO["openrouter"] = duplo("resposta", entrada=1000, saida=2000)

    def test_custo_e_calculado_pela_tabela_do_provedor(self):
        # 1.000 entrada a US$ 2/M + 2.000 saída a US$ 6/M
        self.assertAlmostEqual(0.014, fm.custo_usd(fm.MODELOS["grok-4.5"], 1000, 2000), places=6)

    def test_gasto_acumula_no_orcamento(self):
        orc = fm.Orcamento(teto_usd=1.0)
        fm.chamar("grok-4.5", "p", orcamento=orc, registrar=False)
        fm.chamar("grok-4.5", "p", orcamento=orc, registrar=False)
        self.assertEqual(2, len(orc.chamadas))
        self.assertAlmostEqual(0.028, orc.gasto_usd, places=5)

    def test_orcamento_esgotado_recusa_a_chamada(self):
        orc = fm.Orcamento(teto_usd=0.001)
        with self.assertRaises(fm.ForjaModeloError) as ctx:
            fm.chamar("grok-4.5", "p", max_tokens=2048, orcamento=orc, registrar=False)
        self.assertIn("restantes", str(ctx.exception))

    def test_chamada_acima_do_teto_unitario_e_recusada(self):
        with self.assertRaises(fm.ForjaModeloError) as ctx:
            fm.chamar("grok-4.5", "p" * 100, max_tokens=200_000, registrar=False)
        self.assertIn("teto", str(ctx.exception))


class LedgerTests(unittest.TestCase):
    def setUp(self):
        self._original = dict(fm.DESPACHO)
        self._ledger = fm.LEDGER
        self.addCleanup(lambda: fm.DESPACHO.update(self._original))
        self.addCleanup(lambda: setattr(fm, "LEDGER", self._ledger))
        self._dir = tempfile.TemporaryDirectory()
        self.addCleanup(self._dir.cleanup)
        fm.LEDGER = Path(self._dir.name) / "ledger.jsonl"
        fm.DESPACHO["openrouter"] = duplo("texto sensivel da peca", entrada=100, saida=200)

    def test_ledger_registra_custo_e_nao_conteudo(self):
        fm.chamar("grok-4.5", "pergunta", fase="F5", papel="proponente")
        linha = json.loads(fm.LEDGER.read_text(encoding="utf-8").strip())
        self.assertNotIn("conteudo", linha)
        self.assertNotIn("texto sensivel", json.dumps(linha, ensure_ascii=False))
        self.assertEqual(len("texto sensivel da peca"), linha["caracteresResposta"])
        self.assertEqual("F5", linha["fase"])
        self.assertEqual("xai", linha["familia"])

    def test_gasto_acumulado_soma_por_modelo(self):
        fm.chamar("grok-4.5", "p")
        fm.chamar("grok-4.5", "p")
        resumo = fm.gasto_acumulado()
        self.assertEqual(2, resumo["chamadas"])
        self.assertEqual(2, resumo["porModelo"]["grok-4.5"]["chamadas"])

    def test_ledger_e_append_only(self):
        fm.chamar("sol-5.6-api", "p")
        fm.chamar("grok-4.5", "p")
        self.assertEqual(2, len([x for x in fm.LEDGER.read_text(encoding="utf-8").splitlines() if x.strip()]))


class SegredoTests(unittest.TestCase):
    def test_erro_de_segredo_ausente_nao_vaza_valor(self):
        with self.assertRaises(fm.ForjaModeloError) as ctx:
            fm._segredo("CHAVE_QUE_NAO_EXISTE_NA_FORJA")
        self.assertIn("CHAVE_QUE_NAO_EXISTE_NA_FORJA", str(ctx.exception))
        self.assertNotIn("sk-", str(ctx.exception))


class ProvedorReportadoTests(unittest.TestCase):
    def test_openrouter_recusa_resposta_reportada_como_k2(self):
        payload = {
            "model": "moonshotai/kimi-k2.7-code",
            "choices": [{"message": {"content": "texto"}}],
            "usage": {},
        }
        with patch.object(fm, "_post", return_value=payload), \
                patch.object(fm, "_segredo", return_value="segredo-falso"):
            with self.assertRaises(fm.ForjaModeloError) as ctx:
                fm._openrouter(fm.MODELOS["grok-4.5"], "p", None, 2048, 10)
        self.assertIn("vedado", str(ctx.exception))


if __name__ == "__main__":
    unittest.main(verbosity=2)
