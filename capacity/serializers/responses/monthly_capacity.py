from rest_framework import serializers


class MonthlyCapacityResponseSerializer(serializers.Serializer):
	"""
	{
    "date": "2020-01-01",
    "morning_capacity": 0.6,
    "afternoon_capacity": 0.8
  }
	"""
	date = serializers.DateField()
	morning_capacity = serializers.FloatField()
	afternoon_capacity = serializers.FloatField()

	class Meta:
		fields = ('date', 'morning_capacity', 'afternoon_capacity')
