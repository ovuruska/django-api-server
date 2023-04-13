from django.apps import apps
from rest_framework import serializers

from scheduling.serializers.Branch import BranchSerializer
from scheduling.serializers.Customer import CustomerSerializer
from scheduling.serializers.Dog import DogShallowSerializer
from scheduling.serializers.Employee import EmployeeUserRetrieveSerializer
from scheduling.serializers.Product import ProductSerializer

Appointment = apps.get_model('scheduling', 'Appointment')


class CustomerAppointmentResponseSerializer(serializers.ModelSerializer):
	products = ProductSerializer(many=True)
	branch = BranchSerializer()
	employee = EmployeeUserRetrieveSerializer()
	customer = CustomerSerializer()
	dog = DogShallowSerializer()

	class Meta:
		model = Appointment
		fields = ['id', 'start', 'dog', 'end', 'customer_notes',  'products', 'tip', 'cost', 'branch',
		          'customer', 'employee', 'status']
