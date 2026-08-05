# -*- coding: utf-8 -*-
"""Regressão do ledger de citações materiais (M3.2 do plano 19, lição 52).

DEVE_PEGAR: citação sem fonte vira P1 nominada; proposição sem fonte idem;
tabela ausente gera template + pendência. NÃO_PODE_TRAVAR: citação lastreada é
silêncio; tabela preenchida integra; caso sem estado não explode.
Roda com: python test_forja_ledger_material.py
"""
import json
import tempfile
import unittest
from pathlib import Path

from forja_ledger_material import montar, _parse_proposicoes, TEMPLATE_PROPOSICOES


def _caso(tmp: Path, texto_minuta: str, proposicoes: str | None = None,
          source_ledger: list | None = None) -> tuple[Path, Path]:
    case = tmp / "case-teste"
    (case / "producao").mkdir(parents=True)
    draft = case / "producao" / "MINUTA.md"
    draft.write_text(texto_minuta, encoding="utf-8")
    if proposicoes is not None:
        (case / "producao" / "PROPOSICOES_DECISIVAS.md").write_text(
            proposicoes, encoding="utf-8")
    estado = {"caseId": "case-teste", "inputs": {},
              "sourceLedger": source_ledger or []}
    (case / "FORJA_STATE.json").write_text(json.dumps(estado), encoding="utf-8")
    return case, draft


TABELA_OK = """| # | Proposição | Fonte primária | Localizador | Alcance | Ressalva |
|---|---|---|---|---|---|
| 1 | O prazo foi cumprido | e-STJ fl. 120 | fl. 120 | intimação em 01/07 | nenhuma |
| 2 | Sem fonte esta aqui |  |  |  |  |
"""


class DevePegar(unittest.TestCase):

    def test_citacao_sem_fonte_vira_p1_nominada(self):
        with tempfile.TemporaryDirectory() as tmp:
            case, draft = _caso(Path(tmp), "Aplica-se a Súmula 999 do STJ ao caso.\n")
            ledger = montar(case, draft)
        pend = [p for p in ledger["pendencias"] if "Súmula 999" in p["problema"]]
        self.assertEqual(len(pend), 1)
        self.assertEqual(pend[0]["sev"], "P1")

    def test_proposicao_sem_fonte_vira_p1(self):
        with tempfile.TemporaryDirectory() as tmp:
            case, draft = _caso(Path(tmp), "Texto sem citações.\n", proposicoes=TABELA_OK)
            ledger = montar(case, draft)
        pend = [p for p in ledger["pendencias"] if p["id"] == "prop-2"]
        self.assertEqual(len(pend), 1)

    def test_tabela_ausente_gera_template_e_pendencia(self):
        with tempfile.TemporaryDirectory() as tmp:
            case, draft = _caso(Path(tmp), "Texto.\n")
            ledger = montar(case, draft)
            template = case / "producao" / "PROPOSICOES_DECISIVAS.md"
            self.assertTrue(template.is_file())
        self.assertTrue(any(p["id"] == "proposicoes" for p in ledger["pendencias"]))


class NaoPodeTravar(unittest.TestCase):

    def test_citacao_casada_com_source_ledger_e_silencio(self):
        sl = [{"claim": "Citação na peça: Súmula 999 STJ",
               "classification": "FONTE_OFICIAL",
               "sourcePathOrUrl": "https://scon.stj.jus.br/...",
               "verifiedAt": "2026-07-10T10:00:00-03:00"}]
        with tempfile.TemporaryDirectory() as tmp:
            case, draft = _caso(Path(tmp), "Aplica-se a Súmula 999 do STJ.\n",
                                proposicoes=TABELA_OK.split("| 2")[0],
                                source_ledger=sl)
            ledger = montar(case, draft)
        cit = [e for e in ledger["entradas"] if e["origem"] == "citacao_extraida"][0]
        self.assertEqual(cit["fontePrimaria"], "FONTE_OFICIAL")
        self.assertEqual(cit["verificadoEm"], "2026-07-10T10:00:00-03:00")
        self.assertFalse(any("Súmula 999" in p["problema"] for p in ledger["pendencias"]))

    def test_proposicao_preenchida_integra_sem_pendencia(self):
        so_linha_1 = TABELA_OK.split("| 2")[0]
        with tempfile.TemporaryDirectory() as tmp:
            case, draft = _caso(Path(tmp), "Texto.\n", proposicoes=so_linha_1)
            ledger = montar(case, draft)
        props = [e for e in ledger["entradas"] if e["origem"] == "tabela_proposicoes"]
        self.assertEqual(len(props), 1)
        self.assertEqual(props[0]["fontePrimaria"], "e-STJ fl. 120")
        self.assertFalse(any(p["id"].startswith("prop-") for p in ledger["pendencias"]))

    def test_template_nao_e_parseado_como_proposicao(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "t.md"
            path.write_text(TEMPLATE_PROPOSICOES, encoding="utf-8")
            self.assertEqual(_parse_proposicoes(path), [])

    def test_estado_ausente_nao_explode(self):
        with tempfile.TemporaryDirectory() as tmp:
            case = Path(tmp) / "case-x"
            (case / "producao").mkdir(parents=True)
            draft = case / "producao" / "M.md"
            draft.write_text("Texto simples.\n", encoding="utf-8")
            ledger = montar(case, draft)
        self.assertEqual(ledger["totais"]["entradas"], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
