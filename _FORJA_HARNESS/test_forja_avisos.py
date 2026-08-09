"""Regressão da caixa de avisos — o metro entre detectar e alguém saber.

Âncora real: os embargos de declaração de 07/08/2026 num precedente que o titular
usaria numa negociação. O vigia do STF os detectou às 09h00 de 08/08, gravou a
linha no log de novidades e ninguém leu; o titular soube em 09/08 por outra via.
Nada estava quebrado — o vigia leu, comparou hash, detectou e datou. Faltava
destinatário.

Os dois defeitos que estes testes trancam:

1. o aviso morava num log que ninguém tinha razão de abrir;
2. o log só registrava a novidade, então a execução seguinte dizia "sem
   movimento novo" e a informação saía de vista sozinha, sem ninguém tê-la lido.

Por isso a propriedade central aqui não é depositar: é **permanecer**. Um aviso
não visto continua não visto por quantas leituras houver, e só sai da caixa por
ciência nominada.
"""

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import mock

import forja_avisos as fa


class BaseCaixa(unittest.TestCase):
    def setUp(self):
        self._tmp = TemporaryDirectory()
        self.caixa = Path(self._tmp.name) / "AVISOS.json"
        self._patch = mock.patch.object(fa, "CAIXA", self.caixa)
        self._patch.start()

    def tearDown(self):
        self._patch.stop()
        self._tmp.cleanup()

    def dep(self, chave="c1", **kw):
        base = dict(origem="monitor_stf", chave=chave, titulo="movimento novo",
                    detalhe="Petição 99.875", caso="caso-x")
        base.update(kw)
        return fa.depositar(**base)


class TestPermanencia(BaseCaixa):
    def test_aviso_nao_some_por_ser_lido_muitas_vezes(self):
        """O defeito nº 2: imprimir não é dar ciência."""
        self.dep()
        for _ in range(5):
            self.assertEqual(len(fa.pendentes()), 1)
            fa.linhas_para_contexto()
        self.assertEqual(len(fa.pendentes()), 1)

    def test_execucao_sem_novidade_nao_apaga_o_pendente(self):
        """O vigia rodar de novo e não achar nada não é ciência do que achou antes."""
        self.dep()
        # nenhuma chamada a depositar nesta "execução": nada de novo lá fora
        self.assertEqual(len(fa.pendentes()), 1)

    def test_so_sai_por_ciencia_nominada(self):
        a = self.dep()
        fa.dar_ciencia(a["id"], por="fulano", nota="avisado por e-mail")
        self.assertEqual(fa.pendentes(), [])
        guardado = json.loads(self.caixa.read_text(encoding="utf-8"))["avisos"][0]
        self.assertEqual(guardado["estado"], "visto")
        self.assertEqual(guardado["vistoPor"], "fulano")
        self.assertEqual(guardado["nota"], "avisado por e-mail")

    def test_ciencia_sem_nome_e_recusada_no_cli(self):
        a = self.dep()
        self.assertEqual(fa.main(["--visto", a["id"]]), 2)
        self.assertEqual(len(fa.pendentes()), 1)


class TestIdempotencia(BaseCaixa):
    def test_repetir_o_deposito_nao_duplica(self):
        """O vigia roda de hora em hora; a caixa não pode virar ruído."""
        a = self.dep()
        b = self.dep()
        self.assertEqual(a["id"], b["id"])
        self.assertEqual(len(fa.carregar()["avisos"]), 1)

    def test_reaparecer_nao_reabre_o_que_ja_foi_visto(self):
        a = self.dep()
        fa.dar_ciencia(a["id"], por="fulano")
        self.dep()
        self.assertEqual(fa.pendentes(), [])

    def test_chaves_diferentes_sao_avisos_diferentes(self):
        self.dep(chave="c1")
        self.dep(chave="c2")
        self.assertEqual(len(fa.pendentes()), 2)

    def test_mesma_chave_em_origens_diferentes_nao_colide(self):
        self.dep(chave="c1", origem="monitor_stf")
        self.dep(chave="c1", origem="monitor_djen")
        self.assertEqual(len(fa.pendentes()), 2)


class TestOrdemEContexto(BaseCaixa):
    def test_urgente_vem_primeiro(self):
        self.dep(chave="normal", urgencia="media")
        self.dep(chave="grave", urgencia="alta")
        self.assertEqual(fa.pendentes()[0]["chave"], "grave")

    def test_urgencia_invalida_e_recusada(self):
        with self.assertRaises(ValueError):
            self.dep(urgencia="altíssima")

    def test_contexto_vazio_quando_nao_ha_nada(self):
        """Caixa limpa não polui o começo da sessão."""
        self.assertEqual(fa.linhas_para_contexto(), [])

    def test_contexto_mostra_titulo_id_e_como_dar_ciencia(self):
        a = self.dep(urgencia="alta")
        texto = "\n".join(fa.linhas_para_contexto())
        self.assertIn(a["id"], texto)
        self.assertIn("movimento novo", texto)
        self.assertIn("URGENTE", texto)
        self.assertIn("--visto", texto)

    def test_contexto_declara_quantos_ficaram_de_fora(self):
        for i in range(12):
            self.dep(chave=f"c{i}")
        texto = "\n".join(fa.linhas_para_contexto(limite=3))
        self.assertIn("+9 outro(s)", texto)


