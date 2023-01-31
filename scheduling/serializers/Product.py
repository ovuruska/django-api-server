from rest_framework import serializers

from scheduling.models import Product


class ProductSerializer(serializers.ModelSerializer):
	"""Serializer for product objects."""

	class Meta:
		model = Product
		fields = "__all__"


class ProductRetrieveSerializer(serializers.ModelSerializer):
	"""Serializer for product retrieval."""

	class Meta:
		model = Product
		fields = ["id", "name", "cost", "description", "category"]
