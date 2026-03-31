# Data Pipeline Macroeconômico

![Arquitetura do Projeto](./img/Arquitetura_projeto.png)

Pipeline de dados end-to-end para ingestão, transformação e disponibilização de dados macroeconômicos, com foco na análise da relação entre liquidez de oferta monetária global e o preço do Bitcoin.

## Problema de Negócio

Este projeto nasceu de uma dúvida:
existe, de fato, uma relação entre a macroeconomia e o preço do Bitcoin?

Em vez de aceitar respostas prontas de sites, decidi aplicar na prática um dos princípios mais conhecidos do próprio Bitcoin:
**“Don't trust, verify.”**

A proposta, então, foi clara:
construir um pipeline de dados capaz de coletar, tratar e integrar informações macroeconômicas relevantes — como liquidez global (M2) e câmbio — para investigar, com dados reais, possíveis correlações com o comportamento do Bitcoin.

Mais do que responder uma pergunta, este projeto busca transformar curiosidade em uma arquitetura estruturada, reprodutível e orientada a dados.

## Arquitetura

![Arquitetura airflow](./img/Pipeline_financeira-graph.png)

-> Layers
- Bronze
- Silver
- Gold

-> Armazenamento
- Arquivos interno do container como **Data lake**
- PostgreSQL com **Data warehouse**

-> Orquestração
- Apache Airflow

-> Infraestrutura
- Docker

## Experiência e dificuldades

Aqui vou relatar alguns pontos de aprendizado que tive como primeiro projeto:

- 