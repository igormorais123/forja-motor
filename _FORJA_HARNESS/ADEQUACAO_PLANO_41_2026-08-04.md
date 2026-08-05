# Adequação do Plano 41 ao estado atual — 04/08/2026

Uma equipe de quinze agentes auditou o Plano 41 requisito a requisito contra o
código vivo: 47 requisitos extraídos, 36 auditados, 5 afirmações de "cumprido"
derrubadas por céticos independentes.

**O laudo dela apontou cinco lacunas, duas das quais eu conferi e são falsas.**
Este documento registra o que sobrou depois da conferência, porque a auditoria
também é um artefato e também erra — foi a lição da triagem do censo, e ela
voltou a valer aqui.

## O que o painel acertou

**A detecção de moeda era frágil.** `_MOEDA_EXPLICITA` exigia `R$` colado, e esse
marcador é quem decide se os gates L9 a L13 rodam. Um texto com `R $` — espaço
entre o erre e o cifrão — não acionava a família econômica inteira, e a falha
seria silenciosa: a peça simplesmente não seria auditada quanto à fonte
prevalente. Corrigido nos dois padrões, com regressão nas três variantes e a
não-trava do outro lado, para que número grande sem marcador de moeda continue
sem acionar nada.

## O que o painel errou, e como

**A ocorrência citada não existe.** O agente afirmou que
`PLANO_ESTRATEGICO_CAFELANA_RECONSTRUIDO_FORJA.md`, linha 66, contém
`R $ 524.141.077,62`. Varri todos os `.md` da fábrica: **zero ocorrências** dessa
forma. A fragilidade do regex era real; o caso concreto que a comprovaria, não. O
conserto continua valendo — errar para o lado de auditar a mais custa uma
conferência —, mas o dano relatado era imaginário.

**A "Lacuna 2" é leitura da função errada.** O laudo afirma que
`forja_delivery.py` chama `verificar()` sem `ledger`, `case_dir` nem
`exigir_economico`, e conclui que os gates econômicos nunca rodam em produção. A
linha citada, 89, está dentro de `f7_com_lastro`, que é uma checagem estreita de
P0. O elo 9-B da mesma rota, linhas 322 a 357, localiza o `fact_ledger.json`,
chama `material_economico(texto_f7)` e invoca `validar_gates_economicos` com
ledger e `base_dir`. A rota faz exatamente o que o laudo diz que ela não faz.

**A "Lacuna 4" nega um arquivo que existe.** Afirma que
`test_forja_lastro_rota_producao.py` "não existe em repositório". Ele existe, está
na régua e passa: *o laudo de lastro nasce no disco pela rota de produção, derruba
gate autoatestado sem transcrição e não trava fato transcrito*.

## O que continua aberto, e é decisão sua

**A severidade do L11.** O plano previa P0 para valor monetário órfão; a
implementação está em P1 por medição de cerca de 55% de falsos positivos contra
2.491 valores do acervo. O painel apontou a divergência corretamente. Promover a
P0 sem nova calibração travaria peça legítima; manter em P1 deixa a cifra sem
âncora passar como observação. **Nenhum código resolve isso** — depende de você
decidir se a esteira deve travar ou observar enquanto a separação entre valor
citado e valor calculado não for confiável.

**A tabela de hashes do D6 estava defasada.** A seção existia, mas carregava
hashes de ondas anteriores, duplicava `forja_regua.py` e usava caminho impreciso
para `medina_visual_kit.py`. Ela foi reconciliada com os arquivos atuais e com o
hash conferido na régua final aprovada de 21:58:28; a seção histórica da onda v22
foi preservada. É rastreabilidade, não correção: nada de errado sai da fábrica
por causa disso.

## A lição que este exercício deixa sobre painéis

Três dos cinco achados de alto risco não sobreviveram a quinze minutos de
conferência direta, e todos os três falharam do mesmo jeito: **o agente leu um
trecho do código e generalizou para a rota inteira.** A função `f7_com_lastro` não
passa o ledger, e daí concluiu-se que a entrega não passa; o arquivo não apareceu
numa busca, e daí concluiu-se que ele não existe.

Isso não desqualifica o painel — ele encontrou a fragilidade real do regex, que
nenhuma leitura minha tinha achado em três dias sobre este código. Qualifica o
uso: **achado de painel é hipótese com endereço**, e o endereço é a parte
valiosa. Aceitar o veredito junto com o endereço é que sai caro.

## Estado do plano depois desta passagem

Cumprido no essencial. O desenho D1, os gates D2 e a regressão D4 existem, rodam e
reprovam; o acoplamento D3 alcança a rota de produção e tem teste que prova. Resta
uma decisão sua sobre a severidade do L11; a dívida de hashes foi reconciliada
nesta passagem. A regressão do plano subiu de 33 para 37 cenários e a suíte fecha
em 98 verificações.
