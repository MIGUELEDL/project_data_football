import os
from databricks import sql
import pandas as pd
from dotenv import load_dotenv

# Carrega as variáveis de ambiente definidas no arquivo .env (segurança e portabilidade)
load_dotenv()

def query_gold_table(query_sql):
    """
    Função para consumir dados da camada Gold no Databricks.
    Retorna um DataFrame Pandas pronto para visualização.
    """
    
    # Recupera os nomes do Catálogo e Schema (Medallion Architecture) do ambiente
    catalog = os.getenv("CATALOG_NAME")
    schema = os.getenv("GOLD_SCHEMA")
    
    # Inicializa a conexão como None para evitar o UnboundLocalError no finally
    connection = None
    
    try:
        # Estabelece a conexão com o SQL Warehouse do Databricks
        connection = sql.connect(
            server_hostname=os.getenv("DATABRICKS_SERVER_HOSTNAME"),
            http_path=os.getenv("DATABRICKS_HTTP_PATH"),
            access_token=os.getenv("DATABRICKS_TOKEN")
        )
        
        # O 'with' garante que o cursor seja fechado automaticamente após o uso
        with connection.cursor() as cursor:
            # Seta o contexto do Unity Catalog para evitar nomes longos (catalog.schema.tabela)
            cursor.execute(f"USE CATALOG {catalog}")
            cursor.execute(f"USE SCHEMA {schema}")
            
            # Executa a consulta SQL enviada como argumento
            cursor.execute(query_sql)
            
            # Recupera todos os registros da consulta
            result = cursor.fetchall()
            
            # Extrai o nome das colunas a partir dos metadados do cursor
            column_names = [column[0] for column in cursor.description]
            
            # Converte os dados brutos em um DataFrame do Pandas para facilitar a análise/plotagem
            return pd.DataFrame(result, columns=column_names)
            
    except Exception as e:
        # Em vez de apenas printar no console, vamos subir o erro para o Streamlit
        import streamlit as st
        st.error(f"Erro detalhado: {e}") 
        return pd.DataFrame()
        
    finally:
        # Encerra a conexão com o servidor, liberando recursos no Databricks
        if connection is not None:
            connection.close()