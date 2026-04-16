import streamlit as st
import os
from database import query_gold_table 

st.set_page_config(page_title="Data Engineering - Cartola FC", layout="wide")

st.title("🏗️ Cartola FC: Data Engineering Pipeline")
st.markdown("""
Esta interface é o ponto final de um ecossistema de dados projetado para fornecer tabelas com dados do brasileirão.

### 🛠️ O Pipeline de Dados
O foco aqui é o **processo**, garantindo dados íntegros e performáticos:
* **Ingestão & Orquestração:** Extração automatizada da API e orquestração via **Databricks**.
* **Arquitetura Medallion:** Dados refinados através de camadas **Bronze, Silver e Gold**.
* **Resiliência:** Sistema com fallback automático para dados locais em caso de limite de cota.

---
#### 📊 Visualização das Tabelas (Gold Layer)
""")

# Criando as abas
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Classificação dos Clubes", 
    "Retrospectiva de Estádios", 
    "Estatísticas de Partidas", 
    "Pontuações do Cartola",
    "Retrospecto de Clubes"
])

# Dica: Criamos a pasta 'data' se ela não existir localmente para evitar erros de escrita
if not os.path.exists("data"):
    os.makedirs("data")

with tab1:
    st.header("Classificação dos Clubes")
    # Agora passamos a query E o caminho do arquivo de backup
    df_classificacao = query_gold_table(
        "SELECT * FROM classificacao_brasileirao", 
        "data/classificacao.parquet"
    )
    if not df_classificacao.empty:
        st.dataframe(df_classificacao, width="stretch")
    else:
        st.warning("Dados indisponíveis no momento (Banco e Local).")

with tab2:
    st.header("Retrospectiva de Estádios")
    df_estadios = query_gold_table(
        "SELECT * FROM kpi_estadios", 
        "data/estadios.parquet"
    )
    st.dataframe(df_estadios, width="stretch")

with tab3:
    st.header("Estatísticas de Partidas")
    df_partidas = query_gold_table(
        "SELECT * FROM kpi_partidas", 
        "data/partidas.parquet"
    )
    st.dataframe(df_partidas, width="stretch")

with tab4:
    st.header("Estatísticas de Pontuações do Cartola")
    df_pontuacoes = query_gold_table(
        "SELECT * FROM kpi_pontuacoes_cartola", 
        "data/pontuacoes.parquet"
    )
    st.dataframe(df_pontuacoes, width="stretch")

with tab5:
    st.header("Retrospecto de Clubes")
    df_clubes = query_gold_table(
        "SELECT * FROM stats_clubes", 
        "data/stats_clubes.parquet"
    )
    st.dataframe(df_clubes, width="stretch")

# Rodapé informativo
st.info("💡 Se as tabelas estiverem desatualizadas, é possível que o app esteja operando em modo offline devido a limites de cota da infraestrutura gratuita.")
