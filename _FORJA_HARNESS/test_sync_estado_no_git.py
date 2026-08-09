# -*- coding: utf-8 -*-
"""Regressão do que o sincronizador publica sem estar commitado.

Origem: em 09/08/2026 um script que outra sessão ainda estava escrevendo foi
deliberadamente deixado fora do commit local — arquivo pela metade não entra na
história — e mesmo assim subiu ao `forja-motor` na sincronização seguinte. A
causa é de projeto: `sync_forja_repos.py` copia da **pasta de trabalho** e não
do índice do Git. A cautela do commit não se transferia para a publicação, e
nada no laudo dizia que aquilo tinha acontecido.

O conserto não é exigir rastreamento. Medido no dia, dos 10.884 arquivos
publicados 79 não estavam rastreados, e 52 deles eram ledgers de evento do
acervo, que nascem a cada execução e nunca estariam commitados na hora da
sincronização: barrar pararia a publicação da cadeia de auditoria toda noite.
São dois casos com respostas diferentes — ignorado pelo `.gitignore` é
declaração humana e não é publicado; ainda não commitado é publicado e
declarado.

Os testes montam repositórios de verdade em pasta temporária. `estado_no_git`
consulta `git` sobre `TRABALHO`, que é constante de módulo, então cada teste
aponta a constante para o repositório de mentira e a devolve no fim.
"""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "git-tools"))

import sync_forja_repos as sync  # noqa: E402


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(repo), *args],
                          capture_output=True, text=True, encoding="utf-8",
                          errors="replace")


class _RepoDeMentira:
    """Repositório Git descartável, com o mínimo para `git ls-files` responder."""

    def __enter__(self) -> "_RepoDeMentira":
        self._tmp = tempfile.TemporaryDirectory()
        self.raiz = Path(self._tmp.name).resolve()
        _git(self.raiz, "init", "-q", "-b", "main")
        _git(self.raiz, "config", "user.name", "teste")
        _git(self.raiz, "config", "user.email", "teste@localhost")
        self._anterior = sync.TRABALHO
        sync.TRABALHO = self.raiz
        return self

    def __exit__(self, *exc) -> None:
        sync.TRABALHO = self._anterior
        self._tmp.cleanup()

    def escrever(self, rel: str, texto: str = "x") -> None:
        alvo = self.raiz / rel
        alvo.parent.mkdir(parents=True, exist_ok=True)
        alvo.write_text(texto, encoding="utf-8")

    def commitar(self, *rels: str) -> None:
        for rel in rels:
            _git(self.raiz, "add", "--", rel)
        _git(self.raiz, "commit", "-q", "-m", "fixture")


class TestEstadoNoGit(unittest.TestCase):
    def test_separa_commitado_novo_e_ignorado(self):
        with _RepoDeMentira() as r:
            r.escrever(".gitignore", "vendor/\n")
            r.escrever("motor/pronto.py")
            r.commitar(".gitignore", "motor/pronto.py")
            r.escrever("motor/forja_skill_doctor.py")   # o defeito real
            r.escrever("vendor/olefile/doc/API.md")     # excluído por declaração

            ignorados, novos, indisponivel = sync.estado_no_git([
                ".gitignore", "motor/pronto.py",
                "motor/forja_skill_doctor.py", "vendor/olefile/doc/API.md"])

            self.assertIsNone(indisponivel)
            self.assertEqual(ignorados, {"vendor/olefile/doc/API.md"})
            self.assertEqual(novos, {"motor/forja_skill_doctor.py"})

    def test_arvore_toda_commitada_nao_reporta_nada(self):
        """Sem novidade não há aviso — gate que fala sempre deixa de ser lido."""
        with _RepoDeMentira() as r:
            r.escrever("a.py")
            r.commitar("a.py")
            self.assertEqual(sync.estado_no_git(["a.py"]), (set(), set(), None))

    def test_ledger_de_evento_nao_commitado_e_novo_e_nao_ignorado(self):
        """O caso que proíbe barrar: 52 destes por sincronização, todos legítimos."""
        with _RepoDeMentira() as r:
            r.escrever(".gitignore", "__pycache__/\n")
            r.commitar(".gitignore")
            rels = [f"state/case-x/events/{n:08d}-evt.json" for n in range(4)]
            for rel in rels:
                r.escrever(rel, "{}")
            ignorados, novos, indisponivel = sync.estado_no_git(rels)
            self.assertIsNone(indisponivel)
            self.assertEqual(ignorados, set())
            self.assertEqual(novos, set(rels))

    def test_fora_de_repositorio_degrada_aberto_com_motivo(self):
        """Publicar segue; o que não pode é a conferência falhar em silêncio."""
        with tempfile.TemporaryDirectory() as tmp:
            anterior = sync.TRABALHO
            sync.TRABALHO = Path(tmp).resolve()
            try:
                ignorados, novos, indisponivel = sync.estado_no_git(["a.py"])
            finally:
                sync.TRABALHO = anterior
            self.assertEqual((ignorados, novos), (set(), set()))
            self.assertIsNotNone(indisponivel)
            self.assertIn("repositório", indisponivel)

    def test_caminho_com_acento_e_espaco_sobrevive(self):
        """Metade das pastas desta casa tem acento e espaço; -z existe por isso."""
        with _RepoDeMentira() as r:
            rel = "Petições e anexos/Ação — nº 1/peça.md"
            r.escrever(rel)
            ignorados, novos, indisponivel = sync.estado_no_git([rel])
            self.assertIsNone(indisponivel)
            self.assertEqual(novos, {rel})


class TestPoliticaDePublicacao(unittest.TestCase):
    """A regra de decisão, isolada do Git: quem fica de fora em cada modo."""

    IGNORADOS = {"vendor/doc.md"}
    NOVOS = {"state/events/1.json"}

    def test_padrao_publica_o_novo_e_recusa_o_ignorado(self):
        self.assertEqual(
            sync.fora_da_publicacao(self.IGNORADOS, self.NOVOS, so_rastreados=False),
            self.IGNORADOS)

    def test_estrito_recusa_os_dois(self):
        self.assertEqual(
            sync.fora_da_publicacao(self.IGNORADOS, self.NOVOS, so_rastreados=True),
            self.IGNORADOS | self.NOVOS)

    def test_nao_devolve_os_conjuntos_de_entrada(self):
        """`main` filtra as listas com este resultado; devolver o próprio conjunto
        de entrada faria uma mutação posterior mudar o que o laudo reporta."""
        ignorados = {"a"}
        fora = sync.fora_da_publicacao(ignorados, set(), so_rastreados=False)
        fora.add("b")
        self.assertEqual(ignorados, {"a"})


if __name__ == "__main__":
    unittest.main()
