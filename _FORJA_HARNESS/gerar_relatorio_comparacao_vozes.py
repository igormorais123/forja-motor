"""Gera o relatório HTML da comparação das cinco vozes curtas.

Determinístico: lê `telemetria/COMPARACAO_VOZES_DADOS.json` e escreve o HTML.
Nenhum texto de observação é transcrito à mão — a regra da casa desde 09/07/2026
é que agente que transcreve resume, e 5 de 5 resumiram 80-95% do original.
"""

from __future__ import annotations

import html
import json
from pathlib import Path

FORJA = Path(__file__).resolve().parent
DADOS = FORJA / "telemetria" / "COMPARACAO_VOZES_DADOS.json"
SAIDA = FORJA / "reports" / "COMPARACAO_VOZES_CURTAS_2026-08-08.html"
SAIDA_ANONIMA = FORJA / "reports" / "COMPARACAO_VOZES_CURTAS_2026-08-08_PUBLICAVEL.html"

ROTULOS = {
    "kimi-k3-cursor": "Kimi K3",
    "glm-5.2-cursor": "GLM 5.2",
    "grok-4.5-cursor": "Grok 4.5",
    "luna-5.6-cursor": "Luna 5.6 max",
    "opus-5-cursor": "Opus 5",
}
# O rótulo de cada caso vem do arquivo de dados, que é acervo, e não de um mapa
# escrito aqui. A versão anterior trazia três nomes de cliente no código do
# motor: o relatório é genérico, os casos que ele mede não são, e quem escreve
# o gerador não precisa saber de quem é a peça.
ANONIMO = False


def rotulo_caso(slug: str, dados: dict) -> str:
    """Nome do caso — real na versão local, neutro na versão que sai da máquina.

    A primeira publicação levou nome de cliente e trecho analítico sobre a peça
    dele para uma URL externa. A fronteira MOTOR/ACERVO já dizia que informação
    do escritório não sai; eu tratei o relatório como se ele fosse só sobre
    modelos, quando metade do conteúdo é sobre as peças dos clientes.

    `--anonimo` gera a versão publicável: os casos viram Caso A, B, C. O que se
    perde é saber de qual cliente é cada observação, e isso não faz falta para
    comparar modelos — que é o assunto do relatório.
    """
    if ANONIMO:
        ordem = sorted((dados.get("rotulosCaso") or {}))
        letra = chr(ord("A") + ordem.index(slug)) if slug in ordem else "?"
        return f"Caso {letra}"
    return (dados.get("rotulosCaso") or {}).get(slug, slug)


def e(texto) -> str:
    return html.escape(str(texto if texto is not None else ""))


def n(valor: int) -> str:
    """Milhar com ponto, à brasileira.

    Existe porque a primeira versão formatava com `f"{v:,}"` e depois fazia
    `.replace(",", ".")` no bloco inteiro — o que **comeu as vírgulas das 60
    observações**, trocando pontuação de texto que eu tinha me comprometido a não
    alterar. O gate de fidelidade no fim deste arquivo pega isso agora; a função
    é para não haver o que pegar.
    """
    return f"{valor:,}".replace(",", ".")


def bloco_prompt(d: dict) -> str:
    p = d["prompt"]
    t = p["tetos"]
    return f"""
<h2 id="tarefa">1 · A tarefa exata que foi pedida às cinco vozes</h2>

<p>O texto abaixo é o que foi enviado, palavra por palavra. As cinco leram o
mesmo recorte do mesmo documento e responderam sem histórico de conversa.</p>

<div class="aviso aviso-negativo">
<h4>Correção: as instruções <em>não</em> foram idênticas</h4>
<p>A primeira versão desta página afirmava que nenhuma das cinco recebeu
instrução diferente. <strong>Era falso.</strong> O código acrescenta um bloco
exclusivo ao Kimi K3, porque ele carrega a restrição <code>nao_afirma_fato</code>:</p>
<pre class="prompt">{e(d['prompt']['acrescimoRestrito'])}</pre>
<p>A consequência é direta: o resultado do K3 na coluna <code>viol%</code> não é
comparável ao das outras quatro, porque só ele foi avisado por escrito de que
não seria lido como fonte. Achado do revisor externo.</p>
</div>

<h3>Instrução de sistema</h3>
<pre class="prompt">{e(p['sistema'])}</pre>

<h3>Molde da pergunta</h3>
<pre class="prompt">{e(p['molde'])}</pre>

<h3>Aviso acrescentado quando o documento não cabe no recorte</h3>
<p class="nota">Este bloco só entra quando o alvo passa do teto. Ele existe por
causa de um defeito medido: nas três primeiras execuções, sem ele, as vozes
gastaram 3 de 24 observações reclamando de um truncamento que era nosso, e duas
delas <strong>afirmaram que a peça estava incompleta</strong> — falso, e com cara
de achado acionável.</p>
<pre class="prompt">{e(p['avisoRecorte'])}</pre>

<h3>Tetos, e por que eles estão no código e não no prompt</h3>
<p>Pedir brevidade a um modelo é sugestão. Estes limites são aplicados na
extração da resposta, não confiados à obediência:</p>
<div class="tabela-rolo">
<table>
<thead><tr><th>Limite</th><th>Valor</th><th>Onde age</th></tr></thead>
<tbody>
<tr><td>Recorte do documento enviado</td><td class="num">{n(t['alvo'])} caracteres</td>
    <td>corta o alvo antes de enviar; o corte é declarado ao modelo</td></tr>
<tr><td>Observações por voz</td><td class="num">{t['obs']}</td>
    <td>as excedentes são descartadas e a contagem fica no artefato</td></tr>
<tr><td>Caracteres por observação</td><td class="num">{t['chars']}</td>
    <td>o que passa é cortado e marcado com reticência</td></tr>
<tr><td>Orçamento de saída</td><td class="num">{t['maxTokens']} tokens</td>
    <td>teto da chamada ao modelo</td></tr>
</tbody></table>
</div>
"""


