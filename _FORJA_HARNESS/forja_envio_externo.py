"""Porteiro do que sai da máquina: classe do documento e trilha do envio.

Achado do revisor externo em 09/08/2026, e é o mais sério que a revisão do
painel produziu: **o painel mandava trechos de documento de cliente para cinco
rotas externas sem gate nenhum.** Sem classificação, sem confirmação, sem
registro do que saiu. A conversa toda girava em torno de qual modelo é melhor
enquanto ninguém sabia dizer que material tinha atravessado a porta.

Este módulo não impede o uso legítimo. Ele faz três coisas que não existiam:

1. **Exige a classe do documento.** Produto nosso — blueprint, rascunho, peça em
   redação — pode ir para crítica externa; é para isso que existe a segunda
   opinião. **Documento dos autos não vai**, e isso é recusa dura, não aviso.
   A diferença não é de sensibilidade abstrata: o nosso texto é nosso para
   arriscar, o do processo não é.
2. **Exige confirmação explícita.** Enviar material de cliente a provedor de
   fora é decisão, não efeito colateral de rodar um comando.
3. **Registra o que saiu.** Data, caso, arquivo, hash, quantos caracteres, para
   quais modelos e por qual provedor. Sem isso não há como responder à pergunta
   que uma auditoria faria primeiro: o que exatamente foi exposto, e quando.

O ledger guarda **hash e tamanho, nunca o texto** — a mesma disciplina do resto
da casa. Ele serve para reconstituir a exposição, não para duplicá-la.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

FORJA = Path(__file__).resolve().parent
LEDGER = FORJA / "telemetria" / "ENVIOS_EXTERNOS.jsonl"
VERSAO = "FORJA-ENVIO-EXTERNO-v1"

# Vocabulário fechado. "Sensível" e "confidencial" seriam adjetivos discutíveis
# a cada uso; o que decide aqui é a ORIGEM do texto, que é um fato.
CLASSES = {
    "produto_proprio": (
        "texto que a fábrica escreveu — blueprint, rascunho, peça em redação, "
        "relatório interno. Pode ir para crítica externa."),
    "autos": (
        "peça, decisão, laudo ou documento juntado ao processo, de qualquer "
        "parte. NÃO sai da máquina."),
    "misto": (
        "produto nosso com transcrição extensa dos autos embutida. NÃO sai: "
        "separe antes o que é nosso."),
}
PERMITIDAS = {"produto_proprio"}


class EnvioBloqueado(RuntimeError):
    pass


def _agora() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def autorizar(texto: str, *, classe: str, confirmado: bool,
              destino: list[str], caso: str | None = None,
              arquivo: str | None = None, provedor: str = "cursor") -> dict:
    """Decide se o texto pode sair e registra a saída. Levanta se não pode.

    Devolve o recibo do envio, que o artefato do painel guarda — para que a
    pergunta "isto saiu daqui?" tenha resposta no próprio artefato, e não só num
    ledger que alguém precisa lembrar de abrir.
    """
    if classe not in CLASSES:
        raise EnvioBloqueado(
            f"classe {classe!r} não existe. Declare uma de: {', '.join(CLASSES)}")
    if classe not in PERMITIDAS:
        raise EnvioBloqueado(
            f"envio bloqueado: {classe} — {CLASSES[classe]}\n"
            "Produto nosso é nosso para arriscar numa crítica externa; documento "
            "do processo não é. Se o que você quer criticar é a nossa peça, "
            "aponte para o rascunho, não para os autos.")
    if not confirmado:
        raise EnvioBloqueado(
            "envio externo não confirmado. Estes primeiros caracteres vão para "
            f"provedor de fora ({provedor}), em {len(destino)} modelo(s). "
            "Passe --confirmo-envio-externo para assumir a decisão; ela fica "
            "registrada em telemetria/ENVIOS_EXTERNOS.jsonl.")

    recibo = {
        "contrato": VERSAO,
        "em": _agora(),
        "caso": caso,
        "arquivo": arquivo,
        "classe": classe,
        # Hash e tamanho, nunca o texto: o ledger reconstitui a exposição, não
        # a duplica.
        "sha256": hashlib.sha256(texto.encode("utf-8")).hexdigest(),
        "caracteresEnviados": len(texto),
        "provedor": provedor,
        "modelos": sorted(destino),
    }
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER.open("a", encoding="utf-8") as arq:
        arq.write(json.dumps(recibo, ensure_ascii=False) + "\n")
    return recibo


def historico(limite: int = 20) -> list[dict]:
    """O que já saiu, do mais recente para o mais antigo."""
    if not LEDGER.is_file():
        return []
    linhas = []
    for linha in LEDGER.read_text(encoding="utf-8").splitlines():
        try:
            linhas.append(json.loads(linha))
        except ValueError:
            continue
    return list(reversed(linhas))[:limite]


def main(argv=None) -> int:
    import argparse

    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--limite", type=int, default=20)
    ap.add_argument("--classes", action="store_true",
                    help="mostra o vocabulário de classes")
    args = ap.parse_args(argv)

    if args.classes:
        for nome, texto in CLASSES.items():
            marca = "PODE SAIR" if nome in PERMITIDAS else "BLOQUEADA"
            print(f"{nome:<18} [{marca}]  {texto}")
        return 0

    envios = historico(args.limite)
    if not envios:
        print("nenhum envio externo registrado")
        return 0
    print(f"{'quando':<26} {'caso':<16} {'classe':<17} {'chars':>7}  modelos")
    for e in envios:
        print(f"{e['em']:<26} {str(e.get('caso') or '-'):<16} {e['classe']:<17} "
              f"{e['caracteresEnviados']:>7}  {', '.join(e['modelos'])}")
    print(f"\n{len(envios)} envio(s). Hash e tamanho registrados; o texto não.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
