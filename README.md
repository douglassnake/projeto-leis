# Projeto Leis

Pesquisa jurídica brasileira com fontes oficiais, busca rápida, conexões normativas verificáveis e monitoramento diário.

## Versão inicial

- Portal web estático e responsivo (compatível com GitHub Pages).
- Catálogo inicial de normas federais com links para textos oficiais.
- Pesquisa por assunto, número, ano, ementa e termos.
- Referências cruzadas **curadas** e identificadas como tais; nenhuma conclusão sobre vigência é produzida automaticamente.
- Coletor Python para conferir acessibilidade e metadados de fontes oficiais.
- GitHub Actions: testes, coleta diária e publicação do portal.
- Dados públicos em `data/leis.json` e log da última coleta em `data/coleta.json`.

## Como usar

Abra `index.html` localmente ou ative **Settings → Pages → Build and deployment → Source: GitHub Actions**. O workflow `pages.yml` também pode ser disparado manualmente.

## Desenvolvimento local

```bash
python -m http.server 8000
# http://localhost:8000
python -m unittest discover -s tests -v
python scripts/coletar.py
```

## Limites jurídicos importantes

- Esta primeira versão é um **índice de referências**: para uso jurídico, confira o texto consolidado, alterações e a vigência na fonte oficial.
- O coletor inicial confere páginas de referência; **não** garante cobertura integral do Diário Oficial nem atualização de todos os atos do país.
- Conexões normativas somente entram no índice após inclusão explícita com fundamento verificável.
- Datas de conferência técnica não significam verificação jurídica da vigência.
- Não digite dados pessoais, sigilosos ou de clientes nesta versão pública e sem autenticação.

## Próximos marcos

1. Ingestão incremental das publicações do DOU via fontes autorizadas e deduplicação por identificadores oficiais.
2. Versionamento artigo a artigo, identificação auditável de alterações, revogações e vigência temporal.
3. Busca híbrida/semântica com citações, autenticação, alertas e trilhas de auditoria.
4. Backend e PostgreSQL para produção comercial (GitHub Pages serve apenas site estático).

## Fontes

- Planalto: https://www4.planalto.gov.br/legislacao
- LexML: https://www.lexml.gov.br/
- INLABS/DOU: https://inlabs.in.gov.br/
- Câmara: https://dadosabertos.camara.leg.br/
- Senado: https://www12.senado.leg.br/dados-abertos/

Licença de software: MIT. Conteúdos oficiais permanecem sujeitos às respectivas regras de uso e atribuição.
