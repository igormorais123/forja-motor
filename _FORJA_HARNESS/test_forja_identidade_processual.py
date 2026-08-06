# -*- coding: utf-8 -*-
"""
test_forja_identidade_processual.py — Testes de regressão para gates S2 e S4.

Testes contra sabotagens determinísticas:
  (i) Declaração lastreada na minuta → deve ser recusada
  (ii) Caso sem declaração → não gera P0 automático
  (iii) Peça legítima que cita o papel do adversário → não reprova
  (iv) S2 detecta: nome correto mas papel trocado na janela
  (v) S4 detecta: direção contrária aparece massivamente
"""
import json
import sys
from pathlib import Path

import forja_acervo

# Assumindo que o teste roda de dentro de _FORJA_HARNESS
RAIZ = Path(__file__).resolve().parent

from forja_identidade_processual import (
    gate_s2_pareamento_nome_papel,
    gate_s4_presenca_direcao_pedido,
    validar_declaracao_completa,
)


def test_s2_sem_declaracao():
    """(ii) Caso sem declaração → não gera P0."""
    texto = "O agravante peticionou. O agravado respondeu."
    achados = gate_s2_pareamento_nome_papel(texto, None)
    assert achados == [], f"Gate S2 deve retornar vazio sem declaração, mas retornou: {achados}"
    print("✓ test_s2_sem_declaracao")


def test_s4_sem_declaracao():
    """(ii) Caso sem declaração → não gera P0."""
    texto = "Pede-se o provimento do recurso."
    achados = gate_s4_presenca_direcao_pedido(texto, None)
    assert achados == [], f"Gate S4 deve retornar vazio sem declaração, mas retornou: {achados}"
    print("✓ test_s4_sem_declaracao")


def test_s2_com_declaracao_valida_no_texto():
    """(iii) Peça legítima que cita o papel do adversário → não reprova."""
    # Cenário: CASO-04 (agravada) pede desprovimento do agravo da União (agravante)
    # A peça menciona legitimamente "o agravo da União contra CASO-04"
    decl = {
        "cliente": {"nome": "CASO-04", "papel": "agravada"},
        "adverso": {"nome": "UNIÃO", "papel": "agravante"},
        "direcaoPedido": "desprovimento",
    }

    # Texto que menciona legitimamente o papel do adversário
    texto = (
        "A UNIÃO, na qualidade de agravante, interpôs agravo contra CASO-04. "
        "CASO-04, como agravada, contesta o agravo. "
        "O papel da agravada é responder aos termos do recurso."
    )

    achados = gate_s2_pareamento_nome_papel(texto, decl)
    # Não deve reprovar porque CASO-04 aparece com seu papel correto na maioria das vezes
    if achados:
        assert all(a["sev"] != "P0" for a in achados), f"Gate S2 reprovou peça legítima: {achados}"
    print("✓ test_s2_com_declaracao_valida_no_texto")


def test_s2_detecta_troca():
    """(iv) S2 detecta: nome correto mas papel trocado na janela."""
    decl = {
        "cliente": {"nome": "CASO-04", "papel": "agravada"},
        "adverso": {"nome": "UNIÃO", "papel": "agravante"},
        "direcaoPedido": "desprovimento",
    }

    # Texto MUTADO: CASO-04 mas sempre chamada de agravante (papel errado)
    texto = (
        "CASO-04, na qualidade de agravante, interpôs agravo. "
        "CASO-04, como agravante, pede provimento. "
        "A agravante CASO-04 alega vício processual. "
        "O papel de agravante pertence a CASO-04 neste caso."
    )

    achados = gate_s2_pareamento_nome_papel(texto, decl)
    # Deve reprovar porque nenhuma janela tem o papel correto "agravada"
    p0_count = sum(1 for a in achados if a["sev"] == "P0")
    assert p0_count > 0, f"Gate S2 deveria detectar troca de papel em CASO-04, mas retornou: {achados}"
    print(f"✓ test_s2_detecta_troca ({p0_count} P0)")


