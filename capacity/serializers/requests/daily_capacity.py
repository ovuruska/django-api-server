from django.core.exceptions import ValidationError
from rest_framework import serializers

from capacity.serializers.requests.monthly_capacity import MonthlyCapacityRequestSerializer


def validate_date_format(value):
	# Check if the date string is in the correct format
	try:
		year,month,day = value.split('-')
		day = int(day)
		month = int(month)
		year = int(year)
	except ValueError:
		# If the string cannot be parsed, raise a validation error
		raise ValidationError('Invalid date format. Use "YYYY-MM-DD".')


class DailyCapacityRequestSerializer(MonthlyCapacityRequestSerializer):
	date = serializers.CharField(required=True, validators=[validate_date_format])

