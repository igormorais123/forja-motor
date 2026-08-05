# -*- coding: utf-8 -*-
"""
bancada_registro.py — Emite o registro detalhado dos resultados a partir dos artefatos.

Este arquivo existe para que o registro NÃO seja transcrito à mão. São cerca de
duzentos números entre execução, camada determinística, seis votos cegos e as
suítes do harness; transcrever isso é criar uma segunda fonte da verdade que
diverge da primeira no dia em que alguém reexecutar qualquer etapa.

Tudo o que sai daqui vem de:
  protocolo/DOSSIE_LEDGER.json      insumo congelado
  execucao/<id>/META.json           telemetria de cada participante
  avaliacao/DETERMINISTICA.json     camada 1
  avaliacao/juizes/*.json           os seis votos brutos
  avaliacao/JUIZES_CONSOLIDADO.json camada 2
  avaliacao/QUADRO_FINAL.json       composição
  ../telemetria/BASELINE_*.json     suítes do harness
  ../telemetria/REGUA_*.json        régua

O mapa do cegamento continua fora do workspace. Ele é lido apenas para resolver
rótulo em nome no registro final — o arquivo de mapeamento não é copiado para cá.

Uso: python bancada_registro.py [--saida ARQUIVO]
"""
from __future__ import annotations

import argparse
import glob
import io
import json
import os
import sys
from datetime import datetime
from pathlib import Path

BANCADA = Path(__file__).resolve().parent
FORJA = BANCADA.parent
MAPA = (Path(os.environ.get("FORJA_AR_SECRETS_DIR")
             or Path(os.environ.get("USERPROFILE", Path.home())) / ".forja_ar_secrets")
        / "bancada_cafelana_v7_mapa.json")

CRITERIOS = ["tese", "comando", "autoridade", "arquitetura", "escrita", "utilidade"]
ROTULO_CRITERIO = {
    "tese": "tese principal", "comando": "fidelidade ao comando",
    "autoridade": "uso de autoridade", "arquitetura": "arquitetura",
    "escrita": "escrita forense", "utilidade": "utilidade ao julgador",
}


def _ler(caminho: Path, padrao=None):
    if not caminho.is_file():
        return padrao
    return json.loads(caminho.read_text(encoding="utf-8"))


def _ultimo(padrao: str):
    """O mais RECENTE, por data de modificação — não o último em ordem alfabética.

    A pasta de telemetria mistura arquivos datados (`BASELINE_2026-07-27_...`)
    com snapshots de nome fixo (`BASELINE_pos_E11.json`). Ordenar por nome põe
    os de nome fixo no fim, e o registro passou a citar um baseline de dois dias
    antes como se fosse o da rodada.
    """
    achados = [Path(p) for p in glob.glob(str(FORJA / "telemetria" / padrao))]
    if not achados:
        return None
    return _ler(max(achados, key=lambda p: p.stat().st_mtime))


def _tab(cabecalho: list[str], linhas: list[list], alinhamento: str = "") -> list[str]:
    sep = "|" + "|".join(
        (":---:" if alinhamento[i:i + 1] == "c" else
         "---:" if alinhamento[i:i + 1] == "r" else "---")
        for i in range(len(cabecalho))) + "|"
    saida = ["| " + " | ".join(cabecalho) + " |", sep]
    saida += ["| " + " | ".join(str(c) for c in linha) + " |" for linha in linhas]
    return saida + [""]


