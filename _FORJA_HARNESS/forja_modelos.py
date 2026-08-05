"""Registro e despacho dos modelos de fronteira da FORJA.

A FORJA é um sistema multimodelo: cada modelo trabalha na fase em que é melhor
e é revisado por outro de família diferente. Este módulo é a única porta de
saída para modelo externo — quem chama API solta não entra no ledger, não
respeita teto de gasto e não alimenta o gate `cross_model_review_verified`.

Três defesas estão codificadas aqui:

1. **Conteúdo vazio nunca passa silencioso.** Uma integração ingênua pode
   receber string vazia de um modelo que consumiu o orçamento raciocinando e
   seguir adiante. Aqui isso levanta erro.
2. **Todo gasto é registrado antes de ser esquecido.** O Igor paga por token
   nesses modelos; o ledger é o que permite dizer quanto custou cada peça.
3. **Teto por chamada e por execução.** Sem teto, um laço mal fechado consome
   a assinatura inteira.

O que este módulo deliberadamente NÃO faz: julgar qualidade jurídica. Modelo
externo propõe; a verificação de citação continua sendo trabalho do F7. O Kimi
K3 foi retirado do registro por decisão do titular em 26/07/2026, após reprovar
a bancada jurídica; seus resultados permanecem apenas na telemetria histórica.
A bancada CASO-04 V7, de 27/07/2026, confirmou a retirada num segundo teste
independente: último lugar em todos os seis votos cegos, por unanimidade das
três famílias de juiz, com a peça interrompida no meio da primeira síntese
depois de gastar 30 mil dos 32 mil tokens de orçamento em raciocínio interno.
"""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

FORJA = Path(__file__).resolve().parent
SECRETS = Path(os.environ.get("USERPROFILE", Path.home())) / ".secrets" / "keys.env"
LEDGER = FORJA / "telemetria" / "modelos_ledger.jsonl"

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


class ForjaModeloError(RuntimeError):
    """Falha de despacho de modelo. Nunca carrega segredo na mensagem."""


@dataclass(frozen=True)
class Modelo:
    """Um modelo de fronteira e o lugar dele na esteira."""

    id: str                      # identificador canônico interno
    familia: str                 # anthropic | openai | xai
    provedor: str                # openrouter | local
    remoto: str | None           # ID no provedor; None quando local
    forte_em: tuple[str, ...]
    fases: tuple[str, ...]
    usd_entrada_por_milhao: float = 0.0
    usd_saida_por_milhao: float = 0.0
    # Modelos com raciocínio interno precisam de orçamento generoso ou
    # devolvem resposta vazia. Medido: 641 tokens de raciocínio para 203 de
    # resposta numa pergunta jurídica de quatro linhas.
    raciocina: bool = False
    min_tokens: int = 1024