def test_s4_detecta_troca():
    """(v) S4 detecta: direção contrária aparece massivamente."""
    decl = {
        "cliente": {"nome": "CASO-04", "papel": "agravada"},
        "adverso": {"nome": "UNIÃO", "papel": "agravante"},
        "direcaoPedido": "desprovimento",
    }

    # Texto MUTADO: pede provimento em vez de desprovimento
    texto = (
        "Pede-se o provimento do agravo. "
        "A reforma é o provimento da peça. "
        "O provimento é necessário para corrigir a injustiça. "
        "Requer-se o provimento da demanda."
    )

    achados = gate_s4_presenca_direcao_pedido(texto, decl)
    # Deve reprovar porque "desprovimento" não aparece mas "provimento" sim
    p0_count = sum(1 for a in achados if a["sev"] == "P0")
    assert p0_count > 0, f"Gate S4 deveria detectar troca de direção, mas retornou: {achados}"
    print(f"✓ test_s4_detecta_troca ({p0_count} P0)")


def test_s4_com_direcao_presente():
    """S4 com direção correta presente → não reprova."""
    decl = {
        "cliente": {"nome": "CASO-04", "papel": "agravada"},
        "adverso": {"nome": "UNIÃO", "papel": "agravante"},
        "direcaoPedido": "desprovimento",
    }

    # Texto com direção correta
    texto = (
        "Pede-se o desprovimento do agravo interposto pela União. "
        "O desprovimento é a solução cabível. "
        "Requer-se, assim, o desprovimento da demanda."
    )

    achados = gate_s4_presenca_direcao_pedido(texto, decl)
    # Não deve reprovar porque "desprovimento" está presente
    if achados:
        assert all(a["sev"] != "P0" for a in achados), f"Gate S4 reprovou com direção presente: {achados}"
    print("✓ test_s4_com_direcao_presente")


def test_estrutura_invalida():
    """Declaração com estrutura inválida → não passa validação."""
    decl_ruim = {
        "cliente": {"nome": "CASO-04", "papel": "papel_invalido"},
    }

    val = validar_declaracao_completa(decl_ruim)
    assert not val.valida, "Validação deveria falhar"
    assert any("papel" in e.lower() for e in val.erros), f"Deveria mencionar papel nos erros: {val.erros}"
    print("✓ test_estrutura_invalida")


CASO_REAL = Path("state") / (forja_acervo.caso("CASO-04") or "__sem_acervo__")


def test_regiao_requerimento_nao_e_a_assinatura():
    """O defeito real de 05/08/2026: a região caía no bloco de assinatura.

    `_regiao_requerimento` pegava o ÚLTIMO marcador, e "pede deferimento" vem
    DEPOIS da lista de pedidos. A região devolvida tinha 277 caracteres, era só
    nome de advogado e OAB, e não continha verbo de pedido nenhum — o gate S4
    ficava silenciosamente cego sobre o texto que mais importa.
    """
    from forja_identidade_processual import _regiao_requerimento
    peca = (
        "Preâmbulo longo da peça que ocupa a primeira metade inteira do texto e "
        "existe só para que o corte pela metade tenha material de sobra. " * 6
        + "\n\nAnte o exposto, requerem as agravadas o desprovimento do agravo interno.\n\n"
        "Pede deferimento.\n\nBrasília/DF.\n\nFULANO DE TAL\nOAB/RS 00.000\n"
    )
    regiao = _regiao_requerimento(peca)
    assert regiao, "nenhuma região de requerimento foi encontrada"
    assert "requerem as agravadas" in regiao, (
        "a região começou depois do pedido — provavelmente no bloco de assinatura")
    assert "desprovimento" in regiao, "o pedido ficou fora da região"

    # E o inverso: marcador cedo demais é argumentação, não requerimento.
    argumentativo = "Ante o exposto no acórdão recorrido, " + ("texto. " * 400)
    assert _regiao_requerimento(argumentativo) == "", (
        "marcador na primeira metade foi tratado como requerimento — o gate leria "
        "o corpo da peça como pedido da cliente")
    print("✓ test_regiao_requerimento_nao_e_a_assinatura")


