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
    print("Iniciando ingestão de pontuação...")

    status = requests.get("https://api.cartola.globo.com/mercado/status").json()
    rodada_atual = status["rodada_atual"]

    for rodada in range(1, rodada_atual + 1):

        url = f"https://api.cartola.globo.com/atletas/pontuados/{rodada}"
        data = requests.get(url).json()

        atletas = data.get("atletas", {})

        if not atletas:
            print(f"Rodada {rodada} sem pontuação disponível")
            continue

        print(f"Rodada {rodada} com dados ✅")

        path = f"raw/pontuacao/rodada={rodada}/data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        upload_json(data, path)