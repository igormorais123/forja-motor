"""Diabob no Grok 4.5 — red team adversarial por modelo de outra família.

O Diabob existe para dizer o que a análise principal está evitando ver. Isso
falha quando quem faz o red team é o mesmo modelo que produziu a análise:
ele repete os próprios pontos cegos com voz mais dura. Nomear o modelo é o
que transforma o Diabob de tom em contraditório real.

Grok 4.5 foi escolhido por determinação do titular (26/07/2026) e sustentado
por medição: barato, rápido e, na primeira bancada, resistente às duas provas
de armadilha em que o Kimi K3 confirmou premissa falsa.

O parecer que sai daqui é insumo interno de auditoria. Não vai para a peça,
não vira fundamento e não substitui o F7 — como todo modelo externo na FORJA,
o Diabob propõe objeções, não afirma fatos.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import forja_modelos as fm

# Rota padrão desde 06/08/2026, por ordem do titular: o MESMO Grok 4.5, pela
# assinatura do Cursor. `grok-4.5` (OpenRouter) fica como reserva — a mesma
# família e o mesmo modelo, então cair para ela não muda o contraditório, só o
# meio de transporte e o custo.
MODELO_PADRAO = "grok-4.5-cursor"
MODELO_RESERVA = "grok-4.5"
SKILL = Path.home() / ".claude" / "skills" / "diabob" / "SKILL.md"

PERSONA = """Você é Diabob: crítico contrarian, red team retórico e detector de autoengano.

Regras:
- Comece pelo ponto mais incômodo e mais útil, não pelo mais fácil.
- Separe fato, inferência e provocação. Não exagere certeza; leitura é leitura.
- Troque crueldade por precisão: a pancada precisa ser útil.
- Ataque a tese, nunca quem a escreveu.
- Não invente dispositivo, precedente, número ou data. Se a objeção depende de
  uma fonte que você não tem, diga que depende e nomeie qual seria.
- Feche com um teste de realidade verificável: o que observar para saber se
  você está certo.

Responda em português do Brasil."""

MOLDE = """Analise a seguir. Faça o red team dela.

--- ANÁLISE SOB EXAME ---
{alvo}
--- FIM ---

Entregue:
1. O ponto que a análise está evitando.
2. As três objeções mais fortes, da mais forte para a mais fraca.
3. Qual delas, se verdadeira, derruba a conclusão inteira.
4. O teste de realidade: o que observar para decidir entre você e a análise."""


def red_team(
    alvo: str,
    *,
    modelo: str = MODELO_PADRAO,
    max_tokens: int = 2048,
    orcamento: fm.Orcamento | None = None,
    caso: str | None = None,
    permitir_reserva: bool = True,
) -> dict:
    """Roda o Diabob sobre um texto e devolve o recibo da chamada.

    Se a rota do Cursor falhar (sem login, CLI ausente, tempo esgotado), cai
    para a mesma família pelo OpenRouter e **declara a queda** no recibo. O
    contraditório não pode parar por meio de transporte; o que não se admite é
    a queda silenciosa, porque ela troca assinatura por gasto sem ninguém ver.
    """
    if not alvo.strip():
        raise fm.ForjaModeloError("Diabob sem alvo: red team de texto vazio não é red team")
    prompt = MOLDE.format(alvo=alvo.strip())
    try:
        recibo = fm.chamar(
            modelo, prompt, sistema=PERSONA, max_tokens=max_tokens,
            fase="red_team", papel="diabob", orcamento=orcamento,
        )
        recibo["rotaDegradada"] = None
    except fm.ForjaModeloError as erro:
        if not (permitir_reserva and modelo == MODELO_PADRAO):
            raise
        recibo = fm.chamar(
            MODELO_RESERVA, prompt, sistema=PERSONA, max_tokens=max_tokens,
            fase="red_team", papel="diabob", orcamento=orcamento,
        )
        recibo["rotaDegradada"] = f"{MODELO_PADRAO} indisponível: {erro}"
    recibo["caso"] = caso
    recibo["persona"] = "diabob"
    return recibo


def main() -> None:
    parser = argparse.ArgumentParser(description="Diabob adversarial por modelo externo")
    parser.add_argument("--arquivo", help="arquivo com a análise sob exame")
    parser.add_argument("--texto", help="texto direto, quando não houver arquivo")
    parser.add_argument("--modelo", default=MODELO_PADRAO)
    parser.add_argument("--caso")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if args.arquivo:
        alvo = Path(args.arquivo).read_text(encoding="utf-8", errors="replace")
    elif args.texto:
        alvo = args.texto
    else:
        parser.error("informe --arquivo ou --texto")

    recibo = red_team(alvo, modelo=args.modelo, caso=args.caso)
    if args.json:
        print(json.dumps(recibo, ensure_ascii=False, indent=2))
    else:
        print(f"[diabob · {recibo['modelo']} · {recibo['segundos']}s · "
              f"US$ {recibo['custoUsd']:.4f}]\n")
        if recibo.get("rotaDegradada"):
            print(f"[rota degradada] {recibo['rotaDegradada']}\n")
        print(recibo["conteudo"])


if __name__ == "__main__":
    main()
