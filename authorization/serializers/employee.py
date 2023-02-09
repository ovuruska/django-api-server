from django.apps import apps
from rest_framework import serializers


class EmployeeSerializer(serializers.ModelSerializer):
	class Meta:
		model = apps.get("scheduling.Employee")
		fields = '__all__'