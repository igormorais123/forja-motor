# -*- coding: utf-8 -*-
"""forja_fronteira.py — o que é motor, o que é acervo, o que não sai desta máquina.

A FORJA vive em dois diretórios Git fisicamente separados no PC e uma zona
local que não é versionada:

    %USERPROFILE%\\repos\\forja-motor
    %USERPROFILE%\\repos\\forja-auditoria

O primeiro é um produto genérico, indistinguível de um motor que qualquer
escritório poderia clonar, usar e compartilhar. O segundo é o acervo privado
da instalação: informações do escritório, identidade visual, configuração,
casos, clientes e evidência operacional ficam ali. A separação física não é
apenas um filtro de publicação; os dois destinos são pastas e repositórios
independentes no disco:

    MOTOR    o sistema. Código, contratos, schemas, testes, templates, doutrina.
             Pode ser compartilhado com qualquer escritório. Não pode conter
             dados de cliente, dados pessoais, identidade ou configuração
             específica de uma banca.
    ACERVO   o que prova o que a esteira fez: `state/`, relatórios de execução,
             modelos aprovados, painel de gestão, histórico por caso e toda
             informação específica do escritório. Tem outro regime de acesso.
    LOCAL    o que não vai a repositório nenhum: os autos, o cofre pós-protocolo,
             caches e o que excede o limite de tamanho do GitHub.

Por que isto é código e não uma lista no README. A rotina de sincronização
carregava uma lista de quatro arquivos escrita à mão sob o nome `FORA_DO_MOTOR`.
Medido em 05/08/2026, o repositório do motor tinha **1.843 arquivos com sinal de
cliente**, entre eles 489 com número CNJ. A lista à mão não estava errada — estava
irrelevante diante do volume, que é a lição 87: recurso que depende de esforço
manual por caso não sobrevive ao volume.

O que este módulo detecta, e o que ele não detecta. Ele reprova por DOIS sinais:

  estrutural   número CNJ, CPF, CNPJ e inscrição na OAB. Sempre disponível, não
               depende de nada montado, e é o que pega o acidente típico de
               colar trecho de caso real dentro de um teste ou de um exemplo.
  nominal      nomes de cliente, lidos do registro que vive NO ACERVO. Exato,
               porém só disponível onde o acervo está montado.

O motor não guarda a lista de nomes, nem sequer o hash dela. Guardar hash
resolveria o gate funcionar sozinho, e foi considerado: um repositório que vai
ficar público com o sha256 de "<razão social do cliente>" é confirmável por
tentativa, e confirmação é o vazamento. Fora do acervo o gate roda em modo
`estrutural` e **diz que rodou assim** — degradar é permitido, silêncio não.

Ordem de classificação: a primeira regra que casa decide. As regras estão
escritas do mais específico para o mais geral, e cada uma carrega o motivo.

Uso:
    python forja_fronteira.py                     # gate: varre e conclui
    python forja_fronteira.py --classificar CAMINHO
    python forja_fronteira.py --raiz DIR --json saida.json
Saída: 0 quando o motor está limpo; 1 quando há violação.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

RAIZ_PADRAO = Path(__file__).resolve().parent.parent

MOTOR = "MOTOR"
ACERVO = "ACERVO"
LOCAL = "LOCAL"

# Registro de nomes protegidos. Vive no acervo justamente porque É dado de
# cliente: uma lista dos clientes do escritório é material sigiloso mesmo sem
# nenhum documento junto.
REGISTRO_NOMES = "_FORJA_HARNESS/state/FRONTEIRA_NOMES_PROTEGIDOS.json"

# GitHub recusa arquivo acima de 100 MB; a margem existe porque o limite vale
# para o objeto depois da compressão de transporte.
LIMITE_BYTES = 95 * 2**20

# --------------------------------------------------------------------------
# Sinais estruturais
# --------------------------------------------------------------------------
# CNJ: 0000000-00.0000.0.00.0000. É o identificador mais denso de dado de caso
# que existe — onde ele aparece, há processo real citado.
RE_CNJ = re.compile(r"\b\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}\b")
RE_CPF = re.compile(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b")
RE_CNPJ = re.compile(r"\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b")
# OAB exige a palavra por perto: "OAB/DF 12.345". Sem a âncora, o padrão casaria
# com qualquer número de quatro a seis dígitos e o gate viraria ruído.
RE_OAB = re.compile(r"\bOAB[/\s-]*[A-Z]{2}\s*n?º?\s*\d{2,3}\.?\d{3}\b", re.I)

# Formato da máscara aplicada por `forja_anonimizar.py`. Fica aqui, e não lá,
# porque quem precisa reconhecê-la é o gate: o anonimizador só a escreve.
RE_MASCARA_CNJ = re.compile(r"9\d{6}-00\.\d{4}\.\d\.\d{2}\.0000")
RE_MASCARA_OAB = re.compile(r"OAB[/\s-]*[A-Z]{2}\s*9\d\.\d{3}", re.I)

SINAIS_ESTRUTURAIS = (
    ("CNJ", RE_CNJ),
    ("CPF", RE_CPF),
    ("CNPJ", RE_CNPJ),
    ("OAB", RE_OAB),
)

# Extensões cujo conteúdo é lido em busca de sinal. Binário não é varrido: o
# gate não decodifica PDF nem DOCX, e mentir que varreu seria pior do que
# declarar que não varre. Binário no motor é barrado por regra de caminho.
TEXTO = {".md", ".py", ".json", ".txt", ".html", ".htm", ".yml", ".yaml",
         ".jsonl", ".csv", ".ps1", ".js", ".css", ".tex", ".svg", ".xml",
         ".ini", ".cfg", ".toml", ".sh", ".bat", ""}

# --------------------------------------------------------------------------
# Regras de classificação — a primeira que casa decide
# --------------------------------------------------------------------------
# Cada regra é (prefixo_ou_marca, destino, motivo). `marca` casa em qualquer
# posição do caminho; `prefixo` casa no começo. Prefixos vêm com "/" ao final
# para não confundir `state` com `state_novo`.

# LOCAL — não vai a repositório nenhum.
_LOCAL_MARCAS = [
    ("_FORJA_HARNESS/private/", "área privada local: nunca sai desta máquina"),
    ("private/post_protocol/", "cofre pós-protocolo: retorno humano da peça protocolada"),
    ("PEÇA PROTOCOLADA — ", "cofre pós-protocolo: a peça efetivamente protocolada"),
    ("VERSÃO HUMANA FINAL — ", "cofre pós-protocolo: versão humana final"),
    ("reports/POST_PROTOCOL_LAST_RUN.json", "cofre pós-protocolo: índice da última conferência"),
    ("__pycache__/", "cache do interpretador"),
    (".pytest_cache/", "cache de execução de teste"),
    (".ruff_cache/", "cache do linter"),
    (".mypy_cache/", "cache do verificador de tipo"),
    (".playwright-mcp/", "sobra de sessão de navegador"),
    (".playwright-cli/", "sobra de sessão de navegador"),
    ("node_modules/", "dependência instalável"),
    (".venv/", "ambiente virtual"),
    (".git/", "banco do próprio git"),
    ("telemetria/", "telemetria de execução, regenerável e volumosa"),
    ("graphify-out/", "saída gerada do grafo, regenerável"),
    ("_FERRAMENTAS/.autoresearch/", "bancada de experimento visual: saída regenerável, com peça real dentro"),
    ("00_IA_NAVIGACAO/dados/", "índice gerado que enumera as pastas de caso"),
    ("00_IA_NAVIGACAO/logs/", "log do observador"),
    ("00_IA_NAVIGACAO/INDICE_GERAL_IA.md", "índice gerado que enumera as pastas de caso"),
    ("MAPA_IA.md", "mapa gerado por pasta, reescrito a cada varredura"),
    (".bak-doctorplus-", "backup automático de editor"),
    ("_FORJA_HARNESS/cache/raw/", "captura bruta de página, refazível pela URL"),
    ("_FORJA_HARNESS/debug_contagem.py", "script de depuração apontando para um caso"),
    ("_FERRAMENTAS/organizar_pedidos_email.py",
     "script de uma vez só: mapeia e-mails a pastas de caso de julho de 2026"),
    ("_FORJA_HARNESS/youtube-transcript/", "transcrição de vídeo, alheia ao sistema"),
    ("_FORJA_HARNESS/telemetria", "telemetria de execução"),
    # Mapas gerados por varredura da árvore inteira: enumeram as pastas de caso
    # por construção, e são refeitos a cada rodada do gerador.
    ("ARCHIFY_ARQUITETURA.md", "mapa de arquitetura gerado por varredura"),
    ("GRAPHIFY_GRAFO.md", "grafo gerado por varredura"),
    (".claude/scheduled_tasks.lock", "trava de execução do agendador"),
    (".claude/settings.local.json", "preferência local de máquina"),
    ("scheduled_tasks.lock", "trava de execução"),
    (".autoresearch/", "bancada de experimento do ciclo AR, regenerável"),
    (".planning/", "planejamento de sessão de agente"),
    ("_ocr_", "OCR intermediário de autos, refazível a partir do PDF"),
    ("_CONFERENCIA_", "conferência pontual, datada"),
    ("_CORRECOES_", "correções propostas numa data"),
    ("_LABORATÓRIO_", "laboratório experimental, declaradamente não é prova"),
    ("FRONTEIRA_DO_DISCO.md", "este mapa, reescrito a cada varredura"),
]

# Binário que o motor legitimamente carrega. O gate não lê binário, então cada
# um destes é uma promessa de que alguém olhou. Fora desta lista, binário no
# motor é violação — é onde dado de cliente passaria sem ser lido.
_BINARIO_DECLARADO = [
    ("_FERRAMENTAS/TEMPLATE_MEDINA_OSORIO_PETICAO.docx",
     "o timbre é arte vetorial no cabeçalho e é irreproduzível por código"),
    ("_FERRAMENTAS/assets/", "identidade visual da casa: logo e marca"),
    ("gestao_escritorio/assets/", "logo do painel"),
    ("_FORJA_HARNESS/cache/RITJDFT_ER36.pdf", "emenda regimental oficial, capturada verbatim"),
    ("_FORJA_HARNESS/cache/fontes_oficiais/", "fonte oficial capturada verbatim"),
    ("_FORJA_HARNESS/cache/test_injection_veneno.pdf",
     "PDF de fixture da regressão de injeção indireta"),
    ("_FORJA_HARNESS/exports/gpt-forja/assets/",
     "arte de capa do pacote GPT: bigorna e documento na paleta da casa, sem "
     "nome, marca ou logo de escritório — aberta e conferida em 09/08/2026"),
]

# ACERVO — prova do que a esteira fez. Carrega cliente por natureza.
_ACERVO_PREFIXOS = [
    ("_FORJA_HARNESS/state/", "a cadeia de auditoria por caso"),
    ("_FORJA_HARNESS/reports/", "relatório de execução sobre caso real; `reports/` é destino de escrita de 12 módulos, não fonte do motor"),
    ("_FORJA_HARNESS/autoresearch/ciclos/", "execução do ciclo AR sobre peça real"),
    ("_FORJA_HARNESS/autoresearch/evolucao/", "variantes geradas a partir de peça real"),
    ("_FORJA_HARNESS/autoresearch/candidates/", "candidatas geradas a partir de peça real"),
    ("_FORJA_HARNESS/autoresearch/cache/", "corpus derivado do acervo"),
    ("_FORJA_HARNESS/bancada_cafelana_v7/", "bancada cega construída sobre um caso nominado"),
    ("_FORJA_HARNESS/_scripts_oneoff/", "script de uma vez só, amarrado a um caso"),
    ("_FORJA_HARNESS/00_MAPA_ARQUITETURA_IA/", "mapa gerado que indexa as pastas de caso"),
    ("_FORJA_HARNESS/.planning/", "planejamento de sessão com nome de caso"),
    ("_FORJA_HARNESS/PETICAO_", "peça montada dentro da pasta do motor"),
    ("_FORJA_HARNESS/FORJA/", "sobra de execução"),
    ("_MODELOS/", "peça-modelo aprovada, com texto de cliente"),
    ("gestao_escritorio/data/", "demandas do escritório"),
    ("gestao_escritorio/logs/", "log da fila com nome de cliente"),
    ("gestao_escritorio/entregas_fabio_osorio/", "entregas ao titular"),
    ("gestao_escritorio/hermes_prompts/", "prompts com contexto de demanda real"),
    # Os canários do ciclo AR marcados `_real` são derivados de uma peça
    # protocolada e trazem nome e inscrição na OAB verdadeiros. O manifesto
    # deles fica no motor, preso por hash na régua; o conteúdo, não.
    ("_FORJA_HARNESS/autoresearch/canarios/", "canário derivado de peça real"),
    ("_FORJA_HARNESS/autoresearch/AR_CORPUS.json", "corpus indexando casos reais"),
    ("_FORJA_HARNESS/autoresearch/AR_PANEL.json", "painel do ciclo sobre casos reais"),
    ("_FORJA_HARNESS/autoresearch/AR_LOG.jsonl", "log de execução do ciclo"),
    ("_FORJA_HARNESS/cache/DIFF_", "diff de peça real gerado em teste"),
    # Capturas anotadas com análise do caso. Não são fonte oficial: o texto foi
    # comentado com o nome da operadora e do beneficiário, o que além de ser
    # dado de cliente destrói a razão de a pasta existir, que é guardar o
    # dispositivo verbatim para conferência antes de citar.
    ("_FORJA_HARNESS/cache/fontes_oficiais/README_PESQUISA_", "captura anotada com análise do caso"),
    ("_FORJA_HARNESS/cache/fontes_oficiais/SINTESE_ACHADOS_", "síntese de pesquisa sobre caso real"),
    ("_FORJA_HARNESS/cache/fontes_oficiais/STATUS_CAPTURAS_", "diário de captura de um caso"),
]
_ACERVO_MARCAS = [
    ("PAINEL_ESCRITORIO_MEDINA_OSORIO.html", "painel renderizado com nome de cliente"),
    ("painel_gestao_escritorio.html", "painel renderizado com nome de cliente"),
]

# MOTOR — exceções que moram dentro de pasta classificada como acervo, e
# portanto precisam vir ANTES dela na ordem. Cada uma existe porque o código do
# motor depende do arquivo.
_MOTOR_EXCECOES = [
    ("_FORJA_HARNESS/autoresearch/AR_MANIFEST.json", "protegido por hash na régua"),
    ("_FORJA_HARNESS/autoresearch/canarios/CANARIOS_MANIFEST.json", "protegido por hash na régua"),
    ("_FORJA_HARNESS/autoresearch/prompts/", "prompt do ciclo AR, protegido por hash na régua"),
    ("_FORJA_HARNESS/_scripts_oneoff/validate_f7_integration.py", "chamado por validate_forja_n3.py e por test_forja_reconcile.py"),
    ("_FORJA_HARNESS/_scripts_oneoff/LEIA-ME.md", "explica a pasta"),
    ("_FORJA_HARNESS/autoresearch/canarios/CANARIOS_MANIFEST.json", "protegido por hash na régua"),
    ("_FORJA_HARNESS/autoresearch/canarios/exemplo_placeholder/",
     "canário sintético de demonstração: não deriva de peça real"),
]

# Script de uma vez só amarrado a um caso, dentro da pasta de código do painel.
# São registro do que foi feito, não biblioteca: nenhum outro módulo os importa.
_PREFIXOS_ONEOFF_PAINEL = ("registrar_", "apply_", "preencher_", "seed_",
                           "indexar_", "hermes_reconcile_")

# Data no fim do nome do script: `corrigir_rota_<cliente>_20260805.py`. A lista
# de prefixos acima é a lição 217 em miniatura — ela não previu `corrigir_`, e o
# script novo chegou ao motor com número CNJ e razão social dentro. A data
# resolve por construção: medido em 05/08/2026, os 19 scripts datados da pasta
# são todos de uma vez só, e nenhuma das bibliotecas do painel — `server.py`,
# `office_io.py`, `render_dashboard.py` — carrega data no nome.
RE_SCRIPT_DATADO = re.compile(r"_(\d{8}|\d{4}-\d{2}-\d{2})(_[a-z]+)?\.py$", re.I)

# Arquivo com data no nome é registro de um momento, não doutrina. A regra é
# geral de propósito: uma lista dos 40 relatórios que hoje estão na raiz do
# motor estaria desatualizada no próximo relatório escrito.
RE_DATADO = re.compile(r"_\d{4}-\d{2}(-\d{2})?(_\d{3,4})?\.(md|json|html|txt)$", re.I)

# Famílias de nome que são registro de execução mesmo sem data. Cada prefixo
# nomeia um gênero de artefato produzido POR uma rodada, não consumido por ela.
_PREFIXOS_REGISTRO = (
    "ANALISE_", "AUDITORIA_", "APRENDIZADOS_CONSELHO", "CIRURGIA_", "CONSELHO_",
    "DIAGNOSTICO_", "DIVERGENCIA_", "GOVERNANCA_", "INCIDENTE_", "LACUNA_",
    "LAPIDACAO_", "MEMORIAL_", "O_QUE_DEPENDE_", "RELATORIO_", "TRIAGEM_",
    "VARREDURA_", "F8_PRIMEIRA", "F8S_ANTI",
)

# Saída de execução na raiz do motor: regenerável, e por isso não pertence a
# repositório nenhum.
_SAIDA_SOLTA = {
    "adocao_resultado.json", "mutation_results_temp.json",
    "mutation_aperfeicoada.json", "varredura_output.json",
    "painel_fila_qa.png", "qa_forja_fila_secao.png",
    "test_forja_injection_output.txt",
}

# Pastas do acervo processual: os autos. Não são nem motor nem acervo de
# auditoria — são o material do cliente, e a origem deles é o e-mail.
_RAIZ_MOTOR = {
    "_FORJA_HARNESS", "_FERRAMENTAS", "git-tools", "_LEIS_GERAIS",
    "00_IA_NAVIGACAO", "gestao_escritorio", ".claude", ".agents", ".codex",
}
_RAIZ_ACERVO = {"_MODELOS"}

ARQUIVOS_RAIZ_MOTOR = {
    "CLAUDE.md", "AGENTS.md", "APRENDIZADOS_FEEDBACK_HUMANO.md",
    "PROTOCOLO_TRATAMENTO_E_CITACAO_ACERVO_PROCESSUAL.md",
    "PROTOCOLO_FECHAMENTO_MULTICANAL_WHATSAPP_EMAIL.md",
    "PROMPT-FABRICA-MELHORIA-PETICAO.md", "FAILURE_TAXONOMY.md",
    "QUALITY_BOARD.md", "ARCHIFY_ARQUITETURA.md", "GRAPHIFY_GRAFO.md",
    "ATUALIZAR_MAPA_IA.ps1", "INICIAR_MAPA_IA_VIVO.ps1",
    "MOTOR_DISTRIBUICAO.md",
    ".graphifyignore", "README.md",
}
# `.gitignore` e `.gitattributes` pertencem ao repositório em que estão, e não ao
# motor: o da pasta de trabalho lista caminhos de pasta de caso, e cada
# repositório publicado tem o seu próprio, escrito para o que ele guarda.
ARQUIVOS_RAIZ_ACERVO = {
    "GITHUB_BACKUP_README.md",
    "ENTREGAS_FABIO_OSORIO.md", "CONTROLE_AUTOS_COMPLETOS_2026-07-19.md",
    "RELATORIO_SISTEMA_GESTAO_ESCRITORIO.md",
    "AUDITORIA_ORGANIZACAO_EMAILS_MEDINA_OSORIO_2026-07-07.md",
    "RELATORIO_ORGANIZACAO_EMAILS_MEDINA_OSORIO.md",
}


def _normalizar_sep(caminho: str) -> str:
    """Normaliza separador e tira o prefixo `./`, sem tocar em arquivo oculto.

    `lstrip("./")` parece resolver e não resolve: ele remove QUALQUER ponto ou
    barra do começo, então `.gitignore` virava `gitignore` e `.claude/` virava
    `claude/`. O efeito era silencioso e caro — as pastas de instrução de agente
    `.claude`, `.agents` e `.codex` caíam em LOCAL e simplesmente não eram
    publicadas, sem nada reprovar.
    """
    rel = caminho.replace("\\", "/")
    while rel.startswith("./"):
        rel = rel[2:]
    return rel.lstrip("/")


def classificar(caminho_rel: str) -> tuple[str, str]:
    """Classifica um caminho relativo à pasta de trabalho.

    Devolve (destino, motivo). A primeira regra que casa decide, e a ordem aqui
    é deliberada: exceções do motor vêm antes das pastas de acervo que as
    contêm, e o cofre vem antes de tudo.
    """
    rel = _normalizar_sep(caminho_rel)

    for marca, motivo in _LOCAL_MARCAS:
        if marca in rel:
            return LOCAL, motivo

    for prefixo, motivo in _MOTOR_EXCECOES:
        if rel == prefixo or rel.startswith(prefixo):
            return MOTOR, motivo

    nome_arq = rel.split("/")[-1]
    if rel.startswith("_FORJA_HARNESS/") and rel.count("/") == 1:
        if nome_arq in _SAIDA_SOLTA:
            return LOCAL, "saída de execução regenerável, solta na raiz do motor"
        if RE_DATADO.search(nome_arq) or nome_arq.startswith(_PREFIXOS_REGISTRO):
            return ACERVO, "registro de uma execução, não doutrina do sistema"

    if rel.startswith("gestao_escritorio/scripts/"):
        nome = rel.split("/")[-1]
        if RE_SCRIPT_DATADO.search(nome):
            return ACERVO, ("script com data no nome: registro de um dia, não "
                            "biblioteca do painel")
        if nome.startswith(_PREFIXOS_ONEOFF_PAINEL):
            return ACERVO, ("script de uma vez só amarrado a um caso; nenhum "
                            "módulo o importa")

    for prefixo, motivo in _ACERVO_PREFIXOS:
        if rel.startswith(prefixo):
            return ACERVO, motivo
    for marca, motivo in _ACERVO_MARCAS:
        if marca in rel:
            return ACERVO, motivo

    topo = rel.split("/")[0]
    if "/" not in rel:
        if rel in ARQUIVOS_RAIZ_MOTOR:
            return MOTOR, "doutrina de operação na raiz"
        if rel in ARQUIVOS_RAIZ_ACERVO:
            return ACERVO, "registro do escritório na raiz"
        return LOCAL, "arquivo solto na raiz, não declarado em nenhum dos dois"
    if topo in _RAIZ_MOTOR:
        return MOTOR, "pasta do sistema"
    if topo in _RAIZ_ACERVO:
        return ACERVO, "pasta de acervo de auditoria"
    # Dentro de pasta de caso, o texto de trabalho vai ao acervo e o resto fica.
    # A separação é por extensão porque é a única que distingue os dois sem
    # depender de alguém declarar caso a caso: o markdown é o que a esteira e o
    # advogado escrevem — análise, cronologia, minuta, relatório de melhorias —
    # e some junto com a máquina se não for versionado. PDF de autos, DOCX
    # protocolado, áudio e imagem digitalizada são o material recebido: pesam
    # os 16 GB que quebraram o repositório único e são recuperáveis do e-mail e
    # do próprio processo. O acervo é privado justamente para poder carregar o
    # nome do cliente que estes arquivos trazem.
    if rel.lower().endswith(".md"):
        return ACERVO, ("documento de trabalho do processo: o markdown vai ao "
                        "acervo privado; binário dos autos fica no disco")
    # Catch-all deliberadamente conservador: o que não foi declarado fica LOCAL.
    # O motivo precisa dizer isso, e não inventar explicação — a primeira versão
    # chamava `docs/` de "pasta de caso", e um mapa gerado que erra o motivo
    # mente com aparência de autoridade.
    return LOCAL, ("não declarado em nenhum dos dois lados; na dúvida fica nesta "
                   "máquina — as pastas de caso caem aqui por serem a maioria")


# --------------------------------------------------------------------------
# Detecção de sinal de cliente
# --------------------------------------------------------------------------
def _dobrar(texto: str) -> str:
    """Minúsculas sem acento, para casar nome escrito de formas diferentes."""
    sem = unicodedata.normalize("NFKD", texto)
    sem = "".join(c for c in sem if not unicodedata.combining(c))
    return sem.lower()


def carregar_nomes(raiz: Path) -> tuple[list[str], str]:
    """Lê o registro de nomes protegidos do acervo.

    Devolve (nomes, modo). `modo` é `nominal` quando o registro foi encontrado e
    `estrutural` quando não — e quem chama precisa dizer isso no relatório, para
    que "passou" não signifique coisas diferentes em execuções diferentes.
    """
    registro = raiz / REGISTRO_NOMES
    if not registro.exists():
        return [], "estrutural"
    try:
        dados = json.loads(registro.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return [], "estrutural"
    # Os nomes vão para a frente na grafia original: o casamento de nome
    # ambíguo depende da maiúscula, e dobrar aqui a destruiria.
    nomes = sorted({str(n).strip() for n in (dados.get("nomes") or [])
                    if len(str(n).strip()) >= 4})
    if not nomes:
        return [], "estrutural"
    # A lista de nomes ambíguos também é curadoria de cliente e vem do acervo.
    # Ela é global porque `_padrao_de_nome` decide grafia exata sem receber a
    # raiz; carregá-la aqui garante que quem tem os nomes tem a curadoria junto.
    global _NOMES_AMBIGUOS
    _NOMES_AMBIGUOS = carregar_curadoria(raiz)[2]
    return nomes, "nominal"


# Nomes que também são palavra do vocabulário comum ou jurídico exigem grafia
# exata: "produto in natura" no CDC não é o cliente de mesmo nome, e reprovar a
# captura do art. 12 por causa disso ensina a ignorar o gate. A lista vem do
# acervo, com o resto da curadoria.
_NOMES_AMBIGUOS: set[str] = set()


def e_sintetico(valor: str) -> bool:
    """O número é obviamente inventado?

    Fixture e canário de demonstração usam `0000000-00.0000.0.00.0000`,
    `1234567-89...` e `OAB/DF 12345` de propósito, para que quem lê saiba de
    imediato que não é um processo de verdade. Acusar esses valores treinaria
    a casa a ignorar o gate justamente onde ele deve ser levado a sério.
    """
    # A máscara da casa, emitida por `forja_anonimizar.py`: sequencial na faixa
    # 9xxxxxx, dígito verificador 00 e unidade de origem 0000, preservando ano,
    # segmento e tribunal. Sem reconhecê-la o gate acusa o próprio remédio, e
    # cada rodada de anonimização produziria uma nova safra de violações.
    if RE_MASCARA_CNJ.fullmatch(valor) or RE_MASCARA_OAB.fullmatch(valor):
        return True

    grupos = re.findall(r"\d+", valor)
    if not grupos:
        return False

    def _marcado(d: str) -> bool:
        if len(d) < 5:
            return False
        if len(set(d)) <= 1:                       # 0000000
            return True
        return all((int(b) - int(a)) % 10 == 1     # 1234567
                   for a, b in zip(d, d[1:]))

    # No CNJ o que identifica é o primeiro grupo, o número sequencial; o resto
    # é dígito verificador, ano, segmento e órgão, e testar a concatenação
    # inteira nunca acusaria `1234567-89.2020.8.26.0100`.
    return _marcado(grupos[0]) or _marcado("".join(grupos))


def _padrao_de_nome(nome: str) -> re.Pattern:
    """Regex de palavra inteira para um nome, tolerante a espaço variável.

    A busca por substring encontrou "natura" dentro de "natureza" e reprovou
    quatro capturas de resolução da ANS que não têm nada de cliente. Fronteira
    que grita onde não há problema é fronteira que alguém desliga.
    """
    base = nome if _e_ambiguo(nome) else _dobrar(nome)
    partes = [re.escape(p) for p in base.split()]
    return re.compile(r"\b" + r"[\s\-]+".join(partes) + r"\b")


def sinais_no_texto(texto: str, nomes: list[str],
                    padroes: dict[str, re.Pattern] | None = None) -> list[str]:
    """Sinais de dado de cliente encontrados. Lista ordenada e sem repetição."""
    achados: set[str] = set()
    for rotulo, padrao in SINAIS_ESTRUTURAIS:
        for m in padrao.findall(texto):
            valor = m if isinstance(m, str) else m[0]
            if e_sintetico(valor):
                continue
            achados.add(f"{rotulo}:{valor}")
    if nomes:
        dobrado = _dobrar(texto)
        padroes = padroes if padroes is not None else {
            n: _padrao_de_nome(n) for n in nomes}
        for nome in nomes:
            alvo = texto if _e_ambiguo(nome) else dobrado
            if padroes[nome].search(alvo):
                achados.add(f"NOME:{nome}")
    return sorted(achados)


def _e_ambiguo(nome: str) -> bool:
    """Nome de uma palavra só que também é palavra comum."""
    return " " not in nome and _dobrar(nome) in _NOMES_AMBIGUOS


def _binario_declarado(rel: str) -> bool:
    return any(rel == marca or rel.startswith(marca)
               for marca, _ in _BINARIO_DECLARADO)


def varrer(raiz: Path, incluir_local: bool = False) -> dict:
    """Varre a pasta de trabalho e devolve o laudo da fronteira."""
    nomes, modo = carregar_nomes(raiz)
    padroes = {n: _padrao_de_nome(n) for n in nomes}
    violacoes: list[dict] = []
    contagem = {MOTOR: 0, ACERVO: 0, LOCAL: 0}
    grandes: list[dict] = []

    for p in sorted(raiz.rglob("*")):
        if not p.is_file():
            continue
        try:
            rel = p.relative_to(raiz).as_posix()
        except ValueError:
            continue
        destino, motivo = classificar(rel)
        contagem[destino] += 1
        if destino != MOTOR:
            if not incluir_local:
                continue
        try:
            tamanho = p.stat().st_size
        except OSError:
            continue
        if destino in (MOTOR, ACERVO) and tamanho > LIMITE_BYTES:
            grandes.append({"caminho": rel, "bytes": tamanho, "destino": destino})
        if destino != MOTOR:
            continue
        if p.suffix.lower() not in TEXTO:
            if not _binario_declarado(rel):
                violacoes.append({"caminho": rel, "motivo": motivo,
                                  "sinais": ["BINARIO:" + (p.suffix or "sem extensão")],
                                  "classe": "binario_nao_declarado"})
            continue
        try:
            texto = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        sinais = sinais_no_texto(texto, nomes, padroes)
        if sinais:
            violacoes.append({"caminho": rel, "motivo": motivo,
                              "sinais": sinais[:12],
                              "total_sinais": len(sinais),
                              "classe": "sinal_de_cliente"})

    return {
        "modo": modo,
        "nomesProtegidos": len(nomes),
        "contagem": contagem,
        "violacoes": violacoes,
        "arquivosGrandes": grandes,
        "aprovado": not violacoes and not grandes,
    }


# --------------------------------------------------------------------------
# Geração do registro de nomes
# --------------------------------------------------------------------------
# Palavras que aparecem no campo `clienteOuCaso` e nos nomes de pasta sem serem
# nome de ninguém. Sem esta lista o registro passa a conter "memoriais" e
# "parecer", e o gate reprova metade do motor por falar de si mesmo.
_RUIDO = {
    "e", "de", "da", "do", "dos", "das", "em", "no", "na", "ao", "à", "para",
    "com", "por", "sobre", "outros", "outras", "ltda", "sa", "s", "a", "me",
    "epp", "eireli", "prazo", "urgente", "fwd", "re", "peticao", "petição",
    "memoriais", "memorial", "parecer", "quesitos", "minuta", "elaboracao",
    "elaboração", "embargos", "declaracao", "declaração", "agravo", "recurso",
    "especial", "interno", "instrumento", "apelacao", "apelação", "contrarrazoes",
    "contrarrazões", "acao", "ação", "improbidade", "administrativa", "cautelar",
    "fiscal", "medida", "processo", "proc", "analise", "análise", "caso",
    "pessoal", "plano", "saude", "saúde", "proposta", "servicos", "serviços",
    "juridicos", "jurídicos", "contrato", "social", "documentos", "dados",
    "material", "conteudo", "conteúdo", "relatorio", "relatório", "auditoria",
    "consulta", "tecnico", "técnico", "pericial", "contabil", "contábil",
    "atualizacao", "atualização", "valores", "laudo", "assunto", "julgamento",
    "estrategico", "estratégico", "ajustes", "finais", "nos", "interessado",
    "confidencial", "estritamente", "solicita", "informacoes", "informações",
    "apresenta", "esclarecimentos", "complementacao", "complementação",
    "versao", "versão", "preliminar", "novos", "produtos", "fases", "autonomas",
    "autônomas", "diretrizes", "conclusao", "conclusão", "matriz", "prova",
    "requerimento", "rastreamento", "integral", "processos", "relacionados",
    "mapeamento", "nacional", "coletivas", "envolvendo", "milhoes", "milhões",
    "whatsapp", "audio", "áudio", "triagem", "demandas", "contexto",
    "organizacao", "organização", "nova", "pasta", "comprovantes", "pagamento",
    "jul", "revisao", "revisão", "precedentes", "correcao", "correção",
    "objeto", "dossie", "dossiê", "interno", "decisao", "decisão", "evento",
    "reflexoes", "reflexões", "arquitetura", "taxonomia", "capacitacao",
    "capacitação", "agentes", "estudo", "interacao", "interação", "peças",
    "pecas", "julho", "agosto", "setembro", "outubro", "planejamento",
    "detalhado", "consolidada", "confidencialidade", "assinatura", "entrada",
    "acesso", "encaminhado", "cliente", "senador", "próximos", "proximos",
    "passos", "implementados", "linha", "hermeneutica", "hermenêutica",
    "escolhas", "fundamentacao", "fundamentação", "historico", "histórico",
    "intempestividade", "originario", "originário", "uniao", "união",
    "concluido", "concluído", "solicitacao", "solicitação", "elaboração",
}
_MIN_NOME = 5

# Siglas de recurso, tribunal e unidade da federação. Elas sobrevivem à limpeza
# porque são maiúsculas e curtas, e sem esta lista o registro passa a proteger
# "AgInt AREsp", que aparece em toda a doutrina do motor.
_SIGLAS = {
    "agint", "aresp", "earesp", "edcl", "eds", "ed", "ai", "resp", "re", "are",
    "ediv", "trf", "trf1", "trf2", "trf3", "trf4", "trf5", "jfrj", "jfrs",
    "stj", "stf", "tjto", "tjrj", "tjrs", "tst", "tse", "cnj", "oab", "mpf",
    "ac", "al", "ap", "am", "ba", "ce", "df", "es", "go", "ma", "mt", "ms",
    "mg", "pa", "pb", "pr", "pe", "pi", "rj", "rn", "rs", "ro", "rr", "sc",
    "sp", "se", "to", "ia", "ppt", "pdf", "docx", "html",
}

# A firma não entra no registro de nomes de clientes. Ela não é cliente, e
# protegê-la como se fosse nome de caso faria o gate reprovar vocabulário do
# próprio motor. Isso não autoriza identidade visual de uma banca no produto
# genérico: marca, logo e configuração específicas pertencem ao acervo privado
# e são uma regra de distribuição, não de anonimização de clientes.
_FIRMA = {"medina", "osorio", "osório", "advogados", "inteia"}


def _limpar_nome(bruto: str) -> str:
    """Tira ruído de borda de um nome extraído de título de e-mail ou pasta."""
    s = re.sub(r"\bn?º?\s*[\d.\-/]{6,}\b", " ", bruto)   # números de processo
    s = re.sub(r"[^0-9A-Za-zÀ-ÿ\s&]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    palavras = [p for p in s.split()
                if _dobrar(p) not in _RUIDO
                and _dobrar(p) not in _SIGLAS
                and _dobrar(p) not in _FIRMA
                and len(p) > 1
                and not p.isdigit()]
    return " ".join(palavras).strip()


def _e_nome_plausivel(candidato: str) -> bool:
    """Um nome de pessoa ou empresa tem ao menos uma palavra própria.

    Sem esta exigência o registro recebe fragmento de nome de pasta truncado
    ("onomia", "refle") e substantivo comum em minúscula ("honorários",
    "réplica"), que casariam dentro da doutrina do motor e fariam o gate
    reprovar o sistema por ele falar de si mesmo.
    """
    if len(candidato) < _MIN_NOME:
        return False
    for token in candidato.split():
        letras = [c for c in token if c.isalpha()]
        if len(letras) >= 4 and token[0].isupper() and _dobrar(token) not in _SIGLAS:
            return True
    return False


# Curadoria. A derivação propõe; a curadoria decide. Ela vive no acervo, em
# `FRONTEIRA_CURADORIA.json`, porque cada entrada é nome de cliente ou decisão
# sobre um — e uma lista de clientes dentro do motor seria exatamente o que este
# módulo existe para impedir. Sem ela o registro regenerado volta a divergir do
# revisado a cada demanda nova, que é a lição 87 de novo.
CURADORIA = "_FORJA_HARNESS/state/FRONTEIRA_CURADORIA.json"


def carregar_curadoria(raiz: Path) -> tuple[set[str], set[str], set[str]]:
    """Devolve (nao_e_cliente, sementes, ambiguos) lidos do acervo."""
    caminho = raiz / CURADORIA
    if not caminho.exists():
        return set(), set(), set()
    try:
        d = json.loads(caminho.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return set(), set(), set()
    return (set(d.get("naoECliente") or []), set(d.get("sementes") or []),
            {str(a).lower() for a in (d.get("ambiguos") or [])})


def _componentes_distintivos(nomes: set[str], nao_e_cliente: set[str]) -> set[str]:
    """Palavras isoladas de um nome composto, para que o prenome também proteja.

    O registro guardava o nome completo e nada mais, e é pelo primeiro nome que
    a casa escreve — "a peça do <prenome>", "o grafo do <prenome>". Medido em
    05/08/2026: um plano escrito naquela tarde chegou ao repositório do motor
    com o prenome de um cliente intacto, e o gate aprovou porque procurava o
    nome inteiro. Oito outros arquivos do motor tinham o mesmo defeito.

    Quem decide o que é vocabulário e o que é cliente é a curadoria, no acervo,
    e não uma regra automática. Duas tentativas de automatizar isso falharam, e
    as duas merecem ficar registradas:

      Medir com o padrão contra o texto cru. O gate compara contra o texto sem
      acento e em minúsculas; medir de um jeito e reprovar de outro fez a
      primeira versão aprovar 31 palavras e a varredura seguinte acusar 54
      arquivos legítimos — entre eles a palavra "construção", que é componente
      de uma razão social e vocabulário corrente do mesmo jeito.

      Aceitar a palavra que "não aparece hoje no motor". Parece auto-calibrante
      e é o contrário: **trata o vazamento existente como prova de que a palavra
      é legítima.** O prenome que motivou esta função foi excluído por esse
      critério, justamente porque já havia vazado para nove arquivos.

    Então esta função é deliberadamente burra: devolve os componentes, tira
    ruído, sigla, nome da firma e o que a curadoria já absolveu. O gate acusa; a
    curadoria absolve caso a caso, com a ocorrência à vista.
    """
    componentes: set[str] = set()
    for nome in nomes:
        partes = nome.split()
        if len(partes) < 2:
            continue
        for palavra in partes:
            dobrada = _dobrar(palavra)
            if len(palavra) < _MIN_NOME:
                continue
            if dobrada in _RUIDO or dobrada in _SIGLAS or dobrada in _FIRMA:
                continue
            if dobrada in nao_e_cliente:
                continue
            componentes.add(palavra)
    return componentes - nomes


def gerar_registro(raiz: Path) -> dict:
    """Deriva o registro de nomes protegidos do painel e das pastas de caso.

    A saída é revisável de propósito: o registro é dado de cliente e vai para o
    acervo, então quem o gera precisa poder ler a lista inteira antes de confiar
    nela. Nomes com menos de quatro caracteres são descartados porque casariam
    dentro de palavras comuns.
    """
    nomes: set[str] = set()

    painel = raiz / "gestao_escritorio/data/demandas.json"
    if painel.exists():
        try:
            dados = json.loads(painel.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            dados = {}
        for d in dados.get("demandas") or []:
            campo = str(d.get("clienteOuCaso") or "")
            for parte in re.split(r"[/×xX]|—|–|\se\s", campo):
                limpo = _limpar_nome(parte)
                if _e_nome_plausivel(limpo):
                    nomes.add(limpo)

    for p in raiz.iterdir():
        if not p.is_dir() or p.name.startswith((".", "_", "0")):
            continue
        if p.name in _RAIZ_MOTOR or p.name in _RAIZ_ACERVO:
            continue
        limpo = _limpar_nome(p.name)
        # Só as duas ou três primeiras palavras: o resto do nome da pasta é
        # descrição do pedido, não identificação de quem é o cliente.
        partes = limpo.split()
        for n in (2, 3):
            if len(partes) >= n:
                cand = " ".join(partes[:n])
                if _e_nome_plausivel(cand):
                    nomes.add(cand)

    nao_e_cliente, sementes, _ = carregar_curadoria(raiz)
    nomes = {n for n in nomes if _dobrar(n) not in nao_e_cliente}
    nomes |= sementes
    nomes |= _componentes_distintivos(nomes, nao_e_cliente)

    return {
        "schema": "FORJA-FRONTEIRA-NOMES-v1",
        "porque": ("Lista de nomes protegidos usada por forja_fronteira.py para "
                   "reprovar dado de cliente no repositório do motor. Ela É dado "
                   "de cliente e por isso mora no acervo — o motor não guarda "
                   "estes nomes nem o hash deles."),
        "nomes": sorted(nomes),
    }


MAPA_DO_DISCO = "FRONTEIRA_DO_DISCO.md"


def escrever_mapa(raiz: Path) -> str:
    """Escreve, na raiz da pasta de trabalho, de que lado está cada coisa.

    Por que um mapa gerado e não uma reorganização de pastas. A ideia natural
    era mover as pastas de caso para dentro de `_ACERVO_PROCESSUAL/`, deixando a
    raiz só com o sistema. Medido em 05/08/2026: **57 das 73 pastas de caso são
    citadas por caminho absoluto dentro da cadeia de auditoria** — 934 arquivos,
    1.299 ocorrências, entre elas o `caseFolder` que a esteira resolve em
    execução e que o gate de entrega reprova quando não existe. Mover quebraria a
    proveniência de tudo isso; mover só as 16 soltas deixaria metade das pastas
    de cada lado, que é pior do que qualquer um dos extremos.

    Então a fronteira da montagem aparece como informação, sem fingir que as
    pastas de caso podem ser movidas. Os destinos publicados, porém, são
    geograficamente separados em `%USERPROFILE%\\repos\\forja-motor` e
    `%USERPROFILE%\\repos\\forja-auditoria`. Este arquivo diz de que lado está
    cada entrada da montagem e é reescrito a cada varredura. Para um caminho
    específico, `--classificar` responde na hora.
    """
    linhas = [
        "# Fronteira no disco — o que é motor, o que é acervo, o que fica aqui",
        "",
        "> Gerado por `forja_fronteira.py --mapa`. Não edite à mão: é reescrito a",
        "> cada varredura. Para um caminho específico:",
        "> `python _FORJA_HARNESS/forja_fronteira.py --classificar CAMINHO`",
        "",
        "Os destinos publicados são duas pastas Git independentes: `forja-motor`",
        "(genérico) e `forja-auditoria` (privado e específico do escritório).",
        "As pastas de caso continuam na montagem por propósito. A cadeia de auditoria",
        "cita 57 delas por caminho absoluto, e a esteira resolve o `caseFolder`",
        "em execução — movê-las quebraria a proveniência de 934 artefatos.",
        "",
        "| entrada | lado | por quê |",
        "|---|---|---|",
    ]
    for p in sorted(raiz.iterdir(), key=lambda x: (x.is_file(), x.name.lower())):
        rel = p.name + ("/sonda" if p.is_dir() else "")
        destino, motivo = classificar(rel)
        nome = p.name + ("/" if p.is_dir() else "")
        if len(nome) > 62:
            nome = nome[:59] + "..."
        linhas.append(f"| `{nome}` | {destino} | {motivo} |")
    linhas += [
        "",
        "**MOTOR** vai para `%USERPROFILE%\\repos\\forja-motor`: genérico,",
        "compartilhável e sem identidade ou dado específico de uma banca.",
        "**ACERVO** vai para `%USERPROFILE%\\repos\\forja-auditoria`: privado,",
        "com informação do escritório, casos e evidência operacional.",
        "**LOCAL** não vai a repositório nenhum: os autos, o cofre pós-protocolo,",
        "caches e o que excede o limite de tamanho do GitHub.",
        "",
    ]
    texto = "\n".join(linhas)
    (raiz / MAPA_DO_DISCO).write_text(texto, encoding="utf-8")
    return texto


def _cli(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--raiz", type=Path, default=RAIZ_PADRAO)
    ap.add_argument("--mapa", action="store_true",
                    help="escreve FRONTEIRA_DO_DISCO.md na raiz e sai")
    ap.add_argument("--gerar-registro", action="store_true",
                    help="deriva o registro de nomes e grava no acervo")
    ap.add_argument("--classificar", metavar="CAMINHO",
                    help="mostra o destino e o motivo de um caminho, e sai")
    ap.add_argument("--json", type=Path, help="grava o laudo completo")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args(argv)

    if args.mapa:
        escrever_mapa(args.raiz)
        print(f"{MAPA_DO_DISCO} escrito na raiz da pasta de trabalho")
        return 0

    if args.gerar_registro:
        registro = gerar_registro(args.raiz)
        destino = args.raiz / REGISTRO_NOMES
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(json.dumps(registro, ensure_ascii=False, indent=2),
                           encoding="utf-8")
        print(f"{len(registro['nomes'])} nome(s) protegido(s) em {REGISTRO_NOMES}")
        for n in registro["nomes"]:
            print("   ", n)
        return 0

    if args.classificar:
        destino, motivo = classificar(args.classificar)
        print(f"{destino}  {args.classificar}\n        porque: {motivo}")
        return 0

    laudo = varrer(args.raiz)
    # Reescrito a cada varredura: um mapa que envelhece é pior do que mapa
    # nenhum, porque parece atual.
    try:
        escrever_mapa(args.raiz)
    except OSError:
        pass
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(laudo, ensure_ascii=False, indent=2),
                             encoding="utf-8")

    if not args.quiet:
        c = laudo["contagem"]
        print(f"FRONTEIRA — modo {laudo['modo']}"
              + (f" ({laudo['nomesProtegidos']} nomes protegidos)"
                 if laudo["modo"] == "nominal"
                 else " — o registro de nomes do acervo não está montado;"
                      " só sinais estruturais foram procurados"))
        print(f"  motor {c[MOTOR]}   acervo {c[ACERVO]}   local {c[LOCAL]}")
        for v in laudo["violacoes"][:40]:
            print(f"  [{v['classe']}] {v['caminho']}")
            print(f"        {', '.join(v['sinais'][:5])}")
        if len(laudo["violacoes"]) > 40:
            print(f"  ... e mais {len(laudo['violacoes']) - 40} arquivo(s)")
        for g in laudo["arquivosGrandes"]:
            print(f"  [grande] {g['bytes'] / 2**20:.1f} MB  {g['caminho']}")
        print("APROVADO" if laudo["aprovado"]
              else f"REPROVADO — {len(laudo['violacoes'])} violação(ões),"
                   f" {len(laudo['arquivosGrandes'])} arquivo(s) grande(s)")
    return 0 if laudo["aprovado"] else 1


if __name__ == "__main__":
    sys.exit(_cli())
