# -*- coding: utf-8 -*-
"""test_forja_porta_unica.py — a porta única sabe reprovar, e sabe deixar passar.

Contexto. Em 05/08/2026 o conselho Helena + Efesto + Diabob decidiu, por
unanimidade e sob delegação expressa do Igor, que a fábrica passa a ter **rota
única obrigatória**. A medição do Efesto encontrou seis caminhos capazes de
gerar DOCX pela `PecaVisual` — a entrada canônica e cinco scripts `build_docx.py`
dentro de pastas de caso — e apenas o primeiro chamava o verificador.

A implementação escolhida não deleta os cinco scripts (são registro histórico de
caso, e apagá-los seria destrutivo sem fechar buraco nenhum). Fecha-se a PORTA:
`PecaVisual.salvar()` é o ponto por onde todos os seis passam, e agora nenhum
atravessa sem conferência.

Este arquivo guarda as quatro coisas que a porta precisa provar. As três
primeiras são o que qualquer teste faria; a quarta é a que pega o modo de falha
que eu mesmo cometi construindo isto.

  1. Peça limpa passa.
  2. Peça com bloqueador real — placeholder, origem operacional — não nasce.
  3. Estudo interno com marcador de lacuna passa, porque marcador é legítimo
     em artefato interno e cobrá-lo ali travaria a fábrica todo dia.
  4. O gate lê a chave certa do verificador.

Sobre a quarta. A primeira versão da porta procurava `severidade` no achado; o
verificador devolve `sev`. O gate ficou cego: rodei a calibração contra 25 obras
reais e ela devolveu "zero peças bloqueadas", número que eu quase registrei como
prova de que a trava era segura. Era prova de que ela não enxergava nada. Um
teste que só verificasse "peça limpa passa" teria ficado verde nessa versão.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
FABRICA = RAIZ.parent
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(FABRICA / "_FERRAMENTAS"))

TEMPLATE = FABRICA / "_FERRAMENTAS" / "TEMPLATE_MEDINA_OSORIO_PETICAO.docx"

CORPO_LIMPO = (
    "A embargante opõe os presentes embargos de declaração em face do acórdão "
    "proferido pela colenda Turma, com fundamento no artigo 1.022 do Código de "
    "Processo Civil, pelas razões de direito a seguir expostas de modo "
    "individualizado.\n"
    "O acórdão deixou de enfrentar a tese de prevenção suscitada na petição "
    "inicial do recurso, o que configura omissão qualificada e impede a "
    "prestação jurisdicional completa sobre a matéria devolvida.\n"
    "A jurisprudência desta Corte reconhece que o julgador deve enfrentar todos "
    "os fundamentos capazes de infirmar a conclusão adotada, sob pena de "
    "negativa de prestação jurisdicional.\n"
    "Requer, por fim, o acolhimento dos embargos para que a omissão apontada "
    "seja sanada, com o consequente prequestionamento dos dispositivos "
    "legais e constitucionais invocados nesta oportunidade.\n"
) * 3


def _peca(tmp, corpo, nome="PECA_TESTE.docx", tipo=None):
    from medina_visual_kit import PecaVisual
    pv = PecaVisual(str(Path(tmp) / nome), template=str(TEMPLATE),
                    folio_aureo=False)
    if tipo:
        pv.tipo_produto = tipo
    for paragrafo in corpo.split("\n"):
        if paragrafo.strip():
            pv.doc.add_paragraph(paragrafo.strip())
    return pv


def rodar():
    import tempfile
    falhas = []

    def caso(nome, ok, detalhe=""):
        if ok:
            return
        print(f"  FALHOU: {nome} {detalhe}")
        falhas.append(nome)

    with tempfile.TemporaryDirectory() as tmp:
        # 1. Peça limpa passa e deixa laudo.
        pv = _peca(tmp, CORPO_LIMPO, "LIMPA.docx", tipo="peca")
        try:
            saida = pv.salvar()
            passou = Path(str(saida)).is_file()
        except RuntimeError as erro:
            passou, saida = False, None
            print(f"    (bloqueou a limpa: {erro})")
        caso("peça limpa atravessa a porta", passou)
        caso("a porta grava laudo mesmo quando aprova",
             (Path(tmp) / "LIMPA_PORTA_UNICA.json").is_file())
        if passou:
            laudo = json.loads((Path(tmp) / "LIMPA_PORTA_UNICA.json").read_text(
                encoding="utf-8"))
            caso("laudo registra hash do texto",
                 bool(laudo.get("textoSha256")))
            caso("laudo vincula o DOCX materializado",
                 laudo.get("docxSha256") == hashlib.sha256(
                     Path(saida).read_bytes()).hexdigest())

        # 2. Bloqueador real: placeholder em peça protocolável.
        pv = _peca(tmp, CORPO_LIMPO +
                   "\nO valor será apurado conforme [VERIFICAR EM FONTE OFICIAL "
                   "ANTES DA VERSÃO FINAL] e ajustado na fase própria.\n",
                   "COM_PLACEHOLDER.docx", tipo="peca")
        bloqueou = False
        try:
            pv.salvar()
        except RuntimeError:
            bloqueou = True
        caso("placeholder em peça não atravessa a porta", bloqueou)
        caso("peça bloqueada não nasce em disco",
             not (Path(tmp) / "COM_PLACEHOLDER.docx").is_file())

        # 3. Origem operacional no corpo — P0 inviolável desde 11/07/2026.
        pv = _peca(tmp, CORPO_LIMPO +
                   "\nO documento foi recebido por e-mail e está arquivado na "
                   "pasta do escritório no Drive, de onde será extraído.\n",
                   "COM_ORIGEM.docx", tipo="peca")
        bloqueou = False
        try:
            pv.salvar()
        except RuntimeError:
            bloqueou = True
        caso("origem operacional no corpo não atravessa a porta", bloqueou)

        # 3b. O tamanho não pode ser uma rota de fuga para um bloqueador.
        pv = _peca(tmp, "[VERIFICAR EM FONTE OFICIAL ANTES DA VERSÃO FINAL]",
                   "CURTA.docx", tipo="peca")
        bloqueou = False
        try:
            pv.salvar()
        except RuntimeError:
            bloqueou = True
        caso("placeholder curto também não atravessa a porta", bloqueou)
        caso("peça curta bloqueada não nasce em disco",
             not (Path(tmp) / "CURTA.docx").is_file())

        # 3c. Se o lastro econômico reprova depois da porta, o laudo não pode
        # continuar parecendo aprovação sem DOCX materializado.
        pv = _peca(tmp, CORPO_LIMPO +
                   "\nValor econômico declarado: R$ 100.000,00.\n",
                   "SEM_LASTRO.docx", tipo="peca")
        bloqueou = False
        try:
            pv.salvar()
        except RuntimeError:
            bloqueou = True
        caso("lastro econômico sem fonte bloqueia", bloqueou)
        saida_sem_lastro = Path(tmp) / "SEM_LASTRO.docx"
        caso("lastro bloqueado não deixa DOCX parcial",
             not saida_sem_lastro.is_file())
        laudo_sem_lastro = Path(tmp) / "SEM_LASTRO_PORTA_UNICA.json"
        if laudo_sem_lastro.is_file():
            laudo = json.loads(laudo_sem_lastro.read_text(encoding="utf-8"))
            caso("laudo não declara aprovação após falha do lastro",
                 laudo.get("veredito") == "reprovado" and
                 any(a.get("gate") == "FORJA-LASTRO"
                     for a in laudo.get("bloqueadores") or []))

        # 4. Estudo interno com marcador passa — o par de não-trava.
        #    Sem ele a porta viraria a trava inexequível que a casa proíbe:
        #    todo estudo preliminar carrega marcador de lacuna por desenho.
        pv = _peca(tmp, "ESTUDO PRELIMINAR — DIAGNÓSTICO\n" + CORPO_LIMPO +
                   "\nA base econômica permanece [VERIFICAR EM FONTE OFICIAL "
                   "ANTES DA VERSÃO FINAL] até a juntada do laudo.\n",
                   "ESTUDO.docx", tipo="estudo")
        passou = True
        try:
            pv.salvar()
        except RuntimeError as erro:
            passou = False
            print(f"    ({erro})")
        caso("estudo interno com marcador de lacuna passa", passou)

    # 5. O gate lê a chave certa. Esta é a contraprova da cegueira: se alguém
    #    voltar a procurar `severidade` no lugar de `sev`, os casos 2 e 3 acima
    #    passariam a "aprovar" e só este bate.
    from forja_verificador import verificar
    achados = verificar(CORPO_LIMPO + "\n[VERIFICAR EM FONTE OFICIAL ANTES DA "
                        "VERSÃO FINAL]\n", "peca")
    caso("o verificador devolve severidade na chave `sev`",
         any("sev" in a for a in achados),
         f"chaves vistas: {sorted({k for a in achados for k in a})}")

    if falhas:
        print(f"\nFALHOU: {len(falhas)} verificação(ões) — {', '.join(falhas)}")
        return 1
    print("ok: a porta única reprova bloqueador real, deixa passar peça limpa e "
          "estudo com marcador, e enxerga a severidade na chave certa")
    return 0


if __name__ == "__main__":  # pragma: no cover
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    raise SystemExit(rodar())
