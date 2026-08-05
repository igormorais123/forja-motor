"""Testes para metricas_f7: valida extração de citações, verificações e autoridades."""

from pathlib import Path

import forja_acervo

from forja_metricas_f7 import metricas_f7


def test_f7_campos_sintetico():
    """Testa com md sintético: 2 citações no cache, 1 fora, 1 [VERIFICAR]."""

    md = """# Petição de Teste

Citação presente: Tema 1368 (STJ).
Citação não conferida: REsp 9.999.999.
Citação não conferida: Súmula 5.
Citação não conferida: Informativo 123.

[VERIFICAR EM FONTE OFICIAL: datas exatas dos desembolsos]

Mais texto aqui.
[VERIFICAR: teor literal do capítulo de juros]
"""

    resultado = metricas_f7(md)

    assert resultado["citacoesTotal"] == 4, f"esperado 4 citações, obtido {resultado['citacoesTotal']}"
    # Valida que há não-conferidas independentes do cache oficial de produção.
    assert len(resultado["citacoesNaoConferidas"]) >= 2, \
        f"esperado >= 2 não-conferidas, obtido {len(resultado['citacoesNaoConferidas'])}: {resultado['citacoesNaoConferidas']}"
    assert len(resultado["verificarRestantes"]) == 2, \
        f"esperado 2 [VERIFICAR], obtido {len(resultado['verificarRestantes'])}"

    # Saída ASCII: a régua também roda em consoles Windows em cp1252.
    print("[OK] Test sintético passou")


def test_f7_campos_real():
    """Testa a fonte N3 contra o acervo hash-bound, sem depender da rede.

    O gate de produção continua ``require_live=True``. A reprodução HTTPS e a
    rejeição de manifesto fabricado são cobertas por test_forja_anti_cheat.py.
    """

    md_path = forja_acervo.caminho("fonte-n3-memorial-resp")
    if md_path is None:
        # Em pytest, "não verifiquei" é skip e não falha: falha diz que algo
        # piorou, e o que houve foi o teste não ter sido exercido. O motivo vai
        # junto, para que a ausência apareça em vez de sumir.
        if not forja_acervo.autos_disponiveis():
            import pytest
            pytest.skip(forja_acervo.motivo_da_ausencia_dos_autos())
        raise AssertionError(forja_acervo.motivo_da_ausencia("fonte-n3-memorial-resp"))

    assert md_path.exists(), f"fonte N3 não encontrada: {md_path}"

    md_texto = md_path.read_text(encoding="utf-8")
    resultado = metricas_f7(md_texto, require_live=False)

    print("\n=== Resultado F7 (fonte N3 CASO-02) ===")
    print(f"Citações totais: {resultado['citacoesTotal']}")
    print(f"Citações conferidas: {resultado['citacoesConferidasEmFonte']}")
    print(f"Citações não conferidas ({len(resultado['citacoesNaoConferidas'])}):")
    for cit in resultado["citacoesNaoConferidas"]:
        print(f"  - {cit}")

    assert resultado["citacoesTotal"] > 0, "nenhuma citação encontrada (erro no padrão de regex)"
    # O inventário v2 enxerga também o número CNJ, artigos e diplomas legais.
    # Os três itens não têm captura oficial registrada neste corpus e devem
    # permanecer nominalmente bloqueados; escondê-los criaria falso-verde.
    esperado = forja_acervo.valor("f7-citacoes-sem-lastro")
    assert esperado is not None, forja_acervo.motivo_da_ausencia("f7-citacoes-sem-lastro")
    assert resultado["citacoesNaoConferidas"] == esperado, (
        "mudou o conjunto conhecido de citações sem lastro; auditar antes de aceitar")
    assert resultado["verificarRestantes"] == [], "a fonte N3 não pode conter marcador [VERIFICAR]"
    # nota 10/07/2026: o art. 343-A do RISTJ EXISTE (ER 53/2026); a fonte N3
    # do memorial CASO-02 optou por não citá-lo (memorial não é petição inicial
    # nem recursal). Este guarda só detecta reintrodução silenciosa — se a
    # citação voltar por decisão deliberada, atualizar este teste.
    assert "343-A" not in md_texto, "a fonte N3 reintroduziu o art. 343-A sem decisao registrada"
    assert "22 milhões" not in md_texto, "a fonte N3 reintroduziu o cálculo superado"
    assert resultado["autoridadesDecisivasComVigenciaConferida"] is None, \
        "campo autoridades deve ser None (preenchido manualmente)"

    print("[VERIFICAR]: nenhum encontrado")
    print("[OK] Test com a fonte N3 passou")


if __name__ == "__main__":
    test_f7_campos_sintetico()
    test_f7_campos_real()
    print("\n[OK] Todos os testes passaram")
