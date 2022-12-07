from rest_framework import serializers

from scheduling.models.Customer import Customer


class CustomerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Customer
		fields = ('id','name', 'phone', 'email', 'address','uid')