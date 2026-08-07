# -*- coding: utf-8 -*-
"""
forja_injection_scan.py — Detecção de injeção indireta via PDF (U3 do plano).

Escaneia PDFs em busca de sinais de prompt injection disfarçada:
  (a) Texto com fonte < 2pt (tinta invisível ou carimbo legítimo).
  (b) Texto com cor idêntica/quase idêntica ao fundo (branco sobre branco).
  (c) Padrões de instrução em PT/EN no texto extraído.

Uso: python forja_injection_scan.py <pasta_caso_ou_arquivo.pdf>
Saída: JSON no stdout + evidência persistida. Entradas internas preservam o
       sidecar histórico; entradas externas são isoladas em
       ``telemetria/injection_scans`` e nunca alteram a pasta do anexo.
       Achados marcados como P0 para triagem humana (não bloqueio cego).

Legítimos tolerados:
  - Carimbo, rodapé, assinatura digital < 2pt (comum em notarização).
  - Metadados de PDF (autor, assunto), não texto extraído.

P0 é levantado para triagem HUMANA quando padrão de instrução é detectado,
independentemente de tamanho/cor. Isso NÃO bloqueia a ingestão automaticamente.
"""

import os
import sys
import json
import re
import hashlib
import tempfile
from pathlib import Path

from forja_metadata import retry_transient_io

try:
    import pdfplumber
except ImportError:
    print("Erro: pdfplumber não instalado. pip install pdfplumber", file=sys.stderr)
    sys.exit(1)


# Padrões de instrução de prompt injection (case-insensitive)
# Refinados para evitar falsos positivos em disclaimers legais e linguagem normal.
PADROES_INSTRUCAO_PT = [
    r"ignore as instru[çc][õo]es",
    r"desconsidere as instru[çc][õo]es",
    r"ignore a instru[çc][ãa]o",
    r"n[ãa]o considere o anterior",
    r"es[çc]ueza o que foi dito",
    r"(?:me\s+)?responda que\s+(?:o|a|e)",  # "responda que o recurso" ou similar
    r"diga que\s+(?:o|a|e|sou)",  # "diga que é" ou similar
    r"afirme que\s+(?:o|a|e)",
    r"pense que\s+(?:o|a|e)",
    r"assuma que\s+(?:o|a|e)",
    r"considerem que\s+(?:o|a|e)",
    r"instru[çc][õo]es? do sistema",
    r"instru[çc][ãa]o oculta",
    r"agenda oculta",
    r"mensagem secreta",
]

PADROES_INSTRUCAO_EN = [
    r"ignore previous",
    r"ignore all previous",
    r"disregard the above",
    r"forget the previous",
    r"(?:^|\s)you are\s+(?:a|an|the)\s+[a-z]+",  # "you are a" ou "you are an" — não falso positivo "If you are"
    r"system prompt",
    r"do not mention",
    r"new instructions",
    r"override",
    r"bypass",
    r"hidden agenda",
    r"secret instruction",
]

REGEX_INSTRUCAO = re.compile(
    "|".join(PADROES_INSTRUCAO_PT + PADROES_INSTRUCAO_EN),
    re.IGNORECASE | re.MULTILINE
)

# Limiar de tamanho em pontos (pt). Carimbo legítimo: até ~1.5pt.
LIMIAR_FONTE_PT = 2.0

# Amostragem dos achados de nível de caractere.
#
# Por que existe. Os detectores (a) fonte microscópica e (b) cor invisível
# emitiam UM registro por glifo, e o mesmo glifo era gravado duas vezes — na
# página e no resumo do arquivo. Um PDF pericial de 945 páginas produziu 645.966
# registros e um laudo de 291 MB, quase todo composto de espaços e caracteres
# soltos a 1,7 pt, que em PDF vetorial são artefato de diagramação e não
# tentativa de injeção. O laudo ficou grande demais para ser lido por humano,
# grande demais para o limite de 100 MB por arquivo do GitHub — travando o push
# do repositório inteiro — e não acrescentava nada ao veredito, que sai de
# `padrao_instrucao`.
#
# O que NÃO muda: a contagem, que é exata e vive em `contagens`, e a decisão de
# P0, que continua vindo de `padrao_instrucao` — este não é amostrado, porque é
# de baixo volume e é o achado que exige triagem humana. Amostrar é reduzir a
# evidência ilustrativa, nunca a medida.
AMOSTRA_POR_PAGINA = 20
AMOSTRA_POR_ARQUIVO = 200


