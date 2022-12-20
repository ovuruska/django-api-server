from rest_framework import serializers
from scheduling.models import Appointment
from scheduling.serializers.Branch import BranchSerializer
from scheduling.serializers.Customer import CustomerSerializer
from scheduling.serializers.Dog import DogSerializer
from scheduling.serializers.Employee import EmployeeSerializer
from scheduling.serializers.Product import ProductSerializer
from scheduling.serializers.Service import ServiceSerializer


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
	services = ServiceSerializer(many=True)
	products = ProductSerializer(many=True)
	branch = BranchSerializer()
	employee = EmployeeSerializer()
	customer = CustomerSerializer()
	dog = DogSerializer()

	class Meta:
		model = Appointment
		fields = ['id', 'start','dog', 'end', 'customer_notes','services','products', 'tip', 'cost', 'branch','customer', 'employee','status']