def bloco_modelos(d: dict) -> str:
    linhas = []
    for vid, m in d["modelos"].items():
        controle = ('<span class="chip chip-controle">controle</span>'
                    if m["controle"] else "")
        restr = ('<span class="chip chip-alerta">não afirma fato</span>'
                 if m["restricoes"] else "—")
        linhas.append(f"""<tr>
<td><strong>{e(ROTULOS[vid])}</strong> {controle}<br><code>{e(vid)}</code></td>
<td>{e(m['familia'])}</td>
<td><code>{e(m['remoto'])}</code></td>
<td>assinatura Cursor</td>
<td class="num">US$ 0,00</td>
<td>{restr}</td>
</tr>""")
    return f"""
<h2 id="vozes">2 · Quem correu, e sob que condição</h2>

<div class="tabela-rolo">
<table>
<thead><tr><th>Voz</th><th>Família</th><th>Identificador no Cursor</th>
<th>Rota</th><th>Custo marginal</th><th>Restrição</th></tr></thead>
<tbody>{''.join(linhas)}</tbody></table>
</div>

<div class="aviso">
<h4>Duas leituras que mudam a interpretação de tudo abaixo</h4>
<p><strong>Opus 5 é controle, não concorrente.</strong> É a mesma família que
escreve a peça e que faz a revisão editorial de F7-B. Quando ele concorda com a
análise principal, isso é eco previsível, não confirmação. Ele está na prova para
dar escala: sem um modelo de ponta na mesma tarefa, o número de uma voz nova não
tem régua.</p>
<p><strong>Kimi K3 carrega uma restrição medida.</strong> Na bancada de fidelidade
à fonte de 26/07/2026 ele fez 2 de 6 corretas na condição cautelosa, com 2
invenções, e <strong>0 de 6 na condição solta, com 4 invenções</strong> — o Grok,
na mesma prova solta, fez 6 de 6. Isso não o desqualifica como olhar; desqualifica
como fonte. Nada que ele diga entra na peça como dispositivo, número ou data.</p>
<p><strong>Todas as cinco pela assinatura, e isso não é detalhe de contabilidade.</strong>
<code>gpt-5.6-luna-max</code> existe no Cursor. A rota alternativa do Luna, no
OpenRouter, cobra US$ 1 por milhão de entrada e US$ 6 de saída — ela continua no
registro para quem precisar, e o painel não a usa.</p>
</div>

<h3>Grau de esforço: uma assimetria deliberada</h3>
<p>Quatro vozes correram no grau <code>high</code>. O Luna correu em
<code>max</code>, por pedido expresso. Comparação com esforço desigual mede o
esforço, não o modelo — então esta é a única diferença de configuração e ela está
declarada aqui para não ser lida como resultado.</p>
"""


def bloco_alvos(d: dict) -> str:
    linhas = []
    for a in d["alvos"]:
        linhas.append(f"""<tr>
<td><strong>{e(rotulo_caso(a['caso'], d))}</strong></td>
<td>{e(a['fase'])}</td>
<td><code>{e(a['arquivo'])}</code></td>
<td class="num">{n(a['caracteres'])}</td>
<td class="num">{n(a['caracteresEnviados'])}</td>
<td>{a['fracaoVista']}%</td>
</tr>""")
    return f"""
<h2 id="alvos">3 · Sobre o que elas opinaram</h2>

<p>Três documentos de trabalho reais da esteira, um por caso, todos de F7 — a
fase em que a peça é auditada. Nenhum é dos autos: são o nosso próprio produto,
que é exatamente o que se quer submeter a um olhar de fora.</p>

<div class="tabela-rolo">
<table>
<thead><tr><th>Caso</th><th>Fase</th><th>Arquivo</th>
<th>Caracteres do documento</th><th>Caracteres enviados</th><th>Fração vista</th></tr></thead>
<tbody>{''.join(linhas)}</tbody></table>
</div>

<p class="nota"><strong>Os três foram truncados</strong>, e as vozes foram
avisadas disso. No alvo mais longo as vozes viram 16% do documento. A versão
anterior desta tabela dividia o recorte em <em>caracteres</em> por um total em
<em>bytes</em> e publicava 58%, 44% e 15% — números que não eram fração de nada.
Achado do revisor externo.
Qualquer conclusão delas sobre o fecho, os pedidos ou a conclusão da peça está
fora de alcance por construção — e é por isso que o aviso de recorte existe.</p>
"""


def bloco_indicadores() -> str:
    return """
<h2 id="indicadores">4 · Os indicadores: o que cada um mede, e o que não mede</h2>

<p>Todos são calculados por máquina, sem julgamento humano em nenhuma etapa.
Isso é a força e o limite deles ao mesmo tempo: medem <strong>disciplina</strong>,
não qualidade. Nenhum número desta página promove um modelo a nada.</p>

<div class="fichas">

<article class="ficha">
<h4>viol% — citou fonte que não está no documento</h4>
<p class="como">Extrai de cada observação toda menção a súmula, artigo, tema ou
lei com número, ignorando o que estiver entre aspas, e procura aquele número no
recorte que a voz recebeu.</p>
<p class="serve">Serve porque separa <em>ler</em> de <em>inventar</em>. Citar o
que o documento cita é leitura. Citar o que não está lá é invenção — e invenção é
o modo de falha que a bancada mediu no K3.</p>
<p class="nao">Não serve para dizer se a citação é correta no mundo. Só diz se
ela veio do documento.</p>
<p class="hist">Mudou duas vezes, as duas por falso positivo real. Nasceu
puramente lexical e acusou o GLM por escrever <code>"Súmula 7 …" é a tese inteira
comprada sem verificação</code> — citação entre aspas, criticando o blueprint.
Excluí aspas. Acusou de novo, agora sem aspas: <code>a própria Súmula 5/7 que ele
invoca pode funcionar contra</code>. Também correto. Continuar refinando a regex
até concordar comigo seria moldar o instrumento; a distinção real é de origem, não
de sintaxe.</p>
</article>

<article class="ficha">
<h4>teto% — observações cortadas no limite</h4>
<p class="como">Proporção de observações que terminam em reticência de corte, ou
seja, que bateram nos 300 caracteres.</p>
<p class="serve">Serve porque bater no teto não é o mesmo que escrever bem: o
leitor recebe uma frase pela metade e o resto do raciocínio não chega. Numa voz
que existe para ser curta, é o indicador de aderência ao formato.</p>
<p class="nao">Não diz que o conteúdo era ruim. Diz que uma parte dele não
chegou.</p>
</article>

<article class="ficha">
<h4>chars — caracteres médios por observação</h4>
<p class="como">Média simples do tamanho das observações válidas.</p>
<p class="serve">Serve como perfil de densidade, e para ler o teto% junto: uma
voz com média perto do teto vai bater nele com frequência.</p>
<p class="nao">Mais curto não é melhor nem pior. É perfil.</p>
</article>

<article class="ficha">
<h4>sobrMed — sobreposição lexical com a voz mais próxima</h4>
<p class="como">Para cada observação, o índice de Jaccard sobre palavras de
conteúdo contra a observação mais parecida das outras vozes no mesmo painel.
Média por voz.</p>
<p class="serve">Deveria servir para detectar eco — voz que diz o que outra já
disse. <strong>Medido, não serve.</strong></p>
<p class="nao">Não alcança paráfrase, e não distingue as vozes entre si. Ver a
seção 6.</p>
</article>

<article class="ficha">
<h4>repet — repetição da própria voz entre casos</h4>
<p class="como">Maior sobreposição lexical entre observações da mesma voz em
<em>casos diferentes</em>.</p>
<p class="serve">Serve porque valor alto significa texto genérico: a voz está
produzindo o mesmo comentário para qualquer documento em vez de ler o que está na
frente dela.</p>
<p class="nao">Com três casos, é um sinal fraco. Serve para o extremo, não para
ranquear.</p>
</article>

<article class="ficha">
<h4>seg — segundos por painel</h4>
<p class="como">Tempo de parede da chamada, do envio à resposta completa.</p>
<p class="serve">Serve porque o painel roda dentro de uma fase e o tempo entra no
custo real de usá-lo. Cinco vozes em sequência somam.</p>
<p class="nao">Varia com carga do provedor. Três medições por voz é pouco para
tratar diferença pequena como estável.</p>
</article>

</div>
"""


