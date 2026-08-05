# -*- coding: utf-8 -*-
"""test_forja_varredura_tipografica.py — catraca de conformidade tipográfica.

O padrão Word do escritório existe desde 08/07/2026 e, até 04/08, ninguém sabia
quantas peças saíam dele: o gate que mede só era chamado dentro de uma F8, e a
F8 é a fase que menos roda. Medido pela primeira vez sobre o universo completo
de entregáveis, o retrato foi melhor do que o alarme inicial sugeria — mas o número
só serve para alguma coisa se não puder piorar em silêncio.

A catraca guarda dois compromissos diferentes:

  - o **universo** não pode encolher. Se o filtro de entregável parar de casar
    com os nomes reais, a conformidade fica ótima por falta de material — que é
    a maneira mais fácil de um instrumento mentir.
  - o número de peças fora do padrão não pode crescer.

O que ela NÃO faz: exigir que os casos existentes sejam corrigidos. As peças já
entregues são decisão do Igor, e travar a suíte por causa delas transformaria um
laudo em chantagem.

Uso: python test_forja_varredura_tipografica.py   (exit 0 = ok; exit 1 = regressão)
"""
from __future__ import annotations

import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from forja_varredura_tipografica import _marcar_superadas, varrer  # noqa: E402

# Medido em 04/08/2026, já descontadas as versões superadas por correção posterior
# do próprio escritório — sem esse desconto os números incluíam o parecer da CASO-17
# de 20/07, que foi corrigido para 100% nas três dimensões em 21/07.
# O piso de universo só sobe; os tetos de desvio só descem.
ENTREGAVEIS_MIN = 120
JUSTIFICACAO_ABAIXO_50_MAX = 4
TAMANHO_ABAIXO_90_MAX = 29
FONTE_ABAIXO_90_MAX = 19
TRES_DIMENSOES_MAX = 4


def verificar_familias_nao_pareiam_documentos_distintos() -> list[str]:
    def item(nome, caminho, just, tamanho, fonte):
        return {
            "peca": nome,
            "caminho": caminho,
            "paragrafos": 100,
            "justificacao": just,
            "tamanho": tamanho,
            "fonte": fonte,
        }

    medidas = [
        item("01_PARECER_CASO17_FINAL_LIMPO_PARA_ASSINATURA.docx",
             "C:/fabrica/Caso CASO-17/01_PARECER_CASO17_FINAL_LIMPO_PARA_ASSINATURA.docx",
             0.1, 0.2, 0.2),
        item("01_PARECER_CASO17_CORRIGIDO_JUSTIFICADO.docx",
             "C:/fabrica/Caso CASO-17/01_PARECER_CASO17_CORRIGIDO_JUSTIFICADO.docx",
             1.0, 1.0, 1.0),
        item("02_PARECER_CASO17_CONTROLE_DE_ALTERACOES.docx",
             "C:/fabrica/Caso CASO-17/02_PARECER_CASO17_CONTROLE_DE_ALTERACOES.docx",
             0.2, 0.2, 0.2),
        item("02_PARECER_CASO17_CORRIGIDO_CONTROLE_ALTERACOES.docx",
             "C:/fabrica/Caso CASO-17/02_PARECER_CASO17_CORRIGIDO_CONTROLE_ALTERACOES.docx",
             1.0, 1.0, 1.0),
        item("PLANO_PESQUISA_CASO17_FINAL.docx",
             "C:/fabrica/Caso CASO-17/PLANO_PESQUISA_CASO17_FINAL.docx",
             0.1, 0.1, 0.1),
        item("MEMORIAL_AZIMUT_N3_CORRIGIDA_ENTREGA.docx",
             "C:/fabrica/Caso CASO-17/MEMORIAL_AZIMUT_N3_CORRIGIDA_ENTREGA.docx",
             1.0, 1.0, 1.0),
        item("03_PARECER_NATURA_CABREUA_FINAL.docx",
             "C:/fabrica/Caso A/03_PARECER_NATURA_CABREUA_FINAL.docx",
             0.1, 0.1, 0.1),
        item("03_PARECER_NATURA_CABREUA_CORRIGIDO.docx",
             "C:/fabrica/Caso B/03_PARECER_NATURA_CABREUA_CORRIGIDO.docx",
             1.0, 1.0, 1.0),
    ]
    _marcar_superadas(medidas)
    mapa = {x["peca"]: x["superadaPor"] for x in medidas}
    esperado = {
        "01_PARECER_CASO17_FINAL_LIMPO_PARA_ASSINATURA.docx":
            "01_PARECER_CASO17_CORRIGIDO_JUSTIFICADO.docx",
        "02_PARECER_CASO17_CONTROLE_DE_ALTERACOES.docx":
            "02_PARECER_CASO17_CORRIGIDO_CONTROLE_ALTERACOES.docx",
        "PLANO_PESQUISA_CASO17_FINAL.docx": None,
        "03_PARECER_NATURA_CABREUA_FINAL.docx": None,
    }
    return [f"{nome}: esperado {valor!r}, obtido {mapa.get(nome)!r}"
            for nome, valor in esperado.items() if mapa.get(nome) != valor]


