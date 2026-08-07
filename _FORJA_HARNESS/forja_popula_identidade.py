# -*- coding: utf-8 -*-
"""
forja_popula_identidade.py — Popula F2_IDENTIDADE_PROCESSUAL.json para os 27 casos.

Este script lê FORJA_CASE_MANIFEST.json de cada caso, localiza a fonte de comando
(COMANDO_DO_EMAIL.md, e-mail, decisão impugnada) e extrai informações de:
  - Cliente (nome, papel)
  - Adversário (nome, papel)
  - Direção do pedido

O script pede confirmação para cada caso antes de gravar.

Uso:
  python forja_popula_identidade.py [--auto] [--verbose]

--auto: não pede confirmação, grava tudo
--verbose: mostra detalhes de cada extração
"""
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


RAIZ = Path(__file__).resolve().parent
STATE_DIR = RAIZ / "state"


# Dicionário manual de mapeamentos por padrão de caso. Cada entrada é:
#   <padrão>: (cliente, papel_cliente, adverso, papel_adverso, direcao_pedido, sourceKey, trecho)
#
# sourceKey deve ser uma chave de n4SourceRegistry do manifesto. O trecho
# deve ser verbatim (cópia literal) de ~25+ caracteres da fonte.
#
# CRITÉRIO INVIOLÁVEL: o lastro deve vir de FORA da redação (comando, decisão impugnada,
# e-mail de demanda). NUNCA da minuta ou derivado. A declaração só é válida se
# conferida PALAVRA POR PALAVRA contra a fonte apontada.
#
# Nenhum mapeamento aqui pode ser hipótese. Se houver dúvida sobre o nome ou papel
# da cliente, deixar sem mapeamento (vazio) — declaração inventada é PIOR que ausente,
# porque nasceria válida mas falsa, e o gate morreria junto.
#
# ESTADO (05/08/2026): 27 casos com manifesto, 0 com declaração verificada.
# Os 6 casos que têm draft rodável na mutação não entraram aqui porque não confirmei
# a identidade da cliente contra a fonte real (só havia hipóteses).
MAPEAMENTOS = {
    # Deixado vazio propositalmente. Preencher após verificação manual com a fonte real.
}


def encontrar_caso_por_id(case_id: str) -> Optional[Path]:
    """Localiza diretório de caso por ID."""
    casos = list(STATE_DIR.glob(f"{case_id}"))
    if casos:
        return casos[0]
    return None


def gerar_f2_identidade(
    case_id: str,
    cliente: str,
    papel_cliente: str,
    adverso: str,
    papel_adverso: str,
    direcao: str,
    sourceKey: str,
    trecho: str,
) -> dict:
    """Gera artefato F2_IDENTIDADE_PROCESSUAL.json."""
    return {
        "schemaVersion": 1,
        "artifactType": "F2_IDENTIDADE_PROCESSUAL",
        "caseId": case_id,
        "cliente": {
            "nome": cliente.strip(),
            "papel": papel_cliente.strip().lower(),
        },
        "adverso": {
            "nome": adverso.strip(),
            "papel": papel_adverso.strip().lower(),
        },
        "direcaoPedido": direcao.strip().lower(),
        "lastro": {
            "sourceKey": sourceKey,
            "sha256": "[será preenchido na conferência manual]",
            "trechoVerbatim": trecho.strip(),
        },
        "createdAt": datetime.now().isoformat(),
        "note": "Extraído de COMANDO_DO_EMAIL.md e fontes dos autos. Revisar contra manifesto.",
    }


def processar_caso(
    case_id: str,
    case_dir: Path,
    auto: bool = False,
    verbose: bool = False,
) -> bool:
    """
    Processa um caso: carrega manifesto, extrai dados e cria F2 se mapeamento existe.

    Retorna True se gravou com sucesso.
    """
    # Carregar manifesto
    manifest_path = case_dir / "FORJA_CASE_MANIFEST.json"
    if not manifest_path.exists():
        if verbose:
            print(f"  ✗ Manifesto não existe")
        return False

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as e:
        if verbose:
            print(f"  ✗ Erro ao ler manifesto: {e}")
        return False

    # Verificar se já existe
    f2_path = case_dir / "n4_artifacts" / "F2_IDENTIDADE_PROCESSUAL.json"
    if f2_path.exists():
        if verbose:
            print(f"  ✓ F2 já existe, pulando")
        return True

    # Procurar mapeamento
    dados = MAPEAMENTOS.get(case_id)
    if not dados:
        if verbose:
            print(f"  ⊘ Sem mapeamento — será necessário entrada manual")
        return False

    if verbose:
        print(f"  → Cliente: {dados['cliente']} ({dados['papel_cliente']})")
        print(f"  → Adverso: {dados['adverso']} ({dados['papel_adverso']})")
        print(f"  → Direção: {dados['direcao']}")

    # Gerar artefato
    f2_decl = gerar_f2_identidade(
        case_id=case_id,
        cliente=dados["cliente"],
        papel_cliente=dados["papel_cliente"],
        adverso=dados["adverso"],
        papel_adverso=dados["papel_adverso"],
        direcao=dados["direcao"],
        sourceKey=dados["sourceKey"],
        trecho=dados["trecho"],
    )

    # Pedir confirmação se não --auto
    if not auto:
        print(json.dumps(f2_decl, ensure_ascii=False, indent=2))
        resposta = input(f"\n  Gravar em {f2_path}? [s/N] ").lower().strip()
        if resposta != "s":
            return False

    # Criar diretório se não existe
    f2_path.parent.mkdir(parents=True, exist_ok=True)

    # Gravar
    try:
        f2_path.write_text(json.dumps(f2_decl, ensure_ascii=False, indent=2), encoding="utf-8")
        if verbose:
            print(f"  ✓ Gravado: {f2_path}")
        return True
    except Exception as e:
        print(f"  ✗ Erro ao gravar: {e}", file=sys.stderr)
        return False


def main(argv=None):
    argv = argv or sys.argv[1:]

    auto = "--auto" in argv
    verbose = "--verbose" in argv

    # Encontrar todos os casos com manifesto
    casos = []
    for case_dir in sorted(STATE_DIR.glob("case-*")):
        manifest = case_dir / "FORJA_CASE_MANIFEST.json"
        if manifest.exists():
            casos.append((case_dir.name, case_dir))

    if not casos:
        print("Nenhum caso com FORJA_CASE_MANIFEST.json encontrado", file=sys.stderr)
        return 1

    if verbose:
        print(f"Encontrados {len(casos)} casos com manifesto\n")

    gravos = 0
    for case_id, case_dir in casos:
        print(f"{case_id}...")
        if processar_caso(case_id, case_dir, auto=auto, verbose=verbose):
            gravos += 1
        print()

    print(f"\n{'='*70}")
    print(f"RESUMO: {gravos} artefatos F2_IDENTIDADE_PROCESSUAL gravados")
    print(f"Faltam mapeamentos manualmente: {len(casos) - gravos}")
    print(f"\nPróximo passo: revisar cada declaração contra a fonte real.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