class TestClassificacaoDeGravidade(unittest.TestCase):
    def test_movimento_decisorio_e_urgente(self):
        from forja_monitor_stf import _movimento_grave
        for m in ("07/08/2026 · Petição · Embargos de Declaração - Petição: 99875",
                  "16/07/2026 · Provido · Decisão monocrática",
                  "14/10/2025 · Acórdão · Embargos recebidos",
                  "12/02/2026 · Transitado em julgado"):
            with self.subTest(m=m):
                self.assertTrue(_movimento_grave(m))

    def test_movimento_de_expediente_nao_e_urgente(self):
        """Marcar tudo como urgente é o mesmo que não marcar nada."""
        from forja_monitor_stf import _movimento_grave
        for m in ("30/03/2026 · Petição · Procuração/Substabelecimento",
                  "12/02/2026 · Remessa · à GERÊNCIA DE RECEBIMENTO",
                  "25/02/2026 · Conclusos ao(à) Relator(a)"):
            with self.subTest(m=m):
                self.assertFalse(_movimento_grave(m))


class TestCaixaCorrompidaNaoDerruba(BaseCaixa):
    def test_json_invalido_vira_caixa_vazia_em_vez_de_excecao(self):
        """O hook de sessão é fail-open; a caixa não pode ser o que o derruba."""
        self.caixa.parent.mkdir(parents=True, exist_ok=True)
        self.caixa.write_text("{isto não é json", encoding="utf-8")
        self.assertEqual(fa.carregar()["avisos"], [])
        self.assertEqual(fa.linhas_para_contexto(), [])
        a = self.dep()
        self.assertEqual(len(fa.pendentes()), 1)
        self.assertTrue(a["id"])


if __name__ == "__main__":
    unittest.main()


# ---------------------------------------------------------------------------
# Conferir a fiação do vigia não pode custar um aviso permanente (09/08/2026).
#
# A caixa só esvazia por ciência nominada — é essa permanência que a faz
# funcionar. O efeito colateral apareceu no mesmo dia: três avisos de processo
# inventado, deixados por uma verificação de fiação, viraram a primeira coisa
# que toda sessão lia. Caixa que abre com ruído de teste deixa de ser lida, que
# é exatamente o que ela veio corrigir.
# ---------------------------------------------------------------------------

class TestVigiaSemAviso(unittest.TestCase):
    def _rodar(self, avisar):
        """Executa `verificar` dos dois vigias contra fixture, sem rede."""
        import forja_monitor_djen as djen
        import forja_monitor_stf as stf

        depositados = []
        caixa_falsa = types.ModuleType("forja_avisos")
        caixa_falsa.depositar = lambda **kw: depositados.append(kw)

        with tempfile.TemporaryDirectory() as tmp:
            destino = Path(tmp)
            with mock.patch.dict(sys.modules, {"forja_avisos": caixa_falsa}), \
                 mock.patch.object(djen, "DESTINO", destino), \
                 mock.patch.object(stf, "DESTINO", destino), \
                 mock.patch.object(djen, "consultar", lambda *a, **k: [
                     {"id": "1", "data": "2026-08-01", "tipo": "Intimação",
                      "resumo": "pauta", "urgente": True}]), \
                 mock.patch.object(stf, "consultar",
                                   lambda *a, **k: (["Embargos de declaração"], "sha")):
                # Primeira leitura nunca gera novidade: é o retrato inicial.
                djen.verificar("x", {"tribunal": "TRF3", "numero": "1"}, avisar=avisar)
                stf.verificar("y", {"incidente": "1", "rotulo": "r", "porque": "p"},
                              avisar=avisar)
                # Segunda leitura, com o retrato mudado, é o que dispara.
                with mock.patch.object(djen, "consultar", lambda *a, **k: [
                        {"id": "2", "data": "2026-08-09", "tipo": "Intimação",
                         "resumo": "acórdão", "urgente": True},
                        {"id": "1", "data": "2026-08-01", "tipo": "Intimação",
                         "resumo": "pauta", "urgente": True}]), \
                     mock.patch.object(stf, "consultar", lambda *a, **k: (
                         ["Transitado em julgado", "Embargos de declaração"], "sha2")):
                    djen.verificar("x", {"tribunal": "TRF3", "numero": "1"}, avisar=avisar)
                    stf.verificar("y", {"incidente": "1", "rotulo": "r", "porque": "p"},
                                  avisar=avisar)
        return depositados

    def test_por_padrao_o_vigia_deposita(self):
        """A contraprova: sem ela, `--sem-aviso` poderia estar sempre ligado."""
        origens = {d["origem"] for d in self._rodar(avisar=True)}
        self.assertEqual(origens, {"monitor_djen", "monitor_stf"})

    def test_com_sem_aviso_nada_chega_na_caixa(self):
        self.assertEqual(self._rodar(avisar=False), [])
