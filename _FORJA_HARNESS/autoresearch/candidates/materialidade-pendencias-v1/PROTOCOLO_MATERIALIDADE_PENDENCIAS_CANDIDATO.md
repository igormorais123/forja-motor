# Protocolo candidato — materialidade de pendências

Versão: `FORJA-PEND-MAT-v1-candidate`  
Estado: `estudo_descritivo`  
Promoção: proibida antes dos gates AR, revisão independente e aprovação humana previstas no ciclo Auto-Research.

## Problema

Listar toda lacuna como bloqueador produz três falhas: posterga entregas úteis, transfere ao advogado diligências que não mudam o produto e transforma o e-mail de entrega em inventário defensivo de pendências.

## Regra central

Só se pede ou espera um insumo quando, depois de ajustar honestamente o escopo e a redação, sua ausência:

1. impede cumprir o objeto principal;
2. impede responder uma questão material; ou
3. tornaria falsa uma afirmação necessária do produto.

Se o insumo apenas aumentar confiança, detalhar fundamento, permitir atualização ou melhorar uma conclusão já qualificada, ele é útil, mas não bloqueante. O trabalho segue e a possibilidade de complemento é mencionada brevemente ao advogado.

## Linha operacional confirmada

O procedimento não é apenas “classificar pendências”. É:

1. elaborar e encaminhar o trabalho com o acervo disponível;
2. não adiar a revisão por documentos que só possam aperfeiçoar o resultado;
3. mencionar a pendência ao advogado como ressalva breve, sem enviar o checklist interno;
4. delimitar somente a conclusão que ainda não possa ser certificada;
5. se o documento posterior for materialmente relevante, incorporar seu impacto por ajuste pontual ou adendo, sem reiniciar automaticamente o trabalho.

Assim, uma pendência específica nunca contamina a prontidão de todo o produto quando o objeto proposto já pode ser atendido de forma útil e verdadeira.

## Classificação obrigatória

| Classe | Consequência |
|---|---|
| `essential_to_product` | suspende a entrega porque o objeto principal não pode ser atendido de modo honesto |
| `essential_to_claim` | não suspende necessariamente o produto; exclui ou condiciona apenas a afirmação afetada |
| `useful_nonblocking` | não se espera nem se condiciona a entrega; pode gerar adendo se chegar |
| `irrelevant` | não se pede, não se espera e não se menciona na mensagem de entrega |
| `superseded` | diligência perdeu objeto por fonte, ato ou decisão posterior; retirar da fila |

## Teste de menor bloqueio

Antes de classificar uma pendência como essencial, responder:

1. O produto continua útil se a conclusão afetada for delimitada?
2. É possível substituir certeza por condição, cenário ou ressalva fiel?
3. A ausência impede o objeto ou apenas impede uma certificação mais ampla?
4. A FORJA consegue obter o insumo por fonte já autorizada sem transferir a diligência?
5. O custo e o tempo de esperar são proporcionais ao impacto provável?

Se o produto puder seguir com recorte verdadeiro, a pendência não é `essential_to_product`.

## Comunicação ao advogado

A mensagem de entrega:

- começa pela entrega e pela recomendação;
- não despeja o checklist interno;
- menciona em até duas frases que documentos posteriores poderão justificar ajuste ou adendo;
- nomeia uma pendência somente quando ela limita conclusão relevante do produto;
- nunca diz que o trabalho está incompleto se o objeto delimitado foi cumprido.

Fórmula-base:

> Encaminho a versão elaborada com o acervo disponível. As diligências remanescentes não impedem a análise e poderão, se relevantes, justificar ajuste pontual ou complemento posterior.

Somente quando necessário à decisão do advogado, acrescentar:

> Permanece condicionada apenas a conclusão sobre [ponto específico], que não está apresentada como definitiva na versão encaminhada.

## Casos-âncora da decisão de 23/07/2026

Estes casos documentam a aplicação da regra, sem transformar seus fatos em regra geral:

| Caso | Produto que segue agora | Único limite material |
|---|---|---|
| Vale | análise metodológica, crítica pericial e cenários | certificação do valor final |
| CORSAN | diagnóstico, estratégia e riscos por hipótese | mérito dos autos ainda não recebidos |
| Deltan | parecer para revisão interna | liberação assinável ou externa sem revisão humana |
| Natura | parecer condicionado sobre a tese de prescrição | cobrança global ou afirmação absoluta sobre prescrição parcelar |
| Cafelana | dossiê e pesquisa preliminar | uso definitivo do precedente sem as íntegras críticas |

Fonte operacional interna: `gestao_escritorio/NOTA_DECISAO_PENDENCIAS_ENTREGA_2026-07-23.md`.

## Handoff por fase

- **F2/F2-A:** classificar cada lacuna pela utilidade marginal e pelo impacto no objeto.
- **F3–F5:** tentar fontes autorizadas antes de pedir material ao advogado.
- **F6:** retirar ou condicionar apenas a afirmação afetada; não contaminar todo o produto.
- **F7:** conferir que nenhum item não bloqueante foi promovido a P0/P1 sem consequência material demonstrada.
- **F9:** entregar primeiro; mensagem breve; checklist detalhado permanece interno.
- **F10:** trabalho entregue ao escritório encerra a fronteira operacional quando o objeto delimitado foi atendido, mesmo que um adendo futuro permaneça possível.

## Antifraude

- Não rebaixar pendência para acelerar entrega se a afirmação necessária ficaria falsa.
- Não inflar `essential_to_product` para evitar decisão técnica.
- Toda classificação registra a conclusão afetada, consequência concreta e tratamento.
- `useful_nonblocking` não pode conter `requestBeforeDelivery=true`.
- `irrelevant` e `superseded` não aparecem no e-mail.
- A decisão é revisada quando chega novo documento; não se reinicia automaticamente todo o trabalho.

## Artefato candidato

`PENDENCY_DECISION.json`, validado pelo módulo candidato desta pasta. O artefato separa:

- objeto do produto;
- itens e classificação;
- afirmação afetada;
- tratamento;
- decisão de entrega;
- mensagem curta ao advogado.
