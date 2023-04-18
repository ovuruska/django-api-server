from datetime import datetime

from rest_framework import serializers

ALLOWED_SERVICES = ["Grooming", "We Wash"]

class CustomerAppointmentRequestSerializer(serializers.Serializer):
	# Appointment fields
	# ...

	pet = serializers.IntegerField()
	products = serializers.ListField(child=serializers.IntegerField(), default=[], allow_null=True)
	start = serializers.DateTimeField()
	branch = serializers.IntegerField()
	service = serializers.CharField()
	employee = serializers.IntegerField(default=None, allow_null=True)
	customer_notes = serializers.CharField(default="", allow_null=True)

	# Check if service is Grooming, employee should not ne null
	# Check if service is not Grooming, employee can be null.

	def validate(self, data):
		# Check if service is Grooming, employee should not ne null
		# Check if service is not Grooming, employee can be null.

		service = data.get("service")
		employee = data.get("employee",None)
		start = data.get("start")
		# Start should be in the future
		if start < datetime.now(tz=start.tzinfo):
			raise serializers.ValidationError("Start should be in the future")

		if service == "Grooming" or service == "Full Grooming":
			if employee is None:
				raise serializers.ValidationError("Employee is required for grooming service")


		if service not in ALLOWED_SERVICES:
			raise serializers.ValidationError("Service not allowed")

		return data