#!/usr/bin/env python3
"""Índice experimental de dispositivos de um conjunto limitado de normas oficiais.

Parser conservador: texto para apoio à localização, sem alegar redação consolidada.
Documentos são obtidos diretamente do Planalto; origem e instante ficam registrados.
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "leis.json"
DEST = ROOT / "data" / "dispositivos.json"
ARTIGO = re.compile(r"(?<!\w)Art\.\s*(\d{1,4})(?:[º°o.]|\s)*(?:[-–][A-Z])?\b", re.I)
MAX_BYTES = 2_500_000
MAX_ARTICLES = 600


class TextoHTML(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.skip = 0
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style", "nav"}:
            self.skip += 1
        elif tag in {"p", "div", "br", "li", "h1", "h2", "h3", "tr"} and not self.skip:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in {"script", "style", "nav"} and self.skip:
            self.skip -= 1
        elif tag in {"p", "div", "li", "tr"} and not self.skip:
            self.parts.append("\n")

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)


def extrair_dispositivos(html: str, limite: int = MAX_ARTICLES) -> list[dict]:
    parser = TextoHTML()
    parser.feed(html)
    # Separa por quebra e retém apenas parágrafos cujo início denote artigo.
    linhas = [" ".join(x.split()) for x in "".join(parser.parts).splitlines()]
    registros = []
    atual = None
    for linha in linhas:
        if not linha:
            continue
        m = ARTIGO.match(linha)
        if m:
            if atual and len(atual["texto"]) > 18:
                registros.append(atual)
            if len(registros) >= limite:
                break
            atual = {"artigo": int(m.group(1)), "texto": linha[:7000]}
        elif atual and len(atual["texto"]) < 7000:
            atual["texto"] += "\n" + linha[:1000]
    if atual and len(atual["texto"]) > 18 and len(registros) < limite:
        registros.append(atual)
    # A extração pode incluir duplicatas do menu / cabeçalho; mantém primeiro.
    vistos = set()
    return [x for x in registros if not (x["artigo"] in vistos or vistos.add(x["artigo"]))]


def buscar(url: str) -> str:
    req = Request(url, headers={"User-Agent": "ProjetoLeisResearchBot/0.3 (+https://github.com/douglassnake/projeto-leis)"})
    with urlopen(req, timeout=28) as resp:
        raw = resp.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            raise ValueError("Documento excede limite de extração")
        charset = resp.headers.get_content_charset() or "windows-1252"
        return raw.decode(charset, errors="replace")


def main() -> None:
    normas = json.loads(SOURCE.read_text(encoding="utf-8"))["leis"]
    anterior = json.loads(DEST.read_text(encoding="utf-8")) if DEST.exists() else {}
    cache = {r["lei_id"]: r for r in anterior.get("normas", [])}
    erros = []
    for lei in normas:
        if lei["id"].startswith("CF-"):
            continue
        try:
            dispositivos = extrair_dispositivos(buscar(lei["url"]))
            if len(dispositivos) < 2:
                raise ValueError("Extração insuficiente ou estrutura HTML não reconhecida")
            cache[lei["id"]] = {
                "lei_id": lei["id"], "fonte": lei["url"],
                "extraido_em": datetime.now(timezone.utc).isoformat(),
                "artigos": dispositivos,
            }
            print(lei["id"], len(dispositivos), "dispositivos extraídos")
        except (OSError, ValueError, LookupError) as exc:
            erros.append({"lei_id": lei["id"], "erro": type(exc).__name__})
    saida = {
        "tipo": "extracao_experimental_de_texto",
        "aviso": "Texto extraído automaticamente para localização; estrutura, integridade, redação e vigência NÃO validadas. Confira fonte oficial.",
        "gerado_em": datetime.now(timezone.utc).isoformat(),
        "falhas": erros,
        "normas": sorted(cache.values(), key=lambda x: x["lei_id"]),
    }
    DEST.write_text(json.dumps(saida, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Normas indexadas:", len(cache), "Falhas:", len(erros))


if __name__ == "__main__":
    main()
