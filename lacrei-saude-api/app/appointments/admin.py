from django.contrib import admin

from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'professional', 'appointment_date', 'status')
    list_filter = ('status', 'appointment_date')
    search_fields = ('patient_name', 'professional__social_name')
    ordering = ('-appointment_date',)
