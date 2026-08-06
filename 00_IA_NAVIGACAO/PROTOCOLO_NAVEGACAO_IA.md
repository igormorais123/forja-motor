<!-- IA_NAVIGACAO:GERADO_AUTO:v1 -->
# Protocolo de Navegação IA

Atualizado automaticamente em: **2026-08-06 02:12:36 -0300**

## Objetivo

Dar a qualquer IA um GPS operacional desta pasta: onde começar, que arquivos ler, quando subir ou descer na árvore e como evitar alucinação em trabalho jurídico.

## Ordem padrão

1. Na raiz, ler `AGENTS.md`, `CLAUDE.md`, este protocolo e `MAPA_IA.md`.
2. Escolher a pasta do caso/demanda pelo índice geral.
3. Dentro da pasta alvo, ler o `MAPA_IA.md` local.
4. Ler `COMANDO_DO_EMAIL.md`, `COMANDO_DO_WHATSAPP.md` ou `COMANDO_MANUAL.md`, quando houver.
5. Ler mapas, índices, planos, dossiês, briefs e contexto antes de anexos pesados.
6. Em peça judicial, ler regimento local e `_LEIS_GERAIS` antes de redigir.
7. Verificar fontes primárias para fatos, citações, datas, IDs e jurisprudência.
8. Só depois abrir peças, versões finais, relatórios, QA visual, renders e builds.

## Leitura por tipo de pasta

- `Anexos do email`, `Autos Drive`, `Documentos`: fonte primária ou material recebido; não resumir sem leitura.
- `Links pendentes`: demanda de coleta/baixa; confirmar link antes de tratar como arquivo disponível.
- `_build`, `_extract`, `render`, `QA`, `pages`, `img`: artefato técnico; útil para validar entrega, não para fundamentar fato.
- `_trabalho`, `PLANEJAMENTO`, `visual_law`: produção intermediária; checar se há versão final mais recente.
- `gestao_escritorio`: painel e dados operacionais; manter WhatsApp/Gmail em nível sanitizado.

## Regra jurídica crítica

Toda peça deve identificar tribunal, cabimento, órgão competente, prazo, sustentação oral e impactos regimentais. Se faltar regimento local, a IA deve baixar a consolidação oficial mais recente, converter integralmente para Markdown e registrar fonte/data antes de redigir.

## Marcação de incerteza

- `[FONTE: arquivo]`: quando a informação foi lida no arquivo indicado.
- `[DECLARAÇÃO]`: quando vem de instrução do usuário ou comando, sem prova documental conferida.
- `[INFERÊNCIA]`: quando é conclusão lógica a partir de fontes.
- `[NÃO VERIFICADO]` ou `[VERIFICAR]`: quando ainda não há lastro suficiente para peça.
