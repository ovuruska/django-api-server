from rest_framework import serializers


class MonthlyCapacityRequestSerializer(serializers.Serializer):
    employees = serializers.ListField(child=serializers.IntegerField(), required=False, default=[])
    branches = serializers.ListField(child=serializers.IntegerField(), required=False, default=[])
    service = serializers.CharField(required=True)
    date = serializers.CharField(required=True)