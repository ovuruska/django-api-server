from rest_framework import serializers

from scheduling.models.customer import Customer


class CustomerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Customer
		fields = ('id','name', 'phone', 'email', 'address','uid')


class CustomerEmployeeSerializer(serializers.ModelSerializer):

	lifetime_invoice = serializers.SerializerMethodField()

	def get_lifetime_invoice(self, obj):
		return obj.lifetime_invoice()
	class Meta:
		model = Customer
		fields = ('id','name', 'phone', 'email', 'address','uid','lifetime_invoice')