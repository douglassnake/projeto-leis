#!/usr/bin/env python3
"""Descoberta incremental de links de leis ordinárias no índice oficial do Planalto.

Registra links sem inferir ementa, data de publicação ou vigência. Mudanças
são propostas como monitoramento, não como validação jurídica automática.
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

BASE = "https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2026/lei/_leis2026.htm"
ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "novidades.json"
LAW_RE = re.compile(r"(?:^|/)l(\d{4,6})(?:\.htm|\.html)$", re.I)


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.href = None

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.href = dict(attrs).get("href")

    def handle_endtag(self, tag):
        if tag == "a":
            self.href = None

    def handle_data(self, data):
        if self.href:
            self.links.append((self.href, data.strip()))


def extrair(html: str, base: str = BASE) -> list[dict]:
    parser = LinkParser()
    parser.feed(html)
    encontrados = {}
    for href, texto in parser.links:
        url = urljoin(base, href)
        parsed = urlparse(url)
        if parsed.scheme != "https" or parsed.hostname not in {"www.planalto.gov.br", "planalto.gov.br"}:
            continue
        match = LAW_RE.search(parsed.path)
        if not match:
            continue
        numero = int(match.group(1))
        ident = f"L-{numero}-2026"
        encontrados[ident] = {"id": ident, "numero": numero, "ano": 2026, "url": url, "rotulo": f"Lei nº {numero:,}".replace(",", ".")}
    return sorted(encontrados.values(), key=lambda item: item["numero"], reverse=True)


def main():
    req = Request(BASE, headers={"User-Agent": "ProjetoLeisResearchBot/0.1 (+https://github.com/douglassnake/projeto-leis)"})
    with urlopen(req, timeout=40) as response:
        html = response.read().decode("windows-1252", errors="replace")
    encontrados = extrair(html)
    if not encontrados:
        raise RuntimeError("Nenhuma lei encontrada: manter os dados anteriores e revisar o parser.")
    anterior = json.loads(OUTPUT.read_text(encoding="utf-8")) if OUTPUT.exists() else {}
    anteriores = {item["id"] for item in anterior.get("leis", [])}
    novos = [item["id"] for item in encontrados if item["id"] not in anteriores]
    saida = {
        "fonte": BASE,
        "consultado_em": datetime.now(timezone.utc).isoformat(),
        "tipo": "descoberta_de_referencias",
        "aviso": "Novos links não comprovam data de publicação, vigência ou texto consolidado.",
        "total": len(encontrados),
        "novos_desde_ultima_consulta": [] if not anteriores else novos,
        "leis": encontrados,
    }
    OUTPUT.write_text(json.dumps(saida, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Links encontrados: {len(encontrados)} | novos após base inicial: {len(saida['novos_desde_ultima_consulta'])}")


if __name__ == "__main__":
    main()
