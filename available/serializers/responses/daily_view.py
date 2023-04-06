from django.apps import apps
from rest_framework import serializers

from scheduling.serializers.Branch import BranchSerializer
from scheduling.serializers.Employee import EmployeeShallowSerializer


class BranchNameSerializer(serializers.ModelSerializer):
	id = serializers.IntegerField()
	class Meta:
		model = apps.get_model('scheduling', 'Branch')
		fields = ('id','name')

class EmployeeNameSerializer(serializers.ModelSerializer):
	id = serializers.IntegerField()
	class Meta:
		model = apps.get_model('scheduling', 'Employee')
		fields = ('id','name')

class DailyViewResponseSerializer(serializers.Serializer):

	start = serializers.DateTimeField()
	end = serializers.DateTimeField()
	employee = EmployeeShallowSerializer()
	branch = BranchSerializer()

	# Invalidate the serializer if the start date is after the end date
	# Invalidate if extra fields are passed.
	# Invalidate if the start or end date is not in the correct format
	# Invalidate if the employee or branch is not an integer
	# Invalidate if the employee or branch is not a positive integer
	def validate(self, data):
		if data['start'] > data['end']:
			raise serializers.ValidationError('The start date must be before the end date.')

		if set(data.keys()) != {'start', 'end', 'employee', 'branch'}:
			raise serializers.ValidationError('The serializer must only have the start, end, employee, and branch fields.')
		return data

