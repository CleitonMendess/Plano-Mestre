# Lacrei Saúde API

API RESTful para gerenciamento de consultas médicas. Este é um projeto de 5 dias com Django.

## Estrutura do Projeto

```
lacrei-saude-api/
├── app/                      # Aplicação Django
│   ├── core/                # Configurações globais (settings, urls, wsgi)
│   ├── professionals/       # App: Profissionais de Saúde
│   ├── appointments/        # App: Consultas/Agendamentos
│   └── authentication/      # App: Autenticação (JWT/Tokens)
├── docker/                  # Containerização
├── docs/                    # Documentação
├── tests/                   # Testes
├── .github/workflows/       # CI/CD
├── pyproject.toml          # Dependências (Poetry)
├── docker-compose.yml      # Orquestração de containers
└── manage.py               # CLI do Django
```

## ⏱️ Cronograma (5 dias)

- **Dia 1-2**: Setup, Modelos de BD, Serializers
- **Dia 2-3**: Views/Viewsets, URLs, Autenticação
- **Dia 3-4**: Testes, Validações, Segurança
- **Dia 4-5**: Docker, Deploy local, Refinamento
