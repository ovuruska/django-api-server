from rest_framework import serializers
from scheduling.models import Appointment


class AppointmentCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Appointment
		fields = ('customer', 'dog', 'customer_notes', 'services', 'products', 'branch','start_time','end_time','employee')
		extra_kwargs = {"employee": {"required": False, "allow_null": True}}


class AppointmentEmployeeSerializer(serializers.ModelSerializer):


	class Meta:
		model = Appointment
		fields = '__all__'


class AppointmentCustomerRetrieveSerializer(serializers.ModelSerializer):
	class Meta:
		model = Appointment
		fields = ['id', 'start_time', 'end_time', 'customer_notes','services','products', 'tip', 'cost', 'branch', 'employee']