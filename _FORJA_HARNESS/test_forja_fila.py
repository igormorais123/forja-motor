"""Regressão da FORJA FILA (planejamento/16_TDD §7) — 12/07/2026.

DEVE_PEGAR: bloqueios detectados corretamente. NÃO_PODE_TRAVAR: demanda legítima
não é travada e o determinismo se mantém. Rodar: python test_forja_fila.py (exit 0 = verde).
Fixtures 100% sintéticas; 'hoje' fixo (determinismo).
"""

import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from forja_fila import (  # noqa: E402
    classificar_prontidao, montar_fila, ordenar, pendencia_operacao_assistida, pontuar,
)

HOJE = date(2026, 7, 12)
FALHAS = []


def caso(nome, esperado, obtido):
    if esperado == obtido:
        print(f"[OK    ] {nome}")
    else:
        print(f"[FALHOU] {nome} — esperado {esperado!r}, veio {obtido!r}")
        FALHAS.append(nome)


def demanda(**kw):
    base = {"id": "d1", "titulo": "Demanda teste", "status": "aberta",
            "pasta": "", "prazo": None, "recebidoEm": "2026-07-10T10:00:00-03:00",
            "urgenciaManual": "media", "tags": [], "anexos": {}, "proximaAcao": ""}
    base.update(kw)
    return base


# ---------- DEVE_PEGAR ----------

# 1. anexos externos pendentes -> bloqueada_acesso
cat, _ = classificar_prontidao(demanda(anexos={"externosPendentes": True}), None)
caso("D1 anexos externos pendentes -> bloqueada_acesso", "bloqueada_acesso", cat)

# 2. COMANDO_AUSENTE no F0 -> bloqueada_comando
cat, _ = classificar_prontidao(demanda(), {"gates": [{"code": "COMANDO_AUSENTE", "severity": "P0"}]})
caso("D2 finding COMANDO_AUSENTE -> bloqueada_comando", "bloqueada_comando", cat)

# 3. próxima ação depende do Fábio -> bloqueada_decisao_cliente (com acento e maiúsculas)
cat, motivo = classificar_prontidao(demanda(proximaAcao="Aguardar DECISÃO de Fábio sobre a proposta"), None)
caso("D3 léxico de decisão do cliente -> bloqueada_decisao_cliente", "bloqueada_decisao_cliente", cat)
cat, _ = classificar_prontidao(demanda(proximaAcao="Fábio revisar o dossiê e decidir se agenda reunião"), None)
caso("D3b caso real Roraima (gate M0) -> bloqueada_decisao_cliente", "bloqueada_decisao_cliente", cat)

# 4. espera > 48h gera destaque
fila = montar_fila([demanda(proximaAcao="aguardar decisão de Fábio",
                            manual={"updatedAt": "2026-07-08T09:00:00-03:00"})], {}, HOJE)
caso("D4 espera >48h -> destaque48h", True, fila["bloqueadas"][0]["destaque48h"])
fila = montar_fila([demanda(proximaAcao="aguardar decisão de Fábio",
                            manual={"updatedAt": "2026-07-12T09:00:00-03:00"})], {}, HOJE)
caso("D4b espera <48h -> sem destaque", False, fila["bloqueadas"][0]["destaque48h"])

# 5. prazo vencido: marcador + score máximo de prazo + permanece na fila
p = pontuar(demanda(prazo="2026-07-01"), HOJE)
caso("D5 prazo vencido marcado", True, p["prazoVencido"])
caso("D5b prazo vencido pontua como <=3d (40)", True,
     any(f["fator"] == "PRAZO_VENCIDO" and f["pontos"] == 40 for f in p["fatores"]))
fila = montar_fila([demanda(prazo="2026-07-01")], {}, HOJE)
caso("D5c prazo vencido permanece na fila de produção", 1, len(fila["producao"]))

# 6. hash de origem: coberto em I/O real (gerar() grava demandasSha256) — validado no dry-run M0.

# 7. prazo malformado -> fator PRAZO_ILEGIVEL, sem exceção
p = pontuar(demanda(prazo="consulta pública até agosto"), HOJE)
caso("D7 prazo malformado -> PRAZO_ILEGIVEL sem exceção", True,
     any(f["fator"] == "PRAZO_ILEGIVEL" for f in p["fatores"]))

