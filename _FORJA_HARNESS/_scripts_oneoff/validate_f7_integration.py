"""Validação de integração F7 no render (sem COM)."""

import json
import sys
from pathlib import Path

FORJA = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(FORJA))

from forja_metricas_f7 import metricas_f7  # noqa: E402


def main():
    md_path = FORJA / "state/case-email-azimut-19f3ed5bdbdcf159/producao/MEMORIAL_AZIMUT_RESP_2237713.md"
    md_texto = md_path.read_text(encoding="utf-8")
    metricas = metricas_f7(md_texto)

    # Simula montagem F7 como em forja_render_docx (linhas 198-199)
    f7 = {"arquivo": str(md_path), "tipo": "peca", **metricas}

    print("✓ Montagem F7 bem-sucedida")
    print(f"  citacoesTotal: {f7['citacoesTotal']}")
    print(f"  citacoesConferidasEmFonte: {f7['citacoesConferidasEmFonte']}")
    print(f"  citacoesNaoConferidas ({len(f7['citacoesNaoConferidas'])}):")
    for cit in f7["citacoesNaoConferidas"]:
        print(f"    - {cit}")
    print(f"  verificarRestantes ({len(f7['verificarRestantes'])}):")
    for v in f7["verificarRestantes"][:2]:
        print(f"    - {v['marcador'][:70]}...")
    if len(f7["verificarRestantes"]) > 2:
        print(f"    ... ({len(f7['verificarRestantes']) - 2} mais)")

    # Valida que pode ser serializado para JSON (como will be em F7_VERIFICADOR_FORJA.json)
    json_str = json.dumps(f7, ensure_ascii=False, indent=2)
    assert len(json_str) > 100, "JSON vazio ou muito pequeno"
    print(f"\n✓ JSON serializável ({len(json_str)} bytes)")

    # Valida estrutura esperada
    assert f7["tipo"] == "peca"
    assert "citacoesTotal" in f7
    assert "citacoesNaoConferidas" in f7
    assert "verificarRestantes" in f7
    assert "autoridadesDecisivasComVigenciaConferida" in f7
    assert f7["autoridadesDecisivasComVigenciaConferida"] is None

    print("✓ Estrutura F7 validada")
    print("\nJSON pronto para F7_VERIFICADOR_FORJA.json:")
    print(json_str)


if __name__ == "__main__":
    main()
