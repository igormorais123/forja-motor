"""Regressão dos gates do conselho de 11/07/2026 (Efesto+Helena+Cícero+Diabob).

Cobre:
  - visual_com_lastro: DOCX visual sem lastro / hash errado / lastro ok / legado
  - f3_com_regimento: F3 ausente / sem menção a regimento / com regimento

Rodar: python test_forja_conselho_1107.py  (exit 0 = verde)
"""

import hashlib
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from forja_delivery import f3_com_regimento, visual_com_lastro  # noqa: E402

FALHAS = []


def caso(nome, ok_esperado, resultado):
    ok, motivo = resultado
    if ok is ok_esperado:
        print(f"[OK    ] {nome} ({motivo})")
    else:
        print(f"[FALHOU] {nome} — esperado ok={ok_esperado}, veio ok={ok} ({motivo})")
        FALHAS.append(nome)


with tempfile.TemporaryDirectory() as tmp:
    tmp = Path(tmp)

    # ---- visual_com_lastro ----
    caso("V1 sem DOCX visual reprova", False, visual_com_lastro(None))

    docx = tmp / "PECA_VISUAL_LAW.docx"
    docx.write_bytes(b"conteudo binario da peca visual")
    caso("V2 DOCX sem nenhum lastro reprova", False, visual_com_lastro(docx))

    fid = docx.with_name("FIDELIDADE_VISUAL.json")
    fid.write_text(json.dumps({"docxSha256": "0" * 64}), encoding="utf-8")
    caso("V3 hash ERRADO no lastro reprova (versão errada/alterada)", False, visual_com_lastro(docx))

    fid.write_text(json.dumps({}), encoding="utf-8")
    caso("V4 lastro sem docxSha256 reprova", False, visual_com_lastro(docx))

    sha_real = hashlib.sha256(docx.read_bytes()).hexdigest()
    fid.write_text(json.dumps({"docxSha256": sha_real}), encoding="utf-8")
    caso("V5 não-trava: lastro legítimo (hash bate) aprova", True, visual_com_lastro(docx))

    fid.unlink()
    docx.with_name("RELATORIO_VISUAL_LAW.json").write_text("{}", encoding="utf-8")
    caso("V6 não-trava: evidência legada (RELATORIO_VISUAL_LAW.json) aprova", True, visual_com_lastro(docx))

    docx.with_name("RELATORIO_VISUAL_LAW.json").unlink()
    docx.with_name("resultado.json").write_text("{}", encoding="utf-8")
    caso("V7 não-trava: evidência legada (resultado.json) aprova", True, visual_com_lastro(docx))

    # ---- f3_com_regimento ----
    f3 = tmp / "F3_MAPA_FONTES_E_REGIMENTO.md"
    caso("F1 F3 inexistente reprova", False, f3_com_regimento(f3))

    f3.write_text("# Mapa de fontes\n\nSó jurisprudência do STJ, nada de norma interna.\n", encoding="utf-8")
    caso("F2 F3 sem menção a regimento reprova (lição Libra Sul)", False, f3_com_regimento(f3))

    f3.write_text("# Mapa de fontes\n\nRegimento consultado: REGIMENTO_INTERNO_STJ.md "
                  "(arts. 258-259, 343-A).\n", encoding="utf-8")
    caso("F3 não-trava: F3 citando o regimento aprova", True, f3_com_regimento(f3))

print()
if FALHAS:
    print(f"FALHOU: {len(FALHAS)} caso(s): {FALHAS}")
    raise SystemExit(1)
print("OK: 7 detecções/não-travas do visual + 3 do F3 confirmadas")
