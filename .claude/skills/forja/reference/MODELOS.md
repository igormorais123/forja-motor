# MODELOS — quem roda o quê, e o que é proibido

> Ordem do Igor, 06/08/2026, com o painel curto de 07/08/2026. A allowlist executável é
> `forja_modelos.py`; **modelo fora dela não executa**, e é assim de propósito.

## Índice

- [O quadro](#o-quadro)
- [Proibidos, e por quê](#proibidos-e-por-quê)
- [Revisão cruzada entre famílias](#revisão-cruzada-entre-famílias)
- [Vozes curtas](#vozes-curtas)
- [Como se mede se uma voz merece ficar](#como-se-mede-se-uma-voz-merece-ficar)
- [Fonte desatualizada que já enganou](#fonte-desatualizada-que-já-enganou)

## O quadro

| Papel | Modelo | Rota | Onde |
|---|---|---|---|
| Loop principal, redação, auditoria | Claude Opus 5 | assinatura Claude Max | todas as fases |
| Revisão editorial (F7-B) | `claude-opus-5` | OAuth da assinatura, **sem API key** | F7-B |
| Codex — produção | **`gpt-5.6-luna`**, esforço `max` | CLI Codex | quando a esteira produz pelo Codex |
| Codex — **revisão** | **`gpt-5.6-sol`**, esforço `high` | `forja_revisao_cruzada.py` | revisão cruzada, red team, auditoria |
| Diabob (contraditório) | **Grok 4.5** | assinatura **do Cursor** (`grok-4.5-cursor`) | F4 e F7 |
| Triagem semântica | Grok 4.5 | mesma rota | F1 |
| Vozes curtas (opcional) | Kimi K3, GLM 5.2 | assinatura do Cursor | F4 e F7 |

**O Codex tem dois postos, e a ordem de revisão é a mais recente (10/08/2026).** Ela
supera a de 06/08 só na parte de revisão; produção continua no `luna`. Revisor e produtor
não podem coincidir — é isso que o gate `cross_model_review_verified` protege.

Não chame o Codex à mão para revisar: `forja_revisao_cruzada.py` fecha no código quatro
armadilhas que já custaram tempo — `--cd` explícito (sem ele o Codex responde que o
sandbox bloqueou a leitura, e o parecer sai sem fonte), MCPs desligados, sandbox somente
leitura e prompt por **argumento**. **No Cursor é o inverso**: lá o prompt vai por stdin,
porque o wrapper `.cmd` faz o cmd.exe cortar o argumento na primeira quebra de linha.

A rota do Grok é **sempre** a assinatura do Cursor. O OpenRouter cobra por chamada e
**não é automático**: se a assinatura falhar, o comando falha alto com a instrução de
conserto, e a reserva paga só entra com `--permitir-reserva`. **Gasto novo é decisão do
titular, não consequência de um login vencido.**

## Proibidos, e por quê

| Proibido | Desde | Travado em |
|---|---|---|
| **GPT-5.5** — em nenhuma fase, papel ou justificativa | 06/08/2026 | `forja_modelos.modelo_remoto_proibido` |
| **Kimi K2** | 26/07/2026 | idem |

Não são preferências: são travas. Um modelo proibido não roda mesmo que alguém escreva o
nome no comando.

## Revisão cruzada entre famílias

O trabalho nasce numa família e é revisado por **outra**. Três famílias hoje: Claude,
OpenAI e Grok. O gate recompõe `familyAssurance` a partir do que de fato rodou; não
aceita declaração. Detalhe em
[INVARIANTES.md](INVARIANTES.md#revisão-cruzada-entre-famílias).

**Quando a outra família cai, declare a degradação.** O Codex CLI já falhou no Windows
com `CreateProcessAsUserW failed: 5 (Acesso negado)` e o caso seguiu por outra rota da
mesma assinatura, com o motivo escrito no commit. Rebaixar é permitido; silenciar não.

## Vozes curtas

*07/08/2026 — ordem do Igor.*

Kimi K3 (`kimi-k3-cursor`) e GLM 5.2 (`glm-5.2-cursor`) entram como **opinião lateral
curta**, opcional em F4 e F7, por `forja_painel_curto.py`: no máximo 4 observações de 300
caracteres por voz, com os tetos cortados **no código**, não pedidos no prompt.

Não é gate — Helena, Cícero e Diabob continuam sendo. E **não é fonte**: nada daqui vira
fundamento, citação, número ou data.

O K3 carrega a restrição `nao_afirma_fato` porque a bancada de 26/07 mediu **0 de 6
corretas** na condição solta, com 4 invenções. O GLM não carrega restrição porque **nunca
foi aferido — o que não é o mesmo que ter sido aprovado.**

## Como se mede se uma voz merece ficar

Por `forja_contribuicao.py`, não por impressão. Vereditos de vocabulário fechado;
`duplicada` conta no denominador sem somar, de modo que quem só concorda tira zero; nada
é elegível abaixo de **12 observações e 3 casos distintos**; e `amostra` abre o texto real
antes de decidir, porque **contar não é ler**.

A escada é `observador → consultivo → candidato`, sem pular degrau e sempre com
`--aprovado-por`.

**O placar de contribuição não revoga a bancada de fidelidade à fonte**: são réguas de
coisas diferentes. Uma voz pode contribuir muito e continuar proibida de afirmar fato.

## Fonte desatualizada que já enganou

A skill global `codex-integrado` traz tabelas com `gpt-5.5` e `gpt-5.5-mini`. **Elas não
valem aqui**, e copiá-las sem conferir já produziu rótulo errado em documento da fábrica.
Quando uma fonte externa nomear modelo, confira contra `forja_modelos.py` antes de
escrever.