def main() -> int:
    falhas = 0
    familia_falhas = verificar_familias_nao_pareiam_documentos_distintos()
    if familia_falhas:
        print("  FALHOU: pareamento de versões superadas incorreto:")
        for falha in familia_falhas:
            print(f"      {falha}")
        falhas += 1
    laudo = varrer()
    f = laudo["foraDoPadrao"]

    if laudo.get("erros"):
        print(f"  FALHOU: {len(laudo['erros'])} entregável(is) não abriu(ram); "
              "a varredura não pode passar com cegueira de leitura")
        falhas += 1

    if laudo["entregaveisMedidos"] < ENTREGAVEIS_MIN:
        # Pouco material tem duas causas, e confundi-las é o defeito: se os autos
        # não estão nesta máquina a verificação não aconteceu; se estão e o
        # número caiu, o instrumento perdeu alcance e isso é regressão.
        if not forja_acervo.autos_disponiveis():
            print(f"  NÃO VERIFICADO: só {laudo['entregaveisMedidos']} entregáveis medidos — "
                  + forja_acervo.motivo_da_ausencia_dos_autos())
        else:
            print(f"  FALHOU: só {laudo['entregaveisMedidos']} entregáveis medidos, abaixo do "
                  f"piso de {ENTREGAVEIS_MIN} — a conformidade ficaria boa por falta de "
                  "material, e o filtro de nome é a parte frágil deste instrumento")
            falhas += 1

    for chave, teto, rotulo in (
        ("justificacaoAbaixoDe50", JUSTIFICACAO_ABAIXO_50_MAX, "justificação abaixo de 50%"),
        ("tamanhoAbaixoDe90", TAMANHO_ABAIXO_90_MAX, "tamanho 12 pt abaixo de 90%"),
        ("fonteAbaixoDe90", FONTE_ABAIXO_90_MAX, "Times New Roman abaixo de 90%"),
    ):
        if f[chave] > teto:
            print(f"  FALHOU: {f[chave]} peça(s) com {rotulo}, contra {teto} medidas em "
                  "04/08/2026 — alguma peça nova saiu do padrão da casa")
            falhas += 1

    tres = laudo["foraNasTresDimensoes"]
    if len(tres) > TRES_DIMENSOES_MAX:
        print(f"  FALHOU: {len(tres)} peça(s) fora do padrão nas TRÊS dimensões, contra "
              f"{TRES_DIMENSOES_MAX} — peça assim não passou pela diagramação da casa:")
        for x in tres[:6]:
            print(f"      {x['peca'][:60]}")
        falhas += 1

    if falhas:
        print(f"REGRESSÃO: {falhas} verificação(ões) de conformidade tipográfica falharam")
        return 1
    print(f"ok: {laudo['entregaveisMedidos']} entregáveis medidos; "
          f"{f['justificacaoAbaixoDe50']} abaixo de 50% de justificação e {len(tres)} fora nas "
          "três dimensões — nenhum número piorou")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
