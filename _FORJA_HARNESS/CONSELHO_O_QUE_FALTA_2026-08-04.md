# Conselho Helena + Efesto + Cícero + Diabob — o que falta na FORJA

04/08/2026, 23h. Quatro pareceres independentes, contraditório entre eles,
consolidação. Depois, conferência minha item a item.

## Antes do conteúdo: o conselho falhou na primeira tentativa, e mentiu sobre isso

Na primeira rodada, **Helena e Diabob não entregaram** por falha técnica. O
consolidador recebeu dois pareceres e escreveu um documento intitulado *"o que os
quatro concordam que falta"*, atribuindo consenso a quem não falou.

Registro isso no topo porque é a mesma família de defeito que a fábrica passou o
dia caçando: um artefato que parece completo e não é. A segunda rodada trouxe
Helena e Diabob de verdade, e este documento nasce dela.

## O diagnóstico em que os quatro convergem

**A fábrica aprendeu muito bem o que NÃO fazer, e não tem memória do que fazer.**

São 73 gates que sabem reprovar. Mas "o padrão aprovado pelo dono" existia apenas
como regra escrita em protocolo — e regra escrita não se confere contra um
artefato. O preço apareceu inteiro em 04/08: **quatro vezes num único dia** um
gate reprovou o padrão aprovado e a peça foi tratada como defeituosa. Síntese
executiva a 10,5 pt, fólio de 57,3 pt, mistura de Segoe UI com Times nas tabelas,
título e pull quote. Numa delas cheguei a produzir uma "correção" que desfazia a
identidade visual da casa.

Helena nomeou assim: *o harness não está quebrado, está perdendo a memória do que
aprovou*. Diabob chegou ao mesmo lugar por outro caminho — a medição é circular, o
instrumento consulta o próprio código para saber o que procurar.

## O que já fiz, ainda nesta sessão

**Baseline do padrão aprovado** (`forja_baseline_aprovado.py` +
`BASELINE_APROVADO.json`). Três âncoras congeladas: a V8 do Cafelana, que carrega a
mistura tipográfica em tabela; a V4, que prova que não é acidente de uma versão; e
o template da casa, com o fólio de 57,3 pt medido. O que se congela **não é "zero
achados"** — congelar perfeição seria mentira, o template tem uma linha de exemplo
não justificada. Congela-se o *veredito medido na data da aprovação*, o que pega os
dois lados: artefato editado e gate que derivou.

**Canário anti-moldagem** (`test_forja_layout_antimoldagem.py`). Responde à
objeção mais forte do Diabob: quatro afrouxamentos seguidos e um verde perfeito no
fim são indistinguíveis, pelo resultado, de um gate moldado até aprovar. A prova é
o outro lado — estragar de propósito uma peça aprovada, de quatro maneiras, e
exigir que o gate acuse. Acusa as quatro.

**Registro de invocação** (`executadoCom` no `VISUAL_BUILD.json`). Era a
recomendação convergente de Efesto e Diabob. Sem ela, um laudo verde não distingue
"os gates econômicos rodaram e aprovaram" de "nem foram chamados, porque ninguém
passou o ledger".

## O que ficou e vale a pena

**Red team de compliance jurídico** — proposto por Cícero, aceito por Efesto. Doze
perguntas específicas de responsabilidade profissional: dolo específico separado de
genérico, de culpa e de cegueira deliberada; temeridade e calúnia processual;
prevenção, preclusão, competência e legitimidade. Hoje o red team é genérico. É a
maior lacuna restante e é jurídica, não de engenharia.

**Validação cruzada obrigatória de gate novo** — Helena e Diabob. O contrato já
exige revisão cruzada entre famílias de modelo para a *peça*; não exige para o
*gate*. E gate é escrito por quem produz.

## O que o conselho propôs e eu rejeito

**Conflito de interesses e sigilo profissional como gates automáticos** (Cícero).
Efesto derrubou com o argumento certo: nenhum dos dois é padrão computável.
"Conta bancária" é sigilo sempre; "temos contas a pagar" não é. Um gate assim
erraria em 30% a 40% dos casos e perderia a confiança de quem o lê. Valem como
checklist humano — e checklist humano é desenho de processo, não código.

**Competência material do tribunal** (Cícero). Já existe: está no protocolo desde
06/07 como regra inviolável e na exploração de 100 perguntas da F2A. Cícero não leu
o protocolo antes de propor.

**Quatro recomendações genéricas de Efesto** (pré-gate de ledger econômico, remoção
de tetos silenciosos, guard de serializabilidade, verificação de contexto). Cícero
as derrubou com o argumento do próprio protocolo da casa: menor implementação
coerente, sem funcionalidade para cenário hipotético. Nenhuma delas apontava falha
real ocorrida.

**Assinatura Ed25519 no baseline.** O harness já tem manifesto de hash com motivo
escrito na régua; assinar criptograficamente o baseline não muda quem pode alterá-lo,
porque a chave está na mesma máquina. Seria cerimônia.

## O que dependia de você — RESOLVIDO em 04/08/2026, à noite

O Igor leu esta seção e respondeu às três, na mesma mensagem.

**Conflito e sigilo: mortos, e a família inteira junto.** Não viram checklist nem
nada. Ordem verbatim: *"tira tudo do plano de lgpd ou sigilo são petições judiciais
e uso interno... qualquer preocupaçãozinha genérica ou qualquer coisa preocupação
ética de IA. apenas eu humano me preocupo com ética."* O expurgo está executado e
registrado em `planejamento/06_GATES_QUALIDADE_FORJA.md`, seção "Propostas de gate
REJEITADAS". Levou junto o G18, o E6/R6–R9, o RNF-03 e a política de classificação
da informação da MAP.

**A pergunta sobre autorização do cliente não se sustentou.** O Igor: *"não faz
sentido, não diz nada... coloca o efesto helena e diabob para decidir"*. Decidiram:
Efesto e Helena por não construir; Diabob divergiu propondo um G12 mínimo de
registro da cadeia de origem — que a medição mostrou **já existir** no painel (64
de 64 demandas com origem e data). Não há o que construir em nenhuma das duas
versões. Detalhe no mesmo arquivo.

**Lição que o Diabob deixou e que vale mais que a decisão pontual:** o risco não é
o agente obedecer, é obedecer demais — usar a ordem como licença para matar gate
nascido de falha real. O critério que separa os dois virou regra escrita: o gate
vive se está ancorado em falha registrada em `RETROSPECTIVAS.md` ou
`APRENDIZADOS_FEEDBACK_HUMANO.md`; morre se é "e se acontecesse"; e se não se sabe,
pergunta-se em vez de matar.

**O gate F8-S.** O Igor mandou resolver o que o Diabob viu. Frente em execução —
ver `F8S_ANTICIRCULARIDADE_2026-08-04.md`.
