# -*- coding: utf-8 -*-
"""test_forja_gate_anexo_saida.py — a barreira fica na saída, não no laudo.

A varredura tipográfica media o acervo e reprovava um baseline; ninguém a
consulta antes de anexar um arquivo e apertar enviar. Em 06/08/2026 dois
documentos fora do padrão da casa nas três dimensões seguiram para o cliente
com a medição funcionando o tempo todo. O que faltava não era medida, era
barreira — e barreira no ponto por onde a coisa passa.

Esta suíte guarda quatro compromissos:

  1. O critério reprova o que tem de reprovar e absolve o que tem de absolver:
     falha nas TRÊS dimensões barra; uma dimensão isolada, não.
  2. A ausência de medida nunca vira bloqueio. Arquivo curto, ilegível ou de
     outro formato não é prova de desvio, e reprovar por cegueira transformaria
     a barreira num obstáculo aleatório.
  3. A saída de emergência é nominal. Uma flag booleana liberaria o lote, e é
     no lote liberado em bloco que se esconde o arquivo que ninguém olhou.
  4. Laudo e barreira concordam: o que a varredura do acervo aponta fora nas
     três dimensões, a porta de saída barra. Se discordarem, um dos dois mente.

Uso: python test_forja_gate_anexo_saida.py
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import forja_acervo  # noqa: E402
import forja_gate_anexo_saida as gate  # noqa: E402

falhas = 0
casos = 0


def checar(nome: str, condicao: bool, detalhe: str = "") -> None:
    global falhas, casos
    casos += 1
    if not condicao:
        falhas += 1
        print(f"  FALHOU: {nome}" + (f" — {detalhe}" if detalhe else ""))


def medida(nome, just, tam, fonte, paragrafos=100):
    return {"arquivo": nome, "paragrafos": paragrafos,
            "justificacao": just, "tamanho": tam, "fonte": fonte}


# ------------------------------------------------------- o critério
checar("falhar nas três dimensões reprova",
       gate._falha_nas_tres(medida("x.docx", 0.29, 0.0, 0.0)))
checar("peça no padrão da casa passa",
       not gate._falha_nas_tres(medida("x.docx", 1.0, 1.0, 1.0)))
for rotulo, m in (
    ("só justificação", medida("x.docx", 0.10, 1.0, 1.0)),
    ("só tamanho", medida("x.docx", 1.0, 0.10, 1.0)),
    ("só fonte", medida("x.docx", 1.0, 1.0, 0.10)),
    ("duas de três", medida("x.docx", 0.10, 0.10, 1.0)),
):
    checar(f"{rotulo} não basta para barrar — anexo com quadro ou índice é legítimo",
           not gate._falha_nas_tres(m))

# O limiar exato, nas duas bordas.
checar("exatamente no piso de justificação não reprova",
       not gate._falha_nas_tres(medida("x.docx", gate.PISO_JUSTIFICACAO, 0.0, 0.0)))
checar("um décimo abaixo do piso reprova",
       gate._falha_nas_tres(medida("x.docx", gate.PISO_JUSTIFICACAO - 0.01, 0.0, 0.0)))


# ------------------------------------------------------- ausência de medida
with tempfile.TemporaryDirectory() as tmp:
    base = Path(tmp)
    (base / "planilha.xlsx").write_bytes(b"nao e docx")
    (base / "quebrado.docx").write_bytes(b"isto nao abre no Word")
    checar("arquivo de outro formato não é medido", gate.medir(base / "planilha.xlsx") is None)
    checar("DOCX ilegível não vira bloqueio", gate.medir(base / "quebrado.docx") is None)
    checar("arquivo inexistente não vira bloqueio", gate.medir(base / "nao_existe.docx") is None)
    veredito = gate.avaliar([base / "planilha.xlsx", base / "quebrado.docx"])
    checar("lote sem nada mensurável é aprovado, não barrado", veredito["aprovado"])
    checar("e não inventa medida", veredito["medidos"] == [])


# ------------------------------------------------------- a saída de emergência
class _Falso:
    """Substitui a medição para exercitar a declaração sem depender de arquivo."""
    def __init__(self, mapa):
        self.mapa = mapa

    def __call__(self, caminho, *, motivos=None):
        # `motivos` entrou na medição real em 06/08/2026, para que arquivo sem
        # medida diga POR QUE não tem — curto, ilegível ou de outro formato.
        # O dublê precisa aceitar a mesma assinatura, senão a regressão que
        # protege a barreira quebra na coleta e a barreira fica sem teste.
        medida = self.mapa.get(Path(caminho).name)
        if medida is None and motivos is not None:
            motivos.append({"arquivo": Path(caminho).name, "motivo": "sem medida no dublê"})
        return medida


medir_real = gate.medir
gate.medir = _Falso({
    "de_terceiro.docx": medida("de_terceiro.docx", 0.29, 0.0, 0.0),
    "nossa_fora_do_padrao.docx": medida("nossa_fora_do_padrao.docx", 0.10, 0.0, 0.0),
})
try:
    lote = ["de_terceiro.docx", "nossa_fora_do_padrao.docx"]
    v = gate.avaliar(lote)
    checar("sem declaração, os dois barram", len(v["bloqueados"]) == 2 and not v["aprovado"])

    v = gate.avaliar(lote, material_de_terceiro=["de_terceiro.docx"])
    checar("a declaração libera só o arquivo nomeado",
           [m["arquivo"] for m in v["bloqueados"]] == ["nossa_fora_do_padrao.docx"],
           f"barrados: {[m['arquivo'] for m in v['bloqueados']]}")
    checar("e o liberado fica registrado, não some",
           [m["arquivo"] for m in v["liberadosPorDeclaracao"]] == ["de_terceiro.docx"])

    v = gate.avaliar(lote, material_de_terceiro=["DE_TERCEIRO.DOCX"])
    checar("a declaração não depende de caixa alta ou baixa",
           len(v["liberadosPorDeclaracao"]) == 1)

    v = gate.avaliar(lote, material_de_terceiro=lote)
    checar("declarar todos passa — mas foi decisão nominal, não flag", v["aprovado"])

    texto = gate.explicar(gate.avaliar(lote))
    checar("a mensagem de bloqueio nomeia os arquivos",
           all(n in texto for n in lote))
    checar("e traz os três números medidos, para não ser preciso abrir o arquivo",
           "29%" in texto and "0%" in texto)

    # Um anexo que não desce nem decodifica não pode derrubar a conferência dos
    # outros: a exceção subiria e barraria o envio inteiro por defeito de
    # transporte. Também não pode sumir — barreira com ponto cego invisível é
    # pior que barreira nenhuma. Achado do Codex em 06/08/2026.
    class _ServicoQuebrado:
        """Devolve um rascunho com dois anexos: um íntegro e um corrompido."""
        def users(self):
            return self

        def drafts(self):
            return self

        def messages(self):
            return self

        def attachments(self):
            return self

        def get(self, **_k):
            return self

        def execute(self):
            return {"message": {"id": "m1", "payload": {"parts": [
                {"filename": "corrompido.docx",
                 "body": {"data": "isto-nao-e-base64-valido!!!"}},
                {"filename": "leve.docx", "body": {"data": ""}},
            ]}}}

    v = gate.avaliar_rascunho(_ServicoQuebrado(), "rascunho-x")
    checar("anexo ilegível não derruba a conferência do rascunho inteiro",
           v["aprovado"] and v["medidos"] == [])
    checar("e fica declarado como ponto cego, em vez de sumir",
           [x["arquivo"] for x in v["naoInspecionados"]] == ["corrompido.docx"],
           f"declarados: {v.get('naoInspecionados')}")
    checar("o ponto cego diz a causa, não só que existe — curto, ilegível e "
           "formato inesperado pedem providências diferentes",
           all(x.get("motivo") for x in v["naoInspecionados"]))
finally:
    gate.medir = medir_real


# ------------------------------------------------------- laudo e barreira concordam
# O acoplamento que faltava: tudo o que a varredura do acervo aponta como fora
# do padrão nas três dimensões precisa ser barrado pela porta de saída. Se os
# dois discordarem, um deles está mentindo — e foi exatamente essa distância
# entre medir e impedir que deixou dois documentos saírem em 06/08/2026.
#
# O alvo é descoberto pela medida, e nunca por nome de caso ou de parte: este
# arquivo vive do lado do motor, que existe para ser compartilhado.
if not forja_acervo.autos_disponiveis():
    print("  NÃO VERIFICADO: os autos não estão nesta máquina — a barreira não pôde "
          "ser exercitada contra os documentos reais que a originaram")
else:
    import forja_varredura_tipografica as vt  # noqa: E402

    laudo = vt.varrer()
    fora = [Path(x["caminho"]) for x in laudo["foraNasTresDimensoes"]]
    if not fora:
        print("  (nenhum documento do acervo está fora nas três dimensões hoje)")
    else:
        v = gate.avaliar(fora)
        checar("tudo que o laudo aponta fora nas três dimensões a porta barra",
               len(v["bloqueados"]) == len(fora) and not v["aprovado"],
               f"barrados {len(v['bloqueados'])} de {len(fora)}")

print(f"ok: {casos} casos — anexo fora do padrão da casa não sai pela porta da FORJA"
      if not falhas else f"REGRESSÃO: {falhas} de {casos} casos falharam")
sys.exit(1 if falhas else 0)
