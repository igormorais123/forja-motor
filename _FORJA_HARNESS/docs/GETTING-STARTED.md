<!-- generated-by: gsd-doc-writer -->
# Primeiros passos

Este guia põe uma instalação local da FORJA em condições de validar contratos e executar a subfase F7-B de revisão e escrita final pelo Claude Fable 5. A FORJA é uma ferramenta operacional local; ela não protocola peças nem envia mensagens por conta própria.

## Pré-requisitos

- Windows com PowerShell.
- Python 3.10 ou superior disponível no `PATH`.
- Claude Code disponível no `PATH` e autenticado por OAuth na assinatura Claude Max do Igor.
- Microsoft Word para o fluxo final DOCX→PDF e o QA visual real.
- Para elementos visuais, o arsenal descrito em `../../_FERRAMENTAS/LEIA-ME.md`.

Não há `.env` nem chave de API obrigatória para F7-B. O executor recusa autenticação incompatível com `claude.ai` + assinatura `max`.

## Verificação inicial

Na pasta `_FORJA_HARNESS`:

```powershell
python --version
claude auth status
python forja_phase_contracts.py
python -m unittest -v test_forja_editorial.py
```

O último comando comprova o contrato editorial sem consumir uma sessão real do Fable 5. Para a regressão integrada, consulte `TESTING.md`.

## Fluxo mínimo de uma tentativa F7

1. Consulte o estado do caso e a revisão esperada.

   ```powershell
   python forja_state_machine.py <case-dir> status
   ```

2. Abra uma tentativa isolada de F7.

   ```powershell
   python forja_run.py <case-dir> start F7_AUDITORIA_JURIDICA_FACTUAL --expected-revision <n>
   ```

3. Produza e audite `audited_markdown.md` e `f7_gate_result.json`. O gate precisa comprovar ausência de P0.

4. Execute a revisão final.

   ```powershell
   python forja_editorial.py <case-dir> <attempt-dir> --source audited_markdown.md --f7-gate f7_gate_result.json
   ```

5. Incorpore os artefatos e gates de `FABLE5_RESULT.json` ao `PHASE_RESULT.json` integral da tentativa. Preserve os papéis contratuais de F7; o fragmento editorial não pode substituir o resultado da fase.

6. Promova somente depois de todos os gates passarem.

   ```powershell
   python forja_run.py <case-dir> promote <attempt-dir> --expected-revision <n>
   ```

## Resultado esperado

F7-B gera um bundle vinculado por hashes:

- `final_markdown.md`: cânone textual para F8;
- `editorial_report.json`: relatório estruturado da edição;
- `editorial_diff.patch`: diff auditável;
- `fable5_usage.json`: modelo, sessão e prova de autenticação;
- `editorial_fidelity.json`: gates determinísticos;
- `FABLE5_RESULT.json`: fragmento de resultado para promoção.

Se houver mais de um documento na mesma tentativa, use um sufixo estável:

```powershell
python forja_editorial.py <case-dir> <attempt-dir> --source audited_markdown_nota.md --f7-gate f7_gate_result.json --artifact-suffix _nota
```

O bundle inteiro recebe o mesmo sufixo. Nunca misture o `final_markdown` de um documento com o relatório ou a prova de uso de outro. O suporte a bundles adicionais existe no código, mas ainda não possui regressão dedicada; o bundle-base sem sufixo continua obrigatório.

## Próximas leituras

- `../PROTOCOLO_EDITORIAL_ESCRITA_FINAL.md`: operação completa e falhas.
- `ARCHITECTURE.md`: posição de F7-B no pipeline.
- `CONFIGURATION.md`: flags, contratos e autenticação.
- `DEVELOPMENT.md`: regras para alterar o código.
- `TESTING.md`: baterias e critérios de aceite.
