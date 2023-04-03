from django.apps import apps
from rest_framework import serializers

from capacity.serializers.responses.base import CapacityBaseResponseSerializer


class BranchNameSerializer(serializers.ModelSerializer):
	id = serializers.IntegerField()
	class Meta:
		model = apps.get_model('scheduling', 'Branch')
		fields = ('id','name')


class DailyCapacityResponseSerializer(CapacityBaseResponseSerializer):
	branch = BranchNameSerializer()

	class Meta:
		fields = ('date', 'morning_capacity', 'afternoon_capacity', 'branch')
