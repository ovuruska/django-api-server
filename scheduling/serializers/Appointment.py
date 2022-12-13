from rest_framework import serializers
from scheduling.models import Appointment


class AppointmentCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Appointment
		fields = ('customer', 'dog', 'customer_notes', 'services', 'products', 'branch','start','end','employee')
		extra_kwargs = {"employee": {"required": False, "allow_null": True}}


class AppointmentEmployeeSerializer(serializers.ModelSerializer):


	class Meta:
		model = Appointment
		fields = '__all__'


class AppointmentCustomerRetrieveSerializer(serializers.ModelSerializer):
	class Meta:
		model = Appointment
		fields = ['id', 'start', 'end', 'customer_notes','services','products', 'tip', 'cost', 'branch', 'employee']