from __future__ import annotations

import importlib.util
from pathlib import Path

MODULE_PATH = Path(__file__).with_name("forja_pendencias_utilidade_candidate.py")
SPEC = importlib.util.spec_from_file_location("pendencias_candidate", MODULE_PATH)
assert SPEC and SPEC.loader
candidate = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(candidate)


def base_payload() -> dict:
    return {
        "protocolVersion": candidate.PROTOCOL_VERSION,
        "productObjective": "Entregar parecer técnico com conclusões delimitadas.",
        "deliveryDecision": "proceed",
        "lawyerMessage": (
            "Encaminho o trabalho com o acervo disponível. Documento posterior poderá "
            "justificar ajuste pontual; o valor final ainda não está certificado."
        ),
        "mentionedItemIds": ["P1"],
        "items": [
            {
                "id": "P1",
                "description": "Planilha nativa não recebida.",
                "classification": "essential_to_claim",
                "affectedClaim": "certificação do valor final",
                "consequence": "não certificar o valor enquanto o cálculo não for reproduzido",
                "treatment": "qualify_claim",
                "requestBeforeDelivery": False,
            },
            {
                "id": "P2",
                "description": "Certidão que apenas reforçaria a cronologia.",
                "classification": "useful_nonblocking",
                "affectedClaim": "",
                "consequence": "",
                "treatment": "deliver_and_optional_adendum",
                "requestBeforeDelivery": False,
            },
        ],
    }


def test_caso_misto_libera_produto_e_limita_afirmacao():
    assert candidate.validate(base_payload()) == []


def test_pendencia_apenas_util_nao_pode_gerar_espera():
    payload = base_payload()
    payload["items"][1]["requestBeforeDelivery"] = True
    assert any("não pode atrasar" in error for error in candidate.validate(payload))


def test_item_irrelevante_nao_aparece_na_mensagem():
    payload = base_payload()
    payload["items"][1].update(
        classification="irrelevant",
        treatment="drop",
        requestBeforeDelivery=False,
    )
    payload["mentionedItemIds"].append("P2")
    assert any("não pode aparecer" in error for error in candidate.validate(payload))


def test_bloqueador_do_produto_exige_hold():
    payload = base_payload()
    payload["items"][0].update(
        classification="essential_to_product",
        treatment="hold_product",
        requestBeforeDelivery=True,
    )
    assert any("deliveryDecision deve ser hold" in error for error in candidate.validate(payload))


def test_afirmacao_essencial_tem_de_ser_excluida_ou_qualificada():
    payload = base_payload()
    payload["items"][0]["treatment"] = "deliver_and_optional_adendum"
    assert any("exige excluir ou qualificar" in error for error in candidate.validate(payload))


def test_mensagem_nao_vira_lista_de_pendencias():
    payload = base_payload()
    payload["items"].append(
        {
            "id": "P3",
            "description": "Fonte útil.",
            "classification": "useful_nonblocking",
            "affectedClaim": "",
            "consequence": "",
            "treatment": "deliver_and_optional_adendum",
            "requestBeforeDelivery": False,
        }
    )
    payload["mentionedItemIds"] = ["P1", "P2", "P3"]
    assert any("mais de duas" in error for error in candidate.validate(payload))


def test_mensagem_acima_de_setenta_palavras_reprova():
    payload = base_payload()
    payload["lawyerMessage"] = "palavra " * 71
    assert any("70 palavras" in error for error in candidate.validate(payload))

