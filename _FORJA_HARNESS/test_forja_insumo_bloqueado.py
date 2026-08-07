# -*- coding: utf-8 -*-
"""test_forja_insumo_bloqueado.py — "não localizado" não é diagnóstico.

A regressão guarda a correção mais recorrente que o titular já fez à esteira:
a mesma cobrança, quase palavra por palavra, em CINCO matérias distintas —
quatro delas no mesmo dia de agosto de 2026. Nenhum outro padrão do acervo se
repetiu tanto, e ele não é sobre o texto da peça: é sobre como a esteira relata
um insumo que não conseguiu ler.

Uso: python test_forja_insumo_bloqueado.py
"""
from __future__ import annotations

import json
import sys
import tempfile
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import forja_insumo_bloqueado as ib  # noqa: E402

falhas = 0
casos = 0


def checar(nome: str, condicao: bool, detalhe: str = "") -> None:
    global falhas, casos
    casos += 1
    if not condicao:
        falhas += 1
        print(f"  FALHOU: {nome}" + (f" — {detalhe}" if detalhe else ""))


RECEBIDOS = [{"documento": "cópia integral dos autos, 283 páginas", "conferido": True}]


def escrever(base: Path, itens, recebidos=RECEBIDOS) -> Path:
    caso = base / "caso-x"
    (caso / "n4_artifacts").mkdir(parents=True, exist_ok=True)
    corpo = {"schema": ib.VERSAO, "caseId": "caso-x", "itens": itens}
    if recebidos is not None:
        corpo["recebidos"] = recebidos
    (caso / "n4_artifacts" / ib.ARQUIVO).write_text(
        json.dumps(corpo, ensure_ascii=False), encoding="utf-8")
    return caso


# A data de revalidação é relativa e não fixa. Fixture com data escrita à mão
# passa hoje e falha sozinha daqui a alguns meses, e regressão que quebra pelo
# calendário ensina a equipe a ignorar o vermelho.
_REVALIDAR = (date.today() + timedelta(days=14)).isoformat()

COMPLETO = {
    "documento": "petição inicial da ação civil pública",
    # O par fonte × tipo entrou em 07/08/2026: sem ele não se confere se sobrou
    # rota conhecida por tentar, que foi a lacuna dos dois bloqueios falsos.
    "fonte": "TRF4",
    "tipoDocumento": "peticao_de_parte",
    "rotasTentadas": [],
    "causa": "sem_habilitacao_nos_autos",
    "diligencias": [
        {"onde": "eproc do tribunal", "quando": "2026-08-04",
         "resultado": "exige credencial de parte habilitada"},
        {"onde": "base pública de jurisprudência", "quando": "2026-08-04",
         "resultado": "só o acórdão, sem a inicial"},
    ],
    "consequencia": "o capítulo de fatos fica sem a redação original do pedido",
    "rotaDeSolucao": "habilitação nos autos pelo escritório, ou cópia integral pelo cliente",
    "revalidarApos": _REVALIDAR,
}

with tempfile.TemporaryDirectory() as tmp:
    base = Path(tmp)

    # Caso sem o artefato passa. Exigir o arquivo de todos os casos
    # transformaria um gate sobre qualidade de diagnóstico em burocracia.
    vazio = base / "caso-sem-bloqueio"
    vazio.mkdir()
    checar("caso sem insumo bloqueado é aprovado", ib.validar(vazio) == [])

    checar("declaração completa é aprovada", ib.validar(escrever(base, [COMPLETO])) == [])

    # O ponto do módulo: sintoma recusado como causa.
    for sintoma in ("não localizado", "inacessível", "indisponível", "não foi possível baixar"):
        problemas = ib.validar(escrever(base, [{**COMPLETO, "causa": sintoma}]))
        checar(f"'{sintoma}' é recusado como causa",
               any("sintoma" in p for p in problemas), "; ".join(problemas[:2]))

    problemas = ib.validar(escrever(base, [{**COMPLETO, "causa": "outra_coisa_qualquer"}]))
    checar("causa fora do vocabulário é recusada",
           any("vocabulário" in p for p in problemas))

    # Sem diligências, "indisponível na fonte" é indistinguível de "não procurei".
    for diligencias in ([], None, "consultei o portal"):
        problemas = ib.validar(escrever(base, [{**COMPLETO, "diligencias": diligencias}]))
        checar(f"diligência ausente ({type(diligencias).__name__}) reprova",
               any("diligência" in p for p in problemas))

    problemas = ib.validar(escrever(base, [{
        **COMPLETO, "diligencias": [{"onde": "portal", "resultado": "erro"}]}]))
    checar("diligência sem data reprova", any("quando" in p for p in problemas))

    for campo in ("consequencia", "rotaDeSolucao"):
        problemas = ib.validar(escrever(base, [{**COMPLETO, campo: "  "}]))
        checar(f"'{campo}' vazio reprova", any(campo in p for p in problemas))

    problemas = ib.validar(escrever(base, [{**COMPLETO, "documento": ""}]))
    checar("documento sem identificação reprova",
           any("identificação" in p for p in problemas))

    # As quatro causas do titular, e só elas.
    checar("as quatro causas são exatamente as que o titular pediu para distinguir",
           set(ib.CAUSAS) == {"sem_habilitacao_nos_autos", "restricao_de_permissao_ou_link",
                              "indisponivel_na_fonte", "limitacao_da_ferramenta"})
    for causa in ib.CAUSAS:
        checar(f"causa '{causa}' é aceita",
               ib.validar(escrever(base, [{**COMPLETO, "causa": causa}])) == [])

    # A outra metade da pergunta do titular, feita numa quinta matéria: dizer o
    # que faltou sem dizer o que foi lido não distingue documento que não veio
    # de documento que veio e não foi aberto.
    problemas = ib.validar(escrever(base, [COMPLETO], recebidos=None))
    checar("bloqueio sem inventário do que foi recebido reprova",
           any("recebidos" in p for p in problemas), "; ".join(problemas[:2]))
    problemas = ib.validar(escrever(base, [COMPLETO],
                                    recebidos=[{"documento": "autos integrais"}]))
    checar("recebido sem dizer se foi conferido reprova",
           any("aberto e lido" in p for p in problemas))
    checar("caso sem bloqueio não precisa de inventário",
           ib.validar(escrever(base, [], recebidos=None)) == [])

    # Artefato corrompido não passa em silêncio.
    caso = escrever(base, [COMPLETO])
    (caso / "n4_artifacts" / ib.ARQUIVO).write_text("{ isto nao e json", encoding="utf-8")
    checar("artefato ilegível não é lido como ausência de bloqueio",
           ib.carregar(caso) is None)

print(f"ok: {casos} casos — insumo bloqueado exige causa, diligência e rota"
      if not falhas else f"REGRESSÃO: {falhas} de {casos} casos falharam")
sys.exit(1 if falhas else 0)
