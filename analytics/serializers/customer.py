from rest_framework import serializers

from analytics.models.customer import TopCustomer


class TopCustomerSerializer(serializers.ModelSerializer):


	class Meta:
		model = TopCustomer
		fields = "__all__"

	def get_total(self, obj):
		total = obj.get_total()
		return total