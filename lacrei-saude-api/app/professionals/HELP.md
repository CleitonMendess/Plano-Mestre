# 📁 Pasta: app/professionals/

## O que vai aqui?

Tudo relacionado a **Profissionais de Saúde**. Um "sub-projeto" completo.

## Arquivos Esperados

```
professionals/
├── __init__.py
├── migrations/        # Histórico de mudanças no BD
├── admin.py          # Interface admin do Django
├── apps.py           # Configuração do app
├── models.py         # Tabela: Professional
├── serializers.py    # Converte Professional → JSON
├── views.py          # Lógica das requisições
├── urls.py           # Rotas do app
├── tests.py          # Testes unitários
└── HELP.md           # Este arquivo
```

## Passo a Passo (Dia 1-2)

### 1. models.py - Define a Tabela

```python
from django.db import models
import uuid

class Professional(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    social_name = models.CharField(max_length=255, help_text="Nome social do profissional")
    profession = models.CharField(max_length=255, help_text="Ex: Médico, Enfermeiro")
    address = models.TextField(help_text="Endereço completo")
    contact = models.CharField(max_length=20, help_text="Telefone/WhatsApp")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Professional"
        verbose_name_plural = "Professionals"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.social_name} - {self.profession}"
```

### 2. serializers.py - Converte para JSON

```python
from rest_framework import serializers
from .models import Professional

class ProfessionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professional
        fields = ['id', 'social_name', 'profession', 'address', 'contact', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
```

### 3. views.py - A Lógica

```python
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Professional
from .serializers import ProfessionalSerializer

class ProfessionalViewSet(viewsets.ModelViewSet):
    """
    API para gerenciar Profissionais de Saúde
    - GET /api/professionals/ - Listar todos
    - POST /api/professionals/ - Criar novo
    - GET /api/professionals/{id}/ - Detalhe
    - PUT/PATCH /api/professionals/{id}/ - Atualizar
    - DELETE /api/professionals/{id}/ - Deletar
    """
    queryset = Professional.objects.all()
    serializer_class = ProfessionalSerializer
    
    def perform_create(self, serializer):
        """Chamado ao criar um profissional"""
        serializer.save()
```

### 4. urls.py - Rotas do App

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfessionalViewSet

app_name = 'professionals'

router = DefaultRouter()
router.register(r'professionals', ProfessionalViewSet, basename='professional')

urlpatterns = [
    path('', include(router.urls)),
]
```

### 5. admin.py - Interface Admin

```python
from django.contrib import admin
from .models import Professional

@admin.register(Professional)
class ProfessionalAdmin(admin.ModelAdmin):
    list_display = ['social_name', 'profession', 'created_at']
    search_fields = ['social_name', 'profession']
    list_filter = ['profession', 'created_at']
    ordering = ['-created_at']
```

## Executar Migrações

```bash
# Cria arquivo de migração
python manage.py makemigrations professionals

# Aplica ao banco
python manage.py migrate

# Cria super usuário para admin
python manage.py createsuperuser
```

## Testar a API

```bash
# Listar profissionais
curl http://localhost:8000/api/professionals/

# Criar um novo
curl -X POST http://localhost:8000/api/professionals/ \
  -H "Content-Type: application/json" \
  -d '{
    "social_name": "Dra. Maria Silva",
    "profession": "Cardiologista",
    "address": "Rua das Flores, 123, São Paulo",
    "contact": "11998765432"
  }'
```

## Testes (tests.py)

```python
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Professional

class ProfessionalTests(APITestCase):
    def setUp(self):
        self.professional = Professional.objects.create(
            social_name="Dr. João",
            profession="Médico",
            address="Rua X",
            contact="11999999999"
        )
    
    def test_list_professionals(self):
        response = self.client.get('/api/professionals/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_professional(self):
        data = {
            "social_name": "Dra. Ana",
            "profession": "Enfermeira",
            "address": "Rua Y",
            "contact": "11988888888"
        }
        response = self.client.post('/api/professionals/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
```

## Checklist (Dia 2)

- [ ] Model criado e testado
- [ ] Serializer validando dados
- [ ] ViewSet com CRUD completo
- [ ] URLs mapeadas
- [ ] Admin funcionando
- [ ] Testes passando
- [ ] Paginação configurada (se necessário)

## Validações Importantes

```python
# Em models.py
from django.core.validators import MinLengthValidator

class Professional(models.Model):
    social_name = models.CharField(
        max_length=255,
        validators=[MinLengthValidator(3)],
        help_text="Mínimo 3 caracteres"
    )
    contact = models.CharField(
        max_length=20,
        validators=[RegexValidator(r'^\+?[0-9\-\s\(\)]+$')]
    )
```

---

**Próximo**: Vá para `app/appointments/HELP.md`
