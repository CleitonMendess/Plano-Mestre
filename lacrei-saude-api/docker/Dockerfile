FROM python:3.11-slim

WORKDIR /app

# Instale dependências do sistema
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copie requirements
COPY pyproject.toml poetry.lock* ./

# Instale Poetry e dependências
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

# Copie código da aplicação
COPY . .

# Crie diretório de arquivos estáticos
RUN mkdir -p /app/staticfiles

# Exponha porta
EXPOSE 8000

# Defina variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Permissão para entrypoint
RUN chmod +x docker/entrypoint.sh

# Run
ENTRYPOINT ["/app/docker/entrypoint.sh"]