def bloco_resultado(d: dict) -> str:
    ms = d["indicadores"]["modelos"]
    ordem = ["kimi-k3-cursor", "glm-5.2-cursor", "grok-4.5-cursor",
             "luna-5.6-cursor", "opus-5-cursor"]
    por_id = {m["modelo"]: m for m in ms}
    linhas = []
    for vid in ordem:
        m = por_id[vid]
        controle = ' <span class="chip chip-controle">controle</span>' if \
            d["modelos"][vid]["controle"] else ""
        destaque = ' class="destaque-ruim"' if m["noTetoPct"] > 25 else ""
        linhas.append(f"""<tr>
<td><strong>{e(ROTULOS[vid])}</strong>{controle}</td>
<td class="num">{m['observacoes']}</td>
<td class="num">{m['casos']}</td>
<td class="num bom">{m['taxaViolacao']:.1f}</td>
<td class="num"{destaque}>{m['noTetoPct']:.1f}</td>
<td class="num">{m['caracteresMedios']}</td>
<td class="num">{m['sobreposicaoMedia']:.3f}</td>
<td class="num">{m['repeticaoEntreCasos']:.3f}</td>
<td class="num">{m['segundosMedio']:.1f}</td>
</tr>""")
    seg_total = sum(m["segundosMedio"] for m in ms)
    return f"""
<h2 id="resultado">5 · O resultado comparado</h2>

<p><strong>60 observações. 5 vozes × 3 casos × 4 observações.</strong> Custo
total em dinheiro: US$ 0,00. Custo total em tempo de máquina:
{seg_total:.0f} segundos por documento com as cinco em sequência.</p>

<div class="tabela-rolo">
<table class="principal">
<thead><tr>
<th>Voz</th><th>obs</th><th>casos</th><th>viol%</th><th>teto%</th>
<th>chars</th><th>sobrMed</th><th>repet</th><th>seg</th>
</tr></thead>
<tbody>{''.join(linhas)}</tbody></table>
</div>

<h3>O que se lê nessa tabela</h3>

<div class="aviso aviso-negativo">
<h4>Leia esta tabela como descrição de três execuções, não como ranking</h4>
<p>Cada linha vem de <strong>3 chamadas</strong> ao modelo, não de 12 medições
independentes: as quatro observações de um painel saem da mesma geração, com o
mesmo contexto e o mesmo estado. Não houve repetição, nem randomização da ordem
das chamadas, nem semente registrada. Não há intervalo de confiança calculável.</p>
<p>Duas condições também não foram iguais: o <strong>Luna correu em
<code>max</code></strong> e as outras quatro em <code>high</code>; e o
<strong>Kimi K3 recebeu uma instrução a mais</strong>. Qualquer diferença entre
esses dois e o resto pode ser a condição, não o modelo.</p>
</div>

<div class="achados">

<article class="achado achado-ruim">
<h4>O GLM 5.2 citou duas fontes que não estavam no que leu</h4>
<p>Duas de doze observações trazem súmulas ausentes do recorte. O prompt proíbe
citar lei, artigo, súmula ou precedente — então isto é <strong>desobediência ao
formato</strong>. <strong>Não é prova de invenção:</strong> as súmulas existem e
são pertinentes ao caso; elas só não estavam no texto que a voz recebeu.</p>
<p class="dado">A versão anterior desta página dizia que <em>nenhuma das cinco
inventou citação</em>. O detector que sustentava a frase absolvia qualquer
citação cujo número aparecesse como sequência de dígitos em qualquer ponto do
documento — <code>Súmula 7</code> passava por causa de um <code>7</code> dentro
de uma data. Corrigido e remedido: o zero virou 2 em 60.</p>
</article>

<article class="achado">
<h4>Sete observações do GLM foram cortadas pelo nosso código</h4>
<p>Ele escreve com média de 286 caracteres contra um teto de 300 que
<strong>nós escolhemos</strong>; as outras quatro vozes ficam entre 192 e 256 e
nunca encostam no limite. O que a coluna <code>teto%</code> mede é aderência a
uma especificação nossa, não qualidade nem profundidade.</p>
<p class="dado">Registro de um duplo padrão que estava nesta página: três
observações do K3 foram <em>excluídas</em> do placar porque reclamavam de um
truncamento causado por nós, com a justificativa de que não se cobra do modelo o
erro de quem montou o prompt. As sete do GLM, cortadas por um limite igualmente
nosso, eram <em>contadas contra ele</em>. Mesma classe, tratamento oposto.</p>
</article>

<article class="achado">
<h4>Tempos observados, em ordem fixa de chamada</h4>
<p>GLM 21,0 s · Luna 28,2 s · Grok 33,0 s · K3 33,5 s · Opus 37,4 s. As chamadas
sempre correram na mesma sequência, com o Opus por último, e não foram
intercaladas nem repetidas. Carga do provedor e posição na fila ficam
confundidas com identidade do modelo: isto descreve <strong>estes três
runs</strong>, não uma propriedade do modelo.</p>
</article>

<article class="achado">
<h4>Baixa repetição de vocabulário da mesma voz entre casos</h4>
<p>Entre 0,059 e 0,135. A versão anterior lia isso como <em>todas leem o
documento em vez de repetir fórmula</em>. Não se sustenta: baixa coincidência de
palavras não prova leitura, e a própria página mostra um par semanticamente
idêntico com 0,091. O que o número diz é apenas que as vozes não repetem
literalmente o mesmo texto entre casos.</p>
</article>

</div>
</div>
"""


