# -*- coding: utf-8 -*-
"""
forja_regimentos.py — Auditoria de atualidade dos regimentos internos arquivados.

Por que existe. O protocolo da fábrica manda, para toda peça, ler o regimento do
tribunal e conferir emendas posteriores à consolidação, porque a peça tem de
refletir o regimento vigente NA DATA DO PROTOCOLO. Na prática isso vinha sendo
uma varredura manual por tribunal — item E11 do plano — e varredura manual não
sobrevive ao tempo: dez pastas depois ninguém sabe qual arquivo está velho.

O obstáculo real não era falta de disciplina, e sim falta de forma. Cada
regimento arquivado usa um cabeçalho diferente: um diz "Versão:", outro
"Consolidação oficial vigente:", outro "Consolidado até", com ou sem data de
download. Sem cabeçalho previsível não há auditoria possível — e uma auditoria
que erra o parsing produz o pior resultado de todos, que é declarar desatualizado
um arquivo correto e mandar o operador refazer trabalho pronto.

Este módulo tolera as variações que já existem no acervo em vez de exigir
retrofit, e sinaliza o que falta para que o arquivo se torne auditável. A
regra de leitura é conservadora: **na dúvida, reporta desconhecido, nunca
aprovado**. Ausência de data não é data recente.

Uso:
    python forja_regimentos.py                    # audita a fábrica inteira
    python forja_regimentos.py --raiz DIR         # audita outra raiz
    python forja_regimentos.py --limite-dias 30   # rigor de frescor
    python forja_regimentos.py --json             # saída estruturada
"""
from __future__ import annotations

import argparse
import io
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from datetime import date, datetime
from pathlib import Path

VERSAO = "FORJA-REGIMENTOS-v1"

# Frescor padrão. Trinta dias não é prazo legal: é o intervalo em que emendas
# regimentais costumam se acumular sem ninguém notar. Regimento com verificação
# mais antiga não está errado — está por conferir, que é diferente.
LIMITE_DIAS_PADRAO = 30

_MESES = {m: i for i, m in enumerate(
    ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho",
     "agosto", "setembro", "outubro", "novembro", "dezembro"], start=1)}

# Cada variação abaixo existe hoje no acervo. A lista é ordenada da forma mais
# específica para a mais genérica: a primeira que casar responde.
_PADROES_VERSAO = [
    r"Consolida[çc][ãa]o\s+oficial\s+vigente[:*\s]*([^\n]{3,140})",
    r"Vers[ãa]o[:*\s]*([^\n]{3,140})",
    r"Consolidad[oa]\s+at[ée][:*\s]*([^\n]{3,140})",
    r"incorporado\s+at[ée]\s+([^\n]{3,140})",
    r"[ÚU]ltima\s+emenda(?:\s+incorporada)?[:*\s|]*([^\n|]{3,140})",
    r"compilado\s+at[ée]\s+([^\n]{3,140})",
    r"(?m)^\s*versao(?:_oficial)?\s*:\s*([^\n]{3,140})",
    r"Atualizado\s+pelos\s+Assentos\s+Regimentais[:*\s]*([^\n]{3,140})",
    r"Ato\s+Normativo\s+Base[:*\s|]*([^\n|]{3,140})",
]
# Rótulos de data. Não se captura o valor aqui de propósito: o acervo tem o
# rótulo em prosa ("**Data da verificação:** 2026-07-23") e em célula de tabela
# ("| **Data de Download/Atualização** | 2026-07-06 |"). Um regex que tentasse
# capturar os dois truncava a célula e devolvia data inválida — pior que não
# achar, porque produz confiança falsa. Aqui o rótulo só localiza a LINHA; a
# data é extraída dela por _extrai_data, que sabe reconhecer os três formatos.
_ROTULOS_DATA = [
    r"Data\s+da\s+verifica[çc][ãa]o",
    r"Data\s+de\s+Download(?:/Atualiza[çc][ãa]o)?",
    r"Data\s+do\s+[Dd]ownload(?:\s+e\s+confer[êe]ncia)?",
    r"Conferido\s+em",
    r"Baixado\s+em",
    # Frontmatter YAML — metade do acervo usa esta forma, e ignorá-la fazia o
    # auditor acusar como "sem data" arquivo que traz a data na primeira linha.
    r"^\s*data_verificacao\w*\s*:",
    r"^\s*data_download\s*:",
    r"^\s*download_em\s*:",
    r"^\s*data_conferencia\s*:",
    # Rótulo fraco, deliberadamente por último: aparece com frequência dentro da
    # linha de versão, ao lado de outra data.
    r"atualizad[oa]\s+em",
]
_SECAO_EMENDAS = re.compile(r"emendas?[\s_]+posterior", re.I)
_URL_OFICIAL = re.compile(r"https?://[^\s)\]]+")