def test_peca_aprovada_real_passa_limpa_e_o_mutante_do_fecho_nao():
    """Contraprova contra a peça REAL, não contra texto inventado.

    A âncora é a Impugnação ao AgInt da CASO-04 (V4), aprovada pelo escritório.
    Ela cita legitimamente as duas direções ao longo da argumentação; só o
    requerimento é unívoco. Se este teste começar a acusar o original, o gate
    está errado — regra da casa.
    """
    import re
    from forja_identidade_processual import (carregar_declaracao,
                                             gate_s4_presenca_direcao_pedido)
    if not CASO_REAL.is_dir():
        print("  (pulado: caso real ausente nesta cópia)")
        return
    decl = carregar_declaracao(CASO_REAL)
    assert decl, "o caso real perdeu a declaração de identidade processual"

    from forja_mutation_semantic import _achar_draft
    draft = _achar_draft(CASO_REAL)
    assert draft is not None, (
        "o caso real saiu da bateria — _achar_draft deixou de enxergar "
        "canonical_markdown")
    texto = draft.read_text(encoding="utf-8")

    assert not gate_s4_presenca_direcao_pedido(texto, decl), (
        "o gate acusou a peça APROVADA pelo escritório")

    ocorrencias = list(re.finditer(r"\bdesprovimento\b", texto))
    assert ocorrencias, "a peça real deixou de conter a direção declarada"
    ultima = ocorrencias[-1]
    mutante = texto[:ultima.start()] + "provimento" + texto[ultima.end():]
    achados = gate_s4_presenca_direcao_pedido(mutante, decl)
    assert any(a["gate"] == "S4-direcao-no-requerimento" for a in achados), (
        "inverter o pedido da própria cliente no fecho passou sem ser notado")
    print(f"✓ test_peca_aprovada_real (original limpo; mutante do fecho pego por "
          f"{[a['gate'] for a in achados]})")


def test_lastro_em_artefato_derivado_e_recusado():
    """Declaração lastreada na minuta nasceria mutada junto — tem de ser recusada.

    Foi exatamente o que a primeira geração automática produziu: sourceKey
    `canonical_markdown`, sha256 literalmente "[será preenchido]" e adverso
    "TRANSPORTADORA OU ESTADO". Parecia declaração e era chute.
    """
    from forja_identidade_processual import validar_lastro_de_fonte_externa
    decl = {
        "cliente": {"nome": "X LTDA", "papel": "agravada"},
        "adverso": {"nome": "UNIÃO", "papel": "agravante"},
        "direcaoPedido": "desprovimento",
        "lastro": {"sourceKey": "minuta", "sha256": "a" * 64,
                   "trechoVerbatim": "trecho suficientemente longo para passar do piso"},
    }
    manifesto = {"n4SourceRegistry": {
        "minuta": {"path": "C:/casos/x/producao/draft_markdown.md"},
        "autuacao": {"path": "C:/casos/x/fontes/PETICAO_ADVERSA.pdf"},
    }}
    assert not validar_lastro_de_fonte_externa(decl, manifesto).valida, (
        "lastro apontando para a minuta foi aceito — o gate nasceria cego")

    decl["lastro"]["sourceKey"] = "autuacao"
    assert validar_lastro_de_fonte_externa(decl, manifesto).valida, (
        "lastro em fonte externa legítima foi recusado")
    print("✓ test_lastro_em_artefato_derivado_e_recusado")


