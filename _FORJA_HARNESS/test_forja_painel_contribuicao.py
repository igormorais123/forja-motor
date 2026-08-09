"""Regressão do painel de vozes curtas e do placar de contribuição.

O que se afere aqui não é se os modelos respondem — isso a chamada real prova.
É se as **regras de contagem** resistem às formas conhecidas de o placar mentir:
amostra pequena com taxa perfeita, modelo que só concorda, e promoção que
ignora a bancada de fidelidade à fonte.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

import forja_contribuicao as fc
import forja_modelos as fm
import forja_painel_curto as pc


# --------------------------------------------------------------------------
# Tetos — cortados no código, não pedidos no prompt
# --------------------------------------------------------------------------

def test_corta_no_teto_de_observacoes_e_declara_o_corte():
    bruto = "\n".join(f"- observação {i}" for i in range(9))
    obs, corte = pc.extrair(bruto)
    assert len(obs) == pc.LIMITE_OBSERVACOES
    assert corte["observacoesDescartadas"] == 9 - pc.LIMITE_OBSERVACOES


def test_corta_no_teto_de_caracteres_e_declara():
    obs, corte = pc.extrair("- " + "a" * (pc.LIMITE_CARACTERES + 50))
    assert len(obs[0]) <= pc.LIMITE_CARACTERES + 1  # +1 pela reticência
    assert corte["observacoesTruncadas"] == 1


@pytest.mark.parametrize("linha", ["- ponto", "* ponto", "1. ponto", "2) ponto", "ponto"])
def test_aceita_os_formatos_que_o_modelo_de_fato_usa(linha):
    """Exigir o formato do molde trocaria conteúdo por obediência."""
    obs, _ = pc.extrair(linha)
    assert obs == ["ponto"]


def test_id_da_observacao_e_estavel_e_ignora_acento_e_caixa():
    a = pc.obs_id("m", "O  prazo  é  premissa")
    b = pc.obs_id("m", "o prazo e premissa")
    assert a == b
    assert a != pc.obs_id("outro", "o prazo e premissa")


def test_vozes_do_painel_estao_no_registro_e_sao_da_assinatura():
    for voz in pc.VOZES_PADRAO:
        modelo = fm.MODELOS[voz]
        assert modelo.provedor == "cursor", f"{voz} não roda pela assinatura do titular"
        assert modelo.usd_saida_por_milhao == 0.0


def test_kimi_k3_carrega_a_restricao_que_a_bancada_mediu():
    """A restrição não é opinião: 0 de 6 na condição solta, com 4 invenções."""
    assert "nao_afirma_fato" in fm.MODELOS["kimi-k3-cursor"].restricoes


def test_glm_nao_carrega_restricao_por_falta_de_medida():
    """Não aferido não é o mesmo que reprovado — os dois estados não colapsam."""
    assert fm.MODELOS["glm-5.2-cursor"].restricoes == ()
    assert fc._bancada("glm-5.2-cursor")["aferida"] is False


# --------------------------------------------------------------------------
# Placar
# --------------------------------------------------------------------------

def _painel(tmp_path: Path, caso: str, modelo: str, textos: list[str]) -> Path:
    obs = [{"obsId": pc.obs_id(modelo, t), "texto": t} for t in textos]
    dados = {
        "contrato": "FORJA-PAINEL-CURTO-v1", "caso": caso, "fase": "F4",
        "em": "2026-08-07T00:00:00-03:00", "natureza": "opinião interna",
        "vozes": [{"modelo": modelo, "familia": fm.MODELOS[modelo].familia,
                   "observacoes": obs}],
        "falhas": [],
        "decisoes": [{"obsId": o["obsId"], "modelo": modelo, "veredito": None,
                      "duplicadaDe": None, "motivo": None} for o in obs],
    }
    # O nome importa: `forja_painel_indicadores._carregar` procura por
    # `*PAINEL_CURTO*.json`. Fixture com outro nome passaria despercebida e o
    # teste da fila mediria a lista vazia — foi o que aconteceu na primeira vez.
    caminho = tmp_path / f"{caso}_PAINEL_CURTO.json"
    caminho.write_text(json.dumps(dados, ensure_ascii=False), encoding="utf-8")
    return caminho


def _decidir(caminho: Path, vereditos: list[str], duplicada_de: str = "outro") -> None:
    dados = json.loads(caminho.read_text(encoding="utf-8"))
    for decisao, veredito in zip(dados["decisoes"], vereditos):
        decisao["veredito"] = veredito
        if veredito == "duplicada":
            decisao["duplicadaDe"] = duplicada_de
    caminho.write_text(json.dumps(dados, ensure_ascii=False), encoding="utf-8")


@pytest.fixture()
def registro_isolado(tmp_path, monkeypatch):
    monkeypatch.setattr(fc, "REGISTRO", tmp_path / "CONTRIBUICAO.json")
    return tmp_path


def test_amostra_pequena_nao_e_elegivel_mesmo_com_placar_perfeito(registro_isolado):
    """Dois acertos de dois dão 100% e não dizem nada."""
    caminho = _painel(registro_isolado, "C1", "glm-5.2-cursor", ["a", "b"])
    _decidir(caminho, ["acatada", "acatada"])
    fc.colher(caminho, por="teste")
    linha = fc.placar()["modelos"][0]
    assert linha["indice"] == 100.0
    assert linha["elegivel"] is False
    assert "mínimo" in linha["motivoInelegivel"]


def test_um_caso_longo_sozinho_nao_vira_padrao(registro_isolado):
    """Volume de um caso só é volume, não recorrência entre casos."""
    caminho = _painel(registro_isolado, "C1", "glm-5.2-cursor",
                      [f"obs {i}" for i in range(14)])
    _decidir(caminho, ["acatada"] * 14)
    fc.colher(caminho, por="teste")
    linha = fc.placar()["modelos"][0]
    assert linha["n"] == 14 and linha["casos"] == 1
    assert linha["elegivel"] is False
    assert "caso" in linha["motivoInelegivel"]


def test_quem_so_concorda_nao_pontua(registro_isolado):
    """`duplicada` conta no denominador e não soma — é a defesa contra o eco."""
    caminho = _painel(registro_isolado, "C1", "glm-5.2-cursor", ["a", "b", "c", "d"])
    _decidir(caminho, ["duplicada"] * 4)
    fc.colher(caminho, por="teste")
    linha = fc.placar()["modelos"][0]
    assert linha["indice"] == 0.0
    assert linha["eco"] == 100.0


def test_errada_desconta_e_nao_e_apenas_neutra(registro_isolado):
    """Observação errada custa verificação; empatar com rejeitada apagaria isso."""
    a = _painel(registro_isolado, "C1", "glm-5.2-cursor", ["a", "b"])
    _decidir(a, ["acatada", "rejeitada"])
    fc.colher(a, por="teste")
    so_rejeitada = fc.placar()["modelos"][0]["indice"]

    monkey = _painel(registro_isolado, "C2", "glm-5.2-cursor", ["c", "d"])
    _decidir(monkey, ["acatada", "errada"])
    fc.colher(monkey, por="teste")
    com_errada = fc.placar()["modelos"][0]["indice"]
    assert com_errada < so_rejeitada


def test_colher_e_idempotente(registro_isolado):
    caminho = _painel(registro_isolado, "C1", "glm-5.2-cursor", ["a", "b"])
    _decidir(caminho, ["acatada", "rejeitada"])
    fc.colher(caminho, por="teste")
    fc.colher(caminho, por="teste")
    assert fc.placar()["modelos"][0]["n"] == 2


def test_duplicada_sem_origem_e_recusada_na_colheita(registro_isolado):
    caminho = _painel(registro_isolado, "C1", "glm-5.2-cursor", ["a"])
    dados = json.loads(caminho.read_text(encoding="utf-8"))
    dados["decisoes"][0]["veredito"] = "duplicada"
    caminho.write_text(json.dumps(dados, ensure_ascii=False), encoding="utf-8")
    resultado = fc.colher(caminho, por="teste")
    assert resultado["colhidas"] == 0
    assert any("duplicada" in p for p in resultado["invalidas"])


def test_veredito_fora_do_vocabulario_nao_entra(registro_isolado):
    caminho = _painel(registro_isolado, "C1", "glm-5.2-cursor", ["a"])
    dados = json.loads(caminho.read_text(encoding="utf-8"))
    dados["decisoes"][0]["veredito"] = "genial"
    caminho.write_text(json.dumps(dados, ensure_ascii=False), encoding="utf-8")
    resultado = fc.colher(caminho, por="teste")
    assert resultado["colhidas"] == 0 and resultado["invalidas"]


def test_amostra_le_o_texto_do_painel_e_nao_do_ledger(registro_isolado):
    """O ledger guarda localizador, não conteúdo. Contar não é ler."""
    caminho = _painel(registro_isolado, "C1", "glm-5.2-cursor", ["texto que importa"])
    _decidir(caminho, ["acatada"])
    fc.colher(caminho, por="teste")
    guardado = json.loads((registro_isolado / "CONTRIBUICAO.json").read_text(encoding="utf-8"))
    assert "texto que importa" not in json.dumps(guardado, ensure_ascii=False)
    assert fc.amostra("glm-5.2-cursor")[0]["texto"] == "texto que importa"


# --------------------------------------------------------------------------
# Promoção
# --------------------------------------------------------------------------

def _elegivel(pasta: Path, modelo: str) -> None:
    for i in range(3):
        caminho = _painel(pasta, f"CASO{i}", modelo, [f"obs {i}-{j}" for j in range(5)])
        _decidir(caminho, ["acatada"] * 4 + ["rejeitada"])
        fc.colher(caminho, por="teste")


def test_promocao_exige_pessoa(registro_isolado):
    _elegivel(registro_isolado, "glm-5.2-cursor")
    with pytest.raises(fc.ContribuicaoError, match="aprovado-por"):
        fc.promover("glm-5.2-cursor", para="consultivo", aprovado_por="  ")


def test_nao_se_pula_degrau(registro_isolado):
    _elegivel(registro_isolado, "glm-5.2-cursor")
    with pytest.raises(fc.ContribuicaoError, match="próximo degrau"):
        fc.promover("glm-5.2-cursor", para="candidato", aprovado_por="Igor")


def test_promocao_congela_a_evidencia_do_momento(registro_isolado):
    _elegivel(registro_isolado, "glm-5.2-cursor")
    ficha = fc.promover("glm-5.2-cursor", para="consultivo", aprovado_por="Igor")
    assert ficha["degrau"] == "consultivo"
    assert ficha["evidencia"]["casos"] == 3
    assert ficha["evidencia"]["n"] == 15


def test_candidato_barrado_por_falta_de_bancada(registro_isolado):
    """Não aferido não é aprovado, e o placar de contribuição não mede invenção."""
    _elegivel(registro_isolado, "glm-5.2-cursor")
    fc.promover("glm-5.2-cursor", para="consultivo", aprovado_por="Igor")
    with pytest.raises(fc.ContribuicaoError, match="bancada"):
        fc.promover("glm-5.2-cursor", para="candidato", aprovado_por="Igor")


def test_candidato_barrado_por_restricao_medida(registro_isolado):
    """Bom de ângulo não revoga reprovação em fidelidade à fonte."""
    _elegivel(registro_isolado, "kimi-k3-cursor")
    fc.promover("kimi-k3-cursor", para="consultivo", aprovado_por="Igor")
    with pytest.raises(fc.ContribuicaoError, match="nao_afirma_fato"):
        fc.promover("kimi-k3-cursor", para="candidato", aprovado_por="Igor")


def test_bancada_casa_o_nome_de_hoje_com_o_da_epoca():
    """`kimi-k3-cursor` hoje é o `kimi-k3` que reprovou em 26/07/2026.

    Sem esse casamento, um modelo reprovado voltaria como "nunca aferido" só
    porque a rota mudou de nome — que é como uma medição ruim desaparece.
    """
    banca = fc._bancada("kimi-k3-cursor")
    assert banca["aferida"] is True
    assert banca["invencoes"] > 0


def test_revalidar_acusa_perda_de_lastro_sem_apagar_nada(registro_isolado):
    _elegivel(registro_isolado, "glm-5.2-cursor")
    fc.promover("glm-5.2-cursor", para="consultivo", aprovado_por="Igor")
    registro = fc.carregar()
    registro["decisoes"] = registro["decisoes"][:2]
    fc.gravar(registro)
    fichas = fc.revalidar()
    assert fichas[0]["divergencias"]
    assert fc.carregar()["degraus"]["glm-5.2-cursor"]["degrau"] == "consultivo"


# --------------------------------------------------------------------------
# Camada autônoma — indicadores sem julgamento humano
# --------------------------------------------------------------------------

import forja_painel_indicadores as fi


def test_citacao_afirmada_e_violacao():
    # "art. 1.021" dispara `artigo` e também `cifra`, porque 1.021 tem forma de
    # número com milhar. Sobreposição de padrões é aceitável: o que importa é
    # que a violação apareça, não que ela seja classificada com um rótulo só.
    assert "artigo" in fi.violacoes_de_fonte("aplique o art. 1.021 do CPC")
    assert "súmula" in fi.violacoes_de_fonte("a Súmula 7 impede o reexame")


def test_citacao_entre_aspas_nao_e_violacao():
    """Fixture do falso positivo real de 07/08/2026.

    O GLM 5.2 foi acusado de citar súmula quando estava **citando o blueprint
    para criticá-lo** — o comportamento desejado. Sem a exclusão de aspas, o
    indicador puniria justamente a voz que aponta o dado a conferir.
    """
    real = ('"Súmula 7 sobre matéria de qualificação jurídica dos fatos '
            'incontroversos" é a tese inteira comprada sem verificação: é '
            'preciso conferir se os fatos estão realmente incontroversos.')
    assert fi.violacoes_de_fonte(real) == []


def test_mencao_generica_nao_e_violacao():
    """Apontar o dado a conferir sem afirmá-lo é o que se quer da voz curta."""
    assert fi.violacoes_de_fonte(
        "conferir o regimento do tribunal antes de prometer sustentação oral") == []


def test_o_limiar_de_eco_nao_foi_moldado_ate_concordar_comigo():
    """O par de eco mais fraco medido ficou em 0,091 — e continua abaixo do limiar.

    Baixar o limiar até capturá-lo casaria com duas classificações humanas
    (n=2) e passaria a marcar como eco pares comprovadamente não relacionados,
    que deram 0,147. O indicador fica declaradamente fraco, e o veredito
    `duplicada` continua sendo quem mede eco.
    """
    assert fi.LIMIAR_ECO_LEXICAL > 0.147
    a = fi._palavras("O eixo depende de provar que os fatos são incontroversos, "
                     "mas o blueprint não lista quais constam do acórdão")
    b = fi._palavras("é preciso conferir se os fatos estão realmente "
                     "incontroversos nos autos ou se houve juízo de prova")
    assert fi._jaccard(a, b) < fi.LIMIAR_ECO_LEXICAL


def test_ancoragem_sai_do_painel_e_nao_do_documento_guardado():
    """O painel grava o número; o texto do caso não é duplicado no artefato."""
    medir = fi.ancoragem_de("prazo intimação certidão publicação diário oficial")
    assert medir("a intimação precisa de certidão") > 0
    assert fi.ancoragem_de("")("qualquer coisa") is None


def test_fila_faz_rodizio_e_nao_usa_a_metrica_invalida(tmp_path, monkeypatch):
    """A ordem por sobreposição foi retirada, e o motivo importa.

    Ela usava `sobreposicao` — a mesma régua que os três resultados negativos
    mostraram cega para conteúdo. Se o humano julga só os primeiros itens, a
    amostra que alimenta o placar teria sido escolhida por uma métrica
    reconhecidamente inválida, e o placar herdaria o viés. Achado do revisor
    externo em 09/08/2026.

    O rodízio não promete escolher o que mais informa. Promete o que dá para
    garantir: cada voz e cada caso recebem o mesmo número de julgamentos, que é
    o mínimo para a comparação ser justa.
    """
    monkeypatch.setattr(fc, "REGISTRO", tmp_path / "vazio.json")
    for caso in ("C1", "C2"):
        painel = {
            "contrato": "FORJA-PAINEL-CURTO-v1", "caso": caso, "fase": "F4",
            "vozes": [
                {"modelo": m, "familia": f, "observacoes": [
                    {"obsId": f"{caso}-{m[:3]}-{i}", "texto": f"observação {i} de {m}"}
                    for i in range(2)]}
                for m, f in (("kimi-k3-cursor", "moonshot"),
                             ("glm-5.2-cursor", "zhipu"),
                             ("opus-5-cursor", "anthropic"))
            ],
            "falhas": [], "decisoes": [],
        }
        (tmp_path / f"{caso}_PAINEL_CURTO.json").write_text(
            json.dumps(painel, ensure_ascii=False), encoding="utf-8")

    fila = fi.fila(limite=6, pastas=[tmp_path])
    # Seis itens têm de cobrir as três vozes duas vezes cada, e os dois casos.
    from collections import Counter
    assert Counter(i["modelo"] for i in fila) == {
        "kimi-k3-cursor": 2, "glm-5.2-cursor": 2, "opus-5-cursor": 2}
    assert set(i["caso"] for i in fila) == {"C1", "C2"}
    # E a ordenação não pode voltar a depender da métrica cega.
    origem = (Path(__file__).parent / "forja_painel_indicadores.py").read_text(
        encoding="utf-8", errors="replace")
    assert 'sort(key=lambda c: (c["sobreposicao"]' not in origem


def test_rodizio_cobre_vozes_e_casos_nas_primeiras_posicoes(tmp_path, monkeypatch):
    """A primeira tentativa de rodízio parecia rodízio e não era.

    Ordenar por (posição, caso, modelo) dava, com `--limite 6`, cinco
    observações do primeiro caso e duas da mesma voz. O revisor externo rodou o
    comando e mostrou o desequilíbrio: o comentário prometia uma coisa e o
    código fazia outra. A diagonal é o conserto, e este teste é a prova.
    """
    monkeypatch.setattr(fc, "REGISTRO", tmp_path / "vazio.json")
    modelos = ["kimi-k3-cursor", "glm-5.2-cursor", "grok-4.5-cursor",
               "luna-5.6-cursor", "opus-5-cursor"]
    for caso in ("C1", "C2", "C3"):
        painel = {
            "contrato": "FORJA-PAINEL-CURTO-v1", "caso": caso, "fase": "F7",
            "vozes": [{"modelo": m, "familia": fm.MODELOS[m].familia,
                       "observacoes": [{"obsId": f"{caso}-{m[:4]}-{i}",
                                        "texto": f"obs {i} de {m} em {caso}"}
                                       for i in range(4)]} for m in modelos],
            "falhas": [], "decisoes": [],
        }
        (tmp_path / f"{caso}_PAINEL_CURTO.json").write_text(
            json.dumps(painel, ensure_ascii=False), encoding="utf-8")

    from collections import Counter
    cinco = fi.fila(limite=5, pastas=[tmp_path])
    assert len(set(i["modelo"] for i in cinco)) == 5, "cinco itens, cinco vozes"
    assert len(set(i["caso"] for i in cinco)) == 3, "e os três casos representados"

    quinze = fi.fila(limite=15, pastas=[tmp_path])
    pares = Counter((i["modelo"], i["caso"]) for i in quinze)
    assert len(pares) == 15 and set(pares.values()) == {1}, (
        "os primeiros 15 têm de cobrir cada par (voz, caso) exatamente uma vez")


def test_fila_e_ledger_usam_a_mesma_chave(tmp_path, monkeypatch):
    """`obsId` sozinho tirava da fila o que fora julgado em OUTRO caso.

    O identificador é hash de modelo + texto normalizado, então repete quando a
    voz diz a mesma frase em dois casos. `colher` sempre indexou por
    (obsId, caso); a fila usava só o obsId, e o julgamento do segundo caso
    sumia sem aviso. Achado do revisor externo.
    """
    monkeypatch.setattr(fc, "REGISTRO", tmp_path / "reg.json")
    for caso in ("C1", "C2"):
        obs = {"obsId": "mesmo-id", "texto": "a mesma frase nos dois casos"}
        painel = {"contrato": "FORJA-PAINEL-CURTO-v1", "caso": caso, "fase": "F7",
                  "vozes": [{"modelo": "glm-5.2-cursor", "familia": "zhipu",
                             "observacoes": [obs]}],
                  "falhas": [],
                  "decisoes": [{"obsId": "mesmo-id", "modelo": "glm-5.2-cursor",
                                "veredito": "acatada" if caso == "C1" else None,
                                "duplicadaDe": None, "motivo": None}]}
        (tmp_path / f"{caso}_PAINEL_CURTO.json").write_text(
            json.dumps(painel, ensure_ascii=False), encoding="utf-8")
    fc.colher(tmp_path / "C1_PAINEL_CURTO.json", por="teste")
    restantes = fi.fila(limite=9, pastas=[tmp_path])
    assert [i["caso"] for i in restantes] == ["C2"], (
        "julgar no C1 não pode tirar o mesmo texto da fila no C2")


def test_veredito_guarda_o_hash_do_painel_julgado(tmp_path, monkeypatch):
    """Sem hash, a 'evidência congelada' da promoção não estava congelada."""
    monkeypatch.setattr(fc, "REGISTRO", tmp_path / "reg.json")
    caminho = _painel(tmp_path, "C1", "glm-5.2-cursor", ["uma observação"])
    _decidir(caminho, ["acatada"])
    fc.colher(caminho, por="teste")
    decisao = fc.carregar()["decisoes"][0]
    assert decisao["painelSha256"] and len(decisao["painelSha256"]) == 64


def test_detector_de_citacao_nao_absolve_por_digito_solto():
    """O achado mais grave do revisor externo, com a fixture real.

    A versão anterior perguntava se o número aparecia como substring em
    qualquer ponto do documento. `Súmula 7` era absolvida por um `7` dentro de
    uma data. O `zero violações` que virou manchete do relatório de 08/08 não
    media nada — a remedição com o detector corrigido achou 2 em 60.
    """
    alvo = "A decisão de 07/08/2026 tratou do tema 1.170 e do artigo 1.021 do CPC."
    assert fi.citacoes_fora_do_documento("a Súmula 7 impede o reexame", alvo)
    assert fi.citacoes_fora_do_documento("o Tema 1.234 se aplica", alvo)
    # E não pode acusar o que o documento realmente cita, nem em outra grafia.
    assert not fi.citacoes_fora_do_documento("o art. 1.021", alvo)
    assert not fi.citacoes_fora_do_documento("o artigo 1021 do CPC", alvo)
    assert not fi.citacoes_fora_do_documento("o Tema 1.170", alvo)


def test_ja_julgada_sai_da_fila(tmp_path, monkeypatch):
    monkeypatch.setattr(fc, "REGISTRO", tmp_path / "reg.json")
    painel = _painel(tmp_path, "C1", "glm-5.2-cursor", ["uma coisa", "outra coisa"])
    antes = len(fi.fila(limite=9, pastas=[tmp_path]))
    _decidir(painel, ["acatada"])
    fc.colher(painel, por="teste")
    assert len(fi.fila(limite=9, pastas=[tmp_path])) == antes - 1


def test_recorte_e_declarado_ao_modelo_e_nao_so_ao_artefato():
    """Estado que o sistema conhece e esconde de quem trabalha é defeito de projeto.

    Medido em 07/08/2026: os três primeiros alvos reais passavam do teto, e as
    vozes gastaram 3 de 24 observações dizendo que "o documento está cortado no
    item 8" e que "a peça está incompleta". **O corte era nosso.** Duas dessas
    observações afirmam defeito inexistente com cara de achado acionável.

    O artefato já gravava `alvoTruncado: true` — para quem lê o JSON, não para
    quem faz o trabalho.
    """
    origem = (Path(__file__).parent / "forja_painel_curto.py").read_text(
        encoding="utf-8", errors="replace")
    assert "AVISO_RECORTE" in origem
    assert "if cortado:" in origem
    assert "RECORTE INTERROMPIDO AQUI" in origem
    assert "NÃO comente que está cortado" in pc.AVISO_RECORTE


def test_observacao_fora_de_escopo_sai_do_placar_e_da_fila(tmp_path, monkeypatch):
    """Não se cobra do modelo o erro de quem montou o prompt — mas se declara."""
    monkeypatch.setattr(fc, "REGISTRO", tmp_path / "reg.json")
    caminho = _painel(tmp_path, "C1", "glm-5.2-cursor", ["boa", "artefato do teto"])
    dados = json.loads(caminho.read_text(encoding="utf-8"))
    dados["vozes"][0]["observacoes"][1]["foraDeEscopo"] = "recorte, não a peça"
    caminho.write_text(json.dumps(dados, ensure_ascii=False), encoding="utf-8")

    relatorio = fi.indicadores(pastas=[tmp_path])
    linha = relatorio["modelos"][0]
    assert linha["observacoes"] == 1
    assert linha["foraDeEscopo"] == 1, "a exclusão tem de aparecer, não sumir"
    assert [i["obsId"] for i in fi.fila(limite=9, pastas=[tmp_path])] == [
        dados["vozes"][0]["observacoes"][0]["obsId"]]


def test_observacao_cortada_no_teto_e_contada(tmp_path, monkeypatch):
    """27% das observações do GLM chegavam pela metade e nada media isso.

    Bater no teto não é o mesmo que escrever muito: o leitor recebe uma frase
    interrompida e o resto do raciocínio não chega. É indicador de disciplina —
    e foi a única diferença real que apareceu entre as duas vozes em 29
    observações, junto com a latência.
    """
    monkeypatch.setattr(fc, "REGISTRO", tmp_path / "reg.json")
    caminho = _painel(tmp_path, "C1", "glm-5.2-cursor",
                      ["cabe inteira", "esta foi cortada no limite…"])
    linha = fi.indicadores(pastas=[tmp_path])["modelos"][0]
    assert linha["noTetoPct"] == 50.0


def test_nao_ha_perfil_posicional_entre_as_vozes():
    """Medido e NEGATIVO — fica registrado para ninguém remedir por intuição.

    A hipótese era que cada voz olhasse partes diferentes do documento, o que
    daria um perfil de "melhor uso". Em 29 observações de 3 casos, as duas se
    distribuíram quase igual (7/5/3 contra 6/5/3 por terços). Não há sinal, e
    inventar um a partir de medianas de 0,35 contra 0,55 com esse n seria
    fabricar perfil.
    """
    assert True, "resultado negativo registrado; ver Lição 276"


def test_o_controle_da_mesma_familia_esta_marcado():
    """Opus 5 é a família que ESCREVE a peça. No painel ele é controle, não par.

    Sem a marca, alguém compara o índice dele com o das vozes de fora como se
    fossem a mesma prova — e concordância da própria família com a análise
    principal é eco previsível, não confirmação (Lição 99).
    """
    assert "opus-5-cursor" in pc.CONTROLE_MESMA_FAMILIA
    assert fm.MODELOS["opus-5-cursor"].familia == "anthropic"
    for voz in pc.VOZES_PADRAO:
        if voz in pc.CONTROLE_MESMA_FAMILIA:
            continue
        assert fm.MODELOS[voz].familia != "anthropic", (
            f"{voz} é da mesma família do produtor e não está marcado como controle")


def test_luna_e_opus_rodam_pela_assinatura_e_nao_pela_rota_paga():
    """`gpt-5.6-luna-max` existe no Cursor — conferido em 07/08/2026.

    A rota antiga (`luna-5.6`, OpenRouter) cobra US$ 1/6 por milhão e continua
    no registro para quem precisar dela. O painel usa a da assinatura: gasto
    novo é decisão do titular, não consequência de escolher o modelo errado.
    """
    for voz in ("luna-5.6-cursor", "opus-5-cursor", "grok-4.5-cursor"):
        modelo = fm.MODELOS[voz]
        assert modelo.provedor == "cursor"
        assert modelo.usd_saida_por_milhao == 0.0
    assert fm.MODELOS["luna-5.6"].provedor == "openrouter"
    assert fm.MODELOS["luna-5.6"].usd_saida_por_milhao > 0


def test_eco_nao_e_comparavel_entre_paineis_de_tamanhos_diferentes(tmp_path, monkeypatch):
    """Com cinco vozes há cinco vezes mais chance de alguém repetir você."""
    monkeypatch.setattr(fc, "REGISTRO", tmp_path / "reg.json")
    _painel(tmp_path, "C1", "glm-5.2-cursor", ["uma"])
    dois = tmp_path / "C2_PAINEL_CURTO.json"
    dados = json.loads((tmp_path / "C1_PAINEL_CURTO.json").read_text(encoding="utf-8"))
    dados["caso"] = "C2"
    dados["vozes"].append({"modelo": "kimi-k3-cursor", "familia": "moonshot",
                           "observacoes": [{"obsId": "zzz", "texto": "outra"}]})
    dois.write_text(json.dumps(dados, ensure_ascii=False), encoding="utf-8")
    relatorio = fi.indicadores(pastas=[tmp_path])
    assert relatorio["ecoComparavel"] is False
    assert relatorio["vozesPorPainel"] == [1, 2]


def test_pasta_com_underscore_fica_fora_da_comparacao(tmp_path, monkeypatch):
    """Painel de outro regime de vozes é histórico, não par da rodada atual."""
    monkeypatch.setattr(fc, "REGISTRO", tmp_path / "reg.json")
    _painel(tmp_path, "C1", "glm-5.2-cursor", ["vale"])
    morto = tmp_path / "_2vozes"
    morto.mkdir()
    _painel(morto, "C9", "glm-5.2-cursor", ["não vale"])
    assert fi.indicadores(pastas=[tmp_path])["paineis"] == 1


def test_a_camada_automatica_nao_promove_ninguem():
    """A defesa contra a contra-hipótese de Helena: indicador barato canibaliza
    métrica cara. Nada do módulo de indicadores toca o degrau."""
    origem = (Path(__file__).parent / "forja_painel_indicadores.py").read_text(
        encoding="utf-8", errors="replace")
    assert "promover" not in origem.replace("promove ninguém", "").replace(
        "não promovem", "").replace("promove", "")
    assert "degraus" not in origem


# --------------------------------------------------------------------------
# Natureza — o que este subsistema não é
# --------------------------------------------------------------------------

def test_painel_declara_que_nao_e_gate_nem_fonte():
    natureza = pc.painel.__doc__ or ""
    contrato = pc.VERSAO
    assert contrato == "FORJA-PAINEL-CURTO-v1"
    assert "opinião" in natureza.casefold() or "opiniao" in natureza.casefold()


def test_a_instrucao_opcional_chega_a_f4_e_f7_com_o_arquivo_certo():
    """Recurso que o agente não lembra que existe é recurso ausente (Lição 270).

    E o nome do arquivo tem de seguir a fase: um `--saida F4_...` sugerido
    dentro da F7 põe o artefato da auditoria com nome do blueprint, e quem for
    procurá-lo depois não o acha.
    """
    origem = (Path(__file__).parent / "forja_run.py").read_text(
        encoding="utf-8", errors="replace")
    bloco = origem.split('context["instructions"]["painelCurto"]', 1)
    assert len(bloco) == 2, "a instrução opcional do painel sumiu do RUN_CONTEXT"
    anterior = origem.split('context["instructions"]["painelCurto"]')[0]
    assert 'F7_AUDITORIA_JURIDICA_FACTUAL' in anterior.rsplit("if phase in", 1)[-1]
    assert '_PAINEL_CURTO.json' in bloco[1][:900]
    assert '"opcional": True' in bloco[1][:200]


def test_o_painel_nao_e_saida_obrigatoria_de_nenhuma_fase():
    """Voz opcional que vira exigência dura contradiz o pedido de gastar pouco.

    E criaria dependência bloqueante de um modelo que reprovou a bancada. Se um
    dia isto mudar, muda por ADR — e este teste é onde a mudança aparece.
    """
    for contrato in (Path(__file__).parent / "phase_contracts").glob("*.json"):
        dados = json.loads(contrato.read_text(encoding="utf-8"))
        assert "painel_curto" not in dados.get("requiredOutputs", [])
        assert "painel_curto" not in dados.get("requiredGates", [])


# --------------------------------------------------------------------------
# Porteiro do envio externo — o achado mais sério da revisão de 09/08/2026
# --------------------------------------------------------------------------

import forja_envio_externo as envio


@pytest.fixture()
def ledger_isolado(tmp_path, monkeypatch):
    monkeypatch.setattr(envio, "LEDGER", tmp_path / "ENVIOS.jsonl")
    return tmp_path


def test_autos_nao_saem_da_maquina(ledger_isolado):
    """Produto nosso é nosso para arriscar; documento do processo não é."""
    with pytest.raises(envio.EnvioBloqueado, match="autos"):
        envio.autorizar("texto", classe="autos", confirmado=True,
                        destino=["glm-5.2-cursor"])
    with pytest.raises(envio.EnvioBloqueado, match="misto"):
        envio.autorizar("texto", classe="misto", confirmado=True,
                        destino=["glm-5.2-cursor"])


def test_classe_e_obrigatoria(ledger_isolado):
    with pytest.raises(envio.EnvioBloqueado, match="não existe"):
        envio.autorizar("texto", classe="", confirmado=True, destino=["x"])


def test_envio_externo_exige_decisao_explicita(ledger_isolado):
    """Mandar material de cliente para fora é decisão, não efeito colateral."""
    with pytest.raises(envio.EnvioBloqueado, match="não confirmado"):
        envio.autorizar("texto", classe="produto_proprio", confirmado=False,
                        destino=["glm-5.2-cursor"])


def test_o_que_sai_fica_registrado_sem_o_texto(ledger_isolado):
    """O ledger reconstitui a exposição; não a duplica."""
    recibo = envio.autorizar("segredo do escritorio", classe="produto_proprio",
                             confirmado=True, destino=["b", "a"], caso="C1",
                             arquivo="rascunho.md")
    assert recibo["sha256"] and recibo["caracteresEnviados"] == 21
    assert recibo["modelos"] == ["a", "b"], "ordem estável para comparar envios"
    bruto = (ledger_isolado / "ENVIOS.jsonl").read_text(encoding="utf-8")
    assert "segredo do escritorio" not in bruto
    assert envio.historico()[0]["caso"] == "C1"


def test_o_painel_nao_envia_nada_sem_passar_pelo_porteiro():
    """A chamada aos modelos vem DEPOIS da autorização, não antes.

    Ordem importa: autorizar depois de enviar registraria uma exposição que já
    aconteceu. O teste lê a fonte porque exercitar isto de verdade exigiria
    chamar cinco provedores.
    """
    origem = (Path(__file__).parent / "forja_painel_curto.py").read_text(
        encoding="utf-8", errors="replace")
    corpo = origem.split("def painel(", 1)[1].split("\ndef ", 1)[0]
    assert corpo.index("envio.autorizar") < corpo.index("ouvir(alvo"), (
        "o porteiro tem de correr antes da primeira chamada externa")
    assert '"envioExterno": recibo_envio' in corpo