def _amostrar(destino, registro, limite):
    """Guarda os `limite` primeiros exemplos; o resto vira só contagem."""
    if len(destino) < limite:
        destino.append(registro)

# Tolerância de cor: distância Euclidiana RGB. 5 = praticamente idêntica.
TOLERANCIA_COR = 5.0

# A fonte escaneada pode estar em uma pasta jurídica externa e protegida.
# Nunca deixe o diagnóstico criar artefatos ao lado do documento de terceiro:
# quando a entrada não pertence à FORJA, a evidência fica no cofre local de
# telemetria. Isso também evita que uma pasta de anexos seja alterada apenas
# por uma leitura.
FORJA_ROOT = Path(__file__).resolve().parent
TELEMETRIA_SCAN_DIR = FORJA_ROOT / "telemetria" / "injection_scans"


def _esta_dentro_de(caminho, raiz):
    """Retorna True quando *caminho* está contido em *raiz*."""
    try:
        Path(caminho).resolve().relative_to(Path(raiz).resolve())
        return True
    except ValueError:
        return False


def _id_origem(caminho):
    """Identificador estável para não colidir no cofre de telemetria."""
    origem = str(Path(caminho).resolve()).encode("utf-8", errors="replace")
    return hashlib.sha256(origem).hexdigest()[:12]


def _gravar_json_seguro(caminho, payload):
    """Grava JSON criando apenas diretórios sob o destino já escolhido."""
    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    # Serializa em memória e grava de forma ATÔMICA, em binário, com repetição.
    #
    # A versão anterior usava `json.dump` direto sobre arquivo em modo texto e
    # falhava com `OSError: [Errno 22] Invalid argument` em 8 a 9 dos 15 anexos
    # reais do acervo. O que descarta o conteúdo do PDF como causa é que **o
    # conjunto que falha muda a cada execução**: a mesma entrada reprova numa
    # rodada e passa na seguinte. O padrão é de disputa pelo arquivo — indexador,
    # antivírus ou o observador de mapas do ambiente abrindo o JSON recém-escrito
    # —, e o Windows devolve `Errno 22` quando o handle é reaberto nessa janela.
    #
    # Gravar num temporário ao lado e renomear por cima fecha o caso comum,
    # porque `os.replace` é atômico. O retry canônico do projeto cobre a janela
    # transitória de `Errno 13/22` sem mascarar outros erros de I/O.
    #
    # `surrogatepass` porque o objetivo é PRESERVAR a evidência de um documento
    # possivelmente envenenado, não normalizá-la: trocar o byte estranho por "?"
    # apagaria justamente o que o scanner existe para achar.
    dados = json.dumps(payload, ensure_ascii=False, indent=2).encode(
        "utf-8", errors="surrogatepass"
    )

    def _uma_tentativa():
        fd, nome_temporario = tempfile.mkstemp(
            prefix=f".{caminho.stem}.", suffix=".tmp", dir=caminho.parent
        )
        os.close(fd)
        temporario = Path(nome_temporario)
        try:
            temporario.write_bytes(dados)
            os.replace(temporario, caminho)
        finally:
            temporario.unlink(missing_ok=True)

    retry_transient_io(_uma_tentativa)
    return caminho


