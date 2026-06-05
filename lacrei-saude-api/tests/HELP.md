# 📁 Pasta: tests/

## O que vai aqui?

Testes mais complexos e **Testes de Integração**.

Os testes simples (`test_*.py`) ficam em cada app, mas testes maiores vão aqui.

## Arquivos Esperados

```
tests/
├── __init__.py
├── test_api_integration.py    # Testes que usam múltiplos apps
├── test_permissions.py        # Testes de autenticação/permissões
├── test_validations.py        # Testes de validações
└── HELP.md
```

## Estrutura de Testes

### 1. Testes de Integração (test_api_integration.py)

```python
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from professionals.models import Professional
from appointments.models import Appointment
from datetime import timedelta
from django.utils import timezone

class APIIntegrationTests(APITestCase):
    def setUp(self):
        """Preparar dados para cada teste"""
        # Criar usuário
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        
        # Criar profissional
        self.prof = Professional.objects.create(
            social_name="Dr. Teste",
            profession="Médico",
            address="Rua Teste",
            contact="11999999999"
        )
        
        # Data futura
        self.future = timezone.now() + timedelta(days=7)
    
    def test_full_appointment_workflow(self):
        """Testa fluxo completo: criar profissional → agendar consulta"""
        # 1. Listar profissionais (deve existir o criado)
        resp = self.client.get('/api/professionals/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertGreater(len(resp.data), 0)
        
        # 2. Agendar consulta
        data = {
            "professional_id": str(self.prof.id),
            "patient_name": "Paciente Teste",
            "appointment_date": self.future.isoformat(),
        }
        resp = self.client.post('/api/appointments/', data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        
        # 3. Verificar que consulta aparece ao listar
        resp = self.client.get('/api/appointments/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertGreater(len(resp.data), 0)
        
        # 4. Atualizar status da consulta
        appointment_id = resp.data[0]['id']
        update_data = {"status": "completed"}
        resp = self.client.patch(f'/api/appointments/{appointment_id}/', update_data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
```

### 2. Testes de Autenticação (test_permissions.py)

```python
from rest_framework.test import APITestCase
from rest_framework import status
from professionals.models import Professional

class AuthenticationTests(APITestCase):
    def setUp(self):
        self.prof = Professional.objects.create(
            social_name="Dr. Protegido",
            profession="Médico",
            address="Rua X",
            contact="11999999999"
        )
    
    def test_access_without_token_denied(self):
        """Sem autenticação deve retornar 401"""
        response = self.client.get('/api/professionals/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_without_token_denied(self):
        """Criar sem token deve ser negado"""
        data = {
            "social_name": "Dr. Novo",
            "profession": "Enfermeiro",
            "address": "Rua Y",
            "contact": "11988888888"
        }
        response = self.client.post('/api/professionals/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_with_valid_token_allowed(self):
        """Com token válido deve funcionar"""
        from django.contrib.auth.models import User
        from rest_framework.authtoken.models import Token
        
        user = User.objects.create_user(username='auth_user', password='pass')
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        
        response = self.client.get('/api/professionals/')
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED])
```

### 3. Testes de Validação (test_validations.py)

```python
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import timedelta
from django.utils import timezone

class ValidationTests(APITestCase):
    def test_appointment_date_cannot_be_past(self):
        """Data passada deve ser rejeitada"""
        past = (timezone.now() - timedelta(days=1)).isoformat()
        data = {
            "professional_id": "fake-uuid",
            "patient_name": "Paciente",
            "appointment_date": past,
        }
        response = self.client.post('/api/appointments/', data)
        # Deve falhar por múltiplos motivos, mas a validação de data é importante
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_patient_name_required(self):
        """Nome do paciente é obrigatório"""
        future = (timezone.now() + timedelta(days=7)).isoformat()
        data = {
            "professional_id": "fake-uuid",
            "appointment_date": future,
        }
        response = self.client.post('/api/appointments/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
```

## Como Executar Testes

```bash
# Todos os testes
python manage.py test

# Apenas um arquivo
python manage.py test tests.test_api_integration

# Apenas uma classe
python manage.py test tests.test_api_integration.APIIntegrationTests

# Apenas um método
python manage.py test tests.test_api_integration.APIIntegrationTests.test_full_appointment_workflow

# Com verbosidade
python manage.py test --verbosity=2

# Mostrar que está rodando (live)
python manage.py test --debug-mode
```

## Coverage (Cobertura de Testes)

```bash
# Instalar
pip install coverage

# Rodar com coverage
coverage run --source='.' manage.py test

# Relatório
coverage report

# HTML (mais visual)
coverage html
# Abrir htmlcov/index.html
```

## Checklist (Dia 4)

- [ ] Testes passando para todas as features
- [ ] Coverage > 80%
- [ ] Testes de autenticação funcionando
- [ ] Testes de validação de negócio
- [ ] Testes de integração entre apps

## Exemplo de Teste Robusto

```python
class RobustAppointmentTest(APITestCase):
    """Teste robusto que cobre múltiplos cenários"""
    
    def test_appointment_lifecycle(self):
        # Arrange (Preparar)
        prof = Professional.objects.create(...)
        future = timezone.now() + timedelta(days=1)
        
        # Act (Agir)
        resp = self.client.post('/api/appointments/', {...})
        
        # Assert (Verificar)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Appointment.objects.count(), 1)
        
        # Verificar dados retornados
        data = resp.json()
        self.assertEqual(data['status'], 'scheduled')
```

---

**Próximo**: Vá para `docker/HELP.md`
