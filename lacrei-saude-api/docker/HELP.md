# 📁 Pasta: docker/

## O que vai aqui?

Configuração para **containerizar** sua app (rodar em containers Docker).

## Arquivos Esperados

```
docker/
├── Dockerfile         # Receita para construir imagem
├── entrypoint.sh     # Script que roda quando container inicia
└── HELP.md
```

## Dockerfile

```dockerfile
# Use imagem Python oficial
FROM python:3.11-slim

# Defina diretório de trabalho
WORKDIR /app

# Copie requirements
COPY pyproject.toml ./
COPY poetry.lock ./

# Instale Poetry e dependências
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

# Copie código
COPY . .

# Exponha porta
EXPOSE 8000

# Comando padrão
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

## entrypoint.sh

```bash
#!/bin/bash
set -e

echo "Executando migrações..."
python manage.py migrate

echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

echo "Iniciando servidor..."
python manage.py runserver 0.0.0.0:8000
```

## docker-compose.yml (na raiz do projeto)

```yaml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: lacrei_saude
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: senha_super_segura
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  api:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    environment:
      - DEBUG=True
      - DB_ENGINE=django.db.backends.postgresql
      - DB_NAME=lacrei_saude
      - DB_USER=postgres
      - DB_PASSWORD=senha_super_segura
      - DB_HOST=db
      - DB_PORT=5432
    depends_on:
      - db

volumes:
  postgres_data:
```

## Como Usar

```bash
# Construir imagem
docker build -t lacrei-saude-api .

# Rodar container
docker run -p 8000:8000 lacrei-saude-api

# Com Docker Compose (RECOMENDADO)
docker-compose up

# Em background
docker-compose up -d

# Ver logs
docker-compose logs -f api

# Parar
docker-compose down
```

## Comandos Úteis

```bash
# Executar comando dentro do container
docker-compose exec api python manage.py createsuperuser

# Acessar shell do container
docker-compose exec api bash

# Reconstruir imagem (após mudanças)
docker-compose build

# Limpar tudo (cuidado!)
docker-compose down -v
```

## Checklist (Dia 5)

- [ ] Dockerfile criado
- [ ] docker-compose.yml configurado
- [ ] Imagem buildando sem erros
- [ ] Container rodando localmente
- [ ] BD inicializando corretamente
- [ ] API acessível em http://localhost:8000

---

**Próximo**: Vá para `docs/HELP.md` para documentação
