from rest_framework import generics

from ..models import Appointment
from ..serializers.Appointment import AppointmentSerializer


class AppointmentCreateAPIView(generics.CreateAPIView):
	serializer_class = AppointmentSerializer
	queryset = Appointment.objects.all()

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)
