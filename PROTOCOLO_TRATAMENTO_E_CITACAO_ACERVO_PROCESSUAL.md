# Protocolo de tratamento e citação do acervo processual

Versão: 1.0 — 11/07/2026  
Origem metodológica: feedback do Prof. Fábio Medina Osório  
Aplicação: toda petição, memorial, parecer e manifestação da fábrica

## 1. Regra central: duas camadas

### Camada interna — cadeia de custódia

O ledger de trabalho registra nome e versão do arquivo, canal de obtenção, data, hash, página, evento/ID, vínculo com o ato processual e status de verificação. Essa camada serve à equipe e à auditoria. Pode usar marcadores como `[FONTE INTERNA]`, `[DECLARAÇÃO DO FÁBIO]`, `[INFERÊNCIA]` e `[NÃO VERIFICADO]`.

### Camada externa — linguagem do processo

A peça não revela como a equipe recebeu ou armazenou o documento. Ela indica apenas a posição processual da fonte e uma ponte conferível pelo julgador.

| Situação real | Fórmula externa admitida | Condição |
|---|---|---|
| Documento já juntado | “documento juntado aos autos no evento/ID X, p. Y” | evento/ID e página conferidos |
| Processo do STJ | “e-STJ fl. X” ou “e-STJ fls. X/Y” | paginação conferida na íntegra |
| Documento que acompanhará a peça | “Doc. 01 — [título objetivo]” / “documento anexo” | constar do rol e ser efetivamente anexado |
| Decisão | “decisão de [data], e-STJ fls. X/Y” | data, assinatura e dispositivo conferidos |
| Fonte oficial externa | tribunal/órgão, título, data e URL oficial | vigência e teor literal conferidos |

## 2. Fórmulas proibidas na peça

- “arquivo compartilhado pelo escritório”;
- “recebido por e-mail/WhatsApp”;
- “localizado/encontrado em pasta interna”;
- “arquivo local”, “arquivo do Drive”, caminho de computador ou nome técnico do pipeline;
- `[FONTE: arquivo]`, `[DECLARAÇÃO]`, `[INFERÊNCIA]`, `[VERIFICAR]` ou qualquer nota de produção.

“Documento juntado aos autos” não pode designar item ainda não protocolado. “Documento anexo” não pode designar item que não acompanhará a manifestação.

## 3. Versionamento que importa

O nome da versão, sozinho, não produz confiabilidade. Para cada fonte decisiva, o ledger deve responder:

1. qual ato processual ela representa;
2. quem o praticou e em que data;
3. qual ato foi impugnado;
4. qual pedido foi formulado;
5. qual foi o resultado e o efeito jurídico;
6. onde o fato aparece nos autos;
7. se existe versão posterior, retratação, integração ou substituição.

## 4. Gate para processos volumosos

Antes da redação, criar tabela com identificador único para cada ato. O blueprint só abre quando:

- a íntegra do ato atualmente impugnado foi lida;
- a cronologia não contém referentes ambíguos;
- decisão de reconsideração/retratação foi classificada pelo dispositivo, não por suposição;
- omissões, recursos cabíveis e possível preclusão foram mapeados;
- divergências entre declaração humana e metadados dos autos estão explícitas.

Se qualquer item decisivo faltar, o produto recebe `internal_working`; nenhuma versão protocolável é gerada.

## 5. Gate automático e revisão humana

O verificador FORJA deve bloquear como P0 vazamentos de e-mail, WhatsApp, Drive, pasta interna, caminho local e compartilhamento. A revisão humana final confirma, ainda, que cada “Doc. X”, evento, ID e folha realmente corresponde ao documento citado.
