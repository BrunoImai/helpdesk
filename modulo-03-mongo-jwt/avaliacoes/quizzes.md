# Avaliações de múltipla escolha — Módulo 3 (gabarito)

## Aula 5 — Testes automáticos (pirâmide)
**Pergunta:** Na pirâmide de testes, qual camada deve ter a **maior quantidade** de testes e por quê?

- a) E2E, porque testam o sistema real
- **b) Unidade, porque são rápidos, baratos e isolados** <- correta
- c) Integração, porque cobrem tudo
- d) Todas igual, para equilibrar

*Explicação:* testes de unidade rodam em milissegundos e localizam o erro com precisão; E2E são lentos e frágeis,
por isso poucos.

**Pergunta extra:** Um teste envia `GET /tickets` sem token. Qual status a API deve devolver?

- a) 200
- b) 404
- **c) 401** <- correta
- d) 422

*Explicação:* 401 significa "não autenticado". O 422 é para dados inválidos e o 404 para recurso inexistente.
