from datetime import timedelta

from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from app.professionals.models import Professional
from app.appointments.models import Appointment


class APIFullWorkflowTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        self.professional = Professional.objects.create(
            social_name='Dra. Maria Silva',
            profession='Cardiologista',
            address='Rua das Flores, 123',
            contact='11999999999',
        )
        self.future_date = timezone.now() + timedelta(days=7)

    def test_professional_crud_and_appointment_flow(self):
        create_data = {
            'social_name': 'Dr. João',
            'profession': 'Médico',
            'address': 'Rua X, 45',
            'contact': '11988887777',
        }
        response = self.client.post('/api/professionals/', create_data, format='json')
        self.assertEqual(response.status_code, 201)
        professional_id = response.data['id']

        response = self.client.get('/api/professionals/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(any(item['id'] == professional_id for item in response.data))

        appointment_data = {
            'professional_id': self.professional.id,
            'appointment_date': self.future_date.isoformat(),
            'patient_name': 'Paciente Teste',
            'status': 'scheduled',
        }
        response = self.client.post('/api/appointments/', appointment_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['patient_name'], 'Paciente Teste')

        response = self.client.get(f'/api/appointments/by-professional/{self.professional.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data) >= 1)

    def test_access_requires_authentication(self):
        self.client.credentials()  # remove token
        response = self.client.get('/api/professionals/')
        self.assertEqual(response.status_code, 401)