def bloco_convergencia(d: dict) -> str:
    ordem = ["glm-5.2-cursor", "grok-4.5-cursor", "kimi-k3-cursor",
             "luna-5.6-cursor", "opus-5-cursor"]
    conv = d["convergencia"]

    def val(a, b):
        return conv.get(f"{a}|{b}") or conv.get(f"{b}|{a}")

    cabeca = "".join(f"<th>{e(ROTULOS[v])}</th>" for v in ordem)
    linhas = []
    todos = [v for v in conv.values()]
    lo, hi = min(todos), max(todos)
    for a in ordem:
        celulas = []
        for b in ordem:
            if a == b:
                celulas.append('<td class="diag">—</td>')
                continue
            v = val(a, b)
            # Intensidade proporcional dentro da faixa observada, só para leitura.
            frac = (v - lo) / (hi - lo) if hi > lo else 0
            celulas.append(f'<td class="num" style="--i:{frac:.2f}">{v:.3f}</td>')
        linhas.append(f"<tr><th>{e(ROTULOS[a])}</th>{''.join(celulas)}</tr>")
    return f"""
<h2 id="convergencia">6 · Convergência entre as vozes — e o resultado negativo</h2>

<p>A pergunta era: alguma dupla se parece mais entre si do que com as outras? Se
sim, isso daria um mapa de redundância — e diria quais duas manter e quais cortar.</p>

<div class="tabela-rolo">
<table class="matriz">
<thead><tr><th></th>{cabeca}</tr></thead>
<tbody>{''.join(linhas)}</tbody></table>
</div>

<div class="aviso aviso-negativo">
<h4>Não há estrutura nenhuma. Os dez pares ficaram entre {lo:.3f} e {hi:.3f}.</h4>
<p>Média geral 0,053. A diferença entre o par mais próximo e o mais distante é
ruído com doze observações por voz. <strong>A régua lexical não distingue as
vozes por conteúdo.</strong></p>
<p>Este é o terceiro resultado negativo seguido da camada automática no eixo de
conteúdo, e os três apontam o mesmo limite:</p>
<ol>
<li>Um par de eco que uma pessoa identificou deu <strong>0,091</strong> de
sobreposição — vocabulário quase disjunto dizendo a mesma coisa. Baixar o limiar
para capturá-lo passaria a marcar pares comprovadamente não relacionados, que
deram 0,147.</li>
<li>O perfil <em>posicional</em> — a hipótese de que cada voz olha partes
diferentes do documento — deu negativo: distribuição quase idêntica pelos terços
do texto.</li>
<li>A convergência par a par, esta tabela, é plana.</li>
</ol>
<p>Consequência prática: <code>viol%</code>, <code>teto%</code>,
<code>repet</code> e <code>seg</code> são medidas úteis. <code>sobrMed</code> e o
eco automático não são. <strong>Qual voz serve para quê não sai de máquina.</strong></p>
</div>
"""


def bloco_observacoes(d: dict) -> str:
    por_caso = {}
    for o in d["observacoes"]:
        por_caso.setdefault(o["caso"], {}).setdefault(o["modelo"], []).append(o)
    secoes = []
    # a ordem dos casos vem dos alvos declarados no arquivo de dados; lista
    # fixa aqui seria mais um lugar do motor guardando quem é o cliente
    for caso in [a["caso"] for a in d["alvos"]]:
        alvo = next(a for a in d["alvos"] if a["caso"] == caso)
        blocos = []
        for vid in ("kimi-k3-cursor", "glm-5.2-cursor", "grok-4.5-cursor",
                    "luna-5.6-cursor", "opus-5-cursor"):
            itens = []
            for o in por_caso[caso][vid]:
                marcas = []
                if o["cortadaPeloHarness"]:
                    marcas.append('<span class="chip chip-alerta">cortada pelo nosso código</span>')
                if o["citouFora"]:
                    marcas.append('<span class="chip chip-alerta">citou fonte ausente do recorte</span>')
                itens.append(f"""<li data-voz="{e(vid)}">
<p class="obs">{e(o['texto'])}</p>
<p class="meta"><code>{e(o['obsId'])}</code> · {o['chars']} caracteres ·
ancoragem {o['ancoragem'] if o['ancoragem'] is not None else 'n/d'}
{' '.join(marcas)}</p></li>""")
            controle = ' <span class="chip chip-controle">controle</span>' if \
                d["modelos"][vid]["controle"] else ""
            blocos.append(f"""<div class="voz-bloco" data-voz="{e(vid)}">
<h4>{e(ROTULOS[vid])}{controle}</h4>
<ol class="obs-lista">{''.join(itens)}</ol></div>""")
        secoes.append(f"""<section class="caso">
<h3>{e(rotulo_caso(caso, d))} <span class="caso-meta">{e(alvo['fase'])} ·
<code>{e(alvo['arquivo'])}</code> · {n(alvo['caracteres'])} caracteres, {alvo['fracaoVista']}% visto</span></h3>
{''.join(blocos)}</section>""")
    return f"""
<h2 id="observacoes">7 · As 60 observações, na íntegra</h2>

<p>Tudo que as cinco vozes disseram, sem seleção. <strong>Sete das sessenta
não estão na íntegra:</strong> elas passaram do teto de 300 caracteres e foram
cortadas <em>pelo nosso código</em>, não pelo modelo — as sete são do GLM 5.2 e
estão marcadas. O texto bruto anterior ao corte não foi preservado, então essas
sete não são auditáveis. É um defeito do instrumento, apontado pelo revisor
externo, e o conserto é preservar a resposta bruta nas próximas rodadas.</p>

<div class="filtro" role="group" aria-label="Filtrar por voz">
<button type="button" class="ativo" data-filtro="todas">Todas</button>
<button type="button" data-filtro="kimi-k3-cursor">Kimi K3</button>
<button type="button" data-filtro="glm-5.2-cursor">GLM 5.2</button>
<button type="button" data-filtro="grok-4.5-cursor">Grok 4.5</button>
<button type="button" data-filtro="luna-5.6-cursor">Luna 5.6</button>
<button type="button" data-filtro="opus-5-cursor">Opus 5</button>
</div>

{''.join(secoes)}
"""