def _extrai_data(bruto: str) -> date | None:
    """Extrai data de formatos mistos. Devolve None quando não tem certeza."""
    bruto = bruto.strip().strip("*| ")
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", bruto)
    if m:
        try:
            return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            return None
    m = re.search(r"(\d{1,2})/(\d{1,2})/(\d{4})", bruto)
    if m:
        try:
            return date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
        except ValueError:
            return None
    m = re.search(r"(\d{1,2})\s+de\s+([a-zçã]+)\s+de\s+(\d{4})", bruto, re.I)
    if m and m.group(2).lower() in _MESES:
        try:
            return date(int(m.group(3)), _MESES[m.group(2).lower()], int(m.group(1)))
        except ValueError:
            return None
    return None


def _primeiro(padroes: list[str], texto: str) -> str | None:
    for pat in padroes:
        m = re.search(pat, texto, re.I)
        if m:
            valor = m.group(1).strip().strip("*| ").rstrip(".")
            if valor and valor.lower() not in {"n/a", "-", "--"}:
                return valor
    return None


def _data_do_rotulo(texto: str) -> date | None:
    """Localiza o rótulo de data e extrai a data que vem DEPOIS dele, na linha.

    Duas decisões que parecem detalhe e não são:

    1. A data é lida a partir do fim do rótulo, nunca da linha inteira. A linha
       "Versão: vigente desde 09/03/2024, texto consolidado atualizado em
       08/06/2026" contém duas datas e um rótulo fraco ("atualizado em") no
       meio. Ler a linha toda devolvia 2024 e marcava como vencido um arquivo
       conferido em julho de 2026.

    2. Os rótulos são percorridos em ordem de especificidade, no laço externo.
       "Data do download e conferência" tem de vencer "atualizado em" quando os
       dois aparecem no mesmo arquivo.
    """
    linhas = texto.splitlines()
    for rot in _ROTULOS_DATA:
        padrao = re.compile(rot, re.I | (re.M if rot.startswith("^") else 0))
        for linha in linhas:
            m = padrao.search(linha)
            if m:
                d = _extrai_data(linha[m.end():])
                if d:
                    return d
    return None


@dataclass
class Regimento:
    tribunal: str
    caminho: str
    versao: str | None = None
    verificadoEm: str | None = None
    diasDesdeVerificacao: int | None = None
    urlOficial: str | None = None
    temSecaoEmendas: bool = False
    achados: list[dict] = field(default_factory=list)

    @property
    def bloqueia(self) -> bool:
        return any(a["sev"] == "P0" for a in self.achados)


