from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Professional
from .serializers import ProfessionalSerializer


class ProfessionalViewSet(viewsets.ModelViewSet):
    """API CRUD para profissionais de saúde."""

    queryset = Professional.objects.all()
    serializer_class = ProfessionalSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    lookup_value_regex = '[0-9a-f-]+'
