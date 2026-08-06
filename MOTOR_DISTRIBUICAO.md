# Contrato do FORJA Motor

Este repositório é somente o motor genérico da FORJA. Ele deve ser
indistinguível de um sistema que qualquer escritório possa clonar, executar,
adaptar e compartilhar.

## O que pertence aqui

- código, contratos, schemas, testes e ferramentas reutilizáveis;
- regras de execução que não dependem de uma banca concreta;
- documentação do comportamento do motor sem nomes, contatos ou caminhos
  privados;
- interfaces que acessam dados externos pela porta de acervo, sem embutir os
  valores no código.

## O que não pertence aqui

Tudo que identifica ou descreve uma instalação específica deve ficar em
`forja-auditoria`, incluindo:

- nome, marca, logotipo, domínio, endereço, contatos e identidade visual do
  escritório;
- dados pessoais de sócios, advogados, equipe, clientes ou terceiros;
- configurações locais, contas, destinatários, vigias, demandas e rotinas do
  escritório;
- casos, processos, documentos, relatórios, modelos aprovados e histórico de
  execução;
- qualquer exemplo que permita reconhecer a banca, uma pessoa ou um caso real.

Se o motor precisar de um valor específico, ele deve pedi-lo pela interface de
acervo. Sem o acervo montado, o resultado correto é declarar `não verificado`,
não inventar uma configuração padrão.

## Divisão física no PC

A separação é também de diretórios, não apenas de etiquetas no Git:

```text
%USERPROFILE%\repos\
├── forja-motor       # genérico e compartilhável
└── forja-auditoria   # privado e específico da instalação
```

Os diretórios são repositórios Git independentes. Nunca juntar os dois em
um repositório público, nem resolver a separação apenas por uma pasta
`motor/` dentro do acervo. A rotina de sincronização deve preservar esses dois
destinos físicos e a fronteira `MOTOR`/`ACERVO` deve continuar sendo verificada
antes de qualquer publicação.
