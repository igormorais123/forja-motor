# -*- coding: utf-8 -*-
"""
test_forja_regimentos.py — Regressão da auditoria de regimentos.

O risco desta auditoria não é deixar passar arquivo velho: é o contrário.
Um parser que erra o cabeçalho declara desatualizado um regimento correto e
manda o operador refazer trabalho pronto — e, na terceira vez que isso
acontece, o operador desliga a checagem. Por isso a lista de não-travas cobre
todas as variações de cabeçalho que já existem no acervo real.

Uso: python test_forja_regimentos.py   (exit 0 = ok; exit 1 = regressão)
"""
import io
import sys
import tempfile
from datetime import date
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from forja_regimentos import _extrai_data, auditar_arquivo  # noqa: E402

HOJE = date(2026, 7, 26)

# Cabeçalhos reais do acervo. Cada um vem de uma pasta de caso diferente, e
# nenhum pode ser reprovado por falta de leitura correta.
CABECALHOS_REAIS = [
    ("TRF4 Vale Trading",
     "**Consolidação oficial vigente:** incorporado até o Assento Regimental nº 37/2026\n"
     "**Fonte oficial:** https://www.trf4.jus.br/x.pdf\n"
     "**Data da verificação e do download:** 2026-07-23\n## Emendas posteriores\nNenhuma.",
     "incorporado até o Assento Regimental nº 37/2026", "2026-07-23"),
    ("STJ Cafelana",
     "- **Versão**: Consolidada até a Emenda Regimental n. 47, de 19 de dezembro de 2024\n"
     "- **Fonte**: https://www.stj.jus.br/x\n"
     "- **Data de Download**: 06 de julho de 2026\n## Emendas posteriores\nER 48 a 53.",
     "Consolidada até a Emenda Regimental n. 47", "2026-07-06"),
    ("TJDFT plano de saúde",
     "**Versão:** compilado até a Emenda Regimental nº 36\n"
     "**Fonte:** https://www.tjdft.jus.br/x\n"
     "**Baixado em:** 09/07/2026\n## Emendas posteriores\nNão localizadas.",
     "compilado até a Emenda Regimental nº 36", "2026-07-09"),
    ("TRF1 tabela",
     "| **Versão Consolidada** | Emendas Regimentais 1 a 5 (até 11/04/2022) |\n"
     "| **Fonte** | https://www.trf1.jus.br/x |\n"
     "| **Data de Download/Atualização** | 2026-07-06 |\n## Emendas posteriores\nER 6 a 12.",
     "Emendas Regimentais 1 a 5", "2026-07-06"),
]


def _escrever(tmp: Path, nome: str, conteudo: str) -> Path:
    p = tmp / f"REGIMENTO_INTERNO_{nome}.md"
    p.write_text(conteudo, encoding="utf-8")
    return p


def main() -> int:
    falhas = 0
    casos = 0

    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)

        # 1. Cabeçalhos reais são lidos corretamente e não bloqueiam.
        for rotulo, cab, versao_esperada, data_esperada in CABECALHOS_REAIS:
            casos += 1
            r = auditar_arquivo(_escrever(tmp, rotulo.split()[0], cab),
                                hoje=HOJE, limite_dias=365)
            if r.bloqueia:
                print(f"  TRAVOU INDEVIDAMENTE ({rotulo}): {[a['codigo'] for a in r.achados]}")
                falhas += 1
            elif versao_esperada not in (r.versao or ""):
                print(f"  FALHOU ({rotulo}): versão lida = {r.versao!r}")
                falhas += 1
            elif r.verificadoEm != data_esperada:
                print(f"  FALHOU ({rotulo}): data lida = {r.verificadoEm!r}, esperada {data_esperada}")
                falhas += 1

        # 2. Ausência de versão bloqueia.
        casos += 1
        r = auditar_arquivo(_escrever(tmp, "SEMVERSAO", "# Regimento\nTexto qualquer."),
                            hoje=HOJE, limite_dias=365)
        if "sem_versao" not in [a["codigo"] for a in r.achados]:
            print("  FALHOU: cabeçalho sem versão não foi bloqueado")
            falhas += 1

        # 3. Ausência de data bloqueia — ausência de data não é data recente.
        casos += 1
        r = auditar_arquivo(_escrever(tmp, "SEMDATA", "**Versão:** consolidada até a ER 10\n"),
                            hoje=HOJE, limite_dias=365)
        if "sem_data_verificacao" not in [a["codigo"] for a in r.achados]:
            print("  FALHOU: cabeçalho sem data de verificação não foi bloqueado")
            falhas += 1

        # 4. Verificação vencida é ressalva, não bloqueio: o arquivo não está
        #    errado, está por conferir.
        casos += 1
        r = auditar_arquivo(
            _escrever(tmp, "VENCIDO",
                      "**Versão:** consolidada até a ER 10\n**Fonte:** https://x/y\n"
                      "**Conferido em:** 2026-01-05\n## Emendas posteriores\nnenhuma"),
            hoje=HOJE, limite_dias=30)
        codigos = [a["codigo"] for a in r.achados]
        if "verificacao_vencida" not in codigos:
            print("  FALHOU: verificação vencida não foi sinalizada")
            falhas += 1
        elif r.bloqueia:
            print("  FALHOU: verificação vencida virou bloqueio (deve ser ressalva)")
            falhas += 1

        # 5. Data dentro do limite não gera ressalva de frescor.
        casos += 1
        r = auditar_arquivo(
            _escrever(tmp, "FRESCO",
                      "**Versão:** consolidada até a ER 10\n**Fonte:** https://x/y\n"
                      "**Conferido em:** 2026-07-20\n## Emendas posteriores\nnenhuma"),
            hoje=HOJE, limite_dias=30)
        if any(a["codigo"] == "verificacao_vencida" for a in r.achados):
            print("  FALHOU: regimento recente foi marcado como vencido")
            falhas += 1

    # 6. Parser de data: formatos mistos do acervo.
    for bruto, esperado in [("2026-07-23", date(2026, 7, 23)),
                            ("09/07/2026", date(2026, 7, 9)),
                            ("06 de julho de 2026", date(2026, 7, 6)),
                            ("| 2026-07-06 |", date(2026, 7, 6)),
                            ("data ilegível", None),
                            ("30/02/2026", None)]:
        casos += 1
        if _extrai_data(bruto) != esperado:
            print(f"  FALHOU: data {bruto!r} -> {_extrai_data(bruto)}, esperado {esperado}")
            falhas += 1

    if falhas:
        print(f"REGRESSÃO: {falhas} de {casos} casos falharam")
        return 1
    print(f"ok: {casos} casos de auditoria de regimento conferem "
          f"({len(CABECALHOS_REAIS)} cabeçalhos reais do acervo)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
