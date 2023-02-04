from rest_framework import serializers
from scheduling.models.branch_working_hour import BranchWorkingHour

class BranchWorkingHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = BranchWorkingHour
        fields = ['weekday','date', 'branch', 'workingHours']

