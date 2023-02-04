from rest_framework import serializers

from scheduling.models import EmployeeWorkingHour


class EmployeeWorkingHourSerializer(serializers.ModelSerializer):
	"""
	Serializer for EmployeeWorkingHour model

	"""



	class Meta:
		"""
		Metaclass for EmployeeWorkingHourSerializer
		"""
		model = EmployeeWorkingHour
		fields = "__all__"
