from django.core.exceptions import ValidationError
from rest_framework import serializers

from capacity.serializers.requests.base import BaseRequestSerializer


def validate_date_format(value):
	try:
		# Attempt to parse the date string
		month, year = value.split('/')
		month = int(month)
		year = int(year)
	except ValueError:
		# If the string cannot be parsed, raise a validation error
		raise ValidationError('Invalid date format. Use "MM/YYYY".')

	# Check that the month and year values are within a valid range
	if month < 1 or month > 12:
		raise ValidationError('Invalid month value.')
	if year < 1900 or year > 9999:
		raise ValidationError('Invalid year value.')

	# If the function completes without raising an error, return the validated value
	return value


class MonthlyCapacityRequestSerializer(BaseRequestSerializer):
	date = serializers.CharField(required=True, validators=[validate_date_format])
