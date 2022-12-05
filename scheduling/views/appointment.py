from rest_framework import generics

from ..models import Appointment
from ..serializers.Appointment import AppointmentSerializer


class AppointmentCreateAPIView(generics.CreateAPIView):
	serializer_class = AppointmentSerializer
	queryset = Appointment.objects.all()

	def perform_create(self, serializer):
		print(serializer.validated_data)
		serializer.save(user=self.request.user)