MODELOS: dict[str, Modelo] = {
    # Perfis atualizados em 27/07/2026 com a bancada CASO-04 V7 (seis modelos,
    # a mesma peça real, julgamento cego por três famílias em dupla ordem).
    # Relatório: `bancada_cafelana_v7/RELATORIO_BANCADA_V7.md`.
    "opus-5": Modelo(
        id="opus-5", familia="anthropic", provedor="local", remoto=None,
        # Melhor arquitetura (9,03), escrita (8,55) e uso de autoridade (8,38)
        # da bancada. E o PIOR cumprimento de determinação entre as peças
        # completas (5,33): foi o único que se colocou acima de uma ordem do
        # titular, com a divergência registrada. Escreve melhor e obedece
        # menos — as duas coisas ao mesmo tempo, e as duas medidas.
        forte_em=("loops", "orquestracao", "agentes_paralelos", "regras_novas",
                  "arquitetura_da_peca", "escrita_forense"),
        fases=("F0", "F1", "F2A", "F3", "F4", "F6", "F7", "F9", "F10"),
    ),
    "fable-5": Modelo(
        id="fable-5", familia="anthropic", provedor="local", remoto=None,
        # Melhor cumprimento de determinação da bancada (8,22) e o mais
        # conservador com o texto de origem (preservou 83% dos trechos). É o
        # perfil que F7-B pede, porque ali mudar substância é o defeito, não a
        # virtude. Ponto fraco medido: uso de autoridade (6,47) — não deve ser
        # ele a decidir QUAIS precedentes entram.
        forte_em=("execucao_longa", "poucos_prompts", "fidelidade_ao_comando",
                  "edicao_incremental"),
        fases=("F7B",),
    ),
    # Sol pela assinatura (Codex CLI): custo zero marginal, mas só existe
    # dentro de uma sessão interativa — não serve para bancada nem para laço
    # automatizado.
    "sol-5.6": Modelo(
        id="sol-5.6", familia="openai", provedor="local", remoto=None,
        forte_em=("revisao_adversarial", "achar_erro_do_opus"),
        fases=("F7", "F7B"),
    ),
    # O mesmo modelo por HTTP. É o que permite medir o revisor na bancada e
    # usá-lo em revisão cruzada automatizada, sem depender do CLI.
    "sol-5.6-api": Modelo(
        id="sol-5.6-api", familia="openai", provedor="openrouter",
        remoto="openai/gpt-5.6-sol",
        forte_em=("revisao_adversarial", "achar_erro_do_opus"),
        fases=("F7", "F7B"),
        usd_entrada_por_milhao=5.0, usd_saida_por_milhao=30.0,
        raciocina=True, min_tokens=2048,
    ),
    "grok-4.5": Modelo(
        id="grok-4.5", familia="xai", provedor="openrouter",
        remoto="x-ai/grok-4.5",
        # O único juiz da bancada que se penalizou (−0,75 posições): elegeu peça
        # de família rival nas duas ordens e colocou a própria em 4º e 3º. Isso
        # é a qualidade que se quer de um revisor, e é rara. Como PRODUTOR, o
        # perfil é outro: os três juízes o flagraram afirmando placar de
        # julgamento e unanimidade sem lastro de folha — objeção ele faz bem,
        # afirmação de fato não.
        forte_em=("velocidade", "objecao_direta", "franqueza", "juiz_sem_autopreferencia"),
        fases=("F4", "F7"),
        usd_entrada_por_milhao=2.0, usd_saida_por_milhao=6.0,
    ),
    # Entrou no registro em 27/07/2026, pela bancada. É a alavanca de custo do
    # arranjo: US$ 0,11 contra US$ 0,61 do Sol na MESMA tarefa, em metade do
    # tempo, com nota determinística cheia e zero invenção. Os juízes o acharam
    # correto e menos cirúrgico (7,6–7,9 nos seis critérios) — perfil de
    # primeira passada e de trabalho de volume, não de peça final.
    "luna-5.6": Modelo(
        id="luna-5.6", familia="openai", provedor="openrouter",
        remoto="openai/gpt-5.6-luna",
        forte_em=("custo_baixo", "latencia_baixa", "primeira_passada", "volume"),
        fases=("F0", "F1", "F2A"),
        usd_entrada_por_milhao=1.0, usd_saida_por_milhao=6.0,
        raciocina=True, min_tokens=2048,
    ),
}

# Kimi K2 está fora por ordem expressa do titular (26/07/2026), não por preço.
MODELOS_PROIBIDOS = {"moonshotai/kimi-k2", "moonshotai/kimi-k2.5",
                     "moonshotai/kimi-k2.6", "moonshotai/kimi-k2.7-code",
                     "moonshotai/kimi-k2-thinking", "moonshotai/kimi-k2-0905"}

TETO_USD_POR_CHAMADA = 0.50
TETO_USD_POR_EXECUCAO = 3.00


def modelo_remoto_proibido(remoto: str | None) -> bool:
    """Bloqueia a família K2, inclusive IDs que ainda não existiam no registro.

    A lista explícita documenta os IDs conhecidos. O teste por família evita
    que um novo sufixo de K2 seja adicionado no futuro sem atualizar a lista.
    """
    valor = (remoto or "").strip().casefold().replace("_", "-")
    return (
        valor in {"k2", "kimi-k2"}
        or "kimi-k2" in valor
        or "/k2" in valor
    )


def _confirmar_modelo_reportado(modelo: Modelo, payload: dict) -> None:
    """Falha alto se um provedor declarar qualquer variante vedada de K2."""
    reportado = str(payload.get("model") or "").strip()
    if not reportado:
        return
    if modelo_remoto_proibido(reportado):
        raise ForjaModeloError(
            f"{modelo.id}: provedor reportou modelo vedado pela decisão do titular")


@dataclass
class Orcamento:
    """Contabilidade de uma execução. O teto é limite, não meta."""

    teto_usd: float = TETO_USD_POR_EXECUCAO
    gasto_usd: float = 0.0
    chamadas: list[dict] = field(default_factory=list)

    def restante(self) -> float:
        return max(0.0, self.teto_usd - self.gasto_usd)

    def registrar(self, recibo: dict) -> None:
        self.gasto_usd += float(recibo.get("custoUsd") or 0.0)
        self.chamadas.append(recibo)


