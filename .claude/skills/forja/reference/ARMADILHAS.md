# ARMADILHAS — o que já deu errado, e como

> Nenhuma peça da fábrica saiu protocolável na v1. **30% a 40% do tempo é auditoria, e
> isso é o padrão, não falha.** Cada item aqui tem um caso real atrás; o histórico
> completo está em `_FORJA_HARNESS/RETROSPECTIVAS.md`, que hoje passa de 290 lições.

## Índice

- [Os quatro erros que se repetiram](#os-quatro-erros-que-se-repetiram)
- [Citação: seis modos de falha, não um](#citação-seis-modos-de-falha-não-um)
- [Bloqueio declarado não é bloqueio testado](#bloqueio-declarado-não-é-bloqueio-testado)
- [Achado forte gera excesso na redação](#achado-forte-gera-excesso-na-redação)
- [Gate, documento e quem se autovalida](#gate-documento-e-quem-se-autovalida)
- [Armadilhas de máquina](#armadilhas-de-máquina)

## Os quatro erros que se repetiram

**1. Jurisprudência com atribuição errada.** Frase real atribuída ao precedente errado;
nota de rodapé não localizável. Verifique **cada** citação na fonte — nunca a memória do
modelo.

**2. Premissa não declarada.** Data de intimação assumida, prazo contado com sábado como
dia útil, OCR não confirmado. Premissa sem prova vira `[VERIFICAR]` com bloqueador
nominado. Red team simulando a parte contrária antes do protocolo.

**3. Placeholder esquecido no PDF final.** `[NOME]`, `[CRC-UF]`, `[dia]`. Bloqueador P0 —
`G2-placeholder` mais busca por `[` no texto final e inspeção visual.

**4. Diagramação quebrada que só aparece no render.** Texto estourando borda, legenda
cortada, rodapé colidido. **O QA página a página é o único detector** — nunca declarar
pronto sem ele. E ele falha também: numa entrega de 08/08/2026 aprovou um rótulo escrito
"AGINT" e uma tabela impressa duas vezes.

**Diagnóstico transversal: a IA acerta o eixo jurídico e erra por OMISSÃO nas cautelas de
advogado sênior** — blindagem recursal e questões laterais. Varra sempre prevenção,
preclusão, competência interna, composição **atual** da turma e fatos supervenientes.

## Citação: seis modos de falha, não um

Cinco foram catalogados em 09/07/2026; o sexto entrou em 09/08/2026.

| Modo | O que é |
|---|---|
| inexistente | o julgado não existe |
| nome trocado | existe, mas o relator ou o órgão estão errados |
| misquote | a transcrição não confere com o texto |
| pincite | a página ou o item citado não contém aquilo |
| tese deturpada | confunde *ratio* com *dictum* |
| superado / vigência | o precedente foi superado ou está sob embargos |
| **razão de decidir invertida** | **existe, está corretamente referido, e é usado ao contrário do que decidiu** |

O sexto é o mais difícil, porque **sobrevive a toda checagem de existência**. Caso real: a
parte contrária invocou um AgInt para sustentar perda do efeito interruptivo; lida a
ementa, a razão de decidir aplicada era a **regra** da interrupção, e o recurso fora
**provido** para desfazer a intempestividade reconhecida com a tese oposta. O enunciado da
exceção estava na mesma ementa, e era dele que a citação se servia — legitimamente.

**Existência ≠ atribuição ≠ aderência da ratio.** Só a leitura da ementa separa as três.

## Bloqueio declarado não é bloqueio testado

Em dois dias a esteira declarou **três** bloqueios falsos, todos com causa formalmente
correta:

- o inteiro teor de três acórdãos do STJ, "inalcançável pela automação", dependia de um
  parâmetro de consulta;
- uma decisão do STF, tratada por semanas como dependente de procuração nos autos, tem
  acesso aberto e faltava só o número de incidente;
- a última decisão de uma ação civil pública, dada como dependente de acesso aos autos,
  sai inteira pelo DJEN.

Nos três o agente esgotou **as rotas que já conhecia** e escreveu "não há caminho". E a
redação fechada **remove o item da fila**, porque ninguém reaudita o que já tem causa
registrada. Consulte `forja_rotas_fonte.py` antes; registre `revalidarApos`.

## Achado forte gera excesso na redação

Os piores erros da casa não vieram de má notícia: vieram de **incorporar boa notícia**.
Descoberto um argumento forte, a redação seguinte tende a esticá-lo além do que a fonte
sustenta.

Duas defesas: **objeção externa rejeitada deve ser relida a cada versão** — o motivo de
rejeitar pode ter caducado; e **regra nova se confere contra as que já existem**, não só
contra a evidência que a motivou.

Caso real: a peça afirmava a *razão de decidir* de dois acórdãos que o nosso próprio
relatório de conferência declarava **não lidos**. Um deles fora provido por unanimidade.

## Gate, documento e quem se autovalida

**Gate mede o estado do mundo, não a qualidade da declaração.** O gate de aceite confere
existência, tipo e tamanho do artefato — nunca se ele está bom.

**Gate que só procura defeito nunca detecta pobreza.** É preciso a contraparte
afirmativa, que verifica presença.

**Gate instalado em rota que ninguém percorre é gate nenhum.** Um elo bloqueante sério
rodou em três casos na história inteira.

**Regra escrita que não pega precisa virar gate** — e o inverso também acontece: a seção
do protocolo que criou os gates S6 e S7 nunca os implementou. Veja
[GATES.md](GATES.md#gates-citados-na-documentação-que-não-existem-no-código).

**Comitê de personas não substitui revisão de código.** O conselho leu o dossiê do
construtor e recomendou arquitetura já rejeitada, citando função inexistente. Quem
constrói escreve o gate, mede com ele e se aprova — a circularidade só quebrou na revisão
por outra família, lendo o XML.

**Fonte primária não é revisão de texto.** Num caso real, três camadas de revisão deram
zero P0; abrir os autos deu seis.

**Detecção sem destinatário nomeado é telemetria, não vigilância.** Um monitor capturou
um embargo no dia seguinte ao protocolo, gravou no log e ali ficou — dois dias depois o
titular ainda não sabia. Log é trilha; caixa de aviso é destinatário.

## Armadilhas de máquina

**`OSError: [Errno 22]` ao salvar DOCX** é MAX_PATH do Windows, não corrupção. Construa
em `C:\vt` e copie de volta.

**Não rode o baseline em paralelo com a montagem de peça.** As duas rotas passam pelo
Word por COM; uma trava a outra por meia hora e o wrapper ainda reporta exit 0. Rodada em
série, a mesma suíte leva 3,7 segundos.

**Checagem que responde zero merece a mesma suspeita que resultado bom demais.** Uma
verificação de arquivos versionados respondeu "0 rastreados" para 1.200 arquivos porque a
base relativa estava errada.

**Duas sessões no mesmo repositório colidem em silêncio.** `git add -A` varre o trabalho
alheio; `mkdir(exist_ok=True)` numa pasta que você supõe sua sobrescreve artefato de nome
genérico — `F7_VERIFICADOR_FORJA.json`, `mapa.json`. Commite por caminho nominal e confira
o destino antes de publicar.

**Comando que falha com exit 127 não diz nada sobre o arquivo** — diz que o binário não
existe. Um `ls` aliasado para uma ferramenta ausente já me fez concluir que um script da
casa tinha sumido.

**Divisor de frase quebra em abreviação nos dois sentidos.** O filtro que pegava a metade
que *começa* minúscula deixava passar a que *termina* em "art." — e ela começa maiúscula.
