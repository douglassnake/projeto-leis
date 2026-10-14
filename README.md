# Projeto Leis

Pesquisa jurídica brasileira com fontes oficiais, busca rápida, conexões normativas verificáveis e monitoramento diário.

## Versão inicial

- Portal web estático e responsivo (compatível com GitHub Pages).
- Catálogo inicial de normas federais com links para textos oficiais.
- Pesquisa por assunto, número, ano, ementa e termos.
- Referências cruzadas **curadas** e identificadas como tais; nenhuma conclusão sobre vigência é produzida automaticamente.
- Coletor Python para verificar acessibilidade das fontes e descobrir novas referências de leis ordinárias de 2026 no índice oficial do Planalto.
- GitHub Actions: testes, coleta diária e publicação do portal.
- Dados públicos em `data/leis.json`, referências incrementais em `data/novidades.json` e log de acessibilidade em `data/coleta.json`.

## Como usar

Abra `index.html` localmente ou ative **Settings → Pages → Build and deployment → Source: GitHub Actions**. O workflow `pages.yml` também pode ser disparado manualmente.

## Desenvolvimento local

```bash
python -m http.server 8000
# http://localhost:8000
python -m unittest discover -s tests -v
python scripts/coletar.py
python scripts/descobrir_leis.py
```

## Limites jurídicos importantes

- Esta primeira versão é um **índice de referências**: para uso jurídico, confira o texto consolidado, alterações e a vigência na fonte oficial.
- O coletor confere páginas e descobre links de leis de 2026; **não** garante cobertura integral do Diário Oficial, nem valida ementa, publicação ou vigência.
- Conexões normativas somente entram no índice após inclusão explícita com fundamento verificável.
- Datas de conferência técnica não significam verificação jurídica da vigência.
- Não digite dados pessoais, sigilosos ou de clientes nesta versão pública e sem autenticação.

## Próximos marcos

1. Ampliar a descoberta incremental além das leis ordinárias de 2026, integrar publicações do DOU via fontes autorizadas e deduplicar por identificadores oficiais.
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

## Estado verificado em 14/10/2026

- O arquivo de descoberta automática continha **1.554 referências** de leis ordinárias federais de 2020 a 2026, com sete índices consultados e zero falhas reportadas naquela coleta.
- O portal exibe a busca por metadados, conexões curadas, gráfico e monitor de novas referências.
- Referências descobertas automaticamente ainda **não** contêm o texto integral de artigos, ementas validadas nem análise de vigência.
- A interface ainda é estática e pública: não há contas, dados privados de clientes, IA jurídica, cobrança, banco transacional ou auditoria profissional.
- O workflow de publicação depende da habilitação e permissões do GitHub Pages. Os testes de CI e o site ao vivo devem ser verificados na aba Actions após cada atualização.

## Critérios para o produto comercial

1. Ingestão integral e licenciada/autorizada de normas federais, estaduais e municipais, com identificação de fonte e versão.
2. Parser de artigos, parágrafos, incisos, alíneas e datas de vigência, com controle de erros e revisão.
3. Conexões automatizadas com evidência normativa, classificação de confiança e fluxo de validação.
4. Consulta histórica e auditoria reprodutível, incluindo alterações e revogações.
5. API autenticada, PostgreSQL, políticas de privacidade, controles LGPD, backup/recuperação e rate limits.
6. Assistente RAG com citação ao dispositivo, testes anti-alucinação e explicitação de incerteza.
7. Testes de integração, monitoramento operacional, termos de uso e conformidade comercial.

**Não confundir o MVP de referência legislativa com um sistema jurídico validado para orientar decisões profissionais sem conferir as fontes oficiais.**
