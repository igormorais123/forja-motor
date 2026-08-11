# -*- coding: utf-8 -*-
"""Canário do varredor de fios: ele acusa o retorno que ficou sem resposta?

O defeito que o motivou foi um retorno do escritório sobre peça já entregue,
esperando resposta enquanto todos os gates diziam verde — porque a demanda que o
originou constava cumprida. O teste que importa é esse: chega mensagem da casa
depois da minha última resposta, e o varredor precisa acusar.

Sem rede: a consulta ao Gmail é substituída por um dublê. Sem cliente: os
endereços são inventados, porque a fronteira reprova o contrário.
"""
import unittest
from unittest import mock

import forja_fios_abertos as fios

CASA = ["exemplo.adv.br"]

# internalDate em milissegundos; os valores são arbitrários e só a ordem importa.
DELA = 1_700_000_200_000
MINHA = 1_700_000_100_000


def _msg(quem, quando, assunto="Assunto do caso", enviada=False):
    return {
        "internalDate": str(quando),
        "labelIds": ["SENT"] if enviada else ["INBOX"],
        "payload": {"headers": [{"name": "From", "value": quem},
                                {"name": "Subject", "value": assunto}]},
    }


def _dubles(threads):
    """Devolve uma função no lugar de _pegar, servindo a lista e cada fio."""
    def pegar(url, tk):
        if "/threads?" in url:
            return {"threads": [{"id": k} for k in threads]}
        chave = url.split("/threads/")[1].split("?")[0]
        return {"messages": threads[chave]}
    return pegar


class CanarioDosFiosAbertos(unittest.TestCase):
    def setUp(self):
        p = mock.patch.object(fios, "_token", return_value="fingido")
        p.start()
        self.addCleanup(p.stop)

    def _rodar(self, threads, decisoes=None):
        with mock.patch.object(fios, "_pegar", side_effect=_dubles(threads)):
            return fios.abertos(CASA, decisoes=decisoes)

    def test_resposta_minha_depois_da_dela_fecha_o_fio(self):
        r = self._rodar({"t1": [_msg("adv@exemplo.adv.br", MINHA - 100),
                                _msg("eu@gmail.com", MINHA, enviada=True)]})
        self.assertEqual(r, [])

    def test_retorno_depois_da_minha_resposta_abre_o_fio(self):
        """O caso que motivou o varredor: a peça foi entregue e ela voltou revisada."""
        r = self._rodar({"t1": [_msg("adv@exemplo.adv.br", MINHA - 100),
                                _msg("eu@gmail.com", MINHA, enviada=True),
                                _msg("adv@exemplo.adv.br", DELA,
                                     assunto="Re: memoriais — versão V3")]})
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0]["thread"], "t1")
        self.assertFalse(r[0]["nuncaRespondi"])
        # O rótulo do fio é o assunto da primeira mensagem, não o do "Re:" que
        # reabriu — é assim que o escritório procura o caso.
        self.assertEqual(r[0]["assunto"], "Assunto do caso")

    def test_fio_nunca_respondido_e_marcado_como_tal(self):
        r = self._rodar({"t1": [_msg("adv@exemplo.adv.br", DELA)]})
        self.assertTrue(r[0]["nuncaRespondi"])
        self.assertIsNone(r[0]["minhaUltima"])

    def test_mensagem_de_fora_da_casa_nao_abre_fio(self):
        r = self._rodar({"t1": [_msg("eu@gmail.com", MINHA, enviada=True),
                                _msg("newsletter@outro.com", DELA)]})
        self.assertEqual(r, [])

    def test_ordena_do_mais_recente_para_o_mais_antigo(self):
        r = self._rodar({
            "antigo": [_msg("adv@exemplo.adv.br", DELA - 10_000_000, assunto="antigo")],
            "novo": [_msg("adv@exemplo.adv.br", DELA, assunto="novo")],
        })
        self.assertEqual([f["assunto"] for f in r], ["novo", "antigo"])

    def test_decisao_posterior_encerra_sem_exigir_resposta_artificial(self):
        resolvido = "2023-11-14T23:00:01+00:00"  # posterior a DELA
        r = self._rodar(
            {"t1": [_msg("adv@exemplo.adv.br", DELA)]},
            decisoes={"t1": {"resolvedAt": resolvido, "reason": "ciência"}},
        )
        self.assertEqual(r, [])

    def test_nova_mensagem_depois_da_decisao_reabre_o_fio(self):
        resolvido = "2023-11-14T22:16:39+00:00"  # um segundo antes de DELA
        r = self._rodar(
            {"t1": [_msg("adv@exemplo.adv.br", DELA)]},
            decisoes={"t1": {"resolvedAt": resolvido, "reason": "ciência"}},
        )
        self.assertEqual([f["thread"] for f in r], ["t1"])

    def test_decisao_invalida_nunca_silencia(self):
        r = self._rodar(
            {"t1": [_msg("adv@exemplo.adv.br", DELA)]},
            decisoes={"t1": {"resolvedAt": "data-invalida"}},
        )
        self.assertEqual([f["thread"] for f in r], ["t1"])

    def test_sem_acervo_o_varredor_nao_inventa_alvo(self):
        with (mock.patch.object(fios.forja_acervo, "valor", return_value=[]),
              mock.patch.object(fios.forja_acervo, "fios_resolvidos", return_value={})):
            self.assertEqual(fios.remetentes(), [])
            self.assertEqual(fios.resolvidos(), {})
            self.assertEqual(fios.main(["--dias", "1"]), 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
