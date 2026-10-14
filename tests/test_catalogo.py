import json
import unittest
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]


class CatalogoTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dados = json.loads((ROOT / "data/leis.json").read_text(encoding="utf-8"))
        cls.leis = cls.dados["leis"]

    def test_ids_unicos(self):
        ids = [l["id"] for l in self.leis]
        self.assertEqual(len(ids), len(set(ids)))

    def test_campos_obrigatorios(self):
        for lei in self.leis:
            with self.subTest(id=lei["id"]):
                for campo in ("id", "tipo", "numero", "ano", "titulo", "temas", "url", "relacoes"):
                    self.assertIn(campo, lei)
                self.assertTrue(lei["titulo"].strip())
                self.assertIsInstance(lei["ano"], int)
                self.assertTrue(lei["temas"])
                self.assertEqual(urlparse(lei["url"]).scheme, "https")
                self.assertEqual(urlparse(lei["url"]).hostname, "www.planalto.gov.br")

    def test_relacoes_sem_pontas_soltas(self):
        ids = {lei["id"] for lei in self.leis}
        for lei in self.leis:
            for rel in lei["relacoes"]:
                with self.subTest(origem=lei["id"], alvo=rel["alvo"]):
                    self.assertIn(rel["alvo"], ids)
                    self.assertTrue(rel["tipo"])
                    self.assertTrue(rel["fundamento"].strip())

    def test_lei_14133_relacao_fundamentada(self):
        lei = next(x for x in self.leis if x["id"] == "L-14133-2021")
        self.assertTrue(any(x["alvo"] == "L-8666-1993" and "193" in x["fundamento"] for x in lei["relacoes"]))


if __name__ == "__main__":
    unittest.main()
