# 📁 Pasta: app/appointments/

## O que vai aqui?

Tudo sobre **Consultas/Agendamentos**. Vinculadas aos Profissionais.

## Arquivos Esperados

```
appointments/
├── __init__.py
├── migrations/
├── admin.py
├── apps.py
├── models.py         # Tabela: Appointment
├── serializers.py
├── views.py
├── urls.py
├── tests.py
└── HELP.md           # Este arquivo
```

## Passo a Passo (Dia 2-3)

### 1. models.py - Define a Tabela com Relacionamento

⚠️ **IMPORTANTE**: Appointments tem Chave Estrangeira para Professional

```python
from django.db import models
from django.contrib.postgres.fields import ArrayField
import uuid

class AppointmentStatusChoices(models.TextChoices):
    SCHEDULED = "scheduled", "Agendada"
    COMPLETED = "completed", "Concluída"
    CANCELLED = "cancelled", "Cancelada"
    NO_SHOW = "no_show", "Faltou"

class Appointment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # FK para Professional
    professional = models.ForeignKey(
        'professionals.Professional',
        on_delete=models.CASCADE,
        related_name='appointments',
        help_text="Profissional responsável"
    )
    
    appointment_date = models.DateTimeField(help_text="Data e hora da consulta")
    patient_name = models.CharField(max_length=255, help_text="Nome do paciente")
    status = models.CharField(
        max_length=20,
        choices=AppointmentStatusChoices.choices,
        default=AppointmentStatusChoices.SCHEDULED
    )
    
    notes = models.TextField(blank=True, null=True, help_text="Observações")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Appointment"
        verbose_name_plural = "Appointments"
        ordering = ['appointment_date']
        # Evita agendamentos duplicados na mesma data
        unique_together = ('professional', 'appointment_date')
    
    def __str__(self):
        return f"Consulta - {self.patient_name} com {self.professional.social_name}"
```

### 2. serializers.py - Converte para JSON

```python
from rest_framework import serializers
from .models import Appointment, AppointmentStatusChoices
from professionals.serializers import ProfessionalSerializer

class AppointmentSerializer(serializers.ModelSerializer):
    # Inclui dados do profissional na resposta
    professional = ProfessionalSerializer(read_only=True)
    professional_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = Appointment
        fields = [
            'id',
            'professional',
            'professional_id',
            'appointment_date',
            'patient_name',
            'status',
            'notes',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_appointment_date(self, value):
        """Garante que data está no futuro"""
        from django.utils import timezone
        if value < timezone.now():
            raise serializers.ValidationError("Data não pode ser no passado")
        return value
    
    def validate_patient_name(self, value):
        """Garante nome não vazio"""
        if not value or len(value.strip()) < 3:
            raise serializers.ValidationError("Nome deve ter pelo menos 3 caracteres")
        return value
```

### 3. views.py - Lógica com Filtros

```python
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Appointment
from .serializers import AppointmentSerializer

class AppointmentViewSet(viewsets.ModelViewSet):
    """
    API para gerenciar Consultas
    - GET /api/appointments/ - Listar todas
    - POST /api/appointments/ - Agendar nova
    - GET /api/appointments/{id}/ - Detalhe
    - PUT/PATCH /api/appointments/{id}/ - Atualizar status
    - DELETE /api/appointments/{id}/ - Cancelar
    - GET /api/appointments/by-professional/{professional_id}/ - Listar por profissional
    """
    
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['patient_name', 'professional__social_name']
    ordering = ['appointment_date']
    
    @action(detail=False, methods=['get'])
    def by_professional(self, request, professional_id=None):
        """Retorna consultas de um profissional específico"""
        appointments = self.queryset.filter(
            professional_id=professional_id
        ).order_by('appointment_date')
        serializer = self.get_serializer(appointments, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Retorna apenas consultas futuras"""
        now = timezone.now()
        upcoming = self.queryset.filter(
            appointment_date__gte=now,
            status='scheduled'
        )
        serializer = self.get_serializer(upcoming, many=True)
        return Response(serializer.data)
    
    def perform_update(self, serializer):
        """Ao atualizar, registra mudança"""
        serializer.save()
```

### 4. urls.py

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AppointmentViewSet

app_name = 'appointments'

router = DefaultRouter()
router.register(r'appointments', AppointmentViewSet, basename='appointment')

urlpatterns = [
    path('', include(router.urls)),
]
```

### 5. admin.py

```python
from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient_name', 'professional', 'appointment_date', 'status']
    list_filter = ['status', 'appointment_date']
    search_fields = ['patient_name', 'professional__social_name']
    ordering = ['-appointment_date']
    
    fieldsets = (
        ('Informações', {
            'fields': ('professional', 'patient_name', 'appointment_date')
        }),
        ('Status', {
            'fields': ('status', 'notes')
        }),
        ('Auditoria', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
```

## Testar a API

```bash
# Listar todas consultas
curl http://localhost:8000/api/appointments/

# Agendar nova consulta
curl -X POST http://localhost:8000/api/appointments/ \
  -H "Content-Type: application/json" \
  -d '{
    "professional_id": "uuid-do-profissional",
    "appointment_date": "2026-06-15T14:30:00Z",
    "patient_name": "João Silva",
    "status": "scheduled"
  }'

# Consultas futuras
curl http://localhost:8000/api/appointments/upcoming/

# Consultas de um profissional
curl http://localhost:8000/api/appointments/by-professional/uuid-profissional/
```

## Testes (tests.py)

```python
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import timedelta
from django.utils import timezone
from professionals.models import Professional
from .models import Appointment

class AppointmentTests(APITestCase):
    def setUp(self):
        self.prof = Professional.objects.create(
            social_name="Dr. João",
            profession="Médico",
            address="Rua X",
            contact="11999999999"
        )
        self.future_date = timezone.now() + timedelta(days=7)
    
    def test_create_appointment(self):
        data = {
            "professional_id": str(self.prof.id),
            "patient_name": "Maria Silva",
            "appointment_date": self.future_date.isoformat(),
            "status": "scheduled"
        }
        response = self.client.post('/api/appointments/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_cannot_schedule_past_date(self):
        past_date = timezone.now() - timedelta(days=1)
        data = {
            "professional_id": str(self.prof.id),
            "patient_name": "Maria Silva",
            "appointment_date": past_date.isoformat(),
        }
        response = self.client.post('/api/appointments/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
```

## Checklist (Dia 3)

- [ ] Model com FK para Professional criado
- [ ] Relacionamento bidirecional funcionando
- [ ] Serializer com validações
- [ ] ViewSet com ações customizadas
- [ ] Testes de agendamento
- [ ] Filtro por profissional funcionando
- [ ] Admin decorado e pronto

---

**Próximo**: Vá para `app/authentication/HELP.md`