# --------------------------------------------------------------------------
# S6 e S7 — a forma do caso vem de correções escritas do titular em julho e
# agosto de 2026, em dois processos distintos; os identificadores aqui são
# sintéticos, porque o gate da fronteira acusa número real em arquivo do motor
# e tem razão. O que se reproduz é o modo de falha: os recursos citados a mais
# EXISTEM e são do MESMO cliente, e é por isso que nenhum gate lexical os
# apanha — só a lista externa do que pertence a este trabalho. O tema excluído
# é verdadeiro sobre o caso e estranho ao que o tribunal pode decidir nele.
# --------------------------------------------------------------------------
DECL_ATOS = {
    "atos": {"impugnado": "REsp 0.000.001/UF",
             "relacionados": ["0000000-00.2022.8.26.0000"]},
    "objeto": {"devolvido": "art. 406 do CC — SELIC como índice único",
               "excluidos": ["salvados", "Tema 0.000", "multa do art. 523"]},
}
TEXTO_COM_ERRO = (
    "Trata-se do REsp 0.000.001/UF, originado do AI 0000000-00.2022.8.26.0000. "
    "Como já decidido no REsp 0.000.002/UF e no AREsp 0.000.003/UF, a questão "
    "dos salvados também merece exame, além da multa do art. 523 do CPC."
)
TEXTO_LIMPO = (
    "Trata-se do REsp 0.000.001/UF, originado do AI 0000000-00.2022.8.26.0000. "
    "Aplica-se o art. 406 do Código Civil, com incidência da SELIC."
)


def test_s6_acusa_recurso_de_outro_desdobramento():
    from forja_identidade_processual import gate_s6_identidade_do_ato
    achados = gate_s6_identidade_do_ato(TEXTO_COM_ERRO, DECL_ATOS)
    citados = " ".join(a["problema"] for a in achados)
    assert "0.000.002" in citados, "não acusou o REsp de outro desdobramento"
    assert "0.000.003" in citados, "não acusou o AREsp de outro desdobramento"
    assert all(a["sev"] == "P0" for a in achados)
    print("✓ S6 acusa ato de outro desdobramento do mesmo cliente")


def test_s6_nao_acusa_o_que_foi_declarado():
    from forja_identidade_processual import gate_s6_identidade_do_ato
    assert gate_s6_identidade_do_ato(TEXTO_LIMPO, DECL_ATOS) == []
    print("✓ S6 silencia quando todo ato citado foi declarado")


def test_s7_acusa_tema_fora_do_objeto():
    from forja_identidade_processual import gate_s7_objeto_devolvido
    temas = " ".join(a["problema"] for a in gate_s7_objeto_devolvido(TEXTO_COM_ERRO, DECL_ATOS))
    assert "salvados" in temas and "art. 523" in temas
    assert gate_s7_objeto_devolvido(TEXTO_LIMPO, DECL_ATOS) == []
    print("✓ S7 acusa tema declarado fora do objeto devolvido")


def test_s6_s7_sem_declaracao_nao_opinam():
    # A regra da casa: caso não declarado fica indeterminado, nunca reprovado
    # por ausência. São 52 casos sem declaração — o contrário travaria todos.
    from forja_identidade_processual import (
        gate_s6_identidade_do_ato, gate_s7_objeto_devolvido)
    for decl in ({}, None, {"cliente": {"nome": "X", "papel": "agravada"}}):
        assert gate_s6_identidade_do_ato(TEXTO_COM_ERRO, decl) == []
        assert gate_s7_objeto_devolvido(TEXTO_COM_ERRO, decl) == []
    print("✓ S6 e S7 não opinam sem os blocos declarados")


def main():
    try:
        test_s6_acusa_recurso_de_outro_desdobramento()
        test_s6_nao_acusa_o_que_foi_declarado()
        test_s7_acusa_tema_fora_do_objeto()
        test_s6_s7_sem_declaracao_nao_opinam()
        test_s2_sem_declaracao()
        test_s4_sem_declaracao()
        test_s2_com_declaracao_valida_no_texto()
        test_s2_detecta_troca()
        test_s4_detecta_troca()
        test_s4_com_direcao_presente()
        test_estrutura_invalida()
        test_regiao_requerimento_nao_e_a_assinatura()
        test_peca_aprovada_real_passa_limpa_e_o_mutante_do_fecho_nao()
        test_lastro_em_artefato_derivado_e_recusado()
        print("\n" + "="*70)
        print("TODOS OS TESTES PASSARAM")
        return 0
    except AssertionError as e:
        print(f"\n✗ TESTE FALHOU: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ ERRO: {e}")
        import traceback
        traceback.print_exc()
        return 2


if __name__ == "__main__":
    sys.exit(main())