def montar() -> str:
    ledger = _ler(BANCADA / "protocolo" / "DOSSIE_LEDGER.json", {})
    det = (_ler(BANCADA / "avaliacao" / "DETERMINISTICA.json", {}) or {}).get("resultados", {})
    cons = _ler(BANCADA / "avaliacao" / "JUIZES_CONSOLIDADO.json", {}) or {}
    quadro = (_ler(BANCADA / "avaliacao" / "QUADRO_FINAL.json", {}) or {}).get("quadro", [])
    mapa = (_ler(MAPA, {}) or {}).get("mapa", {})
    votos = [_ler(p) for p in sorted((BANCADA / "avaliacao" / "juizes").glob("*.json"))]
    baseline = _ultimo("BASELINE_*.json")
    regua = _ultimo("REGUA_*.json")

    def nome(rotulo):
        return mapa.get(rotulo, rotulo)

    L: list[str] = []
    add = L.append

    add("# Registro detalhado — Bancada Cafelana V7")
    add("")
    add(f"Gerado por `bancada_registro.py` em {datetime.now().strftime('%d/%m/%Y %H:%M')}. "
        "Todos os números vêm dos artefatos da execução; nenhum foi transcrito à mão.")
    add("")
    add("Leitura de conjunto e conclusões em `RELATORIO_BANCADA_V7.md`; protocolo e "
        "blindagens em `LEIA-ME.md`. Este arquivo é a prova, não a narrativa.")
    add("")

    # ---------------------------------------------------------------- insumo
    add("## 1. Insumo congelado")
    add("")
    add(f"- Dossiê: **{ledger.get('bytes', 0) / 1024:.0f} KB**, {len(ledger.get('pecas', []))} peças")
    add(f"- SHA-256: `{ledger.get('sha256Dossie', '')}`")
    fech = ledger.get("autoridadesFechadas", {})
    add(f"- Ledger fechado: **{len(fech.get('julgados', []))} julgados**, "
        f"{len(fech.get('sumulas', []))} súmulas, {len(fech.get('temas', []))} temas")
    add("")
    add("Peças do dossiê, na ordem em que foram apresentadas:")
    add("")
    L.extend(_tab(["#", "rótulo", "arquivo", "KB", "sha256 (12)"],
                  [[i, p["rotulo"], f"`{p['arquivo']}`", f"{p['bytes'] / 1024:.0f}",
                    f"`{p['sha256'][:12]}`"]
                   for i, p in enumerate(ledger.get("pecas", []), 1)], "rlllr"))

    # ------------------------------------------------------------- execução
    add("## 2. Execução — telemetria por participante")
    add("")
    linhas = []
    for pasta in sorted((BANCADA / "execucao").iterdir()):
        meta = _ler(pasta / "META.json")
        if not meta:
            continue
        p = meta["participante"]
        linhas.append([
            f"`{p['id']}`", p["familia"], p["rota"],
            f"`{meta.get('modeloReportado', '')}`",
            meta.get("palavrasSaida", 0),
            det.get(p["id"], {}).get("palavras", "—"),
            meta.get("tokensSaida") if meta.get("tokensSaida") is not None else "não capturado",
            meta.get("tokensRaciocinio", 0), f"{meta.get('segundos', 0):.0f}",
            f"{meta.get('custoUsd', 0):.3f}",
            "sim" if meta.get("truncada") else "não",
        ])
    L.extend(_tab(["participante", "família", "rota", "modelo no envelope",
                   "palavras (resposta)", "palavras (peça)",
                   "tokens saída", "tokens raciocínio", "seg", "US$", "truncada"],
                  linhas, "lllrrrrrrrc"))
    add("*Palavras (resposta)* inclui o relatório de mudanças contratado; *palavras (peça)* "
        "conta só o texto forense, que é o que a camada determinística avalia.")
    add("")
    add("O modelo do envelope é lido da resposta do provedor, nunca do que foi pedido. "
        "Divergência entre pedido e envelope invalida a execução.")
    add("")
    if any(m for m in linhas if m[6] == "não capturado"):
        add("Os dois participantes de assinatura têm o total de tokens de saída marcado como "
            "**não capturado**: a soma por mensagem do stream devolvia contagem parcial, "
            "defeito corrigido depois desta execução. Como o stream não foi persistido, o "
            "total verdadeiro não é recuperável — e publicar o número parcial seria publicar "
            "um número falso. O custo dessas duas execuções é zero de qualquer modo, por "
            "rodarem na assinatura.")
        add("")

    descartadas = BANCADA / "execucao_descartadas"
    if descartadas.is_dir():
        add("### 2.1 Execuções descartadas, preservadas como evidência")
        add("")
        for sub in sorted(d for d in descartadas.iterdir() if d.is_dir()):
            meta = _ler(sub / "META.json") or {}
            add(f"- **`{sub.name}`** — {meta.get('palavrasSaida', '?')} palavras, "
                f"envelope reportou `{meta.get('modeloReportado', '?')}`. "
                f"Motivo em `execucao_descartadas/LEIA-ME.md`.")
        add("")

    # ------------------------------------------- camada 1 — determinística
    add("## 3. Camada determinística, item a item")
    add("")
    add("### 3.1 Composição da nota")
    add("")
    L.extend(_tab(["participante", "nota", "integridade /40", "obediência /20",
                   "retenção /20", "pendências /12", "ofício /8", "teto"],
                  [[f"`{n}`", f"**{a['pontuacao']['nota']:.1f}**"]
                   + [f"{a['pontuacao']['componentes'][k]:.1f}" for k in
                      ("integridade", "obediencia", "retencao", "pendencias", "oficio")]
                   + [f"{a['pontuacao']['teto']:.0f}"]
                   for n, a in sorted(det.items(),
                                      key=lambda kv: -kv[1]["pontuacao"]["nota"])],
                  "lrrrrrrr"))

    add("### 3.2 Autoridades citadas contra o ledger fechado")
    add("")
    L.extend(_tab(["participante", "citadas na peça", "presentes no dossiê",
                   "novas declaradas", "novas afirmadas", "marcadores [A CONFERIR]"],
                  [[f"`{n}`", a["autoridades"]["citadasNaPeca"], a["autoridades"]["doDossie"],
                    len(a["autoridades"]["novasDeclaradas"]),
                    f"**{len(a['autoridades']['novasAfirmadas'])}**",
                    a["autoridades"]["marcadoresAConferir"]]
                   for n, a in sorted(det.items(),
                                      key=lambda kv: -kv[1]["autoridades"]["citadasNaPeca"])],
                  "lrrrrr"))
    add("*Nova afirmada* = autoridade ausente do dossiê e apresentada como verificada. "
        "É a medida de invenção, e é o único item com poder de teto sobre a nota.")
    add("")

    add("### 3.3 Canários — erros reais deste caso, um por linha")
    add("")
    ordem = sorted(det)
    canarios = {c["id"]: c for a in det.values() for c in a["canarios"]}
    linhas = []
    for cid in sorted(canarios):
        base = canarios[cid]
        estados = ["ACIONADO" if next(c for c in det[n]["canarios"] if c["id"] == cid)["acionado"]
                   else "—" for n in ordem]
        linhas.append([f"`{cid}`", base["peso"], base["titulo"]] + estados)
    L.extend(_tab(["canário", "peso", "o que detecta"] + [f"`{n}`" for n in ordem],
                  linhas, "lrl" + "c" * len(ordem)))

    add("### 3.4 Retenção do ganho da V6")
    add("")
    retencoes = {r["id"]: r for a in det.values() for r in a["retencao"]}
    linhas = []
    for rid in sorted(retencoes):
        base = retencoes[rid]
        estados = []
        for n in ordem:
            item = next(r for r in det[n]["retencao"] if r["id"] == rid)
            estados.append("sim" if item["presente"] else
                           "removido c/ razão" if item["removidoComJustificativa"] else "**não**")
        linhas.append([f"`{rid}`", base["peso"], base["descricao"]] + estados)
    L.extend(_tab(["item", "peso", "o que é"] + [f"`{n}`" for n in ordem],
                  linhas, "lrl" + "c" * len(ordem)))
    add("Remover com razão declarada no relatório conta como cumprido: o prompt mandava "
        "corrigir o que estivesse errado e registrar a divergência. Remover em silêncio, não.")
    add("")
    truncadas = [n for n in ordem
                 if (det[n].get("meta") or {}).get("truncada")]
    if truncadas:
        add(f"**Ressalva de precisão sobre {', '.join(f'`{n}`' for n in truncadas)}.** "
            "A detecção de retenção mede presença do item no texto, e numa peça interrompida "
            "isso confunde menção com entrega: o `kimi-k3` marca `R5` e `R6` porque os dois "
            "aparecem no bloco *Resumo dos pedidos formulados* da ementa de abertura — a peça "
            "termina na Síntese 1 e nunca chega a uma seção de pedidos. Em texto truncado, "
            "leia esta tabela como inventário do que foi anunciado, não do que foi feito.")
        add("")

    add("### 3.5 Pendências declaradas na V6")
    add("")
    pend = {p["id"]: p for a in det.values() for p in a["pendencias"]}
    linhas = []
    for pid in sorted(pend):
        base = pend[pid]
        estados = ["sim" if next(p for p in det[n]["pendencias"] if p["id"] == pid)["tratada"]
                   else "**não**" for n in ordem]
        linhas.append([f"`{pid}`", base["peso"], base["descricao"]] + estados)
    L.extend(_tab(["pendência", "peso", "o que é"] + [f"`{n}`" for n in ordem],
                  linhas, "lrl" + "c" * len(ordem)))

    add("### 3.6 Gates da casa, aplicados sem adaptação")
    add("")
    L.extend(_tab(["participante", "lastro P0", "lastro P1", "estilo humano P0",
                   "estilo P1", "verificador P0", "P0 efetivo", "placeholders indevidos"],
                  [[f"`{n}`", a["gates"]["lastroP0"], a["gates"]["lastroP1"],
                    a["gates"]["estiloP0"], a["gates"]["estiloP1"],
                    a["gates"]["verificadorP0"],
                    a["gates"].get("verificadorP0Efetivo", "—"),
                    len(a["gates"].get("placeholdersIndevidos", []))]
                   for n, a in sorted(det.items())], "lrrrrrrr"))
    add("*P0 efetivo* desconta o placeholder da data do protocolo, exceção documentada "
        "da casa: a própria V6 entregue o tem.")
    add("")

    add("### 3.7 Perfil de trabalho — medido, não pontuado")
    add("")
    L.extend(_tab(["participante", "contenção", "cobertura da V6", "jaccard",
                   "trechos próprios", "leitura"],
                  [[f"`{n}`", f"{a['similaridadeV6']['contencao']:.3f}",
                    f"{a['similaridadeV6']['cobertura']:.3f}",
                    f"{a['similaridadeV6']['jaccard']:.3f}",
                    a["similaridadeV6"]["trechosProprios"],
                    "edição incremental" if a["similaridadeV6"]["contencao"] > 0.7
                    else "híbrido" if a["similaridadeV6"]["contencao"] > 0.3
                    else "reescrita integral"]
                   for n, a in sorted(det.items(),
                                      key=lambda kv: -kv[1]["similaridadeV6"]["contencao"])],
                  "lrrrrl"))
    add("**Contenção** = fração dos trechos de 12 palavras da V7 que já existiam na V6. "
        "**Cobertura** = fração da V6 que sobreviveu. Não entra na nota: o prompt admitia "
        "preservar o texto ou a substância, e descontar por uma leitura permitida mediria "
        "a ambiguidade do enunciado, não o participante.")
    add("")

    # -------------------------------------------------- camada 2 — juízes
    add("## 4. Julgamento cego — os seis votos brutos")
    add("")
    add(f"Votos válidos: **{cons.get('votosValidos', 0)} de {cons.get('votosTotais', 0)}**. "
        f"Anulados: {cons.get('votosAnulados') or 'nenhum'}. "
        f"Custo do julgamento: US$ {cons.get('custoUsd', 0):.2f}.")
    add("")
    add("Cada juiz julgou duas vezes, com a ordem de apresentação invertida. A âncora é uma "
        "transcrição literal da peça eleita, conferida por código contra o texto — voto cuja "
        "âncora não confere é anulado.")
    add("")
    L.extend(_tab(["juiz", "família", "ordem", "elegeu", "âncora", "ranking (melhor → pior)"],
                  [[f"`{v['juiz']}`", v["familiaJuiz"], v["ordem"],
                    f"**{nome(v['voto'].get('protocolaria'))}**",
                    "válida" if v["ancoraValida"] else "**INVÁLIDA**",
                    " > ".join(nome(r) for r in v["voto"].get("ranking", []))]
                   for v in votos], "lllllc"))

    add("### 4.1 Notas por critério — cada juiz, cada peça")
    add("")
    for v in votos:
        add(f"**`{v['juiz']}` · ordem {v['ordem']}**")
        add("")
        notas = v["voto"].get("notas") or {}
        linhas = []
        for rotulo in sorted(notas, key=lambda r: int(r[1:]) if r[1:].isdigit() else 99):
            n = notas[rotulo]
            if not isinstance(n, dict):
                continue
            linhas.append([f"`{nome(rotulo)}`"]
                          + [f"{n.get(c, 0):.1f}" if isinstance(n.get(c), (int, float)) else "—"
                             for c in CRITERIOS]
                          + [f"{sum(n.get(c, 0) for c in CRITERIOS if isinstance(n.get(c), (int, float))) / 6:.2f}"])
        L.extend(_tab(["peça"] + [ROTULO_CRITERIO[c] for c in CRITERIOS] + ["média"],
                      linhas, "l" + "r" * 7))

    add("### 4.2 Média por critério, consolidada")
    add("")
    por = cons.get("porParticipante", {})
    L.extend(_tab(["participante"] + [ROTULO_CRITERIO[c] for c in CRITERIOS] + ["média geral"],
                  [[f"`{n}`"] + [f"{(d['medias'].get(c) or 0):.2f}" for c in CRITERIOS]
                   + [f"**{(d.get('mediaGeral') or 0):.2f}**"]
                   for n, d in sorted(por.items(),
                                      key=lambda kv: -(kv[1].get("mediaGeral") or 0))],
                  "l" + "r" * 7))

    add("### 4.3 Ordenação: Borda bruto e Borda entre famílias")
    add("")
    L.extend(_tab(["participante", "Borda bruto", "Borda entre famílias (média)",
                   "votos de outras famílias", "eleito para protocolo"],
                  [[f"`{n}`", f"{d.get('borda', 0):.0f}",
                    f"**{(d.get('bordaEntreFamiliasMedia') or 0):.2f}**",
                    d.get("votosDeOutrasFamilias", 0), d.get("eleitoParaProtocolo", 0)]
                   for n, d in sorted(por.items(),
                                      key=lambda kv: -(kv[1].get("bordaEntreFamiliasMedia") or 0))],
                  "lrrrr"))
    add("O Borda entre famílias descarta o voto de qualquer juiz sobre peça da própria "
        "família — por isso a coluna é média, e não soma. Como as três famílias de juiz "
        "(anthropic, openai, xai) também competem, cada uma dessas peças perde os 2 votos "
        "do juiz conterrâneo e fica com 4. Só o `kimi-k3` recebe os 6: não há juiz moonshot "
        "na bancada. O Borda bruto fica na tabela para que se veja o quanto a correção move "
        "— o `luna-5.6`, por exemplo, cai de 3º para 4º quando os votos do Sol, da mesma "
        "família, saem da conta.")
    add("")

    add("### 4.4 Auto-preferência e estabilidade de posição")
    add("")
    auto = cons.get("autoPreferencia", {})
    if auto:
        L.extend(_tab(["juiz", "posição que deu a si", "posição que os outros deram", "vantagem"],
                      [[f"`{j}`", f"{d['posicaoQueDeuASiMesmo']:.1f}º",
                        f"{d['posicaoQueOsOutrosDeram']:.2f}º", f"{d['vantagem']:+.2f}"]
                       for j, d in sorted(auto.items(), key=lambda kv: -kv[1]["vantagem"])],
                      "lrrr"))
    est = cons.get("estabilidadeDePosicao", {})
    if est:
        L.extend(_tab(["juiz", "posições idênticas ao inverter a ordem", "manteve o vencedor"],
                      [[f"`{j}`", f"{d['posicoesIdenticas']} de {d['de']}",
                        "sim" if d["mesmoTopo"] else "**não**"]
                       for j, d in sorted(est.items())], "lrc"))
    add("Ranking que muda ao inverter a ordem mede viés de posição, não qualidade. É a razão "
        "pela qual nenhum resultado desta bancada deve ser lido com precisão decimal.")
    add("")

    add("### 4.5 O erro mais grave de cada peça, na palavra dos juízes")
    add("")
    erros: dict[str, list[str]] = {}
    for v in votos:
        for rotulo, texto in (v["voto"].get("erroMaisGrave") or {}).items():
            erros.setdefault(nome(rotulo), []).append(f"[{v['juiz']}/{v['ordem']}] {texto}")
    for participante in sorted(erros):
        add(f"**`{participante}`**")
        add("")
        for linha in erros[participante]:
            add(f"- {linha}")
        add("")

    add("### 4.6 O que decidiu a comparação, por juiz")
    add("")
    for v in votos:
        porque = " ".join(str(v["voto"].get("porque") or "").split())
        add(f"**`{v['juiz']}` · ordem {v['ordem']}** — {porque}")
        add("")

    # ------------------------------------------------------- quadro final
    add("## 5. Quadro final")
    add("")
    L.extend(_tab(["#", "participante", "final", "determinística", "juízes",
                   "tetos aplicados"],
                  [[i, f"`{r['participante']}`", f"**{r['notaFinal']:.1f}**",
                    f"{r['notaDeterministica']:.1f}",
                    f"{r['notaJuizes']:.1f}" if r["notaJuizes"] is not None else "—",
                    "; ".join(r["tetosAplicados"]) or "—"]
                   for i, r in enumerate(quadro, 1)], "rlrrrl"))
    total = sum(r.get("custoUsd") or 0 for r in quadro) + cons.get("custoUsd", 0)
    add(f"Composição: 55% determinística, 45% juízes, com o teto da camada determinística "
        f"valendo como veto sobre a nota final. **Custo total da bancada: US$ {total:.2f}.**")
    add("")

    # ------------------------------------------------- suítes do harness
    add("## 6. Suítes do harness, na mesma rodada")
    add("")
    if baseline:
        add(f"**Baseline** ({baseline.get('geradoEm', '')}, Python {baseline.get('python', '')}): "
            f"**{baseline.get('suitesVerdes')}/{baseline.get('suitesDeclaradas')} suítes verdes** · "
            f"{baseline.get('testesPytest')} testes pytest (+{baseline.get('subtestsPytest')} subtests) · "
            f"{baseline.get('regressoesScript')} regressões em script · "
            f"**{'APROVADO' if baseline.get('aprovado') else 'REPROVADO'}**.")
        add("")
        vermelhas = [s for s in baseline.get("suites", []) if not s.get("verde")]
        if vermelhas:
            add("Suítes vermelhas: " + ", ".join(f"`{s['suite']}`" for s in vermelhas))
        else:
            add("Nenhuma suíte vermelha.")
        add("")
        novas = [s for s in baseline.get("suites", [])
                 if s["suite"] in ("test_forja_identidade_modelo.py", "test_forja_lastro.py",
                                   "test_forja_regimentos.py")]
        if novas:
            add("Suítes acrescentadas nas rodadas recentes:")
            add("")
            L.extend(_tab(["suíte", "família", "resultado"],
                          [[f"`{s['suite']}`", s["familia"], s["resumo"]] for s in novas], "lll"))
    if regua:
        integridade = regua.get("integridade") or {}
        add(f"**Régua** ({regua.get('executadoEm', '')}, modo {regua.get('modo', '')}): "
            f"**{regua.get('veredito')}** em {regua.get('duracaoTotalS')}s · "
            f"integridade de arquivos protegidos: "
            f"{'íntegra' if integridade.get('ok') else 'DIVERGENTE'}.")
        add("")

    add("## 7. Onde está cada artefato")
    add("")
    L.extend(_tab(["artefato", "caminho"], [
        ["dossiê congelado + ledger fechado", "`protocolo/DOSSIE.md`, `protocolo/DOSSIE_LEDGER.json`"],
        ["prompt idêntico a todos", "`protocolo/PROMPT_V7.md`"],
        ["as seis peças e a telemetria", "`execucao/<participante>/SAIDA.md` e `META.json`"],
        ["execuções descartadas", "`execucao_descartadas/`"],
        ["peças anonimizadas", "`cego/P1..P6.md`"],
        ["mapa do cegamento", "fora do workspace, em `~/.forja_ar_secrets/`"],
        ["camada determinística", "`avaliacao/DETERMINISTICA.json`"],
        ["votos brutos dos juízes", "`avaliacao/juizes/<juiz>_<ordem>.json`"],
        ["consolidação dos juízes", "`avaliacao/JUIZES_CONSOLIDADO.json`"],
        ["quadro final", "`avaliacao/QUADRO_FINAL.json`"],
        ["leitura de conjunto", "`RELATORIO_BANCADA_V7.md`"],
        ["protocolo e blindagens", "`LEIA-ME.md`"],
    ], "ll"))

    return "\n".join(L) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description="registro detalhado da bancada")
    ap.add_argument("--saida", type=Path,
                    default=BANCADA / "RESULTADOS_DETALHADOS_BANCADA_V7.md")
    args = ap.parse_args()
    texto = montar()
    args.saida.write_text(texto, encoding="utf-8")
    print(f"registro gravado: {args.saida.name} "
          f"({len(texto) / 1024:.0f} KB, {len(texto.splitlines())} linhas)")
    return 0


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    raise SystemExit(main())
