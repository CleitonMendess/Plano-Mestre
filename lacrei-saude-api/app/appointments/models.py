import uuid

from django.db import models
from app.professionals.models import Professional


class AppointmentStatusChoices(models.TextChoices):
    SCHEDULED = 'scheduled', 'Agendada'
    COMPLETED = 'completed', 'Concluída'
    CANCELLED = 'cancelled', 'Cancelada'
    NO_SHOW = 'no_show', 'Faltou'


class Appointment(models.Model):
    """Representa uma consulta médica agendada."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    professional = models.ForeignKey(
        Professional,
        on_delete=models.CASCADE,
        related_name='appointments'
    )
    appointment_date = models.DateTimeField()
    patient_name = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=AppointmentStatusChoices.choices,
        default=AppointmentStatusChoices.SCHEDULED,
    )
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['appointment_date']
        verbose_name = 'Appointment'
        verbose_name_plural = 'Appointments'
        unique_together = ('professional', 'appointment_date')

    def __str__(self):
        return f'{self.patient_name} com {self.professional.social_name} em {self.appointment_date}'
