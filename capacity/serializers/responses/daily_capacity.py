from rest_framework import serializers

from capacity.serializers.responses.base import CapacityBaseResponseSerializer


class DailyCapacityResponseSerializer(CapacityBaseResponseSerializer):
	branch = serializers.IntegerField()
	class Meta:
		fields = ('date', 'morning_capacity', 'afternoon_capacity','branch')