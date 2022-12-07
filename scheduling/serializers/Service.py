from scheduling.models import Service
from rest_framework import serializers


class ServiceSerializer(serializers.ModelSerializer):
	"""Serializer for service objects."""

	class Meta:
		model = Service
		fields = "__all__"



