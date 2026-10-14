#!/usr/bin/env python3
"""Verificador conservador das URLs oficiais do índice inicial.

Não é um coletor de todas as publicações legislativas. Não altera vigência,
ementas nem conexões sem revisão jurídica. Grava resultados determinísticos
quando há acesso à internet; falhas de rede são reportadas sem apagar dados.
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "data" / "leis.json"
REPORT = ROOT / "data" / "coleta.json"


def verificar_url(url: str, timeout: int = 18) -> dict:
    req = Request(url, headers={"User-Agent": "ProjetoLeisResearchBot/0.1 (+https://github.com/douglassnake/projeto-leis)", "Accept": "text/html,application/xhtml+xml"})
    try:
        with urlopen(req, timeout=timeout) as response:
            return {"http": response.status, "final_url": response.geturl(), "acessivel": 200 <= response.status < 400}
    except HTTPError as exc:
        return {"http": exc.code, "acessivel": False, "erro": "HTTP"}
    except (URLError, TimeoutError, OSError, ValueError) as exc:
        return {"http": None, "acessivel": False, "erro": type(exc).__name__}


def main() -> None:
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    registros = []
    for lei in data["leis"]:
        status = verificar_url(lei["url"])
        registros.append({"id": lei["id"], **status})
        print(lei["id"], status["http"], "OK" if status["acessivel"] else "indisponível")
    saida = {
        "executado_em": datetime.now(timezone.utc).isoformat(),
        "total": len(registros),
        "acessiveis": sum(x["acessivel"] for x in registros),
        "verificacoes": registros,
        "nota": "Checagem de acesso HTTP, NÃO é validação da vigência, integralidade nem atualização legal.",
    }
    REPORT.write_text(json.dumps(saida, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if not all(x["acessivel"] for x in registros):
        print("ATENÇÃO: algumas fontes não responderam. Verifique relatório; catálogo preservado.")


if __name__ == "__main__":
    main()