def bloco_decisao() -> str:
    return """
<h2 id="decisao">8 · As três decisões, com o trade-off de cada uma</h2>

<p>Nenhuma é técnica. As três são de escopo, e por isso não as tomei.</p>

<article class="decisao">
<h3>Decisão 1 · Quantas vozes em produção</h3>
<table class="tradeoff">
<thead><tr><th>Opção</th><th>Ganha</th><th>Perde</th><th>Custo humano por documento</th></tr></thead>
<tbody>
<tr><td><strong>Duas vozes</strong></td>
<td>fila curta, leitura completa provável</td>
<td>menos ângulos; se as duas convergirem, o painel não acrescenta</td>
<td class="num">8 observações · ~3 min</td></tr>
<tr><td><strong>Três vozes</strong></td>
<td>equilíbrio; permite descartar uma sem esvaziar o painel</td>
<td>ainda deixa duas famílias de fora</td>
<td class="num">12 observações · ~4 min</td></tr>
<tr><td><strong>Cinco vozes</strong></td>
<td>cobertura máxima de ângulos; comparação contínua entre modelos</td>
<td>20 observações por documento — deixa de ser voz curta e vira parede</td>
<td class="num">20 observações · ~7 min</td></tr>
</tbody></table>
<p class="reco"><strong>Minha recomendação: três em produção, cinco só em rodada
de comparação.</strong> Sem julgamento acumulado eu não tenho base para dizer
<em>quais</em> três — e é justamente isso que a fila destrava.</p>
</article>

<article class="decisao">
<h3>Decisão 2 · O teto do GLM</h3>
<table class="tradeoff">
<thead><tr><th>Opção</th><th>Ganha</th><th>Perde</th></tr></thead>
<tbody>
<tr><td><strong>Manter 300 para todos</strong></td>
<td>comparação limpa: mesma régua para todas as vozes</td>
<td>58% do que o GLM diz continua chegando pela metade</td></tr>
<tr><td><strong>Subir o teto só para o GLM</strong></td>
<td>o raciocínio dele chega inteiro</td>
<td>quebra a comparabilidade de <code>chars</code> e <code>teto%</code>; e
premia a voz que não obedeceu ao formato</td></tr>
<tr><td><strong>Subir para todos, para 400</strong></td>
<td>comparação preservada; provavelmente zera o corte</td>
<td>painel de cinco vozes passa de ~6 mil para ~8 mil caracteres de leitura</td></tr>
<tr><td><strong>Trocar o GLM por outra voz</strong></td>
<td>resolve sem mexer na régua</td>
<td>o GLM é o mais rápido dos cinco, e não há veredito que diga se ele agrega</td></tr>
</tbody></table>
<p class="reco"><strong>Minha recomendação: manter 300 até haver vereditos.</strong>
Ajustar o instrumento antes de saber se a voz agrega é otimizar a coisa errada.</p>
</article>

<article class="decisao">
<h3>Decisão 3 · Julgar a fila</h3>
<p>É o único caminho para qualquer promoção, e o único que responde <em>qual
voz serve para quê</em>. A fila faz <strong>rodízio diagonal</strong>: cinco
julgamentos cobrem as cinco vozes e os três casos; quinze cobrem cada par
(voz, caso) exatamente uma vez.</p>
<p class="nota">A versão anterior ordenava por sobreposição lexical — a mesma
régua que a seção 6 mostra ser cega para conteúdo. Se você julgasse só os
primeiros itens, a amostra do placar teria sido escolhida por uma métrica
inválida e o placar herdaria o viés. A primeira tentativa de conserto também
falhou: dava cinco observações do mesmo caso nos seis primeiros. Ambos os
achados são do revisor externo.</p>
<pre class="comando">python forja_painel_indicadores.py fila --limite 6</pre>
<p>Cada item sai com o comando de registro pronto. Vocabulário fechado:</p>
<div class="tabela-rolo">
<table>
<thead><tr><th>Veredito</th><th>Quando</th><th>Peso no índice</th></tr></thead>
<tbody>
<tr><td><code>acatada</code></td><td>mudou a peça</td><td>+1</td></tr>
<tr><td><code>acatada_parcial</code></td><td>provocou verificação que mudou algo, mas não como proposto</td><td>+0,5</td></tr>
<tr><td><code>duplicada</code></td><td>correta e já dita por outra voz</td><td>0 — conta no denominador e não soma</td></tr>
<tr><td><code>rejeitada</code></td><td>considerada e descartada</td><td>0</td></tr>
<tr><td><code>errada</code></td><td>factualmente errada; custou verificação à toa</td><td>−1</td></tr>
</tbody></table>
</div>
<p class="nota">Nada é elegível abaixo de <strong>12 observações e 3 casos
distintos</strong>. Hoje as cinco vozes têm exatamente 12 e 3 — o piso está
atingido em amostra, e falta o julgamento.</p>
</article>
"""


def bloco_limites() -> str:
    return """
<h2 id="limites">9 · O que esta medição não sustenta</h2>

<ul class="limites">
<li><strong>Não diz qual modelo é melhor.</strong> Diz qual é mais disciplinado no
formato. Qualidade de observação exige veredito humano, e há zero deles hoje.</li>
<li><strong>Três casos, todos de F7, todos do mesmo escritório.</strong> Nenhuma
conclusão se estende a F4, a outro tipo de peça ou a outro tribunal sem nova
medição.</li>
<li><strong>Uma execução por voz por caso.</strong> Sem repetição, não há como
separar o comportamento do modelo da variação entre chamadas — vale sobretudo para
os segundos.</li>
<li><strong>As vozes viram entre 15% e 58% de cada documento.</strong> Observações
sobre estrutura global da peça estão fora de alcance.</li>
<li><strong>O grau de esforço do Luna é diferente</strong> (<code>max</code>
contra <code>high</code> das outras quatro). Qualquer vantagem dele pode ser
esforço, não modelo.</li>
<li><strong>Sete das 60 observações não têm texto bruto preservado.</strong> Elas
foram cortadas no teto e o original não foi guardado — não são auditáveis.</li>
<li><strong>O detector de citação ainda tem falsos negativos conhecidos:</strong>
não cobre nome de precedente, relator, órgão, tese, data solta nem valor, e
ignora o que estiver entre aspas. Zero nesta coluna significa "não achei nas
formas que sei procurar".</li>
<li><strong>O painel envia trechos de documento de cliente a cinco rotas
externas.</strong> Não há gate de sigilo, classificação nem consentimento no
código. Isso vale para todo uso do painel, não só para esta medição.</li>
<li><strong>Zero em 12 não é taxa zero.</strong> Mesmo supondo independência —
que não há —, o limite superior a 95% de 0/12 fica acima de 20%.</li>
<li><strong>Nenhum juiz automático foi usado, de propósito.</strong> Pedir a um
modelo que classifique as observações dos outros seria LLM-as-judge, já rejeitado
nesta fábrica em 09/07/2026 — e aqui pior, porque o juiz mais provável seria da
mesma família que escreve a peça, medindo concordância consigo mesma.</li>
</ul>

<h2 id="reproduzir">10 · Como reproduzir</h2>
<pre class="comando">python forja_painel_curto.py --arquivo &lt;doc&gt; --caso &lt;id&gt; --fase F7 \\
    --saida telemetria/paineis_curtos/&lt;caso&gt;_F7_PAINEL_CURTO.json

python forja_painel_indicadores.py indicadores
python forja_painel_indicadores.py fila --limite 6
python forja_contribuicao.py colher --painel &lt;painel&gt; --por &lt;nome&gt;
python forja_contribuicao.py placar</pre>
<p class="nota">Dados brutos desta página:
<code>telemetria/COMPARACAO_VOZES_DADOS.json</code>. Geração:
<code>gerar_relatorio_comparacao_vozes.py</code> — determinístico, sem
transcrição manual de nenhuma observação. Regressão do subsistema:
<code>test_forja_painel_contribuicao.py</code>, 49 testes.</p>
"""


