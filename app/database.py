import os
import streamlit as st
from databricks import sql
import pandas as pd
from dotenv import load_dotenv

# Carrega as variáveis de ambiente definidas no arquivo .env (segurança e portabilidade)
load_dotenv()

def _get_secret(key):
    """Pega de st.secrets (Streamlit Cloud) ou .env (local)."""
    try:
        return st.secrets[key]
    except (KeyError, FileNotFoundError):
        return os.getenv(key)

def query_gold_table(query_sql, local_file_path):
    """
    Tenta buscar dados no Databricks. 
    Se falhar, busca em um arquivo local (fallback).
    """
    catalog = _get_secret("CATALOG_NAME")
    schema = _get_secret("GOLD_SCHEMA")
    connection = None
    
    try:
        # Tenta a conexão oficial
        connection = sql.connect(
            server_hostname=os.getenv("DATABRICKS_SERVER_HOSTNAME"),
            http_path=os.getenv("DATABRICKS_HTTP_PATH"),
            access_token=os.getenv("DATABRICKS_TOKEN")
        )
        
        with connection.cursor() as cursor:
            cursor.execute(f"USE CATALOG {catalog}")
            cursor.execute(f"USE SCHEMA {schema}")
            cursor.execute(query_sql)
            
            result = cursor.fetchall()
            column_names = [column[0] for column in cursor.description]
            df = pd.DataFrame(result, columns=column_names)
            
            # Se trouxer dados, salva uma cópia local para atualizar o fallback
            if not df.empty:
                df.to_parquet(local_file_path, index=False)
            return df
            
    except Exception as e:
        print(f"Databricks Offline/Cota excedida. Carregando fallback: {e}")
        try:
            # Se o banco falhar, lê o arquivo que está na pasta do projeto
            return pd.read_parquet(local_file_path)
        except:
            # Se nem o arquivo existir, retorna vazio
            return pd.DataFrame()
            
    finally:
        if connection is not None:
            connection.close()
