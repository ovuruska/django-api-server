from django.core.validators import MinLengthValidator
from rest_framework import serializers

from scheduling.models import EmployeeWorkingHour
from scheduling.serializers.Branch import BranchSerializer
from scheduling.serializers.Employee import EmployeeSerializer, EmployeeShallowSerializer


class EmployeeWorkingHourSerializer(serializers.ModelSerializer):
	"""
	Serializer for EmployeeWorkingHour model

	"""

	class Meta:
		"""
		Metaclass for EmployeeWorkingHourSerializer
		"""
		model = EmployeeWorkingHour
		fields = ["employee", "date",  "branch", "start", "end"]


class WorkingDaySerializer(serializers.Serializer):
	working_hours = serializers.CharField(max_length=24,validators=[MinLengthValidator(24)])
	branch = BranchSerializer(allow_null=True,many=False)
	date = serializers.DateField()
	class Meta:
		fields = ["working_hours","branch","date"]
		depth = 1


class EmployeeWorkingHourRetrieveSerializer(serializers.Serializer):
	start = serializers.DateField()
	end = serializers.DateField()
	employee = EmployeeShallowSerializer(read_only=True,many=False)
	working_hours = WorkingDaySerializer(many=True,allow_null=True)

	class Meta:
		fields = ["start","end","employee","working_hours"]
		depth = 1