CSS = """
:root {
  --petroleo: #395C60;
  --petroleo-fundo: #2C4A4E;
  --terracota: #D9926A;
  --terracota-escura: #9C5B38;
  --grafite: #49494D;

  --ground: #FCFCFB;
  --surface: #EFF4F3;
  --surface-2: #FBF2EC;
  --linha: #D4DEDC;
  --texto: #23292A;
  --texto-fraco: #5F6B6C;
  --accent: var(--terracota-escura);
  --bom: #2F6B4F;
  --ruim: #A33B2A;
  --sombra: 0 1px 2px rgba(35,41,42,.06), 0 8px 24px rgba(35,41,42,.05);
}
@media (prefers-color-scheme: dark) {
  :root {
    --ground: #131C1C;
    --surface: #1B2726;
    --surface-2: #241E1A;
    --linha: #2E403F;
    --texto: #DFE7E5;
    --texto-fraco: #94A5A4;
    --petroleo: #7FAFB0;
    --accent: #E3A57F;
    --bom: #6FB58C;
    --ruim: #E08A76;
    --sombra: 0 1px 2px rgba(0,0,0,.4), 0 8px 24px rgba(0,0,0,.3);
  }
}
:root[data-theme="dark"] {
  --ground: #131C1C; --surface: #1B2726; --surface-2: #241E1A;
  --linha: #2E403F; --texto: #DFE7E5; --texto-fraco: #94A5A4;
  --petroleo: #7FAFB0; --accent: #E3A57F; --bom: #6FB58C; --ruim: #E08A76;
  --sombra: 0 1px 2px rgba(0,0,0,.4), 0 8px 24px rgba(0,0,0,.3);
}
:root[data-theme="light"] {
  --ground: #FCFCFB; --surface: #EFF4F3; --surface-2: #FBF2EC;
  --linha: #D4DEDC; --texto: #23292A; --texto-fraco: #5F6B6C;
  --petroleo: #395C60; --accent: #9C5B38; --bom: #2F6B4F; --ruim: #A33B2A;
  --sombra: 0 1px 2px rgba(35,41,42,.06), 0 8px 24px rgba(35,41,42,.05);
}

* { box-sizing: border-box; }
body {
  margin: 0;
  background: var(--ground);
  color: var(--texto);
  font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  font-size: 17px;
  line-height: 1.65;
  -webkit-font-smoothing: antialiased;
}
.envelope { max-width: 1120px; margin: 0 auto; padding: 0 clamp(16px, 4vw, 48px) 96px; }
.prosa { max-width: 68ch; }

/* --- cabeçalho ------------------------------------------------------- */
header.capa {
  border-bottom: 3px solid var(--petroleo);
  padding: clamp(40px, 7vw, 88px) 0 32px;
  margin-bottom: 8px;
}
.eyebrow {
  font-family: ui-monospace, "Cascadia Code", Consolas, monospace;
  font-size: 12px; letter-spacing: .18em; text-transform: uppercase;
  color: var(--accent); margin: 0 0 18px;
}
h1 {
  font-family: Georgia, "Iowan Old Style", "Times New Roman", serif;
  font-weight: 400; font-size: clamp(32px, 5.2vw, 54px);
  line-height: 1.1; letter-spacing: -.015em; text-wrap: balance;
  margin: 0 0 20px; max-width: 26ch;
}
.subtitulo { font-size: clamp(18px, 2.2vw, 21px); color: var(--texto-fraco);
  max-width: 60ch; margin: 0 0 32px; }
.fichario { display: flex; flex-wrap: wrap; gap: 0; border-top: 1px solid var(--linha); }
.fichario div {
  flex: 1 1 150px; padding: 14px 18px 14px 0; border-right: 1px solid var(--linha);
}
.fichario div:last-child { border-right: none; }
.fichario dt {
  font-family: ui-monospace, Consolas, monospace; font-size: 11px;
  letter-spacing: .1em; text-transform: uppercase; color: var(--texto-fraco);
  margin: 0 0 4px;
}
.fichario dd {
  margin: 0; font-family: Georgia, serif; font-size: 24px;
  font-variant-numeric: tabular-nums; color: var(--petroleo);
}

/* --- veredito -------------------------------------------------------- */
.veredito {
  background: var(--surface); border-left: 4px solid var(--accent);
  padding: 26px 28px; margin: 40px 0 8px; border-radius: 2px;
}
.veredito h2 { margin-top: 0; border: none; padding: 0; font-size: 21px; }
.veredito p:last-child { margin-bottom: 0; }
.veredito ul { margin: 12px 0 0; padding-left: 20px; }
.veredito li { margin-bottom: 8px; }

/* --- estrutura ------------------------------------------------------- */
h2 {
  font-family: Georgia, "Iowan Old Style", serif; font-weight: 400;
  font-size: clamp(24px, 3.2vw, 32px); line-height: 1.2; text-wrap: balance;
  margin: 72px 0 20px; padding-bottom: 10px;
  border-bottom: 1px solid var(--linha);
}
h3 {
  font-family: Georgia, serif; font-weight: 400; font-size: 21px;
  margin: 40px 0 12px; color: var(--petroleo);
}
h4 { font-size: 16px; margin: 0 0 8px; letter-spacing: -.005em; }
p { margin: 0 0 16px; max-width: 68ch; }
.nota { font-size: 15px; color: var(--texto-fraco); }
code {
  font-family: ui-monospace, "Cascadia Code", Consolas, monospace;
  font-size: .88em; background: var(--surface); padding: .12em .38em;
  border-radius: 2px;
}
pre {
  font-family: ui-monospace, "Cascadia Code", Consolas, monospace;
  font-size: 13.5px; line-height: 1.6; background: var(--surface);
  border: 1px solid var(--linha); border-radius: 3px;
  padding: 18px 20px; overflow-x: auto; white-space: pre-wrap;
  margin: 0 0 20px;
}
pre.prompt { border-left: 3px solid var(--petroleo); }
pre.comando { border-left: 3px solid var(--accent); white-space: pre; }

/* --- tabelas --------------------------------------------------------- */
.tabela-rolo { overflow-x: auto; margin: 0 0 24px; box-shadow: var(--sombra);
  border-radius: 3px; }
table { border-collapse: collapse; width: 100%; font-size: 15px;
  background: var(--ground); }
th, td { text-align: left; padding: 11px 14px; border-bottom: 1px solid var(--linha);
  vertical-align: top; }
thead th {
  background: var(--petroleo); color: #F4F8F7; font-weight: 600;
  font-size: 12px; letter-spacing: .06em; text-transform: uppercase;
  white-space: nowrap; border-bottom: none;
}
:root[data-theme="dark"] thead th, tbody tr:nth-child(even) { }
@media (prefers-color-scheme: dark) { thead th { background: #24393A; color: #DFE7E5; } }
:root[data-theme="dark"] thead th { background: #24393A; color: #DFE7E5; }
:root[data-theme="light"] thead th { background: #395C60; color: #F4F8F7; }
tbody tr:last-child td { border-bottom: none; }
td.num, th.num { text-align: right; font-variant-numeric: tabular-nums;
  font-family: ui-monospace, Consolas, monospace; white-space: nowrap; }
table.principal tbody td:first-child { white-space: nowrap; }
td.bom { color: var(--bom); font-weight: 600; }
td.destaque-ruim { color: var(--ruim); font-weight: 700; }
table.matriz th { font-weight: 500; }
table.matriz tbody th { background: var(--surface); font-size: 13px; }
table.matriz td { position: relative; }
table.matriz td.num::before {
  content: ""; position: absolute; inset: 0;
  background: var(--accent); opacity: calc(var(--i, 0) * .22);
}
table.matriz td.diag { background: var(--surface); color: var(--texto-fraco);
  text-align: center; }
table.tradeoff { font-size: 15px; }

/* --- fichas e achados ------------------------------------------------ */
.fichas { display: grid; gap: 16px; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); }
.ficha {
  background: var(--surface); border: 1px solid var(--linha);
  border-radius: 3px; padding: 20px 22px;
}
.ficha h4 { color: var(--petroleo); font-family: Georgia, serif; font-weight: 400;
  font-size: 18px; }
.ficha p { font-size: 14.5px; margin-bottom: 10px; max-width: none; }
.ficha p:last-child { margin-bottom: 0; }
.ficha .como::before { content: "Como "; font-weight: 700; color: var(--texto-fraco); }
.ficha .serve::before { content: "Serve "; font-weight: 700; color: var(--bom); }
.ficha .nao::before { content: "Não serve "; font-weight: 700; color: var(--ruim); }
.ficha .hist { font-size: 13.5px; color: var(--texto-fraco);
  border-top: 1px solid var(--linha); padding-top: 10px; }
.ficha .hist::before { content: "Histórico "; font-weight: 700; }

.achados { display: grid; gap: 16px; }
.achado { border: 1px solid var(--linha); border-left: 4px solid var(--petroleo);
  border-radius: 3px; padding: 18px 22px; background: var(--ground); }
.achado-forte { border-left-color: var(--bom); background: var(--surface); }
.achado-ruim { border-left-color: var(--ruim); background: var(--surface-2); }
.achado h4 { font-size: 17px; }
.achado p { max-width: none; margin-bottom: 10px; }
.achado p:last-child { margin-bottom: 0; }
.achado .dado { font-size: 14.5px; color: var(--texto-fraco); }

.aviso { background: var(--surface-2); border: 1px solid var(--linha);
  border-radius: 3px; padding: 22px 24px; margin: 24px 0; }
.aviso h4 { font-size: 17px; color: var(--accent); }
.aviso p, .aviso li { max-width: none; font-size: 15.5px; }
.aviso p:last-child, .aviso li:last-child { margin-bottom: 0; }
.aviso-negativo { border-left: 4px solid var(--ruim); }
.aviso ol { padding-left: 22px; }
.aviso ol li { margin-bottom: 10px; }

/* --- chips ----------------------------------------------------------- */
.chip {
  display: inline-block; font-family: ui-monospace, Consolas, monospace;
  font-size: 10.5px; letter-spacing: .06em; text-transform: uppercase;
  padding: 2px 7px; border-radius: 2px; vertical-align: middle;
  white-space: nowrap;
}
.chip-controle { background: var(--petroleo); color: #F4F8F7; }
:root[data-theme="dark"] .chip-controle { background: #24393A; color: #BFD4D3; }
@media (prefers-color-scheme: dark) { .chip-controle { background: #24393A; color: #BFD4D3; } }
:root[data-theme="light"] .chip-controle { background: #395C60; color: #F4F8F7; }
.chip-alerta { background: var(--surface-2); color: var(--ruim);
  border: 1px solid var(--ruim); }

/* --- observações ----------------------------------------------------- */
.filtro { display: flex; flex-wrap: wrap; gap: 8px; margin: 24px 0 32px;
  position: sticky; top: 0; background: var(--ground); padding: 12px 0;
  z-index: 5; border-bottom: 1px solid var(--linha); }
.filtro button {
  font: inherit; font-size: 14px; padding: 6px 14px; cursor: pointer;
  background: var(--ground); color: var(--texto);
  border: 1px solid var(--linha); border-radius: 999px;
}
.filtro button:hover { border-color: var(--petroleo); }
.filtro button.ativo { background: var(--petroleo); color: #F4F8F7;
  border-color: var(--petroleo); }
:root[data-theme="dark"] .filtro button.ativo { background: #24393A; color: #DFE7E5; }
@media (prefers-color-scheme: dark) { .filtro button.ativo { background: #24393A; color: #DFE7E5; } }
:root[data-theme="light"] .filtro button.ativo { background: #395C60; color: #F4F8F7; }
.filtro button:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }

.caso { margin-bottom: 48px; }
.caso h3 { border-bottom: 2px solid var(--petroleo); padding-bottom: 8px; }
.caso-meta { font-family: ui-monospace, Consolas, monospace; font-size: 12px;
  color: var(--texto-fraco); font-weight: 400; letter-spacing: 0; }
.voz-bloco { margin-bottom: 24px; }
.voz-bloco h4 { font-family: ui-monospace, Consolas, monospace; font-size: 13px;
  letter-spacing: .08em; text-transform: uppercase; color: var(--accent);
  padding-bottom: 6px; border-bottom: 1px dashed var(--linha); }
.voz-bloco[hidden] { display: none; }
.obs-lista { list-style: none; margin: 0; padding: 0;
  display: grid; gap: 12px; }
.obs-lista li { background: var(--surface); border-radius: 3px;
  padding: 14px 16px; border-left: 2px solid var(--linha); }
.obs { margin: 0 0 8px; font-size: 15.5px; max-width: none; }
.meta { margin: 0; font-family: ui-monospace, Consolas, monospace;
  font-size: 11.5px; color: var(--texto-fraco); max-width: none; }
.meta code { background: transparent; padding: 0; }

/* --- decisões -------------------------------------------------------- */
.decisao { border: 1px solid var(--linha); border-top: 4px solid var(--accent);
  border-radius: 3px; padding: 24px 26px; margin-bottom: 24px;
  background: var(--ground); }
.decisao h3 { margin-top: 0; color: var(--texto); }
.decisao .reco { background: var(--surface); border-left: 3px solid var(--bom);
  padding: 12px 16px; font-size: 15.5px; max-width: none; margin-bottom: 0; }
.limites { padding-left: 22px; max-width: 68ch; }
.limites li { margin-bottom: 12px; }

footer { margin-top: 80px; padding-top: 24px; border-top: 1px solid var(--linha);
  font-size: 14px; color: var(--texto-fraco); }

@media (prefers-reduced-motion: reduce) {
  * { transition: none !important; animation: none !important; }
}
@media (max-width: 640px) {
  body { font-size: 16px; }
  .fichario div { flex-basis: 45%; }
}
"""

