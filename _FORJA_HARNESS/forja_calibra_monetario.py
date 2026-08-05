# -*- coding: utf-8 -*-
"""Calibração da detecção de material econômico — evidência reexecutável.

POR QUE EXISTE. A especificação dos gates L9-L13 (plano 41) faz o gate incidir
só sobre produto com material econômico. A primeira redação dessa detecção
aceitava "sequência numérica com separador de milhar", e a medição mostrou que
isso lê `RE 1.395.147/PR`, `Decreto 10.201/2020` e `Lei 9.469/1997` como
dinheiro — em peça jurídica o caso dominante, não a exceção. O gate nasceria
travando toda peça que cita lei.

Essa medição foi feita primeiro por script ad hoc não persistido. Os números
iam para o relatório ao Fábio como evidência. **Número em relatório de evidência
sem meio de reexecução é atestação sem lastro** — a mesma falha que o Igor
apontou em 30/07/2026 num recibo que trazia `visualQa: 57/57, pass` sem
correspondência na resposta do revisor. Daí este arquivo: qualquer revisor
reproduz os números com um comando, e o gate é calibrado contra o acervo real
antes de bloquear, e não depois.

USO
    python forja_calibra_monetario.py --raiz ".." --saida CALIBRACAO_MONETARIA.json

Devolve, para as duas regras, quantos documentos do acervo seriam considerados
econômicos, e amostra os casos em que as regras divergem — que são exatamente
os falsos positivos que a regra ampla criaria.
"""
import argparse
import json
import re
import sys
from pathlib import Path

FORJA = Path(__file__).resolve().parent

# --- Regra AMPLA (redação original do plano 41, REJEITADA pela medição) -------
# "R$, sequência numérica com separador de milhar, percentual sobre base".
_AMPLA = re.compile(r"R\$|\b\d{1,3}(?:\.\d{3})+(?:,\d+)?\b")

# --- Regra ESTREITA (redação corrigida) --------------------------------------
# Exige marcador de moeda explícito e descarta numeral precedido de referência
# normativa ou processual. A lista de rótulos é a que aparece de fato nas peças
# do escritório; ampliá-la é barato, e cada acréscimo deve vir de um falso
# positivo observado, nunca de imaginação.
_ROTULO_JURIDICO = (
    r"(?:lei(?:\s+complementar)?|decreto(?:-lei)?|s[úu]mula|enunciado|tema|"
    r"medida\s+provis[óo]ria|resolu[çc][ãa]o|instru[çc][ãa]o\s+normativa|portaria|"
    r"emenda|adin?|adc|adpf|re|resp|aresp|ai|ag|agint|edcl|hc|ms|rms|"
    r"processo|autos|proc\.|art(?:igo)?s?\.?|inc(?:iso)?\.?|par[áa]grafo|§)"
)
_ANTES_JURIDICO = re.compile(_ROTULO_JURIDICO + r"[\s ]*n?[ºo°]?[\s .]*$", re.I)

_MOEDA = re.compile(
    r"(R\$|\breais\b|\bmilh[õo]es\s+de\s+reais\b|\bbilh[õo]es\s+de\s+reais\b)", re.I)
_CIFRA = re.compile(r"R\$[\s ]*\d[\d.\s]*(?:,\d{2})?")


def _texto(caminho):
    try:
        return caminho.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


def ocorrencias_ampla(texto):
    """Casamentos da regra ampla, separando os que são referência jurídica."""
    monetarias, juridicas = [], []
    for m in _AMPLA.finditer(texto):
        if m.group(0) == "R$":
            monetarias.append(m.group(0))
            continue
        antes = texto[max(0, m.start() - 40):m.start()]
        (juridicas if _ANTES_JURIDICO.search(antes) else monetarias).append(m.group(0))
    return monetarias, juridicas


def economico_estreito(texto):
    """A regra corrigida: exige marcador de moeda explícito."""
    return bool(_MOEDA.search(texto))


def economico_amplo(texto):
    return bool(_AMPLA.search(texto))


def varrer(raiz, extensoes=(".md", ".txt"), limite_bytes=4_000_000):
    raiz = Path(raiz)
    docs = []
    for p in raiz.rglob("*"):
        if (p.suffix.lower() not in extensoes or not p.is_file()
                or "node_modules" in p.parts or ".git" in p.parts):
            continue
        try:
            if p.stat().st_size > limite_bytes:
                continue
        except OSError:
            continue
        docs.append(p)
    return docs


def calibrar(raiz, amostra=8):
    docs = varrer(raiz)
    total = 0
    amplos = estreitos = 0
    divergentes = []
    total_jur = total_mon = 0
    for p in docs:
        t = _texto(p)
        if t is None:
            continue
        total += 1
        a, e = economico_amplo(t), economico_estreito(t)
        amplos += a
        estreitos += e
        mon, jur = ocorrencias_ampla(t)
        total_mon += len(mon)
        total_jur += len(jur)
        if a and not e and len(divergentes) < amostra:
            _, jur_doc = ocorrencias_ampla(t)
            divergentes.append({
                "arquivo": str(p.relative_to(raiz)),
                "referenciasJuridicasLidasComoDinheiro": len(jur_doc),
                "exemplos": _amostrar_contexto(t, 3),
            })
    return {
        "versao": "FORJA-CALIBRA-MONETARIO-v1",
        "raiz": str(Path(raiz).resolve()),
        "extensoes": list((".md", ".txt")),
        "documentos": total,
        "regraAmpla": {
            "descricao": "R$ OU sequência com separador de milhar (redação original, rejeitada)",
            "documentosTocados": amplos,
            "percentual": round(100 * amplos / max(1, total), 1),
        },
        "regraEstreita": {
            "descricao": "exige marcador de moeda explícito; descarta numeral após rótulo normativo/processual",
            "documentosTocados": estreitos,
            "percentual": round(100 * estreitos / max(1, total), 1),
        },
        "ocorrenciasComSeparadorDeMilhar": {
            "total": total_mon + total_jur,
            "referenciaJuridica": total_jur,
            "percentualReferenciaJuridica": round(100 * total_jur / max(1, total_mon + total_jur), 1),
        },
        "documentosQueSoAReguaAmplaTocaria": amplos - estreitos,
        "amostraDeFalsoPositivo": divergentes,
        "limite": ("Mede INCIDÊNCIA da detecção, não correção do gate. Um documento "
                   "corretamente detectado como econômico ainda pode passar ou reprovar "
                   "nos gates L9-L13 por outros motivos."),
    }


def _amostrar_contexto(texto, n):
    out = []
    for m in _AMPLA.finditer(texto):
        if m.group(0) == "R$":
            continue
        antes = texto[max(0, m.start() - 40):m.start()]
        if _ANTES_JURIDICO.search(antes):
            ini = max(0, m.start() - 24)
            out.append(re.sub(r"\s+", " ", texto[ini:m.end() + 8]).strip())
        if len(out) >= n:
            break
    return out


def main():
    ap = argparse.ArgumentParser(description="Calibração da detecção de material econômico")
    ap.add_argument("--raiz", default=str(FORJA.parent))
    ap.add_argument("--saida", default=None)
    args = ap.parse_args()
    rel = calibrar(args.raiz)
    texto = json.dumps(rel, ensure_ascii=False, indent=2)
    if args.saida:
        Path(args.saida).write_text(texto, encoding="utf-8")
    print(texto)
    return 0


if __name__ == "__main__":
    sys.exit(main())
