import os
from databricks import sql
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

# função para fazer chamada das tabelas com uma query sql (SELECT * FROM table) e transformar e um dataframe no pandas
def query_gold_table(query_sql):
    """Executa queries SQL garantindo o contexto de Catalog e Schema"""
    
    # variaveis .env
    catalog = os.getenv("CATALOG_NAME")
    schema = os.getenv("GOLD_SCHEMA")
    
    try:
        connection = sql.connect(
            server_hostname=os.getenv("DATABRICKS_SERVER_HOSTNAME"),
            http_path=os.getenv("DATABRICKS_HTTP_PATH"),
            access_token=os.getenv("DATABRICKS_TOKEN")
        )
        
        with connection.cursor() as cursor:
            # 1. Seta o contexto inicial para não precisar repetir no SELECT
            cursor.execute(f"USE CATALOG {catalog}")
            cursor.execute(f"USE SCHEMA {schema}")
            
            # 2. Executa a sua query (ex: "SELECT * FROM gold_kpi_partidas")
            cursor.execute(query_sql)
            
            result = cursor.fetchall()
            column_names = [column[0] for column in cursor.description]
            return pd.DataFrame(result, columns=column_names)
            
    except Exception as e:
        print(f"❌ Erro na conexão/query: {e}")
        return pd.DataFrame()
    finally:
        connection.close()