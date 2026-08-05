# FORJA R1 — Contexto travado

**Coletado:** 2026-07-15  
**Status:** pronto para planejamento  
**Origem:** pedido do Igor + pesquisa profunda do codebase

<domain>
## Limite do programa

Planejar e, em etapa posterior separada, executar uma refatoração estrutural segura da FORJA para reduzir duplicidade acidental, aplicar boas práticas, modularizar, organizar o código e criar documentação Mermaid viva. Este pacote não executa a refatoração.

</domain>

<decisions>
## Decisões de implementação

### Preservação

- N2 permanece vigente; N3 e N4 conservam seus modos atuais.
- Gates jurídicos, event store, hashes, locks, replay, contratos históricos e QA real são preservados.
- Duplicação defensiva não será removida apenas por repetição textual.
- Toda movimentação terá teste de caracterização, fachada compatível e rollback.
- Toda exclusão futura exigirá backup verificável, prova de substituição e ensaio de restore.

### Ordem

- Corrigir os quatro gates P0 e a régua de testes antes de mover fronteiras.
- Criar baseline isolado; não executar a refatoração sobre o workspace operacional sujo.
- Extrair infraestrutura neutra antes de reorganizar domínio, CLIs ou diretórios.
- Centralizar catálogos antes de gerar schemas, docs e índices.
- Remover shims somente após replay, testes reais e janela de telemetria sem uso.

### Arquitetura

- Arquitetura-alvo em `src/forja`: `core`, `domain`, `application`, `ports/adapters`, `rendering` e `cli`.
- `forja_n3_common.py` vira fachada temporária, não é removido de uma vez.
- N2 entra por adaptadores; N3 permanece runtime; N4 continua camada candidata de contratos e gates.
- Integrações com Word, gestão, busca e filesystem passam por portas explícitas.
- Documentação arquitetural deve ser gerada ou validada contra AST e catálogos.

### Qualidade

- TDD é obrigatório para lógica com input/output definido, validadores, estados, catálogos, seleção e promoção.
- Reorganização, configuração, documentação e migrações usam planos executivos com testes de caracterização.
- Testes reais com Word/PDF/telemetria permanecem gate de conclusão.
- Nenhum “verde” é aceito sem prova de cobertura da própria régua.

### Discrição técnica do executor

- detalhes internos de classes, nomes auxiliares e sequência dentro de uma tarefa;
- escolha do gerenciador/lock compatível com o Python suportado;
- divisão interna de funções após preservação do contrato público;
- formato exato da telemetria de shims, desde que sanitizado e verificável.

</decisions>

<canonical_refs>
## Referências canônicas

### Norma e governança

- `AGENTS.md` — regras invioláveis da fábrica.
- `FORJA_SPEC_MANIFEST.json` — precedência e estado N2/N3/N4.
- `FORJA_N3_CONFIG.json` — flags e modo candidato.
- `planejamento/01_PRD_FORJA.md` — produto N2 vigente.
- `planejamento/05_FORJA_NIVEL_2_ANALISE_E_PLANO_CORRIGIDO.md` — razões e contrato N2.
- `planejamento/06_GATES_QUALIDADE_FORJA.md` — gates jurídicos e visuais.

### Candidatas e compatibilidade

- `planejamento/08_PLANO_FORJA_N3_INTEGRIDADE_VISUAL_E_GESTAO.md` — integridade N3.
- `planejamento/10_PRD_FORJA_N4_RACIOCINIO_PROVA_CIENCIA.md` — produto N4 candidato.
- `planejamento/11_TDD_FORJA_N4_RACIOCINIO_PROVA_CIENCIA.md` — contratos técnicos N4.
- `planejamento/12_ROADMAP_FORJA_N4_RACIOCINIO_PROVA_CIENCIA.md` — promoção N4.
- `planejamento/20_F2A_EXPLORACAO_100_PERGUNTAS.md` — F2-A obrigatório.

### Pesquisa estrutural

- `.planning/codebase/ARCHITECTURE.md` — arquitetura observada.
- `.planning/codebase/CHANGE_IMPACT.md` — mapa de impacto.
- `.planning/codebase/CONCERNS.md` — riscos P0/P1/P2.
- `.planning/codebase/TESTING.md` — cobertura e lacunas da régua.
- `.planning/codebase/STRUCTURE.md` — estrutura e duplicidades físicas.

</canonical_refs>

<deferred>
## Fora do escopo

- promover N3 ou N4;
- alterar conteúdo jurídico de peças;
- novo banco, RAG, LLM-as-judge, fine-tuning ou infraestrutura paga;
- envio automático, protocolo ou assinatura;
- limpeza destrutiva de estados e evidências;
- reescrita geral do sistema.

</deferred>
