from rest_framework import serializers
from scheduling.models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):


	class Meta:
		model = Appointment
		fields = '__all__'