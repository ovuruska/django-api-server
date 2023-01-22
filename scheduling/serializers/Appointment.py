from rest_framework import serializers
from scheduling.models import Appointment
from scheduling.selectors import get_last_appointment_by_same_dog, get_last_appointment_by_same_customer
from scheduling.serializers.Branch import BranchSerializer
from scheduling.serializers.Customer import CustomerSerializer
from scheduling.serializers.Dog import DogSerializer, DogShallowSerializer
from scheduling.serializers.Employee import EmployeeSerializer, EmployeeShallowSerializer
from scheduling.serializers.Product import ProductSerializer
from scheduling.serializers.Service import ServiceSerializer
from django.db import models


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
	last_customer_appointment = serializers.SerializerMethodField()


	def get_last_dog_appointment(self, obj):

		last_appointment = get_last_appointment_by_same_dog(obj.dog.id)
		if last_appointment is not None:
			return last_appointment.start
		else:
			return None

	def get_last_customer_appointment(self, obj):
		last_appointment = get_last_appointment_by_same_customer(obj.dog.id)
		if last_appointment is not None:
			return last_appointment.start
		else:
			return None
	class Meta:
		model = Appointment
		fields = '__all__'


class AppointmentCustomerRetrieveSerializer(serializers.ModelSerializer):
	services = ServiceSerializer(many=True)
	products = ProductSerializer(many=True)
	branch = BranchSerializer()
	employee = EmployeeShallowSerializer()
	customer = CustomerSerializer()
	dog = DogShallowSerializer()

	class Meta:
		model = Appointment
		fields = ['id', 'start','dog', 'end', 'customer_notes','services','products', 'tip', 'cost', 'branch','customer', 'employee','status']

