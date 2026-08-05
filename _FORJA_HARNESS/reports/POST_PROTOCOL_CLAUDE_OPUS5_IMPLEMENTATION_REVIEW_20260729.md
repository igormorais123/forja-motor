# Revisão adversarial da implementação — loop pós-protocolo

- Data: 2026-07-29
- Revisor solicitado: Claude Code, modelo `claude-opus-5`
- Veredito inicial: `REJECT`
- Escopo: implementação executável, contratos, comparação documental, captura Gmail, aprendizado e loop arquitetural

## Bloqueios críticos encontrados

1. A captura podia gravar o índice antes dos demais artefatos e tornar uma falha intermediária irrecuperável por nova tentativa.
2. Falha de OCR interrompia a varredura sem registrar bloqueio persistente nem continuar para as outras mensagens.
3. O backfill do Gmail podia sobrescrever F9/F10 reais com uma síntese que aparentava aprovação inexistente.
4. A verificação de protocolo aceitava assinatura eletrônica ou vínculo incompleto como prova suficiente.
5. A checagem de vazamento no Git não neutralizava `core.quotepath`, podendo deixar escapar caminhos acentuados.
6. A chave de desligamento protegia apenas a varredura, não as demais entradas de mutação.
7. O avaliador arquitetural não comparava baseline e candidato em checkout isolado.

## Correções altas e médias exigidas

- Normalizar timestamps e exigir `deliveredAt` explícito.
- Dar precedência absoluta a recibos/comprovantes na separação de anexos.
- Tratar polaridade, quantificadores e conteúdo incerto como mudança material.
- Classificar cada alteração real separadamente, usando o agrupamento apenas como localização.
- Falhar fechado quando uma demanda aponta para mais de um caso.
- Preservar decisões de revisão durante rebuild.
- Exigir evidências distintas e testes realmente executados antes de promoção.
- Aplicar allowlist de remetentes antes de baixar anexos.
- Rejeitar texto jurídico bruto nos artefatos rastreados.
- Tornar o cálculo de similaridade limitado.
- Separar corpo de cabeçalhos/rodapés em comparações DOCX.
- Persistir timeouts e validar o manifesto do loop arquitetural.
- Tirar nomes de anexos do relatório operacional rastreado.
- Manter uma única fonte para camadas, causas e impactos.

## Regra de aceite adotada

O sistema só será considerado concluído depois de:

1. cada achado acima ter teste de regressão;
2. o piloto real ser reprocessado sem sobrescrever os F9/F10 originais;
3. a automação desligada durante a correção voltar a ficar ativa apenas após a suíte verde;
4. uma nova revisão do mesmo modelo não registrar achado crítico ou alto aberto.
