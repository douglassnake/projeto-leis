import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class Elementos(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.nav = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag == "script" and "src" in attrs:
            self.nav.append(attrs["src"])


class TestPortal(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = (ROOT / "index.html").read_text(encoding="utf-8")
        cls.parser = Elementos()
        cls.parser.feed(cls.html)

    def test_elementos_essenciais(self):
        for ident in ("query", "searchForm", "tema", "results", "total", "count", "status", "graphSelect", "graphCanvas", "graphDetails", "monitorTotal", "monitorData", "monitorFalhas", "monitorItens"):
            with self.subTest(elemento=ident):
                self.assertIn(ident, self.parser.ids)

    def test_componentes_pesquisa_e_mapa(self):
        for trecho in ("function render()", "function desenharGrafo()", "function painelAtualizacoes(info)", "data/leis.json", "data/novidades.json", "aria-label", "noopener noreferrer"):
            with self.subTest(trecho=trecho):
                self.assertIn(trecho, self.html)

    def test_sem_dependencias_externas_executaveis(self):
        self.assertEqual(self.parser.nav, [])


if __name__ == "__main__":
    unittest.main()
