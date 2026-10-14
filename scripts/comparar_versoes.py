#!/usr/bin/env python3
"""Comparação de extrações, não determinação de alteração legislativa.

Hashes de dispositivos permitem sinalizar diferenças técnicas entre coletas.
Somente o processo jurídico de revisão poderá classificá-las como alterações legais.
"""
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/dispositivos.json"
DEST = ROOT / "data/revisoes.json"


def assinatura(texto):
    # Normalizar apenas espaços; nenhuma interpretação jurídica.
    canon = re.sub(r"\s+", " ", texto).strip()
    return hashlib.sha256(canon.encode("utf-8")).hexdigest()


def comparar(antigo, novo, momento):
    anteriores = antigo.get("assinaturas", {})
    atuais = {}
    eventos = []
    for norma in novo.get("normas", []):
        for artigo in norma.get("artigos", []):
            chave = f'{norma["lei_id"]}:art:{artigo["artigo"]}'
            atual = assinatura(artigo["texto"])
            atuais[chave] = atual
            if chave in anteriores and anteriores[chave] != atual:
                eventos.append({"chave": chave, "tipo": "diferenca_textual", "detectado_em": momento, "revisao": "pendente", "fonte": norma["fonte"]})
            elif chave not in anteriores and anteriores:
                eventos.append({"chave": chave, "tipo": "novo_no_indice", "detectado_em": momento, "revisao": "pendente", "fonte": norma["fonte"]})
    # Omissões na extração não são tratadas como revogações.
    ausentes = sorted(set(anteriores) - set(atuais))
    historico = antigo.get("eventos", []) + eventos
    return {
        "tipo": "monitoramento_de_diferencas_tecnicas",
        "aviso": "Diferença textual NÃO comprova alteração legal. Ausência de artigo NÃO comprova revogação.",
        "comparado_em": momento,
        "artigos_monitorados": len(atuais),
        "assinaturas": atuais,
        "ausentes_na_extracao": ausentes,
        "eventos": historico[-2000:],
    }


def main():
    atual = json.loads(SOURCE.read_text(encoding="utf-8"))
    anterior = json.loads(DEST.read_text(encoding="utf-8")) if DEST.exists() else {}
    agora = datetime.now(timezone.utc).isoformat()
    resultado = comparar(anterior, atual, agora)
    DEST.write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Artigos monitorados:", resultado["artigos_monitorados"], "Eventos históricos:", len(resultado["eventos"]))


if __name__ == "__main__":
    main()