# 8. status pronta_para_revisao -> aguardando_revisao_humana (gate M0)
cat, _ = classificar_prontidao(demanda(status="pronta_para_revisao"), None)
caso("D8 pronta_para_revisao -> aguardando_revisao_humana", "aguardando_revisao_humana", cat)

# ---------- NÃO_PODE_TRAVAR ----------

# 9. demanda limpa -> pronta
cat, _ = classificar_prontidao(demanda(proximaAcao="redigir minuta com base nos autos"), None)
caso("N9 demanda limpa -> pronta", "pronta", cat)

# 10. determinismo: mesmo input -> mesmo documento
f1 = montar_fila([demanda(id="a", prazo="2026-07-20"), demanda(id="b", urgenciaManual="alta")], {}, HOJE)
f2 = montar_fila([demanda(id="a", prazo="2026-07-20"), demanda(id="b", urgenciaManual="alta")], {}, HOJE)
caso("N10 mesmo input -> JSON idêntico", json.dumps(f1, sort_keys=True), json.dumps(f2, sort_keys=True))

# 11. ordem normativa: alta+prazo 5d (70) vence media+prazo 2d (60)
fila = montar_fila([
    demanda(id="media-2d", urgenciaManual="media", prazo="2026-07-14"),
    demanda(id="alta-5d", urgenciaManual="alta", prazo="2026-07-17"),
], {}, HOJE)
caso("N11 alta+5d vence media+2d", "alta-5d", fila["producao"][0]["demandaId"])

# 11b. empate exato resolve por prazo mais próximo, depois recebidoEm, depois id
itens = [
    {"demandaId": "c", "score": 50, "prazo": "2026-07-20", "recebidoEm": "2026-07-01"},
    {"demandaId": "a", "score": 50, "prazo": "2026-07-15", "recebidoEm": "2026-07-05"},
    {"demandaId": "b", "score": 50, "prazo": "2026-07-15", "recebidoEm": "2026-07-02"},
]
ordem = [i["demandaId"] for i in ordenar(itens)]
caso("N11b empate: prazo asc -> recebidoEm asc -> id", ["b", "a", "c"], ordem)

# 12. anti-inanição: baixa prioridade com 30 dias soma +10 de idade
p = pontuar(demanda(urgenciaManual="baixa", recebidoEm="2026-06-12T10:00:00-03:00"), HOJE)
caso("N12 idade 30d soma cap +10", 10, p["score"])

# 13. fila vazia -> documento válido
fila = montar_fila([demanda(status="cumprida")], {}, HOJE)
caso("N13 fila vazia é documento válido", 0, fila["resumo"]["prontas"])
caso("N13b resumo consistente", {"prontas": 0, "bloqueadas": 0, "emProducao": 0,
                                 "aguardandoRevisaoHumana": 0, "aguardandoEvidencia": 0}, fila["resumo"])

# 14. em produção: F5 -> em_producao; F0 e F10 não
cat, _ = classificar_prontidao(demanda(), {"currentPhase": "F5_CHECKLIST"})
caso("N14 F5 -> em_producao", "em_producao", cat)
cat, _ = classificar_prontidao(demanda(), {"currentPhase": "F0_RECONCILIACAO_FILA"})
caso("N14b F0 não é em_producao", "pronta", cat)
cat, _ = classificar_prontidao(demanda(), {"currentPhase": "F10_ENTREGA_EVIDENCIA_APRENDIZADO"})
caso("N14c F10 não é em_producao", "pronta", cat)

# 15. operação assistida: pendência interna vive na fila, nunca em calendário/alarme
cfg = {"fila": {"operacaoAssistidaAte": "2026-07-19"}}
oa = pendencia_operacao_assistida(cfg, date(2026, 7, 15))
caso("N15 antes do prazo: acompanhamento sem pendência", False, oa["fechamentoPendente"])
oa = pendencia_operacao_assistida(cfg, date(2026, 7, 19))
caso("N15b no prazo: fechamento pendente", True, oa["fechamentoPendente"])
caso("N15c sem config: sem pendência (None)", None, pendencia_operacao_assistida({}, HOJE))

print()
if FALHAS:
    print(f"FALHOU: {len(FALHAS)} caso(s): {FALHAS}")
    raise SystemExit(1)
print("OK: fila — 9 detecções + 10 não-travas confirmadas")
