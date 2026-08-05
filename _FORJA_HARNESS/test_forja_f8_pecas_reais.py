# -*- coding: utf-8 -*-
"""test_forja_f8_pecas_reais.py — o QA visual contra peças aprovadas de verdade.

Regressão sintética prova que o gate reprova o defeito que o autor imaginou.
Não prova que ele deixa passar o trabalho que o escritório aprovou — e esse é
o erro mais caro, porque um gate que barra peça boa é desligado pelo operador
na primeira semana, e junto com ele some o dia em que ele acertaria.

Em 04/08/2026 os dezesseis gates da F8 foram exercidos pela primeira vez contra
quatro peças reais e entregues. Reprovaram as quatro. Dois falsos positivos barravam
TODA peça da casa:

  - a síntese executiva no estilo do art. 343-A, obrigatória desde 07/07/2026,
    era lida como corpo fora de tamanho;
  - `docx_folio_collision_safe` exigia fólio de no máximo 36 pt, e o fólio do
    `TEMPLATE_MEDINA_OSORIO_PETICAO.docx` — de onde toda peça é obrigada a
    nascer — mede 57,3 pt. O gate reprovava o próprio template do escritório.

Este teste guarda as duas calibrações contra o material real. Ele é tolerante a
peça ausente (o acervo do escritório não está no repositório do harness) e
exigente quando a peça existe: aí ela precisa passar nos gates estruturais.

Uso: python test_forja_f8_pecas_reais.py   (exit 0 = ok; exit 1 = regressão)
"""
from __future__ import annotations

import io
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

RAIZ = Path(__file__).resolve().parent
import forja_acervo  # noqa: E402

FABRICA = RAIZ.parent

from forja_docx_layout import FOLIO_SAFE_WIDTH_PT, _folio_rectangles, _vml_width_pt  # noqa: E402
from forja_visual_qa_structural import auditar_documento  # noqa: E402

TEMPLATE = FABRICA / "_FERRAMENTAS" / "TEMPLATE_MEDINA_OSORIO_PETICAO.docx"

# Peças aprovadas e entregues. Cada uma passou pelo olho do Fábio ou do Igor.
PECAS_APROVADAS = [c for c in (forja_acervo.caminho("peca-f8-plano-estrategico"),
                               forja_acervo.caminho("peca-f8-memoriais-ai")) if c]

# Não são falsos positivos e não podem entrar na lista acima: são peças reais
# com defeitos já localizados na primeira execução. Mantê-las aqui transforma a
# descoberta em regressão: se o gate deixar de acusar o defeito conhecido, a
# suíte falha; se surgir outro achado, ele não é silenciosamente absorvido.
PECAS_TRIADAS = [(c, ach) for c, ach in (
    (forja_acervo.caminho("peca-triada-nono-topico"), {"body_font_size_not_12pt"}),
    # A V8 esteve aqui com `table_typography_inconsistent`, e era ERRO MEU de
    # triagem: a mistura de Segoe UI com Times dentro da tabela é a identidade
    # da casa, emitida pelo kit visual desde o padrão aprovado em 09/07/2026.
    (forja_acervo.caminho("peca-triada-v8-visual"), set()),
) if c]

# Códigos que NÃO podem aparecer numa peça aprovada. Ficam de fora os que
# apontam defeito real já triado e comunicado ao Igor em
# `F8_PRIMEIRA_EXECUCAO_REAL_2026-08-04.md` — nomeá-los aqui é a diferença entre
# calibrar e maquiar.
PROIBIDOS_EM_PECA_APROVADA = {
    "body_font_size_not_12pt",
    "folio_width_unsafe",
    "body_text_not_justified",
    "body_font_not_medina",
    "structural_text_not_justified",
    "structural_font_not_medina",
    "structural_typography_unresolved",
}
TOLERADOS_COM_MOTIVO = {
    # `table_typography_inconsistent` saiu daqui em 04/08/2026. Ele estava
    # tolerado como "defeito real ainda não corrigido"; era falso positivo do
    # gate contra a identidade da casa, e a tolerância mascarava justamente isso.
    # Tolerar um achado é adiar a pergunta se ele é verdadeiro — e enquanto ele
    # fica na lista, ninguém a faz.
    # A lista está vazia de propósito. Se um achado novo precisar entrar aqui,
    # ele vem com o nome do arquivo, a data e o motivo — nunca só o código.
}
TOLERADOS_COM_MOTIVO = set(TOLERADOS_COM_MOTIVO)


