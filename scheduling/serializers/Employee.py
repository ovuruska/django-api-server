from rest_framework import serializers

from scheduling.models import Employee
from scheduling.serializers.Branch import BranchSerializer


class EmployeeSerializer(serializers.ModelSerializer):
	class Meta:
		model = Employee
		fields = '__all__'

class EmployeeUserRetrieveSerializer(serializers.ModelSerializer):

	class Meta:
		model = Employee
		fields = ('id','name', 'email')

class EmployeeFilterSerializer(serializers.ModelSerializer):
	branch = BranchSerializer()


	class Meta:
		model = Employee
		fields = '__all__'
