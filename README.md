# ⚽ Project Data Football

Este é um projeto de Engenharia de Dados focado na construção de uma pipeline ponta a ponta (End-to-End) utilizando dados da API do Cartola FC. O objetivo principal é a aplicação da arquitetura Medallion e a conteinerização da entrega final.

O projeto coleta dados da API pública do **Cartola FC**, processa-os com **PySpark** e **Delta Lake**, organiza em um modelo dimensional e disponibiliza os resultados para consulta e visualização através do **Streamlit**.

---

## 🔄 Arquitetura do Pipeline

O pipeline segue o padrão **Medallion Architecture (Bronze → Silver → Gold)**.

                ┌──────────────────────────┐
                │     Cartola FC API       │
                │ api.cartola.globo.com    │
                └─────────────┬────────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │   Bronze Layer   │
                     │  Ingestão Raw    │
                     │                  │
                     │ - partidas       │
                     │ - pontuações     │
                     │ - mercado        │
                     │                  │
                     │ Delta Lake       │
                     └────────┬─────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │   Silver Layer   │
                     │ Transformação    │
                     │ e Modelagem      │
                     │                  │
                     │ Dimensões        │
                     │ +                │
                     │ Tabelas Fato     │
                     └────────┬─────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │    Gold Layer    │
                     │  Tabelas KPI     │
                     │                  │
                     │ Classificação    │
                     │ Estatísticas     │
                     │ KPIs             │
                     └────────┬─────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │     Streamlit    │
                     │ Visualização     │
                     │ das tabelas      │
                     │ analíticas       │
                     └─────────────────┘
    
### Bronze
Camada de ingestão de dados brutos da API.

- ingestão via API REST
- persistência em **Delta Lake**
- controle de duplicidade com **MERGE**
- ingestão incremental por rodada

### Silver
Camada responsável por tratamento e modelagem.

Principais objetos:

**Dimensões**
- `dim_atleta`
- `dim_campeonato`
- `dim_clube`
- `dim_estadio`
- `dim_posicao`
- `dim_rodada`'

**Fato**
- `fato_partida`
- `fato_pontuacao`

O projeto utiliza **modelagem dimensional**, com tabelas fato e dimensões para otimizar consultas analíticas.

                         dim_campeonato
                               │
                               │
                               ▼
                        ┌──────────────┐
                        │              │
            dim_rodada ─►              │
                        │              │
                        │              │
                        │  fato_partida│
                        │              │
           dim_estadio ─►              │
                        │              │
                        │              │
           dim_clube ───►              │
                        └──────────────┘


                         dim_posicao
                               │
                               │
                               ▼
                        ┌──────────────┐
                        │              │
           dim_atleta ──►              │
                        │              │
                        │ fato_pontuacao
                        │              │
           dim_rodada ──►              │
                        │              │
           dim_clube ───►              │
                        └──────────────┘

### Gold
Camada analítica utilizada para consumo de dados.

Exemplo de tabela:

`classificacao_brasileirao`

Contém métricas como:

- jogos
- vitórias
- empates
- derrotas
- gols pró
- gols contra
- saldo de gols
- pontos
- posição na tabela

---

## 🧰 Tecnologias Utilizadas

- Python
- PySpark
- SQL
- Docker
- Streamlit
- REST API

---

## 📥 Fonte de Dados

Os dados são coletados da API pública do Cartola FC:

https://api.cartola.globo.com/partidas

---

## ⚙️ Ambiente de Execução

O pipeline de dados deste projeto foi desenvolvido para execução em ambiente **Databricks**, utilizando notebooks PySpark organizados nas camadas da arquitetura Medallion (Bronze, Silver e Gold).

A aplicação **Streamlit** incluída no repositório é utilizada apenas para visualização simples das tabelas analíticas geradas na camada Gold.

Devido à dependência de infraestrutura específica (Databricks Workspace, Jobs e SQL Warehouse), a execução completa do pipeline não está incluída neste repositório.

---

## 📊 Visualização com Streamlit

O projeto inclui uma aplicação Streamlit utilizada apenas para visualizar as tabelas da camada Gold.

O objetivo não é construir dashboards complexos, mas facilitar a consulta dos resultados gerados pelo pipeline de dados.

## 📂 Estrutura do Projeto

├── 01.bronze/          # Notebooks de ingestão raw 
├── 02.silver/          # Notebooks de limpeza e modelagem 
├── 03.gold/            # Notebooks de KPIs e tabelas finais
├── app/                # Aplicação Streamlit (Visualização)
│   ├── main.py         # Interface do Dashboard
│   └── database.py     # Lógica de conexão com Databricks SQL
├── Dockerfile          # Definição da imagem da aplicação
├── docker-compose.yml  # Orquestração do ambiente local
└── pyproject.toml      # Gerenciamento de dependências via UV

---

## 👨‍💻 Autor

Miguel Ernandes Dias Lucena

Projeto desenvolvido para prática de conceitos de Engenharia de Dados, incluindo ingestão de APIs, processamento distribuído com Spark, modelagem dimensional e pipelines de dados.

<img width="1910" height="919" alt="Captura de tela 2026-03-03 041657" src="https://github.com/user-attachments/assets/9b9014c9-66f9-46a1-896a-f3e2a133d682" />

