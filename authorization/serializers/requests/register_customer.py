from rest_framework import serializers


class RegisterCustomerRequestSerializer(serializers.Serializer):
	email = serializers.EmailField()
	password = serializers.CharField()
	first_name = serializers.CharField()
	last_name = serializers.CharField()

