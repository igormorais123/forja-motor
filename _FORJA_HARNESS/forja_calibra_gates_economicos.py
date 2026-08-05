"""Calibração dos gates L9-L13 contra o acervo real da fábrica.

Passo 6 do plano 41. Existe pelo mesmo motivo do `forja_calibra_monetario.py`:
o número da taxa de falso positivo vai ao Fábio como evidência, e número em
relatório de evidência sem comando que o reproduza é atestação sem lastro.

O método é o do gate de colisão de SVG, que a casa já validou: rodar contra o
acervo inteiro, contar reprovações e **nomear cada caso limítrofe** — não
aceitar uma taxa agregada como prova de calibração.

O que este script mede, e o que ele NÃO mede:

  - **Incidência** (`material_economico`): quantos documentos os gates tocam.
    Documento fora disso passa intacto e nem é analisado.
  - **L11 sobre documento sem ledger**: o pior caso. Todo valor calculado vira
    órfão, porque não há âncora nenhuma. Esse número é o TETO de reprovação, não
    a taxa esperada em produção — em produção o caso tem ledger.
  - **Separação citado × calculado**: é a medida que interessa de verdade. Valor
    que a peça CITA (de acórdão, contrato ou laudo da parte adversária) não é
    cálculo nosso e não pode exigir âncora própria. Se a heurística de citação
    estiver fraca, o L11 trava toda peça que cite valor de julgado — o modo de
    falha mais provável desta entrega, segundo o § 5 do plano.

Uso:
    python forja_calibra_gates_economicos.py [--saida CALIBRACAO_GATES_ECONOMICOS.json]
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from forja_lastro import (  # noqa: E402
    VERSAO,
    _valores_monetarios,
    material_economico,
    validar_valores_monetarios,
)

RAIZ = Path(__file__).resolve().parent.parent
VERSAO_CALIBRACAO = "FORJA-CALIBRA-GATES-ECONOMICOS-v1"

# Ruído que não é produto do escritório: cache, dependências, saídas de
# ferramenta e o próprio material de teste — que contém valores fabricados de
# propósito e envenenaria a medição.
IGNORAR = (
    "node_modules", "__pycache__", ".git", "graphify-out", "MAPA_IA.md",
    "00_IA_NAVIGACAO", "cache", ".autoresearch", "test_", "_backups",
)

LIMITE_BYTES = 4 * 1024 * 1024


def relevante(caminho: Path) -> bool:
    partes = caminho.as_posix()
    if any(marca in partes for marca in IGNORAR):
        return False
    try:
        return caminho.stat().st_size <= LIMITE_BYTES
    except OSError:
        return False


def main(argv: list[str]) -> int:
    saida = RAIZ / "_FORJA_HARNESS" / "state" / "CALIBRACAO_GATES_ECONOMICOS.json"
    if "--saida" in argv:
        saida = Path(argv[argv.index("--saida") + 1])

    total = economicos = 0
    valores_totais = valores_citados = 0
    com_reprovacao = 0
    reprovacoes = Counter()
    limitrofes: list[dict] = []

    for caminho in RAIZ.rglob("*.md"):
        if not relevante(caminho):
            continue
        try:
            texto = caminho.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        total += 1
        if not material_economico(texto):
            continue
        economicos += 1

        valores = _valores_monetarios(texto)
        valores_totais += len(valores)
        citados = [v for v in valores if v["citado"]]
        valores_citados += len(citados)

        # Pior caso deliberado: sem ledger, nada tem âncora.
        achados = validar_valores_monetarios(texto, None)
        if achados:
            com_reprovacao += 1
            reprovacoes[len(achados)] += 1

        # Caso limítrofe = documento onde a peça cita valor de terceiro. É onde
        # a heurística de citação decide entre gate útil e trava.
        for v in citados[:2]:
            if len(limitrofes) < 40:
                limitrofes.append({
                    "arquivo": caminho.relative_to(RAIZ).as_posix(),
                    "valor": v["raw"],
                    "reconhecido_como_citacao": True,
                    "trecho": v["contexto"][:180],
                })

    pct = lambda n, d: round(100.0 * n / d, 1) if d else 0.0  # noqa: E731
    resultado = {
        "versao": VERSAO_CALIBRACAO,
        "versaoGates": VERSAO,
        "geradoEm": datetime.now().astimezone().isoformat(timespec="seconds"),
        "raiz": str(RAIZ),
        "documentosAnalisados": total,
        "documentosEconomicos": economicos,
        "incidenciaPct": pct(economicos, total),
        "valoresMonetariosEncontrados": valores_totais,
        "valoresReconhecidosComoCitacao": valores_citados,
        "pctValoresCitados": pct(valores_citados, valores_totais),
        "documentosQueL11ReprovariaSemLedger": com_reprovacao,
        "pctReprovacaoTetoSemLedger": pct(com_reprovacao, economicos),
        "limitrofes": limitrofes,
        "limite": (
            "Reprovação sem ledger é TETO, não taxa esperada: mede o gate contra "
            "documento que ainda não tem memória documental. A medida de calibração "
            "é a separação citado × calculado."
        ),
    }
    saida.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + "\n",
                     encoding="utf-8", newline="\n")

    print(f"documentos analisados ......... {total}")
    print(f"com material econômico ........ {economicos} ({resultado['incidenciaPct']}%)")
    print(f"valores monetários ............ {valores_totais}")
    print(f"reconhecidos como citação ..... {valores_citados} ({resultado['pctValoresCitados']}%)")
    print(f"teto de reprovação sem ledger . {com_reprovacao} de {economicos} "
          f"({resultado['pctReprovacaoTetoSemLedger']}%)")
    print(f"casos limítrofes nomeados ..... {len(limitrofes)}")
    print(f"-> {saida.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
