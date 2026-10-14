import unittest
from scripts.comparar_versoes import assinatura, comparar


class ComparacaoTest(unittest.TestCase):
    def test_normalizacao_de_espacos(self):
        self.assertEqual(assinatura("Art. 1º  Texto"), assinatura("Art. 1º\nTexto"))

    def test_diferenca_nao_e_revogacao(self):
        velho = {"assinaturas": {"L-1-2020:art:1": assinatura("Antigo"), "L-1-2020:art:2": assinatura("Existente")}, "eventos": []}
        novo = {"normas": [{"lei_id": "L-1-2020", "fonte": "https://www.planalto.gov.br/lei.htm", "artigos": [{"artigo": 1, "texto": "Novo"}]}]}
        result = comparar(velho, novo, "2026-10-14T00:00:00Z")
        self.assertEqual(result["eventos"][0]["tipo"], "diferenca_textual")
        self.assertEqual(result["eventos"][0]["revisao"], "pendente")
        self.assertEqual(result["ausentes_na_extracao"], ["L-1-2020:art:2"])
        self.assertNotIn("revogado", str(result["eventos"]))


if __name__ == "__main__":
    unittest.main()
