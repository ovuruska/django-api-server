from scheduling.models import Product
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
	"""Serializer for product objects."""

	class Meta:
		model = Product
		fields = "__all__"



