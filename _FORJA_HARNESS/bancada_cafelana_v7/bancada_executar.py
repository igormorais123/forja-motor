# -*- coding: utf-8 -*-
"""
bancada_executar.py — Despacha a tarefa V7 para cada participante, em isolamento.

O que esta bancada mede é potencial bruto de trabalho jurídico: mesmo dossiê,
mesmo prompt, mesma tarefa, nenhum acesso ao trabalho alheio.

Blindagens contra trapaça, por construção:

1. **Insumo idêntico e hasheado.** O prompt efetivo é `PROMPT_V7.md` + `DOSSIE.md`,
   e o SHA-256 do que foi enviado fica no META de cada execução. Insumo diferente
   invalidaria a comparação antes de qualquer julgamento.
2. **Sem ferramentas na rota de assinatura.** O Claude Code roda com `--tools ""`.
   Sem isso o modelo leria o disco, acharia a V6 no acervo e — pior — acharia as
   peças dos rivais. O isolamento não seria isolamento.
3. **Sem estado compartilhado.** Cada chamada é independente e escreve só na
   própria pasta. Nenhum participante vê saída de outro em nenhum momento.
4. **Identidade do executor conferida no envelope.** Na rota de assinatura, quem
   consumiu tokens é lido do `modelUsage`; na rota HTTP, do campo `model` da
   resposta. Provedor que entrega modelo diferente do pedido é registrado como
   divergência, não aceito em silêncio.
5. **Truncamento é registrado, não escondido.** `finish_reason` diferente de
   `stop` marca a peça como incompleta — resposta cortada não pode ser lida como
   concisão.

Uso:
    python bancada_executar.py --todos
    python bancada_executar.py --participante opus-5 [--refazer]
    python bancada_executar.py --listar
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path

BANCADA = Path(__file__).resolve().parent
FORJA = BANCADA.parent
sys.path.insert(0, str(FORJA))

from forja_modelos import (  # noqa: E402
    OPENROUTER_URL, ForjaModeloError, _segredo, modelo_remoto_proibido,
    registrar_no_ledger,
)

VERSAO = "BANCADA-CAFELANA-V7-v1"

# Teto próprio da bancada. O teto de produção da FORJA (US$ 0,50 por chamada)
# foi calibrado para consultas curtas; uma peça de vinte e tantas páginas não
# cabe nele. O teto continua existindo — é limite, não meta.
TETO_USD_POR_CHAMADA = 1.60
TETO_USD_TOTAL = 12.00
MAX_TOKENS_SAIDA = 32000


@dataclass(frozen=True)
class Participante:
    id: str
    familia: str
    rota: str                # assinatura | openrouter
    endereco: str            # alias do CLI ou id no provedor
    canonico: str            # id canônico esperado no envelope
    usd_entrada_por_milhao: float = 0.0
    usd_saida_por_milhao: float = 0.0
    nota: str = ""


PARTICIPANTES: dict[str, Participante] = {
    # O endereço é o id canônico, NÃO o alias curto: `--model opus` resolveu
    # para `claude-opus-4-8` nesta instalação, e a primeira execução da bancada
    # foi feita pelo modelo errado. O gate de identidade pegou; a execução
    # equivocada está preservada em `execucao_descartadas/`. Alias curto é
    # conveniência de sessão interativa e não serve para medição.
    "opus-5": Participante(
        "opus-5", "anthropic", "assinatura", "claude-opus-5", "claude-opus-5",
        nota="assinatura Claude Max; custo marginal zero"),
    "fable-5": Participante(
        "fable-5", "anthropic", "assinatura", "fable", "claude-fable-5",
        nota="assinatura Claude Max; custo marginal zero"),
    "sol-5.6": Participante(
        "sol-5.6", "openai", "openrouter", "openai/gpt-5.6-sol", "openai/gpt-5.6-sol",
        5.0, 30.0, nota="revisor adversarial de produção da FORJA"),
    "luna-5.6": Participante(
        "luna-5.6", "openai", "openrouter", "openai/gpt-5.6-luna", "openai/gpt-5.6-luna",
        1.0, 6.0, nota="fora do registro de produção; entra a pedido do titular"),
    "grok-4.5": Participante(
        "grok-4.5", "xai", "openrouter", "x-ai/grok-4.5", "x-ai/grok-4.5",
        2.0, 6.0, nota="red team de produção da FORJA"),
    "kimi-k3": Participante(
        "kimi-k3", "moonshot", "openrouter", "moonshotai/kimi-k3", "moonshotai/kimi-k3",
        3.0, 15.0,
        nota="RETIRADO do registro de produção em 26/07/2026 por decisão do titular, "
             "após reprovar a bancada jurídica; participa aqui apenas para efeito "
             "comparativo, e o resultado não reabre a decisão por si só"),
}


def prompt_efetivo() -> tuple[str, dict]:
    tarefa = (BANCADA / "protocolo" / "PROMPT_V7.md").read_text(encoding="utf-8")
    dossie = (BANCADA / "protocolo" / "DOSSIE.md").read_text(encoding="utf-8")
    texto = f"{tarefa}\n\n{'=' * 78}\n# DOSSIÊ\n{'=' * 78}\n\n{dossie}"
    marcas = {
        "sha256Prompt": hashlib.sha256(texto.encode("utf-8")).hexdigest(),
        "sha256Tarefa": hashlib.sha256(tarefa.encode("utf-8")).hexdigest(),
        "sha256Dossie": hashlib.sha256(dossie.encode("utf-8")).hexdigest(),
        "caracteres": len(texto),
    }
    return texto, marcas


def _custo(p: Participante, entrada: int, saida: int) -> float:
    return (entrada * p.usd_entrada_por_milhao + saida * p.usd_saida_por_milhao) / 1_000_000


def _via_openrouter(p: Participante, prompt: str, timeout: int) -> dict:
    if modelo_remoto_proibido(p.endereco):
        raise ForjaModeloError(f"{p.id}: modelo vedado por decisão do titular")
    corpo = json.dumps({
        "model": p.endereco,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": MAX_TOKENS_SAIDA,
    }, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(OPENROUTER_URL, data=corpo, method="POST")
    req.add_header("Authorization", f"Bearer {_segredo('OPENROUTER_API_KEY')}")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resposta:
            payload = json.loads(resposta.read().decode("utf-8"))
    except urllib.error.HTTPError as erro:
        detalhe = erro.read().decode("utf-8", "replace")[:400]
        raise ForjaModeloError(f"HTTP {erro.code} do provedor: {detalhe}") from None
    except OSError as erro:
        raise ForjaModeloError(f"falha de rede: {erro}") from None

    escolha = (payload.get("choices") or [{}])[0]
    uso = payload.get("usage") or {}
    reportado = str(payload.get("model") or "")
    if modelo_remoto_proibido(reportado):
        raise ForjaModeloError(f"{p.id}: provedor reportou modelo vedado")
    return {
        "texto": str((escolha.get("message") or {}).get("content") or ""),
        "finishReason": escolha.get("finish_reason"),
        "tokensEntrada": int(uso.get("prompt_tokens") or 0),
        "tokensSaida": int(uso.get("completion_tokens") or 0),
        "tokensRaciocinio": int((uso.get("completion_tokens_details") or {})
                                .get("reasoning_tokens") or 0),
        "modeloReportado": reportado,
    }


def _via_assinatura(p: Participante, prompt: str, timeout: int) -> dict:
    """Rota da assinatura, capturada por stream.

    O `--output-format json` devolve, em `result`, apenas o ÚLTIMO turno. Uma
    peça longa atravessa mais de um turno, e o resultado veio começando no meio
    de uma palavra: 10 KB do que eram 36 mil tokens de saída. Isso mediria o
    harness, não o modelo. O stream traz todos os blocos de texto, na ordem, e
    a concatenação reconstrói a resposta inteira.
    """
    import shutil, subprocess                                    # noqa: PLC0415

    executavel = shutil.which("claude.cmd") or shutil.which("claude")
    if not executavel:
        raise ForjaModeloError("Claude Code não foi localizado no PATH")
    # Mesma exigência da produção: assinatura Max, nunca chave de API.
    checagem = subprocess.run(
        [executavel, "auth", "status"], cwd=str(FORJA.parent), capture_output=True,
        text=True, encoding="utf-8", errors="replace", timeout=30, shell=False)
    try:
        auth = json.loads(checagem.stdout) if checagem.returncode == 0 else {}
    except json.JSONDecodeError:
        auth = {}
    if not (auth.get("loggedIn") is True and auth.get("authMethod") == "claude.ai"
            and auth.get("subscriptionType") == "max"):
        raise ForjaModeloError("Claude Code não está autenticado pela assinatura Max")

    proc = subprocess.run(
        [executavel, "-p", "--model", p.endereco, "--output-format", "stream-json",
         "--verbose", "--permission-mode", "dontAsk", "--tools", ""],
        input=prompt, cwd=str(FORJA.parent), capture_output=True, text=True,
        encoding="utf-8", errors="replace", timeout=timeout, shell=False,
    )
    if proc.returncode != 0:
        raise ForjaModeloError(f"executor falhou (exit {proc.returncode}): {proc.stderr[-600:]}")

    partes, entrada, saida, modelos, erro = [], 0, 0, set(), None
    for linha in proc.stdout.splitlines():
        linha = linha.strip()
        if not linha:
            continue
        try:
            evento = json.loads(linha)
        except json.JSONDecodeError:
            continue
        tipo = evento.get("type")
        if tipo == "assistant":
            msg = evento.get("message") or {}
            if msg.get("model"):
                modelos.add(str(msg["model"]))
            for bloco in msg.get("content") or []:
                if bloco.get("type") == "text" and bloco.get("text"):
                    partes.append(str(bloco["text"]))
            uso = msg.get("usage") or {}
            entrada += int(uso.get("input_tokens") or 0)
            saida += int(uso.get("output_tokens") or 0)
        elif tipo == "result":
            if evento.get("is_error"):
                erro = str(evento.get("result"))[:300]
            # O `modelUsage` do evento final é o total da execução e tem
            # precedência sobre a soma dos chunks: somar por mensagem devolveu
            # 2 tokens de saída para uma peça de 12 mil palavras, porque os
            # eventos intermediários trazem contagem parcial ou zerada. Número
            # obviamente impossível ainda é número errado no relatório.
            totais = evento.get("modelUsage") or {}
            if totais:
                entrada_total = sum(int(d.get("inputTokens") or 0)
                                    for d in totais.values() if isinstance(d, dict))
                saida_total = sum(int(d.get("outputTokens") or 0)
                                  for d in totais.values() if isinstance(d, dict))
                entrada = entrada_total or entrada
                saida = saida_total or saida
            modelos.update(str(nome) for nome in totais)
    if erro:
        raise ForjaModeloError(f"o executor reportou erro: {erro}")

    return {
        "texto": "".join(partes),
        "finishReason": "stop",
        "tokensEntrada": entrada,
        "tokensSaida": saida,
        "tokensRaciocinio": 0,
        "modeloReportado": ";".join(sorted(modelos)),
        "auth": auth,
        "turnosAssistente": len(partes),
    }


def executar(p: Participante, *, timeout: int, refazer: bool) -> dict:
    destino = BANCADA / "execucao" / p.id
    destino.mkdir(parents=True, exist_ok=True)
    saida_md = destino / "SAIDA.md"
    if saida_md.is_file() and not refazer:
        print(f"  [pula] {p.id}: já executado ({saida_md.stat().st_size / 1024:.0f} KB)")
        return json.loads((destino / "META.json").read_text(encoding="utf-8"))

    prompt, marcas = prompt_efetivo()
    teto = _custo(p, len(prompt) // 3, MAX_TOKENS_SAIDA)
    if p.rota == "openrouter" and teto > TETO_USD_POR_CHAMADA:
        raise ForjaModeloError(
            f"{p.id}: custo máximo estimado US$ {teto:.2f} acima do teto de "
            f"US$ {TETO_USD_POR_CHAMADA:.2f} por chamada")

    print(f"  [roda] {p.id} ({p.rota}) — teto estimado US$ {teto:.2f}")
    inicio = time.monotonic()
    bruto = (_via_assinatura if p.rota == "assinatura" else _via_openrouter)(p, prompt, timeout)
    decorrido = round(time.monotonic() - inicio, 1)

    texto = bruto["texto"]
    if not texto.strip():
        raise ForjaModeloError(
            f"{p.id}: resposta vazia após {bruto['tokensRaciocinio']} tokens de raciocínio")

    custo = round(_custo(p, bruto["tokensEntrada"], bruto["tokensSaida"]), 4)
    divergencia = (p.canonico.casefold() not in (bruto["modeloReportado"] or "").casefold()
                   and bruto["modeloReportado"] != "")
    meta = {
        "versao": VERSAO,
        "participante": asdict(p),
        "em": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "insumo": marcas,
        "sha256Saida": hashlib.sha256(texto.encode("utf-8")).hexdigest(),
        "caracteresSaida": len(texto),
        "palavrasSaida": len(texto.split()),
        "segundos": decorrido,
        "custoUsd": custo,
        "tokensEntrada": bruto["tokensEntrada"],
        "tokensSaida": bruto["tokensSaida"],
        "tokensRaciocinio": bruto["tokensRaciocinio"],
        "finishReason": bruto.get("finishReason"),
        "truncada": bruto.get("finishReason") not in (None, "stop", "end_turn"),
        "modeloReportado": bruto["modeloReportado"],
        "identidadeDivergente": divergencia,
        "auth": bruto.get("auth"),
    }
    saida_md.write_text(texto, encoding="utf-8")
    (destino / "META.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    registrar_no_ledger({
        "modelo": p.id, "familia": p.familia, "provedor": p.rota,
        "fase": "BANCADA_V7", "papel": "participante",
        "tokensEntrada": bruto["tokensEntrada"], "tokensSaida": bruto["tokensSaida"],
        "tokensRaciocinio": bruto["tokensRaciocinio"], "custoUsd": custo,
        "segundos": decorrido, "conteudo": texto,
        "em": meta["em"],
    })
    marca = " TRUNCADA" if meta["truncada"] else ""
    aviso = " IDENTIDADE DIVERGENTE" if divergencia else ""
    print(f"  [ok]   {p.id}: {meta['palavrasSaida']} palavras · {decorrido}s · "
          f"US$ {custo:.3f}{marca}{aviso}")
    return meta


def main() -> int:
    ap = argparse.ArgumentParser(description="bancada Cafelana V7")
    ap.add_argument("--todos", action="store_true")
    ap.add_argument("--participante", action="append", default=[])
    ap.add_argument("--refazer", action="store_true")
    ap.add_argument("--listar", action="store_true")
    ap.add_argument("--timeout", type=int, default=1800)
    args = ap.parse_args()

    if args.listar:
        for p in PARTICIPANTES.values():
            print(f"  {p.id:<10} {p.familia:<10} {p.rota:<11} {p.endereco:<24} {p.nota}")
        return 0

    alvos = ([PARTICIPANTES[i] for i in args.participante] if args.participante
             else list(PARTICIPANTES.values()) if args.todos else [])
    if not alvos:
        ap.error("informe --todos ou --participante ID")

    print(f"BANCADA CAFELANA V7 — {len(alvos)} participante(s)")
    _, marcas = prompt_efetivo()
    print(f"  insumo: {marcas['caracteres'] / 1024:.0f} KB · "
          f"sha256 {marcas['sha256Prompt'][:16]}")
    gasto, falhas = 0.0, []
    for p in alvos:
        try:
            meta = executar(p, timeout=args.timeout, refazer=args.refazer)
            gasto += float(meta.get("custoUsd") or 0.0)
        except Exception as erro:                      # noqa: BLE001
            print(f"  [FALHA] {p.id}: {erro}")
            falhas.append(p.id)
        if gasto > TETO_USD_TOTAL:
            print(f"  [PARA] teto total de US$ {TETO_USD_TOTAL:.2f} atingido")
            break
    print(f"\n  gasto acumulado nesta execução: US$ {gasto:.3f}")
    if falhas:
        print(f"  falharam: {', '.join(falhas)}")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    raise SystemExit(main())
