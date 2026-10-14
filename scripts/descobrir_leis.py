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

YEARS = range(2020, 2027)
def url_indice(ano: int) -> str:
    inicio = ((ano - 2019) // 4) * 4 + 2019
    fim = inicio + 3
    return f"https://www.planalto.gov.br/ccivil_03/_ato{inicio}-{fim}/{ano}/lei/_leis{ano}.htm"

BASE = url_indice(2026)
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


def extrair(html: str, base: str = BASE, ano: int = 2026) -> list[dict]:
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
        ident = f"L-{numero}-{ano}"
        encontrados[ident] = {"id": ident, "numero": numero, "ano": ano, "url": url, "rotulo": f"Lei nº {numero:,}".replace(",", ".")}
    return sorted(encontrados.values(), key=lambda item: item["numero"], reverse=True)


def main():
    anterior = json.loads(OUTPUT.read_text(encoding="utf-8")) if OUTPUT.exists() else {}
    anteriores = {item["id"]: item for item in anterior.get("leis", [])}
    consolidados = dict(anteriores)
    fontes, falhas = [], []
    for ano in YEARS:
        url = url_indice(ano)
        try:
            req = Request(url, headers={"User-Agent": "ProjetoLeisResearchBot/0.2 (+https://github.com/douglassnake/projeto-leis)"})
            with urlopen(req, timeout=25) as response:
                html = response.read().decode("windows-1252", errors="replace")
            itens = extrair(html, url, ano)
            if not itens:
                raise ValueError("índice sem links válidos")
            consolidados.update({item["id"]: item for item in itens})
            fontes.append({"ano": ano, "url": url, "registros": len(itens)})
        except (OSError, ValueError) as exc:
            falhas.append({"ano": ano, "erro": type(exc).__name__})
    if not fontes:
        raise RuntimeError("Nenhum índice acessível; dados anteriores preservados.")
    novos = sorted(set(consolidados) - set(anteriores))
    encontrados = sorted(consolidados.values(), key=lambda x: (x["ano"], x["numero"]), reverse=True)
    saida = {
        "fonte": BASE, "fontes_consultadas": fontes, "falhas": falhas,
        "consultado_em": datetime.now(timezone.utc).isoformat(),
        "tipo": "descoberta_de_referencias",
        "aviso": "Links descobertos não comprovam publicação, ementa, texto integral ou vigência.",
        "total": len(encontrados),
        "novos_desde_ultima_consulta": novos if anteriores else [],
        "leis": encontrados,
    }
    OUTPUT.write_text(json.dumps(saida, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Índices consultados: {len(fontes)} | registros: {len(encontrados)} | novos: {len(novos)} | falhas: {len(falhas)}")


if __name__ == "__main__":
    main()
