# 📁 Pasta: app/authentication/

## O que vai aqui?

Sistema de **Autenticação** - Quem é você e se pode acessar.

## Arquivos Esperados

```
authentication/
├── __init__.py
├── views.py          # Views de login/refresh token
├── urls.py
├── serializers.py    # Serializers para login
└── HELP.md
```

## 🔑 Opções de Autenticação

Escolha **UMA** das opções:

### Opção 1️⃣: JWT (djangorestframework-simplejwt) - RECOMENDADO

**Instalar:**
```bash
pip install djangorestframework-simplejwt
```

**settings.py:**
```python
INSTALLED_APPS = [
    'rest_framework_simplejwt',
    # ... outros
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
}
```

**urls.py (Automático):**
```python
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
```

**Como usar:**
```bash
# 1. Obter tokens
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"seu_usuario","password":"sua_senha"}'

# Resposta:
# {
#   "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
#   "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
# }

# 2. Usar o token para requisições
curl http://localhost:8000/api/professionals/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."

# 3. Renovar token (antes de expirar)
curl -X POST http://localhost:8000/api/auth/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh":"seu_refresh_token"}'
```

### Opção 2️⃣: Token Auth (Simples)

**settings.py:**
```python
INSTALLED_APPS = [
    'rest_framework.authtoken',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}
```

**urls.py:**
```python
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path

urlpatterns = [
    path('token-auth/', obtain_auth_token, name='api_token_auth'),
]
```

## Protegendo Endpoints

### Permissões Globais (settings.py)

```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

### Permissões por ViewSet

```python
from rest_framework.permissions import IsAuthenticated

class ProfessionalViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
```

### Permissões Customizadas

```python
# Em permissions.py
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """Apenas proprietário pode editar"""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
```

## Checklist (Dia 3)

- [ ] JWT ou Token Auth configurado
- [ ] Endpoints de login/refresh funcionando
- [ ] Tokens sendo gerados corretamente
- [ ] Endpoints protegidos retornando 401 sem token
- [ ] Token funcionando em requisições autenticadas
- [ ] Refresh token renovando access token

## Teste Rápido

```python
# shell do Django
python manage.py shell

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# Criar usuário teste
user = User.objects.create_user(username='test', password='123456')
token = Token.objects.create(user=user)
print(f"Token: {token.key}")
```

---

**Próximo**: Vá para `tests/HELP.md`
