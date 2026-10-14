import unittest
from scripts.descobrir_leis import extrair, url_indice


class TestDescoberta(unittest.TestCase):
    def test_extrai_apenas_links_de_leis_no_planalto(self):
        html = """<a href="l15526.htm">Lei nº 15.526</a>
        <a href="/ccivil_03/_ato2023-2026/2026/lei/l15525.htm">Lei nº 15.525</a>
        <a href="https://site-falso.example/l15524.htm">Lei falsa</a>
        <a href="decreto123.htm">Decreto</a>"""
        leis = extrair(html)
        self.assertEqual([lei["numero"] for lei in leis], [15526, 15525])
        self.assertTrue(all(lei["url"].startswith("https://www.planalto.gov.br/") for lei in leis))

    def test_indice_por_quadriênio(self):
        self.assertIn("_ato2019-2022/2020/lei/_leis2020.htm", url_indice(2020))
        self.assertIn("_ato2019-2022/2022/lei/_leis2022.htm", url_indice(2022))
        self.assertIn("_ato2023-2026/2026/lei/_leis2026.htm", url_indice(2026))

    def test_extracao_ano_especifico(self):
        links = extrair('<a href="l14001.htm">Lei</a>', url_indice(2021), 2021)
        self.assertEqual(links[0]["id"], "L-14001-2021")

    def test_rejeita_documentos_fora_do_padrao(self):
        self.assertEqual(extrair("<a href='javascript:alert(1)'>x</a>"), [])


if __name__ == "__main__":
    unittest.main()
