# -*- coding: utf-8 -*-
"""forja_gate_anexo_saida.py — nenhum documento sai fora do padrão da casa.

Por que existe. Em 06/08/2026 dois documentos foram redigidos fora da esteira,
ficaram fora do padrão Word do escritório nas três dimensões e seguiram para o
cliente. A varredura tipográfica os viu — mas ela é **laudo**, não barreira:
mede o acervo depois do fato e reprova um baseline que ninguém consulta antes
de enviar. Entre medir e impedir há a distância que separa relatório de gate.

Onde ele fica. Não adianta instalar a barreira na produção: quem redige fora da
FORJA nunca passa por lá. O único ponto por onde um documento efetivamente sai
sob controle nosso é o disparo de rascunho — `enviar_rascunho`, que despachava
o que estivesse anexado ao rascunho do Gmail sem olhar uma única vez. O
`enviar_email` não tem anexo nenhum, então não há o que conferir ali.

O critério. Reprova quem falha nas **três** dimensões ao mesmo tempo:
justificação, corpo 12 pt e Times New Roman. Uma dimensão isolada pode ser
anexo legítimo — quadro, índice, planilha convertida —, e barrar por ela viraria
obstáculo diário. As três juntas são a assinatura de documento que não passou
pela diagramação da casa, e é essa a frase que o escritório já usa.

A saída de emergência é explícita e fica registrada: material redigido por
terceiro que precise ser encaminhado passa quando declarado nominalmente. Sem a
declaração, não passa — e o motivo vem com os três números medidos, para quem
receber o bloqueio saber o que corrigir sem abrir o arquivo.

Uso:
    python forja_gate_anexo_saida.py <arquivo.docx> [...]
"""
from __future__ import annotations

import sys
from pathlib import Path

# Um documento curto não é peça: é índice, capa, anexo de uma página. Medir
# cobertura tipográfica sobre poucos parágrafos produz veredito instável.
PISO_PARAGRAFOS = 20

# Os mesmos limiares da varredura do acervo. Repeti-los com outro valor faria a
# barreira e o laudo discordarem sobre o que é o padrão da casa.
PISO_JUSTIFICACAO = 0.50
PISO_TAMANHO = 0.90
PISO_FONTE = 0.90

EXTENSOES = {".docx", ".doc"}


def _falha_nas_tres(m: dict) -> bool:
    return (m["justificacao"] < PISO_JUSTIFICACAO
            and m["tamanho"] < PISO_TAMANHO
            and m["fonte"] < PISO_FONTE)


def medir(caminho: Path | str, *, motivos: list | None = None) -> dict | None:
    """Medida tipográfica de um DOCX. `None` quando não há o que julgar.

    Devolver `None` em vez de reprovar é deliberado: arquivo ilegível, curto
    demais ou de outro formato não é prova de desvio, e transformar ausência de
    medida em bloqueio faria a barreira reprovar por cegueira.

    `motivos`, quando passado, recebe a causa de cada `None`. As três não pedem
    a mesma providência — documento curto é anexo comum, ilegível pode ser
    corrupção de transporte, e formato inesperado costuma ser engano de quem
    anexou —, e um ledger que só diz "não inspecionado" obriga a abrir o arquivo
    para descobrir qual delas era.
    """
    caminho = Path(caminho)

    def _sem_medida(causa):
        if motivos is not None:
            motivos.append({"arquivo": caminho.name, "motivo": causa})
        return None

    if caminho.suffix.lower() not in EXTENSOES:
        return _sem_medida("não é documento do Word")
    try:
        from forja_docx_layout import audit_docx_layout
        laudo = audit_docx_layout(caminho)
    except Exception as erro:  # noqa: BLE001
        return _sem_medida(f"não abriu ({type(erro).__name__})")
    m = laudo.get("metrics") or {}
    paragrafos = m.get("bodyParagraphs") or 0
    if paragrafos < PISO_PARAGRAFOS:
        return _sem_medida(f"curto demais para medir ({paragrafos} parágrafos)")
    return {
        "arquivo": caminho.name,
        "paragrafos": paragrafos,
        "justificacao": round(m.get("justificationCoverage", 0), 4),
        "tamanho": round(m.get("sizeCoverage", 0), 4),
        "fonte": round(m.get("fontCoverage", 0), 4),
    }


def avaliar(caminhos, *, material_de_terceiro=None) -> dict:
    """Veredito sobre um conjunto de anexos prestes a sair.

    `material_de_terceiro` é a lista de nomes de arquivo que o remetente declara
    como redigidos fora do escritório. A declaração é nominal de propósito: uma
    flag booleana liberaria o lote inteiro, e é justamente o documento que
    ninguém olhou que se esconde num lote liberado em bloco.
    """
    declarados = {str(n).strip().casefold() for n in (material_de_terceiro or [])}
    medidos, bloqueados, liberados, cegos = [], [], [], []
    for caminho in caminhos:
        # O arquivo que se anuncia como documento do Word e não produz medida é
        # ponto cego: não barra — ausência de medida nunca foi prova de desvio —
        # mas precisa aparecer, senão a barreira parece mais completa do que é.
        # Descoberto ao testar base64 corrompido, que **não** levanta exceção:
        # decodifica em lixo, e o anexo sumia em silêncio.
        motivos = []
        m = medir(caminho, motivos=motivos)
        if m is None:
            cegos.extend(x for x in motivos
                         if Path(caminho).suffix.lower() in EXTENSOES)
            continue
        medidos.append(m)
        if not _falha_nas_tres(m):
            continue
        if m["arquivo"].casefold() in declarados:
            liberados.append(m)
        else:
            bloqueados.append(m)
    return {"medidos": medidos, "bloqueados": bloqueados,
            "liberadosPorDeclaracao": liberados, "naoInspecionados": cegos,
            "aprovado": not bloqueados}