def _segredo(nome: str) -> str:
    """Lê a chave do cofre privado. O valor nunca é registrado nem devolvido a log."""
    if os.environ.get(nome):
        return os.environ[nome]
    if not SECRETS.is_file():
        raise ForjaModeloError(f"cofre de segredos ausente; {nome} indisponível")
    for linha in SECRETS.read_text(encoding="utf-8", errors="replace").splitlines():
        if linha.startswith(f"{nome}="):
            valor = linha.split("=", 1)[1].strip()
            if valor:
                return valor
    raise ForjaModeloError(f"{nome} não consta do cofre de segredos")


def custo_usd(modelo: Modelo, entrada: int, saida: int) -> float:
    return (entrada * modelo.usd_entrada_por_milhao
            + saida * modelo.usd_saida_por_milhao) / 1_000_000


def _post(url: str, cabecalhos: dict, corpo: dict, timeout: int) -> dict:
    dados = json.dumps(corpo, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=dados, method="POST")
    for chave, valor in cabecalhos.items():
        req.add_header(chave, valor)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resposta:
            return json.loads(resposta.read().decode("utf-8"))
    except urllib.error.HTTPError as erro:
        detalhe = erro.read().decode("utf-8", "replace")[:400]
        raise ForjaModeloError(f"HTTP {erro.code} de {url.split('/')[2]}: {detalhe}") from None
    except OSError as erro:
        raise ForjaModeloError(f"falha de rede com {url.split('/')[2]}: {erro}") from None


def _openrouter(modelo: Modelo, prompt: str, sistema: str | None,
                max_tokens: int, timeout: int) -> tuple[str, int, int, int]:
    mensagens = ([{"role": "system", "content": sistema}] if sistema else []) + [
        {"role": "user", "content": prompt}]
    payload = _post(
        OPENROUTER_URL,
        {"Authorization": f"Bearer {_segredo('OPENROUTER_API_KEY')}",
         "Content-Type": "application/json"},
        {"model": modelo.remoto, "messages": mensagens, "max_tokens": max_tokens},
        timeout,
    )
    _confirmar_modelo_reportado(modelo, payload)
    escolha = (payload.get("choices") or [{}])[0]
    uso = payload.get("usage") or {}
    raciocinio = (uso.get("completion_tokens_details") or {}).get("reasoning_tokens") or 0
    return (
        str((escolha.get("message") or {}).get("content") or ""),
        int(uso.get("prompt_tokens") or 0),
        int(uso.get("completion_tokens") or 0),
        int(raciocinio),
    )


DESPACHO = {"openrouter": _openrouter}


