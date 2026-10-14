import unittest
from scripts.indexar_dispositivos import extrair_dispositivos


class TestDispositivos(unittest.TestCase):
    def test_artigos_em_paragrafos(self):
        html = """<html><body>
        <p>Art. 1º Esta Lei dispõe sobre normas gerais de contratação pública.</p>
        <p>Parágrafo único. Aplica-se aos órgãos previstos nesta Lei.</p>
        <p>Art. 2º Esta Lei aplica-se às seguintes contratações.</p>
        </body></html>"""
        arts = extrair_dispositivos(html)
        self.assertEqual([a["artigo"] for a in arts], [1, 2])
        self.assertIn("Parágrafo único.", arts[0]["texto"])

    def test_ignora_scripts_e_texto_sem_artigo(self):
        html = "<script>Art. 5º conteúdo falso</script><p>Somente texto descritivo</p>"
        self.assertEqual(extrair_dispositivos(html), [])


if __name__ == "__main__":
    unittest.main()
