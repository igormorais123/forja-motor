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
import shutil
import subprocess
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

# Pasta vazia e dedicada onde o CLI do Cursor roda. Ele exige confiança no
# diretório de trabalho; confiar a pasta do caso daria ao agente externo a
# vizinhança dos autos, do ledger e dos artefatos. Aqui não há nada a explorar.
CURSOR_SANDBOX = FORJA / "cache" / "cursor_sandbox"


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
    # Restrições medidas, não presumidas. `nao_afirma_fato` marca modelo que
    # reprovou a bancada de fidelidade à fonte: ele pode dar ponto de vista, e
    # não pode ser origem de dispositivo, precedente, número ou data. A régua
    # está em `telemetria/bench_modelos/`, com a data da aferição.
    restricoes: tuple[str, ...] = ()


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
    # O MESMO Grok 4.5, pela assinatura do Cursor em vez do OpenRouter (ordem do
    # titular, 06/08/2026). Rota padrão do Diabob e da triagem rápida de F1.
    #
    # Custo declarado zero de propósito: não é grátis, é mensalidade — não há
    # preço por chamada a registrar, e inventar centavos mentiria no ledger. O
    # ledger continua contando as CHAMADAS, que é o que permite ver volume.
    #
    # Sem contagem de tokens: o CLI não a expõe. Preferimos zero declarado a
    # estimativa por caractere, porque número estimado em ledger vira número
    # citado depois. Quem precisar medir consumo usa a rota OpenRouter.
    # O ID no Cursor NÃO é `grok-4.5`: conferido em 07/08/2026 por
    # `cursor-agent --list-models`, ele expõe `cursor-grok-4.5-{low,medium,high}`
    # e as variantes `-fast`. Usamos `high` porque contraditório é onde se paga
    # por raciocínio, não por latência; a `-fast` fica para quem quiser trocar.
    "grok-4.5-cursor": Modelo(
        id="grok-4.5-cursor", familia="xai", provedor="cursor",
        remoto="cursor-grok-4.5-high",
        forte_em=("velocidade", "objecao_direta", "franqueza",
                  "juiz_sem_autopreferencia", "primeira_passada", "volume"),
        fases=("F1", "F4", "F7"),
        usd_entrada_por_milhao=0.0, usd_saida_por_milhao=0.0,
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
    # --- Vozes curtas do painel (07/08/2026, ordem do titular) ------------
    # Entram para dar PONTO DE VISTA em poucos tópicos, não para trabalhar.
    # A assinatura do Cursor já os paga; o custo real é atenção de quem lê, e
    # por isso o painel corta o tamanho da resposta no código, não no prompt.
    #
    # Kimi K3 saiu do registro em 26/07/2026 por reprovar a bancada jurídica, e
    # o titular decidiu em 07/08 não bani-lo. Ele volta com a restrição que a
    # medição justifica, e não com perdão: na bancada de 26/07 ele fez 2 de 6
    # corretas na condição cautelosa (2 invenções, 1 falha técnica) e **0 de 6
    # na condição solta, com 4 invenções**. O Grok, na mesma prova, fez 6 de 6
    # solto. Um modelo com esse perfil é útil como olhar e é perigoso como
    # fonte — daí `nao_afirma_fato`, que o painel transforma em instrução e em
    # veto de promoção enquanto a bancada disser isso.
    "kimi-k3-cursor": Modelo(
        id="kimi-k3-cursor", familia="moonshot", provedor="cursor",
        remoto="kimi-k3-high",
        forte_em=("ponto_de_vista_lateral", "parecer_curto", "leitura_de_tom"),
        fases=("F4", "F7"),
        usd_entrada_por_milhao=0.0, usd_saida_por_milhao=0.0,
        restricoes=("nao_afirma_fato",),
    ),
    # GLM 5.2 nunca passou pela bancada da casa. Isso NÃO é o mesmo que ter
    # reprovado, e os dois estados não podem colapsar num só: o K3 tem medida
    # ruim, o GLM não tem medida. Enquanto não tiver, ele fica no primeiro
    # degrau e a promoção é recusada por ausência de aferição, com esse motivo
    # escrito — nunca por presunção de que seja pior ou melhor.
    "glm-5.2-cursor": Modelo(
        id="glm-5.2-cursor", familia="zhipu", provedor="cursor",
        remoto="glm-5.2-high",
        forte_em=("ponto_de_vista_lateral", "parecer_curto", "sintese"),
        fases=("F4", "F7"),
        usd_entrada_por_milhao=0.0, usd_saida_por_milhao=0.0,
    ),
    # --- Vozes de comparação (07/08/2026, ordem do titular) ---------------
    # Entraram para dar régua ao painel: sem um modelo de ponta na mesma prova,
    # "o K3 tirou 75" é um número sem escala. Todas pela assinatura do Cursor,
    # no mesmo grau `high` das demais — comparação com esforço desigual mede o
    # esforço, não o modelo. A exceção é o Luna, que o titular pediu em `max`.
    #
    # ATENÇÃO ao Opus: ele é a MESMA família que escreve a peça e que revisa em
    # F7-B. No painel ele é **controle, não par**: serve para medir quanto uma
    # voz da própria casa acrescenta sobre as de fora, que é justamente o que a
    # Lição 99 diz não se poder presumir. Concordância dele com a análise
    # principal não é confirmação — é eco previsível.
    "opus-5-cursor": Modelo(
        id="opus-5-cursor", familia="anthropic", provedor="cursor",
        remoto="claude-opus-5-high",
        forte_em=("raciocinio_juridico", "parecer_curto", "controle_mesma_familia"),
        fases=("F4", "F7"),
        usd_entrada_por_milhao=0.0, usd_saida_por_milhao=0.0,
    ),
    # `gpt-5.6-luna-max` existe na assinatura do Cursor — conferido em
    # 07/08/2026 por `cursor-agent --list-models`. Isso importa: a rota que já
    # estava no registro (`luna-5.6`, OpenRouter) cobra US$ 1/6 por milhão, e a
    # ordem permanente da casa é preferir a assinatura. O `max` é pedido
    # expresso do titular, e é a única voz do painel fora do grau `high`.
    "luna-5.6-cursor": Modelo(
        id="luna-5.6-cursor", familia="openai", provedor="cursor",
        remoto="gpt-5.6-luna-max",
        forte_em=("custo_baixo", "primeira_passada", "parecer_curto", "volume"),
        fases=("F4", "F7"),
        usd_entrada_por_milhao=0.0, usd_saida_por_milhao=0.0,
    ),
}

