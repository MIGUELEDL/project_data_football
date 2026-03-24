FROM python:3.11-slim

WORKDIR /app

# instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 👇 COPIA SÓ O REQUIREMENTS PRIMEIRO
COPY ingestion/requirements.txt .

# 👇 INSTALA DEPENDÊNCIAS
RUN pip install --no-cache-dir -r requirements.txt

# 👇 AGORA copia o resto do código
COPY ingestion/ .

# comando padrão
CMD ["python", "main.py"]