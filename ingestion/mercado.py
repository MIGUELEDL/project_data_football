import requests
import json
import os
from datetime import datetime
from minio import Minio

# Configuração do cliente MinIO
client = Minio(
    os.getenv("S3_ENDPOINT").replace("http://", ""),
    access_key=os.getenv("S3_ACCESS_KEY"),
    secret_key=os.getenv("S3_SECRET_KEY"),
    secure=False
)

bucket = os.getenv("S3_BUCKET")

# Cria o bucket se não existir
def create_bucket():
    if not client.bucket_exists(bucket):
        client.make_bucket(bucket)

# Salva dados JSON localmente e faz upload para o MinIO
def upload_json(data, path):
    file_name = f"/tmp/{datetime.now().timestamp()}.json"

    with open(file_name, "w") as f:
        json.dump(data, f)

    client.fput_object(bucket, path, file_name)

# Executa a ingestão das partidas
def run():
    print("Iniciando ingestão de partidas...")

    status = requests.get("https://api.cartola.globo.com/mercado/status").json()
    rodada_atual = status["rodada_atual"]

    for rodada in range(1, rodada_atual + 1):
        print(f"Rodada {rodada}")

        url = "https://api.cartola.globo.com/atletas/mercado"
        data = requests.get(url).json()

        path = "mercado/data.json"
        upload_json(data, path)

    print("Partidas finalizadas!")

if __name__ == "__main__":
    create_bucket()
    run()