from rest_framework import serializers


class BaseRequestSerializer(serializers.Serializer):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		# Get the keys of the incoming data
		incoming_keys = set(self.initial_data.keys())

		# Get the keys of the allowed fields
		allowed_keys = set(self.fields.keys())

		# Check for extra fields
		extra_fields = incoming_keys - allowed_keys
		if extra_fields:
			# Set is_valid to false.
			self.is_valid = lambda : False

	SERVICE_CHOICES = [("Full Grooming", "Full Grooming"), ("We Wash", "We Wash")]

	employees = serializers.ListField(child=serializers.IntegerField(), required=False, default=[])
	branches = serializers.ListField(child=serializers.IntegerField(), required=False, default=[])
	service = serializers.ChoiceField(choices=SERVICE_CHOICES, required=True)
	date = serializers.CharField(required=True)