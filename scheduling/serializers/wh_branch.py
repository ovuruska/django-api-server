from rest_framework import serializers

from scheduling.models.branch_wh import BranchWorkingHour


class BranchWorkingHourSerializer(serializers.ModelSerializer):
	class Meta:
		model = BranchWorkingHour
		fields = "__all__"
