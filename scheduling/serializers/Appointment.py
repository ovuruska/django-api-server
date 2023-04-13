from rest_framework import serializers

from scheduling.models import Appointment
from scheduling.selectors import get_last_appointment_by_same_dog
from scheduling.serializers.Branch import BranchSerializer
from scheduling.serializers.Customer import CustomerSerializer
from scheduling.serializers.Dog import DogSerializer, DogShallowSerializer
from scheduling.serializers.Employee import EmployeeSerializer, EmployeeShallowSerializer
from scheduling.serializers.Product import ProductSerializer
from scheduling.serializers.Service import ServiceSerializer

class AppointmentEmployeeCreateSerializer(serializers.ModelSerializer):
	dog_name = serializers.CharField(source="dog_name", read_only=True)
	customer_name = serializers.CharField(source="customer_name", read_only=True)
	class Meta:
		model = Appointment
		fields = [
			"employee",
			"start",
			"end",
		]
		extra_kwargs = {"employee": {"required": True, "allow_null": False}}



class AppointmentCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Appointment
		fields = '__all__'
		extra_kwargs = {"employee": {"required": False, "allow_null": True}}


class AppointmentModifySerializer(serializers.ModelSerializer):
	class Meta:
		model = Appointment
		fields = '__all__'


class AppointmentEmployeeSerializer(serializers.ModelSerializer):
	employee = EmployeeSerializer()
	services = ServiceSerializer(many=True)
	products = ProductSerializer(many=True)
	branch = BranchSerializer()
	customer = CustomerSerializer()
	dog = DogSerializer()

	last_dog_appointment = serializers.SerializerMethodField()

	def get_last_dog_appointment(self, obj):

		last_appointment = get_last_appointment_by_same_dog(obj.dog.id, obj.start)
		if last_appointment is not None:
			return last_appointment.start
		else:
			return None

	class Meta:
		model = Appointment
		fields = '__all__'




class GroomerEmptySlotSerializer(serializers.ModelSerializer):
	class Meta:
		model = Appointment
		fields = ['start', 'end']