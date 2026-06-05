from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Appointment
from .serializers import AppointmentSerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    """API CRUD para consultas médicas."""

    queryset = Appointment.objects.select_related('professional').all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['patient_name', 'professional__social_name']
    ordering = ['appointment_date']

    @action(detail=False, methods=['get'], url_path=r'by-professional/(?P<professional_id>[0-9a-f-]+)')
    def by_professional(self, request, professional_id=None):
        appointments = self.get_queryset().filter(professional_id=professional_id)
        serializer = self.get_serializer(appointments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='upcoming')
    def upcoming(self, request):
        from django.utils import timezone

        now = timezone.now()
        appointments = self.get_queryset().filter(appointment_date__gte=now, status='scheduled')
        serializer = self.get_serializer(appointments, many=True)
        return Response(serializer.data)