# Kimi K2 está fora por ordem expressa do titular (26/07/2026), não por preço.
MODELOS_PROIBIDOS = {"moonshotai/kimi-k2", "moonshotai/kimi-k2.5",
                     "moonshotai/kimi-k2.6", "moonshotai/kimi-k2.7-code",
                     "moonshotai/kimi-k2-thinking", "moonshotai/kimi-k2-0905"}

# GPT-5.5 está fora por ordem expressa do titular (06/08/2026): a FORJA usa a
# geração 5.6, e o 5.5 não entra em hipótese nenhuma. Fica em conjunto próprio
# porque `MODELOS_PROIBIDOS` documenta a decisão sobre o K2, com regressão que
# afere isso — misturar as duas apagaria a razão de cada uma. A proibição pega
# em `modelo_remoto_proibido`, que é por onde `chamar` reprova as duas.
MODELOS_PROIBIDOS_GPT55 = {"gpt-5.5", "gpt-5.5-mini", "gpt-5.5-codex",
                           "openai/gpt-5.5", "openai/gpt-5.5-mini"}

# Quando a FORJA usa o Codex, o modelo é o gpt-5.6-luna no esforço máximo, por
# ordem do titular (06/08/2026). Vale para revisão cruzada, red team por família
# distinta e qualquer chamada da esteira — não para o que o Igor faz à mão fora
# dela. O `-c model_reasoning_effort="max"` faz parte da ordem, não é opcional.
CODEX_MODELO_FORJA = "gpt-5.6-luna"
CODEX_ESFORCO_FORJA = "max"

TETO_USD_POR_CHAMADA = 0.50
TETO_USD_POR_EXECUCAO = 3.00


def modelo_remoto_proibido(remoto: str | None) -> bool:
    """Bloqueia a família K2 e a geração GPT-5.5, inclusive IDs futuros.

    A lista explícita documenta os IDs conhecidos. O teste por família evita
    que um novo sufixo seja adicionado no futuro sem atualizar a lista.

    K2: ordem do titular de 26/07/2026, depois de reprovar a bancada jurídica.
    GPT-5.5: ordem do titular de 06/08/2026 — a FORJA usa a geração 5.6, e o
    5.5 não entra em hipótese nenhuma. O teste é por prefixo de versão para
    pegar `gpt-5.5-mini`, `gpt-5.5-codex` e o que mais vier com esse número.
    """
    valor = (remoto or "").strip().casefold().replace("_", "-")
    if valor in {"k2", "kimi-k2"} or "kimi-k2" in valor or "/k2" in valor:
        return True
    return "gpt-5.5" in valor


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


def _cursor_binario() -> Path:
    """Acha o `cursor-agent`. Ele não entra no PATH na instalação padrão do Windows."""
    override = os.environ.get("FORJA_CURSOR_AGENT")
    if override:
        caminho = Path(override)
        if caminho.is_file():
            return caminho
        raise ForjaModeloError(f"FORJA_CURSOR_AGENT aponta para arquivo inexistente: {override}")
    local = Path(os.environ.get("LOCALAPPDATA", "")) / "cursor-agent" / "cursor-agent.cmd"
    if local.is_file():
        return local
    achado = shutil.which("cursor-agent")
    if achado:
        return Path(achado)
    raise ForjaModeloError(
        "cursor-agent não encontrado. Instale o CLI do Cursor ou aponte FORJA_CURSOR_AGENT "
        "para o executável")


