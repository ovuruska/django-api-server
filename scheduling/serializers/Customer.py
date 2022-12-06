from rest_framework import serializers

from scheduling.models.Customer import Customer


class CustomerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Customer
		fields = ('name', 'phone', 'email', 'address','dogs','uid')