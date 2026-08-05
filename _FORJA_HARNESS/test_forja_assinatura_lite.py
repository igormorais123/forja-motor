# -*- coding: utf-8 -*-
"""Regressão da feature FORJA-ASSINATURA Lite (W1 — contratos e modo off).

Duas obrigações desta onda, e a primeira é a que importa: **em `off`, nada muda**.
Contrato novo que altera comportamento antes de ser ligado não é contrato, é
mudança disfarçada. A segunda é que os validadores recusem payload vazio e as
proibições do PRD tenham teste negativo correspondente.
"""

import json
import tempfile
import unittest
from copy import deepcopy
from datetime import datetime
from pathlib import Path

import forja_n4_validate as n4v
from forja_exploracao_100 import (
    DIALECTIC_PROTOCOL,
    record_response,
    render_consultation,
    select_consultation_questions,
    selectable_findings,
    validate_dialectic,
)
from forja_legal_search import LegalSearchError, TeiaJusBridge
from forja_n4_common import ARTIFACT_SPECS
from forja_n4_invalidation import DEPENDENCIES
from forja_n3_common import ForjaN3Error, atomic_write_json
from forja_official_sources import source_excerpt_sha256
from forja_precedente import (
    ANCHOR_PROTOCOL,
    VIGENCIA_STATES,
    failed_anchor_routes,
    validate_anchor_cards,
    validate_legal_research_trace,
)
from forja_reasoning import (
    FAMILIAS_DE_TESE,
    nivel_probatorio,
    validate_brief_references,
    validate_question_tree,
    validate_recipient_map,
    validate_signature_brief,
)

FORJA = Path(__file__).resolve().parent


def mapa_valido() -> dict:
    return {
        "protocolVersion": "FORJA-RECIPIENT-MAP-v1",
        "recipient": {
            "court": "STJ", "organ": "Primeira Turma", "rapporteur": "Ministro X",
            "identityStatus": "confirmed", "sourceIds": ["SRC-ACORDAO-1"],
        },
        "competence": {"status": "confirmed", "basis": "art. 105, III, a, da CF",
                       "sourceIds": ["SRC-ACORDAO-1"]},
        "prevention": {"status": "unknown", "originCaseId": None, "basis": None, "sourceIds": []},
        "composition": {"status": "confirmed", "members": [{"name": "Ministro X"}],
                        "checkedAt": "2026-07-25T10:00:00-03:00",
                        "validUntil": "2026-07-26T10:00:00-03:00",
                        "sourceIds": ["SRC-COMPOSICAO-OFICIAL"]},
        "positions": [{
            "positionId": "POS-1", "level": "rapporteur", "issueId": "ISS-1",
            "decisionIds": ["DEC-1"], "status": "favoravel",
            "asOf": "2026-05-01", "summary": "aplica a tese", "sourceIds": ["SRC-1"],
        }],
        "divergences": [], "appellateRoute": {}, "limitations": [],
        "topologyScopeReason": None,
    }


def brief_valido() -> dict:
    return {
        "protocolVersion": "FORJA-SIGNATURE-BRIEF-v1",
        "decisiveQuestion": "O título executivo incorporou a alíquota da Resolução CIEX?",
        "demonstratedConsequence": "define se a liquidação parte de zero ou de 12%",
        "routes": [
            {"routeId": "R1", "thesisIds": ["T1"], "description": "CIEX integra o título executivo",
             "anchorCandidateIds": ["ANC-1"], "bestObjection": "o dispositivo não nomeia a CIEX",
             "response": "pedido e causa de pedir se leem com o dispositivo",
             "decision": "selected", "decisionReason": "melhor lastro documental"},
            {"routeId": "R2", "thesisIds": ["T2"], "description": "alíquota aberta para a liquidação",
             "anchorCandidateIds": ["ANC-2"], "bestObjection": "o AI conexo tem outro título",
             "response": "usa-se como ratio persuasiva", "decision": "rejected",
             "decisionReason": "mais frágil no ponto decisivo"},
        ],
        "selectedRouteId": "R1",
        "humanDecisionId": "DEC-HUMANA-1",
        "singleRouteReason": None, "complexityReason": None,
        "motherSentence": "A alíquota já estava no pedido.",
        "anchorCandidates": [
            {"anchorCandidateId": "ANC-1", "identity": "STJ, REsp 1.111.111/DF, 1ª Turma",
             "expectedOperation": "apply", "fullTextObtained": True},
            {"anchorCandidateId": "ANC-2", "identity": "TRF1, AC 0000000-00.2000.4.01.3400",
             "expectedOperation": "distinguish", "fullTextObtained": False},
        ],
        "decisiveFactIds": ["F1"], "decisiveDocumentIds": ["D1"],
        "mandatoryContent": ["enfrentar a Informação Fiscal 1.690"],
        "blockingIssues": [],
        "thesisFamilyCoverage": [
            {"family": f, "status": "nao_aplicavel", "reason": "fora do objeto da liquidação", "routeIds": []}
            for f in FAMILIAS_DE_TESE
        ],
    }


