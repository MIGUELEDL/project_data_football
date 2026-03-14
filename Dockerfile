# Estágio de build para pegar o binário do uv
FROM python:3.11-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências primeiro (aproveita o cache do Docker)
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project

# Copiar o restante do código
COPY . .

# Expor a porta do Streamlit
EXPOSE 8501

# Comando para rodar a aplicação usando o ambiente do uv
CMD ["uv", "run", "streamlit", "run", "app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]