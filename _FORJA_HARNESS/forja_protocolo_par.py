# -*- coding: utf-8 -*-
"""forja_protocolo_par.py — a ordem da casa vale para as duas famílias?

`CLAUDE.md` e `AGENTS.md` são os dois documentos que governam esta fábrica. O
Claude carrega um automaticamente; o Codex, o outro. Nenhum dos dois carrega o
do vizinho. Eles nasceram do mesmo protocolo e divergiram: medido em
11/08/2026, **seis assuntos existem só no `AGENTS.md`**, incluindo dois que a
casa trata como estruturais — "Gates computados: fim da autovalidação da
esteira" e a seção própria de anti-alucinação.

O efeito não é de arrumação. Uma ordem escrita num arquivo só **vale para uma
família de modelo e não para a outra**, e ninguém percebe, porque cada agente
lê o seu e encontra um documento coerente. O silêncio do outro lado é
indistinguível de concordância.

**Por que não unificar os dois num gerador.** Foi a primeira saída considerada
e está rejeitada: os arquivos têm conteúdo legitimamente próprio — rotas do
Codex de um lado, do Claude do outro — e uma fonte única ou incharia os dois
com o que não lhes serve, ou perderia o que é específico. A casa já paga esse
preço em `forja_skill_deploy.py`, onde a cópia gerada é idêntica de propósito;
aqui não é o caso. O que se cobra não é identidade, é **paridade de assunto**:
o que é ordem da casa aparece nos dois, com a redação de cada um.

A sonda é declarada, e é isso que a torna auditável: cada assunto tem um termo
que o identifica no texto. Termo não encontrado é assunto ausente — e o termo
se confere abrindo o arquivo, não confiando neste módulo.

Uso
    python forja_protocolo_par.py            # o retrato da paridade
    python forja_protocolo_par.py --json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

FORJA = Path(__file__).resolve().parent
RAIZ = FORJA.parent
CLAUDE = RAIZ / "CLAUDE.md"
AGENTS = RAIZ / "AGENTS.md"

VERSAO = "FORJA-PROTOCOLO-PAR-v1"

# Assunto → termo que o identifica. A lista cobre o que a medição de 11/08/2026
# mostrou divergente, mais o núcleo que precisa continuar nos dois. Assunto
# novo entra aqui quando entra num dos arquivos; é esse acréscimo que faz o
# gate valer alguma coisa.
SONDAS: tuple[tuple[str, str], ...] = (
    ("fronteira motor/acervo", "forja-auditoria"),
    ("regimento do tribunal", "regimento"),
    ("anti-alucinação", "anti-alucina"),
    ("gates computados, fim da autovalidação", "gates computados"),
    ("assinatura visual obrigatória", "assinatura visual"),
    ("conselho Helena/Cícero/Diabob", "diabob"),
    ("modelo editorial e revisão cruzada", "familyassurance"),
    ("ordem de pesquisa jurisprudencial", "orgao especial"),
    ("tratamento e citação do acervo", "origem operacional"),
    ("identidade dos atos recursais", "atos recursais"),
    ("exploração inicial em 100 perguntas", "100 perguntas"),
    ("aprendizado contínuo do retorno humano", "forja_aprendizado"),
    ("bloqueio se testa contra rotas", "forja_rotas_fonte"),
    ("vozes curtas e placar de contribuição", "forja_contribuicao"),
    ("modelo do Codex na FORJA", "gpt-5.6-luna"),
    ("Grok pela assinatura do Cursor", "grok-4.5-cursor"),
    ("repertório de skills por fase", "skills_repertorio"),
    ("vigias diários da esteira", "vigia"),
    ("fontes públicas do CNJ", "cadastro nacional"),
    # Sonda por nome de arquivo, e não pela frase do cabeçalho: os dois
    # documentos tratam o mesmo assunto com redação própria, que é justamente o
    # que este gate permite. Frase de título mediria a redação; o artefato que
    # a ordem manda abrir é o que identifica o assunto nos dois lados.
    ("protocolo de decisão arquitetural", "analise_arquitetural_e_propostas"),
    ("Archify e Graphify", "archify"),
)


def _plano(caminho: Path) -> str:
    """Minúscula, sem acento e sem quebra de linha.

    A normalização de espaço não é detalhe: a primeira medição deste par deu
    um falso "ausente" porque a expressão procurada estava partida entre duas
    linhas do arquivo. Sonda que não normaliza mede a formatação, não o texto.
    """
    t = caminho.read_text(encoding="utf-8", errors="ignore").lower()
    t = unicodedata.normalize("NFKD", t)
    t = "".join(c for c in t if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", t)


def retrato() -> dict:
    c, a = _plano(CLAUDE), _plano(AGENTS)
    so_agents, so_claude, nos_dois, em_nenhum = [], [], [], []
    for assunto, sonda in SONDAS:
        no_c, no_a = sonda in c, sonda in a
        alvo = (nos_dois if no_c and no_a else
                so_claude if no_c else so_agents if no_a else em_nenhum)
        alvo.append({"assunto": assunto, "sonda": sonda})
    return {
        "versao": VERSAO,
        "sondas": len(SONDAS),
        "nosDois": nos_dois,
        "soNoClaude": so_claude,
        "soNoAgents": so_agents,
        "emNenhum": em_nenhum,
        "divergencias": len(so_claude) + len(so_agents),
    }


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--json", action="store_true")
    a = p.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    r = retrato()
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0

    print(f"{r['versao']} — {r['sondas']} assuntos sondados")
    print(f"  nos dois arquivos      {len(r['nosDois']):3d}")
    print(f"  só no CLAUDE.md        {len(r['soNoClaude']):3d}")
    print(f"  só no AGENTS.md        {len(r['soNoAgents']):3d}")
    if r["emNenhum"]:
        print(f"  em nenhum dos dois     {len(r['emNenhum']):3d}  "
              f"(sonda errada, ou o assunto saiu do protocolo)")
    for rotulo, itens in (("só no CLAUDE.md — o Codex não vê", r["soNoClaude"]),
                          ("só no AGENTS.md — o Claude não vê", r["soNoAgents"]),
                          ("em nenhum", r["emNenhum"])):
        for x in itens:
            print(f"    [{rotulo}] {x['assunto']}  (sonda {x['sonda']!r})")
    return 1 if r["divergencias"] else 0


if __name__ == "__main__":
    sys.exit(main())
