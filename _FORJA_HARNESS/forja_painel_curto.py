"""Painel de vozes curtas — ponto de vista de outros modelos, em poucas linhas.

Por que existe: a esteira decide com duas famílias de modelo (Claude e Codex) e
um contraditório (Grok, no Diabob). Isso cobre o eixo principal e não cobre o
ângulo lateral — a leitura que nenhum dos três teria porque os três foram
treinados para o mesmo tipo de resposta cuidadosa. A assinatura do Cursor já dá
acesso a modelos de outras casas; o que faltava era um lugar onde a opinião
deles caiba sem virar trabalho.

O que este painel NÃO é:

- Não é gate. Nada aqui reprova fase, e a ausência do artefato não bloqueia nada.
- Não é fonte. Nenhuma observação daqui vira fundamento, citação ou fato da
  peça. Modelo marcado com `nao_afirma_fato` no registro tem isso medido: o
  Kimi K3 fez 0 de 6 na condição solta da bancada de 26/07/2026, com quatro
  invenções. Ele é bom de ângulo e péssimo de fonte, e as duas coisas convivem.
- Não é conselho. Helena, Cícero e Diabob são obrigatórios e continuam sendo;
  este painel é opinião avulsa, e o próprio artefato declara isso.

**O tamanho é cortado no código, não no prompt.** Pedir brevidade a um modelo é
sugestão; `LIMITE_OBSERVACOES` e `LIMITE_CARACTERES` são regra. Um painel que
devolve três telas de texto por voz teria o custo que o titular disse não querer
e ninguém leria até o fim — o que o transformaria em ritual.

Uso:
    python forja_painel_curto.py --arquivo blueprint.md --caso CASO-19 \
        --saida F4_PAINEL_CURTO.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

import forja_envio_externo as envio
import forja_modelos as fm

VERSAO = "FORJA-PAINEL-CURTO-v1"
FORJA = Path(__file__).resolve().parent

# As vozes do painel. Ordem estável: o artefato é comparável entre casos.
#
# `opus-5-cursor` é **controle, não par**: é a mesma família que escreve a peça
# e que revisa em F7-B. Ele está aqui para dar régua — sem um modelo de ponta na
# mesma prova, o índice de uma voz nova é número sem escala — e para medir
# quanto a voz da própria casa acrescenta sobre as de fora. Concordância dele
# com a análise principal é eco previsível, não confirmação (Lição 99).
VOZES_PADRAO = ("kimi-k3-cursor", "glm-5.2-cursor", "grok-4.5-cursor",
                "luna-5.6-cursor", "opus-5-cursor")

# Voz que compartilha a família do produtor da peça. O artefato marca, e quem
# lê o placar precisa saber antes de comparar índices.
CONTROLE_MESMA_FAMILIA = ("opus-5-cursor",)

# Tetos duros. O de entrada existe porque mandar a peça inteira para uma opinião
# de quatro linhas é desperdício de contexto e de atenção; o de saída, porque
# voz curta que devolve ensaio deixa de ser curta.
LIMITE_ALVO = 6_000
LIMITE_OBSERVACOES = 4
LIMITE_CARACTERES = 300
MAX_TOKENS = 700

PERSONA = """Você lê um documento jurídico de trabalho de um escritório brasileiro e dá
o SEU ponto de vista, em poucas linhas. Você é uma voz lateral, não o revisor.

Regras, todas obrigatórias:
- No máximo {n} observações. Uma linha cada, começando com "- ".
- Cada observação em no máximo {c} caracteres. Frase inteira, sem abreviação.
- Diga o que os outros leitores provavelmente NÃO vão dizer. Concordância não
  ajuda ninguém: se você só concorda, diga isso em uma linha e pare.
- NÃO cite lei, artigo, súmula, precedente, número de processo, data ou valor.
  Você não é fonte de fato aqui. Se a sua observação depende de um dado, diga
  qual dado precisa ser conferido, sem afirmar qual é.
- Não elogie e não resuma o documento. Quem pediu já o leu.

