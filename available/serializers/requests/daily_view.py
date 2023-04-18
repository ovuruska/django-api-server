import datetime

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import Serializer


class DailyViewRequestSerializer(Serializer):
	"""
	employees (optional): A list of integers representing the employee IDs. Default is an empty list [].
branches (optional): A list of integers representing the branch IDs. Default is an empty list [].
service (required): A string representing the service name. "We Wash" | "Full Grooming"
date (required): A string representing the target date in the format YYYY-mm-dd.

Service must be one of the following:
	1- "We Wash"
	2- "Full Grooming"
	"""

	employees = serializers.ListField(child=serializers.IntegerField(), required=False, default=[])
	branches = serializers.ListField(child=serializers.IntegerField(), required=False, default=[])
	service = serializers.CharField(required=True, max_length=50,)

	date = serializers.DateField(required=True)
	duration = serializers.IntegerField(required=False, default=60)

	def validate(self, data):
		# Validate the date
		if data['service'] not in ['We Wash', 'Full Grooming','Grooming']:
			raise ValidationError('The service must be either "We Wash" or "Full Grooming".')
		if data['duration'] < 0:
			raise ValidationError('The duration must be at least 60 minutes.')

		return data
