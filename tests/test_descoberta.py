import unittest
from scripts.descobrir_leis import extrair


class TestDescoberta(unittest.TestCase):
    def test_extrai_apenas_links_de_leis_no_planalto(self):
        html = """<a href="l15526.htm">Lei nº 15.526</a>
        <a href="/ccivil_03/_ato2023-2026/2026/lei/l15525.htm">Lei nº 15.525</a>
        <a href="https://site-falso.example/l15524.htm">Lei falsa</a>
        <a href="decreto123.htm">Decreto</a>"""
        leis = extrair(html)
        self.assertEqual([lei["numero"] for lei in leis], [15526, 15525])
        self.assertTrue(all(lei["url"].startswith("https://www.planalto.gov.br/") for lei in leis))

    def test_rejeita_documentos_fora_do_padrao(self):
        self.assertEqual(extrair("<a href='javascript:alert(1)'>x</a>"), [])


if __name__ == "__main__":
    unittest.main()
