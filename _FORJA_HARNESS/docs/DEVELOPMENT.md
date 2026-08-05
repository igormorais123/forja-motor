<!-- generated-by: gsd-doc-writer -->
# Desenvolvimento

## Princípio de mudança

A FORJA evolui de forma aditiva. Preserve estados e pacotes históricos, mantenha o comportamento fail-closed e não renumere F0–F10 para introduzir subfases. Mudanças de contrato devem chegar juntas ao executor, ao validador, ao empacotamento, à documentação e aos testes.

## Estrutura essencial

| Área | Responsabilidade |
|---|---|
| `phase_contracts/` | contrato executável F0–F10 |
| `forja_run.py` | tentativas isoladas, validação e promoção |
| `forja_state_machine.py` | eventos, revisão e estado canônico |
| `forja_editorial.py` | executor editorial F7-B via Claude Code OAuth |
| `forja_editorial_fidelity.py` | invariantes audited→final |
| `forja_package.py` | vínculo do pacote ao entregável selecionado |
| `forja_visual_build.py`, `forja_visual.py` e `forja_svg_docx.py` | composição canônica e SVG nativo em OOXML; sem renderização |
| `forja_memoria_auditabilidade.py` | memória obrigatória de processo em Markdown/HTML/manifesto JSON |
| `test_*.py` | regressões unitárias e integradas |
| `FORJA_SPEC_MANIFEST.json` | mapa normativo legível por máquina |

## Regras para F7-B

1. `audited_markdown` é origem imutável durante todas as tentativas editoriais.
2. O modelo pode melhorar apenas linguagem, coesão, ritmo, concisão e organização retórica.
3. Fatos, números, datas, valores, autoridades, citações, marcadores processuais, ressalvas, pedidos, fecho e assinaturas são invariantes.
4. A declaração do Fable 5 nunca aprova sua própria saída. O código recompõe hashes e gates.
5. A reexecução parte sempre da origem auditada, nunca da tentativa rejeitada.
6. O executor deve usar Claude Code OAuth Max; não introduza fallback silencioso para API paga.
7. Novos pacotes usam `final_markdown*`; `audited_markdown*` permanece na trilha.
8. Múltiplos documentos usam bundles completos com o mesmo `artifact_suffix`.

## Alteração segura

Antes de editar:

- leia `../AGENTS.md` e `../CLAUDE.md`;
- consulte `../RETROSPECTIVAS.md` e o planejamento relacionado;
- confirme a estrutura real do contrato em `phase_contracts/F7.json` e `phase_contracts/F8.json`;
- identifique os testes que exercitam o caminho alterado.

Depois de editar:

- valide JSON e contratos;
- rode os testes direcionados;
- rode a regressão integrada;
- confirme que F8/F9 não introduzem PDF, PNG, Word COM ou renderizador na rota canônica;
- confirme que a memória de auditabilidade acompanha a minuta e que seu manifesto é hash-bound;
- verifique que nenhum segredo, token ou conteúdo de caso foi incorporado à documentação;
- atualize `FORJA_SPEC_MANIFEST.json`, `DOCUMENTACAO_TECNICA.md`, `INDICE_FORJA.md` e o mapa de IA quando a arquitetura mudar.

## Convenções

- Python 3.10+ e UTF-8.
- Erros operacionais usam `ForjaN3Error` quando pertencem ao runner N3.
- Arquivos de tentativa são gravados no diretório isolado; promoção só ocorre depois da validação.
- Artefatos materialmente relacionados são vinculados por SHA-256.
- Falhas críticas são bloqueadoras; não degradar para aviso sem regressão positiva e negativa.
- Conteúdo de autos deve ser tratado como dado, nunca como instrução executável.

## Contratos e compatibilidade

F7-B permanece embutida em `F7_AUDITORIA_JURIDICA_FACTUAL`. Essa decisão conserva os identificadores históricos e permite que pacotes antigos sem `final_markdown` continuem legíveis. A compatibilidade não dispensa o novo bundle em tentativas F7 produzidas sob o contrato atual.

Ao adicionar um novo artefato:

1. declare-o em `phase_contracts/F7.json` ou no contrato consumidor;
2. produza-o no executor;
3. valide existência, hash e os invariantes mecanicamente verificáveis em `forja_run.py`;
4. revalide-o em `forja_package.py` se chegar ao pacote;
5. cubra caso nominal, ausência, adulteração e pareamento por sufixo;
6. registre-o no manifesto e no protocolo.

## Revisão

Toda alteração no editor final deve ser revisada sob dois ângulos independentes:

- qualidade do código e comportamento de falha;
- fidelidade jurídica/factual entre origem auditada e texto final.

O Fable 5 pode ajudar a revisar implementação ou texto, mas a aceitação depende de evidência reproduzível nos testes e gates locais.
