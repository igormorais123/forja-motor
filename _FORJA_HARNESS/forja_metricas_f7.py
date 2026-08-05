"""FORJA N2 - F7 Métricas leves: citações conferidas, verificações pendentes, autoridades.

Extrai do markdown-fonte campos calculados para o bloco F7 (gate de qualidade).
Sem dependência de COM ou renderização — apenas análise textual.
"""

import re
from pathlib import Path

FORJA = Path(__file__).resolve().parent

CNJ_TRIBUNAIS = {
    "4.01": "TRF1", "4.02": "TRF2", "4.03": "TRF3", "4.04": "TRF4", "4.05": "TRF5", "4.06": "TRF6",
    "8.07": "TJDFT", "8.26": "TJSP", "8.27": "TJTO", "8.21": "TJRS", "8.19": "TJRJ",
}


def tribunal_numero_cnj(value):
    match = re.search(r"\d{7}-\d{2}\.\d{4}\.(\d)\.(\d{2})\.\d{4}", str(value or ""))
    return CNJ_TRIBUNAIS.get(f"{match.group(1)}.{match.group(2)}") if match else None


def extrair_citacoes_basico(md_texto):
    """Fachada compatível sobre o inventário canônico de autoridades."""
    from forja_authorities import extract_authorities

    result = []
    for item in extract_authorities(md_texto):
        entry = dict(item)
        if entry.get("tipo") == "CNJ":
            entry["tipo"] = entry.get("corte") or "TRIBUNAL_NAO_MAPEADO"
        result.append(entry)
    return result


def cache_com_lastro(path, *, require_live=True):
    """Só aceita captura hash-bound no manifesto de fontes oficiais.

    Nome convincente, texto longo ou ``http`` no corpo são dados controlados
    pelo próprio produtor e, isoladamente, não provam a jurisprudência.
    """
    from forja_official_sources import validate_cached_source

    path = Path(path)
    cache_dir = path.resolve().parent
    manifest_path = cache_dir / "OFFICIAL_SOURCE_MANIFEST.json"
    return validate_cached_source(
        path,
        manifest_path,
        cache_dir=cache_dir,
        require_live=require_live,
    )["approved"]


def procurar_em_cache_oficial(citacao, *, require_live=True):
    """Verifica se a citação tem fonte oficial arquivada no cache."""
    cache = FORJA / "cache" / "fontes_oficiais"
    if not cache.exists():
        return None

    tipo = citacao["tipo"]
    numero = citacao["numero"]
    corte = citacao.get("corte")

    classe = str(citacao.get("classe") or "").upper()
    identity = citacao.get("authorityIdentity") or {}
    prefixos = {
        "SUMULA_VINCULANTE": [f"STF_SUMULA_VINCULANTE_{numero}"],
        # Lição 41(c): a chave SUMULA faltava — súmulas nunca eram localizadas no cache
        "SUMULA": [f"STJ_SUMULA_{numero}", f"STF_SUMULA_{numero}"],
        "TEMA": [f"STJ_TEMA_{numero}", f"STF_TEMA_{numero}"],
        "INFORMATIVO": [f"STJ_INFORMATIVO_{numero}", f"STF_INFORMATIVO_{numero}"],
        "STJ": [f"STJ_{classe}_{numero}"],
        "STF": [f"STF_{classe}_{numero}"],
        "NORMA": [
            f"PLANALTO_{identity.get('code')}_ART_{identity.get('article')}"
            if classe == "ARTICLE"
            else f"PLANALTO_{classe}_{numero}"
        ],
    }.get(tipo, [])

    # Corte conhecida: só o cache DAQUELE tribunal vale como conferência.
    if corte in ("STJ", "STF") and tipo not in ("STJ", "STF", "SUMULA_VINCULANTE"):
        prefixos = [p for p in prefixos if p.startswith(corte + "_")]

    achados = [cache / (n + ".txt") for n in prefixos
               if (cache / (n + ".txt")).exists()
               and cache_com_lastro(cache / (n + ".txt"), require_live=require_live)]
    if not achados:
        return None
    # Corte desconhecida com fontes de DOIS tribunais: ambíguo — não conferida.
    if corte is None and len({a.name.split("_", 1)[0] for a in achados}) > 1:
        return None
    return achados[0]


def extrair_marcadores_verificar(md_texto):
    """Extrai todos os marcadores [VERIFICAR...] e contexto (~80 chars)."""
    padroes = re.finditer(r"\[VERIFICAR[^\]]*\]", md_texto)
    marcadores = []
    for m in padroes:
        ini = max(0, m.start() - 40)
        fim = min(len(md_texto), m.end() + 40)
        contexto = re.sub(r"\s+", " ", md_texto[ini:fim]).strip()
        marcadores.append({
            "marcador": m.group(0),
            "contexto": contexto
        })
    return marcadores


def metricas_f7(md_texto, *, require_live=True):
    """Calcula métricas de completude para o gate F7.

    Retorna dict com:
      - citacoesTotal: count
      - citacoesConferidasEmFonte: count + lista de rótulos
      - citacoesNaoConferidas: lista de rótulos SEM fonte
      - verificarRestantes: lista de [VERIFICAR...] com contexto
      - autoridadesDecisivasComVigenciaConferida: null (preenchido manualmente)
    """
    citacoes = extrair_citacoes_basico(md_texto)

    conferidas = []
    nao_conferidas = []

    citation_records = []
    for cit in citacoes:
        source = procurar_em_cache_oficial(cit, require_live=require_live)
        if source:
            conferidas.append(cit["rótulo"])
        else:
            nao_conferidas.append(cit["rótulo"])
        citation_records.append({
            "tipo": cit["tipo"],
            "classe": cit.get("classe"),
            "numero": cit["numero"],
            "corte": cit.get("corte"),
            "rotulo": cit["rótulo"],
            "authorityIdentity": cit.get("authorityIdentity"),
            "sourcePath": str(source) if source else None,
        })

    verificar = extrair_marcadores_verificar(md_texto)

    return {
        "citacoesTotal": len(citacoes),
        "citacoesConferidasEmFonte": len(conferidas),
        "citacoesConferidasRotulos": conferidas,
        "citacoesNaoConferidas": nao_conferidas,
        "citacoes": citation_records,
        "verificarRestantes": verificar,
        "autoridadesDecisivasComVigenciaConferida": None,  # Preenchido manualmente (Modo 6)
    }


if __name__ == "__main__":
    import sys
    import json

    if len(sys.argv) < 2:
        print("uso: python forja_metricas_f7.py <arquivo.md>")
        sys.exit(1)

    md_path = Path(sys.argv[1])
    if not md_path.exists():
        print(f"arquivo não encontrado: {md_path}")
        sys.exit(1)

    texto = md_path.read_text(encoding="utf-8")
    resultado = metricas_f7(texto)
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