def explicar(veredito: dict) -> str:
    """Mensagem de bloqueio: o que reprovou, com que números, e como seguir."""
    linhas = ["Envio barrado: anexo fora do padrão Word do escritório nas três "
              "dimensões — justificação, corpo 12 pt e Times New Roman."]
    for m in veredito["bloqueados"]:
        linhas.append(
            f"  {m['arquivo']} — justificação {m['justificacao']:.0%}, "
            f"tamanho {m['tamanho']:.0%}, fonte {m['fonte']:.0%} "
            f"({m['paragrafos']} parágrafos)")
    linhas.append("Aplique a diagramação da casa antes de enviar. Se o documento "
                  "foi redigido fora do escritório e precisa ser encaminhado como "
                  "veio, declare-o nominalmente em `material_de_terceiro`.")
    return "\n".join(linhas)


def _partes(payload: dict):
    """Percorre a árvore MIME do rascunho. Anexo pode estar em qualquer nível."""
    if not isinstance(payload, dict):
        return
    yield payload
    for parte in payload.get("parts") or []:
        yield from _partes(parte)


def avaliar_rascunho(svc, draft_id: str, *, material_de_terceiro=None) -> dict:
    """Baixa os anexos de um rascunho do Gmail e julga cada um.

    O download é necessário: o Gmail entrega nome e id do anexo no rascunho, mas
    a medida tipográfica precisa do arquivo. Os bytes vão para um temporário que
    é apagado na saída — documento de cliente não fica em disco por causa de uma
    conferência.
    """
    import base64
    import tempfile

    det = svc.users().drafts().get(userId="me", id=draft_id, format="full").execute()
    msg = det.get("message") or {}
    mensagem_id = msg.get("id")

    nao_inspecionados = []
    with tempfile.TemporaryDirectory() as tmp:
        caminhos = []
        for parte in _partes(msg.get("payload") or {}):
            nome = parte.get("filename") or ""
            if Path(nome).suffix.lower() not in EXTENSOES:
                continue
            # Um anexo que não se consegue baixar ou decodificar não pode
            # derrubar a conferência dos outros: a exceção subiria e barraria o
            # envio inteiro por um defeito de transporte, não de conteúdo. Ele
            # também não pode sumir em silêncio, porque aí a barreira passaria a
            # ter um ponto cego que ninguém enxerga. Fica declarado.
            try:
                corpo = parte.get("body") or {}
                ident = corpo.get("attachmentId")
                dados = corpo.get("data")
                if ident and not dados:
                    anexo = svc.users().messages().attachments().get(
                        userId="me", messageId=mensagem_id, id=ident).execute()
                    dados = anexo.get("data")
                if not dados:
                    continue
                # `Path(nome).name` descarta qualquer diretório vindo no campo
                # `filename`, que é texto controlado por quem montou a mensagem.
                destino = Path(tmp) / Path(nome).name
                destino.write_bytes(base64.urlsafe_b64decode(dados))
            except Exception as erro:  # noqa: BLE001
                nao_inspecionados.append(
                    {"arquivo": Path(nome).name, "motivo": f"{type(erro).__name__}"})
                continue
            caminhos.append(destino)
        veredito = avaliar(caminhos, material_de_terceiro=material_de_terceiro)
    veredito["draftId"] = draft_id
    veredito["anexosDocx"] = len(veredito["medidos"])
    veredito["naoInspecionados"] = nao_inspecionados + veredito["naoInspecionados"]
    return veredito


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if not argv:
        print("uso: python forja_gate_anexo_saida.py <arquivo.docx> [...]")
        return 2
    veredito = avaliar([Path(a) for a in argv])
    for m in veredito["medidos"]:
        marca = "REPROVA" if _falha_nas_tres(m) else "ok     "
        print(f"  {marca}  {m['arquivo'][:56]:58} "
              f"just {m['justificacao']:.0%}  tam {m['tamanho']:.0%}  fonte {m['fonte']:.0%}")
    for c in veredito["naoInspecionados"]:
        print(f"  cego     {c['arquivo'][:56]:58} {c['motivo']}")
    if not veredito["medidos"]:
        print("nenhum documento mensurável entre os arquivos informados.")
        return 0
    if veredito["aprovado"]:
        print(f"APROVADO — {len(veredito['medidos'])} anexo(s) dentro do padrão da casa.")
        return 0
    print(explicar(veredito))
    return 1


if __name__ == "__main__":
    sys.exit(main())