def auditar_arquivo(caminho: Path, *, hoje: date, limite_dias: int) -> Regimento:
    texto = caminho.read_text(encoding="utf-8", errors="replace")
    cabecalho = texto[:4000]
    trib = re.search(r"REGIMENTO_INTERNO_([A-Z0-9_]+)", caminho.name)
    reg = Regimento(tribunal=(trib.group(1) if trib else "?"), caminho=str(caminho))

    reg.versao = _primeiro(_PADROES_VERSAO, cabecalho)
    d = _data_do_rotulo(cabecalho)
    if d:
        reg.verificadoEm = d.isoformat()
        reg.diasDesdeVerificacao = (hoje - d).days
    url = _URL_OFICIAL.search(cabecalho)
    reg.urlOficial = url.group(0) if url else None
    reg.temSecaoEmendas = bool(_SECAO_EMENDAS.search(texto))

    if not reg.versao:
        reg.achados.append({
            "sev": "P0", "codigo": "sem_versao",
            "problema": "cabeçalho não declara até qual emenda o texto está consolidado",
            "acao": "acrescente a linha 'Consolidação oficial vigente: ...'"})
    if not reg.verificadoEm:
        reg.achados.append({
            "sev": "P0", "codigo": "sem_data_verificacao",
            "problema": "cabeçalho não declara data de verificação — ausência de data não é data recente",
            "acao": "acrescente 'Data da verificação e do download: AAAA-MM-DD'"})
    elif reg.diasDesdeVerificacao is not None and reg.diasDesdeVerificacao > limite_dias:
        reg.achados.append({
            "sev": "P1", "codigo": "verificacao_vencida",
            "problema": (f"última verificação há {reg.diasDesdeVerificacao} dias "
                         f"(limite {limite_dias}) — conferir emendas posteriores antes de citar"),
            "acao": "consulte o diário eletrônico do tribunal e atualize o cabeçalho"})
    if not reg.urlOficial:
        reg.achados.append({
            "sev": "P1", "codigo": "sem_fonte",
            "problema": "cabeçalho não aponta a URL oficial de onde o texto veio",
            "acao": "registre a fonte oficial para que a conferência seja repetível"})
    if not reg.temSecaoEmendas:
        reg.achados.append({
            "sev": "P1", "codigo": "sem_secao_emendas",
            "problema": ("sem seção de emendas posteriores — o protocolo exige que emendas "
                         "editadas depois da consolidação sejam anexadas ao próprio arquivo"),
            "acao": "crie a seção final 'Emendas posteriores', ainda que para declarar que não há"})
    return reg


def auditar(raiz: Path, *, hoje: date | None = None,
            limite_dias: int = LIMITE_DIAS_PADRAO) -> list[Regimento]:
    hoje = hoje or date.today()
    arquivos = [p for p in sorted(raiz.rglob("REGIMENTO_INTERNO_*.md"))
                if not any(x in p.parts for x in (".git", "node_modules", "__pycache__"))]
    return [auditar_arquivo(p, hoje=hoje, limite_dias=limite_dias) for p in arquivos]


def _relatorio(regs: list[Regimento]) -> str:
    linhas = [f"AUDITORIA DE REGIMENTOS — {VERSAO}", "=" * 72]
    por_tribunal: dict[str, list[Regimento]] = {}
    for r in regs:
        por_tribunal.setdefault(r.tribunal, []).append(r)
    for trib in sorted(por_tribunal):
        linhas.append(f"\n{trib}")
        for r in por_tribunal[trib]:
            marca = "P0" if r.bloqueia else ("P1" if r.achados else "ok")
            versao = r.versao or "(versão não declarada)"
            data = r.verificadoEm or "(sem data)"
            linhas.append(f"  [{marca:2s}] {versao[:70]}")
            linhas.append(f"       verificado em {data} · {Path(r.caminho).parent.name[:58]}")
            for a in r.achados:
                linhas.append(f"       - {a['sev']} {a['codigo']}: {a['problema'][:88]}")
    p0 = sum(1 for r in regs if r.bloqueia)
    p1 = sum(1 for r in regs if r.achados and not r.bloqueia)
    linhas += ["", "=" * 72,
               f"{len(regs)} arquivo(s) · {p0} com bloqueio · {p1} com ressalva · "
               f"{len(regs) - p0 - p1} em ordem"]
    return "\n".join(linhas)


def main() -> int:
    ap = argparse.ArgumentParser(description="audita atualidade dos regimentos arquivados")
    ap.add_argument("--raiz", default=str(Path(__file__).resolve().parent.parent))
    ap.add_argument("--limite-dias", type=int, default=LIMITE_DIAS_PADRAO)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--hoje", help="data de referência AAAA-MM-DD (para teste)")
    args = ap.parse_args()

    hoje = datetime.strptime(args.hoje, "%Y-%m-%d").date() if args.hoje else date.today()
    regs = auditar(Path(args.raiz), hoje=hoje, limite_dias=args.limite_dias)
    if args.json:
        print(json.dumps({"versao": VERSAO, "raiz": args.raiz,
                          "regimentos": [asdict(r) for r in regs]},
                         ensure_ascii=False, indent=2))
    else:
        print(_relatorio(regs))
    return 1 if any(r.bloqueia for r in regs) else 0


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    raise SystemExit(main())
