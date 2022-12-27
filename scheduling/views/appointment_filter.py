from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from scheduling.models import Appointment
from scheduling.serializers.Appointment import AppointmentEmployeeSerializer


class AppointmentFilterListView(generics.ListAPIView):
	queryset = Appointment.objects.all()
	serializer_class = AppointmentEmployeeSerializer
	filter_backends = [DjangoFilterBackend]
	filterset_fields = ["employee__name", "appointment_type", "branch__name", "dog__breed", "created_at", "status",
	                    "start", "appointment_type"]
