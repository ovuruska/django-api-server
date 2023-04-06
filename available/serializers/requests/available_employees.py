from rest_framework import serializers


class AvailableEmployeesRequestSerializer(serializers.Serializer):
	date = serializers.DateTimeField()
	branches = serializers.ListField(child=serializers.IntegerField(), required=False)
	service = serializers.CharField()
	times = serializers.ListField(child=serializers.CharField(), required=False)

