# CONSELHO DA FORJA N4 - PARECER CICERO

**Data de corte:** 11/07/2026  
**Objeto:** confiabilidade juridica da FORJA antes da revisao humana, com foco em registro, prova, fontes, terminologia, citacoes, pedidos e liberacao.

## Resultado juridico direto

A N4 deve ser mantida como instrumento de producao assistida e bloqueante, mas nenhuma aprovacao estrutural pode ser tratada como liberacao juridica. O sistema atual prova razoavelmente que um arquivo existe e nao mudou; ainda nao prova, com a mesma forca, que cada afirmacao material da peca decorre da fonte indicada, que o ato processual foi identificado sem ambiguidade e que todas as citacoes foram conferidas em fonte oficial.

## Acertos

1. Cafelana foi corretamente revogada quando se descobriu a confusao entre o AREsp de 2024 e o AgInt de 2026.
2. A N4 separa alegacao, suporte, contradicao, lacuna e tese, e possui arvore de questoes, grafo e matriz de cobertura.
3. A dimensao intertemporal, a comparacao de pecas adversarias e a auditoria de ciencia interdisciplinar sao juridicamente uteis quando ligadas a fontes.
4. Helena e Cicero aparecem como revisoes internas e nao como autoridades citadas na peca.
5. O protocolo local agora separa proveniencia interna de referencia processual e proibe caminhos, e-mail ou WhatsApp no artefato protocolavel.

## Falhas por severidade

### C-01 - CRITICA - Rastreabilidade de arquivo nao equivale a suporte da proposicao

O registro N4 associa IDs a arquivos e hashes, mas nao exige universalmente a unidade `afirmacao -> fonte primaria -> trecho/localizador -> alcance -> ressalva`. A metrica pode chamar de proveniencia aquilo que e apenas localizacao.

**MUST:** criar cobertura de sustentacao de afirmacoes materiais. Uma fonte somente conta quando a proposicao e o trecho que a sustenta foram registrados e conferidos.

### C-02 - CRITICA - Liberacao juridica ignora gates materiais

`legalReleaseStatus` e derivado essencialmente de `gaps` das teses e da fase F10 (`forja_n4_validate.py:316-341`). Nao agrega diretamente citacoes, prazo, identidade do ato, visual, placeholders, entrega e revisao humana.

**MUST:** matriz positiva de liberacao. `structurally_clear` exige todos os gates; qualquer P0 ou P1 material produz `blocked` ou `human_review_required`.

### C-03 - ALTA - Citacoes nao conferidas nao impedem aparencia de aprovacao

A telemetria real registrou 54 citacoes detectadas, 15 conferidas e 39 nao conferidas. Isso nao prova falsidade, mas impede que o sistema as trate como juridicamente confirmadas.

**MUST:** toda citacao material deve ter fonte oficial, proposicao, trecho e localizador, ou ser retirada/marcada internamente como pendencia. A gestao deve mostrar a cobertura.

### C-04 - ALTA - Identidade do ato processual precisa ser um gate autonomo

O erro Cafelana demonstra que texto persuasivo e visual correto podem estar montados sobre o recurso errado. Em processo volumoso, `o agravo` ou `a decisao` nao bastam.

**MUST:** cronologia e grafo de atos com identificador, data, sujeito, classe/numero, ato impugnado, pedido, efeito e ponte aos autos. Sem a integra do ato atual, o produto permanece `internal_working`.

### C-05 - ALTA - Mutation testing literal nao mede erro juridico decisivo

Remover a expressao que um teste procura apenas demonstra que a busca literal funciona. Nao detecta troca de parte, inversao de tese, decisao diversa, valor, prazo, pedido incompativel ou precedente com alcance menor.

**MUST:** manter o score literal apenas como diagnostico e criar mutacoes juridicas estruturadas. Promocao depende destas, nao daquelas.

### C-06 - ALTA - QA visual aprovado nao resolve fidelidade juridica

Pagina legivel pode conter tese errada; peca correta pode ficar inutilizavel por corte ou sobreposicao. Os gates devem ser separados e ambos obrigatorios.

**MUST:** QA visual pagina a pagina com evidencia; fidelidade semantica comparando fonte canonica, DOCX e PDF; alteracao posterior invalida ambos.

### C-07 - MEDIA - `not_applicable` exige fundamento normativo do tipo de produto

F9/F10 podem ser nao aplicaveis em baseline interna, mas nao em ciclo prospectivo que se apresenta como entrega. Texto livre nao basta.

**SHOULD:** matriz de aplicabilidade por genero, fase e destino.

### C-08 - MEDIA - Pareceres do conselho precisam produzir decisoes rastreaveis

Nomes de revisores diferentes nao demonstram independencia nem que a critica foi enfrentada.

**SHOULD:** cada parecer registra achado, evidencia, disposicao `aceito/rejeitado/adiado`, alteracao correspondente e teste de fechamento.

## Recomendacoes rejeitadas

- **REJECT:** inserir na peca nomes de agentes, scores, prompts ou etiquetas de laboratorio.
- **REJECT:** bloquear trabalho interno apenas porque ainda ha lacuna; o correto e impedir a promocao protocolavel e indicar a providencia concreta.
- **REJECT:** multiplicar ressalvas genericas ou linguagem defensiva. Lacuna deve ser especifica, localizada e acionavel.
- **REJECT:** usar fonte secundaria quando a fonte oficial ou o documento dos autos esta disponivel.

## Criterios de aceite juridico

1. Cada afirmacao material possui fonte primaria, proposicao, trecho/localizador e alcance.
2. Cada precedente material foi conferido quanto a existencia, atualidade, tese e aderencia.
3. O ato impugnado e inequivoco e esta ligado a integra dos autos.
4. Prazo e regime intertemporal derivam de eventos e fontes identificados.
5. Pedidos correspondem aos fundamentos e a competencia do orgao.
6. Nenhum marcador interno ou origem operacional aparece no DOCX/PDF externo.
7. Visual e fidelidade semantica foram revistos depois da ultima alteracao.
8. `structurally_clear` so aparece quando a matriz positiva estiver integralmente satisfeita.
9. Helena e Cicero registraram critica propria e o sistema mostra como cada achado foi tratado.
10. A revisao humana final permanece obrigatoria antes de protocolo.

## Decisao Cicero

Aceito a N4 como arquitetura de minuta inicial e auditoria. Rejeito qualquer leitura de `approved=true` como autorizacao de protocolo. A melhoria prioritaria e transformar cada proposicao juridicamente relevante em uma ponte verificavel entre registro, fonte, raciocinio e pedido.
