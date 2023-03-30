from rest_framework import serializers


class MonthlyCapacityResponseSerializer(serializers.Serializer):
	date = serializers.DateField()
	branch = serializers.IntegerField()
	employee = serializers.IntegerField()

