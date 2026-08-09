"""Regressão do detector de tribunal do F3 (`forja_sources`).

Origem: em 09/08/2026 três casos estavam há 37 horas fora da fila com
`TRIBUNAL_NAO_IDENTIFICADO`. Dois deles diziam o tribunal na primeira linha do
comando — um por sigla de recurso extraordinário com número, outro pelo nome do
STJ por extenso. O detector só sabia ler duas formas: sigla de recurso com
dígitos colados e número CNJ. Não sabia ler tribunal escrito por nome, e a regex
do RE era sensível a maiúscula e quebrava no ponto do milhar.

**Os fixtures preservam a FORMA do texto real e não os identificadores.** Nome de
cliente, número de processo e nome de pasta ficam no acervo; aqui entram
equivalentes neutros com a mesma anatomia — ponto de milhar no número, slug em
minúscula, separador `_`, sigla colada. É a anatomia que o detector lê, e é ela
que precisa estar sob regressão. Por isso também não há CNJ literal no arquivo:
a fronteira motor/acervo reprova qualquer um, e o número é montado em `_cnj`.
"""

import unittest

from forja_sources import (
    GATES_DESTE_MODULO, classificar_produto, detectar_tribunal, merge_gates,
    nomes_de_tribunal,
)


def _cnj(segmento: str, tr: str) -> str:
    """CNJ montado em tempo de execução — literal no motor reprova na fronteira."""
    return f"0001234-56.2020.{segmento}.{tr}.7100"


# Mesma anatomia dos comandos que produziram o bloqueio, com dados neutros.
CMD_RE_COM_PONTO = (
    "_demanda_whatsapp_re_1234567_2026-07-19\n"
    "whatsapp-titular-re1234567-20260719\n"
    "Reconstruir a tese do RE 1.234.567/PR, com rastreabilidade documental "
    "perante o STF."
)
CMD_SO_NOME = (
    "WhatsApp Audio - peça humana e prevenção - 2026-07-08\n"
    "whatsapp-audio-prevencao-20260708\n"
    "Conferir a prevenção do relator no STJ antes de protocolar a manifestação."
)
CMD_SEM_MARCADOR = (
    "_forja_reconstrucao_geral_2026-08-03\n"
    "manual-reconstrucao-geral-20260803\n"
    "Reconstruir a linha do tempo geral do caso e a memória de cálculo."
)


class TestDeteccaoTribunal(unittest.TestCase):
    def test_re_com_ponto_de_milhar_e_slug_minusculo(self):
        """O caso que ficou 37h parado: 'RE 1.234.567/PR' e pasta '_re_1234567_'."""
        tribunal, criterio = detectar_tribunal(CMD_RE_COM_PONTO)
        self.assertEqual(tribunal, "STF")
        self.assertIn("recurso extraordinário", criterio)

    def test_re_sem_pontuacao_continua_detectado(self):
        self.assertEqual(detectar_tribunal("RE 1234567")[0], "STF")

    def test_tribunal_apenas_nomeado(self):
        """Nenhuma sigla de recurso, nenhum CNJ — só a palavra STJ no comando."""
        tribunal, criterio = detectar_tribunal(CMD_SO_NOME)
        self.assertEqual(tribunal, "STJ")
        self.assertIn("nomeado", criterio)

    def test_nome_por_extenso(self):
        self.assertEqual(
            detectar_tribunal("Manifestação ao Supremo Tribunal Federal")[0], "STF")
        self.assertEqual(
            detectar_tribunal("Petição ao Superior Tribunal de Justiça")[0], "STJ")

    def test_dois_tribunais_nomeados_nao_decidem(self):
        """Duas menções de foro, nenhuma citação: aí sim é ambiguidade, e o
        detector não escolhe uma — continua bloqueado, dizendo por quê."""
        tribunal, motivo = detectar_tribunal(
            "Manifestação a protocolar no STF e petição paralela no STJ.")
        self.assertIsNone(tribunal)
        self.assertIn("ambíguo", motivo)
        self.assertIn("STF", motivo)
        self.assertIn("STJ", motivo)

    def test_ausencia_de_marcador_tem_motivo_proprio(self):
        """Ausência e ambiguidade pedem diligências diferentes; não se colapsam."""
        tribunal, motivo = detectar_tribunal(CMD_SEM_MARCADOR)
        self.assertIsNone(tribunal)
        self.assertIn("nenhum marcador", motivo)

    def test_sigla_de_recurso_vence_nome_citado(self):
        """AgInt no REsp tramita no STJ mesmo citando o STF na fundamentação."""
        self.assertEqual(
            detectar_tribunal("AgInt no REsp 1.111.222 — cita o STF")[0], "STJ")

    def test_cnj_vence_nome_citado(self):
        tribunal, criterio = detectar_tribunal(
            f"{_cnj('4', '04')} — memorial que discute tese do STJ")
        self.assertEqual(tribunal, "TRF4")
        self.assertIn("CNJ", criterio)

    def test_trf_e_tj_nomeados(self):
        self.assertEqual(detectar_tribunal("peça ao TRF-4")[0], "TRF4")
        self.assertEqual(
            detectar_tribunal("Tribunal Regional Federal da 1ª Região")[0], "TRF1")
        self.assertEqual(detectar_tribunal("agravo no TJRS")[0], "TJRS")
        self.assertEqual(detectar_tribunal("recurso no TJ-DF")[0], "TJDFT")

    def test_tema_repetitivo_nao_fixa_foro(self):
        """Falso positivo real, pego na medição antes de o conserto ser aceito:
        dois pareceres consultivos que só mencionam 'Tema 1.410 do STJ'."""
        texto = ("Parecer consultivo — diretrizes para conclusão\n"
                 "distinções necessárias na utilização dos Temas 1.410 e 1.326 do STJ;")
        self.assertEqual(nomes_de_tribunal(texto), set())
        self.assertIsNone(detectar_tribunal(texto)[0])

    def test_outras_formas_de_citacao_tambem_nao_fixam_foro(self):
        for trecho in ("Súmula 7 do STJ", "jurisprudência consolidada do STF",
                       "acórdão paradigma do TRF-4", "entendimento firmado no TJSP",
                       "julgado sob repercussão geral no STF"):
            with self.subTest(trecho=trecho):
                self.assertEqual(nomes_de_tribunal(trecho), set())

    def test_mencao_como_foro_sobrevive_ao_filtro(self):
        """O filtro não pode engolir a menção legítima na mesma peça."""
        texto = "Manifestação a ser protocolada no STJ, que aplica a Súmula 7 do STJ."
        self.assertEqual(nomes_de_tribunal(texto), {"STJ"})

    def test_nomes_de_tribunal_nao_casa_dentro_de_palavra(self):
        """Guarda contra o falso positivo óbvio: sigla colada em outra palavra."""
        self.assertEqual(nomes_de_tribunal("estj stfa tjxx"), set())


