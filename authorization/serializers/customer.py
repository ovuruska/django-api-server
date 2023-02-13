from django.apps import apps
from rest_framework import serializers


class CustomerSeralizer(serializers.ModelSerializer):
	class Meta:
		model = apps.get("scheduling.Customer")
		fields = '__all__'