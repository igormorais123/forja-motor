# Relatório PSO-Pet — solução de problemas, formação de teses e valor mensurável

**Data:** 11/07/2026  
**Método:** PSO-PET-1.0  
**Estado:** implementado em sombra, sem alterar gates ou estados dos casos  
**Código:** `../forja_pso_pet.py`  
**Contrato:** `../pso_schemas/pso_case.schema.json`  
**Teste:** `../test_forja_pso_pet.py`  
**Telemetria real:** `PSO_PET_BENCHMARK_REAL_2026-07-11.json`

---

## 1. Conclusão executiva

A nova camada encontrou uma diferença importante entre **completude mecânica** e **qualidade do desenho da solução**.

Os quatro casos N4 auditados possuem artefatos estruturados, mas nenhuma das oito dimensões PSO-Pet foi produzida prospectivamente. Por isso, o sistema registra `not_measured`, nunca nota zero nem aprovação presumida.

Mesmo sem alterar os casos, a auditoria de compatibilidade encontrou 14 sinais acionáveis:

- três casos usam o próprio produto final como suporte exclusivo de ao menos uma pergunta;
- os quatro casos têm somente testes literais observáveis;
- três suítes são retrospectivas;
- três casos mantêm tese sem liberação conjunta de Helena e Cícero;
- Cafelana permanece bloqueada por fonte revogada.

O ganho não é “mais texto”. É tornar demonstráveis dimensões que antes permaneciam implícitas: definição do problema, coerência diagnóstica, alternativas, requisitos, mecanismo, validação, disciplina de contexto e aprendizado.

---

## 2. Arquitetura por partes

### Parte A — Núcleo do problema

Mantém em primeiro plano uma síntese curta com situação atual, estado desejado, lacuna, escopo, limites e resultado direto. O comando original permanece registrado, mas não controla sozinho a definição.

### Parte B — Pacotes de questão

Cada questão ativa recebe um pacote próprio:

- pergunta;
- referências de evidência;
- dependências;
- contexto excluído por ora;
- condição que exige reabertura.

Documento integral permanece no arquivo frio e é carregado quando a questão exigir. Texto bruto acima de 2.000 caracteres dentro do pacote gera alerta de contexto inflado.

### Parte C — História diagnóstica

Fatores são classificados como causa, sintoma, consequência, obstáculo ou oportunidade. Relações exigem justificativa. Casos completos ou intensivos exigem explicação rival e evidência capaz de discriminá-la.

### Parte D — Desenho da tese

A estratégia escolhida deve competir com ao menos uma alternativa substantivamente distinta nos perfis completo e intensivo. Alterar apenas o nome da opção não conta. Veículo, mecanismo e estratégia probatória formam a assinatura de distinção.

### Parte E — Validação e aprendizado

Requisitos materiais são rastreados até testes, evidências e limitações. O plano registra a melhor objeção, resposta, condições de falha e decisões localizadas do conselho. Depois da entrega, distingue resultado direto de desfecho judicial multicausal.

---

## 3. Indicadores vetoriais

Não existe média geral. Cada indicador é a proporção de critérios observáveis atendidos e publica seus próprios critérios. Um valor alto não compensa falha crítica em outra dimensão.

| Código | Indicador | O que mede | Antifraude |
|---|---|---|---|
| PDI | Integridade da definição do problema | estado atual, prova de entrada, estado desejado, lacuna, escopo, limites e resultado direto | produto final não pode provar a própria entrada |
| DCI | Coerência diagnóstica | história, fatores, relações, rival e elo atacável | lista de defeitos sem relações não pontua como diagnóstico |
| AQI | Qualidade das alternativas | viabilidade, distinção, objeção e razão comparativa | opções com mesma assinatura são duplicatas |
| RTI | Rastreabilidade dos requisitos | grupos, IDs, negociação, ligação a opções e validação | requisito material sem teste aparece como lacuna |
| MSI | Especificidade do mecanismo | como a intervenção atua sobre o diagnóstico para produzir resultado direto | descrição genérica de intenção não basta |
| VSI | Força da validação | objeção, resposta, falseabilidade, conselho e revisão independente | produtor e revisor iguais não aprovam |
| CDI | Disciplina de contexto | núcleo curto, pacotes por questão, referências e arquivo frio | despejo de texto é penalizado; ausência não vira “contexto completo” |
| LVI | Validade do aprendizado | resultado direto, desfecho final, rivais, observação e CIMO-Pet | porcentagem de vitória no plano não é aceita como evidência |

### Estado de prontidão

- `blocked`: existe P0 verificável;
- `not_ready`: alguma dimensão crítica PDI/DCI/RTI/VSI abaixo de 70;
- `human_review_required`: sem P0, mas alguma dimensão abaixo de 80;
- `ready_for_human_review`: todas as dimensões alcançam 80 ou mais;
- `not_evaluated`: o plano PSO-Pet não existe.

`ready_for_human_review` não significa pronto para protocolo. O gate jurídico da FORJA continua separado.

