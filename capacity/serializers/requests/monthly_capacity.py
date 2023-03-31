from django.core.exceptions import ValidationError
from rest_framework import serializers


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


class MonthlyCapacityRequestSerializer(serializers.Serializer):
	SERVICE_CHOICES = [("Full Grooming", "Full Grooming"), ("We Wash", "We Wash")]

	employees = serializers.ListField(child=serializers.IntegerField(), required=False, default=[])
	branches = serializers.ListField(child=serializers.IntegerField(), required=False, default=[])
	service = serializers.ChoiceField(choices=SERVICE_CHOICES, required=True)
	date = serializers.CharField(required=True, validators=[validate_date_format])

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		# Get the keys of the incoming data
		incoming_keys = set(self.initial_data.keys())

		# Get the keys of the allowed fields
		allowed_keys = set(self.fields.keys())

		# Check for extra fields
		extra_fields = incoming_keys - allowed_keys
		if extra_fields:
			# Raise a validation error with an appropriate message
			raise serializers.ValidationError(
				f"The following fields are not allowed: {', '.join(extra_fields)}"
			)