def _cursor_texto(bruto: str) -> str:
    """Extrai o texto da resposta, aceitando JSON, JSON por linha ou texto puro.

    O formato de saída do CLI muda entre versões. Preferir texto vazio a um
    parse otimista: `chamar` levanta em conteúdo vazio, e falhar alto é melhor
    do que devolver o log do agente como se fosse o parecer.
    """
    bruto = bruto.strip()
    if not bruto:
        return ""
    try:
        dados = json.loads(bruto)
    except json.JSONDecodeError:
        partes = []
        for linha in bruto.splitlines():
            linha = linha.strip()
            if not linha.startswith("{"):
                continue
            try:
                evento = json.loads(linha)
            except json.JSONDecodeError:
                continue
            for chave in ("text", "content", "delta", "result", "message"):
                valor = evento.get(chave)
                if isinstance(valor, str) and valor:
                    partes.append(valor)
                    break
        return "\n".join(partes) if partes else bruto
    if isinstance(dados, str):
        return dados
    if isinstance(dados, dict):
        for chave in ("result", "text", "content", "response", "output"):
            valor = dados.get(chave)
            if isinstance(valor, str) and valor.strip():
                return valor
        mensagens = dados.get("messages")
        if isinstance(mensagens, list):
            textos = [m.get("content") for m in mensagens
                      if isinstance(m, dict) and isinstance(m.get("content"), str)]
            if textos:
                return "\n".join(textos)
    return bruto


def _cursor(modelo: Modelo, prompt: str, sistema: str | None,
            max_tokens: int, timeout: int) -> tuple[str, int, int, int]:
    """Roda o modelo pela assinatura do Cursor, em modo somente leitura.

    Por que existe: o Grok 4.5 já estava no registro pelo OpenRouter, que cobra
    por chamada. O CLI do Cursor entrega o mesmo modelo pela assinatura que o
    titular já paga. O custo declarado aqui é zero — não porque seja grátis, mas
    porque não é medido por chamada; a mensalidade é o custo, e fingir centavos
    por chamada mentiria no ledger.

    `--mode ask` é obrigatório e não é detalhe: sem ele o agente do Cursor tem
    ferramenta de escrita e shell. Revisor externo não edita o caso.

    O CLI exige confiança no diretório de trabalho. Em vez de confiar a pasta do
    caso — que tem autos, ledger e artefatos —, ele roda numa **pasta vazia
    dedicada**. Nosso uso é texto que entra e texto que sai: o modelo não precisa
    de workspace nenhum, e pasta vazia não tem o que ser explorado. É por isso
    que `--trust` aqui é seguro e na pasta do caso não seria.
    """
    binario = _cursor_binario()
    completo = f"{sistema.strip()}\n\n{prompt}" if sistema else prompt
    # O prompt vai por STDIN, nunca por argumento. Medido em 07/08/2026: o
    # wrapper `.cmd` passa pelo cmd.exe, que corta o argumento na primeira
    # quebra de linha — o modelo respondia sobre a primeira linha e a resposta
    # PARECIA um parecer. Foi assim que o Diabob devolveu "você só me nomeou,
    # não há alvo" com o alvo dentro do prompt. Erro que não levanta exceção e
    # produz texto plausível é o pior tipo, e por isso há regressão para ele.
    comando = [str(binario), "--print", "--output-format", "json",
               "--mode", "ask", "--trust",
               "--model", modelo.remoto or modelo.id]
    CURSOR_SANDBOX.mkdir(parents=True, exist_ok=True)
    try:
        proc = subprocess.run(  # noqa: S603 - binário resolvido acima, sem shell
            comando, capture_output=True, text=True, encoding="utf-8",
            errors="replace", timeout=timeout, input=completo,
            cwd=str(CURSOR_SANDBOX),
        )
    except subprocess.TimeoutExpired:
        raise ForjaModeloError(
            f"{modelo.id}: cursor-agent excedeu {timeout}s sem responder") from None
    except OSError as erro:
        raise ForjaModeloError(f"{modelo.id}: falha ao executar cursor-agent: {erro}") from None

    saida_erro = (proc.stderr or "").strip()
    if proc.returncode != 0:
        if "Authentication required" in saida_erro or "auth" in saida_erro.casefold():
            raise ForjaModeloError(
                f"{modelo.id}: Cursor sem autenticação. Rode `cursor-agent login` no "
                "terminal, ou defina CURSOR_API_KEY. O login abre navegador e é do "
                "titular — nenhum agente faz por ele")
        raise ForjaModeloError(
            f"{modelo.id}: cursor-agent saiu com código {proc.returncode}: {saida_erro[:300]}")

    conteudo = _cursor_texto(proc.stdout or "")
    # O CLI não expõe contagem de tokens. Estimar por caracteres seria inventar
    # número no ledger — que é o defeito que este harness existe para não ter.
    return conteudo, 0, 0, 0


DESPACHO = {"openrouter": _openrouter, "cursor": _cursor}


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
