from rest_framework import serializers

from app.professionals.serializers import ProfessionalSerializer
from .models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
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
            'updated_at',
        ]
        read_only_fields = ['id', 'professional', 'created_at', 'updated_at']

    def validate_appointment_date(self, value):
        from django.utils import timezone

        if value < timezone.now():
            raise serializers.ValidationError('A data da consulta não pode ser no passado.')
        return value

    def create(self, validated_data):
        professional_id = validated_data.pop('professional_id')
        appointment = Appointment.objects.create(
            professional_id=professional_id,
            **validated_data,
        )
        return appointment
