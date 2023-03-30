from rest_framework import serializers


class MonthlyCapacitySerializer(serializers.Serializer):
	date = serializers.DateField()
	branch = serializers.IntegerField()
	employee = serializers.IntegerField()

