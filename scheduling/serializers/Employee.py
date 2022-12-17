from rest_framework import serializers

from scheduling.models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
	class Meta:
		model = Employee
		fields = '__all__'

class EmployeeUserRetrieveSerializer(serializers.ModelSerializer):

	class Meta:
		model = Employee
		fields = ('id','name', 'email')
