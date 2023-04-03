from rest_framework import serializers


class CapacityBaseResponseSerializer(serializers.Serializer):

	date = serializers.DateField()
	morning_capacity = serializers.FloatField()
	afternoon_capacity = serializers.FloatField()

	class Meta:
		fields = ('date', 'morning_capacity', 'afternoon_capacity')
