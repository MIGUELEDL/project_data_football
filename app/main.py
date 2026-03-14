import streamlit as st
import plotly.express as px
from database import query_gold_table # Função que criamos

st.set_page_config(page_title="Data Engineering - Cartola FC", layout="wide")

st.title("🏗️ Cartola FC: Data Engineering Pipeline")
st.markdown("""
Esta interface é o ponto final de um ecossistema de dados projetado para fornecer tabelas com dados do brasileirão, 
preparadas para análises avançadas e modelos de Machine Learning.

### 🛠️ O Pipeline de Dados
O foco aqui é o **processo**, garantindo dados íntegros e performáticos:

* **Ingestão & Orquestração:** Extração automatizada da API e orquestração via **Databricks**.
* **Arquitetura Medallion:** Dados refinados através de camadas **Bronze, Silver e Gold** com **PySpark** e **SQL**.
* **Portabilidade:** Infraestrutura 100% conteinerizada com **Docker**.

---
#### 📊 Visualização das Tabelas (Gold Layer)
*Abaixo, você pode explorar as tabelas resultantes do processo ETL, prontas para o time de Analytics.*
""")

# Criando abas para organizar as visões dos seus notebooks
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Classificação dos Clubes", 
    "Retropesctivas de Estádios", 
    "Estatisticas de partidas", 
    "Estatisticas de pontuações do Cartola",
    "Retrospecto de Clubes"
])

with tab1:
    st.header("Classificação dos Clubes")
    # Nome da tabela
    df_classificacao = query_gold_table("SELECT * FROM classificacao_brasileirao")
    st.table(df_classificacao)

with tab2:
    st.header("Retropesctivas de Estádios")
    df_estadios = query_gold_table("SELECT * FROM kpi_estadios")
    st.dataframe(df_estadios)

with tab3:
    st.header("Estatisticas de partidas")
    df_partidas = query_gold_table("SELECT * FROM kpi_partidas")
    st.dataframe(df_partidas)

with tab4:
    st.header("Estatisticas de pontuações do Cartola")
    df_jogadores_pontuacoes = query_gold_table("SELECT * FROM kpi_pontuacoes_cartola")
    st.dataframe(df_jogadores_pontuacoes)

with tab5:
    st.header("Retrospecto de Clubes")
    df_clubes = query_gold_table("SELECT * FROM stats_clubes")
    st.dataframe(df_clubes)