def chamar(
    modelo_id: str,
    prompt: str,
    *,
    sistema: str | None = None,
    max_tokens: int = 2048,
    timeout: int = 300,
    fase: str | None = None,
    papel: str | None = None,
    orcamento: Orcamento | None = None,
    registrar: bool = True,
) -> dict:
    """Despacha um prompt e devolve o recibo da chamada.

    Levanta se: o modelo não está no registro, é proibido, roda localmente,
    estoura o teto ou devolve conteúdo vazio.
    """
    modelo = MODELOS.get(modelo_id)
    if modelo is None:
        raise ForjaModeloError(f"modelo fora do registro da FORJA: {modelo_id!r}")
    if modelo.remoto in MODELOS_PROIBIDOS or modelo_remoto_proibido(modelo.remoto):
        raise ForjaModeloError(f"{modelo_id}: modelo vedado por decisão do titular")
    if modelo.provedor == "local":
        raise ForjaModeloError(
            f"{modelo_id} roda pela assinatura do Claude Code ou pelo Codex, não por HTTP")

    # Orçamento generoso para quem raciocina: o teto baixo produz resposta
    # vazia, que é pior do que resposta cara.
    if modelo.raciocina:
        max_tokens = max(max_tokens, modelo.min_tokens)

    teto_chamada = custo_usd(modelo, len(prompt) // 3, max_tokens)
    if teto_chamada > TETO_USD_POR_CHAMADA:
        raise ForjaModeloError(
            f"{modelo_id}: custo máximo estimado US$ {teto_chamada:.2f} acima do teto "
            f"de US$ {TETO_USD_POR_CHAMADA:.2f} por chamada")
    if orcamento is not None and teto_chamada > orcamento.restante():
        raise ForjaModeloError(
            f"{modelo_id}: US$ {orcamento.restante():.2f} restantes não cobrem a chamada")

    inicio = time.monotonic()
    conteudo, entrada, saida, raciocinio = DESPACHO[modelo.provedor](
        modelo, prompt, sistema, max_tokens, timeout)
    decorrido = time.monotonic() - inicio

    if not conteudo.strip():
        raise ForjaModeloError(
            f"{modelo_id}: resposta sem conteúdo ({raciocinio} tokens de raciocínio, "
            f"{saida} de saída). Modelo que raciocina consome o orçamento pensando; "
            "aumente max_tokens em vez de tratar o vazio como resposta")

    recibo = {
        "modelo": modelo.id, "familia": modelo.familia, "provedor": modelo.provedor,
        "fase": fase, "papel": papel,
        "tokensEntrada": entrada, "tokensSaida": saida, "tokensRaciocinio": raciocinio,
        "custoUsd": round(custo_usd(modelo, entrada, saida), 6),
        "segundos": round(decorrido, 2),
        "conteudo": conteudo,
        "em": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
    }
    if orcamento is not None:
        orcamento.registrar(recibo)
    if registrar:
        registrar_no_ledger(recibo)
    return recibo


def registrar_no_ledger(recibo: dict) -> None:
    """Grava o recibo sem o texto — o ledger é de custo e proveniência, não de conteúdo."""
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    linha = {k: v for k, v in recibo.items() if k != "conteudo"}
    linha["caracteresResposta"] = len(recibo.get("conteudo") or "")
    with LEDGER.open("a", encoding="utf-8") as arquivo:
        arquivo.write(json.dumps(linha, ensure_ascii=False) + "\n")


def familia_de(modelo_id: str) -> str:
    modelo = MODELOS.get(modelo_id)
    if modelo is None:
        raise ForjaModeloError(f"modelo fora do registro: {modelo_id!r}")
    return modelo.familia


def revisores_de(modelo_id: str, *, fase: str | None = None) -> list[str]:
    """Modelos de outra família aptos a revisar o produtor.

    A revisão cruzada só vale se o revisor não compartilha a família do
    produtor — mesma família erra junto.
    """
    familia = familia_de(modelo_id)
    return sorted(
        outro.id for outro in MODELOS.values()
        if outro.familia != familia and (fase is None or fase in outro.fases)
    )


def modelos_da_fase(fase: str) -> list[str]:
    return sorted(m.id for m in MODELOS.values() if fase in m.fases)


def gasto_acumulado() -> dict:
    """Resumo do ledger — quanto cada modelo custou até agora."""
    if not LEDGER.is_file():
        return {"chamadas": 0, "usdTotal": 0.0, "porModelo": {}}
    total = 0.0
    por_modelo: dict[str, dict] = {}
    chamadas = 0
    for linha in LEDGER.read_text(encoding="utf-8").splitlines():
        if not linha.strip():
            continue
        try:
            item = json.loads(linha)
        except ValueError:
            continue
        chamadas += 1
        custo = float(item.get("custoUsd") or 0.0)
        total += custo
        alvo = por_modelo.setdefault(
            item.get("modelo") or "?", {"chamadas": 0, "usd": 0.0, "segundos": 0.0})
        alvo["chamadas"] += 1
        alvo["usd"] = round(alvo["usd"] + custo, 6)
        alvo["segundos"] = round(alvo["segundos"] + float(item.get("segundos") or 0.0), 2)
    return {"chamadas": chamadas, "usdTotal": round(total, 4), "porModelo": por_modelo}


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Despacho de modelos da FORJA")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("listar")
    sub.add_parser("gasto")
    p = sub.add_parser("chamar")
    p.add_argument("modelo")
    p.add_argument("prompt")
    p.add_argument("--max-tokens", type=int, default=2048)
    p.add_argument("--fase")
    p.add_argument("--papel")
    args = parser.parse_args()

    if args.cmd == "listar":
        for modelo in MODELOS.values():
            print(f"{modelo.id:10} {modelo.familia:10} {modelo.provedor:12} "
                  f"US$ {modelo.usd_entrada_por_milhao:>5.2f}/{modelo.usd_saida_por_milhao:>5.2f} por M  "
                  f"fases: {', '.join(modelo.fases)}")
    elif args.cmd == "gasto":
        print(json.dumps(gasto_acumulado(), ensure_ascii=False, indent=2))
    else:
        recibo = chamar(args.modelo, args.prompt, max_tokens=args.max_tokens,
                        fase=args.fase, papel=args.papel)
        print(f"[{recibo['modelo']} · {recibo['segundos']}s · US$ {recibo['custoUsd']:.4f}]\n")
        print(recibo["conteudo"])


if __name__ == "__main__":
    main()
