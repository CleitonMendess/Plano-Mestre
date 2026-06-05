# 📁 Pasta: app/core/

## O que vai aqui?

Configurações **globais** do Django. É como o "coração" da aplicação.

## Arquivos Esperados

```
core/
├── __init__.py        # Marca como pacote
├── settings.py        # Configurações gerais do Django
├── urls.py           # URLs globais (rotas principais)
├── wsgi.py           # Para produção (AWS, etc)
├── asgi.py           # Para WebSockets (opcional)
└── HELP.md           # Este arquivo
```

## O que colocar aqui

### 1. settings.py
Aqui você define:
- Banco de dados (PostgreSQL)
- Apps instalados (professionals, appointments, etc)
- Autenticação
- CORS
- Variáveis de ambiente
- Logging

**Exemplo básico:**
```python
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = 'sua-chave-super-secreta-aqui'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'rest_framework',
    'professionals',
    'appointments',
    'authentication',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'lacrei_saude',
        'USER': 'postgres',
        'PASSWORD': 'senha',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 2. urls.py
Mapeia as rotas principais:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
    path('api/', include('professionals.urls')),
    path('api/', include('appointments.urls')),
]
```

## Tarefas para o Dia 1

- [ ] Criar `settings.py` com configuração PostgreSQL
- [ ] Criar `urls.py` com rotas principais
- [ ] Configurar CORS
- [ ] Configurar autenticação JWT
- [ ] Testar se `python manage.py runserver` funciona

## Variáveis de Ambiente (Importante!)

Use `.env` para não exposer senhas:

```bash
# .env
DEBUG=True
SECRET_KEY=sua-chave-secreta
DB_NAME=lacrei_saude
DB_USER=postgres
DB_PASSWORD=sua-senha
DB_HOST=localhost
DB_PORT=5432
```

Depois carregue em `settings.py`:
```python
from decouple import config
DEBUG = config('DEBUG', cast=bool)
SECRET_KEY = config('SECRET_KEY')
```

## Checklist de Segurança

- [ ] `DEBUG = False` em produção
- [ ] `SECRET_KEY` em variável de ambiente
- [ ] CORS configurado corretamente (não use '*')
- [ ] Autenticação obrigatória em endpoints sensíveis
- [ ] HTTPS em produção

---

**Próximo**: Vá para `app/professionals/HELP.md`