JS = """
(function () {
  var botoes = document.querySelectorAll('.filtro button');
  botoes.forEach(function (b) {
    b.addEventListener('click', function () {
      var alvo = b.dataset.filtro;
      botoes.forEach(function (o) { o.classList.toggle('ativo', o === b); });
      document.querySelectorAll('.voz-bloco').forEach(function (bloco) {
        bloco.hidden = (alvo !== 'todas' && bloco.dataset.voz !== alvo);
      });
    });
  });
})();
"""


class FidelidadeError(RuntimeError):
    pass


def conferir_fidelidade(corpo: str, d: dict) -> None:
    """Cada observação tem de aparecer no HTML idêntica ao JSON, caractere a caractere.

    Isto não é zelo abstrato. A primeira versão deste gerador aplicava
    `.replace(",", ".")` num bloco inteiro para formatar separador de milhar, e
    **trocou por ponto todas as vírgulas das 60 observações** — pontuação de
    texto que o relatório promete reproduzir sem alteração. O HTML ficou
    plausível, com tamanho certo e 60 blocos no lugar; só a leitura de uma frase
    revelou o estrago.

    É a mesma classe de falha que a fábrica já registrou duas vezes hoje: saída
    verossímil sem exceção nenhuma. O gate compara o que saiu com a fonte, que é
    a única prova que vale.
    """
    problemas = []
    for o in d["observacoes"]:
        if e(o["texto"]) not in corpo:
            problemas.append(f"{o['modelo']} · {o['obsId']}: texto alterado ou ausente")
    for campo in ("sistema", "molde"):
        if e(d["prompt"][campo]) not in corpo:
            problemas.append(f"prompt.{campo}: alterado ou ausente")
    if problemas:
        raise FidelidadeError(
            f"{len(problemas)} divergência(s) entre o HTML e o JSON:\n  "
            + "\n  ".join(problemas[:10]))


