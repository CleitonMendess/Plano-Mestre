# 📁 Pasta: .github/workflows/

## O que vai aqui?

Pipelines de **CI/CD** (Continuous Integration / Continuous Deployment).

## Arquivo Esperado

```
.github/workflows/
├── ci-cd.yml         # Pipeline principal
└── HELP.md
```

## ci-cd.yml - Pipeline no GitHub Actions

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15-alpine
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
    - uses: actions/checkout@v3
    
    - name: Instalar Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Instalar Poetry
      run: |
        curl -sSL https://install.python-poetry.org | python3 -
        export PATH="$HOME/.local/bin:$PATH"
    
    - name: Cache dependências
      uses: actions/cache@v3
      with:
        path: ~/.cache/pypoetry
        key: ${{ runner.os }}-poetry-${{ hashFiles('**/poetry.lock') }}
    
    - name: Instalar dependências
      run: poetry install
    
    - name: Rodas testes
      env:
        DB_HOST: localhost
        DB_USER: postgres
        DB_PASSWORD: postgres
      run: poetry run python manage.py test
    
    - name: Lint (flake8)
      run: poetry run flake8 app --max-line-length=100
    
    - name: Type check (mypy)
      run: poetry run mypy app
      continue-on-error: true

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy para AWS (exemplo)
      run: |
        echo "Deploying to AWS..."
        # Seus comandos de deploy aqui
```

## Como Usar

1. Crie a pasta `.github/workflows/` na raiz do projeto
2. Adicione `ci-cd.yml`
3. Faça push para GitHub
4. Vá em "Actions" para ver os pipelines rodando

## Checklist (Dia 5)

- [ ] Arquivo ci-cd.yml criado
- [ ] Pipeline rodando com sucesso no GitHub
- [ ] Testes passando automaticamente
- [ ] Build funcionando

---

Próximo: Vá para os demais arquivos de documentação!
