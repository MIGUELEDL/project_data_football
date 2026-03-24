FROM python:3.14-slim

# Copiar UV
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Dependências
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project

# Código
COPY . .

# Rodar app
CMD ["uv", "run", "python", "-m", "streamlit", "run", "app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
