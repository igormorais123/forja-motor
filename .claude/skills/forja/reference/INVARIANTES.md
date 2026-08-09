# INVARIANTES — as ordens que não se negociam

> Cada uma tem data e origem, porque em conflito **vale a mais recente** e porque saber
> quem determinou é o que permite reabrir com fato novo. A fonte canônica é o
> `CLAUDE.md` da fábrica; este documento é o extrato operacional. Onde o `CLAUDE.md`
> divergir daqui, ele vence — e conserte esta página.

## Índice

- [Fronteira motor / acervo](#fronteira-motor--acervo)
- [Regimento do tribunal](#regimento-do-tribunal)
- [O que a peça precisa conter](#o-que-a-peça-precisa-conter)
- [Conselho obrigatório](#conselho-obrigatório)
- [Revisão cruzada entre famílias](#revisão-cruzada-entre-famílias)
- [Modelo editorial](#modelo-editorial)
- [Assinatura visual](#assinatura-visual)
- [Tratamento e citação do acervo](#tratamento-e-citação-do-acervo)
- [Identidade dos atos recursais](#identidade-dos-atos-recursais)
- [Exploração em 100 perguntas](#exploração-em-100-perguntas)
- [Ordem de pesquisa jurisprudencial](#ordem-de-pesquisa-jurisprudencial)
- [Advogado, não juiz](#advogado-não-juiz)
- ["Não localizado" não é diagnóstico](#não-localizado-não-é-diagnóstico)
- [Aprendizado contínuo do retorno humano](#aprendizado-contínuo-do-retorno-humano)

---

## Fronteira motor / acervo

O **FORJA Motor** é somente o sistema genérico, indistinguível de um produto que qualquer
escritório possa clonar e usar. Nele não entra nome, marca, logo, contato, configuração,
caso, processo ou dado pessoal do escritório. Tudo isso vai para **`forja-auditoria`**, o
acervo privado.

A fronteira é física: `%USERPROFILE%\repos\forja-motor` e `%USERPROFILE%\repos\forja-auditoria`
são diretórios Git independentes. A montagem local alimenta os dois e não os funde.

## Regimento do tribunal

*06/07/2026 — determinação do chefe do escritório, após erros em peças que ignoraram
peculiaridades regimentais.*

Em **toda** peça: identificar o tribunal pelo número CNJ, endereçamento e decisões; ler
`REGIMENTO_INTERNO_<TRIBUNAL>.md` da pasta do caso; se não existir, baixar a consolidação
oficial e salvar com cabeçalho de metadados (fonte, versão, data do download).

**Nenhum regimento arquivado é vigente pelo que está escrito nele.** Antes de usar,
pesquisar emendas posteriores à consolidação e anexá-las na seção final. A peça reflete o
regimento vigente **na data do protocolo**. A composição do órgão julgador se confirma na
fonte, nunca de memória.

Considerar também `_LEIS_GERAIS`: Estatuto da OAB (Lei 8.906/1994) e LOMAN (LC 35/1979).
Registrar no relatório quais dispositivos foram considerados e como impactaram a peça.

## O que a peça precisa conter

*08/07/2026 — INVIOLÁVEL, minerado dos retornos humanos. Canônico com checklist:
`APRENDIZADOS_FEEDBACK_HUMANO.md`, na raiz da fábrica.*

O diagnóstico que originou esta ordem vale mais que a lista: **a IA acerta o eixo
jurídico e erra por OMISSÃO nas cautelas de advogado sênior** — blindagem recursal e
questões processuais laterais. Nenhum destes sete itens é estilo; todos são conteúdo.

1. **Síntese executiva no estilo do art. 343-A do RISTJ, no início de toda peça**, em
   qualquer tribunal (Prof. Fábio, e-mail de 07/07/2026). Passou de meia página, deixou de
   ser síntese: o desenvolvimento é dos capítulos.
2. **Prequestionamento expresso** — dispositivos legais **e** constitucionais carimbados —
   com **terminologia blindada contra as Súmulas 7/STJ e 279/STF**: "omissão qualificada",
   "fundamentação individualizada", "erro de subsunção". Não escreva nada que se leia como
   pedido de reexame de prova.
3. **Fato superveniente em capítulo autônomo**, com enquadramento fino. O visual é apoio
   dele, nunca o eixo.
4. **Varrer as questões processuais laterais no mapa do caso**: prevenção, preclusão,
   competência interna, composição **atual** da turma e fatos supervenientes. A peça que
   originou a lição estava certa no mérito e não tratou prevenção nem preclusão.
5. **Em embargos de declaração e em improbidade**, as oito diretrizes do Dr. Alessandro: o
   vício se formula como pergunta jurisdicional; admissibilidade não se mistura com
   mérito; e dolo específico **não** é dolo genérico, nem culpa, nem culpa in vigilando,
   nem assunção de risco, nem cegueira deliberada. Os pedidos vão **por vício**, e se
   forem infringentes, pede-se a intimação da parte adversa.
6. **Pós-entrega obrigatório**: retorno recebido → diferença entre a versão protocolada e
   a nossa → classificação → atualização do `APRENDIZADOS_FEEDBACK_HUMANO.md`. É o ciclo
   de [aprendizado contínuo](#aprendizado-contínuo-do-retorno-humano), e ele não é
   opcional.
7. **Prescrição administrativa por matriz, nunca por rótulo global**: separar fundo de
   direito, metodologia, parcelas, negativa e ciência. E-mail não equivale a protocolo
   (enviar ≠ receber ≠ ter competência ≠ processar); a modulação vem do dispositivo
   oficial; o valor é estimativa até a conciliação por parcela; e processo administrativo,
   protesto ou lei posterior não revivem sozinhos pretensão prescrita.

## Conselho obrigatório

*09/07/2026, ampliado em 06/08/2026 — ordem do Igor.*

Toda petição elaborada, melhorada ou revisada passa por **`/helena`** (estratégia),
**`/cicero`** (jurídico) e **Diabob** (contraditório adversarial) **antes da redação
final**. Cada um emite parecer escrito com recomendações numeradas; o redator registra a
decisão sobre cada uma — acatada, rejeitada, por quê.

O Diabob roda **pelo comando**, porque o gate afere a proveniência da chamada e não o
texto:

```
python forja_diabob.py --arquivo <blueprint> --saida F4_PARECER_DIABOB.json
```

Prosa dizendo que passou pelo Diabob reprova. Parecer da mesma família que produziu a
peça reprova como eco. Caso que não declara fica `unknown`, e **`unknown` não é `pass`**.

O parecer do Diabob é insumo interno de auditoria: propõe objeções, **não afirma fatos**,
não vai para a peça, não vira fundamento e não substitui o F7. Ele não se confunde com a
skill `forja-red-team`, que conduz as nove perguntas por dentro — as duas rodam.

## Revisão cruzada entre famílias

*25/07/2026.*

O trabalho pode nascer no Claude ou no Codex, mas **a outra família revisa**. O contrato
do run declara `producerModel` e `reviewerModel`; `familyAssurance` assume `cross_family`,
`cross_session_same_family` ou `unverified`, e é recomposto pelo orquestrador — nunca
aceito por declaração.

O gate `cross_model_review_verified` bloqueia `unverified` em qualquer modo; em
`strict_protocol` só `cross_family` libera. Se a segunda família estiver indisponível, o
caso **não para**: rebaixa para `cross_session_same_family` **com o motivo registrado**.
A degradação é permitida; o silêncio não.

## Modelo editorial

*25/07/2026 — ordem do Igor, supera a de 15/07 que fixava o Fable 5.*

O modelo editorial padrão é **`claude-opus-5`**; o Fable 5 permanece autorizado como
legado. A allowlist é `forja_editorial_model.py` — modelo fora dela não executa.

A subfase `F7-B` só abre depois que `f7_gate_result.json` comprova **zero P0**. O editor
revisa e reescreve **exclusivamente a forma**: não cria nem altera fato, data, número,
valor, citação, autoridade, marcador processual, ressalva, pedido, fecho ou assinatura.
Quem recompõe hashes e invariantes é o orquestrador, por `forja_editorial_fidelity.py`.

`final_markdown` é o único cânone textual de F8 em diante. Os gates automáticos são
escudos lexicais e estruturais — **não** são prova de equivalência semântica nem
substituem a auditoria F7 e a revisão humana.

## Assinatura visual

*30/07/2026 — ordem do Igor; esteira reconstruída em 03/08/2026.*

Nenhuma peça sai sem elementos visuais completos. Detalhe em [VISUAL.md](VISUAL.md).

## Tratamento e citação do acervo

*11/07/2026 — feedback do Fábio, INVIOLÁVEL.*

Duas camadas rigorosamente separadas: **proveniência interna**, no ledger e no relatório
de auditoria; **referência processual**, na peça.

A peça jamais revela a origem operacional do insumo. São proibidas fórmulas como "arquivo
compartilhado pelo escritório", "recebido por e-mail ou WhatsApp", "localizado na pasta",
"arquivo local ou Drive" e caminhos de computador. Na peça só existe referência
verdadeira: "documento juntado aos autos", "e-STJ fl. X", "evento/ID X", "Doc. X —
[título]", "documento anexo". **Não** se chama de "juntado aos autos" o que ainda não foi
protocolado, nem de "anexo" o que não acompanhará a manifestação.

Marcadores de auditoria — `[FONTE: ...]`, `[DECLARAÇÃO]`, `[INFERÊNCIA]`, `[VERIFICAR]` —
pertencem só aos artefatos internos e nunca podem aparecer no DOCX ou PDF protocolável.

Antes da liberação: gate de origem operacional. Qualquer menção a e-mail, WhatsApp,
Drive, pasta interna, caminho local ou compartilhamento no corpo da peça é **bloqueador
P0** (`G9-proveniencia`).

## Identidade dos atos recursais

*11/07/2026 — feedback do Fábio, INVIOLÁVEL.*

Em processo volumoso, antes de redigir: cronologia auditada e grafo dos atos. Cada
recurso, decisão, retratação, destaque e intimação recebe identificador próprio, data,
sujeito, classe e número, ato impugnado, pedido, efeito jurídico e ponte exata para os
autos.

**É proibido escrever "o recurso", "o agravo" ou "a decisão anterior" quando há mais de
um ato possível.** Sem a íntegra do ato atualmente impugnado, a produção permanece
`internal_working` e não gera versão protocolável.

O erro que isso fecha não é número errado: é o número **certo de outro processo do mesmo
cliente** — o texto fica internamente coerente e nenhum gate lexical discorda dele.
Estado da verificação automática: veja
[GATES.md](GATES.md#gates-citados-na-documentação-que-não-existem-no-código).

## Exploração em 100 perguntas

*14/07/2026 — ordem do Igor, INVIOLÁVEL.*

Todo caso novo passa, depois de F1 e **antes** de pesquisa, conselho, blueprint ou
redação, pela subfase `F2A`. O `F2_QUESTION_TREE.json` usa `FORJA-F2A-100-v1`, com
exatamente 100 perguntas, 10 em cada ótica canônica, cada resposta com classificação
epistemológica e lastro quando factual.

**Lacuna não é resposta:** fica `blocked`, com consequência e rota de diligência. Questão
material bloqueada impede peça protocolável.

## Ordem de pesquisa jurisprudencial

*28/07/2026 — diretriz do Prof. Fábio, transmitida pelo Dr. Alessandro.*

A pesquisa percorre os níveis **nesta ordem** e para de subir quando encontra material
aderente. O relatório registra em que nível a peça se apoiou.

1. STF — Plenário
2. STF — pelo relator, quando já há processo no tribunal ou prevenção, e pelos demais
   integrantes das turmas
3. STF — demais turmas
4. STJ — Órgão Especial
5. STJ — pelo relator, quando o processo já está no STJ ou há prevenção, e pelos demais
   integrantes das turmas
6. STJ — demais turmas
7. Tribunal local — Pleno ou Órgão Especial
8. Tribunal local — decisões do relator, quando já está no TJ ou há prevenção
9. Tribunal local — da câmara ou turma julgadora, relatoria dos demais integrantes

Sem competência ou relatoria conhecidas, a pesquisa fica genérica entre turmas e câmaras.

**A ordem não é de hierarquia abstrata: ela persegue quem vai julgar**, e é por isso que
os níveis 2, 5 e 8 quebram a escada dos tribunais. O órgão julgador e a relatoria se
confirmam pelo número no cadastro nacional do CNJ, sem depender de informação de
terceiro — então esses três níveis são a primeira parada real, não uma hipótese.

## Advogado, não juiz

*06/08/2026 — diretriz escrita do titular.*

Risco, objeção e precedente contrário são **identificados e enfrentados**, inclusive por
distinção tecnicamente sustentável — jamais adotados nem antecipados como juízo
desfavorável ao cliente.

Lê-se junto com a regra de enfrentar a objeção mais forte da adversa: **enfrentar serve
para vencer, não para conceder.** Isoladas, as duas se degradam — regra nova se confere
contra as que já existem, e não só contra a evidência que a motivou.

## "Não localizado" não é diagnóstico

*06/08/2026, com o gate de rotas de 07/08/2026 — ordem do Igor, INVIOLÁVEL.*

Foi a cobrança mais recorrente que o titular já fez à esteira: a mesma, quase palavra por
palavra, em cinco matérias distintas.

Insumo que não se conseguiu ler exige **causa em vocabulário fechado** — falta de
habilitação nos autos, restrição de permissão ou link, indisponibilidade na fonte,
limitação da própria ferramenta —, diligências registradas com onde, quando e resultado,
o que da peça fica sem lastro, e quem pode destravar. Cada causa tem solução diferente;
colapsá-las transfere ao titular o trabalho de descobrir qual era.

**E o bloqueio se testa, não se declara.** Cada item de `F1_INSUMO_BLOQUEADO.json` exige
`fonte`, `tipoDocumento`, `rotasTentadas` e `revalidarApos` (no máximo 45 dias). O gate
reprova quando sobra rota conhecida por tentar, quando a causa contradiz o que a fonte de
fato faz, e quando falta prazo de revalidação. Consulte `forja_rotas_fonte.py` **antes**.

Em dois dias a esteira declarou três bloqueios falsos, todos com causa formalmente
correta e conclusão errada — e a redação fechada **remove o item da fila**, porque
ninguém reaudita o que já tem causa registrada.

## Aprendizado contínuo do retorno humano

*06/08/2026 — ordem do Igor, INVIOLÁVEL.*

Toda correção que o titular faz numa peça é insumo do sistema, não só do caso. Seis
passos, nesta ordem:

1. **Capturar e comparar.** `forja_post_protocol.py` traz a versão humana e compara com a
   nossa. Sanitizado por hash: guarda `beforeHash`, `afterHash` e localizador, **nunca o
   trecho** — o texto vive só no cofre local, fora de todo repositório.
2. **Antes de tudo: isto é revisão da nossa peça?** O gate `PP-NOT-A-REVISION` mede a
   proporção de texto em comum e barra abaixo de 0,30. Dos cinco retornos reais medidos,
   três tinham 0,7%, 3,1% e 13,4% e não eram revisão de nada — sozinhos respondiam por
   496 mudanças. **Agregado por classe, esse ruído tinha a forma exata de um padrão do
   escritório**, e quase virou regra permanente.
3. **Ler o padrão, não a ocorrência — e ler o texto, não só a contagem.** `padroes`
   ordena por recorrência **entre casos distintos**. Nenhuma regra é adotada sem que
   alguém tenha lido exemplos com `amostra`.
4. **Adotar com destino executável.** `adotar ... --destino {checklist|template|doutrina}
   --fase Fn --regra "..." --aprovado-por <nome>`. A decisão é humana.
5. **Aplicar de verdade.** `aplicar` escreve a regra no destino. **Registrar a frase não
   é aprender**; aprender é a próxima peça nascer diferente.
6. **Revalidar o lastro.** `revalidar` compara a evidência da adoção com a de hoje. Uma
   regra pode continuar sensata e ter perdido o lastro — foi o que aconteceu com a
   primeira regra da casa, adotada com "3 casos, 12 correções" e reduzida a 1 e 1.

**A correção que vem escrita no e-mail conta igual — e é a maioria.** A varredura pedia
`has:attachment` e descartava em silêncio toda mensagem sem peça anexada. Corrigido, a
primeira rodada trouxe **45 correções** contra as 5 que a esteira via: o loop enxergava
um décimo do retorno do titular. Guarda-se localizador, assunto e data — **nunca o
corpo**.

O elo **5-B** do F10 bloqueia se uma regra adotada saiu do seu destino. Ele **não** exige
que o caso corrente já tenha aprendido: o retorno chega depois do protocolo.
