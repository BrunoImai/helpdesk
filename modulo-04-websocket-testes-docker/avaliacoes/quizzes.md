# Avaliações de múltipla escolha — Módulo 4 (gabarito)

## Aula 2 — Testes automatizados (pirâmide)
**Pergunta:** Na pirâmide de testes, qual camada deve ter a **maior quantidade** de testes e por quê?

- a) E2E, porque testam o sistema real
- **b) Unidade, porque são rápidos, baratos e isolados** <- correta
- c) Integração, porque cobrem tudo
- d) Todas igual, para equilibrar

*Explicação:* testes de unidade rodam em milissegundos e localizam o erro com precisão; E2E são lentos e frágeis,
por isso poucos.

## Aula 4 — Docker
**Pergunta:** Qual a diferença entre o `Dockerfile` e o `docker-compose.yml`?

- a) São sinônimos
- **b) O Dockerfile constrói UMA imagem; o Compose orquestra VÁRIOS serviços (ex.: API + MongoDB) juntos** <- correta
- c) O Dockerfile só serve para bancos de dados
- d) O Compose substitui a necessidade de imagens

*Explicação:* o Compose normalmente **usa** o Dockerfile (`build: .`) e adiciona rede, volumes, variáveis e
dependências entre serviços.