def main() -> int:
    falhas = 0
    casos = 0

    # 1. O limiar do fólio tem de comportar o template aprovado. Sem isto, o
    #    gate volta a reprovar toda peça da casa e ninguém percebe até alguém
    #    abrir quatro documentos à mão, como foi preciso fazer em 04/08.
    casos += 1
    if not TEMPLATE.is_file():
        print(f"  AVISO: template não encontrado em {TEMPLATE} — a âncora do fólio não foi medida")
    else:
        from docx import Document
        larguras = [_vml_width_pt(r) for r in _folio_rectangles(Document(str(TEMPLATE)))]
        larguras = [w for w in larguras if w is not None]
        if not larguras:
            print("  AVISO: o template não expôs largura de fólio; âncora não medida")
        elif max(larguras) > FOLIO_SAFE_WIDTH_PT:
            print(f"  FALHOU: o fólio do TEMPLATE APROVADO mede {max(larguras)} pt e o limiar do "
                  f"gate é {FOLIO_SAFE_WIDTH_PT} pt — o gate reprova o padrão da casa")
            falhas += 1

    # 1-B. A colisão do fólio contra a margem tem de saber os DOIS lados. Sem o
    #      par abaixo, ela vira teto decorativo — o teto absoluto de 61 pt já era
    #      isso: nenhum documento do acervo o violava, e o achado nunca disparava.
    #      Contraprova: o fólio de 57,3 pt do template cabe nos 99,2 pt da margem
    #      padrão. Prova: a família CASO-17 usa margem de editor (51 pt) com o
    #      mesmo fólio, e ali ele realmente entra na mancha de texto.
    #      Triado em 04/08/2026: os quatro documentos acusados são um só desvio —
    #      documento montado com margens de editor reusando o fólio da casa —,
    #      e nenhum deles é peça protocolada.
    casos += 1
    from docx import Document as _Doc
    from forja_docx_layout import _folios_com_margem, FOLIO_MARGIN_SLACK_PT

    def _estoura(caminho):
        for tupla in _folios_com_margem(_Doc(str(caminho))):
            largura, margem = _vml_width_pt(tupla[0]), tupla[1]
            if largura is not None and margem is not None and largura > margem + FOLIO_MARGIN_SLACK_PT:
                return True
        return False

    desviante = next(FABRICA.rglob("PARECER_NATURA_CABREUVA_TRF_MEDINA_FOTO_V2_*.docx"), None)
    if desviante is None:
        print("  AVISO: o desviante do fólio sumiu do acervo — a prova do achado não foi medida")
    elif not _estoura(desviante):
        print("  FALHOU: o fólio de 57,3 pt deixou de ser acusado numa margem de 51 pt "
              f"({desviante.name[:52]}) — a checagem de colisão virou teto decorativo")
        falhas += 1
    for aprovada in PECAS_APROVADAS:
        if aprovada.is_file() and _estoura(aprovada):
            print(f"  FALHOU: peça aprovada acusada de colisão de fólio — {aprovada.name[:52]}")
            falhas += 1

    # 2. As peças aprovadas não podem cair nos gates estruturais.
    examinadas = 0
    for peca in PECAS_APROVADAS:
        if not peca.is_file():
            continue
        examinadas += 1
        casos += 1
        laudo = auditar_documento(peca)
        codigos = {f.get("code") for f in (laudo.get("findings") or [])}
        proibidos = sorted(codigos & PROIBIDOS_EM_PECA_APROVADA)
        if proibidos:
            print(f"  FALHOU: peça aprovada reprovada em {', '.join(proibidos)} — "
                  f"{peca.name[:60]}")
            falhas += 1
        for codigo in sorted(codigos - PROIBIDOS_EM_PECA_APROVADA - TOLERADOS_COM_MOTIVO):
            print(f"  ATENÇÃO: achado novo não triado em {peca.name[:50]}: {codigo}")

    # 3. Os dois achados reais da primeira execução precisam continuar visíveis.
    triadas = 0
    for peca, esperados in PECAS_TRIADAS:
        if not peca.is_file():
            continue
        triadas += 1
        casos += 1
        laudo = auditar_documento(peca)
        codigos = {f.get("code") for f in (laudo.get("findings") or [])}
        faltantes = sorted(esperados - codigos)
        if faltantes:
            print(f"  FALHOU: achado triado desapareceu em {peca.name[:60]}: "
                  f"{', '.join(faltantes)}")
            falhas += 1

    if examinadas + triadas == 0:
        print("  AVISO: nenhuma peça do acervo encontrada; este teste não mediu nada nesta "
              "máquina. Não é aprovação.")

    if falhas:
        print(f"REGRESSÃO: {falhas} de {casos} verificações contra material real falharam")
        return 1
    print(f"ok: {examinadas} peça(s) de referência passam, {triadas} peça(s) triadas "
          f"mantêm seus achados, e o limiar do fólio ({FOLIO_SAFE_WIDTH_PT} pt) "
          "comporta o template da casa")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