def distancia_rgb(cor1, cor2):
    """Calcula distância Euclidiana entre dois RGB (0-1 ou 0-255)."""
    if not cor1 or not cor2 or len(cor1) < 3 or len(cor2) < 3:
        return float('inf')
    r1, g1, b1 = cor1[:3]
    r2, g2, b2 = cor2[:3]
    # Converter para 0-255 se necessário (pdfplumber normaliza para 0-1)
    if max(r1, g1, b1) <= 1.0:
        r1, g1, b1 = r1 * 255, g1 * 255, b1 * 255
    if max(r2, g2, b2) <= 1.0:
        r2, g2, b2 = r2 * 255, g2 * 255, b2 * 255
    return ((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2) ** 0.5


def analisar_pdf(caminho_pdf):
    """
    Escaneia um PDF em busca de sinais de injection.
    Retorna dict com achados por página.
    """
    achados = {
        "arquivo": str(caminho_pdf),
        "paginas": {},
        "resumo_geral": {
            "fonte_microscopica": [],
            "cor_invisivel": [],
            "padrao_instrucao": [],
        },
        # Contagem EXATA, independente da amostragem das listas. Quem decide
        # gravidade lê daqui; as listas servem para o humano ver exemplos.
        "contagens": {
            "fonte_microscopica": 0,
            "cor_invisivel": 0,
            "padrao_instrucao": 0,
        },
        "p0": False,
    }

    try:
        with pdfplumber.open(caminho_pdf) as pdf:
            for num_pagina, pagina in enumerate(pdf.pages, start=1):
                achados_pagina = {
                    "num": num_pagina,
                    "fonte_microscopica": [],
                    "cor_invisivel": [],
                    "padrao_instrucao": [],
                }

                # Extrair texto
                texto_pagina = pagina.extract_text() or ""

                # (c) Padrão de instrução no texto extraído
                for match in REGEX_INSTRUCAO.finditer(texto_pagina):
                    trecho = texto_pagina[
                        max(0, match.start() - 100) : min(len(texto_pagina), match.end() + 100)
                    ].replace("\n", " ")[:200]
                    achados_pagina["padrao_instrucao"].append(
                        {
                            "tipo": "padrao_instrucao",
                            "padrao": match.group(),
                            "trecho": trecho,
                            "severidade": "P0",
                        }
                    )
                    achados["contagens"]["padrao_instrucao"] += 1
                    achados["resumo_geral"]["padrao_instrucao"].append(
                        {"pagina": num_pagina, "padrao": match.group(), "trecho": trecho}
                    )
                    achados["p0"] = True

                # (a) e (b) Análise de caracteres individuais (fonte + cor)
                # pdfplumber extrai text_objects; verificar cada um
                chars = pagina.chars
                if chars:
                    # Tentar detectar cor de fundo da página (heurística)
                    # Próximo objeto preenchido grande = fundo provável
                    cor_fundo = (1.0, 1.0, 1.0)  # Padrão: branco
                    for rect in pagina.rects:
                        if rect.get("fill"):
                            cor_fundo = rect.get("fill") or cor_fundo
                            break

                    for char_obj in chars:
                        tamanho_font = char_obj.get("size", 0)
                        cor_char = char_obj.get("color")

                        # (a) Fonte muito pequena
                        if tamanho_font > 0 and tamanho_font < LIMIAR_FONTE_PT:
                            trecho_char = char_obj.get("text", "?")
                            achados["contagens"]["fonte_microscopica"] += 1
                            _amostrar(
                                achados_pagina["fonte_microscopica"],
                                {
                                    "tipo": "fonte_microscopica",
                                    "texto": trecho_char,
                                    "tamanho_pt": tamanho_font,
                                    "severidade": "P1",
                                },
                                AMOSTRA_POR_PAGINA,
                            )
                            _amostrar(
                                achados["resumo_geral"]["fonte_microscopica"],
                                {
                                    "pagina": num_pagina,
                                    "texto": trecho_char,
                                    "tamanho": tamanho_font,
                                },
                                AMOSTRA_POR_ARQUIVO,
                            )

                        # (b) Cor idêntica ao fundo
                        if cor_char and distancia_rgb(cor_char, cor_fundo) < TOLERANCIA_COR:
                            trecho_char = char_obj.get("text", "?")
                            achados["contagens"]["cor_invisivel"] += 1
                            _amostrar(
                                achados_pagina["cor_invisivel"],
                                {
                                    "tipo": "cor_invisivel",
                                    "texto": trecho_char,
                                    "cor_char": cor_char,
                                    "cor_fundo_estimada": cor_fundo,
                                    "severidade": "P1",
                                },
                                AMOSTRA_POR_PAGINA,
                            )
                            _amostrar(
                                achados["resumo_geral"]["cor_invisivel"],
                                {
                                    "pagina": num_pagina,
                                    "texto": trecho_char,
                                    "distancia_cor": distancia_rgb(cor_char, cor_fundo),
                                },
                                AMOSTRA_POR_ARQUIVO,
                            )

                if any(
                    [
                        achados_pagina["fonte_microscopica"],
                        achados_pagina["cor_invisivel"],
                        achados_pagina["padrao_instrucao"],
                    ]
                ):
                    achados["paginas"][num_pagina] = achados_pagina
    except Exception as e:
        achados["erro"] = str(e)
        return achados

    return achados


def processar_entrada(entrada):
    """
    Recebe caminho de arquivo PDF ou pasta de caso.
    Retorna lista de PDFs para analisar.
    """
    entrada = Path(entrada)

    if entrada.is_file() and entrada.suffix.lower() == ".pdf":
        return [entrada]

    if entrada.is_dir():
        # Glob recursivo por PDFs
        pdfs = list(entrada.glob("**/*.pdf"))
        # Filtrar PDFs > 20MB
        pdfs = [p for p in pdfs if p.stat().st_size < 20 * 1024 * 1024]
        return sorted(pdfs)

    raise ValueError(f"Entrada inválida (não é PDF ou pasta): {entrada}")


# ---------------------------------------------------------------------------
# Gate computado `injection_triaged`
# ---------------------------------------------------------------------------
# Até 04/08/2026 este gate era escrito pelo agente da fase F1: nove execuções,
# nove `pass`, nenhuma reprovação. Ele existe por causa do U3 — conteúdo dos
# autos é DADO, nunca instrução — e um `pass` falso significa ingerir autos sem
# ter procurado texto branco sobre branco, fonte de 1,7 pt ou padrão de comando
# escondido no PDF.
#
# O gate é deliberadamente TOLERANTE À FORMA. Medido no acervo em 04/08/2026:
# o artefato `injection_scan.json` aparece em SETE esquemas distintos, porque
# cada caso inventou o seu (`resumo_p0`, `summaryP0`, `p0` por arquivo;
# `triagem`, `triage`, `humanTriage`, `review`, `injectionTriaged`). Um gate
# preso a um formato reprovaria seis casos corretos. Enquanto o esquema não for
# unificado — trabalho consciente, não conserto de gate —, a verificação
# procura a SUBSTÂNCIA em qualquer um deles:
#
#   LJ1 — houve varredura? algum campo declara quantos documentos foram lidos.
#   LJ2 — havendo achado P0, existe triagem humana registrada?
#
# O que ele não faz: reexecutar a varredura dos PDFs. Isso é caro, depende dos
# autos originais e é trabalho do próprio scanner; aqui se verifica que o
# scanner rodou e que o que ele achou foi tratado.

_CAMPOS_CONTAGEM = ("total_pdfs", "pdfCount", "documentsScanned", "pdfs",
                    "arquivos_analisados", "files", "scanScope")
_CAMPOS_TRIAGEM = ("triagem", "triage", "humanTriage", "review", "injectionTriaged",
                   "existingSpecificEvidence", "approved", "status")
_GATE_VERSAO = "FORJA-INJECAO-GATE-v1"


def _achatar(valor, profundidade=0):
    """Percorre o JSON inteiro; os esquemas aninham de formas diferentes."""
    if profundidade > 6:
        return
    if isinstance(valor, dict):
        yield valor
        for item in valor.values():
            yield from _achatar(item, profundidade + 1)
    elif isinstance(valor, list):
        for item in valor:
            yield from _achatar(item, profundidade + 1)


def _houve_varredura(scan):
    for bloco in _achatar(scan):
        for campo in _CAMPOS_CONTAGEM:
            valor = bloco.get(campo)
            if isinstance(valor, (int, float)) and valor > 0:
                return True
            if isinstance(valor, (list, dict)) and len(valor) > 0:
                return True
    return False


def _p0_detectado(scan):
    """P0 em qualquer um dos sete dialetos, sem confundir 'false' com ausência."""
    for bloco in _achatar(scan):
        if bloco.get("p0") is True:
            return True
        for campo in ("resumo_p0", "summaryP0", "p0Findings"):
            valor = bloco.get(campo)
            # Um resumo é um dicionário de CONTAGENS: `{"cor_invisivel": 0,
            # "fonte_microscopica": 0}` significa que nada foi achado. Tratar o
            # dicionário não vazio como detecção reprovava a CASO-04, cuja
            # varredura estava limpa — o gate acusaria justamente quem varreu
            # direito e registrou o resultado.
            if isinstance(valor, dict):
                if any(isinstance(v, (int, float)) and v > 0 for v in valor.values()):
                    return True
                continue
            if isinstance(valor, list) and len(valor) > 0:
                return True
            if isinstance(valor, (int, float)) and valor > 0:
                return True
        if str(bloco.get("severidade") or "").upper() == "P0":
            return True
        if bloco.get("promptInjectionDetected") is True:
            return True
    return False


def _tem_triagem(scan):
    for bloco in _achatar(scan):
        for campo in _CAMPOS_TRIAGEM:
            valor = bloco.get(campo)
            if isinstance(valor, str) and valor.strip():
                return True
            if isinstance(valor, (dict, list)) and len(valor) > 0:
                return True
            if valor is True:
                return True
    return False


def validar_triagem_injecao(scan):
    """Achados e veredito do gate `injection_triaged`."""
    achados = []
    if not isinstance(scan, dict) or not scan:
        return {"versao": _GATE_VERSAO,
                "findings": [{"gate": "LJ1-sem-varredura", "sev": "P0",
                              "problema": ("artefato de varredura de injecao ausente ou vazio - "
                                           "os autos foram ingeridos sem procurar instrucao oculta"),
                              "acao": "rode forja_injection_scan.py sobre os autos antes de F2",
                              "versao": _GATE_VERSAO}],
                "gates": {"injection_triaged": "fail"}}

    if not _houve_varredura(scan):
        achados.append({
            "gate": "LJ1-sem-varredura", "sev": "P0",
            "problema": ("artefato de varredura nao declara nenhum documento lido - "
                         "nao ha evidencia de que a varredura ocorreu"),
            "acao": "registre o escopo varrido (quantidade e identificadores)",
            "versao": _GATE_VERSAO})

    if _p0_detectado(scan) and not _tem_triagem(scan):
        achados.append({
            "gate": "LJ2-p0-sem-triagem", "sev": "P0",
            "problema": ("varredura acusou P0 de injecao e o artefato nao registra triagem - "
                         "achado de instrucao oculta exige decisao humana registrada"),
            "acao": "registre a triagem humana do achado antes de seguir para F2",
            "versao": _GATE_VERSAO})

    reprovado = any(item["sev"] == "P0" for item in achados)
    return {"versao": _GATE_VERSAO, "findings": achados,
            "gates": {"injection_triaged": "fail" if reprovado else "pass"}}


def main():
    if len(sys.argv) < 2:
        print(
            "Uso: python forja_injection_scan.py <pasta_caso_ou_arquivo.pdf>",
            file=sys.stderr,
        )
        sys.exit(1)

    entrada = sys.argv[1]

    try:
        pdfs = processar_entrada(entrada)
    except ValueError as e:
        print(f"Erro: {e}", file=sys.stderr)
        sys.exit(1)

    if not pdfs:
        print("Nenhum PDF encontrado.", file=sys.stderr)
        sys.exit(1)

    resultado_geral = {
        "entrada": entrada,
        "total_pdfs": len(pdfs),
        "arquivos_analisados": [],
        "resumo_p0": {"padroes_instrucao": 0, "cor_invisivel": 0, "fonte_microscopica": 0},
    }

    for pdf in pdfs:
        achados = analisar_pdf(pdf)
        resultado_geral["arquivos_analisados"].append(achados)
        if achados.get("p0"):
            # Somar pelas CONTAGENS, nunca pelo tamanho da lista: as listas são
            # amostras e subcontariam o achado justamente no arquivo mais sujo.
            contagens = achados.get("contagens") or {}
            resultado_geral["resumo_p0"]["padroes_instrucao"] += contagens.get(
                "padrao_instrucao", 0)
            resultado_geral["resumo_p0"]["cor_invisivel"] += contagens.get(
                "cor_invisivel", 0)
            resultado_geral["resumo_p0"]["fonte_microscopica"] += contagens.get(
                "fonte_microscopica", 0)

    # Persistir a evidência sem alterar pastas externas à FORJA. Para entradas
    # internas, preserva-se o nome histórico; para anexos externos, usa-se o
    # cofre de telemetria com identificador da origem.
    entrada_path = Path(entrada)
    entrada_interna = _esta_dentro_de(entrada_path, FORJA_ROOT)
    if entrada_interna and entrada_path.is_dir():
        saida_json = entrada_path / "F1_INJECTION_SCAN.json"
    elif entrada_interna:
        saida_json = entrada_path.parent / "F1_INJECTION_SCAN.json"
    elif entrada_path.is_dir():
        TELEMETRIA_SCAN_DIR.mkdir(parents=True, exist_ok=True)
        saida_json = TELEMETRIA_SCAN_DIR / f"F1_INJECTION_SCAN-{_id_origem(entrada_path)}.json"
    else:
        TELEMETRIA_SCAN_DIR.mkdir(parents=True, exist_ok=True)
        saida_json = TELEMETRIA_SCAN_DIR / f"F1_INJECTION_SCAN-{_id_origem(entrada_path)}.json"

    try:
        _gravar_json_seguro(saida_json, resultado_geral)
    except OSError as erro:
        # Se uma pasta interna estiver momentaneamente protegida, ainda há um
        # destino canônico local. Se ambos falharem, o scanner não mascara a
        # perda da evidência: sai com erro e não declara a rodada concluída.
        if entrada_interna:
            try:
                TELEMETRIA_SCAN_DIR.mkdir(parents=True, exist_ok=True)
                fallback = TELEMETRIA_SCAN_DIR / f"F1_INJECTION_SCAN-{_id_origem(entrada_path)}.json"
                _gravar_json_seguro(fallback, resultado_geral)
                saida_json = fallback
            except OSError as fallback_erro:
                print(
                    f"Erro: não foi possível persistir o scan ({erro}; fallback: {fallback_erro})",
                    file=sys.stderr,
                )
                sys.exit(1)
        else:
            print(f"Erro: não foi possível persistir o scan: {erro}", file=sys.stderr)
            sys.exit(1)

    # Gravar também um relatório por PDF para debug
    relatorios_pdf = []
    if entrada_path.is_dir():
        if entrada_interna:
            pasta_relatorios = entrada_path
        else:
            pasta_relatorios = TELEMETRIA_SCAN_DIR
        for arquivo_info in resultado_geral["arquivos_analisados"]:
            nome_pdf = Path(arquivo_info["arquivo"]).stem
            if entrada_interna:
                saida_json_pdf = pasta_relatorios / f"F1_INJECTION_{nome_pdf}.json"
            else:
                saida_json_pdf = pasta_relatorios / (
                    f"F1_INJECTION_{nome_pdf}-{_id_origem(arquivo_info['arquivo'])}.json"
                )
            try:
                _gravar_json_seguro(saida_json_pdf, arquivo_info)
                relatorios_pdf.append(str(saida_json_pdf))
            except OSError as erro:
                print(f"Erro: não foi possível persistir relatório de {nome_pdf}: {erro}", file=sys.stderr)
                sys.exit(1)

    # Mantém no retorno a localização efetiva dos artefatos, tornando a
    # proteção contra escrita externa auditável sem depender do stderr.
    resultado_geral["persistencia"] = {
        "scan": str(saida_json),
        "relatorios_pdf": relatorios_pdf,
        "entrada_externa_isolada": not entrada_interna,
    }

    # O próprio sidecar também carrega a prova de onde foi persistido; não
    # basta o processo informar isso apenas no stdout.
    try:
        _gravar_json_seguro(saida_json, resultado_geral)
    except OSError as erro:
        print(f"Erro: não foi possível atualizar a prova de persistência: {erro}", file=sys.stderr)
        sys.exit(1)

    # Saída para stdout permanece JSON puro para os consumidores existentes.
    print(json.dumps(resultado_geral, ensure_ascii=False, indent=2))

    sys.exit(0)


if __name__ == "__main__":
    main()
