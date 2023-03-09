from rest_framework import serializers

from scheduling.models import Employee
from scheduling.serializers.Branch import BranchSerializer


class EmployeeModifySerializer(serializers.ModelSerializer):
	class Meta:
		model = Employee
		fields = ('name', 'email', 'phone', 'branch', 'role')

class EmployeeShallowSerializer(serializers.ModelSerializer):
	class Meta:
		model = Employee
		fields = ('id', 'name', 'email', 'phone', 'branch', 'role','created_at','updated_at')

class EmployeeSerializer(serializers.ModelSerializer):
	branch = BranchSerializer(allow_null=True, required=False)
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

class EmployeeWorkingHoursSerializer(serializers.ModelSerializer):
	class Meta:
		model = Employee
		fields = ('date', 'start', 'end', 'branch')

