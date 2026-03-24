import requests
import json
from datetime import datetime
import os
from s3_client import get_s3

s3 = get_s3()
bucket = os.getenv("S3_BUCKET")

def upload_json(data, path):
    s3.put_object(
        Bucket=bucket,
        Key=path,
        Body=json.dumps(data),
        ContentType="application/json"
    )

def run():
    print("Iniciando ingestão de mercado...")

    url = "https://api.cartola.globo.com/atletas/mercado"
    data = requests.get(url).json()

    rodada = data.get("rodada_atual")

    path = f"raw/mercado/rodada={rodada}/data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    upload_json(data, path)