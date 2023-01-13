from rest_framework import serializers
from scheduling.models import Branch

"""
name = models.CharField(max_length=256)
address = models.CharField(max_length=256)
description = models.CharField(max_length=256)
tubs = models.IntegerField()

"""


class BranchSerializer(serializers.ModelSerializer):
	class Meta:
		model = Branch
		fields = "__all__"


class FreeHoursSerializer(serializers.Serializer):
	free_hours = serializers.ListField(child=serializers.DateTimeField())