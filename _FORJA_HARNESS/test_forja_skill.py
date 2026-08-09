# -*- coding: utf-8 -*-
"""Regressão do verificador da skill, e da própria skill da FORJA.

Dois testes com propósitos distintos, e os dois importam:

1. O verificador pega os defeitos que ele promete pegar — com fixtures sintéticas,
   porque aqui o defeito é mecânico e inventá-lo é legítimo.
2. **A skill de produção passa.** Este é o teste que trabalha: no dia em que alguém
   renomear um script, a skill deixa de descrever o sistema e o baseline avisa. Sem
   ele o verificador seria mais uma coisa instalada na rota que ninguém percorre.
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import forja_skill_doctor as doctor

falhas = 0
casos = 0


def checar(nome, condicao, detalhe=""):
    global falhas, casos
    casos += 1
    if not condicao:
        falhas += 1
        print(f"  FALHOU: {nome}" + (f" — {detalhe}" if detalhe else ""))


def _skill(base: Path, corpo: str, referencias: dict[str, str] | None = None):
    base.mkdir(parents=True, exist_ok=True)
    (base / "SKILL.md").write_text(corpo, encoding="utf-8")
    ref = base / "reference"
    ref.mkdir(exist_ok=True)
    for nome, texto in (referencias or {}).items():
        (ref / nome).write_text(texto, encoding="utf-8")
    return base


CABECALHO = "---\nname: teste\ndescription: skill de teste\n---\n\n"

with tempfile.TemporaryDirectory() as tmp:
    raiz = Path(tmp)

    # --- o defeito central: mandar rodar o que não existe --------------------
    r = doctor.auditar(_skill(raiz / "a", CABECALHO + "Rode `forja_nao_existe_mesmo.py`."))
    checar("script citado e inexistente reprova",
           any(a["gate"] == "DOC1-script-inexistente" for a in r["findings"]))
    checar("e reprovar significa não aprovado", not r["aprovado"])

    # --- e o seu contrário: script real não pode ser acusado -----------------
    r = doctor.auditar(_skill(raiz / "b", CABECALHO + "Rode `forja_baseline.py` e `forja_run.py`."))
    checar("script que existe não gera achado", r["aprovado"],
           str(r["findings"])[:180])

    # --- o defeito que DOC1 não pegava: script certo, flag de outro ----------
    # O caso real: a skill mandava `forja_alertas.py --visto`, e `--visto` é de
    # `forja_avisos.py`. Os dois arquivos existem, então DOC1 aprovava — e
    # `forja_alertas.py` sem argumento sai com sucesso, imprimindo a docstring.
    r = doctor.auditar(_skill(raiz / "i", CABECALHO +
                              "Rode `python forja_alertas.py --visto <id> --por <nome>`."))
    checar("flag que existe em outro script reprova",
           any(a["gate"] == "DOC7-flag-inexistente" for a in r["findings"]),
           str(r["findings"])[:180])
    checar("e reprovar por flag também bloqueia", not r["aprovado"])

    r = doctor.auditar(_skill(raiz / "j", CABECALHO +
                              "Rode `python forja_avisos.py --visto <id> --por <nome>`."))
    checar("a mesma flag no script certo passa", r["aprovado"],
           str(r["findings"])[:180])

    # A flag chega ao script pela continuação de linha, como no shell.
    corpo = CABECALHO + "```\npython forja_baseline.py --json out.json \\\n    --flag-que-nao-existe\n```\n"
    checar("flag na linha continuada por barra invertida também é conferida",
           any(a["gate"] == "DOC7-flag-inexistente"
               for a in doctor.auditar(_skill(raiz / "k", corpo))["findings"]))

    # --- contrato de fase inexistente ---------------------------------------
    r = doctor.auditar(_skill(raiz / "c", CABECALHO + "Veja `phase_contracts/F42.json`."))
    checar("contrato de fase inexistente reprova",
           any(a["gate"] == "DOC2-contrato-inexistente" for a in r["findings"]))
    r = doctor.auditar(_skill(raiz / "d", CABECALHO + "Veja `phase_contracts/F7.json`."))
    checar("contrato de fase existente passa", r["aprovado"])

    # --- elo para seção inexistente -----------------------------------------
    # O caso real: um "ver GATES.md, seção do F8" apontando para uma seção que
    # nunca foi escrita. Quem clica cai no topo e conclui que não há informação.
    refs = {"GATES.md": "# Gates\n\n## Como ler um finding\n\ntexto\n"}
    r = doctor.auditar(_skill(raiz / "l", CABECALHO + "Veja [x](reference/GATES.md#f8--qa-visual).",
                              refs))
    checar("elo para seção inexistente é achado",
           any(a["gate"] == "DOC8-ancora-inexistente" for a in r["findings"]),
           str(r["findings"])[:180])

    r = doctor.auditar(_skill(raiz / "m", CABECALHO + "Veja [x](reference/GATES.md#como-ler-um-finding).",
                              refs))
    checar("elo para seção existente passa", r["aprovado"], str(r["findings"])[:180])

    # A regra do GitHub: cada espaço vira um hífen, então o travessão deixa dois.
    refs2 = {"F.md": "# F\n\n## F1 — Ingestão segura\n\ntexto\n"}
    r = doctor.auditar(_skill(raiz / "n", CABECALHO + "Veja [x](reference/F.md#f1--ingestão-segura).",
                              refs2))
    checar("título com travessão gera dois hífens, e o elo certo não é acusado",
           not any(a["gate"] == "DOC8-ancora-inexistente" for a in r["findings"]),
           str(r["findings"])[:180])

    # --- referência quebrada e referência órfã ------------------------------
    r = doctor.auditar(_skill(raiz / "e", CABECALHO + "Leia [x](reference/NAO_EXISTE.md)."))
    checar("ponteiro para referência inexistente reprova",
           any(a["gate"] == "DOC4-referencia-quebrada" for a in r["findings"]))

    r = doctor.auditar(_skill(raiz / "f", CABECALHO + "Sem ponteiro nenhum.",
                              {"ORFA.md": "ninguém me abre"}))
    checar("referência que ninguém aponta é achado",
           any(a["gate"] == "DOC5-referencia-orfa" for a in r["findings"]))
    checar("mas órfã é P1, não bloqueia", r["aprovado"],
           str(r["findings"])[:180])

    # --- frontmatter ---------------------------------------------------------
    r = doctor.auditar(_skill(raiz / "g", "# Sem frontmatter\n\nnada aqui"))
    checar("skill sem name/description reprova",
           sum(1 for a in r["findings"] if a["gate"] == "DOC6-frontmatter-incompleto") == 2)

    # --- o bloco de exemplo negativo não é acusado ---------------------------
    corpo = (CABECALHO + "Não use isto:\n\n<!-- doctor:ignora -->\n"
             "`forja_que_nunca_existiu.py`\n<!-- /doctor:ignora -->\n")
    r = doctor.auditar(_skill(raiz / "h", corpo))
    checar("script citado como exemplo do que NÃO fazer é ignorado", r["aprovado"],
           str(r["findings"])[:180])

    # --- skill ausente -------------------------------------------------------
    r = doctor.auditar(raiz / "nao_existe")
    checar("pasta sem SKILL.md reprova",
           any(a["gate"] == "DOC0-skill-inexistente" for a in r["findings"]))

# --- e agora o que interessa: a skill de produção ---------------------------
real = doctor.auditar(doctor.SKILL_PADRAO)
checar("a skill da FORJA existe", real.get("conferidos", {}).get("arquivos", 0) > 0,
       "não encontrei .claude/skills/forja")
checar("a skill da FORJA está aprovada contra o disco", real["aprovado"],
       "; ".join(f"{a['gate']} em {a.get('arquivo')}: {a['problema']}"
                 for a in real["findings"])[:400])
checar("ela cita um número plausível de scripts",
       real.get("conferidos", {}).get("scriptsCitados", 0) >= 25,
       f"citou {real.get('conferidos', {}).get('scriptsCitados')}")

# --- e as cópias que os quatro carregadores leem ----------------------------
# A canônica correta não serve de nada se o Claude, o Codex, o Cursor e o Hermes
# estiverem lendo uma versão de três semanas atrás. A cópia envelhece em
# silêncio: é o modo de falha que o próprio deploy existe para evitar, e sem
# esta aferição ninguém saberia qual das cinco está certa.
import forja_skill_deploy as deploy  # noqa: E402

d = deploy.espalhar(apenas_verificar=True)
atrasadas = [x["destino"] for x in d.get("destinos", []) if not x["emDia"]]
checar("as cópias dos quatro carregadores estão em dia com a canônica",
       d.get("ok") is True,
       "desatualizadas: " + ", ".join(atrasadas) +
       " — rode `python forja_skill_deploy.py`" if atrasadas else str(d)[:200])

if falhas:
    print(f"REGRESSÃO: {falhas} de {casos} casos falharam")
    raise SystemExit(1)
print(f"ok: {casos} casos — o verificador pega script renomeado, flag de outro comando, "
      f"contrato ausente e referência quebrada, e a skill da FORJA ainda descreve a FORJA "
      f"que existe ({real['conferidos']['scriptsCitados']} scripts e "
      f"{real['conferidos']['flagsConferidas']} flags citadas, todos no disco)")