---

## 4. Bateria antifraude

### Mutações semânticas

Foram executadas 13 famílias:

1. retirar a prova do estado atual;
2. usar o produto final como prova de entrada;
3. tornar estado atual e desejado equivalentes;
4. confundir resultado direto com vitória final;
5. apagar história diagnóstica;
6. apagar explicação rival;
7. duplicar alternativa mudando apenas o rótulo;
8. deixar apenas uma opção em perfil completo;
9. remover rastreabilidade de requisitos;
10. selecionar alternativa inexistente;
11. apagar melhor objeção;
12. despejar texto bruto no contexto ativo;
13. falsificar a ordem temporal do congelamento.

Resultado: **13/13 detectadas; recall 100%**.

### Controles benignos

Foram executados cinco controles com mudanças legítimas: ampliar arquivo frio, acrescentar gatilho, manter opção não viável, reformular restrição negociável e plano base válido.

Resultado: **0/5 falsos bloqueios; especificidade 100%**.

Esses números medem somente o corpus atual. Não autorizam extrapolar 100% de precisão para todos os casos futuros.

---

## 5. Benchmark em casos reais

| Caso | P0 | P1 | Sinais PSO-Pet |
|---|---:|---:|---|
| Saúde | 0 | 4 | Q-001 circular; suíte retrospectiva; teste literal; conselho pendente |
| Cafelana | 1 | 1 | fonte de origem revogada; teste literal |
| Libra Sul | 0 | 4 | Q-001 e Q-003 circulares; suíte retrospectiva; teste literal; conselho pendente |
| Patrícia/Fábio | 0 | 4 | Q-001 circular; suíte retrospectiva; teste literal; conselho pendente |

### Interpretação correta da circularidade

O achado não prova que a resposta é falsa. Ele demonstra que, naquele artefato, a resposta é sustentada apenas pelo texto produzido, e não por uma fonte de entrada independente. A correção é ligar a pergunta ao documento primário e ao localizador, não apagar a resposta automaticamente.

### Dimensões não medidas

São 32 dimensões não medidas: oito em cada um dos quatro casos. Isso não significa 32 falhas. Significa que os casos anteriores não produziram `PSO_CASE.json` e, portanto, não permitem afirmar que definição, diagnóstico, alternativas e aprendizado foram medidos pelo novo contrato.

---

## 6. Testes de não regressão

- `test_forja_pso_pet.py`: 11/11 aprovados;
- suíte completa `_FORJA_HARNESS`: 141 testes aprovados, 2 exclusões previstas;
- compilação de `forja_pso_pet.py`: aprovada;
- benchmark leu casos reais sem modificar `state/`;
- relatório JSON foi gravado somente em `reports/`.

---

## 7. O que passa a mudar na elaboração

Em novos casos-piloto:

1. F2 escolhe perfil `light`, `full` ou `intensive`;
2. o núcleo do problema e os pacotes de questão são congelados antes do texto final;
3. F3/F4 constroem história diagnóstica e explicações rivais;
4. requisitos jurídicos, do destinatário, limites e restrições são separados;
5. casos completos/intensivos comparam duas intervenções realmente diferentes;
6. a estratégia escolhida explicita mecanismo, resultado direto e gatilho de mudança;
7. F7 valida requisitos, melhor objeção, condições de falha e conselho;
8. F10 registra resultado direto, explicações rivais e aprendizado CIMO-Pet.

---

## 8. Limites e próximos testes

O benchmark atual é retrospectivo. Ele comprova capacidade de detectar falhas conhecidas e lacunas de mensuração, mas ainda não mede:

- redução real do tempo de revisão;
- redução de alterações jurídicas feitas por Fábio;
- aumento do enfrentamento das teses pelo órgão julgador;
- estabilidade em tribunais e produtos distintos;
- taxa de falsos positivos em grande volume.

Esses valores exigem três ciclos prospectivos: leve, completo e intensivo. A promoção futura deve comparar retrabalho, omissões, mudança de sentido, tempo e decisões do conselho contra baselines equivalentes.

---

## 9. Comandos de verificação

```powershell
cd _FORJA_HARNESS
python -m unittest -v test_forja_pso_pet.py
python forja_pso_pet.py audit-case <caseId>
python forja_pso_pet.py validate-plan state\<caseId>\n4_artifacts\PSO_CASE.json
python forja_pso_pet.py write-example --output pso_schemas\PSO_CASE_EXAMPLE.json
python forja_pso_pet.py benchmark --output reports\PSO_PET_BENCHMARK_REAL_2026-07-11.json
python -m unittest discover -p 'test*.py'
```

---

## 10. Decisão de implantação

Manter PSO-Pet em sombra. O contrato e os indicadores estão tecnicamente prontos para pilotos prospectivos, mas nenhum indicador se torna bloqueante antes desses pilotos. A ausência do plano continua sendo `not_evaluated`, e não reprovação retroativa dos casos existentes.
