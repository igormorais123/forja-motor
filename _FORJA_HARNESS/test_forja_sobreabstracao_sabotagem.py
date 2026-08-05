# -*- coding: utf-8 -*-
"""
test_forja_sobreabstracao_sabotagem.py — Teste de sabotagem do gate S5.

Injeta afirmações de jurisprudência sem citação nominal em peças reais e valida
que o gate detecta corretamente. Controle positivo (verificação que o gate funciona).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from forja_verificador import gate_s5_sobreabstracao


def test_sabotagem_simples():
    """Injeta casos de violação óbvia."""
    casos_teste = [
        # Caso 1: "jurisprudência pacífica" isolada
        {
            "nome": "jurisprudência pacífica sem número",
            "texto": (
                "A jurisprudência pacífica firmou que a coisa julgada é absoluta. "
                "Portanto, não há recurso possível nesta matéria."
            ),
            "esperado": True  # deve detectar
        },
        # Caso 2: "entendimento consolidado" sem citação
        {
            "nome": "entendimento consolidado genérico",
            "texto": (
                "É entendimento consolidado que a responsabilidade da Fazenda Pública "
                "exige fato danoso e nexo causal. Aplicam-se os critérios ordinários da "
                "indenização contratual."
            ),
            "esperado": True  # deve detectar
        },
        # Caso 3: "as Cortes Superiores firmaram" sem número
        {
            "nome": "Cortes Superiores genérico",
            "texto": (
                "As Cortes Superiores firmaram que o prazo prescricional é de dez anos. "
                "Logo, a ação prescreveu."
            ),
            "esperado": True  # deve detectar
        },
        # Caso 4: COM citação nominal — deve PASSAR
        {
            "nome": "jurisprudência pacífica COM número",
            "texto": (
                "A jurisprudência pacífica firmou que a coisa julgada é absoluta. "
                "Nesse sentido, REsp nº 1.234.567/SP estabeleceu que o precedente vincula. "
                "Portanto, não há recurso possível."
            ),
            "esperado": False  # não deve detectar
        },
        # Caso 5: Citação nomina no parágrafo seguinte — deve PASSAR
        {
            "nome": "jurisprudência com número no parágrafo seguinte",
            "texto": (
                "A jurisprudência pacífica firmou que a coisa julgada é absoluta.\n\n"
                "Nesse sentido, REsp nº 1.234.567/SP estabeleceu que o precedente vincula."
            ),
            "esperado": False  # não deve detectar
        },
        # Caso 6: Súmula citada inline — deve PASSAR
        {
            "nome": "jurisprudência com Súmula",
            "texto": (
                "A jurisprudência pacífica, em particular a Súmula 7 do STJ, "
                "não permite reexame de prova em recurso extraordinário."
            ),
            "esperado": False  # não deve detectar (Súmula 7 é citada)
        },
        # Caso 7: "é pacífico" sozinho
        {
            "nome": "é pacífico",
            "texto": (
                "É pacífico na doutrina que o abuso de direito gera indenização. "
                "Desse modo, condenamos o réu ao pagamento de reparos."
            ),
            "esperado": True  # deve detectar
        },
    ]

    erros = []
    acertos = 0

    print("Testando detecção de violações (sabotagem)...\n")

    for caso in casos_teste:
        violacoes = gate_s5_sobreabstracao(caso["texto"])
        detectou = len(violacoes) > 0

        if detectou == caso["esperado"]:
            status = "✓ PASSOU"
            acertos += 1
        else:
            status = "✗ FALHOU"
            erros.append(caso)

        print(f"  {status}: {caso['nome']}")
        if violacoes:
            print(f"         Achado: {violacoes[0]['trecho'][:80]}")

    print(f"\nResultado: {acertos}/{len(casos_teste)} testes passaram")

    if erros:
        print(f"\nFalhas:")
        for erro in erros:
            print(f"  - {erro['nome']} (esperado={'detectar' if erro['esperado'] else 'passar'}, obteve={'detectado' if not erro['esperado'] else 'passou'})")
        return False

    return True


def test_evidencia_contexto_longo():
    """A evidência deve apontar para o achado mesmo após um prefixo longo."""
    texto = ("Parágrafo preliminar sem afirmação jurisprudencial.\n\n" * 80) + (
        "A jurisprudência pacífica firmou que a tese é aplicável."
    )
    violacoes = gate_s5_sobreabstracao(texto)
    ok = bool(violacoes) and "jurisprudência pacífica" in violacoes[0].get("trecho", "")
    print(f"\nEvidência com prefixo longo: {'✓ PASSOU' if ok else '✗ FALHOU'}")
    return ok


if __name__ == "__main__":
    if test_sabotagem_simples() and test_evidencia_contexto_longo():
        print("\nTESTE DE SABOTAGEM PASSOU — gate está funcional")
        sys.exit(0)
    else:
        print("\nTESTE DE SABOTAGEM FALHOU — gate não está funcionando corretamente")
        sys.exit(1)
