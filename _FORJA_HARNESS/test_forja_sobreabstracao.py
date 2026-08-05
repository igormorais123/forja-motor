# -*- coding: utf-8 -*-
"""
test_forja_sobreabstracao.py — Teste de detector de afirmação de jurisprudência
sem citação nominal (melhoria S5, gate S5 no verificador).

Executa gate_s5_sobreabstracao contra 25 peças recentes e mede taxa de
falso positivo contra baseline aprovado.

Exit code 0: teste passou. Exit code 1: falsos positivos inaceitáveis.
"""
import sys
import hashlib
import json
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

# Importar o verificador para usar as utilidades
sys.path.insert(0, str(Path(__file__).parent))


def _ler_texto(caminho: Path) -> str:
    """Extrai o texto preservando parágrafos para o gate S5."""
    if caminho.suffix.lower() != ".docx":
        return caminho.read_text(encoding="utf-8")

    with zipfile.ZipFile(caminho) as pacote:
        xml = ET.fromstring(pacote.read("word/document.xml"))
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    paragrafos = []
    for paragrafo in xml.findall(".//w:p", ns):
        texto = "".join(no.text or "" for no in paragrafo.findall(".//w:t", ns))
        if texto.strip():
            paragrafos.append(texto)
    return "\n\n".join(paragrafos)

def test_sobreabstracao_baseline():
    """Executa o gate S5 nas âncoras aprovadas e confere sua identidade."""
    baseline_path = Path(__file__).parent / "BASELINE_APROVADO.json"

    if not baseline_path.exists():
        print(f"ERRO: baseline não encontrado em {baseline_path}")
        return False

    baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
    from forja_verificador import gate_s5_sobreabstracao

    erros = []
    verificadas = 0
    for ancora in baseline["ancoras"]:
        caminho = Path(ancora["caminhoResolvido"])
        if not caminho.exists():
            erros.append(f"arquivo baseline não encontrado: {caminho}")
            continue

        digest = hashlib.sha256(caminho.read_bytes()).hexdigest()
        if digest != ancora.get("sha256"):
            erros.append(f"{ancora['id']}: SHA-256 divergente")
            continue

        try:
            texto = _ler_texto(caminho)
        except (OSError, KeyError, zipfile.BadZipFile, ET.ParseError) as exc:
            erros.append(f"{ancora['id']}: não foi possível extrair texto: {exc}")
            continue

        violacoes = gate_s5_sobreabstracao(texto)
        verificadas += 1
        if violacoes:
            erros.append(
                f"{ancora['id']}: {len(violacoes)} achado(s) S5 em âncora aprovada"
            )
            print(f"  - FALHOU {ancora['id']}: {len(violacoes)} achado(s)")
        else:
            print(f"  - OK {ancora['id']}: {caminho.name}")

    if not verificadas:
        erros.append("nenhuma âncora foi efetivamente verificada")
    if erros:
        for erro in erros:
            print(f"ERRO: {erro}")
    return not erros


def test_sobreabstracao_acervo():
    """Executa o gate contra peças recentes e relata prevalência de alertas.

    O acervo não é rotulado como aprovado/reprovado para S5; portanto, seus
    achados são diagnóstico e não uma taxa de falso positivo nem um limiar de
    aprovação. A aceitação é ancorada nas peças verificadas acima.
    """
    from forja_verificador import gate_s5_sobreabstracao

    state_dir = Path(__file__).parent / "state"

    # Coletar últimos 25 arquivos final_markdown.md ou audited_markdown.md
    markdown_files = sorted(
        list(state_dir.glob("*/runs/*/F7_AUDITORIA_JURIDICA_FACTUAL/*/final_markdown.md")) +
        list(state_dir.glob("*/runs/*/F7_AUDITORIA_JURIDICA_FACTUAL/*/audited_markdown.md")) +
        list(state_dir.glob("*/n3_artifacts/F7_AUDITORIA_JURIDICA_FACTUAL/final_markdown.md")) +
        list(state_dir.glob("*/n3_artifacts/F7_AUDITORIA_JURIDICA_FACTUAL/audited_markdown.md")),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )[:25]

    if not markdown_files:
        print("AVISO: nenhum arquivo markdown encontrado para teste")
        return True, 0, []

    achados_por_caso = []
    total_cases = len(markdown_files)
    casos_com_achado = 0

    for i, arq in enumerate(markdown_files, 1):
        try:
            texto = arq.read_text(encoding="utf-8")
            violacoes = gate_s5_sobreabstracao(texto)

            if violacoes:
                casos_com_achado += 1
                nome_caso = arq.parent.parent.parent.name
                achados_por_caso.append({
                    "caso": nome_caso,
                    "arquivo": arq.name,
                    "violacoes": len(violacoes),
                    "exemplos": violacoes[:2]  # Primeiros 2 exemplos
                })
                print(f"  [{i}/{total_cases}] {nome_caso}: {len(violacoes)} achados")
            else:
                print(f"  [{i}/{total_cases}] {arq.parent.parent.parent.name}: OK")
        except Exception as e:
            print(f"  [{i}/{total_cases}] ERRO ao processar {arq.name}: {e}")
            return False, -1, []

    taxa_com_achado = (casos_com_achado / total_cases * 100) if total_cases > 0 else 0.0

    print(f"\n{'='*60}")
    print(f"RESULTADO: {casos_com_achado}/{total_cases} casos com achados ({taxa_com_achado:.1f}%)")
    print(f"{'='*60}")

    print("OBSERVAÇÃO: o acervo não rotulado não decide aprovação; revisar os "
          "achados contra a fonte quando houver uma âncora humana.")
    return True, taxa_com_achado, achados_por_caso


if __name__ == "__main__":
    print("=" * 60)
    print("Teste de gate S5 — Afirmação de jurisprudência sem citação nominal")
    print("=" * 60)

    print("\n1. Testando baseline aprovado...")
    baseline_ok = test_sobreabstracao_baseline()

    print("\n2. Testando acervo recente...")
    acervo_ok, taxa, achados = test_sobreabstracao_acervo()

    if baseline_ok and acervo_ok:
        print("\nTESTE PASSOU")
        sys.exit(0)
    else:
        print("\nTESTE FALHOU")
        if achados and taxa > 20:
            print("\nPrimeiros achados:")
            for ac in achados[:3]:
                print(f"\n  Caso: {ac['caso']}")
                for ex in ac['exemplos'][:1]:
                    print(f"    - {ex.get('trecho', '(sem contexto)')[:100]}")
        sys.exit(1)