def main() -> None:
    global ANONIMO
    import sys
    ANONIMO = "--anonimo" in sys.argv
    destino = SAIDA_ANONIMA if ANONIMO else SAIDA
    d = json.loads(DADOS.read_text(encoding="utf-8"))
    ms = {m["modelo"]: m for m in d["indicadores"]["modelos"]}
    total_obs = len(d["observacoes"])
    seg_doc = sum(m["segundosMedio"] for m in ms.values())

    corpo = f"""<title>Cinco vozes na mesma prova — comparação medida</title>
<style>{CSS}</style>

<div class="envelope">

<header class="capa">
<p class="eyebrow">FORJA · painel de vozes curtas · medição de 07–08/08/2026</p>
<h1>Cinco modelos na mesma prova, e o que a medição sustenta</h1>
<p class="subtitulo">Kimi K3, GLM 5.2, Grok 4.5, Luna 5.6 max e Opus 5 leram os
mesmos três documentos de trabalho e deram o mesmo tipo de parecer curto. Esta
página traz a tarefa verbatim, os indicadores com o que cada um não mede, as 60
observações na íntegra e o trade-off das três decisões que restam.</p>
<dl class="fichario">
<div><dt>Observações</dt><dd>{total_obs}</dd></div>
<div><dt>Vozes</dt><dd>5</dd></div>
<div><dt>Casos reais</dt><dd>3</dd></div>
<div><dt>Custo</dt><dd>US$ 0,00</dd></div>
<div><dt>Tempo por documento</dt><dd>{seg_doc:.0f} s</dd></div>
<div><dt>Vereditos humanos</dt><dd>0</dd></div>
</dl>
</header>

<div class="veredito prosa">
<h2 style="border:none;margin:0 0 12px;padding:0;">O que a medição já decide, e o que ela não decide</h2>
<p><strong>Esta página foi reprovada numa revisão externa e reescrita.</strong>
A versão de 08/08 afirmava condições iguais que não existiam, apresentava um
detector defeituoso como prova de que ninguém inventou citação, e levava nome de
cliente para fora da máquina. As correções estão marcadas seção a seção.</p>
<p><strong>O que os dados sustentam:</strong> descrições de três chamadas por
modelo, sob condições que <em>não</em> foram idênticas. O GLM citou duas fontes
ausentes do recorte e teve sete respostas cortadas pelo nosso próprio teto. Os
tempos observados vão de 21 s a 37 s, em ordem fixa de chamada.</p>
<p><strong>O que os dados não sustentam:</strong> nenhum ranking entre os cinco.
Nem qual voz serve para quê — a régua automática mede aderência a formato, não
conteúdo, e isso foi confirmado por três resultados negativos.</p>
<ul>
<li>Condições desiguais: o Luna correu em <code>max</code>, os outros em
<code>high</code>; o Kimi K3 recebeu uma instrução a mais.</li>
<li>n real: <strong>3 chamadas</strong> por modelo, não 12 observações
independentes. Sem repetição, sem randomização, sem intervalo de confiança.</li>
<li>Vereditos humanos: <strong>zero</strong>. Nenhum número desta página promove
nenhum modelo a nada, e nenhum deveria influenciar qual usar.</li>
</ul>
</div>

<div class="prosa">
{bloco_prompt(d)}
</div>
{bloco_modelos(d)}
{bloco_alvos(d)}
{bloco_indicadores()}
{bloco_resultado(d)}
{bloco_convergencia(d)}
{bloco_observacoes(d)}
{bloco_decisao()}
<div class="prosa">
{bloco_limites()}
</div>

<footer>
<p>Gerado por <code>gerar_relatorio_comparacao_vozes.py</code> a partir de
<code>telemetria/COMPARACAO_VOZES_DADOS.json</code>. Nenhuma observação foi
transcrita à mão. Fábrica de Melhoria de Petições · harness FORJA.</p>
</footer>

</div>
<script>{JS}</script>
"""
    conferir_fidelidade(corpo, d)
    if ANONIMO:
        vazados = [r for r in (d.get("rotulosCaso") or {}).values() if r in corpo]
        if vazados:
            raise FidelidadeError(
                "versão publicável ainda traz nome de caso: " + ", ".join(vazados))
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(corpo, encoding="utf-8")
    print(f"{destino}  ({n(len(corpo))} bytes)"
          + ("  [ANÔNIMA — casos como Caso A/B/C]" if ANONIMO else "  [LOCAL — nomes reais]"))
    print(f"fidelidade: {len(d['observacoes'])} observações conferidas caractere a "
          "caractere contra o JSON")


if __name__ == "__main__":
    main()