class TestProdutoDeclaradoNaoProtocolavel(unittest.TestCase):
    """Regimento de tribunal não se aplica a documento que não vai a protocolo.

    Caso real: um plano interno de negociação declarava na seção de limites que
    "o material não é peça protocolável", e mesmo assim caía em `indefinido` e
    exigia regimento — gerando um P0 que nada podia resolver, porque não há
    tribunal a identificar num documento que não será protocolado. A declaração
    expressa da casa vence a heurística.
    """

    def test_declaracao_expressa_dispensa_regimento(self):
        for frase in ("O material não é peça protocolável.",
                      "Este documento não constitui peça judicial.",
                      "O produto não será protocolado.",
                      "Material não protocolável, de uso interno."):
            with self.subTest(frase=frase):
                produto, obrigatorio = classificar_produto(
                    "Plano interno para a reunião\n" + frase)
                self.assertEqual(produto, "produto_interno_nao_protocolavel")
                self.assertFalse(obrigatorio)

    def test_peca_de_verdade_continua_exigindo_regimento(self):
        """A contraprova: a declaração é rara e específica, não vale por tema."""
        produto, obrigatorio = classificar_produto(
            "Elaborar memoriais para o agravo interno, a serem protocolados no STJ")
        self.assertEqual(produto, "peca_judicial")
        self.assertTrue(obrigatorio)

    def test_mencao_a_protocolo_sem_negativa_nao_dispensa(self):
        produto, obrigatorio = classificar_produto(
            "Recurso a ser protocolado até sexta; conferir a peça protocolável")
        self.assertTrue(obrigatorio)


class TestGateNaoEhCicatriz(unittest.TestCase):
    def test_modulo_e_dono_dos_proprios_gates(self):
        """O P0 antigo tem de sair quando a execução nova não o reproduz."""
        antigos = [
            {"code": "TRIBUNAL_NAO_IDENTIFICADO", "severity": "P0", "detail": "velho"},
            {"code": "FONTE_PREVALENTE_NAO_VALIDADA", "severity": "P0", "detail": "de outro módulo"},
        ]
        sobrevivem = [g for g in antigos if g["code"] not in GATES_DESTE_MODULO]
        merged = merge_gates(sobrevivem, [])
        codes = {g["code"] for g in merged}
        self.assertNotIn("TRIBUNAL_NAO_IDENTIFICADO", codes)
        self.assertIn("FONTE_PREVALENTE_NAO_VALIDADA", codes)


if __name__ == "__main__":
    unittest.main()
