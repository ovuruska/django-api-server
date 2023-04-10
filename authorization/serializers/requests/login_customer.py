from rest_framework import serializers


class LoginCustomerRequestSerializer(serializers.Serializer):
	email = serializers.EmailField()
	password = serializers.CharField()