class ModoOffTests(unittest.TestCase):
    """Em `off`, a feature não existe para efeito prático."""

    def test_namespace_declarado_na_config_nasce_off(self):
        config = json.loads((FORJA / "state" / "FORJA_N3_CONFIG.json").read_text(encoding="utf-8"))
        espaco = config["forjaAssinaturaLite"]
        self.assertEqual("off", espaco["mode"])
        self.assertEqual([], espaco["pilotCases"])
        self.assertEqual("manual_review_only", espaco["consultationOutboundPolicy"])
        self.assertFalse(espaco["allowPaidResearch"])

    def test_namespace_ausente_equivale_a_off(self):
        with tempfile.TemporaryDirectory() as temp:
            _, efetivo = n4v.effective_signature_lite_mode({}, Path(temp))
            self.assertEqual("off", efetivo)

    def test_modo_desconhecido_falha(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(ForjaN3Error):
                n4v.effective_signature_lite_mode(
                    {"forjaAssinaturaLite": {"mode": "ligado"}}, Path(temp))

    def test_pilot_blocking_so_bloqueia_caso_nomeado(self):
        with tempfile.TemporaryDirectory() as temp:
            caso = Path(temp) / "case-alvo"
            caso.mkdir()
            config = {"forjaAssinaturaLite": {"mode": "pilot_blocking", "pilotCases": ["case-alvo"]}}
            self.assertEqual("pilot_blocking", n4v.effective_signature_lite_mode(config, caso)[1])
            outro = Path(temp) / "case-fora"
            outro.mkdir()
            self.assertEqual("shadow", n4v.effective_signature_lite_mode(config, outro)[1])

    def test_off_nao_exige_os_artefatos_novos(self):
        """A prova central da onda: em off, o conjunto requerido não cresce."""
        with tempfile.TemporaryDirectory() as temp:
            caso = Path(temp) / "case-x"
            caso.mkdir()
            config = json.loads((FORJA / "state" / "FORJA_N3_CONFIG.json").read_text(encoding="utf-8"))
            requeridos = n4v._required_files(config)
            _, modo = n4v.effective_signature_lite_mode(config, caso)
            if modo != "off":
                requeridos.update(n4v.SIGNATURE_LITE_FILES)
            self.assertEqual("off", modo)
            self.assertNotIn("F3_MAPA_DESTINATARIO.json", requeridos)
            self.assertNotIn("F4_SIGNATURE_BRIEF.json", requeridos)

    def test_modo_ligado_exige_os_dois(self):
        config = {"forjaAssinaturaLite": {"mode": "shadow"}}
        with tempfile.TemporaryDirectory() as temp:
            caso = Path(temp)
            _, modo = n4v.effective_signature_lite_mode(config, caso)
            self.assertEqual("shadow", modo)
        self.assertEqual(
            {"F3_MAPA_DESTINATARIO.json", "F4_SIGNATURE_BRIEF.json"},
            n4v.SIGNATURE_LITE_FILES,
        )

    def test_modo_do_n4_nao_foi_alterado(self):
        """A generalização não pode ter mexido no namespace que tem pilotos vivos."""
        config = json.loads((FORJA / "state" / "FORJA_N3_CONFIG.json").read_text(encoding="utf-8"))
        self.assertEqual("pilot_blocking", config["n4"]["mode"])
        self.assertEqual(4, len(config["n4"]["pilotCases"]))


class CatalogoTests(unittest.TestCase):
    def test_catalogo_e_specs_coincidem(self):
        catalogo = json.loads((FORJA / "n4_schemas" / "ARTIFACT_CATALOG.json").read_text(encoding="utf-8"))
        self.assertEqual(set(ARTIFACT_SPECS), set(catalogo["artifacts"]))

    def test_novos_tipos_tem_schema_gerado(self):
        catalogo = json.loads((FORJA / "n4_schemas" / "ARTIFACT_CATALOG.json").read_text(encoding="utf-8"))
        for nome, tipo in (("F3_MAPA_DESTINATARIO.json", "recipient_map"),
                           ("F4_SIGNATURE_BRIEF.json", "signature_brief")):
            entrada = catalogo["artifacts"][nome]
            self.assertEqual(tipo, entrada["type"])
            self.assertTrue((FORJA / "n4_schemas" / entrada["schema"]).is_file())

    def test_saidas_novas_registradas_nas_extensoes(self):
        ext = json.loads((FORJA / "phase_contracts_n4" / "EXTENSIONS.json").read_text(encoding="utf-8"))
        self.assertIn("recipient_map", ext["phases"]["F3"]["outputs"])
        self.assertIn("signature_brief", ext["phases"]["F4"]["outputs"])

    def test_contratos_canonicos_preservam_a_tupla_de_fases(self):
        """DA-01: nenhuma fase nova. F0-F10 continuam sendo onze."""
        contratos = sorted((FORJA / "phase_contracts").glob("F*.json"))
        self.assertEqual(11, len(contratos))


class MapaDestinatarioTests(unittest.TestCase):
    def test_mapa_valido_passa(self):
        self.assertEqual([], validate_recipient_map(mapa_valido()))

    def test_payload_vazio_nao_passa_por_omissao(self):
        # Envelope sem conteúdo não pode ser lido como mapa aprovado; o schema
        # cobre a ausência das chaves e o validador, a substância.
        self.assertEqual([], validate_recipient_map({}))
        catalogo = json.loads((FORJA / "n4_schemas" / "ARTIFACT_CATALOG.json").read_text(encoding="utf-8"))
        self.assertEqual(
            ["recipient", "competence", "prevention", "composition", "positions"],
            catalogo["artifacts"]["F3_MAPA_DESTINATARIO.json"]["keys"],
        )

    def test_identidade_confirmada_sem_fonte_bloqueia(self):
        payload = mapa_valido()
        payload["recipient"]["sourceIds"] = []
        self.assertTrue(any(f["code"] == "FAL-F3-RECIPIENT-UNSOURCED"
                            for f in validate_recipient_map(payload)))

    def test_prevencao_so_por_datajud_bloqueia(self):
        payload = mapa_valido()
        payload["prevention"] = {"status": "confirmed", "sourceIds": ["DATAJUD-ORGAO-JULGADOR"]}
        self.assertTrue(any(f["code"] == "FAL-F3-PREVENTION-DATAJUD-ONLY"
                            for f in validate_recipient_map(payload)))

    def test_composicao_confirmada_sem_data_bloqueia(self):
        payload = mapa_valido()
        payload["composition"].pop("checkedAt")
        self.assertTrue(any(f["code"] == "FAL-F3-COMPOSITION-STALE"
                            for f in validate_recipient_map(payload)))

    def test_posicao_sem_decisao_bloqueia(self):
        payload = mapa_valido()
        payload["positions"][0]["decisionIds"] = []
        self.assertTrue(any(f["code"] == "FAL-F3-POSITION-NO-DECISION"
                            for f in validate_recipient_map(payload)))

    def test_topologia_ampla_sem_justificativa_bloqueia(self):
        payload = mapa_valido()
        payload["positions"][0]["level"] = "plenary"
        self.assertTrue(any(f["code"] == "FAL-F3-TOPOLOGY-UNJUSTIFIED"
                            for f in validate_recipient_map(payload)))
        payload["topologyScopeReason"] = "a tese já foi afetada pela Corte Especial"
        self.assertFalse(any(f["code"] == "FAL-F3-TOPOLOGY-UNJUSTIFIED"
                             for f in validate_recipient_map(payload)))

    def test_desconhecido_e_estado_legitimo(self):
        """Não saber é resposta aceitável; fingir que sabe não é."""
        payload = mapa_valido()
        payload["composition"] = {"status": "unknown", "members": [], "sourceIds": []}
        payload["competence"] = {"status": "unknown", "basis": None, "sourceIds": []}
        self.assertEqual([], validate_recipient_map(payload))


def pergunta(qid="Q001", **kw):
    base = {
        "questionId": qid, "status": "blocked", "materiality": "decisive",
        "caseAnchor": "Liquidação nº 9000011-00.2018.4.04.0000/RS",
        "whyItMatters": "define o formato do produto entregue",
        "text": "O escritório tem acesso à tabela CIEX autêntica por NBM?",
        "questionType": "fact", "humanAuthority": "titular",
        "silencePolicy": "block_dependent",
        "silenceConsequence": "a alíquota permanece questão aberta na consulta",
        "downstreamTargets": ["F4"],
    }
    base.update(kw)
    return base


def arvore(*perguntas, **consulta):
    base_consulta = {
        "status": "draft", "selectedQuestionIds": [str(p["questionId"]) for p in perguntas],
        "renderedBodySha256": None, "outboundPolicy": "manual_review_only",
        "outboundReceiptId": None, "responseRefs": [], "round": 1,
        "preparedAt": "2026-07-25",
    }
    base_consulta.update(consulta)
    return {
        "caseId": "case-teste",
        "problemDefinition": "Definir o formato da consulta antes de redigir.",
        "dialecticProtocolVersion": DIALECTIC_PROTOCOL,
        "questions": list(perguntas),
        "dialecticConsultation": base_consulta,
        "decisionLedger": [],
    }


class SelecaoDialeticaTests(unittest.TestCase):
    """Não se pergunta o que o acervo já responde."""

    def test_pergunta_respondida_pelo_acervo_e_rejeitada(self):
        p = pergunta(alreadyResearched=["ADENDO-24-07"])
        self.assertTrue(any(f["code"] == "FAL-F2B-REDUNDANT" for f in selectable_findings(p)))

    def test_questao_ja_respondida_nao_vai_a_consulta(self):
        p = pergunta(status="answered")
        self.assertTrue(any(f["code"] == "FAL-F2B-NOT-BLOCKED" for f in selectable_findings(p)))

    def test_pergunta_sem_consequencia_do_silencio_e_rejeitada(self):
        p = pergunta(silenceConsequence="")
        self.assertTrue(any(f["code"] == "FAL-F2B-NO-SILENCE-POLICY" for f in selectable_findings(p)))

    def test_fato_nao_admite_valor_padrao(self):
        for tipo in ("fact", "evidence", "authorization"):
            p = pergunta(questionType=tipo, silencePolicy="explicit_reversible_default")
            self.assertTrue(any(f["code"] == "FAL-F2B-FACT-DEFAULT" for f in selectable_findings(p)),
                            f"tipo {tipo} deveria recusar default")

    def test_estrategia_admite_padrao_reversivel(self):
        p = pergunta(questionType="strategy", silencePolicy="explicit_reversible_default")
        self.assertFalse(any(f["code"] == "FAL-F2B-FACT-DEFAULT" for f in selectable_findings(p)))

    def test_pergunta_sem_autoridade_humana_e_rejeitada(self):
        p = pergunta(humanAuthority="quem_souber")
        self.assertTrue(any(f["code"] == "FAL-F2B-NO-AUTHORITY" for f in selectable_findings(p)))

    def test_selecao_e_deterministica(self):
        perguntas = [
            pergunta("Q050", questionType="strategy"),
            pergunta("Q010", questionType="objective"),
            pergunta("Q030", questionType="authorization"),
        ]
        primeira, _ = select_consultation_questions({"questions": perguntas})
        segunda, _ = select_consultation_questions({"questions": list(reversed(perguntas))})
        self.assertEqual(primeira, segunda)
        self.assertEqual("Q010", primeira[0])  # identidade do produto vem primeiro

    def test_volume_alto_alerta_sem_truncar(self):
        perguntas = [pergunta(f"Q{i:03d}", questionType="strategy") for i in range(1, 16)]
        selecionadas, achados = select_consultation_questions({"questions": perguntas})
        self.assertEqual(15, len(selecionadas))  # nada é cortado para caber num número
        self.assertTrue(any(f["code"] == "FAL-F2B-QUESTION-VOLUME" for f in achados))
        self.assertTrue(all(f["severity"] == "p1" for f in achados))


class ConsultaDialeticaTests(unittest.TestCase):
    def test_arvore_sem_bloco_dialetico_continua_valida(self):
        self.assertEqual([], validate_dialectic({"questions": []}))

    def test_envio_autonomo_e_recusado(self):
        payload = arvore(pergunta(), outboundPolicy="auto_send")
        self.assertTrue(any(f["code"] == "FAL-F2B-OUTBOUND-UNAUTHORIZED"
                            for f in validate_dialectic(payload)))

    def test_enviada_sem_recibo_humano_e_recusada(self):
        payload = arvore(pergunta(), status="sent", outboundReceiptId=None)
        self.assertTrue(any(f["code"] == "FAL-F2B-OUTBOUND-UNAUTHORIZED"
                            for f in validate_dialectic(payload)))

    def test_consulta_bem_formada_passa(self):
        self.assertEqual([], validate_dialectic(arvore(pergunta())))

    def test_declaracao_do_escritorio_nao_vira_fato_sem_lastro(self):
        payload = arvore(pergunta("Q001", questionType="fact"))
        payload["decisionLedger"] = [{
            "decisionId": "DEC-1", "questionIds": ["Q001"], "responseAuthor": "Fábio",
            "channel": "email", "epistemicStatus": "office_declaration",
            "decision": "a tabela existe no acervo", "decidedAt": "2026-07-26",
        }]
        self.assertTrue(any(f["code"] == "FAL-F2B-OFFICE-AS-FACT"
                            for f in validate_dialectic(payload)))

    def test_declaracao_com_lastro_documental_passa(self):
        payload = arvore(pergunta("Q001", questionType="fact"))
        payload["decisionLedger"] = [{
            "decisionId": "DEC-1", "questionIds": ["Q001"], "responseAuthor": "Fábio",
            "channel": "email", "epistemicStatus": "office_declaration",
            "supportIds": ["DOC-CIEX-1"], "decision": "tabela juntada",
            "decidedAt": "2026-07-26",
        }]
        self.assertFalse(any(f["code"] == "FAL-F2B-OFFICE-AS-FACT"
                             for f in validate_dialectic(payload)))

    def test_decisao_sem_autor_ou_canal_e_recusada(self):
        payload = arvore(pergunta())
        payload["decisionLedger"] = [{
            "decisionId": "DEC-1", "questionIds": ["Q001"], "responseAuthor": "",
            "channel": "telepatia", "epistemicStatus": "office_declaration",
        }]
        self.assertTrue(any(f["code"] == "FAL-F2B-DECISION-NO-AUTHOR"
                            for f in validate_dialectic(payload)))

    def test_respondida_com_pendencia_e_recusada(self):
        payload = arvore(pergunta("Q001"), pergunta("Q002"), status="answered",
                         outboundReceiptId="REC-1")
        payload["decisionLedger"] = [{
            "decisionId": "DEC-1", "questionIds": ["Q001"], "responseAuthor": "Fábio",
            "channel": "email", "epistemicStatus": "strategic_hypothesis",
            "supportIds": [],
        }]
        self.assertTrue(any(f["code"] == "FAL-F2B-PARTIAL-CLOSED"
                            for f in validate_dialectic(payload)))


class RenderizacaoTests(unittest.TestCase):
    def test_render_preserva_acentuacao_e_pontuacao(self):
        texto = render_consultation(arvore(pergunta()))
        self.assertIn("O escritório tem acesso à tabela CIEX autêntica por NBM?", texto)
        self.assertIn("Liquidação nº 9000011-00.2018.4.04.0000/RS", texto)

    def test_render_recusa_pergunta_sem_consequencia(self):
        with self.assertRaises(ValueError) as erro:
            render_consultation(arvore(pergunta(silenceConsequence="")))
        self.assertIn("consequência", str(erro.exception))

    def test_render_recusa_arvore_sem_selecao(self):
        with self.assertRaises(ValueError):
            render_consultation(arvore(pergunta(), selectedQuestionIds=[]))

    def test_render_nomeia_o_que_ficou_de_fora(self):
        payload = arvore(pergunta("Q001"))
        payload["questions"].append(pergunta("Q099", alreadyResearched=["ADENDO-24-07"]))
        texto = render_consultation(payload)
        self.assertIn("Q099", texto)
        self.assertIn("acervo já responde", texto)

    def test_render_e_estavel_para_a_mesma_arvore(self):
        payload = arvore(pergunta("Q001"), pergunta("Q002", questionType="strategy"))
        self.assertEqual(render_consultation(payload), render_consultation(payload))


class LedgerAppendOnlyTests(unittest.TestCase):
    def test_resposta_parcial_mantem_pendencia(self):
        payload = arvore(pergunta("Q001"), pergunta("Q002"))
        atualizado = record_response(payload, {
            "decisionId": "DEC-1", "questionIds": ["Q001"], "responseAuthor": "Fábio",
            "channel": "email", "epistemicStatus": "strategic_hypothesis",
        })
        consulta = atualizado["dialecticConsultation"]
        self.assertEqual("partially_answered", consulta["status"])
        self.assertEqual(["Q002"], consulta["remainingQuestionIds"])

    def test_todas_respondidas_fecham_a_consulta(self):
        payload = arvore(pergunta("Q001"))
        atualizado = record_response(payload, {
            "decisionId": "DEC-1", "questionIds": ["Q001"], "responseAuthor": "Fábio",
            "channel": "email", "epistemicStatus": "strategic_hypothesis",
        })
        self.assertEqual("answered", atualizado["dialecticConsultation"]["status"])

    def test_ledger_nao_e_reescrito(self):
        payload = arvore(pergunta("Q001"))
        entrada = {"decisionId": "DEC-1", "questionIds": ["Q001"], "responseAuthor": "Fábio",
                   "channel": "email", "epistemicStatus": "strategic_hypothesis"}
        atualizado = record_response(payload, entrada)
        with self.assertRaises(ValueError) as erro:
            record_response(atualizado, entrada)
        self.assertIn("não é reescrito", str(erro.exception))

    def test_segunda_rodada_acumula_sem_apagar(self):
        payload = arvore(pergunta("Q001"), pergunta("Q002"))
        payload = record_response(payload, {
            "decisionId": "DEC-1", "questionIds": ["Q001"], "responseAuthor": "Fábio",
            "channel": "email", "epistemicStatus": "strategic_hypothesis"})
        payload = record_response(payload, {
            "decisionId": "DEC-2", "questionIds": ["Q002"], "responseAuthor": "Fábio",
            "channel": "whatsapp", "epistemicStatus": "office_declaration"})
        self.assertEqual(2, len(payload["decisionLedger"]))
        self.assertEqual("answered", payload["dialecticConsultation"]["status"])


class EstadosCanonicosTests(unittest.TestCase):
    def test_estados_legados_foram_removidos(self):
        """`retired` e `accepted_by_human` davam rota de fuga ao gate."""
        fonte = (FORJA / "forja_reasoning.py").read_text(encoding="utf-8")
        self.assertNotIn('"accepted_by_human"', fonte)
        self.assertNotIn('item.get("status") == "retired"', fonte)

    def test_questao_material_sem_resolucao_e_pega(self):
        payload = {"questions": [{
            "questionId": "Q001", "materiality": "decisive", "status": "not_applicable",
            "lens": "fatos_cronologia", "text": "pergunta material",
        }], "coverage": {"total": 1, "material": 1, "answeredMaterial": 0, "blockedMaterial": 0}}
        self.assertTrue(any(f["code"] == "N4-Q-UNRESOLVED"
                            for f in validate_question_tree(payload)))


class NivelProbatorioTests(unittest.TestCase):
    """Descoberta não é prova — a distinção decide o que o mapa pode afirmar."""

    def test_integra_decide_ementa_corrobora_metadado_orienta(self):
        self.assertEqual("decide", nivel_probatorio("acordao_integra"))
        self.assertEqual("corrobora", nivel_probatorio("ementa"))
        self.assertEqual("orienta", nivel_probatorio("metadado_datajud"))

    def test_tipo_desconhecido_nunca_e_promovido_a_prova(self):
        self.assertEqual("orienta", nivel_probatorio("fonte_que_alguem_inventou"))
        self.assertEqual("orienta", nivel_probatorio(None))

    def test_prevencao_por_metadado_catalogado_bloqueia(self):
        payload = mapa_valido()
        payload["sourceCatalog"] = [{"sourceId": "SRC-META", "kind": "metadado_datajud"}]
        payload["prevention"] = {"status": "confirmed", "sourceIds": ["SRC-META"]}
        self.assertTrue(any(f["code"] == "FAL-F3-PREVENTION-DATAJUD-ONLY"
                            for f in validate_recipient_map(payload)))

    def test_prevencao_por_decisao_integral_passa(self):
        payload = mapa_valido()
        payload["sourceCatalog"] = [{"sourceId": "SRC-DEC", "kind": "decisao_integra"}]
        payload["prevention"] = {"status": "confirmed", "originCaseId": "0001",
                                 "basis": "decisão de prevenção", "sourceIds": ["SRC-DEC"]}
        self.assertFalse(any(f["code"] == "FAL-F3-PREVENTION-DATAJUD-ONLY"
                             for f in validate_recipient_map(payload)))

    def test_composicao_por_metadado_exige_ato_oficial(self):
        payload = mapa_valido()
        payload["sourceCatalog"] = [{"sourceId": "SRC-META", "kind": "metadado_datajud"}]
        payload["composition"]["sourceIds"] = ["SRC-META"]
        self.assertTrue(any(f["code"] == "FAL-F3-COMPOSITION-NO-OFFICIAL-SOURCE"
                            for f in validate_recipient_map(payload)))


class FreshnessTests(unittest.TestCase):
    """`status=confirmed` autodeclarado não sobrevive ao relógio."""

    def test_composicao_dentro_do_limite_passa(self):
        payload = mapa_valido()
        payload["composition"]["checkedAt"] = "2026-07-25T10:00:00-03:00"
        agora = datetime.fromisoformat("2026-07-25T20:00:00-03:00")
        self.assertEqual([], validate_recipient_map(payload, freshness_hours=24, agora=agora))

    def test_composicao_vencida_e_detectada(self):
        payload = mapa_valido()
        payload["composition"]["checkedAt"] = "2026-07-20T10:00:00-03:00"
        agora = datetime.fromisoformat("2026-07-25T20:00:00-03:00")
        achados = validate_recipient_map(payload, freshness_hours=24, agora=agora)
        self.assertTrue(any(f["code"] == "FAL-F3-COMPOSITION-STALE" for f in achados))

    def test_sem_limite_configurado_nao_inventa_prazo(self):
        payload = mapa_valido()
        payload["composition"]["checkedAt"] = "2020-01-01T10:00:00-03:00"
        self.assertEqual([], validate_recipient_map(payload))

    def test_limite_vem_da_configuracao_da_feature(self):
        config = json.loads((FORJA / "state" / "FORJA_N3_CONFIG.json").read_text(encoding="utf-8"))
        self.assertEqual(24, config["forjaAssinaturaLite"]["recipientMapFreshnessHours"])


class TeiaJusPolicyTests(unittest.TestCase):
    """Allowlist ampliada, sem ação paga e sem mutação."""

    def setUp(self):
        self.config = json.loads((FORJA / "FORJA_SEARCH_CONFIG.json").read_text(encoding="utf-8"))
        self.policy = self.config["policy"]

    def test_acoes_de_pesquisa_nao_pagas_entraram(self):
        for acao in ("research_sources", "research_plan", "research_search", "research_mission_get"):
            self.assertIn(acao, self.policy["readActions"])

    def test_acoes_pagas_sao_negadas_explicitamente(self):
        for acao in ("research_mission", "captcha_solve", "apify_contact_enrich"):
            self.assertIn(acao, self.policy["deniedActions"])
            self.assertNotIn(acao, self.policy["readActions"])
            self.assertNotIn(acao, self.policy["mutationActions"])

    def test_negada_e_recusada_antes_da_allowlist(self):
        """Mesmo se alguém a incluir em readActions por engano, a negação prevalece."""
        bridge = TeiaJusBridge.__new__(TeiaJusBridge)
        bridge.config = {"policy": {
            "readActions": ["research_mission"],           # inclusão distraída
            "mutationActions": [],
            "deniedActions": ["research_mission"],
            "deniedReason": "ação read_paid",
        }}
        with self.assertRaises(LegalSearchError) as erro:
            TeiaJusBridge.execute(bridge, "research_mission")
        self.assertIn("negada", str(erro.exception))

    def test_mutacao_listada_exige_autorizacao_explicita(self):
        for acao in ("collect", "stj_collect"):
            self.assertIn(acao, self.policy["mutationActions"])
        self.assertTrue(self.policy["mutationRequiresExplicitFlag"])
        self.assertFalse(self.policy["arbitraryShell"])

    def test_mutacao_nao_listada_e_recusada_pela_allowlist(self):
        """`cgu_update` existe no TeiaJus e a FORJA nunca a listou. Continua fora."""
        self.assertNotIn("cgu_update", self.policy["mutationActions"])
        self.assertNotIn("cgu_update", self.policy["readActions"])
        bridge = TeiaJusBridge.__new__(TeiaJusBridge)
        bridge.config = {"policy": self.policy}
        with self.assertRaises(LegalSearchError) as erro:
            TeiaJusBridge.execute(bridge, "cgu_update", allow_mutation=True)
        self.assertIn("allowlist", str(erro.exception))

    def test_ampliacao_nao_trouxe_acao_de_escrita(self):
        novas = {"research_sources", "research_plan", "research_search", "research_mission_get"}
        self.assertEqual(set(), novas & set(self.policy["mutationActions"]))

    def test_pesquisa_paga_desligada_na_feature(self):
        config = json.loads((FORJA / "state" / "FORJA_N3_CONFIG.json").read_text(encoding="utf-8"))
        self.assertFalse(config["forjaAssinaturaLite"]["allowPaidResearch"])


class SignatureBriefTests(unittest.TestCase):
    def test_brief_valido_passa(self):
        self.assertEqual([], validate_signature_brief(brief_valido()))

    def test_sem_pergunta_decisiva_bloqueia(self):
        payload = brief_valido()
        payload["decisiveQuestion"] = "   "
        self.assertTrue(any(f["code"] == "FAL-F4-NO-DECISIVE-QUESTION"
                            for f in validate_signature_brief(payload)))

    def test_rotas_estruturalmente_duplicadas_bloqueiam(self):
        payload = brief_valido()
        payload["routes"][1] = deepcopy(payload["routes"][0])
        payload["routes"][1]["routeId"] = "R2"
        payload["routes"][1]["decision"] = "rejected"
        payload["routes"][1]["description"] = "outra redação para a mesma coisa"
        self.assertTrue(any(f["code"] == "FAL-F4-ROUTE-DUPLICATE"
                            for f in validate_signature_brief(payload)))

    def test_rota_unica_exige_motivo(self):
        payload = brief_valido()
        payload["routes"] = payload["routes"][:1]
        self.assertTrue(any(f["code"] == "FAL-F4-ROUTE-ARTIFICIAL"
                            for f in validate_signature_brief(payload)))
        payload["singleRouteReason"] = "matéria de competência sem alternativa material"
        self.assertFalse(any(f["code"] == "FAL-F4-ROUTE-ARTIFICIAL"
                             for f in validate_signature_brief(payload)))

    def test_selecao_divergente_bloqueia(self):
        payload = brief_valido()
        payload["selectedRouteId"] = "R2"
        self.assertTrue(any(f["code"] == "FAL-F4-SELECTION-MISMATCH"
                            for f in validate_signature_brief(payload)))

    def test_selecao_sem_decisao_humana_bloqueia(self):
        payload = brief_valido()
        payload["humanDecisionId"] = None
        self.assertTrue(any(f["code"] == "FAL-F4-SELECTION-NO-HUMAN-DECISION"
                            for f in validate_signature_brief(payload)))

    def test_pendencia_bloqueante_impede_selecao(self):
        payload = brief_valido()
        payload["blockingIssues"] = [{"id": "B1", "detail": "tabela CIEX não localizada"}]
        self.assertTrue(any(f["code"] == "FAL-F4-BLOCKED-RELEASE"
                            for f in validate_signature_brief(payload)))

    def test_familia_de_tese_ausente_bloqueia(self):
        payload = brief_valido()
        payload["thesisFamilyCoverage"] = payload["thesisFamilyCoverage"][:-1]
        achados = validate_signature_brief(payload)
        self.assertTrue(any(f["code"] == "FAL-F4-FAMILY-MISSING" for f in achados))

    def test_descarte_de_familia_exige_motivo(self):
        payload = brief_valido()
        payload["thesisFamilyCoverage"][0]["reason"] = ""
        self.assertTrue(any(f["code"] == "FAL-F4-FAMILY-NO-REASON"
                            for f in validate_signature_brief(payload)))

    def test_sao_nove_familias_sem_minimo_numerico_de_teses(self):
        self.assertEqual(9, len(FAMILIAS_DE_TESE))
        schema = json.loads(
            (FORJA / "n4_schemas" / "f4_signature_brief.schema.json").read_text(encoding="utf-8"))
        texto = json.dumps(schema)
        self.assertNotIn("minTheses", texto)
        self.assertNotIn("minimumTheses", texto)


def ficha_de_ancora(**ajustes) -> dict:
    holding = "A alíquota fixada no título executivo integra o julgado e não se reabre na liquidação."
    card = {
        "anchor": True,
        "anchorProtocol": ANCHOR_PROTOCOL,
        "anchorId": "ANC-1",
        "routeId": "R1",
        "fullTextStatus": "verified",
        "holding": {
            "text": holding,
            "locator": "acórdão, fl. 14, item 3 do voto condutor",
            "excerptSha256": source_excerpt_sha256(holding),
        },
        "confusableObiter": ["obiter sobre juros no item 5"],
        "decisiveFacts": ["título com alíquota expressa"],
        "elementComparison": [
            {"element": "título com alíquota expressa", "verdict": "coincide com o caso"},
        ],
        "operation": "apply",
        "vigencia": "vigente",
        "precedenteContrarioConhecido": [],
        "contraryCheckedAt": "2026-07-25T10:00:00-03:00",
        "regime": {
            "legalBasis": ["CPC, art. 927, III"],
            "authorityType": "acórdão de turma",
            "dutyOrEffect": "eficácia persuasiva qualificada",
            "competentBody": "1ª Turma do STJ",
            "changePath": "superação por afetação em repetitivo",
            "validityStatus": "em vigor",
            "checkedAt": "2026-07-25T10:00:00-03:00",
        },
    }
    card.update(ajustes)
    return card


def trilha_de_pesquisa(**ajustes) -> dict:
    payload = {
        "legalResearchProtocol": "FORJA-LEGAL-SEARCH-TRACE-v1",
        "searchRuns": [{
            "queryId": "QRY-1",
            "database": "SCON/STJ",
            "endpointOrTool": "stj_search",
            "executedAt": "2026-07-25T09:00:00-03:00",
            "query": "liquidação alíquota título executivo CIEX",
            "filters": {"orgao": "1ª Seção", "periodo": "2015-2026"},
            "resultIds": ["RES-1"],
            "discarded": [{"resultId": "RES-2", "reason": "matéria tributária diversa"}],
            "negativeResult": False,
            "notSearched": ["repositórios privados"],
            "limitations": ["SCON indisponível para acórdãos anteriores a 1998"],
        }],
    }
    payload.update(ajustes)
    return payload


class TrilhaDePesquisaTests(unittest.TestCase):
    """Ausência só é probatória quando a busca que não achou está descrita."""

    def test_trilha_completa_passa(self):
        self.assertEqual([], validate_legal_research_trace(trilha_de_pesquisa()))

    def test_ledger_sem_bloco_e_anterior_ao_protocolo_nao_irregular(self):
        self.assertEqual([], validate_legal_research_trace({"entries": [{"claim": "x"}]}))

    def test_consulta_incompleta_bloqueia(self):
        for campo in ("database", "executedAt", "query"):
            payload = trilha_de_pesquisa()
            payload["searchRuns"][0][campo] = ""
            with self.subTest(campo=campo):
                self.assertTrue(any(f["code"] == "FAL-F5-QUERY-INCOMPLETE"
                                    for f in validate_legal_research_trace(payload)))

    def test_filtro_ausente_difere_de_filtro_vazio(self):
        payload = trilha_de_pesquisa()
        del payload["searchRuns"][0]["filters"]
        self.assertTrue(any(f["code"] == "FAL-F5-QUERY-INCOMPLETE"
                            for f in validate_legal_research_trace(payload)))
        payload["searchRuns"][0]["filters"] = {}
        self.assertEqual([], validate_legal_research_trace(payload))

    def test_id_de_consulta_repetido_bloqueia(self):
        payload = trilha_de_pesquisa()
        payload["searchRuns"].append(deepcopy(payload["searchRuns"][0]))
        self.assertTrue(any(f["code"] == "FAL-F5-QUERY-DUPLICATE"
                            for f in validate_legal_research_trace(payload)))

    def test_resultado_aproveitado_e_descartado_ao_mesmo_tempo_bloqueia(self):
        payload = trilha_de_pesquisa()
        payload["searchRuns"][0]["discarded"][0]["resultId"] = "RES-1"
        self.assertTrue(any(f["code"] == "FAL-F5-RESULT-DISCARD-OVERLAP"
                            for f in validate_legal_research_trace(payload)))

    def test_descarte_sem_motivo_bloqueia(self):
        payload = trilha_de_pesquisa()
        payload["searchRuns"][0]["discarded"][0]["reason"] = ""
        self.assertTrue(any(f["code"] == "FAL-F5-QUERY-INCOMPLETE"
                            for f in validate_legal_research_trace(payload)))

    def test_resultado_negativo_exige_consulta_executada(self):
        payload = trilha_de_pesquisa()
        run = payload["searchRuns"][0]
        run.update({"negativeResult": True, "resultIds": [], "query": ""})
        self.assertTrue(any(f["code"] == "FAL-F5-NEGATIVE-NO-QUERY"
                            for f in validate_legal_research_trace(payload)))

    def test_negativo_com_resultado_aproveitado_e_contradicao(self):
        payload = trilha_de_pesquisa()
        payload["searchRuns"][0]["negativeResult"] = True
        self.assertTrue(any(f["code"] == "FAL-F5-NEGATIVE-NO-QUERY"
                            for f in validate_legal_research_trace(payload)))

    def test_negativo_reproduzivel_passa(self):
        payload = trilha_de_pesquisa()
        payload["searchRuns"][0].update({"negativeResult": True, "resultIds": [], "discarded": []})
        self.assertEqual([], validate_legal_research_trace(payload))

    def test_replay_declarado_e_inexistente_bloqueia(self):
        payload = trilha_de_pesquisa()
        payload["searchRuns"][0]["replayRef"] = "replays/nao_existe.json"
        self.assertTrue(any(f["code"] == "FAL-F5-REPLAY-MISSING"
                            for f in validate_legal_research_trace(payload, case_dir=FORJA)))

    def test_acao_vedada_bloqueia_a_consulta(self):
        payload = trilha_de_pesquisa()
        payload["searchRuns"][0]["endpointOrTool"] = "research_mission"
        achados = validate_legal_research_trace(
            payload, denied_actions={"research_mission"})
        self.assertTrue(any(f["code"] == "FAL-F5-PAID-ACTION-DENIED" for f in achados))

    def test_acoes_vedadas_da_config_valem_na_trilha(self):
        config = json.loads((FORJA / "FORJA_SEARCH_CONFIG.json").read_text(encoding="utf-8"))
        self.assertIn("research_mission", config["policy"]["deniedActions"])


class FichaDeAncoraTests(unittest.TestCase):
    """Ementa localiza o acórdão; não diz o que ele decidiu."""

    def test_ficha_completa_passa(self):
        self.assertEqual([], validate_anchor_cards([ficha_de_ancora()], selected_route_id="R1"))

    def test_entrada_comum_de_ledger_nao_e_examinada(self):
        self.assertEqual([], validate_anchor_cards([{"claim": "fonte comum", "anchor": False}]))

    def test_ementa_isolada_nao_produz_holding(self):
        card = ficha_de_ancora(fullTextStatus="insufficient")
        self.assertTrue(any(f["code"] == "FAL-F7-ANCHOR-NO-FULL-TEXT"
                            for f in validate_anchor_cards([card])))

    def test_holding_sem_localizador_bloqueia(self):
        card = ficha_de_ancora()
        card["holding"]["locator"] = ""
        self.assertTrue(any(f["code"] == "FAL-F7-HOLDING-NO-LOCATOR"
                            for f in validate_anchor_cards([card])))

    def test_trecho_alterado_falha_por_hash(self):
        card = ficha_de_ancora()
        card["holding"]["text"] = card["holding"]["text"].replace("não se reabre", "pode ser revista")
        self.assertTrue(any(f["code"] == "FAL-F7-HOLDING-HASH-MISMATCH"
                            for f in validate_anchor_cards([card])))

    def test_fato_determinante_sem_confronto_bloqueia(self):
        card = ficha_de_ancora(elementComparison=[])
        self.assertTrue(any(f["code"] == "FAL-F7-FACT-FRAME-INCOMPLETE"
                            for f in validate_anchor_cards([card])))

    def test_confronto_sem_conclusao_bloqueia(self):
        card = ficha_de_ancora()
        card["elementComparison"][0]["verdict"] = ""
        self.assertTrue(any(f["code"] == "FAL-F7-FACT-FRAME-INCOMPLETE"
                            for f in validate_anchor_cards([card])))

    def test_rota_estranha_ao_brief_bloqueia(self):
        card = ficha_de_ancora(routeId="R9")
        achados = validate_anchor_cards([card], selected_route_id="R1", compared_route_ids={"R1", "R2"})
        self.assertTrue(any(f["code"] == "FAL-F7-ANCHOR-INVALIDATES-ROUTE" for f in achados))

    def test_rota_comparada_explicitamente_e_aceita(self):
        card = ficha_de_ancora(routeId="R2")
        self.assertEqual([], validate_anchor_cards(
            [card], selected_route_id="R1", compared_route_ids={"R1", "R2"}))


class VigenciaEContrarioTests(unittest.TestCase):
    """E7 e E8 — o precedente tem estado no tempo e tem adversário conhecido."""

    def test_quatro_estados_de_vigencia(self):
        self.assertEqual(
            {"vigente", "modulado", "superado", "afetado_por_tema_posterior"}, VIGENCIA_STATES)

    def test_vigencia_fora_do_contrato_bloqueia(self):
        card = ficha_de_ancora(vigencia="valido")
        self.assertTrue(any(f["code"] == "FAL-F7-VIGENCIA-INVALIDA"
                            for f in validate_anchor_cards([card])))

    def test_modulado_exige_marco_temporal(self):
        card = ficha_de_ancora(vigencia="modulado")
        self.assertTrue(any(f["code"] == "FAL-F7-MODULACAO-SEM-MARCO"
                            for f in validate_anchor_cards([card])))
        card["marcoTemporalModulacao"] = "efeitos a partir de 12/03/2024"
        self.assertEqual([], validate_anchor_cards([card]))

    def test_superado_nao_se_aplica_e_derruba_a_rota(self):
        card = ficha_de_ancora(vigencia="superado")
        achados = validate_anchor_cards([card])
        self.assertTrue(any(f["code"] == "FAL-F7-ANCHOR-INVALIDATES-ROUTE" for f in achados))

    def test_superado_pode_sustentar_pedido_de_superacao(self):
        card = ficha_de_ancora(vigencia="superado", operation="argue_overruling")
        self.assertEqual([], validate_anchor_cards([card]))

    def test_afetado_por_tema_posterior_aplicado_exige_razao(self):
        card = ficha_de_ancora(vigencia="afetado_por_tema_posterior")
        self.assertTrue(any(f["code"] == "FAL-F7-VIGENCIA-AFETADA-SEM-RAZAO"
                            for f in validate_anchor_cards([card])))

    def test_campo_de_contrario_ausente_difere_de_lista_vazia(self):
        card = ficha_de_ancora()
        del card["precedenteContrarioConhecido"]
        self.assertTrue(any(f["code"] == "FAL-F7-CONTRARY-NOT-EXAMINED"
                            for f in validate_anchor_cards([card])))

    def test_lista_vazia_sem_data_de_exame_nao_declara_nada(self):
        card = ficha_de_ancora(contraryCheckedAt="")
        self.assertTrue(any(f["code"] == "FAL-F7-CONTRARY-NOT-EXAMINED"
                            for f in validate_anchor_cards([card])))

    def test_contrario_citado_sem_operacao_bloqueia(self):
        card = ficha_de_ancora(precedenteContrarioConhecido=[
            {"identity": "STJ, REsp 2.222.222/SP"}])
        self.assertTrue(any(f["code"] == "FAL-F7-CONTRARY-NO-OPERATION"
                            for f in validate_anchor_cards([card])))

    def test_contrario_enfrentado_passa(self):
        card = ficha_de_ancora(precedenteContrarioConhecido=[
            {"identity": "STJ, REsp 2.222.222/SP", "operation": "distinguish",
             "response": "base fática diversa: lá não havia alíquota no dispositivo"}])
        self.assertEqual([], validate_anchor_cards([card]))


class RegimeComoConvencaoInternaTests(unittest.TestCase):
    """E13 — o efeito vem do dispositivo; o rótulo organiza o trabalho interno."""

    def test_regime_incompleto_bloqueia(self):
        for campo in ("legalBasis", "competentBody", "changePath", "checkedAt"):
            card = ficha_de_ancora()
            card["regime"][campo] = [] if campo == "legalBasis" else ""
            with self.subTest(campo=campo):
                self.assertTrue(any(f["code"] == "FAL-F7-REGIME-INCOMPLETE"
                                    for f in validate_anchor_cards([card])))

    def test_efeito_afirmado_sem_dispositivo_bloqueia(self):
        card = ficha_de_ancora()
        card["regime"]["legalBasis"] = []
        achados = validate_anchor_cards([card])
        self.assertTrue(any("sem dispositivo que o crie" in f["detail"] for f in achados))

    def test_score_universal_de_autoridade_bloqueia(self):
        card = ficha_de_ancora()
        card["regime"]["authorityScore"] = 0.92
        self.assertTrue(any(f["code"] == "FAL-F7-REGIME-UNIVERSAL-SCORE"
                            for f in validate_anchor_cards([card])))

    def test_sancao_administrativa_nao_e_precedente(self):
        for autoridade, orgao in (("acórdão sancionador", "CGU — Corregedoria-Geral"),
                                  ("acórdão", "Tribunal de Contas da União"),
                                  ("decisão", "CARF, 1ª Seção")):
            card = ficha_de_ancora()
            card["regime"].update({"authorityType": autoridade, "competentBody": orgao})
            with self.subTest(orgao=orgao):
                self.assertTrue(any(f["code"] == "FAL-F7-ADMIN-NOT-PRECEDENT"
                                    for f in validate_anchor_cards([card])))

    def test_orgao_judicial_nao_e_confundido_com_administrativo(self):
        for orgao in ("1ª Turma do STJ", "Corte Especial do STJ", "2ª Turma do TRF1"):
            card = ficha_de_ancora()
            card["regime"]["competentBody"] = orgao
            with self.subTest(orgao=orgao):
                self.assertEqual([], validate_anchor_cards([card]))

    def test_monocratica_antiga_nao_e_rebaixada_automaticamente(self):
        card = ficha_de_ancora()
        card["regime"].update({
            "authorityType": "decisão monocrática",
            "competentBody": "Relator, 2ª Turma do TRF1",
            "checkedAt": "2026-07-25T10:00:00-03:00",
        })
        card["holding"]["locator"] = "decisão de 03/1999, fl. 2"
        self.assertEqual([], validate_anchor_cards([card]))


class ReaberturaDeF4Tests(unittest.TestCase):
    """Âncora reprovada não é defeito de fonte: é a rota que deixou de existir."""

    def test_ancora_reprovada_nomeia_a_rota_atingida(self):
        card = ficha_de_ancora(fullTextStatus="insufficient")
        achados = validate_anchor_cards([card])
        self.assertEqual({"R1"}, failed_anchor_routes(achados, [card]))

    def test_ancora_integra_nao_reabre_nada(self):
        card = ficha_de_ancora()
        self.assertEqual(set(), failed_anchor_routes(validate_anchor_cards([card]), [card]))

    def test_gatilho_de_invalidacao_atinge_o_brief(self):
        self.assertIn("F4_SIGNATURE_BRIEF.json", DEPENDENCIES["precedent_anchor"])
        self.assertIn("F4_SIGNATURE_BRIEF.json", DEPENDENCIES["recipient_map"])


class CrossReferenceDoBriefTests(unittest.TestCase):
    """IDs que não existem em lugar nenhum são promessa, não lastro."""

    def _caso(self, brief: dict, **artefatos) -> Path:
        base = Path(self._dir.name)
        (base / "n4_artifacts").mkdir(parents=True, exist_ok=True)
        atomic_write_json(base / "n4_artifacts" / "F4_SIGNATURE_BRIEF.json", brief)
        for nome, payload in artefatos.items():
            atomic_write_json(base / "n4_artifacts" / nome, payload)
        return base

    def setUp(self):
        self._dir = tempfile.TemporaryDirectory()
        self.addCleanup(self._dir.cleanup)

    def test_sem_artefato_de_origem_nao_ha_como_acusar_pendurado(self):
        base = self._caso(brief_valido())
        self.assertEqual([], validate_brief_references(brief_valido(), base))

    def test_tese_inexistente_e_pendurada(self):
        base = self._caso(
            brief_valido(),
            **{"F4_THESIS_MATURITY.json": {"theses": [{"thesisId": "T1"}]}})
        achados = validate_brief_references(brief_valido(), base)
        self.assertTrue(any(f["code"] == "FAL-F4-REFERENCE-DANGLING" and "T2" in f["detail"]
                            for f in achados))

    def test_tese_existente_passa(self):
        base = self._caso(
            brief_valido(),
            **{"F4_THESIS_MATURITY.json": {"theses": [{"thesisId": "T1"}, {"thesisId": "T2"}]}})
        self.assertEqual([], validate_brief_references(brief_valido(), base))

    def test_fato_decisivo_vale_por_pergunta_ou_por_no_do_grafo(self):
        base = self._caso(
            brief_valido(),
            **{"F3_REASONING_GRAPH.json": {"nodes": [{"id": "F1"}]}})
        self.assertEqual([], validate_brief_references(brief_valido(), base))

    def test_ancora_candidata_nao_declarada_bloqueia(self):
        brief = brief_valido()
        brief["anchorCandidates"] = brief["anchorCandidates"][:1]
        base = self._caso(brief)
        self.assertTrue(any(f["code"] == "FAL-F4-ANCHOR-DANGLING" and "ANC-2" in f["detail"]
                            for f in validate_brief_references(brief, base)))

    def test_candidata_sem_identidade_do_julgado_bloqueia(self):
        brief = brief_valido()
        brief["anchorCandidates"][0]["identity"] = "  "
        base = self._caso(brief)
        self.assertTrue(any(f["code"] == "FAL-F4-ANCHOR-DANGLING"
                            for f in validate_brief_references(brief, base)))

    def test_ancora_final_em_f4_e_proibida(self):
        brief = brief_valido()
        brief["routes"][0]["finalAnchorIds"] = ["ANC-1"]
        base = self._caso(brief)
        achados = validate_brief_references(brief, base)
        self.assertTrue(any("verificação de íntegra é trabalho de F7" in f["detail"]
                            for f in achados))


if __name__ == "__main__":
    unittest.main(verbosity=2)
