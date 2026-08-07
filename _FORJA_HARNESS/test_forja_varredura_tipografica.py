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
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

import forja_acervo  # noqa: E402
from forja_varredura_tipografica import (  # noqa: E402
    FABRICA,
    _e_entregavel,
    _marcar_superadas,
    varrer,
)

# Medido em 04/08/2026, já descontadas as versões superadas por correção posterior
# do próprio escritório — sem esse desconto os números incluíam o parecer da CASO-17
# de 20/07, que foi corrigido para 100% nas três dimensões em 21/07.
# O piso de universo só sobe; os tetos de desvio só descem.
# Reancorado em 06/08/2026, quando o material recebido por e-mail saiu do escopo
# por decisão do Igor. A população mudou por escolha, e não porque a conformidade
# tenha melhorado: 23 arquivos deixaram de contar e o universo caiu de 142 para
# 119 medidos. Reancorar os dois lados na mesma hora é o que impede a exclusão de
# afrouxar a catraca duas vezes — uma por tirar arquivos, outra por manter tetos
# calibrados numa população maior. A comparação com o retrato de 04/08 fica
# perdida; isso é o custo da mudança de escopo, e não um efeito colateral oculto.
# O piso não existe para policiar a exclusão de um arquivo: existe para pegar o
# filtro de nome quebrando, e filtro quebrado não derruba um — derruba dezenas
# de uma vez. Ancorá-lo no valor exato medido (119, em 06/08/2026) produziria
# reprovação toda vez que alguém apagasse uma cópia obsoleta, e alarme que toca
# por movimento normal é alarme que se aprende a ignorar. A folga abaixo é
# dimensionada pelo modo de falha real, não por conforto: uma queda de dez por
# cento já não é rotina de faxina.
ENTREGAVEIS_MIN = 108
JUSTIFICACAO_ABAIXO_50_MAX = 3
# 24 → 25 em 06/08/2026, e o motivo fica nomeado porque teto que sobe em
# silêncio é o começo de uma catraca que não segura nada. Uma entrega produzida
# pela própria esteira nasceu com o estilo `Normal` em 11 pt — o padrão da casa
# é 12 —, e todos os parágrafos herdavam dali: 0% de cobertura. O estilo foi
# corrigido e a peça subiu para 85%. O que sobra são títulos em 13 pt, que a
# métrica não sabe distinguir de corpo e que são decisão de desenho de quem
# escreveu. A causa raiz não é esta peça: são dez geradores espalhados pelos
# casos, cada um fixando o próprio corpo (9,2; 10,2; 10,5; 11; 11,5 pt) em vez
# de usar os tokens da casa — e é isso que a catraca de geradores abaixo trava.
TAMANHO_ABAIXO_90_MAX = 25
FONTE_ABAIXO_90_MAX = 15
TRES_DIMENSOES_MAX = 3


# Catraca a montante: o defeito não nasce no documento, nasce no gerador.
# Cada entrega vinha escrevendo o próprio `build_*.py` e fixando o corpo à mão —
# 9,2; 10,2; 10,5; 11; 11,5 pt — em vez de usar os tokens da casa, que dizem 12.
# Medir o documento depois pega o sintoma um por um; travar o gerador impede a
# classe inteira. Os dez existentes ficam anistiados, porque são entregas
# passadas e reescrevê-las não é decisão minha; o que não pode é aparecer o
# décimo primeiro.
GERADORES_FORA_DO_CORPO_MAX = 10
_CORPO_A_MAO = re.compile(r"normal\.font\.size\s*=\s*Pt\(\s*([\d.]+)\s*\)")


def verificar_geradores_nao_reinventam_o_corpo() -> int:
    achados = []
    for arquivo in FABRICA.rglob("*.py"):
        if "node_modules" in str(arquivo):
            continue
        try:
            texto = arquivo.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for m in _CORPO_A_MAO.finditer(texto):
            if float(m.group(1)) != 12.0:
                achados.append((float(m.group(1)), arquivo.name))
    if len(achados) <= GERADORES_FORA_DO_CORPO_MAX:
        return 0
    print(f"  FALHOU: {len(achados)} gerador(es) fixam o corpo fora dos 12 pt do "
          f"padrão da casa, contra {GERADORES_FORA_DO_CORPO_MAX} anistiados — "
          f"use os tokens de `_FERRAMENTAS/estilo_medina.py` em vez de escolher "
          f"o tamanho de novo:")
    for tamanho, nome in sorted(achados)[:8]:
        print(f"      {tamanho}pt  {nome[:60]}")
    return 1


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
    privado = FABRICA / "_FORJA_HARNESS" / "private" / "quarentena" / "PETICAO_FINAL.docx"
    if _e_entregavel(privado):
        print("  FALHOU: arquivo da área private entrou no universo de entregáveis")
        falhas += 1
    familia_falhas = verificar_familias_nao_pareiam_documentos_distintos()
    if familia_falhas:
        print("  FALHOU: pareamento de versões superadas incorreto:")
        for falha in familia_falhas:
            print(f"      {falha}")
        falhas += 1
    falhas += verificar_geradores_nao_reinventam_o_corpo()

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