Responda em português do Brasil, sem preâmbulo e sem fecho."""

MOLDE = """Documento de trabalho abaixo. Dê o seu ponto de vista.

--- DOCUMENTO ---
{alvo}
--- {fim} ---

O que você vê aqui que um revisor cuidadoso deste escritório provavelmente
deixaria passar?"""

# Aviso de recorte, e ele não é cosmético.
#
# Medido em 07/08/2026, nos três primeiros casos reais: os três alvos passavam
# de 6.000 caracteres, e as vozes gastaram 3 de 24 observações reclamando que "o
# documento está cortado no item 8" e que "a peça está incompleta". **O corte
# era meu.** Duas dessas observações afirmam um defeito inexistente na peça, com
# aparência de achado acionável — o pior tipo de ruído.
#
# O artefato já gravava `alvoTruncado: true`. O flag existia para quem lê o
# JSON e não para quem faz o trabalho: o prompt não dizia nada. Estado conhecido
# pelo sistema e escondido do agente que depende dele é defeito de projeto, não
# de modelo.
AVISO_RECORTE = """
ATENÇÃO: o texto acima é um RECORTE dos primeiros {n} caracteres de um documento
maior. Ele termina no meio de propósito. NÃO comente que está cortado,
incompleto ou sem fecho, e não conclua nada sobre pedidos, conclusão ou partes
que não aparecem — isso é limitação de quem enviou, não defeito da peça."""


def _agora() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def _norm(texto: str) -> str:
    """Forma canônica para o identificador: sem acento, sem caixa, sem espaço duplo."""
    sem_acento = unicodedata.normalize("NFKD", texto)
    sem_acento = "".join(c for c in sem_acento if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", sem_acento).strip().casefold()


def obs_id(modelo: str, texto: str) -> str:
    """Identificador estável da observação, para a decisão poder apontar para ela.

    Deriva do texto normalizado: a mesma observação do mesmo modelo tem sempre o
    mesmo id, e duas observações diferentes não colidem na prática. Estável é o
    que importa — a decisão humana é registrada dias depois, num arquivo à parte.
    """
    semente = f"{modelo}::{_norm(texto)}".encode("utf-8")
    return hashlib.sha256(semente).hexdigest()[:12]


def extrair(bruto: str) -> tuple[list[str], dict]:
    """Tira as observações do texto livre e aplica os tetos.

    Devolve também o que foi cortado. Corte silencioso é o modo de falha que a
    casa já pagou em outro gate: a saída fica com cara de completa e não é.
    """
    linhas = []
    for linha in (bruto or "").splitlines():
        limpa = linha.strip()
        if not limpa:
            continue
        # Aceita "- ", "* ", "1. ", "1) " e a linha nua. O molde pede um formato;
        # exigir que o modelo o siga para a resposta valer seria trocar conteúdo
        # por obediência.
        limpa = re.sub(r"^(?:[-*•]|\d+[.)])\s*", "", limpa).strip()
        if not limpa or limpa.startswith("---"):
            continue
        linhas.append(limpa)

    excedentes = max(0, len(linhas) - LIMITE_OBSERVACOES)
    linhas = linhas[:LIMITE_OBSERVACOES]
    truncadas = 0
    finais = []
    for linha in linhas:
        if len(linha) > LIMITE_CARACTERES:
            truncadas += 1
            linha = linha[:LIMITE_CARACTERES].rstrip() + "…"
        finais.append(linha)
    return finais, {"observacoesDescartadas": excedentes, "observacoesTruncadas": truncadas}


def ouvir(alvo: str, *, modelo: str, caso: str | None = None,
          fase: str | None = None) -> dict:
    """Chama uma voz e devolve o bloco dela, já cortado nos tetos."""
    registro = fm.MODELOS.get(modelo)
    if registro is None:
        raise fm.ForjaModeloError(f"voz fora do registro da FORJA: {modelo!r}")

    recorte = alvo.strip()
    cortado = len(recorte) > LIMITE_ALVO
    if cortado:
        recorte = recorte[:LIMITE_ALVO]

    sistema = PERSONA.format(n=LIMITE_OBSERVACOES, c=LIMITE_CARACTERES)
    if "nao_afirma_fato" in registro.restricoes:
        # A restrição é medida e vira instrução. Ela não substitui a régua: o
        # artefato marca `podeAfirmarFato: false` de qualquer forma, porque
        # instrução em prompt é pedido e marcação em artefato é fato do registro.
        sistema += ("\n\nATENÇÃO: você não é fonte de fato neste escritório. "
                    "Qualquer dado seu será descartado sem ser conferido.")

    prompt = MOLDE.format(
        alvo=recorte,
        fim="RECORTE INTERROMPIDO AQUI" if cortado else "FIM DO DOCUMENTO")
    if cortado:
        prompt += AVISO_RECORTE.format(n=LIMITE_ALVO)

    recibo = fm.chamar(
        modelo, prompt, sistema=sistema,
        max_tokens=MAX_TOKENS, fase=fase or "painel_curto", papel="voz_curta",
    )
    observacoes, corte = extrair(recibo["conteudo"])
    # A ancoragem é calculada AQUI, com o alvo em mãos, e só o número é gravado.
    # Guardar o texto do documento no artefato para medir depois duplicaria
    # conteúdo do caso sem necessidade — o número basta, e não reconstrói nada.
    from forja_painel_indicadores import ancoragem_de, citacoes_fora_do_documento

    palavras_alvo = ancoragem_de(recorte)
    return {
        "modelo": registro.id,
        "familia": registro.familia,
        "provedor": registro.provedor,
        "restricoes": list(registro.restricoes),
        "podeAfirmarFato": "nao_afirma_fato" not in registro.restricoes,
        # Régua da comparação, e não um detalhe: voz da mesma família do
        # produtor não é par das outras. Sem esta marca, alguém compara o
        # índice do controle com o das vozes de fora como se fossem a mesma
        # coisa — que é o erro que a Lição 99 documenta.
        "controleMesmaFamilia": registro.id in CONTROLE_MESMA_FAMILIA,
        "segundos": recibo["segundos"],
        "custoUsd": recibo["custoUsd"],
        "alvoTruncado": cortado,
        **corte,
        "observacoes": [
            {"obsId": obs_id(registro.id, texto), "texto": texto,
             "ancoragem": palavras_alvo(texto),
             # Citar o que o documento cita é ler; citar o que não está lá é
             # inventar. Só aqui o alvo está em mãos para saber a diferença.
             "citouForaDoDocumento": citacoes_fora_do_documento(texto, recorte)}
            for texto in observacoes
        ],
    }


def painel(alvo: str, *, vozes=VOZES_PADRAO, caso: str | None = None,
           fase: str | None = None, classe: str | None = None,
           confirmado: bool = False, arquivo: str | None = None) -> dict:
    """Roda todas as vozes e monta o artefato.

    Falha de uma voz não derruba as outras: o painel é opinião, e opinião
    parcial continua servindo. A falha fica declarada, para que ninguém leia
    "duas vozes" onde só uma respondeu.

    **Nada sai sem passar pelo porteiro.** Até 09/08/2026 esta função mandava
    trecho de documento de cliente para cinco provedores de fora sem
    classificação, sem confirmação e sem registro — e ninguém conseguia
    responder o que tinha saído. Agora a classe do documento é obrigatória,
    `autos` é recusa dura, e cada envio deixa recibo.
    """
    if not alvo.strip():
        raise fm.ForjaModeloError("painel sem alvo: não se opina sobre texto vazio")

    recorte = alvo.strip()[:LIMITE_ALVO]
    recibo_envio = envio.autorizar(
        recorte, classe=classe or "", confirmado=confirmado,
        destino=list(vozes), caso=caso, arquivo=arquivo)

    blocos, falhas = [], []
    for modelo in vozes:
        try:
            blocos.append(ouvir(alvo, modelo=modelo, caso=caso, fase=fase))
        except fm.ForjaModeloError as erro:
            falhas.append({"modelo": modelo, "erro": str(erro)[:300]})

    return {
        "contrato": VERSAO,
        "caso": caso,
        "fase": fase,
        "em": _agora(),
        "natureza": (
            "Opinião interna e avulsa. NÃO é gate, NÃO é conselho obrigatório e "
            "NÃO é fonte: nenhuma observação daqui vira fundamento, citação, "
            "número ou data da peça. Serve para o redator ver um ângulo que as "
            "vozes principais não veriam, e para medir se essas vozes agregam."
        ),
        "tetos": {
            "caracteresDoAlvo": LIMITE_ALVO,
            "observacoesPorVoz": LIMITE_OBSERVACOES,
            "caracteresPorObservacao": LIMITE_CARACTERES,
            "maxTokens": MAX_TOKENS,
        },
        # Recibo do que atravessou a porta, no próprio artefato: a pergunta
        # "isto saiu daqui?" tem de ter resposta sem depender de alguém lembrar
        # de abrir o ledger.
        "envioExterno": recibo_envio,
        "vozes": blocos,
        "falhas": falhas,
        # Preenchido depois pelo humano ou pelo redator, e colhido por
        # `forja_contribuicao.py colher`. Nasce em branco de propósito: decisão
        # que o próprio painel escreve não mede nada.
        "decisoes": [
            {"obsId": obs["obsId"], "modelo": bloco["modelo"],
             "veredito": None, "duplicadaDe": None, "motivo": None}
            for bloco in blocos for obs in bloco["observacoes"]
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--arquivo", type=Path, help="documento sob opinião")
    parser.add_argument("--texto", help="texto direto, quando não houver arquivo")
    parser.add_argument("--caso")
    parser.add_argument("--fase")
    parser.add_argument("--vozes", nargs="*", default=list(VOZES_PADRAO))
    parser.add_argument("--classe", choices=sorted(envio.CLASSES),
                        help="origem do documento. `produto_proprio` é o que a "
                             "fábrica escreveu e pode ir para crítica externa; "
                             "`autos` e `misto` são recusados")
    parser.add_argument("--confirmo-envio-externo", action="store_true",
                        help="assume a decisão de mandar este texto a provedor "
                             "de fora; fica registrado no ledger de envios")
    parser.add_argument("--saida", type=Path,
                        help="grava o artefato do painel (ex.: F4_PAINEL_CURTO.json)")
    args = parser.parse_args()

    if args.arquivo:
        alvo = args.arquivo.read_text(encoding="utf-8", errors="replace")
    elif args.texto:
        alvo = args.texto
    else:
        parser.error("informe --arquivo ou --texto")

    try:
        resultado = painel(alvo, vozes=tuple(args.vozes), caso=args.caso,
                           fase=args.fase, classe=args.classe,
                           confirmado=args.confirmo_envio_externo,
                           arquivo=str(args.arquivo) if args.arquivo else None)
    except envio.EnvioBloqueado as erro:
        print(f"[porteiro] {erro}")
        return 2
    # Localizador do alvo, para que um indicador criado depois possa ser
    # recomputado sem chamar os modelos de novo — nova chamada devolveria texto
    # diferente, com outros identificadores, e a fila contaria duas vezes.
    resultado["alvoArquivo"] = str(args.arquivo) if args.arquivo else None

    if args.saida:
        args.saida.parent.mkdir(parents=True, exist_ok=True)
        args.saida.write_text(
            json.dumps(resultado, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"painel em {args.saida}")

    for bloco in resultado["vozes"]:
        marca = "" if bloco["podeAfirmarFato"] else "  [não é fonte de fato]"
        print(f"\n[{bloco['modelo']} · {bloco['segundos']}s]{marca}")
        for obs in bloco["observacoes"]:
            print(f"  ({obs['obsId']}) {obs['texto']}")
        if bloco["observacoesDescartadas"]:
            print(f"  … {bloco['observacoesDescartadas']} observação(ões) além do teto, descartada(s)")
    for falha in resultado["falhas"]:
        print(f"\n[{falha['modelo']}] não respondeu: {falha['erro']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
